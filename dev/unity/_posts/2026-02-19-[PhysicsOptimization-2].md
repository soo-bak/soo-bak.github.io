---
layout: single
title: "물리 최적화 (2) - 물리 최적화 전략 - soo:bak"
date: "2026-02-19 22:50:00 +0900"
description: Layer Matrix, Physics.Simulate, 2D vs 3D 물리, Trigger vs Collider, NonAlloc 패턴을 설명합니다.
tags:
  - Unity
  - 최적화
  - 물리
  - 충돌
  - 모바일
---

## Broadphase의 부담을 줄이는 방법

[물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)에서 PhysX의 충돌 검출 과정을 다루었습니다.

Broadphase는 씬의 모든 활성 콜라이더를 서로 비교하여 AABB가 겹치는 후보 쌍을 찾고, Narrowphase가 후보 쌍의 실제 형상으로 정밀 검사를 수행합니다. 콜라이더가 100개이면 잠재적인 쌍은 약 5,000개, 400개이면 약 80,000개입니다. 공간 분할 알고리즘이 실제 비교 횟수를 줄여주지만, 콜라이더가 늘어날수록 비용은 급격히 증가합니다.

<br>

콜라이더 형상 선택(Primitive vs MeshCollider)과 Rigidbody Sleep은 개별 오브젝트의 연산을 가볍게 만들지만, 이 쌍의 수 자체는 줄이지 못합니다.

검사 대상 쌍을 줄이는 것이 가장 직접적인 해결책이며, Layer Collision Matrix가 이 역할을 합니다.

<br>

---

## Layer Collision Matrix

### 레이어 간 충돌 비활성화

Unity의 모든 게임 오브젝트는 하나의 **레이어(Layer)**에 속합니다. `Project Settings → Physics → Layer Collision Matrix`에서 어떤 레이어 쌍이 서로 충돌할지를 설정합니다.

기본 상태에서는 모든 레이어 쌍이 활성화되어 있으므로, Broadphase가 발견한 겹침 후보가 전부 Narrowphase로 진행됩니다. 특정 레이어 쌍의 체크를 해제하면, Broadphase에서 AABB가 겹치더라도 **해당 쌍은 Narrowphase로 전달되지 않으므로 정밀 검사와 충돌 해소가 모두 생략됩니다.**

<br>

```
Layer Collision Matrix 예시

레이어 구성:
  0: Default
  8: Player
  9: Enemy
  10: Bullet
  11: UI
  12: Pickup
  13: Environment

충돌이 필요한 쌍:
  Player   ↔ Enemy         (캐릭터가 적과 충돌)
  Player   ↔ Environment   (캐릭터가 지형과 충돌)
  Player   ↔ Pickup        (캐릭터가 아이템 획득)
  Enemy    ↔ Environment   (적이 지형과 충돌)
  Bullet   ↔ Enemy         (총알이 적에 명중)
  Bullet   ↔ Environment   (총알이 벽에 부딪힘)

충돌이 불필요한 쌍 (체크 해제):
  Player   ↔ Bullet        (자신의 총알과 충돌 불필요)
  Enemy    ↔ Enemy         (적끼리 충돌 불필요)
  Enemy    ↔ Pickup        (적이 아이템 획득 불필요)
  Bullet   ↔ Bullet        (총알끼리 충돌 불필요)
  Bullet   ↔ Pickup        (총알과 아이템 충돌 불필요)
  UI       ↔ (모든 레이어)  (UI는 물리 충돌 불필요)
  Pickup   ↔ Pickup        (아이템끼리 충돌 불필요)
```

<br>

### 비용 감소 원리

Layer Collision Matrix는 Broadphase의 AABB 비교 자체를 줄이지는 않습니다. 줄어드는 것은 Narrowphase입니다. 비활성화된 쌍은 정밀 형상 검사와 충돌 해소를 건너뛰는데, Narrowphase는 AABB 비교보다 연산 비용이 높으므로 건너뛰는 쌍이 많을수록 절감 효과가 큽니다.

<br>

