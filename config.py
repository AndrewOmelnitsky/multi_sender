from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uuid import uuid1

allowed_hosts = [
    ("127.0.0.1", 8000, 1),
    ("127.0.0.1", 8001, 2),
    ("127.0.0.1", 8002, 3),
]

log_hosts = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
]

debug = False

server_host = "127.0.0.1"
server_port = 8000
server_priority = 1

connection_update_time = 10 * 1000

sleep_time_range = (3, 7)

name = uuid1()
templates = Jinja2Templates(directory="templates")
static_files = StaticFiles(directory="static")
