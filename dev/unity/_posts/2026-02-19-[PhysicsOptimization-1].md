---
layout: single
title: "물리 최적화 (1) - 물리 엔진의 실행 구조 - soo:bak"
date: "2026-02-19 21:50:00 +0900"
description: PhysX 동작 원리, 고정 타임스텝, Broadphase/Narrowphase, 콜라이더 비용, Rigidbody Sleep을 설명합니다.
tags:
  - Unity
  - 최적화
  - 물리
  - PhysX
  - 모바일
---

## 물리 연산도 프레임 시간을 사용한다

이전 글에서는 셰이더 복잡도, 오버드로우, 드로우 콜처럼 렌더링 쪽 비용을 다뤘습니다. 렌더링 비용은 주로 GPU 작업량과 연결되지만, 게임의 프레임 시간은 GPU만으로 결정되지 않습니다. Unity의 물리 시뮬레이션은 기본적으로 **CPU에서 실행**되며, 이 시간도 매 프레임 예산에 포함됩니다.

Unity는 게임을 실행하는 동안 스크립트 업데이트와 렌더링뿐 아니라 물리 상태도 갱신합니다. 일반적인 설정에서는 물리 업데이트가 렌더링 프레임과 완전히 같은 간격이 아니라, 고정 시간 스텝을 기준으로 처리됩니다.

따라서 렌더링을 최적화해 GPU 시간이 줄어도, 물리 업데이트가 오래 걸리면 CPU 쪽에서 프레임 시간이 늘어날 수 있습니다. 충돌 검출, Rigidbody 시뮬레이션, Joint 처리, Raycast 같은 작업이 많아질수록 물리 단계의 비용도 커집니다. 물리 최적화는 이 CPU 비용을 관리하는 작업입니다.

> GPU 병렬 처리와 렌더링 파이프라인은 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)과 [래스터라이제이션 파이프라인 (1) - 렌더링 파이프라인의 큰 흐름](/dev/unity/RasterPipeline-1/)에서 더 자세히 다룹니다.
> Unity의 프레임 흐름과 `FixedUpdate()`의 위치는 [게임 루프의 원리 (1) - Unity PlayerLoop와 생명주기](/dev/unity/GameLoop-1/)에서 더 자세히 다룹니다.

---

## PhysX: Unity의 3D 물리 엔진

Unity의 3D 물리 시뮬레이션은 **PhysX** 엔진을 기반으로 동작합니다. PhysX는 고정된 물리 업데이트마다 Rigidbody와 Collider의 상태를 계산합니다.

물리 업데이트 한 번을 **물리 스텝(Physics Step)**이라고 부릅니다. 한 스텝 안에서는 먼저 Rigidbody에 작용한 힘을 속도에 반영하고, 그 속도로 움직일 때 충돌할 수 있는 Collider 쌍을 찾습니다. 이후 실제 접촉과 Joint 제약을 기준으로 위치와 속도를 다시 조정합니다.

따라서 물리 스텝은 속도 갱신, 충돌 검출, 제약 해소라는 순서로 이해할 수 있습니다. 아래 그림은 이 처리 순서를 정리한 것입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">물리 스텝의 큰 흐름</text>

  <rect x="60" y="42" width="440" height="88" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="63" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) 속도 갱신</text>
  <text x="80" y="84" font-family="sans-serif" font-size="11" fill="currentColor">Rigidbody에 작용한 힘과 토크 반영</text>
  <text x="80" y="102" font-family="sans-serif" font-size="11" fill="currentColor">중력, AddForce(), 저항 등을 속도에 반영</text>
  <text x="80" y="121" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 선속도와 각속도 갱신</text>

  <line x1="280" y1="130" x2="280" y2="155" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,150 280,160 285,150" fill="currentColor"/>

  <rect x="60" y="160" width="440" height="88" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="181" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) 충돌 검출 (Collision Detection)</text>
  <text x="80" y="202" font-family="sans-serif" font-size="11" fill="currentColor">충돌 가능성이 있는 Collider 쌍을 선별</text>
  <text x="80" y="220" font-family="sans-serif" font-size="11" fill="currentColor">Broadphase에서 후보를 줄이고 Narrowphase에서 정밀 검사</text>
  <text x="80" y="239" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 접촉점과 충돌 법선 계산</text>

  <line x1="280" y1="248" x2="280" y2="273" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,268 280,278 285,268" fill="currentColor"/>

  <rect x="60" y="278" width="440" height="106" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="299" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) 제약 해소 (Constraint Solving)</text>
  <text x="80" y="320" font-family="sans-serif" font-size="11" fill="currentColor">접촉 제약으로 겹침과 충돌 반응 처리</text>
  <text x="80" y="338" font-family="sans-serif" font-size="11" fill="currentColor">반발, 마찰, 관절(Joint) 제약 반영</text>
  <text x="80" y="356" font-family="sans-serif" font-size="11" fill="currentColor">필요한 속도와 위치 보정 계산</text>
  <text x="80" y="375" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 다음 물리 상태로 갱신</text>
</svg>
</div>

<br>

첫 단계에서는 Rigidbody에 작용한 힘과 토크가 속도에 반영됩니다. 중력(`Physics.gravity`), `AddForce()`, `AddTorque()`, 저항 값은 모두 이 단계에서 선속도와 각속도에 영향을 줍니다.

그다음에는 충돌할 가능성이 있는 Collider 쌍을 찾습니다. 모든 Collider 조합을 정밀하게 검사하면 비용이 너무 크기 때문에, Broadphase에서 먼저 닿을 가능성이 낮은 쌍을 제외합니다. Narrowphase는 이렇게 남은 후보만 실제 Collider 형상에 가깝게 검사하여, 접촉 여부와 접촉점, 충돌 법선을 계산합니다.

마지막으로 PhysX는 계산된 접촉과 제약을 만족하도록 Rigidbody의 움직임을 조정합니다. Collider가 서로 파고들었다면 겹침을 줄이고, 충돌 표면에서는 반발과 마찰을 반영합니다. Joint가 연결된 물체라면 거리나 회전 제한도 함께 맞춥니다.

