from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import uuid1

allowed_hosts = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
]


server_host = "127.0.0.1"
server_port = 8000

connection_update_time = 10000

name = uuid1()
templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")


def get_server_url():
    return f"http://{server_host}:{server_port}"