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

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서는 값 타입과 참조 타입이 메모리에 어떻게 자리잡는지 살펴보았습니다. 값 타입은 데이터를 스택에 직접 담지만, 참조 타입은 힙에 객체를 두고 변수에는 그 주소만 저장합니다. 이 구분이 메모리 배치와 GC 비용을 가르는 출발점이었습니다.

<br>

이전 글이 데이터가 메모리 어디에 놓이는가를 다뤘다면, 이번 글은 한 걸음 더 들어가 작성한 코드가 어떻게 CPU 위에서 실제로 돌아가는지를 따라갑니다. 이 변환과 실행 전반을 맡는 소프트웨어 계층을 **런타임 시스템(Runtime System)**이라고 부릅니다.

"런타임"이라는 말은 본래 "실행 시점"을 가리키지만, 이 글에서 말하는 런타임은 코드 로딩부터 기계어 변환, 메모리 관리, 예외 처리까지 떠맡는 소프트웨어 계층을 뜻합니다. 한 단어가 두 뜻을 겸하는 까닭은, 이 계층이 곧 실행 시점에 동작하는 시스템이기 때문입니다.

<br>

게임 로직이 CPU에서 돌아가려면 C# 소스 코드가 기계어, 즉 바이너리로 바뀌어야 합니다. 그런데 C#은 C++처럼 소스가 곧바로 기계어가 되는 언어가 아닙니다.

C# 컴파일러가 내놓는 결과물은 **IL(Intermediate Language)**이라는 중간 표현입니다. 이 IL을 언제, 어떤 방식으로 기계어로 옮기느냐에 따라 런타임의 성격이 달라집니다.

<br>

이 변환 방식의 차이는 게임 성능에 곧바로 영향을 줍니다. 같은 C# 코드라도 런타임이 인라인화나 루프 벡터화 같은 최적화를 어디까지 적용하느냐에 따라 생성되는 기계어의 품질이 달라지고, CPU가 그 코드를 처리하는 속도도 함께 바뀝니다. iOS처럼 실행 시점에 새 기계어를 만들어내는 것 자체를 막는 플랫폼에서는 특정 런타임 방식을 아예 쓸 수 없기도 합니다.

<br>

Unity는 이 변환을 두 가지 런타임 방식 가운데 하나로 처리합니다. 실행 시점에 IL을 기계어로 옮기는 **Mono(JIT)**, 그리고 빌드 시점에 IL을 C++로 바꾼 뒤 네이티브로 컴파일하는 **IL2CPP(AOT)**입니다. 두 방식은 빌드 시간, 실행 성능, 플랫폼 호환성에서 서로 다른 성격을 띠며, 대상 플랫폼에 따라 선택지가 좁혀지기도 합니다.

이번 글에서는 C# 코드가 기계어로 옮겨지는 과정부터 JIT와 AOT의 차이, Mono와 IL2CPP 비교, C++ 컴파일러 최적화, 코드 스트리핑, 플랫폼별 런타임 제약까지 차례로 다룹니다.

---

## C# 컴파일 과정

C#은 **컴파일 언어**입니다. 작성한 코드를 실행하기에 앞서 컴파일러가 먼저 변환을 거칩니다. 다만 C++처럼 소스 코드가 곧장 기계어가 되지는 않으며, C#의 컴파일에는 중간 단계가 하나 끼어 있습니다.

<br>

C# 컴파일러인 Roslyn은 소스 코드를 **IL(Intermediate Language, 중간 언어)**이라는 바이트코드로 옮깁니다. 같은 코드를 두고 CIL(Common Intermediate Language)이나 MSIL(Microsoft Intermediate Language)이라고도 부릅니다.

다만 IL은 기계어가 아닙니다. CPU가 곧바로 실행하지 못하는, 특정 플랫폼에 매이지 않은 중간 표현입니다.

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

IL이라는 단계를 한 번 거치는 까닭은 .NET의 설계 원칙인 **플랫폼 독립성**에 있습니다.

같은 C# 코드를 Windows, Linux, macOS, iOS, Android에서 모두 돌리려 해도, 플랫폼마다 기계어가 다르기에 결국 플랫폼별로 따로 컴파일해야 합니다. 그런데 IL이라는 중간 표현을 사이에 두면, C# 컴파일러는 플랫폼을 가리지 않는 IL까지만 만들고, 그 IL을 기계어로 옮기는 일은 각 플랫폼의 런타임이 떠맡게 됩니다. 이렇게 컴파일러와 런타임이 역할을 나눠 가지므로, 새 플랫폼을 더할 때도 IL을 옮기는 런타임만 갖추면 됩니다.

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

IL은 스택을 바탕으로 동작하는 명령어 집합입니다. 간단한 C# 코드를 IL로 옮겨 보면 그 성격이 한눈에 드러납니다.

<br>

```
C# 코드:

int Add(int a, int b)
{
    return a + b;
}


IL로 변환된 코드 (개념적 표현):

ldarg.0        // 첫 번째 인자(a)를 스택에 올림
ldarg.1        // 두 번째 인자(b)를 스택에 올림
add            // 스택의 두 값을 더해서 결과를 스택에 올림
ret            // 스택 최상단의 값을 반환
```

<br>

