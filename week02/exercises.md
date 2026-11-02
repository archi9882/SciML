# 第 2 週：命令列參數與第一個批次工作

**本週目標**：把「改常數再手動跑」變成「用參數呼叫程式、批次跑、自動彙整」。這是排程、容器、API、MLOps 的共同起點。
**每天時間**：練習 45–60 分鐘 ＋ 閱讀 15–20 分鐘。
**本週閱讀**：Shen et al. (2023)，可微分模式：物理模式與 ML 如何結合（水文案例為主）。
**完整講解與動畫**：學習站第 2 週頁面。

範例程式：
- `tide_cli.py`：一次執行 = 一次實驗，設定存 `config.json`、結果存 `metrics.json`。
- `batch.py`：跑參數網格、跳過已完成的、彙整成 `summary.csv` 與 `summary.png`。

> **名詞**
> - **命令列參數（argument）**：執行程式時附在後面的設定，例如 `--s2-amp 0.45`。
> - **結束碼（exit code）**：程式結束時回報的數字。0 代表成功，非 0 代表失敗；批次系統只看這個數字判斷成敗。
> - **冪等性（idempotency）**：同一件事做一次或做很多次，結果都一樣。批次中斷後可以直接重跑，不會重複計算或弄亂結果。

---

## Day 1：讀 `tide_cli.py`，先預測再執行

1. 執行 `python tide_cli.py --help`，對照 `parse_args()`，說明每個參數的單位。
2. **先預測**：`python tide_cli.py --s2-amp 1.0 --out runs/test` 印出的 `min_range_m` 大約多少？寫下來再跑。
3. 執行 `python tide_cli.py --s2-amp -1 --out runs/bad`，再執行 `echo $?`（PowerShell 用 `$LASTEXITCODE`）。看到的數字是什麼？為什麼不是 0？

## Day 2：第 1 週的單位陷阱被修好了嗎

1. 找到 `t_hours` 那一行，用自己的話說明它跟第 1 週 `t = np.arange(n)` 的差別。
2. 分別用 `--freq h` 和 `--freq 30min` 執行，比較兩次的 `max_range_m`。應該接近還是差很多？
3. 把 `t_hours` 改回 `np.arange(len(time))`，再用 `--freq 30min` 跑一次。結果錯在哪？改完記得還原。

## Day 3：讀 `batch.py`，理解批次的四個步驟

1. 執行 `python batch.py`，再執行一次。第二次為什麼幾乎沒做事？找出負責的函式。
2. 打開任一個 `runs/` 資料夾，說明 `config.json` 和 `metrics.json` 各回答了什麼問題。
3. 在 `GRID` 加入 `"noise": [0.05, 0.3]`，重跑。總共幾組？先算再跑。

## Day 4：彙整與檢查

1. 打開 `summary.png`。實線（模擬）和虛線（理論）哪裡最接近、哪裡差最多？
2. `noise = 0.3` 時，`min_range_m` 比理論值大還是小？為什麼雜訊會讓「最小潮差」偏大？（提示：每日最高減最低）
3. 這就是一個「方法在什麼條件下會失準」的觀察，記到 `notes.md`。

## Day 5：Linux 基本操作（不用 AI 直接給答案，先自己查）

在 Git Bash 或 WSL 中完成，把指令和輸出記在 `notes.md`：

1. `ls runs | wc -l`：有幾個實驗資料夾？
2. `grep -h min_range runs/*/metrics.json`：一次看所有結果的最小潮差。
3. `cat runs/*/config.json | grep seed | sort | uniq -c`：每個 seed 出現幾次？
4. 用一句話說明 `|`（管線）在做什麼。

## Day 6（週末）：本週產出

1. 在 `notes.md` 畫一張批次流程圖（文字即可）：參數網格 → 送出工作 → 檢查結束碼 → 彙整 → 畫圖。
2. 寫本週閱讀的 5 行摘要（`papers/output/2023_shen.md`）。
3. 在學習站勾選完成並 push。

---

## 加分題

讓 `batch.py` 在某一組參數失敗時（例如 `s2_amp = -1`）繼續跑完其他組，最後回報失敗清單。想想看：失敗的那組，`summary.csv` 裡應該出現嗎？
