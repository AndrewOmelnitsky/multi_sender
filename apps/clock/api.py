import logging
from fastapi.routing import APIRouter

import config
from pydantic import BaseModel, Field
from services.websocket_manager import ws_manager
from services.lamport_clock import lamport_clock
from services import nodes_api
from services.utils import get_all_nodes_hosts
from apps.models import Transaction


router = APIRouter()
transactions = []


@router.get("/get_clock/")
async def get_clock():
    return {"name": config.name, "clock": lamport_clock.get_history()}


@router.post("/add_transaction/")
async def add_transaction(transaction: Transaction):
    transactions.append([
        {
            "name": transaction.sender_name,
            "clock": transaction.sender_clock,
        },
        {
            "name": transaction.receiver_name,
            "clock": transaction.receiver_clock,
        },
    ])


@router.get("/get_statistics/")
async def get_statistics():
    clocks = []
    all_nodes = get_all_nodes_hosts()
    active_nodes = await nodes_api.get_active_nodes(all_nodes)
    
    clocks = await nodes_api.get_clocks_info(active_nodes)
    
    return {"clocks": clocks, "transactions": transactions}