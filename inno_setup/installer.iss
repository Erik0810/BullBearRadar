#define MyAppName "BullBearRadar"
#define MyAppVersion "1.0"
#define MyAppPublisher "Erik Overby"
#define MyAppExeName "BullBearRadar.exe"

[Setup]
AppId={{5A6B7C8D-9E0F-4A1B-8C2D-3E4F5A6B7C8D}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=output
OutputBaseFilename=BullBearRadar
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
PrivilegesRequired=admin
DisableProgramGroupPage=auto

; Minimum Windows version (Windows 7 or later)
MinVersion=6.1sp1

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main application files
Source: "dist\StockSentiment\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs
Source: "..\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Check and install prerequisites (with fallback)
Filename: "powershell.exe"; \
    Parameters: "-ExecutionPolicy Bypass -Command ""$Host.UI.RawUI.WindowTitle = 'Installing Prerequisites'; & '{app}\scripts\install_dependencies.ps1' -OfflineMode"""; \
    WorkingDir: "{app}"; \
    Flags: runhidden; \
    StatusMsg: "Installing prerequisites (this may take several minutes)..."

; Run the application after installation
Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
    Flags: nowait postinstall skipifsilent; \
    Check: ShouldRunApp

#include "env_dialog.iss"

[Code]
var
  PrerequisitesInstalled: Boolean;

function CheckInternetConnection: Boolean;
var
  ResultCode: Integer;
  Cmd: String;
begin
  Result := False;
  Cmd := 'powershell.exe -NoProfile -Command "(Test-NetConnection -ComputerName python.org -Port 80).TcpTestSucceeded"';
  if Exec(Cmd, '', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    Result := (ResultCode = 0);
end;
  
procedure InitializeWizard;
begin
  PrerequisitesInstalled := False;
  InitializeEnvWizard;
end;

function ValidatePrerequisites: Boolean;
var
  ErrorCode: Integer;
begin
  Result := True;
  
  // Skip internet check - we'll handle dependencies offline
  // Check for PowerShell
  if not FileExists(ExpandConstant('{sys}\WindowsPowerShell\v1.0\powershell.exe')) then
  begin
    MsgBox('PowerShell is required but not found. Please install Windows PowerShell 3.0 or later.',
           mbError, MB_OK);
    Result := False;
    Exit;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then
  begin
    PrerequisitesInstalled := True;
  end
  else if CurStep = ssPostInstall then
  begin
    if not UpdateEnvFile() then
    begin
      MsgBox('Failed to create environment configuration file. ' + 
             'Please check the application documentation for manual configuration.', 
             mbError, MB_OK);
    end;
  end;
end;

function ShouldRunApp: Boolean;
begin
  Result := PrerequisitesInstalled;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  NeedsRestart := False;
  
  if not ValidatePrerequisites then
    Result := 'Prerequisites check failed. Installation cannot continue.';
end;