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

[래스터화 파이프라인 (2)](/dev/unity/RasterPipeline-2/)에서는 프래그먼트가 깊이 테스트, 스텐실 테스트, 블렌딩을 거쳐 프레임 버퍼에 기록되는 과정을 살펴봤습니다. 한 프레임의 드로우 콜이 모두 끝나면 프레임 버퍼에는 화면에 표시할 이미지가 완성됩니다.

하지만 프레임 버퍼에 이미지가 완성되었다고 해서 그 이미지가 즉시 화면에 보이는 것은 아닙니다. 디스플레이는 프레임 버퍼 전체를 한 번에 표시하지 않고, 위에서 아래로 한 줄씩 읽어 화면을 갱신합니다. GPU가 새 프레임을 준비하는 시점과 디스플레이가 현재 프레임을 읽는 시점이 어긋나면, 한 화면 안에 서로 다른 두 프레임이 섞이는 **티어링(Tearing)**이 나타날 수 있습니다.

이 문제를 다루기 위해 더블 버퍼링, VSync, 트리플 버퍼링 같은 방법이 쓰입니다. 셋 모두 티어링이나 GPU 대기 시간을 줄이는 대신, 입력 지연, 메모리 사용량, 프레임 페이싱 같은 다른 비용이 따릅니다.

화질 문제는 디스플레이 동기화에만 있지 않습니다. 래스터화는 연속적인 삼각형을 유한한 픽셀 격자로 샘플링하므로, 비스듬한 경계선이 계단 모양으로 보이는 **앨리어싱(Aliasing)**이 생깁니다. 해상도를 높이면 계단은 작아지지만, 유한한 픽셀 격자로 연속적인 경계를 표현한다는 한계는 남습니다.

그래서 계단을 덜 보이게 만드는 **안티앨리어싱(Anti-Aliasing)**이 필요합니다.

이번 글에서는 완성된 프레임이 화면에 닿기까지의 동기화 문제를 먼저 따라가 본 뒤, 래스터화의 표본화 한계를 메우는 안티앨리어싱 기법까지 차례로 살펴봅니다.

---

## 디스플레이 스캔아웃

모니터나 스마트폰 화면은 완성된 프레임 버퍼를 한 번에 통째로 표시하지 않습니다. 프레임 버퍼의 픽셀을 **왼쪽 위부터 오른쪽으로, 한 줄이 끝나면 다음 줄로** 순서대로 읽어 디스플레이에 보냅니다. 이렇게 순차적으로 읽어 화면을 갱신하는 과정을 **스캔아웃(Scanout)**이라고 부릅니다.

이 읽기 순서는 CRT(브라운관) 모니터에서 이어진 방식입니다. CRT에서는 전자빔이 화면을 왼쪽에서 오른쪽으로 한 줄씩 지나가고, 줄이 끝나면 아래 줄로 내려가며 형광체를 발광시켰습니다. 픽셀을 갱신하는 순서가 전자빔의 이동 경로와 같았습니다.

LCD나 OLED는 전자빔을 사용하지 않지만, 디스플레이 컨트롤러가 프레임 버퍼를 읽는 순서는 여전히 비슷한 구조를 따릅니다.

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

디스플레이가 스캔아웃을 초당 반복하는 횟수를 **주사율(Refresh Rate)**이라고 하며, 헤르츠(Hz)로 표시합니다. 60Hz 화면은 초당 60번 전체 화면을 갱신하므로, 한 번의 갱신 주기는 약 16.67ms입니다.

한 번의 갱신 주기는 크게 두 구간으로 나뉩니다. 픽셀 데이터를 실제로 전송하는 **활성 스캔아웃** 구간이 있고, 한 프레임의 스캔이 끝난 뒤 다음 프레임을 다시 읽기 시작하기 전의 짧은 유휴 구간인 **수직 귀선 구간(VBlank, Vertical Blanking Interval)**이 있습니다.

VBlank라는 이름도 CRT에서 왔습니다. 전자빔이 화면 아래까지 내려간 뒤 다시 위로 돌아가는 동안에는 화면을 그리지 않았고, 그 빈 시간이 VBlank였습니다. 지금도 이 구간은 버퍼를 교환하기 좋은 타이밍으로 쓰이며, 뒤에서 다룰 VSync가 이 VBlank를 기준으로 동작합니다.

---

## 티어링

디스플레이는 프레임 버퍼를 위에서 아래로 한 줄씩 읽습니다. 이 스캔아웃이 끝나기 전에 디스플레이가 읽고 있는 버퍼가 새 프레임으로 바뀌면 문제가 생깁니다.

버퍼가 하나뿐이라면 GPU는 디스플레이가 읽는 버퍼에 다음 프레임을 직접 그릴 수밖에 없습니다. 스캔아웃이 화면 중간까지 진행된 시점에 버퍼 내용이 바뀌면, 이미 읽힌 위쪽은 이전 프레임이고 이후 읽히는 아래쪽은 새 프레임이 됩니다. 그 결과 한 화면 안에서 두 프레임이 가로 경계를 기준으로 나뉘어 보입니다.

이렇게 화면이 가로 방향으로 나뉘어 어긋나 보이는 현상을 **티어링(Tearing)**이라고 부릅니다.

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

티어링의 원인은 GPU의 프레임 완성 시점과 디스플레이의 스캔아웃 시점이 서로 동기화되어 있지 않다는 데 있습니다.

