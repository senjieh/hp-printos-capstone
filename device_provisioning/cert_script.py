import subprocess
import os
import datetime
import hashlib
import json
from datetime import datetime
from pymongo import MongoClient
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGOURI = os.getenv("MONGOURI")

# Setup MongoDB client and select the database and collection
client = MongoClient(MONGOURI, 27017)
db = client['hp_print_os']
collection = db['printers']

def datetime_to_unique_serial(dt_object):
    # Convert datetime object to Unix time (seconds since epoch)
    unix_time = int(dt_object.timestamp())
    # Convert Unix time to bytes
    unix_time_bytes = unix_time.to_bytes((unix_time.bit_length() + 7) // 8, 'big')
    # Hash the Unix time using SHA-256
    hash_object = hashlib.sha256(unix_time_bytes)
    # Convert the hash to a hexadecimal string for the serial code
    serial_code = hash_object.hexdigest()
    return serial_code

# Set your paths and filenames
device_id = datetime_to_unique_serial(datetime.now())
device_key_file = f"deviceid_{device_id}.key"
device_csr_file = f"deviceid_{device_id}.csr"
device_cert_file = f"deviceid_{device_id}.crt"
device_json_file = f"deviceid.json"
ca_cert_file = "rootCA.pem"
ca_key_file = "rootCA.key"
common_name = device_id

# Generate a new private key for the device
subprocess.run(["openssl", "genrsa", "-out", device_key_file, "2048"], check=True)

# Generate a CSR for the device
subprocess.run(["openssl", "req", "-new", "-key", device_key_file, "-out", device_csr_file, "-subj", f"/CN={common_name}"], check=True)

# Sign the CSR with your CA to get the device certificate
subprocess.run(["openssl", "x509", "-req", "-in", device_csr_file, "-CA", ca_cert_file, "-CAkey", ca_key_file, "-CAcreateserial", "-out", device_cert_file, "-days", "365", "-sha256"], check=True)


# Generate a new private key for the device in PEM format
subprocess.run(["openssl", "genrsa", "-out", device_key_file, "2048"], check=True)

# Convert the private key to DER format
device_key_file_der = f"deviceid_{device_id}_key.der"
subprocess.run(["openssl", "rsa", "-inform", "PEM", "-outform", "DER", "-in", device_key_file, "-out", device_key_file_der], check=True)

# Generate a CSR for the device
subprocess.run(["openssl", "req", "-new", "-key", device_key_file, "-out", device_csr_file, "-subj", f"/CN={common_name}"], check=True)

# Sign the CSR with your CA to get the device certificate in PEM format
subprocess.run(["openssl", "x509", "-req", "-in", device_csr_file, "-CA", ca_cert_file, "-CAkey", ca_key_file, "-CAcreateserial", "-out", device_cert_file, "-days", "365", "-sha256"], check=True)

# Convert the device certificate to DER format
device_cert_file_der = f"deviceid_{device_id}_cert.der"
subprocess.run(["openssl", "x509", "-inform", "PEM", "-outform", "DER", "-in", device_cert_file, "-out", device_cert_file_der], check=True)

# Save the device ID to a JSON file
device_data = {"device_id": device_id}
with open(device_json_file, "w") as json_file:
    json.dump(device_data, json_file)

print("Device certificate and keys generated.")
print(f"Device ID saved to {device_json_file}")

collection.insert_one({"printer_id": device_id,
                        "user_id": None,
                        "printer_model": "HP Raspberry",
                        "printer_type": "Commercial",
                        "printer_image": "https://cdn11.bigcommerce.com/s-2fbyfnm8ev/images/stencil/1280x1280/products/1737/6232/PICO_W_HERO_TRANSPARENT__26247.1656080410.png?c=2"
                       })

print(f"Device record created")