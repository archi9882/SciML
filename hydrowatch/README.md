# HydroWatch（AI 原版）

流域降雨、逕流、洪水演算與水庫發電系統。這份是 AI 寫好、能從頭跑到尾的原版，之後每週審查其中一塊、找出錯並寫下證據，再換成你自己驗證過的版本。

**不要先讀程式碼找答案。** 第 3 週只要讓它跑起來、畫出架構、記錄觀察。

## 這套系統在做什麼

四個雨量站與一個流量站的原始資料，變成流域平均雨量，經降雨逕流模型得到流量，再演算洪水波在河道裡的傳遞，最後用流量推算水庫蓄水量與發電量，並提供查詢任意位置雨量的 API。

## 執行

在 repo 根目錄、已啟動 `.venv` 的狀態下：

```bash
python -m hydrowatch run     # 跑整條流程，結果在 outputs/（report.json、params.json、overview.png、runs.jsonl）
python -m hydrowatch api     # 啟動 REST API，port 8000
pytest                       # 跑測試
```

API 範例（先執行過一次 `run`）：

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/rain?lat=24.1&lon=121.0&time=2026-01-20T06:00:00Z"
```

## 目錄

| 路徑 | 內容 |
|---|---|
| `hydrowatch/` | 主程式（套件）。入口 `__main__.py`、流程 `pipeline.py` |
| `hydrowatch/sample_data/` | 範例原始資料，格式見該資料夾的 README |
| `deploy/` | Dockerfile、docker-compose、Kubernetes manifest |
| `legacy/` | 舊版 Fortran 洪水演算求解器與它的 Python 翻譯版 |
| `.github/workflows/` | CI 設定 |
| `tests/` | 測試 |

## 已知狀況

沒有。測試全數通過，報告輸出看起來合理。
