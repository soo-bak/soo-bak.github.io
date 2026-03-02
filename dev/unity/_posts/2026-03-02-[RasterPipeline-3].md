---
layout: single
title: "래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱 - soo:bak"
date: "2026-03-02 16:09:00 +0900"
description: 디스플레이 스캔아웃, 티어링, VSync, 더블/트리플 버퍼링, 앨리어싱, MSAA/FXAA/TAA를 설명합니다.
tags:
  - Unity
  - 그래픽스
  - VSync
  - 안티앨리어싱
  - 모바일
---

## 버퍼에서 화면으로

[래스터화 파이프라인 (2)](/dev/unity/RasterPipeline-2/)에서 프래그먼트가 깊이 테스트, 스텐실 테스트, 블렌딩을 거쳐 프레임 버퍼에 기록되는 과정을 다루었습니다. 모든 드로우 콜이 처리되면 프레임 버퍼에는 한 프레임의 완성된 이미지가 담깁니다.

<br>

하지만 프레임 버퍼에 완성된 이미지가 담겼다고 해서, 그 이미지가 곧바로 화면에 나타나는 것은 아닙니다.

디스플레이는 프레임 버퍼를 한 번에 표시하지 않고 순차적으로 읽어가므로, GPU가 프레임을 완성하는 속도와 디스플레이가 화면을 갱신하는 속도가 어긋나면 화면 한 장에 두 프레임이 섞여 보이는 **티어링(Tearing)**이 발생합니다. **더블 버퍼링**, **VSync**, **트리플 버퍼링**은 이 동기화 문제를 단계적으로 해결하기 위한 메커니즘이며, 각각 고유한 트레이드오프를 갖고 있습니다.

<br>

래스터화 과정 자체에도 근본적인 한계가 있습니다.

연속적인 삼각형 가장자리를 유한한 픽셀 격자로 표현하면, 가장자리에 계단 모양의 **앨리어싱(Aliasing)**이 나타납니다. 이 계단 현상은 해상도를 높이면 줄어들지만 완전히 사라지지 않습니다. 나이퀴스트 정리가 설명하듯, 이산적 샘플링으로는 무한히 높은 공간 주파수를 완벽히 재현할 수 없기 때문입니다. 이를 완화하는 **안티앨리어싱(Anti-Aliasing)** 기법에는 MSAA, FXAA, TAA, SMAA 등이 있으며, 접근 방식과 비용이 각기 다릅니다. 특히 모바일에서는 TBDR 아키텍처의 특성에 따라 기법별 비용 구조가 데스크톱과 달라집니다.

<br>

이 글에서는 완성된 프레임이 화면에 도달하기까지의 동기화 문제와, 래스터화의 샘플링 한계를 보완하는 안티앨리어싱 기법을 살펴봅니다.

---

## 디스플레이 스캔아웃

디스플레이 장치(모니터, 스마트폰 화면)는 프레임 버퍼의 데이터를 한 번에 표시하지 않습니다.

프레임 버퍼의 픽셀을 **왼쪽 위부터 오른쪽으로, 위에서 아래로** 순차적으로 읽어 디스플레이의 각 픽셀에 전송합니다. 이 과정을 **스캔아웃(Scanout)**이라 합니다.

<br>

이 순서는 CRT(브라운관) 모니터의 전자빔 주사 방식에서 비롯되었습니다. CRT에서는 전자빔이 화면을 왼쪽에서 오른쪽으로, 위에서 아래로 훑으며 형광체를 발광시켰습니다.

현대의 LCD, OLED 디스플레이는 전자빔을 사용하지 않지만, 디스플레이 컨트롤러가 프레임 버퍼를 읽는 순서는 동일한 관례를 따릅니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="680" height="310" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="340" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">스캔아웃 과정</text>
  <!-- frame buffer box -->
  <rect x="30" y="50" width="240" height="180" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">프레임 버퍼</text>
  <!-- scan line arrows in frame buffer -->
  <line x1="50" y1="90" x2="240" y2="90" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3"/>
  <polygon points="244,90 236,86 236,94" fill="currentColor"/>
  <line x1="50" y1="110" x2="240" y2="110" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3"/>
  <polygon points="244,110 236,106 236,114" fill="currentColor"/>
  <line x1="50" y1="130" x2="240" y2="130" stroke="currentColor" stroke-width="1" stroke-dasharray="6,3"/>
  <polygon points="244,130 236,126 236,134" fill="currentColor"/>
  <!-- scan position indicator -->
  <line x1="50" y1="148" x2="250" y2="148" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2" opacity="0.4"/>
  <!-- unread area -->
  <text x="150" y="180" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(아직 읽지 않음)</text>
  <!-- transfer arrow -->
  <line x1="290" y1="130" x2="390" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="396,130 386,125 386,135" fill="currentColor"/>
  <text x="343" y="120" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">데이터 전송</text>
  <!-- display box -->
  <rect x="410" y="50" width="240" height="180" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="530" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">디스플레이</text>
  <!-- filled scan lines (already displayed) -->
  <rect x="425" y="82" width="210" height="14" rx="2" fill="currentColor" fill-opacity="0.25"/>
  <text x="648" y="93" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">1</text>
  <rect x="425" y="102" width="210" height="14" rx="2" fill="currentColor" fill-opacity="0.25"/>
  <text x="648" y="113" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">2</text>
  <rect x="425" y="122" width="210" height="14" rx="2" fill="currentColor" fill-opacity="0.25"/>
  <text x="648" y="133" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">3</text>
  <!-- scan position on display -->
  <line x1="425" y1="148" x2="635" y2="148" stroke="currentColor" stroke-width="0.5" stroke-dasharray="2,2" opacity="0.4"/>
  <!-- unfilled area on display -->
  <text x="530" y="180" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(아직 갱신 안 됨)</text>
  <!-- scan direction indicator (top-left corner) -->
  <text x="44" y="88" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">→</text>
  <!-- bottom labels -->
  <text x="340" y="258" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">왼쪽 위부터 오른쪽으로, 위에서 아래로 순차 전송</text>
  <text x="340" y="278" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">60Hz 디스플레이: 초당 60번 전체 화면 갱신</text>
  <text x="340" y="298" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">1회 갱신 주기 ≈ 16.67ms (활성 스캔아웃 + VBlank 포함)</text>
</svg>
</div>

<br>

60Hz 디스플레이는 초당 60번 화면을 갱신하며, 한 번의 갱신 주기는 약 16.67ms(1/60초)입니다.

이 주기는 두 구간으로 나뉩니다. 실제로 픽셀 데이터를 전송하는 **활성 스캔아웃** 구간과, 한 프레임의 스캔이 끝난 뒤 다음 프레임이 시작되기 전까지의 짧은 유휴 구간인 **수직 귀선 구간(VBlank, Vertical Blanking Interval)**입니다.

CRT에서 전자빔이 화면 하단에서 상단으로 되돌아가는 시간이 VBlank의 기원이며, 현대 디스플레이에서도 프레임 전환 구간으로 유지됩니다. 이 VBlank 구간이 이후 다룰 VSync와 버퍼 교환의 타이밍 기준점이 됩니다.

---

## 티어링

스캔아웃이 프레임 버퍼를 순차적으로 읽는 도중에 버퍼 내용이 바뀌면, 화면 위쪽에는 이전 프레임, 아래쪽에는 새 프레임이 섞여 나타납니다.

이 현상이 **티어링(Tearing)**입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="520" height="370" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="260" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">티어링 발생 원리</text>
  <text x="260" y="46" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">디스플레이 스캔아웃 진행 중 (프레임 N을 읽는 중)</text>
  <!-- display frame outline -->
  <rect x="130" y="60" width="260" height="210" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- Frame N region (top) — lighter fill -->
  <rect x="131" y="61" width="258" height="95" fill="currentColor" fill-opacity="0.12"/>
  <!-- Frame N scan lines -->
  <rect x="145" y="72" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <rect x="145" y="90" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <rect x="145" y="108" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <rect x="145" y="126" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <!-- Frame N label -->
  <text x="260" y="150" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">프레임 N (스캔 완료)</text>
  <!-- Tearing boundary — zigzag line -->
  <polyline points="130,166 155,160 180,172 205,160 230,172 255,160 280,172 305,160 330,172 355,160 380,172 390,166" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <!-- Tearing label -->
  <text x="440" y="170" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">← 티어링 경계</text>
  <!-- Frame N+1 region (bottom) — darker fill -->
  <rect x="131" y="175" width="258" height="94" fill="currentColor" fill-opacity="0.25"/>
  <!-- Frame N+1 scan lines -->
  <rect x="145" y="186" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.35"/>
  <rect x="145" y="204" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.35"/>
  <rect x="145" y="222" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.35"/>
  <rect x="145" y="240" width="230" height="10" rx="2" fill="currentColor" fill-opacity="0.35"/>
  <!-- Frame N+1 label -->
  <text x="260" y="262" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">프레임 N+1 (교체됨)</text>
  <!-- Annotation: GPU replaced buffer -->
  <line x1="100" y1="220" x2="130" y2="220" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="95" y="224" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">GPU가 버퍼 교체</text>
  <!-- Annotation: already sent to display -->
  <line x1="100" y1="100" x2="130" y2="100" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="95" y="104" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">이미 전송됨</text>
  <!-- Bottom explanation -->
  <text x="260" y="298" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">디스플레이가 프레임 N을 읽는 도중</text>
  <text x="260" y="316" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">GPU가 프레임 버퍼를 프레임 N+1로 교체</text>
  <text x="260" y="340" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">→ 스캔 위치를 기준으로 위/아래가 다른 프레임</text>
  <text x="260" y="360" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">카메라 이동이 빠를수록 프레임 간 차이가 커서 경계가 눈에 띔</text>
