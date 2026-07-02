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

[그래픽스 수학 (3)](/dev/unity/GraphicsMath-3/)에서는 3D 정점이 여러 좌표 공간을 거쳐 2D 화면 좌표에 이르는 과정을 다루었습니다. 버텍스 셰이더가 정점을 클립 공간으로 옮기고 GPU가 원근 나눗셈과 뷰포트 변환을 마치면, 삼각형의 세 꼭짓점은 비로소 화면 위의 2D 좌표를 얻습니다.

이 시점까지 만들어진 것은 세 꼭짓점의 화면 좌표와, 꼭짓점마다 딸려 온 색상·UV 좌표·법선 벡터 같은 속성값뿐입니다. 정작 화면을 채우는 픽셀에는 아직 아무 값도 놓이지 않았습니다.

화면이 연속된 좌표 평면이 아니라 **이산적인 픽셀 격자**이기 때문입니다. 꼭짓점 세 개의 좌표만으로는 삼각형 내부의 어떤 픽셀을 칠해야 하는지, 또 그 픽셀에 어떤 색과 깊이를 채워야 하는지 알 수 없습니다.

이 간극을 메우는 단계가 **래스터화(Rasterization)**입니다. 래스터화는 삼각형이 덮는 픽셀을 찾아내고, 그 자리에 채울 색·깊이·UV·법선 같은 값을 꼭짓점 정보로부터 계산합니다.

이 글에서는 삼각형 내부를 판별하는 방법에서 시작해, 프래그먼트와 픽셀이 어떻게 다른지, 정점 속성이 어떻게 보간되는지, 그리고 GPU가 프래그먼트를 묶어 처리하는 기본 단위인 2x2 Quad가 무엇인지를 차례로 살펴봅니다.

---

## 래스터화란

래스터화는 연속적인 삼각형을 이산적인 픽셀로 바꾸는 과정입니다. 삼각형은 세 꼭짓점으로 매끄럽게 정의되지만, 화면은 픽셀이 한 칸씩 나뉜 격자이기 때문입니다.

래스터화는 삼각형이 덮는 칸마다 그 자리를 칠할 데이터를 하나씩 만듭니다. 이 데이터 묶음 하나하나가 **프래그먼트(Fragment)**이며, 여기에는 색·UV·법선 같은 속성이 담깁니다. 이 속성값은 세 꼭짓점에 정의된 값을 위치에 맞게 섞어 얻습니다.

이름에 들어간 **"래스터(raster)"**도 이 격자에서 왔습니다. 가로 주사선이 위아래로 쌓여 이루는 격자를 뜻하는 말로, **CRT(Cathode Ray Tube)** 모니터가 전자빔으로 화면을 가로줄 단위로 훑어 점을 찍던 시절에서 비롯되었습니다.

파이프라인에서 래스터화는 버텍스 셰이더와 프래그먼트 셰이더 사이에 놓입니다. 앞의 버텍스 셰이더는 정점을 단위로 삼고 뒤의 프래그먼트 셰이더는 픽셀을 단위로 삼으므로, 그 사이에는 정점을 픽셀 단위로 펼치는 단계가 있어야 합니다.

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
  <!-- 프레임 버퍼 출력 -->
  <rect x="120" y="468" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="491" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임 버퍼 출력</text>
</svg>
</div>

<br>

래스터화 이전 단계의 처리량은 정점 수에 그대로 비례합니다. 메쉬의 정점이 1,000개면 버텍스 셰이더도 정점마다 한 번씩, 1,000번만 실행됩니다.

래스터화를 지나면 처리 단위가 정점에서 프래그먼트로 바뀝니다. 같은 메쉬라도 화면에서 넓게 보이면 프래그먼트가 수십만 개까지 늘어날 수 있고, 그 하나하나마다 프래그먼트 셰이더가 실행됩니다. 따라서 **렌더링 성능의 병목은 대부분 래스터화 이후 구간에** 생깁니다.

이렇게 비용이 래스터화 이후로 몰리지만, 개발자가 이 단계의 내부 동작에 직접 개입할 수는 없습니다. 셰이더 코드로 동작을 직접 정의하는 버텍스 셰이더·프래그먼트 셰이더 같은 프로그래머블 단계와 달리, 래스터화는 처리 방식이 GPU 하드웨어에 고정된 **고정 기능(Fixed-Function)** 단계이기 때문입니다.

---

## 삼각형 내부 판별

래스터화의 첫 작업은 화면 격자의 각 픽셀 위치가 삼각형 안에 포함되는지 판별하는 것입니다.

세 꼭짓점이 화면 좌표 (x0, y0), (x1, y1), (x2, y2)로 주어지면 GPU는 각 픽셀 위치를 검사합니다. 픽셀은 면적을 가진 사각 영역이지만, 기본 판별에서는 픽셀 중심 좌표 (px, py)를 대표점으로 사용합니다.

