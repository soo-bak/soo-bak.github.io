---
layout: single
title: "조명과 그림자 (1) - 실시간 조명과 베이크 - soo:bak"
date: "2026-02-17 19:22:00 +0900"
description: 실시간 라이팅 비용, Built-in 멀티패스와 URP 싱글패스, 베이크 라이팅, Light Probe, Mixed 라이팅을 설명합니다.
tags:
  - Unity
  - 최적화
  - 라이팅
  - 베이크
---

## 조명이라는 비용의 시작

[UI 최적화 시리즈](/dev/unity/UIOptimization-1/)에서는 Canvas Rebuild, 오버드로우, 드로우콜 증가가 UI 렌더링 비용을 키우는 과정을 다루었습니다.

이 글부터 다루는 **라이팅(Lighting)**은 렌더링 비용에서 또 다른 큰 비중을 차지하는 서브시스템입니다.

UI가 2D 요소를 효율적으로 화면에 올리는 문제였다면, 라이팅은 3D 씬의 오브젝트가 어떤 빛을 받고 어떤 그림자를 만드는지 계산하는 문제입니다.

<br>

현실 세계에서 빛은 광원에서 출발해 표면에서 반사되고, 그 반사광이 다른 표면에 닿아 다시 반사됩니다.

이 과정을 정확히 시뮬레이션하면 사실적인 이미지를 얻을 수 있지만, 계산량이 너무 커서 실시간 렌더링으로는 감당하기 어렵습니다.

영화 VFX가 한 프레임에 수 분에서 수 시간을 쓰기도 하는 데 반해, 게임은 같은 일을 16ms(60fps) 안에 끝내야 합니다.

이 시간 안에 모든 빛의 반사 과정을 직접 계산할 수는 없으므로, 게임 렌더링은 일부 라이트만 실시간으로 처리하고 나머지는 근사하거나 미리 계산합니다.

이렇게 비용을 줄여도 실시간 라이트는 수가 늘 때마다 부담이 빠르게 커집니다. 라이트가 하나 추가될 때마다 프래그먼트 셰이더가 해야 하는 연산이 늘고, 그림자를 켜면 별도의 렌더 패스까지 필요해지기 때문입니다.

이 비용 구조를 구체적으로 파악하기 위해, 먼저 실시간 라이트 하나가 GPU에서 어떤 연산을 더하는지, 파이프라인 구조에 따라 드로우콜과 셰이더 복잡도가 어떻게 달라지는지를 살펴봅니다.

이어서 베이크 라이팅, Light Probe, Reflection Probe, Mixed 라이팅이 각각 어떤 비용을 줄이고 어떤 제약을 갖는지를 순서대로 다룹니다.

---

## 실시간 라이팅의 비용

실시간 라이트 하나가 추가될 때 발생하는 비용은 파이프라인 구조에 따라 드로우콜로 나타나기도 하고, 셰이더 복잡도로 나타나기도 합니다.

어느 쪽이든 비용이 누적되면 씬에 둘 수 있는 실시간 라이트의 개수가 제한됩니다.

### 라이트 1개의 셰이더 비용

실시간 라이트가 1개 있을 때 프래그먼트 셰이더는 각 프래그먼트마다 라이트와 표면의 상호작용을 계산합니다.

셰이더가 참조하는 기본 정보는 광원의 방향과 색상, 그리고 광원에서 멀어질수록 빛의 세기가 줄어드는 정도를 가리키는 **감쇠(Attenuation)**입니다.

셰이더는 이 정보로 모든 방향으로 고르게 반사되는 **확산 반사(Diffuse)**와 특정 방향으로 집중되는 **정반사(Specular)**를 구한 뒤, 두 성분을 합산해 프래그먼트의 최종 색상을 결정합니다.

실시간 라이트가 2개라면 프래그먼트 셰이더는 이 과정을 2번, 3개라면 3번 반복해야 하는 등, 연산량이 실시간 라이트 수에 비례해 선형으로 늘어납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">라이트 수에 따른 프래그먼트 셰이더 비용</text>

  <!-- === 칸 1: 라이트 1개 (1 묶음, 시작 y=280) === -->
  <text x="90" y="294" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">라이트 1</text>
  <rect x="40" y="302" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="312" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">라이트 방향</text>
  <rect x="40" y="318" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="328" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">NdotL</text>
  <rect x="40" y="334" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="344" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">감쇠(Attenuation)</text>
  <rect x="40" y="350" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="360" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">확산 반사(Diffuse)</text>
  <rect x="40" y="366" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정반사(Specular)</text>

  <!-- === 칸 2: 라이트 2개 (2 묶음, 시작 y=172, 280) === -->
  <!-- 묶음 1 (라이트 1) -->
  <text x="270" y="186" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">라이트 1</text>
  <rect x="220" y="194" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="204" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">라이트 방향</text>
  <rect x="220" y="210" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">NdotL</text>
  <rect x="220" y="226" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="236" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">감쇠(Attenuation)</text>
  <rect x="220" y="242" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="252" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">확산 반사(Diffuse)</text>
  <rect x="220" y="258" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정반사(Specular)</text>
  <!-- 묶음 2 (라이트 2) -->
  <text x="270" y="294" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">라이트 2</text>
  <rect x="220" y="302" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="312" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">라이트 방향</text>
  <rect x="220" y="318" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="328" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">NdotL</text>
  <rect x="220" y="334" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="344" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">감쇠(Attenuation)</text>
  <rect x="220" y="350" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="360" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">확산 반사(Diffuse)</text>
  <rect x="220" y="366" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="270" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정반사(Specular)</text>

  <!-- === 칸 3: 라이트 3개 (3 묶음, 시작 y=64, 172, 280) === -->
  <!-- 묶음 1 (라이트 1) -->
  <text x="450" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">라이트 1</text>
  <rect x="400" y="86" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">라이트 방향</text>
  <rect x="400" y="102" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">NdotL</text>
  <rect x="400" y="118" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="128" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">감쇠(Attenuation)</text>
  <rect x="400" y="134" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">확산 반사(Diffuse)</text>
  <rect x="400" y="150" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="160" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정반사(Specular)</text>
  <!-- 묶음 2 (라이트 2) -->
  <text x="450" y="186" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">라이트 2</text>
  <rect x="400" y="194" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="204" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">라이트 방향</text>
  <rect x="400" y="210" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">NdotL</text>
  <rect x="400" y="226" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="236" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">감쇠(Attenuation)</text>
  <rect x="400" y="242" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="252" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">확산 반사(Diffuse)</text>
  <rect x="400" y="258" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="268" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정반사(Specular)</text>
  <!-- 묶음 3 (라이트 3) -->
  <text x="450" y="294" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor" opacity="0.7">라이트 3</text>
  <rect x="400" y="302" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="312" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">라이트 방향</text>
  <rect x="400" y="318" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="328" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">NdotL</text>
  <rect x="400" y="334" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="344" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">감쇠(Attenuation)</text>
  <rect x="400" y="350" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="360" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">확산 반사(Diffuse)</text>
  <rect x="400" y="366" width="100" height="14" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="450" y="376" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정반사(Specular)</text>

  <!-- x축 baseline -->
  <line x1="20" y1="384" x2="520" y2="384" stroke="currentColor" stroke-width="1" opacity="0.4"/>

  <!-- x축 라벨 (라이트 수) -->
  <text x="90" y="402" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">라이트 1개</text>
  <text x="270" y="402" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">라이트 2개</text>
  <text x="450" y="402" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">라이트 3개</text>

  <!-- ALU 합계 -->
  <text x="90" y="422" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">약 20~30 ALU</text>
  <text x="270" y="422" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">약 40~60 ALU</text>
  <text x="450" y="422" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">약 60~90 ALU (3배)</text>

  <!-- 하단 주석 -->
  <text x="270" y="446" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">라이트가 늘어날 때마다 같은 5단계 ALU 연산이 그대로 반복</text>
</svg>
</div>

<br>

이 조명 계산은 화면에 보이는 모든 프래그먼트에서 반복됩니다. 1080p 해상도(1920×1080)에서 화면 절반을 차지하는 오브젝트는 약 100만 개의 프래그먼트를 생성합니다. 라이트가 3개라면 프레임당 100만 × 3 = 300만 회의 조명 계산이 수행됩니다.

### Built-in 멀티패스에서의 비용

Built-in 파이프라인은 멀티패스 포워드 렌더링을 사용해, 실시간 라이트가 추가될 때마다 같은 오브젝트를 다시 그립니다.

첫 패스 ForwardBase가 메인 Directional Light와 환경광을 처리한 뒤 추가 실시간 라이트마다 ForwardAdd 패스가 한 번씩 더해지므로, **드로우콜은 라이트 수와 화면 오브젝트 수의 곱만큼 발생합니다**.

