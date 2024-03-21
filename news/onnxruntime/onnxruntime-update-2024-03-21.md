# onnxruntime 更新報告 - 2024-03-21

根據最近的郵件內容，這段時間在Microsoft Onnxruntime專案中發生了多個重要事件和動態：



### 主要活動和更新：

- **性能優化：**

   - PR #19985新增了一個端對端性能測試腳本，用於評估LLaMA-2等大型語言模型的性能。

   - PR #19830移除了MPI依賴，改用NCCL進行集體運算，從而提升效率。

  

- **功能新增和修復：**

   - PR #19945添加了TP和Mixtral MoE功能，並修正了orttraining管道的問題。

   - PR #19926更新了ORT Web變更的1.17.3 cherry-picks，提升Web功能的穩定性。

   - PR #19984修正了Min和Max操作中的NaN操作數據，確保計算精確性。

  

- **錯誤修復和討論：**

   - 解決了由CUDA版本不相容導致的問題，建議重新安裝onnxruntime-gpu以避免錯誤。

   - 討論了Java 11的支援問題，需要進行深入調查和修正。



### 相關專有名詞延伸說明：

- **LLaMA-2：** 大型語言模型，利用ONNX Runtime進行加速推理。

- **MoE：** Mixture of Experts，一種神經網絡結構，結合多個專家模型以提高性能。

- **CUDA：** NVIDIA的並行運算平台和應用程式程式介面，用於加速計算。

- **NCCL：** NVIDIA Collective Communications Library，用於高效率的集體通信操作。

- **MPI：** Message Passing Interface，用於在多個進程間進行通信和數據交換。



這些事件反映了專案團隊在持續優化性能、新增功能和解決問題方面的努力，並且表現了對專案的積極參與和專業知識的運用。這些改進將有助於提高Onnxruntime的功能性和效能，同時提供更好的用戶體驗。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。