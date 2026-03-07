---
layout: single
title: "렌더링 기초 (3) - 머티리얼과 셰이더 기초 - soo:bak"
date: "2026-02-13 01:00:00 +0900"
description: 머티리얼의 역할, 셰이더의 구조(버텍스/프래그먼트), 렌더 스테이트, 프로그래머블 셰이더의 역사를 설명합니다.
tags:
  - Unity
  - 최적화
  - 셰이더
  - 머티리얼
  - 모바일
---

## 머티리얼이란

[Part 1](/dev/unity/RenderingFoundation-1/)에서 메쉬가 정점과 삼각형으로 오브젝트의 형태를 정의하는 구조를, [Part 2](/dev/unity/RenderingFoundation-2/)에서 텍스처가 UV 좌표를 통해 표면에 색상과 디테일을 입히는 구조를 살펴보았습니다.
메쉬는 "어떤 모양인가"를 결정하고, 텍스처는 "표면에 입힐 이미지 데이터"를 담고 있습니다.

<br>

하지만 메쉬와 텍스처만으로는 렌더링을 완성할 수 없습니다.

같은 구(sphere) 메쉬에 같은 텍스처를 입히더라도, 표면이 빛을 금속처럼 반사할 수도 있고 천처럼 부드럽게 산란시킬 수도 있습니다.
메쉬의 형태 위에 텍스처를 어떤 방식으로 결합할 것인지, 빛이 표면에 닿았을 때 어떻게 반응할 것인지, 불투명하게 그릴 것인지 반투명하게 합성할 것인지 등을 결정하는 별도의 렌더링 규칙이 필요합니다.

<br>

이 렌더링 규칙을 정의하는 프로그램이 **셰이더(Shader)**이고, 특정 셰이더를 참조하면서 그 셰이더가 요구하는 파라미터 값들을 묶어 저장하는 데이터가 **머티리얼(Material)**입니다.

[Part 1](/dev/unity/RenderingFoundation-1/)의 메쉬, [Part 2](/dev/unity/RenderingFoundation-2/)의 텍스처, 그리고 이 글에서 다루는 머티리얼이 렌더링 파이프라인에 입력되는 세 가지 핵심 데이터입니다.

이 글에서는 머티리얼과 셰이더의 구조, 렌더 스테이트의 역할, 그리고 고정 파이프라인에서 프로그래머블 셰이더로의 발전 과정을 살펴봅니다.

<br>

머티리얼은 **셰이더**를 참조하면서, 셰이더가 요구하는 **파라미터** 값을 저장합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 셰이더 박스 (상단) -->
  <rect x="140" y="8" width="140" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셰이더</text>
  <!-- GPU 주석 -->
  <text x="300" y="34" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">GPU에서 실행되는 프로그램</text>
  <!-- 참조 화살표 (머티리얼 → 셰이더) -->
  <line x1="210" y1="88" x2="210" y2="56" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="205,58 210,50 215,58" fill="currentColor"/>
  <text x="222" y="76" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">참조</text>
  <!-- 머티리얼 외곽 박스 -->
  <rect x="30" y="88" width="360" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="114" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">머티리얼</text>
  <!-- 파라미터 박스 1행 -->
  <rect x="55" y="130" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="100" y="153" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">텍스처들</text>
  <rect x="165" y="130" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="210" y="153" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">색상</text>
  <rect x="275" y="130" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="320" y="153" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">반사도</text>
  <!-- 파라미터 박스 2행 -->
  <rect x="55" y="180" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="100" y="203" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">투명도</text>
  <rect x="165" y="180" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="210" y="203" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">노멀 강도</text>
  <rect x="275" y="180" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="320" y="203" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">기타</text>
</svg>
</div>

<br>

셰이더가 렌더링 규칙을 정의하고 머티리얼이 그 값을 저장하므로, 같은 메쉬에 서로 다른 머티리얼을 적용하면 동일한 형태의 오브젝트가 완전히 다른 외관을 갖게 됩니다.

예를 들어 구(sphere) 메쉬 하나에 금속 머티리얼을 적용하면 반짝이는 금속 구가 되고, 유리 머티리얼을 적용하면 투명한 유리 구가 됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 상단 제목 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">같은 메쉬 + 같은 셰이더, 다른 파라미터 → 다른 외관</text>
  <!-- === 금속 구 (상단) === -->
  <!-- 메쉬 박스 -->
  <rect x="30" y="50" width="90" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="95" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">구 메쉬</text>
  <text x="75" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(동일)</text>
  <!-- + 기호 -->
  <text x="140" y="105" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="bold" fill="currentColor">+</text>
  <!-- 파라미터 박스 -->
  <rect x="160" y="50" width="240" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="70" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">셰이더: Standard</text>
  <line x1="175" y1="78" x2="385" y2="78" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="200" y="96" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">Rendering Mode</text>
  <text x="340" y="96" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">Opaque</text>
  <text x="200" y="112" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">Metallic</text>
  <text x="340" y="112" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">0.9</text>
  <text x="200" y="128" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">Smoothness</text>
  <text x="340" y="128" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">0.8</text>
  <text x="200" y="144" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">색상</text>
  <text x="340" y="144" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">회색</text>
  <!-- 화살표 → 결과 -->
  <line x1="410" y1="100" x2="438" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="436,95 444,100 436,105" fill="currentColor"/>
  <!-- 결과 박스 -->
  <rect x="450" y="76" width="100" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="500" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">반짝이는</text>
  <text x="500" y="112" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">금속 구</text>
  <!-- === 구분선 === -->
  <line x1="50" y1="170" x2="530" y2="170" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- === 유리 구 (하단) === -->
  <!-- 메쉬 박스 -->
  <rect x="30" y="190" width="90" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="235" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">구 메쉬</text>
  <text x="75" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(동일)</text>
  <!-- + 기호 -->
  <text x="140" y="245" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="bold" fill="currentColor">+</text>
  <!-- 파라미터 박스 -->
  <rect x="160" y="190" width="240" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">셰이더: Standard</text>
  <line x1="175" y1="218" x2="385" y2="218" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="200" y="236" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">Rendering Mode</text>
  <text x="340" y="236" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">Transparent</text>
  <text x="200" y="252" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">Metallic</text>
  <text x="340" y="252" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">0.1</text>
  <text x="200" y="268" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">Smoothness</text>
  <text x="340" y="268" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">1.0</text>
  <text x="200" y="284" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">색상</text>
  <text x="340" y="284" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">흰색 (Alpha 0.2)</text>
  <!-- 화살표 → 결과 -->
  <line x1="410" y1="240" x2="438" y2="240" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="436,235 444,240 436,245" fill="currentColor"/>
  <!-- 결과 박스 -->
  <rect x="450" y="216" width="100" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="500" y="236" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">투명한</text>
  <text x="500" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">유리 구</text>
  <!-- 하단 요약 -->
  <text x="280" y="322" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">셰이더(렌더링 규칙)는 같지만 파라미터 값이 다르면 외관이 달라짐</text>
</svg>
</div>

<br>

머티리얼의 핵심은 셰이더이므로, 셰이더가 GPU 안에서 어떤 단계를 거쳐 동작하는지를 이해해야 렌더링 성능까지 파악할 수 있습니다.

---

## 셰이더의 역할

셰이더는 GPU에서 실행되는 프로그램입니다. CPU의 프로그램이 하나의 작업을 순차적으로 처리하는 것과 달리, GPU는 수천 개의 정점이나 수백만 개의 픽셀을 동시에 병렬 처리하도록 설계되어 있고, 셰이더는 이 병렬 구조 위에서 동작합니다.

<br>

셰이더는 역할에 따라 크게 두 종류로 나뉩니다.
하나는 3D 공간의 정점 좌표를 2D 화면 좌표로 변환하는 **버텍스 셰이더(Vertex Shader)**, 다른 하나는 화면의 각 픽셀 색상을 결정하는 **프래그먼트 셰이더(Fragment Shader)** 입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <!-- 입력 라벨: 3D 정점 데이터 -->
  <text x="110" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3D 정점 데이터</text>
  <text x="110" y="35" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(위치, 법선, UV)</text>
  <!-- 입력 화살표 -->
  <line x1="110" y1="42" x2="110" y2="62" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="105,60 110,68 115,60" fill="currentColor"/>
  <!-- 버텍스 셰이더 박스 -->
  <rect x="30" y="70" width="160" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="96" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">버텍스 셰이더</text>
  <line x1="50" y1="106" x2="170" y2="106" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="110" y="126" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">정점마다</text>
  <text x="110" y="142" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">한 번 실행</text>
  <!-- 래스터라이저 화살표 -->
  <line x1="200" y1="120" x2="390" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="388,115 396,120 388,125" fill="currentColor"/>
  <text x="295" y="108" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">래스터라이저</text>
  <text x="295" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(고정 기능)</text>
  <!-- 프래그먼트 셰이더 박스 -->
  <rect x="400" y="70" width="160" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="480" y="96" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프래그먼트 셰이더</text>
  <line x1="420" y1="106" x2="540" y2="106" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="480" y="126" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">픽셀마다</text>
  <text x="480" y="142" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">한 번 실행</text>
  <!-- 출력 라벨: 2D 화면 픽셀 -->
  <text x="480" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2D 화면 픽셀</text>
  <text x="480" y="35" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(최종 색상)</text>
  <!-- 출력 화살표 (프래그먼트 셰이더 → 2D 화면 픽셀) -->
  <line x1="480" y1="70" x2="480" y2="50" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="475,52 480,44 485,52" fill="currentColor"/>
  <!-- 하단: 버텍스 셰이더 주요 작업 -->
  <line x1="110" y1="170" x2="110" y2="188" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="105,186 110,194 115,186" fill="currentColor"/>
  <text x="110" y="212" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">좌표 변환</text>
  <text x="110" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">법선 변환</text>
  <text x="110" y="244" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">정점 애니메이션</text>
  <!-- 하단: 프래그먼트 셰이더 주요 작업 -->
  <line x1="480" y1="170" x2="480" y2="188" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="475,186 480,194 485,186" fill="currentColor"/>
  <text x="480" y="212" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처 샘플링</text>
  <text x="480" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">조명 계산</text>
  <text x="480" y="244" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">색상 결정</text>
