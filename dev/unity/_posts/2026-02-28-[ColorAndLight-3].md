---
layout: single
title: "색과 빛 (3) - 셰이딩 모델 - soo:bak"
date: "2026-02-28 23:06:00 +0900"
description: Lambert 모델, Phong, Blinn-Phong, PBR, Metallic 워크플로우, Unity Lit Shader를 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 셰이딩
  - PBR
  - 모바일
---

## 물리 법칙을 코드로

[색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 빛의 반사·굴절·흡수와 이를 하나의 함수로 통합하는 BRDF 개념을, [색과 빛 (2)](/dev/unity/ColorAndLight-2/)에서 RGB 색 모델, 감마 보정, 선형 워크플로우를 다루었습니다. 빛의 물리적 원리와 색 표현 체계가 갖추어졌으므로, 이제 표면의 밝기를 실제로 계산하는 단계로 넘어갑니다.

컴퓨터 그래픽스 초기에는 표면을 단일 색상으로 칠하는 것이 전부였습니다. 빛의 각도에 따라 밝기가 달라지는 것조차 계산하지 않았습니다.

1970년대에 이르러, 빛이 표면에 닿았을 때 관찰자가 보는 밝기와 색을 수학적으로 정의하는 **셰이딩 모델(Shading Model)**이 등장하면서 화면 속 물체에 처음으로 명암과 광택이 생겼습니다.

[색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 BRDF — 특정 방향에서 들어온 빛이 특정 방향으로 반사되는 비율을 정의하는 함수 — 를 구체적인 수식으로 구현한 것이 셰이딩 모델입니다.

초기 모델들은 물리 법칙에서 유도된 것이 아니라, 눈으로 보기에 그럴듯한 결과를 내도록 수식을 직접 만든 경험적(Empirical) 모델이었습니다.

에너지 보존이나 프레넬 효과가 빠져 있었으므로, 파라미터를 바꾸면 물리적으로 불가능한 결과가 나오기도 했습니다.

GPU 성능이 충분해진 2010년대 이후, 이런 물리 법칙을 수식에 직접 반영하는 PBR(Physically Based Rendering)이 업계 표준으로 자리 잡았습니다.

<br>

이 글에서는 가장 단순한 Lambert 모델부터 시작하여 Phong, Blinn-Phong을 거쳐 PBR까지, 셰이딩 모델의 발전 과정과 각 모델의 수학적 구조를 다룹니다.

---

## Lambert 모델

### 난반사의 수학적 표현

Lambert 모델은 **난반사(Diffuse Reflection)**만을 계산하는 가장 단순한 셰이딩 모델입니다. [색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 것처럼, 난반사는 거친 표면에서 빛이 모든 방향으로 고르게 분산되는 현상입니다. Lambert 모델은 이 성질을 이상적으로 모델링하여, 관찰자가 어떤 각도에서 보더라도 표면의 밝기가 같다고 가정합니다.

관찰 방향이 밝기에 영향을 주지 않으므로, 밝기를 결정하는 것은 빛이 표면에 닿는 각도뿐입니다. 이 각도를 수학적으로 표현하면 **표면 법선(N)**과 **광원 방향(L)**의 내적이 됩니다.

**Lambert 모델의 수식**

$$
\text{Diffuse} = \max(\mathbf{N} \cdot \mathbf{L},\ 0) \times C_{\text{light}} \times C_{\text{albedo}}
$$

- $\mathbf{N}$: 표면 법선 벡터 (단위 벡터 — 크기가 1이어야 내적이 cos θ 값이 됨)
- $\mathbf{L}$: 표면에서 광원을 향하는 방향 벡터 (단위 벡터)
- $\mathbf{N} \cdot \mathbf{L}$: 두 벡터의 내적 ($= \cos\theta$, $\theta$는 법선과 광원 방향 사이의 각도)
- $C_{\text{light}}$: 광원의 색상과 강도
- $C_{\text{albedo}}$: 표면의 Albedo — 각 파장(RGB 채널)별 반사율을 0.0~1.0 범위로 나타낸 값

$\max$ 함수는 내적이 음수가 되는 경우, 즉 빛이 표면 뒤쪽에서 오는 경우를 0으로 잘라냅니다(클램프). 빛이 닿지 않는 면의 밝기는 0입니다.

cos θ 값을 구체적인 각도에 대입하면 밝기 변화를 확인할 수 있습니다. 빛이 표면에 수직으로 내리쬘 때(θ = 0°) cos 0° = 1이므로 밝기가 최대이고, 빛이 표면과 평행하게 스칠 때(θ = 90°) cos 90° = 0이므로 밝기가 0이 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <rect x="1" y="1" width="418" height="368" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="26" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Lambert 모델의 동작</text>

  <!-- 표면 (수평선) -->
  <line x1="60" y1="170" x2="360" y2="170" stroke="currentColor" stroke-width="2"/>
  <text x="370" y="174" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6" text-anchor="start">표면</text>

  <!-- 표면 위의 점 -->
  <circle cx="210" cy="170" r="4" fill="currentColor"/>

  <!-- 법선 벡터 N (수직 위) -->
  <line x1="210" y1="170" x2="210" y2="55" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="210,48 206,58 214,58" fill="currentColor"/>
  <text x="222" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">N</text>
  <text x="222" y="64" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(법선)</text>

  <!-- 광원 방향 벡터 L (대각선, 약 45도) -->
  <line x1="210" y1="170" x2="128" y2="75" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="124,70 126,82 136,76" fill="currentColor"/>
  <text x="110" y="70" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L</text>
  <text x="90" y="82" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(빛 방향)</text>

  <!-- θ 각도 호 -->
  <path d="M 210,130 A 40,40 0 0,0 184,140" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3,2"/>
  <text x="186" y="128" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">θ</text>

  <!-- 구분선 -->
  <line x1="30" y1="195" x2="390" y2="195" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- 각도별 밝기 데이터 (5행) -->
  <!-- 헤더 -->
  <text x="50" y="218" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">각도</text>
  <text x="170" y="218" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">N · L</text>
  <text x="310" y="218" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">밝기</text>
  <line x1="40" y1="224" x2="390" y2="224" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>

  <!-- θ = 0° -->
  <text x="50" y="244" font-family="sans-serif" font-size="10" fill="currentColor">θ = 0°</text>
  <text x="110" y="244" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(정면)</text>
  <text x="170" y="244" font-family="sans-serif" font-size="10" fill="currentColor">cos 0° = 1.0</text>
  <text x="310" y="244" font-family="sans-serif" font-size="10" fill="currentColor">최대 (100%)</text>

  <!-- θ = 45° -->
  <text x="50" y="268" font-family="sans-serif" font-size="10" fill="currentColor">θ = 45°</text>
  <text x="170" y="268" font-family="sans-serif" font-size="10" fill="currentColor">cos 45° ≈ 0.707</text>
  <text x="310" y="268" font-family="sans-serif" font-size="10" fill="currentColor">약 71%</text>

  <!-- θ = 60° -->
  <text x="50" y="292" font-family="sans-serif" font-size="10" fill="currentColor">θ = 60°</text>
  <text x="170" y="292" font-family="sans-serif" font-size="10" fill="currentColor">cos 60° = 0.5</text>
  <text x="310" y="292" font-family="sans-serif" font-size="10" fill="currentColor">50%</text>

  <!-- θ = 90° -->
  <text x="50" y="316" font-family="sans-serif" font-size="10" fill="currentColor">θ = 90°</text>
  <text x="110" y="316" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(수평)</text>
  <text x="170" y="316" font-family="sans-serif" font-size="10" fill="currentColor">cos 90° = 0.0</text>
  <text x="310" y="316" font-family="sans-serif" font-size="10" fill="currentColor">0</text>

  <!-- θ > 90° -->
  <text x="50" y="340" font-family="sans-serif" font-size="10" fill="currentColor">θ > 90°</text>
  <text x="110" y="340" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(뒤쪽)</text>
  <text x="170" y="340" font-family="sans-serif" font-size="10" fill="currentColor">N · L &lt; 0 → max(N·L, 0) = 0</text>
  <text x="310" y="354" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">클램프로 0 처리</text>
</svg>
</div>

### Lambert 모델의 BRDF

앞 섹션의 Diffuse 수식은 광원 색상과 강도까지 포함한 최종 밝기를 계산하는 식입니다. BRDF는 그중에서 표면 자체의 반사 특성만을 분리한 함수로, 입사 방향과 반사 방향에 따라 빛이 반사되는 비율을 정의합니다.

Lambert 모델은 어떤 방향에서 보아도 밝기가 같으므로, BRDF가 방향에 의존하지 않는 상수가 됩니다.

**Lambert BRDF**

$$
f_{\text{Lambert}} = \frac{C_{\text{albedo}}}{\pi}
$$

$C_{\text{albedo}}$를 $\pi$로 나누는 것은 에너지 보존을 위한 정규화(normalization)입니다.

[색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 것처럼 표면에서 나가는 빛의 총 에너지는 들어온 빛의 에너지를 초과할 수 없으므로, BRDF는 이 제약을 만족하도록 크기가 조정되어야 합니다.

<br>

표면의 한 점에서 빛이 반사되어 나갈 수 있는 영역은 표면 위쪽의 반구(hemisphere) 전체입니다.

총 반사 에너지를 구하려면, 반구의 모든 방향에 대해 BRDF 값에 cos θ를 곱한 뒤 적분합니다.

cos θ를 곱하는 이유는 입사각에서와 같은 기하학적 원리입니다. 빛이 표면의 수직에서 벗어날수록 같은 면적에 투영되는 에너지가 줄어들듯, 반사 방향이 법선에서 벗어날수록 해당 방향의 기여도도 줄어들며, 그 비율이 cos θ입니다.

Lambert BRDF는 상수이므로 적분 밖으로 꺼낼 수 있고, cos θ만 반구 전체에 대해 적분하면 그 값이 π입니다. 따라서 Lambert BRDF가 $C_{\text{albedo}} / \pi$이면 총 반사 에너지는 $C_{\text{albedo}}$가 됩니다.

$C_{\text{albedo}}$의 각 채널은 0.0~1.0 범위이므로, 총 반사 에너지는 입사 에너지 이하로 유지됩니다. π로 나누지 않으면 총 반사 에너지가 $\pi \cdot C_{\text{albedo}}$가 되어 입사 에너지를 초과할 수 있습니다.

<br>

실제 셰이더 구현에서는 Diffuse 계산의 나누기를 줄이기 위해 이 π를 생략하기도 합니다. 생략하면 Diffuse가 π배 밝아지지만, 광원 강도를 π로 나누어 상쇄할 수 있습니다.

Unity의 URP Lit Shader처럼 PBR을 엄밀하게 구현하는 셰이더는 BRDF 자체에 π 나누기를 포함하지만, 레거시 셰이더나 커스텀 셰이더에서는 생략하고 광원 쪽에서 보정하는 관례가 남아 있습니다.

### Lambert 모델의 한계

Lambert 모델은 정반사(Specular Reflection)를 표현하지 못합니다. 관찰 방향을 고려하지 않으므로, 플라스틱이나 금속 표면에서 보이는 밝은 하이라이트를 재현할 수 없습니다. 분필, 콘크리트, 사포처럼 완전히 무광인 재질에는 적합하지만, 광택이 있는 대부분의 재질을 표현하려면 정반사 성분을 추가해야 합니다.

---

## Phong 모델

### 정반사의 추가

1975년 Bui Tuong Phong은 Lambert 모델에 **정반사(Specular Reflection)** 성분을 추가하여 광택 표현이 가능한 셰이딩 모델을 제안했습니다. Phong 모델은 세 가지 성분을 각각 계산한 뒤 합산합니다.

- **Ambient**(환경광) — 실제 장면에서는 다른 표면에서 반사된 빛, 하늘 빛 등 간접광이 존재하여 그림자 영역도 완전한 검정이 되지 않습니다. Ambient는 이 간접광을 하나의 상수로 단순 근사한 항입니다.
- **Diffuse**(난반사) — 앞 섹션의 Lambert 모델과 동일합니다.
- **Specular**(정반사) — 표면의 밝은 하이라이트를 만드는 항입니다.

**Phong 모델의 수식**

$$
\text{Color} = \text{Ambient} + \text{Diffuse} + \text{Specular}
$$

$$
\begin{aligned}
\text{Ambient} &= C_{\text{ambient}} \times C_{\text{albedo}} \\
\text{Diffuse} &= \max(\mathbf{N} \cdot \mathbf{L},\ 0) \times C_{\text{light}} \times C_{\text{albedo}} \\
\text{Specular} &= \max(\mathbf{R} \cdot \mathbf{V},\ 0)^{n} \times C_{\text{light}} \times C_{\text{spec}}
\end{aligned}
$$

- $\mathbf{R}$: 반사 벡터 — 입사광이 표면 법선을 기준으로 대칭 반사된 방향
- $\mathbf{V}$: 표면에서 카메라를 향하는 방향 벡터
- $n$: 광택 지수(Shininess Exponent) — 값이 클수록 하이라이트가 작고 날카로워 광택이 강한 표면을, 값이 작을수록 하이라이트가 넓고 부드러워 무광에 가까운 표면을 표현
- $C_{\text{spec}}$: 정반사 색상
- $C_{\text{ambient}}$: 환경광 색상

Ambient와 Diffuse는 앞 섹션의 Lambert 모델에서 다룬 것과 같으므로, Phong 모델의 핵심은 새로 추가된 Specular 항입니다.

### 반사 벡터와 하이라이트

Specular 항은 두 벡터의 관계로 결정됩니다.

**반사 벡터 R**은 입사광이 표면 법선을 기준으로 대칭 반사된 방향이고, **시야 벡터 V**는 표면에서 카메라를 향하는 방향입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 배경 -->
  <rect x="0.5" y="0.5" width="419" height="259" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="210" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Phong 모델의 Specular 계산</text>
  <!-- 화살촉 마커 정의 -->
  <defs>
    <marker id="arrowSpec" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0,0 8,3 0,6" fill="currentColor"/>
    </marker>
  </defs>
  <!-- 표면 선 -->
  <line x1="60" y1="200" x2="360" y2="200" stroke="currentColor" stroke-width="2"/>
  <!-- 표면 라벨 -->
  <text x="370" y="204" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">표면</text>
  <!-- 표면 위의 점 -->
  <circle cx="210" cy="200" r="4" fill="currentColor"/>
  <!-- N 벡터 (수직 위로) -->
  <line x1="210" y1="196" x2="210" y2="62" stroke="currentColor" stroke-width="1.5" marker-end="url(#arrowSpec)"/>
  <text x="220" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">N</text>
  <text x="234" y="58" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(법선)</text>
  <!-- L 벡터 (왼쪽 위 대각선, 약 45도) -->
  <line x1="206" y1="196" x2="114" y2="104" stroke="currentColor" stroke-width="1.5" marker-end="url(#arrowSpec)"/>
  <text x="90" y="96" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">L</text>
  <text x="76" y="110" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(빛 방향)</text>
  <!-- R 벡터 (오른쪽 위 대각선, L과 N 기준 대칭) -->
  <line x1="214" y1="196" x2="306" y2="104" stroke="currentColor" stroke-width="1.5" marker-end="url(#arrowSpec)"/>
  <text x="312" y="96" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">R</text>
  <text x="312" y="110" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(반사 벡터)</text>
  <!-- V 벡터 (R 근처, 약간 더 바깥쪽) -->
  <line x1="214" y1="196" x2="330" y2="126" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" marker-end="url(#arrowSpec)"/>
  <text x="336" y="122" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">V</text>
  <text x="336" y="136" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(시야 벡터)</text>
  <!-- R과 V 사이 각도 호 (R·V 관계 시각화) -->
  <path d="M 280,130 A 40,40 0 0,1 296,118" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <!-- L-N 대칭 표시 (각도 호) -->
  <path d="M 174,162 A 50,50 0 0,1 210,152" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.35"/>
  <path d="M 210,152 A 50,50 0 0,1 246,162" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.35"/>
  <text x="188" y="157" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">θ</text>
  <text x="228" y="157" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">θ</text>
</svg>
</div>

$$
\mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}
$$

$(\mathbf{N} \cdot \mathbf{L})\mathbf{N}$은 L을 법선 방향으로 투영한 벡터로, L과 R의 중간 지점에 해당합니다. L에서 이 중간 지점을 지나 같은 거리만큼 더 나아간 것이 반사 벡터 R이며, 다이어그램에서 L과 R이 법선 양쪽에 같은 각도 θ로 놓이는 것이 이 대칭입니다.

<br>

R을 구한 뒤, 앞 섹션의 Specular 수식에서 기하학적 항만 분리하면 다음과 같습니다.

$$
\max(\mathbf{R} \cdot \mathbf{V},\ 0)^{n}
$$

$\mathbf{R} \cdot \mathbf{V}$는 두 단위 벡터 사이 각도의 코사인이므로, V가 R과 같은 방향이면 1, 직교하면 0입니다.

값이 1에 가까울수록 관찰자가 반사 경로 위에 있어 밝은 하이라이트가 보이고, 0에 가까울수록 반사 경로에서 벗어나 하이라이트가 사라집니다.

### 광택 지수 (Shininess Exponent)

지수 $n$이 하이라이트의 크기를 바꾸는 원리는 거듭제곱의 성질에 있습니다.

$\mathbf{R} \cdot \mathbf{V}$는 0 ~ 1 범위의 값이므로, $n$제곱하면 1에 가까운 값은 거의 그대로 유지되지만, 1에서 조금이라도 떨어진 값은 급격히 0으로 수렴합니다.

예를 들어, $0.9^{10} \approx 0.35$이지만 $0.9^{256} \approx 2 \times 10^{-12}$(거의 0)입니다.

$n$이 크면 반사 방향에서 조금만 벗어나도 기여가 거의 0이 되어 하이라이트가 좁고 날카로워지고, $n$이 작으면 넓은 범위가 유의미한 값을 유지하여 하이라이트가 퍼집니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="20" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">광택 지수에 따른 하이라이트 크기</text>
  <!-- n = 10 -->
  <rect x="10" y="35" width="160" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">n = 10</text>
  <circle cx="90" cy="100" r="35" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <text x="90" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">넓고 부드러운 하이라이트</text>
  <text x="90" y="160" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(고무, 나무 등)</text>
  <!-- n = 50 -->
  <rect x="180" y="35" width="160" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">n = 50</text>
  <circle cx="260" cy="100" r="22" fill="currentColor" fill-opacity="0.3" stroke="none"/>
  <text x="260" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">중간 크기의 하이라이트</text>
  <text x="260" y="160" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(플라스틱 등)</text>
  <!-- n = 256 -->
  <rect x="350" y="35" width="160" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">n = 256</text>
  <circle cx="430" cy="100" r="10" fill="currentColor" fill-opacity="0.6" stroke="none"/>
  <text x="430" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">작고 날카로운 하이라이트</text>
  <text x="430" y="160" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(금속, 유리 등)</text>
</svg>
</div>

### Phong 모델의 한계

Phong 모델은 정반사를 표현할 수 있어 Lambert보다 현실적이지만, 계산 비용, 에너지 보존, 시각적 불연속이라는 세 가지 한계를 가집니다.

<br>

첫째, 반사 벡터 R을 매 픽셀마다 계산하는 비용입니다. R = 2(N·L)N - L은 내적, 스칼라-벡터 곱셈, 벡터 뺄셈을 조합한 연산이며, 프래그먼트 셰이더에서 화면의 모든 픽셀마다 이 연산을 반복해야 하므로 해상도가 높아질수록 연산 부담이 커집니다.

<br>

둘째, 에너지 보존이 보장되지 않습니다. 물리적으로 표면에 도달한 빛 에너지는 난반사와 정반사로 나뉘어야 하고, 둘의 합은 입사 에너지를 초과할 수 없습니다. 그러나 Phong 모델은 Diffuse와 Specular를 각각 독립된 계수로 계산한 뒤 합산할 뿐, 두 항의 비율을 강제하지 않으므로, 계수 조합에 따라 출력 에너지가 입력 에너지를 초과할 수 있습니다.

<br>

셋째, 하이라이트 경계에서 시각적 불연속이 발생할 수 있습니다. Phong의 정반사 항 max(R·V, 0)^n에서, R과 V 사이의 각도가 90도를 넘으면 R·V가 음수가 되고 max 함수가 이를 0으로 잘라냅니다. 양수에서 0으로의 전환이 즉각적이므로, 하이라이트 가장자리가 부드럽게 감쇠하지 않고 날카롭게 끊깁니다. 광택 지수 n이 낮아 하이라이트가 넓은 재질이나, 시야 벡터가 표면과 거의 수평에 가까운 그레이징 앵글(Grazing Angle) 상황에서 이 불연속이 눈에 띄기 쉽습니다.

---

## Blinn-Phong 모델

### Half-Vector를 이용한 근사

Phong 모델의 반사 벡터 R 계산 비용과 시각적 불연속 문제를 개선한 것이 Blinn-Phong 모델입니다.

Jim Blinn이 1977년에 제안한 이 변형은, 반사 벡터 R 대신 **반법선 벡터(Half-Vector, H)**를 사용하여 정반사를 계산합니다.

<br>

**Blinn-Phong 모델의 수식**

$$
\mathbf{H} = \text{normalize}(\mathbf{L} + \mathbf{V})
$$

$$
\text{Specular} = (\mathbf{N} \cdot \mathbf{H})^{n} \times C_{\text{light}} \times C_{\text{spec}}
$$

- $\mathbf{H}$: 반법선 벡터 (광원 방향 $\mathbf{L}$과 시야 방향 $\mathbf{V}$의 중간 방향)
- $\mathbf{N} \cdot \mathbf{H}$: 법선과 반법선 벡터의 내적
- $n$: 광택 지수 (같은 $n$ 값이라도 Blinn-Phong 쪽 하이라이트가 더 넓으므로, Phong과 비슷한 크기의 하이라이트를 얻으려면 $n$을 약 2~4배로 높여야 함)

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="420" height="260" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="210" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Blinn-Phong의 Half-Vector</text>
  <!-- 화살촉 마커 정의 -->
  <defs>
    <marker id="arrowBP" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
      <polygon points="0,0 8,3 0,6" fill="currentColor"/>
    </marker>
  </defs>
  <!-- 표면 -->
  <line x1="60" y1="200" x2="360" y2="200" stroke="currentColor" stroke-width="2"/>
  <text x="370" y="204" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6" text-anchor="start">표면</text>
  <!-- 표면 위 점 -->
  <circle cx="210" cy="200" r="4" fill="currentColor"/>
  <!-- N 벡터 (법선, 수직 위) -->
  <line x1="210" y1="196" x2="210" y2="62" stroke="currentColor" stroke-width="1.8" marker-end="url(#arrowBP)"/>
  <text x="210" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">N</text>
  <text x="210" y="40" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(법선)</text>
  <!-- L 벡터 (빛 방향, 왼쪽 대각선 위) -->
  <line x1="210" y1="196" x2="112" y2="80" stroke="currentColor" stroke-width="1.8" marker-end="url(#arrowBP)"/>
  <text x="100" y="72" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">L</text>
  <text x="88" y="86" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(빛 방향)</text>
  <!-- H 벡터 (반법선, L과 V의 중간 방향 — 파선으로 강조) -->
  <line x1="210" y1="196" x2="262" y2="62" stroke="currentColor" stroke-width="1.8" stroke-dasharray="6,3" marker-end="url(#arrowBP)"/>
  <text x="274" y="52" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">H</text>
  <text x="274" y="42" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(반법선)</text>
  <!-- V 벡터 (시야, 오른쪽 대각선 위) -->
  <line x1="210" y1="196" x2="320" y2="88" stroke="currentColor" stroke-width="1.8" marker-end="url(#arrowBP)"/>
  <text x="334" y="82" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">V</text>
  <text x="346" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(시야)</text>
  <!-- 보조 설명 -->
  <text x="210" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">H = normalize(L + V) — L과 V의 정확한 중간 방향</text>
</svg>
</div>

반법선 벡터 H에는 물리적 의미가 있습니다. 빛이 정확히 관찰자 방향으로 정반사되려면, 표면의 법선이 L과 V의 중간 방향, 즉 H와 일치해야 합니다. N·H가 1에 가까우면 법선이 이 조건을 만족하므로 정반사가 관찰자에게 도달하여 밝은 하이라이트가 나타납니다.

<br>

Blinn-Phong은 Phong의 시각적 불연속 문제도 완화합니다.

Phong에서는 반사 벡터 R과 시야 벡터 V 사이의 각도가 90도를 넘으면 R·V가 음수가 되고, max 함수가 이 값을 0으로 잘라내기 때문에 하이라이트가 날카롭게 끊기는 경계가 생겼습니다.

Blinn-Phong의 N·H에서는 이 문제가 줄어듭니다. 법선 N과 반법선 H 사이의 각도가 90도를 넘으려면 관찰자나 광원이 표면 뒤쪽에 있어야 하는데, 일반적인 조명·시야 조건에서 이런 상황은 드물기 때문에 0으로 클램핑되는 영역 자체가 작아지고 하이라이트 경계가 부드럽게 감쇠합니다.

### Phong과의 비교

Blinn-Phong이 Phong보다 선호되는 이유는 계산 효율과 시각적 안정성 두 가지입니다.

**Phong vs Blinn-Phong**

| 항목 | Phong | Blinn-Phong |
|---|---|---|
| 정반사 계산 | $\mathbf{R} \cdot \mathbf{V}$ | $\mathbf{N} \cdot \mathbf{H}$ |
| 반사 벡터 계산 | $\mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}$ (필요) | 불필요 |
| Half-Vector 계산 | 불필요 | $\mathbf{H} = \text{normalize}(\mathbf{L} + \mathbf{V})$ (필요) |
| 계산 비용 | 약간 높음 | 약간 효율적 (Directional Light에서 $\mathbf{H}$ 재사용) |
| 하이라이트 형태 | 원형에 가까움 | 약간 넓고 부드러움 |
| 에너지 보존 | 보장하지 않음 | 보장하지 않음 |

표의 "계산 비용" 차이는 Directional Light에서 두드러집니다.

Directional Light는 광원 방향 L이 모든 픽셀에서 동일하므로, H = normalize(L + V)에서 L은 상수이고 V만 변수입니다.

직교 투영(Orthographic Projection)에서는 시선이 모두 평행하여 V도 동일하므로, H 자체가 상수가 되어 한 번만 계산하면 됩니다.

원근 투영(Perspective Projection)에서는 카메라 위치에서 각 픽셀의 표면 위치까지의 방향이 다르므로 V가 픽셀마다 달라지지만, 오브젝트가 카메라에서 멀어질수록 시선 방향의 변화량이 줄어들어 H를 근사적으로 재사용할 수 있습니다.

반면 Phong의 반사 벡터 R = 2(N·L)N - L은 표면의 법선 N이 곡률에 따라 픽셀마다 다르므로, L이 일정하더라도 매 픽셀마다 새로 계산해야 합니다.

같은 Directional Light 조건에서 Blinn-Phong은 H를 재사용하여 픽셀당 정반사 연산을 줄일 수 있지만, Phong은 줄일 수 없습니다.

이런 계산 효율 덕분에, OpenGL과 DirectX의 **고정 파이프라인(Fixed-Function Pipeline)** — 셰이더 코드를 직접 작성할 수 없고 하드웨어에 내장된 조명 모델만 사용하던 시절 — 에서 Blinn-Phong이 기본 셰이딩 모델로 채택되었습니다.

Unity의 Built-in 파이프라인에서도 Legacy Shader들이 Blinn-Phong 기반입니다.

### 전통적 모델의 공통 한계

Lambert, Phong, Blinn-Phong은 모두 **경험적(Empirical)** 모델입니다.

물리 법칙을 유도하여 수식을 만든 것이 아니라, 시각적으로 그럴듯한 결과를 목표로 수식을 직접 설계했으므로, 공통된 물리적 한계를 가집니다.

<br>

첫째, 에너지 보존이 구조적으로 보장되지 않습니다. Phong과 Blinn-Phong은 Diffuse 항과 Specular 항을 독립된 계수로 계산한 뒤 합산할 뿐이므로, 계수 조합에 따라 반사 에너지가 입사 에너지를 초과할 수 있습니다. Lambert의 BRDF 형태($C_{\text{albedo}} / \pi$)는 에너지 보존을 만족하지만, 앞서 다룬 것처럼 실제 셰이더에서 π 나누기를 생략하는 경우가 많아, 그 경우에는 에너지 총량을 제한하는 장치가 없습니다.

<br>

둘째, 프레넬 효과가 빠져 있습니다. 시야 각도에 따라 반사율이 달라지는 현상을 수식에 포함하지 않으므로, 그레이징 앵글에서 반사가 강해지는 실제 표면의 모습을 재현할 수 없습니다.

<br>

셋째, 하이라이트의 에너지 재분배가 없습니다. 광택 지수 n을 낮추면 하이라이트가 넓어지지만 밝기는 그대로 유지됩니다. 실제 표면에서는 하이라이트가 넓어질수록 같은 에너지가 더 넓은 면적에 분산되어 단위 면적당 밝기가 줄어드는데, 이 재분배가 일어나지 않아 넓은 하이라이트가 비현실적으로 밝게 표현됩니다.

<br>

이런 한계들을 해결하기 위해, 에너지 보존·프레넬 효과·미세면 분포를 수식에 직접 반영하는 새로운 접근이 등장했습니다.

---

## PBR (Physically Based Rendering)

### PBR의 핵심 원칙

PBR은 물리 법칙에 기반하여 표면의 빛 반사를 계산하는 렌더링 방식입니다. [색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 에너지 보존, 프레넬 효과, 그리고 BRDF 개념이 PBR의 수학적 기반이며, PBR의 핵심 원칙은 세 가지로, 각각 위에서 언급한 전통적 모델의 한계에 대응합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 전체 제목 -->
  <text x="210" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">PBR의 세 가지 핵심 원칙</text>

  <!-- 카드 1: 에너지 보존 -->
  <rect x="20" y="40" width="380" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="62" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) 에너지 보존</text>
  <text x="185" y="62" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Energy Conservation</text>
  <text x="40" y="84" font-family="sans-serif" font-size="11" fill="currentColor">반사된 빛의 총 에너지 ≤ 입사 에너지</text>
  <text x="40" y="104" font-family="sans-serif" font-size="11" fill="currentColor">Diffuse + Specular ≤ 1.0</text>
  <text x="40" y="124" font-family="sans-serif" font-size="11" fill="currentColor">Specular가 증가하면 Diffuse는 감소</text>

  <!-- 카드 2: 프레넬 효과 -->
  <rect x="20" y="158" width="380" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="180" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) 프레넬 효과</text>
  <text x="163" y="180" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Fresnel Effect</text>
  <text x="40" y="202" font-family="sans-serif" font-size="11" fill="currentColor">모든 표면에서 시야 각도에 따라 반사율이 변함</text>
  <text x="40" y="222" font-family="sans-serif" font-size="11" fill="currentColor">가장자리(Grazing Angle)에서 반사가 강해짐</text>

  <!-- 카드 3: 미세면 이론 -->
  <rect x="20" y="266" width="380" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="288" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) 미세면 이론</text>
  <text x="160" y="288" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Microfacet Theory</text>
  <text x="40" y="310" font-family="sans-serif" font-size="11" fill="currentColor">표면을 미세한 거울 면의 집합으로 모델링</text>
  <text x="40" y="330" font-family="sans-serif" font-size="11" fill="currentColor">러프니스가 미세면의 방향 분포를 결정</text>
</svg>
</div>

### 미세면 이론 (Microfacet Theory)

PBR의 정반사 계산은 미세면 이론에 기반합니다.

매끄러워 보이는 표면도 미시적 스케일에서 보면 수많은 **미세면(Microfacet)**의 집합이며, 각 미세면은 작은 거울처럼 동작합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <rect x="0" y="0" width="580" height="520" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor" text-anchor="middle">미세면 이론 (Microfacet Theory)</text>

  <!-- 상단: 거시적 → 미시적 관계 -->
  <text x="40" y="58" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">거시적 표면</text>
  <text x="210" y="58" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(매끄러워 보임)</text>
  <line x1="40" y1="70" x2="350" y2="70" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="195" y1="68" x2="195" y2="30" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.5"/>
  <polygon points="195,28 191,36 199,36" fill="currentColor" opacity="0.5"/>
  <text x="203" y="36" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold" opacity="0.6">N</text>

  <text x="380" y="62" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">확대</text>
  <line x1="355" y1="70" x2="398" y2="96" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" opacity="0.4"/>
  <line x1="355" y1="70" x2="398" y2="70" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2" opacity="0.4"/>

  <text x="400" y="58" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">미시적 구조</text>
  <text x="400" y="72" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(미세면들의 집합)</text>
  <polyline points="400,100 415,82 430,100 440,86 455,100 462,90 478,100 490,84 505,100 515,88 530,100 540,86 555,100" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>

  <line x1="415" y1="82" x2="409" y2="66" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <polygon points="409,64 406,72 412,72" fill="currentColor" opacity="0.7"/>
  <line x1="440" y1="86" x2="437" y2="70" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <polygon points="437,68 434,76 440,76" fill="currentColor" opacity="0.7"/>
  <line x1="462" y1="90" x2="456" y2="74" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <polygon points="456,72 453,80 459,80" fill="currentColor" opacity="0.7"/>
  <line x1="490" y1="84" x2="484" y2="68" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <polygon points="484,66 481,74 487,74" fill="currentColor" opacity="0.7"/>
  <line x1="515" y1="88" x2="515" y2="72" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <polygon points="515,70 512,78 518,78" fill="currentColor" opacity="0.7"/>
  <line x1="540" y1="86" x2="536" y2="70" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <polygon points="536,68 533,76 539,76" fill="currentColor" opacity="0.7"/>
  <text x="418" y="60" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="441" y="64" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="486" y="62" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>

  <text x="290" y="128" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">각 미세면은 자신만의 법선(미세면 법선, m)을 가짐</text>
  <text x="290" y="143" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">거시적 법선 N과 미세면 법선 m은 다를 수 있음</text>

  <line x1="30" y1="158" x2="550" y2="158" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <!-- 하단 좌측: 러프니스 낮음 -->
  <rect x="20" y="168" width="260" height="340" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <text x="150" y="192" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor" text-anchor="middle">러프니스 낮음 (매끄러움)</text>

  <line x1="45" y1="280" x2="255" y2="280" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
  <line x1="70" y1="278" x2="69" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="69,237 66,245 72,245" fill="currentColor"/>
  <line x1="100" y1="278" x2="100" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="100,237 97,245 103,245" fill="currentColor"/>
  <line x1="130" y1="278" x2="131" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="131,237 128,245 134,245" fill="currentColor"/>
  <line x1="160" y1="278" x2="160" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="160,237 157,245 163,245" fill="currentColor"/>
  <line x1="190" y1="278" x2="189" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,237 186,245 192,245" fill="currentColor"/>
  <line x1="220" y1="278" x2="221" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="221,237 218,245 224,245" fill="currentColor"/>

  <line x1="150" y1="278" x2="150" y2="218" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.4"/>
  <polygon points="150,215 147,223 153,223" fill="currentColor" opacity="0.4"/>
  <text x="157" y="222" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold" opacity="0.5">N</text>
  <text x="72" y="234" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="162" y="234" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="224" y="234" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>

  <text x="150" y="308" font-family="sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle" opacity="0.6">미세면 법선이 거시적 법선과</text>
  <text x="150" y="322" font-family="sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle" opacity="0.6">거의 같은 방향</text>

  <text x="150" y="355" font-family="sans-serif" font-size="9" fill="currentColor" text-anchor="middle" opacity="0.5">반사 분포:</text>
  <ellipse cx="150" cy="385" rx="18" ry="40" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1" opacity="0.6"/>

  <text x="150" y="448" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">정반사가 한 방향에 집중</text>
  <text x="150" y="466" font-family="sans-serif" font-size="10.5" fill="currentColor" text-anchor="middle" font-weight="bold">날카로운 하이라이트</text>

  <!-- 하단 우측: 러프니스 높음 -->
  <rect x="300" y="168" width="260" height="340" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <text x="430" y="192" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor" text-anchor="middle">러프니스 높음 (거침)</text>

  <polyline points="325,280 340,262 355,282 365,258 380,280 390,266 405,284 418,256 435,280 448,264 460,282 472,260 488,280 500,268 515,280 528,260 540,280" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>

  <line x1="340" y1="262" x2="326" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="325,238 323,246 329,245" fill="currentColor"/>
  <line x1="365" y1="258" x2="362" y2="228" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="362,225 359,233 365,233" fill="currentColor"/>
  <line x1="390" y1="266" x2="400" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="401,238 397,244 403,246" fill="currentColor"/>
  <line x1="418" y1="256" x2="404" y2="230" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="403,228 401,236 407,235" fill="currentColor"/>
  <line x1="448" y1="264" x2="458" y2="236" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="459,234 455,240 461,242" fill="currentColor"/>
  <line x1="472" y1="260" x2="464" y2="232" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="463,230 461,238 467,237" fill="currentColor"/>
  <line x1="500" y1="268" x2="514" y2="244" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="515,242 511,248 516,250" fill="currentColor"/>
  <line x1="528" y1="260" x2="528" y2="232" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="528,229 525,237 531,237" fill="currentColor"/>

  <line x1="430" y1="270" x2="430" y2="218" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.4"/>
  <polygon points="430,215 427,223 433,223" fill="currentColor" opacity="0.4"/>
  <text x="437" y="222" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold" opacity="0.5">N</text>
  <text x="328" y="234" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="402" y="234" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="460" y="230" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>
  <text x="516" y="240" font-family="sans-serif" font-size="8" fill="currentColor" font-weight="bold" opacity="0.7">m</text>

  <text x="430" y="308" font-family="sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle" opacity="0.6">미세면 법선이 여러 방향으로 분산</text>

  <text x="430" y="340" font-family="sans-serif" font-size="9" fill="currentColor" text-anchor="middle" opacity="0.5">반사 분포:</text>
  <ellipse cx="430" cy="378" rx="65" ry="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" opacity="0.6"/>

  <text x="430" y="448" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">정반사가 넓게 퍼짐</text>
  <text x="430" y="466" font-family="sans-serif" font-size="10.5" fill="currentColor" text-anchor="middle" font-weight="bold">넓고 어두운 하이라이트</text>
</svg>
</div>

러프니스(Roughness)는 미세면 법선의 방향 분포를 조절하는 파라미터입니다.

러프니스가 0에 가까우면 모든 미세면이 같은 방향을 가리키고(완전 거울), 1에 가까우면 미세면이 무작위 방향을 가리킵니다(완전 난반사).

### Cook-Torrance BRDF

PBR의 정반사 성분은 **Cook-Torrance BRDF**로 계산됩니다.

Cook-Torrance BRDF는 "얼마나 많은 미세면이 반사에 기여하는가(D)", "각 미세면이 얼마나 반사하는가(F)", "반사광이 인접 미세면에 막히지 않는가(G)"를 분자에 곱하고, 분모에 정규화 인자를 두어 거시적 표면 단위로 변환하는 분수 형태입니다.

<br>

**Cook-Torrance Specular BRDF**

$$
f_{\text{spec}} = \frac{D(\mathbf{h}) \cdot F(\mathbf{v}, \mathbf{h}) \cdot G(\mathbf{l}, \mathbf{v}, \mathbf{h})}{4(\mathbf{N} \cdot \mathbf{L})(\mathbf{N} \cdot \mathbf{V})}
$$

- $D$: 법선 분포 함수 (Normal Distribution Function)
- $F$: 프레넬 함수 (Fresnel Function)
- $G$: 기하학적 감쇠 함수 (Geometry Function)
- $\mathbf{h}$: 반법선 벡터 $\mathbf{H}$ ($= \text{normalize}(\mathbf{L} + \mathbf{V})$)

분자의 D, F, G는 각각 다른 물리적 현상을 모델링하며, 아래에서 하나씩 살펴봅니다. 분모의 정규화 인자는 세 함수를 모두 다룬 뒤에 설명합니다.

<br>

**D (법선 분포 함수, NDF)**: 전체 미세면 중에서 법선 m이 반법선 벡터 H와 같은 방향을 가리키는 미세면의 비율을 나타냅니다.

거울 반사는 입사각과 반사각이 같을 때만 성립하고, H는 입사 방향 L과 시야 방향 V의 정확한 중간 방향이므로, 법선이 H인 미세면 위에서만 L로 들어온 빛이 V 방향으로 정반사됩니다. D는 이 미세면의 비율을 나타내므로, 하이라이트의 형태와 밝기를 결정합니다.

러프니스가 낮으면 D가 좁고 높은 피크를 형성하여 날카로운 하이라이트가 나타나고, 러프니스가 높으면 D가 넓고 낮은 분포를 형성하여 부드러운 하이라이트가 나타납니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="520" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 제목 -->
  <text x="260" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">법선 분포 함수 D의 형태</text>

  <!-- === 왼쪽: 러프니스 낮음 === -->
  <text x="130" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">러프니스 낮음</text>

  <!-- Y축 -->
  <line x1="130" y1="60" x2="130" y2="155" stroke="currentColor" stroke-width="1.2"/>
  <!-- Y축 화살표 -->
  <polygon points="130,58 126,66 134,66" fill="currentColor"/>

  <!-- X축 -->
  <line x1="50" y1="155" x2="220" y2="155" stroke="currentColor" stroke-width="1.2"/>

  <!-- 좁고 높은 피크 곡선 -->
  <path d="M 60,155 C 80,155 110,154 120,100 Q 125,68 130,62 Q 135,68 140,100 C 150,154 180,155 200,155"
        stroke="currentColor" stroke-width="2" fill="none"/>
  <!-- 곡선 아래 채움 -->
  <path d="M 60,155 C 80,155 110,154 120,100 Q 125,68 130,62 Q 135,68 140,100 C 150,154 180,155 200,155 Z"
        fill="currentColor" fill-opacity="0.1"/>

  <!-- H 방향 라벨 -->
  <text x="130" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">H 방향</text>

  <!-- 설명 텍스트 -->
  <text x="130" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">좁고 높은 피크</text>
  <text x="130" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">= 날카로운 하이라이트</text>

  <!-- === 오른쪽: 러프니스 높음 === -->
  <text x="390" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">러프니스 높음</text>

  <!-- Y축 -->
  <line x1="390" y1="60" x2="390" y2="155" stroke="currentColor" stroke-width="1.2"/>
  <!-- Y축 화살표 -->
  <polygon points="390,58 386,66 394,66" fill="currentColor"/>

  <!-- X축 -->
  <line x1="290" y1="155" x2="490" y2="155" stroke="currentColor" stroke-width="1.2"/>

  <!-- 넓고 낮은 분포 곡선 -->
  <path d="M 300,155 C 315,154 335,150 350,140 Q 370,126 390,120 Q 410,126 430,140 C 445,150 465,154 480,155"
        stroke="currentColor" stroke-width="2" fill="none"/>
  <!-- 곡선 아래 채움 -->
  <path d="M 300,155 C 315,154 335,150 350,140 Q 370,126 390,120 Q 410,126 430,140 C 445,150 465,154 480,155 Z"
        fill="currentColor" fill-opacity="0.1"/>

  <!-- H 방향 라벨 -->
  <text x="390" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">H 방향</text>

  <!-- 설명 텍스트 -->
  <text x="390" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">넓고 낮은 분포</text>
  <text x="390" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">= 부드러운 하이라이트</text>
</svg>
</div>

가장 널리 사용되는 NDF는 **GGX (Trowbridge-Reitz)** 분포입니다. 현실의 하이라이트는 중심부의 밝은 핵 주변으로 빛이 넓게 번져 나가는데, 이전에 쓰이던 Beckmann 분포는 중심에서 벗어나면 값이 급격히 0에 가까워져서 이 번짐을 표현하지 못했습니다. GGX는 분포의 꼬리(tail)가 길어서 중심에서 멀어져도 값이 천천히 감소하므로, 하이라이트 주변의 부드러운 번짐까지 재현합니다. Unity의 URP Lit Shader도 GGX를 사용합니다.

<br>

**F (프레넬 함수)**: [색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 프레넬 효과, 즉 시야 각도에 따라 반사율이 달라지는 현상을 수식으로 계산합니다.

원래의 프레넬 방정식은 편광별 삼각함수와 제곱근 연산이 필요하므로, 실시간 렌더링에서는 내적 하나와 거듭제곱 하나로 충분히 정확한 결과를 내는 **슐릭 근사(Schlick's Approximation)**를 사용합니다.

**슐릭의 프레넬 근사 (Schlick's Approximation)**

$$
F_{\text{Schlick}} = F_0 + (1 - F_0)(1 - \cos\theta)^5
$$

- $F_0$: 정면 입사($\theta = 0°$) 시의 반사율
  - 비금속(유전체): 약 $0.04$ (4%)
  - 금속: 채널별 $0.2 \sim 1.0$ (금속 종류와 파장에 따라 다름)
- $\cos\theta$: 시야 방향과 반법선 벡터의 내적 ($= \mathbf{V} \cdot \mathbf{H}$)

$\theta = 0°$ (정면)이면 $(1 - \cos\theta)^5 = 0$이므로 $F = F_0$, 즉 기본 반사율만 남습니다. $\theta = 90°$ (수평)이면 $(1 - \cos\theta)^5 = 1$이므로 $F \approx 1.0$, 즉 거의 전반사가 됩니다.

$F_0$ 값은 재질의 고유한 성질입니다. 비금속은 $F_0$가 대부분 0.04 근처인 단일 값이지만, 금속은 RGB 채널별로 다른 $F_0$ 값을 가집니다. 금은 (1.0, 0.71, 0.29), 은은 (0.95, 0.93, 0.88), 구리는 (0.95, 0.64, 0.54)입니다.

금속의 $F_0$가 채널별로 다른 이유는, 금속 내부의 자유 전자가 파장에 따라 다른 세기로 빛을 반사하기 때문입니다. 금이 노란색으로 보이는 것은 적색·녹색 파장의 반사율이 청색보다 높기 때문이며, 금의 $F_0$에서 R > G > B 순서가 이를 반영합니다.

<br>

**G (기하학적 감쇠 함수)**: 미세면이 빛(L)과 관찰자(V)에 동시에 노출되는 비율을 반영하여, 스펙큘러 기여를 감쇠시킵니다.

D가 관찰자 방향으로 정반사하는 미세면의 비율을, F가 각 미세면의 반사율을 결정한다면, G는 그 반사광이 인접 미세면에 막히지 않고 관찰자에게 도달하는 비율을 나타냅니다.

러프니스가 높아 요철이 심하면 두 종류의 차폐가 발생합니다. 입사광이 목표 미세면에 닿기 전에 인접 미세면에 가려지는 그림자 효과(Shadowing)와, 미세면에서 반사된 빛이 인접 미세면에 막혀 관찰자에게 도달하지 못하는 마스킹 효과(Masking)입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="520" height="400" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 제목 -->
  <text x="260" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기하학적 감쇠</text>

  <!-- ===== 좌측: 그림자 효과 (Shadowing) ===== -->
  <text x="135" y="55" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">그림자 효과 (Shadowing)</text>
  <text x="135" y="72" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">빛이 미세면에 도달하기 전에 인접 미세면에 의해 차단</text>

  <!-- 미세면 지그재그 (좌측) -->
  <polyline points="20,200 55,140 90,200 125,120 160,200 195,150 230,200 250,170" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>

  <!-- 차단 영역 (그림자) -->
  <polygon points="125,120 108,160 125,200 160,200" fill="currentColor" fill-opacity="0.1" stroke="none"/>
  <text x="132" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">그림자</text>

  <!-- 입사광 화살표 — 산봉우리에 막힘 -->
  <line x1="60" y1="88" x2="118" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="118,128 108,120 112,131" fill="currentColor"/>
  <!-- 빛 라벨 -->
  <text x="52" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">L</text>

  <!-- 차단 표시 (X) -->
  <line x1="115" y1="124" x2="127" y2="136" stroke="currentColor" stroke-width="2" opacity="0.7"/>
  <line x1="127" y1="124" x2="115" y2="136" stroke="currentColor" stroke-width="2" opacity="0.7"/>

  <!-- 미세면 기저선 (좌측) -->
  <line x1="15" y1="200" x2="255" y2="200" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- ===== 우측: 마스킹 효과 (Masking) ===== -->
  <text x="390" y="55" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">마스킹 효과 (Masking)</text>
  <text x="390" y="72" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">반사된 빛이 인접 미세면에 의해 차단</text>

  <!-- 미세면 지그재그 (우측) -->
  <polyline points="270,200 305,150 340,200 375,120 410,200 445,140 480,200 505,170" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>

  <!-- 차단 영역 (마스킹) -->
  <polygon points="445,140 410,200 445,200" fill="currentColor" fill-opacity="0.1" stroke="none"/>
  <text x="438" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">차단</text>

  <!-- 반사면에서 반사되는 빛 -->
  <line x1="375" y1="120" x2="395" y2="96" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="400" y="92" text-anchor="start" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">V</text>
  <text x="375" y="215" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">반사면</text>

  <!-- 반사광 화살표 — 인접 산봉우리에 막힘 -->
  <line x1="395" y1="160" x2="438" y2="146" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="438,146 427,143 431,153" fill="currentColor"/>

  <!-- 차단 표시 (X) -->
  <line x1="434" y1="140" x2="446" y2="152" stroke="currentColor" stroke-width="2" opacity="0.7"/>
  <line x1="446" y1="140" x2="434" y2="152" stroke="currentColor" stroke-width="2" opacity="0.7"/>

  <!-- 반사광 차단 라벨 -->
  <text x="460" y="130" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">반사광 차단</text>

  <!-- 미세면 기저선 (우측) -->
  <line x1="265" y1="200" x2="510" y2="200" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- 구분선 -->
  <line x1="260" y1="85" x2="260" y2="220" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- ===== 하단 방향 범례 ===== -->
  <text x="260" y="240" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">L: 표면 → 광원 방향 · V: 표면 → 관찰자 방향</text>

  <!-- ===== 하단 결론 영역 ===== -->
  <rect x="40" y="260" width="440" height="110" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.5"/>

  <text x="260" y="288" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">G는 Shadowing과 Masking을 모두 고려합니다</text>
  <text x="260" y="318" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">러프니스 ↑ + 비스듬한 각도 → 차단 ↑ → G 값 ↓</text>
  <text x="260" y="348" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">G ∈ [0, 1]: 스펙큘러 항에 곱해져 반사 에너지를 감쇠</text>
</svg>
</div>

G 값은 0(완전 차폐)에서 1(차폐 없음) 사이입니다. 비스듬한 시야 각도에서는 미세면 사이의 차폐가 심해져 G가 크게 낮아지며, 가장자리의 반사광을 감쇠시킵니다. 이 감쇠가 없으면 거친 표면의 가장자리가 비물리적으로 밝게 빛납니다.

<br>

분모의 4 × (N·L) × (N·V)는 정규화 인자입니다. D·F·G는 개별 미세면의 반사를 기준으로 계산되므로, 거시적 표면의 단위 면적당 값으로 변환해야 합니다. N·L은 Lambert 모델에서 다룬 코사인 법칙 -- 빛이 표면에 비스듬히 닿을수록 단위 면적이 받는 광량이 줄어드는 효과 -- 을 반영하고, N·V는 같은 원리를 관찰자 방향에 적용합니다. 4는 미세면 법선과 반법선 벡터 사이의 기하학적 변환(야코비안)에서 유도되는 상수입니다.

### PBR의 최종 셰이딩

PBR의 최종 색상은 Diffuse와 Specular를 더한 값입니다.

다만, 입사 에너지 중 프레넬 반사로 Specular에 쓰인 비율 $F$를 Diffuse에서 빼야 에너지 보존이 성립합니다.

**PBR 최종 셰이딩**

$$
\text{Color} = (1 - F) \cdot f_{\text{diffuse}} + f_{\text{specular}}
$$

- $(1 - F)$: 프레넬 반사에 사용되지 않은 에너지 비율 — 이 비율만큼만 Diffuse에 할당
- $f_{\text{diffuse}}$: Lambert Diffuse ($= C_{\text{albedo}} / \pi$). $\pi$는 앞에서 다룬 반구 적분의 정규화 상수
- $f_{\text{specular}}$: Cook-Torrance Specular ($= D \cdot F \cdot G \;/\; 4(N \cdot L)(N \cdot V)$)

$(1 - F)$ 가중과 각 함수의 정규화가 결합되어, 파라미터를 어떻게 조합하더라도 물리적으로 일관된 결과가 나옵니다.

러프니스를 올리면 NDF(D)의 분포가 넓어지면서 피크가 낮아져, 하이라이트가 퍼지는 만큼 단위 면적당 밝기가 줄어듭니다.

메탈릭을 올리면 Metallic 워크플로우가 Albedo를 F0로 전환하는 비율을 높이고 Diffuse 계수를 줄여, Metallic = 1에서는 Specular 색이 Albedo와 같아지면서 Diffuse가 완전히 사라집니다.

---

## Metallic 워크플로우 vs Specular 워크플로우

Cook-Torrance BRDF는 F0, Roughness, Albedo 등을 입력으로 사용하며, 아티스트가 이 값을 머티리얼에 지정하는 방식에는 Metallic 워크플로우와 Specular 워크플로우 두 가지가 있습니다. BRDF 자체는 동일하고, 파라미터를 조합하는 방식만 다릅니다.

### Metallic 워크플로우

Metallic 워크플로우는 세 개의 주요 파라미터로 구성됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- 외곽 -->
  <rect x="1" y="1" width="498" height="428" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="26" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Metallic 워크플로우</text>

  <!-- (1) Albedo 카드 -->
  <rect x="20" y="42" width="460" height="108" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
  <text x="36" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) Albedo (Base Color)</text>
  <text x="52" y="80" font-family="sans-serif" font-size="10" fill="currentColor">RGB 색상 맵</text>
  <!-- 비금속 분기 -->
  <rect x="36" y="92" width="205" height="48" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text x="138" y="110" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">비금속</text>
  <text x="138" y="128" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">표면의 난반사 색상</text>
  <!-- 금속 분기 -->
  <rect x="259" y="92" width="205" height="48" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text x="362" y="110" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">금속</text>
  <text x="362" y="128" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정반사 색상 (F0)으로 사용</text>

  <!-- (2) Metallic 카드 -->
  <rect x="20" y="164" width="460" height="130" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
  <text x="36" y="184" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) Metallic</text>
  <text x="52" y="202" font-family="sans-serif" font-size="10" fill="currentColor">그레이스케일 값 (0.0 ~ 1.0)</text>
  <!-- 0.0 분기 -->
  <rect x="36" y="214" width="205" height="68" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text x="138" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">0.0 — 비금속 (유전체)</text>
  <text x="138" y="250" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Albedo → Diffuse에 사용</text>
  <text x="138" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">F0 ≈ 0.04 고정</text>
  <!-- 1.0 분기 -->
  <rect x="259" y="214" width="205" height="68" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text x="362" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">1.0 — 금속</text>
  <text x="362" y="250" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Albedo → F0에 사용</text>
  <text x="362" y="268" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Diffuse = 0</text>

  <!-- (3) Roughness 카드 -->
  <rect x="20" y="308" width="460" height="108" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
  <text x="36" y="328" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) Roughness</text>
  <text x="172" y="328" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(또는 Smoothness = 1 − Roughness)</text>
  <text x="52" y="346" font-family="sans-serif" font-size="10" fill="currentColor">그레이스케일 값 (0.0 ~ 1.0)</text>
  <!-- 0.0 분기 -->
  <rect x="36" y="358" width="205" height="46" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text x="138" y="376" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">0.0 — 매끄러운 표면</text>
  <text x="138" y="394" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">날카로운 반사</text>
  <!-- 1.0 분기 -->
  <rect x="259" y="358" width="205" height="46" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text x="362" y="376" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">1.0 — 거친 표면</text>
  <text x="362" y="394" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">부드러운 반사</text>
</svg>
</div>

Metallic 값에 따라 Albedo의 역할이 달라지는 것이 이 워크플로우의 핵심입니다. 비금속(Metallic = 0)에서는 Albedo가 난반사 색상이 되고, 정반사의 F0는 약 0.04(비금속의 일반적인 값)로 고정됩니다. 금속(Metallic = 1)에서는 Albedo가 정반사의 F0 색상이 되고, 난반사는 0으로 사라집니다. 금속은 들어온 빛을 대부분 정반사하므로, 난반사에 쓸 에너지가 남지 않기 때문입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 외곽 -->
  <rect x="1" y="1" width="538" height="308" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="26" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Metallic 값에 따른 변화</text>

  <!-- 칼럼 1: Metallic = 0.0 (비금속) -->
  <rect x="16" y="42" width="164" height="254" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="98" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Metallic = 0.0</text>
  <text x="98" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">비금속 — 예: 나무</text>
  <line x1="28" y1="86" x2="168" y2="86" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="30" y="106" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Diffuse</text>
  <text x="30" y="122" font-family="sans-serif" font-size="10" fill="currentColor">= Albedo (나무 색)</text>
  <text x="30" y="150" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">F0</text>
  <text x="30" y="166" font-family="sans-serif" font-size="10" fill="currentColor">= (0.04, 0.04, 0.04)</text>
  <text x="30" y="182" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">비금속 기본값</text>
  <line x1="28" y1="196" x2="168" y2="196" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <!-- 결과 화살표 -->
  <line x1="30" y1="216" x2="38" y2="216" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="42,216 36,212 36,220" fill="currentColor"/>
  <text x="48" y="212" font-family="sans-serif" font-size="9" fill="currentColor">나무 색의 난반사</text>
  <text x="48" y="226" font-family="sans-serif" font-size="9" fill="currentColor">+ 약한 흰색 하이라이트</text>

  <!-- 칼럼 2: Metallic = 1.0 (금속) -->
  <rect x="188" y="42" width="164" height="254" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="270" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Metallic = 1.0</text>
  <text x="270" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">금속 — 예: 금</text>
  <line x1="200" y1="86" x2="340" y2="86" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="202" y="106" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Diffuse</text>
  <text x="202" y="122" font-family="sans-serif" font-size="10" fill="currentColor">= (0, 0, 0) — 없음</text>
  <text x="202" y="150" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">F0</text>
  <text x="202" y="166" font-family="sans-serif" font-size="10" fill="currentColor">= Albedo (금색)</text>
  <text x="202" y="182" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(1.0, 0.71, 0.29)</text>
  <line x1="200" y1="196" x2="340" y2="196" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <!-- 결과 화살표 -->
  <line x1="202" y1="216" x2="210" y2="216" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,216 208,212 208,220" fill="currentColor"/>
  <text x="220" y="212" font-family="sans-serif" font-size="9" fill="currentColor">난반사 없음</text>
  <text x="220" y="226" font-family="sans-serif" font-size="9" fill="currentColor">+ 금색 하이라이트</text>

  <!-- 칼럼 3: Metallic = 0.5 (중간값 — 비권장) -->
  <rect x="360" y="42" width="164" height="254" rx="5" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.45"/>
  <text x="442" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.55">Metallic = 0.5</text>
  <text x="442" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">중간값</text>
  <line x1="372" y1="86" x2="512" y2="86" stroke="currentColor" stroke-width="0.6" opacity="0.2"/>
  <!-- X 표시 (비권장 강조) -->
  <line x1="418" y1="108" x2="466" y2="148" stroke="currentColor" stroke-width="2.5" opacity="0.18"/>
  <line x1="466" y1="108" x2="418" y2="148" stroke="currentColor" stroke-width="2.5" opacity="0.18"/>
  <text x="442" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">실제 재질에서는</text>
  <text x="442" y="192" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">중간값을 사용하지 않음</text>
  <line x1="372" y1="204" x2="512" y2="204" stroke="currentColor" stroke-width="0.6" opacity="0.2"/>
  <text x="442" y="224" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">"반쯤 금속인 물질"은</text>
  <text x="442" y="238" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">물리적으로 존재하지 않음</text>
  <text x="442" y="262" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">0.5 근처 값은</text>
  <text x="442" y="276" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">먼지 낀 금속, 녹슨 표면 등</text>
  <text x="442" y="290" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">마스크 용도로만 사용</text>
</svg>
</div>

### Specular 워크플로우

Metallic 워크플로우가 Albedo 하나로 Diffuse와 F0를 겸하는 반면, Specular 워크플로우는 Diffuse Color와 Specular Color를 별도의 RGB 맵으로 분리합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="440" height="370" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 제목 -->
  <text x="220" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Specular 워크플로우</text>

  <!-- 카드 1: Diffuse Color -->
  <rect x="20" y="46" width="400" height="90" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="40" y="68" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) Diffuse Color</text>
  <text x="40" y="88" font-family="sans-serif" font-size="11" fill="currentColor">RGB 색상 맵</text>
  <text x="40" y="106" font-family="sans-serif" font-size="11" fill="currentColor">난반사 색상 (비금속에만 의미 있음)</text>
  <text x="40" y="124" font-family="sans-serif" font-size="11" fill="currentColor">금속에서는 검정(0,0,0)으로 설정해야 함</text>

  <!-- 카드 2: Specular Color -->
  <rect x="20" y="152" width="400" height="108" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="40" y="174" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) Specular Color</text>
  <text x="40" y="194" font-family="sans-serif" font-size="11" fill="currentColor">RGB 색상 맵</text>
  <text x="40" y="212" font-family="sans-serif" font-size="11" fill="currentColor">정반사 F0 색상을 직접 지정</text>
  <text x="40" y="232" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">비금속: 그레이 (약 0.04)</text>
  <text x="40" y="248" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">금속: 금속 고유의 색상</text>

  <!-- 카드 3: Glossiness -->
  <rect x="20" y="276" width="400" height="76" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="40" y="298" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) Glossiness</text>
  <text x="192" y="298" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">= 1 − Roughness</text>
  <text x="40" y="318" font-family="sans-serif" font-size="11" fill="currentColor">그레이스케일 값 (0.0 ~ 1.0)</text>
  <text x="40" y="338" font-family="sans-serif" font-size="11" fill="currentColor">표면 매끄러움 정도</text>
