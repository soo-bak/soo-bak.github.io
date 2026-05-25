---
layout: single
title: "모바일 전략 (1) - 발열과 배터리 - soo:bak"
date: "2026-02-21 01:30:00 +0900"
description: 서멀 쓰로틀링, 지속 성능과 피크 성능, Adaptive Performance, 전력 예산, 30fps vs 60fps를 설명합니다.
tags:
  - Unity
  - 최적화
  - 모바일
  - 서멀쓰로틀링
  - 배터리
---

## 모바일만의 제약: 발열과 배터리

데스크톱 게임 최적화에서는 보통 한 프레임 안에서 CPU나 GPU가 어디에 시간을 쓰는지 찾고, 그 병목을 줄이는 것이 핵심입니다. 냉각 여유와 전력 공급이 비교적 크기 때문에, 개별 프레임의 실행 시간을 줄이면 성능 문제가 상당 부분 해결되는 경우가 많습니다.

모바일에서는 상황이 다릅니다. 시작 직후에는 목표 프레임레이트를 유지하더라도, CPU와 GPU 부하가 계속 누적되면 기기가 감당할 수 있는 전력과 열의 한계에 가까워집니다. 이때 문제는 특정 함수 하나의 비용이 아니라, 장시간 유지 가능한 부하 수준입니다.

데스크톱은 전력 공급과 냉각에 비교적 여유가 있지만, 모바일 기기는 제한된 배터리와 작은 방열 면적 안에서 동작합니다. 같은 16.6ms 프레임 예산을 만족하더라도 전력 소모가 크면 배터리가 빠르게 줄고, 열이 누적되면 이후의 성능도 흔들립니다.

따라서 모바일 성능은 짧은 시간의 피크 성능만으로 판단하기 어렵습니다. 실제 플레이 시간에 가깝게 실행했을 때 프레임레이트, 입력 반응, 배터리 소모, 기기 온도가 함께 안정적으로 유지되는지를 봐야 합니다. 이 글에서는 이런 관점에서 서멀 쓰로틀링의 메커니즘, 이에 대응하는 플랫폼 API, 전력 예산의 구조, 그리고 프레임레이트 선택의 트레이드오프를 다룹니다.

---

## 서멀 쓰로틀링 — 모바일 성능의 근본 제약

모바일 기기의 **SoC(System on Chip)**에는 CPU, GPU, 메모리 컨트롤러, ISP, 모뎀 같은 여러 블록이 밀집해 있습니다. CPU와 GPU가 높은 클럭으로 오래 동작하면 전력 소비가 열로 바뀌고, 칩 온도가 안전 범위에 가까워지면 시스템은 과열을 막기 위해 CPU와 GPU의 최대 클럭을 낮춥니다. 이것이 **서멀 쓰로틀링(Thermal Throttling)**입니다.

짧은 벤치마크나 앱 실행 직후의 측정값은 대체로 기기가 차갑고 클럭을 높게 유지할 수 있는 상태의 **피크 성능(Peak Performance)**에 가깝습니다. 반면 게임은 렌더링, 물리, 애니메이션, UI 같은 작업을 실제 플레이 시간 동안 계속 반복합니다. 시간이 지나 열이 누적된 뒤에도 유지할 수 있는 성능이 **지속 성능(Sustained Performance)**이며, 모바일 게임의 프레임레이트와 품질 설정은 이 지속 성능을 기준으로 잡아야 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">서멀 쓰로틀링에 의한 지속 성능 변화</text>

  <line x1="80" y1="55" x2="80" y2="245" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">성능</text>

  <text x="68" y="82" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">높음</text>
  <text x="68" y="166" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">중간</text>
  <text x="68" y="208" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">낮음</text>

  <line x1="80" y1="78" x2="540" y2="78" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <line x1="80" y1="120" x2="540" y2="120" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <line x1="80" y1="162" x2="540" y2="162" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <line x1="80" y1="204" x2="540" y2="204" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>

  <line x1="80" y1="245" x2="540" y2="245" stroke="currentColor" stroke-width="1.5"/>
  <text x="540" y="278" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">시간</text>

  <text x="112" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">시작</text>
  <text x="248" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">열 누적</text>
  <text x="440" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">지속 상태</text>

  <rect x="80" y="58" width="115" height="187" fill="currentColor" fill-opacity="0.025"/>
  <rect x="195" y="58" width="115" height="187" fill="currentColor" fill-opacity="0.05"/>
  <rect x="310" y="58" width="230" height="187" fill="currentColor" fill-opacity="0.025"/>

  <path d="M 90 78 C 130 78, 160 78, 195 82 C 230 90, 250 120, 282 156 C 310 188, 350 204, 540 204" fill="none" stroke="currentColor" stroke-width="2"/>

  <line x1="226" y1="104" x2="245" y2="72" stroke="currentColor" stroke-width="0.8"/>
  <text x="250" y="69" font-family="sans-serif" font-size="10.5" fill="currentColor">클럭 제한 시작</text>

  <text x="138" y="235" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.78">피크 성능</text>
  <text x="252" y="235" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.78">하락 구간</text>
  <text x="425" y="235" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.78">지속 성능</text>

  <text x="290" y="305" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">초기 피크 성능은 오래 유지되지 않으며, 열이 쌓인 뒤의 안정 구간이 실제 기준이 됨</text>
</svg>
</div>

<br>

게임 시작 직후에는 목표 프레임레이트가 나오다가 시간이 지난 뒤 같은 장면에서 프레임 시간이 길어지는 현상은, 코드 경로가 갑자기 바뀌어서가 아니라 클럭 제한으로 같은 작업을 더 낮은 성능에서 처리하기 때문에 발생할 수 있습니다. 따라서 모바일에서는 초반 피크 성능보다 열이 누적된 뒤의 지속 성능을 기준으로 설계해야 합니다.

