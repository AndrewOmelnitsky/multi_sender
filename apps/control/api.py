from fastapi import WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

import config
from config import templates
from services.utils import get_all_nodes_hosts
from services.websocket_manager import ws_manager
from services import nodes_api
from apps.models import Message, Mail, ControlMessage


router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    all_nodes = get_all_nodes_hosts()

    active_nodes = await nodes_api.get_active_nodes(all_nodes)
    active_nodes_names = await nodes_api.get_nodes_names(active_nodes)

    # FIXME:
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


@router.get("/get_active_nodes/")
async def get_active_nodes_view():
    checked_nodes = get_all_nodes_hosts()
    nodes = await nodes_api.get_active_nodes(checked_nodes)
    return {"active_nodes": nodes}


@router.post("/send_mail/")
async def send_mail(message: Message):
    mail = Mail(
        text=message.text,
        sender_name=str(config.name),
    )

    nodes = []
    for node_name in message.receivers:
        try:
            nodes.append(url_by_name[node_name])
        except:
            ...

    await nodes_api.send_mail_to_receivers(nodes, mail)

    mail_to_control = ControlMessage(
        type="your",
        sender_name=mail.sender_name,
        text=mail.text,
    )
    await ws_manager.broadcast(mail_to_control.json())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)