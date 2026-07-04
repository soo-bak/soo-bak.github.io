# RewriteBySoobak-33

대상 글 한 편을, **레퍼런스 시리즈 전체(29편)의 모든 특징을 학습한 기준**에 맞춰 **섹션 단위·SVG 단위로 전면 재작성**하는 독립 스킬.

핵심 목표: 직관적으로 이해되는 **자연스러운 한국어 문체**, **번역투 0건**, **앞/뒤 맥락을 받아 이어지는 문장 연결**, **정보 손실 0건**으로 — 대상 글을 레퍼런스 시리즈와 같은 품질로 끌어올린다.

> 이 스킬은 "그럴듯하게 표면만 손보고 끝냈다고 보고하는 것"을 **명시적으로 금지**한다. 매 섹션은 *원본을 재료로만 쓰는 native-from-scratch 재작성*을 거쳐야 하며, Phase 4에서 **재작성이 실제로 일어났는지 git diff로 증명**한다.

---

## 인자

- `$ARGUMENTS`: 재작성할 **대상 글**의 파일 경로 (한 편). 없으면 사용자에게 요청한다.
- 글 단위로 동작한다. 한 번 호출 = 한 편 전체.

---

## 레퍼런스 시리즈 = 학습 대상 (Unity 최적화 시리즈 전체 29편)

Phase 0은 아래 **29편 전부**를 학습한다. 일부 견본만 보지 않는다 — *전체 시리즈*가 곧 기준이다.

```
GameLoop-1, GameLoop-2,
RenderingFoundation-1, RenderingFoundation-2, RenderingFoundation-3,
GPUArchitecture-1, GPUArchitecture-2,
UnityPipeline-1, UnityPipeline-2, UnityPipeline-3,
ScriptOptimization-1, ScriptOptimization-2,
MemoryManagement-1, MemoryManagement-2, MemoryManagement-3,
UIOptimization-1, UIOptimization-2,
LightingAndShadows-1, LightingAndShadows-2,
ShaderOptimization-1, ShaderOptimization-2,
PhysicsOptimization-1, PhysicsOptimization-2,
ParticleAndAnimation-1, ParticleAndAnimation-2,
Profiling-1, Profiling-2,
MobileStrategy-1, MobileStrategy-2
```

각 슬러그의 파일 경로는 `Glob`으로 해석한다: `dev/unity/_posts/*-[<Slug>].md` (날짜는 하드코딩하지 않는다).

이 29편은 **문체·구조·시각화·용어·연결·교육 흐름의 기준**이다. 대상 글이 어떤 시리즈에 속하든, 결과물은 이 29편과 같은 결로 읽혀야 한다.

**가드**: 만약 `$ARGUMENTS`로 받은 대상 글이 위 29편 중 하나라면 — 그 글은 *학습 기준*이므로 재작성 대상이 아니다. 진행 전에 사용자에게 그 사실을 알리고 의도를 확인한다.

---

## 실행 원칙

이 스킬이 호출되면 **항상 Phase 0~4 전체를 빠짐없이 순서대로 실행**한다. 글이 이미 깔끔해 보여도, 변경할 것이 적어 보여도 프로세스를 축약하거나 "재작성 불필요"로 판단하지 않는다.

**자동 적용**: 본문의 어휘·구조·재작성은 사용자 확인 없이 곧장 Edit로 적용하고, 적용 후 보고한다 (사용자 명시 선호). 단 commit·push·다른 글 수정은 자동 적용 금지 — 보고만 한다.

**정직 보고 의무**: Phase 4의 검증 수치(diff stat, 원문 잔존율, 12축 통과 여부)를 **실제 측정값 그대로** 보고한다. 검증을 통과하지 못한 섹션은 "통과"로 적지 않는다. 통과 못 한 부분은 다시 재작성하고, 그래도 남는 한계는 한계로 보고한다.

---

## 절대 제약 조건 (모든 Phase·모든 수정에 적용)

