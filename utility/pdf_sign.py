import base64
import hashlib
import os

from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import pkcs1_15
from PyPDF2 import PdfReader, PdfWriter


## @brief Exception raised when private key decryption fails
class DecryptionError(Exception):
   pass


## @brief Decrypt a private key using a PIN
## @param private_key_filepath Path to the encrypted private key file
## @param pin User PIN for decryption
## @return Decrypted RSA key object
## @throws DecryptionError if PIN is incorrect or decryption fails
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



## @brief Signs a PDF file using a private key
## @param decrypted_private_key The decrypted RSA private key
## @param pdf_filepath Path to the PDF file to be signed
def sign_pdf_file(decrypted_private_key, pdf_filepath):
    reader = PdfReader(pdf_filepath)
    writer = PdfWriter()

    if "/Signature" in reader.metadata:
      raise ValueError("PDF already has a signature.")

    for page in reader.pages:
        writer.add_page(page)

    pdf_bytes = b"".join([page.extract_text().encode() for page in reader.pages if page.extract_text()])
    hash_obj = SHA256.new(pdf_bytes)

    signature = pkcs1_15.new(decrypted_private_key).sign(hash_obj)

    writer.add_metadata({"/Signature": base64.b64encode(signature).decode()})

    dir_path, filename = os.path.split(pdf_filepath)
    signed_pdf_filename = f"SIGNED_{filename}"
    with open(os.path.join(dir_path, signed_pdf_filename), "wb") as f:
        writer.write(f)

## @brief Verifies the signature of a signed PDF file
## @param pdf_filepath Path to the signed PDF file
## @param public_key_filepath Path to the public key file
## @return Tuple (is_valid, message) where is_valid is a boolean indicating if the signature is valid
def verify_pdf_signature(pdf_filepath, public_key_filepath):
   try:
      with open(public_key_filepath, "rb") as f:
         public_key = RSA.import_key(f.read())

      reader = PdfReader(pdf_filepath)
      metadata = reader.metadata

      if "/Signature" not in metadata:
         return False, "No signature found in the PDF"

      signature = base64.b64decode(metadata["/Signature"])

      pdf_bytes = b"".join([page.extract_text().encode() for page in reader.pages if page.extract_text()])
      hash_obj = SHA256.new(pdf_bytes)

      pkcs1_15.new(public_key).verify(hash_obj, signature)
      return True, "Signature verified successfully"
   except ValueError:
      return False, "Invalid signature"
   except Exception as e:
      return False, f"Verification failed"
