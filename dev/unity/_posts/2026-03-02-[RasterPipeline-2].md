---
layout: single
title: "래스터화 파이프라인 (2) - 출력 병합 - soo:bak"
date: "2026-03-02 16:06:00 +0900"
description: 프레임 버퍼, 깊이 버퍼, Early-Z, 스텐실 버퍼, 블렌딩, 렌더 타겟, MRT를 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 버퍼
  - 깊이테스트
  - 모바일
---

## 프래그먼트 이후의 처리

[래스터화 파이프라인 (1)](/dev/unity/RasterPipeline-1/)에서 삼각형이 화면 격자 위의 프래그먼트로 변환되는 과정을 다루었습니다. Edge Function으로 삼각형 내부를 판별하고, 무게중심 좌표로 정점 속성을 보간하여 각 픽셀 위치마다 프래그먼트 데이터가 만들어졌습니다.

<br>

프래그먼트 셰이더가 색상을 계산한 뒤에도 그 결과가 곧바로 화면에 표시되지는 않습니다.

겹치는 오브젝트의 앞뒤를 가리는 깊이 테스트, 특정 영역에만 렌더링을 제한하는 스텐실 테스트, 반투명 오브젝트의 색상을 합성하는 블렌딩처럼 — 프래그먼트가 최종 픽셀이 되기까지 거쳐야 할 처리가 남아 있습니다.

이 처리들을 통칭하여 **출력 병합(Output Merger)** 단계라 하며, 깊이 버퍼·스텐실 버퍼·프레임 버퍼·렌더 타겟·MRT가 이 단계의 핵심 구성 요소입니다.

---

## 프레임 버퍼

출력 병합 단계의 출발점은 **프레임 버퍼(Frame Buffer)**입니다.

프레임 버퍼는 최종 렌더링 결과가 기록되는 메모리 영역으로, 화면에 표시될 이미지의 각 픽셀 색상이 이곳에 저장됩니다.

한 프레임의 모든 드로우 콜이 처리되면, 프레임 버퍼의 내용이 디스플레이로 전송됩니다.

<br>

프레임 버퍼의 각 픽셀은 RGBA 4개 채널로 구성됩니다.

R(Red)·G(Green)·B(Blue)는 색상을, A(Alpha)는 불투명도를 나타냅니다.

가장 일반적인 형식인 RGBA8은 채널당 8비트(0~255), 픽셀당 총 4바이트를 사용합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="260" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">프레임 버퍼의 메모리 구조</text>
  <text fill="currentColor" x="260" y="35" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">해상도 1920 × 1080 · RGBA8 형식</text>

  <!-- ===== 좌측: 화면 격자 ===== -->
  <text fill="currentColor" x="148" y="58" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">화면 격자</text>

  <!-- 열 헤더 -->
  <text fill="currentColor" x="75" y="74" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">x=0</text>
  <text fill="currentColor" x="119" y="74" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">x=1</text>
  <text fill="currentColor" x="163" y="74" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">x=2</text>
  <text fill="currentColor" x="207" y="74" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">x=3</text>
  <text fill="currentColor" x="240" y="74" text-anchor="middle" font-size="9" opacity="0.35">···</text>

  <!-- 행 헤더 -->
  <text fill="currentColor" x="37" y="96" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">y=0</text>
  <text fill="currentColor" x="37" y="126" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">y=1</text>
  <text fill="currentColor" x="37" y="156" text-anchor="middle" font-size="7.5" font-family="monospace" opacity="0.5">y=2</text>
  <text fill="currentColor" x="37" y="178" text-anchor="middle" font-size="9" opacity="0.35">⋮</text>

  <!-- Row 0 -->
  <rect x="53" y="80" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="74" y="97" text-anchor="middle" font-size="7.5" font-family="monospace">(0,0)</text>
  <rect x="97" y="80" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="118" y="97" text-anchor="middle" font-size="7.5" font-family="monospace">(1,0)</text>
  <rect x="141" y="80" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="162" y="97" text-anchor="middle" font-size="7.5" font-family="monospace">(2,0)</text>
  <rect x="185" y="80" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="206" y="97" text-anchor="middle" font-size="7.5" font-family="monospace">(3,0)</text>
  <text fill="currentColor" x="240" y="97" text-anchor="middle" font-size="9" opacity="0.35">···</text>

  <!-- Row 1 -->
  <rect x="53" y="110" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="74" y="127" text-anchor="middle" font-size="7.5" font-family="monospace">(0,1)</text>
  <rect x="97" y="110" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="118" y="127" text-anchor="middle" font-size="7.5" font-family="monospace">(1,1)</text>
  <rect x="141" y="110" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="162" y="127" text-anchor="middle" font-size="7.5" font-family="monospace">(2,1)</text>
  <rect x="185" y="110" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="206" y="127" text-anchor="middle" font-size="7.5" font-family="monospace">(3,1)</text>
  <text fill="currentColor" x="240" y="127" text-anchor="middle" font-size="9" opacity="0.35">···</text>

  <!-- Row 2 -->
  <rect x="53" y="140" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="74" y="157" text-anchor="middle" font-size="7.5" font-family="monospace">(0,2)</text>
  <rect x="97" y="140" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="118" y="157" text-anchor="middle" font-size="7.5" font-family="monospace">(1,2)</text>
  <rect x="141" y="140" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="162" y="157" text-anchor="middle" font-size="7.5" font-family="monospace">(2,2)</text>
  <rect x="185" y="140" width="42" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.7"/>
  <text fill="currentColor" x="206" y="157" text-anchor="middle" font-size="7.5" font-family="monospace">(3,2)</text>
  <text fill="currentColor" x="240" y="157" text-anchor="middle" font-size="9" opacity="0.35">···</text>

  <!-- 세로 생략 -->
  <text fill="currentColor" x="74" y="178" text-anchor="middle" font-size="9" opacity="0.35">⋮</text>
  <text fill="currentColor" x="118" y="178" text-anchor="middle" font-size="9" opacity="0.35">⋮</text>
  <text fill="currentColor" x="162" y="178" text-anchor="middle" font-size="9" opacity="0.35">⋮</text>
  <text fill="currentColor" x="206" y="178" text-anchor="middle" font-size="9" opacity="0.35">⋮</text>

  <!-- ===== 줌 화살표 ===== -->
  <line x1="95" y1="93" x2="298" y2="93" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>
  <polygon points="296,90 304,93 296,96" fill="currentColor" opacity="0.3"/>

  <!-- ===== 우측: 픽셀 구조 ===== -->
  <text fill="currentColor" x="396" y="58" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">픽셀 1개의 구조</text>

  <rect x="310" y="70" width="40" height="38" rx="3" fill="#E74C3C" fill-opacity="0.2" stroke="#E74C3C" stroke-width="1.2"/>
  <text fill="currentColor" x="330" y="89" text-anchor="middle" font-size="12" font-weight="bold" font-family="monospace">R</text>
  <text fill="currentColor" x="330" y="102" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.5">8 bit</text>

  <rect x="353" y="70" width="40" height="38" rx="3" fill="#27AE60" fill-opacity="0.2" stroke="#27AE60" stroke-width="1.2"/>
  <text fill="currentColor" x="373" y="89" text-anchor="middle" font-size="12" font-weight="bold" font-family="monospace">G</text>
  <text fill="currentColor" x="373" y="102" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.5">8 bit</text>

  <rect x="396" y="70" width="40" height="38" rx="3" fill="#2980B9" fill-opacity="0.2" stroke="#2980B9" stroke-width="1.2"/>
  <text fill="currentColor" x="416" y="89" text-anchor="middle" font-size="12" font-weight="bold" font-family="monospace">B</text>
  <text fill="currentColor" x="416" y="102" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.5">8 bit</text>

  <rect x="439" y="70" width="40" height="38" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="459" y="89" text-anchor="middle" font-size="12" font-weight="bold" font-family="monospace">A</text>
  <text fill="currentColor" x="459" y="102" text-anchor="middle" font-size="7" font-family="sans-serif" opacity="0.5">8 bit</text>

  <line x1="310" y1="114" x2="479" y2="114" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <text fill="currentColor" x="394" y="130" text-anchor="middle" font-size="9" font-family="sans-serif">= 4바이트 (32비트)</text>

  <!-- ===== 하단: 선형 메모리 배치 ===== -->
  <line x1="20" y1="195" x2="500" y2="195" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <text fill="currentColor" x="260" y="216" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">메모리 배치 — 행 우선(Row-Major) 순서</text>

  <!-- Row 0 -->
  <rect x="22" y="228" width="48" height="26" rx="2" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text fill="currentColor" x="46" y="245" text-anchor="middle" font-size="7" font-family="monospace">(0,0)</text>
  <rect x="72" y="228" width="48" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6"/>
  <text fill="currentColor" x="96" y="245" text-anchor="middle" font-size="7" font-family="monospace">(1,0)</text>
  <rect x="122" y="228" width="48" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6"/>
  <text fill="currentColor" x="146" y="245" text-anchor="middle" font-size="7" font-family="monospace">(2,0)</text>
  <text fill="currentColor" x="184" y="245" text-anchor="middle" font-size="9" opacity="0.35">···</text>
  <rect x="196" y="228" width="56" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6"/>
  <text fill="currentColor" x="224" y="245" text-anchor="middle" font-size="7" font-family="monospace">(1919,0)</text>

  <!-- 행 구분선 -->
  <line x1="257" y1="230" x2="257" y2="252" stroke="currentColor" stroke-width="1.5" stroke-dasharray="2,2" opacity="0.25"/>

  <!-- Row 1 ~ 1079 -->
  <rect x="264" y="228" width="48" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6"/>
  <text fill="currentColor" x="288" y="245" text-anchor="middle" font-size="7" font-family="monospace">(0,1)</text>
  <text fill="currentColor" x="328" y="245" text-anchor="middle" font-size="9" opacity="0.35">···</text>
  <rect x="342" y="228" width="68" height="26" rx="2" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.6"/>
  <text fill="currentColor" x="376" y="245" text-anchor="middle" font-size="7" font-family="monospace">(1919,1079)</text>

  <!-- 행 범위 표시 -->
  <line x1="22" y1="260" x2="252" y2="260" stroke="currentColor" stroke-width="0.7" opacity="0.3"/>
  <text fill="currentColor" x="137" y="273" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.4">← row 0 (1920 픽셀) →</text>
  <line x1="264" y1="260" x2="410" y2="260" stroke="currentColor" stroke-width="0.7" opacity="0.3"/>
  <text fill="currentColor" x="337" y="273" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.4">← row 1 ~ 1079 →</text>

  <!-- 주소 증가 방향 -->
  <line x1="22" y1="290" x2="428" y2="290" stroke="currentColor" stroke-width="0.8" opacity="0.2"/>
  <polygon points="426,287 434,290 426,293" fill="currentColor" opacity="0.2"/>
  <text fill="currentColor" x="228" y="303" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.35">메모리 주소 증가 방향</text>

  <!-- ===== 크기 계산 ===== -->
  <rect x="110" y="320" width="300" height="55" rx="6" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="260" y="343" text-anchor="middle" font-size="10" font-family="monospace">1920 × 1080 × 4 = 8,294,400 바이트</text>
  <text fill="currentColor" x="260" y="363" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">≒ 약 8 MB</text>
