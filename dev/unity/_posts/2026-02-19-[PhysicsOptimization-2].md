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

## 실행 구조에서 최적화 전략으로

[물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)에서는 PhysX가 물리 스텝을 실행하는 방식과 Broadphase, Narrowphase, Rigidbody Sleep이 비용에 미치는 영향을 살펴보았습니다.

물리 최적화의 핵심은 물리 엔진이 처리해야 하는 일을 줄이는 것입니다. 모든 Collider 조합을 검사하지 않게 만들고, 물리가 필요하지 않은 시점에는 시뮬레이션을 실행하지 않으며, 충돌 반응이 필요 없는 곳에서는 해소 단계를 생략해야 합니다.

이번 글에서는 이 기준에 따라 물리 최적화 전략을 정리합니다. Layer Collision Matrix는 검사 대상 조합을 줄이는 방법이고, `Physics.Simulate()` 수동 제어는 물리 스텝을 실행하는 시점을 조절하는 방법입니다. Trigger와 NonAlloc 패턴은 충돌 처리와 물리 쿼리의 비용을 줄이는 데 사용됩니다.

마지막으로 Fixed Timestep, Solver Iteration, 정적 Collider 이동처럼 프로젝트 설정이나 오브젝트 구성에서 생기는 비용을 함께 다룹니다. 이 항목들은 작은 설정처럼 보일 수 있지만, 매 물리 스텝마다 반복되는 비용에 영향을 주므로 프로젝트 규모가 커질수록 차이가 커질 수 있습니다.

---

## Layer Collision Matrix

게임 씬의 모든 Collider가 서로 물리 충돌을 일으켜야 하는 것은 아닙니다. 플레이어의 총알은 플레이어와 충돌할 필요가 없고, 아이템끼리 서로 밀어낼 필요도 없는 경우가 많습니다. **Layer Collision Matrix**는 이런 레이어 조합을 물리 충돌 대상에서 제외하는 설정입니다. 불필요한 조합을 꺼 두면 AABB가 겹치더라도 정밀 충돌 검사와 충돌 해소로 이어지지 않습니다.

### 레이어 간 충돌 비활성화

Unity의 GameObject는 하나의 **Layer**에 속합니다. `Project Settings > Physics > Layer Collision Matrix`에서는 Layer 조합별로 물리 충돌을 허용할지 정할 수 있습니다.

예를 들어 `Player`, `Enemy`, `Bullet`, `Pickup`, `Environment`처럼 역할별로 Layer를 나누면 어떤 조합이 실제로 충돌해야 하는지 명확해집니다. `Player`와 `Environment`는 충돌해야 하지만, `Bullet`끼리 서로 충돌하거나 `Pickup`끼리 서로 밀어낼 필요는 없는 경우가 많습니다.

Layer Collision Matrix에서 불필요한 조합의 체크를 해제하면, 두 Collider의 AABB가 겹치더라도 해당 조합은 정밀 충돌 검사와 충돌 해소로 이어지지 않습니다. 즉, “가까이 있을 수는 있지만 물리적으로 반응할 필요는 없는 조합”을 엔진이 더 처리하지 않도록 제외하는 설정입니다.

<br>

**Layer Collision Matrix 예시**

| Layer 조합 | 설정 | 이유 |
|---|---|
| Player ↔ Environment | 활성 | 캐릭터가 지형과 벽에 막혀야 함 |
| Enemy ↔ Environment | 활성 | 적이 지형을 통과하면 안 됨 |
| Bullet ↔ Enemy | 활성 | 총알이 적에게 명중해야 함 |
| Bullet ↔ Environment | 활성 | 총알이 벽에 부딪혀야 함 |
| Bullet ↔ Bullet | 비활성 | 총알끼리 충돌할 필요가 없음 |
| Enemy ↔ Enemy | 비활성 | 적끼리 밀어내지 않는 게임이라면 불필요 |
| Pickup ↔ Pickup | 비활성 | 아이템끼리 물리 반응이 필요 없음 |
| UI ↔ 모든 물리 Layer | 비활성 | UI는 물리 충돌 대상이 아님 |

<br>

### 비용 감소 원리

Layer Collision Matrix는 Broadphase의 AABB 비교 자체를 줄이지는 않습니다. 줄어드는 것은 Narrowphase입니다. 비활성화된 쌍은 정밀 형상 검사와 충돌 해소를 건너뛰는데, Narrowphase는 AABB 비교보다 연산 비용이 높으므로 건너뛰는 쌍이 많을수록 절감 효과가 큽니다.

<br>

**씬 구성** — Player 1개, Enemy 50개, Bullet 100개, Pickup 20개, Environment 200개, UI 30개 (총 401개 콜라이더)

**적용 전 (모든 레이어 쌍 활성)** — 잠재적 쌍 약 80,000쌍

**적용 후 (필요한 쌍만 활성)**

| 쌍 | 개수 |
|---|---|
| Player ↔ Enemy | 50쌍 |
| Player ↔ Env | 200쌍 |
| Player ↔ Pickup | 20쌍 |
| Enemy ↔ Env | 10,000쌍 |
| Bullet ↔ Enemy | 5,000쌍 |
| Bullet ↔ Env | 20,000쌍 |
| **합계** | **약 35,000쌍** |

→ 약 45,000쌍(56%)의 Narrowphase 검사 생략

<br>

오브젝트 수가 많은 레이어의 불필요한 쌍일수록 비활성화 효과가 큽니다. 같은 레이어 내 자기 충돌(Bullet↔Bullet 등)은 해당 레이어의 오브젝트 수가 늘어날수록 쌍이 급격히 증가하므로, 게임 로직에 불필요하다면 비활성화하는 것이 효과적입니다.

