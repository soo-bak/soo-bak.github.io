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

다만 원근 투영의 깊이 값은 카메라로부터의 거리에 대해 균일하게 분포하지 않습니다. 정밀도는 near 평면 근처에 많이 몰리고, far 평면에 가까워질수록 한 깊이 값이 담당하는 실제 거리 범위가 커집니다. 그 결과 먼 곳에 거의 같은 거리로 놓인 두 표면은 깊이 버퍼 안에서 구분하기 어려운 값으로 기록될 수 있습니다.

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

FOV(Field of View)는 카메라의 시야각을 뜻합니다. 이 글에서는 Unity의 `Camera.fieldOfView`처럼 **세로 FOV**를 기준으로 다루며, 이 값은 같은 깊이에 있는 절두체 단면의 세로 크기를 정합니다. FOV가 넓어지면 같은 거리에서 절두체 단면이 커지고, 더 넓은 공간이 NDC의 `[-1, 1]` 범위로 매핑됩니다. 따라서 같은 거리와 같은 크기의 오브젝트는 화면에서 더 작게 보입니다.

반대로 FOV가 좁아지면 같은 거리에서 절두체 단면이 작아지고, 좁은 공간이 화면 범위를 더 크게 차지합니다. 따라서 같은 오브젝트가 확대되어 보이며, 망원 렌즈나 줌 인과 비슷한 효과가 납니다.

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

Aspect ratio는 화면의 가로/세로 비율이며, 기준 FOV가 정해졌을 때 반대 축의 시야 범위를 계산하는 데 사용됩니다.

Unity의 `Camera.fieldOfView`처럼 세로 FOV를 기준으로 하면, aspect ratio는 같은 깊이에 있는 절두체 단면의 가로 폭을 정합니다. 예를 들어 16:9 화면에서 세로 FOV가 60도라면, 가로 FOV는 `2 atan(aspect * tan(60° / 2))`로 계산되어 약 91.5도가 됩니다.

즉 투영 행렬은 세로 FOV로 절두체의 높이를 정하고, aspect ratio로 그 높이에 대응하는 너비를 계산합니다. 반대로 가로 FOV를 기준으로 삼는 설정에서는 aspect ratio를 이용해 세로 범위를 계산합니다.

---

### 투영 행렬의 구성 원리

원근 투영 행렬은 3D 좌표를 화면 픽셀 좌표로 한 번에 바꾸는 행렬이 아닙니다. 이 행렬의 결과는 클립 공간(clip space) 좌표이며, 아직 최종 화면 위치가 확정된 상태가 아닙니다.

중요한 점은 이 단계에서 `x`, `y`는 FOV와 aspect ratio에 맞게 스케일되고, `w`에는 카메라로부터의 거리가 들어간다는 것입니다. 이후 GPU는 클립 공간 좌표의 `x`, `y`, `z`를 `w`로 나누어 NDC 좌표를 만듭니다. 가까운 점은 작은 `w`로 나뉘기 때문에 화면상 변화가 크게 남고, 먼 점은 큰 `w`로 나뉘기 때문에 같은 크기의 변화도 작게 압축됩니다. 이 때문에 같은 크기의 물체라도 멀리 있을수록 화면에서 작게 보입니다.

세로 FOV를 기준으로 보면, 카메라에서 거리 `d`만큼 떨어진 절두체 단면의 절반 높이는 다음과 같습니다.

$$
d \tan(\text{FOV}/2)
$$

절반 너비는 여기에 aspect ratio를 곱한 값입니다.

$$
\text{aspect} \cdot d \tan(\text{FOV}/2)
$$

즉 절두체 위쪽 경계에 있는 점은 원근 나눗셈 후 `y_ndc = 1`이 되어야 하고, 오른쪽 경계에 있는 점은 `x_ndc = 1`이 되어야 합니다. 따라서 `x`, `y`에는 다음 스케일이 곱해집니다.

$$
s_y = \frac{1}{\tan(\text{FOV}/2)}, \qquad
s_x = \frac{1}{\text{aspect} \cdot \tan(\text{FOV}/2)}
$$

FOV가 넓어지면 `tan(FOV/2)`가 커지므로 `s_x`, `s_y`는 작아집니다. 더 넓은 시야를 같은 NDC 범위 안에 넣어야 하므로 물체가 작게 보입니다. 반대로 FOV가 좁아지면 스케일 값이 커져 망원 렌즈처럼 물체가 크게 보입니다.

`x`, `y` 스케일과 깊이 변환, 그리고 `w`에 거리를 넣는 과정을 한 행렬로 묶으면 다음 형태가 됩니다.

$$
P_{\text{persp}} =
\begin{bmatrix}
\frac{1}{\text{aspect} \cdot \tan(\text{FOV}/2)} & 0 & 0 & 0 \\
0 & \frac{1}{\tan(\text{FOV}/2)} & 0 & 0 \\
0 & 0 & \frac{f}{n - f} & \frac{nf}{n - f} \\
0 & 0 & -1 & 0
\end{bmatrix}
$$

여기서 `n`은 near plane 거리, `f`는 far plane 거리입니다.

첫 번째 행과 두 번째 행은 `x`, `y`를 FOV와 aspect ratio에 맞게 스케일합니다.

세 번째 행은 깊이 버퍼에 사용할 `z` 값을 만듭니다. near plane과 far plane 사이의 `z` 값을 깊이 비교에 적합한 범위로 재배치하는 역할입니다.

네 번째 행은 원근감의 핵심입니다.

$$
w_{clip} = -z_{view}
$$

많은 그래픽스 API와 엔진은 뷰 공간에서 카메라가 `-z` 방향을 바라보는 관례를 사용합니다. 이 관례에서는 카메라 앞에 있는 점의 `z_view`가 음수이므로, `-z_view`는 카메라로부터의 양수 거리로 볼 수 있습니다. 이후 원근 나눗셈을 하면 `x`, `y`는 다음처럼 거리로 한 번 더 나뉩니다.

$$
\begin{aligned}
x_{ndc} &= \frac{x_{clip}}{w_{clip}} = \frac{x_{clip}}{d} \\
y_{ndc} &= \frac{y_{clip}}{w_{clip}} = \frac{y_{clip}}{d}
\end{aligned}
$$

계산을 단순하게 보기 위해 FOV와 aspect ratio에 따른 스케일 값은 `1`로 두고, 뷰 공간에서 세로 길이가 `2`인 물체를 가정하겠습니다. 이 물체의 위쪽 점이 `y = 1`, 아래쪽 점이 `y = -1`에 있다면 원래 세로 길이는 `1 - (-1) = 2`입니다.

