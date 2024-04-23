#!/bin/bash

# 定義目錄和環境變量
origin_dir="$HOME/workspace/GmailSummary"
targ_dir="$HOME/workspace/website"
pyenv_path="$HOME/.pyenv/versions/3.10.14/envs/main/bin/python"
log_dir="$origin_dir/logs"
current_date=$(date '+%Y-%m-%d')
project_path="$targ_dir/docs/gmailsummary/news/$current_date"

# 創建所需的目錄
mkdir -p "$log_dir" "$project_path"

cd $origin_dir

# 指定項目名稱列表
project_names=("albumentations" "onnxruntime" "pytorch-lightning" "BentoML" "docusaurus")

for project_name in "${project_names[@]}"; do
    log_file="$log_dir/$project_name-log-$current_date.txt"
    file_name="$project_name.md"

    # 執行程式並處理輸出
    {
        echo "Starting the script for $project_name at $(date)"
        $pyenv_path main.py --project_name $project_name --time_length 1
        mv "$origin_dir/$file_name" "$project_path"
        git -C "$targ_dir" add "$project_path/$file_name"
        echo "Script finished for $project_name at $(date)"
    } >> "$log_file" 2>&1

    # 檢查執行狀態
    if [ $? -ne 0 ]; then
        echo "An error occurred for $project_name, please check the log file $log_file." >> "$log_file"
    fi
done

git -C "$targ_dir" commit -m "[C] Update project report for $current_date"
git -C "$targ_dir" push
