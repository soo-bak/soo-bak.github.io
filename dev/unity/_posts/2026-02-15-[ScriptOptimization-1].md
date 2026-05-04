---
layout: single
title: "스크립트 최적화 (1) - C# 실행과 메모리 할당 - soo:bak"
date: "2026-02-15 21:11:00 +0900"
description: IL2CPP와 Mono, 값 타입과 참조 타입, 숨은 힙 할당, 오브젝트 풀링의 원리를 설명합니다.
tags:
  - Unity
  - 최적화
  - C#
  - 메모리
  - 모바일
---

## C# 코드가 실행되기까지

[게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)에서 GPU 작업이 최적화되어 있어도 CPU가 병목이면 프레임이 떨어진다는 점을 확인했습니다. CPU-bound 상태에서는 해상도를 줄이거나 셰이더를 단순화해도 프레임 시간이 개선되지 않으며, CPU 비용 자체를 직접 줄여야 합니다.

**C# 스크립트 실행**은 CPU가 프레임마다 수행하는 작업 중 개발자가 코드로 직접 제어하는 영역입니다. Update, FixedUpdate, LateUpdate에서 호출되는 게임 로직, AI 판단, 입력 처리 등이 모두 이 영역에 포함됩니다. CPU 비용은 크게 **코드 실행 자체의 비용**과 **메모리 할당·가비지 컬렉션(GC, 사용이 끝난 메모리를 회수하는 과정)의 비용**으로 나뉩니다.

C# 코드가 기계어로 변환되는 방식에 따라 코드 실행 비용이 달라지고, 힙 할당이 쌓여 GC가 동작하면 메모리 비용이 추가됩니다.

이 글에서는 Unity의 **스크립팅 백엔드(Scripting Backend)** — C# 코드를 기계어로 변환하는 방식을 결정하는 엔진 설정 — 인 Mono와 IL2CPP를 살펴보고, 힙 할당이 발생하는 지점과 할당을 줄이는 방법을 다룹니다.

---

## Mono와 IL2CPP

C#은 소스 코드가 곧바로 기계어로 컴파일되지 않습니다.

### C#에서 기계어까지

C# 컴파일러는 소스 코드를 먼저 **IL(Intermediate Language, 중간 언어)**로 변환합니다.
IL은 소스 코드와 기계어 사이의 바이트코드로 CPU가 직접 실행할 수 없어 다시 기계어로 변환해야 하는데, Unity는 원래 이 변환을 게임 실행 중에 수행하는 **Mono**를 사용했고, 이후 실행 성능과 플랫폼 호환성을 개선하기 위해 빌드 시점에 미리 변환하는 **IL2CPP**를 개발했습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">

  <!-- (1) C# 소스 코드 박스 -->
  <rect x="155" y="10" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="35" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">C# 소스 코드</text>

  <!-- 화살표 (1)→(2) -->
  <line x1="240" y1="50" x2="240" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="234,84 240,94 246,84" fill="currentColor"/>
  <text x="310" y="75" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">C# 컴파일러 (Roslyn)</text>

  <!-- (2) IL (중간 언어) 박스 -->
  <rect x="155" y="95" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="120" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">IL (중간 언어)</text>

  <!-- 분기 왼쪽 화살표 (2)→(3L) -->
  <line x1="200" y1="135" x2="120" y2="178" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="114,173 118,184 126,175" fill="currentColor"/>

  <!-- 분기 오른쪽 화살표 (2)→(3R) -->
  <line x1="280" y1="135" x2="360" y2="178" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="354,175 362,184 366,173" fill="currentColor"/>

  <!-- (3L) Mono (JIT) 박스 -->
  <rect x="30" y="185" width="180" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="210" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Mono (JIT)</text>

  <!-- (3R) IL2CPP (AOT) 박스 -->
  <rect x="270" y="185" width="180" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="210" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">IL2CPP (AOT)</text>

  <!-- 왼쪽 변환 설명 -->
  <line x1="120" y1="225" x2="120" y2="278" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="255" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">실행 시점에</text>
  <text x="120" y="270" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">IL → 기계어</text>

  <!-- 오른쪽 변환 설명 -->
  <line x1="360" y1="225" x2="360" y2="278" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="255" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">빌드 시점에</text>
  <text x="360" y="270" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">IL → C++ → 기계어</text>

  <!-- 왼쪽 화살표 → 기계어 -->
  <line x1="120" y1="278" x2="120" y2="328" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="114,324 120,334 126,324" fill="currentColor"/>

  <!-- 오른쪽 화살표 → 기계어 -->
  <line x1="360" y1="278" x2="360" y2="328" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="354,324 360,334 366,324" fill="currentColor"/>

  <!-- (4L) 기계어 박스 (왼쪽) -->
  <rect x="50" y="335" width="140" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="360" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기계어</text>

  <!-- (4R) 기계어 박스 (오른쪽) -->
  <rect x="290" y="335" width="140" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="360" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기계어</text>

  <!-- 하단 부연: 좌/우 구분 라벨 -->
  <text x="120" y="395" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">실행 시점 생성</text>
  <text x="360" y="395" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">빌드 시점 생성</text>

</svg>
</div>

---

### Mono: JIT 컴파일

Mono는 .NET Framework와 호환되는 오픈소스 런타임으로, Windows 이외의 플랫폼에서도 C# 코드를 실행할 수 있도록 개발되었습니다.
Unity는 초기부터 Mono를 채택하여 다양한 플랫폼에서 C# 스크립트를 실행할 수 있게 했습니다.

Mono는 **JIT(Just-In-Time)** 방식으로 메서드가 처음 호출되는 시점에 해당 IL을 기계어로 변환하고, 변환 결과를 캐시하여 이후 호출에서 재사용합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 120" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- 첫 호출 라벨 -->
  <text x="10" y="35" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">첫 호출</text>

  <!-- IL 읽기 -->
  <rect x="90" y="15" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="38" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">IL 읽기</text>

  <!-- 화살표 1→2 -->
  <line x1="190" y1="33" x2="210" y2="33" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="208,28 217,33 208,38" fill="currentColor"/>

  <!-- 기계어 생성 -->
  <rect x="218" y="15" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="273" y="38" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">기계어 생성</text>

  <!-- 화살표 2→3 -->
  <line x1="328" y1="33" x2="348" y2="33" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="346,28 355,33 346,38" fill="currentColor"/>

  <!-- 캐시에 저장 -->
  <rect x="356" y="15" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="416" y="38" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">캐시에 저장</text>

  <!-- 화살표 3→4 -->
  <line x1="476" y1="33" x2="496" y2="33" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="494,28 503,33 494,38" fill="currentColor"/>

  <!-- 실행 -->
  <rect x="504" y="15" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="544" y="38" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">실행</text>

  <!-- 재호출 라벨 -->
  <text x="10" y="90" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">재호출</text>

  <!-- 캐시에서 로드 -->
  <rect x="356" y="70" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="416" y="93" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">캐시에서 로드</text>

  <!-- 화살표 캐시→실행 -->
  <line x1="476" y1="88" x2="496" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="494,83 503,88 494,93" fill="currentColor"/>

  <!-- 실행 (재호출) -->
  <rect x="504" y="70" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="544" y="93" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">실행</text>

</svg>
</div>

<br>

빌드 시점에는 C# 컴파일러가 IL만 생성하면 되므로 빌드가 빠릅니다.

