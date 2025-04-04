## @file usb_handler.py
## @brief USB detection and private key management
##
## Provides functionality to detect USB devices and search for keys.

import logging
import os
from pathlib import Path
from dotenv import load_dotenv

import psutil
# TYLKO NA WINDOWS - win32api, win32file

if os.name == "nt":
    import win32api
    import win32file

from constants import LOGGER_GLOBAL_NAME

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief Checks for USB storage devices connected to the system
## @return Tuple (bool, list|None) - True if USB devices found, with a list of device details
def check_for_usb_device() -> tuple[bool, list | None]:
    usb_disks = []

    if os.name == "nt":
        for partition in psutil.disk_partitions(all=True):
            device = partition.device

            drive_type = win32file.GetDriveType(device)
            if drive_type == win32file.DRIVE_REMOVABLE:
                try:
                    volume_name, _, _, _, _ = win32api.GetVolumeInformation(device)
                except Exception:
                    volume_name = "Unknown"

                usb_disks.append({
                    "device": device,
                    "name": volume_name
                })
    else: # TESTING PURPOSES ONLY FOR UNIX-BASED SYSTEMS
        load_dotenv()
        usb_disks.append({
            "device": os.getenv('CUSTOM_FILEPATH'),
            "name": "USB SIMULATON"
        })
    if usb_disks:
        logger.info(f"USB storage devices detected: {len(usb_disks)}")
        return True, usb_disks
    else:
        logger.info("No USB storage devices detected")
        return False, None

## @brief Search a USB drive for private key files (.key extension)
## @param usb_path Path to the USB drive to search
## @return List of paths to key files found
def search_usb_for_private_key(usb_path) -> list:
    key_files_found = []

    for path in Path(usb_path).rglob('*.key'):
        key_files_found.append(path)
    return key_files_found

## @brief Search local machine for public key files (.pem extension)
## @param local_machine_path Path on local machine to search
## @return List of paths to public key files found
def search_local_machine_for_public_key(local_machine_path) -> list:
    key_files_found = []

    for path in Path(local_machine_path).rglob('*.pem'):
        key_files_found.append(path)
    return key_files_found
