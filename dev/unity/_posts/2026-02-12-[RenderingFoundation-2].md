---
layout: single
title: "렌더링 기초 (2) - 텍스처와 압축 - soo:bak"
date: "2026-02-12 10:11:00 +0900"
description: 텍스처의 원리, UV 매핑, 밉맵, 모바일 텍스처 압축(ASTC/ETC2), 텍스처 메모리 계산을 설명합니다.
tags:
  - Unity
  - 최적화
  - 텍스처
  - 압축
  - 모바일
---

## 메쉬 위에 색을 입히다

[Part 1](/dev/unity/RenderingFoundation-1/)에서 메쉬가 정점(Vertex)과 삼각형으로 3D 형태를 정의하는 구조임을 살펴보았습니다.

<br>

하지만 메쉬만으로는 형태만 있을 뿐, 표면에 색이나 질감이 없습니다. 정점과 삼각형은 "어떤 모양인가"만 알려주고, "어떤 색인가"는 알려주지 않습니다.

캐릭터의 피부색, 갑옷의 금속 질감, 바닥의 나무 무늬 — 이런 시각 정보를 담아두는 것이 **텍스처(Texture)**입니다. 텍스처는 색상 등의 정보를 저장한 2D 이미지입니다.
메쉬의 각 정점에는 UV 좌표가 지정되어 있어서, 텍스처의 어느 위치가 표면의 어느 지점에 대응하는지를 정의합니다. 렌더링 시 프래그먼트 셰이더가 이 UV 좌표를 사용해 텍스처에서 색상을 읽어오고, 최종 픽셀 색상을 계산합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <defs>
    <!-- 텍스처 느낌의 격자 + 노이즈 패턴 -->
    <pattern id="texBrick" x="0" y="0" width="20" height="12" patternUnits="userSpaceOnUse">
      <rect width="20" height="12" fill="#c0855a" opacity="0.35"/>
      <rect x="0" y="0" width="9" height="5" rx="0.5" fill="#a06830" opacity="0.4"/>
      <rect x="11" y="0" width="9" height="5" rx="0.5" fill="#b07840" opacity="0.35"/>
      <rect x="5" y="7" width="9" height="5" rx="0.5" fill="#a87038" opacity="0.4"/>
      <rect x="16" y="7" width="4" height="5" rx="0.5" fill="#b07840" opacity="0.35"/>
      <rect x="0" y="7" width="3" height="5" rx="0.5" fill="#b07840" opacity="0.35"/>
    </pattern>
    <clipPath id="triClipR">
      <polygon points="400,45 310,155 490,155"/>
    </clipPath>
  </defs>

  <!-- 왼쪽: 메쉬만 있는 상태 -->
  <text x="120" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">메쉬만 있는 상태</text>
  <!-- 와이어프레임 삼각형 -->
  <polygon points="120,45 30,155 210,155" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- 정점 표시 -->
  <circle cx="120" cy="45" r="3.5" fill="currentColor" opacity="0.5"/>
  <circle cx="30" cy="155" r="3.5" fill="currentColor" opacity="0.5"/>
  <circle cx="210" cy="155" r="3.5" fill="currentColor" opacity="0.5"/>
  <!-- 레이블 -->
  <text x="120" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">정점과 엣지만 있는 와이어프레임</text>

  <!-- 화살표 + 텍스처 라벨 -->
  <line x1="225" y1="100" x2="290" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="295,100 285,95 285,105" fill="currentColor"/>
  <text x="258" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">+ 텍스처</text>

  <!-- 오른쪽: 텍스처를 입힌 상태 -->
  <text x="400" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">텍스처를 입힌 상태</text>
  <!-- 배경 채움 -->
  <polygon points="400,45 310,155 490,155" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <!-- 텍스처 패턴 (클리핑) -->
  <rect x="310" y="45" width="180" height="110" fill="url(#texBrick)" clip-path="url(#triClipR)"/>
  <!-- 레이블 -->
  <text x="400" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">표면에 색상과 무늬가 입혀진 상태</text>
</svg>
</div>

---

## 텍스처의 구조

텍스처는 가로(Width) x 세로(Height) 크기의 2D 픽셀 격자이며, 각 픽셀에 채널별 데이터가 저장되어 있습니다.
색상 텍스처의 경우 각 픽셀이 색상 값을 담고 있습니다. 가장 흔한 형식은 RGBA로, 빨강(Red), 초록(Green), 파랑(Blue), 투명도(Alpha) 네 채널을 각각 8비트(0~255)로 표현합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">텍스처 (4 x 4 예시, RGBA 32bit)</text>

  <!-- 열 레이블 -->
  <text x="135" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">열 0</text>
  <text x="215" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">열 1</text>
  <text x="295" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">열 2</text>
  <text x="375" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">열 3</text>

  <!-- 행 레이블 -->
  <text x="68" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">행 0</text>
  <text x="68" y="122" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">행 1</text>
  <text x="68" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">행 2</text>
  <text x="68" y="202" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">행 3</text>

  <!-- 격자 외곽 -->
  <rect x="95" y="55" width="320" height="160" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>

  <!-- 세로 구분선 -->
  <line x1="175" y1="55" x2="175" y2="215" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="255" y1="55" x2="255" y2="215" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="335" y1="55" x2="335" y2="215" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>

  <!-- 가로 구분선 -->
  <line x1="95" y1="95" x2="415" y2="95" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="95" y1="135" x2="415" y2="135" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="95" y1="175" x2="415" y2="175" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>

  <!-- 셀 내용: RGBA (행 0) -->
  <text x="135" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="215" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="295" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="375" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>

  <!-- 셀 내용: RGBA (행 1) -->
  <text x="135" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="215" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="295" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="375" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>

  <!-- 셀 내용: RGBA (행 2) -->
  <text x="135" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="215" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="295" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="375" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>

  <!-- 셀 내용: RGBA (행 3) -->
  <text x="135" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="215" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="295" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>
  <text x="375" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">R G B A</text>

  <!-- 행 0 오른쪽 주석 -->
  <text x="425" y="80" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">4 픽셀 x 4 바이트</text>
  <text x="425" y="92" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">= 16 바이트</text>

  <!-- 총 크기 -->
  <text x="240" y="248" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">총 크기: 4 x 4 x 4 바이트 = 64 바이트</text>
</svg>
</div>

<br>

RGBA 형식에서는 한 텍셀이 4바이트(32비트)를 차지합니다.

텍스처 내부의 각 데이터 포인트를 **텍셀(Texel, Texture Element)**이라고 부릅니다. 텍셀은 텍스처에 저장된 값이고, 픽셀은 화면에 실제로 표시되는 점입니다.

텍셀과 픽셀이 항상 1:1로 대응하는 것은 아닙니다. 오브젝트가 카메라에 가까우면 텍셀 하나가 여러 픽셀에 걸치고, 멀리 있으면 여러 텍셀이 하나의 픽셀에 대응합니다.

---

## UV 매핑 — 3D 표면과 2D 텍스처의 대응

텍스처는 2D 데이터이고 메쉬는 3D 표면이므로, 표면의 어느 지점에 텍스처의 어느 부분을 대응시킬지 정해야 합니다. 이 대응 관계를 **UV 매핑(UV Mapping)**이라고 합니다.

### UV 좌표계

