# Matthew Chu
# Password Encryption Methods
# https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html
# https://crypto.stackexchange.com/questions/8121/aes-plaintext-is-smaller-than-128-bits-how-to-expand
# https://www.cryptosys.net/pki/manpki/pki_paddingschemes.html
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16  # Standard AES block size of 128 bits (16 bytes)


# Method takes a message/text and a secret key
def Encrypt(msg, key):
    iv = os.urandom(16)  # Initialization Vector 16 byte string; used in streaming
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())  # Creates a new cipher based on the AES algorithm and its key, the method of encryption(in this case being CTR, which is counter)), and establishing the location of streamed data
    encryptor = cipher.encryptor()
    ct = cipher.update(msg.encode("utf-8")) + encryptor.finalize()
    return base64.b64encode(ct + ":" + iv) # returns a base64 encoded version of the given ciphertext


def Decrypt(cipher, key):
    enc = base64.b64decode(cipher)  # decodes from base 64 to bytes
    decryptor = Cipher(algorithms.AES(key), modes.CTR(cipher[33:]), backend=default_backend())
    decryptor.update(enc) + decryptor.finalize()
    return decryptor