</svg>
</div>

Specular 워크플로우의 핵심은 F0 색상을 아티스트가 RGB로 직접 지정한다는 점입니다. Metallic 워크플로우에서 비금속의 F0는 약 0.04로 고정되지만, Specular 워크플로우에서는 비금속이라도 F0를 자유롭게 설정할 수 있어, 물이나 보석처럼 비금속이면서 F0가 0.04보다 높은 재질을 정밀하게 표현할 때 유리합니다.

<br>

반면, Metallic 워크플로우처럼 셰이더가 에너지 배분을 자동으로 처리하지 않으므로, Diffuse Color와 Specular Color의 합이 입사 에너지를 초과하지 않도록 아티스트가 직접 관리해야 합니다.

### 두 워크플로우의 비교

**Metallic vs Specular 워크플로우 비교**

| 항목 | Metallic | Specular |
|---|---|---|
| 텍스처 수 (같은 정보 기준) | 적음 — Albedo(RGB), Metallic(Gray), Roughness(Gray) | 많음 — Diffuse(RGB), Specular(RGB), Glossiness(Gray) |
| 텍스처 메모리 | 적음 (Metallic이 1채널) | 많음 (Specular가 3채널) |
| 아티스트 오류 가능성 | Metallic 0 또는 1만 사용하면 안전 | 비금속에서 Diffuse와 Specular 합이 에너지 보존 위반 가능 |
| 제어 세밀도 | 비금속의 $F_0$ 제어 불가 ($0.04$ 고정) | $F_0$를 직접 RGB로 설정 가능 |
| 업계 표준 | Unity, Unreal 기본 채택 | 일부 AAA 스튜디오에서 사용 |