IL은 바이트코드 형식을 따르므로, 명령어 하나하나(opcode)는 1바이트나 2바이트로 인코딩되고, 명령어 종류에 따라 그 뒤에 피연산자(operand)가 더 붙기도 합니다.

위 예시에서 `ldarg.0`은 첫 번째 인자를 **평가 스택(Evaluation Stack)**에 올려놓고, `add`는 스택 맨 위의 두 값을 꺼내 더한 다음 그 결과를 다시 스택에 얹습니다.

평가 스택은 IL 명령어가 계산에 쓸 값을 잠시 쌓아 두는 논리적 자료구조입니다. CPU의 레지스터가 연산의 피연산자를 담아 두는 일과 비슷한 자리이지만, 레지스터는 이름을 지정해 곧바로 꺼내 쓰는 데 비해 평가 스택은 LIFO(후입선출) 순서로만 값을 넣고 빼낼 수 있습니다.

<br>

IL은 그 자체로는 CPU가 실행할 수 없으므로, 프로그램이 돌아가기 전에 해당 플랫폼의 기계어로 옮겨져야 합니다. 이 변환을 떠맡는 것이 바로 **런타임**이며, 언제 변환하느냐에 따라 **JIT(Just-In-Time)**와 **AOT(Ahead-Of-Time)** 두 갈래로 나뉩니다.

---

## JIT 컴파일 — Mono 런타임

IL을 언제 기계어로 옮기느냐가 첫 번째 갈림길입니다. 코드를 실행하는 도중에 그때그때 옮기는 방식을 **JIT(Just-In-Time) 컴파일**이라 부르며, Unity에서 이 변환을 맡는 런타임이 바로 **Mono**입니다.

<br>

Mono가 코드를 돌리는 일은 메서드 단위로 일어납니다.

게임이 켜진 뒤 어떤 메서드가 처음 불리면, Mono는 그 메서드의 IL을 읽어 기계어로 옮겨 둡니다. 이렇게 만들어 둔 기계어는 메모리에 캐시로 남기에, 같은 메서드를 다시 부를 때는 변환을 건너뛰고 캐시에 든 기계어를 곧바로 돌리면 됩니다.

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

실행 중에 변환한다는 이 한 가지 성격이 JIT와 AOT를 빌드 속도, 첫 호출 비용, 최적화 깊이, 플랫폼 호환성이라는 네 갈래에서 갈라놓습니다. 하나씩 짚어 보겠습니다.

<br>

**빌드 시간이 짧습니다.**

Roslyn이 IL을 만들어 내면 그 시점에 빌드가 끝납니다. 기계어로 옮기는 일은 실행할 때로 미뤄지므로 빌드에는 끼지 않습니다. Unity 에디터에서 Play를 누르자마자 게임이 도는 것도 같은 까닭인데, IL을 C++로 바꾸고 다시 기계어로 컴파일하는 AOT 단계를 거치지 않고 IL을 그대로 올려 돌리기 때문입니다. 그래서 코드를 고친 뒤 곧장 결과를 확인하는 빠른 이터레이션이 가능해집니다.

<br>

**메서드를 처음 부를 때 변환 비용이 듭니다.**

어떤 메서드가 처음 불리는 순간, JIT 컴파일러가 그 IL을 읽고 기계어를 만들어 내는 데 시간이 걸립니다. 게임이 막 켜진 직후나 새 씬을 막 불러온 직후처럼 여러 메서드가 한꺼번에 처음 불리는 때에는, 그만큼의 변환이 몰리면서 그 순간 프레임 시간이 늘 수 있습니다. 다만 한 번 변환해 둔 메서드는 캐시에 남으므로, 이후 호출에서는 이 비용이 더는 들지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Y axis -->
  <text fill="currentColor" x="18" y="16" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">프레임 시간 (ms)</text>
  <line x1="60" y1="30" x2="60" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <!-- X axis -->
  <line x1="60" y1="210" x2="460" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <!-- 16ms baseline (dashed) -->
  <line x1="60" y1="140" x2="460" y2="140" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3" opacity="0.5"/>
  <text fill="currentColor" x="55" y="144" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.6">16</text>
  <text fill="currentColor" x="465" y="144" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">프레임 예산 (60fps)</text>
  <!-- Bar 1: tall (JIT overhead) -->
  <rect x="85" y="50" width="36" height="160" rx="3" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="103" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">1</text>
  <!-- Bars 2-7: normal height -->
  <rect x="140" y="160" width="36" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="158" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">2</text>
  <rect x="195" y="160" width="36" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="213" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">3</text>
  <rect x="250" y="160" width="36" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="268" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">4</text>
  <rect x="305" y="160" width="36" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="323" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">5</text>
  <rect x="360" y="160" width="36" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="378" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">6</text>
  <rect x="415" y="160" width="36" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="433" y="222" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">7</text>
  <!-- X axis label -->
  <text fill="currentColor" x="270" y="240" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">프레임</text>
  <!-- Annotation: bar 1 -->
  <text fill="currentColor" x="128" y="46" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.7">← 첫 프레임: 다수의 메서드가 JIT 컴파일</text>
  <!-- Bottom annotations -->
  <text fill="currentColor" x="60" y="260" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">프레임 1에서 JIT 컴파일 비용으로 예산 초과</text>
  <text fill="currentColor" x="60" y="275" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">프레임 2부터는 캐시된 기계어 실행 → 정상 프레임</text>
