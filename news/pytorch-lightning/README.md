# pytorch-lightning 更新報告 - 2024-04-01

根據收到的郵件內容，專案的重要更新如下：



1. **Issue #19717 - Extending Argument Linking**：

   在這個議題中，討論了對於參數鏈接功能的擴展。目前的參數鏈接要求兩個參數必須相同，但提出了改進方案，使得可以處理更複雜的參數關係，例如 `a = b + 1`。這項改進將為使用者帶來更大的靈活性和功能性。



2. **Issue #19718 - Training stuck when running on Slurm with multiprocessing**：

   使用者報告了在使用單個GPU在Slurm上進行訓練時遇到的問題。具體來說，在 `training_step` 中調用 `multiprocessing.Pool()` 導致訓練過程永遠無法結束。這需要進一步的調查和解決，以確保在Slurm環境中正常運行。



3. **Issue #19716 - Support TorchEval**：

   討論了對於支持TorchEval的需求，並提到了相容性問題和可能的解決方案。團隊正在積極努力解決問題，以提供更好的支持。



這些更新顯示了團隊對於專案的持續關注和改進，解決問題並增加新功能，以提供更好的用戶體驗和功能性。這些改進將有助於提升專案的效能和功能性，並確保在不同環境下的正常運行。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。