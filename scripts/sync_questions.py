"""學習站講解 → repo 題目同步。

以 site/content/wNN.html 為準，產生 weekNN/notes.md（題目與答案欄），
並在講解裡標上每一題在筆記中的位置（Day N・Qn），讓兩處題目完全一致。

題目來源（依每天的順序）：
1. 理論段落裡的 <div class="callout ask">（寫進筆記的問題）
2. 例題：<div class="callout predict">
3. 變化題：<section> 三 裡的每個 <h3>
4. Day 6：本週大問題（site/index.html 的 Q 陣列）與第四節的要求

用法：python scripts/sync_questions.py [週次 ...]
筆記裡已經寫了答案的週次會跳過，避免覆蓋。
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def big_questions():
    s = (SITE / "index.html").read_text(encoding="utf-8")
    m = re.search(r"\nconst Q=(\[.*?\]);", s)
    return json.loads(m.group(1))


def to_md(h):
    """講解片段 → Markdown：程式碼、粗體、數學與實體。"""
    h = re.sub(r'<span class="qref">.*?</span>', "", h)
    h = re.sub(r'<span class="day-mark">.*?</span>', "", h)
    h = re.sub(r"<code[^>]*>(.*?)</code>", lambda m: "`" + html.unescape(re.sub(r"<[^>]+>", "", m[1])) + "`", h, flags=re.S)
    h = re.sub(r"</?(b|strong)>", "**", h)
    h = re.sub(r"</?(i|em)>", "*", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = h.replace("\\(", "$").replace("\\)", "$").replace("\\[", "$$").replace("\\]", "$$")
    h = h.replace("\\lt", "<").replace("\\gt", ">")
    return re.sub(r"\s+", " ", html.unescape(h)).strip()


def blocks(chunk):
    """一段 HTML 裡的 p、ul、ol（略過提示與參考答案）。"""
    chunk = re.sub(r"<details.*?</details>", "", chunk, flags=re.S)
    out = []
    for m in re.finditer(r"<(p|ul|ol)\b[^>]*>(.*?)</\1>", chunk, flags=re.S):
        if m[1] == "p":
            t = to_md(m[2])
            if t:
                out.append(t)
        else:
            for li in re.findall(r"<li>(.*?)</li>", m[2], flags=re.S):
                out.append("- " + to_md(li))
    return out


def sections(s):
    return re.findall(r'(<section data-day="(\d)">.*?</section>)', s, flags=re.S)


def collect(s):
    """回傳題目清單：(day, kind, title, lines)，以及第四節的要求。"""
    secs = sections(s)
    qs = []
    # 一、理論：ask callout
    theory = secs[0][0]
    day = int(secs[0][1])
    for m in re.finditer(r'<span class="day-mark">Day (\d)</span>|<div class="callout ask"[^>]*>(.*?)</div>', theory, flags=re.S):
        if m[1]:
            day = int(m[1])
        else:
            body = re.sub(r"^\s*<b>.*?</b>", "", m[2], flags=re.S)
            qs.append([day, "ask", "", blocks(body)])
    # 二、例題
    ex, exday = secs[1]
    pm = re.search(r'<div class="callout predict">\s*<b>.*?</b>(.*?)</div>', ex, flags=re.S)
    qs.append([int(exday), "example", "例題", blocks(pm[1])])
    # 三、變化題
    var, vday = secs[2]
    day = int(vday)
    parts = re.split(r"(?=<h3\b)", var)[1:]
    for p in parts:
        hm = re.match(r"<h3\b[^>]*>(.*?)</h3>", p, flags=re.S)
        dm = re.search(r'<span class="day-mark">Day (\d)</span>', hm[1])
        if dm:
            day = int(dm[1])
        qs.append([day, "variation", to_md(hm[1]), blocks(p[hm.end():])])
    # 四、大問題
    final = secs[3][0]
    reqs = [b for b in blocks(final) if b.startswith("- ")]
    rm = re.search(r"papers/output/[^<\s]+\.md", final)
    return qs, reqs, rm[0] if rm else ""


def number(qs):
    """依天數排序並編號；同一天內保持講解中的順序。"""
    order = sorted(range(len(qs)), key=lambda i: (qs[i][0], i))
    count = {}
    for i in order:
        d = qs[i][0]
        count[d] = count.get(d, 0) + 1
        qs[i].append(count[d])
    return [qs[i] for i in order]


def tag_site(s, qs):
    """在講解裡加上「Day N・Qn」標記（重跑時先清掉舊的）。"""
    s = re.sub(r'<span class="qref">.*?</span>', "", s)
    ask_i = var_i = 0
    asks = [q for q in qs if q[1] == "ask"]
    # 依講解出現順序重新取得各類題目的編號
    def ref(q):
        return f'<span class="qref">筆記 Day {q[0]}・Q{q[4]}</span>'
    def ask_sub(m):
        nonlocal ask_i
        q = asks[ask_i]; ask_i += 1
        return m[0] + ref(q)
    s = re.sub(r'<div class="callout ask"[^>]*>\s*<b>寫進筆記</b>', ask_sub, s)
    exq = next(q for q in qs if q[1] == "example")
    s = re.sub(r'(<div class="callout predict">\s*<b>例題</b>)', lambda m: m[1] + ref(exq), s, count=1)
    secs = sections(s)
    var_sec = secs[2][0]
    order = [q for q in qs if q[1] == "variation"]
    order.sort(key=lambda q: q[5])
    def var_sub(m):
        nonlocal var_i
        q = order[var_i]; var_i += 1
        return m[1] + ref(q) + m[2]
    new_var = re.sub(r"(<h3\b[^>]*>.*?)(</h3>)", var_sub, var_sec, flags=re.S)
    s = s.replace(var_sec, new_var)
    final = secs[3][0]
    new_final = re.sub(r'(<h2><span class="stage-no">四</span>回答本週大問題)(</h2>)', r'\1<span class="qref">筆記 Day 6・Q1</span>\2', final)
    return s.replace(final, new_final)


SITE_URL = "https://claude.ai/artifact/Vq3vHXDt4AjtTW9tTbeGQL"


def notes_md(w, qs, bigq, reqs, reading):
    out = [f"**本週大問題：{bigq}**", "",
           f"講解：學習站第 {w} 週（{SITE_URL}#w{w}）。題號與講解的「筆記 Day N・Qn」一致，答案寫在每題下方的 `> ` 之後。"]
    if reading:
        out.append(f"閱讀摘要：`{reading}`")
    out += ["<!-- 題目由 python scripts/sync_questions.py 從學習站講解產生；改題目請改講解再重跑 -->", ""]
    cur = None
    for d, kind, title, lines, n, *_ in qs:
        if d != cur:
            out.append(f"# Day{d}")
            cur = d
        out.append(f"## Q{n}.")
        head = f"{title}：" if title else ""
        out.append(head + (lines[0] if lines else ""))
        out.extend(lines[1:])
        out.append("> ")
        out.append("")
    out.append("# Day6")
    out.append("## Q1.")
    out.append(f"本週大問題：{bigq}")
    if reqs:
        out.append("至少包含：")
        out.extend(reqs)
    out.append("> ")
    return "\n".join(out) + "\n"


def main(weeks):
    bq = big_questions()
    for w in weeks:
        lesson = SITE / "content" / f"w{w:02d}.html"
        if not lesson.exists():
            continue
        wk = ROOT / f"week{w:02d}"
        notes = wk / "notes.md"
        if notes.exists() and re.search(r"^> \S", notes.read_text(encoding="utf-8"), flags=re.M):
            print(f"第 {w} 週的筆記已有答案，跳過")
            continue
        s = lesson.read_text(encoding="utf-8")
        qs, reqs, reading = collect(s)
        for i, q in enumerate(qs):
            q.append(i)  # 講解中的原始順序
        # number() 依天數排序並在尾端加上 Qn → 整理成 (day, kind, title, lines, n, 原順序)
        qs = [[q[0], q[1], q[2], q[3], q[5], q[4]] for q in number(qs)]
        lesson.write_text(tag_site(s, qs), encoding="utf-8")
        notes.write_text(notes_md(w, qs, bq[w - 1], reqs, reading), encoding="utf-8")
        print(f"第 {w} 週：{len(qs) + 1} 題")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]] or range(1, 27))