> Built-in 파이프라인의 구조와 패스 흐름은 [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)에서 자세히 다룹니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 530" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Built-in 멀티패스의 드로우콜 증가</text>

  <!-- === 씬 구성 === -->
  <rect x="20" y="46" width="560" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="36" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">씬 구성</text>

  <rect x="36" y="80" width="170" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="121" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트: 100개</text>

  <rect x="216" y="80" width="348" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">픽셀 라이트: 3개 (Directional 1 + Point 2)</text>

  <!-- === 각 오브젝트당 패스 === -->
  <rect x="20" y="138" width="560" height="106" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="36" y="160" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">각 오브젝트당 패스</text>

  <rect x="36" y="172" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="136" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">ForwardBase: 1회</text>

  <!-- plus sign -->
  <text x="251" y="197" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">+</text>

  <rect x="266" y="172" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="366" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">ForwardAdd: 2회</text>

  <!-- equals sign -->
  <text x="481" y="197" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">=</text>

  <rect x="496" y="172" width="68" height="32" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text x="530" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">3회</text>

  <!-- sub labels -->
  <text x="136" y="222" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Directional + 환경광</text>
  <text x="366" y="222" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">추가 라이트 2개</text>
  <text x="530" y="222" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">합계</text>

  <!-- 전체 드로우콜 공식 -->
  <text x="300" y="238" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">전체 드로우콜: 100 오브젝트 × 3 패스 = 300 드로우콜</text>

  <!-- === 라이트 수별 드로우콜 막대 그래프 === -->
  <rect x="20" y="260" width="560" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="36" y="282" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">라이트 수별 드로우콜 (오브젝트 100개)</text>

  <!-- Bar chart: bars start at x=130, length scaled (100 DC = 100px). So 400 DC = 400px, ends at 530 -->
  <!-- 라이트 1개 -->
  <text x="120" y="314" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">라이트 1개</text>
  <rect x="130" y="300" width="100" height="22" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="315" font-family="sans-serif" font-size="10" fill="currentColor">100 오브젝트 × 1 패스 = 100 드로우콜</text>

  <!-- 라이트 2개 -->
  <text x="120" y="348" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">라이트 2개</text>
  <rect x="130" y="334" width="200" height="22" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="349" font-family="sans-serif" font-size="10" fill="currentColor">100 오브젝트 × 2 패스 = 200 드로우콜</text>

  <!-- 라이트 3개 -->
  <text x="120" y="382" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">라이트 3개</text>
  <rect x="130" y="368" width="300" height="22" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="440" y="383" font-family="sans-serif" font-size="10" fill="currentColor">100 오브젝트 × 3 패스 = 300 드로우콜</text>

  <!-- 라이트 4개 (초과 강조) -->
  <text x="120" y="416" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">라이트 4개</text>
  <rect x="130" y="402" width="400" height="22" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text x="325" y="417" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">100 오브젝트 × 4 패스 = 400 드로우콜</text>

  <!-- X-axis baseline -->
  <line x1="130" y1="440" x2="530" y2="440" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="130" y="454" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">0</text>
  <text x="230" y="454" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">100</text>
  <text x="330" y="454" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">200</text>
  <text x="430" y="454" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">300</text>
  <text x="530" y="454" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">400</text>
  <text x="330" y="478" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">드로우콜 수</text>

  <!-- Bottom conclusion -->
  <line x1="30" y1="504" x2="50" y2="504" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="50,500 60,504 50,508" fill="currentColor"/>
  <text x="70" y="508" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">라이트 하나 추가 = 오브젝트 수만큼 드로우콜 추가</text>
</svg>
</div>

<br>

이렇게 드로우콜이 늘어나면 CPU 부담도 그만큼 커집니다. CPU가 GPU에 명령을 제출하는 횟수가 늘고, 그중 셰이더나 머티리얼이 바뀌는 호출에서는 GPU의 렌더링 상태를 새로 설정하는 **SetPass Call**까지 더해지기 때문입니다.

### URP 싱글패스에서의 비용

URP는 싱글패스 포워드 렌더링을 사용하므로, GPU 버퍼에 일괄 전달된 실시간 라이트 정보를 셰이더 내부에서 한 번에 처리합니다. 따라서 실시간 라이트마다 ForwardAdd 패스를 더하는 Built-in과 달리, 라이트가 1개든 8개든 오브젝트 100개의 드로우콜은 100회로 일정합니다.

그 대신 GPU 부담이 늘어납니다. 프래그먼트 셰이더가 모든 실시간 라이트에 대해 방향·감쇠·Diffuse/Specular를 한 번씩 다시 계산해야 하기 때문에, 라이트가 늘어날수록 GPU 연산이 그에 비례해 무거워집니다.

즉 **이 방식의 부담은 CPU 드로우콜이 아니라 GPU 셰이더 연산에 집중됩니다**. URP에서 오브젝트당 실시간 라이트 수를 기본 4개, 최대 8개로 제한하는 이유도 이 GPU 부담을 통제하기 위함입니다.

이 GPU 부담은 게임 성능과 직결됩니다. 셰이더가 무거워질수록 한 프래그먼트의 처리 시간이 길어지고, 같은 시간 안에 처리할 수 있는 프래그먼트 수가 줄어들어 결국 프레임 레이트가 떨어집니다.

