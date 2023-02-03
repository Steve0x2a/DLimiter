import IPy


def check_ip_if_internal(check_ip, ip_list):
    '''检查IP是否为公网IP&是否包含于排除的网段中'''
    if IPy.IP(check_ip).iptype() == "PUBLIC":
        return False
    for ip in ip_list:
        if check_ip in IPy.IP(ip):
            return False
    return True