UV 좌표계에서 **U**는 가로 축, **V**는 세로 축이며, 두 축 모두 0에서 1 사이의 정규화된 값을 사용합니다. (0, 0)은 텍스처의 왼쪽 아래, (1, 1)은 오른쪽 위에 해당합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 360 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 360px; width: 100%;">
  <!-- V축 -->
  <line x1="60" y1="250" x2="60" y2="30" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="60,25 55,35 65,35" fill="currentColor"/>
  <text x="50" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">V</text>

  <!-- U축 -->
  <line x1="60" y1="250" x2="330" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="335,250 325,245 325,255" fill="currentColor"/>
  <text x="340" y="254" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">U</text>

  <!-- 텍스처 영역 -->
  <rect x="60" y="45" width="260" height="205" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>

  <!-- 텍스처 이미지 레이블 -->
  <text x="190" y="105" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor" opacity="0.5">텍스처 이미지</text>

  <!-- (0.5, 0.5) 점 -->
  <circle cx="190" cy="148" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="190" cy="148" r="2" fill="currentColor"/>
  <text x="205" y="142" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(0.5, 0.5)</text>

  <!-- 축 눈금 레이블 -->
  <text x="55" y="265" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">0</text>
  <text x="55" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">1</text>
  <text x="60" y="275" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">0</text>
  <text x="320" y="275" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">1</text>
</svg>
</div>

<br>

U와 V라는 이름은, 3D 공간 좌표인 X, Y, Z와 구분하기 위해 알파벳 순서상 바로 앞 글자를 택한 것입니다.

### 정점에 UV 좌표 부여

Part 1에서 메쉬의 정점이 위치(x, y, z) 외에 법선, 색상 등 추가 데이터를 가진다고 했습니다. UV 좌표도 이러한 추가 데이터 중 하나로, 각 정점에 (u, v) 값을 지정하여 해당 정점이 텍스처의 어느 위치를 참조할지를 결정합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- 왼쪽: 3D 메쉬의 삼각형 -->
  <text x="130" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">3D 메쉬의 삼각형</text>

  <!-- 삼각형 -->
  <polygon points="130,40 30,170 230,170" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 정점 A -->
  <circle cx="130" cy="40" r="4" fill="currentColor"/>
  <text x="130" y="33" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">A</text>
  <text x="172" y="40" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(0.5, 1.0)</text>

  <!-- 정점 B -->
  <circle cx="30" cy="170" r="4" fill="currentColor"/>
  <text x="16" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">B</text>
  <text x="20" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(0, 0)</text>

  <!-- 정점 C -->
  <circle cx="230" cy="170" r="4" fill="currentColor"/>
  <text x="244" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">C</text>
  <text x="240" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">(1, 0)</text>

  <!-- 오른쪽: 2D 텍스처 UV 공간 -->
  <text x="460" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2D 텍스처</text>

  <!-- V축 -->
  <line x1="340" y1="180" x2="340" y2="32" stroke="currentColor" stroke-width="1.2"/>
  <text x="330" y="38" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">V</text>

  <!-- U축 -->
  <line x1="340" y1="180" x2="580" y2="180" stroke="currentColor" stroke-width="1.2"/>
  <text x="585" y="184" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">U</text>

  <!-- 텍스처 영역 -->
  <rect x="340" y="40" width="230" height="140" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>

  <!-- 텍스처 내 삼각형 -->
  <polygon points="455,40 340,180 570,180" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3,2"/>

  <!-- 텍스처 내 정점 A -->
  <circle cx="455" cy="40" r="4" fill="currentColor"/>
  <text x="470" y="37" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">A</text>

  <!-- 텍스처 내 정점 B -->
  <circle cx="340" cy="180" r="4" fill="currentColor"/>
  <text x="348" y="195" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">B</text>

  <!-- 텍스처 내 정점 C -->
  <circle cx="570" cy="180" r="4" fill="currentColor"/>
  <text x="563" y="195" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">C</text>

  <!-- 축 눈금 -->
  <text x="335" y="195" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">0</text>
  <text x="335" y="48" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">1</text>
  <text x="340" y="205" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">0</text>
  <text x="570" y="205" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">1</text>

  <!-- 하단 정점 데이터 -->
  <text x="300" y="230" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">정점 A: 위치(x,y,z) + UV(0.5, 1.0)</text>
  <text x="300" y="248" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">정점 B: 위치(x,y,z) + UV(0.0, 0.0)</text>
  <text x="300" y="266" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">정점 C: 위치(x,y,z) + UV(1.0, 0.0)</text>
</svg>
</div>

<br>

삼각형 내부의 각 픽셀은 세 정점의 UV 좌표를 **보간(Interpolation)**하여 텍스처의 어느 텍셀을 읽을지 계산합니다.
삼각형 한가운데에 위치한 픽셀이라면 세 정점의 UV 좌표를 거리 비율에 따라 가중 평균하여 고르게 섞인 값을 사용하고, 한쪽 정점에 가까운 픽셀일수록 해당 정점의 UV 좌표에 더 가까운 값을 사용합니다.

### 표면을 펼쳐놓는 것과 같다

UV 매핑은 3D 캐릭터 모델의 표면을 가위로 잘라 납작하게 펼쳐놓는 과정과 같습니다.
펼쳐진 평면이 UV 공간이고, 그 위에 무늬를 입힌 것이 텍스처입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 148" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <defs>
    <pattern id="uvFacePat" x="0" y="0" width="16" height="10" patternUnits="userSpaceOnUse">
      <rect width="16" height="10" fill="currentColor" fill-opacity="0.06"/>
      <line x1="0" y1="5" x2="16" y2="5" stroke="currentColor" stroke-width="0.4" opacity="0.18"/>
      <line x1="8" y1="0" x2="8" y2="5" stroke="currentColor" stroke-width="0.4" opacity="0.18"/>
      <line x1="0" y1="5" x2="0" y2="10" stroke="currentColor" stroke-width="0.4" opacity="0.18"/>
      <line x1="16" y1="5" x2="16" y2="10" stroke="currentColor" stroke-width="0.4" opacity="0.18"/>
    </pattern>
  </defs>

  <!-- ===== 1. 3D 표면 ===== -->
  <text x="95" y="16" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3D 표면</text>
  <!-- 등각 큐브 — 3면 명암 구분 -->
  <polygon points="60,40 95,27 130,40 95,53" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="60,40 95,53 95,93 60,80" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="95,53 130,40 130,80 95,93" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <!-- 정점 -->
  <circle cx="60" cy="40" r="2" fill="currentColor" opacity="0.4"/>
  <circle cx="95" cy="27" r="2" fill="currentColor" opacity="0.4"/>
  <circle cx="130" cy="40" r="2" fill="currentColor" opacity="0.4"/>
  <circle cx="60" cy="80" r="2" fill="currentColor" opacity="0.4"/>
  <circle cx="95" cy="53" r="2" fill="currentColor" opacity="0.4"/>
  <circle cx="95" cy="93" r="2" fill="currentColor" opacity="0.4"/>
  <circle cx="130" cy="80" r="2" fill="currentColor" opacity="0.4"/>
  <text x="95" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">정점마다 (u, v) 좌표</text>

  <!-- ===== 화살표 1 ===== -->
  <line x1="140" y1="60" x2="180" y2="60" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="185,60 177,55 177,65" fill="currentColor"/>
  <text x="163" y="52" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">펼침</text>

  <!-- ===== 2. UV 공간 ===== -->
  <text x="295" y="16" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">UV 공간</text>
  <!-- UV 영역 외곽 -->
  <rect x="195" y="26" width="200" height="92" rx="2" fill="currentColor" fill-opacity="0.02" stroke="currentColor" stroke-width="1.2"/>
  <!-- 6면 전개도 (1-4-1 배치) — 텍스처 패턴 채움 -->
  <polygon points="295,30 323,30 323,58 351,58 351,86 323,86 323,114 295,114 295,86 239,86 239,58 295,58"
    fill="url(#uvFacePat)" stroke="currentColor" stroke-width="1"/>
  <!-- 접는 선 (5개 — 6면을 구분) -->
  <line x1="295" y1="58" x2="323" y2="58" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2,2" opacity="0.35"/>
  <line x1="295" y1="86" x2="323" y2="86" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2,2" opacity="0.35"/>
  <line x1="267" y1="58" x2="267" y2="86" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2,2" opacity="0.35"/>
  <line x1="295" y1="58" x2="295" y2="86" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2,2" opacity="0.35"/>
  <line x1="323" y1="58" x2="323" y2="86" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2,2" opacity="0.35"/>
  <!-- 좌표 표시 -->
  <text x="195" y="130" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.35">(0, 0)</text>
  <text x="373" y="23" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.35">(1, 1)</text>

  <!-- ===== 화살표 2 ===== -->
  <line x1="405" y1="60" x2="435" y2="60" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="440,60 432,55 432,65" fill="currentColor"/>
  <text x="423" y="52" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">매핑</text>

  <!-- ===== 3. 매핑 결과 ===== -->
  <text x="500" y="16" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">매핑 결과</text>
  <!-- 텍스처가 입혀진 큐브 — 패턴 + 면별 명암 -->
  <polygon points="465,40 500,27 535,40 500,53" fill="url(#uvFacePat)" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="465,40 500,53 500,93 465,80" fill="url(#uvFacePat)" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="465,40 500,53 500,93 465,80" fill="currentColor" fill-opacity="0.03"/>
  <polygon points="500,53 535,40 535,80 500,93" fill="url(#uvFacePat)" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="500,53 535,40 535,80 500,93" fill="currentColor" fill-opacity="0.06"/>
  <text x="500" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">텍스처가 입혀진 표면</text>
