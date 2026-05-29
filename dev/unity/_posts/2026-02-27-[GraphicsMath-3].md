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

[그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)에서는 이동, 회전, 스케일을 행렬로 표현하고, 여러 변환을 하나의 4x4 행렬로 합치는 방법을 다뤘습니다.
이번 글에서는 그 행렬들이 실제 렌더링 과정에서 어떤 순서로 쓰이는지 살펴봅니다.

메쉬 안에 저장된 정점 좌표는 곧바로 화면 좌표가 되지 않습니다. 먼저 오브젝트 기준의 좌표로 해석되고, 씬 기준으로 옮겨진 뒤, 카메라와 투영을 거쳐 최종적으로 화면 좌표계까지 이동합니다.

이 과정에서 정점 좌표는 여러 **좌표 공간(Coordinate Space)**을 거칩니다. 좌표 공간은 어떤 위치를 어느 원점과 어느 축을 기준으로 표현할지 정하는 좌표 체계입니다. 같은 점이라도 오브젝트 기준으로 보면 로컬 좌표가 되고, 씬 기준으로 보면 월드 좌표가 되며, 카메라 기준으로 보면 뷰 좌표가 됩니다.

렌더링 과정은 이 좌표 체계를 단계적으로 바꿔 가며 정점의 위치를 계산합니다. 메쉬 안에서는 오브젝트 기준 좌표였던 값이, 다음 단계에서는 씬 기준 좌표가 되고, 다시 카메라 기준 좌표와 투영된 좌표로 바뀝니다. 이런 공간 전환을 계산할 때 사용하는 것이 변환 행렬입니다.

이 글에서는 이 흐름을 따라, 오브젝트 공간의 정점 좌표가 Model 행렬로 월드 공간 좌표가 되고, View 행렬로 카메라 기준 좌표가 되며, Projection 행렬로 클립 공간 좌표가 되는 과정을 먼저 다룹니다. 이어서 클립 공간 좌표가 `w` 나눗셈으로 NDC가 되고, NDC가 뷰포트 변환을 통해 화면 공간의 픽셀 좌표로 바뀌는 마지막 단계까지 정리합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 360 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 360px; width: 100%;">
  <text fill="currentColor" x="180" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.7">정점 좌표가 지나가는 공간</text>

  <rect x="60" y="42" width="240" height="34" rx="5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="180" y="64" text-anchor="middle" font-size="12" font-family="sans-serif">오브젝트 공간</text>
  <line x1="180" y1="76" x2="180" y2="110" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="180,113 176,105 184,105" fill="currentColor"/>
  <text fill="currentColor" x="226" y="98" font-size="10" font-family="sans-serif" opacity="0.65">Model</text>

  <rect x="60" y="116" width="240" height="34" rx="5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="180" y="138" text-anchor="middle" font-size="12" font-family="sans-serif">월드 공간</text>
  <line x1="180" y1="150" x2="180" y2="184" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="180,187 176,179 184,179" fill="currentColor"/>
  <text fill="currentColor" x="226" y="172" font-size="10" font-family="sans-serif" opacity="0.65">View</text>

  <rect x="60" y="190" width="240" height="34" rx="5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="180" y="212" text-anchor="middle" font-size="12" font-family="sans-serif">뷰 공간</text>
  <line x1="180" y1="224" x2="180" y2="258" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="180,261 176,253 184,253" fill="currentColor"/>
  <text fill="currentColor" x="226" y="246" font-size="10" font-family="sans-serif" opacity="0.65">Projection</text>

  <rect x="60" y="264" width="240" height="34" rx="5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="180" y="286" text-anchor="middle" font-size="12" font-family="sans-serif">클립 공간</text>
  <line x1="180" y1="298" x2="180" y2="332" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="180,335 176,327 184,327" fill="currentColor"/>
  <text fill="currentColor" x="226" y="320" font-size="10" font-family="sans-serif" opacity="0.65">w 나누기</text>

  <rect x="60" y="338" width="240" height="34" rx="5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="180" y="360" text-anchor="middle" font-size="12" font-family="sans-serif">NDC</text>
  <line x1="180" y1="372" x2="180" y2="396" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="180,399 176,391 184,391" fill="currentColor"/>
  <text fill="currentColor" x="226" y="388" font-size="10" font-family="sans-serif" opacity="0.65">Viewport</text>

  <rect x="60" y="402" width="240" height="24" rx="5" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="180" y="419" text-anchor="middle" font-size="12" font-family="sans-serif">화면 공간</text>
</svg>
</div>

---

## 오브젝트 공간 (Object Space)

오브젝트 공간은 메쉬 자체를 기준으로 정점 위치를 표현하는 좌표계입니다. 모델 공간(Model Space) 또는 로컬 공간(Local Space)이라고도 부릅니다.

메쉬의 정점 좌표는 씬 안의 위치가 아니라, 모델 안에서 각 정점이 어디에 있는지를 나타냅니다. 모델을 만들 때 정한 원점과 축이 기준이 되며, 이 기준은 모델의 쓰임에 따라 달라질 수 있습니다. 캐릭터는 발 아래를 원점으로 둘 수 있고, 문처럼 회전축이 중요한 모델은 힌지 위치를 원점으로 둘 수 있습니다. 따라서 오브젝트 공간의 (0, 0, 0)은 항상 모델의 중심이 아니라, 그 모델을 다루기 위해 정한 기준점입니다.

예를 들어 발바닥을 원점으로 만든 캐릭터 메쉬라면, 머리 끝에 가까운 정점의 y 값은 모델의 높이에 가까운 값이 됩니다. 그 값이 1.8이라면, 캐릭터 메쉬의 원점에서 위로 1.8만큼 떨어져 있다는 뜻입니다. 이 값만으로는 씬에서의 위치를 알 수 없습니다.

여기서 메쉬 데이터와 Transform의 역할을 구분해야 합니다. 메쉬 데이터에는 정점들이 메쉬 안에서 어떤 좌표를 갖는지가 저장되어 있고, Transform에는 그 메쉬를 씬의 어디에, 어떤 회전과 크기로 놓을지가 저장되어 있습니다. 그래서 오브젝트를 이동하거나 회전하거나 크기를 바꿔도, 메쉬 안에 저장된 정점 좌표 자체가 바뀌지는 않습니다. Unity에서 `Mesh.vertices`로 읽는 값도 Transform이 적용된 결과가 아니라, 메쉬에 저장된 오브젝트 공간 좌표입니다.

이 좌표가 씬에서 실제로 어디에 놓이는지는 Transform을 적용해야 알 수 있습니다. 그 결과가 월드 공간 좌표입니다.

---

## 월드 공간 (World Space)

월드 공간은 씬 전체에서 공통으로 사용하는 좌표계입니다. 오브젝트 공간 좌표가 메쉬 내부 기준의 위치라면, 월드 공간 좌표는 씬 전체 기준의 위치입니다.

같은 메쉬 데이터도 여러 오브젝트가 공유할 수 있습니다. 이때 메쉬 안의 정점 좌표는 같지만, 각 오브젝트가 가진 Transform은 서로 다를 수 있습니다. 그래서 같은 정점 좌표를 가진 메쉬라도 씬에서는 서로 다른 위치에 나타날 수 있습니다.

