import json
import os
from typing import Dict, List

import tiktoken
from openai import OpenAI


def chatgpt_summary(results: List[Dict[str, str]], model: str = 'gpt-3.5-turbo') -> str:

    # Setting `OPENAI_API_KEY` environment variable is required
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    prompt = '''
        根據收到的電子郵件內容，這些是來自gmail api的解析內容，我需要你執行以下步驟以提供詳細的專案進度報告：
        - 關鍵訊息提取：首先，瀏覽郵件，忽略掉非核心訊息，例如日常寒暄、重複內容或不相關的細節。專注於找出關於專案的關鍵更新，包括但不限於錯誤修復、功能增加、討論的議題以及任何特別提到的成就或挑戰。
        - 時間軸建置：確定這些郵件覆蓋的時間範圍。 這可以是郵件中提到的具體日期，或根據郵件的發送時間推斷。 以時間軸為基礎，將找到的資訊依照時間順序排列。
        - 技術細節描述：鑑於目標讀者是該領域的專家，詳細描述與專案相關的技術細節，包括實施的技術方案、遇到的技術挑戰以及如何解決的。
        - 術語解釋：識別專有名詞或專業術語，並根據需要提供簡短的解釋或背景信息，以幫助即便是非項目成員的專家也能理解。
        請確保使用繁體中文編寫，以滿足目標讀者的需求。
    '''

    prompt_final = '''
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
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    for i, seg in enumerate(results_seg):
        content = json.dumps(seg)

        # 估計 token
        tokens = enc.encode(content)
        print(f'Segment {i}: Length of tokens: {len(tokens)}')

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
    print(
        f'Summary all segments, length of tokens: {len(enc.encode(all_content))}...', end=' ', flush=True)

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
