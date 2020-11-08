import os
import json
import sys
from loguru import logger

from scrapper.scrapper import Scrapper

LOCAL_ENV = "env_local.json"


def init_local_env(path: str):
    if os.path.exists(path):
        with open(path) as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                os.environ[key] = value


def init_logger():
    if 'logger_log_to' in os.environ:
        logger.remove()

        if 'console' in os.environ['logger_log_to']:
            logger.add(sys.stdout,
                       colorize=bool(os.environ['logger_console_colorized']),
                       format=os.environ['logger_console_format'],
                       level=os.environ['logger_console_level'])

        if 'file' in os.environ['logger_log_to']:
            logger.add(
                os.environ["logger_file_name"],
                rotation=os.environ["logger_file_rotation"])

        if 'file_json' in os.environ['logger_log_to']:
            logger.add(
                os.environ["logger_file_json_name"],
                rotation=os.environ["logger_file_json_rotation"],
                serialize=True)


def main():
    scrapper = Scrapper()

    while True:
        try:
            scrapper.start()
        except Exception as exc:
            logger.exception(exc)


if __name__ == "__main__":
    init_local_env(LOCAL_ENV)
    init_logger()
    main()
