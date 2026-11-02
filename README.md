# SciML 學習紀錄

從水文與海洋科學背景出發，用 26 週（半年）補齊能源產業數值模擬職缺所需的能力：數值模擬與物理判斷、空間資訊與地理統計、ETL、自有基礎建設、REST API、MLOps，以及驗證 AI 產出的判斷力。

**學習入口**：[SciML 半年學習站](https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL)（每週講解、程式導讀、動畫、每日任務與進度）。原始碼在 `site/`。

每週的程式、論文摘要與失敗案例報告都記錄在這裡。

## 目錄

| 資料夾 | 內容 |
|---|---|
| `week01/` … `week26/` | 每週範例程式、練習題（`exercises.md`）與自己的練習 |
| `papers/` | `input/` 放論文 PDF，`output/` 放自己的反芻（模板 `output/TEMPLATE.md`）；流程見 `.claude/skills/verifying-paper-comprehension/SKILL.md`，期限檢查用 `python papers/check.py` |
| `reports/` | 失敗案例報告：現行方法在哪裡預測不準、原因與佐證（格式見 `reports/TEMPLATE.md`） |
| `backups/` | 進度追蹤頁的勾選與筆記備份 |
| `PLAN.md` | 26 週計畫與交接摘要 |
| `site/` | 學習站原始碼：`index.html` 與每週講解 `content/wNN.html` |
| `jobs/` | 職缺技能盤點 |
| `pyflow/` | 獨立作品：Python 傳遞關係視覺化工具（見 `pyflow/README.zh-TW.md`） |

## 進度

| 階段 | 週 | 主題 | 狀態 |
|---|---|---|---|
| A 打底 | 1–2 | 讀懂資料處理程式、命令列與批次 | 進行中 |
| B 數值方法與物理判斷 | 3–7 | FDM、Burgers、批次實驗框架、PyTorch、PINN 與失敗模式 | |
| B2 神經網路延伸 | 8 | 神經運算元入門 | |
| C 空間資訊與地理統計 | 9–11 | Voronoi／Delaunay、拓撲與座標系統、空間內插 | |
| D ETL 與資料工程 | 12–13 | 異質資料 ETL、資料品質與統計前提 | |
| E 自有基礎建設 | 14–17 | Linux 服務、Docker、多服務架構決策、manifest 審查 | |
| F REST API 與模型服務 | 18–19 | FastAPI、模型服務化、CI/CD | |
| G MLOps 工具鏈 | 20–21 | MLflow、DVC、編排、監控與漂移 | |
| H Legacy 科學程式碼 | 22 | Fortran、OpenMP、AI 翻譯審查 | |
| I 最佳化回顧 | 23 | pymoo、Optuna | |
| J 選修：生成式設計 | 24–25 | 拓樸最佳化資料集、生成模型與物理檢驗 | |
| K 作品集與面試 | 26 | 作品集與模擬面試 | |

## 讀論文的步驟

詳細規則見 [verifying-paper-comprehension skill](.claude/skills/verifying-paper-comprehension/SKILL.md)。

1. 把 PDF 放進 `papers/input/`，檔名 `年份_第一作者.pdf`，例如 `2019_kratzert.pdf`。
2. 執行 `python papers/check.py`，確認這篇出現在「待開始」。
3. 自己先讀。需要查符號、資料、名詞時，請 agent 讀指定的 PDF（每次最多 20 頁，長論文請指定頁碼範圍）；摘要由自己寫，不讓 agent 代寫。
4. 複製 `papers/output/TEMPLATE.md` 為 `papers/output/年份_第一作者.md`，填 5 行摘要與「我還不懂的地方」，並填入 `week`（對應第幾週，1–20）與 `output_started`（YYYY-MM-DD）。**21 天的討論期限從這天開始計算。**
5. 寫完第一版，開一個新 session，說「grill 這篇」並給檔名（會觸發上述 skill），讓 agent 持續提問直到弄懂。
6. 每次討論後，把修正寫進 output 的「Grill 之後的修正」。
7. 弄懂了就把 `status` 改成 `done`；超過 21 天則結束討論，未弄懂的點帶去導讀時問大家。
8. 隨時用 `python papers/check.py` 查看各篇的剩餘天數。

## 執行環境

```bash
pip install -r requirements.txt
python week01/tide_example.py
python week02/batch.py
```
