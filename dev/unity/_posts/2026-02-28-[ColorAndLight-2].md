---
layout: single
title: "색과 빛 (2) - 색 표현과 색공간 - soo:bak"
date: "2026-02-28 23:03:00 +0900"
description: RGB 색 모델, 감마 보정, 선형 색공간, sRGB, HDR, 톤 매핑을 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 색공간
  - 감마
  - 모바일
---

## 연속적인 빛을 디지털로

[색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)에서는 빛이 전자기파이며, 표면에서 반사·굴절·흡수로 나뉘고, 반사는 BRDF로 표현된다는 점을 살펴봤습니다. 이번 글의 출발점은 그 빛을 컴퓨터가 어떻게 숫자로 저장하고 계산하느냐입니다.

현실의 빛은 연속적인 물리량입니다. 밝기는 어두운 밤하늘부터 밝은 한낮까지 그 범위가 넓고, 색을 만드는 파장도 끊김 없이 이어집니다. 반면 컴퓨터는 이 값을 유한한 숫자로 나누어 저장해야 합니다. 그런데 밝기를 같은 간격으로 나누면, 어두운 영역에서 색이 띠처럼 끊겨 보이는 **밴딩(banding)**이 생기기 쉽습니다.

색을 일관되게 저장하고 계산하려면 두 가지 규칙이 필요합니다. **색 모델(Color Model)**은 색을 어떤 숫자 축으로 표현할지 정합니다. RGB는 빨강·초록·파랑 세 축을 사용합니다. **색공간(Color Space)**은 그 숫자가 실제 어떤 색과 밝기를 뜻하는지 정합니다. 같은 RGB 값이라도 원색 좌표, **백색점(White Point)**, **전달 함수(Transfer Function)**가 다르면 화면에 재현되는 색이 달라질 수 있습니다. 이번 글에서는 RGB 색 모델, 감마 보정, 선형 색공간, sRGB, HDR과 톤 매핑, Unity의 Color Space 설정을 차례로 다룹니다.

---

## RGB 색 모델

RGB는 빨강, 초록, 파랑 세 채널의 세기를 조합해 색을 표현하는 모델입니다. 이 표현이 화면에서 실제 색이 되려면 세 색의 빛을 어떻게 섞을지가 정해져야 하고, 그 색을 컴퓨터가 다루려면 각 채널의 세기를 어떤 숫자로 저장할지가 정해져야 합니다. 전자는 빛을 더해 색을 내는 가산 혼합으로, 후자는 채널마다 몇 비트를 배정하느냐의 문제로 이어집니다.

> RGB가 세 채널을 쓰는 이유, 즉 사람의 색 지각과 세 원색의 관계는 [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)에서 다룹니다.

### 가산 혼합

빛은 에너지여서, 서로 다른 색의 빛이 한곳에 겹치면 그 에너지가 더해져 밝아집니다. 이렇게 빛을 더해 색을 만드는 방식이 **가산 혼합(Additive Mixing)**입니다. 빨강과 초록을 더하면 노랑에 가까워지고, 빨강·초록·파랑을 모두 최대로 더하면 흰색이 됩니다.

물감이나 잉크는 반대로 작용합니다. 이들은 빛을 내는 것이 아니라 특정 파장의 빛을 흡수해 색을 만들므로, 여러 색을 섞을수록 흡수되는 파장이 늘어 반사되는 빛은 오히려 줄어듭니다. 더할수록 밝아지는 가산 혼합과 달리 섞을수록 어두워지는 이 방식이 **감산 혼합(Subtractive Mixing)**이며, 화면의 RGB 혼합과는 구분됩니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 380" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="가산 혼합 빛의 혼합 다이어그램: R+G=노랑, R+B=마젠타, G+B=시안, R+G+B=흰색">
  <rect width="620" height="380" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="32" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">가산 혼합 (빛의 혼합)</text>
  <!-- Clip paths for intersection regions -->
  <defs>
    <clipPath id="cR"><circle cx="310" cy="115" r="80"/></clipPath>
    <clipPath id="cG"><circle cx="242" cy="220" r="80"/></clipPath>
    <clipPath id="cB"><circle cx="378" cy="220" r="80"/></clipPath>
  </defs>
  <!-- Base circles (solid, no blend mode) -->
  <circle cx="310" cy="115" r="80" fill="#ff0000"/>
  <circle cx="242" cy="220" r="80" fill="#00ff00"/>
  <circle cx="378" cy="220" r="80" fill="#0000ff"/>
  <!-- Pairwise intersections -->
  <circle cx="242" cy="220" r="80" fill="#ffff00" clip-path="url(#cR)"/>
  <circle cx="378" cy="220" r="80" fill="#ff00ff" clip-path="url(#cR)"/>
  <circle cx="378" cy="220" r="80" fill="#00ffff" clip-path="url(#cG)"/>
  <!-- Triple intersection -->
  <g clip-path="url(#cR)">
    <circle cx="378" cy="220" r="80" fill="#ffffff" clip-path="url(#cG)"/>
  </g>
  <!-- Labels for primary circles -->
  <text x="310" y="88" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#ff6b6b">빨강 (R)</text>
  <text x="175" y="272" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#73f38f">초록 (G)</text>
  <text x="445" y="272" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="#00d4ff">파랑 (B)</text>
  <!-- Overlap labels (dark outline for readability on solid intersection fills) -->
  <text x="247" y="172" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#ffd700" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">노랑</text>
  <text x="247" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#ccc" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">(R+G)</text>
  <text x="373" y="172" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#ff00ff" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">마젠타</text>
  <text x="373" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#ccc" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">(R+B)</text>
  <text x="310" y="248" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#00ffff" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">시안</text>
  <text x="310" y="262" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#ccc" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">(G+B)</text>
  <text x="310" y="208" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#ffffff" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">흰색</text>
  <!-- Combination list -->
  <line x1="40" y1="296" x2="580" y2="296" stroke="#333" stroke-width="1"/>
  <text x="60" y="318" font-family="sans-serif" font-size="12" fill="#ccc">R + G = <tspan fill="#ffd700">노랑 (Yellow)</tspan></text>
  <text x="330" y="318" font-family="sans-serif" font-size="12" fill="#ccc">R + B = <tspan fill="#ff00ff">마젠타 (Magenta)</tspan></text>
  <text x="60" y="340" font-family="sans-serif" font-size="12" fill="#ccc">G + B = <tspan fill="#00ffff">시안 (Cyan)</tspan></text>
  <text x="330" y="340" font-family="sans-serif" font-size="12" fill="#ccc">R + G + B = <tspan fill="#ffffff">흰색 (White)</tspan></text>
  <text x="60" y="362" font-family="sans-serif" font-size="12" fill="#ccc">없음 = <tspan fill="#888">검정 (Black)</tspan></text>
</svg>

<br>

디스플레이는 이 원리를 픽셀 단위로 구현합니다. 모니터의 한 픽셀은 빨강·초록·파랑 서브픽셀로 이루어져 있고, 각 서브픽셀의 밝기를 따로 조절하면 세 빛이 더해져 하나의 색으로 보입니다. 우리가 화면에서 보는 색은 이렇게 세 서브픽셀의 세기를 조합한 결과입니다.

### 채널과 비트 깊이

RGB는 세 원색의 세기를 숫자로 저장합니다. R·G·B 각 채널 값은 흔히 0~255 정수 또는 0.0~1.0 부동소수점으로 표현됩니다.

<br>

**RGB 값의 표현 형식**

| 형식 | 범위 | 빨강 | 흰색 | 검정 |
|------|------|------|------|------|
| 정수 (8비트) | 0 ~ 255 (256단계) | (255, 0, 0) | (255, 255, 255) | (0, 0, 0) |
| 부동소수점 | 0.0 ~ 1.0 | (1.0, 0.0, 0.0) | (1.0, 1.0, 1.0) | (0.0, 0.0, 0.0) |

$$
\text{float} = \frac{\text{정수}}{255}, \quad \text{정수} = \text{float} \times 255
$$

