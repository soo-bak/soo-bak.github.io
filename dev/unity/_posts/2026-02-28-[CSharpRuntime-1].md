---
layout: single
title: "C# 런타임 기초 (1) - 값 타입과 참조 타입 - soo:bak"
date: "2026-02-28 01:46:00 +0900"
description: 값 타입과 참조 타입, 스택과 힙 메모리, 박싱과 언박싱, struct vs class 선택을 설명합니다.
tags:
  - Unity
  - C#
  - 런타임
  - 메모리
  - 모바일
---

## C# 런타임을 먼저 이해해야 하는 이유

Unity에서 C# 코드를 짜다 보면 대부분의 문법은 보이는 그대로 동작하는 것처럼 느껴집니다. `int score = 100;`이라고 적으면 변수에 값이 담기고, `new Enemy()`라고 적으면 적의 객체가 하나 만들어집니다.

그런데 이 두 줄이 메모리에서 하는 일은 전혀 다릅니다. 앞쪽은 스택에 4바이트를 곧장 적어 넣지만, 뒤쪽은 힙에 객체를 따로 만들어 두고 변수에는 그 객체의 주소만 적어 둡니다.

바로 이 차이가 가비지 컬렉터(GC)가 끼어드는지 아닌지를 가릅니다. 매 프레임 돌아가는 코드에서 힙 할당이 조금씩 누적되면, 어느 순간 GC가 깨어나 정리를 시작하면서 화면이 순간적으로 끊깁니다.

<br>

