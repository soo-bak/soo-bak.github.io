---
layout: single
title: "메모리 관리 (1) - 가비지 컬렉션의 원리 - soo:bak"
date: "2026-02-15 22:44:00 +0900"
description: 관리 힙, Boehm GC, GC 스파이크, Incremental GC, GC.Collect 사용 시점을 설명합니다.
tags:
  - Unity
  - 최적화
  - GC
  - 메모리
  - 모바일
---

## 힙 할당에서 가비지 컬렉션으로

[스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서 다루었듯이, 값 타입(int, float, struct 등)은 스택에, 참조 타입(class 인스턴스, string, 배열 등)은 **관리 힙(Managed Heap)**에 할당됩니다.

스택 메모리는 함수가 끝나면 스택 프레임과 함께 사라지므로 별도의 정리가 필요 없습니다.
반면, 관리 힙의 객체는 함수가 끝나도 사라지지 않습니다. 다른 코드가 그 객체를 아직 참조하고 있을 수 있기 때문입니다.
참조가 모두 사라지면 **가비지 컬렉터(Garbage Collector, GC)**가 해당 객체를 찾아 메모리를 회수합니다.

하지만 이 과정에는 비용이 따릅니다.
Unity가 사용하는 Boehm GC는 이 비용이 특히 커서, 게임 중 프레임이 멈추는 원인이 되기도 합니다.

이 글에서는 관리 힙의 구조, Boehm GC의 동작과 비용, 그리고 그 비용을 줄이는 방법을 다룹니다.

---

## 관리 힙(Managed Heap)의 구조

관리 힙은 C# 런타임이 관리하는 메모리 영역입니다.
`new` 키워드로 생성된 class 인스턴스, string 연산으로 만들어진 새 문자열, 배열 등 모든 참조 타입 객체가 이 영역에 할당됩니다.

이 영역은 프로그램이 시작될 때 하나의 연속된 메모리 블록으로 확보됩니다.
객체가 할당될 때마다 빈 공간에 순서대로 배치되며, 블록이 부족해지면 추가 블록을 요청하여 확장됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 150" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">관리 힙의 초기 상태</text>
  <!-- 힙 외곽 -->
  <rect x="20" y="38" width="580" height="52" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 객체A -->
  <rect x="32" y="48" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="72" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체A</text>
  <!-- 객체B -->
  <rect x="122" y="48" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="162" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체B</text>
  <!-- 객체C -->
  <rect x="212" y="48" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="252" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체C</text>
  <!-- 객체D -->
  <rect x="302" y="48" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="342" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체D</text>
  <!-- 빈 공간 (점선) -->
  <rect x="392" y="48" width="196" height="32" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.4"/>
  <text x="490" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">빈 공간 ...</text>
  <!-- 화살표: 다음 할당 위치 -->
  <line x1="392" y1="100" x2="392" y2="84" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="392,80 388,88 396,88" fill="currentColor"/>
  <text x="392" y="116" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">다음 할당 위치</text>
</svg>
</div>

<br>

새 객체를 할당할 때 런타임은 현재 할당 위치에서 필요한 크기만큼 공간을 확보하고, 할당 위치를 앞으로 이동시킵니다.

빈 공간이 충분한 동안 할당은 빠르지만, 부족해지면 GC가 실행됩니다. GC는 더 이상 참조되지 않는 객체를 찾아 메모리를 해제하고, 해제된 공간을 새 할당에 사용할 수 있게 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- === GC 실행 전 === -->
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GC 실행 전 (빈 공간 부족)</text>
  <!-- 힙 외곽 -->
  <rect x="20" y="38" width="580" height="52" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 객체A -->
  <rect x="30" y="48" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="73" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체A</text>
  <!-- 객체B (참조 안 됨 - 약간 다른 표시) -->
  <rect x="126" y="48" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="169" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체B</text>
  <!-- 객체C -->
  <rect x="222" y="48" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체C</text>
  <!-- 객체D (참조 안 됨) -->
  <rect x="318" y="48" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="361" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체D</text>
  <!-- 객체E -->
  <rect x="414" y="48" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="457" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체E</text>
  <!-- 객체F -->
  <rect x="510" y="48" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="551" y="69" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체F</text>
  <!-- 주석: B와 D는 더 이상 참조되지 않음 -->
  <text x="310" y="110" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(객체B와 객체D는 더 이상 참조되지 않음)</text>

  <!-- === GC 실행 후 === -->
  <text x="310" y="146" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GC 실행 후 (해제된 공간 발생)</text>
  <!-- 힙 외곽 -->
  <rect x="20" y="162" width="580" height="52" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 객체A -->
  <rect x="30" y="172" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="73" y="193" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체A</text>
  <!-- 빈 공간 (B 해제) -->
  <rect x="126" y="172" width="86" height="32" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.4"/>
  <text x="169" y="193" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.45">빈</text>
  <!-- 객체C -->
  <rect x="222" y="172" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="193" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체C</text>
  <!-- 빈 공간 (D 해제) -->
  <rect x="318" y="172" width="86" height="32" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.4"/>
  <text x="361" y="193" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.45">빈</text>
  <!-- 객체E -->
  <rect x="414" y="172" width="86" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="457" y="193" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체E</text>
  <!-- 객체F -->
  <rect x="510" y="172" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="551" y="193" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">객체F</text>
</svg>
</div>

<br>

위 그림처럼 GC가 객체를 해제해도 빈 공간이 힙 중간에 흩어질 수 있는데, 이를 **단편화(Fragmentation)**라 합니다.

단편화가 진행되면 전체 빈 공간은 충분하더라도 연속된 큰 공간을 확보할 수 없어 힙을 추가로 확장해야 합니다.
Unity의 Boehm GC에는 이 단편화를 해소할 수 있는 메커니즘이 없어, 힙 할당이 반복될수록 단편화가 누적됩니다.

---

## Unity의 Boehm GC

Unity는 **Boehm-Demers-Weiser GC**(이하 Boehm GC)를 사용합니다. Boehm GC는 C/C++ 환경에서도 동작하도록 설계된 범용 GC로, .NET 런타임이 사용하는 GC와는 다른 구현체입니다.

Boehm GC에는 **비세대(Non-generational)**, **비압축(Non-compacting)**, **보수적(Conservative)** 세 가지 핵심 특성이 있습니다. 이 특성들이 **Stop-the-world** 실행 방식과 결합되어, 앞서 본 단편화 누적을 포함해 Unity에서 GC가 일으키는 성능 문제의 근본 원인이 됩니다.

---

### 비세대(Non-generational)

.NET 런타임의 GC는 **세대별(generational)** 구조를 사용합니다.
"대부분의 객체는 생성 직후 곧 참조를 잃는다"는 통계적 관찰(**generational hypothesis**)에 기반하여, 객체를 Gen0, Gen1, Gen2로 분류하고 최근 생성된 객체(Gen0)만 자주 검사합니다.
오래 살아남은 객체는 상위 세대로 승격되어 드물게 검사되므로, 매번 힙 전체를 순회하지 않아도 가비지 대부분을 회수할 수 있습니다.

반면 Boehm GC는 세대 구분이 없습니다.
GC가 실행될 때마다 **힙 전체**를 검사합니다. 힙에 객체가 100개든 100만 개든, 매번 모든 객체를 순회해야 합니다.

따라서 Boehm GC 실행 1회의 소요 시간은 힙 크기에 비례합니다.
힙이 작을 때는 전체를 검사해도 시간이 짧지만, 게임이 진행되면서 힙이 커지면 실행 한 번에 걸리는 시간도 함께 늘어납니다.
예를 들어 힙이 50MB일 때 5ms 걸리던 GC 실행이 힙이 200MB로 커지면 20ms 이상 소요될 수 있습니다.
게임이 60fps로 동작하려면 한 프레임을 16.6ms 안에 처리해야 하므로, GC 실행 시간이 이 프레임 예산을 초과하면 프레임 드롭으로 이어집니다.

---

### 비압축(Non-compacting)

일반적인 .NET GC는 사용하지 않는 객체를 해제한 뒤, 남은 객체를 한쪽으로 밀어 모아서 메모리를 **압축(compaction)**합니다.
빈 공간이 하나의 연속된 블록으로 합쳐져 단편화가 해소되므로, 새 객체를 할당할 때 빈 공간을 탐색하는 비용이 거의 들지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">압축 GC (.NET)</text>
  <text x="36" y="54" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">GC 전</text>
  <rect x="80" y="38" width="460" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="88" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="120" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">A</text>
  <rect x="160" y="44" width="64" height="20" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="192" y="58" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">빈</text>
  <rect x="232" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="264" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">C</text>
  <rect x="304" y="44" width="64" height="20" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="336" y="58" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">빈</text>
  <rect x="376" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="408" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">E</text>
  <rect x="448" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="480" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">F</text>
  <line x1="280" y1="78" x2="280" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="280,102 276,94 284,94" fill="currentColor"/>
  <text x="36" y="126" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">GC 후</text>
  <rect x="80" y="110" width="460" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="88" y="116" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="120" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">A</text>
  <rect x="156" y="116" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="188" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">C</text>
  <rect x="224" y="116" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="256" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">E</text>
  <rect x="292" y="116" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="324" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">F</text>
  <rect x="364" y="116" width="168" height="20" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="448" y="130" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">연속된 빈 공간</text>
  <line x1="88" y1="150" x2="356" y2="150" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="222" y="164" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">객체 압축</text>
  <line x1="364" y1="150" x2="532" y2="150" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="448" y="164" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">연속된 빈 공간</text>
</svg>
</div>

<br>

반면 Boehm GC는 압축을 수행하지 않으므로, 해제된 객체의 자리가 그대로 빈 공간으로 남습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">비압축 GC (Unity Boehm GC)</text>
  <text x="36" y="54" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">GC 전</text>
  <rect x="80" y="38" width="460" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="88" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="120" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">A</text>
  <rect x="160" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="192" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">B</text>
  <rect x="232" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="264" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">C</text>
  <rect x="304" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="336" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">D</text>
  <rect x="376" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="408" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">E</text>
  <rect x="448" y="44" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="480" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">F</text>
  <text x="280" y="86" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(B와 D는 더 이상 참조 안 됨)</text>
  <line x1="280" y1="94" x2="280" y2="114" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="280,118 276,110 284,110" fill="currentColor"/>
  <text x="36" y="142" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">GC 후</text>
  <rect x="80" y="126" width="460" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="88" y="132" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="120" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">A</text>
  <rect x="160" y="132" width="64" height="20" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="192" y="146" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">빈</text>
  <rect x="232" y="132" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="264" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">C</text>
  <rect x="304" y="132" width="64" height="20" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="336" y="146" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.45">빈</text>
  <rect x="376" y="132" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="408" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">E</text>
  <rect x="448" y="132" width="64" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="480" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">F</text>
  <line x1="192" y1="158" x2="192" y2="172" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <line x1="336" y1="158" x2="336" y2="172" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text x="264" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">빈 공간이 흩어져 있음 (단편화)</text>
</svg>
</div>

<br>

위 그림처럼 빈 공간이 흩어진 상태에서는, 전체 빈 공간이 충분해도 연속된 큰 블록이 없어서 큰 객체를 할당하지 못할 수 있습니다.
예를 들어 총 빈 공간이 10MB이지만 가장 큰 연속 빈 블록이 2MB인 경우, 5MB짜리 배열을 할당할 수 없습니다.

이 경우 Mono(또는 IL2CPP) 런타임이 OS에 새로운 메모리 블록을 요청하여 힙을 **확장(expand)**합니다. 기존 블록의 단편화된 빈 공간은 사용되지 못한 채 남으므로, 실제로 객체가 차지하는 메모리보다 힙 전체 크기가 커집니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">단편화로 인한 힙 확장</text>
  <text x="290" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">기존 힙 (총 빈 공간 10MB, 연속 최대 2MB)</text>
  <rect x="20" y="56" width="540" height="40" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="28" y="62" width="42" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="49" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">A</text>
  <rect x="76" y="62" width="70" height="28" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="111" y="80" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈 2MB</text>
  <rect x="152" y="62" width="42" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="173" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">C</text>
  <rect x="200" y="62" width="46" height="28" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="223" y="80" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈 1MB</text>
  <rect x="252" y="62" width="42" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="273" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">E</text>
  <rect x="300" y="62" width="94" height="28" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="347" y="80" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈 3MB</text>
  <rect x="400" y="62" width="42" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="421" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">G</text>
  <rect x="448" y="62" width="104" height="28" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="500" y="80" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈 4MB</text>
  <text x="290" y="116" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">5MB짜리 배열을 할당할 연속 공간이 없음</text>
  <line x1="290" y1="124" x2="290" y2="144" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,148 286,140 294,140" fill="currentColor"/>

  <!-- 힙 확장 후 -->
  <text x="290" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">힙 확장 후</text>

  <!-- 기존 블록 (단편화 그대로) -->
  <text x="290" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">기존 블록 (단편화 그대로)</text>
  <rect x="20" y="196" width="540" height="36" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="28" y="202" width="42" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="49" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">A</text>
  <rect x="76" y="202" width="70" height="24" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="111" y="218" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈</text>
  <rect x="152" y="202" width="42" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="173" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">C</text>
  <rect x="200" y="202" width="46" height="24" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="223" y="218" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈</text>
  <rect x="252" y="202" width="42" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="273" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">E</text>
  <rect x="300" y="202" width="94" height="24" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="347" y="218" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈</text>
  <rect x="400" y="202" width="42" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="421" y="218" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">G</text>
  <rect x="448" y="202" width="104" height="24" rx="4" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="500" y="218" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">빈</text>

  <!-- 새 블록 (별도 행) -->
  <text x="120" y="256" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">OS에서 별도로 할당한 새 블록</text>
  <rect x="20" y="264" width="160" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="286" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">5MB 배열</text>

  <!-- 하단 요약 -->
  <text x="290" y="320" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 기존 빈 공간 10MB는 여전히 단편화 상태로 낭비</text>
</svg>
</div>

<br>

한번 확장된 힙은 **줄어들지 않습니다.** 게임 초반에 대량의 객체를 생성했다가 해제해도, 힙 크기는 최대치를 유지합니다.

힙이 커지면 비세대 GC의 특성상 검사 범위도 함께 넓어져 GC 실행 시간이 길어집니다.

---

### 보수적(Conservative)

GC는 힙을 검사할 때 스택과 정적 변수 등에 저장된 각 값이 다른 객체를 가리키는 포인터인지, 단순한 정수인지 구분해야 합니다. 이를 위해 .NET 런타임의 GC는 타입 메타데이터를 참조하여 포인터의 위치를 정확히 파악하는데, 이 방식을 **정확한 GC(exact/precise GC)**라 합니다.

반면 Boehm GC는 원래 C/C++ 환경을 위해 설계되었기 때문에 이러한 타입 메타데이터가 없어, 포인터와 정수를 확실히 구분할 수 없습니다. 포인터가 아닌 값을 포인터로 잘못 판단하면 객체가 불필요하게 살아남지만, 반대로 실제 포인터를 놓치면 사용 중인 객체가 해제되어 치명적 오류가 발생합니다.
이 오류를 방지하기 위해 Boehm GC는 힙 주소 범위 안에 들어가는 값을 모두 **포인터로 간주**하며, 이 방식을 **보수적 GC(conservative GC)**라 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 제목 -->
  <text x="270" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">보수적 GC의 판단</text>
  <!-- 헤더 라벨 -->
  <text x="72" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">메모리 위치</text>
  <text x="210" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">저장된 값</text>
  <text x="420" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">GC의 판단</text>
  <!-- 구분선 -->
  <line x1="15" y1="60" x2="525" y2="60" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- 케이스 1: 실제 포인터 -->
  <rect x="15" y="72" width="115" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="72" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">0x1000</text>
  <rect x="150" y="72" width="125" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="212" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">0x00A0B4C0</text>
  <!-- 화살표 -->
  <line x1="280" y1="90" x2="310" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="310,86 318,90 310,94" fill="currentColor"/>
  <!-- 판단 박스 (실제 포인터) -->
  <rect x="322" y="68" width="205" height="76" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="424" y="88" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">힙 주소 범위 안</text>
  <text x="424" y="105" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">→ 포인터로 간주</text>
  <text x="424" y="122" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">→ 이 주소의 객체를</text>
  <text x="424" y="136" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">살아있다고 표시</text>
  <!-- 구분선 -->
  <line x1="15" y1="162" x2="525" y2="162" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.25"/>
  <!-- 케이스 2: 거짓 참조 -->
  <rect x="15" y="178" width="115" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="72" y="201" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">0x1008</text>
  <rect x="150" y="178" width="125" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="212" y="201" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">12345678</text>
  <!-- 화살표 -->
  <line x1="280" y1="196" x2="310" y2="196" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="310,192 318,196 310,200" fill="currentColor"/>
  <!-- 판단 박스 (거짓 참조 - 점선 테두리) -->
  <rect x="322" y="170" width="205" height="88" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="424" y="192" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">정수 값이지만</text>
  <text x="424" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">힙 주소 범위와 우연히 일치</text>
  <text x="424" y="230" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">→ 포인터로 오인할 수 있음</text>
  <text x="424" y="250" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(거짓 참조 — false reference)</text>
  <!-- 범례 -->
  <rect x="15" y="278" width="14" height="14" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="35" y="290" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">실제 포인터로 간주</text>
  <rect x="175" y="278" width="14" height="14" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="195" y="290" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">거짓 참조 가능성</text>
</svg>
</div>

<br>

위 그림의 두 번째 경우처럼 정수 값이 우연히 힙에 할당된 객체의 주소와 일치하면, GC가 포인터로 오인하여 아무도 참조하지 않는 객체가 해제되지 못할 수 있습니다.

이런 현상을 **거짓 참조(false reference)**라 하며, 거짓 참조에 의해 살아남은 객체는 불필요하게 메모리를 점유합니다.
한 건의 누수는 소량이지만, 장시간 실행되는 게임에서는 이러한 누수가 누적됩니다. 해제되지 못한 객체가 힙 곳곳에 남아 단편화를 악화시키고, 단편화로 인한 힙 확장과 비세대 특성이 맞물려 GC 실행 시간이 점점 늘어납니다.

| 특성 | 결과 |
|------|------|
| 비세대 (Non-generational) | 매번 전체 힙 검사 → 힙이 클수록 GC 실행 시간 증가 |
| 비압축 (Non-compacting) | 단편화 → 힙 확장 → 힙이 줄지 않음 |
| 보수적 (Conservative) | 포인터/정수 구분 불확실 → 일부 객체가 해제되지 못할 수 있음 |
| Stop-the-world | GC 실행 중 모든 스크립트 일시 정지 → 프레임 스파이크 |

이 특성들은 서로를 악화시킵니다. 보수적 방식이 일부 객체를 해제하지 못하면 단편화가 심해지고, 단편화가 힙을 확장시키면 비세대 특성 때문에 GC 실행 시간이 늘어납니다. 이 비용이 Stop-the-world 방식으로 메인 스레드에 집중되어, 플레이어에게는 **GC 스파이크**로 드러납니다.

---

## GC 스파이크: Stop-the-World Mark-and-Sweep

GC가 실행되면 모든 C# 스크립트의 실행이 멈춥니다. 힙을 검사하는 동안 스크립트가 객체를 생성하거나 참조를 변경하면 검사 결과가 정확하지 않을 수 있기 때문입니다.
검사가 끝날 때까지 스크립트를 일시 정지하는 이 방식을 **Stop-the-World**라 합니다.

Stop-the-world 상태에서 GC는 **Mark**와 **Sweep** 두 단계를 수행합니다.

---

### Mark 단계

GC는 **루트(root)**에서 출발합니다. 루트는 GC가 객체 탐색을 시작하는 진입점으로, 이 루트를 통해 도달할 수 있는 객체만 살아남습니다.

**GC 루트의 종류**

| 루트 종류 | 대상 |
|-----------|------|
| 스택 변수 | 현재 실행 중인 함수의 지역 변수 |
| 정적 필드 (static fields) | 클래스에 선언된 static 변수 |
| GC 핸들 (GC Handles) | 네이티브 코드와 공유되는 참조 |

스택 변수는 함수가 실행되는 동안만, 정적 필드는 앱이 실행되는 동안 항상, GC 핸들은 네이티브 코드가 C# 객체를 참조하는 동안 루트입니다.

GC는 각 루트에서 참조를 따라가며, 방문한 객체에 mark를 남깁니다. 이 과정을 모든 루트에 대해 반복하면 **도달 가능한(reachable)** 모든 객체가 표시됩니다.

다만 GC는 관리 코드(C#)만 스캔합니다. Unity 엔진(C++)이 MonoBehaviour의 `Update()`를 호출하거나 ScriptableObject를 관리하려면 해당 객체에 대한 참조가 필요한데, 이 참조는 C++ 쪽에 있으므로 GC에는 보이지 않습니다.
이를 방지하기 위해 Unity 엔진은 이런 참조를 GC 핸들로 등록합니다. GC 핸들은 루트이므로, GC가 해당 객체에도 mark를 남겨 수거하지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="20" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Mark 단계: 루트에서 힙으로의 참조 추적</text>
  <!-- === 루트 (힙 바깥) === -->
  <!-- 스택 변수 -->
  <rect x="20" y="40" width="96" height="28" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="59" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">스택 변수</text>
  <!-- 정적 필드 -->
  <rect x="306" y="40" width="96" height="28" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="354" y="59" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">정적 필드</text>
  <!-- 화살표: 스택 변수 → 객체A -->
  <line x1="68" y1="68" x2="68" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="68,100 64,92 72,92" fill="currentColor"/>
  <!-- 화살표: 정적 필드 → 객체D -->
  <line x1="354" y1="68" x2="354" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="354,100 350,92 358,92" fill="currentColor"/>
  <!-- === 관리 힙 === -->
  <rect x="20" y="104" width="580" height="52" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 객체A (mark) -->
  <rect x="30" y="114" width="76" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="135" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">A</text>
  <!-- 화살표: A → B -->
  <line x1="106" y1="130" x2="116" y2="130" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="116,127 122,130 116,133" fill="currentColor"/>
  <!-- 객체B (mark) -->
  <rect x="124" y="114" width="76" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="162" y="135" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">B</text>
  <!-- 화살표: B → C -->
  <line x1="200" y1="130" x2="210" y2="130" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="210,127 216,130 210,133" fill="currentColor"/>
  <!-- 객체C (mark) -->
  <rect x="218" y="114" width="76" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="256" y="135" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">C</text>
  <!-- 객체D (mark) -->
  <rect x="316" y="114" width="76" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="354" y="135" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">D</text>
  <!-- 객체E (도달 불가) -->
  <rect x="414" y="114" width="76" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="452" y="135" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.5">E</text>
  <!-- 객체F (도달 불가) -->
  <rect x="512" y="114" width="76" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="550" y="135" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.5">F</text>
  <!-- mark 라벨 -->
  <text x="68" y="165" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">mark</text>
  <text x="162" y="165" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">mark</text>
  <text x="256" y="165" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">mark</text>
  <text x="354" y="165" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">mark</text>
  <!-- 도달 불가 라벨 -->
  <text x="502" y="165" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.4">참조 없음</text>
  <!-- 관리 힙 라벨 -->
  <text x="310" y="180" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.45">관리 힙</text>
  <!-- 범례 -->
  <rect x="120" y="202" width="14" height="14" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="214" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">도달 가능 (mark)</text>
  <rect x="305" y="202" width="14" height="14" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="325" y="214" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">도달 불가 (수거 대상)</text>
</svg>
</div>

<br>

객체E와 객체F는 어떤 루트에서도 도달할 수 없으므로 mark가 남지 않으며, Sweep 단계의 수거 대상이 됩니다.

---

### Sweep 단계

Sweep 단계에서 GC는 힙의 모든 객체를 순회합니다. 각 객체에 mark가 있으면 건너뛰고, 없으면 해당 메모리를 해제하여 빈 공간으로 되돌립니다.

mark가 있어 해제되지 않은 객체가 영구적으로 보호되는 것은 아닙니다.
GC는 힙 공간이 부족해질 때마다 반복 실행되며, 매번 Mark와 Sweep을 처음부터 수행합니다. 이전 실행에서 살아남은 객체라도 코드에서 더 이상 참조하지 않으면 다음 실행에서 해제됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Sweep 단계</text>
  <!-- === Mark 후 힙 상태 === -->
  <text x="310" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">Mark 후 힙 상태</text>
  <rect x="20" y="60" width="580" height="52" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- A:mark -->
  <rect x="30" y="70" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="71" y="91" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">A:mark</text>
  <!-- B:mark -->
  <rect x="122" y="70" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="163" y="91" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">B:mark</text>
  <!-- C:mark -->
  <rect x="214" y="70" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="91" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">C:mark</text>
  <!-- D:mark -->
  <rect x="306" y="70" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="347" y="91" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">D:mark</text>
  <!-- E:없음 (점선) -->
  <rect x="398" y="70" width="92" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="444" y="91" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">E:없음</text>
  <!-- F:없음 (점선) -->
  <rect x="500" y="70" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="545" y="91" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">F:없음</text>
  <!-- 화살표: Mark 후 → Sweep 후 -->
  <line x1="310" y1="118" x2="310" y2="148" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <polygon points="310,148 306,140 314,140" fill="currentColor" opacity="0.4"/>
  <text x="340" y="137" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">Sweep 실행</text>
  <!-- === Sweep 후 힙 상태 === -->
  <text x="310" y="168" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">Sweep 후 힙 상태</text>
  <rect x="20" y="178" width="580" height="52" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- A -->
  <rect x="30" y="188" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="71" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">A</text>
  <!-- B -->
  <rect x="122" y="188" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="163" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">B</text>
  <!-- C -->
  <rect x="214" y="188" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">C</text>
  <!-- D -->
  <rect x="306" y="188" width="82" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="347" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">D</text>
  <!-- 빈 (E 해제) -->
  <rect x="398" y="188" width="92" height="32" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.4"/>
  <text x="444" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.45">빈</text>
  <!-- 빈 (F 해제) -->
  <rect x="500" y="188" width="90" height="32" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.4"/>
  <text x="545" y="209" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.45">빈</text>
  <!-- 화살표: 해제된 공간 표시 -->
  <line x1="444" y1="230" x2="444" y2="248" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="545" y1="230" x2="545" y2="248" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="444" y1="248" x2="545" y2="248" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text x="494" y="268" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">해제된 공간 (재사용 가능)</text>
</svg>
</div>

<br>

해제된 공간은 이후의 할당에서 재사용할 수 있습니다.
다만 Boehm GC는 비압축이므로, 해제된 공간이 살아남은 객체 사이에 남아 단편화가 발생할 수 있습니다.

---

### Stop-the-World의 비용

Mark와 Sweep이 실행되는 동안 모든 스크립트가 멈추므로, GC 소요 시간이 그대로 해당 프레임의 추가 비용이 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="300" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">60fps 기준 프레임 예산: 16.6ms</text>

  <!-- === 정상 프레임 (15ms) === -->
  <text fill="currentColor" x="10" y="58" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">정상</text>

  <!-- 스크립트 5ms: 기준 27ms=440px, 5ms→81px -->
  <rect x="100" y="40" width="81" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="140" y="55" text-anchor="middle" font-size="10" font-family="sans-serif">스크립트</text>
  <text fill="currentColor" x="140" y="68" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">5ms</text>

  <!-- 렌더링 10ms: 10ms→163px -->
  <rect x="181" y="40" width="163" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="262" y="55" text-anchor="middle" font-size="10" font-family="sans-serif">렌더링</text>
  <text fill="currentColor" x="262" y="68" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">10ms</text>

  <!-- 합계 15ms -->
  <text fill="currentColor" x="354" y="62" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.6">= 15ms</text>

  <!-- === GC 스파이크 프레임 (27ms) === -->
  <text fill="currentColor" x="10" y="128" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">GC 스파이크</text>

  <!-- 스크립트 5ms -->
  <rect x="100" y="110" width="81" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="140" y="125" text-anchor="middle" font-size="10" font-family="sans-serif">스크립트</text>
  <text fill="currentColor" x="140" y="138" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">5ms</text>

  <!-- GC 12ms: 12ms→196px, 진한 opacity -->
  <rect x="181" y="110" width="196" height="36" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="279" y="125" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">GC</text>
  <text fill="currentColor" x="279" y="138" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">12ms</text>

  <!-- 렌더링 10ms -->
  <rect x="377" y="110" width="163" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="458" y="125" text-anchor="middle" font-size="10" font-family="sans-serif">렌더링</text>
  <text fill="currentColor" x="458" y="138" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">10ms</text>

  <!-- 합계 27ms + 경고 마크 -->
  <text fill="currentColor" x="550" y="125" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">!</text>
  <text fill="currentColor" x="562" y="125" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.6">27ms</text>

  <!-- 16.6ms 예산 수직 점선: 100 + (16.6/27)*440 ≈ 370 -->
  <line x1="370" y1="30" x2="370" y2="158" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.45"/>
  <text fill="currentColor" x="370" y="175" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">▲ 16.6ms 예산</text>

  <!-- 예산 초과 구간 표시 -->
  <line x1="372" y1="155" x2="540" y2="155" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <text fill="currentColor" x="456" y="168" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.45">예산 초과 구간</text>
</svg>
</div>

<br>

위 예시에서 GC에 12ms가 소요되면 프레임 시간이 27ms로 늘어나 16.6ms 예산을 초과합니다. 프레임 드롭이 발생하고, 플레이어에게는 화면이 순간적으로 멈추는 **버벅거림(stutter)**으로 느껴집니다.

이 스파이크가 얼마나 클지는 힙 크기에 달려 있습니다. Boehm GC는 비세대 방식이므로, GC가 실행될 때마다 힙에 있는 모든 객체를 검사합니다. 힙에 객체가 많을수록 Mark에서 순회할 참조가 많아지고 Sweep에서 확인할 객체도 많아져, GC 소요 시간이 길어집니다.

힙이 작을 때는 GC가 수 ms 안에 끝날 수 있지만, 힙이 커질수록 수십 ms 이상 소요되어 프레임 예산을 초과하기도 합니다. 
모바일 기기는 데스크톱보다 CPU가 느리므로, 같은 힙 크기에서도 GC 시간이 더 길어집니다.

---

## GC가 트리거되는 시점

스파이크가 얼마나 클지는 힙 크기로 가늠할 수 있지만, 매 프레임 할당되는 객체의 양이 게임 상태에 따라 달라지므로 빈 공간이 언제 부족해질지는 예측하기 어렵습니다. 전투 중이든 컷씬 중이든 프레임이 끊길 수 있지만, 트리거 조건을 이해하면 GC 빈도 자체를 줄일 수 있습니다.

가장 일반적인 트리거 조건은 **힙 할당 실패**입니다.
새 객체를 힙에 할당할 때 빈 공간이 부족하면 GC가 실행됩니다. GC가 메모리를 해제한 뒤 할당을 재시도하고, 그래도 공간이 부족하면 힙이 확장됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">힙 할당과 GC 트리거 흐름</text>
  <!-- 1. new 객체 생성 -->
  <rect x="160" y="40" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="63" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">new 객체 생성</text>
  <!-- 화살표: 1 → 2 -->
  <line x1="260" y1="76" x2="260" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,96 256,88 264,88" fill="currentColor"/>
  <!-- 2. 빈 공간 탐색 (다이아몬드) -->
  <polygon points="260,100 360,140 260,180 160,140" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="260" y="138" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">빈 공간</text>
  <text x="260" y="152" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">충분한가?</text>
  <!-- 충분함 → 할당 완료 (오른쪽) -->
  <line x1="360" y1="140" x2="420" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="420,136 428,140 420,144" fill="currentColor"/>
  <rect x="432" y="122" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="472" y="145" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">할당 완료</text>
  <text x="390" y="132" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">충분</text>
  <!-- 부족함 → GC 실행 (아래쪽) -->
  <line x1="260" y1="180" x2="260" y2="204" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,204 256,196 264,196" fill="currentColor"/>
  <text x="280" y="198" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">부족</text>
  <!-- 3. GC 실행 -->
  <rect x="180" y="208" width="160" height="36" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="231" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">GC 실행</text>
  <!-- 화살표: 3 → 4 -->
  <line x1="260" y1="244" x2="260" y2="268" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,268 256,260 264,260" fill="currentColor"/>
  <!-- 4. 빈 공간 확보 (다이아몬드) -->
  <polygon points="260,272 360,312 260,352 160,312" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="260" y="310" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">빈 공간</text>
  <text x="260" y="324" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">충분한가?</text>
  <!-- 충분함 → 할당 완료 (오른쪽) -->
  <line x1="360" y1="312" x2="420" y2="312" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="420,308 428,312 420,316" fill="currentColor"/>
  <rect x="432" y="294" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="472" y="317" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">할당 완료</text>
  <text x="390" y="304" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">충분</text>
  <!-- 부족함 → 힙 확장 → 할당 완료 (아래쪽) -->
  <line x1="260" y1="352" x2="260" y2="368" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,368 256,360 264,360" fill="currentColor"/>
  <text x="280" y="365" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">부족</text>
  <rect x="180" y="372" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="395" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">힙 확장</text>
  <!-- 힙 확장 → 할당 완료 -->
  <line x1="280" y1="390" x2="420" y2="390" stroke="currentColor" stroke-width="1.5"/>
  <line x1="420" y1="390" x2="420" y2="335" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="416,335 420,327 424,335" fill="currentColor"/>
</svg>
</div>

<br>

매 프레임 힙 할당이 반복되면 GC도 자주 실행됩니다. `Update()`에서 `new`로 객체를 생성하거나 string을 연결하거나 LINQ 쿼리를 사용하면 힙이 빠르게 채워지고, 빈 공간이 부족해질 때마다 GC가 트리거됩니다.

반대로 힙 할당이 거의 없으면 GC도 거의 실행되지 않습니다. **오브젝트 풀링(Object Pooling)** 등으로 한 번 생성한 객체를 재사용하면 `new`에 의한 힙 할당이 줄어, 빈 공간이 부족해지는 빈도가 낮아지고 GC도 덜 실행됩니다.

---

## Incremental GC

GC 트리거 빈도를 줄이는 것이 근본적인 해결이지만, 한번 트리거된 스파이크의 크기도 줄일 수 있습니다. 기존 GC는 Mark-and-Sweep 전체를 한 프레임 안에서 완료하므로, 힙이 크면 큰 스파이크가 발생합니다.

Unity 2019.1부터 지원하는 **Incremental GC**는 이 작업을 **여러 프레임에 나누어** 수행합니다. 한 프레임에 정해진 시간만큼만 처리하고 나머지는 다음 프레임으로 넘겨, 한 프레임에 몰리는 GC 비용을 줄이는 방식입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="320" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">기존 GC vs Incremental GC</text>
  <!-- === 기존 GC === -->
  <text fill="currentColor" x="10" y="58" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">기존 GC</text>
  <!-- 프레임 1: 게임 로직 15ms -->
  <rect x="100" y="40" width="90" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="145" y="55" text-anchor="middle" font-size="10" font-family="sans-serif">게임 로직</text>
  <text fill="currentColor" x="145" y="68" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">15ms</text>
  <!-- GC 25ms -->
  <rect x="190" y="40" width="150" height="36" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="265" y="55" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">GC</text>
  <text fill="currentColor" x="265" y="68" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">25ms</text>
  <!-- 프레임 2: 게임 로직 15ms -->
  <rect x="340" y="40" width="90" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="385" y="55" text-anchor="middle" font-size="10" font-family="sans-serif">게임 로직</text>
  <text fill="currentColor" x="385" y="68" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">15ms</text>
  <!-- 프레임 드롭 경고 -->
  <text fill="currentColor" x="265" y="92" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">! 프레임 드롭</text>
  <!-- === Incremental GC === -->
  <text fill="currentColor" x="10" y="140" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">Incremental</text>
  <text fill="currentColor" x="10" y="153" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">GC</text>
  <!-- 프레임 1: 로직 10ms + GC 5ms -->
  <rect x="100" y="128" width="96" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <rect x="160" y="128" width="36" height="36" rx="0" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <rect x="100" y="128" width="96" height="36" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="130" y="143" text-anchor="middle" font-size="9" font-family="sans-serif">로직</text>
  <text fill="currentColor" x="130" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">10ms</text>
  <text fill="currentColor" x="178" y="143" text-anchor="middle" font-size="9" font-family="sans-serif">GC</text>
  <text fill="currentColor" x="178" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">5ms</text>
  <text fill="currentColor" x="148" y="178" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">15ms</text>
  <!-- 프레임 2 -->
  <rect x="206" y="128" width="96" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <rect x="266" y="128" width="36" height="36" rx="0" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <rect x="206" y="128" width="96" height="36" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="236" y="143" text-anchor="middle" font-size="9" font-family="sans-serif">로직</text>
  <text fill="currentColor" x="236" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">10ms</text>
  <text fill="currentColor" x="284" y="143" text-anchor="middle" font-size="9" font-family="sans-serif">GC</text>
  <text fill="currentColor" x="284" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">5ms</text>
  <text fill="currentColor" x="254" y="178" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">15ms</text>
  <!-- 프레임 3 -->
  <rect x="312" y="128" width="96" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <rect x="372" y="128" width="36" height="36" rx="0" fill="currentColor" fill-opacity="0.12" stroke="none"/>
  <rect x="312" y="128" width="96" height="36" rx="5" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="342" y="143" text-anchor="middle" font-size="9" font-family="sans-serif">로직</text>
  <text fill="currentColor" x="342" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">10ms</text>
  <text fill="currentColor" x="390" y="143" text-anchor="middle" font-size="9" font-family="sans-serif">GC</text>
  <text fill="currentColor" x="390" y="155" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">5ms</text>
  <text fill="currentColor" x="360" y="178" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">15ms</text>
  <!-- ... -->
  <text fill="currentColor" x="422" y="150" text-anchor="start" font-size="13" font-family="sans-serif" opacity="0.5">...</text>
  <text fill="currentColor" x="450" y="150" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">(예산 이내)</text>
  <!-- 16.6ms 예산 점선 (기존 GC 행) -->
  <line x1="200" y1="34" x2="200" y2="82" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.35"/>
  <text fill="currentColor" x="200" y="103" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.4">16.6ms</text>
  <!-- 16.6ms 예산 점선 (Incremental GC 행) -->
  <line x1="200" y1="122" x2="200" y2="170" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.35"/>
  <text fill="currentColor" x="200" y="196" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.4">16.6ms</text>
</svg>
</div>

<br>

위 예시에서 GC 총 작업량은 25ms로 동일하지만, 5ms씩 여러 프레임에 나누어 처리하므로 큰 스파이크를 피할 수 있습니다.

다만 Incremental GC가 프레임 드롭을 완전히 제거하는 것은 아닙니다.
게임 로직이 이미 프레임 예산에 가깝다면 나누어 처리하는 GC 작업이 더해져 예산을 초과할 수 있고, GC 작업 중 나눌 수 없는 단계가 있어 해당 프레임에서 스파이크가 발생할 수도 있습니다.

---

### Incremental GC의 동작 원리

GC 작업을 여러 프레임에 나누면, 프레임 사이에 게임이 계속 실행되면서 두 가지 과제가 생깁니다.

첫 번째는 **진행 상태 보존**입니다.
Mark 단계를 중간에 끊었다가 다음 프레임에서 이어가려면, "어디까지 검사했는지"를 기억해야 합니다.
Incremental GC는 검사 위치를 내부 자료구조에 저장해 두었다가, 다음 프레임에서 그 지점부터 재개합니다.

두 번째는 **참조 변경 추적**입니다.
GC가 쉬는 동안 스크립트가 객체의 참조 필드를 바꾸면, 이미 검사한 결과가 틀어질 수 있습니다.
예를 들어, GC가 프레임 N에서 객체 A를 방문하고 mark를 남겼는데, 프레임 N+1에서 스크립트가 A의 참조 필드를 객체 B(아직 mark되지 않은 새 객체)로 바꿀 수 있습니다.
GC는 A를 이미 방문했으므로 다시 확인하지 않고, B는 mark되지 않은 채 수거 대상이 됩니다.

Incremental GC는 **쓰기 장벽(write barrier)**으로 이 참조 변경 추적 과제를 해결합니다. 스크립트가 A의 참조를 B로 바꾸면, 쓰기 장벽이 이 변경을 자동으로 기록합니다. GC가 다음 프레임에서 작업을 재개할 때 이 기록을 먼저 확인하여 B에도 mark를 남기므로, B가 잘못 수거되는 것을 방지합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="290" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Incremental GC: 프레임별 분산 실행</text>
  <!-- === 프레임 N === -->
  <text fill="currentColor" x="10" y="55" text-anchor="start" font-size="10" font-weight="bold" font-family="sans-serif">프레임 N</text>
  <!-- 스크립트 -->
  <rect x="90" y="38" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="140" y="58" text-anchor="middle" font-size="10" font-family="sans-serif">스크립트</text>
  <!-- Mark 일부 (2ms) -->
  <rect x="190" y="38" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="230" y="52" text-anchor="middle" font-size="9" font-family="sans-serif">Mark 일부</text>
  <text fill="currentColor" x="230" y="64" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2ms</text>
  <!-- 화살표 + 라벨 -->
  <line x1="280" y1="54" x2="310" y2="54" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="310,54 304,50 304,58" fill="currentColor"/>
  <text fill="currentColor" x="400" y="58" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">진행 상태 저장</text>
  <!-- === 프레임 N+1 === -->
  <text fill="currentColor" x="10" y="110" text-anchor="start" font-size="10" font-weight="bold" font-family="sans-serif">프레임 N+1</text>
  <!-- 스크립트 -->
  <rect x="90" y="93" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="140" y="113" text-anchor="middle" font-size="10" font-family="sans-serif">스크립트</text>
  <!-- Mark 계속 + 쓰기 장벽 -->
  <rect x="190" y="93" width="140" height="32" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="107" text-anchor="middle" font-size="9" font-family="sans-serif">Mark 계속 + 쓰기 장벽 반영</text>
  <text fill="currentColor" x="260" y="119" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2ms</text>
  <!-- 화살표 + 라벨 -->
  <line x1="340" y1="109" x2="370" y2="109" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,109 364,105 364,113" fill="currentColor"/>
  <text fill="currentColor" x="440" y="113" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">진행 상태 저장</text>
  <!-- === ... === -->
  <text fill="currentColor" x="165" y="155" text-anchor="middle" font-size="13" font-family="sans-serif" opacity="0.4">...</text>
  <!-- === 프레임 N+K === -->
  <text fill="currentColor" x="10" y="195" text-anchor="start" font-size="10" font-weight="bold" font-family="sans-serif">프레임 N+K</text>
  <!-- 스크립트 -->
  <rect x="90" y="178" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="140" y="198" text-anchor="middle" font-size="10" font-family="sans-serif">스크립트</text>
  <!-- Sweep (2ms) -->
  <rect x="190" y="178" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="230" y="192" text-anchor="middle" font-size="9" font-family="sans-serif">Sweep</text>
  <text fill="currentColor" x="230" y="204" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2ms</text>
</svg>
</div>

---

### Incremental GC의 한계

Incremental GC는 스파이크의 크기를 줄여 주지만, 근본적인 해결책은 아닙니다.

우선, 쓰기 장벽이 모든 참조 변경마다 기록 작업을 수행하므로 **총 GC 시간은 줄어들지 않고 오히려 약간 늘어납니다.**
큰 스파이크 하나가 사라지는 대신 매 프레임 수 ms의 GC 비용이 꾸준히 발생하고, 프레임 예산이 빠듯한 상황에서는 이 비용도 부담이 됩니다.

또한, GC가 여러 프레임에 걸쳐 작업하는 동안에도 스크립트는 계속 새로운 객체를 할당합니다. **해제 속도보다 할당 속도가 빠르면** GC가 따라잡지 못하고, 결국 한 번에 많은 작업을 처리해야 하는 상황이 돌아옵니다.

Incremental GC를 활성화하더라도, 할당 자체를 줄이지 않으면 이 한계는 그대로 남습니다.

---

### Incremental GC 활성화 방법

Unity 에디터의 **Project Settings > Player > Other Settings > Configuration**에서 **Use Incremental GC** 체크박스로 설정할 수 있으며, Unity 2021 LTS 이후 버전에서는 기본으로 활성화되어 있습니다.

---

## GC.Collect() 수동 호출

Incremental GC로 스파이크를 분산하더라도, 힙 공간이 부족해지는 시점은 실행 중 할당 패턴에 따라 달라지므로 GC가 언제 트리거될지 예측하기 어렵습니다. `System.GC.Collect()`를 호출하면 원하는 시점에 GC를 직접 트리거할 수 있습니다.

수동 호출의 목적은 **GC 스파이크를 예측 가능한 시점으로 옮기는 것**입니다. 예를 들어, 전투 중에 GC가 갑자기 실행되어 프레임이 끊기는 것보다 로딩 화면처럼 플레이어가 프레임 드롭을 인지하지 못하는 시점에 미리 실행하는 편이 낫습니다.

**GC.Collect()의 적절한 호출 시점**

| 구분 | 시점 |
|------|------|
| 적합 | 로딩 화면, 씬 전환, 일시 정지 화면, 컷씬, 라운드/스테이지 종료 후 |
| 부적합 | 게임플레이 중, 실시간 멀티플레이 중, 타이밍이 중요한 애니메이션 중 |

<br>

씬 전환 직후는 대표적인 호출 시점입니다. `SceneManager.UnloadSceneAsync()`로 이전 씬을 언로드하면 많은 객체가 참조를 잃는데, 이때 `GC.Collect()`를 호출하면 해당 객체들의 메모리를 바로 회수할 수 있습니다.
로딩 화면이 표시되는 동안 실행하면 GC 스파이크가 플레이어에게 체감되지 않고, 새 씬이 시작될 때 힙에 여유가 확보되어 초반에 GC가 다시 트리거될 가능성도 낮아집니다.

```csharp
async void LoadNextScene()
{
    loadingScreen.SetActive(true);
    await SceneManager.UnloadSceneAsync(currentScene);

    System.GC.Collect(); // 로딩 화면 중이므로 스파이크가 체감되지 않음

    await SceneManager.LoadSceneAsync(nextScene);
    loadingScreen.SetActive(false);
}
```

반대로, 게임플레이 중에 `GC.Collect()`를 호출하면 GC가 완료될 때까지 스크립트가 멈추므로 프레임 드롭이 플레이어에게 그대로 느껴집니다. 게임플레이 도중의 GC 문제는 할당 자체를 줄여서 해결해야 합니다.

---

## Profiler에서 GC 할당 확인하기

GC 문제를 해결하려면 먼저 힙 할당이 어디서 발생하는지 찾아야 합니다.
Unity Profiler의 CPU Usage 모듈에서 **GC Alloc** 컬럼을 보면 각 함수가 프레임마다 얼마나 할당하는지 확인할 수 있습니다.

GC Alloc 값이 0이 아닌 함수는 해당 프레임에서 관리 힙에 메모리를 할당한 것입니다.
Update()처럼 매 프레임 실행되는 함수는 대부분 기존 데이터를 다루므로 새로운 힙 할당이 필요하지 않습니다. 그런데 GC Alloc이 매 프레임 반복적으로 나타난다면, 코드 안에 의도하지 않은 힙 할당이 숨어 있을 가능성이 높습니다.

---

### 숨은 할당의 대표적 사례

GC Alloc을 일으키는 함수를 찾았다면, 그 안에서 어떤 코드가 할당을 만드는지 좁혀야 합니다.
string 연결, 박싱, LINQ, 클로저 등은 `new` 키워드 없이도 힙 할당을 일으키는 대표적인 패턴입니다.
각 패턴의 메커니즘과 대안은 [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서 다룹니다.

게임플레이 중 핵심 루프(Update, FixedUpdate, LateUpdate)에서 GC Alloc을 0B에 가깝게 유지할수록 GC 트리거 빈도가 낮아지고, 스파이크도 줄어듭니다.

---

## GC 문제 해결의 전체 전략

GC 문제의 해결 전략은 세 계층으로 나뉩니다.
할당을 줄이는 것이 근본 해결이고, 스파이크를 분산하는 것이 증상 완화이며, 힙 크기를 관리하는 것이 간접적인 보완입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <!-- 제목 -->
  <text x="320" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GC 문제 해결의 세 계층</text>
  <!-- 3계층 (최상단, 가장 작음) — 간접 효과 -->
  <polygon points="230,48 410,48 440,118 200,118" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="320" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 힙 크기를 관리한다</text>
  <text x="320" y="83" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(간접 효과)</text>
  <text x="320" y="100" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">대량 할당 패턴 제거, 씬 전환 시 불필요한 참조 정리,</text>
  <text x="320" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">정적 필드 참조 누수 점검</text>
  <!-- 2계층 (중간) — 증상 완화 -->
  <polygon points="200,122 440,122 480,202 160,202" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="320" y="145" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. GC 스파이크를 분산한다</text>
  <text x="320" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(증상 완화)</text>
  <text x="320" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Incremental GC 활성화,</text>
  <text x="320" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">로딩/전환 시점에 GC.Collect() 수동 호출</text>
  <!-- 1계층 (최하단, 가장 큼) — 근본 해결 -->
  <polygon points="160,206 480,206 520,296 120,296" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <text x="320" y="229" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 할당 자체를 줄인다</text>
  <text x="320" y="244" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(근본 해결)</text>
  <text x="320" y="262" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">풀링, string 캐싱, 박싱/LINQ 제거, struct 활용,</text>
  <text x="320" y="274" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">매 프레임 할당 코드 제거</text>
  <!-- 우선순위 화살표 (좌측) -->
  <line x1="95" y1="280" x2="95" y2="65" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <polygon points="95,60 91,70 99,70" fill="currentColor" opacity="0.4"/>
  <text x="90" y="175" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4" transform="rotate(-90, 90, 175)">우선순위</text>
</svg>
</div>

<br>

1계층이 가장 효과적입니다.
할당이 줄면 힙이 느리게 차므로 GC가 덜 자주 트리거되고, 힙 크기도 작게 유지되어 비세대 GC의 "힙이 클수록 느려지는" 문제까지 완화됩니다.

할당을 충분히 줄인 뒤에도 남는 GC 비용은 2계층으로 관리합니다.
Incremental GC로 스파이크를 분산하고, `GC.Collect()`로 시점을 제어합니다.

3계층에서는 힙에 불필요하게 남아 있는 객체를 정리합니다.
예를 들어, 씬이 전환된 뒤에도 이전 씬의 데이터를 참조하는 정적 변수가 남아 있으면 GC가 해당 데이터를 해제하지 못해 힙에 계속 남습니다. 이런 참조를 정리하면 GC가 더 많은 메모리를 회수할 수 있고, 힙 크기가 줄어듭니다.

---

## 관리 힙 너머의 메모리

관리 힙은 C# 객체의 메모리일 뿐, Unity에서 사용하는 메모리의 전부가 아닙니다.

텍스처, 메쉬, 오디오 클립, 셰이더 같은 에셋은 관리 힙이 아니라 **네이티브 메모리(Native Memory)**에 로드됩니다.
네이티브 메모리는 C# 런타임이 아니라 Unity 엔진의 C++ 코드가 관리하는 메모리 영역입니다.

실제로 대부분의 게임에서 네이티브 메모리는 관리 힙보다 훨씬 큽니다.
텍스처 하나가 수 MB에서 수십 MB를 차지하므로, 관리 힙이 50MB인 게임에서도 네이티브 메모리는 200~300MB에 달할 수 있습니다.

이 네이티브 메모리의 구조, 에셋의 생명주기(로드/언로드), 메모리 프로파일러를 활용한 진단 방법은 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 보다 자세하게 다룹니다.

---

## 마무리

Unity의 Boehm GC는 비세대, 비압축 특성으로 GC 스파이크가 발생하기 쉽고, 보수적 스캔 방식은 회수 가능한 메모리를 놓쳐 힙을 불필요하게 키울 수 있습니다.

- GC는 Mark(도달 가능한 객체 표시)와 Sweep(표시되지 않은 객체 해제) 두 단계로 동작하며, 전체 과정 동안 스크립트 실행이 멈춥니다(Stop-the-World).
- 비세대 특성 때문에 매번 전체 힙을 검사하므로, 힙이 클수록 GC 시간이 길어집니다.
- 비압축 특성 때문에 해제된 공간이 단편화되고, 힙이 확장되며, 한번 확장된 힙은 줄어들지 않습니다.
- Incremental GC는 GC 작업을 여러 프레임에 분산하여 스파이크를 줄이지만, 총 GC 시간은 같거나 약간 증가합니다.
- GC.Collect()는 로딩 화면이나 씬 전환처럼 플레이어가 프레임 드롭을 체감하지 못하는 시점에 호출합니다.
- Profiler의 GC Alloc 컬럼에서 매 프레임 0이 아닌 값이 나타나면, 의도하지 않은 힙 할당이 존재합니다.

이러한 구조적 한계 때문에, 할당을 줄여 GC 트리거 자체를 억제하는 것이 근본적인 해결 방법이고, Incremental GC와 수동 호출은 그 위에 얹는 보조 수단입니다.

이 글에서는 관리 힙만 다루었지만, 대부분의 게임에서 네이티브 메모리는 관리 힙보다 훨씬 큽니다.
GC 할당을 줄이는 것만으로 메모리 문제가 해결되지 않는다면 네이티브 메모리를 살펴야 합니다. [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 이어집니다.

---

**관련 글**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)

**시리즈**
- **메모리 관리 (1) - 가비지 컬렉션의 원리** (현재 글)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)

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
- **메모리 관리 (1) - 가비지 컬렉션의 원리** (현재 글)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
