---
layout: single
title: "그래픽스 수학 (4) - 투영 - soo:bak"
date: "2026-02-27 22:42:00 +0900"
description: 원근 투영, 직교 투영, 절두체, 깊이 값의 비선형성, Z-fighting, Reversed-Z를 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 수학
  - 투영
  - 모바일
---

## 3D를 2D로 변환하는 문제

[그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)에서 Projection 행렬이 절두체를 직육면체로 변환하고, 원근 나눗셈(w로 나누기)을 통해 원근감이 만들어지는 과정을 살펴봤습니다.

3D 세계를 2D 화면에 그리려면 차원을 하나 줄여야 합니다.

x, y, z 세 축을 x, y 두 축의 평면으로 눌러야 하는데, 단순히 z를 버리면 모든 오브젝트가 거리와 무관하게 같은 크기로 그려집니다. 멀리 있는 산과 눈앞의 캐릭터가 같은 크기가 되고, z 정보가 없으니 어떤 오브젝트가 앞에 있는지도 판단할 수 없습니다.

<br>

투영(Projection)은 이 문제를 해결합니다. Projection 행렬과 원근 나눗셈을 거쳐 3D 좌표가 2D 화면 좌표로 바뀌는 과정에서, 화면의 각 픽셀 위치마다 깊이 값이 깊이 버퍼(depth buffer)에 따로 저장됩니다. 덕분에 원근감을 표현하면서, 어떤 오브젝트가 다른 오브젝트 뒤에 가려지는지도 판정할 수 있습니다.

다만 원근 투영의 수학적 구조에는 한계가 있습니다. 깊이 버퍼의 정밀도가 카메라 가까이에 편중되어 있어서, 먼 곳에서는 정밀도가 급격히 부족해집니다.

먼 곳에서 거의 같은 거리에 놓인 두 표면의 깊이 차이가 이 정밀도보다 작으면, GPU가 앞뒤를 구별할 수 없습니다. 매 프레임 판정이 뒤바뀌면서 화면이 깜빡이는 Z-fighting이 발생합니다.

<br>

이 글에서는 원근 투영과 직교 투영의 Projection 행렬 구조, 비선형성의 원인, 그리고 이를 완화하는 Reversed-Z 기법을 다룹니다.

---

## 원근 투영

### 절두체(Frustum)의 구성 요소

원근 투영(Perspective Projection)은 카메라에서 먼 오브젝트일수록 화면에서 작게, 가까운 오브젝트일수록 크게 그리는 투영 방식입니다.

사람의 눈이 세계를 보는 방식과 같은 원리이며, 3D 게임에서 깊이감을 표현하는 기본 수단입니다.

<br>

원근 투영에서 카메라가 볼 수 있는 영역은 **절두체(Frustum)**라는 잘린 사각뿔 형태이며, 네 가지 파라미터가 그 모양을 결정합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- FOV angle lines (camera to near plane edges, dashed) -->
  <line x1="40" y1="150" x2="140" y2="115" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <line x1="40" y1="150" x2="140" y2="185" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <!-- Frustum (trapezoid) — edges converge to camera at (40,150) -->
  <!-- near half-height=35 at dist=100, far half-height=35×400/100=140 at dist=400 -->
  <polygon points="140,115 440,10 440,290 140,185" fill="currentColor" fill-opacity="0.06" stroke="none"/>
  <!-- Near plane -->
  <line x1="140" y1="115" x2="140" y2="185" stroke="currentColor" stroke-width="2"/>
  <!-- Far plane -->
  <line x1="440" y1="10" x2="440" y2="290" stroke="currentColor" stroke-width="2"/>
  <!-- Top edge -->
  <line x1="140" y1="115" x2="440" y2="10" stroke="currentColor" stroke-width="1.5"/>
  <!-- Bottom edge -->
  <line x1="140" y1="185" x2="440" y2="290" stroke="currentColor" stroke-width="1.5"/>
  <!-- Center axis (dashed) -->
  <line x1="40" y1="150" x2="440" y2="150" stroke="currentColor" stroke-dasharray="6,4" stroke-width="0.7" opacity="0.3"/>
  <!-- Camera point -->
  <circle cx="40" cy="150" r="5" fill="currentColor"/>
  <!-- FOV angle arc (radius 40, half-angle = atan(35/100) ≈ 19.3°) -->
  <!-- endpoints at radius 40: x=40*cos(19.3°)=37.8, y=40*sin(19.3°)=13.2 -->
  <path d="M 37.8,-13.2 A 40,40 0 0,1 37.8,13.2" stroke="currentColor" fill="none" stroke-width="1.2" transform="translate(40, 150)"/>
  <!-- Labels -->
  <text fill="currentColor" x="40" y="175" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">카메라</text>
  <text fill="currentColor" x="95" y="153" font-size="11" font-family="sans-serif">FOV</text>
  <text fill="currentColor" x="290" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.4">절두체</text>
  <text fill="currentColor" x="140" y="207" text-anchor="middle" font-size="10" font-family="sans-serif">Near Plane</text>
  <text fill="currentColor" x="440" y="308" text-anchor="middle" font-size="10" font-family="sans-serif">Far Plane</text>
  <!-- Distance indicators: n -->
  <line x1="40" y1="248" x2="140" y2="248" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="40" y1="243" x2="40" y2="253" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="140" y1="243" x2="140" y2="253" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="90" y="262" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">n</text>
  <!-- Distance indicators: f -->
  <line x1="40" y1="273" x2="440" y2="273" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="40" y1="268" x2="40" y2="278" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="440" y1="268" x2="440" y2="278" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="240" y="287" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">f</text>
  <!-- Parameter list -->
  <text fill="currentColor" x="30" y="310" font-size="10" font-family="sans-serif" opacity="0.7">1. Near Plane: 이 평면보다 가까운 오브젝트는 렌더링하지 않음</text>
  <text fill="currentColor" x="30" y="325" font-size="10" font-family="sans-serif" opacity="0.7">2. Far Plane: 이 평면보다 먼 오브젝트는 렌더링하지 않음  ·  3. FOV: 세로 시야각 (60°~90°)  ·  4. Aspect Ratio: 가로/세로 비율</text>
</svg>
</div>

<br>

Near plane과 far plane 사이에 있는 오브젝트만 렌더링 대상이며, 이 범위 밖의 오브젝트는 클리핑되어 버려집니다.

FOV가 넓으면 화면에 더 많은 영역이 들어오지만, 같은 해상도에 더 넓은 범위를 담으므로 개별 오브젝트가 작아집니다.

FOV가 좁으면 망원 렌즈처럼 좁은 범위만 크게 보입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <text fill="currentColor" x="140" y="22" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">좁은 FOV (30°)</text>
  <text fill="currentColor" x="420" y="22" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">넓은 FOV (90°)</text>
  <g transform="translate(35, 195)">
    <polygon points="0,0 160,-43 160,43" fill="currentColor" fill-opacity="0.07" stroke="none"/>
    <line x1="0" y1="0" x2="160" y2="0" stroke="currentColor" stroke-dasharray="5,4" stroke-width="0.7" opacity="0.3"/>
    <line x1="0" y1="0" x2="160" y2="-43" stroke="currentColor" stroke-width="1.5"/>
    <line x1="0" y1="0" x2="160" y2="43" stroke="currentColor" stroke-width="1.5"/>
    <line x1="160" y1="-43" x2="160" y2="43" stroke="currentColor" stroke-width="2.5"/>
    <circle cx="0" cy="0" r="4" fill="currentColor"/>
    <path d="M 48.3,-12.9 A 50,50 0 0,1 48.3,12.9" stroke="currentColor" fill="none" stroke-width="1.2"/>
    <text fill="currentColor" x="62" y="5" font-size="12" font-family="sans-serif">30°</text>
    <text fill="currentColor" x="0" y="24" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">카메라</text>
  </g>
  <g transform="translate(315, 195)">
    <polygon points="0,0 160,-160 160,160" fill="currentColor" fill-opacity="0.07" stroke="none"/>
    <line x1="0" y1="0" x2="160" y2="0" stroke="currentColor" stroke-dasharray="5,4" stroke-width="0.7" opacity="0.3"/>
    <line x1="0" y1="0" x2="160" y2="-160" stroke="currentColor" stroke-width="1.5"/>
    <line x1="0" y1="0" x2="160" y2="160" stroke="currentColor" stroke-width="1.5"/>
    <line x1="160" y1="-160" x2="160" y2="160" stroke="currentColor" stroke-width="2.5"/>
    <circle cx="0" cy="0" r="4" fill="currentColor"/>
    <path d="M 24.7,-24.7 A 35,35 0 0,1 24.7,24.7" stroke="currentColor" fill="none" stroke-width="1.2"/>
    <text fill="currentColor" x="42" y="5" font-size="12" font-family="sans-serif">90°</text>
    <text fill="currentColor" x="0" y="24" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">카메라</text>
  </g>
  <text fill="currentColor" x="140" y="385" text-anchor="middle" font-size="12" font-family="sans-serif">좁은 영역을 크게 표시</text>
  <text fill="currentColor" x="140" y="403" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.5">망원 렌즈 효과</text>
  <text fill="currentColor" x="420" y="385" text-anchor="middle" font-size="12" font-family="sans-serif">넓은 영역을 작게 표시</text>
  <text fill="currentColor" x="420" y="403" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.5">광각 렌즈 효과</text>
