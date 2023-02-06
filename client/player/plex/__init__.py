from plexapi.server import PlexServer
from conf import Config

plex_client = None
config = Config()
if "plex" in config.cfg and config.cfg.plex.enable:
    plex_client = PlexServer(config.cfg.plex.url, config.cfg.plex.token)