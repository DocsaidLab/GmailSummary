#!/bin/bash

project_name="albumentations"
log_dir="logs"
current_date=$(date '+%Y-%m-%d')
log_file="$log_dir/$project_name-log-$current_date.txt"

# 創造日誌資料夾，若已存在則忽略
mkdir -p $log_dir

# 開始執行並記錄日誌
{
    echo "Starting the script at $(date)"

    # 執行 Python 程式
    python main.py --project_name $project_name --time_length 1 2>&1

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

    echo "Script finished at $(date)"

} >> "$log_file" 2>&1

# 檢查最後命令是否成功
if [ $? -ne 0 ]; then
    echo "An error occurred, please check the log file $log_file."
fi
