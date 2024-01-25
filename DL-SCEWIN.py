import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile
from distutils.spawn import find_executable

import requests

def download_file(url: str, destination: str) -> None:
    with requests.get(url, timeout=5) as response:
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code.
        with open(destination, "wb") as file:
            file.write(response.content)

def extract_zip(source: str, destination: str) -> None:
    with zipfile.ZipFile(source, "r") as file:
        file.extractall(destination)

def download_innoextract(output_path: str) -> None:
    response = requests.get("https://api.github.com/repos/dscharrer/innoextract/releases/latest", timeout=5)
    response.raise_for_status()
    data = response.json()

    for asset in data["assets"]:
        if asset["name"].endswith("windows.zip"):
            file_path = os.path.join(os.environ['TEMP'], asset["name"])
            download_file(asset["browser_download_url"], file_path)
            extract_zip(file_path, output_path)
            break
    else:
        raise FileNotFoundError("Innoextract Windows binary not found in the latest release assets.")

def get_msi_center_version(file_path: str) -> str:
    version_match = re.search(r"_([\d.]+)\.exe$", os.path.basename(file_path))
    if not version_match:
        raise ValueError("Failed to obtain MSI Center version from filename.")
    return version_match.group(1)

def innoextract(command: list) -> None:
    result = subprocess.run(command, capture_output=True)
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, command, output=result.stdout, stderr=result.stderr)

def main() -> int:
    if find_executable("innoextract") is None:
        download_innoextract("C:\\Windows")

    temp_dir = os.environ['TEMP']
    msi_center_zip = os.path.join(temp_dir, "MSI-Center.zip")
    extract_path = os.path.join(temp_dir, "MSI-Center")

    download_file("https://download.msi.com/uti_exe/gaming-gear/MSI-Center.zip", msi_center_zip)
    os.makedirs(extract_path, exist_ok=True)
    extract_zip(msi_center_zip, extract_path)

    msi_center_installers = glob.glob(os.path.join(extract_path, "MSI Center_*.exe"))
    if not msi_center_installers:
        raise FileNotFoundError("MSI Center executable installer not found.")

    msi_center_version = get_msi_center_version(msi_center_installers[0])
    innoextract(["innoextract", msi_center_installers[0], "--output-dir", extract_path])

    appx_bundle = glob.glob(os.path.join(extract_path, "app", "*.appxbundle"))
    if not appx_bundle:
        raise FileNotFoundError("Appx bundle file not found.")

    appx_file_name = f"MSI Center_{msi_center_version}_x64.appx"
    extract_zip(appx_bundle[0], extract_path)

    msi_center_sdk_path = os.path.join(extract_path, "DCv2/Package/MSI Center SDK.exe")
    innoextract(["innoextract", msi_center_sdk_path, "--output-dir", extract_path])

    prepackage_path = os.path.join(extract_path, "tmp/PrePackage")
    engine_lib_installers = glob.glob(os.path.join(prepackage_path, "Engine Lib_*.exe"))
    if not engine_lib_installers:
        raise FileNotFoundError("Engine Lib installer not found.")

    innoextract(["innoextract", engine_lib_installers[0], "--output-dir", extract_path])

    scewin_path = os.path.join(extract_path, "app/Lib/SCEWIN")
    scewin_version_folders = glob.glob(os.path.join(scewin_path, "*"))
    if not scewin_version_folders:
        raise FileNotFoundError("SCEWIN version folder not found.")

    # Clean up residual files
    for file_name in ("BIOSData.db", "BIOSData.txt", "SCEWIN.bat"):
        file_path = os.path.join(scewin_version_folders[0], file_name)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            pass

    # Copy scripts
    for script_name in ("Import.bat", "Export.bat"):
        shutil.copy2(script_name, scewin_version_folders[0])

    shutil.move(scewin_path, ".")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except
