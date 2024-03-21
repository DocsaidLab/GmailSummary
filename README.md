**[English](./README.md)** | [中文](./README_tw.md)

# GmailSummary

<p align="left">
    <a href="./LICENSE"><img src="https://img.shields.io/badge/license-Apache%202-dfd.svg"></a>
</p>

## Introduction

<div align="center">
    <img src="./docs/title.jpg" width="800">
</div>

In everyday life, we often start receiving activity update emails from a GitHub project after clicking the `Watch` option on it. These updates include, but are not limited to, discussions of new features, issue reports, pull requests (PRs), and bug reports, among others.

For example, if you `Watch` the `albumentations` and `onnxruntime` projects and opt for `All Activity`:

- [**albumentations**](https://github.com/albumentations-team/albumentations): You might receive about 10 emails per day.
- [**onnxruntime**](https://github.com/microsoft/onnxruntime): You could get up to 200 emails per day.

Imagine if you're following 10 more projects, you could be receiving 1000 emails a day.

One might wonder: **Does anyone actually read all these emails?**

I certainly don't. I usually delete them without even looking.

Therefore, as an engineer seeking efficiency (or laziness), I began contemplating a solution to this problem.

## Table of Contents

- [Solution](#solution)
    - [1. Using the Gmail API to Retrieve Emails](#1-using-the-gmail-api-to-retrieve-emails)
    - [2. Downloading and Filtering Emails](#2-downloading-and-filtering-emails)
    - [3. Summary Generation](#3-summary-generation)
    - [4. Outputting Summary to Markdown](#4-outputting-summary-to-markdown)
    - [5. Scheduling Automation](#5-scheduling-automation)
    - [6. Integrating All Steps](#6-integrating-all-steps)
- [Implementation Details and Suggestions](#implementation-details-and-suggestions)
- [Conclusion](#conclusion)

## Solution

I devised a plan aimed at handling these emails through automated tools, thereby saving time and effort.

The overall design process and steps are as follows:

### 1. Using the Gmail API to Retrieve Emails

Firstly, it's necessary to set up the Gmail API to access my mailbox. This involves registering a project on Google Workspace, enabling the Gmail API, and then following the [**Python quickstart**](https://developers.google.com/gmail/api/quickstart/python) guide to complete the setup and obtain `credentials.json`.

After obtaining `credentials.json`, you'll need it to acquire `token.json`, which serves as the credential to access the mailbox.

The script provided by Google for obtaining `token.json` is [**login_get_token.py**](login_get_token.py).

This is perhaps the most tedious step of the entire project, but it only needs to be done once. The tricky part is that after obtaining `token.json`, it expires continually, so I wrote another script to refresh `token.json` periodically: [**refresh_token.sh**](refresh_token.sh).

I would recommend readers directly refer to the official documentation for the setup process, as most unofficial tutorials are outdated. (A lesson learned the hard way)

Before running the login program, remember to install the necessary packages:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. Downloading and Filtering Emails

Next, use the Gmail API to download emails and filter out unwanted messages.

I wrote a script, [**parse_message.py**](parse_message.py), specifically for filtering and parsing email content.

### 3. Summary Generation

To generate summaries, I considered two approaches:

- **OpenAI's ChatGPT Model**:

    This was my preferred solution, as it offers high-quality summaries. Registration and installation of `openai` are necessary at [OpenAI API](https://platform.openai.com/docs/overview), and the following example code can be used to generate summaries.

    ```python
    # Example file provided by OpenAI
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

    Inspired by their example, I adapted it into a version more suited to my needs. After experimenting with various Prompt configurations, I selected the most effective version.

    ```python
    import json
    import os
    from typing import Dict, List

    import tiktoken
    from openai import OpenAI


    def chatgpt_summary(results: List[Dict[str, str]], model: str = 'gpt-3.5-turbo') -> str:

        # Setting the `OPENAI_API_KEY` environment variable is required
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

        prompt = '''
            I need you to sift through the preceding paragraphs and summarize them.
            First, eliminate any irrelevant information and identify key textual
            descriptions.
            Then compile a report, detailing what has happened in the project
            over a certain period, based on the content of the emails.
            Please determine the time frame yourself.
            Describe any errors, issues, new features added, and problems solved,
            among other things. You might devise a better way to consolidate
            this information based on your experience.
            Finally, considering the output may contain specific jargon,
            decide if any terms require further explanation. If you think the
            reader might need it, then in addition to summarizing the information,
            include relevant extended explanations.
            Please write the article in Traditional Chinese, elaborating as
            much detail as possible. Since the readers are experts in the field,
            you may describe more related engineering details while ensuring
            paragraph division and completeness of explanations.
        '''

        # Segmenting the results, 30 items per segment
        results_seg = [results[i:i + 30] for i in range(0, len(results), 30)]

        responses = []
        for i, seg in enumerate(results_seg):
            content = json.dumps(seg)

            # Estimate tokens
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

        # Consolidating segment results
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

- [**HuggingFace's mistral-7B model**](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2):

    Although this is an open-source solution, it was ultimately not adopted due to poor performance and high computational resource consumption.

    For those interested in using this model, the example code provided by HuggingFace can be referenced:

    ```python
        # Example file provided by HuggingFace
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

### 4. Outputting Summary to Markdown

For ease of reading and sharing, the summary will be output in Markdown format. This allows for direct pushing to a GitHub repository.

### 5. Scheduling Automation

To fully automate the process, I utilized Linux's `crontab` functionality to set up a scheduled task. This ensures the script automatically runs at a fixed time every day to fetch new emails, generate summaries, and update the GitHub repository.

The specific `crontab` setup is as follows:

```bash
crontab -e
```

Then add the following content:

```bash
# Define your environment variables
OPENAI_API_KEY="your_openai_api_key"

# Automatically run the update script at 6 AM every day
0 6 * * * /path/to/your/script/update_targets_infos.sh

# Refresh the GmailAPI Token every hour
*/50 * * * * /path/to/your/script/refresh_token.sh
```

Before setting up the scheduled tasks, don't forget to grant execution permissions to the script files:

```bash
chmod +x /path/to/your/script/update_targets_infos.sh
chmod +x /path/to/your/script/refresh_token.sh
```

Moreover, due to the unique environment of crontab, you must ensure the correct python environment and associated packages are used. Hence, in the scripts, I usually employ absolute paths for running python programs. Be sure to modify the paths in your scripts accordingly.

```bash
# `update_targets_infos.sh` and `refresh_token.sh`

# ...omitted above

# Run the Python program, remember to change this to your python path
$HOME/.pyenv/versions/3.8.18/envs/main/bin/python main.py --project_name $project_name --time_length 1 2>&1

# ...omitted below
```

---

Reminding readers about the peculiarities of the crontab environment, it does not load your `.bashrc` or `.bash_profile` among other files. Hence, you need to specify all your environment variables within your script.

This is the reason why I set the `OPENAI_API_KEY` environment variable in the crontab's executing script.

So, how do you test an automation task based on the crontab environment after setting it up?

Here's a little trick: start a new terminal session, stripping out all environment variables, then run your script.

```bash
env -i HOME=$HOME OPENAI_API_KEY=your_openai_api_key /bin/bash --noprofile --norc

# Then run your script
/path/to/your/script/update_targets_infos.sh
```

Executing your script from this terminal session allows you to see how it would run under the crontab environment.

### 6. Integrating All Steps

Finally, I integrated all the steps into one script named [**update_targets_infos.py**](update_targets_infos.sh), which includes function calls and the capability to automatically push updates to GitHub.

```bash
#!/bin/bash

cd $HOME/workspace/GmailSummary

# 指定項目名稱列表
project_names=("albumentations" "onnxruntime" "pytorch")
log_dir="logs"
news_dir="news"
current_date=$(date '+%Y-%m-%d')

# 創造日誌資料夾，若已存在則忽略
mkdir -p $log_dir

# 創造news目錄，若已存在則忽略
mkdir -p $news_dir

for project_name in "${project_names[@]}"; do

    log_file="$log_dir/$project_name-log-$current_date.txt"

    project_path="$news_dir/$project_name"

    # 開始執行並記錄日誌
    {
        echo "Starting the script for $project_name at $(date)"

        # 執行 Python 程式
        $HOME/.pyenv/versions/3.8.18/envs/main/bin/python main.py --project_name $project_name --time_length 1 2>&1

        # 構造文件名
        file_name="$project_name-update-$current_date.md"

        # 創造專案資料夾，若已存在則忽略
        mkdir -p $project_path
        mv $file_name $project_path 2>&1

        # 將新文件添加到 Git
        git add "$project_path/$file_name" 2>&1

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

## Implementation Details and Suggestions

When implementing this automation solution, I have some suggestions:

First and foremost, please do not: **hard-code your credentials and keys**.

This could lead to the leakage of your credentials and keys, compromising the security of your emails and data.

Store these sensitive pieces of information securely and do not publicly disclose them under any circumstances.

- **Ensure Security**: When handling the Gmail API and OpenAI API, securely manage your `credentials.json` and API keys.

Other than that, there are just some minor suggestions:

- **Consider the Diversity of Emails**: When filtering and parsing emails, consider different types of email formats and contents to make the script adaptable to various situations.
- **Regular Check and Maintenance**: Although this is an automated solution, regularly checking the execution status and updating scripts to accommodate possible API changes is still necessary.

## Conclusion

Through this project, I have once again successfully increased efficiency (or laziness).

I hope this solution can help those with similar needs and encourage more developers to explore and implement automation solutions to optimize their daily workflows.

## FAQ

1. **Why not use GPT-4?**

    Because it's expensive. Although it produces better content, the price is **20 times** that of GPT-3.5. I don't want to spend too much just for the sake of laziness.

2. **Isn't the content of your emails confidential?**

    No, these emails are public. You can see all the content if you visit the GitHub pages of those open-source projects. However, I guess you don't have the patience to read them all.

3. **How ​​to specify the emails to be analyzed?**

    In `update_targets_infos.py`, you can modify `project_names` to set the projects you want to analyze.

    ```bash
    # update_targets_infos.py
    # Specify a list of project names
    project_names=("albumentations" "onnxruntime") # <-- Modify this line
    ```