Unity의 기본 실행 흐름에서는 한 프레임 업데이트 안에서 물리 단계가 먼저 처리되고, 그 뒤에 일반 업데이트와 렌더링 단계가 이어집니다. 물리 단계는 렌더링이 끝난 뒤에 따로 실행되는 것도 아니고, 렌더링과 동시에 실행되는 것도 아닙니다.

---

## 고정 타임스텝 (Fixed Timestep)

다만 물리 단계가 매 프레임마다 정확히 한 번 실행되는 것은 아닙니다. Unity는 물리 시뮬레이션을 일정한 시간 간격으로 진행하기 위해 **고정 타임스텝(Fixed Timestep)**을 사용합니다. 누적 시간이 고정 간격에 도달하지 못한 프레임에서는 물리 스텝이 실행되지 않을 수 있고, 프레임 시간이 길어진 경우에는 한 프레임 업데이트 안에서 물리 스텝이 여러 번 처리될 수 있습니다.

### 물리가 고정 간격으로 실행되는 이유

물리 스텝은 일정 시간 동안 물체가 얼마나 움직였는지를 계산합니다. 속도가 같아도 계산에 사용하는 시간 간격이 길면 더 멀리 이동하고, 시간 간격이 짧으면 덜 이동합니다. 따라서 물리 스텝의 시간 간격이 매번 달라지면 같은 힘과 속도를 사용해도 결과가 달라질 수 있습니다.

예를 들어 같은 속도로 움직이는 Rigidbody라도 0.01초 동안 계산할 때와 0.05초 동안 계산할 때의 이동 거리는 다릅니다. 만약 프레임 시간을 그대로 물리 계산에 사용한다면, 프레임 드롭이 발생한 순간 한 번의 계산에서 물체가 크게 이동할 수 있습니다. 이 경우 얇은 Collider를 지나치거나 Joint가 불안정하게 반응할 가능성이 커집니다.

그래서 물리 시뮬레이션은 렌더링 프레임 시간에 그대로 맞추기보다, 일정한 시간 간격을 기준으로 처리합니다. Unity의 기본 Fixed Timestep은 **0.02초(50Hz)**입니다.

### 프레임과 물리 스텝의 관계

렌더링 프레임 시간은 매번 달라질 수 있습니다. 어떤 프레임은 10ms 만에 처리되고, 어떤 프레임은 50ms가 걸릴 수 있습니다.
이 때문에 한 프레임에서 물리 스텝이 0번, 1번, 또는 여러 번 처리될 수 있습니다. Fixed Timestep이 20ms라면, 누적된 시간이 20ms에 도달할 때마다 물리 스텝을 한 번 처리합니다. 처리한 20ms는 누적 시간에서 빠지고, 남은 시간이 다시 20ms 이상이면 물리 스텝을 한 번 더 처리합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">프레임 시간과 물리 스텝 처리 횟수 (Fixed Timestep = 0.02초)</text>

  <text x="40" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프레임이 빠를 때 (프레임 시간 = 10ms)</text>

  <rect x="40" y="68" width="100" height="44" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임 1</text>
  <text x="90" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">10ms · 물리 0회</text>

  <rect x="142" y="68" width="100" height="44" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="192" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임 2</text>
  <text x="192" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">10ms · 물리 1회</text>

  <rect x="244" y="68" width="100" height="44" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="294" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임 3</text>
  <text x="294" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">10ms · 물리 0회</text>

  <rect x="40" y="118" width="202" height="28" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="141" y="136" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">물리 스텝 1 (20ms)</text>

  <rect x="244" y="118" width="202" height="28" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="345" y="136" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">물리 스텝 2 (20ms)</text>

  <text x="40" y="170" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 누적 시간이 20ms에 도달할 때마다 물리 1회 실행 (프레임당 0회 또는 1회)</text>

  <text x="40" y="220" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프레임이 느릴 때 (프레임 시간 = 50ms)</text>

  <rect x="40" y="232" width="500" height="58" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프레임 1 (50ms)</text>

  <rect x="55" y="260" width="200" height="22" rx="2" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="155" y="276" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">물리 스텝 1 (20ms)</text>

  <rect x="265" y="260" width="200" height="22" rx="2" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="276" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">물리 스텝 2 (20ms)</text>

  <text x="40" y="312" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 한 프레임 안에서 물리 2회 처리 (누적 시간을 따라잡기 위해 반복)</text>
</svg>
</div>

<br>

이 그림에서 중요한 점은 프레임 하나와 물리 스텝 하나가 1:1로 대응하지 않는다는 것입니다. 프레임 시간이 짧으면 물리 스텝이 처리되지 않는 프레임도 있고, 프레임 시간이 길면 같은 프레임 안에서 여러 물리 스텝이 처리될 수 있습니다.

즉, Fixed Timestep은 물리 스텝 하나가 몇 초 분량의 움직임을 계산할지 정하는 값입니다. Unity는 누적된 시간이 이 값에 도달할 때마다 물리 스텝을 처리합니다. 그래서 프레임 시간이 길면 같은 프레임 안에서 여러 물리 스텝이 이어질 수 있습니다.

### Maximum Allowed Timestep

앞 절의 구조에서는 프레임 시간이 길수록 한 번의 프레임 업데이트에서 처리할 물리 스텝 수도 늘어납니다. 예를 들어 Fixed Timestep이 20ms인데 어떤 프레임이 200ms 걸렸다면, 200ms를 따라잡기 위해 물리 스텝이 최대 10번 필요해집니다.