</svg>
</div>

<br>

**기계어 최적화의 깊이가 얕습니다.**

JIT 컴파일러는 게임이 도는 중간에 기계어를 만들어 내야 하므로 변환에 들일 수 있는 시간이 빠듯합니다. 변환이 길어지는 만큼 게임 실행이 멈춰 기다리게 되기 때문입니다.

컴파일러가 기계어를 다듬을 때 쓰는 대표적인 기법으로는 세 가지를 꼽을 수 있습니다. 짧은 메서드의 본문을 호출하는 자리에 그대로 끼워 넣어 호출 비용을 없애는 **인라이닝(Inlining)**, 반복문의 연산을 CPU의 SIMD 명령어로 묶어 한 번에 여러 데이터를 처리하는 **루프 벡터화(Loop Vectorization)**, 실행 도중 닿을 수 없는 코드를 들어내 바이너리 크기와 분기 비용을 줄이는 **데드 코드 제거(Dead Code Elimination)**입니다.

Mono JIT는 인라이닝이나 데드 코드 제거를 기초적인 선에서만 적용하며, 루프 벡터화처럼 손이 많이 가는 최적화는 거의 손대지 못합니다.

AOT 컴파일러가 빌드 시간을 넉넉히 쓰며 이런 기법을 두루 적용하는 데 비해, JIT 컴파일러는 짧은 시간 안에 "쓸 만한 수준"의 기계어를 빠르게 뽑아내는 쪽에 무게를 둡니다.

<br>

**실행 도중 메모리에 새 코드를 만들어 올립니다.**

JIT 컴파일은 게임이 도는 와중에 실행 가능한 기계어를 메모리에 새로 써넣는 일입니다.

운영체제는 메모리를 영역별로 나누어 읽기, 쓰기, 실행이라는 세 권한을 따로 매깁니다. JIT 컴파일러가 어느 영역에 기계어를 써넣은 뒤 그 영역에 실행 권한까지 붙여 주어야, 비로소 CPU가 그 코드를 돌릴 수 있습니다.

그런데 iOS처럼 서드파티 앱이 메모리 영역에 실행 권한을 실행 도중 새로 붙이는 것을 막아 둔 플랫폼에서는 이 마지막 단계가 막혀 버려, JIT 방식 자체를 쓸 수 없습니다.

---

## AOT 컴파일 — IL2CPP

변환을 실행 시점까지 미루는 JIT와 정반대로, 빌드하는 동안 IL을 기계어로 미리 다 옮겨 두는 방식이 **AOT(Ahead-Of-Time) 컴파일**입니다. 게임을 돌릴 때는 기계어가 이미 갖춰져 있으니, JIT처럼 도중에 변환하는 단계가 끼지 않습니다.

<br>

Unity에서 이 AOT 변환을 떠맡는 파이프라인이 **IL2CPP**입니다.

IL2CPP라는 이름은 "IL to C++"를 줄인 것으로, Unity가 직접 만든 변환 도구를 가리킵니다. 이 도구는 IL을 곧장 기계어로 바꾸지 않고 한 단계를 더 둡니다. IL을 먼저 **C++ 소스 코드**로 옮긴 다음, 그 C++를 플랫폼마다 갖춰진 네이티브 C++ 컴파일러(Clang, GCC, MSVC 등)에 넘겨 컴파일하여 최종 기계어를 뽑아냅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 120" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Box 1: C# 소스 코드 -->
  <rect x="5" y="8" width="120" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="65" y="29" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C# 소스 코드</text>
  <text fill="currentColor" x="65" y="46" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(.cs)</text>
  <text fill="currentColor" x="65" y="76" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">개발자 작성</text>
  <!-- Arrow 1 -->
  <line x1="125" y1="33" x2="153" y2="33" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="158,33 150,28 150,38" fill="currentColor"/>
  <!-- Box 2: IL -->
  <rect x="163" y="8" width="120" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="223" y="29" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">IL</text>
  <text fill="currentColor" x="223" y="46" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(DLL)</text>
  <text fill="currentColor" x="223" y="76" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">C# 컴파일러 (Roslyn)</text>
  <!-- Arrow 2 -->
  <line x1="283" y1="33" x2="311" y2="33" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="316,33 308,28 308,38" fill="currentColor"/>
  <!-- Box 3: C++ 소스 -->
  <rect x="321" y="8" width="120" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="381" y="29" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">C++ 소스</text>
  <text fill="currentColor" x="381" y="46" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.55">(자동 생성)</text>
  <text fill="currentColor" x="381" y="76" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">IL2CPP 변환</text>
  <!-- Arrow 3 -->
  <line x1="441" y1="33" x2="469" y2="33" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="474,33 466,28 466,38" fill="currentColor"/>
  <!-- Box 4: 네이티브 바이너리 -->
  <rect x="479" y="8" width="136" height="50" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="547" y="29" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">네이티브 바이너리</text>
  <text fill="currentColor" x="547" y="76" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">C++ 컴파일러 (Clang 등)</text>
</svg>
</div>

<br>

