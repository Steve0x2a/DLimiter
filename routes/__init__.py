from quart import Blueprint
from routes.emby import bp_emby
from routes.jellyfin import bp_jellyfin
from routes.plex import bp_plex

bp_player = Blueprint('player', __name__, url_prefix="/player")
bp_player.register_blueprint(bp_emby)
bp_player.register_blueprint(bp_jellyfin)
bp_player.register_blueprint(bp_plex)