> IL2CPP가 개발된 이후에도 Unity 에디터는 Mono를 스크립팅 백엔드로 사용합니다. 에디터에서는 코드를 수정하고 바로 Play 모드로 확인하는 반복이 빈번한데, Mono의 빠른 빌드가 이 워크플로에 적합하기 때문입니다.

JIT 변환은 메서드를 호출한 스레드에서 동기적으로 수행되므로, 변환이 끝날 때까지 해당 스레드가 멈춥니다. 게임 시작 직후나 새 씬 로드 직후처럼 아직 호출된 적 없는 메서드가 많은 시점에서는, 첫 호출마다 변환이 발생하여 순간적인 끊김이 생길 수 있습니다.

---

### IL2CPP: AOT 컴파일

**IL2CPP**는 이름 그대로 IL을 C++ 소스 코드로 변환하는 백엔드입니다.
변환된 C++ 코드를 플랫폼의 네이티브 C++ 컴파일러(Clang, MSVC 등)로 컴파일하여 기계어를 생성하며, 이 전체 과정이 빌드 시점에 이루어지는 **AOT(Ahead-Of-Time)** 방식입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 130" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- (1) C# 소스 박스 -->
  <rect x="10" y="15" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="45" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">C# 소스</text>

  <!-- 화살표 (1)→(2) -->
  <line x1="130" y1="40" x2="155" y2="40" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="153,35 162,40 153,45" fill="currentColor"/>

  <!-- (2) IL (DLL) 박스 -->
  <rect x="163" y="15" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="223" y="37" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">IL</text>
  <text x="223" y="53" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(DLL)</text>

  <!-- 화살표 (2)→(3) -->
  <line x1="283" y1="40" x2="308" y2="40" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="306,35 315,40 306,45" fill="currentColor"/>

  <!-- (3) C++ 소스 박스 -->
  <rect x="316" y="15" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="376" y="37" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">C++ 소스</text>
  <text x="376" y="53" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(자동생성)</text>

  <!-- 화살표 (3)→(4) -->
  <line x1="436" y1="40" x2="461" y2="40" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="459,35 468,40 459,45" fill="currentColor"/>

  <!-- (4) 네이티브 바이너리 박스 -->
  <rect x="469" y="15" width="140" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="539" y="37" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">네이티브</text>
  <text x="539" y="53" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">바이너리</text>

  <!-- 하단 도구명 보조 텍스트 -->
  <text x="70" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">개발자 작성</text>
  <text x="223" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">C# 컴파일러</text>
  <text x="223" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(Roslyn)</text>
  <text x="376" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">IL2CPP 변환</text>
  <text x="539" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">C++ 컴파일러</text>
  <text x="539" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(Clang 등)</text>

</svg>
</div>

<br>

IL2CPP로 빌드한 앱은 실행 시점에 이미 기계어가 완성되어 있어 런타임 변환 비용이 없습니다.

IL을 C++로 변환한 뒤 플랫폼의 네이티브 C++ 컴파일러로 빌드하므로 인라이닝, 루프 벡터화, 데드 코드 제거 등의 최적화도 적용됩니다. Mono JIT는 실행 중에 빠르게 기계어를 생성해야 하므로 이런 수준의 최적화를 적용하기 어려워, IL2CPP가 실행 속도에서 유리합니다.

또한 런타임에 새 코드를 생성하지 않으므로, Apple의 보안 정책이 런타임 코드 생성을 금지하는 iOS에서도 사용할 수 있습니다. iOS에서는 IL2CPP가 유일한 선택지이며, Android에서도 기본 백엔드로 권장됩니다.

뿐만 아니라 Unity는 빌드 과정에서 실제로 사용되지 않는 코드를 식별하여 제거하는 **코드 스트리핑(Code Stripping)**을 지원하는데, IL2CPP에서는 모든 코드가 네이티브 바이너리로 컴파일되므로 제거 대상이 많아져 Mono보다 빌드 크기를 더 줄일 수 있습니다.

다만 IL → C++ 변환과 C++ 컴파일 단계가 추가되는 만큼 **빌드 시간은 길어지며**, 대규모 프로젝트에서는 수십 분에 이를 수도 있습니다.

이러한 이유로 개발 중에는 Mono의 빠른 빌드로 테스트하고, 기기 테스트와 출시 빌드에서 IL2CPP를 사용하는 것이 일반적인 워크플로입니다.

---

## 값 타입과 참조 타입

코드 실행 비용 외에 프레임 예산을 소비하는 또 다른 요인이 메모리 할당과 GC입니다.
C#에서는 타입에 따라 데이터가 스택 또는 힙에 저장되며, 이 중 힙에 저장된 데이터만 GC의 관리 대상이 됩니다.

### 스택과 힙

프로세스 메모리에는 코드, 정적 데이터, 힙, 스택 등 여러 영역이 있지만, 실행 중 데이터 할당이 일어나는 곳은 **스택(Stack)**과 **힙(Heap)**입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">

  <!-- 제목 -->
  <text x="210" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프로세스 메모리 레이아웃</text>

  <!-- 높은 주소 라벨 -->
  <text x="210" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">높은 주소</text>

  <!-- 전체 외곽 -->
  <rect x="60" y="50" width="240" height="280" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>

  <!-- 스택 (Stack) 영역 -->
  <rect x="70" y="58" width="220" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">스택 (Stack)</text>
  <text x="180" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">함수 호출 시 자동 할당·해제</text>

  <!-- 스택 → 아래로 성장 화살표 -->
  <line x1="180" y1="112" x2="180" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="180,143 175,135 185,135" fill="currentColor"/>
  <text x="320" y="82" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">← 아래로 성장</text>

  <!-- 사용 가능한 공간 -->
  <text x="180" y="166" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">(사용 가능한 공간)</text>

  <!-- 힙 → 위로 성장 화살표 -->
  <line x1="180" y1="200" x2="180" y2="175" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="180,172 175,180 185,180" fill="currentColor"/>
  <text x="320" y="220" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">← 위로 성장</text>

  <!-- 힙 (Heap) 영역 -->
  <rect x="70" y="205" width="220" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="230" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">힙 (Heap)</text>

  <!-- 구분선 -->
  <line x1="70" y1="253" x2="290" y2="253" stroke="currentColor" stroke-width="1"/>

  <!-- 데이터 (Data) 영역 -->
  <rect x="70" y="255" width="220" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="277" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">데이터 (Data)</text>
  <text x="320" y="277" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">정적/전역 변수</text>

  <!-- 구분선 -->
  <line x1="70" y1="293" x2="290" y2="293" stroke="currentColor" stroke-width="1"/>

  <!-- 코드 (Text) 영역 -->
  <rect x="70" y="295" width="220" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="314" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">코드 (Text)</text>
  <text x="320" y="314" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">실행 가능한 기계어</text>

  <!-- 낮은 주소 라벨 -->
  <text x="210" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">낮은 주소</text>

</svg>
</div>

<br>

**스택**은 함수 호출 시 지역 변수를 위한 공간이 스택 포인터 이동만으로 자동 확보되고, 함수가 반환되면 즉시 해제됩니다. 비용은 극히 낮지만, 데이터의 수명이 함수 호출에 묶여 있어 함수가 반환되면 사라지고, 크기도 제한적입니다(플랫폼에 따라 다르지만 일반적으로 스레드당 수 MB 이내).