따라서 서로 다른 오브젝트의 위치를 비교하려면, 각 정점을 같은 기준인 월드 공간으로 바꿔야 합니다. 두 오브젝트가 얼마나 떨어져 있는지, 어떤 오브젝트가 더 위에 있는지 같은 위치 관계는 월드 좌표를 기준으로 판단합니다.

여기서 필요한 것은 그 메쉬가 씬에 어떻게 배치되어 있는지에 대한 정보입니다. 메쉬 데이터가 정점의 위치를 메쉬 자신의 원점과 축을 기준으로 저장한다면, 배치 정보는 그 메쉬가 씬에서 어떤 위치, 방향, 크기로 놓이는지를 나타냅니다. Unity에서는 이 정보가 오브젝트의 Transform 컴포넌트에 저장되며, 각각 `position`, `rotation`, `localScale`로 표현됩니다.

월드 좌표는 메쉬에 저장된 정점 좌표에 이 배치 정보를 반영한 결과입니다. 즉 메쉬 안에서의 위치에 오브젝트의 크기, 방향, 씬에서의 위치를 함께 적용하면, 그 정점이 씬 전체 기준에서 어디에 있는지 알 수 있습니다.

이 배치 정보를 정점마다 따로따로 적용하기 쉽도록 하나의 4x4 행렬로 묶어 둔 것이 **Model 행렬**입니다. 즉, Model 행렬은 오브젝트 공간 좌표를 월드 공간 좌표로 바꾸는 행렬입니다.

$$
\mathbf{v}_{world} = \mathbf{M}_{model} \times \mathbf{v}_{object}
$$

여기서 $\mathbf{v}_{object}$는 메쉬 안에 저장된 정점 좌표이고, $\mathbf{v}_{world}$는 씬 기준으로 계산된 정점 좌표입니다. 실제 계산에서는 이전 글에서 다룬 것처럼 정점 위치를 동차 좌표 형태로 다룹니다.

<br>

부모가 없는 Unity 오브젝트라면 Model 행렬은 보통 다음처럼 구성됩니다.

$$
\mathbf{M}_{model} = \mathbf{T} \times \mathbf{R} \times \mathbf{S}
$$

`T`는 이동, `R`은 회전, `S`는 스케일입니다. 식은 `T × R × S` 순서로 쓰지만, 정점에 실제로 적용되는 순서는 오른쪽부터입니다. 따라서 로컬 정점은 먼저 스케일되고, 그다음 회전한 뒤, 마지막에 월드 위치로 이동합니다. 스케일과 회전이 먼저 적용되기 때문에 오브젝트는 자기 원점을 기준으로 크기가 바뀌고 회전한 뒤 씬의 위치로 옮겨집니다.

Unity C#에서는 이 Model 행렬을 `transform.localToWorldMatrix`로 얻을 수 있습니다. URP 셰이더에서는 보통 원시 행렬을 직접 다루기보다 `TransformObjectToWorld()` 같은 공간 변환 헬퍼를 사용하고, 행렬 자체가 필요할 때는 `GetObjectToWorldMatrix()`를 사용할 수 있습니다. 오브젝트가 부모 Transform 아래에 있다면 부모의 위치, 회전, 스케일까지 누적된 결과가 `localToWorldMatrix`에 들어갑니다.

이동만 있는 경우에는 Model 행렬의 의미가 가장 단순하게 드러납니다. 오브젝트의 회전이 없고 스케일이 1이며 `position`이 (10, 0, 5)라면, 오브젝트 공간의 정점 (0, 2, 0)은 월드 공간에서 (10, 2, 5)에 놓입니다. 이때 Model 행렬은 모든 정점을 `position`만큼 옮기는 변환이므로, 결과만 보면 다음 덧셈과 같습니다.

$$
(0, 2, 0) + (10, 0, 5) = (10, 2, 5)
$$

이 계산은 Model 행렬을 쓰지 않는 별도의 방법이 아닙니다. 회전과 스케일이 없을 때 Model 행렬의 효과가 단순한 덧셈으로 나타나는 특수한 경우입니다. 회전이나 스케일이 포함되면 정점의 위치에 오브젝트의 크기와 방향 변화까지 함께 반영해야 하므로, 단순히 `position`을 더하는 것만으로는 같은 결과를 얻을 수 없습니다. 이런 경우에도 원리는 같습니다. 오브젝트의 스케일, 회전, 이동이 합쳐진 Model 행렬을 정점 좌표에 곱해 월드 좌표를 계산합니다.

같은 메쉬를 여러 오브젝트가 공유할 때 이 구분이 특히 중요합니다. 메쉬 데이터 안의 정점 좌표는 같지만, 씬에 배치된 각 오브젝트는 서로 다른 Transform을 가질 수 있기 떄문입니다. 따라서 같은 오브젝트 공간 좌표라도 어떤 Model 행렬을 적용하느냐에 따라 월드 좌표가 달라집니다.

---

## 뷰 공간 (View Space)

Model 행렬을 적용하면 오브젝트의 정점은 월드 공간에 놓입니다. 하지만 화면에 그리려면 씬 안의 위치만으로는 부족합니다. 같은 월드 좌표라도 카메라가 어디에 있고 어느 방향을 보는지에 따라 화면에서 보이는 위치가 달라지기 때문입니다.

**뷰 공간(View Space)**은 카메라를 기준으로 정점을 다시 표현한 좌표계입니다. 카메라 공간(Camera Space) 또는 눈 공간(Eye Space)이라고도 합니다. 월드 공간에서는 씬의 원점이 기준이지만, 뷰 공간에서는 카메라가 원점이 됩니다.

<br>

월드 공간에서 뷰 공간으로 바꿀 때는 **View 행렬**(뷰 행렬)을 사용합니다. View 행렬은 월드 공간의 정점을 카메라 기준 좌표로 바꾸는 행렬입니다.

카메라 기준으로 좌표를 표현한다는 것은 카메라를 새로운 원점으로 삼고, 카메라의 방향을 좌표축으로 삼는다는 뜻입니다. 그러려면 월드 공간의 점들을 카메라 기준으로 옮겨서 다시 표현해야 합니다. 이 변환에 사용하는 행렬이 View 행렬입니다.

카메라의 local-to-world 행렬은 카메라 로컬 공간의 좌표를 월드 공간으로 옮길 때 쓰입니다. 하지만 뷰 공간을 만들 때 필요한 것은 반대 방향입니다. 이미 월드 공간에 놓인 정점들을 카메라 기준으로 다시 표현해야 하므로, 월드 좌표를 카메라 로컬 좌표로 바꾸는 변환이 필요합니다. 그래서 View 행렬은 카메라의 local-to-world 행렬에 대한 **역행렬(Inverse)**입니다.

직관적으로는 카메라를 뷰 공간의 원점에 고정해 두고, 월드 전체를 카메라 기준으로 다시 놓는 과정이라고 볼 수 있습니다. 그 결과 모든 오브젝트의 좌표는 씬 원점이 아니라 카메라를 기준으로 표현됩니다.

