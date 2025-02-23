# Installation Guide

## Table of Contents

- [Quick Install](#quick-install)
- [Windows Installation](#windows-installation)
- [macOS Installation](#macos-installation)
- [Linux Installation](#linux-installation)
- [Advanced Installation](#advanced-installation)
- [Troubleshooting](#troubleshooting)

## Quick Install

### For Content Creators

Download our installer:

- [Windows Installer](https://github.com/dasdatasensei/YouTubeVideoAutomation/releases/latest/download/youtube-automation-windows.exe)
- [macOS Installer](https://github.com/dasdatasensei/YouTubeVideoAutomation/releases/latest/download/youtube-automation-mac.dmg)
- [Linux Package](https://github.com/dasdatasensei/YouTubeVideoAutomation/releases/latest/download/youtube-automation-linux.deb)

### For Developers

```bash
git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
cd YouTubeVideoAutomation
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate
pip install -e ".[dev]"
```

## Windows Installation

### Method 1: Using Installer (Recommended)

1. Download [Windows Installer](downloads/windows-installer.exe)
2. Double-click the installer
3. Follow the installation wizard
4. Launch "YouTube Video Automation" from Start Menu

### Method 2: Manual Installation

1. **Install Python**

   - Download [Python 3.9+](https://python.org/downloads)
   - Check "Add Python to PATH" during installation

   ```bash
   # Verify installation
   python --version
   ```

2. **Install FFmpeg**

   - Download [FFmpeg](https://ffmpeg.org/download.html)
   - Extract to C:\ffmpeg
   - Add to Path:
     - Right-click Computer → Properties
     - Advanced system settings
     - Environment Variables
     - Add C:\ffmpeg\bin to Path

3. **Install Application**
   ```bash
   # Open Command Prompt as Administrator
   cd %USERPROFILE%\Documents
   git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
   cd YouTubeVideoAutomation
   python -m venv .venv
   .venv\Scripts\activate
   pip install -e ".[dev]"
   ```

## macOS Installation

### Method 1: Using Installer (Recommended)

1. Download [macOS Installer](downloads/macos-installer.dmg)
2. Double-click the .dmg file
3. Drag application to Applications folder
4. Launch from Applications

### Method 2: Using Homebrew

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python ffmpeg git

# Install application
git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
cd YouTubeVideoAutomation
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Method 3: Manual Installation

1. **Install Python**

   - Download [Python 3.9+](https://python.org/downloads)

   ```bash
   # Verify installation
   python3 --version
   ```

2. **Install FFmpeg**

   ```bash
   # Using Homebrew
   brew install ffmpeg

   # Or download binary
   # Download from https://ffmpeg.org/download.html
   # Extract and add to PATH
   ```

3. **Install Application**
   ```bash
   git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
   cd YouTubeVideoAutomation
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -e ".[dev]"
   ```

## Linux Installation

### Ubuntu/Debian

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv ffmpeg git

# Install application
git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
cd YouTubeVideoAutomation
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Fedora/RHEL

```bash
# Install dependencies
sudo dnf install python3-pip python3-virtualenv ffmpeg git

# Install application
git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
cd YouTubeVideoAutomation
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip python-virtualenv ffmpeg git

# Install application
git clone https://github.com/dasdatasensei/YouTubeVideoAutomation.git
cd YouTubeVideoAutomation
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Advanced Installation

### Docker Installation

```dockerfile
# Dockerfile
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install application
COPY . /app
WORKDIR /app
RUN pip install -e ".[dev]"

# Run application
CMD ["youtube-processor"]
```

```bash
# Build and run
docker build -t youtube-automation .
docker run -it youtube-automation
```

### Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Set up environment variables
cp .env.example .env
# Edit .env with your settings
```

## Verifying Installation

1. **Check Command Availability**

```bash
youtube-processor --version
```

2. **Test FFmpeg**

```bash
youtube-processor test-ffmpeg
```

3. **Verify Authentication**

```bash
youtube-processor verify-auth
```

## Directory Structure

```
~/.youtube-automation/
├── config/
│   ├── client_secrets.json
│   └── token.json
├── work/
├── downloads/
└── logs/
```

## Troubleshooting

### Common Issues

1. **Python Not Found**

```bash
# Windows
python --version
# macOS/Linux
python3 --version
```

- Ensure Python is in PATH
- Try reinstalling Python

2. **FFmpeg Missing**

```bash
ffmpeg -version
```

- Check PATH settings
- Reinstall FFmpeg

3. **Installation Fails**

```bash
# Clear pip cache
pip cache purge
# Reinstall with verbose output
pip install -v -e ".[dev]"
```

### Permission Issues

```bash
# Linux/macOS
sudo chown -R $USER:$USER ~/.youtube-automation

# Windows (Administrative PowerShell)
takeown /f %USERPROFILE%\.youtube-automation /r
```

### Environment Issues

```bash
# Check Python environment
python -c "import sys; print(sys.executable)"

# Check dependencies
pip freeze

# Verify FFmpeg path
which ffmpeg  # Linux/macOS
where ffmpeg  # Windows
```

## Uninstallation

### Windows

```bash
# Using installer
Control Panel → Programs → Uninstall

# Manual
pip uninstall youtube-automation
rmdir /s %USERPROFILE%\.youtube-automation
```

### macOS/Linux

```bash
# Using package manager
brew uninstall youtube-automation  # macOS

# Manual
pip uninstall youtube-automation
rm -rf ~/.youtube-automation
```

## Additional Resources

- [Developer Guide](https://github.com/dasdatasensei/YouTubeVideoAutomation/blob/main/docs/developer_guide.md)
- [Configuration Guide](https://github.com/dasdatasensei/YouTubeVideoAutomation/blob/main/docs/configuration.md)
- [Troubleshooting Guide](https://github.com/dasdatasensei/YouTubeVideoAutomation/blob/main/docs/troubleshooting.md)
- [FAQ](https://github.com/dasdatasensei/YouTubeVideoAutomation/blob/main/docs/faq.md)

---

Need help? Join our [Discord Community](https://discord.gg/thedatasensei) or open an [Issue](https://github.com/dasdatasensei/YouTubeVideoAutomation/issues).
