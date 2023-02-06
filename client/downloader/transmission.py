import transmission_rpc


class Transmission(object):
    def __init__(self,
                 name="",
                 protocol='http',
                 host="127.0.0.1",
                 port=9091,
                 username=None,
                 password=None,
                 path='/transmission/rpc',
                 use_alt_speed_limits=False,
                 origin_speed_down=0,
                 origin_speed_up=0,
                 limit_speed_down=0,
                 limit_speed_up=0):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.path = path
        self.client = transmission_rpc.Client(host=host,
                                              port=port,
                                              username=username,
                                              password=password,
                                              protocol=protocol,
                                              path=path)
        self.use_alt_speed_limits = use_alt_speed_limits
        self.origin_speed_down = origin_speed_down
        self.origin_speed_up = origin_speed_up
        self.limit_speed_down = limit_speed_down
        self.limit_speed_up = limit_speed_up
        self.name = name

    def get_session(self):
        return self.client.get_session()

    def set_speed_limit(self, speed_down: int, speed_up: int, alt_speed_time_enabled: bool = False):

        self.client.set_session(speed_limit_down=speed_down,
                                speed_limit_up=speed_up,
                                alt_speed_time_enabled=alt_speed_time_enabled,
                                speed_limit_down_enabled=True,
                                speed_limit_up_enabled=True)
