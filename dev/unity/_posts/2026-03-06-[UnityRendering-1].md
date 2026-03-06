---
layout: single
title: "Unity 렌더링 (1) - Camera와 Rendering Layer - soo:bak"
date: "2026-03-06 21:03:00 +0900"
description: Camera 컴포넌트, Culling Mask, Clear Flags, 렌더링 순서, Opaque/Transparent 정렬, 멀티 카메라 비용을 설명합니다.
tags:
  - Unity
  - 렌더링
  - Camera
  - Layer
  - 모바일
---

## 렌더링의 시작점, 카메라

이 시리즈에서는 Unity 렌더링 시스템의 기초를 다룹니다. 카메라가 무엇을 어떤 순서로 그리는지(이 글), 그 결과가 어디에 저장되는지([Unity 렌더링 (2)](/dev/unity/UnityRendering-2/)), 이 모든 과정을 엮는 렌더 파이프라인의 종류와 선택 기준([Unity 렌더링 (3)](/dev/unity/UnityRendering-3/))을 순서대로 살펴봅니다. [Unity 렌더 파이프라인](/dev/unity/UnityPipeline-1/) 시리즈에서 다루는 컬링, 정렬, 라이팅, 드로우콜 생성 구조는 이 시리즈의 내용을 토대로 합니다.

<br>

렌더링의 출발점은 **카메라(Camera)**입니다. 씬에 아무리 많은 오브젝트가 배치되어 있어도, 카메라가 없으면 화면에 아무것도 표시되지 않습니다. 카메라가 씬을 바라보는 위치와 방향, 시야각, 그리고 어떤 오브젝트를 대상으로 삼을지에 따라 렌더링할 대상과 순서가 결정됩니다. 렌더링 비용을 제어하려면 카메라의 역할을 먼저 이해해야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더링 흐름에서 카메라의 위치</text>

  <!-- Box 1: 씬 (Scene) -->
  <rect x="115" y="40" width="250" height="95" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="60" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 (Scene)</text>
  <text x="240" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 A</text>
  <text x="240" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 B</text>
  <text x="240" y="112" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 C</text>
  <text x="240" y="128" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">라이트, 파티클 ...</text>

  <!-- Arrow 1 -->
  <line x1="240" y1="135" x2="240" y2="165" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="233,160 240,172 247,160" fill="currentColor"/>

  <!-- Box 2: 카메라 (Camera) -->
  <rect x="95" y="175" width="290" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="196" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">카메라 (Camera)</text>
  <text x="240" y="220" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1) 어디를 바라볼 것인가</text>
  <text x="240" y="240" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(2) 무엇을 그릴 것인가</text>
  <text x="240" y="260" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(3) 어떤 순서로 그릴 것인가</text>
  <text x="240" y="280" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(4) 배경을 어떻게 채울 것인가</text>

  <!-- Arrow 2 -->
  <line x1="240" y1="305" x2="240" y2="335" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="233,330 240,342 247,330" fill="currentColor"/>

  <!-- Box 3: 렌더 파이프라인 -->
  <rect x="115" y="345" width="250" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="368" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더 파이프라인</text>
  <text x="240" y="390" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 컬링, 정렬, 드로우콜</text>
</svg>
</div>

<br>

카메라 컴포넌트의 속성들이 위 네 가지 결정을 제어합니다.

이 글에서는 (1)을 다루는 Camera 컴포넌트의 기본 속성, (2)를 다루는 Culling Mask, (4)를 다루는 Clear Flags, (3)을 다루는 렌더링 순서 순으로, 각 속성의 역할과 렌더링 비용에 미치는 영향을 살펴봅니다.

---

## Camera 컴포넌트

Unity에서 Camera는 씬을 화면에 투영하는 컴포넌트입니다. 게임 오브젝트에 Camera 컴포넌트를 부착하면, 그 오브젝트의 위치와 회전이 곧 카메라의 시점이 됩니다. 투영 방식, 시야각, 가시 범위 등 렌더링의 기본 조건을 결정하는 속성들이 이 컴포넌트에 모여 있습니다.

### Projection — 투영 방식

카메라가 3D 씬을 2D 화면으로 변환하는 방식을 결정합니다.