표의 0.0~1.0 범위는 표준 동적 범위(SDR)를 기준으로 합니다. HDR 렌더링에서는 1.0을 넘는 값도 다루는데, 이 부분은 뒤에서 따로 살펴봅니다.

두 형식 가운데 셰이더 내부의 색 계산에는 주로 부동소수점을 씁니다. 빨간 표면 (1.0, 0.0, 0.0)에 조명 강도 0.5를 곱하면 결과는 (0.5, 0.0, 0.0)이 되어, 밝기가 절반으로 줄었다는 사실을 값에서 그대로 읽을 수 있습니다.

같은 계산을 0~255 정수로 하면 중간 결과를 다시 정수로 양자화해야 하므로 정밀도 손실이 생기기 쉽습니다. 따라서 저장과 표시에는 정수를 쓰더라도, 색을 더하고 곱하는 계산은 부동소수점으로 처리합니다.

한편 각 채널에 몇 비트를 배정하느냐는 표현할 수 있는 단계 수를 정합니다. 채널당 8비트면 $2^8$, 즉 256단계를 나타낼 수 있고, R·G·B 세 채널을 합친 24비트에서는 $256^3$, 약 1,677만 가지 색이 나옵니다.

색 외에 투명도가 필요하면 알파(Alpha) 채널을 더합니다. R·G·B·A 네 채널을 각각 8비트로 저장한 것이 R8G8B8A8, 즉 32비트 포맷입니다.

알파 값은 픽셀이 얼마나 불투명한지를 나타내며, 0은 완전 투명, 255는 완전 불투명입니다. 반투명 UI나 파티클을 그릴 때 이 값이 필요합니다. 다만 R8G8B8A8은 비압축 포맷이라, 실제 게임에서는 메모리와 대역폭을 줄이려고 ASTC나 ETC2 같은 압축 포맷을 함께 쓰는 일이 흔합니다.

24비트로 담는 약 1,677만 색은, 사람이 실제로 구분하는 수백만에서 천만 사이의 색보다 오히려 많습니다. 색의 가짓수만 놓고 보면 24비트는 넉넉합니다.

정작 문제는 색의 가짓수가 아니라, 각 단계가 실제 밝기에 어떤 간격으로 놓이느냐입니다. 단계를 밝기에 선형으로 대응시키면 어두운 영역과 밝은 영역이 같은 수의 단계를 나눠 갖습니다. 그런데 사람 눈은 어두운 쪽의 밝기 차이에 더 민감하기 때문에, 이 영역에 단계가 모자라면 밴딩이 눈에 띄게 드러납니다.

이 단계 배분을 다루는 것이 다음에 살펴볼 감마 보정입니다. 단계를 밝기에 고르게 깔지 않고 어두운 영역에 더 촘촘하게 몰아주면, 같은 256단계로도 더 매끄러운 밝기 변화를 얻을 수 있습니다.

---

## 감마 보정

감마 보정은 숫자로 저장한 밝기 값과 실제 화면 밝기 사이의 비선형 관계를 다루는 방식입니다. 출발점은 초기 디스플레이였던 CRT의 물리적 특성이지만, 지금도 제한된 비트 깊이를 사람의 밝기 지각에 맞게 배분하는 기준으로 사용됩니다.

### CRT 모니터의 비선형 응답

**CRT(Cathode Ray Tube)** 모니터는 입력 전압과 화면 밝기가 선형으로 대응하지 않았습니다. 이러한 응답은 전자총과 형광체의 특성에 따른 것으로, 거듭제곱 함수로 근사할 수 있습니다.

<br>

$$
\text{출력 밝기} = \text{입력값}^{\gamma} \quad (\gamma \approx 2.2)
$$

지수 $\gamma$가 약 2.2이면 중간 입력값은 출력에서 더 어둡게 나타납니다. 양 끝 값인 0.0과 1.0은 그대로 유지되지만, 중간값 0.5는 $0.5^{2.2} \approx 0.218$이 됩니다. 즉 입력 0.5가 물리적 밝기 50%가 아니라 약 22% 수준으로 출력됩니다.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="CRT의 비선형 응답 그래프: 감마 2.2 곡선과 선형 기준선 비교, 입력 0.5에서 출력 약 0.218">
  <rect width="620" height="340" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">CRT의 비선형 응답</text>
  <!-- Axes -->
  <line x1="90" y1="60" x2="90" y2="292" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <line x1="88" y1="290" x2="552" y2="290" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <!-- Y-axis labels -->
  <text x="78" y="294" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">0.0</text>
  <line x1="85" y1="175" x2="90" y2="175" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="78" y="179" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">0.5</text>
  <text x="78" y="64" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">1.0</text>
  <!-- X-axis labels -->
  <text x="90" y="307" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">0.0</text>
  <line x1="320" y1="290" x2="320" y2="295" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="320" y="307" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">0.5</text>
  <text x="550" y="307" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">1.0</text>
  <text x="320" y="325" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">입력값</text>
  <text x="18" y="175" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6" transform="rotate(-90, 18, 175)">출력 밝기</text>
  <!-- Linear reference (dashed) -->
  <line x1="90" y1="290" x2="550" y2="60" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.5"/>
  <text x="430" y="125" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">선형 (y=x)</text>
  <!-- Gamma curve y=x^2.2 -->
  <path d="M 90,290 C 150,288 230,275 320,240 S 460,120 550,60" fill="none" stroke="currentColor" stroke-width="2.5"/>
  <text x="210" y="232" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">감마 2.2</text>
  <!-- Annotation: x=0.5 → y≈0.218 -->
  <line x1="320" y1="290" x2="320" y2="240" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3" opacity="0.7"/>
  <line x1="90" y1="240" x2="320" y2="240" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3" opacity="0.7"/>
  <circle cx="320" cy="240" r="4" fill="currentColor"/>
  <text x="326" y="237" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">입력 0.5 → 출력 ≈ 0.218</text>
  <text x="78" y="244" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">0.218</text>
</svg>

<br>

이처럼 출력 밝기가 입력의 거듭제곱을 따르는 응답을 **감마 응답(Gamma Response)**이라고 부릅니다. 이 응답은 본래 CRT의 물리 구조에서 나왔지만, CRT가 사라진 뒤에도 LCD와 OLED는 같은 곡선을 재현합니다. 기존 사진, 영상, 텍스처가 모두 이 감마 응답을 전제로 만들어졌기 때문입니다. 디스플레이가 입력에 선형으로 응답하면 기존 콘텐츠가 의도와 다르게 보이므로, 오늘날 디스플레이도 대체로 감마 약 2.2에 가까운 응답을 따릅니다.

### 감마 보정이 필요한 이유

