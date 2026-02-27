  ---
layout: single
title: "그래픽스 수학 (3) - 좌표 공간의 전환 - soo:bak"
date: "2026-02-27 22:33:00 +0900"
description: 오브젝트 공간, 월드 공간, 뷰 공간, 클립 공간, NDC, 화면 공간, MVP 행렬을 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 수학
  - 좌표공간
  - 모바일
---

## 오브젝트 공간에서 화면 공간까지

[그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)에서는 이동, 회전, 크기 변환을 하나의 4x4 행렬에 담고, 정점 좌표에 곱해 변환된 좌표를 얻는 과정을 다뤘습니다.

정점 하나가 화면의 픽셀이 되기까지는 여러 **좌표 공간(Coordinate Space)**을 거칩니다.

좌표 공간은 원점과 축 방향이 고정된 기준 틀로, 같은 정점이라도 좌표 공간이 바뀌면 좌표값이 달라집니다.

<br>

공간이 바뀔 때마다 좌표에 변환 행렬을 곱해 다음 좌표 공간의 좌표를 얻습니다.

오브젝트 공간에서 출발한 정점 좌표는 월드, 뷰, 클립 공간을 차례로 거쳐 화면의 픽셀 좌표가 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 320 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 320px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="160" y="18" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">정점이 화면 픽셀이 되기까지 거치는 좌표 공간</text>
  <!-- Box 1: Object Space -->
  <rect x="50" y="35" width="220" height="36" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="160" y="58" text-anchor="middle" font-size="12" font-family="sans-serif">오브젝트 공간 (Object Space)</text>
  <!-- Arrow + label -->
  <line x1="160" y1="71" x2="160" y2="110" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="160,113 156,105 164,105" fill="currentColor"/>
  <text fill="currentColor" x="220" y="96" font-size="10" font-family="sans-serif" opacity="0.6">Model 행렬</text>
  <!-- Box 2: World Space -->
  <rect x="50" y="116" width="220" height="36" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="160" y="139" text-anchor="middle" font-size="12" font-family="sans-serif">월드 공간 (World Space)</text>
  <!-- Arrow + label -->
  <line x1="160" y1="152" x2="160" y2="191" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="160,194 156,186 164,186" fill="currentColor"/>
  <text fill="currentColor" x="220" y="177" font-size="10" font-family="sans-serif" opacity="0.6">View 행렬</text>
  <!-- Box 3: View Space -->
  <rect x="50" y="197" width="220" height="36" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="160" y="220" text-anchor="middle" font-size="12" font-family="sans-serif">뷰 공간 (View Space)</text>
  <!-- Arrow + label -->
  <line x1="160" y1="233" x2="160" y2="272" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="160,275 156,267 164,267" fill="currentColor"/>
  <text fill="currentColor" x="220" y="258" font-size="10" font-family="sans-serif" opacity="0.6">Projection 행렬</text>
  <!-- Box 4: Clip Space -->
  <rect x="50" y="278" width="220" height="36" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="160" y="301" text-anchor="middle" font-size="12" font-family="sans-serif">클립 공간 (Clip Space)</text>
  <!-- Arrow + label -->
  <line x1="160" y1="314" x2="160" y2="353" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="160,356 156,348 164,348" fill="currentColor"/>
  <text fill="currentColor" x="222" y="339" font-size="10" font-family="sans-serif" opacity="0.6">원근 나눗셈 (w 나누기)</text>
  <!-- Box 5: NDC -->
  <rect x="50" y="359" width="220" height="36" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="160" y="382" text-anchor="middle" font-size="12" font-family="sans-serif">NDC (Normalized Device Coords)</text>
  <!-- Arrow + label -->
  <line x1="160" y1="395" x2="160" y2="434" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="160,437 156,429 164,429" fill="currentColor"/>
  <text fill="currentColor" x="220" y="420" font-size="10" font-family="sans-serif" opacity="0.6">뷰포트 변환</text>
  <!-- Box 6: Screen Space -->
  <rect x="50" y="440" width="220" height="36" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="160" y="463" text-anchor="middle" font-size="12" font-family="sans-serif">화면 공간 (Screen Space)</text>
</svg>
</div>

---

## 오브젝트 공간 (Object Space)

오브젝트 공간은 **각 메쉬가 기준으로 사용하는 좌표 공간**입니다. 모델 공간(Model Space) 또는 로컬 공간(Local Space)이라고도 합니다.

3D 모델을 만들 때 정한 원점과 축 방향이 메쉬 데이터에 기록되며, 메쉬에 저장된 모든 정점 좌표는 이 원점을 기준으로 한 값입니다.

<br>

키 1.8미터인 캐릭터 모델을 만들면서 발 아래를 원점 (0, 0, 0)으로 설정했다면, 가슴은 (0, 1.2, 0), 머리 꼭대기는 (0, 1.8, 0)처럼 원점 기준의 좌표로 저장됩니다.

원점을 어디에 둘지는 모델링 과정에서 결정하며, 캐릭터의 발 아래나 모델의 기하학적 중심 등 용도에 따라 달라집니다.

<br>

오브젝트 공간의 좌표는 씬 안에서의 배치와 무관합니다.

같은 캐릭터 모델을 씬의 (100, 0, 50)에 배치하든 (0, 0, 0)에 배치하든, 메쉬에 저장된 정점 좌표는 동일합니다.

씬에서의 위치, 회전, 크기는 Transform 컴포넌트의 position, rotation, localScale이 별도로 관리하며, 이 값들이 오브젝트 공간 좌표를 월드 공간으로 변환하는 데 사용됩니다.

