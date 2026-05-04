---
layout: single
title: "조명과 그림자 (2) - 그림자와 후처리 - soo:bak"
date: "2026-02-19 21:30:00 +0900"
description: Shadow Map, Cascade Shadow, 그림자 대안, 포스트 프로세싱 비용을 설명합니다.
tags:
  - Unity
  - 최적화
  - 그림자
  - 후처리
---

## 빛이 있으면 그림자가 있습니다

[Part 1](/dev/unity/LightingAndShadows-1/)에서는 실시간 조명과 베이크 조명의 비용 구조를 다루었습니다.

조명은 화면의 밝기와 색감을 결정하며, 광원이 닿는 영역과 닿지 않는 영역의 대비가 장면의 분위기를 만듭니다. 

다만 조명만으로는 물체가 바닥이나 주변 환경에 연결되어 있다는 인상을 만들기 어렵습니다. 실제 세계에서는 빛이 오브젝트에 가로막히면 그 뒤에 어두운 영역, 즉 **그림자(Shadow)**가 생기며, 캐릭터가 바닥에 서 있고 건물이나 소품이 지면에 닿아 있다는 시각적 단서를 제공합니다.

그림자가 없으면 오브젝트가 공중에 떠 있는 것처럼 보입니다.

그런데 실시간 그림자를 그리려면 광원의 위치에서 장면을 한 번 더 렌더링해야 하므로, 렌더 패스와 메모리 비용이 별도로 추가됩니다. 또한 **포스트 프로세싱(Post-Processing)**, 즉 렌더링이 끝난 뒤 화면 전체에 추가 효과를 적용하는 단계도 장면 전체를 한 번 더 처리해야 하므로, 그림자와 함께 프레임 예산에서 별도의 비중을 차지합니다.

이어지는 섹션에서는 Shadow Map의 원리와 비용 절감 기법, 저비용 그림자 대안, 그리고 포스트 프로세싱의 구조와 비용을 차례로 다룹니다.

---

## Shadow Map의 원리

**Shadow Map**은 광원에서 출발한 빛이 처음 닿는 물체 표면까지의 거리를 기록한 깊이 텍스처로, 이를 통해 카메라 시점에서 어디가 빛에 닿고 어디가 가려져 있는지 판정합니다.

이 때, '그림자'를 판정하기 위해서는 '광원에서 빛이 어디까지 닿는지'와 '카메라가 본 표면이 어디에 있는지'를 알아야 합니다. 이어지는 두 단계에서 광원 시점 렌더링과 카메라 시점 렌더링이 어떻게 이 정보를 모으는지 차례로 다룹니다.

### 1단계: 광원 시점에서 깊이 텍스처 생성

먼저 GPU는 광원의 시점을 가상의 카메라로 삼아 장면을 렌더링합니다. 이 패스에서는 색상을 계산하지 않고, 광원에서 각 표면까지의 거리, 즉 **깊이(depth)**만 기록합니다.

일반 색상 텍스처가 R, G, B 채널로 색을 기록한다면, Shadow Map은 각 텍셀에 거리 값 하나만 담습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Shadow Map 생성 (1단계)</text>
  <text x="270" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">광원이 카메라가 되어 본 장면의 깊이 이미지</text>

  <!-- ===== 좌측 영역: 장면 측면도 (x = 0 ~ 250) ===== -->
  <text x="155" y="60" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6" font-weight="bold">실제 장면</text>

  <!-- 광원 (상단 좌측 — 위에서 비춤) -->
  <circle cx="35" cy="82" r="12" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="35" cy="82" r="4" fill="currentColor" fill-opacity="0.7"/>
  <text x="55" y="78" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">광원</text>

  <!-- 광원에서 ray fan (점선, 광원이 위에서 아래·우측으로 비춤) -->
  <line x1="42" y1="92" x2="95" y2="105" stroke="currentColor" stroke-width="0.7" stroke-dasharray="3,2" opacity="0.45"/>
  <line x1="44" y1="93" x2="125" y2="115" stroke="currentColor" stroke-width="0.7" stroke-dasharray="3,2" opacity="0.45"/>
  <line x1="45" y1="94" x2="160" y2="125" stroke="currentColor" stroke-width="0.7" stroke-dasharray="3,2" opacity="0.45"/>
  <line x1="46" y1="94" x2="200" y2="148" stroke="currentColor" stroke-width="0.7" stroke-dasharray="3,2" opacity="0.45"/>
  <line x1="46" y1="95" x2="235" y2="148" stroke="currentColor" stroke-width="0.7" stroke-dasharray="3,2" opacity="0.45"/>

  <!-- 건물 (가까움 — 광원 아래 좌측) -->
  <rect x="78" y="105" width="50" height="40" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.2"/>
  <text x="103" y="129" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">건물</text>

  <!-- 나무 (중간 — 광원 아래 가운데) -->
  <polygon points="160,115 140,145 180,145" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="160" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">나무</text>

  <!-- 바닥 (멀음 — 광원 아래 우측까지 펼쳐짐) -->
  <line x1="65" y1="148" x2="240" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="160" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">바닥</text>

  <!-- ===== 중간: 화살표 + 비유 라벨 (x = 250 ~ 290) ===== -->
  <line x1="252" y1="135" x2="285" y2="135" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,131 291,135 285,139" fill="currentColor"/>
  <text x="269" y="120" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">광원 시점</text>
  <text x="269" y="153" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">렌더링</text>

  <!-- ===== 우측 영역: Shadow Map = 깊이 이미지 (x = 295 ~ 535) ===== -->
  <text x="415" y="60" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6" font-weight="bold">Shadow Map (깊이 이미지)</text>

  <!-- 6×4 grid: 24 텍셀, 각 cell 40×30, x_start=295, y_start=75 -->

  <!-- Row 0: y=75~105 -->
  <rect x="295" y="75" width="40" height="30" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.5"/>
  <text x="315" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">5</text>
  <rect x="335" y="75" width="40" height="30" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="0.5"/>
  <text x="355" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">6</text>
  <rect x="375" y="75" width="40" height="30" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="0.5"/>
  <text x="395" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">9</text>
  <rect x="415" y="75" width="40" height="30" fill="currentColor" fill-opacity="0.27" stroke="currentColor" stroke-width="0.5"/>
  <text x="435" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">13</text>
  <rect x="455" y="75" width="40" height="30" fill="currentColor" fill-opacity="0.39" stroke="currentColor" stroke-width="0.5"/>
  <text x="475" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">17</text>
  <rect x="495" y="75" width="40" height="30" fill="currentColor" fill-opacity="0.50" stroke="currentColor" stroke-width="0.5"/>
  <text x="515" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">20</text>

  <!-- Row 1: y=105~135 -->
  <rect x="295" y="105" width="40" height="30" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="0.5"/>
  <text x="315" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">5</text>
  <rect x="335" y="105" width="40" height="30" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.5"/>
  <text x="355" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">7</text>
  <rect x="375" y="105" width="40" height="30" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.5"/>
  <text x="395" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">10</text>
  <rect x="415" y="105" width="40" height="30" fill="currentColor" fill-opacity="0.27" stroke="currentColor" stroke-width="0.5"/>
  <text x="435" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">13</text>
  <rect x="455" y="105" width="40" height="30" fill="currentColor" fill-opacity="0.39" stroke="currentColor" stroke-width="0.5"/>
  <text x="475" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">17</text>
  <rect x="495" y="105" width="40" height="30" fill="currentColor" fill-opacity="0.50" stroke="currentColor" stroke-width="0.5"/>
  <text x="515" y="125" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">20</text>

  <!-- Row 2: y=135~165 -->
  <rect x="295" y="135" width="40" height="30" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="0.5"/>
  <text x="315" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">6</text>
  <rect x="335" y="135" width="40" height="30" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.5"/>
  <text x="355" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">8</text>
  <rect x="375" y="135" width="40" height="30" fill="currentColor" fill-opacity="0.21" stroke="currentColor" stroke-width="0.5"/>
  <text x="395" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">11</text>
  <rect x="415" y="135" width="40" height="30" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="0.5"/>
  <text x="435" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">14</text>
  <rect x="455" y="135" width="40" height="30" fill="currentColor" fill-opacity="0.42" stroke="currentColor" stroke-width="0.5"/>
  <text x="475" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">18</text>
  <rect x="495" y="135" width="40" height="30" fill="currentColor" fill-opacity="0.50" stroke="currentColor" stroke-width="0.5"/>
  <text x="515" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">20</text>

  <!-- Row 3: y=165~195 -->
  <rect x="295" y="165" width="40" height="30" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.5"/>
  <text x="315" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">8</text>
  <rect x="335" y="165" width="40" height="30" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.5"/>
  <text x="355" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">10</text>
  <rect x="375" y="165" width="40" height="30" fill="currentColor" fill-opacity="0.27" stroke="currentColor" stroke-width="0.5"/>
  <text x="395" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">13</text>
  <rect x="415" y="165" width="40" height="30" fill="currentColor" fill-opacity="0.36" stroke="currentColor" stroke-width="0.5"/>
  <text x="435" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">16</text>
  <rect x="455" y="165" width="40" height="30" fill="currentColor" fill-opacity="0.45" stroke="currentColor" stroke-width="0.5"/>
  <text x="475" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">19</text>
  <rect x="495" y="165" width="40" height="30" fill="currentColor" fill-opacity="0.50" stroke="currentColor" stroke-width="0.5"/>
  <text x="515" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">20</text>

  <!-- 텍셀 라벨 (한 cell → 화살표 → "텍셀 1개") -->
  <line x1="375" y1="105" x2="365" y2="220" stroke="currentColor" stroke-width="0.5" opacity="0.6"/>
  <text x="365" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">텍셀 1개 = 한 점의 깊이 값</text>

  <!-- 하단 캡션 -->
  <text x="270" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">일반 사진은 RGB 색상을, Shadow Map은 깊이 값을 텍셀에 저장합니다</text>
  <text x="270" y="278" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">밝을수록 광원에서 가까움 / 어두울수록 멀리 있음</text>
