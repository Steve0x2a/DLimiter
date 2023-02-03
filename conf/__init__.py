import rtoml
from pathlib import Path
from easydict import EasyDict as edict
import os


class Config(object):
    def __init__(self, path):
        self.path = path
        self.cfg = None

    def parse_conf(self):
        if os.path.exists(self.path):
            cfg = edict(rtoml.load(Path(self.path)))
        else:
            raise ValueError("CONFIG FILE NOT FOUND")
            os._exit(1)
        return cfg


config = Config(path="./conf/config.toml").parse_conf()