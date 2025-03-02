import os

RSA_KEY_LENGTH = 4096

LOGS_DIRNAME = 'logs'
LOGS_FILENAME = 'app_logs.log'
LOGGER_GLOBAL_NAME = 'global_logger'

KEYS_DIRNAME = 'keys'

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

BASE_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
STYLES_DIR_PATH = os.path.join(BASE_PROJECT_PATH, 'gui', 'styles')