</svg>
</div>

<br>

UV 펼치기는 보통 모델링 소프트웨어(Blender, Maya 등)에서 이루어지며, 그 결과 각 정점에 UV 좌표가 저장됩니다. Unity는 모델을 임포트할 때 이 UV 좌표를 그대로 사용합니다.

---

## 텍스처 해상도와 메모리

텍스처의 해상도가 높을수록 표면이 선명하게 보이지만, 텍셀 수가 그만큼 늘어나므로 GPU 메모리도 많이 차지합니다. 해상도에 따라 메모리가 어떻게 달라지는지 구체적으로 계산해 봅니다.

### RGBA 32bit 기준 메모리 계산

RGBA 32비트 형식은 텍셀 하나에 빨강(R), 초록(G), 파랑(B), 투명도(A) 네 채널을 각각 8비트(1바이트)씩, 총 4바이트로 저장합니다. 텍스처의 메모리 사용량은 가로 x 세로 x 텍셀당 바이트 수로 계산합니다.

<br>

```
메모리 = 가로 x 세로 x 텍셀당 바이트 수

512  x  512  x 4 =    1,048,576 바이트 =   1 MB
1024 x 1024  x 4 =    4,194,304 바이트 =   4 MB
2048 x 2048  x 4 =   16,777,216 바이트 =  16 MB
4096 x 4096  x 4 =   67,108,864 바이트 =  64 MB
```

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 제목 -->
  <text x="230" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">해상도에 따른 메모리 증가 (RGBA 32bit, 비압축)</text>
  <!-- Y축 레이블 -->
  <text x="16" y="140" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6" transform="rotate(-90,16,140)">메모리 (MB)</text>
  <!-- Y축 눈금 및 보조선 -->
  <text x="50" y="48" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">64</text>
  <line x1="54" y1="45" x2="400" y2="45" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <text x="50" y="138" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">32</text>
  <line x1="54" y1="135" x2="400" y2="135" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <text x="50" y="183" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">16</text>
  <line x1="54" y1="180" x2="400" y2="180" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <!-- Y축 -->
  <line x1="57" y1="38" x2="57" y2="235" stroke="currentColor" stroke-width="1.5"/>
  <!-- X축 -->
  <line x1="57" y1="235" x2="400" y2="235" stroke="currentColor" stroke-width="1.5"/>
  <!-- 막대 1: 512x512 = 1 MB -->
  <rect x="80" y="232" width="50" height="3" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="105" y="227" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">1</text>
  <text x="105" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">512x512</text>
  <!-- 막대 2: 1024x1024 = 4 MB -->
  <rect x="165" y="223" width="50" height="12" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">4</text>
  <text x="190" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">1024x1024</text>
  <!-- 막대 3: 2048x2048 = 16 MB -->
  <rect x="250" y="187" width="50" height="48" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="275" y="182" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">16</text>
  <text x="275" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">2048x2048</text>
  <!-- 막대 4: 4096x4096 = 64 MB -->
  <rect x="335" y="45" width="50" height="190" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="360" y="40" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">64</text>
  <text x="360" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">4096x4096</text>
  <!-- X축 레이블 -->
  <text x="230" y="272" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">해상도</text>
</svg>
</div>

<br>

가로와 세로가 각각 두 배가 되면 텍셀 수는 네 배가 됩니다. 1024x1024에서 2048x2048로 올리면 메모리가 4MB에서 16MB로 네 배 증가하고, 2048x2048에서 4096x4096으로 올리면 16MB에서 64MB로 또 네 배 증가합니다.

### 모바일에서 텍스처 메모리의 비중

모바일 기기의 GPU가 사용할 수 있는 메모리는 데스크톱에 비해 제한적입니다.
데스크톱 GPU는 전용 비디오 메모리(**VRAM**)를 수 GB 이상 갖추고 있지만, 모바일 GPU는 CPU와 메모리를 공유하는 구조이므로 텍스처에 할당할 수 있는 용량이 훨씬 적습니다.

이런 환경에서 텍스처는 전체 GPU 메모리 사용량의 50~70%를 차지하는 경우가 흔합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">모바일 게임의 GPU 메모리 분포 (전형적인 예시)</text>
  <!-- 항목 1: 텍스처 60% -->
  <text x="110" y="55" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">텍스처</text>
  <rect x="120" y="40" width="276" height="22" rx="3" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="404" y="56" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">60%</text>
  <!-- 항목 2: 메쉬 버퍼 15% -->
  <text x="110" y="90" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">메쉬 버퍼</text>
  <rect x="120" y="75" width="69" height="22" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="197" y="91" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">15%</text>
  <!-- 항목 3: 렌더 타깃 15% -->
  <text x="110" y="125" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">렌더 타깃</text>
  <rect x="120" y="110" width="69" height="22" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="197" y="126" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">15%</text>
  <!-- 항목 4: 셰이더, 기타 10% -->
  <text x="110" y="160" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">셰이더, 기타</text>
  <rect x="120" y="145" width="46" height="22" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="174" y="161" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">10%</text>
  <!-- 100% 기준선 (점선) -->
  <line x1="396" y1="35" x2="396" y2="172" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.25"/>
  <text x="396" y="185" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">100%</text>
</svg>
</div>

<br>

캐릭터 하나에도 **Diffuse**(기본 색상), **Normal**(표면 굴곡), **Mask**(재질 구분) 등 여러 장의 텍스처가 필요합니다. 
앞서 계산한 수치를 적용하면, 2048x2048 비압축 텍스처 한 장이 16MB이므로 캐릭터 한 명에 3장이면 48MB, 화면에 캐릭터가 5명이면 240MB입니다. 여기에 배경과 이펙트까지 더하면 모바일 기기에서는 감당하기 어려운 수치가 됩니다.

텍스처의 메모리 사용량을 줄이는 대표적인 방법으로 밉맵과 텍스처 압축이 있습니다.

---

## 밉맵(Mipmap) — 거리에 따른 텍스처 최적화

화면에 작게 보이는 오브젝트에도 원본 고해상도 텍스처를 그대로 사용하면 메모리 외에 다른 문제가 발생합니다.

