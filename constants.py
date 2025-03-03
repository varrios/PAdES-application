import os

#### MISC ####

RSA_KEY_LENGTH = 4096
MAX_PIN_LENGTH = 6

#### LOGGER ####

LOGS_DIRNAME = 'logs'
LOGS_FILENAME = 'app_logs.log'
LOGGER_GLOBAL_NAME = 'global_logger'

#### OTHER PATHS ####

BASE_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
KEYS_DIRNAME = 'keys'

STYLES_DIR_PATH = os.path.join(BASE_PROJECT_PATH, 'gui', 'styles')
ASSETS_DIR_PATH = os.path.join(BASE_PROJECT_PATH, 'gui', 'assets')

STYLESHEET_FILE_PATH = os.path.join(STYLES_DIR_PATH, 'signature_app.css')
ICON_FILE_PATH = os.path.join(ASSETS_DIR_PATH, 'icon.png')
KEYS_DIR_PATH= os.path.join(BASE_PROJECT_PATH, KEYS_DIRNAME)

#### GUI CONSTANTS ####

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

KEYGEN_PAGE_NAME = "keygen_page"
SIGN_PAGE_NAME = "sign_page"
VERIFY_PAGE_NAME = "verify_page"

MAIN_WINDOW_TITLE = "PAdES Signature App"
