# SciML 學習紀錄

從水文與海洋科學背景出發，用 20 週學習以機器學習加速物理模擬：PINN、多目標最佳化、Neural Operator，以及生成式設計。

每週的程式、論文摘要與失敗案例報告都記錄在這裡。

## 目錄

| 資料夾 | 內容 |
|---|---|
| `week01/` … `week20/` | 每週範例程式、練習題（`exercises.md`）與自己的練習 |
| `papers/` | `input/` 放論文 PDF，`output/` 放自己的反芻（模板 `output/TEMPLATE.md`）；流程與提示詞見 `papers/GRILL.md`，期限檢查用 `python papers/check.py` |
| `reports/` | 失敗案例報告：現行方法在哪裡預測不準、原因與佐證（格式見 `reports/TEMPLATE.md`） |
| `backups/` | 進度追蹤頁的勾選與筆記備份 |
| `PLAN.md` | 20 週計畫與交接摘要 |

## 進度

| 階段 | 週 | 主題 | 狀態 |
|---|---|---|---|
| A 打底 | 1–2 | Python 協作、批次腳本 | 進行中 |
| B 數值方法 | 3–5 | 有限差分、Burgers、批次實驗框架 | |
| C PINN | 6–9 | PyTorch、PINN、失敗模式與改善 | |
| D 最佳化 | 10–13 | pymoo、Kaggle、Optuna、多目標調 PINN | |
| E Neural Operator | 14–17 | 資料集、FNO、DeepONet、分佈外測試 | |
| F 選修專題 | 18–19 | 生成式設計：拓樸最佳化 | |
| | 20 | 作品集與論文導讀 | |

## 讀論文的步驟

詳細規則與提示詞見 [papers/GRILL.md](papers/GRILL.md)。

1. 把 PDF 放進 `papers/input/`，檔名 `年份_第一作者.pdf`，例如 `2019_kratzert.pdf`。
2. 執行 `python papers/check.py`，確認這篇出現在「待開始」。
3. 自己先讀。需要查符號、資料、名詞時，請 agent 讀指定的 PDF（每次最多 20 頁，長論文請指定頁碼範圍）；摘要由自己寫，不讓 agent 代寫。
4. 複製 `papers/output/TEMPLATE.md` 為 `papers/output/年份_第一作者.md`，填 5 行摘要與「我還不懂的地方」，並填入 `output_started`（YYYY-MM-DD）。**21 天的討論期限從這天開始計算。**
5. 寫完第一版，開一個新 session，貼上 `papers/GRILL.md` 的提示詞，讓 agent 持續提問直到弄懂。
6. 每次討論後，把修正寫進 output 的「Grill 之後的修正」。
7. 弄懂了就把 `status` 改成 `done`；超過 21 天則結束討論，未弄懂的點帶去導讀時問大家。
8. 隨時用 `python papers/check.py` 查看各篇的剩餘天數。

## 執行環境

```bash
pip install numpy pandas matplotlib
python week01/tide_example.py
```
