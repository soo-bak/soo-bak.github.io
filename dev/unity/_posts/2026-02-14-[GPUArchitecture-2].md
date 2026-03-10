---
layout: single
title: "GPU 아키텍처 (2) - 모바일 GPU와 TBDR - soo:bak"
date: "2026-02-14 11:10:00 +0900"
description: 모바일 GPU의 대역폭 제한, TBR/TBDR 원리, 온칩 타일 메모리, Mali/Adreno/Apple GPU 비교, 오버드로우를 설명합니다.
tags:
  - Unity
  - 최적화
  - GPU
  - TBR
  - TBDR
  - 모바일
---

## 모바일 GPU의 대역폭 제약

[이전 글](/dev/unity/GPUArchitecture-1/)에서 데스크톱 GPU의 구조와 렌더링 파이프라인을 다루었습니다.

데스크톱 GPU는 **IMR(Immediate Mode Rendering)** 방식으로 동작합니다. CPU가 드로우 콜을 제출하면, GPU는 즉시 렌더링 파이프라인 전체를 실행하여 프레임버퍼에 기록합니다.

텍스처, 버텍스/인덱스 버퍼, 프레임버퍼(컬러·깊이·스텐실) 등 렌더링에 필요한 데이터는 모두 GPU 코어 외부의 **VRAM(Video RAM, 비디오 메모리)** 에 위치합니다. 특히 프레임버퍼는 각 프래그먼트를 처리할 때마다 깊이 값을 읽고, 비교하고, 새 색상을 쓰므로 접근 빈도가 높습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 780 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 780px; width: 100%;">
  <!-- Title -->
  <text x="390" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">IMR 방식의 메모리 접근 패턴</text>

  <!-- Row offsets: A=60, B=120, C=180 -->

  <!-- Draw Call A -->
  <rect x="10" y="44" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="64" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">드로우 콜 A</text>
  <!-- Arrow from Draw Call A to pipeline A -->
  <line x1="90" y1="60" x2="112" y2="60" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="112,55 122,60 112,65" fill="currentColor"/>

  <!-- Pipeline A -->
  <rect x="122" y="44" width="36" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="64" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">VS</text>
  <line x1="158" y1="60" x2="170" y2="60" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="168,57 174,60 168,63" fill="currentColor" opacity="0.5"/>
  <rect x="174" y="44" width="50" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="199" y="64" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">클리핑</text>
  <line x1="224" y1="60" x2="236" y2="60" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="234,57 240,60 234,63" fill="currentColor" opacity="0.5"/>
  <rect x="240" y="44" width="60" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="64" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">래스터화</text>
  <line x1="300" y1="60" x2="312" y2="60" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="310,57 316,60 310,63" fill="currentColor" opacity="0.5"/>
  <rect x="316" y="44" width="36" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="334" y="64" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">FS</text>
  <line x1="352" y1="60" x2="364" y2="60" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="362,57 368,60 362,63" fill="currentColor" opacity="0.5"/>
  <rect x="368" y="44" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="413" y="64" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">테스트/블렌딩</text>

  <!-- Draw Call B -->
  <rect x="10" y="104" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">드로우 콜 B</text>
  <line x1="90" y1="120" x2="112" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="112,115 122,120 112,125" fill="currentColor"/>

  <!-- Pipeline B -->
  <rect x="122" y="104" width="36" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">VS</text>
  <line x1="158" y1="120" x2="170" y2="120" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="168,117 174,120 168,123" fill="currentColor" opacity="0.5"/>
  <rect x="174" y="104" width="50" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="199" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">클리핑</text>
  <line x1="224" y1="120" x2="236" y2="120" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="234,117 240,120 234,123" fill="currentColor" opacity="0.5"/>
  <rect x="240" y="104" width="60" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">래스터화</text>
  <line x1="300" y1="120" x2="312" y2="120" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="310,117 316,120 310,123" fill="currentColor" opacity="0.5"/>
  <rect x="316" y="104" width="36" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="334" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">FS</text>
  <line x1="352" y1="120" x2="364" y2="120" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="362,117 368,120 362,123" fill="currentColor" opacity="0.5"/>
  <rect x="368" y="104" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="413" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">테스트/블렌딩</text>

  <!-- Draw Call C -->
  <rect x="10" y="164" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">드로우 콜 C</text>
  <line x1="90" y1="180" x2="112" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="112,175 122,180 112,185" fill="currentColor"/>

  <!-- Pipeline C -->
  <rect x="122" y="164" width="36" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">VS</text>
  <line x1="158" y1="180" x2="170" y2="180" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="168,177 174,180 168,183" fill="currentColor" opacity="0.5"/>
  <rect x="174" y="164" width="50" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="199" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">클리핑</text>
  <line x1="224" y1="180" x2="236" y2="180" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="234,177 240,180 234,183" fill="currentColor" opacity="0.5"/>
  <rect x="240" y="164" width="60" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">래스터화</text>
  <line x1="300" y1="180" x2="312" y2="180" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="310,177 316,180 310,183" fill="currentColor" opacity="0.5"/>
  <rect x="316" y="164" width="36" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="334" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">FS</text>
  <line x1="352" y1="180" x2="364" y2="180" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="362,177 368,180 362,183" fill="currentColor" opacity="0.5"/>
  <rect x="368" y="164" width="90" height="32" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="413" y="184" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">테스트/블렌딩</text>

  <!-- Converging arrows to Framebuffer -->
  <!-- Line from A pipeline end -->
  <line x1="458" y1="60" x2="540" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <!-- Line from B pipeline end -->
  <line x1="458" y1="120" x2="540" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <!-- Line from C pipeline end -->
  <line x1="458" y1="180" x2="540" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <!-- Arrowheads -->
  <polygon points="537,94 546,100 537,106" fill="currentColor"/>
  <polygon points="537,115 546,120 537,125" fill="currentColor"/>
  <polygon points="537,134 546,140 537,146" fill="currentColor"/>

  <!-- Framebuffer box -->
  <rect x="546" y="80" width="130" height="80" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="2"/>
  <text x="611" y="116" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">프레임버퍼</text>
  <text x="611" y="134" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">(VRAM)</text>

  <!-- Bottom annotation -->
  <text x="390" y="232" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">테스트/블렌딩에서 삼각형마다 프레임버퍼 읽기/쓰기 발생</text>

  <!-- Double-headed arrow between Test/Blend and Framebuffer for row B to show read/write -->
  <line x1="480" y1="245" x2="540" y2="245" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.4"/>
  <polygon points="482,242 476,245 482,248" fill="currentColor" opacity="0.4"/>
  <polygon points="538,242 544,245 538,248" fill="currentColor" opacity="0.4"/>
  <text x="510" y="260" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">읽기/쓰기</text>
</svg>
</div>

IMR은 프래그먼트마다 VRAM의 프레임버퍼를 읽고 써야 하므로, 넓은 메모리 대역폭이 필요합니다.
데스크톱 GPU는 전용 VRAM과 128~512bit 폭의 메모리 버스로 수백~수천 GB/s의 대역폭을 확보할 수 있고, 전원 콘센트에서 수백 W를 공급받으므로 전력 제약도 적습니다.

반면 모바일 환경은 배터리로 동작하므로 GPU에 할당할 수 있는 전력이 수 W로 제한되고, GPU 전용 메모리 없이 CPU와 시스템 메모리를 공유합니다.

---

## 모바일의 대역폭 문제

모바일 기기에서 CPU와 GPU는 하나의 **SoC(System on Chip)** 안에 통합되어 있으며, **LPDDR(Low Power Double Data Rate)** 메모리를 함께 사용합니다.
이처럼 하나의 메모리를 공유하는 구조를 **통합 메모리 아키텍처(Unified Memory Architecture, UMA)** 라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <!-- Title -->
  <text x="340" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">데스크톱 vs 모바일 메모리 구조</text>

  <!-- ===== Desktop Section ===== -->
  <text x="20" y="52" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">데스크톱</text>

  <!-- CPU box -->
  <rect x="20" y="62" width="90" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="92" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">CPU</text>

  <!-- PCIe arrow CPU -> GPU -->
  <line x1="110" y1="87" x2="185" y2="87" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="183,82 193,87 183,92" fill="currentColor"/>
  <text x="152" y="80" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">PCIe</text>

  <!-- GPU box -->
  <rect x="193" y="62" width="100" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="243" y="92" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">GPU</text>
  <text x="243" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">별도 칩</text>

  <!-- Double-headed arrow GPU <-> VRAM -->
  <line x1="293" y1="80" x2="438" y2="80" stroke="currentColor" stroke-width="2"/>
  <line x1="293" y1="94" x2="438" y2="94" stroke="currentColor" stroke-width="2"/>
  <polygon points="295,75 287,80 295,85" fill="currentColor"/>
  <polygon points="436,75 444,80 436,85" fill="currentColor"/>
  <polygon points="295,89 287,94 295,99" fill="currentColor"/>
  <polygon points="436,89 444,94 436,99" fill="currentColor"/>
  <text x="366" y="74" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">128~512bit 버스</text>
  <text x="366" y="108" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">수백~수천 GB/s</text>

  <!-- VRAM box -->
  <rect x="444" y="62" width="140" height="50" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="514" y="85" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">전용 VRAM</text>
  <text x="514" y="101" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">(GDDR6 / HBM)</text>

  <!-- Power annotation desktop -->
  <text x="243" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">별도 전원 공급 (수백 W)</text>

  <!-- ===== Divider ===== -->
  <line x1="20" y1="168" x2="660" y2="168" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <!-- ===== Mobile Section ===== -->
  <text x="20" y="194" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">모바일 (SoC)</text>

  <!-- SoC outer box -->
  <rect x="20" y="204" width="270" height="110" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="2"/>
  <text x="155" y="298" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">SoC 칩 내부</text>

  <!-- CPU inside SoC -->
  <rect x="40" y="222" width="100" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="252" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">CPU</text>

  <!-- GPU inside SoC -->
  <rect x="170" y="222" width="100" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="252" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">GPU</text>

  <!-- Double-headed arrow SoC <-> LPDDR -->
  <line x1="290" y1="250" x2="438" y2="250" stroke="currentColor" stroke-width="2"/>
  <line x1="290" y1="264" x2="438" y2="264" stroke="currentColor" stroke-width="2"/>
  <polygon points="292,245 284,250 292,255" fill="currentColor"/>
  <polygon points="436,245 444,250 436,255" fill="currentColor"/>
  <polygon points="292,259 284,264 292,269" fill="currentColor"/>
  <polygon points="436,259 444,264 436,269" fill="currentColor"/>
  <text x="364" y="244" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">64~128bit 버스</text>
  <text x="364" y="278" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">25~50 GB/s</text>
  <text x="364" y="292" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(대역폭 공유)</text>

  <!-- LPDDR box -->
  <rect x="444" y="232" width="140" height="50" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="514" y="255" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">공유 LPDDR</text>
  <text x="514" y="271" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">(시스템 RAM)</text>

  <!-- Power annotation mobile -->
  <text x="155" y="330" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">배터리 전원 (수 W)</text>
