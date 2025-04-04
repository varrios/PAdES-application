import logging
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from constants import LOGGER_GLOBAL_NAME
from utility.pdf_sign import verify_pdf_signature

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief Worker thread for PDF signature verification
##
## This class handles PDF signature verification in a separate thread
## to keep the UI responsive during the verification process
class VerifyPDFWorkerThread(QThread):
    ## @brief Signal emitted when verification progress changes
    change_progress_signal = pyqtSignal(str)
    ## @brief Signal emitted when verification is complete
    ## @param bool Result of verification (True for valid, False for invalid)
    ## @param str Message describing the verification result
    task_finished_signal = pyqtSignal(bool, str)

    ## @brief Initializes the worker thread
    ## @param pdf_filepath Path to the signed PDF file to verify
    ## @param public_key_filepath Path to the public key file
    def __init__(self, pdf_filepath, public_key_filepath):
        super().__init__()
        self.pdf_filepath = pdf_filepath
        self.public_key_filepath = public_key_filepath

    ## @brief Main execution method of the thread
    ##
    ## Verifies the PDF signature and emits signals for progress updates and completion
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
