# Security Policy

## Supported Versions

We maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
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

## Credential Management

IMPORTANT: Never commit sensitive credentials to the repository. This includes:

- OAuth2.0 tokens
- API keys
- Client secrets
- Access tokens
- Refresh tokens
- Docker Hub tokens
- Any other secrets or credentials

### Proper Credential Management

1. Use environment variables for all sensitive data
2. Keep a `.env.example` file in the repo with dummy values
3. Create a local `.env` file (which is git-ignored) with real values
4. For CI/CD, use GitHub Secrets or similar secure storage
5. Regularly rotate all credentials
6. Revoke any exposed credentials immediately

## Security Features

- OAuth2.0 tokens are stored securely in your config directory
- All sensitive data is managed through environment variables
- API credentials are stored locally and encrypted
- Pre-commit hooks detect accidentally committed secrets

## Best Practices

1. **Environment Variables**

   - Never hardcode credentials
   - Use `.env` files for local development
   - Use secure secret management for production

2. **API Security**

   - OAuth2.0 implementation follows security best practices
   - Tokens are automatically refreshed and securely stored
   - All API calls use HTTPS

3. **Development Guidelines**
   - Use environment-specific credentials
   - Keep development and production credentials separate
   - Regular security audits
   - Monitor for exposed secrets

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. DO NOT create a public GitHub issue
2. Email security@yourdomain.com with details
3. Allow 48 hours for initial response
4. Keep the vulnerability private until fixed

## Security Checklist

- [ ] Environment variables configured
- [ ] No hardcoded credentials
- [ ] Pre-commit hooks enabled
- [ ] Credentials properly rotated
- [ ] Security documentation up to date
- [ ] CI/CD secrets configured
- [ ] Access tokens secured

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

- Security: security@thedatasensei.com
- General: jody@thedatasensei.com
- Emergency: security@thedatasensei.com

## Company Information

The Data Sensei
Dr. Jody-Ann S. Jones
Website: www.thedatasensei.com
GitHub: [@dasdatasensei](https://github.com/dasdatasensei)

## Updates

This security policy was last updated in 2025. Check the commit history for changes.
