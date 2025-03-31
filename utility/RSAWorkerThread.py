import os
from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from constants import KEYS_DIR_PATH
from utility.keygen import generate_RSA_keypair, encrypt_private_key


class RSAWorkerThread(QThread):
    change_progress_signal = pyqtSignal(str)
    task_finished_signal = pyqtSignal()
    def __init__(self, filename, pin, usb_path):
        super().__init__()
        self.filename = filename
        self.pin = pin
        self.usb_path = usb_path

    def run(self):
        try:
            sleep(1)
            self.change_progress_signal.emit("Generating RSA keypair...")
            private_key, public_key = generate_RSA_keypair()
            sleep(0.5)

            self.change_progress_signal.emit("Encrypting private key...")
            encrypted_private_key = encrypt_private_key(private_key=private_key, pin=self.pin)
            sleep(0.5)

            self.change_progress_signal.emit("Saving private key to USB storage drive...")
            with open(os.path.join(self.usb_path, f"{self.filename}_private.key"), "wb") as f:
                f.write(encrypted_private_key)
            sleep(0.5)

            self.change_progress_signal.emit("Checking if local keys directory exists...")
            sleep(0.5)
            if not os.path.exists(KEYS_DIR_PATH):
                self.change_progress_signal.emit("Creating local keys directory...")
                os.makedirs(KEYS_DIR_PATH)
                sleep(0.5)


            self.change_progress_signal.emit("Saving public key to local keys directory...")
            with open(os.path.join(KEYS_DIR_PATH, f"{self.filename}_public.pem"), "wb") as f:
                f.write(public_key)
            sleep(0.5)
        except Exception as e:
            self.change_progress_signal.emit("Generation and encryption failed. ❌ Please try again. \n Error: " + str(e))
            sleep(3)
            self.task_finished_signal.emit()
        else:
            self.change_progress_signal.emit("Generation and encryption finished successfully. ✅ ")
            sleep(3)
            self.task_finished_signal.emit()
