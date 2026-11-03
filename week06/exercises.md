# 第 6 週：模式驗證

**本週大問題：模型跟真實世界差多少，差距來自哪裡？**

完整講解在學習站第 6 週頁面。這份檔案只列任務，答案寫進 `week06/notes.md`，錯誤寫進 `week03/audit_log.md`。
本週交付第二個成品 ChannelWatch（`channelwatch/`，先讀 `channelwatch/README.md`）。**不要先讀程式碼找答案。**

## 一、理論與示範（Day 1–4）
1. Verification 與 validation：各舉一個前幾週的例子。
2. 執行 `python week06/validation_example.py`，說明為什麼雨量被少量後 NSE 仍然很高。
3. 水位流量曲線：由實測擬合 Q = a h^b，比較範圍內與外插的誤差；說明 Manning 公式與 n 的來源。
4. 誤差預算：列出至少四項來源與大小，用方均根合成；用手算檢查水量與發電功率的量級。

## 二、例題（Day 4，學習站有完整解）
水位流量曲線外插到 2.0 m 少了 10.5%。拆成「形狀」與「實測誤差」兩個來源，分辨系統性與隨機的差別。

## 三、變化題（Day 5）
1. 把 `part1()` 的雨量縮放改成 0.8 與 0.4，預測率定出的 C 與驗證期 NSE，再執行。
2. 請 AI 寫 `fit_rating(df)`，不提示陷阱；先寫兩個檢查再執行，指出它漏掉的地方。
3. 審查 ChannelWatch 的 Manning 水深與 Froude 數、水位流量曲線與水躍，以及 HydroWatch 的率定與水庫發電量；每項先寫預期值與依據，記進 `audit_log.md`。

## 四、回答大問題（Day 6）
在 `notes.md` 與 `README.md` 寫一頁驗證報告：可信範圍、誤差預算表、審查結果。
閱讀摘要：`papers/output/2002_oberkampf.md`。