</svg>
</div>

### 버텍스 셰이더 (Vertex Shader)

버텍스 셰이더는 [Part 1](/dev/unity/RenderingFoundation-1/)에서 다룬 메쉬의 **정점(Vertex)마다 한 번씩** 실행됩니다.

<br>

버텍스 셰이더의 핵심 역할은 **좌표 변환**입니다.
메쉬의 정점은 원래 오브젝트 자체를 기준으로 한 **로컬 좌표계(Local Space)**에서 정의되어 있습니다. 로컬 좌표계란, 오브젝트의 중심을 원점(0, 0, 0)으로 놓고 각 정점의 위치를 표현한 좌표입니다.

버텍스 셰이더는 이 로컬 좌표를 월드 좌표로, 월드 좌표를 카메라 기준 좌표(뷰 좌표)로, 뷰 좌표를 클립 좌표로 변환하여 출력하고, 이후 GPU의 고정 기능이 원근 나눗셈과 뷰포트 변환을 거쳐 최종 화면 좌표를 산출합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 780 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 780px; width: 100%;">
  <!-- 로컬 좌표 박스 -->
  <rect x="10" y="60" width="110" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">*</text>
  <text x="65" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">로컬 좌표</text>
  <!-- 로컬 좌표 상단 라벨 -->
  <text x="65" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">로컬 좌표</text>
  <text x="65" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(모델 기준)</text>
  <!-- Model Matrix 화살표 -->
  <line x1="125" y1="90" x2="183" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="181,85 189,90 181,95" fill="currentColor"/>
  <text x="155" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">Model</text>
  <text x="155" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Matrix</text>
  <!-- 월드 좌표 박스 -->
  <rect x="192" y="60" width="110" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="247" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">*</text>
  <text x="247" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">월드 좌표</text>
  <!-- 월드 좌표 상단 라벨 -->
  <text x="247" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">월드 좌표</text>
  <text x="247" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(씬 기준)</text>
  <!-- View Matrix 화살표 -->
  <line x1="307" y1="90" x2="365" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="363,85 371,90 363,95" fill="currentColor"/>
  <text x="337" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">View</text>
  <text x="337" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Matrix</text>
  <!-- 뷰 좌표 박스 -->
  <rect x="374" y="60" width="110" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="429" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">*</text>
  <text x="429" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">뷰 좌표</text>
  <!-- 뷰 좌표 상단 라벨 -->
  <text x="429" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">뷰 좌표</text>
  <text x="429" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(카메라 기준)</text>
  <!-- Projection Matrix 화살표 -->
  <line x1="489" y1="90" x2="547" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="545,85 553,90 545,95" fill="currentColor"/>
  <text x="519" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">Projection</text>
  <text x="519" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Matrix</text>
  <!-- 클립 좌표 박스 -->
  <rect x="556" y="60" width="110" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="611" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">*</text>
  <text x="611" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">클립 좌표</text>
  <!-- 클립 좌표 상단 라벨 -->
  <text x="611" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">클립 좌표</text>
  <text x="611" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(Projection 적용 후)</text>
  <!-- 하단 설명 텍스트 -->
  <text x="65" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">오브젝트</text>
  <text x="65" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">자체 기준</text>
  <text x="247" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">씬 안에서의</text>
  <text x="247" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">절대 위치</text>
  <text x="429" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">카메라에서</text>
  <text x="429" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">바라본 위치</text>
  <text x="611" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">버텍스 셰이더</text>
  <text x="611" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">최종 출력</text>
  <!-- 클립 좌표 → GPU 고정 기능 화살표 -->
  <line x1="611" y1="168" x2="611" y2="198" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="606,196 611,204 616,196" fill="currentColor"/>
  <!-- GPU 고정 기능 박스 -->
  <rect x="460" y="208" width="302" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="611" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 고정 기능이 이어받음</text>
  <text x="611" y="250" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">원근 나눗셈 → 뷰포트 변환 → 화면 좌표</text>
</svg>
</div>

<br>

이 변환은 행렬 곱셈으로 수행됩니다.

Model 행렬은 오브젝트의 위치, 회전, 스케일을 반영하여 로컬 좌표를 월드 좌표로 바꾸고, View 행렬은 카메라의 위치와 방향을 반영하여 뷰 좌표로 바꾸며, Projection 행렬은 원근(또는 직교) 투영을 적용하여 클립 좌표로 바꿉니다.

Unity에서는 이 세 행렬을 셰이더에 자동으로 전달하며, 셰이더 안에서 이를 조합한 **MVP(Model-View-Projection)** 변환을 수행합니다.

<br>

버텍스 셰이더의 핵심은 좌표 변환이지만, 정점을 처리하는 과정에서 다른 작업도 함께 수행합니다.
**법선 벡터 변환**(조명 계산에 필요), **UV 좌표 전달**(텍스처 매핑에 필요), **정점 애니메이션**(바람에 흔들리는 나뭇잎, 물결 효과 등)이 대표적입니다. 특히 정점 애니메이션은 CPU가 아닌 GPU에서 수행되므로, 대량의 오브젝트에 적용해도 CPU 부하를 줄일 수 있습니다.

### 프래그먼트 셰이더 (Fragment Shader)

정점의 좌표 변환이 끝나고 화면 좌표가 확정되면, GPU의 고정 기능 하드웨어인 **래스터라이저(Rasterizer)**가 삼각형 내부를 화면 픽셀로 채웁니다([Part 1](/dev/unity/RenderingFoundation-1/)에서 다룬 래스터화 단계).

이때 채워진 각 픽셀 후보를 **프래그먼트(Fragment)**라고 부르며, 프래그먼트 셰이더는 이 프래그먼트마다 한 번씩 실행되어 **최종 색상을 결정**합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- 좌측: 래스터라이저 입력 -->
  <text x="140" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">래스터라이저 입력</text>
  <text x="140" y="36" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(화면 좌표의 세 정점)</text>
  <!-- 삼각형 와이어프레임 -->
  <polygon points="140,60 70,190 210,190" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- 정점 레이블 -->
  <circle cx="140" cy="60" r="4" fill="currentColor"/>
  <text x="140" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v0</text>
  <circle cx="70" cy="190" r="4" fill="currentColor"/>
  <text x="56" y="195" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v1</text>
  <circle cx="210" cy="190" r="4" fill="currentColor"/>
  <text x="224" y="195" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v2</text>
  <!-- 하단 설명 -->
  <text x="140" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">세 정점의 화면 좌표</text>
  <!-- 중앙 화살표 -->
  <line x1="250" y1="130" x2="320" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="318,125 326,130 318,135" fill="currentColor"/>
  <!-- 우측: 래스터라이저 출력 -->
  <text x="450" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">래스터라이저 출력</text>
  <text x="450" y="36" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(프래그먼트들)</text>
  <!-- 프래그먼트 그리드 (삼각형 형태로 채운 사각형들) -->
  <!-- 1행: 1개 -->
  <rect x="443" y="60" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 2행: 3개 -->
  <rect x="428" y="76" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="76" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="76" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 3행: 5개 -->
  <rect x="413" y="92" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="428" y="92" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="92" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="92" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="473" y="92" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 4행: 7개 -->
  <rect x="398" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="413" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="428" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="473" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="488" y="108" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 5행: 9개 -->
  <rect x="383" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="398" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="413" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="428" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="473" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="488" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="503" y="124" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 6행: 11개 -->
  <rect x="368" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="383" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="398" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="413" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="428" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="473" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="488" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="503" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="518" y="140" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 7행: 13개 -->
  <rect x="353" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="368" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="383" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="398" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="413" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="428" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="473" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="488" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="503" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="518" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="533" y="156" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 8행: 15개 -->
  <rect x="338" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="353" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="368" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="383" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="398" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="413" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="428" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="443" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="458" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="473" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="488" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="503" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="518" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="533" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <rect x="548" y="172" width="14" height="14" rx="1" fill="currentColor" fill-opacity="0.35"/>
  <!-- 삼각형 아웃라인 (그리드 위에 겹쳐 표시) -->
  <polygon points="450,54 330,190 570,190" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.3" stroke-dasharray="4,3"/>
  <!-- 하단 설명 -->
  <text x="450" y="210" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">삼각형 내부를 채운 픽셀(프래그먼트)</text>
  <text x="450" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">각 사각형마다 프래그먼트 셰이더 실행</text>
