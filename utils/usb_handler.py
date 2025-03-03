import logging
from pathlib import Path

import psutil
import win32api
import win32file

from constants import LOGGER_GLOBAL_NAME

logger = logging.getLogger(LOGGER_GLOBAL_NAME)


def check_for_usb_device() -> tuple[bool, list]:
    usb_disks = []

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

    if usb_disks:
        print(f"USB storage devices detected: {usb_disks}")
        return True, usb_disks
    else:
        print("No USB storage devices detected.")
        return False, None

def search_usb_for_private_key(usb_path) -> list:
    key_files_found = []

    for path in Path(usb_path).rglob('*.key'):
        key_files_found.append(path)
    return key_files_found
