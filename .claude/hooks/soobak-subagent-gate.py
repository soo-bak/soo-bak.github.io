#!/usr/bin/env python3
"""Stop hook — _posts/*.md 산문 편집이 있었던 턴은, '독립 서브에이전트 리뷰어'의
VERDICT: PASS 증거가 트랜스크립트에 있어야만 종료를 허용한다. (항상 강제)

근거(feedback_independent_review_gate): self-report 게이트는 작업자=감사자라 게임된다.
수동 메모리는 생성 시점에 안 떠 green light 를 준다(게이트 비대칭). 그래서 종료 전
'독립 리뷰어 PASS'를 트랜스크립트 기반으로 결정론적으로 강제한다.

판정(이번 세션 transcript 스캔, tool_use_id 매칭):
- _posts/*.md 에 대한 마지막 Edit/Write tool_use 의 줄 위치(last_edit)와 그 파일명(basename)을 찾는다.
  (tool_use.name 이 Edit|Write 이고 input.file_path 가 _posts/*.md 인 경우만.)
- Agent/Task tool_use 를 수집한다: {tool_use_id: (줄, 프롬프트 JSON 문자열)}.
- tool_result 가운데 'VERDICT: PASS' 를 담은 것의 tool_use_id 를 모은다(pass_ids).
- '충족' 조건 = 다음을 모두 만족하는 Agent 호출이 하나라도 존재:
    (a) 그 결과(tool_use_id)가 pass_ids 에 있다 → 리뷰어가 PASS 를 반환했다.
    (b) 그 Agent 호출(요청)이 last_edit *이후* 줄에 있다 → 마지막 편집을 검토한 리뷰다.
    (c) 그 Agent 프롬프트에 last_edit 파일의 basename 이 들어 있다 → *그 파일을* 검토하라고 시켰다.
  → (c) 가 한계(2)(엉뚱한/사소한 내용 리뷰로 PASS 받기)를 막는다.
- 충족되면 통과, 아니면 block.
- 비동기 보강(2026-07-01): 이 환경은 Agent 를 *항상 background* 로 실행해, 리뷰어 VERDICT 가
  원래 Agent tool_use_id 로 안 들어오고(launch tool_result 는 "Async agent launched" 뿐) 완료 시
  서브에이전트 결과 tool_result 로 주입된다 → 위 id 매칭이 영구 실패. 그래서 동기 경로를 그대로 둔 채,
  '마지막 편집 이후의 엄격·파일명 명시 리뷰 요청(req_line) → 그 *이후* 줄의 서브에이전트 PASS tool_result'
  라는 시간 사슬도 인정한다. PASS 는 여전히 tool_result(내 산문 아님)·요청은 파일명+엄격 형식·둘 다
  편집 이후·PASS 는 요청 이후라 안티-게이밍 ①②③ 유지.
- 안티-게이밍: 내 assistant 산문이나 Agent 프롬프트 안의 'VERDICT: PASS' 는 tool_result 가 아니므로
  무효. 또한 '편집한 파일을 명시하지 않은' 리뷰의 PASS 도 무효.
- 편집이 없거나(last_edit == -1) 조건 충족 시 통과. transcript 미가용 시엔 통과(안전).

stop_hook_active 여도 미충족이면 계속 block 한다(진짜 강제). 편집한 파일을 대상으로 한
리뷰의 PASS tool_result 가 쌓이면 자연히 해제된다.
"""
import json
import os
import re
import sys

_POSTS_RE = re.compile(r"_posts/.*\.md$")
_REVIEW_TOOLS = ("Agent", "Task")

# 한계(1) 완화: 리뷰 *요청 프롬프트*가 '엄격한 다축 검토'의 형식을 갖췄는지 본다.
# 무른 한 줄 프롬프트("리뷰해줘, PASS/FAIL")로는 PASS 를 받아도 게이트가 안 열린다.
# (형식 강제이지 실질 보장은 아님 — 실질 엄격성은 결정론적으로 검증 불가.)
_STRICT_POOL = (
    "가차없", "ruthless", "엄격", "결함", "비문", "인과", "지시어", "referent",
    "연어", "collocation", "흐름", "구조", "봐주지", "의심", "동어반복", "번역투",
)

