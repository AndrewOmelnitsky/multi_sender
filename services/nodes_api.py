import aiohttp
from apps.models import Mail

async def check_is_node_active(
    session: aiohttp.ClientSession,
    node_url: str,
    is_active_url: str = "{url}/mail/is_active/",
) -> bool:
    try:
        url = is_active_url.format(url=node_url)
        async with session.get(url) as response:
            if response.status != 200:
                return False

            return True

    except aiohttp.client_exceptions.ClientConnectorError:
        ...
    except Exception as e:
        print(e)
        print(type(e))

    return False


async def get_active_nodes(nodes_hosts):
    active_nodes = []

    async with aiohttp.ClientSession() as session:
        for node_url in nodes_hosts:
            if await check_is_node_active(session, node_url):
                active_nodes.append(node_url)

    return active_nodes


async def get_node_name(
    session: aiohttp.ClientSession,
    node_url: str,
    get_name_url: str = "{url}/mail/get_name/",
) -> str | None:
    try:
        url = get_name_url.format(url=node_url)
        async with session.get(url) as response:
            if response.status != 200:
                return None
            content = await response.json()
            return content["name"]

    except aiohttp.client_exceptions.ClientConnectorError:
        ...
    except Exception as e:
        print(e)
        print(type(e))

    return None


async def get_nodes_names(nodes_hosts):
    names_to_urls = {}

    async with aiohttp.ClientSession() as session:
        for node_url in nodes_hosts:
            name = await get_node_name(session, node_url)
            names_to_urls[name] = node_url

    return names_to_urls


async def send_mail_to_receiver(
    session: aiohttp.ClientSession,
    node_url: str,
    mail: Mail,
    send_mail_url: str = "{url}/mail/",
) -> bool:
    try:
        url = send_mail_url.format(url=node_url)
        async with session.post(url, json=mail.dict()) as response:
            if response.status != 200:
                return False

            return True

    except aiohttp.client_exceptions.ClientConnectorError:
        ...
    except Exception as e:
        print(e)
        print(type(e))

    return False


async def send_mail_to_receivers(receivers, mail):
    async with aiohttp.ClientSession() as session:
        for node_url in receivers:
            await send_mail_to_receiver(session, node_url, mail)
