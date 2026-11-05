; LotusSubs Windows installer (Inno Setup 6). Build it with ..\build_installer.bat,
; which passes the version from version.py as /DAppVersion=...

#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#define AppName "LotusSubs"
#define AppExe "LotusSubs.exe"
#define Publisher "Lotus Technologies"

[Setup]
; Keep this AppId forever: it is how Windows recognises upgrades of the same app.
AppId={{8F3C2A6E-5B1D-4E7A-9C2F-3D6B8A1E4F70}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#Publisher}
AppCopyright=Copyright (C) 2026 Vidath Dulanjith, {#Publisher}. All rights reserved.
VersionInfoVersion={#AppVersion}
VersionInfoCompany={#Publisher}
VersionInfoDescription={#AppName} Setup
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
; Installs for the current user without admin rights; an admin can choose "all users".
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; The app is 64-bit Python 3.14, which needs Windows 10 or 11.
MinVersion=10.0
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
LicenseFile=..\LICENSE.txt
SetupIconFile=..\assets\logo.ico
UninstallDisplayIcon={app}\{#AppExe}
UninstallDisplayName={#AppName}
WizardStyle=modern
Compression=lzma2/max
SolidCompression=yes
CloseApplications=yes
OutputDir=Output
OutputBaseFilename={#AppName}-Setup-{#AppVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
; The whole PyInstaller folder: LotusSubs.exe must stay next to _internal and bin.
Source: "..\dist\LotusSubs\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExe}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#AppExe}"; Description: "{cm:LaunchProgram,{#AppName}}"; Flags: nowait postinstall skipifsilent
