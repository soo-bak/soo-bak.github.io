---
layout: single
title: "C# 런타임 기초 (2) - .NET 런타임과 IL2CPP - soo:bak"
date: "2026-02-28 01:48:00 +0900"
description: C# 컴파일 과정, IL, JIT vs AOT, Mono와 IL2CPP 비교, 플랫폼별 제약을 설명합니다.
tags:
  - Unity
  - C#
  - IL2CPP
  - Mono
  - 모바일
---

## 타입 시스템에서 실행 환경으로

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서는 값 타입과 참조 타입이 메모리에 놓이는 방식과, 그 차이가 GC 비용으로 이어지는 이유를 살펴봤습니다. 다만 그 코드가 실제로 실행되기까지 어떤 단계를 거치는지는 다루지 않았습니다.

작성한 C# 코드는 CPU가 곧바로 실행할 수 있는 형태가 아닙니다. 소스는 먼저 **IL(Intermediate Language)**이라는 중간 표현으로 컴파일되고, 이 IL을 기계어로 바꿔 실제로 실행하는 일은 별도의 계층이 맡습니다. 이 계층을 **런타임 시스템(Runtime System)**이라고 부릅니다.

런타임 시스템이 IL을 언제, 어떤 방식으로 기계어로 바꾸느냐는 한 가지로 정해져 있지 않습니다. 실행 도중에 변환할 수도 있고, 빌드할 때 미리 네이티브 코드로 만들어 둘 수도 있습니다. 이 선택은 빌드 속도와 실행 성능을 좌우하며, iOS처럼 실행 중 코드 생성을 제한하는 플랫폼에서는 특정 방식이 아예 허용되지 않기도 합니다.

Unity는 이 변환을 주로 두 방식으로 처리합니다. 하나는 실행 시점에 IL을 기계어로 변환하는 **Mono(JIT)**이고, 다른 하나는 빌드 시점에 IL을 C++로 변환한 뒤 네이티브 코드로 컴파일하는 **IL2CPP(AOT)**입니다.

이번 글에서는 Mono와 IL2CPP가 IL을 기계어로 바꾸는 과정을 각각 따라가며, 그 차이가 빌드 속도와 실행 성능, 플랫폼 제약에서 어떻게 드러나는지 살펴봅니다.

---

## C# 컴파일 과정

C#으로 작성한 코드는 실행 전에 컴파일을 거칩니다. 소스를 곧바로 기계어로 번역하는 C++ 컴파일러와 달리, C# 컴파일러 **Roslyn**은 소스를 IL로 변환합니다. 이렇게 만들어진 IL은 CIL(Common Intermediate Language)이나 MSIL(Microsoft Intermediate Language)이라고도 불립니다.

IL은 특정 CPU나 OS에 묶이지 않는 중간 표현이라, CPU가 직접 실행하지 못합니다. 실제로 실행하려면 먼저 기계어로 변환되어야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Box 1: C# 소스 코드 -->
  <rect x="120" y="8" width="240" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="240" y="29" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">C# 소스 코드</text>
  <text fill="currentColor" x="240" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(.cs 파일)</text>
  <text fill="currentColor" x="375" y="36" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">개발자가 작성</text>
  <!-- Arrow 1 -->
  <line x1="240" y1="58" x2="240" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,125 235,117 245,117" fill="currentColor"/>
  <text fill="currentColor" x="255" y="78" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.7">C# 컴파일러 (Roslyn)</text>
  <text fill="currentColor" x="255" y="94" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">구문 분석 → 의미 분석 → IL 생성</text>
  <!-- Box 2: IL 바이트코드 -->
  <rect x="120" y="130" width="240" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="240" y="151" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">IL 바이트코드</text>
  <text fill="currentColor" x="240" y="168" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(.dll 파일)</text>
  <text fill="currentColor" x="375" y="148" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">플랫폼 독립적</text>
  <text fill="currentColor" x="375" y="162" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">중간 코드</text>
  <!-- Arrow 2 -->
  <line x1="240" y1="180" x2="240" y2="242" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,247 235,239 245,239" fill="currentColor"/>
  <text fill="currentColor" x="255" y="202" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.7">여기서부터 방식이 갈라짐</text>
  <text fill="currentColor" x="255" y="218" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">(JIT 또는 AOT)</text>
  <!-- Box 3: 기계어 -->
  <rect x="120" y="252" width="240" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="240" y="273" text-anchor="middle" font-size="14" font-weight="bold" font-family="sans-serif">기계어</text>
  <text fill="currentColor" x="240" y="290" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">(네이티브 코드)</text>
  <text fill="currentColor" x="375" y="270" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">CPU가 직접 실행</text>
  <text fill="currentColor" x="375" y="284" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">플랫폼 종속적</text>
</svg>
</div>

<br>

C#이 IL 단계를 거치는 이유는 .NET의 **플랫폼 독립성**에 있습니다.

플랫폼마다 CPU 아키텍처와 실행 파일 형식이 다르므로, 최종 기계어도 플랫폼별로 달라져야 합니다. 이런 차이에 대응하기 위해, C#은 플랫폼과 무관한 IL까지만 만들고, 이 IL을 기계어로 바꾸는 일은 각 플랫폼의 런타임에 맡깁니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Top box: C# 소스 코드 -->
  <rect x="155" y="5" width="190" height="36" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="250" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">하나의 C# 소스 코드</text>
  <!-- Arrow to IL -->
  <line x1="250" y1="41" x2="250" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="250,68 245,60 255,60" fill="currentColor"/>
  <!-- IL box -->
  <rect x="185" y="73" width="130" height="36" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="250" y="96" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">하나의 IL</text>
  <!-- Fan-out: vertical stem -->
  <line x1="250" y1="109" x2="250" y2="132" stroke="currentColor" stroke-width="1.5"/>
  <!-- Horizontal bar -->
  <line x1="90" y1="132" x2="410" y2="132" stroke="currentColor" stroke-width="1.5"/>
  <!-- Left branch -->
  <line x1="90" y1="132" x2="90" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="90,163 85,155 95,155" fill="currentColor"/>
  <!-- Center branch -->
  <line x1="250" y1="132" x2="250" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="250,163 245,155 255,155" fill="currentColor"/>
  <!-- Right branch -->
  <line x1="410" y1="132" x2="410" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="410,163 405,155 415,155" fill="currentColor"/>
  <!-- Bottom boxes -->
  <rect x="22" y="168" width="136" height="46" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="90" y="187" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">x86 기계어</text>
  <text fill="currentColor" x="90" y="204" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(Windows)</text>
  <rect x="182" y="168" width="136" height="46" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="250" y="187" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">ARM 기계어</text>
  <text fill="currentColor" x="250" y="204" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(iOS/Android)</text>
  <rect x="342" y="168" width="136" height="46" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="410" y="187" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">기타 기계어</text>
  <text fill="currentColor" x="410" y="204" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(WebGL 등)</text>
</svg>
</div>

<br>

IL은 **평가 스택(Evaluation Stack)**이라는 임시 공간을 사용하는 명령어 집합입니다. 계산에 쓸 값을 이 스택에 올려 두고, 명령어가 스택에서 값을 꺼내 처리한 다음 그 결과를 다시 스택에 올리는 방식으로 동작합니다. 평가 스택은 명령어 사이에서 값을 주고받는 논리적 공간으로, 물리적인 CPU 레지스터와 달리 실제 하드웨어로 존재하지는 않습니다.

다음은 두 정수를 더해 돌려주는 간단한 메서드입니다.

<br>

```csharp
static int Add(int a, int b)
{
    return a + b;
}
```