> GPU의 ALU(Arithmetic Logic Unit) 자원과 라이트 수에 따른 셰이더 비용은 [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서 더 자세히 다룹니다. 본 글 후반 〈필레이트 제한과 프래그먼트 비용〉 섹션에서도 라이팅 관점에서 이 관계를 다시 살펴봅니다.

<br>

### 실시간 라이트 수의 한계

병목 위치는 Built-in의 경우 드로우콜, URP의 경우 셰이더 복잡도로 다르지만, 어느 쪽이든 실시간 라이트 수를 계속 늘리기는 어렵습니다. 라이트가 늘어날수록 CPU가 제출해야 하는 렌더링 명령이 늘거나, GPU가 프래그먼트마다 반복해야 하는 조명 계산이 증가하기 때문입니다.

성능 예산이 제한된 프로젝트에서는 흔히 실시간 라이트를 메인 Directional Light 중심으로 줄입니다. 다만 평행광인 Directional Light는 거리에 따른 감쇠가 없어 간접광이나 국지적인 조명까지 다루기는 어렵기 때문에, 그 부족한 부분을 미리 계산해 라이트맵 텍스처에 담아 두는 **베이크 라이팅(Baked Lighting)**을 함께 사용합니다.

---

## 베이크 라이팅 (Baked Lighting)

베이크 라이팅(Baked Lighting)은 정적 환경의 조명을 미리 계산해 라이트맵에 담아 두는 사전 계산 기법입니다. 라이트 수와 무관하게 런타임 비용을 줄여 주는 대신, 사전 계산의 특성상 적용할 수 있는 대상과 갱신 방식에 한계가 있습니다.

이어지는 세 절에서 베이크 라이팅의 메커니즘과 라이트맵의 구조, 그 한계를 순서대로 다룹니다.

### 베이크 라이팅의 메커니즘

베이크 단계에서는 Unity의 Lightmapper가 정적 오브젝트의 각 표면에 빛이 어떻게 도달하는지를 광선 추적(Ray Tracing)으로 미리 계산합니다. 광원이 직접 비추는 빛(직접광, Direct Light)뿐 아니라 다른 표면에서 튕겨 나오는 빛(간접광, Indirect Light)까지 함께 추적해, 표면이 받는 실제 밝기와 색을 구합니다.

이렇게 추적한 결과는 표면 위의 작은 격자(텍셀, Texel) 하나하나에 RGB 색 값으로 기록되어 한 장의 텍스처를 이룹니다. 이 텍스처가 **라이트맵(Lightmap)**이며, 라이트맵 한 텍셀에는 그 자리의 표면이 받는 모든 빛이 이미 합쳐진 최종 조명만 담겨 있습니다.

런타임에는 각 정적 오브젝트가 자신의 UV 좌표를 사용해 라이트맵에서 자기 자리에 해당하는 텍셀을 읽어 옵니다. 읽어 온 조명 값은 오브젝트의 표면 색(알베도, Albedo)과 곱해져 화면에 보이는 최종 색이 됩니다.

<br>

### 라이트맵의 구조

라이트맵은 표면의 각 지점에 도달한 빛의 밝기와 색을 텍셀 하나에 따로 저장합니다. 따라서 각 텍셀이 표면의 어느 지점에 해당하는지 알려 주는 좌표가 필요합니다. 이 좌표를 제공하는 것이 메쉬의 UV 좌표계이며, 라이트맵은 메인 텍스처가 쓰는 채널을 그대로 쓰지 않고 메쉬가 가진 다른 UV 채널을 사용합니다.

> 메쉬의 UV 좌표계가 3D 표면과 2D 텍스처를 연결하는 방식은 [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 자세히 다룹니다.

라이트맵을 메인 텍스처와 같은 UV0으로 읽지 않는 이유는, 두 텍스처가 좌표를 사용하는 방식이 다르기 때문입니다. 메인 텍스처는 표면의 기본 무늬를 입히는 용도라서, 같은 좌표를 여러 표면에서 반복해서 읽어도 문제가 되지 않습니다. 만약 여러 표면이 같은 벽돌 무늬를 읽는다면, 각 표면에 같은 벽돌 패턴이 반복되어 보일 뿐입니다. 타일링이나 미러링을 UV0에서 자연스럽게 사용할 수 있는 이유도 여기에 있습니다.

반면 라이트맵은 표면의 각 위치가 받은 조명 결과를 저장합니다. 같은 벽돌 벽 안에서도 그늘에 가려진 부분과 햇빛을 받는 부분은 서로 다른 밝기를 가져야 합니다. 만약 두 위치가 라이트맵에서 같은 (u, v) 좌표를 가리키면, 하나의 텍셀이 두 위치의 조명 값을 동시에 대표해야 합니다. 이 경우 어느 한쪽 표면에는 맞지 않는 조명이 적용됩니다.

그래서 라이트맵에는 반복이나 겹침이 없는 별도의 UV가 필요합니다. 이 용도로 사용하는 채널이 두 번째 UV 채널인 UV1입니다. 다만 Unity C# API에서는 이 채널을 `Mesh.uv2`로 접근하므로, 채널 번호와 프로퍼티 이름이 한 칸씩 어긋나 보입니다.

베이크가 끝나면 벽, 바닥, 기둥처럼 여러 정적 오브젝트의 조명 결과가 하나의 라이트맵 안에 배치됩니다. 
이때 라이트맵은 아틀라스처럼 쓰이며, 오브젝트마다 자신이 읽을 영역이 따로 배정됩니다. 각 오브젝트의 UV1은 그 배정된 영역만 가리키므로, 같은 라이트맵을 공유해도 다른 오브젝트의 조명 값을 읽지 않습니다. 다만 한 오브젝트에 배정된 영역이 너무 작으면 사용할 수 있는 텍셀 수가 부족해져, 그림자 경계나 밝기 변화가 거친 계단처럼 보일 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">라이트맵의 두 UV 채널</text>

  <!-- ── 좌측: UV0 (메인 텍스처) ── -->
  <rect x="20" y="44" width="275" height="238" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="157" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">UV0 (메인 텍스처)</text>

  <!-- 벽돌 패턴 텍스처 영역 -->
  <rect x="112" y="82" width="90" height="90" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <!-- 벽돌 패턴(간단한 격자) -->
  <line x1="112" y1="112" x2="202" y2="112" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="112" y1="142" x2="202" y2="142" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="142" y1="82"  x2="142" y2="112" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="172" y1="82"  x2="172" y2="112" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="127" y1="112" x2="127" y2="142" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="157" y1="112" x2="157" y2="142" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="187" y1="112" x2="187" y2="142" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="142" y1="142" x2="142" y2="172" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <line x1="172" y1="142" x2="172" y2="172" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <text x="157" y="188" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">벽돌 패턴 텍스처</text>

  <!-- 여러 메쉬 면이 같은 UV 영역으로 매핑 -->
  <rect x="35"  y="214" width="56" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="63"  y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 1</text>

  <rect x="129" y="214" width="56" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="157" y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 2</text>

  <rect x="223" y="214" width="56" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="251" y="236" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 3</text>

  <!-- 화살표: 세 면 → 같은 UV 영역 -->
  <line x1="63"  y1="214" x2="130" y2="180" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polygon points="126,175 133,182 123,182" fill="currentColor"/>
  <line x1="157" y1="214" x2="157" y2="180" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polygon points="153,182 157,172 161,182" fill="currentColor"/>
  <line x1="251" y1="214" x2="184" y2="180" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polygon points="188,175 181,182 191,182" fill="currentColor"/>

  <text x="157" y="270" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">겹침 허용 (타일링/미러링 가능)</text>

  <!-- ── 우측: UV1 (라이트맵) ── -->
  <rect x="305" y="44" width="275" height="238" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="442" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">UV1 (라이트맵)</text>

  <!-- 큰 라이트맵 평면 -->
  <rect x="320" y="82" width="245" height="165" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 서로 겹치지 않는 영역들 -->
  <rect x="330" y="92"  width="74" height="42" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="367" y="117" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">벽 A</text>

  <rect x="412" y="92"  width="66" height="42" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="445" y="117" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">벽 B</text>

  <rect x="486" y="92"  width="70" height="64" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="521" y="128" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">기둥</text>

  <rect x="330" y="142" width="148" height="96" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="404" y="194" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">바닥</text>

  <rect x="486" y="164" width="70" height="74" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="521" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">천장</text>

  <text x="442" y="270" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">겹침 불가 (각 표면 위치 고유)</text>

  <!-- 하단 주석 -->
  <text x="300" y="310" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Unity C# API에서 UV1 채널은 Mesh.uv2로 접근</text>
</svg>
</div>

<br>

라이트맵에는 정적 표면이 받을 조명 결과가 미리 저장됩니다. 이 결과에는 광원에서 표면으로 바로 도달하는 **직접광(Direct Light)**뿐 아니라, 다른 표면에 반사된 뒤 도달하는 **간접광(Indirect Light)**도 포함될 수 있습니다.

간접광은 장면의 분위기를 만드는 데 큰 영향을 줍니다. 예를 들어 붉은 벽에 닿은 빛이 다시 흰색 바닥으로 반사되면, 바닥에도 은은한 붉은 기운이 더해집니다. 이런 현상을 **컬러 블리딩(Color Bleeding)**이라고 합니다.

만약 이런 간접광을 런타임에 매 프레임 정확히 계산하려면 많은 광선 추적이나 복잡한 근사 계산이 필요합니다. 일반적인 실시간 렌더링에서는 부담이 크기 때문에, Unity는 베이크 과정에서 직접광과 간접광을 미리 계산해 라이트맵에 기록합니다.

런타임에는 셰이더가 라이트맵을 샘플링해 이미 계산된 조명 값을 읽기만 하면 됩니다. 덕분에 정적 환경에서는 색 번짐, 부드러운 밝기 변화, 간접광이 만든 공간감을 낮은 런타임 비용으로 표현할 수 있습니다.

### 베이크 라이팅의 제약

베이크 라이팅은 많은 조명 계산을 런타임 밖으로 옮기는 대신, 그 결과를 라이트맵 텍스처에 고정해 둡니다. 이 방식은 런타임 비용을 크게 줄여 주지만, 고정된 데이터라는 특성 때문에 몇 가지 제약이 생깁니다.

가장 기본적인 제약은 적용 대상입니다. 라이트맵은 특정 표면 위치가 받은 조명 값을 UV 좌표에 맞춰 저장합니다. 만약 오브젝트가 움직이거나 회전하면, 라이트맵에 기록된 조명 결과와 실제 표면 위치가 맞지 않게 됩니다. 그래서 캐릭터, NPC, 움직이는 소품 같은 동적 오브젝트에는 라이트맵을 그대로 적용하기 어렵습니다.

라이트맵은 텍스처 자원이므로 메모리도 사용합니다. 씬이 넓거나 정적 오브젝트의 표면이 많을수록 조명 값을 저장해야 할 영역이 늘어납니다. 여기에 그림자 경계나 간접광의 변화를 더 부드럽게 담으려면 더 많은 텍셀이 필요하므로, 라이트맵 해상도를 높이거나 라이트맵 장수를 늘려야 합니다. 예를 들어 압축하지 않은 1024×1024 RGBA 텍스처 한 장은 약 4MB를 차지하므로, 여러 장을 사용하는 씬에서는 라이트맵만으로도 수십 MB의 메모리를 사용할 수 있습니다.

베이크 시간도 고려해야 합니다. 직접광만 계산할 때보다 간접광의 반사까지 함께 계산할 때 처리량이 크게 늘어나고, 씬 구조나 라이트 배치를 수정하면 결과를 다시 베이크해야 합니다. 프로젝트 규모가 커질수록 수정 후 결과를 확인하기까지의 시간이 길어져, 작업 반복 속도에도 영향을 줍니다.

또한 라이트맵은 베이크 시점의 조명 상태를 저장한 결과입니다. 만약 런타임에 해가 이동하거나 라이트가 켜지고 꺼져야 한다면, 그 변화는 라이트맵에 자동으로 반영되지 않습니다. 이런 장면에서는 실시간 라이트, Mixed Lighting, 또는 별도의 연출용 조명 전략을 함께 고려해야 합니다.

이 제약은 동적 오브젝트를 정적 환경과 함께 렌더링할 때 특히 드러납니다. 캐릭터는 라이트맵 대상이 아니지만, 베이크된 환경 안에서 주변 조명과 어울려야 합니다. 만약 캐릭터가 밝은 복도에서 어두운 그늘로 이동했는데도 표면 밝기가 거의 변하지 않는다면, 주변 환경의 조명 상태와 맞지 않아 부자연스럽게 보입니다. 이 문제를 보완하는 장치가 **Light Probe**입니다.

---

## Light Probe

라이트맵은 벽, 바닥, 기둥처럼 움직이지 않는 표면에 조명 결과를 붙여 두는 방식입니다. 반면 Light Probe는 씬 안의 여러 지점에 조명 샘플을 배치해, 그 위치 주변의 밝기와 색감을 저장합니다. 캐릭터나 움직이는 소품은 라이트맵을 직접 사용할 수 없지만, 현재 위치 주변의 프로브 값을 이용해 표면 밝기와 색을 주변 환경에 맞출 수 있습니다.

### Light Probe의 역할

Light Probe는 씬 안의 특정 위치에서 주변 조명이 어떤 상태인지 미리 측정해 둔 지점입니다. 베이크 단계에서는 각 프로브 위치를 기준으로, 어느 방향에서 어떤 색과 밝기의 빛이 들어오는지를 계산합니다.

프로브 하나가 모든 방향의 빛을 세밀한 텍스처처럼 저장한다면 데이터가 너무 커집니다. 그래서 Unity는 이 조명 분포를 몇 개의 숫자로 요약해 저장합니다. 이때 사용하는 표현 방식이 **구면 조화 함수(Spherical Harmonics, SH)**입니다.

SH는 방향별 조명을 아주 정밀하게 저장하는 방식은 아니지만, 여러 방향에서 들어오는 부드러운 환경광과 간접광을 적은 데이터로 표현하는 데 적합합니다. 대신 날카로운 그림자나 뚜렷한 하이라이트처럼 고주파 변화가 큰 조명에는 적합하지 않습니다.

런타임에 동적 오브젝트가 이동하면, Unity는 오브젝트 주변의 프로브 값을 **보간(Interpolation)**하여 현재 위치의 조명을 근사합니다. 오브젝트가 어느 프로브들 사이에 있는지에 따라 각 프로브의 영향이 섞이고, 그 결과로 해당 위치에서 사용할 SH 계수가 만들어집니다.

이렇게 구한 SH 계수는 오브젝트의 렌더링에 사용됩니다. 셰이더는 이 값을 이용해 표면 법선 방향에 맞는 주변 조명을 계산하고, 동적 오브젝트의 밝기와 색을 주변 환경에 맞춥니다.

예를 들어 캐릭터가 밝은 복도에서 어두운 그늘로 이동하면, 밝은 쪽 프로브의 영향은 줄고 어두운 쪽 프로브의 영향은 커집니다. 그 결과 캐릭터의 표면 밝기와 색도 위치에 따라 부드럽게 바뀌며, 라이트맵 대상이 아닌 동적 오브젝트도 베이크된 환경 조명과 자연스럽게 어울릴 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Light Probe 보간 — 캐릭터 이동에 따른 조명 전환</text>

  <!-- 공간 배경 -->
  <rect x="20" y="44" width="560" height="246" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- 영역 라벨 -->
  <text x="160" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">밝은 복도</text>
  <text x="440" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.45">어두운 그늘</text>

  <!-- 영역 구분선 (점선) -->
  <line x1="300" y1="78" x2="300" y2="278" stroke="currentColor" stroke-width="1" stroke-dasharray="3 4" opacity="0.3"/>

  <!-- ── 4개 Light Probe ── -->
  <!-- P1 (좌상, 밝음) -->
  <circle cx="120" cy="110" r="16" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="115" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">P1</text>

  <!-- P2 (좌하, 밝음) -->
  <circle cx="120" cy="240" r="16" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="245" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">P2</text>

  <!-- P3 (우상, 어둠) -->
  <circle cx="480" cy="110" r="16" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="480" y="115" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">P3</text>

  <!-- P4 (우하, 어둠) -->
  <circle cx="480" cy="240" r="16" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="480" y="245" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">P4</text>

  <!-- ── 가중치 선: 위치 A → P1·P2 (가까움, 굵음) ── -->
  <line x1="180" y1="160" x2="132" y2="122" stroke="currentColor" stroke-width="2.2" opacity="0.75"/>
  <text x="146" y="142" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.8">w↑</text>
  <line x1="180" y1="190" x2="132" y2="228" stroke="currentColor" stroke-width="2.2" opacity="0.75"/>
  <text x="146" y="218" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.8">w↑</text>

  <!-- ── 가중치 선: 위치 B → P3·P4 (가까움, 굵음) ── -->
  <line x1="420" y1="160" x2="468" y2="122" stroke="currentColor" stroke-width="2.2" opacity="0.75"/>
  <text x="442" y="142" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.8">w↑</text>
  <line x1="420" y1="190" x2="468" y2="228" stroke="currentColor" stroke-width="2.2" opacity="0.75"/>
  <text x="442" y="218" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.8">w↑</text>

  <!-- ── 캐릭터 위치 A (밝음) ── -->
  <rect x="170" y="155" width="60" height="40" rx="5" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">위치 A</text>

  <!-- ── 캐릭터 위치 B (어둠) ── -->
  <rect x="370" y="155" width="60" height="40" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">위치 B</text>

  <!-- ── 이동 화살표 ── -->
  <line x1="240" y1="175" x2="356" y2="175" stroke="currentColor" stroke-width="1.8" stroke-dasharray="6 4" opacity="0.65"/>
  <polygon points="364,175 354,170 354,180" fill="currentColor" opacity="0.65"/>
  <text x="298" y="167" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">캐릭터 이동</text>

  <!-- ── 하단 주석 ── -->
  <text x="300" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">가까운 프로브일수록 캐릭터 조명에 더 큰 영향(w↑)을 미칩니다</text>
  <text x="300" y="334" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">위치 A는 밝은 P1·P2에, 위치 B는 어두운 P3·P4에 가깝게 보간됩니다</text>
</svg>
</div>

<br>

### 구면 조화 함수(Spherical Harmonics)

구면 조화 함수(Spherical Harmonics, SH)는 방향에 따라 달라지는 값을 적은 수의 계수로 근사하는 방법입니다. Light Probe에서는 한 지점으로 들어오는 빛의 방향별 밝기와 색을 이 계수들로 표현합니다.

직관적으로는 사방에서 들어오는 조명을 몇 개의 숫자로 요약하는 방식에 가깝습니다. Unity의 Light Probe는 보통 L2(2차) SH를 사용하며, 이 경우 빨강, 초록, 파랑 각 색상 채널의 조명 분포를 9개의 계수로 나누어 표현합니다. 이 정도의 정보만으로도 환경광이나 간접광처럼 부드럽게 변하는 조명은 비교적 자연스럽게 표현할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">구면 조화의 저장 효율</text>

  <!-- ── 좌측: 큐브맵 ── -->
  <rect x="20" y="44" width="285" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="162" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">큐브맵</text>

  <!-- 6면 나란히 (2행 3열) -->
  <rect x="45"  y="82" width="70" height="60" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="80"  y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 1</text>
  <text x="80"  y="128" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">8×8</text>

  <rect x="127" y="82" width="70" height="60" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="162" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 2</text>
  <text x="162" y="128" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">8×8</text>

  <rect x="209" y="82" width="70" height="60" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="244" y="112" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 3</text>
  <text x="244" y="128" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">8×8</text>

  <rect x="45"  y="150" width="70" height="60" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="80"  y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 4</text>
  <text x="80"  y="196" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">8×8</text>

  <rect x="127" y="150" width="70" height="60" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="162" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 5</text>
  <text x="162" y="196" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">8×8</text>

  <rect x="209" y="150" width="70" height="60" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="244" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">면 6</text>
  <text x="244" y="196" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">8×8</text>

  <!-- 수치 -->
  <text x="162" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">6면 × 64 텍셀 = 384 값</text>
  <text x="162" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">저해상도(8×8) 기준</text>

  <!-- ── 우측: SH L2 ── -->
  <rect x="315" y="44" width="285" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="457" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SH L2 (9 계수)</text>

  <!-- 9 계수 박스 (3×3 배치) -->
  <rect x="370" y="84"  width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="387" y="106" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₀</text>
  <rect x="410" y="84"  width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="427" y="106" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₁</text>
  <rect x="450" y="84"  width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="467" y="106" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₂</text>

  <rect x="370" y="124" width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="387" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₃</text>
  <rect x="410" y="124" width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="427" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₄</text>
  <rect x="450" y="124" width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="467" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₅</text>

  <rect x="370" y="164" width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="387" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₆</text>
  <rect x="410" y="164" width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="427" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₇</text>
  <rect x="450" y="164" width="34" height="34" rx="3" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="467" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">c₈</text>

  <!-- RGB 채널 주석 -->
  <rect x="500" y="84" width="80" height="114" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="540" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">× 3 채널</text>
  <text x="540" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(RGB)</text>
  <text x="540" y="156" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">각 계수를</text>
  <text x="540" y="170" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">R, G, B</text>
  <text x="540" y="184" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">각각 저장</text>

  <!-- 수치 -->
  <text x="457" y="222" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">9 계수 × 3 채널(RGB) = 27 float</text>
  <text x="457" y="252" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">27 × 4바이트 = 108 바이트</text>

  <!-- ── 중앙 비교 막대 그래프 ── -->
  <text x="310" y="302" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">값 개수 비교</text>

  <!-- 큐브맵 막대 (384) -->
  <text x="60"  y="332" font-family="sans-serif" font-size="10" fill="currentColor">큐브맵</text>
  <rect x="110" y="320" width="440" height="16" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text x="560" y="332" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">384</text>

  <!-- SH L2 막대 (27, 비율로 약 31px) -->
  <text x="60"  y="364" font-family="sans-serif" font-size="10" fill="currentColor">SH L2</text>
  <rect x="110" y="352" width="31"  height="16" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="364" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">27</text>

  <!-- 비율 라벨 -->
  <text x="310" y="390" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">384 값 ↔ 27 float · 약 14배 차이</text>

  <!-- 하단 주석 -->
  <text x="310" y="412" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">SH L2는 저주파(부드러운) 조명을 잘 근사, 날카로운 하이라이트는 표현 불가</text>
</svg>
</div>

<br>

SH 계수는 데이터 크기가 작기 때문에 여러 프로브 값을 섞어 쓰기 쉽습니다. 런타임에는 오브젝트 주변 프로브의 SH 계수를 보간해 현재 위치의 조명 값을 만들고, 셰이더는 표면 법선 방향에 맞는 조명 값을 계산합니다. 이 과정은 여러 실시간 라이트를 직접 계산하는 것보다 비용이 낮습니다.

### Light Probe의 비용과 한계

Light Probe의 런타임 비용은 비교적 낮습니다. 런타임에는 주변 프로브의 SH 계수를 보간하고, 셰이더에서 표면 법선 방향의 조명 값을 계산하면 됩니다. 여러 실시간 라이트를 오브젝트마다 직접 계산하는 것보다 훨씬 가벼운 방식입니다.

대신 표현할 수 있는 조명에는 한계가 있습니다. SH L2는 부드럽게 변하는 저주파 조명 성분을 근사하는 데 적합하지만, 날카로운 그림자 경계나 좁은 스포트라이트처럼 변화가 급격한 조명은 정확히 표현하기 어렵습니다.

따라서 Light Probe는 부드러운 환경광(Ambient)과 간접광을 동적 오브젝트에 전달하는 역할에 적합합니다. 정밀한 직접광, 선명한 그림자, 강한 하이라이트가 필요하다면 실시간 라이트나 실시간 그림자로 보완해야 합니다.

프로브 배치 밀도도 결과 품질에 큰 영향을 줍니다. 밝은 복도에서 어두운 방으로 넘어가는 지점처럼 조명이 급격히 변하는 구간에는 프로브를 촘촘하게 배치해야 보간 결과가 자연스럽습니다. 반대로 조명 변화가 적은 넓은 공간에서는 프로브 간격을 넓혀도 큰 문제가 없습니다.

---

## Reflection Probe

Light Probe가 주변 조명의 밝기와 색을 동적 오브젝트에 전달한다면, Reflection Probe는 주변 환경이 표면에 비치는 반사 정보를 제공합니다. 금속, 유리, 물처럼 반사가 중요한 재질은 단순한 조명 밝기만으로는 충분하지 않으므로, 별도로 주변 환경을 캡처해 반사에 사용합니다.

### 환경 반사의 표현

금속, 유리, 물처럼 반사가 강한 재질은 표면에 주변 장면이 비쳐야 자연스럽게 보입니다. 하지만 반사되는 장면은 표면의 위치와 방향에 따라 달라지므로, 이를 매번 정확히 계산하려면 반사가 필요한 지점에서 주변 환경을 다시 렌더링해야 합니다. 이 작업을 실시간으로 반복하면 비용이 매우 커집니다.

Reflection Probe는 이 비용을 줄이기 위해, 특정 위치에서 주변 환경을 **큐브맵(Cubemap)**으로 캡처해 저장합니다. 큐브맵은 그 위치를 기준으로 위, 아래, 좌, 우, 앞, 뒤 여섯 방향의 장면을 담은 텍스처입니다.

런타임에는 반사가 필요한 표면에서 반사 방향을 계산하고, 해당 위치에 영향을 주는 Reflection Probe의 큐브맵을 그 방향으로 샘플링합니다. 즉, 주변 장면을 매번 다시 렌더링하는 대신, 캡처해 둔 환경 텍스처를 조회해 반사 색상을 얻는 방식입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 385" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Reflection Probe의 동작</text>

  <!-- Capture section background -->
  <rect x="20" y="40" width="480" height="215" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- Capture section label -->
  <text x="40" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">캡처 단계</text>
  <text x="40" y="80" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프로브 위치에서 6방향의 주변 환경을 큐브맵 텍스처에 저장</text>

  <!-- Cubemap cross unfolding -->
  <!-- Top face (위) -->
  <rect x="210" y="95" width="60" height="50" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="124" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">위</text>

  <!-- Left face (좌) -->
  <rect x="140" y="145" width="70" height="50" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="175" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">좌</text>

  <!-- Front face (앞) -->
  <rect x="210" y="145" width="60" height="50" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">앞</text>

  <!-- Right face (우) -->
  <rect x="270" y="145" width="70" height="50" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="305" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">우</text>

  <!-- Back face (뒤) -->
  <rect x="340" y="145" width="70" height="50" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="375" y="174" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">뒤</text>

  <!-- Bottom face (아래) -->
  <rect x="210" y="195" width="60" height="50" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="224" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">아래</text>

  <!-- Cubemap annotation -->
  <text x="430" y="174" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">큐브맵의 6면</text>
  <line x1="411" y1="170" x2="413" y2="170" stroke="currentColor" stroke-width="1" opacity="0.5"/>

  <!-- Runtime section background -->
  <rect x="20" y="275" width="480" height="95" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- Runtime section label -->
  <text x="40" y="297" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">런타임</text>

  <!-- Flow: 반사 벡터 계산 → 큐브맵 샘플링 → 반사 색상 -->
  <!-- Box 1 -->
  <rect x="45" y="310" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="330" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">반사 벡터 계산</text>

  <!-- Arrow 1 -->
  <line x1="165" y1="326" x2="200" y2="326" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,322 210,326 200,330" fill="currentColor"/>

  <!-- Box 2 -->
  <rect x="210" y="310" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="330" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">큐브맵 샘플링</text>

  <!-- Arrow 2 -->
  <line x1="330" y1="326" x2="365" y2="326" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="365,322 375,326 365,330" fill="currentColor"/>

  <!-- Box 3 -->
  <rect x="375" y="310" width="110" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="330" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">반사 색상</text>

  <!-- Cost note -->
  <text x="260" y="362" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">베이크 큐브맵 사용 시 비용: 큐브맵 샘플링 위주</text>
</svg>
</div>

<br>

### 베이크 vs 실시간

Reflection Probe는 큐브맵을 언제 생성하고 갱신하느냐에 따라 비용과 표현 가능 범위가 달라집니다.

**베이크 모드**에서는 에디터에서 큐브맵을 생성해 저장합니다. 런타임에는 이미 만들어진 큐브맵을 샘플링하기만 하므로 비용이 낮습니다. 대신 반사에 비치는 장면은 캡처 시점의 모습으로 고정되며, 런타임에 오브젝트가 이동하거나 조명이 바뀌어도 자동으로 반영되지 않습니다.

**실시간 모드**에서는 런타임에 프로브 위치에서 주변 장면을 다시 렌더링해 큐브맵을 갱신합니다. 큐브맵은 여섯 면으로 이루어진 텍스처이므로, 새 큐브맵을 만들려면 위, 아래, 좌, 우, 앞, 뒤 방향의 장면을 각각 렌더링해야 합니다.

실시간 모드는 환경 변화가 반사에도 반영된다는 장점이 있지만, 큐브맵을 갱신할 때마다 메인 카메라 렌더링과 별도로 추가 렌더링이 발생합니다. 만약 프로브 하나를 매 프레임 갱신한다면, 매 프레임 여섯 방향의 렌더링이 추가됩니다. 프로브 수가 많거나 큐브맵 해상도가 높을수록 부담은 더 커집니다.

따라서 성능 예산이 제한된 프로젝트에서는 Reflection Probe를 기본적으로 베이크 모드로 두는 편이 안정적입니다. 동적으로 변하는 반사가 꼭 필요하다면 매 프레임 갱신을 기본값으로 두기보다, 갱신 주기를 길게 잡거나 특정 상황에서만 갱신하는 식으로 범위를 제한하는 편이 좋습니다. 큐브맵 해상도를 낮추는 것도 비용을 줄이는 방법입니다.

---

## Mixed 라이팅

앞에서 살펴본 베이크 라이팅, Light Probe, Reflection Probe는 런타임 비용을 줄이는 데 효과적이지만, 모든 조명 문제를 해결하지는 못합니다.
정적 환경의 조명은 미리 계산해 비용을 줄이더라도, 캐릭터나 움직이는 오브젝트에는 런타임에 반응하는 조명과 그림자가 필요합니다. 이처럼 베이크 결과와 실시간 조명을 함께 사용하는 방식이 **Mixed 라이팅**입니다.

### 베이크와 실시간의 결합

라이팅 모드를 비교하면 Mixed 라이팅의 위치가 더 분명해집니다.

<br>

**라이팅 모드 비교**

| 모드 | 정적 오브젝트 | 동적 오브젝트 |
|------|---------------|---------------|
| Realtime | 실시간 조명 계산 | 실시간 조명 계산 |
| Baked | 라이트맵 사용 | Light Probe 등으로 간접 조명 보완 |
| Mixed | 라이트맵 또는 Shadowmask 사용 | 실시간 조명과 그림자 사용 |

<br>

Mixed 모드의 핵심은 하나의 라이트가 정적 오브젝트와 동적 오브젝트에 서로 다른 방식으로 적용된다는 점입니다.
정적 오브젝트에는 베이크된 조명과 그림자 정보를 사용하고, 동적 오브젝트에는 런타임에 계산되는 조명과 그림자를 적용합니다. 특히 그림자는 어떤 정보를 라이트맵이나 Shadowmask에 저장하느냐에 따라 비용과 품질이 크게 달라집니다.

### Mixed 라이팅의 그림자 모드

Mixed 라이팅의 그림자 모드는 어떤 그림자를 베이크해 둘지, 어떤 그림자를 런타임에 계산할지 정하는 설정입니다. Unity에서는 이 선택을 **Baked Indirect**, **Shadowmask**, **Subtractive** 세 방식으로 나눕니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Title -->
  <text x="290" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Mixed 라이팅의 그림자 모드</text>

  <!-- Cost spectrum label -->
  <text x="530" y="52" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">런타임 비용</text>

  <!-- === (1) Baked Indirect === -->
  <rect x="20" y="46" width="460" height="108" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="36" y="70" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) Baked Indirect</text>
  <text x="36" y="90" font-family="sans-serif" font-size="11" fill="currentColor">간접광만 베이크, 직접광과 그림자는 모두 실시간</text>
  <text x="36" y="108" font-family="sans-serif" font-size="11" fill="currentColor">정적 오브젝트도 실시간 그림자를 받음</text>
  <text x="36" y="140" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 직접광 변화 대응, Shadow Map 비용 큼</text>

  <!-- Cost indicator: HIGH -->
  <rect x="496" y="46" width="68" height="108" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.5"/>
  <text x="530" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">높음</text>
  <text x="530" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">▲▲▲</text>

  <!-- Arrow between 1 and 2 -->
  <line x1="250" y1="154" x2="250" y2="170" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="245,168 250,178 255,168" fill="currentColor"/>

  <!-- === (2) Shadowmask === -->
  <rect x="20" y="180" width="460" height="118" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="36" y="204" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) Shadowmask</text>
  <text x="36" y="224" font-family="sans-serif" font-size="11" fill="currentColor">간접광 + 정적 오브젝트의 그림자를 베이크</text>
  <text x="36" y="242" font-family="sans-serif" font-size="11" fill="currentColor">정적 오브젝트: 베이크 그림자 (Shadowmask 텍스처)</text>
  <text x="36" y="260" font-family="sans-serif" font-size="11" fill="currentColor">동적 오브젝트: 실시간 그림자 + Probe 가림 정보</text>
  <text x="36" y="284" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 정적 그림자 정보를 저장해 Shadow Map 비용 완화</text>

  <!-- Cost indicator: MEDIUM -->
  <rect x="496" y="180" width="68" height="118" rx="5" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="530" y="234" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">중간</text>
  <text x="530" y="250" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">▲▲</text>

  <!-- Arrow between 2 and 3 -->
  <line x1="250" y1="298" x2="250" y2="314" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="245,312 250,322 255,312" fill="currentColor"/>

  <!-- === (3) Subtractive === -->
  <rect x="20" y="324" width="460" height="88" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="36" y="348" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) Subtractive</text>
  <text x="36" y="368" font-family="sans-serif" font-size="11" fill="currentColor">정적 오브젝트의 직접광, 간접광, 그림자를 베이크</text>
  <text x="36" y="386" font-family="sans-serif" font-size="11" fill="currentColor">동적 오브젝트: 메인 Directional Light 그림자만 제한적 실시간</text>
  <text x="36" y="404" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 가장 낮은 비용, 가장 제한적인 품질</text>

  <!-- Cost indicator: LOW -->
  <rect x="496" y="324" width="68" height="88" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="530" y="364" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">낮음</text>
  <text x="530" y="380" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">▲</text>
