import base64
import hashlib
import os

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter


class DecryptionError(Exception):
   pass


def decrypt_private_key(private_key_filepath, pin):
   try:
      with open(private_key_filepath, "rb") as f:
         data = f.read()
      nonce = data[:16]
      tag = data[16:32]
      ciphertext = data[32:]

      hashed_pin = hashlib.sha256(pin.encode()).digest()
      cipher = AES.new(hashed_pin, AES.MODE_GCM, nonce=nonce)
      return RSA.import_key(cipher.decrypt_and_verify(ciphertext, tag))
   except ValueError:
      raise DecryptionError




def sign_pdf_file(decrypted_private_key, pdf_filepath):
   reader = PdfReader(pdf_filepath)
   writer = PdfWriter()

   for page in reader.pages:
      writer.add_page(page)

   pdf_bytes = b"".join([page.extract_text().encode() for page in reader.pages if page.extract_text()])
   hash_obj = SHA256.new(pdf_bytes)

   signature = pkcs1_15.new(decrypted_private_key).sign(hash_obj)

   writer.add_metadata({"/Signature": base64.b64encode(signature).decode()})

   dir_path, filename = os.path.split(pdf_filepath)
   signed_pdf_filename = f"signed_{filename}"
   with open(os.path.join(dir_path, signed_pdf_filename), "wb") as f:
      writer.write(f)
