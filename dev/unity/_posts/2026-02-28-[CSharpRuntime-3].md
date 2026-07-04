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

[C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서는 C# 코드가 IL을 거쳐 기계어로 바뀌는 과정을 살펴봤습니다. 런타임이 맡는 또 하나의 핵심 역할은 다 쓴 메모리를 회수하는 일입니다.

C#에서 `new`로 참조 타입 객체를 만들면 런타임은 관리 힙에 메모리를 할당합니다. 이후 그 객체에 더 이상 도달할 수 없게 되면 **가비지 컬렉터(Garbage Collector, GC)**가 해당 메모리를 회수합니다.

GC 덕분에 개발자는 메모리를 직접 해제하지 않아도 됩니다. 그 대신 런타임이 회수할 객체를 찾아 정리해야 하며, Unity에서는 이 작업이 프레임 시간에 영향을 줄 수 있습니다. 특히 GC가 동작하는 동안에는 C# 코드 실행이 잠시 멈추므로, 프레임 드롭이나 스파이크로 이어질 수 있습니다.

이 글에서는 GC가 왜 필요한지, Mark-and-Sweep 알고리즘이 객체를 어떻게 찾고 회수하는지, Unity의 Boehm GC와 Incremental GC가 게임 성능에 어떤 영향을 주는지 차례로 살펴봅니다.

---

## GC의 필요성

프로그램이 할당한 메모리는 언젠가 해제되어야 합니다. 메모리는 한정된 자원이라, 다 쓴 객체가 계속 남아 있으면 새로 할당할 공간이 줄어들기 때문입니다.

문제는 어떤 객체를 더 이상 쓰지 않는지, 그래서 언제 메모리를 돌려줄지를 누가 판단하느냐입니다. 개발자가 코드에서 직접 해제하는 방법도 있고, 런타임이 대신 판단하도록 맡기는 방법도 있습니다. 먼저 직접 관리하는 방식의 위험을 살펴본 뒤, GC가 그 일을 어떻게 대신하는지 다룹니다.

### 수동 메모리 관리의 위험

C나 C++에서는 메모리를 언제 해제할지 개발자가 직접 정합니다. `malloc()`이나 `new`로 확보한 메모리는 더 쓰지 않는 순간 `free()`나 `delete`로 직접 돌려줘야 합니다.

이 방식은 제어가 정확한 대신, 어떤 메모리를 언제 돌려줄지를 사람이 일일이 따라가야 합니다. 그 판단은 두 방향으로 어긋날 수 있습니다. 해제할 메모리를 끝내 그대로 두면, 그리고 아직 살아 있는 메모리를 너무 일찍 해제하면 문제가 생깁니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <rect x="0" y="0" width="640" height="300" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="320" y="32" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">해제 시점 판단이 어긋나는 두 방향</text>
  <!-- root -->
  <rect x="240" y="50" width="160" height="38" rx="6" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="320" y="74" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">해제 책임이 흐려진다</text>
  <!-- connectors -->
  <path d="M320 88 V104 M160 104 H480 M160 104 V128 M480 104 V128 M160 168 V190 M480 168 V190" fill="none" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <!-- 왼쪽: 해제 안 함 -->
  <rect x="40" y="128" width="240" height="40" rx="6" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="160" y="153" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">① 다 쓴 메모리를 해제하지 않는다</text>
  <text fill="currentColor" x="160" y="206" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">메모리 누수</text>
  <text fill="currentColor" x="160" y="228" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">안 쓰는 메모리가 남아 사용량이 늘어남</text>
  <text fill="currentColor" x="160" y="247" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">(C#도 참조가 남으면 회수 불가)</text>
  <!-- 오른쪽: 너무 일찍 해제 -->
  <rect x="360" y="128" width="240" height="40" rx="6" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="480" y="153" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">② 살아 있는 메모리를 일찍 해제한다</text>
  <text fill="currentColor" x="480" y="206" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">댕글링 포인터 · 이중 해제</text>
  <text fill="currentColor" x="480" y="228" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">해제된 자리 접근 → 잘못된 값·충돌</text>
  <text fill="currentColor" x="480" y="247" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">두 번 해제 → 할당자 구조 손상</text>
</svg>
</div>

<br>

첫 번째는 **메모리 누수(Memory Leak)**입니다. 다 쓴 메모리를 제때 해제하지 않으면, 그 영역은 프로그램이 도는 동안 계속 남고 실행이 길어질수록 쓰지도 않는 메모리가 늘어 사용량이 올라갑니다.

특히 모바일은 메모리 여유가 제한적이라, 누수가 계속되면 그 영향이 더 빨리 나타납니다. 사용량이 한계에 다가가면 OS가 앱을 강제로 종료하거나, 그 전부터 앱 반응이 느려지기도 합니다.

이런 누수는 C# 환경에서도 예외가 아닙니다. 관리 힙에 있는 객체라도 어딘가에 참조가 남아 있으면 GC가 회수하지 못하므로, 더 쓰지 않는 객체의 참조를 놓지 않으면 논리적 누수로 이어집니다.

두 번째 방향은 반대로, 아직 쓰고 있는 메모리를 너무 일찍 해제할 때 생깁니다. 그 대표적인 경우가 **댕글링 포인터(Dangling Pointer)**입니다. 이미 해제한 메모리를 가리키는 포인터가 그대로 남고, 그 자리가 다른 데이터로 재사용된 뒤 포인터로 접근하면 엉뚱한 값을 읽거나 프로그램이 충돌할 수 있습니다.

게다가 이런 충돌은 메모리 상태에 따라 나타났다 사라졌다 하므로, 원인을 추적하기가 까다롭습니다.

같은 방향에서 한 단계 더 나아간 실수가 **이중 해제(Double Free)**입니다. 이미 해제한 메모리를 다시 해제하면, 할당자가 빈 영역을 추적하려고 유지하는 내부 자료구조가 어긋나면서 그 뒤의 동작을 예측하기 어렵게 됩니다.

두 방향 모두 해제 책임이 흐려질수록 잦아집니다. 어느 코드가 객체를 해제할지 분명하지 않으면, 한쪽은 상대가 해제할 거라 여기며 미루다 누수를 남기고, 다른 쪽은 아직 쓰이는 메모리를 먼저 해제해 댕글링 포인터를 만듭니다.

결국 수동 관리가 안전하려면, 개발자가 모든 객체의 수명을 빠짐없이 직접 추적해야 합니다. 그런데 소유권이 여러 코드에 걸칠수록 이 추적은 점점 어려워집니다. 그래서 C#은 해제 시점을 정하는 일을 사람이 아니라 런타임에 넘깁니다.

---

### GC의 역할

GC는 메모리 해제 책임을 개발자 대신 런타임이 맡도록 만든 장치입니다. 개발자는 객체를 생성하고 사용하며, 회수 시점은 GC가 판단합니다.

기준은 도달 가능성입니다. 어떤 객체에 도달할 수 있는 참조가 더 이상 없으면, GC는 그 객체를 회수 가능한 대상으로 봅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text fill="currentColor" x="310" y="26" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">수동 관리 vs 자동 관리 (GC)</text>
  <!-- 수동 -->
  <rect x="15" y="44" width="285" height="112" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="157" y="68" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">수동 (C/C++)</text>
  <text fill="currentColor" x="30" y="92" font-size="12" font-family="sans-serif" opacity="0.8">개발자가 할당 → 개발자가 해제</text>
  <text fill="currentColor" x="30" y="116" font-size="11" font-family="sans-serif" opacity="0.55">실수하면 →</text>
  <text fill="currentColor" x="30" y="138" font-size="12" font-weight="bold" font-family="sans-serif">누수 · 댕글링 포인터 · 이중 해제</text>
  <!-- 자동 -->
  <rect x="320" y="44" width="285" height="112" rx="8" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="462" y="68" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">자동 (C#, Java 등)</text>
  <text fill="currentColor" x="335" y="92" font-size="12" font-family="sans-serif" opacity="0.8">개발자가 할당 → GC가 해제</text>
  <text fill="currentColor" x="335" y="116" font-size="11" font-family="sans-serif" opacity="0.55">해제 시점을 개발자가 결정하지 않음</text>
  <text fill="currentColor" x="335" y="138" font-size="12" font-weight="bold" font-family="sans-serif">→ 댕글링 포인터 · 이중 해제 불가능</text>
  <!-- 하단 결론 -->
  <rect x="100" y="174" width="420" height="40" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="310" y="199" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">→ 메모리 누수 위험 감소 (참조만 끊으면 GC가 회수)</text>
</svg>
</div>

<br>

그래서 C#에서는 일반적으로 `free()`나 `delete`를 직접 호출하지 않습니다. 객체를 더 이상 사용하지 않게 되면 참조가 사라지고, 이후 GC가 실행될 때 해당 객체가 회수됩니다. 이 방식은 댕글링 포인터와 이중 해제 위험을 크게 줄입니다.

다만 GC가 회수할 객체를 찾아 정리하는 작업에는 CPU 시간이 듭니다. Unity에서는 이 작업이 프레임 시간에 영향을 줄 수 있습니다. 이 비용이 어디서 생기는지 이해하려면, GC가 어떤 객체를 회수할지 판단하는 방식부터 살펴봐야 합니다.

---

## Mark-and-Sweep 알고리즘

GC가 객체를 회수하려면 먼저 어떤 객체가 아직 사용 중인지 판단해야 합니다. 이 판단의 기본 기준은 **도달 가능성(Reachability)**이고, 이를 이용한 대표적인 알고리즘이 **Mark-and-Sweep**입니다.

### 도달 가능성 (Reachability)

GC는 객체가 “의미상 필요한지”를 직접 판단하지 않습니다. 대신 현재 실행 중인 프로그램에서 참조를 따라 도달할 수 있는지를 봅니다. 도달 가능한 객체는 살아 있는 객체로 보고, 어떤 경로로도 도달할 수 없는 객체는 회수 가능한 객체로 봅니다.

도달 가능성 탐색의 출발점은 **GC 루트(GC Root)**입니다. GC 루트에는 현재 실행 중인 스택 변수, 정적 필드, CPU 레지스터에 들어 있는 참조 등이 포함됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <rect x="0" y="0" width="620" height="280" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="310" y="32" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="15" font-weight="bold">GC 루트의 종류</text>
  <!-- 1. 스택 변수 -->
  <text x="30" y="68" fill="currentColor" font-family="sans-serif" font-size="14" font-weight="bold">1. 스택 변수</text>
  <text x="50" y="88" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">현재 실행 중인 메서드의 지역 변수와 매개변수</text>
  <text x="50" y="108" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.6">메서드가 실행 중인 동안 참조하는 객체</text>
  <!-- 2. 정적 필드 -->
  <text x="30" y="142" fill="currentColor" font-family="sans-serif" font-size="14" font-weight="bold">2. 정적 필드 (static field)</text>
  <text x="50" y="162" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">클래스에 속하는 필드로, 프로그램이 끝날 때까지 유지됨</text>
  <text x="50" y="182" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.6">여기에 저장된 참조는 항상 도달 가능</text>
  <!-- 3. CPU 레지스터 -->
  <text x="30" y="216" fill="currentColor" font-family="sans-serif" font-size="14" font-weight="bold">3. CPU 레지스터</text>
  <text x="50" y="236" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">현재 CPU가 처리 중인 값</text>
  <text x="50" y="256" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.6">실행 중인 코드에서 사용하는 참조가 레지스터에 있을 수 있음</text>
</svg>
</div>

<br>

GC 루트가 직접 가리키는 객체는 도달 가능합니다. 그 객체가 다시 가리키는 객체도 도달 가능합니다. GC는 이런 식으로 참조를 따라가며 살아 있는 객체 집합을 만듭니다.

이 집합에 포함되지 않은 객체는 어떤 루트에서도 도달할 수 없으므로, 프로그램이 다시 사용할 수 없습니다. 이런 객체는 회수 대상이 됩니다.

---

### Mark 단계

**Mark(표시)** 단계에서 GC는 루트에서 시작해 참조를 따라 객체 그래프를 순회합니다. 이렇게 도달한 객체는 아직 살아 있다는 뜻이므로, GC는 그 객체를 살아 있는 것으로 표시합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <defs>
    <marker id="m4-ag" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="currentColor"/></marker>
    <marker id="m4-ac" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="currentColor"/></marker>
  </defs>
  <!-- Title -->
  <text x="360" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="16" font-weight="bold">Mark 단계의 동작</text>
  <text x="360" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.6">GC 루트들</text>
  <!-- Root boxes -->
  <rect x="80" y="65" width="120" height="45" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="140" y="93" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="14">스택 변수</text>
  <rect x="300" y="65" width="120" height="45" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="360" y="93" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="14">정적 필드</text>
  <rect x="520" y="65" width="120" height="45" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="580" y="93" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="14">CPU 레지스터</text>
  <!-- Root arrows -->
  <line x1="140" y1="110" x2="140" y2="165" stroke="currentColor" stroke-width="2" marker-end="url(#m4-ac)"/>
  <line x1="360" y1="110" x2="360" y2="165" stroke="currentColor" stroke-width="2" marker-end="url(#m4-ac)"/>
  <line x1="580" y1="110" x2="580" y2="165" stroke="currentColor" stroke-width="2" marker-end="url(#m4-ac)"/>
  <!-- Row 1: reachable objects -->
  <rect x="90" y="175" width="100" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="130" y="200" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13">객체 A</text>
  <text x="195" y="195" fill="currentColor" font-family="monospace" font-size="13">✓</text>
  <rect x="310" y="175" width="100" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="350" y="200" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13">객체 D</text>
  <text x="415" y="195" fill="currentColor" font-family="monospace" font-size="13">✓</text>
  <rect x="530" y="175" width="100" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="570" y="200" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13">객체 F</text>
  <text x="635" y="195" fill="currentColor" font-family="monospace" font-size="13">✓</text>
  <!-- Arrows from A to B and E -->
  <path d="M140 215 L140 250 L220 250 L220 275" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#m4-ag)"/>
  <path d="M155 215 L155 240 L440 240 L440 275" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#m4-ag)"/>
  <!-- Row 2: B and E -->
  <rect x="170" y="285" width="100" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="210" y="310" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13">객체 B</text>
  <text x="275" y="305" fill="currentColor" font-family="monospace" font-size="13">✓</text>
  <rect x="390" y="285" width="100" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="430" y="310" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13">객체 E</text>
  <text x="495" y="305" fill="currentColor" font-family="monospace" font-size="13">✓</text>
  <!-- Arrow from B to C -->
  <path d="M220 325 L220 355 L310 355 L310 375" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#m4-ag)"/>
  <!-- Row 3: C -->
  <rect x="260" y="385" width="100" height="40" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="300" y="410" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13">객체 C</text>
  <text x="365" y="405" fill="currentColor" font-family="monospace" font-size="13">✓</text>
  <!-- Unreachable objects -->
  <text x="600" y="300" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.45">표시되지 않은 객체들</text>
  <text x="600" y="316" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.45">(도달 불가)</text>
  <rect x="530" y="330" width="80" height="35" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.45"/>
  <text x="570" y="352" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" opacity="0.45">객체 G</text>
  <rect x="625" y="330" width="80" height="35" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.45"/>
  <text x="665" y="352" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" opacity="0.45">객체 H</text>
  <rect x="578" y="378" width="80" height="35" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.45"/>
  <text x="618" y="400" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" opacity="0.45">객체 I</text>
</svg>
</div>

<br>

세부 순회 방식은 구현마다 다르지만, 루트에서 시작해 참조를 따라간다는 기본 골격은 어디서나 같습니다.

순회가 끝나면, 표시가 남은 객체는 그대로 살아남습니다. 반대로 표시가 없는 객체는 어떤 루트에서도 도달할 수 없으므로, 이어지는 Sweep 단계에서 회수됩니다.

---

### Sweep 단계

**Sweep(소거)** 단계에서는 힙을 훑으며 Mark 표시가 없는 객체를 회수합니다. 표시된 객체는 유지하고, 표시되지 않은 객체의 공간은 다시 사용할 수 있는 빈 공간으로 돌립니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <text x="360" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="16" font-weight="bold">Sweep 단계의 동작</text>
  <!-- Mark 후 label -->
  <text x="40" y="65" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.6">Mark 후:</text>
  <!-- Mark 후 cells -->
  <rect x="40" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="65" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">A ✓</text>
  <rect x="110" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="135" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">B ✓</text>
  <rect x="180" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="2" opacity="0.45"/>
  <text x="205" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" opacity="0.45">G</text>
  <rect x="250" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="275" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">C ✓</text>
  <rect x="320" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="2" opacity="0.45"/>
  <text x="345" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" opacity="0.45">H</text>
  <rect x="390" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="415" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">D ✓</text>
  <rect x="460" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="485" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">E ✓</text>
  <rect x="530" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="2" opacity="0.45"/>
  <text x="555" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" opacity="0.45">I</text>
  <rect x="600" y="75" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="625" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">F ✓</text>
  <!-- Sweep 후 label -->
  <text x="40" y="155" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.6">Sweep 후:</text>
  <!-- Sweep 후 cells -->
  <rect x="40" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="65" y="188" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">A ✓</text>
  <rect x="110" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="135" y="188" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">B ✓</text>
  <rect x="180" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="2" stroke-dasharray="5,3" opacity="0.5"/>
  <text x="205" y="188" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.5">빈</text>
  <rect x="250" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="275" y="188" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">C ✓</text>
  <rect x="320" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="2" stroke-dasharray="5,3" opacity="0.5"/>
  <text x="345" y="188" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.5">빈</text>
  <rect x="390" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="415" y="188" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">D ✓</text>
  <rect x="460" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="485" y="188" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">E ✓</text>
  <rect x="530" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="2" stroke-dasharray="5,3" opacity="0.5"/>
  <text x="555" y="188" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.5">빈</text>
  <rect x="600" y="165" width="70" height="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="625" y="188" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12">F ✓</text>
  <!-- 해제됨 arrows -->
  <line x1="215" y1="205" x2="215" y2="225" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <text x="215" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.6">해제됨</text>
  <line x1="355" y1="205" x2="355" y2="225" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <text x="355" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.6">해제됨</text>
  <line x1="565" y1="205" x2="565" y2="225" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <text x="565" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.6">해제됨</text>
  <!-- Legend -->
  <rect x="200" y="265" width="14" height="14" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="277" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.6">살아있음</text>
  <rect x="310" y="265" width="14" height="14" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="330" y="277" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.6">해제됨 (새 할당에 사용 가능)</text>
</svg>
</div>

<br>

Sweep이 끝나면 살아남은 객체만 힙에 남고, 회수된 자리는 이후 새 할당에 다시 쓸 수 있게 됩니다. 이렇게 Mark-and-Sweep은 살아 있는 객체를 가려내는 Mark 단계와, 나머지를 회수하는 Sweep 단계로 일을 나눕니다.

객체가 살아 있는지 판단하는 기준은 도달 가능성 하나만이 아닙니다. 더 직관적인 방법으로, 객체마다 자신을 가리키는 참조가 몇 개인지 세어 둘 수도 있습니다. 이 방식이 **참조 카운팅(Reference Counting)**입니다. 어떤 객체의 참조 수가 0이 되면, 런타임이 그 객체를 곧바로 해제합니다.

문제는 참조 수가 0이 되지 않는 경우입니다. **순환 참조(Circular Reference)**가 그렇습니다. A가 B를 가리키고 B가 다시 A를 가리키면, 바깥의 어떤 루트에서도 둘에 도달할 수 없게 된 뒤에도 서로를 향한 참조가 남아 참조 수가 0으로 내려가지 않고, 두 객체는 죽은 채 메모리에 남습니다.

Mark-and-Sweep은 참조 수가 아니라 루트에서 도달 가능한지를 봅니다. 따라서 순환 참조가 있어도 루트에서 닿지 않으면 회수 대상으로 판단할 수 있습니다.

---

## 세대별 GC (Generational GC)

기본 Mark-and-Sweep은 GC가 돌 때마다 힙 전체를 훑습니다. Mark 단계에서 루트부터 살아 있는 객체를 따라가고, Sweep 단계에서 힙에 놓인 객체를 차례로 확인해 표시되지 않은 것을 해제하기 때문입니다. 그래서 힙이 커질수록 한 번의 GC에 걸리는 시간이 길어집니다.

데스크톱과 서버를 겨냥한 .NET 런타임은 이 부담을 줄이려고 **세대별 GC(Generational GC)**를 씁니다. 힙 전체를 같은 빈도로 훑지 않고, 금방 사라지는 객체가 모인 영역은 자주, 오래 살아남은 객체가 모인 영역은 드물게 검사합니다.

### 세대 가설

세대별 GC는 **세대 가설(Generational Hypothesis)**을 바탕으로 합니다. 객체의 수명에는 반복해서 나타나는 두 가지 경향이 있는데, 이를 이용하면 한 번에 검사할 양을 줄일 수 있습니다.

첫째, **대부분의 객체는 수명이 짧습니다**. 임시 문자열, 루프 안에서 만들어지는 중간 결과, 메서드 안에서만 쓰이는 객체가 그렇습니다. 이런 객체는 생성된 뒤 금방 쓸모가 없어집니다.

둘째, **오래 살아남은 객체는 이후에도 계속 살아남는 경향이 있습니다**. 캐시나 설정 데이터, 게임이 실행되는 동안 유지되는 매니저 객체가 그렇습니다. 초기에 만들어진 뒤로 프로그램이 끝날 때까지 남아 있곤 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <defs>
    <marker id="gen-hypothesis-arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="currentColor"/>
    </marker>
  </defs>

  <text fill="currentColor" x="340" y="24" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">세대 가설이 수집 범위를 줄이는 방식</text>

  <!-- Stage 1: allocation burst -->
  <rect x="28" y="58" width="170" height="110" rx="7" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text fill="currentColor" x="113" y="82" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">새 객체 할당</text>
  <text fill="currentColor" x="113" y="103" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">짧은 계산 중 많이 생성</text>
  <rect x="48" y="122" width="44" height="22" rx="11" fill="currentColor" fill-opacity="0.10"/>
  <text fill="currentColor" x="70" y="137" text-anchor="middle" font-size="10" font-family="sans-serif">문자열</text>
  <rect x="98" y="122" width="52" height="22" rx="11" fill="currentColor" fill-opacity="0.10"/>
  <text fill="currentColor" x="124" y="137" text-anchor="middle" font-size="10" font-family="sans-serif">임시 배열</text>
  <rect x="63" y="146" width="70" height="22" rx="11" fill="currentColor" fill-opacity="0.10"/>
  <text fill="currentColor" x="98" y="161" text-anchor="middle" font-size="10" font-family="sans-serif">중간 결과</text>

  <!-- Arrow to Gen 0 collection -->
  <line x1="198" y1="113" x2="248" y2="113" stroke="currentColor" stroke-width="1.5" marker-end="url(#gen-hypothesis-arrow)"/>
  <text fill="currentColor" x="223" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">할당 영역이 참</text>

  <!-- Stage 2: Gen 0 collection -->
  <rect x="252" y="58" width="176" height="110" rx="7" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text fill="currentColor" x="340" y="82" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Gen 0 수집</text>
  <text fill="currentColor" x="340" y="104" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">최근 생성 객체만 먼저 검사</text>
  <line x1="284" y1="130" x2="396" y2="130" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="302" y="151" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.65">죽음</text>
  <text fill="currentColor" x="378" y="151" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.65">생존</text>

  <!-- Branch to collected -->
  <path d="M300 168 V216 H142 V242" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#gen-hypothesis-arrow)"/>
  <rect x="52" y="244" width="180" height="70" rx="7" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3"/>
  <text fill="currentColor" x="142" y="268" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">참조가 끊긴 객체</text>
  <text fill="currentColor" x="142" y="289" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">첫 수집에서 바로 회수</text>
  <text fill="currentColor" x="142" y="306" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">짧게 쓰인 임시 객체</text>

  <!-- Branch to promotion -->
  <path d="M380 168 V216 H538 V242" fill="none" stroke="currentColor" stroke-width="1.5" marker-end="url(#gen-hypothesis-arrow)"/>
  <rect x="448" y="244" width="180" height="70" rx="7" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="538" y="268" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">살아남은 객체</text>
  <text fill="currentColor" x="538" y="289" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">높은 세대로 승격</text>
  <text fill="currentColor" x="538" y="306" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">캐시 · 매니저 · 설정 데이터</text>

  <!-- Result band -->
  <rect x="250" y="244" width="180" height="70" rx="7" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="340" y="268" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">수집 전략</text>
  <text fill="currentColor" x="340" y="289" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">Gen 0은 자주 검사</text>
  <text fill="currentColor" x="340" y="306" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">오래 산 세대는 드물게 검사</text>

  <text fill="currentColor" x="340" y="342" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">핵심은 정확한 통계 그래프가 아니라 첫 수집에서 나뉘는 흐름임</text>
  <text fill="currentColor" x="340" y="358" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">바로 죽는 객체는 빨리 회수하고, 계속 살아남는 객체는 높은 세대로 보냄</text>
</svg>
</div>

<br>

그래서 GC가 모든 객체를 같은 빈도로 검사할 이유는 없습니다. 새로 만들어진 객체는 대부분 금방 쓸모가 없어지므로, 이들이 모인 영역만 자주 검사해도 그 대부분을 회수할 수 있기 때문입니다. 반면 여러 번 살아남은 객체는 다음에도 남을 가능성이 크니, 자주 확인하지 않아도 됩니다.

---

### Gen 0, Gen 1, Gen 2

.NET의 세대별 GC는 객체를 나이에 따라 다른 빈도로 검사하려고, 관리 힙을 **Gen 0, Gen 1, Gen 2** 세 영역으로 나눕니다. 여기서 객체의 나이는 GC가 돌 때마다 살아남은 횟수를 뜻합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <text fill="currentColor" x="350" y="25" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">.NET의 세대별 힙 구조</text>
  <!-- Outer: 관리 힙 -->
  <rect x="20" y="40" width="660" height="230" rx="8" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="350" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.55">관리 힙</text>
  <!-- Gen 0 -->
  <rect x="40" y="75" width="130" height="180" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="105" y="98" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold">Gen 0</text>
  <text fill="currentColor" x="105" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">새 객체</text>
  <text fill="currentColor" x="105" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">할당</text>
  <line x1="55" y1="155" x2="155" y2="155" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="105" y="174" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">크기: 작음</text>
  <line x1="55" y1="185" x2="155" y2="185" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="105" y="204" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">수집: 자주</text>
  <rect x="55" y="218" width="100" height="22" rx="4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="105" y="234" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">빈도 높음</text>
  <!-- Gen 1 -->
  <rect x="190" y="75" width="180" height="180" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="280" y="98" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold">Gen 1</text>
  <text fill="currentColor" x="280" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">Gen 0에서</text>
  <text fill="currentColor" x="280" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">살아남은 객체</text>
  <line x1="205" y1="155" x2="355" y2="155" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="280" y="174" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">크기: 중간</text>
  <line x1="205" y1="185" x2="355" y2="185" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="280" y="204" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">수집: 가끔</text>
  <rect x="215" y="218" width="130" height="22" rx="4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="280" y="234" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">빈도 중간</text>
  <!-- Gen 2 -->
  <rect x="390" y="75" width="270" height="180" rx="6" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="525" y="98" text-anchor="middle" font-family="monospace" font-size="14" font-weight="bold">Gen 2</text>
  <text fill="currentColor" x="525" y="122" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">Gen 1에서</text>
  <text fill="currentColor" x="525" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">살아남은 객체 (장기 생존)</text>
  <line x1="405" y1="155" x2="645" y2="155" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="525" y="174" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">크기: 큼</text>
  <line x1="405" y1="185" x2="645" y2="185" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="525" y="204" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">수집: 드물게</text>
  <rect x="430" y="218" width="190" height="22" rx="4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="525" y="234" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">빈도 낮음 (Full GC)</text>
</svg>
</div>

<br>

**Gen 0**은 새로 할당된 객체가 처음 들어가는 세대입니다. 영역이 작고 GC가 가장 자주 검사하므로, 짧게 쓰이고 사라지는 객체 대부분은 여기서 회수됩니다. Gen 0 수집에서 살아남은 객체는 **Gen 1**로 이동하며, 이렇게 객체를 높은 세대로 옮기는 일을 **승격(Promotion)**이라고 합니다.

**Gen 1**은 Gen 0 수집에서 살아남은 객체가 머무는 중간 세대입니다. 한 번 살아남은 객체는 더 오래 쓰일 가능성이 있으므로, GC는 Gen 1을 Gen 0보다 덜 자주 검사합니다. Gen 1 수집에서도 살아남은 객체는 **Gen 2**로 승격됩니다.

**Gen 2**는 오래 유지되는 객체가 머무는 세대입니다. 세 세대 중 가장 드물게 수집되지만, Gen 2 수집은 아래 세대까지 함께 검사하는 **Full GC**가 되므로 한 번 실행될 때의 비용은 가장 큽니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <defs>
    <marker id="m8-a" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="currentColor"/></marker>
  </defs>
  <text fill="currentColor" x="340" y="25" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">세대별 GC의 수집 흐름</text>
  <!-- 새 객체 생성 -->
  <rect x="70" y="45" width="150" height="36" rx="18" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="145" y="68" text-anchor="middle" font-size="13" font-family="sans-serif">새 객체 생성</text>
  <line x1="145" y1="81" x2="145" y2="100" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Gen 0에 할당 -->
  <rect x="70" y="108" width="150" height="36" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="145" y="131" text-anchor="middle" font-size="13" font-family="sans-serif">Gen 0에 할당</text>
  <!-- trigger -->
  <text fill="currentColor" x="240" y="162" font-size="11" font-family="sans-serif" opacity="0.55">Gen 0이 가득 참</text>
  <line x1="145" y1="144" x2="145" y2="170" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Gen 0 수집 -->
  <rect x="50" y="178" width="190" height="36" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="145" y="198" text-anchor="middle" font-size="12" font-family="sans-serif">Gen 0 수집 실행</text>
  <text fill="currentColor" x="145" y="210" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(빠름, 범위 작음)</text>
  <!-- Branch: dead -->
  <line x1="100" y1="214" x2="100" y2="242" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <text fill="currentColor" x="100" y="262" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">죽은 객체 → 해제</text>
  <!-- Branch: survive to Gen 1 -->
  <line x1="195" y1="214" x2="195" y2="232" stroke="currentColor" stroke-width="1.5"/>
  <line x1="195" y1="232" x2="350" y2="232" stroke="currentColor" stroke-width="1.5"/>
  <line x1="350" y1="232" x2="350" y2="252" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <text fill="currentColor" x="273" y="226" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">살아남은 객체</text>
  <!-- Gen 1로 승격 -->
  <rect x="280" y="260" width="140" height="32" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="350" y="281" text-anchor="middle" font-size="13" font-family="sans-serif">Gen 1로 승격</text>
  <!-- trigger -->
  <text fill="currentColor" x="440" y="312" font-size="11" font-family="sans-serif" opacity="0.55">Gen 1이 가득 참</text>
  <line x1="350" y1="292" x2="350" y2="320" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Gen 1 수집 -->
  <rect x="265" y="328" width="170" height="32" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="350" y="349" text-anchor="middle" font-size="12" font-family="sans-serif">Gen 1 수집 실행</text>
  <!-- Branch: dead -->
  <line x1="310" y1="360" x2="310" y2="388" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <text fill="currentColor" x="310" y="408" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">죽은 객체 → 해제</text>
  <!-- Branch: survive to Gen 2 -->
  <line x1="400" y1="360" x2="400" y2="378" stroke="currentColor" stroke-width="1.5"/>
  <line x1="400" y1="378" x2="540" y2="378" stroke="currentColor" stroke-width="1.5"/>
  <line x1="540" y1="378" x2="540" y2="398" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <text fill="currentColor" x="470" y="372" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">살아남은 객체</text>
  <!-- Gen 2로 승격 -->
  <rect x="470" y="406" width="140" height="32" rx="6" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="540" y="427" text-anchor="middle" font-size="13" font-family="sans-serif">Gen 2로 승격</text>
  <!-- trigger -->
  <text fill="currentColor" x="540" y="460" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">Gen 2 수집은 드물게 실행</text>
  <line x1="540" y1="438" x2="540" y2="468" stroke="currentColor" stroke-width="1.5" marker-end="url(#m8-a)"/>
  <!-- Full GC -->
  <rect x="470" y="476" width="140" height="32" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="540" y="497" text-anchor="middle" font-size="13" font-family="sans-serif">Full GC (비용 높음)</text>
</svg>
</div>

<br>

이렇게 세대를 나누면, 짧게 쓰이는 객체가 모이는 Gen 0은 범위가 작아 자주 수집해도 부담이 적습니다. 객체 대부분이 여기서 회수되므로, 힙 전체를 훑는 비싼 Full GC는 오래된 객체가 어느 정도 모인 뒤에야 가끔 실행됩니다.

.NET의 세대별 GC는 수집을 마친 뒤 **압축(Compaction)**도 수행할 수 있습니다. 살아남은 객체를 힙의 한쪽으로 모아 두면, 그 사이에 흩어져 있던 빈 공간이 반대쪽에 연속된 한 덩어리로 남습니다.

빈 공간이 이렇게 한 덩어리로 모이면, 새 객체에 필요한 자리를 잡기가 쉬워집니다. 작은 빈틈이 힙 곳곳에 흩어져 막상 쓰기는 어려운 상태, 즉 **메모리 단편화(Memory Fragmentation)**도 이 과정에서 줄어듭니다.

---

## Unity의 Boehm GC

앞 절에서 본 세대별 GC는 일반적인 .NET 런타임에 해당합니다. Unity의 Mono 런타임은 이 방식 대신 **Boehm GC(Boehm-Demers-Weiser Garbage Collector)**라는 다른 수집기를 씁니다.

Boehm GC는 .NET의 세대별 GC와 세 가지 점에서 다릅니다.
세대를 나누지 않아 수집할 때마다 힙 전체를 검사하고(**비세대**, Non-generational), 수집한 뒤에도 살아남은 객체를 그대로 두며(**비압축**, Non-compacting), 일부 메모리 값이 실제 참조인지 일반 정수인지 정확히 구분하지 못합니다(**보수적**, Conservative).

이 세 특성 때문에 Unity에서는 GC 비용이 더 커집니다. 각각이 어떤 비용으로 이어지는지 차례로 살펴봅니다.

### 비세대 (Non-generational)

Boehm GC와 .NET GC의 첫 번째 차이는 힙을 세대로 나누는지 여부입니다. Boehm GC는 세대를 나누지 않으므로, .NET GC처럼 Gen 0만 따로 검사하는 부분 수집을 할 수 없습니다.

따라서 GC가 한 번 실행될 때마다 힙 전체가 검사 대상이 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <text x="340" y="25" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="16" font-weight="bold">.NET GC vs Boehm GC: 수집 범위</text>
  <!-- .NET GC -->
  <text x="40" y="58" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">.NET GC (세대별):</text>
  <rect x="40" y="68" width="130" height="50" rx="4" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>
  <text x="105" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13" font-weight="bold">Gen 0</text>
  <rect x="170" y="68" width="180" height="50" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <text x="260" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13" opacity="0.5">Gen 1</text>
  <rect x="350" y="68" width="290" height="50" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <text x="495" y="98" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="13" opacity="0.5">Gen 2</text>
  <!-- highlight bracket for Gen 0 -->
  <line x1="45" y1="126" x2="45" y2="136" stroke="currentColor" stroke-width="2"/>
  <line x1="45" y1="136" x2="165" y2="136" stroke="currentColor" stroke-width="2"/>
  <line x1="165" y1="126" x2="165" y2="136" stroke="currentColor" stroke-width="2"/>
  <text x="105" y="154" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.8">← 검사 →</text>
  <text x="105" y="170" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.55">Gen 0 수집: 여기만 검사 (빠름)</text>
  <!-- Boehm GC -->
  <text x="40" y="202" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">Boehm GC (비세대):</text>
  <rect x="40" y="212" width="600" height="50" rx="4" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>
  <text x="340" y="242" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">전체 힙</text>
  <!-- full scan bracket -->
  <line x1="45" y1="270" x2="45" y2="280" stroke="currentColor" stroke-width="2"/>
  <line x1="45" y1="280" x2="635" y2="280" stroke="currentColor" stroke-width="2"/>
  <line x1="635" y1="270" x2="635" y2="280" stroke="currentColor" stroke-width="2"/>
  <text x="340" y="296" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.55">매번 전부 검사 (힙이 클수록 느림)</text>
</svg>
</div>

<br>

예를 들어 객체 1000개 중 990개가 이미 오래 살아남은 것이라도, Boehm GC는 매 수집마다 1000개를 전부 검사합니다. 오래된 객체를 따로 두고 덜 자주 검사하는 구조가 없기 때문입니다.
그래서 힙에 객체가 많을수록 한 번의 수집에서 살펴야 할 양도 그만큼 커지고, 수집 시간이 길어집니다. 특히 좀처럼 사라지지 않는 오래된 객체가 늘어날수록, 매 수집이 점점 무거워집니다.

### 비압축 (Non-compacting)

두 번째 차이는 수집을 마친 뒤 살아남은 객체를 옮기는지 여부입니다. .NET GC는 압축으로 이들을 힙 한쪽에 모으지만, Boehm GC는 Sweep을 끝낸 뒤에도 객체를 원래 자리에 그대로 둡니다.

그래서 죽은 객체가 비운 자리가 살아남은 객체 사이사이에 빈틈으로 남습니다. 객체를 한데 모으는 단계가 없는 Boehm GC에서는 이런 단편화가 수집을 거듭할수록 심해집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <text x="350" y="25" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="16" font-weight="bold">비압축 GC의 단편화</text>
  <text x="40" y="52" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.55">Sweep 후:</text>
  <!-- Memory cells - widths proportional to byte sizes -->
  <!-- A 20B (live) -->
  <rect x="40" y="62" width="52" height="50" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="66" y="83" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" font-weight="bold">A</text>
  <text x="66" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.55">20B</text>
  <!-- 빈 30B -->
  <rect x="92" y="62" width="78" height="50" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="131" y="83" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.6">빈</text>
  <text x="131" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.6">30B</text>
  <!-- C 40B (live) -->
  <rect x="170" y="62" width="104" height="50" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="222" y="83" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" font-weight="bold">C</text>
  <text x="222" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.55">40B</text>
  <!-- 빈 20B -->
  <rect x="274" y="62" width="52" height="50" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="300" y="83" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.6">빈</text>
  <text x="300" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.6">20B</text>
  <!-- 빈 10B -->
  <rect x="326" y="62" width="26" height="50" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="339" y="92" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="9" opacity="0.6">10B</text>
  <!-- F 50B (live) -->
  <rect x="352" y="62" width="78" height="50" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="391" y="83" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" font-weight="bold">F</text>
  <text x="391" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.55">50B</text>
  <!-- 빈 40B -->
  <rect x="430" y="62" width="104" height="50" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="482" y="83" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.6">빈</text>
  <text x="482" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.6">40B</text>
  <!-- H 30B (live) -->
  <rect x="534" y="62" width="52" height="50" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="560" y="83" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="12" font-weight="bold">H</text>
  <text x="560" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.55">30B</text>
  <!-- 빈 20B -->
  <rect x="586" y="62" width="52" height="50" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.6"/>
  <text x="612" y="83" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.6">빈</text>
  <text x="612" y="100" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" opacity="0.6">20B</text>
  <!-- J 10B (live) -->
  <rect x="638" y="62" width="26" height="50" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="651" y="92" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="10" font-weight="bold">J</text>
  <!-- Stats -->
  <text x="350" y="145" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13">빈 공간 합계: <tspan font-weight="bold">30+20+10+40+20 = 120B</tspan></text>
  <text x="350" y="168" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13">연속된 최대 빈 공간: <tspan font-weight="bold">40B</tspan></text>
  <!-- Conclusion -->
  <rect x="120" y="190" width="460" height="100" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="350" y="218" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">→ 50B 객체를 할당하려면 연속된 50B가 필요</text>
  <text x="350" y="244" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">→ 빈 공간이 120B나 있는데도 할당 실패</text>
  <text x="350" y="270" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" opacity="0.8">→ 힙을 확장해야 함</text>
</svg>
</div>

<br>

그림처럼 빈자리가 잘게 조각나면, 전체 여유는 넉넉해도 새 객체를 들이지 못할 수 있습니다. 흩어진 빈자리를 모두 합치면 120B나 되지만 연속된 자리는 가장 큰 것이 40B뿐이라, 50B짜리 객체를 놓을 자리가 없습니다. 객체를 옮기지 않는 Boehm GC에서는 빈 공간의 총량보다 연속된 한 덩어리의 크기가 중요해지고, 결국 힙은 실제 사용량보다 더 커집니다.

게다가 한 번 커진 힙은 좀처럼 다시 줄지 않습니다. GC가 죽은 객체를 회수해도 힙이 확보해 둔 전체 크기는 그대로 남고, 그만큼 Boehm GC가 매번 훑어야 하는 범위도 넓은 채로 유지됩니다.

예를 들어 게임 초반 로딩에서 임시 객체가 많이 생겨 힙이 한 번 커졌다면, 그 객체들이 나중에 회수되어도 GC가 훑는 범위는 넓어진 채로 남습니다.

### 보수적 (Conservative)

세 번째 차이는 메모리에 놓인 값이 실제 객체 참조인지 판별하는 정확도입니다. Boehm GC는 C와 C++ 같은 환경에서도 사용할 수 있도록 만들어진 범용 수집기라, 모든 위치에 정확한 타입 정보가 없어도 동작하도록 설계되어 있습니다.

문제는 타입 정보가 없으면 어떤 값이 객체 주소를 담은 참조인지, 단순한 정수값인지 확실히 구분할 수 없다는 점입니다.

이 한계는 **스택과 레지스터**에서 특히 중요합니다. 스택의 지역 변수와 레지스터에는 객체 참조뿐 아니라 해시 코드, 계산 중간값, 인덱스 같은 일반 정수도 함께 들어갈 수 있기 때문입니다.

보수적 GC는 이런 값이 참조인지 정수인지 확실하지 않을 때 안전한 쪽으로 판단합니다. 어떤 정수값이 우연히 힙 객체의 주소 범위와 맞으면, GC는 그 값을 참조일 가능성이 있다고 보고 해당 객체를 살아 있는 객체로 취급합니다. 이처럼 애매한 값을 버리지 않고 보수적으로 살려 두기 때문에 **보수적(Conservative)** GC라고 부릅니다.

다만 Unity의 Mono가 모든 영역을 똑같이 보수적으로 훑는 것은 아닙니다. **힙 객체의 필드**에 대해서는 타입 디스크립터를 사용해 어느 필드가 참조이고 어느 필드가 값인지 더 정확하게 알 수 있습니다.

반면 **스택과 레지스터**는 여전히 보수적으로 검사해야 하며, 여기서 잘못 살아남는 객체가 생길 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <defs>
    <marker id="m11-g" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="currentColor"/></marker>
    <marker id="m11-r" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="currentColor"/></marker>
  </defs>
  <text x="350" y="25" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="16" font-weight="bold">보수적 GC의 거짓 참조</text>
  <!-- Stack -->
  <text x="130" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="14" opacity="0.8">스택</text>
  <rect x="30" y="65" width="200" height="42" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="130" y="82" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="11">변수 a = 0x0040A000</text>
  <text x="130" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">실제 객체 참조</text>
  <rect x="30" y="107" width="200" height="42" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.5" opacity="0.55"/>
  <text x="130" y="124" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="11" opacity="0.55">변수 b = 42</text>
  <text x="130" y="142" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">정수값</text>
  <rect x="30" y="149" width="200" height="42" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="130" y="166" text-anchor="middle" fill="currentColor" font-family="monospace" font-size="11">변수 c = 0x0040B200</text>
  <text x="130" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.7">정수값이지만 힙 주소 범위</text>
  <!-- Heap -->
  <text x="520" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="14" opacity="0.8">힙</text>
  <!-- Object X -->
  <rect x="420" y="68" width="200" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="460" y="88" fill="currentColor" font-family="monospace" font-size="10" opacity="0.55">0x0040A000</text>
  <text x="520" y="108" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">객체 X</text>
  <!-- Object Y -->
  <rect x="420" y="140" width="200" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="460" y="160" fill="currentColor" font-family="monospace" font-size="10" opacity="0.55">0x0040B200</text>
  <text x="520" y="180" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">객체 Y</text>
  <!-- Arrow: a → X (solid, 정상 참조) -->
  <line x1="230" y1="86" x2="410" y2="86" stroke="currentColor" stroke-width="2" marker-end="url(#m11-g)"/>
  <text x="320" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.8">정상 참조</text>
  <!-- Arrow: c → Y (dashed, 거짓 참조) -->
  <line x1="230" y1="170" x2="410" y2="165" stroke="currentColor" stroke-width="2" stroke-dasharray="6,4" marker-end="url(#m11-r)"/>
  <text x="320" y="185" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">거짓 참조!</text>
  <!-- Status labels -->
  <text x="640" y="98" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.8">살아있음 ✓</text>
  <text x="640" y="170" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">살아있음?!</text>
  <!-- Explanation -->
  <rect x="60" y="225" width="580" height="80" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="350" y="252" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.8">객체 Y는 아무도 사용하지 않지만,</text>
  <text x="350" y="272" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" opacity="0.8">스택의 정수값 0x0040B200이 우연히 Y의 주소와 일치하여</text>
  <text x="350" y="292" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">GC가 Y를 살아있다고 판단함</text>
  <!-- Legend -->
  <line x1="170" y1="335" x2="220" y2="335" stroke="currentColor" stroke-width="2"/>
  <text x="230" y="339" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.55">정상 참조</text>
  <line x1="340" y1="335" x2="390" y2="335" stroke="currentColor" stroke-width="2" stroke-dasharray="6,4"/>
  <text x="400" y="339" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.55">거짓 참조 (정수값이 주소와 일치)</text>
</svg>
</div>

<br>

그림의 객체 Y가 그런 경우입니다. 이렇게 참조로 오인된 값을 **거짓 참조(False Reference)**라고 합니다.

거짓 참조가 생기면 회수되어야 할 객체가 힙에 남습니다. 이런 객체가 누적되면 힙 크기가 불필요하게 커지고, 비세대 방식과 맞물려 GC가 전체 힙을 검사하는 시간도 길어집니다.

반면 .NET GC는 참조 위치를 정확히 아는 **정확한(Precise)** GC입니다. .NET 런타임은 실행 코드와 함께 GC가 참고할 타입 정보(GC Info)를 유지하므로, 스택의 어느 위치가 객체 참조이고 어느 위치가 일반 값인지 구분할 수 있습니다.

이 정보가 있으면 정수를 참조로 잘못 판단할 가능성이 줄어듭니다. 또한 살아남은 객체를 옮기는 압축을 수행하려면 모든 참조를 새 주소로 갱신해야 하므로, 정확한 참조 정보가 필요합니다.

---

### .NET GC와 Boehm GC 비교

| 특성 | .NET GC (데스크톱/서버) | Boehm GC (Unity) |
|------|------------------------|------------------|
| 세대 구분 | Gen 0/1/2 | 없음 (전체 검사) |
| 압축 | 수행 (단편화 없음) | 안 함 (단편화) |
| 참조 정확도 | 정확 (Precise) | 스택: 보수적 / 힙: 부분 정확 |
| Gen 0 수집 속도 | 빠름 | 해당 없음 |
| 힙 크기와 GC 시간 | 세대별 분리 | 비례 증가 |
| 힙 축소 | 가능 | 제한적 |

<br>

표에서 볼 수 있듯 Boehm GC는 Unity의 프레임 시간 관점에서 불리한 특성을 많이 가집니다. 그럼에도 Unity가 이 수집기를 오래 사용해 온 이유는 단순히 성능 선택의 문제가 아니라 런타임과 엔진 구조의 역사와 관련이 있습니다.

Unity는 초기부터 Mono 런타임을 기반으로 C# 스크립팅 환경을 구성했는데, 당시 Mono가 기본 수집기로 삼은 것이 Boehm GC였습니다. 이후 네이티브 엔진 코드, 직렬화 시스템, 스크립팅 바인딩이 이 런타임 구조와 맞물려 발전했습니다. GC를 다른 방식으로 교체하려면 단순히 수집기 하나를 바꾸는 수준이 아니라, 런타임과 엔진 사이의 여러 연결을 다시 설계해야 합니다.

따라서 Unity의 GC 비용을 이해할 때는 “왜 .NET GC처럼 동작하지 않는가”보다 “현재 Unity 런타임이 어떤 제약을 갖고 있는가”를 기준으로 보는 편이 실용적입니다.

---

## Stop-the-World와 GC 스파이크

앞서 본 비세대·비압축·보수적 특성 때문에, Boehm GC는 한 번 실행될 때마다 시간이 오래 걸립니다.

이렇게 느린 GC는 게임에서 두 가지 문제를 일으킵니다. 하나는 GC가 도는 동안 C# 코드 실행이 멈추는 **Stop-the-World**이고, 다른 하나는 그 멈춤으로 한 프레임이 유독 오래 걸리는 **GC 스파이크(GC Spike)**입니다.

### Stop-the-World

GC가 검사하는 도중에도 코드가 계속 실행되면, 새 객체가 생기거나 참조가 바뀌어 GC가 보던 객체 그래프와 실제 그래프가 어긋날 수 있습니다. 그래서 GC는 Mark와 Sweep을 도는 짧은 시간 동안 코드 실행을 멈추고, 객체 그래프를 고정한 채 검사를 끝냅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <text fill="currentColor" x="350" y="25" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">Stop-the-World의 프레임 영향</text>
  <!-- Normal frame -->
  <text fill="currentColor" x="40" y="58" font-size="12" font-family="sans-serif" opacity="0.7">정상 프레임 (GC 없음)</text>
  <!-- Total bar outline -->
  <rect x="40" y="68" width="580" height="45" rx="4" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <!-- Input -->
  <rect x="40" y="68" width="18" height="45" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <text fill="currentColor" x="49" y="95" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.7" transform="rotate(-90,49,95)">입력</text>
  <!-- Logic -->
  <rect x="58" y="68" width="175" height="45" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <text fill="currentColor" x="145" y="88" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.8">로직</text>
  <text fill="currentColor" x="145" y="104" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">5ms</text>
  <!-- Render -->
  <rect x="233" y="68" width="140" height="45" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <text fill="currentColor" x="303" y="88" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.8">렌더링 명령</text>
  <text fill="currentColor" x="303" y="104" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">4ms</text>
  <!-- Idle -->
  <rect x="373" y="68" width="247" height="45" fill="currentColor" fill-opacity="0.03"/>
  <text fill="currentColor" x="496" y="88" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.45">여유</text>
  <text fill="currentColor" x="496" y="104" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.45">7ms</text>
  <!-- 16.6ms marker -->
  <line x1="620" y1="65" x2="620" y2="120" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text fill="currentColor" x="620" y="133" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">16.6ms</text>
  <text fill="currentColor" x="620" y="146" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(60fps)</text>
  <!-- GC frame -->
  <text fill="currentColor" x="40" y="185" font-size="12" font-family="sans-serif" opacity="0.7">GC가 든 프레임</text>
  <!-- Input -->
  <rect x="40" y="195" width="14" height="45" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <!-- Logic -->
  <rect x="54" y="195" width="130" height="45" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <text fill="currentColor" x="119" y="215" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.8">로직</text>
  <text fill="currentColor" x="119" y="231" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">5ms</text>
  <!-- GC STW (강조) -->
  <rect x="184" y="195" width="390" height="45" rx="2" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="379" y="215" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">GC (Stop-the-World)</text>
  <text fill="currentColor" x="379" y="231" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.7">15ms</text>
  <!-- Render -->
  <rect x="574" y="195" width="104" height="45" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.3"/>
  <text fill="currentColor" x="626" y="215" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">렌더링</text>
  <text fill="currentColor" x="626" y="231" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">4ms</text>
  <!-- 16.6ms marker -->
  <line x1="620" y1="192" x2="620" y2="248" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <!-- Total -->
  <line x1="40" y1="252" x2="678" y2="252" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text fill="currentColor" x="678" y="270" text-anchor="end" font-size="11" font-family="monospace" font-weight="bold">24.5ms</text>
  <!-- Exceed labels -->
  <text fill="currentColor" x="350" y="300" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">→ 프레임 예산 초과</text>
  <text fill="currentColor" x="350" y="322" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">→ 프레임 드롭</text>
</svg>
</div>

<br>

게임은 매 프레임마다 입력을 처리하고, 게임 로직을 돌리고, 렌더링 명령을 만듭니다. GC가 실행되는 프레임에서는 여기에 코드가 멈춰 있던 시간이 그대로 보태집니다. 위 그림에서 5ms 로직과 4ms 렌더링이면 끝났을 프레임에 15ms GC가 더해지면, 전체 시간이 24.5ms까지 늘어납니다.

이렇게 늘어난 시간이 60fps 기준의 한 프레임 예산 16.6ms를 넘으면, 그 프레임은 제때 표시되지 못합니다. 플레이어는 이를 화면이 잠깐 끊기는 **스터터링(Stuttering)**으로 느낍니다.

---

### GC 스파이크

앞서 본 그 부푼 프레임은 Unity Profiler의 프레임 시간 그래프에서 뾰족한 막대 하나로 나타납니다. 고르게 이어지던 다른 막대들 사이에서 GC가 실행된 프레임만 유독 높이 솟기 때문입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text fill="currentColor" x="320" y="25" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">Profiler에서 본 GC 스파이크 (개념적)</text>
  <!-- Y axis -->
  <text fill="currentColor" x="22" y="55" font-size="10" font-family="monospace" opacity="0.55">50</text>
  <text fill="currentColor" x="22" y="95" font-size="10" font-family="monospace" opacity="0.55">40</text>
  <text fill="currentColor" x="22" y="135" font-size="10" font-family="monospace" opacity="0.55">30</text>
  <text fill="currentColor" x="22" y="175" font-size="10" font-family="monospace" opacity="0.55">20</text>
  <text fill="currentColor" x="22" y="195" font-size="10" font-family="monospace" font-weight="bold">16</text>
  <text fill="currentColor" x="22" y="215" font-size="10" font-family="monospace" opacity="0.55">10</text>
  <text fill="currentColor" x="28" y="255" font-size="10" font-family="monospace" opacity="0.55">0</text>
  <line x1="42" y1="45" x2="42" y2="255" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <!-- X axis -->
  <line x1="42" y1="255" x2="610" y2="255" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <text fill="currentColor" x="326" y="280" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.6">프레임</text>
  <!-- Y axis label -->
  <text fill="currentColor" x="12" y="150" font-size="10" font-family="sans-serif" opacity="0.6" transform="rotate(-90,12,150)">프레임 시간 (ms)</text>
  <!-- 60fps baseline -->
  <line x1="42" y1="191" x2="610" y2="191" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.6"/>
  <text fill="currentColor" x="610" y="186" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.7">60fps 기준선 (16.6ms)</text>
  <!-- Normal bars (~15ms = y:195 to y:255, height 60) -->
  <rect x="60" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="100" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="140" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="180" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="220" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="260" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="300" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="340" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <!-- GC SPIKE bar (~50ms = from y:55 to y:255, height 200) -->
  <rect x="380" y="55" width="30" height="200" rx="2" fill="currentColor" fill-opacity="0.8"/>
  <!-- Normal bars after spike -->
  <rect x="420" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="460" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <rect x="500" y="195" width="30" height="60" rx="2" fill="currentColor" fill-opacity="0.5"/>
  <!-- Spike annotation -->
  <line x1="395" y1="48" x2="395" y2="38" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <text fill="currentColor" x="395" y="32" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">GC 스파이크</text>
  <!-- Labels -->
  <text fill="currentColor" x="200" y="300" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">정상</text>
  <text fill="currentColor" x="395" y="300" text-anchor="middle" font-size="11" font-family="sans-serif" font-weight="bold">↑ GC</text>
  <text fill="currentColor" x="465" y="300" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">정상</text>
</svg>
</div>

<br>

스파이크의 크기는 GC 한 번이 오래 걸릴수록 커집니다. 그 시간을 정하는 것은 두 가지입니다. 하나는 GC가 처리해야 할 일의 양이고, 다른 하나는 그 일을 실행하는 기기의 속도입니다.

일의 양부터 보면, 힙이 클수록 검사할 객체가 늘어납니다. Boehm GC는 세대를 나누지 않아 매번 힙 전체를 훑으므로, 객체가 많을수록 Mark와 Sweep에 걸리는 시간이 길어집니다. 참조 구조가 복잡할 때도 마찬가지여서, 루트에서 참조를 따라가는 Mark 단계가 더 오래 걸립니다.

처리 속도는 실행 기기가 정합니다. GC는 결국 CPU가 하는 일이라, 성능이 낮거나 발열로 클럭이 떨어진 모바일에서는 같은 양을 검사해도 더 오래 걸립니다.

---

## Incremental GC

이런 GC 스파이크는 플레이 도중 프레임을 끊기게 만드는 직접적인 원인입니다. Unity는 이 스파이크를 누그러뜨리려고 **Incremental GC(점진적 GC)**를 제공합니다.

### GC 작업의 분산

기존 Boehm GC는 한 번 시작하면 Mark-and-Sweep을 그 프레임 안에서 끝까지 마칩니다. 힙이 클수록 이 한 프레임이 통째로 길어집니다.

Incremental GC는 같은 Mark-and-Sweep을 여러 조각으로 나눠, 프레임마다 일부만 처리합니다. 한 프레임에서 못 끝낸 부분은 다음 프레임으로 넘기므로, 한 프레임에 더해지는 GC 시간이 그만큼 짧아집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <text fill="currentColor" x="360" y="25" text-anchor="middle" font-size="16" font-weight="bold" font-family="sans-serif">기존 GC vs Incremental GC</text>
  <!-- === Non-incremental === -->
  <text fill="currentColor" x="40" y="55" font-size="13" font-weight="bold" font-family="sans-serif">기존 GC (Non-incremental)</text>
  <!-- 16.6ms marker line -->
  <line x1="40" y1="115" x2="690" y2="115" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <text fill="currentColor" x="690" y="112" text-anchor="end" font-size="9" font-family="monospace" opacity="0.6">16.6ms</text>
  <!-- Frame 1: normal 12ms -->
  <rect x="40" y="68" width="90" height="45" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="85" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">정상</text>
  <text fill="currentColor" x="85" y="104" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.55">12ms</text>
  <!-- Frame 2: Logic 5ms + GC 20ms = 25ms (exceeds) -->
  <rect x="140" y="68" width="38" height="45" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="159" y="95" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">로직</text>
  <rect x="178" y="68" width="152" height="45" rx="3" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="254" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" font-weight="bold">GC (Stop-the-World)</text>
  <text fill="currentColor" x="254" y="104" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.8">20ms</text>
  <!-- Frame 2 total -->
  <line x1="140" y1="120" x2="330" y2="120" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="235" y="137" text-anchor="middle" font-size="10" font-family="monospace" font-weight="bold">25ms → 예산 초과</text>
  <!-- Frame 3 & 4: normal -->
  <rect x="340" y="68" width="90" height="45" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="385" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">정상</text>
  <text fill="currentColor" x="385" y="104" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.55">12ms</text>
  <rect x="440" y="68" width="90" height="45" rx="3" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="485" y="88" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">정상</text>
  <text fill="currentColor" x="485" y="104" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.55">12ms</text>
  <!-- Frame labels -->
  <text fill="currentColor" x="85" y="64" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 1</text>
  <text fill="currentColor" x="235" y="64" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 2</text>
  <text fill="currentColor" x="385" y="64" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 3</text>
  <text fill="currentColor" x="485" y="64" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 4</text>
  <!-- === Incremental === -->
  <text fill="currentColor" x="40" y="185" font-size="13" font-weight="bold" font-family="sans-serif">Incremental GC</text>
  <!-- 16.6ms marker line -->
  <line x1="40" y1="248" x2="690" y2="248" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <text fill="currentColor" x="690" y="245" text-anchor="end" font-size="9" font-family="monospace" opacity="0.6">16.6ms</text>
  <!-- Frame 1 -->
  <rect x="40" y="200" width="75" height="45" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <rect x="115" y="200" width="37" height="45" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="77" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">게임</text>
  <text fill="currentColor" x="133" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">GC</text>
  <text fill="currentColor" x="96" y="236" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.55">10+5ms</text>
  <!-- Frame 2 -->
  <rect x="162" y="200" width="75" height="45" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <rect x="237" y="200" width="37" height="45" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="199" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">게임</text>
  <text fill="currentColor" x="255" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">GC</text>
  <text fill="currentColor" x="218" y="236" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.55">10+5ms</text>
  <!-- Frame 3 -->
  <rect x="284" y="200" width="75" height="45" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <rect x="359" y="200" width="37" height="45" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="321" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">게임</text>
  <text fill="currentColor" x="377" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">GC</text>
  <text fill="currentColor" x="340" y="236" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.55">10+5ms</text>
  <!-- Frame 4 -->
  <rect x="406" y="200" width="75" height="45" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <rect x="481" y="200" width="37" height="45" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="443" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">게임</text>
  <text fill="currentColor" x="499" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">GC</text>
  <text fill="currentColor" x="462" y="236" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.55">10+5ms</text>
  <!-- Frame 5 -->
  <rect x="528" y="200" width="75" height="45" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <rect x="603" y="200" width="45" height="45" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="565" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">게임</text>
  <text fill="currentColor" x="625" y="220" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.8">GC</text>
  <text fill="currentColor" x="587" y="236" text-anchor="middle" font-size="8" font-family="monospace" opacity="0.55">10+6ms</text>
  <!-- Frame labels -->
  <text fill="currentColor" x="96" y="196" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 1</text>
  <text fill="currentColor" x="218" y="196" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 2</text>
  <text fill="currentColor" x="340" y="196" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 3</text>
  <text fill="currentColor" x="462" y="196" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 4</text>
  <text fill="currentColor" x="587" y="196" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">프레임 5</text>
  <!-- Per-frame totals -->
  <text fill="currentColor" x="96" y="260" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.8">15ms</text>
  <text fill="currentColor" x="218" y="260" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.8">15ms</text>
  <text fill="currentColor" x="340" y="260" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.8">15ms</text>
  <text fill="currentColor" x="462" y="260" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.8">15ms</text>
  <text fill="currentColor" x="587" y="260" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.8">16ms</text>
  <text fill="currentColor" x="360" y="280" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.8">(모두 예산 이내)</text>
  <!-- Summary -->
  <rect x="120" y="300" width="480" height="55" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="360" y="322" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">GC 총 작업량: ~26ms</text>
  <text fill="currentColor" x="360" y="342" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(쓰기 장벽 오버헤드로 원래 20ms보다 증가)</text>
  <!-- Legend -->
  <rect x="170" y="375" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.1"/>
  <text fill="currentColor" x="190" y="387" font-size="11" font-family="sans-serif" opacity="0.6">게임 로직</text>
  <rect x="290" y="375" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="310" y="387" font-size="11" font-family="sans-serif" opacity="0.6">GC 작업</text>
  <rect x="400" y="375" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="420" y="387" font-size="11" font-family="sans-serif" opacity="0.6">Stop-the-World</text>
</svg>
</div>

<br>

위 그림처럼 Incremental GC는 GC 작업을 여러 프레임에 나누어 한 프레임의 부담을 줄입니다. 대신 뒤에서 볼 쓰기 장벽 비용이 추가되어 총 GC 작업량은 약간 늘 수 있습니다. 핵심은 총량을 없애는 것이 아니라, 한 프레임에 몰리던 시간을 여러 프레임으로 분산해 프레임 예산을 넘기기 어렵게 만드는 것입니다.

---

### 쓰기 장벽 (Write Barrier)

GC 작업을 여러 프레임에 나누면 새로운 문제가 생깁니다. GC가 객체 A를 검사하고 잠시 멈춘 사이에도 코드는 계속 실행되며, 그동안 A의 참조를 바꿀 수 있기 때문입니다.

예를 들어 코드가 `A.child = newObject`로 A에 새 객체를 연결한다면, GC는 A를 이미 검사한 것으로 처리하므로 뒤늦게 연결된 `newObject`가 검사에서 빠질 수 있습니다. 그러면 살아 있는 객체가 도달 불가능한 것으로 잘못 분류되어 회수될 위험이 생깁니다.

Incremental GC는 이 문제를 **쓰기 장벽(Write Barrier)**으로 막습니다. 코드가 참조 필드를 바꿀 때마다 런타임이 그 변경을 따로 기록해 둡니다.

다음 GC 단계에서는 이 기록을 확인해, 참조가 바뀐 객체를 다시 검사합니다. 그러면 중간에 새로 연결된 객체도 Mark에 포함되어, 살아 있는 객체가 잘못 회수되지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <defs>
    <marker id="m16-a" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="currentColor"/></marker>
  </defs>
  <text fill="currentColor" x="340" y="25" text-anchor="middle" font-size="16" font-weight="bold" font-family="sans-serif">쓰기 장벽의 동작</text>
  <!-- Phase 1: 프레임 N -->
  <rect x="30" y="45" width="620" height="110" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="50" y="68" font-size="14" font-weight="bold" font-family="sans-serif">프레임 N</text>
  <rect x="50" y="80" width="12" height="12" rx="2" fill="currentColor" fill-opacity="0.55"/>
  <text fill="currentColor" x="70" y="92" font-size="12" font-family="sans-serif" opacity="0.8">GC가 객체 A를 검사 완료 (Mark: 도달 가능)</text>
  <rect x="50" y="102" width="12" height="12" rx="2" fill="currentColor" fill-opacity="0.55"/>
  <text fill="currentColor" x="70" y="114" font-size="12" font-family="sans-serif" opacity="0.8">GC가 객체 B까지 검사 완료</text>
  <text fill="currentColor" x="70" y="142" font-size="12" font-family="sans-serif" opacity="0.55">→ 프레임 시간 소진, GC 일시 중단</text>
  <!-- Arrow down -->
  <line x1="340" y1="155" x2="340" y2="175" stroke="currentColor" stroke-width="1.5" marker-end="url(#m16-a)"/>
  <!-- Phase 2: 스크립트 실행 -->
  <rect x="30" y="183" width="620" height="95" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="50" y="206" font-size="14" font-weight="bold" font-family="sans-serif">스크립트 실행</text>
  <rect x="50" y="218" width="380" height="26" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="60" y="236" font-size="12" font-family="monospace">A.child = newObject;</text>
  <text fill="currentColor" x="310" y="236" font-size="11" font-family="sans-serif" opacity="0.8">← 참조 변경 발생!</text>
  <rect x="50" y="250" width="300" height="20" rx="4" fill="currentColor" fill-opacity="0.15"/>
  <text fill="currentColor" x="60" y="265" font-size="12" font-family="sans-serif" opacity="0.8">쓰기 장벽이 변경을 기록</text>
  <!-- Arrow down -->
  <line x1="340" y1="278" x2="340" y2="298" stroke="currentColor" stroke-width="1.5" marker-end="url(#m16-a)"/>
  <!-- Phase 3: 프레임 N+1 -->
  <rect x="30" y="306" width="620" height="105" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="50" y="329" font-size="14" font-weight="bold" font-family="sans-serif">프레임 N+1</text>
  <text fill="currentColor" x="70" y="349" font-size="12" font-family="sans-serif" opacity="0.8">GC 재개</text>
  <text fill="currentColor" x="70" y="369" font-size="12" font-family="sans-serif" opacity="0.8">기록된 변경사항 확인: "A의 참조가 변경됨"</text>
  <text fill="currentColor" x="70" y="389" font-size="12" font-family="sans-serif" opacity="0.8">A를 다시 검사하여 newObject도 Mark</text>
  <text fill="currentColor" x="70" y="406" font-size="11" font-family="sans-serif" opacity="0.55">→ 살아있는 객체가 잘못 수거되는 것을 방지</text>
</svg>
</div>

<br>

다만 이 기록을 남기는 데에도 시간이 들고, 참조를 자주 바꾸는 코드에서는 그 부담이 거듭 누적됩니다.

따라서 Incremental GC는 한 프레임의 큰 스파이크를 줄이는 대신, 전체 GC 관련 작업량은 조금 늘 수 있습니다.

### Incremental GC의 한계

Incremental GC는 스파이크를 줄여 주지만, GC가 해야 할 일의 총량까지 줄이지는 않습니다. 힙에 남은 객체를 검사하고 회수하는 작업은 그대로 남고, 새 객체가 계속 생기는 한 GC도 계속 돌아야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text fill="currentColor" x="310" y="28" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">Incremental GC의 효과와 한계</text>
  <!-- 효과 -->
  <rect x="15" y="45" width="285" height="215" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="157" y="70" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">효과</text>
  <text fill="currentColor" x="35" y="96" font-size="12" font-family="sans-serif" opacity="0.8">· 단일 프레임의 GC 스파이크 크기 감소</text>
  <text fill="currentColor" x="35" y="120" font-size="12" font-family="sans-serif" opacity="0.8">· 프레임 드롭 빈도 감소</text>
  <text fill="currentColor" x="35" y="144" font-size="12" font-family="sans-serif" opacity="0.8">· 플레이어가 체감하는 끊김 완화</text>
  <!-- 한계 -->
  <rect x="320" y="45" width="285" height="215" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="462" y="70" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">한계</text>
  <text fill="currentColor" x="340" y="98" font-size="12" font-family="sans-serif" opacity="0.8">· 총 GC 시간은 같거나 약간 증가</text>
  <text fill="currentColor" x="348" y="114" font-size="12" font-family="sans-serif" opacity="0.6">(쓰기 장벽 오버헤드)</text>
  <text fill="currentColor" x="340" y="142" font-size="12" font-family="sans-serif" opacity="0.8">· 매 프레임 2~3ms의 GC 비용이</text>
  <text fill="currentColor" x="348" y="158" font-size="12" font-family="sans-serif" opacity="0.8">지속 발생</text>
  <text fill="currentColor" x="340" y="186" font-size="12" font-family="sans-serif" opacity="0.8">· 할당 속도 > 해제 속도이면</text>
  <text fill="currentColor" x="348" y="202" font-size="12" font-family="sans-serif" opacity="0.8">결국 큰 스파이크 발생</text>
  <text fill="currentColor" x="340" y="230" font-size="12" font-family="sans-serif" opacity="1.0" font-weight="bold">· 힙 할당 자체를 줄이지 않으면</text>
  <text fill="currentColor" x="348" y="246" font-size="12" font-family="sans-serif" opacity="1.0" font-weight="bold">비용이 계속 남음</text>
  <!-- 하단 결론 -->
  <rect x="100" y="265" width="420" height="35" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="310" y="288" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">스파이크 완화 수단이며 할당 감소를 대체하지 않음</text>
</svg>
</div>

<br>

Incremental GC를 켜도, 할당 속도가 GC가 정리하는 속도를 앞지르면 줄였던 스파이크가 다시 나타납니다. 예를 들어 `Update()`에서 프레임마다 `new string()`이나 `new List<>()`를 만들면, 할당이 계속 늘어 GC가 따라잡지 못합니다.

결국 GC 부담을 근본적으로 덜려면, 여전히 힙 할당을 줄여야 합니다. Incremental GC는 피할 수 없는 GC 비용을 프레임마다 잘게 쪼개, 체감 스파이크를 낮추는 보조 수단일 뿐입니다.

---

### Incremental GC 활성화

Incremental GC는 Unity 에디터의 **Project Settings > Player > Other Settings > Configuration**에서 **Use Incremental GC** 옵션으로 설정할 수 있습니다. 프로젝트와 Unity 버전에 따라 기본 상태가 다를 수 있으므로, 대상 플랫폼 빌드 설정에서 직접 확인하는 것이 좋습니다.

Incremental GC는 GC 알고리즘을 바꾸는 기능이 아닙니다. Boehm GC를 그대로 둔 채 Mark-and-Sweep을 여러 프레임에 나눠 실행할 뿐이라, 비세대·비압축·보수적이라는 기본 특성은 이 옵션을 켜도 그대로 남습니다.

---

## GC.Collect()와 프로파일링

GC 실행 시점은 보통 런타임이 정하지만, C#에는 이를 직접 요청하는 `System.GC.Collect()`도 있습니다. 이 메서드를 호출하면 Unity의 Boehm GC가 그 자리에서 전체 힙을 Mark-and-Sweep합니다.

.NET의 세대별 GC에서는 특정 세대까지만 수집하도록 지정할 수 있지만, 세대를 나누지 않는 Boehm GC에는 그런 선택이 없습니다. 그래서 세대 인자를 넘겨도 Unity에서는 늘 전체 힙을 수집합니다.

`GC.Collect()`는 GC 비용을 줄여 주는 도구가 아닙니다. 호출하면 그 자리에서 C# 코드 실행이 멈추고(Stop-the-World), 그러면서도 GC가 할 일의 양은 그대로이기 때문입니다. 바꿀 수 있는 것은 GC가 도는 시점뿐이므로, 씬 전환이나 로딩 화면처럼 멈춤이 자연스러운 순간에 한해 제한적으로 씁니다.

GC 비용을 근본적으로 낮추려면 호출 시점이 아니라 할당량을 줄여야 합니다. 힙 할당이 어디서 얼마나 일어나는지는 Unity Profiler로 확인할 수 있습니다. CPU 모듈의 `GC.Alloc` 마커로 프레임마다 할당을 일으키는 메서드를 찾아낸 뒤, 그 지점의 할당을 줄이거나 없애는 것이 GC 스파이크를 줄이는 첫걸음입니다.

---

## 마무리

이번 글에서는 GC가 도달할 수 없는 객체를 회수하는 원리와, 그 편리함의 대가가 무엇인지 정리했습니다. 핵심은 다음과 같습니다.

- **Mark-and-Sweep**은 GC 루트에서 참조를 따라 도달 가능한 객체에 표시를 남기고, 표시가 없는 객체를 회수합니다.
- **세대별 GC**는 힙을 Gen 0·1·2로 나누고, 수명이 짧은 객체가 모이는 Gen 0을 자주 검사해 비용을 줄입니다.
- **Boehm GC**는 매번 힙 전체를 훑고(비세대), 객체를 옮기지 않아 단편화를 남기며(비압축), 거짓 참조까지 살려 두는(보수적) 탓에 .NET GC보다 비용이 큽니다.
- GC가 도는 동안 코드 실행이 멈추는 **Stop-the-World**가 프레임 예산을 넘기면 **GC 스파이크**로 나타납니다.
- **Incremental GC**는 한 번의 GC를 여러 프레임에 나눠 스파이크를 낮추지만, 총 GC 시간은 같거나 오히려 조금 늘기도 합니다.
- **GC.Collect()**는 GC 시점을 옮길 뿐이라, 비용을 줄이려면 **Profiler**의 `GC.Alloc` 마커로 할당이 많은 지점부터 찾아야 합니다.

정리하면, Unity의 GC 최적화는 결국 GC가 회수할 객체를 처음부터 적게 만드는 일로 모입니다. Boehm GC의 기본 구조는 프로젝트 코드로 바꿀 수 없지만, 매 프레임 새로 만드는 힙 객체의 양은 코드를 쓰는 방식으로 줄일 수 있습니다.

이 글에서 다룬 GC의 원리는 실전에서 힙 할당을 줄이는 기법의 기반이 됩니다. [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서는 Unity 프로젝트의 GC 비용을 측정하고 할당 패턴을 줄이는 방법을, [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서는 코드에 숨어 있는 힙 할당 패턴과 오브젝트 풀링을 다룹니다. 이어지는 다음 글 [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)에서는 C# 런타임의 멀티스레딩과 비동기 프로그래밍으로 넘어갑니다.

<br>

---

**관련 글**
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)

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
