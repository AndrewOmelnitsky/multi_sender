from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel
import aiohttp

import json

import config
from config import templates
from utils import get_all_nodes_hosts


class Mail(BaseModel):
    text: str
    sender_name: str
    
class Massege(BaseModel):
    text: str
    recivers: list[str]
    
class ControlMassege(BaseModel):
    type: str
    text: str
    sender_name: str
    
    
    

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


ws_manager = ConnectionManager()


control_router = APIRouter()
mail_router = APIRouter()

@control_router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    all_nodes = get_all_nodes_hosts()
    
    active_nodes = await get_active_nodes(all_nodes)
    active_nodes_names = await get_nodes_names(active_nodes)
    
    #FIXME:
    global url_by_name
    url_by_name = active_nodes_names
    
    context = {
        "request": request,
        "all_nodes": all_nodes,
        "active_nodes": active_nodes,
        "active_nodes_names": active_nodes_names,
        "connection_update_time": config.connection_update_time,
        "sever_name": config.name,
        "sever_url": config.get_server_url(),
    }

    return templates.TemplateResponse("index.html", context=context)


@control_router.get("/get_active_nodes/")
async def get_active_nodes_view():
    chacked_nodes = get_all_nodes_hosts()
    nodes = await get_active_nodes(chacked_nodes)
    return {"active_nodes": nodes}


@control_router.post("/send_mail/")
async def send_mail(massege: Massege):
    mail = Mail(
        text=massege.text,
        sender_name=str(config.name),
    )
    
    nodes = []
    for node_name in massege.recivers:
        try:
            nodes.append(url_by_name[node_name])
        except:
            ...
            
    await send_mail_to_recivers(nodes, mail)
    
    mail_to_control = ControlMassege(
        type="your",
        sender_name=mail.sender_name,
        text=mail.text,
    )
    await ws_manager.broadcast(mail_to_control.json())
    
    
@control_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@mail_router.get("/is_active/")
async def is_active():
    return {}


@mail_router.get("/get_name/")
async def get_name():
    return {"name": config.name}


@mail_router.post("/")
async def new_mail(mail: Mail):
    mail_to_control = ControlMassege(
        type="other",
        sender_name=mail.sender_name,
        text=mail.text,
    )
    await ws_manager.broadcast(mail_to_control.json())
    return {}


async def check_is_node_active(
    session: aiohttp.ClientSession,
    node_url: str,
    is_active_url: str = "{url}/mail/is_active/",
) -> bool:
    try:
        url = is_active_url.format(url=node_url)
        async with session.get(url) as response:
            if response.status != 200:
                return False
            
            return True
            
    except aiohttp.client_exceptions.ClientConnectorError:
        ...
    except Exception as e:
        print(e)
        print(type(e))
        
    return False


async def get_active_nodes(nodes_hosts):
    active_nodes = []
    
    async with aiohttp.ClientSession() as session:
        for node_url in nodes_hosts:
            if (await check_is_node_active(session, node_url)):
                active_nodes.append(node_url)
                
    return active_nodes


async def get_node_name(
    session: aiohttp.ClientSession,
    node_url: str,
    get_name_url: str = "{url}/mail/get_name/",
) -> str | None:
    try:
        url = get_name_url.format(url=node_url)
        async with session.get(url) as response:
            if response.status != 200:
                return None
            content = await response.json()
            return content["name"]
            
    except aiohttp.client_exceptions.ClientConnectorError:
        ...
    except Exception as e:
        print(e)
        print(type(e))
        
    return None


async def get_nodes_names(nodes_hosts):
    names_to_urls = {}
    
    async with aiohttp.ClientSession() as session:
        for node_url in nodes_hosts:
            name = await get_node_name(session, node_url)
            names_to_urls[name] = node_url
                
    return names_to_urls


async def send_mail_to_reciver(
    session: aiohttp.ClientSession,
    node_url: str,
    mail: Mail,
    send_mail_url: str = "{url}/mail/",
) -> bool:
    try:
        url = send_mail_url.format(url=node_url)
        async with session.post(url, json=mail.dict()) as response:
            if response.status != 200:
                return False

            return True
            
    except aiohttp.client_exceptions.ClientConnectorError:
        ...
    except Exception as e:
        print(e)
        print(type(e))
        
    return False


async def send_mail_to_recivers(recivers, mail):
    async with aiohttp.ClientSession() as session:
        for node_url in recivers:
            await send_mail_to_reciver(session, node_url, mail)
    