</svg>
</div>

<br>

HDR(High Dynamic Range) 렌더링에서는 채널당 8비트로는 밝기 범위가 부족하므로, RGBA16F(채널당 16비트 부동소수점, 픽셀당 8바이트)나 R11G11B10F(픽셀당 4바이트, 알파 채널 없음) 등의 형식을 사용합니다.

형식이 바뀌면 픽셀당 크기가 달라지고, 프레임 버퍼 전체의 메모리 크기도 비례하여 변합니다.

GPU는 렌더링 과정에서 프레임 버퍼에 픽셀을 쓰고, 블렌딩 시에는 기존 값을 다시 읽어야 하므로, 버퍼가 클수록 매 프레임의 대역폭 소비가 증가합니다.

<br>

여기까지 설명한 프레임 버퍼는 색상 데이터만 담는 **색상 버퍼(Color Buffer)**에 해당합니다.

실제 렌더링에서는 색상 버퍼 외에도 깊이 버퍼, 스텐실 버퍼 등 보조 버퍼가 함께 사용됩니다.

OpenGL의 프레임 버퍼 오브젝트(FBO)처럼, 그래픽스 API에서 "프레임 버퍼"라고 부르는 것은 이 보조 버퍼들까지 포함한 버퍼 집합 전체를 가리킵니다.

---

## 깊이 버퍼 (Z-Buffer)

3D 장면에서는 여러 오브젝트가 화면의 같은 픽셀 위치에 겹칠 수 있습니다.

현실 세계에서 가까운 물체가 먼 물체를 가리듯이, 렌더링에서도 카메라에 가까운 오브젝트가 먼 오브젝트를 가려야 자연스러운 3D 장면이 됩니다.

이 **가시성 판별(Visibility Determination)**을 수행하는 것이 **깊이 버퍼(Depth Buffer)**, 또는 **Z-Buffer**입니다.

<br>

깊이 버퍼는 프레임 버퍼와 동일한 해상도를 가지며, 각 픽셀 위치마다 현재까지 기록된 가장 가까운 프래그먼트의 깊이 값을 저장합니다.

깊이 값은 [그래픽스 수학 (3)](/dev/unity/GraphicsMath-3/)에서 다룬 NDC(Normalized Device Coordinates)에서의 z 값을 기반으로 합니다.

DirectX, Metal, Vulkan에서 NDC z 범위는 [0, 1]이고, OpenGL에서는 [-1, 1]입니다. 이 절에서는 [0, 1] 범위를 기준으로 하며, 0.0이 카메라에 가장 가깝고 1.0이 가장 먼 값입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 620" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="260" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">깊이 버퍼의 동작 원리</text>
  <text fill="currentColor" x="260" y="34" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">전통적 매핑 기준: 가까움 = 0.0 / 먼 = 1.0</text>

  <!-- 초기화 단계 -->
  <rect x="130" y="50" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="64" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">프레임 시작</text>
  <text fill="currentColor" x="260" y="79" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">깊이 버퍼 모든 값 → 1.0 (가장 먼 거리)</text>

  <!-- 화살표: 초기화 → A -->
  <line x1="260" y1="86" x2="260" y2="104" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="255,102 260,110 265,102" fill="currentColor"/>

  <!-- ===== 삼각형 A ===== -->
  <rect x="30" y="114" width="460" height="130" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="132" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">삼각형 A — 깊이 0.3</text>

  <!-- A: 비교 영역 -->
  <rect x="50" y="142" width="200" height="50" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text fill="currentColor" x="150" y="159" text-anchor="middle" font-size="10" font-family="sans-serif">깊이 버퍼 현재값: 1.0</text>
  <text fill="currentColor" x="150" y="174" text-anchor="middle" font-size="10" font-family="sans-serif">프래그먼트 깊이: 0.3</text>
  <text fill="currentColor" x="150" y="187" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">비교: 0.3 &lt; 1.0</text>

  <!-- A: 화살표 비교 → 결과 -->
  <line x1="250" y1="167" x2="278" y2="167" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="276,163 284,167 276,171" fill="currentColor"/>

  <!-- A: 결과 (통과) -->
  <rect x="288" y="142" width="184" height="50" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="380" y="158" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">통과</text>
  <text fill="currentColor" x="380" y="172" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">색상 버퍼에 색상 기록</text>
  <text fill="currentColor" x="380" y="184" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">깊이 버퍼 → 0.3 갱신</text>

  <!-- A: 깊이 버퍼 상태 표시 -->
  <text fill="currentColor" x="260" y="232" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">깊이 버퍼 값: 1.0 → 0.3</text>

  <!-- 화살표: A → B -->
  <line x1="260" y1="244" x2="260" y2="262" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="255,260 260,268 265,260" fill="currentColor"/>

  <!-- ===== 삼각형 B ===== -->
  <rect x="30" y="272" width="460" height="130" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text fill="currentColor" x="260" y="290" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">삼각형 B — 같은 위치, 깊이 0.7</text>

  <!-- B: 비교 영역 -->
  <rect x="50" y="300" width="200" height="50" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text fill="currentColor" x="150" y="317" text-anchor="middle" font-size="10" font-family="sans-serif">깊이 버퍼 현재값: 0.3</text>
  <text fill="currentColor" x="150" y="332" text-anchor="middle" font-size="10" font-family="sans-serif">프래그먼트 깊이: 0.7</text>
  <text fill="currentColor" x="150" y="345" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">비교: 0.7 &gt; 0.3</text>

  <!-- B: 화살표 비교 → 결과 -->
  <line x1="250" y1="325" x2="278" y2="325" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="276,321 284,325 276,329" fill="currentColor"/>

  <!-- B: 결과 (실패) -->
  <rect x="288" y="300" width="184" height="50" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text fill="currentColor" x="380" y="316" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif" opacity="0.5">실패</text>
  <text fill="currentColor" x="380" y="330" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.4">색상 버퍼 변경 없음</text>
  <text fill="currentColor" x="380" y="342" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.4">프래그먼트 B 폐기</text>

  <!-- B: 깊이 버퍼 상태 표시 -->
  <text fill="currentColor" x="260" y="390" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">깊이 버퍼 값: 0.3 유지</text>

  <!-- 화살표: B → C -->
  <line x1="260" y1="400" x2="260" y2="418" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="255,416 260,424 265,416" fill="currentColor"/>

  <!-- ===== 삼각형 C ===== -->
  <rect x="30" y="428" width="460" height="130" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="446" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">삼각형 C — 같은 위치, 깊이 0.1</text>

  <!-- C: 비교 영역 -->
  <rect x="50" y="456" width="200" height="50" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text fill="currentColor" x="150" y="473" text-anchor="middle" font-size="10" font-family="sans-serif">깊이 버퍼 현재값: 0.3</text>
  <text fill="currentColor" x="150" y="488" text-anchor="middle" font-size="10" font-family="sans-serif">프래그먼트 깊이: 0.1</text>
  <text fill="currentColor" x="150" y="501" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">비교: 0.1 &lt; 0.3</text>

  <!-- C: 화살표 비교 → 결과 -->
  <line x1="250" y1="481" x2="278" y2="481" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="276,477 284,481 276,485" fill="currentColor"/>

  <!-- C: 결과 (통과) -->
  <rect x="288" y="456" width="184" height="50" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="380" y="472" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">통과</text>
  <text fill="currentColor" x="380" y="486" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">색상 버퍼에 새 색상 기록</text>
  <text fill="currentColor" x="380" y="498" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">깊이 버퍼 → 0.1 갱신</text>

  <!-- C: 깊이 버퍼 상태 표시 -->
  <text fill="currentColor" x="260" y="546" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">깊이 버퍼 값: 0.3 → 0.1</text>

  <!-- 최종 결과 -->
  <rect x="130" y="566" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="581" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">최종 깊이 버퍼 값: 0.1</text>
  <text fill="currentColor" x="260" y="595" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">삼각형 C의 색상이 화면에 표시</text>
</svg>
</div>

<br>

깊이 테스트 덕분에 **불투명 오브젝트**는 렌더링 순서와 무관하게, 3D 공간에서 앞에 있는 것이 뒤에 있는 것을 자연스럽게 가립니다.

삼각형 A를 먼저 그리든 삼각형 C를 먼저 그리든, 최종 결과에서는 가장 가까운 삼각형의 색상만 남습니다.

반투명 오브젝트에서는 사정이 달라지는데, 이는 블렌딩 절에서 다룹니다.

<br>

깊이 버퍼의 일반적인 형식은 **D24S8**(깊이 24비트 + 스텐실 8비트, 합계 32비트)이며, 픽셀당 4바이트입니다. 여기서 스텐실 8비트가 무엇인지는 스텐실 버퍼 절에서 다룹니다.

D24S8은 깊이 테스트와 스텐실 테스트를 모두 지원하므로 대부분의 3D 렌더링 시나리오에서 기본값으로 사용되며, Unity도 대부분의 플랫폼에서 이 형식을 기본으로 채택합니다.

<br>

깊이 전용 형식으로 **D32F**(32비트 부동소수점)를 사용하는 경우도 있습니다.

스텐실이 필요 없고 깊이 정밀도가 특별히 중요한 상황에서 선택됩니다.

비행 시뮬레이터처럼 콕핏(0.1m)과 지형(수십\~수백 km)을 동시에 렌더링하는 경우, 24비트 정수로는 정밀도가 부족하여 z-fighting이 발생할 수 있습니다.

부동소수점의 정밀도 분포(0 근처에 밀집)를 활용하는 Reversed-Z 기법과 D32F를 조합하면 원거리 z-fighting 감소 효과가 극대화됩니다.