<br>

Metallic 워크플로우가 업계 표준으로 자리 잡은 이유는 텍스처 메모리가 적고, 에너지 보존 위반이 구조적으로 발생하기 어렵기 때문입니다. Metallic 값이 0 또는 1이면 셰이더가 Diffuse와 Specular의 에너지 배분을 자동으로 처리합니다.

---

## Unity의 Standard Shader / URP Lit Shader

앞에서 다룬 Cook-Torrance BRDF와 Metallic 워크플로우는 Unity에서 Standard Shader와 URP Lit Shader로 구현되어 있습니다.

### Built-in Standard Shader

Built-in 렌더 파이프라인의 **Standard Shader**는 Metallic 워크플로우와 Specular 워크플로우를 모두 지원합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="480" height="340" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 제목 -->
  <text x="240" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Standard Shader의 주요 프로퍼티</text>
  <text x="240" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Metallic 워크플로우</text>

  <!-- 구분선 -->
  <line x1="30" y1="56" x2="450" y2="56" stroke="currentColor" stroke-width="0.8" opacity="0.2"/>

  <!-- 프로퍼티 행 1: Albedo -->
  <text x="40" y="80" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Albedo</text>
  <text x="160" y="80" font-family="sans-serif" font-size="11" fill="currentColor">표면 색상 텍스처 + 틴트 색상</text>

  <!-- 프로퍼티 행 2: Metallic -->
  <line x1="30" y1="92" x2="450" y2="92" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>
  <text x="40" y="112" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Metallic</text>
  <text x="160" y="112" font-family="sans-serif" font-size="11" fill="currentColor">0.0 ~ 1.0 (또는 텍스처)</text>

  <!-- 프로퍼티 행 3: Smoothness -->
  <line x1="30" y1="124" x2="450" y2="124" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>
  <text x="40" y="144" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Smoothness</text>
  <text x="160" y="144" font-family="sans-serif" font-size="11" fill="currentColor">0.0 ~ 1.0 (= 1 − Roughness)</text>
  <text x="160" y="162" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Metallic Alpha 또는 Albedo Alpha에 저장 가능</text>

  <!-- 프로퍼티 행 4: Normal Map -->
  <line x1="30" y1="174" x2="450" y2="174" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>
  <text x="40" y="194" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Normal Map</text>
  <text x="160" y="194" font-family="sans-serif" font-size="11" fill="currentColor">표면의 미세 굴곡 표현</text>

  <!-- 프로퍼티 행 5: Height Map -->
  <line x1="30" y1="206" x2="450" y2="206" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>
  <text x="40" y="226" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Height Map</text>
  <text x="160" y="226" font-family="sans-serif" font-size="11" fill="currentColor">시차 매핑 (Parallax)</text>

  <!-- 프로퍼티 행 6: Occlusion -->
  <line x1="30" y1="238" x2="450" y2="238" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>
  <text x="40" y="258" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Occlusion</text>
  <text x="160" y="258" font-family="sans-serif" font-size="11" fill="currentColor">간접광 차폐</text>

  <!-- 프로퍼티 행 7: Emission -->
  <line x1="30" y1="270" x2="450" y2="270" stroke="currentColor" stroke-width="0.5" opacity="0.12"/>
  <text x="40" y="290" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Emission</text>
  <text x="160" y="290" font-family="sans-serif" font-size="11" fill="currentColor">자체 발광 색상</text>
