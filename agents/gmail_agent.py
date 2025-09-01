from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

def send_email(to, subject, body):
    try:
        creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.send"])
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

        sent = service.users().messages().send(userId="me", body={'raw': raw}).execute()
        return {"status": "sent", "message_id": sent['id']}
    except Exception as e:
        return {"status": "error", "message": str(e)}
