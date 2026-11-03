# SciML 半年（26 週）訓練計畫：交接摘要

給新對話的 Claude 讀的背景。每週開一個新對話，從這裡接續。
本文件同時存在 claude.ai 專案「All About LLM」（`claude/sciml-plan.md`）與 GitHub repo（`PLAN.md`），兩邊內容保持一致。

## 目前待辦（下次對話先看這裡）
- **位置**：從第 1 週重新開始（2026-11-03 決定）。第 1–3 週的範例程式、`exercises.md`、`notes.md` 題目、學習站講解（`site/content/w01–w03.html`）與 TideWatch 成品已產出；`sealed-answer-key` 已寫入學習站 db（尚未重新發布學習站，w03 講解要發布後才看得到）。
- **學習站**：追蹤頁勾選以重新開始後的實際進度為準。
- **下一個里程碑**：第 3 週交接時批改 `audit_log.md` 初版（只公布已審查模組的答案）；第 4 週起每週審查一個模組（見下方）。

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
- **先地圖、再細節**：每週只有一個「大問題」，開頭先說它在大圖（TideWatch 資料流）的哪一格；所有練習都要能回答「不做這題會不會影響大問題的答案」，不能的就刪或降為延伸。
- **教學順序固定**：一、理論與示範（每個觀念附一個可跑的示範）→ 二、例題（完整逐步解，示範解題方法）→ 三、變化題（改條件／讓方法失敗／讓 AI 做再抓錯，提示與參考答案收合）→ 四、回答大問題（週六產出）。講解片段的 `data-day` 對應每日任務。
- 語法可交給 AI，邏輯不外包；第一個月語法比重低。
- 做中學：每週先給可執行範例程式，學習者讀懂後做練習題。練習要包含「先預測再執行」與「讓方法失敗」。
- 每週至少一題「讓 AI 寫，再找出它錯在哪」（對應職缺 Must Have 3）。
- 物理量、專有名詞第一次出現時要先定義，不預設學習者已知（例如 M2、S2）。
- 每日閱讀：一週一份。階段 A、B、B2、I、J 讀學術論文（近五年為主，經典另標示）；階段 C–H 改讀官方文件、工程講義或經典系統論文。來源要用網路搜尋確認。
- 單一入口：所有教材集中在學習站，講解要簡潔、語意流暢、上下文連貫，必要時用動畫。
- 方便管理、追蹤進度。
- 提問直接寫進筆記：Claude 提出練習或預測問題時，不只在對話中列出，而是直接寫進 `weekNN/notes.md` 對應的 `# DayN` 標題下。
  格式沿用既有筆記：`## Qn.` ＋題目，下一行留 `> ` 讓學習者填答。只新增題目，不修改學習者已寫的答案。

## 存放位置
- **學習站（單一入口）**：https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL
  - 原始碼在 repo 的 `site/`：`index.html`（26 週資料、進度、動畫引擎）＋ `content/wNN.html`（每週講解片段）。
  - 發布：Artifact publish，`url` 為上述網址，`file_path` = `site/index.html`，`files` 帶上所有 `content/wNN.html`。
  - 新增一週講解：依「理論與示範 → 例題 → 變化題 → 回答大問題」寫 `site/content/wNN.html`（大問題在 `Q` 陣列），在 `index.html` 的 `W[NN-1]` 加上 `content:"content/wNN.html"`，需要新動畫就加進 `ANIMS`，然後重新發布。
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

## 26 週大綱（2026-11-03 第三版：AI 先交成品，再逐塊拆解）

**方法**：第 1–2 週打底；第 3 週由 Claude 交付一套完整、能從頭跑到尾的潮汐監測系統 **TideWatch**（AI 原版）。
之後每個單元固定四步：學理論 → 審查成品的對應模組、找錯並寫證據 → 換成學習者自己驗證過的版本 → 確認整套系統仍能跑。
第 26 週把 AI 原版與最終版並排，附錯誤紀錄與抓錯率，作為作品集主軸。原第 23 週「最佳化回顧」拿掉以維持 26 週：Optuna 併入第 21 週，NSGA-II 併入第 24 週（拓樸最佳化的多目標權衡）。

