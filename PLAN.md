# SciML 半年（26 週）訓練計畫：交接摘要

給新對話的 Claude 讀的背景。每週開一個新對話，從這裡接續。
本文件同時存在 claude.ai 專案「All About LLM」（`claude/sciml-plan.md`）與 GitHub repo（`PLAN.md`），兩邊內容保持一致。

## 目前待辦（下次對話先看這裡）
- **位置**：從第 1 週重新開始（2026-11-03 決定），專案情境為水力工程（2026-11-04）。第 1–3 週的範例程式、`exercises.md`、`notes.md` 題目與 HydroWatch 成品已產出，`sealed-answer-key` 已重建；學習站講解（`site/content/w01–w03.html`）、動畫與計畫資料已同步為水力工程版。
- **學習站**：追蹤頁勾選以重新開始後的實際進度為準。
- **計畫第四版（2026-11-04）**：前段 W1–14 HydroWatch（水文）學會方法，後段 W15–26 VPPWatch（虛擬電廠，對準安瑟樂威）再走一次完整循環。週次編號自 W8 起改變，見下方大綱；學習站與本文件已同步。
- **講解進度**：已有講解、範例、練習的週次為 1–6。其餘 7–26 週待寫。
- **明天（2026-11-05）待辦**：
  1. 第 7 週（PyTorch autograd 與訓練迴圈）：範例 `week07/`、講解 `site/content/w07.html`、`exercises.md`、`notes.md`；審查 `hydrowatch/model/ml.py` 的標準化、切分與資料洩漏。
  2. 第 8 週（PINN 與失敗模式，延伸最小版 FNO）、第 9 週（hybrid），順序同上；torch 已安裝（CPU 版）。
  3. 每個模組的講解都照四步寫：先預測該滿足什麼 → 親手做最小版 → 拿前兩步當基準審查 AI 版 → 替換並記錄。
  4. 第 1–14 週的講解頁要附「本週小基建任務」（資料在 `site/index.html` 的 `INF` 陣列）。
  5. 每週寫完後：跑範例確認數字、更新 `site/index.html` 的 `content` 欄位、重新發布學習站、commit 與 push。
  6. 未完成的先留在下面的「待辦（依序）」。
  7. W15–26 的閱讀連結是依記憶填入、尚未上網確認（特別是台電電力交易平台網址），寫該週講解時先查證。W3、W6 講解內文仍是舊週次編號，寫到時順手修正。
- **待辦（依序）**：
  1. 套件已核准安裝（torch、scipy、shapely、scikit-learn、fastapi、uvicorn、httpx、mlflow、optuna、pymoo）；裝好後寫第 7–12 週、第 24–25 週。Prefect 與 DVC 另行評估。
  2. 目前環境就能寫的週次：13、14、15、23、26（pandas、pytest、gfortran 都有）。
  3. 第 16–18 週（Docker、compose、Kubernetes）：使用者安裝 Docker 時遇到阻礙，目前這台電腦沒有 docker、kubectl。先寫成「審查型」練習（讀 Dockerfile 與 manifest 找地雷），指令與輸出標示為未實際執行驗證；待 Docker 可用再補驗證。
  4. 第 19–22 週：fastapi、mlflow、optuna 裝好後驗證；Prefect、DVC 另行評估。
- **Artifact 能力的結論（2026-11-04 實測）**：頁面可載入 pyodide.js 腳本，但 `fetch` 到 CDN 被 CSP 擋下，`loadPyodide` 無法完成，所以不能直接在學習站執行 Python。可能的替代是把 Pyodide 核心與所需套件檔一併發布為頁面的附屬檔案（相對路徑 fetch 可用，單檔上限 15 MB），需要下載 Pyodide 發行檔，尚未嘗試。Artifact 可做的：講解、動畫、進度與筆記（db）、審查紀錄表單、頁內 AI 問答（sample）、匯出檔案（downloads）；不能做：git、torch、Docker、Kubernetes、Fortran、啟動伺服器。
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
- **先地圖、再細節**：每週只有一個「大問題」，開頭先說它在大圖（HydroWatch 資料流）的哪一格；所有練習都要能回答「不做這題會不會影響大問題的答案」，不能的就刪或降為延伸。
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
  - db：collection `data/users/me`，doc `progress`。欄位：`start`、`done`（key `w{週}d{日}c` 練習、`w{週}d{日}p` 閱讀、`w{週}inf` 小基建任務、`iv-q{n}` 面試題）、`notes`（`w{週}` → `{paper, fail}`）、`ev`（證據庫陣列：`kind` 為 ai／adr／exp，另有 `title`、`cat`、`sys`、`week` 等欄位）、`score`（計分板：`hw`／`vpp` → `num`／`phys`／`infra` → `[抓到, 植入]`）、`track`（舊欄位，保留不用）。
  - 讀取：ArtifactData `get`，url 如上，collection `data/users/me`，doc_id `progress`。