<br>

예를 들어 카메라가 월드의 (10, 5, -3)에 있다면, View 행렬에는 월드의 정점들을 그만큼 반대로 옮기는 변환이 들어갑니다. 카메라가 Y축으로 30도 회전해 있다면, 뷰 변환에는 그 반대 방향의 회전도 포함됩니다. 이렇게 카메라 Transform의 역변환을 적용한 결과가 뷰 공간 좌표입니다.

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
  <!-- Z+ axis (behind camera, diagonal) -->
  <line x1="150" y1="150" x2="95" y2="200" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="92,203 102,198 97,190" fill="currentColor"/>
  <text fill="currentColor" x="72" y="215" font-size="12" font-weight="bold" font-family="sans-serif">Z+</text>
  <text fill="currentColor" x="60" y="230" font-size="10" font-family="sans-serif" opacity="0.6">(카메라 뒤쪽)</text>
  <!-- -Z gaze direction (dashed, scene direction) -->
  <line x1="170" y1="130" x2="225" y2="80" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5"/>
  <polygon points="228,77 220,80 222,88" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="240" y="78" font-size="11" font-family="sans-serif" opacity="0.7">-Z (시선 방향)</text>
  <!-- Legend -->
  <text fill="currentColor" x="180" y="260" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">카메라 앞쪽(장면 쪽) = -Z</text>
</svg>
</div>

<br>

Unity에서 View 행렬에 해당하는 값은 `Camera.worldToCameraMatrix`입니다. 이름 그대로 월드 공간의 좌표를 카메라 기준의 좌표로 바꾸는 행렬입니다.

여기서 혼동하기 쉬운 부분은, Unity의 Transform 기준과 렌더링에서 쓰는 View 공간 기준이 서로 다르다는 점입니다. 씬에서 GameObject를 배치할 때 Unity는 +X를 오른쪽, +Y를 위쪽, +Z를 앞쪽으로 보는 왼손 좌표계 관례를 사용합니다. 카메라도 GameObject이므로 회전이 없다면 `transform.forward`는 월드 +Z 방향을 가리킵니다. 그래서 카메라가 원점에 있고 회전이 없다면, 월드 좌표 (0, 0, 5)에 있는 점은 Unity 씬 기준에서 카메라 앞에 있습니다.

하지만 `worldToCameraMatrix`를 거친 뒤의 View 공간은 카메라 Transform의 로컬 공간을 그대로 따르지 않습니다. View 공간은 오브젝트를 배치하기 위한 좌표계가 아니라, Projection 행렬과 셰이더 계산에서 사용할 렌더링용 카메라 좌표계입니다. 이 좌표계에서는 그래픽스 관례에 따라 카메라가 바라보는 앞쪽을 `-Z` 방향으로 둡니다. 따라서 Unity 씬 기준에서 카메라 앞쪽에 있던 점도 View 공간에서는 음수 z 값을 갖습니다.

예를 들어 회전이 없는 카메라가 원점에 있을 때, 월드 좌표 (0, 0, 5)는 `worldToCameraMatrix`를 거치면 View 공간에서 (0, 0, -5)가 됩니다. 점이 카메라 뒤로 간 것이 아닙니다. 같은 위치를 렌더링용 카메라 좌표계로 다시 표현했기 때문에 z 부호가 바뀐 것입니다.

정리하면 Transform 좌표계는 개발자가 씬에서 오브젝트와 카메라를 배치하기 위한 기준이고, View 공간은 Projection 행렬, 클리핑, 셰이더 계산으로 넘기기 위한 렌더링용 기준입니다. `worldToCameraMatrix`는 월드 공간의 점들을 이 렌더링용 카메라 기준으로 변환합니다.

---

## 클립 공간 (Clip Space)

View 행렬을 거치면 정점은 카메라를 원점으로 한 3D 좌표가 됩니다. 그런데 카메라가 보는 공간은 무한히 펼쳐진 3D 공간 전체가 아니라 그중 정해진 범위뿐이고, 이 범위를 **절두체(Frustum)**라고 합니다.

절두체는 시야각(FOV), 화면 비율(aspect ratio), 가까운 평면(near plane), 먼 평면(far plane)이 함께 잘라낸 사각뿔 모양의 공간을 가리킵니다. 그래서 정점이 카메라 기준으로 어디에 있는지를 아는 것만으로는 부족하고, 그 정점이 이 절두체 안에 들어오는지까지 가려내야 합니다.

문제는 절두체가 카메라에서 멀어질수록 벌어지는 비스듬한 사각뿔이라는 데 있습니다. 이 모양 그대로 정점이 안쪽인지 판정하려면 비스듬히 기운 여섯 면을 일일이 기준 삼아 비교해야 합니다. **Projection(투영) 행렬**은 이 번거로운 판정을 GPU가 다루기 쉬운 형태로 바꾸는데, 행렬을 거친 직후의 좌표 공간이 바로 **클립 공간(Clip Space)**입니다. 이 공간에서 정점은 `(x, y, z, w)` 네 값으로 표현됩니다.

네 값 가운데 네 번째 성분 `w`가 특히 중요합니다. 원근 투영에서 `w`는 뷰 공간의 깊이에 비례하도록 만들어지는 값입니다. 카메라에 가까운 정점은 작은 `w`를 갖고, 멀리 있는 정점은 큰 `w`를 갖습니다.

이 값은 클립 공간에서 좌우·위아래 경계를 정하는 기준으로 쓰입니다. 절두체는 가까운 곳에서는 좁고 먼 곳에서는 넓기 때문에, 클립 공간의 경계도 모든 정점에 대해 같은 숫자로 고정되지 않습니다. 대신 각 정점이 가진 `w`를 기준으로, 오른쪽은 `x = w`, 왼쪽은 `x = -w`, 위아래는 각각 `y = w`, `y = -w`가 됩니다.

예를 들어 어떤 정점의 `w`가 `5`라면, 그 정점의 `x`는 `-5`부터 `5` 사이에 있어야 좌우 경계 안쪽에 남습니다. `x = 3`은 안쪽이지만, `x = 7`은 오른쪽 경계를 넘어선 값입니다. 먼 정점일수록 `w`가 크기 때문에 허용되는 `x`, `y` 범위도 넓어지고, 이는 카메라에서 멀어질수록 절두체의 단면이 넓어지는 모양과 맞아떨어집니다.

`z`는 좌우·위아래가 아니라 깊이 방향을 검사하는 데 쓰입니다. 즉 정점이 가까운 평면과 먼 평면 사이에 있는지를 가립니다.

> 다만 `z`의 허용 구간은 그래픽스 API마다 다릅니다. OpenGL은 `x`, `y`와 마찬가지로 `-w`부터 `w`까지를 사용하지만, Direct3D나 Vulkan, Metal은 가까운 평면 쪽을 0에 대응시켜 `0`부터 `w`까지를 사용합니다. 일반적인 셰이더 작성에서는 이 차이를 직접 처리할 일이 많지 않습니다. 다만 깊이 버퍼를 직접 읽거나 커스텀 Projection 행렬을 구성할 때는 플랫폼별 Z 범위 차이를 고려해야 합니다.

