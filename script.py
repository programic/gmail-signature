import json
from string import Template
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_credentials():
    scopes = [
        'https://www.googleapis.com/auth/gmail.settings.basic',
        'https://www.googleapis.com/auth/gmail.settings.sharing',
    ]
    try:
        return service_account.Credentials.from_service_account_file('token.json', scopes=scopes)
    except Exception as e:
        raise Exception(f"Failed to load credentials: {e}")

def load_json_file(file_path, description):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, IOError, ValueError) as e:
        raise Exception(f"Error reading {description}: {e}")

def get_users():
    return load_json_file('users.json', 'users.json')

def get_template():
    try:
        with open('template.html', 'r') as sig_file:
            return Template(sig_file.read())
    except (FileNotFoundError, IOError) as e:
        raise Exception(f"Error reading template.html: {e}")

def get_primary_email(gmail_service):
    try:
        addresses = gmail_service.users().settings().sendAs().list(
            userId='me', fields='sendAs(isPrimary,sendAsEmail)'
        ).execute().get('sendAs', [])
        return next(
            (addr['sendAsEmail'] for addr in addresses if addr.get('isPrimary')),
            None,
        )
    except Exception as e:
        raise Exception(f"Failed to retrieve primary email address: {e}")

def update_signature(credentials, user):
    try:
        credentials_delegated = credentials.with_subject(user['username'])
        gmail_service = build('gmail', 'v1', credentials=credentials_delegated)

        primary_address = get_primary_email(gmail_service)
        if not primary_address:
            print(f"No primary address found for: {user['username']}")
            return

        # Remove the existing signature
        gmail_service.users().settings().sendAs().patch(
            userId='me', sendAsEmail=primary_address, body={'signature': ''}
        ).execute()

        # Set the new signature
        template = get_template()
        new_signature = template.substitute(
            full_name=user['full_name'],
            job_title=user['job_title'],
        )
        gmail_service.users().settings().sendAs().patch(
            userId='me', sendAsEmail=primary_address, body={'signature': new_signature}
        ).execute()

        print(f"Signature updated for: {user['username']}")
    except Exception as e:
        print(f"Failed to update signature for {user['username']}: {e}")

def test_credentials(credentials, user):
    try:
        credentials_delegated = credentials.with_subject(user['username'])
        gmail_service = build('gmail', 'v1', credentials=credentials_delegated)
        addresses = gmail_service.users().settings().sendAs().list(userId='me').execute()
        print(f"Addresses for {user['username']}: {addresses.get('sendAs', [])}")
    except Exception as e:
        print(f"Failed to test credentials for {user['username']}: {e}")

def main():
    try:
        credentials = get_credentials()
        users = get_users()

        # Optional: Test credentials for the first user
        if users:
            test_credentials(credentials, users[0])

        for user in users:
            update_signature(credentials, user)
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == '__main__':
    main()