**Perspective(원근 투영)**는 가까운 물체가 크게, 먼 물체가 작게 보이는 투영입니다. 사람의 시각과 유사하여 3D 게임에서 기본으로 사용됩니다.
[그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 다룬 절두체(Frustum)가 원근 투영의 가시 영역입니다. 절두체는 잘린 피라미드(뿔대) 형태이며, 카메라에서 멀어질수록 보이는 영역이 넓어집니다.

<br>

**Orthographic(직교 투영)**은 거리에 관계없이 물체의 크기가 동일하게 보이는 투영입니다. 2D 게임이나 UI 렌더링에서 사용됩니다.
직교 투영의 가시 영역은 직육면체 형태이며, 카메라 앞 어디에 있든 같은 크기의 물체는 화면에서 같은 크기로 렌더링됩니다.

<br>

원근 투영에서는 절두체가 먼 곳으로 갈수록 넓어지므로 더 많은 오브젝트가 가시 영역에 포함될 수 있고, 직교 투영에서는 가시 영역이 일정하므로 카메라 위치만이 포함 오브젝트를 결정합니다.
가시 영역에 포함되는 오브젝트가 많을수록 렌더링해야 할 대상이 늘어나므로, 투영 방식의 선택은 렌더링 비용에 직접 영향을 줍니다.

### Field of View (FOV)

원근 투영에서 카메라의 수직 시야각을 결정합니다. Unity의 기본값은 60도이며, 값이 클수록 절두체가 넓어져 포함되는 오브젝트 수가 증가하고, 렌더링 대상도 함께 늘어납니다.
반대로 FOV가 좁으면 보이는 오브젝트가 줄어들지만, 개별 오브젝트가 화면에서 차지하는 비율이 커집니다. 직교 투영에서는 FOV 대신 Size 속성이 가시 영역의 크기를 결정하므로, FOV는 원근 투영에서만 의미를 가집니다.

### Near/Far Clip Plane

카메라의 가시 범위를 깊이 방향으로 제한하는 두 평면입니다. **Near Clip Plane**보다 가까운 오브젝트와 **Far Clip Plane**보다 먼 오브젝트는 렌더링에서 제외됩니다.

<br>

이 두 값은 깊이 정밀도에 직접적인 영향을 미칩니다. 깊이 버퍼(Depth Buffer)는 한정된 비트(일반적으로 24비트 또는 32비트)로 Near에서 Far 사이의 거리를 표현합니다.
[그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 다룬 것처럼, 원근 투영은 월드 공간의 거리를 NDC(정규화 장치 좌표)로 변환할 때 비선형 매핑을 적용합니다.

깊이 버퍼는 이 NDC 값을 균일한 정수 단계로 저장하지만, 비선형 매핑 때문에 Near 근처의 좁은 거리 구간이 NDC 범위의 대부분을 차지합니다. 결과적으로 깊이 버퍼의 정밀도가 Near 근처에 집중되고, Far 근처에서는 급격히 떨어집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">깊이 정밀도와 Near/Far 비율</text>

  <!-- === Bar 1: Near=0.01, Far=1000 === -->
  <text x="260" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Near = 0.01, Far = 1000 (비율 100,000:1)</text>

  <!-- Near / Far labels -->
  <text x="40" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Near</text>
  <text x="480" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Far</text>

  <!-- Full bar outline -->
  <rect x="40" y="74" width="440" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>

  <!-- High precision region (~70%) -->
  <rect x="40" y="74" width="308" height="24" rx="3" fill="currentColor" fill-opacity="0.3"/>

  <!-- Low precision region (~30%) -->
  <rect x="348" y="74" width="132" height="24" fill="currentColor" fill-opacity="0.08"/>
  <rect x="40" y="74" width="440" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>

  <!-- Tick marks and values -->
  <line x1="40" y1="98" x2="40" y2="106" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">0.01</text>

  <line x1="348" y1="98" x2="348" y2="106" stroke="currentColor" stroke-width="1"/>
  <text x="348" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">1.0</text>

  <line x1="480" y1="98" x2="480" y2="106" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">1000</text>

  <!-- Precision labels -->
  <text x="194" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정밀도 높음</text>
  <text x="414" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정밀도 낮음</text>

  <!-- === Bar 2: Near=0.3, Far=1000 === -->
  <text x="260" y="148" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Near = 0.3, Far = 1000 (비율 약 3,333:1)</text>

  <!-- Near / Far labels -->
  <text x="40" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Near</text>
  <text x="480" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Far</text>

  <!-- Full bar outline -->
  <rect x="40" y="174" width="440" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>

  <!-- Improved precision region (~50%) -->
  <rect x="40" y="174" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.3"/>

  <!-- Still low but mitigated region (~50%) -->
  <rect x="260" y="174" width="220" height="24" fill="currentColor" fill-opacity="0.08"/>
  <rect x="40" y="174" width="440" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>

  <!-- Tick marks and values -->
  <line x1="40" y1="198" x2="40" y2="206" stroke="currentColor" stroke-width="1"/>
  <text x="40" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">0.3</text>

  <line x1="260" y1="198" x2="260" y2="206" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">100</text>

  <line x1="480" y1="198" x2="480" y2="206" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">1000</text>

  <!-- Precision labels -->
  <text x="150" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정밀도 개선</text>
  <text x="370" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">여전히 낮지만 완화</text>
</svg>
</div>

<br>

**Far/Near 비율이 클수록 Z-fighting 위험이 증가합니다.**
Z-fighting은 깊이 값이 거의 같은 두 표면이 번갈아 보이는 현상입니다. 깊이 정밀도가 부족하면, 서로 가까이 있는 두 면 중 어느 것이 앞에 있는지 GPU가 판별하지 못하기 때문에 발생합니다.

실무에서 깊이 정밀도를 확보하는 가장 직접적인 방법은 Near Clip Plane을 가능한 한 크게 설정하는 것입니다. 모바일에서는 Near를 0.1 이상으로, PC에서도 0.01 이하로 내리지 않는 것이 일반적입니다.
[그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 다루는 **Reversed-Z** 기법은 깊이 버퍼의 정밀도 분포를 뒤집어 원거리 Z-fighting을 완화하며, Unity는 대부분의 플랫폼에서 이를 기본 적용합니다.

### Viewport Rect

카메라의 출력이 화면에서 차지하는 영역을 0~1 범위의 비율로 지정합니다. 네 개의 값 (X, Y, W, H)으로 구성되며, (X, Y)는 시작 위치, (W, H)는 너비와 높이입니다. 기본값 (0, 0, 1, 1)은 화면 왼쪽 아래 모서리에서 시작하여 전체 화면을 사용한다는 뜻입니다.

<br>

화면 분할(Split Screen)에서는 두 카메라의 Viewport Rect를 각각 (0, 0, 0.5, 1)과 (0.5, 0, 0.5, 1)로 설정하여 좌우로 나눕니다.
왼쪽 카메라는 화면의 왼쪽 절반(X=0, W=0.5)을, 오른쪽 카메라는 오른쪽 절반(X=0.5, W=0.5)을 담당합니다.

PIP(Picture-in-Picture) 효과에서는 (0.7, 0.7, 0.25, 0.25)처럼 설정하여, 화면 오른쪽 위 모서리에 전체 화면의 25% 크기인 작은 뷰를 배치합니다.

<br>

Viewport Rect가 작으면 해당 카메라가 그리는 픽셀 수가 줄어들어 프래그먼트 셰이더 부하가 감소합니다. 다만, 화면 분할이나 PIP 자체가 별도의 카메라를 필요로 하므로, 카메라 추가에 따른 컬링과 렌더링 비용이 함께 발생합니다.

---

## Culling Mask

Camera 컴포넌트의 기본 속성이 "어디를, 어떤 방식으로 투영할 것인가"를 결정한다면, Culling Mask는 "무엇을 그릴 것인가"를 결정합니다.
Unity는 오브젝트에 **레이어(Layer)**를 부여할 수 있으며, 총 32개의 레이어 슬롯이 존재합니다.

Camera의 Culling Mask는 이 32개 레이어 중 카메라가 볼 레이어를 **비트마스크(Bitmask)**로 지정합니다.

<br>

Culling Mask는 성능 측면에서 **컬링보다 먼저 작동한다**는 점이 핵심입니다.
컬링(Culling)은 카메라의 시야 밖에 있는 오브젝트를 렌더링 대상에서 제외하는 연산인데, Culling Mask에 포함되지 않은 레이어의 오브젝트는 이 컬링 연산 자체를 거치지 않고 즉시 제외됩니다.
레이어를 세밀하게 분리하면 카메라마다 처리할 오브젝트 수를 줄일 수 있습니다.

<br>

대표적인 활용 예로 세 가지가 있습니다.

게임 카메라에서 UI 레이어를 제외하면, 3D 씬을 렌더링하는 카메라가 UI 오브젝트를 처리하지 않게 됩니다. UI는 별도의 카메라나 Screen Space - Overlay 모드에서 그리므로, 게임 카메라의 Culling Mask에서 UI 레이어를 빼는 것이 일반적입니다.

미니맵 카메라에는 미니맵 전용 레이어만 포함시켜, 전체 씬 대신 단순화된 메쉬와 아이콘만 그리도록 하면 드로우콜 수를 줄일 수 있습니다.

디버그 시각화 레이어를 별도로 분리하면, 개발 중에는 콜라이더나 경로 등을 시각적으로 확인하다가 릴리즈 시 Culling Mask에서 제거하여 불필요한 렌더링을 방지할 수 있습니다.

<br>

Culling Mask는 **렌더링 전용 필터**입니다.
물리(Physics) 시스템에도 레이어 기반 필터인 **Layer Collision Matrix**가 존재하지만, 이는 물리 충돌 판정에만 적용되며 Culling Mask와는 완전히 독립적입니다.

---

## Clear Flags

Culling Mask가 렌더링 대상을 결정하고 나면, 렌더링 결과가 기록될 버퍼를 어떤 상태에서 시작할지를 정해야 합니다.

<br>

카메라의 렌더링 결과는 **프레임버퍼**라는 메모리 영역에 기록됩니다. 프레임버퍼의 주요 구성 요소는 **컬러 버퍼**(픽셀의 색상)와 **깊이 버퍼**(픽셀의 깊이 값)이며, 필요에 따라 스텐실 버퍼 등이 추가됩니다([래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)에서 전체 구조를 다룹니다).
매 프레임 카메라가 렌더링을 시작할 때, 이전 프레임의 데이터가 이 버퍼들에 남아 있습니다.

<br>

**Clear Flags**는 렌더링 시작 전에 컬러 버퍼와 깊이 버퍼를 초기화할지, 이전 결과를 유지할지를 지정합니다.
Built-in 파이프라인에서는 Camera 컴포넌트의 Clear Flags 드롭다운으로, URP에서는 Camera 컴포넌트의 **Environment > Background Type** 설정(Skybox, Solid Color, Uninitialized)으로 설정합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Clear Flags의 네 가지 옵션</text>

  <!-- === Box 1: Skybox === -->
  <rect x="30" y="40" width="460" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Skybox</text>
  <text x="50" y="82" font-family="sans-serif" font-size="11" fill="currentColor">컬러 버퍼: 스카이박스로 채움</text>
  <text x="50" y="98" font-family="sans-serif" font-size="11" fill="currentColor">깊이 버퍼: 초기화</text>
  <text x="310" y="98" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">용도: 3D 게임의 기본 설정</text>

  <!-- === Box 2: Solid Color === -->
  <rect x="30" y="132" width="460" height="80" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="154" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Solid Color</text>
  <text x="50" y="174" font-family="sans-serif" font-size="11" fill="currentColor">컬러 버퍼: 지정한 단색으로 채움</text>
  <text x="50" y="190" font-family="sans-serif" font-size="11" fill="currentColor">깊이 버퍼: 초기화</text>
  <text x="310" y="190" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">용도: 2D 게임, 스카이박스 불필요 시</text>

  <!-- === Box 3: Depth Only === -->
  <rect x="30" y="224" width="460" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="246" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Depth Only</text>
  <text x="50" y="266" font-family="sans-serif" font-size="11" fill="currentColor">컬러 버퍼: 유지 (이전 카메라의 결과 보존)</text>
  <text x="50" y="282" font-family="sans-serif" font-size="11" fill="currentColor">깊이 버퍼: 초기화</text>
  <text x="310" y="282" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">용도: 멀티 카메라 구성의 핵심</text>

  <!-- === Box 4: Don't Clear === -->
  <rect x="30" y="316" width="460" height="80" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="338" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Don&#39;t Clear</text>
  <text x="50" y="358" font-family="sans-serif" font-size="11" fill="currentColor">컬러 버퍼: 유지</text>
  <text x="50" y="374" font-family="sans-serif" font-size="11" fill="currentColor">깊이 버퍼: 유지</text>
  <text x="310" y="374" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">용도: 특수 효과 (잔상, 모션 트레일 등)</text>
</svg>
</div>

<br>

**Skybox**는 가장 일반적인 설정입니다. 컬러 버퍼를 스카이박스 머티리얼로 채우고, 깊이 버퍼를 초기화합니다. 하늘이 보이는 3D 게임에서 기본으로 사용됩니다.

**Solid Color**는 컬러 버퍼를 지정한 단색으로 채우고, 깊이 버퍼를 초기화합니다. Skybox와 동작 구조는 같지만, 스카이박스 머티리얼을 렌더링하지 않으므로 초기화 비용이 더 낮습니다. 2D 게임이나 스카이박스가 불필요한 장면에서 사용합니다.

<br>

**Depth Only**는 멀티 카메라 구성의 기반이 되는 옵션입니다. 컬러 버퍼를 건드리지 않고, 깊이 버퍼만 초기화합니다.

GPU는 픽셀을 그릴 때 **깊이 테스트**를 수행합니다. 깊이 테스트란, 새로 그리려는 픽셀의 깊이 값을 깊이 버퍼에 저장된 기존 값과 비교하여 더 가까운 픽셀만 컬러 버퍼에 기록하는 과정입니다.

Depth Only는 깊이 버퍼를 최대값(Far Plane)으로 초기화하므로, 현재 카메라가 그리는 모든 오브젝트는 이 최대값보다 가까운 깊이를 가져 깊이 테스트를 통과합니다. 컬러 버퍼는 건드리지 않으므로 이전 카메라가 그린 결과가 그대로 남아 있고, 현재 카메라의 오브젝트가 그 위에 덧그려집니다.

이 특성을 이용하여 FPS 게임에서 무기 카메라가 씬 카메라 위에 무기를 그리거나, UI 카메라가 게임 화면 위에 UI를 그리는 구조를 만듭니다.

<br>

**Don't Clear**는 컬러 버퍼와 깊이 버퍼를 모두 유지합니다. 이전 프레임의 이미지 위에 새 프레임을 덧그리므로, 잔상이나 모션 트레일 같은 특수 효과에 활용할 수 있습니다.

<br>

다만 이 동작은 "이전 프레임의 버퍼가 그대로 남아 있다"는 전제에 의존합니다.
데스크톱 GPU(Immediate Mode Rendering)에서는 프레임버퍼가 메인 메모리에 그대로 유지되므로 이 전제가 성립하지만, 모바일 GPU는 사정이 다릅니다. 모바일 GPU가 사용하는 **TBDR(Tile-Based Deferred Rendering)** 아키텍처는 화면을 작은 타일(보통 16x16 또는 32x32 픽셀)로 나누어 GPU 칩 내부의 고속 타일 메모리에서 렌더링한 뒤, 완성된 타일만 메인 메모리로 기록합니다.
새 프레임이 시작되면 타일 메모리는 비워진 상태에서 출발하므로, Don't Clear를 설정해도 이전 프레임의 이미지가 보존되지 않을 수 있습니다.

따라서 Don't Clear는 플랫폼에 따라 정의되지 않은 동작(undefined behavior)을 보일 수 있으며, 일반적인 게임 렌더링에서는 사용하지 않습니다. 모바일에서 잔상 효과가 필요하면 RenderTexture에 이전 프레임을 명시적으로 저장하고 합성하는 방식이 안전합니다.

### 멀티 카메라 시 Clear Flags 조합

멀티 카메라를 사용할 때, Clear Flags의 조합이 최종 화면을 결정합니다. FPS 게임에서 흔히 사용하는 씬 + 무기 + UI 구성을 예로 듭니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">멀티 카메라 Clear Flags 조합 예시</text>
  <rect x="15" y="36" width="340" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="27" y="54" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">카메라 A (Depth -1): 씬 렌더링</text>
  <text x="27" y="70" font-family="sans-serif" font-size="11" fill="currentColor">Clear Flags: Skybox</text>
  <text x="27" y="84" font-family="sans-serif" font-size="11" fill="currentColor">Culling Mask: 게임 오브젝트 레이어</text>
  <text x="27" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 스카이박스 배경 위에 게임 씬을 그림</text>
  <rect x="390" y="36" width="135" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="457" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 렌더링</text>
  <text x="457" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(스카이박스 + 오브젝트)</text>
  <line x1="355" y1="72" x2="386" y2="72" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="386,67 393,72 386,77" fill="currentColor"/>
  <line x1="457" y1="108" x2="457" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="457,136 452,130 462,130" fill="currentColor"/>
  <text x="500" y="124" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">A의 결과</text>
  <text x="500" y="134" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">위에 무기</text>
  <rect x="15" y="140" width="340" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="27" y="158" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">카메라 B (Depth 0): 무기 렌더링</text>
  <text x="27" y="174" font-family="sans-serif" font-size="11" fill="currentColor">Clear Flags: Depth Only  |  Culling Mask: 무기 레이어</text>
  <text x="27" y="190" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 카메라 A의 결과(컬러) 위에 무기를 그림</text>
  <text x="27" y="204" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 깊이만 초기화하여 무기가 씬에 묻히지 않음</text>
  <rect x="390" y="140" width="135" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="457" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">무기 렌더링</text>
  <text x="457" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(A 결과 + 무기)</text>
  <line x1="355" y1="176" x2="386" y2="176" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="386,171 393,176 386,181" fill="currentColor"/>
  <line x1="457" y1="212" x2="457" y2="234" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="457,240 452,234 462,234" fill="currentColor"/>
  <text x="500" y="228" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">A+B의 결과</text>
  <text x="500" y="238" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">위에 UI</text>
  <rect x="15" y="244" width="340" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="27" y="262" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">카메라 C (Depth 1): UI 렌더링</text>
  <text x="27" y="278" font-family="sans-serif" font-size="11" fill="currentColor">Clear Flags: Depth Only  |  Culling Mask: UI 레이어</text>
  <text x="27" y="294" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 카메라 A+B의 결과(컬러) 위에 UI를 그림</text>
  <rect x="390" y="244" width="135" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="457" y="270" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">UI 렌더링</text>
  <text x="457" y="286" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(A+B 결과 + UI)</text>
  <line x1="355" y1="275" x2="386" y2="275" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="386,270 393,275 386,280" fill="currentColor"/>
  <rect x="100" y="320" width="340" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="338" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">최종 화면 = 카메라 A + B + C</text>
</svg>
</div>

<br>

카메라 B와 C의 Clear Flags가 Depth Only이므로, 이전 카메라의 컬러 결과를 보존하면서 자신의 렌더링 대상만 추가로 그립니다.

만약 카메라 B의 Clear Flags가 Skybox나 Solid Color였다면, 카메라 A의 결과가 덮어씌워져 보이지 않게 됩니다.

---

## 렌더링 순서

Culling Mask로 "무엇을 그릴 것인가"가, Clear Flags로 "배경을 어떻게 채울 것인가"가 결정되면, 남은 문제는 "어떤 순서로 그릴 것인가"입니다.
Unity에서 오브젝트가 화면에 그려지는 순서는 Camera Depth → Sorting Layer → Order in Layer → Render Queue → 거리 기반 정렬 순으로 결정됩니다. 앞쪽 기준의 값이 같을 때만 다음 기준으로 넘어가는 구조입니다. 이 중 Sorting Layer와 Order in Layer는 Sprite Renderer, Tilemap 같은 2D 요소의 앞뒤를 제어하는 데 주로 쓰이고, 3D 오브젝트의 순서는 Camera Depth, Render Queue, 거리 기반 정렬이 결정합니다.

### Camera Depth

가장 상위의 정렬 기준입니다. **카메라 간 렌더링 순서**를 결정하며, Camera 컴포넌트의 Depth 속성으로 지정합니다.
낮은 값의 카메라가 먼저 렌더링되고, 높은 값의 카메라가 나중에 렌더링됩니다.
Clear Flags 섹션에서 본 멀티 카메라 예시에서 카메라 A(Depth -1)가 먼저, 카메라 C(Depth 1)가 마지막에 렌더링되는 것이 Camera Depth에 의한 것입니다.

### Sorting Layer

2D 오브젝트(Sprite Renderer, Tilemap 등)의 렌더링 순서를 결정하는 기준입니다.
Project Settings > Tags and Layers에서 정의하며, 목록에서 위에 있는 레이어가 먼저 그려지고, 아래에 있는 레이어가 나중에 그려져 위에 표시됩니다.

<br>

뒤에서 다루는 Render Queue가 셰이더 수준에서 순서를 지정하는 것과 달리, Sorting Layer는 **오브젝트 수준**에서 순서를 제어합니다.
같은 머티리얼을 사용하는 스프라이트들 사이에서도 Sorting Layer를 분리하면 렌더링 순서를 명시적으로 지정할 수 있습니다.
예를 들어 배경(Background) → 지형(Terrain) → 캐릭터(Character) → 전경(Foreground) 순으로 Sorting Layer를 구성하면, 배경이 가장 먼저 그려지고 전경이 가장 나중에 그려져 앞뒤 관계가 일관되게 유지됩니다.

### Order in Layer

같은 Sorting Layer 내에서 렌더링 순서를 세분화하는 정수 값입니다. 작은 값이 먼저 그려지고, 큰 값이 나중에 그려져 위에 표시됩니다. 예를 들어, 위에서 구성한 "Character" Sorting Layer 안에 NPC(Order 0)와 플레이어(Order 1)가 있으면, NPC가 먼저 그려지고 플레이어가 그 위에 표시됩니다.
Sorting Layer가 배경·캐릭터·전경 같은 레이어 간 순서를 정하고, Order in Layer가 같은 레이어 안의 개별 오브젝트 간 순서를 정하는 구조입니다.

### Render Queue

오브젝트 수준에서 순서를 제어하는 Sorting Layer와 달리, **셰이더 수준**에서 지정하는 렌더링 순서입니다. 셰이더의 SubShader 블록에서 `Tags { "Queue" = "..." }`로 지정하거나, 머티리얼 인스펙터에서 직접 값을 설정합니다.

<br>

**Render Queue 기본값**

| 이름 | 값 | 설명 |
|------|-----|------|
| Background | 1000 | 배경 (스카이박스 등) |
| Geometry | 2000 | 불투명 오브젝트 (기본값) |
| AlphaTest | 2450 | 알파 테스트 오브젝트 |
| Transparent | 3000 | 반투명 오브젝트 |
| Overlay | 4000 | 오버레이 효과 (렌즈 플레어 등) |

Render Queue 값이 2500 이하이면 불투명(Opaque)으로, 2501 이상이면 반투명(Transparent)으로 분류됩니다. Opaque는 Front-to-Back(가까운 것 먼저), Transparent는 Back-to-Front(먼 것 먼저)로 정렬되며, 이 분류에 따라 이후의 거리 기반 정렬 방향이 달라집니다.

### 정렬 우선순위 계층

위 네 가지 기준에 거리 기반 정렬을 더한 다섯 단계가 계층적으로 적용됩니다. 상위 기준의 값이 같을 때만 하위 기준이 순서를 결정합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더링 순서 결정 계층</text>
  <!-- Level 1: Camera Depth -->
  <rect x="30" y="36" width="400" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="56" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) Camera Depth</text>
  <text x="230" y="72" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">카메라 간 순서 (가장 상위)</text>
  <text x="230" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Depth가 낮은 카메라 → 먼저 렌더링</text>
  <!-- Arrow 1→2 -->
  <line x1="230" y1="96" x2="230" y2="112" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,118 225,112 235,112" fill="currentColor"/>
  <!-- Level 2: Sorting Layer -->
  <rect x="30" y="122" width="400" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="142" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) Sorting Layer</text>
  <text x="230" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">같은 카메라 안에서의 레이어 순서</text>
  <text x="230" y="174" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">목록 상위 → 먼저 렌더링</text>
  <!-- Arrow 2→3 -->
  <line x1="230" y1="182" x2="230" y2="198" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,204 225,198 235,198" fill="currentColor"/>
  <!-- Level 3: Order in Layer -->
  <rect x="30" y="208" width="400" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="228" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) Order in Layer</text>
  <text x="230" y="244" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">같은 Sorting Layer 안에서의 순서</text>
  <text x="230" y="260" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">값이 작은 것 → 먼저 렌더링</text>
  <!-- Arrow 3→4 -->
  <line x1="230" y1="268" x2="230" y2="284" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,290 225,284 235,284" fill="currentColor"/>
  <!-- Level 4: Render Queue -->
  <rect x="30" y="294" width="400" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="314" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(4) Render Queue</text>
  <text x="230" y="330" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">같은 Order in Layer 안에서의 셰이더 순서</text>
  <text x="230" y="346" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">값이 작은 것 → 먼저 렌더링</text>
  <!-- Arrow 4→5 -->
  <line x1="230" y1="354" x2="230" y2="370" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,376 225,370 235,370" fill="currentColor"/>
  <!-- Level 5: 거리 기반 정렬 (with two sub-items) -->
  <rect x="30" y="380" width="400" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="400" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(5) 거리 기반 정렬</text>
  <!-- Opaque sub-item -->
  <rect x="50" y="410" width="170" height="36" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="135" y="425" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Opaque</text>
  <text x="135" y="440" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Front-to-Back (가까운 것 먼저)</text>
  <!-- Transparent sub-item -->
  <rect x="240" y="410" width="170" height="36" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="325" y="425" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Transparent</text>
  <text x="325" y="440" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Back-to-Front (먼 것 먼저)</text>
