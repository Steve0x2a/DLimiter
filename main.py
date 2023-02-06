from quart import Quart
from routes import bp_player
from conf import Config
import logging

app = Quart(__name__)
cfg = Config()
app.logger.setLevel(logging.INFO)
app.register_blueprint(bp_player)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8088,
    )
