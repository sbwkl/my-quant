import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import httplib2
import socks
from google.oauth2 import service_account
from google_auth_httplib2 import AuthorizedHttp

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

class GmailService():
    def __init__(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("creds/token.json"):
          creds = Credentials.from_authorized_user_file("creds/token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
          else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "creds/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
          # Save the credentials for the next run
          with open("creds/token.json", "w") as token:
            token.write(creds.to_json())


        PROXY_IP = '127.0.0.1'
        PROXY_PORT = 7898
        PROXY_TYPE = socks.SOCKS5 

        proxy_info = httplib2.ProxyInfo(
            proxy_type=PROXY_TYPE,
            proxy_host=PROXY_IP,
            proxy_port=PROXY_PORT
        )

        http = httplib2.Http(proxy_info=proxy_info)
        authorized_http = AuthorizedHttp(creds, http=http)

        # Call the Gmail API
        self.service = build("gmail", "v1", http=authorized_http)
    def message_list(self, q):
        results = self.service.users().messages().list(userId="me", q=q, maxResults=5).execute()
        messages = results.get("messages", [])
        return messages

    def message_get(self, id):
        return self.service.users().messages().get(userId="me", id=id).execute()


def main():
    service = GmailService()
    
    messages = service.message_list("is:unread")

    if not messages:
        print("No messages found.")
        return
    
    print("Messages:")
    for message in messages:
        print(f'Message ID: {message["id"]}')
        msg = (
            service.message_get(message["id"])
        )
        print(f'  Subject: {msg["snippet"]}')

# if __name__ == "__main__":
#   main()