이 물체가 카메라에서 `5`만큼 떨어져 있으면 원근 나눗셈 후 위쪽 점은 `1 / 5 = 0.2`, 아래쪽 점은 `-1 / 5 = -0.2`가 됩니다. 따라서 NDC에서 차지하는 높이는 `0.2 - (-0.2) = 0.4`입니다.

같은 물체가 거리 `20`에 있으면 위쪽 점은 `1 / 20 = 0.05`, 아래쪽 점은 `-1 / 20 = -0.05`가 됩니다. 이때 NDC에서 차지하는 높이는 `0.05 - (-0.05) = 0.1`입니다. 같은 물체라도 거리가 4배 멀어지면, `w`도 4배 커지고, 원근 나눗셈 결과 화면상 높이는 4분의 1로 줄어듭니다.

원근 나눗셈은 화면상의 크기만 바꾸지 않습니다. `z`도 `w`로 나뉘기 때문에, 깊이 버퍼에 저장되는 깊이 값 역시 이 영향을 받습니다.

깊이 값의 목적은 간단합니다. 같은 픽셀에 여러 표면이 겹쳤을 때 어느 표면이 더 앞에 있는지 비교하기 위한 값입니다. 이를 위해 near plane에 있는 점은 깊이 범위의 앞쪽 값으로, far plane에 있는 점은 뒤쪽 값으로 보내야 합니다.

문제는 이 매핑이 실제 거리와 균등하지 않다는 점입니다. 원근감을 만들기 위해 `w`에 거리 `d`를 넣었고, 최종 단계에서 `z`도 그 `d`로 나뉩니다. 그 결과 깊이 값은 거리 자체가 아니라, 거리의 역수에 가까운 형태로 변합니다.

$$
z_{ndc} = \frac{f}{f - n}\left(1 - \frac{n}{d}\right)
$$

여기서 중요한 부분은 `1 / d`입니다. 예를 들어 `n = 1`, `f = 100`이라고 하면 깊이 값은 대략 다음처럼 변합니다.

| 카메라로부터의 거리 `d` | 깊이 값 `z_ndc` |
|---:|---:|
| `1` | `0` |
| `2` | `0.505` |
| `10` | `0.909` |
| `100` | `1` |

거리 `1`에서 `2`로 이동하는 아주 가까운 구간이 깊이 범위의 절반 이상을 차지합니다. 반면 거리 `10`에서 `100`까지의 넓은 구간은 깊이 값으로 보면 `0.909`에서 `1` 사이의 좁은 범위에 압축됩니다.

이 때문에 깊이 버퍼의 정밀도는 카메라 가까이에 많이 배정되고, 멀리 갈수록 부족해집니다. 먼 곳에 있는 두 표면은 실제 거리 차이가 어느 정도 있어도 깊이 버퍼 안에서는 거의 같은 값으로 기록될 수 있고, 이것이 뒤에서 다룰 Z-fighting의 원인이 됩니다.

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
  <text fill="currentColor" x="372" y="135" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">Projection + w 나눗셈</text>
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

  <text fill="currentColor" x="380" y="230" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.72">원근 투영에서는 x, y가 거리 d에 비례하는 w로 나뉘므로, 먼 물체가 더 작은 NDC 영역을 차지합니다.</text>

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
  <text fill="currentColor" x="372" y="380" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">Projection + w 나눗셈</text>
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

직교 투영의 시야 영역은 원근 투영처럼 멀어질수록 넓어지는 절두체가 아니라, near plane과 far plane의 크기가 같은 **직육면체** 형태입니다. 따라서 카메라로부터의 거리가 달라져도 시야 영역의 폭과 높이는 변하지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;" role="img" aria-label="Orthographic camera view volume is a rectangular box with parallel view rays">
  <defs>
    <marker id="ortho-volume-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="currentColor"/>
    </marker>
  </defs>

  <text fill="currentColor" x="310" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">직교 투영의 시야 영역</text>
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
  <text fill="currentColor" x="302" y="154" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.36">직육면체 형태의 시야 영역</text>

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

직교 투영 행렬은 직육면체 형태의 시야 영역을 NDC의 정해진 범위로 맞춰 변환합니다. 원근 투영처럼 멀어질수록 시야 단면이 커지는 구조가 아니므로, `w`에 카메라 거리를 넣어 `x`, `y`를 줄이지 않습니다.

따라서 직교 투영에서는 `x`, `y`, `z`를 각각 정해진 범위에서 NDC 범위로 선형 변환합니다.

$$
P_{\text{ortho}} = \begin{bmatrix} \frac{2}{r - l} & 0 & 0 & -\frac{r + l}{r - l} \\ 0 & \frac{2}{t - b} & 0 & -\frac{t + b}{t - b} \\ 0 & 0 & \frac{-1}{f - n} & -\frac{n}{f - n} \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

$$l, r$$ = 왼쪽, 오른쪽 경계, $$b, t$$ = 아래, 위 경계, $$n, f$$ = near, far plane

이 행렬에서 `x`는 `[l, r]` 범위에서 `[-1, 1]` 범위로, `y`는 `[b, t]` 범위에서 `[-1, 1]` 범위로 옮겨집니다. `z`도 near~far 범위 안에서 깊이 비교에 사용할 값으로 변환됩니다. 중요한 점은 이 과정이 모두 선형이라는 것입니다.

원근 투영과의 가장 큰 차이는 마지막 행에 있습니다.

$$
w_{clip} = 1
$$

원근 투영에서는 `w`가 카메라로부터의 거리 `d`에 비례합니다. 따라서 원근 나눗셈을 거치면 먼 물체일수록 `x`, `y`가 더 크게 나뉘어 작게 보입니다.

직교 투영에서는 `w`가 항상 `1`입니다. GPU가 원근 나눗셈을 수행해도 `x / 1`, `y / 1`이 되므로 `x`, `y`가 거리 때문에 줄어들지 않습니다. 가까운 물체와 먼 물체가 뷰 공간에서 같은 크기라면, NDC에서도 같은 크기를 차지합니다.

---

## 깊이 값의 비선형성

앞에서 본 것처럼 원근 투영에서는 `z`값이 `w`로 나뉩니다. 이 때문에 깊이 버퍼에 저장되는 값은 카메라로부터의 실제 거리와 같은 비율로 증가하지 않습니다.

