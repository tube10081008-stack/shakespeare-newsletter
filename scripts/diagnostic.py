import os
import sys
import resend
from dotenv import load_dotenv

def run_diagnostics():
    print("🔍 [Diagnostic] Starting Resend Configuration Check...")
    
    # 1. Check Environment Variables
    api_key = os.environ.get("RESEND_API_KEY")
    audience_id = os.environ.get("RESEND_AUDIENCE_ID")
    sender_email = os.environ.get("SENDER_EMAIL")
    
    print(f"   [Env] RESEND_API_KEY: {'✅ Found' if api_key else '❌ MISSING'}")
    print(f"   [Env] RESEND_AUDIENCE_ID: {'✅ Found' if audience_id else '❌ MISSING'} (Value: {audience_id if audience_id else 'None'})")
    print(f"   [Env] SENDER_EMAIL: {'✅ Found' if sender_email else '⚠️ MISSING (Will default to onboarding@resend.dev)'}")
    
    if not api_key:
        print("❌ Critical Error: RESEND_API_KEY is missing. Cannot proceed.")
        sys.exit(1)
        
    resend.api_key = api_key
    
    # 2. Check Audience (if ID exists)
    if audience_id:
        print(f"\n🔍 [Diagnostic] Testing Audience Access ({audience_id})...")
        try:
            # Try to fetch list
            response = resend.Contacts.list(audience_id=audience_id)
            print(f"   [Audience] API Response: {response}")
        except Exception as e:
            print(f"   [Audience] ❌ Failed: {str(e)}")
    
    # 3. Test Email Send (REAL INBOX TEST)
    print("\n🔍 [Diagnostic] Testing Real Email Dispatch (Domain Verified)...")
    
    # Real recipients from user's list
    recipients = ["gartenhong@gmail.com", "vinty030@naver.com", "tube10081008@gmail.com"]
    sender = sender_email if sender_email else "Shakespeare <hello@daily-shakespeare.site>"
    
    print(f"   [Email] Attempting to send from '{sender}' to {recipients}...")
    
    try:
        params = {
            "from": sender,
            "to": recipients,
            "subject": "✅ [Final Success] Shakespeare System Connected",
            "html": """
            <h1>System Operational</h1>
            <p>Domain verification confirmed. The pipeline is fully open.</p>
            <p>This email proves that <b>Resend is now accepting emails for your real users.</b></p>
            <br>
            <p>- The Daily Bard Team</p>
            """
        }
        
        email = resend.Emails.send(params)
        print(f"   [Email] ✅ Success! Sent to {len(recipients)} people. ID: {email.get('id')}")
        print(f"   [Email] Full Response: {email}")
    except Exception as e:
        print(f"   [Email] ❌ Failed to send: {str(e)}")

if __name__ == "__main__":
    run_diagnostics()
