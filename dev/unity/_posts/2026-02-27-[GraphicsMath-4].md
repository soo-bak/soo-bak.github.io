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

[그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)에서는 정점 좌표가 Projection 행렬을 거쳐 클립 공간에 도달하고, 이후 원근 나눗셈과 뷰포트 변환을 통해 화면 공간으로 이어지는 흐름을 살펴봤습니다. 이번 글에서는 그중 Projection 단계 자체에 집중합니다.

3D 장면을 2D 화면에 그린다는 것은 카메라가 보는 입체 공간의 점들을 렌더 타깃의 픽셀 위치로 대응시키는 일입니다. 화면에서 실제로 보이는 위치는 x, y 두 축으로 표현되지만, 렌더링 과정에서 z 정보를 단순히 버릴 수는 없습니다. z를 무시하면 거리에 따른 크기 변화가 사라지고, 같은 픽셀을 덮는 여러 표면 중 어느 쪽이 앞에 있는지도 판단할 수 없기 때문입니다.

투영(Projection)은 이 두 가지 문제를 함께 다룹니다. 원근 투영은 가까운 물체는 크게, 먼 물체는 작게 보이도록 좌표를 변환하고, 동시에 깊이 비교에 사용할 값을 만들어 냅니다. 이 깊이 값은 깊이 버퍼(depth buffer)에 저장되며, 같은 픽셀을 그리려는 여러 표면 중 카메라에 더 가까운 표면을 남기는 기준이 됩니다.

다만 원근 투영의 깊이 값은 카메라로부터의 거리에 대해 균일하게 분포하지 않습니다. 정밀도는 near 평면 근처에 많이 몰리고, far 평면에 가까워질수록 한 깊이 값이 담당하는 실제 거리 범위가 커집니다. 그래서 먼 곳에 거의 같은 거리로 놓인 두 표면은 깊이 버퍼 안에서 구분하기 어려운 값으로 기록될 수 있습니다.

이 차이가 깊이 버퍼의 표현 정밀도보다 작아지면 GPU는 어느 표면이 앞에 있는지 안정적으로 판정하지 못합니다. 그 결과 프레임마다 앞뒤 판정이 흔들리면서 표면이 깜빡이는 Z-fighting이 발생합니다.

이 글에서는 원근 투영과 직교 투영의 Projection 행렬 구조, 비선형성의 원인, 그리고 이를 완화하는 Reversed-Z 기법을 다룹니다.

---

## 원근 투영

원근 투영(Perspective Projection)은 카메라에서 먼 오브젝트일수록 화면에서 작게, 가까운 오브젝트일수록 크게 그리는 투영 방식입니다. 카메라의 위치를 하나의 시점으로 두고, 그 시점에서 퍼져 나가는 시야 안의 3D 점들을 2D 화면 위로 대응시키기 때문에 거리감이 생깁니다. Projection 행렬은 이 시야 영역을 클립 공간으로 옮기고, 이후 원근 나눗셈을 거치면서 거리에 따른 화면상의 크기 차이가 만들어집니다.

원근 투영을 이해하려면 먼저 카메라가 볼 수 있는 영역이 어떻게 정해지는지 봐야 합니다.

### 절두체(Frustum)의 구성 요소