Unity에서 `Mesh.vertices`로 접근하는 정점 좌표가 이 오브젝트 공간의 좌표입니다.

---

## 월드 공간 (World Space)

오브젝트 공간의 좌표는 각 메쉬 내부의 기준이므로, 서로 다른 오브젝트 사이의 위치 관계를 표현할 수 없습니다.

월드 공간은 **씬의 모든 오브젝트가 공유하는 단일 좌표계**이며, 오브젝트 공간의 정점 좌표를 월드 공간으로 변환해야 모든 오브젝트가 하나의 좌표계 위에서 서로의 위치를 비교할 수 있게 됩니다.

<br>

**Model 행렬**(모델 행렬)은 오브젝트 공간의 좌표를 월드 공간으로 변환하는 4x4 행렬입니다.

[그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)에서 다룬 이동(T), 회전(R), 스케일(S) 변환을 TRS 순서로 합성한 결과이며, Unity에서는 Transform 컴포넌트의 position, rotation, localScale이 각각 T, R, S의 입력이 됩니다.

Unity API로는 `transform.localToWorldMatrix`가 Model 행렬에 해당하고, 셰이더에서는 `unity_ObjectToWorld`로 접근합니다.

<br>

높이가 2인 메쉬를 예로 들면, 꼭대기 정점은 오브젝트 공간에서 (0, 2, 0)입니다.

이 메쉬를 씬의 position (10, 0, 5)에 배치하면서 회전과 스케일을 기본값(rotation = 항등, scale = 1)으로 두면, Model 행렬에는 순수한 이동 변환만 남습니다.

이동만 있는 경우 오브젝트 공간 좌표에 position을 더하는 것과 같으므로, 꼭대기 정점의 월드 좌표는 (0 + 10, 2 + 0, 0 + 5) = **(10, 2, 5)**,

즉 씬에서 x 방향으로 10, z 방향으로 5만큼 이동한 지점의 높이 2 위치가 됩니다.

회전이나 스케일이 포함되면 단순 덧셈이 아니라 전체 4x4 행렬 곱셈이 필요하지만, 오브젝트 공간 좌표에 Model 행렬을 곱해 월드 좌표를 얻는다는 원리는 동일합니다.

<br>

같은 메쉬를 공유하는 오브젝트가 여럿이면, 오브젝트 공간 좌표는 모두 동일하고 각 오브젝트의 Model 행렬만 다릅니다.

앞서 본 꼭대기 정점 (0, 2, 0)을 가진 메쉬를 position (3, 0, 0)에 하나, position (8, 0, 0)에 하나 배치하면, 같은 꼭대기 정점이 월드 공간에서는 각각 (3, 2, 0)과 (8, 2, 0)으로 변환됩니다.

---

## 뷰 공간 (View Space)

Model 행렬을 통해 모든 오브젝트가 월드 공간에 배치되었지만, 화면에 그리려면 "어디서 바라보는가"라는 카메라 기준이 있어야 합니다.

**뷰 공간(View Space)**은 카메라를 원점으로, 카메라의 시선 방향을 기준 축으로 설정한 좌표계입니다. 카메라 공간(Camera Space) 또는 눈 공간(Eye Space)이라고도 합니다.

<br>

월드 공간에서 뷰 공간으로의 변환에는 **View 행렬**(뷰 행렬)을 사용합니다. View 행렬은 월드 공간의 모든 정점 좌표를, 카메라의 위치와 방향을 원점·기준 축으로 삼는 좌표계로 변환하는 행렬입니다.

앞 섹션에서 Model 행렬(localToWorldMatrix)이 오브젝트 공간 좌표를 월드 공간으로 변환했듯이, 카메라의 localToWorldMatrix도 카메라 로컬 좌표를 월드 좌표로 변환합니다.

View 행렬은 이 행렬의 **역행렬(Inverse)**입니다. localToWorldMatrix가 로컬 → 월드 방향이므로, 역행렬은 반대인 월드 → 로컬 방향입니다.

정점 좌표에 이 역행렬을 곱하면, 카메라 자체가 움직이는 것이 아니라 **월드의 모든 정점이 카메라 기준 좌표로 재배치**됩니다.

<br>

카메라가 월드의 (10, 5, -3)에 위치한다면, View 행렬에는 모든 정점에서 (10, 5, -3)을 빼는 이동 변환이 포함됩니다. 카메라가 Y축으로 30도 회전한 상태라면, -30도 역회전 변환도 포함됩니다. 카메라의 이동과 회전을 각각 역으로 적용한 결과가 뷰 공간 좌표입니다.