감마 보정이 필요한 이유는 사람이 밝기를 느끼는 방식에 있습니다. 눈은 같은 크기의 물리적 밝기 차이라도 어두운 영역에서는 또렷하게 구분하지만, 밝은 영역에서는 그 차이를 잘 알아채지 못합니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 280" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="인간의 밝기 인지: 동일한 25% 물리적 간격이 어두운 쪽에서는 크게, 밝은 쪽에서는 작게 느껴진다">
  <rect width="620" height="280" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">인간의 밝기 인지</text>
  <!-- Gradient bar -->
  <defs>
    <linearGradient id="bwGrad5" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
  </defs>
  <rect x="50" y="55" width="520" height="44" fill="url(#bwGrad5)" rx="4"/>
  <rect x="50" y="55" width="520" height="44" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4" rx="4"/>
  <!-- Tick marks -->
  <line x1="50"  y1="99" x2="50"  y2="108" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <line x1="180" y1="99" x2="180" y2="108" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <line x1="310" y1="99" x2="310" y2="108" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <line x1="440" y1="99" x2="440" y2="108" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <line x1="570" y1="99" x2="570" y2="108" stroke="currentColor" stroke-width="1.5" opacity="0.45"/>
  <text x="50"  y="120" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">0%</text>
  <text x="180" y="120" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">25%</text>
  <text x="310" y="120" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">50%</text>
  <text x="440" y="120" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">75%</text>
  <text x="570" y="120" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">100%</text>
  <!-- Bracket annotations above bar -->
  <path d="M 50,50 L 50,44 L 180,44 L 180,50" fill="none" stroke="currentColor" stroke-width="2"/>
  <text x="115" y="40" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">크게 느낌</text>
  <path d="M 440,50 L 440,44 L 570,44 L 570,50" fill="none" stroke="currentColor" stroke-width="2" opacity="0.5"/>
  <text x="505" y="40" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">작게 느낌</text>
  <!-- Arrow thickness visual -->
  <line x1="50" y1="145" x2="175" y2="145" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>
  <polygon points="175,138 190,145 175,152" fill="currentColor"/>
  <text x="118" y="166" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">인지 차이 큼</text>
  <line x1="180" y1="145" x2="305" y2="145" stroke="currentColor" stroke-width="4" stroke-linecap="round" opacity="0.7"/>
  <polygon points="305,140 318,145 305,150" fill="currentColor" opacity="0.7"/>
  <line x1="315" y1="145" x2="435" y2="145" stroke="currentColor" stroke-width="3" stroke-linecap="round" opacity="0.6"/>
  <polygon points="435,141 448,145 435,149" fill="currentColor" opacity="0.6"/>
  <line x1="445" y1="145" x2="565" y2="145" stroke="currentColor" stroke-width="2" stroke-linecap="round" opacity="0.5"/>
  <polygon points="565,141 578,145 565,149" fill="currentColor" opacity="0.5"/>
  <text x="512" y="166" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">인지 차이 작음</text>
  <!-- Separator and explanation -->
  <line x1="40" y1="185" x2="580" y2="185" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="310" y="210" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.65">물리적으로 동일한 25% 간격이지만,</text>
  <text x="310" y="230" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.65">어두운 쪽에서는 차이를 <tspan fill="currentColor" opacity="1" font-weight="bold">크게 느끼고</tspan></text>
  <text x="310" y="250" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.65">밝은 쪽에서는 차이를 <tspan fill="currentColor" opacity="0.5">작게 느낀다</tspan></text>
</svg>

<br>

이 인지 특성을 무시하고 256단계를 물리적 밝기에 고르게 배분하면 문제가 생깁니다. 어두운 영역에서는 단계가 모자라 밴딩이 드러나고, 밝은 영역에서는 사람이 구분하지 못하는 차이에 단계가 낭비됩니다. 감마 보정은 바로 이 특성에 맞춰, 같은 256단계를 어두운 영역에는 촘촘하게, 밝은 영역에는 성기게 나눕니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 320" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="선형 배분 대 감마 보정 배분 비교: 선형 배분은 어두운 영역 단계 부족으로 밴딩 발생, 감마 보정은 어두운 영역에 단계를 집중하여 부드러운 그라데이션">
  <rect width="620" height="320" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">선형 배분 vs 감마 보정 배분</text>
  <!-- Linear bar -->
  <text x="50" y="58" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">선형 배분</text>
  <defs>
    <linearGradient id="bwGrad6a" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
    <linearGradient id="bwGrad6b" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
  </defs>
  <rect x="50" y="65" width="520" height="42" fill="url(#bwGrad6a)" rx="3"/>
  <rect x="50" y="65" width="520" height="42" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4" rx="3"/>
  <g stroke="#ffffff" stroke-width="1" opacity="0.6">
    <line x1="83"  y1="65" x2="83"  y2="107"/>
    <line x1="116" y1="65" x2="116" y2="107"/>
    <line x1="148" y1="65" x2="148" y2="107"/>
    <line x1="181" y1="65" x2="181" y2="107"/>
    <line x1="213" y1="65" x2="213" y2="107"/>
    <line x1="246" y1="65" x2="246" y2="107"/>
    <line x1="278" y1="65" x2="278" y2="107"/>
    <line x1="311" y1="65" x2="311" y2="107"/>
    <line x1="343" y1="65" x2="343" y2="107"/>
    <line x1="376" y1="65" x2="376" y2="107"/>
    <line x1="408" y1="65" x2="408" y2="107"/>
    <line x1="441" y1="65" x2="441" y2="107"/>
    <line x1="473" y1="65" x2="473" y2="107"/>
    <line x1="506" y1="65" x2="506" y2="107"/>
    <line x1="538" y1="65" x2="538" y2="107"/>
  </g>
  <text x="52" y="125" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">어두운 영역: 단계 적음 → 밴딩 발생</text>
  <text x="390" y="125" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">밝은 영역: 단계 많음 → 비트 낭비</text>
  <line x1="40" y1="148" x2="580" y2="148" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <!-- Gamma bar -->
  <text x="50" y="172" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">감마 보정 배분</text>
  <rect x="50" y="178" width="520" height="42" fill="url(#bwGrad6b)" rx="3"/>
  <rect x="50" y="178" width="520" height="42" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4" rx="3"/>
  <!-- tick positions = (i/16)^2.2 * 520 + 50 (gamma encoding on physical brightness axis) -->
  <g stroke="#ffffff" stroke-width="1" opacity="0.6">
    <line x1="51"  y1="178" x2="51"  y2="220"/>
    <line x1="55"  y1="178" x2="55"  y2="220"/>
    <line x1="63"  y1="178" x2="63"  y2="220"/>
    <line x1="75"  y1="178" x2="75"  y2="220"/>
    <line x1="90"  y1="178" x2="90"  y2="220"/>
    <line x1="110" y1="178" x2="110" y2="220"/>
    <line x1="134" y1="178" x2="134" y2="220"/>
    <line x1="163" y1="178" x2="163" y2="220"/>
    <line x1="196" y1="178" x2="196" y2="220"/>
    <line x1="234" y1="178" x2="234" y2="220"/>
    <line x1="275" y1="178" x2="275" y2="220"/>
    <line x1="321" y1="178" x2="321" y2="220"/>
    <line x1="370" y1="178" x2="370" y2="220"/>
    <line x1="424" y1="178" x2="424" y2="220"/>
    <line x1="481" y1="178" x2="481" y2="220"/>
  </g>
  <text x="52" y="238" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">어두운 영역: 단계 많음 → 부드러운 그라데이션</text>
  <text x="390" y="238" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">밝은 영역: 단계 적음</text>
  <text x="390" y="253" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">→ 인간은 차이 못 느낌</text>
  <line x1="40" y1="272" x2="580" y2="272" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="310" y="294" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">감마 보정은 인간의 비선형 밝기 인지에 맞게 256단계를 재분배한다</text>
</svg>

<br>

이처럼 단계를 다시 나누는 일은 이미지를 저장할 때의 인코딩으로 이루어집니다. **감마 보정(Gamma Correction)**은 선형 밝기 값을 감마의 역수, 즉 약 $1/2.2$ 거듭제곱으로 인코딩하여 비선형 값으로 만드는 처리입니다. 이 값은 화면에 표시될 때 디스플레이의 감마 응답을 거치면서 다시 원래 밝기에 가까워집니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 420" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="감마 인코딩 디코딩 과정: 물리적 밝기 값에서 감마 인코딩, 저장, 모니터 감마 응답을 거쳐 원래 밝기로 복원되는 파이프라인">
  <rect width="620" height="420" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">감마 인코딩/디코딩 과정</text>
  <!-- Box 1 -->
  <rect x="165" y="50" width="290" height="46" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="2" rx="6"/>
  <text x="310" y="78" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">물리적 밝기 값 (선형)</text>
  <!-- Arrow 1 -->
  <line x1="310" y1="96" x2="310" y2="150" stroke="currentColor" stroke-width="2"/>
  <polygon points="303,148 310,164 317,148" fill="currentColor"/>
  <text x="310" y="128" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">감마 인코딩: 값^(1/2.2)</text>
  <!-- Box 2 -->
  <rect x="165" y="165" width="290" height="46" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="2" rx="6"/>
  <text x="310" y="193" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">저장된 값 (감마 공간)</text>
  <!-- Arrow 2 -->
  <line x1="310" y1="211" x2="310" y2="265" stroke="currentColor" stroke-width="2"/>
  <polygon points="303,263 310,279 317,263" fill="currentColor"/>
  <text x="310" y="243" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">모니터 감마 응답: 값^2.2</text>
  <!-- Box 3 -->
  <rect x="165" y="280" width="290" height="46" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="2" rx="6"/>
  <text x="310" y="308" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">화면 출력 밝기 (선형)</text>
  <!-- Separator -->
  <line x1="40" y1="346" x2="580" y2="346" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <!-- Round-trip example -->
  <text x="50" y="368" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">순환 예시</text>
  <text x="50" y="388" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">물리적 밝기 <tspan fill="currentColor" opacity="1" font-weight="bold">0.5</tspan></text>
  <text x="155" y="388" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">→ 인코딩</text>
  <text x="232" y="388" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">0.729</text>
  <text x="277" y="388" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">→ 저장</text>
  <text x="320" y="388" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">(8비트 ≈ 186)</text>
  <text x="420" y="388" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">→ 디코딩</text>
  <text x="490" y="388" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">0.5 복원</text>
  <line x1="40" y1="398" x2="580" y2="398" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="310" y="415" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">두 변환이 상쇄되어 원래의 물리적 밝기가 복원됨</text>
