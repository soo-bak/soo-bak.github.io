---
layout: single
title: "파티클과 애니메이션 (1) - 파티클 시스템 최적화 - soo:bak"
date: "2026-02-19 22:54:00 +0900"
description: 파티클 비용 구조, 파티클 오버드로우, 파티클 수 예산, Prewarm, GPU Instancing을 설명합니다.
tags:
  - Unity
  - 최적화
  - 파티클
  - 이펙트
---

## 물리에서 파티클로

[물리 최적화](/dev/unity/PhysicsOptimization-1/) 시리즈에서는 PhysX 기반 물리 시스템의 비용을 줄이는 방법을 다뤘습니다. 이번 시리즈에서는 시각적 품질을 만드는 서브시스템을 다루며, 이 글에서는 그중 **파티클 시스템(Particle System)**을 살펴봅니다.

파티클 시스템은 연기, 불꽃, 폭발, 먼지, 빗방울, 마법 이펙트처럼 게임에서 흔히 보는 시각 효과를 만들어냅니다. 작은 입자(파티클) 수백에서 수천 개를 생성한 뒤, 각각의 위치, 속도, 크기, 색상, 수명을 매 프레임 갱신하며 화면에 그려냅니다.

이 과정은 CPU와 GPU 양쪽에서 비용을 만듭니다. CPU는 시뮬레이션을, GPU는 렌더링을 담당합니다.

성능 예산이 제한된 환경일수록 이 비용은 프레임 예산에 민감하게 영향을 미칩니다.
파티클 하나의 비용은 작지만, 수백 개가 동시에 활성화되면 CPU 시뮬레이션과 GPU 렌더링 양쪽에서 프레임 예산을 압박합니다.

이 글에서는 파티클 시스템의 비용 구조를 CPU 시뮬레이션과 GPU 렌더링으로 나누어 분석하고, 프래그먼트 셰이더 예산이 제한된 환경에서 특히 큰 비용을 차지하는 오버드로우의 원인을 파악합니다.
이어서 파티클 수 예산, Prewarm 스파이크 회피, Culling Mode 설정, GPU Instancing 적용까지 각 비용을 줄이는 방법을 하나씩 다룹니다.

---

## 파티클 비용 구조

파티클 시스템의 비용은 CPU의 **시뮬레이션 비용**과 GPU의 **렌더링 비용**으로 나뉩니다. 두 영역은 부하의 성격이 달라 따로 살펴볼 필요가 있습니다.

### CPU 비용: 파티클 시뮬레이션

CPU는 매 프레임 활성화된 파티클마다 다음 연산을 수행합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 580" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="24" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">파티클 시뮬레이션 (CPU, 매 프레임)</text>
  <text x="270" y="46" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" fill-opacity="0.7">활성 파티클 하나에 대한 처리</text>

  <rect x="40" y="64" width="460" height="400" rx="8" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>

  <text x="60" y="88" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) 수명 갱신</text>
  <text x="80" y="108" font-family="monospace" font-size="10.5" fill="currentColor">경과 시간 += deltaTime</text>
  <text x="80" y="125" font-family="monospace" font-size="10.5" fill="currentColor">경과 시간 &gt; 수명이면 제거</text>

  <line x1="60" y1="140" x2="480" y2="140" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="158" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) 위치 갱신</text>
  <text x="80" y="178" font-family="monospace" font-size="10.5" fill="currentColor">위치 += 속도 × deltaTime</text>
  <text x="80" y="195" font-family="monospace" font-size="10.5" fill="currentColor">속도 += 가속도 × deltaTime</text>

  <line x1="60" y1="210" x2="480" y2="210" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="228" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) 크기 변화</text>
  <text x="80" y="248" font-family="monospace" font-size="10.5" fill="currentColor">크기 = 커브[경과 시간]</text>

  <line x1="60" y1="262" x2="480" y2="262" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="280" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(4) 색상/알파 변화</text>
  <text x="80" y="300" font-family="monospace" font-size="10.5" fill="currentColor">색상 = 그라디언트[경과 시간]</text>

  <line x1="60" y1="314" x2="480" y2="314" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="332" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(5) 회전</text>
  <text x="80" y="352" font-family="monospace" font-size="10.5" fill="currentColor">회전 += 회전 속도 × deltaTime</text>

  <line x1="60" y1="366" x2="480" y2="366" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="384" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(6) 추가 모듈</text>
  <text x="200" y="384" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.65">활성화된 경우</text>
  <text x="80" y="404" font-family="sans-serif" font-size="10.5" fill="currentColor">Noise · Collision · Force · SubEmitter</text>

  <line x1="270" y1="476" x2="270" y2="496" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="265,491 270,504 275,491" fill="currentColor"/>

  <rect x="70" y="512" width="400" height="56" rx="6" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="534" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레임당 CPU 비용</text>
  <text x="270" y="555" text-anchor="middle" font-family="monospace" font-size="11.5" fill="currentColor">= 파티클 수 × 위 6 단계 연산</text>
</svg>
</div>

<br>

파티클 수가 많아지면 이 연산이 거의 선형적으로 증가합니다. 파티클 100개에서 1,000개로 늘어나면 시뮬레이션 비용도 10배 가까이 커집니다. 여기에 Noise 모듈이나 Collision 모듈처럼 비용이 높은 모듈이 활성화되어 있으면, 파티클당 연산량이 더 커집니다.

예를 들어 Collision 모듈은 파티클마다 물리 월드와의 충돌을 검사합니다. 파티클 500개가 Collision 모듈을 사용하면, 매 프레임 500번의 레이캐스트(또는 유사한 검사)가 추가됩니다. 레이캐스트는 물리 엔진의 Broadphase와 Narrowphase를 거치는 연산이므로, 파티클 시뮬레이션 비용 위에 물리 비용이 중첩됩니다.

### GPU 비용: 파티클 렌더링

