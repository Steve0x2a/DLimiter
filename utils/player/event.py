class Event(object):
    def __init__(self, event=None, endpoint=None, success: bool = False):
        self.event = event
        self.endpoint = endpoint
        self.success = success