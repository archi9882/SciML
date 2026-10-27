# Git 速查手冊（企業級工作流程）

適用於本 repo（`sciml`）。遠端為 `origin`，主分支為 `main`。

---

## 0. 核心原則

1. **`main` 永遠可執行**：不直接在 `main` 上開發，所有變更透過分支與合併完成。
2. **小步提交**：一個 commit 只做一件事，訊息能讓別人看懂為什麼改。
3. **先看再做**：執行任何會改動狀態的指令前，先跑 `git status`。
4. **不改寫已推送的歷史**：已 push 的 commit 不要 `rebase` 或 `reset` 後強制推送。
5. **不提交產物**：資料、輸出圖表、模型權重由 `.gitignore` 排除，不進版控。

---

## 1. 每日必備

| 目的 | 指令 |
|---|---|
| 查看狀態 | `git status` |
| 查看變更內容 | `git diff`（未暫存）／`git diff --staged`（已暫存） |
| 查看歷史（精簡） | `git log --oneline --graph --decorate -20` |
| 同步遠端 | `git pull --rebase` |
| 推送 | `git push` |
| 查看分支 | `git branch -vv` |
| 查看遠端 | `git remote -v` |

---

## 2. 開始一個新任務（標準流程）

```bash
git switch main
git pull --rebase                 # 先同步最新 main
git switch -c feat/w02-batch      # 建立功能分支
# ... 修改檔案 ...
git add -p                        # 逐段檢視後暫存，避免誤提交
git commit                        # 依下方格式寫訊息
git push -u origin feat/w02-batch # 第一次推送，設定追蹤
```

之後在 GitHub 開 Pull Request，審閱後合併到 `main`。

---

## 3. 分支命名

| 前綴 | 用途 | 範例 |
|---|---|---|
| `feat/` | 新功能或新練習 | `feat/w02-batch-script` |
| `fix/` | 修正錯誤 | `fix/tide-resample-off-by-one` |
| `docs/` | 文件 | `docs/venv-guide` |
| `exp/` | 實驗（可能丟棄） | `exp/pinn-beta-sweep` |
| `report/` | 失敗案例報告 | `report/w04-failure-1` |

分支名稱用小寫與連字號，不含空白與中文。

---

## 4. 提交訊息格式（Conventional Commits）

```
<類型>(<範圍>): <摘要，不超過 50 字，命令式語氣>

<正文：說明為什麼改、改了什麼，每行不超過 72 字>

<頁尾：關聯議題或特殊說明>
```

**類型：**

| 類型 | 用途 |
|---|---|
| `feat` | 新增功能或練習 |
| `fix` | 修正錯誤 |
| `docs` | 文件 |
| `refactor` | 重構，不改變行為 |
| `test` | 測試 |
| `chore` | 雜項（設定、依賴） |

**範例：**

```
feat(w02): add argparse CLI for tide batch runs

Allow varying M2 amplitude and noise level from the command line
so the batch summary can be produced without editing source.

Refs: week02/exercises.md Day 3
```

---

## 5. 暫存與提交

| 目的 | 指令 |
|---|---|
| 暫存指定檔案 | `git add 檔名` |
| 逐段暫存（推薦） | `git add -p` |
| 取消暫存 | `git restore --staged 檔名` |
| 提交 | `git commit` |
| 修改最近一次提交訊息（未推送才用） | `git commit --amend` |

---

## 6. 撤銷與還原（依情境選擇）

| 情境 | 指令 | 注意 |
|---|---|---|
| 放棄某檔案的未提交修改 | `git restore 檔名` | **無法復原** |
| 取消暫存 | `git restore --staged 檔名` | 安全 |
| 撤銷最近一次提交，但保留修改 | `git reset --soft HEAD~1` | 未推送才用 |
| 還原已推送的提交 | `git revert <hash>` | 會新增一個反向提交，安全 |
| 暫時存放未完成的工作 | `git stash push -m "說明"` | 之後用 `git stash pop` 取回 |

**禁止（除非你完全明白後果）：**
- `git push --force` 到 `main`
- `git reset --hard` 在有未提交工作時
- 對已共享的分支做 `rebase` 後強制推送（若必要，改用 `git push --force-with-lease`）

---

## 7. 同步與衝突

```bash
git pull --rebase          # 把自己的提交接到遠端最新之後（保持歷史乾淨）
```

衝突處理：
1. `git status` 查看衝突檔案。
2. 編輯檔案，移除 `<<<<<<<`、`=======`、`>>>>>>>` 標記。
3. `git add 檔名`
4. `git rebase --continue`（若是 merge 則 `git commit`）
5. 放棄本次 rebase：`git rebase --abort`

---

## 8. 查找問題

| 目的 | 指令 |
|---|---|
| 查某行是誰改的 | `git blame 檔名` |
| 搜尋歷史中的字串 | `git log -S "關鍵字" --oneline` |
| 二分法找出造成錯誤的提交 | `git bisect start`／`good`／`bad`／`reset` |
| 查看某個提交的內容 | `git show <hash>` |
| 比較兩個分支 | `git log main..feat/xxx --oneline` |

---

## 9. 清理與維護

| 目的 | 指令 |
|---|---|
| 刪除已合併的本機分支 | `git branch -d 分支名` |
| 刪除遠端已不存在的追蹤分支 | `git fetch --prune` |
| 查看被忽略的檔案 | `git status --ignored` |
| 預覽將被清除的未追蹤檔案 | `git clean -nd` |

`git clean -fd` 會永久刪除未追蹤檔案，執行前一定先用 `-n` 預覽。

---

## 10. 常見錯誤與解法

| 錯誤訊息 | 原因 | 解法 |
|---|---|---|
| `repository moved` | 遠端網址已變更 | `git remote set-url origin <新網址>` |
| `rejected (non-fast-forward)` | 遠端有你沒有的提交 | `git pull --rebase` 後再推送 |
| `detached HEAD` | 直接 checkout 到某個 commit | `git switch -c 新分支名` 保存工作 |
| `Author identity unknown` | 未設定使用者資訊 | `git config --global user.name "名字"` 與 `user.email` |
| `Permission denied (publickey)` | SSH 金鑰未設定 | 改用 HTTPS，或設定 SSH 金鑰 |
| `CRLF will be replaced by LF` | Windows 換行差異 | 正常警告，可忽略；統一設定見第 11 節 |

---

## 11. 設定建議（一次性）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的 GitHub 信箱"
git config --global init.defaultBranch main
git config --global pull.rebase true
git config --global push.autoSetupRemote true
git config --global core.autocrlf true      # Windows 使用者
git config --global core.autocrlf input     # Mac/Linux 使用者
```

查看目前設定：`git config --list --show-origin`

---

## 12. 提交前檢查清單

- [ ] `git status` 確認只包含預期的檔案
- [ ] 沒有 `.csv`、`.npz`、`.png` 等產物，也沒有大型資料
- [ ] 沒有密碼、API 金鑰或個人路徑
- [ ] 訊息符合第 4 節格式
- [ ] 程式在 venv 中實際跑過
- [ ] `git pull --rebase` 後才推送

---

## 13. 快速救急

| 狀況 | 第一步 |
|---|---|
| 不確定自己做了什麼 | `git status` 與 `git log --oneline -5` |
| 改壞了檔案 | 若未提交：`git restore 檔名`；若已提交：`git revert <hash>` |
| 推送被拒絕 | `git pull --rebase` 再 `git push` |
| 誤刪了分支 | `git reflog` 找到最後的 commit，再 `git switch -c 分支名 <hash>` |
| 想先離開但工作未完成 | `git stash push -m "說明"` |
