# soobak 재구성 — Multi-paragraph native rewrite

다중 paragraph·section 단위 재구성 시 사용. paragraph 단위 edit는 `/edit-prose` 충분.

## 인자
- `$ARGUMENTS`: 파일 경로 + 재구성할 섹션 또는 multi-paragraph 블록

## 호출 조건

다음 중 하나라도 참:
1. 사용자가 "재구성·전면 재작성·꼼꼼히 다시" 요청 + 2 paragraph 이상 범위
2. 섹션 인트로·브릿지·마무리 통째 교체
3. Multi-paragraph chain 재배치 (배경→문제→해결 / Limit-Compensation 등)
4. ASCII 다이어그램 → SVG 변환 동반 재구성

단일 paragraph는 `/edit-prose`. 본 스킬은 multi-paragraph 한정.

## 재구성 권한 (License)

원문 sentence·paragraph는 *재료*이지 *유지 대상*이 아님. 다음을 명시 허용:

1. **Sentence·paragraph 순서 자유 변경** — 원문 순서 유지는 default 아님
2. **삭제 의무**: 메타 announcement·교과서 패턴·redundancy·섹션 thesis 무관 곁가지·시리즈 다른 글 중복
3. **Carry-over 금지**: 원문 표현 유지 X. 어색하면 통째 다시 쓰기
4. **반복 제거 의무**: 같은 메커니즘·어휘·framing 1회만
5. **문단 통합·분할**: 1 paragraph = 1 정보 단위. 경계 자유 조정

**보존 대상 = 정보, 원문 X**:
- ✓ 누락 금지: 사실·개념·수치·예시·메커니즘·용어
- ✗ 유지 의무 X: sentence·paragraph 경계·순서·표현·어휘 선택

## 재구성 거부 trigger

다음은 재구성 아닌 minor edit으로 간주, 재시도:

| 회피 패턴 | 판정 |
|---|---|
| Carry-over 위주 | 원문 sentence 60%+ 그대로 유지 |
| Redundancy 보존 | 불필요 sentence 결과물에 잔존 |
| 순서 무변경 | 정보 순서 부적절 인지하고도 원문 순서 유지 |
| 반복 보존 | 같은 메커니즘·어휘 2회+ 반복 잔존 |

## 4-Step Process

### Step 1: Scope + 정확성 audit

- 대상 블록 라인 번호 + 직전·직후 2문장 + 현재 ##/### 제목
- 원본 정확성 audit:
  - 핵심 claim 추출 (정의·단언·메커니즘)
  - 본문 다른 등장 grep + cross-reference
  - 영어 원전 용어 referent 일관성
  - 분야 표준 (Unity 공식 문서 등) cross-reference
  - 원본 inconsistency·부정확 검출 → 수정 plan

### Step 2: Multi-paragraph chain 재배치 plan

한국어 자연 chain 패턴 적용:
- **Background-Problem-Solution**: 배경 → 문제 → 해결
- **Cause-Effect**: 이유 → 결과 (절 결합) / 결과 → 이유 (postfix "이는 ~ 때문")
- **Limit-Compensation**: 한계 → 보완
- **Concession-Inference**: 양보 → 인과 결과

영어 직역체 회피: 해결 → 문제 → 해결 (해결 중복) / 결과 → 이유 (영어 직역) 등.

**Synthesis-as-conclusion**: 종합 paragraph는 마지막 isolated single sentence (English topic-first 회피).

### Step 3: Native-from-scratch rewrite

각 paragraph마다 `/edit-prose` 5-step process 적용:
1. 원본 mental dismiss
2. 독자 의문 list
3. Native 새로 쓰기 (원본 carry-over X)
4. 정보 보존 검증
5. 회피 어휘·영어 직역체 grep

**Multi-paragraph 일관성**:
- 직전 paragraph thesis noun → next paragraph specific reference (이 한계는 / 이 차이는)
- 인과 표지 명시 (이는 ~ 때문 / 따라서)
- ~니다 분산을 paragraph 경계 넘어 점검 (전체 5회+ X)

### Step 4: 통합 단일 Edit

- 전체 재구성 결과를 단일 Edit으로 적용
- 정보 누락 0건 검증
- 회피 어휘 0건 검증
- 영어 직역체 5 패턴 0건 검증

## 의무 출력

```
[soobak-redesign]
Scope: ___ (라인 범위)
원본 audit: 정확성 ✓ / inconsistency N건 발견
Chain pattern: Background-Problem-Solution / Cause-Effect / Limit-Compensation / Concession-Inference
재배치: ___ (paragraph 순서 변경 plan)
삭제 대상: ___ (redundancy·메타·곁가지)
Native 후보 paragraph 1: ___
Native 후보 paragraph 2: ___
...
정보 보존: 사실·수치·예시·메커니즘 모두 ✓
회피 어휘 / 영어 직역체 grep: 0건 ✓
```

## Reference

- `memory/edit_patterns.md` — 회피 dictionary, 영어 직역체 5 패턴, 한국어 자연 어순 6원칙
- `memory/reference_diffs.md` — Quality benchmark (LightingAndShadows-1/2 commit)
