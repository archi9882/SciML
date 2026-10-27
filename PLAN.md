# SciML 20 週訓練計畫：交接摘要

給新對話的 Claude 讀的背景。每週開一個新對話，從這裡接續。
本文件同時存在 claude.ai 專案「All About LLM」（`claude/sciml-plan.md`）與 GitHub repo（`PLAN.md`），兩邊內容保持一致。

## 目前待辦（下次對話先看這裡）
- **位置**：第 1 週 Day 2（`week01/exercises.md`），進度到 Q3 一半。
- **已完成**：Q1（t 的單位／取樣頻率）、Q2（S2_AMP 改 1.00 的預測）已寫進 `week01/notes.md` 並由 Claude 檢查過，兩題方向都對；
  Q1 的說法可以更精確（已給修正版解釋），Q2 可回頭用程式印出的理論值 `2*(M2_AMP-S2_AMP)` 驗證預測。
- **未完成**：Q3（改 SEED 看哪些數字變、哪些不變）只做了推理，還沒有實際跑程式比較。
  下次要做的具體動作：把 `SEED` 改成不同值跑兩次，印出並比較 `comp["m2"].head()`（應該不變）與 `eta.head()`（應該不同），
  驗證「只有雜訊受 seed 影響，分潮本身不受影響」，並更新 `notes.md` 裡 Q3 的答案與固定 seed 真正的理由（可重現性，而非「改變輸入變量」）。
- **學習者額外做的事**（非必做，記錄一下）：把 `make_tide()` 拆成 `make_constituents()` + `make_tide()`，並在圖上加了 M2、S2 分潮的子圖；`SEED` 目前已改成 50。
- **repo 整理**：`papers/*.pdf` 已加入 `.gitignore`（commit `beb06a1`），論文只存 5 行摘要，原始 PDF 留在本機。
- **還沒做**：Day 3（pandas 統計：`high_count`、`monthly_mean()`）、Day 4（三子圖＋畫圖檢查清單）、Day 5（手寫 `find_high_tides`）、Day 6（README＋論文摘要＋追蹤頁勾選）。

## 學習者背景
- 水文與海洋科學碩士；修過流體力學、流體動力學、水文學、水文分析。
- 碩論做 NSGA-II，之後沒再深究。
- Python 只會基礎語法；ML 懂理論，沒實際跑過；PDE 與數值模式熟悉度不高。
- 每天 1–1.5 小時。目標職缺：ML 加速物理模擬的研究助理（PINN／FNO／DeepONet／Graph Network、生成式設計、批次實驗、失敗案例報告、論文導讀）。
- 興趣：PINN、最佳化（透過 Kaggle 練習）。
- 在意 context window：每週開新對話，回覆保持精簡。

## 學習偏好（必須遵守）
- 語法可交給 AI，邏輯不外包；第一個月語法比重低。
- 做中學：每週先給可執行範例程式，學習者讀懂後做練習題。練習要包含「先預測再執行」與「讓方法失敗」。
- 每日論文閱讀：一週一篇，與當週練習密切相關；以近五年為主，經典論文另外標示。論文要用網路搜尋確認。
- 專題要多樣化。
- 方便管理、追蹤進度。

## 存放位置
- **GitHub repo（正本）**：https://github.com/archi9882/SciML
  - `weekNN/`：範例程式與 exercises.md（Claude 放）＋學習者的練習
  - `papers/`：論文 5 行摘要（學習者寫，模板 `papers/TEMPLATE.md`）
  - `reports/`：失敗案例報告（學習者寫，模板 `reports/TEMPLATE.md`）
  - `backups/progress.md`：追蹤頁備份（Claude 每週交接時更新）
  - `PLAN.md`：本文件
- **進度追蹤頁**：https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL
  - db：collection `data/users/me`，doc `progress`。欄位：`start`、`track`（選修專題 id）、`done`（key 格式 `w{週}d{日}c` 練習、`w{週}d{日}p` 論文）、`notes`（`w{週}` → `{paper, fail}`）。
  - 讀取：ArtifactData `get`，url 如上，collection `data/users/me`，doc_id `progress`。
- 開始日 2026-10-27（提前開始，原排程為週一到週五練習＋論文，週六本週產出，週日休息；之後幾週可依此順移）。