</svg>

<br>

저장할 때의 $1/2.2$ 거듭제곱과 디스플레이의 $2.2$ 거듭제곱 응답은 서로 역방향이라, 둘을 차례로 거치면 원래 밝기가 그대로 복원됩니다. 이렇게 감마 보정은 제한된 단계를 사람의 밝기 지각에 맞게 배분하면서도, 최종 출력에서는 의도한 밝기 분포를 그대로 재현합니다.

---

## 선형 색공간

감마 보정은 이미지를 저장하고 표시하는 데 유용합니다. 하지만 셰이더가 빛을 더하고 곱하는 조명 계산에서는 감마 인코딩된 값을 그대로 사용할 수 없습니다. 이 값은 물리적 에너지에 비례하지 않으므로, 조명 계산만큼은 **선형 공간(Linear Space)**에서 이루어져야 합니다.

### 조명 계산에서의 문제

조명을 선형 공간에서 계산해야 하는 이유는 선형 공간의 값이 물리적 에너지와 비례하기 때문입니다. 선형 공간에서 값 0.5는 최대 밝기의 50%, 값 0.25는 25%를 뜻합니다. 숫자를 에너지 비율로 직접 사용할 수 있습니다.

반면 감마 공간의 값은 에너지와 비례하지 않습니다. 감마 인코딩된 값 0.5는 실제 선형 밝기로 환산하면 약 22%에 가깝습니다. 이 값을 디코딩하지 않고 조명 계산에 사용하면 빛의 합산과 감쇠가 실제 에너지 계산과 달라집니다.

**선형 공간에서의 올바른 결과:**

$$
\text{빛 A}(0.5) + \text{빛 B}(0.5) = 1.0 \quad (50\% + 50\% = 100\%) \checkmark
$$

<br>

**감마 공간에서의 계산:**

$$
0.5^{2.2} \approx 0.218 \quad \Rightarrow \quad \text{빛 A의 실제 물리적 밝기} \approx 22\%
$$

$$
0.5^{2.2} \approx 0.218 \quad \Rightarrow \quad \text{빛 B의 실제 물리적 밝기} \approx 22\%
$$

<br>

감마 인코딩된 값 0.5 두 개를 디코딩 없이 더하면 계산 결과는 1.0이 됩니다. 하지만 실제 선형 밝기로 보면 각 값은 약 0.218이므로, 물리적으로 더한 값은 0.436에 가깝습니다. 감마 공간에서 더한 1.0은 올바른 0.436보다 큰 값이라, 화면에서 거의 최대 밝기에 이릅니다. 이처럼 감마 공간에서 조명을 계산하면 결과가 의도보다 밝은 쪽으로 치우칩니다.

이 문제는 덧셈에만 한정되지 않습니다. 곱셈, 보간, 감쇠 계산도 모두 비선형 값 위에서 수행되면 물리적 의미가 달라집니다. 조명이 많거나 반사 계산이 여러 단계로 쌓일수록 작은 오차가 누적되어 더 눈에 띄는 결과가 됩니다.

### 선형 공간에서의 조명 계산

선형 공간에서는 값이 에너지와 비례하므로 빛의 덧셈과 곱셈을 물리적 비율로 해석할 수 있습니다.

$$
0.8 \times 0.5 = 0.4 \quad (80\%\text{의 }50\% = 40\%) \checkmark
$$

이 성질은 표면 반사 계산에서 중요합니다. 표면의 **Albedo(반사율)**에 입사광 밝기를 곱하면 표면이 반사하는 빛의 양을 얻습니다. 선형 공간에서는 이 곱셈이 물리적 비율과 일치합니다.

$$
\text{Albedo}(0.6) \times \text{빛}(0.8) = 0.48 \quad (\text{올바른 반사량}) \checkmark
$$

---

## 감마 워크플로우 vs 선형 워크플로우

조명 계산은 선형 공간에서 해야 하지만, 셰이더로 들어오는 입력도 화면으로 나가는 출력도 선형이 아닙니다. 색상 텍스처는 대개 sRGB로 인코딩되어 저장되고, 디스플레이도 감마 응답을 거쳐 화면 밝기를 출력합니다.

그래서 선형으로 계산하려면 입력을 선형으로 디코딩하고, 계산이 끝난 출력을 다시 sRGB로 인코딩해야 합니다. 이 변환을 건너뛰고 감마 값을 그대로 계산에 쓰면 감마 워크플로우이고, 변환을 거쳐 계산 구간을 선형으로 유지하면 선형 워크플로우입니다.

### 감마 워크플로우

감마 워크플로우는 텍스처의 감마 인코딩 값을 선형으로 디코딩하지 않고 그대로 셰이더에 넘깁니다. 셰이더 결과도 별도의 선형-감마 변환 없이 화면으로 보냅니다.

파이프라인은 단순하지만, 셰이더는 감마 공간의 값을 선형 값처럼 사용하게 됩니다. 덧셈과 곱셈이 실제 에너지 비율과 맞지 않으므로 밝기 왜곡이 생길 수 있습니다.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 420" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="감마 워크플로우 파이프라인 다이어그램">
  <rect width="620" height="420" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">감마 워크플로우</text>
  <!-- Box 1: 텍스처 -->
  <rect x="170" y="56" width="280" height="44" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.6" rx="6"/>
  <text x="310" y="83" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">텍스처 (감마 공간)</text>
  <!-- Arrow 1 -->
  <line x1="310" y1="100" x2="310" y2="138" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <polygon points="310,144 305,134 315,134" fill="currentColor" opacity="0.5"/>
  <text x="310" y="122" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">변환 없이 그대로 사용</text>
  <!-- Box 2: 셰이더 조명 계산 (문제) -->
  <rect x="140" y="148" width="340" height="44" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="2.5" rx="6"/>
  <text x="310" y="175" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">셰이더 조명 계산 (감마 공간)</text>
  <!-- Arrow 2 -->
  <line x1="310" y1="192" x2="310" y2="230" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <polygon points="310,236 305,226 315,226" fill="currentColor" opacity="0.5"/>
  <text x="310" y="214" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">결과를 그대로 출력</text>
  <!-- Box 3: 프레임 버퍼 -->
  <rect x="170" y="240" width="280" height="44" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6" rx="6"/>
  <text x="310" y="267" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">프레임 버퍼 (감마 공간)</text>
  <!-- Arrow 3 -->
  <line x1="310" y1="284" x2="310" y2="322" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <polygon points="310,328 305,318 315,318" fill="currentColor" opacity="0.5"/>
  <text x="310" y="306" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">모니터 감마 응답</text>
  <!-- Box 4: 화면 출력 -->
  <rect x="170" y="332" width="280" height="44" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6" rx="6"/>
  <text x="310" y="359" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">화면 출력</text>
  <!-- Warning note -->
  <rect x="60" y="392" width="500" height="20" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5" rx="6"/>
  <text x="310" y="407" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">⚠ 조명 계산이 감마 공간에서 수행됨 → 물리적으로 부정확</text>
