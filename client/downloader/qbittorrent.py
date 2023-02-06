import qbittorrentapi


class QBittorrent(object):
    def __init__(self,
                 name="",
                 host="127.0.0.1",
                 port=8080,
                 username=None,
                 password=None,
                 use_alt_speed_limits=False,
                 origin_speed_down=0,
                 origin_speed_up=0,
                 limit_speed_down=0,
                 limit_speed_up=0):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = qbittorrentapi.Client(host=self.host,
                                            port=self.port,
                                            username=self.username,
                                            password=self.password)
        self.client.auth_log_in()
        self.use_alt_speed_limits = use_alt_speed_limits
        self.origin_speed_down = origin_speed_down
        self.origin_speed_up = origin_speed_up
        self.limit_speed_down = limit_speed_down
        self.limit_speed_up = limit_speed_up
        self.name = name

    def set_speed_limit(self, speed_down: int, speed_up: int, alt_speed_time_enabled: bool = False):
        self.client.application.preferences = {
            "scheduler_enabled": alt_speed_time_enabled,
            "up_limit": speed_up * 1024,
            "dl_limit": speed_down * 1024
        }