| 階段 | 週 | 主題 | 審查成品的模組 | 閱讀 |
|---|---|---|---|---|
| A 打底 | 1 | 讀懂資料處理程式：潮位時間序列 | — | Kratzert 2019 HESS（經典） |
| | 2 | 命令列參數與第一個批次工作 | — | Shen 2023 Nat Rev Earth Env |
| S AI 成品交付 | 3 | 跑起來、畫架構圖、建立 `audit_log.md` | 全系統（只看輸入輸出） | Sculley 2015 NeurIPS（經典） |
| B 數值方法與物理判斷 | 4 | FDM 1D 擴散：穩定性、收斂、顯式與隱式格式的選擇、批次掃描 | transport（穩定條件） | Karniadakis 2021 Nat Rev Phys |
| | 5 | 對流與 Burgers＋可重現實驗框架；失敗報告 #1 | transport（數值擴散、邊界）→ **替換** | Raissi 2019 PINN（經典） |
| | 6 | 模式驗證 V&V：實測潮位、誤差預算 | harmonic → **替換** | Oberkampf & Trucano 2002（經典） |
| | 7 | PyTorch autograd 與神經網路訓練 | ml（訓練迴圈、資料洩漏） | Cuomo 2022 PINN 綜述 |
| | 8 | PINN 解擴散與對流，β 掃描；失敗報告 #2 | 判斷題：成品為何不用 PINN | Krishnapriyan 2021 NeurIPS |
| B2 神經網路與 hybrid | 9 | 神經運算元入門：最小版 FNO 代理模型 | ml（代理模型評估） | Li 2021 FNO |
| | 10 | Hybrid：物理模型＋ML 殘差修正 | ml → **替換** | Willard 2022 ACM CSUR |
| C 空間資訊與地理統計 | 11 | 計算幾何、拓撲、座標系統、mesh | spatial（座標、分割） | SciPy spatial、Shapely 官方文件 |
| | 12 | 空間內插（IDW、克利金、spline）與假設 | spatial → **替換** | Li & Heap 2014 EMS |
| D ETL 與資料工程 | 13 | 異質多源資料 ETL | ingest → **替換** | pandas time series 官方文件 |
| | 14 | 資料品質、統計前提、因果與實驗設計；失敗報告 #3 | quality → **替換** | Breck 2019 MLSys |
| V AI 協作與驗證 | 15 | 系統性否證 AI：錯誤分類、性質測試、檢查表 | 全系統掃描 | Zhang 2024 LLM 程式幻覺 |
| E 自有基礎建設 | 16 | Linux 服務＋Docker 容器化 | deploy（Dockerfile） | Docker 官方文件、MIT Missing Semester |
| | 17 | docker compose 多服務；PaaS/CaaS/FaaS 決策；自動維運與 runbook | deploy（compose、架構選擇） | The Twelve-Factor App |
| | 18 | Kubernetes manifest、10 倍擴展；失敗報告 #4 | deploy → **替換** | Kubernetes config best practices |
| F REST API 與模型服務 | 19 | FastAPI 格網查詢 API | api（介面、錯誤處理） | FastAPI 官方教學 |
| | 20 | 模型服務化、pytest、GitHub Actions CI/CD | api、ops（CI）→ api **替換** | GitHub Actions 官方文件 |
| G MLOps 工具鏈 | 21 | MLflow、DVC、Optuna 調參 | ops（實驗追蹤） | MLflow 官方文件、Akiba 2019 Optuna |
| | 22 | Prefect 編排、監控、漂移偵測 | ops → **替換** | Rabanser 2019 NeurIPS |
| H Legacy 科學程式碼 | 23 | 讀 Fortran 求解器、OpenMP | legacy（AI 翻譯）→ **替換** | fortran-lang 官方教學 |
| J 選修：生成式設計 | 24 | SIMP 拓樸最佳化資料集＋NSGA-II 多目標權衡 | — | Mazé & Ahmed 2023 AAAI、Deb 2002 |
| | 25 | 生成模型與物理檢驗；失敗報告 #5 | — | Giannone 2023 |
| K 作品集與面試 | 26 | AI 原版 vs 最終版、抓錯率、模擬面試 | 全系統比較 | Rules of ML（Google） |

成品模組、審查週與替換週的對照寫在 `site/index.html` 的 `MODS` 與 `AUD`。
單元之間的依賴（哪些週要用到前面的成果）畫在學習站首頁的「單元連動圖」，資料在 `site/index.html` 的 `DEPS`。
每週的每日任務、目標、職缺對照標籤寫在 `site/index.html` 的 `W` 陣列，以學習站為準。

