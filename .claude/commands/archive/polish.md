# 다듬기 — Polish (Stage 3/4)

목소리(톤·리듬) + 흐름(연결·전환). 글의 청각적 자연스러움과 막힘없는 흐름.

## 파이프라인 위치

```
/foundation → /clarify → ▶ /polish → /verify
   기반          이해         다듬기      검증
```

## 인자
- `$ARGUMENTS`: 수정할 파일 경로

## 적용 axis (memory)
- 1순위: **운율** (`linguistic_prosody.md`)
- 2순위: **의미론** (어휘·연결어미)
- 3순위: **화용론** (전환)

## 점검 영역

### A. 어말 ~니다 분산 (운율 1)
- 같은 어간 (~합니다/됩니다/입니다) 연속 3회+ X
- 한 문단 ~니다 종결 5회+ X
- 불가피하면 동사 유형 분산: 자동사 / 타동사 / 명사술어 / 피동·되다형

### B. 어휘 반복 (운율 2)
- 한 문단 같은 단어 3회+ X → 동의어/대명사/재구성
- 한 문장 같은 단어 2회+ → 즉시 점검

### C. 문장 길이 교차 (운율 3)
- 짧은 문장 (40자-) 4개+ 연속 X → 목록처럼 읽힘
- 긴 문장 (80자+) 연속 X → 호흡 부담
- 짧고 긴 문장 교차가 자연 리듬

### D. 기피 어휘 (의미론 1·4)
구어 동사·과장 부사·문학 비유 단독 사용 금지. 매핑표 `linguistic_semantics.md` 참조:
- 쪼개·가르·섞어두·떼어놓·몰아넣·쪽만·쪽은·휩쓸려·잠식·무대·이야기가
- 매우·훨씬·완전히·완벽하게·획기적·혁신적·압도적·차원이 다른·한계를 넘다

### D-1. 추상 주어 + 물리 행위 동사 회피 (의미론 1 · Register-First)
추상 주어(데이터·텍셀·연산·메커니즘·할당·비용)에 물리 행위 동사 회피. 상세 framework `feedback_korean_native_word_order.md` Register-First 참조.

| 물리 행위 동사 (회피) | 격식 추상 동사 (우선) |
|---|---|
| 깔리다·깔다 | 분포·분배·배치 |
| 뿌려지다·뿌리다 | 분배·분포 |
| 박히다·풀다·놓이다·매겨지다·찍히다·새겨지다·펼쳐지다 | 고정·전개·위치·할당·기록·저장 |

**원칙**: 주어 본성(추상·물리)이 술어 register 결정. 시각 직관은 다이어그램·수치 예시에 위임.

**grep**: 깔리·뿌려지·박히·풀어·놓이·매겨지·찍히·새겨지·펼쳐지 — 추상 주어 동반 0건.

### D-2. 시각 결과 진술 — 시각 동사 우선 (운율·의미론)
그림자 경계·텍셀·픽셀 등 *시각 결과*를 진술할 때, 추상명사+자동사보다 *시각 metaphor + 시각 동사*가 reader 직관 형성에 우선.

| 추상명사+자동사 (회피) | 시각 동사 (우선) |
|---|---|
| 계단 현상이 나타납니다 | 계단처럼 거칠게 보입니다 |
| 결과가 발생합니다 | 결과가 드러납니다·생깁니다 |
| 효과가 나타납니다 | 효과가 보입니다·드러납니다 |

**원칙**: 시각 결과 진술은 *그림 그리듯*. 추상명사 명목화는 abstract layer 추가, 시각 동사는 직접 mental image 형성.

**구분**: D-1과 다름 — D-1은 *추상 주어*에 *물리 행위* 매칭 mismatch (회피). D-2는 *시각 결과*에 *시각 동사* 매칭 일치 (우선).

### D-3. Reference chain 명시성 (화용론 · 지시어)
직전 paragraph의 핵심 noun을 다음 paragraph 첫 sentence에서 reference로 받을 때, *generic 지시어*("이 차이")보다 *specific noun re-use*("이 한계") 우선.

