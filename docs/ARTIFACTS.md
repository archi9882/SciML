# 本專案的互動頁面總覽

這份文件整理本專案產生過的三個互動頁面，以及它們在 repo 中的對應檔案。

| 頁面 | 用途 | 線上版（僅擁有者可開） | repo 中的檔案 |
|---|---|---|---|
| 學習進度追蹤頁 | 勾選每週練習、記錄筆記 | https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL | `backups/progress.md`（備份） |
| Git 速查頁（視覺化） | 可搜尋、可一鍵複製指令 | https://claude.ai/artifact/Jn9DyQV2p9bQ3HeSoLGsqn | `docs/git-cheatsheet.html`、`GIT_CHEATSHEET.md`（文字版） |
| Git 團隊流轉動畫 | 逐步展示一個功能如何經過本機、遠端、審查、合併與還原 | https://claude.ai/artifact/C6PUmdxK9gopMNnLkvvJXv | `docs/git-team-workflow.html` |

線上版為私人連結，只有擁有者與被授權的人能開啟。repo 中的 HTML 檔可以直接用瀏覽器開啟，不需要網路以外的環境。

---

## 1. 學習進度追蹤頁

### 用途
記錄 20 週計畫的完成狀態、每週的論文摘要與失敗案例筆記，並保存你選擇的選修專題。

### 資料位置
- 進度存在 claude.ai 的資料庫中：collection `data/users/me`，doc `progress`。
- 欄位：
  - `start`：開始日（預設 2026-11-02）
  - `track`：選修專題 id（`flood`、`cfd`、`inverse`、`gen`、`ocean`）
  - `done`：勾選紀錄，key 格式為 `w{週}d{日}c`（練習）或 `w{週}d{日}p`（論文）
  - `notes`：每週筆記，key 為 `w{週}`

### 備份規則
- 每次開新對話交接時，把追蹤頁的狀態更新到 `backups/progress.md`。
- 目前備份仍是預設狀態，尚未記錄任何勾選。

---

## 2. Git 速查頁

### 內容
- 核心原則、每日指令、新任務流程
- 分支命名、Conventional Commits 格式
- 暫存與提交、撤銷與還原（依風險分級）
- 同步與衝突、查找問題、常見錯誤
- 一次性設定、提交前檢查清單、快速救急

### 使用方式
- 網頁版：瀏覽器開啟 `docs/git-cheatsheet.html`。搜尋框會即時過濾，「複製」按鈕可把指令貼到終端機。
- 文字版：`GIT_CHEATSHEET.md`，適合搜尋或列印。

---

## 3. Git 團隊流轉動畫

### 用途
用一個功能分支的完整生命週期，說明每個指令改變了什麼狀態。畫面包含三部分：提交圖、指令與引數拆解、漫畫式對話。

### 步驟與指令

| 步驟 | 指令 | 發生的事 |
|---|---|---|
| 1 | `git clone <網址> [資料夾]` | 把整個 repo 複製到本機，並建立名為 origin 的遠端 |
| 2 | `git switch -c feat/w02-batch` | 從 main 分出新分支，`-c` 表示建立 |
| 3 | `git add -p`、`git commit -m "..."` | 逐段暫存後提交，commit 只存在本機 |
| 4 | `git push -u origin feat/w02-batch` | 遠端建立同名分支，`-u` 設定追蹤關係 |
| 5 | 在 GitHub 開 Pull Request | 審查入口，不是 git 指令 |
| 6 | 同事合併另一個 PR 到 main | main 往前走，你的分支開始分岔 |
| 7 | `git fetch origin`、`git rebase origin/main` | 把你的 commit 接到最新 main，雜湊值會改變 |
| 8 | `git push --force-with-lease` | 覆寫遠端分支前先檢查遠端沒有他人新增的 commit |
| 9 | 在 GitHub 按下 Merge | 產生有兩個父節點的合併 commit，main 才真正改變 |
| 10 | `git switch main`、`git pull` | 本機 main 追上遠端，之後的任務從這裡開始 |
| 11 | `git revert -m 1 <合併 commit 雜湊值>` | 新增一筆反向 commit，不改寫歷史 |

### 引數分類
動畫中的每個引數都標示了以下四種類別之一：

- **固定**：照寫，例如 `git`、`switch`、`push`。
- **旗標**：改變行為，例如 `-c`、`-u`、`-m`、`--force-with-lease`。
- **自訂**：你決定名稱，例如分支名、commit 訊息、資料夾名。
- **既有**：必須已存在，例如 `origin`、`main`、`origin/main`、要還原的 commit 雜湊值。

常見的誤解：`git switch -c` 的分支名可以自訂，但 `git switch main` 的 `main` 不能自己取名，它必須是已存在的分支。

### 雜湊值說明
動畫中的 `a1b2`、`c3d4` 等是示意用的假值，不是 repo 裡真實的 commit。真實雜湊值可以用 `git log --oneline` 查看。

---

## 更新紀錄
- 2026-10-27：建立本文件，整理三個互動頁面的用途與對應檔案。