</svg>

### 선형 워크플로우

선형 워크플로우는 셰이더가 조명을 계산하기 전에 색상 입력을 선형 공간으로 변환합니다. sRGB 텍스처를 샘플링할 때 GPU가 값을 선형으로 디코딩하면, 셰이더의 조명 계산은 선형 공간에서 진행됩니다.

계산 결과는 선형 상태로 렌더 타깃에 저장됩니다. HDR을 사용하는 경우 이 값은 1.0을 넘을 수 있고, 이후 노출과 톤 매핑을 거쳐 LDR 범위로 압축됩니다. 최종 출력 직전에는 sRGB로 인코딩되어 디스플레이의 감마 응답과 맞춰집니다.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 556" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="선형 워크플로우 파이프라인 다이어그램">
  <rect width="620" height="556" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">선형 워크플로우</text>
  <!-- Box 1: 텍스처 -->
  <rect x="160" y="56" width="300" height="44" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6" rx="6"/>
  <text x="310" y="83" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">텍스처 (sRGB)</text>
  <!-- Arrow 1: sRGB → Linear -->
  <line x1="310" y1="100" x2="310" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="310,144 305,134 315,134" fill="currentColor"/>
  <text x="310" y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">sRGB → Linear 디코딩 (sRGB 설정 시 GPU 자동)</text>
  <!-- Box 2: 셰이더 조명 계산 -->
  <rect x="130" y="148" width="360" height="44" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="2.5" rx="6"/>
  <text x="310" y="175" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">셰이더 조명 계산 (선형 공간)</text>
  <!-- Arrow 2: 선형 저장 -->
  <line x1="310" y1="192" x2="310" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="310,236 305,226 315,226" fill="currentColor"/>
  <text x="310" y="214" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">선형 값 저장</text>
  <!-- Box 3: 렌더 타깃 (HDR) -->
  <rect x="140" y="240" width="340" height="44" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6" rx="6"/>
  <text x="310" y="267" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">렌더 타깃 (선형 · HDR)</text>
  <!-- Arrow 3: 톤 매핑 + sRGB 인코딩 -->
  <line x1="310" y1="284" x2="310" y2="332" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="310,338 305,328 315,328" fill="currentColor"/>
  <text x="310" y="308" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">노출 · 톤 매핑 · Linear → sRGB 인코딩</text>
  <!-- Box 4: 최종 프레임 버퍼 -->
  <rect x="160" y="342" width="300" height="44" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6" rx="6"/>
  <text x="310" y="369" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">최종 프레임 버퍼 (sRGB)</text>
  <!-- Arrow 4: 모니터 -->
  <line x1="310" y1="386" x2="310" y2="424" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <polygon points="310,430 305,420 315,420" fill="currentColor" opacity="0.5"/>
  <text x="310" y="408" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">모니터 감마 응답</text>
  <!-- Box 5: 화면 출력 -->
  <rect x="160" y="434" width="300" height="44" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.6" rx="6"/>
  <text x="310" y="461" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">화면 출력</text>
  <!-- Success note -->
  <rect x="60" y="498" width="500" height="42" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="6"/>
  <text x="310" y="516" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">✓ 조명 계산이 선형 공간에서 수행됨 → 물리적으로 정확</text>
  <text x="310" y="532" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.6">sRGB 디코딩/인코딩은 sRGB 설정 시 GPU 하드웨어가 자동 수행</text>
</svg>

이 디코딩과 인코딩을 셰이더 코드에서 직접 작성할 필요는 없습니다. 텍스처와 렌더 타깃의 sRGB 설정이 올바르면 GPU가 샘플링과 기록 시점에 변환을 처리합니다. 변환은 입출력 경계에서 일어나고, 그 사이의 조명 계산은 선형 공간에서 유지됩니다.

### 두 워크플로우의 시각적 차이

두 워크플로우의 차이는 화면에서도 드러납니다. 같은 씬과 같은 조명을 사용해도 감마 공간 계산과 선형 공간 계산은 중간 톤, 감쇠, 그라데이션에서 다른 결과를 만듭니다.

감마 워크플로우에서는 중간 톤이 필요 이상으로 밝아지거나, 조명 감쇠와 그라데이션이 부자연스럽게 보일 수 있습니다. 선형 워크플로우에서는 빛의 합산과 감쇠가 물리적 비율에 더 가깝게 계산되므로, PBR 머티리얼과 조명이 더 일관된 결과를 냅니다.

이 차이는 PBR에서 특히 중요합니다. PBR의 Cook-Torrance BRDF는 빛의 반사를 물리적으로 모델링하며, 선형 공간 계산을 전제로 합니다. 감마 워크플로우에서 PBR 머티리얼을 사용하면 수식의 전제가 깨져 재질 표현이 의도와 달라질 수 있습니다. PBR 프로젝트에서는 선형 워크플로우를 기본으로 삼는 편이 안전합니다.

> PBR이 미세면 이론을 바탕으로 에너지 보존과 프레넬 효과를 수식에 내장하는 방식, 그리고 그것이 왜 선형 공간 계산을 전제하는지는 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

---

## sRGB

RGB 값 (1, 0, 0)만으로는 그것이 어떤 빨강인지, 중간값 0.5가 실제로 얼마나 밝은지 알 수 없습니다. 숫자에 실제 색과 밝기를 묶어 줄 공통 기준이 있어야 하는데, 이를 정해 둔 사실상의 표준 색공간이 sRGB입니다.

### sRGB란

**sRGB(Standard Red Green Blue)**는 Microsoft와 HP가 정의한 표준 색공간입니다. 빨강·초록·파랑 원색의 색 좌표, 기준 흰색인 D65 백색점, 그리고 밝기를 인코딩하는 전달 함수를 함께 규정합니다. 이 기준이 정해져 있어야 장치가 달라도 같은 RGB 숫자를 같은 색에 가깝게 재현할 수 있습니다.

sRGB는 모니터, 카메라, 웹 브라우저, 이미지 편집 도구에서 기본 색공간으로 널리 사용됩니다. 게임의 색상 텍스처도 대부분 sRGB를 기준으로 저장됩니다.

sRGB의 전달 함수는 단순한 하나의 거듭제곱 함수가 아닙니다. 어두운 구간에서는 선형에 가까운 함수를 쓰고, 나머지 구간에서는 지수 2.4의 거듭제곱 함수를 적용합니다.

그런데 전체 곡선을 단일 거듭제곱 함수로 근사하면 실효 감마(effective gamma)가 약 2.2에 가깝습니다. 그래서 sRGB를 설명할 때 흔히 “감마 약 2.2”라고 부릅니다.

텍스처는 담은 데이터의 성격에 따라 sRGB로 읽을지, 선형 값으로 읽을지가 달라집니다. Albedo나 UI 이미지처럼 눈에 보이는 색을 담은 텍스처는 보통 sRGB로 저장합니다.

반면 노멀맵의 법선 벡터나 메탈릭·러프니스 맵의 물리 파라미터처럼 색이 아니라 수치를 담은 데이터 텍스처는 선형 값으로 읽어야 합니다. 이런 텍스처의 값은 색 지각을 위한 감마 인코딩 대상이 아니라, 셰이더가 그대로 사용하는 데이터이기 때문입니다.

이 구분은 GPU의 텍스처 샘플링에서 중요합니다. sRGB 텍스처를 샘플링하면 GPU는 값을 선형으로 디코딩해 셰이더에 전달합니다. 하지만 이미 선형인 데이터 텍스처에 이 디코딩이 적용되면 값 자체가 달라집니다.