</svg>
</div>

<br>

**Baked Indirect**는 간접광(GI)만 라이트맵과 Light Probe에 저장합니다. 라이트에서 표면으로 바로 도달하는 직접광은 런타임에 계산되고, 그림자도 실시간 Shadow Map으로 처리됩니다. 그래서 조명의 직접적인 밝기 변화는 반영하기 쉽지만, 정적 오브젝트의 그림자까지 매 프레임 다시 계산해야 하므로 그림자 비용이 큽니다. 그림자 예산이 부족한 환경에서는 Shadow Distance나 그림자를 생성하는 오브젝트 수를 제한해야 합니다.

**Shadowmask**는 Mixed 라이트가 정적 표면에서 얼마나 가려지는지를 미리 저장하는 방식입니다. 직접광 자체는 Baked Indirect처럼 런타임에 계산하지만, 정적 벽이나 기둥이 바닥에 만드는 그림자 정보는 베이크 단계에서 Shadowmask 텍스처에 기록합니다.

런타임에는 바닥 픽셀이 Shadowmask를 읽어 "이 라이트가 여기서는 얼마나 가려지는지"를 확인합니다. 예를 들어 벽 뒤쪽 바닥은 라이트가 적게 도달하는 값으로 저장되어 있으므로 더 어둡게 계산됩니다. 정적 오브젝트의 그림자 판정이 텍스처 조회로 대체되기 때문에, 해당 그림자를 위해 Shadow Map을 매 프레임 다시 렌더링하는 비용을 줄일 수 있습니다.