IL2CPP가 IL을 C++로 옮길 때, C#의 class와 struct, 메서드, 배열, 제네릭 같은 요소들이 저마다 대응하는 C++ 코드로 풀려 나옵니다. 사람이 읽을 수는 있으나 기계가 찍어낸 코드라 알아보기 쉬운 편은 아닙니다. 이렇게 나온 C++를 플랫폼의 네이티브 컴파일러가 최적화하고 컴파일해 최종 기계어로 마무리합니다.

<br>

```
IL2CPP 변환 예시 (개념적):

C# 코드:
int Add(int a, int b)
{
    return a + b;
}

  ↓ C# 컴파일러 → IL ↓ IL2CPP 변환

생성된 C++ 코드 (개념적 표현):
int32_t ClassName_Add(int32_t a, int32_t b)
{
    return a + b;
}

  ↓ C++ 컴파일러 (Clang 등)

ARM 기계어:
  ADD W0, W0, W1
  RET
```

<br>

게임을 돌릴 무렵에는 기계어가 이미 다 갖춰져 있으니 JIT처럼 변환에 드는 비용이 없습니다. 게임이 막 켜진 첫 프레임에서도 어느 메서드든 기계어 그대로 곧장 돌아갑니다.

<br>

IL2CPP가 굳이 C++를 한 번 거쳐 가는 까닭은 비용을 아끼려는 실용적 판단에 있습니다.

iOS, Android, Windows, WebGL처럼 플랫폼마다 기계어를 찍어 내는 코드 생성기(code generator)를 손수 만들자면 품이 많이 듭니다. 그 대신 IL2CPP는 이미 각 플랫폼에 자리 잡은 우수한 C++ 컴파일러(Clang, GCC, MSVC 등)에 그 일을 맡깁니다. 덕분에 IL2CPP는 수십 년에 걸쳐 다듬어져 온 C++ 컴파일러의 코드 생성력과 최적화 역량을 그대로 빌려 씁니다. 좋은 도구가 이미 갖춰져 있는데 같은 도구를 처음부터 다시 만드느라 힘을 빼는 대신, 그 능력을 가져다 활용하는 쪽을 택했습니다.

---

## Mono vs IL2CPP 비교

Mono(JIT)와 IL2CPP(AOT)가 코드를 돌리는 방식을 각각 따라가 보았으니, 이제 두 런타임이 어디서 어떻게 갈리는지 주요 특성을 한자리에 모아 보겠습니다.

<br>

<table>
<thead>
<tr><th>항목</th><th>Mono (JIT)</th><th>IL2CPP (AOT)</th></tr>
</thead>
<tbody>
<tr><td>컴파일 시점</td><td>실행 시 (런타임)</td><td>빌드 시 (사전)</td></tr>
<tr><td>변환 경로</td><td>IL → 기계어</td><td>IL → C++ → 기계어</td></tr>
<tr><td>빌드 시간</td><td>짧음</td><td>김 (C++ 컴파일 추가)</td></tr>
<tr><td>실행 성능</td><td>보통 (JIT 최적화 제한적)</td><td>높음 (C++ 컴파일러 최적화)</td></tr>
<tr><td>첫 호출 비용</td><td>있음 (JIT 변환)</td><td>없음 (이미 기계어)</td></tr>
<tr><td>앱 크기</td><td>작음 (IL만 포함)</td><td>큼 (네이티브 바이너리)</td></tr>
<tr><td>코드 보호</td><td>약함 (IL 역컴파일 용이)</td><td>강함 (C++/기계어로 역공학 어려움)</td></tr>
<tr><td>iOS 지원</td><td>불가 (JIT 금지)</td><td>가능 (필수)</td></tr>
<tr><td>에디터에서 사용</td><td>기본 (빠른 이터레이션)</td><td>불가 (빌드 필요)</td></tr>
</tbody>
</table>

<br>

**빌드 시간.**

Mono 빌드는 Roslyn이 IL을 만들어 내는 선에서 마무리됩니다.

반면 IL2CPP 빌드는 그 뒤로 IL을 C++로 옮기는 작업과 그 C++를 컴파일하는 작업이 더 붙습니다. 그래서 규모가 큰 프로젝트에서는 빌드 한 번에 수십 분이 걸리기도 합니다.

이 시간을 줄이려면 이전 빌드와 같은 디렉터리에 다시 빌드해, C++ 컴파일러가 바뀐 파일만 골라 다시 컴파일하도록 하는 **증분 빌드(Incremental Build)**를 쓸 수 있습니다.

여기에 더해 IL2CPP Code Generation 옵션을 Faster (Smaller) Builds로 맞추면 생성되는 C++ 코드량 자체가 줄어, 빌드가 한층 빨라집니다.

<br>

**실행 성능.**

Mono의 JIT 컴파일러는 게임이 도는 도중에 기계어를 서둘러 만들어 내야 하는 처지라, 손이 많이 가는 최적화에는 시간을 들이기 어렵습니다.

반면 IL2CPP에서는 C++ 컴파일러가 빌드 시점에 시간을 넉넉히 들여 코드를 다듬으므로, 그렇게 나온 기계어의 품질이 한 수 위입니다.

