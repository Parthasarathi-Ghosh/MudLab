; MudLab Inno Setup Installer Script
; Builds a self-contained Windows installer from the bundled data/ directory.
; Requirements: Inno Setup 6 (https://jrsoftware.org/isinfo.php)
; Build:  iscc mudlab.iss
; Output: dist\MudLab-0.0.5-Setup.exe

#define AppName      "MudLab"
#define AppVersion   "0.0.5"
#define AppPublisher "MudLab Contributors"
#define AppURL       "https://github.com/Parthasarathi-Ghosh/MudLab"
#define AppExeName   "mudlab.exe"
#define AppIconFile     "data\lib\python3.14\site-packages\mudlab\application\icons\mudlab.ico"
#define AppIconInstalled "lib\python3.14\site-packages\mudlab\application\icons\mudlab.ico"

[Setup]
AppId={{B3F7A2C1-4D9E-4F1B-8E6A-0C2D5A3B7E9F}
AppName={#AppName}
AppVersion={#AppVersion}
AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}/issues
AppUpdatesURL={#AppURL}/releases

; No admin rights required — installs per-user by default.
; Users with admin rights get the option to install system-wide.
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes

; Compiler output
OutputDir=dist
OutputBaseFilename=MudLab-{#AppVersion}-Setup
SetupIconFile={#AppIconFile}

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; UI
WizardStyle=modern
WizardSizePercent=120

; Windows 10+ only
MinVersion=10.0

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; \
    GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copy the entire bundled distribution (Python + GTK + MudLab) into the install dir.
; Excludes __pycache__ bytecode — Python regenerates it on first run.
Source: "data\*"; DestDir: "{app}"; \
    Flags: ignoreversion recursesubdirs createallsubdirs; \
    Excludes: "__pycache__,*.pyc"

[Icons]
; Start Menu
Name: "{group}\{#AppName}";                    Filename: "{app}\bin\{#AppExeName}"; \
    IconFilename: "{app}\{#AppIconInstalled}"
Name: "{group}\{cm:UninstallProgram,{#AppName}}"; Filename: "{uninstallexe}"

; Desktop (optional)
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\bin\{#AppExeName}"; \
    IconFilename: "{app}\{#AppIconInstalled}"; Tasks: desktopicon

[Run]
Filename: "{app}\bin\{#AppExeName}"; \
    Description: "{cm:LaunchProgram,{#AppName}}"; \
    Flags: nowait postinstall skipifsilent