카메라의 원근 시야는 카메라 앞쪽으로 갈수록 넓어지는 사각뿔 형태입니다. 실제 렌더링에서는 이 시야를 near plane과 far plane으로 앞뒤에서 잘라 내며, 이렇게 남은 잘린 사각뿔 모양의 영역을 **절두체(Frustum)**라고 합니다. near plane과 far plane은 렌더링할 깊이 범위를 정하고, FOV와 aspect ratio는 절두체 단면의 높이와 너비 비율을 정합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;" role="img" aria-label="3D view frustum: camera, near plane, far plane, FOV, aspect ratio">
  <defs>
    <marker id="frustum-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- Example geometry: vertical FOV=60deg, aspect=16:9, near=1, far=3. -->
  <!-- Projected points are based on height(d)=2d*tan(FOV/2), width(d)=height(d)*aspect. -->

  <!-- Clipped pyramid rays before the near plane -->
  <line x1="80" y1="230" x2="178.9" y2="181.7" stroke="currentColor" stroke-width="1" stroke-dasharray="5,4" opacity="0.28"/>
  <line x1="80" y1="230" x2="261.1" y2="206.3" stroke="currentColor" stroke-width="1" stroke-dasharray="5,4" opacity="0.28"/>
  <line x1="80" y1="230" x2="261.1" y2="258.3" stroke="currentColor" stroke-width="1" stroke-dasharray="5,4" opacity="0.28"/>
  <line x1="80" y1="230" x2="178.9" y2="233.7" stroke="currentColor" stroke-width="1" stroke-dasharray="5,4" opacity="0.28"/>

  <!-- Vertical FOV plane -->
  <line x1="80" y1="230" x2="500" y2="122.1" stroke="currentColor" stroke-width="1.2" stroke-dasharray="6,4" opacity="0.48"/>
  <line x1="80" y1="230" x2="500" y2="277.9" stroke="currentColor" stroke-width="1.2" stroke-dasharray="6,4" opacity="0.48"/>
  <path d="M 128.5 217.5 A 50 50 0 0 1 129.6 235.7" stroke="currentColor" fill="none" stroke-width="1" opacity="0.55"/>
  <text fill="currentColor" x="126" y="210" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.75">세로 FOV</text>

  <!-- Frustum faces: near plane N, far plane F -->
  <polygon points="178.9,181.7 261.1,206.3 623.2,159.1 376.8,85.1" fill="currentColor" fill-opacity="0.045"/>
  <polygon points="178.9,233.7 261.1,258.3 623.2,315 376.8,240.9" fill="currentColor" fill-opacity="0.055"/>
  <polygon points="178.9,181.7 178.9,233.7 376.8,240.9 376.8,85.1" fill="currentColor" fill-opacity="0.035"/>
  <polygon points="261.1,206.3 261.1,258.3 623.2,315 623.2,159.1" fill="currentColor" fill-opacity="0.07"/>
  <polygon points="376.8,85.1 623.2,159.1 623.2,315 376.8,240.9" fill="currentColor" fill-opacity="0.055" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.65"/>
  <polygon points="178.9,181.7 261.1,206.3 261.1,258.3 178.9,233.7" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.8"/>

  <!-- Frustum edges -->
  <line x1="178.9" y1="181.7" x2="376.8" y2="85.1" stroke="currentColor" stroke-width="1.4"/>
  <line x1="261.1" y1="206.3" x2="623.2" y2="159.1" stroke="currentColor" stroke-width="1.4"/>
  <line x1="261.1" y1="258.3" x2="623.2" y2="315" stroke="currentColor" stroke-width="1.4"/>
  <line x1="178.9" y1="233.7" x2="376.8" y2="240.9" stroke="currentColor" stroke-width="1.4"/>

  <!-- View axis -->
  <line x1="80" y1="230" x2="500" y2="200" stroke="currentColor" stroke-width="1" stroke-dasharray="7,5" opacity="0.36"/>
  <circle cx="220" cy="220" r="3" fill="currentColor" opacity="0.65"/>
  <circle cx="500" cy="200" r="3" fill="currentColor" opacity="0.65"/>
  <text fill="currentColor" x="176" y="261" font-size="10" font-family="sans-serif" opacity="0.65">near 거리 n</text>
  <text fill="currentColor" x="468" y="224" font-size="10" font-family="sans-serif" opacity="0.65">far 거리 f</text>

  <!-- Far plane dimensions -->
  <line x1="376.8" y1="73" x2="623.2" y2="147" stroke="currentColor" stroke-width="0.9" marker-start="url(#frustum-arrow)" marker-end="url(#frustum-arrow)" opacity="0.48"/>
  <text fill="currentColor" x="500" y="94" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.72">너비 = 높이 x aspect</text>
  <line x1="642" y1="159.1" x2="642" y2="315" stroke="currentColor" stroke-width="0.9" marker-start="url(#frustum-arrow)" marker-end="url(#frustum-arrow)" opacity="0.48"/>
  <text fill="currentColor" x="636" y="240" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.72">높이: FOV</text>

  <!-- Labels -->
  <circle cx="80" cy="230" r="5" fill="currentColor"/>
  <text fill="currentColor" x="80" y="253" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">카메라</text>
  <text fill="currentColor" x="220" y="286" text-anchor="middle" font-size="11" font-family="sans-serif">Near Plane</text>
  <text fill="currentColor" x="560" y="340" text-anchor="middle" font-size="11" font-family="sans-serif">Far Plane</text>
  <text fill="currentColor" x="405" y="193" text-anchor="middle" font-size="13" font-family="sans-serif" opacity="0.55">절두체</text>

  <!-- Parameter summary -->
  <text fill="currentColor" x="340" y="382" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.72">near/far plane은 카메라 방향의 렌더링 범위를 자릅니다.</text>
  <text fill="currentColor" x="340" y="400" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">단면 높이 = 2d tan(FOV/2), 단면 너비 = 단면 높이 x aspect</text>
</svg>
</div>

<br>

Near plane과 far plane은 카메라가 렌더링할 깊이 범위를 정합니다. near plane보다 가까운 부분과 far plane보다 먼 부분은 절두체 밖으로 판정되어 클리핑되며, 프리미티브가 경계를 걸치면 경계 안쪽에 남은 부분만 다음 단계로 넘어갑니다.

FOV는 같은 깊이에 있는 절두체 단면의 높이를 정합니다. FOV가 넓어지면 단면이 커져 더 넓은 공간이 NDC의 제한된 범위 안으로 압축되므로, 같은 거리와 크기의 오브젝트는 화면에서 더 작게 보입니다.

