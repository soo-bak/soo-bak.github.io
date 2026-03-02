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

[조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)에서는 라이팅 방식에 따른 비용 차이를, 
[셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서는 셰이더 내부의 연산 비용을 다루었습니다.

두 시리즈 모두 "조명 계산"과 "표면 셰이딩"이 GPU에서 어떻게 처리되는지에 초점을 맞추었지만, 그 계산의 기반이 되는 **빛 자체의 물리적 성질**은 별도로 다루지 않았습니다.

<br>

셰이더가 수행하는 조명 계산은 현실의 빛 현상을 근사한 것입니다.

빛이 물체 표면에 닿으면 일부는 반사되고, 일부는 물체 내부로 들어가며, 일부는 흡수되어 열로 바뀝니다. 물체가 어떤 색으로 보이는지, 표면이 반짝이는지 무광인지, 유리처럼 투명한지 불투명한지는 모두 이 세 가지 현상의 비율에 따라 결정됩니다.

셰이딩 모델은 이 물리적 현상을 수학 수식으로 옮긴 것입니다. 수식의 각 항이 어떤 물리적 현상에 대응하는지를 파악해야 파라미터의 의미를 정확히 이해할 수 있습니다.

<br>

이 시리즈는 그 기반을 다룹니다.

빛이 물리적으로 어떤 존재인지, 표면과 만났을 때 어떤 현상이 일어나는지, 그리고 게임 그래픽스에서 이 현상들을 어떤 수학적 형태로 표현하는지를 다룹니다.

이 원리를 이해하면 셰이딩 모델이 왜 특정 수식을 사용하는지, PBR에 왜 에너지 보존이 필요한지를 자연스럽게 이해할 수 있습니다.

<br>

이 첫 번째 글에서는 빛의 본질인 전자기파부터 시작하여, 표면과의 상호작용(반사, 굴절, 흡수), 이 세 현상을 제약하는 에너지 보존 법칙, 그리고 이 현상들을 하나의 수학적 프레임워크로 통합하는 BRDF 개념까지 순서대로 다룹니다.

---

## 빛이란

빛은 **전자기파(Electromagnetic Wave)**의 일종입니다.

전자기파를 이해하려면 먼저 **전기장(Electric Field)**과 **자기장(Magnetic Field)**을 알아야 합니다.

전하(Electric Charge)란 물질이 띠는 전기적 성질로, 양전하와 음전하가 있습니다.

전기장은 이 전하가 주변 공간에 미치는 힘의 영역이고, 자기장은 움직이는 전하(전류)가 주변에 만드는 힘의 영역입니다.

전자기파는 이 두 장이 서로 수직 방향으로 진동하면서 진공 속에서 초속 약 3억 m(약 30만 km/s)로 전파되는 파동입니다.

라디오파, 마이크로파, 적외선, 가시광선, 자외선, X선, 감마선은 모두 전자기파이며, **파장(Wavelength)**의 범위에 따라 구분됩니다.

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

인간의 눈이 감지할 수 있는 전자기파의 범위가 **가시광선(Visible Light)**이며, 파장은 약 380nm에서 780nm 사이에 걸쳐 있습니다. 이 범위 안에서 파장이 짧은 쪽(약 380nm)은 보라색으로, 긴 쪽(약 780nm)은 빨간색으로 인식됩니다.

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

태양빛이나 형광등에서 나오는 **백색광(White Light)**은 단일 파장이 아니라 가시광선 전 범위의 파장이 섞여 있는 빛입니다. 프리즘에 백색광을 통과시키면 파장별로 굴절 각도가 달라져 무지개색으로 분리되는 현상이 이를 보여줍니다.

<br>

게임 그래픽스에서 빛의 색상은 파장 단위가 아니라 **RGB(Red, Green, Blue)** 세 채널의 값으로 표현됩니다.

이 변환이 가능한 이유는 인간의 눈 망막에 빨강, 초록, 파랑 파장대에 각각 반응하는 세 종류의 원추세포(Cone Cell)가 존재하기 때문입니다. 원추세포는 S(Short, 약 420nm), M(Medium, 약 530nm), L(Long, 약 560nm) 세 유형으로 나뉘며, 각각 파랑, 초록, 빨강 파장대에 가장 민감하게 반응합니다.

<br>

인간이 색을 구분하는 방식은 세 종류의 원추세포가 각각 얼마나 자극되느냐에 달려 있습니다.

파장 조합이 전혀 다른 두 빛이라도, 세 원추세포를 같은 비율로 자극하면 뇌는 같은 색으로 인식합니다.

이 원리 덕분에 빨강, 초록, 파랑 세 원색의 밝기만 조절해도 인간이 지각하는 대부분의 색을 재현할 수 있습니다.

RGB 색 모델의 구조, 채널 비트 깊이, 가산 혼합 원리는 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서 구체적으로 다룹니다.

---

## 반사 (Reflection)

빛이 물체의 표면에 닿으면 일부는 표면에서 되돌아옵니다. 이 현상이 **반사(Reflection)**입니다.

반사의 방식은 표면의 거칠기에 따라 크게 두 가지로 나뉩니다.

<br>

### 정반사 (Specular Reflection)

표면이 매끄러울 때, 입사한 빛은 표면 법선(Normal, 표면에 수직인 방향)을 기준으로 대칭인 방향으로 반사됩니다.

이 현상이 **정반사(Specular Reflection)**입니다. 거울, 금속 표면, 잔잔한 수면에서 관찰할 수 있습니다.

반사 방향이 일정하므로, 관찰자가 반사광 경로에 놓일 때만 밝은 빛이 보입니다. 게임에서 오브젝트 표면에 나타나는 밝은 하이라이트(Specular Highlight)가 정반사를 표현한 것입니다.

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

정반사는 **반사 법칙(Law of Reflection)**을 따릅니다. 입사광과 법선이 이루는 각(입사각)과 반사광과 법선이 이루는 각(반사각)은 항상 같고, 입사광·법선·반사광 세 방향은 같은 평면 위에 놓입니다.

### 난반사 (Diffuse Reflection)

표면이 거칠면, 표면의 미세한 요철 때문에 각 지점의 법선 방향이 제각각입니다.

입사한 빛이 여러 방향으로 흩어져 반사되는데, 이를 **난반사(Diffuse Reflection)**라 합니다. 종이, 나무, 콘크리트, 피부 같은 표면에서 볼 수 있습니다.

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

이처럼 난반사에서는 관찰 방향에 따른 밝기 차이가 거의 없습니다.

<br>

**Lambert 표면**은 이 성질을 이상적으로 모델링한 것으로, 밝기가 오직 입사광과 법선 사이의 각도에만 의존하고 관찰 방향에는 전혀 영향을 받지 않는 표면입니다.

Lambert 표면에서 밝기를 결정하는 것은 입사각의 코사인(cos) 값입니다.

같은 폭의 빛줄기가 표면에 수직으로 닿으면 좁은 면적에 에너지가 집중되지만, 비스듬히 닿으면 넓은 면적에 퍼져 단위 면적당 에너지가 줄어듭니다.

빛이 표면에 수직으로 들어올수록(입사각이 0도에 가까울수록) 밝기가 최대이고, 비스듬할수록 cos 값이 작아지면서 밝기도 줄어듭니다.

[색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다루는 Lambert 셰이딩이 이 원리를 수식으로 구현한 것입니다.

### 현실의 표면

현실의 대부분의 물체는 정반사와 난반사가 혼합된 형태로 빛을 반사합니다.

플라스틱은 난반사가 지배적이지만 표면 코팅층에서 약한 정반사가 섞이고, 금속은 반대로 정반사가 지배적이지만 산화되거나 흠집이 있는 부분에서 난반사가 나타납니다.

셰이딩 모델은 이 혼합 비율을 파라미터로 조절하여 다양한 재질을 하나의 수식으로 표현할 수 있습니다.

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

반사가 빛이 표면에서 되돌아오는 현상이라면, **굴절(Refraction)**은 빛이 서로 다른 매질의 경계를 지날 때 진행 방향이 꺾이는 현상입니다. 여기서 매질(Medium)이란 빛이 이동하는 물질 — 공기, 물, 유리 등 — 을 뜻합니다.

굴절이 일어나는 원인은 매질마다 빛의 전파 속도가 다르기 때문입니다. 빛은 공기 중에서 빠르게 이동하지만, 물이나 유리처럼 밀도가 높은 매질에서는 느려집니다.

빛이 비스듬히 매질 경계에 도달하면, 파면(wavefront)에서 경계를 먼저 지나는 쪽이 먼저 속도가 바뀌고, 나머지 부분은 아직 원래 속도로 진행합니다. 이 속도 차이로 파면 전체가 회전하듯 휘어지면서 진행 방향이 꺾입니다. 물속에 빨대를 넣으면 꺾여 보이는 현상이 굴절의 대표적인 예입니다.

<br>

### 스넬의 법칙

굴절의 정도는 두 매질의 **굴절률(Index of Refraction, IOR)**에 의해 결정됩니다.

굴절률은 진공에서의 빛의 속도(c)를 해당 매질에서의 빛의 속도(v)로 나눈 비율(n = c / v)입니다.

진공의 굴절률이 1.0이므로, 굴절률이 1보다 큰 매질에서는 빛이 진공보다 느리게 진행합니다. 예를 들어 물의 굴절률이 1.33이라는 것은, 물속에서 빛의 속도가 진공의 약 75%(1 / 1.33)라는 뜻입니다.

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

**스넬의 법칙(Snell's Law)**은 굴절각을 계산하는 공식입니다.

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

굴절률이 높은 매질로 빛이 진입하면 빛의 속도가 느려지면서 법선 방향으로 꺾이고, 반대로 낮은 매질로 나가면 법선에서 멀어지는 방향으로 꺾입니다.

굴절률 차이가 클수록 꺾이는 각도도 커집니다. 다이아몬드(IOR 2.42)처럼 굴절률이 높은 물질에서는 빛이 내부에서 여러 번 꺾이며 독특한 광채를 만듭니다.

### 프레넬 효과 (Fresnel Effect)

**프레넬 효과(Fresnel Effect)**는 매질 경계에서 반사와 굴절(투과)의 비율이 **입사 각도**에 따라 달라지는 현상입니다.

표면에 수직으로 입사할 때 반사가 가장 적고, 비스듬하게 입사할수록 반사 비율이 높아집니다.

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

호수 위에서 수면을 정면으로 내려다보면 물속이 비교적 잘 보이지만, 먼 곳의 수면을 비스듬히 바라보면 하늘이 반사되어 비칩니다. 같은 수면인데 보는 각도에 따라 투명도가 달라지는 이 현상이 프레넬 효과의 일상적인 예입니다.

<br>

프레넬 효과는 모든 재질에서 발생하지만, 재질에 따라 변화의 폭이 다릅니다.

금속은 내부의 자유 전자가 입사광을 즉시 흡수하고 재방출하기 때문에, 정면 입사 시에도 반사율이 이미 50~90% 이상(철 약 56%, 은 약 95%)에 달합니다. 각도가 비스듬해져도 반사율이 이미 높은 상태에서 출발하므로, 변화 폭은 상대적으로 작습니다.

반면 비금속(유리, 물, 플라스틱)은 정면 입사 시 반사율이 2~5% 수준으로 낮았다가, 비스듬한 각도에서 급격히 100%에 가까워집니다. 정면과 가장자리의 반사율 차이가 크기 때문에 프레넬 효과가 뚜렷하게 드러납니다.

<br>

이 물리 현상은 게임 그래픽스에서도 그대로 적용됩니다.

오브젝트의 가장자리(실루엣)에서 반사가 강해지는 형태로 관찰되며, PBR(Physically Based Rendering, 물리 기반 렌더링) 셰이딩에서는 이 효과를 재현하는 프레넬 항(입사 각도에 따라 반사율을 조절하는 수식)이 기본으로 포함되어 있습니다.

프레넬 항이 빠지면 모든 각도에서 반사율이 동일해져 가장자리의 반사 강조가 사라집니다. 그 결과 플라스틱이든 유리든 표면이 균일하게 보이고, 재질 간 시각적 차이를 구별하기 어려워집니다.

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

위 그래프의 곡선, 즉 입사각에 따라 반사율이 변하는 프레넬 커브를 수학적으로 근사한 것이 **슐릭 근사(Schlick's Approximation)**입니다.

슐릭 근사는 정면에서 측정한 기본 반사율 $F_0$를 출발점으로, $(1 - \cos\theta)^5$ 항을 통해 입사각이 커질수록 반사율이 1.0에 수렴하는 곡선을 표현합니다.

빛의 편광까지 고려하는 원래의 프레넬 방정식은 s-편광과 p-편광 각각에 대해 삼각함수와 제곱근 연산이 필요하지만, 슐릭 근사는 내적 하나와 거듭제곱 하나로 계산됩니다.

계산량이 적으면서도 결과가 충분히 정확하므로, 실시간 렌더링에서 널리 사용됩니다.

---

## 흡수 (Absorption)

굴절 절에서 다룬 것처럼, 표면에 도달한 빛 중 반사되지 않은 부분은 굴절을 통해 물체 내부로 진입합니다.

내부로 들어간 빛의 일부는 물체를 구성하는 원자·분자의 전자를 들뜬 상태(excited state)로 끌어올리고, 이 에너지는 주변 원자들의 진동으로 전달되어 최종적으로 **열**이 됩니다.

이렇게 빛 에너지가 열로 바뀌어 사라지는 현상이 **흡수(Absorption)**이며, 어떤 파장이 얼마나 흡수되는지는 물질의 분자 구조에 따라 달라집니다.

<br>

물체가 특정 파장의 빛을 흡수하고 나머지 파장을 반사(또는 투과)하면, 관찰자의 눈에는 흡수되지 않고 남은 파장만 도달합니다.

즉, 물체의 색은 흡수되지 않고 남은 파장이 결정합니다.

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

빨간 사과의 표면은 파랑과 초록 파장의 빛을 흡수하고, 빨간 파장의 빛을 난반사합니다. 관찰자의 눈에는 반사된 빨간 빛만 도달하므로 사과가 빨간색으로 보입니다.

<br>

흰색 물체는 모든 파장을 고르게 반사하고, 검은색 물체는 대부분의 파장을 흡수합니다. 검은색 옷이 햇빛 아래에서 더운 이유는, 빛 에너지의 대부분을 흡수하여 열로 변환하기 때문입니다.

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

게임 그래픽스에서 물체의 색은 머티리얼의 **Albedo**(또는 Base Color)로 설정됩니다.

Albedo는 물체가 각 파장(RGB 채널)의 빛을 얼마나 반사하는지를 0.0~1.0 범위로 나타낸 값입니다. 0.0은 해당 채널의 빛을 전부 흡수한다는 뜻이고, 1.0은 전부 반사한다는 뜻입니다.

Albedo가 (1, 0, 0)이면 빨간 빛만 반사하고 나머지를 흡수합니다. (1, 1, 1)이면 모든 빛을 반사하므로 흰색으로 보입니다.

<br>

빛의 색과 물체의 색은 함께 작용합니다.

빨간 Albedo를 가진 물체에 파란 빛만 비추면, 물체는 파란 빛을 흡수하고 반사할 빨간 빛이 입사되지 않으므로 어둡게(거의 검정에 가깝게) 보입니다. 셰이더에서는 조명 색상과 Albedo를 **곱(multiply)**하여 이 상호작용을 계산합니다.

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

이 곱셈이 흡수의 수학적 표현입니다. Albedo의 각 채널 값이 0에 가까울수록 해당 파장을 흡수하고, 1에 가까울수록 해당 파장을 반사합니다.

<br>

### 서브서피스 스캐터링 (Subsurface Scattering)

물체 내부로 진입한 빛이 모두 흡수되는 것은 아닙니다.

**서브서피스 스캐터링(Subsurface Scattering, SSS)**은 물체 내부로 들어간 빛이 흡수되지 않고 내부 입자에 부딪혀 방향을 바꾸며 이동하다가, 입사 지점과 다른 지점의 표면으로 빠져나오는 현상입니다. 피부, 대리석, 밀랍, 우유처럼 빛이 내부를 어느 정도 통과할 수 있는 반투명 재질에서 관찰되며, 빛이 표면 아래에서 퍼지면서 부드럽고 은은한 투과감을 만들어냅니다.

<br>

앞서 난반사를 "입사한 빛이 여러 방향으로 흩어져 반사되는 현상"으로 설명했는데, 비금속 표면에서 난반사가 일어나는 물리적 원인이 이 내부 산란입니다. 빛이 물체 내부에서 여러 번 산란하면 원래의 방향 정보가 사라지고, 표면 밖으로 나올 때 모든 방향으로 고르게 퍼집니다.

불투명한 재질에서는 입사 지점과 출사 지점의 거리가 무시할 수 있을 만큼 가까워서, 셰이더가 이 내부 산란을 표면의 한 점에서 일어나는 난반사(Lambert 모델 등)로 근사합니다.

반면 피부나 대리석처럼 입사-출사 거리가 눈에 띌 만큼 큰 재질에서는 SSS 효과가 시각적으로 드러나므로, 게임에서 별도의 셰이딩 모델이나 포스트 프로세스로 이를 근사합니다.

---

## 에너지 보존

지금까지 반사, 굴절, 흡수를 개별 현상으로 다루었습니다.

이 세 현상 모두에 적용되는 물리적 제약이 **에너지 보존 법칙(Law of Energy Conservation)**입니다.

표면에서 나가는 빛의 총 에너지는 들어온 빛의 에너지를 초과할 수 없습니다.

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

PBR 이전에 널리 쓰이던 전통적 셰이딩 모델(Phong, Blinn-Phong 등)은 Diffuse 성분과 Specular 성분을 독립적으로 계산하여 더했습니다.

두 성분 사이에 에너지 총량을 제한하는 연결이 없었으므로, 특정 파라미터 조합에서 반사 에너지가 입사 에너지를 초과할 수 있었습니다.

그 결과 특정 각도에서 표면이 비정상적으로 밝아지거나, 재질 간 시각적 일관성이 깨지는 문제가 발생했습니다.

<br>

**PBR(Physically Based Rendering)**은 에너지 보존을 수식 수준에서 강제하여 이 문제를 해결합니다. PBR이 강제하는 에너지 보존 규칙은 세 가지입니다.

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

에너지 보존 원칙은 러프니스(Roughness) 파라미터에서 직접 드러납니다.

PBR 셰이더는 표면을 눈에 보이지 않을 만큼 작은 미세 면(microfacet)의 집합으로 모델링하는데, 러프니스는 이 미세 면들의 법선이 얼마나 넓은 범위로 분산되어 있는지를 결정합니다.

러프니스가 높으면 법선 방향이 넓게 퍼져 빛이 여러 방향으로 흩어지고, 하이라이트 영역이 커집니다. 이때 하이라이트의 최대 밝기는 함께 감소합니다. 면적이 넓어졌는데 밝기까지 동일하면 반사 에너지 총량이 입사 에너지를 초과하여 규칙 1을 위반하기 때문입니다.

이 미세 면 법선의 통계적 분포를 기술하는 함수가 NDF(Normal Distribution Function)이며, NDF의 코사인 가중 반구 적분이 항상 1이 되도록 정규화함으로써 "면적 × 밝기 = 일정" 관계가 수식 수준에서 유지됩니다. 여기에 기하 감쇠 함수(G)가 미세 면 사이의 차폐·그림자를, 프레넬 항(F)이 각도별 반사 비율을 처리하며, 이들이 Cook-Torrance BRDF 안에서 결합되어 전체 스페큘러 반사의 에너지 보존이 완성됩니다.

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

에너지 보존이 수식에 내장되어 있으므로, PBR에서는 러프니스를 올리든 메탈릭을 바꾸든 결과가 물리적으로 일관성을 유지합니다. 에너지 보존이 없는 전통 모델에서는 아티스트가 파라미터 조합마다 결과를 수동으로 확인하고 보정해야 했지만, PBR에서는 수식 자체가 물리적 제약을 만족시키므로 그런 보정이 필요 없습니다.

---

## BRDF 개념

지금까지 반사, 굴절, 흡수라는 개별 현상과 이를 제약하는 에너지 보존 법칙을 살펴보았습니다.

이 현상들을 하나의 수학적 프레임워크로 통합하는 도구가 **BRDF(Bidirectional Reflectance Distribution Function, 양방향 반사 분포 함수)**입니다.

<br>

### BRDF란

BRDF는 **특정 방향에서 들어온 빛이 특정 방향으로 반사되는 비율**을 정의하는 함수입니다. "양방향(Bidirectional)"이라는 이름은 입사 방향(wi)과 반사 방향(wo), 두 방향을 모두 인자로 받는 데서 유래합니다.

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

같은 빛이 같은 각도로 들어오더라도 재질에 따라 반사 분포가 달라지며, BRDF는 이 재질별 반사 특성을 수학적으로 기술합니다.

거울은 입사 방향의 정확한 대칭 방향으로만 빛을 반사하므로 BRDF가 그 한 방향에서만 높은 값을 가지고, 분필은 모든 방향으로 고르게 반사하므로 BRDF 값이 방향에 관계없이 균일합니다.

아래 다이어그램은 빛이 법선 방향에서 입사할 때, 반사 방향에 따른 BRDF 값의 분포를 재질별로 비교한 개념도입니다.

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

게임 그래픽스에서 사용하는 셰이딩 모델(Lambert, Phong, Blinn-Phong, Cook-Torrance 등)은 모두 특정 형태의 BRDF를 구현한 것입니다.

<br>

**셰이딩 모델과 BRDF**

| 셰이딩 모델 | BRDF 특성 |
|---|---|
| Lambert | 상수 BRDF (방향 무관), 난반사만 표현 |
| Phong | Lambert + 반사 방향 기반 정반사 추가 |
| Blinn-Phong | Lambert + 반법선 기반 정반사 근사 |
| Cook-Torrance (PBR) | 미세 면 이론 기반 BRDF, 에너지 보존·프레넬 포함, 물리적으로 정확한 반사 분포 |

<br>

Lambert 모델은 BRDF가 상수인 가장 단순한 형태입니다. 반사 방향에 관계없이 동일한 비율로 빛을 반사하므로, 앞서 난반사 절에서 설명한 "어느 각도에서 봐도 밝기가 같은" 표면에 대응합니다.

<br>

반면, PBR에서 사용하는 Cook-Torrance BRDF는 앞서 에너지 보존 절에서 소개한 미세 면(microfacet) 이론을 기반으로 하며, 세 가지 함수의 곱으로 구성됩니다.

법선 분포 함수(D, Normal Distribution Function)는 미세 면 법선 중 관찰자에게 빛을 정반사할 수 있는 방향을 가리키는 비율을 나타내며, 앞서 러프니스 절에서 설명한 NDF가 이 역할을 합니다.

프레넬 함수(F)는 입사각에 따라 반사되는 빛의 비율이 달라지는 프레넬 효과를 계산합니다.

기하 감쇠 함수(G)는 미세 면끼리 서로를 가려서 빛이 차단되는 정도, 즉 자기 그림자(self-shadowing)와 마스킹(masking)을 보정합니다.

이 세 함수의 곱에 정규화 인자를 결합하여, 에너지 보존을 만족하는 정반사 분포를 구성합니다. 각 함수의 구체적인 수식과 정규화 인자의 유도, 셰이딩 모델별 구현 차이는 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

### BRDF의 물리적 제약

물리적으로 올바른 BRDF는 **헬름홀츠 상호성**과 **에너지 보존**, 두 가지 조건을 만족해야 합니다.

<br>

**헬름홀츠 상호성(Helmholtz Reciprocity)**은 입사 방향과 반사 방향을 바꿔도 BRDF 값이 동일해야 한다는 조건입니다.

$$
f_r(\omega_i, \omega_o) = f_r(\omega_o, \omega_i)
$$

이 대칭성이 보장되면 광원과 관찰자의 위치를 맞바꿔도 같은 반사 결과를 얻으므로, 어떤 시점에서든 표면의 반사 특성이 일관되게 유지됩니다.

레이트레이싱에서 카메라로부터 역추적한 광선이 광원에서 출발한 광선과 같은 경로를 공유할 수 있는 것도 이 상호성 덕분입니다.

<br>

**에너지 보존(Energy Conservation)**은 반구 전체에 걸친 반사 에너지의 합이 입사 에너지를 초과하지 않아야 한다는 조건입니다.

$$
\int_{\Omega} f_r(\omega_i, \omega_o) \cos\theta_o \, d\omega_o \le 1
$$

모든 반사 방향 ω_o에 대해 BRDF와 cos θ_o의 적분이 1 이하여야 하며, 이는 앞의 에너지 보존 절에서 다룬 "나가는 에너지 ≤ 들어온 에너지" 원칙을 BRDF 함수 수준으로 공식화한 것입니다.

<br>

이 두 조건을 만족하지 않는 BRDF를 사용하면, 특정 각도에서 표면이 비물리적으로 밝아지거나 시점에 따라 반사가 달라지는 등 일관성 없는 결과가 나타납니다.

Cook-Torrance BRDF는 D·F·G 함수와 정규화 인자 자체가 이 두 조건을 만족하도록 설계되어 있으므로, PBR은 별도의 보정 없이 물리적으로 일관된 결과를 냅니다.

<br>

### BRDF의 범위 — BTDF와 BSDF

BRDF는 표면에서 **반사**되는 빛만 다룹니다.

유리나 물처럼 빛이 표면을 통과하여 반대편으로 나가는 **투과**까지 포함하려면 **BTDF(Bidirectional Transmittance Distribution Function)**가 필요합니다.

유리처럼 반사와 투과가 동시에 일어나는 재질에서는 BRDF와 BTDF를 합친 **BSDF(Bidirectional Scattering Distribution Function)**로 표면의 모든 산란을 기술합니다.

게임 그래픽스에서는 대부분의 표면이 불투명하므로 BRDF만으로 충분합니다. 투과가 필요한 재질도 완전한 BTDF를 계산하기보다, 알파 블렌딩이나 화면 공간 굴절 같은 근사 기법으로 대체하는 것이 일반적입니다.

---

## 마무리

- 빛은 전자기파의 일종이며, 인간이 볼 수 있는 가시광선은 380~780nm 파장 범위에 해당합니다. 게임에서는 RGB 세 채널의 조합으로 파장 정보를 근사합니다
- 빛이 표면에 닿으면 반사, 굴절, 흡수 세 가지 현상이 발생합니다. 반사는 거칠기에 따라 정반사(Specular)와 난반사(Diffuse)로 나뉩니다
- 굴절은 매질 경계에서 빛의 속도 차이가 만드는 방향 변화이며, 프레넬 효과는 입사 각도에 따라 반사/굴절 비율이 변하는 현상입니다
- 흡수는 물체가 특정 파장을 열로 변환하는 과정이며, 흡수되지 않고 반사된 파장이 물체의 색을 결정합니다. 셰이더에서는 조명 색상과 Albedo의 곱셈으로 이 상호작용을 표현합니다
- 에너지 보존은 반사, 굴절, 흡수 에너지의 합이 입사 에너지를 초과할 수 없다는 제약이며, PBR은 이 원칙을 셰이딩 모델 내부에 내장합니다
- BRDF는 입사 방향에서 반사 방향으로 빛이 반사되는 비율을 정의하는 함수이며, 모든 셰이딩 모델은 특정 형태의 BRDF를 구현한 것입니다

이 물리적 현상들은 독립적이지 않습니다. 반사, 굴절, 흡수는 에너지 보존이라는 하나의 제약 아래 서로 연결되고, BRDF는 이 관계를 하나의 함수로 표현합니다.

셰이딩 계산은 이 물리적 원리 위에서 이뤄지지만, 계산 결과를 화면에 옮기려면 **색공간(Color Space)**이라는 디지털 표현 체계가 필요합니다.

감마 보정은 제한된 비트 수를 인간의 밝기 인지에 맞게 배분하고, 선형 워크플로우는 조명 계산의 물리적 정확성을 보장하며, HDR은 현실의 넓은 밝기 범위를 표현합니다.

이 체계를 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서 다룹니다.

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
