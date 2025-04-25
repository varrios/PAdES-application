## @file main.py
## @brief Main entry point for the PAdES application (signature)
##
## This file initializes the logger and launches the PyQt GUI application.

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication

from gui.SignatureApp import SignatureApp
from logger.logger import initialize_logger

logger = initialize_logger()

## @brief Main function to start the signature application
## @return None
def main() -> None:
    logger.info('Signature application started')

    app = QApplication(sys.argv)
    main_window = SignatureApp()
    app.exec()


    logger.info('Signature application exited')


if __name__ == '__main__':
    main()