반대로 FOV가 좁아지면 단면이 작아져 좁은 공간이 화면을 더 크게 채우므로, 같은 오브젝트가 확대되어 망원 렌즈나 줌 인처럼 보입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 760 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 760px; width: 100%;" role="img" aria-label="FOV changes how the same view-space object maps to screen space">
  <!-- Same object in view space: distance d=115, half-height h=20. -->
  <!-- Screen mapping uses y_ndc = y / (d * tan(vertical FOV / 2)). -->

  <text fill="currentColor" x="190" y="28" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">좁은 FOV (30°)</text>
  <text fill="currentColor" x="570" y="28" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">넓은 FOV (90°)</text>

  <g transform="translate(0, 0)">
    <text fill="currentColor" x="112" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.65">View Space 세로 단면</text>
    <text fill="currentColor" x="305" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.65">Screen / NDC</text>

    <!-- View-space FOV wedge. At the object depth, half-height = 115*tan(15deg) = 30.8. -->
    <polygon points="40,210 185,171.1 185,248.9" fill="currentColor" fill-opacity="0.06"/>
    <line x1="40" y1="210" x2="185" y2="210" stroke="currentColor" stroke-dasharray="6,4" stroke-width="0.8" opacity="0.35"/>
    <line x1="40" y1="210" x2="185" y2="171.1" stroke="currentColor" stroke-width="1.4"/>
    <line x1="40" y1="210" x2="185" y2="248.9" stroke="currentColor" stroke-width="1.4"/>
    <line x1="185" y1="171.1" x2="185" y2="248.9" stroke="currentColor" stroke-width="1.7" opacity="0.75"/>

    <!-- Same object and its angular rays. -->
    <rect x="149" y="190" width="12" height="40" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.2"/>
    <line x1="40" y1="210" x2="155" y2="190" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
    <line x1="40" y1="210" x2="155" y2="230" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
    <circle cx="40" cy="210" r="4.5" fill="currentColor"/>
    <path d="M 88.3 197.1 A 50 50 0 0 1 88.3 222.9" stroke="currentColor" fill="none" stroke-width="1.1"/>
    <text fill="currentColor" x="99" y="214" font-size="11" font-family="sans-serif">30°</text>
    <text fill="currentColor" x="40" y="235" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">카메라</text>
    <text fill="currentColor" x="155" y="184" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">같은 오브젝트</text>

    <!-- Screen-space result: object occupies about 65% of screen height. -->
    <rect x="270" y="140" width="70" height="140" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <line x1="270" y1="210" x2="340" y2="210" stroke="currentColor" stroke-dasharray="4,3" stroke-width="0.8" opacity="0.35"/>
    <rect x="294" y="164.6" width="22" height="90.8" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.2"/>
    <text fill="currentColor" x="346" y="143" font-size="9" font-family="sans-serif" opacity="0.6">y=1</text>
    <text fill="currentColor" x="346" y="283" font-size="9" font-family="sans-serif" opacity="0.6">y=-1</text>
    <text fill="currentColor" x="305" y="306" text-anchor="middle" font-size="11" font-family="sans-serif">스크린에서 크게 보임</text>
  </g>

  <g transform="translate(380, 0)">
    <text fill="currentColor" x="112" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.65">View Space 세로 단면</text>
    <text fill="currentColor" x="305" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.65">Screen / NDC</text>

    <!-- View-space FOV wedge. At the object depth, half-height = 115*tan(45deg) = 115. -->
    <polygon points="40,210 185,65 185,355" fill="currentColor" fill-opacity="0.06"/>
    <line x1="40" y1="210" x2="185" y2="210" stroke="currentColor" stroke-dasharray="6,4" stroke-width="0.8" opacity="0.35"/>
    <line x1="40" y1="210" x2="185" y2="65" stroke="currentColor" stroke-width="1.4"/>
    <line x1="40" y1="210" x2="185" y2="355" stroke="currentColor" stroke-width="1.4"/>
    <line x1="185" y1="65" x2="185" y2="355" stroke="currentColor" stroke-width="1.7" opacity="0.75"/>

    <!-- Same object and its angular rays. -->
    <rect x="149" y="190" width="12" height="40" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.2"/>
    <line x1="40" y1="210" x2="155" y2="190" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
    <line x1="40" y1="210" x2="155" y2="230" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
    <circle cx="40" cy="210" r="4.5" fill="currentColor"/>
    <path d="M 64.7 185.3 A 35 35 0 0 1 64.7 234.7" stroke="currentColor" fill="none" stroke-width="1.1"/>
    <text fill="currentColor" x="78" y="214" font-size="11" font-family="sans-serif">90°</text>
    <text fill="currentColor" x="40" y="235" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">카메라</text>
    <text fill="currentColor" x="155" y="184" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">같은 오브젝트</text>

    <!-- Screen-space result: object occupies about 17% of screen height. -->
    <rect x="270" y="140" width="70" height="140" fill="none" stroke="currentColor" stroke-width="1.4"/>
    <line x1="270" y1="210" x2="340" y2="210" stroke="currentColor" stroke-dasharray="4,3" stroke-width="0.8" opacity="0.35"/>
    <rect x="294" y="197.8" width="22" height="24.4" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1.2"/>
    <text fill="currentColor" x="346" y="143" font-size="9" font-family="sans-serif" opacity="0.6">y=1</text>
    <text fill="currentColor" x="346" y="283" font-size="9" font-family="sans-serif" opacity="0.6">y=-1</text>
    <text fill="currentColor" x="305" y="306" text-anchor="middle" font-size="11" font-family="sans-serif">스크린에서 작게 보임</text>
  </g>

  <text fill="currentColor" x="380" y="405" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.72">같은 뷰 공간 좌표라도 Projection 행렬과 원근 나눗셈을 거치면 FOV에 따라 NDC상의 y 비율이 달라집니다.</text>
  <text fill="currentColor" x="380" y="425" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">y_ndc = y / (d tan(FOV/2)) 이므로 FOV가 좁을수록 같은 오브젝트가 스크린 공간에서 더 크게 매핑됩니다.</text>
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

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">w 나눗셈으로 만들어지는 원근감</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">뷰 공간의 두 점</text>
  <text x="60" y="68" font-family="monospace" font-size="11" fill="currentColor">A = (1, 1, -5, 1)</text>
  <text x="260" y="68" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">카메라에서 5m 앞</text>
  <text x="60" y="88" font-family="monospace" font-size="11" fill="currentColor">B = (1, 1, -20, 1)</text>
  <text x="260" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">카메라에서 20m 앞</text>
  <line x1="40" y1="106" x2="580" y2="106" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="130" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">투영 행렬 적용 후 (간략화)</text>
  <text x="60" y="150" font-family="monospace" font-size="11" fill="currentColor">A_clip = (s·1, s·1, z_a, 5)</text>
  <text x="320" y="150" font-family="monospace" font-size="11" fill="currentColor" opacity="0.85">w = 5</text>
  <text x="60" y="170" font-family="monospace" font-size="11" fill="currentColor">B_clip = (s·1, s·1, z_b, 20)</text>
  <text x="320" y="170" font-family="monospace" font-size="11" fill="currentColor" opacity="0.85">w = 20</text>
  <line x1="40" y1="188" x2="580" y2="188" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="212" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">원근 나눗셈 (w로 나누기)</text>
  <text x="60" y="232" font-family="monospace" font-size="11" fill="currentColor">A_ndc = (s/5,  s/5,  ...)</text>
  <text x="340" y="232" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">x, y 비교적 큼</text>
  <text x="60" y="252" font-family="monospace" font-size="11" fill="currentColor">B_ndc = (s/20, s/20, ...)</text>
  <text x="340" y="252" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">x, y 비교적 작음</text>
  <line x1="40" y1="278" x2="580" y2="278" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="310" y="306" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">A는 화면에서 크게, B는 화면에서 작게 표시됨</text>
