import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile
from distutils.spawn import find_executable

import requests


def download_innoextract(output_path: str) -> None:
    response = requests.get("https://api.github.com/repos/dscharrer/innoextract/releases/latest")
    data = response.json()

    for asset in data["assets"]:
        file_name = asset["name"]
        if file_name.endswith("windows.zip"):
            response = requests.get(asset["browser_download_url"])
            file_path = f"{os.environ['TEMP']}\\{file_name}"

            with open(file_path, "wb") as file:
                file.write(response.content)

            with zipfile.ZipFile(file_path, "r") as file:
                file.extract("innoextract.exe", output_path)


def main() -> int:
    if find_executable("innoextract") is None:
        download_innoextract("C:\\Windows")

    MSI_CENTER_ZIP = f"{os.environ['TEMP']}\\MSI-Center.zip"
    EXTRACT_PATH = f"{os.environ['TEMP']}\\MSI-Center"

    response = requests.get("https://download.msi.com/uti_exe/gaming-gear/MSI-Center.zip")

    # Download MSI Center
    with open(MSI_CENTER_ZIP, "wb") as file:
        file.write(response.content)

    os.makedirs(EXTRACT_PATH, exist_ok=True)

    with zipfile.ZipFile(MSI_CENTER_ZIP, "r") as file:
        file.extractall(EXTRACT_PATH)

    MSI_CENTER_INSTALLER = glob.glob(f"{EXTRACT_PATH}\\MSI Center_*.exe")

    if not MSI_CENTER_INSTALLER:
        print("error: MSI Center executable installer not found")
        return 1

    # get version from file name
    MATCH = re.search(r"_([\d.]+)\.exe$", os.path.basename(MSI_CENTER_INSTALLER[0]))

    if not MATCH:
        print("error: Failed to obtain MSI Center version")
        return 1

    MSI_CENTER_VERSION = MATCH.group(1)

    subprocess.call(["innoextract", MSI_CENTER_INSTALLER[0], "--output-dir", EXTRACT_PATH])

    APPXBUNDLE = glob.glob(f"{EXTRACT_PATH}\\app\\*.appxbundle")

    if not APPXBUNDLE:
        print("error: Appx bundle file not found")
        return 1

    APPX_FILE_NAME = f"MSI%20Center_{MSI_CENTER_VERSION}_x64.appx"

    with zipfile.ZipFile(APPXBUNDLE[0], "r") as file:
        file.extract(APPX_FILE_NAME, EXTRACT_PATH)

    MSI_CENTER_SDK_PATH = "DCv2/Package/MSI%20Center%20SDK.exe"

    with zipfile.ZipFile(f"{EXTRACT_PATH}\\{APPX_FILE_NAME}", "r") as file:
        file.extract(MSI_CENTER_SDK_PATH, EXTRACT_PATH)

    subprocess.call(["innoextract", f"{EXTRACT_PATH}\\{MSI_CENTER_SDK_PATH}", "--output-dir", EXTRACT_PATH])

    PREPACKAGE_PATH = f"{EXTRACT_PATH}\\tmp\\PrePackage"

    ENGINE_LIB_INSTALLER = glob.glob(f"{PREPACKAGE_PATH}\\Engine Lib_*.exe")

    if not ENGINE_LIB_INSTALLER:
        print("error: Engine Lib installer not found")
        return 1

    subprocess.call(["innoextract", ENGINE_LIB_INSTALLER[0], "--output-dir", EXTRACT_PATH])

    SCEWIN_PATH = f"{EXTRACT_PATH}\\app\\Lib\\SCEWIN"

    SCEWIN_VERSION_FOLDER = glob.glob(f"{SCEWIN_PATH}\\*\\")

    if not SCEWIN_VERSION_FOLDER:
        print("error: SCEWIN version folder not found")
        return 1

    # remove residual files
    for file in ("BIOSData.db", "BIOSData.txt", "SCEWIN.bat"):
        try:
            os.remove(f"{SCEWIN_VERSION_FOLDER[0]}\\{file}")
        except FileNotFoundError:
            pass

    for script in ("Import.bat", "Export.bat"):
        shutil.copy2(f"{script}", SCEWIN_VERSION_FOLDER[0])

    shutil.move(SCEWIN_PATH, ".")

    return 0


if __name__ == "__main__":
    sys.exit(main())
