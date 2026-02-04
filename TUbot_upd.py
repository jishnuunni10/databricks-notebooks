# Databricks notebook source
# TUbot Update

import time
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TUBot:
    """
    TelegramUpdate Bot class for handling bot operations
    """
    
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize the TUBot
        
        Args:
            bot_token: Telegram bot token
            chat_id: Target chat ID
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Send a message via Telegram bot
        
        Args:
            message: The message text to send
            
        Returns:
            Response dictionary or None if failed
        """
        import requests
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent successfully: {message[:50]}...")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message: {e}")
            return None
    
    def update_bot_status(self, status: str) -> bool:
        """
        Update the bot status
        
        Args:
            status: New status for the bot
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"Updating bot status to: {status}")
        message = f"🤖 Bot Status Update: {status}"
        result = self.send_message(message)
        return result is not None
    
    def run_periodic_update(self, interval_seconds: int = 300):
        """
        Run periodic status updates
        
        Args:
            interval_seconds: Interval between updates (default 5 minutes)
        """
        logger.info(f"Starting periodic updates every {interval_seconds} seconds")
        
        while True:
            try:
                status = f"Active - {time.strftime('%Y-%m-%d %H:%M:%S')}"
                self.update_bot_status(status)
                time.sleep(interval_seconds)
            except KeyboardInterrupt:
                logger.info("Stopping periodic updates")
                break
            except Exception as e:
                logger.error(f"Error in periodic update: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

# Example usage
if __name__ == "__main__":
    # Configuration (replace with your actual values)
    BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    CHAT_ID = "YOUR_CHAT_ID_HERE"
    
    # Initialize bot
    bot = TUBot(BOT_TOKEN, CHAT_ID)
    
    # Send initial message
    bot.send_message("TUBot initialized and ready!")
    
    # Run periodic updates (uncomment to enable)
    # bot.run_periodic_update(interval_seconds=300)