이렇게 절두체 밖의 대상을 걸러내는 과정을 **클리핑(Clipping)**이라고 합니다. "클립 공간"이라는 이름도 이 클리핑이 수행되는 공간이라는 뜻에서 나왔습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text fill="currentColor" x="320" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">거리와 w에 따라 달라지는 클립 경계</text>

  <!-- Left: frustum widening with distance -->
  <text fill="currentColor" x="170" y="46" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">뷰 공간의 절두체</text>
  <circle cx="34" cy="150" r="5" fill="currentColor"/>
  <text fill="currentColor" x="34" y="174" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">카메라</text>
  <line x1="34" y1="150" x2="120" y2="112" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
  <line x1="34" y1="150" x2="120" y2="188" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
  <line x1="120" y1="112" x2="320" y2="58" stroke="currentColor" stroke-width="1.6"/>
  <line x1="120" y1="188" x2="320" y2="242" stroke="currentColor" stroke-width="1.6"/>
  <line x1="120" y1="112" x2="120" y2="188" stroke="currentColor" stroke-width="2"/>
  <line x1="320" y1="58" x2="320" y2="242" stroke="currentColor" stroke-width="2"/>
  <line x1="34" y1="150" x2="335" y2="150" stroke="currentColor" stroke-width="0.8" stroke-dasharray="6,4" opacity="0.35"/>

  <!-- Width indicators -->
  <line x1="100" y1="112" x2="100" y2="188" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.55"/>
  <polygon points="100,112 96,120 104,120" fill="currentColor" opacity="0.55"/>
  <polygon points="100,188 96,180 104,180" fill="currentColor" opacity="0.55"/>
  <text fill="currentColor" x="88" y="154" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.65">좁음</text>

  <line x1="342" y1="58" x2="342" y2="242" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.55"/>
  <polygon points="342,58 338,66 346,66" fill="currentColor" opacity="0.55"/>
  <polygon points="342,242 338,234 346,234" fill="currentColor" opacity="0.55"/>
  <text fill="currentColor" x="354" y="154" font-size="9" font-family="sans-serif" opacity="0.65">넓음</text>

  <text fill="currentColor" x="120" y="208" text-anchor="middle" font-size="10" font-family="sans-serif">near</text>
  <text fill="currentColor" x="320" y="262" text-anchor="middle" font-size="10" font-family="sans-serif">far</text>
  <text fill="currentColor" x="158" y="82" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">w 작음</text>
  <text fill="currentColor" x="272" y="52" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">w 큼</text>

  <!-- Divider -->
  <line x1="378" y1="38" x2="378" y2="268" stroke="currentColor" stroke-width="1" opacity="0.18"/>

  <!-- Right: clip-space intervals -->
  <text fill="currentColor" x="510" y="46" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">클립 공간의 x 경계</text>

  <!-- Near interval -->
  <text fill="currentColor" x="510" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">가까운 정점: w 작음</text>
  <line x1="430" y1="112" x2="590" y2="112" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <line x1="478" y1="112" x2="542" y2="112" stroke="currentColor" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <line x1="510" y1="100" x2="510" y2="124" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <circle cx="526" cy="112" r="4" fill="currentColor"/>
  <circle cx="558" cy="112" r="4" fill="currentColor" opacity="0.25"/>
  <text fill="currentColor" x="478" y="132" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">-w</text>
  <text fill="currentColor" x="542" y="132" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">w</text>
  <text fill="currentColor" x="526" y="98" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.7">안쪽</text>
  <text fill="currentColor" x="558" y="98" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">바깥</text>

  <!-- Far interval -->
  <text fill="currentColor" x="510" y="170" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">먼 정점: w 큼</text>
  <line x1="430" y1="202" x2="590" y2="202" stroke="currentColor" stroke-width="0.8" opacity="0.25"/>
  <line x1="440" y1="202" x2="580" y2="202" stroke="currentColor" stroke-width="5" stroke-linecap="round" opacity="0.45"/>
  <line x1="510" y1="190" x2="510" y2="214" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <circle cx="558" cy="202" r="4" fill="currentColor"/>
  <text fill="currentColor" x="440" y="222" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">-w</text>
  <text fill="currentColor" x="580" y="222" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">w</text>
  <text fill="currentColor" x="558" y="188" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.7">같은 x도 안쪽</text>

  <text fill="currentColor" x="510" y="264" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">w가 커질수록 허용되는 x 범위가 넓어진다</text>
</svg>
</div>

클리핑을 통과한 클립 공간 좌표는 다음 단계에서 `w`로 나뉘어 정규화된 좌표가 됩니다.

---

## NDC (Normalized Device Coordinates)

**NDC(Normalized Device Coordinates)**는 클립 공간 좌표를 `w`로 나눈 뒤 얻는 정규화된 좌표입니다. 아직 픽셀 좌표는 아니고, 해상도와 무관한 공통 기준으로 위치를 표현하는 중간 단계입니다.

클립 공간에서는 좌우·위아래 경계가 정점마다 `-w`부터 `w`까지로 달라졌습니다. 이제 각 정점의 `x`, `y`, `z`를 자신의 `w`로 나누면, 이 가변적인 경계가 고정된 범위로 정리됩니다. 예를 들어 클립 공간에서 오른쪽 경계였던 `x = w`는 나눈 뒤 `x = 1`이 되고, 왼쪽 경계였던 `x = -w`는 `x = -1`이 됩니다. 이 과정을 **원근 나눗셈(Perspective Division)**이라고 하며, 그 결과가 NDC 좌표입니다.

$$x_{ndc} = \frac{x_{clip}}{w_{clip}}, \quad y_{ndc} = \frac{y_{clip}}{w_{clip}}, \quad z_{ndc} = \frac{z_{clip}}{w_{clip}}$$

원근 나눗셈은 셰이더 코드에서 직접 작성하는 단계가 아니라, GPU의 고정 기능 단계에서 자동으로 수행됩니다. 버텍스 셰이더가 클립 공간 좌표를 출력하면, GPU는 클리핑을 처리한 뒤 `x`, `y`, `z`를 `w`로 나누어 NDC 좌표를 만듭니다.

NDC로 변환된 뒤에는 화면 해상도가 1920x1080이든 2560x1440이든, 보이는 범위의 `x`와 `y`가 기본적으로 `-1`부터 `1` 사이에서 표현됩니다. 이후 뷰포트 변환(Viewport Transform)이 이 정규화된 값을 실제 픽셀 좌표로 바꿉니다.

원근감도 이 나눗셈에서 만들어집니다. 같은 클립 공간의 `x`, `y` 값이라도, 가까운 정점처럼 `w`가 작으면 나눈 뒤에도 비교적 큰 값으로 남고, 먼 정점처럼 `w`가 크면 더 작게 줄어듭니다. 예를 들어 `x = 1.2`, `y = 0.8`인 좌표가 있을 때 `w = 2`라면 NDC는 `(0.6, 0.4)`가 되지만, `w = 5`라면 `(0.24, 0.16)`이 됩니다. 먼 점일수록 NDC에서 화면 중심 쪽으로 더 많이 압축되므로, 결과적으로 화면에서도 더 작게 보입니다.

