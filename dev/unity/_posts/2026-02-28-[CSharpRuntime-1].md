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

Unity의 게임 로직은 대부분 C#으로 작성됩니다. 따라서 성능을 이해하려면 코드가 어떤 순서로 실행되는지만 보는 것으로는 부족합니다. 값이 메모리의 어디에 놓이는지, 객체 생성이 언제 힙 할당으로 이어지는지, GC가 어떤 대상을 회수하는지도 함께 알아야 합니다.

예를 들어 일반적인 지역 변수 `int score = 100;`은 변수 자리에 정수 값 자체를 저장합니다. 반면 `new Enemy();`는 관리 힙에 `Enemy` 객체를 만들고, 변수에는 그 객체를 가리키는 참조를 저장합니다. 두 코드는 모두 C# 한 줄이지만, 런타임이 처리하는 방식은 다릅니다.

이 차이는 GC 비용과 직접 연결됩니다. 힙에 만들어진 객체는 더 이상 사용되지 않더라도 즉시 사라지지 않고, 나중에 GC가 회수해야 합니다. 매 프레임 실행되는 코드에서 이런 할당이 반복되면 GC가 동작하는 순간 메인 스레드가 잠시 멈출 수 있고, 그 결과 프레임이 끊겨 보일 수 있습니다.