</svg>
</div>

<br>

대부분의 3D 게임에서 Sorting Layer와 Order in Layer는 2D 요소에만 활용되며, 3D 오브젝트의 순서는 Render Queue와 거리 기반 정렬에 의해 결정됩니다.

---

## Opaque 정렬 -- Front-to-Back

렌더링 순서 계층의 마지막 단계인 "거리 기반 정렬"은 불투명과 반투명에서 정반대 방향으로 동작합니다. 먼저 불투명 정렬을 살펴봅니다.

Render Queue 값이 2500 이하인 오브젝트는 불투명(Opaque)으로 분류됩니다. Unity는 불투명 오브젝트를 **카메라에서 가까운 순서(Front-to-Back)**로 정렬하여 그립니다.

<br>

가까운 오브젝트를 먼저 그리는 이유는 **오버드로우(Overdraw)**를 줄이기 위해서입니다. 오버드로우란 같은 픽셀 위치에 여러 오브젝트의 색상이 중복으로 계산되는 현상입니다. GPU는 픽셀을 그릴 때 프래그먼트 셰이더를 실행하여 색상을 계산하는데, 이 연산은 비용이 높습니다. 뒤에 가려질 픽셀의 셰이더까지 실행하는 것은 GPU 자원의 낭비이며, 프래그먼트 셰이더가 복잡할수록 낭비가 커집니다.