</svg>
</div>

UMA 구조에서는 두 가지 제약이 생깁니다.

**메모리 버스 폭의 차이.** 모바일 SoC의 메모리 버스는 64~128bit으로, 데스크톱(128~512bit)의 절반 이하입니다. 버스 폭이 좁으면 한 클럭당 전송할 수 있는 데이터양이 줄어들어, 모바일의 메모리 대역폭은 25~50 GB/s 수준에 머뭅니다.

> **클럭(clock):** 메모리와 컨트롤러가 한 번 신호를 주고받는 주기입니다. 128bit 버스는 매 클럭마다 16바이트를, 64bit 버스는 8바이트를 전송합니다.

**메모리 대역폭과 전력의 관계.** LPDDR 메모리에서 데이터를 읽거나 쓸 때마다 메모리 컨트롤러, 메모리 버스, DRAM 셀이 모두 활성화되며 전력을 소비합니다.
ARM의 기술 문서에 따르면, 외부 메모리 접근은 칩 내부 메모리 접근에 비해 약 10배 이상의 에너지를 소비합니다. 배터리 전력이 제한적인 모바일 환경에서는 외부 메모리 접근을 줄이는 것이 성능과 전력 효율 모두에 직접적인 영향을 줍니다.

해상도 1920×1080, 60fps 기준으로 프레임버퍼 대역폭을 계산하면 이 제약이 어느 정도인지 확인할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text x="240" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레임버퍼 대역폭 계산</text>
  <line x1="40" y1="34" x2="440" y2="34" stroke="currentColor" stroke-width="1.5"/>
  <!-- 입력 항목 -->
  <text x="60" y="62" font-family="sans-serif" font-size="11" fill="currentColor">픽셀 수</text>
  <text x="420" y="62" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">1920 × 1080 = 2,073,600</text>
  <text x="60" y="86" font-family="sans-serif" font-size="11" fill="currentColor">색상 버퍼</text>
  <text x="420" y="86" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">4 바이트/픽셀 (RGBA8)</text>
  <text x="60" y="110" font-family="sans-serif" font-size="11" fill="currentColor">깊이 버퍼</text>
  <text x="420" y="110" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">4 바이트/픽셀 (D24S8)</text>
  <!-- 구분선 -->
  <line x1="40" y1="122" x2="440" y2="122" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- 소계 -->
  <text x="60" y="148" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">픽셀당 합계</text>
  <text x="420" y="148" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">8 바이트</text>
  <!-- 구분선 -->
  <line x1="40" y1="162" x2="440" y2="162" stroke="currentColor" stroke-width="1.5"/>
  <!-- 계산 결과 -->
  <text x="60" y="190" font-family="sans-serif" font-size="11" fill="currentColor">프레임당 크기</text>
  <text x="420" y="190" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">2,073,600 × 8 ≈ 16 MB</text>
  <text x="60" y="218" font-family="sans-serif" font-size="11" fill="currentColor">초당 (60fps)</text>
  <text x="420" y="218" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor">16 MB × 60 ≈ 960 MB/s</text>
  <!-- 최종 결과 강조 -->
  <rect x="140" y="238" width="200" height="30" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="258" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">≈ 1 GB/s (쓰기만)</text>
</svg>
</div>

위 수치는 모든 픽셀이 정확히 한 번씩만 쓰이고, 깊이 읽기나 오버드로우가 없는 이상적인 경우입니다.

실제로는 프래그먼트마다 깊이를 읽고(4바이트), 테스트를 통과하면 색상과 깊이를 다시 기록(4+4바이트)해야 하므로 픽셀당 12바이트, 약 1.5배가 됩니다. 같은 픽셀을 여러 삼각형이 덮어쓰는 **오버드로우**가 평균 2x라면 여기에 다시 2배가 곱해집니다.

$$\sim 1\,\text{GB/s} \times 1.5\,(\text{읽기+쓰기}) \times 2\,(\text{오버드로우 2x}) = \sim 3\,\text{GB/s}$$

MSAA(멀티샘플 안티앨리어싱)를 적용하면 픽셀당 여러 샘플(4x일 경우 4개)을 저장해야 하므로 프레임버퍼 크기와 대역폭이 샘플 수에 비례하여 증가합니다.

<br>

위 예시처럼 1080p, 60fps 기준으로도 프레임버퍼 접근만으로 약 3 GB/s를 소비하는데, 모바일 GPU의 총 대역폭은 25~50 GB/s입니다. 여기에 텍스처 읽기, 버텍스 데이터 로드, 포스트 프로세싱 등이 같은 대역폭을 나눠 써야 하므로, IMR 방식으로는 대역폭이 부족합니다.

모바일 GPU는 이 문제를 해결하기 위해 IMR과 다른 렌더링 방식을 사용합니다.

---

## 타일 기반 렌더링의 원리 — TBR과 TBDR

**타일 기반 렌더링(Tile-Based Rendering)** 은 화면 전체를 한 번에 처리하는 대신, 16×16 또는 32×32 픽셀 크기의 작은 타일로 나누어 하나씩 렌더링하는 방식입니다.

모바일 GPU 칩 내부에는 타일 렌더링을 위한 전용 SRAM인 **온칩 타일 메모리(On-Chip Tile Memory)** 가 있습니다. GPU 실리콘 위에 직접 배치되어 있어 외부 LPDDR에 비해 접근 속도가 빠르고 전력 소비가 낮습니다.

타일이 충분히 작으면(16×16 또는 32×32 픽셀), 해당 타일의 컬러·깊이·스텐실 버퍼가 이 온칩 타일 메모리에 들어갑니다.

깊이 테스트와 색상 블렌딩이 온칩 타일 메모리 안에서 이루어지면 외부 LPDDR을 거치지 않으므로, IMR에서 문제가 되었던 프래그먼트당 외부 메모리 접근이 대폭 줄어듭니다.

타일 렌더링이 끝나면 최종 컬러만 외부 메모리에 기록하고, 깊이·스텐실 버퍼는 이후 패스에서 필요하지 않으면 기록하지 않고 폐기하여 대역폭을 추가로 절감합니다.

<br>

타일 기반 렌더링은 크게 **TBR(Tile-Based Rendering)**과 **TBDR(Tile-Based Deferred Rendering)**로 나뉩니다. 둘 다 버텍스 셰이더를 먼저 실행하여 모든 삼각형을 타일별로 분류(비닝)한 뒤, 타일 단위로 프래그먼트 셰이딩을 실행합니다.

차이는 프래그먼트 셰이딩 시점입니다.
TBR(ARM Mali, Qualcomm Adreno 등)은 비닝 후 타일 내의 모든 프래그먼트를 셰이딩하며, Early-Z 테스트로 가려진 프래그먼트를 걸러냅니다.

TBDR(Apple GPU/PowerVR 등)은 타일 내에서 **가시성 판정(Hidden Surface Removal, HSR)**을 먼저 수행하여 최종적으로 보이는 프래그먼트만 셰이딩합니다. 가시성이 확인될 때까지 프래그먼트 셰이딩을 미룬다(deferred)는 뜻에서 TBDR이라는 이름이 붙었습니다.

두 방식 모두 비닝과 타일 렌더링의 두 단계로 구성됩니다.

### 1단계: Binning (타일 분류)

GPU는 제출된 모든 드로우 콜에 대해 버텍스 셰이더를 실행하여, 각 정점을 화면 좌표(Screen Space)로 변환합니다.

변환이 끝나면 삼각형이 화면의 어떤 타일에 걸치는지 계산하고, 걸치는 타일마다 해당 삼각형을 등록합니다. 하나의 삼각형이 여러 타일에 걸칠 수 있으므로, 같은 삼각형이 여러 타일에 동시에 등록되기도 합니다.

