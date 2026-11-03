# TideWatch（AI 原版）

潮汐監測與預測系統。這份是 AI 寫好、能從頭跑到尾的原版，之後每週審查其中一塊、找出錯並寫下證據，再換成你自己驗證過的版本。

**不要先讀程式碼找答案。** 第 3 週只要讓它跑起來、畫出架構、記錄觀察。

## 執行

在 repo 根目錄、已啟動 `.venv` 的狀態下：

```bash
python -m tidewatch run     # 跑整條流程，結果在 outputs/（report.json、params.json、overview.png、runs.jsonl）
python -m tidewatch api     # 啟動 REST API，port 8000
pytest                      # 跑測試
```

API 範例（先執行過一次 `run`）：

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/predict?lat=23.5&lon=120.2&time=2026-01-20T06:00:00Z"
```

## 目錄

| 路徑 | 內容 |
|---|---|
| `tidewatch/` | 主程式（套件）。入口 `__main__.py`、流程 `pipeline.py` |
| `tidewatch/sample_data/` | 範例原始資料，格式見該資料夾的 README |
| `deploy/` | Dockerfile、docker-compose、Kubernetes manifest |
| `legacy/` | 舊版 Fortran 求解器與它的 Python 翻譯版 |
| `.github/workflows/` | CI 設定 |
| `tests/` | 測試 |

## 已知狀況

沒有。測試全數通過，報告輸出看起來合理。
