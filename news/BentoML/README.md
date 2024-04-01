# BentoML 更新報告 - 2024-04-02

根據收到的郵件內容，BentoML 專案最近的重要更新包括以下幾點：



1. **Issue #4631 - Trouble in saving the Keras model to the Bentoml model store**:

   一位使用者在 Windows 11 桌面上遇到了保存 Keras 模型到 Bentoml 模型存儲庫時的問題。當使用 `bentoml.keras.save_model` 時出現了 `ValueError`，指出某些參數不被支持。這可能是由於 bentoml._internal.frameworks.keras 庫中的 bug 所導致。這個問題的解決將有助於提高模型保存的穩定性和可靠性。



2. **PR #4628 - docs: Add workers doc**:

   這個 PR 新增了有關如何配置和分配 workers 的文檔。文檔詳細解釋了如何使用 `workers` 參數來設置工作人員的數量，並提到了每個工作人員將模型加載到內存中的注意事項。同時，文檔還提到了如何調整並配置工作人員以有效利用底層硬件加速器，如 CPU 和 GPU。這將有助於用戶更好地管理和優化模型的運行環境。



3. **PR #4627 - fix: issue overriding default service config from config file**:

   這個 PR 解決了從配置文件覆蓋默認服務配置的問題。通過修復相關問題，提高了服務的配置靈活性和準確性。這將使用戶能夠更靈活地定制服務配置，以滿足不同需求和場景的應用。



這些更新涉及到模型保存問題的修復、文檔的增加以及服務配置的改進，對於 BentoML 專案的進一步發展和用戶體驗都具有重要意義。這些改進將有助於提高專案的穩定性、功能性和靈活性，為用戶提供更好的工具和支持。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。