</svg>
</div>

<br>

이 때, 깊이는 텍셀 단위로 끊어져 기록되어, 후속 단계에서 다룰 그림자의 경계 또한 텍셀 단위를 바탕으로 표현됩니다.

<br>

### 2단계: 카메라 시점에서 그림자 판별

이 단계에서는 GPU가 카메라 시점에서 장면을 렌더링하면서, 각 프래그먼트의 월드 위치를 1단계에서 사용한 광원 좌표계로 변환합니다. 이 변환 결과에는 두 가지 정보가 포함됩니다. Shadow Map에서 어느 텍셀을 조회할지 나타내는 위치와, 현재 프래그먼트가 광원 기준으로 얼마나 떨어져 있는지를 나타내는 깊이 값입니다.

GPU는 먼저 변환된 좌표로 Shadow Map의 텍셀을 찾고, 그 텍셀에 저장된 깊이 값을 읽습니다. 이 값은 1단계에서 기록된 값으로, 광원에서 보았을 때 해당 위치에 가장 먼저 나타난 표면의 깊이입니다.

마지막으로 GPU는 변환된 좌표에서 얻은 현재 프래그먼트의 깊이와 Shadow Map에서 읽은 깊이를 비교합니다.
현재 프래그먼트의 깊이가 더 크다면, 그보다 광원에 가까운 표면이 이미 앞에 있다는 뜻입니다. 즉, 광원에서 오는 빛이 그 표면에 가려져 현재 프래그먼트까지 직접 도달하지 못하므로, 해당 프래그먼트는 그림자 영역으로 판정됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">그림자 판별 (2단계)</text>
  <text x="280" y="40" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">광원에서 각 점 방향으로 빛을 쏘았을 때</text>

  <!-- Light source -->
  <circle cx="45" cy="110" r="14" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="45" cy="110" r="5" fill="currentColor" fill-opacity="0.7"/>
  <text x="45" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">광원</text>

  <!-- Path A: Light → 건물 (solid) → 점 A (dotted, blocked) -->
  <!-- Solid ray to 건물 -->
  <line x1="59" y1="103" x2="225" y2="78" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="225,74 215,76 217,84" fill="currentColor"/>
  <text x="140" y="82" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">점 A 방향</text>

  <!-- 건물 block -->
  <rect x="230" y="60" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>
  <text x="248" y="82" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">건물</text>
  <text x="248" y="55" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">거리 5</text>

  <!-- Blocked indicator -->
  <text x="285" y="76" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">가로막힘</text>

  <!-- Dotted continuation to 점 A -->
  <line x1="266" y1="78" x2="420" y2="66" stroke="currentColor" stroke-width="1" stroke-dasharray="3,4" opacity="0.4"/>
  <!-- 점 A -->
  <circle cx="430" cy="65" r="10" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="430" y="69" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">A</text>
  <text x="472" y="69" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">거리 15</text>

  <!-- Path B: Light → 점 B (direct, no obstacle) -->
  <line x1="59" y1="118" x2="420" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="424,161 412,157 414,167" fill="currentColor"/>
  <text x="200" y="152" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">점 B 방향</text>

  <!-- 점 B -->
  <circle cx="434" cy="162" r="10" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="434" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">B</text>
  <text x="472" y="166" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">거리 20</text>
  <text x="370" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">직접 도달</text>

  <!-- Divider -->
  <line x1="30" y1="200" x2="530" y2="200" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,3" opacity="0.3"/>

  <!-- Comparison formulas -->
  <rect x="30" y="212" width="240" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">점 A: Shadow Map 깊이 5, 실제 거리 15</text>
  <text x="150" y="250" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">15 > 5 → 그림자</text>

  <rect x="290" y="212" width="240" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="410" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">점 B: Shadow Map 깊이 20, 실제 거리 20</text>
  <text x="410" y="250" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">20 = 20 → 밝음</text>
</svg>
</div>

이 비교를 카메라가 렌더링하는 각 프래그먼트에서 수행하면, 장면의 어느 지점이 그림자에 속하는지 결정됩니다.

### Shadow Map 해상도와 품질

Shadow Map은 깊이 정보를 텍셀 단위로 저장하므로, 해상도가 그림자 경계의 선명도에 직접 영향을 줍니다.

해상도가 높으면 텍셀 하나가 담당하는 월드 공간 영역이 작아져 그림자 경계가 정밀해집니다. 반면 해상도가 낮으면 텍셀 하나가 넓은 영역을 대표하게 되어 그림자 경계에 **계단 현상(aliasing)**이 나타납니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Shadow Map 해상도에 따른 그림자 품질</text>

  <!-- Left: Low resolution (512x512) -->
  <text x="130" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">낮은 해상도 (512×512)</text>

  <!-- Jagged staircase edge - blocky steps -->
  <path d="M 60,70 L 60,90 L 75,90 L 75,110 L 90,110 L 90,130 L 105,130 L 105,150 L 120,150 L 120,170 L 135,170 L 135,190 L 200,190 L 200,70 Z"
        fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <!-- Highlight the staircase edge -->
  <path d="M 60,70 L 60,90 L 75,90 L 75,110 L 90,110 L 90,130 L 105,130 L 105,150 L 120,150 L 120,170 L 135,170 L 135,190"
        fill="none" stroke="currentColor" stroke-width="2.5"/>

  <text x="130" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 계단 현상(aliasing)</text>

  <!-- Divider -->
  <line x1="260" y1="55" x2="260" y2="225" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.3"/>

  <!-- Right: High resolution (2048x2048) -->
  <text x="390" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">높은 해상도 (2048×2048)</text>

  <!-- Smooth diagonal edge -->
  <path d="M 325,70 L 395,190 L 460,190 L 460,70 Z"
        fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <!-- Highlight the smooth edge -->
  <line x1="325" y1="70" x2="395" y2="190" stroke="currentColor" stroke-width="2.5"/>

  <text x="390" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 부드러운 경계</text>

  <!-- Bottom comparison note -->
  <text x="260" y="248" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">같은 그림자 경계를 다른 텍셀 밀도로 표현한 결과</text>
</svg>
</div>

그런데 해상도를 높이면 품질은 좋아지지만 메모리와 렌더링 비용도 함께 늘어납니다. 512×512 Shadow Map은 약 1MB, 2048×2048 Shadow Map은 약 16MB를 차지합니다. 가로·세로를 각각 4배 키우면 전체 텍셀 수가 16배가 되며, 광원 시점 렌더링이 처리할 픽셀 양(fillrate)도 그만큼 늘어납니다.

따라서 Shadow Map 해상도는 화면에서 그림자가 차지하는 비중과 목표 품질에 맞춰 정해야 합니다. 다만 하나의 Shadow Map이 카메라 시야 전체를 담당할 때는, 해상도를 올리는 것 외에 텍셀을 어떻게 배분할지도 함께 따져야 합니다. 이 배분 방식의 한계는 다음 섹션에서 다룹니다.

---

## Cascade Shadow Maps

**방향광(태양과 같은 평행광)**은 모든 빛이 같은 방향으로 평행하게 진행하므로, 광원 시점에 원근 개념이 없습니다. 이러한 **정사영(orthographic projection)** 시점에서 기록되는 Shadow Map은 월드 공간에 텍셀을 균등하게 분배합니다. 가령 1024×1024 Shadow Map이 가로 100m 영역을 담당한다면, 텍셀 하나는 위치와 무관하게 약 10cm × 10cm 영역을 표현합니다.

반면 카메라가 사람 눈처럼 **원근 투영(perspective projection)**을 사용하는 경우, 같은 크기의 표면이라도 가까이 있을수록 화면에서 더 큰 영역을 차지하며 그만큼 더 많은 픽셀로 표시됩니다. 그러나 그 표면이 Shadow Map에서 차지하는 텍셀 수는 카메라와의 거리와 무관하게 일정하므로, 가까울수록 화면 픽셀당 사용할 수 있는 텍셀 수가 줄어듭니다. 결국 단일 Shadow Map은 가까운 그림자에서 한 텍셀이 화면의 넓은 영역을 대표해야 하는 한계를 가지게 됩니다.

> **점 광원(Point Light)**과 **스폿 광원(Spot Light)**의 Shadow Map은 정사영 대신 원근 투영을 사용합니다. 점 광원은 빛이 360도로 퍼지므로 큐브맵의 6개 면에 각각 원근 투영으로 깊이를 기록하고, 스폿 광원은 원뿔 형태의 시야에 단일 원근 투영을 적용합니다. 이 경우 광원에 가까운 표면일수록 텍셀 밀도가 높아져, Cascade Shadow Maps이 전제하는 월드 공간 균등 분포와는 다릅니다.

