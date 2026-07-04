#!/usr/bin/env python3
"""soobak 문단-경계 게이트 — PostToolUse(Edit|Write) 파일 전체 스캔.

PreToolUse 훅들은 한 edit의 new_string만 보므로 *문단과 문단 사이*에서만
드러나는 결함을 구조적으로 볼 수 없다: 전방 약속 중복(¶1과 ¶5가 같은 약속),
종결 reveal(앞서 다룬 것을 되감아 재명명), 목차 recital, 모호한 전방 지시어.
이 훅은 edit 적용 *후* 파일 전체를 디스크에서 읽어 그 결함을 검출한다. (비차단 경고)
"""
import sys, json, re

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

ti = data.get("tool_input", {}) or {}
path = ti.get("file_path", "") or ""
if "dev/unity" not in path or not path.endswith(".md"):
    sys.exit(0)
try:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
except Exception:
    sys.exit(0)

# 산문 문단만 추출: front-matter, 코드펜스, SVG/HTML/표 블록, 헤딩, 리스트 제외
prose = []
buf = []
in_code = False
in_html = 0
for ln in raw.split("\n"):
    s = ln.strip()
    if s.startswith("```"):
        in_code = not in_code
        if buf:
            prose.append(" ".join(buf)); buf = []
        continue
    if in_code:
        continue
    if re.match(r"<(div|svg|table|thead|tbody|tr|td|th)\b", s):
        in_html += 1
    if in_html:
        if re.search(r"</(div|svg|table)>", s):
            in_html = max(0, in_html - 1)
        continue
    if s == "":
        if buf:
            prose.append(" ".join(buf)); buf = []
        continue
    if s.startswith(("#", "---", "|", "- ", "* ", "<", ">")):
        if buf:
            prose.append(" ".join(buf)); buf = []
        continue
    buf.append(s)
if buf:
    prose.append(" ".join(buf))

hits = []

# (a) 전방 약속 중복: "이번/이/본 글에서는 ~ [현재형 종결]"이 2회+ (위치 무관).
#     마무리 recap의 과거형('살펴봤습니다·다뤘습니다')은 종결이 달라 세지 않는다.
fwd = re.findall(
    r"(?:이번|이|본)\s*글에서는[^.\n]{0,80}?"
    r"(?:살펴봅니다|살펴본다|다룹니다|알아봅니다|짚어봅니다|짚어 봅니다|봅니다)",
    raw,
)
if len(fwd) >= 2:
    hits.append(
        "전방 약속 중복: '이번 글에서는 ~ 살펴봅니다' 류 도입 약속이 " + str(len(fwd))
        + "회 — 도입부가 같은 약속을 반복(순환). 하나만 남기고 나머지는 빈틈 제시/마무리로 전환."
    )

# (b) 모호한 전방 지시어: '이어지는 글'은 '다음 편'으로 읽힘 (링크 동반 시 제외)
if re.search(r"이어지는\s*글", raw) and not re.search(r"이어지는\s*글[^.\n]{0,30}(/dev/|편\])", raw):
    hits.append(
        "모호한 전방 지시: '이어지는 글' — 독자는 '다음 편'으로 읽음. "
        "이 글 내부를 가리키면 '이번 글에서는', 실제 다음 편이면 링크를 동반."
    )

# (c) 목차 recital
if re.search(r"앞으로[^.\n]{0,90}(차례로|순서대로)[^.\n]{0,20}(살펴봅니다|살펴본다|다룹니다|알아봅니다)", raw):
    hits.append("목차 recital: '앞으로 … 차례로 살펴봅니다' — 동기 없는 ToC 나열. 동기/throughline으로 대체.")

# (d) 종결 naming-rewind reveal: "X가/이 바로 **Y**입니다"
m = re.search(r"[가-힣A-Za-z][가-힣A-Za-z ]*(?:이|가)\s*바로\s*\*\*[^*]+\*\*", raw)
if m:
    hits.append(
        "종결 reveal: '… 가 바로 **…**입니다' — 직전에 다룬 것을 되감아 재명명. "
        "용어는 첫 등장 자리에서 바로 명명할 것.  …" + m.group(0)[:26] + "…"
    )

# (e) 섹션 도입부 편집 → 다음 하위섹션 opener와의 preview→detail 에코 동반독 리마인더.
#     탐지가 아니라 *위치 기반 절차 리마인더*: 에코 여부는 의미적("본문이 도입을 넘어
#     전진하는가")이라 grep으로 판정 불가 → 사람이 다음 opener를 함께 읽어야 한다.
#     [heading] → [편집된 도입 프로즈] → [heading] → [프로즈 opener] 형태일 때만 발화.
ns = (ti.get("new_string") or "").strip()
if ns and "\n" not in ns:  # soobak 산문 문단은 한 줄 — 단일 문단 편집에 한정
    lines = raw.split("\n")

    def _cls(s):
        if s == "":
            return "blank"
        if s == "---" or s.startswith("<br"):
            return "sep"
        if s.startswith("#"):
            return "heading"
        if s.startswith(("|", ">", "- ", "* ", "```", "<")):
            return "other"
        return "prose"

    idx = next((i for i, ln in enumerate(lines) if ln.strip() == ns), None)
    if idx is not None:
        # 위: 빈줄·구분선 건너뛴 첫 줄이 heading이면 도입부 위치
        j, preceded_by_heading = idx - 1, False
        while j >= 0:
            c = _cls(lines[j].strip())
            if c in ("blank", "sep"):
                j -= 1
                continue
            preceded_by_heading = (c == "heading")
            break
        # 아래: 빈줄·구분선 건너뛴 첫 줄이 heading인가
        j, next_heading, hj = idx + 1, None, -1
        while j < len(lines):
            c = _cls(lines[j].strip())
            if c in ("blank", "sep"):
                j += 1
                continue
            if c == "heading":
                next_heading, hj = lines[j].strip(), j
            break
        # 그 heading 뒤 첫 콘텐츠가 prose(자체 opener 문단)인가
        opener_prose = False
        if next_heading:
            k = hj + 1
            while k < len(lines):
                c = _cls(lines[k].strip())
                if c in ("blank", "sep"):
                    k += 1
                    continue
                opener_prose = (c == "prose")
                break
        if preceded_by_heading and next_heading and opener_prose:
            hits.append(
                "섹션 도입부 편집 감지 — 다음 하위섹션 '" + next_heading[:40]
                + "' 이 자체 첫 문단으로 엽니다. preview→detail 에코 점검: 그 opener와 "
                "함께 읽어 같은 메커니즘을 *같은 층위*로 반복하지 않는지(본문이 도입의 "
                "예고를 넘어 전진하는지) 확인할 것. 표면 문구가 겹쳐도 본문이 전진하면 OK, "
                "전진 없이 되풀이면 에코=결함."
            )

if not hits:
    sys.exit(0)

msg = (
    "⚠️ soobak 문단-경계 게이트(파일 전체 스캔): PreToolUse가 구조적으로 못 보는 "
    "문단 사이 결함 검출. 해당 지점을 수정한 뒤 0건이 될 때까지 반복할 것. "
    "(이 게이트 통과 전에는 '완료' 선언 금지.)\n"
    + "\n".join("  · " + h for h in hits[:12])
)
print(json.dumps({
    "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg}
}))
sys.exit(0)