이 결과물이 **타일 리스트(Tile List)** 입니다. 각 타일에 그려져야 할 삼각형 목록이 기록되며, 이 데이터는 공유 LPDDR에 저장됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 제목 -->
  <text x="280" y="20" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Binning 단계</text>

  <!-- 타일 그리드 4x3 (배경) -->
  <rect x="40" y="38" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="120" y="38" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="200" y="38" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="280" y="38" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="40" y="98" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="120" y="98" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="200" y="98" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="280" y="98" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="40" y="158" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="120" y="158" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="200" y="158" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>
  <rect x="280" y="158" width="80" height="60" rx="2" fill="none" stroke="currentColor" stroke-width="1" opacity="0.25"/>

  <!-- 타일 번호 (좌상단 작게) -->
  <text x="48" y="52" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T0</text>
  <text x="128" y="52" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T1</text>
  <text x="208" y="52" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T2</text>
  <text x="288" y="52" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T3</text>
  <text x="48" y="112" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T4</text>
  <text x="128" y="112" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T5</text>
  <text x="208" y="112" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T6</text>
  <text x="288" y="112" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T7</text>
  <text x="48" y="172" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T8</text>
  <text x="128" y="172" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T9</text>
  <text x="208" y="172" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T10</text>
  <text x="288" y="172" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">T11</text>

  <!-- 삼각형 A: T4, T5, T6, T9에 걸침 -->
  <polygon points="80,100 240,108 140,210" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="148" y="155" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">A</text>

  <!-- 삼각형 B: T6, T7, T10, T11에 걸침 -->
  <polygon points="310,95 340,200 220,185" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="295" y="168" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">B</text>

  <!-- 범례 -->
  <line x1="390" y1="68" x2="420" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <text x="428" y="72" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">삼각형 A</text>
  <line x1="390" y1="88" x2="420" y2="88" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="428" y="92" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">삼각형 B</text>

  <!-- 화살표: 그리드 → 타일 리스트 -->
  <line x1="200" y1="226" x2="200" y2="248" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="196,246 200,254 204,246" fill="currentColor"/>
  <text x="200" y="244" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">타일별로 분류</text>

  <!-- 타일 리스트 -->
  <rect x="60" y="260" width="440" height="150" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="280" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">타일 리스트</text>
  <text x="280" y="294" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">공유 LPDDR에 저장</text>
  <line x1="80" y1="300" x2="480" y2="300" stroke="currentColor" stroke-width="1" opacity="0.2"/>

  <!-- 타일 리스트 항목 -->
  <text x="120" y="320" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T4</text>
  <text x="130" y="320" fill="currentColor" font-family="sans-serif" font-size="10">→ [ A ]</text>
  <text x="300" y="320" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T5</text>
  <text x="310" y="320" fill="currentColor" font-family="sans-serif" font-size="10">→ [ A ]</text>

  <text x="120" y="342" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T6</text>
  <text x="130" y="342" fill="currentColor" font-family="sans-serif" font-size="10">→ [ A, B ]</text>
  <text x="260" y="342" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">← 두 삼각형이 겹치는 타일</text>

  <text x="120" y="364" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T7</text>
  <text x="130" y="364" fill="currentColor" font-family="sans-serif" font-size="10">→ [ B ]</text>
  <text x="300" y="364" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T9</text>
  <text x="310" y="364" fill="currentColor" font-family="sans-serif" font-size="10">→ [ A ]</text>

  <text x="120" y="386" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T10</text>
  <text x="130" y="386" fill="currentColor" font-family="sans-serif" font-size="10">→ [ B ]</text>
  <text x="300" y="386" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">T11</text>
  <text x="310" y="386" fill="currentColor" font-family="sans-serif" font-size="10">→ [ B ]</text>
</svg>
</div>

비닝 단계에서는 [이전 글](/dev/unity/GPUArchitecture-1/)에서 다룬 렌더링 파이프라인 중 버텍스 셰이더와 클리핑까지만 실행하고, 여기에 타일 분류를 추가하여 타일 리스트를 구축합니다. 래스터화, 프래그먼트 셰이딩, 테스트/블렌딩은 모두 2단계에서 수행됩니다.

모든 삼각형에 대해 버텍스 셰이더를 실행하고 타일 리스트를 외부 메모리에 기록해야 하므로, 비닝의 비용은 삼각형 수에 비례합니다.
타일 크기도 성능에 영향을 주는데, 타일이 작으면 온칩 타일 메모리 사용량이 줄지만 타일 수가 늘어나 비닝과 타일 전환 오버헤드가 커지고, 타일이 크면 타일당 메모리 요구량이 늘어 동시에 처리할 수 있는 타일 수가 줄어듭니다.
GPU 제조사마다 자사 아키텍처에 맞는 크기를 선택하며, Mali는 16×16, Apple GPU는 32×32 픽셀을 사용합니다.

### 2단계: 타일별 렌더링

두 번째 단계에서 GPU는 타일 리스트에서 해당 타일에 등록된 삼각형 목록을 읽어오고, 온칩 타일 메모리에 컬러·깊이·스텐실 버퍼를 배치합니다.

래스터화, 프래그먼트 셰이딩, 깊이 테스트, 블렌딩 과정에서 읽고 쓰는 컬러·깊이·스텐실 데이터가 모두 이 온칩 타일 메모리에 있으므로, 프래그먼트당 외부 메모리 접근이 대폭 줄어듭니다.

타일의 모든 삼각형 처리가 끝나면 최종 컬러만 외부 메모리의 프레임버퍼에 기록하고, 다음 타일로 이동하여 같은 과정을 반복합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">타일별 렌더링 단계 (타일 T6)</text>

  <!-- 상단: 외부 메모리에서 타일 리스트 로드 -->
  <rect x="110" y="40" width="300" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="60" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">외부 메모리에서 타일 리스트 로드: [삼각형 A, ...]</text>

  <!-- 아래쪽 화살표 -->
  <line x1="260" y1="70" x2="260" y2="95" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,92 260,102 266,92" fill="currentColor"/>

  <!-- 온칩 타일 메모리 큰 박스 -->
  <rect x="50" y="102" width="420" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="2"/>
  <text x="260" y="120" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">온칩 타일 메모리</text>

  <!-- 파이프라인 박스들 -->
  <rect x="80" y="134" width="80" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="120" y="153" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">래스터화</text>
  <line x1="160" y1="148" x2="178" y2="148" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="176,145 182,148 176,151" fill="currentColor" opacity="0.5"/>
  <rect x="182" y="134" width="44" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="204" y="153" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">FS</text>
  <line x1="226" y1="148" x2="244" y2="148" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="242,145 248,148 242,151" fill="currentColor" opacity="0.5"/>
  <rect x="248" y="134" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="298" y="153" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">테스트/블렌딩</text>

  <!-- 양방향 화살표: 테스트/블렌딩 ↔ 깊이/색상 버퍼 -->
  <line x1="298" y1="162" x2="298" y2="186" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="294,165 298,162 302,165" fill="currentColor"/>
  <polygon points="294,183 298,186 302,183" fill="currentColor"/>

  <!-- 깊이 버퍼 + 색상 버퍼 -->
  <rect x="190" y="188" width="220" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="300" y="207" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">깊이 버퍼 + 색상 버퍼</text>

  <!-- 아래쪽 화살표: 타일 완료 -->
  <line x1="260" y1="232" x2="260" y2="262" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,258 260,268 266,258" fill="currentColor"/>
  <text x="290" y="252" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">타일 완료</text>

  <!-- 하단: 외부 메모리 프레임버퍼 -->
  <rect x="80" y="268" width="360" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="286" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">외부 메모리 프레임버퍼</text>
  <text x="260" y="300" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">T6 영역에 최종 색상만 기록</text>
</svg>
</div>

IMR에서는 **프래그먼트마다** 외부 메모리의 프레임버퍼를 읽고 썼지만, TBR/TBDR에서는 프래그먼트 처리 중 컬러·깊이·스텐실 접근이 온칩 타일 메모리에서 이루어지므로, 외부 메모리 기록은 **타일마다** 최종 컬러를 한 번 쓰는 것으로 줄어듭니다.

### IMR vs TBR/TBDR 비교