</svg>
</div>

<br>

GPU의 렌더링 완료 시점과 디스플레이의 갱신 주기는 서로 독립적이므로, GPU가 스캔아웃 도중에 프레임 버퍼를 교체하면 스캔 진행 지점을 경계로 위아래에 서로 다른 프레임이 나타납니다.

카메라가 빠르게 회전하거나 장면이 빠르게 이동하면 프레임 간 차이가 커서 경계선이 눈에 띄지만, 정적인 장면에서는 차이가 작아 인지하기 어렵습니다.

---

## 더블 버퍼링

티어링을 방지하는 기본적인 방법이 **더블 버퍼링(Double Buffering)**입니다.

프레임 버퍼를 하나만 사용하는 대신, 두 개의 버퍼를 사용합니다.

버퍼가 두 개이므로 프레임 버퍼 메모리도 2배가 필요합니다.

[래스터화 파이프라인 (2)](/dev/unity/RasterPipeline-2/)에서 다룬 RGBA8 FHD 기준으로 한 장 약 8MB에서 두 장 약 16MB로 늘어나지만, 현대 GPU 메모리 용량에서 이 비용은 무시할 수 있는 수준입니다.

<br>

**프론트 버퍼(Front Buffer)**는 디스플레이가 현재 읽고 있는 버퍼로, 화면에 표시 중인 프레임을 담고 있습니다.

**백 버퍼(Back Buffer)**는 GPU가 새 프레임을 렌더링하는 버퍼로, 렌더링이 완료될 때까지 디스플레이에 노출되지 않습니다.

<br>

GPU는 백 버퍼에 새 프레임을 렌더링합니다.

렌더링이 완료되면 프론트 버퍼와 백 버퍼의 역할을 **교환(Swap)**합니다.

이 교환은 실제 픽셀 데이터를 복사하는 것이 아니라, 디스플레이 컨트롤러가 읽는 버퍼의 포인터만 바꾸는 연산이므로 거의 즉시 완료됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="700" height="330" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="350" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">더블 버퍼링 동작</text>
  <!-- time arrow -->
  <line x1="50" y1="52" x2="640" y2="52" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="646,52 636,47 636,57" fill="currentColor"/>
  <text x="660" y="56" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="11">시간</text>
  <!-- Column headers -->
  <text x="120" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">프레임 1</text>
  <text x="275" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">교환 (Swap)</text>
  <text x="430" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">프레임 2</text>
  <text x="585" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">교환 (Swap)</text>
  <!-- Swap arrows between columns -->
  <text x="197" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13">→</text>
  <text x="352" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13">→</text>
  <text x="507" y="78" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13">→</text>
  <!-- Column 1: Frame 1 -->
  <rect x="40" y="90" width="160" height="100" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- Front buffer A -->
  <rect x="52" y="100" width="136" height="35" rx="3" fill="currentColor" fill-opacity="0.2"/>
  <text x="120" y="115" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">프론트: A</text>
  <text x="120" y="129" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">화면 표시</text>
  <!-- Back buffer B -->
  <rect x="52" y="144" width="136" height="35" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <text x="120" y="159" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">백: B</text>
  <text x="120" y="173" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">렌더링 중</text>
  <!-- Column 2: Swap -->
  <rect x="215" y="90" width="120" height="100" rx="4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <!-- Swap arrows -->
  <path d="M 255,118 C 255,135 295,135 295,152" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="295,156 291,148 299,148" fill="currentColor"/>
  <path d="M 295,118 C 295,135 255,135 255,152" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="255,156 251,148 259,148" fill="currentColor"/>
  <text x="275" y="110" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">포인터 교환</text>
  <!-- Column 3: Frame 2 -->
  <rect x="350" y="90" width="160" height="100" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- Front buffer B (swapped) -->
  <rect x="362" y="100" width="136" height="35" rx="3" fill="currentColor" fill-opacity="0.2"/>
  <text x="430" y="115" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">프론트: B</text>
  <text x="430" y="129" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">화면 표시</text>
  <!-- Back buffer A (swapped) -->
  <rect x="362" y="144" width="136" height="35" rx="3" fill="currentColor" fill-opacity="0.1"/>
  <text x="430" y="159" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">백: A</text>
  <text x="430" y="173" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">렌더링 중</text>
  <!-- Column 4: Swap -->
  <rect x="525" y="90" width="120" height="100" rx="4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <!-- Swap arrows -->
  <path d="M 565,118 C 565,135 605,135 605,152" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="605,156 601,148 609,148" fill="currentColor"/>
  <path d="M 605,118 C 605,135 565,135 565,152" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="565,156 561,148 569,148" fill="currentColor"/>
  <text x="585" y="110" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">포인터 교환</text>
  <!-- Buffer role labels on left side -->
  <text x="32" y="120" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">표시</text>
  <text x="32" y="164" text-anchor="end" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">렌더</text>
  <!-- Divider -->
  <line x1="40" y1="210" x2="660" y2="210" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Bottom conclusions -->
  <text x="350" y="236" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">디스플레이는 항상 완성된 프레임(프론트 버퍼)을 읽음</text>
  <text x="350" y="258" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">GPU는 디스플레이에 노출되지 않는 백 버퍼에 렌더링</text>
  <text x="350" y="280" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">→ 렌더링 중인 미완성 프레임이 화면에 노출되지 않음</text>
  <text x="350" y="310" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">교환은 실제 픽셀 복사가 아닌 포인터만 변경 → 거의 즉시 완료</text>
</svg>
</div>

<br>

더블 버퍼링만으로는 티어링이 완전히 방지되지 않습니다.

버퍼 교환 시점이 디스플레이의 스캔아웃과 동기화되지 않으면, 스캔아웃 도중에 포인터가 바뀌어 여전히 티어링이 발생할 수 있습니다.

VSync가 이 교환 시점을 동기화합니다.

---

## VSync

**VSync(Vertical Synchronization, 수직 동기화)**는 버퍼 교환 시점을 디스플레이의 **VBlank** 구간에 맞추는 메커니즘입니다.

스캔아웃이 진행되는 동안에는 교환을 보류하고, 스캔이 끝난 뒤의 유휴 구간에서만 교환을 수행하여 티어링을 방지합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="700" height="280" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="350" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">VSync의 동작</text>
  <text x="350" y="46" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">VBlank 구간에서만 버퍼 교환 허용</text>
  <!-- time arrow -->
  <line x1="30" y1="68" x2="660" y2="68" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="666,68 656,63 656,73" fill="currentColor"/>
  <text x="680" y="72" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9">시간</text>
  <!-- Scanout region 1: Frame N -->
  <rect x="50" y="82" width="220" height="80" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="106" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">스캔아웃</text>
  <text x="160" y="122" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">(프레임 N 표시)</text>
  <text x="160" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">프론트: A (표시 중)</text>
  <!-- VBlank 1 -->
  <rect x="270" y="82" width="50" height="80" rx="4" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>
  <text x="295" y="108" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">VBlank</text>
  <text x="295" y="128" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">swap</text>
  <!-- swap icon arrows -->
  <line x1="283" y1="140" x2="283" y2="152" stroke="currentColor" stroke-width="1"/>
  <polygon points="283,156 279,150 287,150" fill="currentColor"/>
  <line x1="307" y1="156" x2="307" y2="144" stroke="currentColor" stroke-width="1"/>
  <polygon points="307,140 303,146 311,146" fill="currentColor"/>
  <!-- Scanout region 2: Frame N+1 -->
  <rect x="320" y="82" width="220" height="80" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="430" y="106" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">스캔아웃</text>
  <text x="430" y="122" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">(프레임 N+1 표시)</text>
  <text x="430" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">프론트: B (표시 중)</text>
  <!-- VBlank 2 -->
  <rect x="540" y="82" width="50" height="80" rx="4" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>
  <text x="565" y="108" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">VBlank</text>
  <text x="565" y="128" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">swap</text>
  <!-- swap icon arrows -->
  <line x1="553" y1="140" x2="553" y2="152" stroke="currentColor" stroke-width="1"/>
  <polygon points="553,156 549,150 557,150" fill="currentColor"/>
  <line x1="577" y1="156" x2="577" y2="144" stroke="currentColor" stroke-width="1"/>
  <polygon points="577,140 573,146 581,146" fill="currentColor"/>
  <!-- continuation dots -->
  <text x="610" y="126" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="14" opacity="0.4">...</text>
  <!-- lock icons / prohibited markers during scanout -->
  <line x1="155" y1="164" x2="165" y2="174" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="165" y1="164" x2="155" y2="174" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <text x="160" y="190" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">교환 금지</text>
  <line x1="425" y1="164" x2="435" y2="174" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="435" y1="164" x2="425" y2="174" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <text x="430" y="190" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">교환 금지</text>
  <!-- Divider -->
  <line x1="40" y1="206" x2="660" y2="206" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Bottom conclusions -->
  <text x="350" y="228" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">스캔아웃 중에는 교환이 일어나지 않음 → 티어링 완전 방지</text>
  <text x="350" y="250" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">하나의 스캔아웃에서는 항상 같은 프레임만 읽힘</text>
  <text x="350" y="272" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">GPU가 렌더링을 완료해도 VBlank까지 대기 → 입력 지연 발생 가능</text>