</svg>
</div>

<br>

프래그먼트 셰이더가 수행하는 작업은 크게 세 단계입니다.
**텍스처 샘플링**에서 텍스처의 색상을 읽어오고, **조명 계산**에서 빛과 표면의 상호작용을 계산한 뒤, **최종 색상 결합**에서 이 둘을 합쳐 프래그먼트의 RGBA 색상을 출력합니다.

<br>

**1단계 — 텍스처 샘플링**
래스터라이저는 버텍스 셰이더가 출력한 값들(UV 좌표, 법선 등)을 프래그먼트 위치에 맞게 보간하여 프래그먼트 셰이더에 전달합니다.
프래그먼트 셰이더는 이 중 보간된 UV 좌표를 사용하여 텍스처에서 해당 텍셀(texel) 색상을 읽어옵니다.

<br>

**2단계 — 조명 계산**
표면의 법선 벡터, 광원의 위치와 강도, 카메라의 위치 등을 종합하여 빛이 표면에 어떻게 반사되는지를 계산합니다.
대표적인 조명 성분은 **확산 반사(Diffuse)**, **정반사(Specular)**, **주변광(Ambient)** 세 가지입니다.

> 고급 조명 모델에서는 자체 발광(Emissive), 프레넬(Fresnel), 서브서피스 스캐터링(Subsurface Scattering) 등의 성분도 사용됩니다.

**확산 반사(Diffuse)**는 빛이 표면에 닿은 뒤 모든 방향으로 균일하게 퍼지는 반사입니다.
[Part 1](/dev/unity/RenderingFoundation-1/)에서 다룬 법선 벡터와 광원 방향 사이의 각도(cos θ)가 이 값을 결정하며, 오브젝트의 기본적인 밝고 어두운 면을 만들어 냅니다.

**정반사(Specular)**는 빛이 특정 방향으로 집중 반사되어 표면에 밝은 하이라이트를 만드는 성분입니다.
확산 반사는 법선과 광원 방향만으로 계산되므로 카메라 위치와 무관하지만, 정반사는 반사된 빛이 카메라를 향할 때만 밝게 보이므로 카메라가 이동하면 하이라이트 위치도 함께 달라집니다(시점 의존, View-Dependent).

**주변광(Ambient)**은 직접 광원 없이도 환경에서 간접적으로 도달하는 빛입니다. 직사광선이 닿지 않는 그림자 영역이 완전히 검게 보이지 않는 이유가 이 주변광 때문입니다.

<br>

**3단계 — 최종 색상 결합**
프래그먼트 셰이더는 세 조명 성분을 합산한 조명 값에 텍스처 색상을 결합하고, 머티리얼에 설정된 색상이나 기타 파라미터를 반영하여 프래그먼트의 RGBA 색상을 출력합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- 1단계: 텍스처 샘플링 -->
  <text x="36" y="20" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1) 텍스처 샘플링</text>
  <!-- 입력: UV 좌표 -->
  <rect x="36" y="34" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="86" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">UV 좌표</text>
  <!-- 화살표 UV → 텍셀 읽기 -->
  <line x1="140" y1="51" x2="178" y2="51" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="176,46 184,51 176,56" fill="currentColor"/>
  <!-- 처리: 텍스처에서 텍셀 읽기 -->
  <rect x="188" y="34" width="170" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="273" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처에서 텍셀 읽기</text>
  <!-- 화살표 텍셀 읽기 → 텍스처 색상 -->
  <line x1="362" y1="51" x2="400" y2="51" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="398,46 406,51 398,56" fill="currentColor"/>
  <!-- 출력: 텍스처 색상 -->
  <rect x="410" y="34" width="120" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="470" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">텍스처 색상</text>
  <!-- 수직 연결선 1→2 -->
  <line x1="273" y1="68" x2="273" y2="110" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="268,108 273,116 278,108" fill="currentColor"/>
  <!-- 2단계: 조명 계산 -->
  <text x="36" y="136" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2) 조명 계산</text>
  <!-- 입력들: 법선 벡터, 광원 정보, 카메라 위치 -->
  <rect x="36" y="150" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="86" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">법선 벡터</text>
  <rect x="36" y="192" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="86" y="214" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">광원 정보</text>
  <rect x="36" y="234" width="100" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="86" y="256" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">카메라 위치</text>
  <!-- 합류선 -->
  <line x1="140" y1="167" x2="160" y2="167" stroke="currentColor" stroke-width="1.5"/>
  <line x1="160" y1="167" x2="160" y2="209" stroke="currentColor" stroke-width="1.5"/>
  <line x1="140" y1="209" x2="160" y2="209" stroke="currentColor" stroke-width="1.5"/>
  <line x1="140" y1="251" x2="160" y2="251" stroke="currentColor" stroke-width="1.5"/>
  <line x1="160" y1="209" x2="160" y2="251" stroke="currentColor" stroke-width="1.5"/>
  <!-- 화살표 합류 → 조명 처리 -->
  <line x1="160" y1="209" x2="178" y2="209" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="176,204 184,209 176,214" fill="currentColor"/>
  <!-- 처리: 확산 + 정반사 + 주변광 -->
  <rect x="188" y="188" width="210" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="293" y="214" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">확산 + 정반사 + 주변광</text>
  <!-- 화살표 조명 처리 → 조명 값 -->
  <line x1="402" y1="209" x2="440" y2="209" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="438,204 446,209 438,214" fill="currentColor"/>
  <!-- 출력: 조명 값 -->
  <rect x="450" y="192" width="90" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="495" y="214" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">조명 값</text>
  <!-- 수직 연결선 2→3 -->
  <line x1="293" y1="230" x2="293" y2="275" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="288,273 293,281 298,273" fill="currentColor"/>
  <!-- 3단계: 최종 색상 결정 -->
  <text x="36" y="300" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3) 최종 색상 결정</text>
  <!-- 입력들: 텍스처 색상, 조명 값, 머티리얼 파라미터 -->
  <rect x="36" y="314" width="130" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="336" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처 색상</text>
  <rect x="36" y="356" width="130" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="378" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">조명 값</text>
  <rect x="36" y="398" width="130" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="416" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼 파라미터</text>
  <text x="101" y="428" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(색상, 반사도 등)</text>
  <!-- 합류선 -->
  <line x1="170" y1="331" x2="190" y2="331" stroke="currentColor" stroke-width="1.5"/>
  <line x1="190" y1="331" x2="190" y2="373" stroke="currentColor" stroke-width="1.5"/>
  <line x1="170" y1="373" x2="190" y2="373" stroke="currentColor" stroke-width="1.5"/>
  <line x1="170" y1="415" x2="190" y2="415" stroke="currentColor" stroke-width="1.5"/>
  <line x1="190" y1="373" x2="190" y2="415" stroke="currentColor" stroke-width="1.5"/>
  <!-- 화살표 합류 → 결합 -->
  <line x1="190" y1="373" x2="218" y2="373" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="216,368 224,373 216,378" fill="currentColor"/>
  <!-- 처리: 결합 -->
  <rect x="228" y="356" width="80" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="268" y="378" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">결합</text>
  <!-- 화살표 결합 → 최종 RGBA 출력 -->
  <line x1="312" y1="373" x2="350" y2="373" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="348,368 356,373 348,378" fill="currentColor"/>
  <!-- 출력: 최종 RGBA 출력 -->
  <rect x="360" y="356" width="150" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="435" y="378" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">최종 RGBA 출력</text>
</svg>
</div>

<br>

### 프래그먼트 셰이더가 더 비싼 이유

버텍스 셰이더와 프래그먼트 셰이더를 비교하면, 대부분의 장면에서 프래그먼트 셰이더가 GPU 시간을 더 많이 소비합니다. 가장 큰 원인은 **실행 횟수의 차이**입니다.

삼각형 하나를 예로 들면, 정점이 3개이므로 버텍스 셰이더는 3번 실행됩니다. 같은 삼각형이 화면에서 1,000픽셀을 차지한다면, 프래그먼트 셰이더는 1,000번 실행됩니다.

<br>

일반적인 3D 오브젝트에서 화면에 그려지는 프래그먼트 수는 정점 수보다 수십~수백 배 많습니다.
1080p 해상도(1920x1080) 기준으로 화면 전체를 덮는 오브젝트는 약 207만 개의 프래그먼트를 생성합니다.

여기에 프래그먼트 셰이더는 텍스처 샘플링과 조명 계산 등 버텍스 셰이더의 행렬 곱셈보다 복잡한 연산을 수행하는 경우가 많으므로, 실행 횟수와 연산 복잡도가 함께 작용하여 비용이 커집니다.

