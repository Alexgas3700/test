# 📧 Monthly Newsletter System

Automated email newsletter system that pulls contacts from Google Sheets and sends monthly newsletters on a schedule.

## Features

- 📊 **Google Sheets Integration** - Fetch contacts directly from Google Sheets
- 📨 **Automated Email Sending** - Send beautiful HTML emails via SMTP
- 🗓️ **Monthly Scheduling** - Automatically send newsletters on a specific day each month
- 🎨 **Template Support** - Use Jinja2 templates for customizable email content
- 📝 **Logging** - Comprehensive logging for monitoring and debugging
- ✅ **Configuration Validation** - Built-in validation for all settings

## Project Structure

```
.
├── src/
│   ├── google_sheets_client.py    # Google Sheets integration
│   ├── email_sender.py             # Email sending functionality
│   └── newsletter_scheduler.py    # Scheduling and orchestration
├── templates/
│   ├── newsletter.html             # Main newsletter template
│   └── welcome.html                # Welcome email template
├── logs/                           # Log files (auto-created)
├── credentials/                    # Google service account credentials
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── .env.example                    # Example environment variables
└── README.md                       # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- SMTP email account (Gmail, SendGrid, etc.)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Google Sheets Setup

#### Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Sheets API
4. Create a service account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Give it a name and click "Create"
   - Grant it "Editor" role
   - Click "Done"
5. Create a key for the service account:
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Choose JSON format
   - Save the file as `credentials/service-account.json`

#### Prepare Your Google Sheet

1. Create a Google Sheet with your contacts
2. Format it with these columns (in order):
   - Column A: Name
   - Column B: Email
   - Column C: Status (optional - use "active" or "subscribed")
3. Share the sheet with the service account email (found in the JSON file)
4. Copy the Spreadsheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`

Example sheet format:

| Name          | Email                | Status    |
|---------------|----------------------|-----------|
| John Doe      | john@example.com     | active    |
| Jane Smith    | jane@example.com     | subscribed|
| Bob Johnson   | bob@example.com      | active    |

### 4. Email Configuration

#### For Gmail:

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Generate a new app password for "Mail"
   - Use this password in your `.env` file

#### For Other SMTP Providers:

- **SendGrid**: Use your API key as the password
- **Mailgun**: Use your SMTP credentials
- **Amazon SES**: Use your SMTP credentials

### 5. Environment Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Edit `.env` with your actual values:

```env
# Google Sheets Configuration
GOOGLE_SPREADSHEET_ID=your_actual_spreadsheet_id
GOOGLE_SPREADSHEET_RANGE=Sheet1!A:C
GOOGLE_CREDENTIALS_PATH=credentials/service-account.json

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=Your Newsletter Name

# Newsletter Configuration
NEWSLETTER_SUBJECT=Monthly Newsletter - {{month}}
NEWSLETTER_TEMPLATE=newsletter.html

# Schedule Configuration
SCHEDULE_DAY_OF_MONTH=1
SCHEDULE_TIME=09:00
```

### 6. Verify Configuration

Test your configuration:

```bash
python config.py
```

Test Google Sheets and SMTP connections:

```bash
cd src
python newsletter_scheduler.py --test
```

## Usage

### Run Newsletter Immediately (Testing)

```bash
cd src
python newsletter_scheduler.py --now
```

### Start the Scheduler

Run the scheduler to automatically send newsletters monthly:

```bash
cd src
python newsletter_scheduler.py
```

The scheduler will:
- Run daily at the configured time
- Check if it's the scheduled day of the month
- Send the newsletter if conditions are met
- Log all activities to `logs/newsletter.log`

### Run as a Background Service

#### Using systemd (Linux):

Create a service file `/etc/systemd/system/newsletter.service`:

```ini
[Unit]
Description=Monthly Newsletter Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/workspace
ExecStart=/usr/bin/python3 /path/to/workspace/src/newsletter_scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable newsletter.service
sudo systemctl start newsletter.service
sudo systemctl status newsletter.service
```

#### Using Docker:

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "src/newsletter_scheduler.py"]
```

Build and run:

```bash
docker build -t newsletter-system .
docker run -d --name newsletter --env-file .env newsletter-system
```

## Customizing Email Templates

Templates are located in the `templates/` directory and use Jinja2 syntax.

### Available Variables

- `{{ recipient_name }}` - Recipient's name
- `{{ recipient_email }}` - Recipient's email
- `{{ month }}` - Current month and year (e.g., "January 2026")
- `{{ year }}` - Current year

### Creating a New Template

1. Create a new HTML file in `templates/`
2. Use Jinja2 syntax for dynamic content
3. Update `NEWSLETTER_TEMPLATE` in `.env` to use your new template

Example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Newsletter</title>
</head>
<body>
    <h1>Hello {{ recipient_name }}!</h1>
    <p>This is the newsletter for {{ month }}.</p>
</body>
</html>
```

## Testing Individual Components

### Test Google Sheets Client

```bash
cd src
python google_sheets_client.py credentials/service-account.json YOUR_SPREADSHEET_ID
```

### Test Email Sender

```bash
cd src
python email_sender.py
```

## Monitoring and Logs

Logs are stored in `logs/newsletter.log` and include:
- Campaign start/end times
- Number of contacts fetched
- Number of emails sent/failed
- Error messages and stack traces

View logs:

```bash
tail -f logs/newsletter.log
```

## Troubleshooting

### "Missing required environment variables"

- Ensure your `.env` file exists and contains all required variables
- Check that variable names match exactly

### "Failed to authenticate with Google Sheets API"

- Verify your service account JSON file is in the correct location
- Ensure the Google Sheets API is enabled in your project
- Check that the service account has access to the spreadsheet

### "SMTP connection failed"

- Verify your SMTP credentials are correct
- For Gmail, ensure you're using an App Password, not your regular password
- Check that your firewall allows outbound connections on the SMTP port

### "No contacts found"

- Verify the spreadsheet ID is correct
- Check that the range includes your data
- Ensure the service account has "Viewer" or "Editor" access to the sheet

## Security Best Practices

1. **Never commit `.env` or credentials files** - They're in `.gitignore`
2. **Use App Passwords** - Don't use your main email password
3. **Restrict service account permissions** - Only grant necessary access
4. **Rotate credentials regularly** - Update passwords and service account keys
5. **Monitor logs** - Watch for suspicious activity

## Scheduling Options

The system checks daily if it should send the newsletter. Configure in `.env`:

- `SCHEDULE_DAY_OF_MONTH`: Day of month (1-31)
- `SCHEDULE_TIME`: Time in 24-hour format (HH:MM)

Examples:
- First day of month at 9 AM: `SCHEDULE_DAY_OF_MONTH=1`, `SCHEDULE_TIME=09:00`
- 15th of month at 2 PM: `SCHEDULE_DAY_OF_MONTH=15`, `SCHEDULE_TIME=14:00`

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this for your projects.

## Support

For questions or issues:
- Check the logs in `logs/newsletter.log`
- Review the configuration with `python config.py`
- Test connections with `python src/newsletter_scheduler.py --test`

---

Made with ❤️ for automated newsletter campaigns
