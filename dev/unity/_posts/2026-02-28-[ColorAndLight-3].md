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

[색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)에서는 빛이 표면에서 반사, 굴절, 흡수로 나뉘는 과정을 살펴보고, 이를 BRDF라는 개념으로 정리했습니다. 이어 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서는 RGB 색 모델과 감마 보정, 선형 워크플로우를 통해 색을 디지털 값으로 표현하는 방법을 다루었습니다.

이제 남은 질문은 표면에 닿은 빛이 관찰자에게 어떤 밝기와 색으로 보이느냐입니다. 이 밝기와 색을 계산하는 규칙을 **셰이딩 모델(Shading Model)**이라고 부릅니다. BRDF가 표면이 들어온 빛을 어느 방향으로 얼마나 반사하는지만 정의한다면, 셰이딩 모델은 그 반사 특성에 광원의 색과 강도까지 포함해 관찰자가 보는 최종 밝기와 색을 계산합니다.

초기 셰이딩 모델은 물리 법칙에서 엄밀하게 유도한 식이라기보다, 눈으로 보기에 그럴듯한 명암과 광택을 만들기 위한 **경험적(Empirical)** 모델이었습니다. 이후 GPU가 더 복잡한 조명 계산을 실시간으로 처리할 수 있게 되면서, 에너지 보존과 프레넬 효과, 미세 면 이론을 수식에 직접 반영하는 **PBR(Physically Based Rendering, 물리 기반 렌더링)**이 실시간 그래픽스의 기준으로 자리 잡았습니다.

이 글에서는 단순한 Lambert 모델에서 출발해 Phong과 Blinn-Phong을 거쳐 PBR에 이르기까지, 셰이딩 모델이 어떻게 발전해 왔는지와 각 모델의 수학적 구조를 차례로 살펴봅니다.

---

## Lambert 모델

Lambert 모델은 구조가 단순해, 셰이딩 모델을 처음 이해할 때 출발점으로 삼기 좋습니다. 관찰 방향과 정반사는 다루지 않고, 빛이 표면에 닿는 각도만으로 난반사 밝기를 계산하기 때문입니다.

### 난반사의 수학적 표현

Lambert 모델이 다루는 반사는 **난반사(Diffuse Reflection)** 하나뿐입니다. 난반사는 거친 표면에서 빛이 사방으로 흩어지는 반사로, 표면을 어느 방향에서 보더라도 밝기가 비슷하게 보입니다. Lambert 모델은 이 성질을 이상화해, 관찰 방향이 달라져도 표면 밝기는 그대로라고 가정합니다.

관찰 방향이 밝기를 바꾸지 않으므로, 남는 변수는 빛이 표면에 들어오는 각도뿐입니다. 같은 세기의 빛이라도 표면에 비스듬히 들어오면 그 빛이 더 넓은 면적에 퍼져, 단위 면적이 받는 빛의 양이 줄어듭니다. 그래서 빛을 정면으로 받는 표면일수록 밝고, 비스듬히 받을수록 어두워집니다.

이 입사 각도는 **표면 법선(N)**과 **광원 방향(L)** 사이의 내적으로 나타낼 수 있습니다. 두 벡터가 모두 단위 벡터이면 N·L은 둘 사이 각 θ의 코사인과 같아, 빛이 정면에 가까울수록 1에, 표면과 나란해질수록 0에 가까워집니다.

**Lambert 모델의 수식**

$$
\text{Diffuse} = \max(\mathbf{N} \cdot \mathbf{L},\ 0) \times C_{\text{light}} \times C_{\text{albedo}}
$$

- $\mathbf{N}$: 표면 법선 벡터 (단위 벡터 — 크기가 1이어야 내적이 cos θ 값이 됨)
- $\mathbf{L}$: 표면에서 광원을 향하는 방향 벡터 (단위 벡터)
- $\mathbf{N} \cdot \mathbf{L}$: 두 벡터의 내적 ($= \cos\theta$, $\theta$는 법선과 광원 방향 사이의 각도)
- $C_{\text{light}}$: 광원의 색상과 강도
- $C_{\text{albedo}}$: 표면의 Albedo — 각 파장(RGB 채널)별 반사율을 0.0~1.0 범위로 나타낸 값

<br>

실제 각도를 넣어 보면 식의 의미가 분명해집니다. 빛이 표면에 수직으로 들어와 θ가 0°이면 cos 0° = 1이라 밝기가 최대가 되고, 빛이 표면과 나란히 스쳐 θ가 90°에 다가가면 cos 90° = 0이라 밝기는 0에 가까워집니다.

θ가 90°를 넘어서면 N·L은 음수가 되는데, 이는 빛이 표면 뒤쪽에서 들어온다는 뜻입니다. 빛이 닿지 않는 면이 음의 밝기를 갖지 않도록, $\max$ 함수가 이 값을 0으로 잘라 냅니다.

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

