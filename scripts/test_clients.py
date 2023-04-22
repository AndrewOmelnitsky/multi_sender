import subprocess

EXIT_COMMAND = "exit"


def main():
    test_config = [
        ("Server 1", 8000),
        ("Server 2", 8001),
        ("Server 3", 8002),
    ]
    test_client_processes = []
    
    for name, port in test_config:
        process = subprocess.Popen(["python", "main.py", name, str(port)])
        test_client_processes.append(process)
    
    while True:
        value = input()
        if value == EXIT_COMMAND:
            break
        
        print(f"Wrong command: {value}. Write '{EXIT_COMMAND}' to close servers.")
    
    for process in test_client_processes:
        process.kill()
        
        
if __name__ == '__main__':
    main()