<br>

### 설정 전략

Layer Collision Matrix는 프로젝트 초기에 레이어 구조와 함께 정하는 편이 가장 좋습니다. 새 프로젝트라면 모든 조합을 허용한 상태에서 하나씩 끄기보다, 실제 게임 규칙상 필요한 충돌 조합을 먼저 적어 두고 그 조합만 활성화하는 방식이 더 안전합니다.

이미 진행 중인 프로젝트에서는 한 번에 많은 조합을 끄기보다, 비용이 큰 조합부터 확인합니다. 오브젝트 수가 많은 레이어끼리의 충돌, 같은 레이어 안의 자기 충돌, 게임 로직상 반응이 필요 없는 조합부터 점검하면 영향 범위를 관리하기 쉽습니다.

Layer Collision Matrix는 개별 Collider가 아니라 Layer 조합 단위로 동작합니다. 따라서 충돌 규칙이 같은 오브젝트는 같은 Layer에 모을수록 설정이 단순해집니다. 예를 들어 바닥, 벽, 천장이 모두 플레이어와 적을 막는 역할이라면 하나의 `Environment` Layer로 묶을 수 있습니다. 반대로 서로 다른 충돌 규칙이 필요한 오브젝트를 같은 Layer에 넣으면, Matrix만으로는 원하는 조합을 분리하기 어렵습니다.

---

## Physics.Simulate 수동 제어

Layer Collision Matrix는 물리 엔진이 검사할 Collider 조합을 줄이는 방법입니다. 하지만 충돌 조합을 줄였더라도, Unity가 매 Fixed Timestep마다 물리 시뮬레이션을 실행한다는 사실은 바뀌지 않습니다. Rigidbody 상태 확인, Broadphase 갱신, Sleep/Awake 처리처럼 물리 월드를 갱신하는 작업은 여전히 수행될 수 있습니다.

`Physics.Simulate()` 수동 제어는 자동 시뮬레이션을 끄고, 코드에서 호출한 순간에만 물리 스텝을 진행하는 방식입니다. 메뉴, 대화, 선택 대기처럼 물리 결과가 필요 없는 구간에서는 호출하지 않고, 충돌 결과나 Rigidbody 갱신이 필요한 구간에서만 호출할 수 있습니다.

### 자동 시뮬레이션의 비용

Unity의 기본 설정에서는 물리 시뮬레이션이 자동으로 실행됩니다. 누적된 시간이 Fixed Timestep에 도달하면 Unity는 물리 스텝을 진행하고, 이 과정에서 Rigidbody 갱신, 충돌 후보 갱신, 접촉 처리 같은 작업이 수행됩니다.

이 방식은 실시간 액션처럼 물리 결과가 계속 필요한 장면에서는 자연스럽습니다. 하지만 메뉴, 대화, 컷씬, 인벤토리처럼 물체의 움직임이나 충돌 결과가 필요 없는 구간에서는 같은 자동 실행이 불필요한 비용이 될 수 있습니다.

### 수동 시뮬레이션 전환

`Physics.simulationMode`를 `SimulationMode.Script`로 설정하면 Unity는 물리 스텝을 자동으로 실행하지 않습니다. 이때부터 물리 월드는 `Physics.Simulate(deltaTime)`을 호출한 만큼만 진행됩니다.
이 설정은 개별 Rigidbody나 Collider에 적용하는 값이 아니라, 프로젝트의 3D 물리 월드 전체에 적용됩니다. 에디터에서는 `Project Settings > Physics > Simulation Mode`에서 설정할 수 있고, 코드에서는 `Physics.simulationMode`로 변경할 수 있습니다.

중요한 점은 `FixedUpdate()`와 물리 시뮬레이션이 같은 것이 아니라는 점입니다. `FixedUpdate()`는 고정 간격으로 호출되는 스크립트 콜백이고, 물리 시뮬레이션은 Rigidbody의 속도와 위치, 충돌, Joint, Trigger 상태를 계산하는 엔진 작업입니다. 기본 모드에서는 `FixedUpdate()` 뒤에 Unity가 물리 시뮬레이션을 자동으로 실행하지만, Script 모드에서는 이 자동 실행이 일어나지 않습니다.

기존 Fixed Timestep 간격은 유지하면서 특정 상태에서만 물리를 멈추고 싶다면, `FixedUpdate()`에서 `Physics.Simulate(Time.fixedDeltaTime)` 호출 여부를 분기할 수 있습니다. 메뉴나 대화처럼 물리 결과가 필요 없는 상태에서는 호출하지 않고, 게임 플레이 상태에서만 한 스텝을 진행하는 방식입니다.

```csharp
void FixedUpdate()
{
    if (_state == GameState.Menu || _state == GameState.Dialogue)
    {
        return;
    }

    Physics.Simulate(Time.fixedDeltaTime);
}
```

위 코드에서 `FixedUpdate()`는 계속 호출되지만, 메뉴와 대화 상태에서는 물리 시뮬레이션이 실행되지 않습니다. 게임 플레이 상태에서는 기존 Fixed Timestep 간격에 맞춰 물리 월드가 한 스텝씩 갱신됩니다.

<br>

### 수동 시뮬레이션의 활용

