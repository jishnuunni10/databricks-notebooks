# Databricks Notebooks Collection

This repository contains Databricks notebooks exported from the workspace for version control, collaboration, and documentation purposes.

## Repository Contents

### Notebooks

1. **Touch_update_account.py** / **Touch update account.py**
   - Purpose: Update and "touch" account records via REST API
   - Functionality: Updates account timestamps and metadata
   - Use Case: Account activity tracking and audit trails
   - [Detailed Documentation](https://github.com/jishnuunni10/databricks-notebooks/blob/main/Touch_update_account.py)

2. **TUbot_upd.py**
   - Purpose: Telegram bot for sending status updates and notifications
   - Functionality: Automated messaging and monitoring via Telegram
   - Use Case: Real-time pipeline monitoring and alerting
   - [Detailed Documentation](https://github.com/jishnuunni10/databricks-notebooks/blob/main/TUbot_upd.py)

## Getting Started

### Prerequisites

- Databricks workspace access
- Python 3.8 or higher
- Required Python packages:
  ```bash
  pip install requests
  ```

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/jishnuunni10/databricks-notebooks.git
   ```

2. Import notebooks into your Databricks workspace:
   - Navigate to your Databricks workspace
   - Click "Workspace" → "Import"
   - Select the notebook files from this repository
   - Choose the destination folder

### Configuration

#### For Touch Update Account:
- Set `API_ENDPOINT` to your target API URL
- Configure `HEADERS` with appropriate authentication token
- Store sensitive credentials in Databricks Secrets

#### For TUbot Update:
- Obtain Telegram Bot token from [@BotFather](https://t.me/botfather)
- Get your Chat ID
- Store credentials securely using Databricks Secrets:
  ```python
  BOT_TOKEN = dbutils.secrets.get(scope="telegram-bot", key="bot-token")
  CHAT_ID = dbutils.secrets.get(scope="telegram-bot", key="chat-id")
  ```

## Usage Examples

### Touch Update Account
```python
# Initialize and touch an account
account_id = "12345"
result = touch_account(account_id)

if result:
    print(f"Account {account_id} touched successfully")
```

### TUbot Update
```python
# Initialize bot and send notification
bot = TUBot(BOT_TOKEN, CHAT_ID)
bot.send_message("Pipeline started!")

# Update status
bot.update_bot_status("Processing data...")
```

## Documentation

Comprehensive documentation for each notebook is available in the `.md` directory:
- `Touch_update_account.md` - Complete guide with examples, API reference, and troubleshooting
- `TUbot_upd.md` - Detailed documentation covering setup, usage, and best practices

## Features

### Touch Update Account
- ✅ REST API integration for account updates
- ✅ Timestamp management
- ✅ Error handling and logging
- ✅ Configurable endpoints and authentication

### TUbot Update
- ✅ Telegram integration for notifications
- ✅ HTML message formatting support
- ✅ Periodic status updates
- ✅ Error recovery and logging
- ✅ Databricks job monitoring

## Best Practices

1. **Security**
   - Never hardcode credentials in notebooks
   - Always use Databricks Secrets for sensitive data
   - Implement proper access controls

2. **Error Handling**
   - Implement retry logic for network calls
   - Log errors appropriately
   - Send alerts for critical failures

3. **Monitoring**
   - Track notebook execution metrics
   - Set up alerts for failures
   - Monitor API rate limits

4. **Version Control**
   - Commit changes with descriptive messages
   - Use branches for experimental features
   - Tag releases for production deployments

## Integration Points

These notebooks can be integrated with:
- Databricks Jobs for scheduled execution
- Delta Lake for data operations
- MLflow for ML pipeline monitoring
- Azure Event Hubs / AWS Kinesis for streaming
- Apache Airflow for orchestration

## Troubleshooting

### Common Issues

**Issue**: API authentication fails
- **Solution**: Verify token validity and permissions

**Issue**: Telegram bot not responding
- **Solution**: Check bot token and chat ID, verify network access

**Issue**: Rate limiting errors
- **Solution**: Implement delays between requests

For detailed troubleshooting, refer to the individual notebook documentation files.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Repository Structure

```
databricks-notebooks/
├── README.md                      # This file
├── Touch update account.py        # Account update notebook
├── Touch_update_account.py        # Account update notebook (no spaces)
├── TUbot_upd.py                  # Telegram bot notebook
└── .gitignore                    # Git ignore patterns
```

## Workspace Information

- **Original Location**: `/Workspace/Users/chakkappazhamseries1@gmail.com`
- **Databricks Instance**: `dbc-954e6b63-50c7.cloud.databricks.com`
- **Export Date**: February 4, 2026

## Dependencies

### Python Packages
- `requests` - HTTP library for API calls
- `json` - JSON data handling
- `datetime` - Timestamp management
- `time` - Time operations
- `logging` - Structured logging
- `typing` - Type hints

### Databricks Utilities
- `dbutils.secrets` - Secure credential management
- `dbutils.notebook` - Notebook operations

## Version History

- **v1.0.0** (2026-02-04): Initial repository setup
  - Added Touch Update Account notebook
  - Added TUbot Update notebook
  - Created comprehensive documentation

## License

This project is maintained for internal use. Please refer to your organization's policies regarding code usage and distribution.

## Support

For questions, issues, or feature requests:
- Create an issue in this repository
- Contact the data engineering team
- Refer to detailed documentation in the `.md` files

## Related Resources

- [Databricks Documentation](https://docs.databricks.com/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Python Requests Library](https://requests.readthedocs.io/)

## Acknowledgments

- Databricks community for platform support
- Telegram for Bot API
- Contributors to the open-source libraries used

---

**Last Updated**: February 4, 2026  
**Repository**: https://github.com/jishnuunni10/databricks-notebooks  
**Maintained By**: Data Engineering Team