이 판별에는 Edge Function과 무게중심 좌표가 사용됩니다. Edge Function은 점이 삼각형의 각 변에서 안쪽에 있는지 부호로 판별하고, 무게중심 좌표는 같은 계산을 정점 속성 보간에 사용할 가중치로 확장합니다.

### Edge Function 방식

내부 판별에 널리 쓰이는 방식이 **Edge Function(변 함수)**입니다. 삼각형의 세 변을 하나씩 기준으로 삼아, 검사할 점이 그 변의 안쪽에 있는지 바깥쪽에 있는지 판별합니다. 세 변에서 모두 안쪽이면 그 점은 삼각형 내부이고, 한 변에서라도 바깥쪽이면 외부입니다.

한 변에서 점이 어느 쪽에 있는지는 **2D 외적(Cross Product)**으로 구합니다. 3D 외적이 두 벡터에 수직인 새 벡터를 반환하는 것과 달리, 2D 외적은 두 벡터의 방향 관계를 스칼라 값 하나로 나타냅니다. 벡터 (ax, ay)와 (bx, by)의 2D 외적은 `ax * by - ay * bx`이고, 이 값이 양수이면 (bx, by)가 (ax, ay)의 왼쪽에, 음수이면 오른쪽에 놓입니다.

이렇게 부호 하나만으로 점이 변의 왼쪽인지 오른쪽인지 알 수 있습니다. 다만 그 왼쪽·오른쪽이 삼각형의 안쪽인지 바깥쪽인지는, 세 정점을 도는 순서, 즉 앞면을 어느 방향으로 정의하느냐에 따라 달라집니다.

OpenGL과 Vulkan은 **반시계 방향(Counter-Clockwise, CCW)**을, DirectX와 Metal은 **시계 방향(Clockwise, CW)**을 앞면의 기본 정점 순서로 삼습니다. 이 글에서는 반시계 방향을 기준으로 설명합니다.

GPU는 이 정점 순서를 래스터화 직전의 프리미티브 조립 단계에서 확인합니다. 세 정점이 이루는 **부호 있는 넓이(signed area)**의 부호로 삼각형이 어느 방향으로 도는지 가려내고, 앞면과 반대로 도는 삼각형은 뒷면으로 보아 컬링(Back-Face Culling)으로 래스터화에서 제외하기도 합니다.

반시계 방향으로 도는 삼각형에서는 각 변을 따라갈 때 내부가 변의 왼쪽에 옵니다. 따라서 변의 시작점 A에서 끝점 B로 가는 벡터 AB와, 같은 A에서 점 P로 가는 벡터 AP의 외적이 양수이면 P는 변의 왼쪽, 곧 내부에 있습니다. 음수이면 바깥으로 벗어나고, 0이면 변 위에 정확히 걸칩니다.

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

Edge Function은 픽셀 하나하나를 서로 독립적으로 판별합니다. 한 픽셀의 결과가 다른 픽셀에 영향을 주지 않으므로, GPU는 수많은 픽셀을 **병렬로** 검사할 수 있습니다.

> 수백 개의 스레드가 같은 명령어를 동시에 돌리는 GPU의 SIMT 실행 모델은 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서 자세히 다룹니다. Edge Function의 픽셀별 독립 판별은 이 모델에 자연스럽게 들어맞습니다.

다만 검사 대상 픽셀을 줄이지 않으면 비용이 커집니다. 삼각형마다 화면 전체를 검사한다면 1920×1080 해상도에서 약 207만 개의 픽셀을 평가해야 하지만, 실제 삼각형이 덮는 영역은 그중 일부에 불과합니다.

이를 줄이기 위해 GPU는 먼저 **바운딩 박스(Bounding Box)**를 구합니다. 삼각형 세 꼭짓점의 x, y 최솟값과 최댓값으로 삼각형을 감싸는 사각형을 만들고, 그 안의 픽셀에 대해서만 Edge Function을 평가합니다. 바운딩 박스 밖의 픽셀은 삼각형에 포함될 수 없으므로 검사하지 않습니다.

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

앞에서 구한 세 Edge Function 값 E01, E12, E20은 점의 안팎을 판별하는 데만 쓰이지 않습니다. 각 값은 한 변과 점 P가 이루는 부분 삼각형의 부호 있는 넓이, 정확히는 그 2배와 같습니다. P가 움직이면 이 넓이도 함께 달라지므로, 세 값은 P가 삼각형 안 어디에 있는지까지 나타냅니다.

세 부분 삼각형의 넓이를 더하면 원래 삼각형의 전체 넓이가 됩니다. 그래서 각 값을 전체 넓이로 나누면 합이 1인 세 비율, 곧 **무게중심 좌표(Barycentric Coordinates)**를 얻습니다.

무게중심 좌표는 보통 (u, v, w)로 적으며, 세 값은 점 P가 각 꼭짓점에 얼마나 가까운지를 나타냅니다. P가 한 꼭짓점에 다가갈수록 그 꼭짓점의 값은 1에, 맞은편 변에 다가갈수록 0에 가까워지고, 결국 P는 세 꼭짓점을 (u, v, w)만큼 섞은 위치가 됩니다.

