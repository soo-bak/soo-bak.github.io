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

[C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서는 C# 코드가 IL로 한 번 옮겨진 뒤 다시 기계어로 바뀌어 CPU 위에서 도는 과정을 따라갔습니다. 같은 IL이라도 빌드 시점에 C++로 풀어 네이티브로 미리 컴파일하면 IL2CPP의 AOT 방식이 되고, 실행 도중 그때그때 기계어로 옮기면 Mono의 JIT 방식이 됩니다.

<br>

그런데 런타임이 떠맡는 일은 코드를 돌리는 데서 그치지 않습니다. 그 핵심 역할 가운데 하나가 바로 **메모리의 자동 관리**입니다.

[C# 런타임 기초 (1)](/dev/unity/CSharpRuntime-1/)에서 짚었듯, C# 코드에서 `new`로 참조 타입 객체를 만들면 런타임이 힙에 그만큼의 메모리를 잡아 줍니다. 그리고 그 객체를 가리키는 참조가 모두 사라지면, 런타임을 이루는 구성 요소인 **가비지 컬렉터(Garbage Collector, GC)**가 해당 메모리를 알아서 거두어 갑니다.

<br>

C나 C++에서는 이 일을 개발자가 손수 해야 합니다. 어디서 메모리를 비울지 직접 정해 주어야 하고, 그 판단이 어긋나면 메모리 누수나 댕글링 포인터처럼 프로그램을 무너뜨리는 버그로 이어집니다.

GC는 이 해제 작업을 대신 떠맡아, 개발자가 메모리를 언제 비울지 신경 쓰지 않아도 되게 합니다. 다만 공짜로 얻는 편의는 아닙니다. GC가 도는 동안에는 CPU 시간이 그쪽으로 쏠리고, Unity가 쓰는 Boehm GC는 힙 전체를 훑는 사이 C# 스크립트 실행을 통째로 멈추는 Stop-the-World를 일으킵니다.

<br>

이 글에서는 GC가 왜 필요한지부터 시작해, GC의 바탕이 되는 Mark-and-Sweep 알고리즘, Unity의 Boehm GC가 .NET GC와 어디서 갈리는지, 그리고 이 모든 것이 게임 성능에 어떻게 영향을 주는지를 차례로 살펴봅니다.

---

## GC의 필요성

### 수동 메모리 관리의 위험

C나 C++에서는 메모리를 비우는 일까지 개발자의 몫입니다. `malloc()`이나 `new`로 필요한 만큼 메모리를 잡고, 다 쓰고 나면 `free()`나 `delete`로 직접 돌려줍니다.

언제 잡고 언제 돌려줄지를 개발자가 정하므로, 손에 익으면 군더더기 없이 효율적입니다. 다만 그 판단이 한 번 어긋나면 세 갈래의 위험이 비집고 들어옵니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <rect x="0" y="0" width="620" height="270" rx="8" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="310" y="32" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">수동 메모리 관리의 세 가지 위험</text>
  <!-- 1. 메모리 누수 -->
  <text fill="currentColor" x="30" y="66" font-size="13" font-weight="bold" font-family="sans-serif">1. 메모리 누수 (Memory Leak)</text>
  <text fill="currentColor" x="50" y="86" font-size="12" font-family="sans-serif" opacity="0.8">할당한 메모리를 해제하지 않음</text>
  <text fill="currentColor" x="50" y="104" font-size="11" font-family="sans-serif" opacity="0.55">→ 메모리가 계속 쌓여 결국 부족해짐</text>
  <!-- 2. 댕글링 포인터 -->
  <text fill="currentColor" x="30" y="136" font-size="13" font-weight="bold" font-family="sans-serif">2. 댕글링 포인터 (Dangling Pointer)</text>
  <text fill="currentColor" x="50" y="156" font-size="12" font-family="sans-serif" opacity="0.8">이미 해제된 메모리를 다시 참조함</text>
  <text fill="currentColor" x="50" y="174" font-size="11" font-family="sans-serif" opacity="0.55">→ 엉뚱한 데이터를 읽거나 프로그램이 충돌함</text>
  <!-- 3. 이중 해제 -->
  <text fill="currentColor" x="30" y="206" font-size="13" font-weight="bold" font-family="sans-serif">3. 이중 해제 (Double Free)</text>
  <text fill="currentColor" x="50" y="226" font-size="12" font-family="sans-serif" opacity="0.8">같은 메모리를 두 번 해제함</text>
  <text fill="currentColor" x="50" y="244" font-size="11" font-family="sans-serif" opacity="0.55">→ 메모리 관리 구조가 손상되어 예측 불가능한 동작</text>
</svg>
</div>

<br>

첫 번째 위험인 메모리 누수는 메모리를 잡아 두고 돌려주는 일을 빠뜨릴 때 생깁니다. 한 번 빠뜨린 메모리는 다시 손댈 길이 없어, 프로그램이 오래 돌수록 쓰지도 않는 메모리가 차곡차곡 쌓여 갑니다.

이 문제는 메모리 여유가 빠듯한 모바일에서 특히 날카롭게 드러납니다. iOS는 메모리 압박이 심해지면 앱에 `didReceiveMemoryWarning`을 보내 메모리를 비우라고 재촉하지만, 앱이 제때 충분히 비우지 못하면 jetsam이 그 앱을 강제로 끊어 버립니다.

문제는 이 경고에 응하기가 쉽지 않다는 데 있습니다. 관리 힙의 메모리는 GC가 한 번 돌아야 비로소 회수되고, 설령 회수되더라도 Boehm GC는 비워 낸 공간을 OS에 되돌려주지 않으므로 프로세스가 차지한 메모리 총량 자체는 그대로 남습니다. Android 역시 메모리가 모자라면 백그라운드에 밀려난 앱부터 차례로 끊어 나갑니다.

<br>

두 번째 위험인 댕글링 포인터는 이미 돌려준 메모리를 여전히 가리키는 포인터가 남아 있을 때 생깁니다. 해제된 영역은 곧 다른 용도로 재사용되는데, 그 자리에 다른 데이터가 덮어써진 뒤 옛 포인터로 접근하면 전혀 엉뚱한 값을 읽게 됩니다.

게다가 그 자리에 무엇이 언제 덮어써지느냐에 따라 증상이 매번 달라지므로, 재현조차 들쭉날쭉합니다. 디버깅하기 까다로운 버그가 대개 여기서 비롯됩니다.

<br>

세 번째 위험인 이중 해제는 이미 돌려준 메모리를 또 한 번 돌려줄 때 생깁니다. 두 번째 해제가 메모리 할당자가 안에서 관리하던 자료구조를 헝클어뜨려, 그 뒤로는 할당이든 해제든 무엇 하나 예측대로 굴러가지 않게 됩니다.

<br>

세 위험 모두 코드가 복잡해질수록 빠지기 쉬워집니다. 객체끼리 참조가 얽히고설키면, 어느 객체를 어느 시점에 비워야 안전한지 가늠하기가 어려워지기 때문입니다.

가령 객체 X를 A가 아직 쓰고 있는데 B가 먼저 비워 버리면 A의 참조는 댕글링 포인터가 되고, 반대로 A도 B도 서로 미루다 아무도 비우지 않으면 그대로 메모리 누수로 남습니다.

---

### GC의 역할

이 위험들의 뿌리는 메모리를 비울 책임이 개발자에게 있다는 데 있습니다. GC는 그 책임을 개발자에게서 런타임으로 옮겨 와 문제를 풀어냅니다. 개발자는 메모리를 잡기만 하고, 비우는 일은 GC가 알아서 떠맡습니다.

판단 기준은 단순합니다. 어떤 객체를 가리키는 참조가 더 이상 하나도 남지 않으면, GC가 그 객체의 메모리를 거두어 갑니다.

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

그래서 개발자는 `free()`나 `delete`를 직접 부를 일이 없습니다. 객체를 `new`로 만들어 쓰다가, 다 쓴 뒤 그 객체를 가리키던 참조만 끊어 두면 됩니다. 비우는 시점을 손으로 정하지 않으니, 이미 비운 메모리를 다시 가리키거나 한 번 더 비우는 일 자체가 생기지 않아 댕글링 포인터와 이중 해제는 처음부터 봉쇄됩니다. 참조가 끊긴 객체는 다음 번 GC가 돌 때 회수됩니다.

<br>

물론 GC라고 거저 얻는 것은 아닙니다. GC가 도는 동안에는 CPU 시간이 그쪽으로 들어가고, 때에 따라서는 프로그램 실행이 잠깐 멈추기도 합니다. 이 비용이 언제 얼마나 드는지 가늠하고 다스리려면, 결국 GC가 안에서 어떻게 움직이는지를 알아야 합니다.

---

## Mark-and-Sweep 알고리즘

앞 절에서 보았듯 GC는 참조가 모두 끊긴 객체를 알아서 거두어 갑니다. 그러려면 먼저 지금 힙에 놓인 객체 가운데 어느 것이 아직 살아 있고 어느 것이 죽었는지부터 가려내야 합니다. 이 판정을 도맡는 가장 기본적인 알고리즘이 **Mark-and-Sweep**이며, 그 판정의 잣대로 삼는 것이 바로 **도달 가능성(Reachability)**입니다.

### 도달 가능성 (Reachability)

GC는 객체의 생존 여부를 그 객체가 쓸모 있느냐가 아니라 도달 가능성으로 가립니다. 프로그램이 지금 돌리는 코드에서 참조를 타고 따라가 닿을 수 있는 객체라면 살아 있는 것으로, 어떤 참조를 거쳐도 닿을 수 없는 객체라면 죽은 것으로 봅니다.

<br>

이 도달 가능성을 따질 때 출발점이 되는 것이 **GC 루트(GC Root)**입니다. GC 루트는 프로그램이 지금 직접 손에 쥐고 있는 참조의 진입점으로, 스택 변수와 정적 필드, CPU 레지스터가 여기에 해당합니다.

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

GC 루트가 직접 가리키는 객체는 도달 가능하며, 그 객체가 다시 가리키는 객체도 도달 가능합니다. 이렇게 참조를 한 단계씩 끝까지 타고 들어가면, 도달 가능한 객체 전체가 하나의 집합으로 추려집니다.

이 집합에 끝내 들지 못한 객체는 어떤 루트에서도 닿을 수 없으니 프로그램이 다시 손댈 길이 없고, 그래서 거두어 가도 아무 탈이 없습니다.

---

### Mark 단계

도달 가능성을 가려내는 일이 GC가 가장 먼저 거치는 **Mark(표시)** 단계입니다. GC는 앞서 추린 GC 루트에서 출발해 참조 그래프를 타고 들어가며, 그렇게 닿은 객체마다 "살아 있음" 표시를 하나씩 남깁니다.

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

루트에서 시작한 탐색은 참조 그래프를 한 갈래씩 파고듭니다. 대부분의 GC 구현은 이 탐색에 **마크 스택(mark stack)**을 둔 깊이 우선 탐색을 택하는데, 여기에는 두 가지 이점이 맞물려 있습니다. 스택은 값을 인접한 메모리에 차곡차곡 쌓아 올려 캐시 적중률이 높고, 너비 우선 탐색이라면 따로 들고 있어야 할 큐보다 보조 메모리도 덜 잡아먹습니다.

GC는 이렇게 닿은 객체마다 "도달 가능" 표시를 남깁니다. 그래서 탐색이 다 끝나고 나면, 끝내 표시를 받지 못한 객체는 어느 루트에서도 닿지 못한, 곧 죽은 객체로 가려집니다.

---

### Sweep 단계

살아 있는 객체를 다 표시했으니, 이제 표시가 없는 객체를 실제로 거두어 갈 차례입니다. 이것이 Mark에 뒤이은 **Sweep(소거)** 단계로, GC가 힙에 놓인 객체를 처음부터 끝까지 훑으며 Mark 표시가 붙지 않은 객체의 메모리를 하나씩 풀어 줍니다.

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

Sweep까지 마치고 나면 힙에는 살아 있는 객체만 남고, 죽은 객체가 비워 준 자리는 다음 할당에 그대로 내어 줄 수 있는 빈 공간으로 돌아갑니다. 도달 가능한 객체를 표시하는 Mark와 표시 없는 객체를 거두는 Sweep, 이 두 단계를 묶은 것이 **Mark-and-Sweep 알고리즘**이며, 이것이 GC가 죽은 객체를 가려내는 가장 기본적인 틀입니다.

<br>

죽은 객체를 가려내는 길이 Mark-and-Sweep 하나만 있는 것은 아닙니다. 대표적인 다른 길이 **참조 카운팅(Reference Counting)**입니다. 객체마다 자신을 가리키는 참조가 몇 개인지를 세어 두었다가, 그 수가 0으로 떨어지는 순간 곧바로 해당 객체를 해제합니다.

다만 이 방식에는 빈틈이 있습니다. A가 B를 가리키고 B가 다시 A를 가리키는 **순환 참조**가 끼어 있으면, 바깥에서는 이미 어느 쪽에도 닿을 수 없는데도 서로가 서로를 세어 주는 탓에 참조 수가 0으로 떨어지지 않아, 두 객체가 영영 해제되지 못한 채 힙에 눌러앉습니다.

반면 Mark-and-Sweep은 객체끼리 어떻게 얽혀 있든 따지지 않고 오직 루트에서 닿느냐만 잣대로 삼습니다. 그래서 이런 순환 참조도 루트에서 닿지 못하는 한 죽은 것으로 가려, 군더더기 없이 거두어 갑니다.

---

## 세대별 GC (Generational GC)

Mark-and-Sweep은 GC가 죽은 객체를 가려내는 기본 틀이지만, 세대를 나누지 않는 비세대(non-generational) 방식으로 돌리면 GC가 한 번 돌 때마다 힙에 놓인 객체를 빠짐없이 훑어야 합니다. Mark도 Sweep도 힙 전체를 대상으로 삼기 때문입니다.

그래서 힙에 객체가 10만 개 쌓여 있으면 GC는 매번 그 10만 개를 모두 표시하고 또 모두 소거합니다. 힙이 불어날수록 한 번의 GC에 드는 시간도 그만큼 늘어납니다.

데스크톱과 서버를 겨냥한 .NET 런타임은 이 비용을 덜기 위해 **세대별 GC(Generational GC)**를 들였습니다. 힙 전체를 매번 훑는 대신, 쓰레기가 자주 나오는 자리만 집중해서 살피자는 발상입니다.

### 세대 가설

세대별 GC가 딛고 선 토대가 바로 **세대 가설(Generational Hypothesis)**입니다. 객체의 수명을 두고 경험적으로 거듭 확인된 두 가지 경향을 묶어 부르는 말입니다.

<br>

첫째, **대부분의 객체는 수명이 짧습니다**. 잠깐 쓰고 버리는 임시 문자열이나 루프를 돌며 생기는 중간 결과물, 메서드 안에서만 쓰이는 임시 객체처럼, 만들어지자마자 곧 쓸모를 잃는 객체가 전체의 대부분을 차지합니다.

둘째, **한 번 오래 살아남은 객체는 그 뒤로도 계속 살아남기 쉽습니다**. 캐시나 설정 데이터, 게임이 도는 내내 자리를 지키는 매니저 클래스 인스턴스가 여기 듭니다. 초기에 한 번 만들어진 뒤로는 프로그램이 끝날 때까지 줄곧 살아 있는 객체들입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text fill="currentColor" x="300" y="28" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">객체 수명 분포 (개념적)</text>
  <!-- Y axis -->
  <text fill="currentColor" x="55" y="80" text-anchor="end" font-size="11" font-family="sans-serif" opacity="0.55" transform="rotate(-90,30,140)">객체 수</text>
  <line x1="70" y1="50" x2="70" y2="240" stroke="currentColor" stroke-width="1.5"/>
  <!-- X axis -->
  <line x1="70" y1="240" x2="560" y2="240" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="560,236 570,240 560,244" fill="currentColor"/>
  <text fill="currentColor" x="320" y="262" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">수명</text>
  <!-- X axis labels -->
  <text fill="currentColor" x="110" y="255" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">짧음</text>
  <text fill="currentColor" x="520" y="255" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">긴 수명</text>
  <!-- Bars (object count decreasing as lifetime grows) -->
  <rect x="85" y="60" width="40" height="180" rx="2" fill="currentColor" opacity="0.9"/>
  <rect x="135" y="100" width="40" height="140" rx="2" fill="currentColor" opacity="0.75"/>
  <rect x="185" y="140" width="40" height="100" rx="2" fill="currentColor" opacity="0.6"/>
  <rect x="235" y="175" width="40" height="65" rx="2" fill="currentColor" opacity="0.45"/>
  <rect x="285" y="200" width="40" height="40" rx="2" fill="currentColor" opacity="0.35"/>
  <rect x="335" y="215" width="40" height="25" rx="2" fill="currentColor" opacity="0.28"/>
  <rect x="385" y="222" width="40" height="18" rx="2" fill="currentColor" opacity="0.22"/>
  <rect x="435" y="228" width="40" height="12" rx="2" fill="currentColor" opacity="0.18"/>
  <rect x="485" y="232" width="40" height="8" rx="2" fill="currentColor" opacity="0.15"/>
  <!-- Annotations -->
  <line x1="105" y1="275" x2="105" y2="285" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <line x1="105" y1="285" x2="200" y2="285" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <line x1="200" y1="275" x2="200" y2="285" stroke="currentColor" stroke-width="1" opacity="0.7"/>
  <text fill="currentColor" x="152" y="302" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">대부분의 객체가</text>
  <text fill="currentColor" x="152" y="316" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">여기에 집중 (짧은 수명)</text>
  <line x1="400" y1="275" x2="400" y2="285" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="400" y1="285" x2="520" y2="285" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="520" y1="275" x2="520" y2="285" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text fill="currentColor" x="460" y="302" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">소수의 객체가</text>
  <text fill="currentColor" x="460" y="316" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">오래 생존</text>
</svg>
</div>

<br>

분포를 이렇게 읽으면 GC가 어디에 힘을 쏟아야 하는지가 분명해집니다. 쓰레기의 대부분이 수명 짧은 객체에서 나온다면, 그런 객체가 갓 모여드는 영역만 자주 들여다봐도 쓰레기를 거의 다 걷어 낼 수 있습니다. 오래 살아남아 좀처럼 죽지 않는 객체까지 매번 힙 전체에 끼워 다시 훑을 까닭은 그만큼 줄어듭니다.

---

### Gen 0, Gen 1, Gen 2

세대 가설을 실제 구조로 옮기기 위해, .NET의 세대별 GC는 힙을 Gen 0, Gen 1, Gen 2라는 세 영역으로 가릅니다. 객체가 살아온 시간에 따라 머무는 자리를 달리 정합니다.

갓 만들어진 객체는 모두 Gen 0에서 출발하고, GC 수집을 한 번씩 견뎌 살아남을 때마다 한 단계 위 세대로 옮겨 갑니다. 세대가 높을수록 영역은 더 넓게 잡아 두지만, GC가 들여다보는 빈도는 오히려 낮아집니다. 오래 살아남은 객체일수록 다시 죽을 가능성이 낮아 자주 검사할 까닭이 적기 때문입니다.

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
  <text fill="currentColor" x="105" y="174" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">크기: ~256KB</text>
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
  <text fill="currentColor" x="280" y="174" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">크기: ~2MB</text>
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
  <text fill="currentColor" x="525" y="174" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">크기: 제한 없음</text>
  <line x1="405" y1="185" x2="645" y2="185" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <text fill="currentColor" x="525" y="204" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">수집: 드물게</text>
  <rect x="430" y="218" width="190" height="22" rx="4" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="525" y="234" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.8">빈도 낮음 (Full GC)</text>
</svg>
</div>

<br>

**Gen 0**은 갓 할당된 객체가 가장 먼저 들어서는 세대입니다. 영역을 작게(보통 수백 KB) 잡아 두고 GC가 가장 자주 들여다보므로, 짧게 살다 가는 객체 대부분이 여기서 생겨났다가 여기서 거두어집니다. 새 객체가 차곡차곡 쌓이다 Gen 0이 가득 차면 그 세대만 따로 떼어 수집하는데, 이때 Mark 단계에서 루트로부터 닿아 살아남은 객체만 한 단계 위인 **Gen 1**로 옮겨지고, 이렇게 세대를 올려 보내는 일을 **승격(Promotion)**이라 부릅니다.

<br>

**Gen 1**은 Gen 0 수집을 한 차례 견뎌 낸 객체가 머무는 영역입니다. 한 번 살아남았다는 것은 그만큼 더 오래 쓰일 객체라는 신호이므로, GC는 Gen 1을 Gen 0보다 뜸하게 들여다봅니다. 그러다 Gen 1 수집까지 다시 통과한 객체는 한 단계 더 올라 **Gen 2**로 승격됩니다.

<br>

**Gen 2**는 프로그램 내내 살아남는 장기 생존 객체가 자리 잡는 영역으로, 세 세대 가운데 GC가 가장 드물게 손대는 곳입니다. 다만 Gen 2를 수집하려면 그 아래 세대까지 한꺼번에 훑는 전체 힙 수집, 곧 **Full GC**가 되므로, 한 번 돌 때 드는 비용은 가장 무겁습니다.

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

이 흐름이 곧 세대 가설을 비용으로 환산한 결과입니다. 대부분의 객체가 수명이 짧다면, 크기가 작아 금세 끝나는 Gen 0 수집만 자주 돌려도 쓰레기의 대부분이 걸러집니다. 그래서 비용이 무거운 Full GC는 아래 세대에서 미처 거르지 못한 객체가 쌓일 때만, 그것도 어쩌다 한 번씩만 돌면 됩니다.

<br>

.NET의 세대별 GC는 여기에 더해 수집을 마친 뒤 **압축(Compaction)**까지 거칩니다. 살아남은 객체들을 힙 한쪽으로 차곡차곡 밀어붙여, 그 사이사이 비어 있던 자리를 한데 모아 연속된 빈 공간으로 정리하는 작업입니다.

이렇게 빈자리를 한 덩어리로 모아 두면, 새 객체를 할당할 때 그 연속된 공간을 곧바로 떼어 줄 수 있습니다. 작은 빈틈이 힙 곳곳에 흩어져 쓰지 못하게 되는 메모리 단편화도 이 과정에서 함께 풀립니다.

---

## Unity의 Boehm GC

앞 절에서 본 .NET의 세대별 GC는 데스크톱과 서버를 겨냥한 런타임의 이야기입니다. Unity의 Mono 런타임은 정작 이 세대별 GC를 쓰지 않고, **Boehm GC(Boehm-Demers-Weiser Garbage Collector)**라는 다른 수집기를 얹어 돌립니다.

<br>

Boehm GC는 앞서 본 .NET GC와 세 군데에서 갈립니다. 세대를 따로 나누지 않아 수집할 때마다 힙을 통째로 훑고(**비세대**, Non-generational), 수집을 마쳐도 살아남은 객체를 옮기지 않으며(**비압축**, Non-compacting), 스택에 놓인 값이 객체를 가리키는 참조인지 그저 정수인지를 또렷이 가려내지 못합니다(**보수적**, Conservative).

이 세 성격이 곧 .NET GC와 Boehm GC를 가르는 핵심 차이이며, Unity에서 GC 비용이 유독 무거운 까닭의 뿌리이기도 합니다. 아래에서 하나씩 짚어 보겠습니다.

---

### 비세대 (Non-generational)

Boehm GC와 .NET GC가 처음으로 갈리는 지점은 힙을 세대로 나누느냐입니다. Boehm GC는 세대를 따로 두지 않으므로, .NET GC가 Gen 0만 떼어 살피던 부분 수집이라는 길 자체가 없습니다.

그래서 한 번 GC가 돌 때마다 힙에 놓인 객체를 처음부터 끝까지 빠짐없이 훑어야 합니다.

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

가령 힙에 객체가 1000개 쌓여 있다면, 그중 990개가 한참 전부터 자리를 지켜 온 장기 생존 객체라 해도 Boehm GC는 1000개를 빠짐없이 검사 대상에 올립니다. 오래 살아남은 객체만 따로 건너뛸 길이 없기 때문입니다.

여기서 Mark 단계에 드는 비용은 살아남은 객체 수를 따라가고, Sweep 단계에 드는 비용은 힙 전체 크기를 따라갑니다. 그래서 힙이 불어날수록 한 번의 GC에 걸리는 시간도 그만큼 길어지게 됩니다.

---

### 비압축 (Non-compacting)

두 번째 차이는 수집을 마친 뒤 살아남은 객체를 옮기느냐입니다. 앞서 .NET GC는 압축으로 객체를 한쪽에 차곡차곡 밀어붙인다고 했는데, Boehm GC는 Sweep을 끝내고도 객체를 제자리에 그대로 둡니다.

그러다 보니 죽은 객체를 해제한 자리는 빈틈으로 남고, 그 빈틈이 살아남은 객체 사이사이에 점점이 흩어집니다. 이렇게 작은 빈 공간이 힙 곳곳에 조각조각 끼어드는 것을 **메모리 단편화(Fragmentation)**라고 부릅니다.

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

위 그림처럼 빈자리가 조각나면 묘한 상황이 빚어집니다. 비어 있는 공간을 모두 더하면 120B에 이르는데도, 한 덩어리로 이어진 가장 큰 빈자리는 40B뿐이라 50B짜리 객체 하나 들여놓을 자리가 없습니다. .NET GC라면 압축으로 살아남은 객체를 한쪽에 몰아붙여 빈자리를 늘 한 덩어리로 모아 두므로 이런 일이 생기지 않지만, 객체를 옮기지 않는 Boehm GC에서는 빈 공간 총량이 넉넉해도 이어진 블록이 모자라면 새 객체를 받아 줄 수 없습니다. 결국 힙은 실제로 쓰는 양보다 더 부풀어 오릅니다.

<br>

더 까다로운 점은, 이렇게 한 번 넓어진 힙이 다시 좁아지지 않는다는 데 있습니다. GC가 죽은 객체를 거두어 메모리를 비워 내더라도 힙이 차지한 크기 자체는 그대로 유지되므로, 비세대 방식이 매번 훑어야 하는 검사 범위도 넓어진 채로 남습니다.

가령 게임 초반에 임시 객체를 한꺼번에 쏟아내 힙이 한 차례 넓어졌다면, 그 임시 객체를 모두 거두어 간 뒤에도 GC가 힙 전체를 훑는 시간은 줄지 않고 그대로 길게 남게 됩니다.

---

### 보수적 (Conservative)

세 번째 차이는 어떤 값이 객체를 가리키는 참조인지 가려내는 정확도입니다. Boehm GC는 본래 C와 C++ 같은 언어를 두루 받쳐 주려고 만든 범용 수집기라, 타입 정보가 주어지지 않아도 돌아가도록 설계되어 있습니다.

다만 타입 정보가 없으면, 메모리에 놓인 어떤 값이 객체를 가리키는 포인터인지 그저 평범한 정수인지를 가려낼 길이 없습니다.

<br>

이 한계가 특히 또렷하게 드러나는 자리가 **스택과 레지스터**입니다. 스택의 지역 변수나 레지스터에는 객체를 가리키는 포인터만 담기는 것이 아니라, 해시 코드나 연산 중간값 같은 평범한 정수도 함께 들어앉기 때문입니다.

보수적 GC는 이 슬롯이 포인터를 담았는지 정수를 담았는지 알려 주는 타입 정보를 갖고 있지 않습니다. 그래서 어떤 슬롯의 정수값이 마침 힙에 놓인 객체의 주소와 우연히 맞아떨어지면, GC는 그 값을 포인터로 받아들여 해당 객체를 아직 살아 있는 것으로 묶어 둡니다. 이렇게 멀쩡한 정수까지 참조일지 모른다며 안전하게 넘겨짚는 태도에서 **보수적(Conservative)**이라는 이름이 나왔습니다.

<br>

다만 Unity의 Mono는 이 보수적 스캔의 범위를 한쪽에서 좁혀 둡니다. Boehm GC에 타입 디스크립터를 건네주어, **힙 객체의 필드**만큼은 정확하게 훑도록 다듬어 두었습니다. 객체의 어느 필드가 참조이고 어느 필드가 정수인지 타입 정보로 또렷이 가려낼 수 있기 때문입니다.

그러나 **스택과 레지스터**에는 이런 타입 정보가 끝내 주어지지 않아 여전히 보수적으로 훑을 수밖에 없으며, 뒤에서 볼 거짓 참조도 주로 이 자리에서 생겨납니다.

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

그림 속 객체 Y처럼, 이렇게 우연히 빚어지는 **거짓 참조(False Reference)** 탓에 정작 아무도 쓰지 않는 죽은 객체가 거두어지지 못한 채 힙에 눌러앉을 수 있습니다.

이런 거짓 참조가 곳곳에서 생기면 쓰지도 않는 쓰레기가 힙에 쌓여 크기가 군더더기로 불어나고, 앞서 본 비세대 특성과 맞물려 GC가 힙 전체를 훑는 시간까지 덩달아 길어지게 됩니다.

<br>

반면 .NET GC는 이런 넘겨짚기 없이 참조를 또렷이 가려내는 **정확한(Precise)** GC입니다. .NET 런타임은 JIT 컴파일 시점에 각 스택 프레임마다 타입 정보(GC Info)를 함께 만들어 두므로, 스택의 어느 슬롯이 객체 참조이고 어느 슬롯이 정수인지를 정확히 구분할 수 있습니다.

그래서 정수를 참조로 잘못 넘겨짚는 거짓 참조가 끼어들 여지가 없습니다. 앞 절에서 본 압축, 곧 살아남은 객체를 마음 놓고 옮겨 빈자리를 모으는 일이 가능한 것도 바로 이렇게 참조를 정확히 짚어 두는 덕분입니다.

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

표를 보면 Boehm GC가 .NET GC에 견주어 거의 모든 칸에서 뒤처지는데, 그런데도 Unity가 이 수집기를 그대로 안고 가는 까닭은 성능보다 역사적 사정에 있습니다.

Unity가 Mono 런타임을 처음 들이던 시절(Unity 1.x, 2005년경)에 Boehm GC가 그 일부로 함께 따라 들어왔고, 그 뒤로 엔진의 네이티브 코드와 직렬화 시스템, 스크립팅 바인딩에 이르기까지 엔진의 여러 갈래가 이 GC를 발판으로 쌓여 올라갔습니다. 이제 와 .NET의 세대별 GC로 갈아 끼우려면 이렇게 얽힌 의존 관계를 통째로 다시 설계해야 합니다.

그래서 Unity는 이 교체를 멀리 둔 목표로만 잡아 둔 채, 지금까지도 Boehm GC를 그대로 쓰고 있습니다.

---

## Stop-the-World와 GC 스파이크

세대를 나누지도, 살아남은 객체를 한쪽으로 모으지도, 무엇이 참조인지 단정하지도 않는 Boehm GC의 성격은 한 번 GC가 돌 때 드는 비용을 끌어올립니다. 매번 힙 전체를 보수적으로 훑어야 하니, 그 한 번이 가볍게 끝나기 어렵기 때문입니다.

<br>

이 비용은 코드 위에서만 머무는 추상이 아니라, 게임이 도는 현장에서 두 가지 모습으로 드러납니다. GC가 도는 동안 게임 로직이 잠시 멎는 **Stop-the-World**, 그리고 그 멈춤이 한 프레임의 시간을 위로 솟구치게 하는 **GC 스파이크(GC Spike)**입니다. 앞은 멈춤이라는 동작 자체를, 뒤는 그 동작이 프레임에 남기는 자국을 가리킵니다.

### Stop-the-World

두 모습 가운데 먼저 짚을 것은 멈춤 그 자체입니다. **Stop-the-World**는 GC가 도는 동안 모든 C# 스크립트의 실행을 한꺼번에 멈춰 세우는 동작을 가리킵니다.

<br>

GC가 굳이 스크립트를 멈추는 까닭은 Mark 단계의 결과를 어긋나지 않게 지키기 위해서입니다. GC가 힙을 훑으며 어느 객체가 살아 있는지 표시하는 사이에 스크립트가 끼어들어 새 객체를 만들거나 객체끼리의 참조를 바꿔 버리면, 방금 표시해 둔 결과가 실제 상태와 어긋나게 됩니다. 그래서 GC는 힙 검사를 마칠 때까지 스크립트를 손대지 못하도록 잡아 둡니다.

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

한 프레임 안에서 일어나는 일은 입력 처리와 게임 로직, 렌더링 명령으로 정해져 있는데, GC가 끼어든 프레임에서는 그 사이에 Stop-the-World로 멎어 있던 시간이 고스란히 더해집니다. 위 그림에서 5ms 로직과 4ms 렌더링만으로 끝났을 프레임이, 15ms짜리 GC가 한가운데 들어서면서 24.5ms까지 불어나는 것이 바로 이 합산입니다.

<br>

이렇게 더해진 시간이 60fps 기준의 16.6ms 프레임 예산을 넘어서면, 그 프레임은 제때 화면에 그려지지 못합니다. 화면 갱신이 한 박자 늦어지는 셈이라, 플레이어는 매끄럽게 이어지던 화면이 순간 걸리는 끊김, 곧 **스터터링(Stuttering)**으로 이 지연을 느끼게 됩니다.

---

### GC 스파이크

앞의 Stop-the-World가 프레임을 멎게 하는 동작이라면, 그 멈춤이 프레임 시간 그래프에 남기는 자국이 바로 **GC 스파이크(GC Spike)**입니다. GC가 끼어든 한 프레임만 시간이 유독 높이 솟아오르는 모양이라 이런 이름이 붙었습니다.

<br>

이 모양은 Unity Profiler로 프레임마다의 시간을 늘어놓고 보면 한눈에 드러납니다. 평소 10~15ms 안팎에서 고르게 이어지던 막대들 사이로, GC가 든 프레임 하나만 25~50ms까지 불쑥 솟아 다른 막대를 한참 웃돕니다.

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

막대가 얼마나 높이 솟느냐, 곧 스파이크의 크기를 가르는 것은 **힙 크기**와 **살아 있는 객체의 참조 구조** 두 가지입니다. 둘 다 GC가 한 번 도는 데 걸리는 시간을 좌우하는 요인입니다.

먼저 힙 크기에 따라 검사할 대상의 양이 달라집니다. 세대를 나누지 않는 Boehm GC는 GC가 돌 때마다 힙에 놓인 객체를 빠짐없이 훑으므로, 힙에 쌓인 객체가 많을수록 Mark 단계에서 살펴야 할 객체도 그만큼 불어나 한 번의 GC가 길어집니다. 여기에 객체끼리의 참조가 이리저리 얽혀 있으면, 그 참조를 한 갈래씩 타고 들어가는 그래프 탐색에도 더 많은 시간이 들어갑니다.

<br>

같은 크기의 힙이라도 어느 기기에서 도느냐에 따라 스파이크의 높이는 또 달라집니다. GC는 결국 CPU가 떠맡는 일이라, CPU 성능이 데스크톱보다 처지는 모바일에서는 똑같은 힙을 훑는 데에도 시간이 더 걸리기 때문입니다. 데스크톱에서 5ms로 끝나던 GC가 모바일에서는 15~20ms까지 늘어나기도 합니다.

---

## Incremental GC

앞서 본 GC 스파이크는 한 프레임에 GC 작업이 통째로 몰리면서 그 프레임만 예산을 넘겨 버리는 데서 비롯됩니다. 그렇다면 그 작업을 한 프레임에 다 끝내려 들지 않고 여러 프레임에 잘게 나눠 흘려보내면, 프레임 하나가 솟구치는 일은 누그러뜨릴 수 있습니다. Unity가 2019.1부터 들인 **Incremental GC(점진적 GC)**가 바로 이 발상에서 나온 방식입니다.

### GC 작업의 분산

Boehm GC의 기본 모드는 GC가 한 번 시작되면 Mark-and-Sweep 전체를 그 프레임 안에 끝까지 마쳐야 합니다. 그래서 힙이 무거운 순간에 GC가 끼어들면, 그 한 프레임에 GC 시간이 고스란히 얹혀 예산을 훌쩍 넘기게 됩니다.

Incremental GC는 같은 Mark-and-Sweep을 한 번에 몰아치지 않고, 프레임마다 일부만 떼어 조금씩 밀고 나가는 방식으로 풀어냅니다. 한 프레임에서는 GC 작업의 한 조각만 처리하고 나머지는 다음 프레임으로 넘기므로, 프레임 하나에 얹히는 GC 비용 자체가 작게 쪼개집니다.

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
  <text fill="currentColor" x="235" y="137" text-anchor="middle" font-size="10" font-family="monospace" font-weight="bold">25ms → 프레임 드롭!</text>
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

위 그림에서 보듯, GC를 여러 프레임에 흩뿌리는 대신 치르는 값이 하나 있습니다. 뒤에서 다룰 쓰기 장벽 비용이 더해지면서 GC 총 작업량이 원래 20ms에서 ~26ms로 다소 불어난다는 점입니다. 다만 그렇게 늘어난 작업도 프레임마다 잘게 쪼개져 흘러가므로, 한 프레임이 떠안는 GC 비용은 5ms 안팎으로 가벼워집니다. 그래서 게임 로직과 합쳐도 프레임마다 15ms 안팎에 머물러 16.6ms 예산을 넘지 않고, 눈에 띄던 끊김도 가라앉게 됩니다.

---

### 쓰기 장벽 (Write Barrier)

GC 작업을 여러 프레임에 쪼개 놓으면 기본 모드에는 없던 빈틈이 하나 벌어집니다. GC가 한 프레임에서 객체 A를 검사해 두고 멈춘 뒤, 다음 프레임에서 다시 일을 잡기까지 그 사이에 스크립트가 멀쩡히 돌아간다는 점입니다.

이 틈에 스크립트가 `A.child = newObject`처럼 A의 참조를 바꿔 새 객체를 매달면 문제가 불거집니다. GC는 A를 이미 다 살펴본 뒤라 그 너머에 새로 붙은 newObject를 알 길이 없고, 어느 루트에서도 닿지 못하는 것으로 잘못 가려 멀쩡히 살아 있는 객체를 거두어 버릴 수 있습니다.

<br>

Incremental GC는 이 틈을 **쓰기 장벽(Write Barrier)**으로 메웁니다. 스크립트가 참조 필드를 고쳐 쓸 때마다 런타임이 그 자리에 끼어들어, 이 객체의 참조가 바뀌었다는 사실을 따로 기록해 둡니다.

그러다 다음 프레임에서 GC가 일을 다시 잡으면, 먼저 이 기록부터 들춰 봅니다. 바뀐 자리로 짚어 들어가 A를 한 번 더 검사하면, 그 사이 새로 매달린 newObject까지 빠짐없이 표시되므로 살아 있는 객체를 잘못 거두는 일이 막힙니다.

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

다만 이 안전장치는 공짜로 얻어지지 않습니다. 쓰기 장벽은 참조 필드를 고쳐 쓰는 자리마다 빠짐없이 끼어들어 기록을 남기므로, 참조를 자주 갈아 끼우는 코드일수록 그 기록 비용이 차곡차곡 더해집니다.

앞 그림에서 GC 총 작업량이 원래 20ms에서 ~26ms로 불어난 대목이 바로 이 쓰기 장벽 몫입니다. 한 프레임의 스파이크를 잘게 흩어 주는 대신, 그 대가로 총 작업량이 다소 늘어나는 맞바꿈인 셈입니다.

---

### Incremental GC의 한계

여기까지 보면 Incremental GC가 스파이크를 다스리는 든든한 장치처럼 비치지만, 한 가지 선만큼은 분명히 그어 두어야 합니다. Incremental GC는 GC가 남기는 자국을 잘게 흩어 누그러뜨릴 뿐, GC라는 비용 자체를 걷어 내지는 못합니다.

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
  <text fill="currentColor" x="348" y="246" font-size="12" font-family="sans-serif" opacity="1.0" font-weight="bold">근본 해결 안 됨</text>
  <!-- 하단 결론 -->
  <rect x="100" y="265" width="420" height="35" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="310" y="288" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.8">스파이크 완화 수단이지 근본적 해결책이 아님</text>
</svg>
</div>

<br>

그림의 오른쪽이 짚듯, Incremental GC가 손대는 것은 어디까지나 GC가 한 번 돌 때 남기는 자국의 모양일 뿐, GC가 돌아야 하는 상황 자체는 그대로 남습니다. 힙에 새 객체가 계속 쌓이면 GC는 변함없이 다시 돌고, 매 프레임 2~3ms의 GC 비용도 끊이지 않고 따라붙습니다.

이 한계가 가장 선명하게 드러나는 자리가 매 프레임 새로 할당을 일으키는 코드입니다. `Update()` 안에서 프레임마다 `new string()`이나 `new List<>()`로 객체를 찍어 내면, Incremental GC를 켜 두었더라도 할당이 해제를 앞질러 쌓이면서 GC 비용이 프레임마다 더해지고, 끝내 잘게 흩어 내지 못한 큰 스파이크가 다시 솟구치게 됩니다.

<br>

그래서 GC 문제를 뿌리째 잡으려면 힙 할당 자체를 줄여야 합니다. Incremental GC는 할당을 최대한 덜어 낸 뒤에도 끝내 남는 불가피한 GC 비용을, 한 프레임에 몰리지 않게 여러 프레임으로 흩어 주는 보조 장치로 두는 것이 맞습니다.

---

### Incremental GC 활성화

Incremental GC는 Unity 에디터의 **Project Settings > Player > Other Settings > Configuration**에서 **Use Incremental GC** 체크박스로 켭니다. Unity 2019.3 이후 버전에서는 이 옵션이 처음부터 켜진 채로 들어가 있습니다.

<br>

한 가지 짚어 둘 것은, Incremental GC가 GC 알고리즘 자체를 갈아 끼우는 기능은 아니라는 점입니다. 세대를 나누는 세대별 GC로 바뀌는 것이 아니라, 앞서 본 Boehm GC 위에 얹혀 그 Mark-and-Sweep을 여러 프레임에 나누어 돌리도록 손보는 방식에 가깝습니다.

그러므로 비세대, 비압축, 보수적이라는 Boehm GC의 근본 성격은 Incremental GC를 켜도 그대로입니다. 달라지는 것은 같은 Mark-and-Sweep을 한 프레임에 몰아치느냐, 여러 프레임에 잘게 나누어 흘려보내느냐 하는 처리 시점뿐입니다.

---

## GC.Collect()와 프로파일링

지금까지는 GC가 언제 어떻게 도는지를 런타임의 판단에 맡겨 둔 그림이었습니다. 그런데 C# 코드 쪽에서 GC를 직접 불러내는 손잡이도 하나 마련되어 있는데, 바로 `System.GC.Collect()`입니다. 이 메서드를 호출하면 Unity의 Boehm GC가 그 자리에서 전체 힙을 훑는 Mark-and-Sweep을 돌립니다.

.NET이라면 몇 세대까지 거둘지를 인자로 넘길 수 있지만, Unity의 Boehm GC는 애초에 세대를 나누지 않으므로 그런 인자는 받아도 무시한 채 언제나 힙 전체를 검사합니다.

<br>

다만 이 호출에는 Stop-the-World가 따라붙습니다. 부르는 순간 C# 스크립트가 통째로 멈추므로, 한창 플레이가 돌아가는 도중에 끼워 넣는 것은 피하는 편이 원칙입니다. 대신 씬을 새로 불러오거나 화면이 페이드 아웃되는 것처럼 플레이어가 잠깐의 멈춤을 알아채지 못하는 길목을 골라, 그 틈에 호출해 힙을 한 번 비워 두는 식으로 씁니다.

<br>

힙 할당이 어디서 얼마나 일어나는지를 손으로 가늠하기는 어렵고, 이를 짚어 주는 도구가 Unity Profiler입니다. CPU 모듈에 찍히는 `GC.Alloc` 마커를 따라가면, 매 프레임 어느 메서드가 힙을 얼마나 집어삼키는지 메서드 단위로 드러납니다. GC 스파이크를 다스리는 첫걸음은 결국 이 마커로 할당이 쏠리는 지점을 찾아내, 그 할당 자체를 덜어 내거나 아예 없애는 데 있습니다.

---

## 마무리

GC는 메모리를 알아서 거두어 가는 대신 메모리 누수와 댕글링 포인터, 이중 해제 같은 수동 관리의 위험을 개발자의 손에서 덜어 줍니다. 다만 그 일을 하느라 도는 시간이 그대로 프레임 시간을 갉아먹는데, Unity의 Boehm GC는 비세대·비압축·보수적이라는 성격 탓에 .NET의 세대별 GC보다 이 비용을 더 무겁게 치릅니다.

- Mark-and-Sweep은 GC 루트(스택 변수·정적 필드)에서 참조 그래프를 타고 도달 가능한 객체에 표시를 남긴 뒤, 표시가 없는 객체를 거두어 갑니다.
- .NET의 세대별 GC는 힙을 Gen 0/1/2로 가르고, 수명 짧은 객체가 모여드는 Gen 0만 자주 들여다봅니다.
- Unity의 Boehm GC는 매번 힙 전체를 훑는 비세대, 단편화를 남기는 비압축, 거짓 참조까지 살려 두는 보수적 성격을 함께 지녀 .NET GC보다 비용이 큽니다.
- GC가 도는 동안 모든 스크립트가 멈추는 Stop-the-World가 프레임 예산을 넘기면 GC 스파이크로 이어집니다.
- Incremental GC는 한 번의 GC를 여러 프레임에 잘게 나누어 스파이크를 누그러뜨리지만, 총 GC 시간 자체는 같거나 오히려 조금 늘기도 합니다.
- `GC.Collect()`는 씬 전환처럼 잠깐의 멈춤이 허용되는 길목에서 불러 힙을 비워 두는 용도로 씁니다.
- Unity Profiler의 `GC.Alloc` 마커로 힙 할당이 쏠리는 지점을 짚어 내는 것이 최적화의 출발점입니다.
- GC 문제를 뿌리에서 푸는 길은 결국 힙 할당 자체를 덜어 내는 데 있습니다.

이 항목들을 한 줄로 꿰면, GC 비용을 다스리는 일은 GC 알고리즘을 바꾸는 것이 아니라 GC가 거둘 거리를 애초에 적게 남기는 데로 모입니다. Boehm GC의 성격은 우리가 손댈 수 있는 영역이 아니지만, 매 프레임 얼마나 많은 객체를 새로 힙에 올리느냐는 코드를 쓰는 쪽의 몫이기 때문입니다.

<br>

이 글에서 짚은 GC의 원리는 실전에서 힙 할당을 덜어 내는 기법의 밑바탕이 됩니다. [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서는 Unity 프로젝트의 GC 비용을 직접 재고 할당 패턴을 걷어 내는 방법을, [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서는 코드에 숨어 있는 힙 할당 패턴과 오브젝트 풀링을 다룹니다. 이어지는 다음 글 [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)에서는 C# 런타임의 멀티스레딩과 비동기 프로그래밍으로 넘어갑니다.

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