문제는 물리 스텝 1회가 단순한 시간 차감이 아니라, Rigidbody 갱신, 충돌 검출, 제약 해소를 실제로 한 번 수행하는 CPU 작업이라는 점입니다. 물리 스텝이 10회 필요해지면 이 작업도 10번 반복됩니다. 그만큼 물리 처리에 쓰는 CPU 시간이 증가하고, 렌더링을 포함한 다음 프레임 작업을 시작하거나 끝내는 시점도 뒤로 밀릴 수 있습니다. 이 시간이 다시 누적되면 다음번에도 여러 물리 스텝을 처리해야 하는 상황이 반복됩니다. 이런 악순환을 흔히 **Spiral of Death**라고 부릅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">물리 스텝 폭주 시나리오 (Spiral of Death)</text>

  <text x="290" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">초기 조건 — 프레임 시간: 200ms, Fixed Timestep: 20ms</text>

  <rect x="170" y="68" width="240" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="93" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">물리 스텝 10회 실행 (200ms ÷ 20ms)</text>

  <line x1="290" y1="108" x2="290" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,123 290,133 295,123" fill="currentColor"/>

  <rect x="170" y="133" width="240" height="40" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="158" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">물리 처리 시간 증가</text>

  <line x1="290" y1="173" x2="290" y2="193" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,188 290,198 295,188" fill="currentColor"/>

  <rect x="170" y="198" width="240" height="40" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="223" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">다음 화면 갱신 지연 (250ms)</text>

  <line x1="290" y1="238" x2="290" y2="258" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,253 290,263 295,253" fill="currentColor"/>

  <rect x="170" y="263" width="240" height="40" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="288" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">물리 스텝 12회 실행 → 악순환</text>

  <path d="M 410 283 Q 510 283 510 175 Q 510 88 410 88" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <polygon points="415,83 405,88 415,93" fill="currentColor"/>
</svg>
</div>

<br>

**Maximum Allowed Timestep**은 물리 스텝을 연속해서 처리할 수 있는 시간의 상한입니다. Unity의 기본값은 0.333초입니다.

프레임 시간이 크게 늘어나 물리 스텝이 많이 밀렸더라도, Unity는 물리 스텝을 무한정 처리하지 않습니다. Maximum Allowed Timestep에 도달하면 그 시점에서는 더 많은 물리 스텝을 실행하지 않고, 다음 화면 갱신으로 넘어갈 수 있게 합니다.

이렇게 하면 물리 계산이 CPU 시간을 계속 차지해 화면 갱신을 더 늦추는 상황을 줄일 수 있습니다. 대신 그 시점에 처리하지 못한 물리 스텝은 생략될 수 있습니다. 생략된 시간만큼 물리 시뮬레이션은 실제 경과 시간을 모두 반영하지 못하므로, 프레임 드롭 순간에는 물체 움직임이 잠깐 느려지거나 끊겨 보일 수 있습니다.

이 값을 낮추면 물리 스텝을 연속으로 처리하는 시간이 줄어들어, 물리 처리에 쓰는 CPU 시간을 더 강하게 제한할 수 있습니다. 그 대신 아직 처리하지 못한 물리 스텝이 남아도 더 일찍 멈추게 되므로, 물리 시뮬레이션이 실제 경과 시간을 덜 반영할 가능성이 커집니다. 결국 이 값은 낮을수록 무조건 좋은 설정이 아니라, 목표 프레임률과 물리 정확도 사이에서 조정해야 하는 값입니다.

> Unity의 고정 타임스텝과 `FixedUpdate()` 흐름은 [게임 루프의 원리 (1) - Unity PlayerLoop와 생명주기](/dev/unity/GameLoop-1/)와 [Update, FixedUpdate 그리고 LateUpdate](/dev/unity/UpdateFunctions/)에서 더 자세히 다룹니다.

<br>

---

## 충돌 검출: Broadphase와 Narrowphase

앞 절에서 본 물리 스텝은 속도 갱신, 충돌 검출, 제약 해소로 이어집니다. 이 중 충돌 검출은 씬의 오브젝트 수가 늘어날수록 비용이 빠르게 커질 수 있는 단계입니다. 충돌을 계산하려면 먼저 충돌 가능성이 있는 Collider 조합을 선별해야 하기 때문입니다.

이 비용을 줄이는 핵심이 Broadphase와 Narrowphase의 역할 분담입니다.

### 두 단계로 나누는 이유

씬에 Collider가 $n$개 있으면, 가능한 Collider 쌍의 수는 $n \times (n-1) / 2$입니다. Collider가 100개라면 4,950쌍이고, 1,000개라면 약 50만 쌍입니다. 오브젝트 수가 늘어날수록 검사 후보가 빠르게 늘어나는 구조입니다.

<br>

가능한 Collider 쌍의 수는 다음과 같이 늘어납니다.

| Collider 수 | 검사해야 할 쌍의 수 |
|---:|---:|
| 10 | 45 |
| 50 | 1,225 |
| 100 | 4,950 |
| 500 | 124,750 |
| 1,000 | 499,500 |

<br>

가능한 조합은 많지만, 실제로 정밀 검사가 필요한 조합은 그중 일부입니다.
서로 멀리 떨어진 Collider끼리는 충돌할 수 없으므로, 실제 형상까지 비교할 필요가 없습니다. 그래서 충돌 검출은 먼저 충돌 가능성이 낮은 조합을 제외하고, 남은 후보만 정밀하게 확인하는 구조로 나뉩니다.

### Broadphase: 후보 쌍 필터링

Broadphase의 목적은 정밀 검사가 필요한 Collider 조합을 빠르게 줄이는 것입니다. 이를 위해서는 Collider의 실제 형상을 모두 계산하기보다, 먼저 대략적인 위치 범위만 비교하는 편이 효율적입니다.