앞의 Diffuse 수식은 광원의 색과 강도까지 넣어 최종 밝기를 계산합니다. 반면 [색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 BRDF는 광원을 제외하고 표면 자체의 반사 특성만 분리해, 들어온 빛이 어느 방향으로 얼마나 반사되는지를 정의합니다.

Lambert 모델은 관찰 방향이 바뀌어도 밝기가 같다고 보므로, 그 BRDF 역시 방향에 따라 달라지지 않는 하나의 상수가 됩니다.

**Lambert BRDF**

$$
f_{\text{Lambert}} = \frac{C_{\text{albedo}}}{\pi}
$$

<br>

앞 절의 Diffuse 식에는 이 π 나누기가 빠져 있었는데, BRDF로 엄밀하게 쓰면 이렇게 분모에 π가 들어갑니다. 여기서 $C_{\text{albedo}}$를 $\pi$로 나누는 이유는 에너지 보존을 지키기 위해서입니다. 표면에서 반사돼 나가는 빛의 총량은 들어온 빛을 넘을 수 없으니, BRDF의 크기도 그 한계를 넘지 않도록 정규화해야 합니다.

> 에너지 보존 법칙은 [색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 자세히 다룹니다.

<br>

정규화 상수가 $\pi$인 것은 반사광이 나가는 방향을 반구 전체에 걸쳐 더한 결과입니다. 난반사 표면은 받은 빛을 한 방향이 아니라, 표면 위쪽 반구(Hemisphere)를 채우는 모든 방향으로 반사합니다. 그래서 이 표면이 내보내는 빛의 총량을 구하려면, 그 방향들로 나가는 빛을 빠짐없이 더해야 합니다.

이렇게 모든 방향에 걸쳐 빛을 더하는 계산이 바로 적분입니다. 각 방향으로 나가는 빛의 크기는, 그 방향으로 얼마나 반사되는지를 나타내는 BRDF 값에 cos θ 항을 곱한 값입니다.

여기서 cos θ를 곱하는 것은 앞서 난반사에서 본 것과 같은 이유에서입니다. 한 방향이 법선에서 멀어질수록 같은 표면 면적이 그 방향에 기여하는 비율이 작아지고, 그 비율이 cos θ로 나타납니다.

Lambert BRDF는 상수여서 적분 밖으로 빠져나오고, 남은 cos θ를 반구 전체에 적분하면 그 값이 정확히 π가 됩니다. 그래서 BRDF를 $C_{\text{albedo}} / \pi$로 두면 이 π와 적분에서 나온 π가 서로 상쇄되어, 총 반사 에너지는 $C_{\text{albedo}}$만 남습니다.

$C_{\text{albedo}}$의 각 채널은 0.0에서 1.0 사이 반사율이므로, 이렇게 정규화하고 나면 총 반사 에너지가 입사 에너지를 넘지 않습니다. 반대로 π로 나누지 않으면 총 반사 에너지가 $\pi \cdot C_{\text{albedo}}$로 커져, 입사 에너지를 넘어서며 에너지 보존을 깨뜨릴 수 있습니다.

<br>

다만 실제 셰이더에서는 연산을 아끼려고 이 π 나누기를 건너뛰기도 합니다. 그러면 Diffuse가 π배 밝아지는데, 광원 강도를 미리 π로 나눠 두면 그만큼 상쇄되어 최종 결과는 같아집니다.

Unity의 URP Lit Shader처럼 PBR을 엄밀히 따르는 셰이더는 BRDF 안에 π 나누기를 그대로 두지만, 레거시 셰이더나 커스텀 셰이더에서는 π를 생략하고 광원 쪽에서 보정하는 관례가 아직 남아 있습니다.

### Lambert 모델의 한계

Lambert 모델은 난반사만 다루므로 **정반사(Specular Reflection)**를 표현하지 못합니다. 정반사로 생기는 밝은 하이라이트는 관찰 방향에 따라 위치가 달라지는데, Lambert는 바로 그 방향을 계산에 넣지 않기 때문입니다.

그래서 플라스틱이나 유리, 금속처럼 하이라이트가 또렷한 표면에는 맞지 않고, 분필이나 콘크리트, 사포처럼 광택이 거의 없는 재질에 잘 들어맞습니다. 광택이 있는 재질까지 표현하려면 정반사 성분을 따로 더해야 합니다.

---

## Phong 모델

Phong 모델은 Lambert가 다루지 못한 정반사를 항으로 더해, 표면의 밝은 하이라이트까지 표현합니다. 하이라이트는 빛이 거울처럼 반사되는 방향을 카메라가 가까이서 바라볼 때 강하게 나타나고, 그 방향에서 벗어나 볼수록 약해집니다.

### 정반사의 추가

1975년에 Bui Tuong Phong이 제안한 Phong 모델은 표면의 색을 세 성분으로 나누어 계산한 뒤 더합니다.

- **Ambient**(환경광) — 실제 장면에서는 다른 표면에서 반사된 빛, 하늘 빛 등 간접광이 존재하여 그림자 영역도 완전한 검정이 되지 않습니다. Ambient는 이 간접광을 하나의 상수로 단순 근사한 항입니다.
- **Diffuse**(난반사) — 앞 섹션의 Lambert 모델과 동일합니다.
- **Specular**(정반사) — 표면의 밝은 하이라이트를 만드는 항입니다.

<br>

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

<br>

Ambient와 Diffuse는 앞에서 다룬 계산을 그대로 사용합니다. Phong 모델에서 새롭게 볼 부분은 Specular 항입니다.

### 반사 벡터와 하이라이트

Specular 항의 밝기는 반사 방향과 시야 방향이 얼마나 가까운지에 따라 결정됩니다.

**반사 벡터 R**은 입사광이 표면 법선을 기준으로 대칭 반사된 방향입니다. **시야 벡터 V**는 표면에서 카메라를 향하는 방향입니다.
R과 V가 거의 같은 방향이면 관찰자는 강한 하이라이트를 보고, 두 방향이 멀어질수록 하이라이트는 약해집니다.

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

<br>

$$
\mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}
$$

<br>

여기서 $(\mathbf{N} \cdot \mathbf{L})\mathbf{N}$은 L을 법선 방향으로 투영한 벡터입니다. 반사 벡터 R은 L이 법선을 기준으로 대칭이 되도록 뒤집힌 방향이며, 위 다이어그램의 L과 R이 법선을 사이에 두고 같은 각도를 이루는 모습이 이 관계를 보여 줍니다.

<br>

이렇게 R을 구하고 나면, 앞서 본 Specular 수식에서 색을 뺀 기하학적 항만 따로 떼어 볼 수 있습니다.

$$
\max(\mathbf{R} \cdot \mathbf{V},\ 0)^{n}
$$

<br>

$\mathbf{R} \cdot \mathbf{V}$는 두 단위 벡터가 이루는 각도의 코사인입니다. 시야 벡터가 반사 벡터와 같은 방향이면 1에 가깝고, 두 벡터가 직각에 가까워질수록 0에 가까워집니다.

이 값이 1에 가까울수록 관찰 방향이 정반사 방향과 일치하므로 하이라이트가 강하게 보입니다. 0에 가까우면 관찰 방향이 정반사 방향에서 벗어나 하이라이트가 사라집니다.

### 광택 지수 (Shininess Exponent)

지수 $n$은 하이라이트의 크기와 날카로움을 조절합니다. 하이라이트는 $\mathbf{R} \cdot \mathbf{V}$가 큰 방향, 곧 반사 방향 근처에서만 밝게 나타나는데, $\mathbf{R} \cdot \mathbf{V}$를 $n$제곱하면 반사 방향에서 멀어질수록 밝기가 더 가파르게 작아져 밝은 영역이 좁아지기 때문입니다.

$\mathbf{R} \cdot \mathbf{V}$는 0에서 1 사이의 값입니다. 여기에 $n$제곱을 적용하면 1에 가까운 값은 비교적 유지되지만, 1에서 조금만 멀어진 값은 빠르게 0에 가까워집니다.

예를 들어 $0.9^{10} \approx 0.35$는 아직 의미 있는 값이지만, 지수를 키운 $0.9^{256} \approx 2 \times 10^{-12}$는 사실상 0과 같습니다.

따라서 $n$이 크면 반사 방향에서 조금만 벗어나도 기여가 작아져 하이라이트가 좁고 날카롭게 보입니다. $n$이 작으면 더 넓은 각도에서 값이 남아 하이라이트가 넓고 부드럽게 퍼집니다.

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

Phong 모델은 Lambert보다 광택을 더 그럴듯하게 표현하지만, 그만큼 세 가지 한계도 함께 따라옵니다.

첫째, 반사 벡터 R을 픽셀마다 새로 계산해야 합니다. R = 2(N·L)N - L에는 내적과 스칼라-벡터 곱셈, 벡터 뺄셈이 모두 들어가고, 프래그먼트 셰이더는 이 계산을 화면의 수많은 픽셀에서 반복합니다. 해상도가 높아질수록 정반사 계산에 드는 비용도 그만큼 늘어납니다.

둘째, 에너지 보존을 보장하지 않습니다. 표면에 들어온 빛은 난반사와 정반사로 나뉘므로, 두 성분을 합쳐도 입사 에너지를 넘을 수 없어야 합니다. 그러나 Phong 모델은 Diffuse와 Specular를 따로 계산해 더할 뿐, 둘이 에너지를 어떻게 나눠 가질지는 제한하지 않습니다.

셋째, 하이라이트 경계가 매끄럽게 이어지지 않을 수 있습니다. 정반사 항 max(R·V, 0)^n에서 R과 V의 각도가 90도를 넘으면 R·V가 음수가 되고, max 함수가 그 값을 곧바로 0으로 자르기 때문입니다. 그래서 하이라이트가 넓게 퍼지거나 시선이 표면을 비스듬히 스치는 그레이징 앵글(Grazing Angle)에서는, 하이라이트 가장자리가 부드럽게 사라지지 않고 갑자기 끊겨 보입니다.

---

## Blinn-Phong 모델

Blinn-Phong 모델은 Phong의 정반사 계산을 더 가볍게 바꾼 모델입니다. 반사 벡터를 따로 구하는 대신, 빛 방향과 시야 방향의 한가운데를 향하는 방향에 표면 법선이 얼마나 가까운지로 하이라이트를 구합니다.

### Half-Vector를 이용한 근사

Jim Blinn이 1977년에 제안한 이 모델은 **반법선 벡터(Half-Vector, H)**를 사용합니다. H는 광원 방향 L과 시야 방향 V의 중간 방향이며, 표면 법선 N이 이 방향에 가까울수록 강한 하이라이트가 생긴다고 봅니다.

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

<br>

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

H를 사용하는 이유는 정반사가 일어나는 조건에 있습니다. 빛이 L 방향에서 들어와 V 방향으로 거울처럼 반사되려면, 표면의 법선이 L과 V의 한가운데를 향해야 합니다. 그 한가운데 방향이 바로 H이므로, 표면 법선 N이 H에 가까워질수록, 곧 N·H가 1에 가까울수록 표면이 빛을 시야 쪽으로 더 잘 반사해 하이라이트가 강해집니다.

H를 기준으로 삼으면 Phong에서 보이던 하이라이트 경계의 급격한 끊김도 줄어듭니다. Phong에서는 R과 V의 각도가 90도를 넘으면 R·V가 음수가 되어 max 함수가 이를 0으로 잘랐지만, Blinn-Phong이 쓰는 N과 H는 일반적인 조명과 시야에서 그 각도를 넘는 경우가 드뭅니다. 그래서 0으로 잘리는 영역이 줄고, 하이라이트가 가장자리에서 더 부드럽게 사라집니다.

### Phong과의 비교

Blinn-Phong이 Phong보다 널리 쓰인 이유는 계산이 더 가볍고, 하이라이트가 더 안정적으로 보이기 때문입니다.

**Phong vs Blinn-Phong**

| 항목 | Phong | Blinn-Phong |
|---|---|---|
| 정반사 계산 | $\mathbf{R} \cdot \mathbf{V}$ | $\mathbf{N} \cdot \mathbf{H}$ |
| 반사 벡터 계산 | $\mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}$ (필요) | 불필요 |
| Half-Vector 계산 | 불필요 | $\mathbf{H} = \text{normalize}(\mathbf{L} + \mathbf{V})$ (필요) |
| 계산 비용 | 약간 높음 | 약간 효율적 (Directional Light에서 $\mathbf{H}$ 재사용) |
| 하이라이트 형태 | 원형에 가까움 | 약간 넓고 부드러움 |
| 에너지 보존 | 보장하지 않음 | 보장하지 않음 |