</svg>
</div>

Aspect ratio는 가로 시야각을 결정합니다.

화면이 16:9 비율이면, 세로 FOV가 60도일 때 가로 시야각은 약 91도가 됩니다.

투영 행렬은 이 세로 FOV와 aspect ratio를 조합하여 절두체의 가로·세로 범위를 계산합니다.

---

### 투영 행렬의 구성 원리

원근 투영 행렬은 절두체 안의 3D 좌표를 클립 공간(clip space)으로 변환합니다.

<br>

행렬의 역할은 크게 두 가지입니다.

하나는 x, y를 화면 비율에 맞게 스케일하는 것이고, 다른 하나는 z와 w를 조작하여 깊이 판정과 원근감을 준비하는 것입니다.

<br>

x, y 스케일부터 보면, 절두체 경계에 있는 좌표가 원근 나눗셈(w로 나누기) 후 NDC의 [-1, 1] 범위에 딱 맞도록 조정됩니다.

FOV가 넓으면 카메라가 넓은 범위를 보고 있으므로, 그 넓은 범위를 [-1, 1]에 우겨넣기 위해 모든 x, y가 축소됩니다. 화면에서 보면 개별 오브젝트가 작아지는 광각 효과입니다.

반대로 FOV가 좁으면 좁은 범위만 [-1, 1]에 채우므로, x, y가 확대되어 망원 렌즈처럼 오브젝트가 크게 보입니다.

<br>

z, w 쪽에서는 행렬이 z 좌표를 near~far 범위에 맞게 재배치하면서, 뷰 공간의 z값(카메라로부터의 거리)을 w 성분에 복사합니다.

이후 GPU가 수행하는 원근 나눗셈(x/w, y/w, z/w)에서 이 w가 분모가 되므로, 먼 오브젝트일수록 x, y가 더 많이 줄어들어 화면에서 작게 표시됩니다.

<br>

이 구조를 행렬로 표현하면 다음과 같습니다.

$$
P_{\text{persp}} = \begin{bmatrix} \frac{1}{\text{aspect} \cdot \tan(\text{FOV}/2)} & 0 & 0 & 0 \\ 0 & \frac{1}{\tan(\text{FOV}/2)} & 0 & 0 \\ 0 & 0 & \frac{f}{n - f} & \frac{nf}{n - f} \\ 0 & 0 & -1 & 0 \end{bmatrix}
$$

$$n$$ = near plane 거리, $$f$$ = far plane 거리, $$\text{FOV}$$ = 세로 시야각(라디안), $$\text{aspect}$$ = 가로/세로 비율

(그래픽스 API에 따라 부호와 배치가 다를 수 있음)

<br>

**`(1,1)` 원소 — `1/(aspect * tan(FOV/2))`** : 절두체 좌우 경계에 있는 점이 원근 나눗셈 후 NDC에서 정확히 -1 또는 1이 되도록 x를 스케일합니다. FOV가 넓으면 tan(FOV/2)가 커지고, 그 역수를 곱하므로 x 스케일 값이 줄어들어 좌표가 원점 쪽으로 압축됩니다. aspect로도 나누어, 16:9처럼 가로가 넓은 화면에서 x축 범위를 비율에 맞게 보정합니다.

<br>

**`(2,2)` 원소 — `1/tan(FOV/2)`** : y 좌표를 같은 원리로 스케일합니다. FOV가 세로 시야각 기준으로 정의되어 있으므로, y축에는 aspect 보정 없이 FOV만으로 스케일 값이 결정됩니다.

<br>

**세 번째 행 — z 변환** : z 좌표를 near~far 범위 안에서 재배치합니다. 행렬 곱 직후 z_clip = A * z_view + B (A, B는 near·far로 결정되는 상수) 형태이므로, 이 시점까지 z_clip은 뷰 공간 z에 대해 선형입니다.

비선형성은 원근 나눗셈 단계에서 생깁니다. z_ndc = z_clip / w에서 w(카메라로부터의 거리)가 분모에 들어가기 때문에, 카메라 가까이에서는 1m 차이가 NDC z값을 크게 바꾸지만 먼 곳에서는 같은 1m 차이가 NDC z값을 거의 바꾸지 못합니다. 깊이 정밀도가 카메라 근처에 편중되는 이 비선형 분포가, 뒤에서 다룰 Z-fighting의 원인입니다.

<br>

**네 번째 행 — w 복사 `(0, 0, -1, 0)`** : 원근 나눗셈의 분모가 될 w를 준비하는 행입니다. 네 번째 행과 입력 좌표 (x, y, z, 1)의 내적은 0·x + 0·y + (-1)·z + 0·1 = -z_view이므로, 뷰 공간에서 카메라로부터의 거리가 그대로 w에 들어갑니다(부호는 API 관례에 따라 다름). GPU는 이후 x, y, z 각각을 이 w로 나누어 NDC 좌표를 생성합니다.

<br>

w 나눗셈이 원근감을 만드는 과정을 구체적인 수치로 확인할 수 있습니다.

```
뷰 공간의 두 점:
  A = (1, 1, -5, 1)    카메라에서 5m 앞
  B = (1, 1, -20, 1)   카메라에서 20m 앞

투영 행렬 적용 후 (간략화):
  A_clip = (s·1, s·1, z_a, 5)    w = 5
  B_clip = (s·1, s·1, z_b, 20)   w = 20

원근 나눗셈 (w로 나누기):
  A_ndc = (s/5,  s/5,  ...)    x, y 비교적 큼
  B_ndc = (s/20, s/20, ...)    x, y 비교적 작음

  → A는 화면에서 크게, B는 화면에서 작게 표시됨
```

w가 5인 A는 나눈 뒤에도 x, y가 크게 남고, w가 20인 B는 나눈 뒤 x, y가 1/4로 줄어듭니다. 뷰 공간에서 동일한 (1, 1) 좌표였던 두 점이, 카메라까지의 거리 차이만으로 화면에서 서로 다른 크기로 그려집니다. 원근감은 이 w 나눗셈 한 단계에서 만들어집니다.

---

## 직교 투영

직교 투영(Orthographic Projection)은 원근감이 없는 **평행 투영**입니다.