PhysX는 이 빠른 비교를 위해 각 Collider를 감싸는 단순한 상자를 사용합니다. 이 상자를 **AABB(Axis-Aligned Bounding Box, 축 정렬 경계 상자)**라고 합니다.
AABB는 x, y, z 축에 나란한 직육면체입니다. 두 AABB가 겹치는지는 각 축의 최솟값과 최댓값 범위가 겹치는지만 확인하면 됩니다. 실제 Collider의 삼각형, 곡면, 캡슐 형태를 직접 비교하는 것보다 훨씬 단순한 검사입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">AABB 겹침 검사</text>

  <text x="145" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">겹치지 않음 → 정밀 검사 생략</text>

  <rect x="55" y="72" width="80" height="60" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="95" y="108" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor">A</text>

  <rect x="170" y="72" width="80" height="60" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="210" y="108" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor">B</text>

  <text x="435" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">겹침 → 후보 쌍 등록, Narrowphase로 전달</text>

  <rect x="345" y="72" width="80" height="60" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="375" y="100" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor">A</text>

  <rect x="405" y="100" width="80" height="60" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="460" y="138" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor">B</text>

  <rect x="405" y="100" width="20" height="32" fill="currentColor" fill-opacity="0.20"/>

  <text x="290" y="200" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">겹침 조건 — 모든 축에서 동시에 범위가 겹쳐야 함</text>

  <rect x="80" y="215" width="420" height="95" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="290" y="242" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">A.min.x ≤ B.max.x  AND  A.max.x ≥ B.min.x</text>
  <text x="290" y="266" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">A.min.y ≤ B.max.y  AND  A.max.y ≥ B.min.y</text>
  <text x="290" y="290" text-anchor="middle" font-family="monospace" font-size="12" fill="currentColor">A.min.z ≤ B.max.z  AND  A.max.z ≥ B.min.z</text>
</svg>
</div>

<br>

AABB가 겹치지 않는 조합은 실제 Collider도 서로 겹칠 수 없습니다. 따라서 이런 조합은 Narrowphase로 넘기지 않습니다.

반대로 AABB가 겹치는 조합은 Narrowphase 후보로 남습니다. AABB는 실제 형상을 감싸는 단순한 상자이므로, 상자끼리는 겹쳐도 실제 Collider는 떨어져 있을 수 있습니다. 따라서 Broadphase의 결과는 충돌 확정이 아니라, 정밀 검사가 필요한 후보 목록입니다.

AABB 겹침 검사는 Broadphase가 후보를 줄이는 기본 기준입니다.
실제 엔진은 모든 AABB 조합을 하나씩 비교하지 않고, 비교할 후보를 더 빨리 좁히기 위한 자료구조를 사용합니다. Unity의 Physics 설정에서도 Broadphase Type을 선택할 수 있으며, 대표적인 방식으로 Sweep and Prune(SAP)과 Multi Box Pruning(MBP)이 있습니다.

**SAP(Sweep and Prune)**는 AABB를 한 축에 투영한 구간으로 보고, 그 구간이 겹치지 않는 조합을 먼저 제외하는 방식입니다. 예를 들어 x축 범위가 서로 겹치지 않는 두 AABB는 y축이나 z축을 확인하지 않아도 충돌 후보에서 제외할 수 있습니다. 이렇게 한 축에서 떨어진 조합을 먼저 걸러 비교 대상을 줄입니다.

**MBP(Multi Box Pruning)**는 월드를 여러 영역으로 나누고, 각 영역 안에서 Sweep and Prune을 수행하는 방식입니다. 넓은 씬에서는 서로 멀리 떨어진 Collider가 같은 Broadphase 처리 범위에 들어오지 않도록 나눌 수 있으므로, 불필요한 후보 조합을 줄이는 데 도움이 될 수 있습니다.

### Narrowphase: 정밀 충돌 검사

Narrowphase는 Broadphase에서 남은 후보를 실제 Collider 형상으로 검사하는 단계입니다. AABB가 아니라 Box, Sphere, Capsule, Mesh 같은 Collider의 실제 모양을 사용해 두 Collider가 겹치는지 확인합니다.

이 단계에서 실제 충돌로 판정된 조합만 충돌 해소 단계로 넘어갑니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Broadphase → Narrowphase 흐름</text>

  <text x="290" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">씬의 전체 콜라이더: 500개 (약 125,000쌍)</text>

  <line x1="290" y1="63" x2="290" y2="85" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,80 290,90 295,80" fill="currentColor"/>

  <rect x="155" y="92" width="270" height="65" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="113" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Broadphase</text>
  <text x="290" y="131" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">AABB 겹침 검사</text>
  <text x="290" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">(축 범위 비교, 빠름)</text>

  <line x1="290" y1="157" x2="290" y2="208" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,203 290,213 295,203" fill="currentColor"/>
  <text x="300" y="184" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">AABB가 겹치는 쌍: 약 200쌍 (99.8% 제거)</text>

  <rect x="175" y="215" width="230" height="65" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="236" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Narrowphase</text>
  <text x="290" y="254" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">정밀 형상 검사</text>
  <text x="290" y="271" text-anchor="middle" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">(기하학적 계산, 느림)</text>

  <line x1="290" y1="280" x2="290" y2="328" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,323 290,333 295,323" fill="currentColor"/>
  <text x="300" y="307" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">실제 충돌 쌍: 약 30쌍</text>

  <rect x="195" y="335" width="190" height="42" rx="6" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="361" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">충돌 해소 (Constraint Solving)</text>
</svg>
</div>

<br>

Narrowphase에서 실제 충돌로 확인된 조합에 대해서는 **접촉점(Contact Point)**과 **접촉 법선(Contact Normal)** 같은 정보가 계산됩니다. 접촉점은 두 Collider가 맞닿은 위치를 나타내고, 접촉 법선은 충돌 표면에서 어느 방향으로 밀어내야 하는지를 나타냅니다.

충돌 해소 단계는 이 정보를 사용해 Rigidbody의 위치와 속도를 보정하고, 반발이나 마찰 같은 충돌 반응을 적용합니다. Unity에서 `OnCollisionEnter`가 받는 `Collision` 파라미터의 `contacts` 배열도 이런 접촉점 정보를 담고 있습니다.

### Broadphase 비용이 증가하는 조건

Broadphase 비용은 크게 두 요소의 영향을 받습니다. 하나는 씬에 존재하는 **활성 Collider의 수**이고, 다른 하나는 **그 Collider들이 얼마나 자주 움직이는지**입니다.

활성 Collider가 많으면 Broadphase가 관리해야 할 AABB도 많아집니다. 그만큼 겹침 후보를 만들고 관리하는 비용이 증가합니다.