섀도우 맵에서도 깊이 정밀도 부족이 shadow acne의 직접적 원인이 되므로 D32F를 선택하기도 합니다.

<br>

높은 깊이 정밀도와 스텐실을 동시에 필요로 하는 경우를 위해 **D32F_S8**(32비트 부동소수점 깊이 + 8비트 스텐실, 픽셀당 8바이트)도 존재하지만, 메모리·대역폭 비용이 두 배이므로 흔하지는 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="240" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">깊이 버퍼 형식과 메모리</text>

  <!-- D24S8 형식 라벨 -->
  <text fill="currentColor" x="40" y="52" font-size="11" font-weight="bold" font-family="sans-serif">D24S8 형식</text>
  <text fill="currentColor" x="40" y="65" font-size="9" font-family="sans-serif" opacity="0.5">가장 일반적</text>

  <!-- D24S8: 깊이 24비트 박스 (75%) -->
  <rect x="40" y="76" width="300" height="54" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="190" y="96" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">깊이 (24비트)</text>
  <text fill="currentColor" x="190" y="112" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">0 ~ 16,777,215</text>
  <text fill="currentColor" x="190" y="124" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">75%</text>

  <!-- D24S8: 스텐실 8비트 박스 (25%) -->
  <rect x="340" y="76" width="100" height="54" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="390" y="96" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">스텐실 (8비트)</text>
  <text fill="currentColor" x="390" y="112" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">0 ~ 255</text>
  <text fill="currentColor" x="390" y="124" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">25%</text>

  <!-- D24S8 바이트 표시 -->
  <text fill="currentColor" x="240" y="148" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">픽셀당 4바이트 (32비트)</text>

  <!-- D32F 형식 라벨 -->
  <text fill="currentColor" x="40" y="178" font-size="11" font-weight="bold" font-family="sans-serif">D32F 형식</text>

  <!-- D32F: 깊이 32비트 박스 (전체 폭) -->
  <rect x="40" y="190" width="400" height="54" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="240" y="212" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">깊이 (32비트 float)</text>
  <text fill="currentColor" x="240" y="228" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">높은 정밀도</text>

  <!-- D32F 바이트 표시 -->
  <text fill="currentColor" x="240" y="260" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">픽셀당 4바이트 (스텐실 없음)</text>

  <!-- 메모리 크기 계산 -->
  <text fill="currentColor" x="240" y="278" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">해상도 1920x1080 기준 D24S8: 1920 x 1080 x 4 = 약 8 MB</text>
</svg>
</div>

### 깊이 값의 비선형성

깊이 버퍼에 저장되는 값은 3D 공간의 실제 거리와 선형 관계가 아닙니다.

만약 선형이라면 near = 1m, far = 1000m일 때 거리 500m 지점이 버퍼 값 약 0.5에 대응하겠지만, 실제로는 그렇지 않습니다.

<br>

버텍스 셰이더가 출력한 클립 좌표 (x, y, z, w)에서 GPU는 모든 성분을 w로 나눕니다.

이것이 **원근 나눗셈(perspective divide)**입니다.

원근 투영 행렬은 w에 뷰 공간의 z값을 넣도록 설계되어 있으므로, NDC z = z'/w = z'/z가 되어 결과가 자연스럽게 **1/z에 비례**하는 형태가 됩니다.

<br>

이 비선형 변환의 결과, near = 1, far = 1000일 때 깊이 값 분포는 다음과 같습니다.

| 거리(z) | NDC 깊이 값 |
|---------|------------|
| 1 (near) | 0.000 |
| 2 | ≈ 0.501 |
| 10 | ≈ 0.901 |
| 100 | ≈ 0.991 |
| 500 | ≈ 0.999 |
| 1000 (far) | 1.000 |

버퍼 범위의 **절반(약 0.0\~0.5)**이 거리 1\~2 구간(단 1m)에 사용되고, **나머지 절반(약 0.5\~1.0)**이 2\~1000 구간(998m)에 사용됩니다.

near plane 근처에서는 깊이 값이 촘촘하게 변하여 정밀도가 높고, far plane 근처에서는 깊이 값이 거의 변하지 않아 정밀도가 낮습니다.

<br>

정밀도가 낮은 영역에서는 3D 공간에서 서로 다른 거리에 있는 두 오브젝트가 깊이 버퍼에서 같은 값으로 기록될 수 있습니다.

이 상황에서 두 오브젝트의 표면이 매 프레임마다 번갈아 앞으로 나타나는 **Z-fighting** 현상이 발생합니다.

<br>

이것이 앞서 D32F + Reversed-Z 조합을 언급한 이유이기도 합니다. 이 조합을 이해하려면 먼저 부동소수점의 정밀도 분포를 알아야 합니다.

<br>

IEEE 754 부동소수점은 지수(exponent) 구조 때문에 0에 가까울수록 표현 가능한 값이 촘촘합니다. 0.000001과 0.000002는 쉽게 구분하지만, 0.999998과 0.999999는 구분하기 어렵습니다.

깊이 버퍼가 부동소수점(D32F)일 때, 전통적 매핑(near=0, far=1)에서는 1/z 분포와 float 정밀도 분포가 **같은 방향**으로 겹칩니다.

| | near(가까운 곳) | far(먼 곳) |
|---|---|---|
| 1/z 분포 | 깊이 값이 촘촘 (정밀도 높음) | 깊이 값이 성김 (정밀도 낮음) |
| float 정밀도 | 0 근처 → 촘촘 (정밀도 높음) | 1 근처 → 성김 (정밀도 낮음) |
| **합산** | **이미 충분한데 더 정밀** | **이미 부족한데 더 부족** |

가까운 곳에 정밀도가 과잉으로 몰리고, 먼 곳은 이중으로 부족해집니다.

<br>

원근 투영의 비선형성(1/z) 자체는 바꿀 수 없지만, 깊이 값의 매핑 방향은 바꿀 수 있습니다. Reversed-Z는 near=1, far=0으로 뒤집어 float의 0 근처 정밀도를 먼 거리 쪽에 배분합니다.

| | near(가까운 곳) | far(먼 곳) |
|---|---|---|
| 1/z 분포 | 깊이 값이 촘촘 (변함없음) | 깊이 값이 성김 (변함없음) |
| float 정밀도 | **1 근처 → 성김** | **0 근처 → 촘촘** |
| **합산** | **1/z의 높은 정밀도를 float이 적당히 깎음** | **1/z의 낮은 정밀도를 float이 보충** |

두 분포가 서로 상쇄되어, 전체 깊이 범위에 걸쳐 정밀도가 훨씬 균일해집니다. 이 효과는 float 깊이 버퍼(D32F)에서 뚜렷하며, 값 간격이 균일한 정수 깊이 버퍼(D24S8)에서는 효과가 없습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="260" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">거리 구간별 깊이 버퍼 사용 비율</text>
  <text fill="currentColor" x="260" y="35" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">near = 1, far = 1000 — 막대가 넓을수록 정밀도 높음</text>

  <!-- Row 1: z=1→2 (1m) → 50.1% -->
  <text fill="currentColor" x="128" y="66" text-anchor="end" font-size="11" font-family="sans-serif" font-weight="bold">1 → 2</text>
  <text fill="currentColor" x="128" y="80" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">거리 1 m</text>
  <rect x="138" y="56" width="310" height="28" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="456" y="75" text-anchor="start" font-size="10" font-family="sans-serif" font-weight="bold">50.1%</text>

  <!-- Row 2: z=2→10 (8m) → 40.0% -->
  <text fill="currentColor" x="128" y="110" text-anchor="end" font-size="11" font-family="sans-serif" font-weight="bold">2 → 10</text>
  <text fill="currentColor" x="128" y="124" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">거리 8 m</text>
  <rect x="138" y="100" width="248" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="394" y="119" text-anchor="start" font-size="10" font-family="sans-serif" font-weight="bold">40.0%</text>

  <!-- Row 3: z=10→100 (90m) → 9.0% -->
  <text fill="currentColor" x="128" y="154" text-anchor="end" font-size="11" font-family="sans-serif" font-weight="bold">10 → 100</text>
  <text fill="currentColor" x="128" y="168" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">거리 90 m</text>
  <rect x="138" y="144" width="56" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="202" y="163" text-anchor="start" font-size="10" font-family="sans-serif" font-weight="bold">9.0%</text>

  <!-- Row 4: z=100→1000 (900m) → 0.9% -->
  <text fill="currentColor" x="128" y="198" text-anchor="end" font-size="11" font-family="sans-serif" font-weight="bold">100 → 1000</text>
  <text fill="currentColor" x="128" y="212" text-anchor="end" font-size="9" font-family="sans-serif" opacity="0.5">거리 900 m</text>
  <rect x="138" y="188" width="6" height="28" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="152" y="207" text-anchor="start" font-size="10" font-family="sans-serif" font-weight="bold">0.9%</text>
</svg>
</div>

<br>

Z-fighting을 줄이는 가장 직접적인 방법은 near plane과 far plane의 비율을 줄이는 것입니다.

깊이 값이 1/z에 비례하므로, 이 비율이 클수록(예: near=0.01, far=1000 → 1:100,000) 가까운 쪽에 정밀도가 과도하게 집중되고, 먼 거리의 정밀도는 더욱 부족해집니다.

near=0.3, far=1000이면 비율은 1:3,333으로, 대부분의 장면에서 충분한 정밀도를 확보할 수 있습니다.

Unity 카메라의 Near Clipping Plane 기본값이 0.3인 것도 이 이유입니다.

<br>

현대 렌더링 엔진에서는 **Reversed-Z**라는 기법으로 깊이 정밀도를 개선합니다.