뷰 공간에서의 축 방향 관례는 그래픽스 API마다 약간 다르지만, 공통적으로 X는 오른쪽, Y는 위쪽, 카메라 시선 방향은 -Z입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 360 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 360px; width: 100%;">
  <text fill="currentColor" x="180" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">뷰 공간의 축 방향 (오른손 좌표계)</text>
  <!-- Origin point (camera) -->
  <polygon points="150,140 160,130 170,140 160,150" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.07"/>
  <!-- Y axis (up) -->
  <line x1="160" y1="130" x2="160" y2="42" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="160,38 156,46 164,46" fill="currentColor"/>
  <text fill="currentColor" x="172" y="44" font-size="12" font-weight="bold" font-family="sans-serif">Y+</text>
  <text fill="currentColor" x="190" y="57" font-size="10" font-family="sans-serif" opacity="0.6">(위)</text>
  <!-- X axis (right) -->
  <line x1="170" y1="140" x2="290" y2="140" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="293,140 285,136 285,144" fill="currentColor"/>
  <text fill="currentColor" x="298" y="136" font-size="12" font-weight="bold" font-family="sans-serif">X+</text>
  <text fill="currentColor" x="298" y="152" font-size="10" font-family="sans-serif" opacity="0.6">(오른쪽)</text>
  <!-- Z+ axis (out of screen, diagonal) -->
  <line x1="150" y1="150" x2="95" y2="200" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="92,203 102,198 97,190" fill="currentColor"/>
  <text fill="currentColor" x="72" y="215" font-size="12" font-weight="bold" font-family="sans-serif">Z+</text>
  <text fill="currentColor" x="60" y="230" font-size="10" font-family="sans-serif" opacity="0.6">(화면 바깥쪽)</text>
  <!-- -Z gaze direction (dashed, into screen) -->
  <line x1="170" y1="130" x2="225" y2="80" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5"/>
  <polygon points="228,77 220,80 222,88" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="240" y="78" font-size="11" font-family="sans-serif" opacity="0.7">-Z (시선 방향)</text>
  <!-- Legend -->
  <text fill="currentColor" x="180" y="260" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">카메라 시선 방향 = -Z (화면 안쪽)</text>
</svg>
</div>

<br>

시선 방향이 -Z가 되는 것은 좌표계 관례 때문입니다. **오른손 좌표계**는 오른손의 엄지(X), 검지(Y), 중지(Z)를 서로 직각으로 펼쳤을 때 각 손가락이 가리키는 방향이 축 방향이 되는 규칙이고, **왼손 좌표계**는 같은 방식을 왼손으로 적용한 규칙입니다.

두 좌표계의 핵심 차이는 Z축의 방향입니다.

X가 오른쪽, Y가 위쪽이라고 고정하면, 오른손 좌표계에서는 +Z가 화면 바깥(카메라 뒤쪽)을 가리키고, 왼손 좌표계에서는 +Z가 화면 안쪽(카메라 앞쪽)을 가리킵니다.

OpenGL 등 대부분의 그래픽스 API는 뷰 공간에서 오른손 좌표계를 사용하므로, +Z가 카메라 뒤쪽이고 시선 방향은 -Z가 됩니다.

<br>

Unity에서 `Camera.worldToCameraMatrix`가 View 행렬에 해당합니다. Unity의 씬 좌표계(월드 공간)는 왼손 좌표계를 사용하므로 카메라의 forward 방향이 +Z이지만, `worldToCameraMatrix`는 내부적으로 Z축을 반전시켜 오른손 좌표계의 뷰 공간으로 자동 변환합니다.

---

## 클립 공간 (Clip Space)

뷰 공간까지는 여전히 3D 공간의 좌표입니다. 카메라를 기준으로 한 위치는 알 수 있지만, 아직 화면에 표시할 수 있는 형태가 아닙니다.

**Projection 행렬**(투영 행렬)은 뷰 공간 좌표를 화면 표시를 위한 다음 형태로 변환하며, 그 결과가 **클립 공간(Clip Space)** 좌표입니다.

<br>

투영 과정은 카메라가 볼 수 있는 3D 영역인 **절두체(Frustum)**를 정규화된 직육면체로 변환합니다.

Projection 행렬이 절두체의 기하 정보를 동차 좌표에 인코딩하고, 이후 w 나눗셈(원근 나눗셈, NDC 섹션에서 설명)까지 거치면 직육면체가 완성됩니다.

절두체는 카메라의 시야각(FOV), 화면 비율(aspect ratio), 가까운 평면(near plane)과 먼 평면(far plane)으로 정의되는 잘린 사각뿔 형태의 공간입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Near plane -->
  <line x1="120" y1="120" x2="120" y2="180" stroke="currentColor" stroke-width="2"/>
  <!-- Far plane -->
  <line x1="420" y1="30" x2="420" y2="270" stroke="currentColor" stroke-width="2"/>
  <!-- Top edge -->
  <line x1="120" y1="120" x2="420" y2="30" stroke="currentColor" stroke-width="1.5"/>
  <!-- Bottom edge -->
  <line x1="120" y1="180" x2="420" y2="270" stroke="currentColor" stroke-width="1.5"/>
  <!-- Center axis (dashed) -->
  <line x1="20" y1="150" x2="420" y2="150" stroke="currentColor" stroke-dasharray="6,4" stroke-width="0.7" opacity="0.3"/>
  <!-- Camera point -->
  <circle cx="20" cy="150" r="5" fill="currentColor"/>
  <!-- Camera to near plane edges (dashed, collinear with frustum edges) -->
  <line x1="20" y1="150" x2="120" y2="120" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <line x1="20" y1="150" x2="120" y2="180" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <!-- FOV angle arc -->
  <path d="M 48.7,141.4 A 30,30 0 0,1 48.7,158.6" fill="none" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="66" y="154" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">FOV</text>
  <!-- Labels -->
  <text fill="currentColor" x="20" y="173" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">카메라</text>
  <text fill="currentColor" x="120" y="198" text-anchor="middle" font-size="10" font-family="sans-serif">Near Plane</text>
  <text fill="currentColor" x="420" y="290" text-anchor="middle" font-size="10" font-family="sans-serif">Far Plane</text>
  <!-- Distance indicator: n (camera → near) -->
  <line x1="20" y1="228" x2="120" y2="228" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="20" y1="224" x2="20" y2="232" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="120" y1="224" x2="120" y2="232" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="70" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">n</text>
  <!-- Distance indicator: f (camera → far) -->
  <line x1="20" y1="258" x2="420" y2="258" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="20" y1="254" x2="20" y2="262" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="420" y1="254" x2="420" y2="262" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <text fill="currentColor" x="220" y="274" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">f</text>
  <!-- Bottom note -->
  <text fill="currentColor" x="260" y="298" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">절두체 안의 오브젝트만 렌더링</text>
  <text fill="currentColor" x="260" y="312" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">경계와 교차하는 폴리곤은 잘려서 보이는 부분만 그려짐</text>