이 차이를 파이프라인 전체로 비교하면 다음과 같습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <!-- 제목 -->
  <text x="340" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">IMR vs TBR/TBDR: 외부 메모리 접근 비교</text>

  <!-- === IMR 섹션 === -->
  <rect x="10" y="38" width="660" height="170" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="58" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">IMR</text>

  <!-- IMR 파이프라인 -->
  <rect x="30" y="70" width="72" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="66" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">드로우 콜</text>
  <line x1="102" y1="84" x2="116" y2="84" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="114,81 120,84 114,87" fill="currentColor" opacity="0.5"/>
  <rect x="120" y="70" width="36" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="138" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">VS</text>
  <line x1="156" y1="84" x2="170" y2="84" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="168,81 174,84 168,87" fill="currentColor" opacity="0.5"/>
  <rect x="174" y="70" width="50" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="199" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">클리핑</text>
  <line x1="224" y1="84" x2="238" y2="84" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="236,81 242,84 236,87" fill="currentColor" opacity="0.5"/>
  <rect x="242" y="70" width="64" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="274" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">래스터화</text>
  <line x1="306" y1="84" x2="320" y2="84" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="318,81 324,84 318,87" fill="currentColor" opacity="0.5"/>
  <rect x="324" y="70" width="36" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="342" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">FS</text>
  <line x1="360" y1="84" x2="374" y2="84" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="372,81 378,84 372,87" fill="currentColor" opacity="0.5"/>
  <rect x="378" y="70" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="428" y="89" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">테스트/블렌딩</text>

  <!-- 양방향 화살표: 프래그먼트마다 외부 메모리 -->
  <line x1="428" y1="98" x2="428" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="424,101 428,98 432,101" fill="currentColor"/>
  <polygon points="424,125 428,128 432,125" fill="currentColor"/>
  <text x="490" y="116" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(프래그먼트마다)</text>

  <!-- 외부 메모리 프레임버퍼 -->
  <rect x="368" y="130" width="120" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="428" y="146" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">외부 메모리 프레임버퍼</text>

  <!-- IMR 외부 메모리 접근 바 (긴 바) -->
  <text x="30" y="180" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">외부 메모리 접근:</text>
  <rect x="150" y="168" width="400" height="16" rx="3" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <text x="350" y="179" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">프래그먼트마다 깊이 읽기 + 색상 쓰기</text>
  <text x="560" y="180" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">높음</text>

  <!-- === TBR/TBDR 섹션 === -->
  <rect x="10" y="220" width="660" height="230" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">TBR/TBDR</text>

  <!-- TBR/TBDR 1단계 -->
  <text x="30" y="262" fill="currentColor" font-family="sans-serif" font-size="9" font-weight="bold">1단계</text>
  <rect x="70" y="248" width="72" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="106" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">드로우 콜</text>
  <line x1="142" y1="262" x2="156" y2="262" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="154,259 160,262 154,265" fill="currentColor" opacity="0.5"/>
  <rect x="160" y="248" width="36" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="178" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">VS</text>
  <line x1="196" y1="262" x2="210" y2="262" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="208,259 214,262 208,265" fill="currentColor" opacity="0.5"/>
  <rect x="214" y="248" width="50" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="239" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">클리핑</text>
  <line x1="264" y1="262" x2="278" y2="262" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="276,259 282,262 276,265" fill="currentColor" opacity="0.5"/>
  <rect x="282" y="248" width="70" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="317" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">타일 분류</text>
  <line x1="352" y1="262" x2="366" y2="262" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="364,259 370,262 364,265" fill="currentColor" opacity="0.5"/>
  <rect x="370" y="248" width="130" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="435" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">외부 메모리에 저장</text>

  <!-- TBR/TBDR 2단계 -->
  <text x="30" y="316" fill="currentColor" font-family="sans-serif" font-size="9" font-weight="bold">2단계</text>
  <rect x="70" y="296" width="110" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="125" y="315" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">타일 리스트 로드</text>
  <line x1="180" y1="310" x2="194" y2="310" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="192,307 198,310 192,313" fill="currentColor" opacity="0.5"/>

  <!-- 온칩 타일 메모리 박스 -->
  <rect x="198" y="292" width="310" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <rect x="210" y="298" width="64" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="242" y="317" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">래스터화</text>
  <line x1="274" y1="312" x2="288" y2="312" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="286,309 292,312 286,315" fill="currentColor" opacity="0.5"/>
  <rect x="292" y="298" width="36" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="317" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">FS</text>
  <line x1="328" y1="312" x2="342" y2="312" stroke="currentColor" stroke-width="1" opacity="0.5"/>
  <polygon points="340,309 346,312 340,315" fill="currentColor" opacity="0.5"/>
  <rect x="346" y="298" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="396" y="317" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">테스트/블렌딩</text>
  <text x="455" y="290" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">(온칩 타일 메모리 내)</text>

  <!-- 타일 완료 화살표 -->
  <line x1="353" y1="332" x2="353" y2="358" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="347,354 353,364 359,354" fill="currentColor"/>
  <text x="394" y="354" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">타일 완료 시에만</text>

  <!-- 외부 메모리에 최종 색상 기록 -->
  <rect x="253" y="366" width="200" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="353" y="382" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">외부 메모리에 최종 색상 기록</text>

  <!-- TBR/TBDR 외부 메모리 접근 바 (짧은 바) -->
  <text x="30" y="420" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">외부 메모리 접근:</text>
  <rect x="150" y="408" width="60" height="16" rx="3" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <text x="220" y="420" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.7">타일마다 최종 색상만 쓰기</text>
  <text x="220" y="434" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">낮음</text>
</svg>
</div>

IMR은 프래그먼트를 처리할 때마다 외부 메모리의 깊이 값을 읽고, 새 색상을 쓰므로 외부 메모리 접근량이 프래그먼트 수에 비례합니다.
TBR/TBDR은 이 과정이 온칩 타일 메모리에서 이루어지고, 타일의 모든 프래그먼트 처리가 끝난 뒤 최종 색상만 한 번 외부 메모리에 기록합니다.

이러한 이유로 현재 주요 모바일 GPU(Mali, Adreno, Apple GPU)는 타일 기반 아키텍처를 사용합니다.

---

## 온칩 타일 메모리의 이점

타일 기반 렌더링의 핵심 자원은 온칩 타일 메모리입니다.

GPU 칩은 하나의 **실리콘 다이(silicon die)** 위에 연산 유닛, 캐시 등을 집적하는데, 온칩 타일 메모리도 이 다이 위에 **SRAM(Static RAM)** 으로 만들어집니다. 칩 외부에 별도로 존재하는 LPDDR과는 물리적 위치부터 다르고, 이 차이가 속도와 전력 면에서 이점을 만듭니다.

접근 속도는 외부 LPDDR보다 수십 배 빠릅니다. 칩 내부의 배선이 외부 메모리 인터페이스보다 넓고 빠르므로 대역폭 면에서도 유리합니다. 깊이 테스트나 블렌딩처럼 같은 픽셀 위치를 반복적으로 읽고 쓰는 연산에서 이 차이가 극대화됩니다.

전력 소비도 낮습니다. ARM의 공개 자료에 따르면, 외부 메모리 접근은 칩 내부 메모리 접근에 비해 에너지 소비가 약 10배 이상 높습니다. 배터리로 동작하는 모바일 기기에서 이 차이는 중요합니다.

반면 다이 위의 면적이 제한되므로 용량은 작습니다. 온칩 타일 메모리에는 현재 처리 중인 타일의 색상·깊이·스텐실 버퍼가 들어가는데, 16×16 픽셀 타일 기준으로 색상 버퍼(RGBA8, 4바이트 × 256픽셀)에 1,024바이트, 깊이+스텐실 버퍼(D24S8, 4바이트 × 256픽셀)에 1,024바이트이므로 타일 하나에 약 2 KB가 필요합니다. MSAA를 적용하면 픽셀당 여러 색상·깊이 샘플을 저장해야 하므로 버퍼 크기가 샘플 수만큼 늘어납니다(4xMSAA = 픽셀당 4개 샘플 → 2 KB × 4 = 약 8 KB). 타일 크기를 키우거나 MSAA 수준을 높이면 타일당 메모리 요구량이 늘어나 동시에 처리할 수 있는 타일 수가 줄어듭니다.

GPU 전체의 온칩 타일 메모리 용량은 일반적으로 수백 KB ~ 수 MB 규모입니다.

<br>

| 메모리 계층 | 접근 속도 | 전력 소비 | 용량 |
|---|---|---|---|
| 온칩 타일 메모리 (GPU SRAM) | ~1 사이클 | 낮음 | 타일당 수 KB (전체 수백 KB ~ 수 MB) |
| L2 캐시 (GPU 내부) | ~10 사이클 | 중간 | 수백 KB |
| 외부 메모리 (LPDDR) | ~100 사이클 | 높음 | 수 GB |

\* 사이클 = GPU 클럭 1회. 1 GHz GPU 기준 1사이클 ≒ 1 ns<br>
\* 외부 메모리 접근의 에너지 소비는 온칩 SRAM 대비 약 10배 이상

<br>

이러한 속도와 전력의 이점은 렌더링의 여러 단계에서 구체적으로 나타납니다.

깊이 테스트와 블렌딩은 같은 픽셀 위치의 값을 반복적으로 읽고 쓰는 연산입니다.
IMR에서는 이 접근이 모두 외부 메모리에서 이루어지지만, TBR/TBDR에서는 온칩 타일 메모리에서 이루어집니다. 깊이 테스트를 통과하지 못한 프래그먼트는 온칩에서 즉시 폐기되고, 반투명 오브젝트의 블렌딩(기존 색상을 읽어 새 색상과 혼합하는 읽기-수정-쓰기 과정)도 외부 메모리 대역폭을 소비하지 않습니다.

MSAA에서도 이점이 큽니다.
MSAA는 픽셀당 여러 샘플을 유지하므로 메모리 사용량이 샘플 수에 비례하여 늘어납니다.
IMR에서는 이 데이터가 모두 외부 메모리에 상주하여 대역폭 부하가 커지지만, TBR/TBDR에서는 MSAA 샘플이 온칩 타일 메모리에만 존재합니다.
타일이 끝날 때 **리졸브(Resolve)** — 여러 샘플을 하나의 최종 색상으로 합치는 과정 — 를 수행하여 결과만 외부 메모리에 기록하므로, 4xMSAA를 적용해도 외부 메모리 기록량은 MSAA 없이 렌더링할 때와 동일합니다.

타일 렌더링이 끝나면 최종 색상만 외부 메모리에 기록됩니다. 깊이 버퍼, 스텐실 버퍼, MSAA 샘플 데이터는 타일 렌더링 중에만 필요하므로 외부 메모리에 기록하지 않아도 됩니다.

<br>

Unity에서는 이 특성을 활용하는 기능을 제공합니다.
`Memoryless` 렌더 텍스처는 깊이/스텐실 버퍼처럼 프레임이 끝나면 버려도 되는 데이터에 대해 외부 메모리 자체를 할당하지 않는 설정입니다. 데이터가 온칩 타일 메모리에만 존재하고 외부에 기록되지 않으므로 메모리와 대역폭을 모두 절약합니다. 
`FrameBufferFetch`는 셰이더에서 현재 픽셀의 기존 색상이 필요할 때(예: 커스텀 블렌딩), 외부 메모리를 거치지 않고 온칩 타일 메모리에서 직접 읽는 기능입니다.

---

## Mali / Adreno / Apple GPU 비교

모바일 GPU의 주요 세 계열인 ARM(Mali), Qualcomm(Adreno), Apple은 모두 타일 기반 아키텍처를 사용합니다.
비닝과 온칩 타일 메모리의 기본 원리는 동일하지만, 타일 내에서 불필요한 작업을 줄이는 전략이 각각 다릅니다.

### Mali (ARM)

Mali는 ARM이 설계하여 라이센스하는 **GPU IP(Intellectual Property)** 로, Samsung Exynos, MediaTek Dimensity 등 다양한 SoC에 탑재됩니다. 타일 크기는 16×16 픽셀이 기본이며, 세대별로 아키텍처가 크게 달라(Midgard, Bifrost, Valhall 등) Android 기기 간 GPU 성능 편차가 큽니다.

