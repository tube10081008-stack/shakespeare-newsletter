import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if not RESEND_API_KEY:
    print("❌ Error: RESEND_API_KEY not found in .env")
    exit(1)

resend.api_key = RESEND_API_KEY

def setup_audience():
    print("🔍 Checking existing Audiences...")
    try:
        audiences = resend.Audiences.list()
        
        # Check if we already have an audience
        existing_audience = None
        if audiences and 'data' in audiences and len(audiences['data']) > 0:
            # Just pick the first one or look for a specific name
            for aud in audiences['data']:
                 if aud['name'] == "Shakespeare Newsletter":
                     existing_audience = aud
                     break
            
            if not existing_audience:
                # Use the first one if specific one not found
                existing_audience = audiences['data'][0]
        
        if existing_audience:
            print(f"✅ Found existing Audience: {existing_audience['name']} (ID: {existing_audience['id']})")
            return existing_audience['id']
        
        print("Creating new Audience 'Shakespeare Newsletter'...")
        new_audience = resend.Audiences.create({
            "name": "Shakespeare Newsletter"
        })
        print(f"✅ Created new Audience: {new_audience['name']} (ID: {new_audience['id']})")
        return new_audience['id']

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    audience_id = setup_audience()
    if audience_id:
        print(f"\n👉 Please add this to your .env file:\nRESEND_AUDIENCE_ID={audience_id}")
        with open("audience_id.txt", "w") as f:
            f.write(audience_id)
