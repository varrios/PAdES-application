
from utility.keygen import decrypt_private_key

def sign_pdf_file(pin, filepath, private_key_path):
   print(f"Signing PDF file with pin={pin} filepath={filepath} private_key_path={private_key_path}")
   
   with open(private_key_path, "rb") as f:
        data = f.read()

   nonce = data[:16]
   tag = data[-16:]
   ciphertext = data[16:-16]
   print(decrypt_private_key(nonce, ciphertext, tag, pin))

   return