어떤 값이 어떤 꼭짓점의 가중치가 되는지는 그 변의 맞은편 꼭짓점으로 정해집니다. 예를 들어 변 V1→V2에서 구한 E12는 그 변의 맞은편인 V0의 가중치가 되며, 나머지 두 값도 같은 원리로 짝지어집니다.

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

이 가중치는 점의 위치를 나타내는 데서 그치지 않습니다. 세 꼭짓점에 정의된 색·UV·법선 같은 속성을 (u, v, w)로 섞으면 삼각형 내부 각 위치의 속성을 얻을 수 있고, 래스터화는 이렇게 채운 속성으로 각 픽셀 자리의 **프래그먼트**를 만듭니다. 가중치로 속성을 섞는 보간 과정은 뒤의 보간 절에서 자세히 다룹니다.

---

## 프래그먼트 vs 픽셀

래스터화는 픽셀 위치마다 프래그먼트를 만듭니다. 이름이 비슷해 프래그먼트를 화면의 픽셀과 같은 것으로 여기기 쉽지만, 둘은 서로 다른 대상입니다.

**픽셀(Pixel)**은 화면에 실제로 찍히는 최종 출력 단위입니다. 1920×1080 해상도라면 화면은 약 207만 개의 점으로 나뉘고, 그 점 하나가 픽셀 하나입니다. 픽셀에 담기는 색은 프레임 버퍼에 기록되어 화면에 그대로 표시됩니다.

반면 **프래그먼트(Fragment)**는 그 픽셀 자리를 채울 **후보**일 뿐입니다. 한 프래그먼트는 그 자리에 들어갈 색·깊이·텍스처 좌표(UV)·법선 벡터 같은 속성을 담고 있지만, 아직 최종 출력은 아닙니다. 깊이 테스트, 스텐실 테스트, 블렌딩 같은 후속 단계를 통과한 뒤에야 비로소 픽셀로 남습니다.

이 단계의 셰이더를 "프래그먼트 셰이더"라고 부르는 것도 다루는 대상이 확정된 픽셀이 아니라 아직 후보인 프래그먼트이기 때문입니다. DirectX는 같은 단계를 픽셀 셰이더(Pixel Shader)라고 부르지만, 처리하는 데이터는 똑같은 픽셀 후보입니다.

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

한 픽셀 위치를 여러 삼각형이 겹쳐 덮으면, 그 자리에는 삼각형 수만큼 프래그먼트가 생깁니다. 이 후보들은 깊이 테스트(Depth Test)를 거쳐, 카메라에 가장 가까운 하나만 최종 픽셀로 남고 나머지는 폐기됩니다.

이렇게 한 픽셀 자리를 여러 삼각형이 거듭 덮는 것을 **오버드로우(Overdraw)**라고 합니다. 오버드로우가 있으면 결국 가려져 폐기될 프래그먼트에도 프래그먼트 셰이더가 실행될 수 있고, 화면에 보이지도 않을 색을 계산한 만큼 비용이 낭비됩니다.

> 오버드로우와 Early-Z의 비용은 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서 자세히 다룹니다.

---

## 보간 (Interpolation)

프래그먼트 셰이더는 프래그먼트마다 그 자리의 색·UV·법선 같은 속성을 입력으로 받습니다. 하지만 이 속성은 버텍스 셰이더가 정점마다 내보낸 값이라, 삼각형의 세 정점에만 있을 뿐 그 사이의 프래그먼트 자리에는 정해진 값이 없습니다. 이 빈자리를 채우는 과정이 **보간(Interpolation)**입니다.

### 무게중심 좌표를 이용한 보간

삼각형 내부 판별에서 프래그먼트마다 구해 둔 무게중심 좌표 (u, v, w)가 그대로 보간의 가중치가 됩니다. 세 꼭짓점의 속성 값 A0, A1, A2에 이 가중치를 곱해 더한 것이 프래그먼트 자리의 속성입니다.

$$A(P) = u \cdot A_0 + v \cdot A_1 + w \cdot A_2$$

가중치의 합이 1이라, 이렇게 보간한 값은 늘 세 꼭짓점 값 사이에 놓입니다. 예를 들어 세 꼭짓점의 UV가 각각 (0.0, 1.0), (1.0, 0.0), (0.5, 0.5)이고 어떤 프래그먼트의 무게중심 좌표가 (0.3, 0.4, 0.3)이라면, 세 UV를 이 비율로 섞은 값이 그 프래그먼트의 UV가 됩니다.

$$\mathrm{UV}_P = 0.3\,(0.0,\; 1.0) + 0.4\,(1.0,\; 0.0) + 0.3\,(0.5,\; 0.5) = (0.55,\; 0.45)$$

