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

[색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)에서는 빛이 전자기파의 일종이며, 표면과 만났을 때 반사, 굴절, 흡수가 일어나고, 이 현상들을 BRDF라는 수학적 함수로 통합한다는 내용을 다루었습니다.

<br>

물리적 세계에서 빛의 밝기는 연속적인 값입니다. 햇빛은 흐려졌다가 밝아지는 사이에 무한히 많은 중간 단계를 거치며, 색 역시 무지개처럼 파장이 끊김 없이 이어집니다. 컴퓨터가 이를 다루려면 연속적인 물리량을 유한한 개수의 숫자로 변환해야 하는데, 밝기를 어떤 간격으로 나누느냐에 따라 결과가 크게 달라집니다.

사람의 눈은 어두운 영역의 밝기 차이에는 민감하지만 밝은 영역에서는 둔감하고, 디스플레이의 출력 밝기도 입력 신호에 비례하지 않습니다. 이 비선형 특성을 무시하고 밝기를 균등하게 나누면, 어두운 영역에서 색이 부드럽게 이어지지 않고 띠처럼 끊기는 **밴딩(banding)**이 나타납니다.

<br>

밴딩을 피하려면 비선형 특성에 맞는 색 표현 체계가 필요합니다. 이 체계는 **색 모델**과 **색공간**, 두 단계로 나뉩니다.

**색 모델(Color Model)**은 색을 숫자로 표현하기 위한 틀로, 축의 종류와 개수를 정의합니다. RGB는 빨강·초록·파랑 세 축, CMYK는 시안·마젠타·노랑·검정 네 축, HSL은 색상·채도·명도 세 축을 사용합니다. 디스플레이와 게임 엔진에서는 주로 RGB 모델을 사용합니다.

**색공간(Color Space)**은 색 모델의 숫자가 현실의 어떤 색에 대응하는지를 확정하는 단계입니다. 같은 RGB 모델이라도 "빨강(1, 0, 0)"이 정확히 어떤 물리적 색인지는 색공간마다 다릅니다. 색공간은 각 원색의 색 좌표, 백색점(White Point), 값과 밝기 사이의 변환 곡선인 전달 함수(Transfer Function)를 규정하여, 같은 숫자가 어디서나 같은 색으로 재현되도록 합니다.

<br>

이 글에서는 RGB 색 모델의 구조, 감마 보정의 원리와 필요성, 선형 색공간과 감마 색공간의 차이, sRGB 표준, HDR과 톤 매핑, 그리고 Unity에서의 Color Space 설정을 다룹니다.

---

## RGB 색 모델

### 가산 혼합

