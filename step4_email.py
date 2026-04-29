import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

from step1_scrap import scrap_data


# ---------------------------------
# LOAD ENV VARIABLES
# ---------------------------------
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


# ---------------------------------
# BASE DIRECTORY (AUTO-DETECT FILE LOCATION)
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FILE = os.path.join(BASE_DIR, "template.html")


def send_email_alert(data: dict) -> bool:
    # Email setup
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = f"🚨 Pandemic Alert - {data['country']}"

    # Load HTML template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Replace placeholders in template
    for key, value in data.items():
        html_content = html_content.replace(f"{{{{{key}}}}}", str(value))

    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

    return True


# -------------------
# MAIN PROGRAM (TEST)
# -------------------
if __name__ == "__main__":
    pandemic = scrap_data("Malaysia")
    send_email_alert(pandemic)
    print("✅ Alert email sent successfully")