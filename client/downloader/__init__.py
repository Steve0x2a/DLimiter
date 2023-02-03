from conf import config
from client.downloader.qbittorrent import QBittorrent
from client.downloader.transmission import Transmission
from urllib.parse import urlparse
from log import logger

downloaders = []
for dl_name in config.downloader:
    cfg = config.downloader[dl_name]
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

logger.info("共加载了 %d 个下载器" % len(downloaders))