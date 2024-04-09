# BentoML 更新報告 - 2024-04-10

根據收到的郵件內容，BentoML專案最近的重要更新和討論內容如下：



1. **錯誤修復 - PR #4643**：

   這次修復涉及修正上傳狀態比較的問題。Frost Ming提交了這個修復，並在`src/bentoml/_internal/cloud/bentocloud.py`文件中進行了12處更改。修復解決了可能影響上傳功能的問題，提高了系統的穩定性和可靠性。



2. **功能增加 - PR #4644**：

   這個PR主要更新了BentoML的高層次消息。修改了`README.md`、`docs/source/get-started/introduction.rst`和`docs/source/index.rst`。這次更新提高了BentoML的文檔質量和用戶體驗，使使用者更容易理解和使用BentoML。



3. **討論議題 - Discussion #4645**：

   討論了如何在創建`bentoml.Model`時更改臨時目錄的問題。用戶遇到本地預訓練模型時空間不足的問題，詢問如何更改`bentoml.Model.path`。這引發了對`bentoml.Model`路徑設置的討論，提出了一些解決方案。



以上是BentoML專案最近的重要更新和討論內容。這些更新和討論對專案的進展和用戶體驗都具有重要意義。修復了上傳功能的問題、提高了文檔質量和用戶體驗，以及討論了如何處理模型路徑的問題，這些都是對專案發展和改進有益的貢獻。希望這些更新能夠幫助專案更好地發展，提升使用者的滿意度。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。