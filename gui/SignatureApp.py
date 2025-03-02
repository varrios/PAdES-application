import logging
import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLineEdit, QLabel, QStackedWidget, QGroupBox, QGridLayout, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation

from constants import STYLES_DIR_PATH, LOGGER_GLOBAL_NAME

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

class SignatureApp(QWidget):
    def __init__(self):
        self.page_verify = None
        self.page_sign = None
        self.page_keygen = None
        self.btn_usb = None
        self.btn_verify = None
        self.btn_sign = None
        self.btn_keygen = None
        self.main_layout = None
        self.side_menu = None
        self.content_area = None
        
        
        logger.info("Initializing SignatureApp...")
        super().__init__()
        self.initUI()
        self.show()
        logger.info("SignatureApp initialized")

    def initUI(self):
        self.setWindowTitle("PAdES Signature Tool")
        self.setGeometry(100, 100, 900, 500)

        try:
            with open(os.path.join(STYLES_DIR_PATH, 'signature_app.css')) as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Error loading CSS file: {e}")

        self.main_layout = QHBoxLayout(self)

        # ========== SIDE MENU ==========
        self.side_menu = QVBoxLayout()
        self.side_menu.setSpacing(15)

        self.btn_keygen = QPushButton("🔑 Key Generation", self)
        self.btn_sign = QPushButton("✍️ Sign PDF", self)
        self.btn_verify = QPushButton("✅ Verify Signature", self)
        self.btn_usb = QPushButton("USB Status: ❌ No USB detected", self)
        self.btn_usb.setDisabled(True)

        for btn in [self.btn_keygen, self.btn_sign, self.btn_verify, self.btn_usb]:
            btn.setFixedHeight(50)
            self.side_menu.addWidget(btn)

        self.side_menu.addStretch()

        # ========== CONTENT AREA ==========
        self.content_area = QStackedWidget(self)

        self.page_keygen = self.create_keygen_page()
        self.page_sign = self.create_sign_page()
        self.page_verify = self.create_verify_page()

        self.content_area.addWidget(self.page_keygen)  # Index 0
        self.content_area.addWidget(self.page_sign)  # Index 1
        self.content_area.addWidget(self.page_verify)  # Index 2

        self.btn_keygen.clicked.connect(lambda x: self.switch_page(0))
        self.btn_sign.clicked.connect(lambda x: self.switch_page(1))
        self.btn_verify.clicked.connect(lambda x: self.switch_page(2))

        self.main_layout.addLayout(self.side_menu, 1)
        self.main_layout.addWidget(self.content_area, 4)

        self.setLayout(self.main_layout)

    # ========== CREATE PAGES ==========
    def create_keygen_page(self):
        logger.info("Creating Keygen Page...")
        page = QWidget()
        layout = QVBoxLayout()

        group = QGroupBox("🔑 Generate RSA Key Pair and store on USB")
        group_layout = QGridLayout()

        btn_generate_keys = QPushButton("🔄 Generate RSA Keys")
        btn_select_usb = QPushButton("💾 Select USB Storage")
        input_pin = QLineEdit()
        input_pin.setPlaceholderText("Enter PIN (for encryption)")
        btn_save_key = QPushButton("🔐 Save Encrypted Private Key")

        group_layout.addWidget(btn_generate_keys, 0, 0, 1, 2)
        group_layout.addWidget(btn_select_usb, 1, 0, 1, 2)
        group_layout.addWidget(input_pin, 2, 0)
        group_layout.addWidget(btn_save_key, 2, 1)

        group.setLayout(group_layout)
        layout.addWidget(group)
        page.setLayout(layout)
        logger.info("Keygen Page created!")
        return page

    def create_sign_page(self):
        logger.info("Creating Sign Page...")
        page = QWidget()
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
        page.setLayout(layout)
        logger.info("Sign Page created!")
        return page

    def create_verify_page(self):
        logger.info("Creating Verify Page...")
        page = QWidget()
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
        page.setLayout(layout)
        logger.info("Verify Page created!")
        return page

    # ========== PAGE SWITCHING ==========
    def switch_page(self, index):
        self.content_area.setCurrentIndex(index)
        logger.info(f"Switched to page {index}")
