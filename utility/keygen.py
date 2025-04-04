import logging
import os

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import hashlib

from constants import RSA_KEY_LENGTH, KEYS_DIR_PATH

## @file keygen.py
## @brief RSA key generation and encryption functionality
##
## Provides functions to generate RSA keypairs and encrypt private keys using AES.
## Part of the "2nd auxillary application" functionality for the PAdES application.

from constants import LOGGER_GLOBAL_NAME

logger = logging.getLogger(LOGGER_GLOBAL_NAME)

## @brief Generates an RSA key pair with the specified key length
## @return Tuple containing (private_key, public_key) as bytes
def generate_RSA_keypair():
    key = RSA.generate(RSA_KEY_LENGTH)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

## @brief Encrypts a private key using AES-GCM with a PIN-derived key
## @param private_key The private key bytes to encrypt
## @param pin The user's PIN for encryption
## @return Encrypted private key bytes (nonce + tag + ciphertext)
def encrypt_private_key(private_key, pin):
    key = hashlib.sha256(pin.encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(private_key)
    return cipher.nonce + tag + ciphertext