프래그먼트 셰이더에 연산 하나를 추가하면 그 연산이 207만 번 반복되는 셈이므로, 프래그먼트 셰이더의 복잡도를 줄이는 것은 렌더링 성능 최적화에서 가장 효과가 큰 영역 중 하나입니다.

---

## 렌더 스테이트 (Render State)

셰이더는 정점의 좌표를 변환하고 프래그먼트의 색상을 계산하지만, GPU가 오브젝트를 그리려면 뒷면 삼각형의 제거, 겹치는 오브젝트 간의 깊이 비교, 투명 오브젝트의 색상 합성 같은 추가 처리도 필요합니다.

**렌더 스테이트(Render State)**는 이러한 처리를 GPU 파이프라인이 어떻게 수행할지를 제어하는 설정입니다.
블렌딩, 깊이 테스트, 컬링, 스텐실 테스트 등이 렌더 스테이트에 포함됩니다.

### 블렌딩 (Blending)

GPU가 새 프래그먼트를 그릴 때, 해당 픽셀의 컬러 버퍼에는 이미 다른 색상이 기록되어 있을 수 있습니다. 불투명 오브젝트는 기존 색상을 완전히 덮어쓰면 되지만, 반투명 유리나 연기 같은 오브젝트는 새 색상과 기존 색상을 섞어야 합니다. 이때 새 색상(source)과 기존 색상(destination)을 합성하는 연산이 블렌딩입니다.

알파 블렌딩의 기본 공식은 `결과 = source × α + destination × (1 - α)` 입니다. α가 1이면 새 색상만 남고(불투명), 0이면 기존 색상만 남습니다(완전 투명).

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 좌측: 불투명 -->
  <text x="130" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">불투명 (Blend Off)</text>
  <!-- dst -->
  <rect x="40" y="32" width="80" height="40" rx="5" fill="#4488CC" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="50" text-anchor="middle" font-family="sans-serif" font-size="10" fill="white">dst</text>
  <text x="80" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="white" opacity="0.8">파란 배경</text>
  <!-- + -->
  <text x="140" y="58" text-anchor="middle" font-family="sans-serif" font-size="16" fill="currentColor">+</text>
  <!-- src -->
  <rect x="160" y="32" width="80" height="40" rx="5" fill="#CC4444" stroke="currentColor" stroke-width="1"/>
  <text x="200" y="50" text-anchor="middle" font-family="sans-serif" font-size="10" fill="white">src</text>
  <text x="200" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="white" opacity="0.8">빨간 오브젝트</text>
  <!-- 화살표 -->
  <line x1="130" y1="80" x2="130" y2="108" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="125,106 130,114 135,106" fill="currentColor"/>
  <!-- 결과 -->
  <rect x="70" y="118" width="120" height="44" rx="5" fill="#CC4444" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="140" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="white">빨강</text>
  <text x="130" y="154" text-anchor="middle" font-family="sans-serif" font-size="9" fill="white" opacity="0.8">완전 덮어쓰기</text>
  <!-- 구분선 -->
  <line x1="270" y1="8" x2="270" y2="200" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- 우측: 반투명 -->
  <text x="400" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">반투명 (α = 0.5)</text>
  <!-- dst -->
  <rect x="310" y="32" width="80" height="40" rx="5" fill="#4488CC" stroke="currentColor" stroke-width="1"/>
  <text x="350" y="50" text-anchor="middle" font-family="sans-serif" font-size="10" fill="white">dst</text>
  <text x="350" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="white" opacity="0.8">파란 배경</text>
  <!-- + -->
  <text x="410" y="58" text-anchor="middle" font-family="sans-serif" font-size="16" fill="currentColor">+</text>
  <!-- src (반투명 표현) -->
  <rect x="430" y="32" width="80" height="40" rx="5" fill="#CC4444" fill-opacity="0.5" stroke="currentColor" stroke-width="1"/>
  <text x="470" y="50" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">src</text>
  <text x="470" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">빨간 유리</text>
  <!-- 화살표 -->
  <line x1="400" y1="80" x2="400" y2="108" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,106 400,114 405,106" fill="currentColor"/>
  <!-- 결과 -->
  <rect x="340" y="118" width="120" height="44" rx="5" fill="#884488" stroke="currentColor" stroke-width="1"/>
  <text x="400" y="140" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="white">보라</text>
  <text x="400" y="154" text-anchor="middle" font-family="sans-serif" font-size="9" fill="white" opacity="0.8">src × 0.5 + dst × 0.5</text>
</svg>
</div>

<br>

### 깊이 테스트 (Depth Test / Z-Buffer)

깊이 테스트는 같은 픽셀 위치에 여러 오브젝트가 겹칠 때, 어떤 오브젝트가 앞에 있는지를 판별하는 처리입니다.

GPU는 **Z-buffer(깊이 버퍼)**라는 별도의 버퍼를 유지하며, 각 픽셀마다 현재까지 그려진 가장 가까운 프래그먼트의 깊이 값을 저장합니다. 깊이 값은 카메라로부터의 거리를 나타내며, 값이 작을수록 카메라에 가깝습니다.

새 프래그먼트가 도달하면 GPU는 해당 픽셀의 Z-buffer 값과 비교합니다. 더 가까우면(깊이 값이 더 작으면) 컬러 버퍼에 기록하고 Z-buffer를 갱신합니다. 더 멀면 이미 앞에 다른 오브젝트가 있으므로 폐기합니다.

한 픽셀(P)에 세 오브젝트가 겹치는 경우:

| 단계 | 오브젝트 | 깊이 비교 | 결과 | 컬러 버퍼[P] | Z-buffer[P] |
|------|----------|-----------|------|-------------|-------------|
| 초기 상태 | — | — | — | 비어 있음 | ∞ |
| ① | 빨간 상자 (깊이 7) | 7 < ∞ | 통과 | 빨강 | 7 |
| ② | 파란 구 (깊이 3) | 3 < 7 | 통과 (더 가까움) | 파랑 | 3 |
| ③ | 초록 벽 (깊이 9) | 9 < 3 | 실패 (더 멀음) | 파랑 (변경 없음) | 3 |

최종 결과: **파란 구의 색상이 화면에 표시됨** (깊이 값이 가장 작은 오브젝트)

<br>

### 컬링 (Culling)

컬링은 렌더링할 필요가 없는 요소를 미리 제외하는 처리입니다. 렌더 스테이트에서 제어하는 컬링은 **백 페이스 컬링(Back-face Culling)**으로, 카메라를 향하지 않는 삼각형의 뒷면을 그리지 않는 설정입니다.

삼각형은 평면이므로 바라보는 방향에 따라 두 면이 존재합니다. 같은 삼각형이라도 한쪽에서 보면 정점이 시계 방향으로 나열되고, 반대쪽에서 보면 반시계 방향으로 나열됩니다.
GPU는 이 나열 순서로 앞뒤를 구분합니다.

