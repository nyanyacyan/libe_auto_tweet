import logging

class ColorFormatter(logging.Formatter):

    COLORS = {
        logging.DEBUG: "\033[92m",     # 緑
        logging.INFO: "\033[94m",      # 青
        logging.WARNING: "\033[93m",   # 黄
        logging.ERROR: "\033[91m",     # 赤
        logging.CRITICAL: "\033[95m",  # マゼンタ
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"

class SimpleLogger:
    def __init__(self, name=__name__):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = ColorFormatter("[%(levelname)s] %(message)s")
        ch.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger



if __name__ == "__main__":
    # ロガーを取得
    logger = SimpleLogger(__name__).get_logger()

    # 各レベルのログを出力してみる
    logger.debug("これはデバッグログです")
    logger.info("これは情報ログです")
    logger.warning("これは警告ログです")
    logger.error("これはエラーログです")
    logger.critical("これは重大ログです")