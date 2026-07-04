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

이 시리즈는 Unity가 화면을 그려내는 과정을 처음부터 따라가며 렌더링 시스템의 기초를 정리합니다. 카메라가 무엇을 어떤 순서로 그리는지를 이 글에서 먼저 다루고, 그렇게 그려진 결과가 어디에 저장되는지를 [Unity 렌더링 (2)](/dev/unity/UnityRendering-2/)에서, 이 모든 과정을 하나로 엮는 렌더 파이프라인이 어떤 종류로 나뉘고 무엇을 기준으로 선택하는지를 [Unity 렌더링 (3)](/dev/unity/UnityRendering-3/)에서 이어 살펴봅니다. 컬링과 정렬, 라이팅, 드로우콜 생성을 다루는 [Unity 렌더 파이프라인](/dev/unity/UnityPipeline-1/) 시리즈도 여기서 정리하는 내용을 토대로 합니다.

Unity에서 씬의 오브젝트는 **카메라(Camera)**를 기준으로 화면에 투영됩니다. 씬에 MeshRenderer나 SpriteRenderer가 있어도, 어떤 카메라의 가시 영역에도 들어오지 않으면 최종 화면에는 그려지지 않습니다.

카메라는 렌더 파이프라인에 넘길 입력 범위를 정합니다. Transform은 시점과 방향을, Projection과 Field of View는 보이는 공간의 형태와 크기를, Culling Mask는 렌더링 대상 레이어를 결정합니다. 렌더 파이프라인은 이 조건에 맞는 오브젝트를 추리고 정렬한 뒤 그리기 명령을 만듭니다. 따라서 렌더링 비용을 조절하려면 카메라가 무엇을 보게 만들고, 무엇을 제외하게 만들지부터 확인해야 합니다.

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

그림의 네 결정은 대부분 카메라 컴포넌트의 설정에서 시작됩니다. 기본 속성은 시점과 투영 범위를 정하고, Culling Mask는 렌더링 후보에 포함할 레이어를 고릅니다. Clear Flags는 카메라가 그리기 전에 화면이나 깊이 버퍼를 어떻게 초기화할지 정합니다.

그 뒤 렌더 파이프라인은 카메라가 고른 대상을 컬링하고, 불투명 오브젝트와 투명 오브젝트를 각 규칙에 맞게 정렬한 뒤 그리기 명령을 만듭니다. 아래에서는 이 흐름을 카메라 속성에서 시작해 Culling Mask, Clear Flags, 렌더링 순서로 이어서 봅니다.

---

## Camera 컴포넌트

Camera는 게임 오브젝트에 붙는 컴포넌트입니다. 따라서 카메라의 위치와 방향은 별도 값이 아니라, 그 게임 오브젝트의 Transform으로 결정됩니다. 오브젝트를 이동하면 시점이 이동하고, 오브젝트를 회전하면 바라보는 방향도 함께 바뀝니다.

Camera 컴포넌트는 이 Transform을 기준으로 어떤 공간을 화면에 투영할지 정합니다. 투영 방식, 시야각, 클리핑 범위, 렌더링할 레이어 같은 설정이 여기에 포함됩니다. 렌더 파이프라인은 이 설정을 입력으로 받아 보이는 오브젝트를 추리고, 화면에 그릴 명령을 구성합니다.

### Projection: 투영 방식

Projection은 3D 공간의 좌표를 2D 화면으로 옮기는 방식을 정합니다. 같은 씬이라도 투영 방식이 달라지면 거리감이 달라지고, 카메라가 보게 되는 공간의 형태도 달라집니다.

