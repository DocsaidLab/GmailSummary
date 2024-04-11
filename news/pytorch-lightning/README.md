# pytorch-lightning 更新報告 - 2024-04-12

根據收到的郵件內容，Lightning-AI/pytorch-lightning專案最新的重要更新如下：



1. **Release 2.2.2 - Patch release v2.2.2**:

   - 修復了使用`torch.compile`作為裝飾器時引起TypeError的問題，這是一個重要的錯誤修復，能夠改善程式碼的穩定性和可靠性。

   - 在Fabric中解決了多個問題，包括修復了保存FSDP分片檢查點時可能引起KeyError的問題，以及在使用FSDP時在`Fabric.setup()`中重置權重的問題。這些修復對於提高專案的功能性和效率至關重要。



2. **Legacy checkpoint test for version 2.2.2**:

   - 新增了對使用2.2.2版本創建的舊式檢查點的測試，這有助於確保舊版本的功能在新版本中仍然能夠正常運作。

   - 更新了教程以符合`2.2.2`版本，這有助於用戶更好地理解和應用最新版本的功能。



3. **Issue #18405 - KeyError in save_hyperparameters while using in a subclass**:

   - 對於在子類中使用時引起KeyError的問題進行了討論和解釋，提出了可能的解決方案並討論了可能的影響。這個議題的處理展示了專案團隊對於用戶反饋的重視和積極解決問題的態度。



4. **Issue #19745 - When calling trainer.test() train_dataloader is also validated, which makes no sense**:

   - 發現了一個錯誤，當在trainer中使用“deepspeed”策略時會出現問題，提供了相關的程式碼示例和解釋。這個問題的發現和解決反映了專案團隊對於持續改進和用戶體驗的關注。



這些更新顯示了專案團隊對於持續改進和修復的努力，以及對於用戶反饋的重視。通過解決問題、改進功能和提供更好的用戶體驗，專案不斷演進並為用戶提供更好的支持和工具。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。