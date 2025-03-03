import logging
import os
import sys
from datetime import datetime
from constants import LOGGER_GLOBAL_NAME, LOGS_DIRNAME, LOGS_FILENAME, BASE_PROJECT_PATH

def ensure_logs_dir():
    try:
        os.makedirs(f'{BASE_PROJECT_PATH}/{LOGS_DIRNAME}')
    except FileExistsError:
        pass

def initialize_logger():
    ensure_logs_dir()
    CURRENT_TIME = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            #logging.FileHandler(f'{BASE_PROJECT_PATH}/{LOGS_DIRNAME}/{CURRENT_TIME}_{LOGS_FILENAME}', encoding='utf-8'),
            logging.FileHandler(f'{BASE_PROJECT_PATH}/{LOGS_DIRNAME}/{LOGS_FILENAME}', encoding='utf-8', mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger(LOGGER_GLOBAL_NAME)
