import logging
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit, QLabel
from constants import LOGGER_GLOBAL_NAME, VERIFY_PAGE_NAME

logger = logging.getLogger(LOGGER_GLOBAL_NAME)


class VerifyPage(QWidget):
    def __init__(self):
        logger.info("Initializing VerifyPage UI...")
        try:
            super().__init__()
            self.initUI()
            self.setObjectName(VERIFY_PAGE_NAME)
        except Exception as e:
            logger.error(f"Error initializing VerifyPage: {e}")
        else:
            logger.info("VerifyPage initialized successfully")

    def initUI(self):
        layout = QVBoxLayout()

        group = QGroupBox("✅ Verify Signed PDF")
        group_layout = QGridLayout()

        btn_select_signed_pdf = QPushButton("📄 Select Signed PDF")
        btn_load_public_key = QPushButton("🔑 Load Public Key")
        btn_verify = QPushButton("🔎 Verify Signature")
        label_result = QLabel("🔍 Signature Status: ❓")
        label_result.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        label_result.setAlignment(Qt.AlignmentFlag.AlignCenter)

        group_layout.addWidget(btn_select_signed_pdf, 0, 0, 1, 2)
        group_layout.addWidget(btn_load_public_key, 1, 0, 1, 2)
        group_layout.addWidget(btn_verify, 2, 0, 1, 2)
        group_layout.addWidget(label_result, 3, 0, 1, 2)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)