**힙**은 함수 범위를 넘어서 살아야 하는 데이터 — 여러 객체가 참조하는 인스턴스 등 — 를 저장하는 영역으로, 프로그램이 요청할 때 빈 공간을 탐색하여 할당됩니다. 스택과 달리 함수가 반환되어도 자동으로 해제되지 않으며, C#에서는 GC가 참조되지 않는 객체를 찾아 회수합니다. 크기는 스택보다 훨씬 크고 데이터의 수명이 함수 호출과 무관하여 여러 함수와 객체가 같은 데이터를 공유할 수 있지만, 할당과 해제에 비용이 따릅니다.

<br>

|          | 스택             | 힙               |
|----------|------------------|------------------|
| 할당     | 포인터 이동      | 빈 공간 탐색     |
| 해제     | 자동 (함수 반환) | GC 회수          |
| 크기     | 제한적 (1MB~)    | 시스템 메모리    |
| GC 대상  | 아님             | 해당             |

<br>

**값 타입**과 **참조 타입**의 구분에 따라 데이터가 스택 또는 힙에 할당됩니다.

---

### 값 타입 (Value Type)

`int`, `float`, `bool`, `Vector3`, `Quaternion`, `Color` 같은 기본 타입과 `struct`로 선언한 사용자 정의 타입이 **값 타입**입니다.

값 타입 변수는 데이터를 변수 자체에 직접 저장합니다. 지역 변수로 선언된 값 타입은 스택에 할당되어 함수가 반환되면 자동으로 해제되므로, GC가 관여하지 않습니다.

<br>

```csharp
void MoveCharacter()
{
    Vector3 direction = new Vector3(1, 0, 0);   // 스택에 12바이트 할당
    float speed = 5.0f;                         // 스택에 4바이트 할당
    Vector3 velocity = direction * speed;        // 스택에 12바이트 할당
}
// 함수 종료 → 스택 포인터 이동 → 28바이트 즉시 해제
```

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 300 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 300px; width: 100%;">

  <!-- 제목 -->
  <text x="150" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">스택</text>

  <!-- velocity 칸 -->
  <rect x="50" y="35" width="200" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="58" font-family="sans-serif" font-size="11" fill="currentColor">velocity</text>
  <text x="240" y="58" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">12 bytes</text>

  <!-- "← 스택 최상단" 라벨 -->
  <text x="258" y="58" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">← 최상단</text>

  <!-- speed 칸 -->
  <rect x="50" y="73" width="200" height="38" rx="0" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="96" font-family="sans-serif" font-size="11" fill="currentColor">speed</text>
  <text x="240" y="96" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">4 bytes</text>

  <!-- direction 칸 -->
  <rect x="50" y="111" width="200" height="38" rx="0" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="134" font-family="sans-serif" font-size="11" fill="currentColor">direction</text>
  <text x="240" y="134" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">12 bytes</text>

  <!-- 이전 프레임 칸 (점선) -->
  <rect x="50" y="149" width="200" height="38" rx="0" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="150" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(이전 함수의 스택 프레임)</text>

  <!-- 하단 설명 -->
  <text x="150" y="210" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">함수 종료 시 스택 포인터 이동 → 28바이트 즉시 해제</text>

</svg>
</div>

<br>

데이터를 직접 저장하므로 대입 시에도 **값 전체가 복사**됩니다.
`Vector3 a = b;`라고 쓰면 b의 12바이트 데이터가 a의 공간에 복사되어, a를 수정해도 b는 영향을 받지 않습니다.

---

### 참조 타입 (Reference Type)

`class`로 선언한 타입, `string`, 배열(`int[]`, `GameObject[]` 등), 델리게이트가 **참조 타입**입니다.

참조 타입 변수는 데이터 자체가 아니라 **힙에 할당된 데이터의 주소(참조)**를 저장합니다. `new`로 인스턴스를 생성하면 데이터는 힙에 할당되고, 변수에는 그 주소만 남습니다. 변수 자체는 지역 변수면 스택에, 클래스 필드면 해당 인스턴스와 함께 힙에 위치합니다.

<br>

```csharp
void SpawnEnemy()
{
    Enemy enemy = new Enemy();    // 힙에 Enemy 크기만큼 할당
                                  // 스택에는 참조(주소)만 저장
}
// 함수 종료 → 스택의 참조 변수 해제
// 힙의 Enemy 인스턴스는 남아있음 → GC가 나중에 수거
```

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">

  <!-- ========== 스택 영역 ========== -->
  <text x="100" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">스택</text>

  <!-- enemy 참조 칸 -->
  <rect x="20" y="35" width="160" height="45" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="55" font-family="sans-serif" font-size="11" fill="currentColor">enemy</text>
  <text x="170" y="55" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">참조(주소)</text>
  <text x="100" y="100" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">함수 반환 시 해제</text>

  <!-- ========== 힙 영역 ========== -->
  <text x="400" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">힙</text>

  <!-- Enemy 인스턴스 박스 -->
  <rect x="300" y="35" width="200" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="56" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Enemy 인스턴스</text>
  <line x1="310" y1="65" x2="490" y2="65" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="315" y="85" font-family="sans-serif" font-size="11" fill="currentColor">hp = 100</text>
  <text x="490" y="85" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">int</text>
  <text x="315" y="105" font-family="sans-serif" font-size="11" fill="currentColor">position</text>
  <text x="490" y="105" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Vector3</text>
  <text x="315" y="125" font-family="sans-serif" font-size="11" fill="currentColor">name = "Goblin"</text>
  <text x="490" y="125" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">string</text>
  <text x="400" y="162" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">함수 반환 후에도 유지 → GC가 회수</text>

  <!-- enemy → Enemy 인스턴스 화살표 -->
  <line x1="180" y1="55" x2="292" y2="55" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="288,50 298,55 288,60" fill="currentColor"/>
  <text x="238" y="48" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">가리킴</text>

  <!-- 하단 요약 -->
  <text x="270" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 변수(스택)는 주소만 저장, 실제 데이터(힙)는 별도 공간에 위치</text>

</svg>
</div>

<br>

주소를 저장하므로 대입 시에도 **참조만 복사**됩니다.
`Enemy a = b;`라고 쓰면 a와 b가 같은 힙 메모리를 가리키므로, a를 통해 수정한 데이터는 b로 접근해도 동일합니다.

---

### 값 타입과 참조 타입이 성능에 미치는 영향

값 타입과 참조 타입의 성능 차이는 **할당 위치**에서 비롯됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- 중앙 구분선 -->
  <line x1="310" y1="10" x2="310" y2="200" stroke="currentColor" stroke-width="1" opacity="0.15"/>

  <!-- 제목 -->
  <text x="155" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">값 타입 (스택)</text>
  <text x="465" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">참조 타입 (힙)</text>

  <!-- 행 1: 할당 -->
  <text x="20" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">할당</text>
  <text x="80" y="55" font-family="sans-serif" font-size="11" fill="currentColor">스택 포인터 이동</text>
  <text x="80" y="71" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(1단계)</text>

  <text x="330" y="55" font-family="sans-serif" font-size="11" fill="currentColor">1. 빈 공간 탐색</text>
  <text x="330" y="73" font-family="sans-serif" font-size="11" fill="currentColor">2. 메모리 블록 확보</text>
  <text x="330" y="91" font-family="sans-serif" font-size="11" fill="currentColor">3. 오브젝트 헤더 초기화</text>

  <!-- 행 2: 해제 -->
  <text x="20" y="115" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">해제</text>
  <text x="80" y="115" font-family="sans-serif" font-size="11" fill="currentColor">함수 반환 시 자동</text>

  <text x="330" y="115" font-family="sans-serif" font-size="11" fill="currentColor">GC가 수거할 때까지 유보</text>

  <!-- 행 3: GC -->
  <text x="20" y="150" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GC</text>
  <text x="80" y="150" font-family="sans-serif" font-size="11" fill="currentColor">없음</text>

  <text x="330" y="150" font-family="sans-serif" font-size="11" fill="currentColor">발생 — 힙 전체를 순회하여 회수</text>

  <!-- 결론 구분선 -->
  <line x1="20" y1="170" x2="600" y2="170" stroke="currentColor" stroke-width="1" opacity="0.15"/>

  <!-- 결론 -->
  <text x="155" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 비용 극히 낮음, GC 부담 없음</text>
  <text x="465" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 할당 누적 시 GC 부담 증가</text>