이 메서드를 릴리스 빌드로 컴파일하면 다음과 같은 IL이 만들어집니다.

```
ldarg.0
ldarg.1
add
ret
```

> 디버그 빌드라면 디버깅을 돕는 명령어가 몇 개 더 붙어 이보다 길어집니다.


<br>

IL 명령어는 수행할 동작을 가리키는 **opcode(연산 코드)**와, 경우에 따라 그 동작이 다룰 **피연산자(operand)**로 이뤄집니다. `ldarg.0`은 opcode `ldarg`(인자를 읽어 스택에 올리는 동작)와 피연산자 `0`(몇 번째 인자인지)으로 나뉘고, `add`처럼 피연산자 없이 opcode만으로 끝나는 명령어도 있습니다.

`ldarg.0`과 `ldarg.1`은 첫 번째 인자 `a`와 두 번째 인자 `b`를 차례로 스택에 올립니다. 그러면 스택에는 두 값이 `a`, `b` 순으로 쌓입니다. `add`는 이 두 값을 꺼내 더한 다음 그 합을 다시 스택에 올리므로, 스택에는 `a + b` 하나만 남습니다. 마지막으로 `ret`이 그 값을 호출자에게 돌려줍니다.

> `ldarg.0`이 인자 `a`를 가리키는 것은 `Add`가 정적 메서드이기 때문입니다. 인스턴스 메서드였다면 `ldarg.0`은 `this`를 가리키고, `a`와 `b`는 각각 `ldarg.1`과 `ldarg.2`로 밀려납니다.

이처럼 IL은 계산 과정을 평가 스택의 흐름으로 표현할 뿐, CPU가 그대로 실행하지는 못합니다. 런타임이나 AOT 컴파일러는 이 스택 기반 흐름을 읽어, 각 값을 실제 레지스터와 메모리에 배치하면서 기계어로 옮깁니다. 그리고 이 변환을 **언제** 하느냐에 따라 **JIT(Just-In-Time)**와 **AOT(Ahead-Of-Time)**로 나뉩니다.

---

## JIT 컴파일 — Mono 런타임

IL을 실행 중에 기계어로 변환하는 방식을 **JIT(Just-In-Time) 컴파일**이라고 합니다. Unity에서 Mono 런타임은 이 JIT 방식을 사용합니다.

JIT 변환은 보통 메서드 단위로 이뤄집니다.

어떤 메서드가 처음 호출되면 Mono는 그 메서드의 IL을 읽어 기계어로 변환합니다. 변환된 기계어는 메모리에 캐시되므로, 같은 메서드를 다시 호출할 때는 변환 과정을 반복하지 않고 캐시된 기계어를 실행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text fill="currentColor" x="310" y="16" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">메서드 A 첫 호출</text>
  <!-- Box 1: IL 바이트코드 -->
  <rect x="10" y="28" width="140" height="46" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="80" y="48" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">IL 바이트코드</text>
  <text fill="currentColor" x="80" y="64" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(메서드 A)</text>
  <!-- Arrow 1 -->
  <line x1="150" y1="51" x2="180" y2="51" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="185,51 177,46 177,56" fill="currentColor"/>
  <!-- Box 2: JIT 컴파일러 -->
  <rect x="190" y="28" width="160" height="46" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="270" y="48" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">JIT 컴파일러</text>
  <text fill="currentColor" x="270" y="64" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">IL → 기계어 변환</text>
  <!-- Arrow 2 -->
  <line x1="350" y1="51" x2="380" y2="51" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="385,51 377,46 377,56" fill="currentColor"/>
  <!-- Box 3: 기계어 (캐시) -->
  <rect x="390" y="28" width="130" height="46" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="455" y="48" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">기계어</text>
  <text fill="currentColor" x="455" y="64" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(캐시 저장)</text>
  <!-- Arrow to 실행 -->
  <line x1="520" y1="51" x2="555" y2="51" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="560,51 552,46 552,56" fill="currentColor"/>
  <text fill="currentColor" x="580" y="55" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">실행</text>
  <!-- Cache feedback arrow (curved) -->
  <line x1="455" y1="74" x2="455" y2="130" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <line x1="455" y1="130" x2="312" y2="130" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <polygon points="307,130 315,125 315,135" fill="currentColor"/>
  <!-- Feedback label -->
  <text fill="currentColor" x="310" y="110" text-anchor="end" font-size="11" font-family="sans-serif" opacity="0.6">메서드 A 두 번째 호출</text>
  <text fill="currentColor" x="200" y="148" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.7">캐시된 기계어 직접 실행</text>
  <text fill="currentColor" x="200" y="164" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">(변환 과정 없음)</text>
</svg>
</div>

<br>

JIT는 기계어 변환을 빌드가 아니라 실행 시점으로 미룹니다. 변환을 이렇게 미루기 때문에 JIT는 빌드 속도, 첫 호출 비용, 최적화 수준, 플랫폼 호환성에서 AOT와 차이를 보입니다.

먼저 빌드가 빠릅니다. 빌드 시점에는 IL까지만 만들면 되고 기계어 변환은 실행할 때로 넘어가므로, 코드를 고치고 결과를 확인하는 반복 주기가 짧아집니다. Unity 에디터에서 Play 모드가 비교적 빨리 시작되는 것도 같은 이유에서입니다.

대신 메서드를 처음 호출할 때는 변환 비용이 따릅니다. 그 메서드를 실행하기 전에 IL을 기계어로 변환하는 과정을 한 번 거쳐야 하기 때문입니다. 게임을 시작한 직후나 새 씬을 불러온 직후처럼 많은 메서드가 한꺼번에 처음 불리는 구간에서는 이 변환 비용이 고스란히 그 프레임 시간에 더해집니다. 다만 한 번 변환한 메서드는 캐시에 남으므로, 같은 메서드를 다시 호출할 때는 변환을 거치지 않아 이 비용이 다시 들지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Labels -->
  <text fill="currentColor" x="20" y="18" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">프레임 시간 (ms)</text>
  <rect x="386" y="9" width="12" height="8" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="404" y="17" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">일반 실행</text>
  <rect x="474" y="9" width="12" height="8" rx="2" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="492" y="17" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">JIT 변환 비용</text>

  <!-- Axes -->
  <line x1="70" y1="34" x2="70" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <line x1="70" y1="230" x2="570" y2="230" stroke="currentColor" stroke-width="1.5"/>

  <!-- Reference lines -->
  <line x1="70" y1="150" x2="570" y2="150" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3" opacity="0.5"/>
  <text fill="currentColor" x="64" y="154" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.6">16.6</text>
  <text fill="currentColor" x="562" y="144" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.55">60fps 예산</text>
  <line x1="70" y1="70" x2="570" y2="70" stroke="currentColor" stroke-width="1" stroke-dasharray="3,4" opacity="0.22"/>
  <text fill="currentColor" x="64" y="74" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.45">33.3</text>
  <text fill="currentColor" x="64" y="234" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.45">0</text>

  <!-- Frame bars: base execution plus optional JIT overhead -->
  <rect x="100" y="178" width="42" height="52" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <rect x="100" y="58" width="42" height="120" rx="3" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="121" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">1</text>

  <rect x="160" y="174" width="42" height="56" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="181" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">2</text>

  <rect x="220" y="170" width="42" height="60" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="241" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">3</text>

  <rect x="280" y="176" width="42" height="54" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="301" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">4</text>

  <rect x="340" y="172" width="42" height="58" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <rect x="340" y="96" width="42" height="76" rx="3" fill="currentColor" fill-opacity="0.28" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="361" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">5</text>

  <rect x="400" y="173" width="42" height="57" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="421" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">6</text>

  <rect x="460" y="177" width="42" height="53" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="481" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">7</text>

  <rect x="520" y="171" width="42" height="59" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="541" y="244" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">8</text>

  <!-- Annotations -->
  <text fill="currentColor" x="150" y="54" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">시작 직후 첫 호출 집중</text>
  <line x1="145" y1="58" x2="129" y2="76" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <polygon points="125,81 127,72 134,78" fill="currentColor" opacity="0.55"/>

  <text fill="currentColor" x="391" y="94" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">새 씬/코드 경로</text>
  <line x1="386" y1="98" x2="372" y2="112" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <polygon points="368,117 370,108 377,114" fill="currentColor" opacity="0.55"/>

  <text fill="currentColor" x="320" y="258" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">프레임</text>
  <text fill="currentColor" x="70" y="282" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">JIT 비용은 메서드 첫 호출 시점에 붙음: 시작 직후, 새 씬 로드, 새 코드 경로 진입</text>
  <text fill="currentColor" x="70" y="298" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">이미 변환된 메서드는 캐시된 기계어를 실행하므로 같은 비용이 반복되지 않음</text>