> Unity의 기본 규칙은 카메라에서 바라볼 때 정점이 시계 방향(CW)이면 앞면, 반시계 방향(CCW)이면 뒷면입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 450" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 상단 설명 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">카메라에서 바라본 정점 나열 순서로 앞면/뒷면을 구분</text>
  <!-- 좌측: 시계 방향(CW) 삼각형 -->
  <polygon points="130,50 70,150 190,150" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="130" cy="50" r="4" fill="currentColor"/>
  <text x="130" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v0</text>
  <circle cx="70" cy="150" r="4" fill="currentColor"/>
  <text x="56" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v2</text>
  <circle cx="190" cy="150" r="4" fill="currentColor"/>
  <text x="204" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v1</text>
  <!-- CW 회전 화살표 (270° 원호, v0→v1 방향) -->
  <path d="M 130,100 A 17,17 0 1,1 113,117" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <polygon points="109,120 113,112 117,120" fill="currentColor" opacity="0.4"/>
  <!-- CW 라벨 -->
  <text x="130" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">시계 방향(CW)</text>
  <text x="130" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">= 앞면</text>
  <text x="130" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">렌더링</text>
  <!-- 우측: 반시계 방향(CCW) 삼각형 -->
  <polygon points="400,50 460,150 340,150" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <circle cx="400" cy="50" r="4" fill="currentColor"/>
  <text x="400" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v0</text>
  <circle cx="460" cy="150" r="4" fill="currentColor"/>
  <text x="474" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v2</text>
  <circle cx="340" cy="150" r="4" fill="currentColor"/>
  <text x="326" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">v1</text>
  <!-- CCW 회전 화살표 (270° 원호, v0→v1 방향) -->
  <path d="M 400,100 A 17,17 0 1,0 417,117" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"/>
  <polygon points="413,120 417,112 421,120" fill="currentColor" opacity="0.4"/>
  <!-- CCW 라벨 -->
  <text x="400" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">반시계 방향(CCW)</text>
  <text x="400" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">= 뒷면</text>
  <text x="400" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">컬링(제외)</text>
  <!-- 구분선 -->
  <line x1="40" y1="224" x2="520" y2="224" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- 하단: 닫힌 오브젝트 적용 -->
  <text x="280" y="248" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">닫힌 오브젝트(구, 큐브)에 적용</text>
  <!-- 카메라 -->
  <text x="200" y="276" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">카메라</text>
  <line x1="200" y1="282" x2="200" y2="304" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,302 200,310 205,302" fill="currentColor"/>
  <!-- 앞면 박스 -->
  <rect x="130" y="320" width="140" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="340" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">앞면</text>
  <text x="200" y="356" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(&#8776; 50%)</text>
  <!-- 앞면 → 렌더링 라벨 -->
  <line x1="274" y1="343" x2="310" y2="343" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="308,338 316,343 308,348" fill="currentColor"/>
  <text x="360" y="347" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">렌더링</text>
  <!-- 뒷면 박스 -->
  <rect x="130" y="378" width="140" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="200" y="398" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">뒷면</text>
  <text x="200" y="414" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.35">(&#8776; 50%)</text>
  <!-- 뒷면 → 컬링 라벨 -->
  <line x1="274" y1="401" x2="310" y2="401" stroke="currentColor" stroke-width="1.5" opacity="0.5"/>
  <polygon points="308,396 316,401 308,406" fill="currentColor" opacity="0.5"/>
  <text x="370" y="405" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">컬링(제외)</text>
  <!-- 하단 결론 -->
  <text x="280" y="444" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">렌더링 대상 삼각형 약 50% 감소</text>
</svg>
</div>

<br>

큐브나 구처럼 표면이 닫힌 오브젝트는 뒷면이 카메라에 보이지 않습니다. 백 페이스 컬링을 활성화하면 이 뒷면을 구성하는 삼각형을 건너뛰므로, 렌더링 대상이 대략 절반으로 줄어듭니다. 다만, 종이처럼 양면이 모두 보여야 하는 오브젝트에서는 컬링을 비활성화해야 합니다.

### 스텐실 테스트 (Stencil Test)

**스텐실(Stencil)**은 형판을 뜻합니다. 형판을 대고 칠하면 뚫린 부분만 색이 입혀지듯, **스텐실 테스트**는 화면에서 렌더링할 영역과 제외할 영역을 픽셀 단위로 지정합니다.

이를 위해 GPU는 **스텐실 버퍼(Stencil Buffer)**에 각 픽셀의 정수 값(보통 0~255)을 관리합니다. 먼저 특정 오브젝트를 그리면서 해당 픽셀에 값을 기록해 두고, 이후 다른 오브젝트를 그릴 때 이 값을 조건으로 통과 여부를 결정하는 방식입니다.

포털 효과를 예로 들면, 먼저 포털 형태의 메쉬를 그리면서 해당 픽셀의 스텐실 값을 1로 표시합니다. 이후 다른 씬을 렌더링할 때 "스텐실 값이 1인 픽셀에만 그려라"는 조건을 설정하면, 포털 영역 안에서만 다른 씬이 보입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 470" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Step 1 label -->
  <text x="20" y="22" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1) 포털 메쉬를 그리며 스텐실 버퍼에 값 기록</text>
  <!-- Stencil buffer outer rect -->
  <rect x="60" y="40" width="260" height="170" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="60" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">스텐실 버퍼 상태</text>
  <!-- Grid of 0s (outer region) -->
  <!-- Row 1: all 0s -->
  <text x="90" y="85" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="130" y="85" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="170" y="85" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="210" y="85" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="250" y="85" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="290" y="85" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <!-- Row 2: 0 [1 1 1 1] 0 -->
  <text x="90" y="110" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="290" y="110" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <!-- Row 3: 0 [1 1 1 1] 0 -->
  <text x="90" y="135" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="290" y="135" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <!-- Row 4: 0 [1 1 1 1] 0 -->
  <text x="90" y="160" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="290" y="160" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <!-- Row 5: all 0s -->
  <text x="90" y="185" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="130" y="185" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="170" y="185" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="210" y="185" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="250" y="185" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <text x="290" y="185" text-anchor="middle" font-family="monospace" font-size="13" fill="currentColor" opacity="0.35">0</text>
  <!-- Portal region (inner rect with 1s) -->
  <rect x="120" y="96" width="140" height="72" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 2"/>
  <text x="140" y="115" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="170" y="115" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="200" y="115" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="230" y="115" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="140" y="140" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="170" y="140" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="200" y="140" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="230" y="140" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="140" y="162" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="170" y="162" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="200" y="162" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <text x="230" y="162" text-anchor="middle" font-family="monospace" font-size="13" font-weight="bold" fill="currentColor">1</text>
  <!-- Annotation for portal region -->
  <text x="370" y="110" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">포털 메쉬 영역</text>
  <line x1="262" y1="110" x2="365" y2="110" stroke="currentColor" stroke-width="1" opacity="0.3" stroke-dasharray="3 2"/>
  <!-- Arrow between step 1 and step 2 -->
  <line x1="190" y1="218" x2="190" y2="242" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="185,240 190,248 195,240" fill="currentColor"/>
  <!-- Step 2 label -->
  <text x="20" y="268" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2) 스텐실 = 1인 픽셀만 렌더링</text>
  <!-- Screen outer rect (Step 1과 동일 크기) -->
  <rect x="60" y="282" width="260" height="170" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="302" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">화면 결과</text>
  <!-- Normal scene labels -->
  <text x="190" y="325" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">일반 씬</text>
  <text x="190" y="435" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">일반 씬</text>
  <!-- Portal inner rect (Step 1과 동일 크기) -->
  <rect x="120" y="338" width="140" height="72" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="369" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">다른 씬이</text>
  <text x="190" y="384" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">포털 안에만 보임</text>
  <!-- Annotation -->
  <text x="370" y="374" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">스텐실 = 1 영역만 렌더링</text>
  <line x1="262" y1="374" x2="365" y2="374" stroke="currentColor" stroke-width="1" opacity="0.3" stroke-dasharray="3 2"/>
</svg>
</div>

### 렌더 스테이트 변경의 비용

GPU는 현재 렌더 스테이트에 맞춰 파이프라인을 구성합니다. 스테이트가 바뀌면 파이프라인을 재구성해야 하므로, 이 **스테이트 변경(State Change)**이 잦을수록 렌더링 성능이 떨어집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- LEFT SIDE: Inefficient ordering -->
  <text x="140" y="22" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">비효율적인 순서</text>
  <line x1="50" y1="32" x2="230" y2="32" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Object A -->
  <rect x="40" y="46" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 A: 불투명</text>
  <!-- Change arrow 1 -->
  <text x="256" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">변경</text>
  <line x1="240" y1="80" x2="240" y2="100" stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="3 2"/>
  <!-- Object B -->
  <rect x="40" y="88" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="140" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 B: 투명</text>
  <!-- Change arrow 2 -->
  <text x="256" y="136" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">변경</text>
  <line x1="240" y1="122" x2="240" y2="142" stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="3 2"/>
  <!-- Object C -->
  <rect x="40" y="130" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="152" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 C: 불투명</text>
  <!-- Change arrow 3 -->
  <text x="256" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">변경</text>
  <line x1="240" y1="164" x2="240" y2="184" stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="3 2"/>
  <!-- Object D -->
  <rect x="40" y="172" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="140" y="194" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 D: 투명</text>
  <!-- Result left -->
  <text x="140" y="232" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">스테이트 변경: 3회</text>
  <!-- Divider -->
  <line x1="300" y1="10" x2="300" y2="250" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <!-- RIGHT SIDE: Efficient ordering -->
  <text x="460" y="22" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">효율적인 순서</text>
  <line x1="370" y1="32" x2="550" y2="32" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- Group label: opaque -->
  <text x="460" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">불투명 오브젝트 모아서 그리기</text>
  <!-- Object A -->
  <rect x="360" y="58" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 A: 불투명</text>
  <!-- Object C -->
  <rect x="360" y="96" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 C: 불투명</text>
  <!-- Single change arrow -->
  <text x="576" y="148" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">변경 1회</text>
  <line x1="560" y1="134" x2="560" y2="156" stroke="currentColor" stroke-width="1" opacity="0.4" stroke-dasharray="3 2"/>
  <!-- Group label: transparent -->
  <text x="460" y="152" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">투명 오브젝트 모아서 그리기</text>
  <!-- Object B -->
  <rect x="360" y="158" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="460" y="180" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 B: 투명</text>
  <!-- Object D -->
  <rect x="360" y="196" width="200" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="460" y="218" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 D: 투명</text>
  <!-- Result right -->
  <text x="460" y="256" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">스테이트 변경: 1회</text>
</svg>
</div>

<br>

같은 렌더 스테이트를 사용하는 오브젝트끼리 모아서 그리면 스테이트 변경 횟수를 줄일 수 있습니다.

<br>

이에 따라 대부분의 렌더링 엔진은 불투명 오브젝트를 먼저 모두 그린 뒤, 투명 오브젝트를 그립니다.