**Perspective(원근 투영)**는 가까운 물체를 크게, 먼 물체를 작게 그립니다. 사람의 시각과 비슷한 거리감을 만들 수 있어 3D 게임에서 가장 흔히 사용됩니다. 이 방식에서 카메라가 보는 영역은 [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 다룬 **절두체(Frustum)**입니다. 절두체는 카메라에서 멀어질수록 단면이 넓어지는 형태이므로, 먼 거리일수록 더 넓은 공간이 가시 영역에 포함될 수 있습니다.

**Orthographic(직교 투영)**은 거리와 무관하게 같은 크기의 물체를 화면에서도 같은 크기로 그립니다. 원근감이 사라지는 대신 크기와 비율을 일정하게 유지할 수 있어 2D 게임, UI, 에디터용 뷰처럼 거리 표현보다 정확한 배치가 중요한 화면에 잘 맞습니다. 직교 투영의 가시 영역은 깊이 방향으로 크기가 변하지 않는 직육면체에 가깝습니다.

이 차이는 렌더링 후보를 고르는 방식에도 영향을 줍니다. 원근 투영은 멀리 갈수록 가시 영역이 넓어지고, 직교 투영은 카메라 위치와 Orthographic Size가 정한 일정한 영역 안에서 후보가 결정됩니다. 결국 투영 방식은 화면의 느낌뿐 아니라, 컬링 전에 카메라가 검사해야 하는 공간의 형태까지 함께 바꿉니다.

### Field of View (FOV)

FOV(Field of View)는 원근 투영에서 카메라의 수직 시야각을 정하는 값입니다. Unity의 기본값은 60도이며, 이 각도가 커질수록 카메라는 위아래로 더 넓은 범위를 봅니다. 직교 투영에서는 가시 영역의 크기를 FOV가 아니라 Orthographic Size가 정하므로, FOV는 원근 투영에서만 의미를 가집니다.

FOV를 키우면 절두체가 넓어져 한 화면에 더 많은 공간이 들어옵니다. 화면을 넓게 잡을 수 있는 대신, 가시 영역에 포함되는 오브젝트도 늘어날 수 있습니다. 렌더 파이프라인 입장에서는 컬링해야 할 후보가 많아지고, 실제로 화면에 남는 오브젝트가 많다면 드로우콜과 픽셀 처리 비용도 함께 늘어납니다.

반대로 FOV를 줄이면 화면에 들어오는 공간은 좁아집니다. 보이는 대상 수는 줄어들 수 있지만, 남은 오브젝트는 화면에서 더 크게 보입니다. 그래서 FOV는 단순한 연출 값이 아니라, 화면 구성과 렌더링 비용을 함께 바꾸는 카메라 설정입니다.

### Near/Far Clip Plane

Near/Far Clip Plane은 카메라가 볼 깊이 범위를 정하는 두 절단면입니다. **Near Clip Plane**보다 카메라에 가까운 오브젝트와 **Far Clip Plane**보다 먼 오브젝트는 렌더링 후보에서 제외됩니다. 따라서 이 값은 단순히 보이는 거리를 정하는 설정이면서, 동시에 깊이 버퍼 정밀도에도 영향을 줍니다.

깊이 버퍼(Depth Buffer)는 화면의 각 픽셀에 가장 앞에 있는 표면의 깊이를 저장합니다. 하지만 저장 가능한 단계 수는 24비트나 32비트처럼 처음부터 한정되어 있고, 이 제한된 단계 안에 Near부터 Far까지의 깊이를 나누어 담아야 합니다. Near와 Far 사이가 넓어질수록 같은 단계 수로 더 긴 거리를 표현해야 하므로, 서로 가까운 두 표면을 구분하기가 어려워집니다.

여기에 원근 투영의 깊이 매핑 방식이 겹칩니다. [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 다룬 것처럼, 원근 투영은 카메라 공간의 깊이를 NDC(정규화 장치 좌표)로 옮길 때 거리를 균등하게 나누지 않습니다. 깊이 값은 Near 근처에서 촘촘하게 변하고, Far 쪽으로 갈수록 같은 깊이 값 차이가 더 큰 실제 거리 차이를 뜻하게 됩니다.

아래 그림은 Near와 Far의 비율이 달라질 때 깊이 정밀도 분포가 어떻게 달라지는지를 단순화해 보여 줍니다.

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

결과적으로 Far를 Near로 나눈 비율이 커질수록 깊이 값은 먼 거리에서 더 성기게 배치됩니다. 이때 가까이 붙은 두 표면이 같은 픽셀을 차지하면, 깊이 버퍼가 어느 표면을 앞에 둘지 안정적으로 구분하지 못할 수 있습니다. 화면에서는 두 면이 번갈아 보이거나 깜빡이는 것처럼 나타나는데, 이 현상을 **Z-fighting**이라고 부릅니다.

기본 원칙은 Near를 허용 가능한 범위 안에서 멀리 두고, Far는 실제로 필요한 거리까지만 두는 것입니다. Near를 너무 작게 잡으면 아주 가까운 영역에 깊이 정밀도가 과하게 배정되고, 그만큼 먼 거리의 정밀도가 줄어듭니다. 반대로 Far를 필요 이상으로 크게 잡아도 같은 단계 수로 더 넓은 깊이 범위를 표현해야 하므로 정밀도가 낮아집니다.

실무에서는 카메라 앞에 매우 가까운 오브젝트를 그려야 하는 경우가 아니라면 Near를 과도하게 낮추지 않는 편이 좋습니다. 모바일에서는 Near를 0.1 이상에서 시작하는 경우가 많고, PC에서도 특별한 이유 없이 0.01 아래로 낮추는 설정은 피하는 편이 안전합니다. [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 다룬 **Reversed-Z**는 먼 거리의 깊이 정밀도를 개선하는 기법이며, Unity는 지원 플랫폼에서 이를 자동으로 적용합니다. 다만 Reversed-Z가 있더라도 Near/Far 범위를 필요한 만큼만 잡는 원칙은 그대로 중요합니다.

### Viewport Rect

Viewport Rect는 카메라가 렌더링한 결과를 화면의 어느 영역에 배치할지 정합니다. 값은 `(X, Y, W, H)` 네 개이며 모두 0부터 1 사이의 비율로 해석됩니다. `X`와 `Y`는 출력 영역의 시작 위치, `W`와 `H`는 너비와 높이입니다. 기본값 `(0, 0, 1, 1)`은 화면 왼쪽 아래에서 시작해 전체 화면을 채운다는 뜻입니다.

이 값을 조정하면 여러 카메라가 한 화면을 나누어 사용할 수 있습니다. 화면 분할(Split Screen)에서는 왼쪽 카메라를 `(0, 0, 0.5, 1)`, 오른쪽 카메라를 `(0.5, 0, 0.5, 1)`로 두어 화면을 반씩 나눌 수 있습니다. PIP(Picture-in-Picture)처럼 작은 보조 화면이 필요하다면 `(0.7, 0.7, 0.25, 0.25)`처럼 전체 화면의 일부 영역만 차지하도록 배치할 수 있습니다.

Viewport Rect가 작아지면 그 카메라가 채워야 할 픽셀 수가 줄어듭니다. 따라서 프래그먼트 셰이더와 후처리처럼 픽셀 수에 비례하는 비용은 낮아질 수 있습니다. 다만 화면 분할이나 PIP는 보통 카메라를 추가하는 방식으로 구성되므로, 카메라가 늘어난 만큼 컬링, 정렬, 드로우콜 생성 같은 카메라 단위 비용도 함께 생깁니다.

---

## Culling Mask

Culling Mask는 카메라가 렌더링 대상으로 삼을 레이어를 정하는 필터입니다. Projection, FOV, Clip Plane이 카메라가 볼 공간을 정한다면, Culling Mask는 그 공간 안에서도 어떤 레이어의 오브젝트를 후보로 둘지 결정합니다. 같은 위치에서 같은 방향을 바라보는 카메라라도 Culling Mask가 다르면 서로 다른 오브젝트를 그릴 수 있습니다.

기준이 되는 값은 GameObject의 **레이어(Layer)**입니다. Unity는 오브젝트마다 32개 레이어 중 하나를 지정할 수 있고, Culling Mask는 이 레이어들을 **비트마스크(Bitmask)**로 저장합니다. 마스크에 포함된 레이어의 Renderer만 해당 카메라의 렌더링 후보가 되며, 포함되지 않은 레이어의 Renderer는 화면 안에 있더라도 그 카메라에서는 제외됩니다.

성능 측면에서는 카메라별 후보 집합을 줄인다는 점이 중요합니다. 프러스텀 컬링은 카메라의 가시 영역을 기준으로 오브젝트를 제외하고, Culling Mask는 레이어 조건으로 같은 후보 집합을 제한합니다. 따라서 특정 카메라가 볼 필요 없는 오브젝트를 별도 레이어로 분리하면, 그 카메라가 검사하고 렌더링해야 할 대상 수를 줄일 수 있습니다.

대표적인 예는 UI와 게임 씬의 분리입니다. Screen Space - Overlay UI는 애초에 게임 카메라가 그리는 대상이 아니지만, Screen Space - Camera나 World Space UI를 별도 UI 카메라로 그리는 구성에서는 게임 카메라의 Culling Mask에서 UI 레이어를 제외하는 편이 자연스럽습니다. 이렇게 하면 3D 씬을 그리는 카메라는 게임 월드만 맡고, UI는 UI 카메라나 UI 시스템이 처리합니다.

미니맵도 같은 방식으로 구성할 수 있습니다. 전체 씬을 한 번 더 그리는 대신, 미니맵 전용 레이어에 단순화한 지형, 아이콘, 표시용 오브젝트만 배치하고 미니맵 카메라의 Culling Mask에는 그 레이어만 남깁니다. 디버그 시각화도 레이어를 따로 두면, 개발 중에는 카메라에 포함해 확인하고 릴리즈 구성에서는 마스크에서 제외해 불필요한 렌더링을 막을 수 있습니다.

다만 Culling Mask는 렌더링에만 적용됩니다. 물리 충돌은 같은 GameObject 레이어를 입력으로 사용할 수 있지만, 실제 충돌 여부는 **Layer Collision Matrix**나 Raycast의 LayerMask 같은 물리 설정이 따로 결정합니다. Culling Mask에서 제외했다고 해서 충돌 판정이나 물리 쿼리까지 함께 제외되는 것은 아닙니다.

---

## Clear Flags

Culling Mask가 렌더링 후보를 고른다면, Clear Flags는 그 후보를 그리기 전에 버퍼를 어떤 상태로 시작할지 정합니다. 카메라가 화면을 그릴 때 결과는 컬러 버퍼와 깊이 버퍼에 기록되는데, 이 버퍼에는 이전 프레임의 내용이나 같은 프레임에서 먼저 실행된 다른 카메라의 결과가 남아 있을 수 있습니다.

따라서 카메라는 렌더링을 시작하기 전에 버퍼를 지울지, 일부만 지울지, 그대로 유지할지를 결정해야 합니다. 배경을 스카이박스나 단색으로 채우고 깊이를 초기화할 수도 있고, 컬러는 유지한 채 깊이만 초기화할 수도 있으며, 특수한 경우에는 아무것도 지우지 않을 수도 있습니다. 이 선택을 다루는 설정이 **Clear Flags**입니다.

카메라가 그린 결과가 기록되는 메모리 영역은 **프레임버퍼**입니다. 프레임버퍼는 픽셀의 색상을 저장하는 **컬러 버퍼**와 깊이 테스트에 쓰이는 **깊이 버퍼**를 중심으로 구성되며, 필요에 따라 스텐실 버퍼 같은 부가 버퍼가 더해집니다. 여기서 중요한 점은 Clear Flags가 무엇을 그릴지가 아니라, 그리기 전에 이 버퍼들을 어떤 상태로 만들지를 정한다는 것입니다.

> 프레임버퍼의 전체 구조는 [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)에서 자세히 다룹니다.

Built-in Render Pipeline에서는 이 개념이 Camera 컴포넌트의 **Clear Flags**로 노출됩니다. URP에서는 같은 선택이 Camera의 **Environment > Background Type**과 카메라 스태킹의 깊이 초기화 설정 등으로 나뉘어 보입니다. 이름은 조금 다르지만 핵심은 같습니다. 컬러 버퍼와 깊이 버퍼를 새로 시작할지, 앞선 결과를 유지한 채 덧그릴지를 정하는 것입니다.

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

**Skybox**는 컬러 버퍼를 스카이박스로 채우고, 깊이 버퍼를 초기화합니다. 하늘이나 원경 배경이 필요한 3D 씬에서는 첫 번째 카메라를 이 설정으로 시작하는 경우가 많습니다. 배경까지 함께 그리므로 화면 전체를 새로 구성하는 기본 설정에 가깝습니다.

**Solid Color**는 컬러 버퍼를 지정한 단색으로 지우고, 깊이 버퍼를 초기화합니다. Skybox와 마찬가지로 새 화면을 시작하는 설정이지만, 스카이박스 머티리얼을 그리지 않습니다. 2D 게임, 메뉴 화면, 단색 배경을 쓰는 씬처럼 하늘 배경이 필요 없는 경우에 적합합니다.

**Depth Only**는 컬러 버퍼는 유지하고, 깊이 버퍼만 초기화합니다. 앞선 카메라가 그린 색은 남겨 둔 채, 현재 카메라의 오브젝트를 그 위에 추가하려는 설정입니다.

이때 깊이 버퍼를 초기화하는 이유는 깊이 테스트 때문입니다. GPU는 새 픽셀을 기록하기 전에 그 픽셀의 깊이 값을 깊이 버퍼에 저장된 값과 비교합니다. 깊이 버퍼를 그대로 두면 앞선 카메라가 남긴 깊이 값 때문에 현재 카메라의 오브젝트가 가려질 수 있습니다. Depth Only는 깊이 버퍼를 새로 시작하므로, 현재 카메라는 앞선 화면의 색은 보존하면서 자신의 렌더링 대상만 안정적으로 덧그릴 수 있습니다. FPS 게임의 무기 카메라나 게임 화면 위에 얹는 UI 카메라가 이런 구성을 사용합니다.

**Don't Clear**는 컬러 버퍼와 깊이 버퍼를 모두 초기화하지 않습니다. 버퍼에 남아 있는 내용을 그대로 둔 채 다음 렌더링을 이어 가므로, 이전 결과를 일부러 누적하는 잔상이나 모션 트레일 같은 특수 효과에 사용할 수 있습니다.

다만 이 설정은 버퍼 내용이 원하는 상태로 남아 있다는 전제에 의존합니다. 이 전제는 플랫폼과 렌더 파이프라인에 따라 안정적이지 않을 수 있습니다. 특히 모바일 GPU에서 흔한 **TBDR(Tile-Based Deferred Rendering)** 구조는 화면을 타일 단위로 처리하고, 타일 메모리의 내용을 필요할 때만 메인 메모리에 저장하거나 다시 불러옵니다. 이런 구조에서는 `Don't Clear`를 사용해도 이전 프레임의 컬러와 깊이가 항상 기대한 형태로 남아 있다고 보기 어렵습니다.

그래서 일반적인 게임 렌더링에서는 `Don't Clear`에 의존하지 않는 편이 안전합니다. 잔상 효과가 필요하다면 이전 프레임을 별도의 `RenderTexture`에 명시적으로 저장하고, 현재 프레임에서 셰이더나 후처리 패스로 합성하는 방식이 더 예측 가능합니다.

### 멀티 카메라에서 Clear Flags 조합

멀티 카메라 구성에서는 카메라가 그려지는 순서와 각 카메라의 Clear Flags가 함께 맞아야 합니다. 먼저 그려진 카메라는 프레임버퍼에 컬러와 깊이를 남기고, 뒤에 그려지는 카메라는 그 결과를 지울지 유지할지 결정합니다. 이때 Camera Depth는 카메라 순서를, Culling Mask는 각 카메라가 맡을 레이어를, Clear Flags는 앞선 결과를 보존할 범위를 정합니다.

아래 예시는 월드, 무기, UI를 세 카메라로 분리한 구성입니다. 첫 카메라는 화면의 바탕이 되는 씬을 만들고, 뒤의 두 카메라는 컬러 버퍼를 유지한 채 자기 레이어만 덧그립니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">멀티 카메라의 버퍼 합성 흐름</text>
  <rect x="15" y="36" width="340" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="27" y="54" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">카메라 A (Depth -1): 씬 렌더링</text>
  <text x="27" y="70" font-family="sans-serif" font-size="11" fill="currentColor">Clear Flags: Skybox</text>
  <text x="27" y="84" font-family="sans-serif" font-size="11" fill="currentColor">Culling Mask: 월드 레이어</text>
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
  <text x="27" y="204" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 깊이만 초기화하여 월드 깊이에 막히지 않음</text>
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

카메라 A는 가장 먼저 실행되어 컬러 버퍼를 스카이박스로 채우고, 월드 오브젝트를 그립니다. 이 결과가 이후 카메라가 덧그릴 바탕이 됩니다.

카메라 B와 C는 `Depth Only`를 사용합니다. 두 카메라는 앞선 카메라의 컬러 결과를 지우지 않으므로, 이미 그려진 월드 화면 위에 자기 Culling Mask에 포함된 오브젝트만 추가합니다. 동시에 깊이 버퍼는 새로 시작하므로, 무기나 UI가 앞선 월드 카메라의 깊이 값에 막혀 사라지는 일을 피할 수 있습니다.

만약 카메라 B가 `Skybox`나 `Solid Color`로 시작했다면 컬러 버퍼가 다시 채워져 카메라 A의 월드 화면이 지워집니다. 반대로 깊이 버퍼를 초기화하지 않으면 앞선 카메라가 남긴 깊이 값 때문에 뒤 카메라의 오브젝트가 예상과 다르게 가려질 수 있습니다. 멀티 카메라를 쓸 때는 그래서 카메라 순서, Culling Mask, Clear Flags를 한 세트로 맞춰야 합니다.

---

## 렌더링 순서

Culling Mask가 렌더링 후보를 고르고 Clear Flags가 버퍼의 시작 상태를 정했다면, 남은 문제는 그 대상을 어떤 순서로 그릴지입니다. 같은 픽셀을 여러 오브젝트가 차지할 수 있기 때문에, 그리기 순서는 최종 화면과 성능에 모두 영향을 줍니다.

Unity의 렌더링 순서는 하나의 값으로만 결정되지 않습니다. 먼저 카메라 사이의 순서가 정해지고, 같은 카메라 안에서는 오브젝트의 정렬 정보와 머티리얼의 Render Queue, 카메라와의 거리 같은 기준이 함께 사용됩니다. 이 글에서는 흐름을 이해하기 위해 Camera Depth, Sorting Layer, Order in Layer, Render Queue, 거리 기반 정렬 순서로 나누어 봅니다.

이 기준들은 적용 범위가 서로 다릅니다. Camera Depth는 카메라 단위의 큰 순서를 정하고, Sorting Layer와 Order in Layer는 주로 스프라이트나 타일맵 같은 2D 렌더러의 앞뒤를 조정할 때 쓰입니다. Render Queue와 거리 기반 정렬은 머티리얼과 카메라 위치를 기준으로 3D 오브젝트의 렌더링 순서에 크게 관여합니다.

### Camera Depth

Camera Depth는 여러 카메라가 같은 출력 대상에 그릴 때 카메라 사이의 순서를 정합니다. 값은 Camera 컴포넌트의 Depth 속성으로 지정하며, 값이 낮은 카메라가 먼저 실행되고 값이 높은 카메라가 나중에 실행됩니다.

이 순서는 Clear Flags와 함께 최종 화면을 결정합니다. 먼저 실행된 카메라가 프레임버퍼에 색과 깊이를 남기고, 뒤의 카메라는 그 결과를 유지하거나 지우면서 자기 대상을 그립니다. 앞서 본 멀티 카메라 예시에서 카메라 A(Depth -1)가 월드를 먼저 만들고, 카메라 C(Depth 1)가 UI를 마지막에 얹은 것도 이 순서 때문입니다.

### Sorting Layer

Sorting Layer는 같은 카메라가 그리는 2D 렌더러 사이의 큰 앞뒤 순서를 정합니다. 주로 Sprite Renderer, Tilemap Renderer처럼 2D 요소를 겹쳐 그릴 때 사용하며, 레이어 목록은 Project Settings > Tags and Layers에서 정의합니다.

목록에서 위쪽에 있는 Sorting Layer는 먼저 그려지고, 아래쪽에 있는 Sorting Layer는 나중에 그려져 앞의 결과를 덮습니다. 예를 들어 `Background` → `Terrain` → `Character` → `Foreground` 순서로 레이어를 두면, 배경이 먼저 깔리고 전경이 마지막에 그려집니다. 이렇게 구성하면 같은 머티리얼을 쓰는 스프라이트라도 어느 그룹을 앞에 둘지 오브젝트 단위에서 안정적으로 제어할 수 있습니다.

Sorting Layer는 레이어 그룹 사이의 순서를 정할 뿐, 같은 레이어 안에 있는 개별 오브젝트의 순서까지 세밀하게 정하지는 않습니다. 같은 Sorting Layer 안에서 더 자세한 앞뒤가 필요할 때는 다음 값인 Order in Layer를 사용합니다.

### Order in Layer

Order in Layer는 같은 Sorting Layer 안에서 개별 2D 렌더러의 순서를 정하는 정수 값입니다. 값이 작은 오브젝트가 먼저 그려지고, 값이 큰 오브젝트가 나중에 그려져 앞의 결과를 덮습니다.

예를 들어 `Character` Sorting Layer 안에 NPC를 `Order in Layer = 0`, 플레이어를 `Order in Layer = 1`로 두면 NPC가 먼저 그려지고 플레이어가 그 위에 그려집니다. 배경, 캐릭터, 전경처럼 큰 묶음은 Sorting Layer로 나누고, 같은 묶음 안의 세부 앞뒤는 Order in Layer로 조정하는 식입니다.

### Render Queue

Render Queue는 머티리얼이 어느 렌더링 그룹에 들어갈지를 정하는 값입니다. 셰이더의 SubShader 블록에 `Tags { "Queue" = "..." }`로 기본값을 지정할 수 있고, 머티리얼에서는 이 값을 다시 오버라이드할 수 있습니다. 따라서 같은 오브젝트라도 어떤 머티리얼을 쓰는지에 따라 불투명 오브젝트보다 먼저 그려지거나, 반투명 오브젝트와 함께 나중에 그려질 수 있습니다.

<br>

**Render Queue 기본값**

| 이름 | 값 | 설명 |
|------|-----|------|
| Background | 1000 | 배경 (스카이박스 등) |
| Geometry | 2000 | 불투명 오브젝트 (기본값) |
| AlphaTest | 2450 | 알파 테스트 오브젝트 |
| Transparent | 3000 | 반투명 오브젝트 |
| Overlay | 4000 | 오버레이 효과 (렌즈 플레어 등) |

<br>

Render Queue 값은 낮을수록 먼저 처리되는 큰 순서 기준입니다. `Background`는 가장 앞쪽에서 배경을 만들고, 기본 불투명 오브젝트는 `Geometry` 범위에서 처리되며, 반투명 오브젝트는 `Transparent` 범위로 넘어가 나중에 그려집니다.

중요한 경계는 2500입니다. Unity는 Render Queue가 2500 이하인 대상을 불투명(Opaque) 계열로, 2501 이상인 대상을 반투명(Transparent) 계열로 다룹니다. 불투명 계열은 깊이 버퍼를 활용하기 좋기 때문에 대체로 앞쪽 물체부터 그리는 Front-to-Back 정렬이 유리하고, 반투명 계열은 뒤쪽 색이 먼저 있어야 알파 블렌딩 결과가 맞으므로 Back-to-Front 정렬이 필요합니다.

그래서 Render Queue는 단순히 "몇 번째로 그릴지"를 정하는 숫자가 아니라, 이후 정렬 방식까지 바꾸는 기준입니다. 알파 테스트 머티리얼이 `AlphaTest` 2450에 놓이는 이유도 여기에 있습니다. 알파로 픽셀을 버릴 수는 있지만 깊이 기록은 불투명 오브젝트처럼 사용할 수 있으므로, 반투명 그룹으로 보내지 않고 불투명 쪽 끝에 배치합니다.

### 정렬 우선순위 계층

렌더링 순서는 하나의 숫자만 보고 결정되지 않습니다. 먼저 어떤 카메라가 먼저 실행되는지 정해지고, 그 카메라가 처리하는 렌더러 안에서 2D 정렬 값, 머티리얼의 Render Queue, 카메라와의 거리 같은 기준이 함께 사용됩니다.

다만 모든 기준이 모든 오브젝트에 같은 방식으로 적용되는 것은 아닙니다. Sorting Layer와 Order in Layer는 주로 2D 렌더러의 앞뒤를 다룰 때 의미가 크고, 일반적인 3D 오브젝트에서는 Render Queue와 거리 기반 정렬의 영향이 더 큽니다. 아래 그림은 이 기준들이 어느 범위의 순서를 다루는지 큰 흐름으로 정리한 것입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더링 순서의 주요 기준</text>
  <!-- Level 1: Camera Depth -->
  <rect x="30" y="36" width="400" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="56" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) Camera Depth</text>
  <text x="230" y="72" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">카메라 사이의 실행 순서</text>
  <text x="230" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Depth가 낮은 카메라 → 먼저 실행</text>
  <!-- Arrow 1→2 -->
  <line x1="230" y1="96" x2="230" y2="112" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,118 225,112 235,112" fill="currentColor"/>
  <!-- Level 2: Sorting Layer -->
  <rect x="30" y="122" width="400" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="142" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) Sorting Layer</text>
  <text x="230" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">2D 렌더러의 그룹 순서</text>
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
  <text x="230" y="330" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼의 렌더링 그룹</text>
  <text x="230" y="346" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">큐 값이 낮은 것 → 먼저 렌더링</text>
  <!-- Arrow 4→5 -->
  <line x1="230" y1="354" x2="230" y2="370" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,376 225,370 235,370" fill="currentColor"/>
  <!-- Level 5: 거리 기반 정렬 (with two sub-items) -->
  <rect x="30" y="380" width="400" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="400" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(5) 같은 큐 안의 거리 정렬</text>
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

이 계층은 순서를 이해하기 위한 모델입니다. 실제 렌더링에서는 렌더 파이프라인, 렌더러 종류, 머티리얼 설정에 따라 세부 동작이 달라질 수 있습니다. 그래도 큰 흐름은 같습니다. 카메라 단위 순서가 먼저 화면의 누적 구조를 만들고, 그 안에서 렌더러와 머티리얼의 정렬 정보가 그리기 순서를 좁혀 갑니다.

2D 화면에서는 Sorting Layer와 Order in Layer가 앞뒤 관계를 직접 조정하는 주요 도구가 됩니다. 3D 오브젝트를 볼 때는 먼저 머티리얼의 Render Queue가 불투명 그룹인지 반투명 그룹인지 확인하고, 그다음 같은 그룹 안에서 거리 정렬이 어떤 방향으로 적용되는지를 봐야 합니다. 이 차이가 바로 다음의 Opaque 정렬과 Transparent 정렬로 이어집니다.

---

## Opaque 정렬: Front-to-Back

Render Queue가 2500 이하인 오브젝트는 불투명(Opaque) 계열로 처리됩니다. 이 그룹에서는 Unity가 카메라와의 거리를 기준으로 가까운 오브젝트를 먼저 그리는 **Front-to-Back** 정렬을 사용합니다.

불투명 오브젝트를 가까운 것부터 그리는 이유는 깊이 버퍼를 빨리 채우기 위해서입니다. 가까운 표면이 먼저 그려져 깊이 값이 기록되면, 그 뒤에 있는 표면은 같은 픽셀에서 깊이 테스트에 실패할 수 있습니다. 이때 조건이 맞으면 GPU는 프래그먼트 셰이더를 실행하기 전에 깊이 비교를 먼저 수행하는 **Early-Z 테스트**로 뒤쪽 프래그먼트를 걸러냅니다.

이렇게 걸러진 프래그먼트는 최종 화면에 보이지 않을 픽셀이므로 색을 계산할 필요가 없습니다. 같은 픽셀에 여러 오브젝트가 겹쳐 보이지 않는 픽셀까지 셰이더를 실행하는 상황을 **오버드로우(Overdraw)**라고 하는데, Front-to-Back 정렬은 Early-Z가 이 오버드로우를 줄일 수 있는 조건을 만들어 줍니다. 프래그먼트 셰이더가 복잡한 머티리얼일수록 이 차이는 더 커집니다.

이 흐름이 성립하려면 먼저 그린 오브젝트가 깊이 버퍼에 자기 깊이를 기록해야 합니다. 이 설정이 **깊이 쓰기(Depth Write, `ZWrite`)**입니다. 일반적인 불투명 셰이더는 `ZWrite On`을 사용하므로, 개발자가 별도로 정렬을 처리하지 않아도 Front-to-Back 정렬, 깊이 기록, Early-Z가 함께 동작하는 경우가 많습니다.

---

## Transparent 정렬: Back-to-Front

Render Queue가 2501 이상인 오브젝트는 반투명(Transparent) 계열로 처리됩니다. Unity는 불투명 오브젝트를 먼저 그려 깊이와 배경 색을 만든 뒤, 반투명 오브젝트를 **카메라에서 먼 것부터 가까운 것 순서(Back-to-Front)**로 그립니다.

반투명에서 순서가 중요한 이유는 **알파 블렌딩(Alpha Blending)** 때문입니다. 알파 블렌딩은 지금 그리려는 색을 프레임버퍼에 이미 들어 있는 색과 섞는 연산입니다. 알파 값이 0.0이면 완전히 투명하고, 1.0이면 완전히 불투명하며, 그 사이 값에서는 뒤에 있는 색이 함께 보입니다.

따라서 올바른 결과를 얻으려면 뒤쪽 반투명 오브젝트의 색이 먼저 프레임버퍼에 기록되어 있어야 합니다. 그 위에 더 가까운 반투명 오브젝트를 차례로 섞어야, 유리창이나 연기처럼 여러 반투명 표면이 겹친 결과가 기대한 순서로 누적됩니다. 이 때문에 반투명은 불투명과 반대로 먼 것부터 그립니다.

<br>

### 반투명의 성능 비용

반투명 오브젝트는 불투명 오브젝트보다 비용이 커지기 쉽습니다. 핵심은 반투명 셰이더가 보통 깊이 쓰기(Depth Write, `ZWrite`)를 끈다는 점입니다. 반투명 표면은 뒤쪽 색과 앞쪽 색을 순서대로 섞어야 하므로, 중간에 어떤 반투명 표면이 깊이 버퍼를 막아 버리면 뒤이어 그려질 다른 반투명 프래그먼트가 블렌딩에 참여하지 못할 수 있습니다. 그래서 일반적인 반투명 머티리얼은 `ZWrite Off`를 사용합니다.

문제는 깊이를 쓰지 않으면 반투명끼리 서로를 가려서 비용을 줄이기 어렵다는 데 있습니다. 같은 픽셀에 반투명 프래그먼트가 여러 겹 쌓이면, 그 프래그먼트들은 대체로 모두 셰이더를 실행하고 프레임버퍼의 색과 블렌딩됩니다. 불투명 오브젝트가 먼저 채워 둔 깊이 버퍼 덕분에, 불투명 뒤에 완전히 가려진 반투명 프래그먼트는 깊이 테스트에서 제외될 수 있습니다. 하지만 반투명끼리 겹치는 영역에서는 그런 제외가 잘 일어나지 않으므로, 겹치는 수만큼 오버드로우가 직접 늘어납니다.

따라서 파티클, 유리, 연기, 반투명 UI 같은 요소는 화면에 넓게 깔리거나 여러 겹 겹칠 때 비용이 빠르게 커집니다. 반투명 면적을 줄이고, 겹침을 줄이며, 꼭 필요한 경우에만 높은 해상도 후처리나 복잡한 셰이더를 쓰는 식으로 관리해야 합니다.

### 반투명의 정렬 한계

반투명은 성능뿐 아니라 정렬 정확성에서도 한계가 있습니다. Unity는 반투명 오브젝트를 픽셀 단위로 매번 정렬하지 않고, Renderer 단위의 대표 위치를 기준으로 순서를 정합니다. 일반적으로 이 대표 위치는 오브젝트의 **바운딩 박스(Bounding Box)** 중심, 즉 `Renderer.bounds.center`입니다.

이 방식은 단순한 유리창이나 작은 파티클처럼 오브젝트끼리 앞뒤가 분명한 경우에는 대체로 충분합니다. 하지만 큰 반투명 메쉬가 서로 교차하거나, 실제 표면 위치와 바운딩 박스 중심이 크게 다르면 문제가 생깁니다. 오브젝트 중심만 보면 A가 뒤에 있는 것처럼 보이지만, 화면의 일부 픽셀에서는 A가 B보다 앞에 있을 수 있기 때문입니다.

이런 경우 카메라가 움직일 때 반투명 표면의 앞뒤가 갑자기 뒤집히거나, 겹친 영역이 깜빡이는 것처럼 보일 수 있습니다. 이는 블렌딩 자체의 문제가 아니라, 오브젝트 단위 정렬이 픽셀 단위의 실제 앞뒤 관계를 완전히 표현하지 못해서 생기는 문제입니다.

근본적인 해결책은 **Order-Independent Transparency(OIT)**처럼 그리는 순서에 덜 의존하는 투명도 기법을 사용하는 것입니다. 하지만 OIT는 픽셀별로 여러 투명 프래그먼트를 저장하거나 정렬해야 하므로 메모리와 GPU 비용이 큽니다. 특히 모바일에서는 부담이 커서 일반적인 게임 화면에 무작정 적용하기 어렵습니다.

실무에서는 보통 더 단순한 방식으로 피합니다. 큰 반투명 메쉬를 여러 조각으로 나누어 정렬 기준을 세분화하거나, 반투명 표면이 서로 교차하지 않도록 배치하고, 겹치는 반투명 오브젝트 수를 줄입니다. 가능하다면 알파 블렌딩 대신 알파 테스트, 디더링, 불투명 대체 표현을 쓰는 것도 안정적인 선택입니다.

---

## 멀티 카메라 비용

여기까지는 한 카메라가 화면을 만드는 흐름을 따라왔습니다. 하지만 실제 프로젝트에서는 UI, 미니맵, FPS 무기, 거울, 포탈처럼 별도의 시점이나 출력 영역이 필요한 경우가 자주 있습니다. 이때 카메라를 추가하면 화면 구성은 쉬워지지만, 렌더링 작업도 카메라 단위로 늘어납니다.

카메라 하나는 단순한 뷰포트가 아니라, 자기 기준으로 렌더링 대상을 다시 고르고 그릴 명령을 만드는 단위입니다. 따라서 카메라가 늘어나면 Culling Mask와 절두체를 기준으로 후보를 추리는 작업, 통과한 렌더러의 드로우콜을 준비하는 작업, 실제 픽셀을 채우는 GPU 작업이 추가로 발생할 수 있습니다. 카메라가 같은 씬을 바라보더라도 이전 카메라의 결과를 그대로 재사용하는 것은 아니므로, 필요한 만큼만 두는 것이 기본입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">카메라가 늘 때 반복될 수 있는 작업</text>

  <!-- CPU section label -->
  <text x="40" y="56" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <line x1="70" y1="52" x2="490" y2="52" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- (1) 컬링 -->
  <rect x="40" y="66" width="440" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="86" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) 컬링 연산</text>
  <text x="56" y="106" font-family="sans-serif" font-size="11" fill="currentColor">씬의 오브젝트를 절두체와 비교</text>
  <text x="310" y="106" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Culling Mask + Frustum</text>

  <!-- Arrow -->
  <line x1="260" y1="122" x2="260" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,144 255,138 265,138" fill="currentColor"/>

  <!-- (2) 드로우콜 -->
  <rect x="40" y="148" width="440" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="168" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) 드로우콜 생성</text>
  <text x="56" y="188" font-family="sans-serif" font-size="11" fill="currentColor">컬링 통과 오브젝트에 대해 드로우콜 구성</text>
  <text x="310" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">상태 변경과 배치 구성</text>

  <!-- GPU section label -->
  <text x="40" y="230" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU</text>
  <line x1="70" y1="226" x2="490" y2="226" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- (3) 렌더링 패스 -->
  <rect x="40" y="240" width="440" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="260" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) 렌더링 패스</text>
  <text x="56" y="280" font-family="sans-serif" font-size="11" fill="currentColor">불투명/반투명 패스, 후처리 등이 추가 실행될 수 있음</text>

  <!-- Arrow -->
  <line x1="260" y1="296" x2="260" y2="312" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,318 255,312 265,312" fill="currentColor"/>

  <!-- (4) Clear -->
  <rect x="40" y="322" width="440" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="342" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(4) Clear 비용</text>
  <text x="56" y="358" font-family="sans-serif" font-size="11" fill="currentColor">버퍼 초기화, Render Target 전환, 합성 비용</text>
