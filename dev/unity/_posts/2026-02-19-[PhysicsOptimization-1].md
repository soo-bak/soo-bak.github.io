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

## GPU에서 CPU로

셰이더 복잡도, 오버드로우, 드로우 콜은 모두 GPU 측 비용입니다([GPU 아키텍처](/dev/unity/GPUArchitecture-1/), [렌더링 파이프라인](/dev/unity/RasterPipeline-1/)). 물리 연산은 GPU가 아니라 **CPU에서 실행**됩니다.

<br>

Unity의 프레임은 초기화, 물리, 입력, Update, 애니메이션, 렌더링 순서로 진행됩니다([게임 루프의 원리 (1)](/dev/unity/GameLoop-1/)). 물리 연산은 이 중 **물리 단계**에서 `FixedUpdate()` 콜백과 함께 처리됩니다.

물리 연산이 과도하면 CPU 측 프레임 예산을 소모합니다. 렌더링을 아무리 최적화해도, 물리 단계에서 시간을 너무 많이 쓰면 프레임 드롭이 발생합니다. 모바일 기기의 CPU는 데스크톱에 비해 처리 능력이 제한적이므로, 물리 비용의 영향이 더 큽니다.

<br>

---

## PhysX: Unity의 3D 물리 엔진

Unity의 3D 물리 시뮬레이션은 NVIDIA가 개발한 **PhysX** 엔진이 담당합니다. Unity에 내장되어 있으며, Rigidbody와 Collider 컴포넌트를 추가하면 자동으로 동작합니다.

PhysX는 매 물리 스텝마다 세 단계를 거칩니다.

<br>

```
PhysX의 물리 스텝 처리 과정

  (1) 힘 적용 (Force Integration)
      │  Rigidbody에 누적된 힘과 토크를 속도로 변환
      │  중력, AddForce(), 드래그 등을 반영
      │  → 새로운 속도 계산
      ▼
  (2) 충돌 검출 (Collision Detection)
      │  모든 콜라이더를 검사하여 겹치는 쌍을 찾음
      │  Broadphase → Narrowphase 두 단계로 진행
      │  → 접촉점(Contact Point)과 법선 벡터 계산
      ▼
  (3) 충돌 해소 (Constraint Solving)
      │  겹침을 해결하고 물체를 밀어냄
      │  반발 계수, 마찰 계수를 적용
      │  관절(Joint) 제약 조건 처리
      │  → 최종 위치와 회전 결정
```

<br>

힘 적용 단계에서는 Rigidbody의 속도가 갱신됩니다.

중력(`Physics.gravity`)은 모든 Rigidbody에 자동으로 적용되며, `AddForce()`나 `AddTorque()`로 추가한 힘도 이 단계에서 반영됩니다. Rigidbody의 **drag(저항)**와 **angularDrag(회전 저항)** 값이 속도를 감쇠시킵니다.

<br>

충돌 검출 단계에서는 물체끼리 겹쳤는지를 판별합니다. 물리 시뮬레이션에서 가장 큰 비용이 발생하는 단계이며, Broadphase와 Narrowphase 두 과정으로 나뉩니다.

<br>

충돌 해소 단계에서는 겹친 물체들을 물리 법칙에 따라 분리합니다. 두 물체가 충돌했을 때 어느 방향으로 얼마나 밀어낼지를 계산하는 과정으로, **PhysicMaterial**의 bounciness(반발 계수)와 friction(마찰 계수)이 이 계산에 반영됩니다.

이 세 단계가 하나의 **물리 스텝(Physics Step)**을 구성합니다.

<br>

---

## 고정 타임스텝 (Fixed Timestep)

### 물리가 고정 간격으로 실행되는 이유

`FixedUpdate()`는 고정된 시간 간격으로 호출됩니다([Update, FixedUpdate 그리고 LateUpdate](/dev/unity/UpdateFunctions/)).

물리 엔진은 매 스텝마다 운동 방정식을 수치 **적분(Integration)**하여 물체의 상태를 갱신합니다 — 힘에서 속도를, 속도에서 위치를 시간에 따라 누적하는 식입니다. 가장 단순한 형태로는 현재 속도 × 시간 간격을 현재 위치에 더하여 다음 위치를 구합니다. 시간 간격이 고정되어 있으면 매번 같은 크기의 갱신이 일어나므로, 동일한 초기 조건에서 항상 동일한 결과가 보장됩니다(**결정론적 안정성, Deterministic Stability**).