이 차이는 수학 연산이 빽빽한 게임 로직이나 물리 시뮬레이션, AI 경로 탐색처럼 계산이 무거운 곳에서 두드러져, IL2CPP가 Mono보다 빠르게 돕니다. 특히 수학 연산이나 루프가 몰린 코드에서는 1.5배에서 2배가량 빨라졌다는 보고도 있습니다. 다만 이 수치는 코드의 성격에 따라 들쭉날쭉하며, 디스크나 네트워크 입출력이 중심인 코드에서는 그 차이가 거의 드러나지 않기도 합니다.

<br>

**코드 보호.**

Mono 빌드에는 IL이 손대지 않은 채 그대로 담깁니다.

IL은 클래스명과 메서드명, 변수명처럼 원래 고수준 언어에 가깝던 정보를 그대로 안고 있어, ILSpy나 dnSpy 같은 도구를 들이대면 원본에 가까운 코드로 어렵지 않게 되돌릴 수 있습니다.

이에 비해 IL2CPP 빌드에서는 C# 코드가 C++를 거쳐 기계어까지 내려가면서, 원래의 C# 구조가 상당 부분 흐려집니다.

이것이 완벽한 차단막은 아니지만, 코드를 거꾸로 파헤치는 일을 한결 까다롭게 만듭니다.

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

앞에서 IL2CPP가 실행 성능에서 한 수 위라는 점을 표로 짚었는데, 그 격차가 어디서 벌어지는지는 두 런타임이 기계어를 다듬는 데 쓸 수 있는 시간을 견주어 보면 드러납니다.

Mono의 JIT 컴파일러는 게임이 도는 도중에 기계어를 서둘러 내놓아야 하는 처지라 최적화에 들일 시간이 빠듯합니다. 반면 IL2CPP가 넘기는 C++는 빌드 시점에 컴파일되므로, C++ 컴파일러가 시간에 쫓기지 않고 코드를 깊이 다듬을 수 있습니다.

이 여유 덕분에 C++ 컴파일러는 여러 최적화 기법을 두루 적용하는데, 그 가운데 효과가 두드러지는 세 갈래를 차례로 짚어 보겠습니다.

---

### 인라인화 (Inlining)

C++ 컴파일러가 가장 먼저 손대는 기법은 인라인화입니다.

함수를 한 번 부를 때마다 매개변수를 넘기고, 스택 프레임을 새로 잡고, 끝나면 호출 자리로 되돌아오는 절차가 따라붙습니다. 이 절차에 드는 비용은 함수 본문이 짧을수록 도드라지는데, 정작 함수가 하는 실제 연산은 얼마 안 되는데 그 주변을 감싸는 호출 절차의 몫이 상대적으로 커지기 때문입니다.

인라인화는 함수를 부르는 대신 그 본문을 호출하는 자리에 그대로 끼워 넣어, 이 호출 절차 자체를 없앱니다.

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

다만 인라인화가 가져다주는 이득은 호출 절차를 덜어 내는 데서 끝나지 않습니다.

함수가 따로 떨어져 있으면 컴파일러는 그 함수만 따로 떼어 분석할 뿐, 어디서 어떤 값으로 불리는지까지는 알지 못합니다. 그런데 인라인화로 본문이 호출 지점에 녹아들면, 그 자리에 넘어온 값까지 한눈에 들어오게 됩니다.

위 예시에서 `multiplier`가 늘 `1.0f`로만 넘어온다면, 컴파일러는 `baseSpeed * 1.0f`가 곧 `baseSpeed`임을 알아채고 곱셈을 통째로 들어냅니다.

`GetSpeed()`가 떨어져 있을 때는 호출자의 값이 보이지 않아 이런 정리가 어렵지만, 본문이 합쳐진 뒤에는 값이 그대로 드러나므로 길이 열립니다.

---

### 데드 코드 제거 (Dead Code Elimination)

두 번째는 데드 코드 제거로, 어떤 실행 경로로도 닿을 수 없는 코드를 가려내어 컴파일 결과에서 들어내는 기법입니다.

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

눈에 띄는 `if (false)`만 걸러 내는 데서 그치지도 않습니다. 컴파일러는 상수 전파로 실행 시점의 값이 미리 확정되는 조건문을 추려 내고, 그 조건상 결코 거치지 않는 분기까지 함께 들어냅니다.

이런 분석은 IL2CPP 빌드에서 C++ 컴파일러의 최적화 패스를 거치며 이루어지므로, 같은 일을 제한된 시간 안에 처리하는 JIT보다 더 넓은 범위의 죽은 코드를 짚어 걷어 낼 수 있습니다.

---

### 루프 최적화

앞의 두 기법이 함수와 분기를 겨냥했다면, C++ 컴파일러는 같은 코드를 수없이 되도는 루프에도 따로 손을 댑니다. 한 번의 손질이 반복 횟수만큼 곱절로 되갚아지는 자리인 만큼, 효과를 크게 볼 수 있는 지점입니다.

<br>

**루프 불변 코드 이동(Loop-Invariant Code Motion).**

매 반복마다 똑같은 값을 다시 셈하는 계산을 컴파일러가 알아채면, 그 계산을 루프 바깥으로 끌어내 한 번만 셈하도록 옮깁니다.

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

**루프 언롤링(Loop Unrolling).**