### 멀리 있는 오브젝트의 문제

2048x2048 텍스처를 가진 오브젝트가 카메라에서 멀어져 화면에서 50x50 픽셀 크기로 그려진다고 가정합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 왼쪽: 2048x2048 텍스처 -->
  <text x="100" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2048 x 2048 텍스처</text>
  <rect x="15" y="28" width="170" height="170" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="105" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">약 420만 개의</text>
  <text x="100" y="121" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">텍셀</text>

  <!-- 오른쪽 영역 -->
  <text x="380" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">화면에 표시되는 크기</text>

  <!-- 오른쪽: 50x50 픽셀 (비율 반영 — 170 × 50/2048 ≈ 4px) -->
  <rect x="370" y="32" width="6" height="6" rx="1" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="382" y="39" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">50 x 50 픽셀</text>

  <!-- 오른쪽 주석 -->
  <text x="310" y="75" font-family="sans-serif" font-size="10" fill="currentColor">화면에 필요한 픽셀:</text>
  <text x="310" y="90" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2,500개</text>

  <line x1="310" y1="105" x2="500" y2="105" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <text x="310" y="125" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU는 2,500개의 픽셀을 채우기 위해</text>
  <text x="310" y="140" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">420만 텍셀이 저장된 텍스처에서</text>
  <text x="310" y="155" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">넓은 영역을 샘플링해야 함</text>

  <!-- 화살표: 큰 박스에서 작은 박스 방향 -->
  <line x1="200" y1="55" x2="362" y2="35" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4"/>
  <polygon points="367,34 357,30 358,40" fill="currentColor" opacity="0.4"/>
</svg>
</div>

<br>

화면의 한 픽셀이 텍스처의 수십 개 텍셀에 대응되므로, GPU는 그중 어떤 값을 사용할지 결정해야 합니다. 이 불균형이 두 가지 문제를 일으킵니다.

첫째, **에일리어싱(Aliasing)**입니다.
화면 픽셀 하나에 대응되는 텍셀이 너무 많으면, 카메라가 조금만 움직여도 참조하는 텍셀이 크게 바뀝니다. 이로 인해 텍스처가 깜빡이거나, 규칙적인 간섭 무늬인 모아레(Moire) 패턴이 나타납니다.

둘째, **대역폭 낭비**입니다.
GPU가 텍스처에서 텍셀 값을 읽어오는 행위를 **텍스처 샘플링(Texture Sampling)**이라 합니다. 샘플링은 GPU 메모리에서 데이터를 가져오는 작업이므로, GPU가 초당 전송할 수 있는 데이터량인 **메모리 대역폭(Memory Bandwidth)**을 소모합니다.
화면에 50×50 픽셀로 보이는 오브젝트를 위해 2048×2048 텍스처의 넓은 영역을 샘플링하면, 실제 필요한 것보다 훨씬 많은 텍셀을 읽게 되어 대역폭이 낭비됩니다. GPU 내부의 **텍스처 캐시(Texture Cache)**는 인접한 텍셀을 한 번에 읽어 재사용하도록 설계되어 있는데, 넓은 영역에서 듬성듬성 텍셀을 가져오면 캐시 적중률이 떨어져 메모리 읽기가 추가로 발생하고 대역폭 소비가 더 늘어납니다.

### 밉맵의 원리

**밉맵(Mipmap)**은 원본 텍스처의 축소 버전을 미리 만들어 두어 이 두 문제를 동시에 해결합니다.

>? Mip은 라틴어 "multum in parvo(작은 공간에 많은 것)"의 약자입니다.

<br>

**밉맵 체인 (Mip Chain)**

| Level | 해상도 |
|-------|--------|
| Level 0 | 2048 x 2048 (원본) |
| Level 1 | 1024 x 1024 |
| Level 2 | 512 x 512 |
| Level 3 | 256 x 256 |
| Level 4 | 128 x 128 |
| Level 5 | 64 x 64 |
| Level 6 | 32 x 32 |
| Level 7 | 16 x 16 |
| Level 8 | 8 x 8 |
| Level 9 | 4 x 4 |
| Level 10 | 2 x 2 |
| Level 11 | 1 x 1 |

각 레벨은 이전 레벨에서 인접한 4개의 텍셀을 평균하여 1개로 합쳐 가로와 세로를 절반씩 줄이며, 1×1이 될 때까지 이 과정을 반복합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- ===== Level 0 (4×4): 160×120, 셀 40×30 ===== -->
  <text x="90" y="18" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 0 (4×4)</text>
  <!-- 2×2 그룹 배경 (체커보드로 그룹 구분) -->
  <rect x="10" y="28" width="80" height="60" fill="currentColor" fill-opacity="0.09"/>
  <rect x="90" y="28" width="80" height="60" fill="currentColor" fill-opacity="0.03"/>
  <rect x="10" y="88" width="80" height="60" fill="currentColor" fill-opacity="0.03"/>
  <rect x="90" y="88" width="80" height="60" fill="currentColor" fill-opacity="0.09"/>
  <!-- 외곽선 -->
  <rect x="10" y="28" width="160" height="120" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- 그룹 경계선 (굵게) -->
  <line x1="90" y1="28" x2="90" y2="148" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
  <line x1="10" y1="88" x2="170" y2="88" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
  <!-- 셀 구분선 (가늘게) -->
  <line x1="50" y1="28" x2="50" y2="148" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="130" y1="28" x2="130" y2="148" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="10" y1="58" x2="170" y2="58" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="10" y1="118" x2="170" y2="118" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- 행 0 -->
  <text x="30" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">10</text>
  <text x="70" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">20</text>
  <text x="110" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">60</text>
  <text x="150" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">80</text>
  <!-- 행 1 -->
  <text x="30" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">30</text>
  <text x="70" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">40</text>
  <text x="110" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">40</text>
  <text x="150" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">60</text>
  <!-- 행 2 -->
  <text x="30" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">50</text>
  <text x="70" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">60</text>
  <text x="110" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">30</text>
  <text x="150" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">10</text>
  <!-- 행 3 -->
  <text x="30" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">70</text>
  <text x="70" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">80</text>
  <text x="110" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">50</text>
  <text x="150" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">30</text>

  <!-- 화살표 1 -->
  <line x1="180" y1="88" x2="218" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="223,88 213,83 213,93" fill="currentColor"/>

  <!-- ===== Level 1 (2×2): 80×60, 셀 40×30 ===== -->
  <text x="275" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 1 (2×2)</text>
  <rect x="235" y="58" width="80" height="60" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <line x1="275" y1="58" x2="275" y2="118" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="235" y1="88" x2="315" y2="88" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <text x="255" y="79" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">25</text>
  <text x="295" y="79" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">60</text>
  <text x="255" y="109" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">65</text>
  <text x="295" y="109" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">30</text>

  <!-- 화살표 2 -->
  <line x1="325" y1="88" x2="363" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="368,88 358,83 358,93" fill="currentColor"/>

  <!-- ===== Level 2 (1×1): 40×30, 셀 40×30 ===== -->
  <text x="400" y="63" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 2 (1×1)</text>
  <rect x="380" y="73" width="40" height="30" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="93" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">45</text>

  <!-- 수식 -->
  <text x="230" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(10+20+30+40) / 4 = 25</text>
  <text x="230" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(25+60+65+30) / 4 = 45</text>
</svg>
</div>

### 밉맵 레벨 선택

밉맵 체인이 준비되면, GPU는 **화면 픽셀 하나가 텍스처의 텍셀 몇 개에 대응하는지**를 기준으로 밉맵 레벨을 선택합니다.
인접한 화면 픽셀 사이의 UV 변화량에 텍스처 해상도를 곱하면 픽셀 하나가 커버하는 텍셀 수가 되며, 이 비율이 1:1에 가장 가까운 레벨을 택합니다.