</svg>
</div>

투영 행렬은 절두체의 기하 정보를 동차 좌표에 인코딩하고, 이후 w로 나누는 원근 나눗셈(NDC 변환)까지 거치면 절두체가 정규화된 직육면체로 정리됩니다.

이 과정에서 1/w 스케일이 적용되어, 먼 오브젝트일수록 NDC 좌표가 크게 줄어들며 화면에서 작게 보이고, 가까운 오브젝트는 상대적으로 크게 유지됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 245" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <!-- === Left: View Space (3D Frustum) === -->
  <text fill="currentColor" x="85" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">뷰 공간</text>
  <!-- Camera -->
  <circle cx="10" cy="108" r="3.5" fill="currentColor"/>
  <!-- Camera rays to near face corners (solid: visible, dashed: hidden) -->
  <line x1="10" y1="108" x2="36" y2="91" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="10" y1="108" x2="56" y2="91" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="10" y1="108" x2="56" y2="123" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
  <line x1="10" y1="108" x2="36" y2="123" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 3D Frustum: oblique projection, view from front-top-right -->
  <!-- Near face: NTL(36,91) NTR(56,91) NBR(56,123) NBL(36,123) -->
  <!-- Far face:  FTL(82,60) FTR(140,60) FBR(140,150) FBL(82,150) -->
  <!-- Visible faces (solid) -->
  <!-- Near face (front) -->
  <polygon points="36,91 56,91 56,123 36,123" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <!-- Top surface -->
  <polygon points="36,91 56,91 140,60 82,60" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1"/>
  <!-- Right surface -->
  <polygon points="56,91 56,123 140,150 140,60" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1"/>
  <!-- Hidden edges (dashed): NBL→FBL, FBL→FTL, FBL→FBR -->
  <line x1="36" y1="123" x2="82" y2="150" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="82" y1="150" x2="82" y2="60" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="82" y1="150" x2="140" y2="150" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- A (near, 30% depth) -->
  <circle cx="66" cy="106" r="7" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="66" y="110" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">A</text>
  <text fill="currentColor" x="66" y="126" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">가까움</text>
  <!-- B (far, 75% depth) -->
  <circle cx="95" cy="106" r="7" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="95" y="110" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">B</text>
  <text fill="currentColor" x="95" y="126" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">멀음</text>
  <!-- === Arrow 1: Projection Matrix === -->
  <line x1="150" y1="108" x2="240" y2="108" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="247,108 240,104 240,112" fill="currentColor"/>
  <text fill="currentColor" x="198" y="96" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">투영 행렬</text>
  <!-- === Middle: Clip Space (3D Box) === -->
  <text fill="currentColor" x="310" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">클립 공간</text>
  <text fill="currentColor" x="310" y="30" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">(동차 좌표)</text>
  <text fill="currentColor" x="310" y="44" text-anchor="middle" font-size="7.5" font-family="sans-serif" opacity="0.5">−w ≤ x, y, z ≤ +w</text>
  <!-- 3D cuboid: oblique projection (dx=20, dy=-15) -->
  <!-- Front face: FTL(254,72) FTR(346,72) FBR(346,158) FBL(254,158) -->
  <!-- Back face:  BTL(274,57) BTR(366,57) BBR(366,143) BBL(274,143) -->
  <!-- Visible faces (solid) -->
  <!-- Front face -->
  <polygon points="254,72 346,72 346,158 254,158" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>
  <!-- Top face -->
  <polygon points="254,72 274,57 366,57 346,72" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1"/>
  <!-- Right face -->
  <polygon points="346,72 366,57 366,143 346,158" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1"/>
  <!-- Hidden edges (dashed): all from BBL -->
  <line x1="274" y1="143" x2="274" y2="57" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="274" y1="143" x2="366" y2="143" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="274" y1="143" x2="254" y2="158" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- A in clip space (25% depth, same size r=7) -->
  <circle cx="305" cy="111" r="7" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="305" y="115" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">A</text>
  <text fill="currentColor" x="305" y="88" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">w 작음</text>
  <!-- B in clip space (75% depth, same size r=7) -->
  <circle cx="315" cy="104" r="7" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="315" y="108" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">B</text>
  <text fill="currentColor" x="315" y="81" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">w 큼</text>
  <!-- === Arrow 2: Perspective Divide === -->
  <line x1="374" y1="108" x2="451" y2="108" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="458,108 451,104 451,112" fill="currentColor"/>
  <text fill="currentColor" x="416" y="96" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">÷w</text>
  <text fill="currentColor" x="416" y="125" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">원근 나눗셈</text>
  <!-- === Right: NDC (3D Cuboid) === -->
  <text fill="currentColor" x="525" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">NDC</text>
  <text fill="currentColor" x="525" y="30" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">(정규화된 직육면체)</text>
  <text fill="currentColor" x="525" y="44" text-anchor="middle" font-size="7.5" font-family="sans-serif" opacity="0.5">−1 ≤ x, y ≤ 1</text>
  <!-- 3D cuboid: oblique projection (dx=20, dy=-15) — unified with clip space -->
  <!-- Front face: FTL(468,72) FTR(558,72) FBR(558,158) FBL(468,158) -->
  <!-- Back face:  BTL(488,57) BTR(578,57) BBR(578,143) BBL(488,143) -->
  <!-- Visible faces (solid) -->
  <!-- Front face -->
  <polygon points="468,72 558,72 558,158 468,158" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>
  <!-- Top face -->
  <polygon points="468,72 488,57 578,57 558,72" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1"/>
  <!-- Right face -->
  <polygon points="558,72 578,57 578,143 558,158" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1"/>
  <!-- Hidden edges (dashed): all from BBL -->
  <line x1="488" y1="143" x2="488" y2="57" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="488" y1="143" x2="578" y2="143" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="488" y1="143" x2="468" y2="158" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- A in NDC: near front, larger (÷ small w → big result) -->
  <circle cx="515" cy="114" r="11" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="515" y="119" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">A</text>
  <!-- B in NDC: near back, smaller (÷ large w → small result) -->
  <circle cx="531" cy="102" r="4" stroke="currentColor" stroke-width="1.3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="531" y="105" text-anchor="middle" font-size="7" font-weight="bold" font-family="sans-serif">B</text>
  <!-- Bottom annotations -->
  <text fill="currentColor" x="320" y="197" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.7">w에는 카메라 기준 깊이가 인코딩됨 → 깊이가 클수록(멀수록) w가 큼</text>
  <text fill="currentColor" x="320" y="215" text-anchor="middle" font-size="9.5" font-family="sans-serif" opacity="0.7">÷w 후(NDC) 먼 B의 좌표가 더 줄어들어 → 화면에서 작게 보임</text>
