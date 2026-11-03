# 第 3 週：AI 成品交付，先看全貌

**本週大問題：這套系統由哪些部分組成，每一塊可能在哪裡出錯？**

完整講解在學習站第 3 週頁面。這份檔案只列任務，答案寫進 `week03/notes.md`，錯誤寫進 `week03/audit_log.md`。
成品在 `hydrowatch/`、`deploy/`、`legacy/`、`.github/`；先讀 `hydrowatch/README.md`。**不要先讀程式碼找答案。**

## 一、理論與示範（Day 1–5）
1. 照 README 跑 `python -m hydrowatch run` 與 `pytest`。遇到錯誤，先自己讀訊息最後幾行再問 AI。先看 `outputs/report.json` 有哪些區塊。
2. 畫架構圖：資料從哪來、經過哪些模組、輸出到哪裡。用 `grep -rn "^from hydrowatch\|^import hydrowatch" hydrowatch --include=*.py` 找呼叫關係。先對 `runoff_cli.py`、`batch.py` 練習輸入輸出表。
3. 每個模組寫一行：輸入、輸出、可能出錯的地方（單位、時間、邊界、切分、預設值）。
4. 用已知答案做第一次檢查：雨量與流量的水量平衡（降雨深度 × 流域面積 ≈ 流出水量）、退水常數 k、雨量與流量的合理範圍、鄰近雨量站的降雨應該大致同步、水力發電功率 P = ρgQHη 的量級、資料說明與程式讀法是否一致。
5. 建立 `week03/audit_log.md`：編號、模組、檔案:行、現象、證據、影響多大、狀態。

## 二、例題（Day 5，學習站有完整解）
把第 1 週「退水檢查差 4.6%」與第 2 週「summary 多出 10 列」各寫成一筆 audit 紀錄，分辨「排除」與「已確認」。

## 三、變化題（Day 4–5）
1. 跑之前先預測：5 個測站、30 天、每小時一筆，`report.json` 的 `n_hours` 應是多少、`quality` 哪些欄位預期是 0；跑完逐項比對。
2. `pytest` 全過代表系統正確嗎？讀測試內容，列出三件測試沒檢查、但出錯會影響結果的事。
3. 只把 `hydrowatch/` 的目錄結構給 AI，問「最可能出錯的五個地方」；跟你自己的清單並排，標出雙方各自漏掉的。

## 四、回答大問題（Day 6）
在 `notes.md` 與 `README.md` 寫：架構圖、模組表（輸入／輸出／可能出錯處）、audit_log.md 初版（至少 3 筆有證據，可含「排除」）。
閱讀摘要：`papers/output/2015_sculley.md`。