CPU 시뮬레이션을 거친 파티클은 이제 GPU에서 화면으로 그려집니다. Unity의 파티클 시스템은 기본적으로 각 파티클을 **빌보드(Billboard)**, 즉 카메라를 향해 회전하는 단순한 사각형 메쉬 형태로 만들어, 입체 형태 없이도 어느 시점에서나 일정한 모양을 유지하게 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="24" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">파티클 렌더링 (GPU)</text>
  <text x="270" y="46" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" fill-opacity="0.7">파티클 하나의 렌더링 과정</text>

  <rect x="40" y="64" width="460" height="248" rx="8" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>

  <text x="60" y="88" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) 빌보드 메쉬 생성</text>
  <text x="80" y="110" font-family="sans-serif" font-size="10.5" fill="currentColor">카메라를 향하는 사각형 (정점 4개, 삼각형 2개)</text>

  <line x1="60" y1="124" x2="480" y2="124" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="144" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) 버텍스 셰이더</text>
  <text x="80" y="166" font-family="sans-serif" font-size="10.5" fill="currentColor">사각형의 정점을 화면 좌표로 변환</text>

  <line x1="60" y1="180" x2="480" y2="180" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="200" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) 래스터화</text>
  <text x="80" y="222" font-family="sans-serif" font-size="10.5" fill="currentColor">사각형이 덮는 픽셀 영역 결정</text>

  <line x1="60" y1="236" x2="480" y2="236" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3"/>

  <text x="60" y="256" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(4) 프래그먼트 셰이더</text>
  <text x="80" y="278" font-family="sans-serif" font-size="10.5" fill="currentColor">텍스처 샘플링, 색상 계산, 알파 블렌딩</text>

  <line x1="270" y1="324" x2="270" y2="344" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="265,339 270,352 275,339" fill="currentColor"/>

  <rect x="70" y="360" width="400" height="56" rx="6" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="382" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU 비용의 핵심</text>
  <text x="270" y="403" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(4) 프래그먼트 셰이더가 비용의 대부분을 차지</text>
</svg>
</div>

<br>

파티클 하나의 메쉬는 정점 4개짜리 사각형이라 버텍스 처리 비용이 거의 들지 않습니다. 그 결과 GPU 비용은 **(4) 프래그먼트 셰이더 단계**에 집중되며, 파티클이 화면에서 차지하는 면적이 클수록, 또 파티클끼리 겹칠수록 셰이더 실행 횟수가 늘어납니다.

---

## 파티클 오버드로우: 프래그먼트 셰이더의 최대 비용

파티클 시스템에서 GPU 비용의 핵심은 **오버드로우(Overdraw)**입니다. 픽셀이 덮어 그려질 때마다 프래그먼트 셰이더가 한 번씩 실행되므로, 오버드로우 수치가 클수록 프래그먼트 셰이더 실행 횟수도 그만큼 늘어납니다. 특히 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 다뤘듯 타일 기반 GPU는 한 프레임에 처리할 수 있는 프래그먼트 셰이딩 양이 한정적이라, 오버드로우가 늘어날수록 이 한정된 용량이 더 빠르게 소모됩니다.

이런 부담은 파티클 이펙트에서 특히 두드러집니다. 파티클이 대부분 반투명으로 렌더링되어 겹침이 그대로 비용에 더해지고, 거기에 많은 수가 한곳에 몰리는 일도 흔하기 때문입니다.

### 반투명 렌더링

파티클 오버드로우가 커지는 첫 번째 이유는 반투명 렌더링입니다. 연기, 불꽃, 먼지처럼 배경과 섞여 보여야 하는 이펙트는 대개 **반투명(Alpha Blending)**으로 렌더링됩니다.

불투명 오브젝트는 렌더링될 때 자신의 깊이 값을 깊이 버퍼에 기록합니다. 이후 같은 픽셀에 더 뒤쪽의 프래그먼트가 들어오면 깊이 테스트에서 제외될 수 있으므로, 프래그먼트 셰이더 실행을 줄일 수 있습니다.

반투명 파티클은 보통 깊이 테스트는 수행하더라도 깊이 값은 기록하지 않습니다. 뒤의 배경이나 다른 파티클과 색을 섞어야 하기 때문입니다. 그래서 여러 반투명 파티클이 같은 픽셀에 겹치면, 앞에 그려진 파티클이 뒤의 파티클을 깊이 버퍼에서 막아 주지 못합니다. 각 파티클의 프래그먼트가 차례로 셰이딩되고 블렌딩되며, 겹친 수만큼 GPU 비용이 누적됩니다.

결국 반투명 파티클은 보통 깊이 값을 기록하지 않기 때문에, 파티클끼리 겹쳐도 깊이 버퍼로 서로를 차단하기 어렵습니다. 이 특성 때문에 겹쳐 그려지는 파티클의 오버드로우 비용이 그대로 누적됩니다.

### 공간적 밀집

파티클 오버드로우가 커지는 두 번째 이유는 파티클이 화면상 비슷한 위치에 모이기 쉽다는 점입니다. 폭발 이펙트는 중심부 근처에서 많은 파티클이 동시에 퍼지고, 연기나 먼지 이펙트도 비슷한 경로를 따라 이어지며 같은 화면 영역을 반복해서 덮습니다.
이런 밀집이 생기면 한 픽셀에 여러 파티클의 프래그먼트가 겹쳐 생성되고, 앞에서 설명한 반투명 렌더링 특성 때문에 그 비용이 그대로 누적됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">파티클 오버드로우: 불꽃 이펙트 (화면 중앙에 50개 파티클 겹침)</text>

  <text x="40" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">화면 영역</text>
  <rect x="40" y="62" width="280" height="240" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>

  <rect x="90" y="100" width="180" height="160" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="115" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">파티클 1</text>

  <rect x="115" y="130" width="130" height="115" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="145" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">파티클 2</text>

  <rect x="140" y="160" width="80" height="70" rx="3" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="175" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">파티클 3</text>

  <text x="180" y="200" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">...</text>

  <text x="360" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">겹치는 영역의 한 픽셀</text>
  <line x1="360" y1="64" x2="620" y2="64" stroke="currentColor" stroke-width="0.8"/>

  <text x="360" y="84" font-family="sans-serif" font-size="10" fill="currentColor">파티클 1 프래그먼트 셰이더 실행 (블렌딩)</text>
  <text x="360" y="104" font-family="sans-serif" font-size="10" fill="currentColor">파티클 2 프래그먼트 셰이더 실행 (블렌딩)</text>
  <text x="360" y="124" font-family="sans-serif" font-size="10" fill="currentColor">파티클 3 프래그먼트 셰이더 실행 (블렌딩)</text>
  <text x="360" y="144" font-family="sans-serif" font-size="10" fill="currentColor">...</text>
  <text x="360" y="164" font-family="sans-serif" font-size="10" fill="currentColor">파티클 50 프래그먼트 셰이더 실행 (블렌딩)</text>
  <line x1="360" y1="178" x2="620" y2="178" stroke="currentColor" stroke-width="0.8"/>

  <text x="360" y="206" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 이 픽셀은 50번 셰이딩됨</text>
  <text x="360" y="228" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 오버드로우 = 50×</text>