---

## 발열의 메커니즘

서멀 쓰로틀링을 줄이려면 먼저 열이 왜 쌓이는지 이해해야 합니다. 모바일 게임이 직접 제어할 수 있는 것은 기기의 냉각 구조가 아니라, CPU와 GPU가 매 프레임 소비하는 전력과 그로 인해 발생하는 열입니다.

### 열 발생

SoC가 전력을 소비하면 그 에너지의 상당 부분은 결국 열로 바뀝니다. 게임 부하에서는 CPU와 GPU의 트랜지스터가 계속 스위칭하고, 화면 해상도, 셰이더 복잡도, 물리 연산, 메모리 접근이 늘어날수록 소비 전력도 증가합니다. 동적 전력은 보통 $P_{dynamic} \approx \alpha C V^2 f$로 근사할 수 있습니다. 여기서 $\alpha$는 실제로 스위칭되는 비율, $C$는 회로의 커패시턴스, $V$는 전압, $f$는 클럭 주파수입니다.

클럭만 높아져도 전력은 증가하지만, 실제 고성능 상태에서는 안정적인 동작을 위해 전압도 함께 올라가는 경우가 많습니다. 전압은 수식에서 제곱으로 작용하므로, 높은 클럭과 높은 전압이 겹치면 전력과 발열이 빠르게 늘어납니다. 모바일에서 해상도나 프레임레이트를 높였을 때 발열이 급격히 증가하는 이유가 여기에 있습니다.

데스크톱 CPU와 GPU는 수십~수백 W의 열을 처리할 수 있는 냉각 구조를 전제로 설계됩니다. 반면 스마트폰 SoC는 기기와 방열 구조에 따라 다르지만, 장시간 지속해서 감당할 수 있는 전력 범위가 훨씬 좁습니다. 모바일 SoC가 순간적으로 높은 성능을 낼 수 있더라도, 얇은 기기 안에서 그 열을 계속 배출할 수 없다면 결국 클럭을 낮춰야 합니다.

<br>

**데스크톱과 모바일의 열 처리 방식 비교**

| 항목 | 데스크톱 PC | 스마트폰 |
|---|---|---|
| 전력 공급 | 콘센트 전원을 사용하므로 순간 전력 사용에 비교적 여유가 있음 | 배터리 전력을 사용하므로 전력 소비가 사용 시간과 발열에 직접 연결됨 |
| 열 발생 위치 | CPU와 GPU가 별도 칩과 별도 쿨러를 사용하는 경우가 많음 | CPU와 GPU가 같은 SoC 안에 있어 열이 한 지점에 집중되기 쉬움 |
| 열 배출 방식 | 방열판, 팬, 수냉 라디에이터 등 능동 냉각 사용 가능 | 베이퍼 챔버, 금속 프레임, 후면 커버를 통한 수동 방열에 의존 |
| 지속 성능 | 냉각 설계가 충분하면 높은 클럭을 오래 유지하기 쉬움 | 열이 누적되면 클럭 제한으로 성능이 단계적으로 낮아질 수 있음 |

<br>

### 열 방출의 한계

스마트폰에서 SoC의 열은 기판, 흑연 시트나 베이퍼 챔버, 금속 프레임, 후면 커버를 거쳐 기기 표면으로 퍼지고, 마지막에는 주변 공기로 빠져나갑니다. 팬이 없으므로 열을 밖으로 밀어내는 능동 냉각보다는, 기기 내부에 열을 넓게 분산시키고 표면에서 자연스럽게 방출하는 방식에 의존합니다.

베이퍼 챔버나 히트파이프는 이 과정에서 칩 주변의 열을 더 넓은 면적으로 옮기는 역할을 합니다. 하지만 열을 분산시킬 뿐, 팬처럼 외부로 강제로 배출하지는 않습니다. 그래서 열 발생 속도가 표면을 통한 방열 속도보다 빠르면 내부 온도는 계속 올라갑니다.

기기 표면 온도와 칩 내부의 **정션 온도(Junction Temperature)**도 다르게 봐야 합니다. 정션 온도는 트랜지스터가 실제로 동작하는 반도체 접합부의 온도이며, 사용자가 손으로 느끼는 표면 온도보다 먼저 위험 구간에 가까워질 수 있습니다. 구체적인 임계치는 SoC, 기기 설계, 제조사 정책에 따라 다르지만, 내부 온도가 안전 범위에 가까워지면 시스템은 CPU와 GPU의 클럭을 낮춰 열 발생을 줄입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">쓰로틀링 발생 과정</text>

  <line x1="82" y1="70" x2="82" y2="285" stroke="currentColor" stroke-width="1.2" opacity="0.65"/>
  <line x1="82" y1="285" x2="535" y2="285" stroke="currentColor" stroke-width="1.2" opacity="0.65"/>
  <polygon points="82,64 78,72 86,72" fill="currentColor" opacity="0.65"/>
  <polygon points="542,285 534,281 534,289" fill="currentColor" opacity="0.65"/>
  <text x="74" y="73" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">온도</text>
  <text x="535" y="304" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">시간</text>

  <line x1="90" y1="120" x2="525" y2="120" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.45"/>
  <text x="525" y="112" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.72">열 제한 구간</text>

  <path d="M 92 260 C 145 240, 180 205, 220 156 C 246 126, 272 112, 305 120 C 345 128, 375 150, 420 160 C 465 170, 500 166, 525 162"
        fill="none" stroke="currentColor" stroke-width="2"/>

  <path d="M 92 86 C 150 86, 198 88, 230 92 C 268 97, 284 110, 305 132 C 328 156, 350 184, 385 204 C 425 226, 478 230, 525 230"
        fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="5,4" opacity="0.75"/>

  <circle cx="305" cy="120" r="4" fill="currentColor"/>
  <line x1="305" y1="120" x2="330" y2="86" stroke="currentColor" stroke-width="0.8" opacity="0.8"/>
  <text x="335" y="84" font-family="sans-serif" font-size="10.5" fill="currentColor">클럭 제한 시작</text>

  <g transform="translate(112 330)">
    <line x1="0" y1="0" x2="28" y2="0" stroke="currentColor" stroke-width="2"/>
    <text x="36" y="4" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.78">칩 온도</text>
    <line x1="116" y1="0" x2="144" y2="0" stroke="currentColor" stroke-width="2" stroke-dasharray="5,4" opacity="0.75"/>
    <text x="152" y="4" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.78">사용 가능한 성능</text>
  </g>

  <text x="290" y="360" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">온도가 제한 구간에 가까워지면 클럭이 낮아지고, 낮아진 성능에서 새 균형점이 형성됨</text>