```
Layer Collision Matrix 적용 전후 비교

씬 구성:
  Player(1개), Enemy(50개), Bullet(100개),
  Pickup(20개), Environment(200개), UI(30개)
  = 총 401개 콜라이더

적용 전 (모든 레이어 쌍 활성):
  잠재적 쌍: 약 80,000쌍

적용 후 (필요한 쌍만 활성):
  Player↔Enemy:       50쌍
  Player↔Env:        200쌍
  Player↔Pickup:      20쌍
  Enemy↔Env:      10,000쌍
  Bullet↔Enemy:    5,000쌍
  Bullet↔Env:     20,000쌍
  합계: 약 35,000쌍

→ 약 45,000쌍(56%)의 Narrowphase 검사 생략
```

<br>

오브젝트 수가 많은 레이어의 불필요한 쌍일수록 비활성화 효과가 큽니다. 같은 레이어 내 자기 충돌(Bullet↔Bullet 등)은 해당 레이어의 오브젝트 수가 늘어날수록 쌍이 급격히 증가하므로, 게임 로직에 불필요하다면 비활성화하는 것이 효과적입니다.

<br>

### 설정 전략

Layer Collision Matrix를 설정할 때는 **먼저 모든 쌍을 비활성화한 뒤, 필요한 쌍만 활성화**합니다. 모두 활성인 기본 상태에서 하나씩 끄면 불필요한 쌍을 놓치기 쉽지만, 모두 끈 상태에서 시작하면 게임 로직에 필요한 최소한의 쌍만 남길 수 있습니다.

<br>

레이어를 설계할 때 물리 충돌 여부를 함께 고려하면 Matrix 설정이 단순해집니다. 같은 역할의 오브젝트를 같은 레이어에 모으면 설정할 쌍의 수가 줄어듭니다. 환경 오브젝트를 하나의 Environment 레이어에 모으면 Player↔Environment 한 쌍만 설정하면 되지만, "바닥", "벽", "천장" 레이어로 분리하면 각각에 대해 따로 설정해야 합니다.

<br>

---

## Physics.Simulate 수동 제어

### 자동 시뮬레이션의 비용

Layer Collision Matrix로 불필요한 쌍을 제거해도, 기본 설정에서 Unity의 물리 시뮬레이션은 **자동으로 실행**됩니다. `FixedUpdate()` 타이밍에 맞춰 PhysX가 매 고정 타임스텝마다 시뮬레이션을 수행하며, 물리가 필요하든 필요하지 않든 매 스텝 비용이 발생합니다.

<br>

메뉴 화면, 대화 장면, 컷씬, 인벤토리 화면에서는 물리 시뮬레이션이 필요 없습니다. 하지만 자동 시뮬레이션이 켜져 있으면 이런 장면에서도 PhysX가 매 스텝 동작합니다.

<br>

### 수동 시뮬레이션 전환

`Physics.simulationMode`를 `SimulationMode.Script`로 설정하면 Unity가 자동으로 물리를 실행하지 않습니다. 개발자가 원하는 시점에 `Physics.Simulate()`를 직접 호출하여 물리 스텝을 실행합니다.

<br>

```
자동 시뮬레이션 vs 수동 시뮬레이션

자동 시뮬레이션 (기본):
  FixedUpdate 타이밍마다 자동으로 물리 실행

  프레임 1:  물리 ✓  물리 ✓
  프레임 2:  물리 ✓
  프레임 3:  물리 ✓  물리 ✓  물리 ✓
  (메뉴 화면 진입)
  프레임 4:  물리 ✓  ← 필요 없는데 실행
  프레임 5:  물리 ✓  ← 필요 없는데 실행

수동 시뮬레이션 (SimulationMode.Script):
  Physics.Simulate()를 호출한 시점에만 물리 실행

  프레임 1:  Physics.Simulate(0.02f) 호출
  프레임 2:  Physics.Simulate(0.02f) 호출
  프레임 3:  Physics.Simulate(0.02f) 호출
  (메뉴 화면 진입)
  프레임 4:  호출 안 함  ← 물리 비용 0
  프레임 5:  호출 안 함  ← 물리 비용 0
```

<br>

### 수동 시뮬레이션의 활용

수동 시뮬레이션의 핵심은 `Physics.Simulate()` 호출 빈도를 게임 상황에 맞게 조절하는 것입니다.

<br>

