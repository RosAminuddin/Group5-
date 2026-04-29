
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
# ---------------------------------
# EMAIL CREDENTIALS (from GitHub Secrets)
# ---------------------------------
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# ---------------------------------
# TEMPLATE PATH
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "template.html")


def send_email_github(data: dict) -> bool:
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
        raise RuntimeError("Missing email credentials in environment variables")

    # Load HTML template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace placeholders
    for key, value in data.items():
        html_content = html_content.replace(f"{{{{{key}}}}}", str(value))

    # Create email
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = f"🚨 Pandemic Alert - {data['country']}"

    msg.attach(MIMEText(html_content, "html"))

    # Send email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    print("📧 Email sent successfully from GitHub Actions")
    return True


if __name__ == "__main__":
    from step1_scrap import scrap_data

    data = scrap_data("Malaysia")
    send_email_github(data)