카메라로부터의 거리와 관계없이 오브젝트의 크기가 동일하게 표현됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 375" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Titles -->
  <text fill="currentColor" x="140" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">원근 투영</text>
  <text fill="currentColor" x="420" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">직교 투영</text>
  <!-- ═══ Left: Perspective ═══ -->
  <g transform="translate(25, 130)">
    <!-- Frustum fill & edges -->
    <polygon points="0,0 210,-84 210,84" fill="currentColor" fill-opacity="0.04" stroke="none"/>
    <line x1="0" y1="0" x2="210" y2="-84" stroke="currentColor" stroke-width="1.5"/>
    <line x1="0" y1="0" x2="210" y2="84" stroke="currentColor" stroke-width="1.5"/>
    <line x1="210" y1="-84" x2="210" y2="84" stroke="currentColor" stroke-width="1.8"/>
    <!-- Center axis -->
    <line x1="0" y1="0" x2="210" y2="0" stroke="currentColor" stroke-dasharray="5,4" stroke-width="0.7" opacity="0.2"/>
    <!-- Camera -->
    <circle cx="0" cy="0" r="4" fill="currentColor"/>
    <text fill="currentColor" x="0" y="22" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">카메라</text>
    <!-- Object A at (80, -15), r=9 — offset above axis -->
    <circle cx="80" cy="-15" r="9" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.12"/>
    <text fill="currentColor" x="80" y="-11" text-anchor="middle" font-size="10" font-family="sans-serif">A</text>
    <!-- Object B at (170, 18), r=9 — offset below axis, same real size -->
    <circle cx="170" cy="18" r="9" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.12"/>
    <text fill="currentColor" x="170" y="22" text-anchor="middle" font-size="10" font-family="sans-serif">B</text>
    <!-- Projection lines: camera → A edges → far plane (converging) -->
    <!-- A top: (80,-24) → far plane y = -24×(210/80) = -63 -->
    <!-- A bottom: (80,-6) → far plane y = -6×(210/80) = -15.75 -->
    <line x1="0" y1="0" x2="210" y2="-63" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <line x1="0" y1="0" x2="210" y2="-15.75" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <!-- Projection lines: camera → B edges → far plane -->
    <!-- B top: (170,9) → far plane y = 9×(210/170) = 11.1 -->
    <!-- B bottom: (170,27) → far plane y = 27×(210/170) = 33.4 -->
    <line x1="0" y1="0" x2="210" y2="11.1" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <line x1="0" y1="0" x2="210" y2="33.4" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <!-- Projected sizes on far plane -->
    <!-- A': span = 63 - 15.75 = 47.25 -->
    <line x1="213" y1="-63" x2="213" y2="-15.75" stroke="currentColor" stroke-width="3.5" opacity="0.4"/>
    <!-- B': span = 33.4 - 11.1 = 22.3 -->
    <line x1="213" y1="11.1" x2="213" y2="33.4" stroke="currentColor" stroke-width="3.5" opacity="0.4"/>
    <!-- Labels -->
    <text fill="currentColor" x="226" y="-36" font-size="9" font-family="sans-serif" opacity="0.5">A' (크게)</text>
    <text fill="currentColor" x="226" y="26" font-size="9" font-family="sans-serif" opacity="0.5">B' (작게)</text>
  </g>
  <!-- Perspective caption -->
  <text fill="currentColor" x="140" y="237" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">A, B는 같은 크기 · 투영선이 카메라에서 수렴</text>
  <text fill="currentColor" x="140" y="252" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">→ 가까운 A가 더 크게 투영됨</text>
  <!-- ═══ Right: Orthographic ═══ -->
  <g transform="translate(310, 130)">
    <!-- Rectangle view volume -->
    <rect x="0" y="-70" width="210" height="140" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
    <line x1="210" y1="-70" x2="210" y2="70" stroke="currentColor" stroke-width="1.8"/>
    <!-- Camera -->
    <circle cx="-18" cy="0" r="4" fill="currentColor"/>
    <line x1="-14" y1="0" x2="0" y2="0" stroke="currentColor" stroke-dasharray="3,2" stroke-width="0.8" opacity="0.3"/>
    <text fill="currentColor" x="-18" y="22" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">카메라</text>
    <!-- Object A at (55, -15), r=9 — same offset as perspective -->
    <circle cx="55" cy="-15" r="9" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.12"/>
    <text fill="currentColor" x="55" y="-11" text-anchor="middle" font-size="10" font-family="sans-serif">A</text>
    <!-- Object B at (160, 18), r=9 — same real size, same offset -->
    <circle cx="160" cy="18" r="9" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.12"/>
    <text fill="currentColor" x="160" y="22" text-anchor="middle" font-size="10" font-family="sans-serif">B</text>
    <!-- Parallel projection lines from A edges (horizontal) -->
    <line x1="55" y1="-24" x2="210" y2="-24" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <line x1="55" y1="-6" x2="210" y2="-6" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <!-- Parallel projection lines from B edges (horizontal) -->
    <line x1="160" y1="9" x2="210" y2="9" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <line x1="160" y1="27" x2="210" y2="27" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.25"/>
    <!-- Projected sizes on right edge — both same span (18) -->
    <line x1="213" y1="-24" x2="213" y2="-6" stroke="currentColor" stroke-width="3.5" opacity="0.4"/>
    <line x1="213" y1="9" x2="213" y2="27" stroke="currentColor" stroke-width="3.5" opacity="0.4"/>
    <!-- Labels -->
    <text fill="currentColor" x="226" y="-11" font-size="9" font-family="sans-serif" opacity="0.5">A'</text>
    <text fill="currentColor" x="234" y="8" font-size="8" font-family="sans-serif" opacity="0.35">같은</text>
    <text fill="currentColor" x="234" y="17" font-size="8" font-family="sans-serif" opacity="0.35">크기</text>
    <text fill="currentColor" x="226" y="30" font-size="9" font-family="sans-serif" opacity="0.5">B'</text>
  </g>
  <!-- Orthographic caption -->
  <text fill="currentColor" x="420" y="237" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">A, B는 같은 크기 · 투영선이 평행</text>
  <text fill="currentColor" x="420" y="252" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">→ 거리와 무관하게 같은 크기로 투영됨</text>
  <!-- ═══ Bottom: Screen results ═══ -->
  <line x1="30" y1="268" x2="250" y2="268" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <line x1="310" y1="268" x2="530" y2="268" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <text fill="currentColor" x="140" y="285" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.4">카메라에서 바라본 결과</text>
  <text fill="currentColor" x="420" y="285" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.4">카메라에서 바라본 결과</text>
  <!-- Perspective result: A large, B small (ratio ≈ 2.1:1) -->
  <circle cx="100" cy="325" r="20" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="100" y="329" text-anchor="middle" font-size="12" font-family="sans-serif">A</text>
  <circle cx="190" cy="325" r="9" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="190" y="329" text-anchor="middle" font-size="9" font-family="sans-serif">B</text>
  <text fill="currentColor" x="140" y="362" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">가까운 A는 크게, 먼 B는 작게</text>
  <!-- Orthographic result: A and B same size -->
  <circle cx="385" cy="325" r="14" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="385" y="329" text-anchor="middle" font-size="11" font-family="sans-serif">A</text>
  <circle cx="460" cy="325" r="14" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="460" y="329" text-anchor="middle" font-size="11" font-family="sans-serif">B</text>
  <text fill="currentColor" x="420" y="362" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">거리와 무관하게 동일 크기</text>
</svg>
</div>

<br>

직교 투영의 시야 영역은 절두체가 아니라 **직육면체**입니다. 원근 투영에서는 시야 영역이 카메라에서 멀어질수록 넓어지는 절두체였지만, 직교 투영에서는 모든 거리에서 시야 영역의 폭과 높이가 동일합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <rect x="100" y="25" width="300" height="100" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.8" rx="2"/>
  <circle cx="45" cy="75" r="5" fill="currentColor"/>
  <line x1="50" y1="75" x2="100" y2="75" stroke="currentColor" stroke-dasharray="4,3" stroke-width="1" opacity="0.4"/>
  <text fill="currentColor" x="45" y="97" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">카메라</text>
  <text fill="currentColor" x="250" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.35">모든 거리에서 동일한 폭/높이</text>
  <text fill="currentColor" x="100" y="148" text-anchor="middle" font-size="10" font-family="sans-serif">Near Plane</text>
  <text fill="currentColor" x="400" y="148" text-anchor="middle" font-size="10" font-family="sans-serif">Far Plane</text>
  <!-- n distance -->
  <line x1="45" y1="165" x2="100" y2="165" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="45" y1="161" x2="45" y2="169" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="100" y1="161" x2="100" y2="169" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="72" y="178" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">n</text>
  <!-- f distance -->
  <line x1="45" y1="188" x2="400" y2="188" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="45" y1="184" x2="45" y2="192" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="400" y1="184" x2="400" y2="192" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="222" y="200" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">f</text>
