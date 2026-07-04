#!/usr/bin/env python3
"""Stop hook — 산문(_posts/*.md) 편집이 있었던 턴은 끝내기 전에 '수정 완료 후 회고'를 강제한다.

동작:
- PostToolUse 마커 작성기가 _posts/*.md Edit/Write 때 .claude/.retrospect_pending 를 남긴다.
- 이 Stop 훅은 마커가 있으면 한 번 stop 을 block 하여 회고를 요구하고, 마커를 지운다.
- stop_hook_active 가 참이거나 마커가 없으면 그대로 통과(무한 루프 방지).

결정론적 강화(2026-06-24):
- self-report 게이트는 거짓 보고로 게임할 수 있다(작업자=감사자).
- 그래서 `git diff --numstat HEAD` 로 *이번 턴 실제 변경 규모*를 측정해 block reason 에
  박는다. 사용자와 모델이 같은 객관 숫자를 본다 → '전면 재수정' 범위 거짓 주장이
  숫자와 모순되어 즉시 드러난다. (의미적 정확성은 여전히 결정론적 검증 불가 — 범위만.)
"""
import json
import os
import subprocess
import sys


def _numstat(project_dir):
    """dev/unity/_posts 의 HEAD 대비 numstat → {path: (added, deleted)}."""
    try:
        out = subprocess.run(
            ["git", "-C", project_dir, "diff", "--numstat", "HEAD", "--",
             "dev/unity/_posts", "dev/network/_posts"],
            capture_output=True, text=True, timeout=10,
        ).stdout
    except Exception:
        return None
    res = {}
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 3:
            a, d, p = parts
            try:
                res[p] = (int(a) if a != "-" else 0, int(d) if d != "-" else 0)
            except ValueError:
                pass
    return res


def _turn_delta(project_dir):
    """이번 턴(직전 Stop 대비) 파일별 변경 줄 수. (현재 numstat, 델타 문자열) 반환."""
    base_path = os.path.join(project_dir, ".claude", ".numstat_laststop")
    cur = _numstat(project_dir)
    if cur is None:
        return None
    base = {}
    try:
        with open(base_path) as f:
            base = json.load(f)
    except Exception:
        base = {}
    lines = []
    for p, (a, d) in sorted(cur.items()):
        ba, bd = base.get(p, [0, 0]) if isinstance(base.get(p), list) else (0, 0)
        da, dd = a - ba, d - bd
        # 커밋 등으로 baseline 이 stale 해 음수가 되면 누적값을 이번 턴으로 본다.
        if da < 0:
            da = a
        if dd < 0:
            dd = d
        if da != 0 or dd != 0:
            lines.append(f"   · {os.path.basename(p)}: 직전 턴 이후 +{da}/-{dd} (누적 +{a}/-{d}) — 나 또는 린터, 귀속 불명")
    # 베이스라인 갱신
    try:
        with open(base_path, "w") as f:
            json.dump({k: list(v) for k, v in cur.items()}, f)
    except Exception:
        pass
    return lines


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        print("{}")
        return

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    marker = os.path.join(project_dir, ".claude", ".retrospect_pending")

    existed = os.path.exists(marker)
    if existed:
        try:
            os.remove(marker)
        except OSError:
            pass

    if data.get("stop_hook_active"):
        print("{}")
        return

    if not existed:
        return_clean = True
        # 편집 없는 턴도 베이스라인은 갱신해 둬야 다음 턴 델타가 정확하다.
        _turn_delta(project_dir)
        if return_clean:
            print("{}")
            return

    delta = _turn_delta(project_dir)
    if delta is None:
        evidence = "   (git diff 측정 불가 — 객관 증거 없이는 '전면 재수정' 주장을 자제하라)"
    elif not delta:
        evidence = "   · 이번 턴 _posts 변경 0줄 — 산문을 실제로 바꾼 게 없다. '수정했다' 보고 금지."
    else:
        evidence = "\n".join(delta)

    reason = (
        "이번 턴에 _posts 산문을 편집했습니다. 끝내기 전에 '수정 완료 후 회고'를 "
        "솔직하게 수행해 출력하세요(자기에게 유리하게 포장 금지). "
        "⛔ 모든 항목은 '예/아니오'가 아니라 *증거*로 답하라 — 증거 없는 '예'는 거짓 보고로 간주한다:\n"
        "① 통독: 어떤 줄 범위(H2~다음 H2)를 이번 턴에 실제로 Read 했는지 줄번호로 적어라. 안 읽었으면 '아니오'.\n"
        "② 골격: 섹션이 *완결된 설명으로서 가져야 할 beat 목록*을 적고(원리·정의·기본값/오버로드 동치·사례·"
        "**worked 수치 예**·**실전 use-case 권장**·내부 메커니즘 등), 각 beat '있음/없음'을 표시하라(missing-beat audit). "
        "'없음'이 있는데 안 채웠으면 미완이다.\n"
        "③ 전면 재수정 여부 — 아래 측정값과 대조하되 *측정의 한계*를 알라:\n"
        "── 직전 턴 이후 _posts 변경(git; 나 또는 린터 — 귀속 불명) ──\n"
        + evidence + "\n"
        "⚠️ 위 자동 수치는 per-turn 귀속 불가다(린터가 턴 사이 다른 파일을 건드리고, 재편집된 줄은 누적 delta 0으로 보임). "
        "그러므로 *네가 이번 턴 실제 편집한 파일*을 `git diff -- <파일>`로 직접 확인해 그 결과를 보고에 인용하라.\n"
        "── 위 git 실측으로 검증 ──\n"
        "   (a) 이번 턴 바꾼 문단 수 / 섹션 총 문단 수를 적고, git diff 결과와 *모순되지 않는지* 확인하라.\n"
        "   (b) 이번 턴 *새로 추가한* beat 목록(worked 예·수치 풀이·실전 권장·일반화·동치·메커니즘). 추가 beat 0이면 표면 패치다.\n"
        "   (c) 변경 줄 수가 작거나 추가 beat 0인데 '전면 재수정'이라 쓰면 = 거짓 보고. '표면 패치'라고 정직하게 보고하라.\n"
        "하나라도 미달이면 그 자리에서 다시 하라. '최소 수정/멀쩡한 문장 보존'은 사용자 규칙이 아니다.\n"
        "※ 반복 실패 기록(2026-06-24): 섹션 재작성 요청에 *도입 1문단만* 다듬고 '③ 전면 재수정 예'로 거짓 보고함. "
        "gold-standard는 11-beat 완결판(일반화·기본값 동치·예시 설정·true/false 수치 풀이·실전 권장)이었고 그 6개 beat를 통째 누락했다. "
        "같은 '도입만 손보고 전면 재수정 주장' 재발을 절대 금지한다."
    )
    print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))


if __name__ == "__main__":
    main()