</svg>
</div>

<br>

티어링은 사라지지만, VBlank까지 대기하는 구조에는 두 가지 부작용이 따릅니다.

<br>

**입력 지연(Input Lag) 증가.**

GPU가 프레임을 완료한 시점과 실제 화면에 표시되는 시점 사이에 최대 한 프레임 주기(60Hz에서 약 16.67ms)의 지연이 추가됩니다.

게임 입력이 즉시 화면에 반영되지 않아, 빠른 반응이 중요한 게임에서 이 지연을 느낄 수 있습니다.

<br>

**프레임 레이트 고정.**

VSync가 활성화되면 프레임 레이트가 디스플레이 갱신 주기의 정수 분의 1로만 제한됩니다.

60Hz에서는 60fps(매 VBlank 교환), 30fps(2 VBlank마다 교환), 20fps(3 VBlank마다 교환) 등입니다.

VBlank 구간에서만 교환이 가능하므로, 프레임 완료 시점이 VBlank 사이에 떨어지면 다음 VBlank까지 대기해야 합니다.

60Hz 디스플레이에서 GPU가 프레임을 16.67ms 이내에 완료하면 60fps가 유지됩니다.

그런데 18ms가 걸리면 해당 VBlank을 놓쳐 다음 VBlank까지 기다려야 하므로, 그 프레임의 표시 간격은 33.33ms — 프레임 레이트가 30fps로 절반 떨어집니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Background -->
  <rect x="0" y="0" width="620" height="370" fill="currentColor" fill-opacity="0.06" rx="5" stroke="currentColor" stroke-width="1.5"/>
  <!-- Title -->
  <text x="310" y="28" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">VSync에서 프레임 레이트 급락</text>
  <text x="310" y="46" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">60Hz 디스플레이 — VBlank 간격 16.67ms</text>
  <!-- ===== TOP: GPU 프레임 시간 = 15ms ===== -->
  <text x="30" y="76" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">GPU 프레임 시간 = 15ms</text>
  <text x="590" y="76" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="end">→ 60fps</text>
  <!-- Timeline -->
  <line x1="60" y1="120" x2="580" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <!-- VBlank markers -->
  <line x1="100" y1="85" x2="100" y2="135" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="100" y="148" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 1</text>
  <line x1="220" y1="85" x2="220" y2="135" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="220" y="148" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 2</text>
  <line x1="340" y1="85" x2="340" y2="135" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="340" y="148" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 3</text>
  <line x1="460" y1="85" x2="460" y2="135" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="460" y="148" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 4</text>
  <line x1="580" y1="85" x2="580" y2="135" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <!-- Render blocks (15ms fits in 16.67ms — ~108px of 120px interval) -->
  <rect x="100" y="96" width="108" height="24" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="154" y="112" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 15ms</text>
  <rect x="220" y="96" width="108" height="24" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="274" y="112" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 15ms</text>
  <rect x="340" y="96" width="108" height="24" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="394" y="112" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 15ms</text>
  <rect x="460" y="96" width="108" height="24" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="514" y="112" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 15ms</text>
  <!-- ===== BOTTOM: GPU 프레임 시간 = 18ms ===== -->
  <text x="30" y="186" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">GPU 프레임 시간 = 18ms</text>
  <text x="590" y="186" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold" text-anchor="end">→ 30fps</text>
  <!-- Timeline -->
  <line x1="60" y1="230" x2="580" y2="230" stroke="currentColor" stroke-width="1.5"/>
  <!-- VBlank markers -->
  <line x1="100" y1="195" x2="100" y2="245" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="100" y="258" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 1</text>
  <line x1="220" y1="195" x2="220" y2="245" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="220" y="258" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 2</text>
  <line x1="340" y1="195" x2="340" y2="245" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="340" y="258" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 3</text>
  <line x1="460" y1="195" x2="460" y2="245" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="460" y="258" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 4</text>
  <line x1="580" y1="195" x2="580" y2="245" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <!-- Render block 1: 18ms, starts VBlank1 (100), ends 230, overshoots VBlank2 (220) -->
  <rect x="100" y="206" width="130" height="24" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="165" y="222" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 18ms</text>
  <text x="232" y="196" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.6">초과</text>
  <!-- Wait block 1: from 230 to VBlank3 (340) -->
  <rect x="230" y="206" width="110" height="24" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" rx="3"/>
  <text x="285" y="222" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle" opacity="0.6">대기</text>
  <!-- Render block 2: starts VBlank3 (340), ends 470, overshoots VBlank4 (460) -->
  <rect x="340" y="206" width="130" height="24" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="405" y="222" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 18ms</text>
  <text x="472" y="196" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.6">초과</text>
  <!-- Wait block 2: from 470 to next VBlank (580) -->
  <rect x="470" y="206" width="110" height="24" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" rx="3"/>
  <text x="525" y="222" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle" opacity="0.6">대기</text>
  <!-- ===== CONCLUSION ===== -->
  <line x1="40" y1="282" x2="580" y2="282" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <text x="310" y="306" fill="currentColor" font-family="sans-serif" font-size="11" text-anchor="middle">16.67ms 이내 → 60fps</text>
  <text x="310" y="328" fill="currentColor" font-family="sans-serif" font-size="11" text-anchor="middle">16.67ms 초과 → 30fps</text>
  <text x="310" y="352" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 하나를 넘기면 프레임 레이트 반감</text>
</svg>
</div>

<br>

이 프레임 레이트 급락 현상은 [게임 루프의 원리 (2)](/dev/unity/GameLoop-2/)에서 다룬 프레임 페이싱과 직접 연결됩니다.

모바일 게임에서는 60fps를 안정적으로 유지하기 어려운 경우, 의도적으로 30fps로 고정하여 일관된 프레임 페이싱을 확보하는 전략을 사용하기도 합니다.

<br>

Unity에서 VSync는 `QualitySettings.vSyncCount`로 제어합니다.

값이 1이면 매 VBlank에 교환(60Hz에서 60fps), 2이면 두 번째 VBlank에 교환(60Hz에서 30fps), 0이면 VSync가 비활성화됩니다.

다만 Android와 iOS에서는 운영체제의 디스플레이 합성기(Android의 SurfaceFlinger/Choreographer, iOS의 CADisplayLink)가 VSync 기반으로 동작하므로, `vSyncCount`를 0으로 설정하더라도 프레임 제출 자체가 VSync 주기에 맞춰지는 경우가 대부분입니다.

모바일에서는 `vSyncCount`보다 `Application.targetFrameRate`로 목표 프레임 레이트를 조절하는 것이 실질적인 제어 수단입니다.

<br>

참고로, VSync의 프레임 레이트 고정 문제를 근본적으로 해결하는 **가변 주사율(VRR, Variable Refresh Rate)** 기술도 존재합니다.

G-Sync, FreeSync, Adaptive Sync 등으로 알려진 이 기술은 디스플레이의 갱신 주기를 고정하지 않고 GPU의 프레임 완료 시점에 맞추어 동적으로 조절합니다.

데스크톱 모니터에서 널리 사용되며, 일부 최신 모바일 기기에서도 지원이 확대되고 있습니다.

VRR이 지원되는 환경에서는 VSync의 프레임 레이트 급락이나 트리플 버퍼링의 입력 지연 문제가 크게 완화됩니다.

---

## 트리플 버퍼링

**트리플 버퍼링(Triple Buffering)**은 더블 버퍼링에 버퍼 하나를 추가하여, VSync의 GPU 유휴 시간과 프레임 레이트 급락을 완화하는 방식입니다.

<br>

앞서 살펴본 것처럼, 더블 버퍼링에서 VSync가 활성화되면 GPU는 백 버퍼에 렌더링을 완료한 뒤 다음 VBlank까지 대기해야 합니다.

