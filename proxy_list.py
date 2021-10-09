proxys_list = []
socks_list = []


def add_to_proxy_list(some_proxy, time):
    proxys_list.insert(0, [some_proxy, time])


def get_proxy_q():
    return len(proxys_list)


def get_proxy():
    list_with_proxies = []
    for proxy_index in range(0, 5):
        list_with_proxies.append([proxys_list[proxy_index][0], proxys_list[proxy_index][1]])
    for proxy_index in range(0, 5):
        del proxys_list[0]
    return list_with_proxies


def add_to_socks_list(some_proxy, time):
    socks_list.insert(0, [some_proxy, time])


def get_socks_q():
    return len(socks_list)


def get_socks():
    list_with_socks = []
    for socks_index in range(0, 5):
        list_with_socks.append([socks_list[socks_index][0], socks_list[socks_index][1]])
    for socks_index in range(0, 5):
        del socks_list[0]
    return list_with_socks