반면 시간 간격이 프레임마다 달라지면, 프레임 드롭으로 간격이 갑자기 커질 때 물체가 한 스텝에 큰 거리를 이동합니다. 얇은 벽을 뚫고 지나가거나(터널링), 관절에 연결된 물체가 급격히 튕겨나가는 현상이 발생할 수 있습니다.

<br>

```
가변 타임스텝으로 물리를 실행할 때의 문제

프레임 1: deltaTime = 0.008초  → 물체 이동 거리: 작음
프레임 2: deltaTime = 0.032초  → 물체 이동 거리: 큼
프레임 3: deltaTime = 0.010초  → 물체 이동 거리: 작음
프레임 4: deltaTime = 0.050초  → 물체 이동 거리: 가장 큼

→ 프레임 4에서 물체가 한 번에 큰 거리를 이동
→ 얇은 벽을 뚫고 지나갈 수 있음 (터널링)
→ 충돌 판정이 프레임마다 달라짐
```

<br>

Unity의 물리 엔진은 기본적으로 **0.02초(50Hz)** 간격으로 실행됩니다.

### 프레임과 물리 스텝의 관계

게임의 프레임률은 가변적이지만, 물리 스텝은 고정 간격입니다. 프레임 시간에 따라 한 프레임 안에서 물리 스텝이 몇 번 실행되는지가 달라집니다.

<br>

```
프레임률과 물리 스텝 호출 횟수 (Fixed Timestep = 0.02초)

프레임이 빠를 때 (프레임 시간 = 10ms):
  ┌── 프레임 1 ──┐┌── 프레임 2  ──┐┌── 프레임 3 ──┐
  │    10ms     ││    10ms      ││    10ms     │
  │ 물리 0회     ││ 물리 1회      ││ 물리 0회     │
  └─────────────┘└──────────────┘└─────────────┘
  │         20ms         │         20ms        │
  └── 물리 스텝 1 ────────┘── 물리 스텝 2 ────────┘

  → 누적 시간이 20ms에 도달할 때마다 물리 1회 실행
  → 프레임당 0회 또는 1회


프레임이 느릴 때 (프레임 시간 = 50ms):
  ┌──────────── 프레임 1 ────────────┐
  │              50ms               │
  │ 물리 스텝 1 → 물리 스텝 2          │
  └─────────────────────────────────┘

  → 한 프레임 안에서 물리 2회 실행
  → 밀린 시간을 따라잡기 위해 반복 호출
```

<br>

프레임이 오래 걸리면 한 프레임 안에서 물리 스텝이 여러 번 실행됩니다. Unity는 매 프레임의 경과 시간을 누적하고, 누적 시간이 고정 간격(0.02초) 이상인 동안 물리 스텝을 반복 실행하며 그때마다 0.02초를 차감합니다([게임 루프의 원리 (1)](/dev/unity/GameLoop-1/)). 프레임이 50ms 걸렸다면 누적 시간 50ms에서 20ms씩 두 번 차감되어 물리 스텝이 2회 실행됩니다.

### Maximum Allowed Timestep

프레임이 극도로 느려지면(예: 200ms) 한 프레임 안에서 물리 스텝이 10회 이상 실행될 수 있습니다. 이렇게 되면 물리 연산이 CPU 시간을 독점하고, 다음 프레임은 더 늦어지고, 그래서 물리 스텝이 더 많이 쌓이는 악순환에 빠집니다.

<br>

```
물리 스텝 폭주 시나리오

프레임 시간: 200ms, Fixed Timestep: 20ms

→ 물리 스텝 10회 실행
→ 물리에 CPU 시간 소진
→ 다음 프레임 더 느려짐 (250ms)
→ 물리 스텝 12회 실행
→ 악순환 (Spiral of Death)
```

<br>

이 악순환을 막기 위해 Unity는 **Maximum Allowed Timestep**(기본값 0.333초)을 제공합니다. 한 프레임에서 물리에 소비할 수 있는 최대 시간을 제한하는 설정입니다. 이 값을 초과하면 남은 물리 스텝은 건너뜁니다. 물리 시뮬레이션이 실시간보다 느리게 진행되는 현상이 발생하지만, 게임 전체가 멈추는 것은 방지할 수 있습니다.