움직이는 캐릭터는 위치가 계속 바뀌므로 Shadowmask 텍스처에 고정해 둘 수 없습니다. 캐릭터가 바닥에 드리우는 그림자는 실시간 Shadow Map으로 처리하고, 캐릭터가 정적 그림자 영역 안에 들어갔을 때의 조명 변화는 주변 Light Probe에 저장된 가림 정보를 이용해 보완합니다.

따라서 Shadowmask는 실시간 그림자 렌더링 비용을 줄이는 대신, Shadowmask 텍스처와 Light Probe의 가림 정보를 추가로 저장해야 합니다. 그만큼 메모리 사용량은 Baked Indirect보다 늘어날 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <text x="320" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Shadowmask의 동작 구조</text>

  <!-- Bake section -->
  <rect x="20" y="42" width="600" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="38" y="64" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">베이크 단계</text>

  <rect x="45" y="82" width="150" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">라이트맵</text>
  <text x="120" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">정적 표면의</text>
  <text x="120" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">간접광 저장</text>

  <rect x="245" y="82" width="150" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Shadowmask</text>
  <text x="320" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">정적 표면에서</text>
  <text x="320" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">라이트가 가려지는 정도</text>

  <rect x="445" y="82" width="150" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="520" y="106" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Light Probe</text>
  <text x="520" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">동적 오브젝트용</text>
  <text x="520" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">가림 정보 저장</text>

  <text x="320" y="166" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">직접광은 베이크하지 않고 런타임에 계산</text>

  <!-- Runtime section -->
  <rect x="20" y="220" width="600" height="168" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="38" y="242" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">런타임</text>

  <rect x="45" y="266" width="130" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="295" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정적 표면</text>

  <line x1="175" y1="290" x2="210" y2="290" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="210,286 218,290 210,294" fill="currentColor"/>

  <rect x="220" y="258" width="190" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="315" y="282" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">직접광 계산</text>
  <text x="315" y="298" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">+ 라이트맵</text>
  <text x="315" y="314" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">+ Shadowmask</text>

  <rect x="45" y="332" width="130" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="361" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">동적 오브젝트</text>

  <line x1="175" y1="356" x2="210" y2="356" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="210,352 218,356 210,360" fill="currentColor"/>

  <rect x="220" y="326" width="190" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="315" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">직접광 계산</text>
  <text x="315" y="366" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">+ Light Probe 가림</text>
  <text x="315" y="382" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">정적 그림자 영향 보완</text>

  <rect x="455" y="292" width="130" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="520" y="316" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">동적 그림자</text>
  <text x="520" y="334" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">움직이는 오브젝트는</text>
  <text x="520" y="348" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">Shadow Map으로 처리</text>

  <!-- Bake to runtime arrows -->
  <line x1="120" y1="146" x2="120" y2="205" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <line x1="120" y1="205" x2="270" y2="205" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <line x1="270" y1="205" x2="270" y2="254" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <polygon points="266,252 270,258 274,252" fill="currentColor" opacity="0.4"/>

  <line x1="320" y1="146" x2="320" y2="254" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <polygon points="316,252 320,258 324,252" fill="currentColor" opacity="0.4"/>

  <line x1="520" y1="146" x2="520" y2="205" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <line x1="520" y1="205" x2="360" y2="205" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <line x1="360" y1="205" x2="360" y2="322" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3" opacity="0.4"/>
  <polygon points="356,320 360,326 364,320" fill="currentColor" opacity="0.4"/>