1. **거짓 수정(cosmetic patch) 금지** — 원문 문장 구조를 유지한 채 단어 몇 개만 바꾸는 것은 재작성이 아니다. 매 섹션은 native-from-scratch로 다시 쓴다.
2. **정보 보존** — 사실·수치·기술 메커니즘·단계별 상세·예시·용어는 하나도 누락하지 않는다. 보존 대상은 *정보*이지 *원문 문장*이 아니다.
3. **기술 용어 절대 보존** — L2/L3, 텍셀, 드로우콜, 스택/힙, 박싱, SIMT, IMR, TBDR 등 구체 용어를 간소화하거나 상위 개념으로 대체하지 않는다.
4. **질문형 문체 금지** — 선언문만 사용 (메타 "이 글에서는 ~ 살펴봅니다"는 허용).
5. **"이 글에서 다루기엔 복잡하다" 금지** — 맥락에서 등장한 개념은 완전히 설명한다. "별도 글에서 다루는 것이 적합합니다"는 쓰지 않는다.
6. **초보자 대상** — 암묵적 전제를 명시한다.
7. **교과서 표현 제거** — "~라는 것입니다 / 중요한 점은 / 유의해야 합니다 / 살펴보았으니" → 직접 진술.
8. **산문 우선** — 설명은 불릿보다 산문. (행동 H3의 axis 풀어쓰기도 산문. 정의 list·비교표 같은 자연스러운 불릿만 유지)
9. **개념 글에 JSON/YAML 설정 코드 금지.**
10. **frontmatter·네비게이션 보존** — 글 상단 frontmatter(`---` 블록), 하단 **관련 글 / 시리즈 / 전체 시리즈** 링크 목록은 내용·링크를 **그대로 유지**한다 (마무리 본문 형식만 아래 규칙에 맞춤). 링크를 새로 만들거나 지우지 않는다.
11. **다이어그램 결론 라인은 중복이 아님** — 개념 다이어그램 내부의 "→ 결과" 라인은 자기 완결성을 위해 보존. 코드 출력 블록에서 산문과 겹치는 "→" 라인만 제거.

---

## 거짓 수정(cosmetic) 판정 — 재작성 거부 trigger

다음 중 하나라도 해당하면 그 섹션은 *재작성 실패*로 간주하고 다시 한다:

| 패턴 | 판정 |
|---|---|
| 원문 산문 문장의 40% 이상이 그대로(또는 단어 1~2개만 교체) 잔존 | Carry-over 과다 — patch |
| 영어 직역체 5패턴이 1건이라도 잔존 | 번역투 미해소 |
| 회피 어휘(발생하다·매우·가장·항상·이를 위해 등)가 잔존 | native 미달 |
| 동일 종결어미 4회+ 연속 잔존 | 어미 단조성 미해소 |
| 정보 순서가 부적절함을 인지하고도 원문 순서 유지 | 구조 재작성 회피 |
| 섹션 도입이 motivation 없이 정의로 시작 (H2) | 위계 미적용 |

---

## 참조 자료 (각 Phase·서브에이전트가 Read로 읽는다)

메모리 디렉토리: `/home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/`
이 메모리들은 위 29편 레퍼런스 시리즈에서 이미 추출된 기준이다. **메모리는 distilled 요약, 29편 원문은 ground truth** — Phase 0은 둘을 함께 본다.

| 파일 | 무엇을 담았나 |
|---|---|
| `edit_patterns.md` | native-from-scratch 5-step, 회피 어휘 dictionary, 영어 직역체 5패턴, 한국어 자연 어순 6원칙, resultative 결합, subject-verb register |
| `linguistic_refine_patterns.md` | 12축 한국어 언어학 정밀화 가이드 (모든 prose의 통과 기준) |
| `reference_diffs.md` | 골드 스탠다드 commit의 before/after 대표 변환 8사례 |
| `h2_intro_patterns.md` | H2 도입부 = motivation/배경 (정의는 H3 양보). 5-단계 정형 |
| `feedback_h3_explanation_pattern.md` | 메커니즘 H3 9축 (원인 설명형) |
| `feedback_h3_action_pattern.md` | 행동 H3 7축 (줄이기·전략·개선형, 불릿→산문) |
| `feedback_h2_closing_paragraph.md` | H2 마무리 5축 (thesis 아닌 행동 가이드) |
| `series_continuation_patterns.md` | 후속편 첫 H2 5-beat (Part 1 받기·압축·pivot·roadmap) |
| `term_consistency_audit.md` | 시리즈 직전 편 용어 사전 grep 의무 |
| `feedback_technical_accuracy.md` | 사실 정확성 11항목 (시점·행위자·좌표계·시간 차원 등) |
| `natural_example_patterns.md` | 사례 enumerate 자연화 (끼리나·X와 Y처럼 직역 회피 → 행동 진술) |
| `feedback_auto_apply.md` | 점검 결과 자동 적용 원칙 |

