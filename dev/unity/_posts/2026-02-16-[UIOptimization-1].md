---
layout: single
title: "UI 최적화 (1) - 캔버스와 리빌드 시스템 - soo:bak"
date: "2026-02-16 19:17:00 +0900"
description: Canvas 아키텍처, 메쉬 생성과 배칭, Layout Rebuild와 Visual Rebuild, 리빌드 트리거를 설명합니다.
tags:
  - Unity
  - 최적화
  - UI
  - Canvas
  - 모바일
---

## 화면에 항상 있는 UI의 비용

지금까지 시리즈에서는 게임 루프와 렌더링의 기초부터 스크립트와 메모리 관리까지, 게임 전반에 걸친 주제를 다루었습니다.

이제부터는 Unity 개별 서브시스템의 최적화 패턴을 다룹니다. 그 첫 번째가 **UI(User Interface)** 입니다.

UI를 가장 먼저 다루는 이유는, UI가 **게임플레이 내내 지속적으로 화면에 머무는 요소**이기 때문입니다.

3D 오브젝트는 카메라 밖으로 나가면 렌더링되지 않고, 파티클은 일시적으로만 존재합니다.

반면 체력바, 미니맵, 채팅창, 인벤토리 버튼 같은 UI 요소는 특별히 숨기지 않는 한 매 프레임 화면 위에 남아 있습니다.

화면에 떠 있는 동안 UI는 매 프레임 렌더링되므로, UI 시스템의 불필요한 연산은 작은 비용이라도 플레이 시간 내내 누적됩니다.

<br>

이 글에서는 Unity UI 시스템의 핵심인 **Canvas 아키텍처**와 **리빌드(Rebuild) 시스템**을 다룹니다.

Canvas가 UI 요소를 화면에 그려내는 과정을 따라가면서, 그 안에서 어떤 변경이 비용을 발생시키는지 살펴봅니다.

---

## Canvas의 역할

Canvas는 Unity UI 시스템에서 **모든 UI 요소의 컨테이너** 역할을 합니다. Button, Image, Text 같은 UI 컴포넌트는 Canvas의 자식 오브젝트로 있어야만 화면에 표시됩니다.

Canvas의 두 번째 역할은 **렌더링 준비**입니다. 화면에 표시되는 모든 UI는 결국 GPU가 그릴 수 있는 형태인 **메쉬(Mesh)** 로 변환되어야 하는데, 이 변환을 관리하는 것이 바로 Canvas입니다. 변환된 여러 UI 요소의 메쉬를 하나로 모아 GPU에 한꺼번에 제출하는 작업까지 함께 담당합니다.

UI에 어떤 변경이 생기면 이 변환과 제출 과정이 다시 수행될 수 있기 때문에, Canvas는 UI 성능의 출발점이 됩니다.
---

## UI 요소와 메쉬

[렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 3D 오브젝트가 정점과 삼각형으로 이루어진 메쉬로 표현된다고 설명했습니다.

UI 역시 같은 원리로 메쉬가 되는데, Image, Text, RawImage 같은 요소는 대부분 평면이므로 내부적으로는 **사각형 메쉬**의 형태를 띱니다.

<br>

하나의 UI Image는 정점 4개와 삼각형 2개로 구성된 사각형 메쉬가 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 340 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 340px; width: 100%;">
  <!-- Title -->
  <text x="170" y="20" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">UI Image의 내부 메쉬 구조</text>
  <!-- Quad background -->
  <rect x="70" y="40" width="140" height="120" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- Diagonal line (v0 to v3) -->
  <line x1="70" y1="40" x2="210" y2="160" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3" opacity="0.4"/>
  <!-- Triangle 1 shading (v0, v2, v1) - upper-left -->
  <polygon points="70,40 70,160 210,40" fill="currentColor" fill-opacity="0.04"/>
  <!-- Triangle 2 shading (v1, v2, v3) - lower-right -->
  <polygon points="210,40 70,160 210,160" fill="currentColor" fill-opacity="0.08"/>
  <!-- Vertex dots -->
  <circle cx="70" cy="40" r="4" fill="currentColor"/>
  <circle cx="210" cy="40" r="4" fill="currentColor"/>
  <circle cx="70" cy="160" r="4" fill="currentColor"/>
  <circle cx="210" cy="160" r="4" fill="currentColor"/>
  <!-- Vertex labels -->
  <text x="52" y="36" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">v0</text>
  <text x="228" y="36" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">v1</text>
  <text x="52" y="166" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">v2</text>
  <text x="228" y="166" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">v3</text>
  <!-- Triangle labels inside -->
  <text x="108" y="108" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">삼각형 1</text>
  <text x="178" y="128" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">삼각형 2</text>
  <!-- Info rows -->
  <text x="170" y="195" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.6">삼각형 1: v0, v2, v1</text>
  <text x="170" y="213" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" opacity="0.6">삼각형 2: v1, v2, v3</text>
  <!-- Summary -->
  <rect x="95" y="228" width="150" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="245" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">정점 4개, 삼각형 2개</text>
</svg>
</div>

<br>

Text는 글자 하나당 하나의 사각형 메쉬를 생성합니다. "Hello"라는 텍스트는 5개의 사각형, 즉 정점 20개와 삼각형 10개로 구성됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 400 195" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px; width: 100%;">
  <!-- Title -->
  <text x="200" y="20" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Text "Hello" 의 내부 메쉬 구조</text>
  <!-- Letter boxes -->
  <rect x="40" y="38" width="52" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="66" y="70" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" font-weight="bold">H</text>
  <rect x="104" y="38" width="52" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="70" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" font-weight="bold">e</text>
  <rect x="168" y="38" width="52" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="194" y="70" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" font-weight="bold">l</text>
  <rect x="232" y="38" width="52" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="258" y="70" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" font-weight="bold">l</text>
  <rect x="296" y="38" width="52" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="322" y="70" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" font-weight="bold">o</text>
  <!-- Per-letter annotation -->
  <text x="200" y="112" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">각 글자 = 사각형 1개 = 정점 4개, 삼각형 2개</text>
  <!-- Brace-like connector lines -->
  <line x1="40" y1="124" x2="348" y2="124" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="200" y1="124" x2="200" y2="134" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Summary box -->
  <rect x="80" y="140" width="240" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="200" y="159" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">"Hello" = 5글자</text>
  <text x="200" y="177" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">정점 20개, 삼각형 10개</text>
</svg>
</div>

<br>

화면에 보이는 실제 UI는 대부분 Image와 Text의 조합입니다. "확인" 버튼 하나만 해도 배경 Image의 정점 4개와 라벨 Text "확인"의 정점 8개(2글자 x 4)가 합쳐져, 총 정점 12개로 그려집니다.

UI가 조금만 복잡해져도 정점 수가 빠르게 불어납니다.

---

## Canvas의 메쉬 생성과 배칭

앞 섹션에서 본 것처럼, Canvas에 속한 각 UI 요소는 자신만의 메쉬를 가집니다. Canvas는 이 개별 메쉬들을 그대로 GPU에 보내지 않고, 일정 조건을 만족하는 요소끼리 **하나의 메쉬로 합친 뒤** 제출합니다.
이 과정이 **배칭(Batching)** 이며, 합쳐진 메쉬 하나가 하나의 드로우콜(Draw Call)로 처리되고, 그에 맞춰 **SetPass Call**의 발생 횟수도 함께 줄어듭니다.

**드로우콜**은 CPU가 GPU에 렌더링 명령을 보내는 횟수로, [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)에서 다루었듯이 값이 커질수록 CPU 부하도 같이 커집니다. **SetPass Call**은 머티리얼이나 셰이더 상태를 GPU에 설정하는 호출로, 머티리얼이 바뀔 때마다 발생합니다.

Canvas는 같은 머티리얼을 쓰는 UI 요소들을 하나의 메쉬로 묶어 두 호출의 수를 함께 줄입니다. 같은 머티리얼의 UI 요소가 100개일 때 하나씩 따로 그리면 드로우콜은 100회에 이르지만, 배칭이 적용되면 수 회 수준으로 내려갑니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <text x="340" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">배칭 전후 비교 (같은 머티리얼을 사용하는 경우)</text>
  <!-- Left: 배칭 전 -->
  <text x="165" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">배칭 전</text>
  <rect x="40" y="68" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image A</text>
  <line x1="140" y1="84" x2="192" y2="84" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="192,80 200,84 192,88" fill="currentColor"/>
  <rect x="200" y="68" width="110" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Draw Call 1</text>
  <rect x="40" y="112" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="133" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image B</text>
  <line x1="140" y1="128" x2="192" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="192,124 200,128 192,132" fill="currentColor"/>
  <rect x="200" y="112" width="110" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="133" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Draw Call 2</text>
  <rect x="40" y="156" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="177" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image C</text>
  <line x1="140" y1="172" x2="192" y2="172" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="192,168 200,172 192,176" fill="currentColor"/>
  <rect x="200" y="156" width="110" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="177" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Draw Call 3</text>
  <text x="165" y="214" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">요소 수만큼 드로우콜 발생</text>
  <!-- Divider -->
  <line x1="340" y1="58" x2="340" y2="220" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- Right: 배칭 후 -->
  <text x="510" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">배칭 후</text>
  <rect x="380" y="80" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="101" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image A</text>
  <rect x="380" y="120" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="141" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image B</text>
  <rect x="380" y="160" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="181" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image C</text>
  <line x1="480" y1="96" x2="510" y2="136" stroke="currentColor" stroke-width="1.5"/>
  <line x1="480" y1="136" x2="510" y2="136" stroke="currentColor" stroke-width="1.5"/>
  <line x1="480" y1="176" x2="510" y2="136" stroke="currentColor" stroke-width="1.5"/>
  <line x1="510" y1="136" x2="528" y2="136" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="528,132 536,136 528,140" fill="currentColor"/>
  <rect x="536" y="116" width="90" height="40" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="581" y="133" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">합쳐진 메쉬</text>
  <text x="581" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">Draw Call 1</text>
  <text x="510" y="214" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.55">같은 머티리얼의 요소가 하나의 배치로 합쳐짐</text>
  <!-- Bottom summary -->
  <rect x="190" y="238" width="300" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="340" y="257" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">드로우콜 3회 → 1회로 감소</text>
</svg>
</div>

<br>

Canvas의 배칭은 네 단계를 거쳐 이루어집니다. 먼저 모든 UI 요소의 메쉬 데이터(정점, UV, 색상)를 수집하고, 같은 머티리얼을 쓰는 요소끼리 그룹으로 분류합니다.

그 다음 각 그룹의 메쉬를 하나의 연속된 버퍼로 합친 뒤, 그 버퍼를 GPU에 제출합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Canvas의 메쉬 배칭 과정</text>
  <!-- Column headers -->
  <text x="68" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">UI 요소</text>
  <text x="320" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">Canvas 내부 처리</text>
  <text x="575" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">GPU</text>
  <!-- UI Elements -->
  <rect x="20" y="65" width="96" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="84" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image</text>
  <rect x="20" y="100" width="96" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="119" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Image</text>
  <rect x="20" y="135" width="96" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="154" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Text</text>
  <rect x="20" y="170" width="96" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="68" y="189" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">Button</text>
  <!-- Merge lines from UI elements to processing -->
  <line x1="116" y1="79" x2="145" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="116" y1="114" x2="145" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="116" y1="149" x2="145" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="116" y1="184" x2="145" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="145" y1="130" x2="163" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="163,126 171,130 163,134" fill="currentColor"/>
  <!-- Processing steps -->
  <rect x="175" y="68" width="280" height="130" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="185" y="90" fill="currentColor" font-family="sans-serif" font-size="10">1. 메쉬 데이터 수집 (정점, UV, 색상)</text>
  <text x="185" y="112" fill="currentColor" font-family="sans-serif" font-size="10">2. 배칭 규칙에 따라 그룹 분류</text>
  <text x="185" y="134" fill="currentColor" font-family="sans-serif" font-size="10">3. 그룹별 메쉬를 하나의 버퍼로 합침</text>
  <text x="185" y="156" fill="currentColor" font-family="sans-serif" font-size="10">4. GPU에 제출</text>
  <text x="315" y="185" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">CPU에서 수행</text>
  <!-- Arrow to GPU -->
  <line x1="455" y1="130" x2="503" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="503,126 511,130 503,134" fill="currentColor"/>
  <!-- GPU box -->
  <rect x="515" y="100" width="120" height="60" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="575" y="126" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">합쳐진 메쉬</text>
  <text x="575" y="146" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">버퍼를 렌더링</text>
</svg>
</div>

<br>

이 전체 과정은 **CPU에서 수행**됩니다.

GPU는 이미 합쳐진 최종 메쉬를 받아서 렌더링만 하고, 메쉬를 수집하고 분류하고 합치는 모든 연산은 CPU의 몫입니다.

---

## 리빌드(Rebuild)란

Canvas가 한 번 배칭을 완료하고 GPU에 메쉬를 제출한 뒤, UI에 아무런 변경이 없는 동안에는 추가 작업이 발생하지 않습니다. GPU가 이미 받은 메쉬를 그대로 계속 렌더링하므로, CPU는 다른 작업에 자원을 쓸 수 있습니다.

그러나 Canvas 안의 UI 요소가 **하나라도 바뀌면**, 바뀐 내용을 반영하기 위해 메쉬를 재생성하고 배칭을 다시 실행해야 합니다.

이 재처리 과정이 **리빌드(Rebuild)** 입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">리빌드 발생 흐름</text>
  <!-- Frame N row -->
  <rect x="20" y="45" width="90" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">프레임 N</text>
  <line x1="110" y1="63" x2="142" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="142,59 150,63 142,67" fill="currentColor"/>
  <rect x="154" y="45" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="219" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">UI 변경 없음</text>
  <line x1="284" y1="63" x2="316" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="316,59 324,63 316,67" fill="currentColor"/>
  <rect x="328" y="45" width="150" height="36" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="403" y="62" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">이전 메쉬 유지</text>
  <text x="403" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.55">CPU 비용 0</text>
  <!-- Frame N+1 row -->
  <rect x="20" y="110" width="90" height="36" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="133" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">프레임 N+1</text>
  <line x1="110" y1="128" x2="142" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="142,124 150,128 142,132" fill="currentColor"/>
  <rect x="154" y="110" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="219" y="126" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">Text 변경</text>
  <text x="219" y="140" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">"100" → "99"</text>
  <!-- Rebuild chain -->
  <line x1="284" y1="128" x2="296" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="296,124 304,128 296,132" fill="currentColor"/>
  <rect x="308" y="110" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="348" y="132" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">변경 감지</text>
  <line x1="388" y1="128" x2="400" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="400,124 408,128 400,132" fill="currentColor"/>
  <rect x="412" y="110" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="452" y="132" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">메쉬 재생성</text>
  <line x1="492" y1="128" x2="504" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="504,124 512,128 504,132" fill="currentColor"/>
  <rect x="516" y="110" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="556" y="132" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">배칭 재실행</text>
  <!-- Arrow down to GPU resubmit -->
  <line x1="556" y1="146" x2="556" y2="168" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="552,168 556,176 560,168" fill="currentColor"/>
  <rect x="476" y="180" width="160" height="36" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="556" y="196" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">GPU 재제출</text>
  <text x="556" y="210" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">CPU 비용 발생</text>
</svg>
</div>

<br>

리빌드는 **Canvas 단위**로 일어납니다. Canvas 안에 UI 요소가 100개 있고 그중 1개만 바뀌어도, 변경되지 않은 99개까지 포함한 100개 전체의 메쉬가 다시 수집되고 배칭됩니다.

Canvas에 포함된 요소가 많을수록 리빌드 비용도 함께 커집니다. UI 요소 하나의 변경이 Canvas 전체의 CPU 비용을 유발한다는 점이 UI 성능 문제의 핵심입니다.

---

## 리빌드를 유발하는 변경들

Canvas의 리빌드를 유발하는 변경은 크게 두 종류로 나뉩니다.

UI 요소의 **크기와 위치를 재계산해야 하는 변경**과 UI 요소의 **시각 표현만 갱신하면 되는 변경**이 그것이며, Unity의 Canvas UI 시스템 내부에서는 이 두 종류를 각각 **Layout Rebuild**와 **Visual Rebuild(Graphic Rebuild)** 로 구분합니다.

<br>

Visual Rebuild는 텍스트 내용 교체, 이미지 스프라이트 변경, Color 프로퍼티 변경처럼 배치는 그대로 둔 채 메쉬의 시각 정보만 갱신하면 되는 경우에 일어납니다.

한편 Layout Rebuild는 RectTransform의 크기 변경처럼 요소 자체의 배치가 달라지는 경우에 트리거됩니다.

두 리빌드가 함께 일어나는 경우도 있는데, `SetActive`로 요소를 켜거나 끄는 경우, `SetSiblingIndex`로 Hierarchy 순서를 바꾸는 경우, Canvas 내 UI 요소(Image, Button, Text 등)를 `Instantiate`로 새로 생성하거나 `Destroy`로 제거하는 경우가 여기에 해당합니다.

<br>

앞에서 나열한 변경들은 UI에서 흔히 수행하는 거의 모든 조작에 해당합니다.

체력바의 숫자가 바뀌는 것, 아이템 아이콘이 교체되는 것, 버프 효과로 아이콘 색상이 변하는 것 모두 Canvas 리빌드의 트리거입니다.

---

## Canvas의 Layout Rebuild

Canvas의 Layout Rebuild는 UI 요소의 **크기와 위치를 재계산**하는 과정이며, RectTransform 크기(Width, Height) 변경, UI 요소의 활성화/비활성화, Hierarchy 순서 변경, Canvas 내 UI 요소의 생성·제거 등이 이를 유발합니다.

<br>

이 재계산은 각 UI 요소의 **RectTransform**을 대상으로 이뤄집니다.

RectTransform은 모든 UI 요소가 갖는 Transform 컴포넌트로, 위치·크기·앵커 정보를 담고 있습니다. 스크립트가 `sizeDelta`·`anchoredPosition` 같은 RectTransform 속성을 변경하거나 요소를 활성화·생성·제거하면, 해당 RectTransform에 "갱신이 필요하다"는 **dirty flag**가 설정되고 **CanvasUpdateRegistry**에 등록됩니다.

프레임 끝의 Layout 업데이트 시점에 등록된 dirty RectTransform들만 한꺼번에 재계산되어 새 크기와 위치가 RectTransform에 반영되고, 계산이 끝나면 dirty flag가 해제됩니다.

이렇게 dirty flag로 변경된 요소만 선별하는 방식 덕분에, Unity는 매 프레임 모든 UI 요소를 다시 계산하는 부담 없이 변경이 없는 요소는 그대로 두어 CPU 비용을 아낄 수 있습니다.

<br>

**LayoutGroup**(HorizontalLayoutGroup, VerticalLayoutGroup, GridLayoutGroup)처럼 자식을 자동으로 배치하는 컴포넌트가 붙어 있으면, 그 내부에서 배치 규칙을 재적용하는 추가 재계산이 일어납니다.

이 내부 재계산은 Canvas의 Layout Rebuild와는 구분되는 LayoutGroup 고유의 과정이라 본 글에서는 다루지 않으며, LayoutGroup의 재계산 흐름은 [Unity의 Layout Update Cycle](/dev/unity/UnityLayoutUpdateCycle/)에서 다룹니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Layout Rebuild 의 dirty flag 흐름</text>
  <rect x="30" y="42" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="95" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">sizeDelta 변경</text>
  <line x1="160" y1="60" x2="192" y2="60" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="192,56 200,60 192,64" fill="currentColor"/>
  <rect x="200" y="42" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">dirty flag 설정</text>
  <line x1="320" y1="60" x2="352" y2="60" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="352,56 360,60 352,64" fill="currentColor"/>
  <rect x="360" y="42" width="140" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CanvasUpdateRegistry</text>
  <text x="430" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">에 등록</text>
  <line x1="430" y1="78" x2="430" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="426,120 430,128 434,120" fill="currentColor"/>
  <rect x="340" y="128" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="150" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임 끝, Layout 업데이트 시점</text>
  <line x1="430" y1="164" x2="430" y2="196" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="426,196 430,204 434,196" fill="currentColor"/>
  <rect x="310" y="204" width="160" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="226" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">dirty 요소만 크기/위치 재계산</text>
  <line x1="310" y1="222" x2="278" y2="222" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="278,218 270,222 278,226" fill="currentColor"/>
  <rect x="140" y="204" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="205" y="226" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">dirty flag 해제</text>
</svg>
</div>

---

## Canvas의 Visual Rebuild (Graphic Rebuild)

Canvas의 Visual Rebuild는 UI 요소의 **시각적 표현을 구성하는 메쉬 데이터를 재생성**하는 과정입니다.

이 단계에서는 UI 요소가 실제로 어떤 색·글자·그림으로 보일지를 메쉬에 기록합니다.

<br>

메쉬 데이터 중 어느 부분을 다시 써야 하는지는 어떤 프로퍼티가 바뀌었는지에 따라 달라집니다.

예를 들어 색상(Color 프로퍼티)이 바뀌면 메쉬에 기록된 정점 색상(Vertex Color) 값만 갱신하면 되고, 스프라이트가 교체되면 새 아틀라스 내 위치가 다르므로 UV 좌표를 다시 계산해야 합니다.

텍스트 내용이 `"100"`에서 `"99"`로 바뀌면 글자 수·배치·UV가 전부 달라져 메쉬 자체를 새로 만들어야 하며, Image.Filled 타입의 `fillAmount`가 바뀌는 경우에도 채워진 영역의 정점이 달라지므로 메쉬 형태를 다시 생성해야 합니다.

<br>

| 변경 | 재생성이 필요한 데이터 |
|---|---|
| 색상 변경 (Color 프로퍼티 변경) | 정점 색상 (Vertex Color) |
| 텍스트 내용 변경 ("100" → "99") | 전체 메쉬 재생성 (글자 수, 글자 배치, UV 모두 변경) |
| 스프라이트 교체 (sprite 프로퍼티 변경) | UV 좌표 재계산 (아틀라스 내 위치가 다르므로) |
| fillAmount 변경 (Image.Filled 타입) | 메쉬 형태 재생성 (채워진 영역의 정점 재계산) |

<br>

네 가지 변경 중 Visual Rebuild 비용이 가장 큰 것은 **텍스트 재생성**입니다.

색상·스프라이트·fillAmount는 기존 메쉬의 특정 데이터만 고쳐 쓰면 되지만, 텍스트는 내용이 조금만 바뀌어도 글자 수·배치·UV 좌표가 함께 달라지기 때문에 메쉬 전체를 다시 만들어야 합니다.

메쉬를 다시 만들 때는 먼저 텍스트 전체의 커닝(글자 간격)·줄바꿈·정렬을 계산해 각 글자가 놓일 위치를 정한 뒤, 폰트 텍스처에 미리 저장된 각 글자의 픽셀 이미지(이를 **글리프(Glyph)** 라고 합니다)를 가져와 UV 좌표를 메쉬 데이터에 기록합니다.

결국 텍스트 메쉬 생성은 필요한 글리프를 모아 배치하는 작업이므로, 글리프가 미리 준비되어 있느냐 필요할 때마다 새로 만들어야 하느냐에 따라 텍스트 재생성 비용이 달라집니다.

<br>

영어처럼 글자 집합이 작은 언어는 준비 과정이 단순합니다.

대소문자·숫자·기호를 모두 합쳐도 약 100자 수준이므로, 빌드 시점에 모든 글리프를 하나의 폰트 텍스처에 미리 렌더링해두면 런타임에는 텍스처에서 해당 글자의 UV 좌표만 조회해 사용할 수 있습니다.

반면 한글은 조합 가능한 음절이 11,172자(가~힣)에 이르기 때문에 모두 미리 렌더링해 폰트 텍스처에 담아두기 어렵습니다.

그래서 Unity는 한글을 **동적 폰트(Dynamic Font)**, 즉 필요한 글리프를 런타임에 생성하는 방식으로 처리하는 경우가 많습니다.

<br>

런타임 생성이 가능한 이유는 폰트 파일이 픽셀 이미지가 아니기 때문입니다.

`.ttf`나 `.otf` 파일에는 각 글자가 획의 경계선을 점과 곡선 좌표로 표현한 **윤곽선 데이터**로 저장되어 있어, 글자를 어떤 크기로도 선명하게 표시할 수 있습니다.

다만 화면이나 텍스처는 결국 픽셀 격자이기 때문에, 윤곽선처럼 벡터 형태로 저장된 데이터를 표시 크기에 맞춰 비트맵으로 옮기는 변환 과정이 필요합니다.

이 변환을 **래스터라이즈**라고 부르며, 폰트에서는 윤곽선을 해당 크기의 글자 비트맵으로 만드는 과정이 이에 해당합니다.

<br>

동적 폰트는 텍스트에 새 글자가 등장하면 그 글자의 윤곽선을 래스터라이즈해 글리프를 만들어 **폰트 텍스처 아틀라스**에 추가합니다.

한 번 아틀라스에 들어간 글리프는 그대로 남기 때문에, 같은 글자가 다시 등장하면 추가 비용 없이 재사용됩니다.

다만 아틀라스의 크기는 유한해서, 새 글자가 계속 등장해 빈 공간이 부족해지면 Unity는 더 큰 텍스처를 새로 만들고 기존 글리프를 전부 다시 배치해야 합니다. 이 재배치는 아틀라스 전체를 다시 구성하는 작업이므로, 글리프 하나를 추가할 때보다 비용이 큽니다.

데미지 숫자·점수 표시·채팅 메시지처럼 내용이 매 프레임 바뀌는 UI에서는 Visual Rebuild가 매번 일어나고, 거기에 추가로 드는 비용은 글자와 아틀라스 상태에 따라 달라집니다.

표시할 글자가 모두 아틀라스에 있다면 Visual Rebuild만 일어나고, 아틀라스에 없는 새 글자가 포함되면 그 글자를 래스터라이즈해 아틀라스에 추가하는 비용이 더해지며, 새 글자가 누적되어 아틀라스 용량을 넘어서면 아틀라스 전체를 다시 구성하는 재배치 비용까지 추가됩니다.

---

## Layout Rebuild와 Visual Rebuild의 실행 순서

Layout Rebuild와 Visual Rebuild가 모두 필요한 프레임에서, 두 리빌드는 **Layout Rebuild가 먼저, Visual Rebuild가 나중에** 실행됩니다.

이는 Visual Rebuild가 메쉬를 생성할 때 해당 요소의 최종 크기와 위치가 확정되어 있어야 하기 때문입니다.

예를 들어 Text는 텍스트 영역의 너비를 알아야 줄바꿈을 결정할 수 있고, Image는 이미지의 크기를 알아야 정점 좌표를 계산할 수 있습니다.

따라서 Layout Rebuild가 크기와 위치를 먼저 확정하고, Visual Rebuild가 이 정보를 기반으로 메쉬를 생성합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">리빌드 실행 순서</text>
  <text x="260" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(프레임의 Late Update 이후, 렌더링 직전)</text>

  <!-- Step 1: Layout Rebuild -->
  <rect x="30" y="55" width="460" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="75" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1. Layout Rebuild</text>
  <text x="50" y="93" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">dirty 요소의 크기/위치 재계산 → RectTransform 확정</text>

  <!-- Arrow 1→2 -->
  <line x1="260" y1="105" x2="260" y2="125" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,122 260,132 266,122" fill="currentColor"/>

  <!-- Step 2: Visual Rebuild -->
  <rect x="30" y="135" width="460" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="155" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2. Visual Rebuild</text>
  <text x="50" y="173" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">확정된 크기를 기반으로 메쉬/색상/UV 재생성 → 메쉬 데이터 확정</text>

  <!-- Arrow 2→3 -->
  <line x1="260" y1="185" x2="260" y2="205" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,202 260,212 266,202" fill="currentColor"/>

  <!-- Step 3: Canvas 배칭 -->
  <rect x="30" y="215" width="460" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="235" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3. Canvas 배칭</text>
  <text x="50" y="253" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">모든 요소의 메쉬를 수집하여 배칭 규칙에 따라 합침 → 최종 메쉬 확정</text>

  <!-- Arrow 3→GPU -->
  <line x1="260" y1="265" x2="260" y2="285" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,282 260,292 266,282" fill="currentColor"/>

  <!-- GPU 렌더링 -->
  <rect x="170" y="295" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="318" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU 렌더링</text>
</svg>
</div>

---

## Canvas 단위 리빌드의 비용

Canvas의 리빌드 비용은 그 안에 포함된 UI 요소 수에 비례합니다.

이는 Canvas가 속한 **모든 UI 요소를 함께 배칭**하기 때문입니다. 요소 하나만 바뀌어도 배치 그룹 분류나 정점 오프셋이 달라져, 모든 요소가 다시 배칭됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Canvas 단위 재배칭의 범위</text>
  <text x="270" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(Canvas에 UI 요소 100개 포함)</text>

  <!-- Trigger label -->
  <text x="30" y="65" font-family="sans-serif" font-size="11" fill="currentColor">요소 2의 Text 변경 ("100" → "99")</text>
  <text x="30" y="81" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 요소 2: 메쉬 재생성 (Visual Rebuild)</text>

  <!-- Canvas container -->
  <rect x="30" y="100" width="480" height="250" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="50" y="120" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Canvas</text>

  <!-- 요소 1 (unchanged) -->
  <rect x="55" y="132" width="310" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="70" y="151" font-family="sans-serif" font-size="11" fill="currentColor">요소 1</text>
  <text x="375" y="151" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">변경 없음, 하지만 메쉬 재수집</text>

  <!-- 요소 2 (changed - highlighted) -->
  <rect x="55" y="170" width="310" height="30" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="189" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">요소 2</text>
  <text x="375" y="189" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.8">메쉬 재생성됨</text>

  <!-- 요소 3 (unchanged) -->
  <rect x="55" y="208" width="310" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="70" y="227" font-family="sans-serif" font-size="11" fill="currentColor">요소 3</text>
  <text x="375" y="227" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">변경 없음, 하지만 메쉬 재수집</text>

  <!-- Ellipsis -->
  <text x="210" y="256" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor" opacity="0.5">···</text>

  <!-- 요소 100 (unchanged) -->
  <rect x="55" y="268" width="310" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="70" y="287" font-family="sans-serif" font-size="11" fill="currentColor">요소 100</text>
  <text x="375" y="287" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">변경 없음, 하지만 메쉬 재수집</text>

  <!-- Arrow to rebatching -->
  <line x1="270" y1="350" x2="270" y2="370" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,367 270,377 276,367" fill="currentColor"/>

  <!-- Rebatching result -->
  <rect x="130" y="380" width="280" height="32" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="401" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">100개 요소 전체를 다시 배칭</text>
</svg>
</div>

<br>

다이어그램처럼 요소 2 하나만 변경되어도 **100개 요소 전체가 재배칭됩니다**. Canvas는 변경의 영향 범위를 요소별로 추적하지 않기 때문입니다.

---

## Canvas의 배칭 규칙

Canvas 리빌드의 비용은 요소 수에 비례하는데, 리빌드 결과 GPU에 제출되는 드로우콜의 수는 Canvas의 배칭이 얼마나 이루어지느냐에 달려 있습니다.

Canvas 배칭이 가능하려면 같은 머티리얼을 사용하면서 Hierarchy 순서상 연속해야 합니다. 이 조건을 충족하지 못하면 배치가 나뉘어 드로우콜이 늘어납니다.
<br>

### 같은 머티리얼

Canvas 배칭은 **같은 머티리얼(Material)을 사용하는 요소끼리만** 합칠 수 있습니다.

하나의 드로우콜은 하나의 렌더링 상태(셰이더 + 텍스처 조합)로 처리되므로, 머티리얼이 다르면 별도의 드로우콜로 나뉩니다.

다만 Unity UI에서는 대부분의 요소가 기본 UI 셰이더를 공유하므로, 배칭 가능 여부는 실질적으로 **같은 텍스처를 사용하는지**에 따라 결정됩니다.

즉, 서로 다른 스프라이트라도 **같은 텍스처 아틀라스(Sprite Atlas)** 에 속해 있으면 하나의 텍스처를 공유하므로 같은 배치로 합쳐질 수 있습니다.

아틀라스로 묶지 않은 스프라이트는 각각 별도의 텍스처이므로 배칭되지 않으며, Text 요소 역시 폰트 텍스처를 사용하므로 Image 요소와는 같은 배치로 합쳐지지 않습니다.

### Hierarchy 순서와 깊이

같은 머티리얼을 사용하더라도, 요소들이 렌더링 순서상 연속해 있어야 하나의 배치로 합쳐질 수 있습니다.

Unity UI는 Hierarchy를 **깊이 우선(depth-first)** 으로 순회하여 기본 렌더링 순서를 결정합니다.

부모가 먼저 그려지고 자식들이 순서대로 그려진 뒤 다음 형제로 넘어가므로, **Hierarchy 순서가 렌더링 순서의 기준**이 됩니다.

예를 들어 같은 머티리얼의 요소 A와 C 사이에 다른 머티리얼의 요소 B가 있고, 이 요소들이 **화면상에서 겹치면** 렌더링 순서를 바꿀 수 없으므로 A와 C는 별도의 배치로 나뉘는데, 이 현상을 **배치 브레이킹(Batch Breaking)**이라고 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <!-- Title -->
  <text x="360" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">배치 브레이킹 예시 (A, B, C가 화면상에서 겹치는 경우)</text>

  <!-- LEFT: 조정 전 -->
  <text x="175" y="52" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">조정 전</text>
  <text x="175" y="68" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Hierarchy 순서 (위→아래)</text>

  <!-- Image A (아틀라스 1) -->
  <rect x="30" y="82" width="170" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="115" y="103" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Image A (아틀라스 1)</text>
  <!-- Arrow A → 배치 1 -->
  <line x1="200" y1="100" x2="248" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="255,100 248,96 248,104" fill="currentColor"/>
  <!-- 배치 1 -->
  <rect x="258" y="82" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="298" y="103" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">배치 1</text>

  <!-- Image B (아틀라스 2) -->
  <rect x="30" y="132" width="170" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="115" y="153" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Image B (아틀라스 2)</text>
  <!-- Arrow B → 배치 2 -->
  <line x1="200" y1="150" x2="248" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="255,150 248,146 248,154" fill="currentColor"/>
  <!-- 배치 2 -->
  <rect x="258" y="132" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="298" y="153" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">배치 2</text>
  <text x="298" y="183" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">다른 머티리얼</text>

  <!-- Image C (아틀라스 1) -->
  <rect x="30" y="196" width="170" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="115" y="217" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Image C (아틀라스 1)</text>
  <!-- Arrow C → 배치 3 -->
  <line x1="200" y1="214" x2="248" y2="214" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="255,214 248,210 248,218" fill="currentColor"/>
  <!-- 배치 3 -->
  <rect x="258" y="196" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="298" y="217" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">배치 3</text>
  <text x="298" y="247" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">A와 같지만 B가 중간에 끼어 분리</text>

  <!-- 드로우콜 3회 -->
  <text x="175" y="278" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">→ 드로우콜 3회</text>

  <!-- Divider -->
  <line x1="360" y1="50" x2="360" y2="290" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.3"/>

  <!-- RIGHT: 조정 후 -->
  <text x="545" y="52" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">조정 후</text>
  <text x="545" y="68" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Hierarchy 순서 재배치</text>

  <!-- Image A (아틀라스 1) -->
  <rect x="400" y="90" width="170" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="485" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Image A (아틀라스 1)</text>
  <!-- Image C (아틀라스 1) -->
  <rect x="400" y="132" width="170" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="485" y="153" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Image C (아틀라스 1)</text>

  <!-- Bracket from A+C -->
  <line x1="570" y1="108" x2="590" y2="108" stroke="currentColor" stroke-width="1.5"/>
  <line x1="570" y1="150" x2="590" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <line x1="590" y1="108" x2="590" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <line x1="590" y1="129" x2="618" y2="129" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="625,129 618,125 618,133" fill="currentColor"/>
  <!-- 배치 1 -->
  <rect x="628" y="111" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="668" y="132" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">배치 1</text>
  <text x="668" y="162" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">같은 머티리얼, 연속</text>

  <!-- Image B (아틀라스 2) -->
  <rect x="400" y="182" width="170" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="485" y="203" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Image B (아틀라스 2)</text>
  <!-- Arrow B → 배치 2 -->
  <line x1="570" y1="200" x2="618" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="625,200 618,196 618,204" fill="currentColor"/>
  <!-- 배치 2 -->
  <rect x="628" y="182" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="668" y="203" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">배치 2</text>

  <!-- 드로우콜 2회 -->
  <text x="545" y="278" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">→ 드로우콜 2회</text>

  <!-- Legend -->
  <rect x="200" y="305" width="16" height="12" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="222" y="315" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">아틀라스 1 (실선)</text>
  <rect x="340" y="305" width="16" height="12" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="362" y="315" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">아틀라스 2 (점선)</text>
</svg>
</div>

<br>

다이어그램처럼 A와 C를 Hierarchy에서 연속으로 배치하면 같은 배치로 합쳐져 드로우콜이 3회에서 2회로 줄어듭니다.

다만 실제 UI에서는 수십 개의 요소가 복잡하게 겹치므로 배치 브레이킹이 빈번하게 발생합니다.

### 화면상의 겹침(Overlap)

배치 브레이킹의 핵심 조건은 **화면상의 겹침**입니다.

화면에서 서로 겹치지 않는 요소끼리는 Hierarchy 순서를 바꿔도 시각적 결과가 같습니다. 그래서 다른 머티리얼의 요소가 사이에 있더라도, Unity는 순서를 재배치해 배칭할 수 있고 배치 브레이킹은 발생하지 않습니다.

반면 화면상에서 겹치는 요소는 앞뒤 관계가 시각적 결과를 결정하므로, Hierarchy 순서대로 그려야 합니다. 따라서 다른 머티리얼의 요소가 사이에 있으면, Unity는 그 순서를 따르기 위해 배치를 나눕니다.

---

## 리빌드 비용의 구성

Canvas의 리빌드 비용은 세 단계로 구성됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Canvas 리빌드의 CPU 비용 구성</text>

  <!-- Phase 1: Layout Rebuild -->
  <rect x="40" y="44" width="400" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="64" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1. Layout Rebuild</text>
  <text x="60" y="84" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">dirty flag가 설정된 요소의 크기/위치 재계산</text>
  <text x="60" y="104" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">LayoutGroup 내부라면 그룹 전체 재계산</text>

  <!-- Arrow 1→2 -->
  <line x1="240" y1="120" x2="240" y2="142" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="234,139 240,149 246,139" fill="currentColor"/>

  <!-- Phase 2: Visual Rebuild -->
  <rect x="40" y="152" width="400" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="172" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2. Visual Rebuild</text>
  <text x="60" y="192" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">변경된 요소의 메쉬/색상/UV 재생성</text>
  <text x="60" y="212" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">텍스트 재생성이 가장 비용이 큼</text>

  <!-- Arrow 2→3 -->
  <line x1="240" y1="228" x2="240" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="234,247 240,257 246,247" fill="currentColor"/>

  <!-- Phase 3: Canvas 재배칭 -->
  <rect x="40" y="260" width="400" height="92" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="280" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3. Canvas 재배칭</text>
  <text x="60" y="300" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Canvas 내 모든 요소의 메쉬를 재수집</text>
  <text x="60" y="318" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">배칭 규칙에 따라 다시 그룹화</text>
  <text x="60" y="336" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU에 재제출</text>

  <!-- Bottom formula -->
  <rect x="80" y="376" width="320" height="32" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="397" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">비용 ∝ Canvas 내 요소 수 × 변경 빈도</text>
</svg>
</div>

<br>

Canvas의 리빌드 비용은 **Canvas 내 요소의 수**와 **변경 빈도**가 결정합니다.

요소가 많은 Canvas에서 매 프레임 변경이 일어나면 두 요인이 함께 커지므로, UI 프레임 저하의 흔한 원인이 됩니다.

---

## 마무리

- UI 요소(Image, Text 등)는 내부적으로 사각형 메쉬(정점 4개, 삼각형 2개)로 표현되며, Canvas는 이 메쉬들을 배칭하여 GPU에 제출합니다.
- Canvas 내 UI 요소 하나라도 변경되면, 해당 요소의 Layout Rebuild(크기/위치)와 Visual Rebuild(메쉬/색상/UV) 이후 Canvas 전체의 재배칭이 발생합니다.
- 배칭은 같은 텍스처를 사용하고 렌더링 순서상 연속해 있는 요소끼리 동작하며, 겹치는 요소 사이에 머티리얼이 다른 요소가 있으면 배치가 나뉘어 드로우콜이 증가합니다.
- 리빌드 비용은 Canvas 내 요소 수와 변경 빈도에 비례합니다.

UI 변경이 발생하는 프레임마다 이 비용이 반복되므로, Canvas의 리빌드 구조를 이해하는 것이 UI 최적화의 출발점입니다.

<br>

이 글에서는 Canvas가 UI를 어떻게 그리는지, 어떤 변경이 비용을 발생시키는지 정리했습니다.

[Part 2](/dev/unity/UIOptimization-2/)에서는 Canvas 분리 전략, ScrollRect 풀링, TextMeshPro 활용, 오버드로우 최소화 등 실전에서 적용할 수 있는 UI 최적화 기법을 다룹니다.

<br>

---

**관련 글**
- [Unity의 Layout Update Cycle](/dev/unity/UnityLayoutUpdateCycle/)

**시리즈**
- **UI 최적화 (1) - 캔버스와 리빌드 시스템** (현재 글)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)

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
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- [메모리 관리 (2) - 네이티브 메모리와 에셋](/dev/unity/MemoryManagement-2/)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)
- **UI 최적화 (1) - 캔버스와 리빌드 시스템** (현재 글)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