이 한계는 카메라 가까이에 있는 표면에서 특히 두드러집니다. 예를 들어 카메라 5m 앞의 캐릭터가 화면에서는 수백 픽셀을 차지하더라도, 단일 Shadow Map에서는 그 영역에 배정된 텍셀이 충분하지 않을 수 있습니다. 이 경우 하나의 텍셀이 화면의 여러 픽셀을 대표하게 되어, 그림자 경계가 계단처럼 거칠게 보입니다.

반대로 멀리 있는 표면은 화면에서 작게 보이므로 같은 텍셀 밀도만으로도 품질 저하가 크게 드러나지 않습니다. 문제는 단일 Shadow Map의 해상도를 올리면 가까운 영역만 좋아지는 것이 아니라, 이미 충분한 먼 영역의 텍셀 수도 함께 늘어난다는 점입니다. 그만큼 메모리 사용량과 광원 시점 렌더링 비용도 함께 증가합니다.

결국 단일 Shadow Map은 가까운 곳에는 텍셀이 부족하고, 먼 곳에는 텍셀이 남는 구조적 불균형을 갖게 됩니다.
<br>

**Cascade Shadow Maps**는 카메라가 보는 거리를 **여러 구간(Cascade)**으로 나누고, 구간마다 별도의 Shadow Map을 사용하는 기법입니다. 가까운 구간은 좁은 범위를 높은 텍셀 밀도로 기록하고, 먼 구간은 넓은 범위를 낮은 텍셀 밀도로 기록해 단일 Shadow Map의 배분 불균형을 줄입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">단일 Shadow Map vs Cascade Shadow Maps</text>
  <text x="300" y="40" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">같은 텍셀 수를 거리에 따라 어떻게 분배하는가</text>

  <!-- ===== TOP: 단일 Shadow Map ===== -->
  <text x="300" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">단일 Shadow Map</text>

  <circle cx="40" cy="100" r="10" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="40" cy="100" r="4" fill="currentColor" fill-opacity="0.7"/>
  <text x="40" y="125" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">카메라</text>

  <rect x="70" y="80" width="470" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="305" y="73" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">Shadow Atlas (균일 분배)</text>

  <g fill="currentColor" fill-opacity="0.7">
    <circle cx="82" cy="100" r="2"/><circle cx="102" cy="100" r="2"/><circle cx="122" cy="100" r="2"/><circle cx="142" cy="100" r="2"/>
    <circle cx="162" cy="100" r="2"/><circle cx="182" cy="100" r="2"/><circle cx="202" cy="100" r="2"/><circle cx="222" cy="100" r="2"/>
    <circle cx="242" cy="100" r="2"/><circle cx="262" cy="100" r="2"/><circle cx="282" cy="100" r="2"/><circle cx="302" cy="100" r="2"/>
    <circle cx="322" cy="100" r="2"/><circle cx="342" cy="100" r="2"/><circle cx="362" cy="100" r="2"/><circle cx="382" cy="100" r="2"/>
    <circle cx="402" cy="100" r="2"/><circle cx="422" cy="100" r="2"/><circle cx="442" cy="100" r="2"/><circle cx="462" cy="100" r="2"/>
    <circle cx="482" cy="100" r="2"/><circle cx="502" cy="100" r="2"/><circle cx="522" cy="100" r="2"/>
  </g>

  <line x1="70" y1="140" x2="540" y2="140" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="540,140 532,137 532,143" fill="currentColor" opacity="0.5"/>
  <text x="75" y="155" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">가까운 곳</text>
  <text x="535" y="155" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">먼 곳</text>

  <text x="300" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">→ 가까운 곳에 텍셀 부족, 먼 곳에 텍셀 잉여</text>

  <!-- Divider -->
  <line x1="50" y1="200" x2="550" y2="200" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.3"/>

  <!-- ===== BOTTOM: Cascade Shadow Maps ===== -->
  <text x="300" y="225" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Cascade Shadow Maps</text>

  <circle cx="40" cy="260" r="10" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="40" cy="260" r="4" fill="currentColor" fill-opacity="0.7"/>
  <text x="40" y="285" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">카메라</text>

  <text x="100" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">Cascade 0</text>
  <rect x="70" y="240" width="60" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1.5"/>

  <text x="180" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">Cascade 1</text>
  <rect x="130" y="240" width="100" height="40" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>

  <text x="300" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">Cascade 2</text>
  <rect x="230" y="240" width="140" height="40" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>

  <text x="455" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">Cascade 3</text>
  <rect x="370" y="240" width="170" height="40" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.5"/>

  <g fill="currentColor" fill-opacity="0.7">
    <!-- Cascade 0: 6 dots, 가장 dense -->
    <circle cx="75" cy="260" r="2"/><circle cx="85" cy="260" r="2"/><circle cx="95" cy="260" r="2"/>
    <circle cx="105" cy="260" r="2"/><circle cx="115" cy="260" r="2"/><circle cx="125" cy="260" r="2"/>
    <!-- Cascade 1: 6 dots -->
    <circle cx="138" cy="260" r="2"/><circle cx="155" cy="260" r="2"/><circle cx="172" cy="260" r="2"/>
    <circle cx="189" cy="260" r="2"/><circle cx="206" cy="260" r="2"/><circle cx="223" cy="260" r="2"/>
    <!-- Cascade 2: 6 dots -->
    <circle cx="240" cy="260" r="2"/><circle cx="263" cy="260" r="2"/><circle cx="286" cy="260" r="2"/>
    <circle cx="309" cy="260" r="2"/><circle cx="332" cy="260" r="2"/><circle cx="355" cy="260" r="2"/>
    <!-- Cascade 3: 6 dots, 가장 sparse -->
    <circle cx="380" cy="260" r="2"/><circle cx="408" cy="260" r="2"/><circle cx="436" cy="260" r="2"/>
    <circle cx="464" cy="260" r="2"/><circle cx="492" cy="260" r="2"/><circle cx="520" cy="260" r="2"/>
  </g>

  <line x1="70" y1="300" x2="540" y2="300" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="540,300 532,297 532,303" fill="currentColor" opacity="0.5"/>
  <text x="75" y="315" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">가까운 곳</text>
  <text x="535" y="315" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">먼 곳</text>

  <text x="300" y="340" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">→ 각 cascade 동일 텍셀 수를 다른 영역에 분배, 가까운 곳에 밀도 집중</text>
</svg>
</div>

<br>

각 캐스케이드에 같은 해상도의 Shadow Map을 할당하더라도, 그 Shadow Map이 담는 월드 공간의 범위는 서로 다릅니다. 가까운 캐스케이드는 카메라 근처의 좁은 영역을 담고, 먼 캐스케이드는 더 넓은 영역을 담습니다. 따라서 같은 1024×1024 해상도라도 가까운 구간에서는 텍셀 하나가 더 작은 월드 공간을 담당하고, 먼 구간에서는 더 넓은 월드 공간을 담당합니다.

가까운 그림자는 화면에서 크게 보이므로 작은 그림자 변화도 쉽게 드러납니다. 이 구간에는 높은 텍셀 밀도가 필요합니다. 반대로 먼 그림자는 화면에서 작게 보이므로, 텍셀 하나가 더 넓은 영역을 담당해도 품질 저하가 상대적으로 덜 눈에 띕니다.

Cascade Shadow Maps는 이 차이를 이용해 가까운 구간에는 높은 텍셀 밀도를 주고, 먼 구간에는 낮은 텍셀 밀도를 허용함으로써 제한된 Shadow Map 해상도를 더 효율적으로 사용합니다.

### 캐스케이드 수와 비용

캐스케이드 수를 늘리면 거리별 텍셀 밀도를 더 세밀하게 배분할 수 있습니다. 대신 각 캐스케이드가 담당하는 구간의 Shadow Map을 만들기 위해, 그림자를 생성하는 오브젝트를 광원 시점에서 다시 렌더링해야 합니다. 
따라서 캐스케이드 수가 늘수록 Shadow Map 패스의 드로우콜과 정점 처리 비용도 증가합니다.

다만 비용이 항상 캐스케이드 수에 정확히 비례하는 것은 아닙니다.
각 캐스케이드는 서로 다른 거리 구간을 담당하므로, 그 구간 안에 들어오는 그림자 생성 오브젝트도 서로 다릅니다.
예를 들어 가까운 캐스케이드에는 캐릭터와 주변 소품만 포함될 수 있고, 먼 캐스케이드에는 건물이나 지형처럼 더 큰 오브젝트가 포함될 수 있습니다. 엔진은 각 구간에 들어오지 않는 오브젝트를 제외하고 Shadow Map을 렌더링하므로, 캐스케이드 하나가 추가된다고 항상 같은 양의 렌더링 비용이 더해지는 것은 아닙니다.
이 차이를 고려하더라도, 캐스케이드 수가 많을수록 Shadow Map을 만들어야 하는 구간이 늘어나므로 전체 그림자 비용은 대체로 증가합니다.

<br>
**캐스케이드 수에 따른 비용**

| 캐스케이드 수 | Shadow Map 구간 | 비용 경향 | 품질 특성 |
|--------------|------------------|----------|-----------|
| 1개 | 1개 | 낮음 | 전체 Shadow Distance에 같은 텍셀 밀도 사용 |
| 2개 | 2개 | 중간 | 가까운 구간에 더 많은 텍셀 밀도 배분 |
| 4개 | 4개 | 높음 | 가까운 곳부터 먼 곳까지 단계적으로 품질 조절 |