Mali는 타일 내 불필요한 셰이딩을 줄이기 위해 **Forward Pixel Kill(FPK)** 를 사용합니다.
프래그먼트의 깊이 값은 래스터화 단계에서 정점 위치를 보간하여 결정되므로, 프래그먼트 셰이더가 실행되기 전에 이미 확정되어 있습니다. FPK는 이 점을 활용하여, 프래그먼트 셰이딩이 진행되는 도중에 같은 픽셀 위치에 깊이 값이 더 작은 불투명 프래그먼트가 도착하면 이미 진행 중이던 먼 쪽 프래그먼트의 셰이딩을 즉시 중단합니다.
[이전 글](/dev/unity/GPUArchitecture-1/)에서 다룬 Early-Z 테스트가 셰이딩 시작 **전에** 깊이를 비교하여 거부하는 것과 달리, FPK는 셰이딩이 이미 시작된 프래그먼트도 취소할 수 있습니다.

다만 FPK는 셰이딩이 진행 중인 프래그먼트만 취소할 수 있습니다. 먼 쪽 프래그먼트의 셰이딩이 더 가까운 프래그먼트가 도착하기 전에 이미 완료되었다면 그 낭비는 막지 못합니다.
이런 경우를 줄이려면 Early-Z가 셰이딩 전에 최대한 많이 걸러내야 하며, Unity의 Opaque 패스가 기본적으로 불투명 오브젝트를 앞에서 뒤(front-to-back)로 정렬하는 것도 이를 돕기 위해서입니다. 가까운 오브젝트의 깊이가 먼저 기록되면 Early-Z가 뒤쪽 프래그먼트를 거부할 확률이 높아집니다.

> **깊이 테스트, Early-Z, FPK의 차이**
>
> 세 기술은 모두 깊이 값을 비교하지만, 동작 시점과 역할이 달라 각각 필요합니다.
>
> **깊이 테스트(Z-test)** — 프래그먼트 셰이더 **이후**에 수행됩니다. 셰이딩이 완료된 프래그먼트의 깊이를 **깊이 버퍼에 기록된 값**과 비교하여, 더 먼 프래그먼트의 결과를 폐기하고 더 가까운 프래그먼트의 깊이를 기록합니다. 최종 이미지의 정확성을 보장하는 필수 단계이지만, 셰이딩을 마친 뒤에야 깊이를 비교하므로, 최종적으로 폐기되는 프래그먼트의 셰이딩 비용까지 그대로 소비됩니다.
>
> **Early-Z** — 프래그먼트 셰이더 **이전**에 수행됩니다. 새로 도착한 프래그먼트의 깊이를 **깊이 버퍼에 이미 기록된 값**과 비교하여, 더 먼 프래그먼트를 셰이딩 없이 폐기합니다. 깊이 테스트와 비교 대상은 같지만, 셰이딩 전에 수행하므로 불필요한 셰이딩 비용을 줄입니다.
>
> **FPK** — 프래그먼트 셰이딩 **도중**에 수행됩니다. 새로 도착한 프래그먼트의 깊이를 **현재 셰이딩이 진행 중인 프래그먼트**의 깊이와 비교합니다. 아직 셰이딩이 끝나지 않아 깊이 버퍼에 기록되지 않은 프래그먼트, 즉 Early-Z가 비교할 수 없는 프래그먼트를 대상으로 합니다.
>
> 예를 들어, 프래그먼트 A(z=50)가 Early-Z를 통과하고 셰이딩을 시작합니다.
> A의 셰이딩이 끝나기 전에 같은 픽셀에 프래그먼트 B(z=10)가 도착하면, 깊이 버퍼에는 A의 값이 아직 기록되지 않은 상태라 B도 Early-Z를 통과합니다.
> 이때 FPK가 셰이딩 중인 A의 깊이와 B의 깊이를 비교하여, 더 먼 A의 셰이딩을 취소합니다.
>
> 반대로, A의 셰이딩이 **이미 완료**되어 깊이 버퍼에 z=50이 기록된 뒤에 프래그먼트 C(z=80)가 도착하면, A는 파이프라인에 없으므로 FPK가 비교할 대상이 없습니다.
> 이 경우 Early-Z가 깊이 버퍼의 50과 C의 80을 비교하여 C를 폐기합니다.
>
> 정리하면, 깊이 테스트는 셰이딩 이후에 정확성을 보장하고, Early-Z는 셰이딩 이전에 깊이 버퍼의 확정된 깊이로 불필요한 셰이딩을 방지하며, FPK는 셰이딩 도중에 아직 확정되지 않은 진행 중인 깊이까지 비교하여 낭비를 줄입니다.

### Adreno (Qualcomm)

Adreno GPU는 Qualcomm Snapdragon SoC에 탑재되며, Android 기기에서 높은 점유율을 가진 모바일 GPU입니다.
Adreno는 **FlexRender** 라 불리는 하이브리드 렌더링 방식을 지원하여, 삼각형이 적어서 Binning 오버헤드가 타일링 이점보다 크면 IMR 경로를, 삼각형이 많고 오버드로우가 발생하는 복잡한 장면에서는 타일 기반 경로를 사용합니다. 이 전환은 드라이버가 장면 특성을 분석하여 자동으로 판단합니다.

타일 기반 경로에서 Adreno는 **LRZ(Low Resolution Z-test)** 를 사용하여 불필요한 셰이딩을 줄입니다. LRZ는 Binning 단계에서 각 타일의 깊이 정보를 일반 깊이 버퍼보다 훨씬 낮은 해상도로 별도의 버퍼(LRZ 버퍼)에 기록한 뒤, 타일별 렌더링 단계에서 프래그먼트를 처리하기 전에 이 LRZ 버퍼와 비교합니다. 저해상도 깊이보다 확실히 먼 프래그먼트는 정밀한 깊이 테스트나 셰이딩 없이 바로 제거됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 410" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">LRZ 동작 원리</text>

  <!-- 1단계 섹션 -->
  <rect x="20" y="38" width="580" height="155" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="58" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">1단계: Binning — LRZ 버퍼 생성</text>
  <text x="310" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">각 타일의 깊이를 일반 깊이 버퍼보다 낮은 해상도로 별도 버퍼에 기록</text>

  <!-- 2x3 그리드 -->
  <rect x="130" y="90" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="115" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">z=10</text>

  <rect x="235" y="90" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="285" y="115" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">z=30</text>

  <rect x="340" y="90" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="115" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">z=5</text>

  <rect x="130" y="135" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="160" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">z=25</text>

  <rect x="235" y="135" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="285" y="160" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">z=15</text>

  <rect x="340" y="135" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="160" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">z=40</text>

  <!-- LRZ 버퍼 레이블 -->
  <line x1="445" y1="130" x2="470" y2="118" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="478" y="112" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">영역별 최소 깊이값</text>
  <text x="478" y="126" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold" opacity="0.6">(LRZ 버퍼)</text>

  <!-- 2단계 섹션 -->
  <rect x="20" y="210" width="580" height="185" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="232" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">2단계: 타일별 렌더링 — LRZ 버퍼로 조기 판정</text>
  <text x="310" y="250" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">예: LRZ 깊이값 = 10 인 영역</text>

  <!-- 프래그먼트 z=90 흐름 (가려짐) -->
  <rect x="36" y="266" width="116" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="94" y="285" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">프래그먼트 (z=90)</text>

  <line x1="156" y1="280" x2="186" y2="280" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="186,277 192,280 186,283" fill="currentColor"/>

  <rect x="196" y="266" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="246" y="285" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">10보다 멀다</text>

  <line x1="300" y1="280" x2="330" y2="280" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="330,277 336,280 330,283" fill="currentColor"/>

  <rect x="340" y="266" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="285" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">가려짐 확실</text>

  <line x1="444" y1="280" x2="474" y2="280" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="474,277 480,280 474,283" fill="currentColor"/>

  <rect x="484" y="266" width="104" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="522" y="283" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">래스터화 생략</text>
  <text x="574" y="285" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold" opacity="0.7">✗</text>

  <!-- 프래그먼트 z=5 흐름 (통과) -->
  <rect x="36" y="310" width="116" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="94" y="329" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">프래그먼트 (z=5)</text>

  <line x1="156" y1="324" x2="186" y2="324" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="186,321 192,324 186,327" fill="currentColor"/>

  <rect x="196" y="310" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="246" y="329" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">10보다 가깝다</text>

  <line x1="300" y1="324" x2="330" y2="324" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="330,321 336,324 330,327" fill="currentColor"/>

  <rect x="340" y="310" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="329" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">보일 가능성</text>

  <line x1="444" y1="324" x2="474" y2="324" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="474,321 480,324 474,327" fill="currentColor"/>

  <rect x="484" y="310" width="104" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="522" y="327" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">정밀 깊이 테스트</text>
  <text x="574" y="329" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold" opacity="0.7">✓</text>

  <!-- 하단 요약 -->
  <line x1="40" y1="370" x2="580" y2="370" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="310" y="392" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">확실히 가려지는 프래그먼트만 제거하고, 경계에 있는 프래그먼트는 보수적으로 통과</text>
</svg>
</div>

LRZ는 저해상도로 비교하므로 100% 정확하지는 않습니다. 확실히 가려지는 프래그먼트만 제거하고, 경계에 있는 프래그먼트는 보수적으로 통과시킵니다.

그럼에도 대부분의 장면에서 프래그먼트 셰이더에 도달하는 불필요한 프래그먼트를 크게 줄여줍니다. Mali와 마찬가지로, 불투명 오브젝트를 앞에서 뒤로 정렬하면 타일별 렌더링 단계에서 Early-Z가 뒤쪽 프래그먼트를 더 많이 거부할 수 있어 셰이딩 효율이 높아집니다.

### Apple GPU

Apple GPU는 Apple이 자체 설계한 GPU로, A-시리즈(iPhone) 및 M-시리즈(iPad, Mac) 칩에 탑재됩니다. 초기에는 Imagination Technologies의 **PowerVR** 타일 기반 기술을 라이센스하여 사용했으나, A11 Bionic(2017년) 이후부터 자체 설계 GPU 아키텍처로 전환했습니다.