한 스캔아웃 안에서 버퍼 내용이 여러 번 바뀌면 티어링 경계도 여러 줄 생길 수 있습니다. 카메라가 빠르게 움직이거나 장면 변화가 큰 경우에는 프레임 간 차이가 커서 경계가 쉽게 보이고, 정적인 화면에서는 두 프레임이 비슷해 경계가 잘 드러나지 않습니다.

---

## 더블 버퍼링

티어링은 디스플레이가 읽는 버퍼와 GPU가 그리는 버퍼가 같을 때 발생합니다. 이를 막기 위해 표시용 버퍼와 렌더링용 버퍼를 분리하는 방식이 **더블 버퍼링(Double Buffering)**입니다. 이름 그대로 프레임 버퍼를 두 개 둡니다.

두 버퍼는 역할이 다릅니다. **프론트 버퍼(Front Buffer)**는 디스플레이가 지금 읽고 있는 버퍼이며, 화면에 표시 중인 프레임을 저장합니다. **백 버퍼(Back Buffer)**는 GPU가 새 프레임을 그리는 버퍼이며, 렌더링이 끝나기 전까지 화면에 표시되지 않습니다.

GPU가 백 버퍼에 한 프레임을 모두 그리면 프론트 버퍼와 백 버퍼의 역할을 바꿉니다. 이 작업을 **교환(Swap)**이라고 부릅니다. 교환은 픽셀 데이터를 복사하는 작업이 아니라, 디스플레이 컨트롤러가 어느 버퍼를 읽을지 가리키는 참조를 바꾸는 작업에 가깝습니다.

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

버퍼가 둘이면 메모리 사용량은 그만큼 늘어납니다. [래스터화 파이프라인 (2)](/dev/unity/RasterPipeline-2/)에서 다룬 RGBA8 Full HD 기준으로 색상 버퍼 한 장이 약 8MB이므로 두 장은 약 16MB입니다. 현대 GPU에서는 대체로 감당 가능한 수준이지만, 모바일에서는 해상도와 버퍼 형식에 따라 여전히 고려할 비용입니다.

메모리 비용을 감수하더라도, 버퍼를 둘로 나누는 것만으로는 티어링이 완전히 사라지지 않습니다. 스캔아웃 도중에 Swap이 일어나면 디스플레이가 읽는 버퍼가 중간에 바뀌고, 다시 한 화면 안에 두 프레임이 섞일 수 있습니다.

따라서 남은 문제는 Swap을 언제 허용할 것인가입니다. 이 시점을 디스플레이 갱신 주기에 맞추는 방식이 VSync입니다.

---

## VSync

**VSync(Vertical Synchronization, 수직 동기화)**는 버퍼 교환을 **VBlank** 구간에 맞춰 실행하는 방식입니다. 디스플레이가 한 화면을 모두 읽고 다음 화면을 읽기 시작하기 전의 짧은 구간에서만 Swap을 허용합니다.

백 버퍼가 먼저 완성되더라도 스캔아웃 중에는 Swap을 보류합니다. 스캔아웃이 끝난 뒤 VBlank에 들어갔을 때만 버퍼를 교환하므로, 하나의 스캔아웃 동안 디스플레이는 같은 프레임만 읽게 됩니다. 그 결과 티어링은 사라집니다.

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

VSync는 티어링을 없애지만, 버퍼 교환을 기다리게 만드는 만큼 몇 가지 비용이 생깁니다.

먼저 **입력 지연(Input Lag)**이 늘어납니다. GPU가 프레임을 다 그려도 다음 VBlank가 오기 전까지는 그 프레임이 화면에 표시되지 않습니다. 프레임 완성 시점과 표시 시점 사이에 최대 한 프레임 주기, 60Hz 기준 약 16.67ms가 더해질 수 있습니다.

그만큼 조작이 화면에 늦게 반영되므로, 빠른 반응이 중요한 게임에서는 이 지연을 체감할 수 있습니다.

다음으로, 프레임 레이트가 디스플레이 갱신 주기에 묶입니다. 교환은 VBlank 구간에서만 가능하므로, 프레임을 다 그린 시점이 두 VBlank 사이에 떨어지면 그다음 VBlank가 올 때까지 기다려야 합니다. 이 때문에 프레임 레이트는 갱신 주기를 정수로 나눈 값으로 제한되어, 60Hz에서는 매 VBlank마다 교환하면 60fps, 두 VBlank마다 교환하면 30fps, 세 VBlank마다 교환하면 20fps가 됩니다.

GPU가 한 프레임을 16.67ms 안에 끝내면 60fps가 그대로 유지되지만, 18ms가 걸리면 바로 다음 VBlank를 놓쳐 그다음 VBlank까지 기다려야 합니다. 그러면 이 프레임의 표시 간격이 33.33ms로 늘어나, 체감 프레임 레이트가 30fps로 떨어집니다.

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

이처럼 프레임 표시 간격이 갑자기 커지는 문제는 프레임 페이싱과 직접 연결됩니다. 60fps를 안정적으로 유지하기 어려운 모바일 게임에서는 목표를 30fps로 낮추고, 대신 프레임 간격을 일정하게 유지하는 전략을 선택하기도 합니다.

> 프레임 페이싱은 [게임 루프의 원리 (2)](/dev/unity/GameLoop-2/)에서 자세히 다룹니다.