</svg>
</div>

<br>

Shadowmask에는 Distance Shadowmask라는 거리 기반 설정도 있습니다. 이 설정은 카메라와 가까운 영역의 그림자는 Shadow Map으로 계산하고, Shadow Distance를 넘는 먼 영역은 Shadowmask에 저장된 베이크 그림자로 처리합니다. 가까운 그림자의 선명도는 높일 수 있지만 그만큼 Shadow Map 렌더링 비용이 다시 늘어나므로, 성능 예산이 작다면 일반 Shadowmask 설정을 우선 검토하는 편이 적절합니다.

**Subtractive**는 정적 환경의 조명을 최대한 라이트맵에 베이크해 두는 저비용 모드입니다. 이 모드에서는 벽, 바닥, 지형처럼 움직이지 않는 표면에 Mixed 라이트의 직접광, 간접광, 정적 그림자가 모두 라이트맵으로 기록됩니다. 캐릭터처럼 움직이는 오브젝트에는 직접광만 런타임에 계산하고, 주변의 간접광과 정적 그림자 영향은 Light Probe 값을 이용해 맞춥니다.
동적 오브젝트가 만드는 실시간 그림자는 메인 Directional Light 하나에 대해서만 제한적으로 처리됩니다. 예를 들어 캐릭터가 베이크된 바닥 위에 그림자를 드리우면, Unity는 해당 바닥 픽셀의 라이트맵 색을 더 어둡게 만들어 그림자가 생긴 것처럼 보이게 합니다. 이미 계산된 밝기에서 일부를 빼는 방식으로 그림자를 근사하기 때문에 이 모드를 Subtractive라고 부릅니다.

이 방식은 런타임 비용이 낮은 대신 표현 범위가 좁습니다. 런타임에 라이트가 켜지거나 꺼지는 변화, 여러 실시간 라이트의 그림자, 복잡한 그림자 합성에는 적합하지 않습니다. 따라서 사실적인 조명보다 저사양 환경이나 스타일화된 화면에 더 어울립니다.

<br>

### 성능 예산이 제한된 프로젝트의 Mixed 구성

성능 여유가 크지 않은 프로젝트에서는 모든 조명을 실시간으로 계산하기 어렵습니다. 이럴 때는 태양처럼 장면 전체에 영향을 주는 주요 Directional Light만 Mixed로 사용하고, 실내 조명이나 가로등 같은 보조 조명은 베이크하는 구성이 현실적입니다. 동적 오브젝트의 간접광은 Light Probe로, 금속이나 유리 표면의 환경 반사는 Reflection Probe로 보완합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">

  <!-- Title -->
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">저비용 라이팅 구성</text>

  <!-- Row 1: Directional Light -->
  <rect x="16" y="44" width="170" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="72" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Directional Light</text>
  <text x="101" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(태양)</text>

  <!-- Arrow 1 -->
  <line x1="186" y1="82" x2="218" y2="82" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="218,78 226,82 218,86" fill="currentColor"/>

  <!-- Mode badge 1 -->
  <rect x="230" y="56" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="75" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Mixed 모드</text>

  <!-- Arrow 1b -->
  <line x1="320" y1="70" x2="352" y2="70" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="352,66 360,70 352,74" fill="currentColor"/>

  <!-- Detail box 1 -->
  <rect x="364" y="44" width="240" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="484" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정적 표면: 라이트맵 + Shadowmask</text>
  <text x="484" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">동적 대상: 제한적 실시간 조명/그림자</text>

  <!-- Row 2: 실내 조명, 가로등 등 -->
  <rect x="16" y="138" width="170" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="170" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">실내 조명, 가로등 등</text>

  <!-- Arrow 2 -->
  <line x1="186" y1="176" x2="218" y2="176" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="218,172 226,176 218,180" fill="currentColor"/>

  <!-- Mode badge 2 -->
  <rect x="230" y="150" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="169" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Baked 모드</text>

  <!-- Arrow 2b -->
  <line x1="320" y1="164" x2="352" y2="164" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="352,160 360,164 352,168" fill="currentColor"/>

  <!-- Detail box 2 -->
  <rect x="364" y="138" width="240" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="484" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">라이트맵에 결과 포함, 실시간 조명 계산 없음</text>
  <text x="484" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">동적 오브젝트에는 Light Probe로</text>
  <text x="484" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">간접광 전달</text>

  <!-- Row 3: Light Probe -->
  <rect x="16" y="232" width="170" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="264" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Light Probe</text>

  <!-- Arrow 3 -->
  <line x1="186" y1="270" x2="218" y2="270" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="218,266 226,270 218,274" fill="currentColor"/>

  <!-- Mode badge 3 -->
  <rect x="230" y="244" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="262" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Baked</text>

  <!-- Arrow 3b -->
  <line x1="320" y1="258" x2="352" y2="258" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="352,254 360,258 352,262" fill="currentColor"/>

  <!-- Detail box 3 -->
  <rect x="364" y="232" width="240" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="484" y="258" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">동적 오브젝트에 간접광 전달</text>
  <text x="484" y="276" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정적 그림자 영향 보완</text>

  <!-- Row 4: Reflection Probe -->
  <rect x="16" y="326" width="170" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="358" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Reflection Probe</text>

  <!-- Arrow 4 -->
  <line x1="186" y1="364" x2="218" y2="364" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="218,360 226,364 218,368" fill="currentColor"/>

  <!-- Mode badge 4 -->
  <rect x="230" y="338" width="90" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="275" y="357" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Baked 모드</text>

  <!-- Arrow 4b -->
  <line x1="320" y1="352" x2="352" y2="352" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="352,348 360,352 352,356" fill="currentColor"/>

  <!-- Detail box 4 -->
  <rect x="364" y="326" width="240" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="484" y="362" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">금속/유리 표면의 환경 반사 표현</text>

  <!-- Note -->
  <text x="310" y="430" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">실시간 라이트는 꼭 필요한 연출에만 제한적으로 추가</text>

