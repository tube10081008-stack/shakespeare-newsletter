import json
import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RESEND_AUDIENCE_ID = os.getenv("RESEND_AUDIENCE_ID")

if not RESEND_API_KEY or not RESEND_AUDIENCE_ID:
    print("❌ Error: Missing API Key or Audience ID in .env")
    exit(1)

resend.api_key = RESEND_API_KEY

def migrate():
    json_path = os.path.join(os.path.dirname(__file__), "../src/data/subscribers.json")
    
    if not os.path.exists(json_path):
        print("❌ subscribers.json not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        subscribers = json.load(f)

    print(f"📦 Found {len(subscribers)} subscribers to migrate...")

    for email in subscribers:
        try:
            resend.Contacts.create({
                "email": email,
                "audience_id": RESEND_AUDIENCE_ID,
                "unsubscribed": False
            })
            print(f"✅ Migrated: {email}")
        except Exception as e:
            print(f"⚠️ Failed to migrate {email}: {e}")

if __name__ == "__main__":
    migrate()