</svg>
</div>

<br>

기계어의 최적화 수준도 낮은 편입니다. 인라이닝이나 데드 코드 제거, 루프 최적화 같은 작업은 더 빠른 기계어를 만들어 주지만, 그만큼 코드를 분석하고 변환하는 시간이 듭니다. JIT는 실행 도중에 변환을 끝내야 해서 한 메서드에 그런 시간을 길게 들이기 어렵습니다. 변환이 길어질수록 실행도 그만큼 미뤄지기 때문입니다. 그래서 빌드 시점에 충분히 시간을 들이는 AOT 컴파일러와 비교하면, Mono JIT가 만든 기계어는 최적화가 덜 된 상태에 머무를 수 있습니다.

마지막으로, JIT를 아예 쓸 수 없는 플랫폼이 있습니다. JIT는 실행 중에 새 기계어를 만들어 메모리에 올리고, 그 메모리를 실행할 수 있는 상태로 바꿔야 합니다. 운영체제는 메모리 영역마다 읽기·쓰기·실행 권한을 따로 두는데, JIT는 코드를 써 넣은 영역에 다시 실행 권한을 부여해야 합니다. 그런데 iOS처럼 실행 중 코드 생성을 막아 둔 플랫폼에서는 이 과정 자체가 허용되지 않습니다. 이런 환경에서는 JIT 대신, 빌드 시점에 미리 기계어를 만들어 두는 AOT 방식이 필요합니다.

---

## AOT 컴파일 — IL2CPP

JIT가 변환을 실행 시점까지 미룬다면, **AOT(Ahead-Of-Time) 컴파일**은 빌드 시점에 미리 기계어를 만들어 둡니다. 실행할 때는 이미 만들어진 네이티브 코드를 사용하므로, JIT처럼 첫 호출 시점의 변환 비용이 없습니다.

Unity에서 AOT 빌드를 담당하는 파이프라인이 **IL2CPP**입니다.

IL2CPP는 이름 그대로 IL을 C++ 코드로 변환합니다. 이후 플랫폼별 C++ 컴파일러가 그 C++ 코드를 대상 플랫폼의 실행 형식으로 컴파일합니다. 네이티브 플랫폼에서는 기계어 바이너리가 되고, WebGL에서는 Emscripten을 거쳐 WebAssembly가 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Box 1: C# 소스 코드 -->
  <rect x="8" y="58" width="126" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="71" y="80" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C# 소스 코드</text>
  <text fill="currentColor" x="71" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">.cs</text>

  <!-- Arrow 1 -->
  <line x1="134" y1="85" x2="162" y2="85" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="167,85 159,80 159,90" fill="currentColor"/>
  <text fill="currentColor" x="148" y="43" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">Roslyn</text>

  <!-- Box 2: IL -->
  <rect x="172" y="58" width="116" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="230" y="80" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">IL 어셈블리</text>
  <text fill="currentColor" x="230" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">.dll</text>

  <!-- Arrow 2 -->
  <line x1="288" y1="85" x2="318" y2="85" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="323,85 315,80 315,90" fill="currentColor"/>
  <text fill="currentColor" x="306" y="43" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">IL2CPP</text>

  <!-- Box 3: C++ 소스 -->
  <rect x="328" y="58" width="122" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="389" y="80" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C++ 소스</text>
  <text fill="currentColor" x="389" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">자동 생성</text>

  <!-- Arrow 3 -->
  <line x1="450" y1="85" x2="478" y2="85" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="483,85 475,80 475,90" fill="currentColor"/>
  <text fill="currentColor" x="466" y="37" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">C++ 컴파일러</text>
  <text fill="currentColor" x="466" y="49" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.45">Clang / Emscripten 등</text>

  <!-- Box 4: 플랫폼별 바이너리 -->
  <rect x="488" y="58" width="124" height="54" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="550" y="80" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">플랫폼별 바이너리</text>
  <text fill="currentColor" x="550" y="97" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">기계어 / Wasm</text>

  <!-- Caption -->
  <text fill="currentColor" x="310" y="142" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">빌드 시점에 전체 변환이 끝나므로 실행 중 JIT 변환 단계가 없음</text>
</svg>
</div>

<br>

IL2CPP는 C#의 class, struct, 메서드, 배열, 제네릭 같은 요소를 대응되는 C++ 코드로 변환합니다. 이 C++ 코드는 사람이 직접 작성한 코드라기보다 빌드를 위한 중간 산출물이며, 최종적으로는 플랫폼별 C++ 컴파일러와 툴체인이 최적화하고 컴파일합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text fill="currentColor" x="320" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Add 메서드가 빌드 중 바뀌는 형태</text>

  <!-- Flow line -->
  <line x1="52" y1="68" x2="52" y2="325" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,4" opacity="0.45"/>

  <!-- Stage 1 -->
  <circle cx="52" cy="68" r="14" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="52" y="72" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">1</text>
  <rect x="82" y="42" width="500" height="58" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="104" y="63" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">C# 소스</text>
  <text fill="currentColor" x="104" y="84" text-anchor="start" font-size="12" font-family="monospace">int Add(int a, int b) =&gt; a + b;</text>
  <text fill="currentColor" x="552" y="64" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">.cs</text>

  <!-- Arrow label 1 -->
  <text fill="currentColor" x="52" y="123" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">Roslyn</text>
  <polygon points="52,129 47,121 57,121" fill="currentColor" opacity="0.45"/>

  <!-- Stage 2 -->
  <circle cx="52" cy="154" r="14" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="52" y="158" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">2</text>
  <rect x="82" y="128" width="500" height="58" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="104" y="149" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">IL 어셈블리</text>
  <text fill="currentColor" x="104" y="170" text-anchor="start" font-size="12" font-family="monospace">ldarg.0  ldarg.1  add  ret</text>
  <text fill="currentColor" x="552" y="150" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">평가 스택 명령</text>

  <!-- Arrow label 2 -->
  <text fill="currentColor" x="52" y="209" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">IL2CPP</text>
  <polygon points="52,215 47,207 57,207" fill="currentColor" opacity="0.45"/>

  <!-- Stage 3 -->
  <circle cx="52" cy="240" r="14" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="52" y="244" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">3</text>
  <rect x="82" y="214" width="500" height="58" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="104" y="235" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">C++ 산출물</text>
  <text fill="currentColor" x="104" y="256" text-anchor="start" font-size="11" font-family="sans-serif">함수 본문 + 타입/메서드 메타데이터 + 런타임 연결 정보</text>
  <text fill="currentColor" x="552" y="236" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">자동 생성</text>

  <!-- Arrow label 3 -->
  <text fill="currentColor" x="52" y="295" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">툴체인</text>
  <polygon points="52,301 47,293 57,293" fill="currentColor" opacity="0.45"/>

  <!-- Stage 4 -->
  <circle cx="52" cy="326" r="14" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="52" y="330" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">4</text>
  <rect x="82" y="300" width="500" height="58" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
  <text fill="currentColor" x="104" y="321" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">플랫폼별 실행 코드</text>
  <text fill="currentColor" x="104" y="342" text-anchor="start" font-size="12" font-family="monospace">ARM64: ADD ... RET   /   WebGL: Wasm 명령</text>
  <text fill="currentColor" x="552" y="322" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">빌드 결과</text>

  <!-- Note -->
  <text fill="currentColor" x="320" y="390" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">실제 출력은 플랫폼, 최적화 옵션, 타입 정보에 따라 달라지며 실행 전 빌드 단계에서 확정됨</text>
