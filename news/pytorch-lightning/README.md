# pytorch-lightning 更新報告 - 2024-04-08

根據收到的郵件內容，Lightning-AI/pytorch-lightning專案最近的重要更新包括錯誤修復、功能增加和討論議題。



首先，針對錯誤修復，專案團隊發現在使用pytorch lightning 2.2環境下轉換為torchscript並保存模型後，在不含pytorch lightning 2.2的環境中無法正確加載模型的問題。這導致了在C++部署中無法提供模型服務的困擾。為了暫時解決這個問題，建議降級到pytorch lightning 2.0版本，以確保模型能夠正確加載和運行。



其次，關於功能增加，有用戶提出希望能夠使用TensorBoard記錄直方圖的功能。為了支持這個需求，提出了在`LightningModule`中修改`log`方法以支持直方圖記錄的建議。目前的`LightningModule`類型檢查會阻止多維度的`Tensor`實例通過到`TensorBoardLogger`，因此提出了修改建議以支持直方圖記錄，這將為用戶提供更豐富的模型監控和分析功能。



最後，討論議題涉及到Lightning 2.2.1版本中`save_last`功能的不清晰性。文件描述了當`save_last`為True時會在每次保存檢查點時保存一個`last.ckpt`副本，但議題中的評論指出`last.ckpt`檢查點似乎在每個epoch單獨保存，與`save_top_k`檢查點分開。這引發了對於檢查點保存機制的討論和澄清，以確保用戶能夠正確理解和使用這一功能。



綜合來看，這些更新顯示了專案團隊對於持續改進和用戶需求的關注，同時也凸顯了在開源社區中進行討論和協作的重要性。這些更新將有助於提升專案的功能性和可靠性，同時也為用戶提供更好的使用體驗。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。