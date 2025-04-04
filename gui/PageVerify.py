## @file PageVerify.py
## @brief PDF signature verification page implementation
##
## Contains the UI and logic for the signature verification page, allowing users
## to verify PDF document signatures using the public key.

import logging
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton,
    QLabel, QFileDialog, QMessageBox, QProgressDialog
)

from constants import LOGGER_GLOBAL_NAME, VERIFY_PAGE_NAME
from utility.VerifyPDFWorkerThread import VerifyPDFWorkerThread
from utility.misc import change_opacity

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief PDF signature verification page class
##
## Provides UI for selecting and verifying signed PDF documents using a public key
class VerifyPage(QWidget):
    ## @brief Initializes the verify page
    ## @param parent Parent widget (main application)
    def __init__(self, parent):
        logger.info("Initializing VerifyPage UI...")
        try:
            self.parent_app = parent
            self.pdf_filepath = None
            super().__init__()
            self._init_ui()
            self.setObjectName(VERIFY_PAGE_NAME)
        except Exception as e:
            logger.error(f"Error initializing VerifyPage: {e}")
        else:
            logger.info("VerifyPage initialized successfully")

    ## @brief Sets up the user interface components
    def _init_ui(self):
        layout = QVBoxLayout()

        group = QGroupBox("✅ Verify Signed PDF")
        group_layout = QGridLayout()

        self._btn_select_signed_pdf = QPushButton("📄 Select Signed PDF")
        self._btn_select_signed_pdf.clicked.connect(self._select_pdf_file)

        self._selected_file_label = QPushButton("No file selected")
        self._selected_file_label.setDisabled(True)

        self._btn_verify = QPushButton("🔎 Verify Signature")
        self._btn_verify.clicked.connect(self._verify_pdf_file)

        self._label_result = QLabel("🔍 Signature Status: ❓")
        self._label_result.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self._label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        group_layout.addWidget(self._btn_select_signed_pdf, 0, 0, 1, 2)
        group_layout.addWidget(self._selected_file_label, 1, 0, 1, 2)
        group_layout.addWidget(self._btn_verify, 2, 0, 1, 2)
        group_layout.addWidget(self._label_result, 3, 0, 1, 2)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)

    ## @brief Updates page state based on public key availability
    def refresh_page(self):
        if self.parent_app.public_key_found == False:
            self.setEnabled(False)
            change_opacity(widget=self, value=0.5)
        else:
            self.setEnabled(True)
            change_opacity(widget=self, value=1.0)

    ## @brief Opens a file dialog to select a signed PDF file for verification
    def _select_pdf_file(self):
        logger.info("User prompted to select PDF file to verify")
        pdf_to_verify_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF to Verify",
            "",
            "PDF Files (*.pdf)"
        )
        if pdf_to_verify_path:
            logger.info(f"User selected PDF file: {pdf_to_verify_path}")
            self.pdf_filepath = pdf_to_verify_path
            self._selected_file_label.setText(self.pdf_filepath)
        else:
            logger.info("User cancelled PDF selection")

    ## @brief Validates user input before verification
    ## @return Boolean indicating if validation passed
    def _validate_user_entries(self):
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
        if not self.parent_app.public_key_found:
            error_message = "No public key found on local machine"
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

    ## @brief Initiates the PDF signature verification process
    def _verify_pdf_file(self):
        logger.info("User prompted to verify PDF signature")
        if not self._validate_user_entries():
            return

        public_key_path = self.parent_app.public_key_path
        pdf_filepath = self.pdf_filepath

        self._progress_dialog = QProgressDialog("Starting...", None, 0, 0, self)
        self._progress_dialog.setWindowTitle("PDF verification status")
        self._progress_dialog.setCancelButton(None)
        self._progress_dialog.setMinimumDuration(0)
        self._progress_dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._progress_dialog.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)
        self._progress_dialog.setGeometry(300, 300, 400, 100)

        self._progress_dialog.show()

        self._verify_worker_thread = VerifyPDFWorkerThread(
            pdf_filepath=pdf_filepath,
            public_key_filepath=public_key_path
        )
        self._verify_worker_thread.change_progress_signal.connect(self._verify_worker_update_progress)
        self._verify_worker_thread.task_finished_signal.connect(self._verify_worker_task_finished)
        self._verify_worker_thread.start()

    ## @brief Updates progress dialog with status from the worker thread
    ## @param message Status message to display
    def _verify_worker_update_progress(self, message):
        logger.info(f"PDF verification progress: {message}")
        self._progress_dialog.setLabelText(message)

    ## @brief Handles completion of the verification process
    ## @param is_valid Boolean indicating if signature is valid
    ## @param message Message explaining verification result
    def _verify_worker_task_finished(self, is_valid, message):
        self._progress_dialog.close()
        if is_valid:
            self._label_result.setText(f"✅ {message}")
            self._label_result.setStyleSheet("color: green;")
        else:
            self._label_result.setText(f"❌ {message}")
            self._label_result.setStyleSheet("color: red;")