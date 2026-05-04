# Edit Prose — Native-from-scratch

원본을 *patch*하지 말 것. 한국어 native tech writer로서 이 paragraph를 **처음부터 새로 쓴다**. 원본은 *정보 보존 검증용*으로만 비교.

## 인자
- `$ARGUMENTS`: 수정할 파일 경로 + 대상 (선택: 라인·섹션·전체)

## 5-Step Process (의무)

매 paragraph edit 직전:

### 1. 원본 읽기 → mental dismiss
원본을 읽고 닫는다. 다음 step에서 원본 sentence 구조·어순·연결어를 carry-over하지 말 것.

### 2. 독자 의문 list (원본 보지 않고)
이 paragraph가 무엇을 답해야 하는가? 한국인 초보자가 가질 의문 list:
- "왜 이게 등장하지?" "이 단어 뜻은?" "X와 Y가 어떻게 연결?"
- 직전 paragraph로부터 무엇을 받아야 하는가?
- 다음 paragraph에 무엇을 넘겨야 하는가?

### 3. Native 새로 쓰기
한국어 native tech writer로서 의문에 답하는 paragraph 작성. 원본 sentence 구조 X. *처음부터*.

생성 시 자동 적용:
- 한국어 자연 어순 6원칙 (화제 선치·배경→주제→동사·조건→귀결·원인→결과·수식어→피수식어·시·공간 부사구 앞쪽)
- 절 결합 + ~게 됩니다 resultative (분리 + transition adverb anti-pattern)
- 인과 marker 명시 ("이는 ~ 때문" / "따라서")
- 추상 명사 → 구체 example
- ~니다 분산 + sentence 50-90자 + ≤3 sentences/paragraph

### 4. 정보 보존 검증
원본과 비교. 다음만 검증:
- [ ] 사실·수치·예시 보존?
- [ ] 메커니즘 chain 보존?
- [ ] 직전 paragraph 받는 reference 역할 보존?
- [ ] 다음 paragraph로 넘기는 setup 역할 보존?

문체·어순·연결어는 native version 우선. 원본 회귀 X.

### 5. 회피 어휘 grep + 영어 직역체 5 패턴 grep

회피 dictionary (`memory/edit_patterns.md` §회피 어휘 Dictionary 참조):
- 강조 부사 (매우·훨씬·자체를·쌓이는·치솟다)
- Superlative (가장·항상·모든·절대)
- 영어 idiom 직역 (매핑됩니다·가능한 한·간주될 수 있다)
- 의인화·추상 동사 (비용이 발생하다·문제가 발생하다)
- 물리 행위 동사 (깔리다·뿌려지다·박히다 등) — 추상 주어 동반 시
- 청자 호출 (~봅시다·살펴봅시다)
- 사용자 거부 dictionary (이를 위해·이때·이 과정은·여럿·이쪽·결과적으로 분리)
- 교과서 패턴 (~라는 것입니다·중요한 점은·살펴보았으니)

영어 직역체 5 패턴:
1. SVO 직역
2. Passive 정의 ("~라고 합니다")
3. 후치 정의
4. 영어 idiom (가능한 한·~려 시도)
5. 영어 명사화 (~의 실행)

검출 시 대체 후보 적용.

## 의무 출력 형식

매 Edit 직전 출력:

```
[Native-from-scratch]
1. 독자 의문: ___
2. Native paragraph: ___
3. 정보 보존: ✓ / ⚠️ N건
4. 회피 어휘 grep: 0건 ✓
5. 영어 직역체 grep: 0건 ✓
```

## 제약

- 정보 누락 0건 (사실·수치·예시·메커니즘·전환 역할)
- 원본 sentence carry-over 0건 (구조 X)
- 회피 어휘 0건
- 영어 직역체 5 패턴 0건

## Quality Benchmark

`memory/reference_diffs.md` 참조 — LightingAndShadows-1/2 commit이 gold standard. 새 edit는 이 수준 match가 목표.

## 대규모 재구성

paragraph 단위가 아닌 multi-paragraph·section 단위 재구성 필요 시 `/soobak-redesign` 호출.
