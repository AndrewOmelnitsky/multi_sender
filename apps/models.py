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


class ActiveNode(BaseModel):
    url: str
    name: str


class ActiveNodes(BaseModel):
    active_nodes: list[ActiveNode] = []
