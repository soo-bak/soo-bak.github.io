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

[래스터화 파이프라인 (1)](/dev/unity/RasterPipeline-1/)에서는 삼각형 하나가 화면 격자 위의 프래그먼트로 변환되는 과정을 살펴봤습니다. 픽셀 중심이 삼각형 안에 드는지는 Edge Function으로 판별하고, 통과한 자리에서는 무게중심 좌표로 정점 속성을 보간해 프래그먼트 셰이더의 입력을 만듭니다.

프래그먼트 셰이더는 이 입력을 받아 프래그먼트마다 색을 계산합니다. 다만 이 프래그먼트 셰이더가 정한 색이 그대로 화면의 픽셀이 되지는 않습니다.

한 픽셀의 최종 색은 그 자리에 도착한 프래그먼트 하나만으로 정해지지 않기 때문입니다. 같은 픽셀에 여러 오브젝트가 겹치면 가장 앞에 있는 표면만 남겨야 하고, 어떤 영역은 색을 아예 기록하지 못하도록 막아야 하며, 반투명 표면이라면 새 색을 이미 칠해진 색과 섞어야 합니다. 하나의 프래그먼트가 최종 픽셀로 기록되기까지는 이런 검사와 합성 단계가 남아 있습니다.

이 마지막 검사와 합성을 묶어 **출력 병합(Output Merger)** 단계라고 부릅니다. 이번 글에서는 프래그먼트 셰이더가 계산한 색이 실제 화면이나 렌더 텍스처에 기록되기까지, 색을 담는 프레임 버퍼에서 깊이 버퍼와 스텐실 버퍼, 블렌딩을 지나 출력 대상을 지정하는 렌더 타겟과 MRT에 이르는 단계를 차례로 살펴봅니다.

---

## 프레임 버퍼

프래그먼트 셰이더가 색을 계산해도, 그 값을 저장할 메모리가 없으면 한 프레임의 이미지를 만들 수 없습니다. **프레임 버퍼(Frame Buffer)**는 한 프레임의 색을 픽셀 단위로 기록하는 메모리 영역으로, GPU가 직접 읽고 쓰는 GPU 메모리에 자리합니다. 외장 그래픽 카드라면 전용 메모리인 VRAM이 여기에 해당하고, CPU와 메모리를 공유하는 모바일에서는 그 공유 메모리의 일부가 쓰입니다.

드로우 콜이 실행되는 동안 프래그먼트 셰이더가 계산한 색이 이 버퍼의 픽셀 자리에 기록됩니다. 한 프레임이 완성되면 버퍼에 담긴 색이 디스플레이로 전달되어 화면에 표시됩니다.

프레임 버퍼의 픽셀 하나는 R·G·B·A 네 채널로 이루어집니다. R(Red)·G(Green)·B(Blue)는 색을, A(Alpha)는 불투명도를 나타냅니다.

널리 쓰이는 RGBA8 형식은 채널마다 8비트, 즉 0~255 범위를 쓰므로 픽셀 하나가 4바이트를 차지합니다.

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

밝기 범위가 넓은 HDR(High Dynamic Range) 렌더링에서는 채널당 8비트 정수만으로 밝기를 충분히 표현하기 어렵습니다. 이런 장면에서는 채널마다 16비트 부동소수점을 쓰는 RGBA16F나, 알파 채널을 빼고 픽셀당 4바이트에 맞춘 R11G11B10F 같은 형식을 선택합니다.

형식을 바꾸면 픽셀 하나의 크기가 달라지고, 프레임 버퍼 전체의 메모리 사용량도 그만큼 달라집니다. 영향은 저장 용량에 그치지 않습니다. GPU는 렌더링 중에 프레임 버퍼에 색을 쓰고 블렌딩할 때는 기존 색을 다시 읽으므로, 버퍼가 커질수록 매 프레임 오가는 메모리 대역폭도 함께 늘어납니다.

지금까지 다룬 프레임 버퍼는 색을 저장하는 **색상 버퍼(Color Buffer)**입니다. 하지만 실제 렌더링은 색상 버퍼 하나로 끝나지 않습니다. 앞뒤 관계를 판별하는 깊이 버퍼, 영역을 걸러내는 스텐실 버퍼처럼 색이 아닌 정보를 담는 보조 버퍼도 함께 쓰입니다.

색상 버퍼와 보조 버퍼는 그래픽스 API에서 하나의 출력 대상으로 묶입니다. 예를 들어 OpenGL의 프레임 버퍼 오브젝트(FBO)는 색상 버퍼와 깊이 버퍼, 스텐실 버퍼를 하나로 연결한 출력 대상 집합입니다.

---

## 깊이 버퍼 (Z-Buffer)

3D 장면에서는 여러 오브젝트가 화면의 같은 픽셀에 겹쳐 투영될 수 있습니다. 현실에서 가까운 물체가 먼 물체를 가리듯, 렌더링에서도 카메라에 가까운 표면이 먼 표면을 덮어야 장면이 자연스럽게 보입니다.

그래서 각 픽셀마다 어느 프래그먼트가 더 가까운지 가려내야 합니다. 이 앞뒤 판별, 곧 **가시성 판별(Visibility Determination)**을 맡는 보조 버퍼가 **깊이 버퍼(Depth Buffer)**이며, **Z-Buffer**라고도 부릅니다.

깊이 버퍼는 색상 버퍼와 해상도가 같고, 각 픽셀마다 현재까지 통과한 프래그먼트의 깊이 값을 저장합니다. 새 프래그먼트가 들어오면 GPU는 그 깊이를 버퍼에 저장된 값과 비교해 더 가까운 프래그먼트만 통과시킵니다. 이 비교 단계를 **깊이 테스트(Depth Test)**라고 합니다.

깊이 값의 바탕이 되는 것은 NDC(Normalized Device Coordinates) 공간의 z 값입니다. NDC z의 범위는 그래픽스 API마다 달라서, DirectX·Metal·Vulkan은 [0, 1], OpenGL은 [-1, 1]을 씁니다. 이 절에서는 [0, 1]을 기준으로 삼으며, 0.0이 카메라에 가장 가깝고 1.0이 가장 먼 값에 해당합니다.

> NDC와 z 값이 만들어지는 과정은 [그래픽스 수학 (3)](/dev/unity/GraphicsMath-3/)에서 자세히 다룹니다.

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

깊이 테스트 덕분에 **불투명 오브젝트**는 그리는 순서와 상관없이 3D 공간에서 앞에 있는 표면이 뒤에 있는 표면을 가립니다. 삼각형 A를 먼저 그리든 삼각형 C를 먼저 그리든, 같은 픽셀에는 결국 가장 가까운 삼각형의 색만 남습니다.

반투명 오브젝트는 기존 색과 새 색을 섞어야 하므로 같은 방식으로 처리되지 않습니다. 이 문제는 뒤의 블렌딩 절에서 다시 다룹니다.

