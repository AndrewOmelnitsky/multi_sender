import config


def collect_url(host, port):
    return f"http://{host}:{port}"


def get_all_nodes_hosts():
    all_nodes = []
    for current_node in config.allowed_hosts:
        # print(f"{current_node=}")
        (host, port, *other) = current_node
        # print(f"{host=}")
        # print(f"{port=}")
        # print(f"{other=}")
        
        if config.server_host == host and config.server_port == port:
            continue
        
        all_nodes.append(collect_url(host, port))

    return all_nodes