<br>

앞서 예로 든 2048×2048 텍스처가 화면에서 50×50 픽셀로 보이는 경우, 픽셀당 텍셀 수는 약 2048 / 50 ≈ 41개입니다. 밉맵 레벨은 log₂(41) ≈ 5.4이므로 Level 5(64×64)가 선택됩니다. 이 레벨에서 픽셀당 텍셀 비율은 64 / 50 ≈ 1.3으로 거의 1:1에 가깝습니다.
이 계산은 GPU 하드웨어가 픽셀마다 자동으로 수행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">카메라와의 거리에 따른 밉맵 레벨 선택</text>

  <!-- 거리 축 -->
  <text x="40" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">가까움</text>
  <text x="480" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">멀리</text>
  <line x1="20" y1="50" x2="500" y2="50" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="505,50 495,45 495,55" fill="currentColor"/>

  <!-- 눈금 마커 -->
  <line x1="60" y1="46" x2="60" y2="54" stroke="currentColor" stroke-width="1.5"/>
  <line x1="195" y1="46" x2="195" y2="54" stroke="currentColor" stroke-width="1.5"/>
  <line x1="330" y1="46" x2="330" y2="54" stroke="currentColor" stroke-width="1.5"/>
  <line x1="460" y1="46" x2="460" y2="54" stroke="currentColor" stroke-width="1.5"/>

  <!-- Level 0: 60×60 정사각형, 하단 정렬 y=130 -->
  <rect x="30" y="70" width="60" height="60" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="143" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 0</text>
  <text x="60" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">2048×2048</text>

  <!-- Level 2: 40×40 정사각형, 하단 정렬 y=130 -->
  <rect x="175" y="90" width="40" height="40" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="195" y="143" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 2</text>
  <text x="195" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">512×512</text>

  <!-- Level 5: 24×24 정사각형, 하단 정렬 y=130 -->
  <rect x="318" y="106" width="24" height="24" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="143" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 5</text>
  <text x="330" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">64×64</text>

  <!-- Level 8: 12×12 정사각형, 하단 정렬 y=130 -->
  <rect x="454" y="118" width="12" height="12" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="143" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Level 8</text>
  <text x="460" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">8×8</text>

  <!-- 하단 요약 -->
  <text x="260" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">화면에서 작아질수록 더 축소된 밉맵 레벨 사용</text>
</svg>
</div>

<br>

적절한 밉맵 레벨을 사용하면 화면 픽셀 하나에 대응되는 텍셀 수가 줄어들어, 앞서 지적한 두 문제가 동시에 해소됩니다. 에일리어싱이 감소하고, 읽어야 하는 텍스처 영역이 좁아져 캐시 효율이 올라갑니다.

### 밉맵의 메모리 비용

밉맵은 원본 외에 축소 버전을 추가로 저장하므로 메모리가 늘어납니다. 각 레벨은 가로와 세로가 모두 절반이므로 면적은 이전 레벨의 1/4입니다. Level 1은 원본의 1/4, Level 2는 그 1/4인 1/16, Level 3은 그 1/4인 1/64 ... 이런 식으로 계속 줄어듭니다. 이 값들을 모두 더하면 원본의 약 **33%**(1/3)가 됩니다.

<br>

**밉맵 추가 메모리 계산**

원본 면적을 1이라 하면 (가로 비율의 제곱 = 면적 비율):

$$
\text{Level 1: 가로 } \frac{1}{2} \rightarrow \text{면적 } \left(\frac{1}{2}\right)^{2} = \frac{1}{4}
$$

$$
\text{Level 2: 가로 } \frac{1}{4} \rightarrow \text{면적 } \left(\frac{1}{4}\right)^{2} = \frac{1}{16}
$$

$$
\text{Level 3: 가로 } \frac{1}{8} \rightarrow \text{면적 } \left(\frac{1}{8}\right)^{2} = \frac{1}{64}
$$

$$
\cdots
$$

{% raw %}
$$
\begin{aligned}
\text{합계} &= \frac{1}{4} + \frac{1}{16} + \frac{1}{64} + \frac{1}{256} + \cdots \\[6pt]
&= \frac{1}{4} \times \left(1 + \frac{1}{4} + \frac{1}{16} + \cdots\right) \\[6pt]
&= \frac{1}{4} \times \frac{1}{1 - \frac{1}{4}} = \frac{1}{4} \times \frac{4}{3} = \frac{1}{3} \approx 0.333 \text{ (약 33\%)}
\end{aligned}
$$
{% endraw %}

<br>

**2048×2048 RGBA 비압축 텍스처의 경우:**

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 75" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 원본 16.00 MB -->
  <rect x="10" y="12" width="270" height="30" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="145" y="32" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">원본 16.00 MB</text>
  <!-- 밉맵 추가분 +5.33 MB -->
  <rect x="280" y="12" width="90" height="30" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="325" y="32" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">+5.33 MB</text>
  <!-- 총합 -->
  <line x1="10" y1="52" x2="370" y2="52" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="190" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">밉맵 포함 총합: 21.33 MB</text>
</svg>
</div>

메모리가 33% 늘어나는 대신, 앞에서 살펴본 에일리어싱과 대역폭 낭비가 해결됩니다. 밉맵이 절약하는 대역폭은 추가 메모리 33%를 상쇄하고도 남으므로, 대부분의 게임 엔진은 밉맵을 기본으로 생성합니다.

<br>

다만 모든 텍스처에 밉맵이 필요한 것은 아닙니다. UI 텍스처나, 카메라 줌 없이 고정 크기로 표시되는 2D 스프라이트처럼 화면에서 축소될 일이 없는 텍스처는 밉맵을 끄면 33%의 메모리를 절약할 수 있습니다.

---

## 텍스처 압축 — 모바일의 필수 기술

밉맵이 대역폭을 절약하는 기법이었다면, **텍스처 압축**은 메모리와 대역폭을 동시에 줄이는 기법입니다. 텍스처는 일반적으로 GPU 메모리에서 큰 비중을 차지하는 에셋이며, 텍스처 압축은 이 메모리 사용량을 1/4~1/8로 줄입니다.

### GPU 텍스처 압축의 특징

PNG나 JPEG 같은 일반 이미지 압축과 GPU 텍스처 압축은 설계 목적이 다릅니다.
GPU는 렌더링 중 텍스처의 임의의 위치에서 텍셀을 읽어야 하는데, PNG/JPEG는 이미지 전체를 순차적으로 압축하므로 특정 텍셀만 읽으려면 전체를 비압축 상태로 풀어야(디코딩) 합니다.
풀어낸 비압축 데이터가 GPU 메모리에 그대로 올라가므로, 디스크 저장 크기는 줄어들어도 GPU 메모리는 절약되지 않습니다.