예를 들어 카메라에서 `1m` 떨어진 지점과 `2m` 떨어진 지점의 차이는 깊이 값에 크게 반영됩니다. 하지만 `100m`와 `101m`의 차이는 실제로는 같은 `1m` 차이여도, 깊이 값에서는 훨씬 작게 나타납니다. 깊이 값이 실제 거리 전체에 균등하게 배분되지 않는다는 뜻입니다.

<br>

이 글에서 사용하는 NDC 깊이 범위 `[0, 1]`을 기준으로, 카메라로부터의 거리를 `d`라고 하면 깊이 값은 다음과 같이 계산됩니다.

$$
z_{\text{ndc}} = \frac{f}{f - n} - \frac{f \cdot n}{(f - n) \cdot d}
$$

$$n$$ = near plane 거리, $$f$$ = far plane 거리, $$d$$ = 뷰 공간에서의 실제 거리 ($$n \leq d \leq f$$)

이 식은 near plane에서 `0`, far plane에서 `1`이 되도록 깊이 값을 만듭니다.

중요한 부분은 두 번째 항의 분모에 `d`가 들어간다는 점입니다. 깊이 값은 거리 `d` 자체에 비례하는 것이 아니라, `1 / d`가 섞인 형태로 변합니다. 이 때문에 가까운 거리 구간은 깊이 값 안에서 크게 벌어지고, 먼 거리 구간은 깊이 값의 끝부분에 작게 압축됩니다.

<br>

아래 그래프는 `n = 0.3`, `f = 1000`일 때 거리 `d`에 따라 깊이 값 `z_ndc`가 어떻게 변하는지 보여줍니다. 카메라에 가까운 구간에서는 거리가 조금만 증가해도 `z_ndc`가 빠르게 커집니다. 반대로 어느 정도 멀어진 뒤에는 거리가 크게 증가해도 `z_ndc`는 거의 `1` 근처에서 조금만 변합니다.

즉 깊이 값의 넓은 구간은 카메라 가까이에 사용되고, 먼 거리는 `1`에 가까운 좁은 구간 안에 압축됩니다. 이 분포 때문에 깊이 버퍼 정밀도는 near plane 근처에 많이 몰리고, far plane 쪽으로 갈수록 부족해집니다.

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

24비트 깊이 버퍼의 총 단계 수는 $$2^{24}$$ = 16,777,216입니다. 단계 수 자체는 많지만, 원근 투영의 비선형 깊이 분포 때문에 이 단계들이 실제 거리 전체에 고르게 쓰이지 않습니다. 가까운 구간에는 많은 단계가 배정되고, 먼 구간에는 훨씬 적은 단계만 남습니다. 이 불균형이 원거리에서의 깊이 정밀도 부족을 만듭니다.

---

## Z-fighting

이 정밀도 부족이 실제 렌더링에서 일으키는 문제가 **Z-fighting**입니다. 거의 같은 깊이에 있는 두 표면의 깊이 값이 구분되지 않아, 어느 표면이 앞인지 판정할 수 없게 됩니다.

깊이 버퍼는 연속적인 깊이 값을 그대로 무한히 저장하지 못합니다. 정해진 비트 수 안에서 표현해야 하므로, 계산된 깊이 값은 가장 가까운 저장 단계로 반올림됩니다. 이처럼 연속적인 값을 제한된 단계 중 하나로 바꾸는 과정을 **양자화(quantization)**라고 합니다.

문제는 먼 거리에서 서로 다른 표면의 깊이 값 차이가 매우 작아진다는 점입니다. 두 값의 차이가 깊이 버퍼의 한 단계보다 작으면, 실제로는 서로 다른 거리에 있어도 같은 깊이 값으로 저장될 수 있습니다. 이 순간 깊이 테스트는 두 표면의 앞뒤를 안정적으로 구분할 수 없게 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <defs>
    <marker id="zf-quant-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 Z" fill="currentColor"/>
    </marker>
  </defs>

  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Z-fighting: 서로 다른 깊이가 같은 저장 단계로 묶이는 경우</text>
  <text x="310" y="43" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.62">near = 0.1, far = 1000, 24비트 깊이 버퍼 예시</text>

  <rect x="32" y="68" width="164" height="108" rx="3" fill="currentColor" fill-opacity="0.035" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.32"/>
  <text x="114" y="91" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">뷰 공간 거리</text>
  <text x="52" y="119" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">표면 A</tspan> d = 500.0</text>
  <text x="52" y="143" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">표면 B</tspan> d = 500.1</text>
  <text x="52" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.66">실제 거리 차이 = 0.1</text>

  <line x1="203" y1="122" x2="225" y2="122" stroke="currentColor" stroke-width="1" marker-end="url(#zf-quant-arrow)" opacity="0.55"/>

  <rect x="232" y="68" width="174" height="108" rx="3" fill="currentColor" fill-opacity="0.035" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.32"/>
  <text x="319" y="91" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">NDC 깊이 값</text>
  <text x="250" y="119" font-family="sans-serif" font-size="10.5" fill="currentColor"><tspan font-weight="bold">A</tspan> 0.999899990...</text>
  <text x="250" y="143" font-family="sans-serif" font-size="10.5" fill="currentColor"><tspan font-weight="bold">B</tspan> 0.999900030...</text>
  <text x="250" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.66">차이 ≈ 0.000000040</text>

  <line x1="413" y1="122" x2="435" y2="122" stroke="currentColor" stroke-width="1" marker-end="url(#zf-quant-arrow)" opacity="0.55"/>

  <rect x="442" y="68" width="146" height="108" rx="3" fill="currentColor" fill-opacity="0.035" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.32"/>
  <text x="515" y="91" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">저장 단계</text>
  <text x="462" y="119" font-family="sans-serif" font-size="10.5" fill="currentColor"><tspan font-weight="bold">A</tspan> 16775537</text>
  <text x="462" y="143" font-family="sans-serif" font-size="10.5" fill="currentColor"><tspan font-weight="bold">B</tspan> 16775537</text>
  <text x="462" y="164" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">같은 값으로 저장</text>

  <text x="310" y="207" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.82">두 깊이 값의 차이가 깊이 버퍼 한 단계보다 작으면 같은 정수 값으로 양자화됩니다.</text>

  <line x1="115" y1="248" x2="505" y2="248" stroke="currentColor" stroke-width="1.2" opacity="0.55"/>
  <rect x="244" y="226" width="132" height="44" rx="3" fill="currentColor" fill-opacity="0.055" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <text x="310" y="221" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.62">하나의 깊이 버퍼 저장 단계</text>
  <circle cx="302" cy="248" r="4" fill="currentColor"/>
  <circle cx="318" cy="248" r="4" fill="currentColor" fill-opacity="0.55" stroke="currentColor" stroke-width="1"/>
  <text x="302" y="287" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">A</text>
  <text x="318" y="287" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">B</text>
  <text x="310" y="309" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">깊이 테스트는 두 표면의 앞뒤를 안정적으로 구분할 수 없습니다.</text>
