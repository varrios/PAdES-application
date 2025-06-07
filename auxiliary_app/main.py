## @file main.py
## @brief Main entry point for the PAdES application (auxiliary)
##
## This file initializes the logger and launches the PyQt GUI application.

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication

from gui.AuxiliaryApp import AuxiliaryApp
from logger.logger import initialize_logger

logger = initialize_logger()

## @brief Main function to start the auxiliary application
## @return None
def main() -> None:
    logger.info('Auxiliary application started')

    app = QApplication(sys.argv)
    main_window = AuxiliaryApp()
    app.exec()

    logger.info('Auxiliary application exited')


if __name__ == '__main__':
    main()