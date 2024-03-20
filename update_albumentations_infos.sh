#!/bin/bash

project_name="albumentations"

# 執行 Python 程式
python main.py --project_name $project_name --time_length 1

# 獲取當前日期
current_date=$(date '+%Y-%m-%d')

# 構造文件名
file_name="$project_name-update-$current_date.md"

# 創造資料夾，若有存在則忽略
mkdir -p $project_name
mv $file_name $project_name

# 將新文件添加到 Git
git add "$project_name/$file_name"

# 提交更改
git commit -m "[A] Add $project_name report for $current_date"

# 推送到 GitHub
git push