</svg>
</div>

<br>

한 번의 힙 할당 비용은 마이크로초 단위로 작지만, 할당이 누적되면 **해제를 담당하는 GC**가 더 자주, 더 오래 실행되어 체감 비용이 커집니다.

<br>

Unity가 사용하는 **Boehm GC**는 세대 구분 없이 매번 힙 전체를 순회하며, 이 순회가 메인 스레드에서 실행되므로 게임 로직이 멈춥니다. 힙에 오브젝트가 많을수록 순회 시간이 길어지고, 프레임 예산을 초과하면 프레임 드롭으로 이어지므로, 매 프레임 실행되는 코드에서 **힙 할당을 0에 가깝게 유지**하는 것이 핵심입니다.

Boehm GC의 동작 원리와 프레임 예산에 미치는 영향은 [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)에서 자세히 다룹니다.

## 숨은 힙 할당 패턴들

`new`로 class 인스턴스를 만들면 힙 할당이 발생한다는 점은 코드에서 바로 보입니다.
그런데 `new`를 쓰지 않아도 컴파일러나 런타임이 내부적으로 힙 할당을 수행하는 경우가 있어, 매 프레임 실행되는 코드에서 의도치 않게 GC 압박이 쌓일 수 있습니다. 문자열 연결, LINQ, 박싱, 클로저, foreach Enumerator, params 배열이 대표적입니다.

### 문자열 연결

`string`은 C#에서 참조 타입이므로 힙에 할당되며, 한 번 생성된 객체의 내용을 변경할 수 없는 **불변(immutable)** 타입입니다. 내용을 변경할 수 없으므로 문자열을 연결하거나 치환하면 기존 객체를 수정하는 대신 결과를 담은 새로운 string 객체가 힙에 생성됩니다.

<br>

```csharp
string result = "HP: " + currentHP + "/" + maxHP;
```

위 코드에서 C# 컴파일러는 여러 `+` 연산을 `string.Concat` 단일 호출로 합쳐 중간 문자열 생성을 줄이지만, Concat 자체가 결과를 담은 새 문자열을 힙에 생성하므로 힙 할당은 여전히 발생합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">

  <!-- 호출 코드 -->
  <text x="280" y="18" text-anchor="middle" font-family="monospace" font-size="10.5" fill="currentColor">string.Concat("HP: ", currentHP.ToString(), "/", maxHP.ToString())</text>

  <!-- #1 -->
  <rect x="40" y="34" width="480" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="56" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">#1</text>
  <text x="85" y="56" font-family="sans-serif" font-size="11" fill="currentColor">currentHP.ToString()</text>
  <text x="290" y="56" font-family="sans-serif" font-size="11" fill="currentColor">→ 새 string "75"</text>
  <text x="500" y="56" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">힙 할당</text>

  <!-- 화살표 1→2 -->
  <line x1="280" y1="68" x2="280" y2="82" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="276,79 280,87 284,79" fill="currentColor" opacity="0.4"/>

  <!-- #2 -->
  <rect x="40" y="88" width="480" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="110" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">#2</text>
  <text x="85" y="110" font-family="sans-serif" font-size="11" fill="currentColor">maxHP.ToString()</text>
  <text x="290" y="110" font-family="sans-serif" font-size="11" fill="currentColor">→ 새 string "100"</text>
  <text x="500" y="110" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">힙 할당</text>

  <!-- 화살표 2→3 -->
  <line x1="280" y1="122" x2="280" y2="136" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="276,133 280,141 284,133" fill="currentColor" opacity="0.4"/>

  <!-- #3 -->
  <rect x="40" y="142" width="480" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="164" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">#3</text>
  <text x="85" y="164" font-family="sans-serif" font-size="11" fill="currentColor">string.Concat 결과</text>
  <text x="290" y="164" font-family="sans-serif" font-size="11" fill="currentColor">→ 새 string "HP: 75/100"</text>
  <text x="500" y="164" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">힙 할당</text>

  <!-- 요약 -->
  <text x="280" y="205" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.55">→ 힙 할당 3회, "75"와 "100"은 이후 GC 대상</text>

</svg>
</div>

<br>

이 코드가 매 프레임 UI 텍스트를 갱신하기 위해 Update()에서 호출된다면, 60fps 기준으로 초당 180회의 힙 할당이 이 한 줄에서만 발생합니다.

이 비용을 줄이려면 `StringBuilder`를 사용합니다. StringBuilder는 내부 char 배열 버퍼에 문자열을 이어 쓰므로 Append마다 새 string 객체를 생성하지 않습니다.

<br>

```csharp
// 클래스 필드로 한 번만 생성
private StringBuilder sb = new StringBuilder(64);

void UpdateHPText()
{
    sb.Clear();
    sb.Append("HP: ");
    sb.Append(currentHP);
    sb.Append("/");
    sb.Append(maxHP);
    hpText.text = sb.ToString();   // ToString()에서 한 번만 힙 할당
}
```

<br>

StringBuilder를 필드로 한 번 생성해두고 재사용하면, `+` 연결에서 발생하던 중간 문자열 할당이 사라집니다. 최종 `ToString()` 호출에서 결과 string 하나만 힙에 할당됩니다.

이전 결과를 캐시해두고 값이 바뀔 때만 StringBuilder를 실행하면, 변화가 없는 프레임에서는 힙 할당이 발생하지 않습니다.

