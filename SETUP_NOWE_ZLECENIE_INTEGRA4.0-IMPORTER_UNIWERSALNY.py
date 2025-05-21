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
            # Extract to a temporary directory
            temp_dir = 'temp_extracted'
            z.extractall(temp_dir)
            extracted_folder = os.path.join(temp_dir, os.listdir(temp_dir)[0])
            # Move contents to the target folder
            for item in os.listdir(extracted_folder):
                shutil.move(os.path.join(extracted_folder, item), target_folder)
            # Remove the temporary directory
            shutil.rmtree(temp_dir)
        print(f"Files have been downloaded from {repo_url} and moved to {target_folder}.")
    else:
        print(f"Error during download: {response.status_code}")

# Taking the order number or using the name of the current folder
order_number = input("Enter the order number: ").strip()
folder_prefix = "INTEGRA_ZLOZENIE-"
order_folder_name = folder_prefix + order_number if order_number else folder_prefix + os.path.basename(os.getcwd())

# Create the order folder if it doesn't exist yet
os.makedirs(order_folder_name, exist_ok=True)

# URLs to the GitHub repository archives
integra_repo_url = "https://github.com/pkonieczny007/INTEGRA_ASSEMBLY/archive/refs/heads/main.zip"
importer_repo_url = "https://github.com/pkonieczny007/IMPORTER_UNIWERSALNY/archive/refs/heads/main.zip"

# Downloading and extracting INTEGRA_ASSEMBLY files directly to the IMPORTERY subfolder
importery_folder = os.path.join(order_folder_name, 'IMPORTERY')
os.makedirs(importery_folder, exist_ok=True)
download_and_extract(integra_repo_url, importery_folder)

# Downloading and extracting IMPORTER_UNIWERSALNY files directly to the order folder
download_and_extract(importer_repo_url, order_folder_name)

# Move the setup file to the 'setup' subfolder in the newly created order folder
setup_folder = os.path.join(order_folder_name, 'setup')
os.makedirs(setup_folder, exist_ok=True)
script_name = os.path.basename(__file__)  # Retrieve the name of the current script
shutil.move(script_name, os.path.join(setup_folder, script_name))
print(f"The file {script_name} has been moved to {os.path.join(setup_folder, script_name)}.")