서브에이전트는 위 파일 중 자기 작업에 해당하는 것을 **반드시 먼저 Read**한 뒤 작업한다.

---

# 파이프라인 개요

```
Phase 0  레퍼런스 시리즈 전체(29편) 학습 → Style Spec 산출 (병렬 학습 서브에이전트 + 메인 종합)
Phase 1  대상 글 분석 + 대상 시리즈 개념 맵 + 용어 사전 (메인)
Phase 2  섹션 단위 전면 재작성 → H2 섹션마다 순차 서브에이전트 (앞/뒤 맥락 handoff)
Phase 3  시리즈 정합 (중복 정리 + 용어 일관) → 서브에이전트
Phase 4  전문가 리뷰 + 사실 정확성 + 거짓수정 검증(diff 증명) → 서브에이전트
```

서브에이전트는 `Agent`(subagent_type=general-purpose, model=opus)로 호출한다. Phase 0 학습 서브에이전트는 **병렬**, Phase 2 섹션 재작성은 충돌 방지를 위해 **순차** 실행한다.

---

## Phase 0 — 레퍼런스 시리즈 전체(29편) 학습 (메인 + 병렬 학습 서브에이전트)

대상 글을 건드리기 전, 위 **29편 전부**를 학습해 **Style Spec**을 만든다. 5편 견본으로 좁히지 않는다.

### 0-A. 경로 해석 + 메모리 정독 (메인)
1. 29개 슬러그를 `Glob`으로 실제 파일 경로로 해석한다 (`dev/unity/_posts/*-[<Slug>].md`).
2. 위 표의 12개 메모리 파일을 모두 Read한다.

### 0-B. 병렬 학습 서브에이전트 — 29편 전수 정독
29편을 **4개 배치**로 나눠 4개의 학습 서브에이전트에 할당하고 **동시에(병렬)** 호출한다. (메인 context를 가볍게 유지하면서 전수 학습)

권장 배치:
- 배치 1: GameLoop-1/2, RenderingFoundation-1/2/3, GPUArchitecture-1/2 (7편)
- 배치 2: UnityPipeline-1/2/3, ScriptOptimization-1/2, MemoryManagement-1/2/3 (8편)
- 배치 3: UIOptimization-1/2, LightingAndShadows-1/2, ShaderOptimization-1/2, PhysicsOptimization-1/2 (8편)
- 배치 4: ParticleAndAnimation-1/2, Profiling-1/2, MobileStrategy-1/2 (6편)

**학습 서브에이전트 프롬프트 템플릿:**
```
# 레퍼런스 스타일 학습 서브에이전트

당신은 한국어 기술 글쓰기 문체 분석가입니다.
아래 레퍼런스 글들을 전부 Read하여, 공통된 문체·구조 특징을 실제 문장 근거와 함께 추출합니다. (수정하지 않습니다 — 관찰만)

## 먼저 Read
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/linguistic_refine_patterns.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/edit_patterns.md

## 정독 대상 (전부 Read)
{이 배치의 파일 경로 목록}

## 추출 차원 (각 차원마다 2~3개 실제 인용 근거 첨부)
1. 종결어미 분포·변주 (동일 어미 연속 한계)
2. paragraph 호흡 (문장 수·길이·<br>·빈 줄)
3. H2 도입 패턴 (motivation 우선? 부정 thesis? 사례 dichotomy?)
4. H3 본문 정형 (메커니즘 H3 / 행동 H3 구분 흐름)
5. H2 마무리 패턴 (thesis vs 행동 가이드)
6. 시리즈 후속편 첫 H2 (5-beat 유무, Part 1 받기 표현)
7. transition·인과 표지 어휘 (실제 빈출 어휘)
8. term 표기 (한국어(English) 형식, 도입 패턴)
9. 외부 reference 형식 (inline vs blockquote)
10. 시각화: SVG 스타일 속성(viewBox·currentColor·fill-opacity·font-size·sans-serif), 표·KaTeX 사용 방식
11. 마무리 섹션 골격 (## 마무리 + 불릿 요약 + 통찰 + 다음 글 연결 + 링크 3종)
12. 교육 흐름 (동기→정의→메커니즘→예시 순서 준수 여부)

## 출력
[배치 학습 보고]
- 위 12차원 각각: 관찰된 패턴 + 실제 인용 2~3개
- 이 배치에서 특히 일관되게 나타난 특징 / 편차
```

