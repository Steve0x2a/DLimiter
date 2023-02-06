from conf import Config
from utils.player.event import Event
from utils.player.emby import parse_emby_webhooks, get_emby_playing_session_count
from utils.player.jellyfin import parse_jellyfin_webhooks, get_jellyfin_playing_session_count
from utils.player.plex import parse_plex_webhooks, get_plex_playing_session_count
from utils.ip_check import check_ip_if_internal
from quart import current_app as app
from const import *
from log import logger
import IPy
import time


def emby_apply_limit(context: dict):
    player_type = "emby"
    event = parse_emby_webhooks(context)
    if not event.success:
        logger.error("Event not successful")
        return
    if event.event not in EVENT_TRIGGER:
        logger.debug("事件类型不属于触发类型，跳过")
        return
    if check_ip_if_internal(event.endpoint, Config().cfg.limiter.exclude_ip or []):
        logger.info("事件触发，IP地址{}不属于公网地址，跳过".format(event.endpoint))
        return

    if event.event == EVENT_START:
        # 遍历所有下载器
        for downloader in Config().downloaders:
            downloader.set_speed_limit(downloader.limit_speed_down, downloader.limit_speed_up, False)
            logger.info("监测到{}外网({})播放，触发限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(player_type, event.endpoint,
                                                                                 downloader.name,
                                                                                 downloader.limit_speed_down,
                                                                                 downloader.limit_speed_up))
        Config().limit_client[player_type] = True

    if event.event == EVENT_STOP:

        if get_emby_playing_session_count(Config().cfg.emby.url, Config().cfg.emby.api_key) == 0:
            Config().limit_client[player_type] = False
            if any(Config().limit_client.values()):
                logger.info("监测到{}外网({})停止播放，但是其他客户端:{}正在播放，跳过".format(
                    player_type, event.endpoint, {k
                                                  for k, v in Config().limit_client.items() if v}))
                return
            # 遍历所有下载器
            for downloader in Config().downloaders:
                downloader.set_speed_limit(downloader.origin_speed_down, downloader.origin_speed_up,
                                           downloader.use_alt_speed_limits)
                logger.info("监测到{}外网({})播放停止，触发取消限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(
                    player_type, event.endpoint, downloader.name, downloader.origin_speed_down,
                    downloader.origin_speed_up))
        else:
            logger.info("监测到{}外网({})播放停止，触发取消限速，但是Emby还有其他外网用户在播放，跳过".format(player_type, event.endpoint))


def jellyfin_apply_limit(context: bytes):
    player_type = "jellyfin"
    event = parse_jellyfin_webhooks(context)
    if not event.success:
        logger.error("Event not successful")
        return
    if event.event not in EVENT_TRIGGER:
        logger.debug("事件类型不属于触发类型，跳过")
        return
    # Jellyfin的Webhook不会返回IP地址，只能通过API获取

    if event.event == EVENT_START:
        if get_jellyfin_playing_session_count(Config().cfg.jellyfin.url, Config().cfg.jellyfin.api_key) >= 0:
            # 遍历所有下载器
            for downloader in Config().downloaders:
                downloader.set_speed_limit(downloader.limit_speed_down, downloader.limit_speed_up, False)
                logger.info("监测到{}外网({})播放，触发限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(
                    player_type, event.endpoint, downloader.name, downloader.limit_speed_down,
                    downloader.limit_speed_up))
        else:
            logger.info("监测到{}播放事件，但是Jellyfin没有外网用户在播放，跳过".format(player_type))
        Config().limit_client[player_type] = True

    if event.event == EVENT_STOP:

        if get_jellyfin_playing_session_count(Config().cfg.jellyfin.url, Config().cfg.jellyfin.api_key) == 0:
            Config().limit_client[player_type] = False
            if any(Config().limit_client.values()):
                logger.info("监测到{}外网({})停止播放，但是其他客户端:{}正在播放，跳过".format(
                    player_type, event.endpoint, {k
                                                  for k, v in Config().limit_client.items() if v}))
                return
            # 遍历所有下载器
            for downloader in Config().downloaders:
                downloader.set_speed_limit(downloader.origin_speed_down, downloader.origin_speed_up,
                                           downloader.use_alt_speed_limits)
                logger.info("监测到{}外网({})播放停止，触发取消限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(
                    player_type, event.endpoint, downloader.name, downloader.origin_speed_down,
                    downloader.origin_speed_up))
        else:
            logger.info("监测到{}外网播放停止，触发取消限速，但是Jellyfin还有其他外网用户在播放，跳过".format(player_type))


def plex_apply_limit(context: dict):
    player_type = "plex"
    event = parse_plex_webhooks(context)
    if not event.success:
        logger.error("Event not successful")
        return
    if event.event not in EVENT_TRIGGER:
        logger.debug("事件类型不属于触发类型，跳过")
        return
    # Plex 没提供地址，但是提供了local字段，因此暂时用这个判断是否为外网
    if event.is_local:
        logger.info("本地播放事件，跳过")
        return

    if event.event == EVENT_START:
        # 遍历所有下载器
        for downloader in Config().downloaders:
            downloader.set_speed_limit(downloader.limit_speed_down, downloader.limit_speed_up, False)
            logger.info("监测到{}外网({})播放，触发限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(player_type, event.endpoint,
                                                                                 downloader.name,
                                                                                 downloader.limit_speed_down,
                                                                                 downloader.limit_speed_up))
        Config().limit_client[player_type] = True

    if event.event == EVENT_STOP:

        if get_plex_playing_session_count() == 0:
            Config().limit_client[player_type] = False
            if any(Config().limit_client.values()):
                logger.info("监测到{}外网({})停止播放，但是其他客户端:{}正在播放，跳过".format(
                    player_type, event.endpoint, {k
                                                  for k, v in Config().limit_client.items() if v}))
                return
            # 遍历所有下载器
            for downloader in Config().downloaders:
                downloader.set_speed_limit(downloader.origin_speed_down, downloader.origin_speed_up,
                                           downloader.use_alt_speed_limits)
                logger.info("监测到{}外网({})播放停止，触发取消限速，下载器 {} 限速为 {}K/s 下载，{}K/s 上传".format(
                    player_type, event.endpoint, downloader.name, downloader.origin_speed_down,
                    downloader.origin_speed_up))
        else:
            logger.info("监测到{}外网({})播放停止，触发取消限速，但是Emby还有其他外网用户在播放，跳过".format(player_type, event.endpoint))