Unity에서 VSync는 `QualitySettings.vSyncCount`로 설정합니다. 값을 1로 두면 매 VBlank마다 교환하고, 2로 두면 두 번째 VBlank마다 교환합니다. 60Hz 디스플레이 기준으로 각각 60fps와 30fps에 해당합니다. 0으로 두면 Unity의 VSync 설정은 꺼집니다.

모바일에서는 상황이 다릅니다. Android와 iOS는 여러 앱과 시스템 UI의 화면을 한 장으로 합성하는 운영체제의 컴포지터(Compositor)와 프레임 스케줄링 시스템이 이미 VSync 기반으로 동작합니다. Android의 SurfaceFlinger·Choreographer, iOS의 CADisplayLink가 대표적입니다. 그래서 `vSyncCount`를 0으로 두어도 실제 프레임 제출은 디스플레이 주기에 맞춰지는 경우가 많습니다.

따라서 모바일에서는 `vSyncCount`보다 `Application.targetFrameRate`로 목표 프레임 레이트를 지정하는 쪽이 실질적인 제어 수단에 가깝습니다.

프레임 레이트 고정 문제를 디스플레이 쪽에서 완화하는 기술도 있습니다. **가변 주사율(VRR, Variable Refresh Rate)**은 디스플레이 갱신 주기를 고정하지 않고, GPU가 프레임을 완료하는 시점에 맞춰 주기를 조정합니다. G-Sync, FreeSync, Adaptive Sync가 이 범주에 속합니다.

VRR을 지원하는 환경에서는 VSync에서 생기는 입력 지연과 프레임 레이트 급락이 함께 완화될 수 있습니다. 다만 지원 여부와 동작 범위는 디스플레이, 플랫폼, 그래픽스 API에 따라 달라집니다.

---

## 트리플 버퍼링

VSync를 켠 더블 버퍼링에서는 GPU가 백 버퍼를 완성한 뒤 다음 VBlank까지 기다릴 수 있습니다. 백 버퍼가 하나뿐이라, 그 버퍼가 프론트 버퍼로 교환되기 전에는 다음 프레임을 그릴 공간이 없기 때문입니다. 이 대기 시간을 줄이기 위해 백 버퍼를 하나 더 두는 방식이 **트리플 버퍼링(Triple Buffering)**입니다.

트리플 버퍼링에서는 프론트 버퍼 1개와 백 버퍼 2개를 사용합니다. GPU가 한 백 버퍼에 프레임을 완성하면, 그 버퍼가 VBlank에서 표시되기를 기다리는 동안 다른 백 버퍼에 다음 프레임을 그릴 수 있습니다. 빈 백 버퍼가 하나 더 있으므로 GPU가 대기하는 시간이 줄어듭니다.

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

버퍼를 하나 더 두면 두 가지 이점이 있습니다.

먼저 GPU 활용률이 올라갑니다. VBlank를 기다리며 멈추는 대신 빈 백 버퍼에 다음 프레임을 그릴 수 있으므로, 더블 버퍼링에서 생기던 대기 시간이 줄어듭니다.

둘째, 프레임 레이트가 60fps에서 곧바로 30fps로 떨어지는 상황을 완화할 수 있습니다. 예를 들어 60Hz에서 한 프레임이 18ms 걸리면 더블 버퍼링에서는 다음 VBlank를 놓쳐 30fps로 내려갈 수 있습니다.
트리플 버퍼링에서는 GPU가 계속 다음 프레임을 그리므로 처리량은 약 55fps(1000/18ms)에 가깝게 유지될 수 있습니다. 디스플레이는 60Hz로 동작하지만, VBlank마다 가장 최근에 완성된 프레임을 표시할 수 있으므로 더 많은 갱신 시점에 새 프레임을 올릴 수 있습니다. 다만 GPU 처리량과 디스플레이 주기가 정확히 맞지 않으면 같은 프레임이 두 번 표시되는 미세한 끊김이 생길 수 있습니다.

대신 입력 지연이 늘 수 있습니다. 백 버퍼가 하나 더 있으면 화면에 표시 중인 프레임과 GPU가 현재 그리는 프레임 사이의 간격이 더블 버퍼링보다 커질 수 있습니다. 사용자의 입력이 화면에 반영되기까지 최대 한 프레임 정도 더 걸릴 수 있다는 뜻입니다.

다만 실제 지연은 완성된 프레임을 화면에 올리는 방식, 즉 프레젠트 모드에 따라 달라집니다. VBlank마다 가장 최근에 완성된 백 버퍼만 표시하고 나머지는 버리는 **mailbox** 계열에서는 지연이 거의 늘지 않습니다. 반면 완성된 프레임을 큐에 쌓아 순서대로 표시하는 **render-ahead** 계열에서는 오래된 프레임이 먼저 나가 그만큼 지연이 커집니다.

GPU 메모리도 더 필요합니다. 색상 버퍼가 2개에서 3개로 늘어나므로, Full HD RGBA8 기준으로 약 8MB가 추가됩니다. 모바일에서는 해상도와 HDR 형식에 따라 이 비용이 더 커질 수 있습니다.

트리플 버퍼링은 Unity에서 직접 켜고 끄는 설정이 아니라, 플랫폼과 그래픽스 API, 운영체제의 프레젠트 방식이 함께 결정합니다. 특히 Android와 iOS에서는 운영체제의 컴포지터가 화면을 합성하면서 이미 여러 버퍼를 사용하므로, 트리플 버퍼링도 앱이 아니라 운영체제 차원에서 다뤄집니다.

