from quart import Blueprint
from quart import request
from utils.limiter import jellyfin_apply_limit
from quart import current_app as app
from conf import Config

bp_jellyfin = Blueprint("jellyfin", __name__, url_prefix="/jellyfin")


@bp_jellyfin.route("/", methods=['POST', 'GET'], strict_slashes=False)
async def jellyfin():
    data = await request.get_data()
    try:
        if Config().cfg.jellyfin.enable:
            jellyfin_apply_limit(data)
    except NameError as e:
        app.logger.error("Jellyfin 配置缺失， error: {}".format(e))
    return "jellyfin"