</svg>
</div>

<br>

실행 시점에는 기계어가 이미 만들어져 있으므로, JIT와 달리 메서드를 처음 호출할 때도 변환 비용이 들지 않습니다.

IL2CPP가 C++를 거치는 이유는 플랫폼별 C++ 컴파일러와 툴체인을 활용하기 위해서입니다.

Unity가 모든 플랫폼에 대해 자체 코드 생성기를 직접 만드는 대신, 이미 각 플랫폼에 맞게 검증된 C++ 컴파일러와 툴체인을 사용합니다. 이 덕분에 IL2CPP는 플랫폼 호환성과 컴파일러 최적화 기능을 함께 활용할 수 있습니다.

---

## Mono vs IL2CPP 비교

앞 두 절에서 Mono의 JIT와 IL2CPP의 AOT를 따로 살펴봤습니다. 두 방식은 변환 시점이 다르다는 한 가지 차이에서 출발하지만, 그 차이는 빌드 시간, 실행 성능, 첫 호출 비용, 앱 크기, 코드 보호, 플랫폼 지원으로 이어집니다.

<br>

<table>
<thead>
<tr><th>항목</th><th>Mono (JIT)</th><th>IL2CPP (AOT)</th></tr>
</thead>
<tbody>
<tr><td>컴파일 시점</td><td>실행 시 (런타임)</td><td>빌드 시 (사전)</td></tr>
<tr><td>변환 경로</td><td>IL → 기계어</td><td>IL → C++ → 플랫폼별 실행 코드</td></tr>
<tr><td>빌드 시간</td><td>짧음</td><td>김 (C++ 컴파일 추가)</td></tr>
<tr><td>실행 성능</td><td>JIT 최적화 제약 있음</td><td>C++ 컴파일러/툴체인 최적화 활용</td></tr>
<tr><td>첫 호출 비용</td><td>있음 (JIT 변환)</td><td>없음 (이미 기계어)</td></tr>
<tr><td>앱 크기</td><td>작음 (IL만 포함)</td><td>큼 (플랫폼별 바이너리 포함)</td></tr>
<tr><td>코드 보호</td><td>IL 역컴파일이 비교적 쉬움</td><td>역공학 난도가 상대적으로 높음</td></tr>
<tr><td>iOS 지원</td><td>불가 (JIT 금지)</td><td>가능 (필수)</td></tr>
<tr><td>에디터에서 사용</td><td>기본 (빠른 이터레이션)</td><td>불가 (빌드 필요)</td></tr>
</tbody>
</table>

<br>

빌드 시간은 두 방식이 밟는 단계 수에서 차이가 납니다. Mono 빌드는 C# 소스를 IL로 변환하면 대부분 끝나지만, IL2CPP 빌드는 그 뒤에 IL을 C++로 옮기고 그 C++를 컴파일하는 두 단계를 더 거칩니다. 그래서 프로젝트가 커질수록 빌드가 길어집니다. 이를 줄이려면 출력 경로를 그대로 두고 바뀐 부분만 다시 컴파일하는 **증분 빌드(Incremental Build)**가 도움이 됩니다. IL2CPP의 Code Generation 옵션에는 `Faster (smaller) builds`도 있지만, 이 값은 생성되는 코드 양을 줄여 빌드를 앞당기는 대신 실행 성능을 그만큼 내주므로, 출시 빌드보다는 개발 중 반복 작업에 맞습니다. 출시 빌드에서는 실행 성능을 우선하는 기본값 `Faster runtime`을 그대로 두는 편이 낫습니다.

실행 성능은 최적화에 얼마나 시간을 들일 수 있느냐에 따라 달라집니다. Mono JIT는 실행 도중에 기계어를 만들어야 해서 최적화에 긴 시간을 들이기 어렵지만, IL2CPP는 빌드 시점에 C++ 컴파일러가 최적화를 맡으므로 그만큼 시간을 충분히 쓸 수 있습니다. 그래서 수학 연산이나 반복문이 많은 CPU 중심 코드는 IL2CPP에서 더 빠르게 실행되기도 합니다. 다만 코드에 따라 빨라지는 정도가 다릅니다. 컴파일러 최적화가 줄여 주는 것은 CPU가 계산에 쓰는 시간뿐이기 때문입니다. 파일을 읽거나 네트워크 응답을 기다리는 데 시간을 대부분 쓰는 코드라면, 정작 오래 걸리는 부분은 그 대기 시간이라 계산이 조금 빨라져도 전체 실행 시간은 거의 그대로입니다. 이런 코드에서는 Mono와 IL2CPP의 체감 차이가 크지 않습니다.

코드 보호는 빌드 결과물에 무엇이 남느냐에 달려 있습니다. Mono 빌드에는 IL 어셈블리가 그대로 들어가는데, IL은 클래스와 메서드 구조를 비교적 잘 보존하므로 역컴파일 도구로 원본에 가까운 C#를 복원하기 쉽습니다. 반면 IL2CPP 빌드는 C# 코드가 C++를 거쳐 네이티브 바이너리로 바뀌므로, 원래의 C# 구조를 되짚어 복원하기가 더 어렵습니다. 그렇다고 IL2CPP가 코드를 완전히 숨겨 주는 것은 아닙니다. 네이티브 바이너리와 그 안에 남은 메타데이터를 분석하는 도구가 있는 만큼, 민감한 로직이라면 빌드 방식만으로 보호된다고 가정해서는 안 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Mono 빌드 box -->
  <text fill="currentColor" x="140" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">Mono 빌드</text>
  <rect x="10" y="24" width="260" height="80" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="25" y="46" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.8">앱 패키지 안에</text>
  <text fill="currentColor" x="25" y="62" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.8">Assembly-CSharp.dll 포함</text>
  <text fill="currentColor" x="25" y="80" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ IL 역컴파일러로 C# 소스 복원 가능</text>
  <text fill="currentColor" x="25" y="96" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ 클래스, 메서드, 변수명이 그대로 보임</text>
  <!-- IL2CPP 빌드 box -->
  <text fill="currentColor" x="420" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">IL2CPP 빌드</text>
  <rect x="290" y="24" width="260" height="186" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="305" y="46" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.8">앱 패키지 안에</text>
  <text fill="currentColor" x="305" y="62" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.8">네이티브 바이너리 포함</text>
  <text fill="currentColor" x="305" y="80" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ 기계어 수준의 역공학만 가능</text>
  <text fill="currentColor" x="305" y="96" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ 원본 C# 구조 파악이 어려움</text>
  <!-- 단서 -->
  <line x1="305" y1="110" x2="535" y2="110" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="305" y="128" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">다만 global-metadata.dat에</text>
  <text fill="currentColor" x="305" y="143" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">클래스명, 메서드명, 문자열 리터럴 등의</text>
  <text fill="currentColor" x="305" y="158" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">메타데이터가 남아 있어</text>
  <text fill="currentColor" x="305" y="173" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">Il2CppDumper 같은 도구로</text>
  <text fill="currentColor" x="305" y="188" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">구조 복원이 가능하므로</text>
  <text fill="currentColor" x="305" y="203" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">완전한 보호는 아님</text>
