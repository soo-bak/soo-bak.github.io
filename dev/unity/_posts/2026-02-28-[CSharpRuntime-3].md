---
layout: single
title: "C# 런타임 기초 (3) - 가비지 컬렉션의 기초 - soo:bak"
date: "2026-02-28 01:52:00 +0900"
description: GC의 필요성, Mark-and-Sweep, 세대별 GC, Unity의 Boehm GC, Incremental GC를 설명합니다.
tags:
  - Unity
  - C#
  - GC
  - 메모리
  - 모바일
---

## 메모리를 자동으로 관리하는 대가

[C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서 C# 코드가 IL로 컴파일된 뒤, Mono 또는 IL2CPP를 통해 기계어로 변환되어 실행되는 과정을 다루었습니다.

IL2CPP는 IL을 C++로 변환한 뒤 네이티브 컴파일하는 AOT 방식이고, Mono는 실행 시점에 JIT 컴파일하는 방식이었습니다.

<br>

런타임이 담당하는 역할은 코드 실행만이 아닙니다. 런타임의 핵심 기능 중 하나가 **메모리의 자동 관리**입니다.

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 다루었듯이, C# 코드에서 `new`로 참조 타입 객체를 생성하면 런타임이 힙에 메모리를 할당합니다. 그 객체가 더 이상 쓰이지 않으면, 런타임의 구성 요소인 **가비지 컬렉터(Garbage Collector, GC)**가 해당 메모리를 자동으로 회수합니다.

<br>

C나 C++에서는 개발자가 메모리를 직접 해제해야 하며, 실수하면 메모리 누수나 댕글링 포인터 같은 치명적 버그가 발생합니다.

GC는 이 해제 과정을 자동화하여 개발자가 해제를 신경 쓰지 않아도 되게 하지만, 그 대가로 GC가 실행되는 동안 CPU 시간을 소모하고, Unity의 Boehm GC는 힙 전체를 검사하면서 C# 스크립트 실행을 멈추는 Stop-the-World를 발생시킵니다.

<br>

이 글에서는 GC의 필요성, GC의 핵심 알고리즘인 Mark-and-Sweep, Unity의 Boehm GC와 .NET GC의 차이, 그리고 GC가 게임 성능에 미치는 영향을 다룹니다.

---

## GC의 필요성

### 수동 메모리 관리의 위험

C나 C++ 같은 언어에서는 개발자가 메모리를 직접 관리합니다. `malloc()`이나 `new`로 메모리를 할당하고, `free()`나 `delete`로 해제합니다.

할당과 해제의 타이밍을 개발자가 결정하므로, 정확하게 사용하면 효율적이지만, 실수가 끼어들면 세 가지 위험이 생깁니다.

<br>

<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" aria-label="수동 메모리 관리의 세 가지 위험: 메모리 누수, 댕글링 포인터, 이중 해제" style="width:100%;max-width:620px;display:block;margin:0 auto">
  <rect x="0" y="0" width="620" height="280" rx="8" fill="#1a1f1e" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="32" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">수동 메모리 관리의 세 가지 위험</text>
  <!-- 1. 메모리 누수 -->
  <text x="30" y="68" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">1. 메모리 누수 (Memory Leak)</text>
  <text x="50" y="88" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="13">할당한 메모리를 해제하지 않음</text>
  <text x="50" y="108" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 메모리가 계속 쌓여 결국 부족해짐</text>
  <!-- 2. 댕글링 포인터 -->
  <text x="30" y="140" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">2. 댕글링 포인터 (Dangling Pointer)</text>
  <text x="50" y="160" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="13">이미 해제된 메모리를 다시 참조함</text>
  <text x="50" y="180" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 엉뚱한 데이터를 읽거나 프로그램이 충돌함</text>
  <!-- 3. 이중 해제 -->
  <text x="30" y="212" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">3. 이중 해제 (Double Free)</text>
  <text x="50" y="232" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="13">같은 메모리를 두 번 해제함</text>
  <text x="50" y="252" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 메모리 관리 구조가 손상되어 예측 불가능한 동작 발생</text>
</svg>

<br>

메모리 누수는 할당만 하고 해제를 빠뜨릴 때 발생합니다.

프로그램이 오래 실행될수록 사용하지 않는 메모리가 누적됩니다.

모바일에서 특히 심각한데, iOS는 메모리 압박이 심해지면 `didReceiveMemoryWarning`을 보내지만, 앱이 충분히 빠르게 메모리를 확보하지 못하면 jetsam이 앱을 강제 종료시킵니다.

관리 힙 메모리는 GC가 실행되어야 회수되고, 회수되더라도 Boehm GC는 빈 공간을 OS에 반환하지 않으므로 프로세스의 메모리 사용량 자체는 줄어들지 않습니다. 따라서 이 경고에 대응하기 어렵습니다.

Android도 메모리 압박 상황에서 백그라운드 앱부터 순차적으로 종료합니다.

<br>

댕글링 포인터는 해제한 메모리를 여전히 참조할 때 발생합니다.

해제된 메모리 영역에 다른 데이터가 덮어쓰여지면, 이전 포인터를 통해 접근했을 때 전혀 다른 값을 읽게 됩니다.

재현 조건이 매번 달라지기 때문에 디버깅이 어려운 버그의 대표적 원인입니다.


<br>

이중 해제도 비슷한 맥락으로, 이미 해제된 메모리를 다시 해제하면 메모리 할당자의 내부 자료구조가 손상되어, 이후의 모든 할당과 해제가 예측 불가능해집니다.

<br>

이 세 가지 문제는 코드가 복잡해질수록 발생 가능성이 높아집니다.

객체 간에 참조가 얽혀 있으면, 어떤 객체를 언제 해제해야 안전한지 판단하기 어렵습니다.

객체 X를 A가 사용 중인데 B가 해제하면 댕글링 포인터가 되고, 둘 다 해제를 미루면 메모리 누수가 됩니다.

---

### GC의 역할

GC는 해제 책임을 개발자에게서 런타임으로 옮겨 이 문제를 해결합니다.

개발자는 메모리를 할당만 하고, 해제는 GC가 자동으로 수행합니다.

어떤 객체에 대한 참조가 더 이상 존재하지 않으면, GC가 그 객체의 메모리를 회수합니다.

<br>

<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" aria-label="수동 관리 vs 자동 관리: C/C++의 수동 해제와 GC 기반 자동 해제 비교" style="width:100%;max-width:620px;display:block;margin:0 auto">
  <text x="310" y="28" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">수동 관리 vs 자동 관리 (GC)</text>
  <!-- 수동 -->
  <rect x="15" y="45" width="285" height="110" rx="8" fill="#1a1f1e" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="157" y="68" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">수동 (C/C++)</text>
  <text x="30" y="92" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">개발자가 할당 → 개발자가 해제</text>
  <text x="30" y="114" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">실수하면 →</text>
  <text x="30" y="136" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">누수, 댕글링 포인터, 이중 해제</text>
  <!-- 자동 -->
  <rect x="320" y="45" width="285" height="110" rx="8" fill="#1a1f1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="462" y="68" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">자동 (C#, Java 등)</text>
  <text x="335" y="92" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">개발자가 할당 → GC가 해제</text>
  <text x="335" y="114" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">해제 시점을 개발자가 결정하지 않음</text>
  <text x="335" y="136" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="12">→ 댕글링 포인터, 이중 해제 불가능</text>
  <!-- 하단 결론 -->
  <rect x="100" y="175" width="420" height="40" rx="6" fill="#1a1f1e" stroke="#333" stroke-width="1"/>
  <text x="310" y="200" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 메모리 누수 위험 감소 (참조만 끊으면 GC가 회수)</text>
</svg>

<br>

개발자 입장에서는 `free()`나 `delete`를 호출할 필요 없이, 객체를 `new`로 만들고 다 쓴 뒤 참조를 끊기만 하면 됩니다. 참조가 끊어진 객체는 GC의 다음 실행 시점에 회수됩니다.

<br>

다만 GC에도 비용이 있습니다.

GC가 실행되는 동안 CPU 시간을 소모하고, 경우에 따라 프로그램 실행이 잠시 멈추기도 합니다. 이 비용을 예측하고 제어하려면 GC의 동작 원리를 이해해야 합니다.

---

## Mark-and-Sweep 알고리즘

GC가 회수 대상을 결정하는 가장 기본적인 알고리즘은 Mark-and-Sweep입니다.

### 도달 가능성 (Reachability)

**도달 가능성(Reachability)**은 GC가 객체의 생존 여부를 판단하는 기준입니다.

프로그램이 실행 중인 코드에서 참조 체인을 따라 접근할 수 있는 객체는 "살아있는" 것이고, 어떤 경로로도 접근할 수 없는 객체는 "죽은" 것입니다.

<br>

도달 가능성 판단의 출발점이 **GC 루트(GC Root)**입니다. GC 루트는 프로그램이 현재 직접 참조하고 있는 진입점들입니다.

<br>

<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" aria-label="GC 루트의 종류: 스택 변수, 정적 필드, CPU 레지스터" style="width:100%;max-width:620px;display:block;margin:0 auto">
  <rect x="0" y="0" width="620" height="280" rx="8" fill="#1a1f1e" stroke="#333" stroke-width="1.5"/>
  <text x="310" y="32" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">GC 루트의 종류</text>
  <!-- 1. 스택 변수 -->
  <text x="30" y="68" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">1. 스택 변수</text>
  <text x="50" y="88" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="13">현재 실행 중인 메서드의 지역 변수와 매개변수</text>
  <text x="50" y="108" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">메서드가 실행 중인 동안 참조하는 객체</text>
  <!-- 2. 정적 필드 -->
  <text x="30" y="142" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">2. 정적 필드 (static field)</text>
  <text x="50" y="162" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="13">클래스에 속하는 필드로, 프로그램이 끝날 때까지 유지됨</text>
  <text x="50" y="182" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">여기에 저장된 참조는 항상 도달 가능</text>
  <!-- 3. CPU 레지스터 -->
  <text x="30" y="216" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">3. CPU 레지스터</text>
  <text x="50" y="236" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="13">현재 CPU가 처리 중인 값</text>
  <text x="50" y="256" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">실행 중인 코드에서 사용하는 참조가 레지스터에 있을 수 있음</text>
</svg>

<br>

GC 루트가 직접 참조하는 객체는 도달 가능하고, 그 객체가 다시 참조하는 객체도 도달 가능합니다.

이렇게 참조 체인을 끝까지 따라가면 도달 가능한 객체의 전체 집합이 결정됩니다.

이 체인에 포함되지 않는 객체는 프로그램이 접근할 방법이 없으므로 해제해도 안전합니다.

---

### Mark 단계

GC 실행의 첫 번째 단계는 **Mark(표시)**입니다.

GC 루트에서 출발하여, 참조 그래프를 따라 도달 가능한 모든 객체에 "살아있음" 표시를 합니다.

<br>

<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" aria-label="Mark 단계의 동작: GC 루트에서 참조 그래프를 따라 도달 가능한 객체를 표시하는 과정" style="width:100%;max-width:720px;display:block;margin:0 auto">
  <defs>
    <marker id="m4-ag" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
    <marker id="m4-ac" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#00d4ff"/></marker>
  </defs>
  <!-- Title -->
  <text x="360" y="28" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">Mark 단계의 동작</text>
  <text x="360" y="52" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">GC 루트들</text>
  <!-- Root boxes -->
  <rect x="80" y="65" width="120" height="45" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="140" y="93" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="14">스택 변수</text>
  <rect x="300" y="65" width="120" height="45" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="360" y="93" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="14">정적 필드</text>
  <rect x="520" y="65" width="120" height="45" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="580" y="93" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="14">CPU 레지스터</text>
  <!-- Root arrows -->
  <line x1="140" y1="110" x2="140" y2="165" stroke="#00d4ff" stroke-width="2" marker-end="url(#m4-ac)"/>
  <line x1="360" y1="110" x2="360" y2="165" stroke="#00d4ff" stroke-width="2" marker-end="url(#m4-ac)"/>
  <line x1="580" y1="110" x2="580" y2="165" stroke="#00d4ff" stroke-width="2" marker-end="url(#m4-ac)"/>
  <!-- Row 1: reachable objects -->
  <rect x="90" y="175" width="100" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="130" y="200" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">객체 A</text>
  <text x="195" y="195" fill="#73f38f" font-family="monospace" font-size="13">✓</text>
  <rect x="310" y="175" width="100" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="350" y="200" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">객체 D</text>
  <text x="415" y="195" fill="#73f38f" font-family="monospace" font-size="13">✓</text>
  <rect x="530" y="175" width="100" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="570" y="200" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">객체 F</text>
  <text x="635" y="195" fill="#73f38f" font-family="monospace" font-size="13">✓</text>
  <!-- Arrows from A to B and E -->
  <path d="M140 215 L140 250 L220 250 L220 275" fill="none" stroke="#73f38f" stroke-width="2" marker-end="url(#m4-ag)"/>
  <path d="M155 215 L155 240 L440 240 L440 275" fill="none" stroke="#73f38f" stroke-width="2" marker-end="url(#m4-ag)"/>
  <!-- Row 2: B and E -->
  <rect x="170" y="285" width="100" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="210" y="310" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">객체 B</text>
  <text x="275" y="305" fill="#73f38f" font-family="monospace" font-size="13">✓</text>
  <rect x="390" y="285" width="100" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="430" y="310" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">객체 E</text>
  <text x="495" y="305" fill="#73f38f" font-family="monospace" font-size="13">✓</text>
  <!-- Arrow from B to C -->
  <path d="M220 325 L220 355 L310 355 L310 375" fill="none" stroke="#73f38f" stroke-width="2" marker-end="url(#m4-ag)"/>
  <!-- Row 3: C -->
  <rect x="260" y="385" width="100" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="300" y="410" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">객체 C</text>
  <text x="365" y="405" fill="#73f38f" font-family="monospace" font-size="13">✓</text>
  <!-- Unreachable objects -->
  <text x="600" y="300" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="12">표시되지 않은 객체들</text>
  <text x="600" y="316" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="12">(도달 불가)</text>
  <rect x="530" y="330" width="80" height="35" rx="6" fill="#1a1f1e" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="570" y="352" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">객체 G</text>
  <rect x="625" y="330" width="80" height="35" rx="6" fill="#1a1f1e" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="665" y="352" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">객체 H</text>
  <rect x="578" y="378" width="80" height="35" rx="6" fill="#1a1f1e" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="618" y="400" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">객체 I</text>
</svg>

<br>

GC는 루트에서 시작하여 참조 그래프를 탐색합니다.

대부분의 GC 구현은 마크 스택(mark stack)을 사용한 깊이 우선 탐색을 채택하는데, 스택 자료구조가 인접한 메모리를 순차적으로 사용하여 캐시 적중률이 높고, 너비 우선 탐색에 필요한 큐보다 보조 메모리 소비가 적기 때문입니다.

방문한 객체마다 "도달 가능" 표시를 남기므로, 탐색이 끝난 뒤 표시가 없는 객체는 어떤 경로로도 접근할 수 없는 죽은 객체입니다.

---

### Sweep 단계

Mark가 끝나면 **Sweep(소거)** 단계로 넘어갑니다.

이 단계에서 GC는 힙의 모든 객체를 순회하면서, Mark 표시가 없는 객체의 메모리를 해제합니다.

<br>

<svg viewBox="0 0 720 310" xmlns="http://www.w3.org/2000/svg" aria-label="Sweep 단계의 동작: Mark 표시가 없는 객체의 메모리를 해제하는 과정" style="width:100%;max-width:720px;display:block;margin:0 auto">
  <text x="360" y="28" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">Sweep 단계의 동작</text>
  <!-- Mark 후 label -->
  <text x="40" y="65" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">Mark 후:</text>
  <!-- Mark 후 cells -->
  <rect x="40" y="75" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="65" y="98" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">A ✓</text>
  <rect x="110" y="75" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="135" y="98" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">B ✓</text>
  <rect x="180" y="75" width="70" height="40" fill="#1a1f1e" stroke="#555" stroke-width="2"/>
  <text x="205" y="98" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">G</text>
  <rect x="250" y="75" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="275" y="98" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">C ✓</text>
  <rect x="320" y="75" width="70" height="40" fill="#1a1f1e" stroke="#555" stroke-width="2"/>
  <text x="345" y="98" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">H</text>
  <rect x="390" y="75" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="415" y="98" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">D ✓</text>
  <rect x="460" y="75" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="485" y="98" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">E ✓</text>
  <rect x="530" y="75" width="70" height="40" fill="#1a1f1e" stroke="#555" stroke-width="2"/>
  <text x="555" y="98" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">I</text>
  <rect x="600" y="75" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="625" y="98" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">F ✓</text>
  <!-- Sweep 후 label -->
  <text x="40" y="155" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">Sweep 후:</text>
  <!-- Sweep 후 cells -->
  <rect x="40" y="165" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="65" y="188" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">A ✓</text>
  <rect x="110" y="165" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="135" y="188" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">B ✓</text>
  <rect x="180" y="165" width="70" height="40" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="205" y="188" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">빈</text>
  <rect x="250" y="165" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="275" y="188" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">C ✓</text>
  <rect x="320" y="165" width="70" height="40" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="345" y="188" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">빈</text>
  <rect x="390" y="165" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="415" y="188" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">D ✓</text>
  <rect x="460" y="165" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="485" y="188" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">E ✓</text>
  <rect x="530" y="165" width="70" height="40" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="555" y="188" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">빈</text>
  <rect x="600" y="165" width="70" height="40" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="625" y="188" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">F ✓</text>
  <!-- 해제됨 arrows -->
  <line x1="215" y1="205" x2="215" y2="225" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="215" y="240" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">해제됨</text>
  <line x1="355" y1="205" x2="355" y2="225" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="355" y="240" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">해제됨</text>
  <line x1="565" y1="205" x2="565" y2="225" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="565" y="240" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">해제됨</text>
  <!-- Legend -->
  <rect x="200" y="265" width="14" height="14" fill="#1a1f1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="220" y="277" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">살아있음</text>
  <rect x="310" y="265" width="14" height="14" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="330" y="277" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">해제됨 (새 할당에 사용 가능)</text>
</svg>

<br>

Sweep이 끝나면 살아있는 객체만 남고, 나머지 메모리는 새 할당에 사용할 수 있는 빈 공간이 됩니다.

**Mark-and-Sweep 알고리즘**은 이 두 단계——도달 가능한 객체를 표시하고, 표시되지 않은 객체를 해제하는——를 합친 GC의 가장 기본적인 형태입니다.

<br>

GC 알고리즘에는 다른 방식도 있습니다.

대표적인 대안이 **참조 카운팅(Reference Counting)**으로, 각 객체가 자신을 참조하는 횟수를 추적하다가 참조 횟수가 0이 되면 즉시 해제합니다.

그러나 A가 B를 참조하고 B가 A를 참조하는 **순환 참조**가 있으면, 외부에서 접근할 수 없어도 참조 횟수가 0이 되지 않아 영원히 해제되지 않습니다.

Mark-and-Sweep은 루트에서의 도달 가능성만을 기준으로 삼기 때문에, 순환 참조 여부와 관계없이 도달 불가능한 객체를 수거합니다.

---

## 세대별 GC (Generational GC)

Mark-and-Sweep은 GC의 기본 알고리즘이지만, 비세대(non-generational) 방식에서는 GC가 실행될 때마다 힙 전체가 수집 대상이 됩니다.

힙에 10만 개의 객체가 있으면 Mark와 Sweep 모두 그 10만 개를 대상으로 동작하므로, 힙이 커질수록 GC 실행 시간도 길어집니다.

데스크톱/서버용 .NET 런타임은 이 비용을 줄이기 위해 **세대별 GC(Generational GC)**를 도입했습니다.

### 세대 가설

세대별 GC의 토대는 **세대 가설(Generational Hypothesis)**입니다.

<br>

세대 가설의 핵심은 두 가지입니다.

첫째, **대부분의 객체는 수명이 짧다**는 것입니다. 임시 문자열, 루프 안에서 생성된 중간 결과물, 메서드 내부의 임시 객체처럼 생성 직후 곧바로 쓸모없어지는 객체가 전체의 대부분을 차지합니다.

둘째, **한 번 오래 살아남은 객체는 계속 생존할 가능성이 높다**는 것입니다. 캐시, 설정 데이터, 매니저 클래스 인스턴스처럼 프로그램 전체 수명 동안 유지되는 객체가 이에 해당합니다.

<br>

<svg viewBox="0 0 600 320" xmlns="http://www.w3.org/2000/svg" aria-label="객체 수명 분포: 대부분의 객체는 수명이 짧고, 소수만 오래 생존하는 분포" style="width:100%;max-width:600px;display:block;margin:0 auto">
  <text x="300" y="28" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">객체 수명 분포 (개념적)</text>
  <!-- Y axis -->
  <text x="55" y="80" text-anchor="end" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12" transform="rotate(-90,30,140)">객체 수</text>
  <line x1="70" y1="50" x2="70" y2="240" stroke="#555" stroke-width="1.5"/>
  <!-- X axis -->
  <line x1="70" y1="240" x2="560" y2="240" stroke="#555" stroke-width="1.5"/>
  <polygon points="560,236 570,240 560,244" fill="#555"/>
  <text x="320" y="262" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">수명</text>
  <!-- X axis labels -->
  <text x="110" y="255" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">짧음</text>
  <text x="520" y="255" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">긴 수명</text>
  <!-- Bars -->
  <rect x="85" y="60" width="40" height="180" rx="2" fill="#73f38f" opacity="0.9"/>
  <rect x="135" y="100" width="40" height="140" rx="2" fill="#73f38f" opacity="0.75"/>
  <rect x="185" y="140" width="40" height="100" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="235" y="175" width="40" height="65" rx="2" fill="#73f38f" opacity="0.45"/>
  <rect x="285" y="200" width="40" height="40" rx="2" fill="#73f38f" opacity="0.35"/>
  <rect x="335" y="215" width="40" height="25" rx="2" fill="#73f38f" opacity="0.28"/>
  <rect x="385" y="222" width="40" height="18" rx="2" fill="#73f38f" opacity="0.22"/>
  <rect x="435" y="228" width="40" height="12" rx="2" fill="#73f38f" opacity="0.18"/>
  <rect x="485" y="232" width="40" height="8" rx="2" fill="#73f38f" opacity="0.15"/>
  <!-- Annotations -->
  <line x1="105" y1="275" x2="105" y2="285" stroke="#00d4ff" stroke-width="1"/>
  <line x1="105" y1="285" x2="200" y2="285" stroke="#00d4ff" stroke-width="1"/>
  <line x1="200" y1="275" x2="200" y2="285" stroke="#00d4ff" stroke-width="1"/>
  <text x="152" y="302" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="11">대부분의 객체가</text>
  <text x="152" y="316" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="11">여기에 집중 (짧은 수명)</text>
  <line x1="400" y1="275" x2="400" y2="285" stroke="#888" stroke-width="1"/>
  <line x1="400" y1="285" x2="520" y2="285" stroke="#888" stroke-width="1"/>
  <line x1="520" y1="275" x2="520" y2="285" stroke="#888" stroke-width="1"/>
  <text x="460" y="302" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">소수의 객체가</text>
  <text x="460" y="316" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">오래 생존</text>
</svg>

<br>

대부분의 쓰레기가 수명이 짧은 객체에서 나온다면, 그 객체들이 모여 있는 영역만 자주 검사하는 것으로 충분합니다.

매번 힙 전체를 검사할 필요가 없습니다.

---

### Gen 0, Gen 1, Gen 2

.NET의 세대별 GC는 힙을 Gen 0, Gen 1, Gen 2 세 영역으로 나눕니다.

새로 생성된 객체는 Gen 0에 할당되고, GC 수집에서 살아남을수록 높은 세대로 승격됩니다.

세대가 높을수록 영역 크기는 크지만, 수집 빈도는 낮습니다.

<br>

<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg" aria-label=".NET의 세대별 힙 구조: Gen 0, Gen 1, Gen 2로 나뉜 관리 힙" style="width:100%;max-width:700px;display:block;margin:0 auto">
  <text x="350" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">.NET의 세대별 힙 구조</text>
  <!-- Outer: 관리 힙 -->
  <rect x="20" y="40" width="660" height="230" rx="8" fill="none" stroke="#555" stroke-width="2"/>
  <text x="350" y="62" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">관리 힙</text>
  <!-- Gen 0 -->
  <rect x="40" y="75" width="130" height="180" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="105" y="98" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="14" font-weight="bold">Gen 0</text>
  <text x="105" y="122" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">새 객체</text>
  <text x="105" y="138" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">할당</text>
  <line x1="55" y1="155" x2="155" y2="155" stroke="#333" stroke-width="1"/>
  <text x="105" y="174" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">크기: ~256KB</text>
  <line x1="55" y1="185" x2="155" y2="185" stroke="#333" stroke-width="1"/>
  <text x="105" y="204" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">수집: 자주</text>
  <rect x="55" y="218" width="100" height="22" rx="4" fill="#73f38f" opacity="0.2"/>
  <text x="105" y="234" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="10">빈도 높음</text>
  <!-- Gen 1 -->
  <rect x="190" y="75" width="180" height="180" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="280" y="98" text-anchor="middle" fill="#00d4ff" font-family="monospace" font-size="14" font-weight="bold">Gen 1</text>
  <text x="280" y="122" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">Gen 0에서</text>
  <text x="280" y="138" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">살아남은 객체</text>
  <line x1="205" y1="155" x2="355" y2="155" stroke="#333" stroke-width="1"/>
  <text x="280" y="174" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">크기: ~2MB</text>
  <line x1="205" y1="185" x2="355" y2="185" stroke="#333" stroke-width="1"/>
  <text x="280" y="204" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">수집: 가끔</text>
  <rect x="215" y="218" width="130" height="22" rx="4" fill="#00d4ff" opacity="0.15"/>
  <text x="280" y="234" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="10">빈도 중간</text>
  <!-- Gen 2 -->
  <rect x="390" y="75" width="270" height="180" rx="6" fill="#1a1f1e" stroke="#ffd700" stroke-width="2"/>
  <text x="525" y="98" text-anchor="middle" fill="#ffd700" font-family="monospace" font-size="14" font-weight="bold">Gen 2</text>
  <text x="525" y="122" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">Gen 1에서</text>
  <text x="525" y="138" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">살아남은 객체 (장기 생존)</text>
  <line x1="405" y1="155" x2="645" y2="155" stroke="#333" stroke-width="1"/>
  <text x="525" y="174" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">크기: 제한 없음</text>
  <line x1="405" y1="185" x2="645" y2="185" stroke="#333" stroke-width="1"/>
  <text x="525" y="204" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">수집: 드물게</text>
  <rect x="430" y="218" width="190" height="22" rx="4" fill="#ffd700" opacity="0.12"/>
  <text x="525" y="234" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="10">빈도 낮음 (Full GC)</text>
</svg>

<br>

**Gen 0**은 새로 할당된 객체가 처음 들어가는 세대입니다.

크기가 작고(보통 수백 KB), GC가 가장 자주 검사합니다.

Gen 0에 공간이 부족하면 Gen 0 수집이 발생하고, 여기서 살아남은 객체(Mark 단계에서 도달 가능한 객체)는 **Gen 1**로 승격(Promotion)됩니다.

<br>

**Gen 1**은 Gen 0 수집을 한 번 통과한 객체가 머무는 영역으로, Gen 0보다 덜 자주 검사합니다.

Gen 1 수집에서도 살아남은 객체는 **Gen 2**로 승격됩니다.

<br>

**Gen 2**는 장기 생존 객체가 머무는 영역이며, 수집 빈도가 가장 낮습니다.

Gen 2 수집은 전체 힙 수집(Full GC)에 해당하므로 비용이 가장 높습니다.

<br>

<svg viewBox="0 0 680 520" xmlns="http://www.w3.org/2000/svg" aria-label="세대별 GC의 수집 흐름: 새 객체가 Gen 0에서 Gen 2까지 승격되는 과정" style="width:100%;max-width:680px;display:block;margin:0 auto">
  <defs>
    <marker id="m8-a" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#f9fffb"/></marker>
    <marker id="m8-r" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ff6b6b"/></marker>
    <marker id="m8-g" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
  </defs>
  <text x="340" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">세대별 GC의 수집 흐름</text>
  <!-- 새 객체 생성 -->
  <rect x="70" y="45" width="150" height="36" rx="18" fill="#1a1f1e" stroke="#f9fffb" stroke-width="1.5"/>
  <text x="145" y="68" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="13">새 객체 생성</text>
  <line x1="145" y1="81" x2="145" y2="100" stroke="#f9fffb" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Gen 0에 할당 -->
  <rect x="70" y="108" width="150" height="36" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="145" y="131" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">Gen 0에 할당</text>
  <!-- trigger -->
  <text x="240" y="162" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">Gen 0이 가득 참</text>
  <line x1="145" y1="144" x2="145" y2="170" stroke="#f9fffb" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Gen 0 수집 -->
  <rect x="50" y="178" width="190" height="36" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="145" y="198" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">Gen 0 수집 실행</text>
  <text x="145" y="210" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="10">(빠름, 범위 작음)</text>
  <!-- Branch: dead -->
  <line x1="100" y1="214" x2="100" y2="242" stroke="#ff6b6b" stroke-width="1.5" marker-end="url(#m8-r)"/>
  <text x="100" y="262" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">죽은 객체 → 해제</text>
  <!-- Branch: survive to Gen 1 -->
  <line x1="195" y1="214" x2="195" y2="232" stroke="#73f38f" stroke-width="1.5"/>
  <line x1="195" y1="232" x2="350" y2="232" stroke="#73f38f" stroke-width="1.5"/>
  <line x1="350" y1="232" x2="350" y2="252" stroke="#73f38f" stroke-width="1.5" marker-end="url(#m8-g)"/>
  <text x="273" y="226" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="11">살아남은 객체</text>
  <!-- Gen 1로 승격 -->
  <rect x="280" y="260" width="140" height="32" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="350" y="281" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">Gen 1로 승격</text>
  <!-- trigger -->
  <text x="440" y="312" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">Gen 1이 가득 참</text>
  <line x1="350" y1="292" x2="350" y2="320" stroke="#f9fffb" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Gen 1 수집 -->
  <rect x="265" y="328" width="170" height="32" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="350" y="349" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">Gen 1 수집 실행</text>
  <!-- Branch: dead -->
  <line x1="310" y1="360" x2="310" y2="388" stroke="#ff6b6b" stroke-width="1.5" marker-end="url(#m8-r)"/>
  <text x="310" y="408" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">죽은 객체 → 해제</text>
  <!-- Branch: survive to Gen 2 -->
  <line x1="400" y1="360" x2="400" y2="378" stroke="#73f38f" stroke-width="1.5"/>
  <line x1="400" y1="378" x2="540" y2="378" stroke="#73f38f" stroke-width="1.5"/>
  <line x1="540" y1="378" x2="540" y2="398" stroke="#73f38f" stroke-width="1.5" marker-end="url(#m8-g)"/>
  <text x="470" y="372" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="11">살아남은 객체</text>
  <!-- Gen 2로 승격 -->
  <rect x="470" y="406" width="140" height="32" rx="6" fill="#1a1f1e" stroke="#ffd700" stroke-width="2"/>
  <text x="540" y="427" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="13">Gen 2로 승격</text>
  <!-- trigger -->
  <text x="540" y="460" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">Gen 2 수집은 드물게 실행</text>
  <line x1="540" y1="438" x2="540" y2="468" stroke="#f9fffb" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Full GC -->
  <rect x="470" y="476" width="140" height="32" rx="6" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2"/>
  <text x="540" y="497" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">Full GC (비용 높음)</text>
</svg>

<br>

세대 가설에 따르면 대부분의 객체는 수명이 짧으므로, 크기가 작은 Gen 0만 자주 검사하는 것으로 대부분의 쓰레기를 처리할 수 있습니다.

전체 힙을 검사하는 Full GC는 드물게만 발생합니다.

<br>

.NET의 세대별 GC는 수집 후 **압축(Compaction)**도 수행합니다.

살아남은 객체를 힙의 한쪽으로 밀어 넣어 빈 공간을 연속으로 만드는 과정입니다.

압축 덕분에 새 객체를 할당할 때 연속된 빈 공간을 바로 사용할 수 있고, 메모리 단편화가 발생하지 않습니다.

---

## Unity의 Boehm GC

Unity의 Mono 런타임은 위에서 설명한 .NET의 세대별 GC를 사용하지 않습니다.

대신 **Boehm GC(Boehm-Demers-Weiser Garbage Collector)**를 사용합니다.

Boehm GC는 세대를 나누지 않고(**비세대**, Non-generational), 수집 후 객체를 이동시키지 않으며(**비압축**, Non-compacting), 스택의 참조를 정확히 구분하지 못합니다(**보수적**, Conservative).

이 세 가지 특성이 .NET GC와의 핵심 차이이자, Unity에서 GC 비용이 높은 근본 원인입니다.

---

### 비세대 (Non-generational)

Boehm GC는 세대를 구분하지 않습니다.

.NET GC처럼 Gen 0만 검사하는 부분 수집이 없으므로, GC가 실행되면 매번 힙 전체를 처음부터 끝까지 검사합니다.

<br>

<svg viewBox="0 0 680 310" xmlns="http://www.w3.org/2000/svg" aria-label=".NET GC vs Boehm GC 수집 범위 비교: 세대별 부분 수집 vs 전체 힙 수집" style="width:100%;max-width:680px;display:block;margin:0 auto">
  <text x="340" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">.NET GC vs Boehm GC: 수집 범위</text>
  <!-- .NET GC -->
  <text x="40" y="58" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">.NET GC (세대별):</text>
  <rect x="40" y="68" width="130" height="50" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="2"/>
  <text x="105" y="98" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="13">Gen 0</text>
  <rect x="170" y="68" width="180" height="50" rx="4" fill="#1a1f1e" stroke="#555" stroke-width="1.5"/>
  <text x="260" y="98" text-anchor="middle" fill="#555" font-family="monospace" font-size="13">Gen 1</text>
  <rect x="350" y="68" width="290" height="50" rx="4" fill="#1a1f1e" stroke="#555" stroke-width="1.5"/>
  <text x="495" y="98" text-anchor="middle" fill="#555" font-family="monospace" font-size="13">Gen 2</text>
  <!-- highlight bracket for Gen 0 -->
  <line x1="45" y1="126" x2="45" y2="136" stroke="#73f38f" stroke-width="2"/>
  <line x1="45" y1="136" x2="165" y2="136" stroke="#73f38f" stroke-width="2"/>
  <line x1="165" y1="126" x2="165" y2="136" stroke="#73f38f" stroke-width="2"/>
  <text x="105" y="154" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="12">← 검사 →</text>
  <text x="105" y="170" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">Gen 0 수집: 여기만 검사 (빠름)</text>
  <!-- Boehm GC -->
  <text x="40" y="202" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">Boehm GC (비세대):</text>
  <rect x="40" y="212" width="600" height="50" rx="4" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2"/>
  <text x="340" y="242" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">전체 힙</text>
  <!-- full scan bracket -->
  <line x1="45" y1="270" x2="45" y2="280" stroke="#ff6b6b" stroke-width="2"/>
  <line x1="45" y1="280" x2="635" y2="280" stroke="#ff6b6b" stroke-width="2"/>
  <line x1="635" y1="270" x2="635" y2="280" stroke="#ff6b6b" stroke-width="2"/>
  <text x="340" y="296" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">매번 전부 검사 (힙이 클수록 느림)</text>
</svg>

<br>

힙에 객체가 1000개 있으면 1000개 전부를 검사합니다.

그 중 990개가 장기 생존 객체여도 예외 없이 모두 검사 대상입니다.

Mark 단계의 비용은 살아있는 객체 수에, Sweep 단계의 비용은 전체 힙 크기에 비례하므로, 힙이 커질수록 GC 실행 시간이 길어집니다.

---

### 비압축 (Non-compacting)

Boehm GC는 Sweep 후에 객체를 이동시키지 않습니다.

죽은 객체를 해제하면 그 자리가 빈 공간으로 남고, 살아있는 객체 사이사이에 빈 공간이 흩어집니다. 이를 **메모리 단편화(Fragmentation)**라 합니다.

<br>

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg" aria-label="비압축 GC의 단편화: 빈 공간이 흩어져 있어 충분한 총량에도 큰 객체를 할당할 수 없는 상황" style="width:100%;max-width:700px;display:block;margin:0 auto">
  <text x="350" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">비압축 GC의 단편화</text>
  <text x="40" y="52" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="13">Sweep 후:</text>
  <!-- Memory cells - widths proportional to byte sizes -->
  <!-- A 20B -->
  <rect x="40" y="62" width="52" height="50" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="66" y="83" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">A</text>
  <text x="66" y="100" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">20B</text>
  <!-- 빈 30B -->
  <rect x="92" y="62" width="78" height="50" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="131" y="83" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">빈</text>
  <text x="131" y="100" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="10">30B</text>
  <!-- C 40B -->
  <rect x="170" y="62" width="104" height="50" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="222" y="83" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">C</text>
  <text x="222" y="100" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">40B</text>
  <!-- 빈 20B -->
  <rect x="274" y="62" width="52" height="50" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="300" y="83" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">빈</text>
  <text x="300" y="100" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="10">20B</text>
  <!-- 빈 10B -->
  <rect x="326" y="62" width="26" height="50" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="339" y="92" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="9">10B</text>
  <!-- F 50B -->
  <rect x="352" y="62" width="78" height="50" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="391" y="83" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">F</text>
  <text x="391" y="100" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">50B</text>
  <!-- 빈 40B -->
  <rect x="430" y="62" width="104" height="50" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="482" y="83" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">빈</text>
  <text x="482" y="100" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="10">40B</text>
  <!-- H 30B -->
  <rect x="534" y="62" width="52" height="50" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="560" y="83" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">H</text>
  <text x="560" y="100" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">30B</text>
  <!-- 빈 20B -->
  <rect x="586" y="62" width="52" height="50" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="612" y="83" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">빈</text>
  <text x="612" y="100" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="10">20B</text>
  <!-- J 10B -->
  <rect x="638" y="62" width="26" height="50" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="651" y="92" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="10">J</text>
  <!-- Stats -->
  <text x="350" y="145" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="13">빈 공간 합계: <tspan fill="#ff6b6b">30+20+10+40+20 = 120B</tspan></text>
  <text x="350" y="168" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="13">연속된 최대 빈 공간: <tspan fill="#ffd700">40B</tspan></text>
  <!-- Conclusion -->
  <rect x="120" y="190" width="460" height="100" rx="8" fill="#1a1f1e" stroke="#333" stroke-width="1.5"/>
  <text x="350" y="218" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 50B 객체를 할당하려면 연속된 50B가 필요</text>
  <text x="350" y="244" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 빈 공간이 120B나 있는데도 할당 실패</text>
  <text x="350" y="270" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 힙을 확장해야 함</text>
</svg>

<br>

반면 .NET GC는 압축을 수행하여 살아있는 객체를 한쪽으로 밀어 넣으므로, 빈 공간이 항상 연속으로 존재합니다.

Boehm GC에서는 단편화 때문에 빈 공간의 총합이 충분해도 연속된 빈 블록이 부족하면 새 객체를 할당할 수 없어, 힙이 실제 필요량보다 더 커지게 됩니다.

<br>

한 번 확장된 힙은 다시 줄어들지 않습니다.

GC가 메모리를 회수해도 힙 크기 자체는 유지되므로, GC 검사 범위도 넓은 상태로 남습니다.

예를 들어 게임 초반에 대량의 임시 객체를 할당하여 힙이 한 번 확장되면, 임시 객체가 모두 수거된 뒤에도 GC 실행 시간은 영구적으로 늘어납니다.

---

### 보수적 (Conservative)

Boehm GC는 원래 C/C++용으로 설계된 범용 GC로, 타입 정보 없이도 동작합니다.

타입 정보가 없으면 메모리의 어떤 값이 객체를 가리키는 포인터인지, 단순 정수인지 구분할 수 없습니다.

<br>

특히 **스택과 레지스터**에서 이 문제가 드러납니다.

스택의 지역 변수나 레지스터에는 포인터뿐 아니라 해시 코드, 연산 중간값 같은 정수도 저장됩니다.

보수적 GC는 이 슬롯들의 타입 정보가 없으므로, 저장된 정수값이 우연히 힙에 존재하는 객체의 주소와 일치하면, 그것을 포인터로 간주하고 해당 객체를 살아있는 것으로 취급합니다.

이것이 **보수적(Conservative)**이라는 이름의 유래입니다.

<br>

다만 Unity의 Mono는 Boehm GC에 타입 디스크립터를 제공하여, **힙 객체의 필드**는 정확하게 스캔합니다. 객체의 어떤 필드가 참조이고 어떤 필드가 정수인지 타입 정보로 구분할 수 있기 때문입니다.

그러나 **스택과 레지스터**에는 여전히 타입 정보가 없어 보수적으로 스캔하며, 거짓 참조는 주로 여기서 발생합니다.

<br>

<svg viewBox="0 0 700 390" xmlns="http://www.w3.org/2000/svg" aria-label="보수적 GC의 거짓 참조: 스택의 정수값이 힙 주소와 우연히 일치하여 죽은 객체를 살아있다고 판단하는 상황" style="width:100%;max-width:700px;display:block;margin:0 auto">
  <defs>
    <marker id="m11-g" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
    <marker id="m11-r" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#ff6b6b"/></marker>
  </defs>
  <text x="350" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">보수적 GC의 거짓 참조</text>
  <!-- Stack -->
  <text x="130" y="55" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="14">스택</text>
  <rect x="30" y="65" width="200" height="42" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="130" y="82" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="11">변수 a = 0x0040A000</text>
  <text x="130" y="100" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="10">실제 객체 참조</text>
  <rect x="30" y="107" width="200" height="42" fill="#1a1f1e" stroke="#555" stroke-width="1.5"/>
  <text x="130" y="124" text-anchor="middle" fill="#555" font-family="monospace" font-size="11">변수 b = 42</text>
  <text x="130" y="142" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="10">정수값</text>
  <rect x="30" y="149" width="200" height="42" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2"/>
  <text x="130" y="166" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="11">변수 c = 0x0040B200</text>
  <text x="130" y="184" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="10">정수값이지만 힙 주소 범위</text>
  <!-- Heap -->
  <text x="520" y="55" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="14">힙</text>
  <!-- Object X -->
  <rect x="420" y="68" width="200" height="50" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="460" y="88" fill="#888" font-family="monospace" font-size="10">0x0040A000</text>
  <text x="520" y="108" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">객체 X</text>
  <!-- Object Y -->
  <rect x="420" y="140" width="200" height="50" rx="6" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="2"/>
  <text x="460" y="160" fill="#888" font-family="monospace" font-size="10">0x0040B200</text>
  <text x="520" y="180" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">객체 Y</text>
  <!-- Arrow: a → X (solid green) -->
  <line x1="230" y1="86" x2="410" y2="86" stroke="#73f38f" stroke-width="2" marker-end="url(#m11-g)"/>
  <text x="320" y="78" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="10">정상 참조</text>
  <!-- Arrow: c → Y (dashed red) -->
  <line x1="230" y1="170" x2="410" y2="165" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#m11-r)"/>
  <text x="320" y="185" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="10">거짓 참조!</text>
  <!-- Status labels -->
  <text x="640" y="98" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="11">살아있음 ✓</text>
  <text x="640" y="170" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">살아있음?!</text>
  <!-- Explanation -->
  <rect x="60" y="225" width="580" height="80" rx="8" fill="#1a1f1e" stroke="#333" stroke-width="1.5"/>
  <text x="350" y="252" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">객체 Y는 아무도 사용하지 않지만,</text>
  <text x="350" y="272" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">스택의 정수값 0x0040B200이 우연히 Y의 주소와 일치하여</text>
  <text x="350" y="292" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">GC가 Y를 살아있다고 판단함</text>
  <!-- Legend -->
  <line x1="170" y1="335" x2="220" y2="335" stroke="#73f38f" stroke-width="2"/>
  <text x="230" y="339" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">정상 참조</text>
  <line x1="340" y1="335" x2="390" y2="335" stroke="#ff6b6b" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="400" y="339" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">거짓 참조 (정수값이 주소와 일치)</text>
</svg>

<br>

이런 **거짓 참조(False Reference)**로 인해 실제로는 죽은 객체가 수거되지 않을 수 있습니다.

거짓 참조가 많이 발생하면 힙에 쓰레기가 쌓여 힙 크기가 불필요하게 커지고, 비세대 GC 특성과 맞물려 GC 실행 시간도 함께 늘어납니다.

<br>

반면 .NET GC는 **정확한(Precise)** GC입니다.

.NET 런타임은 JIT 컴파일 시점에 각 스택 프레임의 타입 정보(GC Info)를 생성하므로, 스택의 어떤 슬롯이 객체 참조이고 어떤 슬롯이 정수인지 정확히 구분할 수 있습니다.

거짓 참조가 발생하지 않으며, 객체를 안전하게 이동(압축)할 수 있는 것도 이 정확한 참조 추적 덕분입니다.

---

### .NET GC와 Boehm GC 비교

| 특성 | .NET GC (데스크톱/서버) | Boehm GC (Unity) |
|------|------------------------|------------------|
| 세대 구분 | Gen 0/1/2 | 없음 (전체 검사) |
| 압축 | 수행 (단편화 없음) | 안 함 (단편화) |
| 참조 정확도 | 정확 (Precise) | 스택: 보수적 / 힙: 부분 정확 |
| Gen 0 수집 속도 | 빠름 | 해당 없음 |
| 힙 크기와 GC 시간 | 세대별 분리 | 비례 증가 |
| 힙 축소 | 가능 | 불가능 |

<br>

Boehm GC가 Unity에 남아 있는 이유는 역사적 배경에 있습니다.

Unity가 Mono 런타임을 채택한 초기(Unity 1.x, 2005년경)에 Boehm GC가 함께 포함되었고, 이후 엔진의 네이티브 코드, 직렬화 시스템, 스크립팅 바인딩 등 많은 부분이 이 GC 위에서 구축되었습니다.

.NET의 세대별 GC로 교체하려면 이 의존 관계 전체를 재설계해야 합니다.

Unity는 이 교체를 장기 목표로 두고 있지만, 현재까지는 Boehm GC가 유지되고 있습니다.

---

## Stop-the-World와 GC 스파이크

Boehm GC의 비세대, 비압축, 보수적 특성은 GC 한 번의 실행 비용을 높입니다.

이 비용은 실제 게임에서 Stop-the-World와 GC 스파이크라는 형태로 나타납니다.

### Stop-the-World

**Stop-the-World**는 GC가 실행되는 동안 모든 C# 스크립트 실행을 중단시키는 동작입니다.

힙을 검사하는 도중에 스크립트가 객체를 생성하거나 참조를 변경하면 Mark 결과가 부정확해질 수 있으므로, GC는 검사가 끝날 때까지 스크립트 실행을 멈춥니다.

<br>

<svg viewBox="0 0 700 340" xmlns="http://www.w3.org/2000/svg" aria-label="Stop-the-World의 프레임 영향: GC로 인해 프레임 예산을 초과하는 상황" style="width:100%;max-width:700px;display:block;margin:0 auto">
  <text x="350" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">Stop-the-World의 프레임 영향</text>
  <!-- Normal frame -->
  <text x="40" y="58" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">정상 프레임 (GC 없음):</text>
  <!-- Total bar outline -->
  <rect x="40" y="68" width="580" height="45" rx="4" fill="none" stroke="#555" stroke-width="1"/>
  <!-- Input -->
  <rect x="40" y="68" width="18" height="45" fill="#00d4ff" opacity="0.6"/>
  <text x="49" y="95" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9" transform="rotate(-90,49,95)">입력</text>
  <!-- Logic -->
  <rect x="58" y="68" width="175" height="45" fill="#73f38f" opacity="0.3"/>
  <text x="145" y="88" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="11">로직</text>
  <text x="145" y="104" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">5ms</text>
  <!-- Render -->
  <rect x="233" y="68" width="140" height="45" fill="#00d4ff" opacity="0.25"/>
  <text x="303" y="88" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="11">렌더링 명령</text>
  <text x="303" y="104" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">4ms</text>
  <!-- Idle -->
  <rect x="373" y="68" width="247" height="45" fill="#1a1f1e" stroke="none"/>
  <text x="496" y="88" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="11">여유</text>
  <text x="496" y="104" text-anchor="middle" fill="#555" font-family="monospace" font-size="10">7ms</text>
  <!-- 16.6ms marker -->
  <line x1="620" y1="65" x2="620" y2="120" stroke="#555" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="620" y="133" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">16.6ms</text>
  <text x="620" y="146" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="10">(60fps)</text>
  <!-- GC frame -->
  <text x="40" y="185" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">GC가 발생한 프레임:</text>
  <!-- Input -->
  <rect x="40" y="195" width="14" height="45" fill="#00d4ff" opacity="0.6"/>
  <!-- Logic -->
  <rect x="54" y="195" width="130" height="45" fill="#73f38f" opacity="0.3"/>
  <text x="119" y="215" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="11">로직</text>
  <text x="119" y="231" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">5ms</text>
  <!-- GC STW -->
  <rect x="184" y="195" width="390" height="45" rx="2" fill="#ff6b6b" opacity="0.3" stroke="#ff6b6b" stroke-width="2"/>
  <text x="379" y="215" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12" font-weight="bold">GC (Stop-the-World)</text>
  <text x="379" y="231" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="10">15ms</text>
  <!-- Render -->
  <rect x="574" y="195" width="104" height="45" fill="#00d4ff" opacity="0.25"/>
  <text x="626" y="215" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="10">렌더링</text>
  <text x="626" y="231" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">4ms</text>
  <!-- 16.6ms marker -->
  <line x1="620" y1="192" x2="620" y2="248" stroke="#555" stroke-width="1" stroke-dasharray="3,2"/>
  <!-- Total -->
  <line x1="40" y1="252" x2="678" y2="252" stroke="#ff6b6b" stroke-width="1"/>
  <text x="678" y="270" text-anchor="end" fill="#ff6b6b" font-family="monospace" font-size="11">24.5ms</text>
  <!-- Exceed labels -->
  <text x="350" y="300" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 프레임 예산 초과</text>
  <text x="350" y="322" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">→ 프레임 드롭</text>
</svg>

<br>

위 다이어그램에서 볼 수 있듯이, GC의 Stop-the-World 시간은 해당 프레임의 로직·렌더링 시간에 그대로 합산됩니다.

합산된 시간이 프레임 예산을 넘으면 해당 프레임의 화면 갱신이 늦어지고, 플레이어는 끊김(스터터링)을 체감합니다.

---

### GC 스파이크

**GC 스파이크(GC Spike)**는 GC로 인해 특정 프레임의 시간이 급격히 치솟는 현상입니다.

Unity Profiler에서 확인하면, 평소 10~15ms 수준이던 프레임 시간이 GC가 발생한 프레임에서 25~50ms까지 솟구칩니다.

<br>

<svg viewBox="0 0 640 320" xmlns="http://www.w3.org/2000/svg" aria-label="Profiler에서 본 GC 스파이크: 특정 프레임에서 GC로 인해 프레임 시간이 급증하는 현상" style="width:100%;max-width:640px;display:block;margin:0 auto">
  <text x="320" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">Profiler에서 본 GC 스파이크 (개념적)</text>
  <!-- Y axis -->
  <text x="22" y="55" fill="#888" font-family="monospace" font-size="10">50</text>
  <text x="22" y="95" fill="#888" font-family="monospace" font-size="10">40</text>
  <text x="22" y="135" fill="#888" font-family="monospace" font-size="10">30</text>
  <text x="22" y="175" fill="#888" font-family="monospace" font-size="10">20</text>
  <text x="22" y="195" fill="#ffd700" font-family="monospace" font-size="10">16</text>
  <text x="22" y="215" fill="#888" font-family="monospace" font-size="10">10</text>
  <text x="28" y="255" fill="#888" font-family="monospace" font-size="10">0</text>
  <line x1="42" y1="45" x2="42" y2="255" stroke="#555" stroke-width="1.5"/>
  <!-- X axis -->
  <line x1="42" y1="255" x2="610" y2="255" stroke="#555" stroke-width="1.5"/>
  <text x="326" y="280" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">프레임</text>
  <!-- Y axis label -->
  <text x="12" y="150" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="10" transform="rotate(-90,12,150)">프레임 시간 (ms)</text>
  <!-- 60fps baseline -->
  <line x1="42" y1="191" x2="610" y2="191" stroke="#ffd700" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="610" y="186" text-anchor="end" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="10">60fps 기준선 (16.6ms)</text>
  <!-- Normal bars (12 frames, bar at ~15ms = y:195 to y:255, height 60) -->
  <rect x="60" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="100" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="140" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="180" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="220" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="260" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="300" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="340" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <!-- GC SPIKE bar (~50ms = from y:55 to y:255, height 200) -->
  <rect x="380" y="55" width="30" height="200" rx="2" fill="#ff6b6b" opacity="0.8"/>
  <!-- Normal bars after spike -->
  <rect x="420" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="460" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <rect x="500" y="195" width="30" height="60" rx="2" fill="#73f38f" opacity="0.6"/>
  <!-- Spike annotation -->
  <line x1="395" y1="48" x2="395" y2="38" stroke="#ff6b6b" stroke-width="1"/>
  <text x="395" y="32" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">GC 스파이크</text>
  <!-- Labels -->
  <text x="200" y="300" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">정상</text>
  <text x="395" y="300" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">↑ GC</text>
  <text x="465" y="300" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">정상</text>
</svg>

<br>

GC 스파이크의 크기는 **힙 크기**와 **살아있는 객체의 참조 구조**에 따라 달라집니다.

비세대인 Boehm GC는 매번 힙 전체를 검사하므로, 힙에 객체가 많을수록 Mark 단계에서 검사할 대상이 늘어나 GC 시간이 길어집니다.

객체 간 참조가 복잡하게 얽혀 있으면 참조 그래프를 탐색하는 시간도 함께 증가합니다.

<br>

모바일 기기에서는 CPU 성능이 데스크톱보다 낮으므로, 같은 크기의 힙에서도 GC 시간이 더 깁니다. 데스크톱에서 5ms인 GC가 모바일에서는 15~20ms로 나타날 수도 있습니다.

---

## Incremental GC

GC 스파이크로 인한 프레임 드롭을 완화하기 위해 Unity는 2019.1부터 **Incremental GC(점진적 GC)**를 도입했습니다.

### GC 작업의 분산

기본 모드에서는 GC가 시작되면 한 프레임 안에 Mark-and-Sweep 전체를 완료해야 합니다.

Incremental GC는 같은 작업을 여러 프레임에 나누어 조금씩 수행합니다.

<br>

<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" aria-label="기존 GC vs Incremental GC: 단일 프레임 집중 처리 vs 여러 프레임 분산 처리 비교" style="width:100%;max-width:720px;display:block;margin:0 auto">
  <text x="360" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">기존 GC vs Incremental GC</text>
  <!-- === Non-incremental === -->
  <text x="40" y="55" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="13">기존 GC (Non-incremental):</text>
  <!-- 16.6ms marker line -->
  <line x1="40" y1="115" x2="690" y2="115" stroke="#ffd700" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="690" y="112" text-anchor="end" fill="#ffd700" font-family="monospace" font-size="9" opacity="0.7">16.6ms</text>
  <!-- Frame 1: normal 12ms -->
  <rect x="40" y="68" width="90" height="45" rx="3" fill="#73f38f" opacity="0.3" stroke="#73f38f" stroke-width="1"/>
  <text x="85" y="88" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="10">정상</text>
  <text x="85" y="104" text-anchor="middle" fill="#888" font-family="monospace" font-size="9">12ms</text>
  <!-- Frame 2: Logic 5ms + GC 20ms = 25ms (exceeds) -->
  <rect x="140" y="68" width="38" height="45" rx="3" fill="#73f38f" opacity="0.3"/>
  <text x="159" y="95" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9">로직</text>
  <rect x="178" y="68" width="152" height="45" rx="3" fill="#ff6b6b" opacity="0.35" stroke="#ff6b6b" stroke-width="2"/>
  <text x="254" y="88" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="10">GC (Stop-the-World)</text>
  <text x="254" y="104" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="9">20ms</text>
  <!-- Frame 2 total -->
  <line x1="140" y1="120" x2="330" y2="120" stroke="#ff6b6b" stroke-width="1"/>
  <text x="235" y="137" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="10">25ms → 프레임 드롭!</text>
  <!-- Frame 3 & 4: normal -->
  <rect x="340" y="68" width="90" height="45" rx="3" fill="#73f38f" opacity="0.3" stroke="#73f38f" stroke-width="1"/>
  <text x="385" y="88" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="10">정상</text>
  <text x="385" y="104" text-anchor="middle" fill="#888" font-family="monospace" font-size="9">12ms</text>
  <rect x="440" y="68" width="90" height="45" rx="3" fill="#73f38f" opacity="0.3" stroke="#73f38f" stroke-width="1"/>
  <text x="485" y="88" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="10">정상</text>
  <text x="485" y="104" text-anchor="middle" fill="#888" font-family="monospace" font-size="9">12ms</text>
  <!-- Frame labels -->
  <text x="85" y="64" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 1</text>
  <text x="235" y="64" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 2</text>
  <text x="385" y="64" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 3</text>
  <text x="485" y="64" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 4</text>
  <!-- === Incremental === -->
  <text x="40" y="185" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">Incremental GC:</text>
  <!-- 16.6ms marker line -->
  <line x1="40" y1="248" x2="690" y2="248" stroke="#ffd700" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="690" y="245" text-anchor="end" fill="#ffd700" font-family="monospace" font-size="9" opacity="0.7">16.6ms</text>
  <!-- Frame 1 -->
  <rect x="40" y="200" width="75" height="45" rx="3" fill="#73f38f" opacity="0.3"/>
  <rect x="115" y="200" width="37" height="45" rx="3" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="1"/>
  <text x="77" y="220" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9">게임</text>
  <text x="133" y="220" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="9">GC</text>
  <text x="96" y="236" text-anchor="middle" fill="#888" font-family="monospace" font-size="8">10+5ms</text>
  <!-- Frame 2 -->
  <rect x="162" y="200" width="75" height="45" rx="3" fill="#73f38f" opacity="0.3"/>
  <rect x="237" y="200" width="37" height="45" rx="3" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="1"/>
  <text x="199" y="220" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9">게임</text>
  <text x="255" y="220" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="9">GC</text>
  <text x="218" y="236" text-anchor="middle" fill="#888" font-family="monospace" font-size="8">10+5ms</text>
  <!-- Frame 3 -->
  <rect x="284" y="200" width="75" height="45" rx="3" fill="#73f38f" opacity="0.3"/>
  <rect x="359" y="200" width="37" height="45" rx="3" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="1"/>
  <text x="321" y="220" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9">게임</text>
  <text x="377" y="220" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="9">GC</text>
  <text x="340" y="236" text-anchor="middle" fill="#888" font-family="monospace" font-size="8">10+5ms</text>
  <!-- Frame 4 -->
  <rect x="406" y="200" width="75" height="45" rx="3" fill="#73f38f" opacity="0.3"/>
  <rect x="481" y="200" width="37" height="45" rx="3" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="1"/>
  <text x="443" y="220" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9">게임</text>
  <text x="499" y="220" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="9">GC</text>
  <text x="462" y="236" text-anchor="middle" fill="#888" font-family="monospace" font-size="8">10+5ms</text>
  <!-- Frame 5 -->
  <rect x="528" y="200" width="75" height="45" rx="3" fill="#73f38f" opacity="0.3"/>
  <rect x="603" y="200" width="45" height="45" rx="3" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="1"/>
  <text x="565" y="220" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="9">게임</text>
  <text x="625" y="220" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="9">GC</text>
  <text x="587" y="236" text-anchor="middle" fill="#888" font-family="monospace" font-size="8">10+6ms</text>
  <!-- Frame labels -->
  <text x="96" y="196" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 1</text>
  <text x="218" y="196" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 2</text>
  <text x="340" y="196" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 3</text>
  <text x="462" y="196" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 4</text>
  <text x="587" y="196" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="9">프레임 5</text>
  <!-- Per-frame totals -->
  <text x="96" y="260" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="9">15ms</text>
  <text x="218" y="260" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="9">15ms</text>
  <text x="340" y="260" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="9">15ms</text>
  <text x="462" y="260" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="9">15ms</text>
  <text x="587" y="260" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="9">16ms</text>
  <text x="360" y="280" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="11">(모두 예산 이내)</text>
  <!-- Summary -->
  <rect x="120" y="300" width="480" height="55" rx="8" fill="#1a1f1e" stroke="#333" stroke-width="1.5"/>
  <text x="360" y="322" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">GC 총 작업량: <tspan fill="#ffd700">~26ms</tspan></text>
  <text x="360" y="342" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">(쓰기 장벽 오버헤드로 원래 20ms보다 증가)</text>
  <!-- Legend -->
  <rect x="190" y="375" width="14" height="14" rx="2" fill="#73f38f" opacity="0.3"/>
  <text x="210" y="387" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">게임 로직</text>
  <rect x="300" y="375" width="14" height="14" rx="2" fill="#ffd700" opacity="0.25" stroke="#ffd700" stroke-width="1"/>
  <text x="320" y="387" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">GC 작업</text>
  <rect x="410" y="375" width="14" height="14" rx="2" fill="#ff6b6b" opacity="0.35" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="430" y="387" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">Stop-the-World</text>
</svg>

<br>

쓰기 장벽 오버헤드 때문에 GC 총 작업량은 약간 늘어나지만, 여러 프레임에 나누어 처리하므로 프레임당 GC 비용이 작아집니다. 각 프레임이 예산 이내에 머물면 끊김이 사라집니다.

---

### 쓰기 장벽 (Write Barrier)

GC 작업을 여러 프레임에 나누면 문제가 하나 생깁니다.

GC가 객체 A를 검사하고 다음 프레임으로 넘어간 사이에, 스크립트가 `A.child = newObject`처럼 참조를 변경할 수 있습니다.

GC는 A를 이미 검사했으므로 newObject의 존재를 모르고, 도달 불가능으로 판단하여 잘못 수거할 수 있습니다.

<br>

Incremental GC는 이 문제를 **쓰기 장벽(Write Barrier)**으로 해결합니다.

스크립트가 참조 필드를 변경할 때마다, 런타임이 "이 객체의 참조가 변경되었다"는 기록을 남깁니다.

GC가 다음 프레임에서 작업을 재개할 때, 이 기록을 참조하여 변경된 부분을 다시 검사합니다.

<br>

<svg viewBox="0 0 680 420" xmlns="http://www.w3.org/2000/svg" aria-label="쓰기 장벽의 동작: GC가 중단된 사이에 참조가 변경되면 쓰기 장벽이 변경을 기록하여 다음 GC 재개 시 재검사하는 과정" style="width:100%;max-width:680px;display:block;margin:0 auto">
  <defs>
    <marker id="m16-a" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#f9fffb"/></marker>
  </defs>
  <text x="340" y="25" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="16" font-weight="bold">쓰기 장벽의 동작</text>
  <!-- Phase 1: 프레임 N -->
  <rect x="30" y="45" width="620" height="110" rx="8" fill="#1a1f1e" stroke="#ffd700" stroke-width="1.5"/>
  <text x="50" y="68" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">프레임 N</text>
  <rect x="50" y="80" width="12" height="12" rx="2" fill="#73f38f"/>
  <text x="70" y="92" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">GC가 객체 A를 검사 완료 (Mark: 도달 가능)</text>
  <rect x="50" y="102" width="12" height="12" rx="2" fill="#73f38f"/>
  <text x="70" y="114" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">GC가 객체 B까지 검사 완료</text>
  <text x="70" y="142" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">→ 프레임 시간 소진, GC 일시 중단</text>
  <!-- Arrow down -->
  <line x1="340" y1="155" x2="340" y2="175" stroke="#f9fffb" stroke-width="1.5" marker-end="url(#m16-a)"/>
  <!-- Phase 2: 스크립트 실행 -->
  <rect x="30" y="183" width="620" height="95" rx="8" fill="#1a1f1e" stroke="#00d4ff" stroke-width="1.5"/>
  <text x="50" y="206" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">스크립트 실행</text>
  <rect x="50" y="218" width="380" height="26" rx="4" fill="#2a1a1a" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="60" y="236" fill="#ff6b6b" font-family="monospace" font-size="12">A.child = newObject;</text>
  <text x="310" y="236" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">← 참조 변경 발생!</text>
  <rect x="50" y="250" width="300" height="20" rx="4" fill="#ffd700" opacity="0.15"/>
  <text x="60" y="265" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="12">쓰기 장벽이 변경을 기록</text>
  <!-- Arrow down -->
  <line x1="340" y1="278" x2="340" y2="298" stroke="#f9fffb" stroke-width="1.5" marker-end="url(#m16-a)"/>
  <!-- Phase 3: 프레임 N+1 -->
  <rect x="30" y="306" width="620" height="105" rx="8" fill="#1a1f1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="50" y="329" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">프레임 N+1</text>
  <text x="70" y="349" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">GC 재개</text>
  <text x="70" y="369" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="12">기록된 변경사항 확인: "A의 참조가 변경됨"</text>
  <text x="70" y="389" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="12">A를 다시 검사하여 newObject도 Mark</text>
  <text x="70" y="406" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">→ 살아있는 객체가 잘못 수거되는 것을 방지</text>
</svg>

<br>

쓰기 장벽은 모든 참조 필드 변경마다 기록 작업을 수행하므로, 참조 변경이 빈번한 코드에서는 오버헤드가 누적됩니다.

앞서 다이어그램에서 총 GC 시간이 20ms에서 ~26ms로 증가한 부분이 이 쓰기 장벽 비용에 대한 예시입니다.

---

### Incremental GC의 한계

Incremental GC는 스파이크를 완화하는 수단이지 근본적인 해결책이 아닙니다.

<br>

<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg" aria-label="Incremental GC의 효과와 한계: 스파이크 완화 효과와 총 GC 시간 증가 등의 한계" style="width:100%;max-width:620px;display:block;margin:0 auto">
  <text x="310" y="28" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">Incremental GC의 효과와 한계</text>
  <!-- 효과 -->
  <rect x="15" y="45" width="285" height="215" rx="8" fill="#1a1f1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="157" y="70" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">효과</text>
  <text x="35" y="96" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">· 단일 프레임의 GC 스파이크 크기 감소</text>
  <text x="35" y="120" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">· 프레임 드롭 빈도 감소</text>
  <text x="35" y="144" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">· 플레이어가 체감하는 끊김 완화</text>
  <!-- 한계 -->
  <rect x="320" y="45" width="285" height="215" rx="8" fill="#1a1f1e" stroke="#ff6b6b" stroke-width="1.5"/>
  <text x="462" y="70" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="14" font-weight="bold">한계</text>
  <text x="340" y="98" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">· 총 GC 시간은 같거나 약간 증가</text>
  <text x="348" y="114" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">(쓰기 장벽 오버헤드)</text>
  <text x="340" y="142" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">· 매 프레임 2~3ms의 GC 비용이</text>
  <text x="348" y="158" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">지속 발생</text>
  <text x="340" y="186" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">· 할당 속도 > 해제 속도이면</text>
  <text x="348" y="202" fill="#ccc" font-family="'Noto Sans KR',sans-serif" font-size="12">결국 큰 스파이크 발생</text>
  <text x="340" y="230" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">· 힙 할당 자체를 줄이지 않으면</text>
  <text x="348" y="246" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="12">근본 해결 안 됨</text>
  <!-- 하단 결론 -->
  <rect x="100" y="265" width="420" height="35" rx="6" fill="#1a1f1e" stroke="#ffd700" stroke-width="1"/>
  <text x="310" y="288" text-anchor="middle" fill="#ffd700" font-family="'Noto Sans KR',sans-serif" font-size="12">스파이크 완화 수단이지 근본적 해결책이 아님</text>
</svg>

<br>

Incremental GC는 GC가 발생했을 때의 영향을 줄일 뿐, GC 발생 자체를 막지는 않습니다.

힙 할당이 계속되면 GC도 계속 실행됩니다.

예를 들어 `Update()`에서 매 프레임 `new string()`이나 `new List<>()`를 호출하면, Incremental GC가 활성화되어 있어도 GC 비용이 매 프레임 누적되어 결국 큰 스파이크가 재발합니다.

<br>

GC 문제의 근본 해결은 힙 할당 자체를 줄이는 것입니다.

Incremental GC는 할당을 최소화한 뒤에도 남는 불가피한 GC 비용을 분산하는 보조 수단입니다.

---

### Incremental GC 활성화

Unity 에디터에서 **Project Settings > Player > Other Settings > Configuration** 항목의 **Use Incremental GC** 체크박스로 활성화합니다. Unity 2019.3 이후 버전에서는 기본으로 활성화되어 있습니다.

<br>

Incremental GC는 Boehm GC 위에서 동작합니다.

세대별 GC로 바뀌는 것이 아니라, 기존 Boehm GC의 Mark-and-Sweep을 프레임 간에 나누어 실행하는 방식입니다.

비세대, 비압축, 보수적이라는 Boehm GC의 근본 특성은 변하지 않습니다.

---

## GC.Collect()와 프로파일링

`System.GC.Collect()`를 호출하면, Unity의 Boehm GC는 즉시 전체 힙을 대상으로 Mark-and-Sweep을 실행합니다.

비세대 GC이므로 세대를 지정하는 인자는 무시되고, 항상 전체 힙을 검사합니다.

<br>

호출 시 Stop-the-World가 발생하므로, 게임플레이 중에는 사용하지 않는 것이 원칙입니다.

씬 로딩이나 페이드 아웃처럼 플레이어가 끊김을 인지하지 못하는 시점에 호출하여 힙을 정리하는 용도로 활용합니다.

<br>

힙 할당이 어디에서 얼마나 발생하는지는 Unity Profiler로 파악합니다.

CPU 모듈의 `GC.Alloc` 마커를 확인하면, 매 프레임 어떤 메서드가 얼마만큼의 힙 할당을 일으키는지 추적할 수 있습니다.

GC 스파이크를 줄이는 첫 단계는 이 마커로 할당 지점을 찾아 할당 자체를 제거하거나 줄이는 것입니다.

---

## 마무리

GC는 메모리의 자동 회수를 통해 수동 관리의 위험(메모리 누수, 댕글링 포인터, 이중 해제)을 제거하지만, 실행 비용이 프레임 시간에 직접 영향을 줍니다. Unity의 Boehm GC는 비세대, 비압축, 보수적이라는 특성 때문에 .NET의 세대별 GC보다 이 비용이 높습니다.

- Mark-and-Sweep은 GC 루트(스택 변수, 정적 필드)에서 참조 그래프를 따라 도달 가능한 객체를 표시하고, 표시되지 않은 객체를 해제합니다.
- .NET의 세대별 GC는 힙을 Gen 0/1/2로 나누어, 짧은 수명의 객체가 모인 Gen 0만 자주 검사합니다.
- Unity의 Boehm GC는 비세대(매번 전체 힙 검사), 비압축(단편화 발생), 보수적(거짓 참조 가능)이라 .NET GC보다 비용이 높습니다.
- GC 실행 중 모든 스크립트가 멈추는 Stop-the-World가 프레임 예산을 초과하면 GC 스파이크로 이어집니다.
- Incremental GC는 GC 작업을 여러 프레임에 분산하여 스파이크를 완화하지만, 총 GC 시간은 같거나 약간 늘어납니다.
- `GC.Collect()`는 씬 전환 등 끊김이 허용되는 시점에 호출하여 힙을 정리합니다.
- Unity Profiler의 `GC.Alloc` 마커로 힙 할당 지점을 파악하는 것이 최적화의 출발점입니다.
- GC 문제의 근본 해결은 힙 할당 자체를 줄이는 것입니다.

<br>

이 글에서 다룬 GC의 원리는 실전에서 힙 할당을 줄이는 기법의 기초가 됩니다. [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서 Unity 프로젝트에서의 GC 비용 측정과 할당 패턴 제거를 다루고, [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서 숨은 힙 할당 패턴과 오브젝트 풀링을 다룹니다. 다음 글인 [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)에서는 C# 런타임의 멀티스레딩과 비동기 프로그래밍을 다룹니다.

<br>

---

**관련 글**
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)

**시리즈**
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
- **C# 런타임 기초 (3) - 가비지 컬렉션의 기초 (현재 글)**
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)

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
- **C# 런타임 기초 (3) - 가비지 컬렉션의 기초** (현재 글)
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)
- [게임 물리 (1) - 강체 역학의 원리](/dev/unity/GamePhysics-1/)
- [게임 물리 (2) - 충돌 검출의 원리](/dev/unity/GamePhysics-2/)
- [게임 물리 (3) - 제약 조건과 솔버](/dev/unity/GamePhysics-3/)
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