수동 시뮬레이션은 물리 결과가 필요 없는 상태가 명확한 게임에서 효과가 큽니다. 메뉴, 대화, 인벤토리, 턴 선택 대기처럼 Rigidbody가 움직이지 않고 충돌 결과도 필요 없는 구간에서는 물리 스텝을 건너뛸 수 있습니다. 반대로 공격이 발동되거나, 블록이 떨어지거나, 캐릭터가 다시 움직이기 시작하는 구간에서는 `Physics.Simulate()`를 호출해 물리 월드를 갱신합니다.

이 방식은 물리 콜백의 실행 시점도 바꿉니다. 기본 모드에서는 Unity가 자동으로 물리 시뮬레이션을 실행한 뒤 `OnCollisionEnter`, `OnTriggerEnter` 같은 콜백을 발생시킵니다. Script 모드에서는 이런 콜백이 `Physics.Simulate()` 호출 과정에서 발생합니다. 따라서 물리 콜백이 항상 자동 시뮬레이션 직후에 실행된다고 전제한 코드가 있다면, 수동 시뮬레이션으로 전환할 때 실행 순서를 함께 점검해야 합니다.

---

## 2D 물리와 3D 물리

Layer Collision Matrix와 수동 시뮬레이션은 이미 선택한 물리 엔진 안에서 작업량을 줄이는 방법입니다. 하지만 2D 게임이라면 그보다 먼저 확인해야 할 것이 있습니다. 프로젝트가 실제로 2D 물리를 사용하고 있는지, 아니면 3D 물리 컴포넌트로 2D처럼 동작하게 만들고 있는지입니다.

2D 화면에서 움직이는 게임이라도 `Rigidbody`, `BoxCollider` 같은 3D 컴포넌트를 사용하면 PhysX가 3차원 물리로 계산합니다. 반대로 `Rigidbody2D`, `BoxCollider2D`를 사용하면 Box2D 기반의 2D 물리로 계산됩니다. 두 방식은 컴포넌트 이름만 다른 것이 아니라, 서로 다른 물리 엔진을 사용합니다.

### 두 개의 독립된 물리 엔진

Unity의 3D 물리와 2D 물리는 서로 다른 엔진을 사용합니다. 3D 물리는 PhysX를 기반으로 하고, 2D 물리는 Box2D를 기반으로 합니다. 3D Collider와 2D Collider는 서로 다른 물리 시스템에 속하므로, 서로 충돌 대상으로 계산되지 않습니다.

<br>

| 구분 | 3D 물리 | 2D 물리 |
|---|---|---|
| 기반 엔진 | PhysX | Box2D |
| Rigidbody | `Rigidbody` | `Rigidbody2D` |
| Box Collider | `BoxCollider` | `BoxCollider2D` |
| Capsule Collider | `CapsuleCollider` | `CapsuleCollider2D` |
| 원형 Collider | `SphereCollider` | `CircleCollider2D` |
| 복합 형상 Collider | `MeshCollider` | `PolygonCollider2D` |

<br>

### 2D 게임에서 3D 물리를 사용하면 생기는 문제

2D처럼 보이는 게임에서도 `Rigidbody`, `BoxCollider` 같은 3D 물리 컴포넌트를 사용할 수는 있습니다. 하지만 이 경우 Unity는 PhysX 기반의 3D 물리로 계산합니다. 화면에서는 x, y 평면만 사용하더라도 물리 엔진은 z축을 포함한 3차원 공간을 기준으로 Broadphase, 충돌 검사, 충돌 해소를 처리합니다.

<br>

| 항목 | 3D 물리 컴포넌트 사용 | 2D 물리 컴포넌트 사용 |
|---|---|---|
| 사용하는 엔진 | PhysX | Box2D |
| 계산 기준 | x, y, z 3차원 | x, y 2차원 |
| Collider | `BoxCollider`, `SphereCollider` 등 | `BoxCollider2D`, `CircleCollider2D` 등 |
| Rigidbody | `Rigidbody` | `Rigidbody2D` |
| 관리해야 할 축 | z축 위치와 회전까지 고려 | 2D 평면 기준으로 처리 |

2D 게임에서 3D 물리를 사용하면 불필요한 축까지 관리해야 하고, z축 위치나 회전이 의도와 다르게 변하지 않도록 별도로 제한해야 할 수 있습니다. 게임이 실제로 2D 평면에서만 동작한다면 2D 물리 컴포넌트를 사용하는 편이 더 단순하고, 물리 엔진도 필요한 차원만 계산합니다.

<br>

### 2D 물리에서의 적용

이 글에서 다루는 최적화 방향은 2D 물리에도 대부분 대응됩니다. 불필요한 충돌 조합을 줄이고, 필요할 때만 시뮬레이션을 진행하며, 물리 쿼리에서 할당을 줄이는 원리는 같습니다. 다만 2D 물리는 별도의 엔진과 API를 사용하므로 설정 위치와 함수 이름을 구분해야 합니다.

<br>

| 영역 | 3D 물리 | 2D 물리 |
|---|---|---|
| Layer Collision Matrix | `Project Settings → Physics` | `Project Settings → Physics 2D` |
| 수동 시뮬레이션 | `Physics.simulationMode` / `Physics.Simulate()` | `Physics2D.simulationMode` / `Physics2D.Simulate()` |
| NonAlloc 쿼리 | `Physics.RaycastNonAlloc()`, `Physics.OverlapSphereNonAlloc()` 등 | `Physics2D.RaycastNonAlloc()`, `Physics2D.OverlapCircleNonAlloc()`, `Physics2D.OverlapBoxNonAlloc()` 등 |
| Sleep | `Rigidbody` | `Rigidbody2D` |

