---
layout: single
title: "Unity 렌더 파이프라인 (3) - 컬링과 오클루전 - soo:bak"
date: "2026-02-15 16:34:00 +0900"
description: Frustum Culling, Occlusion Culling, 레이어별 컬링, LOD 시스템, 텍스처 아틀라스를 설명합니다.
tags:
  - Unity
  - 최적화
  - 컬링
  - LOD
  - 모바일
---

## 보이지 않는 것은 그리지 않는다

[Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)에서는 배칭을 통해 CPU가 GPU에 렌더링 명령을 제출하는 비용을 줄이는 방법을 살펴보았습니다. Static Batching으로 드로우콜을 합치거나, SRP Batcher로 렌더 스테이트 전환을 줄이면 CPU 부담이 감소합니다.

하지만 배칭이 아무리 효율적이어도, 화면에 보이지 않는 오브젝트까지 GPU에 제출하면 결과가 폐기될 작업에 CPU와 GPU 모두 시간을 소비합니다. 가장 빠른 드로우콜은 아예 호출하지 않는 드로우콜입니다.

**컬링(Culling)**은 불필요한 드로우콜을 없애기 위해, GPU에 제출하기 전에 화면에 보이지 않는 오브젝트를 걸러내는 과정입니다.

<br>

씬에 오브젝트가 1,000개 있더라도 CPU에서 컬링을 거치면 카메라에 보이는 100개만 GPU에 제출되고, 나머지 900개는 렌더링 자체가 생략됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 씬의 전체 오브젝트 -->
  <text fill="currentColor" x="160" y="20" font-size="12" font-family="sans-serif" font-weight="bold">씬의 전체 오브젝트 (1,000개)</text>
  <!-- 화살표 1 -->
  <line x1="160" y1="30" x2="160" y2="55" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="160,58 156,52 164,52" fill="currentColor"/>
  <!-- 컬링 박스 -->
  <rect x="90" y="62" width="140" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="160" y="84" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">컬링</text>
  <text fill="currentColor" x="160" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(Culling)</text>
  <!-- 주석: 보이지 않는 오브젝트 제거 -->
  <text fill="currentColor" x="245" y="90" font-size="10" font-family="sans-serif" opacity="0.5">← 보이지 않는 오브젝트 제거</text>
  <!-- 화살표 2 -->
  <line x1="160" y1="112" x2="160" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="160,143 156,137 164,137" fill="currentColor"/>
  <!-- 렌더링 대상 -->
  <text fill="currentColor" x="160" y="165" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold">렌더링 대상 (100개)</text>
  <!-- 화살표 3 -->
  <line x1="160" y1="175" x2="160" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="160,203 156,197 164,197" fill="currentColor"/>
  <!-- 배칭 박스 -->
  <rect x="90" y="207" width="140" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="160" y="229" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">배칭</text>
  <text fill="currentColor" x="160" y="245" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(Batching)</text>
  <!-- 주석: 드로우콜/상태 변경 줄이기 -->
  <text fill="currentColor" x="245" y="235" font-size="10" font-family="sans-serif" opacity="0.5">← 드로우콜/상태 변경 줄이기</text>
  <!-- 화살표 4 -->
  <line x1="160" y1="257" x2="160" y2="285" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="160,288 156,282 164,282" fill="currentColor"/>
  <!-- GPU 렌더링 박스 -->
  <rect x="90" y="292" width="140" height="45" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="160" y="319" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">GPU 렌더링</text>
</svg>
</div>

<br>

컬링이 **무엇을** 렌더링할지 결정하면, 배칭은 그 결과를 받아 드로우콜을 효율적으로 묶어 GPU에 제출합니다.
Unity에서는 Frustum Culling, Occlusion Culling, 레이어별 컬링 거리로 렌더링 대상을 줄이고, LOD와 텍스처 아틀라스로 남은 오브젝트의 렌더링 비용을 낮춥니다.

---

## Frustum Culling

**Frustum Culling**은 카메라의 시야 영역 밖에 있는 오브젝트를 렌더링 대상에서 제외하는 기법입니다. Unity는 별도의 설정 없이 매 프레임 자동으로 수행합니다.

이 시야 영역을 **뷰 프러스텀(View Frustum)**이라고 합니다. **시야각(Field of View)**이 각도 범위를 결정하고, **가까운 클리핑 평면(Near Clip Plane)**과 **먼 클리핑 평면(Far Clip Plane)**이 렌더링 거리의 앞뒤 한계를 정합니다. Unity의 기본값은 Near가 0.3, Far가 1,000 단위입니다.

이 세 값이 만들어내는 공간은 잘린 사각뿔 형태이며, 프러스텀 안에 들어오는 오브젝트만 카메라에 보입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 뷰 프러스텀: 3D 잘린 사각뿔 (의사 투영) -->
  <!-- 카메라(왼쪽)에서 오른쪽으로 뻗어나가는 절두체 -->
  <!-- 좌표: C(55,200), Near면 x≈135, Far면 x≈420-470 -->

  <!-- 1. 면 채우기 (스트로크 없이, 뒤에서부터) -->
  <!-- 왼쪽 면 (시점에서 보이는 측면) -->
  <polygon points="135,165 420,48 420,352 135,235" fill="currentColor" fill-opacity="0.03"/>
  <!-- 윗면 -->
  <polygon points="135,165 147,159 470,20 420,48" fill="currentColor" fill-opacity="0.05"/>
  <!-- 먼 면 (Far Clip Plane) -->
  <polygon points="420,48 470,20 470,324 420,352" fill="currentColor" fill-opacity="0.04"/>
  <!-- 가까운 면 (Near Clip Plane) -->
  <polygon points="135,165 147,159 147,229 135,235" fill="currentColor" fill-opacity="0.10"/>

  <!-- 2. 숨겨진 모서리 (점선) -->
  <!-- 아래-뒤쪽 Near 모서리 -->
  <line x1="135" y1="235" x2="147" y2="229" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 아래-오른쪽 절두체 모서리 -->
  <line x1="147" y1="229" x2="470" y2="324" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- 3. 보이는 모서리 (실선) -->
  <!-- 왼쪽 면 4변 -->
  <line x1="135" y1="165" x2="420" y2="48" stroke="currentColor" stroke-width="1.2"/>
  <line x1="135" y1="235" x2="420" y2="352" stroke="currentColor" stroke-width="1.2"/>
  <line x1="135" y1="165" x2="135" y2="235" stroke="currentColor" stroke-width="1.2"/>
  <line x1="420" y1="48" x2="420" y2="352" stroke="currentColor" stroke-width="1.2"/>
  <!-- 윗면 추가 모서리 -->
  <line x1="135" y1="165" x2="147" y2="159" stroke="currentColor" stroke-width="1.2"/>
  <line x1="420" y1="48" x2="470" y2="20" stroke="currentColor" stroke-width="1.2"/>
  <line x1="147" y1="159" x2="470" y2="20" stroke="currentColor" stroke-width="1.2"/>
  <!-- 먼 면 추가 모서리 -->
  <line x1="470" y1="20" x2="470" y2="324" stroke="currentColor" stroke-width="1.2"/>
  <line x1="420" y1="352" x2="470" y2="324" stroke="currentColor" stroke-width="1.2"/>
  <!-- 가까운 면 오른쪽 모서리 (뒤쪽이므로 점선) -->
  <line x1="147" y1="159" x2="147" y2="229" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- 4. 카메라 → Near 면 점선 (사각뿔 꼭짓점 표현) -->
  <line x1="55" y1="200" x2="135" y2="165" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3" opacity="0.4"/>
  <line x1="55" y1="200" x2="135" y2="235" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3" opacity="0.4"/>
  <line x1="55" y1="200" x2="147" y2="159" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,4" opacity="0.2"/>
  <line x1="55" y1="200" x2="147" y2="229" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,4" opacity="0.2"/>

  <!-- 5. FOV 각도 표시 -->
  <path d="M 82,188 A 30,30 0 0,1 82,212" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>
  <text fill="currentColor" x="96" y="204" font-size="10" font-family="sans-serif" font-weight="bold" opacity="0.6">FOV</text>

  <!-- 6. 카메라 아이콘 -->
  <rect x="33" y="189" width="22" height="22" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="55" cy="200" r="3" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="44" y="228" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">카메라</text>

  <!-- 7. 레이블 -->
  <!-- Near Clip Plane -->
  <text fill="currentColor" x="118" y="256" font-size="10" font-family="sans-serif" opacity="0.6">Near Clip</text>
  <text fill="currentColor" x="118" y="268" font-size="10" font-family="sans-serif" opacity="0.6">Plane</text>
  <!-- Far Clip Plane -->
  <text fill="currentColor" x="448" y="355" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">Far Clip Plane</text>
  <!-- 프러스텀 내부 레이블 -->
  <text fill="currentColor" x="290" y="185" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">뷰 프러스텀</text>
  <text fill="currentColor" x="290" y="203" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(View Frustum)</text>
  <text fill="currentColor" x="290" y="222" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.4">잘린 사각뿔 형태의 3D 공간</text>

  <!-- 8. 거리 축 -->
  <line x1="44" y1="385" x2="445" y2="385" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="44" y1="380" x2="44" y2="390" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="141" y1="380" x2="141" y2="390" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="445" y1="380" x2="445" y2="390" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <text fill="currentColor" x="44" y="402" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">0</text>
  <text fill="currentColor" x="141" y="402" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">Near</text>
  <text fill="currentColor" x="445" y="402" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">Far</text>
