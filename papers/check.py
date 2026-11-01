"""檢查 papers/ 的反芻進度與 grill 期限。

用法：python papers/check.py
規則：期限為 output_started 起 21 天，從開始撰寫 output 的那天算起。
"""
from datetime import date, datetime, timedelta
from pathlib import Path

PAPERS_DIR = Path(__file__).resolve().parent
INPUT_DIR = PAPERS_DIR / "input"
OUTPUT_DIR = PAPERS_DIR / "output"

GRILL_DAYS = 21  # 討論期限：三週
WARN_DAYS = 7    # 剩餘天數不足此值時加註警告


def read_front_matter(path: Path) -> dict:
    """讀取檔案開頭 --- 之間的 key: value，不依賴 yaml 套件。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta


def main() -> None:
    today = date.today()
    pending, active, expired, done = [], [], [], []

    # 已有 output 的論文，依狀態與期限分類
    for md in sorted(OUTPUT_DIR.glob("*.md")):
        if md.name == "TEMPLATE.md":
            continue
        meta = read_front_matter(md)
        if meta.get("status") == "done":
            done.append(md.stem)
            continue
        started = meta.get("output_started", "")
        if not started:
            pending.append((md.stem, "output 已建立但尚未填 output_started，計時未開始"))
            continue
        try:
            start_date = datetime.strptime(started, "%Y-%m-%d").date()
        except ValueError:
            pending.append((md.stem, f"output_started 格式錯誤：{started}（應為 YYYY-MM-DD）"))
            continue
        deadline = start_date + timedelta(days=GRILL_DAYS)
        left = (deadline - today).days
        if left < 0:
            expired.append((md.stem, deadline, -left))
        else:
            active.append((md.stem, deadline, left))

    # 有 input 但還沒有 output 的論文
    written = {md.stem for md in OUTPUT_DIR.glob("*.md")}
    for pdf in sorted(INPUT_DIR.glob("*.pdf")):
        if pdf.stem not in written:
            pending.append((pdf.stem, "已有論文但尚未開始寫 output"))

    print(f"今天：{today}")
    print(f"討論期限：output_started 起 {GRILL_DAYS} 天\n")

    if active:
        print("[進行中] 請開新 session 與 agent 對話（提示詞見 papers/GRILL.md）")
        for name, deadline, left in active:
            warn = "  <-- 即將到期" if left <= WARN_DAYS else ""
            print(f"  {name}：剩 {left} 天（{deadline} 截止）{warn}")
    if expired:
        print("[已逾期] 討論結束，未弄懂的點寫進「我還不懂的地方」帶去導讀")
        for name, deadline, over in expired:
            print(f"  {name}：{deadline} 截止，已逾 {over} 天")
    if pending:
        print("[待開始]")
        for name, note in pending:
            print(f"  {name}：{note}")
    if done:
        print(f"[已完成] {', '.join(done)}")
    if not (active or expired or pending or done):
        print("目前沒有論文。把 PDF 放進 papers/input/ 開始。")


if __name__ == "__main__":
    main()