예를 들어 노멀맵의 값 0.5가 sRGB 디코딩을 거치면 약 0.218로 내려갑니다. 그러면 셰이더는 의도와 다른 법선 방향으로 조명을 계산하게 됩니다. 데이터 텍스처에서 sRGB를 끄는 것은 이 때문입니다.

### 텍스처 임포트 설정

Unity에서는 텍스처를 sRGB로 읽을지 선형으로 읽을지를 임포트 설정의 **sRGB(Color Texture)** 체크박스로 제어합니다. 눈에 보이는 색을 담은 텍스처는 켜서 sRGB로, 수치를 담은 데이터 텍스처는 꺼서 선형으로 읽도록 지정합니다.

<br>

| 텍스처 유형 | sRGB | 이유 |
|---|---|---|
| Albedo / Base Color | 켜기 | sRGB 인코딩된 색상 |
| Emission | 켜기 | sRGB 인코딩된 색상 |
| UI Sprite | 켜기 | sRGB 인코딩된 색상 |
| Normal Map | 끄기 | 방향 벡터 — 선형 값 그대로 |
| Metallic Map | 끄기 | 물리 파라미터 — 선형 값 그대로 |
| Roughness/Smoothness | 끄기 | 물리 파라미터 — 선형 값 그대로 |
| Height Map | 끄기 | 높이 스칼라 — 선형 값 그대로 |
| Occlusion Map | 끄기 | 차폐 계수 — 선형 값 그대로 |

<br>

sRGB를 잘못 설정하면 그 결과가 화면에 곧바로 드러납니다. 노멀맵에 sRGB를 켜 두면 법선 방향이 틀어지고, Albedo 같은 색상 텍스처에서 sRGB를 꺼 두면 색이 선형으로 변환되지 않아 의도보다 어둡게 보입니다.
둘 다 셰이더 코드가 아니라 임포트 설정에서 생기는 문제이므로, 텍스처를 가져온 뒤 색감이나 조명이 이상하면 셰이더를 고치기 전에 sRGB 설정부터 확인해야 합니다.

---

## HDR

지금까지 다룬 색상 값은 0에서 1 사이에 놓이고, 1.0이 표현할 수 있는 가장 밝은 값입니다. 하지만 직사광선을 받는 면은 그늘진 곳보다 수백 배 넘게 밝아, 그 밝기는 1.0이라는 천장을 한참 넘어섭니다. 이렇게 밝은 곳과 어두운 곳이 한 장면에 함께 있으면, 0에서 1이라는 좁은 폭으로는 둘의 차이를 다 담지 못합니다.

### LDR의 한계

한 장면이 동시에 표현할 수 있는 가장 어두운 값과 가장 밝은 값의 비율을 **동적 범위(Dynamic Range)**라고 합니다. 최종 색상 값을 0에서 1 사이, 8비트 저장 기준으로는 0에서 255 사이로 제한해 이 동적 범위를 좁힌 방식이 **LDR(Low Dynamic Range)**입니다.

LDR의 문제는 밝은 영역에서 쉽게 클리핑이 생긴다는 점입니다. 서로 다른 강도의 빛이라도 최종 값이 1.0을 넘으면 모두 1.0에서 멈춰, 똑같은 흰색이 됩니다. 그 결과 밝은 구름, 금속 반사, 발광체 주변처럼 실제로는 밝기 차이가 남아 있어야 하는 영역의 디테일이 사라질 수 있습니다.

이 한계를 줄이는 방법이 **HDR(High Dynamic Range)** 렌더링입니다. HDR은 조명을 계산하는 동안 1.0을 넘는 밝기를 잘라 내지 않고 그대로 유지하다가, 화면에 내보내기 직전에 이 넓은 범위를 0에서 1 사이로 압축합니다. 1.0에서 잘라 버리는 LDR과 달리 범위 전체를 함께 줄여 밝은 값들의 차이를 살리는데, 이 압축 단계를 **톤 매핑(Tone Mapping)**이라고 합니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 310" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="현실 세계의 밝기 범위 대수 척도 시각화">
  <rect width="620" height="310" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">현실 세계의 밝기 범위</text>
  <!-- Scale bar (어두움→밝음을 fill-opacity 증가로 표현) -->
  <rect x="50" y="66" width="520" height="20" fill="currentColor" fill-opacity="0.04" rx="3"/>
  <rect x="50"  y="66" width="104" height="20" fill="currentColor" fill-opacity="0.1"/>
  <rect x="154" y="66" width="104" height="20" fill="currentColor" fill-opacity="0.22"/>
  <rect x="258" y="66" width="104" height="20" fill="currentColor" fill-opacity="0.34"/>
  <rect x="362" y="66" width="104" height="20" fill="currentColor" fill-opacity="0.46"/>
  <rect x="466" y="66" width="52"  height="20" fill="currentColor" fill-opacity="0.58"/>
  <rect x="518" y="66" width="52"  height="20" fill="currentColor" fill-opacity="0.72"/>
  <rect x="50"  y="66" width="520" height="20" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4" rx="3"/>
  <!-- Tick marks and labels -->
  <line x1="50"  y1="86" x2="50"  y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="50"  y="109" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">별빛</text>
  <text x="50"  y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">0.0001</text>
  <line x1="154" y1="86" x2="154" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="154" y="109" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">달빛</text>
  <text x="154" y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">0.01</text>
  <line x1="258" y1="86" x2="258" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="258" y="109" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">실내 조명</text>
  <text x="258" y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">1.0</text>
  <line x1="362" y1="86" x2="362" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="362" y="109" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">흐린 날 야외</text>
  <text x="362" y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">10</text>
  <line x1="466" y1="86" x2="466" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="466" y="109" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">맑은 날 야외</text>
  <text x="466" y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">100</text>
  <line x1="570" y1="86" x2="570" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="570" y="109" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">직사광선</text>
  <text x="570" y="122" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">10,000</text>
  <!-- LDR bracket (좁은 범위 · 점선으로 한정 강조) -->
  <line x1="50"  y1="148" x2="258" y2="148" stroke="currentColor" stroke-width="2" stroke-dasharray="5,3"/>
  <line x1="50"  y1="143" x2="50"  y2="153" stroke="currentColor" stroke-width="2"/>
  <line x1="258" y1="143" x2="258" y2="153" stroke="currentColor" stroke-width="2"/>
  <text x="154" y="168" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">LDR이 한 번에 담는 범위</text>
  <text x="154" y="183" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(노출에 따라 이동)</text>
  <!-- HDR bracket (전체 범위 · 실선) -->
  <line x1="50"  y1="208" x2="570" y2="208" stroke="currentColor" stroke-width="2"/>
  <line x1="50"  y1="203" x2="50"  y2="213" stroke="currentColor" stroke-width="2"/>
  <line x1="570" y1="203" x2="570" y2="213" stroke="currentColor" stroke-width="2"/>
  <text x="310" y="228" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">HDR</text>
  <text x="310" y="264" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">LDR은 현실 밝기의 극히 일부만 표현 가능</text>
  <text x="310" y="284" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">(상대 밝기 예시 · 로그 척도로 간소화)</text>
</svg>

### HDR 렌더링

HDR 렌더링을 하려면 렌더링 결과를 저장하는 프레임 버퍼가 1.0을 넘는 값을 담을 수 있어야 합니다. 예를 들어 일반 표면의 밝기가 0.8이라면, 태양이나 강한 반사광은 5.0, 10.0처럼 더 큰 값으로 남겨 둘 수 있어야 합니다.

이를 위해 HDR에서는 보통 **16비트 부동소수점(half-float)** 또는 **32비트 부동소수점** 렌더 타깃을 사용합니다. 8비트 정수 포맷은 0에서 1 사이의 정규화된 값만 표현하는 반면, 부동소수점 포맷은 조명 누적 중 생기는 1.0 초과 값을 잘라내지 않고 보존할 수 있습니다.

<br>

