[English](./README.md) | **[中文](./README_tw.md)**

# GmailSummary

<p align="left">
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-dfd.svg"></a>
</p>

## Introduction

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
    - [6. 串接所有步驟](#6-串接所有步驟)
- [實作細節與建議](#實作細節與建議)
- [結論](#結論)

## 解決方案

我構思了一個方案，目的是透過自動化的工具來處理這些郵件，從而節省時間和精力。

整體設計流程和步驟如下列：

### 1. 使用 Gmail API 獲取郵件

首先，需要設置 Gmail API 來訪問我的郵箱。這需要在 Google Workspace 上註冊一個專案並啟用 Gmail API，然後按照 [**Python quickstart**](https://developers.google.com/gmail/api/quickstart/python) 的指南完成設定，獲取 `credentials.json`。

得到 `credentials.json` 之後，需要使用它來獲取 `token.json`，這是用於訪問郵箱的憑證。

用來獲取 `token.json` 的程式由 Google 所提供：[**login_get_token.py**](login_get_token.py)。

這大概是整個專案中最繁瑣的一步，但只需要做一次。比較麻煩的是取得 `token.json` 之後，它會一直過期，所以需要定期更新，因此我另外寫了一個程式來定時更新 `token.json`：[**refresh_token.sh**](refresh_token.sh)。

相關設定方式我會建議讀者直接參考官方文件，因為非官方的教學大多都已經過時了。（踩坑經驗）

執行 login 的程式前，記得先安裝相關的套件：

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. 下載並過濾郵件

接下來，利用 Gmail API 下載郵件並過濾掉不需要的郵件。

我寫了個程式 [**parse_message.py**](parse_message.py)，專門用於過濾和解析郵件內容。

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

        # 分段，每 30 個內容分一段
        results_seg = [results[i:i + 30] for i in range(0, len(results), 30)]

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
        all_content = '\n\n'.join(responses)
        summary = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{all_content}\n\n{prompt}"},
            ],
            temperature=0.7,
        ).choices[0].message.content

        return summary
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

為了讓這個過程完全自動化，我利用了 Linux 的 `crontab` 功能來設置定時任務。這樣可以確保每天固定時間自動執行程式，抓取新郵件，生成摘要，並更新 GitHub 存儲庫。

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

# 每天早上 6 點自動執行更新程式
0 6 * * * /path/to/your/script/update_albumentations_infos.sh

# 每小時更新 GmailAPI Token
*/50 * * * * /path/to/your/script/refresh_token.sh
```

在設置定時任務之前，不要忘記給程式文件賦予執行權限：

```bash
chmod +x /path/to/your/script/update_albumentations_infos.sh
chmod +x /path/to/your/script/refresh_token.sh
```

此外，由於 crontab 的環境特殊性，你必須確保執行的 python 環境和相關套件都是正確的。因此在程式中，我通常會使用絕對路徑來執行 python 程式，請記得要修改程式中的路徑。

```bash
# `update_albumentations_infos.sh` and `refresh_token.sh`

# ...以上省略

# 執行 Python 程式，要把這邊改成你自己的 python 路徑
$HOME/.pyenv/versions/3.8.18/envs/main/bin/python main.py --project_name $project_name --time_length 1 2>&1

# ...以下省略
```

---

提醒讀者 crontab 環境特殊性，它不會讀取你的 `.bashrc` 或 `.bash_profile` 等文件，所以你需要在程式中指定所有的環境變數。

這也是為什麼我會在 `crontab` 的執行程式中設置 `OPENAI_API_KEY` 環境變數的原因。

那麼完成設定後，該如何測試基於 crontab 環境的自動化任務呢？

這裡提供一個小技巧：我們啟動一個新的終端，剔除所有的環境變數，然後執行程式。

```bash
env -i HOME=$HOME OPENAI_API_KEY=your_openai_api_key /bin/bash --noprofile --norc

# 接著執行程式
/path/to/your/script/update_albumentations_infos.sh
```

從這個終端執行程式，你就可以看到程式在 crontab 環境下的執行狀況。

### 6. 串接所有步驟

最後，我把所有的步驟串接在一起，寫成了一個程式 [**update_albumentations_infos.py**](update_albumentations_infos.sh)。

其中包括了函數調用還有自動推送到 GitHub 的功能。

```bash
#!/bin/bash

# update_albumentations_infos.sh

cd $HOME/workspace/GmailSummary

# 指定項目名稱列表
project_names=("albumentations" "onnxruntime")
log_dir="logs"
current_date=$(date '+%Y-%m-%d')

# 創造日誌資料夾，若已存在則忽略
mkdir -p $log_dir

for project_name in "${project_names[@]}"; do

    log_file="$log_dir/$project_name-log-$current_date.txt"

    # 開始執行並記錄日誌
    {
        echo "Starting the script for $project_name at $(date)"

        # 執行 Python 程式
        $HOME/.pyenv/versions/3.8.18/envs/main/bin/python main.py --project_name $project_name --time_length 1 2>&1

        # 構造文件名
        file_name="$project_name-update-$current_date.md"

        # 創造專案資料夾，若已存在則忽略
        mkdir -p $project_name
        mv $file_name $project_name 2>&1

        # 將新文件添加到 Git
        git add "$project_name/$file_name" 2>&1

        # 提交更改
        git commit -m "[A] Add $project_name report for $current_date" 2>&1

        # 推送到 GitHub
        git push 2>&1

        echo "Script finished for $project_name at $(date)"

    } >> "$log_file" 2>&1

    # 檢查最後命令是否成功
    if [ $? -ne 0 ]; then
        echo "An error occurred for $project_name, please check the log file $log_file."
    fi

done
```

## 實作細節與建議

在實施這一個自動化方案時，我有些建議：

首先，不管怎樣，拜託不要：**硬編碼你的憑證和密鑰**。

這樣做會導致你的憑證和密鑰泄露，進而導致你的郵件和數據不再安全。

請將這些敏感信息存儲在安全的地方，並且不要將它們直接公開在任何場合。

- **確保安全性**：處理 Gmail API 和 OpenAI API 時，請妥善保管你的 `credentials.json` 和 API 密鑰。

其他就不是很重要了，就是一些小建議：

- **考慮郵件多樣性**：在過濾和解析郵件時，考慮到不同類型的郵件格式和內容，使程式能夠靈活應對各種情況。
- **定期檢查與維護**：雖然這是一個自動化方案，但定期檢查執行狀況和更新程式以適應可能的 API 變更仍然是必要的。

## 結論

通過這個項目，我再次成功地提高效率（偷懶）了。

我希望這個方案能夠幫助到有類似需求的人，並鼓勵更多的開發者探索和實施自動化解決方案來優化日常工作流程。

## FAQ

1. **為什麼不用 GPT-4？**

    因為很貴，雖然生成內容好，但是價格是 GPT-3.5 的 **20 倍**。我不想為了偷懶花太多錢。

2. **你的郵件內容不是機密嗎？**

    不是，這些郵件都是公開的，你只要去那些開源專案的 GitHub 頁面，就可以看到所有的內容，不過我猜你沒有耐心看完。
