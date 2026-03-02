---
layout: single
title: "래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지 - soo:bak"
date: "2026-03-02 16:03:00 +0900"
description: 래스터화의 원리, 삼각형 내부 판별, 무게중심 좌표, 보간, 2x2 Quad 실행을 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 래스터화
  - 프래그먼트
  - 모바일
---

[그래픽스 수학 (3)](/dev/unity/GraphicsMath-3/)에서 3D 정점이 여러 좌표 공간을 거쳐 2D 화면 좌표로 변환되는 과정을 다루었습니다. 버텍스 셰이더가 정점의 좌표를 클립 공간으로 변환하고, GPU가 원근 나눗셈과 뷰포트 변환을 수행하면, 삼각형의 세 꼭짓점은 화면 위의 2D 좌표를 갖게 됩니다.

이 시점에서 파이프라인에 존재하는 데이터는 삼각형의 세 꼭짓점 좌표와, 각 꼭짓점에 정의된 색상, UV 좌표, 법선 벡터 등의 속성뿐입니다. 화면에는 아직 아무것도 그려지지 않았습니다.

<br>

그런데 화면은 연속적인 좌표 평면이 아니라 **이산적인 픽셀 격자**입니다.

세 꼭짓점의 좌표만으로는 화면에 무엇을 그릴 수 없습니다.

**래스터화(Rasterization)**는 삼각형이 덮는 영역의 각 픽셀이 삼각형 내부인지 판별하고, 내부라면 정점의 속성(색상, UV, 법선 등)을 그 위치에 맞게 보간하여 픽셀별 처리 데이터인 **프래그먼트**를 생성합니다.

래스터화는 GPU의 고정 기능 하드웨어가 수행하므로 셰이더 코드로 직접 제어할 수 없습니다. 그러나 래스터화가 생성하는 프래그먼트의 수와 분포가 이후 프래그먼트 셰이더의 실행 횟수와 깊이 테스트의 부하를 결정하므로, 래스터화의 원리를 이해하는 것은 렌더링 성능을 파악하는 출발점이 됩니다.

이 글에서는 삼각형 내부 판별, 프래그먼트와 픽셀의 차이, 정점 속성의 보간, 그리고 GPU의 프래그먼트 처리 최소 단위인 2x2 Quad까지 하나의 흐름으로 다룹니다.

---

## 래스터화란

래스터화는 **연속적인 기하 도형(삼각형)을 픽셀 단위의 프래그먼트로 변환하는 과정**입니다.

"래스터(raster)"는 수평 주사선의 격자를 뜻하는 단어로, **CRT(Cathode Ray Tube)** 모니터 시절부터 화면을 격자 형태의 점으로 구성한 데서 유래합니다.

<br>

래스터화는 렌더링 파이프라인의 중간에 위치합니다.

버텍스 셰이더가 정점 단위로 처리하는 기하 단계와, 프래그먼트 셰이더가 픽셀 단위로 처리하는 픽셀 단계를 연결합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 560" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더링 파이프라인에서 래스터화의 위치</text>
  <!-- 정점 데이터 입력 -->
  <rect x="120" y="40" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="63" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">정점 데이터 입력</text>
  <!-- Arrow -->
  <line x1="210" y1="76" x2="210" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,106 205,96 215,96" fill="currentColor"/>
  <!-- 버텍스 셰이더 -->
  <rect x="120" y="108" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="131" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">버텍스 셰이더</text>
  <text x="320" y="131" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">각 정점의 좌표 변환 (MVP)</text>
  <!-- Arrow -->
  <line x1="210" y1="144" x2="210" y2="168" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,174 205,164 215,164" fill="currentColor"/>
  <!-- 프리미티브 조립 -->
  <rect x="120" y="176" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="199" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프리미티브 조립</text>
  <text x="320" y="199" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">정점을 삼각형으로 조립, 클리핑</text>
  <!-- Arrow -->
  <line x1="210" y1="212" x2="210" y2="236" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,242 205,232 215,232" fill="currentColor"/>
  <!-- 래스터화 (highlighted) -->
  <rect x="110" y="244" width="200" height="44" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2.5"/>
  <text x="210" y="271" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">래스터화</text>
  <text x="330" y="262" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">삼각형 → 프래그먼트 변환</text>
  <text x="330" y="276" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">[이 글의 범위]</text>
  <!-- Arrow -->
  <line x1="210" y1="288" x2="210" y2="312" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,318 205,308 215,308" fill="currentColor"/>
  <!-- 프래그먼트 셰이더 -->
  <rect x="120" y="320" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="343" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프래그먼트 셰이더</text>
  <text x="320" y="343" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">각 프래그먼트의 색상 계산</text>
  <!-- Arrow -->
  <line x1="210" y1="356" x2="210" y2="380" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,386 205,376 215,376" fill="currentColor"/>
  <!-- 깊이/스텐실 테스트 + 블렌딩 -->
  <rect x="120" y="388" width="180" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="408" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">깊이/스텐실 테스트</text>
  <text x="210" y="424" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">+ 블렌딩</text>
  <text x="320" y="416" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">가시성 판별</text>
  <!-- Arrow -->
  <line x1="210" y1="436" x2="210" y2="460" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,466 205,456 215,456" fill="currentColor"/>
  <!-- 프레임버퍼 출력 -->
  <rect x="120" y="468" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="491" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임버퍼 출력</text>
</svg>
</div>

<br>

래스터화 이전 단계에서 다루는 데이터의 양은 정점 수에 비례합니다. 메쉬의 정점이 1,000개라면 버텍스 셰이더도 1,000번 실행됩니다.

래스터화 이후에는 상황이 달라집니다.

같은 메쉬가 화면의 넓은 영역을 차지하면 프래그먼트는 수십만 개에 달할 수 있고, 각각에 대해 프래그먼트 셰이더가 실행되므로 **렌더링 성능의 병목은 대부분 래스터화 이후에서 발생**합니다.

<br>

래스터화는 **고정 기능(Fixed-Function)** 단계입니다.

버텍스 셰이더나 프래그먼트 셰이더처럼 개발자가 셰이더 코드로 동작을 정의하는 프로그래머블 단계와 달리, 고정 기능 단계는 GPU 하드웨어에 동작이 미리 고정되어 있어 내부 알고리즘을 변경할 수 없습니다.

---

## 삼각형 내부 판별

래스터화의 첫 번째 과제는 화면 격자 위의 각 픽셀 위치가 삼각형 내부에 있는지 판별하는 것입니다.