</svg>
</div>

<br>

파티클 오버드로우는 제한된 **필레이트(Fill Rate)** 예산을 빠르게 소모합니다. 예를 들어 파티클 이펙트가 화면 중앙의 200×200 픽셀 영역을 덮고, 그 영역에서 평균 오버드로우가 30×라면 해당 영역에서만 200 × 200 × 30 = 1,200,000번의 프래그먼트 셰이딩이 발생합니다. 같은 종류의 이펙트가 여러 개 겹치면 이 비용은 빠르게 늘어납니다.

따라서 오버드로우를 줄이려면 파티클 수뿐 아니라, 파티클이 화면에서 차지하는 면적과 같은 픽셀에 겹치는 횟수도 함께 줄여야 합니다.

### 오버드로우 줄이기

오버드로우를 줄이는 방향은 앞에서 본 비용 구조와 같습니다. 같은 픽셀에 겹치는 파티클 수를 줄이고, 각 파티클이 화면에서 차지하는 면적을 줄이며, 프래그먼트 셰이더 자체를 가볍게 만들어야 합니다.

가장 직접적인 방법은 파티클 수를 줄이는 것입니다. 같은 화면 영역에 겹치는 파티클이 줄어들면 해당 픽셀에서 실행되는 프래그먼트 셰이딩 횟수도 줄어듭니다. 수를 줄일 때는 파티클 개수로 만들던 세부 표현을 텍스처 안으로 옮기는 방식이 효과적입니다. 예를 들어 작은 연기 조각을 많이 뿌리기보다, 한 장의 텍스처에 농도 변화와 가장자리 흐림을 충분히 넣으면 더 적은 파티클로도 비슷한 시각적 밀도와 형태를 만들 수 있습니다.

파티클의 화면 크기도 중요합니다. 파티클 수가 같아도 각 파티클이 큰 빌보드로 그려지면 더 넓은 픽셀 영역을 덮고, 서로 겹치는 면적도 커집니다. 반대로 불필요하게 큰 파티클 크기를 줄이면 이펙트의 형태는 유지하면서도 같은 픽셀에 겹치는 프래그먼트 수를 낮출 수 있습니다.

마지막으로 파티클 셰이더를 단순하게 유지해야 합니다. 오버드로우가 큰 이펙트에서는 같은 픽셀에서 셰이더가 여러 번 실행되므로, 프래그먼트당 비용이 그대로 반복됩니다. 조명 계산이 필요 없는 이펙트는 Unlit 셰이더를 사용하고, 노멀 맵이나 불필요한 텍스처 샘플링을 줄이면 오버드로우가 큰 상황에서도 비용 증가 폭을 낮출 수 있습니다.

이 중에서 가장 먼저 관리할 항목은 파티클 수입니다. 파티클 수는 CPU 시뮬레이션 비용과 GPU 오버드로우에 동시에 영향을 주기 때문에, 프로젝트 단위의 예산으로 관리하는 편이 효과적입니다.

---

## 파티클 수 예산

파티클 수를 줄이려면 개별 이펙트만 보는 것으로는 부족합니다. 화면에는 여러 이펙트가 동시에 존재할 수 있고, 각 이펙트의 파티클 수가 적절해 보여도 합산하면 프레임 예산을 넘을 수 있습니다. 따라서 프로젝트에서는 한 화면에서 동시에 활성화될 수 있는 파티클 수의 상한을 정하고, 이 범위 안에서 이펙트별 배분을 관리해야 합니다.

이때 기준이 되는 전체 허용량이 **파티클 수 예산(Particle Budget)**이며, 각 이펙트의 `Max Particles`, Emission Rate, Lifetime은 이 범위 안에서 조정합니다.

### 예산을 정할 때의 기준

파티클 수 예산은 하나의 고정된 숫자로 정하기 어렵습니다. 같은 수의 파티클이라도 화면 해상도, 파티클 크기, 반투명 비율, 셰이더 복잡도, 다른 렌더링 부하에 따라 실제 비용이 달라집니다. 예를 들어 작은 불꽃 파티클이 많이 흩어진 장면보다, 큰 연기 파티클이 화면을 넓게 덮는 장면이 더 무거울 수 있습니다.

이 때문에 예산은 목표 기기와 목표 프레임률만으로 확정하기보다, 실제 장면에서 비용을 확인하며 조정하는 편이 적절합니다. 먼저 대략적인 초기값을 잡고, 평상시 장면이 아니라 전투, 폭발, 환경 효과처럼 파티클이 가장 많이 겹치는 상황을 기준으로 확인합니다.

이런 확인은 Unity Profiler에서 진행합니다. 파티클 시뮬레이션에 걸리는 CPU 시간과 렌더링 비용을 측정하고, 화면 전체의 동시 활성 파티클 수·이펙트 하나의 파티클 수·동시에 재생되는 이펙트 수를 함께 보면 비용이 어디에서 늘어나는지 파악하기 쉽습니다.

예산의 기준은 “파티클을 몇 개까지 만들 수 있는가”보다 “가장 무거운 장면에서도 목표 프레임 시간을 지킬 수 있는가”에 두어야 합니다. 반투명 파티클이 많거나 화면을 크게 덮는 이펙트는 적은 수로도 큰 비용을 만들 수 있으므로, 파티클 수만 보지 말고 오버드로우와 프레임 시간을 함께 확인하는 편이 적절합니다.

### Max Particles 설정

**Max Particles**는 개별 이펙트에 파티클 수 예산을 적용하는 설정입니다. Unity 파티클 시스템에서 동시에 존재할 수 있는 파티클 수의 상한을 정하며, 이 상한에 도달하면 기존 파티클이 소멸해 활성 수가 줄어들기 전까지 새 파티클이 생성되지 않습니다.