</svg>
</div>

<br>

### 바운딩 볼륨과 교차 검사

오브젝트가 프러스텀 안에 있는지 판단하려면 메쉬와 프러스텀을 비교해야 합니다.
메쉬의 삼각형 하나하나를 프러스텀의 6개 평면과 비교하면 연산이 많아, 씬의 모든 오브젝트에 매 프레임 적용하기는 어렵습니다. 
대부분의 엔진은 삼각형 단위 비교 대신, 오브젝트를 감싸는 단순한 도형이 프러스텀과 겹치는지만 검사합니다.

Unity가 이 교차 검사에 사용하는 도형은 **AABB(Axis-Aligned Bounding Box)**, 오브젝트를 감싸는 가장 작은 직육면체입니다.
Axis-Aligned(축 정렬)라는 이름대로 각 변이 항상 월드 좌표축(x, y, z)에 평행합니다. 방향이 고정되어 있으므로, 각 축에서 오브젝트가 차지하는 범위(예: x 2~5, y 1~4, z 3~7)만으로 직육면체의 위치와 크기가 모두 정해집니다.

이 범위를 프러스텀의 6개 평면과 비교하면 교차 여부를 바로 판단할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- y축 -->
  <line x1="80" y1="260" x2="80" y2="30" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="80,27 76,35 84,35" fill="currentColor"/>
  <text fill="currentColor" x="70" y="30" font-size="12" font-family="sans-serif" font-style="italic">y</text>
  <!-- x축 -->
  <line x1="80" y1="260" x2="370" y2="260" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="373,260 365,256 365,264" fill="currentColor"/>
  <text fill="currentColor" x="375" y="265" font-size="12" font-family="sans-serif" font-style="italic">x</text>
  <!-- z축 (대각선 아래-왼쪽) -->
  <line x1="80" y1="260" x2="30" y2="300" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="27,302 36,298 32,293" fill="currentColor"/>
  <text fill="currentColor" x="20" y="312" font-size="12" font-family="sans-serif" font-style="italic">z</text>
  <!-- AABB 직육면체 (등각 투영) -->
  <!-- 앞면 -->
  <rect x="130" y="100" width="160" height="130" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 윗면 -->
  <polygon points="130,100 175,65 335,65 290,100" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 옆면 -->
  <polygon points="290,100 335,65 335,195 290,230" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 내부 텍스트 -->
  <text fill="currentColor" x="210" y="160" text-anchor="middle" font-size="12" font-family="sans-serif">오브젝트</text>
  <text fill="currentColor" x="210" y="178" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(메쉬)</text>
  <!-- 꼭짓점 좌표 -->
  <text fill="currentColor" x="100" y="248" font-size="10" font-family="sans-serif" font-weight="bold">(2, 1, 3)</text>
  <text fill="currentColor" x="300" y="58" font-size="10" font-family="sans-serif" font-weight="bold">(5, 4, 7)</text>
  <!-- 범위 정보 -->
  <text fill="currentColor" x="210" y="290" text-anchor="middle" font-size="11" font-family="sans-serif">AABB 범위: x = 2~5, y = 1~4, z = 3~7</text>
  <text fill="currentColor" x="210" y="310" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">각 변이 좌표축에 평행 → 여섯 개의 숫자로 형태 결정</text>
</svg>
</div>

<br>

AABB가 6개 평면(상, 하, 좌, 우, Near, Far) 중 하나라도 완전히 바깥에 있으면 프러스텀 외부로 판정합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Far 레이블 -->
  <text fill="currentColor" x="250" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">Far</text>
  <!-- 프러스텀 사다리꼴 -->
  <polygon points="60,30 440,30 330,230 170,230" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- Near 레이블 -->
  <text fill="currentColor" x="250" y="250" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">Near</text>
  <!-- A: 프러스텀 안 -->
  <rect x="140" y="70" width="50" height="40" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="165" y="95" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">A</text>
  <!-- B: 경계 걸침 -->
  <rect x="280" y="190" width="60" height="55" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text fill="currentColor" x="310" y="222" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">B</text>
  <!-- C: 프러스텀 밖 -->
  <rect x="410" y="195" width="50" height="40" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="435" y="220" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">C</text>
  <!-- 카메라 -->
  <line x1="250" y1="290" x2="250" y2="265" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="250,262 246,268 254,268" fill="currentColor"/>
  <text fill="currentColor" x="250" y="305" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">카메라</text>
  <!-- 범례 -->
  <rect x="50" y="320" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="70" y="332" font-size="10" font-family="sans-serif">A: 프러스텀 안에 포함 → 렌더링</text>
  <rect x="50" y="340" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text fill="currentColor" x="70" y="352" font-size="10" font-family="sans-serif">B: 경계에 걸침 → 렌더링 (보수적 판정)</text>
  <rect x="295" y="320" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="315" y="332" font-size="10" font-family="sans-serif">C: 프러스텀 밖 → 제거</text>
</svg>
</div>

<br>

