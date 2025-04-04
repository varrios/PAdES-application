import logging
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from constants import LOGGER_GLOBAL_NAME
from utility.pdf_sign import verify_pdf_signature

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

class VerifyPDFWorkerThread(QThread):
    change_progress_signal = pyqtSignal(str)
    task_finished_signal = pyqtSignal(bool, str)

    def __init__(self, pdf_filepath, public_key_filepath):
        super().__init__()
        self.pdf_filepath = pdf_filepath
        self.public_key_filepath = public_key_filepath

    def run(self):
        try:
            sleep(1)
            self.change_progress_signal.emit("Loading public key...")
            sleep(0.5)

            self.change_progress_signal.emit("Verifying PDF signature...")
            is_valid, message = verify_pdf_signature(
                pdf_filepath=self.pdf_filepath,
                public_key_filepath=self.public_key_filepath
            )
            sleep(0.5)

            self.task_finished_signal.emit(is_valid, message)
        except Exception as e:
            self.change_progress_signal.emit(f"Verification failed. ❌ Error: {str(e)}")
            sleep(1)
            self.task_finished_signal.emit(False, str(e))
