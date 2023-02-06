import requests
from conf import Config
import json
from log import logger
from utils.player.event import Event
from const import *
from utils.ip_check import check_ip_if_internal


def parse_jellyfin_webhooks(context: bytes):
    try:
        data = json.loads(context)
        # "NotificationType": "PlaybackStart",
        if data['NotificationType'] == "PlaybackStart":
            return Event(EVENT_START, "", True)
        if data['NotificationType'] == "PlaybackStop":
            return Event(EVENT_STOP, "", True)
        return Event(EVENT_OTHER, "", True)
    except Exception as e:
        logger.error("解析jellyfin webhooks错误:{},context:{}".format(e, context))
        return Event()
    return


def get_jellyfin_playing_session_count(url, api_key):
    try:
        r = requests.get(url + "/Sessions?api_key=" + api_key)
        data = r.json()
        count = 0
        for item in data:
            if "NowPlayingItem" in item and not check_ip_if_internal(item['RemoteEndPoint'],
                                                                     Config().cfg.limiter.exclude_ip or []):
                count += 1
                logger.info("监测到Jellinfin外网用户{}({})正在播放".format(item['UserName'], item['RemoteEndPoint']))
        logger.info("当前Jellyfin外网播放会话数:{}".format(count))
        return count
    except Exception as e:
        logger.error("解析Jellyfin session api错误:{}, 返回值:{}".format(e, r.text[:100]))
        return 0