이 절의 깊이 테스트 설명은 가까울수록 0.0, 멀수록 1.0인 전통적 매핑을 기준으로 했지만, Reversed-Z에서는 방향을 뒤집어 near plane이 1.0, far plane이 0.0에 대응합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="240" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">버퍼 형식별 값 간격 비교</text>

  <!-- ===== D32F (부동소수점) ===== -->
  <text fill="currentColor" x="20" y="50" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">D32F (부동소수점)</text>
  <text fill="currentColor" x="200" y="50" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">값 간격 불균일</text>

  <!-- 바: 0.0 근처 -->
  <text fill="currentColor" x="18" y="75" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.6">0.0 근처</text>
  <rect x="80" y="64" width="300" height="16" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="388" y="76" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">촘촘</text>

  <!-- 바: 0.5 근처 -->
  <text fill="currentColor" x="18" y="97" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.6">0.5 근처</text>
  <rect x="80" y="86" width="150" height="16" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="238" y="98" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">중간</text>

  <!-- 바: 1.0 근처 -->
  <text fill="currentColor" x="18" y="119" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.6">1.0 근처</text>
  <rect x="80" y="108" width="60" height="16" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="148" y="120" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">성김</text>

  <!-- 구분선 -->
  <line x1="20" y1="138" x2="460" y2="138" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>

  <!-- ===== D24S8 (정수) ===== -->
  <text fill="currentColor" x="20" y="162" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">D24S8 (정수)</text>
  <text fill="currentColor" x="170" y="162" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">값 간격 균일</text>

  <!-- 바: 0.0 근처 -->
  <text fill="currentColor" x="18" y="187" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.6">0.0 근처</text>
  <rect x="80" y="176" width="150" height="16" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="238" y="188" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">동일</text>

  <!-- 바: 0.5 근처 -->
  <text fill="currentColor" x="18" y="209" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.6">0.5 근처</text>
  <rect x="80" y="198" width="150" height="16" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="238" y="210" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">동일</text>

  <!-- 바: 1.0 근처 -->
  <text fill="currentColor" x="18" y="231" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.6">1.0 근처</text>
  <rect x="80" y="220" width="150" height="16" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="238" y="232" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">동일</text>
</svg>
</div>

이 차이가 Reversed-Z의 효과를 결정합니다.

| | 전통적 매핑 | Reversed-Z |
|---|---|---|
| **D32F** (불균일) | 1/z 편향 + float 편향 = 이중 편향 | 1/z 편향 ↔ float 편향 = **상쇄** |
| **D24S8** (균일) | 1/z 편향만 존재 | 1/z 편향만 존재 — **변화 없음** |

<br>

Unity는 DirectX, Metal, Vulkan 플랫폼에서 Reversed-Z를 기본으로 사용합니다. OpenGL/OpenGL ES에서는 NDC z 범위가 [-1, 1]이므로, near를 1에, far를 0에 매핑하는 Reversed-Z 기법을 그대로 적용할 수 없어 Reversed-Z가 사용되지 않습니다.

Reversed-Z를 사용하는 플랫폼에서는 깊이 버퍼의 초기화 값이 1.0이 아닌 0.0이 되며, 깊이 비교 함수도 Less 대신 Greater로 바뀝니다.

Unity가 이 설정을 자동으로 처리하므로 셰이더 작성 시 별도 대응은 불필요하지만, 깊이 버퍼를 직접 읽거나 커스텀 깊이 연산을 수행할 때는 깊이 방향이 플랫폼에 따라 다르다는 점을 인지해야 합니다.

Unity는 이를 위해 셰이더에서 `UNITY_REVERSED_Z` 매크로를 제공합니다.

---

## Early-Z vs Late-Z

렌더링 파이프라인의 논리적 순서에서 깊이 테스트는 프래그먼트 셰이더 **이후**에 위치합니다.

색상을 계산한 뒤에야 폐기 여부가 결정되므로, 가려질 프래그먼트에도 셰이더 비용이 그대로 소모됩니다.

**Early-Z**는 이 순서를 뒤집어, 프래그먼트 셰이더 **이전**에 깊이 테스트를 먼저 수행합니다.

가려질 프래그먼트는 셰이딩 자체를 건너뛰므로 연산 비용이 절감됩니다.

### Late-Z (논리적 순서)

Late-Z는 논리적 순서 그대로, 프래그먼트 셰이더가 실행된 **이후** 깊이 테스트를 수행하는 방식입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- 제목 -->
  <text x="180" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Late-Z 흐름</text>

  <!-- 1단계: 래스터화 -->
  <rect x="90" y="40" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="63" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">래스터화</text>

  <!-- 화살표 1→2 -->
  <line x1="180" y1="76" x2="180" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,95 185,95 180,103" fill="currentColor"/>

  <!-- 2단계: 프래그먼트 셰이더 (강조) -->
  <rect x="90" y="105" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>
  <text x="180" y="128" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">프래그먼트 셰이더</text>
  <text x="290" y="128" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">← 셰이딩 비용 발생</text>

  <!-- 화살표 2→3 -->
  <line x1="180" y1="141" x2="180" y2="163" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,160 185,160 180,168" fill="currentColor"/>

  <!-- 3단계: 깊이 테스트 (강조) -->
  <rect x="90" y="170" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>
  <text x="180" y="193" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">깊이 테스트</text>
  <text x="290" y="193" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">← 셰이딩 이후 폐기 판정</text>

  <!-- 화살표 3→4 -->
  <line x1="180" y1="206" x2="180" y2="228" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,225 185,225 180,233" fill="currentColor"/>

  <!-- 4단계: 프레임 버퍼 기록 -->
  <rect x="90" y="235" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="258" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">프레임 버퍼 기록</text>

  <!-- 문제 영역 -->
  <rect x="40" y="300" width="280" height="90" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="180" y="322" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">문제</text>
  <text x="180" y="345" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">가려질 프래그먼트에도 셰이딩 비용이 전부 소모됨</text>
  <text x="180" y="365" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">셰이더가 복잡할수록 낭비가 커짐</text>
</svg>
</div>

### Early-Z (최적화)

Early-Z는 프래그먼트 셰이더 **이전에** 깊이 테스트를 수행합니다.

해당 픽셀 위치에 이미 더 가까운 깊이 값이 기록되어 있으면, 셰이더를 실행하지 않고 프래그먼트를 바로 폐기합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- 제목 -->
  <text x="180" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Early-Z 흐름</text>

  <!-- 1단계: 래스터화 -->
  <rect x="90" y="40" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="63" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">래스터화</text>

  <!-- 화살표 1→2 -->
  <line x1="180" y1="76" x2="180" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,95 185,95 180,103" fill="currentColor"/>

  <!-- 2단계: Early-Z 테스트 (강조) -->
  <rect x="90" y="105" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>
  <text x="180" y="128" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">Early-Z 테스트</text>
  <text x="290" y="128" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">← 깊이 비교 먼저 수행</text>

  <!-- 실패 분기: 오른쪽으로 -->
  <line x1="270" y1="123" x2="295" y2="123" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.5"/>
  <line x1="295" y1="123" x2="295" y2="168" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.5"/>
  <polygon points="290,165 300,165 295,173" fill="currentColor" opacity="0.5"/>
  <rect x="235" y="175" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.5"/>
  <text x="295" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">프래그먼트 폐기</text>
  <text x="295" y="203" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">(셰이딩 건너뜀)</text>
  <text x="283" y="156" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">실패</text>

  <!-- 화살표 2→3 (통과) -->
  <line x1="180" y1="141" x2="180" y2="218" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,215 185,215 180,223" fill="currentColor"/>
  <text x="168" y="183" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">통과</text>

  <!-- 3단계: 프래그먼트 셰이더 -->
  <rect x="90" y="225" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="248" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">프래그먼트 셰이더</text>
  <text x="290" y="248" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">← 보이는 프래그먼트만 셰이딩</text>

  <!-- 화살표 3→4 -->
  <line x1="180" y1="261" x2="180" y2="283" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,280 185,280 180,288" fill="currentColor"/>

  <!-- 4단계: 프레임 버퍼 기록 -->
  <rect x="90" y="290" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="313" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">프레임 버퍼 기록</text>

  <!-- 이점 영역 -->
  <rect x="40" y="350" width="280" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="180" y="370" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">이점</text>
  <text x="180" y="388" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">가려진 프래그먼트의 셰이딩 비용을 미리 절약</text>
</svg>
</div>

<br>

Early-Z가 효과적으로 작동하려면, 불투명 오브젝트를 카메라 기준으로 **앞에서 뒤(front-to-back)** 순서로 렌더링해야 합니다.

가까운 오브젝트를 먼저 그리면 깊이 버퍼에 작은 값이 먼저 기록되고, 이후 도착하는 먼 오브젝트의 프래그먼트는 Early-Z에서 바로 폐기됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Early-Z와 렌더링 순서</text>

  <!-- 구분선 -->
  <line x1="280" y1="34" x2="280" y2="295" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>

  <!-- 좌측 헤더 -->
  <text x="142" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">앞→뒤 (최적)</text>

  <!-- 우측 헤더 -->
  <text x="420" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">뒤→앞 (비효과적)</text>

  <!-- ===== 좌측 (앞→뒤) ===== -->

  <!-- 1) 캐릭터 → 통과 -->
  <rect x="15" y="64" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="83" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1) 캐릭터</text>
  <text x="108" y="83" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.1</text>
  <text x="30" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">통과, 셰이딩, 기록</text>

  <!-- 2) 건물 → Early-Z 실패 -->
  <rect x="15" y="122" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.5"/>
  <text x="30" y="141" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.5">2) 건물</text>
  <text x="93" y="141" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.35">깊이 0.5 — 가려진 부분</text>
  <text x="30" y="158" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.45">Early-Z 실패 → 셰이딩 건너뜀</text>

  <!-- 3) 배경 → Early-Z 실패 -->
  <rect x="15" y="180" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.5"/>
  <text x="30" y="199" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.5">3) 배경</text>
  <text x="85" y="199" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.35">깊이 0.9 — 가려진 부분</text>
  <text x="30" y="216" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.45">Early-Z 실패 → 셰이딩 건너뜀</text>

  <!-- 좌측 결과 -->
  <rect x="15" y="248" width="250" height="40" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="140" y="273" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">셰이딩 1회 — 비용 절약</text>

  <!-- ===== 우측 (뒤→앞) ===== -->

  <!-- 1) 배경 → 통과 -->
  <rect x="295" y="64" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="83" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1) 배경</text>
  <text x="375" y="83" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.9</text>
  <text x="310" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">통과, 셰이딩, 기록</text>

  <!-- 2) 건물 → 통과, 덮어쓰기 -->
  <rect x="295" y="122" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="141" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2) 건물</text>
  <text x="375" y="141" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.5</text>
  <text x="310" y="158" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">통과, 셰이딩, 덮어쓰기</text>
  <text x="540" y="158" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">(배경 낭비)</text>

  <!-- 3) 캐릭터 → 통과, 덮어쓰기 -->
  <rect x="295" y="180" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="199" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3) 캐릭터</text>
  <text x="390" y="199" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.1</text>
  <text x="310" y="216" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">통과, 셰이딩, 덮어쓰기</text>
  <text x="540" y="216" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">(건물 낭비)</text>

  <!-- 우측 결과 -->
  <rect x="295" y="248" width="250" height="40" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="420" y="273" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">셰이딩 3회 — 2회 낭비 (오버드로우)</text>