</svg>
</div>

클립 공간의 좌표는 [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)에서 다룬 **동차 좌표(Homogeneous Coordinates)** (x, y, z, w) 형태입니다.

Part 2에서 w는 변환 전 입력 좌표의 성질(w=1 위치, w=0 방향)을 나타냈지만, Projection 행렬을 거치면 w의 값이 바뀌어, 뷰 공간의 z값(카메라 기준 깊이)이 w에 기록됩니다.

먼 오브젝트일수록 w가 크고, 가까운 오브젝트일수록 w가 작습니다.

다음 단계인 NDC 변환에서 x, y, z를 이 w로 나누면, w가 큰(먼) 오브젝트의 NDC 좌표가 더 크게 줄어들어 화면에서 작게 표시됩니다. 위 다이어그램에서 A와 B의 크기 변화가 이 과정을 보여줍니다.

<br>

**클리핑(Clipping)**은 이 공간에서 수행됩니다.

클립 공간에서 좌표의 각 성분이 -w ~ +w 범위 안에 있으면 절두체 내부, 벗어나면 절두체 외부입니다.

모든 정점이 범위 밖인 삼각형은 통째로 버려지고, 경계에 걸친 삼각형은 절두체 경계에서 잘려 보이는 부분만 남습니다.

"클립 공간"이라는 이름 자체가 이 클리핑이 수행되는 공간이라는 뜻에서 유래합니다.

---

## NDC (Normalized Device Coordinates)

클리핑을 통과한 클립 공간 좌표에 대해, x, y, z를 w로 나누는 **원근 나눗셈(Perspective Division)**을 수행하면 NDC 좌표가 됩니다.

$$x_{ndc} = \frac{x_{clip}}{w_{clip}}, \quad y_{ndc} = \frac{y_{clip}}{w_{clip}}, \quad z_{ndc} = \frac{z_{clip}}{w_{clip}}$$

원근 나눗셈은 GPU 하드웨어가 자동으로 수행합니다. 버텍스 셰이더가 클립 공간 좌표를 출력하면, 래스터라이저 단계에서 w로 나누어 NDC로 변환합니다.

<br>

NDC 좌표는 장치 해상도에 의존하지 않도록 정규화(Normalized)되어 있습니다. x, y 범위는 [-1, 1]로, NDC 기준 (-1, -1)이 좌측 하단, (1, 1)이 우측 상단에 해당합니다. 이후 뷰포트 변환(Viewport Transform)에서 실제 픽셀 좌표로 매핑되며, API에 따라 y축 방향이 달라질 수 있습니다. z 범위도 그래픽스 API에 따라 다릅니다.

<br>

$w$에는 카메라 기준 깊이가 들어 있으므로, 같은 $(x, y)$라도 $w$가 작으면(가까우면) 나눈 결과가 크고, $w$가 크면(멀면) 나눈 결과가 작습니다. 클립 좌표 $(1.2,\; 0.8)$이 같은 두 오브젝트를 비교하면, 가까운 A($w = 2$)는 NDC $(0.6,\; 0.4)$, 먼 B($w = 5$)는 NDC $(0.24,\; 0.16)$이 됩니다. A의 NDC 좌표가 B보다 크므로, 원근 나눗셈을 거친 A가 화면에서 더 크게 표시됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <text fill="currentColor" x="210" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">NDC의 x, y 범위</text>
  <!-- NDC square (200×200, x,y both [-1,1]) -->
  <rect x="100" y="35" width="200" height="200" stroke="currentColor" stroke-width="1.8" fill="currentColor" fill-opacity="0.04" rx="2"/>
  <!-- Center diamond -->
  <polygon points="200,128 207,135 200,142 193,135" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="218" y="140" font-size="9" font-family="sans-serif" opacity="0.5">원점</text>
  <!-- Y axis labels -->
  <text fill="currentColor" x="88" y="42" text-anchor="end" font-size="10" font-family="sans-serif">1.0</text>
  <text fill="currentColor" x="88" y="140" text-anchor="end" font-size="10" font-family="sans-serif">0.0</text>
  <text fill="currentColor" x="88" y="240" text-anchor="end" font-size="10" font-family="sans-serif">-1.0</text>
  <text fill="currentColor" x="72" y="140" text-anchor="end" font-size="11" font-weight="bold" font-family="sans-serif">Y</text>
  <!-- X axis labels -->
  <text fill="currentColor" x="100" y="253" text-anchor="middle" font-size="10" font-family="sans-serif">-1.0</text>
  <text fill="currentColor" x="200" y="253" text-anchor="middle" font-size="10" font-family="sans-serif">0.0</text>
  <text fill="currentColor" x="300" y="253" text-anchor="middle" font-size="10" font-family="sans-serif">1.0</text>
  <text fill="currentColor" x="330" y="253" font-size="11" font-weight="bold" font-family="sans-serif">X</text>
