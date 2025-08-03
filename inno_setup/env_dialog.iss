[Code]
var
  EnvPage: TInputQueryWizardPage;
  
procedure InitializeEnvWizard;
begin
  EnvPage := CreateInputQueryPage(wpSelectDir,
    'Reddit API Configuration', 
    'Please enter your Reddit API credentials',
    'These credentials are required for accessing Reddit data. You can obtain them from https://www.reddit.com/prefs/apps');
    
  EnvPage.Add('Reddit Client ID:', False);
  EnvPage.Add('Reddit Client Secret:', False);
  EnvPage.Add('Reddit User Agent:', False);
  
  // Set default user agent
  EnvPage.Values[2] := 'StockSentiment/1.0';
end;

function UpdateEnvFile(): Boolean;
var
  EnvContent: TStringList;
  EnvPath: String;
begin
  Result := True;
  try
    EnvContent := TStringList.Create;
    try
      EnvContent.Add('# Reddit API Credentials');
      EnvContent.Add('REDDIT_CLIENT_ID=' + EnvPage.Values[0]);
      EnvContent.Add('REDDIT_CLIENT_SECRET=' + EnvPage.Values[1]);
      EnvContent.Add('REDDIT_USER_AGENT=' + EnvPage.Values[2]);
      
      EnvPath := ExpandConstant('{app}\.env');
      EnvContent.SaveToFile(EnvPath);
    finally
      EnvContent.Free;
    end;
  except
    Result := False;
  end;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = EnvPage.ID then
  begin
    if EnvPage.Values[0] = '' then
    begin
      MsgBox('Please enter your Reddit Client ID', mbError, MB_OK);
      Result := False;
      Exit;
    end;
    
    if EnvPage.Values[1] = '' then
    begin
      MsgBox('Please enter your Reddit Client Secret', mbError, MB_OK);
      Result := False;
      Exit;
    end;
    
    if EnvPage.Values[2] = '' then
    begin
      MsgBox('Please enter a Reddit User Agent', mbError, MB_OK);
      Result := False;
      Exit;
    end;
  end;
end;