<br>

이 낭비를 줄이는 GPU 기능이 **Early-Z 테스트**입니다. Early-Z는 프래그먼트 셰이더를 실행하기 전에 해당 픽셀의 깊이 값을 먼저 비교합니다. 이미 가까운 오브젝트가 그려져 깊이 버퍼에 기록되어 있으면, 뒤에 있는 오브젝트의 프래그먼트는 깊이 테스트에서 탈락하여 셰이더 실행 자체가 생략됩니다. 가까운 오브젝트를 먼저 그려야 깊이 버퍼에 비교 기준이 채워지므로, Front-to-Back 정렬과 Early-Z는 함께 맞물려 오버드로우를 방지합니다.

<br>

Unity는 불투명 오브젝트에 대해 Front-to-Back 정렬을 자동으로 적용합니다. 개발자가 별도로 정렬을 지정하지 않아도, Render Queue 2500 이하의 오브젝트는 엔진 내부에서 카메라와의 거리 순으로 정렬됩니다.

<br>

앞서 설명한 대로 Early-Z가 동작하려면 먼저 그려진 오브젝트가 깊이 버퍼에 자신의 깊이 값을 기록해 두어야 합니다. 이 깊이 기록을 제어하는 셰이더 설정이 **깊이 쓰기(Depth Write, `ZWrite`)**입니다. 불투명 셰이더의 기본 설정은 `ZWrite On`이므로, 일반적인 불투명 머티리얼에서는 Front-to-Back 정렬과 Early-Z가 자동으로 맞물려 동작합니다.