</svg>
</div>

---

## IL2CPP의 최적화 이점

IL2CPP가 실행 성능에서 앞서는 것은 주로 최적화를 빌드 시점에 끝내 두기 때문입니다. JIT는 실행 도중에 변환을 마쳐야 해서 최적화에 긴 시간을 들이기 어렵지만, IL2CPP는 빌드할 때 C++ 컴파일러에 최적화를 맡기므로 그런 시간 제약을 받지 않습니다. 덕분에 컴파일러는 코드를 더 넓게 분석하고 더 과감하게 최적화할 수 있습니다.

이렇게 적용되는 대표적인 최적화가 인라인화, 데드 코드 제거, 루프 최적화입니다.

---

### 인라인화 (Inlining)

함수를 호출하는 데에는 본문을 실행하는 일 말고도 고정된 절차가 따라붙습니다. 인자를 넘기고, 함수가 끝난 뒤 어디로 돌아올지 기록해 두고, 본문으로 건너뛰었다가 다시 제자리로 돌아오는 과정입니다. 본문이 두세 줄로 짧은 함수라면, 정작 계산은 잠깐인데 이 호출 절차가 그만큼, 때로는 그 이상으로 시간을 차지합니다.

인라인화는 이 호출 자체를 없애는 최적화입니다. 컴파일러가 함수를 부르는 대신 그 본문을 호출 지점에 그대로 복사해 넣으면, 인자 전달과 복귀 같은 절차가 사라지고 마치 처음부터 그 자리에 본문을 적어 둔 것처럼 실행됩니다.

<br>

```csharp
// 인라인화 예시

// 인라인화 전:
float GetSpeed()
{
    return baseSpeed * multiplier;
}

void Update()
{
    float s = GetSpeed();    // 함수 호출 오버헤드
    transform.position += direction * s * Time.deltaTime;
}


// 인라인화 후 (컴파일러가 자동 수행):
void Update()
{
    float s = baseSpeed * multiplier;    // 함수 본문이 직접 삽입됨
    transform.position += direction * s * Time.deltaTime;
}
```

<br>

인라인화의 효과는 호출 비용을 없애는 데서 그치지 않습니다. 인라인화 전이라면 `GetSpeed`는 독립된 함수 하나로 컴파일됩니다. 이 함수 하나가 모든 호출 지점에 쓰이므로, 컴파일러는 `multiplier`가 그때그때 무슨 값일지 가정할 수 없어 `baseSpeed * multiplier`를 일반적인 곱셈 그대로 둡니다. 그런데 본문이 호출 지점 안으로 들어오면, 컴파일러는 그 자리에 실제로 놓인 값과 조건까지 함께 보면서 코드를 더 줄일 수 있습니다.

앞의 예에서 `multiplier`가 늘 `1.0f`임을 컴파일러가 알아낼 수 있다고 하면, 호출 지점에 들어온 `baseSpeed * multiplier`는 `baseSpeed * 1.0f`가 됩니다.
이렇게 변수 자리에 알려진 상수를 대입하는 것을 상수 전파(constant propagation)라고 합니다. 그러면 `* 1.0f`는 곱해도 값이 그대로라 쓸모가 없으니, 컴파일러가 이 곱셈을 제거해 식을 `baseSpeed` 하나로 줄입니다. 
이처럼 의미를 잃은 연산을 없애는 것이 불필요한 연산 제거입니다.

---

### 데드 코드 제거 (Dead Code Elimination)

데드 코드 제거는 어떤 실행 경로로도 도달할 수 없는 코드를 최종 결과에서 제외하는 최적화입니다. 이런 코드는 실행될 일이 없어, 빌드에 남겨 둬도 바이너리 크기만 키울 뿐입니다.

<br>

```csharp
// 데드 코드 제거 예시:

// 컴파일러 분석 전:
void Process(int value)
{
    if (false)
    {
        // 이 블록은 실행되지 않음
        DoExpensiveWork();
    }

    DoActualWork(value);
}


// 컴파일러 분석 후:
void Process(int value)
{
    DoActualWork(value);
}
```

<br>

위 코드에서 `if (false)` 블록은 조건이 참이 되는 일이 없어 `DoExpensiveWork` 호출까지 한 번도 실행되지 않습니다. 컴파일러는 이 블록을 통째로 제거하고, 실제로 실행되는 `DoActualWork`만 남깁니다.

다만 모든 데드 코드가 `if (false)`처럼 눈에 잘 띄는 것은 아닙니다. 컴파일러는 상수 전파와 조건 분석을 거쳐, 겉보기에는 실행될 듯하지만 실제로는 도달할 수 없는 분기까지 가려냅니다.

---

### 루프 최적화

루프는 같은 코드를 여러 번 반복하므로, 최적화 한 번으로 얻는 이득이 반복 횟수만큼 커집니다. C++ 컴파일러는 루프를 대상으로 여러 최적화를 적용하는데, 대표적인 것이 루프 불변 코드 이동, 루프 언롤링, 벡터화입니다.

**루프 불변 코드 이동(Loop-Invariant Code Motion)**은 반복마다 같은 결과가 나오는 계산을 루프 밖으로 옮기는 최적화입니다. 값이 매 반복에서 달라지지 않는다면 한 번만 계산해 두면 충분하니, 컴파일러는 이 계산을 루프 앞으로 옮겨 같은 값을 거듭 구하지 않게 합니다.

<br>

```csharp
// 루프 불변 코드 이동:

// 최적화 전:
for (int i = 0; i < count; i++)
{
    float radius = maxRange * 0.5f;    // 매 반복 같은 값
    if (distances[i] < radius)
    {
        // ...
    }
}

// 최적화 후 (컴파일러 자동 수행):
float radius = maxRange * 0.5f;        // 루프 밖으로 이동
for (int i = 0; i < count; i++)
{
    if (distances[i] < radius)
    {
        // ...
    }
}
```

<br>

**루프 언롤링(Loop Unrolling)**은 루프 본문을 여러 번 복사해, 원래 여러 번에 걸쳐 하던 일을 한 번의 반복에서 처리하도록 펼치는 최적화입니다. 예를 들어 원소를 하나씩 처리하던 루프를 한 반복에서 네 개씩 처리하고 카운터를 4씩 올리도록 바꾸면, 반복 횟수가 1/4로 줄어듭니다. 루프는 한 바퀴마다 조건 비교와 카운터 증가, 처음으로 되돌아가는 분기 같은 제어 동작을 거치므로, 반복이 줄어든 만큼 이 동작도 그만큼 덜 거치게 됩니다. 주로 반복 횟수가 적거나 컴파일 시점에 정해지는 루프에 적용됩니다.

<br>

