import json
import os
from typing import Dict, List

import tiktoken
from openai import OpenAI


def chatgpt_summary(results: List[Dict[str, str]], model: str = 'gpt-3.5-turbo') -> str:

    # Setting `OPENAI_API_KEY` environment variable is required
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    prompt = '''
        我需要你針對前面段落進行梳理和總結，你會先過去掉其中不重要的資訊，找到關鍵的文字敘述。
        然後你彙整報告，告訴讀者過去一段時間內，請你根據郵件內容自行判定時間區段，
        這個專案發生什麼事情，有什麼錯誤，議題，新增了什麼功能和解決了什麼問題等等，
        包含但不限於以上，你會根據你的經驗提供更好的彙整方式。
        最後，考慮到輸出的內容可能有一些特定的專有名詞，請你自行判斷專有名詞是否需要額外的解釋，
        如果你認為讀者可能需要，那除了彙整資訊之外，還要再補上相關的延伸說明。
        請用繁體中文撰寫文章且儘可能闡述詳細的內容，讀者是該領域的專家，因此寫文章時請你可以
        多描述一些相關的工程細節，同時務必注意分段和說明完整性。
    '''

    # 分段，每 20 個內容分一段
    results_seg = [results[i:i + 20] for i in range(0, len(results), 20)]

    responses = []
    for i, seg in enumerate(results_seg):
        content = json.dumps(seg)

        # 估計 token
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
        tokens = enc.encode(content)
        print(f'Segment {i}: Length of tokens: {len(tokens)}')

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{content}\n\n{prompt}"},
            ],
            temperature=0.7,
        ).choices[0].message.content

        responses.append(response)

    # 彙整分段結果
    print(f'Summary all segments...', end=' ')
    all_content = '\n\n'.join(responses)
    summary = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{all_content}\n\n{prompt}"},
        ],
        temperature=0.7,
    ).choices[0].message.content
    print('Done.')

    return summary
