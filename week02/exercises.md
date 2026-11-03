# 第 2 週：命令列參數與第一個批次工作

**本週大問題：怎麼讓「改一個參數、看結果」變得便宜又不出錯？**

完整講解（理論與示範、例題、動畫）在學習站第 2 週頁面。這份檔案只列任務，答案寫進 `week02/notes.md`。

## 一、理論與示範（Day 1–3）
1. `runoff_cli.py`：`--help` 看參數與單位；`--k-hours 0.2 --out runs/bad` 看錯誤訊息與結束碼（`echo $?`／`$LASTEXITCODE`）。
2. 單位陷阱的修正：`--freq 10min` 與 `--freq 30min` 比較筆數、洪峰與退水檢查，用理論判斷修正是否成立（預期 8640 與 2880 筆）。
3. `batch.py`：跑兩次，說明第二次為什麼幾乎沒做事；讀 `already_done()`。
4. 管線：`ls runs | wc -l`、`grep -h peak_true runs/*/metrics.json`、`cat runs/*/config.json | grep seed | sort | uniq -c`。

## 二、例題（Day 4，學習站有完整解）
在 `GRID` 加入 `"noise": [0.04, 0.12]`。先預測組數、跳過數、`summary.csv` 列數，再實際跑，找出新舊結果混在一起的原因與修正方式。

## 三、變化題（Day 5）
1. 用 `--noise 0` 當基準，說明 `peak_obs` 比 `peak_true` 高多少（預設的 8% 相對誤差）、為什麼雜訊會讓洪峰系統性偏高。
2. 加入 `k_hours = 0.2`（會被參數檢查擋下），讓批次跑完其他組並列出失敗清單；決定失敗組要不要進摘要。
3. 請 AI 寫 `check_summary.py` 檢查「每組都有結果、沒有重複」，用例題那份 30 列的 summary 測它，指出它漏抓的地方。

## 四、回答大問題（Day 6）
在 `notes.md` 畫批次流程圖並說明：每一步防止哪種錯、新舊結果混在一起怎麼防、何時重跑全部。
閱讀摘要：`papers/output/2023_shen.md`。
