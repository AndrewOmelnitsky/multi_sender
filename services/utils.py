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


def get_next_node():
    min_node = [float('inf'), None]
    next_node = [float('inf'), None]
    
    for current_node in config.allowed_hosts:
        (host, port, priority, *other) = current_node
        
        if min_node[0] > priority:
            min_node = [priority, current_node]
            
        if next_node[0] > priority and priority > config.server_priority:
            next_node = [priority, current_node]
    
    # print(config.allowed_hosts)
    # print(config.server_priority)
    # print(next_node)
    # print(min_node)
    if next_node[1] is None:
        next_node = min_node
        
    return next_node[1]
    
next_node = get_next_node()


def get_prev_node():
    max_node = [-1, None]
    prev_node = [-1, None]
    
    for current_node in config.allowed_hosts:
        (host, port, priority, *other) = current_node
        
        if max_node[0] < priority:
            max_node = [priority, current_node]
            
        if prev_node[0] < priority and priority < config.server_priority:
            prev_node = [priority, current_node]
            
    if prev_node[1] is None:
        prev_node = max_node
        
    return prev_node[1]
    
prev_node = get_next_node()