</svg>
</div>

직교 투영 행렬은 원근 투영 행렬보다 구조가 간단합니다. 원근감을 만들 필요가 없으므로 w 성분을 건드리지 않고, x, y, z를 스케일과 오프셋만으로 정해진 범위에 매핑합니다.

$$
P_{\text{ortho}} = \begin{bmatrix} \frac{2}{r - l} & 0 & 0 & -\frac{r + l}{r - l} \\ 0 & \frac{2}{t - b} & 0 & -\frac{t + b}{t - b} \\ 0 & 0 & \frac{-1}{f - n} & -\frac{n}{f - n} \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

$$l, r$$ = 왼쪽, 오른쪽 경계, $$b, t$$ = 아래, 위 경계, $$n, f$$ = near, far plane

(그래픽스 API에 따라 부호와 배치가 다를 수 있음)

<br>

원근 투영 행렬과의 핵심 차이는 **네 번째 행**에 있습니다.

원근 투영에서는 네 번째 행 `(0, 0, -1, 0)`이 뷰 공간의 z를 w에 복사하여 원근 나눗셈의 분모를 만들었지만, 직교 투영에서는 네 번째 행이 `(0, 0, 0, 1)`이므로 w가 항상 1로 유지됩니다.

<br>

원근 투영에서 원근감이 생기는 이유는 각 정점의 w가 카메라로부터의 거리에 비례하여 **정점마다 다른 값**을 갖기 때문입니다. 가까운 정점은 w가 작아 x/w, y/w 결과가 크고, 먼 정점은 w가 커서 결과가 작습니다. 같은 크기의 오브젝트라도 거리에 따라 화면에서 다른 크기로 보이는 것이 이 원리입니다.

직교 투영에서는 w가 거리와 무관하게 항상 1이므로, 원근 나눗셈이 x/1 = x, y/1 = y가 됩니다. 거리가 다른 두 정점이라도 나눗셈의 분모가 동일하기 때문에 x, y 좌표가 거리에 의해 변하지 않고, 같은 크기의 오브젝트는 카메라로부터의 거리와 무관하게 화면에서 동일한 크기로 표시됩니다.

<br>

직교 투영은 거리에 따른 크기 변화가 없어야 하는 상황에서 사용됩니다. 2D 게임에서는 모든 오브젝트가 카메라 거리와 무관하게 지정된 크기로 표시되어야 하고, UI 요소는 화면에 고정된 픽셀 크기로 렌더링되어야 합니다. 미니맵이나 탑다운 전략 게임에서도 거리에 따른 크기 왜곡 없이 정확한 비율이 유지되어야 합니다.

---

## 깊이 값의 비선형성

원근 나눗셈이 z(깊이)에도 적용되면서, NDC의 z값은 뷰 공간에서의 실제 거리와 **비선형(non-linear)** 관계를 갖게 됩니다.

앞서 투영 행렬의 세 번째 행을 다룰 때 이 비선형성을 간략히 언급했는데, 이 섹션에서는 변환 공식과 구체적 수치를 통해 비선형 분포가 깊이 버퍼 정밀도에 어떤 영향을 미치는지 정량적으로 살펴봅니다.

<br>

뷰 공간에서 카메라로부터의 거리를 d라 하면, NDC의 깊이값 z_ndc는 다음 공식으로 결정됩니다 (DirectX 관례, $$[0, 1]$$ 범위).

$$
z_{\text{ndc}} = \frac{f}{f - n} - \frac{f \cdot n}{(f - n) \cdot d}
$$

$$n$$ = near plane 거리, $$f$$ = far plane 거리, $$d$$ = 뷰 공간에서의 실제 거리 ($$n \leq d \leq f$$)

$$d = n \;\Rightarrow\; z_{\text{ndc}} = 0$$ (가장 가까움), $$d = f \;\Rightarrow\; z_{\text{ndc}} = 1$$ (가장 멀음)

공식의 두 번째 항 $$\frac{f \cdot n}{(f - n) \cdot d}$$에서 d가 분모에 있으므로, z_ndc는 1/d에 비례하는 성분을 포함합니다.

d가 작을 때(카메라에 가까울 때) z_ndc의 변화율이 크고, d가 클 때(카메라에서 멀 때) 변화율이 급격히 작아집니다.

<br>

아래 그래프는 n=0.3, f=1000일 때 d에 따른 z_ndc의 변화를 보여줍니다. 가로축이 로그 스케일임에도 곡선이 near 근처에서 급경사를 이루고, far 쪽에서는 거의 수평에 가깝습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Y axis -->
  <line x1="55" y1="230" x2="55" y2="22" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="55,20 51,28 59,28" fill="currentColor"/>
  <!-- X axis -->
  <line x1="55" y1="230" x2="425" y2="230" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="427,230 419,226 419,234" fill="currentColor"/>
  <!-- Horizontal gridlines -->
  <line x1="55" y1="190" x2="420" y2="190" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="150" x2="420" y2="150" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="110" x2="420" y2="110" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="70" x2="420" y2="70" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="30" x2="420" y2="30" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <!-- Vertical gridlines at log ticks -->
  <line x1="55" y1="230" x2="55" y2="30" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="157" y1="230" x2="157" y2="30" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="259" y1="230" x2="259" y2="30" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="362" y1="230" x2="362" y2="30" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <!-- Y labels -->
  <text fill="currentColor" x="48" y="234" text-anchor="end" font-size="10" font-family="sans-serif">0.0</text>
  <text fill="currentColor" x="48" y="194" text-anchor="end" font-size="10" font-family="sans-serif">0.2</text>
  <text fill="currentColor" x="48" y="154" text-anchor="end" font-size="10" font-family="sans-serif">0.4</text>
  <text fill="currentColor" x="48" y="114" text-anchor="end" font-size="10" font-family="sans-serif">0.6</text>
  <text fill="currentColor" x="48" y="74" text-anchor="end" font-size="10" font-family="sans-serif">0.8</text>
  <text fill="currentColor" x="48" y="34" text-anchor="end" font-size="10" font-family="sans-serif">1.0</text>
  <!-- X tick marks and labels (log scale) -->
  <line x1="55" y1="230" x2="55" y2="235" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="55" y="248" text-anchor="middle" font-size="10" font-family="sans-serif">0.3</text>
  <text fill="currentColor" x="55" y="260" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">near</text>
  <line x1="157" y1="230" x2="157" y2="235" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="157" y="248" text-anchor="middle" font-size="10" font-family="sans-serif">1</text>
  <line x1="199" y1="230" x2="199" y2="234" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="199" y="247" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">3</text>
  <line x1="259" y1="230" x2="259" y2="235" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="259" y="248" text-anchor="middle" font-size="10" font-family="sans-serif">10</text>
  <line x1="308" y1="230" x2="308" y2="234" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="308" y="247" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">30</text>
  <line x1="362" y1="230" x2="362" y2="235" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="362" y="248" text-anchor="middle" font-size="10" font-family="sans-serif">100</text>
  <line x1="420" y1="230" x2="420" y2="235" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="420" y="248" text-anchor="middle" font-size="10" font-family="sans-serif">1000</text>
  <text fill="currentColor" x="420" y="260" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">far</text>
  <!-- Axis titles -->
  <text fill="currentColor" x="14" y="130" text-anchor="middle" font-size="11" font-family="sans-serif" transform="rotate(-90,14,130)">z_ndc</text>
  <text fill="currentColor" x="237" y="280" text-anchor="middle" font-size="11" font-family="sans-serif">실제 거리 d (로그 스케일)</text>
  <!-- Curve: z_ndc = f/(f-n) - fn/((f-n)*d), n=0.3, f=1000 -->
  <!-- x_pos = 55 + (log10(d) - log10(0.3)) / (log10(1000) - log10(0.3)) * 365 -->
  <!-- y_pos = 230 - z_ndc * 200 -->
  <polyline points="55,230 66,197 78,168 90,146 101,130 108,120 120,106 131,96 139,89 148,83 157,78 170,71 182,65 194,61 199,59 211,55 224,51 237,48 247,46 259,43 273,41 286,39 299,38 308,37 316,36 328,35 338,34.5 349,34 362,33.2 374,32.6 386,32.2 399,31.7 407,31.4 420,30.8" stroke="currentColor" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <!-- Shaded region: near precision zone -->
  <rect x="55" y="28" width="102" height="204" fill="currentColor" opacity="0.04" rx="2"/>
  <!-- Annotations -->
  <line x1="88" y1="185" x2="78" y2="168" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <text fill="currentColor" x="92" y="190" font-size="9.5" font-family="sans-serif" opacity="0.6">near 근처: 급격한 변화</text>
  <text fill="currentColor" x="92" y="203" font-size="9.5" font-family="sans-serif" opacity="0.6">→ 높은 정밀도</text>
  <text fill="currentColor" x="280" y="55" font-size="9.5" font-family="sans-serif" opacity="0.6">far 근처: 완만한 변화</text>
  <text fill="currentColor" x="280" y="67" font-size="9.5" font-family="sans-serif" opacity="0.6">→ 낮은 정밀도</text>
  <line x1="340" y1="49" x2="330" y2="35" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
