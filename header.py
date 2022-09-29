import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

__all__ = ["get_body_heats"]

SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.metadata',
]
TOKEN = 'key/token.json'
CREDENTIALS = 'key/credentials.json'
MAX_RESULTS = 100 # recommended value is number of people in a team
LABEL_ID = 'Label_3169023884978674845'

def print_log(*logs, **settings):
    print(*logs, **settings)

def get_token(token_path):
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds

def get_headers_by(service):
    def get_headers(id):
        return (
            service.users()
                .messages()
                .get(userId='me', id=id, format='metadata')
                .execute()["payload"]["headers"]
            )
    return get_headers

def get_body_heats():
    creds = get_token(TOKEN)
    try:
        service = build('gmail', 'v1', credentials=creds)
        mails = service.users().messages().list(userId='me', labelIds=LABEL_ID).execute()
        get_headers = get_headers_by(service)
    except HttpError as error:
        print(f'An error occurred: {error}')

    if not mails:
        print('No body heat found.')
        return
    for mail in mails['messages']:
        try:
            headers = get_headers(mail['id'])
            contents = {content['name']: content['value'] for content in headers}
            yield tuple(contents[name] for name in ["Subject", "Date", "From"])
        except HttpError as error:
            print_log(f"Error when get the mail id {mail['id']}")
            continue