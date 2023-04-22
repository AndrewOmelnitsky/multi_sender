from fastapi.routing import APIRouter

import config
from services.websocket_manager import ws_manager
from apps.models import Mail, ControlMessage

router = APIRouter()

@router.get("/is_active/")
async def is_active():
    return {}


@router.get("/get_name/")
async def get_name():
    return {"name": config.name}


@router.post("/")
async def new_mail(mail: Mail):
    mail_to_control = ControlMessage(
        type="other",
        sender_name=mail.sender_name,
        text=mail.text,
    )
    await ws_manager.broadcast(mail_to_control.json())
    return {}