아래 그림은 위의 원근 나눗셈 예시를 3D 위치, 클립 공간 좌표, NDC 위치로 함께 나타낸 것입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <text fill="currentColor" x="340" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">뷰 공간에서 NDC까지의 원근 나눗셈</text>

  <!-- View-space frustum -->
  <text fill="currentColor" x="126" y="44" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">뷰 공간</text>
  <circle cx="24" cy="156" r="4" fill="currentColor"/>
  <text fill="currentColor" x="24" y="178" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">카메라</text>
  <line x1="24" y1="156" x2="78" y2="123" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="24" y1="156" x2="78" y2="189" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="78,123 104,118 104,194 78,189" fill="currentColor" fill-opacity="0.035" stroke="currentColor" stroke-width="1"/>
  <polygon points="78,123 104,118 224,70 160,88" fill="currentColor" fill-opacity="0.025" stroke="currentColor" stroke-width="1"/>
  <polygon points="104,118 104,194 224,238 224,70" fill="currentColor" fill-opacity="0.025" stroke="currentColor" stroke-width="1"/>
  <line x1="78" y1="189" x2="160" y2="224" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="160" y1="88" x2="160" y2="224" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="160" y1="224" x2="224" y2="238" stroke="currentColor" stroke-width="0.9" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="24" y1="156" x2="226" y2="156" stroke="currentColor" stroke-width="0.8" stroke-dasharray="5,4" opacity="0.22"/>
  <circle cx="112" cy="130" r="5" fill="currentColor"/>
  <text fill="currentColor" x="112" y="118" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">A</text>
  <text fill="currentColor" x="112" y="148" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.65">가까움</text>
  <circle cx="188" cy="144" r="5" fill="currentColor" fill-opacity="0.55" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="188" y="132" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.75">B</text>
  <text fill="currentColor" x="188" y="162" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.65">멀음</text>

  <!-- Projection arrow -->
  <line x1="238" y1="156" x2="282" y2="156" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="288,156 281,152 281,160" fill="currentColor"/>
  <text fill="currentColor" x="263" y="143" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.75">Projection</text>

  <!-- Clip-space coordinate table -->
  <text fill="currentColor" x="374" y="44" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">클립 공간</text>
  <rect x="296" y="64" width="156" height="120" rx="4" fill="currentColor" fill-opacity="0.035" stroke="currentColor" stroke-width="1"/>
  <line x1="296" y1="102" x2="452" y2="102" stroke="currentColor" stroke-width="0.8" opacity="0.22"/>
  <line x1="296" y1="143" x2="452" y2="143" stroke="currentColor" stroke-width="0.8" opacity="0.22"/>
  <text fill="currentColor" x="320" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">점</text>
  <text fill="currentColor" x="386" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">(x, y, z, w)</text>
  <text fill="currentColor" x="320" y="127" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">A</text>
  <text fill="currentColor" x="386" y="127" text-anchor="middle" font-size="10" font-family="monospace">(1.2, 0.8, zA, 2)</text>
  <text fill="currentColor" x="320" y="168" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">B</text>
  <text fill="currentColor" x="386" y="168" text-anchor="middle" font-size="10" font-family="monospace">(1.2, 0.8, zB, 5)</text>
  <text fill="currentColor" x="374" y="205" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">z도 함께 w로 나뉜다</text>

  <!-- Perspective divide arrow -->
  <line x1="463" y1="156" x2="507" y2="156" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="513,156 506,152 506,160" fill="currentColor"/>
  <text fill="currentColor" x="488" y="143" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">÷w</text>

  <!-- NDC x-y plane with a small z cue -->
  <text fill="currentColor" x="592" y="44" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">NDC</text>
  <polygon points="526,80 646,80 646,200 526,200" fill="currentColor" fill-opacity="0.035" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="542,64 662,64 662,184 646,200 646,80 526,80" fill="currentColor" fill-opacity="0.018" stroke="currentColor" stroke-width="0.9" opacity="0.5"/>
  <line x1="526" y1="140" x2="646" y2="140" stroke="currentColor" stroke-width="0.8" opacity="0.32"/>
  <line x1="586" y1="80" x2="586" y2="200" stroke="currentColor" stroke-width="0.8" opacity="0.32"/>
  <line x1="646" y1="200" x2="662" y2="184" stroke="currentColor" stroke-width="0.9" opacity="0.5"/>
  <text fill="currentColor" x="526" y="214" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.65">-1</text>
  <text fill="currentColor" x="586" y="214" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.65">0</text>
  <text fill="currentColor" x="646" y="214" text-anchor="middle" font-size="8.5" font-family="sans-serif" opacity="0.65">1</text>
  <text fill="currentColor" x="516" y="84" text-anchor="end" font-size="8.5" font-family="sans-serif" opacity="0.65">1</text>
  <text fill="currentColor" x="516" y="143" text-anchor="end" font-size="8.5" font-family="sans-serif" opacity="0.65">0</text>
  <text fill="currentColor" x="516" y="203" text-anchor="end" font-size="8.5" font-family="sans-serif" opacity="0.65">-1</text>
  <text fill="currentColor" x="596" y="227" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">x, y는 -1부터 1로 정리</text>
  <text fill="currentColor" x="662" y="194" font-size="8.5" font-family="sans-serif" opacity="0.55">z</text>

  <!-- Points: front x-y plane origin (586,140), scale 60px per NDC unit -->
  <line x1="586" y1="140" x2="622" y2="116" stroke="currentColor" stroke-width="1.1" opacity="0.45"/>
  <line x1="586" y1="140" x2="600" y2="130" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4,3" opacity="0.45"/>
  <circle cx="622" cy="116" r="4" fill="currentColor"/>
  <text fill="currentColor" x="628" y="112" font-size="10" font-weight="bold" font-family="sans-serif">A</text>
  <circle cx="600" cy="130" r="4" fill="currentColor" fill-opacity="0.55" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="606" y="128" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.75">B</text>

  <text fill="currentColor" x="340" y="287" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.65">A와 B는 같은 x, y를 갖지만, w가 큰 B는 NDC에서 원점 쪽으로 더 많이 압축된다</text>
</svg>
</div>

위 그림은 3D 공간의 가까운 점과 먼 점이 클립 공간에서 `(x, y, z, w)` 형태가 되고, 원근 나눗셈 뒤 NDC의 정규화된 범위로 들어오는 흐름을 보여 줍니다. 오른쪽 그림은 화면 위치를 보기 위해 NDC의 x-y 평면을 강조한 것이며, `z`도 함께 `w`로 나뉘어 깊이값으로 정리됩니다.

---

## 화면 공간 (Screen Space)

좌표가 NDC로 변환되면 보이는 영역은 `-1`부터 `1`까지의 정규화된 범위로 정리됩니다. 하지만 이 값은 아직 화면의 몇 번째 픽셀인지를 나타내지 않습니다.