</svg>
</div>

### URP Lit Shader

URP(Universal Render Pipeline)의 **Lit Shader**도 같은 Cook-Torrance BRDF를 사용하며, 모바일 GPU에 맞춘 경량 구현을 채택합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- 전체 제목 -->
  <text x="230" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP Lit Shader의 특징</text>

  <!-- 카드 1: PBR 기반 -->
  <rect x="20" y="40" width="420" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">PBR 기반</text>
  <text x="40" y="84" font-family="sans-serif" font-size="11" fill="currentColor">GGX NDF + 슐릭 프레넬 + Smith-GGX 기하함수</text>
  <text x="40" y="106" font-family="sans-serif" font-size="11" fill="currentColor">에너지 보존 + 프레넬 효과 기본 포함</text>

  <!-- 카드 2: Metallic 워크플로우 -->
  <rect x="20" y="148" width="420" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="170" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Metallic 워크플로우 기본</text>

  <!-- 좌측 열 -->
  <circle cx="50" cy="194" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="62" y="198" font-family="sans-serif" font-size="11" fill="currentColor">Base Map (Albedo)</text>
  <circle cx="50" cy="216" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="62" y="220" font-family="sans-serif" font-size="11" fill="currentColor">Metallic Map</text>
  <circle cx="50" cy="238" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="62" y="242" font-family="sans-serif" font-size="11" fill="currentColor">Smoothness</text>
  <text x="62" y="258" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(Metallic Alpha에 저장)</text>

  <!-- 우측 열 -->
  <circle cx="250" cy="194" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="262" y="198" font-family="sans-serif" font-size="11" fill="currentColor">Normal Map</text>
  <circle cx="250" cy="216" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="262" y="220" font-family="sans-serif" font-size="11" fill="currentColor">Occlusion Map</text>
  <circle cx="250" cy="238" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="262" y="242" font-family="sans-serif" font-size="11" fill="currentColor">Emission</text>

  <!-- 카드 3: 모바일 최적화 -->
  <rect x="20" y="316" width="420" height="104" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="338" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">모바일 최적화</text>

  <circle cx="50" cy="360" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="62" y="364" font-family="sans-serif" font-size="11" fill="currentColor">싱글패스 포워드 렌더링</text>
  <circle cx="50" cy="382" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="62" y="386" font-family="sans-serif" font-size="11" fill="currentColor">셰이더 내부에서 half 정밀도 적극 활용</text>
  <circle cx="50" cy="404" r="2.5" fill="currentColor" opacity="0.5"/>
  <text x="62" y="408" font-family="sans-serif" font-size="11" fill="currentColor">Specular Highlights / Environment Reflections 끄기 옵션</text>