---

## Transparent 정렬 -- Back-to-Front

Render Queue 값이 2501 이상인 오브젝트는 반투명(Transparent)으로 분류됩니다.
Unity는 **불투명 오브젝트를 모두 먼저 그린 뒤, 반투명 오브젝트를 그립니다.** 반투명 오브젝트끼리의 정렬 방향은 불투명과 정반대로, **카메라에서 먼 순서(Back-to-Front)**입니다.

먼 것부터 그리는 이유는 **알파 블렌딩(Alpha Blending)**의 특성에 있습니다.
알파 블렌딩은 현재 프래그먼트의 색상과 프레임버퍼에 이미 기록된 색상을 투명도에 따라 혼합하는 연산입니다. 알파 값(Alpha)은 0.0(완전 투명)에서 1.0(완전 불투명) 사이의 투명도 정보입니다. 이 연산이 올바르게 동작하려면, 뒤에 있는 오브젝트의 색상이 먼저 프레임버퍼에 존재해야 합니다.

<br>

### 반투명의 성능 비용

반투명 오브젝트는 불투명 오브젝트에 비해 렌더링 비용이 높습니다. 반투명 셰이더는 **깊이 쓰기를 비활성화(`ZWrite Off`)**하기 때문입니다.
반투명 오브젝트가 깊이 값을 기록하면, 이후에 그려지는 다른 반투명 프래그먼트가 깊이 테스트에서 탈락하여 블렌딩에 참여하지 못합니다. 알파 블렌딩은 겹치는 모든 반투명 프래그먼트의 색상을 혼합해야 올바른 결과가 나오므로, 반투명 오브젝트는 깊이 버퍼에 기록하지 않습니다.