예를 들어 2D 물리의 충돌 매트릭스는 `Project Settings > Physics 2D`에서 설정하고, 수동 시뮬레이션은 `Physics2D.simulationMode`와 `Physics2D.Simulate()`를 사용합니다. Rigidbody2D에도 Sleep이 있으므로 안정된 2D 오브젝트는 반복 계산에서 제외될 수 있고, NonAlloc 계열의 2D 쿼리를 사용하면 반복적인 물리 쿼리에서 힙 할당을 줄일 수 있습니다.

<br>

---

## Trigger vs Collider

앞에서는 충돌 조합을 줄이거나, 물리 스텝을 실행할 시점을 조절하거나, 2D/3D 중 알맞은 물리 엔진을 선택하는 방법을 다뤘습니다. 이번에는 개별 Collider가 충돌을 어떻게 처리할지에 초점을 둡니다.

게임에는 물체를 실제로 막아야 하는 충돌도 있지만, 영역에 들어왔는지만 알면 되는 충돌도 많습니다. 아이템 획득, 감지 범위, 이벤트 구역처럼 위치 보정이나 반발 처리가 필요 없다면 일반 Collider 대신 Trigger를 사용할 수 있습니다.

### 물리적 반응의 유무

Collider 컴포넌트는 `Is Trigger` 설정에 따라 처리 방식이 달라집니다. `Is Trigger`가 꺼져 있으면 충돌한 물체의 위치와 속도를 보정하는 일반 Collider로 동작하고, `Is Trigger`가 켜져 있으면 겹침 이벤트만 발생시키는 Trigger로 동작합니다.

일반 Collider는 물리적 반응을 포함합니다. 두 Collider가 충돌하면 물리 엔진은 접촉점을 계산하고, 겹친 물체가 분리되도록 위치와 속도를 보정합니다. 이 과정에서 반발과 마찰도 함께 처리됩니다.

Trigger는 겹침을 이벤트로 알리는 데 초점을 둡니다. 두 Collider가 겹쳐도 위치 보정이나 반발 처리는 수행하지 않으며, `OnTriggerEnter`, `OnTriggerStay`, `OnTriggerExit` 같은 콜백으로 영역 진입과 이탈만 전달합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Collider 처리 방식</text>

  <text x="145" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Collider (Is Trigger = false)</text>

  <rect x="70" y="75" width="55" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="97" y="100" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">A</text>
  <rect x="170" y="75" width="55" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="197" y="100" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">B</text>

  <line x1="125" y1="95" x2="145" y2="95" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="148,95 142,92 142,98" fill="currentColor"/>
  <line x1="170" y1="95" x2="150" y2="95" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="147,95 153,92 153,98" fill="currentColor"/>

  <text x="147" y="138" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">겹침을 해소</text>
  <text x="147" y="165" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">접촉점 계산 → 위치 보정 → 반발/마찰 적용</text>

  <text x="147" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.75">콜백</text>
  <text x="147" y="220" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">OnCollisionEnter</text>
  <text x="147" y="237" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">OnCollisionStay</text>
  <text x="147" y="254" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">OnCollisionExit</text>

  <line x1="290" y1="40" x2="290" y2="270" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" stroke-opacity="0.4"/>

  <text x="435" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Trigger (Is Trigger = true)</text>

  <rect x="370" y="75" width="65" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="385" y="100" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">A</text>
  <rect x="420" y="75" width="65" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="470" y="100" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor">B</text>
  <text x="427" y="105" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" fill-opacity="0.75">겹침</text>

  <text x="435" y="138" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">겹침 이벤트만 전달</text>
  <text x="435" y="165" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">위치 보정과 반발 처리는 수행하지 않음</text>

  <text x="435" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" fill-opacity="0.75">콜백</text>
  <text x="435" y="220" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">OnTriggerEnter</text>
  <text x="435" y="237" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">OnTriggerStay</text>
  <text x="435" y="254" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">OnTriggerExit</text>
</svg>
</div>

<br>

### Trigger가 더 가벼운 이유

Trigger도 어떤 Collider가 영역 안에 들어왔는지는 판단해야 하므로, 후보 탐색과 겹침 판별 자체는 필요합니다. 차이는 그다음 단계입니다. 일반 Collider는 접촉을 해소하기 위해 위치와 속도를 보정하고 반발, 마찰 같은 물리 반응을 계산하지만, Trigger는 이런 충돌 해소 단계를 수행하지 않습니다.

