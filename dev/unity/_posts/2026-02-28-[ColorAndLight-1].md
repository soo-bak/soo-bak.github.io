---
layout: single
title: "색과 빛 (1) - 빛의 물리적 원리 - soo:bak"
date: "2026-02-28 23:00:00 +0900"
description: 전자기파와 가시광선, 반사, 굴절, 흡수, 에너지 보존, BRDF 개념을 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 빛
  - 물리
  - 모바일
---

## 셰이더가 모방하는 물리 현상

지금까지 빛을 다룬 글은 주로 구현과 비용에서 출발했습니다. [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)에서는 라이팅 방식에 따른 비용 차이를 다루었고, [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서는 셰이더 연산이 GPU에 어떤 부담을 주는지 살펴보았습니다. 이제는 그 계산이 무엇을 근사하는지, 즉 빛 자체와 표면에서 일어나는 현상을 정리할 차례입니다.

셰이더의 조명 계산은 현실의 빛을 그대로 시뮬레이션하지 않고, 화면에 필요한 결과만 수식으로 근사합니다. 빛이 물체 표면에 닿으면 일부는 반사되고, 일부는 내부로 들어가 투과하거나 산란되며, 일부는 물질에 흡수되어 열로 바뀝니다. 물체가 금속처럼 반짝이는지, 종이처럼 무광인지, 유리처럼 투명한지는 이 과정들이 어떤 비율로 일어나는지에 따라 달라집니다.

이 시리즈는 빛의 물리적 성질에서 시작해, 게임 그래픽스가 그 현상을 어떤 수학과 셰이딩 모델로 근사하는지 차례로 정리합니다. 첫 글에서는 빛을 전자기파로 보는 관점에서 출발하고, 반사·굴절·흡수, 에너지 보존, BRDF 개념까지 이어서 살펴봅니다.

---

## 빛이란

우리가 눈으로 보는 빛은 **전자기파(Electromagnetic Wave)**입니다. 전자기파는 **전기장(Electric Field)**과 **자기장(Magnetic Field)**이 함께 진동하며 공간을 지나가는 파동입니다.

전기장과 자기장은 **전하(Electric Charge)**와 연결됩니다. 전기장은 전하가 주변 공간에 만드는 힘의 장이고, 자기장은 움직이는 전하, 즉 전류가 만드는 힘의 장입니다. 전자기파에서는 이 두 장이 서로 수직 방향으로 진동하며 함께 퍼져 나갑니다.

전자기파는 진공에서 초속 약 3억 m, 즉 약 30만 km/s로 전파됩니다. 같은 전자기파라도 **파장(Wavelength)**에 따라 성질과 이름이 달라지며, 라디오파, 마이크로파, 적외선, 가시광선, 자외선, X선, 감마선은 모두 서로 다른 파장 범위의 전자기파입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 130" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="280" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">전자기파 스펙트럼</text>
  <!-- 스펙트럼 전체 바 배경 -->
  <rect x="40" y="34" width="480" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 영역 구분선 (6개 경계) -->
  <line x1="108" y1="34" x2="108" y2="66" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="177" y1="34" x2="177" y2="66" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="245" y1="34" x2="245" y2="66" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="314" y1="34" x2="314" y2="66" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="382" y1="34" x2="382" y2="66" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="451" y1="34" x2="451" y2="66" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <!-- 가시광선 영역 하이라이트 -->
  <rect x="245" y="34" width="69" height="32" fill="currentColor" fill-opacity="0.15"/>
  <!-- 영역 레이블 -->
  <text fill="currentColor" x="74" y="54" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">라디오파</text>
  <text fill="currentColor" x="142" y="54" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">마이크로파</text>
  <text fill="currentColor" x="211" y="54" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">적외선</text>
  <text fill="currentColor" x="280" y="54" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">가시광선</text>
  <text fill="currentColor" x="348" y="54" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">자외선</text>
  <text fill="currentColor" x="416" y="54" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">X선</text>
  <text fill="currentColor" x="475" y="54" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">감마선</text>
  <!-- 파장 방향 화살표 -->
  <line x1="40" y1="84" x2="520" y2="84" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <!-- 왼쪽 화살표 머리 -->
  <polygon points="40,84 48,80 48,88" fill="currentColor" opacity="0.4"/>
  <!-- 오른쪽 화살표 머리 -->
  <polygon points="520,84 512,80 512,88" fill="currentColor" opacity="0.4"/>
  <text fill="currentColor" x="40" y="100" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">긴 파장</text>
  <text fill="currentColor" x="520" y="100" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">짧은 파장</text>
  <!-- 가시광선 강조 주석 -->
  <line x1="280" y1="66" x2="280" y2="112" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.4"/>
  <polygon points="280,112 276,104 284,104" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="280" y="126" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">인간의 눈이 감지하는 영역</text>
</svg>
</div>

| 영역 | 파장 |
|:---:|:---:|
| 라디오 | ~1m |
| 마이크로파 | ~1mm |
| 적외선 | ~1μm |
| **가시광선** | **380~780nm** |
| 자외선 | ~10nm |
| X선 | ~0.1nm |
| 감마선 | <0.01nm |

<br>

이 넓은 스펙트럼 중 인간의 눈이 감지하는 좁은 구간을 **가시광선(Visible Light)**이라고 합니다. 파장으로는 대략 380nm에서 780nm 사이입니다. 가시광선 안에서도 짧은 파장은 보라색에 가깝고, 긴 파장은 빨간색에 가깝게 보입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 140" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="260" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">가시광선 스펙트럼</text>
  <!-- 스펙트럼 바 배경 -->
  <rect x="40" y="32" width="440" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 색상 구간 (7개 구간, 파장 비례 폭) -->
  <!-- 보라 380-430 : 50nm → 55px -->
  <rect x="40" y="32" width="55" height="36" rx="5" fill="currentColor" fill-opacity="0.22"/>
  <!-- 남색 430-470 : 40nm → 44px -->
  <rect x="95" y="32" width="44" height="36" fill="currentColor" fill-opacity="0.18"/>
  <!-- 파랑 470-530 : 60nm → 66px -->
  <rect x="139" y="32" width="66" height="36" fill="currentColor" fill-opacity="0.14"/>
  <!-- 초록 530-580 : 50nm → 55px -->
  <rect x="205" y="32" width="55" height="36" fill="currentColor" fill-opacity="0.10"/>
  <!-- 노랑 580-600 : 20nm → 22px -->
  <rect x="260" y="32" width="22" height="36" fill="currentColor" fill-opacity="0.07"/>
  <!-- 주황 600-700 : 100nm → 110px -->
  <rect x="282" y="32" width="110" height="36" fill="currentColor" fill-opacity="0.04"/>
  <!-- 빨강 700-780 : 80nm → 88px -->
  <rect x="392" y="32" width="88" height="36" rx="5" fill="currentColor" fill-opacity="0.02"/>
  <!-- 구간 경계선 -->
  <line x1="95" y1="32" x2="95" y2="68" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="139" y1="32" x2="139" y2="68" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="205" y1="32" x2="205" y2="68" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="260" y1="32" x2="260" y2="68" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="282" y1="32" x2="282" y2="68" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="392" y1="32" x2="392" y2="68" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <!-- 색상 레이블 -->
  <text fill="currentColor" x="67" y="54" text-anchor="middle" font-size="10" font-family="sans-serif">보라</text>
  <text fill="currentColor" x="117" y="54" text-anchor="middle" font-size="10" font-family="sans-serif">남색</text>
  <text fill="currentColor" x="172" y="54" text-anchor="middle" font-size="10" font-family="sans-serif">파랑</text>
  <text fill="currentColor" x="232" y="54" text-anchor="middle" font-size="10" font-family="sans-serif">초록</text>
  <text fill="currentColor" x="271" y="54" text-anchor="middle" font-size="9" font-family="sans-serif">노랑</text>
  <text fill="currentColor" x="337" y="54" text-anchor="middle" font-size="10" font-family="sans-serif">주황</text>
  <text fill="currentColor" x="436" y="54" text-anchor="middle" font-size="10" font-family="sans-serif">빨강</text>
  <!-- 파장 눈금선 (바 아래로 연장) -->
  <line x1="40" y1="68" x2="40" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="95" y1="68" x2="95" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="139" y1="68" x2="139" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="205" y1="68" x2="205" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="260" y1="68" x2="260" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="282" y1="68" x2="282" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="392" y1="68" x2="392" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <line x1="480" y1="68" x2="480" y2="80" stroke="currentColor" stroke-width="0.8" opacity="0.4"/>
  <!-- 파장 수치 레이블 (nm) -->
  <text fill="currentColor" x="40" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">380</text>
  <text fill="currentColor" x="95" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">430</text>
  <text fill="currentColor" x="139" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">470</text>
  <text fill="currentColor" x="205" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">530</text>
  <text fill="currentColor" x="260" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">580</text>
  <text fill="currentColor" x="282" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">600</text>
  <text fill="currentColor" x="392" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">700</text>
  <text fill="currentColor" x="480" y="92" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">780</text>
  <!-- 단위 표시 -->
  <text fill="currentColor" x="500" y="92" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">(nm)</text>
  <!-- 파장 방향 화살표 -->
  <line x1="40" y1="112" x2="480" y2="112" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="40,112 48,108 48,116" fill="currentColor" opacity="0.4"/>
  <polygon points="480,112 472,108 472,116" fill="currentColor" opacity="0.4"/>
  <text fill="currentColor" x="40" y="128" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">짧은 파장 · 높은 에너지</text>
  <text fill="currentColor" x="480" y="128" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">긴 파장 · 낮은 에너지</text>
</svg>
</div>

<br>

태양빛이나 형광등 빛처럼 우리가 흰색으로 느끼는 **백색광(White Light)**은 하나의 파장으로 이루어진 빛이 아닙니다. 가시광선 범위의 여러 파장이 섞인 빛이며, 프리즘을 통과하면 파장마다 굴절되는 각도가 달라 여러 색의 띠로 분리됩니다.

하지만 게임 그래픽스에서는 빛의 색을 파장 분포 그대로 저장하지 않습니다. 대부분 **RGB(Red, Green, Blue)** 세 채널의 값으로 색을 표현합니다. 연속적인 파장 분포를 세 값으로 줄일 수 있는 이유는 인간의 눈이 모든 파장을 개별적으로 측정하지 않기 때문입니다.

망막에는 빛을 받아들이는 세 종류의 **원추세포(Cone Cell)**가 있고, 각각 S(Short), M(Medium), L(Long)으로 나뉘어 짧은 파장대, 중간 파장대, 긴 파장대에 민감하게 반응합니다. 사람이 느끼는 색은 세 원추세포가 얼마나 자극되는지의 비율로 결정되므로, RGB는 실제 파장 분포 전체를 저장하지 않고도 인간의 색 지각을 실용적으로 근사할 수 있습니다.

> RGB 색 모델의 구조와 채널 비트 깊이, 가산 혼합 원리는 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서 자세히 다룹니다.

---

## 반사 (Reflection)

빛이 물체 표면에 닿으면 일부는 내부로 들어가지 않고 표면에서 되돌아 나옵니다. 이 현상을 **반사(Reflection)**라고 합니다.

반사된 빛의 분포는 표면의 거칠기에 따라 달라집니다. 거울처럼 매끄러운 표면에서는 빛이 한 방향으로 집중되어 반사되고, 종이처럼 거친 표면에서는 여러 방향으로 흩어집니다. 이 차이가 정반사와 난반사를 나눕니다.

<br>

### 정반사 (Specular Reflection)

매끄러운 표면에서 나타나는 반사가 **정반사(Specular Reflection)**입니다. 표면이 매끄러우면 표면의 미세한 법선 방향이 거의 같으므로, 들어온 빛은 표면에 수직인 **법선(Normal)**을 기준으로 대칭이 되는 방향으로 반사됩니다. 거울, 매끄러운 금속, 잔잔한 수면이 이런 반사를 보입니다.

정반사에서는 반사광이 특정 방향으로 집중됩니다. 따라서 관찰자가 그 방향에 있을 때만 표면이 강하게 빛나 보입니다. 게임에서 금속이나 매끄러운 표면 위에 나타나는 밝은 점, 즉 **하이라이트(Specular Highlight)**는 이 정반사를 근사한 결과입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 185" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="210" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">정반사 (Specular Reflection)</text>
  <!-- 표면 -->
  <line x1="30" y1="145" x2="390" y2="145" stroke="currentColor" stroke-width="1.8"/>
  <text fill="currentColor" x="390" y="162" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">매끄러운 표면</text>
  <!-- 입사점 -->
  <circle cx="210" cy="145" r="4" fill="currentColor"/>
  <text fill="currentColor" x="210" y="170" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">입사점</text>
  <!-- 법선 N -->
  <line x1="210" y1="145" x2="210" y2="28" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <polygon points="210,24 206,32 214,32" fill="currentColor"/>
  <text fill="currentColor" x="222" y="36" font-size="12" font-weight="bold" font-family="sans-serif">N</text>
  <!-- 입사광 -->
  <line x1="105" y1="35" x2="204" y2="139" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="206,141 196,137 202,131" fill="currentColor"/>
  <text fill="currentColor" x="95" y="32" font-size="11" font-weight="bold" font-family="sans-serif">입사광</text>
  <!-- 반사광 -->
  <line x1="210" y1="145" x2="309" y2="41" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="312,38 304,42 308,49" fill="currentColor"/>
  <text fill="currentColor" x="300" y="32" font-size="11" font-weight="bold" font-family="sans-serif">반사광</text>
  <!-- θ 입사각 호 -->
  <path d="M210,110 A35,35 0 0,0 185,120" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="181" y="110" font-size="11" font-family="sans-serif" font-style="italic">θ</text>
  <!-- θ 반사각 호 -->
  <path d="M210,110 A35,35 0 0,1 235,120" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="237" y="110" font-size="11" font-family="sans-serif" font-style="italic">θ</text>
  <!-- 주석 -->
  <text fill="currentColor" x="210" y="185" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">반사각 = 입사각 · 반사 방향이 하나로 결정됨</text>
</svg>
</div>

<br>

반사광의 방향은 **반사 법칙(Law of Reflection)**으로 정해집니다. 입사광이 법선과 이루는 입사각과, 반사광이 법선과 이루는 반사각은 같습니다. 입사광, 법선, 반사광은 같은 평면 위에 놓입니다.

### 난반사 (Diffuse Reflection)

거친 표면에서 나타나는 반사가 **난반사(Diffuse Reflection)**입니다. 거친 표면은 눈에 잘 보이지 않는 미세한 요철을 가지며, 지점마다 법선 방향이 조금씩 다릅니다. 들어온 빛은 서로 다른 미세 법선을 만나 여러 방향으로 반사됩니다. 종이, 나무, 콘크리트, 피부 같은 표면이 이런 반사를 보입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="210" y="16" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">난반사 (Diffuse Reflection)</text>
  <!-- 거친 표면 (지그재그) -->
  <polyline points="30,150 90,150 100,145 107,152 114,144 121,153 128,143 135,152 142,144 149,153 156,143 163,152 170,144 177,153 184,143 191,152 198,144 205,153 212,143 219,152 226,144 233,153 240,144 247,152 254,145 260,150 330,150" fill="none" stroke="currentColor" stroke-width="1.8"/>
  <line x1="330" y1="150" x2="400" y2="150" stroke="currentColor" stroke-width="1.8"/>
  <line x1="30" y1="150" x2="90" y2="150" stroke="currentColor" stroke-width="1.8"/>
  <text fill="currentColor" x="175" y="172" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">미세한 요철</text>
  <!-- 입사점 -->
  <circle cx="180" cy="148" r="3.5" fill="currentColor"/>
  <!-- 입사광 -->
  <line x1="100" y1="40" x2="175" y2="143" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="177,145 168,139 174,133" fill="currentColor"/>
  <text fill="currentColor" x="100" y="35" font-size="11" font-weight="bold" font-family="sans-serif">입사광</text>
  <!-- 산란 반사광 (부채꼴, 7개 — 법선 기준 좌우 대칭 분포) -->
  <!-- -60° -->
  <line x1="180" y1="148" x2="93" y2="98" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="93,98 102,99 99,105" fill="currentColor" opacity="0.6"/>
  <!-- -40° -->
  <line x1="180" y1="148" x2="116" y2="71" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="116,71 124,75 121,82" fill="currentColor" opacity="0.6"/>
  <!-- -20° -->
  <line x1="180" y1="148" x2="146" y2="51" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="146,51 152,57 145,59" fill="currentColor" opacity="0.6"/>
  <!-- 0° (수직) -->
  <line x1="180" y1="148" x2="180" y2="48" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="180,48 176,56 184,56" fill="currentColor" opacity="0.6"/>
  <!-- +20° -->
  <line x1="180" y1="148" x2="214" y2="51" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="214,51 208,57 215,59" fill="currentColor" opacity="0.6"/>
  <!-- +40° -->
  <line x1="180" y1="148" x2="244" y2="71" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="244,71 236,75 239,82" fill="currentColor" opacity="0.6"/>
  <!-- +60° -->
  <line x1="180" y1="148" x2="267" y2="98" stroke="currentColor" stroke-width="1.5" opacity="0.6"/>
  <polygon points="267,98 258,99 261,105" fill="currentColor" opacity="0.6"/>
  <!-- 주석 -->
  <text fill="currentColor" x="210" y="195" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">빛이 모든 방향으로 고르게 분산됨 → 어느 각도에서 봐도 밝기가 비슷함</text>
</svg>
</div>

<br>

빛이 여러 방향으로 분산되므로, 난반사 표면은 보는 방향이 바뀌어도 밝기가 크게 달라지지 않습니다.

이 성질을 이상화한 모델이 **Lambert 표면**입니다. Lambert 표면의 밝기는 입사광과 법선 사이의 각도에만 좌우되고, 관찰 방향에는 의존하지 않습니다. 따라서 밝기는 입사각의 **코사인(cos)** 값으로 표현됩니다.

입사각이 밝기에 영향을 주는 이유는 같은 빛이 덮는 표면 면적이 달라지기 때문입니다. 빛이 표면에 수직으로 들어오면 에너지가 좁은 면적에 집중되고, 비스듬히 들어오면 같은 에너지가 더 넓은 면적에 퍼집니다. 그래서 입사각이 0도에 가까울수록 밝고, 비스듬해질수록 cos 값이 작아지며 밝기도 줄어듭니다.

> Lambert 셰이딩이 이 원리를 수식으로 구현하는 과정은 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

### 현실의 표면

순수한 정반사와 순수한 난반사는 이상적인 양 극단입니다. 실제 물체 대부분은 두 반사를 함께 보입니다.

플라스틱은 난반사가 주를 이루지만 표면 코팅층에서 약한 정반사도 생깁니다. 금속은 정반사가 강하지만 산화되거나 흠집이 난 부분에서는 빛이 흩어져 난반사 성분이 섞입니다. 표면의 인상은 두 반사가 어떤 비율로 나타나는지에 따라 달라집니다.

셰이딩 모델은 이 혼합 비율을 머티리얼 파라미터로 제어합니다. 같은 수식 안에서도 파라미터를 바꾸면 무광 플라스틱부터 매끄러운 금속까지 다양한 재질을 표현할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 배경 -->
  <rect x="0.75" y="0.75" width="478.5" height="208.5" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="240" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">정반사와 난반사의 혼합</text>
  <!-- 연속 스케일 선 -->
  <line x1="60" y1="100" x2="420" y2="100" stroke="currentColor" stroke-width="2"/>
  <!-- 세 지점 원 -->
  <circle cx="60" cy="100" r="6" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="240" cy="100" r="6" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="420" cy="100" r="6" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <!-- 순수 난반사 라벨 -->
  <text x="60" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">순수 난반사</text>
  <text x="60" y="76" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(종이, 분필)</text>
  <text x="60" y="128" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Diffuse 100%</text>
  <text x="60" y="141" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Specular 0%</text>
  <!-- 혼합 라벨 -->
  <text x="240" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">혼합</text>
  <text x="240" y="76" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(플라스틱, 나무)</text>
  <!-- 순수 정반사 라벨 -->
  <text x="420" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">순수 정반사</text>
  <text x="420" y="76" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(거울, 금속)</text>
  <text x="420" y="128" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Specular 100%</text>
  <text x="420" y="141" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Diffuse 0%</text>
  <!-- 거칠기 양방향 화살표 -->
  <line x1="80" y1="178" x2="400" y2="178" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <!-- 왼쪽 화살촉 -->
  <polygon points="80,178 88,174 88,182" fill="currentColor" opacity="0.5"/>
  <!-- 오른쪽 화살촉 -->
  <polygon points="400,178 392,174 392,182" fill="currentColor" opacity="0.5"/>
  <!-- 거칠기 라벨 -->
  <text x="80" y="196" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">거칠기 높음</text>
  <text x="400" y="196" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">거칠기 낮음</text>
</svg>
</div>

---

## 굴절 (Refraction)

반사가 표면에서 빛이 되돌아 나오는 현상이라면, **굴절(Refraction)**은 빛이 다른 물질 안으로 들어가면서 방향을 바꾸는 현상입니다. 공기에서 물로, 물에서 유리로 빛이 넘어갈 때처럼 성질이 다른 두 물질의 경계를 지날 때 진행 방향이 바뀝니다. 빛이 지나는 공기, 물, 유리 같은 물질을 **매질(Medium)**이라고 합니다.

빛이 방향을 바꾸는 이유는 매질마다 빛의 속도가 다르기 때문입니다. 같은 빛이라도 공기에서는 비교적 빠르게 진행하고, 물이나 유리처럼 굴절률이 높은 매질에서는 더 느리게 진행합니다.

빛이 경계에 비스듬히 닿으면 속도 차이가 진행 방향을 바꿉니다. **파면(wavefront)**의 한쪽이 먼저 다른 매질에 들어가 속도가 달라지는 동안, 나머지 쪽은 아직 기존 매질에서 움직입니다. 그 결과 파면 전체가 기울어지고 빛의 진행 방향이 꺾입니다. 물컵 속 빨대가 수면을 기준으로 꺾여 보이는 현상이 굴절의 일상적인 예입니다.

<br>

### 스넬의 법칙

빛이 얼마나 꺾이는지는 두 매질에서 빛의 속도가 얼마나 다른지에 따라 정해집니다. 이 차이를 나타내는 값이 **굴절률(Index of Refraction, IOR)**입니다.

굴절률은 진공에서의 빛 속도 $c$를 해당 매질에서의 빛 속도 $v$로 나눈 비율, 즉 $n = c / v$로 정의됩니다.

진공의 굴절률은 1.0입니다. 굴절률이 1보다 큰 매질에서는 빛이 진공에서보다 느리게 진행합니다. 예를 들어 물의 굴절률이 약 1.33이라는 것은 물속에서 빛의 속도가 진공 속도의 약 75%($1 / 1.33$)라는 뜻입니다.

<br>

**주요 물질의 굴절률 (IOR)**

| 물질 | 굴절률 |
|---|---|
| 진공 | 1.0 |
| 공기 | 1.0003 |
| 물 | 1.33 |
| 유리 | 1.5 |
| 다이아몬드 | 2.42 |

<br>

두 매질의 굴절률을 알면 빛이 어느 각도로 꺾이는지 **스넬의 법칙(Snell's Law)**으로 계산할 수 있습니다.

<br>

$$
n_1 \sin\theta_1 = n_2 \sin\theta_2
$$

- $n_1$: 입사 매질의 굴절률
- $n_2$: 굴절 매질의 굴절률
- $\theta_1$: 입사각 (입사광과 법선 사이의 각도)
- $\theta_2$: 굴절각 (굴절광과 법선 사이의 각도)

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 매질 2 배경 -->
  <rect x="30" y="130" width="360" height="120" fill="currentColor" fill-opacity="0.04"/>
  <!-- 매질 경계선 -->
  <line x1="30" y1="130" x2="390" y2="130" stroke="currentColor" stroke-width="1.8"/>
  <text fill="currentColor" x="385" y="125" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">매질 경계</text>
  <!-- 법선 (점선) -->
  <line x1="210" y1="20" x2="210" y2="260" stroke="currentColor" stroke-width="1.2" stroke-dasharray="6,3" opacity="0.4"/>
  <!-- 입사점 -->
  <circle cx="210" cy="130" r="4" fill="currentColor"/>
  <!-- 매질 레이블 -->
  <text fill="currentColor" x="65" y="50" font-size="12" font-family="sans-serif">매질 1 (n₁, 예: 공기)</text>
  <text fill="currentColor" x="65" y="230" font-size="12" font-family="sans-serif">매질 2 (n₂, 예: 유리)</text>
  <!-- 입사광 -->
  <line x1="130" y1="28" x2="206" y2="125" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="208,127 199,122 205,117" fill="currentColor"/>
  <text fill="currentColor" x="135" y="65" font-size="11" font-weight="bold" font-family="sans-serif">입사광</text>
  <!-- θ1 각도 호 -->
  <path d="M210,95 A35,35 0 0,0 186,107" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="184" y="95" font-size="12" font-family="sans-serif" font-style="italic">θ₁</text>
  <!-- 굴절광 -->
  <line x1="210" y1="130" x2="262" y2="248" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="264,252 256,248 262,242" fill="currentColor"/>
  <text fill="currentColor" x="268" y="218" font-size="11" font-weight="bold" font-family="sans-serif">굴절광</text>
  <!-- θ2 각도 호 -->
  <path d="M210,165 A35,35 0 0,1 226,160" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="226" y="172" font-size="12" font-family="sans-serif" font-style="italic">θ₂</text>
  <!-- 주석 -->
  <text fill="currentColor" x="210" y="275" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">n₂ > n₁ → θ₂ < θ₁ (법선 쪽으로 꺾임) · n₂ < n₁ → θ₂ > θ₁ (법선에서 멀어짐)</text>
</svg>
</div>

<br>

빛이 굴절률이 더 높은 매질로 들어가면 속도가 줄고 법선 쪽으로 꺾입니다. 반대로 굴절률이 낮은 매질로 나가면 법선에서 멀어지는 방향으로 꺾입니다. 두 매질의 굴절률 차이가 클수록 방향 변화도 커집니다.

다이아몬드는 굴절률이 약 2.42로 높습니다. 내부로 들어간 빛이 크게 꺾이고 여러 번 반사되면서 다이아몬드 특유의 강한 광채가 만들어집니다.

### 프레넬 효과 (Fresnel Effect)

스넬의 법칙이 빛의 진행 방향을 다룬다면, **프레넬 효과(Fresnel Effect)**는 같은 경계에서 빛이 반사와 투과로 나뉘는 비율을 다룹니다. 이 비율은 빛이 표면에 들어오는 각도에 따라 달라집니다.

빛이 표면에 거의 수직으로 들어올 때는 반사되는 비율이 작고, 표면을 스치듯 비스듬히 들어올수록 반사되는 비율이 커집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레넬 효과</text>

  <!-- ===== 왼쪽: 수직 입사 ===== -->
  <g transform="translate(10, 40)">
    <!-- 배경 박스 -->
    <rect x="0" y="0" width="240" height="290" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
    <!-- 소제목 -->
    <text x="120" y="24" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정면에서 볼 때 (수직 입사)</text>

    <!-- 법선 (점선) -->
    <line x1="120" y1="45" x2="120" y2="205" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.35"/>
    <text x="134" y="54" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">법선</text>

    <!-- 표면 -->
    <line x1="30" y1="130" x2="210" y2="130" stroke="currentColor" stroke-width="2"/>
    <text x="212" y="134" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">표면</text>

    <!-- 매질 레이블 -->
    <text x="45" y="80" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">매질 1 (공기)</text>
    <text x="45" y="165" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">매질 2 (유리 등)</text>

    <!-- 입사광 (위에서 거의 수직으로) -->
    <line x1="110" y1="58" x2="118" y2="126" stroke="currentColor" stroke-width="2.5"/>
    <polygon points="118,126 113,117 122,119" fill="currentColor"/>
    <text x="83" y="72" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">입사광</text>

    <!-- 반사광 (얇은 선 = 약한 반사) -->
    <line x1="122" y1="126" x2="130" y2="58" stroke="currentColor" stroke-width="1" opacity="0.45"/>
    <polygon points="130,58 124,65 133,65" fill="currentColor" opacity="0.45"/>
    <text x="135" y="72" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">반사 (약)</text>

    <!-- 투과광 (두꺼운 선 = 강한 투과) -->
    <line x1="119" y1="134" x2="125" y2="200" stroke="currentColor" stroke-width="3.5"/>
    <polygon points="125,200 119,190 131,190" fill="currentColor"/>
    <text x="133" y="178" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">투과 (강)</text>

    <!-- 결론 -->
    <text x="120" y="238" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">→ 반사: 약함 / 투과: 강함</text>
    <text x="120" y="258" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 표면이 투명하게 보임</text>
  </g>

  <!-- ===== 오른쪽: 수평에 가까운 입사 ===== -->
  <g transform="translate(270, 40)">
    <!-- 배경 박스 -->
    <rect x="0" y="0" width="240" height="290" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
    <!-- 소제목 -->
    <text x="120" y="24" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">비스듬하게 볼 때 (수평 입사)</text>

    <!-- 법선 (점선) -->
    <line x1="140" y1="45" x2="140" y2="205" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.35"/>
    <text x="154" y="54" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">법선</text>

    <!-- 표면 -->
    <line x1="30" y1="130" x2="210" y2="130" stroke="currentColor" stroke-width="2"/>
    <text x="212" y="134" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">표면</text>

    <!-- 매질 레이블 -->
    <text x="45" y="80" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">매질 1 (공기)</text>
    <text x="45" y="165" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">매질 2 (유리 등)</text>

    <!-- 입사광 (비스듬하게, 수평에 가까운 각도) -->
    <line x1="30" y1="80" x2="136" y2="126" stroke="currentColor" stroke-width="2.5"/>
    <polygon points="136,126 127,120 131,128" fill="currentColor"/>
    <text x="42" y="74" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">입사광</text>

    <!-- 반사광 (두꺼운 선 = 강한 반사) -->
    <line x1="144" y1="126" x2="210" y2="75" stroke="currentColor" stroke-width="3.5"/>
    <polygon points="210,75 200,80 205,72" fill="currentColor"/>
    <text x="177" y="70" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">반사 (강)</text>

    <!-- 투과광 (얇은 선 = 약한 투과) -->
    <line x1="141" y1="134" x2="155" y2="200" stroke="currentColor" stroke-width="1" opacity="0.45"/>
    <polygon points="155,200 149,191 160,192" fill="currentColor" opacity="0.45"/>
    <text x="160" y="178" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">투과 (약)</text>

    <!-- 결론 -->
    <text x="120" y="238" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">→ 반사: 강함 / 투과: 약함</text>
    <text x="120" y="258" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 표면이 거울처럼 보임</text>
  </g>
</svg>
</div>

<br>

수면을 정면에 가깝게 내려다보면 빛이 많이 투과해 물속이 비교적 잘 보입니다. 반대로 먼 수면을 낮은 각도로 바라보면 반사가 강해져 하늘이 비쳐 보입니다. 같은 물이라도 보는 각도에 따라 투명하게 보이거나 반사면처럼 보이는 이유가 프레넬 효과입니다.

프레넬 효과는 대부분의 재질에서 나타나지만, 정면과 가장자리 사이의 반사율 차이는 재질마다 다릅니다.

금속은 자유 전자 때문에 정면 입사에서도 반사율이 높습니다. 철은 대략 50% 이상, 은은 90% 이상을 반사할 수 있습니다. 정면 반사율이 이미 높기 때문에 입사각이 비스듬해져도 반사율 변화 폭은 비교적 작습니다.

유리, 물, 플라스틱 같은 비금속은 정면 반사율이 보통 2~5% 수준으로 낮습니다. 하지만 표면을 스치는 각도로 갈수록 반사율은 100%에 가까워집니다. 그래서 비금속에서는 가장자리에서 반사가 강해지는 변화가 더 뚜렷합니다.

게임 그래픽스에서도 이 현상을 사용합니다. 화면에서는 시선과 표면이 거의 나란해지는 오브젝트 가장자리, 즉 실루엣 부근에서 반사가 강해지는 형태로 나타납니다. **PBR(Physically Based Rendering, 물리 기반 렌더링)** 셰이딩은 입사각에 따라 반사율을 조절하는 프레넬 항을 포함해 이 효과를 재현합니다.

프레넬 항이 없으면 반사율이 보는 각도와 무관하게 고정됩니다. 그러면 가장자리에서 반사가 강해지는 표현이 사라지고, 플라스틱이나 유리 같은 재질의 차이가 덜 자연스럽게 보입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 380 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 380px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="210" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">프레넬 효과의 반사율 변화</text>
  <!-- Y축 -->
  <line x1="55" y1="220" x2="55" y2="35" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="55,32 51,40 59,40" fill="currentColor"/>
  <text fill="currentColor" x="50" y="28" text-anchor="end" font-size="11" font-family="sans-serif">반사율</text>
  <!-- Y축 눈금 -->
  <text fill="currentColor" x="48" y="224" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">0</text>
  <line x1="52" y1="220" x2="58" y2="220" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="48" y="54" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">1</text>
  <line x1="52" y1="50" x2="58" y2="50" stroke="currentColor" stroke-width="1"/>
  <!-- X축 -->
  <line x1="55" y1="220" x2="355" y2="220" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="358,220 350,216 350,224" fill="currentColor"/>
  <!-- X축 눈금 -->
  <text fill="currentColor" x="55" y="238" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">0°</text>
  <text fill="currentColor" x="340" y="238" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">90°</text>
  <text fill="currentColor" x="55" y="252" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.4">정면 입사</text>
  <text fill="currentColor" x="340" y="252" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.4">수평 입사</text>
  <!-- 프레넬 곡선 (베지에) -->
  <path d="M55,215 C120,212 220,208 270,190 Q300,170 320,120 Q335,75 340,50" fill="none" stroke="currentColor" stroke-width="2.2"/>
  <!-- 주석: 2~5% -->
  <line x1="58" y1="215" x2="105" y2="215" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.3"/>
  <text fill="currentColor" x="110" y="210" font-size="10" font-family="sans-serif" opacity="0.5">비금속 기준 약 2~5%</text>
  <!-- 주석: 100% -->
  <line x1="340" y1="50" x2="340" y2="65" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.3"/>
  <text fill="currentColor" x="310" y="78" font-size="10" font-family="sans-serif" opacity="0.5">100%에 수렴</text>
</svg>
</div>

<br>

입사각에 따라 반사율이 증가하는 프레넬 커브를 간단한 식으로 근사한 것이 **슐릭 근사(Schlick's Approximation)**입니다.

슐릭 근사는 정면 반사율 $F_0$를 출발점으로 삼고, $(1 - \cos\theta)^5$ 항을 사용해 입사각이 커질수록 반사율이 1.0에 가까워지는 곡선을 만듭니다.

이 근사를 사용하는 이유는 계산 비용을 줄이기 위해서입니다. 원래의 프레넬 방정식은 편광을 고려하며 삼각함수와 제곱근 연산이 필요하지만, 슐릭 근사는 벡터 내적과 거듭제곱만으로 비슷한 형태의 곡선을 만듭니다. 픽셀마다 매 프레임 반복되는 실시간 렌더링에서는 이 정도의 근사가 비용과 품질 사이에서 실용적입니다.

---

## 흡수 (Absorption)

굴절은 빛이 표면을 지나 물체 안으로 들어가는 과정을 설명합니다. 하지만 안으로 들어간 빛이 모두 다시 밖으로 나오는 것은 아닙니다. 물질 속을 지나며 일부 에너지는 사라질 수 있습니다.

빛이 물체 안에서 에너지를 잃는 과정은 원자와 분자 수준에서 일어납니다. 빛의 일부가 물질을 이루는 원자·분자의 전자를 들뜬 상태(excited state)로 만들고, 이 에너지가 주변 원자의 진동 에너지로 옮겨가 **열**로 바뀝니다. 빛이 이렇게 물질 안에서 사라지는 과정을 **흡수(Absorption)**라고 합니다.

어떤 파장이 얼마나 흡수되는지는 물질의 분자 구조에 따라 달라집니다. 물체가 특정 파장을 흡수하고 나머지를 반사하거나 투과시키면, 관찰자의 눈에는 흡수되지 않고 남은 빛만 도달합니다. 물체의 색은 이 남은 빛의 결과입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 제목 -->
  <text x="210" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">흡수와 색의 관계</text>

  <!-- 백색광 레이블 -->
  <text x="150" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">백색광</text>
  <text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(모든 파장 포함)</text>

  <!-- 백색광 → 사과 화살표 -->
  <line x1="150" y1="70" x2="150" y2="95" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="145,93 150,102 155,93" fill="currentColor"/>

  <!-- 사과 박스 -->
  <rect x="50" y="105" width="200" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="128" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">빨간 사과</text>

  <!-- 구분선 -->
  <line x1="70" y1="138" x2="230" y2="138" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>

  <!-- 파랑 흡수 행 -->
  <text x="75" y="162" font-family="sans-serif" font-size="11" fill="currentColor">파랑 흡수</text>
  <line x1="148" y1="158" x2="195" y2="158" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="193,155 200,158 193,161" fill="currentColor" opacity="0.5"/>
  <text x="210" y="162" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">열</text>

  <!-- 초록 흡수 행 -->
  <text x="75" y="185" font-family="sans-serif" font-size="11" fill="currentColor">초록 흡수</text>
  <line x1="148" y1="181" x2="195" y2="181" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="193,178 200,181 193,184" fill="currentColor" opacity="0.5"/>
  <text x="210" y="185" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">열</text>

  <!-- 빨강 반사 행 -->
  <text x="75" y="218" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">빨강 반사</text>

  <!-- 빨강 반사 → 박스 밖으로 나가는 화살표 -->
  <line x1="148" y1="214" x2="262" y2="214" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="260,210 270,214 260,218" fill="currentColor"/>

  <!-- 눈 아이콘 (타원 + 원) -->
  <ellipse cx="310" cy="214" rx="22" ry="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
  <circle cx="310" cy="214" r="5" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>

  <!-- 눈 레이블 -->
  <text x="310" y="244" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">눈에 빨간색으로 보임</text>

  <!-- 보충 설명 -->
  <text x="210" y="290" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">흡수된 파장 → 운동 에너지(열)로 변환 / 반사된 파장 → 관찰자에게 도달</text>
</svg>
</div>

<br>

빨간 사과를 예로 들면, 표면은 파랑과 초록 계열의 빛을 많이 흡수하고 빨강 계열의 빛을 주로 반사합니다. 관찰자의 눈에는 반사된 빨강 계열의 빛이 도달하므로 사과가 빨갛게 보입니다.

흰 물체와 검은 물체는 양 극단에 가깝습니다. 흰 물체는 여러 파장을 비교적 고르게 반사하고, 검은 물체는 들어온 빛을 대부분 흡수합니다. 검은 옷이 햇빛 아래에서 더 뜨겁게 느껴지는 것도 흡수한 빛 에너지가 열로 바뀌기 때문입니다.

<br>

**색과 흡수/반사의 관계**

| 물체 색 | 흡수하는 파장 | 반사하는 파장 |
|---|---|---|
| 빨강 | 파랑, 초록 | 빨강 |
| 초록 | 빨강, 파랑 | 초록 |
| 파랑 | 빨강, 초록 | 파랑 |
| 흰색 | (거의 없음) | 모든 파장 |
| 검정 | 모든 파장 | (거의 없음) |
| 노랑 | 파랑 | 빨강, 초록 |

<br>

게임 그래픽스에서는 이런 흡수와 반사의 관계를 머티리얼의 **Albedo** 또는 Base Color로 표현합니다.

Albedo는 물체가 RGB 세 채널의 빛을 각각 얼마나 반사하는지를 0.0부터 1.0 사이 값으로 나타냅니다. 채널 값이 0.0에 가까우면 해당 채널의 빛을 많이 흡수하고, 1.0에 가까우면 많이 반사합니다. 이 값이 현실의 파장별 흡수·반사를 RGB 수준에서 근사합니다.

예를 들어 Albedo가 (1, 0, 0)이면 빨강 채널만 반사해 빨갛게 보이고, (1, 1, 1)이면 세 채널을 모두 반사해 흰색에 가깝게 보입니다.

다만 최종 색은 Albedo만으로 정해지지 않습니다. 표면을 비추는 조명의 색도 함께 영향을 줍니다.

빨간 Albedo를 가진 물체에 파란 빛만 비추면, 물체는 파란 빛을 거의 반사하지 못하고 반사할 빨간 빛도 들어오지 않습니다. 그래서 결과는 어둡게 보입니다. 셰이더는 이 상호작용을 조명 색상과 Albedo를 채널별로 **곱(multiply)**하는 방식으로 계산합니다.

<br>

**조명 색상과 Albedo의 상호작용** (색상 필터링만 표현, 조명 각도에 따른 밝기 변화는 생략)

$$
\text{반사 색상} = \text{조명 색상} \times \text{Albedo}
$$

$$
\begin{aligned}
\text{예시 1: 백색광 + 빨간 Albedo} \quad & (1,\;1,\;1) \times (1,\;0,\;0) = (1,\;0,\;0) \;\rightarrow\; \text{빨간색} \\[4pt]
\text{예시 2: 파란 조명 + 빨간 Albedo} \quad & (0,\;0,\;1) \times (1,\;0,\;0) = (0,\;0,\;0) \;\rightarrow\; \text{검정} \\[4pt]
\text{예시 3: 노란 조명 + 초록 Albedo} \quad & (1,\;1,\;0) \times (0,\;1,\;0) = (0,\;1,\;0) \;\rightarrow\; \text{초록색}
\end{aligned}
$$

<br>

이 곱셈은 흡수와 반사를 RGB 채널 수준에서 근사한 것입니다. Albedo의 채널 값이 0에 가까울수록 해당 빛은 흡수되고, 1에 가까울수록 반사됩니다. 다만 물체 안으로 들어간 빛이 항상 바로 흡수되거나 입사 지점에서 반사되는 것은 아닙니다. 표면 아래에서 산란된 뒤 다른 위치로 빠져나오는 경우도 있습니다.

<br>

### 서브서피스 스캐터링 (Subsurface Scattering)

물체 안으로 들어간 빛이 모두 흡수되는 것은 아닙니다. 일부는 물질 내부에서 여러 번 산란된 뒤, 들어온 지점과 다른 위치로 다시 밖으로 나옵니다. 이 빛이 반투명 재질 특유의 부드러운 느낌을 만듭니다.

안으로 들어간 빛이 내부 입자에 부딪혀 방향을 바꾸며 이동하다가 입사 지점과 다른 위치에서 빠져나오는 현상을 **서브서피스 스캐터링(Subsurface Scattering, SSS)**이라고 합니다. 피부, 대리석, 밀랍, 우유처럼 빛이 내부를 어느 정도 통과하는 재질에서 잘 드러납니다. 빛이 표면 아래로 퍼진 뒤 나오기 때문에 가장자리와 얇은 부분이 부드럽고 은은하게 보입니다.

이 내부 산란은 난반사와도 연결됩니다. 비금속 표면에서 난반사가 생기는 물리적 원인 중 하나가 빛의 내부 산란입니다. 빛이 물질 안에서 여러 번 방향을 바꾸면 원래 입사 방향의 정보가 약해지고, 다시 밖으로 나올 때 여러 방향으로 퍼집니다.

셰이더가 내부 산란을 다루는 방식은 빛이 물질 안에서 얼마나 멀리 이동하는지에 따라 달라집니다. 나무나 돌처럼 불투명한 재질에서는 빛이 들어간 위치와 다시 나오는 위치가 매우 가깝다고 볼 수 있습니다. 이 경우에는 표면 한 점에서 일어나는 난반사, 예를 들어 Lambert 모델로 충분히 근사할 수 있습니다.

반면 피부나 대리석처럼 빛이 내부에서 눈에 띄는 거리만큼 이동하는 재질은 한 점 난반사만으로 표현하기 어렵습니다. 이런 재질에서는 전용 셰이딩 모델이나 포스트 프로세스를 사용해 SSS 효과를 근사합니다.

---

## 에너지 보존

앞에서는 반사, 굴절, 흡수를 따로 설명했습니다. 하지만 실제 표면에서는 이 현상들이 같은 순간에 함께 일어납니다. 들어온 빛의 일부는 반사되고, 일부는 투과되며, 일부는 물질 안에서 흡수됩니다.

이때 전체 에너지는 **에너지 보존 법칙(Law of Energy Conservation)**을 따릅니다. 표면에서 나가는 빛과 흡수되는 에너지의 합은 표면으로 들어온 빛의 총량을 넘을 수 없습니다. 반사·투과·흡수는 서로 독립적으로 늘어나는 값이 아니라, 하나의 입사 에너지를 나눠 쓰는 항입니다.

<br>

$$
E_{\text{입사}} = E_{\text{반사}} + E_{\text{투과}} + E_{\text{흡수}}
$$

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 배경 -->
  <rect x="0.5" y="0.5" width="419" height="259" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="210" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">에너지 보존</text>
  <!-- 입사 레이블 -->
  <text x="40" y="58" font-family="sans-serif" font-size="11" fill="currentColor">입사: 100%</text>
  <!-- 스택 바: 반사 30% -->
  <rect x="40" y="72" width="100" height="40" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">반사: 30%</text>
  <!-- 화살표: 반사 → 눈에 보임 -->
  <line x1="140" y1="92" x2="280" y2="92" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polygon points="280,88 290,92 280,96" fill="currentColor"/>
  <text x="300" y="96" font-family="sans-serif" font-size="11" fill="currentColor">눈에 보임</text>
  <!-- 스택 바: 흡수 50% -->
  <rect x="40" y="112" width="100" height="40" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="136" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">흡수: 50%</text>
  <!-- 화살표: 흡수 → 열로 변환 -->
  <line x1="140" y1="132" x2="280" y2="132" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polygon points="280,128 290,132 280,136" fill="currentColor"/>
  <text x="300" y="136" font-family="sans-serif" font-size="11" fill="currentColor">열로 변환</text>
  <!-- 스택 바: 투과 20% -->
  <rect x="40" y="152" width="100" height="40" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="176" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">투과: 20%</text>
  <!-- 화살표: 투과 → 물체 통과 -->
  <line x1="140" y1="172" x2="280" y2="172" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polygon points="280,168 290,172 280,176" fill="currentColor"/>
  <text x="300" y="176" font-family="sans-serif" font-size="11" fill="currentColor">물체 통과</text>
  <!-- 검증 텍스트 -->
  <text x="210" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">30% + 50% + 20% = 100%  ✓</text>
</svg>
</div>

<br>

### 에너지 보존이 그래픽스에서 중요한 이유

에너지 보존이 그래픽스에서 중요한 이유는 전통적인 셰이딩 모델의 한계에서 잘 드러납니다. PBR 이전에 널리 쓰이던 Phong이나 Blinn-Phong 모델은 Diffuse 성분과 Specular 성분을 따로 계산한 뒤 더하는 방식이었습니다.

문제는 두 성분의 합을 입사 에너지 이하로 제한하는 구조가 없었다는 점입니다. 파라미터 조합에 따라 Diffuse와 Specular의 합이 들어온 빛보다 커질 수 있었고, 표면이 받은 것보다 더 많은 빛을 내보내는 비물리적인 결과가 나올 수 있었습니다.

이런 초과는 특정 각도에서 표면이 과하게 밝아지거나, 같은 조명 아래의 재질들이 서로 일관되지 않게 보이는 문제로 나타납니다. 한 재질을 보기 좋게 맞춰도 다른 조명이나 다른 각도에서 다시 어색해질 수 있습니다.

**PBR(Physically Based Rendering)**은 이 문제를 수식 안에서 제한합니다. 반사와 난반사가 나눠 쓸 수 있는 에너지의 총량을 계산식이 제한하므로, 받은 빛보다 더 많은 빛을 내보내지 않도록 설계됩니다. PBR에서 이 원칙은 다음과 같은 규칙으로 나타납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 외곽 배경 -->
  <rect x="1" y="1" width="438" height="308" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="220" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">PBR의 에너지 보존</text>
  <!-- 구분선 -->
  <line x1="30" y1="42" x2="410" y2="42" stroke="currentColor" stroke-opacity="0.2" stroke-width="1"/>
  <!-- 규칙 1 카드 -->
  <rect x="20" y="54" width="400" height="68" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>
  <text x="36" y="76" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">규칙 1: 반사 에너지 ≤ 입사 에너지</text>
  <text x="36" y="106" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Diffuse 반사 + Specular 반사 ≤ 1.0</text>
  <!-- 규칙 2 카드 -->
  <rect x="20" y="134" width="400" height="68" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>
  <text x="36" y="156" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">규칙 2: Specular가 증가하면 Diffuse는 감소</text>
  <text x="36" y="178" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">표면이 더 많이 정반사하면, 난반사에 쓸 수 있는</text>
  <text x="36" y="192" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">에너지가 그만큼 줄어든다</text>
  <!-- 규칙 3 카드 -->
  <rect x="20" y="214" width="400" height="82" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-opacity="0.3" stroke-width="1"/>
  <text x="36" y="236" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">규칙 3: 금속은 Diffuse가 거의 0</text>
  <text x="36" y="260" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">금속 표면은 자유전자가 빛을 대부분 정반사한다</text>
  <text x="36" y="274" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Diffuse로 나갈 에너지가 남지 않는다</text>
</svg>
</div>

<br>

이 제약은 러프니스(Roughness) 파라미터를 볼 때 잘 드러납니다. PBR 셰이더는 표면을 매우 작은 **미세 면(microfacet)**의 집합으로 보고, 러프니스는 이 미세 면들의 법선 방향이 얼마나 넓게 퍼져 있는지를 나타냅니다.

러프니스를 높이면 미세 면 법선이 넓게 퍼지고, 반사된 빛도 여러 방향으로 분산됩니다. 하이라이트는 넓어지지만 peak 밝기는 낮아집니다. 하이라이트 면적이 넓어졌는데 밝기까지 그대로라면, 반사 에너지 총량이 입사 에너지를 넘기 때문입니다.

미세 면 법선이 어느 방향에 얼마나 분포하는지를 나타내는 함수가 **NDF(Normal Distribution Function)**입니다. NDF는 정규화되어 있어 하이라이트가 넓어질수록 밝기가 낮아지는 관계가 수식 안에서 유지됩니다.

정반사 에너지 보존은 NDF만으로 끝나지 않습니다. 미세 면끼리 서로 가리는 효과는 기하 감쇠 함수(G)가, 보는 각도에 따른 반사율 변화는 프레넬 항(F)이 담당합니다. 이 요소들이 **Cook-Torrance BRDF** 안에서 함께 사용되어 정반사 분포를 만듭니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- 제목 -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">러프니스에 따른 하이라이트 변화 (에너지 보존)</text>

  <!-- ===== 왼쪽: 러프니스 낮음 ===== -->
  <text x="140" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">러프니스 낮음 (매끄러움)</text>

  <!-- 배경 박스 -->
  <rect x="20" y="62" width="240" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 기준선 -->
  <line x1="40" y1="185" x2="240" y2="185" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- 좁고 밝은 로브 (뾰족한 삼각형) -->
  <polygon points="140,95 120,185 160,185" fill="currentColor" fill-opacity="0.55" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>

  <!-- 주석 -->
  <text x="140" y="215" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">좁고 밝은 하이라이트</text>
  <text x="140" y="230" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">총 에너지 = E</text>

  <!-- ===== 오른쪽: 러프니스 높음 ===== -->
  <text x="380" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">러프니스 높음 (거침)</text>

  <!-- 배경 박스 -->
  <rect x="260" y="62" width="240" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 기준선 -->
  <line x1="280" y1="185" x2="480" y2="185" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.3"/>

  <!-- 넓고 어두운 로브 (낮고 넓은 삼각형) -->
  <polygon points="380,150 300,185 460,185" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>

  <!-- 주석 -->
  <text x="380" y="215" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">넓고 어두운 하이라이트</text>
  <text x="380" y="230" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">총 에너지 = E (동일)</text>

  <!-- ===== 등호 연결 ===== -->
  <text x="260" y="140" text-anchor="middle" font-family="sans-serif" font-size="18" font-weight="bold" fill="currentColor" opacity="0.4">=</text>

  <!-- ===== 하단 결론 ===== -->
  <line x1="100" y1="260" x2="420" y2="260" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="260" y="285" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">면적 × 밝기 = 일정</text>

</svg>
</div>

<br>

PBR은 이런 제약을 수식 안에 포함하므로 러프니스나 메탈릭 값을 바꿔도 결과가 물리적으로 크게 벗어나지 않습니다. 전통 모델에서는 아티스트가 파라미터 조합을 보며 밝기를 직접 조정해야 하는 경우가 많았지만, PBR에서는 계산식이 에너지 보존을 기본적으로 유지합니다.

---

## BRDF 개념

앞서 반사, 굴절, 흡수가 에너지 보존이라는 제약 안에서 함께 동작한다는 점을 보았습니다. 이제 셰이더는 그중 반사되는 빛을 더 구체적으로 계산해야 합니다. 같은 양의 빛이 들어와도 표면이 거울인지 분필인지에 따라 빛이 되돌아가는 방향과 세기가 달라지기 때문입니다.

이 차이를 함수로 표현한 것이 **BRDF(Bidirectional Reflectance Distribution Function, 양방향 반사 분포 함수)**입니다. BRDF는 입사 방향과 출사 방향을 기준으로, 표면이 빛을 어느 방향으로 얼마나 반사하는지 정의합니다.

<br>

### BRDF란

BRDF의 "양방향(Bidirectional)"은 입사 방향(ωi)과 반사 방향(ωo)을 모두 사용한다는 뜻입니다. 표면 반사는 들어오는 빛의 방향뿐 아니라 관찰자가 바라보는 방향에도 영향을 받으므로, 두 방향을 함께 넣어야 같은 표면의 반사 특성을 일관되게 표현할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 185" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 표면 -->
  <line x1="30" y1="150" x2="390" y2="150" stroke="currentColor" stroke-width="1.8"/>
  <text fill="currentColor" x="390" y="168" text-anchor="end" font-size="11" font-family="sans-serif" opacity="0.5">표면</text>
  <!-- 표면 점 x -->
  <circle cx="210" cy="150" r="4" fill="currentColor"/>
  <text fill="currentColor" x="210" y="175" text-anchor="middle" font-size="11" font-family="sans-serif">표면 점 x</text>
  <!-- 법선 N (점선) -->
  <line x1="210" y1="150" x2="210" y2="18" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <polygon points="210,14 206,22 214,22" fill="currentColor"/>
  <text fill="currentColor" x="222" y="28" font-size="12" font-weight="bold" font-family="sans-serif">N</text>
  <!-- 입사 방향 ωi -->
  <line x1="95" y1="32" x2="204" y2="143" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="206,145 196,141 202,135" fill="currentColor"/>
  <text fill="currentColor" x="80" y="28" font-size="12" font-weight="bold" font-family="sans-serif">ωi</text>
  <text fill="currentColor" x="60" y="44" font-size="10" font-family="sans-serif" opacity="0.5">입사 방향</text>
  <!-- 반사 방향 ωo -->
  <line x1="210" y1="150" x2="319" y2="38" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="322,35 314,38 318,46" fill="currentColor"/>
  <text fill="currentColor" x="332" y="28" font-size="12" font-weight="bold" font-family="sans-serif">ωo</text>
  <text fill="currentColor" x="340" y="44" font-size="10" font-family="sans-serif" opacity="0.5">반사 방향</text>
</svg>
</div>

$$
f_r(\omega_i, \omega_o) = \frac{L_o(\omega_o)}{E_i(\omega_i)}
$$

- **복사휘도(Radiance)**: 특정 방향으로 단위 면적, 단위 입체각당 전달되는 빛 에너지
- **복사조도(Irradiance)**: 특정 입사 방향 ωi의 빛이 표면의 단위 면적에 기여하는 에너지 (입사 복사휘도 × cosθi × 미분 입체각으로 계산)
- **입력**: 입사 방향 ωi, 반사 방향 ωo
- **출력**: 반사 비율 (0 이상의 실수)

<br>

같은 방향에서 같은 빛이 들어와도 표면이 거울인지 분필인지에 따라 반사 분포는 달라집니다. BRDF는 이런 재질별 반사 특성을 방향에 따른 값의 분포로 표현합니다.

거울은 입사 방향과 대칭인 한 방향으로 빛을 집중해 반사하므로, BRDF도 그 방향에서 큰 값을 가집니다. 반면 분필은 빛을 여러 방향으로 고르게 흩뜨리므로, BRDF 값이 넓은 방향 범위에 분포합니다.

같은 입사 조건에서도 재질에 따라 BRDF 분포가 달라지는 모습을 비교하면 다음과 같습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 450" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 이상적 거울 -->
  <text fill="currentColor" x="60" y="18" font-size="12" font-weight="bold" font-family="sans-serif">이상적 거울</text>
  <line x1="40" y1="90" x2="440" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="240" cy="90" r="3.5" fill="currentColor"/>
  <line x1="240" y1="90" x2="240" y2="22" stroke="currentColor" stroke-width="2.2"/>
  <polygon points="240,18 236,26 244,26" fill="currentColor"/>
  <text fill="currentColor" x="340" y="78" font-size="10" font-family="sans-serif" opacity="0.5">하나의 반사 방향에만 에너지 집중</text>
  <!-- 매끄러운 금속 -->
  <text fill="currentColor" x="60" y="128" font-size="12" font-weight="bold" font-family="sans-serif">매끄러운 금속</text>
  <line x1="40" y1="200" x2="440" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="240" cy="200" r="3.5" fill="currentColor"/>
  <path d="M200,200 Q210,155 240,138 Q270,155 280,200" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.8" fill-rule="nonzero"/>
  <text fill="currentColor" x="340" y="168" font-size="10" font-family="sans-serif" opacity="0.5">좁은 범위에 에너지 집중</text>
  <!-- 거친 플라스틱 -->
  <text fill="currentColor" x="60" y="238" font-size="12" font-weight="bold" font-family="sans-serif">거친 플라스틱</text>
  <line x1="40" y1="310" x2="440" y2="310" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="240" cy="310" r="3.5" fill="currentColor"/>
  <path d="M150,310 Q160,275 200,262 Q240,250 280,262 Q320,275 330,310" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <path d="M195,310 Q210,272 240,260 Q270,272 285,310" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.8"/>
  <text fill="currentColor" x="340" y="278" font-size="10" font-family="sans-serif" opacity="0.5">넓게 분산 + 약한 하이라이트</text>
  <!-- 분필 (이상적 난반사) -->
  <text fill="currentColor" x="60" y="348" font-size="12" font-weight="bold" font-family="sans-serif">분필 (이상적 난반사)</text>
  <line x1="40" y1="410" x2="440" y2="410" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="240" cy="410" r="3.5" fill="currentColor"/>
  <path d="M140,410 A100,100 0 0,1 340,410" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.8"/>
  <text fill="currentColor" x="340" y="388" font-size="10" font-family="sans-serif" opacity="0.5">모든 방향으로 균일</text>
  <!-- 입사 조건 범례 -->
  <line x1="24" y1="426" x2="24" y2="438" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3,2"/>
  <polygon points="24,442 21,437 27,437" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="34" y="440" font-size="10" font-family="sans-serif" opacity="0.5">ωi — 법선 방향 입사 (모든 재질 공통)</text>
</svg>
</div>

<br>

### BRDF와 셰이딩 모델의 관계

BRDF가 재질의 반사 분포를 정의한다면, 셰이딩 모델은 이 분포를 실제 계산식으로 구현한 것입니다. Lambert, Phong, Blinn-Phong, Cook-Torrance 같은 모델은 각각 다른 형태의 BRDF를 사용합니다. 어떤 분포를 선택하느냐가 모델의 차이를 만듭니다.

<br>

**셰이딩 모델과 BRDF**

| 셰이딩 모델 | BRDF 특성 |
|---|---|
| Lambert | 상수 BRDF (방향 무관), 난반사만 표현 |
| Phong | Lambert + 반사 방향 기반 정반사 추가 |
| Blinn-Phong | Lambert + 반법선 기반 정반사 근사 |
| Cook-Torrance (PBR) | 미세 면 이론 기반 BRDF, 에너지 보존·프레넬 포함, 물리적으로 정확한 반사 분포 |

<br>

가장 단순한 형태는 Lambert입니다. Lambert BRDF는 방향과 무관한 상수에 가깝기 때문에, 관찰 방향이 바뀌어도 밝기가 크게 변하지 않는 난반사 표면을 표현합니다. 분필처럼 빛을 넓게 퍼뜨리는 표면이 이 모델과 가깝습니다.

Cook-Torrance는 PBR에서 널리 쓰이는 모델이며, 앞서 본 미세 면(microfacet) 이론을 기반으로 합니다. 표면을 작은 거울 조각들의 집합으로 보고, 그 조각들의 분포와 가림, 프레넬 반사를 함수로 계산합니다.

법선 분포 함수(D, Normal Distribution Function)는 미세 면 중에서 반사에 기여할 방향을 가진 면이 얼마나 많은지 나타냅니다. 표면이 거칠수록 미세 면 방향이 넓게 퍼지고 분포도 넓어집니다.

프레넬 함수(F)는 입사각에 따라 반사율이 달라지는 프레넬 효과를 반영합니다.

기하 감쇠 함수(G)는 미세 면끼리 서로 가리거나 그림자를 만드는 효과, 즉 self-shadowing과 masking을 반영합니다.

이 요소들을 조합하고 정규화하면 에너지 보존을 고려한 정반사 분포를 만들 수 있습니다. 같은 BRDF라는 틀 안에서도 Lambert는 단순한 난반사를, Cook-Torrance는 미세 면 기반의 정반사를 표현합니다.

> 각 함수의 구체적인 수식과 정규화 인자의 유도, 셰이딩 모델별 구현 차이는 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

### BRDF의 물리적 제약

BRDF가 물리적으로 타당하려면 몇 가지 조건을 만족해야 합니다. 여기서 중요한 조건은 **헬름홀츠 상호성**과 **에너지 보존**입니다. 하나는 방향을 바꾸어도 반사 특성이 일관되어야 한다는 조건이고, 다른 하나는 표면이 받은 빛보다 더 많은 빛을 내보낼 수 없다는 조건입니다.

**헬름홀츠 상호성(Helmholtz Reciprocity)**은 입사 방향과 반사 방향을 서로 바꿔도 BRDF 값이 같아야 한다는 조건입니다.

$$
f_r(\omega_i, \omega_o) = f_r(\omega_o, \omega_i)
$$

이 조건이 지켜지면 광원과 관찰자의 위치를 서로 바꾸어도 반사 특성이 일관됩니다. 레이트레이싱에서 카메라에서 출발한 광선을 광원 방향으로 거꾸로 추적할 수 있는 것도 이런 상호성과 관련이 있습니다.

**에너지 보존(Energy Conservation)**은 표면 위 반구 전체로 반사되는 에너지를 모두 더해도 입사 에너지를 넘지 않아야 한다는 조건입니다.

$$
\int_{\Omega} f_r(\omega_i, \omega_o) \cos\theta_o \, d\omega_o \le 1
$$

반사 방향 ω_o 전체에 대해 BRDF에 cos θ_o를 곱해 적분한 값이 1을 넘지 않아야 한다는 뜻입니다. 앞서 본 "나가는 에너지 ≤ 들어온 에너지" 원칙을 BRDF 함수에 적용한 형태입니다.

이 조건을 어기면 표면이 받은 빛보다 더 밝게 보이거나, 시점이 바뀔 때 반사가 일관되지 않은 결과가 나올 수 있습니다.

Cook-Torrance는 D·F·G 항과 정규화 인자를 통해 이 조건들을 만족하도록 설계됩니다. 그래서 PBR에서는 별도의 수동 보정 없이도 비교적 일관된 반사 결과를 얻을 수 있습니다.

<br>

### BRDF의 범위 — BTDF와 BSDF

BRDF는 표면에서 **반사되는** 빛을 다루는 함수입니다. 하지만 빛은 반사만 하는 것이 아니라 투과되기도 하므로, BRDF가 다루는 범위를 구분해야 합니다.

유리나 물처럼 빛이 표면을 통과해 반대편으로 나가는 **투과**를 다루려면 **BTDF(Bidirectional Transmittance Distribution Function)**가 필요합니다. 반사와 투과를 함께 다루는 더 넓은 개념은 **BSDF(Bidirectional Scattering Distribution Function)**입니다.

게임에서 다루는 표면은 대부분 불투명하므로, 반사만 기술하는 BRDF만으로도 많은 재질을 표현할 수 있습니다. 투과가 필요한 재질도 실제 BTDF를 엄밀하게 계산하기보다 알파 블렌딩이나 화면 공간 굴절 같은 근사를 사용하는 경우가 많습니다. 따라서 실시간 렌더링에서는 BRDF가 대부분의 표면 반사 계산의 중심이 됩니다.

---

## 마무리

이번 글에서는 셰이더가 근사하는 빛의 기본 물리 현상을 반사, 굴절, 흡수, 에너지 보존, BRDF의 흐름으로 정리했습니다. 핵심은 다음과 같습니다.

- 빛은 전자기파의 한 갈래이며, 사람 눈이 감지하는 가시광선은 대략 380~780nm 파장 범위에 있습니다. 게임은 이 연속 스펙트럼을 RGB 세 채널로 근사합니다.
- 빛이 표면에 닿으면 반사·굴절·흡수로 나뉘며, 반사는 표면 거칠기에 따라 정반사(Specular)와 난반사(Diffuse)로 구분됩니다.
- 굴절은 매질 경계에서 빛의 속도가 달라져 진행 방향이 바뀌는 현상이고, 프레넬 효과는 입사각이 비스듬해질수록 반사율이 커지는 현상입니다.
- 흡수는 물체가 특정 파장의 에너지를 열로 바꾸는 과정이며, 흡수되지 않고 반사되거나 투과된 빛이 우리가 보는 색을 만듭니다.
- 셰이더는 흡수와 반사를 조명 색상과 Albedo의 채널별 곱으로 근사합니다.
- 에너지 보존은 반사·투과·흡수로 나뉜 에너지의 합이 입사 에너지를 넘지 못한다는 제약이며, PBR은 이 제약을 셰이딩 모델 안에 포함합니다.
- BRDF는 어느 방향에서 들어온 빛이 어느 방향으로 얼마나 반사되는지를 정의하는 함수이며, 셰이딩 모델은 각자 다른 BRDF 형태로 반사를 계산합니다.

이 현상들은 따로 떨어져 있지 않습니다. 반사·굴절·흡수는 에너지 보존이라는 제약 안에서 함께 동작하고, BRDF는 그중 표면 반사를 방향별 비율로 정리합니다.

셰이딩 계산은 이런 물리 원리를 바탕으로 하지만, 계산 결과를 화면의 픽셀로 옮기려면 **색공간(Color Space)**이라는 디지털 표현 체계를 거쳐야 합니다.

색공간 안에서 감마 보정은 제한된 비트를 사람의 밝기 지각에 맞춰 배분하고, 선형 워크플로우는 조명 계산을 물리적으로 더 일관되게 만들며, HDR은 현실의 넓은 밝기 범위를 표현합니다.

이 표현 체계는 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서 이어서 다룹니다.

<br>

---

**관련 글**
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- **색과 빛 (1) - 빛의 물리적 원리 (현재 글)**
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)

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
- **색과 빛 (1) - 빛의 물리적 원리** (현재 글)
- [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)
- [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
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
