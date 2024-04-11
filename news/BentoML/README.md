# BentoML 更新報告 - 2024-04-12

根據收到的郵件內容，重要的更新內容如下：



1. **錯誤修復：**

   在名為`Service`的類別中，使用`PILImage`時遇到問題，無法使用`Content-Type: image/jpeg`，需要改為`Content-Type: multipart/form-data`。在嘗試使用`@bentoml.api(input_spec=Image())`時出現錯誤，提示`Image must be a class type`。這個問題需要解決以確保正確的圖片處理和API溝通。



2. **功能迁移：**

   嘗試將現有的代碼從舊的裝飾器`@bentoml.service`和`@bentoml.api`遷移到新的裝飾器，以利用引入的並發功能。在遷移過程中遇到問題，導致需要更改端點調用的`Content-Type`。這需要仔細檢查和調整以確保功能的順利遷移。



3. **討論議題：**

   有一個討論關於如何像FastAPI風格一樣調試BentoML應用程式的問題，詢問是否有使用新的`@bentoml.service`註釋的解決方法。這個議題可能需要進一步的研究和討論，以找到最佳的調試方法。



總的來說，專案目前主要集中在解決從舊裝飾器到新裝飾器的代碼遷移問題，包括修復圖片處理的錯誤和調整端點調用的`Content-Type`。同時，討論如何更有效地調試BentoML應用程式也是一個重要的議題。這些更新將有助於提升應用程式的效能和可靠性。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。