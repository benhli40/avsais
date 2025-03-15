from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly"]

class GmailManager:
    def __init__(self):
        self.creds = None
        self.authenticate()
    
    def authenticate(self):
        """Handles OAuth2 authentication for Gmail API."""
        creds_path = "gmail_credentials.json"
        token_path = "token.pickle"
        
        if os.path.exists(token_path):
            with open(token_path, "rb") as token:
                self.creds = pickle.load(token)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError("Missing gmail_credentials.json. Ensure the file is in the correct directory.")
                
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            with open(token_path, "wb") as token:
                pickle.dump(self.creds, token)
    
    def send_email(self, recipient, subject, body):
        """Sends an email using Gmail API."""
        service = build("gmail", "v1", credentials=self.creds)
        message = MIMEText(body)
        message["to"] = recipient
        message["subject"] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            send_message = service.users().messages().send(userId="me", body={"raw": encoded_message}).execute()
            return f"Email sent successfully to {recipient}. Message ID: {send_message['id']}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"
    
if __name__ == "__main__":
    gmail_manager = GmailManager()
    
    # Example: Sending an email
    print(gmail_manager.send_email("recipient@example.com", "Test Email", "Hello! This is a test email sent from AVSAIS using OAuth2."))