</svg>
</div>

<br>

Unity의 렌더링 파이프라인(URP, Built-in, HDRP)은 Early-Z 효율을 위해 불투명 오브젝트를 자동으로 카메라 기준 앞→뒤 순서로 정렬합니다.

Unity는 렌더링 순서를 **렌더 큐(Render Queue)**라는 번호 체계로 관리하는데, 불투명 오브젝트가 속하는 Opaque 큐에 이 앞→뒤 정렬이 적용됩니다.

### Early-Z가 작동하지 않는 경우

Early-Z가 비활성화되거나 효과가 제한되는 경우가 있습니다.

<br>

첫째, **Alpha Test(discard/clip)** — 셰이더에서 `discard` 명령으로 프래그먼트를 폐기하는 경우, 셰이더를 실행해봐야 해당 프래그먼트가 살아남는지 알 수 있습니다.

Early-Z는 깊이 비교뿐 아니라 통과한 프래그먼트의 깊이를 버퍼에 미리 기록하므로, `discard`로 사라질 프래그먼트의 깊이까지 버퍼에 남아 뒤의 오브젝트를 잘못 가릴 수 있습니다.

GPU는 이를 방지하기 위해 해당 드로우 콜의 Early-Z를 비활성화하거나 크게 제한합니다. [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 TBDR 환경의 alpha test 비용도 이 비활성화에서 비롯됩니다.

<br>

둘째, **셰이더에서 깊이 값을 수정**하는 경우 — 프래그먼트 셰이더가 출력 깊이를 직접 변경하면(`SV_Depth` 출력 등), 래스터화 단계에서 보간된 깊이와 최종 출력 깊이가 달라집니다.

Early-Z는 래스터화 단계의 깊이를 기준으로 판단하므로, 셰이더가 깊이를 바꾸면 판단이 틀어집니다. 이 경우에도 GPU는 Early-Z를 비활성화합니다.

<br>

셋째, **깊이 쓰기 비활성화** — `ZWrite Off`로 깊이 쓰기를 끄면 깊이 버퍼가 갱신되지 않습니다.

Early-Z 테스트 자체는 여전히 수행되므로, 이미 깊이 버퍼에 기록된 불투명 오브젝트 뒤에 있는 프래그먼트는 걸러집니다.

다만 깊이를 새로 기록하지 않으므로, 이 오브젝트 자체가 이후 드로우 콜의 Early-Z 판단에 기여하지 못합니다.

<br>

반투명 오브젝트가 `ZWrite Off`를 사용하는 것도 같은 이유입니다.

반투명 오브젝트가 깊이를 기록하면, 그 뒤에 있는 오브젝트가 깊이 테스트에서 탈락하여 투명한 면 너머로 보여야 할 장면이 사라집니다.

따라서 반투명 오브젝트는 깊이를 읽기만 하고 쓰지 않으므로, Early-Z 최적화 효과가 제한됩니다.

---

## 스텐실 버퍼

깊이 버퍼가 "어떤 프래그먼트가 앞에 있는가"를 판별한다면, **스텐실 버퍼(Stencil Buffer)**는 "이 픽셀에 그릴 것인가, 말 것인가"를 판별합니다.

각 픽셀에 8비트 정수 값(0~255)을 저장하며, 앞서 다룬 D24S8 형식에서 깊이 24비트 옆의 나머지 8비트가 스텐실 버퍼입니다.

<br>

프래그먼트가 도착하면, 해당 픽셀에 기록된 스텐실 값과 미리 설정한 참조 값을 비교합니다.

조건을 만족하면 그리고, 만족하지 않으면 건너뜁니다.

이런 **조건부 렌더링**을 활용하면, 특정 영역에 스텐실 값을 먼저 기록해 둔 뒤 그 위치에만 그리거나 피해서 그릴 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 제목 -->
  <text x="220" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">스텐실 버퍼의 기본 동작</text>

  <!-- 설정 영역 -->
  <rect x="40" y="36" width="360" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="54" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">렌더링 시 스텐실 테스트 설정</text>
  <text x="60" y="72" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">1) 참조 값(Ref): 비교에 사용할 기준 값 (0~255)</text>
  <text x="60" y="87" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">2) 비교 함수(Comp): Equal, NotEqual, Less, Greater 등</text>
  <text x="60" y="102" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">3) 통과/실패 시 동작(Pass/Fail Op): Keep, Replace, Increment 등</text>

  <!-- 동작 흐름 레이블 -->
  <text x="220" y="134" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">동작 흐름</text>

  <!-- 1단계: 프래그먼트 도착 -->
  <rect x="110" y="146" width="180" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="167" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프래그먼트 도착</text>

  <!-- 화살표 1→2 -->
  <line x1="200" y1="178" x2="200" y2="198" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,195 205,195 200,203" fill="currentColor"/>

  <!-- 2단계: 스텐실 테스트 (강조) -->
  <rect x="90" y="205" width="220" height="40" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="2"/>
  <text x="200" y="222" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스텐실 테스트</text>
  <text x="200" y="237" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">버퍼 값과 참조 값 비교</text>

  <!-- 스텐실 실패 분기: 오른쪽 -->
  <line x1="310" y1="225" x2="340" y2="225" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.5"/>
  <line x1="340" y1="225" x2="340" y2="260" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.5"/>
  <polygon points="335,257 345,257 340,265" fill="currentColor" opacity="0.5"/>
  <rect x="290" y="267" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.5"/>
  <text x="355" y="282" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Fail Op 실행</text>
  <text x="355" y="296" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">프래그먼트 폐기</text>
  <text x="328" y="252" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">실패</text>

  <!-- 화살표 2→3 (통과) -->
  <line x1="200" y1="245" x2="200" y2="310" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,307 205,307 200,315" fill="currentColor"/>
  <text x="188" y="280" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">통과</text>

  <!-- 3단계: 깊이 테스트 -->
  <rect x="110" y="317" width="180" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="340" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">깊이 테스트</text>

  <!-- 깊이 실패 분기: 오른쪽 -->
  <line x1="290" y1="335" x2="340" y2="335" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.5"/>
  <line x1="340" y1="335" x2="340" y2="368" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,2" opacity="0.5"/>
  <polygon points="335,365 345,365 340,373" fill="currentColor" opacity="0.5"/>
  <rect x="290" y="375" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.5"/>
  <text x="355" y="390" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">ZFail Op 실행</text>
  <text x="355" y="404" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">프래그먼트 폐기</text>
  <text x="328" y="361" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">실패</text>

  <!-- 화살표 3→4 (통과) -->
  <line x1="200" y1="353" x2="200" y2="418" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,415 205,415 200,423" fill="currentColor"/>
  <text x="188" y="390" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">통과</text>

  <!-- 4단계: Pass Op + 기록 -->
  <rect x="90" y="425" width="220" height="40" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="442" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Pass Op 실행</text>
  <text x="200" y="457" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프레임 버퍼에 기록</text>
</svg>
</div>

### 스텐실 버퍼의 활용 예시

**거울 효과.**

거울 표면의 영역에 스텐실 값을 기록합니다.

반사된 장면을 렌더링할 때, 스텐실 값이 존재하는 영역에만 그리도록 설정합니다.

거울 영역 밖에서는 반사 장면이 보이지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 제목 -->
  <text x="210" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">거울 효과의 스텐실 흐름</text>

  <!-- ===== 1단계 ===== -->
  <text x="210" y="46" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1단계: 거울 표면 렌더링 (스텐실 기록)</text>

  <!-- 화면 영역 (외곽 박스) -->
  <rect x="60" y="58" width="220" height="140" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="76" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">화면 영역</text>

  <!-- 거울 영역 (내부 박스, 강조) -->
  <rect x="105" y="90" width="110" height="80" rx="4" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="2"/>
  <text x="160" y="126" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">거울 표면</text>
  <text x="160" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">스텐실 = 1</text>

  <!-- 나머지 영역 주석 -->
  <text x="305" y="100" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">거울 영역의 스텐실 = 1</text>
  <text x="305" y="116" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">나머지 영역의 스텐실 = 0</text>

  <!-- 나머지 영역 스텐실 = 0 표시 -->
  <text x="90" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">스텐실 = 0</text>
  <text x="245" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">스텐실 = 0</text>

  <!-- 화살표 1단계 → 2단계 -->
  <line x1="210" y1="205" x2="210" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="205,227 215,227 210,235" fill="currentColor"/>

  <!-- ===== 2단계 ===== -->
  <text x="210" y="254" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2단계: 반사 장면 렌더링 (스텐실 테스트)</text>

  <!-- 테스트 조건 박스 -->
  <rect x="60" y="266" width="300" height="32" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="287" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Comp = Equal, Ref = 1</text>

  <!-- 결과 설명 -->
  <rect x="60" y="312" width="300" height="48" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="210" y="333" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">스텐실 = 1인 영역에만 반사 장면이 그려짐</text>
  <text x="210" y="351" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">거울 밖으로 반사 장면이 삐져나오지 않음</text>
</svg>
</div>

<br>

**아웃라인 효과.**

오브젝트를 정상적으로 렌더링하면서 스텐실에 1을 기록합니다.

이후 오브젝트를 약간 크게 확대하여 외곽선 색상으로 렌더링하되, 스텐실이 1인 영역은 제외합니다.

결과적으로 오브젝트의 가장자리에만 외곽선이 남습니다.

<br>

**포털 효과.**

포털 프레임 영역을 렌더링하면서 해당 픽셀에 스텐실 값을 기록합니다.

이후 포털 너머의 장면(별도 카메라로 촬영한 다른 공간)을 렌더링할 때, 스텐실 값이 존재하는 영역에만 그리도록 설정합니다.

포털 프레임 밖으로 다른 공간의 장면이 삐져나오지 않으므로, 프레임 안쪽에서만 다른 세계가 보이는 효과가 만들어집니다.

<br>

Unity에서 스텐실 테스트는 셰이더의 `Stencil` 블록에서 설정합니다.

앞서 설명한 참조 값(`Ref`), 비교 함수(`Comp`), 통과·실패 시 동작(`Pass`, `Fail`, `ZFail`)을 이 블록에서 지정합니다.

<br>

UI 시스템의 **Mask** 컴포넌트도 내부적으로 스텐실 버퍼를 사용합니다.

Mask 오브젝트를 렌더링할 때 해당 영역에 스텐실 값을 기록하고, 자식 UI 요소는 스텐실 값이 일치하는 픽셀에만 렌더링됩니다.

Mask를 중첩하면 비트 단위로 마스크 값을 누적하므로(1 → 3 → 7 → 15 …), 8비트 범위에서 최대 8단계까지 중첩이 가능합니다.

다만 Mask 자체가 별도의 드로우 콜을 발생시키고, 자식 요소의 머티리얼에 스텐실 설정이 추가되어 배칭이 깨질 수 있습니다.

또한 커스텀 셰이더를 사용하는 UI 요소는 기본 `UI/Default` 셰이더에 내장된 스텐실 프로퍼티(`_StencilComp`, `_Stencil`, `_StencilOp` 등)가 빠져 있으므로, 이를 명시적으로 추가하지 않으면 Mask 하위에 있어도 마스킹이 작동하지 않습니다.

<br>

2D 스프라이트 영역에서는 **SpriteMask** 컴포넌트가 같은 역할을 합니다.

SpriteMask도 내부적으로 스텐실 버퍼를 사용하며, SpriteRenderer의 **Mask Interaction** 속성을 Visible Inside Mask 또는 Visible Outside Mask로 설정하여 마스킹 여부를 제어합니다.

기본 `Sprites-Default` 셰이더에 스텐실 프로퍼티가 내장되어 있으므로 기본 셰이더를 사용하면 바로 작동하지만, 커스텀 셰이더를 쓸 때 스텐실 프로퍼티를 추가해야 하는 점은 UI Mask와 동일합니다.

<br>

반면 **RectMask2D**는 스텐실 버퍼를 사용하지 않습니다.

CPU에서 RectTransform 영역을 기준으로 영역 밖의 UI 요소를 렌더링 대상에서 제외하는 방식이므로, 드로우 콜 추가나 배칭 영향 없이 마스킹이 이루어집니다.

대신 직사각형 영역만 마스킹할 수 있어, 원형이나 불규칙한 형태의 마스킹에는 Mask를 사용해야 합니다.

---

## 블렌딩

지금까지 다룬 깊이 테스트와 스텐실 테스트는 프래그먼트를 "통과시키거나 버리는" 이진 판정이었습니다.

불투명 오브젝트는 뒤에 있는 것을 완전히 가리므로 가장 가까운 프래그먼트 하나만 남기면 되고, 이진 판정만으로 충분합니다.

반면 유리, 물, 파티클 이펙트처럼 뒤에 있는 것이 비쳐 보여야 하는 반투명 오브젝트에서는, 새로운 프래그먼트의 색상과 기존 프레임 버퍼의 색상을 **혼합(Blend)**해야 합니다.

### 블렌딩 공식

블렌딩은 소스 색상(새 프래그먼트)과 대상 색상(프레임 버퍼의 기존 값)을 각각의 팩터(factor)로 곱한 뒤 더하는 연산입니다.

$$\text{최종 색상} = \text{Src} \times \text{SrcFactor} + \text{Dst} \times \text{DstFactor}$$

- **소스 색상(Src)**: 프래그먼트 셰이더가 출력한 색상
- **대상 색상(Dst)**: 프레임 버퍼에 이미 기록된 색상
- **소스 팩터(SrcFactor)**: 소스 색상에 곱하는 계수
- **대상 팩터(DstFactor)**: 대상 색상에 곱하는 계수

### Alpha Blending

**Alpha Blending**은 소스의 알파 값(투명도)을 팩터로 사용하여 소스와 대상을 혼합합니다. 유리, 물 등 반투명 표면의 렌더링에 사용됩니다.

- **소스 팩터**: $\text{SrcAlpha}$ $(= \text{src.a})$
- **대상 팩터**: $\text{OneMinusSrcAlpha}$ $(= 1 - \text{src.a})$

$$\text{최종 색상} = \text{src.rgb} \times \text{src.a} + \text{dst.rgb} \times (1 - \text{src.a})$$

**예시** --- 소스: 빨강 $(1,\,0,\,0)$, $\text{alpha} = 0.3$ (30% 불투명) / 대상: 파랑 $(0,\,0,\,1)$

$$\begin{aligned}
\text{최종} &= (1,\,0,\,0) \times 0.3 + (0,\,0,\,1) \times 0.7 \\\\
&= (0.3,\,0,\,0) + (0,\,0,\,0.7) \\\\
&= (0.3,\,0,\,0.7) \quad \rightarrow \text{30\% 빨강 + 70\% 파랑}
\end{aligned}$$

### Additive Blending

**Additive Blending**은 소스 색상을 대상 색상에 단순히 더합니다. 파티클 이펙트(불꽃, 빛줄기 등)에서 주로 사용됩니다.

- **소스 팩터**: $\text{One}$ $(= 1)$
- **대상 팩터**: $\text{One}$ $(= 1)$

$$\text{최종 색상} = \text{src.rgb} \times 1 + \text{dst.rgb} \times 1 = \text{src.rgb} + \text{dst.rgb}$$

여러 파티클이 겹칠수록 색상이 밝아지므로, 밝은 빛 효과에 적합합니다.

### 반투명 오브젝트의 정렬 문제

반투명 오브젝트를 올바르게 렌더링하려면 **뒤에서 앞(back-to-front)** 순서로 그려야 합니다.

블렌딩은 프레임 버퍼에 이미 기록된 색상 위에 새 색상을 겹치는 연산이므로, 가장 뒤에 있는 오브젝트부터 프레임 버퍼에 깔아야 올바른 결과가 나옵니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">반투명 정렬 순서</text>

  <!-- 구분선 -->
  <line x1="280" y1="34" x2="280" y2="295" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>

  <!-- 좌측 헤더 -->
  <text x="142" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">뒤→앞 (올바른 순서)</text>

  <!-- 우측 헤더 -->
  <text x="420" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">앞→뒤 (잘못된 순서)</text>

  <!-- ===== 좌측 (뒤→앞) ===== -->

  <!-- 1) 배경 -->
  <rect x="15" y="64" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="83" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1) 배경</text>
  <text x="85" y="83" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">z=100</text>
  <text x="30" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">프레임 버퍼에 기록</text>

  <!-- 2) 유리 A -->
  <rect x="15" y="122" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="141" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2) 유리 A</text>
  <text x="105" y="141" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">z=50, α=0.5</text>
  <text x="30" y="158" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">배경과 블렌딩</text>

  <!-- 3) 유리 B -->
  <rect x="15" y="180" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="199" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3) 유리 B</text>
  <text x="105" y="199" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">z=20, α=0.3</text>
  <text x="30" y="216" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">유리 A 결과와 블렌딩</text>

  <!-- 좌측 결과 -->
  <rect x="15" y="248" width="250" height="40" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="140" y="273" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">자연스러운 반투명 겹침</text>

  <!-- ===== 우측 (앞→뒤) ===== -->

  <!-- 1) 유리 B -->
  <rect x="295" y="64" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="83" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1) 유리 B</text>
  <text x="390" y="83" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">z=20, α=0.3</text>
  <text x="310" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">빈 버퍼와 블렌딩</text>
  <text x="540" y="100" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">(배경 없음)</text>

  <!-- 2) 유리 A -->
  <rect x="295" y="122" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="141" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2) 유리 A</text>
  <text x="390" y="141" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">z=50, α=0.5</text>
  <text x="310" y="158" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">순서 뒤바뀐 블렌딩</text>

  <!-- 3) 배경 -->
  <rect x="295" y="180" width="250" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="199" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3) 배경</text>
  <text x="370" y="199" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">z=100</text>
  <text x="310" y="216" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">유리 위에 덮어쓰기</text>
  <text x="540" y="216" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">(유리가 가려짐)</text>

  <!-- 우측 결과 -->
  <rect x="295" y="248" width="250" height="40" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="420" y="273" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">시각적 오류</text>
