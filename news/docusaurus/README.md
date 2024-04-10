# docusaurus 更新報告 - 2024-04-11

根據收到的郵件內容，關於專案的重要更新如下：



1. **Issue #9880 - onBrokenAnchors reports spurious broken anchors**:

   使用者報告在建置網站時出現大量虛假的錨點錯誤，升級到 docusaurus 3.2 未解決問題。可能是由於其他依賴升級導致的。這個問題需要進一步的調查和修復。



2. **PR #10038 - Update intro.md**:

   包含了對 intro.md 的更新，引入了 Lighthouse 報告以評估部署預覽的性能、可訪問性、最佳實踐、SEO 等方面。同時提到了需要簽署貢獻者許可協議才能合併任何拉取請求的規定。



3. **PR #10037 - fix(theme-classic): Debounce during onRouteUpdate in classic theme**:

   解決了在嚴格模式下，連結轉換時進度條仍保留在頂部的問題。使用 debounce 取代 `window.setTimeout()` 來解決這個問題。同時提供了 Lighthouse 報告以評估部署預覽的性能等方面。



4. **Issue #10036 - When testing on StrictMode, the bar remains on the top**:

   描述了在嚴格模式下，連結轉換時進度條仍保留在頂部的情況。提供了重現步驟和預期行為，需要進一步的調查和修復。



5. **[facebook/docusaurus] chore(deps): bump semver from 7.3.4 to 7.6.0 (PR #10034)**:

   semver庫從版本7.3.4升級到7.6.0，主要功能是在強制轉換時保留版本的預發行和構建部分。包括Dependabot相關的工作。



以上是關於專案的重要更新摘要。這些更新涵蓋了錯誤修復、功能增加以及對於特定功能或錯誤的討論。這些訊息提供了對於專案進展和問題解決的洞察，有助於團隊更好地管理和改進專案。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。