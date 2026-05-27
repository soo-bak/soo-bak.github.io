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

[C# 런타임 기초 (1) - 값 타입과 참조 타입](/dev/unity/CSharpRuntime-1/)에서 값 타입은 데이터를 직접 저장하고 스택에 할당되며, 참조 타입은 힙에 객체가 할당되고 변수에 주소만 저장된다는 점을 살펴보았습니다. 이 타입 구분이 메모리 배치와 GC 비용을 결정합니다.

<br>

이전 글에서는 데이터가 메모리 어디에 저장되는가를 다루었다면, 이 글에서는 한 단계 나아가 "작성한 코드가 어떻게 CPU에서 실행되는가"를 다루며, 이 과정을 담당하는 것이 **런타임 시스템(Runtime System)**입니다.

"런타임"이라는 단어 자체는 "실행 시점"을 뜻하지만, 이 글에서는 코드 로딩, 기계어 변환, 메모리 관리, 예외 처리까지 담당하는 소프트웨어 계층을 가리킵니다. 같은 단어가 두 가지 뜻으로 쓰이는 이유는, 이 소프트웨어 계층이 바로 "실행 시점에 동작하는 시스템"이기 때문입니다.

CPU에서 게임 로직이 실행되려면 C# 소스 코드가 기계어(바이너리)로 변환되어야 하는데, C#은 C++처럼 소스 코드가 곧바로 기계어로 변환되는 구조가 아닙니다.

C#의 컴파일 결과물은 **IL(Intermediate Language)**이라는 중간 표현이며, 이 IL을 기계어로 변환하는 시점과 방식에 따라 런타임의 성격이 달라집니다.

<br>

이 변환 방식의 차이는 게임 성능에 직접 영향을 줍니다.

같은 C# 코드라도 런타임이 적용하는 최적화 수준(인라인화, 루프 벡터화 등)에 따라 생성되는 기계어의 품질이 달라지고, CPU 연산 속도가 바뀝니다. iOS처럼 실행 시점에 새 기계어를 생성하는 것 자체를 금지하는 플랫폼에서는 특정 런타임 방식을 아예 사용할 수 없습니다.

<br>

Unity에서는 두 가지 런타임 방식 중 하나를 선택하여 이 변환을 수행합니다.

실행 시점에 IL을 기계어로 변환하는 **Mono(JIT)**와, 빌드 시점에 IL을 C++로 변환한 뒤 네이티브 컴파일하는 **IL2CPP(AOT)**입니다.

두 방식은 빌드 시간, 실행 성능, 플랫폼 호환성에서 서로 다른 특성을 가지며, 대상 플랫폼에 따라 선택이 제한되기도 합니다.

이 글에서는 C# 코드가 기계어로 변환되는 과정, JIT와 AOT의 차이, Mono와 IL2CPP 비교, C++ 컴파일러 최적화, 코드 스트리핑, 플랫폼별 런타임 제약을 다룹니다.

---

## C# 컴파일 과정

C#은 **컴파일 언어**입니다. 작성한 코드를 실행하기 전에 컴파일러가 먼저 변환 작업을 수행합니다. 다만 C++처럼 소스 코드가 곧바로 기계어로 변환되지는 않습니다. C#의 컴파일 과정에는 **중간 단계**가 하나 존재합니다.

<br>

C# 컴파일러(Roslyn)는 소스 코드를 **IL(Intermediate Language, 중간 언어)**이라는 바이트코드로 변환합니다. IL은 CIL(Common Intermediate Language) 또는 MSIL(Microsoft Intermediate Language)이라고도 불립니다.

IL은 기계어가 아닙니다. CPU가 직접 실행할 수 없는, 플랫폼에 독립적인 중간 표현입니다.

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

IL을 중간에 두는 이유는 .NET의 설계 원칙인 **플랫폼 독립성** 때문입니다.

C#으로 작성한 코드를 Windows, Linux, macOS, iOS, Android 등 다양한 플랫폼에서 실행하려면, 각 플랫폼의 기계어가 다르므로 플랫폼마다 별도로 컴파일해야 합니다.

IL이라는 중간 단계를 두면 C# 컴파일러는 플랫폼과 무관한 IL만 생성하고, 기계어 변환은 각 플랫폼의 런타임이 맡습니다. 컴파일러와 런타임의 역할이 분리되는 구조입니다.

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

IL은 스택 기반의 명령어 집합으로 구성됩니다. 간단한 C# 코드가 IL로 변환된 결과를 보면 IL의 성격이 드러납니다.

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

IL은 바이트코드 형식이므로, 각 명령어(opcode)는 1바이트 또는 2바이트로 인코딩되며 명령어에 따라 피연산자(operand)가 추가로 붙습니다.

위 예시에서 `ldarg.0`은 첫 번째 인자를 **평가 스택(Evaluation Stack)**에 올리는 명령이고, `add`는 스택 최상단의 두 값을 꺼내 더한 뒤 결과를 다시 스택에 올리는 명령입니다.

평가 스택은 IL 명령어가 연산에 사용할 값을 임시로 쌓아두는 논리적 자료구조입니다. CPU에서 레지스터가 연산의 피연산자를 보관하는 역할과 비슷하지만, 레지스터는 이름으로 직접 접근하는 반면 평가 스택은 LIFO(후입선출) 방식으로만 접근합니다.

<br>

IL 자체는 CPU가 실행할 수 없으므로, 실행 전에 반드시 해당 플랫폼의 기계어로 변환되어야 합니다. 이 변환을 담당하는 것이 **런타임**이며, 변환 방식에 따라 **JIT(Just-In-Time)**와 **AOT(Ahead-Of-Time)**로 나뉩니다.

---

## JIT 컴파일 — Mono 런타임

**JIT(Just-In-Time) 컴파일**은 프로그램을 실행하는 시점에 IL을 기계어로 변환하는 방식입니다. Unity에서 이 JIT 변환을 담당하는 런타임이 **Mono**입니다.

<br>

Mono 런타임에서의 실행 흐름은 다음과 같습니다.

게임이 시작되고 특정 메서드가 처음 호출되면, Mono가 해당 메서드의 IL을 읽어 기계어로 변환합니다. 변환된 기계어는 메모리에 캐시되므로, 같은 메서드가 두 번째로 호출될 때는 변환 없이 캐시된 기계어를 바로 실행합니다.

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

이 JIT 방식은 빌드 속도, 첫 호출 비용, 최적화 깊이, 플랫폼 호환성 네 가지 측면에서 AOT 방식과 뚜렷한 차이를 보입니다.

<br>

**빌드 시간이 짧습니다.**

C# 컴파일러가 IL을 생성하면 빌드가 끝납니다. 기계어 변환은 실행 시점에 일어나므로 빌드 과정에 포함되지 않습니다. Unity 에디터에서 Play 버튼을 누르면 즉시 게임이 실행되는 것도, IL → C++ → 기계어로 이어지는 AOT 변환 단계 없이 IL을 그대로 로드하여 실행하기 때문입니다. 덕분에 코드를 수정하고 바로 테스트하는 빠른 이터레이션이 가능합니다.

<br>

**첫 호출 시 변환 비용이 발생합니다.**

메서드가 처음 호출될 때 JIT 컴파일러가 IL을 읽고 기계어를 생성하는 시간이 소요됩니다. 게임 시작 직후나 새 씬 로드 직후에 처음 호출되는 메서드들이 동시에 JIT 컴파일되면, 순간적으로 프레임 시간이 늘어날 수 있습니다. 한 번 컴파일된 메서드는 캐시되므로, 이후에는 이 비용이 발생하지 않습니다.

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

**최적화 수준에 한계가 있습니다.**

JIT 컴파일러는 실행 시점에 기계어를 생성해야 하므로, 변환에 쓸 수 있는 시간이 제한됩니다. 변환 시간이 길어지면 게임 실행이 그만큼 지연되기 때문입니다.

컴파일러가 기계어를 생성할 때 적용할 수 있는 대표적인 최적화 기법으로는, 짧은 메서드의 본문을 호출 지점에 직접 삽입하여 호출 비용을 제거하는 **인라이닝**, 반복문의 연산을 CPU의 SIMD 명령어로 묶어 한 번에 여러 데이터를 처리하는 **루프 벡터화**, 실행 경로에 도달할 수 없는 코드를 삭제하여 바이너리 크기와 분기 비용을 줄이는 **데드 코드 제거** 등이 있습니다.

Mono JIT는 인라이닝이나 데드 코드 제거를 기초적인 수준에서 수행하지만, 루프 벡터화 같은 고비용 최적화는 거의 적용하지 못합니다.

AOT 컴파일러는 빌드 시간에 여유가 있어 이런 최적화를 폭넓게 적용할 수 있는 반면, JIT 컴파일러는 빠르게 "충분히 쓸 만한" 기계어를 생성하는 데 초점을 맞춥니다.

<br>

**런타임에 새로운 코드를 생성합니다.**

JIT 컴파일은 실행 시점에 메모리에 실행 가능한 기계어를 새로 만들어 올리는 과정입니다.

운영체제는 메모리의 각 영역에 읽기, 쓰기, 실행 세 종류의 권한을 별도로 관리합니다.

JIT 컴파일러가 메모리에 기계어를 쓴 뒤 해당 영역에 실행 권한을 부여해야 CPU가 그 기계어를 실행할 수 있습니다.

iOS처럼 서드파티 앱이 메모리에 실행 권한을 동적으로 부여하는 것을 금지하는 플랫폼에서는 이 과정 자체가 차단되므로 JIT 방식을 사용할 수 없습니다.

---

## AOT 컴파일 — IL2CPP

**AOT(Ahead-Of-Time) 컴파일**은 프로그램을 빌드하는 시점에 IL을 기계어로 미리 변환하는 방식입니다. 실행 시점에는 이미 기계어가 완성되어 있으므로, JIT 변환 과정이 없습니다.

<br>

Unity에서 AOT 컴파일을 수행하는 파이프라인이 **IL2CPP**입니다.

IL2CPP는 "IL to C++"의 약자로, Unity가 자체 개발한 변환 도구입니다. IL을 직접 기계어로 변환하는 대신, IL을 먼저 **C++ 소스 코드**로 변환하고, 그 C++ 코드를 플랫폼의 네이티브 C++ 컴파일러(Clang, GCC, MSVC 등)로 컴파일하여 최종 기계어를 생성합니다.

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

IL2CPP가 IL을 C++로 변환하는 과정에서, C#의 class, struct, 메서드, 배열, 제네릭 등이 대응하는 C++ 코드로 생성됩니다. 사람이 읽을 수 있는 형태이지만 자동 생성된 코드라 가독성이 높지는 않습니다. 이렇게 생성된 C++ 코드를 플랫폼의 네이티브 컴파일러가 최적화하고 컴파일하여 최종 기계어를 만듭니다.

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

실행 시점에는 이미 기계어가 완성되어 있으므로, JIT 변환 비용이 없습니다. 게임 시작 직후 첫 프레임에서도 모든 메서드가 기계어로 즉시 실행됩니다.

<br>

IL2CPP가 IL을 C++로 변환하는 이유는 실용적인 비용 절감에 있습니다.

각 플랫폼(iOS, Android, Windows, WebGL 등)에 대한 기계어 코드 생성기(code generator)를 직접 만드는 대신, 이미 각 플랫폼에 존재하는 고품질 C++ 컴파일러(Clang, GCC, MSVC 등)를 활용합니다. 수십 년간 발전해 온 C++ 컴파일러의 코드 생성 능력과 최적화 역량을 빌리는 구조입니다.

---

## Mono vs IL2CPP 비교

앞에서 Mono(JIT)와 IL2CPP(AOT)의 동작 방식을 각각 살펴보았습니다. 두 런타임의 주요 특성을 정리하면 다음과 같습니다.

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

Mono 빌드는 C# 컴파일러가 IL을 생성하면 끝납니다.

IL2CPP 빌드는 여기에 IL → C++ 변환, C++ 컴파일이 추가되므로, 대규모 프로젝트에서는 수십 분에 이를 수 있습니다.

빌드 시간을 줄이려면, 이전 빌드와 같은 디렉터리에 빌드하여 C++ 컴파일러가 변경된 파일만 재컴파일하는 **증분 빌드(Incremental Build)**를 활용할 수 있습니다.

IL2CPP Code Generation 옵션을 Faster (Smaller) Builds로 설정하면 생성되는 C++ 코드량이 줄어들어 빌드 시간이 더 단축됩니다.

<br>

**실행 성능.**

Mono의 JIT 컴파일러는 실행 시점에 빠르게 기계어를 생성해야 하므로 복잡한 최적화에 시간을 쓸 수 없습니다.

반면 IL2CPP는 빌드 시점에 C++ 컴파일러가 충분한 시간을 들여 최적화하므로, 생성된 기계어의 품질이 더 높습니다.

수학 연산이 많은 게임 로직, 물리 시뮬레이션, AI 경로 탐색 등에서 IL2CPP가 Mono보다 빠른 실행 속도를 보이며, 수학 연산이나 루프가 집중된 코드에서 1.5배에서 2배의 속도 향상이 보고된 바 있습니다. 다만 이 수치는 코드 패턴에 따라 편차가 크며, I/O 중심 코드에서는 차이가 미미할 수 있습니다.

<br>

**코드 보호.**

Mono 빌드에서는 IL이 그대로 포함됩니다.

IL은 고수준 언어에 가까운 정보(클래스명, 메서드명, 변수명 등)를 보존하고 있어, ILSpy나 dnSpy 같은 도구로 쉽게 역컴파일됩니다.

IL2CPP 빌드에서는 C# 코드가 C++을 거쳐 기계어로 변환되므로, 원본 C# 코드의 구조가 상당 부분 사라집니다.

완전한 보호는 아니지만, 역공학 난이도가 크게 높아집니다.

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

Mono JIT는 실행 중에 빠르게 기계어를 생성해야 하므로 최적화에 쓸 시간이 제한되지만, IL2CPP는 빌드 시점에 C++ 컴파일러가 시간 제약 없이 최적화를 적용할 수 있습니다.

C++ 컴파일러가 적용하는 대표적인 최적화 기법은 다음과 같습니다.

---

### 인라인화 (Inlining)

함수를 호출하면 매개변수 전달, 스택 프레임 생성, 반환 등의 오버헤드가 발생하며, 함수 본문이 짧을수록 이 오버헤드가 실제 연산 비용에 비해 커집니다.

인라인화는 함수를 호출하는 대신 호출 지점에 함수 본문을 직접 삽입하여 이 오버헤드를 제거합니다.

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

인라인화의 효과는 호출 오버헤드 제거에 그치지 않습니다.

함수가 분리되어 있으면 컴파일러는 각 함수를 독립적으로 분석하지만, 인라인화로 함수 본문이 호출 지점에 합쳐지면 호출자의 문맥까지 함께 볼 수 있습니다.

위 예시에서 `multiplier`가 항상 `1.0f`라면, 컴파일러는 `baseSpeed * 1.0f`를 `baseSpeed`로 단순화할 수 있습니다.

`GetSpeed()`가 별도 함수일 때는 이런 최적화가 불가능하지만, 인라인화 후에는 호출자의 값이 보이므로 가능해집니다.

---

### 데드 코드 제거 (Dead Code Elimination)

실행 경로에서 도달할 수 없는 코드를 컴파일 결과에서 제거하는 최적화입니다.

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

단순한 `if (false)` 외에도, 컴파일러는 상수 전파를 통해 실행 시점에 값이 확정되는 조건문을 분석하고, 도달 불가능한 분기를 제거할 수 있습니다.

IL2CPP 빌드에서는 이 분석이 C++ 컴파일러의 최적화 패스로 수행되므로, JIT보다 더 넓은 범위의 데드 코드를 식별하고 제거합니다.

---

### 루프 최적화

인라인화와 데드 코드 제거 외에도, C++ 컴파일러는 루프에 대해 다양한 최적화를 수행합니다.

<br>

**루프 불변 코드 이동(Loop-Invariant Code Motion).**

루프 안에서 매 반복마다 같은 결과를 내는 계산을 루프 밖으로 이동시킵니다.

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

루프의 반복 횟수가 적고 고정적일 때, 루프 본문을 여러 번 복사하여 루프 제어(비교, 증가, 분기) 오버헤드를 줄입니다.

<br>

**벡터화(Vectorization, SIMD).**

배열의 각 요소에 같은 연산을 반복하는 루프를 **SIMD(Single Instruction, Multiple Data)** 명령어로 변환하여, 한 번의 명령어로 여러 데이터를 동시에 처리합니다.

예를 들어, 4개의 float 값에 같은 덧셈을 수행할 때, 일반 코드는 4번의 덧셈 명령을 실행하지만, SIMD 명령어는 1번의 명령으로 4개의 덧셈을 동시에 수행합니다.

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

IL2CPP의 이점은 실행 성능만이 아닙니다.

IL2CPP 빌드 과정에서 Unity는 **코드 스트리핑(Code Stripping)**도 수행합니다.

게임에서 실제로 사용하지 않는 코드를 식별하여 최종 빌드에서 제거하는 과정입니다.

<br>

.NET 라이브러리에는 수많은 클래스와 메서드가 포함되어 있지만, 대부분의 게임에서는 그 일부만 사용합니다.

코드 스트리핑은 진입점(entry point)에서 시작하여 참조를 따라가며, 실제로 도달 가능한 코드만 남기고 나머지를 제거합니다.

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

코드 스트리핑으로 줄어드는 크기는 수 MB에서 수십 MB에 이릅니다.

모바일에서는 이 차이가 큰데, Google Play 기준으로 앱 크기가 200 MB를 넘으면 다운로드 시 경고가 표시되어 이탈률이 높아집니다.

<br>

다만 코드 스트리핑에는 주의할 점이 있습니다.

리플렉션(reflection)을 통해 동적으로 접근하는 코드는 정적 분석에서 참조가 감지되지 않아 제거될 수 있습니다.

예를 들어, `Type.GetType("MyClass")`으로 문자열 기반으로 타입에 접근하면, 스트리핑 도구는 `MyClass`가 사용되고 있다는 사실을 인식하지 못합니다.

제거된 코드를 런타임에 사용하려 하면 `MissingMethodException`이나 `TypeLoadException`이 발생합니다.

JSON 직렬화 라이브러리(예: `JsonUtility`, Newtonsoft.Json)가 리플렉션으로 프로퍼티에 접근하는 경우에도 같은 문제가 발생할 수 있으므로, 직렬화 대상 타입은 특히 주의해야 합니다.

<br>

Unity의 `link.xml` 파일에 보존할 타입이나 어셈블리를 명시하면 이 문제를 방지할 수 있습니다.

`link.xml`은 프로젝트의 Assets 폴더에 배치하는 XML 파일로, 코드 스트리핑에서 제외할 대상을 지정합니다.

`[Preserve]` 어트리뷰트를 클래스나 메서드에 직접 적용하는 방법도 있습니다.

---

## 플랫폼별 런타임 제약

모든 플랫폼에서 Mono와 IL2CPP를 자유롭게 선택할 수 있는 것은 아닙니다.

보안 정책이나 플랫폼 아키텍처에 따라 특정 런타임 방식이 강제되거나 제한됩니다.

---

### iOS: JIT 불가 → IL2CPP 필수

앞서 JIT 컴파일이 "런타임에 새로운 코드를 생성한다"는 특성을 확인했습니다.

Apple의 iOS는 보안 정책상 **실행 시점에 새로운 실행 가능 코드를 메모리에 생성하는 것을 허용하지 않습니다**.

JIT 컴파일은 런타임에 기계어를 생성하여 메모리에 올리는 과정이므로, 이 정책에 의해 차단됩니다.

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

iOS 빌드에서는 반드시 IL2CPP를 사용해야 합니다.

Unity의 iOS 빌드 설정에서 Scripting Backend로 IL2CPP만 선택할 수 있는 것도 이 정책 때문입니다.

<br>

iOS의 JIT 금지 정책은 Unity 게임뿐 아니라 iOS의 모든 서드파티 앱 프로세스에 적용됩니다.

다만 WKWebView를 통해 웹 콘텐츠를 표시하면, WebKit이 Apple이 관리하는 별도의 WebContent 프로세스에서 실행되므로 해당 프로세스에서는 JIT가 허용됩니다.

Safari가 JIT를 사용할 수 있는 것도 이 구조 덕분입니다.

반면, JavaScriptCore를 앱 프로세스 내에 직접 임베드하면 JIT 없이 인터프리터 모드로만 동작합니다.

---

### Android: IL2CPP 권장

Android는 iOS와 달리 JIT를 금지하지 않으므로 Mono 런타임도 사용할 수 있지만, 실무에서는 IL2CPP가 권장됩니다.

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

Google Play 스토어는 2019년 8월부터 새로 제출하는 앱에 64비트(ARM64) 바이너리를 포함하도록 요구하고 있습니다. IL2CPP는 ARM64 네이티브 바이너리를 직접 생성하므로 이 요구를 충족합니다.

<br>

따라서 개발 중에는 에디터에서 Mono를 사용하여 빠르게 이터레이션하고, 기기 테스트와 출시 빌드에서 IL2CPP를 사용하는 워크플로가 일반적입니다.

---

### WebGL: IL2CPP 필수

WebGL 빌드는 게임을 웹 브라우저에서 실행하기 위한 플랫폼입니다.

브라우저 환경에서는 네이티브 바이너리를 직접 실행할 수 없으므로, Unity는 IL2CPP로 생성한 C++ 코드를 **Emscripten** 컴파일러를 통해 **WebAssembly(Wasm)**로 변환합니다.

Emscripten은 C/C++ 코드를 브라우저에서 실행 가능한 Wasm 바이너리로 변환하는 도구입니다.

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

WebGL에서는 브라우저의 보안 샌드박스 안에서 코드가 실행됩니다.

브라우저 자체는 JavaScript나 Wasm을 JIT 컴파일하지만, 이는 브라우저 엔진 내부의 동작이며 외부 코드가 임의로 기계어를 생성하여 실행할 수는 없습니다.

Mono 런타임이 브라우저 안에서 JIT 컴파일을 수행할 수 없으므로, IL2CPP를 통한 AOT 컴파일이 유일한 방법입니다.

<br>

런타임 방식 외에도 브라우저 환경에서 오는 제약이 있습니다.

C# 수준의 멀티스레딩(`System.Threading`)은 사용할 수 없는데, WebAssembly에서는 GC가 다른 스레드를 동기적으로 일시 정지시키는 메커니즘을 지원하지 않기 때문입니다.

네이티브(C/C++) 수준의 스레딩만 실험적으로 지원됩니다.

파일 시스템 접근은 브라우저의 가상 파일 시스템으로 제한되고, `Thread.Sleep`이나 동기적 파일 I/O처럼 메인 스레드를 블로킹하는 패턴도 사용할 수 없습니다.

브라우저가 할당하는 메모리에도 상한이 있어, 대규모 에셋을 한꺼번에 로드하면 메모리 부족으로 크래시가 발생할 수 있습니다.

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

모바일 게임 개발에서 최종 빌드가 IL2CPP로 만들어진다는 것은, C# 코드가 IL을 거쳐 C++로 변환된 뒤 기계어로 실행된다는 뜻입니다.

리플렉션 제한, 코드 스트리핑, 제네릭 인스턴스화 등 IL2CPP 환경의 제약을 인식한 상태에서 코드를 작성해야 안정적인 빌드가 가능합니다.

---

## 개발 워크플로

플랫폼별 제약까지 확인했으므로, 실무에서 Mono와 IL2CPP를 어떻게 조합하여 사용하는지 정리합니다.

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

에디터에서 Mono로 빠르게 개발하고, 기기 빌드에서 IL2CPP의 성능 이점과 플랫폼 호환성을 확보하는 구조입니다.

<br>

2단계에서 IL2CPP 빌드를 정기적으로 수행하는 이유는, Mono에서 정상 동작하던 코드가 IL2CPP에서 문제를 일으킬 수 있기 때문입니다.

코드 스트리핑 절에서 다룬 리플렉션 접근 타입의 제거 문제나, AOT 환경에서 특정 제네릭 인스턴스화가 누락되는 문제가 대표적입니다.

<br>

예를 들어, `List<MyCustomStruct>`를 코드에서 직접 사용하지 않고 리플렉션으로만 생성하면, AOT 컴파일러가 해당 제네릭 인스턴스를 생성하지 않아 런타임에 `ExecutionEngineException`이 발생할 수 있습니다.

AOT 환경에서는 JIT처럼 실행 시점에 새 제네릭 인스턴스를 만들 수 없으므로, 빌드 시점에 사용될 모든 제네릭 타입 조합이 코드에서 명시적으로 참조되어야 합니다.

직접 참조하지 않는 제네릭 조합이 필요하다면, 해당 조합을 사용하는 더미 코드를 작성하여 AOT 컴파일러가 인스턴스를 생성하도록 유도할 수 있습니다.

이런 문제를 출시 직전에 발견하면 수정 비용이 커지므로, 개발 초기부터 기기 빌드를 자주 수행하여 미리 잡아내는 것이 중요합니다.

---

## 마무리

C# 코드가 CPU에서 실행되려면 기계어로 변환되어야 하며, 이 변환 과정에는 IL이라는 중간 단계가 존재합니다. Unity에서는 Mono(JIT)와 IL2CPP(AOT) 두 가지 런타임 방식 중 하나를 선택하여 이 변환을 수행합니다.

- **IL(중간 언어)**은 C# 컴파일러가 소스 코드를 변환한 플랫폼 독립적 바이트코드입니다. CPU가 직접 실행할 수 없으며, 런타임이 기계어로 변환해야 합니다.
- **Mono(JIT)**는 실행 시점에 IL을 기계어로 변환합니다. 빌드가 빠르고 에디터에서 즉시 실행할 수 있지만, 첫 호출 시 변환 비용이 발생하고 최적화 수준에 한계가 있습니다.
- **IL2CPP(AOT)**는 빌드 시점에 IL을 C++로 변환한 뒤, C++ 컴파일러가 인라인화, 데드 코드 제거, 루프 최적화 등을 적용하여 JIT보다 품질 높은 기계어를 생성합니다. 빌드 시간은 길지만 실행 성능이 높습니다.
- **코드 스트리핑**은 사용되지 않는 코드를 빌드에서 제거하여 앱 크기를 줄입니다. 리플렉션으로 접근하는 코드가 제거될 수 있으므로 link.xml로 보존 대상을 지정해야 합니다.
- iOS와 WebGL에서는 JIT가 불가능하므로 IL2CPP가 필수이며, Android에서도 성능과 64비트 지원을 위해 IL2CPP가 권장됩니다.

<br>

C# 코드의 컴파일 과정과 런타임 방식을 이해했으므로, 이 지식은 [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서 다루는 IL2CPP 환경에서의 실행 비용 분석에 직접 연결됩니다. 다음 글에서는 런타임이 담당하는 또 다른 핵심 기능인 가비지 컬렉션을 다룹니다. [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 GC의 동작 원리, Unity의 Boehm GC 특성, GC 스파이크와 Incremental GC를 설명합니다.

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