</svg>
</div>

GPU는 픽셀을 그릴 때마다 깊이 테스트(depth test)를 수행합니다. 이미 그려진 표면의 깊이 값이 깊이 버퍼에 저장되어 있고, 새로 그리려는 표면의 깊이 값이 들어오면 두 값을 비교합니다. 새 표면이 더 가깝다고 판단되면 기존 값을 덮어쓰고, 더 멀다고 판단되면 버립니다.

두 표면의 깊이 차이가 충분히 크면 비교 결과는 명확합니다. 같은 픽셀에 표면 A와 표면 B가 겹쳐도, 더 가까운 표면의 깊이 값이 확실히 구분되므로 뒤쪽 표면은 깊이 테스트에서 제외됩니다. 이 경우 화면에는 앞쪽 표면만 안정적으로 남습니다.

Z-fighting은 두 표면의 깊이 차이가 깊이 버퍼가 구분할 수 있는 간격보다 작을 때 발생합니다. 실제 공간에서는 표면 A가 조금 더 앞에 있더라도, 깊이 버퍼에는 A와 B가 거의 같은 값으로 저장될 수 있습니다. 이렇게 되면 깊이 테스트가 항상 같은 표면을 선택하지 못하고, 작은 계산 차이나 카메라 움직임에 따라 선택 결과가 달라질 수 있습니다.

그 결과 화면에서는 두 표면이 한자리를 두고 번갈아 나타나는 것처럼 보입니다. 프레임마다 선택되는 표면이 바뀌면 깜빡임으로 보이고, 픽셀마다 선택이 갈리면 얼룩지거나 찢어진 패턴처럼 보입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 490 175" xmlns="http://www.w3.org/2000/svg" style="max-width: 490px; width: 100%;">
  <!-- ═══ Left: Normal rendering ═══ -->
  <text fill="currentColor" x="115" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">정상 렌더링</text>
  <!-- Only the front surface remains visible after a stable depth test. -->
  <rect x="40" y="28" width="150" height="88" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" rx="2"/>
  <text fill="currentColor" x="115" y="68" text-anchor="middle" font-size="11" font-family="sans-serif">표면 A</text>
  <text fill="currentColor" x="115" y="84" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.45">앞쪽 표면</text>
  <text fill="currentColor" x="115" y="107" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.45">표면 B는 깊이 테스트에서 제외</text>
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
  <!-- B cells (darker overlay) — unstable selection pattern -->
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
  <text fill="currentColor" x="345" y="150" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">깊이 값이 거의 같음 → 픽셀마다 선택이 갈림</text>
  <text fill="currentColor" x="345" y="164" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.5">작은 변화에도 패턴이 바뀌어 깜빡임</text>
</svg>
</div>

<br>

Z-fighting이 잘 발생하는 상황은 크게 세 가지로 볼 수 있습니다.

첫 번째는 카메라에서 먼 곳에 있는 표면들입니다. 원근 투영의 깊이 값은 far 쪽으로 갈수록 실제 거리 차이를 작게 반영합니다. 따라서 가까운 곳에서는 충분히 구분되던 간격도, 먼 곳에서는 깊이 버퍼의 같은 저장 단계로 묶일 수 있습니다. 멀리 있는 지형, 도로, 건물 외벽처럼 넓은 표면들이 서로 가까이 놓일 때 이런 문제가 잘 드러납니다.

두 번째는 거의 같은 평면에 겹쳐 있는 표면입니다. 예를 들어 바닥 위에 붙인 데칼, 같은 위치에 중복된 메시, 코플래너(coplanar) 면처럼 두 표면의 위치가 거의 같으면 깊이 값도 처음부터 거의 같습니다. 이 경우에는 깊이 버퍼 정밀도가 충분하더라도 깊이 값만으로는 어느 쪽을 우선할지 안정적으로 정하기 어렵습니다. 따라서 렌더링 순서를 명확히 하거나, 깊이 오프셋을 적용하거나, 데칼 전용 처리처럼 깊이 값 외의 기준을 함께 사용해야 합니다.

세 번째는 카메라의 near/far 범위를 지나치게 넓게 잡은 경우입니다. 깊이 버퍼의 단계 수는 정해져 있으므로, 표현해야 할 거리 범위가 넓어질수록 같은 단계가 더 넓은 실제 거리를 담당하게 됩니다.

---

### Near/Far 평면 설정의 중요성

near plane과 far plane은 단순히 보이는 범위의 시작과 끝을 정하는 값이 아닙니다. 깊이 버퍼가 가진 한정된 정밀도를 그 범위 안에서 나누어 쓰게 만드는 기준이기도 합니다.

따라서 목표는 렌더링에 필요한 거리 범위만 남기는 것입니다. near plane은 카메라에 너무 붙이지 않고, far plane은 실제로 보여야 하는 최대 거리보다 과하게 멀리 두지 않는 편이 좋습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">near/far 범위가 깊이 정밀도에 미치는 영향</text>
  <text x="40" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">설정 1: near = 0.01, far = 10000</text>
  <line x1="40" y1="60" x2="580" y2="60" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="84" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 카메라 바로 앞의 매우 좁은 구간까지 깊이 범위에 포함</text>
  <text x="60" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 매우 먼 거리까지 포함되어 전체 깊이 범위가 과도하게 넓음</text>
  <text x="60" y="122" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 원거리 깊이 정밀도에 불리</text>
  <text x="40" y="162" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">설정 2: near = 0.1, far = 1000</text>
  <line x1="40" y1="170" x2="580" y2="170" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="194" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 불필요하게 가까운 영역을 줄여 near 쪽 편중을 완화</text>
  <text x="60" y="212" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 필요한 원거리까지만 포함하여 깊이 범위를 줄임</text>
  <text x="60" y="232" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 같은 깊이 버퍼에서도 더 나은 정밀도 확보</text>
  <text x="40" y="272" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">설정 3: near = 0.5, far = 500</text>
  <line x1="40" y1="280" x2="580" y2="280" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="304" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 장면이 허용한다면 더 가까운 불필요 구간을 제외</text>
  <text x="60" y="322" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ far도 필요한 거리까지만 두어 깊이 범위를 더 좁힘</text>
  <text x="60" y="342" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ Z-fighting 위험을 낮추기 쉬움</text>