</svg>
</div>

싱글패스 포워드 렌더링이란, 각 오브젝트를 한 번의 드로우 콜로 그리면서 주 광원과 보조 광원의 조명을 모두 계산하는 방식입니다. 디퍼드 렌더링(Deferred Rendering)과 달리 G-Buffer(지오메트리 정보를 저장하는 중간 렌더 타겟)를 거치지 않으므로 추가적인 메모리 대역폭 부담이 없고, 모바일 GPU에서 메모리 대역폭은 전력 소비와 직결되므로 이 구조가 모바일에 유리합니다.

### 모바일에서의 PBR 비용

PBR은 Blinn-Phong보다 프래그먼트 셰이더 연산량이 많습니다. GGX NDF 계산, 프레넬 근사, 기하학적 감쇠 계산이 추가되기 때문입니다. URP는 이 추가 비용을 줄이기 위한 옵션을 제공합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 전체 제목 -->
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP Lit의 모바일 비용 관리</text>

  <!-- (1) Specular Highlights 끄기 — 강조 카드 (두꺼운 테두리) -->
  <rect x="20" y="40" width="440" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2.2"/>
  <text x="40" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) Specular Highlights 끄기</text>
  <text x="214" y="62" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">— 큰 ALU 절약</text>
  <text x="40" y="84" font-family="sans-serif" font-size="11" fill="currentColor">Material Inspector에서 체크 해제</text>
  <line x1="40" y1="96" x2="52" y2="96" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="52,93 52,99 58,96" fill="currentColor" opacity="0.5"/>
  <text x="62" y="100" font-family="sans-serif" font-size="11" fill="currentColor">Specular 계산(D, F, G) 전체를 건너뜀</text>
  <line x1="40" y1="114" x2="52" y2="114" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="52,111 52,117 58,114" fill="currentColor" opacity="0.5"/>
  <text x="62" y="118" font-family="sans-serif" font-size="11" fill="currentColor">하이라이트가 사라지지만, 거친 재질(나무, 돌)에서는 시각적 차이 적음</text>
  <line x1="40" y1="132" x2="52" y2="132" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="52,129 52,135 58,132" fill="currentColor" opacity="0.5"/>
  <text x="62" y="136" font-family="sans-serif" font-size="11" fill="currentColor">큰 ALU 절약</text>

  <!-- (2) Environment Reflections 끄기 -->
  <rect x="20" y="188" width="440" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="210" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) Environment Reflections 끄기</text>
  <line x1="40" y1="224" x2="52" y2="224" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="52,221 52,227 58,224" fill="currentColor" opacity="0.5"/>
  <text x="62" y="228" font-family="sans-serif" font-size="11" fill="currentColor">Reflection Probe 샘플링 건너뜀</text>
  <line x1="40" y1="244" x2="52" y2="244" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="52,241 52,247 58,244" fill="currentColor" opacity="0.5"/>
  <text x="62" y="248" font-family="sans-serif" font-size="11" fill="currentColor">큐브맵 텍스처 샘플링 1회 절약</text>

  <!-- (3) half 정밀도 -->
  <rect x="20" y="286" width="440" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="308" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) half 정밀도</text>
  <text x="40" y="330" font-family="sans-serif" font-size="11" fill="currentColor">URP Lit 셰이더 코드는 내부적으로 조명 계산의 중간값에</text>
  <text x="40" y="350" font-family="sans-serif" font-size="11" fill="currentColor">half(16비트 부동소수점)를 사용하여 모바일 GPU의 ALU 처리량을 높임</text>

  <!-- (4) Simple Lit Shader — 강조 카드 (두꺼운 테두리) -->
  <rect x="20" y="384" width="440" height="126" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2.2"/>
  <text x="40" y="406" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(4) Simple Lit Shader</text>
  <text x="195" y="406" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">— PBR 포기, 최대 성능</text>
  <text x="40" y="430" font-family="sans-serif" font-size="11" fill="currentColor">PBR 대신 Blinn-Phong 기반의 간소화 셰이더</text>
  <text x="40" y="452" font-family="sans-serif" font-size="11" fill="currentColor">성능이 극도로 중요한 저사양 기기용</text>
  <line x1="40" y1="468" x2="52" y2="468" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="52,465 52,471 58,468" fill="currentColor" opacity="0.5"/>
  <text x="62" y="472" font-family="sans-serif" font-size="11" fill="currentColor">PBR의 물리적 일관성은 포기</text>

  <!-- 하단 주석 -->
  <text x="240" y="508" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">굵은 테두리 = 성능 영향이 큰 옵션</text>