</svg>
</div>

<br>

비용만 보면 한 카메라로 끝내는 구성이 가장 단순합니다. 하지만 기능상 카메라를 나누어야 하는 경우도 많습니다. 이때는 카메라를 추가하는 것 자체보다, 추가한 카메라가 무엇을 얼마나 자주 그리는지가 비용을 좌우합니다.

### 비용 최소화 전략

멀티 카메라 비용을 줄이는 핵심은 추가한 카메라가 반복하는 일을 줄이는 것입니다. 카메라 수를 무조건 줄이는 것보다, 각 카메라가 꼭 필요한 대상만 보고 필요한 순간에만 렌더링하도록 만드는 쪽이 실무에서 더 중요합니다.

먼저 별도 카메라가 정말 필요한지부터 확인합니다. 단순한 HUD처럼 3D 씬 위에 항상 고정되어 보이는 UI라면 `Screen Space - Overlay`가 가장 단순합니다. 이 모드는 UI를 그리기 위해 별도의 카메라를 요구하지 않으므로, UI 전용 카메라가 만드는 컬링과 렌더링 비용을 피할 수 있습니다.

다만 URP에서는 렌더 흐름까지 함께 봐야 합니다. `Screen Space - Overlay` UI는 카메라 렌더링 스택 바깥에서 최종 화면 위에 그려집니다. 그래서 UI가 포스트 프로세싱, 카메라 스택, 렌더 스케일, 특정 Render Target 흐름 안에 포함되어야 한다면 `Screen Space - Camera`나 URP의 Overlay Camera가 더 적절할 수 있습니다. UI가 단순히 화면 위에 얹히면 되는지, 아니면 씬 렌더링 과정 안에 들어가야 하는지를 기준으로 선택합니다.

