from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build("gmail", "v1", credentials=creds)

results = service.users().messages().list(
    userId="me",
    q="is:unread",
    maxResults=5
).execute()

messages = results.get("messages", [])

print(f"\nUnread emails found: {len(messages)}\n")

for message in messages:
    email = service.users().messages().get(
        userId="me",
        id=message["id"],
        format="metadata",
        metadataHeaders=["From", "Subject", "Date"]
    ).execute()

    headers = email.get("payload", {}).get("headers", [])

    data = {}
    for header in headers:
        data[header["name"]] = header["value"]

    print("=" * 60)
    print("From   :", data.get("From", "Unknown"))
    print("Subject:", data.get("Subject", "No subject"))
    print("Date   :", data.get("Date", "Unknown"))
    print("=" * 60)