모바일 기기는 CPU가 느려 물리 스텝 폭주 시 프레임 드롭이 데스크톱보다 심각해지므로, Maximum Allowed Timestep을 기본값보다 낮추면 폭주를 더 빠르게 차단할 수 있습니다.

<br>

---

## 충돌 검출: Broadphase와 Narrowphase

### 두 단계로 나누는 이유

PhysX의 물리 스텝에서 충돌 검출이 가장 큰 비용을 차지합니다. 오브젝트 수가 늘어나면 검사해야 할 조합의 수가 급격히 증가하기 때문입니다. 씬에 콜라이더가 n개 있으면, 모든 쌍을 검사하는 비용은 O(n^2)입니다. 콜라이더 100개면 4,950쌍, 1,000개면 약 50만 쌍이 됩니다.

<br>

```
콜라이더 수에 따른 쌍의 수 (n × (n-1) / 2)

콜라이더 수       검사해야 할 쌍의 수
─────────────────────────────────────
       10                  45
       50               1,225
      100               4,950
      500             124,750
    1,000             499,500
```

<br>

50만 쌍 각각에 대해 정밀한 기하학적 충돌 검사를 수행하는 것은 비현실적입니다. 그래서 PhysX는 충돌 검출을 두 단계로 나누어, 실제로 충돌할 가능성이 있는 쌍만 정밀 검사합니다.

### Broadphase: 후보 쌍 필터링

Broadphase는 정밀한 형상 검사 전에, 두 콜라이더가 서로 가까이 있는지를 먼저 빠르게 판별하는 단계입니다. 각 콜라이더를 **AABB(Axis-Aligned Bounding Box, 축 정렬 경계 상자)** — 콜라이더를 완전히 감싸는 축 정렬 직육면체 — 로 감싸고, 이 직육면체끼리 겹치는지만 비교합니다.

AABB는 축에 정렬되어 있으므로, 겹침 판별이 x, y, z 각 축의 최솟값과 최댓값 비교만으로 끝납니다. 실제 콜라이더의 삼각형이나 곡면을 계산하는 것에 비해 훨씬 빠르고, 콜라이더의 형상이 복잡해져도 AABB 비교 비용은 동일합니다.

<br>

```
AABB 겹침 검사

겹치지 않음 → 정밀 검사 생략:
  ┌──────┐        ┌──────┐
  │  A   │        │  B   │
  └──────┘        └──────┘

겹침 → 후보 쌍 등록, Narrowphase로 전달:
  ┌──────┐
  │  A ┌─┼────┐
  └────┼─┘ B  │
       └──────┘

겹침 조건 — 모든 축에서 동시에 범위가 겹쳐야 함:
  A.min.x ≤ B.max.x  AND  A.max.x ≥ B.min.x
  A.min.y ≤ B.max.y  AND  A.max.y ≥ B.min.y
  A.min.z ≤ B.max.z  AND  A.max.z ≥ B.min.z
```

<br>

AABB가 겹치지 않으면 두 콜라이더는 절대 충돌하지 않으므로, 정밀 검사를 건너뛸 수 있습니다. 게임 씬에서 대부분의 콜라이더 쌍은 서로 멀리 떨어져 있으므로, Broadphase에서 대다수의 쌍이 걸러집니다.

<br>

PhysX는 내부적으로 공간을 분할하는 알고리즘을 사용하여 O(n^2)보다 효율적으로 겹치는 AABB 쌍을 찾습니다.

**SAP(Sweep and Prune)**는 모든 AABB의 시작점과 끝점을 한 축 위에 정렬한 뒤, 왼쪽부터 훑으며 구간이 겹치는 AABB끼리만 다른 축을 추가로 비교하는 방식입니다. 한 축에서 이미 떨어진 쌍은 비교 자체를 건너뛰므로, 멀리 있는 오브젝트 쌍이 대부분인 씬에서 검사 횟수가 크게 줄어듭니다.

**MBP(Multi Box Pruning)**는 공간을 격자로 나누고, 각 AABB가 속한 격자 칸을 기록하여 같은 칸을 공유하는 AABB끼리만 비교하는 방식입니다. 서로 다른 칸에 있는 AABB는 겹칠 수 없으므로 비교 대상에서 제외됩니다.