</svg>
</div>

near plane은 깊이 정밀도에 특히 큰 영향을 줍니다. 원근 투영에서는 정밀도가 near 근처에 몰리므로, near를 지나치게 낮추면 가장 세밀하게 구분할 수 있는 깊이 단계가 카메라 바로 앞의 아주 짧은 구간에 쓰입니다. 대부분의 장면에서는 카메라 앞 몇 센티미터까지 렌더링할 필요가 없습니다. 그런데도 near를 0에 가깝게 두면 그 불필요한 구간까지 깊이 범위에 포함되고, 중거리와 원거리에서 사용할 정밀도는 그만큼 줄어듭니다. 결과적으로 먼 표면들의 작은 깊이 차이를 구분하기 어려워져 Z-fighting에 더 취약해집니다.

far plane은 해당 카메라가 실제 지오메트리로 그려야 하는 가장 먼 거리까지만 포함하는 편이 좋습니다. far를 과도하게 멀리 두면 깊이 버퍼가 같은 단계 수로 더 넓은 거리 범위를 감당해야 합니다. 특히 원거리 구간은 이미 깊이 값 변화가 작게 압축되어 있으므로, far가 멀어질수록 한 단계가 담당하는 실제 거리가 더 커집니다. 그 결과 중거리 이후에 가까이 놓인 표면들은 깊이 버퍼에서 같은 값으로 묶이기 쉬워지고, Z-fighting도 더 쉽게 발생합니다.

따라서 near와 far는 장르별 권장값이나 고정된 숫자로 정하기보다, 카메라가 반드시 그려야 하는 가장 가까운 표면과 가장 먼 표면을 기준으로 잡아야 합니다. 1인칭 손이나 무기처럼 카메라에 매우 가까운 모델이 필요하다면 전체 장면의 near를 무리하게 낮추기보다, 별도 카메라나 렌더링 레이어로 분리하는 방법을 고려할 수 있습니다. 반대로 먼 산, 하늘, 배경처럼 정확한 깊이 비교가 중요하지 않은 요소는 fog, LOD, culling, skybox 같은 방식으로 처리하는 편이 낫습니다. 이렇게 하면 far를 불필요하게 키우지 않으면서도 필요한 시각적 범위를 유지할 수 있습니다.

---

## Reversed-Z

near/far 범위를 좁히는 것은 Z-fighting을 줄이기 위해 가장 먼저 확인해야 할 설정입니다. 필요한 깊이 범위만 남기면 같은 깊이 버퍼 단계가 더 좁은 실제 거리 범위에 배분되기 때문입니다.

하지만 범위를 좁혀도 깊이 정밀도가 near 쪽에 치우치는 구조 자체는 그대로입니다. 원근 투영에서는 깊이 값이 여전히 near 근처에서 크게 변하고, far 쪽으로 갈수록 실제 거리 차이를 작게 반영합니다. 장면의 스케일이 크거나 원거리 표면이 많다면, near/far를 적절히 잡아도 원거리 정밀도 부족이 다시 드러날 수 있습니다.

이 구조적 편향을 줄이기 위해 깊이 값의 방향을 뒤집어 사용하는 기법이 **Reversed-Z**입니다.

기본 깊이 매핑에서는 near plane이 `0`, far plane이 `1`에 대응합니다. 따라서 카메라에서 멀어질수록 깊이 값은 `1`에 가까워집니다. Reversed-Z는 이 관계를 뒤집어 near를 `1`, far를 `0`에 대응시킵니다.

이 반전이 정밀도 향상으로 이어지는지는 깊이 값이 `0`과 `1` 사이에서 어떤 간격으로 저장되는지에 달려 있습니다. D16, D24 같은 정규화 정수 깊이 형식은 `0`부터 `1`까지의 깊이 범위를 균일하게 나누므로, 깊이 매핑을 뒤집어도 저장 간격의 분포는 달라지지 않습니다. 반면 D32_FLOAT 같은 부동소수점 깊이 형식은 값이 `0`에 가까울수록 표현 간격이 좁아집니다. 따라서 Reversed-Z처럼 far를 `0`에 대응시키면, 정밀도가 부족했던 원거리 깊이 값이 float의 촘촘한 구간에 저장되어 더 잘 구분됩니다.

### 부동소수점 깊이 형식의 값 간격

부동소수점 깊이 형식은 깊이 값을 float으로 저장합니다. float이 표현할 수 있는 값은 연속적이지 않으므로, 계산된 깊이는 가장 가까운 표현값으로 기록됩니다. 이때 인접한 표현값 사이의 간격이 깊이를 구분할 수 있는 최소 단위가 됩니다.

앞에서 본 것처럼 float은 `0.0` 근처에서 간격이 좁고, `1.0`에 가까워질수록 간격이 넓어집니다. 이를 값의 배치로 보면 다음과 같습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 110" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text fill="currentColor" x="240" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">float의 [0, 1] 값 간격</text>
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
  <text fill="currentColor" x="120" y="97" font-size="10" font-family="sans-serif" opacity="0.6">← 값 간격이 좁음</text>
  <text fill="currentColor" x="320" y="97" font-size="10" font-family="sans-serif" opacity="0.6">값 간격이 넓음 →</text>
</svg>
</div>

이런 간격 차이는 float의 지수 구조에서 나옵니다. float은 값을 유효숫자와 지수로 나누어 저장하는데, 유효숫자에 쓸 수 있는 비트 수는 정해져 있습니다. 지수가 작아 값의 규모가 작아지면 같은 유효숫자 한 칸이 나타내는 절대 크기도 작아집니다. 반대로 값의 규모가 커질수록 한 칸이 나타내는 절대 크기는 커집니다. 그래서 float은 작은 값 근처에서는 촘촘하고, 큰 값 근처에서는 간격이 넓어집니다.

### 기본 깊이 매핑에서의 정밀도 겹침

