from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QPushButton, QLineEdit


class KeygenPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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
        self.setLayout(layout)