- **GitHub repo（正本）**：https://github.com/archi9882/SciML
  - `weekNN/`：範例程式與 `exercises.md`（Claude 放）＋學習者的 `notes.md` 與練習
  - `papers/input/`：論文 PDF（不進版控）；`papers/output/`：論文反芻（模板 `papers/output/TEMPLATE.md`）
  - 反芻後開新 session 讓 agent grill，期限為 `output_started` 起 21 天；流程見 `.claude/skills/verifying-paper-comprehension/SKILL.md`，`python papers/check.py` 列出剩餘天數
  - `reports/`：失敗案例報告（模板 `reports/TEMPLATE.md`）
  - `jobs/`：職缺技能盤點
  - `backups/progress.md`：學習站進度備份
- 開始日 2026-10-27。每週 6 天練習＋閱讀（第 6 天為本週產出），第 7 天休息。

## 26 週大綱（2026-11-04 第四版：HydroWatch 學方法，VPPWatch 再走一次）

**方法**：第 1–2 週打底；第 3 週交付 AI 寫好的 **HydroWatch**（W6 另交付 **ChannelWatch**），第 15 週交付虛擬電廠成品 **VPPWatch**。
每個模組固定四步：**先預測**它該滿足什麼 → **親手做最小版** → 拿前兩步當基準**審查 AI 版**、找錯並寫證據 → **替換並記錄**，確認整套系統仍能跑。
W14 揭曉 HydroWatch 前段模組的答案卷，W26 揭曉 VPPWatch 與 HydroWatch 後段模組（deploy、api、ops、legacy），兩份抓錯率並排比較，作為作品集主軸。
第三版到第四版拿掉的：ChannelWatch 的獨立審查週（併入 W6、W14）、W24–25 生成式設計選修、FNO 獨立週（併入 W8）。
前段 W1–14 每週另有一項約 30 分鐘的小基建任務（`INF` 陣列）。

| 階段 | 週 | 主題 | 審查成品的模組 | 閱讀 |
|---|---|---|---|---|
| A 打底 | 1 | 讀懂資料處理程式：降雨逕流時間序列 | — | Kratzert 2019 HESS（經典） |
| | 2 | 命令列參數與第一個批次工作 | — | Shen 2023 Nat Rev Earth Env |
| S HydroWatch 交付 | 3 | 跑起來、畫架構圖、建立 `audit_log.md` | 全系統（只看輸入輸出） | Sculley 2015 NeurIPS（經典） |
| B 數值方法與物理判斷 | 4 | FDM 1D 擴散：穩定性、收斂、顯式與隱式 | routing（穩定條件） | Karniadakis 2021 Nat Rev Phys |
| | 5 | 對流與 Burgers＋可重現實驗框架；失敗報告 #1 | routing → **替換** | Raissi 2019 PINN（經典） |
| | 6 | 模式驗證 V&V；交付 ChannelWatch | runoff、reservoir、channel → **替換** | Oberkampf & Trucano 2002（經典） |
| B2 神經網路與 hybrid | 7 | PyTorch autograd 與訓練迴圈 | ml（訓練迴圈、資料洩漏） | Cuomo 2022 PINN 綜述 |
| | 8 | PINN 失敗模式；延伸：最小版 FNO 代理模型；失敗報告 #2 | ml（代理模型評估） | Krishnapriyan 2021、Li 2021 FNO |
| | 9 | Hybrid：物理模型＋ML 殘差修正 | ml → **替換** | Willard 2022 ACM CSUR |
| C 空間資訊與地理統計 | 10 | 計算幾何、拓撲、座標系統 | spatial（座標、分割） | SciPy spatial、Shapely 官方文件 |
| | 11 | 空間內插（IDW、克利金、spline）與假設 | spatial → **替換** | Li & Heap 2014 EMS |
| D 資料工程與統計 | 12 | 異質多源資料 ETL | ingest → **替換** | pandas time series 官方文件 |
| | 13 | 資料品質、統計前提、因果與實驗設計；失敗報告 #3 | quality → **替換** | Breck 2019 MLSys |
| V 否證 AI 與計分 | 14 | 錯誤分類、prompt 策略、性質測試、檢查表；**揭曉前段答案卷** | HydroWatch＋ChannelWatch 全系統 | Zhang 2024、Jia & Harman 2011（經典） |
| P VPPWatch 交付與串流 | 15 | VPPWatch 交付與植錯；讀台電即時備轉與需量反應規則 | 全系統（第一輪掃描） | 台電電力交易平台 |
| | 16 | 串流遙測：MQTT、TimescaleDB | telemetry → **替換** | MQTT 5.0 規格 |
| E 自有基礎建設 | 17 | Linux 服務、Docker、備份與還原演練 | VPP deploy＋HW deploy（Dockerfile） | Docker 官方文件、MIT Missing Semester |
| | 18 | compose 多服務；自架或託管 ADR；runbook | VPP deploy＋HW deploy（compose） | The Twelve-Factor App |
| M 能源模型與市場 | 19 | 光電物理、hybrid、日射量內插（移植前段方法） | pv → **替換** | Holmgren 2018 pvlib JOSS |
| | 20 | 儲能 SoC、貨櫃 2D 熱傳導；Fortran 參考實作；失敗報告 #4 | storage、HW legacy → **替換** | LeVeque 2007、fortran-lang |
| | 21 | 需量反應基準負載的因果實驗 | dr → **替換** | Abadie 2010 JASA（經典） |
| | 22 | 儲能日前投標：NSGA-II 三目標 | bid → **替換** | Xu 2018 TPWRS、Deb 2002 |
| O 平台、服務與維運 | 23 | K8s manifest、10 倍壓力測試、故障演練 | VPP deploy＋HW deploy（k8s）→ **替換** | Kubernetes config、Google SRE postmortem |
| | 24 | REST API、模型服務化、CI/CD | VPP api＋HW api、CI → **替換** | FastAPI、GitHub Actions 官方文件 |
| | 25 | MLflow、DVC、Prefect、漂移偵測 | VPP ops＋HW ops → **替換** | MLflow 官方文件、Rabanser 2019 |
| K 作品集與面試 | 26 | **揭曉後段答案卷**，兩份抓錯率並排；模擬面試 | 全系統比較 | Rules of ML（Google） |