두 모델의 계산 비용 차이는 H와 R이 각각 무엇에 의존하는지에서 나옵니다. Blinn-Phong의 H = normalize(L + V)는 빛 방향과 시야 방향에만 의존하므로, 두 방향이 모두 일정한 장면에서는 H가 상수가 되어 한 번 계산한 값을 여러 픽셀에서 재사용할 수 있습니다. 광원이 한 방향으로 고정된 Directional Light에 직교 투영을 쓰는 경우가 그렇고, 원근 투영이라도 멀리 있는 표면에서는 시야 차이가 작아 근사적으로 다시 쓸 수 있습니다.

반면 Phong의 R = 2(N·L)N - L은 표면 법선 N에 의존합니다. N은 곡률과 노멀맵에 따라 픽셀마다 달라지므로, L이 일정해도 R은 픽셀마다 다시 계산해야 합니다. 그래서 같은 Directional Light에서도 Blinn-Phong은 H를 재사용해 정반사 계산을 아끼지만, Phong은 R을 줄이기 어렵습니다.

이런 이유로 OpenGL과 DirectX의 **고정 파이프라인(Fixed-Function Pipeline)** 시절에는 Blinn-Phong이 기본 셰이딩 모델로 널리 사용되었습니다. 이 시기에는 사용자가 셰이더 코드를 직접 작성하기보다 하드웨어가 제공하는 조명 모델을 선택해 사용했습니다.

