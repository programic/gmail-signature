import os.path
import json
from string import Template

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import *
from google.auth.exceptions import *

def get_credentials():
    scopes =['https://www.googleapis.com/auth/gmail.settings.basic', 'https://www.googleapis.com/auth/gmail.settings.sharing']
    credentials = service_account.Credentials.from_service_account_file('token.json', scopes=scopes)
    if not credentials:
        raise Exception('No credential file selected, so stopping')

    return credentials

def get_users():
    try:
        users_file = open('users.json', 'r')
        return json.load(users_file)
    except (FileNotFoundError, IOError, ValueError):
        print('Could not open the users.json file')
        raise

def get_template():
    try:
        sig_file = open('template.html', 'r')
        return Template(sig_file.read())
    except (FileNotFoundError, IOError):
        print('Could not open the template.html file')
        raise

def update_sig(credentials, user):
    credentials_delegated = credentials.with_subject(user['username'])
    gmail_service = build('gmail', 'v1', credentials=credentials_delegated)

    # Get primary address of user
    addresses = gmail_service.users().settings().sendAs().list(userId='me', fields='sendAs(isPrimary,sendAsEmail)').execute().get('sendAs')
    address = None
    for address in addresses:
        if address.get('isPrimary'):
            break

    if address:
        sig = get_template().substitute(full_name=user['full_name'], job_title=user['job_title'], working_days=user['working_days'])
        rsp = gmail_service.users().settings().sendAs().patch(userId='me', sendAsEmail=address['sendAsEmail'], body={'signature': sig}).execute()
        print(f"Signature changed for: {user['username']}")
    else:
        print(f"Could not find primary address for: {user['username']}")

def test_credentials(credentials, user):
    credentials_delegated = credentials.with_subject(user['username'])
    gmail_service = build('gmail', 'v1', credentials=credentials_delegated)
    addresses = gmail_service.users().settings().sendAs().list(userId='me').execute()
    print(addresses)

def main():
    credentials = get_credentials()
    users = get_users()

    test_credentials(credentials, users[0])

#     for user in users:
#         update_sig(credentials, user)

if __name__ == '__main__':
    main()