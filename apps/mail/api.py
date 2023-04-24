import logging
from fastapi.routing import APIRouter

import config
from services.websocket_manager import ws_manager
from apps.models import Mail, ControlMessage


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

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

    # print("Got mail")
    logger_message = (
        f"\u001b[31mGot mail\u001b[0m\n\tfrom: {mail.sender_name}\n\ttext: {mail.text}"
    )
    logger_decor = "=" * 20
    logger.warning(logger_decor + "\n" + logger_message + "\n" + logger_decor)
    await ws_manager.broadcast(mail_to_control.json())
    return {}