턴제 게임에서 플레이어가 행동을 선택하는 동안, 퍼즐 게임에서 다음 수를 고민하는 동안 물체는 움직이지 않습니다. 이 구간에서 `Physics.Simulate()`를 호출하지 않으면 물리 연산이 완전히 사라집니다. 공격이 발동되거나 블록이 떨어지는 순간에만 호출하면 됩니다.

실시간 액션 게임에서도 모든 프레임에 같은 물리 비용이 필요하지는 않습니다. 전투 구간에서는 매 프레임 물리를 실행하되, 이동만 하는 구간에서는 2프레임에 1번만 호출하면 물리 연산이 절반으로 줄어듭니다.

<br>

```csharp
// 상황별 시뮬레이션 빈도 조절

void Update() {
    if (_currentScene == SceneType.Menu) {
        // 메뉴: 물리 불필요
        return;
    }

    if (_currentScene == SceneType.Combat) {
        // 전투: 매 프레임
        Physics.Simulate(Time.fixedDeltaTime);
    }

    if (_currentScene == SceneType.Exploration) {
        // 탐색: 2프레임에 1번
        _accumulator += Time.deltaTime;
        if (_accumulator >= Time.fixedDeltaTime * 2f) {
            Physics.Simulate(Time.fixedDeltaTime);
            _accumulator -= Time.fixedDeltaTime * 2f;
        }
    }
}
```

메뉴에서는 물리 비용이 0이 되고, 탐색에서는 절반, 전투에서만 전체 비용이 발생합니다.

<br>

자동 시뮬레이션에서는 `FixedUpdate()` 직후에 PhysX가 충돌 검출과 Rigidbody/Joint 적분을 수행하고, 그 결과로 물리 콜백(`OnCollisionEnter`, `OnTriggerEnter` 등)이 호출됩니다.

수동 시뮬레이션에서는 이 전체 과정이 `Physics.Simulate()` 호출 안으로 옮겨집니다. `Update()`에서 `Physics.Simulate()`를 호출하면 충돌 검출부터 콜백 발생까지 모두 `Update()` 안에서 실행됩니다. 콜백이 `FixedUpdate()` 직후에 실행되는 것을 전제한 코드가 있다면 동작이 달라질 수 있습니다.

<br>

---

## 2D 물리와 3D 물리

### 두 개의 독립된 물리 엔진

지금까지 다룬 Layer Collision Matrix와 수동 시뮬레이션은 물리 엔진의 작업량을 줄이는 전략이었습니다. 게임의 차원에 맞는 물리 엔진을 선택하는 것도 비용에 영향을 미칩니다.

Unity에는 3D 물리 엔진(PhysX)과 2D 물리 엔진(Box2D)이 **별도로** 존재합니다. 두 엔진은 완전히 독립적이며, 각각 고유한 콜라이더와 Rigidbody 컴포넌트를 사용합니다.

<br>

```
Unity의 두 물리 엔진

3D 물리 (PhysX)              2D 물리 (Box2D)

BoxCollider                  BoxCollider2D
SphereCollider               CircleCollider2D
CapsuleCollider              CapsuleCollider2D
MeshCollider                 PolygonCollider2D
Rigidbody                    Rigidbody2D

→ 두 엔진은 독립 — 3D 콜라이더와 2D 콜라이더는 서로 충돌하지 않음
```

<br>

### 2D 게임에서 3D 물리를 사용하면 생기는 문제

2D 게임에서 3D 물리(Rigidbody, BoxCollider 등)를 사용하는 경우가 있습니다. 기능적으로 동작하지만, PhysX는 모든 연산을 3차원(x, y, z)으로 수행하므로 z축 계산이 낭비됩니다.

<br>

```
2D 게임에서 3D vs 2D 물리 비교

                  3D 물리 (PhysX)      2D 물리 (Box2D)

연산 차원          x, y, z              x, y
AABB 비교         6개 범위              4개 범위
충돌 해소         3축 법선/접촉점        2축 법선/접촉점
z축 드리프트       발생 가능             해당 없음
```

