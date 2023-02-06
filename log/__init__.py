import logging
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self):
        # 设置全局logger等级
        root_logger = logging.getLogger()
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(lineno)s %(message)s",
                                      datefmt="%Y-%m-%d %H:%M:%S")

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)

        self.logger = logging.getLogger("DLimiter")
        self.logger.setLevel(logging.INFO)

        self.logger.info("日志初始化完成")

    def get_logger(self):
        return self.logger


logger = Logger().get_logger()