#!/bin/bash

# 定義目錄和環境變量
origin_dir="$HOME/workspace/GmailSummary"
targ_dir="$HOME/workspace/website"
pyenv_path="$HOME/.pyenv/versions/3.10.14/envs/main/bin/python"
log_dir="$origin_dir/logs"
current_date=$(date '+%Y-%m-%d')
news_dir="$targ_dir/docs/gmailsummary/news/$current_date"

# 創建所需的目錄
mkdir -p "$log_dir" "$news_dir"

# 指定項目名稱列表
project_names=("albumentations") # "onnxruntime" "pytorch-lightning" "BentoML" "docusaurus"

for project_name in "${project_names[@]}"; do
    log_file="$log_dir/$project_name-log-$current_date.txt"
    project_path="$news_dir/$project_name"
    file_name="$project_name.md"
    mkdir -p "$project_path"

    # 執行 Python 程式並處理輸出
    {
        echo "Starting the script for $project_name at $(date)"
        $pyenv_path main.py --project_name $project_name --time_length 1
        mv "$origin_dir/$file_name" "$project_path"
        git -C "$targ_dir" add "$project_path/$file_name"
        git -C "$targ_dir" commit -m "[C] Update $project_name report for $current_date"
        echo "Script finished for $project_name at $(date)"
    } >> "$log_file" 2>&1

    # 檢查執行狀態
    if [ $? -ne 0 ]; then
        echo "An error occurred for $project_name, please check the log file $log_file." >> "$log_file"
    fi
done

# 推送 Git 變更
{
    git -C "$targ_dir" push
} >> "$log_file" 2>&1
