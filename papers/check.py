"""檢查 papers/ 的反芻進度與 grill 期限。

用法：python papers/check.py
規則：期限為 output_started 起 21 天，從開始撰寫 output 的那天算起。
週次：output 開頭的 week 欄位（1–20）手動填寫，代表這篇對應第幾週的練習。
"""
from datetime import date, datetime, timedelta
from pathlib import Path

PAPERS_DIR = Path(__file__).resolve().parent
INPUT_DIR = PAPERS_DIR / "input"
OUTPUT_DIR = PAPERS_DIR / "output"

COURSE_START = date(2026, 10, 27)  # 課程開始日（見 PLAN.md），用來推算週次
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


def parse_week(text: str):
    """把 week 欄位轉成 1–20 的整數；空白或不合法回傳 None。"""
    if text.isdigit() and 1 <= int(text) <= 20:
        return int(text)
    return None


def week_label(week) -> str:
    """顯示用的週次標籤；沒填的顯示 W?，排版才會對齊。"""
    return f"W{week:02d}" if week else "W??"


def week_of(day: date) -> int:
    """依課程開始日推算某天落在第幾週（開始日當天起算為第 1 週）。"""
    return (day - COURSE_START).days // 7 + 1


def main() -> None:
    today = date.today()
    pending, active, expired, done, notes = [], [], [], [], []

    # 已有 output 的論文，依狀態與期限分類
    for md in sorted(OUTPUT_DIR.glob("*.md")):
        if md.name == "TEMPLATE.md":
            continue
        meta = read_front_matter(md)
        week = parse_week(meta.get("week", ""))
        if week is None:
            notes.append(f"{md.stem}：week 欄位未填或不在 1–20，請補上")
        if meta.get("status") == "done":
            done.append((week, md.stem))
            continue
        started = meta.get("output_started", "")
        if not started:
            pending.append((week, md.stem, "output 已建立但尚未填 output_started，計時未開始"))
            continue
        try:
            start_date = datetime.strptime(started, "%Y-%m-%d").date()
        except ValueError:
            pending.append((week, md.stem, f"output_started 格式錯誤：{started}（應為 YYYY-MM-DD）"))
            continue
        # 手填週次與開始日推算不同時提醒（刻意配合其他週的練習可忽略）
        if week is not None and week != week_of(start_date):
            notes.append(f"{md.stem}：week={week}，但 output_started 落在第 {week_of(start_date)} 週")
        deadline = start_date + timedelta(days=GRILL_DAYS)
        left = (deadline - today).days
        if left < 0:
            expired.append((week, md.stem, deadline, -left))
        else:
            active.append((week, md.stem, deadline, left))

    # 有 input 但還沒有 output 的論文（尚無週次資訊）
    written = {md.stem for md in OUTPUT_DIR.glob("*.md")}
    for pdf in sorted(INPUT_DIR.glob("*.pdf")):
        if pdf.stem not in written:
            pending.append((None, pdf.stem, "已有論文但尚未開始寫 output"))

    # 依週次排序，沒填週次的排最後
    def by_week(item):
        return item[0] if item[0] else 99

    print(f"今天：{today}（課程第 {week_of(today)} 週）")
    print(f"討論期限：output_started 起 {GRILL_DAYS} 天\n")

    if active:
        print("[進行中] 請開新 session 與 agent 對話（用 verifying-paper-comprehension skill）")
        for week, name, deadline, left in sorted(active, key=by_week):
            warn = "  <-- 即將到期" if left <= WARN_DAYS else ""
            print(f"  {week_label(week)} {name}：剩 {left} 天（{deadline} 截止）{warn}")
    if expired:
        print("[已逾期] 討論結束，未弄懂的點寫進「我還不懂的地方」帶去導讀")
        for week, name, deadline, over in sorted(expired, key=by_week):
            print(f"  {week_label(week)} {name}：{deadline} 截止，已逾 {over} 天")
    if pending:
        print("[待開始]")
        for week, name, note in sorted(pending, key=by_week):
            print(f"  {week_label(week)} {name}：{note}")
    if done:
        items = ", ".join(f"{week_label(w)} {n}" for w, n in sorted(done, key=by_week))
        print(f"[已完成] {items}")
    if notes:
        print("[提醒]")
        for note in notes:
            print(f"  {note}")
    if not (active or expired or pending or done):
        print("目前沒有論文。把 PDF 放進 papers/input/ 開始。")


if __name__ == "__main__":
    main()