깊이 쓰기가 없으면 반투명 오브젝트끼리는 Early-Z로 서로를 걸러낼 수 없어, 같은 픽셀 위치에 겹치는 반투명 프래그먼트가 모두 셰이더를 실행합니다.
불투명 오브젝트는 반투명보다 먼저 그려지고 깊이 버퍼에 기록되므로, 불투명 오브젝트 뒤에 완전히 가려진 반투명 프래그먼트는 깊이 테스트에서 걸러집니다.
하지만 반투명끼리 겹치는 영역에서는 걸러낼 수단이 없습니다. 반투명 오브젝트가 겹칠수록 오버드로우가 직접적으로 증가하는 구조입니다.

### 반투명의 정렬 한계

비용 외에 정확성 문제도 있습니다.
반투명 오브젝트의 **정렬 기준은 바운딩 박스(Bounding Box)의 중심**입니다. 바운딩 박스는 오브젝트의 메쉬를 감싸는 최소 크기의 직육면체이며, Unity는 이 바운딩 박스의 중심(`Renderer.bounds.center`)과 카메라 사이의 거리를 기준으로 정렬합니다.
대부분의 경우 올바르게 동작하지만, 큰 메쉬가 서로 교차하거나 바운딩 박스의 중심이 실제 표면 위치와 크게 다르면 정렬 오류가 발생합니다. 이 오류는 반투명 표면이 깜빡이거나 앞뒤가 뒤바뀌어 보이는 시각적 결함으로 나타납니다.