</svg>
</div>

<br>

쓰로틀링은 보통 한 번에 끝나는 이벤트가 아니라 단계적으로 진행됩니다. SoC 내부의 CPU와 GPU는 같은 전력·열 예산을 공유하므로, 한쪽의 부하가 커지면 다른 쪽이 사용할 수 있는 여유도 줄어듭니다. 온도가 올라가면 시스템은 먼저 최대 클럭을 낮추거나 고성능 코어 사용을 제한하고, 상황이 더 나빠지면 더 강한 성능 제한을 적용할 수 있습니다. 극단적인 경우에는 앱이 종료되거나 기기가 성능 보호 모드로 들어갈 수 있습니다.

외부 환경도 쓰로틀링 시점에 영향을 줍니다. 주변 온도가 높으면 기기 표면에서 공기로 열이 빠져나가기 어렵고, 두꺼운 케이스나 충전 중 사용도 발열 조건을 악화시킬 수 있습니다. 같은 빌드라도 여름철 실외 테스트와 겨울철 실내 테스트, 케이스 착용 여부, 충전 상태에 따라 쓰로틀링이 시작되는 시점이 달라질 수 있으므로, 성능 테스트에서는 이런 조건을 통일하고 함께 기록해야 합니다.

---

## Adaptive Performance

서멀 쓰로틀링이 시작된 뒤에는 게임이 원하는 성능을 유지하기 어렵습니다. 시스템이 온도 보호를 위해 클럭을 제한하면, 같은 작업도 더 오래 걸리고 프레임레이트가 흔들릴 수 있습니다. **Adaptive Performance**는 이 상태에 도달하기 전에 기기의 열 상태를 읽고, 해상도, 그림자, LOD, 후처리 같은 품질 항목을 단계적으로 조절해 부하를 낮추는 접근입니다.

### Unity Adaptive Performance Provider

Unity Adaptive Performance는 기기의 열 상태, 전력 상태, 병목 정보를 가져오기 위해 플랫폼별 **Provider**를 사용합니다. Android에서는 ADPF 기반 Android Provider를 우선 검토하고, 대상 기기가 Samsung Galaxy 중심이라면 Samsung Android Provider를 함께 고려할 수 있습니다. Samsung Provider는 GameSDK 기반으로 기기별 열 상태와 성능 정보를 Adaptive Performance에 전달하지만, 신규 프로젝트에서는 대상 OS와 provider 지원 범위를 먼저 확인해야 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Adaptive Performance 동작 구조</text>

  <rect x="40" y="48" width="160" height="78" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="120" y="72" text-anchor="middle" font-family="sans-serif" font-size="12.5" font-weight="bold" fill="currentColor">플랫폼 Provider</text>
  <text x="120" y="94" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">열 상태</text>
  <text x="120" y="112" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">성능 힌트 / 병목 정보</text>

  <line x1="200" y1="87" x2="244" y2="87" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="244,87 234,81 234,93" fill="currentColor"/>

  <rect x="244" y="48" width="174" height="78" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.4"/>
  <text x="331" y="72" text-anchor="middle" font-family="sans-serif" font-size="12.5" font-weight="bold" fill="currentColor">Adaptive Performance</text>
  <text x="331" y="94" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">WarningLevel</text>
  <text x="331" y="112" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">BottleneckStatus</text>

  <line x1="418" y1="87" x2="462" y2="87" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="462,87 452,81 452,93" fill="currentColor"/>

  <rect x="462" y="48" width="118" height="78" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="521" y="72" text-anchor="middle" font-family="sans-serif" font-size="12.5" font-weight="bold" fill="currentColor">Indexer</text>
  <text x="521" y="94" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">부하 수준 결정</text>
  <text x="521" y="112" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">Scaler 우선순위</text>

  <line x1="521" y1="126" x2="521" y2="160" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="521,160 515,150 527,150" fill="currentColor"/>

  <rect x="70" y="160" width="480" height="86" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="310" y="184" text-anchor="middle" font-family="sans-serif" font-size="12.5" font-weight="bold" fill="currentColor">Scaler가 품질 항목을 단계적으로 조정</text>
  <text x="110" y="213" font-family="sans-serif" font-size="10.5" fill="currentColor">해상도 스케일</text>
  <text x="240" y="213" font-family="sans-serif" font-size="10.5" fill="currentColor">그림자</text>
  <text x="330" y="213" font-family="sans-serif" font-size="10.5" fill="currentColor">LOD</text>
  <text x="405" y="213" font-family="sans-serif" font-size="10.5" fill="currentColor">후처리</text>
  <text x="485" y="213" font-family="sans-serif" font-size="10.5" fill="currentColor">프레임레이트</text>

  <line x1="310" y1="246" x2="310" y2="278" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="310,278 304,268 316,268" fill="currentColor"/>

  <rect x="70" y="278" width="480" height="76" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="310" y="302" text-anchor="middle" font-family="sans-serif" font-size="12.5" font-weight="bold" fill="currentColor">목표</text>
  <text x="310" y="326" text-anchor="middle" font-family="sans-serif" font-size="10.8" fill="currentColor">쓰로틀링 진입 전 평균 부하를 낮춰 지속 프레임레이트를 안정화</text>