깊이 버퍼에서 흔히 쓰이는 형식은 **D24S8**입니다. 깊이 24비트와 스텐실 8비트를 합쳐 32비트, 즉 픽셀당 4바이트를 사용합니다. 여기서 스텐실 8비트가 어떤 역할을 하는지는 스텐실 버퍼 절에서 따로 살펴봅니다.

D24S8은 깊이 테스트와 스텐실 테스트를 함께 처리할 수 있어 많은 3D 렌더링 환경에서 기본 형식으로 사용됩니다. Unity에서도 플랫폼과 렌더 파이프라인 설정에 따라 이 계열의 깊이/스텐실 형식이 자주 쓰입니다.

깊이만 저장할 때는 **D32F**(32비트 부동소수점)를 선택하기도 합니다. 스텐실이 필요 없고 깊이 정밀도가 중요한 상황에 적합한 형식입니다.

예를 들어 비행 시뮬레이터처럼 콕핏의 가까운 표면과 수십\~수백 km 떨어진 지형을 한 화면에 함께 그리는 경우, 24비트 정수 깊이만으로는 원거리에서 z-fighting이 나타날 수 있습니다. 이런 장면에서는 D32F와 Reversed-Z를 함께 사용해 먼 거리의 깊이 정밀도를 개선할 수 있습니다. 섀도우 맵에서도 깊이 정밀도가 부족하면 shadow acne가 생길 수 있으므로 D32F를 사용하는 경우가 있습니다.

높은 깊이 정밀도와 스텐실이 동시에 필요할 때는 **D32F_S8**(32비트 부동소수점 깊이 + 8비트 스텐실, 픽셀당 8바이트)을 사용할 수도 있습니다. 다만 픽셀당 비용이 커지므로 필요한 경우에만 선택하는 편입니다.

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

깊이 버퍼에 기록되는 값은 3D 공간의 실제 거리와 선형으로 대응하지 않습니다. 선형이라면 near = 1m, far = 1000m인 장면에서 500m 지점이 깊이 값 약 0.5에 해당해야 하지만, 원근 투영에서는 그렇게 나뉘지 않습니다.

원인은 원근 투영 과정에 있습니다. 버텍스 셰이더가 클립 좌표 (x, y, z, w)를 출력하면 GPU는 모든 성분을 w로 나누어 NDC 좌표를 만듭니다. 이 단계를 **원근 나눗셈(perspective divide)**이라고 부릅니다.

원근 투영 행렬에서는 w 성분이 뷰 공간의 깊이와 연결됩니다. 따라서 NDC z는 단순한 거리 값이 아니라 z를 포함한 나눗셈 결과가 되고, 깊이 값은 대략 **1/z에 가까운 비선형 분포**를 보입니다.

이 비선형 변환을 거치면, near = 1, far = 1000인 장면에서 거리에 따른 깊이 값이 다음처럼 분포합니다.

<br>

| 거리(z) | NDC 깊이 값 |
|---------|------------|
| 1 (near) | 0.000 |
| 2 | ≈ 0.501 |
| 10 | ≈ 0.901 |
| 100 | ≈ 0.991 |
| 500 | ≈ 0.999 |
| 1000 (far) | 1.000 |

<br>

표를 보면 깊이 값이 near 쪽에 크게 몰려 있음을 알 수 있습니다. 버퍼 범위의 **절반(약 0.0\~0.5)**이 거리 1\~2 구간, 즉 1m에 사용되고, **나머지 절반(약 0.5\~1.0)**이 2\~1000 구간, 즉 998m를 담당합니다.

그 결과 near plane 가까이에서는 깊이 값이 크게 변해 구분할 수 있는 단계가 많고, far plane 가까이에서는 깊이 값 변화가 작아 구분 단계가 부족해집니다.

먼 거리에서 정밀도가 부족하면, 실제로는 서로 떨어져 있는 두 표면이 깊이 버퍼에서는 거의 같은 값으로 기록될 수 있습니다. 그러면 GPU가 어느 표면을 앞쪽으로 볼지 안정적으로 판단하지 못하면서 두 표면이 번갈아 보이는 **Z-fighting** 현상이 나타납니다.

앞서 언급한 D32F + Reversed-Z 조합은 이 원거리 정밀도 문제를 줄이기 위한 방법입니다. 이 조합이 효과를 내는 이유를 보려면 먼저 부동소수점 값의 간격을 이해해야 합니다.

IEEE 754 부동소수점은 지수(exponent) 구조 때문에 0에 가까울수록 표현 가능한 값의 간격이 작습니다. 반대로 1에 가까워질수록 값 사이의 간격은 상대적으로 넓어집니다.

깊이 버퍼가 부동소수점(D32F)이고 전통적 매핑(near=0, far=1)을 사용하면, 원근 투영의 비선형 분포와 float 정밀도 분포가 **같은 방향**으로 겹칩니다.

<br>

| | near(가까운 곳) | far(먼 곳) |
|---|---|---|
| 1/z 분포 | 깊이 값이 촘촘 (정밀도 높음) | 깊이 값이 성김 (정밀도 낮음) |
| float 정밀도 | 0 근처 → 촘촘 (정밀도 높음) | 1 근처 → 성김 (정밀도 낮음) |
| **합산** | **이미 충분한데 더 정밀** | **이미 부족한데 더 부족** |

<br>

전통적 매핑에서는 가까운 곳에 정밀도가 과하게 몰리고, 먼 곳은 원근 투영의 분포와 float의 값 간격이 함께 작용해 정밀도가 더 부족해집니다.

원근 투영이 만드는 비선형성 자체는 그대로 두더라도, 깊이 값을 어느 방향으로 저장할지는 바꿀 수 있습니다. Reversed-Z는 near=1, far=0으로 깊이 방향을 뒤집어, 0 근처에서 촘촘해지는 float의 값 간격을 far 쪽에 배치합니다.

<br>

| | near(가까운 곳) | far(먼 곳) |
|---|---|---|
| 1/z 분포 | 깊이 값이 촘촘 (변함없음) | 깊이 값이 성김 (변함없음) |
| float 정밀도 | **1 근처 → 성김** | **0 근처 → 촘촘** |
| **합산** | **1/z의 높은 정밀도를 float이 적당히 깎음** | **1/z의 낮은 정밀도를 float이 보충** |

<br>

이렇게 두 분포가 서로 보완되면서 전체 깊이 범위의 정밀도가 더 고르게 배분됩니다. 다만 이 효과는 값 간격이 불균일한 float 깊이 버퍼(D32F)에서 특히 의미가 있습니다. 값 간격이 균일한 정수 깊이 버퍼(D24S8)에서는 Reversed-Z만으로 같은 효과를 기대하기 어렵습니다.

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

Z-fighting을 줄이는 직접적인 방법은 near plane과 far plane의 비율을 좁히는 것입니다. 이 비율이 커질수록(예: near=0.01, far=1000 → 1:100,000) 정밀도가 near 쪽으로 더 심하게 몰리고, 먼 거리의 깊이 단계는 더 부족해집니다.