</svg>
<p style="font-size: 0.9em; opacity: 0.6; margin-top: 0.5em;">Z(NDC) 범위 — OpenGL: [-1, 1], DirectX / Metal / Vulkan: [0, 1]</p>
</div>

<br>

Unity는 내부적으로 플랫폼의 그래픽스 API에 맞게 Z 범위를 자동 조정합니다.

셰이더를 작성할 때 플랫폼별 Z 범위 차이를 직접 처리해야 하는 경우는 거의 없지만, 깊이 버퍼를 직접 읽거나 커스텀 투영 행렬을 구성할 때는 이 차이를 인지하고 있어야 합니다.

---

## 화면 공간 (Screen Space)

NDC까지 정규화된 좌표를 실제 화면의 **픽셀 좌표**로 변환하면 화면 공간(Screen Space)이 됩니다. 이 변환을 **뷰포트 변환(Viewport Transform)**이라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Left: NDC (square: x,y both [-1,1]) -->
  <text fill="currentColor" x="95" y="18" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">NDC</text>
  <rect x="35" y="35" width="120" height="120" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.04" rx="2"/>
  <!-- NDC labels -->
  <text fill="currentColor" x="28" y="42" text-anchor="end" font-size="9" font-family="sans-serif">1.0</text>
  <text fill="currentColor" x="28" y="160" text-anchor="end" font-size="9" font-family="sans-serif">-1.0</text>
  <text fill="currentColor" x="14" y="100" text-anchor="end" font-size="10" font-weight="bold" font-family="sans-serif">Y</text>
  <text fill="currentColor" x="35" y="175" text-anchor="middle" font-size="9" font-family="sans-serif">-1.0</text>
  <text fill="currentColor" x="155" y="175" text-anchor="middle" font-size="9" font-family="sans-serif">1.0</text>
  <text fill="currentColor" x="170" y="175" font-size="10" font-weight="bold" font-family="sans-serif">X</text>
  <!-- Center: Arrow -->
  <line x1="170" y1="95" x2="310" y2="95" stroke="currentColor" stroke-width="2"/>
  <polygon points="313,95 305,90 305,100" fill="currentColor"/>
  <text fill="currentColor" x="242" y="82" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">뷰포트 변환</text>
  <!-- Right: Screen Space -->
  <text fill="currentColor" x="430" y="18" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">화면 공간 (1920 x 1080)</text>
  <rect x="330" y="35" width="200" height="120" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.04" rx="2"/>
  <!-- Screen labels -->
  <text fill="currentColor" x="323" y="42" text-anchor="end" font-size="9" font-family="sans-serif">1080</text>
  <text fill="currentColor" x="323" y="160" text-anchor="end" font-size="9" font-family="sans-serif">0</text>
  <text fill="currentColor" x="308" y="100" text-anchor="end" font-size="10" font-weight="bold" font-family="sans-serif">Y</text>
  <text fill="currentColor" x="330" y="175" text-anchor="middle" font-size="9" font-family="sans-serif">0</text>
  <text fill="currentColor" x="530" y="175" text-anchor="middle" font-size="9" font-family="sans-serif">1920</text>
  <text fill="currentColor" x="545" y="175" font-size="10" font-weight="bold" font-family="sans-serif">X</text>
</svg>
</div>

화면 해상도가 $width \times height$이고 뷰포트 시작점이 $(x_0,\; y_0)$일 때, 변환 공식은 단순한 스케일과 오프셋입니다.

$$x_{screen} = \frac{x_{ndc} + 1}{2} \times width + x_0$$

$$y_{screen} = \frac{y_{ndc} + 1}{2} \times height + y_0$$

예시 ($1920 \times 1080$):
- NDC $(0,\; 0)$ → 화면 $(960,\; 540)$: 화면 중앙
- NDC $(-1,\; -1)$ → 화면 $(0,\; 0)$: 왼쪽 아래
- NDC $(1,\; 1)$ → 화면 $(1920,\; 1080)$: 오른쪽 위

<br>

뷰포트 변환도 GPU 하드웨어가 자동으로 처리합니다. 래스터라이저 단계에서 NDC 좌표를 픽셀 좌표로 변환한 뒤, 삼각형이 덮는 픽셀 영역을 판정하고 각 픽셀마다 **프래그먼트(Fragment)**를 생성합니다. 프래그먼트는 해당 픽셀에서 실행할 셰이딩 연산의 입력 데이터 묶음으로, 보간된 좌표·UV·법선 등을 담고 있습니다.

