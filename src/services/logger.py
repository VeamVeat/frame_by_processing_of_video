import logging
import os

from dotenv import load_dotenv

load_dotenv('.env')


def setup_logger():
    logging.basicConfig(
        filename=os.getenv('LOGGING_FILE_NAME'),
        level=logging.INFO,
        format=os.getenv('LOGGING_FORMAT'),
        datefmt=os.getenv('LOGGING_DATE_FMT')
    )

    return logging.getLogger(__name__)