UV뿐 아니라 색, 법선, 직접 정의한 속성도 정점마다 값이 있다면 같은 방식으로 보간됩니다. 가령 세 꼭짓점이 빨강·초록·파랑이면, 내부의 한 점에서는 무게중심 좌표의 비율대로 세 색이 섞입니다.

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

무게중심 보간이 쓰는 가중치 (u, v, w)는 세 꼭짓점의 2D 화면 좌표만으로 구해집니다. 이 가중치로 올바른 값을 얻으려면, 화면에서 잰 거리가 3D 공간의 거리에 그대로 비례해야 합니다. 
다시 말해 화면에서 두 꼭짓점의 한가운데에 찍힌 픽셀은 3D 표면에서도 정확히 중간 지점이어야 합니다. 이 조건은 세 꼭짓점의 깊이가 모두 같을 때, 곧 표면이 화면과 나란할 때만 성립합니다.

원근 투영에서는 카메라에 가까운 영역이 화면에 넓게 펼쳐지고, 먼 영역은 좁게 압축됩니다. 따라서 깊이가 다른 두 꼭짓점을 잇는 선에서는, 화면에서 같은 간격으로 떨어져 보이는 두 지점이라도 3D 공간에서의 실제 간격이 달라집니다. 이런 선에서 화면상 한가운데에 있는 픽셀은 3D 공간에서 가까운 꼭짓점 쪽으로 치우쳐 있습니다.

화면 좌표만으로 보간하면 이 치우침을 반영하지 못합니다. 한가운데 픽셀에는 가까운 꼭짓점의 값이 더 많이 담겨야 하지만, 단순 보간은 두 꼭짓점의 값을 절반씩 섞습니다. 이렇게 어긋난 값이 표면 전체에 퍼지면 눈에 띄는 왜곡으로 이어집니다. 바닥 타일이나 벽 텍스처가 원근 방향으로 부자연스럽게 늘어나거나 찌그러져 보이곤 합니다.

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
  <text x="470" y="74" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">✗ 왜곡</text>
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
  <text x="470" y="140" font-family="sans-serif" font-size="9" fill="currentColor" font-weight="bold">✓ 정확</text>
  <!-- 결론 -->
  <text x="260" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 단순 보간은 텍스처를 균등하게 배분하여 원근감이 사라진다</text>
  <text x="260" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 원근 보정은 깊이(w)를 반영하여 가까운 쪽을 크게, 먼 쪽을 작게 보간한다</text>
</svg>
</div>

<br>

이 왜곡은 보간에 깊이를 반영하면 바로잡을 수 있습니다. 어떤 값을 보간하느냐가 관건입니다. 무게중심 보간은 화면 좌표를 따라 선형으로 변하는 값만 정확히 재현하는데, 원근이 적용된 속성값 A는 화면을 따라 그렇게 변하지 않습니다. 그래서 A를 화면 좌표만으로 보간하면 값이 어긋납니다.

대신 화면 좌표에 선형으로 변하는 다른 양을 보간하면 됩니다. 속성값 A를 깊이 w(클립 공간 좌표의 네 번째 성분)로 나눈 A/w와, 깊이의 역수인 1/w가 바로 그런 양입니다. 이 둘은 무게중심 좌표로 보간해도 각 픽셀에서 정확한 값이 나오고, 보간한 A/w를 보간한 1/w로 나누면 w가 상쇄되어 원래의 A가 복원됩니다.

무게중심 좌표를 깊이 w와 구분해 λ로 적으면, 이 보정은 단순합 $\lambda_0 A_0 + \lambda_1 A_1 + \lambda_2 A_2$가 아니라 다음과 같습니다.

$$A(P) = \frac{\lambda_0 \frac{A_0}{w_0} + \lambda_1 \frac{A_1}{w_1} + \lambda_2 \frac{A_2}{w_2}}{\lambda_0 \frac{1}{w_0} + \lambda_1 \frac{1}{w_1} + \lambda_2 \frac{1}{w_2}}$$

<br>

일반적인 셰이더에서는 이 계산을 직접 구현하지 않습니다. 버텍스 셰이더가 w를 포함한 클립 공간 좌표를 출력하면, 래스터화 하드웨어가 그 w로 속성 보간에 원근 보정을 자동으로 적용합니다.

다만 원근 보정이 늘 옳은 것은 아닙니다. 이 보정은 보간하는 값이 3D 표면에 속한 속성, 즉 표면 위 한 점에 대해 정의되어 표면을 따라 변하는 값이라고 전제합니다. UV나 법선이 여기에 해당하며, 이런 속성은 원근 보정을 거쳐야 표면 위에서 올바르게 분포합니다.

반대로 어떤 값은 표면이 아니라 화면을 기준으로 변해야 합니다. 깊이와 무관하게 화면에서 일정한 굵기로 그려야 하는 외곽선이 그렇습니다. 이런 값에까지 원근 보정을 적용하면, 화면 좌표를 따라 곧게 이어져야 할 분포가 깊이에 끌려 가까운 꼭짓점 쪽으로 쏠리고, 오히려 화면에서 어긋나 보입니다. 따라서 HLSL에서는 이런 변수에 `noperspective` 수식어를 붙여, 원근 보정 없이 화면 좌표를 따라 그대로 보간하도록 지정합니다.