</svg>
</div>

<br>

대부분의 모바일 프로젝트에서는 Lit Shader를 기본으로 사용하되, PBR 비용이 시각적 효과 대비 과한 오브젝트에 한해 Simple Lit이나 Unlit을 적용합니다.

### Shader Graph와 커스텀 셰이더

URP에서는 **Shader Graph**를 사용하여 비주얼 노드 기반으로 커스텀 셰이더를 만들 수 있습니다. Shader Graph의 Lit Master Node를 선택하면 Cook-Torrance BRDF 위에 커스텀 효과를 추가하는 구조입니다. 아티스트가 추가한 노드는 Albedo, Metallic, Smoothness, Normal 등의 입력 값을 가공하는 역할을 합니다.

<br>

Lit 기반 Shader Graph에서 Albedo, Metallic, Smoothness 등 표준 입력 포트에 값을 연결하는 한, 셰이더 내부의 Cook-Torrance BRDF가 Diffuse와 Specular의 에너지 배분을 자동으로 처리합니다. 다만 Emission은 BRDF 외부에서 더해지는 값이므로, 과도한 Emission으로 인한 물리적 일관성 훼손은 아티스트가 직접 관리해야 합니다.

---

## 마무리

셰이딩 모델은 빛이 표면에 닿았을 때 관찰자가 보는 밝기와 색을 수학적으로 계산하는 체계입니다. Lambert에서 시작하여 Phong, Blinn-Phong을 거쳐 PBR까지, 셰이딩 모델은 점점 더 물리적으로 정확한 결과를 내는 방향으로 발전해 왔습니다.