기본 매핑에서는 float의 촘촘한 구간이 정밀도가 부족한 원거리 쪽에 쓰이지 않습니다. 원근 투영만 보아도 near 근처는 깊이 값이 크게 변해 서로 구분되기 쉽고, far 근처는 깊이 값 변화가 작아 구분되기 어렵습니다. 그런데 기본 매핑은 near를 NDC `0`, far를 NDC `1`에 대응시킵니다. 부동소수점 깊이 버퍼에서는 `0` 근처의 표현 간격이 좁으므로, 저장 정밀도까지 near 쪽에 더해집니다. 반대로 far 쪽은 원근 투영으로 이미 깊이 변화가 작게 압축되어 있는데, 저장되는 값도 간격이 넓은 `1` 근처를 사용하게 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기본 깊이 매핑에서 정밀도가 near 쪽에 몰리는 방식</text>
  <text x="60" y="56" font-family="sans-serif" font-size="11" fill="currentColor">NDC 깊이</text>
  <text x="160" y="56" font-family="sans-serif" font-size="11" fill="currentColor">0</text>
  <line x1="180" y1="52" x2="540" y2="52" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="552" y="56" font-family="sans-serif" font-size="11" fill="currentColor">1</text>
  <text x="60" y="80" font-family="sans-serif" font-size="11" fill="currentColor">대응 거리</text>
  <text x="160" y="80" font-family="sans-serif" font-size="10" fill="currentColor">near plane</text>
  <line x1="220" y1="76" x2="510" y2="76" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="520" y="80" font-family="sans-serif" font-size="10" fill="currentColor">far plane</text>
  <line x1="40" y1="100" x2="580" y2="100" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="124" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">원근 투영의 깊이 값 변화</text>
  <text x="60" y="146" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">near 쪽: 깊이 값 변화가 큼 → 실제 거리 구분이 쉬움</text>
  <text x="60" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">far 쪽: 깊이 값 변화가 작음 → 실제 거리 구분이 어려움</text>
  <line x1="40" y1="184" x2="580" y2="184" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="208" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">float의 저장 간격</text>
  <text x="60" y="230" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">NDC 0 근처: 값 간격이 좁음 → 저장 정밀도 높음</text>
  <text x="60" y="248" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">NDC 1 근처: 값 간격이 넓음 → 저장 정밀도 낮음</text>
  <line x1="40" y1="268" x2="580" y2="268" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="294" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">→ near 쪽</tspan>: 깊이 변화도 크고 저장 간격도 좁음 <tspan opacity="0.7">(정밀도 중복)</tspan></text>
  <text x="40" y="318" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">→ far 쪽</tspan>: 깊이 변화는 작고 저장 간격은 넓음 <tspan opacity="0.7">(정밀도 부족)</tspan></text>
</svg>
</div>

즉 기본 매핑은 이미 구분이 쉬운 가까운 곳에 정밀도를 더 보태고, 정작 필요한 먼 곳에는 넓은 저장 간격을 남깁니다. 원거리 정밀도를 보완하려면 이 배치를 뒤집어, float의 촘촘한 `0` 근처 구간을 far 쪽에 대응시켜야 합니다.

---

### Reversed-Z의 원리

Reversed-Z는 앞에서 본 배치를 그대로 뒤집습니다. near plane을 NDC `1`에, far plane을 NDC `0`에 대응시켜 먼 거리가 `0` 근처의 깊이 값을 사용하게 만듭니다.

이렇게 해도 원근 투영의 비선형성 자체가 사라지는 것은 아닙니다. near 근처에서는 여전히 깊이 값 변화가 크고, far 쪽으로 갈수록 변화가 작게 압축됩니다. 달라지는 것은 그 압축된 far 구간이 float의 어느 영역에 저장되느냐입니다.

Reversed-Z에서는 far 쪽이 float의 `0` 근처에 놓입니다. float은 `0` 근처에서 표현 간격이 좁으므로, 기본 매핑에서 부족했던 원거리 저장 정밀도를 보완할 수 있습니다. 반대로 near 쪽은 float의 `1` 근처를 사용하게 되지만, near에서는 원근 투영이 이미 깊이 값을 크게 변화시키기 때문에 상대적으로 손실이 작습니다.

결과적으로 정밀도가 가까운 곳에만 과하게 몰리지 않고, 깊이 범위 전체에 더 고르게 퍼집니다.

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
  <!-- Curve labels -->
  <text fill="currentColor" x="95" y="47" font-size="10" font-family="sans-serif" opacity="0.6">원근 투영 정밀도</text>
  <text fill="currentColor" x="95" y="165" font-size="10" font-family="sans-serif" opacity="0.6">float 정밀도 (Reversed-Z)</text>
  <text fill="currentColor" x="275" y="62" font-size="10" font-family="sans-serif" opacity="0.72">near: 원근 투영 정밀도 높음</text>
  <text fill="currentColor" x="260" y="182" font-size="10" font-family="sans-serif" opacity="0.72">far: float의 0 근처 정밀도가 보완</text>
  <!-- Bottom note -->
  <text fill="currentColor" x="240" y="245" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">부족한 원거리 쪽에 float의 촘촘한 구간을 배치</text>
</svg>
</div>

---

### Reversed-Z 적용 시 변경사항

Reversed-Z는 깊이 값을 읽는 방식만 바꾸는 기법이 아닙니다. 깊이 값을 만들고, 비교하고, 초기화하는 기준이 모두 반대로 맞춰져야 합니다. 직접 적용한다면 다음 세 가지가 함께 바뀌어야 합니다.

첫째, **투영 행렬이 만드는 깊이 매핑을 뒤집습니다**. 기본 매핑에서는 원근 나눗셈을 거친 뒤 near plane이 NDC `0`, far plane이 NDC `1`에 놓이지만, Reversed-Z에서는 이 결과가 반대로 나와야 합니다. 따라서 near가 `1`, far가 `0`에 대응하도록 투영 행렬의 깊이 계산을 바꿉니다.

둘째, **깊이 테스트의 비교 방향을 뒤집습니다**. 깊이 테스트는 새로 그리려는 프래그먼트의 깊이와 이미 깊이 버퍼에 저장된 값을 비교해, 카메라에 더 가까운 쪽을 남깁니다. 기본 매핑에서는 가까울수록 깊이 값이 작기 때문에 더 작은 값이 통과하는 `Less` 또는 `LessEqual` 비교를 사용합니다. Reversed-Z에서는 가까울수록 깊이 값이 커지므로, 더 큰 값이 통과하도록 `Greater` 또는 `GreaterEqual` 비교로 바꿔야 합니다.

셋째, **깊이 버퍼의 클리어 값을 바꿉니다**. 프레임을 시작할 때 깊이 버퍼는 먼저 기본값으로 채워지는데, 이 값은 이후 그려질 프래그먼트들이 깊이 테스트를 통과할 수 있도록 가장 먼 깊이를 뜻해야 합니다. 기본 매핑에서는 far가 `1.0`에 놓이므로 `1.0`으로 클리어하지만, Reversed-Z에서는 far가 `0.0`에 놓이기 때문에 클리어 값도 `0.0`이 되어야 합니다.

