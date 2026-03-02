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

[C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 GC의 동작 원리를 다루었습니다.

Mark-and-Sweep 알고리즘으로 도달 불가능한 객체를 찾아 메모리를 회수하며, Unity의 Boehm GC는 비세대·비압축·보수적 방식이라 GC 스파이크가 발생할 수 있음을 확인했습니다.

GC가 실행되는 동안 모든 C# 스크립트 실행이 멈추는 Stop-the-World도 프레임 드롭의 원인이었습니다.

<br>

지금까지 다룬 타입 시스템, 런타임 컴파일, GC는 모두 "하나의 실행 흐름"을 전제로 한 이야기였습니다.

하지만 현대 모바일 CPU는 4~8개의 코어를 갖추고 있습니다.

단일 스레드로 실행하면 한 코어만 사용하고 나머지는 유휴 상태로 남습니다.

경로 탐색, 물리 시뮬레이션, 대량 데이터 처리 같은 CPU 집약적인 작업은 한 코어로는 프레임 예산 16.6ms 안에 끝내기 어렵고, 유휴 코어를 활용하는 멀티스레딩이 필요합니다.

<br>

한편 `Transform.position`, `GameObject.SetActive()` 같은 대부분의 Unity API는 메인 스레드에서만 호출할 수 있으며, 워커 스레드에서 호출하면 `UnityException`이 발생합니다.

멀티스레딩을 도입하더라도 이 제약 안에서 작업을 나누어야 합니다.

<br>

이 글에서는 프로세스와 스레드의 개념부터 시작하여, ThreadPool, Task, async/await, 경쟁 조건과 동기화, Unity의 메인 스레드 제약, 그리고 코루틴/async/await/Job System의 비교까지 순서대로 정리합니다.

---

## 프로세스와 스레드

### 프로세스

**프로세스(Process)**는 OS가 프로그램마다 생성하는 실행 단위입니다.

각 프로세스는 독립된 메모리 공간(코드 영역, 데이터 영역, 힙, 스택)을 가지며, 다른 프로세스의 메모리에 직접 접근할 수 없으므로 하나가 비정상 종료되어도 나머지에 영향을 미치지 않습니다.

Unity 게임을 빌드하여 실행하면 OS가 하나의 프로세스를 생성하고, 그 안에서 게임의 모든 동작이 이루어집니다.

---

### 스레드

**스레드(Thread)**는 프로세스 내부의 실행 흐름입니다.

프로세스가 "프로그램 전체의 실행 환경"이라면, 스레드는 그 환경 안에서 "실제로 코드를 실행하는 단위"입니다.

하나의 프로세스는 여러 스레드를 가질 수 있으며, 이 스레드들은 힙과 데이터 영역을 공유합니다.

여러 스레드가 힙의 같은 객체를 동시에 읽고 쓸 수 있습니다.

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

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다루었듯이, 각 스레드는 자신만의 스택(지역 변수, 호출 스택)을 가지지만, 힙에 있는 객체는 공유합니다.

여러 스레드가 같은 데이터를 복사 없이 읽을 수 있어 효율적이지만, 동시에 수정하면 예상과 다른 결과가 발생할 수 있습니다.

---

### 멀티스레드의 이점

현대 모바일 기기의 CPU는 4~8코어가 일반적입니다.

Snapdragon 8 Gen 3는 8코어(1 Prime + 5 Performance + 2 Efficiency 구성, Cortex-X4/A720/A520), Apple A17 Pro는 6코어(2 Performance + 4 Efficiency 구성)를 갖습니다.

하나의 스레드는 한 번에 하나의 코어에서만 실행되므로, 단일 스레드로 실행하면 한 코어만 사용하고 나머지 코어는 유휴 상태가 됩니다.

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

여러 코어에서 작업을 동시에 수행하면, 단일 스레드로 30ms 걸리던 작업을 10ms로 줄일 수 있습니다.

경로 탐색, 물리 연산, 대량 데이터 처리 같은 CPU 집약적인 작업에서 효과가 큽니다.

I/O 바운드 작업에서도 유용합니다. 파일을 읽거나 네트워크 응답을 기다리는 동안 다른 스레드가 CPU를 활용할 수 있기 때문입니다.

---

## Thread 클래스와 스레드 풀

### Thread 클래스

C#에서 스레드를 직접 생성하는 기본 방법은 `System.Threading.Thread` 클래스를 사용하는 것입니다.

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

`new Thread()`로 스레드 객체를 생성하고 `Start()`를 호출하면, OS가 새 스레드를 만들어 지정된 메서드를 실행합니다.

다만 스레드를 직접 생성하는 데는 비용이 따릅니다.

OS 커널 오브젝트 생성, 스레드당 약 1MB의 스택 메모리 예약(.NET 기본값, 플랫폼에 따라 다를 수 있음), 컨텍스트 스위칭(CPU가 실행 중인 스레드를 전환할 때 레지스터 상태를 저장하고 복원하는 작업) 비용 등이 수반됩니다.

작업이 빈번하게 발생하는 경우, 매번 스레드를 생성하고 폐기하는 오버헤드가 실제 작업 비용보다 클 수 있습니다.

<br>

`Thread.Sleep()`은 현재 스레드를 OS 수준에서 지정 시간 동안 블로킹합니다.

스레드가 Sleep 상태에 들어가면 OS 스케줄러가 해당 스레드를 실행 대기 큐에서 제거하고, 지정 시간이 지나야 다시 대기 큐에 넣습니다.

그 동안 해당 스레드는 아무 코드도 실행할 수 없습니다.

이 동작 자체는 어디서 호출하든 동일하지만, **어떤 스레드에서 호출하느냐**에 따라 결과가 달라집니다.

Unity의 메인 스레드는 매 프레임마다 `Update()` → 렌더링 → `LateUpdate()` 순서로 게임 루프를 실행하는 유일한 스레드입니다.

메인 스레드에서 `Thread.Sleep()`을 호출하면 이 루프 자체가 블로킹되어 화면 갱신, 입력 처리, 물리 시뮬레이션 모두 멈추므로, 메인 스레드에서는 절대 사용하면 안 됩니다.

<br>

반면, `new Thread()`로 직접 생성한 전용 스레드에서는 해당 스레드만 블로킹될 뿐 메인 스레드의 게임 루프에는 영향이 없으므로 사용할 수 있습니다.

<br>

스레드 풀 스레드에서는 주의가 필요합니다.

스레드 풀은 제한된 수의 워커 스레드를 여러 작업이 공유하는 구조이므로, `Thread.Sleep()`으로 워커 스레드가 블로킹되면 Sleep이 끝날 때까지 그 스레드는 풀에 반환되지 않습니다.

블로킹된 스레드가 쌓이면 다른 작업이 워커 스레드를 할당받지 못해 전체 처리량이 떨어집니다.

<br>

스레드 풀에서 대기가 필요하다면 `Thread.Sleep()` 대신 `await Task.Delay()`를 사용합니다.

`await` 키워드를 만나면 현재 메서드의 실행이 그 지점에서 중단되고, 스레드는 즉시 풀에 반환됩니다.

`Task.Delay()` 내부에서는 OS 타이머가 지정 시간을 측정하고, 시간이 만료되면 중단된 메서드의 나머지 부분(continuation)을 스레드 풀의 유휴 워커 스레드에 스케줄합니다.

대기 시간 동안 어떤 스레드도 점유하지 않으므로, 워커 스레드가 고갈되는 문제가 발생하지 않습니다.

---

### ThreadPool

스레드를 매번 생성하고 폐기하는 비용을 해결하기 위해, .NET 런타임은 **스레드 풀(ThreadPool)**을 제공합니다.

런타임이 최소 개수의 워커 스레드(worker thread)를 미리 생성해 놓고, 작업이 요청되면 유휴 스레드에 할당합니다.

유휴 스레드가 없으면 풀이 새 스레드를 추가로 생성하며, 최대 개수까지 수요에 따라 자동으로 늘어납니다.

작업이 끝나면 스레드는 폐기되지 않고 풀로 돌아가 다음 작업을 기다립니다.

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

`Thread`와 `ThreadPool`은 "스레드에서 코드를 실행한다"는 기본 기능만 제공하므로, 그 이상의 제어가 필요하면 개발자가 직접 구현해야 합니다.

작업이 끝났는지 확인하는 것부터 쉽지 않습니다.

`Thread`는 `Join()`으로 완료를 기다릴 수 있지만, `Join()`은 호출한 스레드를 블로킹합니다.

Unity 메인 스레드에서 `Join()`을 호출하면 게임 루프가 멈추므로 사실상 사용할 수 없고, 블로킹 없이 완료 여부를 알려면 플래그 변수를 직접 만들어 폴링해야 합니다.

`ThreadPool.QueueUserWorkItem()`은 작업의 완료 여부를 알 수 있는 핸들 자체를 반환하지 않습니다.

<br>

결과값을 받는 것도 마찬가지입니다.

`Thread`와 `ThreadPool` 모두 작업의 반환값을 전달하는 메커니즘이 없으므로, 공유 변수에 결과를 저장하고 `lock` 등으로 동기화해야 합니다.

<br>

예외 처리도 문제입니다.

워커 스레드에서 발생한 예외는 호출 측에 자동으로 전파되지 않습니다.

스레드 내부에서 `try-catch`로 직접 잡아 오류 상태를 수동으로 전달해야 합니다.

<br>

**Task**는 이 세 가지 문제를 하나의 객체로 해결합니다.

`Task` 객체가 작업의 상태(실행 중, 완료, 실패)를 추적하므로 `await`로 블로킹 없이 완료를 기다릴 수 있고, `Task<T>`는 완료 시 결과값을 담아 `await` 표현식이 직접 값을 반환하며, 워커 스레드에서 발생한 예외는 `Task` 내부에 저장되었다가 `await` 시점에 호출 측으로 다시 던져집니다.

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

`Task.Run()`은 전달받은 델리게이트를 스레드 풀의 워커 스레드에서 실행합니다.

호출 즉시 `Task` 객체를 반환하므로, 호출 측은 블로킹 없이 다른 작업을 계속하다가 필요한 시점에 `await`로 완료를 기다리거나 결과를 받을 수 있습니다.

<br>

이처럼 `Task`를 반환하는 비동기 메서드를 작성하는 방식을 .NET에서는 **TAP(Task-based Asynchronous Pattern)**이라 합니다.

TAP 이전에는 콜백(AsyncCallback) 기반 패턴이 사용되었는데, 비동기 작업이 연쇄되면 콜백 안에 콜백이 중첩되어 흐름을 추적하기 어려웠습니다.

TAP은 모든 비동기 메서드가 `Task` 또는 `Task<T>`를 반환하도록 통일하고, 메서드 이름 끝에 `Async`를 붙이는 것을 관례로 합니다.

<br>

```csharp
async Task<string> LoadDataAsync(string path)
{
    string data = await File.ReadAllTextAsync(path);
    return data;
}
```

<br>

`async`/`await`와 결합하면 콜백 중첩 없이 동기 코드와 같은 순서로 비동기 흐름을 작성할 수 있습니다.

---

## async/await의 동작 원리

### 상태 머신 변환

비동기 메서드는 `await` 지점에서 실행을 멈췄다가 나중에 이어서 재개해야 합니다.

이를 위해 C# 컴파일러는 `async` 메서드를 **상태 머신(State Machine)**으로 변환합니다.

각 `await` 지점이 상태 전환 경계가 되고, 지역 변수와 실행 위치가 상태 머신의 필드에 저장되어 재개 시 복원됩니다.

`async`/`await`은 이 상태 머신을 직접 작성하지 않아도 되게 해 주는 **문법적 편의(syntactic sugar)**입니다.

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

상태 머신은 `await` 지점에서 비동기 작업의 완료 여부를 확인합니다.

이미 완료되었으면 결과를 꺼내 다음 코드를 바로 실행하고, 아직 완료되지 않았으면 현재 상태를 저장한 뒤 호출자에게 제어를 돌려줍니다(**양보**, yield).

이 양보 덕분에 호출자 스레드는 블로킹되지 않고 다른 작업을 계속할 수 있습니다.

비동기 작업이 완료되면 저장된 지점에서 상태 머신이 재개되어 나머지 코드를 실행합니다.

---

### 비동기와 멀티스레드는 다르다

`async`/`await`이 반드시 멀티스레드를 의미하지는 않습니다.

`await`은 "이 작업이 끝날 때까지 스레드를 블로킹하지 않겠다"는 의미이지, "이 작업을 다른 스레드에서 실행하겠다"는 의미가 아닙니다.

`await` 후에 어느 스레드에서 실행을 재개하는지는 **동기화 컨텍스트(SynchronizationContext)**에 따라 결정됩니다.

동기화 컨텍스트란, 비동기 작업이 완료된 후 "어느 스레드에서 이어서 실행할지"를 결정하는 런타임 메커니즘입니다.

<br>

|  | 비동기 (async/await) | 멀티스레드 |
|---|---|---|
| 핵심 원리 | 작업 완료를 기다리는 동안 스레드를 블로킹하지 않음 | 여러 스레드에서 동시에 코드를 실행 |
| 스레드 동작 | 같은 스레드 또는 다른 스레드에서 재개 가능 | 반드시 여러 스레드가 관여 |
| Unity에서 | `await` 후 → 메인 스레드에서 재개 (`UnitySynchronizationContext`) | `Task.Run()` → 스레드 풀에서 실행 |

<br>

Unity 엔진은 메인 스레드에 `UnitySynchronizationContext`를 설정합니다.

`await`이 양보할 때 이 컨텍스트가 연속(continuation)을 캡처하여 메인 스레드의 실행 큐에 넣고, Unity의 메인 루프가 다음 프레임에서 이를 꺼내 실행합니다.

덕분에 `await` 이후 코드는 메인 스레드에서 재개되고, Unity API를 안전하게 호출할 수 있습니다.

<br>

`ConfigureAwait(false)`를 사용하면 이 컨텍스트 캡처를 건너뜁니다.

메인 스레드로 돌아오는 비용을 피할 수 있어 Unity API가 필요 없는 순수 연산에서는 유용하지만, `await` 이후 코드가 스레드 풀의 아무 스레드에서 재개될 수 있습니다.

이 상태에서 Unity API를 호출하면 메인 스레드가 아니기 때문에 런타임 에러가 발생합니다.

<br>

다만 `await` 시점에 작업이 이미 완료되었으면, `ConfigureAwait` 설정과 무관하게 스레드 전환 없이 현재 스레드에서 바로 계속 실행됩니다.

---

## 경쟁 조건과 동기화

### 경쟁 조건 (Race Condition)

여러 스레드가 같은 데이터를 동시에 읽고 쓰면, 어느 스레드가 먼저 실행되느냐에 따라 결과가 달라지는 **경쟁 조건(Race Condition)**이 발생할 수 있습니다.

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

`counter++`는 코드에서는 한 줄이지만, 내부적으로 값 읽기 → 증가 → 쓰기 세 단계로 실행됩니다.

쓰기 전에 다른 스레드가 같은 값을 읽으면 두 스레드가 동일한 값에서 증가시키므로, 하나의 증가가 소실됩니다.

경쟁 조건은 스레드의 실행 타이밍에 따라 발생 여부가 달라지기 때문에 재현이 어렵습니다.

10,000번 실행 중 한 번만 나타나거나 특정 기기에서만 발생할 수 있어, 테스트에서 통과하더라도 실제 환경에서 문제가 드러나는 경우가 많습니다.

---

### 동기화 메커니즘

경쟁 조건을 방지하려면, 공유 데이터에 대한 접근을 **동기화(Synchronization)**해야 합니다.

<br>

**lock 문.**

가장 기본적인 동기화 도구입니다. `lock` 블록 안에는 한 번에 하나의 스레드만 진입할 수 있습니다.

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

스레드 A가 `lock` 블록에 진입하면, 스레드 B는 A가 빠져나올 때까지 대기합니다.

"읽기 → 증가 → 쓰기" 세 단계가 다른 스레드의 간섭 없이 수행되므로, 외부에서 보면 나눌 수 없는 하나의 연산, 즉 **원자적(atomic)** 연산처럼 동작합니다.

실제로 CPU 명령어 하나로 실행되는 것은 아니고 세 명령어가 그대로 실행되지만, `lock`이 상호 배제를 보장하여 중간에 다른 스레드가 끼어들 수 없습니다.

<br>

**Interlocked.**

`lock`은 여러 명령어를 하나의 블록으로 묶어 보호하지만, 단순한 숫자 증감이나 대입처럼 단일 연산만 보호하면 되는 경우에는 `Interlocked` 클래스가 더 적합합니다.

`Interlocked`는 CPU가 제공하는 원자적 명령어(예: x86의 `lock xadd`)를 직접 사용하여 읽기-수정-쓰기를 하나의 CPU 명령어로 실행합니다.

`lock`처럼 다른 스레드를 대기시키는 것이 아니라 연산 자체가 중간에 끼어들 수 없으므로 오버헤드가 적습니다.

<br>

```csharp
Interlocked.Increment(ref counter);  // 원자적으로 1 증가
```

<br>

**Monitor.**

`lock` 문은 내부적으로 `Monitor.Enter()`와 `Monitor.Exit()`로 변환됩니다.

`lock`은 블록을 빠져나올 때까지 무조건 대기하므로, 상대 스레드가 lock을 오래 잡고 있으면 호출 측도 그만큼 멈춥니다.

`Monitor.TryEnter()`를 직접 사용하면 타임아웃을 지정할 수 있어, 일정 시간 안에 진입하지 못하면 대기를 포기하고 다른 처리를 할 수 있습니다.

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

동기화를 잘못 사용하면 **데드락(Deadlock)**이 발생할 수 있습니다.

두 스레드가 서로 상대방이 가진 lock을 기다리면, 둘 다 영원히 진행할 수 없습니다.

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

데드락을 방지하는 기본 원칙은 **lock을 항상 같은 순서로 획득**하는 것입니다.

위 다이어그램에서 데드락이 발생한 이유는 스레드 A가 lockX → lockY 순서로, 스레드 B가 lockY → lockX 순서로 획득하여 서로 상대가 쥔 lock을 기다리는 순환이 만들어졌기 때문입니다.

모든 스레드가 lockX를 먼저, lockY를 나중에 획득하도록 통일하면, lockX를 대기하는 스레드는 아직 lockY를 쥐고 있지 않으므로 순환이 형성되지 않습니다.

<br>

lock 안에서 다른 lock을 획득하는 중첩 잠금은 가능하면 피하는 것이 안전합니다.

데드락은 한 스레드가 lock을 쥔 채 다른 lock을 요청할 때 발생하므로, 동시에 두 개 이상의 lock을 잡지 않으면 순환 대기 자체가 불가능합니다.

<br>

lock의 범위를 최소화하는 것도 같은 맥락입니다.

lock을 잡고 있는 시간이 짧을수록 그 안에서 다른 lock을 요청하게 될 가능성이 줄어듭니다.

<br>

Unity에서 데드락이 특히 위험한 이유는 메인 스레드가 블로킹되면 게임 루프 전체가 멈추기 때문입니다.

가장 흔한 패턴은 메인 스레드에서 `task.Wait()`이나 `task.Result`를 호출하는 경우입니다.

`Wait()`은 Task가 완료될 때까지 호출 스레드를 블로킹합니다.

그런데 async 메서드의 `await` 이후 코드(continuation)는 `UnitySynchronizationContext`를 통해 메인 스레드의 실행 큐에 예약됩니다.

메인 스레드가 이미 `Wait()`으로 멈춰 있으므로 큐에 들어온 continuation을 처리할 수 없고, continuation이 실행되지 않으면 Task는 완료 상태로 전환될 수 없습니다.

메인 스레드는 Task 완료를 기다리고, Task 완료는 메인 스레드를 기다리는 순환 대기가 형성됩니다.

---

## Unity의 메인 스레드 제약

### Unity API는 메인 스레드 전용

Unity 엔진의 API는 **메인 스레드에서만 호출할 수 있습니다**.

`Transform.position`, `GameObject.SetActive()`, `Instantiate()`, `Destroy()` 등 대부분의 Unity API를 다른 스레드에서 호출하면 런타임 에러가 발생합니다.

<br>

| API | 메인 스레드 | 워커 스레드 |
|---|---|---|
| `transform.position = newPos` | 정상 | UnityException |
| `gameObject.SetActive(true)` | 정상 | UnityException |
| `Instantiate(prefab)` | 정상 | UnityException |
| `Debug.Log("message")` | 정상 | 허용 (thread-safe) |

<br>

`Debug.Log`가 워커 스레드에서 허용되는 이유는, Unity의 로깅 시스템이 내부적으로 스레드 안전하게 구현되어 있기 때문입니다.

로깅은 게임 오브젝트의 상태를 변경하지 않고 메시지를 기록만 하므로, 엔진 데이터 불일치 문제가 발생하지 않습니다.

<br>

이 제약이 존재하는 이유는 Unity의 C++ 엔진 내부 데이터 구조가 스레드 안전(thread-safe)하게 설계되지 않았기 때문입니다.

모든 API 호출에 lock을 거는 방법도 있지만, 그러면 스레드가 하나뿐인 일반적인 상황에서도 매 호출마다 lock 획득/해제 비용을 지불해야 합니다.

대부분의 게임 로직은 메인 스레드 하나에서 실행되므로, 모든 호출에 동기화 비용을 부과하는 것은 대다수에게 불필요한 오버헤드입니다.

<br>

여러 스레드가 동시에 엔진 데이터를 건드리면 내부 상태가 불일치에 빠집니다.

Transform을 예로 들면, 오브젝트의 월드 좌표는 부모-자식 계층 구조를 따라 로컬 행렬을 누적 곱하여 계산됩니다.

한 스레드가 부모의 위치를 이동시키면 부모의 로컬 행렬이 바뀌고, 자식의 월드 행렬도 다시 계산되어야 합니다.

이 재계산 도중에 다른 스레드가 자식의 월드 좌표를 읽으면, 부모는 새 값이지만 자식은 아직 갱신 전인 중간 상태의 좌표를 받게 됩니다.

<br>

Unity는 이런 문제를 원천 차단하기 위해 API 진입 시점에서 호출 스레드를 확인하고, 메인 스레드가 아니면 `UnityException`을 발생시킵니다.

---

### 메인 스레드로 작업 전달

Unity API가 메인 스레드 전용이라는 제약 아래에서, 멀티스레드의 이점을 활용하려면 작업을 분리해야 합니다.

계산은 워커 스레드에서, 결과 적용은 메인 스레드에서 수행하는 구조입니다.

<br>

**UnitySynchronizationContext.**

앞서 살펴본 것처럼, Unity는 메인 스레드에 `UnitySynchronizationContext`를 설정합니다.

`await`으로 양보한 뒤의 코드(continuation)는 이 컨텍스트가 메인 스레드의 실행 큐에 예약하고, 다음 프레임에서 메인 루프가 꺼내 실행합니다.

덕분에 `async`/`await`만으로 워커 스레드 계산 → 메인 스레드 적용 패턴을 자연스럽게 구현할 수 있습니다.

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

JSON 파싱, 경로 탐색, 절차적 생성 등 무거운 연산에 이 패턴을 적용하면 메인 스레드의 프레임 예산을 소비하지 않으면서 결과를 안전하게 반영할 수 있습니다.

<br>

**수동 디스패처.**

직접 생성한 스레드나 `async`/`await`을 지원하지 않는 라이브러리 콜백에서 결과를 메인 스레드로 전달해야 할 때는 직접 디스패처를 구현할 수 있습니다.

스레드 안전한 큐(`ConcurrentQueue`)에 `Action`을 넣고, 메인 스레드의 `Update()`에서 꺼내 실행하는 방식입니다.

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

이 방식은 `UnitySynchronizationContext`가 내부적으로 하는 일을 직접 구현하는 것입니다.

큐 관리와 `Update()` 폴링을 직접 작성해야 하므로 코드량이 늘어나지만, `async`/`await` 없이도 워커 스레드의 결과를 메인 스레드로 전달할 수 있고, 실행 시점을 프레임 단위로 세밀하게 제어할 수 있습니다.

---

## 코루틴 vs async/await vs Job System

앞에서 C#의 스레딩, Task, async/await, 경쟁 조건과 동기화를 살펴봤습니다.

Unity에서 비동기적으로 작업을 처리하는 방법은 **코루틴(Coroutine)**, **async/await**, **Job System** 세 가지이며, 각각 스레드 모델과 적합한 사용 사례가 다릅니다.

---

### 코루틴 (Coroutine)

코루틴은 Unity의 전통적인 비동기 처리 방식입니다.

`IEnumerator`를 반환하는 메서드를 `StartCoroutine()`으로 실행하고, `yield return`으로 실행을 양보하면 다음 프레임에 이어서 실행됩니다.

<br>

코루틴은 멀티스레드가 아닙니다.

`yield return null`은 현재 프레임의 실행을 멈추고 다음 프레임에 이어서 실행하라는 의미로, 하나의 긴 작업을 여러 프레임에 걸쳐 나누는 시분할 방식입니다.

메인 스레드 하나에서 실행되므로 한 프레임당 부담은 줄어들지만, 여러 코어를 동시에 활용하지 않기 때문에 총 작업 시간은 줄어들지 않습니다.

<br>

메인 스레드에서 실행되므로 Unity API를 자유롭게 호출할 수 있고, `WaitForSeconds` 같은 프레임 기반 타이밍 제어가 직관적입니다.

다만 시작 시 `IEnumerator` 객체가 힙에 할당되어 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 다룬 GC 부담이 생기고, `catch` 절이 있는 `try` 블록 안에서는 `yield return`을 사용할 수 없으며(CS1626), 반환값을 직접 받을 수도 없습니다.

---

### async/await in Unity

`async`/`await`은 코루틴의 제약을 해소합니다.

try-catch로 예외를 처리할 수 있고, `Task<T>`로 반환값을 전달할 수 있으며, `Task.Run()`과 결합하면 실제 멀티스레드 처리도 가능합니다.

C# 표준 문법이므로 Unity 외부 라이브러리와도 호환됩니다.

다만 Unity 환경에서는 코루틴에 없던 문제가 생깁니다.

<br>

첫째, `async void`입니다.

표준 .NET 환경에서 `async void` 메서드의 예외는 `SynchronizationContext`로 전파되며, 처리되지 않으면 프로세스가 종료될 수 있습니다.

Unity 환경에서는 `UnitySynchronizationContext`가 예외를 잡아 콘솔에 로그로 출력하므로 즉시 크래시가 발생하지는 않지만, 호출자가 예외를 `await`으로 관찰하거나 전파할 수 없다는 근본적인 문제는 동일합니다.

가능하면 `async Task`를 반환하는 것이 안전합니다.

`async void`를 사용해야 할 때는 메서드 내부에서 try-catch로 예외를 직접 처리해야 합니다.

<br>

둘째, 오브젝트 생명주기입니다.

코루틴은 MonoBehaviour가 파괴되면 자동으로 중단되지만, async 메서드의 continuation은 `UnitySynchronizationContext`의 실행 큐에 이미 등록되어 있어 오브젝트가 파괴된 후에도 재개됩니다.

파괴된 오브젝트의 `Transform`에 접근하면 에러가 발생하므로, `await` 후에 `this == null` 확인이나 `destroyCancellationToken`(Unity 2022.2 이상)으로 유효성을 검증해야 합니다.

<br>

셋째, `Task.Run()` 내부에서는 Unity API를 호출할 수 없습니다.

앞서 살펴본 것처럼 `Task.Run()`의 람다는 워커 스레드에서 실행되고, Unity API는 메인 스레드에서만 호출할 수 있기 때문입니다.

`await Task.Run(...)` 다음 줄은 `UnitySynchronizationContext`가 메인 스레드에서 재개하므로, 워커 스레드의 계산 결과를 Unity API에 반영하는 코드는 `await` 이후에 작성합니다.

<br>

Unity 2023.1부터는 `Awaitable` 클래스가 도입되었습니다.

`NextFrameAsync()`, `WaitForSecondsAsync()` 등 Unity 프레임 루프에 맞춘 비동기 API를 제공합니다.

`Task`와 달리 `SynchronizationContext` 캡처를 거치지 않고 PlayerLoop에 직접 연결되어 메인 스레드에서 재개되며, Awaitable 객체를 내부적으로 풀링하여 힙 할당을 줄입니다.

<br>

서드파티 라이브러리인 UniTask도 실무에서 널리 사용됩니다.

async/await을 힙 할당 없이 실행하고, `WhenAll`/`WhenAny` 등 `Task` 수준의 조합 API를 제공하며, PlayerLoop의 어느 시점에서 재개할지 세밀하게 지정할 수 있습니다.

---

### Job System

**C# Job System**은 앞에서 다룬 lock 기반 동기화와 접근 방식이 다릅니다.

lock은 여러 스레드가 같은 데이터를 공유하되 접근 순서를 제어하는 방식이지만, Job System은 애초에 스레드 간 데이터 공유를 차단하여 경쟁 조건이 발생할 수 없는 구조를 만듭니다.

<br>

Job은 [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다룬 struct(값 타입)로 정의합니다.

struct는 워커 스레드에 전달될 때 값이 통째로 복사되므로, 메인 스레드와 워커 스레드가 각자 독립된 사본을 갖게 됩니다.

같은 메모리를 가리키는 스레드가 없으니 lock 없이도 경쟁 조건이 발생하지 않습니다.

<br>

Job 내부에서 참조 타입(클래스, 배열 등)은 사용할 수 없습니다.

참조 타입 변수는 관리 힙의 객체를 가리키는 포인터이므로, Job이 참조를 들고 있으면 두 스레드가 같은 힙 객체를 공유하게 되어 struct 복사로 확보한 격리가 무너지기 때문입니다.

대신 `NativeArray<T>` 같은 네이티브 메모리 컨테이너를 사용합니다.

네이티브 메모리는 관리 힙 바깥에 위치하며, Job System이 어떤 Job이 어떤 `NativeArray`를 읽기 전용으로 쓰는지, 읽기-쓰기로 쓰는지를 추적하여 충돌을 감지합니다.

Job이 관리 힙을 전혀 건드리지 않으므로(struct는 복사, 컨테이너는 네이티브 메모리) GC가 추적할 객체가 없어 GC 할당이 발생하지 않습니다.

<br>

Job System의 struct 제약은 Burst 컴파일러와도 맞물립니다.

Burst는 Job 코드를 LLVM 기반 네이티브 코드로 컴파일하는 고성능 컴파일러입니다.

[C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서 다룬 IL2CPP도 C#을 네이티브 코드로 컴파일하지만, IL2CPP는 C#의 모든 기능을 지원해야 하므로 GC 쓰기 장벽, 가상 메서드 디스패치 테이블, 예외 처리용 스택 해제 코드 등을 네이티브 코드에 포함합니다.

Burst는 이 부담을 없애기 위해, C# 문법 중 성능에 불리한 기능을 아예 사용하지 못하게 제한합니다.

이렇게 제한된 C# 문법 범위를 HPC#(High-Performance C#)이라 부르며, Burst로 컴파일되는 Job 코드에서 HPC# 범위를 벗어나는 기능(클래스 생성, try-catch 등)을 사용하면 컴파일 에러가 발생합니다.

<br>

각 제약이 구체적으로 어떤 런타임 부담을 제거하는지 살펴보면 다음과 같습니다.

먼저 관리 객체(클래스, 문자열 등)를 금지하면 컴파일러가 객체 접근마다 삽입해야 하는 코드가 사라집니다. 일반 C# 런타임은 참조 필드에 값을 대입할 때마다 GC에 변경 사실을 알리는 코드(쓰기 장벽)를 삽입하고, 객체에 접근하기 전에 null 여부를 검사하는 코드를 삽입합니다. 관리 객체가 존재하지 않으면 이 코드들이 전부 불필요합니다.

가상 메서드는 실행 시점에 실제 타입을 확인해서 호출할 메서드를 결정합니다. 컴파일 시점에는 어떤 메서드가 호출될지 알 수 없으므로, 컴파일러가 메서드 본문을 호출 지점에 직접 삽입하는 최적화(인라이닝)를 적용할 수 없습니다. 가상 메서드를 금지하면 호출 대상이 컴파일 시점에 확정되므로 인라이닝이 가능해지고, 함수 호출 오버헤드가 사라집니다.

try-catch를 금지하면(try-finally는 Burst 1.6부터 지원) 예외 처리를 위한 우회 경로가 사라집니다. 일반 C# 런타임은 예외가 발생했을 때 호출 스택을 거슬러 올라가며 catch 블록을 찾는 코드를 미리 준비해 두는데, try-catch가 없으면 코드가 처음부터 끝까지 분기 없이 실행된다고 가정할 수 있습니다.

세 제약이 GC 추적, 런타임 디스패치, 예외 우회 경로를 모두 제거하면, 남는 것은 순수하게 데이터를 읽고 연산하고 쓰는 코드뿐입니다. Burst는 이 코드를 대상으로 `NativeArray`에 대한 루프를 [C# 런타임 기초 (2)](/dev/unity/CSharpRuntime-2/)에서 다룬 SIMD 명령어로 자동 벡터화하여 한 사이클에 `float` 4~8개를 동시에 처리하는 수준까지 최적화할 수 있습니다.

<br>

struct 복사와 HPC# 제약이 설계 수준에서 격리를 확보한다면, 이 격리를 실행 시점에 강제하는 것은 Job System의 안전 시스템입니다.

안전 시스템은 `NativeContainer`마다 어떤 Job이 어떤 접근 권한(읽기 전용 또는 읽기-쓰기)을 갖는지를 메타데이터로 추적합니다.

`job.Schedule()`을 호출하는 시점에 이 메타데이터를 검사하여, 두 Job이 같은 `NativeArray`에 동시에 쓰려 하거나 한쪽이 쓰는 동안 다른 쪽이 읽으려 하면 `InvalidOperationException`을 발생시킵니다.

앞에서 살펴본 일반 멀티스레드 프로그래밍에서는 실행 중 타이밍이 겹쳐야만 드러나던 문제를, 워커 스레드가 Job을 실행하기 전인 스케줄링 단계에서 미리 잡아내는 것입니다.

<br>

안전 시스템이 충돌을 차단만 하면 동시에 같은 데이터를 다루는 Job은 아예 스케줄링할 수 없게 됩니다.

이 문제는 의존성으로 해결합니다.

Job A가 `NativeArray`에 데이터를 쓰고 Job B가 그 결과를 읽어야 한다면, `jobB.Schedule(jobAHandle)`처럼 A의 `JobHandle`을 B에 전달합니다.

Job System은 A가 완료된 후에만 B를 실행하므로, lock이나 수동 동기화 없이도 실행 순서가 보장됩니다.

<br>

다만 Job System에는 기존 C# 코드와 다른 패턴이 필요합니다.

모든 데이터를 struct로 설계해야 하고, `NativeArray`는 GC가 관리하지 않으므로 생성 시 수명을 직접 지정(`Allocator.Temp`, `TempJob`, `Persistent`)하고 사용 후 `Dispose()`를 호출해야 하며, 복잡한 파이프라인에서는 여러 `JobHandle` 간의 의존성 그래프를 직접 구성해야 합니다.

이런 진입 장벽 때문에, 프레임 예산에 여유가 있다면 코루틴이나 async/await으로 충분한 작업에 Job System을 도입할 필요는 없습니다.

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

세 가지 방식은 경쟁 관계가 아니라 상호 보완 관계입니다.

연출 시퀀스처럼 프레임 단위로 타이밍을 제어해야 하면 코루틴이 적합합니다.

파일 로딩이나 네트워크 응답을 기다리는 상황에는 `async`/`await`을 사용하고, 수천 개의 에이전트에 대한 경로 탐색처럼 CPU 집약적인 병렬 연산은 Job System이 담당합니다.

<br>

실제 프로젝트에서는 세 가지를 혼합합니다.

네트워크에서 데이터를 `async`/`await`으로 받고, 받은 데이터를 Job System으로 병렬 처리한 뒤, 처리 결과를 코루틴으로 순차적으로 화면에 표시하는 식입니다.

<br>

다만 멀티스레딩은 경쟁 조건, 데드락, 디버깅 난이도 증가라는 비용을 수반합니다.

단일 스레드에서 프레임 예산을 지키고 있다면 도입할 이유가 없습니다.

Unity Profiler의 CPU 모듈에서 메인 스레드의 프레임 시간을 먼저 측정하고, 특정 작업이 프레임 예산을 초과하는 것을 확인한 뒤에 해당 작업을 워커 스레드나 Job System으로 이동하는 접근이 일반적입니다.

---

## 마무리

C# 런타임이 제공하는 멀티스레딩·비동기 도구와, Unity 엔진의 메인 스레드 제약을 함께 살펴봤습니다.

- 프로세스는 독립된 메모리 공간을 가진 실행 단위이고, 스레드는 프로세스 내부에서 메모리를 공유하는 실행 흐름입니다
- ThreadPool은 스레드를 미리 생성해두고 재사용하여 생성/폐기 비용을 제거합니다
- Task는 비동기 작업을 추상화하며, async/await은 컴파일러가 상태 머신으로 변환하여 비동기 코드를 동기 코드처럼 작성할 수 있게 합니다
- 비동기(async)와 멀티스레드는 같은 개념이 아닙니다. await 후에 같은 스레드에서 재개될 수 있습니다
- 여러 스레드가 같은 데이터에 접근하면 경쟁 조건이 발생하며, lock, Interlocked 등으로 동기화해야 합니다
- Unity API는 메인 스레드에서만 호출 가능하며, 워커 스레드에서 호출하면 런타임 에러가 발생합니다
- 코루틴(프레임 분산), async/await(I/O 대기, 백그라운드 계산), Job System(CPU 집약적 병렬 처리)은 각각 적합한 사용 사례가 다르며 상호 보완적입니다

공통된 흐름은, 동시성이 필요해질수록 제약도 함께 늘어난다는 점입니다. 코루틴은 메인 스레드 안에서 동작하므로 제약이 거의 없지만, Job System은 struct 전용 설계, 네이티브 메모리 수동 관리, 의존성 그래프 구성까지 요구합니다. 어떤 도구를 선택할지는 결국 프로파일링 결과가 보여주는 병목에 달려 있습니다.

<br>

이 시리즈에서 다룬 값 타입과 참조 타입, 런타임과 IL2CPP, 가비지 컬렉션, 스레딩과 비동기는 이후 최적화 시리즈의 출발점이 됩니다. [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)에서는 Unity API 호출의 성능 특성과 메인 스레드 부하를 줄이는 전략을 살펴봅니다.

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
