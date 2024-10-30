import boto3
from botocore.exceptions import NoCredentialsError
import sys
from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256


def download_from_s3(bucket_name, s3_file_name, local_file_path):
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Download the file
        s3.download_file(bucket_name, s3_file_name, f"encrypted/{s3_file_name}")
        print("Download Successful")
        return True
    except FileNotFoundError as e:
        print("The file was not found on S3")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    
def decrypt(ciphered_path, key_path, output_filename):
    with open(f"{key_path}.aes", "rb") as f:
        aes_key = f.read()
    
    with open(f"{key_path}.hmac", "rb") as f:
        hmac_key = f.read()
    
    with open(ciphered_path, "rb") as f:
        tag = f.read(32)
        nonce = f.read(8)
        ciphertext = f.read()
        
    try:
        hmac = HMAC.new(hmac_key, digestmod=SHA256)
        tag = hmac.update(nonce + ciphertext).verify(tag)
    except ValueError:
        print("The message was modified!")
        sys.exit(1)

    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    message = cipher.decrypt(ciphertext)
    
    with open(output_filename, "wb") as f:
        f.write(message)

# Example usage
local_file_path = "downloads/" + sys.argv[1]
bucket_name = 'testspaperdianabucket'
s3_file_name = sys.argv[1]
 
download_from_s3(bucket_name, s3_file_name, local_file_path)

decrypt(f"encrypted/{s3_file_name}.ciph", "keys/" + s3_file_name, local_file_path)
