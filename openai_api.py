import os

from openai import OpenAI


def chatgpt_summary(content: str, model: str = 'gpt-3.5-turbo') -> str:

    # Setting `OPENAI_API_KEY` environment variable is required
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    prompt = '''
        我需要你幫我針對上面段落進行梳理和總結，然後給我彙整報告，要告訴讀者過去一段時間
        （請你根據郵件內容自行判定時間區段）內，這個專案發生什麼事情，有什麼錯誤被發現，
        有什麼議題在討論，新增了什麼功能和解決了什麼問題等等，包含但不限於以上，
        請你根據你的經驗提供更好的彙整方式。
        最後，考慮到輸出的內容可能有一些特定的專有名詞，請你自行判斷專有名詞是否需要額外的解釋，
        如果你認為讀者可能需要，那除了彙整資訊之外，還要再補上相關的延伸說明。
        請用繁體中文撰寫文章且儘可能闡述更多內容，且寫文章時請你務必注意分段和說明完整性。
    '''

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{content}\n\n{prompt}"},
        ],
        temperature=0,
    )

    return response.choices[0].message.content