</svg>
</div>

<br>

24비트 정수 깊이 버퍼는 NDC의 $$[0, 1]$$ 범위를 균일한 간격의 정수 단계로 나눕니다. 균일한 간격이므로, 어떤 거리 구간이 NDC 범위에서 차지하는 비율만큼 깊이 버퍼의 정수 단계도 배분됩니다. 그런데 비선형 변환 때문에 NDC 범위 대부분이 near 근처의 좁은 거리 구간에 몰리므로, **깊이 버퍼의 정수 단계도 near 근처에 집중되고 far 근처에는 거의 배분되지 않습니다.**

아래 표는 near = 0.1, far = 1000인 경우의 구체적인 분포입니다 (그래프와 near 값이 다른 점에 주의).

```
깊이 정밀도 분포 예시 (near=0.1, far=1000)

  뷰 공간 거리 범위       NDC 깊이 범위      깊이 버퍼의 비율
  ────────────────────────────────────────────────────────
  0.1  ~  1.0  (근거리)    0.0 ~ 0.90         약 90%
  1.0  ~  10   (중거리)    0.90 ~ 0.99        약 9%
  10   ~ 1000  (원거리)    0.99 ~ 1.0         약 1%
  ────────────────────────────────────────────────────────

  → 깊이 버퍼 정밀도의 90%가 카메라에서 1미터 이내에 집중
  → 10미터 ~ 1000미터 구간에는 정밀도의 1%만 배분
```

24비트 깊이 버퍼의 총 단계 수는 $$2^{24}$$ = 16,777,216입니다. 위 표에서 NDC 범위의 약 90%가 카메라에서 1미터 이내에 집중되므로, 약 1,510만 단계가 이 좁은 구간에 사용됩니다. 반면 10미터에서 1,000미터까지의 넓은 구간에는 약 17만 단계만 남습니다. 이 불균형이 원거리에서의 깊이 정밀도 부족을 만듭니다.

---

## Z-fighting

이 정밀도 부족이 실제 렌더링에서 일으키는 문제가 **Z-fighting**입니다. 거의 같은 깊이에 있는 두 표면의 깊이 값이 구분되지 않아, 어느 표면이 앞인지 판정할 수 없게 됩니다.

**양자화(quantization)**는 연속적인 깊이 값을 정해진 비트 수의 정수로 변환하는 과정입니다. 깊이 버퍼는 이 양자화를 통해 깊이를 저장합니다. 24비트 깊이 버퍼라면 16,777,216개의 정수 단계로 깊이를 표현합니다. 원거리에서 정밀도가 부족하면, 서로 다른 두 깊이 값이 양자화 과정에서 같은 정수로 변환됩니다.

```
Z-fighting 현상

  카메라에서 먼 거리에 있는 두 표면:
    표면 A: 뷰 공간 깊이 = 500.0
    표면 B: 뷰 공간 깊이 = 500.1 (0.1 차이)

  깊이 버퍼 (24비트) 값:
    표면 A: 0.999899990...  →  양자화 후  16775537
    표면 B: 0.999900030...  →  양자화 후  16775537  (같은 값!)

  → 두 표면의 깊이 값이 같아져 버림
  → 어느 표면이 앞인지 판단 불가
```

GPU는 각 픽셀을 그릴 때 깊이 테스트(depth test)를 수행합니다. 새로 그리려는 픽셀의 깊이 값과 깊이 버퍼에 이미 저장된 값을 비교하여, 더 가까운 쪽만 화면에 남기는 과정입니다. 두 표면의 양자화된 깊이 값이 동일하면, 이 비교에서 앞뒤를 가릴 수 없습니다.

이때 어느 표면이 남는지는 GPU가 삼각형을 처리하는 순서에 따라 달라지는데, 이 순서는 프레임마다 카메라 위치, 컬링 결과, 드라이버의 내부 스케줄링 등에 의해 미세하게 바뀔 수 있습니다.

같은 픽셀 안에서도 부동소수점 보간의 미세한 차이로 인해 인접 픽셀끼리 다른 표면이 선택되기도 합니다.

그 결과 두 표면이 프레임마다, 픽셀마다 번갈아 나타나며 화면이 깜빡입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 490 175" xmlns="http://www.w3.org/2000/svg" style="max-width: 490px; width: 100%;">
  <!-- ═══ Left: Normal rendering ═══ -->
  <text fill="currentColor" x="115" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">정상 렌더링</text>
  <!-- Surface B (behind — drawn first, offset right+down to peek out) -->
  <rect x="55" y="43" width="150" height="88" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="1" stroke-opacity="0.35" rx="2"/>
  <!-- Surface A (in front — drawn on top, covers most of B) -->
  <rect x="30" y="28" width="150" height="88" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1" rx="2"/>
  <text fill="currentColor" x="105" y="70" text-anchor="middle" font-size="11" font-family="sans-serif">표면 A</text>
  <text fill="currentColor" x="105" y="84" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.4">(A가 앞 → A만 보임)</text>
  <!-- B label on exposed bottom strip -->
  <text fill="currentColor" x="130" y="127" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">표면 B (뒤)</text>
  <!-- Caption -->
  <text fill="currentColor" x="115" y="150" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">깊이 값이 구분됨</text>
  <text fill="currentColor" x="115" y="164" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">→ 앞 표면만 안정적으로 표시</text>
  <!-- ═══ Right: Z-fighting ═══ -->
  <text fill="currentColor" x="345" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">Z-fighting 발생</text>
  <!-- Grid base (same 150×88 as left surfaces) -->
  <rect x="270" y="28" width="150" height="88" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.8" rx="2"/>
  <!-- Grid lines (5 cols × 4 rows, cell = 30×22) -->
  <line x1="300" y1="28" x2="300" y2="116" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="330" y1="28" x2="330" y2="116" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="360" y1="28" x2="360" y2="116" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="390" y1="28" x2="390" y2="116" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="270" y1="50" x2="420" y2="50" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="270" y1="72" x2="420" y2="72" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="270" y1="94" x2="420" y2="94" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <!-- B cells (darker overlay) — 무작위 패턴 -->
  <!-- Row 0: _B_B_ -->
  <rect x="300" y="28" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <rect x="360" y="28" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <!-- Row 1: B_B_B -->
  <rect x="270" y="50" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <rect x="330" y="50" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <rect x="390" y="50" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <!-- Row 2: _BB__ -->
  <rect x="300" y="72" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <rect x="330" y="72" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <!-- Row 3: B__BB -->
  <rect x="270" y="94" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <rect x="360" y="94" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <rect x="390" y="94" width="30" height="22" fill="currentColor" fill-opacity="0.30"/>
  <!-- Legend -->
  <rect x="430" y="38" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.25"/>
  <text fill="currentColor" x="446" y="49" font-size="9" font-family="sans-serif" opacity="0.5">표면 A</text>
  <rect x="430" y="56" width="12" height="12" fill="currentColor" fill-opacity="0.38" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.25"/>
  <text fill="currentColor" x="446" y="67" font-size="9" font-family="sans-serif" opacity="0.5">표면 B</text>
  <!-- Caption -->
  <text fill="currentColor" x="345" y="150" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">같은 깊이 값 → 픽셀마다 A/B 무작위 결정</text>
  <text fill="currentColor" x="345" y="164" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">매 프레임 패턴이 바뀌어 깜빡거림</text>
