import hashlib

from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA


def decrypt_private_key(private_key_filepath, pin):
   with open(private_key_filepath, "rb") as f:
      data = f.read()
   nonce = data[:16]
   tag = data[16:32]
   ciphertext = data[32:]

   hashed_pin = hashlib.sha256(pin.encode()).digest()
   cipher = AES.new(hashed_pin, AES.MODE_GCM, nonce=nonce)
   return RSA.import_key(cipher.decrypt_and_verify(ciphertext, tag))



def sign_pdf_file(decrypted_private_key, pdf_filepath):


   return