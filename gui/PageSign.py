import logging

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QMessageBox
from constants import LOGGER_GLOBAL_NAME, SIGN_PAGE_NAME
from utility.misc import change_opacity
from utility.pdf_sign import sign_pdf_file


logger = logging.getLogger(LOGGER_GLOBAL_NAME)


class SignPage(QWidget):
    def __init__(self, parent):
        logger.info("Initializing SignPage UI...")
        try:
            self.pdf_filepath = None
            self.parent_app = parent
            super().__init__()
            self._init_ui()
            self.setObjectName(SIGN_PAGE_NAME)
        except Exception as e:
            logger.error(f"Error initializing SignPage: {e}")
        else:
            logger.info("SignPage initialized successfully")

    def _init_ui(self):
        layout = QVBoxLayout()

        self._group = QGroupBox("✍️ Select PDF & Sign with RSA Key")

        self._btn_select_pdf = QPushButton("📄 Select PDF to Sign")
        self._btn_select_pdf.clicked.connect(self._select_pdf_file)

        self._selected_file_label = QPushButton("No file selected")
        self._selected_file_label.setDisabled(True)

        self._input_sign_pin = QLineEdit()
        self._input_sign_pin.setPlaceholderText("Enter PIN to Decrypt Key")
        self._input_sign_pin.setMaxLength(6)
        self._input_sign_pin.setValidator(QIntValidator(0, 999999, self))

        self._btn_sign = QPushButton("✔️ Sign & Save PDF")
        self._btn_sign.clicked.connect(self._sign_pdf_file)

        group_layout = QVBoxLayout()
        group_layout.addWidget(self._btn_select_pdf)
        group_layout.addWidget(self._selected_file_label)
        group_layout.addWidget(self._input_sign_pin)
        group_layout.addWidget(self._btn_sign)

        self._group.setLayout(group_layout)

        layout.addWidget(self._group)
        self.setLayout(layout)

    # ========== REFRESH PAGE ==========

    def refresh_page(self):
        if self.parent_app.usb_path is None or self.parent_app.private_key_found == False:
            self.setEnabled(False)
            change_opacity(widget=self, value=0.5)
        else:
            self.setEnabled(True)
            change_opacity(widget=self, value=1.0)


    def _select_pdf_file(self):
        pdf_to_sign_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF to Sign",
            "",
            "PDF Files (*.pdf)"
        )
        if pdf_to_sign_path:
            self.pdf_filepath = pdf_to_sign_path
            self._selected_file_label.setText(self.pdf_filepath)

    def _sign_pdf_file(self):
        if not self._validate_user_entries():
            return
        pin = self._input_sign_pin.text()
        private_key_path = self.parent_app.private_key_path
        sign_pdf_file(pin, self.pdf_filepath, private_key_path)




    def _validate_user_entries(self):
        if not self._input_sign_pin.text():
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
        if not self.pdf_filepath:
            error_message = "No PDF file selected"
            logger.error(error_message)
            error_dialog = QMessageBox.critical(
                self,
                "Validation error",
                error_message,
                buttons=QMessageBox.StandardButton.Ok,
                defaultButton=QMessageBox.StandardButton.Ok,
            )
            return False
        if not self.parent_app.private_key_found:
            error_message = "No private key found on usb"
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








