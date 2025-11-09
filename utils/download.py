import os
import requests
import zipfile
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}

# Request the ZIP file
response = requests.get(API_URL, headers=headers)

if response.status_code == 200:
    # Read response into memory buffer
    zip_file = zipfile.ZipFile(BytesIO(response.content))

    # Extract to target folder
    extract_folder = "data"
    os.makedirs(extract_folder, exist_ok=True)

    zip_file.extractall(extract_folder)

    print(f"Data extracted directly to ./{extract_folder}")
else:
    print(f"Error {response.status_code}: {response.text}")
