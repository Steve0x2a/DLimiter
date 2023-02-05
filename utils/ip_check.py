import IPy


def check_ip_if_internal(check_ip, ip_list):
    '''检查IP是否为公网IP&是否包含于排除的网段中'''
    # IPv6 情况比较复杂， 目前只判断是否为fe80 开头，如果不是则判断属于公网，后续考虑判断两个ipv6在不在同一个网段。
    if IPy.IP(check_ip).version() == 6 and not check_ip.startswith('fe80'):
        return False
    if IPy.IP(check_ip).iptype() == "PUBLIC":
        return False
    for ip in ip_list:
        if check_ip in IPy.IP(ip):
            return False
    return True