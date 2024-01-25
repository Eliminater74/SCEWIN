# SCEWIN / AMISCE 🛠️

![SCEWIN Logo](https://github.com/Eliminater74/SCEWIN/blob/main/media/SCEWIN.png?raw=true)

**SCEWIN** is a powerful tool for modifying BIOS NVRAM variables, including those not visible through UEFI. Originally bundled with MSI Center, this repository provides SCEWIN binaries standalone, eliminating the need for MSI's additional software.

---

## ⚠️ Disclaimer

This project is **not** affiliated with [American Megatrends (AMI)](https://www.ami.com). Improper use of SCEWIN could lead to system instability. Proceed with caution and at your own risk.

---

## 🚀 Usage

1. **Export NVRAM Settings**: Run `Export.bat` to export NVRAM settings to `nvram.txt`.
2. **Edit Settings**: Modify `nvram.txt` as needed.
3. **Import NVRAM Settings**: Run `Import.bat` to write changes back to NVRAM.

---

## 🛠 Troubleshooting

Errors during usage? Consult `log-file.txt` generated during `Export.bat` or `Import.bat` execution. Error types:

- [Both](#both)
- [Export](#export)
- [Import](#import)

### Both

#### LoadDeviceDriver Errors
- **Causes**: Missing drivers (`amifldrv64.sys`, `amigendrv64.sys`) or lack of admin privileges.
- **Fixes**: Ensure drivers are present and CMD is run with admin rights.

#### ERROR:57
- **Causes**: Incorrect command or missing NVRAM script file.
- **Fixes**: Verify command correctness and script file existence.

### Export

#### WARNING: HII Data Issues
- **For ASUS Motherboards**: Check [ASUS section](#asus).
- **Others**: Solution under development.

#### ERROR:4 / ERROR:82
- **Causes**: BIOS incompatibility or outdated `SmiVariable`.
- **Fixes**: Use [UEFITool](https://github.com/LongSoft/UEFITool) to verify or update the `SmiVariable`.

#### Platform Identification Failure
- **Cause**: Outdated Aptio core version.
- **Fix**: Use `/d` option to override.

### Import

#### Error Writing to NVRAM
- **Causes**: Write-protected variables or disabled `PCI Device`.
- **Fixes**: Enable `PCI Device` in Device Manager, follow motherboard-specific instructions.

#### System Configuration Unchanged
- **Causes**: Unmodified import script or failed changes application.
- **Fixes**: Review and modify the script correctly.

#### Warning in Line
- **Cause**: Line-specific errors in the script.
- **Fixes**: Comment out or manually correct the erroneous line.

---

### Specific Motherboard Solutions

#### ASUS
- **Steps**: Enable `Publish HII Resources` in BIOS.
- **For Z790+, B760+**: Disable `Password protection of Runtime Variables`.

#### ASRock
- **Steps**: Disable `Password protection of Runtime Variables` using [UEFI Editor](https://boringboredom.github.io/UEFI-Editor) for menu access.

---

## 📝 Reporting Issues

Encounter additional problems or have solutions not working? Please report them in the [issue tracker](https://github.com/amitxv/SCEWIN/issues). Before creating a new issue, check if it's already reported or discussed.

---
