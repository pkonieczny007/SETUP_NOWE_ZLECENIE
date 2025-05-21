import requests
import zipfile
import io
import os
import shutil

# Function to download and extract a repository
def download_and_extract(repo_url, target_folder):
    response = requests.get(repo_url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            temp_dir = 'temp_extracted'
            z.extractall(temp_dir)
            extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            os.makedirs(target_folder, exist_ok=True)
            for item in os.listdir(extracted_folder):
                shutil.move(os.path.join(extracted_folder, item), target_folder)
            shutil.rmtree(temp_dir)
        print(f"Files have been downloaded from {repo_url} and moved to {target_folder}.")
    else:
        print(f"Error during download: {response.status_code}")

# Get order number or fallback to current folder name
order_number = input("Enter the order number: ").strip()
folder_prefix = "INTEGRA_ZLOZENIE-"
order_folder_name = folder_prefix + order_number if order_number else folder_prefix + os.path.basename(os.getcwd())

# Create main order folder
os.makedirs(order_folder_name, exist_ok=True)

# Define GitHub URLs
urls_and_folders = {
    "https://github.com/pkonieczny007/INTEGRA_ASSEMBLY/archive/refs/heads/main.zip": 'IMPORTERY',
    "https://github.com/pkonieczny007/INTEGRA_BM/archive/refs/heads/main.zip": 'BM_IMPORTERY',
    "https://github.com/pkonieczny007/MARSZRUTA/archive/refs/heads/main.zip": 'MARSZRUTA',
    "https://github.com/pkonieczny007/IMPORTER_UNIWERSALNY/archive/refs/heads/main.zip": '',  # goes to root
}

# Download and extract each repository
for url, subfolder in urls_and_folders.items():
    target_path = os.path.join(order_folder_name, subfolder) if subfolder else order_folder_name
    os.makedirs(target_path, exist_ok=True)
    download_and_extract(url, target_path)

# Move this script to setup folder
setup_folder = os.path.join(order_folder_name, 'setup')
os.makedirs(setup_folder, exist_ok=True)
script_name = os.path.basename(__file__)
shutil.move(script_name, os.path.join(setup_folder, script_name))
print(f"The file {script_name} has been moved to {os.path.join(setup_folder, script_name)}.")