---

## 앨리어싱

디스플레이 동기화로 티어링 없이 프레임을 내보내더라도, 그 프레임 자체의 화질은 렌더링 단계에서 이미 제한됩니다.

매끄러운 삼각형 가장자리를 유한한 픽셀 격자에 맞춰 표현하면, 비스듬한 경계선이 계단 모양으로 보입니다. 이렇게 연속적인 도형을 이산적인 격자로 샘플링할 때 생기는 왜곡을 **앨리어싱(Aliasing)**이라고 하며, 톱니처럼 보이는 가장자리를 **jaggies**라고 부릅니다.

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

계단이 생기는 근본 원인은 **샘플링 자체의 한계**입니다. 연속적인 대상을 일정한 간격의 샘플로 표현하는 한, 샘플 간격보다 더 세밀한 변화는 정확히 복원할 수 없습니다.

이 한계를 신호 처리 이론에서 설명하는 것이 **나이퀴스트 정리(Nyquist Theorem)**입니다. 연속 신호를 이산 샘플로 정확히 복원하려면, 샘플링 주파수가 원래 신호의 최대 주파수의 2배 이상이어야 합니다. 이 조건을 만족하지 못하면 원래 신호에는 없던 가짜 패턴, 즉 앨리어스가 결과에 섞입니다.

래스터화도 같은 관점에서 볼 수 있습니다. 연속적인 장면을 픽셀 격자 위의 샘플로 표현하는 **공간적 샘플링**입니다. 여기서 샘플링 주파수는 픽셀이 얼마나 촘촘한지, 즉 해상도에 해당합니다. 신호의 주파수는 화면에서 색이나 밝기가 얼마나 짧은 거리 안에 바뀌는지를 뜻하는 **공간 주파수**에 해당합니다.

공간 주파수는 장면의 부분마다 다릅니다. 넓은 하늘처럼 색이 천천히 변하는 영역은 공간 주파수가 낮습니다. 체크무늬 바닥, 얇은 선, 삼각형 가장자리처럼 색이 짧은 거리 안에서 급격히 바뀌는 영역은 공간 주파수가 높습니다.

삼각형 가장자리는 특히 문제가 큽니다. 삼각형 안쪽과 바깥쪽이 한 경계에서 불연속적으로 바뀌기 때문에, 이론적으로 공간 주파수가 무한히 높습니다. 어떤 유한한 해상도도 이런 불연속 경계를 완전히 정확하게 샘플링할 수는 없습니다.

그래서 해상도를 올려도 앨리어싱이 완전히 사라지지는 않습니다. 픽셀이 촘촘해지면 계단의 크기는 작아지고 눈에 덜 띄지만, 유한한 샘플로 불연속 경계를 표현한다는 한계는 남습니다.

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

해상도를 올리면 프래그먼트 수와 메모리 대역폭이 함께 늘어나므로, 화질을 위해 무작정 높일 수만은 없습니다.

---

## 안티앨리어싱 기법들

표본화의 한계로 생기는 계단 현상을 줄이는 보정 기법을 통틀어 안티앨리어싱이라고 부릅니다.

안티앨리어싱 기법은 가장자리를 어디서, 무엇으로 다듬느냐에 따라 달라집니다. MSAA는 래스터화 단계에서 픽셀마다 표본을 더 찍고, FXAA와 SMAA는 완성된 이미지의 가장자리를 후처리로 분석해 다듬으며, TAA는 여러 프레임에 걸쳐 표본을 누적합니다. 여기서는 이 네 기법을 차례로 살펴봅니다.

### MSAA (Multi-Sample Anti-Aliasing)

MSAA는 한 픽셀 안에 **서브 샘플(Sub-sample)**이라 부르는 표본 위치를 여러 개 두는 하드웨어 안티앨리어싱입니다. 삼각형이 픽셀을 얼마나 덮는지 판정할 때, 픽셀 중심 한 곳만 보지 않고 이 서브 샘플 각각이 삼각형 안에 들어오는지를 따로 확인합니다. 가장자리가 픽셀을 가로지르면 서브 샘플 가운데 일부만 삼각형에 덮이는데, 그중 몇 개가 덮였는지를 래스터화 단계에서 세어 둡니다. 이렇게 구한 덮인 비율을 **커버리지(Coverage)**라고 하며, 2x·4x·8x는 픽셀마다 두는 서브 샘플의 개수를 뜻합니다.

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

커버리지는 이렇게 서브 샘플 단위로 구하지만, 정작 색을 만드는 **프래그먼트 셰이더는 보통 픽셀당 한 번만 실행됩니다**. 서브 샘플마다 따로 계산되는 값은 커버리지와 깊이, 스텐실뿐입니다. 셰이더가 만든 하나의 색은 삼각형이 덮은 서브 샘플에만 기록되고, 덮지 않은 서브 샘플에는 기존 색이 그대로 남습니다. 출력할 픽셀 색을 정할 때는 이 서브 샘플 값들을 평균해 하나로 합치는데, 이 단계를 **리졸브(Resolve)**라고 합니다. 가장자리 픽셀에서는 삼각형 색과 배경색이 커버리지 비율만큼 섞여, 완전히 켜지거나 꺼지는 대신 중간색을 띱니다. 계단이 부드러워지는 것은 이 때문입니다.

