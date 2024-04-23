import json
import os
from typing import Dict, List

import tiktoken
from openai import OpenAI


def chatgpt_summary(results: List[Dict[str, str]], model: str = 'gpt-3.5-turbo') -> str:

    # Setting `OPENAI_API_KEY` environment variable is required
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    prompt = '''
        根據收到的電子郵件內容，這些是來自gmail api的解析內容，請你進行關鍵訊息提取，
        包括但不限於錯誤修復、功能增加、討論的議題以及任何特別提到的成就或挑戰，請詳細描述你認為重要的內容。
    '''

    prompt_final = '''
        針對前面所有內容進行梳理和總結，找到關鍵的文字敘述，包括但不限於錯誤修復、功能增加、
        討論的議題以及任何特別提到的成就或挑戰，請詳細描述你認為重要的內容。
        最後，考慮到內容可能有一些專有名詞，請你額外的補充相對應的解釋和延伸說明。
        請用繁體中文撰寫文章且儘可能闡述詳細的內容，讀者是該領域的專家，
        因此寫文章時請你可以多描述一些相關的工程細節，請使用分段說明和保持敘述的完整性。
    '''

    # 分段，每 20 個內容分一段
    results_seg = [results[i:i + 20] for i in range(0, len(results), 20)]

    responses = []
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    for i, seg in enumerate(results_seg):
        content = json.dumps(seg)

        # 估計 token
        tokens = enc.encode(content)
        print(f'Segment {i}: Length of tokens: {len(tokens)}')

        if len(tokens) > 16000:
            continue

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{content}\n\n{prompt}"},
            ],
            temperature=0.2,
        ).choices[0].message.content

        responses.append(response)

    # 彙整分段結果
    all_content = '\n\n'.join(responses)
    tokens = enc.encode(all_content)
    print(
        f'Summary all segments, length of tokens: {len(tokens)}...', end=' ', flush=True)

    summary = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{all_content}\n\n{prompt_final}"},
        ],
        temperature=0.2,
    ).choices[0].message.content
    print('Done.')

    return summary