3D 물리를 사용하면 비용만 낭비되는 것이 아니라, 충돌 해소 과정에서 오브젝트가 z축으로 미세하게 밀려나는 문제도 발생할 수 있습니다. 2D 게임이라면 2D 물리 컴포넌트를 사용하는 것이 같은 결과를 내면서 불필요한 연산을 제거하는 방법입니다.

<br>

### 2D 물리에서의 적용

이 글에서 다루는 최적화 전략은 2D 물리에도 동일하게 적용됩니다. 원리는 같고, API 이름만 다릅니다.

<br>

```
3D → 2D API 대응

Layer Collision Matrix
  3D: Project Settings → Physics
  2D: Project Settings → Physics 2D

수동 시뮬레이션
  3D: Physics.simulationMode / Physics.Simulate()
  2D: Physics2D.simulationMode / Physics2D.Simulate()

NonAlloc 쿼리
  3D: Physics.RaycastNonAlloc(), Physics.OverlapSphereNonAlloc() 등
  2D: Physics2D.RaycastNonAlloc(), Physics2D.OverlapCircleNonAlloc(),
      Physics2D.OverlapBoxNonAlloc() 등

Sleep
  3D: Rigidbody
  2D: Rigidbody2D
```

`Physics2D.simulationMode`를 `Script`로 설정하면, 메뉴 화면이나 대화 장면처럼 2D 물리가 불필요한 구간에서 시뮬레이션을 건너뛸 수 있습니다. Rigidbody2D에도 Sleep 메커니즘이 있으므로, 오래 움직이지 않는 2D 오브젝트는 자동으로 물리 계산이 일시중지됩니다. NonAlloc 쿼리는 3D와 마찬가지로 힙 할당 없이 2D 물리 쿼리를 수행합니다.

<br>

---

## Trigger vs Collider

### 물리적 반응의 유무

앞에서 물리 엔진의 작업량을 줄이고 올바른 엔진을 선택하는 전략을 다루었습니다. 개별 콜라이더 수준에서도 비용을 줄일 수 있습니다.

콜라이더에는 **일반 콜라이더(Collider)**와 **트리거(Trigger)** 두 가지 모드가 있으며, `Is Trigger` 체크박스로 전환합니다.

<br>

일반 콜라이더는 물리적 반응을 수반합니다. 두 물체가 겹치면 PhysX가 충돌 해소(Constraint Solving)를 실행합니다. 접촉점을 계산하고, 물체를 밀어내고, 반발과 마찰을 적용합니다.

트리거는 겹침만 감지합니다. 두 물체가 겹쳐도 밀어내거나 튕기는 물리적 반응 없이, 영역에 무엇이 들어왔는지만 판별합니다.

<br>

```
Collider vs Trigger

일반 Collider (Is Trigger = false)

  [A] →← [B]              충돌 시 밀려남

  접촉점 계산 → 물체 분리 → 반발/마찰 적용
  콜백: OnCollisionEnter / OnCollisionStay / OnCollisionExit

Trigger (Is Trigger = true)

  [A   |겹침|   B]         겹쳐도 통과

  겹침 감지만 수행, 물리적 반응 없음
  콜백: OnTriggerEnter / OnTriggerStay / OnTriggerExit
```

<br>

### Trigger가 더 가벼운 이유

트리거는 충돌 해소 단계를 건너뜁니다. Broadphase와 Narrowphase까지는 일반 콜라이더와 동일하지만, 겹침이 확인되면 접촉점 계산, 물체 분리, 반발·마찰 처리 없이 바로 콜백(`OnTriggerEnter`)을 호출합니다. 물리적 반응이 필요 없는 콜라이더를 트리거로 전환하면 이 비용이 사라집니다.

<br>

```
처리 단계 비교

일반 Collider:
  Broadphase → Narrowphase → 접촉점 계산
  → 충돌 해소 → 위치/속도 갱신 → OnCollisionEnter

Trigger:
  Broadphase → Narrowphase → 겹침 확인
  (접촉점 계산 · 충돌 해소 · 위치/속도 갱신 생략)
  → OnTriggerEnter
```

<br>

### Trigger를 사용해야 하는 상황

게임에서 물리적 반응 없이 영역 감지만 필요한 상황은 많습니다.

<br>

