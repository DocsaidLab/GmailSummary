from datetime import datetime, timedelta
from typing import Dict, List

import pytz


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
