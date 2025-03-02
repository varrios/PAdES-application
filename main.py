import sys

from PyQt6.QtWidgets import QApplication

from gui.SignatureApp import SignatureApp
from logger.logger import initialize_logger

logger = initialize_logger()

def main() -> None:
    logger.info('Main application started')

    app = QApplication(sys.argv)
    main_window = SignatureApp()
    app.exec()


    logger.info('Main application exited')


if __name__ == '__main__':
    main()