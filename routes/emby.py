from quart import Blueprint
from quart import request
from utils.limiter import player_apply_limit
from quart import current_app as app
from conf import config

bp_emby = Blueprint("emby", __name__, url_prefix="/emby")


@bp_emby.route("/", methods=['POST', 'GET'], strict_slashes=False)
async def emby():
    data = await request.form
    if config.emby.enable:
        player_apply_limit("emby", data.to_dict(flat=False))
    return "emby"


