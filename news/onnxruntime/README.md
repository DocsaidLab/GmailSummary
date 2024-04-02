# onnxruntime 更新報告 - 2024-04-03

根據收到的郵件內容，專案中的一些重要更新如下：



1. **LLC Core count calculations updated (PR #20171)**：

   在這個Pull Request中，提到了LLC核心計算的更新，並成功啟動了Azure Pipelines中的一個流水線。雖然具體的調整細節未在郵件中提及，但可以看出團隊正在對LLC核心計算進行調整和更新。



2. **Fix build errors from date/date.h C++20 compatibility (PR #20139)**：

   這個Pull Request解決了與C++20兼容性相關的錯誤，並且在Azure Pipelines中成功啟動了多個流水線。修復這些錯誤對於確保代碼的順利構建和運行至關重要。



3. **Add dml build instructions for onnxruntime-genai (PR #20179)**：

   這個Pull Request包含了一系列提交，旨在為onnxruntime-genai添加DirectML構建指令。除此之外，提交中還進行了格式調整，以確保指令的清晰和準確。



4. **Export of Openai Whisper with batched prompts (PR #19854)**：

   這個Pull Request涉及到Openai Whisper的導出，並且在提交中添加了緩存目錄。這個更新可能有助於改善Openai Whisper的功能和性能。



5. **[Performance] Share weights between sessions to accelerate inference (Issue #20172)**：

   這個議題討論了共享權重以加速推斷的方法。討論涉及到保存某些張量作為外部張量、權重共享對記憶體和時間的節省，以及讀取和覆蓋特定張量的問題。這些討論有助於優化推斷過程的效率和性能。



這些更新涵蓋了專案中的重要變更和討論，包括修復錯誤、新增功能以及性能優化方面的工作。團隊的努力和合作有助於專案的持續進展和改進。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。