<br>

이 정렬 오류를 완전히 해결하려면 Order-Independent Transparency(OIT)가 필요합니다.
OIT는 정렬 순서에 의존하지 않고 픽셀 단위에서 올바른 블렌딩을 수행하는 기법이지만, 모바일에서는 추가 메모리와 GPU 연산 비용이 큽니다. 실무에서는 반투명 메쉬가 서로 교차하지 않도록 배치하거나, 반투명 오브젝트 수 자체를 줄이는 것이 현실적인 대응입니다.

---

## 멀티 카메라 비용

지금까지 카메라 한 대가 씬을 렌더링하는 과정을 살펴보았습니다. 실제 프로젝트에서는 카메라가 여러 대 필요한 경우가 많은데, 카메라 수 증가는 곧 성능 비용 증가입니다.
Unity에서 활성화된 카메라 하나당 씬의 오브젝트를 절두체와 비교하는 **컬링이 1회**, 컬링을 통과한 오브젝트를 화면에 그리는 **렌더링이 1회** 실행됩니다. 카메라가 하나 추가될 때마다 이 과정이 통째로 반복되므로, CPU와 GPU 양쪽에서 비용이 발생합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">카메라 추가 시 발생하는 비용</text>

  <!-- CPU section label -->
  <text x="40" y="56" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <line x1="70" y1="52" x2="490" y2="52" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- (1) 컬링 -->
  <rect x="40" y="66" width="440" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="86" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) 컬링 연산</text>
  <text x="56" y="106" font-family="sans-serif" font-size="11" fill="currentColor">씬의 오브젝트를 절두체와 비교</text>
  <text x="310" y="106" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Culling Mask + Frustum Culling</text>

  <!-- Arrow -->
  <line x1="260" y1="122" x2="260" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,144 255,138 265,138" fill="currentColor"/>

  <!-- (2) 드로우콜 -->
  <rect x="40" y="148" width="440" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="168" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) 드로우콜 생성</text>
  <text x="56" y="188" font-family="sans-serif" font-size="11" fill="currentColor">컬링 통과 오브젝트에 대해 드로우콜 구성</text>
  <text x="310" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">SetPassCall 증가</text>

  <!-- GPU section label -->
  <text x="40" y="230" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU</text>
  <line x1="70" y1="226" x2="490" y2="226" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- (3) 렌더링 패스 -->
  <rect x="40" y="240" width="440" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="260" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) 렌더링 패스</text>
  <text x="56" y="280" font-family="sans-serif" font-size="11" fill="currentColor">Opaque → Transparent → Post-Processing 전체 재실행</text>

  <!-- Arrow -->
  <line x1="260" y1="296" x2="260" y2="312" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,318 255,312 265,312" fill="currentColor"/>

  <!-- (4) Clear -->
  <rect x="40" y="322" width="440" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="342" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(4) Clear 비용</text>
  <text x="56" y="358" font-family="sans-serif" font-size="11" fill="currentColor">Clear Flags에 따른 버퍼 초기화 + Render Target 전환</text>
</svg>
</div>

<br>

게임 카메라 1대만으로 렌더링하는 것이 가장 가볍습니다. 하지만 실제 프로젝트에서는 UI 카메라, 미니맵 카메라, 무기/손 카메라(FPS), 거울/포탈 카메라 등 다양한 이유로 추가 카메라가 필요해집니다.

### 비용 최소화 전략

추가 카메라가 필요한 상황에서도 비용을 줄이는 방법이 있습니다.

<br>

**UI에는 Screen Space - Overlay 모드를 사용합니다.**
Canvas의 Render Mode를 Screen Space - Overlay로 설정하면 별도의 카메라 없이 UI가 렌더링됩니다. Screen Space - Camera 모드는 별도의 카메라를 할당해야 하므로 카메라 비용이 추가됩니다. UI가 3D 씬 위에 올라가기만 하는 구조라면 Overlay가 적합합니다.

다만 URP에서는 주의할 점이 있습니다. URP가 포스트 프로세싱을 적용할 때, 3D 씬은 화면에 직접 그려지지 않고 중간 Render Target(오프스크린 버퍼)에 먼저 렌더링됩니다.
그런데 Screen Space - Overlay UI는 렌더 파이프라인 바깥에서 동작하므로, 이 중간 버퍼가 아닌 최종 화면 버퍼(Back Buffer)에 직접 그려집니다. 결과적으로 3D 씬의 중간 버퍼를 화면 버퍼로 복사하는 Blit 패스가 추가로 발생합니다.
이 추가 비용이 문제가 되면, 아래에서 설명하는 URP Camera Stacking의 Overlay Camera와 Screen Space - Camera 모드를 조합하여 UI를 3D 씬과 동일한 렌더링 흐름에 포함시키는 방법이 있습니다.

<br>

**Culling Mask를 최소화합니다.**
추가 카메라가 필요하더라도, Culling Mask를 해당 카메라의 목적에 맞는 레이어로만 제한하면 컬링과 드로우콜 비용을 줄일 수 있습니다. 미니맵 카메라가 전체 씬 대신 미니맵 전용 간소화 오브젝트만 그리면, 드로우콜 수가 크게 줄어듭니다.

