"""LotusSubs product details: the single place to bump the version.

main.py shows these in the About box; build.bat runs this file to write
version_info.txt, which PyInstaller embeds as the .exe's Windows "Details" tab.
"""
APP_NAME = "LotusSubs"
APP_VERSION = "1.0.0"
DESCRIPTION = "LotusSubs - AI subtitles on the Hiru SUB TAG bed"
AUTHOR = "Vidath Dulanjith"
COMPANY = "Lotus Technologies"
COPYRIGHT = f"Copyright © 2026 {AUTHOR}, {COMPANY}. All rights reserved."


def write_version_file(path: str = "version_info.txt") -> None:
    nums = tuple(int(n) for n in APP_VERSION.split(".")) + (0,) * (4 - len(APP_VERSION.split(".")))
    strings = {
        "CompanyName": COMPANY,
        "FileDescription": DESCRIPTION,
        "FileVersion": APP_VERSION,
        "InternalName": APP_NAME,
        "LegalCopyright": COPYRIGHT,
        "OriginalFilename": f"{APP_NAME}.exe",
        "ProductName": APP_NAME,
        "ProductVersion": APP_VERSION,
        "Comments": f"Author: {AUTHOR}",
    }
    entries = ",\n".join(f"        StringStruct({k!r}, {v!r})" for k, v in strings.items())
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"""VSVersionInfo(
  ffi=FixedFileInfo(filevers={nums}, prodvers={nums}, mask=0x3f, flags=0x0,
                    OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)),
  kids=[
    StringFileInfo([StringTable('040904B0', [
{entries}
    ])]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
""")


if __name__ == "__main__":
    write_version_file()