불투명 오브젝트는 깊이 테스트만으로 앞뒤가 결정되므로 어떤 순서로 그려도 시각적 결과는 같습니다. 이 점을 활용하여 카메라에서 가까운 순서(front-to-back)로 정렬하면, 가까운 오브젝트가 먼저 깊이 버퍼를 채워 뒤에 가려지는 프래그먼트를 조기에 폐기할 수 있어 불필요한 셰이딩이 줄어듭니다.

투명 오브젝트는 반대로 먼 순서(back-to-front)로 그립니다. 알파 블렌딩은 컬러 버퍼에 이미 기록된 색상 위에 새 색상을 합성하므로, 뒤에 있는 오브젝트의 색상이 먼저 기록되어 있어야 올바른 결과가 나옵니다.

---

## 고정 파이프라인에서 프로그래머블 셰이더로

지금까지 설명한 버텍스 셰이더와 프래그먼트 셰이더는 조명 모델, 정점 변형, 시각 효과 등을 개발자가 직접 프로그래밍할 수 있는 구조입니다.

하지만 초기 GPU는 조명이나 텍스처 처리 방식이 하드웨어에 고정되어 있어, 정해진 방식 외의 렌더링은 불가능했습니다. 이 제약을 넘어서며 등장한 것이 프로그래머블 셰이더입니다.

<br>

### 고정 기능 파이프라인 (Fixed Function Pipeline)

초기 GPU(1990년대)의 **고정 기능 파이프라인**에서 개발자가 제어할 수 있는 것은 광원 수, 텍스처 모드 같은 몇 가지 파라미터뿐이었습니다. 조명 계산이나 텍스처 합성의 알고리즘 자체를 바꿀 수는 없었습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Input: 정점 데이터 -->
  <text x="140" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 데이터</text>
  <!-- Arrow down -->
  <line x1="140" y1="28" x2="140" y2="48" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="135,46 140,54 145,46" fill="currentColor"/>
  <!-- Stage 1: 좌표 변환 -->
  <rect x="60" y="56" width="160" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="78" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">좌표 변환</text>
  <text x="140" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(고정)</text>
  <!-- Annotation 1 -->
  <line x1="220" y1="82" x2="250" y2="82" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="256" y="78" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">위치, 회전, 스케일 값만</text>
  <text x="256" y="92" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">설정 가능</text>
  <!-- Arrow down -->
  <line x1="140" y1="108" x2="140" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="135,126 140,134 145,126" fill="currentColor"/>
  <!-- Stage 2: 조명 계산 -->
  <rect x="60" y="136" width="160" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="158" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">조명 계산</text>
  <text x="140" y="176" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(고정)</text>
  <!-- Annotation 2 -->
  <line x1="220" y1="162" x2="250" y2="162" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="256" y="158" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">광원 위치, 색상, 개수만</text>
  <text x="256" y="172" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">설정 가능</text>
  <!-- Arrow down -->
  <line x1="140" y1="188" x2="140" y2="208" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="135,206 140,214 145,206" fill="currentColor"/>
  <!-- Stage 3: 텍스처 합성 -->
  <rect x="60" y="216" width="160" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="238" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">텍스처 합성</text>
  <text x="140" y="256" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(고정)</text>
  <!-- Annotation 3 -->
  <line x1="220" y1="242" x2="250" y2="242" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="256" y="238" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">블렌딩 모드, 안개(Fog)만</text>
  <text x="256" y="252" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">설정 가능</text>
  <!-- Arrow down -->
  <line x1="140" y1="268" x2="140" y2="288" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="135,286 140,294 145,286" fill="currentColor"/>
  <!-- Output: 화면 -->
  <text x="140" y="310" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">화면</text>
  <!-- Bottom summary -->
  <line x1="40" y1="330" x2="440" y2="330" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="240" y="352" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">모든 단계의 알고리즘이 하드웨어에 고정</text>
  <text x="240" y="370" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">파라미터 조절만 가능, 알고리즘 변경 불가</text>
</svg>
</div>

<br>

이 구조는 단순하고 하드웨어 최적화에 유리했지만, 표현의 한계가 분명했습니다. 모든 게임이 같은 조명 모델을 사용할 수밖에 없었으므로, 시각적 차별화가 어려웠습니다.

### 프로그래머블 셰이더의 등장

2000년 말 DirectX 8.0이 발표되고, 2001년 NVIDIA GeForce 3가 출시되면서 **프로그래머블 셰이더**가 도입되었습니다. 고정되어 있던 정점 처리와 픽셀 처리 단계를 개발자가 직접 프로그래밍할 수 있게 되었습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 470" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Input: 정점 데이터 -->
  <text x="150" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 데이터</text>
  <!-- Arrow down -->
  <line x1="150" y1="28" x2="150" y2="48" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="145,46 150,54 155,46" fill="currentColor"/>
  <!-- Stage 1: 버텍스 셰이더 -->
  <rect x="60" y="56" width="180" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="80" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">버텍스 셰이더</text>
  <line x1="80" y1="88" x2="220" y2="88" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="150" y="106" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">개발자가 작성하는 프로그램</text>
  <text x="150" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(프로그래머블)</text>
  <!-- Annotation 1 -->
  <line x1="240" y1="92" x2="270" y2="92" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="276" y="82" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">좌표 변환, 법선 처리,</text>
  <text x="276" y="96" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">정점 변형 등을 자유롭게 구현</text>
  <!-- Arrow down -->
  <line x1="150" y1="128" x2="150" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="145,146 150,154 155,146" fill="currentColor"/>
  <!-- Stage 2: 래스터라이저 -->
  <rect x="60" y="156" width="180" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="150" y="178" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">래스터라이저</text>
  <text x="150" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(고정 기능)</text>
  <!-- Annotation 2 -->
  <line x1="240" y1="182" x2="270" y2="182" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="276" y="186" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">하드웨어 고정 (변경 불가)</text>
  <!-- Arrow down -->
  <line x1="150" y1="208" x2="150" y2="228" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="145,226 150,234 155,226" fill="currentColor"/>
  <!-- Stage 3: 프래그먼트 셰이더 -->
  <rect x="60" y="236" width="180" height="72" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="260" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프래그먼트 셰이더</text>
  <line x1="80" y1="268" x2="220" y2="268" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="150" y="286" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">개발자가 작성하는 프로그램</text>
  <text x="150" y="300" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(프로그래머블)</text>
  <!-- Annotation 3 -->
  <line x1="240" y1="272" x2="270" y2="272" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="276" y="262" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">조명 모델, 텍스처 합성,</text>
  <text x="276" y="276" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">색상 계산 등을 자유롭게 구현</text>
  <!-- Arrow down -->
  <line x1="150" y1="308" x2="150" y2="328" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="145,326 150,334 155,326" fill="currentColor"/>
  <!-- Output: 화면 -->
  <text x="150" y="350" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">화면</text>
  <!-- Bottom summary -->
  <line x1="40" y1="370" x2="480" y2="370" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="260" y="392" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">고정 파이프라인과의 차이:</text>
  <text x="260" y="412" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">파라미터 조절만 가능 → 알고리즘 자체를 교체 가능</text>
</svg>
</div>

<br>

이 변화 덕분에 만화 느낌의 **툰 셰이딩(Toon Shading)**, 물리 법칙 기반의 사실적 표면을 표현하는 **PBR(Physically Based Rendering)**, 복잡한 형상을 실시간으로 그리는 **레이 마칭(Ray Marching)** 같은 기법이 가능해졌습니다.

### 셰이더 언어의 발전

초기에는 어셈블리에 가까운 저수준 명령어로 셰이더를 작성했지만, 이후 C 언어와 유사한 문법의 고수준 셰이더 언어가 등장했습니다.

| 시기 | 언어 / 기술 | 특징 |
|------|-------------|------|
| ~2001 | 어셈블리 셰이더 | 레지스터 직접 조작 |
| 2002~ | HLSL (DirectX) | C 유사 문법 |
| | Cg (NVIDIA) | 크로스 API 대응 |
| 2004~ | GLSL (OpenGL) | C 유사 문법 |
| 2014~ | Metal Shading Language | Apple 플랫폼 전용 |
| 2016~ | SPIR-V (Vulkan) | 셰이더 바이트코드 표준 |

<br>

Unity의 셰이더 시스템도 이 흐름을 따라 발전했습니다.

Unity는 셰이더의 구조(패스, 렌더 스테이트, 프로퍼티 등)를 선언하는 **ShaderLab**이라는 고유의 기술 언어를 사용합니다.

ShaderLab 안에 셰이더 코드를 작성하는 방식은 시대에 따라 변화했습니다.
초기에는 고정 파이프라인 명령을 나열하는 **고정 함수 셰이더** 방식이었지만, 이후 **Cg**와 **HLSL**로 버텍스/프래그먼트 셰이더를 직접 작성하는 방식으로 전환되었습니다.