| Generic reference (약함) | Specific reference (우선) |
|---|---|
| 이 차이는 ~ | 이 한계는 ~ (직전 P "한계" 받기) |
| 이 현상은 ~ | 이 mismatch는 ~ (직전 P 어휘 받기) |

**원칙**: 직전 paragraph의 thesis noun을 다음 paragraph 시작 sentence에서 그대로 echo — chain 강화.

### E. 교과서 패턴 회피 (화용론 13)
- "~라는 것입니다", "중요한 점은", "유의해야", "살펴보았으니", "다음과 같이" 절대 금지

### F. 연결어미 ↔ 논리 관계 일치 (의미론 2)
- 인과: ~므로 / ~기 때문에 / ~어서
- 대립: ~지만 / ~나
- 병렬: ~며 / ~고
- 배경+후속: ~는데
- 조건: ~면 / ~거든

**자주 발생하는 오용**: 병렬에 "반대로" 사용, 배경 제시에 "지만" 사용, 인과를 "~고"로 약화.

### F-1. Cause-effect 두 가지 자연 형식 분기 (Resultative · Korean discourse)
인과 chain을 절 결합으로만 처리하지 말고 emphasis에 따라 분기. 상세 `feedback_resultative_clause_combination.md`·`feedback_korean_native_word_order.md` Cause-Effect 두 패턴 참조.

| 형식 | 구조 | 사용 |
|---|---|---|
| 절 결합 subordination | "이유 X-므로/-여 결과 Y" | 이유가 condition으로 깔리는 흐름 |
| **Postfix reasoning** | "결과 Y. 이는 X 때문입니다." | **결과 강조 + 이유 supplement** |

**금지**: "X합니다. 결과적으로/따라서 Y됩니다" 분리 + transition adverb (영어 번역체).

### F-2. Multi-paragraph discourse — Synthesis-as-conclusion (화용론 · Korean discourse)
종합·결론 paragraph 위치 점검. 영어 topic-sentence-first ↔ 한국어 conclusion-last 차이.

| 패턴 | 사용 |
|---|---|
| **English topic-first** (회피) | thesis paragraph 첫 sentence → 압축 supports |
| **Korean explanation → synthesis** (우선) | explanation paragraphs → 종합 paragraph (마지막 isolated single sentence) |

**Trade-off 설명 2-paragraph 패턴**:
- P_explain: 시도 + 결과 (절 결합 ~여) + 이유 (postfix "때문입니다")
- P_synthesis: "결국 ~게 됩니다" 단일 sentence isolated

### G. 문단 간 전환 (화용론 6)
- 문단 시작 문장이 직전 문단 결론을 받는가?
- A→B 사이 끼인 내용이 흐름 끊으면 위치 이동
- 다이어그램·코드 직후 산문은 자연 연결

### H. 호흡 분리 (운율 4)
- 한 문장이 두 번 읽어야 이해되면 분리
- 절 중첩 3단계+ 또는 쉼표 4개+ → 강제 분리

### I. 짧은 문장 연결 (운율 3)
- 연속된 짧은 문장이 연결 없이 나열되면 목록처럼 읽힘
- 논리 관계(~하고/~하면/~도)로 병합하여 흐름 만들기

### J. 소리 내어 읽기 (운율 5)
- Edit 후 첫 문단 + 인접 문장 소리 내어 자연스러운지

## 출력 형식

```
[Stage 3: polish]

운율
- ~니다 분산: N건 변형
- 어휘 반복: N건 교체
- 문장 길이 교차: N건
- 호흡 분리: N건
- 짧은 문장 통합: N건
- 소리 내어 읽기: ✓

의미론
- 기피 어휘: N건 제거
- 연결어미 일치: N건 교정

화용론
- 교과서 패턴: N건 수정
- 문단 전환: N건 보강
```

## 제약

- 의미 변경 X
- 정보 누락 0건 (process 7)
- 사실 정확성은 다음 stage `/verify` 담당