<br>

성능 예산이 제한된 프로젝트에서는 **1~2개 캐스케이드**를 기준으로 시작하는 편이 현실적입니다.

Shadow Distance를 짧게 잡으면 같은 해상도를 더 좁은 범위에 사용할 수 있으므로, 캐스케이드 수가 적어도 가까운 그림자 품질을 확보하기 쉽습니다. 반대로 넓은 야외 장면처럼 먼 거리 그림자까지 중요하다면 4개 캐스케이드를 사용할 수 있지만, 그만큼 그림자 예산을 더 확보해야 합니다.

---

## Shadow Distance

**Shadow Distance**는 카메라로부터 어느 거리까지 실시간 그림자를 계산할지를 정하는 값입니다. 이 거리보다 먼 오브젝트는 실시간 Shadow Map 생성 대상에서 제외됩니다.

Shadow Distance를 어떻게 설정하느냐에 따라 Shadow Map의 텍셀 밀도와 렌더링 비용이 함께 달라집니다. Shadow Distance가 길면 Shadow Map이 카메라에서 먼 영역까지 포함해야 하므로, 같은 해상도를 더 넓은 범위에 나누어 사용하게 됩니다. 그만큼 텍셀 밀도가 낮아져 가까운 그림자 경계도 거칠게 보일 수 있습니다.

반대로 Shadow Distance를 줄이면 Shadow Map이 카메라 주변의 좁은 범위에 집중됩니다. 같은 해상도를 더 가까운 영역에 사용할 수 있으므로 그림자 경계를 더 선명하게 표현하기 쉽고, 먼 오브젝트가 Shadow Map 패스에서 제외되어 렌더링 비용도 줄어듭니다.

대부분의 장면에서는 카메라 주변의 그림자가 가장 눈에 잘 띄고, 멀리 있는 그림자는 작게 보이거나 다른 디테일에 묻혀 품질 차이가 덜 드러납니다. 따라서 Shadow Distance는 가능한 한 길게 두기보다, 실제 시야 거리와 플레이어가 주목하는 범위에 맞춰 제한하는 편이 효율적입니다.

---

## 저비용 그림자 대안

Shadow Map 기반 그림자는 오브젝트의 형태를 반영한 실시간 그림자를 만들 수 있지만, 광원 시점에서 장면을 추가로 렌더링해야 하므로 비용이 큽니다. 따라서 모든 오브젝트에 같은 방식의 실시간 그림자를 적용하기보다, 대상의 중요도와 화면에서의 비중에 따라 더 가벼운 표현을 함께 사용하는 편이 효율적입니다.

### Blob Shadow

**Blob Shadow**는 실제 그림자를 계산하지 않고, 오브젝트의 발밑이나 접촉 지점 주변에 흐릿한 원형 또는 타원형 텍스처를 배치하는 기법입니다. 광원 시점에서 깊이를 기록하거나 비교하지 않으므로 Shadow Map이 필요하지 않습니다. 비용은 보통 어두운 텍스처가 입혀진 작은 쿼드(quad, 사각형 폴리곤) 하나를 그리는 정도에 가깝습니다.

대신 Blob Shadow는 오브젝트의 실제 실루엣이나 광원 방향을 반영하지 못합니다. 캐릭터가 팔을 벌리거나 무기를 들어도 그림자는 거의 같은 타원형으로 남고, 광원 방향이 바뀌어도 실제 그림자처럼 길어지거나 한쪽으로 늘어나지 않습니다. 바닥이 크게 기울어져 있거나 높이가 다른 표면이 겹치는 장면에서도 자연스럽게 맞지 않을 수 있습니다.

따라서 Blob Shadow는 정확한 그림자를 표현하는 용도보다, 오브젝트가 바닥에 붙어 있다는 접지감을 낮은 비용으로 전달하는 용도에 적합합니다. 많은 캐릭터나 소형 오브젝트를 동시에 렌더링해야 하는 장면, 또는 모바일·저품질 설정에서 실시간 그림자 비용을 크게 줄여야 하는 경우에 우선 고려할 수 있습니다.

### Projector / Decal

**Projector**(Built-in Render Pipeline) 또는 **Decal**(URP)은 어두운 텍스처를 특정 방향으로 투영해, 표면 위에 그림자처럼 보이는 패턴을 입히는 기법입니다.

예를 들어 캐릭터의 대략적인 윤곽이나 발밑 그림자 텍스처를 아래 방향으로 투영하면, 바닥 위에 단순한 원형보다 형태가 있는 그림자를 표현할 수 있습니다. 실제 Shadow Map처럼 오브젝트의 현재 자세와 광원 방향을 깊이 비교로 계산하는 것은 아니지만, Blob Shadow보다 표면에 붙는 느낌이나 형태를 더 조절하기 쉽습니다.

비용은 투영 범위가 닿는 표면의 면적과 픽셀 수에 따라 달라집니다. Blob Shadow는 보통 작은 쿼드 하나만 그리지만, Projector/Decal은 투영 볼륨 안에 들어온 바닥, 벽, 다른 오브젝트 표면까지 처리할 수 있습니다. 
따라서 투영 범위가 넓거나 여러 표면과 겹치면 처리할 픽셀이 늘어나고, 그림자 대안으로 쓰더라도 비용이 커질 수 있습니다.

### 베이크 그림자

건물, 지형, 고정된 소품처럼 움직이지 않는 정적 오브젝트의 그림자는 런타임에 매 프레임 다시 계산할 필요가 없습니다. [Part 1](/dev/unity/LightingAndShadows-1/)에서 다룬 라이트맵 베이킹을 사용하면, 정적 조명과 그림자 결과를 미리 계산해 라이트맵 텍스처에 저장할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">베이크 그림자</text>

  <!-- Section 1: 에디터 -->
  <rect x="20" y="40" width="480" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="60" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">에디터 (빌드 전)</text>

  <rect x="35" y="72" width="120" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="95" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">광원 위치/방향</text>
  <text x="95" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">정적 오브젝트 대상</text>

  <line x1="158" y1="93" x2="195" y2="93" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,93 187,88 187,98" fill="currentColor"/>

  <rect x="198" y="72" width="120" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="258" y="97" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">그림자 계산</text>

  <line x1="321" y1="93" x2="358" y2="93" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="358,93 350,88 350,98" fill="currentColor"/>

  <rect x="361" y="72" width="128" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="425" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">라이트맵 텍스처</text>
  <text x="425" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">에 기록</text>

  <!-- Section 2: 런타임 -->
  <rect x="20" y="145" width="480" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="165" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">런타임</text>

  <rect x="35" y="177" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="100" y="199" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">라이트맵 → 표면</text>

  <line x1="168" y1="195" x2="205" y2="195" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="205,195 197,190 197,200" fill="currentColor"/>

  <rect x="208" y="177" width="150" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="283" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">실시간 계산 없이</text>
  <text x="283" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">그림자 표현</text>

  <text x="400" y="199" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">비용: 텍스처 샘플링 1회</text>

  <!-- Section 3: 제약 (dashed border) -->
  <rect x="20" y="240" width="480" height="88" rx="5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="40" y="262" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">제약</text>

  <circle cx="45" cy="283" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="58" y="287" font-family="sans-serif" font-size="10" fill="currentColor">오브젝트가 움직이면 그림자가 따라가지 않음</text>

  <circle cx="45" cy="308" r="4" fill="currentColor" fill-opacity="0.3"/>
  <text x="58" y="312" font-family="sans-serif" font-size="10" fill="currentColor">광원이 바뀌어도 그림자가 갱신되지 않음</text>
</svg>
</div>

베이킹은 런타임이 아니라 에디터에서 미리 수행되므로, 실시간 프레임 예산에 맞추지 않고 더 많은 계산 시간을 사용할 수 있습니다. 런타임에는 이미 계산된 결과를 라이트맵에서 샘플링하기만 하므로, 정적 오브젝트의 그림자 비용을 크게 줄일 수 있습니다.

대신 베이크된 그림자는 텍스처에 고정된 결과입니다. 오브젝트가 이동하거나 광원 방향이 바뀌면, 라이트맵에 저장된 그림자와 실제 장면 상태가 어긋납니다. 이런 변화는 라이트맵이 자동으로 갱신하지 못하므로, 동적 오브젝트나 시간에 따라 변하는 조명에는 별도의 실시간 그림자 전략이 필요합니다.

### 하이브리드 접근

그림자 표현은 하나의 방식만으로 처리하기보다, 대상의 성격과 중요도에 따라 나누어 적용하는 편이 효율적입니다.
정적 배경은 베이크 그림자로 처리하고, 플레이어 주변의 중요한 동적 오브젝트에는 실시간 Shadow Map을 사용하며, 멀리 있거나 중요도가 낮은 오브젝트에는 Blob Shadow나 Projector/Decal처럼 가벼운 표현을 사용할 수 있습니다.

