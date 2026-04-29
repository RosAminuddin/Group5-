# ============================================================
# step5_telegram.py
# WHAT  : Send a Telegram message notification via Bot API
#
# SETUP (do this once):
#   1. Open Telegram → search @BotFather → send /newbot
#   2. Follow prompts → copy the bot TOKEN it gives you
#   3. Start a chat with your new bot (send it any message)
#   4. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
#   5. Find "chat" → "id" in the response → copy that number
#   6. Add both to your .env file (see keys below)
# ============================================================

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID   = os.getenv("TELEGRAM_CHAT_ID")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


# ============================================================
# step5_telegram.py
# WHAT  : Send Pandemic Alert notification via Telegram Bot API
# ============================================================
 
import requests
import os
from dotenv import load_dotenv
 
load_dotenv()
 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
 
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
 
 
def send_telegram_notification(record: dict) -> bool:
    """
    Send a Telegram message with pandemic record details.
 
    Args:
        record: dict returned from save_db():
                { id, data, created_at }
 
    Returns:
        True if sent successfully
    """
 
    data = record["data"]
 
    message = (
        "🚨 PANDEMIC ALERT\n\n"
        f"Record ID      : {record['id']}\n"
        f"Recorded At   : {record['created_at']}\n\n"
        f"Country       : {data['country']}\n"
        f"Today Cases   : {data['today_cases']}\n"
        f"Today Deaths  : {data['today_deaths']}\n"
        f"Total Cases   : {data['total_cases']}\n\n"
        "Data saved to Excel & Database ✅"
    )
 
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
 
    try:
        print("[TELEGRAM] Sending notification...")
        response = requests.post(TELEGRAM_API_URL, data=payload, timeout=10)
        response.raise_for_status()
        print("[TELEGRAM] Notification sent successfully ✅")
        return True
 
    except Exception as e:
        print(f"[TELEGRAM] Failed to send notification: {e}")
        return False
 
 
# -------------------
# MAIN PROGRAM (TEST)
# -------------------
if __name__ == "__main__":
    from step1_scrap import scrap_data
    from step3_db import init_db, save_db
 
    init_db()
    pandemic = scrap_data("Malaysia")
    record = save_db(pandemic)
 
    send_telegram_notification(record)
 