## @file AuxiliaryApp.py
## @brief Auxiliary application window class
##
## Contains the main window of the auxiliary application with all the UI components.

import logging
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
)

from constants import LOGGER_GLOBAL_NAME, KEYGEN_PAGE_NAME, \
    ICON_FILE_PATH, STYLESHEET_FILE_PATH, KEYS_DIR_PATH, AUXILIARY_WINDOW_TITLE
from gui.PageKeygen import KeygenPage
from utility.usb_handler import check_for_usb_device, search_usb_for_private_key, search_local_machine_for_public_key

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief Auxiliary application window class
##
## Manages the auxiliary application window that focuses on key generation functionality.
## Includes USB detection and provides information about key status.
class AuxiliaryApp(QWidget):
    ## @brief Initializes the auxiliary application window
    def __init__(self):
        self._main_layout = None
        self._side_menu = None
        self._content_area = None

        self._btn_usb = None

        self._page_keygen = None

        # USB and Key handling
        ## @brief Path to the detected USB device
        self.usb_path : Path | None = None

        ## @brief Path to the private key file on USB
        self.private_key_path : Path | None = None
        ## @brief Flag indicating if a private key was found
        self.private_key_found : bool = False

        ## @brief Path to the public key file on local machine
        self.public_key_path : Path | None = None
        ## @brief Flag indicating if a public key was found
        self.public_key_found : bool = False

        logger.info("==== AUXILIARY APP INITIALIZING GUI ====")
        super().__init__()
        self._init_ui()
        self.show()
        logger.info("==== AUXILIARY APP GUI INITIALIZATION FINISHED ====")

        self._refresh_pages()

    ## @brief Sets up the user interface
    def _init_ui(self):
        self.setWindowTitle(AUXILIARY_WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_FILE_PATH))
        self.setGeometry(100, 100, 900, 500)

        self._load_stylesheet()

        self._main_layout = QHBoxLayout(self)

        # ========== SIDE MENU ==========
        self._create_side_menu()

        # ========== CONTENT AREA ==========
        self._create_content_area()

        self._main_layout.addLayout(self._side_menu, 1)
        self._main_layout.addWidget(self._content_area, 4)

        self.setLayout(self._main_layout)



    ## @brief Checks USB status and updates the UI
    def _update_usb_status(self):
        logger.info("Checking for USB devices...")
        result, drives = check_for_usb_device()

        usb_found_status = ""
        usb_private_key_found_status = ""
        local_public_key_found_status = ""

        # Search for public key on local machine
        public_keys_found = search_local_machine_for_public_key(local_machine_path=KEYS_DIR_PATH)
        if public_keys_found:
            self.public_key_found = True
            self.public_key_path = public_keys_found[0]
            local_public_key_found_status += \
                (
                    f"🔑 Public key found on local machine at:\n"
                    f"{str(public_keys_found[0])}"
                )
        else:
            self.public_key_found = False
            self.public_key_path = None
            local_public_key_found_status += "❌ No public key found on local machine"


        # If USB detected, search for private key
        if not result:
            self.usb_path = None
            self.private_key_found = False
            self.private_key_path = None
            usb_found_status += "❌ No USB detected"
        else:
            self.usb_path = drives[0]['device']
            usb_found_status += \
                (
                    f"🟢 USB detected:\n"
                    f"{drives[0]['device']}{drives[0]['name']}"
                )
            # Search for private key
            private_keys_found = search_usb_for_private_key(usb_path=self.usb_path)
            if private_keys_found:
                self.private_key_found = True
                self.private_key_path = private_keys_found[0]
                usb_private_key_found_status += \
                    (
                        f"🔑 Private key found on USB at:\n"
                        f"{str(private_keys_found[0])}"
                    )
            else:
                self.private_key_found = False
                usb_private_key_found_status += "❌ No private key found on USB drive"


        self._btn_usb.setText(
            f"{usb_found_status}\n"
            f"{usb_private_key_found_status}\n"
            f"{local_public_key_found_status}"
        )

    ## @brief Refreshes all pages status periodically
    def _refresh_pages(self):
        logger.info("Refreshing pages...")
        self._update_usb_status()
        self._page_keygen.refresh_page()
        QTimer.singleShot(2000, self._refresh_pages)

    ## @brief Loads the application stylesheet from CSS file
    def _load_stylesheet(self):
        try:
            with open(STYLESHEET_FILE_PATH) as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Error loading CSS file: {e}")
        else:
            logger.info("CSS file loaded successfully")

    ## @brief Creates the side navigation menu
    def _create_side_menu(self):
        self._side_menu = QVBoxLayout()
        self._side_menu.setSpacing(15)

        self._btn_usb = QPushButton("USB Status: ❌ No USB detected", self)
        self._btn_usb.setDisabled(True)
        self._btn_usb.setFixedHeight(180)
        self._side_menu.addWidget(self._btn_usb)

        self._side_menu.addStretch()

    ## @brief Creates the content area with all pages
    def _create_content_area(self):
        self._content_area = QStackedWidget(self)

        self._page_keygen = KeygenPage(parent=self)

        self._content_area.addWidget(self._page_keygen)
