import logging
import os
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from constants import KEYS_DIR_PATH, LOGGER_GLOBAL_NAME
from utility.keygen import generate_RSA_keypair, encrypt_private_key
from utility.pdf_sign import decrypt_private_key

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

class SignPDFWorkerThread(QThread):
    change_progress_signal = pyqtSignal(str)
    task_finished_signal = pyqtSignal()
    def __init__(self, pdf_filepath, pin, private_key_filepath):
        super().__init__()
        self.pdf_filepath = pdf_filepath
        self.pin = pin
        self.private_key_filepath = private_key_filepath

    def run(self):
        try:
            self.change_progress_signal.emit("Decrypting private key with provided PIN...")
            decrypted_private_key = decrypt_private_key(private_key_filepath=self.private_key_filepath, pin=self.pin)
            sleep(0.5)



        except Exception as e:
            self.change_progress_signal.emit("PDF signing failed. ❌ Please try again. \n Error: " + str(e))
            sleep(2)
            self.task_finished_signal.emit()
        else:
            self.change_progress_signal.emit("PDF signature added successfully. ✅ ")
            sleep(2)
            self.task_finished_signal.emit()
