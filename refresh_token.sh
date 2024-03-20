#!/bin/bash

cd $HOME/workspace/GmailSummary

log_file="login-$(date '+%Y-%m-%d').log"

# 執行 python 刷新令牌，同時處理正常輸出和錯誤
$HOME/.pyenv/versions/3.8.18/envs/main/bin/python "./login_get_token.py" >> $log_file 2>&1