</svg>
</div>

<br>

이 뒤→앞 정렬 순서는 앞서 Early-Z 절에서 다룬 불투명 오브젝트의 앞→뒤 정렬과 정반대입니다.

Unity는 불투명 오브젝트(Opaque 큐, 2000번대)를 앞→뒤로, 반투명 오브젝트(Transparent 큐, 3000번대)를 뒤→앞으로 그리며, 이 정렬 방향의 차이 때문에 두 단계가 분리되어 있습니다.

<br>

반투명 오브젝트의 뒤→앞 정렬은 완벽하지 않습니다.

정렬은 픽셀 단위가 아니라 오브젝트의 중심점(pivot) 기준이므로, 두 반투명 오브젝트가 서로 관통하면 하나의 중심점만으로는 정확한 순서를 결정할 수 없습니다.

이때 시각적 아티팩트가 발생하며, 래스터화 기반 렌더링의 근본적인 한계입니다.

---

## 렌더 타겟과 MRT

지금까지 다룬 버퍼와 블렌딩은 모두 렌더링 결과를 화면용 프레임 버퍼에 기록하는 것을 전제로 했습니다.

하지만 출력 대상이 항상 화면일 필요는 없습니다. 예를 들어 거울에 비친 장면을 표현하려면, 거울 시점의 렌더링 결과를 화면이 아닌 텍스처에 먼저 기록해야 합니다.

이처럼 렌더링 결과가 기록되는 대상을 **렌더 타겟(Render Target)**이라 하며, 화면용 프레임 버퍼도, 텍스처도 모두 렌더 타겟입니다.

### 렌더 텍스처

렌더 타겟으로 지정된 텍스처를 **렌더 텍스처(Render Texture)**라고 합니다.

앞의 거울 예시에서 거울 시점으로 렌더링한 결과가 기록된 텍스처가 곧 렌더 텍스처이며, 이 텍스처를 거울 표면의 머티리얼에 입히면 반사 효과가 완성됩니다.

이처럼 렌더 텍스처는 이후 다른 렌더링 패스에서 입력 텍스처로 사용됩니다.

<br>

Unity에서는 `RenderTexture` 클래스가 렌더 텍스처에 대응합니다.

카메라의 Target Texture에 RenderTexture를 할당하면, 해당 카메라의 렌더링 결과가 화면 대신 렌더 텍스처에 기록됩니다.

### MRT (Multiple Render Targets)

일반적인 렌더링에서는 프래그먼트 셰이더가 하나의 색상 값을 출력하여 하나의 렌더 타겟에 기록합니다.