GPU 텍스처 압축(ASTC, ETC2 등)은 텍스처를 4×4 같은 고정 크기의 블록으로 나누어 압축하며, 각 블록이 독립적이므로 GPU가 임의의 텍셀을 읽을 때 해당 블록만 처리하면 됩니다. **전체를 디코딩할 필요가 없으므로 텍스처는 압축된 상태 그대로 GPU 메모리에 올라가며, GPU 하드웨어의 내장 디코더가 필요한 블록만 실시간으로 디코딩합니다.**

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- 상단: 일반 이미지 압축 (PNG/JPEG) -->
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">일반 이미지 압축 (PNG/JPEG)</text>

  <!-- 디스크 박스 -->
  <rect x="20" y="34" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="54" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">디스크</text>
  <text x="80" y="72" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">PNG 압축 2 MB</text>

  <!-- 화살표 1 -->
  <line x1="140" y1="59" x2="195" y2="59" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,59 190,54 190,64" fill="currentColor"/>

  <!-- CPU 디코딩 박스 -->
  <rect x="200" y="34" width="140" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="54" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">CPU에서 디코딩</text>
  <text x="270" y="72" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">비압축 풀기</text>

  <!-- 화살표 2 -->
  <line x1="340" y1="59" x2="405" y2="59" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="410,59 400,54 400,64" fill="currentColor"/>

  <!-- GPU 메모리 박스 (큰 크기 강조) -->
  <rect x="410" y="30" width="150" height="58" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="2"/>
  <text x="485" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU 메모리</text>
  <text x="485" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">비압축 16 MB</text>

  <!-- 메모리 절약 없음 -->
  <text x="485" y="106" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메모리 절약 없음</text>

  <!-- 구분선 -->
  <line x1="40" y1="128" x2="540" y2="128" stroke="currentColor" stroke-width="0.5" stroke-dasharray="6,4" opacity="0.3"/>

  <!-- 하단: GPU 텍스처 압축 (ASTC/ETC2) -->
  <text x="290" y="156" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU 텍스처 압축 (ASTC/ETC2)</text>

  <!-- 디스크 박스 -->
  <rect x="20" y="172" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">디스크</text>
  <text x="80" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">ASTC 4 MB</text>

  <!-- 긴 화살표 (직접 전송) -->
  <line x1="140" y1="197" x2="405" y2="197" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="410,197 400,192 400,202" fill="currentColor"/>
  <text x="270" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">그대로 올림</text>

  <!-- GPU 메모리 박스 -->
  <rect x="410" y="172" width="150" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="485" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU 메모리</text>
  <text x="485" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">ASTC 압축 4 MB</text>

  <!-- 메모리 절약됨 + GPU 하드웨어 -->
  <text x="485" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메모리 절약됨</text>
  <text x="485" y="254" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">GPU 하드웨어가 직접 읽음</text>
</svg>
</div>

### 블록 압축의 원리

대부분의 GPU 텍스처 압축 포맷은 텍스처를 작은 블록(일반적으로 4×4 텍셀)으로 나누고 각 블록을 고정된 크기의 데이터로 압축하는 **블록 압축(Block Compression)** 방식을 사용합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2048 x 2048 텍스처를 4x4 블록으로 분할</text>

  <!-- 왼쪽: 큰 격자 (일부만 표시) -->
  <rect x="30" y="38" width="160" height="160" rx="3" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>

  <!-- 세로 구분선 -->
  <line x1="50" y1="38" x2="50" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="70" y1="38" x2="70" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="90" y1="38" x2="90" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="110" y1="38" x2="110" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="130" y1="38" x2="130" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="150" y1="38" x2="150" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="170" y1="38" x2="170" y2="198" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>

  <!-- 가로 구분선 -->
  <line x1="30" y1="58" x2="190" y2="58" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="30" y1="78" x2="190" y2="78" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="30" y1="98" x2="190" y2="98" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="30" y1="118" x2="190" y2="118" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="30" y1="138" x2="190" y2="138" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="30" y1="158" x2="190" y2="158" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <line x1="30" y1="178" x2="190" y2="178" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>

  <!-- "..." 표시 -->
  <text x="196" y="125" font-family="sans-serif" font-size="14" fill="currentColor" opacity="0.4">...</text>
  <text x="110" y="212" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">...</text>

  <!-- 강조 블록 (왼쪽 위 한 블록) -->
  <rect x="30" y="38" width="20" height="20" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>

  <!-- 블록 수 레이블 -->
  <text x="110" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">512 x 512 = 262,144 개 블록</text>

  <!-- 확대 화살표 -->
  <line x1="52" y1="48" x2="290" y2="68" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <polygon points="295,67 285,63 286,72" fill="currentColor"/>

  <!-- 오른쪽: 확대된 4x4 블록 -->
  <text x="420" y="44" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">하나의 블록 (4 x 4)</text>

  <!-- 블록 외곽 -->
  <rect x="300" y="56" width="240" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 가로 구분선 -->
  <line x1="300" y1="101" x2="540" y2="101" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="300" y1="146" x2="540" y2="146" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="300" y1="191" x2="540" y2="191" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>

  <!-- 세로 구분선 -->
  <line x1="360" y1="56" x2="360" y2="236" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="420" y1="56" x2="420" y2="236" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <line x1="480" y1="56" x2="480" y2="236" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>

  <!-- 셀 레이블: 행 0 -->
  <text x="330" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P0</text>
  <text x="390" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P1</text>
  <text x="450" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P2</text>
  <text x="510" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P3</text>

  <!-- 셀 레이블: 행 1 -->
  <text x="330" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P4</text>
  <text x="390" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P5</text>
  <text x="450" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P6</text>
  <text x="510" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P7</text>

  <!-- 셀 레이블: 행 2 -->
  <text x="330" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P8</text>
  <text x="390" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P9</text>
  <text x="450" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P10</text>
  <text x="510" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P11</text>

  <!-- 셀 레이블: 행 3 -->
  <text x="330" y="219" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P12</text>
  <text x="390" y="219" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P13</text>
  <text x="450" y="219" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P14</text>
  <text x="510" y="219" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">P15</text>

  <!-- 16 텍셀 레이블 -->
  <text x="420" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">16 텍셀</text>
</svg>
</div>

이 16개 텍셀을 RGBA(32bit, 텍셀당 4바이트)로 개별 저장하면 64바이트가 필요하지만, 블록 압축은 블록 내 색상 분포를 소수의 대표 정보와 텍셀별 선택 데이터로 압축하여 고정된 크기(예: 8 또는 16바이트)로 줄입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 120" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 비압축 바 -->
  <text x="240" y="16" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4×4 블록 압축 비교 (ETC2 RGBA)</text>
  <rect x="30" y="32" width="320" height="28" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="190" y="51" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">비압축: 16 텍셀 × 4 바이트 = 64 바이트</text>

  <!-- 압축 바 -->
  <rect x="30" y="72" width="80" height="28" rx="3" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1.2"/>
  <text x="70" y="91" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">16 바이트</text>

  <!-- 압축률 레이블 -->
  <text x="125" y="91" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">← 4:1 압축</text>
</svg>
</div>

<br>

압축된 블록의 크기가 모두 동일하므로, GPU는 임의의 텍셀이 속한 블록 번호에 블록 크기를 곱하는 것만으로 해당 블록의 메모리 위치를 계산할 수 있고, 전체 텍스처를 디코딩하지 않고도 필요한 텍셀에 바로 접근할 수 있습니다.

---

## 주요 텍스처 압축 포맷

블록 압축의 원리는 같지만, 구체적인 압축 포맷은 플랫폼과 GPU에 따라 다릅니다. Unity에서 주로 사용되는 포맷은 ETC2와 ASTC입니다.

### ETC2 (Ericsson Texture Compression 2)

ETC2는 OpenGL ES(모바일 GPU용 그래픽 API 표준) 3.0에 포함된 텍스처 압축 포맷입니다. OpenGL ES 3.0 이상을 지원하는 Android와 iOS 기기에서 하드웨어 디코딩이 가능합니다.

<br>

**ETC2 사양**

블록 크기: 4 x 4 텍셀 (고정)

| 모드 | 블록당 크기 | 텍셀당 크기 | bpp | 비압축 대비 |
|------|-------------|-------------|-----|-------------|
| RGB 모드 | 8 바이트/블록 | 0.5 바이트/텍셀 | 4 bpp | 24bpp → 4bpp (6:1) |
| RGBA 모드 | 16 바이트/블록 | 1.0 바이트/텍셀 | 8 bpp | 32bpp → 8bpp (4:1) |

