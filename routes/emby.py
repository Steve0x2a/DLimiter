from quart import Blueprint
from quart import request
from utils.limiter import emby_apply_limit
from quart import current_app as app
from conf import Config

bp_emby = Blueprint("emby", __name__, url_prefix="/emby")


@bp_emby.route("/", methods=['POST', 'GET'], strict_slashes=False)
async def emby():
    data = await request.form
    try:
        if Config().cfg.emby.enable:
            emby_apply_limit(data.to_dict(flat=False))
    except NameError as e:
        app.logger.error("Emby 解析出错， error: {}".format(e))
    return "emby"