AABB가 프러스텀 경계에 걸치는 경우(B)에는 보수적으로 렌더링 대상에 포함합니다. 실제로는 메쉬의 일부만 보일 수 있지만, AABB 단위로는 이를 정확히 구분할 수 없기 때문입니다.

<br>

### Frustum Culling의 비용과 효과

AABB와 평면의 교차 검사는 오브젝트 하나당 6개 평면과의 비교 연산만 수행합니다. 오브젝트 1,000개를 검사해도 CPU에서 수십 마이크로초(µs) 수준에 끝나면서, 프러스텀 밖의 오브젝트 전부를 렌더링에서 제외할 수 있습니다.

특히, 카메라가 씬의 일부만 바라보는 일반적인 상황에서 Frustum Culling은 렌더링 대상을 크게 줄여줍니다. 넓은 오픈 월드에서 카메라가 한 방향을 바라보면, 뒤쪽과 좌우 먼 곳의 오브젝트가 모두 제거됩니다.

하지만 프러스텀 안에 있더라도 건물이나 벽에 가려져 보이지 않는 경우까지는 걸러내지 못합니다. 이 부분을 담당하는 것이 Occlusion Culling입니다.

---

## Occlusion Culling

**Occlusion Culling**은 프러스텀 안에 있지만 다른 물체에 완전히 가려진(occluded) 오브젝트를 렌더링 대상에서 제외하는 기법입니다. 건물 뒤의 가구, 벽 뒤의 방, 산 뒤편의 마을처럼 화면에 나타나지 않는 오브젝트가 대상입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- 카메라 -->
  <text fill="currentColor" x="150" y="20" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">카메라</text>
  <!-- 화살표: 카메라 → 건물 -->
  <line x1="150" y1="28" x2="150" y2="50" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="150,53 146,47 154,47" fill="currentColor"/>
  <!-- 건물 (Occluder) -->
  <rect x="70" y="57" width="160" height="55" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="150" y="82" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">건물 (벽)</text>
  <text fill="currentColor" x="150" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">Occluder</text>
  <!-- 주석 -->
  <text fill="currentColor" x="245" y="88" font-size="10" font-family="sans-serif" opacity="0.5">← 가리는 오브젝트</text>
  <!-- 가려진 영역 표시 -->
  <line x1="150" y1="112" x2="150" y2="150" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text fill="currentColor" x="185" y="136" font-size="9" font-family="sans-serif" opacity="0.5">가려진 영역</text>
  <polygon points="150,153 146,147 154,147" fill="currentColor"/>
  <!-- 가구 (Occludee) -->
  <rect x="70" y="157" width="160" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text fill="currentColor" x="150" y="182" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">가구 (테이블)</text>
  <text fill="currentColor" x="150" y="200" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">Occludee</text>
  <!-- 주석 -->
  <text fill="currentColor" x="245" y="178" font-size="10" font-family="sans-serif" opacity="0.5">← 가려진 오브젝트</text>
  <text fill="currentColor" x="245" y="194" font-size="9" font-family="sans-serif" opacity="0.5">Frustum 안에 있지만 보이지 않음</text>
  <text fill="currentColor" x="245" y="208" font-size="9" font-family="sans-serif" opacity="0.5">→ Occlusion Culling으로 제거</text>
</svg>
</div>

### Unity의 Occlusion Culling: 베이크 방식

가려짐 여부는 카메라 위치와 오브젝트들 사이의 앞뒤 관계에 따라 달라지므로, 매 프레임 계산하면 비용이 커질 수 있습니다.

Unity는 이 부담을 런타임에서 빌드 타임으로 옮기는 **베이크(Bake) 방식**을 사용합니다.
에디터에서 미리 씬을 분석하여 각 위치에서 어떤 오브젝트가 보이는지를 계산해 두고, 런타임에는 이 결과를 조회만 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 570 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 570px; width: 100%;">
  <!-- 단계 1: 3D 셀 분할 -->
  <text fill="currentColor" x="90" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">1. 씬을 3D 셀(Cell)로 분할</text>

  <!-- 3D 복셀 그리드: 전면 4×4, 셀 27px, 깊이 3층, 오프셋 (10,-7)/층 -->
  <!-- 숨겨진 모서리 (점선) -->
  <line x1="50" y1="38" x2="50" y2="146" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.25"/>
  <line x1="50" y1="146" x2="158" y2="146" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.25"/>
  <line x1="20" y1="167" x2="50" y2="146" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.25"/>

  <!-- 전면 (4×4 그리드) -->
  <rect x="20" y="59" width="108" height="108" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.2"/>
  <line x1="47" y1="59" x2="47" y2="167" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="74" y1="59" x2="74" y2="167" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="101" y1="59" x2="101" y2="167" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="20" y1="86" x2="128" y2="86" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="20" y1="113" x2="128" y2="113" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="20" y1="140" x2="128" y2="140" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>

  <!-- 하이라이트 셀 C11, C12, C21 -->
  <rect x="47" y="86" width="27" height="27" fill="currentColor" fill-opacity="0.10"/>
  <rect x="74" y="86" width="27" height="27" fill="currentColor" fill-opacity="0.10"/>
  <rect x="47" y="113" width="27" height="27" fill="currentColor" fill-opacity="0.10"/>

  <!-- 윗면 (평행사변형) -->
  <polygon points="20,59 128,59 158,38 50,38" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <line x1="30" y1="52" x2="138" y2="52" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="40" y1="45" x2="148" y2="45" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="47" y1="59" x2="77" y2="38" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="74" y1="59" x2="104" y2="38" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="101" y1="59" x2="131" y2="38" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>

  <!-- 오른쪽면 (평행사변형) -->
  <polygon points="128,59 158,38 158,146 128,167" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <line x1="138" y1="52" x2="138" y2="160" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="148" y1="45" x2="148" y2="153" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="128" y1="86" x2="158" y2="65" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="128" y1="113" x2="158" y2="92" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="128" y1="140" x2="158" y2="119" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>

  <!-- 셀 레이블 (전면) -->
  <text fill="currentColor" x="33" y="76" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C00</text>
  <text fill="currentColor" x="60" y="76" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C01</text>
  <text fill="currentColor" x="87" y="76" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C02</text>
  <text fill="currentColor" x="114" y="76" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C03</text>
  <text fill="currentColor" x="33" y="103" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C10</text>
  <text fill="currentColor" x="60" y="103" text-anchor="middle" font-size="7" font-family="sans-serif" font-weight="bold">C11</text>
  <text fill="currentColor" x="87" y="103" text-anchor="middle" font-size="7" font-family="sans-serif" font-weight="bold">C12</text>
  <text fill="currentColor" x="114" y="103" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C13</text>
  <text fill="currentColor" x="33" y="130" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C20</text>
  <text fill="currentColor" x="60" y="130" text-anchor="middle" font-size="7" font-family="sans-serif" font-weight="bold">C21</text>
  <text fill="currentColor" x="87" y="130" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C22</text>
  <text fill="currentColor" x="114" y="130" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C23</text>
  <text fill="currentColor" x="33" y="157" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C30</text>
  <text fill="currentColor" x="60" y="157" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C31</text>
  <text fill="currentColor" x="87" y="157" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C32</text>
  <text fill="currentColor" x="114" y="157" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.4">C33</text>

  <!-- 축 표시 -->
  <g opacity="0.5">
    <line x1="15" y1="185" x2="38" y2="185" stroke="currentColor" stroke-width="1"/>
    <text fill="currentColor" x="41" y="188" font-size="8" font-family="sans-serif" font-style="italic">x</text>
    <line x1="15" y1="185" x2="15" y2="168" stroke="currentColor" stroke-width="1"/>
    <text fill="currentColor" x="11" y="165" font-size="8" font-family="sans-serif" font-style="italic">y</text>
    <line x1="15" y1="185" x2="27" y2="177" stroke="currentColor" stroke-width="1"/>
    <text fill="currentColor" x="30" y="175" font-size="8" font-family="sans-serif" font-style="italic">z</text>
  </g>

  <!-- 화살표: 그리드 → 가시 목록 -->
  <line x1="170" y1="113" x2="210" y2="113" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="213,113 207,109 207,117" fill="currentColor"/>

  <!-- 단계 2: 가시 목록 -->
  <text fill="currentColor" x="393" y="16" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">2. 각 셀에서 보이는 오브젝트 목록</text>
  <rect x="220" y="30" width="340" height="102" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="237" y="57" font-size="10" font-family="sans-serif" font-weight="bold">C11</text>
  <text fill="currentColor" x="280" y="57" font-size="10" font-family="sans-serif">→ {건물A, 나무B, 도로C, ...}</text>
  <text fill="currentColor" x="237" y="82" font-size="10" font-family="sans-serif" font-weight="bold">C12</text>
  <text fill="currentColor" x="280" y="82" font-size="10" font-family="sans-serif">→ {건물A, 울타리D, ...}</text>
  <text fill="currentColor" x="237" y="107" font-size="10" font-family="sans-serif" font-weight="bold">C21</text>
  <text fill="currentColor" x="280" y="107" font-size="10" font-family="sans-serif">→ {나무B, 도로C, 건물E, ...}</text>

  <!-- 화살표: 가시 목록 → 저장 -->
  <line x1="390" y1="132" x2="390" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="390,161 386,155 394,155" fill="currentColor"/>

  <!-- 단계 3: 저장 -->
  <rect x="305" y="166" width="170" height="35" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="390" y="188" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">3. 바이너리 데이터로 저장</text>
