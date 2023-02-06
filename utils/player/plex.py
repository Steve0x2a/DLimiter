import json
from const import *
import requests
from utils.player.event import Event
from client.player.plex import plex_client
from conf import Config
from log import logger


def parse_plex_webhooks(context: dict):
    try:
        data = context['payload']
        event = json.loads(str(data[0]))
        if event['event'] == "media.play":
            return Event(EVENT_START, event['Player']['publicAddress'], True, event['Player']['local'])
        if event['event'] == "media.stop":
            return Event(EVENT_STOP, event['Player']['publicAddress'], True, event['Player']['local'])
        return Event(EVENT_OTHER, event['Session']['RemoteEndPoint'], True, event['Player']['local'])
    except Exception as e:
        logger.error("解析Plex webhooks错误:{},context:{}".format(e, context))
        return Event()


def get_plex_playing_session_count():
    try:
        sessions = plex_client.sessions()
        count = 0
        for session in sessions:
            if not session.player.local:
                count += 1
                logger.info("监测到Plex外网用户{}({})正在播放".format(session.name, session.player.address))
        logger.info("当前Plex外网播放会话数:{}".format(count))
        return count
    except Exception as e:
        logger.error("解析emby session api错误:{}".format(e))
        return 0