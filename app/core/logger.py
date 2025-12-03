import logging
import sys

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('nysa_system')
        self.initialized = False

    def setup(self, app):
        if self.initialized: return
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        self.logger.addHandler(handler)
        self.initialized = True
        self.info("Logger System Started")

    def _format_msg(self, msg, key=None, data=None):
        log_text = f"{msg}"
        if key:
            log_text += f" | Key: [{key}]"

        if data:
            log_text += f" | Data: {str(data)}"

        return log_text

    def info(self, msg, key=None, data=None):
        self.logger.info(self._format_msg(msg, key, data))

    def warn(self, msg, key=None, data=None):
        self.logger.warning(self._format_msg(msg, key, data))

    def error(self, msg, key=None, data=None):
        self.logger.error(self._format_msg(msg, key, data))

logger = Logger()