백 버퍼가 1개뿐이라 VBlank에서 교환되기 전까지는 새 프레임을 쓸 곳이 없기 때문입니다. 이 대기 시간 동안 GPU는 유휴 상태가 됩니다.

<br>

트리플 버퍼링에서는 백 버퍼가 2개이므로, GPU가 하나의 백 버퍼(백A)에 렌더링을 완료한 즉시 다른 백 버퍼(백B)에 다음 프레임 렌더링을 시작할 수 있습니다.

백A가 VBlank에서 교환되기를 기다리는 동안에도 백B에 쓸 수 있으므로, GPU가 멈추지 않습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 355" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Background -->
  <rect x="0" y="0" width="620" height="355" fill="currentColor" fill-opacity="0.06" rx="5" stroke="currentColor" stroke-width="1.5"/>
  <!-- Title -->
  <text x="310" y="28" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold" text-anchor="middle">더블 버퍼링 vs 트리플 버퍼링</text>

  <!-- ===== TOP SECTION: 더블 버퍼링 ===== -->
  <text x="30" y="60" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">더블 버퍼링 (VSync ON)</text>
  <!-- Timeline -->
  <line x1="60" y1="105" x2="570" y2="105" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="576,105 566,100 566,110" fill="currentColor"/>
  <text x="590" y="109" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">시간</text>
  <!-- VBlank markers -->
  <line x1="100" y1="70" x2="100" y2="120" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="100" y="133" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 1</text>
  <line x1="260" y1="70" x2="260" y2="120" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="260" y="133" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 2</text>
  <line x1="420" y1="70" x2="420" y2="120" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="420" y="133" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 3</text>
  <!-- Render block 1 -->
  <rect x="100" y="81" width="115" height="24" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="157" y="97" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- Wait block 1 -->
  <rect x="215" y="81" width="45" height="24" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" rx="3"/>
  <text x="237" y="97" fill="currentColor" font-family="sans-serif" font-size="8" text-anchor="middle" opacity="0.6">대기</text>
  <!-- swap at VBlank 2 -->
  <text x="260" y="73" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">swap</text>
  <!-- Render block 2 -->
  <rect x="260" y="81" width="115" height="24" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="317" y="97" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- Wait block 2 -->
  <rect x="375" y="81" width="45" height="24" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" rx="3"/>
  <text x="397" y="97" fill="currentColor" font-family="sans-serif" font-size="8" text-anchor="middle" opacity="0.6">대기</text>
  <!-- swap at VBlank 3 -->
  <text x="420" y="73" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">swap</text>
  <!-- Render block 3 -->
  <rect x="420" y="81" width="115" height="24" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="477" y="97" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- Conclusion -->
  <text x="310" y="158" fill="currentColor" font-family="sans-serif" font-size="10" text-anchor="middle">GPU가 12ms에 완료해도 VBlank까지 5ms 대기 → GPU 유휴 시간 발생</text>

  <!-- ===== Divider ===== -->
  <line x1="40" y1="178" x2="580" y2="178" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- ===== BOTTOM SECTION: 트리플 버퍼링 ===== -->
  <text x="30" y="208" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">트리플 버퍼링 (VSync ON)</text>
  <!-- Timeline -->
  <line x1="60" y1="253" x2="570" y2="253" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="576,253 566,248 566,258" fill="currentColor"/>
  <text x="590" y="257" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">시간</text>
  <!-- VBlank markers -->
  <line x1="100" y1="218" x2="100" y2="268" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="100" y="281" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 1</text>
  <line x1="260" y1="218" x2="260" y2="268" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="260" y="281" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 2</text>
  <line x1="420" y1="218" x2="420" y2="268" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="420" y="281" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank 3</text>
  <!-- Render block 1: 버퍼 A -->
  <rect x="100" y="229" width="115" height="24" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="157" y="245" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- Render block 2: 버퍼 B -->
  <rect x="215" y="229" width="115" height="24" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="272" y="245" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- swap at VBlank 2 -->
  <text x="260" y="221" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">swap</text>
  <!-- Render block 3: 버퍼 C (swap으로 해제된 기존 프론트) -->
  <rect x="330" y="229" width="115" height="24" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="387" y="245" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- swap at VBlank 3 -->
  <text x="420" y="221" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">swap</text>
  <!-- Render block 4: 버퍼 A (순환 반복) -->
  <rect x="445" y="229" width="115" height="24" fill="currentColor" fill-opacity="0.24" stroke="currentColor" stroke-width="1" rx="3"/>
  <text x="502" y="245" fill="currentColor" font-family="sans-serif" font-size="9" text-anchor="middle">렌더 12ms</text>
  <!-- Conclusion -->
  <text x="310" y="308" fill="currentColor" font-family="sans-serif" font-size="10" text-anchor="middle">빈 백 버퍼가 있는 동안 다음 프레임 즉시 시작 → 대기 감소 (큐 포화 시 대기 재발생)</text>
  <!-- Legend + Bottom note -->
  <text x="310" y="326" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">3개 버퍼(■ ■ □)가 순환하며 항상 빈 버퍼에 렌더링</text>
  <text x="310" y="340" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5" text-anchor="middle">VBlank에서 표시 가능한 프레임이 있으면 프론트 교환 (프레젠트 모드에 따라 동작 차이)</text>
</svg>
</div>

<br>

트리플 버퍼링은 두 가지 이점을 제공합니다.

<br>

첫째, GPU가 VBlank을 기다리지 않고 계속 다음 프레임을 렌더링할 수 있으므로 **GPU 활용률이 높아집니다**.

빈 백 버퍼가 있는 동안에는 더블 버퍼링에서 발생하던 대기가 줄어듭니다.

<br>

둘째, 프레임 시간이 VBlank 간격을 약간 초과하더라도 프레임 레이트가 절반으로 떨어지지 않습니다.

60Hz에서 프레임 시간이 18ms인 경우, 더블 버퍼링에서는 매 프레임이 VBlank을 놓쳐 30fps로 고정됩니다.

트리플 버퍼링에서는 GPU가 대기 없이 계속 렌더링하므로, GPU의 처리량은 약 55fps(1000/18ms)를 유지합니다.

디스플레이는 여전히 60Hz로 동작하지만, 매 VBlank마다 가장 최근 완료된 프레임을 표시하므로 대부분의 VBlank에서 새 프레임이 나타납니다.

다만 GPU 처리량과 디스플레이 주파수가 정확히 일치하지 않으면, 간헐적으로 같은 프레임이 두 VBlank 연속 표시되는 미세한 끊김(micro-stutter)이 발생할 수 있습니다.

<br>

한편, 백 버퍼가 2개이므로 디스플레이에 표시 중인 프레임과 GPU가 렌더링 중인 프레임 사이의 격차가 더블 버퍼링보다 한 프레임 더 벌어질 수 있어, 사용자의 입력이 화면에 반영되기까지 최대 한 프레임분의 **입력 지연이 추가**되는 트레이드오프가 있습니다.

다만, 이는 VBlank 시점에 **가장 최근 완료된 백 버퍼**를 프론트와 교환하는 방식(Vulkan의 mailbox 모드, Android SurfaceFlinger 등) 기준이며, 완료된 프레임을 대기열에 순서대로 쌓아두는 방식(DirectX의 render-ahead queue 등)에서는 대기열 깊이만큼 입력 지연이 더 늘어날 수 있습니다.

<br>

트리플 버퍼링의 비용은 **메모리 사용량 증가**입니다. 색상 버퍼가 2개에서 3개로 늘어나므로, Full HD RGBA8 기준으로 약 8MB가 추가됩니다. 모바일에서 메모리가 제한적인 환경에서는 이 추가 비용이 무시할 수 없습니다.

<br>

Unity에서 트리플 버퍼링은 플랫폼과 그래픽스 API에 따라 자동으로 결정됩니다. 대부분의 모바일 플랫폼(Android, iOS)에서는 운영체제의 컴포지터 수준에서 트리플 버퍼링이 기본 동작입니다.

---

## 앨리어싱

디스플레이 동기화와 별개로, 래스터화에는 또 다른 근본적인 한계가 있습니다.