Apple GPU의 **HSR(Hidden Surface Removal)** 은 타일 내의 모든 삼각형에 대해 래스터화와 깊이 테스트까지만 먼저 수행합니다.
각 삼각형을 래스터화하면서 프래그먼트의 깊이 값을 계산하고 깊이 버퍼와 비교하여, 픽셀마다 가장 가까운 프래그먼트를 갱신합니다. 모든 삼각형이 이 과정을 마치면 각 픽셀 위치에서 보이는 프래그먼트가 결정되고, 그 프래그먼트에 대해서만 셰이더를 실행합니다. TBDR의 "Deferred"는 이처럼 셰이딩을 래스터화와 깊이 테스트 이후로 미루는 것을 뜻합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">Apple GPU의 HSR 동작 흐름</text>

  <!-- 상단: 삼각형 정보 -->
  <rect x="20" y="38" width="580" height="42" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">타일 T6의 픽셀 P에 삼각형 3개가 겹침</text>
  <text x="310" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">삼각형 A (z=50)  ·  삼각형 B (z=10)  ·  삼각형 C (z=80)</text>

  <!-- 1단계 섹션 -->
  <rect x="20" y="96" width="580" height="200" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="118" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">1단계: 래스터화 — 모든 삼각형의 위치만 처리 (셰이딩 없음)</text>
  <text x="310" y="138" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">픽셀 P의 깊이 버퍼 변화</text>

  <!-- 삼각형 A: z=50 기록 -->
  <rect x="46" y="152" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="96" y="171" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">삼각형 A</text>

  <line x1="150" y1="166" x2="180" y2="166" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="180,163 186,166 180,169" fill="currentColor"/>

  <rect x="190" y="152" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="171" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">z=50 기록</text>

  <rect x="320" y="152" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="370" y="171" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">깊이 버퍼: 50</text>

  <!-- 삼각형 B: z=10 갱신 -->
  <rect x="46" y="194" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="96" y="213" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">삼각형 B</text>

  <line x1="150" y1="208" x2="180" y2="208" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="180,205 186,208 180,211" fill="currentColor"/>

  <rect x="190" y="194" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="213" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">z=10 갱신</text>

  <rect x="320" y="194" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="370" y="213" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">깊이 버퍼: 10</text>

  <text x="450" y="213" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(50보다 가까움)</text>

  <!-- 삼각형 C: z=80 무시 -->
  <rect x="46" y="236" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="96" y="255" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">삼각형 C</text>

  <line x1="150" y1="250" x2="180" y2="250" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="180,247 186,250 180,253" fill="currentColor"/>

  <rect x="190" y="236" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="240" y="255" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">z=80 무시</text>

  <rect x="320" y="236" width="100" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="370" y="255" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">깊이 버퍼: 10</text>

  <text x="450" y="255" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(10보다 멀음)</text>

  <!-- 2단계 섹션 -->
  <rect x="20" y="312" width="580" height="100" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="334" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">2단계: 셰이딩 — 최종적으로 보이는 프래그먼트만 실행</text>

  <!-- 삼각형 B만 셰이딩 -->
  <rect x="60" y="350" width="140" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="369" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">픽셀 P → 삼각형 B</text>

  <line x1="204" y1="364" x2="234" y2="364" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="234,361 240,364 234,367" fill="currentColor"/>

  <rect x="244" y="350" width="120" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="304" y="369" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">셰이딩 실행 (1회)</text>

  <!-- 삼각형 A, C는 셰이딩 없음 -->
  <rect x="400" y="350" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="490" y="369" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">삼각형 A, C → 셰이딩 없음</text>

  <!-- 하단 요약 -->
  <line x1="40" y1="430" x2="580" y2="430" stroke="currentColor" stroke-width="1" opacity="0.15"/>
  <text x="310" y="450" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">불투명 지오메트리에 한해, 가려진 프래그먼트의 셰이딩이 하드웨어 수준에서 완전히 제거됨</text>
</svg>
</div>

HSR은 모든 삼각형의 깊이를 먼저 비교한 뒤 보이는 것만 셰이딩하므로, 불투명 오브젝트의 정렬 순서가 성능에 미치는 영향이 크지 않습니다.

### 세 아키텍처 비교 요약

| 항목 | Mali | Adreno | Apple |
|---|---|---|---|
| 렌더링 방식 | TBR | TBR + IMR 혼합 (FlexRender) | TBDR |
| 타일 크기 | 16×16 | 가변 | 32×32 |
| 오버드로우 최적화 | FPK (셰이딩 중 취소) | LRZ (래스터화 전 제거) | HSR (보이는 것만 셰이딩) |
| 대표 SoC | Exynos, Dimensity | Snapdragon | A-시리즈, M-시리즈 |

세 아키텍처 모두 타일 기반이며, 차이는 타일 내에서 불필요한 작업을 어떻게 줄이느냐에 있습니다.
Mali는 이미 진행 중인 셰이딩을 취소(FPK)하고, Adreno는 저해상도 깊이로 조기에 걸러내며(LRZ), Apple은 보이는 것만 셰이딩을 시작(HSR)합니다.

다만 세 기술 모두 불투명 오브젝트에서만 동작합니다. 방식은 다르지만 모두 깊이 값을 비교하여 가려진 프래그먼트의 셰이딩을 생략하는 기술인데, 반투명 오브젝트는 겹치는 모든 레이어를 블렌딩해야 하므로 셰이딩을 생략할 수 없습니다.

---

## 오버드로우가 타일 기반 GPU에서 특히 비싼 이유

**오버드로우(Overdraw)** 는 화면의 같은 픽셀 위치에 여러 오브젝트가 겹치면서 셰이딩이 중복 실행되는 현상입니다.
한 픽셀에 배경, 건물, 캐릭터가 겹치면 해당 픽셀은 세 번 셰이딩되지만, 최종적으로 보이는 것은 가장 앞의 캐릭터뿐이므로 나머지 두 번은 낭비입니다.
앞에서 살펴본 FPK, LRZ, HSR은 모두 이 낭비를 줄이기 위한 기술입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <!-- Title -->
  <text x="340" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">오버드로우 예시 (한 픽셀 위치)</text>

  <!-- === Top section: Camera + 3 objects === -->

  <!-- Camera -->
  <rect x="30" y="46" width="80" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">카메라</text>

  <!-- Arrow from camera -->
  <line x1="110" y1="64" x2="155" y2="64" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="155,59 165,64 155,69" fill="currentColor"/>

  <!-- Object: 캐릭터 z=10 -->
  <rect x="175" y="46" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="63" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">캐릭터</text>
  <text x="225" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">z = 10</text>

  <!-- Object: 건물 z=50 -->
  <rect x="305" y="46" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="355" y="63" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">건물</text>
  <text x="355" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">z = 50</text>

  <!-- Object: 배경 z=100 -->
  <rect x="435" y="46" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="485" y="63" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">배경</text>
  <text x="485" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">z = 100</text>

  <!-- Depth axis label -->
  <text x="590" y="68" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">깊이 →</text>

  <!-- === Divider === -->
  <line x1="30" y1="100" x2="650" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text x="340" y="120" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">뒤에서 앞으로 그릴 경우</text>

  <!-- === Step 1: 배경 셰이딩 (낭비) === -->
  <rect x="50" y="138" width="420" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="66" y="159" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">1)</text>
  <text x="86" y="159" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">배경 셰이딩</text>
  <line x1="195" y1="155" x2="255" y2="155" stroke="currentColor" stroke-width="1"/>
  <polygon points="253,151 261,155 253,159" fill="currentColor"/>
  <text x="275" y="159" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">결과 기록</text>
  <rect x="490" y="143" width="60" height="22" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="520" y="158" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.7">낭비</text>

  <!-- === Step 2: 건물 셰이딩 (낭비) === -->
  <rect x="50" y="182" width="420" height="34" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="66" y="203" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">2)</text>
  <text x="86" y="203" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">건물 셰이딩</text>
  <line x1="195" y1="199" x2="255" y2="199" stroke="currentColor" stroke-width="1"/>
  <polygon points="253,195 261,199 253,203" fill="currentColor"/>
  <text x="275" y="203" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">덮어쓰기</text>
  <rect x="490" y="187" width="60" height="22" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="520" y="202" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.7">낭비</text>

  <!-- === Step 3: 캐릭터 셰이딩 (최종 결과) === -->
  <rect x="50" y="226" width="420" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="66" y="247" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">3)</text>
  <text x="86" y="247" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">캐릭터 셰이딩</text>
  <line x1="210" y1="243" x2="255" y2="243" stroke="currentColor" stroke-width="1"/>
  <polygon points="253,239 261,243 253,247" fill="currentColor"/>
  <text x="275" y="247" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">덮어쓰기</text>
  <rect x="490" y="231" width="90" height="22" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="535" y="246" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">최종 결과</text>

  <!-- === Bottom summary === -->
  <line x1="30" y1="278" x2="650" y2="278" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="210" y="290" width="260" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="311" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">오버드로우 = 3x</text>
  <text x="340" y="336" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">한 픽셀에 3번 셰이딩</text>
</svg>
</div>

<br>

모바일 GPU는 데스크톱에 비해 연산 자원이 훨씬 제한적입니다. **ALU(Arithmetic Logic Unit, 연산 유닛)** 수는 데스크톱의 수천~수만 개에 비해 약 1,000~2,000개 수준이고, **필레이트(Fill Rate)** — 초당 처리 가능한 프래그먼트 수 — 도 데스크톱의 수백억~수천억 픽셀/초에 비해 약 150억~500억 픽셀/초입니다.
타일 기반 렌더링이 절약하는 것은 외부 메모리 대역폭이며, 오버드로우로 인한 셰이더 중복 실행은 이 제한된 연산 예산을 그대로 소비합니다.