| 항목 | LDR (R8G8B8A8) | HDR (R16G16B16A16F) |
|---|---|---|
| 채널당 | 8비트 정수 | 16비트 부동소수점 |
| 범위 | 0 ~ 1 (0 ~ 255) | 0 이상 (half-float 최대 65504) |
| 크기 | 4바이트/픽셀 | 8바이트/픽셀 |
| 1080p | 약 8MB | 약 16MB (LDR의 2배) |

<br>

대신 부동소수점 렌더 타깃은 픽셀당 데이터가 두 배여서, 메모리와 대역폭 부담이 LDR의 약 두 배에 이릅니다. 특히 모바일에서는 이 대역폭이 성능에 곧장 영향을 줍니다.

그래서 Bloom이나 강한 Emission처럼 1.0을 넘는 밝기에 의존하는 효과를 쓰지 않는다면, LDR 렌더링만으로도 충분합니다.

### 톤 매핑 (Tone Mapping)

HDR 렌더 타깃에 남은 1.0 초과 값은 화면에 나갈 때 결국 0에서 1 사이로 내려와야 합니다. 1.0을 넘는 값을 모두 1.0으로 자르는 클리핑에서는 2.0이든 10.0이든 같은 흰색이 되어, 하이라이트 안의 밝기 차이가 사라집니다. 톤 매핑은 입력이 커질수록 출력 증가폭을 줄이는 비선형 곡선으로 압축해, 하이라이트를 1.0 근처로 모으면서도 그 차이를 남깁니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 320" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="톤 매핑의 역할 — 클리핑 vs 톤 매핑 비교">
  <rect width="620" height="320" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">톤 매핑의 역할</text>
  <!-- HDR values row -->
  <text x="70"  y="72" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">0</text>
  <text x="168" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">0.5</text>
  <text x="266" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">1.0</text>
  <text x="364" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">2.0</text>
  <text x="462" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">5.0</text>
  <text x="560" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">10.0</text>
  <text x="310" y="56" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">HDR 입력</text>
  <line x1="40" y1="84" x2="590" y2="84" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <!-- Clamping section (손실 · 점선 테두리 + 낮은 opacity) -->
  <rect x="40" y="94" width="540" height="80" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3" opacity="0.6" rx="4"/>
  <text x="310" y="112" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold" opacity="0.55">클리핑 (단순 자르기) — 출력</text>
  <text x="70"  y="136" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">0</text>
  <text x="168" y="136" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">0.5</text>
  <text x="266" y="136" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.7">1.0</text>
  <text x="364" y="136" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.45">1.0</text>
  <text x="462" y="136" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.45">1.0</text>
  <text x="560" y="136" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.45">1.0</text>
  <text x="430" y="158" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">차이가 모두 사라짐</text>
  <!-- Tone mapping section (보존 · 실선 + full opacity) -->
  <rect x="40" y="188" width="540" height="80" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5" rx="4"/>
  <text x="310" y="206" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">톤 매핑 (비선형 압축) — 출력</text>
  <text x="70"  y="230" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">0</text>
  <text x="168" y="230" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">0.4</text>
  <text x="266" y="230" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">0.7</text>
  <text x="364" y="230" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">0.85</text>
  <text x="462" y="230" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">0.95</text>
  <text x="560" y="230" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" font-weight="bold">0.98</text>
  <text x="430" y="252" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">밝은 영역도 차이가 보존됨</text>
  <text x="310" y="292" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">값이 커질수록 출력 증가폭이 줄어듦 — 하이라이트 디테일 보존 (예시 값)</text>
</svg>

<br>

HDR 값을 어떤 곡선으로 압축하는지는 알고리즘마다 다르고, 같은 입력이라도 곡선에 따라 최종 색감과 대비가 달라집니다. 대표적인 방식으로는 Reinhard, ACES(Academy Color Encoding System), Neutral이 있습니다.

<br>

| 알고리즘 | 특징 |
|---|---|
| Reinhard | 밝은 영역을 부드럽게 압축하는 단순한 곡선 |
| ACES (Filmic) | 영화 필름의 톤 곡선을 모방하여 대비가 강하고 채도가 풍부함 |
| Neutral | 색상(Hue)과 채도(Saturation) 변화를 최소화하고 밝기만 압축 |

<br>

Unity URP(Universal Render Pipeline)에서는 Volume 시스템의 Tonemapping 항목에서 톤 매핑 방식을 선택할 수 있습니다.

### Bloom과 HDR

**Bloom**은 강하게 빛나는 영역의 둘레로 빛이 번지는 효과입니다. 번짐을 어디에 입힐지 고르려면 어떤 픽셀을 "충분히 밝다"고 볼지 정하는 임계값이 필요합니다. 그런데 이 임계값을 어디에 둘 수 있느냐가 LDR과 HDR에서 달라집니다.

LDR에서는 모든 값이 0에서 1 사이에 머무르기 때문에 이 임계값을 잡기가 어렵습니다. 임계값을 0.8로 두면 0.8과 1.0 사이의 값이 전부 번짐 대상이 되어, 강한 광원뿐 아니라 적당히 밝은 표면까지 함께 번집니다.

HDR에서는 1.0을 넘는 값이 그대로 남아 있어, 임계값을 1.0 위로 올릴 수 있습니다. 그러면 태양이나 발광체, 폭발처럼 일반 표면보다 확연히 밝은 픽셀만 번짐 대상으로 선별되어, Bloom이 더 자연스러워집니다.

---

## Unity의 Color Space 설정

조명 계산을 선형 공간에서 하고, sRGB 텍스처를 선형으로 디코딩하고, HDR 값을 톤 매핑으로 압축하는 과정은 모두 프로젝트가 선형 워크플로우를 따를 때 성립합니다. Unity에서는 프로젝트가 이 선형 워크플로우를 따를지, 아니면 변환을 생략한 감마 워크플로우를 따를지를 색공간 설정 하나로 정합니다.

설정은 **Project Settings > Player > Other Settings > Color Space**에 있습니다. Linear를 선택하면 앞서 설명한 선형 워크플로우가 적용됩니다. 입력 단계에서 sRGB 텍스처를 선형 값으로 디코딩해 조명을 선형 공간에서 계산하고, 출력 단계에서 다시 sRGB로 인코딩해 화면으로 내보냅니다. Gamma를 선택하면 이 디코딩과 인코딩을 건너뛴 채, 셰이더가 감마 값을 그대로 조명 계산에 사용합니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 416" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="Unity Color Space 설정 UI 및 Gamma vs Linear 비교">
  <rect width="620" height="416" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="bold" fill="currentColor">Unity Color Space 설정</text>
  <!-- Settings panel mockup -->
  <rect x="160" y="52" width="300" height="90" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" opacity="0.5" rx="5"/>
  <rect x="160" y="52" width="300" height="22" fill="currentColor" fill-opacity="0.1" stroke="none" rx="5"/>
  <rect x="160" y="63" width="300" height="11" fill="currentColor" fill-opacity="0.1" stroke="none"/>
  <text x="310" y="67" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Project Settings  ▷  Player  ▷  Other Settings</text>
  <text x="180" y="94" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">Color Space</text>
  <circle cx="264" cy="90" r="5" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <text x="274" y="94" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">Gamma</text>
  <circle cx="340" cy="90" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="340" cy="90" r="2.5" fill="currentColor"/>
  <text x="350" y="94" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">Linear</text>
  <text x="310" y="128" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">렌더 파이프라인과 대상 플랫폼별 지원 확인 필요</text>
  <line x1="40" y1="158" x2="580" y2="158" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <!-- Gamma column (주의 · 점선 테두리 + 낮은 강조) -->
  <rect x="40" y="164" width="258" height="196" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.6" rx="5"/>
  <rect x="40" y="164" width="258" height="28" fill="currentColor" fill-opacity="0.08" stroke="none" rx="5"/>
  <rect x="40" y="183" width="258" height="9" fill="currentColor" fill-opacity="0.08" stroke="none"/>
  <text x="169" y="183" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor" opacity="0.6">Gamma</text>
  <text x="58" y="212" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">•  텍스처를 선형화하지 않고 조명 계산</text>
  <text x="58" y="232" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">•  감마 공간 조명 계산</text>
  <text x="58" y="252" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">•  구형/저사양 호환에 유리</text>
  <text x="58" y="272" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">•  PBR/블렌딩 결과 왜곡 가능</text>
  <text x="58" y="292" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">•  중간 톤이 과도하게 밝아질 수 있음</text>
  <text x="58" y="312" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">•  에너지 보존 가정이 깨질 수 있음</text>
  <!-- Linear column (권장 · 실선 테두리 + 강조) -->
  <rect x="322" y="164" width="258" height="196" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5" rx="5"/>
  <rect x="322" y="164" width="258" height="28" fill="currentColor" fill-opacity="0.12" stroke="none" rx="5"/>
  <rect x="322" y="183" width="258" height="9" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <text x="451" y="183" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Linear</text>
  <text x="340" y="212" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">•  GPU가 sRGB 텍스처를 자동 선형화</text>
  <text x="340" y="232" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">•  선형 공간 조명 계산</text>
  <text x="340" y="252" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.7">•  sRGB 샘플링/출력 지원 필요</text>
  <text x="340" y="272" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">•  물리적으로 정확</text>
  <text x="340" y="292" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">•  PBR 전제 조건</text>
  <text x="340" y="312" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">•  에너지 보존 유지</text>
  <text x="340" y="332" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">•  HDR/톤 매핑 워크플로우에 유리</text>
  <text x="310" y="380" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.55">프로젝트 시작 시 결정 — 개발 중 변경 시 머티리얼·라이팅 전체 재작업 필요</text>
  <text x="310" y="396" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">PBR 기반 렌더링에서는 Linear 설정이 기준이 됨</text>