이처럼 여러 그림자 방식을 함께 사용하는 전략을 **하이브리드 접근**이라고 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Title -->
  <text x="250" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">하이브리드 그림자 전략</text>

  <!-- Outer container -->
  <rect x="15" y="38" width="470" height="210" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>

  <!-- Header row labels -->
  <text x="110" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">대상</text>
  <text x="300" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">기법</text>
  <text x="445" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">비용</text>

  <line x1="25" y1="65" x2="475" y2="65" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Row 1: 배경 -->
  <rect x="25" y="72" width="460" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="93" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">배경</text>
  <text x="110" y="108" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">정적 오브젝트</text>
  <text x="300" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">베이크 그림자 (라이트맵)</text>
  <text x="445" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">없음</text>

  <!-- Row 2: 캐릭터 -->
  <rect x="25" y="130" width="460" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="151" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐릭터</text>
  <text x="110" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">동적 오브젝트</text>
  <text x="300" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">실시간 Shadow Map (캐스케이드 1~2개)</text>
  <text x="300" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">또는 Blob Shadow / Projector</text>
  <text x="445" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">중간</text>

  <!-- Row 3: 기타 소품 -->
  <rect x="25" y="188" width="460" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="209" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">기타 소품</text>
  <text x="110" y="224" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">동적 소품</text>
  <text x="300" y="216" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Blob Shadow 또는 그림자 없음</text>
  <text x="445" y="216" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">낮음</text>

  <!-- Summary note -->
  <rect x="30" y="260" width="440" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="250" y="277" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">배경은 베이크로 품질 확보, 캐릭터만 실시간 처리</text>
  <text x="250" y="292" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">→ 전체 비용 억제 + 시각적 완성도 유지</text>
</svg>
</div>

<br>

배경의 건물, 지형, 나무처럼 움직이지 않는 오브젝트의 그림자는 라이트맵이나 Shadowmask로 베이크합니다. 
플레이어 주변의 중요한 동적 오브젝트에는 실시간 Shadow Map을 사용하되, 캐스케이드 수와 Shadow Distance는 필요한 범위 안에서만 유지합니다. 더 낮은 품질 설정에서는 동적 오브젝트의 실시간 그림자도 Blob Shadow나 Projector/Decal로 대체할 수 있습니다.

---

## Shadow Map의 추가 비용

실시간 Shadow Map을 사용하면 그림자의 형태를 오브젝트에 맞게 표현할 수 있지만, 메인 카메라 렌더링 외에 별도의 작업이 추가됩니다.

먼저 Shadow Map을 만들기 위해 그림자를 생성하는 오브젝트를 광원 시점에서 다시 렌더링해야 합니다.
이 과정에서 오브젝트별 드로우콜, 버텍스 셰이더 실행, 래스터화와 깊이 기록 비용이 추가됩니다. 캐스케이드를 사용하면 이 렌더링이 거리 구간별로 나뉘어 수행되므로, 처리해야 하는 구간 수와 각 구간에 들어오는 오브젝트 수가 비용을 좌우합니다.

렌더링이 끝난 Shadow Map은 깊이 텍스처로 GPU 메모리에 저장됩니다. 해상도가 높거나 캐스케이드 수가 많을수록 필요한 메모리도 늘어납니다.

이후 메인 카메라 렌더링에서는 프래그먼트마다 그림자 여부를 판정하기 위해 이 Shadow Map을 조회합니다. 그림자를 받는 화면 영역이 넓을수록 Shadow Map 샘플링도 더 많이 발생하므로, 메인 패스의 텍스처 조회 비용도 함께 증가합니다.

타일 기반 GPU에서는 렌더 타깃 전환 비용도 고려해야 합니다. Shadow Map은 광원 시점의 깊이를 기록하는 렌더 타깃이고, 메인 카메라는 카메라 시점의 색상을 기록하는 렌더 타깃입니다. 이 둘 사이를 전환할 때 타일 메모리의 내용을 저장하거나 다시 읽어야 할 수 있으므로, 메모리 대역폭이 제한된 환경에서는 추가 부담이 됩니다.