반대로 near=0.3, far=1000으로 두면 비율이 1:3,333까지 줄어들어 일반적인 장면에서는 더 안정적인 깊이 정밀도를 얻을 수 있습니다. Unity 카메라의 Near Clipping Plane 기본값이 0.3인 것도 이와 관련이 있습니다.

near/far 조정만으로 충분하지 않을 때는 **Reversed-Z**가 원거리 정밀도를 보완합니다.

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

버퍼 형식에 따라 값 간격이 다르므로, Reversed-Z의 효과도 형식에 따라 달라집니다.

<br>

| | 전통적 매핑 | Reversed-Z |
|---|---|---|
| **D32F** (불균일) | 1/z 편향 + float 편향 = 이중 편향 | 1/z 편향 ↔ float 편향 = **상쇄** |
| **D24S8** (균일) | 1/z 편향만 존재 | 1/z 편향만 존재 — **변화 없음** |

<br>

일반적인 Unity 렌더링에서는 이 차이를 직접 맞출 필요가 없습니다. Unity와 렌더 파이프라인이 플랫폼에 맞는 GPU 투영 행렬, 깊이 버퍼 초기값, 깊이 테스트 비교 방향을 내부에서 설정하기 때문입니다. DirectX, Metal, Vulkan 계열에서는 Reversed-Z가 사용되고, OpenGL/OpenGL ES 계열에서는 전통적인 깊이 방향이 사용됩니다.

Reversed-Z가 적용된 플랫폼에서는 깊이 값 1.0이 near 쪽, 0.0이 far 쪽을 뜻합니다. 그래서 깊이 버퍼 초기값은 전통적인 1.0 대신 0.0이 되고, 깊이 비교 방향도 Less 계열이 아니라 Greater 계열로 바뀝니다. 카메라와 머티리얼, 렌더 패스가 기본 깊이 흐름을 따른다면 이 변경은 Unity가 처리합니다.

주의해야 할 코드는 깊이 값을 직접 읽거나 직접 비교하는 코드입니다. 예를 들어 `_CameraDepthTexture`의 raw depth를 비교하거나, 커스텀 깊이 패스에서 투영 행렬과 깊이 비교를 직접 구성한다면 플랫폼별 깊이 방향을 고려해야 합니다. 셰이더에서는 `UNITY_REVERSED_Z` 매크로로 분기하거나, 가능하면 Unity의 깊이 변환 헬퍼를 사용해 raw depth 해석을 직접 고정하지 않는 편이 안전합니다.

> 원근 투영에서 깊이 값이 비선형이 되는 이유와 Reversed-Z의 수학적 배경은 [그래픽스 수학 (4)](/dev/unity/GraphicsMath-4/)에서 더 자세히 다룹니다.

---

## Early-Z vs Late-Z

같은 깊이 테스트라도 프래그먼트 셰이더 앞에서 실행하느냐, 뒤에서 실행하느냐에 따라 비용이 달라집니다. 어차피 가려질 프래그먼트라면 색을 계산한 뒤 버리는 것보다, 셰이딩 전에 걸러내는 편이 더 효율적입니다.

파이프라인의 논리적 순서대로라면 깊이 테스트는 프래그먼트 셰이더 뒤에서 실행됩니다. 이 방식을 Late-Z라고 부릅니다. 반대로 깊이 비교를 셰이더 앞으로 앞당겨, 가려질 프래그먼트의 셰이딩을 건너뛰는 방식이 **Early-Z**입니다.

### Late-Z (논리적 순서)

Late-Z는 파이프라인의 논리적 순서를 그대로 따라, 프래그먼트 셰이더가 색을 계산한 **뒤에** 깊이 테스트로 폐기 여부를 결정합니다. 어떤 프래그먼트가 가려지는지는 셰이딩이 끝난 뒤에야 알 수 있습니다.

이 순서에서는 다른 오브젝트에 가려져 결국 버려질 프래그먼트도 일단 셰이더를 실행합니다. 같은 픽셀이 여러 번 셰이딩되는 오버드로우(overdraw)가 그대로 비용이 되고, 셰이더가 복잡할수록 낭비도 커집니다.

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

Early-Z는 Late-Z에서 생기는 셰이딩 낭비를 줄이기 위해 깊이 테스트를 프래그먼트 셰이더 **앞으로** 옮깁니다. 색을 계산하기 전에 깊이부터 먼저 비교하는 방식입니다.

해당 픽셀 위치에 이미 더 가까운 깊이 값이 기록되어 있으면, 새 프래그먼트는 화면에 보일 수 없습니다. 이 경우 GPU는 프래그먼트 셰이더를 실행하지 않고 바로 폐기할 수 있습니다. 조건이 맞으면 GPU가 자동으로 적용하므로, 일반적으로 개발자가 별도로 켜는 옵션은 아닙니다.

