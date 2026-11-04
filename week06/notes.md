**本週大問題：模型跟真實世界差多少，差距來自哪裡？**

講解：學習站第 6 週（https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL#w6）。題號與講解的「筆記 Day N・Qn」一致，答案寫在每題下方的 `> ` 之後。
閱讀摘要：`papers/output/2002_oberkampf.md`
<!-- 題目由 python scripts/sync_questions.py 從學習站講解產生；改題目請改講解再重跑 -->

# Day1
## Q1.
各舉一個前幾週的例子，說明什麼是 verification、什麼是 validation。
> 

# Day2
## Q1.
執行 `python week06/validation_example.py`。雨量只量到 60% 時，$C$ 被調成多少？為什麼 NSE 仍然很高？
> 

# Day3
## Q1.
手算：寬 20 m、坡降 0.004、$n = 0.04$ 的矩形河道，$Q = 60$ m³/s 的正常水深（用 $h = \left(q\,n/\sqrt{S}\right)^{3/5}$）。
> 

# Day4
## Q1.
列出你的誤差預算：至少四項來源、大小與依據，並用方均根合成。
> 

## Q2.
例題：水位流量曲線外插到 2.0 m，比 Manning 少 10.5%。是資料不夠，還是方法的問題？請拆出來源，並各自估計大小。
> 

# Day5
## Q1.
變化 1：雨量被少量，$C$ 會怎麼變：在 `part1()` 把雨量縮放改成 0.8 與 0.4，先預測率定出來的 $C$ 與驗證期 NSE，再執行。$C$ 的值落在哪裡？有沒有碰到格點的邊界？
> 

## Q2.
變化 2：讓 AI 寫水位流量曲線，用外插抓錯：請 AI 寫一個 `fit_rating(df)`，由 `stage` 與 `discharge` 兩欄擬合曲線並回傳外插到 2.0 m 的流量。不要提示任何陷阱。先寫好兩個檢查再執行：實測範圍內的誤差、已知答案的外插值（用本週範例的 Manning 真值）。它通過嗎？有沒有告訴你外插風險？
> 

## Q3.
變化 3：審查成品，寫進 audit_log.md：這是本週的主要練習。對下面三塊各做一次「手算已知答案 → 跟程式比較 → 差距拆成來源」，每發現一項就記進 `audit_log.md`（含證據與影響大小，查過沒問題的也要記為「排除」）：
- **ChannelWatch 的 Manning 水深與 Froude 數**：讀 `channelwatch/sample_data/README.md` 的河床描述，查 Chow 表選 $n$，手算 $Q = 100$ m³/s 的正常水深與流速，再跟 `python -m channelwatch run` 的報告比較。
- **ChannelWatch 的水位流量曲線與水躍**：對照實測資料的單位與範圍；手算水躍的共軛水深。
- **HydroWatch 的率定與水庫發電量**：看 `report.json` 的 `runoff` 與 `reservoir`，檢查率定怎麼評分、發電功率與水量平衡的量級。
> 

# Day6
## Q1.
本週大問題：模型跟真實世界差多少，差距來自哪裡？
至少包含：
- **可信範圍**：模型在哪些條件下可採信，哪些不行（例如水位流量曲線只在實測範圍內）。
- **誤差預算表**：至少四項來源，各自的大小與依據，以及合成後的總誤差。
- **審查結果**：`audit_log.md` 中本週三塊的紀錄，每筆都有證據與影響大小。
> 