> 타일 기반 GPU의 Store/Load 구조는 [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.

따라서 모든 오브젝트가 실시간 그림자를 생성할 필요는 없습니다. 작은 소품이나 먼 곳의 오브젝트처럼 그림자가 화면에서 잘 드러나지 않는 대상은 Shadow Map 패스에서 제외하는 편이 효율적입니다. Unity에서는 MeshRenderer의 **Cast Shadows**를 Off로 설정해 해당 오브젝트가 Shadow Map 생성에 참여하지 않도록 할 수 있습니다.

---

## 포스트 프로세싱(Post Processing)의 구조

3D 장면 렌더링이 끝나면 카메라가 본 장면의 색상 결과가 화면 해상도의 텍스처에 저장됩니다. 이 텍스처를 렌더 타깃 또는 프레임버퍼라고 부르며, 각 픽셀에는 화면에 표시할 색상 값이 들어 있습니다.

**포스트 프로세싱(Post Processing)**은 이 렌더링 결과를 입력으로 받아 화면 전체에 후처리 연산을 적용하는 단계입니다. Bloom은 밝은 영역을 번지게 만들고, Color Grading은 색감을 조정하며, Tone Mapping은 HDR 밝기를 화면에 표시 가능한 범위로 변환합니다.

이 시점에는 메쉬, 정점, 변환 행렬 같은 지오메트리 정보가 이미 픽셀 색상으로 변환된 뒤입니다. 따라서 포스트 프로세싱은 장면을 다시 그리거나 조명을 다시 계산하는 작업이 아니라, 이미 만들어진 화면 이미지를 처리하는 2D 이미지 처리에 가깝습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Title -->
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">포스트 프로세싱의 위치</text>

  <!-- Left section: 3D 장면 렌더링 -->
  <rect x="15" y="42" width="230" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3D 장면 렌더링</text>

  <!-- Flow: 메쉬 → 셰이딩 → 프레임버퍼 -->
  <rect x="30" y="78" width="60" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="60" y="98" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">메쉬</text>

  <line x1="93" y1="94" x2="113" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="113,94 107,89 107,99" fill="currentColor"/>

  <rect x="116" y="78" width="60" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="146" y="98" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이딩</text>

  <line x1="146" y1="110" x2="146" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="146,128 141,122 151,122" fill="currentColor"/>

  <rect x="85" y="130" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="145" y="147" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프레임버퍼</text>
  <text x="145" y="161" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(2D 이미지)</text>

  <!-- Arrow from left to right section -->
  <line x1="248" y1="130" x2="285" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,130 277,125 277,135" fill="currentColor"/>

  <!-- Right section: 포스트 프로세싱 -->
  <rect x="288" y="42" width="275" height="150" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="425" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">포스트 프로세싱</text>

  <!-- Effect chain -->
  <rect x="305" y="78" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="355" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Bloom</text>

  <rect x="305" y="110" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="355" y="128" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Color Grading</text>

  <rect x="305" y="142" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="355" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Tone Mapping</text>

  <text x="355" y="180" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Vignette ...</text>

  <!-- Arrow to 최종 화면 -->
  <line x1="410" y1="130" x2="440" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="440,130 434,125 434,135" fill="currentColor"/>

  <rect x="443" y="100" width="105" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="496" y="128" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">최종 화면</text>
  <text x="496" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">출력</text>

  <!-- Bottom labels -->
  <text x="130" y="215" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">3D 오브젝트 처리</text>
  <text x="425" y="215" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">2D 이미지 처리</text>

  <!-- Divider line between labels -->
  <line x1="255" y1="200" x2="255" y2="222" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
</svg>
</div>

<br>

포스트 프로세싱의 비용은 장면 자체의 복잡도보다, 렌더링이 끝난 화면 이미지를 얼마나 넓은 범위로 처리하느냐에 더 크게 좌우됩니다. 일반적인 전체 화면 효과는 화면에 보이는 모든 픽셀을 한 번씩 읽고, 효과가 적용된 새 색상을 계산합니다.

따라서 포스트 프로세싱에서는 **필레이트(Fill Rate)** 와 메모리 대역폭이 중요해집니다. 해상도가 높을수록 처리해야 할 픽셀 수가 늘고, 여러 패스로 나뉜 효과일수록 같은 화면 이미지를 반복해서 읽고 써야 합니다.

예를 들어 1920×1080 화면에는 약 207만 개의 픽셀이 있습니다. 전체 화면 포스트 프로세싱을 한 패스 적용하면, 이 픽셀 수만큼 포스트 프로세싱 셰이더가 실행됩니다.

만약 효과가 세 개의 패스로 구성되어 있다면 화면 전체를 세 번 처리하게 됩니다. 이때 각 패스에서 원본 색상, 깊이 텍스처, 블러 텍스처 등을 몇 번 읽는지에 따라 실제 비용이 달라집니다.

---

## 포스트 프로세싱 효과별 비용

포스트 프로세싱은 대부분 화면 전체를 대상으로 하지만, 모든 효과의 비용이 같은 것은 아닙니다. 어떤 효과는 픽셀당 간단한 연산 한두 번으로 끝나고, 어떤 효과는 여러 텍스처를 반복해서 읽거나 화면을 여러 번 처리해야 합니다.

따라서 효과별 비용은 주로 픽셀당 연산량, 텍스처 샘플링 횟수, 패스 수에 따라 달라집니다.

### 저비용 효과

**Color Grading(색 보정)**은 화면의 색상을 의도한 톤으로 변환하는 효과입니다. 보통 **LUT(Look-Up Table)** 에 입력 색상과 출력 색상의 대응 관계를 미리 저장해 두고, 런타임에는 현재 픽셀 색상으로 LUT를 조회해 보정된 색상을 얻습니다. 복잡한 색 변환을 매번 수식으로 계산하지 않아도 되므로, 대체로 픽셀당 적은 수의 텍스처 샘플링으로 처리할 수 있습니다.

<br>

**Vignette(비네트)**는 화면 가장자리로 갈수록 이미지를 어둡게 만드는 효과입니다. 각 픽셀의 화면상 위치가 중심에서 얼마나 떨어져 있는지 계산하고, 그 거리에 따라 원래 색상에 어두운 계수를 곱합니다. 추가 텍스처를 여러 번 읽지 않고 간단한 산술 연산으로 처리할 수 있어 비교적 가벼운 편입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">저비용 포스트 프로세싱</text>
  <!-- Divider line -->
  <line x1="260" y1="38" x2="260" y2="250" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <!-- Left column: Color Grading -->
  <text x="130" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Color Grading</text>
  <!-- Step 1: Input -->
  <rect x="30" y="62" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">입력 픽셀 색상</text>
  <text x="130" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">(R, G, B)</text>
  <!-- Arrow -->
  <line x1="130" y1="98" x2="130" y2="118" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="130,122 126,114 134,114" fill="currentColor"/>
  <!-- Step 2: LUT -->
  <rect x="30" y="124" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">LUT 텍스처에서 대응 색상 참조</text>
  <text x="130" y="152" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.6" fill="currentColor">(텍스처 샘플링 1회)</text>
  <!-- Arrow -->
  <line x1="130" y1="160" x2="130" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="130,184 126,176 134,176" fill="currentColor"/>
  <!-- Step 3: Output -->
  <rect x="30" y="186" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">출력 픽셀 색상</text>
  <text x="130" y="214" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">(R', G', B')</text>
  <!-- Bottom note -->
  <text x="130" y="242" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.5" fill="currentColor">텍스처 샘플링 1회</text>
  <!-- Right column: Vignette -->
  <text x="390" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Vignette</text>
  <!-- Step 1: Distance -->
  <rect x="290" y="62" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">화면 중앙에서의 거리 d 계산</text>
  <!-- Arrow -->
  <line x1="390" y1="92" x2="390" y2="112" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="390,116 386,108 394,108" fill="currentColor"/>
  <!-- Step 2: Brightness formula -->
  <rect x="290" y="118" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">밝기 = 1.0 - (d / 최대거리)^강도</text>
  <!-- Arrow -->
  <line x1="390" y1="148" x2="390" y2="168" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="390,172 386,164 394,164" fill="currentColor"/>
  <!-- Step 3: Output -->
  <rect x="290" y="174" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="194" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">출력 = 원래 색상 × 밝기</text>
  <!-- Bottom note -->
  <text x="390" y="228" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.5" fill="currentColor">텍스처 샘플링 없음, 수학 연산만</text>
</svg>
</div>

### 중비용 효과

**Bloom**은 화면의 밝은 영역이 주변으로 번져 보이게 만드는 효과입니다. 먼저 밝기 기준을 넘는 픽셀만 추출하고, 이 결과를 여러 단계의 낮은 해상도 텍스처로 **다운샘플**합니다. 이후 각 단계에서 [가우시안 블러](/dev/graphics/GaussianBlur/) 같은 블러를 적용해 빛이 퍼지는 형태를 만듭니다.

Bloom이 중비용 효과로 분류되는 이유는 한 번의 전체 화면 패스로 끝나지 않기 때문입니다. 밝은 영역 추출, 다운샘플, 블러, 업샘플, 원본 이미지와의 합성처럼 여러 단계가 필요하고, 단계마다 중간 텍스처를 읽고 써야 합니다.

대신 블러의 많은 부분은 원본보다 낮은 해상도에서 수행됩니다. 해상도가 낮아지면 처리할 픽셀 수가 줄고, 낮은 해상도에서 만든 블러는 원본 해상도로 다시 합성될 때 더 넓은 번짐처럼 보입니다. 그래서 Bloom은 여러 패스를 사용하지만, 전체 해상도에서 큰 블러를 직접 계산하는 방식보다 효율적으로 처리할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Bloom 처리 과정</text>
  <!-- Step 1: Original image -->
  <rect x="140" y="38" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">원본 이미지 (1920×1080)</text>
  <!-- Arrow -->
  <line x1="240" y1="68" x2="240" y2="86" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,90 236,82 244,82" fill="currentColor"/>
  <!-- Step 2: Threshold -->
  <rect x="140" y="92" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">밝은 픽셀 추출 (Threshold)</text>
  <!-- Arrow -->
  <line x1="240" y1="122" x2="240" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,144 236,136 244,136" fill="currentColor"/>
  <!-- Downsample section label -->
  <text x="240" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">다운샘플 (해상도를 절반씩 줄이며 블러)</text>
  <!-- Downsample boxes: decreasing width -->
  <rect x="90" y="170" width="160" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">960×540</text>
  <line x1="250" y1="183" x2="268" y2="183" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="272,183 264,179 264,187" fill="currentColor"/>
  <rect x="275" y="173" width="120" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="335" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">480×270</text>
  <!-- Second row of downsample -->
  <line x1="335" y1="193" x2="335" y2="207" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="335,211 331,203 339,203" fill="currentColor"/>
  <rect x="275" y="214" width="100" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="229" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">240×135</text>
  <line x1="270" y1="224" x2="252" y2="224" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="248,224 256,220 256,228" fill="currentColor"/>
  <rect x="168" y="214" width="80" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="208" y="229" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">120×67</text>
  <!-- Arrow down to upsample -->
  <line x1="208" y1="234" x2="208" y2="260" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="208,264 204,256 212,256" fill="currentColor"/>
  <!-- Upsample section label -->
  <text x="240" y="280" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">업샘플 (다시 확대하며 합성)</text>
  <!-- Upsample boxes: increasing width -->
  <rect x="168" y="290" width="80" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="208" y="305" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">120×67</text>
  <line x1="248" y1="300" x2="266" y2="300" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="270,300 262,296 262,304" fill="currentColor"/>
  <rect x="273" y="290" width="100" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="323" y="305" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">240×135</text>
  <!-- Second row of upsample -->
  <line x1="323" y1="310" x2="323" y2="324" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="323,328 319,320 327,320" fill="currentColor"/>
  <rect x="263" y="331" width="120" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="323" y="346" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">480×270</text>
  <line x1="258" y1="341" x2="240" y2="341" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="236,341 244,337 244,345" fill="currentColor"/>
  <rect x="76" y="331" width="160" height="20" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="156" y="346" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">960×540</text>
  <!-- Arrow to final -->
  <line x1="240" y1="351" x2="240" y2="373" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,377 236,369 244,369" fill="currentColor"/>
  <!-- Final: Composite -->
  <rect x="120" y="379" width="240" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="399" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">원본과 합성 → 최종 이미지</text>
  <!-- Bottom notes -->
  <rect x="80" y="428" width="320" height="70" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="240" y="450" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.6" fill="currentColor">텍스처 샘플링: 다운샘플 + 업샘플 단계마다 다수 발생</text>
  <text x="240" y="466" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.6" fill="currentColor">렌더 타깃 전환: 단계마다 해상도가 다른 텍스처 사용</text>
  <text x="240" y="486" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">비용: 중간</text>
</svg>
</div>

Bloom의 비용은 중간 텍스처를 몇 단계까지 만들고, 각 단계에서 텍스처를 몇 번 샘플링하느냐에 따라 달라집니다. 다운샘플과 업샘플 단계에서는 이전 단계의 텍스처를 읽고, 다른 해상도의 렌더 타깃에 결과를 기록합니다.

이 과정에서는 렌더 타깃 전환도 반복됩니다. 타일 기반 GPU에서는 렌더 타깃이 바뀔 때마다 현재 타일의 결과를 메인 메모리에 기록(Store)하거나, 새 렌더 타깃의 내용을 다시 읽어와야(Load) 할 수 있습니다.

따라서 Bloom은 블러 연산 자체뿐 아니라 중간 텍스처와 렌더 타깃 전환 비용도 함께 고려해야 합니다. 다만 대부분의 블러가 다운샘플된 저해상도에서 수행되므로, 넓은 번짐 효과를 전체 해상도에서 직접 계산하는 것보다는 비용을 낮출 수 있습니다.

<br>

**Tone Mapping**은 HDR 렌더링 결과의 밝기 범위를 디스플레이가 표현할 수 있는 범위로 변환하는 과정입니다.

HDR에서는 픽셀의 밝기 값이 1.0을 넘을 수 있습니다. 예를 들어 태양은 10.0, 하늘은 3.0, 전등은 1.5처럼 서로 다른 밝기 차이를 큰 범위 안에 저장할 수 있습니다. 하지만 일반적인 화면 출력은 마지막에 0~1 범위로 정리되어야 합니다.

만약 HDR 값을 Tone Mapping 없이 그대로 출력하면 1.0을 넘는 값이 모두 최대 밝기로 잘립니다. 태양, 하늘, 전등이 모두 흰색으로 뭉개져 보이고, 원래 갖고 있던 밝기 차이가 사라집니다.

Tone Mapping은 넓은 밝기 범위를 0~1로 압축하면서도, 밝기의 상대적인 차이가 남도록 곡선을 적용합니다. ACES, Filmic 같은 방식은 이 압축 곡선을 정의하는 방법이며, 어두운 영역과 밝은 영역을 보존하는 방식이 서로 다릅니다.

Tone Mapping 자체는 보통 픽셀당 수학 연산으로 처리되므로 단독 비용은 낮은 편입니다. 다만 실제 포스트 프로세싱 체인에서는 Color Grading, 노출 보정, 감마 변환 같은 단계와 함께 실행되는 경우가 많습니다. 이 경우 픽셀마다 LUT 샘플링과 수학 연산이 함께 수행되므로, 단독 Tone Mapping보다 비용이 늘어 저~중비용으로 보는 편이 적절합니다.

### 고비용 효과

**SSAO(Screen Space Ambient Occlusion)**는 접촉부, 구석, 틈새처럼 빛이 잘 들어가기 어려운 부분에 어두운 음영을 더하는 효과입니다. 화면에 저장된 깊이 값을 바탕으로 각 픽셀 주변을 여러 번 샘플링하고, 주변 지오메트리가 얼마나 가까이 둘러싸고 있는지를 근사합니다.

SSAO가 비싼 이유는 이 계산이 화면의 많은 픽셀에서 반복되기 때문입니다. 한 픽셀의 음영을 정하려면 현재 깊이뿐 아니라 주변 여러 지점의 깊이를 읽어야 하고, 샘플 수가 늘수록 텍스처 조회 횟수도 그대로 증가합니다. 여기에 노이즈를 줄이기 위한 블러 패스가 추가되는 경우도 많습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- Title -->
  <text x="230" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SSAO의 비용 구조</text>
  <!-- Subtitle -->
  <text x="230" y="44" text-anchor="middle" font-family="sans-serif" font-size="10" opacity="0.6" fill="currentColor">각 픽셀에 대해:</text>
  <!-- Step 1 -->
  <rect x="50" y="56" width="360" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="75" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">(1) 깊이 버퍼에서 현재 픽셀의 깊이 읽기</text>
  <!-- Arrow -->
  <line x1="230" y1="84" x2="230" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,100 226,92 234,92" fill="currentColor"/>
  <!-- Step 2 -->
  <rect x="50" y="102" width="360" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="121" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">(2) 주변 N개 방향으로 샘플 포인트 생성 (N = 8~32)</text>
  <!-- Arrow -->
  <line x1="230" y1="130" x2="230" y2="142" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,146 226,138 234,138" fill="currentColor"/>
  <!-- Step 3 -->
  <rect x="50" y="148" width="360" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="167" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">(3) 각 샘플 포인트의 깊이를 깊이 버퍼에서 읽기</text>
  <!-- Arrow -->
  <line x1="230" y1="176" x2="230" y2="188" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,192 226,184 234,184" fill="currentColor"/>
  <!-- Step 4 -->
  <rect x="50" y="194" width="360" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="213" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">(4) 각 샘플의 깊이를 비교하여 가려진 정도 계산</text>
  <!-- Arrow -->
  <line x1="230" y1="222" x2="230" y2="234" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,238 226,230 234,230" fill="currentColor"/>
  <!-- Step 5 -->
  <rect x="50" y="240" width="360" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="259" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">(5) 결과를 블러하여 노이즈 제거</text>
  <!-- Sampling info box -->
  <rect x="60" y="288" width="340" height="46" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="230" y="308" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.6" fill="currentColor">픽셀당 텍스처 샘플링: N + 1회 (N = 샘플 수)</text>
  <text x="230" y="324" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.6" fill="currentColor">추가 블러 패스: 1~2회</text>
  <!-- Cost calculation box -->
  <rect x="60" y="350" width="340" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="370" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">1920×1080 해상도, 샘플 16개 기준:</text>
  <text x="230" y="390" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">총 텍스처 샘플링 = 2,073,600 × 17 ≒ 3,525만 회</text>
  <text x="230" y="406" text-anchor="middle" font-family="sans-serif" font-size="9" opacity="0.6" fill="currentColor">+ 블러 패스의 추가 샘플링</text>
  <text x="230" y="424" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">비용: 높음</text>
</svg>
</div>

<br>

따라서 SSAO는 샘플 수와 해상도 설정에 따라 비용 차이가 크게 납니다. 성능 예산이 제한된 환경에서는 낮은 해상도나 적은 샘플 수로 제한하거나, 필요하지 않다면 끄는 편이 효율적입니다. 정적 오브젝트의 접촉 음영이 목적이라면 베이크 시점에 Ambient Occlusion을 라이트맵에 포함시키는 방식으로 일부를 대체할 수 있습니다.

<br>

**Motion Blur**는 카메라나 오브젝트가 움직일 때 생기는 잔상을 후처리로 표현하는 효과입니다. 게임 렌더링의 각 프레임은 기본적으로 한순간의 정지 화면이므로, 빠르게 움직이는 물체나 카메라 회전에 속도감을 더하려면 이전 프레임과 현재 프레임의 차이를 이용해 흐림을 만들어야 합니다.

이를 위해 먼저 **모션 벡터(motion vector)**가 필요합니다. 모션 벡터는 각 픽셀이 이전 프레임에서 현재 프레임까지 화면상에서 어느 방향으로 얼마나 이동했는지를 나타내는 값입니다. 카메라 움직임과 오브젝트 움직임을 반영하려면 이 정보를 별도의 버퍼에 기록해야 합니다.

포스트 프로세싱 단계에서는 각 픽셀의 모션 벡터를 읽고, 그 방향을 따라 여러 지점의 색상을 샘플링해 섞습니다. 샘플 수가 많을수록 잔상은 부드러워지지만, 픽셀당 텍스처 조회 횟수도 늘어납니다. 따라서 Motion Blur는 모션 벡터 생성 비용과 블러 샘플링 비용을 함께 고려해야 합니다.

<br>

**Depth of Field(피사계 심도)**는 초점이 맞은 거리의 대상은 선명하게 두고, 그보다 앞이나 뒤에 있는 영역을 흐리게 만드는 효과입니다. 카메라 렌즈에서 나타나는 배경 흐림을 후처리로 재현하는 방식입니다.

먼저 깊이 버퍼를 참조해 각 픽셀이 초점 거리에서 얼마나 떨어져 있는지 계산합니다. 초점 거리와의 차이가 작으면 선명하게 유지하고, 차이가 클수록 더 강한 블러를 적용합니다. 문제는 화면 전체에 같은 블러를 적용할 수 없다는 점입니다. 깊이에 따라 흐림의 크기가 달라져야 하므로, 여러 단계의 블러 결과를 만들고 깊이에 따라 섞어야 합니다.

이 과정에서 화면을 낮은 해상도로 다운샘플하고, 여러 크기의 블러를 만든 뒤 다시 원래 이미지와 합성하는 방식이 자주 사용됩니다. Depth of Field는 깊이 버퍼 조회, 여러 단계의 블러, 합성 패스가 함께 필요하므로 비용이 높은 효과에 속합니다.

### 비용 요약

포스트 프로세싱 비용은 효과 이름만으로 결정되지 않습니다. 같은 Bloom이라도 해상도, 다운샘플 단계 수, 블러 품질에 따라 비용이 달라지고, SSAO나 Motion Blur도 샘플 수를 낮추면 부담을 줄일 수 있습니다.

다만 일반적인 경향은 다음처럼 정리할 수 있습니다.

| 효과 | 비용 경향 | 주된 비용 요인 | 조절 방법 |
|------|----------|----------------|----------|
| Color Grading | 낮음 | LUT 샘플링 | LUT 크기, 다른 효과와 통합 |
| Vignette | 낮음 | 화면 위치 기반 연산 | 강도와 범위 조절 |
| Tone Mapping | 낮음~중간 | 픽셀당 수학 함수 | Color Grading과 통합 |
| Bloom | 중간 | 다운샘플, 블러, 업샘플 | 해상도, 반복 횟수, 블러 품질 제한 |
| SSAO | 높음 | 주변 깊이 샘플링, 블러 | 샘플 수와 해상도 제한 |
| Motion Blur | 높음 | 모션 벡터, 방향성 샘플링 | 샘플 수와 적용 대상 제한 |
| Depth of Field | 높음 | 깊이 기반 블러, 합성 | 품질 단계와 블러 반경 제한 |

<br>

비용이 낮은 효과는 보통 픽셀당 간단한 수학 연산이나 적은 수의 텍스처 샘플링으로 끝납니다. 반대로 비용이 높은 효과는 주변 픽셀이나 깊이 값을 여러 번 읽고, 추가 블러나 합성 패스를 거칩니다.

성능 예산이 제한된 환경에서는 Color Grading, Tone Mapping, Vignette처럼 가벼운 효과를 기본으로 두고, Bloom은 품질을 낮춰 제한적으로 사용하는 편이 현실적입니다. SSAO, Motion Blur, Depth of Field는 화면 품질에 미치는 효과가 크지만 비용도 높으므로, 필요할 때만 켜고 샘플 수와 해상도를 함께 조절해야 합니다.

---

## 렌더 타깃 전환과 URP 포스트 프로세싱

포스트 프로세싱 효과를 여러 개 적용하면, 보통 앞 단계의 출력이 다음 단계의 입력이 됩니다. 예를 들어 Bloom 결과를 만든 뒤 그 위에 Color Grading을 적용하고, 마지막에 Vignette를 적용하는 식입니다.

각 효과가 별도 패스로 실행된다면 GPU는 중간 결과를 텍스처에 기록하고, 다음 패스에서 그 텍스처를 다시 읽어야 합니다. 이때 GPU가 결과를 기록하는 대상 텍스처를 **렌더 타깃(Render Target)**이라고 합니다.

패스가 바뀌면서 GPU가 기록할 렌더 타깃도 바뀌면, 렌더 타깃 전환이 발생합니다. 타일 기반 GPU에서는 이 전환 과정에서 타일 메모리의 내용을 메인 메모리에 저장(Store)하거나, 다음 렌더 타깃의 내용을 다시 읽어오는(Load) 작업이 필요할 수 있습니다. 따라서 효과가 여러 패스로 나뉠수록 셰이더 연산뿐 아니라 메모리 대역폭 비용도 함께 누적됩니다.

> 타일 기반 GPU의 Store/Load 구조는 [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.

URP에서는 포스트 프로세싱이 렌더 파이프라인 안에 포함되어 있습니다. **Volume 시스템**은 어떤 효과를 사용할지, 각 효과의 강도와 파라미터를 어떻게 적용할지를 결정하는 설정 계층입니다. 실제 렌더링 단계에서는 이 Volume 설정을 바탕으로 필요한 포스트 프로세싱 패스가 구성됩니다.

URP의 핵심은 모든 효과를 무조건 하나의 패스로 합치는 것이 아니라, 통합할 수 있는 효과와 별도 패스가 필요한 효과를 구분해 처리하는 데 있습니다. Color Grading, Tone Mapping, Vignette처럼 현재 픽셀의 색상을 보정하는 효과는 하나의 포스트 프로세싱 패스에서 순서대로 처리하기 쉽습니다. 반면 Bloom이나 Depth of Field처럼 다운샘플, 업샘플, 중간 블러 텍스처가 필요한 효과는 별도 패스와 렌더 타깃을 사용해야 합니다.

따라서 URP의 포스트 프로세싱 최적화는 렌더 타깃 전환을 완전히 없애는 방식이 아닙니다. 별도 패스가 필요한 효과는 유지하되, 통합 가능한 효과를 한 패스로 묶어 불필요한 중간 렌더 타깃을 줄이는 방식에 가깝습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP 포스트 프로세싱 흐름</text>

  <!-- === Volume Section === -->
  <text x="20" y="52" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Volume</text>

  <!-- Volume Profile box -->
  <rect x="20" y="62" width="195" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="117" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Volume Profile</text>
  <text x="117" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(효과와 강도 설정)</text>

  <!-- Arrow from Volume to enabled effects -->
  <line x1="215" y1="92" x2="295" y2="92" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="295,87 305,92 295,97" fill="currentColor"/>

  <!-- Enabled effects box -->
  <rect x="305" y="62" width="195" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="402" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활성 포스트 효과</text>
  <text x="402" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(카메라/씬 기준 적용)</text>

  <!-- Volume note -->
  <text x="260" y="145" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Volume 설정을 바탕으로 필요한 효과만 활성화</text>

  <!-- Dashed divider -->
  <line x1="20" y1="165" x2="500" y2="165" stroke="currentColor" stroke-width="1" stroke-dasharray="6,4" opacity="0.3"/>

  <!-- === URP Section === -->
  <text x="20" y="192" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">URP</text>

  <!-- URP Pipeline outer box -->
  <rect x="20" y="202" width="480" height="145" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="222" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">URP Pipeline</text>

  <!-- 렌더링 box -->
  <rect x="40" y="238" width="80" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="260" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>

  <!-- Arrow from 렌더링 to post processing -->
  <line x1="120" y1="255" x2="168" y2="255" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="168,250 178,255 168,260" fill="currentColor"/>

  <!-- URP Post Processing box -->
  <rect x="178" y="232" width="305" height="105" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="253" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">URP Post Processing</text>

  <!-- Effect list -->
  <text x="210" y="275" font-family="sans-serif" font-size="10" fill="currentColor">├ Bloom: 별도 중간 텍스처</text>
  <text x="210" y="292" font-family="sans-serif" font-size="10" fill="currentColor">├ Color Grading + Tone Mapping</text>
  <text x="210" y="309" font-family="sans-serif" font-size="10" fill="currentColor">├ Vignette</text>
  <text x="210" y="326" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">└ 가능한 효과는 통합 패스로 처리</text>

  <!-- URP note -->
  <text x="260" y="368" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">필요한 별도 패스는 유지하고, 통합 가능한 효과는 한 패스로 묶음</text>
</svg>
</div>

<br>

위 구조에서 중요한 점은 Volume이 비용을 직접 줄이는 기능은 아니라는 점입니다. Volume은 어떤 효과가 활성화되는지를 정하고, 실제 비용은 URP가 그 효과들을 몇 개의 패스로 실행하는지에 따라 달라집니다. 통합 가능한 효과가 많을수록 렌더 타깃 전환은 줄어들고, Bloom처럼 별도 중간 텍스처가 필요한 효과가 많을수록 추가 패스와 대역폭 비용이 늘어납니다.

또한 포스트 프로세싱 셰이더에서는 정밀도 선택도 비용에 영향을 줍니다. 색상 보정이나 비네트처럼 높은 수치 정밀도가 필요하지 않은 연산은 `half` 정밀도로도 충분한 경우가 많습니다. 대상 GPU가 16비트 연산을 효율적으로 처리한다면, 이런 연산에서 레지스터 사용량과 ALU 비용을 줄일 수 있습니다.

---

## 포스트 프로세싱 적용 시 주의사항

앞에서 살펴본 것처럼 포스트 프로세싱 비용은 주로 해상도, 패스 수, 텍스처 샘플링 횟수, 렌더 타깃 형식에서 결정됩니다. 실제 설정을 조정할 때는 다음 기준을 우선 확인하는 편이 좋습니다.

**해상도** — Render Scale이나 내부 렌더링 해상도를 낮추면 포스트 프로세싱이 처리할 픽셀 수가 줄어듭니다. 대신 화면 선명도도 함께 낮아질 수 있으므로, UI 가독성이나 화면 디테일을 확인해야 합니다.

**효과 구성** — 단순히 켜진 효과의 개수만 보지 말고, 별도 패스가 필요한 효과가 포함되어 있는지 확인해야 합니다. Bloom, Depth of Field처럼 중간 텍스처와 블러가 필요한 효과는 비용이 빠르게 늘어납니다.

**HDR 여부** — Bloom과 Tone Mapping이 필요하지 않은 품질 단계라면 HDR을 끄는 것도 선택지입니다. HDR을 사용하면 더 큰 렌더 타깃 형식이 필요할 수 있고, 그만큼 메모리 사용량과 대역폭 비용이 늘어납니다.

---

## 마무리

- Shadow Map은 광원 시점에서 기록한 깊이와 현재 프래그먼트의 광원 기준 깊이를 비교해 그림자를 판정합니다.
- Shadow Map 해상도, Cascade 수, Shadow Distance는 그림자 품질과 비용을 함께 바꾸는 핵심 설정입니다.
- 모든 오브젝트에 실시간 Shadow Map을 적용하기보다, 대상에 따라 Blob Shadow, Projector/Decal, 베이크 그림자를 조합하는 편이 효율적입니다.
- 포스트 프로세싱은 렌더링이 끝난 화면 이미지를 다시 처리하므로, 해상도, 패스 수, 텍스처 샘플링 횟수, 렌더 타깃 형식이 비용을 좌우합니다.
- URP는 통합 가능한 포스트 프로세싱 효과를 한 패스로 묶어 렌더 타깃 전환과 대역폭 비용을 줄입니다.

그림자와 포스트 프로세싱은 서로 다른 기능이지만, 비용을 관리하는 방식은 비슷합니다. 화면에서 눈에 잘 띄는 곳에 예산을 집중하고, 중요도가 낮은 곳은 범위를 줄이거나 더 가벼운 표현으로 대체해야 합니다.

<br>

이제 남는 질문은 이런 비용이 실제 셰이더 코드 안에서 어떻게 만들어지는지입니다. 조명 계산, 그림자 비교, 포스트 프로세싱 효과는 모두 셰이더 명령어로 실행되고, 명령어 수와 정밀도, 분기, 텍스처 샘플링 방식에 따라 GPU 비용이 달라집니다.

다음 글인 [셰이더 최적화 (1)](/dev/unity/ShaderOptimization-1/)에서는 `half`와 `float`의 정밀도 선택, 분기 비용, 텍스처 샘플링, 셰이더 복잡도가 GPU 성능에 어떤 영향을 주는지 살펴봅니다.

<br>

---

**관련 글**
- [Bloom 효과의 원리](/dev/graphics/Bloom/)
- [Gaussian Blur의 원리](/dev/graphics/GaussianBlur/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- **조명과 그림자 (2) - 그림자와 후처리** (현재 글)

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
- [UI 최적화 (1) - 캔버스와 리빌드 시스템](/dev/unity/UIOptimization-1/)
- [UI 최적화 (2) - UI 최적화 전략](/dev/unity/UIOptimization-2/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- **조명과 그림자 (2) - 그림자와 후처리** (현재 글)
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
