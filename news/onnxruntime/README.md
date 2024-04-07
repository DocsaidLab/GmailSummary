# onnxruntime 更新報告 - 2024-04-08

根據收到的郵件內容，有關專案更新的重要資訊如下：



在專案「microsoft/onnxruntime」中，關於 Issue #19603，提到了缺少 onnxruntime_providers_tensorrt for cuda 12 builds 的問題，需要相關人員提供更新。這個問題對 CUDA 12 版本的構建造成了影響，需要解決缺少提供者的問題。另外，PR #20154 則是關於支持每通道量化權重的功能增加，@adrianlizarraga 推送了相應的提交，這將對 QNN 功能帶來改進。



在另一個分支中，也是在專案「microsoft/onnxruntime」中，有關 PR #19974 的更新顯示使用者「satyajandhyala」推送了一系列提交，旨在優化 MatMulNBits 的性能，包括改進性能、修復錯誤、格式調整等。這些更改旨在進一步改進 MatMulNBits 的性能和功能。此外，另一個更新是關於 PR #20163，使用者「liqunfu」推送了一個提交，對4位CPU進行了改進，調整了子塊的長度並優化了AVX512和AVX2的性能，帶來了約20%的改進。



這些更新顯示了團隊在持續改進和優化不同專案中的努力，以提高性能、修復錯誤並增加功能。這些努力將有助於提升產品質量和用戶體驗。延伸說明：CUDA 是 NVIDIA 開發的一種並行運算平台和應用程式程式設計介面。QNN 是指量化神經網絡（Quantized Neural Networks），是一種將神經網絡權重和激活值轉換為低精度表示的技術，以節省計算和存儲空間。MatMulNBits 是指矩陣乘法（Matrix Multiplication）的 N 位版本，用於計算矩陣相乘的運算。 AVX512 和 AVX2 則是 Intel 開發的指令集擴展，用於提高 CPU 運算性能。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。