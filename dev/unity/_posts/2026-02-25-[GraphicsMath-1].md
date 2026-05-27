---
layout: single
title: "그래픽스 수학 (1) - 벡터와 벡터 연산 - soo:bak"
date: "2026-02-25 21:03:00 +0900"
description: 벡터의 개념, 덧셈과 뺄셈, 크기와 정규화, 내적, 외적, Unity의 Vector3를 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 수학
  - 벡터
  - 모바일
---

## 3D 그래픽스에서 수학이 필요한 이유

Unity에서 위치를 바꾸거나 카메라를 회전시키는 코드는 대부분 API 호출로 끝납니다. 하지만 그 API 안에서는 좌표, 벡터, 행렬, 투영 같은 수학 연산이 계속 실행됩니다.

캐릭터의 위치는 좌표로 저장되고, 바라보는 방향은 방향 벡터로 표현됩니다. 이동은 위치에 이동량을 더하는 연산이고, 조명 밝기는 표면 방향과 빛 방향의 관계로 계산됩니다. 오브젝트의 회전과 3D 공간을 2D 화면으로 옮기는 과정에는 행렬 연산이 들어갑니다.

[렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 법선 벡터가 빛 계산에 사용된다고 했고, [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)에서 셰이더가 정점 변환과 조명 계산을 수행한다고 했습니다.

이때 등장하는 벡터, 행렬, 좌표 변환, 투영을 이해해야 렌더링 파이프라인과 셰이더 코드가 어떤 값을 다루는지 따라갈 수 있습니다.

<br>

Unity API가 많은 계산을 대신 처리하므로, 수학을 깊게 몰라도 게임을 만들 수는 있습니다.

다만 성능 병목을 분석하거나 셰이더를 직접 수정해야 할 때는 이야기가 달라집니다. 내부에서 어떤 벡터를 만들고 어떤 값을 비교하는지 알아야 불필요한 계산을 줄이거나 잘못된 좌표 변환을 찾을 수 있기 때문입니다.

이 시리즈에서는 렌더링과 셰이더를 읽는 데 필요한 그래픽스 수학을 다룹니다. 첫 글의 주제는 벡터입니다. 벡터가 위치, 방향, 이동량을 어떻게 표현하는지 확인한 뒤, 덧셈, 뺄셈, 정규화, 내적, 외적이 Unity와 렌더링에서 어떤 의미를 갖는지 연결합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 580 90" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <rect x="5" y="8" width="110" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="60" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">벡터</text>
  <text fill="currentColor" x="60" y="44" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">위치 · 방향 · 속도</text>
  <text fill="currentColor" x="60" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(현재 글)</text>
  <line x1="115" y1="34" x2="147" y2="34" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="149,34 143,30 143,38" fill="currentColor"/>
  <rect x="152" y="8" width="110" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="207" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">행렬</text>
  <text fill="currentColor" x="207" y="44" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">이동 · 회전 · 스케일</text>
  <text fill="currentColor" x="207" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(Part 2)</text>
  <line x1="262" y1="34" x2="294" y2="34" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="296,34 290,30 290,38" fill="currentColor"/>
  <rect x="299" y="8" width="120" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="359" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">좌표 공간</text>
  <text fill="currentColor" x="359" y="44" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">오브젝트 · 월드 · 뷰 · 클립</text>
  <text fill="currentColor" x="359" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(Part 3)</text>
  <line x1="419" y1="34" x2="451" y2="34" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="453,34 447,30 447,38" fill="currentColor"/>
  <rect x="456" y="8" width="110" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="511" y="28" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">투영</text>
  <text fill="currentColor" x="511" y="44" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">원근 · 직교</text>
  <text fill="currentColor" x="511" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">(Part 4)</text>
</svg>
</div>

---

## 벡터란 무엇인가

게임에서 위치를 다룰 때는 숫자 하나만으로는 충분하지 않습니다. 캐릭터가 얼마나 이동했는지도 중요하지만, 어느 방향으로 이동했는지도 함께 필요하기 때문입니다.

숫자 하나로 표현되는 값은 **스칼라(Scalar)**입니다. 온도 25도, 질량 5kg, 속력 60km/h처럼 크기만 있는 값이 여기에 해당합니다. 스칼라는 값의 크기를 나타낼 수 있지만, 방향은 담지 않습니다.

반대로 **벡터(Vector)**는 크기와 방향을 함께 담습니다. "북쪽으로 60km/h"는 얼마나 빠른지와 어느 쪽으로 움직이는지를 함께 나타내고, "오른쪽으로 3미터 이동"도 이동 거리와 방향을 함께 나타냅니다.

그래서 벡터는 좌표축별 성분으로 표현합니다. 2D 벡터는 x, y 두 성분을 사용하고, 3D 벡터는 x, y, z 세 성분을 사용합니다. Unity의 `Vector3`도 이 세 성분으로 위치, 방향, 이동량을 표현합니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 540 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 2D 벡터 -->
  <text fill="currentColor" x="125" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">2D 벡터</text>
  <line x1="50" y1="180" x2="50" y2="35" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="50,32 46,40 54,40" fill="currentColor"/>
  <text fill="currentColor" x="38" y="42" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <line x1="50" y1="180" x2="225" y2="180" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="228,180 220,176 220,184" fill="currentColor"/>
  <text fill="currentColor" x="232" y="193" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <line x1="100" y1="40" x2="100" y2="180" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="150" y1="40" x2="150" y2="180" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="200" y1="40" x2="200" y2="180" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="50" y1="130" x2="220" y2="130" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="50" y1="80" x2="220" y2="80" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <text fill="currentColor" x="100" y="195" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="150" y="195" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <text fill="currentColor" x="200" y="195" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">3</text>
  <text fill="currentColor" x="42" y="134" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="42" y="84" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <line x1="50" y1="180" x2="196" y2="83" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="200,80 195,87 192,81" fill="currentColor"/>
  <circle cx="200" cy="80" r="3" fill="currentColor"/>
  <text fill="currentColor" x="168" y="68" font-size="11" font-family="sans-serif" font-weight="bold">v = (3, 2)</text>
  <!-- 3D 벡터 -->
  <!-- 단위벡터: x̂=(35,0), ŷ=(0,-38), ẑ=(-13,10). 원점 O=(345,175) -->
  <!-- v=(3,2,4) → P = O + 3x̂ + 2ŷ + 4ẑ = (398, 139) -->
  <!-- 바닥 투영 F = O + 3x̂ + 4ẑ = (398, 215) -->
  <text fill="currentColor" x="400" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">3D 벡터</text>
  <!-- 바닥 그리드 (xz 평면) — z 방향 선 (x=1,2,3) -->
  <line x1="380" y1="175" x2="328" y2="215" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="415" y1="175" x2="363" y2="215" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="450" y1="175" x2="398" y2="215" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <!-- 바닥 그리드 (xz 평면) — x 방향 선 (z=1,2,3,4) -->
  <line x1="332" y1="185" x2="437" y2="185" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="319" y1="195" x2="424" y2="195" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="306" y1="205" x2="411" y2="205" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <line x1="293" y1="215" x2="398" y2="215" stroke="currentColor" stroke-width="0.3" opacity="0.12"/>
  <!-- Y축 -->
  <line x1="345" y1="175" x2="345" y2="38" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="345,35 341,43 349,43" fill="currentColor"/>
  <text fill="currentColor" x="333" y="45" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <!-- X축 -->
  <line x1="345" y1="175" x2="498" y2="175" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="501,175 493,171 493,179" fill="currentColor"/>
  <text fill="currentColor" x="505" y="188" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <!-- Z축 -->
  <line x1="345" y1="175" x2="293" y2="215" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="287,220 291,212 295,218" fill="currentColor"/>
  <text fill="currentColor" x="274" y="225" font-size="11" font-family="sans-serif" font-style="italic">z</text>
  <!-- 축 눈금 -->
  <text fill="currentColor" x="380" y="189" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="415" y="189" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <text fill="currentColor" x="450" y="189" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">3</text>
  <text fill="currentColor" x="337" y="141" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="337" y="103" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <text fill="currentColor" x="285" y="220" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">4</text>
  <!-- 투영선 (점선) — x=3 지점에서 z 방향 -->
  <line x1="450" y1="175" x2="398" y2="215" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 투영선 (점선) — z=4 지점에서 x 방향 -->
  <line x1="293" y1="215" x2="398" y2="215" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 투영선 (점선) — 바닥 투영점 F에서 수직으로 y=2 -->
  <line x1="398" y1="215" x2="398" y2="141" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>
  <circle cx="398" cy="215" r="2.5" fill="currentColor" fill-opacity="0.2"/>
  <!-- 투영선 (점선) — Oz에서 Oyz로 수직 (z=4 면의 왼쪽 변) -->
  <line x1="293" y1="215" x2="293" y2="139" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 투영선 (점선) — P에서 Oyz로 (-x 방향, yz 평면) -->
  <line x1="398" y1="139" x2="293" y2="139" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 투영선 (점선) — Oyz에서 y축으로 (-z 방향) -->
  <line x1="293" y1="139" x2="345" y2="99" stroke="currentColor" stroke-width="0.7" stroke-dasharray="4,3" opacity="0.3"/>
  <circle cx="293" cy="139" r="2" fill="currentColor" fill-opacity="0.15"/>
  <circle cx="345" cy="99" r="2.5" fill="currentColor" fill-opacity="0.2"/>
  <!-- 벡터 v = (3, 2, 4) -->
  <line x1="345" y1="175" x2="394" y2="142" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="398,139 389,141 393,146" fill="currentColor"/>
  <circle cx="398" cy="139" r="3" fill="currentColor"/>
  <text fill="currentColor" x="410" y="132" font-size="11" font-family="sans-serif" font-weight="bold">v = (3, 2, 4)</text>
</svg>
</div>

<br>

같은 x, y, z 성분이라도 어떤 값으로 쓰느냐에 따라 위치, 방향, 속도처럼 다른 의미를 가집니다.

**위치 벡터(Position Vector)**로 사용할 때는 공간의 한 점을 가리킵니다. 캐릭터 위치가 (5, 0, 3)이라면, 원점에서 x 방향으로 5, y 방향으로 0, z 방향으로 3만큼 떨어진 지점에 있다는 뜻입니다.

**방향 벡터(Direction Vector)**로 사용할 때는 어느 쪽을 향하는지만 나타냅니다. 캐릭터의 전방 방향이나 표면의 법선 방향처럼 위치보다 방향 자체가 중요한 값입니다. 이런 경우에는 거리 정보가 섞이지 않도록 크기를 1로 맞춘 단위 벡터를 주로 사용합니다.

**속도 벡터(Velocity Vector)**로 사용할 때는 방향에 빠르기까지 포함됩니다. (2, 0, -1)이라는 속도 벡터는 1초 동안 x 방향으로 2, z 방향으로 -1만큼 이동한다는 뜻입니다.

---

## 벡터의 기본 연산

벡터를 실제 코드에서 사용하려면 위치를 더하고, 두 위치의 차이를 구하고, 방향에 속력을 곱하는 계산이 필요합니다. 방향 벡터의 길이를 1로 맞출 때는 벡터를 자신의 크기로 나누기도 합니다. 이때 사용하는 기본 연산이 덧셈, 뺄셈, 스칼라 곱과 스칼라 나눗셈입니다.

---

### 덧셈

두 벡터를 더할 때는 같은 자리의 성분끼리 더합니다.

$$
\mathbf{a} = (2, \; 1), \quad \mathbf{b} = (1, \; 3)
$$

$$
\mathbf{a} + \mathbf{b} = (2{+}1, \; 1{+}3) = (3, \; 4)
$$

벡터 덧셈은 이동량을 차례대로 적용하는 것과 같습니다. 먼저 벡터 a만큼 이동하고, 그 끝점에서 다시 벡터 b만큼 이동하면, 처음 출발점에서 마지막 도착점까지의 이동량이 a + b입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 310 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 310px; width: 100%;">
  <!-- Y축 -->
  <line x1="55" y1="260" x2="55" y2="10" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="55,8 51,16 59,16" fill="currentColor"/>
  <text fill="currentColor" x="43" y="18" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <!-- X축 -->
  <line x1="55" y1="260" x2="275" y2="260" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="278,260 270,256 270,264" fill="currentColor"/>
  <text fill="currentColor" x="280" y="273" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <!-- 그리드 -->
  <line x1="115" y1="15" x2="115" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="175" y1="15" x2="175" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="235" y1="15" x2="235" y2="260" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="200" x2="270" y2="200" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="140" x2="270" y2="140" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="80" x2="270" y2="80" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="55" y1="20" x2="270" y2="20" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <!-- 눈금 -->
  <text fill="currentColor" x="115" y="277" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="175" y="277" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <text fill="currentColor" x="235" y="277" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">3</text>
  <text fill="currentColor" x="46" y="204" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="46" y="144" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <text fill="currentColor" x="46" y="84" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">3</text>
  <text fill="currentColor" x="46" y="24" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">4</text>
  <!-- 결과 a+b 점선 -->
  <line x1="55" y1="260" x2="231" y2="24" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.35"/>
  <!-- 벡터 a: (0,0)→(2,1) -->
  <line x1="55" y1="260" x2="170" y2="203" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="175,200 170,207 166,201" fill="currentColor"/>
  <!-- 벡터 b: (2,1)→(3,4) -->
  <line x1="175" y1="200" x2="232" y2="26" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="235,20 236,28 230,26" fill="currentColor"/>
  <!-- 점 표시 -->
  <circle cx="175" cy="200" r="3.5" fill="currentColor"/>
  <circle cx="235" cy="20" r="3.5" fill="currentColor"/>
  <!-- 레이블 -->
  <text fill="currentColor" x="132" y="222" font-size="11" font-family="sans-serif" font-weight="bold">a = (2, 1)</text>
  <text fill="currentColor" x="240" y="120" font-size="11" font-family="sans-serif" font-weight="bold">b = (1, 3)</text>
  <text fill="currentColor" x="180" y="14" font-size="11" font-family="sans-serif" font-weight="bold">(3, 4) = a + b</text>
</svg>
</div>

<br>

게임에서는 현재 위치에 이동량을 더할 때 이 연산을 사용합니다. 캐릭터의 현재 위치에 이동 벡터를 더하면 새 위치가 됩니다.

$$
\begin{aligned}
\text{현재 위치} &= (5, \; 0, \; 3) \\
\text{이동 벡터} &= (1, \; 0, \; {-}2) \\[6pt]
\text{새 위치} &= (5{+}1, \; 0{+}0, \; 3{+}({-}2)) = (6, \; 0, \; 1)
\end{aligned}
$$

---

### 뺄셈

두 벡터를 뺄 때도 같은 자리의 성분끼리 뺍니다.

$$
\mathbf{a} = (4, \; 3), \quad \mathbf{b} = (1, \; 1)
$$

$$
\mathbf{a} - \mathbf{b} = (4{-}1, \; 3{-}1) = (3, \; 2)
$$

두 위치를 빼면 한 위치에서 다른 위치까지의 차이가 벡터로 나옵니다.

`target - origin`을 계산하면 `origin`에서 `target`까지 이동하려면 어느 방향으로 얼마나 가야 하는지 알 수 있습니다. 이 벡터의 방향은 `target` 쪽이고, 크기는 두 점 사이의 거리입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 340 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 340px; width: 100%;">
  <!-- Y축 -->
  <line x1="50" y1="200" x2="50" y2="20" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="50,17 46,25 54,25" fill="currentColor"/>
  <text fill="currentColor" x="38" y="27" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <!-- X축 -->
  <line x1="50" y1="200" x2="310" y2="200" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="313,200 305,196 305,204" fill="currentColor"/>
  <text fill="currentColor" x="316" y="213" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <!-- 그리드 -->
  <line x1="110" y1="25" x2="110" y2="200" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="170" y1="25" x2="170" y2="200" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="230" y1="25" x2="230" y2="200" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="290" y1="25" x2="290" y2="200" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="50" y1="140" x2="305" y2="140" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="50" y1="80" x2="305" y2="80" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <!-- 눈금 -->
  <text fill="currentColor" x="110" y="215" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="170" y="215" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <text fill="currentColor" x="230" y="215" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">3</text>
  <text fill="currentColor" x="290" y="215" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">4</text>
  <text fill="currentColor" x="42" y="144" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="42" y="84" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">2</text>
  <!-- origin → target 방향 벡터 -->
  <line x1="110" y1="140" x2="286" y2="83" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="290,80 285,87 282,81" fill="currentColor"/>
  <!-- 점 표시 -->
  <circle cx="110" cy="140" r="4" fill="currentColor"/>
  <circle cx="290" cy="80" r="4" fill="currentColor"/>
  <!-- 레이블 -->
  <text fill="currentColor" x="110" y="162" text-anchor="middle" font-size="10" font-family="sans-serif">origin = (1, 1)</text>
  <text fill="currentColor" x="290" y="68" text-anchor="middle" font-size="10" font-family="sans-serif">target = (4, 3)</text>
  <text fill="currentColor" x="230" y="138" font-size="10" font-family="sans-serif" opacity="0.7">target − origin = (3, 2)</text>
</svg>
</div>

<br>

적 캐릭터를 플레이어 쪽으로 움직일 때도 같은 계산을 사용합니다. 플레이어 위치에서 적 위치를 빼면, 적에서 플레이어로 향하는 벡터를 얻을 수 있습니다.

이 벡터를 정규화한 뒤 이동 속력을 곱하면 실제 이동에 사용할 속도 벡터가 됩니다.

$$
\begin{aligned}
\text{플레이어 위치} &= (10, \; 0, \; 5) \\
\text{적 위치} &= (3, \; 0, \; 2) \\[6pt]
\text{방향 벡터} &= \text{플레이어 위치} - \text{적 위치} \\
&= (10{-}3, \; 0{-}0, \; 5{-}2) \\
&= (7, \; 0, \; 3)
\end{aligned}
$$

---

### 스칼라 곱과 나눗셈

벡터에 숫자 하나를 곱하거나 나누면 벡터의 길이를 조절할 수 있습니다. 계산할 때는 x, y, z 각 성분을 같은 숫자로 곱하거나 나눕니다.

$$
\mathbf{v} = (3, \; 2)
$$

$$
\begin{aligned}
2\mathbf{v} &= (6, \; 4) & &\text{— 크기가 2배} \\
0.5\mathbf{v} &= (1.5, \; 1) & &\text{— 크기가 절반} \\
\frac{\mathbf{v}}{2} &= (1.5, \; 1) & &\text{— 0.5를 곱한 것과 같음} \\
{-}\mathbf{v} &= (-3, \; -2) & &\text{— 방향 반전}
\end{aligned}
$$

기하학적으로 스칼라 곱과 나눗셈은 벡터의 **크기를 변경**합니다.

양수를 곱하거나 나누면 같은 방향으로 늘어나거나 줄어들고, 음수를 곱하면 **방향이 반전**됩니다. 나눗셈은 0이 아닌 값에 대해서만 사용할 수 있으며, `v / 2`는 `v * 0.5`와 같은 의미입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 440 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- Y축 -->
  <line x1="170" y1="265" x2="170" y2="12" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="170,10 166,18 174,18" fill="currentColor"/>
  <text fill="currentColor" x="158" y="20" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <!-- X축 -->
  <line x1="15" y1="170" x2="428" y2="170" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="430,170 422,166 422,174" fill="currentColor"/>
  <text fill="currentColor" x="434" y="183" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <!-- 그리드 -->
  <line x1="170" y1="100" x2="420" y2="100" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="170" y1="30" x2="420" y2="30" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <line x1="60" y1="170" x2="60" y2="240" stroke="currentColor" stroke-width="0.3" opacity="0.15"/>
  <!-- 벡터 2v = (6, 4) — 연한 스타일 -->
  <line x1="170" y1="170" x2="376" y2="33" stroke="currentColor" stroke-width="1.8" opacity="0.45"/>
  <polygon points="380,30 376,37 373,31" fill="currentColor" opacity="0.45"/>
  <circle cx="380" cy="30" r="3" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="386" y="26" font-size="10" font-family="sans-serif" opacity="0.6">2v = (6, 4)</text>
  <!-- 벡터 v = (3, 2) — 주 벡터 -->
  <line x1="170" y1="170" x2="271" y2="103" stroke="currentColor" stroke-width="2.5"/>
  <polygon points="275,100 271,107 268,101" fill="currentColor"/>
  <circle cx="275" cy="100" r="3" fill="currentColor"/>
  <text fill="currentColor" x="280" y="96" font-size="11" font-family="sans-serif" font-weight="bold">v = (3, 2)</text>
  <!-- 벡터 0.5v = (1.5, 1) — 연한 스타일 -->
  <line x1="170" y1="170" x2="220" y2="138" stroke="currentColor" stroke-width="1.8" opacity="0.45"/>
  <polygon points="223,135 219,141 217,136" fill="currentColor" opacity="0.45"/>
  <circle cx="223" cy="135" r="3" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="227" y="131" font-size="10" font-family="sans-serif" opacity="0.6">0.5v = (1.5, 1)</text>
  <!-- 벡터 -v = (-3, -2) — 점선 스타일 -->
  <line x1="170" y1="170" x2="69" y2="237" stroke="currentColor" stroke-width="2" stroke-dasharray="6,3"/>
  <polygon points="65,240 69,234 72,240" fill="currentColor"/>
  <circle cx="65" cy="240" r="3" fill="currentColor"/>
  <text fill="currentColor" x="20" y="256" font-size="10" font-family="sans-serif">−v = (−3, −2)</text>
</svg>
</div>

<br>

게임에서는 방향에 속력을 붙일 때 스칼라 곱을 사용합니다. 방향 벡터에 속력 값을 곱하면 속도 벡터가 되고, 같은 방향으로 더 빠르게 이동하려면 더 큰 값을 곱하면 됩니다. 반대로 벡터를 일정한 크기로 줄이거나 정규화할 때는 스칼라 나눗셈이 사용됩니다.

---

## 벡터의 크기와 정규화

벡터는 방향만 담는 것이 아니라 길이도 함께 가집니다. 두 위치 사이의 거리를 구하려면 벡터의 길이를 알아야 합니다. 반대로 방향만 필요할 때는 길이가 계산에 섞이지 않도록 벡터의 길이를 1로 맞춥니다.

### 크기 (Magnitude)

벡터의 **크기(Magnitude)**는 벡터가 나타내는 화살표의 길이입니다. 2D 벡터 (x, y)는 x축 이동량과 y축 이동량이 직각을 이루므로, 피타고라스 정리로 길이를 구할 수 있습니다.

**2D 벡터의 크기**

$$
|\mathbf{v}| = \sqrt{x^2 + y^2}
$$

$$
\begin{aligned}
\mathbf{v} &= (3, \; 4) \\[4pt]
|\mathbf{v}| &= \sqrt{3^2 + 4^2} \\
&= \sqrt{9 + 16} \\
&= \sqrt{25} = 5
\end{aligned}
$$

<br>

3D 벡터도 같은 원리를 사용합니다. x, y, z 세 성분이 서로 직교하는 축의 이동량이므로, 세 성분의 제곱을 더한 뒤 제곱근을 구합니다.

**3D 벡터의 크기**

$$
|\mathbf{v}| = \sqrt{x^2 + y^2 + z^2}
$$

$$
\begin{aligned}
\mathbf{v} &= (1, \; 2, \; 2) \\[4pt]
|\mathbf{v}| &= \sqrt{1^2 + 2^2 + 2^2} \\
&= \sqrt{1 + 4 + 4} \\
&= \sqrt{9} = 3
\end{aligned}
$$

<br>

3D에서 이 공식을 떠올리기 어렵다면, 바닥면의 대각선을 먼저 구한 뒤 그 대각선과 y축 높이를 다시 조합한다고 보면 됩니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 500 170" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- 2D -->
  <text fill="currentColor" x="110" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">2D</text>
  <line x1="30" y1="140" x2="190" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <line x1="190" y1="140" x2="190" y2="40" stroke="currentColor" stroke-width="1.5"/>
  <line x1="30" y1="140" x2="190" y2="40" stroke="currentColor" stroke-width="2.5"/>
  <polyline points="175,140 175,125 190,125" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text fill="currentColor" x="110" y="158" text-anchor="middle" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <text fill="currentColor" x="204" y="95" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <text fill="currentColor" x="92" y="82" font-size="11" font-family="sans-serif">빗변</text>
  <circle cx="30" cy="140" r="3" fill="currentColor"/>
  <circle cx="190" cy="40" r="3" fill="currentColor"/>
  <!-- 3D -->
  <!-- 등축 단위: x̂=(28,0), ẑ=(-11,13), ŷ=(0,-28) -->
  <!-- O=(295,120), Ox=(407,120), Oz=(262,159), Oxz=(374,159), P=(374,75) -->
  <text fill="currentColor" x="340" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">3D</text>
  <!-- 바닥면 사각형 4변 -->
  <line x1="295" y1="120" x2="407" y2="120" stroke="currentColor" stroke-width="1.5"/><!-- O→Ox (x) -->
  <line x1="407" y1="120" x2="374" y2="159" stroke="currentColor" stroke-width="1.5"/><!-- Ox→Oxz (z) -->
  <line x1="295" y1="120" x2="262" y2="159" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/><!-- O→Oz -->
  <line x1="262" y1="159" x2="374" y2="159" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/><!-- Oz→Oxz -->
  <!-- 바닥 대각선: O→Oxz √(x²+z²) -->
  <line x1="295" y1="120" x2="374" y2="159" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3" opacity="0.6"/>
  <!-- y 변: Oxz→P -->
  <line x1="374" y1="159" x2="374" y2="75" stroke="currentColor" stroke-width="1.5"/>
  <!-- 공간 대각선: O→P |v| -->
  <line x1="295" y1="120" x2="374" y2="75" stroke="currentColor" stroke-width="2.5"/>
  <!-- 변 레이블 -->
  <text fill="currentColor" x="351" y="133" text-anchor="middle" font-size="11" font-family="sans-serif" font-style="italic">x</text>
  <text fill="currentColor" x="398" y="148" font-size="11" font-family="sans-serif" font-style="italic">z</text>
  <text fill="currentColor" x="386" y="105" font-size="11" font-family="sans-serif" font-style="italic">y</text>
  <text fill="currentColor" x="322" y="150" font-size="10" font-family="sans-serif" opacity="0.55">√(x²+z²)</text>
  <text fill="currentColor" x="318" y="88" font-size="11" font-family="sans-serif">|v|</text>
  <!-- 꼭짓점 -->
  <circle cx="295" cy="120" r="3" fill="currentColor"/>
  <circle cx="407" cy="120" r="2.5" fill="currentColor"/>
  <circle cx="374" cy="159" r="2.5" fill="currentColor"/>
  <circle cx="374" cy="75" r="3" fill="currentColor"/>
</svg>
</div>

$$
\text{2D:} \quad |\mathbf{v}| = \sqrt{x^2 + y^2} \qquad \text{3D:} \quad |\mathbf{v}| = \sqrt{x^2 + y^2 + z^2}
$$

<br>

게임에서 벡터의 크기는 **거리 계산**에 직접 쓰입니다. 두 오브젝트의 위치를 빼면 한 오브젝트에서 다른 오브젝트로 향하는 벡터가 나오고, 그 벡터의 크기가 두 점 사이의 거리입니다.

$$
\begin{aligned}
\text{플레이어 위치} &= (10, \; 0, \; 5) \\
\text{적 위치} &= (3, \; 0, \; 2) \\[6pt]
\text{차이 벡터} &= (10{-}3, \; 0{-}0, \; 5{-}2) = (7, \; 0, \; 3) \\[4pt]
\text{거리} &= |\text{차이 벡터}| = \sqrt{7^2 + 0^2 + 3^2} \\
&= \sqrt{49 + 0 + 9} \\
&= \sqrt{58} \approx 7.62
\end{aligned}
$$

---

### 단위 벡터와 정규화

**단위 벡터(Unit Vector)**는 크기가 정확히 1인 벡터입니다. 단위 벡터는 순수한 **방향**만을 나타내며, 크기 정보를 담지 않습니다.

임의의 벡터를 단위 벡터로 바꾸는 연산을 **정규화(Normalization)**라고 합니다. 벡터의 각 성분을 벡터의 크기로 나누면 방향은 유지되고 크기만 1이 됩니다.

<br>

**정규화 공식**

$$
\hat{\mathbf{v}} = \frac{\mathbf{v}}{|\mathbf{v}|}
$$

$$
\begin{aligned}
\mathbf{v} &= (3, \; 0, \; 4) \\[4pt]
|\mathbf{v}| &= \sqrt{9 + 0 + 16} = \sqrt{25} = 5 \\[4pt]
\hat{\mathbf{v}} &= \left(\frac{3}{5}, \; \frac{0}{5}, \; \frac{4}{5}\right) = (0.6, \; 0, \; 0.8) \\[4pt]
|\hat{\mathbf{v}}| &= \sqrt{0.36 + 0 + 0.64} = \sqrt{1} = 1 \quad \leftarrow \text{크기가 1}
\end{aligned}
$$

정규화된 벡터는 원래 벡터와 같은 방향을 가리키지만 크기는 1입니다. 즉, 방향 정보만 남기고 거리나 속력 같은 크기 정보는 제거합니다.

<br>

게임에서 정규화는 방향과 속력을 분리할 때 사용합니다. 적에서 플레이어를 향하는 벡터를 구한 뒤, 이 벡터를 정규화하고 원하는 속력을 곱하면 이동 속도 벡터가 됩니다.

정규화하지 않은 벡터를 그대로 이동에 사용하면, 두 오브젝트 사이가 멀수록 벡터의 크기도 커집니다. 그러면 방향만 달라져야 하는 상황에서 이동 속도까지 함께 달라집니다.

$$
\begin{aligned}
\text{방향 벡터} &= (7, \; 0, \; 3) & &\leftarrow |\mathbf{v}| \approx 7.62 \\
\text{정규화} &= (0.92, \; 0, \; 0.39) & &\leftarrow |\hat{\mathbf{v}}| = 1 \\[6pt]
\text{이동 속도} &= \hat{\mathbf{v}} \times \text{속력} \\
&= (0.92, \; 0, \; 0.39) \times 5 \\
&= (4.6, \; 0, \; 1.95)
\end{aligned}
$$

---

### Unity에서의 크기와 정규화

Unity의 `Vector3`에는 크기와 정규화에 대응하는 속성이 준비되어 있습니다.

`Vector3.magnitude`는 벡터의 크기를 반환합니다. 내부적으로 $\sqrt{x^2 + y^2 + z^2}$를 계산합니다.

`Vector3.normalized`는 정규화된 벡터를 반환합니다. 내부적으로 크기를 먼저 구한 뒤 각 성분을 나눕니다.

`Vector3.sqrMagnitude`는 크기의 **제곱** 값을 반환합니다. 내부적으로 $x^2 + y^2 + z^2$만 계산하고 제곱근을 생략합니다.

제곱근 연산은 덧셈이나 곱셈보다 비용이 큽니다. 거리의 정확한 값이 필요하지 않고 기준 거리보다 가까운지만 확인하면 된다면 `sqrMagnitude`를 사용할 수 있습니다. 양수 거리에서는 a > b이면 a² > b²이므로, 제곱값끼리 비교해도 대소 관계가 유지되기 때문입니다.

```csharp
// magnitude 사용 (제곱근 포함)
float dist = (target - origin).magnitude;
if (dist < 10f) { ... }

// sqrMagnitude 사용 (제곱근 생략)
float sqrDist = (target - origin).sqrMagnitude;
if (sqrDist < 100f) { ... }    // 10의 제곱 = 100
```

예를 들어 반경 10 안에 들어왔는지만 확인한다면, 실제 거리와 10을 비교할 필요가 없습니다. 거리의 제곱값을 구한 뒤 10의 제곱인 100과 비교하면 같은 판단을 할 수 있습니다. 프레임마다 많은 오브젝트의 거리를 검사하는 코드에서는 이런 방식으로 제곱근 계산을 줄일 수 있습니다.

---

## 내적 (Dot Product)

게임에서는 두 방향이 얼마나 비슷한지 판단해야 할 때가 많습니다. 플레이어가 적을 바라보고 있는지, 표면이 빛을 정면으로 받고 있는지, 오브젝트가 카메라를 향하고 있는지 같은 판단이 여기에 해당합니다.

**내적(Dot Product)**은 이런 방향 관계를 숫자 하나로 바꾸는 연산입니다. 두 벡터를 입력으로 받아 스칼라 값을 반환하며, 이 값의 부호와 크기를 보면 두 벡터가 같은 쪽을 향하는지, 수직에 가까운지, 반대쪽을 향하는지 알 수 있습니다.

---

### 내적의 공식

내적은 코드에서는 성분별 곱의 합으로 계산합니다.

<br>

$$
\mathbf{a} \cdot \mathbf{b} = a_x b_x + a_y b_y + a_z b_z
$$

$$
\begin{aligned}
\mathbf{a} &= (2, \; 3, \; 1), \quad \mathbf{b} = (4, \; {-}1, \; 2) \\[6pt]
\mathbf{a} \cdot \mathbf{b} &= 2 \times 4 + 3 \times ({-}1) + 1 \times 2 \\
&= 8 + ({-}3) + 2 \\
&= 7
\end{aligned}
$$

<br>

내적은 두 벡터 사이의 각도와도 연결됩니다.

$$
\mathbf{a} \cdot \mathbf{b} = |\mathbf{a}| \; |\mathbf{b}| \; \cos\theta
$$

여기서 $\lvert\mathbf{a}\rvert$는 벡터 a의 크기, $\lvert\mathbf{b}\rvert$는 벡터 b의 크기, $\theta$는 두 벡터 사이의 각도입니다.

<br>

이 식 때문에 내적 값으로 두 벡터의 방향 차이를 읽을 수 있습니다. 특히 두 벡터의 크기가 1이면 식이 더 단순해집니다.

---

### 내적의 기하학적 의미

두 벡터가 모두 **단위 벡터**(크기 1)라면, 앞의 식에서 $|\mathbf{a}|$와 $|\mathbf{b}|$가 모두 1이 됩니다.

$$
|\mathbf{a}| = 1, \; |\mathbf{b}| = 1 \; \text{일 때:} \quad \mathbf{a} \cdot \mathbf{b} = 1 \times 1 \times \cos\theta = \cos\theta
$$

두 단위 벡터의 내적은 두 벡터 사이 각도의 코사인 값과 같습니다. 그래서 벡터를 정규화해 두면 내적 결과만으로 두 방향이 얼마나 비슷한지 판단할 수 있습니다.

<br>

**$\cos\theta$ 의 부호와 방향 관계**

$$
\begin{aligned}
\theta = 0^\circ &\rightarrow \cos\theta = 1.0 & &\text{같은 방향} \\
\theta = 60^\circ &\rightarrow \cos\theta = 0.5 & &\text{같은 방향 쪽} \\
\theta = 90^\circ &\rightarrow \cos\theta = 0.0 & &\text{수직} \\
\theta = 120^\circ &\rightarrow \cos\theta = -0.5 & &\text{반대 방향 쪽} \\
\theta = 180^\circ &\rightarrow \cos\theta = -1.0 & &\text{정반대}
\end{aligned}
$$

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 540 135" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 내적 > 0 -->
  <text fill="currentColor" x="90" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">내적 > 0</text>
  <text fill="currentColor" x="90" y="32" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(같은 방향)</text>
  <line x1="30" y1="100" x2="148" y2="100" stroke="currentColor" stroke-width="2"/>
  <polygon points="150,100 144,96 144,104" fill="currentColor"/>
  <text fill="currentColor" x="156" y="104" font-size="11" font-family="sans-serif" font-weight="bold">a</text>
  <line x1="30" y1="100" x2="79" y2="41" stroke="currentColor" stroke-width="2"/>
  <polygon points="81,39 79,47 73,43" fill="currentColor"/>
  <text fill="currentColor" x="87" y="38" font-size="11" font-family="sans-serif" font-weight="bold">b</text>
  <path d="M 60,100 A 30,30 0 0,0 49,77" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text fill="currentColor" x="68" y="86" font-size="9" font-family="sans-serif" opacity="0.6">θ</text>
  <!-- 내적 = 0 -->
  <text fill="currentColor" x="270" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">내적 = 0</text>
  <text fill="currentColor" x="270" y="32" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(수직)</text>
  <line x1="210" y1="100" x2="328" y2="100" stroke="currentColor" stroke-width="2"/>
  <polygon points="330,100 324,96 324,104" fill="currentColor"/>
  <text fill="currentColor" x="336" y="104" font-size="11" font-family="sans-serif" font-weight="bold">a</text>
  <line x1="210" y1="100" x2="210" y2="48" stroke="currentColor" stroke-width="2"/>
  <polygon points="210,45 206,53 214,53" fill="currentColor"/>
  <text fill="currentColor" x="220" y="48" font-size="11" font-family="sans-serif" font-weight="bold">b</text>
  <polyline points="210,85 225,85 225,100" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text fill="currentColor" x="233" y="88" font-size="9" font-family="sans-serif" opacity="0.6">90°</text>
  <!-- 내적 < 0 -->
  <text fill="currentColor" x="450" y="16" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">내적 &lt; 0</text>
  <text fill="currentColor" x="450" y="32" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">(반대 방향)</text>
  <line x1="390" y1="100" x2="508" y2="100" stroke="currentColor" stroke-width="2"/>
  <polygon points="510,100 504,96 504,104" fill="currentColor"/>
  <text fill="currentColor" x="516" y="104" font-size="11" font-family="sans-serif" font-weight="bold">a</text>
  <line x1="390" y1="100" x2="333" y2="53" stroke="currentColor" stroke-width="2"/>
  <polygon points="330,50 337,52 334,58" fill="currentColor"/>
  <text fill="currentColor" x="322" y="48" font-size="11" font-family="sans-serif" font-weight="bold">b</text>
  <path d="M 420,100 A 30,30 0 0,0 367,81" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text fill="currentColor" x="400" y="86" font-size="9" font-family="sans-serif" opacity="0.6">θ</text>
</svg>
</div>

내적이 양수이면 두 벡터의 각도가 90도보다 작고, 음수이면 90도보다 큽니다. 값이 0에 가까우면 두 방향은 거의 수직입니다.

이 성질은 앞뒤 판정에 자주 사용됩니다. 플레이어의 전방 벡터와 적을 향한 방향 벡터를 내적했을 때 값이 양수이면, 적은 플레이어가 바라보는 앞쪽에 있습니다. 값이 음수이면 플레이어 뒤쪽에 있는 것으로 볼 수 있습니다.

카메라와 오브젝트의 앞뒤 관계를 판단할 때도 같은 방식으로 사용할 수 있습니다. 별도의 각도 계산 없이 내적의 부호만으로 시야 판정이나 앞뒤 구분을 처리할 수 있습니다.

---

### 내적과 조명 계산

내적은 **조명(Lighting)** 계산에서 자주 등장합니다. [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 법선(Normal)과 빛의 각도에 따라 표면 밝기가 달라진다고 했습니다. 이 각도 관계를 수치로 바꿀 때 내적을 사용합니다.

표면의 법선 벡터 N은 표면에서 수직으로 뻗어나가는 방향이고, 광원 방향 벡터 L은 표면에서 광원을 향하는 방향입니다. 이 두 벡터의 내적 $\mathbf{N} \cdot \mathbf{L}$은 빛이 표면에 얼마나 직접적으로 닿는지를 나타냅니다.

<br>

$\mathbf{N}$과 $\mathbf{L}$이 모두 단위 벡터일 때, $\mathbf{N} \cdot \mathbf{L} = \cos\theta$입니다. 빛이 표면 뒤쪽에서 오는 경우($\theta > 90°$)에는 음수가 되므로, 실제 조명 계산에서는 0 이하를 잘라냅니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 420 175" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 표면 -->
  <line x1="40" y1="140" x2="380" y2="140" stroke="currentColor" stroke-width="2"/>
  <text fill="currentColor" x="385" y="144" font-size="10" font-family="sans-serif" opacity="0.5">표면</text>
  <!-- 표면 해칭 -->
  <line x1="60" y1="140" x2="50" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="90" y1="140" x2="80" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="120" y1="140" x2="110" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="150" y1="140" x2="140" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="180" y1="140" x2="170" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="240" y1="140" x2="230" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="270" y1="140" x2="260" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="300" y1="140" x2="290" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="330" y1="140" x2="320" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <line x1="360" y1="140" x2="350" y2="155" stroke="currentColor" stroke-width="0.7" opacity="0.2"/>
  <!-- 법선 N (위로) -->
  <line x1="210" y1="140" x2="210" y2="22" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="210,18 206,26 214,26" fill="currentColor"/>
  <text fill="currentColor" x="222" y="26" font-size="12" font-family="sans-serif" font-weight="bold">N</text>
  <!-- 광원 방향 L (표면에서 광원 쪽으로) -->
  <line x1="210" y1="140" x2="112" y2="48" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="108,45 115,50 112,56" fill="currentColor"/>
  <text fill="currentColor" x="94" y="42" font-size="12" font-family="sans-serif" font-weight="bold">L</text>
  <!-- 광선 표시 (L 반대 방향에서 들어오는 빛) -->
  <line x1="108" y1="45" x2="70" y2="15" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- 각도 θ -->
  <path d="M 210,110 A 30,30 0 0,0 189,115" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <text fill="currentColor" x="194" y="106" font-size="12" font-family="sans-serif" font-style="italic" opacity="0.7">θ</text>
  <!-- 표면 접점 -->
  <circle cx="210" cy="140" r="3" fill="currentColor"/>
</svg>
</div>

$$
\text{밝기} = \max(0, \;\mathbf{N} \cdot \mathbf{L}) = \max(0, \;\cos\theta)
$$

$$
\begin{aligned}
\theta = 0^\circ &\rightarrow \cos(0^\circ) = 1.0 & &\text{(가장 밝음)} \\
\theta = 45^\circ &\rightarrow \cos(45^\circ) \approx 0.71 & &\text{(중간 밝기)} \\
\theta = 90^\circ &\rightarrow \cos(90^\circ) = 0.0 & &\text{(빛이 닿지 않음)} \\
\theta > 90^\circ &\rightarrow \cos\theta < 0 & &\text{(표면 뒤쪽, 0으로 처리)}
\end{aligned}
$$

<br>

확산(Diffuse) 조명에서는 빛이 표면에 정면으로 들어올수록 밝고, 옆에서 스치듯 들어올수록 어둡게 보입니다. 법선과 빛 방향의 내적은 이 차이를 1에서 0 사이의 값으로 바꿔 주므로, 표면 밝기를 계산하는 기본 값으로 사용할 수 있습니다. 이 방식이 **램버트 반사(Lambertian Reflectance)**의 기본 형태입니다.

Unity에서는 이 내적 계산을 `Vector3.Dot(a, b)`로 작성합니다.

```csharp
Vector3 N = transform.up;          // 표면 법선
Vector3 L = lightDirection;        // 광원 방향 (단위 벡터)

float brightness = Vector3.Dot(N, L);
brightness = Mathf.Max(brightness, 0f);  // 음수는 0으로
```

---

## 외적 (Cross Product)

내적이 두 벡터에서 숫자 하나를 얻는 연산이라면, **외적(Cross Product)**은 두 벡터에서 새로운 벡터를 얻는 연산입니다. 외적의 결과는 입력 두 벡터에 모두 수직인 방향을 가리키며, 3D 공간에서만 정의됩니다.

---

### 외적의 공식

외적은 다음 공식으로 계산합니다.

$$
\mathbf{a} \times \mathbf{b} = (a_y b_z - a_z b_y, \;\; a_z b_x - a_x b_z, \;\; a_x b_y - a_y b_x)
$$

$$
\begin{aligned}
\mathbf{a} &= (1, \; 0, \; 0), \quad \mathbf{b} = (0, \; 1, \; 0) \\[6pt]
\mathbf{a} \times \mathbf{b} &= (0 \cdot 0 - 0 \cdot 1, \;\; 0 \cdot 0 - 1 \cdot 0, \;\; 1 \cdot 1 - 0 \cdot 0) \\
&= (0, \; 0, \; 1)
\end{aligned}
$$

x축 방향 벡터 (1, 0, 0)과 y축 방향 벡터 (0, 1, 0)의 외적은 z축 방향 벡터 (0, 0, 1)입니다. x축과 y축에 모두 수직인 방향이 z축이므로, 결과가 직관적으로 일치합니다.

---

### 외적의 기하학적 의미

외적의 결과는 두 입력 벡터가 놓인 평면에서 수직으로 뻗는 벡터입니다. 그래서 삼각형이나 표면의 방향을 나타내는 **법선 벡터(Normal Vector)**를 구할 때 외적을 사용합니다.

결과 벡터의 길이도 의미를 가집니다. 외적의 크기는 다음과 같고, 이 값은 두 벡터가 만드는 평행사변형의 넓이와 같습니다.

$$
\lvert\mathbf{a} \times \mathbf{b}\rvert = \lvert\mathbf{a}\rvert \; \lvert\mathbf{b}\rvert \; \sin\theta
$$

두 벡터가 평행하면 평행사변형의 넓이가 0이므로 외적의 크기도 0입니다. 두 벡터가 수직에 가까워질수록 넓이가 커지고, 외적의 크기도 함께 커집니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 420 205" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 평행사변형 -->
  <polygon points="60,175 240,175 310,115 130,115" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 벡터 a (아래 변) -->
  <line x1="60" y1="175" x2="236" y2="175" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="240,175 234,171 234,179" fill="currentColor"/>
  <text fill="currentColor" x="150" y="196" text-anchor="middle" font-size="12" font-family="sans-serif" font-weight="bold">a</text>
  <!-- 벡터 b (왼쪽 변) -->
  <line x1="60" y1="175" x2="127" y2="118" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="130,115 127,123 121,119" fill="currentColor"/>
  <text fill="currentColor" x="78" y="138" font-size="12" font-family="sans-serif" font-weight="bold">b</text>
  <!-- a × b 벡터 (위로) -->
  <line x1="185" y1="145" x2="185" y2="22" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="185,18 181,26 189,26" fill="currentColor"/>
  <text fill="currentColor" x="200" y="20" font-size="12" font-family="sans-serif" font-weight="bold">a × b</text>
  <!-- 넓이 레이블 -->
  <text fill="currentColor" x="185" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.4">넓이 = |a × b|</text>
</svg>
</div>

---

### 외적의 방향

외적의 결과는 두 벡터가 이루는 평면에 수직이지만, 그 수직 방향은 두 가지가 가능합니다. 어느 쪽을 결과로 볼지는 좌표계의 손잡이 규칙으로 정합니다. 수학과 OpenGL에서는 **오른손 법칙(Right-Hand Rule)**을 사용합니다.

오른손의 네 손가락을 벡터 a 방향으로 뻗은 뒤, 벡터 b 방향으로 감아쥡니다. 이때 엄지가 가리키는 방향이 $\mathbf{a} \times \mathbf{b}$의 방향입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 330 172" xmlns="http://www.w3.org/2000/svg" style="max-width: 330px; width: 100%;">
  <circle cx="90" cy="155" r="3" fill="currentColor" fill-opacity="0.3"/>
  <!-- 벡터 a (오른쪽) -->
  <line x1="90" y1="155" x2="268" y2="155" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="270,155 264,151 264,159" fill="currentColor"/>
  <text fill="currentColor" x="276" y="159" font-size="12" font-family="sans-serif" font-weight="bold">a</text>
  <!-- 벡터 b (위쪽-오른쪽) -->
  <line x1="90" y1="155" x2="166" y2="85" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="170,82 163,87 167,93" fill="currentColor"/>
  <text fill="currentColor" x="178" y="82" font-size="12" font-family="sans-serif" font-weight="bold">b</text>
  <!-- a × b (위로) -->
  <line x1="90" y1="155" x2="90" y2="22" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="90,18 86,26 94,26" fill="currentColor"/>
  <text fill="currentColor" x="103" y="20" font-size="12" font-family="sans-serif" font-weight="bold">a × b</text>
  <!-- θ 각도 -->
  <path d="M 120,155 A 30,30 0 0,0 109,132" fill="none" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text fill="currentColor" x="125" y="140" font-size="10" font-family="sans-serif" font-style="italic" opacity="0.6">θ</text>
</svg>
</div>

외적에서는 입력 순서가 결과 방향을 결정합니다. $\mathbf{a} \times \mathbf{b}$와 $\mathbf{b} \times \mathbf{a}$는 길이는 같지만 서로 반대 방향을 가리킵니다.

$$
\mathbf{a} \times \mathbf{b} = -(\mathbf{b} \times \mathbf{a})
$$

<br>

Unity는 왼손 좌표계를 사용하므로, Unity의 x, y, z축에서 외적 방향을 예상할 때는 **왼손 법칙**으로 확인해야 합니다. 왼손의 네 손가락을 첫 번째 벡터 방향에서 두 번째 벡터 방향으로 감아쥐면, 엄지가 가리키는 방향이 `Vector3.Cross(a, b)`의 결과 방향입니다.

<br>

Unity의 기본 축으로 확인하면 다음과 같습니다.

```csharp
Vector3.Cross(Vector3.right, Vector3.up);      // (0, 0, 1) = forward
Vector3.Cross(Vector3.right, Vector3.forward);  // (0, -1, 0) = down
```

첫 번째 예시에서 왼손 손가락을 right(+x)에서 up(+y) 방향으로 감아쥐면, 엄지가 forward(+z)를 가리킵니다. Unity에서 외적의 방향을 예상할 때는 이 축 방향을 기준으로 확인해야 합니다.

---

### 외적의 활용: 면의 법선 계산

외적은 **삼각형의 법선 벡터**를 구할 때 자주 사용합니다. [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 메쉬가 삼각형으로 구성되며, 각 표면에 법선이 있다고 했습니다. 삼각형의 세 정점 v0, v1, v2가 주어지면 두 변을 벡터로 만들 수 있고, 두 변의 외적이 삼각형 면에 수직인 방향을 줍니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 280 170" xmlns="http://www.w3.org/2000/svg" style="max-width: 280px; width: 100%;">
  <!-- 삼각형 -->
  <polygon points="140,20 40,145 240,145" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.8"/>
  <!-- 정점 -->
  <circle cx="140" cy="20" r="3.5" fill="currentColor"/>
  <text fill="currentColor" x="152" y="16" font-size="12" font-family="sans-serif" font-weight="bold">v₀</text>
  <circle cx="40" cy="145" r="3.5" fill="currentColor"/>
  <text fill="currentColor" x="22" y="162" font-size="12" font-family="sans-serif" font-weight="bold">v₁</text>
  <circle cx="240" cy="145" r="3.5" fill="currentColor"/>
  <text fill="currentColor" x="248" y="162" font-size="12" font-family="sans-serif" font-weight="bold">v₂</text>
  <!-- edge₁ 방향 (v₀→v₁) -->
  <text fill="currentColor" x="70" y="68" font-size="9" font-family="sans-serif" opacity="0.5">edge₁</text>
  <!-- edge₂ 방향 (v₀→v₂) -->
  <text fill="currentColor" x="195" y="68" font-size="9" font-family="sans-serif" opacity="0.5">edge₂</text>
</svg>
</div>

$$
\begin{aligned}
\mathbf{edge_1} &= \mathbf{v_1} - \mathbf{v_0} \\
\mathbf{edge_2} &= \mathbf{v_2} - \mathbf{v_0} \\[6pt]
\mathbf{N} &= \mathbf{edge_1} \times \mathbf{edge_2} \\[4pt]
\hat{\mathbf{N}} &= \frac{\mathbf{N}}{|\mathbf{N}|} \quad \leftarrow \text{정규화}
\end{aligned}
$$

법선의 방향은 정점의 감기 순서(Winding Order)에 따라 달라집니다. 감기 순서는 삼각형의 세 정점을 나열하는 순서입니다. 정점 순서가 바뀌면 edge1과 edge2의 순서도 바뀌고, 외적은 입력 순서가 바뀔 때 방향이 반전되므로 법선 방향도 반대로 뒤집힙니다.

GPU는 이 감기 순서를 사용해 삼각형의 앞면과 뒷면을 구분합니다. 래스터화 단계에서 화면에 투영된 삼각형의 정점 순서가 시계 방향(CW)인지 반시계 방향(CCW)인지 확인하고, 뒷면으로 판정된 삼각형은 백페이스 컬링(Backface Culling)으로 제거할 수 있습니다.

Unity는 시계 방향(CW)을 앞면으로 판정합니다. OpenGL 기반 엔진은 반시계 방향(CCW)을 앞면으로 사용하므로, 엔진에 따라 규칙이 다릅니다.

<br>

Unity에서 외적은 `Vector3.Cross(a, b)`로 계산합니다. 삼각형의 정점 순서를 Unity의 앞면 규칙에 맞추면, 이 연산으로 앞면 방향의 법선을 얻을 수 있습니다.

```csharp
Vector3 edge1 = v1 - v0;
Vector3 edge2 = v2 - v0;
Vector3 normal = Vector3.Cross(edge1, edge2).normalized;
```

---

## Unity에서의 Vector3

앞에서 다룬 연산은 Unity에서 대부분 `Vector3`를 통해 사용합니다. `Vector3`는 x, y, z 성분을 가진 3D 벡터 구조체이며, 덧셈과 뺄셈은 연산자로, 내적과 외적은 정적 메서드로 제공됩니다.

---

### 위치와 방향

Unity에서 오브젝트가 어디에 있고 어느 쪽을 향하는지는 `Transform` 컴포넌트에서 읽습니다.

`Transform.position`은 오브젝트의 **월드 공간 위치**입니다. 씬의 원점을 기준으로 오브젝트가 어디에 있는지를 나타내는 위치 벡터입니다.

방향은 `Transform.forward`, `Transform.up`, `Transform.right`로 읽습니다. 이 값들은 오브젝트가 회전한 상태를 반영한 전방, 위쪽, 오른쪽 방향입니다. 모두 길이가 1인 단위 벡터이므로, 이동 방향이나 내적 계산에 바로 사용할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 340 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 340px; width: 100%;">
  <circle cx="140" cy="125" r="3" fill="currentColor" fill-opacity="0.3"/>
  <!-- up (0, 1, 0) -->
  <line x1="140" y1="125" x2="140" y2="22" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="140,18 136,26 144,26" fill="currentColor"/>
  <text fill="currentColor" x="156" y="28" font-size="11" font-family="sans-serif" font-weight="bold">up (0, 1, 0)</text>
  <!-- right (1, 0, 0) -->
  <line x1="140" y1="125" x2="298" y2="125" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="300,125 294,121 294,129" fill="currentColor"/>
  <text fill="currentColor" x="240" y="115" font-size="11" font-family="sans-serif" font-weight="bold">right (1, 0, 0)</text>
  <!-- forward (0, 0, 1) -->
  <line x1="140" y1="125" x2="78" y2="200" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="75,203 83,200 81,193" fill="currentColor"/>
  <text fill="currentColor" x="35" y="218" font-size="11" font-family="sans-serif" font-weight="bold">forward (0, 0, 1)</text>
</svg>
</div>

<br>

위 다이어그램은 오브젝트가 회전하지 않았을 때의 기본 방향입니다. 오브젝트를 회전시키면 `forward`, `up`, `right`도 그 회전에 맞춰 바뀌므로, 현재 오브젝트가 바라보는 방향을 기준으로 사용할 수 있습니다.

```csharp
Vector3 pos = transform.position;       // 위치 벡터
Vector3 fwd = transform.forward;        // 전방 단위 벡터
Vector3 up  = transform.up;             // 위쪽 단위 벡터
Vector3 rt  = transform.right;          // 오른쪽 단위 벡터
```

---

### 미리 정의된 벡터

`Vector3`에는 자주 쓰는 월드 방향 벡터가 정적 속성으로 정의되어 있습니다.

```csharp
// 미리 정의된 Vector3 상수

  Vector3.zero     = (0, 0, 0)      // 원점
  Vector3.one      = (1, 1, 1)      // 모든 성분이 1
  Vector3.up       = (0, 1, 0)      // 월드 위쪽
  Vector3.down     = (0, -1, 0)     // 월드 아래쪽
  Vector3.forward  = (0, 0, 1)      // 월드 전방
  Vector3.back     = (0, 0, -1)     // 월드 후방
  Vector3.right    = (1, 0, 0)      // 월드 오른쪽
  Vector3.left     = (-1, 0, 0)     // 월드 왼쪽
```

`Vector3.up`과 `transform.up`은 이름이 비슷하지만 의미가 다릅니다. `Vector3.up`은 월드 공간의 고정된 방향 (0, 1, 0)을 가리키고, `transform.up`은 오브젝트가 회전한 뒤의 위쪽 방향을 가리킵니다. 오브젝트가 기울어져 있다면 `transform.up`도 그 기울어진 방향을 따라갑니다.

---

### Unity의 좌표계

앞에서 `Transform.forward`와 외적의 방향을 설명하면서 Unity의 축 방향을 여러 번 사용했습니다. 여기서는 그 기준만 정리합니다. Unity는 **왼손 좌표계(Left-Handed Coordinate System)**를 사용하며, **X축은 오른쪽**, **Y축은 위쪽**, **Z축은 전방**을 가리킵니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 320 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 320px; width: 100%;">
  <circle cx="120" cy="140" r="3" fill="currentColor" fill-opacity="0.3"/>
  <!-- Y (위) -->
  <line x1="120" y1="140" x2="120" y2="22" stroke="currentColor" stroke-width="2"/>
  <polygon points="120,18 116,26 124,26" fill="currentColor"/>
  <text fill="currentColor" x="135" y="28" font-size="12" font-family="sans-serif" font-weight="bold">Y (위)</text>
  <!-- X (오른쪽) -->
  <line x1="120" y1="140" x2="278" y2="140" stroke="currentColor" stroke-width="2"/>
  <polygon points="280,140 274,136 274,144" fill="currentColor"/>
  <text fill="currentColor" x="246" y="130" font-size="12" font-family="sans-serif" font-weight="bold">X (오른쪽)</text>
  <!-- Z (전방) -->
  <line x1="120" y1="140" x2="62" y2="193" stroke="currentColor" stroke-width="2"/>
  <polygon points="59,196 67,192 65,186" fill="currentColor"/>
  <text fill="currentColor" x="30" y="208" font-size="12" font-family="sans-serif" font-weight="bold">Z (전방)</text>
</svg>
</div>

수학 교과서나 일부 3D 도구는 z축 방향을 Unity와 다르게 잡는 경우가 있습니다. 그래서 외부 도구에서 만든 모델을 가져오거나, 스크립트에서 외적과 방향 벡터를 직접 계산할 때는 Unity의 기준인 **+Z = Forward**를 먼저 확인해야 합니다.

---

### 주요 Vector3 메서드 정리

앞에서 다룬 벡터 연산을 Unity API 기준으로 모으면 다음과 같습니다.

| 연산 | Unity API | 결과 |
|:---|:---|:---|
| 덧셈 | `a + b` | Vector3 |
| 뺄셈 | `a - b` | Vector3 |
| 스칼라 곱 | `v * s` 또는 `s * v` | Vector3 |
| 스칼라 나눗셈 | `v / s` | Vector3 |
| 크기 | `v.magnitude` | float |
| 크기의 제곱 | `v.sqrMagnitude` | float |
| 정규화 | `v.normalized` | Vector3 |
| 내적 | `Vector3.Dot(a, b)` | float |
| 외적 | `Vector3.Cross(a, b)` | Vector3 |
| 두 점 사이 거리 | `Vector3.Distance(a, b)` | float |
| 선형 보간 | `Vector3.Lerp(a, b, t)` | Vector3 |

<br>

`Vector3.Distance(a, b)`는 `(a - b).magnitude`와 같은 의미입니다. 거리의 대소만 비교한다면 `(a - b).sqrMagnitude`를 사용해 제곱근 계산을 피할 수 있습니다.

`Vector3.Lerp(a, b, t)`는 두 벡터 a와 b 사이를 t 비율(0~1)로 **선형 보간(Linear Interpolation)**합니다.

내부적으로 $\mathbf{a} + (\mathbf{b} - \mathbf{a}) \cdot t$를 계산하므로, $t = 0$이면 $\mathbf{a}$, $t = 1$이면 $\mathbf{b}$, $t = 0.5$이면 두 벡터의 중간점이 됩니다. 이동이나 카메라 추적처럼 두 값 사이를 부드럽게 이어야 할 때 사용합니다.

---

## 마무리

이번 글에서는 Unity와 렌더링에서 자주 만나는 벡터 연산을 기본 개념부터 API 사용까지 연결했습니다.

- 스칼라는 크기만 가진 양이고, 벡터는 크기와 방향을 동시에 가진 양입니다. 3D 벡터는 x, y, z 세 성분으로 표현됩니다.
- 벡터의 덧셈은 이동의 합성, 뺄셈은 두 점 사이의 방향 벡터, 스칼라 곱과 나눗셈은 크기 변경이나 방향 반전입니다.
- 벡터의 크기는 $\sqrt{x^2 + y^2 + z^2}$로 계산되며, 정규화는 크기 1인 단위 벡터로 변환하는 연산입니다. `sqrMagnitude`는 제곱근을 생략하여 거리 비교에서 성능 이점을 줍니다.
- 내적(Dot Product)은 두 벡터 사이의 각도 관계를 스칼라로 표현하며, 단위 벡터의 내적은 $\cos\theta$로 조명 계산($\mathbf{N} \cdot \mathbf{L}$)의 수학적 기반입니다.
- 외적(Cross Product)은 두 벡터에 수직인 새 벡터를 만들며, 삼각형의 법선 벡터 계산에 사용됩니다. 외적 결과의 크기는 $\lvert\mathbf{a}\rvert\lvert\mathbf{b}\rvert\sin\theta$로 평행사변형의 넓이와 같습니다.
- Unity는 왼손 좌표계(Y-up, Z-forward)를 사용하므로, 외적 방향과 삼각형 감기 순서를 Unity의 좌표계 기준으로 확인해야 합니다.

벡터는 공간의 위치와 방향을 표현하지만, 오브젝트를 이동하거나 회전시키려면 벡터를 다른 벡터로 바꾸는 변환이 필요합니다. 이 변환을 체계적으로 다루는 도구가 **행렬(Matrix)**입니다.

[그래픽스 수학 (2) - 행렬과 변환](/dev/unity/GraphicsMath-2/)에서는 이동, 회전, 스케일이 행렬 곱셈으로 표현되는 방식을 다룹니다.

<br>

---

**관련 글**
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- **그래픽스 수학 (1) - 벡터와 벡터 연산** (현재 글)
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
