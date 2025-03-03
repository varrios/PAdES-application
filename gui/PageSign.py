import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit, QLabel
from constants import LOGGER_GLOBAL_NAME, SIGN_PAGE_NAME

logger = logging.getLogger(LOGGER_GLOBAL_NAME)


class SignPage(QWidget):
    def __init__(self):
        logger.info("Initializing SignPage UI...")
        try:
            super().__init__()
            self.initUI()
            self.setObjectName(SIGN_PAGE_NAME)
        except Exception as e:
            logger.error(f"Error initializing SignPage: {e}")
        else:
            logger.info("SignPage initialized successfully")

    def initUI(self):
        layout = QVBoxLayout()

        group = QGroupBox("✍️ Select PDF & Sign with RSA Key")
        group_layout = QGridLayout()

        btn_select_pdf = QPushButton("📄 Select PDF to Sign")
        btn_load_key = QPushButton("🔍 Detect USB & Load Private Key")
        input_sign_pin = QLineEdit()
        input_sign_pin.setPlaceholderText("Enter PIN to Decrypt Key")
        btn_sign = QPushButton("✔️ Sign & Save PDF")

        group_layout.addWidget(btn_select_pdf, 0, 0, 1, 2)
        group_layout.addWidget(btn_load_key, 1, 0, 1, 2)
        group_layout.addWidget(input_sign_pin, 2, 0)
        group_layout.addWidget(btn_sign, 2, 1)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)