---
layout: single
title: "스크립트 최적화 (2) - Unity API와 실행 비용 - soo:bak"
date: "2026-02-15 21:46:00 +0900"
description: GetComponent 캐싱, Find 비용, Camera.main, Update 오버헤드, Transform 배치 연산, NonAlloc 패턴을 설명합니다.
tags:
  - Unity
  - 최적화
  - API
  - 스크립트
  - 모바일
---

## C# 할당에서 Unity API로

[스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서는 C# 수준의 할당 패턴을 다루었습니다. string 연결, LINQ, 박싱 등 C# 코드 자체에서 발생하는 힙 할당이 GC 부담의 원인이 된다는 점을 확인했습니다.

<br>

하지만 C# 코드 자체의 할당을 모두 제거해도, Unity 게임의 스크립트 비용이 충분히 낮아지지 않는 경우가 있습니다. Unity 엔진은 C++로 작성되어 있고, C# 스크립트가 Unity API를 호출하면 관리 코드(C#)에서 네이티브 코드(C++)로 경계를 넘는 전환이 발생합니다.

`transform.position`을 읽거나 `GetComponent<T>()`를 호출하는 것은 C# 코드에서 한 줄이지만, 내부적으로는 이 경계를 넘어 네이티브 엔진에 접근합니다.

매 프레임 이런 호출이 수백 번 반복되면, 경계 전환 비용만으로도 프레임 예산의 상당 부분을 차지할 수 있습니다. 여기에 씬 전체를 검색하는 API, 호출 자체만으로 오버헤드가 있는 콜백, 매번 배열을 새로 할당하는 물리 쿼리까지 더해지면 비용은 더욱 커집니다.

<br>

이 글에서는 Unity 스크립팅에서 자주 사용되면서도 비용이 높은 API들을 하나씩 확인하고, 각각의 대안을 정리합니다.

---

## GetComponent 캐싱

### GetComponent의 동작 방식

`GetComponent<T>()`는 앞서 설명한 관리-네이티브 경계를 넘어, 게임 오브젝트에 부착된 컴포넌트 목록을 순회하며 타입을 비교합니다. 이 경계를 넘을 때 **마샬링(Marshalling)**이 필요합니다.

마샬링이란 C#과 C++이 서로 다른 방식으로 데이터를 메모리에 저장하기 때문에, 한쪽의 데이터를 다른 쪽이 이해할 수 있는 형식으로 변환하는 과정입니다. `int`, `float` 같은 단순 타입은 양쪽의 메모리 레이아웃이 동일하여 변환 없이 전달되지만, `string`이나 참조 타입 배열 등은 실제 데이터 복사나 변환이 필요합니다.

이 변환 과정 자체가 순수 C# 메서드 호출보다 비용이 높습니다.

<br>

```
  C# (관리 코드)                  C++ (네이티브 코드)
       │                             │
       │─── 관리 → 네이티브 전환 ──────►│
       │                             │ 컴포넌트 목록에서 타입 T 탐색
       │◄── 네이티브 → 관리 전환 ───────│
       │                             │
    결과 수신
```

컴포넌트가 적은 게임 오브젝트에서는 순회 비용이 미미합니다. 하지만 이 함수를 매 프레임 호출하면, 네이티브 전환 비용과 순회 비용이 프레임마다 반복됩니다. 결과는 항상 같은데 매번 처음부터 다시 검색하는 셈입니다.

### 캐싱 패턴

`Awake()`나 `Start()`에서 한 번 호출하여 결과를 멤버 변수에 저장하면, 이후에는 변수 접근만으로 컴포넌트를 사용할 수 있습니다.

<br>

```csharp
// 매 프레임 GetComponent 호출 → 프레임마다 네이티브 전환 + 순회
void Update()
{
    Rigidbody rb = GetComponent<Rigidbody>();
    rb.AddForce(Vector3.up);
}
```

<br>

```csharp
// Awake()에서 한 번만 호출하여 캐시 → Update()에서는 필드 접근만 발생
Rigidbody _rb;

void Awake()
{
    _rb = GetComponent<Rigidbody>();
}

void Update()
{
    _rb.AddForce(Vector3.up);
}
```

### GetComponentInChildren과 GetComponentInParent

`GetComponentInChildren<T>()`은 자기 자신과 모든 자식 오브젝트의 컴포넌트를 재귀적으로 순회합니다. 자식 계층이 깊을수록 순회 범위가 넓어지고, 비용도 비례하여 증가합니다.

<br>

```
Root (호출 지점)
 ├── Child A
 │     ├── Child A-1
 │     └── Child A-2
 ├── Child B
 │     └── Child B-1
 └── Child C

→ Root 포함 7개 오브젝트의 컴포넌트를 모두 검사
```

<br>

`GetComponentInParent<T>()`는 반대 방향으로, 자기 자신에서 루트까지 부모를 순회합니다. 계층이 깊을수록 순회 거리가 길어집니다.

<br>

이 함수들도 결과가 런타임에 바뀌지 않는다면 캐싱이 필요합니다. `GetComponentInChildren`은 자식 수에 비례하여 비용이 증가하므로, 자식이 수십 개인 프리팹에서 매 프레임 호출하면 비용이 커집니다.

---

## Find 계열 함수의 비용

GetComponent 계열은 하나의 게임 오브젝트 내부에서 컴포넌트를 검색합니다. 하지만 특정 오브젝트 자체를 찾아야 할 때는 검색 범위가 씬 전체로 넓어집니다.

### GameObject.Find()

`GameObject.Find(string name)`는 씬에 존재하는 모든 활성 게임 오브젝트를 순회하면서 이름을 비교합니다. 씬의 활성 게임 오브젝트 수를 n이라 하면, 검색 시간은 n에 비례합니다(시간 복잡도 O(n)).

<br>

```
GameObject.Find("Player")

씬의 활성 오브젝트: Enemy1, Tree01, Tree02, Rock, NPC_A, ... Player
                                                               ↑ 발견
→ 일치하는 이름을 찾을 때까지 순회 (O(n))
```

<br>

씬에 오브젝트가 많을수록 검색 시간이 선형적으로 증가합니다. 이 함수를 `Update()`에서 매 프레임 호출하면 프레임마다 씬 전체를 순회합니다.

### FindObjectOfType과 FindObjectsOfType

`FindObjectOfType<T>()`는 씬의 모든 활성 오브젝트에서 특정 타입의 컴포넌트를 검색합니다. `GameObject.Find()`가 이름으로 검색하는 것과 달리, 타입으로 검색합니다. 검색 범위는 동일하게 씬 전체입니다.

<br>

`FindObjectsOfType<T>()`는 해당 타입의 모든 컴포넌트를 배열로 반환합니다. 배열을 새로 생성하므로 힙 할당이 발생합니다. 검색 비용에 할당 비용까지 더해집니다.

```
함수                        검색 기준    할당         비용
──────────────────────────────────────────────────────────
GameObject.Find()           이름         없음         O(n)
FindObjectOfType<T>()       타입         없음         O(n)
FindObjectsOfType<T>()      타입         배열 생성    O(n) + 할당
```

<br>

세 함수 모두 검색 범위가 씬 전체이므로, 결과가 바뀌지 않는다면 초기화 시점에 캐싱하는 것이 원칙입니다.

### 대안: 직접 참조와 이벤트

Find 계열 함수를 사용하지 않고 오브젝트 간 참조를 설정하는 방법은 여러 가지입니다.

<br>

**Inspector 직접 연결.** MonoBehaviour의 public 필드나 `[SerializeField]` 필드에 Inspector에서 오브젝트를 드래그 앤 드롭으로 할당합니다. 씬 로드 시점에 참조가 이미 설정되어 있으므로, 런타임 검색이 필요 없습니다.

<br>

```csharp
[SerializeField] Transform _player;

void Update()
{
    float dist = Vector3.Distance(transform.position, _player.position);
    // 런타임 검색 없음 — 씬 로드 시 참조가 직렬화되어 있음
}
```

<br>

**이벤트 시스템.** 오브젝트 A가 오브젝트 B를 직접 참조하는 대신, 이벤트를 발행하고 B가 이를 구독하는 구조입니다. 오브젝트 간 직접 참조가 제거되므로 Find가 필요 없고, 결합도(coupling)도 낮아집니다.

<br>

**DI 프레임워크.** VContainer, Zenject 등의 DI(Dependency Injection) 프레임워크를 사용하면, 오브젝트 간 참조를 프레임워크가 주입하므로 Find가 불필요합니다.

---

## Camera.main의 비용

앞서 살펴본 `Find` 계열 함수와 같은 문제가 `Camera.main`에도 숨어 있습니다. `Camera.main`은 C# 프로퍼티처럼 보이지만, Unity 2020.2 이전 버전에서는 내부적으로 `FindGameObjectWithTag("MainCamera")`를 호출합니다. 태그가 "MainCamera"인 게임 오브젝트를 씬에서 매번 검색하는 구조입니다.

즉, `Camera.main`에 접근할 때마다 `FindGameObjectWithTag("MainCamera")`가 실행되어 씬의 태그를 순회하고, 찾은 오브젝트에서 Camera 컴포넌트를 반환합니다. `Update()`에서 `Camera.main.transform.position`을 읽으면 매 프레임 태그 검색이 실행되고, 여러 스크립트에서 각각 호출하면 같은 검색이 중복됩니다.

### 버전별 차이

Unity 2020.2부터는 엔진 내부에서 `Camera.main`의 결과를 캐싱합니다. 한 번 검색한 뒤 캐시에 저장하고, 이후 호출에서는 캐시된 값을 돌려줍니다. 카메라가 추가되거나 제거될 때만 캐시 갱신이 일어납니다.

<br>

```
Unity 버전          캐싱 여부        매 프레임 비용
──────────────────────────────────────────────────
2020.1 이전         캐싱 없음        매번 태그 검색
2020.2 이후         엔진 내부 캐싱   거의 없음
```

하위 버전 호환이 필요한 프로젝트이거나, 캐싱 동작에 의존하지 않고 명시적으로 관리하고 싶다면 직접 캐싱하는 것이 적합합니다.

<br>

```csharp
Camera _mainCamera;

void Awake() {
    _mainCamera = Camera.main;
}

void Update() {
    Vector3 camPos = _mainCamera.transform.position;
}
```

런타임에 메인 카메라가 교체되는 경우(예: 컷씬 전환)에는, 교체 시점에 캐시를 갱신하는 로직을 추가해야 합니다.

---

## Update() 오버헤드

### 빈 Update()도 비용이 있다

지금까지 `Find`나 `Camera.main`처럼 특정 API 호출의 비용을 살펴보았습니다. `Update()` 오버헤드는 API 선택과 무관하게, 호출 구조 자체에서 발생하는 비용입니다.

MonoBehaviour의 `Update()` 함수는 Unity 엔진이 매 프레임 호출합니다. 이 호출 과정 자체에 비용이 있으며, `Update()`가 비어 있어도 마찬가지입니다.

<br>

Unity 엔진은 C++로 작성된 네이티브 코드에서 C# 관리 코드의 `Update()`를 호출합니다. 이 전환 과정에서 다음과 같은 처리가 일어납니다.

```
네이티브 엔진(C++)              관리 코드(C#)
─────────────────────────────────────────────
MonoBehaviour 목록 순회
  → 네이티브 → 관리 전환  ──→  Update() 실행
  ← 관리 → 네이티브 전환  ←──  반환
  (각 MonoBehaviour마다 반복)
```

<br>

전환 비용은 한 번만 보면 미미합니다. 하지만 오브젝트 수가 늘어나면 누적됩니다. 씬에 1,000개의 오브젝트가 있고 각각 빈 `Update()`를 가지고 있다면, 매 프레임 1,000번의 네이티브-관리 코드 전환이 발생합니다.

<br>

Unity 엔진은 `Update()` 메서드가 정의되어 있는지를 기준으로 호출 목록에 등록합니다. 메서드 내부가 비어 있어도 정의만 되어 있으면 호출 대상에 포함됩니다. 따라서 사용하지 않는 `Update()` 함수는 선언 자체를 제거해야 합니다. 메서드를 제거하면 호출 목록에서 빠지므로, 전환 비용도 사라집니다.

### Update 통합 패턴

개별 오브젝트마다 `Update()`를 두는 대신, 하나의 오브젝트만 `Update()`를 갖고 나머지 오브젝트의 로직을 순수 C# 호출로 실행하는 구조입니다.

<br>

```
┌─────────┐  ┌─────────┐  ┌─────────┐       ┌─────────┐
│ Enemy 1 │  │ Enemy 2 │  │ Enemy 3 │  ...  │Enemy 100│
│Update() │  │Update() │  │Update() │       │Update() │
└─────────┘  └─────────┘  └─────────┘       └─────────┘

→ 100번의 네이티브-관리 전환
```

<br>

```
        ┌──────────────┐
        │ EnemyUpdater │
        │  Update()    │
        └──────┬───────┘
     ┌─────────┼─────────┐
     ▼         ▼         ▼
  Enemy 1   Enemy 2   Enemy 3  ...
  Tick()    Tick()    Tick()

→ 1번의 네이티브-관리 전환
→ 이후는 순수 C# 메서드 호출 (Tick)
```

<br>

`EnemyUpdater`가 `Update()`를 통해 엔진으로부터 호출을 받고, 내부에서 각 오브젝트의 `Tick()` 메서드를 C# 레벨에서 직접 호출합니다. `Tick()`은 MonoBehaviour의 콜백이 아니라 일반 C# 메서드이므로, 네이티브-관리 전환이 발생하지 않습니다. 100개 오브젝트 기준으로 네이티브 전환이 100번에서 1번으로 줄어듭니다. `EnemyUpdater`는 순회와 호출만 담당하고, 각 Enemy의 로직은 `Tick()` 안에 그대로 남아 있으므로 책임이 분산된 상태를 유지합니다.

모든 로직을 한 클래스에 몰아넣는 것이 아니라 Update 호출만 통합하는 구조이며, Unity 공식 성능 가이드에서도 권장하는 최적화 패턴입니다.

<br>

이 패턴은 동일한 로직을 수행하는 다수의 오브젝트(적, 총알, 파티클 등)에 적합합니다. 오브젝트마다 서로 다른 독립적인 로직을 수행하는 경우에는 하나의 Update로 묶기 어렵습니다.

### 이벤트 기반과 코루틴

매 프레임 검사할 필요가 없는 로직은 `Update()` 밖으로 빼는 것이 효과적입니다.

<br>

**이벤트 기반.** 상태가 변할 때만 처리하는 구조입니다. 예를 들어, 체력이 변할 때만 UI를 갱신한다면, `Update()`에서 매 프레임 체력을 확인하는 대신, 체력이 변하는 시점에 이벤트를 발행하고 UI가 이를 구독하여 갱신합니다.

<br>

```csharp
// Update() 방식 — 매 프레임 실행
void Update() {
    if (_currentHp != _previousHp) {
        UpdateHpUI(_currentHp);
        _previousHp = _currentHp;
    }
}
// → 체력이 변하지 않아도 매 프레임 비교 실행
```

<br>

```csharp
// 이벤트 방식 — 변화 시에만 실행
public event Action<int> OnHpChanged;

public void TakeDamage(int amount) {
    _currentHp -= amount;
    OnHpChanged?.Invoke(_currentHp);
}
// → 체력이 변할 때만 UI 갱신 코드 실행
```

<br>

**코루틴.** 일정 주기로 반복해야 하지만 매 프레임까지는 필요 없는 로직에 적합합니다. 예를 들어, 주변 적을 탐색하는 로직은 0.5초마다 한 번 실행해도 충분할 수 있습니다. [Unity와 코루틴](/dev/unity/UnityCoroutine/)에서 코루틴의 동작 원리를 다루었습니다.

<br>

```csharp
IEnumerator ScanEnemies() {
    while (true) {
        PerformScan();
        yield return new WaitForSeconds(0.5f);
    }
}
// → 0.5초마다 한 번 실행
```

<br>

코루틴 내부에서 `new WaitForSeconds()`가 매번 힙 할당을 발생시키므로, 이 객체를 캐싱하면 할당도 제거할 수 있습니다.

<br>

```csharp
WaitForSeconds _wait = new WaitForSeconds(0.5f); // 한 번만 생성

IEnumerator ScanEnemies() {
    while (true) {
        PerformScan();
        yield return _wait; // 할당 없음
    }
}
```

---

## Transform 배치 연산

앞에서는 코루틴의 힙 할당을 줄이는 캐싱 기법을 살펴보았습니다. 이번에는 Unity에서 가장 빈번하게 접근하는 API인 Transform 프로퍼티의 호출 비용과, 이를 줄이는 배치 연산 기법을 다룹니다.

### Transform 접근의 네이티브 비용

`transform.position`, `transform.rotation`, `transform.localScale` 등의 프로퍼티는 C# 프로퍼티처럼 보이지만, 내부적으로 네이티브 엔진 코드를 호출합니다. 값을 읽을 때도, 쓸 때도 네이티브 전환이 발생합니다.

<br>

```
C# 코드                               네이티브 엔진(C++)
──────────────────────────────────────────────────────────
Vector3 pos = transform.position;
  → 관리 → 네이티브 전환  ──→  월드 위치 계산
  ← 네이티브 → 관리 전환  ←──  Vector3 값 반환
```

한 프레임 안에서 `transform.position`을 여러 번 읽으면, 같은 네이티브 호출이 반복됩니다.

```csharp
// 비효율적인 패턴 — 네이티브 호출 3번
void Update() {
    float x = transform.position.x;
    float y = transform.position.y;
    float z = transform.position.z;
}
```

<br>

```csharp
// 개선된 패턴 — 네이티브 호출 1번, 이후 로컬 변수 접근
void Update() {
    Vector3 pos = transform.position;
    float x = pos.x;
    float y = pos.y;
    float z = pos.z;
}
```

### position과 rotation 개별 설정의 비용

Unity 엔진은 각 오브젝트의 위치, 회전, 스케일을 하나의 변환 행렬(Transform matrix)로 통합하여 관리합니다. 렌더링과 물리 연산은 이 행렬을 기준으로 동작합니다. `transform.position`을 설정하면, 엔진은 변경된 위치를 반영하여 이 변환 행렬을 다시 계산합니다. `transform.rotation`을 설정해도 마찬가지입니다. 한 프레임에서 position과 rotation을 각각 설정하면, 행렬 재계산이 2번 일어납니다.

<br>

```csharp
// 개별 설정 — 행렬 재계산 2회
transform.position = newPosition;    // 행렬 재계산 1회
transform.rotation = newRotation;    // 행렬 재계산 1회
```

<br>

```csharp
// 배치 설정 — 행렬 재계산 1회
transform.SetPositionAndRotation(newPosition, newRotation);
```

`Transform.SetPositionAndRotation()`은 위치와 회전을 한 번에 설정하고, 행렬 재계산도 한 번만 수행합니다. 네이티브 호출도 2번에서 1번으로 줄어듭니다.

오브젝트 1개에서 이 차이는 미미합니다. 하지만 매 프레임 수백 개 오브젝트의 위치와 회전을 갱신하는 경우(적 이동, 총알 궤적 등)에는 누적 효과가 체감됩니다.

### 부모-자식 계층과 Transform 전파

Unity의 Transform은 부모-자식 계층 구조를 가집니다. 한 오브젝트의 Transform이 변경되면, 그 아래 전체 자식 계층의 월드 좌표가 재계산됩니다.

<br>

```
      Parent  ← position 변경
       ├── Child A     ← 월드 좌표 재계산
       │     ├── A-1   ← 월드 좌표 재계산
       │     └── A-2   ← 월드 좌표 재계산
       ├── Child B     ← 월드 좌표 재계산
       └── Child C     ← 월드 좌표 재계산

→ Parent 하나를 변경했지만, 자식 5개의 월드 좌표도 재계산
```

<br>

자식이 많은 오브젝트의 Transform을 매 프레임 변경하면, 전파되는 재계산 비용이 커집니다. 이를 줄이는 방법은 두 가지입니다.

<br>

첫째, Transform 계층을 가능한 한 얕게 유지합니다. 깊은 계층일수록 전파 단계가 많아집니다. 시각적으로 부모-자식 관계가 필요 없는 오브젝트는 계층에서 분리하는 것이 좋습니다.

<br>

둘째, `transform.localPosition`과 `transform.localRotation`을 사용합니다. Transform은 내부적으로 부모 기준의 로컬 좌표를 저장합니다. `transform.position`(월드 좌표)을 설정하면, Unity는 이 월드 좌표를 부모 기준의 로컬 좌표로 변환하기 위해 부모의 역행렬을 곱하는 연산을 추가로 수행합니다.

<br>

`transform.localPosition`을 직접 설정하면 이 변환 과정을 건너뛰므로, 부모-자식 계층에서 Transform을 변경할 때는 가능한 한 로컬 좌표를 사용하는 것이 효율적입니다.

---

## NonAlloc 물리 쿼리

Transform 접근 비용을 줄이는 방법을 살펴보았으니, 이번에는 물리 쿼리에서 발생하는 힙 할당 문제와 그 해결 방법을 다룹니다. 물리 쿼리란 물리 엔진에 공간적 질문을 던지는 함수로, "이 광선이 무언가에 부딪히는가?"(Raycast)나 "이 구 범위 안에 어떤 콜라이더가 있는가?"(OverlapSphere) 등이 해당됩니다.

### 기본 물리 쿼리의 할당 문제

적 탐지, 시야 확인, 지형 판정 등 게임 로직에서는 레이캐스트나 오버랩 검사를 자주 사용합니다. `Physics.RaycastAll()`, `Physics.OverlapSphere()`, `Physics.SphereCastAll()` 등의 함수는 호출할 때마다 결과를 담을 배열을 새로 생성합니다. 이 배열은 힙에 할당되며, 사용이 끝나면 GC의 수거 대상이 됩니다.

<br>

```csharp
RaycastHit[] hits = Physics.RaycastAll(origin, direction, maxDistance);
// → 호출할 때마다 RaycastHit[] 배열을 새로 생성 (힙 할당)
// → 이전 호출에서 생성한 배열은 GC 수거 대상
```

<br>

이런 쿼리를 매 프레임 수행하면, 매 프레임 배열이 할당되고 GC 부담이 누적됩니다.

### NonAlloc 패턴

Unity는 대부분의 물리 쿼리에 NonAlloc 버전을 제공합니다. NonAlloc 함수는 미리 만들어둔 배열을 인자로 받아, 그 배열에 결과를 채웁니다. 배열을 새로 만들지 않으므로 힙 할당이 발생하지 않습니다.

<br>

```csharp
RaycastHit[] _hitBuffer = new RaycastHit[32]; // 한 번만 생성

void Update() {
    int hitCount = Physics.RaycastNonAlloc(
        origin, direction, _hitBuffer, maxDistance
    );

    for (int i = 0; i < hitCount; i++) {
        ProcessHit(_hitBuffer[i]);
    }
}
// → _hitBuffer를 재사용하므로 Update()에서 힙 할당 없음
// → 반환값은 실제로 채워진 결과 수
```

NonAlloc 함수의 반환값은 배열에 채워진 결과의 수입니다. 배열 크기보다 결과가 많으면, 배열 크기만큼만 채워지고 나머지는 무시됩니다. 따라서 배열 크기를 예상 최대 결과 수에 맞춰 설정해야 합니다.

### 주요 NonAlloc 함수 목록

```
기본 함수                        NonAlloc 버전
───────────────────────────────────────────────────────────
Physics.RaycastAll()             Physics.RaycastNonAlloc()
Physics.OverlapSphere()          Physics.OverlapSphereNonAlloc()
Physics.SphereCastAll()          Physics.SphereCastNonAlloc()
Physics.OverlapBox()             Physics.OverlapBoxNonAlloc()
Physics.BoxCastAll()             Physics.BoxCastNonAlloc()
Physics.CapsuleCastAll()         Physics.CapsuleCastNonAlloc()

Physics2D.RaycastAll()           Physics2D.RaycastNonAlloc()
Physics2D.OverlapCircleAll()     Physics2D.OverlapCircleNonAlloc()
```

위 표에서 볼 수 있듯이, 2D 물리 쿼리에도 동일한 NonAlloc 버전이 존재합니다.

### 배열 크기 설정

배열 크기를 너무 작게 잡으면 결과가 잘리고, 너무 크게 잡으면 메모리를 낭비합니다. 게임의 특성에 맞추어 적절한 크기를 설정해야 합니다.

<br>

```
용도                        예상 최대 결과 수     권장 배열 크기
──────────────────────────────────────────────────────────────
전방 레이캐스트 (벽 검사)         1~3                  8
범위 내 적 탐지                   5~15                32
폭발 범위 오브젝트 검출           10~50               64
```

<br>

결과가 배열 크기를 초과하는 상황이 발생한다면, 배열 크기를 늘리거나 쿼리 조건(거리, 레이어 마스크 등)을 더 제한하여 결과 수를 줄이는 것이 좋습니다.

---

## 기타 비용이 높은 API 패턴

앞에서 다룬 API 외에도, Unity 스크립팅에서 비용이 예상보다 높은 패턴이 몇 가지 더 있습니다.

### CompareTag와 문자열 비교

`gameObject.tag == "Enemy"`는 내부적으로 `gameObject.tag` 프로퍼티가 새 string을 생성합니다. 이 string은 힙에 할당되며 GC 대상이 됩니다. `gameObject.CompareTag("Enemy")`는 string을 생성하지 않고 네이티브 레벨에서 직접 비교하므로, 할당이 없습니다.

<br>

```csharp
// 힙 할당 발생 — tag 프로퍼티가 새 string을 생성
gameObject.tag == "Enemy"

// 힙 할당 없음 — 네이티브 레벨에서 직접 비교
gameObject.CompareTag("Enemy")
```

### SendMessage의 비용

`SendMessage(string methodName)`은 게임 오브젝트에 부착된 모든 MonoBehaviour에서 해당 이름의 메서드를 검색하고 호출합니다. 이 과정에서 **리플렉션(Reflection)**을 사용합니다. 리플렉션은 런타임에 타입 정보를 조사하고 메서드를 동적으로 찾는 기술입니다. 컴파일 시점에 호출 대상이 확정되는 직접 호출과 달리, 리플렉션은 매번 탐색이 필요하므로 비용이 높습니다.

`SendMessage`는 메서드 이름을 문자열로 받기 때문에, 이름을 잘못 입력해도 컴파일 시점에 오류를 잡을 수 없습니다.

직접 메서드 호출이나 인터페이스 기반 호출로 대체하는 것이 성능과 유지보수 양쪽에 모두 유리합니다.

### Debug.Log의 릴리스 빌드 비용

`Debug.Log()`는 개발 중 디버깅에 사용하지만, 릴리스 빌드에서도 제거되지 않습니다. 로그 문자열을 매번 생성하므로 힙 할당이 발생하고, 콘솔 출력 자체도 비용이 있습니다. 릴리스 빌드에서는 `Debug.Log()`를 조건부 컴파일(Conditional attribute)이나 전처리기 지시문으로 제거해야 합니다.

<br>

```csharp
#if UNITY_EDITOR
    Debug.Log("디버그 메시지");
#endif
// → 에디터에서만 실행, 빌드에서는 코드 자체가 제거됨
```

---

## 마무리

- Unity API의 한 줄 호출이 내부적으로 네이티브 경계 전환, 씬 전체 순회, 배열 힙 할당 등의 비용을 발생시킬 수 있습니다.
- GetComponent, Find 계열, Camera.main은 결과가 바뀌지 않는다면 캐싱하여 반복 호출을 제거합니다.
- 빈 Update()는 선언 자체를 제거하고, 다수 오브젝트는 Update 통합 패턴으로 네이티브 전환 횟수를 줄입니다.
- Transform은 SetPositionAndRotation()으로 행렬 재계산을 줄이고, 물리 쿼리는 NonAlloc 버전으로 매 프레임 할당을 제거합니다.
- CompareTag, 조건부 컴파일 등 작은 습관도 프레임 전체에서 누적 효과를 만듭니다.

이들의 공통점은 "비용이 발생하는 지점을 정확히 알고, 그 빈도를 줄이는 것"입니다. 네이티브 전환 자체는 제거할 수 없지만, 캐싱과 배치로 전환 횟수를 줄이고, NonAlloc과 CompareTag로 힙 할당을 제거하면, 같은 로직을 더 적은 비용으로 실행할 수 있습니다.

<br>

힙 할당을 줄여야 하는 근본적인 이유는 **가비지 컬렉션(GC)** 때문입니다. 힙에 할당된 객체는 더 이상 참조되지 않으면 GC가 수거하고, GC 동작 중에는 게임 로직이 멈추어 프레임 드롭으로 이어집니다. 모바일에서는 이 GC 스파이크가 특히 두드러집니다.

GC가 언제, 어떻게 동작하는지를 이해하면 할당을 줄이는 것 이상의 최적화가 가능합니다.

[메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서 GC 알고리즘의 특성, 메모리 풀링, Incremental GC 등 메모리 관리 전반을 다룹니다.

<br>

---

**관련 글**
- [Unity와 코루틴](/dev/unity/UnityCoroutine/)
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)

**시리즈**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- **스크립트 최적화 (2) - Unity API와 실행 비용 (현재 글)**
