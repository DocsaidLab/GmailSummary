# BentoML 更新報告 - 2024-04-01

根據收到的郵件內容，這是一則關於BentoML專案的更新訊息。在這封郵件中，提到了一個新功能的需求，即暴露Prometheus Collector Registry客戶端選項。發件人在測試多個服務時遇到了一個問題，即因為處於同一進程中，出現了重複的Prometheus Collector Registry，而在測試中並不需要這些指標。因此，他建議配置並暴露此參數，以便在需要時啟用指標，以避免這個問題。



這則更新訊息主要針對解決重複Collector Registry的問題提出了一個新功能需求。該需求是為了避免在測試中出現不必要的指標，並提供了一種配置選項來啟用或禁用Prometheus Collector Registry客戶端。



這個功能的動機部分未提供具體內容，而其他部分也沒有進一步的回應。整體而言，這封郵件強調了在BentoML專案中解決重複Collector Registry問題的重要性，並提出了一個具體的解決方案。



這則更新訊息提到的主題是Issue #4626，可以在GitHub上查看更多詳細信息。這封郵件是由BentoML專案發出的，收件人收到此郵件是因為他訂閱了這個主題。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。