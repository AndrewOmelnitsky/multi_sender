import random
import time
import logging
from fastapi.routing import APIRouter

import config
from services.websocket_manager import ws_manager
from services.lamport_clock import lamport_clock
from apps.models import Mail, ControlMessage, Transaction
from services import nodes_api
from services.utils import get_all_nodes_hosts, collect_url, get_next_node, get_prev_node


logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/is_active/")
async def is_active():
    return {}


@router.get("/get_name/")
async def get_name():
    return {"name": config.name}


@router.post("/")
async def new_mail(mail: Mail):
    lamport_clock.update(mail.lamport_clock)
    
    mail_to_control = ControlMessage(
        type="other",
        sender_name=mail.sender_name,
        text=mail.text,
        time=mail.time,
    )

    logger_message = (
        f"\u001b[31mGot mail\u001b[0m\n\tfrom: {mail.sender_name}\n\ttext: {mail.text}"
    )
    logger_decor = "=" * 20
    logger.warning(logger_decor + "\n" + logger_message + "\n" + logger_decor)
    await ws_manager.broadcast(mail_to_control.json())
    
    new_transaction = Transaction(
        sender_name=mail.sender_name,
        sender_clock=mail.lamport_clock,
        receiver_name=config.name,
        receiver_clock=lamport_clock.get(),
    )
    await nodes_api.log_transaction(new_transaction)
    
    if mail.author_name != config.name:
        await cycle_send(mail)
    
    return {}


async def cycle_send(mail):
    all_nodes = get_all_nodes_hosts()
    active_nodes = await nodes_api.get_active_nodes(all_nodes)
    url_by_name = await nodes_api.get_nodes_names(active_nodes)
    
    mail = Mail(
        sender_name=mail.sender_name,
        author_name=mail.author_name,
        text=mail.text,
        is_cycle=True,
    )
    
    next_node = get_next_node()
    prev_node = get_prev_node()
    next_node_host = collect_url(next_node[0], next_node[1])
    prev_node_host = collect_url(prev_node[0], prev_node[1])
    
    print("=" * 20)
    print("server_port", config.server_port)
    print(prev_node_host)
    print(next_node_host)
    print(config.allowed_hosts)
    print(url_by_name)
    print("=" * 20)
    
    sender_name = mail.sender_name
    mail.sender_name = config.name
    host = url_by_name[sender_name]
    
    print(host, next_node_host)
    if prev_node_host != host:
        return 
    
    
    # idx = all_nodes.index(host) + 1
    # idx = idx % len(all_nodes)
    # next_node = all_nodes[idx]
    # print(sender_name, config.name, idx, next_node)
    
    # if idx == config.allowed_hosts.index(config.get_server_url()):
    #     return
    
    time.sleep(random.randint(*config.sleep_time_range))
    
    await nodes_api.send_mail_to_receivers([next_node_host, ], mail)