## 20 週大綱
| 階段 | 週 | 主題 | 論文 |
|---|---|---|---|
| A 打底 | 1 | 用 AI 協作寫 Python：潮位時間序列（範例已給） | Kratzert 2019 HESS（經典） |
| | 2 | 命令列參數與批次腳本 | Shen 2023 Nat Rev Earth Env |
| B 數值方法 | 3 | 有限差分 1D 擴散、穩定性、收斂 | Karniadakis 2021 Nat Rev Phys |
| | 4 | 1D 對流與 Burgers、數值擴散；失敗報告 #1 | Raissi 2019 PINN（經典） |
| | 5 | 批次實驗框架：參數掃描、可重現性、5 分鐘摘要 | PDEBench 2022 |
| C PINN | 6 | PyTorch autograd、MLP 擬合 | Cuomo 2022 PINN 綜述 |
| | 7 | PINN 解 1D 擴散，與 FDM 比較 | Wang 2020 gradient pathologies（經典） |
| | 8 | PINN 對流方程 β 掃描；失敗報告 #2 | Krishnapriyan 2021 NeurIPS |
| | 9 | loss 權重與 curriculum 改善 | Wang 2023 Expert's Guide |
| D 最佳化 | 10 | pymoo 重做 NSGA-II、hypervolume | Deb 2002 NSGA-II（經典） |
| | 11 | Kaggle Playground：LightGBM、CV vs LB | Grinsztajn 2022 |
| | 12 | Optuna 調參、剪枝 | Akiba 2019 Optuna（經典） |
| | 13 | 多目標最佳化調 PINN（精度 vs 時間） | Frazier 2018 BO 教學（經典） |
| E Neural Operator | 14 | 用求解器產生 Burgers 資料集 | Li 2021 FNO |
| | 15 | FNO 1D、解析度遷移 | Lu 2021 DeepONet |
| | 16 | DeepONet vs FNO；失敗報告 #3 | Sun 2023 FNO 淹水預報 |
| | 17 | 分佈外測試：方法極限一頁報告（進階：PDEBench／The Well 資料） | Pfaff 2021 MeshGraphNets |
| F 選修專題 | 18–19 | 五選一，見下表；失敗報告 #4 | 依專題 |
| | 20 | 作品集、論文導讀演練 | PINNacle 2024 |

## 選修專題（第 18–19 週，五選一）
**目前選擇：生成式設計（gen）**，學習者可在追蹤頁更改；以 db 的 `track` 欄位為準。

| 專題（id） | 對應 | 第 18 週 | 第 19 週 | 論文 |
|---|---|---|---|---|
| 淹水與淺水方程（flood） | 水文背景 | 1D SWE 潰壩 Lax–Friedrichs | PINN vs GNN 淹水模型 | Dazzi 2024 WRR；Bentivoglio 2023 HESS |
| 翼型 CFD 代理模型（cfd） | 流體／最貼近職缺 | AirfRANS 資料探索＋MLP 基準 | 誤差空間分佈、OOD 雷諾數 | Bonnet 2022 AirfRANS；Yagoubi 2024 ML4CFD |
| 逆問題（inverse） | 熱傳／地下水 | 2D 熱傳導正問題 FDM＋PINN | PINN 估 k(x,y)，掃感測器數與雜訊 | Cai 2021 J Heat Transfer；He 2020 AWR（經典） |
| 生成式設計（gen） | 最佳化 | SIMP 拓樸最佳化批次產生資料 | 條件 VAE／U-Net 生成＋compliance 檢驗 | Mazé & Ahmed 2023 AAAI；Giannone 2023 |
| 海洋與氣象 emulator（ocean） | 海洋背景 | WeatherBench 2 子集、persistence／climatology 基準 | 小型 FNO／U-Net、rollout 穩定性 | Rasp 2024 JAMES；Dheeshjith 2025 GRL Samudra |

cfd 與 ocean 資料量大，建議 Colab。20 週後可再選第二個專題。

## 每週交接流程
1. 學習者在新對話說「第 N 週進度」。
2. 讀追蹤頁 db 的勾選與筆記；pull repo，看 `papers/`、`reports/` 與當週練習；給回饋。
3. 視進度調整，產出第 N+1 週範例程式與 exercises.md（格式比照第 1 週：每日任務、先預測再執行、AI 使用規則、週六產出），commit 到 `weekNN/`。
4. 更新 `backups/progress.md`；必要時在本文件「進度紀錄」加一行，並同步到專案文件。

## 進度紀錄
- 2026-10-27：計畫建立，第 1 週範例（tide_example.py、exercises.md）已交付。
- 2026-10-27：第 18–19 週改為五選一選修專題（追蹤頁 v2）；學習者選擇生成式設計。
- 2026-10-27：建立 GitHub repo archi9882/SciML 作為正本。
- 2026-10-27：開始日提前至當天，追蹤頁與本文件同步更新。
- 2026-10-28：追蹤頁加入「本週管制熱圖」（練習／論文完成度一目了然）。
- 2026-10-28：第 1 週 Day 2 完成 Q1、Q2，Q3 待實際驗證（見上方「目前待辦」）；`papers/*.pdf` 加入 .gitignore。