### 0-C. Style Spec 종합 (메인)
4개 배치 보고 + 메모리를 종합하여, 이후 모든 재작성 서브에이전트에 전달할 **Style Spec**을 출력한다. 보고들 사이에 편차가 있으면 *다수 패턴*을 기준으로 채택하되, 가장 정제된 편(LightingAndShadows-1/2·ShaderOptimization-1/2·ParticleAndAnimation-1)의 패턴에 가중치를 둔다.

```
[Style Spec — 레퍼런스 29편에서 학습]
종결어미 분포·변주 / paragraph 호흡: ...
H2 도입 정형 / H3 정형(메커니즘·행동) / H2 마무리 정형: ...
후속편 첫 H2 5-beat: ...
transition·인과 표지 / term 표기 / 외부 reference 형식: ...
SVG 표준(속성값 명시) / 표·KaTeX 규칙 / 마무리 섹션 골격: ...
교육 흐름 규칙: ...
```

### SVG 표준 (29편 공통 — Style Spec에 포함)
```
래퍼:  <div style="text-align: center; margin: 1.5em 0;">
태그:  <svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="max-width: {W}px; width: 100%;">
색상:  stroke·fill 모두 currentColor만. 하드코딩 색(#000·black) 금지
글꼴:  font-family="sans-serif"
배경:  fill="currentColor" fill-opacity="0.06" (강조 0.15~0.2)
테두리: stroke="currentColor" stroke-width="1.2~1.5", rx="2~5"
제목:  font-size="13" font-weight="bold" / 부제 font-size="10" opacity="0.6" / 레이블 9~11
화살표: <line> + <polygon> (점선 stroke-dasharray) / 주석 <!-- 구획 -->
닫기:  </svg></div>
정확성: visual 비율 ≈ 수학 비율, 모든 요소가 viewBox 경계 안.
```

### 마무리 섹션 골격 (29편 공통 — Style Spec에 포함)
```
## 마무리

- (불릿 5~8개) 글의 중요한 내용만 경어체로 요약. 기술 용어 정확 보존. 각 항목 독립 완결.

(통찰 paragraph) 불릿들의 공통점을 메타 수준에서 정리.

<br>

(다음 글 연결 1~2 paragraph) 자연스러운 다음 글로의 확장 + [다음 글](URL)에서는 ~ 살펴봅니다.

<br>

---

**관련 글** / **시리즈** / **전체 시리즈**  (링크 목록은 기존 그대로 보존)
```

---

## Phase 1 — 대상 글 분석 + 대상 시리즈 개념 맵 + 용어 사전 (메인)

> 주의: Phase 0의 *레퍼런스 시리즈*(29편)와 Phase 1의 *대상 시리즈*(대상 글이 속한 시리즈)는 별개다. 개념 맵·용어 사전은 **대상 글이 속한 시리즈**(대상 글 footer의 전체 시리즈) 기준으로 만든다.

### 1-A. 대상 시리즈 자동 추출
1. 대상 파일을 Read.
2. 하단 `**전체 시리즈**` 링크 목록의 URL에서 슬러그 추출 → `Glob`으로 파일 경로 해석.
3. `(현재 글)` 표시로 대상의 시리즈 내 위치 파악. 같은 시리즈 모든 편 Read.

