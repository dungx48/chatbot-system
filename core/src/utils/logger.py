import logging
import json
import sys

class JsonLogger:
    def __init__(self):
        self.logger = logging.getLogger("JsonLogger")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                "level": record.levelname,
                "message": record.getMessage(),
                "timestamp": self.formatTime(record),
                "filename": record.filename,
                "lineno": record.lineno,
            }
            return json.dumps(log_record)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)

# Create a logger instance
logger = JsonLogger()