</svg>
</div>

이 구성의 목적은 매 프레임 다시 계산해야 하는 조명을 최소화하는 것입니다. 주요 Directional Light와 꼭 필요한 동적 그림자만 실시간으로 남기고, 정적 조명과 정적 그림자, 간접광, 환경 반사는 베이크 데이터에서 읽습니다. 그 결과 여러 실시간 라이트를 반복 계산하는 부담을 줄이고, 비교적 가벼운 텍스처 샘플링과 Light Probe 평가로 대부분의 조명 결과를 얻을 수 있습니다.

---

## 실시간 라이트의 추가 고려 사항

베이크와 프로브를 사용하더라도 모든 실시간 라이트가 사라지는 것은 아닙니다. 남겨 둔 실시간 라이트는 프래그먼트 셰이더에서 계속 계산되므로, 라이트 수와 적용 범위를 함께 관리해야 합니다.

### 필레이트 제한과 프래그먼트 비용

필레이트 관점에서 보면, 실시간 라이트는 화면에 그려지는 프래그먼트마다 반복되는 조명 계산을 늘립니다. Directional Light 하나만 있으면 한 번의 조명 계산으로 끝나지만, 같은 픽셀에 Point Light나 Spot Light가 추가로 영향을 주면 그 라이트만큼 방향, 감쇠, 색상 합성이 반복됩니다. 그림자를 사용하는 라이트라면 Shadow Map 샘플링도 추가됩니다.

따라서 라이트 하나의 비용은 라이트 개수만으로 결정되지 않습니다. 해당 라이트가 화면의 얼마나 넓은 영역에 영향을 주는지, 그림자를 사용하는지, 그리고 그 영역에 오버드로우가 얼마나 있는지가 함께 비용을 만듭니다.

<br>

**실시간 라이트 비용을 키우는 조건**

| 조건 | 비용이 커지는 이유 |
|------|------------------|
| Directional Light 추가 | 화면 전체 프래그먼트에 조명 계산이 추가됨 |
| 범위가 큰 Point/Spot Light | 영향을 받는 화면 영역이 넓어짐 |
| 그림자 있는 라이트 | 조명 계산에 Shadow Map 샘플링이 추가됨 |
| 오버드로우가 많은 영역 | 같은 화면 위치에서 조명 계산이 여러 번 반복됨 |

따라서 실시간 라이트의 비용을 판단할 때는 개수뿐 아니라, 화면에서 차지하는 영향 범위와 그림자 사용 여부도 함께 고려해야 합니다.

> 필레이트 제한의 기본 개념은 [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)에서 자세히 다룹니다.
> 모바일 GPU에서 필레이트와 오버드로우가 비용으로 이어지는 구조는 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.

### Point/Spot Light의 범위 최적화

Directional Light는 방향만 가진 광원이라 씬 전체에 영향을 줍니다. 반면 **Point Light**와 **Spot Light**는 지정된 범위 안에서만 조명을 계산합니다. 범위가 커질수록 더 많은 표면과 프래그먼트가 라이트의 영향을 받으므로, 프래그먼트 셰이더에서 수행되는 조명 계산도 늘어납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Point/Spot Light의 Range와 조명 계산 대상</text>
  <text x="300" y="42" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.65">같은 씬, 같은 라이트 위치에서 Range만 다르게 설정한 결과 (위에서 본 모습)</text>

  <!-- Panel divider -->
  <line x1="300" y1="62" x2="300" y2="298" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.25"/>

  <!-- ===== LEFT PANEL: 넓은 Range ===== -->
  <text x="160" y="80" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">넓은 Range</text>

  <!-- Range circle -->
  <circle cx="160" cy="195" r="95" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.75"/>

  <!-- Renderers (in-range: filled / out-of-range: dashed) -->
  <rect x="58" y="163" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="98" y="238" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <rect x="128" y="138" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <rect x="168" y="208" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <rect x="193" y="163" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <rect x="233" y="228" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <rect x="83" y="253" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="133" y="218" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>

  <!-- Light source -->
  <g stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
    <line x1="148" y1="195" x2="153" y2="195"/>
    <line x1="167" y1="195" x2="172" y2="195"/>
    <line x1="160" y1="183" x2="160" y2="188"/>
    <line x1="160" y1="202" x2="160" y2="207"/>
    <line x1="151.5" y1="186.5" x2="155" y2="190"/>
    <line x1="168.5" y1="203.5" x2="165" y2="200"/>
    <line x1="151.5" y1="203.5" x2="155" y2="200"/>
    <line x1="168.5" y1="186.5" x2="165" y2="190"/>
  </g>
  <circle cx="160" cy="195" r="3" fill="currentColor"/>

  <!-- Range indicator -->
  <line x1="160" y1="195" x2="255" y2="195" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.55"/>
  <text x="207" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">Range</text>

  <!-- Summary -->
  <text x="160" y="285" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold" opacity="0.85">조명 계산 후보가 늘어남</text>
  <text x="160" y="301" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">더 많은 렌더러·프래그먼트에서 라이트 합성</text>

  <!-- ===== RIGHT PANEL: 좁은 Range ===== -->
  <text x="440" y="80" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">좁은 Range</text>

  <!-- Range circle -->
  <circle cx="440" cy="195" r="40" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.75"/>

  <!-- Renderers (same offsets from light center) -->
  <rect x="338" y="163" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="378" y="238" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="408" y="138" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="448" y="208" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <rect x="473" y="163" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="513" y="228" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="363" y="253" width="14" height="14" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.4"/>
  <rect x="413" y="218" width="14" height="14" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>

  <!-- Light source -->
  <g stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
    <line x1="428" y1="195" x2="433" y2="195"/>
    <line x1="447" y1="195" x2="452" y2="195"/>
    <line x1="440" y1="183" x2="440" y2="188"/>
    <line x1="440" y1="202" x2="440" y2="207"/>
    <line x1="431.5" y1="186.5" x2="435" y2="190"/>
    <line x1="448.5" y1="203.5" x2="445" y2="200"/>
    <line x1="431.5" y1="203.5" x2="435" y2="200"/>
    <line x1="448.5" y1="186.5" x2="445" y2="190"/>
  </g>
  <circle cx="440" cy="195" r="3" fill="currentColor"/>

  <!-- Range indicator -->
  <line x1="440" y1="195" x2="480" y2="195" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.55"/>
  <text x="460" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">Range</text>

  <!-- Summary -->
  <text x="440" y="285" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold" opacity="0.85">조명 계산 후보가 줄어듦</text>
  <text x="440" y="301" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">영향권 안의 렌더러만 라이트 합성</text>

  <!-- Legend -->
  <g transform="translate(110 326)">
    <rect x="0" y="-7" width="11" height="11" rx="1.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
    <text x="16" y="2" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">Range 안 — 조명 계산 대상 렌더러</text>
  </g>
  <g transform="translate(355 326)">
    <rect x="0" y="-7" width="11" height="11" rx="1.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.45"/>
    <text x="16" y="2" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">Range 밖 — 계산에서 제외</text>
  </g>
</svg>
</div>

Range는 단순히 라이트가 얼마나 멀리 닿는지를 정하는 값이 아니라, 조명 계산 후보가 되는 렌더러와 픽셀의 범위를 정하는 값입니다. Range를 필요 이상으로 크게 잡으면 실제로는 거의 보이지 않는 표면까지 라이트 영향권에 들어가고, 그만큼 조명 계산과 그림자 처리 후보도 늘어납니다.

따라서 Point Light와 Spot Light는 연출에 필요한 범위까지만 좁히는 편이 좋습니다. 비용을 판단할 때도 라이트 개수만 보지 말고, 각 라이트가 화면에서 얼마나 넓은 영역에 영향을 주는지 함께 확인해야 합니다.

<br>

### Per Object Light Limit 제어

Range가 라이트 하나의 영향 영역을 줄이는 설정이라면, **Per Object Light Limit**은 오브젝트 하나가 받을 수 있는 추가 라이트 수를 제한하는 설정입니다. URP Forward 렌더링에서는 메인 Directional Light가 별도로 처리되고, Point Light와 Spot Light 같은 **Additional Lights**가 이 제한의 대상이 됩니다.