값을 정할 때 Emission Rate가 높거나 Lifetime이 길면 활성 파티클 수가 계속 늘어날 수 있으므로, 각 이펙트가 의도한 최대 밀도를 넘지 않도록 상한을 정해야 합니다. 반복 재생되는 연기, 불꽃, 먼지 이펙트는 시간이 지나면 생성되는 파티클 수와 소멸하는 파티클 수가 균형을 이루므로, 유지되는 활성 수를 기준으로 값을 맞추는 편이 적절합니다.

값이 너무 낮으면 이펙트의 밀도가 갑자기 줄거나 흐름이 끊겨 보일 수 있고, 너무 높으면 상한이 실제 예산 제한 역할을 하지 못합니다. 따라서 기본값을 그대로 두기보다, 이펙트가 가장 밀집한 구간에서 필요한 파티클 수를 확인하고 그보다 약간 여유 있는 값으로 설정하는 편이 적절합니다.

### 이펙트별 예산 배분

파티클 수 예산은 이펙트마다 같은 기준으로 나누기 어렵습니다. 비용은 파티클 개수뿐 아니라 화면에서 차지하는 면적, 반투명 정도, 수명, 셰이더 복잡도에 따라 달라지기 때문입니다. 따라서 이펙트별 예산은 “몇 개를 쓰는가”보다 “그 파티클들이 화면에서 어떤 비용을 만드는가”를 기준으로 배분하는 편이 적절합니다.

짧게 나타났다 사라지는 타격 이펙트는 순간 비용은 생기지만 화면에 오래 남지 않습니다. 반대로 연기, 불꽃, 먼지처럼 반복 재생되거나 수명이 긴 이펙트는 파티클 수가 계속 누적되므로, Max Particles와 Lifetime을 더 엄격하게 관리해야 합니다.

이펙트의 시각적 특성도 함께 봐야 합니다. 비나 눈처럼 개별 파티클이 작고 셰이더가 단순한 경우에는 파티클 수가 많아도 오버드로우 영향이 상대적으로 작을 수 있습니다. 반면 폭발, 마법, 연기처럼 큰 반투명 파티클이 한 영역에 밀집하는 이펙트는 파티클 수가 적어도 필레이트 부담이 커질 수 있습니다.

결국 이펙트별 파티클 수는 종류별 고정값으로 정하기보다, 화면에 머무는 시간, 차지하는 면적, 반투명 겹침, 셰이더 복잡도를 함께 보고 배분하는 편이 적절합니다.

---

## Prewarm과 시뮬레이션 스파이크

앞에서는 동시에 존재하는 파티클 수를 기준으로 예산을 나누었습니다. 하지만 총량이 예산 안에 있더라도, 생성과 시뮬레이션 비용이 특정 프레임에 몰리면 순간적인 CPU 스파이크가 발생할 수 있습니다.

이 스파이크는 **Prewarm**을 사용할 때 두드러집니다. 파티클이 0개에서 시작해 서서히 늘어나면 생성과 갱신 비용이 여러 프레임에 나뉘어 발생합니다. **Prewarm**을 켜면 이펙트가 이미 한동안 진행된 상태에서 시작합니다. 예를 들어 연기 이펙트라면 활성화 순간부터 연기가 이미 피어 있는 모습으로 등장합니다. Unity는 이 상태를 만들기 위해 한 사이클 분량(`Duration`)의 시뮬레이션을 활성화 프레임에 압축해 한 번에 실행하므로, 그 프레임의 CPU 비용이 크게 늘어납니다.

### Prewarm의 동작

위에서 말한 비용 집중은 Prewarm이 초기 상태를 만드는 방식에서 발생합니다. Looping 파티클 시스템에서 Duration은 한 번의 반복이 진행되는 시간입니다. Prewarm은 파티클 시스템을 처음 표시할 때 0초 상태에서 시작하지 않고, Duration만큼 시간이 지난 것처럼 파티클의 위치와 수명을 미리 계산해 둔 상태로 시작합니다.

Prewarm이 꺼져 있으면 파티클 시스템은 비어 있는 상태에서 시작합니다. 이후 Emission Rate에 따라 파티클이 생성되고, Lifetime이 끝난 파티클이 소멸하면서 활성 파티클 수가 점차 균형에 가까워집니다. 모닥불, 연기, 안개처럼 계속 유지되는 이펙트는 이 구간에서 처음에는 비어 보일 수 있습니다.

Prewarm이 켜져 있으면 Unity는 파티클 시스템이 활성화될 때, 이미 생성되어 있어야 할 파티클들의 위치와 남은 수명을 한 번에 계산합니다. 그래서 첫 프레임부터 재생이 진행된 상태처럼 보일 수 있지만, 그만큼 생성, 수명 갱신, 모듈 평가가 한 프레임에 모일 수 있습니다.