따라서 Trigger는 충돌을 막는 용도가 아니라, 겹침을 감지하는 용도에 적합합니다. 아이템 획득, 감지 영역, 이벤트 구역처럼 위치 보정과 반발 처리가 필요 없는 경우에는 Trigger를 사용해 충돌 해소 비용을 줄일 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">처리 단계 비교</text>

  <text x="20" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Collider (Is Trigger = false)</text>

  <g font-family="sans-serif" font-size="10" fill="currentColor">
    <rect x="20" y="72" width="80" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="60" y="91" text-anchor="middle">Broadphase</text>

    <rect x="115" y="72" width="80" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="155" y="91" text-anchor="middle">Narrowphase</text>

    <rect x="215" y="72" width="150" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="290" y="91" text-anchor="middle">Solver: 위치/속도 보정</text>

    <rect x="390" y="72" width="115" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
    <text x="447" y="91" text-anchor="middle">Collision 콜백</text>
  </g>

  <g stroke="currentColor" stroke-width="1.2" fill="currentColor">
    <line x1="100" y1="87" x2="113" y2="87"/>
    <polygon points="116,87 110,84 110,90"/>
    <line x1="195" y1="87" x2="213" y2="87"/>
    <polygon points="216,87 210,84 210,90"/>
    <line x1="365" y1="87" x2="388" y2="87"/>
    <polygon points="391,87 385,84 385,90"/>
  </g>

  <text x="20" y="140" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Trigger (Is Trigger = true)</text>

  <g font-family="sans-serif" font-size="10" fill="currentColor">
    <rect x="20" y="154" width="80" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="60" y="173" text-anchor="middle">Broadphase</text>

    <rect x="115" y="154" width="80" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="155" y="173" text-anchor="middle">Narrowphase</text>

    <rect x="215" y="154" width="150" height="30" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3" stroke-opacity="0.55"/>
    <text x="290" y="173" text-anchor="middle" fill-opacity="0.65">Solver 생략</text>

    <rect x="390" y="154" width="115" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
    <text x="447" y="173" text-anchor="middle">Trigger 콜백</text>
  </g>

  <g stroke="currentColor" stroke-width="1.2" fill="currentColor">
    <line x1="100" y1="169" x2="113" y2="169"/>
    <polygon points="116,169 110,166 110,172"/>
    <line x1="195" y1="169" x2="213" y2="169"/>
    <polygon points="216,169 210,166 210,172"/>
    <line x1="365" y1="169" x2="388" y2="169" stroke-dasharray="3,2"/>
    <polygon points="391,169 385,166 385,172"/>
  </g>
</svg>
</div>

<br>

### Trigger를 사용해야 하는 상황

Trigger는 물체의 이동을 막기 위한 충돌에는 사용하지 않습니다. 두 물체가 겹친 뒤 위치 보정이나 반발 처리가 필요하다면 Collider로 처리해야 합니다. 반대로 영역에 들어왔는지, 특정 대상과 겹쳤는지만 알면 되는 경우에는 Trigger가 더 적합합니다.

<br>

| 사용 예 | Trigger가 적합한 이유 |
|---|---|
| 아이템 획득 | 플레이어와 겹쳤는지만 확인하면 되고, 아이템이 플레이어를 밀어낼 필요가 없음 |
| 이벤트 구역 | 특정 영역에 들어왔는지만 알면 되며, 보이지 않는 벽처럼 막을 필요가 없음 |
| 공격 범위 판정 | 범위 안의 대상에게 데미지를 적용하면 되고, 공격 범위 자체가 대상을 밀어낼 필요는 없음 |
| AI 감지 범위 | 대상이 감지 영역 안에 있는지만 확인하면 됨 |

<br>

벽, 바닥, 캐릭터 몸체처럼 실제로 움직임을 막아야 하는 충돌은 Collider로 처리해야 합니다. 반대로 아이템, 감지 영역, 이벤트 구역처럼 물리 반응이 필요 없는 영역은 Trigger로 처리하는 편이 적절합니다.

하나의 캐릭터에 Collider와 Trigger를 함께 사용할 때는 역할별로 오브젝트를 나누는 편이 관리하기 쉽습니다. 예를 들어 적 캐릭터의 부모 오브젝트에는 몸체 충돌용 Collider를 두고, 감지 범위는 자식 오브젝트의 Trigger로 분리할 수 있습니다.

이렇게 나누면 몸체 충돌은 부모 오브젝트의 `OnCollision...` 콜백에서, 감지 범위는 자식 오브젝트의 `OnTrigger...` 콜백에서 처리할 수 있습니다. 충돌 처리와 감지 처리가 한 스크립트에 섞이지 않으므로, 각 Collider의 역할도 더 명확해집니다.

---

## Raycasting과 NonAlloc 패턴

Trigger는 미리 만들어 둔 영역에 다른 Collider가 들어왔을 때 콜백을 받는 방식입니다. 이 방식은 영역이 계속 존재하고, 진입이나 이탈 시점을 처리해야 할 때 적합합니다.

반대로 판정이 필요한 시점이 정해져 있다면 Trigger 영역을 계속 유지할 필요가 없습니다. 총알을 발사한 순간 명중 지점을 확인하거나, 현재 조준선이 가리키는 대상을 찾거나, 폭발이 발생한 순간 범위 안의 대상을 찾는 경우가 그렇습니다. 이런 판정에는 Raycast나 Overlap 같은 물리 쿼리를 사용합니다.

물리 쿼리는 조준선 갱신, 마우스 선택, AI 탐지처럼 매 프레임 반복되는 경우가 많습니다. 호출 횟수가 많아지면 Collider를 찾는 비용뿐 아니라, 결과를 담기 위해 생성되는 배열 할당도 문제가 됩니다.

### 물리 쿼리의 역할

물리 쿼리(Physics Query)는 자동 충돌 이벤트와 별개로, 코드가 원하는 시점에 Collider를 검색하는 기능입니다. 대표적으로 Raycast와 Overlap 쿼리를 사용합니다.

| 쿼리 | 검사 방식 | 주로 쓰는 상황 |
|---|---|---|
| Raycast | 한 지점에서 특정 방향으로 선을 쏘아, 경로에 있는 Collider를 찾음 | 총알 명중 판정, 조준선 검사, 클릭한 오브젝트 판별, 바닥 거리 측정 |
| Overlap | 특정 영역 안에 들어와 있는 Collider를 찾음 | 폭발 범위 판정, AI 감지 범위 검색, 스킬 범위 내 대상 선별 |

<br>

Raycast는 방향이 중요한 검사에 적합하고, Overlap은 범위 안의 대상을 모아야 할 때 적합합니다. 이런 쿼리는 조준선 갱신이나 AI 탐지처럼 반복적으로 호출되는 경우가 많으므로, 쿼리 횟수와 함께 호출 과정에서 발생하는 힙 할당도 확인해야 합니다.