### Narrowphase: 정밀 충돌 검사

Broadphase에서 AABB가 겹치는 것으로 판별된 쌍에 대해서만 Narrowphase가 실행됩니다. Narrowphase는 콜라이더의 **실제 형상**을 기반으로 정밀한 충돌 검사를 수행합니다.

<br>

```
Broadphase → Narrowphase 흐름

  씬의 전체 콜라이더: 500개 (약 125,000쌍)
          │
          ▼
  ┌─────────────────────────┐
  │      Broadphase          │
  │  AABB 겹침 검사          │
  │  (축 범위 비교, 빠름)    │
  └─────────────────────────┘
          │
          │  AABB가 겹치는 쌍: 약 200쌍  (99.8% 제거)
          ▼
  ┌─────────────────────────┐
  │      Narrowphase         │
  │  정밀 형상 검사           │
  │  (기하학적 계산, 느림)    │
  └─────────────────────────┘
          │
          │  실제 충돌 쌍: 약 30쌍
          ▼
  충돌 해소 (Constraint Solving)
```

<br>

Narrowphase에서 실제로 충돌한 쌍에 대해 **접촉점(Contact Point)**과 **접촉 법선(Contact Normal)**이 계산되며, 충돌 해소 단계에서는 이 정보를 바탕으로 물체를 밀어내는 방향과 크기를 결정합니다. `OnCollisionEnter`의 `Collision` 파라미터가 제공하는 `contacts` 배열이 이 접촉점 정보입니다.

### Broadphase 비용이 증가하는 조건

Broadphase의 비용은 씬에 존재하는 **활성 콜라이더의 총 수**에 비례합니다. 콜라이더가 많으면 AABB 겹침 검사의 대상이 늘어나고, 공간 분할 자료구조를 갱신하는 비용도 증가합니다.

특히 **움직이는 콜라이더**는 매 물리 스텝마다 AABB가 갱신됩니다. 정적 콜라이더(Static Collider)는 위치가 변하지 않으므로 AABB를 한 번만 계산하면 됩니다. 반면 Rigidbody가 부착된 동적 콜라이더는 매 스텝마다 새 위치에 맞게 AABB를 다시 계산하고, 공간 분할 자료구조에 다시 삽입해야 합니다.

<br>

```
정적 콜라이더 vs 동적 콜라이더의 Broadphase 비용

정적 콜라이더 (Rigidbody 없음):
  - AABB 한 번 계산 후 고정
  - Broadphase 자료구조에 한 번 삽입
  - 이후 스텝에서 갱신 비용 없음

동적 콜라이더 (Rigidbody 있음):
  - 매 물리 스텝마다 AABB 재계산
  - Broadphase 자료구조 갱신
  - 오브젝트가 빠르게 움직이면 AABB가 크게 변하여
    후보 쌍의 수도 늘어남
```

<br>

씬에 정적 배경 오브젝트가 수백 개 있어도, 움직이지 않으면 Broadphase 부하는 크지 않습니다. 하지만 Rigidbody가 부착된 동적 오브젝트가 수백 개라면, Broadphase의 매 스텝 갱신 비용이 상당해집니다.

---

## 콜라이더 종류별 비용

Broadphase가 콜라이더의 수에 따라 비용이 결정되는 반면, Narrowphase의 비용은 콜라이더의 **형상(Shape)** 종류에 따라 크게 달라집니다. PhysX가 지원하는 콜라이더는 크게 **Primitive 콜라이더**와 **Mesh 콜라이더**로 나뉩니다.

### Primitive 콜라이더

Box, Sphere, Capsule 콜라이더는 **수학적 공식**으로 충돌을 판별합니다.

<br>

```
Primitive 콜라이더의 충돌 판별

Sphere vs Sphere:
  두 중심 사이의 거리 < 반지름의 합
  → 거리 계산 한 번으로 판별 완료

Box vs Box:
  분리 축 정리(SAT: Separating Axis Theorem) 적용
  → 최대 15개 축에 대한 투영 비교
  → 여전히 고정된 수의 연산

Capsule vs Capsule:
  선분 사이의 최소 거리 계산
  → 닫힌 형태의 수학 공식으로 해결
```