</svg>
</div>

<br>

베이크를 실행하면 Unity는 씬 공간을 3D 격자(Cell)로 나누고, 건물이나 벽 같은 정적 오브젝트(Occluder)의 메쉬를 단순한 블록(복셀)으로 변환합니다. 그런 뒤 각 셀에서 블록에 완전히 막혀 도달할 수 없는 오브젝트를 제외하고, 나머지를 해당 셀의 가시 목록으로 저장합니다.

### 런타임 동작

런타임에는 카메라의 현재 위치가 어느 셀에 해당하는지를 찾고, 그 셀의 가시 목록을 조회합니다. 가시 목록에 없는 오브젝트는 렌더링 대상에서 제외됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 카메라 위치 → 셀 -->
  <rect x="90" y="10" width="240" height="35" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="210" y="33" text-anchor="middle" font-size="12" font-family="sans-serif">카메라 위치 → <tspan font-weight="bold">셀 C11</tspan>에 해당</text>
  <!-- 화살표 -->
  <line x1="210" y1="45" x2="210" y2="72" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,75 206,69 214,69" fill="currentColor"/>
  <!-- 가시 목록 조회 -->
  <rect x="70" y="79" width="280" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="210" y="100" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C11의 가시 목록 조회</text>
  <text fill="currentColor" x="210" y="120" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">{건물A, 나무B, 도로C}</text>
  <!-- 화살표 -->
  <line x1="210" y1="129" x2="210" y2="156" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,159 206,153 214,153" fill="currentColor"/>
  <!-- 렌더링 제외 -->
  <rect x="55" y="163" width="310" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="210" y="184" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">가시 목록에 없는 오브젝트 → 렌더링 제외</text>
  <text fill="currentColor" x="210" y="204" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(건물E, 울타리D, 가구F 등)</text>
</svg>
</div>

<br>

이 조회는 씬 로드 시 RAM에 올라온 베이크 데이터에서 셀을 찾고 가시 목록을 참조하는 것이므로, 런타임에 가시성을 새로 계산하는 것에 비해 부담이 작습니다.

### 베이크 방식의 제약

베이크 방식은 런타임 비용을 줄이지만, 베이크 시간, Occluder의 정적 제한, 메모리 사용이라는 제약이 따릅니다.

씬이 크고 복잡할수록 **베이크 시간**이 길어집니다. 셀 수와 오브젝트 수가 많을수록 각 셀에서의 가시성 계산량이 증가하며, 대규모 씬에서는 수십 분 이상 소요되기도 합니다.

**Occluder는 정적 오브젝트로 제한됩니다.** Occluder의 위치와 형태가 베이크 데이터에 기록되어 있으므로, 런타임에 위치가 바뀌는 동적 오브젝트(캐릭터, 이동하는 플랫폼 등)는 Occluder가 될 수 없습니다.
다만 동적 오브젝트라도 **Occludee**(가려지는 역할)로는 등록할 수 있습니다. Occluder가 고정되어 있는 만큼, 동적 오브젝트가 그 뒤에 있는지는 런타임에 판단할 수 있기 때문입니다.

베이크된 가시성 데이터는 씬과 함께 저장되고, 런타임에 **메모리**에 로드됩니다. 셀이 세밀할수록, 오브젝트가 많을수록 데이터 크기가 커집니다. 모바일처럼 가용 메모리가 제한된 환경에서는 셀 크기를 지나치게 줄이지 않도록 주의해야 합니다.

<br>

### 씬 구조에 따른 Occlusion Culling 효과

Occlusion Culling의 효과는 씬에서 시야를 차단하는 구조물이 얼마나 있느냐에 따라 달라집니다.
건물 내부에서는 벽 뒤 다른 방이, 도시에서는 건물 뒤편이 가려져 렌더링 대상이 크게 줄어듭니다.
반면, 평원이나 사막처럼 탁 트인 환경에서는 오브젝트 대부분이 실제로 보이므로 제거할 대상이 적습니다.

---

## 레이어별 컬링 거리

Frustum Culling과 Occlusion Culling을 거쳐도, 풀 한 포기, 작은 돌, 파티클 이펙트 같은 오브젝트가 카메라에서 200m 떨어져 있으면 화면에서 한두 픽셀 크기로 나타나, 시각적 효과는 거의 없지만 렌더링 비용은 그대로 발생합니다.

**레이어별 컬링 거리(Per-Layer Culling Distance)**는 오브젝트 종류마다 컬링 거리를 두어, 그 밖의 오브젝트를 렌더링에서 제외하는 방식입니다.
Unity에서는 오브젝트를 레이어로 분류한 뒤, `Camera.layerCullDistances`로 레이어마다 컬링 거리를 지정할 수 있습니다. 풀 레이어에 30m, 소품 레이어에 80m를 설정하면 해당 거리 밖의 풀과 소품이 렌더링에서 제외됩니다.

### 컬링 거리 측정 방식

컬링 거리를 지정하지 않은 레이어는 카메라의 Far Clip Plane을 그대로 사용합니다.

