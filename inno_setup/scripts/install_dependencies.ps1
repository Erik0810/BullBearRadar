# Parameters
param(
    [switch]$OfflineMode = $false
)

# Function to install Python if not present
function Install-Python {
    if ($OfflineMode) {
        Write-Host "Offline mode: Skipping Python installation. Please install Python 3.7+ manually if needed."
        return $false
    }
    
    Write-Host "Python not found. Installing Python..."
    
    # Download Python 3.9 installer
    $pythonUrl = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        # Install Python with required options
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
        
        # Clean up
        Remove-Item $installerPath
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        
        Write-Host "Python installed successfully"
        return $true
    }
    catch {
        Write-Host "Failed to install Python: $_"
        return $false
    }
}

# Check if Python is installed
$pythonCommand = "python"
$pythonInstalled = $false

try {
    $pythonVersion = & $pythonCommand --version
    Write-Host "Found Python: $pythonVersion"
    $pythonInstalled = $true
}
catch {
    $pythonInstalled = Install-Python
    if (-not $pythonInstalled) {
        Write-Host "Failed to install Python. Please install Python 3.7 or higher manually."
        exit 1
    }
}

# Ensure pip is up to date
Write-Host "Updating pip..."
& $pythonCommand -m pip install --upgrade pip

# Install required packages
Write-Host "Installing required Python packages..."
& $pythonCommand -m pip install --no-cache-dir praw>=7.0.0 yfinance>=0.1.63 vaderSentiment>=3.3.2 pandas>=1.2.0 nltk>=3.6.0 python-dotenv>=0.19.0 matplotlib>=3.4.0

# Run NLTK data download script
Write-Host "Downloading NLTK data..."
& $pythonCommand "scripts\download_nltk.py"

Write-Host "Dependencies installation completed successfully!"