이 방식은 계속 반복되는 이펙트에서 자연스럽습니다. 연기나 모닥불처럼 일정한 상태를 유지해야 하는 이펙트는 처음부터 어느 정도 채워진 상태로 시작해도 어색하지 않습니다. 반대로 한 번 재생되고 끝나는 폭발이나 타격 이펙트는 시작, 확산, 소멸의 순서 자체가 연출이므로, Prewarm으로 시작 구간을 건너뛰면 의도한 타이밍이 깨질 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Prewarm Off vs On</text>

  <text x="20" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Prewarm Off (기본)</text>
  <line x1="20" y1="62" x2="620" y2="62" stroke="currentColor" stroke-width="0.8"/>

  <text x="20" y="85" font-family="sans-serif" font-size="11" fill="currentColor">t=0</text>
  <text x="60" y="85" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.7">파티클 시스템 활성화</text>
  <circle cx="200" cy="82" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="500" y="85" font-family="sans-serif" font-size="11" fill="currentColor">파티클 1개</text>

  <text x="20" y="110" font-family="sans-serif" font-size="11" fill="currentColor">t=1</text>
  <circle cx="200" cy="107" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="215" cy="107" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <circle cx="230" cy="107" r="3.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text x="500" y="110" font-family="sans-serif" font-size="11" fill="currentColor">파티클 3개</text>

  <text x="20" y="135" font-family="sans-serif" font-size="11" fill="currentColor">t=2</text>
  <g fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="200" cy="132" r="3.5"/><circle cx="215" cy="132" r="3.5"/><circle cx="230" cy="132" r="3.5"/>
    <circle cx="245" cy="132" r="3.5"/><circle cx="260" cy="132" r="3.5"/><circle cx="275" cy="132" r="3.5"/>
  </g>
  <text x="500" y="135" font-family="sans-serif" font-size="11" fill="currentColor">파티클 6개</text>

  <text x="20" y="160" font-family="sans-serif" font-size="11" fill="currentColor">t=3</text>
  <g fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="200" cy="157" r="3.5"/><circle cx="215" cy="157" r="3.5"/><circle cx="230" cy="157" r="3.5"/>
    <circle cx="245" cy="157" r="3.5"/><circle cx="260" cy="157" r="3.5"/><circle cx="275" cy="157" r="3.5"/>
    <circle cx="290" cy="157" r="3.5"/><circle cx="305" cy="157" r="3.5"/><circle cx="320" cy="157" r="3.5"/>
    <circle cx="335" cy="157" r="3.5"/>
  </g>
  <text x="500" y="160" font-family="sans-serif" font-size="11" fill="currentColor">파티클 10개 (정상 상태)</text>

  <text x="20" y="190" font-family="sans-serif" font-size="11" fill="currentColor">→ 정상 상태까지 서서히 도달</text>
  <text x="20" y="210" font-family="sans-serif" font-size="11" fill="currentColor">→ 자연스럽지만, 켜는 순간 비어 보임</text>

  <line x1="20" y1="230" x2="620" y2="230" stroke="currentColor" stroke-width="1"/>

  <text x="20" y="255" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Prewarm On</text>
  <line x1="20" y1="262" x2="620" y2="262" stroke="currentColor" stroke-width="0.8"/>

  <text x="20" y="285" font-family="sans-serif" font-size="11" fill="currentColor">t=0</text>
  <text x="60" y="285" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.7">파티클 시스템 활성화</text>
  <g fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="200" cy="282" r="3.5"/><circle cx="215" cy="282" r="3.5"/><circle cx="230" cy="282" r="3.5"/>
    <circle cx="245" cy="282" r="3.5"/><circle cx="260" cy="282" r="3.5"/><circle cx="275" cy="282" r="3.5"/>
    <circle cx="290" cy="282" r="3.5"/><circle cx="305" cy="282" r="3.5"/><circle cx="320" cy="282" r="3.5"/>
    <circle cx="335" cy="282" r="3.5"/>
  </g>
  <text x="500" y="285" font-family="sans-serif" font-size="11" fill="currentColor">파티클 10개 (즉시 정상 상태)</text>

  <text x="20" y="310" font-family="sans-serif" font-size="11" fill="currentColor">t=1</text>
  <g fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="200" cy="307" r="3.5"/><circle cx="215" cy="307" r="3.5"/><circle cx="230" cy="307" r="3.5"/>
    <circle cx="245" cy="307" r="3.5"/><circle cx="260" cy="307" r="3.5"/><circle cx="275" cy="307" r="3.5"/>
    <circle cx="290" cy="307" r="3.5"/><circle cx="305" cy="307" r="3.5"/><circle cx="320" cy="307" r="3.5"/>
    <circle cx="335" cy="307" r="3.5"/>
  </g>
  <text x="500" y="310" font-family="sans-serif" font-size="11" fill="currentColor">파티클 10개</text>

  <text x="20" y="335" font-family="sans-serif" font-size="11" fill="currentColor">t=2</text>
  <g fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="200" cy="332" r="3.5"/><circle cx="215" cy="332" r="3.5"/><circle cx="230" cy="332" r="3.5"/>
    <circle cx="245" cy="332" r="3.5"/><circle cx="260" cy="332" r="3.5"/><circle cx="275" cy="332" r="3.5"/>
    <circle cx="290" cy="332" r="3.5"/><circle cx="305" cy="332" r="3.5"/><circle cx="320" cy="332" r="3.5"/>
    <circle cx="335" cy="332" r="3.5"/>
  </g>
  <text x="500" y="335" font-family="sans-serif" font-size="11" fill="currentColor">파티클 10개</text>

  <text x="20" y="370" font-family="sans-serif" font-size="11" fill="currentColor">→ 활성화 순간부터 완전한 이펙트</text>
  <text x="20" y="390" font-family="sans-serif" font-size="11" fill="currentColor">→ 첫 프레임에 모든 파티클을 한꺼번에 시뮬레이션</text>
</svg>
</div>

<br>

### Prewarm의 비용

Prewarm의 비용은 파티클 시스템을 활성화하는 순간에 발생합니다.