카메라가 필요하다면 Culling Mask를 최대한 좁힙니다. 추가 카메라가 전체 씬을 다시 보게 두면, 그 카메라는 다시 많은 오브젝트를 컬링하고 렌더링 후보로 검토해야 합니다. 미니맵 카메라라면 미니맵 전용 레이어에 단순화한 지형과 아이콘만 두고, 무기 카메라라면 무기와 손 레이어만 보게 만드는 식으로 역할을 제한합니다.

마지막으로 매 프레임 갱신할 필요가 없는 카메라는 갱신 주기를 낮춥니다. 미니맵, 거울, 보안 카메라, 포탈 화면처럼 약간 늦게 갱신되어도 문제가 작은 화면은 매 프레임 렌더링하지 않아도 됩니다. 필요한 프레임에만 카메라를 켜서 `RenderTexture`에 결과를 갱신하고, 나머지 프레임에는 마지막 결과를 재사용하면 CPU와 GPU 비용을 분산할 수 있습니다.

### URP의 Camera Stacking

URP에서는 여러 카메라를 **Camera Stacking**으로 묶어 하나의 화면을 만들 수 있습니다. 기준이 되는 카메라는 **Base Camera**이고, 그 위에 덧그릴 카메라는 **Overlay Camera**로 등록합니다. Base Camera가 먼저 씬을 렌더링하고, Stack 리스트에 들어 있는 Overlay Camera들이 그 결과 위에 순서대로 추가됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Base Camera와 Overlay Stack</text>

  <!-- Outer box: Base Camera -->
  <rect x="30" y="36" width="420" height="280" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="58" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Base Camera</text>
  <text x="50" y="76" font-family="sans-serif" font-size="11" fill="currentColor">Render Type: Base</text>
  <text x="50" y="94" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">출력 대상과 기본 씬 렌더링 담당</text>

  <!-- Inner box: Stack list -->
  <rect x="50" y="108" width="380" height="170" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="66" y="128" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Camera Stack (위에서 아래 순서로 추가):</text>

  <!-- Sub-box 1: Overlay Camera A -->
  <rect x="66" y="138" width="348" height="56" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="82" y="157" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Overlay Camera A</text>
  <text x="82" y="173" font-family="sans-serif" font-size="10" fill="currentColor">Render Type: Overlay</text>
  <text x="82" y="188" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Base 결과 위에 레이어 추가</text>

  <!-- Divider -->
  <line x1="80" y1="200" x2="400" y2="200" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Sub-box 2: Overlay Camera B -->
  <rect x="66" y="206" width="348" height="56" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="82" y="225" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Overlay Camera B</text>
  <text x="82" y="241" font-family="sans-serif" font-size="10" fill="currentColor">Render Type: Overlay</text>
  <text x="82" y="256" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">A 결과 위에 다시 추가</text>

  <!-- Annotations below stack -->
  <text x="240" y="298" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Overlay 순서 = Camera Stack 리스트 순서</text>
  <text x="240" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">각 Overlay도 컬링과 드로우콜 비용을 가짐</text>