Blinn-Phong은 오늘날에도 가벼운 실시간 셰이딩을 설명할 때 기준점으로 쓰입니다.

### 전통적 모델의 공통 한계

지금까지 본 Lambert와 Phong, Blinn-Phong은 모두 물리 법칙이 아니라 보기 좋은 결과를 실시간으로 얻으려고 만든 **경험적(Empirical)** 모델입니다. 그만큼 세 모델에는 공통된 물리적 한계가 있습니다.

<br>

첫째, 에너지 보존을 구조적으로 보장하지 않습니다. Phong과 Blinn-Phong은 Diffuse와 Specular를 독립적으로 계산한 뒤 더하므로, 두 계수를 잘못 조합하면 반사 에너지가 입사 에너지를 넘을 수 있습니다. Lambert BRDF($C_{\text{albedo}} / \pi$)는 에너지 보존을 만족하지만, 실제 셰이더에서 π 나누기를 생략하면 이 조건이 깨질 수 있습니다.

<br>

둘째, 프레넬 효과가 빠져 있습니다. 실제 표면은 시야가 비스듬해질수록, 곧 그레이징 앵글(Grazing Angle)에 가까워질수록 반사율이 높아지는데, 전통적 모델은 이 변화를 계산에 넣지 않습니다.

<br>

셋째, 하이라이트 면적과 에너지 분배가 연결되어 있지 않습니다. 광택 지수 n을 낮추면 하이라이트는 넓어지지만, 그에 맞춰 밝기가 물리적으로 정규화되지는 않습니다. 실제 표면이라면 같은 에너지가 더 넓은 영역에 퍼질수록 단위 면적당 밝기가 낮아져야 합니다.

<br>

이런 한계들을 해결하기 위해 에너지 보존, 프레넬 효과, 미세 면(microfacet) 분포를 수식에 직접 담는 접근이 등장했습니다.

---

## PBR (Physically Based Rendering)

PBR은 셰이딩 모델의 기준을 “보기 좋은 근사”에서 “물리적으로 일관된 근사”로 옮긴 접근입니다. 완전한 광학 시뮬레이션은 아니지만, 표면이 받은 빛보다 더 많은 빛을 내보내지 않고, 시야 각도와 표면 거칠기에 따른 반사 변화를 수식 안에서 처리합니다.

### PBR의 핵심 원칙

[색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 BRDF가 PBR의 토대입니다. PBR은 이 BRDF가 물리적으로 일관되도록 세 가지 원칙을 따릅니다.

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

  <!-- 카드 3: 미세 면 이론 -->
  <rect x="20" y="266" width="380" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="288" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) 미세 면 이론</text>
  <text x="160" y="288" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Microfacet Theory</text>
  <text x="40" y="310" font-family="sans-serif" font-size="11" fill="currentColor">표면을 미세한 거울 면의 집합으로 모델링</text>
  <text x="40" y="330" font-family="sans-serif" font-size="11" fill="currentColor">러프니스가 미세 면의 방향 분포를 결정</text>