움직이는 Collider는 여기에 갱신 비용이 추가됩니다. 위치가 변하지 않는 정적 Collider는 같은 AABB를 계속 사용할 수 있지만, Rigidbody와 함께 움직이는 Collider는 물리 스텝마다 새 위치에 맞춰 AABB와 Broadphase 자료구조를 갱신해야 합니다. 움직이는 Collider가 많을수록 이 갱신 비용이 누적됩니다.

<br>

**정적 Collider와 동적 Collider의 Broadphase 비용**

| 측면 | 정적 Collider | 동적 Collider |
|---|---|---|
| AABB | 위치가 변하지 않으면 재사용 가능 | 움직임에 따라 갱신 필요 |
| Broadphase 자료구조 | 갱신 비용이 작음 | 위치 변화에 따라 갱신 필요 |
| 후보 조합 | 대체로 안정적 | 주변 Collider와의 후보 조합이 자주 바뀔 수 있음 |

<br>

따라서 Broadphase 최적화에서는 Collider의 총수만으로 비용을 판단하기 어렵습니다. 배경 지형이나 벽처럼 움직이지 않는 Collider보다, Rigidbody와 함께 움직이며 매 스텝 AABB가 바뀌는 Collider가 비용에 더 큰 영향을 줄 수 있습니다. Broadphase 비용을 볼 때는 전체 Collider 수와 함께, 위치 변화 때문에 AABB 갱신이 필요한 Collider 수를 확인해야 합니다.

---

## 콜라이더 종류별 비용

Broadphase를 거쳐 후보가 줄어들면, Narrowphase에서는 남은 Collider 조합을 실제 형상 기준으로 검사합니다. 이때 비용은 Collider가 어떤 형태인지에 따라 크게 달라집니다.

비용 차이는 충돌 형상을 얼마나 단순한 규칙으로 표현할 수 있는지에서 나옵니다. Sphere는 중심과 반지름만으로, Capsule은 중심선과 반지름만으로 충돌을 대략 판별할 수 있습니다.
반면 MeshCollider는 메쉬를 이루는 삼각형 구조를 기준으로 검사해야 하므로, 더 복잡한 표면을 표현할 수 있는 대신 검사 과정도 무거워지기 쉽습니다.

### Primitive 콜라이더

Primitive Collider는 Unity가 기본으로 제공하는 단순한 기하 형상의 Collider입니다. Box, Sphere, Capsule이 대표적입니다.
형태가 정해져 있기 때문에, 물리 엔진은 복잡한 메쉬를 해석하지 않고 해당 기본 형상끼리의 관계만 계산하면 됩니다.

Primitive Collider 사이에도 필요한 계산은 조금씩 다릅니다. 중요한 점은 모두 정해진 기본 형상을 기준으로 판별한다는 것입니다. 오브젝트의 시각적 모델이 복잡하더라도 Collider 자체가 Sphere라면 물리 엔진은 Sphere로만 충돌을 계산합니다. 따라서 MeshCollider처럼 삼각형 수에 따라 검사 대상이 늘어나지 않고, 대부분의 경우 Narrowphase 비용이 낮고 예측하기 쉽습니다.

### MeshCollider

MeshCollider는 메쉬를 충돌 형상으로 사용하는 Collider입니다. Primitive Collider처럼 기본 도형으로 근사하지 않고, 메쉬가 가진 표면과 굴곡을 충돌 계산에 반영할 수 있습니다. 지형, 계단, 건물 내부처럼 표면 형태가 중요한 오브젝트에 유용하지만, Narrowphase에서는 메쉬의 삼각형 구조를 다루어야 하므로 비용이 커지기 쉽습니다.

MeshCollider는 크게 Non-Convex와 Convex로 나눌 수 있습니다. 두 방식은 원본 메쉬를 얼마나 유지하는지, 그리고 어떤 오브젝트에 사용할 수 있는지가 다릅니다.

<br>

**MeshCollider 사용 기준**

| 방식 | 충돌 형상 | 적합한 경우 | 제약 |
|---|---|---|---|
| Non-Convex | 원본 메쉬의 오목한 구조와 빈 공간을 유지 | 지형, 계단, 건물 내부처럼 움직이지 않는 충돌 표면 | 오브젝트 자체가 힘과 충돌 반응으로 움직이는 Rigidbody라면 사용할 수 없음 |
| Convex | 메쉬를 볼록한 충돌 형상으로 단순화 | MeshCollider가 필요한 동적 Rigidbody | 오목한 부분과 빈 공간이 충돌 형상에서 사라질 수 있음 |

<br>

Non-Convex MeshCollider는 원본 메쉬의 오목한 부분과 빈 공간을 충돌 형상에 그대로 남깁니다. 계단의 단차, 건물 내부의 통로, 지형의 굴곡처럼 표면 구조가 중요한 환경 오브젝트에 적합합니다. 움직이지 않는 바닥이나 벽에 사용하면, 플레이어나 물체의 Rigidbody가 그 표면에 부딪히거나 그 위를 이동할 수 있습니다.
대신 Narrowphase 비용은 높아집니다. 충돌 형상이 삼각형 기반이기 때문에, 충돌 후보가 된 Collider가 메쉬의 어느 삼각형과 관련되는지 좁혀야 합니다. PhysX는 **BVH(Bounding Volume Hierarchy)** 같은 가속 구조로 가능성이 낮은 삼각형 묶음을 제외하지만, 최종적으로는 삼각형 구조를 기준으로 충돌을 판별합니다.

> Unity의 3D 물리에서 Non-Convex MeshCollider는 주로 움직이지 않는 충돌 표면에 사용됩니다. Rigidbody가 힘과 충돌 반응을 받아 움직이는 경우에는, 물리 엔진이 해당 Collider를 동적인 강체 형상으로 계산해야 합니다. PhysX는 이런 Collider에 볼록 형상을 요구하므로, MeshCollider를 사용하려면 Convex 옵션을 켜야 합니다.

<br>

