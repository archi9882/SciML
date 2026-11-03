# 第 5 週：對流與 Burgers 方程

**本週大問題：數值方法本身會造成哪些失真，怎麼系統性地找出它的邊界？**

完整講解在學習站第 5 週頁面。這份檔案只列任務，答案寫進 `week05/notes.md`，錯誤寫進 `week03/audit_log.md`。

## 一、理論與示範（Day 1–4）
1. 執行 `python week05/advection_burgers.py`；說明 upwind、CFL 數與下游零梯度邊界。
2. 數值擴散：用 D_num = a·dx·(1 − C)/2 預測高斯波的變異數，與輸出比對。
3. Burgers：改變 ν 與網格，觀察最大梯度；判斷哪些條件還沒收斂。
4. `solve(params)`：讀它的輸入與輸出，說明為什麼這個介面方便批次掃描與存檔。

## 二、例題（Day 4，學習站有完整解）
CFL = 0.5 時峰值降到 0.454：用公式預測，拆成格式與物理兩個來源。

## 三、變化題（Day 4–5）
1. 用第二段輸出判斷 ν = 0.05、0.01、0.002 各自的收斂網格，估計 ν = 0.002 需要多少格。
2. 請 AI 寫批次掃描 nx 與 cfl 的程式；先寫兩個檢查（變異數接近預測、同參數結果一致）再執行，指出錯在哪裡。
3. 審查 HydroWatch 的 `routing.py` 的數值擴散與邊界條件，對照 `legacy/reference_output.txt`；寫你自己的 `solve(params)` 並換進去。

## 四、回答大問題（Day 6）
在 `notes.md` 回答大問題，並完成失敗案例報告 #1（`reports/`，格式見 `reports/TEMPLATE.md`）。
閱讀摘要：`papers/output/2019_raissi.md`。
