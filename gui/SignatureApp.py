import logging
import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QLineEdit, QLabel, QStackedWidget, QGroupBox, QGridLayout, QMessageBox, QFrame
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer

from constants import STYLES_DIR_PATH, LOGGER_GLOBAL_NAME
from gui.PageKeygen import KeygenPage
from gui.PageSign import SignPage
from gui.PageVerify import VerifyPage
from utils.usb_handler import check_for_usb_device

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

class SignatureApp(QWidget):
    # ========== INITIALIZE GUI ==========

    def __init__(self):
        logger.info("Initializing SignatureApp...")
        super().__init__()
        self.initUI()
        self.show()
        logger.info("SignatureApp initialized")

    def initUI(self):
        self.setWindowTitle("PAdES Signature Tool")
        self.setGeometry(100, 100, 900, 500)

        self.load_stylesheet()

        self.main_layout = QHBoxLayout(self)

        # ========== SIDE MENU ==========
        self.create_side_menu()

        # ========== CONTENT AREA ==========
        self.create_content_area()

        self.main_layout.addLayout(self.side_menu, 1)
        self.main_layout.addWidget(self.content_area, 4)

        self.setLayout(self.main_layout)

        self.update_usb_status()

    # ========== PAGE SWITCHING ==========

    def switch_page(self, index):
        self.content_area.setCurrentIndex(index)
        logger.info(f"Switched to page {index}")

    # ========== USB STATUS ==========

    def update_usb_status(self):
        result, drives = check_for_usb_device()
        if result:
            (self.btn_usb.setText
                (
                f"✅ USB detected\n"
                f"{drives[0]['device']}{drives[0]['name']}"
                )
            )
        else:
            self.btn_usb.setText("❌ No USB detected")

        QTimer.singleShot(5000, self.update_usb_status)

    # ========== STYLESHEET ==========

    def load_stylesheet(self):
        try:
            with open(os.path.join(STYLES_DIR_PATH, 'signature_app.css')) as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Error loading CSS file: {e}")

    # ========== SIDE MENU ==========

    def create_side_menu(self):
        self.side_menu = QVBoxLayout()
        self.side_menu.setSpacing(15)

        self.btn_keygen = QPushButton("🔑 Key Generation", self)
        self.btn_sign = QPushButton("✍️ Sign PDF", self)
        self.btn_verify = QPushButton("✅ Verify Signature", self)
        self.btn_usb = QPushButton("USB Status: ❌ No USB detected", self)
        self.btn_usb.setDisabled(True)

        for btn in [self.btn_keygen, self.btn_sign, self.btn_verify, self.btn_usb]:
            if btn == self.btn_usb:
                btn.setFixedHeight(80)
            else:
                btn.setFixedHeight(50)

            self.side_menu.addWidget(btn)

        self.side_menu.addStretch()

    # ========== CONTENT AREA ==========

    def create_content_area(self):
        self.content_area = QStackedWidget(self)

        self.page_keygen = KeygenPage()
        self.page_sign = SignPage()
        self.page_verify = VerifyPage()

        self.content_area.addWidget(self.page_keygen)  # Index 0
        self.content_area.addWidget(self.page_sign)  # Index 1
        self.content_area.addWidget(self.page_verify)  # Index 2

        self.btn_keygen.clicked.connect(lambda x: self.switch_page(0))
        self.btn_sign.clicked.connect(lambda x: self.switch_page(1))
        self.btn_verify.clicked.connect(lambda x: self.switch_page(2))