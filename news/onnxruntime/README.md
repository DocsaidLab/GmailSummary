# onnxruntime 更新報告 - 2024-04-11

根據收到的郵件內容，以下是幾個重要的專案更新：



1. 在 [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) 專案中，有一個關於更新 protobufjs 版本的 PR (#20270)。這次更新將 protobufjs 從 7.2.4 升級到 7.2.5，修復了一些 bug，包括註釋解析中的崩潰、新 Buffer 的棄用警告等。這次更新還提供了釋出說明和變更日誌，詳細列出了修復的問題和改進的內容。



2. 另一個重要更新是在 [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) 專案的 PR #20167 中，討論了是否將 TensorRT 10 支援的 PR (#19695) 合併到主分支。團隊同意先將該 PR 合併到主分支，以確保順利進行後續工作。



3. 還有一倁關於整合 ONNX 1.16.0 的討論在 [microsoft/onnxruntime](https://github.com/microsoft/onnxruntime) 專案的 PR #19745 中。提及了新增的測試和修正，以確保與最新版本的 ONNX 整合順利進行。



這些更新顯示了團隊在持續改進專案功能和性能方面的努力，並且展示了他們在解決問題和實現目標方面的進展。這些訊息對於團隊成員和利益相關者來說都是重要的，因為它們提供了對專案進展的清晰和具體的了解。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。