import os
import shutil
from zipfile import ZipFile

if __name__ == "__main__":
    download_dir = "./downloads"
    # for path in os.listdir(download_dir):
    #     if path.endswith(".zip"):
    #         print(path)
    #         zip_file = os.path.join(download_dir, path)
    #         with ZipFile(zip_file, 'r') as zip_ref:
    #             zip_ref.extractall(download_dir)

    for filename in os.listdir(download_dir):
        file_path = os.path.join(download_dir, filename)

        if os.path.isdir(file_path):
            continue

        file_extension = os.path.splitext(filename)[1]
        if not file_extension:
            continue

        extension_dir = os.path.join(download_dir, file_extension[1:].lower())

        if not os.path.exists(extension_dir):
            os.makedirs(extension_dir)

        try:
            shutil.move(file_path, os.path.join(extension_dir, filename))
            print(f"Moved {filename} to {extension_dir}")
        except Exception as e:
            print(f"Error moving {filename}: {str(e)}")
