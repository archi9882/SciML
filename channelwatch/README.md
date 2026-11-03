# ChannelWatch（AI 原版）

明渠水力學成品：由實測流量建立水位流量曲線，算正常水深與臨界水深，推壅水水面線，並計算溢洪道下游的水躍。這份是 AI 寫好、能從頭跑到尾的原版，之後審查其中一塊、找出錯並寫下證據，再換成你自己驗證過的版本。

**不要先讀程式碼找答案。**

## 這套系統在做什麼

河道為矩形斷面（寬 30 m、坡降 0.01、卵石夾大塊石）。程式用 Manning 公式算設計洪水（100 m3/s）的水深，用標準步推法算堰前壅水的水面線，用 Bélanger 公式算溢洪道趾部的水躍，並用人工實測的水位與流量擬合水位流量曲線。

## 執行

在 repo 根目錄、已啟動 `.venv` 的狀態下：

```bash
python -m channelwatch run    # 結果印在螢幕並存到 outputs/channel/report.json
pytest                        # 跑測試
```

## 目錄

| 路徑 | 內容 |
|---|---|
| `channelwatch/hydraulics.py` | 斷面幾何、正常水深、臨界水深、Froude 數 |
| `channelwatch/profile.py` | 漸變流水面線 |
| `channelwatch/jump.py` | 水躍 |
| `channelwatch/rating.py` | 水位流量曲線 |
| `channelwatch/sample_data/` | 實測流量資料，格式見該資料夾的 README |

## 已知狀況

沒有。測試全數通過，報告輸出看起來合理。