</svg>
</div>

w가 5인 A는 나눈 뒤에도 x, y가 크게 남고, w가 20인 B는 나눈 뒤 x, y가 1/4로 줄어듭니다. 뷰 공간에서 동일한 (1, 1) 좌표였던 두 점이, 카메라까지의 거리 차이만으로 화면에서 서로 다른 크기로 그려집니다. 원근감은 이 w 나눗셈 한 단계에서 만들어집니다.

---

## 직교 투영

직교 투영(Orthographic Projection)은 원근감이 없는 **평행 투영**입니다.

카메라로부터의 거리와 관계없이 오브젝트의 크기가 동일하게 표현됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 760 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 760px; width: 100%;" role="img" aria-label="Perspective and orthographic projection compared from view volume to normalized device coordinates">
  <defs>
    <marker id="projection-compare-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- Perspective row -->
  <text fill="currentColor" x="380" y="24" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">원근 투영: 절두체를 NDC로 매핑</text>
  <text fill="currentColor" x="180" y="51" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">View Volume: Frustum</text>
  <text fill="currentColor" x="522" y="51" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">NDC x-y 평면</text>

  <!-- Frustum: far rectangle is a scaled version of the near rectangle from the camera point. -->
  <line x1="55" y1="150" x2="115" y2="115" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="55" y1="150" x2="160" y2="125" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="55" y1="150" x2="160" y2="185" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="55" y1="150" x2="115" y2="175" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <polygon points="115,115 160,125 307,90 199,66" fill="currentColor" fill-opacity="0.04"/>
  <polygon points="115,175 160,185 307,234 199,210" fill="currentColor" fill-opacity="0.05"/>
  <polygon points="115,115 115,175 199,210 199,66" fill="currentColor" fill-opacity="0.035"/>
  <polygon points="160,125 160,185 307,234 307,90" fill="currentColor" fill-opacity="0.065"/>
  <polygon points="199,66 307,90 307,234 199,210" fill="currentColor" fill-opacity="0.055" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.62"/>
  <polygon points="115,115 160,125 160,185 115,175" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.45"/>
  <line x1="115" y1="115" x2="199" y2="66" stroke="currentColor" stroke-width="1.2"/>
  <line x1="160" y1="125" x2="307" y2="90" stroke="currentColor" stroke-width="1.2"/>
  <line x1="160" y1="185" x2="307" y2="234" stroke="currentColor" stroke-width="1.2"/>
  <line x1="115" y1="175" x2="199" y2="210" stroke="currentColor" stroke-width="1.2"/>
  <line x1="55" y1="150" x2="253" y2="150" stroke="currentColor" stroke-dasharray="6,4" stroke-width="0.8" opacity="0.32"/>
  <circle cx="55" cy="150" r="4.5" fill="currentColor"/>
  <text fill="currentColor" x="55" y="173" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.62">카메라</text>
  <text fill="currentColor" x="137" y="204" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.58">near</text>
  <text fill="currentColor" x="253" y="255" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.58">far</text>

  <!-- Same real size in view space. -->
  <circle cx="145" cy="145" r="11.5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="145" y="149" text-anchor="middle" font-size="10" font-family="sans-serif">A</text>
  <text fill="currentColor" x="145" y="126" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">가까움</text>
  <circle cx="245" cy="180" r="11.5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="245" y="184" text-anchor="middle" font-size="10" font-family="sans-serif">B</text>
  <text fill="currentColor" x="245" y="203" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">멀리 있음</text>

  <line x1="55" y1="150" x2="145" y2="133.5" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.28"/>
  <line x1="55" y1="150" x2="145" y2="156.5" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.28"/>
  <line x1="55" y1="150" x2="245" y2="168.5" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.28"/>
  <line x1="55" y1="150" x2="245" y2="191.5" stroke="currentColor" stroke-width="0.6" stroke-dasharray="3,3" opacity="0.28"/>

  <line x1="335" y1="150" x2="410" y2="150" stroke="currentColor" stroke-width="1.1" marker-end="url(#projection-compare-arrow)" opacity="0.65"/>
  <text fill="currentColor" x="372" y="135" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">Projection</text>
  <text fill="currentColor" x="372" y="165" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">w = d</text>

  <!-- NDC is shown as a canonical x-y square, not a screen aspect rectangle. -->
  <polygon points="482,73 587,73 610,55 505,55" fill="currentColor" fill-opacity="0.025" stroke="currentColor" stroke-width="0.8" opacity="0.45"/>
  <rect x="482" y="73" width="105" height="105" fill="none" stroke="currentColor" stroke-width="1.35"/>
  <line x1="505" y1="55" x2="505" y2="160" stroke="currentColor" stroke-width="0.8" opacity="0.35"/>
  <line x1="587" y1="73" x2="610" y2="55" stroke="currentColor" stroke-width="0.8" opacity="0.35"/>
  <line x1="587" y1="178" x2="610" y2="160" stroke="currentColor" stroke-width="0.8" opacity="0.35"/>
  <line x1="482" y1="125.5" x2="587" y2="125.5" stroke="currentColor" stroke-dasharray="4,3" stroke-width="0.8" opacity="0.35"/>
  <line x1="534.5" y1="73" x2="534.5" y2="178" stroke="currentColor" stroke-dasharray="4,3" stroke-width="0.8" opacity="0.35"/>
  <text fill="currentColor" x="592" y="77" font-size="8" font-family="sans-serif" opacity="0.58">x,y = 1</text>
  <text fill="currentColor" x="592" y="181" font-size="8" font-family="sans-serif" opacity="0.58">-1</text>
  <circle cx="516" cy="107" r="22" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="516" y="111" text-anchor="middle" font-size="11" font-family="sans-serif">A</text>
  <circle cx="558" cy="148" r="10" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="558" y="151" text-anchor="middle" font-size="8" font-family="sans-serif">B</text>

  <text fill="currentColor" x="380" y="230" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.72">원근 투영은 원근 나눗셈에서 w가 거리 d에 비례하므로, 같은 크기의 먼 물체가 더 작은 NDC 범위를 차지합니다.</text>

  <line x1="35" y1="265" x2="725" y2="265" stroke="currentColor" stroke-width="0.7" opacity="0.14"/>

  <!-- Orthographic row -->
  <text fill="currentColor" x="380" y="292" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">직교 투영: 직육면체를 NDC로 매핑</text>
  <text fill="currentColor" x="180" y="319" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">View Volume: Box</text>
  <text fill="currentColor" x="522" y="319" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">NDC x-y 평면</text>

  <!-- Orthographic volume shown with a horizontal depth axis: no tilt, same near/far size. -->
  <rect x="105" y="350" width="195" height="90" fill="currentColor" fill-opacity="0.045" stroke="currentColor" stroke-width="1.35"/>
  <rect x="105" y="350" width="50" height="90" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.45"/>
  <rect x="250" y="350" width="50" height="90" fill="currentColor" fill-opacity="0.055" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.62"/>
  <line x1="105" y1="350" x2="250" y2="350" stroke="currentColor" stroke-width="1.2"/>
  <line x1="155" y1="350" x2="300" y2="350" stroke="currentColor" stroke-width="1.2"/>
  <line x1="155" y1="440" x2="300" y2="440" stroke="currentColor" stroke-width="1.2"/>
  <line x1="105" y1="440" x2="250" y2="440" stroke="currentColor" stroke-width="1.2"/>

  <!-- Orthographic camera plane and parallel rays. -->
  <rect x="45" y="350" width="50" height="90" fill="currentColor" fill-opacity="0.018" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.62"/>
  <line x1="45" y1="350" x2="105" y2="350" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.34"/>
  <line x1="95" y1="350" x2="155" y2="350" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.34"/>
  <line x1="95" y1="440" x2="155" y2="440" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.34"/>
  <line x1="45" y1="440" x2="105" y2="440" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.34"/>
  <line x1="70" y1="395" x2="275" y2="395" stroke="currentColor" stroke-dasharray="6,4" stroke-width="0.8" opacity="0.32"/>
  <circle cx="70" cy="395" r="4.5" fill="currentColor"/>
  <text fill="currentColor" x="70" y="456" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.62">카메라</text>
  <text fill="currentColor" x="130" y="456" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.58">near</text>
  <text fill="currentColor" x="275" y="476" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.58">far</text>
  <text fill="currentColor" x="200" y="340" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.58">깊이축 수평 표시: near/far 단면 크기가 동일</text>

  <circle cx="145" cy="390" r="11.5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="145" y="394" text-anchor="middle" font-size="10" font-family="sans-serif">A</text>
  <text fill="currentColor" x="145" y="373" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">가까움</text>
  <circle cx="245" cy="425" r="11.5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="245" y="429" text-anchor="middle" font-size="10" font-family="sans-serif">B</text>
  <text fill="currentColor" x="245" y="448" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">멀리 있음</text>

  <line x1="335" y1="395" x2="410" y2="395" stroke="currentColor" stroke-width="1.1" marker-end="url(#projection-compare-arrow)" opacity="0.65"/>
  <text fill="currentColor" x="372" y="380" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">Projection</text>
  <text fill="currentColor" x="372" y="410" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">w = 1</text>

  <polygon points="482,338 587,338 610,320 505,320" fill="currentColor" fill-opacity="0.025" stroke="currentColor" stroke-width="0.8" opacity="0.45"/>
  <rect x="482" y="338" width="105" height="105" fill="none" stroke="currentColor" stroke-width="1.35"/>
  <line x1="505" y1="320" x2="505" y2="425" stroke="currentColor" stroke-width="0.8" opacity="0.35"/>
  <line x1="587" y1="338" x2="610" y2="320" stroke="currentColor" stroke-width="0.8" opacity="0.35"/>
  <line x1="587" y1="443" x2="610" y2="425" stroke="currentColor" stroke-width="0.8" opacity="0.35"/>
  <line x1="482" y1="390.5" x2="587" y2="390.5" stroke="currentColor" stroke-dasharray="4,3" stroke-width="0.8" opacity="0.35"/>
  <line x1="534.5" y1="338" x2="534.5" y2="443" stroke="currentColor" stroke-dasharray="4,3" stroke-width="0.8" opacity="0.35"/>
  <text fill="currentColor" x="592" y="342" font-size="8" font-family="sans-serif" opacity="0.58">x,y = 1</text>
  <text fill="currentColor" x="592" y="446" font-size="8" font-family="sans-serif" opacity="0.58">-1</text>
  <circle cx="514" cy="385" r="12" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="514" y="389" text-anchor="middle" font-size="9" font-family="sans-serif">A</text>
  <circle cx="558" cy="420" r="12" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.14"/>
  <text fill="currentColor" x="558" y="424" text-anchor="middle" font-size="9" font-family="sans-serif">B</text>

  <text fill="currentColor" x="380" y="503" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.72">직교 투영은 w가 항상 1이므로, 깊이가 달라도 같은 크기의 물체는 같은 크기의 NDC 범위를 차지합니다.</text>
