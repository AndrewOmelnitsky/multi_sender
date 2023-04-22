import subprocess


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


def waiting_for_exit():
    while True:
        try:
            input()
        except KeyboardInterrupt:
            return


def main():
    test_config = [
        ("Server 1", 8000),
        ("Server 2", 8001),
        ("Server 3", 8002),
    ]

    with ProcessManager() as process_manager:
        for name, port in test_config:
            process = subprocess.Popen(["python", "main.py", name, str(port)])
            process_manager.add(process)

        waiting_for_exit()


if __name__ == "__main__":
    main()
