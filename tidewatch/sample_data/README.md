# 範例原始資料

| 檔案 | 欄位 | 說明 |
|---|---|---|
| `stations.csv` | id、name、lat、lon | 測站清單，座標為 WGS84 經緯度（度） |
| `station_A.csv` | time_utc、level_m | 時間為 UTC（ISO 8601），水位單位公尺，每小時一筆 |
| `station_B.csv` | time_local、level_cm | 時間為台灣當地時間（UTC+8），檔案中沒有時區標記；水位單位公分，每小時一筆 |
| `station_C.csv` | timestamp、level_m | 時間為 UTC，水位單位公尺，每 30 分鐘一筆；`-999` 代表缺值 |
| `station_D.csv` | time_utc、level_m | 時間為 UTC，水位單位公尺，每小時一筆 |

資料期間：2026-01-01 起共 30 天。