### 1-B. 대상 시리즈 개념 맵
| 개념명 | 최초 상세 설명 위치 | 이후 등장 위치 | 등장 유형 (정의 / 맥락 요약 / 전제 참조 / 불필요 반복) |
|---|---|---|---|

### 1-C. 직전 편 용어 사전 (term_consistency_audit.md)
직전 편이 있으면 핵심 개념 명사·메커니즘 동사·단위어·외래어 표기·추상↔구체 라벨 분포를 grep 추출. 동일 개념은 직전 편 표기를 따른다.

### 1-D. 5-스케일 통독 + 구조·시각 인벤토리
| 스케일 | 점검 |
|---|---|
| 글 전체 | 주제 완결성, 시리즈 내 역할, 도입-전개-마무리 |
| 섹션 | H2/H3 순서의 교육적 흐름, 섹션 간 연결, 중복 |
| 문단 | 단일 책임, 문단 간 인과 |
| 문장 | 선언문·주어 명시·능동·교과서 표현·길이 |
| 단어 | 용어 통일·기술 용어 보존·주관 표현·조사/접속사 |

추가로 **시각 인벤토리**: ASCII 다이어그램 / 텍스트 수식 / 코드블록 표 위치를 모두 기록.

### 1-E. 출력
```
[Phase 1]
대상 시리즈: N편 / 대상 위치: (n)편
개념 맵: (표)
직전 편 용어 사전: (표 또는 "직전 편 없음")
H2 섹션 목록(순서대로): [L.. ## A], [L.. ## B], ...
시각 인벤토리: ASCII N개 / 텍스트 수식 N개 / 코드표 N개 (각 위치)
주요 구조 이슈: (정의→동기 역순, 이질 주제 혼재 등)
```

---

## Phase 2 — 섹션 단위 전면 재작성 (순차 루프, 핵심)

**Phase 1의 H2 섹션 목록을 순서대로 순회**하며, 섹션마다 재작성 서브에이전트를 1개씩 **순차** 호출한다. 각 서브에이전트에 **직전(이미 재작성된) 섹션의 마지막 2~3문장**과 **다음 섹션의 제목·첫 문단**을 함께 넘겨 — 앞을 받고 뒤로 넘기는 연결을 보장한다.

도입부(첫 H2)가 후속편이면 series_continuation 5-beat을 적용한다.

