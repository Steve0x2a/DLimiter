class Event(object):
    def __init__(self, event=None, endpoint=None, success: bool = False, is_local: bool = False):
        self.event = event
        self.endpoint = endpoint
        self.success = success
        self.is_local = is_local  # 只有plex需要判断
