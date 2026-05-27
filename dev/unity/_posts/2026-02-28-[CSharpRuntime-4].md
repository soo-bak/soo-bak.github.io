---
layout: single
title: "C# 런타임 기초 (4) - 스레딩과 비동기 - soo:bak"
date: "2026-02-28 02:33:00 +0900"
description: 프로세스와 스레드, ThreadPool, Task, async/await, 경쟁 조건, Unity 메인 스레드 제약을 설명합니다.
tags:
  - Unity
  - C#
  - 스레딩
  - 비동기
  - 모바일
---

## 하나의 스레드를 넘어서

[C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서는 GC가 메모리를 회수하는 원리를 다루었습니다.

Mark-and-Sweep으로 더 이상 도달할 수 없는 객체를 찾아 회수하되, Unity의 Boehm GC는 세대를 나누지 않고 압축도 하지 않는 보수적 방식이라 GC 스파이크가 나타날 수 있었습니다.

특히 GC가 도는 동안 C# 스크립트 실행이 통째로 멈추는 Stop-the-World는 프레임 드롭으로 이어지기 쉬웠습니다.

<br>

지금까지 살펴본 타입 시스템, 런타임 컴파일, GC는 모두 코드가 "하나의 실행 흐름"을 따라 흐른다는 전제 위에 서 있었습니다.

하지만 요즘 모바일 CPU는 대체로 4~8개의 코어를 갖추고 있어서, 단일 스레드로만 돌리면 코어 하나만 일하고 나머지는 놀게 됩니다.

경로 탐색이나 물리 시뮬레이션, 대량 데이터 처리처럼 CPU를 오래 붙잡는 작업은 코어 하나로 프레임 예산 16.6ms 안에 끝내기가 어렵기에, 놀고 있는 코어까지 끌어다 쓰는 멀티스레딩이 필요해집니다.

<br>

한편 `Transform.position`이나 `GameObject.SetActive()`처럼 대부분의 Unity API는 메인 스레드에서만 부를 수 있고, 워커 스레드에서 부르면 `UnityException`이 발생합니다.

따라서 멀티스레딩을 들이더라도 이 제약 안에서 작업을 나눠야 합니다.

<br>

이 글에서는 프로세스와 스레드 개념에서 출발해 ThreadPool과 Task, async/await, 경쟁 조건과 동기화, Unity의 메인 스레드 제약을 거쳐, 코루틴과 async/await, Job System을 비교하는 데까지 차례로 살펴봅니다.

---

## 프로세스와 스레드

### 프로세스

**프로세스(Process)**는 OS가 프로그램을 실행할 때마다 하나씩 띄우는 실행 단위입니다.

각 프로세스는 코드 영역과 데이터 영역, 힙, 스택으로 이루어진 독립된 메모리 공간을 따로 갖습니다. 다른 프로세스의 메모리에는 직접 손댈 수 없어서, 한 프로세스가 비정상 종료되더라도 나머지 프로세스는 그 영향을 받지 않습니다.

Unity 게임을 빌드해 실행하면 OS가 프로세스 하나를 띄우고, 게임의 모든 동작은 그 안에서 이루어집니다.

---

### 스레드

**스레드(Thread)**는 프로세스 안에서 실제로 코드가 흐르는 실행 단위입니다.

프로세스가 "프로그램 전체가 올라가는 실행 환경"이라면, 스레드는 그 환경 안에서 한 줄 한 줄 코드를 돌리는 일꾼에 가깝습니다.

한 프로세스는 여러 스레드를 거느릴 수 있고, 이 스레드들은 힙과 데이터 영역을 함께 씁니다. 그래서 여러 스레드가 힙에 놓인 같은 객체를 동시에 읽고 쓸 수도 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 프로세스 외곽 -->
  <rect x="10" y="8" width="500" height="254" rx="8" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="34" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">프로세스</text>
  <!-- 공유 메모리 -->
  <rect x="55" y="48" width="410" height="44" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="75" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">공유 메모리 (힙, 데이터)</text>
  <!-- 상향 화살표 -->
  <line x1="130" y1="92" x2="130" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="130,92 125,102 135,102" fill="currentColor"/>
  <line x1="260" y1="92" x2="260" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,92 255,102 265,102" fill="currentColor"/>
  <line x1="390" y1="92" x2="390" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="390,92 385,102 395,102" fill="currentColor"/>
  <!-- 스레드 1 -->
  <rect x="65" y="142" width="130" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="130" y="165" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 1</text>
  <text fill="currentColor" x="130" y="183" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(스택)</text>
  <!-- 스레드 2 -->
  <rect x="195" y="142" width="130" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="165" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 2</text>
  <text fill="currentColor" x="260" y="183" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(스택)</text>
  <!-- 스레드 3 -->
  <rect x="325" y="142" width="130" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="390" y="165" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 3</text>
  <text fill="currentColor" x="390" y="183" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(스택)</text>
  <!-- 하단 설명 -->
  <text fill="currentColor" x="260" y="228" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.5">각 스레드는 자체 스택을 가지지만, 힙 메모리는 모든 스레드가 공유</text>
</svg>
</div>

<br>

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다룬 것처럼, 지역 변수와 호출 스택이 담기는 스택은 스레드마다 따로 두지만, 힙에 놓인 객체는 여러 스레드가 함께 봅니다.

같은 데이터를 복사 없이 곧장 읽어 쓸 수 있다는 점은 효율적이지만, 둘 이상의 스레드가 그 데이터를 동시에 고치면 예상과 어긋난 결과가 나올 수 있습니다.

---

### 멀티스레드의 이점

요즘 모바일 기기의 CPU는 대체로 4~8개의 코어를 품고 있습니다.

가령 Snapdragon 8 Gen 3는 1 Prime + 5 Performance + 2 Efficiency로 짜인 8코어(Cortex-X4/A720/A520)이고, Apple A17 Pro는 2 Performance + 4 Efficiency로 짜인 6코어입니다.

그런데 스레드 하나는 한 번에 코어 하나에서만 돌기 때문에, 단일 스레드로만 실행하면 코어 하나에 일이 몰리고 나머지 코어는 놀게 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 단일 스레드 섹션 -->
  <text fill="currentColor" x="20" y="20" font-size="13" font-weight="bold" font-family="sans-serif">단일 스레드</text>
  <!-- 코어 1: 긴 바 -->
  <text fill="currentColor" x="20" y="50" font-size="11" font-family="sans-serif" opacity="0.7">코어 1</text>
  <rect x="80" y="36" width="360" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="260" y="51" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">작업 A + B + C</text>
  <!-- 코어 2: 유휴 -->
  <text fill="currentColor" x="20" y="76" font-size="11" font-family="sans-serif" opacity="0.7">코어 2</text>
  <line x1="80" y1="72" x2="440" y2="72" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.3"/>
  <text fill="currentColor" x="260" y="76" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.4">(유휴)</text>
  <!-- 코어 3: 유휴 -->
  <text fill="currentColor" x="20" y="100" font-size="11" font-family="sans-serif" opacity="0.7">코어 3</text>
  <line x1="80" y1="96" x2="440" y2="96" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.3"/>
  <text fill="currentColor" x="260" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.4">(유휴)</text>
  <!-- 총 시간 -->
  <text fill="currentColor" x="456" y="51" font-size="11" font-family="sans-serif" opacity="0.55">30ms</text>
  <!-- 구분선 -->
  <line x1="20" y1="120" x2="500" y2="120" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- 멀티스레드 섹션 -->
  <text fill="currentColor" x="20" y="148" font-size="13" font-weight="bold" font-family="sans-serif">멀티스레드</text>
  <!-- 코어 1: 짧은 바 (작업 A) -->
  <text fill="currentColor" x="20" y="178" font-size="11" font-family="sans-serif" opacity="0.7">코어 1</text>
  <rect x="80" y="164" width="120" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="140" y="179" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">작업 A</text>
  <!-- 코어 2: 짧은 바 (작업 B) -->
  <text fill="currentColor" x="20" y="204" font-size="11" font-family="sans-serif" opacity="0.7">코어 2</text>
  <rect x="80" y="190" width="120" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="140" y="205" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">작업 B</text>
  <!-- 코어 3: 짧은 바 (작업 C) -->
  <text fill="currentColor" x="20" y="230" font-size="11" font-family="sans-serif" opacity="0.7">코어 3</text>
  <rect x="80" y="216" width="120" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="140" y="231" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.7">작업 C</text>
  <!-- 총 시간 -->
  <text fill="currentColor" x="214" y="179" font-size="11" font-family="sans-serif" opacity="0.55">10ms</text>
</svg>
</div>

<br>

작업을 여러 코어에 나눠 동시에 돌리면, 단일 스레드로 30ms 걸리던 일을 10ms까지 줄일 수 있습니다.

이런 이점은 경로 탐색이나 물리 연산, 대량 데이터 처리처럼 CPU를 오래 붙잡는 작업에서 특히 도드라집니다.

I/O 바운드 작업에서도 멀티스레딩은 쓸모가 있습니다. 파일을 읽거나 네트워크 응답을 기다리느라 한 스레드가 멈춰 있는 동안, 다른 스레드가 그 틈에 CPU를 돌릴 수 있기 때문입니다.

---

## Thread 클래스와 스레드 풀

### Thread 클래스

스레드를 코드에서 직접 만들어 보고 싶을 때 가장 먼저 손이 가는 도구가 `System.Threading.Thread` 클래스입니다.

<br>

```csharp
using System.Threading;

void StartWork()
{
    Thread thread = new Thread(DoHeavyWork);
    thread.Start();
}

void DoHeavyWork()
{
    // 이 코드는 새 스레드에서 실행됨
}
```

<br>

`new Thread()`로 스레드 객체를 만든 뒤 `Start()`를 부르면, OS가 새 스레드를 띄워 넘겨받은 메서드를 그 위에서 돌립니다.

다만 스레드를 이렇게 손수 만드는 데는 만만찮은 비용이 따라붙습니다.

OS 커널 오브젝트를 만들고, 스레드 하나마다 약 1MB의 스택 메모리를 미리 잡아 두며(.NET 기본값으로, 플랫폼에 따라 달라질 수 있습니다), 실행 중이던 스레드를 다른 스레드로 바꿀 때마다 레지스터 상태를 저장했다가 되돌리는 컨텍스트 스위칭까지 거쳐야 하기 때문입니다.

그래서 짧은 작업이 자주 들어오는 상황이라면, 매번 스레드를 만들고 버리는 오버헤드가 정작 작업 자체보다 더 커지기도 합니다.

<br>

스레드를 직접 다룰 때 자주 마주치는 `Thread.Sleep()`은 현재 스레드를 OS 수준에서 지정한 시간만큼 멈춰 세웁니다.

스레드가 Sleep에 들어가면 OS 스케줄러가 그 스레드를 실행 대기 큐에서 빼 두었다가, 시간이 다 지나야 다시 큐에 넣어 줍니다.

그동안 해당 스레드는 단 한 줄의 코드도 돌릴 수 없습니다.

<br>

동작 자체는 어디서 부르든 똑같지만, 정작 중요한 것은 **어느 스레드에서 부르느냐**입니다. 멈춰 세우는 대상이 바로 그 스레드라서, 호출하는 스레드가 무엇이냐에 따라 영향이 전혀 달라지기 때문입니다.

Unity의 메인 스레드는 매 프레임 `Update()` → 렌더링 → `LateUpdate()` 순서로 게임 루프를 돌리는 유일한 스레드입니다.

이 스레드에서 `Thread.Sleep()`을 부르면 루프 자체가 멈춰 버려 화면 갱신도, 입력 처리도, 물리 시뮬레이션도 함께 얼어붙으므로, 메인 스레드에서는 결코 써서는 안 됩니다.

<br>

반면 `new Thread()`로 따로 만든 전용 스레드라면 멈추는 것은 그 스레드 하나뿐이고 메인 게임 루프는 멀쩡히 돌아가므로, 이 경우에는 마음 놓고 써도 됩니다.

<br>

조심해야 할 쪽은 스레드 풀에서 빌려 온 워커 스레드입니다.

스레드 풀은 한정된 수의 워커 스레드를 여러 작업이 돌려 쓰는 구조여서, `Thread.Sleep()`으로 워커 스레드를 붙잡아 두면 Sleep이 끝날 때까지 그 스레드가 풀로 돌아오지 못합니다.

이렇게 묶여 버린 스레드가 하나둘 늘어나면 다른 작업이 워커 스레드를 받지 못해 전체 처리량이 떨어지게 됩니다.

<br>

그래서 스레드 풀 안에서 잠시 기다려야 한다면 `Thread.Sleep()` 대신 `await Task.Delay()`를 씁니다.

`await` 키워드를 만나는 순간 현재 메서드의 실행은 그 지점에서 일단 멈추고, 스레드는 곧장 풀로 반환됩니다.

기다리는 동안 `Task.Delay()` 내부에서는 OS 타이머가 시간을 재고, 시간이 다 차면 멈춰 두었던 메서드의 나머지(continuation)를 풀에서 놀고 있는 워커 스레드에 다시 얹어 줍니다.

대기하는 내내 어떤 스레드도 붙잡고 있지 않으므로, 워커 스레드가 바닥나는 일도 생기지 않습니다.

---

### ThreadPool

스레드를 매번 새로 만들고 버리는 비용을 덜어 주려고, .NET 런타임은 미리 만들어 둔 스레드를 빌려 쓰는 **스레드 풀(ThreadPool)**을 마련해 둡니다.

런타임은 워커 스레드(worker thread)를 최소 개수만큼 미리 띄워 두었다가, 작업이 들어오면 놀고 있는 스레드에 맡깁니다.

쉬는 스레드가 하나도 없으면 풀이 새 스레드를 더 만들어 채우며, 정해진 최대치까지는 수요에 맞춰 알아서 늘어납니다.

작업이 끝난 스레드는 버려지지 않고 풀로 되돌아와 다음 일감을 기다립니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Thread (직접 생성) 제목 -->
  <text fill="currentColor" x="20" y="20" font-size="13" font-weight="bold" font-family="sans-serif">Thread (직접 생성)</text>
  <!-- Thread flow: 작업 → 스레드 생성 → 실행 → 폐기 -->
  <rect x="20" y="34" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="50" y="53" text-anchor="middle" font-size="11" font-family="sans-serif">작업</text>
  <line x1="80" y1="49" x2="106" y2="49" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="110,49 103,44 103,54" fill="currentColor"/>
  <rect x="110" y="34" width="100" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="160" y="53" text-anchor="middle" font-size="11" font-family="sans-serif">스레드 생성</text>
  <line x1="210" y1="49" x2="236" y2="49" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,49 233,44 233,54" fill="currentColor"/>
  <rect x="240" y="34" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="270" y="53" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">실행</text>
  <line x1="300" y1="49" x2="326" y2="49" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="330,49 323,44 323,54" fill="currentColor"/>
  <rect x="330" y="34" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="360" y="53" text-anchor="middle" font-size="11" font-family="sans-serif">폐기</text>
  <text fill="currentColor" x="410" y="53" font-size="10" font-family="sans-serif" opacity="0.5">매번 비용 발생</text>
  <!-- 구분선 -->
  <line x1="20" y1="82" x2="500" y2="82" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- ThreadPool (재사용) 제목 -->
  <text fill="currentColor" x="20" y="106" font-size="13" font-weight="bold" font-family="sans-serif">ThreadPool (재사용)</text>
  <!-- Pool box -->
  <rect x="20" y="116" width="280" height="42" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="35" y="135" font-size="10" font-family="sans-serif" opacity="0.55">풀 :</text>
  <rect x="62" y="126" width="64" height="24" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="94" y="142" text-anchor="middle" font-size="9" font-family="sans-serif">스레드 1</text>
  <rect x="134" y="126" width="64" height="24" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="166" y="142" text-anchor="middle" font-size="9" font-family="sans-serif">스레드 2</text>
  <rect x="206" y="126" width="64" height="24" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="238" y="142" text-anchor="middle" font-size="9" font-family="sans-serif">스레드 3</text>
  <!-- Flow: 작업 → 할당 → 실행 → 반환 -->
  <rect x="20" y="174" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="50" y="193" text-anchor="middle" font-size="11" font-family="sans-serif">작업</text>
  <line x1="80" y1="189" x2="116" y2="189" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="120,189 113,184 113,194" fill="currentColor"/>
  <text fill="currentColor" x="165" y="193" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">스레드 할당</text>
  <line x1="210" y1="189" x2="236" y2="189" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,189 233,184 233,194" fill="currentColor"/>
  <rect x="240" y="174" width="60" height="30" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="270" y="193" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">실행</text>
  <!-- 반환 화살표 (점선) -->
  <path d="M 300 189 L 340 189 Q 360 189 360 170 Q 360 137 302 137" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5"/>
  <polygon points="302,137 310,132 310,142" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="380" y="193" font-size="10" font-family="sans-serif" opacity="0.5">반환</text>
  <text fill="currentColor" x="380" y="207" font-size="10" font-family="sans-serif" opacity="0.5">(생성/폐기 없음)</text>
</svg>
</div>

<br>

```csharp
using System.Threading;

void QueueWork()
{
    ThreadPool.QueueUserWorkItem(_ => DoHeavyWork());
}
```

<br>

`ThreadPool.QueueUserWorkItem()`으로 작업을 큐에 넣으면, 풀에 대기 중인 스레드가 작업을 가져가 실행합니다.

스레드 수는 런타임이 자동으로 관리하므로, 개발자가 직접 스레드 수를 조절할 필요가 없습니다.

---

## Task와 TAP

`Thread`와 `ThreadPool`이 해 주는 일은 "스레드에 코드를 얹어 돌린다"는 데까지입니다. 그 이상으로 작업을 들여다보고 제어하려면 손이 많이 가는데, 크게 세 가지에서 막힙니다.

<br>

먼저 작업이 끝났는지 확인하는 것부터 까다롭습니다.

`Thread`에는 완료를 기다리는 `Join()`이 있지만, `Join()`은 호출한 쪽 스레드를 그대로 멈춰 세웁니다.

Unity 메인 스레드에서 부르면 게임 루프가 멈춰 버려 사실상 쓸 수 없고, 그렇다고 블로킹 없이 진행 상황만 엿보려면 완료 여부를 담을 플래그 변수를 직접 만들어 계속 들여다보는 폴링을 짜야 합니다.

`ThreadPool.QueueUserWorkItem()`은 한술 더 떠서, 완료 여부를 물어볼 핸들조차 돌려주지 않습니다.

<br>

결과값을 돌려받는 일도 마찬가지로 번거롭습니다.

`Thread`와 `ThreadPool` 어느 쪽도 작업의 반환값을 호출 측으로 건네주는 길이 없어서, 공유 변수에 결과를 담아 두고 `lock` 따위로 접근을 맞춰 줘야 합니다.

<br>

예외를 처리하는 대목도 걸림돌입니다.

워커 스레드 안에서 예외가 터져도 그것이 호출한 쪽으로 저절로 올라오지는 않습니다.

결국 스레드 안에서 `try-catch`로 직접 붙잡아 오류가 났다는 사실을 따로 손수 전달해야 합니다.

<br>

**Task**는 이 세 가지 골칫거리를 객체 하나로 한꺼번에 풀어 줍니다.

`Task` 객체가 작업이 실행 중인지, 끝났는지, 실패했는지 그 상태를 스스로 들고 있어 `await`로 블로킹 없이 완료를 기다릴 수 있고, `Task<T>`라면 끝났을 때 결과값을 담아 두어 `await` 표현식이 그 값을 바로 돌려줍니다. 워커 스레드에서 터진 예외 역시 `Task` 안에 담겨 있다가 `await`하는 순간 호출한 쪽으로 다시 던져집니다.

<br>

```csharp
using System.Threading.Tasks;

// 결과가 없는 비동기 작업
Task task = Task.Run(() => DoHeavyWork());

// 결과가 있는 비동기 작업
Task<int> taskWithResult = Task.Run(() => CalculateScore());
int score = await taskWithResult;
```

<br>

`Task.Run()`은 넘겨받은 델리게이트를 스레드 풀의 워커 스레드 위에서 돌립니다.

부르자마자 `Task` 객체를 손에 쥐여 주므로, 호출한 쪽은 멈추지 않고 다른 일을 하다가 정작 필요한 시점에 `await`로 완료를 기다리거나 결과를 건네받으면 됩니다.

<br>

이처럼 `Task`를 돌려주는 형태로 비동기 메서드를 짜는 방식을 .NET에서는 **TAP(Task-based Asynchronous Pattern)**이라 부릅니다.

TAP이 자리잡기 전에는 콜백(AsyncCallback)에 기댄 방식을 썼는데, 비동기 작업이 줄줄이 이어지면 콜백 안에 또 콜백이 들어앉으며 흐름을 좇기가 어려워지곤 했습니다.

TAP은 비동기 메서드라면 죄다 `Task`나 `Task<T>`를 돌려주도록 모양을 맞추고, 메서드 이름 끝에 `Async`를 달아 두는 것을 관례로 삼습니다.

<br>

```csharp
async Task<string> LoadDataAsync(string path)
{
    string data = await File.ReadAllTextAsync(path);
    return data;
}
```

<br>

여기에 `async`/`await`까지 더하면, 콜백을 겹겹이 쌓지 않고도 동기 코드를 읽듯 같은 순서로 비동기 흐름을 풀어 쓸 수 있습니다.

---

## async/await의 동작 원리

### 상태 머신 변환

비동기 메서드는 `await` 지점에서 실행을 한 번 멈췄다가, 기다리던 작업이 끝난 뒤 같은 자리에서 다시 이어 가야 합니다.

이렇게 멈췄다 이어 가는 흐름을 풀어내려고 C# 컴파일러는 `async` 메서드를 **상태 머신(State Machine)**으로 바꿔 둡니다.

`await` 지점 하나하나가 상태가 갈리는 경계가 되고, 그때까지 쓰던 지역 변수와 어디까지 실행했는지가 상태 머신의 필드에 담겨 있다가 재개할 때 그대로 되살아납니다.

이 상태 머신을 손수 짜지 않아도 되도록 거들어 주는 **문법적 편의(syntactic sugar)**가 바로 `async`/`await`입니다.

<br>

```csharp
// async 메서드의 컴파일러 변환 (개념적)

// 원본 코드:
  async Task DoWorkAsync()
  {
      var a = await Step1Async();     // await 지점 1
      var b = await Step2Async(a);    // await 지점 2
      ProcessResult(b);
  }

// 컴파일러가 생성하는 상태 머신 (개념적):
  // state 0 → Step1Async 시작 → 미완료 시 양보
  // state 1 → Step1 결과 저장 → Step2Async 시작
  // state 2 → Step2 결과 저장 → ProcessResult 호출
```

<br>

`await` 지점에 닿으면 상태 머신은 먼저 기다리던 작업이 끝났는지부터 살핍니다.

이미 끝나 있으면 그 결과를 꺼내 다음 코드로 곧장 넘어가고, 아직 끝나지 않았으면 지금까지의 상태를 저장해 둔 채 제어를 호출자에게 되돌려줍니다(**양보**, yield).

이렇게 양보하므로 호출자 스레드는 멈춰 서지 않고 그 사이 다른 일을 이어 갈 수 있습니다.

뒤이어 비동기 작업이 끝나면 저장해 둔 지점에서 상태 머신이 다시 깨어나 나머지 코드를 마저 실행합니다.

---

### 비동기와 멀티스레드는 다르다

앞서 본 양보는 스레드를 블로킹하지 않으려는 장치일 뿐, `async`/`await`을 쓴다고 해서 곧 멀티스레드가 되는 것은 아닙니다.

`await`이 약속하는 바는 "이 작업이 끝날 때까지 스레드를 붙잡아 두지 않겠다"는 데까지이지, "이 작업을 다른 스레드에 떠넘겨 돌리겠다"는 뜻이 아니기 때문입니다.

그렇다면 `await` 뒤의 코드를 어느 스레드에서 이어 갈지는 누가 정하느냐 하면, **동기화 컨텍스트(SynchronizationContext)**가 그 역할을 맡습니다.

동기화 컨텍스트는 비동기 작업이 끝난 뒤 그 다음 코드를 어느 스레드에 얹어 이어 갈지를 가려 주는 런타임 장치입니다.

<br>

|  | 비동기 (async/await) | 멀티스레드 |
|---|---|---|
| 핵심 원리 | 작업 완료를 기다리는 동안 스레드를 블로킹하지 않음 | 여러 스레드에서 동시에 코드를 실행 |
| 스레드 동작 | 같은 스레드 또는 다른 스레드에서 재개 가능 | 반드시 여러 스레드가 관여 |
| Unity에서 | `await` 후 → 메인 스레드에서 재개 (`UnitySynchronizationContext`) | `Task.Run()` → 스레드 풀에서 실행 |

<br>

Unity 엔진은 메인 스레드에 `UnitySynchronizationContext`를 미리 걸어 둡니다.

그래서 `await`이 양보하는 순간 이 컨텍스트가 그 뒤를 이을 코드, 즉 연속(continuation)을 붙들어 메인 스레드의 실행 큐에 넣어 두고, Unity 메인 루프가 다음 프레임에 그것을 꺼내 돌립니다.

이런 흐름 덕분에 `await` 다음 코드는 다시 메인 스레드에서 깨어나며, 그 안에서 Unity API를 마음 놓고 부를 수 있습니다.

<br>

반대로 `ConfigureAwait(false)`를 붙이면 이 컨텍스트를 붙드는 단계를 건너뜁니다.

메인 스레드로 굳이 돌아오는 비용을 덜 수 있어 Unity API가 필요 없는 순수 계산에서는 쓸모가 있지만, 그만큼 `await` 다음 코드가 스레드 풀의 어느 스레드에서 깨어날지 장담할 수 없게 됩니다.

이렇게 메인 스레드가 아닌 곳에서 Unity API를 부르면 런타임 에러로 이어집니다.

<br>

다만 `await`에 닿은 그 시점에 작업이 이미 끝나 있었다면, `ConfigureAwait` 설정과 상관없이 스레드를 갈아타지 않고 지금 스레드에서 곧장 다음 코드로 넘어갑니다.

---

## 경쟁 조건과 동기화

### 경쟁 조건 (Race Condition)

여러 스레드가 같은 데이터를 동시에 읽고 고치면, 어느 스레드가 먼저 손을 대느냐에 따라 결과가 들쭉날쭉해지는 **경쟁 조건(Race Condition)**이 생길 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- 공유 변수 -->
  <rect x="150" y="6" width="200" height="30" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="250" y="26" text-anchor="middle" font-size="12" font-weight="bold" font-family="monospace">int counter = 0</text>
  <!-- 컬럼 헤더 -->
  <text fill="currentColor" x="125" y="62" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 A</text>
  <text fill="currentColor" x="375" y="62" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 B</text>
  <!-- 컬럼 구분선 -->
  <line x1="250" y1="48" x2="250" y2="200" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.2"/>
  <!-- 동시 읽기 구간 하이라이트 -->
  <rect x="18" y="72" width="464" height="34" rx="4" fill="currentColor" fill-opacity="0.08"/>
  <!-- Step 1: 동시 읽기 -->
  <text fill="currentColor" x="125" y="94" text-anchor="middle" font-size="11" font-family="monospace">temp = counter → 0</text>
  <text fill="currentColor" x="375" y="94" text-anchor="middle" font-size="11" font-family="monospace">temp = counter → 0</text>
  <!-- Step 2: 증가 -->
  <text fill="currentColor" x="125" y="132" text-anchor="middle" font-size="11" font-family="monospace">temp = temp + 1 → 1</text>
  <text fill="currentColor" x="375" y="132" text-anchor="middle" font-size="11" font-family="monospace">temp = temp + 1 → 1</text>
  <!-- Step 3: 쓰기 -->
  <text fill="currentColor" x="125" y="170" text-anchor="middle" font-size="11" font-family="monospace">counter = temp → 1</text>
  <text fill="currentColor" x="375" y="170" text-anchor="middle" font-size="11" font-family="monospace">counter = temp → 1</text>
  <!-- 동시 읽기 라벨 -->
  <text fill="currentColor" x="488" y="94" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">동시 읽기</text>
  <!-- 구분선 -->
  <line x1="40" y1="200" x2="460" y2="200" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- 결과 -->
  <rect x="100" y="214" width="300" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="250" y="236" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">결과: counter = 1 (기대값: 2)</text>
  <text fill="currentColor" x="250" y="254" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">하나의 증가 연산이 소실됨</text>
</svg>
</div>

<br>

위 그림의 `counter++`는 코드에서는 한 줄이지만, 속을 들여다보면 값을 읽고, 1을 더하고, 다시 써넣는 세 단계로 풀려 실행됩니다.

한 스레드가 써넣기도 전에 다른 스레드가 같은 값을 읽어 가면, 두 스레드가 똑같은 값에서 1씩 더하는 꼴이 되어 한쪽의 증가가 그대로 묻혀 버립니다.

이런 경쟁 조건은 스레드들이 맞물리는 타이밍에 따라 나타났다 안 나타났다 하므로 다시 재현해 보기가 까다롭습니다.

10,000번을 돌려 한 번 비칠까 말까 하거나 특정 기기에서만 모습을 드러내기도 하여, 테스트는 멀쩡히 통과해 놓고 막상 실제 환경에서야 문제가 불거지는 일이 잦습니다.

---

### 동기화 메커니즘

경쟁 조건을 막으려면 여러 스레드가 공유 데이터에 손대는 순간을 서로 어긋나게 **동기화(Synchronization)**해 주어야 합니다.

<br>

**lock 문.**

가장 손쉽게 집어 드는 동기화 도구입니다. `lock` 블록 안에는 한 번에 한 스레드만 들어설 수 있습니다.

<br>

```csharp
private readonly object lockObj = new object();
private int counter = 0;

void IncrementCounter()
{
    lock (lockObj)
    {
        counter++;
    }
}
```

<br>

스레드 A가 `lock` 블록에 먼저 들어가 있으면, 스레드 B는 A가 그 블록을 빠져나올 때까지 문 앞에서 기다립니다.

그 사이 "읽기 → 증가 → 쓰기" 세 단계가 다른 스레드의 끼어듦 없이 한 번에 끝나므로, 밖에서 보면 더 쪼갤 수 없는 하나의 연산, 곧 **원자적(atomic)** 연산처럼 굴러갑니다.

물론 세 단계가 정말 CPU 명령어 하나로 합쳐지는 것은 아니고 명령어 셋은 그대로 실행되지만, `lock`이 상호 배제를 지켜 주는 덕에 그 도중 다른 스레드가 비집고 들어올 틈이 없습니다.

<br>

**Interlocked.**

`lock`이 여러 명령어를 한 블록으로 싸잡아 지켜 준다면, 숫자를 하나 올리거나 값을 갈아 끼우는 정도의 단일 연산만 지키면 될 때는 `Interlocked` 클래스 쪽이 더 잘 맞습니다.

`Interlocked`는 CPU가 갖춘 원자적 명령어(이를테면 x86의 `lock xadd`)를 곧장 끌어다 써서 읽기-수정-쓰기를 CPU 명령어 하나로 끝냅니다.

`lock`처럼 다른 스레드를 줄 세워 기다리게 하는 방식이 아니라 연산 자체에 끼어들 틈이 없는 구조라, 그만큼 치르는 오버헤드도 가볍습니다.

<br>

```csharp
Interlocked.Increment(ref counter);  // 원자적으로 1 증가
```

<br>

**Monitor.**

사실 `lock` 문도 컴파일을 거치면 속으로는 `Monitor.Enter()`와 `Monitor.Exit()` 호출로 바뀝니다.

다만 `lock`은 블록에 들어설 때까지 무작정 기다리기만 하므로, 상대 스레드가 lock을 오래 쥐고 있으면 부른 쪽도 그만큼 발이 묶입니다.

이럴 때 `Monitor.TryEnter()`를 직접 끌어다 쓰면 기다릴 시간에 상한을 둘 수 있어, 정해 둔 시간 안에 들어서지 못하면 대기를 접고 다른 일로 방향을 틀 수 있습니다.

```csharp
if (Monitor.TryEnter(lockObj, TimeSpan.FromMilliseconds(100)))
{
    try { counter++; }
    finally { Monitor.Exit(lockObj); }
}
else
{
    // 100ms 안에 lock을 획득하지 못한 경우의 처리
}
```

---

### 데드락 (Deadlock)

동기화를 다루는 손길이 어긋나면 이번에는 **데드락(Deadlock)**이 생길 수 있습니다.

두 스레드가 서로 상대가 쥐고 있는 lock이 풀리기만 기다린다면, 어느 쪽도 한 발짝을 못 떼고 영영 멈춰 서게 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <defs>
    <marker id="deadlock-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor" fill-opacity="0.5"/>
    </marker>
  </defs>
  <!-- 컬럼 헤더 -->
  <text fill="currentColor" x="125" y="22" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 A</text>
  <text fill="currentColor" x="375" y="22" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스레드 B</text>
  <!-- 컬럼 구분선 -->
  <line x1="250" y1="8" x2="250" y2="160" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.2"/>
  <!-- Step 1: 획득 -->
  <rect x="30" y="38" width="190" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="125" y="58" text-anchor="middle" font-size="11" font-family="sans-serif">lock(lockX) 획득</text>
  <rect x="280" y="38" width="190" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="375" y="58" text-anchor="middle" font-size="11" font-family="sans-serif">lock(lockY) 획득</text>
  <!-- Step 2: 시도 → 대기 (강조) -->
  <rect x="30" y="86" width="190" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="125" y="106" text-anchor="middle" font-size="11" font-family="sans-serif">lock(lockY) 시도 → 대기</text>
  <rect x="280" y="86" width="190" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="375" y="106" text-anchor="middle" font-size="11" font-family="sans-serif">lock(lockX) 시도 → 대기</text>
  <!-- 교차 화살표 (순환 대기 시각화) -->
  <line x1="220" y1="100" x2="282" y2="60" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5" marker-end="url(#deadlock-arrow)"/>
  <line x1="280" y1="100" x2="218" y2="60" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5" marker-end="url(#deadlock-arrow)"/>
  <!-- 의존 설명 -->
  <text fill="currentColor" x="125" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(B가 lockY 해제 필요)</text>
  <text fill="currentColor" x="375" y="136" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(A가 lockX 해제 필요)</text>
  <!-- 구분선 -->
  <line x1="40" y1="154" x2="460" y2="154" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- 결과 -->
  <rect x="100" y="168" width="300" height="34" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="250" y="190" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">순환 대기 → 둘 다 영원히 블로킹</text>
</svg>
</div>

<br>

데드락을 막는 가장 기본은 **모든 스레드가 lock을 늘 같은 순서로 손에 넣게** 하는 것입니다.

위 그림에서 데드락이 생긴 까닭은, 스레드 A는 lockX → lockY 순서로 쥐려 하고 스레드 B는 lockY → lockX 순서로 쥐려 들어, 서로가 상대 손에 들린 lock을 마주 기다리는 고리가 닫혀 버렸기 때문입니다.

여기서 모든 스레드가 lockX부터 잡고 lockY를 나중에 잡도록 순서를 맞춰 두면, lockX를 기다리는 스레드는 아직 lockY를 손에 쥐지 않은 상태라 이런 고리가 닫힐 일이 없습니다.

<br>

한 lock을 쥔 채 그 안에서 또 다른 lock을 잡는 중첩 잠금은 되도록 피해 두는 편이 안전합니다.

데드락은 한 스레드가 lock 하나를 쥔 채 다른 lock을 더 달라고 손을 뻗을 때 생기므로, 애초에 동시에 두 개 이상을 쥐지 않으면 순환 대기라는 고리가 만들어질 길조차 없습니다.

<br>

lock을 거는 범위를 되도록 좁게 잡는 것도 결국 같은 줄기에서 나옵니다.

lock을 쥐고 있는 시간이 짧을수록 그 안에서 또 다른 lock에 손을 뻗게 될 여지가 그만큼 줄어들기 때문입니다.

<br>

Unity에서 데드락이 유독 무서운 까닭은, 하필 메인 스레드가 묶이면 게임 루프 전체가 함께 얼어붙기 때문입니다.

이런 일로 가장 자주 빠져드는 길목이 메인 스레드에서 `task.Wait()`이나 `task.Result`를 부르는 경우입니다.

`Wait()`은 해당 Task가 끝날 때까지 부른 스레드를 그 자리에 붙들어 둡니다.

그런데 async 메서드에서 `await` 다음으로 이어질 코드(continuation)는 `UnitySynchronizationContext`를 거쳐 메인 스레드의 실행 큐에 예약되어 차례를 기다립니다.

메인 스레드는 이미 `Wait()`에 붙들려 옴짝달싹 못 하니 큐에 들어온 continuation을 꺼내 돌릴 수 없고, 그 continuation이 돌지 못하면 Task 역시 완료 상태로 넘어가지 못합니다.

결국 메인 스레드는 Task가 끝나기를 기다리고 Task는 메인 스레드가 풀려나기를 기다리는, 서로 맞물린 순환 대기에 갇히고 맙니다.

---

## Unity의 메인 스레드 제약

### Unity API는 메인 스레드 전용

Unity 엔진이 내어 주는 API는 **메인 스레드에서만 부를 수 있습니다**.

`Transform.position`이나 `GameObject.SetActive()`, `Instantiate()`, `Destroy()`를 비롯한 대부분의 Unity API는 워커 스레드에서 건드리는 순간 런타임 에러로 이어집니다.

<br>

| API | 메인 스레드 | 워커 스레드 |
|---|---|---|
| `transform.position = newPos` | 정상 | UnityException |
| `gameObject.SetActive(true)` | 정상 | UnityException |
| `Instantiate(prefab)` | 정상 | UnityException |
| `Debug.Log("message")` | 정상 | 허용 (thread-safe) |

<br>

표에서 `Debug.Log`만 워커 스레드에서 허용되는 까닭은, Unity의 로깅 시스템 자체가 스레드 안전하게 짜여 있어서입니다.

로깅은 게임 오브젝트의 상태를 손대지 않고 메시지를 적어 두기만 하므로, 여러 스레드가 함께 불러도 엔진 데이터가 어긋날 일이 없습니다.

<br>

이런 제약이 따라붙는 까닭은 Unity의 C++ 엔진 내부 데이터 구조가 처음부터 스레드 안전(thread-safe)하게 설계되지 않았기 때문입니다.

모든 API 호출마다 lock을 걸어 막는 길도 있지만, 그러면 스레드가 하나뿐인 흔한 상황에서도 매 호출마다 lock을 쥐고 푸는 비용을 고스란히 치러야 합니다.

대부분의 게임 로직은 메인 스레드 하나에서 흐르기에, 모든 호출에 이런 동기화 비용을 물리는 것은 다수에게 군더더기일 뿐입니다.

<br>

여러 스레드가 같은 엔진 데이터를 동시에 손대면 내부 상태가 어긋난 채 남기 쉽습니다.

Transform을 예로 들면, 오브젝트의 월드 좌표는 부모에서 자식으로 내려오는 계층을 따라 로컬 행렬을 차례로 곱해 구합니다.

한 스레드가 부모의 위치를 옮기면 부모의 로컬 행렬이 바뀌므로, 그에 맞춰 자식의 월드 행렬도 다시 구해야 합니다.

하필 이 재계산이 끝나기 전에 다른 스레드가 자식의 월드 좌표를 읽어 가면, 부모 쪽은 새 값으로 갱신됐는데 자식 쪽은 아직 갱신 전인 중간 상태의 좌표를 손에 쥐게 됩니다.

<br>

Unity는 이런 어긋남을 애초에 막으려고, API에 들어서는 길목마다 부른 스레드가 무엇인지부터 확인합니다. 메인 스레드가 아니라면 그 자리에서 `UnityException`을 던져 호출을 막아 세웁니다.

---

### 메인 스레드로 작업 전달

Unity API를 메인 스레드에서만 부를 수 있다는 제약을 지키면서도 멀티스레드의 이점을 누리려면, 하나의 일을 두 갈래로 쪼개야 합니다.

무거운 계산은 워커 스레드에 맡겨 두고, 그 결과를 게임 오브젝트에 반영하는 일만 메인 스레드로 가져오면 됩니다.

<br>

**UnitySynchronizationContext.**

앞서 짚었듯, Unity는 메인 스레드에 `UnitySynchronizationContext`를 미리 걸어 둡니다.

`await`으로 양보한 뒤에 이어질 코드, 즉 연속(continuation)은 이 컨텍스트가 메인 스레드의 실행 큐에 예약해 두고, 다음 프레임에서 메인 루프가 그것을 꺼내 돌립니다.

이 흐름 덕분에 `async`/`await`만으로도 "워커 스레드 계산 → 메인 스레드 적용"이라는 갈래 나누기가 손쉽게 풀립니다.

<br>

```csharp
async void ProcessDataAsync()
{
    // 메인 스레드
    int result = await Task.Run(() =>
    {
        // 워커 스레드 (스레드 풀)
        return HeavyCalculation();
    });
    // 메인 스레드 (UnitySynchronizationContext)
    transform.position = new Vector3(result, 0, 0);
}
```

<br>

JSON 파싱이나 경로 탐색, 절차적 생성처럼 CPU를 오래 붙잡는 연산을 이 패턴에 얹으면, 메인 스레드의 프레임 예산을 갉아먹지 않으면서도 그 결과를 안전하게 반영할 수 있습니다.

<br>

**수동 디스패처.**

손수 만든 스레드나 `async`/`await`을 모르는 라이브러리의 콜백에서 결과를 메인 스레드로 넘겨야 할 때는, 전달 통로를 직접 짜 줄 수 있습니다.

스레드 안전한 큐(`ConcurrentQueue`)에 실행할 `Action`을 쌓아 두면, 메인 스레드의 `Update()`가 매 프레임 그 큐를 비우며 쌓인 작업을 하나씩 꺼내 돌립니다.

<br>

```csharp
ConcurrentQueue<Action> mainThreadActions = new ConcurrentQueue<Action>();

// 워커 스레드에서 호출
void OnCalculationComplete(Vector3 result)
{
    mainThreadActions.Enqueue(() => transform.position = result);
}

// 메인 스레드 (Update)
void Update()
{
    while (mainThreadActions.TryDequeue(out Action action))
        action();
}
```

<br>

따지고 보면 이것은 `UnitySynchronizationContext`가 속에서 알아서 해 주던 일을 손으로 다시 짜 보는 셈에 가깝습니다.

큐를 건사하고 `Update()`에서 폴링하는 코드를 직접 떠안아야 해 손은 더 가지만, 그 대가로 `async`/`await`에 기대지 않고도 워커 스레드의 결과를 메인 스레드로 넘길 수 있고, 어느 프레임에 실행할지를 직접 골라 세밀하게 다룰 수 있습니다.

---

## 코루틴 vs async/await vs Job System

지금까지 C#의 스레딩과 Task, async/await, 그리고 경쟁 조건과 동기화를 차례로 짚어 왔습니다. 이 도구들을 Unity 안에서 실제로 쓸 때는 어떤 방식을 고르느냐에 따라 코드가 어느 스레드에서 실행되고 어떤 작업에 어울리는지가 크게 갈립니다.

Unity에서 비동기 작업을 다루는 길은 크게 **코루틴(Coroutine)**, **async/await**, **Job System** 세 갈래입니다. 셋은 스레드 모델도 다르고 잘 맞는 용도도 달라서, 하나로 모든 상황을 메우기보다 작업의 성격에 맞춰 골라 쓰게 됩니다.

---

### 코루틴 (Coroutine)

세 가지 가운데 가장 오래된 방식이 코루틴입니다. `IEnumerator`를 반환하는 메서드를 `StartCoroutine()`에 넘겨 실행하고, 중간에 `yield return`으로 제어를 양보하면 그 지점에서 멈췄다가 다음 프레임에 이어서 실행됩니다.

<br>

여기서 짚어 둘 점은 코루틴이 멀티스레드가 아니라는 사실입니다. `yield return null`은 지금 프레임의 실행을 거기서 멈추고 다음 프레임에 나머지를 이어 실행하라는 표시이므로, 긴 작업 하나를 여러 프레임에 걸쳐 나누어 처리하는 시분할에 가깝습니다. 모든 조각이 메인 스레드 하나에서 처리되어 한 프레임이 맡는 부담은 가벼워지지만, 여러 코어를 동시에 쓰는 방식이 아니라서 작업 전체가 끝나는 시간은 줄지 않습니다.

<br>

대신 메인 스레드에서 실행되는 덕분에 Unity API를 자유롭게 호출할 수 있고, `WaitForSeconds`처럼 프레임을 기준으로 타이밍을 제어하는 방식이 직관적으로 들어맞습니다. 다만 코루틴을 시작할 때마다 `IEnumerator` 객체가 힙에 할당되어 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 다룬 GC 부담이 생기고, `catch` 절이 붙은 `try` 블록 안에서는 `yield return`을 사용할 수 없으며(CS1626), 작업 결과를 반환값으로 직접 받아 올 수도 없습니다.

---

### async/await in Unity

코루틴이 안고 있던 제약은 `async`/`await`으로 상당 부분 풀립니다. try-catch로 예외를 처리할 수 있고, `Task<T>`로 반환값을 전달할 수 있으며, `Task.Run()`과 결합하면 실제 멀티스레드 처리까지 가능합니다. C# 표준 문법이라 Unity 바깥의 라이브러리와도 그대로 호환됩니다.

<br>

다만 Unity 위에서 쓸 때는 코루틴에는 없던 세 가지 문제가 따라옵니다. 첫째는 `async void`입니다. 표준 .NET 환경에서 `async void` 메서드가 던진 예외는 `SynchronizationContext`로 전파되며, 끝까지 처리되지 않으면 프로세스가 종료되기도 합니다. Unity 환경에서는 `UnitySynchronizationContext`가 이 예외를 잡아 콘솔에 로그로 남기므로 곧장 크래시로 이어지지는 않지만, 호출자가 예외를 `await`으로 관찰하거나 다시 전파할 수 없다는 근본 문제는 그대로입니다. 따라서 가능하면 `async Task`로 반환하는 편이 안전하고, `async void`가 불가피한 자리에서는 메서드 안에서 try-catch로 예외를 직접 처리해야 합니다.

<br>

둘째는 오브젝트 생명주기입니다. 코루틴은 MonoBehaviour가 파괴되는 순간 자동으로 중단되지만, async 메서드의 continuation은 이미 `UnitySynchronizationContext`의 실행 큐에 등록되어 있어 오브젝트가 파괴된 뒤에도 그대로 재개됩니다. 이때 이미 파괴된 오브젝트의 `Transform`에 접근하면 에러가 나므로, `await` 다음에는 `this == null` 검사나 `destroyCancellationToken`(Unity 2022.2 이상)으로 오브젝트가 아직 유효한지 확인하는 편이 안전합니다.

<br>

셋째는 `Task.Run()` 안에서 Unity API를 호출할 수 없다는 제약입니다. 앞서 짚었듯 `Task.Run()`에 넘긴 람다는 워커 스레드에서 실행되고, Unity API는 메인 스레드에서만 호출할 수 있기 때문입니다. 한편 `await Task.Run(...)` 다음 줄은 `UnitySynchronizationContext`가 메인 스레드에서 다시 이어 주므로, 워커 스레드에서 계산한 결과를 Unity API에 반영하는 코드는 `await` 이후에 두면 됩니다.

<br>

이런 차이를 Unity 쪽에서 직접 메워 주는 도구가 Unity 2023.1부터 들어온 `Awaitable` 클래스입니다. `NextFrameAsync()`나 `WaitForSecondsAsync()`처럼 Unity 프레임 루프에 맞춘 비동기 API를 제공하는데, `Task`와 달리 `SynchronizationContext` 캡처를 거치지 않고 PlayerLoop에 곧장 연결되어 메인 스레드에서 재개됩니다. 또한 Awaitable 객체를 내부적으로 풀링하므로 힙 할당까지 줄어듭니다.

<br>

같은 맥락에서 서드파티 라이브러리인 UniTask도 실무에서 널리 쓰입니다. async/await을 힙 할당 없이 실행하면서 `WhenAll`이나 `WhenAny` 같은 `Task` 수준의 조합 API를 제공하고, PlayerLoop의 어느 시점에서 재개할지까지 세밀하게 지정할 수 있습니다.

---

### Job System

**C# Job System**은 앞에서 다룬 lock 기반 동기화와 출발점부터 다릅니다. lock이 여러 스레드가 같은 데이터를 공유하도록 둔 채 접근 순서만 통제하는 방식이라면, Job System은 스레드끼리 데이터를 공유할 길을 처음부터 막아 경쟁 조건이 생길 수 없는 구조를 만들어 둡니다.

<br>

그 구조의 출발이 Job을 [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다룬 struct, 곧 값 타입으로 정의한다는 점입니다. struct는 워커 스레드로 넘어갈 때 값이 통째로 복사되므로, 메인 스레드와 워커 스레드가 서로 무관한 독립된 사본을 하나씩 들게 됩니다. 같은 메모리를 가리키는 스레드가 아예 없으니 lock을 걸지 않아도 경쟁 조건이 생기지 않습니다.

<br>

이 격리를 지키려고 Job 안에서는 참조 타입(클래스, 배열 등)을 쓸 수 없습니다. 참조 타입 변수는 관리 힙의 객체를 가리키는 포인터라서, Job이 참조 하나를 들고 있으면 두 스레드가 같은 힙 객체를 공유하게 되고, struct 복사로 확보해 둔 격리가 그대로 무너지기 때문입니다. 그래서 참조 타입 대신 `NativeArray<T>` 같은 네이티브 메모리 컨테이너를 씁니다. 네이티브 메모리는 관리 힙 바깥에 자리하고, 어떤 Job이 어떤 `NativeArray`를 읽기 전용으로 쓰는지 읽기-쓰기로 쓰는지를 Job System이 추적해 충돌을 잡아냅니다. 이렇게 Job이 관리 힙을 전혀 건드리지 않으므로(struct는 복사하고, 컨테이너는 네이티브 메모리에 두므로) GC가 추적할 객체 자체가 없어 GC 할당도 생기지 않습니다.

<br>

struct로 데이터를 묶는 이 제약은 Burst 컴파일러와도 맞물립니다. Burst는 Job 코드를 LLVM 기반 네이티브 코드로 컴파일하는 고성능 컴파일러인데, 같은 "C#을 네이티브로" 컴파일하더라도 [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서 다룬 IL2CPP와는 방향이 다릅니다. IL2CPP는 C#의 모든 기능을 지원해야 하므로 GC 쓰기 장벽, 가상 메서드 디스패치 테이블, 예외 처리용 스택 해제 코드 같은 것들을 네이티브 코드에 함께 넣어 둡니다. 반면 Burst는 이 부담을 덜어 내려고, C# 문법 가운데 성능에 불리한 기능은 아예 쓰지 못하게 막습니다. 이렇게 추려진 C# 문법의 범위를 HPC#(High-Performance C#)이라 부르며, Burst로 컴파일되는 Job 코드에서 클래스 생성이나 try-catch처럼 HPC# 바깥의 기능을 쓰면 컴파일 에러가 납니다.

<br>

각 제약이 어떤 런타임 부담을 덜어 내는지를 하나씩 짚어 보겠습니다. 먼저 관리 객체(클래스, 문자열 등)를 금지하면 컴파일러가 객체에 접근할 때마다 끼워 넣던 코드가 사라집니다. 일반 C# 런타임은 참조 필드에 값을 대입할 때마다 변경 사실을 GC에 알리는 코드, 곧 쓰기 장벽을 끼워 넣고, 객체에 접근하기 전에는 null인지 검사하는 코드를 넣습니다. 그런데 관리 객체가 처음부터 없으면 이 코드들은 모두 쓸모가 없어집니다.

다음으로 가상 메서드는 실행 시점에 실제 타입을 확인한 뒤에야 호출할 메서드를 정합니다. 컴파일 시점에는 어느 메서드가 불릴지 알 수 없으니, 컴파일러가 메서드 본문을 호출 지점에 직접 펼쳐 넣는 최적화, 곧 인라이닝을 적용할 수 없습니다. 가상 메서드를 막으면 호출 대상이 컴파일 시점에 확정되어 인라이닝이 가능해지고, 함수 호출에 따르는 오버헤드도 사라집니다.

마지막으로 try-catch를 금지하면(try-finally는 Burst 1.6부터 지원합니다) 예외 처리를 위한 우회 경로가 사라집니다. 일반 C# 런타임은 예외가 났을 때 호출 스택을 거슬러 올라가며 catch 블록을 찾는 코드를 미리 갖춰 두는데, try-catch가 없으면 코드가 처음부터 끝까지 분기 없이 흐른다고 가정할 수 있기 때문입니다.

이렇게 세 제약이 GC 추적과 런타임 디스패치, 예외 우회 경로를 모두 걷어 내고 나면, 남는 것은 데이터를 읽고 연산하고 쓰는 순수한 코드뿐입니다. Burst는 이 코드를 대상으로 `NativeArray`를 순회하는 루프를 [C# 런타임 기초 (2)](/dev/unity/CSharpRuntime-2/)에서 다룬 SIMD 명령어로 자동 벡터화하여, 한 사이클에 `float` 4~8개를 한꺼번에 처리하는 수준까지 최적화합니다.

<br>

struct 복사와 HPC# 제약이 설계 수준에서 격리를 확보한다면, 그 격리를 실행 시점에 강제로 지키게 하는 쪽은 Job System의 안전 시스템입니다. 안전 시스템은 `NativeContainer`마다 어떤 Job이 어떤 접근 권한(읽기 전용 또는 읽기-쓰기)을 갖는지를 메타데이터로 따로 기록해 둡니다. 그리고 `job.Schedule()`을 호출하는 순간 이 메타데이터를 검사해, 두 Job이 같은 `NativeArray`에 동시에 쓰려 하거나 한쪽이 쓰는 동안 다른 쪽이 읽으려 하면 그 자리에서 `InvalidOperationException`을 던집니다. 앞에서 살펴본 일반 멀티스레드 프로그래밍이라면 실행 중에 타이밍이 겹쳐야 비로소 드러났을 문제를, 워커 스레드가 Job을 실행하기 전인 스케줄링 단계에서 미리 잡아내는 셈입니다.

<br>

그런데 안전 시스템이 충돌을 막기만 하면, 같은 데이터를 동시에 다루는 Job은 아예 스케줄링조차 할 수 없게 됩니다. 이 제약은 의존성으로 해결합니다. Job A가 `NativeArray`에 데이터를 쓰고 Job B가 그 결과를 읽어야 한다면, `jobB.Schedule(jobAHandle)`처럼 A의 `JobHandle`을 B에 전달합니다. 그러면 Job System이 A가 끝난 뒤에야 B를 실행하므로, lock이나 수동 동기화 없이도 실행 순서가 보장됩니다.

<br>

이처럼 Job System은 기존 C# 코드와는 사뭇 다른 작성 방식을 요구합니다. 데이터를 모두 struct로 설계해야 하고, `NativeArray`는 GC가 관리하지 않으므로 만들 때 수명을 직접 지정(`Allocator.Temp`, `TempJob`, `Persistent`)한 뒤 다 쓰고 나서 `Dispose()`로 해제해야 하며, 파이프라인이 복잡해지면 여러 `JobHandle` 사이의 의존성 그래프까지 직접 구성해야 합니다. 이런 진입 비용이 있는 만큼, 프레임 예산에 아직 여유가 있어 코루틴이나 async/await만으로 감당되는 작업이라면 굳이 Job System을 도입할 이유는 없습니다.

---

### 세 가지 방식의 비교

|  | 코루틴 | async/await | Job System |
|---|---|---|---|
| 스레드 | 메인 (단일) | 메인 (Task.Run 시 워커) | 워커 (병렬) |
| Unity API | 사용 가능 | 메인 스레드 재개 시 가능 | 사용 불가 |
| GC 할당 | 시작 시 발생 | Task 기반 시 발생 (Awaitable은 풀링) | 없음 (struct) |
| 적합한 사례 | 프레임 분산, 타이밍 제어 | I/O 대기, 백그라운드 계산 | CPU 집약 병렬, 물리, AI |
| 난이도 | 낮음 | 중간 | 높음 |

<br>

표에서 보듯 세 방식은 서로 자리를 다투는 경쟁 관계가 아니라, 각자 잘하는 영역이 갈리는 상호 보완 관계에 가깝습니다. 연출 시퀀스처럼 프레임 단위로 타이밍을 맞춰야 하는 작업이라면 코루틴이 잘 어울리고, 파일 로딩이나 네트워크 응답을 기다려야 하는 상황에는 `async`/`await`이 제격이며, 수천 개 에이전트의 경로 탐색처럼 CPU를 많이 쓰는 병렬 연산은 Job System이 맡습니다.

<br>

그래서 실제 프로젝트에서는 셋을 한 흐름 안에 섞어 쓰는 경우가 많습니다. 예를 들어 네트워크에서 데이터를 `async`/`await`으로 받아 온 다음, 그 데이터를 Job System으로 병렬 처리하고, 처리된 결과를 코루틴으로 한 프레임씩 나눠 화면에 보여 주는 식으로 이어 붙입니다.

<br>

다만 어느 방식이든 멀티스레딩으로 넘어가는 순간 경쟁 조건과 데드락, 그리고 디버깅 난도가 함께 올라간다는 비용이 따라옵니다. 따라서 단일 스레드만으로 프레임 예산을 지키고 있다면 굳이 도입할 이유가 없습니다. 실무에서는 먼저 Unity Profiler의 CPU 모듈로 메인 스레드의 프레임 시간을 재고, 특정 작업이 프레임 예산을 넘어서는 것을 확인한 뒤에야 그 작업을 워커 스레드나 Job System으로 옮기는 순서를 밟는 편이 일반적입니다.

---

## 마무리

이번 글에서는 C# 런타임이 손에 쥐여 주는 멀티스레딩·비동기 도구를, Unity 엔진이 거는 메인 스레드 제약과 나란히 놓고 살펴봤습니다.

- 프로세스는 독립된 메모리 공간을 따로 갖는 실행 단위이고, 스레드는 그 프로세스 안에서 메모리를 함께 쓰며 흐르는 실행 흐름입니다
- ThreadPool은 스레드를 미리 만들어 두고 돌려 써서, 매번 생성하고 폐기하는 비용을 덜어 냅니다
- Task는 비동기 작업을 객체 하나로 추상화하고, async/await은 컴파일러가 이를 상태 머신으로 바꿔 비동기 코드를 동기 코드 읽듯 풀어 쓰게 해 줍니다
- 비동기(async)와 멀티스레드는 같은 개념이 아니어서, await 뒤의 코드는 같은 스레드에서 다시 이어질 수도 있습니다
- 여러 스레드가 같은 데이터에 동시에 손대면 경쟁 조건이 생기므로, lock이나 Interlocked로 접근을 맞춰 주어야 합니다
- Unity API는 메인 스레드에서만 부를 수 있고, 워커 스레드에서 부르면 런타임 에러로 이어집니다
- 코루틴은 프레임 분산에, async/await은 I/O 대기와 백그라운드 계산에, Job System은 CPU 집약적인 병렬 처리에 각각 어울려 서로를 보완합니다

이 도구들을 가로지르는 흐름은, 동시성을 깊이 끌어들일수록 그만큼 제약도 함께 늘어난다는 점입니다. 코루틴은 메인 스레드 안에서만 돌기에 따로 지켜야 할 제약이 거의 없는 반면, Job System은 데이터를 struct로만 짜야 하고 네이티브 메모리를 손수 관리하며 의존성 그래프까지 직접 엮어야 합니다. 결국 어떤 도구로 손을 뻗을지는 프로파일링이 짚어 주는 병목이 가른다고 할 수 있습니다.

<br>

이 시리즈에서 짚어 온 값 타입과 참조 타입, 런타임과 IL2CPP, 가비지 컬렉션, 스레딩과 비동기는 앞으로 이어질 최적화 시리즈의 출발점이 됩니다. [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)에서는 Unity API 호출이 어떤 성능 특성을 갖는지, 그리고 메인 스레드에 걸리는 부하를 어떻게 줄이는지를 살펴봅니다.

<br>

---

**관련 글**
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)

**시리즈**
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- **C# 런타임 기초 (4) - 스레딩과 비동기** (현재 글)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- [그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- **C# 런타임 기초 (4) - 스레딩과 비동기** (현재 글)
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
