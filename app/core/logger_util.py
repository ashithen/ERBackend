import logging

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Pass Uvicorn logs to Loguru
        logger.opt(depth=6).log(record.levelname.lower(), record.getMessage())