</svg>
</div>

<br>

직교 투영의 시야 영역은 절두체가 아니라 **직육면체**입니다. 원근 투영에서는 시야 영역이 카메라에서 멀어질수록 넓어지는 절두체였지만, 직교 투영에서는 모든 거리에서 시야 영역의 폭과 높이가 동일합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;" role="img" aria-label="Orthographic camera view volume is a rectangular box with parallel view rays">
  <defs>
    <marker id="ortho-volume-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="currentColor"/>
    </marker>
  </defs>

  <text fill="currentColor" x="310" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">직교 시야 볼륨</text>
  <text fill="currentColor" x="310" y="52" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.62">깊이축 수평 표시: near plane과 far plane의 크기가 같은 직육면체</text>

  <!-- Orthographic camera plane and parallel rays. -->
  <rect x="30" y="95" width="100" height="110" fill="currentColor" fill-opacity="0.018" stroke="currentColor" stroke-width="0.8" stroke-dasharray="5,4" opacity="0.62"/>
  <line x1="30" y1="95" x2="105" y2="95" stroke="currentColor" stroke-width="0.9" stroke-dasharray="5,4" opacity="0.36"/>
  <line x1="130" y1="95" x2="205" y2="95" stroke="currentColor" stroke-width="0.9" stroke-dasharray="5,4" opacity="0.36"/>
  <line x1="130" y1="205" x2="205" y2="205" stroke="currentColor" stroke-width="0.9" stroke-dasharray="5,4" opacity="0.36"/>
  <line x1="30" y1="205" x2="105" y2="205" stroke="currentColor" stroke-width="0.9" stroke-dasharray="5,4" opacity="0.36"/>

  <!-- Orthographic cuboid: near and far rectangles are identical in size. -->
  <rect x="105" y="95" width="395" height="110" fill="currentColor" fill-opacity="0.045" stroke="currentColor" stroke-width="1.4"/>
  <rect x="105" y="95" width="100" height="110" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.7"/>
  <rect x="400" y="95" width="100" height="110" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.65"/>

  <!-- Parallel volume edges. -->
  <line x1="105" y1="95" x2="400" y2="95" stroke="currentColor" stroke-width="1.3"/>
  <line x1="205" y1="95" x2="500" y2="95" stroke="currentColor" stroke-width="1.3"/>
  <line x1="205" y1="205" x2="500" y2="205" stroke="currentColor" stroke-width="1.3"/>
  <line x1="105" y1="205" x2="400" y2="205" stroke="currentColor" stroke-width="1.3"/>

  <!-- Camera origin and center axis. -->
  <circle cx="80" cy="150" r="4.8" fill="currentColor"/>
  <text fill="currentColor" x="80" y="246" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.62">카메라</text>
  <line x1="80" y1="150" x2="450" y2="150" stroke="currentColor" stroke-dasharray="7,5" stroke-width="0.9" opacity="0.36"/>
  <text fill="currentColor" x="282" y="132" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.42">평행한 시선 방향</text>

  <text fill="currentColor" x="155" y="228" text-anchor="middle" font-size="10" font-family="sans-serif">Near Plane</text>
  <text fill="currentColor" x="450" y="228" text-anchor="middle" font-size="10" font-family="sans-serif">Far Plane</text>
  <text fill="currentColor" x="302" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.36">직교 시야 직육면체</text>

  <!-- Constant cross-section dimensions on the far plane. -->
  <line x1="400" y1="81" x2="500" y2="81" stroke="currentColor" stroke-width="0.85" marker-start="url(#ortho-volume-arrow)" marker-end="url(#ortho-volume-arrow)" opacity="0.52"/>
  <text fill="currentColor" x="450" y="76" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">너비 = 높이 x aspect</text>
  <line x1="515" y1="95" x2="515" y2="205" stroke="currentColor" stroke-width="0.85" marker-start="url(#ortho-volume-arrow)" marker-end="url(#ortho-volume-arrow)" opacity="0.52"/>
  <text fill="currentColor" x="510" y="152" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">높이 = 2 x Size</text>

  <!-- Distances from the camera origin to clipping planes. -->
  <line x1="80" y1="270" x2="155" y2="270" stroke="currentColor" stroke-width="0.8" opacity="0.48"/>
  <line x1="80" y1="266" x2="80" y2="274" stroke="currentColor" stroke-width="0.8" opacity="0.48"/>
  <line x1="155" y1="266" x2="155" y2="274" stroke="currentColor" stroke-width="0.8" opacity="0.48"/>
  <text fill="currentColor" x="118" y="284" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">n</text>

  <line x1="80" y1="292" x2="450" y2="292" stroke="currentColor" stroke-width="0.8" opacity="0.48"/>
  <line x1="80" y1="288" x2="80" y2="296" stroke="currentColor" stroke-width="0.8" opacity="0.48"/>
  <line x1="450" y1="288" x2="450" y2="296" stroke="currentColor" stroke-width="0.8" opacity="0.48"/>
  <text fill="currentColor" x="265" y="306" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">f</text>
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