Prewarm이 꺼져 있으면 파티클 생성, 위치 갱신, 색상·크기 변화가 실제 재생 시간에 따라 여러 프레임으로 나뉘어 처리됩니다. 반대로 Prewarm이 켜져 있으면 Unity가 한 루프 사이클이 지난 상태를 만들기 위해 필요한 계산을 활성화 프레임에 처리합니다. 이때 생성해야 할 파티클 수가 많거나, Noise, Color over Lifetime, Size over Lifetime 같은 모듈이 많이 켜져 있으면 초기화 비용이 커질 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Prewarm 스파이크 (CPU 부하)</text>

  <text x="20" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Prewarm Off — 비용이 프레임에 걸쳐 분산</text>

  <text x="20" y="85" font-family="sans-serif" font-size="11" fill="currentColor">t=0</text>
  <rect x="60" y="76" width="6" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="85" font-family="sans-serif" font-size="11" fill="currentColor">0.05ms (파티클 1개)</text>

  <text x="20" y="110" font-family="sans-serif" font-size="11" fill="currentColor">t=1</text>
  <rect x="60" y="101" width="18" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="110" font-family="sans-serif" font-size="11" fill="currentColor">0.15ms (파티클 3개)</text>

  <text x="20" y="135" font-family="sans-serif" font-size="11" fill="currentColor">t=2</text>
  <rect x="60" y="126" width="36" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="135" font-family="sans-serif" font-size="11" fill="currentColor">0.30ms (파티클 6개)</text>

  <text x="20" y="160" font-family="sans-serif" font-size="11" fill="currentColor">t=3</text>
  <rect x="60" y="151" width="60" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="160" font-family="sans-serif" font-size="11" fill="currentColor">0.50ms (정상 상태)</text>

  <line x1="20" y1="190" x2="620" y2="190" stroke="currentColor" stroke-width="1"/>

  <text x="20" y="215" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Prewarm On — 첫 프레임에 스파이크</text>

  <text x="20" y="245" font-family="sans-serif" font-size="11" fill="currentColor">t=0</text>
  <rect x="60" y="236" width="240" height="14" fill="currentColor" fill-opacity="0.85"/>
  <text x="310" y="245" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2.0ms (한 사이클 전체를 시뮬레이션)</text>

  <text x="20" y="270" font-family="sans-serif" font-size="11" fill="currentColor">t=1</text>
  <rect x="60" y="261" width="60" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="270" font-family="sans-serif" font-size="11" fill="currentColor">0.50ms (정상 상태)</text>

  <text x="20" y="295" font-family="sans-serif" font-size="11" fill="currentColor">t=2</text>
  <rect x="60" y="286" width="60" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="295" font-family="sans-serif" font-size="11" fill="currentColor">0.50ms</text>

  <text x="20" y="320" font-family="sans-serif" font-size="11" fill="currentColor">t=3</text>
  <rect x="60" y="311" width="60" height="14" fill="currentColor" fill-opacity="0.55"/>
  <text x="350" y="320" font-family="sans-serif" font-size="11" fill="currentColor">0.50ms</text>
</svg>
</div>

<br>

Prewarm 스파이크는 Duration이 길수록, Emission Rate가 높을수록, 활성화된 모듈이 많을수록 커집니다. Duration이 길면 미리 계산해야 할 시간 구간이 길어지고, Emission Rate가 높으면 초기화 시점에 만들어야 할 파티클 수가 늘어납니다. 여기에 여러 모듈의 계산이 더해지면 활성화 프레임의 CPU 비용이 더 커집니다.

특히 여러 이펙트가 같은 순간에 Prewarm으로 활성화되면 각각의 초기화 비용이 한 프레임에 겹칩니다. 개별 이펙트의 비용은 작아 보여도, 동시에 처리되면 프레임 드롭으로 이어질 수 있습니다.

### Prewarm 대안

Prewarm을 피하려면 두 가지를 분리해서 생각해야 합니다. 이펙트가 처음 보이는 순간에는 이미 충분히 채워진 상태여야 하지만, 그 상태를 만들기 위한 계산이 같은 프레임에 몰리면 안 됩니다. 따라서 대안은 파티클을 미리 준비해 두거나, 필요한 시뮬레이션을 로딩이나 전환 구간에서 먼저 처리하는 방식입니다.

모닥불, 환경 연기, 안개처럼 씬에 계속 존재하는 이펙트는 플레이어에게 보이기 전부터 파티클 시스템을 활성 상태로 둘 수 있습니다. 이 경우 파티클은 씬이 진행되는 동안 실제 프레임을 따라 생성되고 소멸하므로, Prewarm처럼 활성화 순간에 초기 상태를 한꺼번에 계산하지 않습니다. 플레이어가 해당 영역을 볼 때는 파티클 분포가 이미 충분히 채워진 상태가 됩니다.

호출 시점을 직접 제어해야 한다면 `ParticleSystem.Simulate()`를 사용할 수 있습니다. 이 메서드는 지정한 시간만큼 파티클 시스템을 시뮬레이션하므로, Prewarm처럼 이미 진행된 상태를 만들 수 있습니다. 차이는 시점입니다. 로딩 화면, 씬 전환, 연출 시작 전 준비 구간처럼 프레임 예산에 여유가 있는 시점에 호출하면, 활성화 프레임에 몰릴 비용을 미리 처리할 수 있습니다.

---

## 파티클 Culling

파티클이 화면에 보이지 않는다고 해서 비용이 항상 사라지는 것은 아닙니다. 카메라 밖의 파티클은 렌더링 대상에서 제외될 수 있지만, 생성, 수명, 위치 갱신 같은 시뮬레이션은 Culling 설정에 따라 계속 실행되거나 카메라 안으로 다시 들어올 때 한꺼번에 처리될 수 있습니다.

따라서 파티클 Culling에서는 두 가지를 구분해야 합니다. 먼저 카메라 Frustum 밖에 있는 동안 파티클 시스템을 어떻게 시뮬레이션할지 정하고, 그다음 너무 멀어서 의미가 없는 이펙트는 오브젝트 단위로 비활성화해 시뮬레이션과 렌더링 비용을 함께 제거합니다.

### Culling 모드

Unity의 파티클 시스템에는 카메라 밖에 있을 때의 동작을 제어하는 **Culling Mode** 설정이 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">파티클 Culling: 카메라 Frustum과 파티클 시스템</text>

  <text x="40" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">카메라 Frustum</text>
  <rect x="40" y="62" width="380" height="100" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>

  <g fill="none" stroke="currentColor" stroke-width="1.2">
    <circle cx="120" cy="112" r="5"/>
    <circle cx="140" cy="112" r="5"/>
    <circle cx="160" cy="112" r="5"/>
  </g>
  <text x="180" y="116" font-family="sans-serif" font-size="11" fill="currentColor">파티클 시스템 A</text>
  <text x="180" y="138" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.8">→ 시뮬레이션 + 렌더링</text>

  <g fill="none" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8">
    <circle cx="460" cy="112" r="5"/>
    <circle cx="480" cy="112" r="5"/>
    <circle cx="500" cy="112" r="5"/>
  </g>
  <text x="520" y="116" font-family="sans-serif" font-size="11" fill="currentColor">파티클 시스템 B</text>
  <text x="520" y="138" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.8">→ Culling Mode에 따라 결정</text>

  <line x1="40" y1="180" x2="600" y2="180" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="320" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.7">Frustum 안: 렌더링 대상 / Frustum 밖: Culling Mode 결정</text>
</svg>
</div>