불투명 오브젝트는 FPK, LRZ, HSR이 오버드로우를 줄여 주지만, 반투명 오브젝트는 겹치는 모든 레이어를 블렌딩해야 하므로 이 최적화가 적용되지 않습니다. 겹치는 만큼 셰이딩이 그대로 실행됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <!-- Title -->
  <text x="360" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">같은 픽셀에 3개 오브젝트가 겹칠 때</text>

  <!-- =========== LEFT: 불투명 =========== -->

  <!-- Left panel background -->
  <rect x="15" y="42" width="335" height="310" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>

  <!-- Left title -->
  <text x="182" y="66" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">불투명 (앞에서 뒤 순서)</text>

  <!-- Row 1: 캐릭터(z=10) → 셰이딩 ✓  깊이 10 기록 -->
  <rect x="30" y="82" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="101" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">캐릭터 (z=10)</text>
  <line x1="150" y1="97" x2="182" y2="97" stroke="currentColor" stroke-width="1"/>
  <polygon points="180,93 188,97 180,101" fill="currentColor"/>
  <text x="196" y="95" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">셰이딩 ✓</text>
  <text x="196" y="108" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">깊이 10 기록</text>

  <!-- Row 2: 건물(z=50) → 폐기 ✗  10보다 멀다 -->
  <rect x="30" y="124" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="90" y="143" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">건물 (z=50)</text>
  <line x1="150" y1="139" x2="182" y2="139" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="180,135 188,139 180,143" fill="currentColor" opacity="0.4"/>
  <text x="196" y="137" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">폐기 ✗</text>
  <text x="196" y="150" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.4">10보다 멀다</text>

  <!-- Row 3: 배경(z=100) → 폐기 ✗  10보다 멀다 -->
  <rect x="30" y="166" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="90" y="185" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">배경 (z=100)</text>
  <line x1="150" y1="181" x2="182" y2="181" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="180,177 188,181 180,185" fill="currentColor" opacity="0.4"/>
  <text x="196" y="179" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">폐기 ✗</text>
  <text x="196" y="192" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.4">10보다 멀다</text>

  <!-- Left divider -->
  <line x1="30" y1="212" x2="335" y2="212" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Left result -->
  <rect x="80" y="224" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="180" y="244" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">셰이딩 1회</text>

  <!-- =========== RIGHT: 반투명 =========== -->

  <!-- Right panel background -->
  <rect x="370" y="42" width="335" height="310" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>

  <!-- Right title -->
  <text x="537" y="66" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">반투명 (뒤에서 앞 순서)</text>

  <!-- Row 1: 연기 A(z=50) → 셰이딩 + 블렌딩 -->
  <rect x="385" y="82" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="445" y="101" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">연기 A (z=50)</text>
  <line x1="505" y1="97" x2="537" y2="97" stroke="currentColor" stroke-width="1"/>
  <polygon points="535,93 543,97 535,101" fill="currentColor"/>
  <text x="551" y="101" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">셰이딩 + 블렌딩</text>

  <!-- Row 2: 연기 B(z=40) → 셰이딩 + 블렌딩 -->
  <rect x="385" y="124" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="445" y="143" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">연기 B (z=40)</text>
  <line x1="505" y1="139" x2="537" y2="139" stroke="currentColor" stroke-width="1"/>
  <polygon points="535,135 543,139 535,143" fill="currentColor"/>
  <text x="551" y="143" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">셰이딩 + 블렌딩</text>

  <!-- Row 3: 연기 C(z=30) → 셰이딩 + 블렌딩 -->
  <rect x="385" y="166" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="445" y="185" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">연기 C (z=30)</text>
  <line x1="505" y1="181" x2="537" y2="181" stroke="currentColor" stroke-width="1"/>
  <polygon points="535,177 543,181 535,185" fill="currentColor"/>
  <text x="551" y="185" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10">셰이딩 + 블렌딩</text>

  <!-- Right divider -->
  <line x1="385" y1="212" x2="690" y2="212" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Right result -->
  <rect x="435" y="224" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="535" y="244" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">셰이딩 3회</text>
  <text x="537" y="272" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">깊이 판별 불가</text>
</svg>
</div>

<br>

모바일 게임에서 반투명 오버드로우가 빈번한 대표적인 요소로는 파티클 시스템, UI, 반투명 머티리얼이 있습니다.
파티클 시스템은 연기, 불꽃, 폭발 등을 표현할 때 반투명 **빌보드(Billboard, 항상 카메라를 향하는 사각형)** 를 수십~수백 장 겹치며, 각 파티클이 화면의 넓은 영역을 덮을수록 오버드로우가 급격히 늘어납니다.
UI도 배경 패널, 그림자, 테두리, 아이콘, 텍스트 등 여러 반투명 레이어가 겹쳐 화면의 넓은 영역을 차지하고, 유리·물·홀로그램 같은 반투명 머티리얼이 서로 겹치는 경우도 마찬가지입니다.

> Unity 에디터의 Scene View에서 **Overdraw 시각화 모드**(상단 드롭다운)를 활성화하면 오버드로우가 발생하는 영역을 색상 강도로 확인할 수 있습니다.

### 오버드로우와 셰이더 복잡도

오버드로우 배수는 곧 프래그먼트 셰이더 실행 배수이므로, 셰이더가 복잡할수록 오버드로우의 비용이 커집니다.
Unlit 셰이더처럼 텍스처 하나만 읽는 경우에는 계산이 가벼워서 오버드로우 2~3x도 견딜 수 있지만, 노멀 맵, 스페큘러, 조명 계산이 포함된 셰이더는 텍스처를 여러 장 읽고 수학 연산을 수십 번 수행합니다. 오버드로우 3x면 이 비싼 셰이더가 3번 반복 실행되므로, 프레임 레이트가 급격히 떨어집니다.

---

## 타일 기반 렌더링에서 주의해야 할 추가 사항

앞에서 타일 기반 렌더링이 대역폭을 절약하는 원리와, FPK/LRZ/HSR이 오버드로우를 줄이는 방식을 살펴봤습니다. 하지만 타일 기반 렌더링에는 데스크톱 IMR에서는 신경 쓰지 않아도 되는 추가 고려 사항이 있습니다.

### 타일 메모리와 Load/Store

렌더링 전에 외부 메모리의 이전 내용을 온칩 타일 메모리로 불러오는 과정을 **Load**, 렌더링이 끝난 뒤 결과를 외부 메모리에 기록하는 과정을 **Store** 또는 **Resolve** 라 합니다.

이 Load/Store가 타일마다 발생하므로, 불필요한 Load나 Store가 늘어나면 타일 기반 렌더링의 대역폭 이점이 상쇄됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 전체 외곽 -->
  <rect x="10" y="10" width="500" height="400" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="36" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">타일 하나의 렌더링 사이클</text>

  <!-- 1. Load 박스 -->
  <rect x="60" y="56" width="400" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="78" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1. Load</text>
  <text x="80" y="96" font-family="sans-serif" font-size="11" fill="currentColor">외부 메모리 → 온칩 타일 메모리</text>
  <text x="80" y="114" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(이전 내용이 필요하면 로드, Clear면 생략)</text>

  <!-- 화살표: Load → Render -->
  <line x1="260" y1="124" x2="260" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="256,148 260,156 264,148" fill="currentColor"/>

  <!-- 2. Render 박스 -->
  <rect x="60" y="160" width="400" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="182" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2. Render</text>
  <text x="80" y="200" font-family="sans-serif" font-size="11" fill="currentColor">래스터화 → 프래그먼트 셰이더 → 테스트/블렌딩</text>
  <text x="80" y="218" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(읽고 쓰는 데이터가 온칩 타일 메모리에 있음)</text>

  <!-- 화살표: Render → Store -->
  <line x1="260" y1="228" x2="260" y2="252" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="256,252 260,260 264,252" fill="currentColor"/>

  <!-- 3. Store 박스 -->
  <rect x="60" y="264" width="400" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="286" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3. Store</text>
  <text x="80" y="304" font-family="sans-serif" font-size="11" fill="currentColor">온칩 타일 메모리 → 외부 메모리</text>
  <text x="80" y="322" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">(최종 색상 저장, 깊이/스텐실은 선택적)</text>

  <!-- 구분선 -->
  <line x1="40" y1="350" x2="480" y2="350" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- 하단 주석 -->
  <text x="260" y="374" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Load 생략 = 대역폭 절약</text>
  <text x="260" y="394" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">깊이/스텐실 Store 생략 = 대역폭 절약</text>
</svg>
</div>

Load는 이전 프레임의 내용이 필요할 때만 발생합니다.
Unity에서 카메라의 Clear Flags를 "Solid Color"나 "Skybox"로 설정하면 화면 전체를 새로 그리므로, GPU는 이전 내용을 Load하지 않고 타일 메모리를 직접 초기화합니다.

반면 "Don't Clear"로 설정하면 이전 프레임의 내용을 유지해야 하므로, GPU는 렌더링 전에 외부 메모리에서 이전 내용을 Load해야 하고 그만큼 대역폭을 소비합니다.

### 렌더 타깃 전환 비용

GPU가 렌더링 결과를 기록하는 대상을 **렌더 타깃(Render Target)** 이라 합니다. 기본 렌더 타깃은 화면에 표시되는 프레임 버퍼이지만, 포스트 프로세싱처럼 중간 결과가 필요하면 별도의 **렌더 텍스처(Render Texture)** 에 렌더링하기도 합니다.

GPU는 같은 대상을 동시에 읽고 쓸 수 없으므로, 렌더 텍스처에 그린 장면을 읽어서 후처리한 결과는 다른 렌더 텍스처나 프레임 버퍼에 기록해야 합니다.
이처럼 한 프레임을 렌더링하는 도중에 출력 대상을 바꾸는 것이 렌더 타깃 전환이며, 중간 결과가 필요한 한 피할 수 없습니다.

<br>