<br>

### 기본 물리 쿼리의 할당 문제

`Physics.RaycastAll()`이나 `Physics.OverlapSphere()`처럼 결과를 배열로 반환하는 함수는, 호출할 때마다 새로운 배열을 반환합니다. 이 배열은 힙에 할당되며, 사용이 끝나면 GC(Garbage Collector)의 수거 대상이 됩니다.

호출 빈도가 낮다면 큰 부담이 되지 않지만, 조준선, AI 탐지, 범위 스킬처럼 매 프레임 반복되는 쿼리에서는 작은 할당도 계속 누적됩니다. 예를 들어 60fps에서 매 프레임 한 번 호출하면 초당 60개의 배열이 생성되고, 같은 쿼리를 호출하는 오브젝트가 20개라면 초당 1,200개의 배열이 만들어집니다.

<br>

배열을 반환하는 쿼리는 호출 결과를 새 배열로 돌려줍니다.

```csharp
RaycastHit[] hits = Physics.RaycastAll(origin, dir, dist);
// 매 호출마다 RaycastHit[] 힙 할당
```

NonAlloc 버전은 결과를 저장할 배열을 인자로 받습니다. 같은 배열을 반복해서 넘기면 새 결과 배열을 할당하지 않습니다. 결과는 전달한 배열에 기록되고, 함수의 반환값은 기록된 결과 개수를 의미합니다.

```csharp
private readonly RaycastHit[] _buffer = new RaycastHit[32];

int count = Physics.RaycastNonAlloc(origin, dir, _buffer, dist);
// 반환값은 _buffer에 저장된 결과 개수
```

<br>

### NonAlloc 패턴 적용

NonAlloc 패턴의 목적은 반복 쿼리에서 결과 배열이 매번 새로 할당되는 것을 막는 것입니다. 이를 위해 결과를 담을 배열을 미리 준비하고, 쿼리를 호출할 때 그 배열을 인자로 전달합니다. 함수는 배열에 결과를 기록한 뒤 기록된 개수를 반환하므로, 결과를 처리할 때는 반환된 개수만큼만 순회합니다.

반복 물리 쿼리가 자주 쓰이는 예로 AI 탐지가 있습니다. AI가 주변의 적을 계속 확인해야 한다면 일정 범위 안의 Collider를 반복해서 검색하게 됩니다. 이때 배열을 반환하는 `OverlapSphere()`를 `Update()`마다 호출하면, 매 프레임 새로운 `Collider[]`가 할당됩니다.

```csharp
private float _detectionRange = 10f;
private LayerMask _enemyLayerMask;

void Update()
{
    // 결과 배열이 반환되므로, 이 호출마다 힙 할당이 발생합니다.
    Collider[] enemies = Physics.OverlapSphere(
        transform.position,
        _detectionRange,
        _enemyLayerMask
    );

    for (int i = 0; i < enemies.Length; i++)
    {
        ProcessEnemy(enemies[i]);
    }
}
```

같은 탐지를 NonAlloc 함수로 바꾸면 미리 준비한 배열에 결과를 기록하므로, 호출할 때마다 새 결과 배열이 할당되지 않습니다.

```csharp
private float _detectionRange = 10f;
private LayerMask _enemyLayerMask;
private readonly Collider[] _enemyBuffer = new Collider[16];

void Update()
{
    // 결과는 _enemyBuffer에 기록되고, count에는 기록된 개수가 들어갑니다.
    int count = Physics.OverlapSphereNonAlloc(
        transform.position,
        _detectionRange,
        _enemyBuffer,
        _enemyLayerMask
    );

    // 이전 호출의 결과가 남아 있을 수 있으므로 count까지만 순회합니다.
    for (int i = 0; i < count; i++)
    {
        ProcessEnemy(_enemyBuffer[i]);
    }
}
```

여기서 중요한 값은 `count`입니다. `count`는 이번 호출에서 `_enemyBuffer`에 실제로 기록된 Collider 수를 의미합니다. 버퍼 배열에는 이전 호출의 값이 남아 있을 수 있어, 결과를 처리할 때는 배열의 앞쪽 `count`개까지만 순회해야 합니다.

버퍼가 담을 수 있는 결과 수에도 한계가 있습니다. 감지 범위 안의 Collider가 `_enemyBuffer.Length`보다 많으면, 배열에 들어가지 못한 결과는 처리할 수 없습니다. 따라서 해당 쿼리에서 필요한 결과가 충분히 들어갈 수 있는 크기로 버퍼를 준비해야 합니다.

<br>

### 주요 NonAlloc 함수

반복 호출되는 쿼리는 다음과 같이 NonAlloc 버전으로 바꿀 수 있습니다.

| 쿼리 목적 | 배열을 반환하는 함수 | NonAlloc 버전 |
|---|---|
| Raycast 결과 여러 개 검색 | `Physics.RaycastAll()` | `Physics.RaycastNonAlloc()` |
| Shape Cast 결과 여러 개 검색 | `Physics.SphereCastAll()`, `Physics.BoxCastAll()`, `Physics.CapsuleCastAll()` | `Physics.SphereCastNonAlloc()`, `Physics.BoxCastNonAlloc()`, `Physics.CapsuleCastNonAlloc()` |
| 영역 안의 Collider 검색 | `Physics.OverlapSphere()`, `Physics.OverlapBox()`, `Physics.OverlapCapsule()` | `Physics.OverlapSphereNonAlloc()`, `Physics.OverlapBoxNonAlloc()`, `Physics.OverlapCapsuleNonAlloc()` |