마지막으로 GPU는 NDC의 좌표를 렌더 타깃 안의 뷰포트 사각형에 맞춰 픽셀 좌표로 바꿉니다. 예를 들어 NDC의 왼쪽 끝은 뷰포트의 왼쪽 픽셀 위치로, 오른쪽 끝은 뷰포트의 오른쪽 픽셀 위치로 대응됩니다. 이렇게 얻은 픽셀 기준 좌표가 **화면 공간(Screen Space)**이며, 이 변환을 **뷰포트 변환(Viewport Transform)**이라고 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text fill="currentColor" x="320" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">NDC를 뷰포트 픽셀 좌표로 변환</text>

  <!-- NDC square -->
  <text fill="currentColor" x="125" y="42" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">NDC</text>
  <rect x="45" y="58" width="160" height="130" rx="2" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.035"/>
  <line x1="45" y1="123" x2="205" y2="123" stroke="currentColor" stroke-width="0.8" opacity="0.32"/>
  <line x1="125" y1="58" x2="125" y2="188" stroke="currentColor" stroke-width="0.8" opacity="0.32"/>
  <circle cx="125" cy="123" r="4" fill="currentColor"/>
  <text fill="currentColor" x="134" y="118" font-size="9" font-family="sans-serif" opacity="0.7">(0, 0)</text>
  <text fill="currentColor" x="45" y="204" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">-1</text>
  <text fill="currentColor" x="125" y="204" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">0</text>
  <text fill="currentColor" x="205" y="204" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">1</text>
  <text fill="currentColor" x="36" y="191" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">-1</text>
  <text fill="currentColor" x="36" y="126" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">0</text>
  <text fill="currentColor" x="36" y="61" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">1</text>
  <text fill="currentColor" x="215" y="204" font-size="10" font-weight="bold" font-family="sans-serif">x</text>
  <text fill="currentColor" x="36" y="48" text-anchor="end" font-size="10" font-weight="bold" font-family="sans-serif">y</text>
  <circle cx="45" cy="188" r="3" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="58" y="185" font-size="8.5" font-family="sans-serif" opacity="0.65">(-1, -1)</text>
  <circle cx="205" cy="58" r="3" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="145" y="54" font-size="8.5" font-family="sans-serif" opacity="0.65">(1, 1)</text>

  <!-- Arrow -->
  <line x1="230" y1="123" x2="325" y2="123" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="331,123 323,118 323,128" fill="currentColor"/>
  <text fill="currentColor" x="280" y="108" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">뷰포트 변환</text>
  <text fill="currentColor" x="280" y="142" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">scale + offset</text>

  <!-- Screen/viewport rectangle -->
  <text fill="currentColor" x="480" y="42" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">화면 공간</text>
  <text fill="currentColor" x="480" y="56" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.65">뷰포트: 1920 x 1080</text>
  <rect x="370" y="78" width="220" height="124" rx="2" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.035"/>
  <line x1="370" y1="140" x2="590" y2="140" stroke="currentColor" stroke-width="0.8" opacity="0.32"/>
  <line x1="480" y1="78" x2="480" y2="202" stroke="currentColor" stroke-width="0.8" opacity="0.32"/>
  <circle cx="480" cy="140" r="4" fill="currentColor"/>
  <text fill="currentColor" x="489" y="135" font-size="9" font-family="sans-serif" opacity="0.7">(960, 540)</text>
  <circle cx="370" cy="202" r="3" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="382" y="198" font-size="8.5" font-family="sans-serif" opacity="0.65">(0, 0)</text>
  <circle cx="590" cy="78" r="3" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="500" y="74" font-size="8.5" font-family="sans-serif" opacity="0.65">(1920, 1080)</text>
  <text fill="currentColor" x="370" y="218" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">0</text>
  <text fill="currentColor" x="480" y="218" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">960</text>
  <text fill="currentColor" x="590" y="218" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7">1920</text>
  <text fill="currentColor" x="603" y="218" font-size="10" font-weight="bold" font-family="sans-serif">x</text>
  <text fill="currentColor" x="360" y="205" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">0</text>
  <text fill="currentColor" x="360" y="143" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">540</text>
  <text fill="currentColor" x="360" y="82" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.7">1080</text>
  <text fill="currentColor" x="360" y="68" text-anchor="end" font-size="10" font-weight="bold" font-family="sans-serif">y</text>
</svg>
</div>

뷰포트의 시작점이 $(x_0,\; y_0)$이고 크기가 $width \times height$라면, 뷰포트 변환은 정규화된 좌표를 뷰포트 크기만큼 키운 뒤 시작점만큼 옮기는 과정입니다. 이 글에서는 Unity의 화면 좌표처럼 왼쪽 아래를 $(0,\; 0)$으로 두는 기준을 사용합니다.

$$x_{screen} = \frac{x_{ndc} + 1}{2} \times width + x_0$$

$$y_{screen} = \frac{y_{ndc} + 1}{2} \times height + y_0$$

예를 들어 뷰포트가 화면 전체이고 크기가 $1920 \times 1080$이라면, NDC 좌표는 다음처럼 화면 공간의 위치로 대응됩니다.

- NDC $(-1,\; -1)$ → 화면 $(0,\; 0)$: 왼쪽 아래 경계
- NDC $(0,\; 0)$ → 화면 $(960,\; 540)$: 화면 중앙
- NDC $(1,\; 1)$ → 화면 $(1920,\; 1080)$: 오른쪽 위 경계

즉 뷰포트 변환은 `-1`부터 `1`까지의 정규화된 범위를 실제 뷰포트의 폭과 높이에 맞게 늘려 주는 단계입니다.

<br>

뷰포트 변환도 셰이더 코드에서 직접 작성하는 단계가 아니라, GPU의 고정 기능 단계에서 자동으로 처리됩니다. 이 변환이 끝나면 정점의 위치는 렌더 타깃 안의 뷰포트 좌표로 표현되고, 래스터라이저는 이 좌표를 바탕으로 삼각형이 화면의 어느 영역을 덮는지 계산합니다.

그다음 삼각형이 덮는 각 픽셀 위치에 대해 **프래그먼트(Fragment)**가 만들어집니다. 프래그먼트에는 픽셀 셰이더에서 사용할 보간된 UV, 법선, 색상 같은 값이 함께 전달됩니다.

앞의 변환들은 GPU 렌더링 파이프라인에서 자동으로 일어나지만, Unity는 CPU 코드에서도 비슷한 공간 변환 함수를 제공합니다. `Camera.WorldToScreenPoint()`는 월드 공간의 위치를 현재 카메라 기준의 화면 좌표로 바꿉니다. UI 요소를 3D 오브젝트 위치에 겹쳐 배치할 때 자주 쓰입니다. 반대로 화면 좌표에서 월드 공간 쪽으로 위치나 방향을 구할 때는 `Camera.ScreenToWorldPoint()`나 `Camera.ScreenPointToRay()`를 사용합니다.

---

## MVP 행렬의 의미

