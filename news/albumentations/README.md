# albumentations 更新報告 - 2024-04-09

Albumentations團隊最近針對其專案進行了一系列重要更新。首先，他們修復了一個關於多個關鍵點增強功能的錯誤（Issue #1638）。該問題導致當使用`add_targets`方法添加額外目標時，第二個關鍵點的角度出現錯誤。團隊承認了這個問題並表示將在未來幾個小時內解決。同時，他們建議用戶使用`additional_targets`參數來添加額外目標，而非`add_targets`方法。



其次，Albumentations團隊改進了RandomShadow的介面（Issue #1632）。他們新增了`num_shadows_limit`參數，並修復了類型錯誤，同時更新了相關的測試以確保新參數的正常運作。這些改進將提高RandomShadow轉換的效能和可靠性。



最後，團隊優化了性能和技術債務（Issue #1606）。他們合併了一個名為`add_weighted`的功能，以取代`mix_arrays`，並將其合併到主分支中。這項改進不僅提高了功能的性能，還解決了技術債務問題。特別感謝@gogetron的貢獻。



這些更新顯示Albumentations團隊致力於改進和優化其圖像增強庫，以提供更好的功能和性能。他們積極回應用戶反饋，解決問題並持續改進產品，以滿足用戶的需求和期望。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。