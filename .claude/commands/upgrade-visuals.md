# 시각화 업그레이드 — Upgrade Visuals

블로그 글의 시각화 요소(ASCII 다이어그램, 텍스트 수식 등)를 SVG/KaTeX/MD 테이블로 변환합니다.

## 인자
- `$ARGUMENTS`: 수정할 파일 경로

## 적용 axis (memory)
- 1순위: **화용론** (다이어그램·코드 후속 연결)

## 점검 항목

### 1. ASCII 다이어그램 → SVG
- ASCII 박스·화살표 다이어그램 발견 → SVG로 변환
- `viewBox`, `currentColor` 사용 (다크모드 호환)
- `<text>` 요소는 `font-family="sans-serif"` 명시
- 화살표는 `<polygon>` 또는 `<marker>` 사용

### 2. 텍스트 수식 → KaTeX
- `O(n²)`, `f(x) = ax + b` 같은 수식은 LaTeX 형식으로 변환
- 인라인: `$수식$`, 블록: `$$수식$$`

### 3. 표 형식 정규화
- `|` 마크다운 표 사용
- 헤더 정렬 (`|---|---|`)
- 셀 너비 균일

### 4. 다이어그램 후속 산문 (화용론 8)
- 다이어그램 직후 첫 산문이 다이어그램이 보여준 것을 받는가?
- 다이어그램의 결론·과정을 받는 절("이렇게 ~하면")로 시작해야 함

### 5. 다이어그램 결론 라인
- 개념 다이어그램의 "→" 결론 라인은 **중복이 아님** — 보존
- 코드 출력 블록의 `→` 산문 중복 라인은 제거 가능

### 6. SVG 표준 패턴
```xml
<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">제목</text>
  <rect x="..." y="..." width="..." height="..." rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="..." y="..." text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스트</text>
  <line x1="..." y1="..." x2="..." y2="..." stroke="currentColor" stroke-width="1.5"/>
  <polygon points="..." fill="currentColor"/>
</svg>
</div>
```

## 출력 형식

```
[Upgrade Visuals]
- ASCII → SVG: N개 변환
- 수식 → KaTeX: N건
- 표 정규화: N건
- 다이어그램 후속 산문: N건 보강
- SVG 다크모드 호환: ✓
```

## 제약

- 정보 누락 0건
- 다이어그램 변환 시 원본의 모든 정보 보존
- 변환 후 다이어그램과 본문의 일관성 점검