</svg>
</div>

<br>

Adaptive Performance에서 먼저 확인할 값은 열 상태를 나타내는 **WarningLevel**과 현재 병목을 나타내는 **BottleneckStatus**입니다. WarningLevel은 품질을 얼마나 적극적으로 낮출지 판단하는 신호로 사용할 수 있으며, 대표적으로 다음 세 단계가 있습니다.

<br>

| WarningLevel | 의미 | 대응 방향 |
|---|---|---|
| **NoWarning** | 일반적인 열 상태 | 현재 품질 설정을 유지하되, 프레임 시간과 병목 상태를 계속 관찰 |
| **ThrottlingImminent** | 쓰로틀링이 가까워질 수 있는 상태 | 해상도, LOD, 그림자 거리처럼 체감이 작은 항목부터 단계적으로 낮춤 |
| **Throttling** | 이미 열 제한의 영향을 받고 있는 상태 | 평균 부하를 더 적극적으로 낮춰 정상 열 상태로 돌아가도록 조정 |

<br>

품질 조절은 **Scaler** 단위로 구성합니다. Scaler는 해상도 스케일, 프레임레이트, 그림자, LOD, 후처리처럼 개별 품질 항목을 조절하는 구성 요소입니다. **Indexer**는 열 상태와 성능 상태를 바탕으로 어떤 Scaler를 어느 정도 적용할지 결정하고, Scaler는 개발자가 미리 정한 범위 안에서 값을 조절합니다.

예를 들어 GPU 병목과 열 경고가 함께 나타난다면, 해상도 스케일이나 그림자 관련 Scaler를 먼저 낮추는 식으로 구성할 수 있습니다. 반대로 CPU 병목이 주요 원인이라면 렌더 해상도를 낮추는 것보다 오브젝트 수, 애니메이션, 물리 빈도처럼 CPU 부하에 영향을 주는 항목을 우선 조정하는 편이 적절합니다. 중요한 것은 모든 품질을 한 번에 낮추는 것이 아니라, 체감 영향이 작은 항목부터 단계적으로 조정하도록 범위와 우선순위를 미리 설계하는 것입니다.

### iOS의 Thermal State API

iOS에서도 목적은 같습니다. 기기의 열 상태를 읽고, 열 제한이 본격적으로 걸리기 전에 게임의 부하를 낮추는 것입니다. 다만 Android Adaptive Performance Provider처럼 Unity 패키지 안에서 상태 수집과 Scaler 조정을 함께 처리하기보다, Apple의 `ProcessInfo.thermalState`로 현재 시스템의 열 상태를 확인한 뒤 게임 쪽 품질 정책에 연결하는 방식으로 접근합니다. 이 값은 실제 온도 수치가 아니라, 앱이 부하를 줄여야 하는 정도를 나타내는 단계 정보입니다.

<br>

**iOS Thermal State (`ProcessInfo.thermalState`)**

| 상태 | 의미 |
|---|---|
| `.nominal` | 일반적인 열 상태. 별도 조정 없이 현재 품질 유지 가능 |
| `.fair` | 열 상태가 올라가는 단계. 체감이 작은 품질 항목부터 완만하게 조정 |
| `.serious` | 높은 열 상태. 해상도, 후처리, 그림자, 프레임레이트 등 부하를 적극적으로 낮춤 |
| `.critical` | 매우 높은 열 상태. 가능한 작업량을 최소화하고, 복구될 때까지 품질을 크게 낮춤 |

<br>

iOS에서는 `thermalState`를 한 번 읽는 것뿐 아니라, 상태 변화 알림을 받아 품질 정책에 연결하는 방식이 적절합니다. Unity 프로젝트에서는 Swift나 Objective-C 네이티브 플러그인으로 `thermalState`와 변경 알림을 C#에 전달하고, 상태에 따라 렌더 해상도, 후처리, 그림자, 목표 프레임레이트 같은 항목을 단계적으로 조정합니다.

### Adaptive Performance 없이 대응하기

Adaptive Performance Provider나 iOS Thermal State API를 사용할 수 없는 환경에서는 열 상태를 직접 알기 어렵습니다. 이 경우 프레임 시간 변화를 관찰해 쓰로틀링 가능성을 간접적으로 추정할 수 있습니다.