</svg>
</div>

### 미세 면 이론 (Microfacet Theory)

정반사 계산의 중심에는 **미세 면 이론(Microfacet Theory)**이 있습니다. PBR은 표면을 완전히 매끄러운 한 장의 면으로 보지 않고, 작은 거울 면들이 모인 구조로 봅니다.

겉보기에는 매끈한 표면도 미시적으로 보면 수많은 **미세 면(microfacet)**으로 이루어져 있습니다. 각 미세 면은 저마다 다른 방향을 향한 작은 거울처럼 빛을 반사합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <rect x="0" y="0" width="580" height="520" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="28" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor" text-anchor="middle">미세 면 이론 (Microfacet Theory)</text>

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
  <text x="400" y="72" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(미세 면들의 집합)</text>
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

  <text x="290" y="128" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">각 미세 면은 자신만의 법선(미세 면 법선, m)을 가짐</text>
  <text x="290" y="143" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">거시적 법선 N과 미세 면 법선 m은 다를 수 있음</text>

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

  <text x="150" y="308" font-family="sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle" opacity="0.6">미세 면 법선이 거시적 법선과</text>
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

  <text x="430" y="308" font-family="sans-serif" font-size="9.5" fill="currentColor" text-anchor="middle" opacity="0.6">미세 면 법선이 여러 방향으로 분산</text>

  <text x="430" y="340" font-family="sans-serif" font-size="9" fill="currentColor" text-anchor="middle" opacity="0.5">반사 분포:</text>
  <ellipse cx="430" cy="378" rx="65" ry="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" opacity="0.6"/>

  <text x="430" y="448" font-family="sans-serif" font-size="10" fill="currentColor" text-anchor="middle" opacity="0.6">정반사가 넓게 퍼짐</text>
  <text x="430" y="466" font-family="sans-serif" font-size="10.5" fill="currentColor" text-anchor="middle" font-weight="bold">넓고 어두운 하이라이트</text>
</svg>
</div>

미세 면 법선이 한 방향으로 정렬되어 있는지, 아니면 여러 방향으로 흩어져 있는지를 나타내는 값이 러프니스(Roughness)입니다.

러프니스가 0에 가까우면 미세 면 법선이 비슷한 방향으로 정렬되어 날카로운 반사가 생깁니다. 러프니스가 1에 가까울수록 미세 면 법선이 여러 방향으로 분산되어 반사가 넓고 부드럽게 퍼집니다.

### Cook-Torrance BRDF

미세 면 이론을 실제 정반사 수식으로 옮긴 것이 **Cook-Torrance BRDF**이며, PBR의 정반사 성분은 이 식으로 계산됩니다.

<br>

**Cook-Torrance Specular BRDF**

$$
f_{\text{spec}} = \frac{D(\mathbf{h}) \cdot F(\mathbf{v}, \mathbf{h}) \cdot G(\mathbf{l}, \mathbf{v}, \mathbf{h})}{4(\mathbf{N} \cdot \mathbf{L})(\mathbf{N} \cdot \mathbf{V})}
$$

- $D$: 법선 분포 함수 (Normal Distribution Function)
- $F$: 프레넬 함수 (Fresnel Function)
- $G$: 기하 감쇠 함수 (Geometry Function)
- $\mathbf{h}$: 반법선 벡터 $\mathbf{H}$ ($= \text{normalize}(\mathbf{L} + \mathbf{V})$)

<br>

이 식은 분자에서 세 항(D·F·G)을 곱해 정반사의 세기를 구하고, 분모로 그 값을 미세 면 단위에서 거시적 표면 단위로 바꿉니다. 분자의 D·F·G부터 차례로 살펴본 뒤, 분모의 정규화 항을 정리하겠습니다.

먼저 **법선 분포 함수(NDF)**인 D는 전체 미세 면 가운데 법선 m이 반법선 벡터 H를 향한 것의 비율을 나타냅니다.

거울 반사는 입사 방향과 반사 방향이 미세 면 법선을 기준으로 대칭일 때 일어납니다. 반법선 벡터 H는 L과 V의 중간 방향이므로, 법선이 H를 향한 미세 면만 L에서 들어온 빛을 V 방향으로 반사할 수 있습니다. D는 이런 미세 면의 비율을 나타내므로 하이라이트의 모양과 밝기에 직접 영향을 줍니다.

러프니스가 낮으면 D 분포가 좁고 높아져 하이라이트가 작고 날카롭게 보입니다. 러프니스가 높으면 D 분포가 넓고 낮아져 하이라이트가 넓고 부드럽게 보입니다.

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

D의 형태를 정하는 NDF로는 **GGX (Trowbridge-Reitz)** 분포가 널리 사용됩니다. Beckmann 분포는 중심에서 멀어질수록 값이 빠르게 줄어 하이라이트 가장자리의 긴 번짐을 표현하기 어렵습니다. GGX는 꼬리(tail)가 길어 중심에서 멀어진 영역의 값도 천천히 줄기 때문에, 현실적인 하이라이트 번짐을 더 잘 표현합니다. Unity의 URP Lit Shader도 GGX 기반의 정반사 모델을 사용합니다.

<br>

D가 어떤 미세 면이 정반사에 기여하는지를 정한다면, **프레넬 함수**인 F는 그 미세 면이 시야 각도에 따라 빛을 얼마나 반사하는지를 정합니다. [색과 빛 (1)](/dev/unity/ColorAndLight-1/)에서 다룬 프레넬 효과, 즉 시야가 비스듬해질수록 반사율이 커지는 현상을 표현하는 항입니다.