반복 횟수가 적고 미리 정해져 있는 루프라면, 컴파일러는 본문을 여러 벌 복사해 늘어놓아 루프 자체를 줄이거나 없앱니다. 그러면 반복을 돌 때마다 따라붙던 조건 비교와 카운터 증가, 되돌아가는 분기 같은 제어 비용을 그만큼 덜어 내게 됩니다.

<br>

**벡터화(Vectorization, SIMD).**

배열의 원소마다 똑같은 연산을 되풀이하는 루프는 **SIMD(Single Instruction, Multiple Data)** 명령어로 묶어, 명령 한 번에 여러 데이터를 나란히 처리하도록 바꿀 수 있습니다.

가령 네 개의 float에 같은 덧셈을 적용한다고 하면, 평범한 코드는 덧셈 명령을 네 번 따로 돌려야 합니다. SIMD 명령어는 이 넷을 한데 실어 단 한 번의 명령으로 동시에 더해 냅니다.

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
  <text fill="currentColor" x="260" y="325" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">Mono JIT는 이 최적화들을 제한적으로만 수행 → IL2CPP가 실행 성능에서 유리</text>
</svg>
</div>

---

## 코드 스트리핑

IL2CPP를 거쳐 얻는 이득은 빨라진 실행 속도만이 아닙니다. 빌드 결과물의 크기도 함께 줄어듭니다.

IL2CPP로 빌드하는 동안 Unity는 **코드 스트리핑(Code Stripping)**을 함께 돌립니다. 게임이 실제로 쓰지 않는 코드를 가려내, 최종 빌드에서 그 부분을 들어내는 작업입니다.

<br>

.NET 라이브러리에는 무수히 많은 클래스와 메서드가 들어 있지만, 한 게임이 그중 손대는 것은 일부에 지나지 않습니다.

코드 스트리핑은 프로그램이 처음 실행되는 진입점(entry point)에서 출발해, 거기서 부르는 코드, 다시 그 코드가 부르는 코드로 참조를 한 단계씩 짚어 나갑니다. 그렇게 따라가다 끝내 닿지 못한 코드는 어디서도 쓰이지 않는다고 보고 걷어 냅니다.

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

이렇게 걷어 내어 줄어드는 크기는 수 MB에서 수십 MB에 이릅니다.

이 차이는 모바일에서 특히 무게를 갖습니다. Google Play는 앱 크기가 200 MB를 넘어서면 내려받기 전에 경고를 띄우는데, 이 경고를 본 이용자가 설치를 단념하면서 이탈률이 올라가기 때문입니다.

<br>

다만 이렇게 참조를 따라가는 방식에는 함정이 하나 숨어 있는데, 바로 리플렉션(reflection)으로 코드를 실행 도중에 동적으로 끌어다 쓰는 경우입니다.

이런 호출은 빌드 시점의 정적 분석에 참조로 잡히지 않으니, 실제로는 쓰이는 코드인데도 스트리핑에 함께 걷어 내지곤 합니다.

가령 `Type.GetType("MyClass")`처럼 타입을 문자열 이름으로 찾아 쓰면, 그 이름은 실행 중에야 비로소 풀리는 값이라 스트리핑 도구로서는 `MyClass`가 어딘가에서 쓰인다는 단서를 잡을 길이 없습니다.

이렇게 잘려 나간 코드를 정작 런타임에 불러 쓰려 하면 `MissingMethodException`이나 `TypeLoadException` 같은 예외가 발생합니다.

`JsonUtility`나 Newtonsoft.Json 같은 JSON 직렬화 라이브러리도 객체의 프로퍼티를 리플렉션으로 더듬어 읽는 만큼 같은 덫에 걸리기 쉬우므로, 직렬화에 오르내리는 타입은 한층 눈여겨봐야 합니다.

<br>

이런 사고를 막으려면, 스트리핑이 건드리지 못하도록 살려 둘 대상을 미리 일러두면 됩니다.

Unity의 `link.xml`은 프로젝트의 Assets 폴더에 두는 XML 파일로, 코드 스트리핑에서 빼 둘 타입이나 어셈블리를 여기에 적어 두면 그대로 보존됩니다. 코드 쪽에서 해결하고 싶다면, 살려 둘 클래스나 메서드에 `[Preserve]` 어트리뷰트를 곧장 붙여 두는 길도 있습니다.

---

## 플랫폼별 런타임 제약

Mono와 IL2CPP 가운데 어느 쪽을 쓸지 늘 자유롭게 고를 수 있는 것은 아닙니다. 대상으로 삼은 플랫폼이 어떤 보안 정책을 두고 있는지, 또 어떤 아키텍처 위에서 도는지에 따라, 특정 런타임 방식만 허용되거나 한쪽이 아예 막히는 경우가 생깁니다.

---

### iOS: JIT 불가 → IL2CPP 필수

JIT 컴파일은 실행 도중에 기계어를 새로 만들어 메모리에 올리는 방식이라는 점을 앞서 짚었습니다. iOS에서 이 방식이 가로막히는 까닭이 바로 여기에 맞물립니다.

Apple은 iOS의 보안 정책상 **실행 시점에 새로 실행할 수 있는 코드를 메모리에 만들어 내는 일을 허용하지 않습니다**. JIT는 런타임에 기계어를 찍어 메모리에 얹는 과정이므로, 이 정책에 정면으로 걸려 막혀 버립니다.

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