</svg>
</div>

<br>

Camera Stacking에서 Overlay Camera는 Base Camera와 별개로 최종 화면을 만드는 카메라가 아닙니다. Base Camera의 렌더링 흐름 안에 들어가고, Base Camera의 Stack 리스트에 등록된 순서대로 실행됩니다. 그래서 Overlay Camera끼리의 순서는 일반적인 Camera Depth보다 **Stack 리스트의 순서**를 기준으로 이해하는 편이 맞습니다.

이 구조의 장점은 여러 결과를 직접 `RenderTexture`에 따로 그린 뒤 Blit로 합성하는 방식보다 구성이 단순하다는 점입니다. Base Camera의 결과 위에 Overlay Camera를 순서대로 얹을 수 있으므로, 무기, UI, 특정 효과 레이어처럼 같은 화면 안에서 분리해 그리고 싶은 대상을 관리하기 쉽습니다.

하지만 Camera Stacking이 Overlay Camera의 비용을 없애 주는 것은 아닙니다. Overlay Camera도 자기 Culling Mask를 기준으로 대상을 고르고, 필요한 드로우콜을 만들고, 픽셀을 그립니다. 따라서 URP에서도 Stack에 카메라를 많이 쌓기보다, 각 Overlay Camera가 꼭 필요한 레이어만 보게 하고 필요한 경우에만 사용해야 합니다.