**깊이 정밀도 분포 예시** (near=0.1, far=1000)

| 뷰 공간 거리 범위 | NDC 깊이 범위 | 깊이 버퍼의 비율 |
|:---|:---|:---:|
| 0.1 ~ 1.0 (근거리) | 0.0 ~ 0.90 | 약 90% |
| 1.0 ~ 10 (중거리) | 0.90 ~ 0.99 | 약 9% |
| 10 ~ 1000 (원거리) | 0.99 ~ 1.0 | 약 1% |

깊이 버퍼 정밀도의 90%가 카메라에서 1미터 이내에 집중되고, 10미터부터 1000미터 구간에는 정밀도의 1%만 배분됩니다.

24비트 깊이 버퍼의 총 단계 수는 $$2^{24}$$ = 16,777,216입니다. 위 표에서 NDC 범위의 약 90%가 카메라에서 1미터 이내에 집중되므로, 약 1,510만 단계가 이 좁은 구간에 사용됩니다. 반면 10미터에서 1,000미터까지의 넓은 구간에는 약 17만 단계만 남습니다. 이 불균형이 원거리에서의 깊이 정밀도 부족을 만듭니다.

---

## Z-fighting

이 정밀도 부족이 실제 렌더링에서 일으키는 문제가 **Z-fighting**입니다. 거의 같은 깊이에 있는 두 표면의 깊이 값이 구분되지 않아, 어느 표면이 앞인지 판정할 수 없게 됩니다.