> Early-Z가 GPU 하드웨어에서 오버드로우 비용을 줄이는 과정은 [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 더 자세히 다룹니다.

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

Early-Z는 깊이 버퍼에 더 가까운 값이 이미 기록되어 있을 때에만 뒤쪽 프래그먼트를 걸러낼 수 있습니다. 따라서 불투명 오브젝트는 카메라에서 가까운 것부터, 즉 **앞에서 뒤(front-to-back)** 순서로 렌더링하는 것이 유리합니다.

가까운 오브젝트를 먼저 그리면 깊이 버퍼가 가까운 값으로 일찍 채워져, 뒤따라 들어오는 먼 프래그먼트가 셰이딩 전에 걸러집니다. 반대로 먼 오브젝트부터 그리면 그 프래그먼트가 셰이딩된 뒤에 가까운 오브젝트에 덮이므로, 그만큼 셰이딩 비용이 낭비됩니다.

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

이 정렬은 개발자가 직접 처리하지 않아도 됩니다. Unity는 렌더링 순서를 **렌더 큐(Render Queue)**라는 번호 체계로 관리하고, 불투명 오브젝트가 모이는 Opaque 큐 안에서는 카메라에 가까운 것부터 자동으로 그립니다.

### Early-Z가 작동하지 않는 경우

Early-Z가 항상 적용되는 것은 아닙니다. 셰이더를 실행하기 전에 깊이만으로 프래그먼트를 거르려면, 그 프래그먼트의 **생존 여부**와 **최종 깊이**가 셰이더 실행 전에 이미 정해져 있어야 합니다. 셰이더가 둘 중 하나를 바꿀 수 있으면 이 전제가 깨지므로, GPU는 그 드로우 콜에서 Early-Z를 끄거나 제한하고 기본 순서인 Late-Z로 처리합니다.

이 전제는 셰이더가 프래그먼트의 **생존 여부**를 직접 정할 때 먼저 깨집니다. `discard`나 `clip`으로 일부 프래그먼트를 버리는 Alpha Test가 여기 해당하며, 어떤 프래그먼트가 끝까지 남을지는 셰이더를 실행해 봐야 알 수 있습니다.

Early-Z가 깊이 쓰기까지 앞당기면, 셰이더 실행 전에 통과한 프래그먼트의 깊이가 버퍼에 먼저 기록될 수 있습니다. 그런데 그 프래그먼트가 셰이더 안에서 `discard`로 사라지면, 보이지 않는 표면의 깊이만 버퍼에 남아 뒤의 오브젝트를 잘못 가립니다. GPU는 이런 오류를 막으려고 해당 드로우 콜의 Early-Z를 끄거나 제한합니다.

> TBDR 환경에서 alpha test가 비싼 이유도 이 비활성화와 관련됩니다. 자세한 내용은 [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룹니다.

다음은 셰이더가 프래그먼트의 **최종 깊이**를 바꾸는 경우입니다. 프래그먼트 셰이더가 `SV_Depth`로 깊이를 직접 출력하면, 래스터화가 보간한 깊이와 셰이더가 최종적으로 내놓는 깊이가 달라집니다. Early-Z는 셰이더 실행 전의 보간 깊이로 판단하므로, 셰이더가 나중에 깊이를 바꾸면 그 판단이 어긋날 수 있어 이 경우에도 Early-Z를 적용하기 어렵습니다.

마지막 경우는 성격이 조금 다릅니다. 깊이 쓰기를 끄면(`ZWrite Off`) 이 오브젝트를 그리는 동안 깊이 버퍼가 갱신되지 않지만, 그렇다고 Early-Z가 꺼지지는 않습니다. 이미 깊이 버퍼에 기록된 값과 비교하는 테스트는 그대로 동작해, 앞서 그려진 불투명 오브젝트 뒤의 프래그먼트는 여전히 걸러집니다.

다만 이 오브젝트는 자신의 깊이를 버퍼에 남기지 않으므로, 이후 드로우 콜의 Early-Z 판단에는 보탬이 되지 않습니다.

반투명 표면이 깊이를 기록해 버리면 그 뒤의 오브젝트가 깊이 테스트에서 탈락해, 투명한 표면 너머로 보여야 할 장면이 사라집니다. 반투명 오브젝트가 `ZWrite Off`를 쓰는 것도 이를 피하기 위해서입니다. 따라서 반투명 오브젝트는 보통 깊이를 읽기만 하고 쓰지는 않으며, 그만큼 이후 렌더링에서 Early-Z로 얻을 이점도 줄어듭니다.

---

## 스텐실 버퍼

깊이 테스트가 앞뒤 관계를 기준으로 프래그먼트를 걸러낸다면, 스텐실 테스트는 *어느 영역에 그릴 수 있는지*를 기준으로 프래그먼트를 걸러냅니다. 이 판정에 사용하는 픽셀별 저장 공간이 **스텐실 버퍼(Stencil Buffer)**이고, 스텐실 버퍼 값을 기준으로 통과 여부를 정하는 과정이 스텐실 테스트입니다.

스텐실 버퍼에는 픽셀마다 정수 값 하나가 저장됩니다. 보통 8비트를 사용하므로 0부터 255까지의 값을 담을 수 있습니다. 앞서 본 D24S8 형식에서는 깊이 24비트와 스텐실 8비트가 하나의 깊이/스텐실 텍스처 안에 함께 저장됩니다.

프래그먼트가 들어오면 GPU는 해당 픽셀의 스텐실 값과 미리 지정한 참조 값(Ref)을 비교합니다. 비교 함수로는 Equal, NotEqual, Less, Greater 등을 사용할 수 있습니다. 조건을 만족한 프래그먼트는 다음 단계로 넘어가고, 만족하지 못한 프래그먼트는 폐기됩니다.

테스트 결과에 따라 스텐실 값을 어떻게 바꿀지도 지정할 수 있습니다. 값을 유지하는 Keep, 참조 값으로 덮어쓰는 Replace, 값을 증가·감소시키는 Increment·Decrement 같은 동작을 통과, 실패, 깊이 실패 상황별로 따로 설정할 수 있습니다. 읽기 마스크와 쓰기 마스크를 함께 사용하면 하나의 8비트 스텐실 버퍼를 여러 용도로 나눠 쓸 수도 있습니다.

이 구조를 이용하면 특정 영역에 먼저 값을 표시해 둔 뒤, 그 영역에만 그리거나 반대로 그 영역을 피해 그릴 수 있습니다. 즉 스텐실 버퍼는 픽셀 단위의 마스크로 동작합니다.

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

스텐실 버퍼는 화면의 일부 영역에만 렌더링을 허용하고 싶을 때 자주 사용됩니다.
보통은 두 단계로 구성합니다. 첫 번째 패스에서 허용할 영역을 스텐실 값으로 표시하고, 두 번째 패스에서 그 값을 비교해 통과한 픽셀에만 실제 내용을 그립니다.

**거울 효과**는 첫 번째 패스에서 거울 표면이 차지하는 픽셀에 스텐실 값을 기록합니다. 두 번째 패스에서는 거울에 비친 장면을 렌더링하되, 비교 함수를 Equal로 두고 참조 값을 거울에 기록한 값으로 맞춥니다. 그러면 반사 영상은 스텐실 값이 일치하는 거울 안쪽에만 그려집니다.

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
  <text x="210" y="351" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">거울 밖에는 반사 장면이 그려지지 않음</text>
</svg>
</div>

**외곽선 효과**는 먼저 오브젝트를 평소대로 그리면서 해당 픽셀에 스텐실 1을 기록합니다. 다음 패스에서는 같은 오브젝트를 조금 키워 외곽선 색으로 그리되, 비교 함수를 NotEqual로 두어 스텐실이 1인 본체 안쪽은 건너뜁니다. 그러면 본체와 겹치지 않는 바깥쪽 픽셀에만 색이 남아 외곽선처럼 보입니다.

**포털 효과**는 포털 프레임이 차지하는 영역에 스텐실 값을 기록한 뒤, 다른 카메라가 렌더링한 포털 너머의 장면을 그립니다. 스텐실 값이 일치하는 픽셀만 통과시키면, 다른 공간의 영상이 포털 프레임 안쪽에만 표시됩니다.

Unity 셰이더에서는 이런 스텐실 동작을 `Stencil` 블록에 작성합니다. 비교에 사용할 참조 값(`Ref`), 비교 함수(`Comp`), 테스트 결과에 따라 버퍼 값을 바꾸는 동작(`Pass`·`Fail`·`ZFail`)을 이 블록에서 지정합니다. 동작에는 Keep, Replace, Increment, Decrement, Invert 등을 사용할 수 있습니다.

UI를 특정 모양 안쪽으로 제한하는 클리핑도 같은 원리를 사용합니다. UI 시스템의 **Mask** 컴포넌트는 Mask 오브젝트가 차지하는 영역에 스텐실 값을 기록하고, 자식 UI 요소는 그 값이 일치하는 픽셀에만 그려지게 합니다. Mask를 여러 겹으로 중첩하면 마스크 값이 비트 단위로 누적되며, 8비트 스텐실 범위 안에서 제한된 깊이만큼 중첩할 수 있습니다.

다만 Mask는 마스크 영역을 스텐실에 기록하고 자식을 모두 그린 뒤 그 값을 되돌리는 단계를 거치므로, 드로우 콜이 더 늘어납니다. 자식 요소도 스텐실 비교 설정이 들어간 상태로 그려져, 마스크 밖이나 다른 마스크에 속한 요소와 한 배치로 묶이지 못해 배칭이 끊길 수 있습니다. 

또한 직접 작성한 UI 셰이더에는 이런 스텐실 처리가 기본으로 들어 있지 않으므로, 기본 `UI/Default` 셰이더에서 스텐실 프로퍼티(`_StencilComp`·`_Stencil`·`_StencilOp` 등)와 그 값을 읽는 `Stencil` 블록을 함께 가져와 넣어야 합니다. 자식의 클리핑은 Mask가 직접 하는 것이 아니라 자식 셰이더의 스텐실 비교로 이루어지고, Unity는 그 비교에 쓸 참조 값과 함수를 런타임에 이 프로퍼티로 넘겨주기 때문입니다. 이 둘이 없으면 비교 자체가 일어나지 않아, 자식이 마스크 밖에서도 그대로 그려집니다.

2D 스프라이트에서는 **SpriteMask** 컴포넌트가 같은 역할을 합니다. SpriteMask도 내부적으로 스텐실 버퍼를 사용하며, SpriteRenderer의 **Mask Interaction**을 Visible Inside Mask 또는 Visible Outside Mask로 설정해 마스크 안쪽과 바깥쪽 중 어느 쪽을 보일지 정합니다. 커스텀 스프라이트 셰이더를 사용할 때는 UI Mask와 마찬가지로 스텐실 관련 프로퍼티와 패스 설정을 포함해야 합니다.

반면 **RectMask2D**는 스텐실 버퍼를 사용하지 않습니다. RectTransform이 정한 사각형 영역을 기준으로 바깥쪽 UI 요소를 렌더링 대상에서 제외하므로, 일반 Mask보다 비용이 낮고 배칭에 주는 영향도 작습니다. 대신 마스크 모양은 직사각형으로 제한됩니다. 원형이나 불규칙한 윤곽이 필요하면 스텐실을 사용하는 Mask를 써야 합니다.

---

## 블렌딩

앞서 다룬 깊이 테스트와 스텐실 테스트는 프래그먼트를 통과시킬지 버릴지를 정할 뿐입니다. 통과한 프래그먼트의 색은 기본적으로 프레임 버퍼의 기존 색을 덮어쓰며, 두 색을 섞지는 않습니다.

불투명 오브젝트는 이 덮어쓰기만으로 충분합니다. 뒤가 비치지 않으니, 같은 픽셀에는 가장 가까운 색 하나만 남아도 결과가 맞기 때문입니다.

반면 유리나 물, 파티클처럼 뒤가 비쳐 보여야 하는 반투명 오브젝트는 덮어쓰면 뒤쪽 색이 사라집니다. 이를 막으려면 새 색과 기존 색을 일정 비율로 섞어 앞뒤가 함께 보이게 해야 합니다. 이 처리가 **블렌딩(Blending)**입니다.

### 블렌딩 공식

블렌딩의 계산은 단순합니다. 새로 들어온 색과 프레임 버퍼에 이미 있던 색에 각각 팩터(factor)를 곱한 다음 더하는, 두 색의 가중합입니다.

$$\text{최종 색상} = \text{Src} \times \text{SrcFactor} + \text{Dst} \times \text{DstFactor}$$

식의 네 항은 색과 팩터로 나뉩니다. 색은 소스(Src)와 대상(Dst) 둘인데, 소스는 프래그먼트 셰이더가 출력한 색이고 대상은 같은 픽셀의 프레임 버퍼에 이미 기록되어 있던 색입니다. 두 색은 블렌딩 시점에 이미 정해져 들어오는 값이라 바꿀 수 없습니다. 반면 각 색에 곱하는 소스 팩터(SrcFactor)와 대상 팩터(DstFactor)는 셰이더에서 지정하는 값으로, 두 색을 어떤 비율로 합칠지를 정합니다.

따라서 어떤 결과가 나올지는 이 두 팩터가 정합니다. 색을 그대로 둔 채 팩터만 달리해도 합성 결과가 달라지며, 뒤에서 다룰 Alpha Blending과 Additive Blending의 차이 또한 두 팩터에 어떤 값을 지정하는가에 있습니다.

### Alpha Blending

**Alpha Blending**은 소스의 알파 값을 그대로 합성 비율로 삼는 블렌딩입니다. 알파는 앞서 프레임 버퍼에서 본 불투명도 값으로, 이 값이 곧 새 색이 차지하는 몫이 되고 나머지는 뒤쪽 색이 채웁니다. 그래서 알파가 클수록 새 색이 더 진하게 드러나고, 작을수록 뒤쪽 색이 더 많이 비칩니다. 유리나 물처럼 뒤가 비쳐 보여야 하는 반투명 표면이 이렇게 그려집니다.

이 비율을 블렌딩 공식의 두 팩터로 옮기면, 소스 팩터는 알파가 되고 대상 팩터는 그 나머지인 1에서 알파를 뺀 값이 됩니다.

- **소스 팩터**: $\text{SrcAlpha}$ $(= \text{src.a})$
- **대상 팩터**: $\text{OneMinusSrcAlpha}$ $(= 1 - \text{src.a})$

$$\text{최종 색상} = \text{src.rgb} \times \text{src.a} + \text{dst.rgb} \times (1 - \text{src.a})$$

이렇게 두 팩터의 합은 언제나 1이 되므로, 소스와 대상은 정해진 몫을 나눠 가질 뿐 합성 결과가 원래 밝기 범위를 벗어나지 않습니다.

예를 들어 불투명도가 30%, 곧 $\text{alpha} = 0.3$ 인 빨강 소스 $(1,\,0,\,0)$ 를 파랑 대상 $(0,\,0,\,1)$ 위에 그린다면, 합성 결과는 다음과 같습니다.

$$\begin{aligned}
\text{최종} &= (1,\,0,\,0) \times 0.3 + (0,\,0,\,1) \times 0.7 \\\\
&= (0.3,\,0,\,0) + (0,\,0,\,0.7) \\\\
&= (0.3,\,0,\,0.7) \quad \rightarrow \text{30\% 빨강 + 70\% 파랑}
\end{aligned}$$

### Additive Blending

**Additive Blending**은 소스 색과 대상 색을 비율 조정 없이 그대로 더하는 블렌딩입니다. Alpha Blending이 알파에 따라 두 색을 각각 줄여 섞은 것과 달리, 여기서는 두 색을 줄이지 않고 곧바로 합칩니다.

이를 블렌딩 공식의 두 팩터로 옮기면, 소스 팩터와 대상 팩터가 모두 1이 됩니다. 두 색에 1을 곱하면 값이 그대로 남으므로, 식은 두 색을 그대로 더한 값이 됩니다.

- **소스 팩터**: $\text{One}$ $(= 1)$
- **대상 팩터**: $\text{One}$ $(= 1)$

$$\text{최종 색상} = \text{src.rgb} \times 1 + \text{dst.rgb} \times 1 = \text{src.rgb} + \text{dst.rgb}$$

두 색을 그대로 더하면, 겹친 부분은 원래의 두 색보다 밝아집니다. 결과를 밝기 범위 안에 묶어 두던 Alpha Blending과 달리, 더한 값은 채널이 표현할 수 있는 최댓값을 넘어설 수 있습니다. 이때 넘친 값은 최댓값으로 잘리므로, 색이 거듭 더해진 자리는 모든 채널이 차올라 흰색에 가까워집니다.

실제로도 여러 빛이 한곳에 모이면 더 밝아집니다. Additive Blending은 이렇게 더해지는 빛을 그대로 표현하기 때문에, 불꽃이나 빛줄기처럼 빛이 모여 강해지는 파티클 이펙트에 자주 쓰입니다.

### 반투명 오브젝트의 정렬 문제

깊이 테스트 덕분에 불투명 오브젝트는 어떤 순서로 그려도 최종 결과가 같았습니다. 깊이 테스트가 가장 가까운 표면만 남기고 나머지를 걸러내기 때문입니다. 반면 반투명 표면은 뒤쪽을 덮어쓰지 않고 섞으므로, 블렌딩이 그 순간 프레임 버퍼에 들어 있는 색을 대상으로 가져옵니다. 그래서 같은 자리에 반투명 표면이 겹치면 나중에 그린 색이 먼저 그린 색 위에 합성되고, 그리는 순서가 곧 앞뒤로 겹치는 순서가 됩니다.

올바른 겹침을 얻으려면 더 먼 표면이 버퍼에 먼저 들어가 있어야 합니다. 그래서 반투명 오브젝트는 **뒤에서 앞(back-to-front)** 순서로, 가장 먼 표면부터 그립니다. 먼 표면을 먼저 기록하고 그 위에 가까운 표면을 차례로 합성하면, 뒤쪽 색이 앞쪽 반투명 표면을 통해 자연스럽게 비칩니다.

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

이 뒤→앞은 불투명 오브젝트의 그리기 순서와 반대입니다. 불투명은 어떤 순서로 그려도 결과가 같으니, 그 자유를 성능에 씁니다. Early-Z 절에서 다룬 대로, 가까운 것부터 앞→뒤로 그리면 뒤쪽 프래그먼트를 일찍 걸러내 셰이딩 비용을 아낄 수 있기 때문입니다. 반면 반투명은 순서가 최종 색을 바꾸므로 그런 자유가 없고, 정확한 결과를 위해 반드시 먼 것부터 뒤→앞으로 그려야 합니다.

Unity가 불투명과 반투명을 서로 다른 렌더 큐로 나누는 것도 이 정렬 순서 때문입니다. 앞서 본 Opaque 큐(2000번대)가 불투명 오브젝트를 앞→뒤로 그렸다면, 반투명 오브젝트는 Transparent 큐(3000번대)에 모여 뒤→앞으로 정렬됩니다.

그런데 이 뒤→앞 정렬은 오브젝트 단위로 이뤄집니다. 화면의 픽셀마다 어느 표면이 더 먼지 일일이 따져 순서를 매기는 것은 비용이 너무 크기 때문입니다. 그래서 Unity는 오브젝트의 중심처럼 대표 깊이 하나를 뽑아, 그 값으로 오브젝트 전체를 그릴 차례를 정합니다.

오브젝트들이 서로 떨어져 있으면 이 방식으로 충분합니다. 문제는 두 반투명 오브젝트가 서로 뚫고 지나갈 때입니다. 예를 들어 반투명한 두 판이 X자로 교차하면, 한 판은 교차선을 경계로 한쪽에서는 다른 판 앞에, 반대쪽에서는 뒤에 놓입니다. 그런데 대표 깊이는 오브젝트마다 하나뿐이라, 이렇게 한 오브젝트가 '앞이면서 동시에 뒤'인 상태를 담아내지 못합니다.

결국 두 판 가운데 하나가 통째로 앞으로 정렬되어, 원래 상대 뒤에 있어야 할 부분에서도 상대를 덮습니다. 그래서 교차 부분에서 두 판이 자연스럽게 엇갈리지 못하고, 한쪽 판만 앞에 보이면서 그 경계가 부자연스럽게 끊겨 보입니다. 이는 반투명을 픽셀이 아니라 오브젝트 단위로 정렬하는 래스터화 렌더링의 대표적인 한계입니다.

---

## 렌더 타겟과 MRT

출력 병합을 거친 색은 어딘가에 기록되어야 합니다. 지금까지는 그 대상을 화면에 그대로 표시될 프레임 버퍼로 두고 살펴봤습니다.

다만 기록 대상이 언제나 화면용 프레임 버퍼인 것은 아닙니다. 렌더링 결과를 디스플레이로 곧바로 내보내지 않고, 화면 밖 텍스처에 담아 두었다가 이후 단계에서 다시 쓰는 경우도 많습니다. 거울에 비친 모습을 그릴 때가 그렇습니다.

출력 병합의 결과가 기록되는 이 대상을 **렌더 타겟(Render Target)**이라고 부릅니다. 화면에 표시될 프레임 버퍼도 렌더 타겟이고, 화면 밖에 따로 마련한 텍스처도 렌더 타겟입니다.

### 렌더 텍스처

렌더 타겟이 화면 밖에 둔 텍스처일 때, 그 텍스처를 **렌더 텍스처(Render Texture)**라고 부릅니다.

앞의 거울이 바로 이 경우입니다. 거울 시점으로 한 번 렌더링한 결과가 렌더 텍스처에 기록되고, 이 텍스처를 거울 표면의 머티리얼에 입히면 반사가 화면에 나타납니다.

거울처럼 한 패스에서 먼저 그려 두고 그 결과를 다음 패스가 입력으로 읽는 방식은 렌더 텍스처에서 폭넓게 쓰입니다. 화면에 출력하기 전 색을 보정하는 후처리, 수면 반사, 광원 시점에서 먼저 렌더링하는 그림자 맵이 모두 이 구조를 따릅니다.

Unity에서는 `RenderTexture` 클래스가 이 역할을 합니다. 카메라의 Target Texture에 RenderTexture를 지정하면, 그 카메라의 출력은 화면이 아니라 해당 렌더 텍스처에 기록됩니다.

### MRT (Multiple Render Targets)

일반적인 렌더링에서는 프래그먼트 셰이더가 색 하나를 출력하고, 그 값이 렌더 타겟 하나에 기록됩니다.

**MRT(Multiple Render Targets)**는 이 출력 대상을 여러 개로 늘리는 기능입니다. 프래그먼트 셰이더가 한 번 실행될 때 **여러 값을 한꺼번에 출력하고**, 각 값은 서로 다른 렌더 타겟에 동시에 기록됩니다. 같은 프래그먼트를 다시 그리지 않고도 색, 법선, 깊이처럼 성격이 다른 데이터를 한 패스에서 나눠 저장할 수 있습니다.

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

MRT를 대표적으로 활용하는 사례가 **Deferred Rendering(디퍼드 렌더링)**입니다. 이름 그대로 조명 계산을 뒤로 미루는 방식인데, 무엇을 얻으려고 미루는지는 조명을 그 자리에서 바로 계산하는 **Forward Rendering**과 비교하면 드러납니다.

Forward Rendering은 오브젝트를 그리는 동안 조명까지 한꺼번에 계산합니다. 광원이 N개, 오브젝트가 M개인 장면이라면 조명 계산이 최대 N × M번에 이를 수 있어, 광원이든 오브젝트든 늘어나는 만큼 비용이 가파르게 불어납니다.

Deferred Rendering은 이 비용을 덜기 위해 렌더링을 두 단계로 나눕니다.

첫 단계인 **Geometry Pass**에서는 조명을 아직 계산하지 않습니다. 오브젝트의 색상과 법선, 스페큘러, 깊이 같은 표면 정보만 MRT로 여러 렌더 텍스처에 한꺼번에 기록합니다. 이렇게 표면 정보가 종류별로 나뉘어 담긴 텍스처 묶음을 **G-Buffer**라고 부릅니다.

두 번째 단계인 **Lighting Pass**에 이르러서야 조명을 계산합니다. G-Buffer에 저장해 둔 색상과 법선, 스페큘러, 깊이를 읽어, 화면을 채운 픽셀 하나하나의 음영을 정합니다.

이렇게 단계를 나누면 조명 계산이 오브젝트 수를 따라 늘어나지 않습니다. Geometry Pass를 지나고 나면 한 픽셀에 오브젝트가 몇 개나 겹쳐 있었든 가장 가까운 표면 하나만 G-Buffer에 남고, 그 정보를 읽는 Lighting Pass는 오브젝트가 아니라 화면의 픽셀을 대상으로 삼기 때문입니다. 따라서 같은 화면이라면 오브젝트가 10개든 1만 개든 조명 단계의 비용은 크게 달라지지 않습니다.

그렇다고 조명 비용이 아예 사라지는 것은 아닙니다. 픽셀 하나의 색을 정하려면 그 자리에 닿는 광원을 하나씩 더해 가야 하므로, 광원이 늘어나는 데에는 Forward와 Deferred 모두 비용이 따릅니다. 다만 그 비용이 불어나는 방식이 서로 다릅니다.

Forward는 광원이 하나 늘 때마다 오브젝트마다 조명을 다시 계산하므로, 그 비용이 오브젝트 수만큼 곱해집니다. 반면 Deferred의 Lighting Pass는 앞서 본 대로 오브젝트가 아니라 화면의 픽셀을 대상으로 하므로, 광원이 늘어도 그 비용은 픽셀 수에만 더해질 뿐 오브젝트 수와는 무관합니다.

이 차이는 광원이 많아질수록 벌어집니다. 따라서 한 장면을 비추는 광원이 많을수록 Deferred Rendering이 유리해집니다.

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

### Deferred Rendering의 비용과 한계

조명 계산을 줄이는 이점을 얻는 대신, Deferred는 Geometry Pass와 Lighting Pass 사이 내내 G-Buffer를 GPU 메모리에 유지해야 합니다. Geometry Pass가 기록한 색상, 법선, 스페큘러, 깊이는 한 장에 모이지 않고 종류마다 다른 텍스처에 나뉘어 담기는데, 그 텍스처 하나하나가 화면 전체를 덮는 크기입니다. 결국 화면을 가득 채운 이미지 여러 장이 Lighting Pass가 다 읽어 갈 때까지 메모리에 나란히 올라가 있어야 합니다.

규모를 가늠해 보면, Full HD 해상도에서 RGBA8 텍스처 한 장이 약 8MB입니다. G-Buffer가 텍스처 서너 장으로 이루어지면 그것만으로 24\~32MB가 듭니다. 게다가 이 텍스처들을 매 프레임 새로 기록하고 다시 읽어 들이므로, 늘어나는 것은 메모리 용량만이 아니라 그 사이를 오가는 대역폭이기도 합니다.

비용이 메모리에만 그치지는 않습니다. G-Buffer가 한 픽셀에 가장 가까운 표면 하나의 정보만 남기는 탓에, Deferred가 구조적으로 제대로 담아내지 못하는 오브젝트도 있습니다. 대표적인 경우가 반투명 오브젝트입니다.

벽 앞에 반투명 유리가 놓인 장면이라면, 그 픽셀을 제대로 그리는 데에 유리 자체의 색과 그 너머로 비치는 벽의 색이 모두 필요합니다. 그런데 유리의 색과 법선을 G-Buffer에 적는 순간 그 자리에 있던 벽의 정보가 덮여, 정작 합성에 있어야 할 뒤쪽 색이 사라집니다.

따라서 반투명 오브젝트는 G-Buffer를 거치지 않습니다. 불투명 오브젝트를 Deferred로 모두 그린 다음, 그 위에 반투명 표면을 Forward 패스로 덧그립니다. 이때 반투명 표면의 색이 화면에 이미 칠해진 색과 직접 섞이므로, G-Buffer에서라면 사라졌을 뒤쪽 색이 그대로 합성에 쓰입니다. 실제로 Deferred를 쓰는 렌더러도 반투명만큼은 이렇게 Forward 경로로 처리합니다.

안티앨리어싱에서도 비슷한 한계가 나타납니다. **MSAA**는 한 픽셀 안에 여러 서브 샘플을 두고 그 값들을 모아 가장자리의 계단을 누그러뜨리는 기법인데, Deferred에서는 이 서브 샘플을 G-Buffer의 타겟마다 따로 보관했다가 조명 계산을 마친 뒤에야 합칠 수 있습니다. 그만큼 메모리와 대역폭, 구현 복잡도가 함께 늘어납니다. 이 때문에 MSAA 대신, 화면이 다 그려진 다음 적용하는 FXAA나 TAA 같은 후처리 안티앨리어싱에 의존하는 경우가 많습니다.

이 비용들 가운데 메모리와 대역폭 부담은 어느 플랫폼에서 렌더링하느냐에 따라 크게 달라집니다. 자원이 넉넉하지 않은 모바일에서는 이 부담이 특히 큽니다. Unity의 URP가 모바일 프로젝트에서 Forward Rendering을 기본값으로 두는 것도 이런 사정 때문입니다. 다만 모바일에서 이 부담이 늘 같은 정도로 큰 것은 아닙니다. [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 TBDR 아키텍처에서는 G-Buffer의 일부를 타일 단위로 온칩 메모리에서 처리할 수 있어, 대역폭 부담을 어느 정도 줄일 여지가 있습니다.

반대로 메모리와 대역폭에 여유가 있는 데스크톱과 콘솔에서는 이 부담이 렌더링 방식을 가를 만큼 결정적이지 않습니다. 이런 환경에서는 장면을 비추는 광원의 수와 표현하려는 효과를 따져, Forward와 Deferred를 적절히 사용합니다.

---

## 출력 병합의 전체 흐름

앞에서는 깊이 테스트와 스텐실 테스트, 블렌딩, 렌더 타겟을 단계별로 따로 살펴봤습니다. 이 단계들은 실제로는 하나의 경로로 이어져 있어서, 프래그먼트 하나가 그 길을 차례로 지나며 렌더 타겟에 기록됩니다. 아래 다이어그램은 그 경로를 위에서 아래로 정리한 것입니다.

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

맨 위의 래스터화가 만들어 낸 프래그먼트는 프래그먼트 셰이더를 거쳐 색을 얻습니다. 이때 깊이 테스트가 셰이더 앞에 오는지 뒤에 오는지는 드로우 콜에 따라 달라집니다. Early-Z가 적용되면 셰이더 앞에서 깊이 테스트를 먼저 수행해(다이어그램의 점선 단계) 가려질 프래그먼트를 셰이딩 전에 걸러 내고, 적용되지 않으면 셰이더를 지난 뒤 Late-Z 경로에서 깊이 테스트를 수행합니다. 같은 프래그먼트가 두 경로를 중복으로 거치지는 않습니다.

셰이딩을 마친 프래그먼트는 스텐실 테스트를 거치며, Late-Z 경로라면 깊이 테스트도 이 단계에서 함께 실행됩니다. 두 테스트는 프래그먼트를 통과시킬지 버릴지 결정할 뿐, 색을 섞지는 않습니다. 통과한 프래그먼트만 블렌딩 단계로 넘어가, 블렌딩이 켜져 있으면 렌더 타겟에 이미 칠해진 색과 합성됩니다. 그 결과는 렌더 타겟에 기록되며, 대상이 프레임 버퍼라면 화면으로 출력되고 렌더 텍스처라면 이후 패스의 입력이 됩니다.

이 경로가 거치는 버퍼들은 저마다 화면 크기만 한 메모리를 차지합니다. 각 버퍼의 역할과 크기를 정리하면 다음과 같습니다.

| 버퍼 | 크기/형식 | 역할 |
|------|-----------|------|
| 프레임 버퍼 (색상 버퍼) | RGBA8/16F, 4~8 B/pixel | 최종 색상 저장 |
| 깊이+스텐실 버퍼 | D24S8 (4 B/pixel) 또는 D32F_S8 (8 B/pixel) | 가시성 판별 (깊이 테스트) + 조건부 렌더링 (마스킹) |
| 렌더 텍스처 | 다양 | 오프스크린 렌더링, MRT, G-Buffer, 포스트 프로세싱 |

예를 들어 1920x1080 해상도에서 RGBA8 색상 버퍼와 D24S8 깊이+스텐실 버퍼를 사용하면, 색상 버퍼가 약 8MB, 깊이+스텐실 버퍼가 약 8MB를 차지합니다. 기본 출력 버퍼만 계산해도 프레임 하나에 약 16MB가 필요합니다.

---

## 마무리

이번 글에서는 프래그먼트 셰이더가 만든 결과가 렌더 타겟에 기록되기 전, 출력 병합 단계에서 거치는 검사와 합성을 정리했습니다. 핵심은 다음과 같습니다.

- **프레임 버퍼**는 화면에 보일 색을 저장하는 버퍼입니다. RGBA8은 픽셀당 4바이트를 차지하며, HDR 렌더링에서는 RGBA16F나 R11G11B10F 같은 형식을 씁니다.
- **깊이 버퍼(Z-Buffer)**는 픽셀마다 가장 가까운 표면의 깊이를 저장해 가시성을 판별합니다. 원근 투영의 깊이 값은 비선형이므로 far 쪽 정밀도가 부족해질 수 있고, 이로 인해 z-fighting이 나타날 수 있습니다.
- **Reversed-Z**는 깊이 방향을 뒤집어 near=1, far=0으로 두는 기법입니다. D32F 같은 부동소수점 깊이 버퍼와 함께 쓰면 원거리 깊이 정밀도를 개선할 수 있습니다.
- **Early-Z**는 깊이 테스트를 프래그먼트 셰이더 앞으로 앞당겨 보이지 않을 프래그먼트의 셰이딩을 줄입니다. `discard`, `clip`, `SV_Depth`처럼 셰이더가 가시성이나 깊이를 바꿀 수 있는 경우에는 제한됩니다.
- **스텐실 버퍼**는 픽셀마다 정수 값을 저장해 특정 영역에만 그리거나 특정 영역을 제외하는 마스크로 사용됩니다. 거울, 포털, 외곽선, UI Mask, SpriteMask가 대표적인 활용 예입니다.
- **블렌딩**은 새 프래그먼트의 색을 렌더 타겟에 이미 있는 색과 합성합니다. 반투명 오브젝트는 결과가 순서에 의존하므로 일반적으로 뒤에서 앞(back-to-front) 순서로 그립니다.
- **렌더 타겟**은 렌더링 결과가 기록되는 대상입니다. 화면 밖 텍스처에 기록하면 렌더 텍스처가 되며, MRT를 사용하면 한 패스에서 여러 렌더 타겟에 동시에 데이터를 저장할 수 있습니다.
- **Deferred Rendering**은 MRT로 표면 정보를 G-Buffer에 모아 둔 뒤 조명을 나중에 한 번에 계산하는 방식입니다. 조명 비용이 오브젝트 수와 분리되어 광원이 많은 장면에 유리하지만, G-Buffer를 메모리에 유지해야 하고 반투명은 Forward 경로로 따로 그려야 합니다.

정리하면, 같은 장면이라도 어떤 버퍼 형식을 쓰는지, 오브젝트를 어떤 순서로 그리는지, 결과를 프레임 버퍼에 기록하는지 렌더 텍스처에 기록하는지에 따라 화면의 정확성과 성능이 함께 달라집니다.

다만 프레임 버퍼에 색이 모두 기록되었다고 해서 그 이미지가 바로 화면에 보이는 것은 아닙니다. GPU가 만든 프레임이 디스플레이로 전달되는 과정에는 스캔아웃과 동기화 문제가 있고, 이 타이밍이 맞지 않으면 화면이 가로로 찢어지는 티어링이 나타날 수 있습니다.

[다음 글](/dev/unity/RasterPipeline-3/)에서는 스캔아웃과 티어링, VSync, 더블·트리플 버퍼링을 다룬 뒤, 래스터화가 안고 있는 근본적 한계인 앨리어싱과 그것을 다듬는 안티앨리어싱 기법까지 살펴봅니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

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