## TideWatch 成品與答案保管
- **交付時機**：第 2 週交接時由 Claude 產生，放在 repo 的 `tidewatch/`、`deploy/`、`legacy/`、`.github/`（成品的 CI），附 README 與 `audit_log.md` 模板。
- **錯誤來源**：AI 自然寫錯的地方＋刻意埋的錯（單位、時區、投影、穩定條件、資料洩漏、統計前提、Dockerfile／manifest 地雷、Fortran 翻譯錯等），難度由淺到深，對應各審查週。
- **答案保管**：埋錯清單**不得**寫進 repo、PLAN.md、專案文件或任何學習者會打開的檔案。存在學習站 db：collection `data/users/me`，doc `sealed-answer-key`（頁面不讀取、不顯示）。用 ArtifactData `get` 讀取。
- **批改**：交接時學習者先交出 `audit_log.md` 裡找到的錯，Claude 再讀答案、只公布該週模組的部分，記錄抓錯率（已找到／該模組埋錯數，另計 AI 自然錯誤）。

## 每週交接流程
1. 學習者在新對話說「第 N 週進度」。
2. 讀學習站 db 的勾選與筆記；pull repo，看 `weekNN/notes.md`、`papers/output/`、`reports/`；給回饋。
3. 若本週有審查模組：先收學習者的 `audit_log.md`，再讀 `sealed-answer-key` 只公布該模組答案並記錄抓錯率。
4. 產出第 N+1 週（若尚未產出）：`weekNN/` 範例程式＋`exercises.md`（每日任務、先預測再執行、讓 AI 出錯的題目、週六產出），以及 `site/content/wNN.html` 講解（理論、程式導讀、必要時新增動畫），重新發布學習站。
5. 更新 `backups/progress.md`、本文件「目前待辦」與「進度紀錄」，同步到專案文件。

## 進度紀錄
- 2026-10-27：計畫建立。
- 2026-10-27：建立 GitHub repo archi9882/SciML 作為正本；開始日提前至當天。
- 2026-10-28：追蹤頁加入「本週管制熱圖」；`papers/*.pdf` 加入 .gitignore。
- 2026-11-02：目標職缺改為安瑟樂威（`jobs/anselorway-energy.md`），計畫由 20 週改為 26 週；保留數值方法、PINN、神經網路基礎、生成式設計，新增空間資訊、ETL、自有基礎建設、REST API、MLOps、legacy 程式碼。
- 2026-11-03：教學格式改為「一週一大問題＋理論與示範 → 例題 → 變化題 → 回答大問題」；學習站首頁最上方加入大圖（TideWatch 資料流與「本週」位置），每週頁面顯示大問題與小地圖；第 1、2 週講解與 exercises.md 依新格式改寫。
- 2026-11-03：計畫第三版：改為「AI 先交成品、逐塊拆解」。新增第 3 週 TideWatch 交付，其後各單元加入審查與替換；拿掉原第 23 週最佳化回顧（Optuna 併入 W21、NSGA-II 併入 W24），維持 26 週。學習站首頁新增成品模組卡，審查週頁面顯示「本週審查成品」。
- 2026-11-02：計畫第二版：W1 Day 3–4 合併、原 W5 併入 W4、原 W9–10 合併、原 W14–15 合併；省下 3 週新增 W5 模式驗證、W9 Hybrid、W14 系統性驗證 AI。學習站首頁加入單元連動圖，參考來源收在頁末。
- 2026-11-03：進度重置，從第 1 週重新開始。
- 2026-11-04：依職缺條件重新檢驗後補強：TideWatch 新增測站分割（`spatial/partition.py`）與代理模型（`model/surrogate.py`）；W4 加入顯式與隱式格式比較；W14 併入因果推論與實驗設計；W17 加入自動維運與 runbook。W11 的多格式空間資料與 mesh generation 尚未補。
- 2026-11-03：產出第 1–3 週教材與 TideWatch 成品（`tidewatch/`、`deploy/`、`legacy/`、`.github/`、`tests/`），埋錯清單存入學習站 db 的 `sealed-answer-key`；第 3 週講解 `site/content/w03.html` 與 `week03/`（含 `audit_log.md` 模板）。
- 2026-11-02：追蹤頁改版為「SciML 半年學習站」（同一網址、進度保留），原始碼放 `site/`；第 1、2 週講解與 7 個動畫上線。