연속적인 도형(삼각형의 가장자리)을 이산적인 격자(픽셀)로 표현하면 가장자리에 계단이 생기는데, 이 현상을 **앨리어싱(Aliasing)**이라 하며 톱니 모양의 가장자리를 **jaggies**라고 부릅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <rect x="0" y="0" width="580" height="300" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="24" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">앨리어싱의 발생 원리</text>
  <!-- Left: smooth diagonal -->
  <text x="120" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">연속적인 삼각형 가장자리</text>
  <rect x="30" y="62" width="180" height="180" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <line x1="30" y1="242" x2="210" y2="62" stroke="currentColor" stroke-width="2"/>
  <!-- Arrow between -->
  <line x1="225" y1="152" x2="295" y2="152" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="305,152 295,147 295,157" fill="currentColor"/>
  <!-- Right: pixel grid label -->
  <text x="420" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">픽셀 격자로 표현</text>
  <!-- 6x6 grid, cell=28, origin=(312,64) -->
  <!-- Row 0: □□□□□■ -->
  <rect x="312" y="64" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="340" y="64" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="368" y="64" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="396" y="64" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="424" y="64" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="452" y="64" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 1: □□□□■■ -->
  <rect x="312" y="92" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="340" y="92" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="368" y="92" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="396" y="92" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="424" y="92" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="452" y="92" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 2: □□□■■■ -->
  <rect x="312" y="120" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="340" y="120" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="368" y="120" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="396" y="120" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="424" y="120" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="452" y="120" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 3: □□■■■■ -->
  <rect x="312" y="148" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="340" y="148" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="368" y="148" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="396" y="148" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="424" y="148" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="452" y="148" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 4: □■■■■■ -->
  <rect x="312" y="176" width="28" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="340" y="176" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="368" y="176" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="396" y="176" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="424" y="176" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="452" y="176" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 5: ■■■■■■ -->
  <rect x="312" y="204" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="340" y="204" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="368" y="204" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="396" y="204" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="424" y="204" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="452" y="204" width="28" height="28" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Diagonal overlay on grid -->
  <line x1="312" y1="232" x2="480" y2="64" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.4"/>
  <!-- Legend -->
  <text x="500" y="150" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">■ 켜짐</text>
  <text x="500" y="165" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">□ 꺼짐</text>
  <!-- Annotation -->
  <text x="290" y="256" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">픽셀은 '켜짐(■)' 또는 '꺼짐(□)' 두 상태뿐</text>
  <text x="290" y="274" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">→ 대각선 가장자리가 계단 형태로 표현됨</text>
</svg>
</div>

### 나이퀴스트 정리와 앨리어싱

앨리어싱이 단순히 해상도가 낮아서 생기는 문제처럼 보이지만, 근본 원인은 **샘플링 자체의 한계**에 있습니다.

신호 처리 이론의 **나이퀴스트 정리(Nyquist Theorem)**에 따르면, 연속 신호를 이산 샘플로 정확히 복원하려면, 샘플링 주파수가 원래 신호의 최대 주파수의 2배 이상이어야 합니다.

이 조건을 충족하지 못하면, 원래 신호에 존재하지 않던 가짜 패턴(앨리어스)이 나타납니다.

<br>

이 관점에서, 래스터화는 연속적인 장면을 픽셀 격자로 찍어내는 **공간적 샘플링**입니다.

샘플링 주파수에 대응하는 것은 픽셀 밀도(해상도)이고, 신호의 주파수에 대응하는 것은 화면에서 얼마나 짧은 거리 안에 색상이 바뀌는지를 나타내는 **공간 주파수**입니다.

넓은 하늘처럼 색상이 천천히 바뀌는 영역은 공간 주파수가 낮고, 체크무늬 패턴이나 삼각형 가장자리처럼 색상이 급격히 바뀌는 영역은 공간 주파수가 높습니다.

<br>

삼각형 가장자리는 색상이 한 픽셀 내에서 삼각형 안쪽과 바깥쪽으로 불연속하게 바뀌는 경계이므로, 이론적으로 무한히 높은 공간 주파수를 가지며 유한한 해상도의 픽셀 격자로는 완벽하게 표현할 수 없습니다.

해상도를 높이면 계단의 크기가 줄어들어 눈에 덜 띄지만, 앨리어싱 자체를 완전히 제거할 수는 없습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <rect x="0" y="0" width="600" height="340" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="24" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">해상도와 앨리어싱</text>
  <!-- LEFT: 저해상도 (480p) — 4x4 grid, cell=32 -->
  <text x="140" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">저해상도 (480p)</text>
  <!-- Row 0: □□□■ -->
  <rect x="44" y="64" width="32" height="32" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="76" y="64" width="32" height="32" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="108" y="64" width="32" height="32" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="140" y="64" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 1: □□■■ -->
  <rect x="44" y="96" width="32" height="32" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="76" y="96" width="32" height="32" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="108" y="96" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="140" y="96" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 2: □■■■ -->
  <rect x="44" y="128" width="32" height="32" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5"/>
  <rect x="76" y="128" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="108" y="128" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="140" y="128" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Row 3: ■■■■ -->
  <rect x="44" y="160" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="76" y="160" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="108" y="160" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <rect x="140" y="160" width="32" height="32" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.5"/>
  <!-- Diagonal overlay on low-res -->
  <line x1="44" y1="192" x2="172" y2="64" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3" opacity="0.4"/>
  <text x="140" y="210" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">큰 계단, 눈에 잘 보임</text>
  <!-- Separator -->
  <line x1="280" y1="55" x2="280" y2="220" stroke="currentColor" stroke-width="0.5" stroke-dasharray="3,3" opacity="0.3"/>
  <!-- RIGHT: 고해상도 (4K) — 12x8 grid, cell=12, origin=(332,64) -->
  <text x="440" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">고해상도 (4K)</text>
  <!-- Row 0: cols 10,11 filled -->
  <rect x="332" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="64" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 1: cols 9..11 -->
  <rect x="332" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="76" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 2: cols 8..11 -->
  <rect x="332" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="88" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 3: cols 7..11 -->
  <rect x="332" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="100" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 4: cols 5..11 -->
  <rect x="332" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="112" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 5: cols 4..11 -->
  <rect x="332" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="124" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 6: cols 3..11 -->
  <rect x="332" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="136" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Row 7: cols 2..11 -->
  <rect x="332" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="344" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.3"/>
  <rect x="356" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="368" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="380" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="392" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="404" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="416" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="428" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="440" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="452" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <rect x="464" y="148" width="12" height="12" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="0.3"/>
  <!-- Diagonal overlay on high-res grid -->
  <line x1="332" y1="160" x2="476" y2="64" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2" opacity="0.4"/>
  <text x="440" y="178" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">작은 계단, 상대적으로 덜 보임</text>
  <!-- Bottom annotations -->
  <text x="300" y="248" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">해상도를 높이면 앨리어싱이 줄지만 완전히 사라지지는 않음</text>
  <text x="300" y="268" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">또한 해상도를 높이면 프래그먼트 수가 급증하여 렌더링 비용도 급증</text>
  <!-- Legend -->
  <text x="30" y="248" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">■ 삼각형 내부</text>
  <text x="30" y="263" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">□ 삼각형 외부</text>
  <text x="30" y="278" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">--- 실제 가장자리</text>
</svg>
</div>

<br>

모바일에서는 해상도를 무한정 높일 수 없으므로, 별도의 안티앨리어싱 기법으로 계단 현상을 완화합니다.

---

## 안티앨리어싱 기법들

**안티앨리어싱(Anti-Aliasing)**은 앨리어싱을 줄이기 위한 기법의 총칭입니다.

접근 방식에 따라 크게 **샘플링 기반(하드웨어)**과 **후처리 기반(소프트웨어)**으로 나뉩니다.

### MSAA (Multi-Sample Anti-Aliasing)

MSAA는 래스터화 단계에서 작동하는 **하드웨어 기반** 안티앨리어싱입니다.

각 픽셀 내에 여러 **서브 샘플(Sub-sample)** 위치를 설정하고, 삼각형 가장자리가 이 서브 샘플 중 일부만 덮는지 전부 덮는지에 따라 가장자리의 색상을 부드럽게 만듭니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <rect x="0" y="0" width="560" height="340" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="24" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">MSAA 4x의 동작</text>
  <!-- LEFT: pixel with 4 sub-samples -->
  <text x="130" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">하나의 픽셀 내 4개 서브 샘플</text>
  <rect x="40" y="65" width="180" height="160" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- Sub-sample dots at quarter positions -->
  <circle cx="85" cy="105" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>
  <circle cx="175" cy="105" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>
  <circle cx="85" cy="185" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>
  <circle cx="175" cy="185" r="5" fill="currentColor" fill-opacity="0.3" stroke="currentColor" stroke-width="1"/>
  <!-- Labels -->
  <text x="85" cy="105" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">0</text>
  <text x="175" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">1</text>
  <text x="85" y="200" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">2</text>
  <text x="175" y="200" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">3</text>
  <text x="130" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">· = 서브 샘플 위치 (예시)</text>
  <!-- Arrow between -->
  <line x1="235" y1="145" x2="295" y2="145" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="305,145 295,140 295,150" fill="currentColor"/>
  <!-- RIGHT: pixel with triangle edge -->
  <text x="430" y="50" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">삼각형 가장자리가 픽셀을 부분적으로 덮는 경우</text>
  <rect x="340" y="65" width="180" height="160" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <!-- Triangle fill (left portion) -->
  <polygon points="340,65 340,225 475,65" fill="currentColor" fill-opacity="0.08"/>
  <!-- Triangle edge diagonal -->
  <line x1="340" y1="225" x2="475" y2="65" stroke="currentColor" stroke-width="2"/>
  <!-- Sub-sample 0 (top-left) — INSIDE triangle -->
  <circle cx="385" cy="105" r="6" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <text x="385" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">0</text>
  <!-- Sub-sample 1 (top-right) — OUTSIDE -->
  <circle cx="475" cy="105" r="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="475" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">1</text>
  <!-- Sub-sample 2 (bottom-left) — INSIDE -->
  <circle cx="385" cy="185" r="6" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <text x="385" y="200" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">2</text>
  <!-- Sub-sample 3 (bottom-right) — OUTSIDE -->
  <circle cx="475" cy="185" r="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="475" y="200" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">3</text>
  <!-- Legend for right side -->
  <text x="430" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">■ = 삼각형 내부 (2개)  · = 삼각형 외부 (2개)</text>
  <!-- Bottom annotations -->
  <text x="280" y="270" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">4개 중 2개가 삼각형 내부 → 커버리지 = 50%</text>
  <text x="280" y="290" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">최종 색상 = 서브 샘플 색상의 평균 (커버리지 비율 2/4 반영)</text>
  <text x="280" y="310" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">→ 경계 픽셀에서 부분 커버리지를 반영해 계단 현상 완화</text>