지금까지의 공간 변환을 정점 하나의 흐름으로 정리하면, 오브젝트 공간의 좌표는 Model, View, Projection 행렬을 차례로 거쳐 클립 공간 좌표가 됩니다. Model 행렬은 오브젝트 내부 기준의 좌표를 월드 기준으로 옮기고, View 행렬은 그 월드 좌표를 카메라 기준으로 다시 표현합니다. 마지막으로 Projection 행렬은 카메라가 보는 절두체를 클립 공간에서 다루기 쉬운 형태로 바꿉니다.

이 세 변환을 하나의 행렬 곱으로 묶어 표현한 것이 **MVP 행렬**입니다. 그래서 MVP를 적용한다는 말은 Model, View, Projection 변환을 한 번에 이어서 적용한다는 뜻입니다.

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

이 글처럼 정점 벡터를 식의 오른쪽에 두는 표기에서는, 변환이 오른쪽에서 왼쪽 순서로 적용됩니다. 그래서 실제 흐름은 $\mathbf{M}$(Model)이 먼저 정점을 월드 공간으로 옮기고, 그 결과에 $\mathbf{V}$(View)가 적용되어 뷰 공간 좌표가 되며, 마지막으로 $\mathbf{P}$(Projection)가 적용되어 클립 공간 좌표가 됩니다.

중요한 점은 행렬의 순서를 바꾸면 안 된다는 것입니다. $\mathbf{P} \times \mathbf{V} \times \mathbf{M}$과 $\mathbf{M} \times \mathbf{V} \times \mathbf{P}$는 전혀 다른 변환입니다. 다만 순서를 유지한 채 괄호를 어디에 묶을지는 바꿀 수 있습니다. 행렬 곱셈에는 결합 법칙이 성립하기 때문입니다.

$$
(\mathbf{A} \times \mathbf{B}) \times \mathbf{C} = \mathbf{A} \times (\mathbf{B} \times \mathbf{C})
$$

이 성질 덕분에 $\mathbf{P}$, $\mathbf{V}$, $\mathbf{M}$을 정점마다 따로 적용하지 않고, 먼저 하나의 행렬로 묶어 둘 수 있습니다.

<br>

**따로 적용하는 경우**:

$$\mathbf{v}_{world} = \mathbf{M} \times \mathbf{v}_{object}$$

$$\mathbf{v}_{view} = \mathbf{V} \times \mathbf{v}_{world}$$

$$\mathbf{v}_{clip} = \mathbf{P} \times \mathbf{v}_{view}$$

**MVP로 묶어 적용하는 경우**:

$$\mathbf{MVP} = \mathbf{P} \times \mathbf{V} \times \mathbf{M}$$

$$\mathbf{v}_{clip} = \mathbf{MVP} \times \mathbf{v}_{object}$$

두 방식은 정점을 같은 클립 공간 위치로 보냅니다. 차이는 계산을 언제 묶느냐에 있습니다. MVP 행렬을 미리 만들어 두면 각 정점마다 Model, View, Projection을 차례로 곱하지 않고, 이미 합쳐진 행렬 하나만 곱하면 됩니다. 오브젝트 하나에 정점이 많을수록 이런 사전 계산의 이점이 커집니다.

<br>

다만 셰이더에서 항상 MVP만 필요한 것은 아닙니다. MVP는 최종적으로 정점을 클립 공간에 놓기 위한 변환입니다. 조명 계산처럼 월드 공간의 위치나 뷰 공간의 방향이 필요한 경우에는, Model 행렬이나 View 행렬을 따로 사용해 그 공간의 값을 별도로 계산합니다.

---

### 버텍스 셰이더에서의 MVP

