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

Unity로 게임을 만들며 쓰는 C# 코드는 겉보기에 단순합니다. `int score = 100;`은 변수에 값을 적어 넣고, `new Enemy()`는 객체 하나를 만듭니다. 그런데 이 두 줄이 메모리에서 하는 일은 전혀 다릅니다. 앞 줄은 스택에 4바이트를 직접 저장하지만, 뒤 줄은 힙에 객체를 할당한 뒤 변수에는 그 주소만 담습니다.

이 차이는 가비지 컬렉터(GC)가 개입하는지를 가릅니다. 매 프레임 도는 코드에서 힙 할당이 쌓이면 GC가 그만큼 자주 돌고, 그때마다 프레임이 끊깁니다.

[스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)에서는 IL2CPP와 힙 할당 패턴, 오브젝트 풀링을 다루었고, [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서는 Boehm GC의 동작과 GC 스파이크를 다루었습니다. 두 글을 제대로 따라가려면 값 타입과 참조 타입이 각각 어디에 저장되는지, 힙 할당이 왜 비용이 되는지, 박싱이 무엇인지부터 짚어야 합니다.

이 시리즈는 C# 코드가 실행될 때 메모리에서 일어나는 일, 런타임이 코드를 기계어로 바꾸는 과정, GC가 힙을 관리하는 방법, 스레딩과 비동기가 Unity에서 받는 제약을 처음부터 정리합니다.

그 출발점인 이 글에서는 C# 타입 시스템의 가장 기본 갈래인 **값 타입(Value Type)**과 **참조 타입(Reference Type)**을 다룹니다. 둘 중 무엇을 쓰느냐에 따라 데이터가 메모리 어디에 놓이는지, 대입할 때 무엇이 복사되는지, GC가 관리하는 대상이 되는지가 달라집니다.

---

## 값 타입 (Value Type)

C#의 **값 타입**은 데이터 자체를 변수에 담는 타입입니다. `int`, `float`, `bool`, `double`, `char` 같은 기본 숫자·논리 타입이 여기에 속하고, `struct`로 선언한 사용자 정의 타입도 값 타입입니다. Unity에서 자주 쓰는 `Vector3`, `Quaternion`, `Color`, `Ray`, `Bounds`도 모두 struct, 즉 값 타입입니다.

값 타입 변수 안에는 데이터가 그대로 들어 있습니다. `int score = 100;`이라고 선언하면 `score`라는 메모리 공간에 정수 100이 직접 적히며, 다른 곳을 가리키는 주소가 아니라 값 그 자체가 변수 안에 자리합니다.

<svg viewBox="0 0 460 140" xmlns="http://www.w3.org/2000/svg" aria-label="값 타입 변수의 메모리 배치: int score=100이 스택에 직접 저장되는 구조" style="width:100%;max-width:460px;display:block;margin:0 auto">
  <text x="150" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">값 타입 변수의 메모리 배치</text>
  <text x="150" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="13">int score = 100;</text>
  <!-- score 변수 박스 -->
  <rect x="50" y="58" width="180" height="75" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="68" y="78" fill="#73f38f" font-family="monospace" font-size="13">score</text>
  <!-- 값 내부 박스 -->
  <rect x="70" y="86" width="140" height="34" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="140" y="108" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="15" font-weight="bold">100</text>
  <text x="140" y="130" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">(4 bytes)</text>
  <!-- 어노테이션 -->
  <text x="248" y="108" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="12">← 데이터 자체가 직접 저장됨</text>
</svg>

값 타입을 대입하면 **데이터 전체가 복사**됩니다. `int a = b;`라고 쓰면 b에 든 값이 a의 공간으로 그대로 복사되고, 이후 a를 바꿔도 b는 영향을 받지 않습니다. 두 변수가 서로 독립된 데이터를 따로 갖기 때문입니다.

<svg viewBox="0 0 440 170" xmlns="http://www.w3.org/2000/svg" aria-label="값 타입의 대입: a=10, b=20이 독립적인 복사본으로 존재" style="width:100%;max-width:440px;display:block;margin:0 auto">
  <text x="220" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">값 타입의 대입 (복사)</text>
  <text x="220" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="12">int b = a;  b = 20;  // a와 b는 독립적</text>
  <!-- a 변수 -->
  <text x="120" y="72" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="13">a:</text>
  <rect x="60" y="80" width="120" height="46" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="120" y="110" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="16" font-weight="bold">10</text>
  <text x="120" y="148" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">독립적인 복사본</text>
  <!-- b 변수 -->
  <text x="320" y="72" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="13">b:</text>
  <rect x="260" y="80" width="120" height="46" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="320" y="110" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="16" font-weight="bold">20</text>
  <text x="320" y="148" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">독립적인 복사본</text>
</svg>

struct도 같은 규칙을 따릅니다. `Vector3 a = b;`라고 쓰면 b의 x, y, z 세 값 12바이트가 통째로 a에 복사되므로, a의 x를 바꿔도 b의 x는 그대로입니다.

<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" aria-label="Vector3 struct의 대입: 12바이트 전체 복사로 독립적인 두 변수 생성" style="width:100%;max-width:520px;display:block;margin:0 auto">
  <text x="260" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">Vector3의 대입 (복사)</text>
  <text x="260" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">Vector3 b = a;  b.x = 99;  // 12바이트 전체 복사, b만 변경</text>
  <!-- a 변수 -->
  <text x="130" y="70" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="13">a:</text>
  <rect x="50" y="78" width="160" height="130" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="130" y="104" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">x = 1</text>
  <line x1="65" y1="112" x2="195" y2="112" stroke="#333" stroke-width="1"/>
  <text x="130" y="134" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">y = 2</text>
  <line x1="65" y1="142" x2="195" y2="142" stroke="#333" stroke-width="1"/>
  <text x="130" y="164" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">z = 3</text>
  <line x1="65" y1="172" x2="195" y2="172" stroke="#333" stroke-width="1"/>
  <text x="130" y="196" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">(12 bytes)</text>
  <!-- b 변수 -->
  <text x="390" y="70" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="13">b:</text>
  <rect x="310" y="78" width="160" height="130" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="390" y="104" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">x = 99</text>
  <line x1="325" y1="112" x2="455" y2="112" stroke="#333" stroke-width="1"/>
  <text x="390" y="134" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">y = 2</text>
  <line x1="325" y1="142" x2="455" y2="142" stroke="#333" stroke-width="1"/>
  <text x="390" y="164" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13">z = 3</text>
  <line x1="325" y1="172" x2="455" y2="172" stroke="#333" stroke-width="1"/>
  <text x="390" y="196" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">(12 bytes)</text>
</svg>

이 복사는 메서드 호출에서도 똑같이 일어납니다. 값 타입을 매개변수로 넘기면 원본이 아니라 그 복사본이 전달되므로, 메서드 안에서 매개변수를 고쳐도 호출한 쪽의 원본은 그대로 남습니다.

복사를 건너뛰고 싶을 때는 `ref`, `out`, `in` 키워드로 값 타입도 참조로 넘길 수 있습니다. `ref`는 원본을 직접 읽고 쓰도록 열어 주고, `out`은 메서드가 반드시 값을 채워 내보내도록 강제합니다. `in`은 읽기 전용 참조라 복사를 피하면서도 원본을 건드리지 못하게 막으므로, 큰 struct를 넘길 때 복사 비용을 덜어 줍니다.

---

## 참조 타입 (Reference Type)

C#의 **참조 타입**은 데이터 그 자체가 아니라, 데이터가 놓인 메모리 위치의 **주소(참조)**를 변수에 담는 타입입니다. `class`로 선언한 사용자 정의 타입과 `string`, 배열(`int[]`, `GameObject[]` 등), 델리게이트(delegate)가 여기에 속하고, Unity의 `MonoBehaviour`, `GameObject`, `Transform`, `Texture2D`도 모두 class라 참조 타입입니다.

참조 타입 인스턴스는 `new` 키워드로 만듭니다. `new`를 호출하면 객체의 실제 데이터는 **힙(Heap)**에 할당되고, 변수에는 그 힙 주소만 들어갑니다.

<svg viewBox="0 0 620 220" xmlns="http://www.w3.org/2000/svg" aria-label="참조 타입 변수의 메모리 배치: 스택의 참조가 힙의 실제 데이터를 가리키는 구조" style="width:100%;max-width:620px;display:block;margin:0 auto">
  <defs>
    <marker id="d5-ag" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
  </defs>
  <text x="310" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">참조 타입 변수의 메모리 배치</text>
  <text x="310" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="13">Enemy enemy = new Enemy();</text>
  <!-- 스택/힙 레이블 -->
  <text x="130" y="70" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">스택</text>
  <text x="470" y="70" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">힙</text>
  <!-- 스택 박스 -->
  <rect x="30" y="80" width="200" height="120" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="50" y="102" fill="#73f38f" font-family="monospace" font-size="13">enemy</text>
  <!-- 참조 내부 박스 -->
  <rect x="50" y="110" width="160" height="52" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="130" y="132" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">0x00A0B4C0</text>
  <text x="130" y="150" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">(참조/주소)</text>
  <text x="130" y="192" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">(4 or 8 bytes)</text>
  <!-- 화살표: 스택 → 힙 -->
  <line x1="230" y1="136" x2="345" y2="136" stroke="#73f38f" stroke-width="2" marker-end="url(#d5-ag)"/>
  <!-- 힙 박스 -->
  <rect x="358" y="80" width="230" height="130" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="378" y="102" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">Enemy 인스턴스</text>
  <line x1="373" y1="110" x2="573" y2="110" stroke="#333" stroke-width="1"/>
  <text x="378" y="130" fill="#f9fffb" font-family="monospace" font-size="12">hp = 100</text>
  <text x="378" y="150" fill="#f9fffb" font-family="monospace" font-size="12">attack = 15</text>
  <text x="378" y="170" fill="#f9fffb" font-family="monospace" font-size="12">name = "Goblin"</text>
  <text x="473" y="202" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">(수십~수백 bytes)</text>
</svg>

위 그림에서 변수 `enemy`에 담긴 것은 힙에 놓인 Enemy 인스턴스의 주소(0x00A0B4C0)뿐이고, hp·attack·name 같은 실제 데이터는 힙에 있습니다. 그래서 변수 크기는 객체가 얼마나 크든 주소 크기로 고정되어, 32비트 플랫폼에서는 4바이트, 64비트 플랫폼에서는 8바이트입니다.

참조 타입은 **대입할 때 주소만 복사**됩니다. `Enemy a = b;`라고 쓰면 b가 가리키던 힙 주소가 a로 복사되어, a와 b는 **같은 힙 객체**를 함께 가리킵니다. 그러니 a로 데이터를 고치면 b로 봐도 그 변경이 그대로 보입니다.

<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" aria-label="참조 타입의 대입: 두 변수 a와 b가 같은 힙의 Enemy 객체를 참조" style="width:100%;max-width:600px;display:block;margin:0 auto">
  <defs>
    <marker id="d6-ag" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
  </defs>
  <text x="300" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">참조 타입의 대입 (참조 복사)</text>
  <text x="300" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">Enemy b = a;  b.hp = 50;  // 같은 객체를 공유, a.hp도 50</text>
  <!-- 스택/힙 레이블 -->
  <text x="100" y="70" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">스택</text>
  <text x="440" y="70" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">힙</text>
  <!-- 스택 박스 -->
  <rect x="30" y="80" width="140" height="100" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <!-- a 참조 -->
  <rect x="45" y="90" width="110" height="30" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="100" y="110" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">a (참조)</text>
  <!-- b 참조 -->
  <rect x="45" y="135" width="110" height="30" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="100" y="155" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">b (참조)</text>
  <!-- 힙 박스 -->
  <rect x="330" y="80" width="230" height="100" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="350" y="102" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">Enemy 인스턴스</text>
  <line x1="345" y1="110" x2="545" y2="110" stroke="#333" stroke-width="1"/>
  <text x="350" y="132" fill="#f9fffb" font-family="monospace" font-size="12">hp = 50</text>
  <text x="350" y="152" fill="#f9fffb" font-family="monospace" font-size="12">attack = 15</text>
  <!-- 화살표: a → 힙 -->
  <line x1="155" y1="105" x2="318" y2="105" stroke="#73f38f" stroke-width="2" marker-end="url(#d6-ag)"/>
  <!-- 화살표: b → 힙 (수렴) -->
  <path d="M155 150 L240 150 L240 130 L318 130" fill="none" stroke="#73f38f" stroke-width="2" marker-end="url(#d6-ag)"/>
  <!-- 주석 -->
  <text x="445" y="210" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">a와 b가 같은 객체를 공유</text>
</svg>

정리하면 값 타입의 대입은 데이터를 복사해 서로 독립된 사본을 만들고, 참조 타입의 대입은 같은 데이터를 가리키는 또 하나의 별명을 만듭니다.

`string`은 참조 타입이면서도 **불변(immutable)**이라는 점이 조금 특이합니다. string을 "수정"하면 기존 객체가 바뀌는 게 아니라 새 string 객체가 힙에 새로 만들어지므로, 문자열을 반복해 이어 붙이면 그만큼 힙 할당이 쌓입니다.

---

## 스택 메모리

값 타입과 참조 타입의 성능 차이는 데이터가 놓이는 메모리 영역, 곧 스택과 힙이 서로 다르게 동작한다는 데서 비롯됩니다.

**스택**은 함수 호출에 맞춰 자동으로 관리되는 영역입니다. 함수가 호출되면 그 함수의 지역 변수와 매개변수, 돌아갈 반환 주소를 담을 공간이 스택 위에 쌓이는데, 이렇게 호출 한 번에 대응하는 메모리 블록을 **스택 프레임(Stack Frame)**이라고 합니다.

<svg viewBox="0 0 560 300" xmlns="http://www.w3.org/2000/svg" aria-label="스택 프레임의 구조: Attack 함수 호출 시 매개변수, 반환 주소, 지역 변수가 스택에 쌓이는 구조" style="width:100%;max-width:560px;display:block;margin:0 auto">
  <text x="280" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">스택 프레임의 구조</text>
  <!-- 코드 -->
  <text x="30" y="60" fill="#888" font-family="monospace" font-size="12">void Attack(int damage)</text>
  <text x="30" y="78" fill="#888" font-family="monospace" font-size="12">{</text>
  <text x="30" y="96" fill="#888" font-family="monospace" font-size="12">    float multiplier = 1.5f;</text>
  <text x="30" y="114" fill="#888" font-family="monospace" font-size="12">    int total = ...;</text>
  <text x="30" y="132" fill="#888" font-family="monospace" font-size="12">}</text>
  <!-- 스택 레이블 -->
  <text x="430" y="54" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">스택</text>
  <!-- Attack 스택 프레임 -->
  <rect x="330" y="62" width="200" height="155" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <!-- multiplier -->
  <rect x="345" y="72" width="170" height="28" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1"/>
  <text x="430" y="91" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="11">multiplier (4 bytes)</text>
  <!-- 스택 최상단 어노테이션 -->
  <text x="340" y="56" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="10">↑ 스택 최상단</text>
  <!-- total -->
  <rect x="345" y="106" width="170" height="28" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1"/>
  <text x="430" y="125" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="11">total (4 bytes)</text>
  <!-- damage -->
  <rect x="345" y="140" width="170" height="28" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1"/>
  <text x="430" y="159" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="11">damage (4 bytes)</text>
  <!-- 반환 주소 -->
  <rect x="345" y="174" width="170" height="28" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1"/>
  <text x="430" y="193" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">반환 주소</text>
  <!-- 구분선 -->
  <line x1="330" y1="217" x2="530" y2="217" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3"/>
  <!-- 호출한 함수의 스택 프레임 -->
  <rect x="330" y="225" width="200" height="55" rx="6" fill="#1a1f1e" stroke="#555" stroke-width="1.5"/>
  <text x="430" y="250" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="12">(호출한 함수의</text>
  <text x="430" y="268" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="12">스택 프레임)</text>
</svg>

스택은 이름 그대로 가장 나중에 들어온 것이 가장 먼저 나가는 **LIFO(Last-In, First-Out)** 구조입니다. 가장 최근에 호출된 함수의 프레임이 맨 위에 놓이고, 그 함수가 끝나면 맨 위 프레임부터 떨어져 나갑니다.

함수 A가 B를 부르고 B가 다시 C를 부르면 스택에는 A, B, C 순서로 프레임이 쌓입니다. 끝나는 순서는 그 반대여서, C가 먼저 빠지고 그다음 B가 빠집니다.

<svg viewBox="0 0 720 240" xmlns="http://www.w3.org/2000/svg" aria-label="함수 호출과 스택 변화: A, B, C 함수가 호출되고 종료되며 스택 프레임이 쌓이고 제거되는 5단계 시퀀스" style="width:100%;max-width:720px;display:block;margin:0 auto">
  <text x="360" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">함수 호출과 스택 변화</text>
  <!-- 1: A() 호출 -->
  <text x="72" y="52" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">A() 호출</text>
  <rect x="32" y="172" width="80" height="55" rx="5" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="72" y="204" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="12">A 프레임</text>
  <!-- 2: A → B() 호출 -->
  <text x="216" y="46" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">A → B()</text>
  <text x="216" y="60" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">호출</text>
  <rect x="176" y="120" width="80" height="50" rx="5" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="216" y="150" text-anchor="middle" fill="#00d4ff" font-family="monospace" font-size="12">B 프레임</text>
  <rect x="176" y="172" width="80" height="55" rx="5" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="216" y="204" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="12">A 프레임</text>
  <!-- 3: A → B → C() 호출 -->
  <text x="360" y="46" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">A → B → C()</text>
  <text x="360" y="60" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">호출</text>
  <rect x="320" y="68" width="80" height="50" rx="5" fill="#1a1f1e" stroke="#ff6b6b" stroke-width="2"/>
  <text x="360" y="98" text-anchor="middle" fill="#ff6b6b" font-family="monospace" font-size="12">C 프레임</text>
  <rect x="320" y="120" width="80" height="50" rx="5" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="360" y="150" text-anchor="middle" fill="#00d4ff" font-family="monospace" font-size="12">B 프레임</text>
  <rect x="320" y="172" width="80" height="55" rx="5" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="360" y="204" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="12">A 프레임</text>
  <!-- 4: C 종료 -->
  <text x="504" y="52" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">C 종료</text>
  <rect x="464" y="120" width="80" height="50" rx="5" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="504" y="150" text-anchor="middle" fill="#00d4ff" font-family="monospace" font-size="12">B 프레임</text>
  <rect x="464" y="172" width="80" height="55" rx="5" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="504" y="204" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="12">A 프레임</text>
  <!-- 5: B 종료 -->
  <text x="648" y="52" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="11">B 종료</text>
  <rect x="608" y="172" width="80" height="55" rx="5" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="648" y="204" text-anchor="middle" fill="#73f38f" font-family="monospace" font-size="12">A 프레임</text>
</svg>

이 모든 과정은 **스택 포인터(Stack Pointer)** 레지스터 하나로 관리됩니다. 함수가 호출되면 포인터를 옮겨 공간을 확보하고 함수가 끝나면 도로 옮겨 반납하는데, 할당이든 해제든 CPU 명령어 한두 개, 수 나노초면 끝납니다.

스택에 올라간 데이터는 함수가 끝나는 순간 자동으로 사라지므로, 따로 해제할 일도 GC가 관여할 일도 없습니다. 값 타입 지역 변수가 GC 대상에서 빠지는 이유가 이 자동 해제에 있습니다.

대신 스택은 크기가 빠듯합니다. 스레드 하나당 대략 **1MB** 정도만 주어지고, 이 한도를 넘으면 **StackOverflowException**이 납니다. 재귀 호출이 끝없이 이어지거나 수 KB가 넘는 큰 struct를 지역 변수로 두면 이 한계에 닿을 수 있습니다.

---

## 힙 메모리

스택이 함수 호출에 맞춰 자동으로 관리되는 영역이라면, **힙(Heap)**은 프로그램이 명시적으로든 암묵적으로든 따로 요청한 메모리가 자리 잡는 영역입니다. `new` 키워드로 직접 요청하는 경우가 대표적이고, 박싱이나 문자열 연결처럼 코드 표면에는 드러나지 않는 요청도 있습니다. 참조 타입 인스턴스와 string 객체, 배열이 모두 이 힙에 할당됩니다.

힙에 올라간 메모리는 함수가 끝나도 사라지지 않습니다. 함수 A가 만든 객체를 B에 넘겼다면 B가 끝난 뒤에도 A가 그 객체를 계속 써야 하므로, 힙 데이터의 수명은 함수가 아니라 그것을 가리키는 참조가 정합니다.

그래서 힙의 해제는 **가비지 컬렉터(GC)**가 맡습니다. GC는 힙을 주기적으로 훑어 더 이상 어디서도 참조되지 않는 객체를 골라 그 메모리를 회수합니다. 개발자가 일일이 해제하지 않아도 된다는 점은 편하지만, GC가 도는 동안에는 성능 비용이 따릅니다.

<svg viewBox="0 0 650 270" xmlns="http://www.w3.org/2000/svg" aria-label="힙 메모리의 생명주기: 함수 실행 중 스택이 힙을 참조하다가, 함수 종료 후 참조가 끊기고 GC 수거 대기 상태가 되는 과정" style="width:100%;max-width:650px;display:block;margin:0 auto">
  <defs>
    <marker id="d10-ag" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
  </defs>
  <text x="325" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">힙 메모리 할당과 해제</text>
  <!-- 시점 1: 함수 실행 중 -->
  <text x="160" y="52" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="13">시점 1: 함수 실행 중</text>
  <text x="80" y="78" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="12">스택</text>
  <text x="220" y="78" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="12">힙</text>
  <!-- 스택 박스 (시점 1) -->
  <rect x="40" y="88" width="80" height="40" rx="5" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="80" y="113" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">e</text>
  <!-- 화살표 -->
  <line x1="120" y1="108" x2="168" y2="108" stroke="#73f38f" stroke-width="2" marker-end="url(#d10-ag)"/>
  <!-- 힙 박스 (시점 1) -->
  <rect x="180" y="88" width="80" height="40" rx="5" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="220" y="113" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">Enemy</text>
  <!-- 코드 설명 -->
  <text x="160" y="155" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">Enemy e = new Enemy();</text>
  <!-- 구분선 -->
  <line x1="320" y1="60" x2="320" y2="175" stroke="#555" stroke-width="1" stroke-dasharray="5,3"/>
  <!-- 시점 2: 함수 종료 후 -->
  <text x="490" y="52" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="13">시점 2: 함수 종료 후</text>
  <text x="410" y="78" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="12">스택</text>
  <text x="550" y="78" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="12">힙</text>
  <!-- 스택 박스 (시점 2, 해제됨) -->
  <rect x="370" y="88" width="80" height="40" rx="5" fill="#1a1f1e" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="410" y="113" text-anchor="middle" fill="#555" font-family="'Noto Sans KR',sans-serif" font-size="11">(해제)</text>
  <!-- 힙 박스 (시점 2, GC 대기) -->
  <rect x="510" y="88" width="80" height="40" rx="5" fill="#1a1f1e" stroke="#555" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="550" y="113" text-anchor="middle" fill="#555" font-family="monospace" font-size="12">Enemy</text>
  <!-- GC 수거 대기 어노테이션 -->
  <text x="550" y="148" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">참조 없음</text>
  <text x="550" y="164" text-anchor="middle" fill="#ff6b6b" font-family="'Noto Sans KR',sans-serif" font-size="11">GC 수거 대기</text>
  <!-- 하단 설명 -->
  <rect x="100" y="195" width="450" height="65" rx="6" fill="#1a1f1e" stroke="#333" stroke-width="1"/>
  <text x="325" y="218" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">함수 종료 → 스택의 참조 변수 e는 자동 해제</text>
  <text x="325" y="238" text-anchor="middle" fill="#888" font-family="'Noto Sans KR',sans-serif" font-size="12">힙의 Enemy 인스턴스는 남아 있음 → GC가 나중에 회수</text>
</svg>

힙 할당은 스택 할당보다 비쌉니다. 스택은 포인터만 옮기면 끝나지만, 힙은 요청한 크기에 맞는 빈 공간을 찾고, 객체 헤더(타입 정보·동기화 블록 등)를 초기화하고, 메모리 관리용 메타데이터까지 갱신해야 하기 때문입니다. 그래서 스택 할당이 수 나노초로 끝나는 데 비해 힙 할당은 수십~수백 나노초가 걸립니다.

크기 제한은 스택보다 헐겁습니다. 힙은 시스템 메모리가 허용하는 만큼 늘어나지만, 그만큼 커지면 GC가 훑어야 할 범위도 함께 넓어집니다.

|  | 스택 | 힙 |
|---|---|---|
| **할당** | 포인터 이동 (수 ns) | 빈 공간 탐색 (수십~수백 ns) |
| **해제** | 포인터 복원 (수 ns) | GC가 수거 (GC 실행 시 비용) |
| **크기** | ~1MB/스레드 | 시스템 메모리 범위 내 자유 |
| **GC 대상** | 아님 | 맞음 |
| **데이터 수명** | 함수 수명과 동일 | 참조가 살아 있는 동안 |

값 타입 지역 변수는 함수가 끝나면 스택에서 즉시 사라지지만, 참조 타입 인스턴스는 힙에 남아 GC가 회수할 때까지 유지됩니다. 이 수명 차이가 두 타입의 성능 차이로 이어집니다.

Unity의 GC(Boehm GC)는 힙을 세대로 나누지 않는 비세대(non-generational) 방식이라, GC가 실행될 때마다 힙 전체를 검사합니다. 힙에 객체가 많을수록 검사 범위가 넓어지고 GC 실행 시간이 길어집니다. 비세대 GC의 동작 원리는 [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)에서 다룹니다.

---

## 박싱과 언박싱

값 타입 데이터도 뜻하지 않게 힙에 할당될 때가 있습니다. 값 타입과 참조 타입 사이를 오가는 변환인 **박싱(Boxing)**과 **언박싱(Unboxing)** 때문인데, 박싱이 일어나면 스택에 있던 값이 힙으로 복사됩니다.

---

### 박싱 (Boxing)

C#에서는 `int`, `float` 같은 값 타입까지 포함해 모든 타입이 최상위 타입 `object`를 상속합니다. 이 상속 관계 덕분에 `object obj = score;`처럼 값 타입을 `object`나 인터페이스 타입 변수에 대입할 수 있는데, 이 대입이 일어나는 순간 런타임이 **박싱**을 수행합니다.

<svg viewBox="0 0 660 370" xmlns="http://www.w3.org/2000/svg" aria-label="박싱 과정: 값 타입이 힙에 새 객체로 할당되고, 스택의 참조가 힙 객체를 가리키는 3단계 과정" style="width:100%;max-width:660px;display:block;margin:0 auto">
  <defs>
    <marker id="d12-ay" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#e9c062"/></marker>
    <marker id="d12-ag" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#73f38f"/></marker>
  </defs>
  <text x="330" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">박싱 과정</text>
  <text x="330" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="12">object boxed = score;  // 박싱 발생</text>
  <!-- 3단계 설명 -->
  <rect x="30" y="62" width="600" height="100" rx="6" fill="#1a1f1e" stroke="#333" stroke-width="1"/>
  <text x="50" y="86" fill="#e9c062" font-family="'Noto Sans KR',sans-serif" font-size="12" font-weight="bold">1단계</text>
  <text x="110" y="86" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">힙에 새 객체를 할당 (오브젝트 헤더 + 타입 정보 + 데이터 공간)</text>
  <text x="50" y="112" fill="#e9c062" font-family="'Noto Sans KR',sans-serif" font-size="12" font-weight="bold">2단계</text>
  <text x="110" y="112" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">스택의 score 값(100)을 힙 객체의 데이터 공간에 복사</text>
  <text x="50" y="138" fill="#e9c062" font-family="'Noto Sans KR',sans-serif" font-size="12" font-weight="bold">3단계</text>
  <text x="110" y="138" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">스택의 boxed 변수에 힙 객체의 주소를 저장</text>
  <!-- 스택/힙 레이블 -->
  <text x="130" y="190" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">스택</text>
  <text x="480" y="190" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">힙</text>
  <!-- 스택 박스 -->
  <rect x="30" y="200" width="200" height="130" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <!-- score 변수 -->
  <rect x="45" y="210" width="170" height="40" rx="4" fill="#1a2a1e" stroke="#73f38f" stroke-width="1.5"/>
  <text x="130" y="228" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">score = 100</text>
  <text x="130" y="244" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">(4 bytes, 스택)</text>
  <!-- boxed 참조 -->
  <rect x="45" y="262" width="170" height="30" rx="4" fill="#1a2a1e" stroke="#e9c062" stroke-width="1.5"/>
  <text x="130" y="282" text-anchor="middle" fill="#e9c062" font-family="monospace" font-size="12">boxed (참조)</text>
  <text x="130" y="326" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">값 복사 + 힙 할당 발생</text>
  <!-- 화살표: boxed → 힙 -->
  <line x1="230" y1="277" x2="358" y2="277" stroke="#e9c062" stroke-width="2" marker-end="url(#d12-ay)"/>
  <!-- 힙 박스 -->
  <rect x="370" y="200" width="250" height="130" rx="6" fill="#1a1f1e" stroke="#e9c062" stroke-width="2"/>
  <text x="495" y="224" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">[오브젝트 헤더]</text>
  <line x1="385" y1="232" x2="605" y2="232" stroke="#333" stroke-width="1"/>
  <text x="495" y="252" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">[타입 정보: Int32]</text>
  <line x1="385" y1="260" x2="605" y2="260" stroke="#333" stroke-width="1"/>
  <text x="495" y="280" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13" font-weight="bold">값: 100</text>
  <line x1="385" y1="290" x2="605" y2="290" stroke="#333" stroke-width="1"/>
  <text x="495" y="310" text-anchor="middle" fill="#e9c062" font-family="'Noto Sans KR',sans-serif" font-size="11">(총 약 12~24 bytes)</text>
</svg>

4바이트짜리 int 하나를 박싱하면 플랫폼에 따라 힙에 12~24바이트짜리 객체가 만들어집니다. 32비트 플랫폼에서는 오브젝트 헤더 8바이트(동기화 블록 인덱스 4바이트 + 타입 포인터 4바이트)에 데이터 4바이트가 더해져 12바이트가 되고, 64비트 플랫폼에서는 헤더가 16바이트로 커지고 정렬 패딩이 붙어 24바이트가 됩니다.

Unity가 주로 겨냥하는 64비트 모바일(ARM64)이라면 24바이트로, 원래 스택에 있던 4바이트의 여섯 배를 차지합니다.

게다가 박싱은 그때마다 힙에 새 객체를 만들고, 그 객체는 GC가 관리해야 할 대상이 됩니다. 한 번이라면 대수롭지 않지만, 매 프레임 반복되면 힙 할당이 쌓여 GC 스파이크를 부릅니다.

---

### 언박싱 (Unboxing)

**언박싱**은 박싱된 힙 객체에서 원래 값 타입 데이터를 꺼내 다시 스택으로 복사하는 과정입니다.

<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" aria-label="언박싱 과정: 힙 객체의 타입을 확인한 뒤 데이터를 스택으로 복사하는 2단계 과정" style="width:100%;max-width:620px;display:block;margin:0 auto">
  <defs>
    <marker id="d13-ac" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto"><polygon points="0 0,10 3.5,0 7" fill="#00d4ff"/></marker>
  </defs>
  <text x="310" y="22" text-anchor="middle" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="15" font-weight="bold">언박싱 과정</text>
  <text x="310" y="46" text-anchor="middle" fill="#888" font-family="monospace" font-size="12">int unboxed = (int)boxed;  // 언박싱</text>
  <!-- 2단계 설명 -->
  <rect x="30" y="62" width="560" height="70" rx="6" fill="#1a1f1e" stroke="#333" stroke-width="1"/>
  <text x="50" y="86" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="12" font-weight="bold">1단계</text>
  <text x="110" y="86" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">boxed가 가리키는 힙 객체의 타입이 int인지 확인</text>
  <text x="50" y="112" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="12" font-weight="bold">2단계</text>
  <text x="110" y="112" fill="#f9fffb" font-family="'Noto Sans KR',sans-serif" font-size="12">힙 객체의 데이터를 스택의 unboxed 변수에 복사</text>
  <!-- 힙/스택 레이블 -->
  <text x="150" y="160" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="13">힙</text>
  <text x="480" y="160" text-anchor="middle" fill="#73f38f" font-family="'Noto Sans KR',sans-serif" font-size="13">스택</text>
  <!-- 힙 박스 -->
  <rect x="40" y="170" width="220" height="100" rx="6" fill="#1a1f1e" stroke="#00d4ff" stroke-width="2"/>
  <text x="150" y="194" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">[오브젝트 헤더]</text>
  <line x1="55" y1="202" x2="245" y2="202" stroke="#333" stroke-width="1"/>
  <text x="150" y="222" text-anchor="middle" fill="#888" font-family="monospace" font-size="11">[타입 정보: Int32]</text>
  <line x1="55" y1="230" x2="245" y2="230" stroke="#333" stroke-width="1"/>
  <text x="150" y="254" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="13" font-weight="bold">값: 100</text>
  <!-- 화살표: 힙 → 스택 (복사) -->
  <line x1="260" y1="220" x2="368" y2="220" stroke="#00d4ff" stroke-width="2" marker-end="url(#d13-ac)"/>
  <text x="314" y="212" text-anchor="middle" fill="#00d4ff" font-family="'Noto Sans KR',sans-serif" font-size="11">복사</text>
  <!-- 스택 박스 -->
  <rect x="380" y="200" width="200" height="40" rx="6" fill="#1a1f1e" stroke="#73f38f" stroke-width="2"/>
  <text x="480" y="218" text-anchor="middle" fill="#f9fffb" font-family="monospace" font-size="12">unboxed = 100</text>
  <text x="480" y="256" text-anchor="middle" fill="#888" font-family="monospace" font-size="10">(4 bytes, 스택)</text>
</svg>

언박싱 자체는 힙 할당을 일으키지 않습니다. 힙에 있던 데이터를 스택으로 옮겨 적기만 하기 때문입니다. 다만 타입이 맞는지 확인하고 데이터를 복사하는 비용은 들고, 타입이 어긋나면 `InvalidCastException`이 납니다.

박싱했다고 해서 반드시 언박싱이 뒤따르는 것도 아닙니다. `object`인 채로만 쓰이다 참조가 사라지면 GC가 그대로 수거합니다. 그래서 성능 부담의 무게는 박싱 쪽에 실립니다. 언박싱을 하든 안 하든, 박싱하는 순간 이미 힙 할당과 GC 부담이 생기기 때문입니다.

---

### 박싱이 발생하는 흔한 패턴

`object boxed = intValue;`처럼 박싱을 코드에 대놓고 쓰는 경우는 드뭅니다. 정작 까다로운 쪽은 박싱이 **암묵적으로** 끼어드는 패턴입니다.

**string.Format과 문자열 보간.** `string.Format`은 매개변수 타입이 `object`라서, 값 타입 인자를 넘기면 그 자리에서 박싱됩니다. 문자열 보간(`$"HP: {hp}/{maxHp}"`)도 Unity의 C# 컴파일러(Roslyn)가 내부적으로 `string.Format` 호출로 바꾸기 때문에 같은 박싱이 일어납니다.

.NET 6 이상에서는 `DefaultInterpolatedStringHandler`가 도입되면서, 컴파일러가 제네릭 `AppendFormatted<T>` 코드로 변환해 이 박싱을 없앴습니다. 다만 Unity 런타임은 이 핸들러를 지원하지 않으므로, Unity에서는 문자열 보간이 여전히 박싱을 부릅니다.

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

**비제네릭 컬렉션.** `ArrayList`나 `Hashtable` 같은 비제네릭 컬렉션은 요소를 `object`로 담기 때문에, 값 타입을 넣을 때마다 박싱이 일어납니다.

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

**인터페이스로의 변환.** 값 타입이 인터페이스를 구현하더라도, 그 값을 인터페이스 타입 변수에 대입하는 순간 박싱이 일어납니다.

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

**Dictionary의 키로 struct를 사용할 때.** `Dictionary<TKey, TValue>`는 키를 비교하려고 `GetHashCode()`와 `Equals()`를 부릅니다. 이때 struct가 `IEquatable<T>`를 구현하지 않으면 매개변수 타입이 `object`인 기본 `object.Equals(object)` 오버로드가 불리고, 그 호출마다 struct 값이 박싱됩니다.

`GetHashCode()`도 오버라이드하지 않으면 기본 `ValueType.GetHashCode()`가 쓰입니다. 이 기본 구현은 struct 메모리를 바이트 단위로 해싱하려 하는데, struct에 참조 타입 필드가 섞여 있거나 필드 사이에 패딩(정렬용 빈 바이트)이 끼면 바이트 단위 해싱이 어긋납니다. 그러면 리플렉션으로 필드를 하나씩 읽어 처리하느라 성능이 크게 떨어집니다.

그래서 struct를 Dictionary 키로 쓸 때는 `IEquatable<T>`를 구현하고 `GetHashCode()`를 오버라이드해 박싱과 리플렉션 비용을 함께 막아야 합니다.

| 패턴 | 대안 |
|---|---|
| `string.Format("{0}", intValue)` | `StringBuilder.Append(int)` 또는 `int.ToString()` 직접 사용 |
| `ArrayList` / `Hashtable`에 값 타입 추가 | `List<T>` / `Dictionary<K,V>` (제네릭 컬렉션) |
| 값 타입을 인터페이스 변수에 대입 | 제네릭 메서드로 대체 (`where T : IComparable<T>`) |
| struct를 Dictionary 키로 사용 (`IEquatable<T>` 미구현 시) | `IEquatable<T>` 구현 + `GetHashCode()` 오버라이드 |

---

## struct vs class 선택 기준

사용자 정의 타입을 `struct`(값 타입)로 선언할지 `class`(참조 타입)로 선언할지에 따라 메모리 배치, 대입 동작, GC 관여 여부가 달라집니다.

---

### struct가 적합한 경우

struct는 크기가 작고, 불변이며, 수명이 짧은 데이터에 적합합니다.

**크기가 작은 경우.** 대체로 **16바이트 이하**면 struct가 알맞습니다. struct는 대입할 때 데이터 전체가 복사되어 크기가 커질수록 복사 비용이 불어나는데, Microsoft의 .NET 설계 가이드라인(Choosing Between Class and Struct)이 16바이트를 기준으로 드는 까닭은 x64에서 레지스터 두 번의 이동으로 복사되는 크기이기 때문입니다. 이 안쪽이면 참조를 복사하며 힙 할당과 GC 비용을 떠안는 것보다 전체 비용이 더 쌉니다.

이 선을 넘으면 복사 비용이 늘지만, 기준이 절대적이지는 않습니다. Unity의 `Ray`(24B)와 `Bounds`(24B)는 16바이트를 넘고도 struct인데, 복사 비용이 조금 늘더라도 힙 할당과 GC를 피하는 편이 전체 성능에 더 낫기 때문입니다.

```csharp
// struct 크기와 복사 비용:

Vector3 (12 bytes): x, y, z  // → 복사 비용 낮음
Color32 (4 bytes):  r, g, b, a  // → 복사 비용 낮음

struct LargeData (128 bytes) // : 여러 필드  → 복사 비용 높음
                             //             → class가 적합할 수 있음
```

**불변(immutable)인 경우.** 만든 뒤 필드를 더 건드리지 않는 데이터라면 struct가 잘 맞습니다. struct는 대입할 때 값 전체가 복사되므로, 가변(mutable) struct는 복사본을 고쳐도 원본이 그대로 남습니다. class처럼 원본까지 같이 바뀌리라 기대하면 버그로 이어지기 쉬우니, struct는 처음부터 불변으로 설계하는 편이 안전합니다.

**수명이 짧은 경우.** 함수 안에서 잠깐 만들어 쓰고 함수가 끝나면 버려질 데이터는, 스택에 올라가는 struct가 유리합니다. 힙 할당도 GC 관여도 없어서 매 프레임 새로 만들어도 GC를 압박하지 않습니다.

---

### class가 적합한 경우

class는 크기가 크거나, 참조 공유가 필요하거나, 다형성 또는 긴 수명이 요구되는 데이터에 적합합니다.

**크기가 큰 경우.** 필드가 많아 수십~수백 바이트에 이르는 데이터는 class로 선언합니다. class는 대입할 때 주소만 복사하므로, 객체가 아무리 커도 복사 비용은 4~8바이트로 일정합니다.

**참조를 공유해야 하는 경우.** 여러 곳에서 같은 데이터를 가리키고 한쪽의 수정이 다른 쪽에도 그대로 보여야 한다면 class가 맞습니다. 게임의 상태 관리나 매니저 패턴에서 흔히 이런 공유가 필요합니다.

**다형성(Polymorphism)이 필요한 경우.** 다형성은 같은 메서드를 불러도 객체의 실제 타입에 따라 다르게 동작하는 성질로, 상속을 바탕으로 구현됩니다. struct는 상속을 받지 못하므로 `virtual` 메서드나 `abstract` 클래스 같은 다형성 패턴은 class로 풀어야 합니다.

**수명이 긴 경우.** 씬 내내 살아 있거나 여러 프레임에 걸쳐 상태를 이어 가는 오브젝트는, 힙에 머무는 class가 알맞습니다.

---

### Unity에서의 예시

Unity 내장 타입의 struct/class 분류가 이 기준을 잘 보여줍니다.

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

`Vector3`은 12바이트짜리 작은 데이터라 위치나 방향을 담는 임시 값으로 자주 쓰입니다. `Transform.position`이 돌려준 Vector3를 수정해도 원본 Transform의 위치는 그대로여야 하므로, 대입할 때 독립된 복사본이 생기는 struct가 알맞습니다.

`GameObject`는 여러 컴포넌트를 담는 컨테이너라 크기가 크고 상속 구조를 씁니다. 한 스크립트에서 `GameObject.SetActive(false)`를 부르면 같은 오브젝트를 가리키는 모든 곳에서 비활성화가 보여야 하므로, 참조를 공유하는 class가 알맞습니다.

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

다만 값 타입이 필드로 참조 타입을 품으면(예: struct 안의 string 필드) struct 본체는 스택에 있어도 그 string은 힙에 할당됩니다. struct를 썼다고 해서 안의 모든 데이터가 스택에 놓이는 것은 아니므로, GC 비용 이점을 온전히 누리려면 struct 안에 참조 타입 필드를 두지 않는 편이 좋습니다.

struct가 어디에 할당되는지도 따져 봐야 합니다. struct가 스택에 올라가는 것은 **지역 변수**로 선언했을 때뿐입니다. class의 필드로 선언한 struct는 그 class 인스턴스와 함께 **힙**에 놓이고, 배열 요소인 struct도 배열 자체가 힙에 있으니 힙에 자리합니다.

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

`in` 매개변수는 큰 struct를 참조로 넘겨 복사 비용을 줄이되 원본은 고치지 않겠다는 약속입니다. 그런데 일반 struct의 메서드는 내부에서 필드를 바꿀 수도 있고, 컴파일러는 그 메서드가 실제로 필드를 건드리는지 미리 알지 못합니다.

그래서 `in` 매개변수나 `readonly` 변수에서 struct 메서드를 부르면, 컴파일러는 원본을 지키려고 매번 복사본을 떠서 그 복사본 위에서 메서드를 돌립니다. 이것이 **방어적 복사(defensive copy)**입니다. 코드에는 드러나지 않아 알아채기 어려운 데다, 큰 struct에서 메서드를 자주 부르면 `in`으로 줄이려던 복사가 오히려 늘어납니다.

`readonly struct`로 선언하면 모든 필드가 바뀌지 않음이 보장되어 컴파일러가 방어적 복사를 건너뜁니다. 그러니 `in` 매개변수와 함께 쓸 struct는 `readonly struct`로 선언해 두는 편이 좋습니다.

박싱 한 번이 차지하는 힙 할당 비용은 크지 않습니다. 문제는 `Update()`처럼 매 프레임 도는 코드, 곧 **핫 패스(hot path)**에서 박싱이 되풀이될 때입니다. 프레임마다 힙 할당이 쌓이면 GC가 자주 끼어들고, 그 GC 스파이크가 프레임 드롭으로 이어집니다. 반대로 초기화 코드나 이벤트 핸들러처럼 어쩌다 한 번 도는 경로라면 박싱이 한두 번 일어나도 쌓이지 않아 성능에 영향을 주지 않습니다.

그래서 이 글에서 다룬 struct/class 선택과 박싱 회피는 핫 패스에 집중해 적용하고, 무엇을 손볼지는 Unity Profiler로 실제 병목을 확인한 뒤 정하는 편이 안전합니다. 측정 없이 모든 코드를 최적화하려 들면 코드 복잡도만 키우기 쉽습니다.  

---

## 마무리

- 값 타입(int, float, struct 등)은 데이터를 직접 저장하고, 대입 시 전체가 복사됩니다. 지역 변수일 때 스택에 할당되어 GC 관여 없이 함수 종료 시 자동 해제됩니다.
- 참조 타입(class, string, array 등)은 힙에 객체를 할당하고, 변수에는 주소만 저장됩니다. 대입 시 주소만 복사되어 같은 객체를 공유합니다.
- 스택은 포인터 이동만으로 할당/해제되어 비용이 극히 낮고, 힙은 빈 공간 탐색과 GC 회수가 필요하여 비용이 높습니다.
- 박싱은 값 타입을 object나 인터페이스로 변환할 때 힙에 새 객체를 할당합니다. string.Format, 문자열 보간, 비제네릭 컬렉션, 인터페이스 변환 등에서 암묵적으로 발생합니다.
- struct는 16바이트 이하의 불변 데이터에 적합하고, class는 참조 공유나 다형성이 필요한 데이터에 적합합니다. struct가 스택에 할당되는 것은 지역 변수일 때이며, class의 필드나 배열 요소로 존재하면 힙에 위치합니다.
- `in` 매개변수와 함께 사용하는 struct는 `readonly struct`로 선언하여 방어적 복사를 방지합니다.
- 이 글에서 다룬 원칙은 매 프레임 실행되는 핫 패스에서 의미가 있으며, 최적화는 Unity Profiler로 실제 병목을 확인한 뒤 적용합니다.

값 타입과 참조 타입의 메모리 동작은 [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)의 GC 할당 최소화 전략과 [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)의 GC 원리를 이해하는 기초가 됩니다.

[C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서 C# 코드가 IL을 거쳐 기계어로 변환되는 과정과 Mono, IL2CPP의 차이를 다룹니다.

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
