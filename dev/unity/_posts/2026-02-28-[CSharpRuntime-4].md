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

[C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서는 GC가 더 이상 도달할 수 없는 객체를 찾아 메모리를 회수하는 과정을 다루었습니다. Unity의 Boehm GC는 비세대·비압축·보수적 특성 때문에 한 번의 수집 비용이 커질 수 있고, Stop-the-World로 인해 GC 스파이크가 나타날 수 있습니다.

지금까지는 프로그램이 명령을 위에서 아래로 하나씩 차례대로 실행한다고 전제하고 타입 시스템, 런타임 컴파일, GC를 설명했습니다. 그러나 경로 탐색이나 물리 계산, 대량 데이터 처리처럼 시간이 오래 걸리는 작업을 이 하나의 흐름에서 처리하면, 그 작업이 끝날 때까지 화면 갱신이나 입력 처리 같은 다른 일이 모두 차례를 기다려야 합니다. 이렇게 한 프레임에 주어진 시간을 넘기면 화면이 끊기고, CPU에 코어가 여러 개 있어도 흐름이 하나뿐이면 그중 한 코어만 쓰게 됩니다.

이를 해결하려면 작업을 나누어 여러 코어에서 함께 실행해야 합니다. 작업을 별도의 프로그램, 즉 여러 프로세스로 나누는 멀티프로세싱도 있지만, 게임처럼 같은 데이터를 자주 주고받는 작업에는 한 프로그램 안에서 실행 흐름만 나누는 멀티스레딩이 더 알맞습니다. C#은 멀티스레딩을 다루는 여러 도구를 제공합니다.

다만 Unity에는 한 가지 제약이 있습니다. `Transform.position`이나 `GameObject.SetActive()`처럼 엔진을 직접 다루는 기능은 대부분 프로그램의 주 실행 흐름, 곧 메인 스레드에서만 호출할 수 있습니다. 이를 다른 흐름에서 호출하면 `UnityException`이 발생하므로, 시간이 오래 걸리는 계산과 그 결과를 엔진에 반영하는 Unity API 호출은 서로 분리해야 합니다.

이번 글에서는 프로세스와 스레드의 차이에서 시작해 ThreadPool, Task, async/await, 경쟁 조건과 동기화, Unity의 메인 스레드 제약을 차례로 정리합니다. 마지막에는 코루틴, async/await, Job System이 각각 어떤 작업에 적합한지도 비교합니다.

---

## 프로세스와 스레드

멀티스레딩을 다루기에 앞서, 그 바탕이 되는 프로세스와 스레드를 먼저 정리합니다. 특히 이 둘은 메모리를 다루는 방식이 다른데, 이 차이가 동시 실행의 이점과 위험을 함께 만듭니다.

### 프로세스

**프로세스(Process)**는 OS가 프로그램마다 마련하는 독립된 실행 환경입니다.

프로세스마다 코드 영역, 데이터 영역, 힙, 스택으로 이루어진 자기만의 메모리 공간이 주어집니다. 프로세스는 서로의 메모리에 직접 접근할 수 없으므로, 하나가 비정상 종료되어도 다른 프로세스의 메모리는 그대로 남습니다.

Unity 게임을 빌드해 실행하면 OS가 프로세스를 하나 만들고, 게임은 그 안에서 실행됩니다.

---

### 스레드

**스레드(Thread)**는 프로세스 안에서 실제로 코드를 실행하는 단위입니다. 프로세스가 프로그램이 동작할 환경을 마련한다면, 스레드는 그 환경 안에서 명령을 한 줄씩 처리해 나가는 흐름입니다.

한 프로세스 안에는 여러 스레드가 있을 수 있습니다. 이 스레드들은 각자 스택을 따로 쓰지만, 힙과 데이터 영역은 공유합니다. 따라서 여러 스레드가 힙에 있는 같은 객체를 동시에 읽거나 쓸 수 있습니다.

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

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다룬 것처럼, 지역 변수와 호출 정보가 쌓이는 스택은 스레드마다 따로 존재합니다. 반면 힙에 놓인 객체는 같은 프로세스 안의 여러 스레드가 공유합니다.

공유 힙 덕분에 같은 데이터를 복사 없이 다룰 수 있지만, 둘 이상의 스레드가 같은 객체를 동시에 수정하면 예상과 다른 결과가 나올 수 있습니다.

게임에서 무거운 계산을 여러 코어로 나눌 때 별도의 프로세스가 아니라 스레드를 쓰는 것도 이 때문입니다. 프로세스는 각자 메모리가 벽으로 막혀 있어, 데이터를 주고받으려면 한쪽 것을 복사해 건네야 합니다. 반면 한 프로세스 안의 스레드들은 같은 힙 메모리를 함께 쓰므로, 데이터를 복사하지 않고 그대로 둔 채 작업만 코어별로 나눠 맡을 수 있습니다.

---

### 멀티스레드의 이점

오늘날에는 모바일 기기의 CPU에도 여러 개의 코어가 들어 있습니다. 다만 스레드 하나는 한 순간에 한 코어에서만 실행되므로, 모든 작업을 단일 스레드에서 처리하면 한 코어에만 작업이 집중되고 나머지 코어는 충분히 활용되지 못합니다.

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

서로 독립적인 작업을 여러 코어에 나누어 동시에 실행하면 전체 처리 시간을 줄일 수 있습니다. 위 그림처럼 단일 스레드로 30ms 걸리던 작업이 세 코어에 고르게 나뉜다면 전체 처리 시간이 10ms 안팎으로 줄어들 수 있습니다.

이 장점은 경로 탐색, 물리 연산, 대량 데이터 처리처럼 CPU 계산량이 큰 작업에서 특히 중요합니다.

파일 읽기나 네트워크 요청처럼 I/O를 기다리는 작업에서도 스레드를 분리하면 도움이 됩니다. 한 작업이 응답을 기다리는 동안 다른 스레드가 CPU 작업을 계속 처리할 수 있기 때문입니다.

---

## Thread 클래스와 스레드 풀

스레드는 C#에서 직접 만들 수 있습니다. 다만 새로 만들고 없애는 데 자원과 시간이 들기 때문에, .NET은 미리 만들어 둔 스레드를 여러 작업이 재사용하는 스레드 풀을 제공합니다.

### Thread 클래스

스레드를 직접 만들 때는 `System.Threading.Thread` 클래스를 사용합니다.

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

`new Thread()`로 스레드 객체를 생성하고 `Start()`를 호출하면, OS가 새 스레드를 만들어 지정한 메서드를 그 스레드에서 실행합니다.

다만 스레드를 직접 만드는 데는 비용이 듭니다. OS는 커널 오브젝트를 만들고 스레드마다 스택 메모리를 확보해야 하며, 실행할 스레드를 바꿀 때마다 레지스터 상태를 저장하고 복원하는 컨텍스트 스위칭도 일어납니다. 스택 크기나 세부 비용은 런타임과 플랫폼에 따라 달라집니다.

짧은 작업이 자주 생기면 스레드를 매번 만들고 없애는 비용이 작업 자체보다 커질 수 있습니다.

비용과 더불어, 직접 만든 스레드에서는 멈추는 호출도 조심해야 합니다. `Thread.Sleep()`은 호출한 스레드를 지정한 시간 동안 멈추는데, 그동안 그 스레드는 아무 코드도 실행하지 않습니다.

그래서 Sleep은 **어느 스레드에서 호출하느냐**가 중요합니다. Unity의 메인 스레드는 입력 처리와 `Update()`, `LateUpdate()`, 렌더링 준비 같은 게임 루프의 핵심 작업을 처리하므로, 여기서 Sleep을 호출하면 게임 루프 전체가 멈춰 화면 갱신과 입력, 물리 처리까지 함께 지연됩니다. 반면 `new Thread()`로 만든 전용 워커 스레드에서 호출하면 그 워커만 잠시 멈추고, 게임 루프는 계속 실행됩니다.

이처럼 직접 만든 스레드는 생성 비용과 멈춤 관리를 모두 개발자가 감당해야 합니다. 그래서 짧은 작업마다 스레드를 새로 만들기보다, 미리 준비된 스레드를 빌려 쓰는 것이 효율적입니다.

### ThreadPool

.NET 런타임은 미리 만들어 둔 워커 스레드를 여러 작업이 돌려쓰는 **스레드 풀(ThreadPool)**을 제공합니다. 작업마다 스레드를 새로 만들고 없애지 않으므로, 그만큼 생성·폐기 비용을 줄일 수 있습니다.

이 절약은 스레드를 재사용하는 흐름에서 나옵니다. 작업이 들어오면 런타임은 대기 중인 워커 스레드 하나에 그 작업을 맡기고, 작업이 끝나도 그 스레드를 폐기하지 않고 풀로 돌려보냅니다. 돌아온 스레드는 풀에서 기다리다가 다음 작업을 맡습니다.

풀의 스레드 수는 고정되어 있지 않습니다. 모든 스레드가 일하고 있으면 런타임이 새 스레드를 더하고, 작업이 줄면 다시 줄입니다.

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

개발자는 작업을 큐에 넣고, 스레드 수와 재사용은 런타임에 맡길 수 있습니다.

---

## Task와 TAP

`Thread`와 `ThreadPool`은 코드를 다른 스레드에서 실행해 줍니다. 다만 둘 다 저수준 도구라, 실행을 맡긴 작업을 대표하는 객체를 돌려주지 않습니다. 그래서 작업이 끝나기를 기다리거나, 결과를 돌려받거나, 예외를 처리하려면 매번 직접 코드를 작성해야 합니다.

예를 들어 완료를 기다리는 `Join()`은 호출한 스레드를 블로킹해 Unity 메인 스레드에서는 게임 루프를 멈추고, 작업의 반환값은 공유 변수에 담아 `lock`으로 지켜야 하며, 워커 스레드에서 던져진 예외는 호출한 쪽으로 자동 전파되지 않아 `try-catch`로 직접 잡아 넘겨야 합니다.

**Task**는 이 문제들을 하나의 작업 객체로 묶어 해결합니다.

`Task`는 작업이 실행 중인지, 완료되었는지, 실패했는지 상태를 보관합니다. `await`으로 블로킹 없이 완료를 기다릴 수 있고, `Task<T>`는 완료 시 결과값을 제공합니다. 워커 스레드에서 발생한 예외도 `Task` 안에 저장되었다가 `await`하는 지점에서 다시 던져집니다.

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

`Task.Run()`은 넘겨받은 델리게이트를 스레드 풀의 워커 스레드에서 실행합니다.

호출자는 즉시 `Task` 객체를 받습니다. 이후 다른 작업을 계속하다가 결과가 필요한 시점에 `await`으로 완료를 기다리면 됩니다.

이처럼 `Task`를 반환하는 형태로 비동기 메서드를 작성하는 방식을 .NET에서는 **TAP(Task-based Asynchronous Pattern)**이라고 부릅니다.

TAP 이전에는 콜백 기반 비동기 패턴을 많이 사용했습니다. 하지만 비동기 작업이 연속되면 콜백 안에 다시 콜백이 들어가 코드 흐름을 읽기 어려워졌습니다.

TAP에서는 비동기 메서드가 `Task`나 `Task<T>`를 반환하고, 메서드 이름 끝에 `Async`를 붙이는 것을 관례로 삼습니다.

<br>

```csharp
async Task<string> LoadDataAsync(string path)
{
    string data = await File.ReadAllTextAsync(path);
    return data;
}
```

<br>

여기에 `async`/`await`을 사용하면 콜백을 중첩하지 않고도, 동기 코드와 비슷한 순서로 비동기 흐름을 작성할 수 있습니다.

예를 들어 데이터를 불러오고, 가공하고, 저장하는 세 단계를 차례로 이어야 한다면, 콜백 방식에서는 다음 단계가 앞 단계의 콜백 안으로 들어가 점점 깊이 중첩됩니다.

<br>

```csharp
// 콜백 방식 — 단계가 늘수록 안으로 깊어진다
LoadAsync(path, data =>
{
    ProcessAsync(data, result =>
    {
        SaveAsync(result, () =>
        {
            // 세 단계가 모두 끝난 뒤 할 일
        });
    });
});
```

<br>

같은 흐름을 `async`/`await`으로 쓰면 중첩이 사라지고, 위에서 아래로 읽는 동기 코드와 같은 순서가 됩니다.

<br>

```csharp
// async/await — 동기 코드처럼 위에서 아래로
var data = await LoadAsync(path);
var result = await ProcessAsync(data);
await SaveAsync(result);
// 세 단계가 모두 끝난 뒤 할 일
```

---

## async/await의 동작 원리

앞 절에서 `async`/`await`이 비동기 코드를 동기 코드처럼 깔끔하게 쓸 수 있게 해 준다는 것을 살펴봤습니다. 그 깔끔함 뒤에서 컴파일러가 적지 않은 일을 대신 처리하는데, 이 절에서는 그 처리 과정과 멈춘 코드가 어느 스레드에서 이어지는지를 살펴봅니다. 이 원리를 알면 `async`/`await`을 쓰면 멀티스레드가 된다는 흔한 오해도 바로잡을 수 있습니다.

### 상태 머신 변환

비동기 메서드는 `await` 지점에서 실행을 잠시 멈추고, 기다리던 작업이 끝나면 중단된 위치에서 다시 이어져야 합니다.

이 흐름을 구현하기 위해 C# 컴파일러는 `async` 메서드를 **상태 머신(State Machine)**으로 변환합니다.

각 `await` 지점은 상태가 나뉘는 경계가 됩니다. 컴파일러는 현재까지 사용한 지역 변수와 실행 위치를 상태 머신의 필드에 저장해, 멈췄던 자리에서 다시 이어 갈 수 있도록 준비해 둡니다.

`async`/`await`은 개발자가 이 상태 머신을 직접 작성하지 않아도 되게 해 주는 문법입니다.

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

`await` 지점에 도달하면 상태 머신은 먼저 기다리는 작업이 이미 끝났는지 확인합니다.

이미 끝났다면 결과를 꺼내 다음 코드로 바로 진행합니다. 아직 끝나지 않았다면 현재 상태를 저장하고 제어를 호출자에게 돌려줍니다. 이를 **양보(yield)**라고 볼 수 있습니다.

이렇게 양보가 일어나도 호출자 스레드는 블로킹되지 않으므로, 다른 작업을 계속 처리할 수 있습니다.

이후 비동기 작업이 완료되면 상태 머신은 저장된 위치에서 다시 실행되고, `await` 뒤의 코드를 이어서 실행합니다.

---

### 비동기와 멀티스레드는 다르다

앞서 본 양보는 호출한 스레드가 블로킹되지 않게 해 줍니다. `async`/`await`을 사용한다고 해서 자동으로 멀티스레드가 되는 것은 아닙니다.

`await`의 의미는 “작업이 끝날 때까지 현재 스레드를 블로킹하지 않겠다”에 가깝습니다. “이 작업을 반드시 다른 스레드에서 실행하겠다”는 의미는 아닙니다.

`await` 뒤의 코드가 어느 스레드에서 이어질지는 **동기화 컨텍스트(SynchronizationContext)**가 결정할 수 있습니다.

동기화 컨텍스트는 비동기 작업이 끝난 뒤 이어서 실행할 코드(continuation)를 정해진 스레드로 보내, 그 스레드에서 실행되게 하는 통로입니다.

<br>

|  | 비동기 (async/await) | 멀티스레드 |
|---|---|---|
| 핵심 원리 | 작업 완료를 기다리는 동안 스레드를 블로킹하지 않음 | 여러 스레드에서 동시에 코드를 실행 |
| 스레드 동작 | 같은 스레드 또는 다른 스레드에서 재개 가능 | 반드시 여러 스레드가 관여 |
| Unity에서 | `await` 후 → 메인 스레드에서 재개 (`UnitySynchronizationContext`) | `Task.Run()` → 스레드 풀에서 실행 |

<br>

Unity는 메인 스레드로 코드를 보내는 동기화 컨텍스트, 즉 `UnitySynchronizationContext`를 미리 마련해 둡니다. 이 컨텍스트에 코드를 맡기면 그 코드는 메인 스레드에서 실행됩니다. 그래서 메인 스레드에서 시작한 `async` 메서드가 `await`을 만나면, 이 컨텍스트가 "작업이 끝난 뒤 코드를 돌려보낼 곳"으로 기억됩니다.

기다리던 작업은 메인 스레드가 아닌 다른 스레드에서 끝나는 경우가 많습니다. 예를 들어 `Task.Run`으로 넘긴 계산은 워커 스레드에서 끝납니다. 이를 그대로 두면 `await` 뒤에 이어질 코드(continuation)도 그 워커 스레드에서 실행되고, 메인 스레드가 아니므로 Unity API를 호출할 수 없습니다.

`UnitySynchronizationContext`가 이 문제를 해결합니다. continuation을 워커 스레드에서 곧장 실행하는 대신, 앞서 기억해 둔 메인 스레드로 돌려보냅니다. 구체적으로는 continuation을 메인 스레드가 처리하는 큐에 넣어 두고, Unity 메인 루프가 매 프레임 이 큐를 비우며 continuation을 실행합니다. 그 결과 `await` 뒤의 코드는 다시 메인 스레드에서 이어지고, 그 안에서 Unity API를 안전하게 호출할 수 있습니다.

반대로 `ConfigureAwait(false)`를 사용하면 현재 동기화 컨텍스트로 돌아오려는 동작을 생략합니다.

메인 스레드로 돌아오는 비용을 줄일 수 있어 Unity API가 필요 없는 코드에서는 유용할 수 있습니다. 하지만 `await` 다음 코드가 어떤 스레드에서 실행될지 보장하기 어렵습니다.
그 상태에서 Unity API를 호출하면 메인 스레드 제약을 위반할 수 있습니다.

한 가지 예외가 있습니다. `await`에 도달한 시점에 기다리던 작업이 이미 끝나 있는 경우인데, 결과를 캐시에 담아 두는 비동기 메서드가 그 예입니다.

<br>

```csharp
Dictionary<string, Texture> cache = new();

async Task<Texture> GetTextureAsync(string url)
{
    // 캐시에 있으면 await 없이 바로 반환 → 이미 완료된 Task
    if (cache.TryGetValue(url, out var hit))
        return hit;

    // 캐시에 없을 때만 실제로 기다린다
    var texture = await DownloadAsync(url);
    cache[url] = texture;
    return texture;
}

// 호출 지점
var texture = await GetTextureAsync(url);
ApplyTexture(texture);
```

<br>

캐시에 값이 있으면 `GetTextureAsync`는 `await`을 거치지 않고 끝나므로, 호출 지점의 `await`은 이미 완료된 `Task`를 받습니다. 멈출 이유가 없으니 `await`은 실행을 멈추지 않고 `ApplyTexture`까지 같은 스레드에서 그대로 이어 갑니다. 멈춤도 재개도 없어 `ConfigureAwait` 설정 역시 영향을 주지 않습니다. 캐시에 값이 없을 때만 `DownloadAsync`에서 실제로 멈췄다가 재개되고, 그때는 앞서 설명한 동기화 컨텍스트 규칙을 따릅니다.

---

## 경쟁 조건과 동기화

`Thread`나 `Task.Run`으로 작업을 여러 스레드에 나누면 처리 속도를 끌어올릴 수 있습니다. 다만 여러 스레드가 같은 데이터를 함께 다루기 시작하면, 단일 스레드에서는 없던 문제가 따라옵니다. 이 절에서는 그 대표적인 문제인 경쟁 조건을 살펴보고, `lock`·`Interlocked`·`Monitor`로 막는 방법과, 그 과정에서 새로 생기는 함정인 데드락까지 다룹니다.

### 경쟁 조건 (Race Condition)

여러 스레드가 같은 데이터를 동시에 읽고 수정하면, 실행 순서에 따라 결과가 달라지는 **경쟁 조건(Race Condition)**이 생길 수 있습니다.

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

위 그림의 `counter++`는 코드에서는 한 줄이지만, 실제로는 값을 읽고, 1을 더하고, 다시 쓰는 단계로 나뉘어 실행됩니다.

한 스레드가 새 값을 쓰기 전에 다른 스레드가 같은 기존 값을 읽으면, 두 스레드가 같은 값에서 각각 1을 더합니다. 그 결과 한쪽의 증가가 덮어써져 최종 값이 기대보다 작아집니다.

경쟁 조건은 스레드의 실행 타이밍에 따라 나타날 때도 있고 그렇지 않을 때도 있어 재현하기 어렵습니다.

수천 번 실행해도 한 번만 나타나거나 특정 기기에서만 재현되기도 해서, 테스트는 통과해도 실제 환경에서 비로소 문제가 드러나는 경우가 많습니다.

---

### 동기화 메커니즘

경쟁 조건을 막으려면 공유 데이터에 한 번에 한 스레드만 접근하도록 순서를 통제해야 합니다. 이렇게 접근을 조율하는 것을 **동기화(Synchronization)**라고 하며, C#은 `lock`·`Interlocked`·`Monitor` 같은 도구를 제공합니다.

`lock`은 가장 기본이 되는 도구로, 블록 안에 한 번에 한 스레드만 들어가도록 막습니다.

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

스레드 A가 블록 안에 있는 동안 스레드 B는 밖에서 대기하므로, “읽기 → 증가 → 쓰기” 세 단계가 중간에 끊기지 않고 한 번에 끝납니다. 이 세 단계가 CPU 명령어 하나로 합쳐지는 것은 아니지만, `lock`이 상호 배제를 보장하는 덕분에 다른 스레드는 그 중간 상태를 보지 못합니다. 그래서 밖에서 보면 `counter++`가 더 쪼갤 수 없는 하나의 연산, 즉 **원자적(atomic)** 연산처럼 동작합니다.

`lock`이 여러 줄로 된 블록을 보호한다면, 값 하나를 증가시키거나 교체하는 단순한 연산에는 `Interlocked`가 더 알맞습니다. 두 도구가 안전을 지키는 방식은 다릅니다. `lock`은 “읽기 → 증가 → 쓰기” 세 단계 사이로 다른 스레드가 들어오지 못하게 막지만, `Interlocked`는 이 세 단계를 CPU가 제공하는 명령어 하나로 합칩니다. 명령어 하나는 실행 도중에 끊기지 않으니, 다른 스레드가 들어올 틈이 처음부터 없어 `lock` 없이도 안전합니다. 잠금을 걸고 푸는 과정도 없어 `lock`보다 가볍습니다.

<br>

```csharp
Interlocked.Increment(ref counter);  // 원자적으로 1 증가
```

<br>

지금까지 쓴 `lock`은 사실 더 낮은 수준의 `Monitor`를 간편하게 감싼 문법으로, 컴파일 과정에서 `Monitor.Enter()`와 `Monitor.Exit()` 호출로 바뀝니다. 그래서 `Monitor`를 직접 쓰면 `lock`이 감춰 둔 제어를 더 세밀하게 다룰 수 있습니다. 예를 들어 `lock`은 블록에 들어갈 차례가 올 때까지 무한정 기다리지만, `Monitor.TryEnter()`는 기다리는 시간에 상한을 둘 수 있습니다. 정해진 시간 안에 lock을 얻지 못하면 대기를 멈추고 다른 일을 처리하면 됩니다.

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

<br>

정리하면 여러 줄을 묶어 보호할 때는 `lock`, 값 하나를 다루는 단순 연산에는 `Interlocked`, 대기 시간 제어처럼 `lock`만으로 부족할 때는 `Monitor`를 직접 씁니다.

---

### 데드락 (Deadlock)

동기화를 잘못 사용하면 **데드락(Deadlock)**이 생길 수 있습니다.

데드락은 두 개 이상의 스레드가 서로 상대가 보유한 lock이 풀리기를 기다리면서, 어느 쪽도 더 이상 진행하지 못하는 상태입니다.

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

위 그림에서 스레드 A는 lockX를 잡은 채 lockY를, 스레드 B는 lockY를 잡은 채 lockX를 기다립니다. 둘 다 상대가 잡은 lock이 풀리기만 기다리는 순환 대기에 빠져, 어느 쪽도 더 진행하지 못합니다. 이런 순환 대기는 모든 스레드가 lock을 **같은 순서로** 얻게 하면 막을 수 있습니다. 예컨대 항상 lockX를 먼저, lockY를 나중에 얻도록 정해 두면, lockX를 기다리는 스레드는 아직 lockY를 잡고 있지 않으므로 순환이 생기지 않습니다.

중첩 잠금을 피하면 데드락을 더 확실히 막을 수 있습니다. 중첩 잠금은 한 `lock` 블록 안에서 또 다른 lock을 잡는 것으로, 위 그림에서 스레드 A가 lockX를 쥔 채 lockY를 잡으려 한 상황이 여기에 해당합니다. 한 스레드가 두 lock을 동시에 쥐지 않도록 lockX로 할 일을 끝내고 풀어 준 뒤에 lockY를 잡으면, “하나를 쥔 채 다른 하나를 기다리는” 상황이 처음부터 생기지 않습니다.

lock을 잡는 범위를 좁게 유지하는 것도 같은 맥락에서 도움이 됩니다. lock을 잡고 있는 시간이 짧을수록 다른 스레드가 기다리는 시간이 줄고, 여러 lock이 겹쳐 잡힐 가능성도 작아집니다.

Unity에서는 메인 스레드가 막히면 게임 루프 전체가 멈추므로, 데드락이 특히 치명적입니다. 대표적인 위험 사례로 메인 스레드에서 `task.Wait()`이나 `task.Result`를 호출하는 경우를 들 수 있습니다.

`Wait()`과 `Result`는 Task가 끝날 때까지 호출한 스레드를 블로킹합니다. 그런데 Unity의 `async` 메서드에서 `await` 이후의 continuation은 `UnitySynchronizationContext`를 거쳐 메인 스레드의 실행 큐에 예약됩니다. 메인 스레드가 `Wait()`으로 막혀 있으면 큐에 들어온 이 continuation을 실행하지 못하고, continuation이 실행되지 않으면 그 Task도 끝나지 못합니다.

결국 메인 스레드는 Task가 끝나기를 기다리고, 그 Task는 메인 스레드에서 실행될 continuation을 기다리는 순환 대기에 빠집니다.

---

## Unity의 메인 스레드 제약

앞에서 다룬 스레딩 기법은 대부분 플랫폼과 무관합니다. 하지만 Unity에서는 엔진 API의 대부분을 메인 스레드에서만 호출할 수 있다는 강한 제약이 더해집니다. 이 절에서는 이 제약이 왜 존재하는지 살펴보고, 그 안에서 멀티스레딩을 쓰는 방법 — 무거운 계산은 워커 스레드에 맡기고 그 결과만 메인 스레드에서 반영하는 방식 — 을 알아봅니다.

### Unity API는 메인 스레드 전용

Unity 엔진 API의 대부분은 **메인 스레드에서만 호출할 수 있습니다**.

`Transform.position`, `GameObject.SetActive()`, `Instantiate()`, `Destroy()` 같은 API를 워커 스레드에서 호출하면 런타임 에러가 발생합니다.

<br>

| API | 메인 스레드 | 워커 스레드 |
|---|---|---|
| `transform.position = newPos` | 정상 | UnityException |
| `gameObject.SetActive(true)` | 정상 | UnityException |
| `Instantiate(prefab)` | 정상 | UnityException |
| `Debug.Log("message")` | 정상 | 허용 (thread-safe) |

<br>

표에서 `Debug.Log`가 워커 스레드에서 허용되는 이유는 로깅 시스템이 스레드 안전하게 동작하도록 설계되어 있기 때문입니다.

로깅은 게임 오브젝트의 상태를 직접 변경하지 않고 메시지를 기록하는 작업이므로, 여러 스레드에서 호출해도 엔진 데이터 구조를 직접 훼손하지 않습니다.

반면 나머지 API 대부분은 C++로 작성된 엔진 내부 데이터를 직접 다룹니다. 이 데이터 구조가 여러 스레드의 동시 호출에 안전하도록 만들어지지 않았기 때문에, Unity는 이런 API를 메인 스레드로만 제한합니다.

모든 API 호출에 lock을 걸어 보호할 수도 있지만, 그렇게 하면 단일 스레드로 실행되는 일반적인 상황에서도 매 호출마다 동기화 비용을 지불해야 합니다.

대부분의 게임 로직은 메인 스레드에서 실행되므로, 모든 엔진 API에 이 비용을 추가하는 것은 성능상 불리합니다.

또한 여러 스레드가 같은 엔진 데이터를 동시에 수정하면 내부 상태가 일관성을 잃을 수 있습니다.

Transform을 예로 들면, 오브젝트의 월드 좌표는 부모-자식 계층을 따라 로컬 변환을 조합해 계산됩니다.

한 스레드가 부모의 위치를 바꾸면 자식의 월드 좌표도 다시 계산되어야 합니다.

이 재계산이 끝나기 전에 다른 스레드가 자식의 월드 좌표를 읽으면, 부모는 새 값인데 자식은 아직 갱신 전인 중간 상태를 읽을 수 있습니다.

Unity는 이런 상태 불일치를 막기 위해 API 호출 시 호출 스레드를 검사합니다. 메인 스레드가 아니라면 `UnityException`을 던져 호출을 차단합니다.

---

### 메인 스레드로 작업 전달

Unity API를 메인 스레드에서만 호출할 수 있다는 제약 안에서 멀티스레딩을 쓰려면, 작업을 계산 단계와 적용 단계로 나눠야 합니다. 무거운 계산은 워커 스레드에서 처리하고, 그 결과를 게임 오브젝트에 반영하는 일만 메인 스레드에서 실행합니다.

이 분리를 가장 간단히 구현하는 길은 `async`/`await`입니다. 앞서 본 것처럼 Unity는 메인 스레드에 `UnitySynchronizationContext`를 설정해 두므로, 메인 스레드에서 시작한 `async` 메서드에서는 `await` 이후의 continuation이 이 컨텍스트를 거쳐 메인 스레드의 실행 큐에 예약되고 다음 프레임에 실행됩니다. 따라서 무거운 계산을 `await Task.Run(...)`으로 워커 스레드에 넘기기만 하면, `await` 뒤의 코드는 다시 메인 스레드에서 이어져 Unity API를 그대로 호출할 수 있습니다.

<br>

```csharp
async Task ProcessDataAsync()
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

JSON 파싱, 경로 탐색, 절차적 생성처럼 CPU 시간이 필요한 계산을 이 패턴으로 분리하면, 메인 스레드의 프레임 시간을 줄이면서 결과는 안전하게 Unity 오브젝트에 반영할 수 있습니다.

`async`/`await`을 쓸 수 없는 경우도 있습니다. 직접 만든 스레드나, 콜백으로 결과를 돌려주는 외부 라이브러리가 그렇습니다. 이럴 때는 메인 스레드로 결과를 넘기는 통로를 직접 만들어야 합니다. 스레드 안전한 큐(`ConcurrentQueue`)에 실행할 `Action`을 넣어 두고, 메인 스레드의 `Update()`에서 매 프레임 그 큐를 비우며 작업을 하나씩 실행합니다.

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

이 방식은 `UnitySynchronizationContext`가 내부에서 자동으로 처리하던 메인 스레드 예약을 손으로 구현한 것과 같습니다. 큐와 `Update()` 폴링을 직접 관리해야 해서 코드는 늘지만, 자동 방식과 달리 작업을 어느 프레임에 실행할지 직접 정할 수 있습니다.

---

## 코루틴 vs async/await vs Job System

지금까지 C#의 스레딩과 비동기 도구, 그리고 경쟁 조건과 동기화를 살펴봤습니다. 이 도구들을 Unity에서 활용해 비동기 흐름이나 병렬 작업을 다룰 때는, 크게 **코루틴**, **`async`/`await`**, **Job System** 세 가지 방식을 쓸 수 있습니다.

세 방식은 서로를 대체하는 방식이 아니라, 상황에 따라 선택해 쓰는 도구입니다. 코드가 어느 스레드에서 실행되는지(그래서 Unity API를 호출할 수 있는지), GC 할당이 생기는지, 어떤 작업에 적합한지가 방식마다 다릅니다. 이 절에서는 세 방식을 이 기준들로 하나씩 비교합니다.

---

### 코루틴 (Coroutine)

코루틴은 하나의 작업을 여러 프레임에 나눠 실행하는, Unity에서 오래전부터 쓰인 방식입니다. `IEnumerator`를 반환하는 메서드를 `StartCoroutine()`으로 시작하면, 실행 도중 `yield return`을 만날 때마다 그 자리에서 멈췄다가 지정한 시점 — 이를테면 다음 프레임 — 에 멈춘 곳부터 다시 이어 갑니다.

이렇게 멈췄다 잇는 것은 새 스레드를 만드는 일이 아닙니다. 코루틴은 멀티스레드가 아니라 처음부터 끝까지 메인 스레드 하나에서 실행됩니다. 그래서 긴 작업을 여러 프레임에 분산해 한 프레임의 부담을 줄일 수는 있어도, 여러 CPU 코어를 동시에 쓰는 병렬 처리는 할 수 없습니다.

대신 모든 코드가 메인 스레드에서 실행되는 덕분에 Unity API를 자유롭게 호출할 수 있고, `WaitForSeconds`처럼 프레임과 시간 흐름에 맞춰 제어하기도 쉽습니다. 다만 코루틴을 시작할 때 `IEnumerator` 객체가 힙에 할당되어 GC 부담이 될 수 있고, `catch` 절이 붙은 `try` 블록 안에서는 `yield return`을 쓸 수 없으며(CS1626), 작업 결과를 반환값으로 곧바로 받기도 어렵습니다.

---

### async/await in Unity

`async`/`await`은 코루틴의 일부 제약을 보완합니다. `try-catch`로 예외를 처리할 수 있고, `Task<T>`로 결과값을 전달할 수 있으며, `Task.Run()`과 결합하면 실제 워커 스레드에서 계산을 실행할 수 있습니다. C# 표준 문법이므로 Unity 외부의 .NET 라이브러리와도 잘 맞습니다.

다만 Unity에서 쓸 때는 주의할 점이 몇 가지 있습니다. 첫째, `async void`를 되도록 피해야 합니다. `async void` 메서드에서 던져진 예외는 호출자가 `await`으로 붙잡을 수 없어서, Unity 콘솔에 로그만 남을 뿐 호출자가 흐름을 제어하거나 예외를 다시 던지기는 어렵습니다. 그래서 가능하면 `async Task`를 반환하고, 이벤트 핸들러처럼 `async void`가 불가피한 곳에서는 메서드 안에서 예외를 직접 처리합니다.

둘째, 오브젝트의 생명주기를 고려해야 합니다. 코루틴은 `MonoBehaviour`가 파괴되면 함께 멈추지만, async 메서드의 continuation은 이미 `UnitySynchronizationContext`에 예약돼 있을 수 있습니다. 오브젝트가 파괴된 뒤 그 continuation이 재개되면 이미 사라진 `Transform` 같은 대상에 접근하게 됩니다. 따라서 `await` 다음에는 `this == null`을 확인하거나, 지원되는 Unity 버전이라면 `destroyCancellationToken` 같은 취소 수단으로 오브젝트가 아직 유효한지 점검합니다.

셋째, `Task.Run()` 안에서는 Unity API를 호출할 수 없습니다. `Task.Run()`에 넘긴 코드는 스레드 풀의 워커 스레드에서 실행되고, Unity API는 메인 스레드 전용이기 때문입니다. 앞 절에서 본 대로 워커 스레드에서는 순수 계산만 하고, 그 결과를 오브젝트에 반영하는 코드는 `await Task.Run(...)` 뒤에 둬야 합니다.

한편 Unity는 자체 비동기 타입인 `Awaitable`도 제공합니다. `NextFrameAsync()`나 `WaitForSecondsAsync()`처럼 프레임 루프에 맞춘 비동기 API를 갖추고 있어 PlayerLoop에 맞춰 메인 스레드에서 재개되고, Awaitable 객체를 내부적으로 풀링해 `Task` 기반 코드보다 힙 할당을 줄입니다.

같은 이유로 UniTask 같은 서드파티 라이브러리도 많이 사용됩니다. UniTask는 async/await 스타일을 유지하면서 힙 할당을 줄이고, `WhenAll`, `WhenAny` 같은 조합 API와 PlayerLoop 기반 재개 시점 제어를 제공합니다.

---

### Job System

**C# Job System**은 일반적인 lock 기반 멀티스레딩과 출발점이 다릅니다. lock은 여러 스레드가 같은 데이터를 공유하는 상태에서 접근 순서를 통제합니다. 반면 Job System은 데이터 공유 방식을 제한해 경쟁 조건이 생기기 어려운 구조를 먼저 만듭니다.

이 구조는 Job을 [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다룬 `struct`, 즉 값 타입으로 정의하는 데서 출발합니다. Job 데이터가 워커 스레드로 넘어갈 때 값이 복사되면, 메인 스레드와 워커 스레드는 서로 다른 사본을 다룹니다. 같은 관리 객체를 동시에 수정하지 않으므로 lock 없이도 안전한 실행 구조를 만들 수 있습니다.

이 격리를 유지하기 위해 Job 안에서는 클래스나 일반 배열 같은 참조 타입을 사용할 수 없습니다. 참조 타입은 관리 힙의 객체를 가리키므로, Job이 참조를 들고 있으면 여러 스레드가 같은 힙 객체를 공유하게 됩니다. 대신 `NativeArray<T>` 같은 `NativeContainer`를 사용합니다. 이 컨테이너들은 관리 힙 바깥의 네이티브 메모리를 사용하고, Job System은 어떤 Job이 어떤 컨테이너를 읽거나 쓰는지 추적해 충돌을 검사합니다. Job이 관리 힙 객체를 직접 다루지 않기 때문에 GC 할당도 줄어듭니다.

이 제약은 Burst 컴파일러와도 연결됩니다. Burst는 Job 코드를 LLVM 기반 네이티브 코드로 컴파일하는 고성능 컴파일러입니다. [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서 다룬 IL2CPP도 C#을 네이티브 코드로 바꾸지만, IL2CPP는 일반 C# 기능을 폭넓게 지원해야 하므로, GC 쓰기 장벽, 가상 메서드 디스패치, 예외 처리 같은 런타임 지원 코드가 필요합니다. 반면 Burst는 Job 코드에서 성능에 불리한 기능을 제한합니다. 이 제한된 C# 범위를 HPC#(High-Performance C#)이라고 부르며, 클래스 생성이나 try-catch처럼 지원 범위를 벗어난 기능을 사용하면 컴파일 에러가 발생합니다.

이 기능들을 제한하는 이유는 저마다 런타임 비용으로 이어지기 때문입니다. 관리 객체를 금지하면 참조를 대입할 때 드는 GC 쓰기 장벽과 접근 전 null 검사가 빠지고, 가상 메서드를 막으면 호출 대상이 실행 시점의 타입에 따라 달라지지 않아 컴파일러가 이를 미리 확정할 수 있으며, 예외 처리를 제한하면 호출 스택을 거슬러 `catch`를 찾는 경로를 네이티브 코드에 담지 않아도 됩니다.

이런 제약을 적용하면 Job 코드는 데이터를 읽고 계산하고 쓰는 흐름에 가까워집니다. Burst는 이 코드를 대상으로 인라이닝, 루프 최적화, SIMD 벡터화 같은 최적화를 적용할 수 있습니다. 예를 들어 `NativeArray`를 순회하는 반복문은 [C# 런타임 기초 (2)](/dev/unity/CSharpRuntime-2/)에서 다룬 SIMD 명령어를 활용할 수 있는 형태로 최적화될 수 있습니다.

struct와 HPC# 제약이 설계 단계에서 데이터 공유를 제한한다면, 실행 시점의 검사는 Job System의 안전 시스템이 맡습니다. 안전 시스템은 `NativeContainer`마다 어떤 Job이 읽기 전용으로 접근하는지, 어떤 Job이 쓰기 권한을 갖는지 메타데이터로 기록합니다. `job.Schedule()`을 호출할 때 이 정보를 검사해, 두 Job이 같은 `NativeArray`에 동시에 쓰거나 한쪽이 쓰는 동안 다른 쪽이 읽으려 하면 `InvalidOperationException`을 발생시킵니다. 일반 멀티스레드 코드에서는 실행 타이밍이 겹쳐야 드러나는 문제를, Job System은 스케줄링 단계에서 미리 잡아냅니다.

같은 데이터를 순서대로 사용해야 하는 Job은 의존성으로 연결합니다. Job A가 `NativeArray`에 데이터를 쓰고 Job B가 그 결과를 읽어야 한다면, `jobB.Schedule(jobAHandle)`처럼 A의 `JobHandle`을 B에 전달합니다. 그러면 Job System은 A가 끝난 뒤에 B를 실행하므로 lock 없이도 실행 순서를 보장할 수 있습니다.

대신 Job System은 일반 C# 코드보다 작성 제약이 큽니다. 데이터를 `struct`와 `NativeContainer` 중심으로 설계해야 하고, `NativeArray` 같은 네이티브 메모리는 `Allocator.Temp`, `TempJob`, `Persistent`처럼 수명을 직접 정한 뒤 `Dispose()`로 해제해야 합니다. 작업이 복잡해지면 여러 `JobHandle`의 의존성 그래프도 직접 구성해야 합니다. 따라서 코루틴이나 async/await만으로 프레임 예산을 지킬 수 있다면 Job System을 도입할 필요는 없습니다. Job System은 CPU 병렬 처리의 이득이 이 설계 비용을 넘어서는 작업에 적합합니다.

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

실제 프로젝트에서는 세 방식을 함께 사용하는 경우도 많습니다. 예를 들어 네트워크에서 데이터를 `async`/`await`으로 받아 온 뒤, 그 데이터를 Job System으로 병렬 처리하고, 처리된 결과를 코루틴으로 여러 프레임에 나누어 화면에 반영할 수 있습니다.

다만 멀티스레딩이나 Job System을 쓰기 시작하면 경쟁 조건, 데드락, 생명주기 관리, 디버깅 난도가 함께 늘어납니다. 단일 스레드만으로 프레임 예산을 지킬 수 있다면 이런 복잡한 구조를 도입할 이유가 없습니다. 먼저 Unity Profiler의 CPU 모듈로 병목을 확인하고, 특정 작업이 프레임 시간을 크게 차지할 때 그 작업만 워커 스레드나 Job System으로 옮기는 순서가 현실적입니다.

---

## 마무리

이번 글에서는 C#의 멀티스레딩·비동기 도구를 Unity의 메인 스레드 제약과 함께 살펴보았습니다. 핵심은 다음과 같습니다.

- **프로세스**는 독립된 메모리 공간을 가진 실행 환경이고, **스레드**는 그 안에서 코드를 실제로 실행하는 흐름입니다.
- **ThreadPool**은 스레드를 미리 만들어 재사용해, 매번 생성하고 폐기하는 비용을 줄입니다.
- **Task**는 비동기 작업의 상태, 결과, 예외를 하나의 객체로 표현합니다.
- **async/await**으로 작성한 비동기 메서드는 컴파일러가 상태 머신으로 변환해, 스레드를 블로킹하지 않고 작업 완료를 기다립니다.
- **비동기와 멀티스레드**는 같은 개념이 아니며, `await` 이후 코드가 반드시 다른 스레드에서 실행되는 것도 아닙니다.
- **경쟁 조건**은 여러 스레드가 같은 데이터를 동시에 수정할 때 생기며, `lock`·`Interlocked`·`Monitor` 같은 동기화 도구로 막습니다.
- **Unity API**는 대부분 메인 스레드 전용이라, 워커 스레드에서는 순수 계산만 하고 결과 적용은 메인 스레드로 넘겨야 합니다.
- **코루틴·async/await·Job System**은 각각 프레임 분산과 타이밍 제어, I/O 대기와 백그라운드 계산, CPU 집약 병렬 처리에 적합합니다.

정리하면, 동시성을 더 깊게 사용할수록 성능 가능성은 커지지만 제약도 함께 늘어납니다. 코루틴은 메인 스레드 안에서 동작해 사용이 단순하지만 CPU 병렬 처리는 하지 않습니다. Job System은 여러 코어를 적극적으로 활용할 수 있지만, 데이터 구조와 메모리 수명, 의존성 관리까지 직접 설계해야 합니다. 어떤 도구를 사용할지는 추측이 아니라 프로파일링으로 확인한 병목을 기준으로 정해야 합니다.

이 시리즈에서 다룬 값 타입과 참조 타입, 런타임과 IL2CPP, 가비지 컬렉션, 스레딩과 비동기는 이후 최적화 주제의 기반이 됩니다. [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)에서는 Unity API 호출의 성능 특성과 메인 스레드 부하를 줄이는 방법을 다룹니다.

<br>

---

**관련 글**
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)

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
