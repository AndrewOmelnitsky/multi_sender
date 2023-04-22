from pydantic import BaseModel


class Mail(BaseModel):
    text: str
    sender_name: str


class Message(BaseModel):
    text: str
    receivers: list[str]


class ControlMessage(BaseModel):
    type: str
    text: str
    sender_name: str