---

## 2x2 Quad 실행

보간까지 끝나면 각 프래그먼트는 색·UV·법선처럼 프래그먼트 셰이더가 사용할 속성을 모두 갖춥니다. 그런데 GPU는 이 프래그먼트를 하나씩 따로 셰이더에 넘기지 않습니다. 화면에서 가로·세로로 맞닿은 2x2 픽셀을 하나의 **Quad**로 묶어, 네 프래그먼트를 한꺼번에 실행합니다.

프래그먼트는 저마다 화면 위의 독립된 자리이므로, 한 자리의 계산은 본래 다른 자리와 무관하게 따로 진행할 수 있습니다. 그런데도 GPU가 네 프래그먼트를 한 Quad로 묶는 이유는, 프래그먼트 셰이더가 한 점의 색을 정하는 데 그 점 하나의 값만이 아니라 이웃한 점과의 차이까지 알아야 하기 때문입니다. 차이는 두 점을 맞대어야 나오는 값이라, 프래그먼트 하나를 따로 떼어 놓으면 구할 수 없습니다.

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

프래그먼트 셰이더가 이웃의 값까지 필요로 하는 가장 흔한 경우는 텍스처를 읽어 들일 때입니다. 같은 텍스처라도 화면에 크게 보일 때와 작게 보일 때 읽는 방식이 서로 달라야 합니다.

텍스처를 입힌 표면은 카메라에서 멀어질수록 화면에서 작게 보입니다. 표면이 작아지면 화면의 한 픽셀이 텍스처의 넓은 영역을 한꺼번에 담게 되는데, 이때 원본 텍스처를 그대로 읽으면 픽셀마다 그 영역의 어느 한 점만 뽑혀 표면에 거친 노이즈가 나타납니다. 이를 피하려고 GPU는 표면이 작아진 만큼 미리 줄여 둔 텍스처를 대신 읽습니다. 이렇게 원본을 절반씩 줄여 가며 쌓은 사본 묶음이 **밉맵(Mipmap)**이며, 가까워서 크게 보이는 표면은 높은 해상도 사본을, 멀어서 작게 보이는 표면은 낮은 해상도 사본을 읽습니다.

남는 문제는 표면이 얼마나 작아졌는지, 곧 어느 레벨을 읽어야 하는지를 GPU가 어떻게 아는가입니다. GPU는 이 크기 변화를 이웃한 두 픽셀의 UV 차이로 판단합니다. 화면에서 픽셀 하나를 옆으로 옮겼을 때 UV가 크게 달라지면, 그 픽셀은 텍스처를 이루는 최소 칸인 **텍셀(Texel)** 여러 개에 걸쳐 있다는 뜻이라 낮은 해상도 레벨이 알맞습니다. 반대로 UV가 조금만 달라지면 한두 텍셀만 덮으므로 높은 해상도 레벨이 알맞습니다. 이때 UV는 화면의 가로·세로 두 방향으로 따로 변하니 변화량도 방향마다 따로 재며, 한 방향에 대한 변화량이 UV의 **편미분값(partial derivative)**입니다. 이처럼 이웃 프래그먼트와 값을 맞대어 얻는 차이를 통틀어 **미분값(derivative)**이라고 합니다.

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

한 프래그먼트가 편미분값을 구하려면 옆 프래그먼트의 UV를 읽어 와야 합니다. 그런데 이 UV를 언제 읽느냐가 중요합니다. 프래그먼트 셰이더는 색을 한 번의 연산으로 정하는 것이 아니라 여러 명령어를 차례로 실행하는 작은 프로그램이고, 편미분값은 이 명령어들의 처음이 아니라 중간의 어느 지점에서 계산되기 때문입니다. 따라서 한 프래그먼트가 그 지점에 이르러 옆 UV를 읽을 때, 옆 프래그먼트도 같은 지점까지 진행해 자신의 UV를 이미 구해 두어야 합니다.

문제는 네 프래그먼트가 같은 코드를 실행하더라도 본래 서로 독립적으로 진행되는 계산이라는 점입니다. 만약 저마다 다른 속도로 실행된다면 프로그램 안에서 진행한 위치가 서로 어긋나므로, 한 프래그먼트가 편미분 지점에 이르렀을 때 옆 프래그먼트는 아직 그 지점에 도달하지 못했을 수 있습니다. 이때 옆의 UV는 미처 계산되지 않았으므로, 그 값을 읽어 올 수 없습니다. GPU는 이런 어긋남을 처음부터 없애기 위해, 한 Quad의 네 프래그먼트를 각각 하나의 스레드에 배정하고, 네 스레드가 늘 같은 명령어를 같은 순간에 함께 실행하도록 합니다.

> Warp 단위 SIMT 실행은 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서 다룹니다.

