import os

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
import hashlib

from constants import RSA_KEY_LENGTH, KEYS_DIR_PATH

'''
    "2nd auxillary application" functionality 
'''

def generate_RSA_keypair():
    key = RSA.generate(RSA_KEY_LENGTH)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_private_key(private_key, pin):
    key = hashlib.sha256(pin.encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(private_key)
    return cipher.nonce, ciphertext, tag

def decrypt_private_key(nonce, ciphertext, tag, pin):
    key = hashlib.sha256(pin.encode()).digest()
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