Convex MeshCollider는 원본 메쉬를 **볼록 껍질(Convex Hull)** 형태로 변환합니다. 볼록 껍질은 안쪽으로 파인 공간이 없는 충돌 형상입니다. 이 변환을 거치면 Non-Convex보다 충돌 판별이 단순해지고 비용도 낮아집니다.
대신 원래 메쉬의 빈 공간이나 오목한 윤곽이 사라질 수 있어, 화면상으로는 들어갈 수 있어 보이는 부분이 물리적으로는 막힌 것처럼 동작할 수 있습니다. Primitive Collider보다는 여전히 복잡하므로 비용도 더 높습니다.

### 비용 비교와 Compound Collider

앞의 내용을 Narrowphase 비용 관점에서 정리하면 다음과 같습니다. 실제 비용은 Collider 조합, 접촉 수, 플랫폼에 따라 달라질 수 있으므로 절대적인 순위가 아니라 일반적인 경향으로 봐야 합니다.

| 종류 | 비용 경향 | 이유 |
|---|---|---|
| Sphere | 낮음 | 중심과 반지름으로 단순하게 판별 가능 |
| Capsule | 낮음 | 중심선과 반지름을 기준으로 판별 |
| Box | 낮음 | 제한된 수의 축 비교로 판별 |
| Convex MeshCollider | 중간 | 볼록 형상으로 단순화되지만 Primitive보다 복잡함 |
| Non-Convex MeshCollider | 높음 | 삼각형 구조를 기준으로 후보와 접촉을 계산 |

<br>

정확한 메쉬 윤곽이 꼭 필요하지 않다면, MeshCollider 대신 여러 Primitive Collider를 조합하는 방법도 있습니다. 여러 Primitive Collider를 하나의 Rigidbody 아래에 배치해 하나의 충돌 형상처럼 사용하는 구성을 **Compound Collider**라고 합니다. 예를 들어 캐릭터의 몸통은 Capsule, 무기는 Box, 방패는 Sphere로 근사할 수 있습니다.

Compound Collider는 원본 모델의 세부 윤곽을 그대로 재현하기보다, 충돌에 필요한 큰 형태를 여러 Primitive Collider로 근사합니다. 물리 엔진은 복잡한 메쉬 하나가 아니라 단순한 기본 형상 여러 개를 검사하므로, 동적 오브젝트에서는 MeshCollider보다 비용을 낮추기 쉽습니다. 각 Primitive Collider의 위치와 크기를 조정해 원하는 충돌 범위를 맞출 수 있다는 장점도 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">MeshCollider vs Compound Collider</text>

  <text x="145" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">MeshCollider (삼각형 2,000개)</text>

  <path d="M 145 75 L 175 90 L 190 130 L 180 175 L 170 200 L 178 232 L 145 245 L 112 232 L 120 200 L 110 175 L 100 130 L 115 90 Z" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <line x1="145" y1="75" x2="145" y2="245" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>
  <line x1="115" y1="90" x2="178" y2="232" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>
  <line x1="175" y1="90" x2="112" y2="232" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>
  <line x1="100" y1="130" x2="190" y2="130" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>
  <line x1="110" y1="175" x2="180" y2="175" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>
  <line x1="120" y1="200" x2="170" y2="200" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.5"/>

  <text x="145" y="270" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">메쉬 형상 그대로 사용 → 정밀하지만 비용 높음</text>

  <text x="435" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Compound Collider (Primitive 조합)</text>

  <circle cx="420" cy="95" r="18" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="100" font-family="sans-serif" font-size="11" fill="currentColor">← Sphere (머리)</text>

  <rect x="410" y="120" width="20" height="60" rx="10" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="155" font-family="sans-serif" font-size="11" fill="currentColor">← Capsule (몸통)</text>

  <rect x="403" y="186" width="11" height="42" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <rect x="426" y="186" width="11" height="42" rx="2" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="212" font-family="sans-serif" font-size="11" fill="currentColor">← Box 2개 (다리)</text>

  <text x="435" y="270" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">근사적이지만 비용 낮음</text>
</svg>
</div>

<br>

Collider 선택은 정밀도와 비용의 균형입니다. 정적인 환경처럼 표면 형태가 중요한 경우에는 MeshCollider가 필요할 수 있고, 물리 시뮬레이션으로 움직이는 오브젝트는 Convex MeshCollider나 Compound Collider처럼 더 단순한 충돌 형상을 우선 검토하는 편이 좋습니다.

<br>

---

## Rigidbody Sleep

Collider의 수와 형상이 같아도, 모든 Rigidbody가 매 물리 스텝마다 같은 방식으로 처리되지는 않습니다. 이미 멈춰 있는 Rigidbody까지 계속 속도와 위치를 갱신하면 불필요한 비용이 생깁니다. Unity의 3D 물리는 이런 Rigidbody를 **Sleep 상태**로 두어, 다시 시뮬레이션할 필요가 생기기 전까지 반복 갱신을 줄입니다.

### Sleep 상태란

Sleep은 충분히 안정된 Rigidbody의 반복 갱신을 일시적으로 멈추는 상태입니다. Collider나 GameObject를 비활성화하는 기능은 아니며, Rigidbody의 속도와 위치를 매 물리 스텝마다 다시 계산하지 않도록 하는 최적화에 가깝습니다.

예를 들어 바닥 위에 멈춰 있는 상자가 Awake 상태라면, PhysX는 물리 스텝마다 상자의 속도와 위치를 갱신하고 바닥과의 접촉을 처리합니다. 화면상으로는 정지해 보여도 물리 계산에는 계속 포함됩니다.

Sleep 상태가 되면 이 Rigidbody는 매 스텝 다시 계산되지 않습니다. Awake 상태에서 수행하던 속도와 위치 갱신, 접촉 보정, Joint 제약 해소가 생략됩니다. 또한 Collider 위치가 변하지 않으므로, Broadphase에서 사용하는 경계 정보를 계속 갱신할 필요도 줄어듭니다.

