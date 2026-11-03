# 範例原始資料

| 檔案 | 欄位 | 說明 |
|---|---|---|
| `stations.csv` | id、name、lat、lon | 測站清單，座標為 WGS84 經緯度（度） |
| `rain_R1.csv` | time_utc、rain_mm | 雨量站 R1。時間為 UTC，每小時一筆，欄位為該小時降雨深度（mm） |
| `rain_R2.csv` | time_local、rain_mm_10min | 雨量站 R2。時間為台灣當地時間（UTC+8），檔案中沒有時區標記；每 10 分鐘一筆，欄位為該 10 分鐘內的累積降雨深度（mm） |
| `rain_R3.csv` | time_utc、rain_in | 雨量站 R3。時間為 UTC，每小時一筆，單位為英寸（inch） |
| `rain_R4.csv` | timestamp、rain_mm | 雨量站 R4。時間為 UTC，每小時一筆，單位 mm；`-999` 代表缺值（儀器沒有資料） |
| `flow_Q.csv` | time_utc、q_m3s | 流域出口流量站。時間為 UTC，每小時一筆，單位 m3/s；`-999` 代表缺值 |

資料期間：2026-01-01 起共 30 天。流域面積 120 km2。