현재는 **HLSL**이 표준이며, 노드 기반으로 셰이더를 구성하는 **Shader Graph**도 제공됩니다. Shader Graph도 내부적으로 HLSL 코드를 생성하므로, 최종 결과는 코드로 작성한 셰이더와 동일합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 1단계: 고정 함수 셰이더 -->
  <rect x="80" y="10" width="260" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="36" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">고정 함수 셰이더 (레거시)</text>
  <text x="360" y="36" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">고정 파이프라인 시절</text>
  <!-- 화살표 1→2 -->
  <line x1="210" y1="52" x2="210" y2="76" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="205,74 210,82 215,74" fill="currentColor"/>
  <!-- 2단계: ShaderLab + Cg -->
  <rect x="80" y="84" width="260" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="110" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">ShaderLab + Cg</text>
  <text x="360" y="110" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">프로그래머블 셰이더 초기</text>
  <!-- 화살표 2→3 -->
  <line x1="210" y1="126" x2="210" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="205,148 210,156 215,148" fill="currentColor"/>
  <!-- 3단계: ShaderLab + HLSL -->
  <rect x="80" y="158" width="260" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="184" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">ShaderLab + HLSL (현재 표준)</text>
  <!-- 분기 -->
  <line x1="210" y1="200" x2="210" y2="218" stroke="currentColor" stroke-width="1.5"/>
  <line x1="135" y1="218" x2="285" y2="218" stroke="currentColor" stroke-width="1.5"/>
  <line x1="135" y1="218" x2="135" y2="240" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="130,238 135,246 140,238" fill="currentColor"/>
  <line x1="285" y1="218" x2="285" y2="240" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="280,238 285,246 290,238" fill="currentColor"/>
  <!-- 방법 1: HLSL 직접 -->
  <rect x="50" y="248" width="170" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="135" y="266" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">HLSL 코드 직접 작성</text>
  <text x="135" y="282" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(코드 기반)</text>
  <!-- 방법 2: Shader Graph -->
  <rect x="250" y="248" width="170" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="335" y="266" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Shader Graph</text>
  <text x="335" y="282" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(노드 기반, HLSL 자동 생성)</text>
  <!-- 하단 결론 -->
  <text x="235" y="322" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">최종 결과는 모두 HLSL 셰이더</text>
</svg>
</div>

---

## Unity의 머티리얼 시스템

앞서 다룬 머티리얼과 셰이더의 일반 구조가 Unity에서는 어떻게 구현되는지 살펴봅니다.

<br>

### 머티리얼과 셰이더의 관계

Unity에서 머티리얼은 하나의 셰이더를 참조하고, 그 셰이더가 정의한 프로퍼티 값을 저장합니다. Inspector 창에서 텍스처, 색상, 수치 등을 설정하면, 렌더링 시 이 값들이 셰이더에 전달됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 머티리얼 A -->
  <rect x="20" y="8" width="225" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="132" y="28" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">머티리얼 A</text>
  <line x1="30" y1="36" x2="235" y2="36" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="36" y="54" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_MainTex</text>
  <text x="230" y="54" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">벽돌 텍스처</text>
  <text x="36" y="72" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_Metallic</text>
  <text x="230" y="72" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">0.0</text>
  <text x="36" y="90" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_Smoothness</text>
  <text x="230" y="90" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">0.3</text>
  <text x="36" y="108" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_BumpMap</text>
  <text x="230" y="108" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">벽돌 노멀 맵</text>
  <!-- 머티리얼 B -->
  <rect x="275" y="8" width="225" height="120" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="387" y="28" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">머티리얼 B</text>
  <line x1="285" y1="36" x2="490" y2="36" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="291" y="54" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_MainTex</text>
  <text x="485" y="54" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">금속 텍스처</text>
  <text x="291" y="72" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_Metallic</text>
  <text x="485" y="72" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">0.9</text>
  <text x="291" y="90" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_Smoothness</text>
  <text x="485" y="90" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">0.7</text>
  <text x="291" y="108" text-anchor="start" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">_BumpMap</text>
  <text x="485" y="108" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">금속 노멀 맵</text>
  <!-- 참조 화살표 (머티리얼 → 셰이더) -->
  <line x1="132" y1="128" x2="132" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <line x1="387" y1="128" x2="387" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <line x1="132" y1="158" x2="387" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <line x1="260" y1="158" x2="260" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="255,178 260,186 265,178" fill="currentColor"/>
  <!-- 공유 셰이더 -->
  <rect x="160" y="188" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="211" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Standard Shader</text>
  <!-- 하단 결론 -->
  <text x="260" y="254" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">같은 셰이더, 다른 프로퍼티 → 별도 머티리얼</text>
</svg>
</div>

<br>

프로퍼티 값이 하나라도 다르면 별도의 머티리얼로 취급되어 드로우콜이 분리됩니다. 같은 셰이더와 프로퍼티를 사용하는 오브젝트라면 머티리얼을 통합하여 드로우콜을 줄일 수 있습니다.

### 머티리얼과 드로우콜

오브젝트를 렌더링할 때, 머티리얼이 바뀌면 CPU는 셰이더, 렌더 스테이트, 프로퍼티를 GPU에 새로 설정해야 합니다. 이 상태 전환 명령을 **셋 패스 콜(SetPass Call)**이라 합니다.

상태가 설정된 후 CPU가 메쉬, 변환 행렬, 오브젝트별 라이팅 데이터(라이트 프로브 계수, 라이트맵 UV 등)를 지정하여 GPU에 그리라는 명령을 보내는 것이 **드로우콜(Draw Call)**입니다.

<br>

드로우콜마다 CPU는 오브젝트별 데이터를 설정하고 **커맨드 버퍼(Command Buffer)**에 명령을 기록해야 합니다. 오브젝트가 수백~수천 개로 늘어나면 드로우콜 수도 함께 증가하여 CPU 측 병목이 될 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 상단 섹션: 머티리얼이 모두 다를 때 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">머티리얼이 모두 다를 때</text>
  <!-- 오브젝트 1 → 드로우콜 1 -->
  <rect x="30" y="36" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 1 : 머티리얼 A</text>
  <line x1="200" y1="51" x2="340" y2="51" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="338,46 346,51 338,56" fill="currentColor"/>
  <rect x="350" y="36" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 1</text>
  <!-- 오브젝트 2 → 드로우콜 2 -->
  <rect x="30" y="74" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 2 : 머티리얼 B</text>
  <line x1="200" y1="89" x2="340" y2="89" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="338,84 346,89 338,94" fill="currentColor"/>
  <rect x="350" y="74" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 2</text>
  <!-- 오브젝트 3 → 드로우콜 3 -->
  <rect x="30" y="112" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="132" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 3 : 머티리얼 C</text>
  <line x1="200" y1="127" x2="340" y2="127" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="338,122 346,127 338,132" fill="currentColor"/>
  <rect x="350" y="112" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="132" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 3</text>
  <!-- 오브젝트 4 → 드로우콜 4 -->
  <rect x="30" y="150" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="170" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 4 : 머티리얼 D</text>
  <line x1="200" y1="165" x2="340" y2="165" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="338,160 346,165 338,170" fill="currentColor"/>
  <rect x="350" y="150" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="170" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 4</text>
  <!-- 합계 -->
  <text x="410" y="202" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합계: 드로우콜 4회</text>
  <!-- 구분선 -->
  <line x1="40" y1="222" x2="520" y2="222" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <!-- 하단 섹션: 같은 머티리얼을 공유할 때 -->
  <text x="280" y="248" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">같은 머티리얼을 공유할 때 (배칭 가능)</text>
  <!-- 오브젝트 1 머티리얼 A -->
  <rect x="30" y="264" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="284" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 1 : 머티리얼 A</text>
  <!-- 오브젝트 2 머티리얼 A -->
  <rect x="30" y="302" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="322" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 2 : 머티리얼 A</text>
  <!-- 오브젝트 3 머티리얼 A -->
  <rect x="30" y="340" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="360" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 3 : 머티리얼 A</text>
  <!-- 배칭 화살표: 3개 → 드로우콜 1 -->
  <line x1="200" y1="279" x2="250" y2="279" stroke="currentColor" stroke-width="1.5"/>
  <line x1="250" y1="279" x2="250" y2="355" stroke="currentColor" stroke-width="1.5"/>
  <line x1="200" y1="317" x2="250" y2="317" stroke="currentColor" stroke-width="1.5"/>
  <line x1="200" y1="355" x2="250" y2="355" stroke="currentColor" stroke-width="1.5"/>
  <line x1="250" y1="317" x2="340" y2="317" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="338,312 346,317 338,322" fill="currentColor"/>
  <rect x="350" y="302" width="160" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="430" y="322" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 1 (배칭)</text>
  <!-- 오브젝트 4 머티리얼 B → 드로우콜 2 -->
  <rect x="30" y="384" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="404" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트 4 : 머티리얼 B</text>
  <line x1="200" y1="399" x2="340" y2="399" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="338,394 346,399 338,404" fill="currentColor"/>
  <rect x="350" y="384" width="160" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="430" y="404" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 2</text>
  <!-- 합계 -->
  <text x="430" y="434" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합계: 드로우콜 2회</text>
</svg>
</div>

<br>

**배칭(Batching)**은 동일한 머티리얼을 사용하는 여러 오브젝트의 메쉬를 합쳐 더 적은 수의 드로우콜로 그리는 기법입니다.

<br>

