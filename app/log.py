import logging
import os
from pathlib import Path
import coloredlogs

LOGS_DIR = f"{os.getcwd()}/logs"

logger = logging.getLogger("main")
logger_stream_handler = logging.StreamHandler()

main_logs_directory = Path(LOGS_DIR)
main_logs_directory.mkdir(exist_ok=True)

logger_file_handler = logging.FileHandler(main_logs_directory / "main.log", encoding="utf-8")

LOGGING_FORMAT = "%(asctime)s - %(levelname)s: %(message)s [%(filename)s:%(lineno)d]"
logger_file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

logger.addHandler(logger_file_handler)
logger.addHandler(logger_stream_handler)

logger.setLevel(logging.DEBUG)

coloredlogs.install(level="DEBUG", logger=logger, fmt=LOGGING_FORMAT, milliseconds=True)