기본적으로 컬링 거리는 카메라 전방 축(z축)에 대한 **투영 거리**로 측정됩니다.
투영 거리란 오브젝트가 카메라 전방 축을 따라 얼마나 앞에 있는지를 나타내는 값으로, 옆이나 위아래 방향의 거리는 포함되지 않습니다. 카메라 정면의 오브젝트는 거의 전방에만 떨어져 있으므로 직선 거리와 투영 거리가 거의 같습니다. 화면 가장자리에 보이는 오브젝트는 카메라에서 옆으로 치우쳐 있으므로, 같은 직선 거리라도 투영 거리는 짧아집니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 400 215" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px; width: 100%;">
  <!-- 전방 축 -->
  <line x1="40" y1="170" x2="350" y2="170" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.25"/>
  <text fill="currentColor" x="355" y="173" font-size="8" font-family="sans-serif" opacity="0.4" font-style="italic">전방 축</text>

  <!-- 카메라 -->
  <polygon points="40,170 25,160 25,180" fill="currentColor" opacity="0.8"/>
  <text fill="currentColor" x="25" y="197" font-size="9" font-family="sans-serif" text-anchor="middle">카메라</text>

  <!-- 컬링 거리 경계 -->
  <line x1="160" y1="25" x2="160" y2="182" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.5"/>
  <text fill="currentColor" x="160" y="207" text-anchor="middle" font-size="9" font-weight="bold" font-family="sans-serif">컬링 거리 80m</text>

  <!-- A: 정면 오브젝트 (축 위, 컬링 경계 밖) -->
  <line x1="40" y1="170" x2="190" y2="170" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>
  <circle cx="190" cy="170" r="4" fill="currentColor"/>
  <text fill="currentColor" x="198" y="167" font-size="9" font-family="sans-serif" font-weight="bold">A (정면)</text>
  <text fill="currentColor" x="115" y="163" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">투영 100m ≈ 직선 100m</text>
  <text fill="currentColor" x="198" y="180" font-size="8" font-family="sans-serif" opacity="0.5">80m 초과 → 제거</text>

  <!-- B: 가장자리 오브젝트 (축에서 벗어남, 투영이 컬링 경계 안) -->
  <line x1="40" y1="170" x2="138" y2="56" stroke="currentColor" stroke-width="1.2" opacity="0.6"/>
  <circle cx="138" cy="56" r="4" fill="currentColor"/>
  <text fill="currentColor" x="146" y="53" font-size="9" font-family="sans-serif" font-weight="bold">B (가장자리)</text>
  <text fill="currentColor" x="75" y="100" font-size="8" font-family="sans-serif" opacity="0.6">직선 100m</text>

  <!-- B의 투영 (수직 점선) -->
  <line x1="138" y1="56" x2="138" y2="170" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.35"/>

  <!-- B 투영 거리 표시 -->
  <line x1="40" y1="177" x2="138" y2="177" stroke="currentColor" stroke-width="2.5" opacity="0.5"/>
  <text fill="currentColor" x="89" y="190" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.6">투영 ≈ 65m</text>

  <!-- B 결과 -->
  <text fill="currentColor" x="138" y="42" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">80m 이내 → 렌더링</text>
</svg>
</div>

<br>

이 때문에 카메라를 회전하면 같은 오브젝트의 투영 거리가 달라집니다. 직선 거리 100m인 오브젝트가 화면 중앙에 있을 때는 투영 거리도 약 100m이지만, 카메라를 회전하여 화면 가장자리로 밀려나면 투영 거리가 줄어듭니다. 컬링 거리가 80m라면, 중앙에서는 80m를 넘어 제거되지만 가장자리에서는 80m 안에 들어와 다시 나타납니다. 카메라 회전만으로 오브젝트가 갑자기 나타나거나 사라질 수 있습니다.

투영 거리 대신 카메라로부터의 직선 거리(반경)로 컬링하면 이 문제가 사라집니다. 직선 거리는 카메라 회전에 영향받지 않으므로 오브젝트의 컬링 여부가 안정적으로 유지됩니다. Unity에서는 `Camera.layerCullSpherical`을 true로 설정하여 이 방식을 사용할 수 있습니다.

<br>

### 효과와 주의점

레이어 하나에 거리를 지정하면 해당 레이어의 오브젝트 전체에 적용되므로, 풀·돌·파티클처럼 개수가 많은 오브젝트도 한 번의 설정으로 처리할 수 있습니다.

다만 컬링 거리가 짧을수록, 플레이어가 이동할 때 오브젝트가 갑자기 나타나는 **팝인(Pop-in)**이 눈에 띕니다.

---

## LOD 시스템 실전

