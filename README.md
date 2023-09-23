# SCEWIN

SCEWIN is a tool to modify BIOS NVRAM including options that are not visible through UEFI. As far as I know, it is exclusively shipped with MSI Center. This repository was created to provide the SCEWIN binaries without installing the MSI bloatware so that you don't have to.

## Usage

1. Run the ``Export.bat`` script to export NVRAM data to ``BIOSSettings.txt``

2. Depending on the type of variable, move the ``*`` to the desired option or change the value

3. Run the ``Import.bat`` script to write the configuration in ``BIOSSettings.txt`` to NVRAM
