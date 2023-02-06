import rtoml
from pathlib import Path
from easydict import EasyDict as edict
from threading import Lock
from log import logger
import os
from client.downloader.qbittorrent import QBittorrent
from client.downloader.transmission import Transmission

config = None
# 线程锁
lock = Lock()


def singleconfig(cls):
    def _singleconfig(*args, **kwargs):
        global config
        if not config:
            with lock:
                config = cls(*args, **kwargs)
        return config

    return _singleconfig


@singleconfig
class Config(object):
    def __init__(self):
        self.path = os.environ.get('DLIMITER_CONFIG') or "./conf/config.toml"
        self.cfg = self.parse_conf()
        self.parse_downloaders()
        self.limit_client = {
            "emby": False,
            "jellyfin": False,
        }

    def parse_conf(self):
        if os.path.exists(self.path):
            cfg = edict(rtoml.load(Path(self.path)))
        else:
            raise ValueError("CONFIG FILE NOT FOUND")
            os._exit(1)
        logger.info("配置文件加载成功")
        return cfg

    def parse_downloaders(self):
        downloaders = []
        for dl_name in self.cfg.downloader:
            cfg = self.cfg.downloader[dl_name]
            dl_type = cfg["type"]
            if dl_type == "transmission":
                downloader = Transmission(name=dl_name,
                                          protocol=cfg["protocol"],
                                          host=cfg["host"],
                                          port=cfg["port"],
                                          username=cfg["username"],
                                          password=cfg["password"],
                                          path=cfg["rpc_path"],
                                          use_alt_speed_limits=cfg["use_alt_speed_limits"],
                                          origin_speed_down=cfg["origin_speed_down"],
                                          origin_speed_up=cfg["origin_speed_up"],
                                          limit_speed_down=cfg["limit_speed_down"],
                                          limit_speed_up=cfg["limit_speed_up"])
                downloaders.append(downloader)
            elif dl_type == "qbittorrent":
                downloader = QBittorrent(name=dl_name,
                                         host=cfg["host"],
                                         port=cfg["port"],
                                         username=cfg["username"],
                                         password=cfg["password"],
                                         use_alt_speed_limits=cfg["use_alt_speed_limits"],
                                         origin_speed_down=cfg["origin_speed_down"],
                                         origin_speed_up=cfg["origin_speed_up"],
                                         limit_speed_down=cfg["limit_speed_down"],
                                         limit_speed_up=cfg["limit_speed_up"])
                downloaders.append(downloader)
        self.downloaders = downloaders
        logger.info("共加载了 %d 个下载器" % len(downloaders))