成品模組、審查週與替換週的對照寫在 `site/index.html` 的 `MODS` 與 `AUD`。
單元之間的依賴（哪些週要用到前面的成果）畫在學習站首頁的「單元連動圖」，資料在 `site/index.html` 的 `DEPS`。
每週的每日任務、目標、職缺對照標籤寫在 `site/index.html` 的 `W` 陣列，以學習站為準。

## HydroWatch 成品與答案保管
- **交付時機**：第 2 週交接時由 Claude 產生，放在 repo 的 `hydrowatch/`、`deploy/`、`legacy/`、`.github/`（成品的 CI），附 README 與 `audit_log.md` 模板。
- **錯誤來源**：AI 自然寫錯的地方＋刻意埋的錯（單位、時區、投影、穩定條件、資料洩漏、統計前提、Dockerfile／manifest 地雷、Fortran 翻譯錯等），難度由淺到深，對應各審查週。
- **答案保管**：埋錯清單**不得**寫進 repo、PLAN.md、專案文件或任何學習者會打開的檔案。存在學習站 db：collection `data/users/me`，doc `sealed-answer-key`（頁面不讀取、不顯示）。用 ArtifactData `get` 讀取。
- **VPPWatch**：第 15 週交接時由 Claude 產生，放在 repo 的 `vppwatch/`，另由獨立 agent 植入數值、物理、基建三類錯誤；埋錯清單存入學習站 db 的 `sealed-answer-key-vpp`，規則同上。學習者的錯誤紀錄寫在 `audit_log_vpp.md`。
- **計分**：揭曉後把各類「抓到／植入」填進學習站首頁的抓錯率計分板（db `progress.score`）。
- **批改**：交接時學習者先交出 `audit_log.md` 裡找到的錯，Claude 再讀答案、只公布該週模組的部分，記錄抓錯率（已找到／該模組埋錯數，另計 AI 自然錯誤）。

## 每週交接流程
1. 學習者在新對話說「第 N 週進度」。
2. 讀學習站 db 的勾選與筆記；pull repo，看 `weekNN/notes.md`、`papers/output/`、`reports/`；給回饋。
3. 若本週有審查模組：先收學習者的 `audit_log.md`，再讀 `sealed-answer-key` 只公布該模組答案並記錄抓錯率。
4. 產出第 N+1 週（若尚未產出）：`weekNN/` 範例程式＋`exercises.md`（每日任務、先預測再執行、讓 AI 出錯的題目、週六產出），以及 `site/content/wNN.html` 講解（理論、程式導讀、必要時新增動畫），重新發布學習站。
5. 更新 `backups/progress.md`、本文件「目前待辦」與「進度紀錄」，同步到專案文件。