다만 프레임 시간 증가는 에셋 로딩, GC, 네트워크, 장면 복잡도 변화로도 발생할 수 있으므로, 단일 프레임 스파이크를 쓰로틀링으로 판단하면 안 됩니다. 같은 장면과 비슷한 작업량이 유지되는 상황에서 최근 몇 초 동안의 평균 프레임 시간이 점진적으로 길어지고, 이 상태가 일정 시간 이상 지속될 때 품질을 한 단계 낮추는 방식이 더 안전합니다. 품질을 복원할 때도 바로 되돌리기보다, 충분한 안정 구간과 쿨다운을 둬야 품질 단계가 자주 흔들리지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">프레임 시간 기반 대응 흐름</text>

  <rect x="48" y="52" width="150" height="64" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="123" y="76" text-anchor="middle" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="currentColor">프레임 시간 수집</text>
  <text x="123" y="98" text-anchor="middle" font-family="sans-serif" font-size="10.2" fill="currentColor">이동 평균 / P95 관찰</text>

  <line x1="198" y1="84" x2="238" y2="84" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="238,84 228,78 228,90" fill="currentColor"/>

  <rect x="238" y="52" width="154" height="64" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="315" y="76" text-anchor="middle" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="currentColor">지속 악화 확인</text>
  <text x="315" y="98" text-anchor="middle" font-family="sans-serif" font-size="10.2" fill="currentColor">스파이크는 제외</text>

  <line x1="392" y1="84" x2="432" y2="84" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="432,84 422,78 422,90" fill="currentColor"/>

  <rect x="432" y="52" width="140" height="64" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.4"/>
  <text x="502" y="76" text-anchor="middle" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="currentColor">품질 한 단계 조정</text>
  <text x="502" y="98" text-anchor="middle" font-family="sans-serif" font-size="10.2" fill="currentColor">부하 낮추기</text>

  <line x1="502" y1="116" x2="502" y2="150" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="502,150 496,140 508,140" fill="currentColor"/>

  <rect x="112" y="150" width="398" height="72" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="310" y="174" text-anchor="middle" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="currentColor">히스테리시스와 쿨다운</text>
  <text x="310" y="196" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">낮출 때와 복원할 때의 기준을 다르게 두고, 변경 후 일정 시간 대기</text>

  <line x1="310" y1="222" x2="310" y2="254" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="310,254 304,244 316,244" fill="currentColor"/>

  <rect x="58" y="254" width="220" height="70" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="168" y="278" text-anchor="middle" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="currentColor">계속 나빠지면</text>
  <text x="168" y="300" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">해상도, 그림자, LOD 등을 추가로 낮춤</text>

  <rect x="342" y="254" width="220" height="70" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="452" y="278" text-anchor="middle" font-family="sans-serif" font-size="11.5" font-weight="bold" fill="currentColor">충분히 안정되면</text>
  <text x="452" y="300" text-anchor="middle" font-family="sans-serif" font-size="10.5" fill="currentColor">천천히 품질을 복원</text>

  <text x="310" y="356" text-anchor="middle" font-family="sans-serif" font-size="10.8" fill="currentColor">목표는 정확한 온도 추정이 아니라, 지속적인 프레임 악화를 완만하게 대응하는 것</text>
</svg>
</div>

<br>

이 방식은 실제 온도나 클럭 상태를 직접 읽는 것이 아니므로 쓰로틀링을 정확히 판별하지는 못합니다. 대신 별도 플랫폼 API 없이도 적용할 수 있으므로, 열 상태 정보를 얻기 어려운 기기에서 보수적인 fallback으로 사용할 수 있습니다.

---

## 전력 예산

Adaptive Performance나 프레임 시간 모니터링은 열 상태가 나빠졌을 때 부하를 조절하는 대응책입니다. 하지만 장시간 안정적인 성능을 얻으려면, 애초에 게임이 사용하는 전력을 기기가 지속적으로 감당할 수 있는 범위 안에 두어야 합니다. 발열은 전력 소비의 결과이므로, 먼저 게임 실행 중 어떤 요소가 전력을 많이 쓰는지 파악해야 합니다.

### 전력 소비의 주요 요인

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">게임 실행 중 전력 소비에 영향을 주는 요소</text>
  <text x="290" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.68">실제 비중은 기기, 밝기, 장르, 네트워크 상태, 그래픽 설정에 따라 달라짐</text>

  <text x="160" y="76" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU</text>
  <rect x="170" y="64" width="245" height="18" rx="2" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1"/>
  <text x="426" y="76" font-family="sans-serif" font-size="10.5" fill="currentColor">렌더링 부하가 클수록 증가</text>

  <text x="160" y="104" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU</text>
  <rect x="170" y="92" width="170" height="18" rx="2" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1"/>
  <text x="351" y="104" font-family="sans-serif" font-size="10.5" fill="currentColor">스크립트·물리·애니메이션 부하</text>

  <text x="160" y="132" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">디스플레이</text>
  <rect x="170" y="120" width="150" height="18" rx="2" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="331" y="132" font-family="sans-serif" font-size="10.5" fill="currentColor">밝기·화면 톤에 영향</text>

  <text x="160" y="160" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">메모리 대역폭</text>
  <rect x="170" y="148" width="115" height="18" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="296" y="160" font-family="sans-serif" font-size="10.5" fill="currentColor">텍스처·렌더 타깃 접근</text>

  <text x="160" y="188" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">네트워크</text>
  <rect x="170" y="176" width="72" height="18" rx="2" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="253" y="188" font-family="sans-serif" font-size="10.5" fill="currentColor">온라인 상태·모뎀 품질 의존</text>

  <text x="160" y="216" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">기타 시스템</text>
  <rect x="170" y="204" width="54" height="18" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="235" y="216" font-family="sans-serif" font-size="10.5" fill="currentColor">오디오·센서·백그라운드 작업</text>

  <text x="290" y="260" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 프로젝트에서 큰 비중을 차지하는 요소를 측정한 뒤 우선 최적화</text>
</svg>
</div>

<br>