### 섹션 재작성 서브에이전트 프롬프트 템플릿
```
# 섹션 전면 재작성 서브에이전트

당신은 한국어 기술 글쓰기 전문 편집자이자 Unity/CS 교육 전문가입니다.
아래 섹션을 native-from-scratch로 **전면 재작성**합니다. 원문은 정보 보존 검증용 *재료*일 뿐이며, 문장 구조·어순·연결어를 가져오지 않습니다.

## 먼저 Read할 자료
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/edit_patterns.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/linguistic_refine_patterns.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/h2_intro_patterns.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/feedback_h3_explanation_pattern.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/feedback_h3_action_pattern.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/feedback_h2_closing_paragraph.md
- /home/soo-bak/.claude/projects/-home-soo-bak-soo-bak-github-io/memory/natural_example_patterns.md
- (후속편 도입부면) series_continuation_patterns.md
- 레퍼런스 견본 1편 (이 섹션 주제와 가장 가까운 편): {경로}

## Style Spec (레퍼런스 29편 학습 결과)
{Phase 0 Style Spec 전문}

## 대상 파일 / 섹션
파일: {경로}
이 섹션: {## 제목, 라인 범위}
섹션 원문:
{섹션 전체 텍스트}

## 앞 맥락 (이미 재작성됨 — 이 섹션 첫 문장이 받아야 함)
{직전 섹션 마지막 2~3문장}

## 뒤 맥락 (이 섹션 마지막이 넘겨야 함)
{다음 섹션 제목 + 첫 문단}

## 대상 시리즈 개념 맵 / 용어 사전
{개념 맵 + 직전 편 용어 사전}

## native-from-scratch 5-step (각 paragraph 의무)
1. 원문 읽고 mental dismiss
2. 독자 의문 list (한국인 초보자 의문 + 앞에서 받을 것 + 뒤로 넘길 것)
3. 원본 구조를 버리고 처음부터 새로 쓰기
4. 정보 보존 검증 (사실·수치·예시·메커니즘·전환 역할)
5. 회피 어휘 grep + 영어 직역체 5패턴 grep → 대체

## 구조 규칙
- H2 도입 = motivation/배경 (정의·메커니즘은 H3에 양보). 첫 문장이 추상 thesis면 둘째 문장에 구체 사례 동반
- 메커니즘 H3: 9축 / 행동 H3: 7축 (메모리 참조)
- H2 마무리: thesis 아닌 행동 가이드, 메커니즘 → 행동 axes 분해
- 정의→동기 역순이면 동기→정의로 재배치. 이질 주제 혼재면 분리
- 12축 통과: 어미 단조성·명사 술어 박멸·절 결합 resultative·화제 선치·다단 transition·회피 dictionary·추상→구체·외부 reference blockquote·paragraph 1~3문장·term 표기 일관

## 시각 처리 (이 섹션 내부)
- ASCII 다이어그램 → SVG (Style Spec SVG 표준)
- 텍스트 수식 → KaTeX (인라인 $...$, 블록 $$...$$)
- 코드블록 표(비교·정리용) → 마크다운 표. 실제 코드 출력은 유지
- 다이어그램 직후 첫 산문은 다이어그램 결론을 받는 절로 시작
- 변환 시 원본 정보 전부 보존

## 절대 제약
{스킬의 "절대 제약 조건" 11개 전문}

## 작업
1. 위 자료 Read
2. paragraph 단위 native-from-scratch 재작성 (5-step) + 시각 자산 변환
3. 단일 Edit으로 섹션 교체
4. 자기 검증 후 보고:

[섹션 재작성 보고: ## 제목]
- 독자 의문 list / 앞 받기·뒤 넘기기 연결: ...
- 정보 보존: 사실·수치·예시·메커니즘·용어 모두 ✓ / ⚠️ N건
- 원문 산문 문장 잔존율(그대로): 약 N% (40% 미만이어야 함)
- 회피 어휘 grep: 0건 / N건→대체
- 영어 직역체 5패턴 grep: 0건 / N건→대체
- 동일 어미 4회+ 연속: 0건
- 시각 변환: ASCII→SVG N / 수식→KaTeX N / 코드표→MD표 N
```

### 마무리 섹션 처리
`## 마무리`는 Style Spec 마무리 골격으로 재작성. 불릿 요약은 본문에서 *실제 다룬* 내용만, 다음 글 연결은 본문 논조에 부합하게. 관련/시리즈/전체 시리즈 링크 목록은 그대로 보존.

---

## Phase 3 — 시리즈 정합 (중복 정리 + 용어 일관) [서브에이전트]

Phase 2 완료 후 호출. 대상 시리즈 개념 맵·용어 사전 기반으로 점검.

```
# 시리즈 정합 서브에이전트

## 먼저 Read
- term_consistency_audit.md (메모리 경로)
- 대상 파일 + 대상 시리즈 인접 편

## 중복 4유형 처리
- 정의: 이 글이 최초 상세 위치면 유지
- 맥락 요약: 흐름상 필수면 "~에서 살펴본 것처럼, [개념]은 [한 줄]입니다." + 링크로 압축
- 전제 참조: 재설명 불필요면 용어만 + 링크
- 불필요 반복: 같은 깊이 반복이면 삭제 또는 한 줄 참조

## 용어 일관
- 직전 편 용어 사전과 동일 개념의 모든 인스턴스 일치 (본문·표·SVG label·소제목 전부)
- 위반 시 일괄 변환 후 grep으로 잔존 0건 확인

## 원칙
- 글 자립성 보장 / 같은 깊이 중복 금지 / 대상 파일만 수정 (다른 글은 리포트만) / 기술 용어·수치 보존

## 보고
[시리즈 정합 보고]
- 중복 처리: 정의 유지 N / 맥락 요약 N / 전제 참조 N / 불필요 반복 삭제 N
- 용어 일관 위반→일괄 수정: N건
- 다른 글 수정 권고: (있으면)
```