그래서 iOS를 겨냥한 빌드라면 IL2CPP 말고는 길이 없습니다. Unity의 iOS 빌드 설정에서 Scripting Backend 항목에 IL2CPP만 고를 수 있게 막혀 있는 것도 결국 이 정책에서 비롯됩니다.

<br>

이 JIT 금지는 Unity로 만든 게임에만 적용되는 규칙이 아니라, iOS에서 도는 모든 서드파티 앱 프로세스에 똑같이 걸립니다. 다만 WKWebView로 웹 콘텐츠를 띄우는 경우는 사정이 다릅니다. WKWebView 안의 WebKit은 Apple이 직접 관리하는 별도의 WebContent 프로세스에서 도는데, 이 프로세스에서는 JIT가 열려 있어 Safari가 JIT를 쓸 수 있는 것도 같은 구조 덕입니다.

반면 JavaScriptCore를 앱 프로세스 안에 직접 끌어다 박아 넣으면, JIT 없이 인터프리터 모드로만 돌아가게 됩니다.

---

### Android: IL2CPP 권장

Android는 iOS처럼 JIT를 틀어막지는 않아, Mono 런타임도 그대로 쓸 수 있습니다. 그렇더라도 실무에서는 IL2CPP 쪽을 권하는데, 그 배경에는 성능과 정책을 비롯한 몇 가지 이유가 함께 얽혀 있습니다.

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

이 가운데 64비트 지원은 권장에 그치지 않는 출시 요건이기도 합니다. Google Play 스토어가 2019년 8월부터 새로 올리는 앱에 64비트(ARM64) 바이너리를 함께 담도록 요구하고 있는데, IL2CPP는 ARM64 네이티브 바이너리를 곧장 뽑아내므로 이 조건을 그대로 만족합니다.

<br>

그래서 개발하는 동안에는 에디터에서 Mono로 빠르게 코드를 고쳐 가며 돌려 보고, 정작 기기 테스트와 출시 빌드 단계에서는 IL2CPP로 넘어가는 흐름이 보통 자리잡습니다.

---

### WebGL: IL2CPP 필수

WebGL 빌드는 게임을 웹 브라우저 위에서 돌리기 위한 플랫폼입니다. 그런데 브라우저 안에서는 네이티브 바이너리를 곧바로 실행할 길이 없습니다. 그래서 Unity는 IL2CPP로 뽑아낸 C++ 코드를 **Emscripten** 컴파일러에 넘겨 **WebAssembly(Wasm)**라는 형식으로 다시 옮깁니다.

여기서 Emscripten은 C/C++ 코드를 브라우저가 실행할 수 있는 Wasm 바이너리로 바꿔 주는 도구를 말합니다.

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

WebGL에서 게임 코드는 브라우저가 둘러친 보안 샌드박스 안에 갇힌 채 돌아갑니다. 브라우저 엔진 자체야 JavaScript나 Wasm을 JIT 컴파일하지만, 그것은 어디까지나 엔진 내부에서 일어나는 일일 뿐, 바깥에서 들어온 코드가 제멋대로 기계어를 찍어 실행하도록 열어 두지는 않습니다. 따라서 Mono 런타임이 브라우저 안에서 JIT를 돌릴 길은 없고, IL2CPP로 AOT 컴파일하는 방법만 남게 됩니다.

<br>

브라우저 환경이 거는 제약은 런타임 방식에만 그치지 않습니다. 먼저 C# 수준의 멀티스레딩, 즉 `System.Threading`은 아예 쓸 수 없습니다. 이는 WebAssembly가 GC로 하여금 다른 스레드를 동기적으로 멈춰 세우는 메커니즘을 받쳐 주지 못하기 때문이며, 그나마 네이티브(C/C++) 수준의 스레딩만 실험적으로 열려 있는 정도입니다.

파일을 다루는 쪽도 좁아져, 파일 시스템 접근은 브라우저가 마련한 가상 파일 시스템 범위로 묶입니다. `Thread.Sleep`이나 동기적 파일 I/O처럼 메인 스레드를 붙잡아 멈추게 하는 패턴 역시 허용되지 않습니다. 여기에 브라우저가 내주는 메모리에도 상한이 걸려 있어, 큼직한 에셋을 한꺼번에 올리려 들면 메모리가 모자라 크래시로 이어질 수 있습니다.

---

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

모바일 게임을 개발할 때 최종 빌드가 IL2CPP로 묶인다는 말은, 우리가 짠 C# 코드가 IL을 거쳐 C++로 옮겨진 뒤 기계어가 되어 돌아간다는 뜻입니다. 그렇다면 리플렉션이 제한되고, 코드 스트리핑이 끼어들며, 제네릭이 빌드 시점에 미리 인스턴스화되어야 하는 IL2CPP 특유의 제약들을 머릿속에 둔 채 코드를 써야, 기기에서 흔들림 없이 도는 빌드를 손에 쥘 수 있습니다.

---

## 개발 워크플로

플랫폼마다 어떤 런타임이 강제되고 어떤 쪽이 막히는지까지 짚어 보았습니다. 그렇다면 실제 개발에서는 Mono와 IL2CPP를 어떻게 번갈아 엮어 쓰게 되는지, 그 흐름을 단계별로 따라가 보겠습니다.

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

