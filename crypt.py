from Crypto.Cipher import AES
from Crypto import Random
import base64

from PBKDF2 import PBKDF2

block_size = 16
key_size = 32
mode = AES.MODE_CBC 

def GenerateKey():
  key_bytes = Random.new().read(key_size)
  key_string = base64.urlsafe_b64encode(str(key_bytes)) 

  return (key_bytes, key_string)

def getKey(passphrase):
  salt = "\\x91\\x13nyP\\x0fO&" # random salt
  key = PBKDF2(passphrase, salt).read(key_size)
  return key

def encode(key_string, data):
  plain_text = data
  key = getKey(key_string)

  pad = block_size - len(plain_text) % block_size 
  data = plain_text + pad * chr(pad) 
  iv_bytes = Random.new().read(block_size)
  encrypted_bytes = iv_bytes + AES.new(key, mode, iv_bytes).encrypt(data) 

  encrypted_string = str(encrypted_bytes)

  return encrypted_string

def decode(key_string, data):
  key = getKey(key_string)

  encrypted_bytes = data
  iv_bytes = encrypted_bytes[:block_size] 
  encrypted_bytes = encrypted_bytes[block_size:] 
  plain_text = AES.new(key, mode, iv_bytes).decrypt(encrypted_bytes)
  pad = ord(plain_text[-1]) 
  plain_text = plain_text[:-pad] 

  return plain_text
