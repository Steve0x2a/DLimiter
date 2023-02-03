from conf import config
from utils.player.event import Event
from utils.player.emby import parse_emby_webhooks, get_emby_playing_session_count
from utils.ip_check import check_ip_if_internal
from client.downloader import downloaders
from quart import current_app as app
from const import *
from log import logger
import IPy


def player_apply_limit(player_type: str, context: dict):
    global IS_LIMITED
    if player_type == PLAYER_EMBY:
        event = parse_emby_webhooks(context)
    else:
        event = Event()
    if not event.success:
        logger.error("Event not successful")
        return
    if event.event not in EVENT_TRIGGER:
        logger.debug("事件类型不属于触发类型，跳过")
        return
    if check_ip_if_internal(event.endpoint, config.limiter.exclude_ip or []):
        logger.info("事件触发，IP地址{}不属于公网地址，跳过".format(event.endpoint))
        return

    if event.event == EVENT_START:
        # 遍历所有下载器
        for downloader in downloaders:
            downloader.set_speed_limit(downloader.limit_speed_down, downloader.limit_speed_up, False)
            logger.info("监测到{}外网({})播放，触发限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(player_type, event.endpoint,
                                                                                 downloader.name,
                                                                                 downloader.limit_speed_down,
                                                                                 downloader.limit_speed_up))
        IS_LIMITED = True

    if event.event == EVENT_STOP:
        # 遍历所有下载器
        if get_emby_playing_session_count(config.emby.url, config.emby.api_key) == 0:
            for downloader in downloaders:
                downloader.set_speed_limit(downloader.origin_speed_down, downloader.origin_speed_up,
                                           downloader.use_alt_speed_limits)
                logger.info("监测到{}外网({})播放停止，触发取消限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(
                    player_type, event.endpoint, downloader.name, downloader.origin_speed_down,
                    downloader.origin_speed_up))
        else:
            logger.info("监测到{}外网({})播放停止，触发取消限速，但是Emby还有其他外网用户在播放，跳过".format(player_type, event.endpoint))
        IS_LIMITED = False