네 스레드가 항상 코드의 같은 지점을 지나므로, 셰이더가 UV를 계산하는 명령어에 이르면 네 스레드의 UV가 모두 준비됩니다. 이때 한 스레드는 가로나 세로로 맞닿은 옆 스레드의 UV를 곧바로 읽어, 두 값의 차이로 편미분값을 얻습니다. 가로 방향의 차이가 `ddx()`, 세로 방향의 차이가 `ddy()`이며, `fwidth()`는 두 값의 크기를 더해 변화량을 한꺼번에 나타냅니다. 셰이더에서 이 세 함수를 호출하면 GPU는 위와 같은 방식으로 화면 공간 미분값을 계산합니다.

### 작은 삼각형의 비효율

Quad는 맞닿은 2x2 픽셀을 한 단위로 묶어 처리하므로, 삼각형이 그 안을 얼마나 채우든 네 프래그먼트가 늘 함께 실행됩니다. 삼각형이 Quad를 가득 채울 때는 네 자리가 모두 화면에 남을 픽셀이라 버릴 것이 없습니다. 그러나 삼각형이 네 자리 가운데 한두 곳만 덮으면, 삼각형 밖에 놓인 나머지 자리도 같은 묶음이라 그대로 실행됩니다.

이렇게 삼각형 밖에서 함께 실행되는 자리를 **헬퍼 프래그먼트(Helper Fragment)**라고 합니다. 화면에 남지 않을 자리인데도 셰이더를 끝까지 실행하는 이유는, 삼각형 안쪽 프래그먼트가 미분값을 구하려면 이웃 자리의 값이 있어야 하는데 그 이웃이 바로 이 바깥 자리이기 때문입니다. 헬퍼 프래그먼트도 안쪽 프래그먼트와 마찬가지로 셰이더를 실행하지만, 그렇게 얻은 색은 화면에 기록되지 않고 버려집니다.

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

버려지는 양은 삼각형이 Quad를 얼마나 채우지 못했는가에 그대로 비례합니다. 큰 삼각형은 여러 Quad에 걸쳐 있어, 안쪽 Quad는 네 자리가 모두 삼각형 안에 들고 헬퍼 프래그먼트는 경계에 걸친 가장자리 Quad에서만 생깁니다. 반면 한두 픽셀 크기의 삼각형은 어느 Quad도 제대로 채우지 못해, 네 자리에서 모두 셰이더가 실행되어도 화면에 남는 것은 한둘, 곧 효율이 25~50%에 그칩니다.

이런 작은 삼각형이 한 화면을 가득 메우면 Quad마다 생기는 낭비가 빠르게 누적됩니다. 대표적인 경우가 수십만 폴리곤짜리 고해상도 메쉬가 카메라에서 멀어져 화면에 작게 보일 때입니다. 멀어진 만큼 삼각형 하나하나가 몇 픽셀 크기로 줄어들어, 화면을 채운 거의 모든 Quad에 헬퍼 프래그먼트가 들어찹니다.

엔진의 LOD(Level of Detail) 시스템이 멀리 있는 오브젝트를 더 단순한 메쉬로 바꾸는 것도 이 때문입니다. 화면에서 작게 보일 오브젝트를 미리 삼각형이 적은 버전으로 그려 두면, Quad를 채우지 못하는 작은 삼각형이 화면을 뒤덮는 일을 막을 수 있습니다. 이 비용은 처리 자원이 한정된 모바일에서 특히 부담스럽습니다.

> 타일 기반 GPU의 Binning 비용은 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 다룹니다.

화면에 2픽셀 이하의 작은 삼각형이 빽빽한 장면이라면, 삼각형 수를 줄이는 것만으로 버텍스 단계와 프래그먼트 단계의 효율을 함께 끌어올릴 수 있습니다.

---

## 래스터화 규칙

메쉬는 작은 삼각형을 빈틈없이 이어 붙여 만든 표면이라, 이웃한 두 삼각형이 변 하나를 함께 쓰는 경계가 곳곳에 생깁니다. 래스터화는 삼각형마다 그 안에 드는 픽셀 자리를 찾아 프래그먼트를 만드는데, 픽셀 중심이 이 공유 변 위에 정확히 놓이면 두 삼각형 가운데 어느 쪽이 그 자리를 그릴지 정해야 합니다.

삼각형 내부 판별은 세 변의 Edge Function 값이 모두 0 이상인 픽셀 중심을 안쪽으로 봅니다. 이 값이 0이면 픽셀 중심이 변 위에 정확히 놓였다는 뜻이라, 0을 포함하는 이 기준은 변 위의 픽셀까지 안쪽으로 받아들입니다. 따라서 두 삼각형이 한 변을 공유하면, 그 변 위의 같은 픽셀 중심이 양쪽 삼각형에서 모두 안쪽 조건을 만족해 같은 자리에 프래그먼트가 두 번 만들어집니다.

