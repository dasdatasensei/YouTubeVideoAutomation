# YouTube Video Automation

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-green.svg)](https://ffmpeg.org/)
[![YouTube API](https://img.shields.io/badge/YouTube%20API-v3-red.svg)](https://developers.google.com/youtube/v3)
[![yt-dlp](https://img.shields.io/badge/yt--dlp-2025.2-blue.svg)](https://github.com/yt-dlp/yt-dlp)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)](https://streamlit.io)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.0%2B-orange.svg)](https://docs.pydantic.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🎥 Professional-grade automation for YouTube content creators. Process, enhance, and schedule your videos with ease.

## 🏗️ Architecture

![YouTube Video Automation Architecture](assets/youtube_video_automation_screenshot.png)

## ✨ Features

### Core Capabilities

- 🎬 Process both local videos and YouTube content
- 🔄 Add professional end screens automatically
- 📅 Schedule uploads with precise timing
- 📊 Batch process multiple videos
- 🖼️ Custom thumbnail processing
- 🏷️ Rich metadata management

### Creator Tools

- 📋 Batch upload via spreadsheet
- 🎮 Gaming-specific templates
- 📚 Tutorial series automation
- 🎙️ Podcast/Interview templates
- 📱 Vlog content management

### Technical Features

- 🔒 Secure OAuth2.0 authentication
- 🛠️ FFmpeg video processing
- 📝 Comprehensive logging
- ⚡ Efficient local processing
- 🔄 Automatic retry handling

## 🚀 Quick Start

### For Content Creators

👉 [See our Content Creator Guide](docs/content_creator_guide.md)

- Simple setup instructions
- Video upload guide
- Batch processing templates
- Best practices

### For Developers

👉 [See our Developer Guide](docs/developer_guide.md)

- Technical setup
- API documentation
- Contribution guidelines
- Architecture details

## 📖 Documentation

### User Guides

- [Getting Started](docs/getting_started.md)
- [Content Creator Guide](docs/content_creator_guide.md)
- [Batch Processing Guide](docs/batch_processing.md)
- [Best Practices](docs/best_practices.md)

### Technical Documentation

- [Developer Guide](docs/developer_guide.md)
- [Authentication Guide](docs/authentication.md)
- [API Reference](docs/api_reference.md)
- [Architecture Overview](docs/architecture.md)

### Templates & Examples

- [Gaming Channel Templates](docs/templates/gaming.md)
- [Tutorial Series Templates](docs/templates/tutorials.md)
- [Vlog Templates](docs/templates/vlogs.md)
- [Batch Processing Guide](docs/batch_processing.md)

## 🛠️ Installation

### Quick Install (Content Creators)

Download the latest release for your platform:

- [Windows Installer](https://github.com/dasdatasensei/YouTubeVideoAutomation/releases/latest/download/youtube-automation-windows.exe)
- [Mac Installer](https://github.com/dasdatasensei/YouTubeVideoAutomation/releases/latest/download/youtube-automation-mac.dmg)
- [Linux Package](https://github.com/dasdatasensei/YouTubeVideoAutomation/releases/latest/download/youtube-automation-linux.deb)

### Developer Installation

```bash
# Clone repository
git clone https://github.com/yourusername/youtube-automation.git
cd youtube-automation

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

## ⚙️ Configuration

1. Get YouTube API credentials:

   - Visit [Google Cloud Console](https://console.cloud.google.com)
   - Create a project & enable YouTube Data API
   - Download credentials

2. Run initial setup:

```bash
youtube-processor configure
```

## 📝 Usage Examples

### Single Video Upload

```bash
youtube-processor process-local video.mp4 \
    --title "My Awesome Video" \
    --description "Check out this content!" \
    --publish-time "2024-02-20T15:00:00"
```

### Batch Processing

```bash
youtube-processor batch-process schedule.csv
```

See [Usage Guide](docs/usage.md) for more examples.

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Install development dependencies
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- [FFmpeg](https://ffmpeg.org/) for video processing
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [All Contributors](docs/CONTRIBUTORS.md)

## 🆘 Support

- 📚 [Documentation](docs/)
- 💬 [Discussions](https://github.com/yourusername/youtube-automation/discussions)
- 🐛 [Issue Tracker](https://github.com/yourusername/youtube-automation/issues)
- 📧 [Contact Support](support@yourdomain.com)

---

[Website](https://yourdomain.com) • [Documentation](docs/) • [Release Notes](CHANGELOG.md) • [Support](support@yourdomain.com)