가장자리에서 색이 섞이려면 서브 샘플 가운데 일부만 삼각형에 덮여야 합니다. 면 안쪽 픽셀은 사정이 다릅니다. 삼각형 경계가 걸치지 않아 모든 서브 샘플이 빠짐없이 삼각형에 덮이므로, 커버리지는 늘 가득 차고 섞을 색도 생기지 않습니다. 즉 MSAA가 보는 것은 삼각형이 픽셀을 얼마나 덮느냐일 뿐, 그 안에서 색이 어떻게 달라지는지가 아닙니다. 따라서 MSAA가 다듬어 주는 대상은 삼각형의 윤곽선에 한정됩니다.

면 안쪽의 색이 한결같다는 뜻은 아닙니다. 한 픽셀보다 잘게 변하는 색은 면 안쪽에도 얼마든지 있는데, MSAA는 이 색을 픽셀당 한 번만 계산하므로 그 변화를 담아내지 못합니다. 그래서 촘촘한 텍스처에는 모아레가 어른거리고, 좁은 스페큘러 하이라이트는 카메라가 조금만 움직여도 프레임마다 깜박입니다. 이것은 가장자리가 아니라 색 자체에서 생기는 앨리어싱이라, 커버리지만 다루는 MSAA로는 서브 샘플을 아무리 늘려도 줄지 않습니다.

MSAA의 비용은 두 곳에서 나옵니다. 색을 계산하는 셰이더 연산과, 그 결과를 메모리로 실어 나르는 대역폭입니다. 연산 쪽부터 보면 이 부담은 생각보다 가볍습니다. 앞서 설명한 대로 MSAA에서 셰이더는 픽셀당 한 번만 실행되기 때문입니다. 같은 목적의 **SSAA(Super-Sample Anti-Aliasing)**는 서브 샘플마다 셰이더를 실행해 4x에서는 셰이더 비용이 이론상 네 배가 되지만, MSAA는 커버리지만 서브 샘플별로 따로 구하고 색은 한 번만 계산하므로 셰이더 비용이 거의 그대로입니다.

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
  <text x="300" y="428" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">가장자리에서만 중간색이 생기므로 부드러운 경계 표현</text>
</svg>
</div>

연산이 이렇게 가벼운 대신, MSAA에서 실제로 부담이 되는 쪽은 대역폭입니다. 서브 샘플 수만큼 불어난 데이터를 메모리로 실어 나르는 일이 비용의 핵심이고, 이 부담이 얼마나 커지는지는 데이터가 머무는 위치, 곧 GPU 아키텍처에 따라 달라집니다.

GPU 곁에 붙은 온칩(on-chip) 메모리는 접근이 빠른 대신 용량이 작고, 화면을 통째로 담는 외부 메모리는 용량이 크지만 멀리 있어 데이터를 주고받는 데 시간과 전력이 더 듭니다. 그래서 아껴야 하는 것은 외부 메모리를 오가는 데이터의 양, 곧 대역폭입니다. 모바일 GPU가 주로 쓰는 **TBDR(Tile-Based Deferred Rendering)** 아키텍처는 화면을 작은 타일로 나눠 온칩 메모리에서 한 타일씩 그립니다. 늘어난 서브 샘플 데이터도 이 온칩에 머물다가, 리졸브로 하나의 색으로 합쳐진 뒤 최종 색만 외부 메모리로 나갑니다. 서브 샘플이 외부 메모리를 오가지 않으니 4x MSAA를 켜도 대역폭은 거의 늘지 않습니다. 반면 데스크톱 GPU에서 흔한 **IMR(Immediate Mode Rendering)** 방식은 서브 샘플 데이터를 외부 메모리에 그대로 저장하므로, 오가는 데이터가 샘플 수만큼 늘어 대역폭 비용도 그에 비례해 커집니다.

