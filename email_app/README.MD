# Email Application

A Python-based email client app that supports IMAP and POP3 protocols with OAuth2 authentication.

## Features

- OAuth2 authentication for Gmail
- Support for both IMAP and POP3 protocols
- Email attachment handling
- Email downloading and saving
- Unread email detection
- Subject-based email search

## Prerequisites

- Python 3.8+
- Gmail account
- OAuth2 credentials from Google Cloud Console

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up OAuth2 credentials:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Gmail API

## Configuration

1. 
   - `DOWNLOAD_FOLDER`: Path for saving attachments
   - `TOKEN_FILE`: Path for OAuth2 token storage
   - `SCOPES`: Gmail API scopes
   - `REDIRECT_URI`: OAuth2 callback URL

## File Structure

```
email_app/
├── email_downloads/
├── credentials.json
├── emails.py
├── get_token.py
├── main.py
├── requirements.txt
└── README.md
```