from base64 import urlsafe_b64decode


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