원래의 프레넬 방정식은 실시간 렌더링에서 그대로 쓰기에는 계산 비용이 큽니다. 그래서 실시간 셰이딩에서는 내적과 거듭제곱만으로 충분히 가까운 값을 얻는 **슐릭 근사(Schlick's Approximation)**를 주로 사용합니다.

<br>

**슐릭의 프레넬 근사 (Schlick's Approximation)**

$$
F_{\text{Schlick}} = F_0 + (1 - F_0)(1 - \cos\theta)^5
$$

- $F_0$: 정면 입사($\theta = 0°$) 시의 반사율
  - 비금속(유전체): 약 $0.04$ (4%)
  - 금속: 채널별 $0.2 \sim 1.0$ (금속 종류와 파장에 따라 다름)
- $\cos\theta$: 시야 방향과 반법선 벡터의 내적 ($= \mathbf{V} \cdot \mathbf{H}$)

<br>

정면에서 보는 $\theta = 0°$에서는 $(1 - \cos\theta)^5$가 0이 되어 $F = F_0$가 됩니다. 즉 재질의 기본 반사율만 적용됩니다. 반대로 시야가 표면을 거의 스치는 $\theta = 90°$에서는 이 항이 1에 가까워져 $F$가 1.0에 다다르고, 거의 모든 빛이 반사됩니다.

비금속, 즉 유전체는 $F_0$가 대체로 0.04 안팎의 회색 값입니다. 반면 금속은 채널마다 $F_0$가 달라 고유한 색을 띠며, 금은 (1.0, 0.71, 0.29), 은은 (0.95, 0.93, 0.88), 구리는 (0.95, 0.64, 0.54)에 가깝습니다.

금속의 $F_0$가 채널마다 다른 이유는 금속이 파장마다 빛을 다르게 반사하기 때문입니다. 금이 노란빛을 띠는 것도 적색과 녹색 파장을 청색보다 강하게 반사하기 때문이며, $F_0$의 R > G > B 관계가 이 특성을 나타냅니다.

<br>

D가 어느 미세 면이 반사에 기여하는지, F가 그 미세 면이 얼마나 반사하는지를 정했다면, **기하 감쇠 함수**인 G는 빛이 그 미세 면에 도달하고 다시 빠져나오는 동안 주변 미세 면에 가리지 않는 비율을 나타냅니다.

러프니스가 높아 표면 요철이 거칠어지면 두 종류의 차단이 생깁니다. 하나는 들어오는 빛이 목표 미세 면에 도달하기 전에 주변 미세 면에 가려지는 그림자 효과(Shadowing)이고, 다른 하나는 반사된 빛이 관찰자에게 나가기 전에 주변 미세 면에 가려지는 마스킹 효과(Masking)입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="520" height="400" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 제목 -->
  <text x="260" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기하 감쇠</text>

  <!-- ===== 좌측: 그림자 효과 (Shadowing) ===== -->
  <text x="135" y="55" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">그림자 효과 (Shadowing)</text>
  <text x="135" y="72" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">빛이 미세 면에 도달하기 전에 인접 미세 면에 의해 차단</text>

  <!-- 미세 면 지그재그 (좌측) -->
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

  <!-- 미세 면 기저선 (좌측) -->
  <line x1="15" y1="200" x2="255" y2="200" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- ===== 우측: 마스킹 효과 (Masking) ===== -->
  <text x="390" y="55" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">마스킹 효과 (Masking)</text>
  <text x="390" y="72" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">반사된 빛이 인접 미세 면에 의해 차단</text>

  <!-- 미세 면 지그재그 (우측) -->
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

  <!-- 미세 면 기저선 (우측) -->
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

G는 0에서 1 사이의 값입니다. 0은 빛이 완전히 가려진 상태이고, 1은 가려짐이 없는 상태입니다. 시야가 표면을 비스듬히 스칠수록 미세 면끼리 서로를 가리는 비율이 커져 G가 낮아지고, 거친 표면의 가장자리 반사가 과도하게 밝아지는 것을 막습니다.

<br>

분모의 4 × (N·L) × (N·V)는 정규화 항입니다. D·F·G는 미세 면 기준의 반사량을 다루므로, 이를 거시적 표면의 단위 면적 기준으로 변환해야 합니다. N·L은 입사 방향의 코사인 법칙을, N·V는 관찰 방향의 기하학적 비율을 반영합니다. 앞의 4는 미세 면 법선과 반법선 벡터 사이의 기하학적 변환에서 나오는 상수입니다.

### PBR의 최종 셰이딩

지금까지 정반사 성분을 D, F, G로 나누어 보았습니다. 이제 난반사와 정반사를 합쳐 한 픽셀의 최종 색을 계산합니다.

Diffuse와 Specular를 단순히 더하면 에너지 보존이 깨질 수 있습니다. 프레넬 항 $F$만큼의 에너지가 Specular에 사용되므로, Diffuse에는 남은 에너지 비율인 $(1 - F)$만 배정해야 합니다.

**PBR 최종 셰이딩**

$$
\text{Color} = (1 - F) \cdot f_{\text{diffuse}} + f_{\text{specular}}
$$

- $(1 - F)$: 프레넬 반사에 사용되지 않은 에너지 비율 — 이 비율만큼만 Diffuse에 할당
- $f_{\text{diffuse}}$: Lambert Diffuse ($= C_{\text{albedo}} / \pi$). $\pi$는 앞에서 다룬 반구 적분의 정규화 상수
- $f_{\text{specular}}$: Cook-Torrance Specular ($= D \cdot F \cdot G \;/\; 4(N \cdot L)(N \cdot V)$)

<br>

이렇게 Diffuse와 Specular로 에너지를 나누고 Cook-Torrance BRDF를 정규화해 두면, 파라미터를 바꿔도 반사 에너지가 입사 에너지를 넘지 않습니다.

러프니스를 높이면 하이라이트가 넓어지는 만큼 단위 면적당 밝기는 낮아져, 같은 에너지가 더 넓은 영역에 퍼집니다. 광택 지수를 낮춰 하이라이트만 넓히던 전통적 모델과 달리, 여기서는 면적과 밝기가 함께 움직입니다.

메탈릭 값을 높이면 Albedo가 Diffuse 색이 아니라 F0, 즉 정반사 색에 더 많이 사용됩니다. Metallic이 1이면 Specular 색은 Albedo와 같아지고 Diffuse는 0에 가까워집니다. 이처럼 PBR의 물리식은 같더라도, 머티리얼 파라미터를 어떤 방식으로 입력하느냐에 따라 워크플로우가 나뉩니다.

---

## Metallic 워크플로우 vs Specular 워크플로우

Cook-Torrance BRDF로 셰이딩하려면 F0, Roughness, Albedo 같은 값이 필요합니다. 이 값을 머티리얼에 지정하는 방식은 크게 두 가지가 있습니다. 하나는 Metallic 워크플로우이고, 다른 하나는 Specular 워크플로우입니다. 두 방식은 같은 BRDF를 사용하지만, 아티스트가 입력하는 파라미터 구성이 다릅니다.

### Metallic 워크플로우

Metallic 워크플로우는 Albedo, Metallic, Roughness 세 파라미터를 기본 입력으로 사용합니다.

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

이 워크플로우에서는 Metallic 값에 따라 Albedo의 의미가 달라집니다. 비금속(Metallic = 0)에서는 Albedo가 표면의 난반사 색상이고, 정반사의 F0는 약 0.04의 회색 값으로 고정됩니다. 금속(Metallic = 1)에서는 Albedo가 정반사의 F0 색상으로 사용되고, Diffuse는 0이 됩니다. 금속은 빛을 내부로 흡수해 색 있는 난반사를 만들기보다, 표면에서 색 있는 정반사로 되돌리기 때문입니다.

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

Metallic 워크플로우가 Albedo 하나의 의미를 Metallic 값에 따라 바꾸는 방식이라면, Specular 워크플로우는 난반사 색과 정반사 F0 색을 **Diffuse Color**와 **Specular Color** 두 RGB 맵으로 나눠 지정합니다.

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

이 방식에서는 F0 색상을 RGB로 직접 조정할 수 있습니다. Metallic 워크플로우에서는 비금속의 F0가 대체로 0.04에 고정되지만, Specular 워크플로우에서는 물이나 보석처럼 비금속이면서도 기본 반사율이 다른 재질을 더 세밀하게 표현할 수 있습니다.

대신 오류 가능성도 커집니다. Diffuse Color와 Specular Color를 모두 직접 지정하므로, 두 값의 조합이 에너지 보존을 위반하지 않도록 주의해야 합니다.

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

Metallic 워크플로우가 Unity와 Unreal을 비롯한 실시간 렌더링의 기본으로 자리 잡은 것은 메모리와 안정성 덕분입니다. Metallic은 1채널 값이라 텍스처 메모리를 적게 씁니다. 또한 색을 따로 지정하지 않고 이 한 값으로 Diffuse와 Specular의 배분을 정하므로, 아티스트가 에너지 보존을 위반하기 어렵습니다.

---

## Unity의 URP Lit Shader

지금까지 살펴본 Cook-Torrance BRDF와 Metallic 워크플로우는 Unity URP의 기본 PBR 셰이더인 **Lit Shader**에도 그대로 쓰입니다. Lit Shader는 기능이 옵션으로 나뉘고 셰이더 변형이 관리되어, 모바일부터 PC까지 폭넓은 플랫폼에서 동작합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 312" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
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
</svg>
</div>

### 싱글패스 포워드 렌더링

Lit Shader의 모바일 성능에는 픽셀당 조명 연산량뿐 아니라 장면을 그리는 렌더링 경로도 영향을 줍니다. URP는 기본 경로로 싱글패스 포워드 렌더링을 쓰며, 오브젝트를 그리는 패스 안에서 주 광원과 추가 광원의 조명을 함께 계산합니다. 디퍼드 렌더링(Deferred Rendering)은 이와 달리 화면에 보이는 표면의 지오메트리 정보를 G-Buffer라는 중간 버퍼에 먼저 기록해 두고, 조명은 그 버퍼를 읽어 별도 단계에서 계산합니다.

두 방식은 메모리 대역폭을 쓰는 양에서 차이가 납니다. 디퍼드는 화면 크기만 한 G-Buffer를 기록했다가 조명 단계에서 다시 읽어 들이는 만큼 대역폭 소모가 크지만, 포워드는 이 버퍼를 두지 않으므로 쓰고 다시 읽는 왕복 자체가 없습니다.
메모리 대역폭이 성능과 전력 소비에 곧바로 영향을 주는 모바일 GPU에서는 디퍼드의 이런 대역폭 부담이 특히 크게 작용하기 때문에, URP는 포워드를 기본 렌더링 경로로 삼습니다.

> 싱글패스 포워드와 디퍼드 렌더링의 구조와 차이는 [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)에서 자세히 다룹니다.

### 모바일에서의 PBR 비용

PBR은 최적화되어 있더라도 Blinn-Phong보다 프래그먼트 셰이더 연산이 많습니다. GGX NDF, 프레넬 근사, 기하 감쇠를 계산해야 하므로 픽셀당 ALU 비용이 증가합니다. URP는 이 비용을 줄일 수 있도록 몇 가지 옵션을 제공합니다.

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

실제 모바일 프로젝트에서는 모든 오브젝트에 Lit Shader를 일률적으로 적용하기보다, 재질의 사실감이 화면에서 얼마나 드러나는지에 맞춰 셰이더를 골라 쓰는 쪽이 현실적입니다.
플레이어가 가까이서 보는 주인공이나 무기, 화면을 크게 차지하는 주요 배경에는 Lit을 유지해 PBR의 금속감과 거칠기를 살리고, 멀리 놓인 소품이나 광택이 거의 드러나지 않는 표면은 Simple Lit이나, 조명 계산을 생략하는 Unlit으로 낮춰 비용을 줄입니다.

### Shader Graph와 커스텀 셰이더

기본 Lit Shader만으로 원하는 표현을 구현하기 어려울 때는 URP의 **Shader Graph**로 커스텀 셰이더를 직접 만들 수 있습니다. 이때 Lit 계열 출력 노드를 쓰면, 빛을 다루는 Cook-Torrance BRDF는 셰이더 내부에 그대로 남고, 그래프는 Albedo, Metallic, Smoothness, Normal 같은 입력 값을 가공해 넘기는 역할만 맡습니다. Diffuse와 Specular로 에너지를 나누는 계산은 그 내부 BRDF가 처리하므로, 커스텀 셰이더에서도 물리 기반의 일관성이 유지됩니다.

다만 Emission은 BRDF를 거치지 않고 최종 색에 그대로 더해지므로, 에너지 보존의 적용을 받지 않습니다. 그래서 발광 값을 지나치게 키우면 이 물리 기반 일관성이 깨질 수 있습니다.

---

## 마무리

셰이딩 모델은 빛이 표면에 닿았을 때 관찰자가 어떤 밝기와 색을 보게 되는지를 수학으로 계산합니다. Lambert에서 출발해 Phong과 Blinn-Phong을 거쳐 PBR에 이르기까지, 이 계산은 점점 더 물리 법칙에 가까워지는 방향으로 다듬어져 왔습니다.

- **Lambert 모델**은 난반사만 다루는 가장 단순한 모델입니다. 밝기를 표면 법선 N과 광원 방향 L의 내적(N·L)으로 결정하고, 관찰 방향은 고려하지 않습니다.
- **Phong 모델**은 Lambert에 정반사를 더합니다. 반사 벡터 R과 시야 벡터 V의 내적을 max(R·V, 0)^n 형태로 계산해 하이라이트를 만들고, 지수 n으로 하이라이트 크기를 조절합니다.
- **Blinn-Phong 모델**은 반법선 벡터 H = normalize(L + V)를 사용해 정반사를 근사합니다. R을 직접 계산하지 않아 Phong보다 가볍고, 하이라이트 경계도 더 안정적입니다.
- **PBR**은 에너지 보존, 프레넬 효과, 미세 면 이론을 기반으로 물리적으로 일관된 셰이딩을 계산합니다. Cook-Torrance BRDF는 법선 분포 함수(D), 프레넬 함수(F), 기하 감쇠 함수(G)로 정반사를 구성합니다.
- **Metallic 워크플로우**는 Albedo, Metallic, Roughness로 재질을 정의합니다. Specular 워크플로우보다 텍스처 메모리를 적게 쓰고, 에너지 보존을 깨는 조합을 줄이기 쉬워 Unity와 Unreal에서 널리 쓰입니다.
- **URP Lit Shader**는 PBR 기반 셰이더로, 모바일에서는 대역폭 부담이 적은 싱글패스 포워드 경로로 그려지고, Specular Highlights와 Environment Reflections를 끄는 옵션으로 연산 비용을 줄일 수 있습니다. 성능이 더 중요한 재질에는 Simple Lit 또는 Unlit을 선택할 수 있습니다.

정리하면 셰이딩 모델의 발전은 더 많은 물리 조건을 수식 안에 넣는 방향으로 진행되었습니다. Lambert는 난반사만 계산했고, Phong과 Blinn-Phong은 정반사를 추가했으며, PBR은 에너지 보존과 프레넬 효과, 미세 면 분포까지 함께 다룹니다. 대신 모델이 물리적으로 정확해질수록 계산 비용도 함께 증가합니다.

이 글에서 다룬 셰이딩 모델은 [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)에서 정리한 머티리얼과 셰이더의 관계를 바탕으로 합니다. 머티리얼이 Albedo, Metallic, Roughness 같은 입력 값을 제공하면 셰이더가 그 값을 BRDF에 넣어 최종 색을 계산하며, 이 글이 다룬 것이 그 BRDF의 안쪽입니다.

이 셰이딩 모델은 이후 조명과 최적화 주제로도 이어집니다. [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)에서는 조명 계산이 실제 렌더링 비용에 어떤 영향을 주는지 다루고, [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서는 Cook-Torrance의 D, F, G 계산처럼 ALU 비용을 늘리는 요소를 더 자세히 살펴봅니다.

<br>

---

**관련 글**
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
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
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- **색과 빛 (3) - 셰이딩 모델** (현재 글)
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