Unity에서는 CPU 측에서도 공간 변환 함수를 제공합니다. `Camera.WorldToScreenPoint()`는 월드 공간 좌표를 뷰·투영·뷰포트 변환까지 한 번에 적용하여 화면 픽셀 좌표로 변환합니다. 반대로 화면 좌표를 월드 공간으로 역변환할 때는 `Camera.ScreenToWorldPoint()`나 `Camera.ScreenPointToRay()`를 사용합니다. UI 요소를 3D 오브젝트 위치에 겹쳐 배치할 때는 전자를, 마우스 클릭 지점에서 3D 공간으로 레이를 쏠 때는 후자를 사용하는 것이 대표적인 예입니다.

---

## MVP 행렬의 의미

오브젝트 공간에서 클립 공간까지의 세 단계는 각각 Model, View, Projection 행렬로 수행됩니다. 이 세 행렬을 합쳐서 **MVP 행렬**이라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 140" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Box 1: Object Space -->
  <rect x="10" y="20" width="90" height="44" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="55" y="39" text-anchor="middle" font-size="10" font-family="sans-serif">오브젝트 공간</text>
  <text fill="currentColor" x="55" y="53" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(x, y, z, 1)</text>
  <!-- Arrow: Model -->
  <line x1="100" y1="42" x2="150" y2="42" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="153,42 146,38 146,46" fill="currentColor"/>
  <text fill="currentColor" x="127" y="32" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">Model</text>
  <!-- Box 2: World Space -->
  <rect x="156" y="24" width="72" height="36" rx="6" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.04"/>
  <text fill="currentColor" x="192" y="47" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">월드 공간</text>
  <!-- Arrow: View -->
  <line x1="228" y1="42" x2="278" y2="42" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="281,42 274,38 274,46" fill="currentColor"/>
  <text fill="currentColor" x="255" y="32" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">View</text>
  <!-- Box 3: View Space -->
  <rect x="284" y="24" width="72" height="36" rx="6" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.04"/>
  <text fill="currentColor" x="320" y="47" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">뷰 공간</text>
  <!-- Arrow: Projection -->
  <line x1="356" y1="42" x2="415" y2="42" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="418,42 411,38 411,46" fill="currentColor"/>
  <text fill="currentColor" x="387" y="32" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">Projection</text>
  <!-- Box 4: Clip Space -->
  <rect x="421" y="20" width="100" height="44" rx="6" stroke="currentColor" stroke-width="1.5" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="471" y="39" text-anchor="middle" font-size="10" font-family="sans-serif">클립 공간</text>
  <text fill="currentColor" x="471" y="53" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(x', y', z', w')</text>
  <!-- MVP bracket (bottom) -->
  <line x1="100" y1="80" x2="100" y2="88" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <line x1="100" y1="88" x2="418" y2="88" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <line x1="418" y1="80" x2="418" y2="88" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text fill="currentColor" x="259" y="106" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.7">MVP</text>
  <!-- Formula hint -->
  <text fill="currentColor" x="259" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">v_clip = P × V × M × v_object</text>
</svg>
</div>

$$\mathbf{v}_{clip} = \mathbf{P} \times \mathbf{V} \times \mathbf{M} \times \mathbf{v}_{object}$$

행렬 곱셈은 오른쪽에서 왼쪽으로 적용됩니다. 정점에 $\mathbf{M}$(Model)을 먼저 곱하고, 그 결과에 $\mathbf{V}$(View)를 곱하고, 그 결과에 $\mathbf{P}$(Projection)를 곱합니다.

행렬 곱셈은 결합 법칙(associative law)이 성립합니다.

결합 법칙이란 $(\mathbf{A} \times \mathbf{B}) \times \mathbf{C} = \mathbf{A} \times (\mathbf{B} \times \mathbf{C})$가 성립한다는 뜻으로, 곱셈 순서를 바꾸지 않는 한 어떤 쌍을 먼저 곱해도 결과가 같다는 성질입니다. 이 성질 덕분에 $\mathbf{P} \times \mathbf{V} \times \mathbf{M}$을 미리 하나의 행렬로 곱해둘 수 있고, 정점 하나당 행렬 곱셈 한 번으로 오브젝트 공간에서 클립 공간까지의 변환이 완료됩니다.

<br>

**개별 적용** (정점당 행렬-벡터 곱셈 3번):

$$\mathbf{v}_{world} = \mathbf{M} \times \mathbf{v}$$

$$\mathbf{v}_{view} = \mathbf{V} \times \mathbf{v}_{world}$$

$$\mathbf{v}_{clip} = \mathbf{P} \times \mathbf{v}_{view}$$

**MVP로 합쳐서 적용** (정점당 행렬-벡터 곱셈 1번):

$$\mathbf{MVP} = \mathbf{P} \times \mathbf{V} \times \mathbf{M} \quad \text{(오브젝트당 1회, 사전 계산)}$$

$$\mathbf{v}_{clip} = \mathbf{MVP} \times \mathbf{v}$$

MVP 행렬을 사전에 계산하면 정점당 행렬-벡터 곱셈 횟수가 3번에서 1번으로 줄어듭니다. 행렬-행렬 곱셈(MVP 계산)은 오브젝트당 1번만 수행하면 되므로, 정점이 많을수록 절약 효과가 커집니다.

<br>

다만 항상 MVP 하나로 끝낼 수 있는 것은 아닙니다.

셰이더에서 조명 계산을 수행하려면 월드 공간이나 뷰 공간에서의 좌표가 필요한데, MVP로 한 번에 클립 공간까지 변환하면 중간 단계의 좌표를 알 수 없습니다. 이 경우에는 Model 행렬이나 View 행렬을 별도로 적용하여 중간 좌표를 따로 구해야 합니다.

---