| Culling Mode | 화면 밖 동작 | 화면 복귀 시 |
|---|---|---|
| Automatic (기본) | Looping 시스템은 일시정지하고, Looping이 아닌 일회성 이펙트는 계속 시뮬레이션 | Unity가 시스템 특성에 따라 처리 |
| Pause And Catch-up | 시뮬레이션 일시정지 | 화면 밖에 있던 시간만큼 추가 시뮬레이션을 수행하므로 스파이크가 생길 수 있음 |
| Pause | 시뮬레이션 일시정지 | 정지된 상태에서 이어서 재생되므로 스파이크는 없지만, 화면 밖에서의 시간 흐름은 반영되지 않음 |
| Always Simulate | 화면 밖에서도 시뮬레이션 계속 실행 | 별도 보정 없음 |

<br>

**Always Simulate**는 화면 밖에서도 파티클 시뮬레이션을 계속 진행합니다. 다시 화면에 들어왔을 때 이펙트 상태가 실제 시간 흐름과 맞지만, 보이지 않는 동안에도 CPU 비용이 유지됩니다. 컷씬처럼 카메라 복귀 시점의 이펙트 상태가 중요할 때만 사용하는 편이 적절합니다.

**Pause And Catch-up**은 화면 밖에서는 시뮬레이션을 멈추고, 다시 보이는 순간 화면 밖에 있던 시간만큼 추가 시뮬레이션을 수행합니다. 보이지 않는 동안의 CPU 비용은 줄일 수 있지만, 복귀 프레임에 계산이 몰려 Prewarm과 비슷한 스파이크가 생길 수 있습니다.

**Pause**는 화면 밖에서 시뮬레이션을 멈춘 뒤, 다시 보일 때 멈춘 상태에서 이어서 재생합니다. 화면 밖에서 흐른 시간은 반영되지 않지만, 복귀 시 보정 계산이 없으므로 스파이크가 생기지 않습니다. 카메라 밖에서의 변화가 중요하지 않은 환경 이펙트에 적합합니다.

**Automatic**은 Unity가 파티클 시스템의 특성에 따라 위 동작을 선택하는 모드입니다. Looping 시스템은 보통 Pause처럼 멈추고, Looping이 아닌 일회성 이펙트는 시간 흐름이 끊기지 않도록 계속 시뮬레이션합니다. 기본값으로 시작할 수는 있지만, 화면 밖 비용이나 복귀 시 스파이크가 문제가 되면 이펙트 성격에 맞춰 모드를 직접 지정하는 편이 적절합니다.

### 화면 밖 이펙트 비활성화

Culling Mode는 파티클 시스템이 카메라 Frustum 밖으로 벗어났을 때의 처리 방식을 정합니다. 즉, 보이지 않는 동안 시뮬레이션을 멈출지 계속할지를 결정할 뿐, Frustum 안에 있는 이펙트를 거리나 중요도에 따라 제외하지는 않습니다. 카메라 정면의 먼 거리에 있는 작은 증기나 먼지 이펙트처럼 화면상 영향이 거의 없는 경우에도, Frustum 안에 있다면 시뮬레이션 대상에 남습니다.

이런 경우에는 Culling Mode와 별도로 거리 기준을 두는 편이 적절합니다. 플레이어가 식별하기 어려운 거리의 모닥불, 증기, 먼지 이펙트는 파티클 생성, 수명 계산, 위치 갱신을 유지해도 화면 품질에 기여하는 정도가 작습니다. 일정 거리 밖에서는 파티클 시스템의 게임 오브젝트를 비활성화해 시뮬레이션과 렌더링을 함께 중단하고, 다시 가까워질 때 활성화하는 식으로 관리할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">거리 기반 이펙트 비활성화</text>

  <text x="180" y="55" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활성 범위</text>
  <rect x="50" y="62" width="320" height="130" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3"/>

  <circle cx="100" cy="125" r="9" fill="currentColor"/>
  <text x="115" y="129" font-family="sans-serif" font-size="11" fill="currentColor">카메라</text>

  <circle cx="260" cy="155" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="272" y="159" font-family="sans-serif" font-size="11" fill="currentColor">이펙트 A ← 활성</text>

  <circle cx="430" cy="180" r="6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="442" y="184" font-family="sans-serif" font-size="11" fill="currentColor" fill-opacity="0.65">이펙트 B ← 비활성</text>

  <circle cx="540" cy="225" r="6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="552" y="229" font-family="sans-serif" font-size="11" fill="currentColor" fill-opacity="0.65">이펙트 C ← 비활성</text>

  <line x1="20" y1="252" x2="620" y2="252" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="20" y="272" font-family="sans-serif" font-size="11" fill="currentColor">거리 &lt; 활성 범위 → 이펙트 활성화</text>
  <text x="340" y="272" font-family="sans-serif" font-size="11" fill="currentColor">거리 &gt; 비활성 범위 → 이펙트 비활성화 (게임 오브젝트 Off)</text>
</svg>
</div>

<br>

거리 기반 비활성화는 오픈 월드나 넓은 맵처럼 환경 이펙트가 여러 위치에 흩어져 있는 경우에 효과적입니다. 가까운 이펙트만 유지하고 먼 이펙트를 꺼 두면, 플레이어가 볼 가능성이 낮은 파티클 시스템의 시뮬레이션 비용을 줄일 수 있습니다.

다만 활성화 거리와 비활성화 거리를 같은 값으로 두면 경계 부근에서 문제가 생길 수 있습니다. 플레이어가 기준 거리 주변을 오가거나 카메라가 미세하게 흔들릴 때, 이펙트가 짧은 간격으로 켜지고 꺼질 수 있기 때문입니다. 이런 반복 전환은 **히스테리시스(Hysteresis)**로 줄입니다. 예를 들어 30m 이내로 들어오면 활성화하고, 50m 이상 멀어졌을 때만 비활성화하면 30~50m 구간에서는 기존 상태를 유지하므로 불필요한 전환이 줄어듭니다.

---

## GPU Instancing을 이용한 파티클 렌더링

지금까지는 파티클이 화면에서 얼마나 많이 겹쳐 그려지는지, 그리고 보이지 않는 동안 시뮬레이션을 어떻게 줄일지에 초점을 맞췄습니다. 렌더링 비용에는 여기에 더해 **드로우 콜(Draw Call)** 비용도 포함됩니다.