[색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다루었듯이, 인간의 망막에는 빨강(R), 초록(G), 파랑(B) 파장대에 각각 반응하는 세 종류의 원추세포가 있고, 이 세 원색의 밝기 조합만으로 대부분의 색을 재현할 수 있습니다.

RGB 색 모델은 이 원리를 기반으로, 세 원색의 빛을 서로 다른 비율로 합산하여 색을 만듭니다.

빛은 에너지이므로, 서로 다른 색의 빛을 한 지점에 겹치면 에너지가 합산되어 결과가 더 밝아집니다. 이 방식이 **가산 혼합(Additive Mixing)**입니다. 빨강, 초록, 파랑을 모두 최대 밝기로 합치면 흰색이 됩니다.

반대로 물감이나 잉크는 특정 파장의 빛을 흡수하므로, 여러 색을 섞을수록 흡수되는 파장이 늘어나 반사되는 빛이 줄고 결과가 어두워집니다. 이 방식은 **감산 혼합(Subtractive Mixing)**입니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 380" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="가산 혼합 빛의 혼합 다이어그램: R+G=노랑, R+B=마젠타, G+B=시안, R+G+B=흰색">
  <rect width="620" height="380" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="32" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">가산 혼합 (빛의 혼합)</text>
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
  <text x="310" y="88" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#ff6b6b">빨강 (R)</text>
  <text x="175" y="272" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#73f38f">초록 (G)</text>
  <text x="445" y="272" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#00d4ff">파랑 (B)</text>
  <!-- Overlap labels (dark outline for readability on solid intersection fills) -->
  <text x="247" y="172" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ffd700" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">노랑</text>
  <text x="247" y="186" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#ccc" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">(R+G)</text>
  <text x="373" y="172" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff00ff" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">마젠타</text>
  <text x="373" y="186" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#ccc" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">(R+B)</text>
  <text x="310" y="248" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#00ffff" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">시안</text>
  <text x="310" y="262" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#ccc" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">(G+B)</text>
  <text x="310" y="208" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ffffff" stroke="#1a1f1e" stroke-width="3" paint-order="stroke">흰색</text>
  <!-- Combination list -->
  <line x1="40" y1="296" x2="580" y2="296" stroke="#333" stroke-width="1"/>
  <text x="60" y="318" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">R + G = <tspan fill="#ffd700">노랑 (Yellow)</tspan></text>
  <text x="330" y="318" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">R + B = <tspan fill="#ff00ff">마젠타 (Magenta)</tspan></text>
  <text x="60" y="340" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">G + B = <tspan fill="#00ffff">시안 (Cyan)</tspan></text>
  <text x="330" y="340" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">R + G + B = <tspan fill="#ffffff">흰색 (White)</tspan></text>
  <text x="60" y="362" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">없음 = <tspan fill="#888">검정 (Black)</tspan></text>
</svg>

<br>

모니터의 각 픽셀은 빨강, 초록, 파랑 세 개의 서브픽셀로 구성되어 있습니다.
각 서브픽셀의 밝기를 조절하여 다양한 색을 만듭니다. 빨강과 초록을 동시에 켜면 노란색이 되고, 세 서브픽셀을 모두 최대 밝기로 켜면 흰색이 됩니다.

### 채널과 비트 깊이

RGB 색 모델에서 각 채널(R, G, B)의 값은 정수 형식과 부동소수점 형식, 두 가지로 표현됩니다.

<br>

**RGB 값의 표현 형식**

| 형식 | 범위 | 빨강 | 흰색 | 검정 |
|------|------|------|------|------|
| 정수 (8비트) | 0 ~ 255 (256단계) | (255, 0, 0) | (255, 255, 255) | (0, 0, 0) |
| 부동소수점 | 0.0 ~ 1.0 | (1.0, 0.0, 0.0) | (1.0, 1.0, 1.0) | (0.0, 0.0, 0.0) |

$$
\text{float} = \frac{\text{정수}}{255}, \quad \text{정수} = \text{float} \times 255
$$

위 표의 부동소수점 범위 0.0~1.0은 표준 동적 범위(SDR) 기준입니다. HDR 렌더링에서는 1.0을 초과하는 값도 사용하며, 이에 대해서는 뒤에서 다룹니다.

<br>

채널당 8비트($2^8$)는 256단계를 의미합니다. R, G, B 세 채널을 합하면 24비트이며, 표현 가능한 색의 총 수는 $256^3 =$ 약 1,677만 색입니다.

<br>

여기에 투명도를 나타내는 알파(Alpha) 채널을 추가하면 R8G8B8A8(32비트) 포맷이 됩니다.

알파 채널은 픽셀의 불투명도를 0(완전 투명)에서 255(완전 불투명)로 나타냅니다. 반투명 UI나 파티클 이펙트에 필수적이며, R8G8B8A8은 가장 기본적인 비압축 텍스처 포맷입니다. 실제 게임에서는 메모리 절약을 위해 ASTC나 ETC2 같은 압축 포맷으로 변환하여 GPU에 로드하는 경우가 많습니다.

<br>

셰이더 내부에서는 부동소수점 형식을 사용합니다. 예를 들어 빨간 표면 (1.0, 0.0, 0.0)에 조명 강도 0.5를 곱하면 결과가 (0.5, 0.0, 0.0)이 되어, 밝기가 절반으로 줄었음을 값에서 바로 읽을 수 있습니다.

정수(0~255)로 같은 계산을 하려면 곱셈 결과를 다시 255로 나누어 원래 범위로 되돌려야 하고, 이 과정에서 소수점 이하가 잘려 정밀도가 떨어집니다.

<br>

인간의 눈이 구분할 수 있는 색은 약 1,000만 가지로 추정됩니다. 24비트(약 1,677만 색)는 이 수를 넘어서므로 총 색 수 자체는 부족하지 않습니다.
그러나 채널 값 0~255가 물리적 밝기에 어떻게 대응하느냐에 따라 표현 품질이 달라집니다.
이 대응을 선형(비례)으로 설정하면, 어두운 영역과 밝은 영역에 같은 수의 단계가 배정됩니다. 사람의 눈은 어두운 영역의 밝기 차이에 민감하므로, 이 영역에 배정된 단계 수가 부족하면 도입부에서 언급한 밴딩이 나타납니다.
감마 보정은 채널 값과 밝기 사이에 비선형 대응을 적용하여, 어두운 영역에 더 많은 단계를 배정함으로써 이 문제를 해결합니다.

---

## 감마 보정

### CRT 모니터의 비선형 응답

CRT(Cathode Ray Tube) 모니터는 입력 전압과 화면 밝기가 비선형 관계였습니다. CRT는 전자총이 형광체에 전자를 쏘아 발광시키는 구조인데, 그리드 전압에 따라 전자빔의 전류가 비선형적으로 변하고, 형광체의 발광 특성까지 겹쳐 전압을 두 배로 올려도 밝기가 두 배가 되지 않습니다. 이 비선형 관계는 거듭제곱 함수로 표현됩니다.

<br>

$$
\text{출력 밝기} = \text{입력값}^{\gamma} \quad (\gamma \approx 2.2)
$$

예를 들어, 입력 0.0일 때 $0.0^{2.2} = 0.0$(검정), 입력 0.5일 때 $0.5^{2.2} \approx 0.218$(물리적 밝기의 약 22%), 입력 1.0일 때 $1.0^{2.2} = 1.0$(최대 밝기)입니다.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 340" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="CRT의 비선형 응답 그래프: 감마 2.2 곡선과 선형 기준선 비교, 입력 0.5에서 출력 약 0.218">
  <rect width="620" height="340" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">CRT의 비선형 응답</text>
  <!-- Axes -->
  <line x1="90" y1="60" x2="90" y2="292" stroke="#666" stroke-width="1.5"/>
  <line x1="88" y1="290" x2="552" y2="290" stroke="#666" stroke-width="1.5"/>
  <!-- Y-axis labels -->
  <text x="78" y="294" text-anchor="end" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">0.0</text>
  <line x1="85" y1="175" x2="90" y2="175" stroke="#666" stroke-width="1"/>
  <text x="78" y="179" text-anchor="end" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">0.5</text>
  <text x="78" y="64" text-anchor="end" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">1.0</text>
  <!-- X-axis labels -->
  <text x="90" y="307" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">0.0</text>
  <line x1="320" y1="290" x2="320" y2="295" stroke="#666" stroke-width="1"/>
  <text x="320" y="307" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">0.5</text>
  <text x="550" y="307" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">1.0</text>
  <text x="320" y="325" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">입력값</text>
  <text x="18" y="175" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888" transform="rotate(-90, 18, 175)">출력 밝기</text>
  <!-- Linear reference (dashed) -->
  <line x1="90" y1="290" x2="550" y2="60" stroke="#888" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="430" y="125" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">선형 (y=x)</text>
  <!-- Gamma curve y=x^2.2 -->
  <path d="M 90,290 C 150,288 230,275 320,240 S 460,120 550,60" fill="none" stroke="#00d4ff" stroke-width="2.5"/>
  <text x="210" y="232" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#00d4ff">감마 2.2</text>
  <!-- Annotation: x=0.5 → y≈0.218 -->
  <line x1="320" y1="290" x2="320" y2="240" stroke="#ED7D31" stroke-width="1.2" stroke-dasharray="4,3"/>
  <line x1="90" y1="240" x2="320" y2="240" stroke="#ED7D31" stroke-width="1.2" stroke-dasharray="4,3"/>
  <circle cx="320" cy="240" r="4" fill="#ED7D31"/>
  <text x="326" y="237" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#ED7D31">입력 0.5 → 출력 ≈ 0.218</text>
  <text x="78" y="244" text-anchor="end" font-family="'Noto Sans KR',sans-serif" font-size="10" fill="#ED7D31">0.218</text>
</svg>

<br>

이 비선형 응답은 CRT의 물리적 구조에서 비롯된 것이지만, 현대의 LCD나 OLED 모니터도 내부 펌웨어에서 동일한 감마 곡선을 적용합니다.
수십 년간 제작된 사진, 영상, 텍스처가 모두 감마 2.2 디스플레이를 전제로 인코딩되어 있어, 모니터가 선형 응답을 사용하면 기존 콘텐츠가 전체적으로 밝고 바래 보이기 때문입니다.
따라서 사실상 모든 디스플레이가 감마 2.2의 비선형 응답을 따릅니다.

### 감마 보정이 필요한 이유

CRT의 감마 곡선은 어두운 쪽 밝기를 촘촘하게, 밝은 쪽은 성기게 구분합니다. 인간의 눈도 어두운 영역의 밝기 변화에 민감하고 밝은 영역에서는 둔감하기 때문에, CRT의 비선형 응답은 제한된 비트를 인간이 민감하게 느끼는 어두운 영역에 집중시키는 결과를 냅니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 280" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="인간의 밝기 인지: 동일한 25% 물리적 간격이 어두운 쪽에서는 크게, 밝은 쪽에서는 작게 느껴진다">
  <rect width="620" height="280" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">인간의 밝기 인지</text>
  <!-- Gradient bar -->
  <defs>
    <linearGradient id="bwGrad5" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#000000"/>
      <stop offset="100%" stop-color="#ffffff"/>
    </linearGradient>
  </defs>
  <rect x="50" y="55" width="520" height="44" fill="url(#bwGrad5)" rx="4"/>
  <rect x="50" y="55" width="520" height="44" fill="none" stroke="#555" stroke-width="1" rx="4"/>
  <!-- Tick marks -->
  <line x1="50"  y1="99" x2="50"  y2="108" stroke="#888" stroke-width="1.5"/>
  <line x1="180" y1="99" x2="180" y2="108" stroke="#888" stroke-width="1.5"/>
  <line x1="310" y1="99" x2="310" y2="108" stroke="#888" stroke-width="1.5"/>
  <line x1="440" y1="99" x2="440" y2="108" stroke="#888" stroke-width="1.5"/>
  <line x1="570" y1="99" x2="570" y2="108" stroke="#888" stroke-width="1.5"/>
  <text x="50"  y="120" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">0%</text>
  <text x="180" y="120" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">25%</text>
  <text x="310" y="120" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">50%</text>
  <text x="440" y="120" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">75%</text>
  <text x="570" y="120" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">100%</text>
  <!-- Bracket annotations above bar -->
  <path d="M 50,50 L 50,44 L 180,44 L 180,50" fill="none" stroke="#73f38f" stroke-width="2"/>
  <text x="115" y="40" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">크게 느낌</text>
  <path d="M 440,50 L 440,44 L 570,44 L 570,50" fill="none" stroke="#888" stroke-width="2"/>
  <text x="505" y="40" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">작게 느낌</text>
  <!-- Arrow thickness visual -->
  <line x1="50" y1="145" x2="175" y2="145" stroke="#73f38f" stroke-width="7" stroke-linecap="round"/>
  <polygon points="175,138 190,145 175,152" fill="#73f38f"/>
  <text x="118" y="166" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#73f38f">인지 차이 큼</text>
  <line x1="180" y1="145" x2="305" y2="145" stroke="#ccc" stroke-width="4" stroke-linecap="round"/>
  <polygon points="305,140 318,145 305,150" fill="#ccc"/>
  <line x1="315" y1="145" x2="435" y2="145" stroke="#ccc" stroke-width="3" stroke-linecap="round"/>
  <polygon points="435,141 448,145 435,149" fill="#ccc"/>
  <line x1="445" y1="145" x2="565" y2="145" stroke="#888" stroke-width="2" stroke-linecap="round"/>
  <polygon points="565,141 578,145 565,149" fill="#888"/>
  <text x="512" y="166" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">인지 차이 작음</text>
  <!-- Separator and explanation -->
  <line x1="40" y1="185" x2="580" y2="185" stroke="#333" stroke-width="1"/>
  <text x="310" y="210" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">물리적으로 동일한 25% 간격이지만,</text>
  <text x="310" y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">어두운 쪽에서는 차이를 <tspan fill="#73f38f">크게 느끼고</tspan></text>
  <text x="310" y="250" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">밝은 쪽에서는 차이를 <tspan fill="#888">작게 느낀다</tspan></text>
</svg>

<br>

이 비선형 인지 특성 아래에서 256단계를 물리적 밝기에 균일하게 배분하면, 어두운 영역에서는 앞서 본 밴딩이 발생하고, 밝은 영역에서는 인간이 구분하지 못하는 밝기 차이에 단계를 낭비합니다. 같은 256단계라도 인간의 인지 곡선에 맞춰 재분배하면 두 문제를 동시에 해결할 수 있습니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 320" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="선형 배분 대 감마 보정 배분 비교: 선형 배분은 어두운 영역 단계 부족으로 밴딩 발생, 감마 보정은 어두운 영역에 단계를 집중하여 부드러운 그라데이션">
  <rect width="620" height="320" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">선형 배분 vs 감마 보정 배분</text>
  <!-- Linear bar -->
  <text x="50" y="58" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#ccc">선형 배분</text>
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
  <rect x="50" y="65" width="520" height="42" fill="none" stroke="#555" stroke-width="1" rx="3"/>
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
  <text x="52" y="125" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff6b6b">어두운 영역: 단계 적음 → 밴딩 발생</text>
  <text x="390" y="125" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">밝은 영역: 단계 많음 → 비트 낭비</text>
  <line x1="40" y1="148" x2="580" y2="148" stroke="#333" stroke-width="1"/>
  <!-- Gamma bar -->
  <text x="50" y="172" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#ccc">감마 보정 배분</text>
  <rect x="50" y="178" width="520" height="42" fill="url(#bwGrad6b)" rx="3"/>
  <rect x="50" y="178" width="520" height="42" fill="none" stroke="#555" stroke-width="1" rx="3"/>
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
  <text x="52" y="238" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">어두운 영역: 단계 많음 → 부드러운 그라데이션</text>
  <text x="390" y="238" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">밝은 영역: 단계 적음</text>
  <text x="390" y="253" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">→ 인간은 차이 못 느낌</text>
  <line x1="40" y1="272" x2="580" y2="272" stroke="#333" stroke-width="1"/>
  <text x="310" y="294" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">감마 보정은 인간의 비선형 밝기 인지에 맞게 256단계를 재분배한다</text>
</svg>

<br>

**감마 보정(Gamma Correction)**은 이미지를 저장할 때 물리적 밝기 값에 감마의 역수(1/2.2 = 약 0.4545)를 지수로 적용하여 비선형으로 인코딩하는 과정입니다.
이렇게 인코딩된 값은 저장을 거쳐 모니터에서 다시 디코딩되는데, 전체 과정은 다음과 같습니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 420" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="감마 인코딩 디코딩 과정: 물리적 밝기 값에서 감마 인코딩, 저장, 모니터 감마 응답을 거쳐 원래 밝기로 복원되는 파이프라인">
  <rect width="620" height="420" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="30" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">감마 인코딩/디코딩 과정</text>
  <!-- Box 1 -->
  <rect x="165" y="50" width="290" height="46" fill="#1a1f1e" stroke="#5B9BD5" stroke-width="2" rx="6"/>
  <text x="310" y="78" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#f9fffb">물리적 밝기 값 (선형)</text>
  <!-- Arrow 1 -->
  <line x1="310" y1="96" x2="310" y2="150" stroke="#73f38f" stroke-width="2"/>
  <polygon points="303,148 310,164 317,148" fill="#73f38f"/>
  <text x="310" y="128" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">감마 인코딩: 값^(1/2.2)</text>
  <!-- Box 2 -->
  <rect x="165" y="165" width="290" height="46" fill="#1a1f1e" stroke="#5B9BD5" stroke-width="2" rx="6"/>
  <text x="310" y="193" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#f9fffb">저장된 값 (감마 공간)</text>
  <!-- Arrow 2 -->
  <line x1="310" y1="211" x2="310" y2="265" stroke="#73f38f" stroke-width="2"/>
  <polygon points="303,263 310,279 317,263" fill="#73f38f"/>
  <text x="310" y="243" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">모니터 감마 응답: 값^2.2</text>
  <!-- Box 3 -->
  <rect x="165" y="280" width="290" height="46" fill="#1a1f1e" stroke="#5B9BD5" stroke-width="2" rx="6"/>
  <text x="310" y="308" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#f9fffb">화면 출력 밝기 (선형)</text>
  <!-- Separator -->
  <line x1="40" y1="346" x2="580" y2="346" stroke="#333" stroke-width="1"/>
  <!-- Round-trip example -->
  <text x="50" y="368" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">순환 예시</text>
  <text x="50" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">물리적 밝기 <tspan fill="#00d4ff">0.5</tspan></text>
  <text x="155" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">→ 인코딩</text>
  <text x="232" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#00d4ff">0.729</text>
  <text x="277" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">→ 저장</text>
  <text x="320" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">(8비트 ≈ 186)</text>
  <text x="420" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">→ 디코딩</text>
  <text x="490" y="388" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#00d4ff">0.5 복원</text>
  <line x1="40" y1="398" x2="580" y2="398" stroke="#333" stroke-width="1"/>
  <text x="310" y="415" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">두 변환이 상쇄되어 원래의 물리적 밝기가 복원됨</text>
</svg>

<br>

값^(1/2.2)로 인코딩한 뒤 모니터가 값^2.2로 디코딩하면, 두 지수가 상쇄되어 의도한 밝기 분포가 재현됩니다.

---

## 선형 색공간

### 조명 계산에서의 문제

앞 절에서 감마 보정이 8비트의 제한된 단계를 인간의 인지에 맞게 재분배한다고 했습니다.
이 재분배는 이미지를 저장하고 표시하는 데에는 적합하지만, 셰이더에서 조명을 계산할 때에는 산술 결과가 물리적 현실과 어긋나는 원인이 됩니다.
물리적으로 정확한 조명 계산은 **선형 공간(Linear Space)**에서 수행해야 합니다.

<br>

"선형"이란 숫자 값과 물리적 에너지가 정비례 관계에 있다는 뜻입니다.
선형 공간에서 값 0.5는 물리적 최대 밝기의 정확히 50%에 대응하고, 값 0.25는 25%에 대응합니다.

<br>

감마 공간의 값은 물리적 에너지에 비례하지 않습니다. 값 0.5의 실제 물리적 밝기는 약 22%에 불과합니다.

셰이더가 이 비선형 값을 디코딩하지 않고 조명 계산에 사용하면 결과가 물리적 현실과 어긋나는데, 밝기 0.5인 조명 두 개를 합산하는 예시에서 그 차이가 드러납니다.

**선형 공간에서의 올바른 결과:**

$$
\text{빛 A}(0.5) + \text{빛 B}(0.5) = 1.0 \quad (50\% + 50\% = 100\%) \checkmark
$$

**감마 공간에서의 계산:**

$$
0.5^{2.2} \approx 0.218 \quad \Rightarrow \quad \text{빛 A의 실제 물리적 밝기} \approx 22\%
$$

$$
0.5^{2.2} \approx 0.218 \quad \Rightarrow \quad \text{빛 B의 실제 물리적 밝기} \approx 22\%
$$

셰이더가 감마 인코딩된 값을 디코딩 없이 합산하면 0.5 + 0.5 = 1.0, 즉 100%라는 결과를 냅니다. 그러나 각 값의 실제 물리적 밝기는 0.218이므로, 올바른 합산 결과는 0.218 + 0.218 = 0.436(43.6%)입니다. 셰이더 출력(100%)과 물리적 합산(43.6%) 사이에 두 배 이상의 차이가 생기며, 화면에는 물리적으로 올바른 밝기보다 과도하게 밝은 결과가 표시됩니다.

<br>

위 예시처럼, 감마 공간에서는 합산뿐 아니라 밝기에 관한 모든 산술이 왜곡됩니다. 중간 톤이 과도하게 밝아지고, 거리에 따라 빛의 세기가 줄어드는 조명 감쇠(Attenuation) 곡선도 부자연스러워집니다. 조명의 수가 많아지거나 반사 계산이 복잡해질수록 이 오차가 누적되어 더 두드러집니다.

### 선형 공간에서의 조명 계산

앞 절에서 선형 공간의 합산이 물리적으로 정확하다는 것을 확인했습니다. 이 정확성은 덧셈에만 국한되지 않고 곱셈에도 그대로 적용됩니다. 숫자 값과 물리적 에너지가 정비례하므로, 곱셈 결과 역시 물리적 비율을 그대로 반영합니다.

$$
0.8 \times 0.5 = 0.4 \quad (80\%\text{의 }50\% = 40\%) \checkmark
$$

이 성질은 셰이더의 반사 계산에서 특히 중요합니다. 표면의 Albedo(반사율)에 입사광 밝기를 곱하면 반사되어 나오는 빛의 양이 되는데, 선형 공간에서는 이 곱셈이 물리적으로 올바른 반사량을 바로 산출합니다.

$$
\text{Albedo}(0.6) \times \text{빛}(0.8) = 0.48 \quad (\text{올바른 반사량}) \checkmark
$$

---

## 감마 워크플로우 vs 선형 워크플로우

앞 절에서 확인했듯이, 조명 계산은 선형 공간에서 수행해야 물리적으로 정확합니다. 하지만 텍스처는 sRGB 감마 인코딩된 상태로 저장되고, 모니터도 입력 신호에 감마 약 2.2의 비선형 응답을 적용합니다. 셰이더에 값을 넘기기 전후에 감마 변환 단계를 거치느냐에 따라, 렌더링 파이프라인은 두 가지 워크플로우로 나뉩니다.

### 감마 워크플로우

감마 워크플로우에서는 텍스처의 감마 인코딩된 값을 변환 없이 그대로 셰이더에 전달합니다. 변환 과정이 없으므로 구현이 단순하지만, 셰이더가 감마 공간의 값으로 조명을 계산하게 되어 앞 절에서 살펴본 밝기 왜곡이 그대로 발생합니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 420" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="감마 워크플로우 파이프라인 다이어그램">
  <rect width="620" height="420" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">감마 워크플로우</text>
  <!-- Box 1: 텍스처 -->
  <rect x="170" y="56" width="280" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" stroke-dasharray="6,3" rx="6"/>
  <text x="310" y="83" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">텍스처 (감마 공간)</text>
  <!-- Arrow 1 -->
  <line x1="310" y1="100" x2="310" y2="138" stroke="#888" stroke-width="1.5"/>
  <polygon points="310,144 305,134 315,134" fill="#888"/>
  <text x="310" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">변환 없이 그대로 사용</text>
  <!-- Box 2: 셰이더 조명 계산 (문제) -->
  <rect x="140" y="148" width="340" height="44" fill="none" stroke="#ff6b6b" stroke-width="2" rx="6"/>
  <text x="310" y="175" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">셰이더 조명 계산 (감마 공간)</text>
  <!-- Arrow 2 -->
  <line x1="310" y1="192" x2="310" y2="230" stroke="#888" stroke-width="1.5"/>
  <polygon points="310,236 305,226 315,226" fill="#888"/>
  <text x="310" y="214" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">결과를 그대로 출력</text>
  <!-- Box 3: 프레임 버퍼 -->
  <rect x="170" y="240" width="280" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" rx="6"/>
  <text x="310" y="267" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">프레임 버퍼 (감마 공간)</text>
  <!-- Arrow 3 -->
  <line x1="310" y1="284" x2="310" y2="322" stroke="#888" stroke-width="1.5"/>
  <polygon points="310,328 305,318 315,318" fill="#888"/>
  <text x="310" y="306" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">모니터 감마 응답</text>
  <!-- Box 4: 화면 출력 -->
  <rect x="170" y="332" width="280" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" rx="6"/>
  <text x="310" y="359" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">화면 출력</text>
  <!-- Warning note -->
  <rect x="60" y="392" width="500" height="20" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.2" rx="6"/>
  <text x="310" y="407" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff6b6b">⚠ 조명 계산이 감마 공간에서 수행됨 → 물리적으로 부정확</text>
</svg>

### 선형 워크플로우

선형 워크플로우에서는 sRGB 텍스처를 셰이더에 전달할 때 GPU가 자동으로 선형 값으로 디코딩합니다.
조명 계산 결과는 선형 HDR 렌더 타깃에 저장되고, 노출·톤 매핑을 거쳐 LDR로 변환된 뒤 sRGB 인코딩되어 프레임 버퍼에 기록됩니다. 모니터의 감마 응답이 이 인코딩을 상쇄하여 의도한 밝기로 화면에 표시됩니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 556" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="선형 워크플로우 파이프라인 다이어그램">
  <rect width="620" height="556" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">선형 워크플로우</text>
  <!-- Box 1: 텍스처 -->
  <rect x="160" y="56" width="300" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" rx="6"/>
  <text x="310" y="83" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">텍스처 (sRGB)</text>
  <!-- Arrow 1: sRGB → Linear -->
  <line x1="310" y1="100" x2="310" y2="138" stroke="#73f38f" stroke-width="1.5"/>
  <polygon points="310,144 305,134 315,134" fill="#73f38f"/>
  <text x="310" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#73f38f">sRGB → Linear 디코딩 (sRGB 설정 시 GPU 자동)</text>
  <!-- Box 2: 셰이더 조명 계산 -->
  <rect x="130" y="148" width="360" height="44" fill="none" stroke="#73f38f" stroke-width="2" rx="6"/>
  <text x="310" y="175" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">셰이더 조명 계산 (선형 공간)</text>
  <!-- Arrow 2: 선형 저장 -->
  <line x1="310" y1="192" x2="310" y2="230" stroke="#73f38f" stroke-width="1.5"/>
  <polygon points="310,236 305,226 315,226" fill="#73f38f"/>
  <text x="310" y="214" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">선형 값 저장</text>
  <!-- Box 3: 렌더 타깃 (HDR) -->
  <rect x="140" y="240" width="340" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" rx="6"/>
  <text x="310" y="267" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">렌더 타깃 (선형 · HDR)</text>
  <!-- Arrow 3: 톤 매핑 + sRGB 인코딩 -->
  <line x1="310" y1="284" x2="310" y2="332" stroke="#73f38f" stroke-width="1.5"/>
  <polygon points="310,338 305,328 315,328" fill="#73f38f"/>
  <text x="310" y="308" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#73f38f">노출 · 톤 매핑 · Linear → sRGB 인코딩</text>
  <!-- Box 4: 최종 프레임 버퍼 -->
  <rect x="160" y="342" width="300" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" rx="6"/>
  <text x="310" y="369" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">최종 프레임 버퍼 (sRGB)</text>
  <!-- Arrow 4: 모니터 -->
  <line x1="310" y1="386" x2="310" y2="424" stroke="#888" stroke-width="1.5"/>
  <polygon points="310,430 305,420 315,420" fill="#888"/>
  <text x="310" y="408" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">모니터 감마 응답</text>
  <!-- Box 5: 화면 출력 -->
  <rect x="160" y="434" width="300" height="44" fill="none" stroke="#5B9BD5" stroke-width="1.5" rx="6"/>
  <text x="310" y="461" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">화면 출력</text>
  <!-- Success note -->
  <rect x="60" y="498" width="500" height="42" fill="#0e1f12" stroke="#73f38f" stroke-width="1.2" rx="6"/>
  <text x="310" y="516" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">✓ 조명 계산이 선형 공간에서 수행됨 → 물리적으로 정확</text>
  <text x="310" y="532" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">sRGB 디코딩/인코딩은 sRGB 설정 시 GPU 하드웨어가 자동 수행</text>
</svg>

<br>

sRGB 디코딩과 인코딩은 텍스처 및 렌더 타깃의 sRGB 설정이 켜져 있을 때 GPU 하드웨어가 자동으로 처리합니다. sRGB 텍스처를 샘플링하면 GPU가 선형 값으로 디코딩하고, sRGB 렌더 타깃에 기록하면 감마 인코딩을 적용하므로, 셰이더 코드에서 변환을 직접 작성할 필요가 없습니다.

### 두 워크플로우의 시각적 차이

같은 씬이라도 감마 워크플로우와 선형 워크플로우로 렌더링하면 시각적 결과가 달라집니다.

<br>

감마 워크플로우에서는 중간 톤이 지나치게 밝아지고, 조명 감쇠가 급격하며, 어두운 부분에서 디테일이 손실되고, 채도가 부자연스럽게 높아 보입니다.
반면 선형 워크플로우에서는 중간 톤이 자연스럽고, 조명 감쇠가 물리적으로 정확하며, 어두운 부분의 그라데이션이 보존되어 전체적으로 사실적인 결과를 냅니다.

<br>

이러한 왜곡은 물리 기반 셰이딩에서 특히 치명적입니다.
[색과 빛 (3)](/dev/unity/ColorAndLight-3/)에서 다루는 PBR(Cook-Torrance BRDF)은 미세면 이론을 기반으로 에너지 보존과 프레넬 효과를 수식에 내장한 셰이딩 모델이며, 선형 공간에서의 조명 계산을 전제로 설계되었습니다.
감마 워크플로우에서 PBR 머티리얼을 사용하면 비선형 값으로 셰이딩 수식이 계산되어 에너지 보존이 깨지고, 의도한 재질 표현이 나오지 않으므로 PBR을 사용하는 프로젝트에서는 반드시 선형 워크플로우를 선택해야 합니다.

---

## sRGB

### sRGB란

**sRGB(Standard Red Green Blue)**는 1996년에 Microsoft와 HP가 공동으로 정의한 **표준 색공간**입니다. 특정 원색 좌표(색역), D65 백색점, 감마 약 2.2의 전달 함수를 하나의 규격으로 묶어, 서로 다른 장치에서도 같은 숫자가 같은 색으로 재현되도록 합니다. 각 채널의 값 범위는 0에서 1이며, 8비트 기준으로는 0에서 255입니다.

모니터, 카메라, 웹 브라우저, 이미지 편집 도구 대부분이 sRGB를 기본 색공간으로 사용하며, 게임 텍스처 역시 대다수가 sRGB로 저장되어 있습니다.

<br>

sRGB 전달 함수는 정확히 하나의 수식이 아니라, 0에 가까운 구간에서 선형 함수를, 나머지 구간에서 지수 2.4의 거듭제곱 함수를 이어 붙인 혼합 곡선입니다.

지수가 2.4임에도 "감마 약 2.2"라 부르는 이유는, 두 구간을 결합한 전체 곡선의 실효 감마(effective gamma) — 즉, 곡선 전체를 단일 거듭제곱 함수로 근사했을 때의 지수 — 가 약 2.2에 수렴하기 때문입니다.

<br>

텍스처가 담고 있는 데이터의 성격에 따라 sRGB 인코딩 여부가 나뉩니다.
눈에 보이는 색상을 저장한 텍스처는 sRGB로 인코딩되어 있습니다.

- 색상 텍스처 (Albedo, Diffuse, Emissive 등)
- UI 이미지
- 사진, 스크린샷

반면, 색상이 아닌 물리적 수치를 저장하는 데이터 텍스처는 처음부터 선형 값이므로 sRGB 인코딩이 적용되어 있지 않으며, Linear로 임포트해야 합니다.

- 노멀맵 — 법선 방향 벡터
- 메탈릭/러프니스 맵 — 재질 물리 파라미터
- 하이트맵 — 높이 스칼라 값
- 라이트맵 — 조명 강도 (선형 또는 RGBM 인코딩)

<br>

sRGB 텍스처를 셰이더에서 샘플링할 때, GPU가 자동으로 감마 디코딩(선형 변환)을 수행합니다.
이미 선형인 데이터 텍스처에 이 디코딩이 적용되면 값 자체가 왜곡됩니다.
예를 들어 노멀맵에서 법선 방향을 나타내는 값 0.5가 감마 디코딩을 거치면 0.5^2.2 ≈ 0.218로 바뀌어, 셰이더가 전혀 다른 방향의 법선으로 조명을 계산하게 됩니다.
데이터 텍스처를 Linear로 임포트해야 하는 이유가 바로 이것입니다.

### 텍스처 임포트 설정

앞서 설명한 sRGB 텍스처와 Linear 텍스처의 구분은 Unity의 Texture Import Settings에서 sRGB(Color Texture) 체크박스로 제어합니다.
체크박스를 켜면 GPU가 셰이더 샘플링 시 자동으로 감마 디코딩(선형 변환)을 수행하고, 끄면 저장된 값을 그대로 전달합니다.

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

sRGB 설정을 잘못 적용하면 렌더링 오류가 발생합니다.
노멀맵에 sRGB를 켜면 법선 벡터에 불필요한 감마 디코딩이 적용되어 조명이 비정상적으로 반응하고, 반대로 Albedo 텍스처에 sRGB를 끄면 감마 디코딩이 누락되어 색상이 의도보다 어둡게 출력됩니다.
텍스처를 임포트한 뒤 조명 반응이나 색감이 이상하다면 이 체크박스 설정을 먼저 확인해야 합니다.

---

## HDR

### LDR의 한계

지금까지 다룬 색상 값은 모두 최종 저장 값이 0에서 1(8비트면 0에서 255) 범위로 제한되어 있었습니다. 이처럼 한 장면에서 동시에 표현할 수 있는 밝기 비율, 즉 **다이나믹 레인지(Dynamic Range)**가 좁은 방식을 **LDR(Low Dynamic Range)**이라 합니다.

<br>

하지만 현실 세계의 밝기 범위는 모니터보다 훨씬 넓습니다. 한밤중의 달빛부터 직사광선까지, 실제 밝기 비율은 수백만 대 1에 달합니다. **HDR(High Dynamic Range)**은 렌더링 계산 단계에서 1.0을 넘는 값도 다룰 수 있도록 확장한 방식이며, 최종 출력 시 톤 매핑과 sRGB 인코딩을 거쳐 0~1 범위의 LDR로 변환됩니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 310" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="현실 세계의 밝기 범위 대수 척도 시각화">
  <rect width="620" height="310" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">현실 세계의 밝기 범위</text>
  <!-- Scale bar -->
  <rect x="50" y="66" width="520" height="20" fill="#2a2f2e" rx="3"/>
  <rect x="50"  y="66" width="104" height="20" fill="#1a2a4a"/>
  <rect x="154" y="66" width="104" height="20" fill="#1e3a5a"/>
  <rect x="258" y="66" width="104" height="20" fill="#2a5a7a"/>
  <rect x="362" y="66" width="104" height="20" fill="#3a7a9a"/>
  <rect x="466" y="66" width="52"  height="20" fill="#5aaa9a"/>
  <rect x="518" y="66" width="52"  height="20" fill="#f0c040"/>
  <rect x="50"  y="66" width="520" height="20" fill="none" stroke="#444" stroke-width="1" rx="3"/>
  <!-- Tick marks and labels -->
  <line x1="50"  y1="86" x2="50"  y2="96" stroke="#888" stroke-width="1.2"/>
  <text x="50"  y="109" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">별빛</text>
  <text x="50"  y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">0.0001</text>
  <line x1="154" y1="86" x2="154" y2="96" stroke="#888" stroke-width="1.2"/>
  <text x="154" y="109" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">달빛</text>
  <text x="154" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">0.01</text>
  <line x1="258" y1="86" x2="258" y2="96" stroke="#888" stroke-width="1.2"/>
  <text x="258" y="109" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">실내 조명</text>
  <text x="258" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">1.0</text>
  <line x1="362" y1="86" x2="362" y2="96" stroke="#888" stroke-width="1.2"/>
  <text x="362" y="109" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">흐린 날 야외</text>
  <text x="362" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">10</text>
  <line x1="466" y1="86" x2="466" y2="96" stroke="#888" stroke-width="1.2"/>
  <text x="466" y="109" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">맑은 날 야외</text>
  <text x="466" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">100</text>
  <line x1="570" y1="86" x2="570" y2="96" stroke="#888" stroke-width="1.2"/>
  <text x="570" y="109" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">직사광선</text>
  <text x="570" y="122" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#888">10,000</text>
  <!-- LDR bracket -->
  <line x1="50"  y1="148" x2="258" y2="148" stroke="#ff6b6b" stroke-width="2"/>
  <line x1="50"  y1="143" x2="50"  y2="153" stroke="#ff6b6b" stroke-width="2"/>
  <line x1="258" y1="143" x2="258" y2="153" stroke="#ff6b6b" stroke-width="2"/>
  <text x="154" y="168" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ff6b6b" font-weight="bold">LDR이 한 번에 담는 범위</text>
  <text x="154" y="183" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="10" fill="#ff6b6b" opacity="0.7">(노출에 따라 이동)</text>
  <!-- HDR bracket -->
  <line x1="50"  y1="208" x2="570" y2="208" stroke="#73f38f" stroke-width="2"/>
  <line x1="50"  y1="203" x2="50"  y2="213" stroke="#73f38f" stroke-width="2"/>
  <line x1="570" y1="203" x2="570" y2="213" stroke="#73f38f" stroke-width="2"/>
  <text x="310" y="228" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f" font-weight="bold">HDR</text>
  <text x="310" y="264" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">LDR은 현실 밝기의 극히 일부만 표현 가능</text>
  <text x="310" y="284" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">(상대 밝기 예시 · 로그 척도로 간소화)</text>
</svg>

### HDR 렌더링

HDR 렌더링에서는 프레임 버퍼에 0~1 범위를 넘는 값을 저장합니다.
태양의 밝기를 10.0으로, 금속 표면의 반사를 5.0으로 표현하는 식입니다.
LDR의 8비트 정수 포맷은 0~1 범위만 담을 수 있으므로, HDR에서는 **16비트 부동소수점(half-float)** 또는 **32비트 부동소수점** 프레임 버퍼를 사용합니다.

<br>

| 항목 | LDR (R8G8B8A8) | HDR (R16G16B16A16F) |
|---|---|---|
| 채널당 | 8비트 정수 | 16비트 부동소수점 |
| 범위 | 0 ~ 1 (0 ~ 255) | 0 이상 (half-float 최대 65504) |
| 크기 | 4바이트/픽셀 | 8바이트/픽셀 |
| 1080p | 약 8MB | 약 16MB (LDR의 2배) |

<br>

픽셀당 크기가 LDR의 2배인 만큼, 같은 해상도에서 메모리 사용량과 대역폭 소비도 2배가 됩니다.
메모리 대역폭이 제한적인 모바일 환경에서는 이 추가 비용이 프레임 레이트에 직접 영향을 주기 때문에, 블룸이나 톤 매핑처럼 1.0을 초과하는 값을 활용하는 후처리가 필요하지 않다면 LDR 프레임 버퍼만으로 충분합니다.

### 톤 매핑 (Tone Mapping)

HDR로 렌더링된 이미지를 최종적으로 화면에 표시하려면, 모니터가 표현할 수 있는 LDR 범위로 변환해야 합니다.
**톤 매핑(Tone Mapping)**이 이 변환을 담당합니다.
보통 먼저 노출(Exposure)로 장면 전체의 밝기를 조절한 뒤, 톤 매핑이 하이라이트를 비선형적으로 압축합니다.

<br>

HDR 렌더링에서 1.0은 기준 밝기(화이트 포인트)에 해당하며, 1.0을 초과하는 값은 하이라이트로 취급됩니다.
이 하이라이트를 단순히 1.0으로 잘라내면(클램핑), 원래 2.0이었던 곳과 10.0이었던 곳이 모두 같은 1.0이 되어 밝은 영역의 디테일이 사라집니다.
톤 매핑은 값이 커질수록 출력의 증가폭을 줄여, 하이라이트가 1.0 근처로 부드럽게 눌리면서도 서로 간의 차이는 유지되도록 합니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 320" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="톤 매핑의 역할 — 클램핑 vs 톤 매핑 비교">
  <rect width="620" height="320" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">톤 매핑의 역할</text>
  <!-- HDR values row -->
  <text x="70"  y="72" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">0</text>
  <text x="168" y="72" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">0.5</text>
  <text x="266" y="72" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">1.0</text>
  <text x="364" y="72" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">2.0</text>
  <text x="462" y="72" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">5.0</text>
  <text x="560" y="72" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">10.0</text>
  <text x="310" y="56" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">HDR 입력</text>
  <line x1="40" y1="84" x2="590" y2="84" stroke="#333" stroke-width="1"/>
  <!-- Clamping section -->
  <rect x="40" y="94" width="540" height="80" fill="#1f1010" stroke="#ff6b6b" stroke-width="1" rx="4"/>
  <text x="310" y="112" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ff6b6b" font-weight="bold">클램핑 (단순 자르기) — 출력</text>
  <text x="70"  y="136" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">0</text>
  <text x="168" y="136" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">0.5</text>
  <text x="266" y="136" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ccc">1.0</text>
  <text x="364" y="136" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ff6b6b">1.0</text>
  <text x="462" y="136" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ff6b6b">1.0</text>
  <text x="560" y="136" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#ff6b6b">1.0</text>
  <text x="430" y="158" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff6b6b">차이가 모두 사라짐</text>
  <!-- Tone mapping section -->
  <rect x="40" y="188" width="540" height="80" fill="#0e1a0e" stroke="#73f38f" stroke-width="1" rx="4"/>
  <text x="310" y="206" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f" font-weight="bold">톤 매핑 (비선형 압축) — 출력</text>
  <text x="70"  y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f">0</text>
  <text x="168" y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f">0.4</text>
  <text x="266" y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f">0.7</text>
  <text x="364" y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f">0.85</text>
  <text x="462" y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f">0.95</text>
  <text x="560" y="230" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" fill="#73f38f">0.98</text>
  <text x="430" y="252" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">밝은 영역도 차이가 보존됨</text>
  <text x="310" y="292" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">값이 커질수록 출력 증가폭이 줄어듦 — 하이라이트 디테일 보존 (예시 값)</text>
</svg>

<br>

대표적인 톤 매핑 알고리즘으로는 Reinhard, ACES(Academy Color Encoding System), Neutral 등이 있으며, 압축 곡선의 형태에 따라 같은 HDR 데이터라도 색감과 대비가 달라집니다.

<br>

| 알고리즘 | 특징 |
|---|---|
| Reinhard | 밝은 영역을 부드럽게 압축하는 단순한 곡선 |
| ACES (Filmic) | 영화 필름의 톤 곡선을 모방하여 대비가 강하고 채도가 풍부함 |
| Neutral | 색상(Hue)과 채도(Saturation) 변화를 최소화하고 밝기만 압축 |

<br>

Unity URP(Universal Render Pipeline)에서는 Volume 시스템의 Tonemapping 설정에서 Neutral과 ACES를 선택할 수 있습니다.

### Bloom과 HDR

**Bloom**은 밝은 광원 주변에서 빛이 번지는 효과입니다.
Bloom을 적용하려면 "특별히 밝은 부분"을 구별할 기준이 필요한데, LDR에서는 모든 밝기가 0~1 범위 안에 있어서 이 기준을 잡기 어렵습니다.
임계값을 0.8로 설정하면 0.8~1.0 사이의 모든 영역에 Bloom이 걸려, 의도하지 않은 곳까지 빛이 번집니다.

<br>

HDR에서는 1.0을 초과하는 값이 존재하므로, 임계값을 1.0으로 설정하면 태양, 발광체, 폭발처럼 실제로 강하게 빛나는 영역에만 Bloom이 적용됩니다.
"1.0 초과 = 특별히 밝은 부분"이라는 물리적 기준이 생기기 때문에, HDR 렌더링에서 Bloom이 자연스러운 결과를 냅니다.

---

## Unity의 Color Space 설정

Unity는 **Project Settings > Player > Other Settings > Color Space**에서 Gamma와 Linear 중 하나를 선택하도록 합니다. 이 설정이 앞서 다룬 선형 워크플로우, sRGB 텍스처 처리, HDR 렌더링의 동작 방식을 결정합니다.

<br>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 620 416" style="width:100%;max-width:620px;display:block;margin:0 auto" aria-label="Unity Color Space 설정 UI 및 Gamma vs Linear 비교">
  <rect width="620" height="416" fill="#1a1f1e" stroke="#333" stroke-width="1.5" rx="8"/>
  <text x="310" y="36" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold" fill="#f9fffb">Unity Color Space 설정</text>
  <!-- Settings panel mockup -->
  <rect x="160" y="52" width="300" height="90" fill="#111615" stroke="#555" stroke-width="1.2" rx="5"/>
  <rect x="160" y="52" width="300" height="22" fill="#2a2f2e" stroke="none" rx="5"/>
  <rect x="160" y="63" width="300" height="11" fill="#2a2f2e" stroke="none"/>
  <text x="310" y="67" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#aaa">Project Settings  ▷  Player  ▷  Other Settings</text>
  <text x="180" y="94" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">Color Space</text>
  <circle cx="264" cy="90" r="5" fill="none" stroke="#888" stroke-width="1.5"/>
  <text x="274" y="94" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">Gamma</text>
  <circle cx="340" cy="90" r="5" fill="none" stroke="#73f38f" stroke-width="1.5"/>
  <circle cx="340" cy="90" r="2.5" fill="#73f38f"/>
  <text x="350" y="94" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">Linear</text>
  <text x="310" y="128" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#555">HDRP: Linear 필수 / URP: Linear 권장 (템플릿 기본값인 경우 많음)</text>
  <line x1="40" y1="158" x2="580" y2="158" stroke="#333" stroke-width="1"/>
  <!-- Gamma column -->
  <rect x="40" y="164" width="258" height="196" fill="#1a1212" stroke="#ff6b6b" stroke-width="1.2" rx="5"/>
  <rect x="40" y="164" width="258" height="28" fill="#2a1515" stroke="none" rx="5"/>
  <rect x="40" y="183" width="258" height="9" fill="#2a1515" stroke="none"/>
  <text x="169" y="183" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#ff6b6b">Gamma</text>
  <text x="58" y="212" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">•  텍스처를 선형화하지 않고 조명 계산</text>
  <text x="58" y="232" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">•  감마 공간 조명 계산</text>
  <text x="58" y="252" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">•  구형/저사양 호환에 유리</text>
  <text x="58" y="272" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff6b6b">•  PBR/블렌딩 결과 왜곡 가능</text>
  <text x="58" y="292" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff6b6b">•  중간 톤이 과도하게 밝아질 수 있음</text>
  <text x="58" y="312" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ff6b6b">•  에너지 보존 가정이 깨질 수 있음</text>
  <!-- Linear column -->
  <rect x="322" y="164" width="258" height="196" fill="#0e1a0e" stroke="#73f38f" stroke-width="1.2" rx="5"/>
  <rect x="322" y="164" width="258" height="28" fill="#0e2010" stroke="none" rx="5"/>
  <rect x="322" y="183" width="258" height="9" fill="#0e2010" stroke="none"/>
  <text x="451" y="183" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="13" font-weight="bold" fill="#73f38f">Linear</text>
  <text x="340" y="212" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">•  GPU가 sRGB 텍스처를 자동 선형화</text>
  <text x="340" y="232" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">•  선형 공간 조명 계산</text>
  <text x="340" y="252" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#ccc">•  sRGB 샘플링 지원 필요 (모바일: GLES3+)</text>
  <text x="340" y="272" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">•  물리적으로 정확</text>
  <text x="340" y="292" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">•  PBR 전제 조건</text>
  <text x="340" y="312" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">•  에너지 보존 유지</text>
  <text x="340" y="332" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#73f38f">•  HDR/톤 매핑 워크플로우에 유리</text>
  <text x="310" y="380" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="12" fill="#888">프로젝트 시작 시 결정 — 개발 중 변경 시 머티리얼·라이팅 전체 재작업 필요</text>
  <text x="310" y="396" text-anchor="middle" font-family="'Noto Sans KR',sans-serif" font-size="11" fill="#555">HDRP는 Linear만 지원</text>
</svg>

### 모바일에서 Linear Color Space의 지원

Linear 색공간을 사용하려면 GPU가 **sRGB 텍스처 샘플링**과 **sRGB 프레임 버퍼 쓰기**를 하드웨어적으로 지원해야 합니다. PC와 콘솔에서는 거의 모든 기기가 지원하지만, 모바일에서는 기기의 GPU와 API 버전에 따라 지원 여부가 달라집니다. Android에서는 OpenGL ES 3.0 이상 또는 Vulkan을 지원하는 GPU와 Android 4.3(API Level 18) 이상이 필요하고, iOS에서는 Metal API를 지원하는 A7 칩 이상(iPhone 5s 이후)에서 사용할 수 있습니다.

<br>

이 조건을 만족하지 않는 구형 기기에서는 Unity가 자동으로 Gamma 모드로 폴백(fallback)하며, 앞서 설명한 감마 워크플로우의 한계가 그대로 적용되어 조명 계산이 부정확해지고 PBR 결과가 의도와 달라질 수 있습니다.

### 프로젝트 시작 시 설정

Color Space는 프로젝트 초기에 결정하고 이후에 변경하지 않는 것이 원칙입니다. 개발 중간에 Gamma에서 Linear로(또는 반대로) 전환하면 기존에 만든 모든 머티리얼과 라이팅의 시각적 결과가 달라지고, 아티스트가 색상 값과 조명 강도를 처음부터 다시 조정해야 하므로 프로젝트 규모에 비례하는 추가 작업이 발생합니다.

<br>

PBR을 사용하는 프로젝트라면 처음부터 Linear를 선택해야 합니다. HDRP는 Linear만 지원하며, URP의 Lit Shader도 Linear 색공간을 전제로 설계되어 있어 Gamma에서 사용하면 에너지 보존 가정이 깨지고 의도한 재질 표현이 나오지 않을 수 있습니다.

---

## 마무리

- RGB 색 모델은 빨강, 초록, 파랑 세 원색의 가산 혼합으로 색을 표현합니다. 채널당 8비트(0~255)가 일반적이며, 셰이더 내부에서는 0.0~1.0 부동소수점을 사용합니다
- 감마 보정은 8비트의 제한된 단계를 인간의 비선형적 밝기 인지에 맞게 재분배합니다. 이미지를 감마 1/2.2로 인코딩하여 저장하고, 모니터가 감마 2.2로 디코딩하여 원래의 물리적 밝기를 복원합니다
- 선형 색공간에서는 밝기 값이 물리적 에너지에 비례하므로 조명 계산이 정확합니다. 감마 공간에서 조명 계산을 수행하면 오차가 누적되어 결과가 부정확해집니다
- 선형 워크플로우는 텍스처를 선형으로 디코딩한 뒤 조명 계산을 수행하고, 결과를 감마 인코딩하여 출력합니다. GPU가 sRGB 변환을 하드웨어적으로 처리합니다
- sRGB는 감마 약 2.2 기반의 표준 색공간이며, 색상 텍스처에 적용되지만 노멀맵이나 메탈릭맵 같은 데이터 텍스처에는 적용하지 않습니다
- HDR은 렌더링 계산 단계에서 1.0을 넘는 밝기 값을 다루며, 노출 조절과 톤 매핑을 거쳐 LDR 범위로 변환됩니다. Bloom은 HDR의 1.0 초과 값을 기준으로 적용할 때 자연스러운 결과를 냅니다
- Unity에서는 Color Space를 Linear로 설정해야 PBR이 올바르게 동작하며, 2015년 이후 출시된 대부분의 모바일 기기가 이를 지원합니다

이 개념들은 각각 독립적이지 않습니다. 텍스처에 저장된 색이 sRGB 디코딩을 거쳐 선형 공간에서 조명 계산되고, 감마 인코딩을 거쳐 화면에 표시되기까지 하나의 파이프라인으로 연결됩니다.

이 글에서 다룬 디지털 색 표현과 Part 1의 빛의 물리적 원리가 갖추어지면, 다음 단계는 표면의 밝기를 실제로 계산하는 **셰이딩 모델**입니다. Lambert, Phong, Blinn-Phong의 전통적 모델에서 시작하여, PBR의 Cook-Torrance 모델이 왜 에너지 보존과 프레넬 효과를 내장하게 되었는지까지 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

<br>

---

**관련 글**
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- **색과 빛 (2) - 색 표현과 색공간 (현재 글)**
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)

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
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)
- [게임 물리 (1) - 강체 역학의 원리](/dev/unity/GamePhysics-1/)
- [게임 물리 (2) - 충돌 검출의 원리](/dev/unity/GamePhysics-2/)
- [게임 물리 (3) - 제약 조건과 솔버](/dev/unity/GamePhysics-3/)
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