**양자화(quantization)**는 연속적인 깊이 값을 정해진 비트 수의 정수로 변환하는 과정입니다. 깊이 버퍼는 이 양자화를 통해 깊이를 저장합니다. 24비트 깊이 버퍼라면 16,777,216개의 정수 단계로 깊이를 표현합니다. 원거리에서 정밀도가 부족하면, 서로 다른 두 깊이 값이 양자화 과정에서 같은 정수로 변환됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Z-fighting 현상</text>
  <text x="40" y="50" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">카메라에서 먼 거리에 있는 두 표면</text>
  <text x="60" y="72" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">표면 A</tspan>: 뷰 공간 깊이 = 500.0</text>
  <text x="60" y="92" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">표면 B</tspan>: 뷰 공간 깊이 = 500.1 <tspan opacity="0.7">(0.1 차이)</tspan></text>
  <line x1="40" y1="112" x2="580" y2="112" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="138" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">깊이 버퍼 (24비트) 값</text>
  <text x="60" y="160" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">표면 A</tspan>: 0.999899990…  →  양자화 후  16775537</text>
  <text x="60" y="180" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">표면 B</tspan>: 0.999900030…  →  양자화 후  <tspan font-weight="bold">16775537 (같은 값!)</tspan></text>
  <line x1="40" y1="202" x2="580" y2="202" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="228" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 두 표면의 깊이 값이 같아져 버림</text>
  <text x="40" y="252" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 어느 표면이 앞인지 판단 불가</text>
