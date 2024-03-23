#!/bin/bash

cd $HOME/workspace/GmailSummary

# 指定項目名稱列表
project_names=("albumentations" "onnxruntime")
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
        mv $file_name "$project_path/README.md" 2>&1

        # 將新文件添加到 Git
        git add "$project_path/README.md" 2>&1

        # 提交更改
        git commit -m "[C] Updare $project_name report for $current_date" 2>&1

        # 推送到 GitHub
        git push 2>&1

        echo "Script finished for $project_name at $(date)"

    } >> "$log_file" 2>&1

    # 檢查最後命令是否成功
    if [ $? -ne 0 ]; then
        echo "An error occurred for $project_name, please check the log file $log_file."
    fi

done
