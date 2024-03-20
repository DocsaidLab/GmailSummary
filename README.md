# GmailSummary

<div align="center">
    <img src="./docs/title.jpg" width="800">
</div>

在日常生活中，我們經常會因為點擊了 GitHub 上的某個專案的 `Watch` 選項而開始收到該專案的活動更新郵件。這些更新包括但不限於 issue 回報、pull request (PR) 以及 bug 報告等。例如，我曾經遇到的情況如下：

- [**albumentations**](https://github.com/albumentations-team/albumentations): 大約每天收到 10 封郵件。
- [**onnxruntime**](https://github.com/microsoft/onnxruntime): 每天則是高達 200 封。

這引發了一個問題：真有人會一封不漏地閱讀這些郵件嗎？

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

我構思了一個方案，目的是透過自動化的工具來處理這些郵件，從而節省時間和精力。整體設計流程和步驟如下列：

### 1. 使用 Gmail API 獲取郵件

首先，需要設置 Gmail API 來訪問我的郵箱。這需要在 Google Workspace 上註冊一個專案並啟用 Gmail API，然後按照 [Python quickstart](https://developers.google.com/gmail/api/quickstart/python) 的指南完成設定，獲取 `credentials.json` 和 `token.json`。

這大概是整個專案中最繁瑣的一步，但只需要做一次。

我會建議讀者直接參考官方文件，因為非官方的教學大多都已經過時了。（踩坑經驗）

### 2. 下載並過濾郵件

接下來，利用 Gmail API 下載郵件並過濾掉不需要的郵件。我寫了個腳本 [parse_message.py](parse_message.py)，專門用於過濾和解析郵件內容。

### 3. 摘要生成

為了生成摘要，我考慮了兩種方案：

- **OpenAI 的 ChatGPT 模型**: 這是我的首選方案，因為它提供了高品質的摘要。需要在 [OpenAI API](https://platform.openai.com/docs/overview) 註冊並安裝 `openai`，使用以下範例代碼生成摘要。

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

- [**HuggingFace 的 mistral-7B 模型**](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) : 雖然這是一個開源方案，但因效果不佳以及運算資源消耗較大，所以最終未採用。

    如果你想使用這個模型，可以參考以下範例代碼：

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
# 每天早上 6 點自動執行更新腳本
0 6 * * * /path/to/your/script/update_albumentations_infos.sh
```

在設置定時任務之前，不要忘記給腳本文件賦予執行權限：

```bash
chmod +x /path/to/your/script/update_albumentations_infos.sh
```

這樣，每天系統將自動處理郵件摘要並更新，大大節省了人工閱讀和整理的時間。

## 實作細節與建議

在實施這一個自動化方案時，我有些建議：

首先，不管怎樣，拜託不要：**硬編碼你的憑證和密鑰**。

這樣做會導致你的憑證和密鑰泄露，進而導致你的郵件和數據不再安全。請將這些敏感信息存儲在安全的地方，並且不要將它們直接公開在任何場合。

- **確保安全性**：處理 Gmail API 和 OpenAI API 時，請妥善保管你的 `credentials.json` 和 API 密鑰。

其他就不是很重要了，就是一些小建議：

- **考慮郵件多樣性**：在過濾和解析郵件時，考慮到不同類型的郵件格式和內容，使腳本能夠靈活應對各種情況。
- **定期檢查與維護**：雖然這是一個自動化方案，但定期檢查執行狀況和更新腳本以適應可能的 API 變更仍然是必要的。

## 結論

通過這個項目，我再次成功地提高效率（偷懶）了。

我希望這個方案能夠幫助到有類似需求的人，並鼓勵更多的開發者探索和實施自動化解決方案來優化日常工作流程。