컬링은 보이지 않는 오브젝트를 제거하지만, 화면에 보이는 오브젝트는 그대로 렌더링해야 합니다.
**LOD(Level of Detail)**는 카메라에서 먼 오브젝트의 메쉬를 단순한 버전으로 교체하여 정점 수를 줄이는 방식입니다. 기본 개념은 [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 다루었습니다.

### LOD 단계 전환

Unity에서 LOD는 **LODGroup** 컴포넌트로 동작합니다. 하나의 LODGroup 안에 여러 단계(LOD 0, LOD 1, LOD 2, ...)가 있고, 각 단계에 서로 다른 복잡도의 메쉬가 들어갑니다. LOD 0이 가장 정밀한 원본 메쉬이고, 숫자가 올라갈수록 삼각형 수가 줄어듭니다.

단계 전환의 기준은 카메라와의 절대 거리가 아니라 **화면 점유 비율(Screen Relative Height)**입니다.
오브젝트의 바운딩 볼륨이 화면 높이에서 차지하는 비율이 줄어들면 다음 단계로 전환됩니다. 큰 건물은 100m 떨어져도 화면 비율이 높아 LOD 0을 유지하지만, 작은 돌은 20m만 떨어져도 비율이 낮아 LOD 2로 전환됩니다.

### LOD 전환과 Cross Fade

LOD 단계가 바뀔 때 메쉬가 순간적으로 교체되면, 삼각형 수 차이로 인해 실루엣이 급변하는 **팝핑(Popping)** 현상이 발생합니다. 이를 완화하기 위해 Unity의 LODGroup은 **Fade Mode** 설정을 제공합니다.

**None**은 전환 시점에서 메쉬를 즉시 교체합니다. 추가 비용이 없지만, 팝핑이 발생합니다.

**Cross Fade**는 전환 시점 전후로 이전 LOD와 다음 LOD를 동시에 렌더링하면서 투명도를 전환합니다. 이전 LOD가 점점 투명해지고 다음 LOD가 점점 불투명해지므로 전환 자체는 부드럽습니다. 하지만 전환 구간에서는 두 단계의 메쉬가 같은 픽셀을 모두 기록하므로 **오버드로우(Overdraw)**가 발생하여 렌더링 비용이 일시적으로 증가합니다.

**SpeedTree**는 나무와 식생 모델 생성 미들웨어인 SpeedTree 에셋 전용 모드입니다. Cross Fade와 유사하게 전환 구간에서 블렌딩을 수행하지만, 나뭇잎이나 가지처럼 복잡한 실루엣의 식생에 맞게 조정된 방식을 사용합니다.

<br>

### 디더링 기반 Cross Fade

**디더링(Dithering) 기반 Cross Fade**는 두 LOD를 투명도로 섞는 대신, 픽셀 위치를 체크무늬처럼 나누어 한 픽셀에 한쪽 LOD만 그리는 방식입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 일반 Cross Fade -->
  <text fill="currentColor" x="130" y="18" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">일반 Cross Fade</text>
  <text fill="currentColor" x="130" y="34" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(투명도 블렌딩)</text>
  <!-- LOD 0: 전체 픽셀, 반투명 -->
  <text fill="currentColor" x="25" y="62" font-size="10" font-family="sans-serif" font-weight="bold">LOD 0</text>
  <g transform="translate(65, 46)">
    <rect x="0" y="0" width="130" height="18" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="0.5"/>
    <text fill="currentColor" x="140" y="14" font-size="9" font-family="sans-serif" opacity="0.5">50% 투명</text>
  </g>
  <!-- LOD 1: 전체 픽셀, 반투명 -->
  <text fill="currentColor" x="25" y="88" font-size="10" font-family="sans-serif" font-weight="bold">LOD 1</text>
  <g transform="translate(65, 72)">
    <rect x="0" y="0" width="130" height="18" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="0.5"/>
    <text fill="currentColor" x="140" y="14" font-size="9" font-family="sans-serif" opacity="0.5">50% 투명</text>
  </g>
  <text fill="currentColor" x="130" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">→ 모든 픽셀을 두 번 기록</text>
  <!-- 구분선 -->
  <line x1="260" y1="15" x2="260" y2="200" stroke="currentColor" stroke-width="0.8" opacity="0.2"/>
  <!-- 디더링 Cross Fade -->
  <text fill="currentColor" x="390" y="18" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">디더링 Cross Fade</text>
  <text fill="currentColor" x="390" y="34" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(체크무늬 패턴)</text>
  <!-- LOD 0: 체크무늬 절반 -->
  <text fill="currentColor" x="290" y="62" font-size="10" font-family="sans-serif" font-weight="bold">LOD 0</text>
  <g transform="translate(325, 46)">
    <rect x="0" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="26" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="52" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="78" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="104" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="0" y="0" width="130" height="18" fill="none" stroke="currentColor" stroke-width="0.5"/>
  </g>
  <!-- LOD 1: 나머지 절반 -->
  <text fill="currentColor" x="290" y="88" font-size="10" font-family="sans-serif" font-weight="bold">LOD 1</text>
  <g transform="translate(325, 72)">
    <rect x="13" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="39" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="65" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="91" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="117" y="0" width="13" height="18" fill="currentColor" fill-opacity="0.20"/>
    <rect x="0" y="0" width="130" height="18" fill="none" stroke="currentColor" stroke-width="0.5"/>
  </g>
  <text fill="currentColor" x="390" y="110" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">→ 각 픽셀을 한 번만 기록</text>
</svg>
</div>

<br>

전환이 진행될수록 이전 LOD가 담당하는 픽셀은 줄어들고 다음 LOD의 픽셀은 늘어납니다. 각 픽셀이 한 번만 기록되므로, 일반 Cross Fade의 오버드로우가 발생하지 않습니다.

다만 픽셀 기록과 셰이더 연산은 다릅니다. GPU는 양쪽 LOD의 프래그먼트 셰이더를 모든 픽셀에 대해 실행한 뒤, 디더링 패턴에 해당하지 않는 결과를 `clip()`으로 버립니다. 버리는 시점이 셰이더 실행 이후이므로 연산은 이미 수행된 상태이고, 드로우콜도 양쪽 LOD 각각 발생합니다. 디더링이 줄이는 것은 오버드로우(픽셀 기록 횟수)이지, 셰이더 연산이나 드로우콜이 아닙니다.

전환 구간에서는 디더링 패턴이 미세하게 보일 수 있고, 모바일처럼 해상도가 낮은 환경에서는 더 드러납니다. 하지만 모바일 GPU는 프레임버퍼에 기록할 수 있는 픽셀 수(**필레이트, Fill Rate**)가 제한적이어서 오버드로우의 비용이 크므로, 패턴이 보이더라도 디더링 방식이 유리한 경우가 많습니다.

### 모바일에서의 LOD 설계

모바일에서는 GPU 성능과 메모리가 제한적입니다. LOD 단계가 많으면 그만큼 메쉬 에셋이 늘어나 메모리 사용량이 커지고, 화면에서 충분히 작아질 때까지 고폴리곤 메쉬를 유지하도록 설정하면 GPU에 부담이 됩니다.

그래서 단계 수는 적게, 전환은 일찍 일어나도록 보수적으로 설정합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 화면 점유 비율 레이블 -->
  <text fill="currentColor" x="30" y="16" font-size="10" font-family="sans-serif" opacity="0.5">화면 점유 비율</text>
  <text fill="currentColor" x="30" y="35" font-size="9" font-family="sans-serif" opacity="0.5">100%</text>
  <text fill="currentColor" x="160" y="35" font-size="9" font-family="sans-serif" opacity="0.5">25%</text>
  <text fill="currentColor" x="275" y="35" font-size="9" font-family="sans-serif" opacity="0.5">10%</text>
  <text fill="currentColor" x="385" y="35" font-size="9" font-family="sans-serif" opacity="0.5">3%</text>
  <text fill="currentColor" x="485" y="35" font-size="9" font-family="sans-serif" opacity="0.5">0%</text>
  <!-- LOD 구간 바 -->
  <rect x="30" y="42" width="140" height="45" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <rect x="170" y="42" width="115" height="45" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <rect x="285" y="42" width="105" height="45" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.5"/>
  <rect x="390" y="42" width="100" height="45" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5"/>
  <!-- LOD 레이블 -->
  <text fill="currentColor" x="100" y="60" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">LOD 0</text>
  <text fill="currentColor" x="100" y="77" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">삼각형 100%</text>
  <text fill="currentColor" x="228" y="60" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">LOD 1</text>
  <text fill="currentColor" x="228" y="77" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">삼각형 40%</text>
  <text fill="currentColor" x="338" y="60" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">LOD 2</text>
  <text fill="currentColor" x="338" y="77" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">삼각형 15%</text>
  <text fill="currentColor" x="440" y="60" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Culled</text>
  <text fill="currentColor" x="440" y="77" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">삼각형 0%</text>
  <!-- 방향 화살표 -->
  <text fill="currentColor" x="30" y="108" font-size="10" font-family="sans-serif">가까움</text>
  <line x1="75" y1="104" x2="455" y2="104" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="458,104 452,100 452,108" fill="currentColor"/>
  <text fill="currentColor" x="465" y="108" font-size="10" font-family="sans-serif">멀어짐</text>
  <!-- 주석 -->
  <text fill="currentColor" x="260" y="140" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">괄호 안의 값은 LOD 0 대비 삼각형 수 비율</text>
</svg>
</div>

<br>

LOD 단계 사이의 삼각형 감소율이 클수록 정점 처리 비용 절약이 크지만, 전환 시 실루엣 차이가 커져 팝핑이 눈에 띄기 쉽습니다. 위 다이어그램에서 LOD 1의 삼각형 수는 LOD 0의 40%이므로, 정점 처리 비용은 60% 줄어들면서도 실루엣 변화는 비교적 완만합니다.

마지막 Culled 단계는 오브젝트를 아예 렌더링하지 않는 단계입니다. 화면에서 3% 미만을 차지하는 오브젝트는 대부분 눈에 띄지 않으므로 제거해도 시각적 차이가 작습니다. 다만, 랜드마크 건물이나 주요 지형처럼 멀리서도 존재감이 필요한 오브젝트는 Culled 대신 LOD 2를 유지하는 편이 자연스럽습니다.

---

## 텍스처 아틀라스

컬링과 LOD는 렌더링 대상의 수와 복잡도를 줄이는 방식이지만, 텍스처 아틀라스는 접근이 다릅니다. 여러 텍스처를 하나의 큰 텍스처에 합쳐, 오브젝트를 그릴 때마다 발생하는 **텍스처 바인딩 변경(GPU 상태 전환)**을 줄입니다.

[Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)에서 다루었듯이 GPU는 상태 머신이고, 텍스처 교체는 비용이 큰 상태 전환 중 하나입니다. 나무, 풀, 돌, 울타리가 각각 다른 텍스처를 쓰면 오브젝트를 바꿀 때마다 텍스처를 교체해야 하지만, 하나의 아틀라스를 공유하면 텍스처가 바인딩된 상태 그대로 여러 오브젝트를 그릴 수 있습니다.

나아가 같은 텍스처를 사용하면 머티리얼 통일도 가능해집니다. Static Batching은 같은 머티리얼을 사용하는 오브젝트끼리만 배칭할 수 있는데, 아틀라스 덕분에 머티리얼이 달랐던 오브젝트들이 배칭 대상이 됩니다. 정적 오브젝트라면 Static Batching으로 메쉬를 합쳐 드로우콜을 줄일 수 있습니다.

### UV 좌표 조정

**UV 좌표**는 메쉬의 정점이 텍스처의 어느 위치를 가리키는지 나타내는 2D 좌표입니다. 개별 텍스처에서는 UV가 (0, 0)에서 (1, 1)까지 텍스처 전체를 가리키지만, 아틀라스에서는 해당 오브젝트의 텍스처가 차지하는 영역만 가리키도록 조정됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 개별 텍스처 -->
  <text fill="currentColor" x="100" y="18" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">개별 텍스처</text>
  <text fill="currentColor" x="100" y="34" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">UV (0,0)~(1,1) → 전체 참조</text>
  <rect x="20" y="44" width="70" height="70" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="55" y="83" text-anchor="middle" font-size="10" font-family="sans-serif">나무</text>
  <rect x="100" y="44" width="70" height="70" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="135" y="83" text-anchor="middle" font-size="10" font-family="sans-serif">풀</text>
  <rect x="20" y="124" width="70" height="70" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="55" y="163" text-anchor="middle" font-size="10" font-family="sans-serif">돌</text>
  <rect x="100" y="124" width="70" height="70" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="135" y="163" text-anchor="middle" font-size="10" font-family="sans-serif">울타리</text>
  <!-- 화살표 -->
  <text fill="currentColor" x="210" y="120" font-size="18" font-family="sans-serif" opacity="0.4">→</text>
  <!-- 아틀라스 -->
  <text fill="currentColor" x="380" y="18" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">아틀라스 (1장)</text>
  <text fill="currentColor" x="380" y="34" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">UV 범위가 영역별로 나뉨</text>
  <!-- 아틀라스 격자 -->
  <rect x="260" y="44" width="240" height="180" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="380" y1="44" x2="380" y2="224" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3"/>
  <line x1="260" y1="134" x2="500" y2="134" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3"/>
  <!-- 아틀라스 셀 배경 -->
  <rect x="261" y="45" width="118" height="88" fill="currentColor" fill-opacity="0.06"/>
  <rect x="381" y="45" width="118" height="88" fill="currentColor" fill-opacity="0.03"/>
  <rect x="261" y="135" width="118" height="88" fill="currentColor" fill-opacity="0.03"/>
  <rect x="381" y="135" width="118" height="88" fill="currentColor" fill-opacity="0.06"/>
  <!-- 셀 텍스트 -->
  <text fill="currentColor" x="320" y="93" text-anchor="middle" font-size="11" font-family="sans-serif">나무</text>
  <text fill="currentColor" x="440" y="93" text-anchor="middle" font-size="11" font-family="sans-serif">풀</text>
  <text fill="currentColor" x="320" y="183" text-anchor="middle" font-size="11" font-family="sans-serif">돌</text>
  <text fill="currentColor" x="440" y="183" text-anchor="middle" font-size="11" font-family="sans-serif">울타리</text>
  <!-- UV 좌표 표기 -->
  <text fill="currentColor" x="320" y="108" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.5">(0, 0.5)~(0.5, 1.0)</text>
  <text fill="currentColor" x="440" y="108" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.5">(0.5, 0.5)~(1.0, 1.0)</text>
  <text fill="currentColor" x="320" y="198" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.5">(0, 0)~(0.5, 0.5)</text>
  <text fill="currentColor" x="440" y="198" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.5">(0.5, 0)~(1.0, 0.5)</text>
  <!-- 축 좌표 -->
  <text fill="currentColor" x="256" y="230" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.4">(0,0)</text>
  <text fill="currentColor" x="380" y="230" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.4">(0.5,0)</text>
  <text fill="currentColor" x="504" y="230" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.4">(1,0)</text>
  <text fill="currentColor" x="248" y="138" text-anchor="end" font-size="8" font-family="monospace" opacity="0.4">(0,0.5)</text>
  <text fill="currentColor" x="248" y="50" text-anchor="end" font-size="8" font-family="monospace" opacity="0.4">(0,1)</text>
</svg>
</div>

<br>

나무 오브젝트의 UV를 (0, 0)~(1, 1)에서 (0, 0.5)~(0.5, 1.0)으로 변환하면, 아틀라스에서 나무 텍스처가 위치한 왼쪽 위 영역만 참조하게 됩니다. 실제로는 아틀라스 생성 도구나 모델링 도구가 텍스처 배치와 UV 변환을 처리하므로, 좌표를 직접 계산할 일은 거의 없습니다.

### 2D와 3D에서의 아틀라스

**2D(Sprite Atlas):** Unity는 여러 스프라이트를 하나의 아틀라스로 합치는 Sprite Atlas 기능을 제공합니다. UI 아이콘, 2D 캐릭터 스프라이트, 타일맵 등을 지정하면 빌드 시 아틀라스가 자동 생성되고 UV도 함께 조정됩니다.

**3D(Texture Atlas):** 3D 메쉬는 오브젝트 표면을 감싸는 복잡한 UV 레이아웃을 가지고 있어, 아틀라스에 맞게 UV를 재배치하는 작업이 필요합니다. Unity에는 이를 자동으로 처리하는 기능이 없으므로, 3D 모델링 도구(Blender, Maya 등)에서 텍스처를 합치고 UV를 조정합니다. 씬에서 자주 함께 등장하는 오브젝트를 같은 아틀라스로 묶으면 효과적입니다.

<br>

### 아틀라스의 크기와 제약

모바일에서는 아틀라스 크기로 1024x1024 또는 2048x2048이 일반적이며, 4096x4096도 가능하지만 메모리 부담이 큽니다. 2048x2048 아틀라스에 256x256 텍스처를 넣으면 최대 64개(8×8)가 들어갑니다.

텍스처 사이에는 **패딩(Padding)**을 두어, 샘플링 시 인접 텍스처의 색상이 경계를 넘어 번지는 **블리딩(Bleeding)**을 방지합니다. 패딩만큼 실제 넣을 수 있는 텍스처 수는 줄어듭니다.

GPU는 텍스처를 통째로 메모리에 로드하므로, 아틀라스 안의 텍스처 중 일부만 사용되더라도 전체 아틀라스가 메모리에 올라갑니다. 아틀라스가 크고 사용하지 않는 영역이 많으면 그만큼 메모리가 낭비됩니다.

---

## 최적화 기법 비교

지금까지 다룬 기법들은 렌더링 비용을 서로 다른 방식으로 줄입니다.

| 기법 | 역할 | 동작 시점 | 추가 비용 |
|------|------|-----------|-----------|
| Frustum Culling | 프러스텀 밖 오브젝트 제거 | 매 프레임 자동 | 거의 없음 |
| Occlusion Culling | 가려진 오브젝트 제거 | 오프라인 베이크 + 런타임 조회 | 베이크 시간, 메모리 |
| 레이어별 컬링 거리 | 레이어별로 먼 오브젝트 제거 | 매 프레임 자동 | 거의 없음 |
| LOD | 화면 비율에 따라 메쉬 단순화 | 매 프레임 자동 | LOD 메쉬 에셋 |
| 텍스처 아틀라스 | 텍스처 바인딩 변경 감소, 머티리얼 통일 | 사전 준비 | UV 조정, 아틀라스 메모리 |

이 기법들은 서로 배타적이지 않으며 함께 적용됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 런타임 파이프라인 라벨 -->
  <text fill="currentColor" x="30" y="14" font-size="9" font-family="sans-serif" opacity="0.4">런타임 (매 프레임)</text>
  <!-- 시작: 씬 전체 -->
  <text fill="currentColor" x="170" y="38" font-size="12" font-weight="bold" font-family="sans-serif">씬의 전체 오브젝트 (1,000개)</text>
  <!-- 화살표 -->
  <line x1="170" y1="46" x2="170" y2="66" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="170,69 166,63 174,63" fill="currentColor"/>
  <!-- Frustum Culling -->
  <rect x="60" y="73" width="220" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="170" y="97" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Frustum Culling</text>
  <text fill="currentColor" x="295" y="90" font-size="10" font-family="sans-serif" opacity="0.5">프러스텀 밖 700개 제거</text>
  <text fill="currentColor" x="295" y="105" font-size="10" font-family="sans-serif" font-weight="bold">→ 남은 300개</text>
  <!-- 화살표 -->
  <line x1="170" y1="111" x2="170" y2="131" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="170,134 166,128 174,128" fill="currentColor"/>
  <!-- Occlusion Culling -->
  <rect x="60" y="138" width="220" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="170" y="162" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Occlusion Culling</text>
  <text fill="currentColor" x="295" y="155" font-size="10" font-family="sans-serif" opacity="0.5">가려진 100개 제거</text>
  <text fill="currentColor" x="295" y="170" font-size="10" font-family="sans-serif" font-weight="bold">→ 남은 200개</text>
  <!-- 화살표 -->
  <line x1="170" y1="176" x2="170" y2="196" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="170,199 166,193 174,193" fill="currentColor"/>
  <!-- 레이어별 컬링 거리 -->
  <rect x="60" y="203" width="220" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="170" y="227" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">레이어별 컬링 거리</text>
  <text fill="currentColor" x="295" y="220" font-size="10" font-family="sans-serif" opacity="0.5">먼 거리 50개 제거</text>
  <text fill="currentColor" x="295" y="235" font-size="10" font-family="sans-serif" font-weight="bold">→ 남은 150개</text>
  <!-- 화살표 -->
  <line x1="170" y1="241" x2="170" y2="261" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="170,264 166,258 174,258" fill="currentColor"/>
  <!-- LOD -->
  <rect x="60" y="268" width="220" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="170" y="292" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">LOD</text>
  <text fill="currentColor" x="295" y="285" font-size="10" font-family="sans-serif" opacity="0.5">삼각형 수 감소 + Culled 30개</text>
  <text fill="currentColor" x="295" y="300" font-size="10" font-family="sans-serif" font-weight="bold">→ 남은 120개</text>
  <!-- 화살표 -->
  <line x1="170" y1="306" x2="170" y2="340" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="170,343 166,337 174,337" fill="currentColor"/>
  <!-- GPU 제출 -->
  <rect x="60" y="347" width="220" height="38" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="170" y="371" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">GPU에 제출 (120개)</text>
  <!-- 텍스처 아틀라스: 파이프라인 밖, 오른쪽에 별도 표시 -->
  <rect x="340" y="347" width="170" height="38" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text fill="currentColor" x="425" y="363" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">텍스처 아틀라스</text>
  <text fill="currentColor" x="425" y="378" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(사전 준비) 상태 전환 감소</text>
  <!-- 아틀라스에서 GPU 제출로 화살표 -->
  <line x1="340" y1="366" x2="285" y2="366" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <polygon points="282,366 288,362 288,370" fill="currentColor" opacity="0.5"/>
  <!-- 사전 준비 라벨 -->
  <text fill="currentColor" x="340" y="340" font-size="9" font-family="sans-serif" opacity="0.4">사전 준비 (에셋 단계)</text>
</svg>
</div>

---

## 마무리

- Frustum Culling은 카메라의 프러스텀 밖에 있는 오브젝트를 GPU에 제출하지 않으며, Unity가 매 프레임 자동으로 수행합니다.
- Occlusion Culling은 에디터에서 정적 Occluder의 가시성을 베이크한 뒤, 런타임에 Occludee가 가려져 있는지를 테이블 조회로 판정합니다.
- Per-Layer Culling Distance는 레이어별로 컬링 거리를 다르게 설정하여, 멀리 있는 작은 오브젝트를 먼저 제거합니다.
- LOD는 화면 점유 비율에 따라 메쉬의 폴리곤 수를 단계적으로 줄여 GPU 부하를 낮춥니다.
- 텍스처 아틀라스는 여러 텍스처를 하나로 합쳐 텍스처 바인딩 변경을 줄이고, 머티리얼 통일을 통해 Static Batching 조건을 만듭니다.

각 기법은 파이프라인의 서로 다른 지점에서 비용을 줄이며, 프로젝트의 씬 구조와 타겟 기기에 맞게 조합하여 적용합니다.

<br>

UnityPipeline 시리즈에서는 렌더 파이프라인의 구조(Part 1), 드로우콜과 배칭(Part 2), 컬링과 LOD(Part 3)를 통해 GPU 쪽 렌더링 비용을 줄이는 방법을 살펴보았습니다.

GPU 쪽 비용이 정리되면, 다음 병목은 매 프레임 실행되는 C# 스크립트, Unity API 호출, 가비지 컬렉션 같은 CPU 쪽에서 발생합니다. [스크립트 최적화](/dev/unity/ScriptOptimization-1/) 시리즈에서 이 CPU 비용을 줄이는 방법을 다룹니다.

---

**관련 글**
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)
- **Unity 렌더 파이프라인 (3) - 컬링과 오클루전** (현재 글)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)
- **Unity 렌더 파이프라인 (3) - 컬링과 오클루전** (현재 글)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