<br>

**매 프레임 렌더링하지 않습니다.**
미니맵이나 거울처럼 매 프레임 갱신이 필요하지 않은 카메라는, 일정 프레임 간격으로만 렌더링하여 비용을 분산합니다. Camera 컴포넌트를 비활성화했다가 필요한 프레임에서만 활성화하거나, RenderTexture에 결과를 캐싱하는 방식입니다.

### URP의 Camera Stacking

URP에서는 **Camera Stacking** 방식으로 멀티 카메라를 관리합니다. Base Camera 위에 Overlay Camera를 쌓는 구조입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP Camera Stacking</text>

  <!-- Outer box: Base Camera -->
  <rect x="30" y="36" width="420" height="280" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="58" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Base Camera</text>
  <text x="50" y="76" font-family="sans-serif" font-size="11" fill="currentColor">Render Type: Base</text>
  <text x="50" y="94" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">씬 렌더링 (풀 파이프라인 실행)</text>

  <!-- Inner box: Stack list -->
  <rect x="50" y="108" width="380" height="170" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="66" y="128" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Stack 리스트 (위에서 아래 순서로 실행):</text>

  <!-- Sub-box 1: Overlay Camera A -->
  <rect x="66" y="138" width="348" height="56" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="82" y="157" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Overlay Camera A</text>
  <text x="82" y="173" font-family="sans-serif" font-size="10" fill="currentColor">Render Type: Overlay</text>
  <text x="82" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Base 위에 추가 렌더링</text>

  <!-- Divider -->
  <line x1="80" y1="200" x2="400" y2="200" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Sub-box 2: Overlay Camera B -->
  <rect x="66" y="206" width="348" height="56" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="82" y="225" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Overlay Camera B</text>
  <text x="82" y="241" font-family="sans-serif" font-size="10" fill="currentColor">Render Type: Overlay</text>
  <text x="82" y="256" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">A 위에 추가 렌더링</text>

  <!-- Annotations below stack -->
  <text x="240" y="298" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">렌더링 순서 = Stack 리스트 순서</text>
  <text x="240" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(Overlay Camera의 Depth 속성은 무관)</text>
</svg>
</div>

<br>

Built-in 파이프라인에서는 각 카메라가 독립적으로 렌더링을 실행하고, Camera Depth 값으로 순서를 결정합니다.
URP의 Camera Stacking에서는 Overlay Camera가 독립적으로 실행되지 않고, Base Camera가 자신의 렌더링을 마친 직후 Stack 리스트에 등록된 순서대로 Overlay Camera를 차례로 실행합니다.
따라서 Overlay Camera의 렌더링 순서는 Camera Depth 속성이 아니라 **Stack 리스트의 등록 순서**로 결정됩니다.

<br>

Built-in 파이프라인에서는 독립 카메라마다 별도의 Render Target 할당과 전환이 발생하지만, URP의 Camera Stacking에서는 Overlay Camera가 Base Camera의 Render Target에 직접 그리므로 전환 비용이 줄어듭니다.
다만, Overlay Camera가 추가될 때마다 컬링과 드로우콜이 증가하는 점은 동일하므로, 카메라 수를 최소화하는 원칙은 변하지 않습니다.

---

## 마무리

이 글에서 살펴본 내용을 정리하면:

- Projection과 Near/Far Clip Plane이 가시 범위와 깊이 정밀도를 결정하며, Far/Near 비율이 클수록 Z-fighting 위험이 증가합니다
- Culling Mask는 레이어 비트마스크로 렌더링 대상을 필터링하며, 물리 시스템의 Layer Collision Matrix와는 독립적으로 동작합니다
- Clear Flags는 프레임버퍼의 초기화 방식을 결정하며, 멀티 카메라 구성에서 Depth Only가 핵심 역할을 합니다
- 렌더링 순서는 Camera Depth > Sorting Layer > Order in Layer > Render Queue > 거리 기반 정렬의 계층 구조를 따릅니다
- 불투명은 Front-to-Back 정렬로 Early-Z를 활용하고, 반투명은 Back-to-Front 정렬로 알파 블렌딩을 수행하되 ZWrite Off로 인해 오버드로우 비용이 높습니다
- 반투명의 정렬 기준은 바운딩 박스 중심이므로, 메쉬가 교차하거나 바운딩 박스 중심과 표면 위치가 크게 다르면 정렬 오류가 발생합니다
- 카메라 하나가 추가될 때마다 컬링과 렌더링이 한 사이클 추가되므로, 카메라 수를 최소화하는 것이 성능 관리의 기본입니다

<br>

카메라의 투영 방식과 가시 범위가 렌더링 대상의 범위를 결정하고, Culling Mask가 그 범위를 레이어 단위로 좁히며, Clear Flags가 프레임 간 결과의 보존 여부를 결정하고, 렌더링 순서 계층이 최종 픽셀 출력의 앞뒤를 확정합니다.
이 네 가지가 카메라에서 렌더 파이프라인으로 전달되는 입력 조건의 전부입니다.

카메라가 무엇을 어떤 순서로 그리는지를 확인했습니다. 이 글에서 "프레임버퍼에 기록된다", "컬러 버퍼", "깊이 버퍼"라는 표현이 여러 번 등장했는데, 이 버퍼들이 실제로 어떤 구조이며 어떻게 관리되는지에 따라 렌더링 성능이 달라집니다.

[Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)에서는 Back Buffer와 RenderTexture의 구조, Render Target 전환이 모바일 GPU에 미치는 영향, 그리고 해상도와 컬러 포맷에 따른 메모리 비용을 다룹니다.

<br>

---

**관련 글**
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)

**시리즈**
- **Unity 렌더링 (1) - Camera와 Rendering Layer (현재 글)**
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)

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
- **Unity 렌더링 (1) - Camera와 Rendering Layer** (현재 글)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