Sleep 상태의 Rigidbody도 다시 움직일 조건이 생기면 Awake 상태로 돌아옵니다. 다른 Awake Rigidbody가 충돌하거나 `AddForce()`, `WakeUp()` 같은 호출이 발생하는 경우가 여기에 해당합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Sleep 상태의 효과 — 씬에 Rigidbody 200개</text>

  <rect x="50" y="50" width="75" height="42" rx="4" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text x="87" y="76" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">30개</text>

  <rect x="125" y="50" width="425" height="42" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.5"/>
  <text x="337" y="76" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">170개</text>

  <text x="87" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활성(Awake)</text>
  <text x="337" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Sleep 상태</text>

  <text x="87" y="135" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">매 물리 스텝마다</text>
  <text x="87" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">속도·위치 갱신, 접촉 처리</text>

  <text x="337" y="135" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">반복 갱신에서 제외</text>
  <text x="337" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">필요하면 다시 Awake</text>

  <text x="290" y="200" text-anchor="middle" font-family="sans-serif" font-size="12" font-style="italic" fill="currentColor">→ 씬의 Rigidbody 수보다 Awake 상태인 Rigidbody 수가 더 중요함</text>
</svg>
</div>

### Sleep 전환 조건

Rigidbody가 Sleep 상태로 전환되려면 움직임이 충분히 작아져야 합니다.
Unity는 Rigidbody가 얼마나 움직이고 회전하는지를 기준으로 Sleep 전환 여부를 판단합니다. 내부적으로는 선속도와 각속도에서 계산한 운동 에너지를 **Sleep Threshold**와 비교하며, 운동 에너지가 이 기준보다 낮은 상태로 유지되면 Sleep 상태로 전환될 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Sleep 전환 과정</text>

  <line x1="80" y1="55" x2="80" y2="225" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="75,60 80,48 85,60" fill="currentColor"/>
  <text x="80" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">운동 에너지</text>

  <line x1="80" y1="225" x2="545" y2="225" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="540,220 550,225 540,230" fill="currentColor"/>
  <text x="540" y="247" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">시간</text>

  <line x1="80" y1="155" x2="530" y2="155" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="88" y="148" font-family="sans-serif" font-size="10" fill="currentColor">Sleep Threshold</text>

  <path d="M 95 75 L 130 105 L 165 145 L 200 175 L 240 160 L 280 138 L 320 175 L 365 200 L 420 207 L 530 207" fill="none" stroke="currentColor" stroke-width="1.8"/>

  <circle cx="430" cy="207" r="4" fill="currentColor"/>
  <line x1="434" y1="206" x2="468" y2="188" stroke="currentColor" stroke-width="1"/>
  <text x="473" y="192" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Sleep 상태로 전환</text>

  <text x="290" y="275" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">운동 에너지가 Sleep Threshold보다 낮게 유지되면 Sleep 상태로 전환</text>
</svg>
</div>

<br>

Sleep Threshold는 Rigidbody가 Sleep 상태로 전환될지 판단할 때 사용하는 에너지 기준값입니다.
Rigidbody별 값은 `Rigidbody.sleepThreshold`로 조정할 수 있고, 프로젝트 기본값은 `Project Settings > Physics > Sleep Threshold`에서 설정합니다. Unity의 기본값은 일반적으로 0.005입니다.

### Sleep 해제 조건

Sleep 상태의 Rigidbody도 외부 작용을 받으면 다시 Awake 상태로 돌아옵니다. 즉, 물리 엔진이 속도와 위치를 다시 갱신해야 하는 상황이 생기면 Sleep 상태가 해제됩니다.

대표적인 경우는 힘이나 토크를 가하는 경우입니다. `AddForce()`나 `AddTorque()`를 호출하면 Rigidbody는 다시 시뮬레이션 대상이 됩니다. 다만 `useGravity`가 활성화되어 있다는 이유만으로 Rigidbody가 계속 Awake 상태로 유지되는 것은 아닙니다. 충분히 안정된 Rigidbody라면 중력의 영향을 받는 설정이어도 Sleep 상태로 들어갈 수 있습니다.

다른 Rigidbody와의 상호작용도 Sleep을 해제할 수 있습니다. Awake 상태의 Rigidbody가 Sleep 상태의 Rigidbody와 충돌하거나, Joint로 연결된 Rigidbody가 움직이면 해당 Rigidbody도 다시 계산에 포함될 수 있습니다.

스크립트에서 Rigidbody 상태를 직접 바꾸는 경우도 마찬가지입니다. 위치, 회전, 속도처럼 물리 상태에 영향을 주는 값을 변경하면 다음 물리 스텝에서 그 변화를 기준으로 다시 계산해야 합니다.

필요한 경우에는 `Rigidbody.WakeUp()`을 직접 호출해 Sleep 상태를 해제할 수도 있습니다. 이 메서드는 자동 해제 조건을 기다리지 않고 해당 Rigidbody를 Awake 상태로 되돌릴 때 사용합니다.

### Sleep을 방해하는 실수

Sleep은 Rigidbody가 일정 시간 동안 안정되어 있을 때 동작합니다. 코드가 매 물리 스텝마다 Rigidbody의 위치, 회전, 속도, 힘을 계속 바꾸면 PhysX는 그 Rigidbody를 안정된 상태로 판단하기 어렵습니다.

대표적인 예는 Rigidbody가 붙은 오브젝트의 `transform.position`을 직접 수정하는 코드입니다. 문제는 오브젝트가 움직인다는 사실 자체가 아니라, Rigidbody 위치를 물리 API가 아닌 Transform 대입으로 바꾼다는 점입니다. 이렇게 하면 PhysX가 관리하는 Rigidbody 상태와 스크립트가 바꾸는 Transform 상태가 어긋나기 쉽고, Sleep 판단도 의도와 다르게 동작할 수 있습니다.

다음 코드는 `FixedUpdate()`에서 Rigidbody의 Transform 위치를 직접 바꾸는 예입니다.

```csharp
void FixedUpdate()
{
    Vector3 nextPosition = transform.position + _velocity * Time.fixedDeltaTime;
    transform.position = nextPosition;
}
```