---

## Phase 4 — 전문가 리뷰 + 사실 정확성 + 거짓수정 검증 (diff 증명) [서브에이전트]

Phase 3 완료 후 호출. 문장 단위 전수 점검 + **재작성이 실제로 일어났음을 git diff로 증명**.

```
# 최종 리뷰·검증 서브에이전트

## 먼저 Read
- linguistic_refine_patterns.md (12축)
- feedback_technical_accuracy.md (사실 정확성 11항목)
- reference_diffs.md (품질 벤치마크)
- 대상 파일 (수정 완료본) + 대상 시리즈 인접 편

## Trial 1 — 어휘·구조 (12축 전수)
첫 문장부터 끝까지, 12축 미달이면 즉시 Edit 수정.

## Trial 2 — 사실 정확성 (11항목)
시점 vs 결과 상태 · 행위자 정확(의인화) · 수치 hedge · 메커니즘 chain 성립 · 용어/약어 정확 · 명사구 시간 의미 · 좌표계(screen vs world) · 사례→메커니즘 chain · thesis-only 결론 회피 · SVG-prose 메커니즘 중복 · 시간 차원 명시. 일상어로 풀어 쓴 부정확 집중 점검.

## Trial 3 — 거짓수정(cosmetic) 검증 [정직 보고 의무]
1. `git diff --stat {파일}` → 변경량 측정. 분량 대비 변경이 미미하면 해당 섹션 재작성 지시.
2. `git diff {파일}` 통독 → 원문 산문 40%+ 잔존 섹션 식별 → native-from-scratch 재작성.
3. 잔존 grep (실측 보고): `매핑됩니다`,`가능한 한`,`발생합니다`,`매우`,`가장`,`항상`,`이를 위해`,`이때`,`결과적으로` / 동일 어미 연속 / `라는 것입니다`,`중요한 점은`,`유의해야` — 각 0건. 잔존 시 수정 후 재확인.

## Trial 4 — 시각(SVG) 단위 점검
- ASCII 다이어그램 잔존 0건 / 텍스트 수식 잔존 0건
- 모든 SVG: currentColor만·sans-serif·viewBox·max-width·정상 닫힘
- 다이어그램 직후 산문이 다이어그램 결론을 받는가

## 보고 (실측값 그대로)
[최종 검증 보고]
| 차원 | 탐지 | 수정 | 비고 |
| 12축 자연화 / 사실 정확성 / 거짓수정(diff +N/-N, 잔존 최대 N%) / 시각 |
[grep 실측] 영어 직역체·회피 어휘 0 / 동일 어미 연속 0 / 교과서 표현 0 / ASCII·수식 잔존 0
[재작성 재지시] ## 섹션명: 사유 → 재작성함 (있으면)
```

---

## 최종 출력 (메인 에이전트)

```
## RewriteBySoobak-33 결과 — {파일}

### Phase 0 학습
- 레퍼런스 29편 전수 정독(4배치 병렬) + 메모리 12파일 → Style Spec 산출

### Phase 1 분석
- 대상 시리즈 N편 / 대상 (n)편 / 개념 맵 N항목 / H2 섹션 N개 / 시각 자산 N개

### Phase 2 섹션 재작성
| 섹션 | 정보보존 | 산문잔존율 | 직역체 | 시각변환 |
...

### Phase 3 시리즈 정합
- 중복 처리 N건 / 용어 일관 수정 N건

### Phase 4 최종 검증 (실측)
- git diff: +N / -N 줄 / 산문 잔존 최대: N% (전 섹션 40% 미만)
- 영어 직역체·회피 어휘·교과서 표현·ASCII·텍스트수식 잔존: 모두 0건
- 12축 통과 ✓ / 사실 정확성 ✓ / SVG 표준 ✓

### 정보·구조 보존
| 기술 용어 / 수치 / frontmatter·네비게이션 / 시리즈 중복 해소 / 글 자립성 | ✓·✗ |

### 한계·후속 (있으면 정직하게)
- ...
```

commit·push는 사용자가 요청할 때만. 자동 수행 금지.
