from argparse import ArgumentParser
from datetime import datetime, timedelta

from gmail_api import build_service, get_messages, parse_message
from openai_api import chatgpt_summary
from tqdm import tqdm


def generate_markdown_report(input_text, project_name, date):
    title = f"{project_name}"
    markdown_text = input_text.replace('\n', '\n\n')
    markdown_content = f"# {title}\n\n## {date} 彙整報告\n\n{markdown_text}"
    file_name = f"{project_name}.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(markdown_content)
    return file_name


def main(project_name, time_length):

    current_date = datetime.now()
    after_date = current_date - timedelta(days=time_length)
    after_date = after_date.strftime('%Y/%m/%d')

    service = build_service()
    messages = get_messages(
        service,
        after_date=after_date,
        subject_filter=project_name
    )

    results = [
        parse_message(service, msg['id'])
        for msg in tqdm(messages)
    ]

    # 調用 OpenAI API
    summary = chatgpt_summary(results)
    summary = f'{summary}\n\n---\n\n本日共彙整郵件： {len(results)} 封\n\n以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。'

    # 生成 Markdown 報告
    markdown_file = generate_markdown_report(
        summary, project_name, current_date.strftime('%Y-%m-%d'))
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