# RC5 비우회(2026-06-30): 한 문단을 ~8라운드 반려시킨 근본은 모든 게이트가 register만 보고
# naturalness(원어민 리듬·동사 분포)를 못 본 것이다. 게다가 '독립' 리뷰어 rubric을 내가 매번
# 즉석 작성해 내 맹점을 상속시켰다. 그래서 리뷰가 *naturalness/벤치마크 축을 실제로 지시받았는지*를
# 결정론적으로 강제한다 — 아래 토큰이 하나도 없으면 그 PASS 로는 Stop 게이트가 열리지 않는다.
_NATURALNESS_REQUIRED = (
    "gold-standard", "gold standard", "리듬", "동사 분포", "동사 분포도", "소리내어", "소리 내어",
)


def _is_strict_prompt(p):
    """리뷰 프롬프트가 (a) VERDICT 이진 판정 프로토콜 + (b) 다축 엄격 검토 지시(≥4축) +
    (c) naturalness/gold-standard 벤치마크 축을 담고 있는지. 최소 형식 게이트."""
    if "VERDICT: PASS" not in p or "VERDICT: FAIL" not in p:
        return False
    if sum(1 for t in _STRICT_POOL if t in p) < 4:
        return False
    # (c) naturalness/벤치마크 축이 *명시적으로* 지시됐는가 (RC5)
    return any(t in p for t in _NATURALNESS_REQUIRED)