정리하면, 원근 투영을 거친 깊이 값은 far 쪽으로 갈수록 변화 폭이 작아집니다. Reversed-Z는 이렇게 압축된 원거리 깊이 값이 부동소수점 깊이 버퍼의 `0` 근처에 기록되도록 매핑을 뒤집습니다. float은 `0` 근처에서 표현 간격이 좁기 때문에, 원거리에서 부족해진 깊이 구분 능력을 저장 단계에서 보완할 수 있습니다.

이 방식이 제대로 동작하려면 깊이 값을 만드는 기준, 비교하는 기준, 초기화하는 기준이 모두 같아야 합니다. 투영 행렬은 near가 `1`, far가 `0`이 되도록 깊이 값을 만들고, 깊이 테스트는 더 큰 값을 더 가까운 값으로 받아들여야 합니다. 깊이 버퍼도 가장 먼 값인 `0`으로 클리어해야 합니다. 이 중 하나라도 기존 기준으로 남아 있으면 깊이 판정이 어긋나거나, 화면에 아무것도 그려지지 않는 문제가 생길 수 있습니다.

---

### Unity에서의 Reversed-Z 지원

Unity는 사용 중인 그래픽스 API에 맞춰 깊이 버퍼의 방향을 자동으로 정합니다. DirectX 11/12, Metal, Vulkan에서는 Reversed-Z가 사용되며, 이때 깊이 버퍼와 깊이 텍스처의 값은 near plane에서 `1`, far plane에서 `0`에 가까워집니다. 반대로 OpenGL ES, WebGL, OpenGL 계열에서는 전통적인 깊이 방향을 사용하므로 near plane이 `0`, far plane이 `1`에 대응합니다.

| 그래픽스 API | 깊이 값 방향 | Reversed-Z | 대표 플랫폼 |
|---|---|---|---|
| DirectX 11 / 12 | near `1` → far `0` | 적용 | Windows, Xbox |
| Metal | near `1` → far `0` | 적용 | iOS, macOS |
| Vulkan | near `1` → far `0` | 적용 | Android, Windows, Linux |
| OpenGL ES / WebGL | near `0` → far `1` | 미적용 | Android 구형 기기, Web |
| OpenGL 계열 | near `0` → far `1` | 미적용 | 일부 데스크톱 환경 |

<br>

일반적인 URP 렌더링에서는 이 차이를 직접 처리하지 않아도 됩니다. Unity와 URP가 현재 그래픽스 API에 맞춰 GPU 투영 행렬, 깊이 테스트 방향, 깊이 버퍼 초기값을 내부에서 맞춰 주기 때문입니다. 카메라, 머티리얼, 렌더 패스가 기본 깊이 흐름을 따른다면 클립 공간 좌표와 깊이 비교도 플랫폼의 깊이 방향에 맞게 동작합니다.

문제가 되는 경우는 깊이 값을 **직접 읽거나 직접 비교하는** 코드입니다. 예를 들어 `_CameraDepthTexture`나 URP의 `SampleSceneDepth()`로 얻은 raw depth를 그대로 비교하거나, 포스트 프로세싱에서 깊이 기반 효과를 만들거나, 커스텀 섀도우/깊이 패스에서 투영 행렬을 직접 조합할 때는 깊이 방향 차이를 고려해야 합니다.

Reversed-Z에서는 깊이 값 `1`이 가까운 쪽, `0`이 먼 쪽을 의미합니다. 반대로 전통적인 깊이 버퍼에서는 `0`이 near, `1`이 far입니다. 따라서 raw depth를 항상 `0 = near`, `1 = far`라고 가정하면 가까움과 멂의 판정이 플랫폼에 따라 뒤집힐 수 있습니다.

이런 코드는 셰이더에서 `UNITY_REVERSED_Z`로 분기하거나, 가능하면 Unity가 제공하는 `Linear01Depth()`, `LinearEyeDepth()`, `UNITY_Z_0_FAR_FROM_CLIPSPACE()` 같은 헬퍼를 사용하는 편이 안전합니다. C#에서는 `SystemInfo.usesReversedZBuffer`로 현재 플랫폼이 Reversed-Z를 사용하는지 확인할 수 있습니다.

모바일도 하나의 규칙으로 묶을 수 없습니다. iOS와 macOS처럼 Metal을 사용하는 환경은 Reversed-Z를 사용하고, Android도 Vulkan으로 실행하면 Reversed-Z가 적용됩니다. 반면 OpenGL ES 기반의 구형 Android 기기나 WebGL 환경은 전통적인 깊이 방향을 사용할 수 있습니다. 여러 플랫폼을 대상으로 한다면 raw depth 값에 고정된 의미를 부여하지 말고, Unity의 매크로와 깊이 변환 함수를 기준으로 처리하는 것이 가장 안전합니다.

---

## Unity 카메라의 투영 설정

Unity Camera에서 투영 방식은 `Projection`으로 선택합니다. `Perspective`는 원근감이 있는 절두체를 만들고, `Orthographic`은 거리와 관계없이 같은 크기로 보이는 직육면체 형태의 시야 영역을 만듭니다. 깊이 정밀도는 별도 품질 옵션보다 `Near`와 `Far` 사이의 범위에 크게 좌우됩니다. Reversed-Z는 Unity가 그래픽스 API에 맞춰 처리하므로, Camera 컴포넌트에서 직접 켜고 끄는 설정은 없습니다.

| 속성 | 기본값 | 모드 | 설명 |
|---|---|---|---|
| Projection | Perspective | 공통 | 원근 / 직교 투영 방식 선택 |
| Field of View | 60 | Perspective | 시야각. 기본은 세로 기준 |
| Size | 5 | Orthographic | 화면 세로 절반 크기 |
| Near Clip Plane | 0.3 | 공통 | 렌더링을 시작하는 거리 |
| Far Clip Plane | 1000 | 공통 | 렌더링을 끝내는 거리 |

<br>

Perspective 모드에서는 `Camera.fieldOfView`가 시야각을 정합니다. 값이 커질수록 더 넓은 영역이 보이고 원근감도 강해지며, 값이 작아질수록 좁게 당겨 보입니다. 기본값은 `60`도이고, 스크립트에서 `camera.fieldOfView = 90f;`처럼 바꿔 줌 인/아웃, 조준, 대시 시야 확장 같은 연출에 사용할 수 있습니다.