[스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서는 IL2CPP와 힙 할당 패턴, 오브젝트 풀링을 다루었고, [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서는 Boehm GC가 어떻게 돌아가는지와 GC 스파이크를 다루었습니다. 다만 그 두 시리즈를 끝까지 따라가려면, 값 타입과 참조 타입이 각각 어디에 놓이는지, 힙 할당이 왜 비용으로 돌아오는지, 박싱이 무엇인지를 먼저 손에 쥐고 있어야 합니다.

<br>

그래서 이 시리즈에서는 C# 코드가 실행되는 동안 메모리에서 무슨 일이 벌어지는지, 런타임이 그 코드를 어떻게 기계어로 바꾸는지, GC가 힙을 어떤 방식으로 정리하는지, 스레딩과 비동기가 Unity 안에서 어떤 제약에 묶이는지를 바닥부터 차근차근 짚어 나갑니다.

<br>

그 첫 글인 이번 편에서는 C# 타입 시스템의 밑바탕에 자리한 갈래, 곧 **값 타입(Value Type)**과 **참조 타입(Reference Type)**을 다룹니다. 두 타입을 어느 쪽으로 쓰느냐에 따라 데이터가 메모리 어디에 자리잡는지, 대입할 때 무엇이 복사되는지, 나아가 GC가 손대는 대상이 되는지가 달라집니다.

---

## 값 타입 (Value Type)

앞서 갈라 둔 두 갈래 가운데 먼저 살펴볼 쪽은 **값 타입(Value Type)**입니다. 값 타입은 데이터 자체를 변수 안에 곧장 담아 두는 타입으로, 변수가 곧 데이터인 셈입니다.

`int`, `float`, `bool`, `double`, `char` 같은 기본 숫자·논리 타입이 여기에 속하고, `struct`로 직접 선언한 사용자 정의 타입도 모두 값 타입입니다. Unity에서 자주 마주치는 `Vector3`, `Quaternion`, `Color`, `Ray`, `Bounds`도 내부적으로는 전부 struct, 곧 값 타입으로 정의되어 있습니다.

<br>

값 타입 변수 안에는 다른 곳을 가리키는 주소가 아니라 데이터가 그대로 담깁니다.

예를 들어 `int score = 100;`이라고 적으면, `score`라는 이름이 붙은 메모리 공간에 정수 `100`이 직접 기록됩니다. 어딘가에 따로 저장된 값을 찾아가는 주소가 아니라, 숫자 자체가 변수 자리에 그대로 들어앉습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 150" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text fill="currentColor" x="230" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">값 타입 변수의 메모리 배치</text>
  <text fill="currentColor" x="230" y="40" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.6">int score = 100;</text>
  <!-- score 변수 박스 -->
  <rect x="50" y="56" width="170" height="78" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="66" y="76" text-anchor="start" font-size="12" font-family="monospace" opacity="0.7">score</text>
  <!-- 값 내부 박스 -->
  <rect x="68" y="84" width="134" height="40" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="135" y="105" text-anchor="middle" font-size="15" font-weight="bold" font-family="monospace">100</text>
  <text fill="currentColor" x="135" y="120" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.5">(4 bytes)</text>
  <!-- 어노테이션 -->
  <text fill="currentColor" x="240" y="100" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.7">← 데이터 자체가</text>
  <text fill="currentColor" x="240" y="116" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.7">　 직접 저장됨</text>
</svg>
</div>

<br>

값 타입을 다른 변수에 대입하면 데이터 전체가 그대로 복사됩니다.

`int a = b;`라고 쓰면 `b`에 담긴 값이 `a`의 공간으로 통째로 옮겨 적힙니다. 이렇게 복사가 끝난 뒤에는 `a`를 아무리 바꿔도 `b`는 꿈쩍하지 않는데, 두 변수가 서로 다른 자리에 각자의 데이터를 따로 쥐고 있기 때문입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <text fill="currentColor" x="220" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">값 타입의 대입 (복사)</text>
  <text fill="currentColor" x="220" y="40" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.6">int b = a;  b = 20;  // a와 b는 독립적</text>
  <!-- a 변수 -->
  <text fill="currentColor" x="120" y="66" text-anchor="middle" font-size="12" font-family="monospace" opacity="0.7">a:</text>
  <rect x="60" y="74" width="120" height="50" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="120" y="105" text-anchor="middle" font-size="16" font-weight="bold" font-family="monospace">10</text>
  <text fill="currentColor" x="120" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">독립적인 복사본</text>
  <!-- b 변수 -->
  <text fill="currentColor" x="320" y="66" text-anchor="middle" font-size="12" font-family="monospace" opacity="0.7">b:</text>
  <rect x="260" y="74" width="120" height="50" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="320" y="105" text-anchor="middle" font-size="16" font-weight="bold" font-family="monospace">20</text>
  <text fill="currentColor" x="320" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">독립적인 복사본</text>
</svg>
</div>

<br>

`struct`로 묶은 값 타입에도 같은 규칙이 그대로 통합니다.

`Vector3 a = b;`라고 쓰면 `b`가 품고 있던 `x`, `y`, `z` 세 값, 곧 12바이트가 한 덩어리로 `a`에 복사됩니다. 복사된 `a`의 `x`를 99로 바꾸더라도 원본 `b`의 `x`는 그대로 남습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text fill="currentColor" x="260" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Vector3의 대입 (복사)</text>
  <text fill="currentColor" x="260" y="40" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">Vector3 b = a;  b.x = 99;  // 12바이트 전체 복사, b만 변경</text>
  <!-- a 변수 -->
  <text fill="currentColor" x="130" y="66" text-anchor="middle" font-size="12" font-family="monospace" opacity="0.7">a:</text>
  <rect x="50" y="74" width="160" height="134" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="130" y="100" text-anchor="middle" font-size="13" font-family="monospace">x = 1</text>
  <line x1="65" y1="110" x2="195" y2="110" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="130" y="132" text-anchor="middle" font-size="13" font-family="monospace">y = 2</text>
  <line x1="65" y1="142" x2="195" y2="142" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="130" y="164" text-anchor="middle" font-size="13" font-family="monospace">z = 3</text>
  <line x1="65" y1="174" x2="195" y2="174" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="130" y="196" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.5">(12 bytes)</text>
  <!-- b 변수 -->
  <text fill="currentColor" x="390" y="66" text-anchor="middle" font-size="12" font-family="monospace" opacity="0.7">b:</text>
  <rect x="310" y="74" width="160" height="134" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="390" y="100" text-anchor="middle" font-size="13" font-family="monospace">x = 99</text>
  <line x1="325" y1="110" x2="455" y2="110" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="390" y="132" text-anchor="middle" font-size="13" font-family="monospace">y = 2</text>
  <line x1="325" y1="142" x2="455" y2="142" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="390" y="164" text-anchor="middle" font-size="13" font-family="monospace">z = 3</text>
  <line x1="325" y1="174" x2="455" y2="174" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="390" y="196" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.5">(12 bytes)</text>
</svg>
</div>

<br>

이렇게 통째로 복사하는 동작은 메서드에 값을 넘길 때도 똑같이 일어납니다.

값 타입을 매개변수로 넘기면 원본이 아니라 그 복사본이 메서드로 건너가므로, 메서드 안에서 매개변수를 아무리 고쳐도 호출한 쪽의 원본은 그대로 보존됩니다.

<br>

다만 `ref`, `out`, `in` 키워드를 붙이면 값 타입이라도 복사 없이 참조로 넘길 수 있습니다.

`ref`는 메서드가 원본을 직접 읽고 쓰도록 열어 주고, `out`은 메서드 안에서 그 변수에 반드시 값을 채워 넣도록 강제합니다. `in`은 읽기 전용 참조로 넘겨, 복사를 피하면서도 원본을 건드리지 못하게 막습니다. 그래서 덩치 큰 struct를 매개변수로 넘길 때 `in`을 쓰면 복사에 드는 비용을 덜어낼 수 있습니다.

---

## 참조 타입 (Reference Type)

값 타입이 데이터를 변수 안에 직접 쥐고 있었다면, **참조 타입(Reference Type)**은 데이터를 다른 곳에 따로 두고 그것이 놓인 메모리 위치의 **주소(참조)**만 변수에 담아 둡니다. 변수를 열어 보면 값 자체가 아니라 "데이터는 저쪽 주소에 있다"고 알려 주는 이정표 하나가 들어 있는 셈입니다.

`class`로 직접 선언한 사용자 정의 타입을 비롯해 `string`, 배열(`int[]`, `GameObject[]` 등), 델리게이트(delegate)가 모두 참조 타입에 속합니다. Unity에서 늘 다루는 `MonoBehaviour`, `GameObject`, `Transform`, `Texture2D`도 전부 class로 정의되어 있어 참조 타입입니다.

<br>

참조 타입의 인스턴스는 `new` 키워드로 만듭니다.

`new`를 호출하면 객체의 실제 데이터는 **힙(Heap)**에 자리잡고, 변수에는 그 힙 위치를 가리키는 주소만 적힙니다. 데이터 본체와 그것을 가리키는 변수가 서로 다른 메모리 영역에 나뉘어 놓이게 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text fill="currentColor" x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">참조 타입 변수의 메모리 배치</text>
  <text fill="currentColor" x="300" y="40" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.6">Enemy enemy = new Enemy();</text>
  <!-- 스택/힙 레이블 -->
  <text fill="currentColor" x="125" y="64" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">스택</text>
  <text fill="currentColor" x="460" y="64" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">힙</text>
  <!-- 스택 박스 -->
  <rect x="30" y="74" width="190" height="120" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="48" y="96" text-anchor="start" font-size="12" font-family="monospace" opacity="0.7">enemy</text>
  <!-- 참조 내부 박스 -->
  <rect x="48" y="104" width="154" height="50" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="125" y="126" text-anchor="middle" font-size="12" font-family="monospace">0x00A0B4C0</text>
  <text fill="currentColor" x="125" y="143" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.55">(참조/주소)</text>
  <text fill="currentColor" x="125" y="184" text-anchor="middle" font-size="9" font-family="monospace" opacity="0.5">(4 or 8 bytes)</text>
  <!-- 화살표: 스택 → 힙 -->
  <line x1="220" y1="129" x2="335" y2="129" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="340,129 332,124 332,134" fill="currentColor"/>
  <!-- 힙 박스 -->
  <rect x="348" y="74" width="230" height="130" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="368" y="96" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">Enemy 인스턴스</text>
  <line x1="363" y1="104" x2="563" y2="104" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="368" y="124" text-anchor="start" font-size="12" font-family="monospace">hp = 100</text>
  <text fill="currentColor" x="368" y="144" text-anchor="start" font-size="12" font-family="monospace">attack = 15</text>
  <text fill="currentColor" x="368" y="164" text-anchor="start" font-size="12" font-family="monospace">name = "Goblin"</text>
  <text fill="currentColor" x="463" y="194" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(수십~수백 bytes)</text>
</svg>
</div>

<br>

변수 `enemy` 안에 들어 있는 것은 힙에 놓인 Enemy 인스턴스의 주소(`0x00A0B4C0`) 하나뿐이며, `hp`·`attack`·`name` 같은 실제 데이터는 모두 힙 쪽에 있습니다.

그래서 변수가 차지하는 크기는 객체가 얼마나 큰지와 무관하게 주소 하나만큼으로, 32비트 플랫폼에서는 4바이트, 64비트 플랫폼에서는 8바이트로 정해집니다.

<br>

참조 타입을 다른 변수에 대입하면 **데이터가 아니라 주소만** 복사됩니다.

`Enemy a = b;`라고 쓰면 `b`가 가리키던 힙 주소가 그대로 `a`에 옮겨 적혀, 두 변수가 **같은 힙 객체**를 함께 가리키게 됩니다. 그래서 `a`를 통해 데이터를 고치면 `b`로 읽어도 똑같이 바뀐 값이 나오는데, 애초에 둘이 같은 객체 하나를 보고 있기 때문입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text fill="currentColor" x="290" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">참조 타입의 대입 (참조 복사)</text>
  <text fill="currentColor" x="290" y="40" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.6">Enemy b = a;  b.hp = 50;  // 같은 객체를 공유, a.hp도 50</text>
  <!-- 스택/힙 레이블 -->
  <text fill="currentColor" x="100" y="64" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">스택</text>
  <text fill="currentColor" x="430" y="64" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">힙</text>
  <!-- 스택 박스 -->
  <rect x="30" y="74" width="140" height="100" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- a 참조 -->
  <rect x="45" y="86" width="110" height="30" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="100" y="106" text-anchor="middle" font-size="12" font-family="monospace">a (참조)</text>
  <!-- b 참조 -->
  <rect x="45" y="130" width="110" height="30" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="100" y="150" text-anchor="middle" font-size="12" font-family="monospace">b (참조)</text>
  <!-- 힙 박스 -->
  <rect x="320" y="74" width="230" height="100" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="340" y="96" text-anchor="start" font-size="12" font-weight="bold" font-family="sans-serif">Enemy 인스턴스</text>
  <line x1="335" y1="104" x2="535" y2="104" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="340" y="126" text-anchor="start" font-size="12" font-family="monospace">hp = 50</text>
  <text fill="currentColor" x="340" y="146" text-anchor="start" font-size="12" font-family="monospace">attack = 15</text>
  <!-- 화살표: a → 힙 -->
  <line x1="155" y1="101" x2="308" y2="101" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="313,101 305,96 305,106" fill="currentColor"/>
  <!-- 화살표: b → 힙 (수렴) -->
  <path d="M155 145 L235 145 L235 122 L308 122" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="313,122 305,117 305,127" fill="currentColor"/>
  <!-- 주석 -->
  <text fill="currentColor" x="435" y="200" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">a와 b가 같은 객체를 공유</text>
</svg>
</div>

<br>

같은 대입이라도 두 타입은 정반대로 움직입니다. 값 타입의 대입은 데이터를 통째로 베껴 서로 간섭하지 않는 독립된 사본을 남기지만, 참조 타입의 대입은 한 객체에 이름표를 하나 더 붙이는, 곧 같은 데이터를 공유하는 별명을 만들 뿐입니다.

<br>

참조 타입 가운데 `string`은 결이 조금 다른데, 참조 타입이면서도 한번 만들어진 내용은 더는 바꿀 수 없는 **불변(immutable)** 객체이기 때문입니다.

그래서 string을 "수정"한다고 해도 힙에 놓인 기존 객체가 고쳐지는 것이 아니라, 매번 새로운 string 객체가 힙에 따로 만들어집니다. 이런 까닭에 문자열을 거듭 이어 붙이다 보면 그때마다 새 객체가 힙에 쌓여 할당이 누적되며, 이는 다음 절에서 살펴볼 메모리 영역의 동작과 곧장 맞물립니다.

---

## 스택 메모리

값 타입과 참조 타입의 성능이 갈리는 까닭은 두 타입의 데이터가 서로 다른 메모리 영역에 놓이기 때문입니다. 그 영역이 바로 **스택(Stack)**과 **힙(Heap)**이며, 둘은 데이터를 다루는 방식이 근본부터 다릅니다.

<br>

먼저 스택은 함수 호출에 맞물려 저절로 관리되는 영역입니다.

어떤 함수가 호출되면 그 함수가 쓸 지역 변수와 매개변수, 그리고 호출이 끝난 뒤 돌아갈 위치를 적어 둔 반환 주소가 한 덩어리로 묶여 스택 위에 올라갑니다.

이렇게 함수 호출 한 번에 대응해 묶이는 메모리 블록을 **스택 프레임(Stack Frame)**이라고 부릅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <text fill="currentColor" x="280" y="22" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스택 프레임의 구조</text>
  <!-- 코드 -->
  <text fill="currentColor" x="30" y="60" font-family="monospace" font-size="12" opacity="0.6">void Attack(int damage)</text>
  <text fill="currentColor" x="30" y="78" font-family="monospace" font-size="12" opacity="0.6">{</text>
  <text fill="currentColor" x="30" y="96" font-family="monospace" font-size="12" opacity="0.6">    float multiplier = 1.5f;</text>
  <text fill="currentColor" x="30" y="114" font-family="monospace" font-size="12" opacity="0.6">    int total = ...;</text>
  <text fill="currentColor" x="30" y="132" font-family="monospace" font-size="12" opacity="0.6">}</text>
  <!-- 스택 레이블 -->
  <text fill="currentColor" x="430" y="54" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.6">스택</text>
  <!-- 스택 최상단 어노테이션 -->
  <text fill="currentColor" x="330" y="56" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.55">↑ 스택 최상단</text>
  <!-- Attack 스택 프레임 (강조: opacity 0.12) -->
  <rect x="330" y="62" width="200" height="155" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <!-- multiplier -->
  <rect x="345" y="72" width="170" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="430" y="91" text-anchor="middle" font-family="monospace" font-size="11">multiplier (4 bytes)</text>
  <!-- total -->
  <rect x="345" y="106" width="170" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="430" y="125" text-anchor="middle" font-family="monospace" font-size="11">total (4 bytes)</text>
  <!-- damage -->
  <rect x="345" y="140" width="170" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="430" y="159" text-anchor="middle" font-family="monospace" font-size="11">damage (4 bytes)</text>
  <!-- 반환 주소 -->
  <rect x="345" y="174" width="170" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="430" y="193" text-anchor="middle" font-family="monospace" font-size="11" opacity="0.6">반환 주소</text>
  <!-- 구분선 -->
  <line x1="330" y1="217" x2="530" y2="217" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.4"/>
  <!-- 호출한 함수의 스택 프레임 (보조: opacity 0.5) -->
  <rect x="330" y="225" width="200" height="55" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <text fill="currentColor" x="430" y="250" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.5">(호출한 함수의</text>
  <text fill="currentColor" x="430" y="268" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.5">스택 프레임)</text>
</svg>
</div>

<br>

스택이라는 이름은 그 동작 방식을 그대로 담고 있어, 가장 나중에 올라온 것이 가장 먼저 내려가는 **LIFO(Last-In, First-Out)** 구조를 가리킵니다.

가장 최근에 호출된 함수의 프레임이 늘 스택 최상단을 차지하다가, 그 함수가 끝나는 순간 최상단의 프레임부터 차례로 걷히게 됩니다.

가령 함수 A가 B를 부르고 B가 다시 C를 부르면 스택에는 A, B, C 순서로 프레임이 차곡차곡 올라가며, 이후 C가 끝나면 C의 프레임이 먼저 걷히고 뒤이어 B가 끝나면 B의 프레임도 걷혀 나갑니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <text fill="currentColor" x="360" y="22" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">함수 호출과 스택 변화</text>
  <!-- 1: A() 호출 -->
  <text fill="currentColor" x="72" y="52" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">A() 호출</text>
  <rect x="32" y="172" width="80" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="72" y="204" text-anchor="middle" font-family="monospace" font-size="12">A 프레임</text>
  <!-- 2: A → B() 호출 -->
  <text fill="currentColor" x="216" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">A → B()</text>
  <text fill="currentColor" x="216" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">호출</text>
  <rect x="176" y="120" width="80" height="50" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="216" y="150" text-anchor="middle" font-family="monospace" font-size="12">B 프레임</text>
  <rect x="176" y="172" width="80" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2" opacity="0.6"/>
  <text fill="currentColor" x="216" y="204" text-anchor="middle" font-family="monospace" font-size="12" opacity="0.6">A 프레임</text>
  <!-- 3: A → B → C() 호출 -->
  <text fill="currentColor" x="360" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">A → B → C()</text>
  <text fill="currentColor" x="360" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">호출</text>
  <rect x="320" y="68" width="80" height="50" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="360" y="98" text-anchor="middle" font-family="monospace" font-size="12">C 프레임</text>
  <rect x="320" y="120" width="80" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2" opacity="0.6"/>
  <text fill="currentColor" x="360" y="150" text-anchor="middle" font-family="monospace" font-size="12" opacity="0.6">B 프레임</text>
  <rect x="320" y="172" width="80" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2" opacity="0.6"/>
  <text fill="currentColor" x="360" y="204" text-anchor="middle" font-family="monospace" font-size="12" opacity="0.6">A 프레임</text>
  <!-- 4: C 종료 -->
  <text fill="currentColor" x="504" y="52" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">C 종료</text>
  <rect x="464" y="120" width="80" height="50" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="504" y="150" text-anchor="middle" font-family="monospace" font-size="12">B 프레임</text>
  <rect x="464" y="172" width="80" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2" opacity="0.6"/>
  <text fill="currentColor" x="504" y="204" text-anchor="middle" font-family="monospace" font-size="12" opacity="0.6">A 프레임</text>
  <!-- 5: B 종료 -->
  <text fill="currentColor" x="648" y="52" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">B 종료</text>
  <rect x="608" y="172" width="80" height="55" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="648" y="204" text-anchor="middle" font-family="monospace" font-size="12">A 프레임</text>
</svg>
</div>

<br>

이 모든 쌓고 걷는 과정은 **스택 포인터(Stack Pointer)**라는 레지스터 하나가 도맡습니다.

함수가 호출되면 CPU가 스택 포인터를 옮겨 그만큼의 공간을 확보하고, 함수가 끝나면 포인터를 원래 자리로 되돌려 그 공간을 한 번에 반납합니다.

할당이든 해제든 CPU 명령어 한두 개로 처리되어, 한 번에 수 나노초밖에 들지 않습니다.

<br>

스택에 올라간 데이터는 함수가 끝나는 순간 프레임째 사라지므로, 따로 해제해 주거나 GC가 손댈 일이 없습니다.

값 타입으로 선언한 지역 변수가 GC 대상에 들지 않는 것도 이렇게 함수와 수명을 함께하며 저절로 정리되기 때문입니다.

<br>

다만 스택이 쓸 수 있는 공간은 넉넉하지 않아, 대체로 스레드 하나당 **1MB** 안팎이 주어집니다.

이 한도를 넘기면 **StackOverflowException**이 던져집니다.

끝을 모르고 이어지는 재귀 호출이나, 수 KB가 넘는 큰 struct를 지역 변수로 잡는 경우라면 이 한계에 닿을 수 있습니다.

<br>

---

## 힙 메모리

스택이 함수 호출에 맞물려 저절로 관리되는 영역이었다면, **힙(Heap)**은 프로그램이 명시적으로든 암묵적으로든 요청해 둔 메모리가 자리잡는 영역입니다.

눈에 잘 띄는 통로는 `new` 키워드를 통한 명시적 할당이지만, 박싱이나 문자열 이어 붙이기처럼 코드 표면에는 드러나지 않는 암묵적 할당도 있습니다. 앞서 살펴본 참조 타입의 인스턴스, string 객체, 배열이 모두 이 힙에 놓입니다.

<br>

힙에 놓인 메모리는 함수가 끝나도 곧장 풀려나지 않습니다.

함수 A에서 만든 객체를 함수 B로 넘겨주면, B가 반환된 뒤에도 A가 그 객체를 계속 들여다봐야 할 수 있기 때문입니다. 그래서 힙 데이터의 수명을 가르는 기준은 함수의 시작과 끝이 아니라, 그 객체를 가리키는 **참조**가 살아 있는지 여부입니다.

<br>

힙에 쌓인 메모리를 거두어들이는 일은 **가비지 컬렉터(GC)**가 맡습니다.

GC는 이따금 힙을 훑으며 어디에서도 더는 가리키지 않는 객체를 골라내고, 그 자리를 회수해 다시 쓸 수 있게 돌려놓습니다. 개발자가 직접 해제 시점을 챙기지 않아도 된다는 점은 편하지만, GC가 도는 동안에는 그만큼의 성능 비용이 따라붙습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text fill="currentColor" x="320" y="22" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">힙 메모리 할당과 해제</text>
  <!-- 시점 1: 함수 실행 중 -->
  <text fill="currentColor" x="160" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.7">시점 1: 함수 실행 중</text>
  <text fill="currentColor" x="80" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">스택</text>
  <text fill="currentColor" x="220" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">힙</text>
  <!-- 스택 박스 (시점 1) -->
  <rect x="40" y="86" width="80" height="42" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="80" y="112" text-anchor="middle" font-family="monospace" font-size="12">e</text>
  <!-- 화살표 -->
  <line x1="120" y1="107" x2="170" y2="107" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,107 167,102 167,112" fill="currentColor"/>
  <!-- 힙 박스 (시점 1) -->
  <rect x="180" y="86" width="80" height="42" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="112" text-anchor="middle" font-family="monospace" font-size="12">Enemy</text>
  <!-- 코드 설명 -->
  <text fill="currentColor" x="160" y="152" text-anchor="middle" font-family="monospace" font-size="11" opacity="0.6">Enemy e = new Enemy();</text>
  <!-- 구분선 -->
  <line x1="320" y1="44" x2="320" y2="172" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3" opacity="0.4"/>
  <!-- 시점 2: 함수 종료 후 -->
  <text fill="currentColor" x="490" y="50" text-anchor="middle" font-size="12" font-family="sans-serif" opacity="0.7">시점 2: 함수 종료 후</text>
  <text fill="currentColor" x="410" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">스택</text>
  <text fill="currentColor" x="550" y="76" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.55">힙</text>
  <!-- 스택 박스 (시점 2, 해제됨) -->
  <rect x="370" y="86" width="80" height="42" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5"/>
  <text fill="currentColor" x="410" y="112" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.5">(해제)</text>
  <!-- 힙 박스 (시점 2, GC 대기) -->
  <rect x="510" y="86" width="80" height="42" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.5"/>
  <text fill="currentColor" x="550" y="112" text-anchor="middle" font-family="monospace" font-size="12" opacity="0.6">Enemy</text>
  <!-- GC 수거 대기 어노테이션 -->
  <text fill="currentColor" x="550" y="148" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">참조 없음</text>
  <text fill="currentColor" x="550" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">GC 수거 대기</text>
  <!-- 하단 설명 -->
  <rect x="95" y="200" width="450" height="62" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="320" y="223" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">함수 종료 → 스택의 참조 변수 e는 자동 해제</text>
  <text fill="currentColor" x="320" y="243" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.6">힙의 Enemy 인스턴스는 남아 있음 → GC가 나중에 회수</text>
</svg>
</div>

<br>

같은 할당이라도 힙은 스택보다 거쳐야 할 단계가 많습니다.

스택은 포인터를 한 칸 옮기면 그만이지만, 힙에서는 요청한 크기에 들어맞는 빈 자리를 먼저 찾아야 하고, 객체 헤더(타입 정보, 동기화 블록 등)를 초기화해야 하며, 메모리 관리에 쓰이는 메타데이터까지 갱신해야 합니다. 이렇게 손이 여러 번 가는 탓에, 한 번에 수 나노초로 끝나는 스택 할당과 달리 힙 할당은 수십에서 수백 나노초에 이릅니다.

<br>

대신 힙은 쓸 수 있는 크기의 제약이 스택만큼 빠듯하지 않습니다.

시스템 메모리가 허용하는 한도 안에서 얼마든지 넓어질 수 있는데, 다만 힙이 커진 만큼 GC가 한 번 돌 때 훑어야 할 범위도 그에 맞춰 넓어집니다.

<br>

|  | 스택 | 힙 |
|---|---|---|
| **할당** | 포인터 이동 (수 ns) | 빈 공간 탐색 (수십~수백 ns) |
| **해제** | 포인터 복원 (수 ns) | GC가 수거 (GC 실행 시 비용) |
| **크기** | ~1MB/스레드 | 시스템 메모리 범위 내 자유 |
| **GC 대상** | 아님 | 맞음 |
| **데이터 수명** | 함수 수명과 동일 | 참조가 살아 있는 동안 |

<br>

값 타입으로 잡은 지역 변수는 함수가 끝나는 순간 스택에서 곧바로 걷히지만, 참조 타입 인스턴스는 힙에 남아 GC가 거두어 갈 때까지 버팁니다. 바로 이 수명의 길이 차이가 두 타입의 성능 차이로 이어집니다.

<br>

Unity가 쓰는 GC(Boehm GC)는 힙을 세대로 갈라 두지 않는 비세대(non-generational) 방식이라, GC가 한 번 돌 때마다 힙 전체를 처음부터 끝까지 훑습니다. 그러니 힙에 객체가 많이 쌓여 있을수록 훑어야 할 범위가 넓어지고, GC가 한 사이클을 도는 데 걸리는 시간도 그만큼 길어집니다.

> 비세대 GC의 동작 원리는 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 자세히 다룹니다.

<br>

---

## 박싱과 언박싱

값 타입은 스택에 자리 잡는다고 앞에서 정리했지만, 코드를 어떻게 쓰느냐에 따라 그 값이 의도와 무관하게 힙으로 옮겨 가기도 합니다.

이렇게 값 타입과 참조 타입 사이를 오가는 변환을 각각 **박싱(Boxing)**과 **언박싱(Unboxing)**이라 부르며, 박싱이 일어날 때 스택에 있던 값이 힙으로 복사되면서 새 힙 할당이 생깁니다.

---

### 박싱 (Boxing)

박싱이 가능한 까닭은 C#의 타입 계층에 있습니다. `int`나 `float` 같은 값 타입까지 포함해 모든 타입이 최상위 타입인 `object`를 상속하기 때문입니다.

이 상속 관계가 받쳐 주므로 `object obj = score;`처럼 값 타입을 `object`나 인터페이스 타입 변수에 그대로 대입할 수 있습니다.

그리고 이 대입이 일어나는 순간, 런타임이 값을 참조 타입 형태로 감싸는 **박싱**을 수행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 660 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; width: 100%;">
  <text fill="currentColor" x="330" y="22" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">박싱 과정</text>
  <text fill="currentColor" x="330" y="46" text-anchor="middle" font-size="12" font-family="monospace" opacity="0.55">object boxed = score;  // 박싱 발생</text>
  <!-- 3단계 설명 -->
  <rect x="30" y="62" width="600" height="100" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="50" y="86" font-size="12" font-weight="bold" font-family="sans-serif">1단계</text>
  <text fill="currentColor" x="110" y="86" font-size="12" font-family="sans-serif" opacity="0.8">힙에 새 객체를 할당 (오브젝트 헤더 + 타입 정보 + 데이터 공간)</text>
  <text fill="currentColor" x="50" y="112" font-size="12" font-weight="bold" font-family="sans-serif">2단계</text>
  <text fill="currentColor" x="110" y="112" font-size="12" font-family="sans-serif" opacity="0.8">스택의 score 값(100)을 힙 객체의 데이터 공간에 복사</text>
  <text fill="currentColor" x="50" y="138" font-size="12" font-weight="bold" font-family="sans-serif">3단계</text>
  <text fill="currentColor" x="110" y="138" font-size="12" font-family="sans-serif" opacity="0.8">스택의 boxed 변수에 힙 객체의 주소를 저장</text>
  <!-- 스택/힙 레이블 -->
  <text fill="currentColor" x="130" y="190" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스택</text>
  <text fill="currentColor" x="480" y="190" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">힙</text>
  <!-- 스택 박스 -->
  <rect x="30" y="200" width="200" height="130" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- score 변수 -->
  <rect x="45" y="210" width="170" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="130" y="228" text-anchor="middle" font-size="12" font-family="monospace">score = 100</text>
  <text fill="currentColor" x="130" y="244" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.55">(4 bytes, 스택)</text>
  <!-- boxed 참조 -->
  <rect x="45" y="262" width="170" height="30" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="130" y="282" text-anchor="middle" font-size="12" font-family="monospace">boxed (참조)</text>
  <text fill="currentColor" x="130" y="326" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.55">값 복사 + 힙 할당 발생</text>
  <!-- 화살표: boxed → 힙 -->
  <line x1="230" y1="277" x2="356" y2="277" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="361,277 353,272 353,282" fill="currentColor"/>
  <!-- 힙 박스 -->
  <rect x="370" y="200" width="250" height="130" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="495" y="224" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.55">[오브젝트 헤더]</text>
  <line x1="385" y1="232" x2="605" y2="232" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="495" y="252" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.55">[타입 정보: Int32]</text>
  <line x1="385" y1="260" x2="605" y2="260" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="495" y="280" text-anchor="middle" font-size="13" font-weight="bold" font-family="monospace">값: 100</text>
  <line x1="385" y1="290" x2="605" y2="290" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="495" y="310" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">(총 약 12~24 bytes)</text>
</svg>
</div>

<br>

스택에서 4바이트면 충분하던 int 하나가 박싱을 거치면, 힙에서는 플랫폼에 따라 12~24바이트짜리 객체로 불어납니다.

32비트 플랫폼이라면 오브젝트 헤더 8바이트(동기화 블록 인덱스 4바이트와 타입 포인터 4바이트)에 데이터 4바이트가 더해져 12바이트에 이릅니다.

64비트 플랫폼으로 가면 헤더만 16바이트로 늘고 정렬 패딩까지 끼면서 24바이트까지 커집니다.

Unity가 주로 겨냥하는 64비트 모바일(ARM64) 환경이 바로 이 경우라, 스택에 두었을 때보다 6배 넓은 공간을 차지하게 됩니다.

<br>

박싱은 일어날 때마다 힙에 새 객체를 만들어 내고, 그 객체는 고스란히 GC의 관리 대상으로 넘어갑니다.

박싱이 한 번뿐이라면 부담이라 할 것도 없지만, 매 프레임 같은 코드가 반복되면 힙 할당이 차곡차곡 누적되어 GC 스파이크를 불러옵니다.

---

### 언박싱 (Unboxing)

박싱이 값을 힙 객체로 감싸는 과정이라면, 그 반대 방향이 **언박싱**입니다. 박싱되어 힙에 들어가 있던 객체에서 원래의 값 타입 데이터를 다시 꺼내 스택으로 복사해 옵니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text fill="currentColor" x="310" y="22" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">언박싱 과정</text>
  <text fill="currentColor" x="310" y="46" text-anchor="middle" font-size="12" font-family="monospace" opacity="0.55">int unboxed = (int)boxed;  // 언박싱</text>
  <!-- 2단계 설명 -->
  <rect x="30" y="62" width="560" height="70" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="50" y="86" font-size="12" font-weight="bold" font-family="sans-serif">1단계</text>
  <text fill="currentColor" x="110" y="86" font-size="12" font-family="sans-serif" opacity="0.8">boxed가 가리키는 힙 객체의 타입이 int인지 확인</text>
  <text fill="currentColor" x="50" y="112" font-size="12" font-weight="bold" font-family="sans-serif">2단계</text>
  <text fill="currentColor" x="110" y="112" font-size="12" font-family="sans-serif" opacity="0.8">힙 객체의 데이터를 스택의 unboxed 변수에 복사</text>
  <!-- 힙/스택 레이블 -->
  <text fill="currentColor" x="150" y="160" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">힙</text>
  <text fill="currentColor" x="480" y="160" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">스택</text>
  <!-- 힙 박스 -->
  <rect x="40" y="170" width="220" height="100" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="150" y="194" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.55">[오브젝트 헤더]</text>
  <line x1="55" y1="202" x2="245" y2="202" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="150" y="222" text-anchor="middle" font-size="11" font-family="monospace" opacity="0.55">[타입 정보: Int32]</text>
  <line x1="55" y1="230" x2="245" y2="230" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text fill="currentColor" x="150" y="254" text-anchor="middle" font-size="13" font-weight="bold" font-family="monospace">값: 100</text>
  <!-- 화살표: 힙 → 스택 (복사) -->
  <line x1="260" y1="220" x2="366" y2="220" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="371,220 363,215 363,225" fill="currentColor"/>
  <text fill="currentColor" x="314" y="212" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">복사</text>
  <!-- 스택 박스 -->
  <rect x="380" y="200" width="200" height="40" rx="6" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="480" y="224" text-anchor="middle" font-size="12" font-family="monospace">unboxed = 100</text>
  <text fill="currentColor" x="480" y="256" text-anchor="middle" font-size="10" font-family="monospace" opacity="0.55">(4 bytes, 스택)</text>
</svg>
</div>

<br>

언박싱 과정 자체는 힙에 새 객체를 만들지 않습니다. 이미 힙에 있는 데이터를 스택 쪽으로 옮겨 복사할 뿐이기 때문입니다.

다만 공짜는 아니라서, 타입이 맞는지 확인하고 데이터를 복사하는 만큼의 비용이 들고, 꺼내려는 타입이 실제 힙 객체의 타입과 어긋나면 `InvalidCastException`을 던집니다.

<br>

그렇다고 박싱된 객체가 언제나 언박싱으로 이어지는 것은 아닙니다. `object` 상태 그대로만 쓰이다가 참조가 끊기면, 언박싱 없이 GC가 그대로 거두어 갑니다.

<br>

따라서 성능 비용의 무게중심은 언박싱이 아니라 박싱 쪽에 있습니다. 언박싱을 하든 하지 않든, 힙 할당과 GC 부담을 만들어 내는 쪽은 어디까지나 박싱이기 때문입니다.

---

### 박싱이 발생하는 흔한 패턴

`object boxed = intValue;`처럼 박싱을 코드에 직접 적어 넣는 일은 흔치 않습니다.

성능에 부담을 주는 박싱은 대개 코드만으로는 드러나지 않게 **암묵적으로** 일어나며, 대표적으로 아래 네 가지 패턴에서 나타납니다.

<br>

**string.Format과 문자열 보간.**

첫 번째는 문자열을 조립할 때입니다. `string.Format`은 받아들이는 매개변수의 타입이 `object`라서, 값 타입 인자를 넘기는 순간 그 값이 박싱됩니다.

문자열 보간(`$"HP: {hp}/{maxHp}"`)도 안심할 수 없습니다. Roslyn 컴파일러가 이 보간 구문을 내부적으로 `string.Format` 호출로 풀어 주기 때문에, 결국 같은 박싱을 거치게 됩니다.

<br>

다만 이 동작은 런타임에 따라 달라집니다. .NET 6 이상에서는 `DefaultInterpolatedStringHandler`가 도입되어, 컴파일러가 보간 구문을 제네릭 `AppendFormatted<T>` 기반 코드로 바꿔 줌으로써 박싱을 없앴습니다.

그러나 Unity가 쓰는 런타임은 아직 이 핸들러를 지원하지 않습니다. 그래서 Unity 환경에서는 문자열 보간이 여전히 박싱을 유발합니다.

<br>

```csharp
// string.Format에서의 박싱:

int hp = 75;
int maxHp = 100;
string text = string.Format("HP: {0}/{1}", hp, maxHp);
// hp가 object로 박싱 (힙 할당 #1)
// maxHp가 object로 박싱 (힙 할당 #2)
// Format 결과 string 생성 (힙 할당 #3)
// → 한 줄에 힙 할당 3회
```

<br>

**비제네릭 컬렉션.**

두 번째는 오래된 컬렉션을 쓸 때입니다. `ArrayList`나 `Hashtable` 같은 비제네릭 컬렉션은 요소를 모두 `object` 타입으로 저장하므로, 값 타입을 하나 담을 때마다 그 값이 박싱을 거쳐 들어갑니다.

<br>

```csharp
// 비제네릭 컬렉션에서의 박싱:

ArrayList list = new ArrayList();
list.Add(42);       // 42가 object로 박싱 → 힙 할당
list.Add(3.14f);    // 3.14f가 object로 박싱 → 힙 할당


// 제네릭 컬렉션 (박싱 없음):

List<int> list = new List<int>();
list.Add(42);       // int 그대로 저장 → 박싱 없음
list.Add(99);       // int 그대로 저장 → 박싱 없음
```

<br>

**인터페이스로의 변환.**

세 번째는 값 타입을 인터페이스로 다룰 때입니다. struct가 어떤 인터페이스를 구현하고 있더라도, 그 값을 인터페이스 타입 변수에 대입하는 순간 박싱을 거치게 됩니다. 인터페이스 참조는 힙 객체를 가리키는 형태라야 성립하기 때문입니다.

<br>

```csharp
// 인터페이스 변환에서의 박싱:

struct MyStruct : IComparable<MyStruct>
{
    public int Value;
    public int CompareTo(MyStruct other) => Value.CompareTo(other.Value);
}

MyStruct s = new MyStruct { Value = 10 };
IComparable<MyStruct> comparable = s;    // 박싱 발생: 힙 할당
```

<br>

**Dictionary의 키로 struct를 사용할 때.**

마지막은 struct를 `Dictionary<TKey, TValue>`의 키로 쓸 때입니다. Dictionary는 키가 같은지 따지려고 `GetHashCode()`와 `Equals()`를 호출하는데, struct가 `IEquatable<T>`를 구현하지 않으면 기본 `object.Equals(object)` 오버로드로 넘어갑니다. 이 메서드의 매개변수 타입이 `object`라서, 비교가 일어날 때마다 struct 값이 박싱됩니다.

<br>

`GetHashCode()`까지 오버라이드하지 않으면 문제가 한 겹 더 쌓입니다. 이때는 기본 `ValueType.GetHashCode()` 구현이 동원되는데, 이 구현은 struct가 차지한 메모리를 바이트 단위로 훑어 해시 값을 만들려 합니다.

다만 struct 안에 참조 타입 필드가 섞여 있거나, 필드를 정렬하느라 생긴 패딩(빈 바이트)이 끼어 있으면 바이트 단위 해싱으로는 올바른 값을 얻지 못합니다. 그러면 런타임은 리플렉션으로 필드를 하나하나 읽어 가며 해시를 계산하는 느린 경로로 빠지고, 성능이 눈에 띄게 떨어집니다.

<br>

따라서 struct를 Dictionary 키로 쓸 생각이라면, `IEquatable<T>`를 구현하고 `GetHashCode()`를 함께 오버라이드해 두는 편이 좋습니다. 그래야 비교 때마다 생기던 박싱도, 느린 리플렉션 경로도 한꺼번에 막을 수 있습니다.

<br>

| 패턴 | 대안 |
|---|---|
| `string.Format("{0}", intValue)` | `StringBuilder.Append(int)` 또는 `int.ToString()` 직접 사용 |
| `ArrayList` / `Hashtable`에 값 타입 추가 | `List<T>` / `Dictionary<K,V>` (제네릭 컬렉션) |
| 값 타입을 인터페이스 변수에 대입 | 제네릭 메서드로 대체 (`where T : IComparable<T>`) |
| struct를 Dictionary 키로 사용 (`IEquatable<T>` 미구현 시) | `IEquatable<T>` 구현 + `GetHashCode()` 오버라이드 |

---

## struct vs class 선택 기준

같은 데이터를 담더라도 `struct`(값 타입)로 선언하느냐 `class`(참조 타입)로 선언하느냐에 따라 그 데이터가 메모리 어디에 놓이는지, 대입할 때 무엇이 복사되는지, GC가 관여하는지가 모두 달라집니다.

그래서 사용자 정의 타입을 만들 때는 둘 중 어느 쪽으로 선언할지부터 정해야 하며, 그 판단 기준을 데이터의 성격에 따라 살펴보겠습니다.

---

### struct가 적합한 경우

데이터가 작고, 한 번 만든 뒤 바뀌지 않으며, 잠깐 쓰고 사라지는 성격이라면 struct로 선언하는 편이 어울립니다.

<br>

**크기가 작은 경우.**

데이터 크기가 **16바이트 이하**라면 struct가 무난한 선택입니다.

struct는 대입할 때 담긴 값 전체가 그대로 복사되기에, 크기가 커질수록 복사에 드는 비용도 함께 늘어납니다.

Microsoft의 .NET 설계 가이드라인(Choosing Between Class and Struct)이 굳이 16바이트를 경계로 삼는 까닭은, x64 환경에서 이 정도 크기까지는 레지스터를 두 번 옮기는 것만으로 복사가 끝나기 때문입니다.

이 범위 안에서는 참조만 복사하는 대신 힙 할당과 GC 비용을 떠안는 쪽보다 전체적으로 더 가볍게 끝납니다.

<br>

물론 16바이트를 넘어가면 복사 비용이 늘어나지만, 이 수치를 넘었다고 해서 무조건 class로 가야 한다는 뜻은 아닙니다.

실제로 Unity의 `Ray`(24B)나 `Bounds`(24B)는 16바이트를 훌쩍 넘기면서도 struct로 정의되어 있습니다.

복사 비용이 조금 더 들더라도 힙 할당과 GC를 아예 거치지 않는 쪽이 전체 성능에는 더 이득이기 때문입니다.

<br>

```csharp
// struct 크기와 복사 비용:

Vector3 (12 bytes): x, y, z  // → 복사 비용 낮음
Color32 (4 bytes):  r, g, b, a  // → 복사 비용 낮음

struct LargeData (128 bytes) // : 여러 필드  → 복사 비용 높음
                             //             → class가 적합할 수 있음
```

<br>

**불변(immutable)인 경우.**

한 번 만든 뒤 필드를 고치지 않는 불변(immutable) 데이터에도 struct가 잘 맞습니다.

struct는 대입할 때 값 전체가 복사되므로, 필드를 바꿀 수 있는 가변(mutable) struct는 복사본을 고쳐도 원본은 그대로 남습니다.

class처럼 원본까지 함께 바뀔 것으로 기대하다 보면 추적하기 어려운 버그로 이어지기에, struct는 처음부터 불변으로 설계해 두는 편이 안전합니다.

<br>

**수명이 짧은 경우.**

함수 안에서 잠깐 만들어 쓰고 함수가 끝나면 더 둘 필요가 없는 데이터라면, 스택에 올라가는 struct가 유리합니다.

스택에 올라간 값은 힙 할당도 GC 관여도 없어, 매 프레임 새로 만들어도 GC를 압박하지 않게 됩니다.

<br>

---

### class가 적합한 경우

반대로 데이터가 크거나, 여러 곳이 같은 값을 함께 봐야 하거나, 다형성이나 긴 수명이 필요한 경우라면 class가 어울립니다.

<br>

**크기가 큰 경우.**

필드가 많아 수십에서 수백 바이트에 이르는 데이터는 class로 선언하는 편이 낫습니다.

class는 대입할 때 참조, 즉 객체의 주소만 복사하기 때문에, 객체가 아무리 커져도 복사 비용은 4~8바이트로 늘 일정하게 유지됩니다.

<br>

**참조를 공유해야 하는 경우.**

같은 데이터를 여러 곳에서 함께 바라보고, 한쪽에서 고친 내용이 다른 쪽에도 그대로 비쳐야 하는 상황이라면 class가 맞습니다.

게임의 전체 상태를 다루거나 매니저 패턴을 구성할 때 흔히 이런 요구가 따라옵니다.

<br>

**다형성(Polymorphism)이 필요한 경우.**

다형성은 같은 메서드를 호출하더라도 객체의 실제 타입에 따라 서로 다른 동작이 일어나는 성질로, 상속을 토대로 구현됩니다.

struct는 상속을 지원하지 않으므로, `virtual` 메서드나 `abstract` 클래스처럼 다형성에 기대는 설계는 모두 class로 풀어야 합니다.

<br>

**수명이 긴 경우.**

씬 내내 살아 있어야 하거나 여러 프레임에 걸쳐 상태를 이어가야 하는 오브젝트라면, 힙에 자리 잡는 class가 어울립니다.

---

### Unity에서의 예시

앞서 정리한 기준이 실제로 어떻게 적용되는지는 Unity가 내장 타입을 struct와 class로 나눠 둔 모습에서 잘 드러납니다.

<br>

**struct (값 타입):**

| 타입 | 크기 | 용도 |
|---|---|---|
| Vector3 | 12B | 위치, 방향, 크기 |
| Vector2 | 8B | 2D 좌표, UV |
| Quaternion | 16B | 회전 |
| Color | 16B | 색상 (float 채널) |
| Color32 | 4B | 색상 (byte 채널) |
| Ray | 24B | 광선 (원점 + 방향) |
| Bounds | 24B | 바운딩 박스 (중심 + 크기) |
| RaycastHit | 44~52B | 레이캐스트 결과 |

**class (참조 타입):**

| 타입 | 용도 |
|---|---|
| GameObject | 씬의 오브젝트 (컴포넌트 컨테이너) |
| Transform | 위치/회전/크기 관리 (계층 구조) |
| MonoBehaviour | 사용자 스크립트의 기반 클래스 |
| Texture2D | 텍스처 데이터 |
| Material | 렌더링 머티리얼 |
| Mesh | 메쉬 데이터 |

<br>

`Vector3`은 12바이트밖에 안 되는 작은 데이터로, 위치나 방향을 잠깐 담는 임시 값으로 수없이 오갑니다.

`Transform.position`이 돌려준 Vector3를 손봐도 원본 Transform의 위치까지 따라 바뀌면 곤란하므로, 대입할 때마다 독립된 복사본을 떼어 주는 struct가 알맞습니다.

<br>

반면 `GameObject`는 여러 컴포넌트를 담는 컨테이너라 덩치가 크고, 상속을 토대로 한 구조를 갖습니다.

한 스크립트에서 `GameObject.SetActive(false)`를 호출했을 때 그 오브젝트를 가리키던 모든 곳에서 비활성화가 함께 비쳐야 하므로, 참조를 나눠 갖는 class가 알맞습니다.

<br>

|  | struct | class |
|---|---|---|
| **메모리 위치** | 스택 (지역 변수일 때) | 힙 |
| **대입 동작** | 전체 복사 | 참조(주소) 복사 |
| **GC 관여** | 없음 (스택 할당 시) | 있음 |
| **크기 기준** | 16바이트 이하 | 제한 없음 |
| **상속** | 불가 | 가능 |
| **null 가능** | 불가 (Nullable 제외) | 가능 |
| **복사 비용** | 크기에 비례 | 4~8바이트 고정 |
| **적합한 용도** | 좌표, 색상, 결과 값 | 게임 오브젝트, 매니저 |

<br>

다만 값 타입이 필드로 참조 타입을 끌어안고 있다면, 가령 struct 안에 string 필드가 들어 있다면, struct 본체는 스택에 놓이더라도 그 string은 따로 힙에 자리를 잡습니다.

그러니 struct로 선언했다고 해서 그 안의 모든 데이터가 통째로 스택에 머무는 것은 아니며, GC 비용을 덜어 내는 이점을 온전히 누리려면 struct 내부에 참조 타입 필드를 두지 않는 편이 좋습니다.

<br>

struct가 어디에 놓이는지도 한 번 짚고 넘어갈 만합니다.

struct가 스택에 올라가는 것은 어디까지나 **지역 변수**로 선언했을 때에 한합니다.

class의 필드로 선언한 struct는 그 class 인스턴스를 따라 **힙**에 함께 놓이고, 배열의 요소로 들어간 struct도 배열 자체가 힙에 있는 탓에 결국 힙에 자리합니다.

<br>

```csharp
// struct의 할당 위치:

// 1. 지역 변수 → 스택
void Update()
{
    Vector3 dir = Vector3.forward;    // 스택에 할당
}

// 2. class 필드 → 힙 (class 인스턴스와 함께)
class Player : MonoBehaviour
{
    Vector3 spawnPosition;            // Player 인스턴스가 힙에 있으므로
                                      // spawnPosition도 힙에 존재
}

// 3. 배열 요소 → 힙 (배열이 힙에 있으므로)
Vector3[] waypoints = new Vector3[10]; // 배열 전체가 힙에 할당
                                       // 각 Vector3도 힙에 존재
```

<br>

큰 struct를 넘길 때 쓰는 `in` 매개변수는, 복사 비용을 아끼려고 값을 참조로 건네면서도 원본만큼은 건드리지 않겠다고 약속해 둡니다.

그런데 일반 struct의 메서드는 내부에서 필드를 고칠 여지가 있고, 컴파일러로서는 그 메서드가 정말로 필드를 고치는지 미리 알아낼 길이 없습니다.

그래서 `in` 매개변수나 `readonly` 변수를 통해 struct의 메서드를 부를 때, 컴파일러는 원본을 지키려고 매번 복사본을 따로 떠서 그 복사본에 대고 메서드를 돌립니다.

이렇게 컴파일러가 몰래 떠 두는 복사본을 **방어적 복사(defensive copy)**라고 부릅니다.

<br>

이 복사는 코드 어디에도 적혀 있지 않아 알아차리기 어려운 데다, 큰 struct에서 메서드를 거듭 호출하다 보면 `in`으로 줄이려던 복사 비용이 도리어 불어납니다.

대신 `readonly struct`로 선언해 두면 모든 필드가 바뀌지 않음이 보장되기에, 컴파일러는 방어적 복사를 아예 건너뜁니다.

그러니 `in` 매개변수와 짝지어 쓸 struct라면 `readonly struct`로 선언해 두는 편이 안전합니다.

<br>

박싱 한 번이 일으키는 힙 할당 비용은 그 자체로는 거의 무시해도 좋을 만큼 작습니다.

정작 발목을 잡는 쪽은 `Update()`처럼 매 프레임 도는 코드, 곧 **핫 패스(hot path)**에서 박싱이 끝없이 되풀이될 때입니다.

프레임마다 힙 할당이 누적되면 GC가 그만큼 자주 끼어들고, GC 스파이크가 일면서 프레임이 떨어지게 됩니다.

반대로 초기화 코드나 이벤트 핸들러처럼 어쩌다 한 번 도는 경로라면 박싱이 한두 번 일어나도 누적될 틈이 없어, 성능에는 거의 흔적을 남기지 않습니다.

그래서 이 글에서 다룬 struct와 class 선택, 그리고 박싱을 피하는 원칙은 핫 패스에 힘을 모아 적용하고, 어디를 손볼지는 Unity Profiler로 진짜 병목을 짚어 본 뒤에 정하는 것이 옳습니다.

측정도 없이 모든 코드를 싸잡아 최적화하려 들면 코드만 복잡해질 뿐입니다.  

---

## 마무리

- 값 타입(int, float, struct 등)은 데이터를 변수 안에 곧장 담아 두며, 대입할 때 그 값 전체가 복사됩니다. 지역 변수로 선언하면 스택에 올라가, 함수가 끝나는 순간 GC의 손을 거치지 않고 저절로 걷힙니다.
- 참조 타입(class, string, array 등)은 객체 본체를 힙에 두고, 변수에는 그 위치를 가리키는 주소만 담깁니다. 그래서 대입하면 주소만 옮겨 적혀, 두 변수가 같은 객체 하나를 함께 가리키게 됩니다.
- 스택은 포인터를 한 칸 옮기는 것만으로 할당과 해제가 끝나 비용이 거의 들지 않지만, 힙은 빈 자리를 찾아야 하고 다 쓴 메모리를 GC가 거두어 가야 하는 만큼 비용이 더 무겁습니다.
- 박싱은 값 타입을 object나 인터페이스 타입으로 옮길 때 힙에 새 객체를 만들어 냅니다. string.Format이나 문자열 보간, 비제네릭 컬렉션, 인터페이스 변환처럼 코드 표면에 드러나지 않는 자리에서 암묵적으로 일어납니다.
- struct는 16바이트 안팎의 작고 바뀌지 않는 데이터에 어울리고, class는 같은 값을 여러 곳이 공유하거나 다형성이 필요한 데이터에 어울립니다. 다만 struct가 스택에 놓이는 것은 지역 변수일 때뿐이며, class의 필드나 배열 요소로 들어가면 힙에 자리잡습니다.
- 큰 struct를 `in` 매개변수로 넘길 때는 `readonly struct`로 선언해, 컴파일러가 몰래 떠 두는 방어적 복사를 막아 두는 편이 좋습니다.
- 이런 원칙이 무게를 갖는 곳은 매 프레임 도는 핫 패스이므로, 어디를 손볼지는 Unity Profiler로 진짜 병목을 짚어 본 뒤에 정하는 것이 옳습니다.

이 모든 갈래는 결국 하나의 질문, 곧 데이터가 메모리 어디에 놓이느냐로 모입니다. 같은 데이터라도 스택에 두면 함수와 수명을 함께하며 GC를 비켜 가지만, 힙에 두면 GC가 거두어 갈 때까지 남아 그만큼의 부담을 남기기에, 타입을 고르는 일은 곧 그 데이터를 어느 메모리에 맡길지 정하는 일과 같습니다.

<br>

값 타입과 참조 타입이 메모리에서 움직이는 방식은 [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)의 GC 할당 최소화 전략과 [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)의 GC 원리를 따라가는 밑바탕이 됩니다. 이어지는 [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서는 우리가 짠 C# 코드가 IL을 거쳐 기계어로 바뀌어 가는 과정과, Mono와 IL2CPP가 어떻게 갈리는지를 살펴봅니다.

<br>

---

**관련 글**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)

**시리즈**
- **C# 런타임 기초 (1) - 값 타입과 참조 타입 (현재 글)**
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
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
- **C# 런타임 기초 (1) - 값 타입과 참조 타입** (현재 글)
- [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)
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