불투명 표면에서는 같은 자리의 색이 다시 덮여도 눈에 잘 드러나지 않지만, 반투명 표면에서는 두 프래그먼트가 차례로 블렌딩됩니다. 그러면 공유 변을 따라 반투명 색이 한 번 더 합성되어, 경계가 주변보다 진하게 보입니다.

반대로 변 위의 픽셀을 양쪽 삼각형에서 모두 빼도록 기준을 바꾸면, 이번에는 어느 삼각형도 그 자리를 그리지 않아 경계를 따라 가느다란 틈이 벌어집니다. 함께 그리면 덧칠이 남고 함께 빼면 틈이 생기니, 공유 변 위의 픽셀은 두 삼각형 가운데 정확히 한쪽에서만 그려져야 합니다.

남은 문제는 그 한쪽을 어떻게 고르느냐입니다. 픽셀 중심이 공유 변 위에 있다는 사실만 보면 두 삼각형은 같은 조건에 놓입니다. 그래서 픽셀 위치만으로는 어느 쪽에 포함할지 정할 수 없습니다. 같은 변을 공유하더라도 한쪽은 포함하고 다른 쪽은 제외하도록 갈라 줄 기준이 필요합니다.

### Top-Left Rule

이 기준은 지금 처리 중인 삼각형 하나만 보고 정할 수 있어야 합니다. 래스터라이저는 삼각형을 하나씩 래스터화하므로, 한 삼각형을 검사하는 동안 그 변을 공유하는 이웃 삼각형까지 함께 비교하지 않습니다. 따라서 공유 변 위의 픽셀 중심을 넣을지 뺄지는 현재 삼각형의 정보만으로 결정되어야 합니다.

이때 사용할 수 있는 정보가 정점 순서입니다. 삼각형의 세 정점을 순서대로 이으면 세 변에도 방향이 생기며, 이 정점 순서를 와인딩(winding)이라고 합니다. 한 메쉬의 삼각형들은 같은 와인딩으로 만들어지므로, 변을 공유하는 두 삼각형은 같은 변을 서로 반대 방향으로 지납니다. 따라서 현재 삼각형의 정점 순서만 보아도 그 변이 어느 방향으로 놓인 경계인지 알 수 있습니다.

Top-Left Rule은 이 방향을 기준으로 경계를 분류합니다. 아래로 내려가는 변은 삼각형의 왼쪽 경계를 이루는 왼쪽 변(left edge)으로 보고, 수평이면서 왼쪽을 향하는 변은 위쪽 경계를 이루는 위쪽 변(top edge)으로 봅니다. 픽셀 중심이 변 위에 정확히 놓이면, 왼쪽 변과 위쪽 변에서는 삼각형 안쪽에 포함하고 오른쪽 변과 아래쪽 변에서는 제외합니다.

공유 변에서는 이 분류가 두 삼각형에서 서로 다르게 나옵니다. 한쪽 삼각형이 그 변을 왼쪽 변이나 위쪽 변으로 지나면, 맞은편 삼각형은 같은 선분을 반대 방향으로 지나므로 오른쪽 변이나 아래쪽 변으로 봅니다. 그래서 변 위의 픽셀 중심은 한쪽 삼각형에만 포함됩니다. 같은 자리에 프래그먼트가 두 번 생기지도 않고, 어느 쪽에서도 빠져 틈이 생기지도 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Top-Left Rule</text>
  <text x="240" y="35" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">두 삼각형이 변을 공유하는 경우</text>
  <!-- Triangle A (공유 변 제외) -->
  <polygon points="80,50 80,170 380,50" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="82" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">A</text>
  <!-- Triangle B (공유 변 포함) -->
  <polygon points="380,50 80,170 380,170" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="152" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" font-weight="bold">B</text>
  <!-- 공유 변: A의 와인딩 방향 (↗ 위로) — 제외, 점선 화살표 -->
  <line x1="106" y1="153" x2="337" y2="60" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.4"/>
  <polygon points="345,58 337,65 334,58" fill="currentColor" opacity="0.4"/>
  <text x="260" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">↗ 제외</text>
  <!-- 공유 변: B의 와인딩 방향 (↙ 아래로) — left edge, 포함, 실선 화살표 -->
  <line x1="354" y1="67" x2="123" y2="160" stroke="currentColor" stroke-width="2.5"/>
  <polygon points="115,162 123,155 126,162" fill="currentColor"/>
  <text x="200" y="145" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">↙ left edge → 포함</text>
  <!-- 결론 -->
  <text x="240" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 같은 변이라도 진행 방향이 반대이므로, 한쪽만 포함</text>
  <text x="240" y="214" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">빈 틈(gap)이나 이중 렌더링(double draw) 방지</text>
</svg>
</div>

<br>

이 규칙은 그래픽스 API에서도 정해진 동작으로 다룹니다. DirectX와 Metal, Vulkan은 Top-Left Rule을 명세에 적어 두고, OpenGL은 세부 처리를 구현 정의(implementation-defined)로 남기지만 실제 구현은 대체로 같은 방식으로 처리합니다.