**벡터화(Vectorization)**는 배열의 원소마다 같은 연산을 반복하는 루프를 **SIMD(Single Instruction, Multiple Data)** 명령어로 바꾸는 최적화입니다. SIMD는 이름 그대로 명령 하나로 여러 데이터를 한꺼번에 처리합니다. 값을 하나씩 다루는 보통의 코드라면 네 개의 `float`를 더하는 데 덧셈이 네 번 필요하지만, SIMD는 이 네 값을 한 레지스터에 묶어 한 번의 덧셈으로 끝냅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Outer frame -->
  <rect x="5" y="5" width="510" height="330" rx="8" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- Title -->
  <text fill="currentColor" x="260" y="30" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">IL2CPP가 활용하는 C++ 컴파일러 최적화</text>
  <line x1="30" y1="40" x2="490" y2="40" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- 인라인화 -->
  <text fill="currentColor" x="30" y="66" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">인라인화</text>
  <text fill="currentColor" x="42" y="82" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">짧은 메서드의 호출 오버헤드 제거</text>
  <text fill="currentColor" x="42" y="97" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">추가 최적화의 기회 확대</text>
  <!-- 데드 코드 제거 -->
  <text fill="currentColor" x="30" y="122" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">데드 코드 제거</text>
  <text fill="currentColor" x="42" y="138" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">도달 불가능한 코드를 바이너리에서 제거</text>
  <text fill="currentColor" x="42" y="153" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">바이너리 크기 감소</text>
  <!-- 루프 최적화 -->
  <text fill="currentColor" x="30" y="178" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">루프 최적화</text>
  <text fill="currentColor" x="42" y="194" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">불변 코드 이동, 언롤링, 벡터화</text>
  <text fill="currentColor" x="42" y="209" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">반복 연산의 CPU 비용 감소</text>
  <!-- 상수 전파 -->
  <text fill="currentColor" x="30" y="234" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">상수 전파 (Constant Propagation)</text>
  <text fill="currentColor" x="42" y="250" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">컴파일 시 확정 가능한 값을 상수로 치환</text>
  <!-- 공통 부분식 제거 -->
  <text fill="currentColor" x="30" y="275" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">공통 부분식 제거 (Common Subexpression Elimination)</text>
  <text fill="currentColor" x="42" y="291" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.65">같은 계산의 반복 수행 방지</text>
  <!-- Footer -->
  <line x1="30" y1="305" x2="490" y2="305" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="260" y="325" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">IL2CPP는 빌드 시점에 네이티브 컴파일러 최적화를 활용</text>
</svg>
</div>

---

## 코드 스트리핑

IL2CPP의 이점은 실행 성능에 그치지 않습니다. 빌드 시점에 전체 코드를 분석할 수 있다는 같은 특성 덕분에, **코드 스트리핑(Code Stripping)**도 함께 적용됩니다. 앞의 데드 코드 제거가 실행될 수 없는 코드를 없앴다면, 코드 스트리핑은 실행될 수는 있어도 이 앱이 어디서도 호출하지 않는 코드와 라이브러리 일부를 최종 빌드에서 제거합니다.

예를 들어 `System.Xml`이나 `System.Net` 같은 .NET 라이브러리에는 타입과 메서드가 수없이 들어 있지만, 대부분의 게임은 그중 극히 일부만 사용합니다. 스트리핑 도구는 게임의 진입점에서 출발해, 직접 호출되는 메서드와 그것이 다시 호출하는 메서드를 참조를 따라가며 하나씩 표시합니다. 끝까지 한 번도 표시되지 않은 코드는 게임이 어디서도 부르지 않는다는 뜻이므로 빌드에서 제거합니다.
이를테면 XML을 전혀 다루지 않는 게임이라면 `System.Xml`이 통째로 제외됩니다. 데드 코드 제거와는 코드가 제외되는 이유가 다릅니다. 데드 코드는 `if (false)` 속 코드처럼 실행될 길이 없어서 빠지고, 스트리핑되는 코드는 멀쩡히 실행되는데도 이 게임이 쓰지 않아서 제외됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Box 1: .NET 라이브러리 전체 (large) -->
  <text fill="currentColor" x="270" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">.NET 라이브러리 전체</text>
  <rect x="30" y="24" width="480" height="76" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="50" y="48" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.IO</text>
  <text fill="currentColor" x="160" y="48" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Net</text>
  <text fill="currentColor" x="280" y="48" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Xml</text>
  <text fill="currentColor" x="400" y="48" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Json</text>
  <text fill="currentColor" x="50" y="68" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Text</text>
  <text fill="currentColor" x="160" y="68" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Linq</text>
  <text fill="currentColor" x="280" y="68" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Collections</text>
  <text fill="currentColor" x="430" y="68" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">System.Threading</text>
  <text fill="currentColor" x="470" y="88" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.4">...</text>
  <!-- Arrow down -->
  <line x1="270" y1="100" x2="270" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="270,133 265,125 275,125" fill="currentColor"/>
  <text fill="currentColor" x="285" y="120" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">정적 분석 (참조 추적)</text>
  <!-- Box 2: 게임에서 사용하는 코드 (smaller) -->
  <text fill="currentColor" x="270" y="150" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">게임에서 실제로 사용하는 코드</text>
  <rect x="80" y="158" width="380" height="76" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="100" y="180" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.65">System.Collections.Generic.List&lt;T&gt;</text>
  <text fill="currentColor" x="100" y="196" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.65">System.Collections.Generic.Dictionary&lt;K,V&gt;</text>
  <text fill="currentColor" x="100" y="212" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.65">System.Text.StringBuilder</text>
  <text fill="currentColor" x="100" y="228" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.65">System.Math</text>
  <text fill="currentColor" x="350" y="228" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.4">... (사용하는 부분만)</text>
  <!-- Arrow down -->
  <line x1="270" y1="234" x2="270" y2="260" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="270,265 265,257 275,257" fill="currentColor"/>
  <!-- Result -->
  <rect x="110" y="272" width="320" height="30" rx="6" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="270" y="292" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.8">사용된 부분만 빌드에 포함 → 빌드 크기 감소</text>
</svg>
</div>

<br>

코드 스트리핑은 빌드 크기를 줄이는 데 도움이 됩니다. 특히 모바일에서는 빌드 크기가 다운로드 시간, 설치 경험, 스토어 정책에 영향을 줄 수 있으므로, 사용하지 않는 코드를 없애는 일이 중요합니다.

다만 정적 분석만으로는 모든 사용을 파악하지 못하는 경우가 있습니다. 리플렉션(reflection)처럼 실행 중에 타입이나 메서드를 문자열로 찾는 코드가 그렇습니다. 이런 호출은 빌드 시점 분석에서 직접 참조로 드러나지 않으므로, 실제로는 사용하는 타입이나 메서드가 스트리핑으로 제거될 수 있습니다.

예를 들어 `Type.GetType("MyClass")`는 찾으려는 타입을 `"MyClass"`라는 문자열로만 가리킵니다. 분석기에게 이 문자열은 그저 글자일 뿐이라 실제 `MyClass` 타입과 이어지지 않고, 그 타입을 직접 쓰는 코드가 따로 없으면 `MyClass`는 안 쓰이는 것으로 분류돼 제거됩니다. 이렇게 제거된 타입이나 메서드를 실행 중에 찾으면, 대상이 이미 사라진 뒤라 `TypeLoadException`이나 `MissingMethodException` 같은 오류가 납니다.

직렬화 라이브러리에서도 비슷한 문제가 생길 수 있습니다. 리플렉션으로 필드나 프로퍼티를 읽는 방식이라면, 직렬화 대상 타입이 스트리핑되지 않도록 보존 설정을 확인해야 합니다.

이런 문제를 막으려면 스트리핑에서 제외할 타입이나 멤버를 명시해야 합니다. Unity에서는 `link.xml`에 보존할 어셈블리, 타입, 멤버를 지정할 수 있고, 코드에서 직접 표시하려면 `[Preserve]` 어트리뷰트를 사용할 수 있습니다.

---

## 플랫폼별 런타임 제약

