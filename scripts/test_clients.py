import subprocess
import socket
import sys
import json
from pathlib import Path


class ProcessManager(object):
    def __init__(self):
        self._processes = []

    def __enter__(self):
        self._processes = []
        return self

    def __exit__(self, type, value, traceback):
        for process in self._processes:
            process.kill()

    def add(self, process):
        self._processes.append(process)


def is_port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


def waiting_for_exit():
    while True:
        try:
            input()
        except KeyboardInterrupt:
            return


def main(args=sys.argv):
    try:
        number_of_servers = int(args[1])
    except:
        number_of_servers = 3
    
    start_port = 8000
    servers_configs = []
    server_name_template = "Server {id}"
    server_host = "127.0.0.1"
    allowed_hosts = []
    
    for i in range(number_of_servers):
        while not is_port_open(start_port):
            start_port += 1
            
        servers_configs.append((
            server_name_template.format(id=i+1),
            start_port,
            i + 1,
        ))
        allowed_hosts.append((server_host, start_port, i + 1))
        start_port += 1

    project_dir = Path(__file__).resolve().parent.parent
    with ProcessManager() as process_manager:
        for name, port, priority in servers_configs:
            process = subprocess.Popen([
                "python",
                str(project_dir / "main.py"),
                name,
                str(port),
                str(priority),
                json.dumps(allowed_hosts),
            ])
            process_manager.add(process)

        waiting_for_exit()


if __name__ == "__main__":
    main()
