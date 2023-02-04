from quart import Quart
from routes import bp_player
import logging

app = Quart(__name__)

app.register_blueprint(bp_player)
app.logger.setLevel(logging.INFO)
# app.run(host="0.0.0.0", port=8088)
