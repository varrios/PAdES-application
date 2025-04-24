## @file main.py
## @brief Main entry point for the PAdES application
##
## This file initializes the logger and launches the PyQt GUI application.

import sys

from PyQt6.QtWidgets import QApplication

from gui.AuxiliaryApp import AuxiliaryApp
from gui.SignatureApp import SignatureApp
from logger.logger import initialize_logger

logger = initialize_logger()

## @brief Main function to start the application
## @return None
def main() -> None:
    logger.info('Auxiliary application started')

    app = QApplication(sys.argv)
    main_window = AuxiliaryApp()
    app.exec()


    logger.info('Auxiliary application exited')


if __name__ == '__main__':
    main()