</svg>

### 모바일에서 Linear Color Space의 지원

Linear Color Space를 사용하려면 대상 플랫폼이 두 가지 변환을 하드웨어로 지원해야 합니다. 
하나는 색상 텍스처를 샘플링할 때 sRGB 값을 선형으로 디코딩하는 변환이고, 다른 하나는 최종 출력을 렌더 타깃에 기록할 때 다시 sRGB로 인코딩하는 변환입니다.

현대 PC와 콘솔, Metal이나 Vulkan을 사용하는 모바일 환경에서는 대체로 Linear 워크플로우를 사용할 수 있습니다. 다만 오래된 모바일 기기, 구형 그래픽 API, 일부 WebGL 환경에서는 지원 범위가 제한될 수 있습니다.

프로젝트에서 Color Space를 Linear로 지정해도, 대상 기기가 앞의 두 변환을 지원하지 못하면 의도대로 동작하지 않습니다. 따라서 모바일을 대상으로 한다면 실제 빌드 타깃의 그래픽 API, 최소 지원 기기, 렌더 파이프라인 설정에서 Linear Color Space와 HDR 렌더 타깃이 지원되는지 함께 확인해야 합니다.

### 프로젝트 시작 시 설정

색공간은 같은 텍스처와 조명 값을 어떻게 해석할지 정하기 때문에, 프로젝트의 전체 룩에 직접 영향을 줍니다. 따라서 색공간은 가능하면 프로젝트 시작 단계에서 정해 두는 것이 좋습니다.

만약, 개발 중간에 Gamma와 Linear를 바꾸면 그동안 맞춰 둔 머티리얼, 라이트 강도, 후처리 값이 한꺼번에 다르게 보이고, 이를 새 색공간에 맞게 재설정해야 하는 일이 발생합니다. 이런 항목은 프로젝트가 진행될수록 쌓이므로, 색공간을 늦게 바꿀수록 비용이 더 커집니다.

시작 단계에서 어떤 색공간을 기본으로 둘지는 프로젝트의 렌더링 방식에 따라 달라집니다. 조명을 물리적으로 다루는 PBR 머티리얼과 HDR 후처리는 모두 선형 공간 계산을 전제하므로, 이런 기능에 의존하는 프로젝트라면 보통 Linear Color Space를 기준으로 잡습니다. 다만 모바일이나 WebGL에서는 앞서 살펴본 플랫폼 제약이 따르므로, Linear가 지원되는지와 성능 비용을 확인한 뒤 색공간을 확정해야 합니다.

---

## 마무리

이번 글에서는 색을 숫자로 저장하는 방식과, 그 숫자를 조명 계산과 화면 출력에서 어떻게 해석해야 하는지 정리했습니다. 핵심은 다음과 같습니다.

- **RGB 색 모델**은 빨강, 초록, 파랑 채널을 더해 색을 표현합니다. 채널당 8비트를 사용하면 각 채널은 0부터 255까지 256단계로 표현되고, 셰이더 내부에서는 보통 이 값을 0.0에서 1.0 사이의 부동소수점으로 다룹니다.
- **감마 보정**은 디스플레이의 비선형 응답과 인간의 밝기 지각을 고려한 인코딩입니다. 이미지를 감마 1/2.2에 가깝게 저장하면 제한된 비트 깊이를 어두운 영역에 더 효율적으로 배분할 수 있습니다.
- **조명 계산**은 선형 공간에서 이루어져야 합니다. 밝기 값이 실제 빛의 에너지에 비례해야 덧셈, 곱셈, 보간, 감쇠 계산이 물리적 의미를 유지합니다.
- **선형 워크플로우**는 입력 단계에서 sRGB 텍스처를 선형 값으로 디코딩하고, 조명을 선형 공간에서 계산한 뒤, 출력 단계에서 다시 sRGB로 인코딩합니다.
- **sRGB**는 원색, 백색점, 전달 함수를 함께 정의한 표준 색공간입니다. Albedo처럼 눈에 보이는 색상 텍스처는 sRGB로 읽고, 노멀맵이나 메탈릭맵처럼 수치를 담은 데이터 텍스처는 선형 값 그대로 읽어야 합니다.
- **HDR 렌더링**은 1.0을 넘는 밝기 값을 중간 렌더링 단계에서 보존합니다. 이후 노출 조정과 톤 매핑을 통해 화면이 표현할 수 있는 LDR 범위로 압축하며, Bloom 같은 후처리는 이 1.0 초과 값을 기준으로 더 자연스럽게 동작합니다.
- Unity에서는 **Color Space** 설정으로 Gamma와 Linear 워크플로우를 선택합니다. PBR 기반 렌더링과 HDR 후처리를 사용하는 프로젝트라면 Linear를 기준으로 검토하되, 대상 플랫폼의 지원 범위와 성능 비용도 함께 확인해야 합니다.

정리하면 디지털 색 표현은 두 요구를 동시에 만족해야 합니다. 저장과 출력 단계에서는 디스플레이와 인간의 밝기 지각을 고려해야 하고, 조명 계산 단계에서는 빛의 물리적 덧셈이 성립하도록 선형 값을 사용해야 합니다.

이 글에서 다룬 색공간과 [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)를 바탕으로, 다음 글에서는 표면이 입사광을 어떻게 반사해 최종 밝기를 만드는지 살펴봅니다. Lambert, Phong, Blinn-Phong에서 출발해 PBR의 Cook-Torrance 모델이 에너지 보존과 프레넬 효과를 어떻게 반영하는지 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 이어 다룹니다.

<br>

---

**관련 글**
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- **색과 빛 (2) - 색 표현과 색공간** (현재 글)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)
- [Unity 엔진 핵심 (1) - GameObject와 Component](/dev/unity/UnityCore-1/)
- [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)
- [Unity 엔진 핵심 (3) - Unity 실행 순서](/dev/unity/UnityCore-3/)
- [Unity 엔진 핵심 (4) - Unity의 스레딩 모델](/dev/unity/UnityCore-4/)
- [Unity 에셋 시스템 (1) - Asset Import Pipeline](/dev/unity/UnityAsset-1/)
- [Unity 에셋 시스템 (2) - Serialization과 Instantiation](/dev/unity/UnityAsset-2/)
- [Unity 에셋 시스템 (3) - Scene Management](/dev/unity/UnityAsset-3/)
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