2D 물리에서도 같은 방식의 NonAlloc 쿼리를 사용할 수 있습니다. 대표적으로 `Physics2D.RaycastNonAlloc()`, `Physics2D.OverlapCircleNonAlloc()`, `Physics2D.OverlapBoxNonAlloc()` 등이 있습니다.

<br>

### 레이어 마스크로 검색 대상 줄이기

NonAlloc 함수는 반복 쿼리의 힙 할당을 줄여주지만, 쿼리가 검사하는 후보 수 자체를 줄여주지는 않습니다. 후보 수를 줄이려면 어떤 Collider를 검색 대상에 포함할지 함께 제한해야 합니다.

이때 사용하는 값이 **레이어 마스크(LayerMask)**입니다. 레이어 마스크를 지정하지 않으면 같은 반경 안의 모든 레이어가 검색 대상이 됩니다. 예를 들어 적 탐지 쿼리라면 Enemy 레이어를 포함한 LayerMask를 만들어 두고, 쿼리 호출 시 함께 넘기는 편이 적절합니다.

```csharp
Physics.OverlapSphereNonAlloc(pos, 15f, buffer);
// 반경 15m 안의 모든 레이어를 검색
```

다음 코드는 같은 반경을 검색하지만, `enemyLayerMask`를 함께 넘겨 Enemy 레이어만 결과 후보에 포함합니다.

```csharp
Physics.OverlapSphereNonAlloc(pos, 15f, buffer, enemyLayerMask);
// 반경 15m 안의 Enemy 레이어만 검색
```

<br>

레이어뿐 아니라 검색 반경이나 박스 크기도 후보 수에 영향을 줍니다. 반복 쿼리에서는 NonAlloc 함수로 결과 배열 할당을 줄이고, 레이어 마스크와 검색 범위로 불필요한 후보를 함께 줄이는 방식이 적절합니다.

---

## 물리 설정 조정

앞에서 다룬 Layer Collision Matrix, Trigger, NonAlloc 쿼리는 물리 엔진이 처리할 후보를 줄이는 방법에 가깝습니다.
하지만 후보 수만으로 물리 비용이 결정되지는 않습니다. 물리 스텝이 실행되는 빈도와, 한 스텝 안에서 겹친 물체를 분리하거나 Joint로 연결된 물체의 거리와 각도를 맞추는 등의 반복 계산도 CPU 시간에 영향을 줍니다.

이 실행 빈도와 반복 계산을 조정하는 대표적인 설정이 Fixed Timestep과 Solver Iteration입니다.
Fixed Timestep은 물리 스텝 사이의 시간 간격을 정하고, Solver Iteration은 충돌한 물체를 분리하고 Joint로 연결된 물체의 위치 관계를 맞추는 계산을 몇 번 반복할지 정합니다. Unity에서는 Fixed Timestep을 Project Settings의 Time 항목에서 조정하고, Solver Iteration의 전역 기본값은 Physics Settings에서 조정합니다.

Fixed Timestep을 크게 설정하면 같은 시간 동안 실행되는 물리 스텝 수가 줄고, Solver Iteration을 낮추면 한 스텝 안에서 반복되는 계산량이 줄어듭니다. 그만큼 CPU 비용은 낮아질 수 있지만, 충돌 반응이 거칠어지거나 Joint가 불안정해질 수 있습니다.

### Fixed Timestep 조정

Fixed Timestep은 한 번의 물리 스텝이 담당하는 시간 간격입니다. 0.02초로 설정하면 1초를 50개의 물리 스텝으로 나누어 계산하고, 0.04초로 설정하면 25개의 물리 스텝으로 계산합니다. 값이 커질수록 같은 시간 동안 실행되는 물리 스텝 수는 줄어듭니다.

<br>

| Fixed Timestep | 초당 물리 스텝 수 |
|---|---|
| 0.02초 | 50회 |
| 0.03초 | 약 33회 |
| 0.04초 | 25회 |

<br>

스텝 수가 줄어들면 물리 계산 횟수도 줄어 CPU 비용을 낮출 수 있습니다. 대신 한 스텝이 담당하는 시간이 길어지므로, 빠르게 움직이는 물체의 충돌 반응이 덜 정밀해질 수 있습니다. Joint로 연결된 물체도 위치 관계를 맞추는 간격이 길어져 흔들림이 커질 수 있습니다.

따라서 Fixed Timestep은 물리를 얼마나 드문 간격으로 계산해도 되는지를 정하는 값에 가깝습니다. 물리 퍼즐, 차량, 액션 게임처럼 충돌 반응이 게임플레이에 직접 영향을 주는 경우에는 기본값에 가까운 간격을 유지하는 편이 안정적입니다. 물리 상호작용이 단순한 게임이라면 값을 늘려 물리 스텝 수를 줄일 수 있지만, Profiler로 비용 변화를 확인하고 플레이 테스트에서 충돌 누락이나 움직임의 어색함이 없는지 함께 확인하는 편이 적절합니다.

### Solver Iteration 조정

물리 스텝에서는 물리 엔진이 맞춰야 하는 조건들이 생깁니다. 충돌한 물체는 서로 겹치지 않도록 분리되어야 하고, Joint로 연결된 물체는 지정된 거리나 회전 제한을 벗어나지 않아야 합니다. **솔버(Solver)**는 이런 조건을 만족시키기 위해 여러 번의 반복 계산을 수행하며, 매 반복마다 위치나 속도를 조금씩 보정합니다.