</svg>
</div>

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

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">near, far 설정에 따른 정밀도 변화</text>
  <text x="40" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">설정 1: near=0.01, far=10000</text>
  <line x1="40" y1="60" x2="580" y2="60" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="84" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ near가 0에 매우 가까워 깊이 단계가 극단적으로 near 쪽에 편중</text>
  <text x="60" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ far가 커서 정밀도가 부족한 원거리 구간이 넓음</text>
  <text x="60" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ Z-fighting 빈번</text>
  <text x="40" y="162" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">설정 2: near=0.1, far=1000</text>
  <line x1="40" y1="170" x2="580" y2="170" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="194" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ near가 0에서 멀어져 편중이 크게 완화</text>
  <text x="60" y="212" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ far가 줄어 원거리 구간이 좁아짐</text>
  <text x="60" y="232" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 원거리 Z-fighting 감소</text>
  <text x="40" y="272" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">설정 3: near=0.5, far=500</text>
  <line x1="40" y1="280" x2="580" y2="280" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="304" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ near가 0에서 충분히 떨어져 편중이 적음</text>
  <text x="60" y="322" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ far가 작아 깊이 범위 전체가 좁음</text>
  <text x="60" y="342" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ Z-fighting 거의 발생하지 않음</text>
</svg>
</div>

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

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기본 깊이 매핑 (near→NDC 0, far→NDC 1)</text>
  <text x="60" y="56" font-family="sans-serif" font-size="11" fill="currentColor">NDC 깊이</text>
  <text x="160" y="56" font-family="sans-serif" font-size="11" fill="currentColor">0</text>
  <line x1="180" y1="52" x2="540" y2="52" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="552" y="56" font-family="sans-serif" font-size="11" fill="currentColor">1</text>
  <text x="60" y="80" font-family="sans-serif" font-size="11" fill="currentColor">대응 거리</text>
  <text x="160" y="80" font-family="sans-serif" font-size="10" fill="currentColor">near plane</text>
  <line x1="220" y1="76" x2="510" y2="76" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="520" y="80" font-family="sans-serif" font-size="10" fill="currentColor">far plane</text>
  <line x1="40" y1="100" x2="580" y2="100" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="124" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">원근 투영의 정밀도 분포</text>
  <text x="60" y="146" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">near 근처 (0에 가까움): 깊이 변화가 큼 → 정밀도 높음</text>
  <text x="60" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">far 근처 (1에 가까움): 깊이 변화가 작음 → 정밀도 낮음</text>
  <line x1="40" y1="184" x2="580" y2="184" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="208" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">부동소수점의 정밀도 분포</text>
  <text x="60" y="230" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">0 근처: 표현 가능한 값이 많음 → 정밀도 높음</text>
  <text x="60" y="248" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">1 근처: 표현 가능한 값이 적음 → 정밀도 낮음</text>
  <line x1="40" y1="268" x2="580" y2="268" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="294" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">→ near 근처</tspan>: 이미 정밀도가 높은 곳에 float 정밀도까지 높음 <tspan opacity="0.7">(과잉)</tspan></text>
  <text x="40" y="318" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">→ far 근처</tspan>: 이미 정밀도가 낮은 곳에 float 정밀도까지 낮음 <tspan opacity="0.7">(부족)</tspan></text>
</svg>
</div>

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