**MRT(Multiple Render Targets)**를 사용하면 프래그먼트 셰이더가 **여러 색상 값을 동시에 출력**하여, 각각을 서로 다른 렌더 타겟에 한 번의 패스로 기록할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="250" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">MRT의 동작</text>

  <!-- ===== 일반 렌더링 (상단) ===== -->
  <text fill="currentColor" x="250" y="46" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">일반 렌더링 (렌더 타겟 1개)</text>

  <!-- 셰이더 박스 -->
  <rect x="30" y="56" width="130" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="95" y="78" text-anchor="middle" font-size="10" font-family="sans-serif">프래그먼트 셰이더</text>

  <!-- 화살표 -->
  <line x1="160" y1="73" x2="218" y2="73" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="216,69 224,73 216,77" fill="currentColor"/>
  <text fill="currentColor" x="192" y="66" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">색상 1개</text>

  <!-- 렌더 타겟 0 -->
  <rect x="228" y="56" width="150" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="303" y="78" text-anchor="middle" font-size="10" font-family="sans-serif">렌더 타겟 0에 기록</text>

  <!-- 구분선 -->
  <line x1="30" y1="108" x2="470" y2="108" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- ===== MRT (하단) ===== -->
  <text fill="currentColor" x="250" y="132" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">MRT (렌더 타겟 여러 개)</text>

  <!-- 셰이더 박스 (MRT) -->
  <rect x="30" y="150" width="130" height="160" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="95" y="234" text-anchor="middle" font-size="10" font-family="sans-serif">프래그먼트</text>
  <text fill="currentColor" x="95" y="248" text-anchor="middle" font-size="10" font-family="sans-serif">셰이더</text>

  <!-- 출력 0: 색상 → Albedo -->
  <line x1="160" y1="180" x2="268" y2="180" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="266,176 274,180 266,184" fill="currentColor"/>
  <text fill="currentColor" x="214" y="173" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 0: 색상</text>
  <rect x="278" y="166" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="368" y="184" text-anchor="middle" font-size="10" font-family="sans-serif">렌더 타겟 0 (Albedo)</text>

  <!-- 출력 1: 법선 → Normal -->
  <line x1="160" y1="220" x2="268" y2="220" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="266,216 274,220 266,224" fill="currentColor"/>
  <text fill="currentColor" x="214" y="213" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 1: 법선</text>
  <rect x="278" y="206" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="368" y="224" text-anchor="middle" font-size="10" font-family="sans-serif">렌더 타겟 1 (Normal)</text>

  <!-- 출력 2: 스페큘러 → Specular -->
  <line x1="160" y1="260" x2="268" y2="260" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="266,256 274,260 266,264" fill="currentColor"/>
  <text fill="currentColor" x="214" y="253" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 2: 스페큘러</text>
  <rect x="278" y="246" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="368" y="264" text-anchor="middle" font-size="10" font-family="sans-serif">렌더 타겟 2 (Specular)</text>

  <!-- 출력 3: 깊이 → Depth -->
  <line x1="160" y1="300" x2="268" y2="300" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="266,296 274,300 266,304" fill="currentColor"/>
  <text fill="currentColor" x="214" y="293" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 3: 깊이</text>
  <rect x="278" y="286" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="368" y="304" text-anchor="middle" font-size="10" font-family="sans-serif">렌더 타겟 3 (Depth)</text>
</svg>
</div>

### Deferred Rendering의 G-Buffer

MRT가 가장 활발히 쓰이는 곳이 **Deferred Rendering(디퍼드 렌더링)**입니다.

Forward Rendering에서는 각 오브젝트를 렌더링할 때 조명 계산까지 함께 수행합니다.

광원이 N개이고 오브젝트가 M개이면 조명 계산이 최대 N × M번 반복되므로, 광원 수가 늘어날수록 비용이 급증합니다.

<br>

Deferred Rendering은 이 문제를 피하기 위해 렌더링을 두 단계로 나눕니다.

첫 번째 단계(Geometry Pass)에서는 조명 계산 없이, 모든 오브젝트의 기하 정보(색상, 법선, 스페큘러(표면의 정반사 특성) 등)만 MRT를 통해 여러 렌더 텍스처에 기록합니다.

이 텍스처 집합이 **G-Buffer**입니다.

<br>

두 번째 단계(Lighting Pass)에서는 G-Buffer의 데이터를 읽어 조명 계산을 수행합니다.

조명 비용이 오브젝트 수(M)와 무관하게 화면의 픽셀 수와 광원 수(N)에만 비례하므로, 광원이 많은 장면에서 Forward Rendering보다 효율적입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="260" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">Deferred Rendering의 G-Buffer</text>

  <!-- ===== Geometry Pass ===== -->
  <rect x="20" y="34" width="480" height="170" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="52" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">Geometry Pass (MRT 사용)</text>

  <!-- 셰이더 박스 -->
  <rect x="40" y="64" width="120" height="120" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="100" y="126" text-anchor="middle" font-size="10" font-family="sans-serif">프래그먼트</text>
  <text fill="currentColor" x="100" y="140" text-anchor="middle" font-size="10" font-family="sans-serif">셰이더</text>

  <!-- 출력 0: Albedo -->
  <line x1="160" y1="86" x2="238" y2="86" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,82 244,86 236,90" fill="currentColor"/>
  <text fill="currentColor" x="200" y="80" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 0</text>
  <rect x="248" y="72" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="308" y="90" text-anchor="middle" font-size="10" font-family="sans-serif">Albedo</text>
  <text fill="currentColor" x="388" y="90" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">(색상)</text>

  <!-- 출력 1: Normal -->
  <line x1="160" y1="116" x2="238" y2="116" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,112 244,116 236,120" fill="currentColor"/>
  <text fill="currentColor" x="200" y="110" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 1</text>
  <rect x="248" y="102" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="308" y="120" text-anchor="middle" font-size="10" font-family="sans-serif">Normal</text>
  <text fill="currentColor" x="388" y="120" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">(법선)</text>

  <!-- 출력 2: Specular -->
  <line x1="160" y1="146" x2="238" y2="146" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,142 244,146 236,150" fill="currentColor"/>
  <text fill="currentColor" x="200" y="140" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">출력 2</text>
  <rect x="248" y="132" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="308" y="150" text-anchor="middle" font-size="10" font-family="sans-serif">Specular</text>
  <text fill="currentColor" x="388" y="150" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">(반사)</text>

  <!-- 깊이: Depth -->
  <line x1="160" y1="176" x2="238" y2="176" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="236,172 244,176 236,180" fill="currentColor"/>
  <text fill="currentColor" x="200" y="170" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">깊이</text>
  <rect x="248" y="162" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="308" y="180" text-anchor="middle" font-size="10" font-family="sans-serif">Depth</text>
  <text fill="currentColor" x="388" y="180" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">(깊이)</text>

  <!-- ===== G-Buffer 라벨 ===== -->
  <line x1="260" y1="204" x2="260" y2="230" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="255,228 260,236 265,228" fill="currentColor"/>

  <!-- G-Buffer: 4개 텍스처 가로 나열 -->
  <rect x="20" y="240" width="480" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="256" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">G-Buffer</text>

  <rect x="35" y="266" width="104" height="32" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="87" y="286" text-anchor="middle" font-size="9" font-family="sans-serif">Albedo 텍스처</text>

  <rect x="149" y="266" width="104" height="32" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="201" y="286" text-anchor="middle" font-size="9" font-family="sans-serif">Normal 텍스처</text>

  <rect x="263" y="266" width="104" height="32" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="315" y="286" text-anchor="middle" font-size="9" font-family="sans-serif">Specular 텍스처</text>

  <rect x="377" y="266" width="104" height="32" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="429" y="286" text-anchor="middle" font-size="9" font-family="sans-serif">Depth 텍스처</text>

  <!-- 화살표: G-Buffer → Lighting Pass -->
  <line x1="260" y1="310" x2="260" y2="340" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="255,338 260,346 265,338" fill="currentColor"/>

  <!-- ===== Lighting Pass ===== -->
  <rect x="20" y="350" width="480" height="110" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="260" y="370" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">Lighting Pass</text>

  <!-- 조명 계산 박스 -->
  <rect x="50" y="382" width="240" height="60" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="170" y="402" text-anchor="middle" font-size="10" font-family="sans-serif">각 광원에 대해:</text>
  <text fill="currentColor" x="170" y="416" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">G-Buffer에서 색상, 법선, 스페큘러,</text>
  <text fill="currentColor" x="170" y="430" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">깊이를 읽어 조명 계산</text>

  <!-- 화살표: 조명 → 프레임 버퍼 -->
  <line x1="290" y1="412" x2="338" y2="412" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="336,408 344,412 336,416" fill="currentColor"/>

  <!-- 렌더 타겟 -->
  <rect x="348" y="386" width="140" height="52" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="418" y="406" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">렌더 타겟</text>
  <text fill="currentColor" x="418" y="422" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">프레임 버퍼 또는</text>
  <text fill="currentColor" x="418" y="433" text-anchor="middle" font-size="8" font-family="sans-serif" opacity="0.5">렌더 텍스처</text>

  <!-- 하단 보조 텍스트 -->
  <text fill="currentColor" x="260" y="490" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">조명 비용: 오브젝트 수(M)와 무관, 픽셀 수 x 광원 수(N)에 비례</text>
</svg>
</div>

<br>

G-Buffer는 여러 렌더 텍스처로 구성되므로 메모리 사용량이 큽니다.

Full HD 기준으로 G-Buffer 하나의 텍스처가 약 8MB이고, 3~4개를 사용하면 24~32MB에 달합니다.

매 프레임마다 이 데이터를 읽고 써야 하므로 대역폭 부담도 그만큼 늘어납니다.

<br>

Deferred Rendering에는 메모리·대역폭 외에도 구조적 한계가 있습니다.

G-Buffer의 각 픽셀에는 가장 가까운 표면 하나의 속성만 저장됩니다.

예를 들어 빨간 벽 앞에 반투명 유리가 있으면, 유리의 색상·법선을 G-Buffer에 기록하는 순간 벽의 정보가 덮어쓰여 사라집니다.

반투명 렌더링은 두 표면의 색상을 블렌딩해야 하므로 양쪽 정보가 모두 필요하지만, G-Buffer 구조에서는 한쪽만 남습니다.

따라서 반투명 오브젝트는 G-Buffer를 거치지 않고 별도의 Forward 패스로 렌더링됩니다.

