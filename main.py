import json
from argparse import ArgumentParser
from datetime import datetime, timedelta

import tiktoken
from get_messages import get_messages
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from openai_api import chatgpt_summary
from parse_message import parse_message
from tqdm import tqdm


def generate_markdown_report(input_text, project_name, date):
    title = f"{project_name} 更新報告 - {date}"
    markdown_text = input_text.replace('\n', '\n\n')
    markdown_content = f"# {title}\n\n{markdown_text}"
    file_name = f"{project_name}-Update-{date}.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    return file_name


def main(project_name, time_length):

    current_date = datetime.now()
    after_date = current_date - timedelta(days=time_length)
    after_date = after_date.strftime('%Y/%m/%d')

    # 載入認證並創建 GmailAPI 客戶端
    creds = None

    # token.json 存儲了用戶的訪問令牌和刷新令牌，並在訪問令牌到期時自動刷新
    token_file = 'token.json'
    creds = Credentials.from_authorized_user_file(
        token_file, scopes=['https://www.googleapis.com/auth/gmail.readonly'])

    # 建立 GmailAPI 客戶端
    service = build('gmail', 'v1', credentials=creds)

    messages = get_messages(
        service,
        after_date=after_date,
        subject_filter=project_name
    )

    results = [
        parse_message(service, msg['id'])
        for msg in tqdm(messages)
    ]

    # 估計 token
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = enc.encode(json.dumps(results, indent=4))
    print(f'Length of tokens: {len(tokens)}')

    # 調用 OpenAI API
    summary = chatgpt_summary(json.dumps(results, indent=4))
    summary = f'{summary}\n\n---\n\n以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。'

    # 生成 Markdown 報告
    markdown_file = generate_markdown_report(summary)
    print(f"Markdown 文件已生成: {markdown_file}")


if __name__ == "__main__":
    parser = ArgumentParser(description="Generate a project update report.")
    parser.add_argument(
        "--project_name",
        type=str,
        help="The name of the project to track.",
        default="Albumentations"
    )
    parser.add_argument(
        "--time_length",
        type=int,
        help="The time length (in days) to track updates.",
        default=1
    )

    args = parser.parse_args()

    main(args.project_name, args.time_length)
