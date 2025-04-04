## @file constants.py
## @brief Application-wide constants and configuration values
##
## This file contains all the constant values used throughout the application,
## including paths, configuration settings, and GUI constants.

import os

#### MISC ####

## @brief Length of RSA key in bits (as per requirements: 4096)
RSA_KEY_LENGTH = 4096
## @brief Maximum PIN length for key encryption/decryption
MAX_PIN_LENGTH = 6

#### LOGGER ####

## @brief Directory name for storing log files
LOGS_DIRNAME = 'logs'
## @brief Log filename
LOGS_FILENAME = 'app_logs.log'
## @brief Global logger name used throughout the application
LOGGER_GLOBAL_NAME = 'global_logger'

#### OTHER PATHS ####

## @brief Base path of the project directory
BASE_PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
## @brief Directory name for storing public keys
KEYS_DIRNAME = 'keys'

## @brief Path to the styles directory
STYLES_DIR_PATH = os.path.join(BASE_PROJECT_PATH, 'gui', 'styles')
## @brief Path to the assets directory
ASSETS_DIR_PATH = os.path.join(BASE_PROJECT_PATH, 'gui', 'assets')

## @brief Path to the CSS stylesheet file
STYLESHEET_FILE_PATH = os.path.join(STYLES_DIR_PATH, 'signature_app.css')
## @brief Path to the application icon file
ICON_FILE_PATH = os.path.join(ASSETS_DIR_PATH, 'icon.png')
## @brief Path to the directory where public keys are stored
KEYS_DIR_PATH= os.path.join(BASE_PROJECT_PATH, KEYS_DIRNAME)

#### GUI CONSTANTS ####

## @brief Width of the main application window
WINDOW_WIDTH = 800
## @brief Height of the main application window
WINDOW_HEIGHT = 600

## @brief Object name for the key generation page
KEYGEN_PAGE_NAME = "keygen_page"
## @brief Object name for the signing page
SIGN_PAGE_NAME = "sign_page"
## @brief Object name for the verification page
VERIFY_PAGE_NAME = "verify_page"

## @brief Title of the main application window
MAIN_WINDOW_TITLE = "PAdES Signature App"