이 코드는 `FixedUpdate()`가 호출될 때마다 Transform 위치를 직접 바꿉니다. Rigidbody가 붙은 오브젝트의 위치를 이런 방식으로 계속 수정하면, 물리 엔진이 관리해야 할 위치를 스크립트가 반복해서 바꾸는 셈이 됩니다.

스크립트가 위치를 직접 정해 주는 오브젝트라면, 보통 Kinematic Rigidbody로 두고 `Rigidbody.MovePosition()`을 사용하는 편이 더 적절합니다. 아래 코드는 같은 이동을 Transform이 아니라 Rigidbody를 통해 전달하는 예입니다.

```csharp
void FixedUpdate()
{
    if (_velocity.sqrMagnitude == 0f)
    {
        return;
    }

    Vector3 nextPosition = _rb.position + _velocity * Time.fixedDeltaTime;
    // Kinematic Rigidbody의 다음 위치를 물리 엔진에 전달
    _rb.MovePosition(nextPosition);
}
```

이 방식은 Transform을 직접 덮어쓰지 않고, Rigidbody가 다음 물리 스텝에서 사용할 위치를 물리 엔진에 알려 줍니다.

움직이는 환경 오브젝트도 물리 엔진이 움직임을 추적할 수 있는 형태로 구성해야 합니다. Unity에서 Rigidbody 없이 Collider만 있는 오브젝트는 Static Collider로 취급됩니다. Static Collider는 움직이지 않는 충돌체를 전제로 하므로, 스크립트로 Transform을 바꿔도 Kinematic Rigidbody나 동적 Rigidbody의 이동과 같은 방식으로 처리되지 않습니다.

이 차이는 Sleep 상태의 Rigidbody와 함께 있을 때 특히 중요합니다.
대표적인 예는 중력의 영향을 받는 Rigidbody가 Rigidbody 없이 Collider만 가진 발판 위에서 Sleep 상태에 들어간 상황입니다.
이때 발판의 Transform만 이동시키면, 발판의 위치는 바뀌지만 그 위의 Rigidbody가 곧바로 Awake 상태로 돌아온다고 보장할 수 없습니다.
발판이 아래로 이동하거나 사라졌다면 중력의 영향을 받는 Rigidbody는 다시 아래로 움직여야 합니다. 그러나 Sleep 상태가 유지되면 중력과 접촉 상태에 대한 계산이 바로 다시 시작되지 않으므로, Rigidbody가 잠시 기존 위치에 남아 있는 것처럼 보일 수 있습니다.

움직이는 바닥이나 플랫폼처럼 다른 Rigidbody와 상호작용해야 하는 오브젝트는 Static Collider만으로 구성하지 않는 편이 좋습니다. Collider에 Kinematic Rigidbody를 함께 두면, 물리 엔진이 그 이동을 Rigidbody의 움직임으로 추적할 수 있습니다.

정리하면 Sleep을 활용하려면 Rigidbody의 상태 변화를 물리 엔진이 추적할 수 있어야 합니다. Rigidbody가 붙은 오브젝트의 Transform을 직접 수정하거나, 움직이는 Collider를 Static으로 처리하면 Sleep과 Wake Up 흐름이 의도와 다르게 동작할 수 있습니다.

<br>

---

## 물리 비용 확인하기

앞에서 살펴본 Fixed Timestep, Collider 형상, Broadphase, Sleep은 모두 물리 스텝의 CPU 비용으로 이어집니다. 실제 프로젝트에서는 원인을 짐작해 설정부터 바꾸기보다, Profiler와 Physics Debugger의 측정값으로 병목을 먼저 확인하는 편이 안전합니다.

Unity Profiler에서는 먼저 한 프레임 안에서 물리가 차지한 시간을 확인합니다.
`Physics.Processing`은 물리 처리에 사용된 전체 시간을 보여주므로, 이 값이 크면 물리 스텝이 프레임 시간을 많이 사용하고 있다는 뜻입니다.
그다음 하위 마커를 보면 비용이 PhysX 시뮬레이션, 접촉 처리, 보간 중 어느 쪽에 몰려 있는지 나누어 볼 수 있습니다.

---

## 마무리

- PhysX는 고정 타임스텝을 기준으로 물리 스텝을 실행하며, 한 스텝 안에서 힘 적용, 충돌 검출, 충돌 해소를 처리합니다.
- Fixed Timestep은 물리 스텝의 실행 빈도에 영향을 주고, Maximum Allowed Timestep은 프레임이 늦어졌을 때 한 번에 처리할 물리 시간을 제한합니다.
- Broadphase 비용은 충돌 후보가 될 Collider 조합의 수와 관련이 있고, Narrowphase 비용은 실제 충돌 검사를 수행하는 Collider 형상에 영향을 받습니다.
- Primitive Collider는 단순한 기본 형상이라 충돌 판별 비용이 낮은 편이며, MeshCollider는 더 정밀한 형상을 표현할 수 있지만 삼각형 구조 때문에 비용이 커지기 쉽습니다.
- Rigidbody Sleep은 안정된 Rigidbody를 반복 계산에서 제외해, 실제로 물리 스텝에서 갱신해야 하는 Rigidbody 수를 줄입니다.

물리 최적화에서는 먼저 Profiler와 Physics Debugger로 병목 위치를 확인해야 합니다. 충돌 후보가 많다면 필터링을, Collider 형상이 원인이라면 Collider 구성을, Awake 상태의 Rigidbody가 많다면 Sleep을 방해하는 코드가 없는지 점검해야 합니다.

[Part 2](/dev/unity/PhysicsOptimization-2/)에서는 Layer Collision Matrix, Physics.Simulate 수동 제어, Trigger 활용, NonAlloc 패턴처럼 실제 프로젝트에서 적용할 수 있는 물리 최적화 전략을 다룹니다.

<br>

---

**관련 글**
- [Unity의 Update, FixedUpdate 그리고 LateUpdate](/dev/unity/UpdateFunctions/)
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)

**시리즈**
- **물리 최적화 (1) - 물리 엔진의 실행 구조 (현재 글)**
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)

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
- **물리 최적화 (1) - 물리 엔진의 실행 구조** (현재 글)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