> IL2CPP 백엔드와 힙 할당 패턴, 오브젝트 풀링은 [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서, Boehm GC의 동작과 GC 스파이크 대응은 [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서 자세히 다룹니다.

이번 글에서는 C# 타입 시스템의 기본 구분인 **값 타입(Value Type)**과 **참조 타입(Reference Type)**을 기준으로, 데이터가 메모리에 놓이는 방식과 대입할 때 복사되는 대상이 어떻게 달라지는지 살펴봅니다. 이어서 값 타입이 `object`나 인터페이스로 다뤄질 때 발생하는 박싱이 왜 힙 할당으로 이어질 수 있는지도 함께 정리합니다.

---

## 값 타입 (Value Type)

먼저 볼 것은 **값 타입(Value Type)**입니다. 값 타입은 변수의 메모리 공간 안에 데이터 자체를 저장합니다. 변수의 메모리 공간이 곧 그 값의 저장 공간이 됩니다.

`int`, `float`, `bool`, `double`, `char` 같은 기본 숫자·논리 타입이 여기에 속합니다. `struct`로 정의한 사용자 정의 타입도 값 타입이며, Unity에서 자주 사용하는 `Vector3`, `Quaternion`, `Color`, `Ray`, `Bounds`도 모두 struct로 정의되어 있습니다.

예를 들어 `int score = 100;`이라고 선언하면 `score` 변수의 메모리 공간에 정수 값 `100`이 직접 저장됩니다. 이 과정에서 별도의 객체가 만들어지지는 않습니다.

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

값 타입을 다른 변수에 대입하면 데이터 전체가 복사됩니다. `int a = b;`라고 쓰면 `b`에 저장된 값이 `a`의 메모리 공간으로 복사되어, 두 변수는 같은 값을 각자 따로 저장합니다.

복사가 끝난 뒤에는 한쪽 값을 바꿔도 다른 쪽은 바뀌지 않습니다. `a`와 `b`가 서로 다른 메모리 공간에 독립적인 값을 가지고 있기 때문입니다.

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

이 규칙은 `struct`로 만든 값 타입에도 그대로 적용됩니다. 예를 들어 `Vector3 a = b;`라고 쓰면 `b`의 `x`, `y`, `z` 필드가 모두 `a`로 복사됩니다. `Vector3`는 세 개의 `float`를 가지므로 일반적으로 12바이트가 복사됩니다.

복사된 두 인스턴스는 서로 독립적입니다. `a.x`를 99로 바꿔도 `b.x`는 그대로 남습니다. 두 변수는 같은 객체를 공유하는 것이 아니라, 같은 필드 값을 가진 별도의 값 타입 인스턴스이기 때문입니다.

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

값 타입을 메서드에 전달하면, 메서드는 원본 값을 직접 다루지 않습니다. 호출하는 쪽의 값이 복사되어 매개변수에 들어갑니다.

따라서 메서드 안에서 매개변수 값을 변경해도 호출한 쪽의 원본은 바뀌지 않습니다. 메서드 내부의 매개변수와 호출한 쪽의 변수는 서로 다른 메모리 공간에 놓인 별도의 값입니다.

작은 값 타입에서는 복사 비용이 거의 문제 되지 않지만, 큰 struct를 자주 전달하는 코드에서는 복사 비용이 누적될 수 있습니다. 이때 `ref`, `out`, `in`을 사용하면 값을 새로 복사하지 않고 원본 저장 위치를 기준으로 전달할 수 있는데, 이를 **참조 전달**이라고 합니다.

다만 참조 전달은 다음 절에서 다룰 **참조 타입**과는 다른 개념입니다. 값 타입을 참조 전달해도 타입 자체가 참조 타입으로 바뀌는 것은 아니며, 호출 방식만 달라집니다.

---

## 참조 타입 (Reference Type)

**참조 타입(Reference Type)**은 값 타입과 다르게 객체 데이터를 변수 안에 직접 저장하지 않습니다. 객체 본체는 힙에 만들고, 변수에는 그 객체가 있는 위치를 가리키는 참조가 저장됩니다.

`class`로 선언한 사용자 정의 타입을 비롯해 `string`, 배열(`int[]`, `GameObject[]` 등), 델리게이트(delegate)는 모두 참조 타입입니다. Unity에서 자주 다루는 `MonoBehaviour`, `GameObject`, `Transform`, `Texture2D`도 class로 정의되어 있으므로 참조 타입에 속합니다.

참조 타입 인스턴스는 보통 `new` 키워드로 만듭니다. `new`를 호출하면 객체의 실제 데이터는 **힙(Heap)**에 할당되고, 변수에는 그 힙 위치를 가리키는 참조가 저장됩니다. 즉 객체 본체와 변수가 서로 다른 메모리 영역에 놓입니다.

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
  <text fill="currentColor" x="368" y="164" text-anchor="start" font-size="12" font-family="monospace">name = "EnemyA"</text>
  <text fill="currentColor" x="463" y="194" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(수십~수백 bytes)</text>
</svg>
</div>

<br>

변수 `enemy` 안에는 힙에 있는 `Enemy` 인스턴스의 주소(`0x00A0B4C0`)가 저장되어 있습니다. `hp`, `attack`, `name` 같은 실제 필드 값은 변수 안이 아니라 힙 객체 안에 들어 있습니다.

따라서 참조 변수의 크기는 객체의 크기와 직접 관련이 없습니다. 변수에는 주소 하나가 들어가므로, 일반적으로 32비트 환경에서는 4바이트, 64비트 환경에서는 8바이트를 차지합니다.

참조 타입을 다른 변수에 대입하면 **객체 본체가 아니라 참조만** 복사됩니다. `Enemy a = b;`라고 쓰면 `b`가 가리키던 힙 주소가 `a`에도 저장되고, 두 변수는 같은 힙 객체를 함께 가리킵니다. 따라서 `a`를 통해 필드를 바꾸면 같은 객체를 가리키는 `b`에도 그 변경이 그대로 반영됩니다.

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

`a = b`처럼 같은 대입문을 쓰더라도, 타입에 따라 복사되는 대상이 다릅니다. 값 타입에서는 `b`의 데이터가 `a`로 복사되어 두 값이 서로 독립됩니다. 반면 참조 타입에서는 객체가 새로 복제되지 않고, `a`와 `b`가 같은 객체를 함께 가리키게 됩니다.

참조 타입 가운데 `string`은 따로 주의해야 합니다. `string`은 참조 타입이지만, 한 번 만들어진 내용을 바꿀 수 없는 **불변(immutable)** 객체입니다. 문자열을 수정하는 것처럼 보이는 코드는 기존 객체를 고치는 것이 아니라 새 문자열 객체를 만들어 참조를 바꾸는 방식으로 동작합니다. 그래서 문자열을 반복해서 이어 붙이면 새 객체 할당이 누적될 수 있습니다.

---

## 스택 메모리

값 타입과 참조 타입의 성능이 달라지는 이유는 두 타입의 데이터가 서로 다른 메모리 영역에 놓이기 때문입니다. 그 영역이 바로 **스택(Stack)**과 **힙(Heap)**이며, 둘은 데이터를 다루는 방식이 근본부터 다릅니다.

먼저 스택은 함수 호출 단위로 관리되는 메모리 영역입니다. 함수가 호출되면 그 함수의 지역 변수, 매개변수, 반환 주소 등을 담을 공간이 스택에 마련됩니다. 이렇게 함수 호출 하나에 대응해 만들어지는 메모리 블록을 **스택 프레임(Stack Frame)**이라고 합니다.

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

스택은 **LIFO(Last-In, First-Out)** 구조로 동작합니다. 나중에 만들어진 스택 프레임이 먼저 제거되는 방식입니다.

가장 최근에 호출된 함수의 프레임은 스택의 최상단에 놓입니다. 그 함수가 끝나면 최상단 프레임이 제거되고, 실행 흐름은 그 아래에 있던 호출자 함수로 돌아갑니다.

예를 들어 함수 A가 B를 호출하고, B가 다시 C를 호출하면 스택에는 A, B, C 순서로 프레임이 쌓입니다. 이후 C가 끝나면 C의 프레임이 먼저 제거되고, B가 끝나면 B의 프레임이 제거됩니다.

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

이 과정은 **스택 포인터(Stack Pointer)**라는 레지스터를 움직이는 방식으로 처리됩니다.

함수가 호출되면 CPU는 스택 포인터를 조정해 필요한 공간을 확보합니다. 함수가 끝나면 스택 포인터를 이전 위치로 되돌려 해당 프레임의 공간을 한 번에 반납합니다.

이 방식은 별도의 탐색이나 복잡한 해제 절차가 필요 없기 때문에 매우 빠릅니다. 스택 할당과 해제는 보통 포인터 값을 조정하는 수준에서 끝납니다.

이때 스택 프레임 안에 있던 데이터도 함께 정리됩니다. 개발자가 따로 해제할 필요가 없고, GC가 나중에 찾아 회수할 대상도 아닙니다. 값 타입 지역 변수가 보통 GC 부담을 만들지 않는 것은 이 때문입니다.

다만 스택 공간은 제한되어 있습니다. 스레드마다 정해진 스택 크기를 넘으면 **StackOverflowException**이 발생합니다. 종료 조건이 잘못된 재귀 호출이나, 매우 큰 struct를 지역 변수로 반복해서 만드는 코드는 이 한계에 닿을 수 있습니다.

---

## 힙 메모리

스택이 함수 호출 단위로 관리되는 영역이라면, **힙(Heap)**은 함수 수명과 별도로 유지되어야 하는 객체가 놓이는 영역입니다.

가장 분명한 힙 할당은 `new Enemy()`처럼 class 인스턴스를 만들거나, `new int[100]`처럼 배열을 만드는 경우입니다. 반면 `new Vector3(1, 2, 3)`처럼 struct를 생성한다고 해서 그 값이 곧바로 힙에 놓이는 것은 아닙니다.

struct는 값 자체가 저장되므로, 어디에 선언되었느냐에 따라 놓이는 위치가 달라집니다. 지역 변수로 만든 `Vector3 position`은 보통 스택 프레임 안에 놓이고, class의 필드로 들어간 `Vector3 position`은 그 class 객체의 일부로 힙에 함께 놓입니다. 배열 요소로 들어간 struct도 배열 객체 안에 포함됩니다.

그 밖에도 박싱이나 문자열 이어 붙이기처럼, 겉으로는 객체를 직접 만드는 코드가 없어 보여도 내부적으로 힙 할당이 생기는 경우가 있습니다.

힙에 놓인 객체는 그 객체를 만든 함수가 끝나도 바로 사라지지 않습니다. 다른 함수나 다른 객체가 계속 참조할 수 있기 때문입니다. 따라서 힙 객체의 수명은 함수의 시작과 끝이 아니라, 그 객체에 도달할 수 있는 참조가 남아 있는지에 따라 결정됩니다.

힙 객체를 회수하는 일은 **가비지 컬렉터(GC)**가 맡습니다. GC는 더 이상 참조되지 않는 객체를 찾아 회수하고, 그 공간을 다시 사용할 수 있게 만듭니다. 개발자가 직접 해제 시점을 관리하지 않아도 된다는 장점이 있지만, GC가 실행되는 동안에는 CPU 시간과 프레임 시간이 소모됩니다.

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

스택 할당은 정해진 순서로 공간을 쌓고 되돌리는 구조라, 포인터 위치를 조정하는 것만으로 처리됩니다. 반면 힙에서는 새 객체를 넣을 수 있는 공간을 찾아야 하고, 그 공간에 객체 본문뿐 아니라 타입 정보와 GC가 추적할 관리 정보도 함께 준비해야 합니다. 또한 힙 객체는 만들어진 순서대로 사라지지 않으므로, 스택처럼 마지막에 쌓은 공간을 바로 되돌리는 방식으로 정리할 수 없습니다.

힙이 필요한 이유는 객체의 수명이 함수 호출 하나로 끝나지 않을 수 있기 때문입니다. 어떤 함수에서 만든 객체라도 다른 객체나 변수에서 계속 참조하고 있다면 힙에 남아 있고, 더 이상 참조되지 않을 때 GC의 회수 대상이 됩니다.

<br>

|  | 스택 | 힙 |
|---|---|---|
| **할당** | 포인터 위치 조정 | 빈 공간 탐색과 객체 초기화 |
| **해제** | 포인터 복원 | GC가 회수 |
| **크기** | ~1MB/스레드 | 시스템 메모리 범위 내 자유 |
| **GC 대상** | 아님 | 맞음 |
| **데이터 수명** | 함수 수명과 동일 | 참조가 살아 있는 동안 |

<br>

값 타입 지역 변수는 함수가 끝날 때 스택 프레임과 함께 사라집니다. 반면 참조 타입 인스턴스는 힙에 남아 있다가 GC가 회수할 때 정리됩니다. 이 수명 관리 방식의 차이가 값 타입과 참조 타입의 성능 차이로 이어집니다.

Unity가 사용하는 Boehm GC는 힙을 세대로 나누지 않는 비세대(non-generational) 방식입니다. 따라서 힙에 객체가 많이 쌓여 있을수록 GC가 검사해야 할 범위가 커지고, GC 한 사이클에 걸리는 시간도 늘어날 수 있습니다.

> 비세대 GC의 동작 원리는 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 자세히 다룹니다.

---

## 박싱과 언박싱

값 타입 값을 `object` 변수에 담거나, 인터페이스 타입 매개변수로 넘기는 코드도 작성할 수 있습니다. 예를 들어 `object value = 10;`처럼 `int` 값을 `object`로 받거나, 어떤 struct를 `IComparable` 같은 인터페이스 타입으로 다루는 경우입니다. 이때 런타임은 값 타입 데이터를 그대로 참조처럼 넘기지 않고, 힙 객체로 감싸는 과정을 거칩니다.

값 타입 값을 참조 타입 객체로 감싸는 변환을 **박싱(Boxing)**이라고 하고, 박싱된 객체에서 다시 값 타입 값을 꺼내는 변환을 **언박싱(Unboxing)**이라고 합니다. 박싱이 일어나면 새 힙 객체가 만들어지고, 그 안에 값 타입 데이터가 복사됩니다.

---

### 박싱 (Boxing)

박싱이 가능한 배경에는 C#의 타입 계층이 있습니다. C#의 모든 타입은 최상위 타입인 `System.Object` 아래에 놓이며, `int`나 `float` 같은 값 타입도 이 계층 안에 포함됩니다. 그래서 `object boxed = score;`처럼 값 타입 값을 `object` 변수에 넣는 코드가 허용됩니다.

인터페이스도 비슷합니다. 어떤 struct가 `IComparable`을 구현했다면, 그 값을 `IComparable comparable = value;`처럼 인터페이스 타입 변수에 담을 수 있습니다. 값 타입 값을 `object`나 인터페이스 타입으로 받는 이런 변환에서 박싱이 발생할 수 있습니다.

하지만 `object` 변수나 일반적인 인터페이스 타입 변수는 객체를 가리키는 참조를 저장하는 형태입니다. 값 타입 값은 변수 안에 데이터 자체로 저장되어 있으므로, 런타임은 그 값을 바로 참조 변수에 넣을 수 없습니다. 대신 힙에 새 객체를 만들고, 그 안에 값 타입 데이터를 복사한 뒤, 변수에는 그 객체를 가리키는 참조를 저장합니다. 이 변환이 박싱입니다.

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
  <text fill="currentColor" x="495" y="310" text-anchor="middle" font-size="11" font-family="sans-serif" opacity="0.7">(객체 헤더 포함)</text>
</svg>
</div>

<br>

예를 들어 `int` 값 자체는 4바이트만 있으면 저장할 수 있습니다. 하지만 박싱되면 그 4바이트 값이 힙 객체 안에 들어가고, 그 객체 안에는 런타임이 객체를 식별하고 관리하기 위한 추가 정보도 함께 저장됩니다. 그래서 박싱된 `int`는 원래의 `int` 값 하나보다 더 많은 메모리를 사용합니다.

박싱은 기존 객체를 재사용하지 않고, 일어날 때마다 새로운 힙 할당을 만듭니다. 매 프레임 실행되는 코드에서 박싱이 자주 발생하면 GC가 회수해야 할 작은 객체가 계속 늘어나고, 어느 순간 프레임이 끊기는 GC 스파이크로 이어질 수 있습니다.

---

### 언박싱 (Unboxing)

박싱된 값은 `object` 같은 참조 타입 변수에 들어 있지만, 다시 `int` 같은 값 타입으로 사용하려면 힙 객체 안의 값을 값 타입 변수로 되돌려야 합니다.

박싱된 값을 다시 값 타입 변수에 넣으려면 대상 타입을 명시하는 캐스팅이 필요합니다. `int unboxed = (int)boxed;`에서 `(int)`는 `boxed`를 `int`로 꺼내겠다는 명시적 캐스팅입니다. 이때 런타임은 `boxed`가 실제로 박싱된 `int`인지 확인한 뒤, 힙 객체 안의 값을 `unboxed` 변수로 복사합니다. 이 과정이 **언박싱(Unboxing)**입니다.

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

언박싱은 새 힙 객체를 만들지 않습니다. 이미 힙에 있는 박싱 객체에서 값을 읽어, 새 값 타입 변수로 복사하는 과정입니다. 대신 런타임은 먼저 박싱 객체 안의 실제 타입이 캐스팅 대상과 맞는지 확인해야 합니다. 예를 들어 박싱된 값이 `int`인데 `float`로 꺼내려 하면 `InvalidCastException`이 발생합니다.

언박싱에도 타입 검사와 값 복사 비용은 있지만, 성능상 더 주의해야 할 부분은 보통 박싱입니다. 힙 할당과 GC 부담은 박싱이 일어나는 순간 만들어지기 때문입니다. 박싱된 객체가 언박싱되지 않고 `object` 상태로만 사용되더라도, 참조가 사라지면 결국 GC가 회수해야 할 힙 객체로 남습니다.

---

### 박싱이 발생하는 흔한 패턴

`object boxed = intValue;`처럼 박싱을 직접 쓰는 코드는 많지 않습니다.

문제가 되는 박싱은 보통 코드에서 잘 드러나지 않는 **암묵적 변환**으로 발생합니다. 값 타입을 `object`나 인터페이스 타입으로 받는 API에 넘기거나, 오래된 컬렉션에 저장하거나, 비교 로직에서 기본 경로를 타는 경우가 대표적입니다.

그중 값 타입을 `object`로 받는 API의 흔한 예가 `string.Format`입니다. `string.Format`은 인자를 `object`로 받기 때문에, `int`나 `float` 같은 값 타입 인자를 넘기면 각 인자가 박싱됩니다.

<br>

```csharp
int hp = 75;
int maxHp = 100;

string text = string.Format("HP: {0}/{1}", hp, maxHp);
// hp가 object로 박싱 (힙 할당 #1)
// maxHp가 object로 박싱 (힙 할당 #2)
// Format 결과 string 생성 (힙 할당 #3)
```

<br>

문자열 보간(`$"HP: {hp}/{maxHp}"`)은 문자열 생성과 박싱 여부를 나누어 보아야 합니다. `hp`와 `maxHp`처럼 실행 중 값이 들어가는 표현식이라면, 보간식은 결과를 담는 새 `string` 객체를 만듭니다.

문제는 그 과정에서 값 타입 인자가 박싱되는지입니다. 이는 컴파일러가 보간식을 어떤 코드로 변환하느냐에 따라 달라집니다. C# 10 이후의 `interpolated string handler`를 지원하는 환경에서는 박싱을 피할 수 있는 경로가 있지만, Unity 프로젝트에서는 사용하는 Unity 버전이 이 방식을 공식 지원하는지 확인해야 합니다. 이 최적화를 전제로 둘 수 없는 환경에서는 문자열 보간이 값 타입 박싱을 만들 수 있으므로, 매 프레임 갱신되는 UI 문자열은 Profiler에서 실제 GC Alloc을 확인해야 합니다.

값 타입이 `object`로 넘어갈 때 박싱된다는 점은 컬렉션에서도 그대로 적용됩니다. `ArrayList`나 `Hashtable` 같은 오래된 비제네릭 컬렉션은 요소를 `object`로 저장하므로, 값 타입을 추가하면 그 값이 먼저 `object`로 박싱됩니다. 반면 `List<int>`처럼 제네릭 컬렉션을 사용하면 요소 타입이 `int`로 유지되므로, 같은 값을 저장해도 박싱이 필요 없습니다.

<br>

```csharp
ArrayList list = new ArrayList();
list.Add(42);       // 42가 object로 박싱 → 힙 할당
list.Add(3.14f);    // 3.14f가 object로 박싱 → 힙 할당

List<int> genericList = new List<int>();
genericList.Add(42);       // int 그대로 저장 → 박싱 없음
genericList.Add(99);       // int 그대로 저장 → 박싱 없음
```

<br>

struct도 인터페이스를 구현할 수 있습니다. 예를 들어 `MyStruct`가 `IComparable<MyStruct>`를 구현했다면, `MyStruct` 값끼리 `CompareTo()`를 사용해 비교할 수 있습니다.

다만 값 타입인 struct를 인터페이스 타입으로 다룰 때는 박싱이 발생할 수 있습니다. `IComparable<MyStruct>` 같은 인터페이스 변수는 `MyStruct` 값 자체를 보관하는 공간이 아니라, `IComparable<MyStruct>`로 사용할 수 있는 객체의 참조를 저장하는 변수입니다. 따라서 `MyStruct` 값을 여기에 대입하면 런타임은 그 값의 복사본을 박싱해 힙에 객체를 만들고, 인터페이스 변수에는 그 박싱된 객체의 참조를 저장합니다.

아래 예시는 `a`를 인터페이스 타입 변수에 담아 `CompareTo()`를 호출합니다. 이때 `a`의 복사본이 박싱되고, `comparable`에는 그 박싱 객체의 참조가 저장됩니다.

<br>

```csharp
struct MyStruct : IComparable<MyStruct>
{
    public int Value;
    public int CompareTo(MyStruct other) => Value.CompareTo(other.Value);
}

MyStruct a = new MyStruct { Value = 10 };
MyStruct b = new MyStruct { Value = 20 };

IComparable<MyStruct> comparable = a;    // a의 복사본이 박싱됨
int result = comparable.CompareTo(b);
```

<br>

struct를 `Dictionary<TKey, TValue>`의 키로 사용할 때도 비교 방식을 신경 써야 합니다. 제네릭 Dictionary는 키를 `TKey` 타입 그대로 저장하므로, `Dictionary<MyStruct, TValue>`에 `MyStruct` 키를 넣는 것 자체가 곧바로 박싱을 만들지는 않습니다.

주의할 지점은 키를 찾는 과정입니다. Dictionary는 먼저 `GetHashCode()`로 후보 위치를 찾고, 같은 위치에 있는 후보 키와 찾는 키가 정말 같은지 `Equals()`로 다시 확인합니다. 조회가 많을수록 이 두 메서드가 반복해서 호출됩니다.

키 타입인 struct가 `IEquatable<MyStruct>`를 구현하면 Dictionary는 `Equals(MyStruct other)`처럼 같은 값 타입끼리 비교할 수 있습니다. 반대로 이 구현이 없으면 `Equals(object obj)` 같은 `object` 기반 비교 경로를 탈 수 있고, 그 과정에서 비교 대상이 박싱되거나 느린 기본 비교가 사용될 수 있습니다.

따라서 struct를 Dictionary 키로 사용할 계획이라면 `IEquatable<T>`를 구현하고, `Equals()`와 `GetHashCode()`를 함께 명확히 정의해야 합니다. 이렇게 하면 키 저장 방식이 바뀌는 것은 아니지만, 키 비교가 더 예측 가능해지고 반복 조회에서 생길 수 있는 불필요한 런타임 비용을 줄일 수 있습니다.

<br>

---

## struct vs class 선택 기준

사용자 정의 타입을 만들 때 핵심은 그 데이터가 값처럼 복사되어도 되는지, 하나의 객체로 공유되어야 하는지입니다.

좌표, 색상, 회전값, 계산 결과처럼 복사본이 따로 존재해도 의미가 유지되는 데이터라면 `struct`가 적합합니다. 반대로 게임 오브젝트, 컴포넌트, 매니저, 서비스 객체처럼 여러 코드가 같은 대상을 참조하고 상태 변화를 공유해야 한다면 `class`가 적합합니다.

이때 데이터 크기와 복사 비용, 힙 할당과 GC 부담, 수명, 상속과 다형성 필요 여부도 함께 보아야 합니다. 값으로 두면 복사 비용이 중요해지고, 객체로 두면 힙 할당과 공유 수명이 중요해지기 때문입니다.

---

### struct가 적합한 경우

`struct`는 데이터를 하나의 독립된 값으로 다뤄야 할 때 선택합니다. 좌표, 색상, 회전값, 충돌 판정 결과처럼 계산 중에 만들어지는 값은 보통 "같은 대상"인지보다 "어떤 값을 담고 있는지"가 더 중요합니다.

예를 들어 `(1, 2, 3)`이라는 위치 값은 어느 변수에서 왔는지와 관계없이 같은 위치를 뜻합니다. 이 값을 다른 변수에 복사한 뒤 복사본만 수정해도, 원래 위치가 함께 바뀌지 않는 편이 자연스럽습니다. 값 타입은 대입과 매개변수 전달에서 값 전체가 복사되므로, 이런 데이터의 독립성을 기본 동작으로 표현할 수 있습니다.

다음으로 볼 것은 복사 비용입니다. `struct`는 참조 하나를 복사하는 것이 아니라 필드 전체를 복사합니다. `Vector3`, `Quaternion`, `Color`처럼 크기가 작은 값은 복사 비용이 낮고, 별도의 힙 객체를 만들지 않아도 됩니다. 그래서 자주 만들어지는 계산용 값에서도 부담이 작습니다. .NET 설계 가이드라인에서 대략 **16바이트 이하**를 작은 `struct`의 기준으로 보는 것도 이 복사 비용을 낮게 유지하기 위한 기준입니다.

다만 이 크기는 절대적인 제한이 아닙니다. Unity의 `Ray`나 `Bounds`는 16바이트보다 크지만 `struct`입니다. 이 타입들은 내부에 여러 값을 담고 있지만, 여전히 하나의 계산 값으로 다뤄집니다. `Ray`는 레이캐스트에 사용할 광선 값을 전달하고, `Bounds`는 영역 계산에 사용할 범위 값을 전달합니다. 복사본이 생겨도 같은 광선이나 같은 영역을 나타내는 값으로 의미가 유지됩니다.

그래서 `struct`를 선택할 때는 크기만 보지 않고, 그 값이 얼마나 자주 복사되는지도 함께 봐야 합니다. 값의 크기가 조금 커도 복사되는 횟수가 제한적이고 힙 할당을 피하는 이점이 크다면 `struct`로 둘 수 있습니다. 반대로 큰 데이터가 여러 시스템 사이를 계속 오가고, 매번 값 전체가 복사된다면 참조만 전달하는 `class` 쪽이 더 나을 수 있습니다.

변경 방식도 중요합니다. 값 타입은 복사본이 쉽게 생기기 때문에, 필드를 직접 바꾸는 가변 `struct`는 어느 복사본을 수정하고 있는지 헷갈리기 쉽습니다. 가능하면 값이 바뀔 때 기존 인스턴스의 일부 필드를 고치기보다, 변경된 값을 담은 새 인스턴스를 만들어 대입하는 구조가 더 명확합니다.

정리하면 `struct`는 작고, 값 자체가 의미를 가지며, 복사되어도 원본과 독립적으로 다뤄져야 하는 데이터에 적합합니다. 매 프레임 위치, 방향, 색상, 충돌 결과 같은 작은 값이 많이 만들어지는 코드에서는 이런 성질이 힙 할당과 GC 부담을 줄이는 데 도움이 됩니다.

---

### class가 적합한 경우

`class`는 데이터를 독립된 값이 아니라, 여러 코드가 함께 바라보는 하나의 인스턴스로 다뤄야 할 때 선택합니다. 게임 오브젝트, 컴포넌트, 매니저, 리소스처럼 같은 대상을 여러 곳에서 참조하고 조작해야 한다면 참조 타입이 필요합니다.

참조 타입은 대입하거나 매개변수로 넘길 때 객체 본체를 복사하지 않습니다. 복사되는 것은 힙에 있는 객체를 가리키는 참조입니다. 따라서 여러 변수가 같은 인스턴스를 가리킬 수 있고, 한쪽에서 바꾼 상태를 다른 쪽에서도 같은 객체의 상태로 볼 수 있습니다.

예를 들어 어떤 `GameObject`를 여러 스크립트가 참조하고 있다고 하겠습니다. 한 스크립트에서 이 오브젝트를 비활성화하면, 다른 스크립트가 가진 참조도 같은 오브젝트를 가리키므로 비활성화된 상태를 보게 됩니다. 이런 경우에는 값이 같다는 사실보다 같은 인스턴스를 공유한다는 사실이 더 중요합니다.

크기가 큰 데이터도 `class`를 검토할 수 있습니다. 값 타입으로 두면 대입이나 매개변수 전달 때마다 필드 전체가 복사되지만, 참조 타입은 객체 크기와 관계없이 참조만 복사합니다. 여러 시스템 사이를 자주 오가는 데이터라면, 객체 본체를 한 곳에 두고 참조만 전달하는 구조가 더 낮은 전달 비용을 가질 수 있습니다.

다만 크기가 크다는 이유만으로 항상 `class`를 선택해야 하는 것은 아닙니다. `class` 인스턴스는 힙에 할당되고, 더 이상 사용되지 않을 때 GC가 회수해야 합니다. 짧은 시간 동안만 쓰고 버리는 계산용 데이터라면, 힙 할당과 GC 부담이 오히려 더 큰 비용이 될 수 있습니다. 따라서 공유 상태가 필요한지, 객체 수명이 얼마나 긴지, 반복 할당이 발생하는지를 함께 봐야 합니다.

상속 기반의 다형성이 필요한 경우에도 `class`를 사용합니다. C#에서 `virtual` 메서드, `abstract` 클래스, 상속 계층을 이용하는 설계는 `class`에서만 가능합니다. `struct`도 인터페이스를 구현할 수는 있지만, 다른 타입을 상속해 계층을 만들 수는 없습니다.

정리하면 `class`는 같은 인스턴스를 여러 곳에서 공유해야 하거나, 상태가 여러 프레임에 걸쳐 유지되어야 하거나, 상속과 다형성이 필요한 데이터에 적합합니다. 반대로 단순히 잠깐 계산하고 버리는 작은 값이라면, `class`로 만들었을 때 생기는 힙 할당과 GC 비용을 먼저 의식해야 합니다.

---

### Unity에서의 예시

Unity의 내장 타입을 보면 앞에서 본 기준이 실제 API에 어떻게 반영되어 있는지 확인할 수 있습니다. 위치, 회전, 색상처럼 계산 중에 자주 오가는 데이터는 대부분 값 타입이고, 씬에 존재하는 오브젝트나 엔진 리소스처럼 여러 코드가 같은 대상을 바라봐야 하는 데이터는 참조 타입입니다.

<br>

| 구분 | Unity 타입 | 다루는 방식 |
|---|---|---|
| 값 타입 | `Vector2`, `Vector3`, `Quaternion`, `Color`, `Color32` | 좌표, 방향, 회전, 색상처럼 계산에 쓰이는 값 |
| 값 타입 | `Ray`, `Bounds`, `RaycastHit` | 광선, 영역, 충돌 결과처럼 질의 과정에서 만들어지는 값 |
| 참조 타입 | `GameObject`, `Transform`, `MonoBehaviour` | 씬 안의 특정 오브젝트와 컴포넌트 |
| 참조 타입 | `Texture2D`, `Material`, `Mesh` | 여러 곳에서 참조될 수 있는 엔진 리소스 |

<br>

`Vector3`는 위치나 방향을 나타내는 값입니다. `Transform.position`을 읽으면 현재 위치를 나타내는 `Vector3` 값이 반환됩니다. 이 값은 `Transform` 자체가 아니라, 그 시점의 위치를 복사한 값입니다.

따라서 반환된 `Vector3`를 지역 변수에 담아 수정해도 원본 `Transform`의 위치가 자동으로 바뀌지는 않습니다. 수정한 위치를 실제 오브젝트에 적용하려면 다시 `Transform.position`에 대입해야 합니다.

<br>

```csharp
Vector3 position = transform.position;
position.y += 1f;
transform.position = position;
```

반대로 `GameObject`는 씬 안의 특정 오브젝트를 가리키는 참조 타입입니다. 여러 스크립트가 같은 `GameObject` 참조를 가지고 있다면, 모두 같은 인스턴스를 바라봅니다. 한쪽에서 `SetActive(false)`를 호출하면 다른 쪽에서도 그 오브젝트가 비활성화된 상태로 보입니다.

<br>

이 차이를 정리하면 다음과 같습니다.

| 기준 | `struct` | `class` |
|---|---|---|
| 의미 | 독립적인 값 | 공유되는 인스턴스 |
| 대입 동작 | 값 전체 복사 | 참조 복사 |
| 상태 공유 | 복사본끼리 독립 | 같은 객체 상태를 공유 |
| 복사 비용 | 값의 크기에 비례 | 참조 크기에 비례 |
| 상속 | 불가 | 가능 |
| 대표 용도 | 좌표, 색상, 계산 결과 | 오브젝트, 컴포넌트, 리소스 |

<br>

여기서 주의할 점은 `struct`가 항상 스택에 놓이는 것은 아니라는 점입니다. 값 타입은 자신을 담고 있는 저장 위치에 포함됩니다. 지역 변수로 선언한 작은 `struct`는 보통 별도의 힙 객체를 만들지 않지만, 클래스 필드나 배열 요소로 들어간 `struct`는 그 객체나 배열 안에 포함됩니다.

또한 `struct` 안에 `string` 같은 참조 타입 필드가 있다면, `struct` 안에는 문자열 객체 자체가 들어가는 것이 아니라 그 객체를 가리키는 참조가 들어갑니다. 실제 문자열 객체는 힙에 따로 존재합니다.

<br>

```csharp
// 지역 변수: 작은 값 타입 값으로 사용
void Update()
{
    Vector3 dir = Vector3.forward;
}

// class 필드: Player 인스턴스 안에 포함됨
class Player : MonoBehaviour
{
    Vector3 spawnPosition;
}

// 배열 요소: Vector3 값들이 배열 객체 안에 연속 저장됨
Vector3[] waypoints = new Vector3[10];
```

<br>

`struct`는 다른 변수에 대입할 때마다 값 전체가 복사됩니다. 복사 한 번의 비용은 작지만, 큰 `struct`가 자주 복사되면 그 비용을 무시하기 어렵습니다. 따라서 큰 `struct`를 다룰 때는 복사가 어디서 생기는지 알아 둘 필요가 있습니다.

첫 번째 복사는 함수에 값을 넘길 때 생깁니다. 함수를 호출하면 인자로 넘긴 `struct` 값이 매개변수로 복사되기 때문입니다. 작은 값이라면 잘 드러나지 않지만, 큰 값이 매 프레임 여러 함수를 거치면 호출하는 횟수만큼 복사 비용이 더해집니다.

매개변수를 `in`으로 받으면 이 복사를 피할 수 있습니다. `in`은 값을 복사하지 않고 원본을 읽기 전용 참조로 넘기므로, 값이 아무리 커도 넘기는 비용은 참조 하나에 그칩니다.

```csharp
void UseByValue(Bounds bounds)
{
    // Bounds 값 전체가 복사됨
}

void UseByIn(in Bounds bounds)
{
    // Bounds 값을 읽기 전용 참조로 받음
}
```

`in`으로 첫 번째 복사를 막아도, 그렇게 받은 값의 메서드가 자기 필드를 바꾼다면 이번에는 두 번째 복사가 생깁니다. 다음 `Counter`의 `Next()`가 그런 메서드입니다.

```csharp
struct Counter
{
    public int Value;

    public int Next()
    {
        Value++;
        return Value;
    }
}

void Print(in Counter counter)
{
    int value = counter.Next();
}
```

`Print()`의 `counter`는 `in`으로 받아 읽기 전용입니다. 그런데 `Next()`는 `Value++`로 자기 필드를 바꾸는 메서드입니다.

원본은 바꿀 수 없으니, 컴파일러는 원본 대신 자유롭게 바꿀 수 있는 임시 복사본을 만들고, 그 복사본에서 `Next()`를 실행합니다.

이때 늘어난 `Value`는 복사본에만 남고, 원본 `counter`는 그대로입니다. 이처럼 읽기 전용 원본을 지키기 위해 컴파일러가 자동으로 끼워 넣는 복사를 **방어적 복사(defensive copy)**라고 합니다.

방어적 복사는 값을 바꾸는 멤버에서만 생기는 것은 아닙니다. 프로퍼티 `bounds.size`를 읽을 때 호출되는 `get`은 값을 읽기만 하는데도, `readonly`가 붙어 있지 않으면 여기서도 복사가 생깁니다. 컴파일러는 멤버가 실제로 무엇을 하는지가 아니라 `readonly` 표시가 있는지만으로 복사 여부를 판단하기 때문입니다. 표시가 없는 멤버는 원본을 바꿀 수 있는 것으로 간주됩니다.

반면 `Counter`의 `Value`처럼 `struct`에 그대로 들어 있는 필드를 읽을 때는 복사가 생기지 않습니다. 필드를 읽는 것은 메서드 호출이 아니라 데이터를 직접 꺼내는 것이라, 원본을 바꿀 일이 없기 때문입니다.

결국 두 번째 복사는 `in` 때문이 아니라, `readonly`가 붙지 않은 멤버를 호출하기 때문에 생깁니다. 이 복사를 막으려면 값이 바뀌지 않는다는 사실을 타입에 표시하면 됩니다. 타입 전체가 불변이라면 `readonly struct`로 선언하고, 그렇지 않다면 값을 바꾸지 않는 멤버에만 `readonly`를 붙입니다. 그러면 컴파일러는 그 멤버가 원본을 바꾸지 않는다고 보고, 복사 없이 곧바로 실행합니다.

다만 두 복사가 항상 문제가 되는 것은 아닙니다. 초기화에서 한두 번 일어나는 복사는 무시해도 되지만, `Update()`처럼 매 프레임 실행되는 코드에서는 작은 복사가 거듭 누적되어 성능에 부담을 줍니다. 이렇게 자주 실행되어 성능을 좌우하는 코드 경로를 **핫 패스(hot path)**라고 하며, 복사를 줄이는 일이 의미가 있는 곳도 결국 이 핫 패스입니다.

따라서 `struct`와 `class`를 선택하거나 `in`, `readonly struct`를 적용하기 전에, 먼저 Profiler로 비용이 실제로 드러나는 자리를 확인하는 것이 좋습니다. 모든 타입을 미리 최적화할 필요는 없습니다. 핫 패스에서 복사나 박싱, 힙 할당이 반복되는 지점부터 점검하면 충분합니다.

---

## 마무리

값 타입과 참조 타입은 데이터를 메모리에 놓는 방식부터 다릅니다. 이 차이가 대입과 매개변수 전달에서 무엇이 복사되는지, 그리고 박싱이 왜 힙 할당과 GC 비용으로 이어지는지를 결정합니다.

- **값 타입**은 데이터 자체를 저장합니다. 대입하거나 매개변수로 넘기면 값 전체가 복사되고, 지역 변수로 사용될 때는 보통 스택 프레임과 함께 정리됩니다.
- **참조 타입**은 객체 본체를 힙에 두고, 변수에는 그 객체를 가리키는 참조를 저장합니다. 대입하면 객체가 복사되는 것이 아니라 참조가 복사되므로, 여러 변수가 같은 객체를 공유할 수 있습니다.
- **스택**은 함수 호출 단위로 관리됩니다. 함수가 끝나면 해당 스택 프레임이 사라지므로, 스택에 놓인 데이터는 별도의 해제나 GC 없이 정리됩니다.
- **힙**은 함수 수명과 분리된 객체를 저장합니다. 힙 객체는 참조가 남아 있는 동안 유지되고, 더 이상 도달할 수 없게 되면 GC가 회수합니다.
- **박싱**은 값 타입을 힙 객체로 감싸는 변환입니다. `object`, 인터페이스, 비제네릭 컬렉션, 일부 문자열 처리처럼 암묵적으로 일어나는 경로를 주의해야 합니다.
- **struct와 class 선택**은 크기만으로 결정하지 않습니다. 작고 독립적인 값에는 struct가 적합하고, 공유 상태·정체성·다형성이 필요한 대상에는 class가 적합합니다.
- **큰 struct와 핫 패스**에서는 복사 비용, 방어적 복사, 박싱 여부를 Profiler로 확인해야 합니다. 모든 코드를 미리 최적화하기보다, 매 프레임 반복되는 경로부터 점검해야 합니다.

결국 타입을 선택하는 일은 데이터를 메모리 어디에 둘지, 그래서 어떤 비용을 치를지를 함께 정하는 결정입니다. 값 타입과 참조 타입의 차이를 알아 두면, 복사와 박싱, GC 비용이 어디서 생기는지를 코드를 보며 가늠할 수 있습니다.

이 구분은 이후 런타임과 GC를 다루는 바탕이 됩니다. 이어지는 [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서는 C# 코드가 IL을 거쳐 기계어로 바뀌는 과정과, Unity에서 Mono와 IL2CPP가 어떻게 다른지 살펴봅니다.

<br>

---

**관련 글**
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)

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