### 버텍스 셰이더에서의 MVP

버텍스 셰이더의 핵심 역할이 MVP 변환입니다. [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)의 렌더링 파이프라인에서, 버텍스 셰이더가 각 정점의 좌표를 변환한다고 설명한 것이 이 과정에 대한 설명입니다.

<br>

Unity의 셰이더에서는 `UnityObjectToClipPos(v.vertex)`라는 함수가 MVP 변환을 수행합니다. 이 함수의 내부 연산은 다음과 같습니다.

- 입력: 오브젝트 공간의 정점 좌표 $\mathbf{v} = (x,\; y,\; z,\; 1)$
- 출력: 클립 공간의 좌표 $(x',\; y',\; z',\; w')$

$$\mathbf{v}_{clip} = \underbrace{\texttt{UNITY\_MATRIX\_VP}}_{\mathbf{P} \times \mathbf{V}} \times \underbrace{\texttt{unity\_ObjectToWorld}}_{\mathbf{M}} \times \mathbf{v}$$

Unity는 내부적으로 `UNITY_MATRIX_MVP` 대신 `UNITY_MATRIX_VP`(Projection × View)와 `unity_ObjectToWorld`(Model)를 분리하여 관리합니다.

View 행렬(`Camera.worldToCameraMatrix`)과 Projection 행렬(`Camera.projectionMatrix`)은 카메라에 의존하므로, 같은 카메라로 렌더링하는 동안 VP는 한 번만 계산하면 됩니다.

반면 Model 행렬(`transform.localToWorldMatrix`)은 오브젝트마다 다르므로, VP를 재사용하고 오브젝트마다 Model만 교체하는 방식이 효율적입니다.

`UnityObjectToClipPos()` 함수는 내부적으로 이 VP/Model 분리 방식을 사용하며, GPU 인스턴싱 처리까지 포함하고 있으므로 MVP 변환을 직접 작성하는 것보다 안전합니다.

---

### 전체 변환 과정 정리

정점 하나가 화면 픽셀이 되기까지의 전체 과정을 구체적인 수치로 정리합니다.

<br>

```
정점 좌표 변환의 전체 흐름 (예시)

1. 오브젝트 공간
   정점 좌표: (0, 1.8, 0, 1)
   (캐릭터 모델의 머리 위치)

2. 월드 공간  ← Model 행렬 적용
   Transform: position=(10, 0, 5), rotation=none, scale=1
   결과: (10, 1.8, 5, 1)
   (씬에서 캐릭터가 서 있는 위치)

3. 뷰 공간  ← View 행렬 적용
   카메라: 위치=(10, 2, 0), +Z 방향을 바라봄
   결과: (0, -0.2, -5, 1)
   (카메라 기준 — 정면 5m 앞, 약간 아래)

4. 클립 공간  ← Projection 행렬 적용
   FOV=60°, aspect=16:9, near=0.3, far=1000
   결과: (0, -0.35, 4.40, 5)
   (w에 뷰 공간 깊이 5가 들어감)

5. NDC  ← 원근 나눗셈 (÷w)
   결과: (0, -0.07, 0.88)
   (화면 중앙에서 약간 아래 / 깊이 0.88)

6. 화면 공간  ← 뷰포트 변환
   해상도: 1920×1080
   결과: (960, 578)
   (화면 중앙에서 약간 아래의 픽셀)
```

위 과정에서 셰이더가 담당하는 부분은 1~4단계(MVP 변환)이고, 5~6단계는 GPU 하드웨어가 자동으로 처리합니다. 버텍스 셰이더가 클립 공간의 좌표를 출력하면, 이후 과정은 개발자가 개입할 필요 없이 GPU가 수행합니다.

---

## 마무리

3D 정점이 화면의 2D 픽셀이 되기까지 6개의 좌표 공간을 순서대로 거칩니다. 각 공간은 서로 다른 기준 원점과 축을 가지며, 공간 사이의 전환은 행렬 곱셈으로 이루어집니다.

<br>

- **오브젝트 공간**은 메쉬 자체의 로컬 좌표계이며, 모델의 중심이 원점입니다.
- **월드 공간**은 씬 전체의 공통 좌표계입니다. Model 행렬(Transform의 position, rotation, scale)이 오브젝트 공간에서 월드 공간으로 변환합니다.
- **뷰 공간**은 카메라를 원점에, 시선 방향을 -Z에 놓은 좌표계입니다. View 행렬(카메라 Transform의 역변환)이 월드 공간에서 뷰 공간으로 변환합니다.
- **클립 공간**은 Projection 행렬이 절두체를 직육면체로 변환한 결과이며, 클리핑은 이 공간에서 수행됩니다.
- **NDC**는 클립 공간 좌표를 w로 나누어 x, y 범위를 [-1, 1]로 정규화한 좌표입니다.
- **화면 공간**은 NDC를 뷰포트 변환으로 픽셀 좌표로 변환한 최종 결과입니다.
- 버텍스 셰이더의 핵심 역할은 Model, View, Projection을 순서대로 적용하는 **MVP 변환**이며, Unity에서는 `UnityObjectToClipPos()`로 수행합니다.

Projection 행렬의 내부 원리인 원근 투영과 직교 투영의 행렬 구성, 깊이 값의 비선형성, 그리고 이로 인한 Z-fighting 문제와 해결 방법은 [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 이어집니다.

---

**관련 글**
- [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)

**시리즈**
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- **그래픽스 수학 (3) - 좌표 공간의 전환 (현재 글)**
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- **그래픽스 수학 (3) - 좌표 공간의 전환** (현재 글)
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