```
Trigger 적합 사례

아이템 획득
  플레이어가 아이템 위를 지나가면 획득
  아이템이 플레이어를 밀어내면 안 됨
  → Trigger로 겹침 감지 후 아이템 제거

영역 진입 감지
  특정 구역에 플레이어가 들어오면 이벤트 발생
  보이지 않는 벽이 플레이어를 막으면 안 됨
  → Trigger 콜라이더로 영역 설정

공격 범위 판정
  검의 휘두름 범위에 적이 있는지 확인
  검이 적을 물리적으로 밀어내는 것은 부자연스러움
  → Trigger로 범위 겹침 확인 후 데미지 적용

AI 시야 탐지
  적 AI의 시야 범위에 플레이어가 들어왔는지 확인
  물리적 반응 불필요
  → 큰 Sphere Trigger로 탐지 범위 설정
```

<br>

물리적으로 밀어내야 하는 경우(캐릭터가 벽에 부딪힘, 공이 바닥에서 튕김 등)에만 일반 콜라이더를 사용하고, 나머지는 가능한 한 Trigger를 사용하는 것이 물리 비용을 줄이는 데 효과적입니다.

<br>

Trigger와 일반 콜라이더를 하나의 오브젝트에 함께 사용하는 것도 가능합니다.

예를 들어, 적 캐릭터에 일반 콜라이더(몸체 충돌)와 큰 Sphere Trigger(탐지 범위)를 함께 부착할 수 있습니다. 다만 같은 오브젝트에 두면 OnCollisionEnter와 OnTriggerEnter 콜백이 모두 같은 스크립트에 도착하므로, 어떤 콜라이더가 이벤트를 발생시켰는지 구분해야 합니다. Trigger 콜라이더를 별도의 자식 오브젝트에 분리하면 각 스크립트가 자신의 역할에 맞는 콜백만 처리할 수 있습니다.

<br>

---

## Raycasting과 NonAlloc 패턴

### 물리 쿼리의 역할

총을 쏘면 총알이 어디에 맞았는지, 폭발이 발생하면 범위 안에 누가 있는지를 판정해야 합니다. 이런 판정은 PhysX의 자동 충돌 검출과 별개로, 개발자가 직접 호출하는 **물리 쿼리(Physics Query)**로 수행합니다.

물리 쿼리는 크게 두 가지입니다. **레이캐스트(Raycast)**는 한 지점에서 특정 방향으로 광선을 쏘아 경로상의 콜라이더를 찾고, **오버랩(Overlap)** 쿼리는 특정 영역 안에 있는 콜라이더를 찾습니다.

<br>

```
물리 쿼리 사용 예

레이캐스트 (Raycast):
  - 총알의 탄도 계산 (발사 → 명중 판정)
  - 시선 방향에 벽이 있는지 확인
  - 마우스 클릭 위치의 오브젝트 판별
  - 바닥까지의 거리 측정

오버랩 (Overlap):
  - 폭발 범위 내 오브젝트 검출
  - AI의 탐지 범위 내 적 검색
  - 스킬 범위 내 대상 선별
```

<br>

이 쿼리들은 `Update()`나 `FixedUpdate()` 안에서 매 프레임 호출해야 하는 경우가 많습니다. AI가 주변 적을 매 프레임 탐색하거나, 조준선의 명중 대상을 매 프레임 갱신해야 하기 때문입니다.

<br>

### 기본 물리 쿼리의 할당 문제

`Physics.RaycastAll()`이나 `Physics.OverlapSphere()` 같은 함수는 호출할 때마다 결과를 담을 배열을 힙에 새로 생성합니다. 이 배열은 사용 후 GC(Garbage Collector)의 수거 대상이 됩니다. 60fps 게임에서 매 프레임 호출하면 초당 60개의 배열이 힙에 쌓이고, 이런 쿼리를 호출하는 오브젝트가 20개라면 초당 1,200개로 늘어납니다.

<br>

```
기본 쿼리 vs NonAlloc 쿼리

기본 쿼리 (매 호출마다 배열 생성):

  RaycastHit[] hits = Physics.RaycastAll(origin, dir, dist);
  → 매 호출마다 RaycastHit[] 힙 할당

NonAlloc 쿼리 (사전 할당 배열 재사용):

  RaycastHit[] _buffer = new RaycastHit[32];  // 한 번만 생성

  int count = Physics.RaycastNonAlloc(origin, dir, _buffer, dist);
  → _buffer 재사용, 힙 할당 없음
  → 반환값은 실제 결과 수
```

