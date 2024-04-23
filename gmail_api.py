from base64 import urlsafe_b64decode
from datetime import datetime, timedelta
from typing import Dict, List

import pytz
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def build_service():
    creds = None
    token_file = 'token.json'
    creds = Credentials.from_authorized_user_file(
        token_file, scopes=['https://www.googleapis.com/auth/gmail.readonly'])
    service = build('gmail', 'v1', credentials=creds)
    return service


def get_messages(
    service,
    user_id='me',
    after_date=None,
    subject_filter: str = None,
    max_results: int = 500
) -> List[Dict[str, str]]:
    """
    A function to list all messages in the user's mailbox.

    Args:
        service:
            An authorized Gmail API service instance.
        user_id:
            The user's email address. The special value 'me' can be used to
            indicate the authenticated user.
        after_date:
            The start date of the date range to filter messages.
            Format: "yyyy/mm/dd".
        subject_filter:
            A string to filter messages by subject.
        max_results:
            The maximum number of messages to return. The default is 200.

    If no date range is specified, the function will list past 24 hours' messages.

    Returns:
        A list of message IDs.
    """
    tz = pytz.timezone('Asia/Taipei')
    if not after_date:
        now = datetime.now(tz)
        after_date = (now - timedelta(days=1)).strftime('%Y/%m/%d')

    messages = []
    try:
        query = ''
        if after_date:
            query += f' after:{after_date}'
        if subject_filter:
            query += f' subject:("{subject_filter}")'

        response = service.users().messages().list(
            userId=user_id, q=query, maxResults=max_results).execute()

        messages.extend(response.get('messages', []))

        # Handle pagination with nextPageToken
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id, q=query, maxResults=max_results, pageToken=page_token).execute()
            messages.extend(response.get('messages', []))

    except Exception as error:
        print(f'An error occurred: {error}')

    if not messages:
        print("No messages found.")

    return messages


def parse_message(service, msg_id, user_id='me'):
    """
    Parse and display the sent time, subject, sender, recipient, and content of
    a specific email.

    Args:
        service:
            An authorized Gmail API service instance.
        msg_id:
            The ID of the email to extract information from.
        user_id:
            The user's email address. The special value 'me' can be used to
            indicate the authenticated user.


    Returns:
        A dictionary containing the sent time, subject, sender, recipient, and
        content of the email.
    """

    try:
        message = service.users().messages().get(
            userId=user_id, id=msg_id, format='full').execute()
        headers = message['payload']['headers']
        parts = message['payload'].get('parts', [])
        email_data = {
            'Date': None,
            'Subject': None,
            'Text': None
        }

        # 解析頭信息以獲取寄件時間、主旨、寄件者和收件者
        for header in headers:
            if header['name'] == 'Date':
                email_data['Date'] = header['value']
            elif header['name'] == 'Subject':
                email_data['Subject'] = header['value']

        # 解析郵件正文
        for part in parts:
            if part['mimeType'] == 'text/plain' or part['mimeType'] == 'text/html':
                data = part['body']['data']
                text = urlsafe_b64decode(data.encode('ASCII')).decode('UTF-8')
                email_data['Text'] = text
                break  # 只取第一個符合條件的部分

        return email_data

    except Exception as error:
        print(f'An error occurred: {error}')
        return None