\* bpp (bits per pixel): 텍셀당 비트 수. 비압축 RGB는 24bpp, RGBA는 32bpp

<br>

RGB 모드는 색상만 블록당 8바이트로 압축합니다.

RGBA 모드는 알파 채널을 별도의 8바이트 블록으로 추가 저장하므로, 블록당 8 + 8 = 16바이트가 됩니다.

<br>

ETC2는 블록 크기가 4×4로 고정이어서, 덜 중요한 텍스처의 품질을 낮춰 메모리를 더 절약하는 선택이 불가능합니다.

### ASTC (Adaptive Scalable Texture Compression)

**ASTC**는 ARM과 AMD가 공동 개발하고 Khronos Group이 표준화한 텍스처 압축 포맷입니다. iOS 8 이상, Android는 OpenGL ES 3.2 이상 또는 Vulkan을 지원하는 기기에서 하드웨어 디코딩이 가능합니다.

ETC2와 가장 큰 차이점은 개발자가 텍스처마다 블록 크기를 선택할 수 있다는 점입니다. 압축된 블록 하나는 블록 크기에 관계없이 항상 128비트(16바이트)이므로, 블록이 커지면 더 많은 텍셀이 같은 128비트를 나눠 쓰게 됩니다.
텍셀당 정밀도는 낮아지지만 bpp가 줄어들어 메모리가 절약됩니다.

<br>

**ASTC 주요 블록 크기별 bpp (모든 블록은 128비트 = 16바이트)**

| 블록 크기 | 텍셀 수 | bpp | 품질 |
|-----------|---------|------|------|
| 4 x 4 | 16 | 8.00 | 최고 |
| 5 x 5 | 25 | 5.12 | ↓ |
| 6 x 6 | 36 | 3.56 | ↓ |
| 8 x 8 | 64 | 2.00 | ↓ |
| 10 x 10 | 100 | 1.28 | ↓ |
| 12 x 12 | 144 | 0.89 | 최저 |

\* 이 외에 5x4, 6x5, 8x6 등 비정사각 블록도 지원

<br>

ETC2 RGBA는 16바이트를 RGB 8바이트 + 알파 8바이트로 고정 분할합니다. 알파가 단순한(대부분 불투명한) 텍스처라도 알파에 항상 8바이트가 할당되어 나머지 RGB에 쓸 수 없습니다. ASTC는 16바이트를 채널별로 고정 분할하지 않으므로, 알파가 단순하면 그만큼 RGB에 더 많은 비트를 써서 색상 품질을 높일 수 있습니다.

다만 블록 크기를 키워 메모리를 절약할수록 텍셀당 정밀도가 낮아지므로, 경계가 뭉개지거나 인접 블록 사이에 색상이 번지는 **압축 아티팩트(Compression Artifact)**가 나타날 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- 제목 -->
  <text x="250" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">블록 크기에 따른 품질-크기 트레이드오프</text>

  <!-- Y축 -->
  <line x1="70" y1="40" x2="70" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <text x="28" y="58" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">높음</text>
  <text x="28" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">낮음</text>
  <text x="28" y="140" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">품질</text>

  <!-- X축 -->
  <line x1="70" y1="230" x2="420" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">작음</text>
  <text x="400" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">큼</text>
  <text x="245" y="270" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">메모리 절약</text>

  <!-- 데이터 점: 4x4 (높은 품질, 적은 절약) -->
  <circle cx="105" cy="60" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="56" font-family="sans-serif" font-size="10" fill="currentColor">4x4</text>

  <!-- 데이터 점: 5x5 -->
  <circle cx="155" cy="90" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="86" font-family="sans-serif" font-size="10" fill="currentColor">5x5</text>

  <!-- 데이터 점: 6x6 -->
  <circle cx="210" cy="120" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="116" font-family="sans-serif" font-size="10" fill="currentColor">6x6</text>

  <!-- 데이터 점: 8x8 -->
  <circle cx="275" cy="150" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="146" font-family="sans-serif" font-size="10" fill="currentColor">8x8</text>

  <!-- 데이터 점: 10x10 -->
  <circle cx="340" cy="180" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="355" y="176" font-family="sans-serif" font-size="10" fill="currentColor">10x10</text>

  <!-- 데이터 점: 12x12 (낮은 품질, 많은 절약) -->
  <circle cx="395" cy="210" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1.5"/>
  <text x="380" y="206" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">12x12</text>

  <!-- 추세선 (점선) -->
  <line x1="105" y1="60" x2="395" y2="210" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.2"/>
</svg>
</div>

<br>

이 트레이드오프를 텍스처별로 조절할 수 있다는 점이 ASTC의 장점입니다. 캐릭터 얼굴처럼 시각적으로 중요한 텍스처에는 4×4나 5×5를, 먼 배경이나 반복 패턴에는 8×8이나 10×10을 선택할 수 있습니다.

### 포맷 비교와 선택

| 포맷 | 블록 크기 | bpp 범위 | 지원 기기 |
|------|-----------|----------|-----------|
| ETC2 | 4x4 고정 | 4 / 8 | Android + iOS (ES 3.0+) |
| ASTC | 4x4 ~ 12x12 가변 | 0.89 ~ 8.00 | Android + iOS (ES 3.2+ / Vulkan) |

Unity에서는 텍스처 Import Settings의 플랫폼별 탭에서 압축 포맷을 선택합니다. Android와 iOS 모두 ASTC를 지정하면 하나의 포맷으로 양 플랫폼을 지원할 수 있습니다.

---

## 텍스처 메모리 공식

텍스처의 메모리 사용량은 해상도, 포맷(bpp), 밉맵 여부로 결정됩니다.

> 큐브맵(×6), 텍스처 배열(×레이어 수), 3D 텍스처(×깊이) 등 다른 텍스처 유형에는 추가 요소가 있지만, 여기서는 일반 2D 텍스처만 다룹니다.

<br>

### 기본 공식

$$
\text{텍스처 메모리} = \text{가로} \times \text{세로} \times \frac{\text{bpp}}{8} \times \text{밉맵 계수}
$$

밉맵 계수:
- 밉맵 켜짐 = 1.33 (원본 + 33%)
- 밉맵 꺼짐 = 1.00 (원본만)

<br>

### 계산 예시

2048x2048 텍스처를 여러 포맷으로 저장했을 때의 메모리를 비교합니다.

<br>

**포맷별 메모리 비교 (2048 x 2048, 밉맵 포함)**

| 포맷 | bpp | 텍스처 크기 | 밉맵 포함 |
|------|-----|-------------|-----------|
| RGBA 비압축 | 32 | 16.00 MB | 21.33 MB |
| ETC2 RGB | 4 | 2.00 MB | 2.67 MB |
| ETC2 RGBA | 8 | 4.00 MB | 5.33 MB |
| ASTC 4x4 | 8 | 4.00 MB | 5.33 MB |
| ASTC 6x6 | 3.56 | 1.78 MB | 2.37 MB |
| ASTC 8x8 | 2 | 1.00 MB | 1.33 MB |

계산 과정 (ASTC 6x6 예시):

