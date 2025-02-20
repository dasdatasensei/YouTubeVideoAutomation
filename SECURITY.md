# Security Policy

## Supported Versions

We maintain security updates for the following versions:

| Version | Supported          |
| ------- | ----------------- |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Considerations

### Data Security
- All video files are processed locally on your machine
- OAuth2.0 tokens are stored securely in your config directory
- No video content is transmitted to third parties
- API credentials are stored locally and encrypted

### API Security
- All API communication uses HTTPS
- OAuth2.0 implementation follows security best practices
- Tokens are automatically refreshed and securely stored
- Rate limiting is implemented to prevent API abuse

### Local Storage
- Temporary files are cleaned up after processing
- Work directories are created with appropriate permissions
- Sensitive files are not included in logs

## Reporting a Vulnerability

We take security seriously. If you find a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email security@thedatasensei.com with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - (Optional) Suggested fix

We will:
1. Acknowledge receipt within 24 hours
2. Provide an initial assessment within 72 hours
3. Keep you updated on the progress
4. Credit you in our security acknowledgments (if desired)

## Best Practices for Users

1. **API Credentials**
   - Keep your `client_secrets.json` secure
   - Don't share your OAuth tokens
   - Regularly rotate credentials

2. **File Security**
   - Clear the work directory after usage
   - Don't process sensitive videos on shared machines
   - Keep your installation updated

3. **Access Control**
   - Use environment-specific credentials
   - Limit API scope to necessary permissions
   - Monitor your Google Cloud Console for unusual activity

## Security Features

Our application implements several security measures:

1. **Authentication**
   - Secure OAuth2.0 implementation
   - Token refresh handling
   - Automatic token secure storage

2. **File Handling**
   - Secure temporary file creation
   - Automatic cleanup
   - Permission checking

3. **Error Handling**
   - No sensitive data in error messages
   - Secure logging practices
   - Failed authentication handling

4. **Network Security**
   - HTTPS for all API communication
   - Certificate validation
   - Secure webhook handling

## Development Security

For developers contributing to the project:

1. **Environment Setup**
   - Use virtual environments
   - Keep dependencies updated
   - Follow secure coding practices

2. **Testing**
   - Run security checks
   - Use test credentials
   - Validate input handling

3. **Code Review**
   - Security-focused reviews
   - Dependency scanning
   - Regular security audits

## Acknowledgments

We thank the following for their security contributions:
- Security researchers and reporters
- Open source security tools
- GitHub security features

## Contact

- Security: security@thedatasensei.com.com
- General: support@thedatasensei.com
- Emergency: security-emergency@thedatasensei.com

## Updates

This security policy may be updated. Check the commit history for changes.