<br>

### NonAlloc 패턴 적용

NonAlloc 패턴은 결과를 담을 배열을 **미리 한 번 생성**해두고, 매 호출마다 그 배열을 재사용합니다. 배열을 새로 만들지 않으므로 힙 할당이 발생하지 않습니다.

<br>

```csharp
// NonAlloc 패턴 적용 예시: AI 적 탐지

// 할당이 발생하는 코드
void Update() {
    Collider[] enemies = Physics.OverlapSphere(
        transform.position, detectionRange, enemyLayer
    );
    for (int i = 0; i < enemies.Length; i++) {
        ProcessEnemy(enemies[i]);
    }
}

// NonAlloc 적용 코드
// _enemyBuffer 재사용 — 힙 할당 0
// 결과가 16개를 초과하면 16개까지만 채워짐
Collider[] _enemyBuffer = new Collider[16];

void Update() {
    int count = Physics.OverlapSphereNonAlloc(
        transform.position, detectionRange,
        _enemyBuffer, enemyLayer
    );
    for (int i = 0; i < count; i++) {
        ProcessEnemy(_enemyBuffer[i]);
    }
}
```

<br>

### 주요 NonAlloc 함수

```
3D 물리 쿼리 NonAlloc 대응표

기본 함수                        NonAlloc 버전
──────────────────────────────────────────────────────────
Physics.RaycastAll()             Physics.RaycastNonAlloc()
Physics.SphereCastAll()          Physics.SphereCastNonAlloc()
Physics.BoxCastAll()             Physics.BoxCastNonAlloc()
Physics.CapsuleCastAll()         Physics.CapsuleCastNonAlloc()
Physics.OverlapSphere()          Physics.OverlapSphereNonAlloc()
Physics.OverlapBox()             Physics.OverlapBoxNonAlloc()
Physics.OverlapCapsule()         Physics.OverlapCapsuleNonAlloc()


2D 물리 쿼리 NonAlloc 대응표
──────────────────────────────────────────────────────────
Physics2D.RaycastAll()           Physics2D.RaycastNonAlloc()
Physics2D.OverlapCircleAll()     Physics2D.OverlapCircleNonAlloc()
Physics2D.OverlapBoxAll()        Physics2D.OverlapBoxNonAlloc()
```

<br>

### 배열 크기와 레이어 마스크

NonAlloc 함수의 배열 크기는 예상 최대 결과 수에 맞추어 설정합니다. 결과가 배열보다 많으면 초과분은 무시되므로, 너무 작게 잡으면 일부 결과를 놓칠 수 있습니다. 반대로 너무 크면 메모리를 불필요하게 점유합니다.

<br>

레이어 마스크 없이 검색하면 주변의 모든 콜라이더가 결과에 포함되므로, 배열을 크게 잡아야 합니다. 물리 쿼리에 **레이어 마스크(LayerMask)**를 지정하면 해당 레이어의 콜라이더만 검출되므로 결과 수가 줄어들고, 배열 크기도 작게 설정할 수 있습니다.

<br>

```
레이어 마스크와 거리 제한으로 결과 수 줄이기

레이어 마스크 없이:
  Physics.OverlapSphereNonAlloc(pos, 50f, buffer)
  → 반경 50m 내 모든 레이어의 콜라이더 검출
  → 환경, 아이템, 적, UI 등 수백 개 가능

레이어 마스크 + 거리 제한:
  Physics.OverlapSphereNonAlloc(
      pos, 15f, buffer, enemyLayerMask
  )
  → 반경 15m 내 적 레이어의 콜라이더만 검출
```

<br>

레이어 마스크는 Broadphase 단계에서 적용됩니다. 해당 레이어가 아닌 콜라이더는 검사 자체를 건너뛰므로, 쿼리의 처리 비용도 줄어듭니다. NonAlloc 패턴에 레이어 마스크를 함께 지정하면 효과적입니다.

<br>

---

## 물리 설정 미세 조정

