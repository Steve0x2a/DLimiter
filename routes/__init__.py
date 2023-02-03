from quart import Blueprint
from routes.emby import bp_emby
from conf import config

bp_player = Blueprint('player', __name__, url_prefix="/player")
bp_player.register_blueprint(bp_emby)
