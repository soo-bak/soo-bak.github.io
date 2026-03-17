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

[스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서는 string 연결, LINQ, 박싱 등 C# 코드에서 발생하는 힙 할당이 GC 부담으로 이어지는 과정을 다뤘습니다.

C# 코드의 힙 할당 외에도, Unity API 호출 자체에 숨은 비용이 있습니다.
Unity 엔진은 C++로 작성되어 있어, C# 스크립트가 Unity API를 호출할 때마다 관리 코드(C#)에서 네이티브 코드(C++)로 경계를 넘어야 합니다.
이때 데이터 형식을 맞추는 **마샬링(Marshalling)**이 발생합니다. C#과 C++은 같은 데이터라도 내부 표현이 달라, 경계를 넘을 때 상대가 읽을 수 있는 형식으로 변환해야 합니다.
`int`, `float` 같은 숫자 타입은 양쪽 표현이 같아서 변환 없이 전달되지만, `string`이나 배열은 데이터를 복사해야 하므로 전환 비용이 더 큽니다.

`transform.position`을 읽거나 `GetComponent<T>()`를 호출하는 것은 C# 한 줄이지만, 내부적으로는 매번 이 경계를 넘어 네이티브 엔진에 접근합니다.

경계 전환 외에도, 씬 전체를 순회하는 검색 API, 호출할 때마다 배열을 새로 할당하는 물리 쿼리, 호출 자체에 오버헤드가 있는 콜백 등 Unity API에는 C# 코드 표면에서 보이지 않는 비용이 여러 곳에 숨어 있습니다. 이런 호출이 매 프레임 수백 번 반복되면, 프레임 예산의 상당 부분을 차지할 수 있습니다.

이 글에서는 Unity 스크립팅에서 자주 사용되면서도 비용이 높은 API들을 확인하고, 각각의 대안을 정리합니다.

---

## GetComponent의 비용

`GetComponent<T>()`는 Unity 스크립트에서 자주 호출되는 API인 만큼, 경계 전환 비용이 누적되기 쉽습니다.

### GetComponent의 동작 방식

`GetComponent<T>()`를 호출하면 관리-네이티브 경계를 넘어 C++ 엔진으로 진입하고, 엔진이 해당 게임 오브젝트의 컴포넌트 목록을 순회하며 타입 T와 일치하는 컴포넌트를 찾아 반환합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- 왼쪽 영역: C# (관리 코드) -->
  <rect x="20" y="10" width="200" height="240" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">C# (관리 코드)</text>

  <!-- 오른쪽 영역: C++ (네이티브 코드) -->
  <rect x="300" y="10" width="200" height="240" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">C++ (네이티브 코드)</text>

  <!-- GetComponent 호출 표시 -->
  <text x="120" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">GetComponent&lt;T&gt;() 호출</text>

  <!-- 화살표 1: 관리 → 네이티브 전환 -->
  <line x1="220" y1="100" x2="294" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,95 300,100 290,105" fill="currentColor"/>
  <text x="260" y="93" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">관리 → 네이티브 전환</text>

  <!-- 네이티브 측 처리 -->
  <text x="400" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">컴포넌트 목록에서</text>
  <text x="400" y="142" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">타입 T 탐색</text>

  <!-- 화살표 2: 네이티브 → 관리 전환 -->
  <line x1="300" y1="170" x2="226" y2="170" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,165 220,170 230,175" fill="currentColor"/>
  <text x="260" y="163" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">네이티브 → 관리 전환</text>

  <!-- 결과 수신 -->
  <text x="120" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">결과 수신</text>

  <!-- 경계선 (점선) -->
  <line x1="260" y1="10" x2="260" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>

</svg>
</div>

이 함수를 매 프레임 호출하면, 경계 전환과 컴포넌트 순회가 프레임마다 반복됩니다. 컴포넌트 구성이 런타임에 바뀌지 않더라도 엔진은 매번 처음부터 검색하므로, 같은 결과를 반복해서 찾는 셈입니다.

한 번 찾은 결과를 `Awake()`나 `Start()`에서 멤버 변수에 저장해 두면, 이후에는 변수 접근만으로 컴포넌트를 사용할 수 있습니다.

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

`GetComponent<T>()`가 한 오브젝트의 컴포넌트만 검색하는 반면, `GetComponentInChildren<T>()`은 자기 자신과 모든 자식 오브젝트의 컴포넌트를 재귀적으로 순회합니다.
자식 계층이 깊을수록 순회 대상이 많아지므로 비용도 증가합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">

  <!-- Root 노드 -->
  <rect x="160" y="10" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="33" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Root</text>

  <!-- Root 라벨 -->
  <text x="300" y="33" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">호출 지점</text>

  <!-- Root → Child A 연결선 -->
  <line x1="180" y1="46" x2="100" y2="86" stroke="currentColor" stroke-width="1.5"/>

  <!-- Root → Child B 연결선 -->
  <line x1="220" y1="46" x2="220" y2="86" stroke="currentColor" stroke-width="1.5"/>

  <!-- Root → Child C 연결선 -->
  <line x1="260" y1="46" x2="340" y2="86" stroke="currentColor" stroke-width="1.5"/>

  <!-- Child A 노드 -->
  <rect x="40" y="86" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="109" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Child A</text>

  <!-- Child B 노드 -->
  <rect x="180" y="86" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="109" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Child B</text>

  <!-- Child C 노드 -->
  <rect x="320" y="86" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="370" y="109" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Child C</text>

  <!-- Child A → A-1 연결선 -->
  <line x1="80" y1="122" x2="55" y2="162" stroke="currentColor" stroke-width="1.5"/>

  <!-- Child A → A-2 연결선 -->
  <line x1="120" y1="122" x2="150" y2="162" stroke="currentColor" stroke-width="1.5"/>

  <!-- Child B → B-1 연결선 -->
  <line x1="240" y1="122" x2="240" y2="162" stroke="currentColor" stroke-width="1.5"/>

  <!-- Child A-1 노드 -->
  <rect x="15" y="162" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Child A-1</text>

  <!-- Child A-2 노드 -->
  <rect x="110" y="162" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Child A-2</text>

  <!-- Child B-1 노드 -->
  <rect x="200" y="162" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Child B-1</text>

  <!-- 구분선 -->
  <line x1="40" y1="230" x2="400" y2="230" stroke="currentColor" stroke-width="1" opacity="0.2"/>

  <!-- 결론 텍스트 -->
  <text x="220" y="258" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">→ Root 포함 7개 오브젝트의 컴포넌트를 모두 검사</text>

</svg>
</div>

`GetComponentInParent<T>()`는 반대 방향으로, 자기 자신에서 루트까지 부모를 순회합니다. 계층이 깊을수록 순회 거리가 길어집니다.

GetComponent와 마찬가지로, 결과가 런타임에 바뀌지 않는다면 캐싱이 적합합니다. 특히 `GetComponentInChildren`은 자식 수에 비례하여 순회 비용이 증가하므로, 자식이 수십 개인 프리팹에서는 캐싱 효과가 큽니다.

---

## Find 계열 함수의 비용

GetComponent 계열이 한 오브젝트 안에서 컴포넌트를 검색한다면, Find 계열은 씬 전체의 오브젝트를 대상으로 검색합니다.

### GameObject.Find()

`GameObject.Find(string name)`는 이름이 일치하는 오브젝트를 찾을 때까지 활성 오브젝트를 순회합니다. 씬의 오브젝트 수에 비례하여 검색 시간이 늘어납니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">

  <!-- 호출 코드 제목 -->
  <text x="270" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GameObject.Find("Player")</text>

  <!-- 순회 화살표 (왼→오) -->
  <line x1="30" y1="65" x2="500" y2="65" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.4"/>
  <polygon points="496,60 506,65 496,70" fill="currentColor" opacity="0.4"/>

  <!-- 오브젝트 박스들 -->
  <rect x="20" y="80" width="72" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="56" y="101" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Enemy1</text>

  <rect x="102" y="80" width="72" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="138" y="101" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Tree01</text>

  <rect x="184" y="80" width="72" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="101" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Tree02</text>

  <rect x="266" y="80" width="60" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="296" y="101" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Rock</text>

  <rect x="336" y="80" width="66" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="369" y="101" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">NPC_A</text>

  <!-- 생략 표시 -->
  <text x="424" y="101" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">...</text>

  <!-- Player 박스 (강조) -->
  <rect x="448" y="80" width="72" height="34" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="484" y="101" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Player</text>

  <!-- 발견 화살표 (위를 가리킴) -->
  <line x1="484" y1="155" x2="484" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="478,124 484,114 490,124" fill="currentColor"/>
  <text x="484" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">발견</text>

  <!-- 결론 텍스트 -->
  <text x="270" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">→ 일치하는 이름을 찾을 때까지 순회 (O(n))</text>

</svg>
</div>

`FindObjectOfType<T>()`와 `FindObjectsOfType<T>()`도 같은 방식으로 동작하지만, 이름 대신 타입으로 검색합니다.
`FindObjectsOfType<T>()`는 해당 타입의 모든 컴포넌트를 배열로 반환하므로, 호출할 때마다 배열이 힙에 할당되어 순회 비용에 할당 비용까지 더해집니다.

| 함수 | 검색 기준 | 할당 | 비용 |
|------|-----------|------|------|
| GameObject.Find() | 이름 | 없음 | O(n) |
| FindObjectOfType\<T\>() | 타입 | 없음 | O(n) |
| FindObjectsOfType\<T\>() | 타입 | 배열 생성 | O(n) + 할당 |

찾으려는 대상이 바뀌지 않는다면, 초기화 시점에 한 번만 호출하여 캐싱하는 것이 효과적입니다.

### 런타임 검색의 대안

캐싱은 검색 횟수를 줄이지만, 애초에 검색이 필요 없는 구조를 만들 수도 있습니다.

Inspector에서 `[SerializeField]` 필드에 오브젝트를 직접 할당해 두면, 참조가 씬 로드 시점에 바로 연결되므로 런타임에 검색할 필요가 없습니다.

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

오브젝트 간 참조 자체를 없애려면, 이벤트를 발행하고 필요한 쪽이 구독하는 구조를 사용할 수 있습니다.
Find 없이도 오브젝트 간 통신이 가능하고 결합도도 낮아집니다. 이벤트 기반 구조는 이 글의 이벤트 기반과 코루틴 섹션에서 코드와 함께 다룹니다.

VContainer, Zenject 등의 DI(Dependency Injection) 프레임워크도 런타임 검색을 제거합니다. DI에서는 오브젝트가 자신이 필요로 하는 참조를 선언만 하면, 프레임워크가 생성 시점에 해당 참조를 자동으로 전달합니다. 오브젝트가 직접 Find로 상대를 찾는 대신, 프레임워크가 연결을 대신 처리하는 구조입니다.

---

## Camera.main의 비용

`Camera.main`은 간단한 프로퍼티 접근처럼 보이지만, Unity 2020.2 이전 버전에서는 내부적으로 `FindGameObjectWithTag("MainCamera")`를 호출합니다. 접근할 때마다 씬의 태그를 순회하여 MainCamera 태그를 가진 오브젝트를 찾고, 그 오브젝트의 Camera 컴포넌트를 반환합니다.

`Update()`에서 `Camera.main.transform.position`을 읽으면 매 프레임 이 태그 검색이 반복되고, 여러 스크립트에서 각각 호출하면 같은 검색이 중복됩니다.

### 버전별 차이

Unity 2020.2부터는 엔진이 `Camera.main`의 결과를 내부적으로 캐싱하여, 카메라가 추가되거나 제거될 때만 갱신합니다.

| Unity 버전 | 캐싱 여부 | 매 프레임 비용 |
|------------|-----------|----------------|
| 2020.1 이전 | 캐싱 없음 | 매번 태그 검색 |
| 2020.2 이후 | 엔진 내부 캐싱 | 거의 없음 |

하위 버전을 지원해야 하거나 캐싱을 직접 관리하고 싶다면, `Awake()`에서 한 번 호출하여 저장해 두는 것이 적합합니다.

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

캐시한 참조는 메인 카메라가 바뀌면 무효가 됩니다. 컷씬 전환 등으로 카메라가 교체된다면, 교체 시점에 캐시를 다시 할당해야 합니다.

---

## Update() 오버헤드

`Update()`는 스크립트가 호출하는 API가 아니라, 엔진이 매 프레임 스크립트를 호출하는 함수입니다.
이 호출에서도 네이티브-관리 전환이 오브젝트마다 발생하고, 매 프레임 실행할 필요가 없는 로직까지 `Update()`에 담기면 낭비가 더해집니다.

### 빈 Update()도 비용이 있다

`Update()` 메서드가 정의되어 있으면, 메서드 내부가 비어 있더라도 Unity 엔진은 매 프레임 그 메서드를 호출합니다.
Unity의 네이티브 엔진(C++)이 MonoBehaviour의 `Update()`를 호출하는 과정에서 네이티브 코드에서 관리 코드로의 왕복 전환이 각 오브젝트마다 발생하기 때문입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">

  <!-- 왼쪽 영역: 네이티브 엔진 (C++) -->
  <rect x="15" y="10" width="220" height="270" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="125" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">네이티브 엔진 (C++)</text>

  <!-- 오른쪽 영역: 관리 코드 (C#) -->
  <rect x="305" y="10" width="220" height="270" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="415" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">관리 코드 (C#)</text>

  <!-- 경계선 (점선) -->
  <line x1="268" y1="10" x2="268" y2="280" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>

  <!-- 왕복 1: 오브젝트 A — U자형 경로 -->
  <text x="100" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">오브젝트 A</text>
  <path d="M 160,70 L 390,70 C 420,70 420,98 390,98 L 160,98" stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.8"/>
  <polygon points="164,93 154,98 164,103" fill="currentColor" opacity="0.8"/>
  <text x="415" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Update()</text>

  <!-- 왕복 2: 오브젝트 B — U자형 경로 -->
  <text x="100" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">오브젝트 B</text>
  <path d="M 160,135 L 390,135 C 420,135 420,163 390,163 L 160,163" stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.8"/>
  <polygon points="164,158 154,163 164,168" fill="currentColor" opacity="0.8"/>
  <text x="415" y="153" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Update()</text>

  <!-- 왕복 3: 오브젝트 C — U자형 경로 -->
  <text x="100" y="212" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">오브젝트 C</text>
  <path d="M 160,200 L 390,200 C 420,200 420,228 390,228 L 160,228" stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.8"/>
  <polygon points="164,223 154,228 164,233" fill="currentColor" opacity="0.8"/>
  <text x="415" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Update()</text>

  <!-- 생략 표시 -->
  <text x="100" y="262" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor" opacity="0.4">...</text>

  <!-- 구분선 -->
  <line x1="40" y1="288" x2="500" y2="288" stroke="currentColor" stroke-width="1" opacity="0.2"/>

  <!-- 결론 텍스트 -->
  <text x="270" y="308" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">→ 오브젝트마다 네이티브-관리 경계를 왕복</text>

</svg>
</div>

이 전환이 `Update()`를 가진 오브젝트마다 발생합니다. 씬에 1,000개의 오브젝트가 있고 각각 빈 `Update()`를 가지고 있다면, 매 프레임 1,000번의 네이티브-관리 코드 전환이 발생합니다.

따라서 사용하지 않는 `Update()`는 선언 자체를 제거하는 것이 좋습니다. 엔진은 메서드의 존재 여부로 호출 대상을 결정하므로, 선언이 없으면 호출 대상에서 빠지고 전환 비용도 사라집니다.

### Update 통합 패턴

빈 `Update()`는 제거할 수 있지만, 매 프레임 로직이 필요한 오브젝트가 수백 개라면 전환 횟수 자체를 줄여야 합니다.
한 오브젝트만 `Update()`를 정의하여 엔진의 콜백을 받고, 그 안에서 나머지 오브젝트의 로직을 순수 C# 호출로 실행하면 전환을 1회로 줄일 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">

  <!-- Enemy 1 -->
  <rect x="20" y="15" width="90" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="36" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Enemy 1</text>
  <text x="65" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Update()</text>

  <!-- Enemy 2 -->
  <rect x="125" y="15" width="90" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="36" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Enemy 2</text>
  <text x="170" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Update()</text>

  <!-- Enemy 3 -->
  <rect x="230" y="15" width="90" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="36" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Enemy 3</text>
  <text x="275" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Update()</text>

  <!-- ... 생략 표시 -->
  <text x="350" y="45" text-anchor="middle" font-family="sans-serif" font-size="15" fill="currentColor" opacity="0.5">...</text>

  <!-- Enemy 100 -->
  <rect x="385" y="15" width="105" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="437" y="36" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Enemy 100</text>
  <text x="437" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Update()</text>

  <!-- 각 박스에서 아래로 내리는 화살표 (네이티브 전환 표시) -->
  <line x1="65" y1="65" x2="65" y2="92" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="61,88 65,96 69,88" fill="currentColor" opacity="0.4"/>

  <line x1="170" y1="65" x2="170" y2="92" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="166,88 170,96 174,88" fill="currentColor" opacity="0.4"/>

  <line x1="275" y1="65" x2="275" y2="92" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="271,88 275,96 279,88" fill="currentColor" opacity="0.4"/>

  <line x1="437" y1="65" x2="437" y2="92" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="433,88 437,96 441,88" fill="currentColor" opacity="0.4"/>

  <!-- 네이티브 전환 표시줄 -->
  <line x1="30" y1="100" x2="510" y2="100" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>
  <text x="270" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">네이티브 ↔ 관리 전환 경계</text>

  <!-- 결론 텍스트 -->
  <text x="270" y="145" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">→ 100번의 네이티브-관리 전환</text>

</svg>
</div>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">

  <!-- EnemyUpdater 박스 -->
  <rect x="185" y="10" width="170" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="31" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">EnemyUpdater</text>
  <text x="270" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Update()</text>

  <!-- EnemyUpdater에서 아래로 내려가는 화살표 (1회 전환) -->
  <line x1="270" y1="60" x2="270" y2="80" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="266,76 270,84 274,76" fill="currentColor" opacity="0.4"/>

  <!-- 네이티브 전환 표시줄 -->
  <line x1="30" y1="88" x2="510" y2="88" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>
  <text x="270" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">네이티브 ↔ 관리 전환 경계 (1회만 통과)</text>

  <!-- EnemyUpdater → 각 Enemy 분기선 -->
  <line x1="270" y1="108" x2="65" y2="125" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="270" y1="108" x2="195" y2="125" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="270" y1="108" x2="345" y2="125" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="270" y1="108" x2="475" y2="125" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>

  <!-- 분기 화살표 끝 -->
  <polygon points="61,122 65,130 69,122" fill="currentColor" opacity="0.4"/>
  <polygon points="191,122 195,130 199,122" fill="currentColor" opacity="0.4"/>
  <polygon points="341,122 345,130 349,122" fill="currentColor" opacity="0.4"/>
  <polygon points="471,122 475,130 479,122" fill="currentColor" opacity="0.4"/>

  <!-- Enemy 1 -->
  <rect x="20" y="130" width="90" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Enemy 1</text>
  <text x="65" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Tick()</text>

  <!-- Enemy 2 -->
  <rect x="150" y="130" width="90" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="195" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Enemy 2</text>
  <text x="195" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Tick()</text>

  <!-- Enemy 3 -->
  <rect x="300" y="130" width="90" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="345" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Enemy 3</text>
  <text x="345" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Tick()</text>

  <!-- ... 생략 표시 -->
  <text x="420" y="155" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">...</text>

  <!-- Enemy N -->
  <rect x="430" y="130" width="90" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="475" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Enemy N</text>
  <text x="475" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Tick()</text>

  <!-- 결론 텍스트 -->
  <text x="270" y="192" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">→ 1번의 네이티브-관리 전환, 이후는 순수 C# 메서드 호출 (Tick)</text>

</svg>
</div>

```csharp
// Enemy는 Update()를 정의하지 않음 → 호출 목록에 등록되지 않음
public class Enemy : MonoBehaviour {
    public void Tick() {
        // 이동, AI 등 프레임별 로직
    }
}

// EnemyUpdater만 Update()를 가짐 → 네이티브 전환 1회
public class EnemyUpdater : MonoBehaviour {
    List<Enemy> _enemies = new List<Enemy>();

    void Update() {
        for (int i = 0; i < _enemies.Count; i++) {
            _enemies[i].Tick();
        }
    }
}
```

<br>

`EnemyUpdater`가 엔진의 `Update()` 콜백을 받고, 내부에서 각 `Enemy`의 `Tick()`을 직접 호출합니다.
`Tick()`은 엔진 콜백이 아닌 일반 C# 메서드이므로 네이티브-관리 전환이 발생하지 않습니다. 100개 오브젝트 기준으로 전환이 100번에서 1번으로 줄어듭니다.

각 Enemy의 로직은 `Tick()` 안에 그대로 남고, `EnemyUpdater`는 순회와 호출만 담당합니다.

### 이벤트 기반과 코루틴

전환 횟수를 줄이는 것과 별개로, 매 프레임 실행할 필요가 없는 로직은 `Update()` 자체에서 빼는 것이 효과적입니다.

상태가 변할 때만 반응하면 되는 로직에는 이벤트 기반 구조가 효과적입니다.
체력 UI 갱신을 예로 들면, `Update()`에서는 변화가 없어도 매 프레임 비교를 실행하지만, 이벤트를 사용하면 체력이 실제로 변하는 시점에만 코드가 실행됩니다.

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

매 프레임은 아니지만 일정 주기로 반복해야 하는 로직은 코루틴으로 `Update()` 밖으로 옮길 수 있습니다. 예를 들어, 주변 적 탐색은 0.5초마다 한 번이면 충분할 수 있습니다.

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

`new WaitForSeconds()`는 호출할 때마다 객체를 힙에 할당합니다. 필드에 한 번만 생성해 두면 이 할당을 제거할 수 있습니다.

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

## Transform 배치 연산

Transform의 프로퍼티는 게임 로직에서 빈번하게 접근되는 만큼, 비용이 누적되기 쉽습니다.

### Transform 접근의 네이티브 비용

`transform.position`, `transform.rotation`, `transform.localScale` 등의 프로퍼티는 필드 접근처럼 가벼워 보이지만, 값을 읽을 때도 쓸 때도 내부적으로 네이티브 전환이 발생합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">

  <!-- 왼쪽 영역: C# 코드 -->
  <rect x="15" y="10" width="210" height="200" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">C# 코드</text>

  <!-- 오른쪽 영역: 네이티브 엔진(C++) -->
  <rect x="335" y="10" width="210" height="200" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="440" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">네이티브 엔진 (C++)</text>

  <!-- 경계선 (점선) -->
  <line x1="280" y1="10" x2="280" y2="210" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>

  <!-- C# 호출 코드 -->
  <text x="120" y="72" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Vector3 pos =</text>
  <text x="120" y="88" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">transform.position;</text>

  <!-- 화살표 1: 관리 → 네이티브 전환 -->
  <line x1="225" y1="110" x2="329" y2="110" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="325,105 335,110 325,115" fill="currentColor"/>
  <text x="280" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">관리 → 네이티브 전환</text>

  <!-- 네이티브 측 처리 -->
  <text x="440" y="115" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">월드 위치 계산</text>

  <!-- 화살표 2: 네이티브 → 관리 전환 -->
  <line x1="335" y1="150" x2="231" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="235,145 225,150 235,155" fill="currentColor"/>
  <text x="280" y="143" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">네이티브 → 관리 전환</text>

  <!-- 결과 수신 -->
  <text x="440" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Vector3 값 반환</text>

  <!-- C# 측 결과 -->
  <text x="120" y="190" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">pos에 값 저장</text>

</svg>
</div>

스크립트가 한 프레임 안에서 `transform.position`을 여러 번 읽으면, 읽을 때마다 같은 네이티브 호출이 반복됩니다.

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

게임에서는 오브젝트의 위치와 회전을 동시에 변경하는 경우가 흔합니다. 적이 이동하면서 방향을 바꾸거나, 총알이 궤적을 따라 날아갈 때가 대표적입니다. 이때 `transform.position`과 `transform.rotation`을 각각 설정하면, 눈에 보이지 않는 비용이 중복 발생합니다.

<br>

Unity 엔진은 각 오브젝트의 위치, 회전, 스케일을 하나의 **변환 행렬(Transform matrix)**로 통합하여 관리합니다.

렌더링과 물리 연산이 이 행렬을 기준으로 동작하기 때문에, position이나 rotation을 설정할 때마다 엔진은 행렬을 다시 계산합니다.
한 프레임에서 둘을 각각 설정하면 이 재계산이 2번 발생합니다.

<br>

```csharp
// 개별 설정 — 네이티브 호출 2회 + 행렬 재계산 2회
transform.position = newPosition;    // 네이티브 호출 + 행렬 재계산
transform.rotation = newRotation;    // 네이티브 호출 + 행렬 재계산
```

<br>

`Transform.SetPositionAndRotation()`은 위치와 회전을 한 번의 네이티브 호출로 설정하고, 행렬 재계산도 한 번만 수행합니다.

<br>

```csharp
// 배치 설정 — 네이티브 호출 1회 + 행렬 재계산 1회
transform.SetPositionAndRotation(newPosition, newRotation);
```

수백 개 오브젝트가 매 프레임 위치와 회전을 갱신한다면, 이 차이가 프레임 예산에 영향을 줄 수 있습니다.

### 부모-자식 계층과 Transform 전파

Unity의 Transform은 부모-자식 계층 구조를 가지기 때문에, 부모의 Transform이 변경되면 그 아래 전체 자식의 월드 좌표가 자동으로 재계산됩니다.
캐릭터 아래에 무기, 방패, 이펙트 등 수십 개의 자식이 붙어 있다면, 캐릭터가 이동할 때마다 수십 번의 재계산이 발생합니다.

이 전파 비용을 줄이려면, Transform 계층을 가능한 한 얕게 유지하는 것이 좋습니다. 부모의 움직임을 따라갈 필요가 없는 오브젝트는 계층에서 분리하면 전파 대상이 줄어듭니다.

또한 `transform.position`(월드 좌표) 대신 `transform.localPosition`(로컬 좌표)을 사용하면 추가 연산을 줄일 수 있습니다.
Transform은 내부적으로 부모 기준의 로컬 좌표를 저장하기 때문에, 월드 좌표를 설정하면 엔진이 부모의 역행렬을 곱하는 변환을 추가로 수행합니다. `transform.localPosition`을 직접 설정하면 이 변환을 건너뜁니다.

---

## NonAlloc 물리 쿼리

물리 쿼리는 물리 엔진에 공간적 질문을 던지는 함수입니다. 광선이 무언가에 부딪히는지(Raycast), 구 범위 안에 어떤 콜라이더가 있는지(OverlapSphere), 상자 형태의 경로에 충돌이 있는지(BoxCast) 등 다양한 형태가 있습니다. 호출 빈도가 높은 만큼, 매 호출의 힙 할당이 누적되기 쉽습니다.

### 기본 물리 쿼리의 할당 문제

적 탐지, 시야 확인, 지형 판정 등에 사용하는 `Physics.RaycastAll()`, `Physics.OverlapSphere()`, `Physics.SphereCastAll()` 등은 호출할 때마다 결과 배열을 힙에 새로 생성하고, 사용이 끝난 배열은 GC 수거 대상이 됩니다.

<br>

```csharp
RaycastHit[] hits = Physics.RaycastAll(origin, direction, maxDistance);
// → 호출할 때마다 RaycastHit[] 배열을 새로 생성 (힙 할당)
// → 이전 호출에서 생성한 배열은 GC 수거 대상
```

<br>

이런 쿼리를 매 프레임 수행하면 배열 할당이 누적되어 GC 부담이 커집니다.

### NonAlloc 패턴

이 할당을 제거하기 위해, Unity는 대부분의 물리 쿼리에 NonAlloc 버전을 제공합니다. NonAlloc 함수는 미리 만들어둔 배열을 인자로 받아 결과를 채우므로, 호출할 때마다 배열을 새로 생성하지 않습니다.

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

결과가 배열 크기보다 많으면 배열 크기만큼만 채워지고 나머지는 무시되므로, 배열 크기를 예상 최대 결과 수에 맞춰 설정해야 합니다.

### 주요 NonAlloc 함수 목록

| 기본 함수 | NonAlloc 버전 |
|-----------|---------------|
| Physics.RaycastAll() | Physics.RaycastNonAlloc() |
| Physics.OverlapSphere() | Physics.OverlapSphereNonAlloc() |
| Physics.SphereCastAll() | Physics.SphereCastNonAlloc() |
| Physics.OverlapBox() | Physics.OverlapBoxNonAlloc() |
| Physics.BoxCastAll() | Physics.BoxCastNonAlloc() |
| Physics.CapsuleCastAll() | Physics.CapsuleCastNonAlloc() |
| Physics2D.RaycastAll() | Physics2D.RaycastNonAlloc() |
| Physics2D.OverlapCircleAll() | Physics2D.OverlapCircleNonAlloc() |

### 배열 크기 설정

용도에 따라 예상 결과 수가 다르므로, 배열 크기도 이에 맞춰 조절합니다.

| 용도 | 예상 최대 결과 수 | 권장 배열 크기 |
|------|-------------------|----------------|
| 전방 레이캐스트 (벽 검사) | 1~3 | 8 |
| 범위 내 적 탐지 | 5~15 | 32 |
| 폭발 범위 오브젝트 검출 | 10~50 | 64 |

결과가 초과한다면, 배열을 늘리거나 쿼리 조건(거리, 레이어 마스크 등)을 제한하여 결과 수를 줄일 수 있습니다.

---

## 기타 비용이 높은 API 패턴

### CompareTag와 문자열 비교

`gameObject.tag` 프로퍼티에 접근하면 엔진이 태그 값을 새 string으로 힙에 생성합니다. 반면 `CompareTag()`는 string을 생성하지 않고 네이티브 레벨에서 직접 비교하므로 할당이 발생하지 않습니다.

<br>

```csharp
// 힙 할당 발생 — tag 프로퍼티가 새 string을 생성
gameObject.tag == "Enemy"

// 힙 할당 없음 — 네이티브 레벨에서 직접 비교
gameObject.CompareTag("Enemy")
```

### SendMessage의 비용

`SendMessage(string methodName)`은 게임 오브젝트에 부착된 모든 MonoBehaviour를 순회하며, 문자열로 전달된 이름과 일치하는 메서드를 런타임에 탐색합니다.
이 탐색은 **리플렉션(Reflection)**을 사용하기 때문에, 컴파일 시점에 호출 대상이 확정되는 직접 호출에 비해 비용이 높고, 메서드 이름을 잘못 입력해도 컴파일러가 잡지 못합니다.

직접 메서드 호출이나 인터페이스 기반 호출로 대체하면 런타임 탐색이 사라지고 컴파일 시점 검증도 가능해집니다.

### Debug.Log의 릴리스 빌드 비용

`Debug.Log()`는 디버깅용이지만 릴리스 빌드에도 그대로 남습니다. 호출될 때마다 로그 문자열을 힙에 생성하고 콘솔 I/O도 발생하므로, 전처리기 지시문으로 릴리스 빌드에서 제거하는 것이 좋습니다.

<br>

```csharp
#if UNITY_EDITOR
    Debug.Log("디버그 메시지");
#endif
// → 에디터에서만 실행, 빌드에서는 코드 자체가 제거됨
```

## 마무리

Unity API 한 줄의 호출 뒤에는 네이티브 경계 전환, 씬 순회, 배열 할당 등 C# 코드 표면에서 보이지 않는 비용이 숨어 있습니다.

- GetComponent, Find, Camera.main은 결과가 바뀌지 않는다면 초기화 시점에 캐싱하여 반복 호출을 제거합니다.
- 빈 Update()는 선언을 제거하고, 다수 오브젝트는 통합 패턴으로 네이티브 전환 횟수를 줄입니다. 매 프레임이 불필요한 로직은 이벤트나 코루틴으로 Update() 밖으로 옮깁니다.
- Transform은 SetPositionAndRotation()으로 행렬 재계산을 줄이고, localPosition으로 역행렬 연산을 건너뜁니다.
- 물리 쿼리는 NonAlloc으로, 태그 비교는 CompareTag()로 힙 할당을 제거합니다.
- SendMessage()는 리플렉션을 사용하므로 직접 호출이나 인터페이스로 대체합니다.
- Debug.Log()는 전처리기 지시문으로 릴리스 빌드에서 제거합니다.

네이티브 전환 자체를 없앨 수는 없지만, 캐싱과 배치로 전환 횟수를 줄이고 할당을 제거하면, 같은 로직을 더 적은 비용으로 실행할 수 있습니다.

<br>

힙 할당이 누적되면 GC가 더 자주, 더 오래 실행되어 프레임 드롭으로 이어집니다. GC가 언제, 어떻게 동작하는지를 이해하면 할당을 줄이는 것 이상의 최적화가 가능합니다.

[메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서 GC 알고리즘의 특성, 메모리 풀링, Incremental GC 등 메모리 관리 전반을 다룹니다.

<br>

---

**관련 글**
- [Unity와 코루틴](/dev/unity/UnityCoroutine/)
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)

**시리즈**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- **스크립트 최적화 (2) - Unity API와 실행 비용 (현재 글)**

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
- **스크립트 최적화 (2) - Unity API와 실행 비용** (현재 글)
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
