# albumentations 更新報告 - 2024-04-10

根據收到的郵件內容，Albumentations專案最新的重要更新內容如下：



首先，專案修復了一個問題，即在使用`CoarseDropout`時，即使設置`remove_invisible=False`也會刪除關鍵點。為了解決這個問題，用戶提供了一個解決方法，即在`A.Compose`中使用`keypoint_params=A.KeypointParams(format='xy', remove_invisible=False)`，並通過將`apply_to_keypoints`設置為`A.NoOp()`來解決這個問題。



其次，另一個重要更新是關於修復`add_target`介面的問題。在這個修復中，將`additional_targets`和`transforms`的初始化移至基類，並將`additional_targets`設置為私有。同時，添加了一個`get_supported_keys`方法來返回支持的鍵列表。然而，一些評論者指出這個修改增加了複雜性，建議簡化實現以減少複雜性。



最後，一個關於對輸入進行檢查的草稿被提出，但目前與`Replay`存在衝突。該草稿包括了一些新的方法和修改，以確保輸入數據的一致性和正確性。



總的來說，Albumentations團隊在不斷努力解決問題，改進功能，並提出新的想法來提高庫的效能和易用性。他們積極回應用戶的反饋，並致力於不斷改進和創新。這些更新顯示了團隊對於提升Albumentations專案品質和功能的承諾，同時也展示了他們對於解決技術挑戰和持續改進的決心。這些努力將有助於提升用戶體驗，並使Albumentations成為一個更加強大和可靠的圖像增強庫。



---



以上報告由 OpenAI GPT-3.5 Turbo 模型自動生成。