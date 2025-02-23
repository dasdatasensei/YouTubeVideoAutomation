# Troubleshooting Guide

## Table of Contents

- [Quick Solutions](#quick-solutions)
- [Installation Issues](#installation-issues)
- [Authentication Problems](#authentication-problems)
- [Video Processing Issues](#video-processing-issues)
- [Upload Problems](#upload-problems)
- [Batch Processing Errors](#batch-processing-errors)
- [Common Error Messages](#common-error-messages)
- [Advanced Debugging](#advanced-debugging)

## Quick Solutions

### Top 5 Common Issues

1. **OAuth Error**

   ```
   Error: Token expired or invalid
   ```

   - Delete `config/token.json`
   - Run `youtube-processor configure`
   - Re-authenticate

2. **FFmpeg Not Found**

   ```
   Error: [Errno 2] No such file or directory: 'ffmpeg'
   ```

   - Check FFmpeg installation
   - Verify PATH settings
   - Reinstall FFmpeg if needed

3. **Upload Failed**

   ```
   Error: Failed to upload video
   ```

   - Check internet connection
   - Verify file permissions
   - Ensure sufficient quota

4. **CSV Format Error**

   ```
   Error: CSV validation failed
   ```

   - Check column names
   - Verify date formats
   - Remove special characters

5. **Processing Error**
   ```
   Error: Video processing failed
   ```
   - Check disk space
   - Verify video format
   - Check FFmpeg compatibility

## Installation Issues

### Python Environment Problems

1. **Python Not Found**

   ```bash
   # Check Python version
   python --version
   python3 --version
   ```

   Solution:

   - Reinstall Python
   - Add to PATH
   - Use correct command for OS

2. **Virtual Environment Issues**

   ```bash
   # Create new environment
   python -m venv .venv --clear
   # Activate environment
   source .venv/bin/activate  # Linux/macOS
   .\.venv\Scripts\activate   # Windows
   ```

3. **Dependency Conflicts**
   ```bash
   # Clear environment
   pip freeze > requirements.txt
   pip uninstall -r requirements.txt -y
   # Reinstall
   pip install -e ".[dev]"
   ```

## Authentication Problems

### OAuth2.0 Issues

1. **Invalid Client Secrets**

   ```
   Error: The OAuth client was not found
   ```

   Solution:

   - Download new credentials
   - Place in correct location
   - Verify file permissions

2. **Token Refresh Failed**

   ```python
   # Check token status
   youtube-processor token-info
   # Reset authentication
   youtube-processor reset-auth
   ```

3. **Scope Issues**
   ```
   Error: Insufficient Permission
   ```
   Solution:
   - Check required scopes
   - Re-authenticate with correct scopes
   - Update OAuth consent screen

### Code Examples

```python
# Manual token refresh
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

credentials = Credentials.from_authorized_user_file('token.json')
if credentials.expired:
    credentials.refresh(Request())
```

## Video Processing Issues

### FFmpeg Problems

1. **Format Compatibility**

   ```bash
   # Check video format
   ffmpeg -i video.mp4
   ```

   Solution:

   - Convert to compatible format
   - Update FFmpeg
   - Check codec support

2. **Processing Failed**

   ```python
   # Enable debug logging
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Resource Issues**
   - Check disk space
   - Monitor memory usage
   - Verify file permissions

### Debugging Steps

```bash
# Test FFmpeg installation
ffmpeg -version

# Check video info
ffprobe video.mp4

# Test processing
ffmpeg -i input.mp4 -t 10 test_output.mp4
```

## Upload Problems

### Network Issues

1. **Connection Timeout**

   ```python
   # Implement retry logic
   from tenacity import retry, stop_after_attempt

   @retry(stop=stop_after_attempt(3))
   def upload_with_retry():
       # Upload code
   ```

2. **Quota Exceeded**

   - Check quota usage
   - Implement rate limiting
   - Request quota increase

3. **Large File Issues**
   - Use chunked upload
   - Verify file size limits
   - Check network stability

### API Errors

```python
# Handle API errors
try:
    upload_video()
except HttpError as e:
    if e.resp.status == 403:
        # Handle quota
    elif e.resp.status == 500:
        # Handle server error
```

## Batch Processing Errors

### CSV Issues

1. **Invalid Format**

   ```python
   # Validate CSV
   import pandas as pd

   def validate_csv(file_path):
       df = pd.read_csv(file_path)
       # Validation logic
   ```

2. **Path Problems**

   - Use absolute paths
   - Check file existence
   - Verify permissions

3. **Scheduling Conflicts**
   - Check time formats
   - Verify timezone settings
   - Space out uploads

### Error Handling

```python
def process_batch(csv_file):
    errors = []
    for row in csv_file:
        try:
            process_video(row)
        except Exception as e:
            errors.append({
                'row': row,
                'error': str(e)
            })
    return errors
```

## Common Error Messages

### Error Code Reference

| Code     | Message           | Solution        |
| -------- | ----------------- | --------------- |
| AUTH001  | Token expired     | Refresh token   |
| PROC001  | Processing failed | Check FFmpeg    |
| UPLD001  | Upload failed     | Check network   |
| BATCH001 | CSV invalid       | Validate format |
| QUOTA001 | Quota exceeded    | Wait/increase   |

### Debugging Commands

```bash
# Check system status
youtube-processor diagnose

# Test components
youtube-processor test-all

# Verify setup
youtube-processor verify-installation
```

## Advanced Debugging

### Logging

1. **Enable Debug Logs**

   ```python
   # Set environment variable
   export YOUTUBE_PROCESSOR_LOG_LEVEL=DEBUG

   # Or in code
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Log File Location**

   ```
   logs/youtube_processor.log
   ```

3. **Log Analysis**

   ```bash
   # View recent errors
   tail -f logs/youtube_processor.log | grep ERROR

   # Search for specific issues
   grep "Upload failed" logs/youtube_processor.log
   ```

### Development Tools

1. **Interactive Debug Mode**

   ```bash
   youtube-processor --debug process video.mp4
   ```

2. **Network Debugging**

   ```python
   # Enable request logging
   import httplib2
   httplib2.debuglevel = 4
   ```

3. **Profile Performance**

   ```python
   import cProfile

   cProfile.run('process_video()')
   ```

### Recovery Steps

1. **Clean Start**

   ```bash
   # Remove all temporary files
   youtube-processor clean-all

   # Reset configuration
   youtube-processor reset-config

   # Reinitialize
   youtube-processor initialize
   ```

2. **Backup/Restore**

   ```bash
   # Backup configuration
   youtube-processor backup-config

   # Restore from backup
   youtube-processor restore-config
   ```

3. **Emergency Stop**

   ```bash
   # Stop all processes
   youtube-processor emergency-stop

   # Cancel scheduled uploads
   youtube-processor cancel-all
   ```

## Additional Resources

- [Error Code Reference](error_codes.md)
- [FFmpeg Troubleshooting](ffmpeg_guide.md)
- [Network Issues](network_guide.md)
- [API Quotas](quotas.md)

## Getting Help

### Support Resources

- 📚 [Documentation](https://github.com/dasdatasensei/YouTubeVideoAutomation/tree/main/docs)
- 💬 [Community Forum](https://github.com/dasdatasensei/YouTubeVideoAutomation/discussions)
- 🐛 [Issue Tracker](https://github.com/dasdatasensei/YouTubeVideoAutomation/issues)
- 📧 [Email Support](mailto:jody@thedatasensei.com)
- 📱 [Discord Server](https://discord.gg/thedatasensei)

### Debug Information

When reporting issues, please include:

1. Error message and stack trace
2. System information:
   ```bash
   youtube-processor debug-info
   ```
3. Steps to reproduce
4. Log files from:
   ```
   ~/.youtube-automation/logs/
   ```

### Contact Information

- Technical Support: [jody@thedatasensei.com](mailto:jody@thedatasensei.com)
- Discord: [Join Community](https://discord.gg/thedatasensei)
- GitHub: [Open Issue](https://github.com/dasdatasensei/YouTubeVideoAutomation/issues/new)
