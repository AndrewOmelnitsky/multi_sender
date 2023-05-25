import time

from pydantic import BaseModel, Field
from services.lamport_clock import lamport_clock


class Transaction(BaseModel):
    sender_name: str
    sender_clock: int
    receiver_name: str
    receiver_clock: int


class Mail(BaseModel):
    text: str
    sender_name: str
    author_name: str
    is_cycle: bool = False
    time: float = Field(default_factory=time.time)
    lamport_clock: int = Field(default_factory=lamport_clock.get)


class Message(BaseModel):
    text: str
    receivers: list[str]


class ControlMessage(BaseModel):
    type: str
    text: str
    sender_name: str
    time: float


class ActiveNode(BaseModel):
    url: str
    name: str


class ActiveNodes(BaseModel):
    active_nodes: list[ActiveNode] = []
