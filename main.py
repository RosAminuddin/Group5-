import json

from step1_scrap import scrap_data
from step2_excel import save_to_excel
from step3_db import init_db, save_db
from step4_email import send_email_alert


DEATH_ALERT_THRESHOLD = 1  # demo purpose


def main():
    print("🚀 Pandemic Alert Automation Started")

    data = scrap_data("Malaysia")
    print("✅ Data scraped")

    excel_path = save_to_excel(data)
    print(f"✅ Excel saved: {excel_path}")

    init_db()
    record = save_db(data)
    print("✅ DB saved")
    print(json.dumps(record, indent=2))

    if data["today_deaths"] >= DEATH_ALERT_THRESHOLD:
        send_email_alert(data)
        print("🚨 Alert email sent")
    else:
        print("ℹ️ No alert condition met")

    print("✅ Automation completed")


if __name__ == "__main__":
    main()