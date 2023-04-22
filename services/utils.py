import config


def get_all_nodes_hosts():
    all_nodes = config.allowed_hosts.copy()
    try:
        all_nodes.remove(config.get_server_url())
    except:
        ...

    return all_nodes
