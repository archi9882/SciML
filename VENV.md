# 虛擬環境（venv）建立與激活手冊

本 repo 的所有練習都在同一個虛擬環境裡執行。`.venv/` 不進版控，每台電腦要自己建立一次。

## 0. 前置需求

- Python 3.11 以上（`python --version` 或 `python3 --version` 可確認）
- 已在 `sciml` 資料夾內（有 `requirements.txt` 的那層）

## 1. 建立 venv（只需做一次）

```bash
python -m venv .venv
```

成功後，資料夾內會出現 `.venv/`。

## 2. 激活 venv（每次開新終端機都要做）

| 系統 | 指令 |
|---|---|
| Mac / Linux | `source .venv/bin/activate` |
| Windows（PowerShell） | `.venv\Scripts\Activate.ps1` |
| Windows（CMD） | `.venv\Scripts\activate.bat` |

激活後，終端機提示字元前面會出現 `(.venv)`。

## 3. 安裝套件（只需做一次，或 requirements.txt 更新後再做）

```bash
pip install -r requirements.txt
```

若安裝失敗，改用：

```bash
pip install numpy pandas matplotlib
```

## 4. 確認環境正確

```bash
python -c "import numpy, pandas, matplotlib; print('OK')"
python week01/tide_example.py
```

第一行印出 `OK`，第二行能跑完並印出每日統計，就表示環境正確。

## 5. 在 VS Code 使用這個 venv

1. 按 `Ctrl+Shift+P`（Mac 為 `Cmd+Shift+P`）。
2. 執行 **Python: Select Interpreter**。
3. 選擇路徑包含 `.venv` 的那一項。

之後 VS Code 的終端機與執行按鈕都會使用這個環境。

## 6. 離開 venv

```bash
deactivate
```

## 常見問題

- **PowerShell 出現「無法載入…因為這個系統上已停用指令碼執行」**：以系統管理員身分執行一次 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`，再重新激活。
- **`python` 指到錯的版本**：改用 `py -3.11 -m venv .venv`（Windows）或 `python3.11 -m venv .venv`（Mac/Linux）。
- **不確定有沒有激活**：看提示字元前面有沒有 `(.venv)`，或執行 `which python`（Windows 用 `where python`），路徑應指向 `.venv` 內。
- **想重建 venv**：`deactivate` 後刪除 `.venv/` 資料夾，重新執行第 1–3 步。