</svg>
</div>

<br>

Z-fighting이 발생하기 쉬운 대표적인 상황은 세 가지입니다.

카메라에서 먼 거리에 있는 두 표면은 Z-fighting에 취약합니다. 앞서 살펴본 것처럼, 원근 투영의 비선형성 때문에 깊이 버퍼의 정수 단계 대부분이 near 근처에 집중됩니다. 원거리에 배분되는 단계 수가 적으므로, 가까운 곳에서는 구분되던 거리 차이가 먼 곳에서는 같은 정수 단계로 양자화됩니다.

같은 위치에 겹쳐 배치된 면도 Z-fighting을 일으킵니다. 데칼(바닥에 붙은 혈흔, 타이어 자국 등)이나 코플래너(coplanar, 같은 평면 위에 놓인) 면은 두 표면 사이의 물리적 간격이 거의 없습니다. 물리적 간격이 없으면 깊이 값 자체가 동일하거나 한 단계 이내의 차이만 남으므로, 깊이 정밀도와 무관하게 기하학적으로 구분이 불가능합니다.

near 평면 값이 지나치게 작거나 far 평면 값이 지나치게 큰 경우에도 Z-fighting 가능성이 높아집니다. near 값이 0에 가까워질수록 $$1/d$$ 곡선의 급변 구간이 확장되어, 깊이 버퍼 단계가 극단적으로 near 쪽에 편중됩니다. far 값이 커지면 이미 단계가 부족한 원거리 구간이 더 넓어져, 한 단계당 커버하는 실제 거리가 길어집니다. 이 두 조건은 각각 독립적으로 정밀도를 악화시키며, 동시에 해당하면 효과가 중첩됩니다.

---

### Near/Far 평면 설정의 중요성

깊이 정밀도 부족으로 인한 Z-fighting을 줄이는 가장 직접적인 방법은 **near 평면을 카메라에서 가능한 한 멀리, far 평면을 가능한 한 가까이** 설정하는 것입니다.

```
near, far 설정에 따른 정밀도 변화

  설정 1: near=0.01, far=10000
  ──────────────────────────────────────────────
  → near가 0에 매우 가까워 깊이 단계가 극단적으로 near 쪽에 편중
  → far가 커서 정밀도가 부족한 원거리 구간이 넓음
  → Z-fighting 빈번

  설정 2: near=0.1, far=1000
  ──────────────────────────────────────────────
  → near가 0에서 멀어져 편중이 크게 완화
  → far가 줄어 원거리 구간이 좁아짐
  → 원거리 Z-fighting 감소

  설정 3: near=0.5, far=500
  ──────────────────────────────────────────────
  → near가 0에서 충분히 떨어져 편중이 적음
  → far가 작아 깊이 범위 전체가 좁음
  → Z-fighting 거의 발생하지 않음
```

near를 0에서 멀리 놓을수록 $1/d$ 곡선의 급변 구간이 줄어들고, far를 줄일수록 정밀도가 부족한 원거리 구간이 좁아집니다. 게임에서 카메라 바로 앞 0.01미터까지 렌더링해야 하는 경우는 드물기 때문에, near를 0.1~1.0 수준으로 설정하는 것이 일반적입니다.

<br>

far 평면도 실제로 필요한 거리까지만 설정해야 합니다. 오픈 월드 게임에서 먼 곳까지 대비하여 far를 100,000으로 설정하면, 대부분의 깊이 정밀도가 가까운 곳에 몰려서 중거리 이후의 모든 오브젝트가 Z-fighting에 노출됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="220" y="18" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">near/far 설정 가이드</text>
  <!-- Header row -->
  <rect x="20" y="30" width="160" height="28" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3" rx="2"/>
  <rect x="180" y="30" width="120" height="28" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3" rx="2"/>
  <rect x="300" y="30" width="120" height="28" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3" rx="2"/>
  <text fill="currentColor" x="100" y="49" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">게임 유형</text>
  <text fill="currentColor" x="240" y="49" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">near 권장</text>
  <text fill="currentColor" x="360" y="49" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">far 권장</text>
  <!-- Row 1 -->
  <rect x="20" y="58" width="160" height="28" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="180" y="58" width="120" height="28" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="300" y="58" width="120" height="28" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <text fill="currentColor" x="100" y="77" text-anchor="middle" font-size="10" font-family="sans-serif">1인칭 슈팅</text>
  <text fill="currentColor" x="240" y="77" text-anchor="middle" font-size="10" font-family="sans-serif">0.1 ~ 0.3</text>
  <text fill="currentColor" x="360" y="77" text-anchor="middle" font-size="10" font-family="sans-serif">500 ~ 1000</text>
  <!-- Row 2 -->
  <rect x="20" y="86" width="160" height="28" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="180" y="86" width="120" height="28" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="300" y="86" width="120" height="28" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <text fill="currentColor" x="100" y="105" text-anchor="middle" font-size="10" font-family="sans-serif">3인칭 액션</text>
  <text fill="currentColor" x="240" y="105" text-anchor="middle" font-size="10" font-family="sans-serif">0.3 ~ 1.0</text>
  <text fill="currentColor" x="360" y="105" text-anchor="middle" font-size="10" font-family="sans-serif">300 ~ 800</text>
  <!-- Row 3 -->
  <rect x="20" y="114" width="160" height="28" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="180" y="114" width="120" height="28" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="300" y="114" width="120" height="28" fill="none" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <text fill="currentColor" x="100" y="133" text-anchor="middle" font-size="10" font-family="sans-serif">탑다운 전략</text>
  <text fill="currentColor" x="240" y="133" text-anchor="middle" font-size="10" font-family="sans-serif">1.0 ~ 5.0</text>
  <text fill="currentColor" x="360" y="133" text-anchor="middle" font-size="10" font-family="sans-serif">200 ~ 500</text>
  <!-- Row 4 -->
  <rect x="20" y="142" width="160" height="28" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="180" y="142" width="120" height="28" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <rect x="300" y="142" width="120" height="28" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <text fill="currentColor" x="100" y="161" text-anchor="middle" font-size="10" font-family="sans-serif">모바일 캐주얼</text>
  <text fill="currentColor" x="240" y="161" text-anchor="middle" font-size="10" font-family="sans-serif">0.1 ~ 0.5</text>
  <text fill="currentColor" x="360" y="161" text-anchor="middle" font-size="10" font-family="sans-serif">100 ~ 300</text>
  <!-- Footer -->
  <text fill="currentColor" x="220" y="193" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">원칙: near는 카메라에서 가능한 한 멀리, far는 가능한 한 가까이</text>
</svg>
</div>

---

## Reversed-Z

near/far 비율을 줄이는 것이 Z-fighting 완화의 기본 전략이지만, 근본적인 해결책은 아닙니다.

near/far 비율을 아무리 줄여도 원근 투영 자체의 수학적 구조가 깊이 정밀도의 편향을 만들기 때문입니다.

이 편향을 구조적으로 개선하는 기법이 **Reversed-Z**입니다.

### 부동소수점의 정밀도 특성

