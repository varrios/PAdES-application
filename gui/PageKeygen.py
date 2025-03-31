import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit, QHBoxLayout, \
    QLabel, QMessageBox, QProgressDialog

from constants import LOGGER_GLOBAL_NAME, KEYGEN_PAGE_NAME, MAX_PIN_LENGTH
from utility.RSAWorkerThread import RSAWorkerThread
from utility.misc import change_opacity

logger = logging.getLogger(LOGGER_GLOBAL_NAME)


class KeygenPage(QWidget):
    def __init__(self, parent):
        self._numpad_buttons = None
        self._layout = None
        self._group = None
        self._group_layout = None
        self._pin_layout = None
        self._numpad_layout = None

        self._btn_generate_keys = None
        self._input_pin = None
        self._btn_save_key = None

        logger.info("Initializing KeygenPage UI...")
        try:
            self.parent_app = parent
            super().__init__()
            self._init_ui()
            self.setObjectName(KEYGEN_PAGE_NAME)
        except Exception as e:
            logger.error(f"Error initializing KeygenPage: {e}")
        else:
            logger.info("KeygenPage initialized successfully")

    def _init_ui(self):
        self._layout = QVBoxLayout()

        self._group = QGroupBox("🔑 [Auxillary] Generate and encrypt RSA Key Pair")
        self._group_layout = QVBoxLayout()

        # ========== PINPAD INIT ==========
        self._pinpad_init()

        self._btn_save_key = QPushButton("🔐 Generate RSA Key Pair and Save Encrypted Private Key on USB drive")
        self._btn_save_key.clicked.connect(self._generate_and_encrypt_keypair)

        #keyname_input_label = QLabel("Enter key filename:")

        self._key_filename_input = QLineEdit()
        self._key_filename_input.setPlaceholderText("Key filename")
        self._key_filename_input.setMaxLength(50)
        #self._key_filename_input.setText("default_keyname")


        self._group_layout.addLayout(self._pin_layout)
        self._group_layout.addLayout(self._numpad_layout)
        #self._group_layout.addWidget(keyname_input_label)
        self._group_layout.addWidget(self._key_filename_input)
        self._group_layout.addWidget(self._btn_save_key)


        self._group.setLayout(self._group_layout)
        self._layout.addWidget(self._group)
        self.setLayout(self._layout)

    # ========== PINPAD HANDLING ==========

    def _pinpad_init(self):
        self._pin_layout = QHBoxLayout()
        self._input_pin = QLineEdit()
        self._input_pin.setPlaceholderText(f"Enter PIN (max {MAX_PIN_LENGTH} digits)")
        self._input_pin.setEchoMode(QLineEdit.EchoMode.Password)
        self._input_pin.setMaxLength(6)
        self._input_pin.setValidator(QIntValidator(0, 999999, self))

        self._btn_toggle_pin = QPushButton()
        self._btn_toggle_pin.setText("👁")
        self._btn_toggle_pin.setCheckable(True)
        self._btn_toggle_pin.clicked.connect(self._toggle_pin_visibility)

        self._pin_layout.addWidget(self._input_pin)
        self._pin_layout.addWidget(self._btn_toggle_pin)

        self._numpad_layout = QGridLayout()
        self._numpad_buttons = []
        for i in range(10):
            btn = QPushButton(str(i))
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda checked, digit=i: self._add_digit(digit))
            self._numpad_buttons.append(btn)

        positions = [(i, j) for i in range(3) for j in range(3)] + [(3, 1)]
        for pos, btn in zip(positions, self._numpad_buttons):
            self._numpad_layout.addWidget(btn, *pos)

        self._btn_backspace = QPushButton("⬅️")
        self._btn_backspace.setFixedSize(50, 50)
        self._btn_backspace.clicked.connect(self._remove_digit)

        self._btn_clear = QPushButton("❌")
        self._btn_clear.setFixedSize(50, 50)
        self._btn_clear.clicked.connect(lambda: self._input_pin.setText(""))

        self._numpad_layout.addWidget(self._btn_backspace, 3, 0)
        self._numpad_layout.addWidget(self._btn_clear, 3, 2)

    def _add_digit(self, digit):
        if len(self._input_pin.text()) < MAX_PIN_LENGTH:
            self._input_pin.setText(self._input_pin.text() + str(digit))

    def _remove_digit(self):
        self._input_pin.setText(self._input_pin.text()[:-1])

    def _toggle_pin_visibility(self):
        if self._btn_toggle_pin.isChecked():
            self._input_pin.setEchoMode(QLineEdit.EchoMode.Normal)
            self._btn_toggle_pin.setText("🙈")
        else:
            self._input_pin.setEchoMode(QLineEdit.EchoMode.Password)
            self._btn_toggle_pin.setText("👁")

    # ========== REFRESH PAGE ==========

    def refresh_page(self):
        if self.parent_app.usb_path is None:
            self.setEnabled(False)
            change_opacity(widget=self, value=0.5)
        else:
            self.setEnabled(True)
            change_opacity(widget=self, value=1.0)

    # ========== HELPER FUNCTIONS ==========

    def _validate_user_entries(self):
        if not self._input_pin.text():
            error_message = "PIN is empty"

            logger.error(error_message)

            error_dialog = QMessageBox.critical(
                self,
                "Validation error",
                error_message,
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return False
        if not self._key_filename_input.text():
            error_message = "Key filename is empty"
            logger.error(error_message)
            error_dialog = QMessageBox.critical(
                self,
                "Validation error",
                error_message,
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return False
        return True


    # ========== RSA WORKER THREADED FUNCTIONALITY ==========

    def _generate_and_encrypt_keypair(self):
        logger.info("User prompted for key generation and encryption")
        if not self._validate_user_entries():
            return
        pin = self._input_pin.text()
        key_filename = self._key_filename_input.text()
        usb_path = self.parent_app.usb_path

        self._progress_dialog = QProgressDialog("Starting...", None, 0, 0, self)
        self._progress_dialog.setWindowTitle("Key generation and encryption status")
        self._progress_dialog.setCancelButton(None)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._progress_dialog.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self._progress_dialog.setGeometry(300, 300, 400, 100)
        self._progress_dialog.show()

        self._rsa_worker_thread = RSAWorkerThread(pin=pin, filename=key_filename, usb_path=usb_path)
        self._rsa_worker_thread.change_progress_signal.connect(self._rsa_worker_update_progress)
        self._rsa_worker_thread.task_finished_signal.connect(self._rsa_worker_task_finished)
        self._rsa_worker_thread.start()

    def _rsa_worker_update_progress(self, message):
        logger.info(f"Key generation and encryption progress: {message}")
        self._progress_dialog.setLabelText(message)

    def _rsa_worker_task_finished(self):
        self._progress_dialog.close()