Mono와 IL2CPP 중 어느 쪽을 쓸지는 늘 개발자가 정하는 것이 아니라, 플랫폼이 대신 정하기도 합니다. 플랫폼마다 보안 정책과 지원하는 아키텍처, 허용하는 빌드 형식이 다르고, 이런 조건이 특정 런타임만 허용하는 경우가 있기 때문입니다.

### iOS: JIT 불가 → IL2CPP 필수

JIT가 동작하려면 실행 중에 기계어를 만들어 실행 가능한 메모리에 올릴 수 있어야 합니다. 그런데 Apple의 iOS 보안 정책은 서드파티 앱이 실행 중에 이렇게 새 실행 코드를 만드는 것을 막습니다. 그래서 iOS에서는 JIT 기반 Mono를 쓸 수 없고, 빌드 시점에 기계어를 미리 만들어 두는 IL2CPP AOT를 써야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 일반 플랫폼 -->
  <text fill="currentColor" x="135" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">일반 플랫폼</text>
  <rect x="10" y="24" width="250" height="80" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="25" y="46" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">메모리 영역에 실행 권한(Execute)</text>
  <text fill="currentColor" x="25" y="60" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">부여 가능</text>
  <text fill="currentColor" x="25" y="78" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ JIT가 생성한 기계어를 실행 가능</text>
  <text fill="currentColor" x="25" y="94" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ 정상 동작</text>
  <!-- iOS -->
  <text fill="currentColor" x="405" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">iOS</text>
  <rect x="280" y="24" width="250" height="176" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="295" y="46" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">서드파티 앱이 메모리에 실행 권한을</text>
  <text fill="currentColor" x="295" y="60" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">동적으로 부여하는 것을 금지</text>
  <line x1="295" y1="72" x2="515" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text fill="currentColor" x="295" y="90" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">→ JIT가 기계어를 생성해도</text>
  <text fill="currentColor" x="295" y="104" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">   실행할 수 없음</text>
  <!-- X mark for JIT -->
  <line x1="300" y1="122" x2="312" y2="134" stroke="currentColor" stroke-width="2" opacity="0.7"/>
  <line x1="312" y1="122" x2="300" y2="134" stroke="currentColor" stroke-width="2" opacity="0.7"/>
  <text fill="currentColor" x="320" y="132" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.7">Mono JIT 사용 불가</text>
  <!-- Check mark for AOT -->
  <line x1="302" y1="158" x2="308" y2="164" stroke="currentColor" stroke-width="2" opacity="0.7"/>
  <line x1="308" y1="164" x2="318" y2="150" stroke="currentColor" stroke-width="2" opacity="0.7"/>
  <text fill="currentColor" x="325" y="162" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif" opacity="0.8">IL2CPP (AOT) 필수</text>
  <!-- Divider -->
  <line x1="300" y1="175" x2="515" y2="175" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text fill="currentColor" x="295" y="193" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.45">Apple 보안 정책에 의한 제한</text>
</svg>
</div>

<br>

Unity의 iOS Player 설정에서 IL2CPP가 강제되는 것도 이 때문입니다. 이는 Unity가 택한 방침이 아니라 iOS의 앱 실행 정책에서 비롯된 제약입니다.

### Android: IL2CPP 권장

Android는 iOS와 달리 JIT를 전면적으로 막지 않아 Mono도 쓸 수 있습니다. 다만 출시 빌드에서는 IL2CPP를 선택하는 경우가 많습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <rect x="5" y="5" width="470" height="220" rx="8" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- Title -->
  <text fill="currentColor" x="240" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Android에서 IL2CPP가 권장되는 이유</text>
  <line x1="25" y1="38" x2="455" y2="38" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Item 1 -->
  <text fill="currentColor" x="30" y="62" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">1.</text>
  <text fill="currentColor" x="50" y="62" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">실행 성능 향상</text>
  <text fill="currentColor" x="50" y="78" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">C++ 컴파일러의 최적화로 더 빠른 기계어 생성</text>
  <!-- Item 2 -->
  <text fill="currentColor" x="30" y="102" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">2.</text>
  <text fill="currentColor" x="50" y="102" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">64비트 지원</text>
  <text fill="currentColor" x="50" y="118" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">Google Play는 64비트 바이너리를 요구 — IL2CPP는 ARM64를 완전히 지원</text>
  <!-- Item 3 -->
  <text fill="currentColor" x="30" y="142" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">3.</text>
  <text fill="currentColor" x="50" y="142" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">코드 보호</text>
  <text fill="currentColor" x="50" y="158" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">IL 역컴파일 방지</text>
  <!-- Item 4 -->
  <text fill="currentColor" x="30" y="182" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">4.</text>
  <text fill="currentColor" x="50" y="182" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">일관된 동작</text>
  <text fill="currentColor" x="50" y="198" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">iOS와 같은 런타임 → 플랫폼 간 동작 차이 최소화</text>
</svg>
</div>

<br>

이 네 가지 가운데 출시에서 특히 결정적인 것은 64비트 지원 요건입니다. Google Play는 앱이 64비트(ARM64) 바이너리를 포함하도록 요구하는데, Unity의 Mono 백엔드는 Android에서 이 ARM64를 만들지 못하고 IL2CPP만 지원합니다. 그래서 Play 스토어에 올리는 빌드라면 IL2CPP를 써야 합니다.

### WebGL: IL2CPP 필수

WebGL 빌드는 게임을 브라우저 안에서 실행합니다. 브라우저는 보통의 네이티브 실행 파일을 직접 실행하지 못하므로, Unity는 IL2CPP로 만든 C++ 코드를 **Emscripten**을 거쳐 **WebAssembly(Wasm)**로 변환합니다.

Emscripten은 C/C++ 코드를 브라우저가 실행할 수 있는 Wasm 형식으로 컴파일하는 도구입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 80" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- C# -->
  <rect x="5" y="10" width="60" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="35" y="31" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C#</text>
  <line x1="65" y1="26" x2="87" y2="26" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="92,26 84,21 84,31" fill="currentColor"/>
  <!-- IL -->
  <rect x="97" y="10" width="50" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="122" y="31" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">IL</text>
  <line x1="147" y1="26" x2="169" y2="26" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="174,26 166,21 166,31" fill="currentColor"/>
  <!-- C++ (IL2CPP) -->
  <rect x="179" y="10" width="110" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="234" y="31" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C++ (IL2CPP)</text>
  <line x1="289" y1="26" x2="311" y2="26" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="316,26 308,21 308,31" fill="currentColor"/>
  <!-- WebAssembly -->
  <rect x="321" y="10" width="160" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="401" y="31" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">WebAssembly</text>
  <text fill="currentColor" x="401" y="56" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(Emscripten)</text>
  <line x1="481" y1="26" x2="503" y2="26" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="508,26 500,21 500,31" fill="currentColor"/>
  <!-- 브라우저 -->
  <text fill="currentColor" x="520" y="31" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif" opacity="0.8">브라우저에서 실행</text>
</svg>
</div>

<br>

네이티브 빌드가 운영체제 위에서 독립된 프로그램으로 실행되는 것과 달리, WebGL 빌드는 웹 페이지 안에서 브라우저가 제공하는 자원만으로 동작합니다. 이 한계는 런타임에서부터 나타납니다. iOS와 마찬가지로 브라우저도 실행 도중에 만들어 낸 기계어를 받아 주지 않아, 실행 중 변환에 기대는 Mono JIT를 쓸 수 없습니다. 그래서 WebGL도 빌드 시점에 변환을 끝내는 IL2CPP AOT를 씁니다.