빌보드 파티클은 보통 하나의 파티클 시스템 안에서 묶여 그려지므로 드로우 콜이 크게 늘지 않습니다. 문제가 되는 경우는 파티클을 3D 메쉬로 렌더링할 때입니다. 메쉬 파티클은 파티클마다 더 많은 정점과 렌더링 상태를 사용하므로, 파티클 수가 늘어날수록 드로우 콜과 CPU 제출 비용이 커질 수 있습니다. 이때 GPU Instancing을 적용하면 같은 메쉬를 반복해서 그리는 비용을 줄일 수 있습니다.

### 빌보드 파티클과 메쉬 파티클의 차이

Unity 파티클 시스템의 기본 렌더링 방식은 빌보드입니다. 빌보드 파티클은 카메라를 향하는 사각형으로 그려지며, 보통 같은 파티클 시스템 안에서 하나로 묶여 렌더링됩니다. 따라서 한 시스템 안의 파티클 수가 늘어난다고 해서 드로우 콜이 파티클 수만큼 늘어나지는 않습니다.

빌보드 파티클에서 먼저 문제가 되는 비용은 대개 드로우 콜보다 화면을 덮는 면적, 오버드로우, 셰이더 복잡도입니다.

상황이 달라지는 지점은 **Render Mode**를 **Mesh**로 설정했을 때입니다. 메쉬 파티클은 각 파티클을 사각형 빌보드가 아니라 지정된 3D 메쉬로 그립니다. 바위 조각, 잔해, 잎사귀처럼 입체 형태가 필요한 이펙트에는 유용하지만, 파티클 하나가 더 많은 정점과 렌더링 데이터를 사용하게 됩니다.

| Render Mode | 렌더링 방식 | 주로 확인할 비용 |
|---|---|---|
| Billboard | 카메라를 향하는 사각형으로 렌더링 | 화면 점유 면적, 오버드로우, 셰이더 비용 |
| Mesh | 지정한 3D 메쉬를 파티클마다 렌더링 | 정점 처리, 메쉬 렌더링 비용, 드로우 콜 증가 여부 |

메쉬 파티클이 여러 시스템에 나뉘어 있거나, 같은 메쉬를 많은 파티클이 반복해서 사용하는 경우에는 드로우 콜과 CPU 제출 비용이 중요해질 수 있습니다. 이때 검토할 수 있는 기능이 GPU Instancing입니다.

### GPU Instancing 적용

GPU Instancing은 동일한 메쉬와 머티리얼을 반복해서 렌더링할 때 효과가 있습니다. 파티클 시스템에서 이 조건에 해당하는 대표적인 경우가 **Mesh Render Mode**입니다. 잔해, 잎사귀, 작은 돌처럼 같은 3D 메쉬를 여러 파티클이 공유한다면, GPU Instancing으로 드로우 콜과 렌더링 명령 제출 비용을 줄일 수 있습니다.

> GPU Instancing의 원리와 SRP Batcher와의 관계는 [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)에서 더 자세히 다룹니다.

파티클 시스템에서 GPU Instancing을 사용하려면 먼저 Renderer 모듈의 Render Mode가 Mesh여야 합니다. 그다음 **Enable GPU Instancing**을 켜고, 해당 머티리얼의 셰이더가 Particle System GPU Instancing을 지원하는지 확인합니다. 실행 플랫폼에서도 GPU Instancing이 지원되어야 합니다.

셰이더 지원 여부는 렌더 파이프라인과 사용하는 셰이더에 따라 달라집니다. 기본 셰이더라도 프로젝트 설정이나 셰이더 종류에 따라 결과가 달라질 수 있으므로, Frame Debugger나 Profiler에서 실제 드로우 콜이 줄었는지 확인하는 편이 적절합니다. 커스텀 셰이더를 사용한다면 일반적인 Instancing 옵션만 켜는 것으로 충분하지 않을 수 있습니다. Unity가 파티클마다 전달하는 위치, 색상, 크기 데이터를 셰이더 코드에서 읽고 적용하도록 작성되어 있어야 합니다.

빌보드 파티클은 이 기능을 먼저 검토할 대상이 아닙니다. 빌보드 파티클의 병목은 보통 드로우 콜보다 오버드로우와 셰이더 비용에서 먼저 나타나므로, 앞에서 다룬 파티클 수, 화면 점유 면적, 셰이더 복잡도 조정이 우선입니다. GPU Instancing은 같은 3D 메쉬를 많이 반복해서 사용하는 메쉬 파티클에서 검토하는 편이 적절합니다.

---

## 마무리

- 파티클 시스템의 비용은 CPU 시뮬레이션과 GPU 렌더링으로 나뉩니다.
- CPU 비용은 활성 파티클 수, Lifetime, Emission Rate, 모듈 구성, Prewarm 여부에 영향을 받습니다.
- GPU 비용은 화면 점유 면적, 오버드로우, 반투명 렌더링, 셰이더 복잡도에 영향을 받습니다.
- Max Particles와 파티클 수 예산은 이펙트가 사용할 수 있는 파티클 수의 상한을 정하는 기준입니다.
- Culling Mode와 거리 기반 비활성화는 보이지 않거나 중요도가 낮은 이펙트의 시뮬레이션 비용을 줄입니다.
- GPU Instancing은 같은 3D 메쉬를 반복해서 사용하는 메쉬 파티클에서 드로우 콜을 줄일 때 검토합니다.

파티클 최적화는 단순히 파티클 수를 줄이는 작업이 아닙니다. 파티클이 얼마나 오래 살아 있는지, 화면에서 얼마나 넓게 겹치는지, 어떤 셰이더로 그려지는지, 보이지 않을 때도 시뮬레이션되는지까지 함께 조정해야 합니다.

<br>

[Part 2](/dev/unity/ParticleAndAnimation-2/)에서는 애니메이션 시스템의 비용을 다룹니다. Animator 사용 여부, 리그 타입(Generic vs Humanoid), 애니메이션 압축, Culling 모드, GPU Skinning이 매 프레임 애니메이션 비용에 어떤 영향을 주는지 살펴봅니다.

<br>

---

**관련 글**
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- **파티클과 애니메이션 (1) - 파티클 시스템 최적화** (현재 글)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)

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
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)
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
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- **파티클과 애니메이션 (1) - 파티클 시스템 최적화** (현재 글)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
