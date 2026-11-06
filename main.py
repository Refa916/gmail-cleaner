import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

print("DEBUG: EMAIL_USER =", EMAIL_USER)
print("DEBUG: EMAIL_PASS =", "SET" if EMAIL_PASS else "MISSING")

if not EMAIL_USER or not EMAIL_PASS:
    print("❌ ERROR: Missing EMAIL_USER or EMAIL_PASS in environment variables.")
    exit(1)

# Keywords to flag as spam
keywords = ["stock","trade", "buy","promotion","alert" ]

# Connection config
SINCE = "01-Jan-2025"
BEFORE = "01-Jul-2025"
BATCH_SIZE = 3000
progress_file = "last_email.txt"

def connect():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("inbox")
    return mail

def save_progress(index):
    with open(progress_file, "w") as f:
        f.write(str(index))

def load_progress():
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            return int(f.read().strip())
    return 0

def decode_subject(subject_raw):
    if not subject_raw:
        return ""
    decoded = decode_header(subject_raw)[0]
    subject, encoding = decoded if len(decoded) == 2 else (decoded[0], None)
    if isinstance(subject, bytes):
        try:
            subject = subject.decode(encoding or "utf-8", errors="ignore")
        except Exception:
            subject = subject.decode("utf-8", errors="ignore")
    return subject

# Start cleaning loop
start_index = load_progress()
mail = connect()
print("✅ Logged in successfully")
print(f"Using SINCE={SINCE} and BEFORE={BEFORE}")

status, search_data = mail.search(None, f'(SINCE {SINCE} BEFORE {BEFORE})')
email_ids = search_data[0].split()
total_emails = len(email_ids)
print(f"📨 Found {total_emails} emails in range")
if start_index > 0:
    print(f"🔁 Resuming from email #{start_index + 1}")

while start_index < total_emails:
    try:
        end_index = min(start_index + BATCH_SIZE, total_emails)
        print(f"\n⚙️  Processing emails {start_index + 1} to {end_index}")

        deleted_count = 0

        for i in range(start_index, end_index):
            num = email_ids[i]
            status, msg_data = mail.fetch(num, "(RFC822)")

            if status != "OK" or not msg_data or not isinstance(msg_data[0], tuple):
                print(f"⚠️ Skipping email ID: {num}")
                continue

            raw_email = msg_data[0][1]
            try:
                msg = email.message_from_bytes(raw_email)
            except Exception as e:
                print(f"⚠️ Malformed email at index {i}: {e}")
                continue

            subject = decode_subject(msg["Subject"])
            print(f"Checking: {subject}")

            if any(keyword.lower() in subject.lower() for keyword in keywords):
                print(f"👉 Match & deleting: {subject}")
                mail.store(num, "+FLAGS", "\\Deleted")
                deleted_count += 1

            time.sleep(0.02)

        mail.expunge()
        print(f"✅ Batch complete. Deleted: {deleted_count}")
        start_index = end_index
        save_progress(start_index)

    except (imaplib.IMAP4.abort, ConnectionResetError) as e:
        print(f"\n⚠️ Connection lost: {e}")
        print("⏳ Pausing for 30 seconds then reconnecting...")
        time.sleep(30)
        mail = connect()
        print("🔁 Reconnected. Resuming...")

print("\n🎉 All matching emails processed and deleted.")
if os.path.exists(progress_file):
    os.remove(progress_file)