Layer Collision Matrix와 수동 시뮬레이션 외에도, Physics Settings에서 조정할 수 있는 항목이 있습니다. Fixed Timestep은 물리 스텝의 실행 빈도를 제어하고, Solver Iteration은 충돌 해소의 정확도를 조절합니다.

### Fixed Timestep 조정

기본값 0.02초(50Hz)는 대부분의 게임에 적합합니다. 모바일 게임에서는 성능 제약으로 인해 0.04초(25Hz)로 늘려도 괜찮은 경우가 많습니다. 물리 스텝 빈도를 절반으로 줄이면 물리 연산 횟수도 절반이 됩니다.

<br>

```
Fixed Timestep에 따른 물리 스텝 수

1초 동안의 물리 스텝 수:

  Fixed Timestep = 0.02초  → 초당 50회
  Fixed Timestep = 0.03초  → 초당 약 33회
  Fixed Timestep = 0.04초  → 초당 25회

  30fps 게임에서:
  0.02초: 프레임당 약 1.67회 → 대부분 1~2회
  0.04초: 프레임당 약 0.83회 → 대부분 0~1회
```

<br>

Fixed Timestep을 늘리면 비용이 줄지만, 물리 시뮬레이션의 정밀도가 낮아집니다. 빠르게 움직이는 물체의 충돌 판정이 부정확해지거나, 관절이 불안정해질 수 있습니다. 물리가 핵심인 게임(물리 퍼즐, 차량 시뮬레이션 등)에서는 충돌 누락이나 관절 떨림이 게임플레이를 직접 손상시킬 수 있습니다. 반면 물리 상호작용이 단순한 게임(캐주얼, 매치3 등)에서는 0.04초로 충분한 경우가 많습니다.

### Solver Iteration Count

`Rigidbody.solverIterations`(기본값 6)는 PhysX가 충돌 해소 단계에서 실행하는 **솔버(Solver)**의 위치 반복 횟수를 제어합니다. 솔버는 접촉점에서 겹친 물체를 밀어내는 연산을 반복하여 겹침을 해소하는데, 반복 횟수가 많을수록 물체가 정확한 위치로 분리되지만 CPU 비용도 비례하여 증가합니다.

`Rigidbody.solverVelocityIterations`(기본값 1)는 속도 보정의 반복 횟수를 제어합니다. 충돌 후 반발(바운스)과 마찰에 의한 속도 변화를 계산하는 단계로, 반복 횟수가 많을수록 반발과 마찰이 정밀해집니다.

단순한 충돌만 처리하는 오브젝트는 반복 횟수를 2~3으로 줄여도 플레이어가 차이를 느끼기 어렵습니다. 반면 래그돌처럼 여러 관절이 연결된 오브젝트는 반복 횟수가 부족하면 관절이 늘어나거나 떨리므로, 기본값 이상이 필요할 수 있습니다.

<br>

전역 기본값은 `Physics Settings → Default Solver Iterations`에서 설정합니다. 전역 값을 낮게 설정하고, 래그돌처럼 정밀도가 필요한 오브젝트만 `Rigidbody.solverIterations`로 개별적으로 높이면 전체 비용을 줄일 수 있습니다.

<br>

---

## 정적 콜라이더 이동의 비용

[물리 최적화 (1)](/dev/unity/PhysicsOptimization-1/)에서 확인한 것처럼, 정적 콜라이더(Rigidbody가 없는 콜라이더)는 AABB를 한 번만 계산하고 Broadphase 자료구조에 한 번만 삽입됩니다. 정적 콜라이더는 움직이지 않는다고 가정되기 때문입니다.

그런데 스크립트에서 정적 콜라이더의 `transform.position`을 변경하면 비용이 큽니다. PhysX는 정적 콜라이더와 동적 콜라이더를 서로 다른 Broadphase 자료구조로 관리합니다. 동적 콜라이더의 자료구조는 매 프레임 위치가 바뀌는 것을 전제로 설계되어, AABB 갱신이 가볍습니다. 반면 정적 콜라이더의 자료구조는 한 번 배치되면 움직이지 않는다는 전제로 최적화되어 있어, 위치가 바뀌면 해당 콜라이더를 제거하고 새 위치에 다시 삽입하는 재구성이 필요합니다.

