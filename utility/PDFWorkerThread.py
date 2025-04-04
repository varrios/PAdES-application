import logging
import os
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from constants import KEYS_DIR_PATH, LOGGER_GLOBAL_NAME
from utility.keygen import generate_RSA_keypair, encrypt_private_key
from utility.pdf_sign import decrypt_private_key, DecryptionError, sign_pdf_file

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief Worker thread for PDF signing
##
## This class handles PDF signing in a separate thread
## to keep the UI responsive during the signing process
class SignPDFWorkerThread(QThread):
    ## @brief Signal emitted when signing progress changes
    change_progress_signal = pyqtSignal(str)
    ## @brief Signal emitted when signing is complete
    task_finished_signal = pyqtSignal()

    ## @brief Initializes the worker thread
    ## @param pdf_filepath Path to the PDF file to sign
    ## @param pin User PIN for private key decryption
    ## @param private_key_filepath Path to the encrypted private key file
    def __init__(self, pdf_filepath, pin, private_key_filepath):
        super().__init__()
        self.pdf_filepath = pdf_filepath
        self.pin = pin
        self.private_key_filepath = private_key_filepath

    ## @brief Main execution method of the thread
    ##
    ## Decrypts the private key with the PIN and signs the PDF file
    def run(self):
        try:
            sleep(1)
            self.change_progress_signal.emit("Decrypting private key with provided PIN...")
            decrypted_private_key = decrypt_private_key(private_key_filepath=self.private_key_filepath, pin=self.pin)
            sleep(0.5)
            sign_pdf_file(decrypted_private_key=decrypted_private_key, pdf_filepath=self.pdf_filepath)
            sleep(0.5)


        except DecryptionError:
            self.change_progress_signal.emit("PDF signing failed. ❌ Given PIN does not match private key generated.")
            sleep(3)
            self.task_finished_signal.emit()
        except Exception as e:
            self.change_progress_signal.emit("PDF signing failed. ❌ Please try again. \n Error: " + str(e))
            sleep(3)
            self.task_finished_signal.emit()
        else:
            self.change_progress_signal.emit("PDF signature added successfully. ✅ ")
            sleep(3)
            self.task_finished_signal.emit()