<br>

또한 G-Buffer는 픽셀 단위로 데이터를 저장하므로, 서브 샘플 단위의 데이터가 필요한 MSAA와 직접 호환되지 않습니다.

그래서 Deferred Rendering에서 안티앨리어싱이 필요하면, FXAA나 TAA 같은 후처리 기반 기법을 사용합니다.

<br>

메모리와 대역폭이 제한적인 모바일에서는 이 부담이 크기 때문에, Unity URP의 모바일 설정에서는 Forward Rendering이 기본으로 사용됩니다.

다만 [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 TBDR 아키텍처에서는 타일 단위로 G-Buffer를 온칩 메모리에서 처리할 수 있어, 모바일에서도 대역폭 부담이 줄어듭니다.

반면 HDRP(High Definition Render Pipeline)는 데스크톱·콘솔을 대상으로 하며, HDRP Asset의 Lit Shader Mode 설정을 통해 Forward와 Deferred를 모두 지원합니다.

---

## 출력 병합의 전체 흐름

앞에서 다룬 깊이 테스트, 스텐실 테스트, 블렌딩, 렌더 타겟이 출력 병합 단계에서 어떻게 연결되는지 아래 다이어그램으로 정리했습니다.

Early-Z가 활성화된 드로우 콜에서는 프래그먼트 셰이더 이전에 깊이 테스트가 수행되고, 비활성화된 경우에는 Late-Z 경로만 사용되며, 두 경로가 동시에 실행되지는 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 680" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">출력 병합의 전체 흐름</text>

  <!-- 1: 래스터화 -->
  <rect x="130" y="36" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="58" text-anchor="middle" font-size="11" font-family="sans-serif">래스터화</text>

  <!-- 화살표 1→2 -->
  <line x1="220" y1="70" x2="220" y2="90" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,88 220,96 225,88" fill="currentColor"/>

  <!-- 2: 프래그먼트 -->
  <rect x="130" y="98" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="120" text-anchor="middle" font-size="11" font-family="sans-serif">프래그먼트 (UV, 법선, 깊이 등)</text>

  <!-- 화살표 2→Early-Z (분기, 점선) -->
  <line x1="220" y1="132" x2="220" y2="152" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,150 220,158 225,150" fill="currentColor"/>

  <!-- 3: Early-Z 테스트 (점선 — 선택적) -->
  <rect x="130" y="160" width="180" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text fill="currentColor" x="220" y="180" text-anchor="middle" font-size="11" font-family="sans-serif">Early-Z 테스트</text>
  <text fill="currentColor" x="220" y="196" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">활성화 시, 통과한 프래그먼트만 계속</text>

  <!-- 버퍼 참조: 깊이 버퍼 (읽기) → Early-Z -->
  <rect x="400" y="164" width="150" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text fill="currentColor" x="475" y="182" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">깊이 버퍼 (읽기)</text>
  <line x1="400" y1="180" x2="314" y2="180" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <polygon points="316,176 308,180 316,184" fill="currentColor" opacity="0.6"/>

  <!-- 화살표 3→4 -->
  <line x1="220" y1="206" x2="220" y2="228" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,226 220,234 225,226" fill="currentColor"/>

  <!-- 4: 프래그먼트 셰이더 -->
  <rect x="130" y="236" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="258" text-anchor="middle" font-size="11" font-family="sans-serif">프래그먼트 셰이더</text>

  <!-- 화살표 4→5 -->
  <line x1="220" y1="270" x2="220" y2="292" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,290 220,298 225,290" fill="currentColor"/>

  <!-- 5: 스텐실 테스트 -->
  <rect x="130" y="300" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="322" text-anchor="middle" font-size="11" font-family="sans-serif">스텐실 테스트</text>

  <!-- 버퍼 참조: 스텐실 버퍼 (읽기/쓰기) -->
  <rect x="400" y="304" width="150" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="475" y="322" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">스텐실 버퍼 (읽기/쓰기)</text>
  <line x1="400" y1="318" x2="314" y2="318" stroke="currentColor" stroke-width="1"/>
  <polygon points="316,314 308,318 316,322" fill="currentColor" opacity="0.6"/>

  <!-- 화살표 5→6 -->
  <line x1="220" y1="334" x2="220" y2="356" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,354 220,362 225,354" fill="currentColor"/>

  <!-- 6: 깊이 테스트 (Late-Z) -->
  <rect x="130" y="364" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="386" text-anchor="middle" font-size="11" font-family="sans-serif">깊이 테스트 (Late-Z)</text>

  <!-- 버퍼 참조: 깊이 버퍼 (읽기/쓰기) -->
  <rect x="400" y="368" width="150" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="475" y="386" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">깊이 버퍼 (읽기/쓰기)</text>
  <line x1="400" y1="382" x2="314" y2="382" stroke="currentColor" stroke-width="1"/>
  <polygon points="316,378 308,382 316,386" fill="currentColor" opacity="0.6"/>

  <!-- 화살표 6→7 -->
  <line x1="220" y1="398" x2="220" y2="420" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,418 220,426 225,418" fill="currentColor"/>

  <!-- 7: 블렌딩 -->
  <rect x="130" y="428" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="450" text-anchor="middle" font-size="11" font-family="sans-serif">블렌딩</text>

  <!-- 버퍼 참조: 렌더 타겟 (Dst 읽기) -->
  <rect x="400" y="432" width="150" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="475" y="450" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">렌더 타겟 (Dst 읽기)</text>
  <line x1="400" y1="446" x2="314" y2="446" stroke="currentColor" stroke-width="1"/>
  <polygon points="316,442 308,446 316,450" fill="currentColor" opacity="0.6"/>

  <!-- 화살표 7→렌더 타겟 -->
  <line x1="220" y1="462" x2="220" y2="492" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,490 220,498 225,490" fill="currentColor"/>

  <!-- ===== 렌더 타겟 (쓰기) ===== -->
  <rect x="130" y="498" width="180" height="34" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="220" y="520" text-anchor="middle" font-size="11" font-family="sans-serif">렌더 타겟 (쓰기)</text>

  <!-- 주석: 렌더 타겟 설정에 따라 -->
  <text fill="currentColor" x="220" y="548" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">렌더 타겟 설정에 따라</text>

  <!-- 분기: 좌측 ㄱ자 (박스 하단 → 좌로 꺾음) -->
  <line x1="220" y1="532" x2="220" y2="560" stroke="currentColor" stroke-width="1.2"/>
  <line x1="220" y1="560" x2="130" y2="560" stroke="currentColor" stroke-width="1.2"/>
  <line x1="130" y1="560" x2="130" y2="578" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="125,576 130,584 135,576" fill="currentColor"/>

  <!-- 분기: 우측 ㄱ자 (같은 수평선에서 우로 꺾음) -->
  <line x1="220" y1="560" x2="390" y2="560" stroke="currentColor" stroke-width="1.2"/>
  <line x1="390" y1="560" x2="390" y2="578" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="385,576 390,584 395,576" fill="currentColor"/>

  <!-- 프레임 버퍼 → 디스플레이 -->
  <rect x="50" y="584" width="160" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="130" y="604" text-anchor="middle" font-size="10" font-family="sans-serif">프레임 버퍼 → 디스플레이</text>

  <!-- 렌더 텍스처 → 이후 패스 -->
  <rect x="310" y="584" width="160" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="390" y="604" text-anchor="middle" font-size="10" font-family="sans-serif">렌더 텍스처 → 이후 패스</text>
</svg>
</div>

<br>

각 버퍼의 역할과 크기는 다음과 같습니다.

| 버퍼 | 크기/형식 | 역할 |
|------|-----------|------|
| 프레임 버퍼 (색상 버퍼) | RGBA8/16F, 4~8 B/pixel | 최종 색상 저장 |
| 깊이+스텐실 버퍼 | D24S8 (4 B/pixel) 또는 D32F_S8 (8 B/pixel) | 가시성 판별 (깊이 테스트) + 조건부 렌더링 (마스킹) |
| 렌더 텍스처 | 다양 | 오프스크린 렌더링, MRT, G-Buffer, 포스트 프로세싱 |

해상도 1920x1080, D24S8 + RGBA8 기준: 색상 버퍼 \~8 MB, 깊이+스텐실 \~8 MB, 합계 \~16 MB (프레임당)

---

## 마무리

- **프레임 버퍼**는 최종 색상이 기록되는 메모리 영역이며, RGBA 채널로 구성됩니다.
- **깊이 버퍼(Z-Buffer)**는 각 픽셀의 가장 가까운 프래그먼트 깊이를 저장하여 가시성을 판별합니다.
- **Early-Z**는 프래그먼트 셰이더 이전에 깊이 테스트를 수행하여 가려진 프래그먼트의 셰이딩 비용을 절약하지만, alpha test나 깊이 수정 시에는 비활성화됩니다.
- **스텐실 버퍼**는 8비트 정수 값으로 조건부 렌더링(거울, 포털, 아웃라인 등)을 구현합니다.
- **블렌딩**은 반투명 오브젝트의 색상을 렌더 타겟의 기존 값(Dst)과 혼합하며, 올바른 결과를 위해 뒤에서 앞(back-to-front) 순서로 렌더링해야 합니다.
- **렌더 타겟**은 렌더링 결과가 기록되는 대상이며, 프레임 버퍼뿐 아니라 렌더 텍스처도 렌더 타겟이 됩니다. **MRT**는 한 번의 패스로 여러 렌더 타겟에 동시에 기록하여 Deferred Rendering의 G-Buffer 구성에 사용됩니다.

이 버퍼들은 모두 GPU 메모리에 위치하며, [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 TBDR의 타일 메모리에서는 깊이 테스트, 블렌딩, MSAA가 온칩에서 수행되어 대역폭을 절약합니다.

프레임 버퍼에 기록된 이미지는 아직 화면에 표시된 것이 아닙니다. 프레임 버퍼의 데이터가 디스플레이에 전달되는 과정에서 GPU와 디스플레이의 타이밍이 어긋나면 화면이 찢어지는 현상이 발생합니다.

[다음 글](/dev/unity/RasterPipeline-3/)에서는 스캔아웃, 티어링, VSync, 더블/트리플 버퍼링과 함께, 래스터화의 근본적 한계인 앨리어싱과 안티앨리어싱 기법들을 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- **래스터화 파이프라인 (2) - 출력 병합** (현재 글)
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
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- **래스터화 파이프라인 (2) - 출력 병합** (현재 글)
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
