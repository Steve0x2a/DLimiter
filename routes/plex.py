from quart import Blueprint
from quart import request
from utils.limiter import plex_apply_limit
from quart import current_app as app
from conf import Config

bp_plex = Blueprint("plex", __name__, url_prefix="/plex")


@bp_plex.route("/", methods=['POST', 'GET'], strict_slashes=False)
async def plex():
    data = await request.form
    try:
        if Config().cfg.plex.enable:
            plex_apply_limit(data.to_dict(flat=False))
    except NameError as e:
        app.logger.error("Plex 解析出错， error: {}".format(e))
    return "plex"