<br>

Primitive 콜라이더는 오브젝트가 크든 작든 검사에 필요한 연산 수가 고정되어 있으므로, 충돌 검사 비용이 **일정**합니다.

### MeshCollider

MeshCollider는 3D 모델의 메쉬 형상을 그대로 콜라이더로 사용합니다. 정밀한 충돌 판정이 가능하지만, 비용이 Primitive에 비해 훨씬 큽니다.

<br>

```
MeshCollider의 충돌 판별

Non-Convex MeshCollider:
  메쉬의 모든 삼각형을 대상으로 상대 콜라이더와의 교차 검사 수행
  삼각형 500개 메쉬 → 최대 500번의 삼각형-형상 교차 검사
  (내부적으로 BVH로 가속하지만 여전히 Primitive보다 훨씬 비쌈)

Convex MeshCollider:
  볼록 껍질(Convex Hull)로 단순화, 최대 255개 정점으로 제한
  GJK 알고리즘으로 충돌 판별
  Non-Convex보다 빠르지만 여전히 Primitive보다 비쌈
```

<br>

Non-Convex MeshCollider는 오목한 형상도 표현할 수 있지만, 삼각형 단위로 충돌 검사를 수행하므로 메쉬의 삼각형 수에 비례하여 비용이 증가합니다. PhysX 내부적으로 **BVH(Bounding Volume Hierarchy)**를 사용하여 검사 대상 삼각형을 좁힙니다. BVH는 삼각형들을 트리 구조로 묶어서, 충돌 가능성이 없는 삼각형 그룹을 빠르게 건너뛰는 가속 구조입니다. 이 가속이 있더라도 고정 연산인 Primitive 콜라이더보다 훨씬 높은 비용이 발생합니다.

<br>

Convex MeshCollider는 메쉬를 볼록 껍질(Convex Hull)로 변환하여 **GJK(Gilbert-Johnson-Keerthi)** 알고리즘으로 충돌을 판별합니다. GJK는 두 볼록 도형 사이의 최소 거리를 반복적으로 좁혀가며 겹침 여부를 판단하는 알고리즘으로, 삼각형을 개별적으로 검사하는 것보다 효율적입니다. Non-Convex보다 빠르지만 Primitive보다는 여전히 비용이 높습니다. 또한 Convex 변환 과정에서 원래 메쉬의 오목한 부분이 채워지므로, 형상이 달라질 수 있습니다.

### 콜라이더 비용 비교

```
콜라이더 종류별 Narrowphase 비용 비교

종류                     비용            비고
──────────────────────────────────────────────────────────
Sphere                   가장 낮음       거리 비교 한 번
Capsule                  낮음            선분 거리 계산
Box                      낮음            분리 축 비교
Convex MeshCollider      중간            GJK 알고리즘
Non-Convex MeshCollider  높음            삼각형 단위 검사
```

<br>

게임에서는 복잡한 형상의 오브젝트도 Primitive 콜라이더의 **조합**으로 근사할 수 있습니다. 캐릭터의 몸통을 Capsule로, 무기를 Box로, 방패를 Sphere로 표현하는 식입니다. 여러 Primitive를 조합한 **Compound Collider**는 MeshCollider 하나보다 대부분의 경우 비용이 낮습니다.

<br>

```
MeshCollider vs Compound Collider

MeshCollider (삼각형 2,000개):
  메쉬 형상 그대로 사용 → 정밀하지만 비용 높음

Compound Collider (Primitive 조합):
     ○  ← Sphere (머리)
     ┃  ← Capsule (몸통)
    ╱╲  ← Box 2개 (다리)
  → 근사적이지만 비용 낮음
```

<br>

지형(Terrain)이나 복잡한 정적 환경 오브젝트처럼, Primitive로 근사하기 어렵고 정밀한 충돌이 필요한 경우에는 MeshCollider가 필요합니다. 이런 경우에도 Non-Convex MeshCollider는 물리 힘으로 움직이는 Rigidbody(non-kinematic)와 함께 사용할 수 없다는 제약이 있습니다. 동적 오브젝트에는 Convex MeshCollider나 Primitive 조합을 사용해야 합니다.

<br>

---

## Rigidbody Sleep

### Sleep 상태란