<br>

```
정적 콜라이더 이동의 문제

정적 콜라이더를 이동시키면:
  1. Broadphase 자료구조에서 제거
  2. 새 위치에서 AABB 재계산
  3. Broadphase 자료구조에 재삽입
  4. 내부 가속 구조(BVH 등) 부분 재구성

  → 정적 콜라이더는 이동하지 않는다고 최적화되어 있으므로
    이 재구성 비용은 동적 콜라이더의 AABB 갱신보다 훨씬 높음
```

<br>

해결 방법은 Rigidbody를 부착하는 것입니다. Rigidbody가 있으면 PhysX는 해당 콜라이더를 동적 자료구조에서 관리하므로, 위치가 바뀌어도 가벼운 AABB 갱신으로 처리됩니다. 물리 힘이 아니라 스크립트로만 위치를 제어하는 경우에는 **Kinematic Rigidbody**(`Rigidbody.isKinematic = true`)를 사용합니다. Kinematic Rigidbody는 중력이나 충돌 반발에 반응하지 않으면서도, 동적 자료구조에 포함되어 효율적으로 갱신됩니다.

<br>

---

## 최적화 전략 종합

지금까지 다룬 물리 최적화 전략을 비용 대비 효과 순으로 정리합니다.

<br>

```
물리 최적화 전략 우선순위

높은 효과, 낮은 구현 비용:
  1. Layer Collision Matrix 설정
     → 불필요한 충돌 쌍 제거
     → 설정만 변경하면 됨, 코드 수정 불필요
     → 프로젝트 초기에 레이어 구조와 함께 설정하면 이상적

  2. 정적 콜라이더에 Rigidbody(Kinematic) 부착
     → 정적 콜라이더 이동으로 인한 재구성 비용 제거
     → 컴포넌트 추가만 하면 됨

  3. Trigger 활용
     → 물리적 반응이 불필요한 곳에서 충돌 해소 생략
     → Is Trigger 체크만 변경

높은 효과, 중간 구현 비용:
  4. NonAlloc 물리 쿼리
     → 매 프레임 힙 할당 제거
     → 코드 수정 필요하지만 패턴이 단순

  5. 2D 게임에 2D 물리 사용
     → z축 연산 제거
     → 프로젝트 초기에 결정하면 비용 없음

  6. Fixed Timestep 조정
     → 물리 스텝 빈도 감소
     → 값 변경만 하면 되지만 정밀도 영향 확인 필요

중간 효과, 높은 구현 비용:
  7. Physics.Simulate 수동 제어
     → 불필요한 시점에 물리 완전 중단
     → 타이밍 관리 코드 필요

  8. Solver Iteration 개별 조정
     → 오브젝트별 정밀도/비용 최적화
     → 각 오브젝트의 요구사항 분석 필요
```

<br>

---

## CPU에서 시각 효과로

물리가 게임 로직을 위한 서브시스템이라면, 파티클과 애니메이션은 시각적 품질에 직접 영향을 미치는 서브시스템입니다. 비용을 줄이면서 품질을 유지하는 과제는 동일하지만, 접근 방식이 다릅니다.

[ParticleAndAnimation 시리즈](/dev/unity/ParticleAndAnimation-1/)에서 이어서 다룹니다.

---

## 마무리

- 물리 최적화는 PhysX가 처리하는 대상의 수와 복잡도를 줄이는 것으로 귀결됩니다.
- Broadphase 단계에서 걸러낼수록(Layer Collision Matrix, LayerMask) 이후 모든 단계의 비용이 줄어듭니다.
- 충돌 해소가 불필요한 곳은 Trigger로 전환하고, 물리 쿼리는 NonAlloc 패턴으로 힙 할당을 제거합니다.
- 움직이는 콜라이더에 Kinematic Rigidbody를 부착하면 Broadphase 자료구조 재구성을 피할 수 있습니다.
- 구현 비용 대비 효과가 높은 전략부터 적용하면, 적은 작업으로 큰 절감을 얻을 수 있습니다.

<br>

---

**관련 글**
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)

**시리즈**
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- **물리 최적화 (2) - 물리 최적화 전략** (현재 글)