---

## 마무리

이번 글에서는 카메라가 어디를 보고, 무엇을, 어떤 순서로 그릴지, 그리고 그리기 전에 버퍼를 어떤 상태로 시작할지를 정하는 과정을 살펴보았습니다. 핵심은 다음과 같습니다.

- **Projection과 Near/Far Clip Plane**은 카메라가 볼 공간의 범위와 깊이 정밀도를 함께 정합니다. Far를 Near로 나눈 비율이 클수록 먼 거리의 깊이 값이 성겨져 Z-fighting 위험이 커집니다.
- **Culling Mask**는 32개 레이어를 비트마스크로 지정해 카메라가 그릴 대상을 제한합니다. 다만 같은 GameObject 레이어를 쓰더라도 물리 충돌은 Layer Collision Matrix가 따로 판정하므로, 렌더링에서 제외한 레이어가 충돌 판정에서도 제외되는 것은 아닙니다.
- **Clear Flags**는 컬러 버퍼와 깊이 버퍼를 그리기 전에 어떻게 비우고 시작할지 정합니다. 멀티 카메라 구성에서는 컬러는 남기고 깊이만 초기화하는 Depth Only가 앞선 화면 위에 덧그리는 기준이 됩니다.
- **렌더링 순서**는 하나의 값으로 결정되지 않습니다. Camera Depth가 카메라 사이의 순서를 정하고, 그 안에서 Sorting Layer와 Order in Layer, Render Queue, 거리 기반 정렬이 렌더러 종류와 머티리얼에 따라 함께 작용합니다.
- **불투명과 반투명 정렬**은 방향이 반대입니다. 불투명은 Front-to-Back으로 그려 Early-Z로 오버드로우를 줄이고, 반투명은 Back-to-Front로 그려 겹친 색이 올바른 순서로 섞이도록 합니다. 반투명은 보통 `ZWrite Off`로 동작하므로 겹치는 영역에서 오버드로우 비용이 커집니다.
- **반투명 정렬**은 바운딩 박스 중심을 기준으로 하므로 픽셀 단위의 앞뒤를 완전히 표현하지 못합니다. 큰 메쉬가 서로 교차하거나 중심이 실제 표면과 크게 어긋나면 정렬이 뒤집혀 보일 수 있습니다.
- **멀티 카메라**는 카메라마다 컬링, 드로우콜 구성, 렌더링 패스를 다시 수행합니다. 필요한 카메라만 두고, 각 카메라의 Culling Mask를 좁히고 갱신 주기를 낮추는 것이 비용 관리의 기본입니다.

<br>

결국 이 글에서 다룬 설정과 규칙은 카메라가 정하는 것과 렌더 파이프라인이 수행하는 것으로 나뉩니다. Projection과 Culling Mask, Clear Flags는 카메라가 정하는 입력이고, 컬링과 정렬, 드로우콜 생성은 렌더 파이프라인이 그 입력을 받아 수행하는 일입니다. 그래서 화면에 남는 결과와 그 비용은 이 두 단계가 맞물려 정해집니다.

<br>

지금까지 카메라가 그리는 과정을 살펴보면서 프레임버퍼와 컬러 버퍼, 깊이 버퍼가 여러 번 등장했습니다. 카메라는 결과를 이 버퍼에 기록할 뿐, 버퍼 자체가 어떤 구조이고 어떻게 관리되는지, 그것이 성능에 어떤 영향을 주는지는 아직 다루지 않았습니다.

[Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)에서는 Back Buffer와 RenderTexture의 구조, Render Target 전환이 모바일 GPU에 미치는 영향, 그리고 해상도와 컬러 포맷에 따라 달라지는 메모리 비용을 이어서 다룹니다.

<br>

---

**관련 글**
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)

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
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
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