그래픽 부하가 큰 게임에서는 **GPU**가 주요 전력 소비원이 되는 경우가 많습니다. 프래그먼트 셰이더가 화면의 수많은 픽셀에서 텍스처 샘플링과 조명 계산을 수행하고, 렌더 타깃을 읽고 쓰기 때문입니다. **오버드로우(Overdraw)**가 심하면 같은 픽셀을 여러 번 처리하므로 GPU 작업량과 메모리 대역폭 사용량이 함께 증가합니다.

**CPU** 전력은 스크립트 실행, 물리 연산, 애니메이션 평가, UI 리빌드, 렌더 준비처럼 매 프레임 반복되는 작업에 영향을 받습니다. 모바일 SoC는 보통 고성능 코어와 고효율 코어를 함께 사용하며, 운영 체제 스케줄러가 부하와 열 상태에 따라 스레드를 배치합니다. 게임이 코어 배치를 직접 통제하기는 어렵지만, 메인 스레드의 지속 부하를 줄이고 불필요한 작업 빈도를 낮추면 고성능 코어를 오래 점유하는 시간을 줄일 수 있습니다.

**디스플레이** 전력은 화면 밝기, 주사율, 표시되는 색과 면적의 영향을 받습니다. 특히 **OLED** 디스플레이에서는 밝은 픽셀이 많을수록 소비 전력이 늘어날 수 있습니다. 다만 화면을 무조건 어둡게 만드는 것은 해법이 아닙니다. 가독성, 접근성, 아트 방향을 유지하면서 과도하게 밝은 전체 화면 효과, 긴 시간 유지되는 흰색 UI, 불필요한 최대 밝기 유도처럼 전력 소모를 키우는 요소를 줄이는 쪽으로 접근하는 편이 적절합니다.

### 메모리 대역폭과 전력

모바일 SoC에서 **메모리 대역폭(Memory Bandwidth)**은 GPU만의 자원이 아닙니다. CPU, GPU, 디스플레이 컨트롤러, 비디오 디코더, 운영 체제 작업이 같은 DRAM을 공유하며, 이들이 초당 읽고 쓰는 데이터량이 전체 대역폭과 전력 소비에 영향을 줍니다. 게임 실행 중에는 텍스처, 버퍼, 렌더 타깃을 반복해서 읽고 쓰는 렌더링 작업이 많기 때문에 GPU가 대역폭 사용량을 크게 끌어올리는 경우가 많습니다.

문제는 DRAM 접근이 칩 내부 캐시나 레지스터 접근보다 에너지 비용이 크다는 점입니다. 같은 장면을 그리더라도 큰 텍스처를 자주 읽고, 렌더 타깃을 여러 번 읽고 쓰고, CPU에서 만든 데이터를 GPU가 반복해서 참조하면 공유 DRAM 사용량이 늘어납니다. 따라서 메모리 대역폭 최적화는 외부 메모리에서 오가는 바이트 수와 접근 횟수를 줄이는 작업입니다. 텍스처 압축은 읽어야 할 데이터 크기를 줄이고, 밉맵은 축소되어 보이는 오브젝트에서 더 작은 텍스처 레벨을 샘플링하게 해 불필요한 고해상도 텍스처 접근을 줄입니다. 렌더 타깃 축소와 오버드로우 감소는 프레임 버퍼 접근을 줄이고, 불필요한 버퍼 복사 제거는 CPU와 GPU 사이의 데이터 이동을 줄입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">모바일 SoC의 공유 메모리 대역폭</text>
  <text x="310" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">CPU, GPU, 디스플레이와 시스템 작업이 같은 DRAM을 나누어 사용</text>

  <rect x="235" y="126" width="150" height="70" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="153" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공유 DRAM</text>
  <text x="310" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">메모리 대역폭</text>

  <rect x="42" y="70" width="150" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="117" y="92" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <text x="117" y="111" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">스크립트, 물리, AI</text>

  <rect x="428" y="70" width="150" height="54" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="503" y="92" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU</text>
  <text x="503" y="111" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">텍스처, 렌더 타깃</text>

  <rect x="42" y="218" width="150" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="117" y="240" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">디스플레이</text>
  <text x="117" y="259" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프레임 버퍼 읽기</text>

  <rect x="428" y="218" width="150" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="503" y="240" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">시스템 작업</text>
  <text x="503" y="259" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">비디오, OS, 네트워크</text>

  <line x1="192" y1="97" x2="235" y2="140" stroke="currentColor" stroke-width="1.2" opacity="0.75"/>
  <polygon points="229,140 238,143 235,134" fill="currentColor" opacity="0.75"/>
  <line x1="428" y1="97" x2="385" y2="140" stroke="currentColor" stroke-width="1.2" opacity="0.75"/>
  <polygon points="385,134 382,143 391,140" fill="currentColor" opacity="0.75"/>
  <line x1="192" y1="245" x2="235" y2="182" stroke="currentColor" stroke-width="1.2" opacity="0.75"/>
  <polygon points="237,188 238,179 230,184" fill="currentColor" opacity="0.75"/>
  <line x1="428" y1="245" x2="385" y2="182" stroke="currentColor" stroke-width="1.2" opacity="0.75"/>
  <polygon points="390,184 382,179 383,188" fill="currentColor" opacity="0.75"/>

  <text x="310" y="302" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 렌더링 부하가 큰 게임에서는 GPU 접근이 큰 비중을 차지하지만, 대역폭 자체는 SoC 전체가 공유</text>
</svg>
</div>

<br>

[렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 다룬 텍스처 압축과 밉맵은 전력 관점에서도 중요합니다. 텍스처 압축은 저장되는 텍스처 크기와 런타임 대역폭을 함께 줄입니다. 반면 밉맵은 전체 텍스처 메모리를 조금 더 사용하지만, 멀리 있거나 작게 보이는 오브젝트에서 낮은 해상도 레벨을 샘플링하게 해 캐시 효율을 높이고 대역폭 낭비를 줄입니다. 즉 압축은 메모리 사용량과 대역폭을 줄이는 기법이고, 밉맵은 추가 메모리를 감수하는 대신 샘플링 비용과 대역폭을 줄이는 기법에 가깝습니다.

셰이더 복잡도도 전력에 영향을 줍니다. 프래그먼트 셰이더에서 텍스처를 여러 장 샘플링하거나, 복잡한 라이팅 모델을 계산하거나, 분기(if-else)가 많으면 GPU의 연산량과 메모리 접근이 함께 늘어납니다. 텍스처 샘플링 최소화, 셰이더 분기 최소화, 라이팅 계산 단순화 같은 모바일 셰이더 최적화 기법은 실행 시간을 줄일 뿐 아니라, 공유 메모리 대역폭을 덜 사용하게 만들어 전력 효율도 개선합니다.

---

## 30fps vs 60fps — 프레임레이트의 트레이드오프

모바일 게임에서 목표 프레임레이트는 부드러움과 입력 반응성을 좌우하지만, 동시에 전력과 발열을 크게 바꾸는 설정입니다. 높은 프레임레이트가 항상 더 좋은 선택은 아니며, 장르의 조작 요구와 기기의 지속 성능을 함께 고려해야 합니다.

### 60fps의 비용

같은 장면을 같은 품질로 그린다면 60fps는 30fps보다 초당 프레임을 두 배 더 만들어야 합니다. 그만큼 CPU는 게임 로직과 렌더 준비를 더 자주 처리하고, GPU는 셰이더 실행과 렌더 타깃 쓰기를 더 자주 수행합니다. 동시에 각 프레임에 쓸 수 있는 시간은 33.33ms에서 16.67ms로 줄어들기 때문에, 작업을 끝낸 뒤 SoC가 쉬거나 낮은 클럭으로 내려갈 여지도 줄어듭니다.

예를 들어 한 프레임의 CPU/GPU 작업이 10ms 정도라면, 30fps에서는 33.33ms 예산 안에 비교적 긴 여유 시간이 남습니다. 이 시간 동안 운영 체제는 클럭과 전압을 낮추거나 일부 블록을 쉬게 하여 평균 전력을 낮출 수 있습니다. 반면 60fps에서는 프레임 예산이 16.67ms로 줄어들어 같은 작업이라도 유휴 시간이 크게 줄고, SoC가 더 높은 클럭과 전압을 유지하는 시간이 길어집니다. 앞에서 본 것처럼 동적 전력은 전압과 클럭의 영향을 크게 받기 때문에, 60fps는 평균 전력과 발열을 빠르게 끌어올릴 수 있습니다.

**30fps vs 60fps**

| 프레임레이트 | 프레임 예산 | 유휴 시간 | 클럭·전압 경향 | 전력·발열 경향 |
|---|---:|---|---|---|
| 30fps | 33.33ms | 상대적으로 많음 | 낮아질 여지 있음 | 상대적으로 낮음 |
| 60fps | 16.67ms | 상대적으로 적음 | 높은 상태가 오래 유지됨 | 상대적으로 높음 |

<br>

결과적으로 60fps는 30fps보다 더 부드럽고 입력 반응도 좋지만, 같은 품질을 유지한다면 기기가 더 빨리 뜨거워지고 배터리도 더 빠르게 소모됩니다. 냉각 여유가 작은 기기에서는 실행 초반에 60fps를 유지하더라도, 열이 누적된 뒤에는 클럭 제한으로 목표 프레임레이트를 계속 유지하기 어려울 수 있습니다.

### 30fps의 이점

30fps의 가장 큰 이점은 같은 품질을 유지할 때 초당 처리해야 하는 프레임 수가 줄어든다는 점입니다. 프레임 예산은 33.33ms로 길어지고, 한 프레임의 작업을 끝낸 뒤 남는 시간 동안 SoC가 낮은 클럭으로 내려갈 여지가 생깁니다. 이 차이는 순간 성능보다 평균 전력을 낮추는 데 중요하며, 결과적으로 열이 누적되는 속도를 늦출 수 있습니다.

이 여유를 어디에 사용할지는 별도의 결정입니다. 같은 그래픽 품질을 유지하면 평균 부하를 낮추는 데 도움이 되고, 남는 예산을 그림자, 후처리, 오브젝트 밀도 같은 항목에 사용하면 화면 품질을 높일 수 있습니다. 대신 그만큼 전력과 발열 이점은 줄어듭니다.

따라서 30fps는 단순히 성능을 낮추는 선택이 아니라, 부드러움과 입력 반응성, 화면 품질, 발열, 배터리 사이의 우선순위를 정하는 선택입니다. 조작 정밀도보다 장시간 안정성과 배터리 지속 시간이 중요한 장르에서는 30fps가 더 현실적인 기준이 될 수 있습니다.

### 장르별 판단

프레임레이트는 장르 이름만으로 결정하기보다, 플레이어가 얼마나 빠르게 반응해야 하는지와 한 세션을 얼마나 오래 유지해야 하는지를 기준으로 정하는 편이 안전합니다. 아래 표는 고정 규칙이 아니라 목표 프레임레이트를 정할 때의 출발점입니다.

**프레임레이트 선택 기준**

| 우선순위 | 적합한 목표 | 예시 |
|---|---|---|
| 장시간 안정성, 배터리, 화면 품질 | 30fps | 퍼즐, 방치형, 턴제 RPG, 전략 게임 |
| 입력 반응성, 조준, 판정 정확도 | 60fps | 경쟁 FPS, 격투, 리듬 게임, 실시간 대전 |
| 상황별 부하와 조작 강도가 크게 달라짐 | 30~60fps 동적 전환 | 탐색과 전투가 분리된 액션 RPG, 오픈월드 |

<br>

동적 전환을 사용할 때는 전환 시점이 중요합니다. 전투 중처럼 입력이 민감한 구간에서 30fps와 60fps를 자주 오가면 프레임 페이싱 변화가 바로 체감될 수 있습니다. 씬 전환, 로딩, 컷신, 메뉴 진입처럼 조작 부담이 낮은 시점에 `Application.targetFrameRate`를 바꾸고, 한 번 전환한 뒤에는 일정 시간 동안 같은 설정을 유지해야 합니다. 낮출 때와 다시 올릴 때의 조건도 다르게 두어야 프레임레이트가 짧은 간격으로 오르내리는 현상을 피할 수 있습니다. Unity 모바일 빌드에서는 목표 프레임레이트를 정할 때 `Application.targetFrameRate`를 우선 확인하고, 플랫폼별 동작은 실기기에서 검증합니다.

---

## 지속 성능 기준의 설계

프레임레이트와 품질 기준을 정했다면, 그 목표가 실제 플레이 시간 동안 유지되는지 확인해야 합니다. 모바일에서 중요한 것은 기기가 차가울 때 잠깐 도달한 최고 성능이 아니라, 열이 누적된 뒤에도 유지할 수 있는 프레임 시간과 품질입니다.

| 기준 | 설계 흐름 | 결과 |
|---|---|---|
| 피크 성능 기준 | 차가운 기기나 짧은 테스트에서 나온 프레임레이트를 기준으로 목표 설정 | 열이 누적된 뒤 클럭 제한이 걸리면 프레임 시간이 늘어나고 목표 프레임레이트를 유지하기 어려움 |
| 지속 성능 기준 | 기준 기기에서 실제 플레이 시나리오를 충분히 연속 실행한 뒤, 예열 후 프레임 시간과 열 상태를 기준으로 목표 설정 | 장시간 플레이에서 유지 가능한 프레임레이트, 해상도, 품질 수준을 정할 수 있음 |

<br>

프로파일링도 이 지속 성능 상태를 포함해야 합니다. 측정 시간은 고정된 숫자보다 프로젝트의 실제 플레이 세션과 기준 기기의 열 특성에 맞추는 편이 적절합니다. 기기가 차가운 초반 구간의 데이터만 보면 피크 성능은 알 수 있지만, 열이 오른 뒤 프레임 예산을 계속 지킬 수 있는지는 확인하기 어렵습니다.

---

## 마무리

이 글의 핵심은 모바일 성능을 순간적인 처리 속도가 아니라, 제한된 전력과 방열 조건 안에서 오래 유지할 수 있는 성능으로 봐야 한다는 점입니다.

- 모바일 SoC는 CPU, GPU, 메모리, 디스플레이가 좁은 전력·열 예산을 공유하므로, 한 부분의 부하 증가가 전체 지속 성능에 영향을 줄 수 있습니다.
- 서멀 쓰로틀링은 OS가 기기를 보호하기 위해 클럭과 전력 사용을 제한하는 과정이며, 게임 쪽에서는 평균 부하를 낮추고 품질을 단계적으로 조정해 대응해야 합니다.
- Adaptive Performance, iOS Thermal State API, 프레임 시간 모니터링은 열 상태 악화를 감지하는 수단이며, 실제 효과는 어떤 품질 항목을 언제 낮추는지에 따라 달라집니다.
- 전력 최적화는 GPU 연산만 줄이는 문제가 아닙니다. 반복되는 CPU 작업, 텍스처와 렌더 타깃 접근, 오버드로우, 디스플레이 밝기, 목표 프레임레이트가 모두 배터리와 발열에 영향을 줍니다.
- 30fps와 60fps의 선택은 단순한 화질 설정이 아니라, 부드러움과 입력 반응성, 화면 품질, 발열, 배터리 지속 시간 사이의 우선순위 결정입니다.
- 목표 프레임레이트와 품질은 차가운 기기의 피크 성능이 아니라, 기준 기기에서 열이 누적된 뒤에도 유지되는 지속 성능을 기준으로 정해야 합니다.

모바일 게임의 성능은 코드의 효율성만으로 결정되지 않습니다. 같은 코드라도 기기 크기, SoC, 방열 구조, 배터리 상태, 주변 온도에 따라 유지 가능한 품질이 달라집니다. 따라서 모바일 최적화는 “가장 빠른 순간”을 만드는 작업이 아니라, 실제 플레이 시간 동안 감당 가능한 부하를 설계하는 작업에 가깝습니다.

다음 단계는 이 원칙을 품질 설정과 빌드 전략으로 옮기는 것입니다. 기기 등급에 따라 해상도, 그림자, 셰이더, 에셋 압축, 스트리핑 수준을 나누어야 같은 게임도 다양한 모바일 기기에서 안정적으로 동작할 수 있습니다.

[Part 2](/dev/unity/MobileStrategy-2/)에서는 Quality Settings 계층 설계, 기기 등급 분류, IL2CPP 스트리핑, 에셋 압축 등 빌드와 품질 전략을 다룹니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- **모바일 전략 (1) - 발열과 배터리** (현재 글)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