> `ToString()` 호출의 할당마저 제거하려면, `Span<T>`과 스택 메모리를 활용하여 힙 할당 없이 문자열을 조립하는 [ZString](https://github.com/Cysharp/ZString) 같은 라이브러리를 사용할 수 있습니다.

---

### LINQ

**LINQ(Language Integrated Query)**는 `Where`, `Select`, `OrderBy` 같은 메서드를 체인으로 이어 붙여 컬렉션을 필터링·정렬·변환하는 문법으로, 코드는 간결하지만 내부적으로 힙 할당을 유발합니다.

<br>

```csharp
var activeEnemies = enemies.Where(e => e.IsAlive).OrderBy(e => e.Distance);
```

<br>

이 한 줄은 읽기 쉽지만, 내부적으로 여러 힙 할당을 수반합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- #1 -->
  <rect x="30" y="10" width="460" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="32" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">#1</text>
  <text x="75" y="32" font-family="sans-serif" font-size="11" fill="currentColor">Where()가 이터레이터 객체 생성</text>
  <text x="470" y="32" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">힙 할당</text>

  <!-- 화살표 1→2 -->
  <line x1="260" y1="44" x2="260" y2="56" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="256,53 260,61 264,53" fill="currentColor" opacity="0.4"/>

  <!-- #2 -->
  <rect x="30" y="62" width="460" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">#2</text>
  <text x="75" y="84" font-family="sans-serif" font-size="11" fill="currentColor">OrderBy()가 이터레이터 객체 생성</text>
  <text x="470" y="84" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">힙 할당</text>

  <!-- 화살표 2→3 -->
  <line x1="260" y1="96" x2="260" y2="108" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="256,105 260,113 264,105" fill="currentColor" opacity="0.4"/>

  <!-- #3 -->
  <rect x="30" y="114" width="460" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="136" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">#3</text>
  <text x="75" y="136" font-family="sans-serif" font-size="11" fill="currentColor">열거 시 정렬용 내부 버퍼 할당</text>
  <text x="470" y="136" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">힙 할당</text>


</svg>
</div>

<br>

LINQ 연산자는 호출 시점에 결과를 바로 계산하지 않고, 나중에 실제로 데이터를 순회할 때 계산합니다. 이를 **지연 평가(lazy evaluation)**라고 합니다.

지연 평가를 위해 각 연산자는 "다음 원소를 달라"는 요청에 하나씩 응답하며 컬렉션을 순회하는 **이터레이터 객체**를 힙에 생성합니다.
`OrderBy` 같은 정렬 연산은 이터레이터 외에 정렬용 내부 버퍼도 힙에 할당합니다.

이 할당은 LINQ 호출마다 발생하므로, 초기화 코드처럼 한 번만 실행되는 곳에서는 문제되지 않지만 매 프레임 실행되는 경로에서는 for 루프와 직접 조건 분기로 대체하여 힙 할당을 피할 수 있습니다.

<br>

```csharp
// LINQ 대신 for 루프로 대체
for (int i = 0; i < enemies.Count; i++)
{
    if (enemies[i].IsAlive)
    {
        // 처리
    }
}
```

---

### 박싱 (Boxing)

**박싱(Boxing)**은 값 타입을 `object`, `System.ValueType`, 또는 인터페이스 같은 참조 타입으로 변환할 때 발생합니다. 참조 타입은 힙에 존재해야 하므로, 값 타입 데이터를 힙에 새로 생성한 객체로 복사하는 과정이 필요하며, 이 복사마다 힙 할당이 수반됩니다.

<br>

```csharp
int score = 100;
object boxed = score;    // 박싱 발생
```

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">

  <!-- ========== 스택 영역 ========== -->
  <text x="100" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">스택</text>

  <!-- score 칸 -->
  <rect x="20" y="35" width="160" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="58" font-family="sans-serif" font-size="11" fill="currentColor">score = 100</text>
  <text x="170" y="58" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">4 bytes</text>

  <!-- boxed 칸 -->
  <rect x="20" y="83" width="160" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="106" font-family="sans-serif" font-size="11" fill="currentColor">boxed</text>
  <text x="170" y="106" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">참조</text>

  <!-- ========== 힙 영역 ========== -->
  <text x="400" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">힙</text>

  <!-- 박싱된 객체 박스 -->
  <rect x="300" y="35" width="200" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">박싱된 객체</text>
  <line x1="310" y1="62" x2="490" y2="62" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="315" y="80" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 헤더</text>
  <text x="490" y="80" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">12~20 bytes</text>
  <line x1="310" y1="90" x2="490" y2="90" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="315" y="110" font-family="sans-serif" font-size="11" fill="currentColor">값: 100</text>
  <text x="490" y="110" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">4 bytes</text>

  <!-- boxed → 힙 객체 참조 화살표 -->
  <line x1="180" y1="102" x2="292" y2="80" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="288,76 298,80 290,85" fill="currentColor"/>
  <text x="238" y="84" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">가리킴</text>

  <!-- 하단: 크기 대비 요약 -->
  <text x="100" y="155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">4 bytes</text>
  <text x="250" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">→</text>
  <text x="400" y="155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">16~24 bytes</text>
  <text x="270" y="185" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 4바이트 int 하나가 박싱되면 16~24바이트 힙 객체가 생성</text>

</svg>
</div>

<br>

힙에 할당되는 모든 참조 타입 객체에는 데이터 앞에 **오브젝트 헤더**가 붙습니다.
오브젝트 헤더는 런타임이 객체의 타입과 상태를 관리하기 위한 메타데이터로, 플랫폼에 따라 12~20바이트를 차지합니다. 4바이트짜리 int 하나가 박싱되면 이 헤더가 추가되어 힙에 16~24바이트의 객체가 생성됩니다.

이런 박싱은 코드 표면에 드러나지 않는 곳에서도 발생합니다.

예를 들어 `string.Format`은 매개변수 타입이 `object`이므로, `string.Format("{0}", intValue)`처럼 값 타입을 전달하면 박싱이 발생합니다. 문자열 보간(`$"HP: {hp}"`)도 Unity의 .NET 프로파일에서는 `string.Format`으로 컴파일되므로 동일합니다.

<br>

```csharp
int hp = 75;
string text = string.Format("HP: {0}", hp);   // hp가 object로 박싱됨
string text2 = $"HP: {hp}";                    // 동일하게 박싱 발생
```

<br>

`ArrayList`나 `Hashtable` 같은 비제네릭 컬렉션도 요소를 `object`로 저장하므로, 값 타입을 추가할 때마다 박싱이 발생합니다.

<br>

```csharp
ArrayList list = new ArrayList();
list.Add(42);         // 42가 박싱됨
list.Add(3.14f);      // 3.14f가 박싱됨
```

<br>

반면 `List<int>` 같은 제네릭 컬렉션은 요소를 int 타입 그대로 저장하므로 박싱이 발생하지 않으며, `Dictionary<TKey, TValue>`도 마찬가지입니다.
비제네릭 컬렉션 대신 제네릭 컬렉션을 사용하면 값 타입 저장 시 박싱을 피할 수 있습니다.

다만 `Dictionary`의 키로 struct를 사용할 때는, struct가 `IEquatable<T>`를 구현했는지에 따라 박싱 여부가 달라집니다.
`Dictionary`는 키를 비교할 때 `EqualityComparer<TKey>.Default`를 사용하는데, `IEquatable<T>`를 구현한 struct는 제네릭 타입 `T`를 그대로 받는 `Equals(T)`가 호출되어 박싱이 발생하지 않습니다.
구현하지 않은 struct는 `object.Equals(object)`로 폴백되어, 매개변수 타입이 `object`이므로 키가 박싱됩니다.

---

### 람다와 클로저

**람다 식(lambda expression)**은 별도의 메서드를 선언하지 않고 인라인으로 짧은 함수를 정의하는 문법으로, 사용 방식에 따라 힙 할당을 유발합니다.

<br>

```csharp
enemies.Sort((a, b) => a.Distance.CompareTo(b.Distance));
```

<br>

람다가 자신의 매개변수만 사용하고 **바깥 범위의 변수를 사용하지 않으면**, C# 컴파일러가 델리게이트를 정적 필드에 캐시합니다.
캐시된 델리게이트가 재사용되므로, 반복 호출에서 추가 힙 할당이 발생하지 않습니다.

반면 람다가 자신의 매개변수가 아닌 바깥 범위의 변수에 접근하여 함께 유지하는 것을 **캡처(capture)**라 하며, 캡처가 발생할 때마다 힙 할당이 수반됩니다.
캡처된 변수는 원래 스택에 존재하지만, 람다는 자신을 만든 함수가 반환된 뒤에도 콜백 등으로 실행될 수 있으므로 스택에 남겨두면 접근할 수 없습니다.

이를 해결하기 위해 C# 컴파일러는 캡처된 변수를 담는 숨겨진 클래스를 생성하고, 런타임에 이 클래스의 인스턴스를 힙에 할당하여 변수의 수명을 연장합니다.

```csharp
void SetupButton()
{
    string menuId = "settings";
    button.onClick.AddListener(() => OpenMenu(menuId));
}
// SetupButton()은 즉시 반환됨
// 버튼 클릭은 수 초~수 분 뒤에 발생 → 그때 람다가 실행됨
```

`SetupButton()`이 반환되면 스택 프레임이 사라지고, 지역 변수 `menuId`도 함께 사라집니다. 그런데 버튼 클릭 시 실행되는 람다는 여전히 `menuId`에 접근해야 합니다.
C# 컴파일러가 `menuId`를 힙의 클로저 객체로 옮기는 이유가 바로 이것입니다. 스택에 남겨두면 함수 반환 후 접근할 수 없기 때문입니다.

이처럼 캡처가 발생하는 람다와 캡처된 변수를 담은 환경을 합쳐 **클로저(closure)**라고 합니다.

<br>

```csharp
void FilterByRange(float maxRange)
{
    var inRange = enemies.FindAll(e => e.Distance < maxRange);
    // maxRange를 캡처 → 클로저
}
```

<br>

`maxRange`는 `FilterByRange`의 매개변수이므로 람다 입장에서는 바깥 범위의 변수, 즉 캡처 대상입니다.
`FilterByRange`가 매 프레임 호출된다면, 호출마다 클로저 객체가 힙에 생성되어 GC 압박이 누적됩니다.

이를 피하려면 캡처 대상 변수를 클래스 필드로 옮기고 람다 대신 일반 메서드를 사용하면 됩니다. 필드는 클래스 인스턴스와 함께 힙에 이미 존재하므로 수명 연장이 필요 없고, 바깥 변수를 참조하지 않는 일반 메서드의 델리게이트는 컴파일러가 캐시하므로 추가 할당도 발생하지 않습니다.

<br>

```csharp
// 캡처 발생 → 매 호출마다 클로저 + 델리게이트 힙 할당
void Update()
{
    float maxRange = attackRange;
    var inRange = enemies.FindAll(e => e.Distance < maxRange);
}
```

<br>

```csharp
// 캡처 제거 + 델리게이트 캐시 → 클로저·델리게이트 할당 제거
// (FindAll 자체는 결과를 담을 새 List를 반환하므로 힙 할당이 발생합니다)
private float maxRange;
private Predicate<Enemy> isInRangePredicate;

bool IsInRange(Enemy e) => e.Distance < maxRange;

void Awake()
{
    isInRangePredicate = IsInRange;   // 델리게이트를 한 번만 생성
}

void Update()
{
    maxRange = attackRange;
    var inRange = enemies.FindAll(isInRangePredicate);
}
```

---

### foreach와 Enumerator

`foreach` 문은 컬렉션 순회 시 내부적으로 `GetEnumerator()`를 호출하여 Enumerator 객체를 얻습니다. Enumerator가 class(참조 타입)로 구현되어 있으면 이 객체가 힙에 할당되고, struct(값 타입)로 구현되어 있으면 힙 할당 없이 스택에서 처리됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 195" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- 왼쪽: foreach 문법 -->
  <text x="105" y="16" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">foreach 문법</text>
  <rect x="5" y="24" width="200" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="18" y="50" font-family="monospace" font-size="10.5" fill="currentColor">foreach (var item</text>
  <text x="18" y="67" font-family="monospace" font-size="10.5" fill="currentColor">        in collection)</text>
  <text x="18" y="84" font-family="monospace" font-size="10.5" fill="currentColor">{</text>
  <text x="18" y="101" font-family="monospace" font-size="10.5" fill="currentColor">    // item 사용</text>
  <text x="18" y="118" font-family="monospace" font-size="10.5" fill="currentColor">}</text>

  <!-- 중앙 화살표 -->
  <line x1="220" y1="84" x2="260" y2="84" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="258,79 267,84 258,89" fill="currentColor"/>
  <text x="243" y="72" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">컴파일러</text>
  <text x="243" y="102" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">변환</text>

  <!-- 오른쪽: 변환된 코드 -->
  <text x="450" y="16" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">컴파일러가 변환한 코드</text>
  <rect x="275" y="24" width="340" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="288" y="48" font-family="monospace" font-size="10.5" fill="currentColor">var e = collection.GetEnumerator();</text>
  <text x="288" y="65" font-family="monospace" font-size="10.5" fill="currentColor">while (e.MoveNext())</text>
  <text x="288" y="82" font-family="monospace" font-size="10.5" fill="currentColor">{</text>
  <text x="288" y="99" font-family="monospace" font-size="10.5" fill="currentColor">    var item = e.Current;</text>
  <text x="288" y="116" font-family="monospace" font-size="10.5" fill="currentColor">    // item 사용</text>
  <text x="288" y="133" font-family="monospace" font-size="10.5" fill="currentColor">}</text>

  <!-- GetEnumerator 주석 -->
  <text x="610" y="48" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← Enumerator 생성</text>

  <!-- 하단 요약 -->
  <text x="310" y="175" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ Enumerator가 class면 힙 할당, struct면 할당 없음</text>

</svg>
</div>

<br>

`List<T>`와 `Dictionary<TKey, TValue>`의 Enumerator는 struct로 구현되어 있어 foreach로 순회해도 힙 할당이 발생하지 않습니다.

다만 같은 컬렉션이라도 `IEnumerable<T>` 타입 변수에 담거나 매개변수로 `IEnumerable<T>`을 받아 순회하면 박싱이 발생할 수 있습니다. `IEnumerable<T>`의 `GetEnumerator()`는 `IEnumerator<T>` 인터페이스를 반환하므로, struct Enumerator가 인터페이스로 변환되면서 힙 할당이 일어나기 때문입니다.

<br>

```csharp
// List<Enemy> 타입 그대로 순회 → struct Enumerator → 박싱 없음
foreach (var e in enemies) { ... }

// IEnumerable<T>을 거쳐 순회 → struct Enumerator가 인터페이스로 변환 → 박싱 발생
IEnumerable<Enemy> enumerable = enemies;
foreach (var e in enumerable) { ... }

// 매개변수가 IEnumerable<T>인 경우도 동일
void ProcessEnemies(IEnumerable<Enemy> targets)
{
    foreach (var e in targets) { ... }   // 박싱 발생
}
```

<br>

Enumerator가 struct인지 class인지 확인하기 어려운 컬렉션을 매 프레임 순회해야 한다면, for 루프와 인덱서로 대체하여 힙 할당을 피할 수 있습니다.

<br>

```csharp
for (int i = 0; i < list.Count; i++)
{
    var item = list[i];
}
```

### params 배열

`params` 키워드가 붙은 매개변수는 호출 시 전달된 가변 인자를 배열로 받습니다.

<br>

```csharp
void LogMessage(string format, params object[] args)
{
    // ...
}

LogMessage("Player {0} scored {1}", playerName, score);
```

<br>

위 호출처럼 `params object[]`를 사용하면, C# 컴파일러가 호출 시점에 인자를 담을 새 배열을 힙에 생성하는 코드를 삽입합니다.
배열의 원소 타입이 `object`이므로, 인자가 값 타입이면 박싱도 추가로 발생합니다.

Unity의 `Debug.LogFormat`도 `params object[]`를 사용하므로 같은 할당이 발생합니다. 인자 수가 고정되어 있다면 오버로드를 만들어 배열 생성을 피할 수 있습니다.

<br>

```csharp
// params object[] → 호출마다 배열 힙 할당
void LogMessage(string format, params object[] args) { ... }

// 인자 수별 오버로드 → 배열 할당 없음
void LogMessage(string format, object arg0) { ... }
void LogMessage(string format, object arg0, object arg1) { ... }
```

---

### 숨은 힙 할당 패턴 정리

| 패턴                     | 대안                                    |
|--------------------------|------------------------------------------|
| string 연결 (+)          | StringBuilder 재사용                    |
| LINQ 체인                | for 루프와 직접 조건 분기               |
| 박싱 (int → object)      | 제네릭 컬렉션, 오버로드                |
| 클로저 (외부 변수 캡처)  | 필드로 이동, 일반 메서드               |
| foreach (일부 컬렉션)    | for + 인덱서                           |
| params 배열              | 고정 인자 수 오버로드                  |

<br>

위 패턴들은 매 프레임 실행되는 코드(Update, FixedUpdate, LateUpdate)에서 가장 먼저 점검할 대상입니다. 초기화 코드나 씬 전환처럼 한 번만 실행되는 경로에서는 가독성과 유지보수성을 우선해도 됩니다.

---

## 오브젝트 풀링

코드 수준의 힙 할당 패턴 외에, 총알, 파티클 이펙트, 적 캐릭터처럼 게임 플레이 중 반복적으로 생성·파괴되는 오브젝트도 GC 부담의 원인이 됩니다.

### Instantiate와 Destroy의 비용

`Instantiate()`는 프리팹을 복제하여 새 GameObject를 만듭니다.
이 과정에서 Unity는 네이티브 메모리와 관리 메모리 양쪽에 새 공간을 할당하고, 프리팹에 저장된 컴포넌트 속성값(직렬화된 데이터)을 새 오브젝트로 복사한 뒤, `Awake`와 `OnEnable` 콜백을 호출합니다.

이렇게 생성된 오브젝트가 더 이상 필요하지 않으면 `Destroy()`로 파괴하는데, 모든 메모리가 즉시 해제되는 것은 아닙니다.
Unity의 GameObject는 Transform이나 Mesh 등 실제 오브젝트 데이터를 담는 **네이티브 메모리**와, MonoBehaviour 인스턴스나 GameObject 참조 등 C# 측 객체를 담는 **관리 메모리(managed memory)** 힙으로 나뉘어 있는데, `Destroy()`는 네이티브 메모리만 즉시 해제하고 관리 메모리 쪽은 GC가 수거할 때까지 힙에 남깁니다.
게임 로직이 Instantiate와 Destroy를 반복 호출하면 관리 메모리 쪽의 미회수 객체가 쌓여 GC 부담이 커집니다.

네이티브 메모리와 관리 메모리의 구조는 [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)에서 자세히 다룹니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 175" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">

  <!-- Instantiate 박스 -->
  <rect x="20" y="15" width="150" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="40" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Instantiate()</text>

  <!-- 화살표 → 사용 -->
  <line x1="170" y1="35" x2="195" y2="35" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="193,30 202,35 193,40" fill="currentColor"/>

  <!-- 사용 박스 -->
  <rect x="205" y="15" width="80" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="245" y="40" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">사용</text>

  <!-- 화살표 → Destroy -->
  <line x1="285" y1="35" x2="310" y2="35" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="308,30 317,35 308,40" fill="currentColor"/>

  <!-- Destroy 박스 -->
  <rect x="320" y="15" width="150" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="395" y="40" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Destroy()</text>

  <!-- 반복 표시 -->
  <text x="505" y="40" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">↻ 반복</text>

  <!-- Destroy 결과: 비대칭 해제 -->
  <text x="330" y="78" font-family="sans-serif" font-size="10" fill="currentColor">네이티브 메모리</text>
  <text x="470" y="78" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 즉시 해제</text>
  <text x="330" y="96" font-family="sans-serif" font-size="10" fill="currentColor">관리 메모리</text>
  <text x="470" y="96" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 힙에 잔존</text>

  <!-- 구분선 -->
  <line x1="20" y1="115" x2="540" y2="115" stroke="currentColor" stroke-width="1" opacity="0.15"/>

  <!-- 하단 결론 -->
  <text x="280" y="140" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 반복할수록 관리 메모리의 미회수 객체가 누적되어 GC 부담 증가</text>
  <text x="280" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ GC 실행 시 프레임 스파이크</text>

</svg>
</div>

<br>

---

### 풀링의 원리

**오브젝트 풀링(Object Pooling)**은 오브젝트를 파괴하는 대신 **비활성화하여 보관하고**, 새로 필요할 때 **다시 활성화하여 재사용**하는 패턴입니다.
Instantiate와 Destroy를 호출하지 않으므로 힙 할당과 GC 대상이 생기지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- 초기화 라벨 -->
  <text x="10" y="38" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">초기화</text>

  <!-- Instantiate × N -->
  <rect x="80" y="18" width="150" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="155" y="41" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Instantiate × N</text>

  <!-- 화살표 → -->
  <line x1="230" y1="36" x2="255" y2="36" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="253,31 262,36 253,41" fill="currentColor"/>

  <!-- 비활성화 후 풀에 보관 -->
  <rect x="263" y="18" width="290" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="408" y="41" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">SetActive(false) → 풀에 보관</text>

  <!-- 꺼내기 라벨 -->
  <text x="10" y="98" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">꺼내기</text>

  <rect x="80" y="78" width="340" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="101" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">풀에서 비활성 오브젝트를 가져와 SetActive(true)</text>

  <!-- 반환 라벨 -->
  <text x="10" y="155" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">반환</text>

  <rect x="80" y="135" width="310" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="235" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">사용 종료 → SetActive(false) → 풀에 반환</text>

  <!-- 부연 설명 -->
  <text x="80" y="190" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ Destroy()를 호출하지 않으므로 GC 대상이 되지 않음</text>

</svg>
</div>

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- 풀링 없음 섹션 -->
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">풀링 없음</text>

  <rect x="40" y="30" width="120" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Instantiate</text>

  <line x1="160" y1="47" x2="185" y2="47" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="183,42 192,47 183,52" fill="currentColor"/>

  <rect x="193" y="30" width="80" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="233" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">사용</text>

  <line x1="273" y1="47" x2="298" y2="47" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="296,42 305,47 296,52" fill="currentColor"/>

  <rect x="306" y="30" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="356" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Destroy</text>

  <text x="420" y="52" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(매 생성마다 반복)</text>

  <!-- 결론 화살표 -->
  <text x="100" y="82" font-family="sans-serif" font-size="11" fill="currentColor">→ 힙 할당 누적 → GC 스파이크</text>

  <!-- 구분선 -->
  <line x1="40" y1="100" x2="580" y2="100" stroke="currentColor" stroke-width="1" opacity="0.2"/>

  <!-- 풀링 적용 섹션 -->
  <text x="310" y="125" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">풀링 적용</text>

  <!-- 초기화 행 -->
  <text x="40" y="152" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">초기화 시</text>

  <rect x="110" y="135" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="157" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Instantiate × N (한 번)</text>

  <!-- 이후 행 -->
  <text x="40" y="192" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">이후</text>

  <rect x="110" y="175" width="140" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="197" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">SetActive(true)</text>

  <line x1="250" y1="192" x2="270" y2="192" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="268,187 277,192 268,197" fill="currentColor"/>

  <rect x="278" y="175" width="80" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="318" y="197" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">사용</text>

  <line x1="358" y1="192" x2="378" y2="192" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="376,187 385,192 376,197" fill="currentColor"/>

  <rect x="386" y="175" width="150" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="461" y="197" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">SetActive(false)</text>

  <!-- 결론 -->
  <text x="110" y="226" font-family="sans-serif" font-size="11" fill="currentColor">→ 게임 플레이 중 Instantiate/Destroy 없음</text>

</svg>
</div>

---

### 풀링이 적합한 대상

풀링은 총알, 파티클 이펙트, 대미지 텍스트처럼 **짧은 수명 주기로 반복 생성·파괴되는 오브젝트**에 효과적입니다.
플레이어 캐릭터나 배경 지형처럼 씬에 한 번 생성되고 유지되는 오브젝트에는 불필요합니다.

풀 크기는 동시에 활성화될 수 있는 오브젝트의 최대 수에 맞춰 결정합니다. 예를 들어 총알이 화면에 동시에 최대 30개까지 존재한다면 30~40개로 잡으면 됩니다.
풀이 부족하면 추가로 Instantiate하거나, 가장 오래된 활성 오브젝트를 강제 반환하는 정책을 택할 수 있습니다.

### Unity의 ObjectPool<T>

Unity 2021.1부터 `UnityEngine.Pool` 네임스페이스에 `ObjectPool<T>` 클래스가 제공됩니다.

<br>

```csharp
using UnityEngine.Pool;

public class BulletPool : MonoBehaviour
{
    public GameObject bulletPrefab;
    private ObjectPool<GameObject> pool;

    void Awake()
    {
        pool = new ObjectPool<GameObject>(
            createFunc:      () => Instantiate(bulletPrefab),
            actionOnGet:     bullet => bullet.SetActive(true),
            actionOnRelease: bullet => bullet.SetActive(false),
            actionOnDestroy: bullet => Destroy(bullet),
            defaultCapacity: 30,
            maxSize:         100
        );
    }

    public GameObject GetBullet()  => pool.Get();       // 풀에서 꺼내기
    public void ReturnBullet(GameObject bullet) => pool.Release(bullet); // 풀에 반환
}
```

<br>

`Get()` 호출 시 풀에 가용 오브젝트가 있으면 꺼내고, 없으면 `createFunc`으로 새로 생성합니다.

`Release()` 시 풀이 `maxSize`에 도달해 있으면 오브젝트를 풀에 보관하지 않고 `actionOnDestroy`로 폐기하며,
`Clear()`나 `Dispose()` 호출 시에도 `actionOnDestroy`가 실행됩니다.

`defaultCapacity`는 내부 컬렉션의 초기 용량, `maxSize`는 풀이 보관할 수 있는 최대 오브젝트 수입니다.

`ObjectPool<T>`은 스레드 안전(thread-safe)하지 않아 여러 스레드가 동시에 접근하면 데이터가 깨질 수 있으므로, Unity의 메인 스레드에서만 사용해야 합니다.
Unity의 게임 로직(Update, FixedUpdate 등)은 메인 스레드에서 실행되므로 일반적인 풀링 사용에서는 문제가 되지 않지만, Job System이나 async/await 등 멀티스레드 환경에서 풀에 접근해야 한다면 별도의 동기화가 필요합니다.

### 풀링 사용 시 주의점

풀에서 꺼낸 오브젝트에는 이전 사용의 상태가 남아 있을 수 있으므로, 총알의 속도, 방향, 대미지 등을 꺼낼 때마다 초기화해야 합니다. `actionOnGet` 콜백이 이 초기화를 수행하기에 적합합니다.

또한 오브젝트를 꺼낸 후 반환하지 않으면 풀이 점점 비어 새 오브젝트를 계속 생성하게 되므로, 오브젝트의 수명이 끝나는 모든 경로(충돌, 시간 초과, 화면 밖 이동 등)에서 반환을 호출해야 합니다.

풀에 미리 생성하는 오브젝트만큼 게임 시작 시점부터 메모리를 차지한다는 점도 고려해야 합니다. 필요한 만큼만 미리 만들고, 부족할 때 추가 생성하는 방식으로 초기 비용을 조절할 수 있습니다.

## C# 할당 패턴을 넘어서

C# 코드에서 힙 할당 패턴을 제거하면 GC 압박은 줄어듭니다. 하지만 Unity 게임에서 스크립트 비용의 상당 부분은 **Unity API 호출**에서도 발생합니다.

`GetComponent`, `Find`, `SendMessage` 같은 API는 C# 코드에서 한 줄이지만, 내부적으로 관리 코드(C#)에서 네이티브 코드(C++)로 호출 경계를 넘으며 데이터 변환과 검증이 발생합니다. API에 따라 씬 전체 검색이나 배열 할당 등의 숨은 비용도 추가됩니다.

Unity API 수준의 비용 구조와 대안은 [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)에서 다룹니다.

## 마무리

C# 스크립트의 CPU 비용은 코드 실행 비용과 힙 할당·GC 비용으로 나뉘며, 힙 할당을 줄여 GC 부담을 최소화하는 것이 프레임 안정성의 핵심입니다.

- Mono(JIT)는 실행 시점에, IL2CPP(AOT)는 빌드 시점에 IL을 기계어로 변환하며, 모바일 빌드에서는 IL2CPP가 기본 백엔드로 권장됩니다.
- IL2CPP는 네이티브 C++ 컴파일러의 최적화 패스를 활용해 실행 속도를 높이고, 코드 스트리핑으로 빌드 크기를 줄입니다.
- 값 타입은 스택에 할당되어 GC 대상이 아니고, 참조 타입은 힙에 할당되어 GC가 관리합니다.
- Unity의 Boehm GC는 세대 구분 없이 힙 전체를 순회하며, 메인 스레드에서 실행되어 프레임을 멈춥니다.
- string 연결, LINQ, 박싱, 클로저, foreach Enumerator, params 배열은 `new` 없이도 힙 할당을 유발합니다.
- 매 프레임 실행되는 코드에서 힙 할당을 0에 가깝게 유지하는 것이 GC 스파이크 예방의 핵심 전략입니다.
- 오브젝트 풀링은 미리 생성한 오브젝트를 비활성화·재활성화하여 런타임 Instantiate/Destroy 호출을 제거합니다.

코드 한 줄이 힙 할당을 유발하는지는 C#의 타입 시스템과 컴파일러 동작에 달려 있습니다. 이 패턴들을 인지하면, 프로파일러에서 GC 스파이크를 발견했을 때 원인을 추적하는 출발점이 됩니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)

**시리즈**
- **스크립트 최적화 (1) - C# 실행과 메모리 할당 (현재 글)**
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)

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
- **스크립트 최적화 (1) - C# 실행과 메모리 할당** (현재 글)
- [스크립트 최적화 (2) - Unity API와 실행 비용](/dev/unity/ScriptOptimization-2/)
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
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
