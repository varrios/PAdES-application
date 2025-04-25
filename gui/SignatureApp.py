## @file SignatureApp.py
## @brief Signature application window class
##
## Contains the main window of the application with all the UI components
## and handles navigation between pages.

import logging
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget
)



from constants import LOGGER_GLOBAL_NAME, KEYGEN_PAGE_NAME, SIGN_PAGE_NAME, VERIFY_PAGE_NAME, \
    MAIN_WINDOW_TITLE, ICON_FILE_PATH, STYLESHEET_FILE_PATH, KEYS_DIR_PATH
from gui.PageKeygen import KeygenPage
from gui.PageSign import SignPage
from gui.PageVerify import VerifyPage
from utility.usb_handler import check_for_usb_device, search_usb_for_private_key, search_local_machine_for_public_key

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief Signature application window class
##
## Manages the main application window, page switching, and USB detection
class SignatureApp(QWidget):
    ## @brief Initializes the main application window
    def __init__(self):
        self._main_layout = None
        self._side_menu = None
        self._content_area = None

        self._btn_usb = None
        self._btn_verify = None
        self._btn_sign = None
        self._btn_keygen = None

        self._page_verify = None
        self._page_sign = None

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

        logger.info("==== INITIALIZING GUI ====")
        super().__init__()
        self._init_ui()
        self.show()
        logger.info("==== GUI INITIALIZATION FINISHED ====")

        self._refresh_pages()

    ## @brief Sets up the user interface
    def _init_ui(self):
        self.setWindowTitle(MAIN_WINDOW_TITLE)
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

    ## @brief Switches to the specified page
    ## @param page_name Name of the page to switch to
    def _switch_page(self, page_name):
        self._content_area.setCurrentWidget(self._content_area.findChild(QWidget, page_name))
        logger.info(f"Switched to page {page_name}")

    ## @brief Checks USB status and updates the UI
    ##
    ## Detects USB devices, searches for private keys on USB drives and public keys
    ## on the local machine. Updates instance variables with found paths and
    ## updates the USB status button text to display the current status.
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
    ##
    ## Updates USB status and refreshes all application pages.
    ## Sets a timer to call itself again after 2000ms (2 seconds).
    def _refresh_pages(self):
        logger.info("Refreshing pages...")
        self._update_usb_status()
        self._page_sign.refresh_page()
        self._page_verify.refresh_page()
        QTimer.singleShot(2000, self._refresh_pages)

    ## @brief Loads the application stylesheet from CSS file
    ##
    ## Attempts to read and apply the CSS style from the file specified in STYLESHEET_FILE_PATH.
    ## Logs success or failure of the operation.
    def _load_stylesheet(self):
        try:
            with open(STYLESHEET_FILE_PATH) as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            logger.error(f"Error loading CSS file: {e}")
        else:
            logger.info("CSS file loaded successfully")

    ## @brief Creates the side navigation menu
    ##
    ## Sets up the layout and buttons for the side navigation menu,
    ## including sign and verify buttons and the USB status display.
    def _create_side_menu(self):
        self._side_menu = QVBoxLayout()
        self._side_menu.setSpacing(15)

        self._btn_sign = QPushButton("✍️ Sign PDF", self)
        self._btn_verify = QPushButton("✅ Verify Signature", self)
        self._btn_usb = QPushButton("USB Status: ❌ No USB detected", self)
        self._btn_usb.setDisabled(True)

        for btn in [self._btn_sign, self._btn_verify, self._btn_usb]:
            if btn == self._btn_usb:
                btn.setFixedHeight(180)
            else:
                btn.setFixedHeight(50)

            self._side_menu.addWidget(btn)

        self._side_menu.addStretch()

    ## @brief Creates the content area with all pages
    ##
    ## Initializes the stacked widget for content area, creates all page instances,
    ## adds them to the widget stack, and connects navigation buttons to page switching.
    def _create_content_area(self):
        self._content_area = QStackedWidget(self)

        self._page_sign = SignPage(parent=self)
        self._page_verify = VerifyPage(parent=self)

        self._content_area.addWidget(self._page_sign)
        self._content_area.addWidget(self._page_verify)

        self._btn_sign.clicked.connect(lambda x: self._switch_page(page_name=SIGN_PAGE_NAME))
        self._btn_verify.clicked.connect(lambda x: self._switch_page(page_name=VERIFY_PAGE_NAME))