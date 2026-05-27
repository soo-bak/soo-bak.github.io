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

지금까지 빛을 다룬 글은 모두 GPU 쪽에서 출발했습니다. [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)에서는 라이팅을 어떻게 처리하느냐에 따라 비용이 어떻게 갈리는지 짚었고, [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서는 셰이더 안에서 벌어지는 연산이 얼마나 무거운지를 따졌습니다.

다만 두 글 모두 빛을 *계산하는 쪽*만 보았을 뿐, 그 계산이 흉내 내려는 빛 자체가 무엇인지는 한 번도 들여다보지 않았습니다.

셰이더가 매 픽셀마다 돌리는 조명 계산은, 결국 현실에서 빛이 보이는 현상을 수식으로 근사한 값을 내놓습니다. 빛 한 줄기가 물체 표면에 닿는 순간 그 일부는 표면에서 곧장 튕겨 나가고, 일부는 표면 아래로 파고들며, 나머지는 물질에 흡수되어 열로 바뀝니다. 어떤 색으로 보일지, 금속처럼 반짝일지 종이처럼 무광일지, 유리처럼 속이 비칠지 벽돌처럼 막혀 있을지는 이 세 갈래의 비율이 가릅니다.

셰이딩 모델이라 부르는 수식은 바로 이 물리 현상을 수학으로 옮겨 적어 둡니다. 그래서 수식의 각 항이 어느 현상을 나타내는지 알고 나면, 파라미터 하나를 만질 때 표면이 왜 그렇게 변하는지가 비로소 손에 잡히게 됩니다.

이 시리즈는 그 바닥을 채우려 합니다. 빛이 물리적으로 어떤 존재인지에서 출발해, 빛이 표면과 만나면 무슨 현상이 나타나는지, 그리고 게임 그래픽스가 그 현상을 어떤 수학으로 담아내는지까지 차례로 풀어 갑니다.

이 바탕을 깔아 두면, 셰이딩 모델이 왜 하필 그 수식을 고르는지, PBR이 왜 에너지 보존을 고집하는지가 막연한 규칙이 아니라 당연한 귀결로 읽히게 됩니다.

이번 첫 글에서는 빛의 정체인 전자기파에서 출발합니다. 이어서 빛이 표면과 만나 갈라지는 반사·굴절·흡수를 살펴보고, 이 세 갈래를 묶어 두는 에너지 보존 법칙을 짚은 뒤, 마지막으로 이 모두를 한 틀로 모으는 BRDF까지 순서대로 다룹니다.

---

## 빛이란

우리가 눈으로 보는 빛은 그 정체가 **전자기파(Electromagnetic Wave)**입니다. 전자기파가 무엇인지는 **전기장(Electric Field)**과 **자기장(Magnetic Field)**이라는 두 개념에서 풀어 나갈 수 있습니다.

먼저 **전하(Electric Charge)**는 물질이 띠는 전기적 성질로, 양전하와 음전하로 나뉩니다. 전기장은 이 전하가 주변 공간에 미치는 힘의 영역이며, 자기장은 움직이는 전하, 곧 전류가 그 둘레에 만들어 내는 힘의 영역입니다.

전자기파는 이렇게 생긴 두 장이 서로 수직 방향으로 진동하며 퍼져 나가는 파동으로, 진공에서 초속 약 3억 m, 즉 약 30만 km/s로 전파됩니다.

같은 전자기파라도 파장이 얼마냐에 따라 성질이 달라집니다. 라디오파부터 마이크로파, 적외선, 가시광선, 자외선, X선, 감마선에 이르기까지 모두 전자기파이며, 이들을 구분하는 기준이 바로 **파장(Wavelength)**의 범위입니다.

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

이 넓은 스펙트럼 가운데 인간의 눈이 감지하는 좁은 구간이 **가시광선(Visible Light)**으로, 파장으로는 약 380nm에서 780nm 사이입니다. 같은 가시광선 안에서도 파장이 짧은 쪽인 약 380nm는 보라색으로, 긴 쪽인 약 780nm는 빨간색으로 눈에 들어옵니다.

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

태양빛이나 형광등 빛처럼 우리가 흰색으로 느끼는 **백색광(White Light)**은 어느 한 파장만으로 이루어진 빛이 아닙니다. 가시광선 전 범위의 파장이 한데 섞여 있는 빛이며, 프리즘을 통과시키면 그 사실이 눈에 보이게 됩니다. 파장마다 굴절되는 각도가 조금씩 다르므로 섞여 있던 색이 무지개 띠로 나뉘어 펼쳐집니다.

정작 게임 그래픽스에서 빛의 색상을 다룰 때는 파장이라는 물리량을 그대로 쓰지 않습니다. 대신 **RGB(Red, Green, Blue)** 세 채널의 값으로 색을 표현합니다.

파장을 RGB 세 값으로 옮겨도 되는 까닭은 우리 눈의 구조에 있습니다. 망막에는 빛을 받아들이는 세 종류의 **원추세포(Cone Cell)**가 있는데, 각각 S(Short, 약 420nm), M(Medium, 약 530nm), L(Long, 약 560nm)으로 나뉘며 차례로 파랑·초록·빨강 파장대에 민감하게 반응합니다.

우리가 어떤 색을 보느냐는 결국 세 원추세포가 각각 얼마나 자극되는지, 그 자극의 비율로 정해집니다. 그래서 파장 구성이 전혀 다른 두 빛이라도 세 원추세포를 같은 비율로 자극한다면 뇌는 둘을 같은 색으로 받아들입니다.

빨강·초록·파랑 세 원색의 밝기만 조절해도 사람이 지각하는 색의 대부분을 다시 만들어 낼 수 있는 것은 바로 이 원리 덕분입니다. RGB 표현이 파장을 직접 다루지 않고도 통하는 근거이기도 합니다.

> RGB 색 모델의 구조와 채널 비트 깊이, 가산 혼합 원리는 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서 자세히 다룹니다.

---

## 반사 (Reflection)

빛 한 줄기가 물체 표면에 닿는 순간, 그 일부는 안으로 들어가지 못하고 표면에서 곧장 되돌아 나옵니다. 이렇게 표면에서 빛이 되돌아 나오는 현상을 **반사(Reflection)**라고 합니다.

같은 반사라도 빛이 되돌아 나오는 모양새는 표면이 얼마나 거친가에 따라 갈립니다. 거울처럼 매끄러운 표면에서는 빛이 한 방향으로 가지런히 튕겨 나오는 반면, 종이처럼 거친 표면에서는 사방으로 흩어지며, 이 차이가 정반사와 난반사라는 두 갈래를 만듭니다.

<br>

### 정반사 (Specular Reflection)

두 갈래 가운데 매끄러운 표면 쪽에서 나타나는 것이 **정반사(Specular Reflection)**입니다. 표면이 매끄러우면 닿는 모든 지점이 같은 방향을 향하므로, 들어온 빛은 표면에 수직인 방향, 곧 **법선(Normal)**을 기준으로 대칭이 되는 한 방향으로만 튕겨 나갑니다. 거울이나 금속 표면, 잔잔한 수면이 이렇게 빛을 반사합니다.

반사광이 한 방향으로 모이는 만큼, 관찰자는 그 반사광이 향하는 길목에 눈을 두었을 때만 밝게 빛나는 부분을 보게 됩니다. 게임에서 금속이나 매끄러운 표면 위에 도드라지게 맺히는 밝은 점, 즉 **하이라이트(Specular Highlight)**가 바로 이 정반사를 옮겨 놓은 것입니다.

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

반사광이 어느 방향으로 향할지는 **반사 법칙(Law of Reflection)**으로 정해집니다. 입사광이 법선과 이루는 각인 입사각과, 반사광이 법선과 이루는 각인 반사각은 서로 같으며, 입사광과 법선, 반사광 세 방향은 하나의 평면 위에 함께 놓입니다.

### 난반사 (Diffuse Reflection)

반대로 거친 표면 쪽에서 나타나는 것이 **난반사(Diffuse Reflection)**입니다. 거친 표면은 눈에 잘 보이지 않는 미세한 요철로 덮여 있어, 지점마다 법선이 가리키는 방향이 조금씩 어긋나 있습니다. 들어온 빛은 이 제각각의 법선을 만나 서로 다른 방향으로 튕겨 나가므로, 한 줄기가 여러 갈래로 흩어지며 반사됩니다. 종이나 나무, 콘크리트, 사람의 피부가 이렇게 빛을 흩뿌립니다.

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

빛이 사방으로 고르게 흩어지므로, 난반사하는 표면은 어느 쪽에서 바라보든 밝기가 거의 비슷하게 보입니다. 보는 위치를 옮겨도 눈에 들어오는 밝기가 좀처럼 달라지지 않는 셈입니다.

이 성질을 이상에 가깝게 다듬어 둔 모델이 **Lambert 표면**으로, 밝기가 오직 입사광과 법선 사이의 각도에만 좌우되고 관찰 방향에는 흔들리지 않는 표면을 가리킵니다. 그래서 Lambert 표면의 밝기를 정하는 값은 입사각의 **코사인(cos)** 하나로 좁혀집니다.

각도가 밝기를 가르는 까닭은 같은 빛줄기가 덮는 면적이 달라지기 때문입니다. 일정한 폭의 빛줄기가 표면에 수직으로 내리꽂히면 좁은 면적에 에너지가 모이는 반면, 비스듬히 닿으면 같은 에너지가 더 넓은 면적에 퍼져 단위 면적당 밝기가 옅어집니다. 그래서 빛이 표면에 수직으로 들어와 입사각이 0도에 가까울수록 밝기가 최대에 이르고, 비스듬해질수록 cos 값이 작아지며 밝기도 함께 줄어듭니다.

> Lambert 셰이딩이 이 원리를 수식으로 구현하는 과정은 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

### 현실의 표면

앞서 본 순수한 정반사와 난반사는 어디까지나 양 극단에 놓인 이상적인 경우이고, 우리가 손으로 만지는 물체 대부분은 그 사이 어딘가에서 두 반사를 함께 일으킵니다.

플라스틱은 난반사가 주를 이루면서도 표면을 덮은 코팅층에서 약한 정반사가 덧입혀지고, 금속은 거꾸로 정반사가 주를 이루지만 산화되거나 흠집이 난 부분에서는 빛이 흩어져 난반사가 섞여 듭니다. 결국 같은 물체 안에서도 두 반사가 어느 비율로 어우러지느냐가 그 표면의 인상을 가릅니다.

셰이딩 모델은 바로 이 혼합 비율을 하나의 파라미터로 쥐고 있어, 값을 옮기는 것만으로 무광 플라스틱부터 번들거리는 금속까지 다양한 재질을 같은 수식 위에서 그려 낼 수 있습니다.

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

앞 절에서 다룬 반사가 표면에서 빛이 되돌아 나오는 현상이라면, **굴절(Refraction)**은 빛이 표면 안으로 들어가면서 방향을 바꾸는 현상입니다. 공기에서 물로, 물에서 유리로 빛이 넘어갈 때처럼 성질이 다른 두 물질의 경계를 지날 때 진행 방향이 꺾이게 됩니다. 여기서 빛이 지나는 물질, 즉 공기나 물, 유리 같은 것을 **매질(Medium)**이라 부릅니다.

빛이 방향을 꺾는 까닭은 매질마다 빛이 퍼져 나가는 속도가 다르기 때문입니다. 같은 빛이라도 공기 속에서는 빠르게 나아가지만, 물이나 유리처럼 더 빽빽한 매질로 들어서면 속도가 느려집니다.

빛이 경계에 비스듬히 닿는 순간을 따라가 보면 이 속도 차이가 어떻게 방향을 바꾸는지 드러납니다. **파면(wavefront)**의 한쪽 끝이 경계를 먼저 넘어 속도가 줄어드는 동안 아직 경계 밖에 남은 쪽은 원래 속도를 유지하므로, 파면 전체가 한쪽으로 회전하듯 기울어지며 진행 방향이 꺾이게 됩니다. 물컵에 꽂은 빨대가 수면을 기준으로 어긋나 보이는 모습이 바로 이 굴절이 눈에 드러난 예입니다.

<br>

### 스넬의 법칙

빛이 얼마나 꺾이는지는 두 매질이 빛을 얼마나 느리게 만드는지로 정해지며, 이 느려지는 정도를 숫자로 나타낸 값을 **굴절률(Index of Refraction, IOR)**이라 합니다.

굴절률은 진공에서의 빛 속도 $c$를 해당 매질에서의 빛 속도 $v$로 나눈 비율, 곧 $n = c / v$로 정의됩니다.

진공에서의 빛 속도를 기준으로 삼으므로 진공의 굴절률은 1.0이 되고, 굴절률이 1보다 큰 매질에서는 빛이 진공에서보다 느리게 나아간다는 뜻이 됩니다. 물의 굴절률 1.33을 예로 들면, 물속에서 빛의 속도가 진공에서의 약 75%($1 / 1.33$)로 떨어진다는 의미입니다.

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

이렇게 정의한 두 매질의 굴절률을 알면, 빛이 어느 각도로 꺾일지를 **스넬의 법칙(Snell's Law)**으로 계산할 수 있습니다.

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

굴절률이 더 높은 매질로 빛이 들어서면 속도가 줄면서 법선 쪽으로 더 바짝 꺾이고, 반대로 더 낮은 매질로 빠져나갈 때는 법선에서 멀어지는 쪽으로 꺾입니다. 두 매질의 굴절률 차이가 벌어질수록 꺾이는 각도도 그만큼 커지게 됩니다.

이 점은 굴절률이 2.42에 이르는 다이아몬드에서 잘 드러납니다. 안으로 들어온 빛이 높은 굴절률 탓에 내부에서 여러 차례 꺾이고 되돌면서, 다이아몬드 특유의 반짝이는 광채를 만들어 냅니다.

### 프레넬 효과 (Fresnel Effect)

앞서 스넬의 법칙이 빛이 꺾이는 각도를 다뤘다면, 같은 경계에서 빛이 반사와 굴절(투과)로 나뉘는 비율은 빛이 들어오는 각도에 따라 달라집니다. 이렇게 입사 각도가 반사와 투과의 몫을 좌우하는 현상을 **프레넬 효과(Fresnel Effect)**라 부릅니다.

빛이 표면에 수직으로 가까이 들어올 때는 반사로 돌아가는 몫이 적고, 표면을 스치듯 비스듬히 들어올수록 반사되는 비율이 높아집니다.

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

호숫가에서 발밑의 수면을 곧장 내려다보면 빛이 대부분 물속으로 투과해 바닥이 비교적 잘 들여다보이지만, 저 멀리 비스듬히 놓인 수면으로 눈을 돌리면 그쪽에서는 반사가 우세해져 하늘이 거울처럼 비칩니다. 같은 물인데도 바라보는 각도에 따라 투명하게도, 반사면처럼도 보이는 이 차이가 프레넬 효과를 일상에서 확인할 수 있는 예입니다.

프레넬 효과 자체는 어느 재질에서나 나타나지만, 정면과 가장자리 사이에서 반사율이 얼마나 크게 벌어지는지는 재질에 따라 달라집니다.

금속에서는 내부의 자유 전자가 들어온 빛을 곧바로 흡수했다가 다시 내보내므로, 정면으로 들어온 빛도 이미 50~90% 이상이 반사됩니다. 철이 약 56%, 은이 약 95%에 이르는 식이며, 출발점인 정면 반사율이 이미 높은 만큼 각도가 비스듬해져도 더 높아질 여지가 적어 변화 폭이 작은 편입니다.

반면 유리나 물, 플라스틱 같은 비금속에서는 정면 반사율이 2~5% 수준에 머무르다가, 표면을 스치는 각도로 갈수록 100%에 빠르게 가까워집니다. 정면과 가장자리의 반사율 차이가 크게 벌어지므로, 비금속에서는 프레넬 효과가 한결 뚜렷하게 드러납니다.

게임 그래픽스도 이 물리 현상을 그대로 가져다 씁니다. 화면에서는 시선과 표면이 거의 나란해지는 오브젝트의 가장자리, 즉 실루엣 부분에서 반사가 강해지는 모습으로 드러나며, **PBR(Physically Based Rendering, 물리 기반 렌더링)** 셰이딩에서는 입사 각도에 따라 반사율을 조절하는 프레넬 항을 수식 안에 기본으로 두어 이 효과를 재현합니다.

만약 셰이더에서 프레넬 항을 빼면 어느 각도에서나 반사율이 같은 값으로 고정되어, 가장자리에서 반사가 살아나는 표현이 사라집니다. 그러면 플라스틱이든 유리든 표면이 한결같이 밋밋하게 보여, 재질끼리의 시각적 차이를 알아보기 어려워집니다.

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

위 그래프에서 입사각에 따라 반사율이 휘어 오르는 이 프레넬 커브를 간단한 식으로 근사한 것이 **슐릭 근사(Schlick's Approximation)**입니다.

슐릭 근사는 정면에서 잰 기본 반사율 $F_0$를 출발점으로 삼고, 여기에 $(1 - \cos\theta)^5$ 항을 더해 입사각이 커질수록 반사율이 1.0 쪽으로 끌려 올라가는 곡선을 그려 냅니다.

이렇게 근사하는 까닭은 계산을 가볍게 하기 위해서입니다. 빛의 편광까지 따지는 원래의 프레넬 방정식은 s-편광과 p-편광 각각에 삼각함수와 제곱근 연산을 풀어야 하지만, 슐릭 근사는 벡터 내적 하나와 거듭제곱 하나로 거의 같은 곡선을 그려 냅니다. 한 픽셀마다 이 계산을 매 프레임 되풀이하는 실시간 렌더링에서는, 눈에 띄는 차이 없이 연산 부담만 덜어 주는 이 근사가 자연스레 표준처럼 자리잡았습니다.

---

## 흡수 (Absorption)

굴절 절에서는 빛이 표면을 지나 물체 안으로 들어가는 통로를 다루었습니다. 그렇게 안으로 들어간 빛은 거기서 멈추지 않으며, 물질 속을 지나는 동안 조금씩 자기 에너지를 잃어 갑니다.

빛이 물체 안에서 에너지를 잃는 과정은 분자 단위에서 일어납니다. 안으로 들어간 빛의 일부가 물질을 이루는 원자·분자의 전자를 들뜬 상태(excited state)로 끌어올리며, 이 에너지가 주변 원자들의 진동으로 옮겨 가 끝내 **열**로 바뀝니다. 빛이 이렇게 열이 되어 사라지는 과정을 **흡수(Absorption)**라고 부릅니다.

어떤 파장이 얼마나 흡수되는지는 물질마다 다른데, 이는 흡수가 그 물질의 분자 구조에 따라 정해지기 때문입니다.

흡수는 단순히 빛을 줄이는 데 그치지 않고, 우리가 보는 색을 만들어 냅니다. 물체가 특정 파장만 골라 흡수하고 나머지를 반사하거나 투과시키면, 관찰자의 눈에는 흡수를 피해 남은 파장만 도달합니다.

즉, 물체의 색이란 흡수되지 않고 살아남은 파장이 눈에 들어와 보이는 결과입니다.

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

빨간 사과를 예로 들면, 그 표면은 파랑과 초록 파장을 흡수하고 빨강만 사방으로 흩어 반사합니다. 관찰자의 눈에 도달하는 빛은 이 빨강뿐이어서 사과가 빨갛게 보이게 됩니다.

흰 물체와 검은 물체는 양 극단을 보여 줍니다. 흰 물체는 파장을 가리지 않고 고르게 반사하는 반면, 검은 물체는 들어온 빛을 거의 다 흡수해 되돌려 보낼 파장이 남지 않습니다. 여름철 검은 옷이 유난히 더운 까닭도 여기에 있어서, 흡수한 빛 에너지의 대부분이 앞서 본 과정대로 열로 바뀌기 때문입니다.

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

지금까지 본 흡수와 색의 관계를 게임 그래픽스는 머티리얼의 **Albedo**(또는 Base Color)로 옮겨 담습니다.

Albedo는 물체가 RGB 세 채널의 빛을 각각 얼마나 되돌려 보내는지를 0.0부터 1.0 사이의 값으로 적어 둔 것입니다. 채널 값이 0.0이면 그 파장을 전부 흡수해 버리고, 1.0이면 그대로 다 반사하므로, 이 값이 곧 현실의 파장별 흡수·반사 정도를 대신합니다.

가령 Albedo가 (1, 0, 0)이면 빨강만 반사하고 파랑과 초록은 흡수해 빨갛게 보이며, (1, 1, 1)이면 세 파장을 모두 반사해 흰색이 됩니다.

다만 우리가 보는 색은 Albedo 혼자 정하지 않으며, 그 자리를 비추는 빛의 색과 함께 정해집니다.

빨간 Albedo를 가진 물체에 파란 빛만 비추는 경우를 생각해 보면, 물체는 파랑을 흡수해 버리는데 정작 반사할 빨강은 처음부터 들어오지 않으므로 거의 검게 가라앉습니다. 셰이더는 이런 상호작용을 조명 색상과 Albedo를 채널끼리 **곱(multiply)**하는 연산으로 풀어냅니다.

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

결국 이 곱셈이 흡수를 수식으로 옮겨 놓은 셈입니다. Albedo의 채널 값이 0에 가까울수록 그 파장은 흡수되어 사라지고, 1에 가까울수록 살아남아 화면에 반사됩니다. 다만 안으로 들어간 빛이 늘 이렇게 흡수되거나 곧장 반사되는 것만은 아니어서, 표면 아래를 한참 헤매다 엉뚱한 곳으로 빠져나오는 빛도 있습니다.

<br>

### 서브서피스 스캐터링 (Subsurface Scattering)

물체 안으로 들어간 빛이 전부 흡수로 사라지는 것은 아닙니다. 일부는 흡수를 피한 채 물질 속을 떠돌다가 들어온 자리와 동떨어진 곳으로 다시 나오기도 하는데, 이렇게 새어 나온 빛이 재질 특유의 분위기를 만듭니다.

이처럼 안으로 들어간 빛이 내부 입자에 부딪혀 방향을 바꿔 가며 헤매다 입사 지점과 다른 표면으로 빠져나오는 현상을 **서브서피스 스캐터링(Subsurface Scattering, SSS)**이라고 부릅니다. 피부나 대리석, 밀랍, 우유처럼 빛이 속을 어느 정도 통과하는 반투명 재질에서 잘 드러나는데, 빛이 표면 아래로 번지며 새어 나오므로 가장자리가 부드럽고 은은하게 비치게 됩니다.

사실 이 내부 산란은 앞서 다룬 난반사와 뿌리가 같습니다. 난반사를 "들어온 빛이 여러 방향으로 흩어져 반사되는 현상"이라 설명했는데, 비금속 표면에서 그런 흩어짐을 만드는 물리적 원인이 바로 이 산란입니다. 빛이 속에서 여러 번 부딪히는 동안 원래 향하던 방향을 잊어버리고, 다시 밖으로 나설 무렵에는 어느 한쪽으로 치우치지 않고 사방으로 고르게 퍼지기 때문입니다.

셰이더가 이 산란을 다루는 방식은 재질이 빛을 얼마나 멀리 떠돌게 하느냐에 따라 갈립니다. 나무나 돌 같은 불투명 재질에서는 빛이 들어온 자리와 다시 나오는 자리가 거의 겹칠 만큼 가까우므로, 셰이더는 굳이 속을 추적하지 않고 표면의 한 점에서 일어나는 난반사(Lambert 모델 등)로 갈음합니다.

반면 피부나 대리석은 입사와 출사 사이의 거리가 눈에 띌 만큼 벌어져, 한 점 근사로는 그 은은한 비침을 담아내기 어렵습니다. 이런 재질에서는 SSS가 화면에 또렷이 드러나므로, 게임은 전용 셰이딩 모델이나 포스트 프로세스를 따로 두어 그 효과를 흉내 냅니다.

---

## 에너지 보존

앞에서는 반사와 굴절, 흡수를 서로 떨어진 현상처럼 하나씩 짚어 왔습니다. 다만 빛 한 줄기가 표면에 닿는 순간 이 셋은 동시에 일어나며, 그 결과를 함께 묶는 하나의 제약을 따릅니다.

이 제약을 **에너지 보존 법칙(Law of Energy Conservation)**이라 부릅니다. 표면을 떠나는 빛의 총량은 표면으로 들어온 빛의 총량을 넘어설 수 없으며, 반사로 되돌아가든 안쪽으로 굴절해 들어가든 재질에 흡수되든 이 한도를 함께 나눠 쓰게 됩니다.

들어온 에너지가 반사·투과·흡수 세 갈래로 갈라져 그 합이 입사량과 같아진다는 점은 아래 수식과 스택에서 한눈에 확인할 수 있습니다.

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

에너지 보존이 왜 그래픽스에서 중요한지는 그것이 없던 시절의 셰이딩을 떠올리면 분명해집니다. PBR 이전에 널리 쓰이던 Phong이나 Blinn-Phong 같은 전통 모델은 난반사를 맡는 Diffuse 성분과 정반사를 맡는 Specular 성분을 따로 계산한 뒤 단순히 더했습니다.

문제는 두 성분을 묶어 총량을 제한하는 고리가 어디에도 없었다는 데 있습니다. 이 고리가 빠져 있으므로 파라미터를 어떻게 조합하느냐에 따라 둘의 합이 들어온 빛보다 커지는 일까지 허용되었고, 표면이 받은 것보다 많은 빛을 내보내는 물리적으로 불가능한 상태가 만들어지곤 했습니다.

이런 초과는 특정 각도에서 표면이 까닭 없이 환하게 들뜨거나, 같은 조명 아래 둔 재질들이 서로 어긋나 보이는 식으로 드러났습니다. 결국 한 재질을 그럴듯하게 맞춰도 다른 재질이나 다른 각도에서 다시 깨지므로, 장면 전체의 일관성을 손으로 붙잡아 두기가 어려웠습니다.

**PBR(Physically Based Rendering)**은 이 빈틈을 아예 수식 안에서 막습니다. 아티스트의 주의에 기대는 대신, 반사와 난반사가 나눠 쓸 수 있는 에너지의 총량을 계산식 자체가 묶어 두므로 초과 자체가 일어날 수 없습니다. PBR이 이렇게 강제하는 규칙은 크게 세 가지로 정리됩니다.

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

이 강제가 실제 화면에서 어떻게 모습을 드러내는지는 러프니스(Roughness) 파라미터를 만질 때 또렷이 보입니다. PBR 셰이더는 표면을 눈에 보이지 않을 만큼 잘게 쪼갠 **미세 면(microfacet)**의 모음으로 다루며, 러프니스는 이 미세 면들의 법선이 얼마나 넓은 범위에 흩어져 있는지를 가리키는 값입니다.

러프니스를 올리면 법선이 사방으로 퍼지면서 반사된 빛도 여러 방향으로 갈라지고, 화면의 하이라이트는 그만큼 넓게 번집니다. 다만 이렇게 영역이 넓어질 때 하이라이트의 최댓값은 도리어 낮아집니다. 면적이 커졌는데 밝기까지 그대로라면 반사로 나가는 에너지의 총합이 들어온 빛을 넘어서, 규칙 1을 그대로 어기게 되기 때문입니다.

이 미세 면 법선이 어느 방향에 얼마나 몰려 있는지를 확률처럼 기술하는 함수가 **NDF(Normal Distribution Function)**입니다. NDF는 코사인 가중으로 반구 전체를 적분한 값이 항상 1이 되도록 정규화되어 있어, "면적 × 밝기 = 일정"이라는 관계가 사람의 손이 아니라 수식 안에서 지켜집니다.

스페큘러 반사의 보존은 NDF 하나로 끝나지 않습니다. 미세 면끼리 서로를 가리거나 그림자를 드리우는 몫은 기하 감쇠 함수(G)가, 보는 각도에 따라 달라지는 반사 비율은 프레넬 항(F)이 맡으며, 이 셋이 **Cook-Torrance BRDF** 안에서 한데 묶여 정반사 쪽 에너지 보존을 마무리합니다.

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

이처럼 제약이 수식 안에 처음부터 박혀 있으므로, PBR에서는 러프니스를 올리든 메탈릭을 바꾸든 결과가 물리적으로 어긋나지 않습니다. 보존 장치가 없던 전통 모델에서는 아티스트가 파라미터를 조합할 때마다 결과를 눈으로 확인하고 손으로 맞춰야 했지만, PBR에서는 계산식 자체가 제약을 떠안으므로 그런 수동 보정이 더는 끼어들 자리가 없습니다.

---

## BRDF 개념

앞서 우리는 반사, 굴절, 흡수를 따로 다루고, 이 세 현상이 에너지 보존이라는 하나의 한계 안에서 움직인다는 점까지 확인했습니다. 그런데 빛이 표면에 닿아 어떻게 흩어지는지를 셰이더로 계산하려면, 이 현상들을 서로 떨어진 조각이 아니라 하나의 식으로 다룰 수 있어야 합니다.

빛이 어느 방향으로 들어와 어느 방향으로 얼마나 반사되는지를 함수 하나로 묶어 기술하는 도구가 바로 **BRDF(Bidirectional Reflectance Distribution Function, 양방향 반사 분포 함수)**입니다.

<br>

### BRDF란

BRDF는 어떤 방향에서 들어온 빛이 어떤 방향으로 반사되는지, 그 반사 비율을 알려 주는 함수입니다. 이름에 붙은 "양방향(Bidirectional)"은 입사 방향(ωi)과 반사 방향(ωo)을 모두 인자로 받는다는 뜻으로, 들어오는 방향 하나만으로는 반사 분포를 결정할 수 없기 때문에 두 방향을 함께 넣어야 비로소 값이 정해집니다.

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

같은 빛이 같은 각도로 들어와도, 그 빛을 받은 표면이 거울이냐 분필이냐에 따라 반사되는 모양은 전혀 달라집니다. BRDF가 인자 하나가 아니라 함수인 까닭이 여기에 있는데, 재질마다 다른 이 반사 특성을 방향에 따른 값의 분포로 담아내기 때문입니다.

거울은 입사 방향과 정확히 대칭을 이루는 한 방향으로만 빛을 되돌리므로, BRDF도 그 한 방향에서만 큰 값을 가지고 나머지 방향에서는 거의 0이 됩니다. 반면 분필은 빛을 사방으로 고르게 흩뜨리기에, 어느 방향을 보더라도 BRDF 값이 비슷하게 균일합니다.

이처럼 같은 입사 조건에서도 재질에 따라 분포가 어떻게 갈리는지, 빛이 법선 방향에서 들어올 때를 기준으로 네 재질을 나란히 비교하면 다음과 같습니다.

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

앞 절에서 BRDF를 재질마다 다른 반사 분포로 정의했다면, 게임에서 쓰는 셰이딩 모델은 이 분포를 실제 계산식으로 옮긴 결과입니다. Lambert, Phong, Blinn-Phong, Cook-Torrance처럼 이름이 다른 모델들도 결국은 저마다 특정한 형태의 BRDF를 골라 구현한 것이며, 어떤 분포를 택하느냐가 모델 사이의 차이를 가릅니다.

<br>

**셰이딩 모델과 BRDF**

| 셰이딩 모델 | BRDF 특성 |
|---|---|
| Lambert | 상수 BRDF (방향 무관), 난반사만 표현 |
| Phong | Lambert + 반사 방향 기반 정반사 추가 |
| Blinn-Phong | Lambert + 반법선 기반 정반사 근사 |
| Cook-Torrance (PBR) | 미세 면 이론 기반 BRDF, 에너지 보존·프레넬 포함, 물리적으로 정확한 반사 분포 |

<br>

표에서 가장 단순한 형태가 Lambert입니다. BRDF가 방향과 무관한 상수 하나여서 어느 쪽으로 반사되든 같은 비율을 돌려주므로, 앞서 난반사 절에서 살펴본 "어느 각도에서 봐도 밝기가 같은" 표면이 바로 이 상수 BRDF로 표현됩니다. 빛이 사방으로 고르게 퍼지는 분필이 Lambert가 그리는 분포와 가깝습니다.

반대쪽 끝에 놓인 Cook-Torrance는 PBR의 표준 모델로, 앞서 에너지 보존 절에서 이름을 꺼낸 미세 면(microfacet) 이론을 토대로 삼습니다. 표면을 미세한 거울 조각의 집합으로 보고, 그 조각들의 거동을 세 함수의 곱으로 풀어내는 방식입니다.

먼저 법선 분포 함수(D, Normal Distribution Function)는 수많은 미세 면 가운데 관찰자 쪽으로 빛을 정반사하도록 향한 조각이 얼마나 되는지를 나타냅니다. 앞서 러프니스 절에서 다룬 NDF가 바로 이 역할을 맡으며, 표면이 거칠수록 조각의 방향이 흩어져 분포가 넓어집니다.

다음으로 프레넬 함수(F)는 입사각에 따라 반사되는 빛의 비율이 달라지는 프레넬 효과를 담당하여, 비스듬히 스칠수록 반사가 강해지는 변화를 값에 반영합니다.

마지막으로 기하 감쇠 함수(G)는 미세 면끼리 서로 앞을 가려 빛이 막히는 정도, 즉 자기 그림자(self-shadowing)와 마스킹(masking)으로 잃는 양을 덜어 냅니다.

이 셋을 곱한 뒤 정규화 인자를 붙이면, 에너지 보존을 깨지 않는 정반사 분포가 만들어집니다. 결국 같은 BRDF라는 틀 안에서, Lambert는 상수 하나로, Cook-Torrance는 세 함수의 곱으로 서로 다른 재질의 반사를 그려 내는 셈입니다.

> 각 함수의 구체적인 수식과 정규화 인자의 유도, 셰이딩 모델별 구현 차이는 [색과 빛 (3) - 셰이딩 모델](/dev/unity/ColorAndLight-3/)에서 다룹니다.

### BRDF의 물리적 제약

함수 형태가 어떻든 BRDF라고 부를 수 있으려면, 그 값이 현실의 빛을 거스르지 않아야 합니다. 물리적으로 올바른 BRDF가 지켜야 할 조건은 크게 두 가지로, **헬름홀츠 상호성**과 **에너지 보존**입니다.

첫째 조건인 **헬름홀츠 상호성(Helmholtz Reciprocity)**은 입사 방향과 반사 방향을 서로 맞바꿔도 BRDF 값이 그대로여야 한다고 요구합니다.

$$
f_r(\omega_i, \omega_o) = f_r(\omega_o, \omega_i)
$$

이 대칭이 지켜지면 광원 자리에 관찰자를 두고 관찰자 자리에 광원을 두어도 반사 결과가 똑같으므로, 어느 시점에서 표면을 보든 그 반사 특성이 흔들리지 않습니다.

레이트레이싱에서 카메라로부터 거꾸로 추적한 광선이 광원에서 출발한 광선과 같은 경로를 따라갈 수 있는 것도, 방향을 뒤집어도 값이 같다는 이 상호성에 기댄 결과입니다.

둘째 조건인 **에너지 보존(Energy Conservation)**은 표면 위 반구 전체로 반사되는 에너지를 모두 더해도 들어온 에너지를 넘지 못하도록 막습니다.

$$
\int_{\Omega} f_r(\omega_i, \omega_o) \cos\theta_o \, d\omega_o \le 1
$$

반사 방향 ω_o 전체에 걸쳐 BRDF에 cos θ_o를 곱해 적분한 값이 1을 넘지 않아야 한다는 뜻으로, 앞서 에너지 보존 절에서 본 "나가는 에너지 ≤ 들어온 에너지"라는 원칙을 이번에는 BRDF라는 함수 자체에 새겨 넣은 형태입니다.

두 조건 가운데 하나라도 어긴 BRDF를 쓰면, 어떤 각도에서 표면이 받은 빛보다 더 밝게 빛나거나 시점을 옮길 때마다 반사가 들쭉날쭉해지는 식으로 결과가 어긋나기 시작합니다.

앞서 살펴본 Cook-Torrance는 D·F·G 세 함수와 정규화 인자가 처음부터 이 두 조건을 만족하도록 짜여 있습니다. 그 덕분에 PBR에서는 작가가 따로 손을 대 밝기를 깎거나 더하지 않아도 물리적으로 어긋남 없는 반사를 얻게 됩니다.

<br>

### BRDF의 범위 — BTDF와 BSDF

지금까지 BRDF로 반사를 다루었지만, 이 함수가 담는 것은 어디까지나 표면에서 **튕겨 나오는** 빛뿐입니다. 빛이 늘 표면에 부딪혀 되돌아오기만 하는 것은 아니어서, 함수가 가리는 범위를 짚어 둘 필요가 있습니다.

유리나 물처럼 빛이 표면을 뚫고 반대편으로 빠져나가는 **투과**까지 함께 보려면, 같은 방식으로 투과 방향의 분포를 기술하는 **BTDF(Bidirectional Transmittance Distribution Function)**를 따로 둡니다. 한 표면에서 반사와 투과가 동시에 일어나는 유리 같은 재질이라면, 둘을 합쳐 표면 위 모든 산란을 한꺼번에 담는 **BSDF(Bidirectional Scattering Distribution Function)**로 다루게 됩니다.

다만 게임에 등장하는 표면은 대개 불투명하기에, 반사만 기술하는 BRDF만으로도 화면 대부분이 채워집니다. 투과가 필요한 재질조차 BTDF를 정직하게 계산하기보다 알파 블렌딩이나 화면 공간 굴절 같은 근사로 대신하는 편이 흔하며, 결국 게임 화면에 보이는 빛의 거동은 BRDF라는 함수 하나가 거의 도맡는 셈입니다. 이렇게 반사·굴절·흡수와 에너지 보존이라는 따로 떨어진 현상들이, 빛이 어느 방향으로 얼마나 흩어지는지를 묻는 한 함수 안으로 모이게 됩니다.

---

## 마무리

- 빛은 전자기파의 한 갈래이며, 사람 눈이 받아들이는 가시광선은 380~780nm 파장 범위에 걸쳐 있습니다. 게임은 이 연속 스펙트럼을 RGB 세 채널로 근사해 다룹니다
- 빛이 표면에 닿는 순간 반사·굴절·흡수 세 갈래로 나뉘며, 그중 반사는 표면 거칠기에 따라 정반사(Specular)와 난반사(Diffuse)로 다시 갈라집니다
- 굴절은 매질 경계에서 빛의 속도가 달라지며 방향이 꺾이는 현상이고, 프레넬 효과는 입사 각도가 비스듬해질수록 반사와 굴절의 비율이 기울어지는 모습을 가리킵니다
- 흡수는 물체가 특정 파장을 열로 바꾸는 과정이며, 흡수되지 않고 되돌아온 파장이 곧 우리가 보는 물체의 색이 됩니다. 셰이더는 이 과정을 조명 색상과 Albedo의 곱으로 표현합니다
- 에너지 보존은 반사·굴절·흡수로 갈라진 에너지의 합이 들어온 에너지를 넘지 못한다는 제약이며, PBR은 이 제약을 셰이딩 모델 안에 처음부터 심어 둡니다
- BRDF는 어느 방향에서 들어온 빛이 어느 방향으로 얼마나 반사되는지를 정의하는 함수이며, 어떤 셰이딩 모델이든 저마다의 BRDF 형태로 빛의 반사를 계산합니다

이렇게 정리한 현상들은 따로 떨어져 있지 않습니다. 반사·굴절·흡수는 에너지 보존이라는 하나의 제약 아래 묶이고, BRDF는 그 관계를 빛이 흩어지는 비율이라는 한 함수로 끌어모읍니다.

셰이딩 계산은 이런 물리 원리 위에서 이뤄지지만, 그 결과를 화면의 픽셀로 옮기려면 **색공간(Color Space)**이라는 디지털 표현 체계를 거쳐야 합니다.

이 체계 안에서 감마 보정은 한정된 비트를 사람의 밝기 인지에 맞춰 배분하고, 선형 워크플로우는 조명 계산이 물리적으로 어긋나지 않도록 받쳐 주며, HDR은 현실의 넓은 밝기 범위를 담아냅니다.

이 표현 체계를 [색과 빛 (2) - 색 표현과 색공간](/dev/unity/ColorAndLight-2/)에서 다룹니다.

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
