## @file PageSign.py
## @brief PDF signing page implementation
##
## Contains the UI and logic for the PDF signing page, allowing users
## to sign PDF documents with their private key.

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit, QLabel, QFileDialog, \
    QMessageBox, QProgressDialog, QProgressBar
from constants import LOGGER_GLOBAL_NAME, SIGN_PAGE_NAME
from utility.PDFWorkerThread import SignPDFWorkerThread
from utility.misc import change_opacity
from utility.pdf_sign import sign_pdf_file


logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief PDF signing page class
##
## Provides UI for selecting and signing PDF documents using a private key
class SignPage(QWidget):
    ## @brief Initializes the sign page
    ## @param parent Parent widget (main application)
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

    ## @brief Sets up the user interface components
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

    ## @brief Updates page state based on USB and key availability
    def refresh_page(self):
        if self.parent_app.usb_path is None or self.parent_app.private_key_found == False:
            self.setEnabled(False)
            change_opacity(widget=self, value=0.5)
        else:
            self.setEnabled(True)
            change_opacity(widget=self, value=1.0)


    ## @brief Opens a file dialog to select a PDF file for signing
    def _select_pdf_file(self):
        logger.info("User prompted to select PDF file to sign")
        pdf_to_sign_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF to Sign",
            "",
            "PDF Files (*.pdf)"
        )
        if pdf_to_sign_path:
            logger.info(f"User selected PDF file: {pdf_to_sign_path}")
            self.pdf_filepath = pdf_to_sign_path
            self._selected_file_label.setText(self.pdf_filepath)
        else:
            logger.info("User cancelled PDF selection")

    ## @brief Validates user input before signing
    ## @return Boolean indicating if validation passed
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

    ## @brief Initiates the PDF signing process with the private key
    def _sign_pdf_file(self):
        logger.info("User prompted to sign PDF file")
        if not self._validate_user_entries():
            return
        pin = self._input_sign_pin.text()
        private_key_path = self.parent_app.private_key_path
        pdf_filepath = self.pdf_filepath

        self._progress_dialog = QProgressDialog("Starting...", None, 0, 0, self)
        self._progress_dialog.setWindowTitle("PDF signing status")
        self._progress_dialog.setCancelButton(None)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._progress_dialog.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self._progress_dialog.setGeometry(300, 300, 400, 100)

        self._progress_dialog.show()

        self._pdf_worker_thread = SignPDFWorkerThread(pdf_filepath=pdf_filepath, pin=pin, private_key_filepath=private_key_path)
        self._pdf_worker_thread.change_progress_signal.connect(self._pdf_worker_update_progress)
        self._pdf_worker_thread.task_finished_signal.connect(self._pdf_worker_task_finished)
        self._pdf_worker_thread.start()

    ## @brief Updates progress dialog with status from the worker thread
    ## @param message Status message to display
    def _pdf_worker_update_progress(self, message):
        logger.info(f"PDF signing progress: {message}")
        self._progress_dialog.setLabelText(message)

    ## @brief Handles completion of the PDF signing process
    def _pdf_worker_task_finished(self):
        self._progress_dialog.close()







