from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit, QLabel


class SignPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

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