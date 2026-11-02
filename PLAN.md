# SciML 半年（26 週）訓練計畫：交接摘要

給新對話的 Claude 讀的背景。每週開一個新對話，從這裡接續。
本文件同時存在 claude.ai 專案「All About LLM」（`claude/sciml-plan.md`）與 GitHub repo（`PLAN.md`），兩邊內容保持一致。

## 目前待辦（下次對話先看這裡）
- **位置**：第 1 週 Day 3（pandas 統計＋報告圖，原 Day 3、4 已合併）。Day 4 改為「讓 AI 把取樣改成 30 分鐘，用筆數與物理檢查找出它漏改的地方」。
- **已完成**：Day 1；Day 2 的 Q1、Q2、Q3 都寫進 `week01/notes.md`。Q3 已用 `week01/seed_check.py` 實測，結論正確（只有分潮 comp 不受 seed 影響；固定 seed 是為了可重現）。
  Q1 的說法可再精確：除了 t 的單位，`n = days * 24` 也寫死了，30min 取樣時只模擬 30 天。學習站第 1 週講解已補上。
- **學習者自行做的事**：把 `make_tide()` 拆成 `make_constituents()` + `make_tide()`，圖上加了 M2、S2 子圖；`SEED` 目前是 50。
- **追蹤頁勾選落後**：db 只勾了 `w1d1c`，Day 2 實際已完成但未勾。
- **還沒做**：第 1 週 Day 3–6；第 2 週範例與講解已提前交付（`week02/`、學習站第 2 週）。

## 學習者背景
- 水文與海洋科學碩士；修過流體力學、流體動力學、水文學、水文分析。
- 碩論做 NSGA-II，之後沒再深究。
- Python 只會基礎語法；ML 懂理論，沒實際跑過；PDE 與數值模式熟悉度不高。
- 每天 1–1.5 小時。
- **目標職缺（2026-11-02 起）**：安瑟樂威（能源公司），技能盤點見 `jobs/anselorway-energy.md`。
  Must Have：數值模擬與物理判斷、自有基礎建設架構（PaaS/CaaS/FaaS）、GAI 協作與驗證。
  Should Have：空間資訊技術、資料分析、Python ETL、REST API。Nice to Have：ML 訓練與服務化、Fortran/C 等 legacy、MLOps、空間內插與地理統計。
  原本的 PINN/FNO 研究助理職缺已被取代，相關部分保留在 B、B2 階段。
- 興趣：PINN、最佳化。
- 在意 context window：每週開新對話，回覆保持精簡。

## 學習偏好（必須遵守）
- 語法可交給 AI，邏輯不外包；第一個月語法比重低。
- 做中學：每週先給可執行範例程式，學習者讀懂後做練習題。練習要包含「先預測再執行」與「讓方法失敗」。
- 每週至少一題「讓 AI 寫，再找出它錯在哪」（對應職缺 Must Have 3）。
- 物理量、專有名詞第一次出現時要先定義，不預設學習者已知（例如 M2、S2）。
- 每日閱讀：一週一份。階段 A、B、B2、I、J 讀學術論文（近五年為主，經典另標示）；階段 C–H 改讀官方文件、工程講義或經典系統論文。來源要用網路搜尋確認。
- 單一入口：所有教材集中在學習站，講解要簡潔、語意流暢、上下文連貫，必要時用動畫。
- 方便管理、追蹤進度。

## 存放位置
- **學習站（單一入口）**：https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL
  - 原始碼在 repo 的 `site/`：`index.html`（26 週資料、進度、動畫引擎）＋ `content/wNN.html`（每週講解片段）。
  - 發布：Artifact publish，`url` 為上述網址，`file_path` = `site/index.html`，`files` 帶上所有 `content/wNN.html`。
  - 新增一週講解：寫 `site/content/wNN.html`，在 `index.html` 的 `W[NN-1]` 加上 `content:"content/wNN.html"`，需要新動畫就加進 `ANIMS`，然後重新發布。
  - db：collection `data/users/me`，doc `progress`。欄位：`start`、`done`（key `w{週}d{日}c` 練習、`w{週}d{日}p` 閱讀）、`notes`（`w{週}` → `{paper, fail}`）、`track`（舊欄位，保留不用）。
  - 讀取：ArtifactData `get`，url 如上，collection `data/users/me`，doc_id `progress`。
- **GitHub repo（正本）**：https://github.com/archi9882/SciML
  - `weekNN/`：範例程式與 `exercises.md`（Claude 放）＋學習者的 `notes.md` 與練習
  - `papers/input/`：論文 PDF（不進版控）；`papers/output/`：論文反芻（模板 `papers/output/TEMPLATE.md`）
  - 反芻後開新 session 讓 agent grill，期限為 `output_started` 起 21 天；流程見 `.claude/skills/verifying-paper-comprehension/SKILL.md`，`python papers/check.py` 列出剩餘天數
  - `reports/`：失敗案例報告（模板 `reports/TEMPLATE.md`）
  - `jobs/`：職缺技能盤點
  - `backups/progress.md`：學習站進度備份
- 開始日 2026-10-27。每週 6 天練習＋閱讀（第 6 天為本週產出），第 7 天休息。