- Lambert 모델은 난반사만 계산하는 가장 단순한 모델입니다. 밝기는 표면 법선 N과 광원 방향 L의 내적(N·L)으로 결정됩니다. BRDF가 상수이므로 모든 방향에서 같은 밝기로 보입니다
- Phong 모델은 Lambert에 정반사를 추가합니다. 반사 벡터 R과 시야 벡터 V의 내적 max(R·V, 0)^n으로 하이라이트를 계산하며, 지수 n으로 하이라이트 크기를 조절합니다
- Blinn-Phong 모델은 반법선 벡터 H = normalize(L + V)를 사용하여 정반사를 근사합니다. N·H로 하이라이트를 계산하며, Phong보다 계산 효율이 좋습니다
- PBR은 에너지 보존, 프레넬 효과, 미세면 이론에 기반하여 물리적으로 정확한 셰이딩을 수행합니다. Cook-Torrance BRDF는 법선 분포 함수(D), 프레넬 함수(F), 기하학적 감쇠 함수(G)의 세 요소로 구성됩니다
- Metallic 워크플로우는 Albedo, Metallic, Roughness 세 파라미터로 재질을 정의하며, Unity와 Unreal의 기본 방식입니다. Specular 워크플로우보다 텍스처 메모리가 적고 에너지 보존 위반이 구조적으로 발생하기 어렵습니다
- Unity의 URP Lit Shader는 PBR 기반이며, 모바일 최적화를 위해 Specular Highlights와 Environment Reflections를 개별적으로 끌 수 있습니다. 극도로 제한된 환경에서는 Blinn-Phong 기반의 Simple Lit Shader를 사용할 수 있습니다

이 시리즈에서 다룬 빛의 물리적 원리, 색 표현 체계, 셰이딩 모델은 다른 시리즈의 내용과 직접 연결됩니다.

[조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)에서 다루는 라이팅 비용의 핵심 구성 요소가 BRDF 평가이고, [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서 다루는 ALU 비용의 주요 대상 중 하나가 Cook-Torrance의 D, F, G 계산입니다.

[렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)에서 다룬 머티리얼의 구성 요소(셰이더 + 파라미터)가 이 글의 Metallic 워크플로우에서 구체적인 형태를 갖춥니다.

<br>

---

**관련 글**
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- **색과 빛 (3) - 셰이딩 모델 (현재 글)**

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
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- **색과 빛 (3) - 셰이딩 모델** (현재 글)
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
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