Orthographic 모드에서는 `Camera.orthographicSize`가 화면에 들어오는 세로 범위를 정합니다. 이 값은 화면 세로 절반의 크기이므로, `Size`가 `5`이면 화면의 세로 전체는 월드 공간 `10`단위를 표시합니다. 가로 범위는 카메라의 aspect ratio에 따라 자동으로 결정됩니다.

`Camera.nearClipPlane`과 `Camera.farClipPlane`은 카메라가 실제로 그리는 거리 범위를 정합니다. near보다 가까운 물체와 far보다 먼 물체는 렌더링되지 않습니다. 깊이 정밀도를 확보하려면 이 범위를 불필요하게 넓히지 않는 것이 중요합니다. 장면에서 허용되는 한 near는 멀리 두고, far는 가까이 두는 편이 좋습니다.

다만 near를 너무 멀리 두면 카메라 가까이의 물체가 잘리고, far를 너무 가까이 두면 먼 배경이나 대형 오브젝트가 사라집니다. 기본값 `0.3`과 `1000`은 출발점일 뿐이며, 실제 장면의 크기와 카메라 동선에 맞춰 조정해야 합니다.

투영 모드는 Camera 컴포넌트의 `Projection` 드롭다운에서 바꾸거나, 스크립트에서 `camera.orthographic = true` 또는 `false`로 전환합니다. `true`이면 `orthographicSize`가, `false`이면 `fieldOfView`가 화면 범위를 결정합니다.

---

### projectionMatrix 직접 설정

`camera.projectionMatrix`에 행렬을 대입하면 Unity가 `fieldOfView`, `orthographicSize`, `nearClipPlane`, `farClipPlane`, `aspect`로 계산하던 투영 행렬을 직접 지정할 수 있습니다. 일반적인 카메라 설정은 앞의 속성만으로 충분하지만, 한쪽으로 치우친 절두체, 포털이나 반사 렌더링을 위한 기울어진 클리핑 평면, 특수한 렌즈 보정처럼 기본 Camera 설정으로 표현하기 어려운 경우에는 투영 행렬을 직접 다룹니다.

평소에는 Unity가 Camera 속성을 바탕으로 투영 행렬을 만들어 줍니다. 예를 들어 `fieldOfView`, `orthographicSize`, `nearClipPlane`, `farClipPlane`, `aspect`가 바뀌면 그 값들을 반영한 투영 행렬이 다시 계산됩니다.

하지만 `camera.projectionMatrix`에 직접 행렬을 넣으면, 그 순간부터 카메라는 Unity가 계산한 행렬 대신 사용자가 넣은 행렬을 사용합니다. 이 상태에서는 `fieldOfView` 같은 속성값이 바뀌어도 렌더링에 쓰이는 투영 행렬이 자동으로 따라 바뀌지 않습니다. 기본 방식으로 돌아가려면 `camera.ResetProjectionMatrix()`를 호출해야 합니다.

따라서 커스텀 투영 행렬은 필요한 렌더링 구간에만 제한해서 쓰는 편이 좋습니다. 특히 투영 행렬을 셰이더나 커맨드 버퍼에서 직접 조합해 사용한다면, 앞에서 본 플랫폼별 깊이 방향과 GPU 투영 행렬 차이까지 함께 고려해야 합니다.

한편 단순히 깊이 정밀도를 조정하려는 목적이라면 `projectionMatrix`를 직접 만들 필요가 없습니다. 스크립트에서 `nearClipPlane`과 `farClipPlane`을 장면 규모에 맞게 바꾸는 것으로도 충분한 경우가 많습니다. 예를 들어 실내 장면에서는 far를 작게 줄이고, 야외 장면에서는 필요한 거리까지만 늘려 near/far 범위를 좁게 유지하는 식으로 관리할 수 있습니다.

---

## 마무리

이번 글에서는 Projection 행렬이 카메라의 시야 영역을 클립 공간으로 바꾸는 방식과, 그 과정에서 깊이 값이 어떻게 만들어지는지 살펴봤습니다. 원근 투영과 직교 투영은 화면상의 크기 변화를 만드는 방식이 다르고, 특히 원근 투영의 깊이 값은 near/far 범위와 깊이 버퍼 형식에 크게 영향을 받습니다.

- **원근 투영**은 near, far, FOV, aspect ratio로 정해지는 절두체를 클립 공간으로 변환하고, 원근 나눗셈을 통해 가까운 물체는 크게, 먼 물체는 작게 보이게 만듭니다.
- **직교 투영**은 near plane과 far plane의 크기가 같은 직육면체 형태의 시야 영역을 사용합니다. `w`가 항상 `1`이므로, 거리가 달라도 같은 크기의 물체는 화면에서도 같은 크기로 보입니다.
- **깊이 값의 비선형성**은 원근 투영에서 생기는 중요한 특징입니다. 깊이 정밀도는 near 근처에 많이 몰리고, far 쪽으로 갈수록 같은 깊이 값 하나가 더 넓은 실제 거리 범위를 담당합니다.
- **Z-fighting**은 깊이 버퍼가 두 표면의 앞뒤를 안정적으로 구분하지 못할 때 발생합니다. near를 가능한 한 멀리 두고, far를 필요한 범위까지만 줄이면 near/far 비율이 줄어 깊이 정밀도를 확보하기 쉬워집니다.
- **Reversed-Z**는 깊이 매핑을 near = `1`, far = `0`으로 뒤집는 기법입니다. 부동소수점 깊이 버퍼에서는 float의 `0` 근처 정밀도를 far 쪽에 배치해 원거리 깊이 정밀도를 보완합니다.
- **Unity의 Reversed-Z 처리**는 그래픽스 API에 따라 자동으로 적용됩니다. DirectX, Metal, Vulkan에서는 Reversed-Z가 사용되고, OpenGL ES나 WebGL처럼 전통적인 깊이 방향을 쓰는 환경에서는 raw depth를 직접 해석할 때 주의해야 합니다.
- **Unity Camera 설정**에서는 `fieldOfView`, `orthographicSize`, `nearClipPlane`, `farClipPlane`이 투영과 깊이 범위를 정합니다. 일반적인 경우에는 이 속성들을 조정하면 충분하고, 비표준 투영이 필요할 때만 `projectionMatrix`를 직접 설정합니다.

여기까지가 정점이 화면에 놓이기 전까지의 수학적 변환입니다. 실제 렌더링에서는 이 좌표들이 래스터화, 깊이 테스트, 셰이딩 단계를 거치며 최종 픽셀 색으로 이어집니다.

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)

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