머티리얼이 다르면 셋 패스 콜(상태 전환)이 늘고 배칭 기회도 줄어들므로, **텍스처 아틀라스(Texture Atlas)**(여러 텍스처를 하나로 합치는 기법)를 사용하거나 유사한 오브젝트끼리 같은 머티리얼을 공유하도록 설계하여 머티리얼 수를 줄이는 것이 성능 최적화의 기본입니다.

### 셰이더 변형 (Shader Variants)

머티리얼마다 사용하는 기능 조합이 다를 수 있습니다. 예를 들어 노멀 맵을 쓰는 머티리얼은 노멀 맵 샘플링 코드가 포함된 셰이더가 필요하고, 쓰지 않는 머티리얼은 해당 코드가 빠진 셰이더가 필요합니다.

Unity는 이런 조합마다 별도의 셰이더 파일을 작성하는 대신, 하나의 셰이더 소스에 키워드를 정의하고 조합별로 다른 버전을 컴파일합니다. 이 각각의 컴파일 결과를 **셰이더 변형(Shader Variant)**이라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Standard Shader 루트 -->
  <rect x="160" y="10" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="33" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Standard Shader</text>
  <!-- 수직 줄기 -->
  <line x1="260" y1="46" x2="260" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <!-- 변형 1 -->
  <line x1="260" y1="72" x2="290" y2="72" stroke="currentColor" stroke-width="1.5"/>
  <rect x="290" y="56" width="210" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="395" y="77" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">_NORMALMAP ON + _METALLIC ON</text>
  <text x="395" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">변형 1</text>
  <!-- 변형 2 -->
  <line x1="260" y1="118" x2="290" y2="118" stroke="currentColor" stroke-width="1.5"/>
  <rect x="290" y="102" width="210" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="395" y="123" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">_NORMALMAP ON + _METALLIC OFF</text>
  <text x="395" y="98" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">변형 2</text>
  <!-- 변형 3 -->
  <line x1="260" y1="164" x2="290" y2="164" stroke="currentColor" stroke-width="1.5"/>
  <rect x="290" y="148" width="210" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="395" y="169" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">_NORMALMAP OFF + _METALLIC ON</text>
  <text x="395" y="144" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">변형 3</text>
  <!-- 변형 4 -->
  <line x1="260" y1="210" x2="290" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <rect x="290" y="194" width="210" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="395" y="215" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">_NORMALMAP OFF + _METALLIC OFF</text>
  <text x="395" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">변형 4</text>
  <!-- 하단 보조 텍스트 -->
  <text x="260" y="258" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">키워드 2개 x 각 2가지 옵션 = 4개 변형</text>
  <text x="260" y="276" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">키워드가 N개이면 최대 2^N개 변형이 생성될 수 있음</text>
</svg>
</div>

<br>

위 예시에서는 키워드가 2개뿐이지만, 실제 셰이더는 그림자, 안개, 라이트맵 등 다양한 키워드를 포함하므로 변형 수가 수백~수천 개로 급증할 수 있습니다.

변형이 많아지면 빌드 시간과 메모리 사용량이 늘어나고, 빌드 시점에 미리 컴파일되지 않은 변형이 런타임에 처음 사용되면 그 자리에서 셰이더 컴파일이 발생하여 순간적인 끊김이 생길 수 있습니다.

<br>

이를 관리하기 위해 사용하지 않는 키워드를 제거하거나, **셰이더 변형 스트리핑**으로 불필요한 변형을 빌드에서 제거하여 변형 수와 빌드 크기를 줄입니다.
런타임에 필요한 변형은 **Shader Variant Collection**으로 미리 컴파일(프리워밍)해 두면 끊김을 방지할 수 있습니다.

---

## 메쉬, 텍스처, 머티리얼의 관계 — 렌더링의 입력 데이터

[Part 1](/dev/unity/RenderingFoundation-1/)부터 이 글까지 세 편에 걸쳐 렌더링의 입력 데이터를 구성하는 세 가지 요소를 살펴보았습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 오브젝트 외곽 박스 -->
  <rect x="20" y="10" width="520" height="310" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="36" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">오브젝트</text>
  <!-- 메쉬 박스 -->
  <rect x="42" y="52" width="130" height="200" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="107" y="76" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">메쉬</text>
  <line x1="55" y1="86" x2="159" y2="86" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="107" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">정점</text>
  <text x="107" y="126" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">인덱스</text>
  <text x="107" y="146" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">UV</text>
  <text x="107" y="166" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">법선</text>
  <text x="107" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">탄젠트</text>
  <text x="107" y="206" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">버텍스 컬러</text>
  <text x="107" y="226" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">...</text>
  <!-- 메쉬 하단 보조 텍스트 -->
  <text x="107" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">형태를 정의</text>
  <!-- 머티리얼 박스 -->
  <rect x="200" y="52" width="318" height="250" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="359" y="76" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">머티리얼</text>
  <line x1="213" y1="86" x2="505" y2="86" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <!-- 셰이더 내부 박스 -->
  <rect x="218" y="96" width="120" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="278" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">셰이더</text>
  <line x1="230" y1="126" x2="326" y2="126" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="278" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">버텍스</text>
  <text x="278" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트</text>
  <!-- 파라미터 내부 박스 -->
  <rect x="356" y="96" width="144" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="428" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">파라미터</text>
  <line x1="368" y1="126" x2="488" y2="126" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <!-- 파라미터 내부 항목 박스 -->
  <rect x="372" y="136" width="112" height="78" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="428" y="156" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">텍스처</text>
  <text x="428" y="174" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">색상</text>
  <text x="428" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">반사도</text>
  <text x="428" y="208" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">...</text>
  <!-- 머티리얼 하단 보조 텍스트 -->
  <text x="359" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">외관을 결정</text>
  <!-- 화살표: 오브젝트 → GPU로 전달 -->
  <line x1="280" y1="320" x2="280" y2="354" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,352 280,360 285,352" fill="currentColor"/>
  <text x="280" y="380" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU로 전달</text>
  <!-- 화살표: GPU로 전달 → 렌더링 파이프라인 -->
  <line x1="280" y1="388" x2="280" y2="414" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,412 280,420 285,412" fill="currentColor"/>
  <rect x="180" y="422" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="443" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">렌더링 파이프라인</text>
</svg>
</div>

<br>

**메쉬**는 정점, 인덱스, UV, 법선, 탄젠트, 버텍스 컬러 등으로 오브젝트의 형태를 정의합니다.

**텍스처**는 표면의 색상, 노멀, 러프니스 등을 2D 이미지로 담는 데이터입니다.

**머티리얼**은 셰이더와 파라미터(텍스처 포함)를 묶어 메쉬 표면의 외관을 정의합니다.

<br>

렌더링 파이프라인에는 이 세 가지 외에도 트랜스폼, 카메라, 라이팅 데이터 등이 입력되지만, 이 세 가지가 오브젝트의 시각적 결과물을 구성하는 핵심 에셋입니다.

---

## 마무리

머티리얼은 셰이더와 파라미터를 묶어 메쉬 표면의 외관을 정의합니다. 이 글에서는 셰이더의 구조, 렌더 스테이트, 드로우콜의 관계를 살펴보았습니다.

이 글에서 다룬 핵심을 정리하면 다음과 같습니다.

- 머티리얼은 셰이더(GPU 프로그램)와 파라미터(텍스처, 색상, 반사도 등)를 묶은 단위입니다
- 셰이더는 버텍스 셰이더(정점 좌표 변환)와 프래그먼트 셰이더(픽셀 색상 계산)로 나뉘며, 프래그먼트 수가 정점 수보다 수십~수백 배 많아 프래그먼트 셰이더의 복잡도가 성능에 직접적인 영향을 줍니다
- GPU는 셰이더 외에도 블렌딩, 깊이 테스트, 스텐실 테스트, 컬링 같은 렌더 스테이트 설정이 필요하며, 스테이트 변경이 잦을수록 성능이 떨어집니다
- 셰이더는 고정 기능 파이프라인에서 프로그래머블 셰이더로 발전하여, 개발자가 조명 모델과 시각 효과를 직접 구현할 수 있게 되었습니다
- 머티리얼이 바뀌면 셋 패스 콜(상태 전환 명령)이 발생하고, 각 오브젝트마다 드로우콜(그리기 명령)이 발생합니다
- 같은 머티리얼을 공유하는 오브젝트끼리 배칭으로 묶으면 드로우콜을 줄일 수 있습니다
- 셰이더 변형은 키워드 조합에 따라 급증할 수 있으므로, 불필요한 변형을 제거하고 필요한 변형을 프리워밍하여 관리합니다

세 편에 걸쳐 살펴본 메쉬, 텍스처, 머티리얼/셰이더는 렌더링 파이프라인에 입력되는 핵심 에셋입니다. 다음 시리즈에서는 이 데이터를 실제로 처리하는 GPU의 내부 구조를 살펴봅니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)

**시리즈**
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- **렌더링 기초 (3) - 머티리얼과 셰이더 기초 (현재 글)**

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- **렌더링 기초 (3) - 머티리얼과 셰이더 기초** (현재 글)
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