삼각형의 세 꼭짓점이 화면 좌표 (x0, y0), (x1, y1), (x2, y2)로 주어졌을 때, 각 픽셀의 중심점 (px, py)이 이 삼각형 안에 있는지를 결정해야 합니다. 픽셀은 점이 아니라 면적을 가진 사각 영역이므로, GPU는 그 영역의 중심 좌표를 대표점으로 사용합니다.

### Edge Function 방식

GPU가 사용하는 표준적인 방법은 **Edge Function(변 함수)**입니다.

삼각형의 세 변 각각에 대해, 주어진 점이 변의 어느 쪽에 있는지를 판별합니다. 세 변 모두에 대해 같은 쪽(안쪽)에 있으면 삼각형 내부에 있는 것이고, 하나라도 바깥쪽이면 외부에 있는 것입니다.

<br>

변 하나에 대한 Edge Function은 **2D 외적(Cross Product)**으로 계산됩니다.

3D 외적이 두 벡터에 수직인 새로운 벡터를 반환하는 것과 달리, 2D 외적은 두 벡터의 방향 관계를 스칼라 값 하나로 나타냅니다. 벡터 (ax, ay)와 (bx, by)의 2D 외적은 `ax * by - ay * bx`이며, 결과값이 양수이면 (bx, by)가 (ax, ay)의 왼쪽에, 음수이면 오른쪽에 있습니다.

이 부호를 이용하면 임의의 점이 변의 어느 쪽에 위치하는지 계산 한 번으로 결정할 수 있습니다.

<br>

다만 부호의 의미는 삼각형의 정점 순서, 즉 앞면을 어느 방향으로 정의하느냐에 따라 달라집니다.

OpenGL과 Vulkan은 **반시계 방향(Counter-Clockwise, CCW)**을, DirectX와 Metal은 **시계 방향(Clockwise, CW)**을 앞면의 기본 정점 순서로 사용합니다.

이 글에서는 반시계 방향 기준으로 설명합니다.

<br>

래스터화 직전의 프리미티브 조립 단계에서, GPU는 세 정점의 부호 있는 넓이(signed area)를 검사하여 정점 순서를 확인하며, 뒷면으로 판정된 삼각형은 컬링(Back-Face Culling)되어 래스터화 대상에서 제외됩니다.

반시계 방향으로 나열된 삼각형에서 각 변을 따라 진행할 때, 삼각형의 내부는 항상 변의 왼쪽에 위치합니다.

따라서 변의 시작점 A에서 끝점 B로 향하는 벡터 AB와, 시작점 A에서 판별 대상점 P로 향하는 벡터 AP의 2D 외적이 양수이면 P는 변의 왼쪽(내부 쪽)에, 음수이면 오른쪽(외부 쪽)에, 0이면 변 위에 있습니다.

<br>

**Edge Function의 원리**

삼각형의 꼭짓점 $V_0, V_1, V_2$, 판별 대상점 $P$

변 $V_0 \to V_1$에 대한 Edge Function:

$$E_{01}(P) = (V_{1x} - V_{0x})(P_y - V_{0y}) - (V_{1y} - V_{0y})(P_x - V_{0x})$$

변 $V_1 \to V_2$에 대한 Edge Function:

$$E_{12}(P) = (V_{2x} - V_{1x})(P_y - V_{1y}) - (V_{2y} - V_{1y})(P_x - V_{1x})$$

변 $V_2 \to V_0$에 대한 Edge Function:

$$E_{20}(P) = (V_{0x} - V_{2x})(P_y - V_{2y}) - (V_{0y} - V_{2y})(P_x - V_{2x})$$

판별: $E_{01}(P) \geq 0$ AND $E_{12}(P) \geq 0$ AND $E_{20}(P) \geq 0$ 이면 $P$는 삼각형 내부 (반시계 방향 정점 순서 기준)

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Edge Function 시각적 예시</text>
  <!-- 왼쪽: P가 내부 -->
  <polygon points="130,42 50,172 210,172" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="36" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V0</text>
  <text x="38" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V1</text>
  <text x="222" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V2</text>
  <circle cx="130" cy="125" r="3.5" fill="currentColor"/>
  <text x="142" y="129" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">P</text>
  <text x="130" y="202" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">세 변 모두의 안쪽 → 내부</text>
  <!-- 오른쪽: Q가 외부 -->
  <polygon points="390,42 310,172 470,172" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="36" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V0</text>
  <text x="298" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V1</text>
  <text x="482" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V2</text>
  <circle cx="490" cy="130" r="3.5" fill="currentColor"/>
  <text x="502" y="134" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">Q</text>
  <text x="390" y="202" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">V2→V0 변의 바깥쪽 → 외부</text>
</svg>
</div>

<br>

Edge Function 방식에서 각 픽셀의 판별은 독립적입니다.

픽셀 A의 판별 결과가 픽셀 B에 영향을 주지 않으므로, GPU가 수많은 픽셀을 **병렬로** 판별할 수 있습니다.

[GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 다룬 SIMT 모델은 수백 개의 스레드가 동일한 명령어를 동시에 실행하는 구조인데, Edge Function의 픽셀별 독립 판별이 이 구조에 자연스럽게 들어맞습니다.

<br>

Edge Function은 픽셀 하나당 한 번 실행됩니다.

삼각형마다 화면의 모든 픽셀을 검사하면 1920×1080 해상도 기준으로 약 207만 번의 평가가 필요한데, 삼각형이 실제로 덮는 영역은 그 중 극히 일부입니다.

실제 GPU는 이 낭비를 줄이기 위해 **바운딩 박스(Bounding Box)**를 먼저 구합니다.

삼각형 세 꼭짓점의 x, y 좌표에서 최솟값과 최댓값을 취하면 삼각형을 둘러싸는 사각형이 만들어지고, GPU는 이 사각형 안의 픽셀에 대해서만 Edge Function을 평가합니다.

바운딩 박스 계산은 비교 연산 몇 번이면 끝나지만, 삼각형이 닿을 수 없는 픽셀을 사전에 걸러내어 불필요한 평가를 대폭 줄입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">바운딩 박스 최적화</text>
  <!-- 화면 격자 -->
  <rect x="50" y="35" width="280" height="225" rx="3" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1" stroke-opacity="0.2"/>
  <text x="55" y="30" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">화면 격자</text>
  <!-- 격자선 (수평) -->
  <line x1="50" y1="60" x2="330" y2="60" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="85" x2="330" y2="85" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="110" x2="330" y2="110" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="135" x2="330" y2="135" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="160" x2="330" y2="160" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="185" x2="330" y2="185" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="210" x2="330" y2="210" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="50" y1="235" x2="330" y2="235" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <!-- 격자선 (수직) -->
  <line x1="78" y1="35" x2="78" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="106" y1="35" x2="106" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="134" y1="35" x2="134" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="162" y1="35" x2="162" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="190" y1="35" x2="190" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="218" y1="35" x2="218" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="246" y1="35" x2="246" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="274" y1="35" x2="274" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="302" y1="35" x2="302" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <!-- 바운딩 박스 -->
  <rect x="106" y="85" width="168" height="150" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="2" stroke-dasharray="5,3"/>
  <!-- 삼각형 내부 영역 -->
  <polygon points="190,90 110,230 270,230" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <!-- 범례 -->
  <rect x="355" y="78" width="14" height="14" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="375" y="90" font-family="sans-serif" font-size="10" fill="currentColor">삼각형 내부</text>
  <rect x="355" y="102" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="3,2"/>
  <text x="375" y="114" font-family="sans-serif" font-size="10" fill="currentColor">바운딩 박스</text>
  <!-- 결론 -->
  <text x="230" y="282" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">바운딩 박스 안의 픽셀에 대해서만 Edge Function 평가</text>
  <text x="230" y="298" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">바운딩 박스 밖의 픽셀은 검사 생략</text>
</svg>
</div>

### 무게중심 좌표 (Barycentric Coordinates)

Edge Function의 세 값 E01, E12, E20은 단순히 "안/밖"을 판별하는 것 이상의 정보를 제공합니다.

각 Edge Function 값은 기하학적으로 해당 변과 점 P로 이루어지는 부분 삼각형의 넓이(부호 있는 값의 2배)에 해당합니다.

세 부분 삼각형의 넓이를 합치면 원래 삼각형 전체 넓이가 되므로, 각 값을 전체 넓이로 나누면 세 값의 합이 정확히 1이 됩니다. 

이렇게 정규화된 세 값이 **무게중심 좌표(Barycentric Coordinates)**이며, 삼각형 내부에서 점 P의 위치를 세 꼭짓점에 대한 가중치로 표현합니다.

<br>

무게중심 좌표는 보통 (u, v, w) 또는 (lambda0, lambda1, lambda2)로 표기하며, 세 값의 합은 항상 1입니다.

각 값은 해당 꼭짓점이 점 P에 미치는 가중치를 나타내며, 점 P가 특정 꼭짓점에 가까울수록 그 꼭짓점에 대응하는 값이 1에 가까워집니다.

<br>

각 Edge Function 값이 어느 꼭짓점의 가중치가 되는지는 기하학적으로 결정됩니다.

E12는 점 P가 변 V1→V2에서 얼마나 떨어져 있는지에 비례합니다.

V0은 변 V1→V2의 맞은편 꼭짓점이므로, P가 V0에 가까울수록 E12가 커지고, P가 변 V1→V2 위에 있으면 E12는 0이 됩니다.

같은 원리로 E20은 V1에 대한, E01은 V2에 대한 가중치입니다.

<br>

**무게중심 좌표의 의미**

삼각형 꼭짓점 $V_0, V_1, V_2$, 내부의 점 $P$

$$P = u \cdot V_0 + v \cdot V_1 + w \cdot V_2 \qquad (u + v + w = 1, \;\; u \geq 0, \;\; v \geq 0, \;\; w \geq 0)$$

$u, v, w$ 계산 — 삼각형 전체 넓이 $S = E_{01} + E_{12} + E_{20}$ (부호 있는 넓이의 2배):

$$u = \frac{E_{12}}{S} \qquad v = \frac{E_{20}}{S} \qquad w = \frac{E_{01}}{S}$$

- $u$: $V_0$에 대한 가중치 ($V_0$ 맞은편 변 $V_1 \to V_2$ 기준)
- $v$: $V_1$에 대한 가중치 ($V_1$ 맞은편 변 $V_2 \to V_0$ 기준)
- $w$: $V_2$에 대한 가중치 ($V_2$ 맞은편 변 $V_0 \to V_1$ 기준)

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">무게중심 좌표 예시</text>
  <!-- 삼각형 -->
  <polygon points="175,42 55,190 295,190" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- V0 -->
  <circle cx="175" cy="42" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="175" y="35" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V0</text>
  <text x="175" y="25" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.55">(u=1, v=0, w=0)</text>
  <!-- V1 -->
  <circle cx="55" cy="190" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="55" y="207" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V1</text>
  <text x="55" y="220" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.55">(u=0, v=1, w=0)</text>
  <!-- V2 -->
  <circle cx="295" cy="190" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="295" y="207" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V2</text>
  <text x="295" y="220" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.55">(u=0, v=0, w=1)</text>
  <!-- P -->
  <circle cx="163" cy="146" r="4" fill="currentColor"/>
  <text x="176" y="144" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">P</text>
  <!-- P의 좌표 -->
  <text x="370" y="75" font-family="sans-serif" font-size="10" fill="currentColor">P의 무게중심 좌표:</text>
  <text x="370" y="93" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">u=0.3, v=0.4, w=0.3</text>
  <!-- 성질 -->
  <text x="370" y="125" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">V1에 가까울수록 v가 크고</text>
  <text x="370" y="141" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">V0에 가까울수록 u가 크다</text>
  <text x="370" y="170" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">삼각형 중심: u = v = w = 1/3</text>
  <!-- 꼭짓점 좌표 요약 -->
  <text x="260" y="250" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">각 꼭짓점의 무게중심 좌표: V0(1,0,0) · V1(0,1,0) · V2(0,0,1)</text>
</svg>
</div>

<br>

무게중심 좌표 (u, v, w)는 곧 정점 속성 보간의 가중치입니다.

V0의 색상이 빨강, V1이 초록, V2가 파랑이고 어떤 픽셀의 무게중심 좌표가 (0.5, 0.3, 0.2)라면, 그 픽셀의 색상은 빨강 50% + 초록 30% + 파랑 20%를 혼합한 값이 됩니다.

색상뿐 아니라 UV 좌표, 법선 벡터 등 꼭짓점에 정의된 모든 속성을 같은 방식으로 보간할 수 있습니다.

래스터화는 삼각형 내부의 각 픽셀마다 이 보간을 수행하여, 보간된 속성이 채워진 픽셀별 데이터인 **프래그먼트**를 생성합니다.

---

## 프래그먼트 vs 픽셀

Edge Function과 무게중심 좌표를 통해 삼각형 내부의 픽셀 위치가 판별되면, 각 위치에 대해 래스터화가 생성하는 것이 **프래그먼트(Fragment)**입니다.

프래그먼트와 픽셀은 흔히 혼용되지만, 엄밀히 다른 개념입니다.

<br>

**픽셀(Pixel)**은 화면의 최종 출력 단위입니다.

1920x1080 해상도의 디스플레이에는 약 207만 개의 픽셀이 있고, 각 픽셀은 화면에서 하나의 점에 해당합니다.

프레임버퍼에 최종 기록되어 화면에 표시되는 색상 값이 곧 픽셀입니다.

<br>

**프래그먼트(Fragment)**는 삼각형이 덮는 픽셀 위치에 대한 **후보 데이터**입니다.

래스터화가 삼각형 내부의 각 픽셀 위치에 대해 생성하는 것이 프래그먼트이며, 각 프래그먼트에는 해당 위치의 색상, 깊이, 텍스처 좌표(UV), 법선 벡터 등의 속성이 채워져야 합니다.

이 속성들은 정점에 정의된 값으로부터 보간을 통해 계산됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프래그먼트와 픽셀의 관계</text>
  <text x="300" y="40" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">같은 픽셀 위치에 삼각형 A, B, C가 겹치는 경우</text>
  <!-- 삼각형 A -->
  <rect x="30" y="62" width="140" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">삼각형 A (z=0.3)</text>
  <!-- Arrow A → Fragment A -->
  <line x1="170" y1="78" x2="210" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="216,78 206,73 206,83" fill="currentColor"/>
  <!-- 프래그먼트 A -->
  <rect x="218" y="62" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="278" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 A</text>
  <!-- 삼각형 B -->
  <rect x="30" y="110" width="140" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">삼각형 B (z=0.7)</text>
  <!-- Arrow B → Fragment B -->
  <line x1="170" y1="126" x2="210" y2="126" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="216,126 206,121 206,131" fill="currentColor"/>
  <!-- 프래그먼트 B -->
  <rect x="218" y="110" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="278" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 B</text>
  <!-- 삼각형 C -->
  <rect x="30" y="158" width="140" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="178" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">삼각형 C (z=0.5)</text>
  <!-- Arrow C → Fragment C -->
  <line x1="170" y1="174" x2="210" y2="174" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="216,174 206,169 206,179" fill="currentColor"/>
  <!-- 프래그먼트 C -->
  <rect x="218" y="158" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="278" y="178" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 C</text>
  <!-- Converging lines from fragments to depth test -->
  <line x1="338" y1="78" x2="370" y2="126" stroke="currentColor" stroke-width="1.5"/>
  <line x1="338" y1="126" x2="370" y2="126" stroke="currentColor" stroke-width="1.5"/>
  <line x1="338" y1="174" x2="370" y2="126" stroke="currentColor" stroke-width="1.5"/>
  <!-- Arrow to depth test box -->
  <line x1="370" y1="126" x2="384" y2="126" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="390,126 380,121 380,131" fill="currentColor"/>
  <!-- 깊이 테스트 -->
  <rect x="392" y="106" width="90" height="40" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="437" y="123" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">깊이 테스트</text>
  <text x="437" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">하나만 남음</text>
  <!-- Arrow to final pixel -->
  <line x1="482" y1="126" x2="510" y2="126" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="516,126 506,121 506,131" fill="currentColor"/>
  <!-- 최종 픽셀 -->
  <rect x="518" y="110" width="66" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="551" y="127" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">최종 픽셀</text>
  <text x="551" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(1개)</text>
  <!-- Conclusion text -->
  <text x="300" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">한 픽셀 위치에 프래그먼트가 3개 생성됨</text>
  <text x="300" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">깊이 테스트를 거쳐 가장 가까운 프래그먼트 A만 최종 픽셀로 남음</text>
</svg>
</div>

<br>

한 픽셀 위치에 여러 삼각형이 겹치면 프래그먼트도 여러 개 생성됩니다. 

프래그먼트들은 이후의 깊이 테스트(Depth Test)를 거쳐 카메라에 가장 가까운 하나만 최종 픽셀로 남고, 나머지는 폐기됩니다.
 
폐기되는 프래그먼트에 대해서도 프래그먼트 셰이더는 실행되므로, 그 연산 비용은 낭비됩니다.
 
같은 픽셀 위치를 여러 삼각형이 덮어쓰는 이 현상이 [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 다룬 **오버드로우(Overdraw)**이며, Early-Z 테스트는 프래그먼트 셰이더 실행 전에 깊이 테스트를 수행하여 이 낭비를 줄입니다.

<br>

"프래그먼트 셰이더"라는 이름은 이 셰이더가 최종 픽셀이 아니라 후보 단계의 프래그먼트에 대해 실행되기 때문에 붙었습니다.

DirectX에서는 같은 단계를 픽셀 셰이더(Pixel Shader)라 부르지만, 처리 대상은 동일하게 프래그먼트입니다.

---

## 보간 (Interpolation)

버텍스 셰이더가 출력하는 색상, UV 좌표, 법선 벡터 등의 속성은 정점에만 정의되어 있고, 정점 사이에 위치하는 프래그먼트에는 이 값이 없습니다.

**보간(Interpolation)**은 앞에서 구한 무게중심 좌표를 가중치로 사용하여 정점의 속성 값으로부터 프래그먼트 위치의 속성 값을 산출합니다.

### 무게중심 좌표를 이용한 보간

앞에서 구한 무게중심 좌표 (u, v, w)를 직접 가중치로 사용합니다.

세 꼭짓점의 속성 값이 A0, A1, A2일 때, 프래그먼트 위치의 속성 값은 세 값의 가중 합입니다.

<br>

**무게중심 좌표 보간**

속성 값의 보간:

$$A(P) = u \cdot A_0 + v \cdot A_1 + w \cdot A_2$$

<br>

**예시 — UV 좌표 보간**

$V_0$의 UV: $(0.0, \; 1.0)$, &nbsp; $V_1$의 UV: $(1.0, \; 0.0)$, &nbsp; $V_2$의 UV: $(0.5, \; 0.5)$

프래그먼트 $P$의 무게중심 좌표: $u = 0.3, \; v = 0.4, \; w = 0.3$

$$U_P = 0.3 \times 0.0 + 0.4 \times 1.0 + 0.3 \times 0.5 = 0.55$$

$$V_P = 0.3 \times 1.0 + 0.4 \times 0.0 + 0.3 \times 0.5 = 0.45$$

$P$의 UV $= (0.55, \; 0.45)$

<br>

이 방식은 UV 좌표뿐 아니라 법선 벡터, 정점 색상, 커스텀 속성 등 버텍스 셰이더가 출력하는 모든 속성에 동일하게 적용됩니다.

프래그먼트 셰이더가 입력으로 받는 UV, 법선 등의 값은 모두 이 보간 과정을 거친 결과입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <text x="250" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">색상 보간 예시</text>
  <!-- 삼각형 -->
  <polygon points="175,42 55,190 295,190" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 꼭짓점 라벨 -->
  <circle cx="175" cy="42" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="175" y="33" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V0 (빨강)</text>
  <circle cx="55" cy="190" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="55" y="205" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V1 (초록)</text>
  <circle cx="295" cy="190" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="295" y="205" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">V2 (파랑)</text>
  <!-- 점 P -->
  <circle cx="163" cy="146" r="4" fill="currentColor"/>
  <text x="176" y="144" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">P</text>
  <!-- 가중치 주석 -->
  <text x="340" y="90" font-family="sans-serif" font-size="10" fill="currentColor">u = 0.3 → 빨강 30%</text>
  <text x="340" y="108" font-family="sans-serif" font-size="10" fill="currentColor">v = 0.4 → 초록 40%</text>
  <text x="340" y="126" font-family="sans-serif" font-size="10" fill="currentColor">w = 0.3 → 파랑 30%</text>
  <!-- 결과 -->
  <text x="250" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">결과: P = 초록빛이 도는 중간색 (R=0.3, G=0.4, B=0.3)</text>
</svg>
</div>

### 원근 보정 보간 (Perspective-Correct Interpolation)

앞에서 다룬 무게중심 좌표 보간은 화면에 투영된 2D 좌표만으로 가중치를 계산합니다.

그런데 원근 투영에서는 카메라에 가까운 영역이 화면에서 넓게 펼쳐지고, 먼 영역은 좁게 압축됩니다.

화면 위에서 같은 간격이라도 3D 공간에서의 실제 간격은 다릅니다.

이 차이를 무시하고 화면 공간에서 단순히 보간하면, 카메라에 가까운 쪽의 텍스처가 늘어나고 먼 쪽이 찌그러지는 왜곡이 발생합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">화면에 보간된 텍스처 비교</text>
  <text x="80" y="42" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">가까운 쪽</text>
  <text x="390" y="42" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">먼 쪽</text>
  <!-- 1행: 단순 보간 (등간격 = 왜곡) -->
  <text x="25" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">단순</text>
  <text x="25" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">보간</text>
  <rect x="80" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="105" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T1</text>
  <rect x="130" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="155" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T2</text>
  <rect x="180" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="205" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T3</text>
  <rect x="230" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="255" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T4</text>
  <rect x="280" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="305" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T5</text>
  <rect x="330" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="355" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T6</text>
  <rect x="380" y="52" width="50" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="405" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T7</text>
  <text x="470" y="62" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">등간격</text>
  <text x="470" y="74" font-family="sans-serif" font-size="9" fill="#c0392b" font-weight="bold">✗ 왜곡</text>
  <!-- 2행: 원근 보정 보간 (비등간격 = 올바름) -->
  <text x="25" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">원근</text>
  <text x="25" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">보정</text>
  <rect x="80" y="116" width="90" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="125" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T1</text>
  <rect x="170" y="116" width="70" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="205" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T2</text>
  <rect x="240" y="116" width="55" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="267" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T3</text>
  <rect x="295" y="116" width="42" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="316" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T4</text>
  <rect x="337" y="116" width="35" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="354" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T5</text>
  <rect x="372" y="116" width="30" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="387" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T6</text>
  <rect x="402" y="116" width="28" height="28" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="416" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">T7</text>
  <text x="470" y="128" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">비등간격</text>
  <text x="470" y="140" font-family="sans-serif" font-size="9" fill="#27ae60" font-weight="bold">✓ 정확</text>
  <!-- 결론 -->
  <text x="260" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 단순 보간은 텍스처를 균등하게 배분하여 원근감이 사라진다</text>
  <text x="260" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 원근 보정은 깊이(w)를 반영하여 가까운 쪽을 크게, 먼 쪽을 작게 보간한다</text>
</svg>
</div>

<br>

여기서 사용되는 **w 값(w₀, w₁, w₂)**은 버텍스 셰이더가 출력하는 클립 공간 좌표의 네 번째 성분입니다. Projection 행렬의 구조에 따라 뷰 공간 z값의 부호가 달라지지만(OpenGL 계열은 w = −z, DirectX 계열은 w = z), 어느 경우든 카메라로부터의 깊이를 나타냅니다.

앞 절의 무게중심 좌표 (u, v, w)에서 w가 "세 번째 가중치"를 가리키는 것과 의미가 다르므로 주의가 필요합니다.

<br>

원근 투영 후 화면 공간에서 속성 A를 직접 보간하면 비선형이라 결과가 틀리지만, A/w와 1/w는 화면 공간에서도 선형으로 변합니다.

원근 보정 보간은 이 성질을 이용합니다.

먼저 각 정점의 속성 값을 해당 정점의 클립 공간 w로 나눈 A/w 상태에서 무게중심 좌표로 보간하고, 1/w도 같은 방식으로 보간합니다.

그런 다음 A/w 보간 결과를 1/w 보간 결과로 나누면 w가 상쇄되어 3D 공간에서의 올바른 속성 값이 복원됩니다.

<br>

**원근 보정 보간 공식**

표기 구분:
- $\lambda_0, \lambda_1, \lambda_2$ — 무게중심 좌표 (앞 절의 $u, v, w$와 동일, 혼동 방지를 위해 $\lambda$로 표기)
- $w_0, w_1, w_2$ — 각 정점의 클립 공간 $w$ 값 (뷰 공간 $z$값, 카메라 기준 깊이)

일반 보간 (화면 공간, 부정확):

$$A(P) = \lambda_0 A_0 + \lambda_1 A_1 + \lambda_2 A_2$$

원근 보정 보간 (정확):

$$A(P) = \frac{\lambda_0 \frac{A_0}{w_0} + \lambda_1 \frac{A_1}{w_1} + \lambda_2 \frac{A_2}{w_2}}{\lambda_0 \frac{1}{w_0} + \lambda_1 \frac{1}{w_1} + \lambda_2 \frac{1}{w_2}}$$

<br>

버텍스 셰이더가 클립 공간 좌표(w 포함)를 출력하면, 래스터화 하드웨어가 w 값을 사용하여 모든 속성 보간에 원근 보정을 자동으로 적용합니다.

셰이더에서 이 보정을 직접 구현할 필요는 없습니다.

<br>

다만 스크린 스페이스 UV나 포스트 프로세싱처럼 화면 좌표 기준으로 보간해야 하는 값에는 원근 보정이 오히려 왜곡을 만듭니다.

HLSL에서는 버텍스 셰이더 출력 변수에 `noperspective` 수식어를 붙여 해당 변수의 원근 보정을 비활성화할 수 있습니다.

---

## 2x2 Quad 실행

보간까지 완료되면 각 프래그먼트에는 프래그먼트 셰이더가 사용할 속성 값이 준비됩니다.

GPU는 이 프래그먼트를 개별적으로 처리하지 않고, 텍스처 샘플링에 필요한 화면 공간 미분값을 구하기 위해 항상 인접한 2x2 픽셀을 하나로 묶은 **Quad** 단위로 처리합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2x2 Quad의 구조</text>
  <text x="240" y="35" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">화면 격자 위의 한 영역</text>
  <!-- Quad 배경 (교차 음영) -->
  <rect x="120" y="48" width="104" height="104" fill="currentColor" fill-opacity="0.08"/>
  <rect x="224" y="48" width="104" height="104" fill="currentColor" fill-opacity="0.03"/>
  <rect x="120" y="152" width="104" height="104" fill="currentColor" fill-opacity="0.03"/>
  <rect x="224" y="152" width="104" height="104" fill="currentColor" fill-opacity="0.08"/>
  <!-- Row 0 -->
  <rect x="120" y="48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="146" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P0</text>
  <rect x="172" y="48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="198" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P1</text>
  <rect x="224" y="48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P4</text>
  <rect x="276" y="48" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="302" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P5</text>
  <!-- Row 1 -->
  <rect x="120" y="100" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="146" y="132" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P2</text>
  <rect x="172" y="100" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="198" y="132" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P3</text>
  <rect x="224" y="100" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="132" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P6</text>
  <rect x="276" y="100" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="302" y="132" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P7</text>
  <!-- Row 2 -->
  <rect x="120" y="152" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="146" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P8</text>
  <rect x="172" y="152" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="198" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P9</text>
  <rect x="224" y="152" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P12</text>
  <rect x="276" y="152" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="302" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P13</text>
  <!-- Row 3 -->
  <rect x="120" y="204" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="146" y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P10</text>
  <rect x="172" y="204" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="198" y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P11</text>
  <rect x="224" y="204" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P14</text>
  <rect x="276" y="204" width="52" height="52" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="302" y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">P15</text>
  <!-- Quad 라벨 -->
  <text x="240" y="276" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Quad 0: [P0, P1, P2, P3] ← 2x2 묶음</text>
  <text x="240" y="293" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Quad 1: [P4, P5, P6, P7] ← 2x2 묶음</text>
</svg>
</div>

### Quad 단위 실행의 이유

GPU가 프래그먼트를 2x2 단위로 묶어 처리하는 이유는 **텍스처 샘플링에 필요한 미분값(derivative)** 때문입니다.

<br>

텍스처를 샘플링할 때, GPU는 어떤 밉맵(Mipmap) 레벨을 사용할지 결정해야 합니다. 밉맵은 원본 텍스처를 절반씩 축소하여 미리 만들어둔 여러 해상도의 텍스처 체인입니다. 가까운 오브젝트는 텍스처가 크게 보이므로 고해상도 밉맵을 사용하고, 먼 오브젝트는 텍스처가 작게 보이므로 저해상도 밉맵을 사용합니다.

적절한 밉맵 레벨을 결정하는 기준은, 화면의 1픽셀이 텍스처에서 얼마나 넓은 영역에 대응하는지입니다. 텍스처를 구성하는 최소 단위를 **텍셀(Texel)**이라 하며, 1픽셀에 대응하는 텍셀이 많을수록 텍스처가 작게 보이므로 저해상도 밉맵이 선택됩니다. 이 대응 관계는 화면에서 1픽셀 이동했을 때의 UV 변화량, 즉 UV 좌표의 **편미분값(partial derivative)**으로 측정하며, 인접한 픽셀의 UV 값 차이에서 구합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Quad에서의 편미분 계산</text>
  <!-- Top-left: P(x,y) -->
  <rect x="100" y="40" width="130" height="65" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="165" y="60" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">P(x, y)</text>
  <text x="165" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">UV = (0.3, 0.7)</text>
  <!-- Top-right: P(x+1,y) -->
  <rect x="230" y="40" width="130" height="65" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="295" y="60" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">P(x+1, y)</text>
  <text x="295" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">UV = (0.35, 0.7)</text>
  <!-- Bottom-left: P(x,y+1) -->
  <rect x="100" y="105" width="130" height="65" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="165" y="125" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">P(x, y+1)</text>
  <text x="165" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">UV = (0.3, 0.75)</text>
  <!-- Bottom-right: P(x+1,y+1) -->
  <rect x="230" y="105" width="130" height="65" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="295" y="125" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">P(x+1, y+1)</text>
  <text x="295" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">UV = (0.35, 0.75)</text>
  <!-- 수평 화살표: 상단 행 (ddx) -->
  <line x1="195" y1="34" x2="265" y2="34" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="268,34 260,30 260,38" fill="currentColor" opacity="0.5"/>
  <text x="230" y="28" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">ddx</text>
  <!-- 수평 화살표: 하단 행 (ddx) -->
  <line x1="195" y1="176" x2="265" y2="176" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="268,176 260,172 260,180" fill="currentColor" opacity="0.5"/>
  <text x="230" y="189" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">ddx</text>
  <!-- 수직 화살표: 좌측 열 (ddy) -->
  <line x1="94" y1="68" x2="94" y2="133" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="94,138 90,130 98,130" fill="currentColor" opacity="0.5"/>
  <text x="84" y="105" text-anchor="end" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">ddy</text>
  <!-- 수직 화살표: 우측 열 (ddy) -->
  <line x1="366" y1="68" x2="366" y2="133" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="366,138 362,130 370,130" fill="currentColor" opacity="0.5"/>
  <text x="376" y="105" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">ddy</text>
  <!-- 계산 결과 -->
  <text x="260" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">dU/dx = 0.35 − 0.3 = 0.05 (수평 방향 UV 변화율)</text>
  <text x="260" y="216" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">dV/dy = 0.75 − 0.7 = 0.05 (수직 방향 UV 변화율)</text>
  <!-- 밉맵 레벨 결정 -->
  <text x="260" y="252" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">변화율이 크면 → 1픽셀에 많은 텍셀 대응 → 저해상도 밉맵</text>
  <text x="260" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">변화율이 작으면 → 1픽셀에 적은 텍셀 대응 → 고해상도 밉맵</text>
</svg>
</div>

<br>

이 계산을 위해 같은 Quad 안의 4개 프래그먼트는 하나의 Warp 안에 배치됩니다([GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/) 참조).

같은 Warp의 스레드는 레인 간 교환 명령(NVIDIA의 `shfl.sync`, AMD의 `ds_swizzle` 등)으로 서로의 레지스터 값을 직접 읽을 수 있으므로, 추가 메모리 접근 없이 인접 프래그먼트의 값을 참조할 수 있습니다.

셰이더에서 `ddx()`, `ddy()`, `fwidth()` 함수를 호출하면 GPU는 이 교환 명령으로 편미분을 계산합니다.

### 작은 삼각형의 비효율

삼각형이 Quad 내에서 일부 픽셀만 덮더라도 GPU는 4개 프래그먼트를 모두 실행해야 합니다.

삼각형 밖의 프래그먼트는 **헬퍼 프래그먼트(Helper Fragment)**로, 편미분 계산을 위해 프래그먼트 셰이더가 실행되지만 최종 결과는 폐기됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">헬퍼 프래그먼트의 발생</text>
  <!-- 좌: 1픽셀만 덮는 경우 -->
  <text x="145" y="45" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">1픽셀만 덮는 경우</text>
  <!-- 2x2 Quad -->
  <rect x="80" y="55" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="145" y="55" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <rect x="80" y="120" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="112" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">■</text>
  <rect x="145" y="120" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <!-- 결과 -->
  <text x="145" y="206" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">4개 실행, 1개 유효</text>
  <text x="145" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">효율 25%</text>
  <!-- 우: Quad를 가득 채우는 경우 -->
  <text x="395" y="45" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Quad를 가득 채우는 경우</text>
  <!-- 2x2 Quad (모두 채움) -->
  <rect x="330" y="55" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="362" y="93" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">■</text>
  <rect x="395" y="55" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="427" y="93" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">■</text>
  <rect x="330" y="120" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="362" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">■</text>
  <rect x="395" y="120" width="65" height="65" rx="3" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="427" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">■</text>
  <!-- 결과 -->
  <text x="395" y="206" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">4개 실행, 4개 유효</text>
  <text x="395" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">효율 100%</text>
  <!-- 범례 -->
  <rect x="170" y="252" width="12" height="12" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <text x="188" y="263" font-family="sans-serif" font-size="9" fill="currentColor">유효 프래그먼트</text>
  <rect x="280" y="252" width="12" height="12" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>
  <text x="298" y="263" font-family="sans-serif" font-size="9" fill="currentColor">헬퍼 프래그먼트 (폐기)</text>
</svg>
</div>

<br>

이 비효율은 삼각형이 작을수록 심해집니다.

삼각형이 크면 내부 Quad는 100% 효율로 채워지고 가장자리 Quad에서만 헬퍼 프래그먼트가 발생하지만, 1~2픽셀짜리 삼각형은 Quad를 거의 채우지 못해 효율이 25~50%까지 떨어집니다.

이런 삼각형이 대량으로 존재하면 오버헤드가 누적되어 프래그먼트 셰이더의 유효 작업 비율이 크게 떨어집니다.

수십만 폴리곤의 고해상도 메쉬가 카메라에서 멀리 있어 화면에서 작게 보이는 경우가 대표적입니다.

LOD(Level of Detail) 시스템이 카메라에서 먼 오브젝트의 메쉬를 단순한 버전으로 교체하는 이유 중 하나가 이 Quad 오버헤드 때문입니다.

<br>

모바일에서 삼각형 수를 줄여야 하는 이유는 버텍스 셰이더 부하([GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 TBDR의 Binning 비용)뿐 아니라, 이 Quad 비효율과도 관련이 있습니다.

화면에서 2픽셀 이하 크기의 삼각형이 다수 존재한다면, 삼각형 수를 줄이는 것만으로도 프래그먼트 셰이더 단계의 효율이 함께 높아집니다.

---

## 래스터화 규칙

Edge Function은 점이 삼각형 내부에 있는지 판별하지만, 변 위에 정확히 놓인 샘플 포인트(픽셀 중심, 또는 MSAA 샘플 위치)는 내부와 외부 어느 쪽에도 속하지 않습니다.

두 삼각형이 변을 공유할 때, 이 샘플 포인트를 양쪽 모두 포함하면 두 번 그려지고, 양쪽 모두 제외하면 빈 틈이 생깁니다.

### Top-Left Rule

이 문제를 해결하기 위해 GPU는 **Top-Left Rule**을 적용합니다.

변 위에 놓인 샘플 포인트는 해당 변이 삼각형의 위쪽 변(top edge)이나 왼쪽 변(left edge)일 때만 포함되고, 그 외에는 제외됩니다.

<br>

여기서 **왼쪽 변(left edge)**과 **위쪽 변(top edge)**은 삼각형 안에서의 시각적 위치가 아니라, 와인딩 순서에서의 진행 방향으로 분류됩니다. 와인딩 순서를 따라갈 때 위로 올라가는 변이 left edge, 수평이면서 오른쪽으로 진행하는 변이 top edge입니다.

<br>

이 방향 기반 분류가 공유 변 문제를 해결합니다. 두 삼각형이 동일한 정점 좌표를 공유하고 일관된 와인딩으로 래스터화되면, 공유 변의 진행 방향이 서로 반대가 됩니다. 한쪽에서 위로 올라가는 변(left → 포함)은 다른 쪽에서 아래로 내려가는 변(제외)이 되므로, 공유 변 위의 샘플 포인트는 항상 정확히 한 삼각형에만 포함됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Top-Left Rule</text>
  <text x="240" y="35" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">두 삼각형이 변을 공유하는 경우</text>
  <!-- Triangle A (공유 변 포함) -->
  <polygon points="80,50 80,170 380,50" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="82" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">A</text>
  <!-- Triangle B (공유 변 제외) -->
  <polygon points="380,50 80,170 380,170" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="152" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">B</text>
  <!-- 공유 변: A의 와인딩 방향 (V1→V2, ↗ 위로) — 실선 화살표 -->
  <line x1="106" y1="153" x2="337" y2="60" stroke="currentColor" stroke-width="2.5"/>
  <polygon points="345,58 337,65 334,58" fill="currentColor"/>
  <text x="260" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">↗ left edge → 포함</text>
  <!-- 공유 변: B의 와인딩 방향 (V0→V1, ↙ 아래로) — 점선 화살표 -->
  <line x1="354" y1="67" x2="123" y2="160" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.4"/>
  <polygon points="115,162 123,155 126,162" fill="currentColor" opacity="0.4"/>
  <text x="200" y="145" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">↙ 제외</text>
  <!-- 결론 -->
  <text x="240" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 같은 변이라도 진행 방향이 반대이므로, 한쪽만 포함</text>
  <text x="240" y="214" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">빈 틈(gap)이나 이중 렌더링(double draw) 방지</text>
</svg>
</div>

<br>

Top-Left Rule은 DirectX, Metal, Vulkan 명세에 규정되어 있으며, OpenGL에서는 구현 정의(implementation-defined)로 남겨두지만 대부분의 구현이 동일한 규칙을 따릅니다.

---

## 래스터화의 전체 흐름 정리

앞에서 다룬 각 단계를 하나의 흐름으로 연결하면 래스터화의 전체 과정이 드러납니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <text x="270" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">래스터화 전체 과정</text>
  <!-- Step 1 -->
  <circle cx="98" cy="51" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="55" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">1</text>
  <rect x="115" y="35" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="55" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">입력</text>
  <text x="330" y="55" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">세 꼭짓점의 2D 좌표 + 속성</text>
  <line x1="215" y1="67" x2="215" y2="76" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,82 211,74 219,74" fill="currentColor"/>
  <!-- Step 2 -->
  <circle cx="98" cy="98" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="102" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">2</text>
  <rect x="115" y="82" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">바운딩 박스 계산</text>
  <text x="330" y="102" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">x, y 최솟값/최댓값으로 사각 영역</text>
  <line x1="215" y1="114" x2="215" y2="123" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,129 211,121 219,121" fill="currentColor"/>
  <!-- Step 3 -->
  <circle cx="98" cy="145" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="149" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">3</text>
  <rect x="115" y="129" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="149" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">내부 판별 (Edge Function)</text>
  <text x="330" y="149" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">세 변의 Edge Function 평가</text>
  <line x1="215" y1="161" x2="215" y2="170" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,176 211,168 219,168" fill="currentColor"/>
  <!-- Step 4 -->
  <circle cx="98" cy="192" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="196" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">4</text>
  <rect x="115" y="176" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">무게중심 좌표 계산</text>
  <text x="330" y="196" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">정규화하여 (u, v, w) 도출</text>
  <line x1="215" y1="208" x2="215" y2="217" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,223 211,215 219,215" fill="currentColor"/>
  <!-- Step 5 -->
  <circle cx="98" cy="239" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="243" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">5</text>
  <rect x="115" y="223" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="243" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">속성 보간</text>
  <text x="330" y="237" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">UV, 법선, 색상 보간</text>
  <text x="330" y="250" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">+ 원근 보정 적용</text>
  <line x1="215" y1="255" x2="215" y2="264" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,270 211,262 219,262" fill="currentColor"/>
  <!-- Step 6 -->
  <circle cx="98" cy="286" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="290" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">6</text>
  <rect x="115" y="270" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 생성</text>
  <text x="330" y="290" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">보간된 속성을 담은 데이터 생성</text>
  <line x1="215" y1="302" x2="215" y2="311" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,317 211,309 219,309" fill="currentColor"/>
  <!-- Step 7 -->
  <circle cx="98" cy="333" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="337" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">7</text>
  <rect x="115" y="317" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="337" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">2x2 Quad 구성</text>
  <text x="330" y="337" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">헬퍼 프래그먼트 추가</text>
  <line x1="215" y1="349" x2="215" y2="358" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,364 211,356 219,356" fill="currentColor"/>
  <!-- Step 8 -->
  <circle cx="98" cy="380" r="10" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>
  <text x="98" y="384" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">8</text>
  <rect x="115" y="364" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="384" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 셰이더로 전달</text>
  <text x="330" y="384" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Quad 단위로 셰이더 실행</text>
</svg>
</div>

이 8단계가 하나의 삼각형에 대해 완료되면, 해당 삼각형이 덮는 모든 픽셀 위치에 대한 프래그먼트 데이터가 프래그먼트 셰이더로 넘어갑니다.

---

## 마무리

- **래스터화**는 삼각형이 덮는 화면 영역의 각 픽셀 위치를 식별하고 프래그먼트를 생성합니다.
- **Edge Function**은 2D 외적으로 점이 삼각형 내부에 있는지를 판별하며, 각 픽셀을 독립적으로 처리할 수 있어 GPU 병렬 처리에 적합합니다.
- **무게중심 좌표**는 삼각형 내부의 점을 세 꼭짓점에 대한 가중치로 표현하며, 정점 속성 보간의 기반입니다.
- **프래그먼트**는 최종 픽셀의 후보이며, 한 픽셀 위치에 여러 프래그먼트가 존재할 수 있고 깊이 테스트를 거쳐 하나만 남습니다.
- **보간**은 무게중심 좌표를 사용한 선형 보간이며, 3D 오브젝트에서는 원근 보정 보간이 자동 적용됩니다.
- **2x2 Quad**는 GPU가 프래그먼트를 처리하는 최소 단위이며, 삼각형이 작을수록 헬퍼 프래그먼트에 의한 비효율이 커집니다.

래스터화는 고정 기능 단계이므로 셰이더로 제어할 수 없지만, 삼각형의 크기와 화면 점유 면적이 프래그먼트 수를 결정하고, 이것이 프래그먼트 셰이더의 비용에 직접 영향을 미칩니다.

래스터화로 생성된 프래그먼트는 프래그먼트 셰이더를 거쳐 색상이 결정되지만, 그것만으로 최종 픽셀이 확정되지는 않습니다. 겹치는 프래그먼트 중 어떤 것을 남길지, 특정 영역에만 그릴지, 반투명 효과를 어떻게 합성할지를 결정하는 별도의 메커니즘이 필요합니다.

[다음 글](/dev/unity/RasterPipeline-2/)에서는 프레임 버퍼, 깊이 버퍼, 스텐실 버퍼, 블렌딩, 렌더 타겟과 MRT를 다룹니다. 프래그먼트 셰이더의 비용 구조와 최적화 방법은 [셰이더 최적화 (1)](/dev/unity/ShaderOptimization-1/)에서 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)

**시리즈**
- **래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지** (현재 글)
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱](/dev/unity/RasterPipeline-3/)

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
- [C# 런타임 기초 (3) - 가비지 컬렉션의 기초](/dev/unity/CSharpRuntime-3/)
- [C# 런타임 기초 (4) - 스레딩과 비동기](/dev/unity/CSharpRuntime-4/)
- [색과 빛 (1) - 빛의 물리적 원리](/dev/unity/ColorAndLight-1/)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
- **래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지** (현재 글)
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