물리 씬에 Rigidbody가 많더라도, 모든 Rigidbody가 항상 물리 연산에 참여하지는 않습니다. PhysX는 **충분히 오랜 시간 동안 거의 움직이지 않는 Rigidbody**를 **Sleep 상태**로 전환합니다.

Sleep 상태의 Rigidbody는 물리 시뮬레이션에서 제외됩니다. 힘 적용, 충돌 검출, 충돌 해소의 모든 단계를 건너뜁니다. Broadphase에서도 이 Rigidbody는 동적 오브젝트가 아닌 정적 오브젝트처럼 취급되어 매 스텝 AABB 갱신이 발생하지 않습니다.

<br>

```
Sleep 상태의 효과

씬에 Rigidbody 200개가 있는 경우:

  활성(Awake) Rigidbody: 30개
   → 매 물리 스텝마다 힘 적용, 충돌 검출, 충돌 해소 수행

  수면(Sleep) Rigidbody: 170개
   → 물리 연산 완전 제외, CPU 비용 0

  → 실질적인 물리 비용은 30개 기준으로 산정됨
```

### Sleep 전환 조건

Rigidbody가 Sleep으로 전환되는 조건은 **에너지 기반**입니다. Rigidbody의 운동 에너지(선속도와 각속도로 계산)가 **Sleep Threshold** 값보다 작은 상태가 일정 시간 동안 지속되면 Sleep으로 전환됩니다.

<br>

```
Sleep 전환 과정

                  운동 에너지
                      │
  Sleep Threshold ────┼──────────────────────────────
                      │
                      │╲
                      │ ╲    ╱╲
                      │  ╲  ╱  ╲
                      │   ╲╱    ╲_______ → Sleep!
                      │
                      └─────────────────────────► 시간

  운동 에너지가 Sleep Threshold 아래로 유지되는 시간이
  충분히 길면 Sleep 상태로 전환
```

<br>

Sleep Threshold는 `Rigidbody.sleepThreshold` 프로퍼티로 개별 Rigidbody마다 설정할 수 있고, `Physics Settings → Sleep Threshold`에서 전역 기본값을 설정할 수 있습니다. 기본값은 0.005입니다.

### Sleep 해제 조건

Sleep 상태의 Rigidbody는 다음 조건 중 하나가 발생하면 깨어납니다.

<br>

```
Sleep 해제 조건

(1) 외력 적용
    → AddForce(), AddTorque() 호출
    → 중력 제외 (Sleep 상태에서는 중력도 적용되지 않음)

(2) 충돌
    → 다른 활성 Rigidbody가 부딪힘
    → 활성 오브젝트가 Sleep 오브젝트를 밀어냄

(3) Transform 직접 변경
    → transform.position이나 transform.rotation을
      스크립트에서 직접 변경
    → Rigidbody.MovePosition()이나
      Rigidbody.MoveRotation() 호출

(4) 관절(Joint) 연결된 오브젝트가 깨어남
    → Joint로 연결된 다른 Rigidbody가 활성화되면
      함께 깨어남

(5) 명시적 호출
    → Rigidbody.WakeUp() 메서드 호출
```

### Sleep을 방해하는 실수

Sleep 메커니즘은 자동으로 동작하지만, 코드에서 의도치 않게 Sleep을 방해하는 패턴이 있습니다.

대표적인 실수는 `FixedUpdate()`에서 매 스텝 Rigidbody의 `transform.position`에 값을 직접 할당하는 것입니다. `transform.position`에 값을 할당하면 Rigidbody가 깨어납니다. `AddForce()`나 `Rigidbody.MovePosition()`은 물리 엔진을 통해 이동하므로 속도가 0이 되면 자연스럽게 Sleep에 진입합니다.

<br>

또 다른 실수는 극히 작은 힘을 지속적으로 가하는 것입니다. 눈에 보이지 않을 정도의 미세한 힘이라도 `AddForce()`로 가해지면 Rigidbody가 깨어납니다. 바람 효과나 잔잔한 물결 같은 미세한 힘을 모든 오브젝트에 매 스텝 적용하면, Sleep 상태에 들어갈 수 있는 오브젝트가 영원히 깨어 있게 됩니다.

<br>

**[문제]** transform.position 직접 수정:

```csharp
void FixedUpdate() {
    transform.position += velocity * Time.fixedDeltaTime;
}
```

매 스텝 Rigidbody가 깨어나므로 Sleep이 불가능합니다.

<br>

**[개선]** Rigidbody API 사용:

```csharp
void FixedUpdate() {
    _rb.MovePosition(_rb.position + velocity * Time.fixedDeltaTime);
}
```

MovePosition은 물리 엔진을 통해 이동하므로, 속도가 0이 되면 자연스럽게 Sleep에 진입합니다.

<br>

Sleep 메커니즘이 정상적으로 동작하면, 씬에 Rigidbody가 수백 개 있더라도 실제로 물리 연산에 참여하는 오브젝트는 소수에 불과합니다. 별도의 코드 없이 물리 비용을 줄이는 내장 메커니즘이지만, `transform.position` 직접 수정이나 미세한 힘의 지속 적용이 이 메커니즘을 무력화합니다.

<br>

---

## 물리 프로파일링의 기초

Unity Profiler와 Physics Debugger로 물리가 프레임 예산을 얼마나 차지하는지 확인할 수 있습니다.

<br>

```
물리 관련 Profiler 마커

Physics.Processing     ← 물리 시뮬레이션 전체 시간
Physics.Simulate       ← PhysX 내부 시뮬레이션
Physics.Contacts       ← 접촉점 처리
Physics.Interpolation  ← 보간 처리

Physics Debugger 항목:
  - 활성 Rigidbody 수
  - Sleep 상태 Rigidbody 수
  - 접촉 쌍의 수
  - 콜라이더 종류별 수
```

<br>

30fps 기준(33.3ms 예산)에서 `Physics.Processing`이 5ms 이상을 차지하면 물리 비용이 프레임 예산에서 상당한 비중을 차지하는 상태입니다.

Physics Debugger에서 활성 Rigidbody 수와 Sleep 상태의 비율을 확인하면 Sleep이 정상적으로 동작하는지 점검할 수 있고, 프로파일러 수치를 통해 병목이 Broadphase에 있는지, Narrowphase에 있는지, Sleep이 제대로 작동하지 않는 것인지를 판별할 수 있습니다.

---

## 구조에서 전략으로

각 최적화 전략은 이 실행 구조의 특정 단계에 대응합니다.

Layer Collision Matrix는 Broadphase 단계에서 검사 대상 쌍 자체를 줄이고, Trigger는 Narrowphase 이후의 충돌 해소 단계를 생략합니다.

[Part 2](/dev/unity/PhysicsOptimization-2/)에서는 Layer Collision Matrix, Physics.Simulate 수동 제어, 2D/3D 물리 선택, Trigger 활용, NonAlloc 패턴 등 구체적인 최적화 전략을 다룹니다.

---

## 마무리

- PhysX는 매 고정 타임스텝마다 힘 적용, 충돌 검출, 충돌 해소를 순서대로 수행합니다.
- 고정 타임스텝(기본 0.02초)은 시뮬레이션의 결정론적 안정성을 보장하며, Maximum Allowed Timestep(기본 0.333초)은 물리 스텝 폭주를 방지합니다.
- 충돌 검출은 AABB 기반 Broadphase와 정밀 형상 기반 Narrowphase로 나뉘며, 오브젝트 수에 따라 Broadphase, 콜라이더 형상에 따라 Narrowphase 비용이 증가합니다.
- Primitive 콜라이더(Sphere, Box, Capsule)는 고정 비용이고, MeshCollider는 삼각형 수에 비례하는 비용이 발생합니다.
- Rigidbody Sleep은 비활성 오브젝트를 물리 연산에서 자동으로 제외하여 CPU 비용을 절감합니다.

물리 최적화는 이 구조의 각 단계에서 비용을 줄이는 것입니다. 어느 단계가 병목인지를 Profiler로 확인하고, 해당 단계에 맞는 전략을 적용해야 합니다.

[Part 2](/dev/unity/PhysicsOptimization-2/)에서는 Layer Collision Matrix, Physics.Simulate 수동 제어, Trigger 활용, NonAlloc 패턴 등 구체적인 최적화 전략을 다룹니다.

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
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- **물리 최적화 (1) - 물리 엔진의 실행 구조** (현재 글)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