{% raw %}
$$
\begin{aligned}
& 2048 \times 2048 \times \frac{3.56}{8} \times 1.33 \\[4pt]
&= 4{,}194{,}304 \times 0.445 \times 1.33 \\[4pt]
&= 4{,}194{,}304 \times 0.592 \\[4pt]
&\approx 2{,}483{,}027 \text{ 바이트} \approx 2.37 \text{ MB}
\end{aligned}
$$
{% endraw %}

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">메모리 절약 비교 (2048 x 2048, 밉맵 포함)</text>

  <!-- 비압축 RGBA: 21.33 MB (기준, 100%) -->
  <text x="95" y="52" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">비압축 RGBA</text>
  <rect x="100" y="38" width="340" height="20" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="445" y="52" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">21.33 MB (기준)</text>

  <!-- ETC2 RGBA: 5.33 MB (75% 절약, ~25% of max) -->
  <text x="95" y="88" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">ETC2 RGBA</text>
  <rect x="100" y="74" width="85" height="20" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">5.33 MB (75% 절약)</text>

  <!-- ASTC 4x4: 5.33 MB (75% 절약) -->
  <text x="95" y="124" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">ASTC 4x4</text>
  <rect x="100" y="110" width="85" height="20" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="190" y="124" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">5.33 MB (75% 절약)</text>

  <!-- ASTC 6x6: 2.37 MB (89% 절약, ~11% of max) -->
  <text x="95" y="160" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">ASTC 6x6</text>
  <rect x="100" y="146" width="38" height="20" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="143" y="160" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">2.37 MB (89% 절약)</text>

  <!-- ASTC 8x8: 1.33 MB (94% 절약, ~6% of max) -->
  <text x="95" y="196" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">ASTC 8x8</text>
  <rect x="100" y="182" width="21" height="20" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="126" y="196" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">1.33 MB (94% 절약)</text>
</svg>
</div>

<br>

앞서 비압축 2048×2048 텍스처 기준으로 캐릭터 5명에 240MB가 필요하다고 계산했습니다. 여기에 밉맵을 포함하고 압축 포맷을 적용하면:

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 100" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="16" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">캐릭터 5명 텍스처 메모리 (2048×2048 × 3장 × 밉맵)</text>

  <!-- 비압축 RGBA: 320 MB -->
  <text x="95" y="46" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">비압축 RGBA</text>
  <rect x="100" y="32" width="320" height="22" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="425" y="47" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">약 320 MB</text>

  <!-- ASTC 6x6: 36 MB -->
  <text x="95" y="82" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">ASTC 6x6</text>
  <rect x="100" y="68" width="36" height="22" rx="3" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="141" y="83" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">약 36 MB</text>
</svg>
</div>

<br>

게임에는 캐릭터 외에도 배경, 이펙트, UI 등 수많은 텍스처가 필요하므로, 캐릭터 텍스처만으로 320MB를 사용하는 것은 현실적이지 않습니다. ASTC 6×6을 적용한 36MB라면 나머지 에셋에 충분한 여유를 남길 수 있습니다.

---

## 실전 가이드라인

프로젝트에서 텍스처를 설정할 때 참고할 기준입니다.

### 해상도 선택

텍스처 해상도는 오브젝트가 화면에서 차지하는 크기에 맞춰야 합니다.
화면에 100×100 픽셀로 보이는 오브젝트에 2048×2048 텍스처를 할당하면 메모리만 낭비됩니다. 밉맵이 렌더링 시 적절한 축소 레벨을 사용하더라도 원본 텍스처는 GPU 메모리에 그대로 남아 있으므로, 처음부터 해상도를 맞추는 것이 근본적인 해결입니다.

<br>

**화면 점유 크기에 따른 텍스처 해상도 가이드**

| 화면 점유 크기 | 권장 해상도 |
|----------------|-------------|
| 전체 화면 배경 | 1024 ~ 2048 |
| 주인공 캐릭터 | 1024 ~ 2048 |
| 일반 NPC / 소품 | 512 ~ 1024 |
| 먼 배경 오브젝트 | 256 ~ 512 |
| 파티클 / 이펙트 | 128 ~ 256 |

### 압축 포맷 선택

ASTC는 블록이 커질수록 bpp가 낮아져 텍스처 전체 메모리가 줄지만 품질도 낮아집니다. 텍스처 용도에 따라 블록 크기를 다르게 설정합니다.

<br>

**텍스처 용도에 따른 ASTC 블록 크기 가이드**

| 텍스처 용도 | 권장 ASTC 블록 | bpp |
|-------------|----------------|------|
| 캐릭터 얼굴 / 중요 UI | 4x4 | 8.00 |
| 캐릭터 몸체 / 무기 | 5x5 | 5.12 |
| 배경 건물 / 지형 | 6x6 | 3.56 |
| 먼 배경 / 스카이박스 | 8x8 | 2.00 |

### 밉맵 설정

밉맵은 약 33%의 추가 메모리를 사용하지만, 에일리어싱을 줄이고 대역폭을 절약합니다.
일반적으로 3D 공간에서 카메라와의 거리가 변하는 오브젝트에는 밉맵을 켜고, UI 요소나 고정 크기 스프라이트처럼 항상 같은 크기로 그려지는 텍스처에는 끄는 것이 효율적입니다.

### 2의 거듭제곱 크기

텍스처 크기는 128, 256, 512, 1024, 2048 등 2의 거듭제곱(Power of Two, POT)으로 설정하는 것이 좋습니다. POT로 설정하면 밉맵의 각 레벨이 정확히 절반으로 나뉘고, 4×4나 8×8 블록으로도 나누어떨어집니다.

비-POT(NPOT) 텍스처는 밉맵 레벨마다 크기가 정확히 절반이 되지 않아 반올림이 필요합니다.
ASTC와 ETC2는 POT를 요구하지 않지만, 블록 크기의 배수가 아니면 가장자리에 패딩이 추가됩니다.
특별한 이유가 없다면 POT로 설정하는 것이 안전합니다.

---

## 마무리

텍스처는 UV 좌표를 통해 메쉬 표면에 대응되는 2D 이미지이며, 해상도·밉맵·압축 포맷이 메모리 사용량을 결정합니다.

이 글에서 다룬 핵심을 정리하면 다음과 같습니다.

- 해상도가 두 배가 되면 메모리는 네 배로 늘어납니다
- 밉맵은 33%의 추가 메모리로 에일리어싱과 대역폭 낭비를 줄입니다
- GPU 텍스처 압축은 고정 크기 블록 단위로 압축하여 랜덤 접근을 유지하면서 메모리를 절약합니다
- ASTC는 텍스처마다 블록 크기를 선택할 수 있어 품질과 메모리의 균형을 조절할 수 있습니다
- 최종 메모리 사용량은 `가로 × 세로 × (bpp / 8) × 밉맵 계수`로 계산됩니다

Part 1에서 메쉬가 3D 형태를 정의했다면, 텍스처는 그 표면에 색과 질감을 입힙니다. 하지만 같은 메쉬와 텍스처라도 금속처럼 빛을 반사하거나 천처럼 흡수하는 등 표면의 반응이 다를 수 있습니다. 이 표면 반응을 GPU에서 계산하는 프로그램이 **셰이더(Shader)**입니다. Part 1에서 등장한 **버텍스 셰이더**는 정점의 위치를 화면 좌표로 변환하고, **프래그먼트 셰이더**는 각 픽셀의 최종 색상을 계산합니다. 이 글에서 다룬 텍스처는 프래그먼트 셰이더가 픽셀 색상을 결정할 때 참조하는 데이터입니다.

**머티리얼(Material)**은 어떤 셰이더를 사용할지 지정하고, 그 셰이더에 전달할 값(텍스처, 색상, 금속성, 거칠기 등)을 저장합니다. 하나의 셰이더를 여러 머티리얼이 공유할 수 있고, 각 머티리얼이 다른 값을 전달하면 금속, 나무, 천 등 서로 다른 표면을 표현할 수 있습니다. [Part 3](/dev/unity/RenderingFoundation-3/)에서 머티리얼과 셰이더의 구조를 살펴봅니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)

**시리즈**
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- **렌더링 기초 (2) - 텍스처와 압축 (현재 글)**
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- **렌더링 기초 (2) - 텍스처와 압축** (현재 글)
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
