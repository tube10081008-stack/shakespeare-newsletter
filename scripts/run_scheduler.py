import schedule
import time
import subprocess
import os
import sys

# Define the task
def job():
    print(f"\n⏰ [Scheduler] It's 07:00 AM! Triggering The Daily Bard...")
    script_path = os.path.join(os.path.dirname(__file__), "dispatch_newsletter.py")
    
    # Run the dispatch script
    try:
        # Use the same python executable
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ [Scheduler] Error running dispatch: {e}")

# Schedule the job
# For testing, you can uncomment the next line to run every minute:
# schedule.every(1).minutes.do(job)

# Production Schedule
schedule.every().day.at("07:00").do(job)

print("⏳ [Scheduler] Daily Bard Scheduler Started.")
print("   - Target Time: 07:00 AM Daily")
print("   - To test immediately, modify the script to run 'every(1).minutes'")
print("   - Press Ctrl+C to stop.")

# Check loop
while True:
    schedule.run_pending()
    time.sleep(60)