결국 에디터에서는 Mono로 코드를 빠르게 고쳐 가며 개발하고, 기기로 넘긴 빌드에서는 IL2CPP가 안기는 성능과 플랫폼 호환성을 챙기는 구조인 셈입니다.

<br>

2단계에서 IL2CPP 빌드를 한 번씩 꾸준히 돌려 보는 까닭은, Mono에서는 멀쩡히 돌던 코드가 IL2CPP로 넘어가면 탈을 내기도 하기 때문입니다. 앞서 코드 스트리핑을 다루며 보았던, 리플렉션으로만 닿는 타입이 잘려 나가는 문제나, AOT 환경에서 특정 제네릭 인스턴스가 빠져 버리는 문제가 그 대표적인 사례입니다.

<br>

가령 `List<MyCustomStruct>`를 코드에서 직접 손대지 않고 리플렉션으로만 만들어 쓴다고 해 보겠습니다. 이 경우 AOT 컴파일러는 빌드 도중 그런 제네릭 인스턴스가 필요하다는 사실을 알아채지 못해 아예 만들어 두지 않고, 그 탓에 런타임에 막상 그 타입을 찾으면 `ExecutionEngineException`이 튀어나올 수 있습니다.

AOT 환경에서는 JIT와 달리 실행 도중에 새 제네릭 인스턴스를 즉석에서 찍어 낼 수가 없습니다. 그러므로 빌드 시점에 쓰일 제네릭 타입 조합은 하나도 빠짐없이 코드 어딘가에서 직접 참조되고 있어야 합니다. 코드에서 곧장 건드리지 않는 조합이 그래도 필요하다면, 그 조합을 한 번 써 보는 더미 코드를 끼워 두어 AOT 컴파일러가 해당 인스턴스를 만들어 두도록 떠밀 수 있습니다.

이런 종류의 문제는 출시를 코앞에 두고서야 드러나면 손보는 품이 훌쩍 불어나므로, 개발 초반부터 기기 빌드를 자주 돌려 미리 걸러 내는 편이 안전합니다.

---

## 마무리

C# 코드가 CPU 위에서 돌아가려면 기계어로 옮겨져야 하는데, 그 길목에는 IL이라는 중간 단계가 한 번 끼어듭니다. Unity는 이 변환을 Mono(JIT)와 IL2CPP(AOT) 두 런타임 가운데 하나에 맡깁니다.

- **IL(중간 언어)**은 C# 컴파일러가 소스 코드를 옮겨 낸 플랫폼 독립적 바이트코드를 가리킵니다. CPU가 곧바로 실행하지는 못하므로, 런타임이 한 번 더 기계어로 풀어내야 비로소 돌아갑니다.
- **Mono(JIT)**는 실행하는 도중에 IL을 기계어로 옮기는 방식으로, 빌드가 빠르고 에디터에서 즉시 돌려 볼 수 있습니다. 다만 메서드를 처음 부를 때 변환 비용이 들고 최적화의 깊이도 얕은 편에 머뭅니다.
- **IL2CPP(AOT)**는 빌드 단계에서 IL을 먼저 C++로 바꿔 두는데, 이어서 C++ 컴파일러가 인라인화와 데드 코드 제거, 루프 최적화를 두루 적용해 JIT보다 품질 높은 기계어를 뽑아냅니다. 빌드에 시간이 더 드는 대신 실행 성능은 한 수 앞섭니다.
- **코드 스트리핑**은 게임이 쓰지 않는 코드를 빌드에서 걷어 내 앱 크기를 줄여 줍니다. 다만 리플렉션으로 닿는 코드까지 함께 잘려 나갈 수 있어, 살려 둘 대상은 `link.xml`에 미리 적어 두어야 합니다.
- iOS와 WebGL은 JIT 자체가 막혀 있어 IL2CPP 말고는 길이 없고, Android에서도 실행 성능과 64비트 지원을 챙기려면 IL2CPP 쪽으로 기웁니다.

<br>

이 다섯 갈래를 가로지르는 한 가지 축은, 언제 그리고 어디까지 시간을 들여 IL을 기계어로 옮기느냐에 있습니다. 변환을 실행 시점까지 미루면 빌드는 가벼워지는 대신 첫 호출 비용과 최적화 한계를 떠안고, 빌드 시점에 미리 다 옮겨 두면 그 반대가 되기에, 결국 어느 쪽을 고르느냐는 대상 플랫폼과 우선순위에 따라 갈립니다.

<br>

이렇게 C# 코드가 컴파일을 거쳐 런타임 위에서 도는 과정을 짚어 둔 덕에, [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서 다루는 IL2CPP 환경의 실행 비용 분석으로 곧장 이어 갈 수 있습니다. 한편 런타임이 떠맡는 핵심 역할은 기계어 변환에 그치지 않는데, 그 가운데 또 하나가 바로 가비지 컬렉션입니다. 다음 글 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서는 GC가 어떻게 동작하는지, Unity의 Boehm GC가 어떤 특성을 띠는지, 그리고 GC 스파이크와 Incremental GC를 차례로 살펴봅니다.

<br>

---

**관련 글**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)

**시리즈**
- [C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)
- **C# 런타임 기초 (2) - .NET 런타임과 IL2CPP (현재 글)**
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
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
