# Stock Sentiment Analyzer Installer

This directory contains the necessary files to create a Windows installer for the Stock Sentiment Analyzer application.

## Installation Package Features

The generated installer (`StockSentimentSetup.exe`) is a standalone package that can be shared and run on any Windows computer. It includes:

- Automatic Python installation if not present
- Installation of all required Python packages
- NLTK data download
- Environment configuration setup
- Desktop and Start Menu shortcuts

## For End Users

1. Download `StockSentimentSetup.exe`
2. Run the installer (requires administrator privileges)
3. Follow the installation wizard
4. Enter your Reddit API credentials when prompted
   - You can get these from https://www.reddit.com/prefs/apps
5. Launch the application from the desktop shortcut or Start Menu

### System Requirements

- Windows 7 SP1 or later
- Internet connection (for initial setup)
- 500MB free disk space
- Administrator privileges (for installation only)

## For Developers

### Prerequisites

1. Install Python 3.7 or higher
2. Install Inno Setup from https://jrsoftware.org/isinfo.php
3. Install PyInstaller: `pip install pyinstaller`

### Building the Installer

1. Open a command prompt in this directory
2. Run the build script:
   ```bash
   python build.py
   ```
   This will:
   - Clean previous builds
   - Package the application using PyInstaller
   - Copy necessary files to the dist directory

3. Open Inno Setup Compiler
4. Open `installer.iss`
5. Click "Compile" to create the installer
6. The installer will be created as `output/StockSentimentSetup.exe`

### Directory Structure

```
inno_setup/
├── assets/            # Icons and images
│   └── app.ico       # Application icon
├── scripts/          # Installation scripts
│   ├── install_dependencies.ps1
│   └── download_nltk.py
├── build.py          # Build automation script
├── installer.iss     # Main Inno Setup script
├── env_dialog.iss    # Environment configuration dialog
└── stock_sentiment.spec  # PyInstaller configuration
```

### Distribution

The generated `StockSentimentSetup.exe` is a standalone installer that can be distributed to end users. It contains:

1. The packaged application
2. All necessary scripts for:
   - Python installation
   - Package dependencies
   - NLTK data
   - Environment setup

Users don't need to manually install Python or any dependencies - the installer handles everything automatically.

## Troubleshooting

### For End Users

If you encounter issues during installation:
1. Ensure you have administrator privileges
2. Check your internet connection
3. Temporarily disable antivirus software
4. Run the installer with `/LOG="install.log"` for detailed logs

### For Developers

Common build issues:
1. PyInstaller errors:
   - Ensure all dependencies are installed
   - Check the PyInstaller spec file configuration
2. Inno Setup errors:
   - Verify file paths in installer.iss
   - Check for required administrator privileges

## Support

For issues or questions:
1. Check the application's main README
2. Submit an issue on the project repository
3. Contact the development team