Reversed-Z의 원리를 이해하려면 먼저 **부동소수점(floating-point)** 숫자의 정밀도 분포를 알아야 합니다. IEEE 754 부동소수점 표준에서 32비트 float의 정밀도는 **0에 가까울수록 높고, 1에 가까울수록 낮습니다**.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 110" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text fill="currentColor" x="240" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">32비트 float에서 구분 가능한 값의 분포</text>
  <!-- Number line -->
  <line x1="50" y1="45" x2="430" y2="45" stroke="currentColor" stroke-width="1.2"/>
  <!-- Tick marks — each tick represents a representable float value -->
  <!-- Spacing increases roughly ×1.13 per step: dense near 0, sparse near 1 -->
  <line x1="50" y1="30" x2="50" y2="60" stroke="currentColor" stroke-width="1.2"/>
  <line x1="53" y1="33" x2="53" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="56" y1="33" x2="56" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="60" y1="33" x2="60" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="64" y1="33" x2="64" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="69" y1="33" x2="69" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="74" y1="33" x2="74" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="80" y1="33" x2="80" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="87" y1="33" x2="87" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="95" y1="33" x2="95" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="104" y1="33" x2="104" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="114" y1="33" x2="114" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="126" y1="33" x2="126" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="139" y1="33" x2="139" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="154" y1="33" x2="154" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="171" y1="33" x2="171" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="190" y1="33" x2="190" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="212" y1="33" x2="212" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="237" y1="33" x2="237" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="266" y1="33" x2="266" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="299" y1="33" x2="299" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="337" y1="33" x2="337" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="381" y1="33" x2="381" y2="57" stroke="currentColor" stroke-width="0.8" opacity="0.7"/>
  <line x1="430" y1="30" x2="430" y2="60" stroke="currentColor" stroke-width="1.2"/>
  <!-- Labels -->
  <text fill="currentColor" x="50" y="75" text-anchor="middle" font-size="11" font-family="sans-serif">0.0</text>
  <text fill="currentColor" x="430" y="75" text-anchor="middle" font-size="11" font-family="sans-serif">1.0</text>
  <!-- Annotations -->
  <text fill="currentColor" x="120" y="97" font-size="10" font-family="sans-serif" opacity="0.6">← 정밀도 높음 (촘촘)</text>
  <text fill="currentColor" x="320" y="97" font-size="10" font-family="sans-serif" opacity="0.6">정밀도 낮음 (듬성듬성) →</text>
</svg>
</div>

이 특성은 부동소수점의 표현 방식(부호 + 지수 + 가수)에서 비롯됩니다.

부동소수점은 과학적 표기법처럼 "1.xxxx x 2^n" 형태로 값을 저장하는데, 값이 작을수록 지수(n)가 작아지고, 지수가 작을수록 가수부의 각 비트가 표현하는 간격이 좁아집니다. 0에 가까울수록 구분 가능한 값이 촘촘하고, 1에 가까울수록 듬성듬성합니다.

이 부동소수점 정밀도 분포가 원근 투영의 깊이 분포와 겹치면서 문제가 심화됩니다.

```
기본 깊이 매핑 (near→NDC 0, far→NDC 1)

  NDC 깊이:  0 ────────────────────────────────── 1
  대응 거리: near plane ────────────────────── far plane

  원근 투영의 정밀도 분포:
  near 근처(0에 가까움): 깊이 변화가 큼 → 정밀도 높음
  far 근처(1에 가까움):  깊이 변화가 작음 → 정밀도 낮음

  부동소수점의 정밀도 분포:
  0 근처: 표현 가능한 값이 많음 → 정밀도 높음
  1 근처: 표현 가능한 값이 적음 → 정밀도 낮음

  → near 근처: 이미 정밀도가 높은 곳에 float 정밀도까지 높음 (과잉)
  → far 근처:  이미 정밀도가 낮은 곳에 float 정밀도까지 낮음 (부족)
```

<br>

기본 매핑에서는 near plane이 NDC 0에, far plane이 NDC 1에 대응합니다.

원근 투영의 비선형성은 near 근처에 깊이 값을 집중시키고, 부동소수점도 0 근처에 표현 가능한 값이 촘촘합니다.

두 분포가 같은 방향으로 겹치므로, near 근처에는 정밀도가 남아돌지만 far 근처에는 둘 다 희박하여 정밀도 부족이 심화됩니다.

---

### Reversed-Z의 원리

Reversed-Z는 깊이 매핑을 **뒤집어서** near plane에 NDC 1을, far plane에 NDC 0을 대응시킵니다. 기본 매핑에서 near가 NDC 0, far가 NDC 1이었다면, Reversed-Z에서는 near가 NDC 1, far가 NDC 0입니다.

이렇게 뒤집으면 원근 투영의 정밀도 분포와 부동소수점의 정밀도 분포가 **상보적으로** 작용합니다.

near 근처(NDC 1 근처)에서는 원근 투영이 정밀도를 집중시키지만 float는 1 근처에서 정밀도가 낮으므로, 한쪽의 과잉이 다른 쪽의 부족을 메웁니다.

far 근처(NDC 0 근처)에서는 반대로, 원근 투영의 정밀도는 낮지만 float가 0 근처에서 정밀도가 높아 이를 보상합니다.

두 정밀도 곡선이 겹치지 않고 교차하면서, 전체적으로 균일한 깊이 정밀도를 얻게 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- Y axis -->
  <line x1="55" y1="195" x2="55" y2="20" stroke="currentColor" stroke-width="1.2"/>
  <!-- X axis -->
  <line x1="55" y1="195" x2="420" y2="195" stroke="currentColor" stroke-width="1.2"/>
  <!-- Axis labels -->
  <text fill="currentColor" x="14" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" transform="rotate(-90,14,110)">정밀도</text>
  <text fill="currentColor" x="55" y="212" text-anchor="middle" font-size="10" font-family="sans-serif">near</text>
  <text fill="currentColor" x="415" y="212" text-anchor="middle" font-size="10" font-family="sans-serif">far</text>
  <text fill="currentColor" x="235" y="228" text-anchor="middle" font-size="11" font-family="sans-serif">거리</text>
  <!-- Perspective precision (declining): high at near, low at far -->
  <polyline points="55,30 65,42 80,58 100,78 120,95 145,112 175,130 210,148 250,162 290,172 330,178 370,182 415,185" stroke="currentColor" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
  <!-- Float precision in Reversed-Z (rising): low at near/NDC≈1, high at far/NDC≈0 -->
  <polyline points="55,185 65,173 80,157 100,137 120,120 145,103 175,85 210,67 250,53 290,43 330,37 370,33 415,30" stroke="currentColor" fill="none" stroke-width="1.8" stroke-dasharray="4,3" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
  <!-- Combined effective precision (≈ uniform) -->
  <line x1="55" y1="108" x2="415" y2="108" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
  <!-- Crossing point of two component curves -->
  <circle cx="138" cy="108" r="3.5" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="1"/>
  <!-- Curve labels -->
  <text fill="currentColor" x="95" y="47" font-size="10" font-family="sans-serif" opacity="0.6">원근 투영 정밀도</text>
  <text fill="currentColor" x="95" y="165" font-size="10" font-family="sans-serif" opacity="0.6">float 정밀도 (Reversed-Z)</text>
  <text fill="currentColor" x="275" y="95" font-size="11" font-family="sans-serif">결합 정밀도 ≈ 균일</text>
  <text fill="currentColor" x="158" y="96" font-size="9" font-family="sans-serif" opacity="0.5">교차</text>
  <!-- Bottom note -->
  <text fill="currentColor" x="240" y="245" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">두 정밀도 분포가 반대 방향 → 서로 상쇄하여 전 구간 균일</text>
</svg>
</div>

Reversed-Z의 효과는 깊이 버퍼의 형식에 따라 다릅니다.

정수형 깊이 버퍼(D24 등)에서는 정밀도 분포가 개선되지만 그 폭은 제한적입니다.

반면 부동소수점 깊이 버퍼(D32_FLOAT)에서는 효과가 극적입니다. 부동소수점은 0.0 근처에서 정밀도가 높고 1.0 근처에서 낮은데, Reversed-Z가 far를 0.0에, near를 1.0에 매핑하므로 원근 투영의 비선형 편향과 부동소수점의 정밀도 분포가 서로 상쇄되어 전 구간에서 정밀도가 크게 향상됩니다.

---

### Reversed-Z 적용 시 변경사항

Reversed-Z를 적용하려면 세 가지를 변경해야 합니다.

첫째, **투영 행렬의 깊이 매핑을 뒤집습니다**. 기본 매핑에서 near=0, far=1이던 것을 near=1, far=0으로 바꾸도록 투영 행렬의 세 번째 행(0-indexed row 2)을 수정합니다.