## 進度紀錄
- 2026-11-04：計畫第四版。前段 W1–14 HydroWatch、後段 W15–26 VPPWatch（虛擬電廠，對準安瑟樂威），兩套都走「預測 → 最小版 → 審查 → 替換」。W8 併入 FNO、拿掉 W24–25 生成式設計選修；新增 W15 VPPWatch 交付、W16 串流遙測、W19 光電、W20 儲能與熱傳導、W21 需量反應因果、W22 NSGA-II 投標、W23 壓測與故障演練。學習站首頁新增職缺覆蓋度矩陣、抓錯率計分板、證據庫（AI 錯誤、ADR、實驗）、面試題庫；W1–14 每週加小基建任務。HydroWatch 的 deploy、api、ops、legacy 改在後段與 VPPWatch 同週審查，答案於 W26 揭曉。
- 2026-10-27：計畫建立。
- 2026-10-27：建立 GitHub repo archi9882/SciML 作為正本；開始日提前至當天。
- 2026-10-28：追蹤頁加入「本週管制熱圖」；`papers/*.pdf` 加入 .gitignore。
- 2026-11-02：目標職缺改為安瑟樂威（`jobs/anselorway-energy.md`），計畫由 20 週改為 26 週；保留數值方法、PINN、神經網路基礎、生成式設計，新增空間資訊、ETL、自有基礎建設、REST API、MLOps、legacy 程式碼。
- 2026-11-03：教學格式改為「一週一大問題＋理論與示範 → 例題 → 變化題 → 回答大問題」；學習站首頁最上方加入大圖（HydroWatch 資料流與「本週」位置），每週頁面顯示大問題與小地圖；第 1、2 週講解與 exercises.md 依新格式改寫。
- 2026-11-03：計畫第三版：改為「AI 先交成品、逐塊拆解」。新增第 3 週 HydroWatch 交付，其後各單元加入審查與替換；拿掉原第 23 週最佳化回顧（Optuna 併入 W21、NSGA-II 併入 W24），維持 26 週。學習站首頁新增成品模組卡，審查週頁面顯示「本週審查成品」。
- 2026-11-02：計畫第二版：W1 Day 3–4 合併、原 W5 併入 W4、原 W9–10 合併、原 W14–15 合併；省下 3 週新增 W5 模式驗證、W9 Hybrid、W14 系統性驗證 AI。學習站首頁加入單元連動圖，參考來源收在頁末。
- 2026-11-03：進度重置，從第 1 週重新開始。
- 2026-11-04：專案情境由潮汐改為水力工程（流域降雨 → 逕流 → 河道洪水演算 → 水庫水量平衡與發電量），成品更名為 HydroWatch，W1–W3 的範例、練習與成品重做；埋錯清單重建（40 筆）。學習站講解與動畫尚未同步。
- 2026-11-04：第 6 週交付：講解 `site/content/w06.html`、範例 `week06/validation_example.py`、`exercises.md`、`notes.md`；本週交付第二個成品 ChannelWatch，審查 HydroWatch 的率定與水庫發電、ChannelWatch 的水深與水位流量曲線。
- 2026-11-04：補齊第 4、5 週：講解 `site/content/w04.html`、`w05.html`，範例 `week04/diffusion_fdm.py`、`week05/advection_burgers.py`、`exercises.md`、`notes.md`。已有講解的週次：1–6；尚未撰寫：7–26（其中 7–12、16–22、24–25 需要額外套件或工具，見對話記錄的清點）。
- 2026-11-04：參數改為以鯉魚潭水庫集水區為參考，逐項查證或推導，來源與假設見 `docs/parameters.md`、推導程式見 `scripts/derive_parameters.py`；資料期間改為 2026 年 8 月。新增第二個成品 ChannelWatch（明渠水力學：Manning 水深、水面線、水躍、水位流量曲線，`channelwatch/`），埋錯清單存入學習站 db 的 `sealed-answer-key-channel`（11 筆）；預計在第 6 週交接時交付，於第 6 週與第 15 週審查。HydroWatch 埋錯清單更新為 41 筆。
- 2026-11-04：依職缺條件重新檢驗後補強：HydroWatch 新增測站分割（`spatial/partition.py`）與代理模型（`model/surrogate.py`）；W4 加入顯式與隱式格式比較；W14 併入因果推論與實驗設計；W17 加入自動維運與 runbook。W11 的多格式空間資料與 mesh generation 尚未補。
- 2026-11-03：產出第 1–3 週教材與 HydroWatch 成品（`hydrowatch/`、`deploy/`、`legacy/`、`.github/`、`tests/`），埋錯清單存入學習站 db 的 `sealed-answer-key`；第 3 週講解 `site/content/w03.html` 與 `week03/`（含 `audit_log.md` 模板）。
- 2026-11-02：追蹤頁改版為「SciML 半年學習站」（同一網址、進度保留），原始碼放 `site/`；第 1、2 週講解與 7 個動畫上線。