오브젝트 주변의 추가 라이트가 한도를 넘으면, URP는 거리와 밝기 등을 기준으로 영향이 큰 라이트를 우선 선택합니다. 예를 들어 Limit이 2이고 주변에 Point Light 5개가 있다면, 그 오브젝트에는 영향이 큰 2개만 전달되고 나머지 3개는 해당 오브젝트의 조명 계산에서 제외됩니다.

Per Object Light Limit을 낮출수록 셰이더가 한 오브젝트에 대해 계산하는 추가 라이트 수가 줄어듭니다. 그만큼 프래그먼트당 조명 계산이 줄어 ALU 비용을 낮출 수 있지만, 선택되지 않은 라이트의 영향은 해당 오브젝트에 적용되지 않습니다. 한도를 지나치게 낮추면 오브젝트가 받던 보조 조명이나 하이라이트가 사라져, 이동 중에 밝기 변화가 부자연스럽게 보일 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Per Object Light Limit의 역할</text>

  <!-- Additional lights -->
  <text x="280" y="52" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">오브젝트 주변 Additional Lights</text>

  <circle cx="120" cy="82" r="17" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="86" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">L1</text>

  <circle cx="200" cy="82" r="17" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="86" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">L2</text>

  <circle cx="280" cy="82" r="17" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="86" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">L3</text>

  <circle cx="360" cy="82" r="17" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="86" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">L4</text>

  <circle cx="440" cy="82" r="17" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="440" y="86" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">L5</text>

  <!-- Selection stage -->
  <line x1="280" y1="104" x2="280" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="274,124 280,134 286,124" fill="currentColor"/>

  <rect x="145" y="136" width="270" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="159" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">URP가 거리와 밝기 등을 기준으로 선별</text>

  <!-- Limit rows -->
  <line x1="280" y1="174" x2="280" y2="198" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="274,194 280,204 286,194" fill="currentColor"/>

  <rect x="35" y="210" width="220" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="145" y="232" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">Limit = 4</text>
  <text x="145" y="252" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">최대 4개 라이트 전달</text>
  <text x="145" y="268" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">L1, L2, L3, L4 계산</text>

  <rect x="305" y="210" width="220" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="415" y="232" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">Limit = 2</text>
  <text x="415" y="252" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">최대 2개 라이트 전달</text>
  <text x="415" y="268" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">L1, L2 계산 · 나머지는 제외</text>

  <!-- Bottom note -->
  <rect x="55" y="298" width="450" height="38" rx="5" fill="currentColor" fill-opacity="0.11" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="314" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">Limit을 낮추면 계산할 추가 라이트 수는 줄어듭니다.</text>
  <text x="280" y="329" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">대신 선택되지 않은 라이트는 해당 오브젝트에 적용되지 않습니다.</text>
</svg>
</div>

---

## 라이팅 구성 요소 선택 기준

라이팅 구성의 핵심은 실시간으로 계산해야 하는 요소와 미리 계산해 둘 수 있는 요소를 구분하는 데 있습니다.
Realtime, Mixed, Baked는 라이트 자체의 계산 방식을 정하고, Light Probe와 Reflection Probe는 베이크된 조명 정보를 동적 오브젝트와 반사 표현에 전달하는 보조 시스템입니다.

**라이팅 구성 요소 비교**

| 구성 요소 | 주된 역할 | 런타임 비용 | 적합한 사용 |
|----------|----------|-------------|-------------|
| Realtime 라이트 | 직접광과 그림자를 런타임에 계산 | 높음 | 움직이는 라이트, 실시간 변화가 중요한 연출 |
| Mixed 라이트 | 정적 표면은 라이트맵/Shadowmask, 동적 오브젝트는 실시간 조명 사용 | 중간 | 태양처럼 장면 전체에 영향을 주는 주요 라이트 |
| Baked 라이트 | 움직이지 않는 조명 결과를 라이트맵에 저장 | 낮음 | 실내 조명, 가로등처럼 고정된 보조 조명 |
| Light Probe | 동적 오브젝트에 베이크된 주변 조명 전달 | 낮음 | 캐릭터, NPC, 움직이는 소품의 밝기 보정 |
| Reflection Probe | 큐브맵으로 주변 환경 반사 제공 | 낮음 | 금속, 유리, 물 표면의 반사 표현 |

정리하면, 런타임에 변해야 하는 직접광과 그림자만 Realtime 또는 Mixed로 남기고, 고정된 조명, 간접광, 환경 반사는 라이트맵과 프로브에서 읽도록 구성하는 것이 기본 방향입니다.

---

## 베이크 작업 흐름

Unity에서 베이크 라이팅을 설정할 때는 정적 오브젝트 지정, 라이트 모드 선택, Lighting Settings 구성, 프로브 배치, 베이크 실행 순서로 진행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 805" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- Title -->
  <text x="220" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">베이크 라이팅 설정 흐름</text>

  <!-- Step 1 -->
  <rect x="30" y="44" width="380" height="108" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="66" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) 베이크 대상 지정</text>
  <text x="220" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">정적 표면의 Contribute GI 활성화</text>
  <text x="220" y="104" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">움직이지 않는 Renderer만 라이트맵에 포함</text>
  <text x="220" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">벽, 바닥, 건물, 지형 등</text>

  <!-- Arrow 1→2 -->
  <line x1="220" y1="152" x2="220" y2="176" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,172 220,182 226,172" fill="currentColor"/>

  <!-- Step 2 -->
  <rect x="30" y="186" width="380" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="208" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) 라이트 모드 설정</text>
  <text x="220" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">라이트마다 Realtime / Mixed / Baked 선택</text>
  <text x="220" y="250" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">주요 라이트: Mixed 또는 Realtime</text>
  <text x="220" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">고정 보조 라이트: Baked 우선 검토</text>

  <!-- Arrow 2→3 -->
  <line x1="220" y1="286" x2="220" y2="310" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,306 220,316 226,306" fill="currentColor"/>

  <!-- Step 3 -->
  <rect x="30" y="320" width="380" height="118" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="342" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) Lighting Settings 구성</text>
  <text x="220" y="362" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Window → Rendering → Lighting</text>
  <text x="220" y="384" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Lightmapper 선택 (Progressive CPU/GPU)</text>
  <text x="220" y="400" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Lightmap Resolution 설정 (texels per unit)</text>
  <text x="220" y="416" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">Mixed Lighting Mode 선택 (Shadowmask 등)</text>
  <text x="220" y="432" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">라이트맵 압축과 해상도 예산 확인</text>

  <!-- Arrow 3→4 -->
  <line x1="220" y1="438" x2="220" y2="462" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,458 220,468 226,458" fill="currentColor"/>

  <!-- Step 4 -->
  <rect x="30" y="472" width="380" height="112" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="494" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(4) 프로브 배치</text>
  <text x="220" y="514" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Light Probe: 동적 오브젝트 이동 경로</text>
  <text x="220" y="532" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">조명 변화가 큰 구간은 더 촘촘하게 배치</text>
  <text x="220" y="550" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Reflection Probe: 반사가 중요한 공간에 배치</text>
  <text x="220" y="568" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">금속, 유리, 물 표면이 있는 구역</text>

  <!-- Arrow 4→5 -->
  <line x1="220" y1="584" x2="220" y2="608" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,604 220,614 226,604" fill="currentColor"/>

  <!-- Step 5 -->
  <rect x="30" y="618" width="380" height="126" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="640" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(5) 베이크 실행</text>
  <text x="220" y="662" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Generate Lighting 실행</text>
  <text x="220" y="682" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">라이트맵, Shadowmask, 프로브 데이터 생성</text>
  <text x="220" y="700" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">Lighting Data Asset에 베이크 결과 저장</text>
  <text x="220" y="724" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">베이크 시간은 씬 규모와 해상도 설정에 따라 달라짐</text>
</svg>
</div>

<br>

베이크를 실행한 뒤에는 결과를 확인하면서 라이트맵 해상도와 프로브 배치를 조정합니다.
그림자 경계가 흐릿한 표면은 라이트맵 해상도나 UV 배치를 확인하고, 동적 오브젝트의 밝기 전환이 어색한 구간은 Light Probe 밀도를 높입니다.
반대로 눈에 잘 띄지 않는 배경 오브젝트에 높은 라이트맵 해상도를 쓰고 있다면, 품질보다 메모리 비용만 늘어날 수 있습니다.

---

## 마무리

- 실시간 라이트는 파이프라인 구조에 따라 드로우콜 증가나 프래그먼트 셰이더 복잡도 증가로 비용을 만듭니다.
- 베이크 라이팅은 정적 표면의 조명 결과를 라이트맵에 저장해, 런타임 조명 계산을 텍스처 샘플링으로 대체합니다.
- Light Probe는 동적 오브젝트에 베이크된 주변 조명을 전달하고, Reflection Probe는 큐브맵으로 환경 반사를 제공합니다.
- Mixed 라이팅은 정적 표면에는 베이크 결과를 사용하고, 동적 오브젝트에는 필요한 실시간 조명을 남기는 절충안입니다. Shadowmask를 사용하면 정적 그림자의 실시간 비용을 더 줄일 수 있습니다.

이제 남는 큰 비용은 **그림자**입니다. 실시간 그림자는 Shadow Map을 만들기 위해 광원 시점의 렌더링 패스를 추가로 실행하므로, 조명 계산 자체보다 더 큰 부담이 될 수 있습니다.

[Part 2](/dev/unity/LightingAndShadows-2/)에서는 그림자의 동작 원리와 비용, 그리고 후처리(Post-Processing)의 비용 구조를 다룹니다.

<br>

---

**관련 글**
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- **조명과 그림자 (1) - 실시간 조명과 베이크** (현재 글)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)

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
- **조명과 그림자 (1) - 실시간 조명과 베이크** (현재 글)
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
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