Solver Iteration은 이 반복 계산을 몇 번 수행할지 정하는 값입니다. 반복 횟수가 많을수록 겹침이나 Joint 오차가 줄어들어 결과가 안정적이지만, Solver에 사용하는 CPU 시간도 늘어납니다.

Unity에서는 Solver 반복 횟수를 위치 보정과 속도 보정으로 나누어 조정할 수 있습니다. `Rigidbody.solverIterations`는 겹친 물체를 분리하고 Joint의 거리나 회전 제한을 맞추는 위치 보정 반복 횟수입니다. `Rigidbody.solverVelocityIterations`는 충돌 후 반발과 마찰처럼 속도 변화를 계산하는 반복 횟수입니다.

필요한 반복 횟수는 오브젝트의 물리 구조에 따라 달라집니다. 바닥이나 벽과 단순히 충돌하는 오브젝트는 낮은 반복 횟수에서도 문제가 잘 드러나지 않을 수 있습니다. 반면 래그돌, 체인, 차량 서스펜션처럼 여러 Joint가 연결된 구조는 작은 오차가 누적되기 쉬우므로, 반복 횟수가 부족하면 관절이 늘어나거나 떨림이 커질 수 있습니다.

Unity에서는 전역 기본값을 `Physics Settings → Default Solver Iterations`와 `Default Solver Velocity Iterations`에서 설정합니다. 필요하다면 개별 Rigidbody의 `solverIterations`와 `solverVelocityIterations`를 따로 조정할 수도 있습니다. 모든 Rigidbody의 반복 횟수를 높게 두기보다, 대부분의 오브젝트는 전역 기본값을 따르게 하고 안정성이 필요한 Rigidbody만 개별 값을 높이는 편이 적절합니다.

<br>

---

## 정적 콜라이더 이동의 비용

[물리 최적화 (1)](/dev/unity/PhysicsOptimization-1/)에서 확인한 것처럼, 정적 콜라이더는 Rigidbody가 없는 Collider입니다. Unity의 물리 엔진은 이런 Collider를 움직이지 않는 환경 요소로 다룹니다. 바닥, 벽, 기둥처럼 위치가 고정된 오브젝트라면 이 방식이 적절합니다.

문제는 정적 Collider의 Transform을 플레이 중에 자주 바꾸는 경우입니다. 물리 엔진은 해당 Collider를 움직이는 물체로 관리하고 있지 않기 때문에, 위치가 바뀔 때마다 Broadphase에 등록된 충돌 후보 정보를 다시 맞춰야 합니다. 단순히 Rigidbody의 위치가 갱신되는 경우보다 비용이 커질 수 있고, Sleep 상태의 Rigidbody와 상호작용할 때도 의도한 시점에 깨우지 못하는 문제가 생길 수 있습니다.

따라서 플레이 중 위치가 바뀌는 발판, 문, 이동 플랫폼 같은 오브젝트는 정적 Collider로 두기보다 Rigidbody를 함께 사용하는 편이 적절합니다. 중력이나 충돌 반발로 움직일 필요가 없고 스크립트가 위치를 제어하는 오브젝트라면 **Kinematic Rigidbody**(`Rigidbody.isKinematic = true`)를 사용합니다. 이렇게 구성하면 물리 엔진이 해당 Collider를 움직일 수 있는 물체로 다루므로, 정적 Collider를 Transform으로 직접 움직일 때보다 안정적으로 갱신됩니다.

<br>

---

## 마무리

- Layer Collision Matrix와 LayerMask는 불필요한 충돌 후보를 줄여, Broadphase 이후 단계로 넘어가는 작업량을 줄입니다.
- 물리 결과가 필요 없는 구간에서는 `Physics.Simulate()` 호출 자체를 제어해 물리 스텝 실행 비용을 줄일 수 있습니다.
- 2D 게임에서는 2D 물리 컴포넌트를 사용해, 3D 물리 계산과 축 고정 문제를 피하는 편이 적절합니다.
- 물리적 반응이 필요 없는 영역 판정은 Trigger를 사용하고, 반복 물리 쿼리는 NonAlloc 함수로 결과 배열 할당을 줄입니다.
- Fixed Timestep과 Solver Iteration은 CPU 비용과 물리 반응의 안정성을 함께 바꾸므로, Profiler와 플레이 테스트를 기준으로 조정해야 합니다.
- 플레이 중 움직이는 환경 Collider는 정적 Collider로 두기보다 Kinematic Rigidbody를 함께 사용해 물리 엔진이 움직임을 추적할 수 있게 구성하는 편이 적절합니다.

물리 최적화는 한 가지 설정으로 해결되는 문제가 아닙니다. 충돌 후보를 줄이고, 물리 스텝을 필요한 시점에만 실행하고, 충돌 반응이 필요한 경우와 감지만 필요한 경우를 구분해야 합니다. 그다음 Fixed Timestep, Solver Iteration, Kinematic Rigidbody 같은 설정을 프로젝트의 물리 의존도에 맞춰 조정하는 흐름이 적절합니다.

[파티클과 애니메이션 (1)](/dev/unity/ParticleAndAnimation-1/)에서는 물리 시스템 다음으로, 화면 효과와 움직임을 구성하는 파티클 시스템의 비용 구조를 다룹니다. CPU 시뮬레이션, GPU 렌더링, 오버드로우, 파티클 수 예산을 중심으로 살펴봅니다.

<br>

---

**관련 글**
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)

**시리즈**
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- **물리 최적화 (2) - 물리 최적화 전략** (현재 글)

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
- **물리 최적화 (2) - 물리 최적화 전략** (현재 글)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