</svg>
</div>

<br>

MSAA에서 서브 샘플마다 개별적으로 계산되는 것은 커버리지(삼각형이 해당 위치를 덮는지)와 깊이 값뿐이며, **프래그먼트 셰이더는 보통 픽셀당 1번만 실행**됩니다.

계산된 색상은 삼각형이 덮는 서브 샘플에만 기록되고, 덮지 않는 서브 샘플에는 기존 배경 색상이 남습니다.

최종 출력 시 4개 서브 샘플의 색상을 평균하는 **리졸브(Resolve)** 과정을 거쳐 최종 픽셀 색상이 결정됩니다.

<br>

가장 단순한 안티앨리어싱인 **SSAA(Super-Sample Anti-Aliasing)**는 서브 샘플마다 프래그먼트 셰이더를 실행하므로, 4x SSAA의 셰이더 비용은 이론상 4배입니다.

MSAA는 보통 셰이더를 1번만 실행하고 커버리지만 서브 샘플별로 계산하므로, 동일한 서브 샘플 수에서 셰이더 비용이 SSAA의 1/4에 불과합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <rect x="0" y="0" width="600" height="440" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="24" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">MSAA에서 셰이더 실행과 커버리지</text>
  <!-- TOP: SSAA comparison -->
  <rect x="30" y="40" width="540" height="40" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="300" y="57" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">SSAA: 서브 샘플마다 셰이더 실행 → 4x = 이론상 비용 4배</text>
  <text x="300" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">비현실적인 비용</text>
  <!-- MAIN: MSAA detail box -->
  <rect x="30" y="90" width="540" height="300" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="110" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">MSAA: 보통 픽셀당 셰이더 1회 실행</text>
  <!-- 4 sub-samples grid -->
  <rect x="50" y="122" width="250" height="130" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="175" y="140" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">서브 샘플별 데이터</text>
  <!-- Sub-sample 0 -->
  <circle cx="80" cy="168" r="6" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <text x="95" y="163" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9">샘플 0: 커버리지=1, 깊이=0.3</text>
  <!-- Sub-sample 1 -->
  <circle cx="80" cy="190" r="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="95" y="194" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">샘플 1: 커버리지=0, 깊이=N/A</text>
  <!-- Sub-sample 2 -->
  <circle cx="80" cy="212" r="6" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1"/>
  <text x="95" y="216" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9">샘플 2: 커버리지=1, 깊이=0.3</text>
  <!-- Sub-sample 3 -->
  <circle cx="80" cy="234" r="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="95" y="238" text-anchor="start" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">샘플 3: 커버리지=0, 깊이=N/A</text>
  <!-- Arrow to shader -->
  <line x1="310" y1="190" x2="355" y2="190" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="365,190 355,185 355,195" fill="currentColor"/>
  <!-- Shader execution box -->
  <rect x="370" y="125" width="190" height="60" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="465" y="147" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">셰이더 1번 실행 (보통)</text>
  <text x="465" y="165" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">결과: 빨강 (1, 0, 0)</text>
  <!-- Arrow down from shader to sub-sample assignment -->
  <line x1="465" y1="185" x2="465" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="465,220 460,210 470,210" fill="currentColor"/>
  <!-- Result assignment -->
  <rect x="370" y="222" width="190" height="60" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="465" y="242" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9">커버된 샘플 0, 2 → 빨강 기록</text>
  <text x="465" y="258" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.6">샘플 1, 3 → 기존 배경 유지</text>
  <!-- Arrow down to resolve -->
  <line x1="300" y1="290" x2="300" y2="310" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="300,320 295,310 305,310" fill="currentColor"/>
  <!-- Resolve step -->
  <rect x="60" y="322" width="480" height="55" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="300" y="342" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">리졸브 (Resolve)</text>
  <text x="300" y="362" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">(빨강 + 빨강 + 배경 + 배경) / 4 = 50% 빨강 + 50% 배경</text>
  <!-- Bottom summary -->
  <text x="300" y="408" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">보통 셰이더 비용은 SSAA의 1/4 — 커버리지만 서브 샘플별로 계산</text>
  <text x="300" y="428" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">가장자리에서만 중간색이 생기므로 부드러운 에지 표현</text>
</svg>
</div>

<br>

MSAA는 삼각형 가장자리의 앨리어싱에 효과적입니다.

하지만 텍스처 내부의 앨리어싱(미세한 반복 패턴이 픽셀 격자와 간섭하여 생기는 모아레 무늬 등)이나, 셰이더에서 발생하는 앨리어싱(스페큘러 하이라이트의 깜박임 등)에는 효과가 없습니다.

이 종류의 앨리어싱은 서브 샘플의 커버리지가 아니라 셰이더 연산 자체에서 발생하기 때문입니다.

<br>

**모바일에서의 MSAA.**

[GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 것처럼, TBDR 아키텍처에서 MSAA는 온칩 타일 메모리에서 수행됩니다.

서브 샘플 데이터가 온칩에만 존재하고, 타일이 완료될 때 리졸브하여 최종 색상만 외부 메모리에 기록합니다.

4xMSAA를 적용해도 외부 메모리에 기록되는 데이터량은 MSAA 없이 렌더링할 때와 동일합니다.

반면 IMR(Immediate Mode Rendering, 데스크톱 GPU의 기본 렌더링 방식)에서는 서브 샘플 데이터가 외부 메모리에 상주하므로 대역폭 부하가 샘플 수에 비례하여 늘어납니다.

이 구조 덕분에 TBDR 기반 모바일 GPU에서는 MSAA의 대역폭 비용이 IMR보다 낮습니다.

<br>

온칩 타일 메모리 사용량이 서브 샘플 수에 비례하여 증가하므로(4xMSAA에서 4배), GPU에 따라 유효 타일 크기가 줄어들 수 있고, 리졸브 연산의 비용도 존재합니다.

그럼에도 IMR 대비 대역폭 이점이 크기 때문에, TBDR 기반 모바일에서 MSAA는 가장 권장되는 안티앨리어싱 기법입니다.

<br>

Unity URP에서 MSAA는 렌더 파이프라인 에셋의 Quality 설정에서 활성화하며, 2x 또는 4x가 일반적입니다. 모바일에서도 4xMSAA까지 합리적인 비용으로 사용할 수 있습니다.

다만 후처리(Post-Processing)와의 호환성 제약이 있습니다. 후처리 효과가 렌더 텍스처를 읽으려면 서브 샘플 데이터를 먼저 리졸브해야 하는데, 리졸브 후에는 서브 샘플 정보가 사라지므로 후처리 단계의 효과(블룸, 톤매핑 등)에는 MSAA가 적용되지 않습니다. URP에서 후처리가 활성화되면 이 리졸브 패스가 자동으로 삽입됩니다.

### FXAA (Fast Approximate Anti-Aliasing)

FXAA는 **후처리 기반** 안티앨리어싱입니다.

렌더링이 완료된 최종 이미지에 대해 **이미지 처리**로 가장자리를 부드럽게 만듭니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 760 315" xmlns="http://www.w3.org/2000/svg" style="max-width: 760px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="760" height="315" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="380" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">FXAA의 동작 원리</text>

  <!-- Step 1: 에지 검출 -->
  <rect x="20" y="50" width="220" height="220" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">1단계: 에지 검출</text>
  <!-- 3x3 grid: 휘도(luma) 값 -->
  <rect x="55" y="88" width="50" height="36" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="111" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.82</text>
  <rect x="105" y="88" width="50" height="36" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="111" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.78</text>
  <rect x="155" y="88" width="50" height="36" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="111" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.85</text>
  <!-- row 2 -->
  <rect x="55" y="124" width="50" height="36" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="147" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.80</text>
  <rect x="105" y="124" width="50" height="36" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="147" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.75</text>
  <rect x="155" y="124" width="50" height="36" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="147" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.21</text>
  <!-- row 3 -->
  <rect x="55" y="160" width="50" height="36" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="183" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.18</text>
  <rect x="105" y="160" width="50" height="36" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="183" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.15</text>
  <rect x="155" y="160" width="50" height="36" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <text x="180" y="183" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">0.20</text>
  <!-- edge indicator (L-shape, 2px inset toward bright side to avoid overlap with cell borders) -->
  <line x1="55" y1="158" x2="153" y2="158" stroke="currentColor" stroke-width="2" stroke-dasharray="4,2" opacity="0.7"/>
  <line x1="153" y1="122" x2="153" y2="158" stroke="currentColor" stroke-width="2" stroke-dasharray="4,2" opacity="0.7"/>
  <line x1="153" y1="122" x2="205" y2="122" stroke="currentColor" stroke-width="2" stroke-dasharray="4,2" opacity="0.7"/>
  <text x="130" y="215" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">휘도 대비가 임계값 이상</text>
  <text x="130" y="228" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">→ 에지 후보</text>

  <!-- Arrow 1→2 -->
  <line x1="248" y1="160" x2="278" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="284,160 274,155 274,165" fill="currentColor"/>

  <!-- Step 2: 에지 방향 분석 -->
  <rect x="290" y="50" width="180" height="220" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="380" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">2단계: 에지 방향 분석</text>
  <!-- 2×3 mini grid: bright top, dark bottom (echoes step 1) -->
  <rect x="326" y="90" width="36" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <rect x="362" y="90" width="36" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <rect x="398" y="90" width="36" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <rect x="326" y="118" width="36" height="28" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="0.7"/>
  <rect x="362" y="118" width="36" height="28" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="0.7"/>
  <rect x="398" y="118" width="36" height="28" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="0.7"/>
  <!-- Edge direction arrow along bright/dark boundary (2px inset) -->
  <line x1="318" y1="116" x2="440" y2="116" stroke="currentColor" stroke-width="2.5"/>
  <polygon points="445,116 437,111 437,121" fill="currentColor"/>
  <!-- Result -->
  <text x="380" y="168" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">에지 방향: 수평</text>
  <!-- Caption -->
  <text x="380" y="205" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">주변 대비를 비교해</text>
  <text x="380" y="218" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">에지가 뻗어가는 방향을 근사</text>

  <!-- Arrow 2→3 -->
  <line x1="478" y1="160" x2="508" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="514,160 504,155 504,165" fill="currentColor"/>

  <!-- Step 3: 에지 방향 블렌딩 -->
  <rect x="520" y="50" width="220" height="220" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="630" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">3단계: 에지 방향 블렌딩</text>
  <text x="630" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">에지 방향으로 여러 지점 샘플링</text>
  <!-- Edge direction line -->
  <line x1="545" y1="130" x2="715" y2="130" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2" opacity="0.3"/>
  <!-- Sample points along edge (size = weight) -->
  <circle cx="558" cy="130" r="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="0.8"/>
  <circle cx="582" cy="130" r="3.5" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8"/>
  <circle cx="606" cy="130" r="4" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <circle cx="630" cy="130" r="5.5" fill="currentColor" fill-opacity="0.7" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="654" cy="130" r="4" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <circle cx="678" cy="130" r="3.5" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="0.8"/>
  <circle cx="702" cy="130" r="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="0.8"/>
  <text x="630" y="117" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" font-weight="bold">중심 픽셀</text>
  <!-- Legend -->
  <text x="630" y="149" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.4">● 크기 = 가중치 (중심에 가까울수록 큼)</text>
  <!-- Arrow down -->
  <line x1="630" y1="158" x2="630" y2="172" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="630,178 625,170 635,170" fill="currentColor"/>
  <!-- Result: before/after (only edge boundary pixels change) -->
  <text x="580" y="193" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">적용 전</text>
  <rect x="540" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <rect x="560" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <rect x="580" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="0.7"/>
  <rect x="600" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="0.7"/>
  <text x="630" y="212" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">→</text>
  <text x="680" y="193" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8" opacity="0.5">적용 후</text>
  <rect x="640" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <rect x="660" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="0.7"/>
  <rect x="680" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="0.7"/>
  <rect x="700" y="198" width="20" height="20" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="0.7"/>
  <!-- caption -->
  <text x="630" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">가중 혼합 → 에지 경계만 부드럽게</text>
  <text x="630" y="254" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(전체 블러가 아닌 에지 맞춤 필터링)</text>

  <!-- bottom note -->
  <text x="380" y="286" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">후처리라 기하 정보 없이 이미지 휘도 대비로만 에지 추정 (풀스크린 1패스)</text>
  <text x="380" y="302" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">→ 에지가 아닌 디테일도 뭉개져 선명도가 일부 감소할 수 있음</text>
</svg>
</div>

<br>

FXAA는 비용이 낮습니다.

하나의 풀스크린 후처리 패스로 수행되며, 삼각형 수나 장면 복잡도와 무관하게 해상도에만 비례합니다. 장면이 아무리 복잡해도 비용이 늘어나지 않습니다.

또한 삼각형 가장자리뿐 아니라 텍스처 경계, 셰이더 에지 등 이미지의 모든 고대비 경계에 효과가 있습니다.

<br>

반면, FXAA는 기하학적 정보 없이 최종 이미지의 밝기 차이만으로 에지를 추정하므로, 에지가 아닌 세밀한 디테일(텍스트, 가는 선, 텍스처의 미세한 패턴)까지 함께 흐려질 수 있습니다.

Unity URP에서는 카메라 컴포넌트의 Anti-aliasing 설정에서 FXAA를 선택할 수 있습니다.

<br>

모바일에서 FXAA는 MSAA 대비 텍스처 디테일 손실이 크고, TBDR에서 MSAA의 비용이 충분히 낮으므로, MSAA가 선호되는 경우가 많습니다.

다만 후처리 파이프라인이 이미 존재하고 MSAA와 호환되지 않는 특수한 상황에서는 FXAA가 대안이 됩니다.

### TAA (Temporal Anti-Aliasing)

TAA는 **시간적(Temporal)** 정보를 활용하는 안티앨리어싱입니다.

매 프레임마다 카메라의 투영 행렬에 서브 픽셀 크기의 미세한 오프셋(**지터링, Jittering**)을 적용하면, 장면 전체가 화면상에서 1픽셀 미만만큼 미세하게 이동하므로 삼각형 가장자리가 픽셀 격자와 만나는 위치가 프레임마다 달라집니다.

여러 프레임에 걸쳐 서로 다른 서브 픽셀 위치의 샘플을 누적하여 가장자리를 부드럽게 만듭니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="580" height="340" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="290" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">TAA의 원리</text>

  <!-- TOP: 4 frames with sub-pixel jitter positions -->
  <!-- Frame 1 -->
  <rect x="60" y="50" width="80" height="80" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">프레임 1</text>
  <!-- 4x4 pixel grid lines -->
  <line x1="80" y1="74" x2="80" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="100" y1="74" x2="100" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="120" y1="74" x2="120" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="64" y1="87" x2="136" y2="87" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="64" y1="100" x2="136" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="64" y1="113" x2="136" y2="113" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- dot at (1,1) position -->
  <circle cx="80" cy="87" r="4" fill="currentColor"/>

  <!-- Frame 2 -->
  <rect x="180" y="50" width="80" height="80" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">프레임 2</text>
  <line x1="200" y1="74" x2="200" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="220" y1="74" x2="220" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="240" y1="74" x2="240" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="184" y1="87" x2="256" y2="87" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="184" y1="100" x2="256" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="184" y1="113" x2="256" y2="113" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- dot at (1,3) position -->
  <circle cx="200" cy="113" r="4" fill="currentColor"/>

  <!-- Frame 3 -->
  <rect x="300" y="50" width="80" height="80" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">프레임 3</text>
  <line x1="320" y1="74" x2="320" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="340" y1="74" x2="340" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="360" y1="74" x2="360" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="304" y1="87" x2="376" y2="87" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="304" y1="100" x2="376" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="304" y1="113" x2="376" y2="113" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- dot at (3,1) position -->
  <circle cx="340" cy="87" r="4" fill="currentColor"/>

  <!-- Frame 4 -->
  <rect x="420" y="50" width="80" height="80" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="68" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">프레임 4</text>
  <line x1="440" y1="74" x2="440" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="460" y1="74" x2="460" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="480" y1="74" x2="480" y2="126" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="424" y1="87" x2="496" y2="87" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="424" y1="100" x2="496" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <line x1="424" y1="113" x2="496" y2="113" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- dot at (3,3) position -->
  <circle cx="460" cy="113" r="4" fill="currentColor"/>

  <!-- Bracket connecting 4 frames -->
  <line x1="100" y1="134" x2="100" y2="142" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="100" y1="142" x2="460" y2="142" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="460" y1="134" x2="460" y2="142" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- Labels -->
  <text x="290" y="158" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">서브 픽셀 위치가 매 프레임 다름</text>
  <text x="290" y="174" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">투영 행렬에 서브 픽셀 오프셋(지터)을 적용</text>

  <!-- Single arrow down to formula box -->
  <line x1="290" y1="182" x2="290" y2="194" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,200 285,192 295,192" fill="currentColor"/>

  <!-- BOTTOM: Blending formula box -->
  <rect x="100" y="200" width="380" height="90" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="225" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">시간적 누적 (Temporal Accumulation)</text>
  <text x="290" y="252" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">누적 결과 = 현재 샘플 × α + 이전 누적 × (1 - α)</text>
  <text x="290" y="275" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">(α ≒ 0.05 ~ 0.1)</text>

  <!-- Bottom note -->
  <text x="290" y="316" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11">→ 여러 서브 픽셀 위치의 샘플이 누적되어 가장자리가 부드러워짐</text>
  <text x="290" y="334" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">프레임당 추가 샘플링 없이 시간 축 누적만으로 안티앨리어싱 수행</text>
</svg>
</div>

<br>

TAA는 프레임당 추가 샘플링 없이 시간 축의 누적만으로 안티앨리어싱을 수행하므로, 단일 프레임 기준의 비용이 낮습니다. 

삼각형 가장자리뿐 아니라 셰이더 앨리어싱, 스페큘러 반짝임 등에도 효과적입니다.

<br>

TAA의 주요 문제는 **고스팅(Ghosting)**과 **흐려짐**입니다.

고스팅은 오브젝트가 빠르게 움직일 때 이전 프레임의 잔상이 현재 프레임에 남는 현상입니다.

TAA는 이전 프레임의 결과를 현재 프레임에서 재사용하며, 이를 위해 이전 프레임의 픽셀을 현재 프레임의 좌표로 옮기는 **재투영(Reprojection)**을 수행합니다.

오브젝트가 움직이면 이전 프레임의 픽셀 위치와 현재 위치가 달라지므로 잔상이 생깁니다.

<br>

이 문제를 완화하기 위해 **모션 벡터(Motion Vector)**를 사용합니다.

모션 벡터는 각 픽셀의 프레임 간 이동량을 기록하며, 이를 통해 이전 프레임의 픽셀을 현재 위치로 보정합니다.

다만 이전 프레임에서 가려져 있다가 새로 드러나는 영역(disocclusion)에서는 참조할 이전 데이터가 없으므로 고스팅이 여전히 나타납니다.

<br>

흐려짐은 여러 프레임의 데이터를 블렌딩하는 과정에서 발생합니다.

카메라가 정지해 있으면 샘플이 안정적으로 누적되어 선명해지지만, 카메라가 움직이면 누적 데이터가 흐릿한 상태로 유지될 수 있습니다.

TAA 이후에 **샤프닝(Sharpening) 패스**를 추가하여 이를 완화하는 것이 일반적이며, Unity URP의 TAA도 내부적으로 샤프닝을 적용합니다.

<br>

TAA는 데스크톱과 콘솔에서 널리 사용되며, Unity URP에서는 카메라 컴포넌트의 Anti-aliasing 설정에서 TAA를 선택할 수 있습니다.

모바일에서도 지원되지만, 모션 벡터 생성 패스와 누적 결과를 저장하는 히스토리 버퍼의 추가 비용을 고려해야 합니다.

### SMAA (Subpixel Morphological Anti-Aliasing)

SMAA는 FXAA와 마찬가지로 후처리 기반이지만, 에지 검출의 정확도가 높습니다.

FXAA가 인접 픽셀의 밝기 차이만으로 에지를 추정하는 반면, SMAA는 에지의 **형태(morphology)**를 분석합니다.

검출된 에지가 L자, Z자, U자 등 어떤 패턴인지 인식하고, 각 패턴에 최적화된 블렌딩 가중치를 적용합니다.

<br>

SMAA는 FXAA보다 가장자리 품질이 높고 흐려짐이 적지만, 후처리 패스가 여러 단계(에지 검출 → 블렌딩 가중치 계산 → 최종 블렌딩)로 나뉘므로 비용도 높습니다.

Unity URP에서는 카메라 컴포넌트의 Anti-aliasing 설정에서 SMAA를 선택할 수 있으며, Low/Medium/High 품질 단계를 지정할 수 있습니다.

### 안티앨리어싱 기법 비교

지금까지 다룬 네 가지 안티앨리어싱 기법의 특성을 비교합니다.

| | MSAA | FXAA | TAA | SMAA |
|---|---|---|---|---|
| 유형 | 하드웨어 (래스터화 단계) | 후처리 (이미지 기반) | 시간적 (프레임 누적) | 후처리 (형태 분석) |
| 작동 위치 | 래스터화 | 최종 이미지 (1 패스) | 최종 이미지 (1 패스 + 히스토리) | 최종 이미지 (3 패스) |
| 가장자리 품질 | 좋음 (기하 정보 기반) | 보통 (밝기 차이 기반) | 좋음 (서브 픽셀 누적) | 좋음 (형태 기반 분석) |
| 셰이더 앨리어싱 | 효과 없음 (커버리지만) | 효과 있음 (모든 에지) | 효과 있음 (모든 에지) | 효과 있음 (모든 에지) |
| 흐려짐 | 없음 | 있음 | 있음 (움직임) | 적음 |
| 비용 | TBDR에서 낮음 / IMR에서 중간 | 낮음 | 중간 | 중간~높음 |
| 모바일 적합도 | 권장 (TBDR 이점) | 대안 (비용 낮음) | 조건부 사용 (메모리 비용) | 제한적 (패스 비용) |

<br>

TBDR 기반 모바일에서는 MSAA의 대역폭 비용이 낮으므로 **MSAA 4x가 첫 번째 선택지**입니다. 후처리 파이프라인과의 호환성 문제가 있거나 셰이더 앨리어싱까지 해결해야 하는 경우 FXAA 또는 TAA를 고려합니다. 각 기법의 비용과 품질 트레이드오프는 대상 기기의 GPU 성능에 따라 달라지므로, 프로파일링으로 확인하는 것이 가장 정확합니다.

---

## 마무리

- **스캔아웃**은 프레임 버퍼를 왼쪽 위부터 순차적으로 읽어 디스플레이에 전송하는 과정입니다.
- **티어링**은 스캔아웃 도중 프레임 버퍼가 교체되어 화면에 두 프레임이 섞이는 현상입니다.
- **더블 버퍼링**은 프론트/백 두 버퍼를 교환하여, 렌더링 중인 프레임이 화면에 노출되지 않게 합니다.
- **VSync**는 버퍼 교환을 디스플레이 갱신 타이밍에 맞추어 티어링을 방지하지만, 입력 지연과 프레임 레이트 고정의 부작용이 있습니다.
- **트리플 버퍼링**은 백 버퍼를 2개 사용하여 VSync의 GPU 유휴 시간을 줄이고 프레임 레이트 급락을 완화하지만, 디스플레이와 GPU 사이의 프레임 격차가 벌어져 입력 지연이 추가될 수 있습니다.
- **앨리어싱**은 연속적인 삼각형 가장자리를 이산 픽셀로 표현할 때 발생하는 계단 현상이며, 해상도만으로는 완전히 해결되지 않습니다.
- **MSAA**는 하드웨어 기반으로 서브 샘플 커버리지를 사용하며, TBDR에서 대역폭 비용이 낮아 모바일에서 권장됩니다.
- **FXAA**는 후처리 기반으로 비용이 낮지만 이미지가 흐려지고, **SMAA**는 에지 형태 분석으로 FXAA보다 정확하지만 여러 패스가 필요하므로 비용이 높습니다.
- **TAA**는 프레임 간 서브 픽셀 누적으로 높은 품질을 달성하지만 고스팅이 발생합니다.

래스터화 파이프라인 시리즈 전체를 통해, 삼각형이 화면의 프래그먼트로 변환되고(Part 1), 여러 버퍼 시스템을 거쳐 최종 픽셀로 확정되며(Part 2), 디스플레이에 표시되어 사용자의 눈에 도달하는(Part 3) 전 과정을 다루었습니다. 이 과정에서 프래그먼트 수, 오버드로우, 버퍼 대역폭, 정렬 순서가 모두 성능에 영향을 미치며, 각 단계의 원리를 이해해야 병목을 정확히 진단할 수 있습니다.

VSync와 프레임 페이싱이 게임 루프에 미치는 영향은 [게임 루프의 원리 (2)](/dev/unity/GameLoop-2/)에서, TBDR 아키텍처에서 MSAA가 효율적인 구조적 이유는 [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 각각 다루고 있습니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- [래스터화 파이프라인 (1) - 삼각형에서 프래그먼트까지](/dev/unity/RasterPipeline-1/)
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- **래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱** (현재 글)

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
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- **래스터화 파이프라인 (3) - 디스플레이와 안티앨리어싱** (현재 글)
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