렌더링 파이프라인에서 버텍스 셰이더가 가장 먼저 맡는 일은 각 정점을 클립 공간으로 보내는 것입니다. [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 버텍스 셰이더가 정점 단위로 실행되며 위치를 변환한다고 설명한 부분이 바로 이 단계입니다.

수학적으로는 이 단계가 오브젝트 공간 정점에 Model, View, Projection 행렬을 차례로 적용하는 과정입니다. URP 셰이더 코드에서는 같은 변환을 직접 행렬 곱으로 풀어 쓰지 않고, Unity가 제공하는 `TransformObjectToHClip()`로 표현합니다.

```hlsl
OUT.positionCS = TransformObjectToHClip(IN.positionOS.xyz);
```

`TransformObjectToHClip()`은 오브젝트 공간 정점 위치를 받아 클립 공간 좌표를 반환합니다. 이 반환값이 버텍스 셰이더에서 `SV_POSITION`으로 넘기는 위치입니다.

수식으로 쓰면 입력 정점 $\mathbf{v}_{object} = (x,\; y,\; z,\; 1)$이 다음 과정을 거쳐 클립 공간 좌표 $\mathbf{v}_{clip} = (x',\; y',\; z',\; w')$가 됩니다.

$$
\mathbf{v}_{clip}
= \underbrace{\mathbf{P}}_{\text{Projection}}
\times
\underbrace{\mathbf{V}}_{\text{View}}
\times
\underbrace{\mathbf{M}}_{\text{Model}}
\times
\mathbf{v}_{object}
$$

이 식을 URP 헬퍼 함수 기준으로 보면, `TransformObjectToHClip()`은 오브젝트 공간 좌표를 월드 공간으로 변환한 뒤, 카메라의 View-Projection 변환을 적용해 클립 공간 좌표를 만듭니다. 결과는 위의 `P × V × M × v_object`와 같지만, 셰이더 코드에서는 행렬을 직접 조합하지 않고 URP가 제공하는 변환 함수를 호출하는 형태가 됩니다.

따라서 버텍스 셰이더에서 필요한 값이 최종 정점 위치뿐이라면, `SV_POSITION`으로 선언된 출력에 `TransformObjectToHClip()`의 결과를 대입하면 됩니다. 반대로 조명 계산이나 뷰 방향 계산처럼 월드 공간 위치, 뷰 공간 위치, 클립 공간 위치를 함께 써야 한다면 `GetVertexPositionInputs()`를 사용할 수 있습니다.

```hlsl
VertexPositionInputs positions = GetVertexPositionInputs(IN.positionOS.xyz);
OUT.positionCS = positions.positionCS;
```

`GetVertexPositionInputs()`는 같은 입력 정점에서 여러 공간의 위치를 계산해 `VertexPositionInputs` 구조체로 돌려줍니다. 이 중 `positionCS`가 클립 공간 좌표이며, 최종적으로 `SV_POSITION`에 연결되는 값입니다.

URP의 변환 헬퍼를 사용하면 오브젝트별 Model 행렬, 카메라의 View-Projection 행렬, GPU 인스턴싱이나 스테레오 렌더링 같은 렌더링 경로의 차이를 직접 맞출 필요가 줄어듭니다. 버텍스 셰이더가 `SV_POSITION`으로 선언된 출력에 클립 공간 좌표를 넣으면, GPU는 그 값을 사용해 프리미티브를 클립 공간에서 클리핑합니다. 이후 원근 나눗셈과 뷰포트 변환을 거쳐 화면 공간 위치가 정해집니다.

---

### 전체 변환 과정 정리

마지막으로 정점 좌표가 화면 공간까지 변환되는 흐름을 하나의 예시로 정리합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 660" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <text x="350" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">정점 좌표 변환의 전체 흐름 (예시)</text>
  <rect x="40" y="38" width="180" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 오브젝트 공간</text>
  <text x="130" y="80" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">(0, 1.8, 0, 1)</text>
  <text x="130" y="98" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">모델 안의 머리 쪽 정점</text>
  <text x="240" y="68" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">← Model 행렬 적용</text>
  <text x="240" y="86" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">Transform: position=(10, 0, 5)</text>
  <text x="240" y="100" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">rotation=none, scale=1</text>
  <line x1="130" y1="106" x2="130" y2="128" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="130,132 126,124 134,124" fill="currentColor"/>
  <rect x="40" y="132" width="180" height="68" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="154" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. 월드 공간</text>
  <text x="130" y="174" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">(10, 1.8, 5, 1)</text>
  <text x="130" y="192" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">씬 안의 머리 쪽 위치</text>
  <text x="240" y="162" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">← View 행렬 적용</text>
  <text x="240" y="180" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">카메라: 위치=(10, 2, 0)</text>
  <text x="240" y="194" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">+Z 방향을 바라봄</text>
  <line x1="130" y1="200" x2="130" y2="222" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="130,226 126,218 134,218" fill="currentColor"/>
  <rect x="40" y="226" width="180" height="68" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="248" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 뷰 공간</text>
  <text x="130" y="268" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">(0, -0.2, -5, 1)</text>
  <text x="130" y="286" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">카메라 기준 — 정면으로 5만큼 앞, 약간 아래</text>
  <text x="240" y="256" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">← Projection 행렬 적용</text>
  <text x="240" y="274" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">FOV=60°, aspect=16:9</text>
  <text x="240" y="288" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">near=0.3, far=1000</text>
  <line x1="130" y1="294" x2="130" y2="316" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="130,320 126,312 134,312" fill="currentColor"/>
  <rect x="40" y="320" width="180" height="68" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="342" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4. 클립 공간</text>
  <text x="130" y="362" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">(0, -0.35, 4.40, 5)</text>
  <text x="130" y="380" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">w에 뷰 공간 깊이 5가 들어감</text>
  <text x="240" y="358" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">← 원근 나눗셈 (÷w)</text>
  <line x1="130" y1="388" x2="130" y2="410" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="130,414 126,406 134,406" fill="currentColor"/>
  <rect x="40" y="414" width="180" height="68" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="436" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">5. NDC</text>
  <text x="130" y="456" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">(0, -0.07, 0.88)</text>
  <text x="130" y="474" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">화면 중앙에서 약간 아래 / 깊이 0.88</text>
  <text x="240" y="452" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">← 뷰포트 변환</text>
  <text x="240" y="470" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">해상도: 1920×1080</text>
  <line x1="130" y1="482" x2="130" y2="504" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="130,508 126,500 134,500" fill="currentColor"/>
  <rect x="40" y="508" width="180" height="68" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.4"/>
  <text x="130" y="530" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">6. 화면 공간</text>
  <text x="130" y="550" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">(960, 502)</text>
  <text x="130" y="568" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">화면 중앙에서 약간 아래의 픽셀</text>
  <text x="350" y="624" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">셰이더: 1~4단계(MVP) · GPU 자동: 5~6단계</text>
</svg>
</div>

이 흐름에서 버텍스 셰이더가 계산하는 마지막 위치는 클립 공간 좌표입니다. 이 좌표는 버텍스 셰이더 출력 중 `SV_POSITION`으로 선언된 값에 대입되며, 이후 클리핑, 원근 나눗셈, 뷰포트 변환은 셰이더 코드가 아니라 그래픽스 파이프라인의 후속 단계에서 처리됩니다.

---

## 마무리

이번 글에서는 메쉬에 저장된 오브젝트 공간 정점이 화면의 픽셀 위치로 이어지기까지, 렌더링 파이프라인이 좌표의 기준을 어떻게 바꾸는지 살펴봤습니다. 앞 글에서 다룬 4x4 행렬과 동차 좌표는 여기서 Model, View, Projection 행렬로 이어지며, 각각 오브젝트 배치, 카메라 기준 재표현, 클립 공간 변환을 담당합니다.

- **오브젝트 공간**의 정점 좌표는 메쉬 안에서의 위치입니다. 오브젝트를 씬의 어디에 배치하든 메쉬에 저장된 정점 값은 그대로이며, 이 좌표만으로는 화면에서 어디에 보일지 알 수 없습니다.
- **Model 행렬**은 오브젝트의 Transform을 반영해 오브젝트 공간 좌표를 월드 공간 좌표로 바꿉니다. 같은 메쉬를 공유하더라도 오브젝트마다 Model 행렬이 다르면 월드 공간의 위치는 달라집니다.
- **View 행렬**은 월드 공간을 카메라 기준으로 다시 표현합니다. Unity의 카메라 Transform과 렌더링용 View 공간은 같은 개념이 아니며, View 행렬은 월드 좌표를 투영 단계에서 사용할 카메라 기준 좌표로 변환합니다.
- **Projection 행렬**은 카메라가 보는 절두체를 클립 공간의 동차 좌표로 바꿉니다. 클립 공간은 화면 픽셀 좌표가 아니라, 보이는 범위를 판정하고 이후 원근 나눗셈을 수행하기 위한 중간 공간입니다.
- **클리핑**은 클립 공간 좌표를 기준으로 이루어집니다. 정점이 Projection 행렬을 거쳐 클립 공간 좌표가 되었다고 해서 이미 클리핑이 끝난 것은 아니며, GPU는 이 좌표를 사용해 프리미티브의 보이는 부분만 남깁니다.
- **원근 나눗셈**은 클립 공간 좌표의 x, y, z를 `w`로 나누어 NDC로 만드는 단계입니다. 이 과정에서 원근 투영의 거리감이 반영되고, 좌표 범위가 화면에 매핑하기 쉬운 정규화된 범위로 정리됩니다.
- **뷰포트 변환**은 NDC를 렌더 타깃 안의 픽셀 기준 화면 공간 좌표로 바꿉니다. 원근 나눗셈과 뷰포트 변환은 버텍스 셰이더에 직접 작성하는 코드가 아니라, 그래픽스 파이프라인의 후속 단계에서 처리됩니다.
- **MVP 변환**은 Model, View, Projection을 순서대로 적용해 오브젝트 공간 정점을 클립 공간 좌표로 보내는 과정입니다. URP 셰이더에서는 보통 `P × V × M`을 직접 작성하지 않고 `TransformObjectToHClip()`이나 `GetVertexPositionInputs()` 같은 헬퍼 함수로 이 변환을 표현합니다.

Projection 행렬의 내부 원리인 원근 투영과 직교 투영의 행렬 구성, 깊이 값의 비선형성, 그리고 이로 인한 Z-fighting 문제와 해결 방법은 [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)에서 이어집니다.

---

**관련 글**
- [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)

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