## 26 週大綱（2026-11-02 第二版：壓縮拖沓單元，省下的 3 週補 Must Have 深度）
| 階段 | 週 | 主題 | 閱讀 |
|---|---|---|---|
| A 打底 | 1 | 讀懂資料處理程式：潮位時間序列（Day 3–4 合併，新增「讓 AI 改程式再抓錯」） | Kratzert 2019 HESS（經典） |
| | 2 | 命令列參數與第一個批次工作 | Shen 2023 Nat Rev Earth Env |
| B 數值方法與物理判斷 | 3 | FDM 1D 擴散：穩定性、收斂、批次掃描 Δx/Δt | Karniadakis 2021 Nat Rev Phys |
| | 4 | 對流與 Burgers＋可重現實驗框架（併入原第 5 週）；失敗報告 #1 | Raissi 2019 PINN（經典） |
| | 5 | **新增**：模式驗證 V&V，用實測潮位檢驗模型、誤差預算 | Oberkampf & Trucano 2002（經典） |
| | 6 | PyTorch autograd 與神經網路訓練 | Cuomo 2022 PINN 綜述 |
| | 7 | PINN 解擴散與對流，β 掃描；失敗報告 #2 | Krishnapriyan 2021 NeurIPS |
| B2 神經網路與 hybrid | 8 | 神經運算元入門：最小版 FNO 代理模型 | Li 2021 FNO |
| | 9 | **新增**：Hybrid，物理模型＋ML 殘差修正，三種做法比較 | Willard 2022 ACM CSUR |
| C 空間資訊與地理統計 | 10 | 計算幾何、拓撲、座標系統、mesh（原第 9、10 週合併） | SciPy spatial、Shapely 官方文件 |
| | 11 | 空間內插（IDW、克利金、spline）與假設 | Li & Heap 2014 EMS |
| D ETL 與資料工程 | 12 | 異質多源資料 ETL | pandas time series 官方文件 |
| | 13 | 資料品質監控與統計前提；失敗報告 #3 | Breck 2019 MLSys |
| V AI 協作與驗證 | 14 | **新增**：系統性指揮與否證 AI，錯誤案例庫與驗證檢查表 | Zhang 2024 LLM 程式幻覺 |
| E 自有基礎建設 | 15 | Linux 服務＋Docker 容器化（原第 14、15 週合併） | Docker 官方文件、MIT Missing Semester |
| | 16 | docker compose 多服務；PaaS/CaaS/FaaS 決策 | The Twelve-Factor App |
| | 17 | 審查 Kubernetes manifest；10 倍擴展評估；失敗報告 #4 | Kubernetes config best practices |
| F REST API 與模型服務 | 18 | FastAPI 格網查詢 API | FastAPI 官方教學 |
| | 19 | 模型服務化、pytest、GitHub Actions CI/CD | GitHub Actions 官方文件 |
| G MLOps 工具鏈 | 20 | MLflow 實驗追蹤與模型註冊、DVC | Sculley 2015 NeurIPS（經典） |
| | 21 | Prefect 編排、監控、漂移偵測 | Rabanser 2019 NeurIPS |
| H Legacy 科學程式碼 | 22 | 讀 Fortran 求解器、AI 翻譯審查、OpenMP | fortran-lang 官方教學 |
| I 最佳化回顧 | 23 | pymoo NSGA-II＋Optuna | Deb 2002 NSGA-II（經典） |
| J 選修：生成式設計 | 24 | SIMP 拓樸最佳化資料集 | Mazé & Ahmed 2023 AAAI |
| | 25 | 生成模型與物理檢驗；失敗報告 #5 | Giannone 2023 |
| K 作品集與面試 | 26 | 作品集、對照職缺準備實例、模擬面試 | Rules of ML（Google） |

單元之間的依賴（哪些週要用到前面的成果）畫在學習站首頁的「單元連動圖」，資料在 `site/index.html` 的 `DEPS`。
每週的每日任務、目標、職缺對照標籤寫在 `site/index.html` 的 `W` 陣列，以學習站為準。

## 每週交接流程
1. 學習者在新對話說「第 N 週進度」。
2. 讀學習站 db 的勾選與筆記；pull repo，看 `weekNN/notes.md`、`papers/output/`、`reports/`；給回饋。
3. 產出第 N+1 週（若尚未產出）：`weekNN/` 範例程式＋`exercises.md`（每日任務、先預測再執行、讓 AI 出錯的題目、週六產出），以及 `site/content/wNN.html` 講解（理論、程式導讀、必要時新增動畫），重新發布學習站。
4. 更新 `backups/progress.md`、本文件「目前待辦」與「進度紀錄」，同步到專案文件。

## 進度紀錄
- 2026-10-27：計畫建立，第 1 週範例（tide_example.py、exercises.md）已交付。
- 2026-10-27：建立 GitHub repo archi9882/SciML 作為正本；開始日提前至當天。
- 2026-10-28：追蹤頁加入「本週管制熱圖」。第 1 週 Day 2 Q1、Q2 完成；`papers/*.pdf` 加入 .gitignore。
- 2026-11-02：目標職缺改為安瑟樂威（`jobs/anselorway-energy.md`），計畫由 20 週改為 26 週；保留數值方法、PINN、神經網路基礎、生成式設計，新增空間資訊、ETL、自有基礎建設、REST API、MLOps、legacy 程式碼。
- 2026-11-02：計畫第二版：W1 Day 3–4 合併、原 W5 併入 W4、原 W9–10 合併、原 W14–15 合併；省下 3 週新增 W5 模式驗證、W9 Hybrid、W14 系統性驗證 AI。學習站首頁加入單元連動圖，參考來源收在頁末。
- 2026-11-02：追蹤頁改版為「SciML 半年學習站」（同一網址、進度保留），原始碼放 `site/`；第 1、2 週講解與 7 個動畫上線。第 2 週範例 `week02/tide_cli.py`、`batch.py`、`exercises.md` 提前交付。