데스크톱 IMR은 렌더링 데이터가 항상 외부 메모리(VRAM)에 있어 렌더 타깃을 전환해도 쓰기 대상만 바꾸면 됩니다.
반면 타일 기반 렌더링에서는 데이터가 온칩 타일 메모리에 있으므로, 전환할 때마다 현재 내용을 Store하고 새 렌더 타깃을 Load해야 하며, 전환이 잦을수록 대역폭 소비가 늘어납니다.

예를 들어 블룸은 밝은 부분 추출 → 블러(수평·수직 별도 패스) → 원본 합성 과정에서 단계마다 쓰기 대상이 바뀌어 최소 4번의 전환이 발생하고, 피사계 심도(Depth of Field)나 모션 블러(Motion Blur)처럼 별도 패스가 필요한 효과를 추가하면 그만큼 전환 횟수도 늘어납니다.
모바일에서 포스트 프로세싱 패스가 많을수록 Load/Store 대역폭 비용이 커지는 이유입니다.

### Alpha Test와 타일 기반 GPU

텍스처의 알파 값을 기준값과 비교하여 기준 이하인 프래그먼트를 폐기하는 기법을 **알파 테스트(Alpha Test)** 라 부릅니다.
현대 셰이더에서는 `discard`(GLSL) 또는 `clip`(HLSL) 명령어로 구현합니다.

나뭇잎이나 철조망처럼 윤곽이 복잡한 형태는 폴리곤으로 정밀하게 모델링하면 삼각형 수가 많아지므로, 단순한 사각형 폴리곤에 알파 채널이 포함된 텍스처를 입힌 뒤 알파 값이 낮은 부분을 폐기하여 형태를 표현합니다.

<br>

타일 기반 GPU에서 알파 테스트는 특별한 문제를 일으킵니다. 앞에서 살펴본 것처럼 깊이 값은 래스터화 단계에서 확정되며, LRZ, HSR, FPK는 이를 활용하여 셰이딩 전이나 도중에 불필요한 프래그먼트를 걸러냅니다.

그런데 `discard`가 실행되면 해당 프래그먼트의 색상뿐 아니라 깊이도 기록되지 않습니다. 깊이 자체는 래스터화 시점에 알고 있지만, 셰이더가 프래그먼트를 폐기할 수 있으므로 그 깊이가 최종적으로 유효한지는 셰이더 실행이 끝나야 결정됩니다.

Early-Z와 LRZ, HSR은 이 프래그먼트의 깊이를 깊이 버퍼에 미리 반영할 수 없고, FPK는 셰이딩 중인 `discard` 프래그먼트의 깊이를 기준으로 다른 프래그먼트를 취소할 수 없습니다. `discard`된 프래그먼트 뒤의 프래그먼트를 취소하면, 해당 픽셀에 유효한 프래그먼트가 없어지기 때문입니다.

따라서 `discard`가 포함된 셰이더에서는 해당 드로우 콜에 대해 깊이 기반 최적화가 비활성화되거나 효과가 크게 줄어듭니다.


<br>

`discard`는 렌더링 결과의 정확성을 위해 반드시 실행되어야 하는 셰이더 로직입니다. 나뭇잎 텍스처의 투명한 부분을 폐기하지 않으면 사각형 폴리곤이 그대로 보이기 때문입니다. 반면 깊이 기반 최적화는 성능을 높이기 위한 것이므로, 비활성화해도 렌더링 결과는 동일합니다. GPU는 정확한 이미지를 먼저 보장해야 하므로, `discard`가 포함된 셰이더를 반드시 실행하는 대신 해당 드로우 콜에 대해 깊이 기반 최적화를 비활성화하거나 효과를 크게 줄입니다.

따라서 모바일에서는 가능하면 `discard` 대신 **알파 블렌딩(Alpha Blending)** 을 사용하는 편이 유리합니다. 알파 블렌딩은 프래그먼트를 폐기하지 않고 알파 값에 따라 기존 색상과 혼합하는 방식으로, 반투명 오브젝트로 처리되어 오버드로우 비용은 발생하지만 `discard`를 사용하지 않으므로 다른 불투명 오브젝트의 깊이 기반 최적화에 영향을 주지 않습니다.

깊이 기반 최적화는 드로우 콜 단위로 적용되므로, `discard`를 사용하지 않는 불투명 오브젝트들은 FPK, LRZ, HSR의 이점을 그대로 유지합니다. 알파 테스트가 반드시 필요한 경우에는 해당 오브젝트의 수를 최소화하는 것이 좋습니다.

### 삼각형 수와 Binning 부하

데스크톱 IMR에서는 각 삼각형이 버텍스 셰이딩을 마치면 곧바로 프래그먼트 셰이딩으로 넘어갑니다. 여러 삼각형이 파이프라인의 서로 다른 단계에 동시에 있으므로, 한 삼각형의 프래그먼트 처리와 다른 삼각형의 버텍스 처리가 동시에 진행될 수 있습니다.

반면 타일 기반 렌더링에서는 모든 삼각형에 대해 버텍스 셰이더를 실행하고 각 삼각형이 어느 타일에 속하는지 분류하는 Binning 단계를 먼저 거쳐야 타일별 렌더링이 시작됩니다. 삼각형 수가 많으면 Binning 단계가 길어지고, 그동안 프래그먼트 처리는 시작할 수 없습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 전체 외곽 -->
  <rect x="10" y="10" width="540" height="360" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="36" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">타일 기반 렌더링에서 삼각형 수에 따른 부하 분포</text>

  <!-- 시나리오 1: 삼각형이 적은 장면 -->
  <text x="40" y="68" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">삼각형이 적은 장면</text>

  <!-- Binning 바 (짧음) -->
  <text x="40" y="94" font-family="sans-serif" font-size="10" fill="currentColor">Binning</text>
  <rect x="150" y="82" width="70" height="18" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>

  <!-- 프래그먼트 처리 바 (길고 강조) -->
  <text x="40" y="122" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 처리</text>
  <rect x="150" y="110" width="320" height="18" rx="3" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.5"/>

  <!-- 병목 표시 -->
  <text x="480" y="122" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">← 병목</text>

  <!-- 결론 -->
  <text x="150" y="148" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 프래그먼트 셰이딩이 병목</text>

  <!-- 구분선 -->
  <line x1="30" y1="166" x2="530" y2="166" stroke="currentColor" stroke-width="1" opacity="0.2"/>

  <!-- 시나리오 2: 삼각형이 많은 장면 -->
  <text x="40" y="194" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">삼각형이 많은 장면</text>

  <!-- Binning 바 (길고 강조) -->
  <text x="40" y="220" font-family="sans-serif" font-size="10" fill="currentColor">Binning</text>
  <rect x="150" y="208" width="280" height="18" rx="3" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1.5"/>

  <!-- 병목 표시 -->
  <text x="440" y="220" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">← 병목</text>

  <!-- 프래그먼트 처리 바 (짧음) -->
  <text x="40" y="248" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트 처리</text>
  <rect x="150" y="236" width="120" height="18" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>

  <!-- 결론 -->
  <text x="150" y="274" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ Binning(버텍스 셰이딩)이 병목</text>

  <!-- 하단 구분선 -->
  <line x1="30" y1="296" x2="530" y2="296" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- 하단 주석 -->
  <text x="280" y="324" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">삼각형 수 → Binning 시간</text>
  <text x="280" y="344" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">셰이더 복잡도 → 프래그먼트 처리 시간</text>
</svg>
</div>

Binning과 프래그먼트 처리 중 어느 쪽이 병목인지는 Arm Mobile Studio(Mali), Snapdragon Profiler(Adreno), Xcode GPU Profiler(Apple) 등 벤더별 GPU 프로파일링 도구에서 두 단계의 시간을 분리하여 확인할 수 있습니다.

모바일에서 Binning 병목을 줄이려면 LOD(Level of Detail)로 먼 오브젝트의 삼각형 수를 줄이거나, 카메라에 보이지 않는 오브젝트를 컬링하여 GPU에 제출되는 총 삼각형 수를 관리해야 합니다.

---

## 마무리

이 글에서는 모바일 GPU가 제한된 대역폭 안에서 렌더링 효율을 높이는 방법과, 타일 기반 아키텍처에서 추가로 고려해야 할 사항을 살펴보았습니다.

- 모바일 GPU는 CPU와 시스템 메모리(LPDDR)를 공유하며, 메모리 대역폭이 25~50 GB/s로 데스크톱의 약 1/10 수준입니다.
- 타일 기반 렌더링(TBR/TBDR)은 화면을 타일로 분할하여 온칩 타일 메모리에서 래스터화, 깊이 테스트, 블렌딩, MSAA를 처리하고, 최종 색상만 외부 메모리에 기록합니다.
- Mali(FPK), Adreno(LRZ), Apple(HSR)은 각각 다른 방식으로 가려진 프래그먼트의 셰이딩을 줄이지만, 깊이 정보를 기반으로 동작하므로 불투명 오브젝트에서 효과적입니다.
- 반투명 오브젝트는 겹치는 모든 레이어를 블렌딩해야 하므로 이 최적화의 도움을 받지 못하고, 오버드로우가 프래그먼트 처리 비용을 직접 증가시킵니다.
- 렌더 타깃 전환의 Load/Store 비용, `discard`에 의한 깊이 기반 최적화 비활성화, Binning 단계의 삼각형 수 비례 비용은 타일 기반 렌더링 고유의 고려 사항입니다.

모바일 GPU 아키텍처의 핵심은 제한된 대역폭과 연산 자원 안에서 효율을 극대화하는 것입니다. 타일 기반 렌더링과 온칩 타일 메모리는 외부 메모리 접근을 줄이고, FPK·LRZ·HSR은 가려진 프래그먼트의 불필요한 셰이딩을 제거합니다.

<br>

---

**관련 글**
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- **GPU 아키텍처 (2) - 모바일 GPU와 TBDR** (현재 글)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- **GPU 아키텍처 (2) - 모바일 GPU와 TBDR** (현재 글)
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