둘째, **깊이 테스트의 비교 방향을 뒤집습니다**. 깊이 테스트는 같은 픽셀에 여러 프래그먼트가 겹칠 때, 카메라에 더 가까운 프래그먼트를 남기는 역할을 합니다. 기본 매핑에서는 가까운 물체일수록 깊이 값이 작으므로 Less 비교(값이 작으면 통과)를 사용하지만, Reversed-Z에서는 가까운 물체일수록 깊이 값이 크므로 Greater 비교(값이 크면 통과)로 변경해야 합니다.

셋째, **깊이 버퍼의 클리어 값을 변경합니다**. 렌더링 시작 시 깊이 버퍼는 "가장 먼 거리"를 뜻하는 값으로 초기화됩니다. 기본 매핑에서 가장 먼 거리는 NDC 1이므로 클리어 값이 1.0이지만, Reversed-Z에서는 가장 먼 거리가 NDC 0이므로 클리어 값을 0.0으로 바꿔야 합니다.

---

### Unity에서의 Reversed-Z 지원

Unity는 그래픽스 API에 따라 Reversed-Z를 자동 적용합니다.

NDC 깊이 범위가 [0, 1]인 API(DirectX 11/12, Metal, Vulkan)에서는 기본 활성화되고, NDC 깊이 범위가 [-1, 1]인 OpenGL 계열에서는 적용되지 않습니다.

OpenGL은 깊이 범위의 중심이 0이므로, near→1 / far→0으로 뒤집는 Reversed-Z 기법을 그대로 적용할 수 없기 때문입니다.

| 그래픽스 API | NDC 깊이 | Reversed-Z | 비고 |
|---|---|---|---|
| DirectX 11 / 12 | [0, 1] | 적용 | Windows PC |
| Metal | [0, 1] | 적용 | iOS, macOS |
| Vulkan | [0, 1] | 적용 | Android, PC |
| OpenGL ES | [-1, 1] | 미적용 | 일부 Android |
| OpenGL | [-1, 1] | 미적용 | Linux 등 |

Reversed-Z가 활성화된 플랫폼에서는 Unity의 투영 행렬과 깊이 테스트가 이미 뒤집힌 매핑을 반영합니다.

`UnityObjectToClipPos()`로 클립 공간 좌표를 구하고 내장 깊이 테스트를 그대로 사용하면, 셰이더에서 별도 처리 없이 Reversed-Z가 동작합니다.

<br>

단, 깊이 버퍼를 **직접 읽거나 비교하는** 커스텀 셰이더에서는 깊이 값의 의미가 달라지는 점을 고려해야 합니다.

Reversed-Z 환경에서 깊이 값 0은 가장 먼 거리, 1은 가장 가까운 거리이므로, 기본 매핑(0=near, 1=far)을 가정한 계산은 near/far 판정이 반전됩니다.

Unity는 `UNITY_REVERSED_Z` 매크로를 제공하며, 이 매크로로 플랫폼별 분기를 처리할 수 있습니다.

모바일에서는 Vulkan이나 Metal을 사용하는 기기라면 Reversed-Z가 자동 적용되지만, OpenGL ES만 지원하는 구형 Android 기기에서는 Reversed-Z 없이 동작합니다. 이 경우 앞서 다룬 near/far 비율 관리가 깊이 정밀도 확보의 주요 수단이 됩니다.

---

## Unity 카메라의 투영 설정

원근 투영과 직교 투영은 Unity Camera 컴포넌트의 속성으로 직접 제어됩니다. 깊이 정밀도는 near/far 평면 설정을 통해 간접적으로 조절되고, Reversed-Z는 Unity가 플랫폼별로 자동 적용하므로 별도 속성은 없습니다.

| 속성 | 기본값 | 모드 | 설명 |
|---|---|---|---|
| Projection | — | — | Perspective / Orthographic 선택 |
| Field of View | 60 | Perspective | 세로 시야각 (도) |
| Size | 5 | Orthographic | 세로 절반 크기 (월드 단위) |
| Near Clip Plane | 0.3 | 공통 | near 평면 거리 |
| Far Clip Plane | 1000 | 공통 | far 평면 거리 |

**Camera.fieldOfView** 는 Perspective 모드에서의 세로 FOV를 도 단위로 지정하며, 기본값은 60도입니다. 스크립트에서 `camera.fieldOfView = 90f;` 처럼 동적으로 변경할 수 있고, 줌 인/아웃 효과나 대시 시 시야 확장 연출에 활용됩니다.

**Camera.orthographicSize** 는 Orthographic 모드에서 화면 세로 절반의 크기를 월드 단위로 지정합니다. Size가 5이면 화면의 세로 전체가 월드의 10단위를 표시합니다. 가로는 aspect ratio에 따라 자동 결정됩니다.

**Camera.nearClipPlane** 과 **Camera.farClipPlane** 은 near/far 평면 거리입니다. near 평면을 카메라에서 가능한 한 멀리, far 평면을 가능한 한 가까이 설정해야 깊이 정밀도를 확보할 수 있습니다. 기본값은 각각 0.3과 1000이며, 장면의 실제 필요 범위에 맞춰 조정하는 것이 좋습니다.

투영 모드 전환은 Camera 컴포넌트의 Projection 드롭다운 또는 스크립트에서 `camera.orthographic = true/false`로 제어합니다.

---

### projectionMatrix 직접 설정

`camera.projectionMatrix`에 커스텀 행렬을 대입하면 투영 행렬을 직접 지정할 수 있습니다. 비대칭 절두체(Oblique Frustum, 물 반사나 포털 렌더링에서 클리핑 평면을 기울여야 할 때), 비표준 FOV 구성, VR/AR 렌즈 왜곡 보정 등 기본 투영 설정만으로는 표현할 수 없는 경우에 사용됩니다.

이렇게 직접 설정한 투영 행렬은 Unity의 자동 조정(화면 비율 변경에 따른 aspect 갱신 등)을 무시합니다. 따라서 필요한 시점에만 사용하고, 이후 `camera.ResetProjectionMatrix()`를 호출하여 자동 계산 모드로 되돌리는 것이 일반적입니다.

<br>

모바일에서 투영 행렬을 직접 설정하는 경우는 드물지만, near/far 평면 값을 스크립트에서 동적으로 조정하는 것은 실용적입니다. 실내 장면에서는 far를 100으로 줄이고, 야외 장면에서는 500으로 늘리는 식으로, 장면 규모에 맞게 깊이 정밀도를 확보할 수 있습니다.

---

## 마무리

투영은 3D 공간을 2D 화면으로 변환하는 과정이며, 이 과정의 수학적 구조가 깊이 정밀도를 결정합니다.

<br>

- **원근 투영**은 절두체(near, far, FOV, aspect ratio)를 직육면체로 변환하고, w 성분으로 원근 나눗셈을 수행하여 원근감을 구현합니다. **직교 투영**은 거리에 따른 크기 변화가 없는 평행 투영이며, 2D 게임이나 UI 렌더링에 사용됩니다.
- 원근 투영 후 **깊이 값은 비선형**으로, near 근처에 정밀도가 집중되고 far 근처에는 부족합니다.
- **Z-fighting**은 이 정밀도 부족으로 두 표면이 번갈아 보이는 현상이며, near를 크게, far를 작게 설정하여 완화할 수 있습니다.
- **Reversed-Z**는 깊이 매핑을 뒤집어(near=1, far=0) 부동소수점의 정밀도 분포와 상보적으로 작용하게 하여, 전 구간에서 균일한 깊이 정밀도를 얻는 기법입니다. Unity는 DirectX, Metal, Vulkan 플랫폼에서 자동 적용합니다.
- Reversed-Z 적용 시 **투영 행렬의 깊이 매핑**, **깊이 테스트 비교 방향**, **깊이 클리어 값** 세 가지를 변경해야 하며, Unity는 지원 플랫폼에서 이를 자동으로 처리합니다.
- Unity 카메라의 `fieldOfView`, `nearClipPlane`, `farClipPlane`이 투영 설정의 핵심이며, `projectionMatrix`를 직접 설정하여 커스텀 투영도 가능합니다.

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)

**시리즈**
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- **그래픽스 수학 (4) - 투영 (현재 글)**

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- **그래픽스 수학 (4) - 투영** (현재 글)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
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
