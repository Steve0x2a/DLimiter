import json
from const import *
from quart import current_app as app
import requests
from utils.player.event import Event
from utils.ip_check import check_ip_if_internal
from conf import config
from log import logger


def parse_emby_webhooks(context: dict):
    try:
        data = context['data']
        for item in data:
            event = json.loads(str(item))
            if event['Event'] == "playback.start":
                return Event(EVENT_START, event['Session']['RemoteEndPoint'], True)
            if event['Event'] == "playback.stop":
                return Event(EVENT_STOP, event['Session']['RemoteEndPoint'], True)
            return Event(EVENT_OTHER, event['Session']['RemoteEndPoint'], True)
    except Exception as e:
        logger.error("解析webhooks错误:{},context:{}".format(e, context))
        return Event()


def get_emby_playing_session_count(url, api_key):
    try:
        r = requests.get(url + "/emby/Sessions?api_key=" + api_key)
        data = r.json()
        count = 0
        for item in data:
            if "NowPlayingItem" in item and not check_ip_if_internal(item['RemoteEndPoint'], config.limiter.exclude_ip
                                                                     or []):
                count += 1
                logger.info("监测到Emby外网用户{}({})正在播放".format(item['UserName'], item['RemoteEndPoint']))
        logger.info("当前Emby外网播放会话数:{}".format(count))
        return count
    except Exception as e:
        logger.error("解析emby session api错误:{}, 返回值:{}".format(e, r.text))
        return 0