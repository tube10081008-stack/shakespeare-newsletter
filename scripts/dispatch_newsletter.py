import asyncio
import json
import os
import sys
import time
import resend
from dotenv import load_dotenv
from generate_issue import generate_issue
from email_template import generate_email_html

# Load environment variables
load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "onboarding@resend.dev") # Default Resend Test Email

if RESEND_API_KEY:
    resend.api_key = RESEND_API_KEY

async def dispatch():
    print("🚀 [Dispatcher] Starting Daily Bard sequence...")
    
    # 1. Generate Content
    print("✍️ [Dispatcher] Asking NotebookLM to write today's issue...")
    start_time = time.time()
    
    # Check if a forced/demo issue exists and is recent (optional logic, skipping for now to always generate fresh or use existing)
    # For now, we reuse the existing logic: generate if needed, or just read latest.
    # To ensure automation, we should probably generate fresh content if this is a scheduled run.
    # For this script, let's assume we want to generate fresh content.
    await generate_issue()
    # print("⚠️ [Dispatcher] Skipping generation for test run (using existing data).")
    
    duration = time.time() - start_time
    print(f"✅ [Dispatcher] Content generated in {duration:.2f}s")

    # 2. Read Generated Content
    data_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_issue.json")
    if not os.path.exists(data_path):
        print("❌ [Dispatcher] Error: Content file not found!")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 3. Create Email Body
    print("🎨 [Dispatcher] Designing HTML email...")
    html_body = generate_email_html(data)
    
    # Save HTML for inspection
    html_path = os.path.join(os.path.dirname(__file__), "../src/data/latest_email.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_body)
    print(f"💾 [Dispatcher] Email preview saved to: {html_path}")

    # 4. Read Subscribers
    subscribers_file = os.path.join(os.path.dirname(__file__), "../src/data/subscribers.json")
    subscribers = []
    if os.path.exists(subscribers_file):
        with open(subscribers_file, "r") as f:
            try:
                subscribers = json.load(f)
            except:
                pass
    
    # Add a fallback for testing if list is empty
    if not subscribers:
        print("⚠️ [Dispatcher] No subscribers found. Sending to test email only.")
        # Attempt to prompt or default? Let's just warn.
        # subscribers = ["delivered@resend.dev"] 

    print(f"📨 [Dispatcher] Preparing to send to {len(subscribers)} subscribers...")
    
    if not RESEND_API_KEY:
        print("⚠️ [Dispatcher] RESEND_API_KEY not found in .env. Skipping actual send. (Simulation Mode)")
        for sub in subscribers:
            print(f"   [Simulation] 📤 Sent to {sub}")
            await asyncio.sleep(0.5)
        return

    # Real Send via Resend
    success_count = 0
    for sub in subscribers:
        try:
            params = {
                "from": "The Daily Bard <" + SENDER_EMAIL + ">",
                "to": [sub],
                "subject": f"📜 {data.get('title', 'The Daily Bard')}",
                "html": html_body,
            }
            
            email = resend.Emails.send(params)
            print(f"   [Resend] 📤 Sent to {sub} (ID: {email.get('id')})")
            success_count += 1
            await asyncio.sleep(0.5) # Rate limiting courtesy
        except Exception as e:
            print(f"   [Resend] ❌ Failed to send to {sub}: {str(e)}")

    print(f"🎉 [Dispatcher] Batch complete! Sent {success_count}/{len(subscribers)} emails.")

if __name__ == "__main__":
    asyncio.run(dispatch())
