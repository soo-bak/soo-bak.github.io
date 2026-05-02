---
layout: single
title: "셰이더 최적화 (1) - 셰이더 성능의 원리 - soo:bak"
date: "2026-02-19 21:33:00 +0900"
description: 셰이더 컴파일 과정, ALU/텍스처/대역폭 비용, 프래그먼트 셰이더 병목, half vs float 정밀도를 설명합니다.
tags:
  - Unity
  - 최적화
  - 셰이더
  - GPU
---

## 셰이더의 비용 구조

조명, 그림자, 후처리(Post-Processing)는 화면의 품질을 좌우하는 대표적인 렌더링 기법이며, 모두 GPU에서 실행되는 프로그램인 **셰이더(Shader)** 로 구현됩니다.

조명 모델이 복잡해지거나 후처리 패스가 많아질수록 셰이더가 처리하는 연산량이 늘어나, 그만큼 프레임 시간이 길어집니다.

[렌더링 기초 (3)](/dev/unity/RenderingFoundation-3/)에서 셰이더가 머티리얼의 동작을 정의하는 프로그램임을 살펴봤고, [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 GPU가 셰이더를 수천 개의 스레드로 병렬 실행하는 구조를 확인했습니다.

이 글에서는 셰이더 내부의 **어떤 연산이** 비용을 만드는지, 그리고 그 비용이 어떤 조건에서 병목으로 이어지는지를 다룹니다.

비용 구조를 이해하면 특정 셰이더의 병목 원인을 분리하고 최적화 방향을 잡을 수 있습니다.

---

## 셰이더 컴파일 파이프라인

Unity에서 셰이더를 만들 때는 `.shader` 파일(ShaderLab 문법) 또는 Shader Graph를 사용합니다.

이렇게 만든 셰이더는 GPU에서 곧바로 실행되지 않고, 플랫폼과 GPU에 맞는 여러 단계의 변환을 거쳐 GPU 기계어가 됩니다.

이 과정을 이해하면 같은 셰이더라도 실행 환경에 따라 성능이 달라질 수 있는 이유를 파악할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 620" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셰이더 컴파일 파이프라인</text>
  <!-- Source code group box -->
  <rect x="40" y="35" width="460" height="160" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="270" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">소스 코드 작성</text>
  <!-- ShaderLab box -->
  <rect x="80" y="70" width="150" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="155" y="88" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">ShaderLab</text>
  <text x="155" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(.shader 파일)</text>
  <!-- Shader Graph box -->
  <rect x="310" y="70" width="150" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="385" y="88" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Shader Graph</text>
  <text x="385" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(비주얼 노드)</text>
  <!-- HLSL box -->
  <rect x="195" y="145" width="150" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">HLSL 코드</text>
  <!-- Arrow: ShaderLab -> HLSL -->
  <line x1="155" y1="114" x2="155" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="155" y1="130" x2="230" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="230" y1="130" x2="230" y2="145" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="224,141 230,151 236,141" fill="currentColor"/>
  <!-- Arrow: Shader Graph -> HLSL (ShaderLab 대칭, 내부 변환 표기) -->
  <line x1="385" y1="114" x2="385" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="385" y1="130" x2="310" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <line x1="310" y1="130" x2="310" y2="145" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="304,141 310,151 316,141" fill="currentColor"/>
  <text x="395" y="124" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(내부 변환)</text>
  <!-- Arrow: HLSL -> Unity Compiler -->
  <line x1="270" y1="181" x2="270" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,206 270,216 276,206" fill="currentColor"/>
  <!-- Unity Compiler label -->
  <text x="270" y="232" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Unity 셰이더 컴파일러</text>
  <text x="270" y="247" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(에디터/빌드 시점)</text>
  <!-- Arrow: Compiler -> 3 branches -->
  <line x1="270" y1="255" x2="270" y2="275" stroke="currentColor" stroke-width="1.5"/>
  <!-- Horizontal spread line -->
  <line x1="90" y1="275" x2="450" y2="275" stroke="currentColor" stroke-width="1.5"/>
  <!-- Left branch down -->
  <line x1="90" y1="275" x2="90" y2="290" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="84,286 90,296 96,286" fill="currentColor"/>
  <!-- Center branch down -->
  <line x1="270" y1="275" x2="270" y2="290" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,286 270,296 276,286" fill="currentColor"/>
  <!-- Right branch down -->
  <line x1="450" y1="275" x2="450" y2="290" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="444,286 450,296 456,286" fill="currentColor"/>
  <!-- SPIR-V box -->
  <rect x="20" y="298" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">SPIR-V</text>
  <text x="90" y="332" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(Vulkan)</text>
  <!-- GLSL box -->
  <rect x="200" y="298" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GLSL</text>
  <text x="270" y="332" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(OpenGL ES)</text>
  <!-- Metal SL box -->
  <rect x="380" y="298" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Metal SL</text>
  <text x="450" y="332" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(iOS)</text>
  <!-- IR labels -->
  <text x="90" y="365" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">중간 표현 (IR)</text>
  <text x="270" y="365" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">중간 표현 (IR)</text>
  <text x="450" y="365" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">중간 표현 (IR)</text>
  <!-- Arrows: IR -> GPU drivers -->
  <line x1="90" y1="342" x2="90" y2="380" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="84,376 90,386 96,376" fill="currentColor"/>
  <line x1="270" y1="342" x2="270" y2="380" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,376 270,386 276,376" fill="currentColor"/>
  <line x1="450" y1="342" x2="450" y2="380" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="444,376 450,386 456,376" fill="currentColor"/>
  <!-- GPU Driver boxes -->
  <rect x="20" y="388" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="406" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 드라이버</text>
  <text x="90" y="422" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(Adreno 등)</text>
  <rect x="200" y="388" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="406" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 드라이버</text>
  <text x="270" y="422" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(Mali 등)</text>
  <rect x="380" y="388" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="406" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 드라이버</text>
  <text x="450" y="422" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(Apple GPU)</text>
  <!-- Arrows: GPU drivers -> GPU machine code -->
  <line x1="90" y1="432" x2="90" y2="470" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="84,466 90,476 96,466" fill="currentColor"/>
  <line x1="270" y1="432" x2="270" y2="470" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,466 270,476 276,466" fill="currentColor"/>
  <line x1="450" y1="432" x2="450" y2="470" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="444,466 450,476 456,466" fill="currentColor"/>
  <!-- GPU Machine code boxes -->
  <rect x="20" y="478" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="496" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 전용</text>
  <text x="90" y="512" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">기계어</text>
  <rect x="200" y="478" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="496" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 전용</text>
  <text x="270" y="512" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">기계어</text>
  <rect x="380" y="478" width="140" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="496" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 전용</text>
  <text x="450" y="512" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">기계어</text>
</svg>
</div>

<br>

### 각 단계의 역할

첫 단계의 역할은 개발자가 셰이더의 동작을 직접 정의하는 것입니다.

표준은 ShaderLab 안에 HLSL(High-Level Shading Language) 코드를 작성하는 방식이며, Shader Graph에서 노드를 연결해 시각적으로 구성할 수도 있습니다.

Shader Graph도 내부에서 HLSL 코드로 변환되며, View Generated Shader 메뉴로 그 결과를 확인할 수 있습니다.

<br>

다음 단계의 역할은 HLSL 코드를 대상 플랫폼의 그래픽스 API에 맞는 **중간 표현(Intermediate Representation, IR)**으로 변환하는 것입니다.

Unity 컴파일러가 에디터 작업이나 빌드 시점에 변환하며, Vulkan에서는 SPIR-V, OpenGL ES에서는 GLSL, Metal에서는 Metal Shading Language가 결과물입니다.

같은 HLSL 코드라도 키워드 조합에 따라 서로 다른 셰이더 배리언트(variant)가 함께 생성됩니다.

<br>

마지막 단계의 역할은 중간 표현을 특정 GPU 하드웨어의 기계어(ISA, Instruction Set Architecture)로 변환하는 것입니다.

GPU 드라이버가 앱 실행 시점(런타임)이나 설치 시점에 변환하며, 같은 중간 표현이라도 ARM Mali GPU와 Qualcomm Adreno GPU는 서로 다른 기계어를 만들어 냅니다.

드라이버마다 최적화 방식이 다르므로 최종 성능도 함께 달라질 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">같은 HLSL 코드에서 플랫폼별로 다른 최종 코드가 나오는 이유</text>
  <!-- HLSL Source box (left, vertically centered across 3 rows) -->
  <rect x="15" y="52" width="100" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="112" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">HLSL 소스</text>
  <text x="65" y="127" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(공통)</text>
  <!-- Row 1: SPIR-V → Adreno 드라이버 → Adreno 기계어 -->
  <!-- Branch arrow from HLSL to SPIR-V -->
  <line x1="115" y1="77" x2="145" y2="77" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="141,71 151,77 141,83" fill="currentColor"/>
  <!-- SPIR-V box -->
  <rect x="153" y="55" width="100" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="203" y="74" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">SPIR-V</text>
  <text x="203" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(Vulkan)</text>
  <!-- Arrow SPIR-V → Adreno 드라이버 -->
  <line x1="253" y1="77" x2="283" y2="77" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="279,71 289,77 279,83" fill="currentColor"/>
  <!-- Adreno 드라이버 box -->
  <rect x="291" y="55" width="120" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="351" y="74" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Adreno 드라이버</text>
  <text x="351" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(런타임 컴파일)</text>
  <!-- Arrow Adreno 드라이버 → Adreno 기계어 -->
  <line x1="411" y1="77" x2="441" y2="77" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="437,71 447,77 437,83" fill="currentColor"/>
  <!-- Adreno 기계어 box -->
  <rect x="449" y="55" width="150" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="524" y="74" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Adreno 기계어</text>
  <text x="524" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(GPU 전용 ISA)</text>
  <!-- Row 2: GLSL → Mali 드라이버 → Mali 기계어 -->
  <!-- Branch arrow from HLSL to GLSL -->
  <line x1="115" y1="117" x2="145" y2="117" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="141,111 151,117 141,123" fill="currentColor"/>
  <!-- GLSL box -->
  <rect x="153" y="95" width="100" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="203" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GLSL</text>
  <text x="203" y="129" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(OpenGL ES)</text>
  <!-- Arrow GLSL → Mali 드라이버 -->
  <line x1="253" y1="117" x2="283" y2="117" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="279,111 289,117 279,123" fill="currentColor"/>
  <!-- Mali 드라이버 box -->
  <rect x="291" y="95" width="120" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="351" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Mali 드라이버</text>
  <text x="351" y="129" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(런타임 컴파일)</text>
  <!-- Arrow Mali 드라이버 → Mali 기계어 -->
  <line x1="411" y1="117" x2="441" y2="117" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="437,111 447,117 437,123" fill="currentColor"/>
  <!-- Mali 기계어 box -->
  <rect x="449" y="95" width="150" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="524" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Mali 기계어</text>
  <text x="524" y="129" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(GPU 전용 ISA)</text>
  <!-- Row 3: Metal → Apple 드라이버 → Apple GPU 기계어 -->
  <!-- Branch arrow from HLSL to Metal -->
  <line x1="115" y1="157" x2="145" y2="157" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="141,151 151,157 141,163" fill="currentColor"/>
  <!-- Metal box -->
  <rect x="153" y="135" width="100" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="203" y="154" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Metal</text>
  <text x="203" y="169" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(iOS)</text>
  <!-- Arrow Metal → Apple 드라이버 -->
  <line x1="253" y1="157" x2="283" y2="157" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="279,151 289,157 279,163" fill="currentColor"/>
  <!-- Apple 드라이버 box -->
  <rect x="291" y="135" width="120" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="351" y="154" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Apple 드라이버</text>
  <text x="351" y="169" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(런타임 컴파일)</text>
  <!-- Arrow Apple 드라이버 → Apple GPU 기계어 -->
  <line x1="411" y1="157" x2="441" y2="157" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="437,151 447,157 437,163" fill="currentColor"/>
  <!-- Apple GPU 기계어 box -->
  <rect x="449" y="135" width="150" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="524" y="154" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Apple GPU 기계어</text>
  <text x="524" y="169" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(GPU 전용 ISA)</text>
  <!-- Separator line -->
  <line x1="40" y1="205" x2="580" y2="205" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Conclusion text -->
  <text x="310" y="232" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">동일한 셰이더 소스라도 최종 실행 코드는 GPU마다 다름</text>
  <text x="310" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">특정 GPU에서만 느려지는 현상이 발생할 수 있음</text>
</svg>
</div>

<br>

결국 개발자가 직접 관여할 수 있는 영역은 주로 첫 단계인 소스 코드 부분이며, 컴파일러와 GPU 드라이버는 변환을 자동으로 수행하므로 직접 제어할 수 없는 영역입니다.

따라서 셰이더 최적화는 소스 코드 수준에서 불필요한 연산을 줄여 GPU가 효율적으로 실행하기 쉬운 형태로 코드를 작성하는 것이 중요합니다.

---

## 셰이더의 세 가지 비용

셰이더가 GPU에서 실행될 때 드는 비용은 한 종류가 아닙니다. 비용은 크게 세 가지로 구분되며, 어느 쪽이 병목인지에 따라 적용해야 할 최적화의 방향이 달라집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- Title -->
  <text x="220" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셰이더 비용의 세 가지 축</text>
  <!-- Box 1: ALU -->
  <rect x="30" y="38" width="380" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="58" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1. ALU 연산</text>
  <text x="50" y="76" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU 연산 유닛에서 수행하는 수학 계산</text>
  <text x="50" y="94" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">+, -, *, /, sin, cos, dot, normalize, lerp</text>
  <!-- Box 2: Texture Sampling -->
  <rect x="30" y="114" width="380" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="134" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2. 텍스처 샘플링</text>
  <text x="50" y="152" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">텍스처 메모리에서 텍셀을 읽어오는 연산</text>
  <text x="50" y="170" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">메모리 접근이 필요하므로 ALU 연산보다 느림</text>
  <!-- Box 3: Memory Bandwidth -->
  <rect x="30" y="190" width="380" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="210" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3. 메모리 대역폭</text>
  <text x="50" y="228" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">텍스처/버퍼 데이터의 메모리 ↔ GPU 전송량</text>
  <text x="50" y="246" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">해상도와 텍스처 크기에 비례하여 증가</text>
  <!-- Conclusion -->
  <text x="220" y="288" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">세 축 중 어느 쪽이 병목인지에 따라 최적화 방향이 달라짐</text>
</svg>
</div>

<br>

### ALU 연산 (Arithmetic Logic Unit)

ALU 연산은 GPU의 연산 유닛(Arithmetic Logic Unit)에서 처리하는 수학 계산입니다.

셰이더에서 작성하는 모든 산술·벡터·행렬·비교 계산이 여기에 해당합니다.

<br>

**ALU에서 처리하는 대표적인 연산**

| 연산 분류 | 함수 |
|-----------|------|
| 기본 산술 | `+`  `-`  `*`  `/` |
| 삼각함수 | `sin()`  `cos()`  `tan()` |
| 벡터 연산 | `dot()`  `cross()`  `normalize()`  `length()` |
| 보간 | `lerp()`  `smoothstep()`  `saturate()` |
| 거듭제곱 | `pow()`  `exp()`  `log()`  `sqrt()` |
| 행렬 곱셈 | `mul(matrix, vector)` |
| 비교/분기 | `if`  `step()`  `max()`  `min()`  `clamp()` |

<br>

같은 ALU 연산이라도 종류에 따라 비용이 크게 달라집니다.

예를 들어, 덧셈과 곱셈은 GPU가 빠르게 처리하도록 설계된 기본 연산이지만, `sin()`·`cos()`·`pow()` 같은 초월함수는 내부적으로 여러 연산 단계를 거치므로 비용이 더 큽니다.

`normalize()` 역시 각 성분의 제곱 합산과 역수 제곱근 계산이 결합된 복합 연산이라, 단순한 덧셈보다 여러 배의 비용이 듭니다.

<br>

| 연산 | 상대 비용 예시 | 비고 |
|------|-------------------|------|
| add, mul | 1 | |
| mad (a*b+c) | 1 | GPU가 효율적으로 처리 |
| min, max, clamp | 1 | |
| dot (float4) | 1 | |
| lerp | 1 | |
| rsqrt | 1 ~ 2 | |
| rcp (역수) | 1 ~ 2 | |
| normalize | 2 ~ 3 | dot + rsqrt + mul |
| sin, cos | 2 ~ 4 | |
| pow | 3 ~ 5 | exp(y * log(x)) |
| log, exp | 2 ~ 3 | |

<br>

GPU가 가장 효율적으로 처리하는 형태는 `a * b + c` 같은 곱셈-덧셈 조합인 **mad(multiply-add)**입니다.

따라서 셰이더 컴파일러는 가능한 모든 계산을 mad로 모아 처리합니다. 예를 들어 조명 계산의 `dot(normal, lightDir) * intensity + ambient`도 mad 한 번으로 처리됩니다.

<br>

컴파일러가 mad로 모아 처리해도 셰이더의 ALU 연산이 누적되면 GPU 연산 유닛이 병목이 되는 상태가 **ALU-bound** 또는 **compute-bound**입니다. 특히 프래그먼트 셰이더는 화면의 모든 픽셀마다 실행되므로, 셰이더 한 줄의 비용이 픽셀 수만큼 곱해져 누적 비용이 빠르게 커집니다.

복잡한 조명 모델·다수의 광원·절차적 텍스처 생성(noise 함수 등)이 모두 픽셀당 ALU 연산 수를 늘리는 패턴으로, ALU-bound의 대표적인 원인입니다.

<br>

### 텍스처 샘플링

텍스처 샘플링은 셰이더가 텍스처에서 텍셀(색상 값)을 읽어오는 연산입니다. HLSL에서는 `tex2D()`·`SAMPLE_TEXTURE2D()` 같은 함수가 이 연산을 수행합니다.

ALU 연산은 레지스터의 값을 연산 유닛 안에서 직접 계산하지만, 텍스처 샘플링은 연산 유닛 바깥의 메모리에서 데이터를 가져와야 합니다. **메모리 접근**은 내부 계산보다 더 오래 걸리므로, 텍스처 샘플링은 셰이더 비용에서 큰 비중을 차지합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Section 1: ALU -->
  <text x="20" y="18" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">ALU 연산 — 데이터가 바로 옆에 있음</text>
  <!-- Outer box: 연산 유닛 -->
  <rect x="20" y="30" width="260" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="50" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">연산 유닛</text>
  <!-- Inner box: 레지스터 -->
  <rect x="40" y="58" width="220" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="150" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">레지스터 (데이터)</text>
  <!-- Annotation -->
  <text x="300" y="60" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← 데이터가 유닛 내부에 이미 존재</text>
  <text x="300" y="78" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">1~5 사이클 (수 나노초)</text>
  <!-- Section 2: Texture Sampling -->
  <text x="20" y="148" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">텍스처 샘플링 — 데이터를 멀리서 가져와야 함</text>
  <!-- 연산 유닛 box -->
  <rect x="20" y="162" width="140" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">연산 유닛</text>
  <!-- 텍스처 메모리 box -->
  <rect x="320" y="162" width="140" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="182" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">텍스처</text>
  <text x="390" y="200" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">메모리</text>
  <!-- Arrow: 연산 유닛 -> 텍스처 메모리 (메모리 버스) -->
  <line x1="160" y1="182" x2="310" y2="182" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="306,176 316,182 306,188" fill="currentColor"/>
  <text x="240" y="176" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">메모리 버스</text>
  <!-- Arrow: 텍스처 메모리 -> 연산 유닛 (데이터 전송) -->
  <line x1="320" y1="202" x2="170" y2="202" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="174,196 164,202 174,208" fill="currentColor"/>
  <text x="240" y="214" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">데이터 전송</text>
  <!-- Bottom labels -->
  <text x="90" y="248" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">요청 후 대기</text>
  <text x="390" y="248" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">캐시 적중: ~10 사이클</text>
  <text x="390" y="264" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">캐시 미스: 수백 사이클</text>
</svg>
</div>

<br>

GPU는 이런 비용을 줄이기 위해 **텍스처 캐시**를 사용합니다. 메모리에서 한 번 읽은 블록을 캐시에 보관해, 인접한 프래그먼트가 같은 영역을 다시 참조할 때 메모리 없이 가져옵니다.

또한 [렌더링 기초 (2)](/dev/unity/RenderingFoundation-2/)에서 다룬 밉맵도 캐시 효율을 높이는 기법입니다. 적절한 밉맵 레벨을 사용하면 텍스처의 좁은 영역만 읽으므로, 같은 캐시 블록을 자주 재사용해 적중률(hit rate)이 올라갑니다.

<br>

한편 텍스처 샘플링 비용은 여러 요인의 영향을 받습니다. 텍스처 수와 해상도, 밉맵, 필터링 모드, 압축 여부가 모두 영향을 줍니다.

<br>

| 요인 | 비용이 커지는 방향 | 비용을 줄이는 방향 |
|------|-------------------|-------------------|
| 텍스처 수 | 셰이더당 텍스처가 많을수록 샘플링 횟수 비례 증가 | 사용하지 않는 샘플 제거 |
| 텍스처 해상도 | 고해상도 → 캐시 미스 증가 | 적절한 해상도 선택 |
| 밉맵 | 미사용 시 캐시 미스 증가 | 밉맵 사용 → 캐시 적중률 향상 |
| 필터링 모드 | bilinear: 4텍셀, trilinear: 8텍셀, anisotropic: 최대 16텍셀+ | 낮은 필터링 모드 선택 |
| 텍스처 압축 | 비압축: 원본 크기 전송 | ASTC/ETC2 압축 → 대역폭 절약 |

<br>

이 중 **필터링 모드**는 한 번의 샘플링이 읽는 텍셀 수를 결정합니다. Bilinear 모드는 대상 좌표 주변 4개 텍셀을 가중 평균하고, Trilinear 모드는 인접한 두 밉맵 레벨에서 bilinear를 두 번 수행해 총 8개를 보간합니다. Anisotropic 모드는 표면이 카메라에 비스듬할 때 시야 방향을 따라 추가 샘플을 수행해 최대 16개 이상의 텍셀을 읽습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">필터링 모드별 텍셀 읽기 수</text>
  <!-- === Bilinear Section (left) === -->
  <text x="110" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Bilinear</text>
  <text x="110" y="63" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">밉맵 레벨 1개에서 4텍셀</text>
  <!-- 2x2 grid -->
  <rect x="72" y="75" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="98" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="108" y="75" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="126" y="98" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="72" y="111" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="134" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="108" y="111" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="126" y="134" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <!-- 4 texel label -->
  <text x="110" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">4텍셀</text>
  <!-- === Trilinear Section (right) === -->
  <text x="350" y="48" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Trilinear</text>
  <text x="350" y="63" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">밉맵 레벨 2개에서 각 4텍셀 = 총 8텍셀</text>
  <!-- Level N label -->
  <text x="290" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">레벨 N</text>
  <!-- Level N 2x2 grid -->
  <rect x="252" y="88" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="288" y="88" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="306" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="252" y="124" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="288" y="124" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="306" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <!-- Level N+1 label -->
  <text x="410" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">레벨 N+1</text>
  <!-- Level N+1 2x2 grid -->
  <rect x="372" y="88" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="408" y="88" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="426" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="372" y="124" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <rect x="408" y="124" width="36" height="36" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="426" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">T</text>
  <!-- Interpolation arrow -->
  <line x1="290" y1="170" x2="290" y2="185" stroke="currentColor" stroke-width="1.5"/>
  <line x1="290" y1="185" x2="350" y2="195" stroke="currentColor" stroke-width="1.5"/>
  <line x1="410" y1="170" x2="410" y2="185" stroke="currentColor" stroke-width="1.5"/>
  <line x1="410" y1="185" x2="350" y2="195" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="344,191 350,201 356,191" fill="currentColor"/>
  <text x="350" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">보간</text>
  <!-- 8 texel label -->
  <text x="350" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">8텍셀</text>
</svg>
</div>

<br>

따라서 성능 예산이 제한된 환경에서는 필터링 모드 선택과 설정도 비용에 직접 영향을 줍니다. UI 텍스처·픽셀 아트처럼 밉맵 레벨 간 전환이 크게 문제 되지 않는 텍스처는 Bilinear 모드를 선택해 한 샘플링이 읽는 텍셀 수를 4개로 제한할 수 있습니다.

한편 지형·캐릭터 모델처럼 카메라에 비스듬하게 보이는 표면 텍스처는 Anisotropic 모드를 선택해 선명도를 유지할 수 있습니다. Bilinear·Trilinear는 좁은 영역의 4~8개 텍셀만 평균하므로 표면이 비스듬할수록 흐릿해지지만, Anisotropic은 시야 방향을 따라 추가 샘플을 수행해 디테일을 살립니다. 이때 필터링 레벨은 한 샘플링이 수행할 추가 샘플의 최대 수를 결정하며, 화질이 허용하는 범위에서 최소로 낮추면 추가 샘플 수가 줄어 대역폭을 절약할 수 있습니다.

<br>

### 메모리 대역폭

메모리 대역폭은 단위 시간당 메모리와 GPU 사이에 전송할 수 있는 데이터 양, 즉 그 데이터가 이동하는 통로(메모리 버스)의 전송 용량입니다. 텍스처 샘플링은 메모리에서 데이터를 가져오는 동작이며, 대역폭은 그 동작이 사용할 수 있는 통로의 너비, 즉 한 번에 흐를 수 있는 데이터 양입니다.

이 너비는 GPU 유형에 따라 크게 달라집니다. 고성능 외장 GPU는 256~384bit 이상의 메모리 버스로 수백 GB/s 대역폭을 확보하지만, 저전력·내장 GPU는 32~128bit의 좁은 버스로 수십 GB/s 수준에 머무릅니다. 따라서 성능 등급이 낮거나 전력 예산이 작은 GPU일수록 대역폭 여유가 줄어듭니다.

한편 이 대역폭은 텍스처 샘플링뿐 아니라 프레임버퍼 읽기/쓰기·정점 데이터 읽기 등이 함께 사용하는 공유 자원입니다. 한 작업이 더 많은 데이터를 전송하면 다른 작업이 사용할 여유가 줄어듭니다.

> 모바일 GPU에서 메모리 대역폭이 특히 제한되는 구조와 TBDR 원리는 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.

따라서 텍스처 수·해상도·필터링 모드처럼 메모리 전송을 늘리는 모든 요인이 같은 대역폭 예산을 두고 경쟁합니다. 전송량이 예산을 넘어서면 GPU 연산 유닛이 데이터 도착을 기다리는 시간이 늘어나 전체 처리 속도가 떨어지는 **대역폭 바운드(bandwidth-bound)** 상태가 됩니다.

이 부담은 텍스처 압축(ASTC·ETC2)으로 직접 줄일 수 있습니다. 2048×2048 비압축 RGBA 텍스처는 16MB지만 ASTC 6×6으로 압축하면 약 1.78MB로 줄어, 같은 텍스처를 읽더라도 메모리 버스를 통과하는 데이터가 약 1/9로 감소합니다.

> 텍스처 압축 형식(ASTC·ETC2)의 원리와 메모리 절감 효과는 [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 자세히 다룹니다.

<br>

### 세 가지 비용의 관계

실제 셰이더에서 GPU는 ALU 연산·텍스처 샘플링·메모리 접근을 병렬로 처리하므로, 세 사이클 중 최댓값이 셰이더 실행 시간을 결정합니다. 따라서 셰이더가 느릴 때는 원인이 ALU 연산 과다인지·텍스처 샘플링 과다인지·대역폭 부족인지를 먼저 구분해야 적절한 최적화를 적용할 수 있습니다.

<br>

| 병목 유형 | 원인 조건 | 최적화 방향 |
|-----------|----------|-------------|
| ALU-bound (연산 병목) | pow, sin 등 고비용 연산이 많은 셰이더 | 연산 단순화, LUT 사용, half 정밀도 |
| Texture-bound (텍스처 병목) | 텍스처를 여러 장 읽거나 높은 필터링 모드 사용 | 텍스처 수 줄이기, 필터링 모드 낮추기, 밉맵 활용 |
| Bandwidth-bound (대역폭 병목) | 고해상도 비압축 텍스처로 메모리 전송량 과다 | 텍스처 압축(ASTC/ETC2), 해상도·필터링 레벨 조정 |

<br>

이때 GPU 프로파일링 도구(Qualcomm Snapdragon Profiler, ARM Mali Offline Compiler, Xcode GPU Profiler 등)를 사용하면 셰이더의 병목 유형을 확인할 수 있습니다. 예를 들어 Mali Offline Compiler는 셰이더 코드를 분석해 ALU 사이클·텍스처 사이클·로드/스토어 사이클을 각각 출력합니다.

세 사이클 중 가장 큰 값을 만든 작업이 곧 그 셰이더의 병목이므로, 위 표에서 해당 병목 유형의 최적화 방향을 골라 적용하면 가장 효과적으로 성능을 개선할 수 있습니다.

---

## 프래그먼트 셰이더가 병목이 되기 쉬운 이유

프래그먼트 셰이더는 셰이더 단계 중 병목이 되기 쉽습니다.
버텍스 셰이더는 모델의 정점마다 한 번씩, 프래그먼트 셰이더는 화면의 프래그먼트(픽셀 후보)마다 한 번씩 호출되는데, 일반적인 실시간 렌더링에서는 프래그먼트 수가 정점 수보다 많기 때문입니다. 여기에 오버드로우가 그 수를 더 늘리고 GPU의 필레이트 예산이 처리량의 상한을 정합니다.

> 셰이더 단계 구조와 정점·프래그먼트 단위 실행 모델은 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서 자세히 다룹니다.

<br>

### 정점 수 vs 프래그먼트 수

일반적인 실시간 렌더링에서 한 프레임에 처리되는 정점 수는 보통 수만에서 수십만 개 수준입니다. 반면 1920×1080 해상도에서는 화면의 픽셀 수만 계산해도 2,073,600개이며, 오버드로우 없이 모든 픽셀을 한 번씩만 그려도 약 **207만 개**의 프래그먼트가 생성됩니다. 즉, 같은 장면에서도 프래그먼트 셰이더의 실행 횟수는 버텍스 셰이더보다 훨씬 커지기 쉽습니다.

이 차이는 최적화 효과에도 그대로 이어집니다. 같은 명령어 하나를 줄이더라도, 프래그먼트 셰이더에서는 훨씬 많은 실행을 줄일 수 있습니다. 반면 버텍스 셰이더에서 줄어드는 실행 횟수는 처리한 정점 수에 그칩니다.

<br>

### 오버드로우의 영향

프래그먼트 셰이더 관점에서 오버드로우 배수는 곧 실행 횟수의 배수입니다.
1920×1080 화면에서 오버드로우가 없다면 약 207만 개의 프래그먼트를 처리하지만, 평균 오버드로우가 2x라면 처리해야 하는 프래그먼트 수는 약 414만 개로 늘어납니다.

특히 파티클, UI 오버레이, 반투명 머티리얼처럼 겹친 결과를 블렌딩해야 하는 요소는 뒤쪽 프래그먼트를 쉽게 건너뛰기 어렵습니다. 이런 요소가 화면의 넓은 영역을 덮으면, 프래그먼트 셰이더의 명령어 수가 조금만 늘어도 전체 비용이 빠르게 누적됩니다.

> 오버드로우와 Early-Z의 기본 원리는 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서 자세히 다룹니다.
> 모바일 GPU에서 오버드로우가 특히 비싼 이유는 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.
<br>

### 필레이트 예산과 프래그먼트 비용

프래그먼트 셰이더 관점에서 필레이트 예산은 GPU가 단위 시간 안에 처리할 수 있는 프래그먼트 수의 상한입니다. 프래그먼트 수가 많거나 프래그먼트당 명령어 수가 많을수록 이 예산을 더 빠르게 소모합니다.

1920×1080 화면에서 평균 오버드로우가 2x라면, 한 프레임에 처리해야 하는 프래그먼트 수는 약 414만 개입니다.

$$
1920 \times 1080 \times 2 = 4{,}147{,}200
$$

목표가 60fps이고 프래그먼트마다 30개의 명령어가 실행된다면, 초당 명령어 실행 규모는 약 75억 번입니다.

$$
4{,}147{,}200 \times 30 \times 60 \approx 7.46 \times 10^9
$$

같은 조건에서 프래그먼트당 명령어 수를 20개로 줄이면 약 50억 번으로 줄어듭니다.

$$
4{,}147{,}200 \times 20 \times 60 \approx 4.98 \times 10^9
$$

즉, 프래그먼트당 명령어를 10개 줄였을 뿐이지만, 초당 실행 규모는 약 25억 번 줄어듭니다.

$$
7.46 \times 10^9 - 4.98 \times 10^9 \approx 2.48 \times 10^9
$$

물론 실제 GPU 성능이 위 계산처럼 단순히 명령어 개수만으로 결정되지는 않습니다. 같은 명령어라도 비용이 다를 수 있고, 텍스처 샘플링을 기다리는 시간이나 메모리 대역폭 부족이 병목이 되면 ALU 명령어 수를 줄여도 기대만큼 빨라지지 않을 수 있습니다. GPU가 많은 프래그먼트를 병렬로 처리한다는 점도 실제 실행 시간을 단순 계산과 다르게 만듭니다.

다만 프래그먼트 셰이더는 화면의 많은 프래그먼트마다 반복 실행됩니다. 따라서 프래그먼트당 비용이 조금만 늘어나도 그 차이가 프래그먼트 수와 프레임 수만큼 반복되어 전체 비용으로 누적됩니다.

> 필레이트 제한의 기본 개념은 [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)에서 자세히 다룹니다.
> 모바일 GPU에서 필레이트와 오버드로우가 비용으로 이어지는 구조는 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.

<br>

---

## 정밀도: half vs float

프래그먼트 셰이더처럼 같은 연산이 많은 프래그먼트에서 반복되는 단계에서는, 변수 하나의 정밀도 선택도 성능에 영향을 줄 수 있습니다.

따라서 필요한 정확도를 유지하는 범위 안에서 **변수의 정밀도(precision)** 를 낮추는 것은 셰이더 비용을 줄이는 기본적인 최적화 방법입니다.

<br>

### float와 half의 차이

셰이더에서 주로 사용하는 부동소수점 타입은 `float`와 `half`입니다. 두 타입은 값을 표현하는 데 사용하는 비트 수가 다릅니다.

`float`는 32비트 부동소수점 타입으로 넓은 범위와 높은 정밀도를 제공합니다. 반면 `half`는 16비트 부동소수점 타입으로, 표현할 수 있는 범위와 정밀도를 줄이는 대신 더 적은 레지스터와 메모리 대역폭으로 처리될 수 있습니다.

Unity 셰이더에는 더 낮은 정밀도의 `fixed` 타입도 있습니다. 다만 셰이더 최적화에서 중요한 기준은 보통 32비트 정밀도를 유지할지, 16비트 정밀도로 낮춰도 되는지입니다. 따라서 이후 설명은 `float`와 `half`의 차이를 중심으로 진행하고, `fixed`는 표에서 참고용으로만 포함합니다.

<br>

| 타입 | 비트 수 | 표현 가능 범위 | 대략적인 정밀도 |
|------|--------|---------------|-------------------|
| float | 32비트 | ±3.4 × 10³⁸ | 약 7자리 |
| half | 16비트 | ±65,504 | 약 3자리 |
| fixed | 보통 11비트 | -2.0 ~ +2.0 | 1/256 단위 |

<br>

`half`는 사용할 수 있는 비트 수가 적기 때문에 표현 범위와 정밀도에 한계가 있습니다. 65,504를 넘는 값은 표현할 수 없고, 작은 차이도 `float`만큼 세밀하게 유지하지 못할 수 있습니다. 이런 특성 때문에 위치, 긴 거리 값, 반복 계산으로 오차가 누적되는 값에는 `float`를 사용하는 편이 안전합니다.

반대로 색상, 밝기, 노멀, 0~1 범위의 마스크처럼 값의 범위가 작고 약간의 정밀도 손실이 눈에 잘 띄지 않는 데이터는 `half`로 낮추기 좋은 후보입니다. 다만 `half`로 선언했다고 해서 항상 16비트 연산으로 실행되는 것은 아닙니다. 실제 성능 이점은 GPU와 그래픽스 API, 컴파일러가 이 값을 최종 코드에서 어떻게 처리하는지에 따라 달라지며, 이 차이를 다음 절에서 살펴봅니다.

<br>

### 플랫폼마다 다른 half 처리

`half`는 중간 정밀도 타입이지만, 소스 코드에 `half`라고 적은 값이 모든 환경에서 반드시 16비트 연산으로 실행되는 것은 아닙니다. 셰이더 타입은 컴파일 과정에서 그래픽스 API와 GPU가 지원하는 연산 정밀도에 맞게 변환됩니다. 만약 대상 환경이 16비트 연산을 효율적으로 지원하면 `half`가 16비트 값으로 유지될 수 있지만, 그렇지 않다면 32비트 `float`처럼 처리될 수 있습니다.

그 결과 `half`의 성능 효과도 환경에 따라 달라집니다. 32비트로 처리되는 환경에서는 `float`와 차이가 거의 없지만, 16비트 연산을 활용하는 환경에서는 레지스터 사용량이 줄거나 ALU 처리량이 좋아질 수 있습니다.

따라서 `half`는 정밀도 손실이 문제가 되지 않는 값에 제한적으로 적용하고, 실제 대상 기기에서 성능 이점과 화면 품질을 함께 확인하는 방식으로 사용해야 합니다.

<br>

### 16비트 연산 지원 GPU에서의 이점

16비트 연산을 잘 지원하는 GPU에서는 `half`가 실제 성능 이점으로 이어질 수 있습니다. 같은 연산 폭 안에서 16비트 값을 더 많이 처리할 수 있거나, 같은 값을 저장하는 데 필요한 레지스터와 메모리 대역폭이 줄어들 수 있기 때문입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- Title -->
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">같은 32비트 폭의 연산 유닛에서의 처리 차이</text>
  <!-- float section -->
  <text x="40" y="50" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">float 연산:</text>
  <!-- Single 32-bit block -->
  <rect x="40" y="60" width="280" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="83" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">32비트 값 1개</text>
  <!-- float annotation -->
  <text x="340" y="78" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← 한 사이클에 1개 처리</text>
  <!-- half section -->
  <text x="40" y="126" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">half 연산:</text>
  <!-- Two 16-bit blocks side by side -->
  <rect x="40" y="136" width="140" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="159" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">16비트 값 A</text>
  <rect x="180" y="136" width="140" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="159" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">16비트 값 B</text>
  <!-- half annotation -->
  <text x="340" y="154" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← 한 사이클에 2개 처리</text>
  <!-- Conclusion -->
  <text x="230" y="210" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">같은 하드웨어 폭에 half 2개가 들어가면 처리량이 증가</text>
</svg>
</div>

<br>

일부 GPU는 32비트 연산을 처리하던 폭 안에서 16비트 연산을 더 많이 배치할 수 있습니다. 이런 구조에서는 `half` 연산의 처리량이 `float`보다 높아질 수 있습니다. 다만 이 효과는 모든 GPU나 모든 셰이더 명령에 항상 적용되는 규칙이 아니라, 하드웨어와 컴파일러가 실제 16비트 연산을 활용할 때 나타나는 이점입니다.

연산 처리량 외에도 레지스터 사용량이 줄어들 수 있습니다. `half` 변수가 실제 16비트로 유지되면 같은 수의 값을 더 작은 정밀도로 보관할 수 있어, 셰이더가 요구하는 레지스터 부담이 낮아질 수 있습니다.

레지스터 부담이 줄어드는 효과는 **점유율(occupancy)**과 연결됩니다. 점유율은 GPU가 동시에 유지할 수 있는 스레드가 얼마나 충분한지를 나타내는 지표입니다. 레지스터 파일은 실행 중인 스레드들이 나누어 쓰는 한정된 자원이므로, 스레드 하나가 차지하는 레지스터 수가 줄어들면 같은 레지스터 파일 안에 더 많은 스레드를 유지할 수 있습니다.

점유율이 높아지면 텍스처 샘플링이나 메모리 접근을 기다리는 동안 다른 스레드를 실행하기 쉬워져, 연산 유닛이 쉬는 시간을 줄이는 데 도움이 됩니다. 따라서 레지스터 사용량이 점유율을 제한하던 셰이더에서는 `half` 사용이 성능 개선으로 이어질 수 있습니다.

<br>

| 항목 | 기대할 수 있는 효과 | 실제 효과가 나타나는 조건 |
|------|---------------------|---------------------------|
| ALU 처리량 | 같은 시간에 더 많은 연산을 처리할 수 있음 | GPU와 컴파일러가 16비트 연산을 실제로 사용 |
| 레지스터 사용량 | 값 하나를 보관하는 부담 감소 | `half`가 16비트 값으로 유지됨 |
| 점유율 | 동시에 유지할 수 있는 스레드 수 증가 가능 | 레지스터 사용량이 점유율을 제한함 |
| 메모리 대역폭 | 저장하거나 전송할 데이터량 감소 가능 | 버퍼·텍스처 포맷까지 16비트로 사용 |

<br>

### 정밀도 선택 기준

`half`는 값의 범위가 좁고, 약간의 정밀도 손실이 화면에 잘 드러나지 않는 데이터에 우선 적용하는 편이 안전합니다. 반대로 값의 범위가 넓거나 작은 차이가 화면 결과에 직접 영향을 주는 계산은 `float`로 유지해야 합니다.

<br>

| 데이터 | 권장 정밀도 | 이유 |
|--------|-------------|------|
| 색상 (RGB, RGBA) | `half` 후보 | 보통 0~1 범위이며 작은 오차가 눈에 잘 띄지 않음 |
| 밝기·마스크 값 | `half` 후보 | 대부분 0~1 범위에서 사용됨 |
| 법선 벡터 (Normal) | `half` 후보 | -1~1 범위의 방향 정보이며, 많은 모바일 셰이더에서 낮은 정밀도로 처리 가능 |
| 조명 계산 중간값 | `half` 후보 | dot product, 감쇠 값처럼 제한된 범위의 값이 많음 |
| 위치 (Position) | `float` 권장 | 월드 좌표가 커질수록 정밀도 부족이 눈에 띄기 쉬움 |
| 깊이 (Depth) | `float` 권장 | 작은 차이가 Z-fighting이나 그림자 판정에 영향을 줄 수 있음 |
| 행렬 변환 (MVP 등) | `float` 권장 | 곱셈이 연쇄되어 오차가 누적되기 쉬움 |

<br>

대표적으로 위치 계산은 `float`로 유지하는 편이 안전합니다. `half`는 `float`보다 유효 정밀도가 낮으므로, 월드 좌표처럼 값이 커질수록 작은 위치 변화를 세밀하게 표현하기 어렵습니다. 만약 월드 좌표나 카메라 상대 좌표 계산에 `half`를 사용하면, 카메라 이동 중 오브젝트가 미세하게 떨리는 현상이 나타날 수 있습니다.

반대로 색상, 마스크, 법선, 단순 조명 중간값처럼 범위가 제한된 값은 `half`로 낮춰도 시각적 차이가 작을 가능성이 큽니다. 다만 타일링이 큰 UV, 넓은 거리 범위의 감쇠 계산, 깊이와 그림자 비교처럼 작은 오차가 결과를 바꿀 수 있는 값은 예외로 두어야 합니다.

<br>

### 혼합 정밀도 예시

실제 코드에서는 변수의 역할에 따라 `float`와 `half`를 섞어 쓰는 경우가 많습니다. 아래 코드는 한 가지 예시로, 위치와 UV는 보수적으로 `float`로 두고 법선과 단순 조명 계산은 `half` 후보로 둔 형태입니다.

<br>

```hlsl
// 버텍스 셰이더 출력 (보간기)
struct v2f
{
    float4 pos    : SV_POSITION; // 클립 공간 위치는 float 유지
    float2 uv     : TEXCOORD0;   // 타일링 가능성이 있으면 float 유지
    half3 normal  : TEXCOORD1;   // 정규화된 방향 값은 half 후보
};

// 프래그먼트 셰이더
half4 frag(v2f i) : SV_Target
{
    // 색상은 보통 0~1 범위이므로 half 후보
    half4 albedo = SAMPLE_TEXTURE2D(_MainTex, sampler_MainTex, i.uv);

    // 단순 조명 중간값도 범위가 제한적이면 half 후보
    half3 n = normalize(i.normal);
    half NdotL = saturate(dot(n, _MainLightDirection.xyz));
    half3 diffuse = albedo.rgb * NdotL * _MainLightColor.rgb;

    return half4(diffuse, albedo.a);
}
```

이 예시는 정밀도 선택을 보수적으로 적용한 형태입니다. 위치는 화면상의 정점 위치를 결정하므로 `float`로 유지하고, 법선과 색상, 단순 조명 중간값처럼 범위가 제한된 값은 `half` 후보로 둡니다. 대상 환경이 16비트 연산을 실제로 활용한다면 이런 값에서 레지스터 사용량이나 ALU 처리량 이점을 기대할 수 있습니다.

UV도 0~1 범위에 머문다면 `half` 후보가 될 수 있습니다. 다만 타일링을 적용하면 샘플링에 사용하는 UV에 타일링 배수가 곱해져 값의 범위가 커집니다. 부동소수점은 값이 커질수록 표현 간격도 커지므로, 큰 UV 값을 `half`로 다루면 샘플링 위치가 어긋나 텍스처가 흔들리거나 뭉개져 보일 수 있습니다. 그래서 예시에서는 타일링 가능성을 고려해 UV를 `float`로 선언했습니다.

정리하면, `half`는 색상이나 방향처럼 제한된 범위에 머무는 값부터 적용하고, 위치·깊이·큰 범위의 UV처럼 작은 오차가 화면에 바로 드러나는 값은 `float`로 남기는 것이 안전합니다.

---

## 명령어 수와 성능의 관계

셰이더의 비용을 줄이려면 먼저 현재 셰이더가 어느 정도의 일을 하고 있는지 확인해야 합니다. 이때 가장 먼저 확인할 수 있는 지표가 **명령어 수(instruction count)**입니다.

명령어 수는 셰이더 컴파일러가 HLSL을 대상 GPU용 코드로 변환한 뒤, 해당 셰이더가 실행하는 연산의 규모를 보여 줍니다. 같은 조건이라면 명령어 수가 적은 셰이더일수록 GPU가 처리해야 할 작업도 줄어듭니다. 따라서 명령어 수는 셰이더 간 비용을 비교할 때 출발점으로 사용할 수 있습니다.

다만 명령어 수가 성능을 완전히 결정하지는 않습니다. 앞에서 본 것처럼 텍스처 샘플링, 메모리 대역폭, 정밀도, 실행 횟수도 함께 영향을 주므로, 명령어 수는 절대적인 답이 아니라 병목을 추정하기 위한 첫 번째 지표로 보는 편이 안전합니다.

<br>

### Unity에서 명령어 수 확인

Unity에서 셰이더 파일을 선택하고 Inspector의 "Compile and show code"를 누르면, 선택한 플랫폼과 그래픽스 API 기준으로 컴파일된 셰이더 코드를 확인할 수 있습니다. 이 출력에는 버텍스 셰이더와 프래그먼트 셰이더가 각각 어떤 종류의 명령어를 얼마나 사용하는지가 함께 표시됩니다.

<br>

```
컴파일된 셰이더 출력 (예시)

// OpenGL ES 3.0 (Mali GPU 대상)
//
// Vertex shader:   8 math, 0 texture          총  8 명령어
// Fragment shader: 12 math, 3 texture          총 15 명령어
```

<br>

성능 예산이 제한된 프로젝트에서는 특히 프래그먼트 셰이더의 명령어 수를 먼저 확인하는 것이 좋습니다. 프래그먼트 셰이더는 화면 픽셀 수와 오버드로우에 비례해 반복 실행되므로, 명령어 수가 조금만 늘어도 전체 비용이 크게 누적될 수 있습니다.

<br>

| 프래그먼트 셰이더 명령어 수 | 해석 | 확인할 점 |
|-----------------------------|------|------------|
| 5 ~ 15 | 매우 단순한 셰이더 | 단색, 텍스처 1장, 간단한 보정 |
| 15 ~ 30 | 비교적 가벼운 셰이더 | 기본 텍스처 샘플링과 단순 조명 |
| 30 ~ 60 | 비용 확인이 필요한 셰이더 | 화면 점유율, 오버드로우, 텍스처 수 확인 |
| 60 이상 | 고비용 후보 | 품질 단계 분리나 연산 단순화 검토 |

<br>

이 표는 절대적인 기준이 아니라, 프래그먼트 셰이더를 처음 훑어볼 때 사용하는 대략적인 눈금입니다. 같은 30개 명령어라도 텍스처 샘플링이 많은 셰이더와 ALU 연산 중심의 셰이더는 실제 비용이 다를 수 있습니다. 텍스처 캐시 적중률, 대역폭, 분기, 정밀도, 오버드로우가 모두 함께 영향을 주기 때문입니다.

따라서 명령어 수는 단독 결론이 아니라 비교의 출발점으로 보는 편이 안전합니다. 같은 플랫폼, 같은 렌더링 조건, 비슷한 유형의 셰이더끼리 비교할 때 가장 유용합니다.

<br>

### 계산 위치와 보간 오차

앞에서 본 실행 횟수 차이는 연산을 어디에 둘지 판단하는 기준이 됩니다. 프래그먼트마다 반복할 필요가 없는 계산이라면 버텍스 셰이더에서 먼저 처리하고, 그 결과를 프래그먼트로 보간해 사용할 수 있습니다.

예를 들어 `viewDir`을 프래그먼트 셰이더에서 정규화하면, 화면에 생성된 모든 프래그먼트에서 `normalize()`가 실행됩니다. 만약 한 프레임에 200만 개의 프래그먼트가 있다면 정규화도 200만 번 수행됩니다.

같은 계산을 버텍스 셰이더에서 먼저 수행하면 실행 횟수는 정점 수만큼으로 줄어듭니다. 정점이 10만 개라면 `normalize()`는 10만 번만 실행되고, 삼각형 내부의 프래그먼트는 정점에서 계산된 값을 보간해 사용합니다.

다만 버텍스 셰이더에서 계산한 값이 각 프래그먼트에 그대로 전달되는 것은 아닙니다. GPU는 삼각형의 세 정점에서 계산된 값을 기준으로, 삼각형 내부의 각 프래그먼트에 들어갈 값을 선형 보간합니다. 즉, 프래그먼트가 받는 값은 그 위치에서 직접 계산한 결과가 아니라, 주변 정점의 결과를 섞어 만든 근사값입니다.

법선 벡터나 뷰 방향처럼 표면을 따라 부드럽게 변하는 값은 이런 근사로도 충분한 경우가 많습니다. 반대로 하이라이트처럼 픽셀마다 변화가 뚜렷한 계산이나, 화면의 작은 차이가 바로 드러나는 계산은 프래그먼트 셰이더에서 직접 처리하는 편이 안전합니다.

특히 법선이나 뷰 방향처럼 조명 계산에 쓰는 방향 벡터는 보통 길이가 1인 단위 벡터를 기준으로 계산합니다. 그런데 보간은 두 방향을 섞어 중간값을 만드는 과정일 뿐, 결과의 길이를 다시 1로 맞춰 주지는 않습니다. 예를 들어 두 정점의 법선이 각각 `(1, 0, 0)`과 `(0, 1, 0)`이라면, 중간 지점의 보간값은 `(0.5, 0.5, 0)`이 됩니다. 이 벡터의 길이는 1이 아니라 약 0.707입니다.

따라서 보간된 방향 벡터를 정확한 단위 벡터로 사용해야 한다면, 프래그먼트 셰이더에서 다시 `normalize()`를 수행해야 합니다. 이 경우 절감한 비용의 일부가 다시 발생합니다.

따라서 버텍스 셰이더로 옮길 수 있는 연산은, 보간된 값을 사용해도 시각적 차이가 작고 추가 보정 비용이 크지 않은 경우로 제한하는 편이 안전합니다.

---

## 셰이더 비용을 높이는 흔한 패턴

앞에서는 셰이더 비용을 ALU 연산, 텍스처 샘플링, 메모리 대역폭, 정밀도, 실행 횟수로 나누어 살펴보았습니다. 실제 셰이더에서는 이 요소들이 따로 나타나기보다, 특정 코드 패턴 안에서 함께 비용을 키우는 경우가 많습니다.

### 불필요한 고정밀도 연산

프래그먼트 셰이더는 같은 코드를 많은 프래그먼트에서 반복 실행합니다. 이때 색상, 마스크, 단순 조명 중간값처럼 낮은 정밀도로도 충분한 값까지 모두 `float`로 처리하면, 16비트 연산을 활용할 수 있는 환경에서 레지스터 사용량과 ALU 비용이 불필요하게 커질 수 있습니다.

반대로 위치, 깊이, 큰 범위의 UV, 행렬 변환처럼 작은 오차가 화면에 바로 드러나는 값은 `float`로 유지해야 합니다. 따라서 정밀도 최적화의 핵심은 모든 변수를 `half`로 바꾸는 것이 아니라, 낮은 정밀도로도 결과가 안정적으로 유지되는 값을 구분하는 데 있습니다.

<br>

### 반복되는 고비용 수학 연산

`pow()`, `sin()`, `cos()` 같은 함수는 단순한 덧셈이나 곱셈보다 비용이 큽니다. 이런 연산이 프래그먼트 셰이더 안에서 넓은 화면 영역에 반복되면, 셰이더가 ALU 연산 쪽으로 쉽게 무거워질 수 있습니다.

만약 연산의 입력 범위가 정해져 있고 결과가 부드럽게 변한다면, **LUT(Look-Up Table)** 를 사용할 수 있습니다. LUT는 함수의 결과를 미리 계산해 텍스처에 저장해 두고, 런타임에는 수학 함수를 직접 계산하는 대신 텍스처에서 값을 읽는 방식입니다.

<br>

```hlsl
// 직접 계산
half specular = pow(NdotH, _Shininess);

// LUT 조회
half specular = SAMPLE_TEXTURE2D(
    _SpecLUT,
    sampler_SpecLUT,
    half2(NdotH, _Shininess)
).r;
```

다만 LUT를 사용하면 텍스처 슬롯과 메모리를 추가로 사용하고, 샘플링 비용과 캐시 적중률의 영향도 받습니다. 
따라서 LUT는 같은 고비용 함수가 많은 프래그먼트에서 반복되고, 직접 계산보다 텍스처 조회가 더 저렴하다고 판단될 때 적용하는 것이 적절합니다.

<br>

### 텍스처 수와 채널 패킹

PBR(Physically Based Rendering) 워크플로우에서는 Albedo, Normal, Metallic, Roughness, Occlusion, Emission처럼 여러 텍스처를 함께 사용하는 경우가 많습니다. 텍스처를 많이 읽을수록 샘플링 횟수와 메모리 대역폭 부담이 늘어납니다.

Metallic, Roughness, Occlusion 같은 값은 색상처럼 RGB 세 값이 모두 필요한 데이터가 아닙니다. 각 픽셀마다 금속성, 거칠기, 차폐 정도를 나타내는 숫자 하나만 있으면 되므로, 보통 R 채널 하나만 읽어도 충분합니다. 이런 단일 값들을 하나의 RGBA 텍스처에 나누어 담으면, 여러 번의 텍스처 샘플링을 한 번으로 줄일 수 있습니다. 이 방식을 **채널 패킹(Channel Packing)**이라고 합니다.

<br>

| 채널 | 저장할 데이터 예시 |
|------|-------------------|
| R | Metallic |
| G | Roughness |
| B | Occlusion |
| A | 추가 마스크 또는 미사용 |

```hlsl
half3 packed = SAMPLE_TEXTURE2D(_PackedTex, sampler_PackedTex, uv).rgb;
half metallic  = packed.r;
half roughness = packed.g;
half occlusion = packed.b;
```

<br>

채널 패킹을 적용하려면 함께 묶을 데이터의 사용 조건이 맞아야 합니다.
같은 해상도와 같은 UV로 샘플링할 수 있어야 하며, 색상 텍스처가 아니라 데이터 텍스처이므로 sRGB 보정이 적용되지 않도록 주의해야 합니다.
또한 각 데이터가 서로 다른 압축 형식이나 해상도를 필요로 한다면, 별도 텍스처로 두는 편이 더 적절할 수 있습니다.

<br>

### Warp/Wavefront 내 분기 발산

GPU는 여러 스레드를 Warp(NVIDIA) 또는 Wavefront(AMD) 단위로 묶어 같은 명령 흐름으로 실행합니다. 만약 프래그먼트 셰이더의 `if` 조건이 프래그먼트마다 다르게 평가되면, 같은 Warp/Wavefront 안에서도 일부 스레드는 `true` 경로를, 일부 스레드는 `false` 경로를 따라야 합니다. 이런 상황을 **분기 발산(branch divergence)**이라고 합니다.

분기 발산이 발생하면 GPU는 한쪽 경로만 실행하고 끝낼 수 없습니다. `true` 경로와 `false` 경로를 차례로 처리해야 하므로, 조건문이 기대한 것만큼 작업을 줄이지 못할 수 있습니다. 반대로 조건이 머티리얼이나 오브젝트 단위 값처럼 묶음 전체에서 같게 평가된다면, 같은 `if`문이라도 발산 비용은 크게 늘어나지 않습니다.

> Warp/Wavefront와 분기 발산의 기본 원리는 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서 자세히 다룹니다.

<br>

```hlsl
// 조건이 프래그먼트마다 달라지면 분기 발산 가능
if (brightness > 0.5)
{
    color *= 2.0;
}

// 값 선택만 필요하다면 산술식으로 대체 가능
color *= lerp(1.0, 2.0, step(0.5, brightness));
```

`step()`과 `lerp()`를 사용하면 간단한 값 선택을 분기 없이 표현할 수 있습니다. 이 방식은 Warp/Wavefront 안의 스레드가 같은 명령 흐름을 유지하게 해 주지만, 대신 양쪽 값을 계산한 뒤 그중 하나를 선택하는 형태가 되기 쉽습니다.

따라서 항상 `if`문보다 빠르다고 볼 수는 없습니다. 조건이 머티리얼 값처럼 균일하게 평가된다면 발산이 거의 없고, 분기 안에서 무거운 계산이나 텍스처 샘플링을 건너뛸 수 있다면 `if`문을 유지하는 편이 더 나을 수 있습니다.

결국 분기 최적화는 `if`문을 없애는 작업이 아니라, 조건이 프래그먼트마다 갈리는지와 각 경로에서 실제로 줄어드는 비용을 함께 판단하는 작업입니다.

---

## 마무리

- 셰이더 비용은 ALU 연산, 텍스처 샘플링, 메모리 대역폭이 함께 결정하며, 병목 유형에 따라 최적화 방향이 달라집니다.
- HLSL 소스는 플랫폼별 컴파일러와 GPU 드라이버를 거쳐 다른 기계어로 변환되므로, 최종 성능은 실제 대상 기기에서 확인해야 합니다.
- 프래그먼트 셰이더는 프래그먼트 수와 오버드로우에 비례해 반복 실행되므로, 작은 명령어 차이도 전체 비용으로 크게 누적될 수 있습니다.
- `half`는 값의 범위와 정밀도가 충분한 경우에만 적용해야 하며, 실제 이점은 대상 GPU가 16비트 연산을 활용할 때 나타납니다.
- LUT, 채널 패킹, 분기 대체, 버텍스 셰이더로의 연산 이동은 비용을 줄일 수 있지만, 각각 텍스처 비용, 데이터 조건, 분기 균일성, 보간 오차를 함께 고려해야 합니다.

셰이더 최적화는 그래픽 품질을 단순히 낮추는 작업이 아니라, 같은 결과를 더 적은 실행 횟수와 더 적절한 데이터 표현으로 처리하도록 조정하는 과정입니다. 명령어 수, 정밀도, 텍스처 수, 계산 위치를 바꿀 때는 실제 대상 기기에서 성능과 화면 품질을 함께 확인해야 합니다.

다만 개별 셰이더의 비용을 줄이는 것만으로 전체 렌더링 비용이 해결되지는 않습니다. Unity에서는 키워드 조합에 따라 하나의 셰이더 소스에서 수백~수천 개의 **셰이더 배리언트(variant)**가 생성될 수 있고, 배리언트 수가 늘어나면 빌드 시간, 메모리, 로딩 시간에도 영향을 줍니다.

[Part 2](/dev/unity/ShaderOptimization-2/)에서는 셰이더 배리언트 관리와 성능 예산이 제한된 환경에서 사용하는 셰이더 기법을 다룹니다.

<br>

---

**관련 글**
- [Phong Shading Model의 원리](/dev/graphics/PhongShadingModel/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)

**시리즈**
- **셰이더 최적화 (1) - 셰이더 성능의 원리 (현재 글)**
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)

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
- [조명과 그림자 (2) - 그림자와 후처리](/dev/unity/LightingAndShadows-2/)
- **셰이더 최적화 (1) - 셰이더 성능의 원리** (현재 글)
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