> TBDR이 타일을 온칩에서 처리하는 방식은 [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 자세히 다룹니다.

물론 TBDR에서도 비용이 아주 없지는 않습니다. 온칩 타일 메모리 사용량은 서브 샘플 수에 비례해 늘고, 리졸브에도 추가 연산이 듭니다. 타일 메모리가 커진 만큼 GPU에 따라 한 번에 처리하는 타일 크기가 줄기도 합니다. 그래도 대역폭에서 얻는 이점이 이 비용을 넘어서기 때문에, TBDR 기반 모바일에서는 MSAA가 첫 번째 선택지가 되는 경우가 많습니다.

Unity URP에서는 렌더 파이프라인 에셋의 Quality 설정에서 MSAA를 켜고 단계를 정합니다. 모바일에서는 보통 2x나 4x를 먼저 검토합니다.

다만 후처리(Post-Processing)와 함께 쓸 때는 한 가지 유의할 점이 있습니다. 후처리 효과는 렌더링된 화면을 텍스처로 읽어 가공하는데, 서브 샘플이 그대로 남아 있는 MSAA 버퍼는 이 상태로 일반 텍스처처럼 읽을 수 없습니다. 그래서 URP은 후처리 앞에 MSAA 버퍼를 하나로 합치는 리졸브 패스를 자동으로 넣습니다. 이 리졸브로 서브 샘플 정보가 사라지므로, 블룸이나 톤매핑처럼 그 뒤에 적용되는 후처리에는 MSAA의 가장자리 정보가 반영되지 않습니다.

### FXAA (Fast Approximate Anti-Aliasing)

FXAA는 래스터화에는 개입하지 않고, 렌더링이 끝난 최종 이미지를 다듬는 **후처리 기반** 안티앨리어싱입니다. 픽셀마다 커버리지를 따로 구하던 MSAA와 달리, FXAA는 삼각형이나 깊이 같은 장면의 기하 정보를 전혀 참고하지 않습니다.

그 대신 화면에 이미 그려진 색에서 밝기 성분인 **휘도(Luma)**를 추출하여, 휘도가 급격히 변하는 자리를 경계로 판정합니다. 그렇게 찾은 경계 부근만 주변 픽셀과 부드럽게 섞어 계단을 누그러뜨립니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 760 315" xmlns="http://www.w3.org/2000/svg" style="max-width: 760px; width: 100%;">
  <!-- background -->
  <rect x="0" y="0" width="760" height="315" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- title -->
  <text x="380" y="28" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">FXAA의 동작 원리</text>

  <!-- Step 1: 경계 검출 -->
  <rect x="20" y="50" width="220" height="220" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">1단계: 경계 검출</text>
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
  <text x="130" y="228" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">→ 경계 후보</text>

  <!-- Arrow 1→2 -->
  <line x1="248" y1="160" x2="278" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="284,160 274,155 274,165" fill="currentColor"/>

  <!-- Step 2: 경계 방향 분석 -->
  <rect x="290" y="50" width="180" height="220" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="380" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">2단계: 경계 방향 분석</text>
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
  <text x="380" y="168" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" font-weight="bold">경계 방향: 수평</text>
  <!-- Caption -->
  <text x="380" y="205" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">주변 대비를 비교해</text>
  <text x="380" y="218" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">경계가 뻗어가는 방향을 근사</text>

  <!-- Arrow 2→3 -->
  <line x1="478" y1="160" x2="508" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="514,160 504,155 504,165" fill="currentColor"/>

  <!-- Step 3: 경계 방향 블렌딩 -->
  <rect x="520" y="50" width="220" height="220" rx="4" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="630" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">3단계: 경계 방향 블렌딩</text>
  <text x="630" y="95" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">경계 방향으로 여러 지점 샘플링</text>
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
  <text x="630" y="240" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">가중 혼합 → 경계만 부드럽게</text>
  <text x="630" y="254" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(전체 블러가 아닌 경계 맞춤 필터링)</text>

  <!-- bottom note -->
  <text x="380" y="286" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">후처리라 기하 정보 없이 이미지 휘도 대비로만 경계 추정 (풀스크린 1패스)</text>
  <text x="380" y="302" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">→ 경계가 아닌 디테일도 뭉개져 선명도가 일부 감소할 수 있음</text>
</svg>
</div>

이렇게 완성된 이미지 한 장만 처리하므로 FXAA는 비용이 낮습니다. 화면 전체를 한 차례 훑는 풀스크린 후처리 한 패스로 끝나기 때문에, 비용은 주로 화면 해상도에 비례할 뿐 삼각형 수나 장면의 복잡도와는 거의 무관합니다.

비용이 낮다는 점과 함께 살펴야 할 것이 보정 범위입니다. 경계를 휘도 하나로만 가려내기 때문에, 그 범위는 삼각형 가장자리에 머물지 않습니다. 텍스처의 무늬든 셰이더가 만들어 낸 고대비 경계든, 화면에서 밝기가 가파르게 달라지는 자리라면 출처를 가리지 않고 모두 보정 대상이 됩니다. 커버리지만 보던 MSAA로는 다루지 못하던 자리까지 함께 누그러지는 것은 이 때문입니다.

출처를 가리지 않는다는 바로 그 점이 선명도에는 손해가 됩니다. 휘도 대비만 볼 뿐 기하 정보가 없으니, FXAA는 실제 물체의 경계와 또렷하게 그려 넣은 무늬를 가려내지 못합니다. 그래서 흐려져서는 안 될 글자나 UI의 가는 선, 텍스처의 미세한 무늬까지 경계로 오인해 함께 뭉개기도 합니다.

이러한 장단점 때문에, 어느 기법이 알맞은지는 환경에 따라 달라집니다. 모바일에서는 FXAA보다 MSAA를 먼저 검토하는 경우가 많습니다. 앞서 설명한 대로 TBDR 기반 GPU에서는 MSAA의 대역폭 비용이 낮게 유지되는 반면, FXAA에서는 텍스처 디테일이 흐려지는 손실이 더 두드러지기 때문입니다. 반대로 이미 후처리 파이프라인을 거치고 있거나 MSAA를 적용하기 어려운 환경이라면, 패스 하나로 끝나는 FXAA가 가벼운 대안이 됩니다.

### TAA (Temporal Anti-Aliasing)

MSAA와 FXAA가 한 프레임 안에서 문제를 해결하려는 방식이라면, TAA는 여러 프레임의 정보를 누적해 사용하는 **시간적(Temporal)** 안티앨리어싱입니다.

출발점은 **지터링(Jittering)**입니다. 프레임마다 카메라의 투영 행렬에 서브 픽셀 크기의 작은 오프셋을 더하면, 장면이 화면에서 1픽셀보다 작은 거리만큼 이동한 것처럼 샘플링됩니다. 그러면 삼각형 가장자리가 픽셀 격자와 만나는 위치도 프레임마다 조금씩 달라집니다.

TAA는 이렇게 서로 다른 서브 픽셀 위치에서 얻은 결과를 여러 프레임에 걸쳐 누적합니다. 한 프레임에서는 샘플 수가 부족해도, 시간 축으로 여러 샘플을 모으면 더 매끄러운 가장자리를 만들 수 있습니다.

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

샘플을 한 프레임에 몰지 않고 시간 축에 나누어 모으기 때문에, TAA는 프레임당 샘플 수를 크게 늘리지 않고도 품질을 높일 수 있습니다. 삼각형 가장자리는 물론, 셰이더 앨리어싱이나 스페큘러 하이라이트의 깜박임처럼 프레임마다 흔들리는 요소까지 누그러뜨립니다.

하지만 여러 프레임을 누적하기 때문에 생기는 약점도 있습니다. 대표적인 문제가 **고스팅(Ghosting)**과 **흐려짐**입니다.

고스팅은 빠르게 움직이는 오브젝트 뒤로 이전 프레임의 잔상이 따라붙는 현상입니다. 이런 잔상이 생기는 이유는 TAA가 이전 프레임까지 누적한 히스토리를 현재 프레임에 다시 쓰기 때문입니다. 오브젝트나 카메라가 움직이면 같은 대상이라도 화면에 맺히는 위치가 프레임마다 달라지는데, 화면 좌표가 같다는 이유로 이전 색을 그대로 누적하면 이미 옮겨 간 위치와 어긋난 색이 남아 잔상처럼 번집니다.

이 어긋남을 바로잡으려면 누적해 둔 히스토리를 대상이 옮겨 간 위치까지 따라가게 해야 합니다. 이렇게 이전 프레임의 픽셀을 현재 프레임의 좌표로 옮기는 과정이 **재투영(Reprojection)**이고, 그 좌표를 알려 주는 정보가 **모션 벡터(Motion Vector)**입니다. 모션 벡터는 각 픽셀이 이전 프레임에서 현재 프레임으로 얼마나 이동했는지 기록하며, TAA는 이를 따라 히스토리 값을 현재 위치에서 끌어옵니다.

그래도 모든 어긋남이 사라지지는 않습니다. 이전 프레임에서는 다른 오브젝트에 가려져 있다가 현재 프레임에서 새로 드러난 영역(disocclusion)은 끌어올 과거 데이터가 없습니다. 이런 영역에서는 잘못된 히스토리가 섞이거나, 히스토리를 버리면서 노이즈가 생기기도 합니다.

두 번째 약점인 흐려짐은 여러 프레임을 평균하는 과정에서 생깁니다. 카메라가 정지해 있으면 샘플이 안정적으로 누적되지만, 카메라나 오브젝트가 움직이는 동안에는 누적된 히스토리가 현재 프레임과 완전히 맞지 않아 이미지가 부드럽지만 흐릿하게 보일 수 있습니다.

그래서 TAA 뒤에는 보통 **샤프닝(Sharpening) 패스**를 추가해 선명도를 보정합니다. Unity URP의 TAA도 샤프닝 옵션을 함께 제공합니다.

TAA는 데스크톱과 콘솔에서 두루 쓰이며, Unity URP에서도 카메라 컴포넌트의 Anti-aliasing 설정에서 TAA를 선택할 수 있습니다.

모바일에서도 사용할 수 있지만, 모션 벡터 생성과 히스토리 버퍼 저장이 필요합니다. 메모리와 대역폭, 후처리 비용을 실제 기기에서 확인해야 합니다.

### SMAA (Subpixel Morphological Anti-Aliasing)

SMAA도 FXAA처럼 최종 이미지를 대상으로 하는 후처리 기반 안티앨리어싱입니다. 다만 경계를 찾고 보정하는 방식이 더 정교합니다.

FXAA가 인접 픽셀의 밝기 차이만으로 경계를 추정한다면, SMAA는 검출한 경계가 어떤 **형태(morphology)**를 띠는지까지 분석합니다. 경계가 어느 방향으로 이어지는지, L자나 Z자 같은 패턴을 이루는지 판단한 뒤, 그 형태에 맞춰 픽셀마다 적용할 블렌딩 가중치를 계산합니다.

이렇게 윤곽의 생김새를 따라 색을 섞기 때문에, SMAA는 밝기만 보고 뭉뚱그리던 FXAA보다 가장자리를 또렷하게 남기고 흐려짐도 적은 편입니다. 대신 경계 검출, 블렌딩 가중치 계산, 최종 블렌딩의 세 단계 패스로 나뉘므로 비용은 FXAA보다 높습니다.

Unity URP에서는 카메라 컴포넌트의 Anti-aliasing 설정에서 SMAA를 선택할 수 있고, Low·Medium·High의 품질 단계를 함께 지정합니다.

### 안티앨리어싱 기법 비교

네 기법의 가장 큰 차이는 앨리어싱을 어디서 다루느냐에 있습니다. MSAA는 래스터화 단계에서 삼각형 가장자리만 직접 처리해 흐려짐이 없는 대신 셰이더가 만든 경계는 잡지 못하고, 나머지 셋은 완성된 이미지를 손봐 그런 경계까지 다루는 대신 흐려짐을 어느 정도 감수합니다. 지금까지 살펴본 내용을 표로 정리하면 다음과 같습니다.

| | MSAA | FXAA | TAA | SMAA |
|---|---|---|---|---|
| 유형 | 하드웨어 (래스터화 단계) | 후처리 (이미지 기반) | 시간적 (프레임 누적) | 후처리 (형태 분석) |
| 작동 위치 | 래스터화 | 최종 이미지 (1 패스) | 최종 이미지 (1 패스 + 히스토리) | 최종 이미지 (3 패스) |
| 가장자리 품질 | 좋음 (기하 정보 기반) | 보통 (밝기 차이 기반) | 좋음 (서브 픽셀 누적) | 좋음 (형태 기반 분석) |
| 셰이더 앨리어싱 | 효과 없음 (커버리지만) | 효과 있음 (모든 경계) | 효과 있음 (모든 경계) | 효과 있음 (모든 경계) |
| 흐려짐 | 없음 | 있음 | 있음 (움직임) | 적음 |
| 비용 | TBDR에서 낮음 / IMR에서 중간 | 낮음 | 중간 | 중간~높음 |
| 모바일 적합도 | 권장 (TBDR 이점) | 대안 (비용 낮음) | 조건부 사용 (메모리 비용) | 제한적 (패스 비용) |

선택 기준은 대상 플랫폼과 문제의 종류입니다. TBDR 기반 모바일에서는 MSAA의 대역폭 비용이 낮은 편이므로 **MSAA 2x 또는 4x를 먼저 검토**할 만합니다. 셰이더 앨리어싱이나 텍스처 내부의 고주파 패턴까지 줄여야 한다면 FXAA, SMAA, TAA 같은 후처리 기반 기법이 후보가 됩니다.
셋 중에서는 비용을 가장 아끼려면 FXAA, 흐려짐을 더 줄이려면 SMAA, 모션 벡터와 히스토리 버퍼를 감당할 수 있고 움직이는 장면의 시간적 안정성까지 얻으려면 TAA가 적합합니다.
어느 쪽이든 최종 선택은 실제 기기에서 품질과 프레임 시간을 직접 재 보고 결정하는 것이 가장 안전합니다.

---

## 마무리

이번 글에서는 완성된 프레임이 디스플레이에 표시되는 과정과, 래스터화의 샘플링 한계로 생기는 앨리어싱을 줄이는 방법을 정리했습니다. 핵심은 다음과 같습니다.

- **스캔아웃**은 프레임 버퍼를 왼쪽 위부터 한 줄씩 읽어 디스플레이로 보내는 과정입니다. 한 프레임의 스캔이 끝난 뒤 다음 스캔이 시작되기 전의 짧은 구간이 **VBlank**입니다.
- **티어링**은 스캔아웃 도중 버퍼가 교환되어 한 화면에 서로 다른 프레임이 섞이는 현상입니다.
- **더블 버퍼링**은 프론트 버퍼와 백 버퍼를 분리해 렌더링 중인 프레임이 화면에 직접 노출되지 않도록 합니다.
- **VSync**는 버퍼 교환을 VBlank에 맞춰 티어링을 막습니다. 대신 입력 지연이 늘 수 있고, 프레임 시간이 VBlank 간격을 넘기면 60fps에서 30fps처럼 표시 간격이 크게 늘어날 수 있습니다.
- **트리플 버퍼링**은 백 버퍼를 하나 더 두어 GPU 대기 시간을 줄입니다. 대신 메모리 사용량이 늘고, 프레젠트 방식에 따라 입력 지연이 더 커질 수 있습니다.
- **앨리어싱**은 연속적인 도형을 유한한 픽셀 격자로 샘플링할 때 생기는 계단 현상입니다. 해상도를 높이면 줄어들지만 완전히 사라지지는 않습니다.
- **나이퀴스트 정리**는 샘플링 주파수가 신호의 최대 주파수보다 충분히 높아야 한다는 기준을 제시합니다. 삼각형 경계처럼 불연속적인 영역은 유한한 픽셀 격자로 완벽히 복원할 수 없으므로 안티앨리어싱이 필요합니다.
- **MSAA**는 픽셀 안의 여러 서브 샘플로 커버리지를 계산해 삼각형 가장자리를 부드럽게 만듭니다. TBDR 기반 모바일에서는 대역폭 비용이 낮을 수 있어 먼저 검토할 만한 기법입니다.
- **FXAA**는 최종 이미지의 대비를 보고 경계를 부드럽게 만드는 후처리 기법입니다. 비용은 낮지만 텍스트나 텍스처 디테일이 흐려질 수 있습니다.
- **SMAA**는 후처리 기반이면서도 경계의 형태까지 분석해 FXAA보다 선명한 결과를 냅니다. 대신 여러 패스를 거치므로 비용이 더 높습니다.
- **TAA**는 프레임마다 서브 픽셀 위치를 바꾸고 이전 프레임을 누적해 품질을 높입니다. 셰이더 앨리어싱에도 효과가 있지만, 고스팅과 흐려짐을 관리해야 합니다.

이 글이 다룬 두 문제는 모두 디스플레이가 공간과 시간 양쪽에서 잘게 나뉘어 있다는 데서 비롯됩니다. 화면은 픽셀이라는 격자로 공간을 나누고, 갱신 주기라는 간격으로 시간을 나눕니다. 픽셀 격자로 샘플링하는 데서 생기는 계단은 안티앨리어싱이, 갱신 주기와 어긋나 생기는 티어링은 VSync와 버퍼링이 다룹니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

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
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
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
