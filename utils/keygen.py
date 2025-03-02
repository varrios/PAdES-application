from constants import RSA_KEY_LENGTH
from Crypto.PublicKey import RSA


'''
    "2nd auxillary application" functionality 
'''

def save_RSA_keypair():
    pass

def generate_RSA_keypair():
    key = RSA.generate(RSA_KEY_LENGTH)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