제약은 런타임에만 그치지 않습니다. 브라우저에서 게임은 페이지를 그리는 메인 스레드를 함께 쓰므로, 네이티브와 달리 C# 스레드를 자유롭게 쓸 수 없습니다. 파일을 동기적으로 읽거나 메인 스레드를 오래 붙잡는 작업도 페이지를 멈춰 세우기 때문에 제한됩니다.

파일 시스템과 메모리도 브라우저가 허용하는 API와 한도 안에서만 다룰 수 있습니다. 따라서 WebGL을 겨냥한 프로젝트라면 네이티브 플랫폼과 같은 런타임 환경을 가정해서는 안 됩니다.

### 플랫폼별 런타임 선택 정리

<table>
<thead>
<tr><th>플랫폼</th><th>Mono (JIT)</th><th>IL2CPP (AOT)</th><th>권장</th></tr>
</thead>
<tbody>
<tr><td>Unity 에디터 (개발 중)</td><td>O (기본)</td><td>X</td><td>Mono (빠른 반복)</td></tr>
<tr><td>Windows / Mac (스탠드얼론)</td><td>O</td><td>O</td><td>상황에 따라</td></tr>
<tr><td>iOS</td><td>X (금지)</td><td>O (필수)</td><td>IL2CPP</td></tr>
<tr><td>Android</td><td>O</td><td>O</td><td>IL2CPP (성능 + 64bit)</td></tr>
<tr><td>WebGL</td><td>X</td><td>O (필수)</td><td>IL2CPP</td></tr>
<tr><td>콘솔 (PS, Xbox, etc.)</td><td>X</td><td>O (필수)</td><td>IL2CPP</td></tr>
</tbody>
</table>

<br>

모바일과 WebGL 출시 빌드에서 IL2CPP를 사용한다는 것은 C# 코드가 IL을 거쳐 C++와 네이티브 코드로 바뀐다는 뜻입니다. 따라서 리플렉션, 코드 스트리핑, 제네릭 사용 방식처럼 IL2CPP에서 달라질 수 있는 지점을 미리 확인해야 합니다.

---

## 개발 워크플로

실제 개발에서는 Mono와 IL2CPP를 목적에 따라 나누어 사용하는 경우가 많습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Stage 1 -->
  <rect x="10" y="8" width="460" height="100" rx="8" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="30" y="30" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">1단계: 코드 작성 및 에디터 테스트</text>
  <rect x="30" y="40" width="420" height="56" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.6"/>
  <text fill="currentColor" x="45" y="58" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">Mono (JIT)</text>
  <text fill="currentColor" x="45" y="74" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">Play 즉시 실행 · 빠른 이터레이션 · 로직 검증에 집중</text>
  <!-- Arrow 1→2 -->
  <line x1="240" y1="108" x2="240" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,133 235,125 245,125" fill="currentColor"/>
  <!-- Stage 2 -->
  <rect x="10" y="138" width="460" height="100" rx="8" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="30" y="160" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">2단계: 기기 테스트</text>
  <rect x="30" y="170" width="420" height="56" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.6"/>
  <text fill="currentColor" x="45" y="188" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">IL2CPP (AOT)</text>
  <text fill="currentColor" x="45" y="204" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">실제 기기에서 성능 측정 · IL2CPP 특유의 문제 확인</text>
  <text fill="currentColor" x="45" y="218" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.45">(코드 스트리핑, 리플렉션 제한 등)</text>
  <!-- Arrow 2→3 -->
  <line x1="240" y1="238" x2="240" y2="258" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,263 235,255 245,255" fill="currentColor"/>
  <!-- Stage 3 -->
  <rect x="10" y="268" width="460" height="96" rx="8" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="30" y="290" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">3단계: 출시 빌드</text>
  <rect x="30" y="300" width="420" height="52" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.6"/>
  <text fill="currentColor" x="45" y="318" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif" opacity="0.8">IL2CPP (AOT)</text>
  <text fill="currentColor" x="45" y="334" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">최종 성능 최적화 · 코드 스트리핑으로 빌드 크기 최소화 · 코드 보호</text>
</svg>
</div>

<br>

그래서 에디터에서는 Mono로 빠르게 반복하며 개발하고, 기기 테스트와 출시 빌드에서는 IL2CPP로 실제 런타임 조건을 확인하는 흐름이 일반적입니다.

그런데 Mono에서 정상 동작하던 코드가 IL2CPP에서는 다르게 동작할 수 있습니다. 그 원인은 앞서 본 코드 스트리핑과 리플렉션, 그리고 아직 다루지 않은 AOT의 제네릭 처리입니다.

AOT는 코드에 쓰인 제네릭 타입 조합을 빌드 시점에 미리 모두 컴파일해 두고, 실행 중에 새 조합을 JIT로 만들어 내지는 못합니다. 그래서 어떤 제네릭 조합이 코드에서 직접 참조되지 않고 리플렉션으로만 쓰이면, 빌드 분석이 그 조합을 보지 못해 컴파일하지 않고, 실행 중에 그 조합을 쓸 때 예외가 납니다. 이런 조합이 필요하다면 빌드 시점에 드러나도록 코드에서 한 번 명시적으로 참조해 두거나 보존 설정에 넣어야 합니다.

이런 차이는 출시 직전에야 발견하면 수정 비용이 커집니다. 그래서 개발 중에도 일정한 주기로 IL2CPP 기기 빌드를 만들어 미리 확인해 두는 것이 안전합니다.

---

## 마무리

이번 글에서는 C# 소스가 기계어가 되기까지 거치는 단계와, Unity가 그 변환을 Mono(JIT)와 IL2CPP(AOT)로 어떻게 처리하는지 정리했습니다. 핵심은 다음과 같습니다.

- **IL**은 C# 컴파일러가 만드는 플랫폼 독립적인 중간 코드입니다. CPU가 직접 실행하지 못하므로 런타임이 기계어로 바꿔야 합니다.
- **Mono(JIT)**는 실행 중에 IL을 기계어로 바꿉니다. 빌드와 에디터 반복은 빠르지만, 첫 호출 비용과 실행 중 최적화 제약이 있습니다.
- **IL2CPP(AOT)**는 빌드 시점에 IL을 C++로 옮겨 네이티브 바이너리로 컴파일합니다. 빌드 시간은 길어지지만, 첫 호출 비용이 없고 플랫폼별 C++ 컴파일러의 최적화를 활용합니다.
- **코드 스트리핑**은 빌드에서 쓰지 않는 코드를 제거해 크기를 줄입니다. 리플렉션이나 직렬화로만 쓰이는 코드는 정적 분석에 드러나지 않아 `link.xml`이나 `[Preserve]`로 따로 남겨야 할 수 있습니다.
- **플랫폼 제약**으로 iOS와 WebGL은 IL2CPP가 필수이고, Android 출시 빌드도 64비트 요건 때문에 보통 IL2CPP로 검증합니다.

정리하면, 이 차이들은 결국 IL을 언제 기계어로 바꾸느냐로 모입니다. 실행 시점에 바꾸면 개발 반복이 빠른 대신 런타임 비용과 플랫폼 제약을 안고, 빌드 시점에 미리 바꾸면 빌드 시간은 늘어도 실행 환경이 더 예측 가능해집니다.

이 글에서 다룬 변환 파이프라인을 바탕으로, 다음 글 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서는 런타임의 또 다른 핵심 역할인 메모리 회수를 다룹니다. GC가 어떤 기준으로 힙의 객체를 찾아 회수하는지, Unity의 Boehm GC와 Incremental GC가 어떻게 다른지 살펴봅니다.

<br>

---

**관련 글**
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
- **C# 런타임 기초 (2) - .NET 런타임과 IL2CPP** (현재 글)
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
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
