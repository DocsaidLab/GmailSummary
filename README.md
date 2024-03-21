# GmailSummary

<div align="center">
    <img src="./docs/title.jpg" width="800">
</div>

在日常生活中，我們經常會因為點擊了 GitHub 上的某個專案的 `Watch` 選項而開始收到該專案的活動更新郵件。這些更新包括但不限於新功能的討論、issue 回報、pull request (PR) 以及 bug 報告等。

簡單舉個例子，如果你 `Watch` 了 `albumentations` 和 `onnxruntime` 項目，然後採用 `All Activity` 的方式：

- [**albumentations**](https://github.com/albumentations-team/albumentations): 大約每天收到 10 封郵件。
- [**onnxruntime**](https://github.com/microsoft/onnxruntime): 每天則是高達 200 封。

我們可以想像，如果你還關注了其他 10 個項目，那麼你每天將會收到 1000 封郵件。

我就想問：**真有人會一封不漏地閱讀這些郵件嗎？**

反正我不會，通常連看都不看就直接刪除了。

因此，作為一名尋求效率（偷懶）的工程師，我開始思考如何解決這個問題。

## 目錄

- [解決方案](#解決方案)
    - [1. 使用 Gmail API 獲取郵件](#1-使用-gmail-api-獲取郵件)
    - [2. 下載並過濾郵件](#2-下載並過濾郵件)
    - [3. 摘要生成](#3-摘要生成)
    - [4. 輸出摘要至 Markdown](#4-輸出摘要至-markdown)
    - [5. 定時執行自動化](#5-定時執行自動化)
- [實作細節與建議](#實作細節與建議)
- [結論](#結論)

## 解決方案

我構思了一個方案，目的是透過自動化的工具來處理這些郵件，從而節省時間和精力。

整體設計流程和步驟如下列：

### 1. 使用 Gmail API 獲取郵件

首先，需要設置 Gmail API 來訪問我的郵箱。這需要在 Google Workspace 上註冊一個專案並啟用 Gmail API，然後按照 [**Python quickstart**](https://developers.google.com/gmail/api/quickstart/python) 的指南完成設定，獲取 `credentials.json`。

得到 `credentials.json` 之後，需要使用它來獲取 `token.json`，這是用於訪問郵箱的憑證。

用來獲取 `token.json` 的腳本由 Google 所提供：[**login_get_token.py**](login_get_token.py)。

這大概是整個專案中最繁瑣的一步，但只需要做一次。比較麻煩的是取得 `token.json` 之後，它會一直過期，所以需要定期更新，因此我另外寫了一個腳本來定時更新 `token.json`：[**refresh_token.sh**](refresh_token.sh)。

相關設定方式我會建議讀者直接參考官方文件，因為非官方的教學大多都已經過時了。（踩坑經驗）

執行 login 的程式前，記得先安裝相關的套件：

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. 下載並過濾郵件

接下來，利用 Gmail API 下載郵件並過濾掉不需要的郵件。

我寫了個腳本 [**parse_message.py**](parse_message.py)，專門用於過濾和解析郵件內容。

### 3. 摘要生成

為了生成摘要，我考慮了兩種方案：

- **OpenAI 的 ChatGPT 模型**：

    這是我的首選方案，因為它提供了高品質的摘要。需要在 [OpenAI API](https://platform.openai.com/docs/overview) 註冊並安裝 `openai`，使用以下範例代碼生成摘要。

    ```python
    # 由 OpenAI 提供的範例檔案
    from openai import OpenAI
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
    )

    print(completion.choices[0].message)
    ```

    我參考他們提供的範例，把它修改成了一個更適合我的需求的版本，我嘗試了幾種 Prompt 的設置，最終選擇了一個效果最好的版本。

    ```python
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
    ```

- [**HuggingFace 的 mistral-7B 模型**](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) :

    雖然這是一個開源方案，但因效果不佳以及運算資源消耗較大，所以最終未採用。

    如果你想使用這個模型，可以參考以下由 HuggingFace 所提供的範例代碼：

    ```python
    # 由 HuggingFace 提供的範例檔案
    from transformers import AutoModelForCausalLM, AutoTokenizer

    device = "cuda" # the device to load the model onto

    model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")

    messages = [
        {"role": "user", "content": "What is your favourite condiment?"},
        {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
        {"role": "user", "content": "Do you have mayonnaise recipes?"}
    ]

    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")

    model_inputs = encodeds.to(device)
    model.to(device)

    generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)
    decoded = tokenizer.batch_decode(generated_ids)
    print(decoded[0])
    ```

### 4. 輸出摘要至 Markdown

為了方便閱讀和分享，摘要將輸出成 Markdown 格式，這樣就可以直接推送到 GitHub 上。

### 5. 定時執行自動化

為了讓這個過程完全自動化，我利用了 Linux 的 `crontab` 功能來設置定時任務。這樣可以確保每天固定時間自動執行腳本，抓取新郵件，生成摘要，並更新 GitHub 存儲庫。

具體的 `crontab` 設定如下：

```bash
crontab -e
```

接著添加以下內容：

```bash
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command

# Define your environment variables
OPENAI_API_KEY="your_openai_api_key"

# 每天早上 6 點自動執行更新腳本
0 6 * * * /path/to/your/script/update_albumentations_infos.sh

# 每小時更新 GmailAPI Token
*/50 * * * * /path/to/your/script/refresh_token.sh
```

在設置定時任務之前，不要忘記給腳本文件賦予執行權限：

```bash
chmod +x /path/to/your/script/update_albumentations_infos.sh
chmod +x /path/to/your/script/refresh_token.sh
```

此外，由於 crontab 的環境特殊性，你必須確保執行的 python 環境和相關套件都是正確的。因此在腳本中，我通常會使用絕對路徑來執行 python 程式，請記得要修改腳本中的路徑。

```bash
# `update_albumentations_infos.sh` and `refresh_token.sh`

# ...以上省略

# 執行 Python 程式，要把這邊改成你自己的 python 路徑
$HOME/.pyenv/versions/3.8.18/envs/main/bin/python main.py --project_name $project_name --time_length 1 2>&1

# ...以下省略
```

## 實作細節與建議

在實施這一個自動化方案時，我有些建議：

首先，不管怎樣，拜託不要：**硬編碼你的憑證和密鑰**。

這樣做會導致你的憑證和密鑰泄露，進而導致你的郵件和數據不再安全。

請將這些敏感信息存儲在安全的地方，並且不要將它們直接公開在任何場合。

- **確保安全性**：處理 Gmail API 和 OpenAI API 時，請妥善保管你的 `credentials.json` 和 API 密鑰。

其他就不是很重要了，就是一些小建議：

- **考慮郵件多樣性**：在過濾和解析郵件時，考慮到不同類型的郵件格式和內容，使腳本能夠靈活應對各種情況。
- **定期檢查與維護**：雖然這是一個自動化方案，但定期檢查執行狀況和更新腳本以適應可能的 API 變更仍然是必要的。

## 結論

通過這個項目，我再次成功地提高效率（偷懶）了。

我希望這個方案能夠幫助到有類似需求的人，並鼓勵更多的開發者探索和實施自動化解決方案來優化日常工作流程。

