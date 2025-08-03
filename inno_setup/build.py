import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_dir():
    """Clean up build and dist directories"""
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        # Ensure PyInstaller is installed
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        
        # Build the executable
        subprocess.run([
            sys.executable, 
            '-m', 
            'PyInstaller',
            '--noconfirm',
            '--clean',
            'stock_sentiment.spec'
        ], check=True)
        
        print("Successfully built executable")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False

def copy_additional_files():
    """Copy additional required files to the dist directory"""
    dist_dir = Path('dist/BullBearRadar')
    
    # Create scripts directory in dist
    scripts_dir = dist_dir / 'scripts'
    scripts_dir.mkdir(exist_ok=True)
    
    # Copy scripts
    shutil.copy2('scripts/install_dependencies.ps1', scripts_dir)
    shutil.copy2('scripts/download_nltk.py', scripts_dir)
    
    # Copy .env.template
    shutil.copy2('../.env.template', dist_dir / '.env.template')
    
    print("Successfully copied additional files")

def main():
    # Clean previous builds
    clean_build_dir()
    
    # Build executable
    if not build_executable():
        sys.exit(1)
    
    # Copy additional files
    try:
        copy_additional_files()
    except Exception as e:
        print(f"Error copying additional files: {e}")
        sys.exit(1)
    
    print("Build completed successfully!")

if __name__ == "__main__":
    main()