def _scan(tpath):
    """(last_edit_line, last_edit_base, agent_reqs, pass_ids, pass_lines) 반환. 못 읽으면 None."""
    last_edit = -1
    last_edit_base = None
    agent_reqs = {}   # tool_use_id -> (line, prompt_json_str)
    pass_ids = set()  # tool_use_id of results containing VERDICT: PASS
    pass_lines = []   # line numbers of subagent tool_results containing VERDICT: PASS
    n = 0
    try:
        with open(tpath, encoding="utf-8") as f:
            for line in f:
                n += 1
                try:
                    ev = json.loads(line)
                except Exception:
                    continue
                typ = ev.get("type")
                msg = ev.get("message")
                content = msg.get("content") if isinstance(msg, dict) else None
                if not isinstance(content, list):
                    continue
                if typ == "assistant":
                    for it in content:
                        if not isinstance(it, dict) or it.get("type") != "tool_use":
                            continue
                        name = it.get("name")
                        if name in ("Edit", "Write"):
                            fp = (it.get("input") or {}).get("file_path", "") or ""
                            if _POSTS_RE.search(fp):
                                last_edit = n
                                last_edit_base = os.path.basename(fp)
                        elif name in _REVIEW_TOOLS:
                            tid = it.get("id")
                            if tid:
                                agent_reqs[tid] = (n, json.dumps(it.get("input") or {}, ensure_ascii=False))
                elif typ == "user":
                    for it in content:
                        if not isinstance(it, dict) or it.get("type") != "tool_result":
                            continue
                        tid = it.get("tool_use_id")
                        txt = json.dumps(it.get("content", ""), ensure_ascii=False)
                        if "VERDICT: PASS" in txt:
                            if tid:
                                pass_ids.add(tid)
                            # 비동기 경로(2026-07-01): 이 환경은 Agent 를 항상 background 로 실행한다.
                            # 그래서 리뷰어의 VERDICT 는 원래 Agent tool_use_id 가 아니라, 완료 시
                            # 주입되는 *서브에이전트 결과* tool_result(sourceToolAssistantUUID/toolUseResult
                            # 를 가진 user tool_result)로 들어온다 — 원래 id 매칭이 구조적으로 불가.
                            # 따라서 PASS tool_result 의 *줄 위치*도 따로 모아, 마지막 편집 이후의
                            # '엄격·파일명 명시 리뷰 요청 → 그 뒤 서브에이전트 PASS' 시간 사슬로 인정한다.
                            # (이 PASS 는 type=user tool_result 라 내 assistant 산문은 절대 포함 못 함 →
                            #  안티-게이밍 ①(내 산문) 유지. 파일명·시점 요건은 main 에서 강제 → ②③ 유지.)
                            if "VERDICT: FAIL" not in txt:
                                pass_lines.append(n)
    except Exception:
        return None
    return (last_edit, last_edit_base, agent_reqs, pass_ids, pass_lines)


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        print("{}")
        return

    tpath = data.get("transcript_path", "")
    if not tpath or not os.path.exists(tpath):
        print("{}")  # 측정 불가 → 안전하게 통과
        return

    scanned = _scan(tpath)
    if scanned is None:
        print("{}")
        return
    last_edit, last_edit_base, agent_reqs, pass_ids, pass_lines = scanned
    if last_edit == -1:
        print("{}")  # 이번 세션 _posts 편집 없음
        return

    # 동기 경로(원래): 마지막 편집 *이후* 요청되고, 그 파일명을 명시했으며, 엄격 형식을 갖췄고,
    # PASS 를 받은(원래 tool_use_id 매칭) 리뷰가 하나라도 있는가
    for tid, (aline, aprompt) in agent_reqs.items():
        if (tid in pass_ids and aline > last_edit
                and last_edit_base and last_edit_base in aprompt
                and _is_strict_prompt(aprompt)):
            print("{}")
            return

    # 비동기 경로(2026-07-01): Agent 가 항상 background 로 실행되는 환경에서는 PASS tool_result 가
    # 원래 Agent tool_use_id 로 안 들어와 위 매칭이 영구 실패한다. 의도(파일 F 편집 후, F 를 검토하라고
    # 시킨 엄격 독립 리뷰어가 PASS)를 보존하면서 시간 사슬로 인정:
    #   (1) 마지막 편집 이후의 '엄격 + 파일명 명시' 리뷰 요청이 존재(가장 이른 것의 줄 = req_line)
    #   (2) 그 요청 *이후* 줄에 서브에이전트 PASS tool_result 가 존재
    # 안티-게이밍: PASS 는 type=user tool_result(내 산문 아님)·요청은 파일명+엄격 형식·둘 다 편집 이후·
    # PASS 는 요청 이후 → ①내 산문 ②엉뚱한 파일 ③편집 전 리뷰 모두 차단.
    strict_req_lines = [
        aline for (aline, aprompt) in agent_reqs.values()
        if aline > last_edit and last_edit_base and last_edit_base in aprompt
        and _is_strict_prompt(aprompt)
    ]
    if strict_req_lines:
        req_line = min(strict_req_lines)
        if any(pline > req_line for pline in pass_lines):
            print("{}")
            return

    reason = (
        "⛔ 독립 서브에이전트 리뷰어 게이트(항상 강제) — 미충족.\n"
        "이번 세션에서 _posts 산문(" + (last_edit_base or "?") + ")을 편집했는데, 그 마지막 편집 "
        "*이후* 에 *그 파일을 대상으로 한* 독립 서브에이전트 리뷰어의 VERDICT: PASS 가 트랜스크립트에 "
        "없습니다. self-report 회고만으로는 끝낼 수 없습니다(작업자=감사자라 게임됨).\n"
        "지금 해야 할 일:\n"
        "1. Agent 도구로 *가차없는* 독립 리뷰어를 띄워 편집한 섹션을 검토시켜라(SendMessage 말고 "
        "매번 새 Agent — fresh eyes). 리뷰어 프롬프트는 *엄격 형식*을 갖춰야 게이트가 인정한다:\n"
        "   · 검토 대상 파일명('" + (last_edit_base or "해당 파일") + "')을 반드시 포함\n"
        "   · 판정 프로토콜 명시: `VERDICT: PASS` 와 `VERDICT: FAIL` 두 문구를 프롬프트에 적어 둘 것\n"
        "   · 다축 엄격 검토 지시: 가차없이·결함·비문·인과·referent·연어·흐름/구조·번역투·동어반복·"
        "봐주지 말 것 중 4개 이상의 점검 축을 프롬프트에 명시\n"
        "   · ⛔ naturalness 축 필수(RC5): '리듬'·'동사 분포'·'소리내어' 중 하나 이상 + 동일 글/시리즈의 "
        "*gold-standard 형제 문단을 지목해 대조*하라는 지시를 반드시 포함(.claude/soobak-review-rubric.md 인스턴스화 권장). "
        "register만 검사하는 리뷰의 PASS로는 게이트가 열리지 않는다 — 8라운드 반려의 근본\n"
        "2. FAIL 이면 지적을 *전부* 반영해 다시 편집하고, 새 리뷰어로 재검 — VERDICT: PASS 가 나올 "
        "때까지 반복한다.\n"
        "3. PASS 를 받으면 리뷰어가 발견한 내용(내 작업 비판 포함)을 정직하게 relay 하고, agentId 와 "
        "VERDICT 를 인용해 보고하라.\n"
        "해제 조건: '편집한 파일명을 명시한' 리뷰 요청 + 그 결과 tool_result 의 VERDICT: PASS. "
        "내 산문에 'VERDICT: PASS' 를 적거나, 엉뚱한 내용을 리뷰시켜 받은 PASS 로는 해제되지 않는다."
    )
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


if __name__ == "__main__":
    main()
