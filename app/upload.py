#Upload data to S3

import boto3
from botocore.exceptions import NoCredentialsError
import sys

from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
import os

def save_keys(aes_key, hmac_key, key_name):
    os.makedirs("keys", exist_ok=True)
    with open(f"keys/{key_name}.aes", "wb") as f:
        f.write(aes_key)
    
    with open(f"keys/{key_name}.hmac", "wb") as f:
        f.write(hmac_key)

def cipher_data(local_file_path, aes_key, hmac_key):
    
    with open(local_file_path, 'rb') as f:
        data = f.read()
        cipher = AES.new(aes_key, AES.MODE_CTR)
        ciphertext = cipher.encrypt(data)

        hmac = HMAC.new(hmac_key, digestmod=SHA256)
        tag = hmac.update(cipher.nonce + ciphertext).digest() 
    
    os.makedirs("encrypted", exist_ok=True)
    
    with open(f"encrypted/{os.path.basename(local_file_path)}.ciph", "wb") as f:
        f.write(tag)
        f.write(cipher.nonce)
        f.write(ciphertext)  

def upload_to_s3(local_file_path, bucket_name, s3_file_name):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

# Example usage
local_file_path = sys.argv[1]
bucket_name = 'testspaperdianabucket'
s3_file_name = sys.argv[1]

aes_key = get_random_bytes(16)
hmac_key = get_random_bytes(16)

cipher_data(local_file_path, aes_key, hmac_key)
save_keys(aes_key, hmac_key, os.path.basename(local_file_path))

upload_to_s3(f"encrypted/{os.path.basename(local_file_path)}.ciph", bucket_name, s3_file_name)
