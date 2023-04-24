import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
import webbrowser
import json

from apps.control.api import router as control_router
from apps.mail.api import router as mail_router
import config
import sys


def configure():
    # create instance of the app
    app = FastAPI(title="multi_sender", debug=config.debug)

    # create the instance for the routes
    main_api_router = APIRouter()

    # set routes to the app instance
    main_api_router.include_router(mail_router, prefix="/mail", tags=["mails"])
    main_api_router.include_router(
        control_router, prefix="/control", tags=["ui", "controls"]
    )

    app.include_router(main_api_router)
    app.mount("/static", config.static_files, name="static")

    origins = [
        config.get_server_url(),
        f"ws://{config.server_host}:{config.server_port}",
    ]

    app = CORSMiddleware(
        app=app,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


def open_control_page():
    url = f"{config.get_server_url()}/control"
    webbrowser.open(url)


def main(name=None, port=None, allowed_hosts=None):
    config.allowed_hosts = allowed_hosts or config.allowed_hosts
    config.server_port = port or config.server_port
    config.name = name or config.name
    
    app = configure()
    open_control_page()
    uvicorn.run(app, host=config.server_host, port=config.server_port)


if __name__ == "__main__":
    # run app on the host and port
    name = None
    try:
        name = sys.argv[1]
    except:
        ...

    port = None
    try:
        port = int(sys.argv[2])
    except:
        ...
        
    allowed_hosts = None
    try:
        allowed_hosts = json.loads(sys.argv[3])
    except:
        ...

    main(name=name, port=port, allowed_hosts=allowed_hosts)