---

## 래스터화의 전체 흐름 정리

앞에서는 래스터화 안에서 일어나는 일을 하나씩 나누어 보았습니다. 이제 그 단계들을 한 흐름으로 이어 보면, 세 꼭짓점이 어떻게 픽셀 위치의 프래그먼트로 바뀌는지 정리할 수 있습니다.

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

래스터화는 기하 단계에서 넘어온 세 꼭짓점의 2D 좌표와 속성에서 시작합니다. 먼저 세 꼭짓점을 감싸는 바운딩 박스를 구해 검사할 영역을 좁히고, 그 안의 픽셀 위치마다 Edge Function으로 삼각형 안쪽인지 확인합니다.

안쪽으로 판정된 위치에서는 무게중심 좌표 (u, v, w)를 구합니다. 이 값은 세 꼭짓점의 속성을 섞는 가중치가 되고, 래스터화는 이를 이용해 UV, 법선, 색상을 픽셀 위치에 맞게 보간합니다. 원근 투영으로 생기는 깊이 차이는 이 과정에서 함께 보정됩니다.

보간된 속성은 프래그먼트에 담깁니다. GPU는 이 프래그먼트들을 2x2 Quad로 묶어 화면 공간 미분을 구할 수 있게 만들고, 삼각형 밖에 걸친 자리에는 필요한 경우 헬퍼 프래그먼트를 더합니다. 이렇게 만들어진 Quad가 프래그먼트 셰이더의 실행 단위가 됩니다.

따라서 래스터화는 기하 단계와 픽셀 셰이딩 단계를 잇는 중간 단계입니다. 여기서 프래그먼트의 수와 화면 분포가 정해지므로, 뒤에서 실행될 프래그먼트 셰이더의 비용도 이 단계의 결과에 따라 달라집니다.

---

## 마무리

이번 글에서는 화면 좌표로 변환된 삼각형이 프래그먼트로 바뀌어 프래그먼트 셰이더에 전달되기까지, 래스터화 단계에서 일어나는 일을 정리했습니다. 핵심은 다음과 같습니다.

- **래스터화**는 연속 좌표로 정의된 삼각형을 픽셀 위치별 프래그먼트로 변환하는 고정 기능 단계입니다.
- **Edge Function**은 점이 삼각형의 각 변에서 어느 쪽에 있는지 부호로 판별합니다. 세 변 모두에서 안쪽으로 판정된 픽셀 위치에 프래그먼트가 생성됩니다.
- **무게중심 좌표**는 삼각형 내부의 한 점을 세 꼭짓점에 대한 가중치로 표현합니다.
- **프래그먼트**는 픽셀 자리를 채울 후보입니다. 같은 픽셀 위치에 프래그먼트가 여러 개 생길 수 있고, 후속 테스트를 통과한 것만 프레임 버퍼에 남습니다.
- **보간**은 무게중심 좌표를 가중치로 세 꼭짓점의 속성을 섞어 프래그먼트 자리의 값을 채웁니다. 원근 투영에서는 1/w를 이용한 원근 보정 보간이 필요합니다.
- **2x2 Quad**는 GPU가 프래그먼트 네 개를 함께 실행하는 단위입니다. 텍스처 밉맵 선택에 필요한 미분값을 얻기 위해 사용되며, 작은 삼각형에서는 헬퍼 프래그먼트 때문에 효율이 떨어질 수 있습니다.
- **Top-Left Rule**은 공유 변 위의 픽셀을 두 삼각형 가운데 한쪽에만 포함해, 같은 자리가 두 번 그려지거나 빠지는 일을 막는 경계 규칙입니다.

정리하면, 래스터화는 고정 기능 단계라 개발자가 내부 알고리즘을 직접 바꿀 수 없으므로, 최적화는 LOD로 삼각형 수를 줄이는 것처럼 이 단계로 넘어오는 입력을 조절하는 방식으로 이루어집니다. 작은 삼각형과 오버드로우, 넓은 화면 점유 면적이 왜 비용으로 이어지는지 알면, 어떤 입력을 조절해야 할지도 판단할 수 있습니다.

래스터화가 만든 프래그먼트는 프래그먼트 셰이더를 거쳐 색을 얻지만, 그 색이 곧바로 픽셀에 놓이지는 않습니다. 어떤 프래그먼트를 남길지, 어느 영역에만 기록할지, 기존 색과 어떻게 섞을지는 다음 단계인 출력 병합에서 결정됩니다.

[다음 글](/dev/unity/RasterPipeline-2/)에서는 프레임 버퍼와 깊이·스텐실 버퍼, 블렌딩, 그리고 렌더 타겟과 MRT를 살펴봅니다. 프래그먼트 셰이더의 비용 구조와 이를 줄이는 방법은 [셰이더 최적화 (1)](/dev/unity/ShaderOptimization-1/)에서 이어집니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)

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
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
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
