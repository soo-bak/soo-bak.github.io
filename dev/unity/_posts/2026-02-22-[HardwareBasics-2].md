---
layout: single
title: "하드웨어 기초 (2) - 메모리 계층 구조 - soo:bak"
date: "2026-02-22 01:05:00 +0900"
description: 레지스터, L1/L2/L3 캐시, DRAM, 메모리 계층 피라미드, 캐시 라인, 지역성, 접근 패턴을 설명합니다.
tags:
  - Unity
  - 하드웨어
  - 메모리
  - 캐시
  - 모바일
---

## 연산 속도와 메모리 속도의 격차

[하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)에서 CPU가 명령어를 여러 단계(Fetch → Decode → Execute → Memory → Writeback)로 나누어 처리하는 파이프라인 구조를 다루었습니다.

파이프라인이 매 클럭마다 명령어를 하나씩 완료하려면, 각 단계에서 필요한 데이터가 즉시 준비되어야 합니다. 3 GHz CPU에서 단순 연산 한 건은 1클럭(약 0.33 ns)이면 끝나지만, 그 연산에 필요한 데이터가 DRAM(메인 메모리)에 있으면 가져오는 데 약 100 ns, 즉 200~300 클럭이 소요됩니다.

그 동안 파이프라인은 데이터가 도착할 때까지 진행하지 못하고 대기합니다.

<br>

CPU 설계자들은 이 격차를 메우기 위해 메모리를 단일 장치가 아닌 **계층 구조**로 설계했습니다. 빠르지만 작은 메모리를 CPU 가까이에 두고, 느리지만 큰 메모리를 멀리 배치하는 방식입니다. 이 글에서는 메모리 계층 구조의 동작 원리와, 게임에서 데이터 접근 순서가 성능에 미치는 영향을 다룹니다.

<br>

---

## 메모리 계층 피라미드

메모리 계층은 피라미드로 나타낼 수 있습니다. 꼭대기에 가까울수록 빠르고 용량이 작으며, 아래로 내려갈수록 느리고 용량이 커집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">메모리 계층 피라미드</text>
  <polygon points="240,42 320,42 332,72 228,72" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">레지스터</text>
  <polygon points="228,72 332,72 348,102 212,102" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="91" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L1 캐시</text>
  <polygon points="212,102 348,102 372,138 188,138" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L2 캐시</text>
  <polygon points="188,138 372,138 404,178 156,178" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="161" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L3 캐시</text>
  <polygon points="156,178 404,178 444,222 116,222" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="204" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DRAM (메인 메모리)</text>
  <text x="450" y="60" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">~0.3 ns · 수백 B ~ 수 KB</text>
  <text x="450" y="91" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">~1 ns · 32 ~ 64 KB (코어당)</text>
  <text x="450" y="123" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">~5 ns · 256 KB ~ 1 MB (코어당)</text>
  <text x="450" y="161" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">~15 ns · 4 ~ 64 MB (공유)</text>
  <text x="450" y="204" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">~100 ns · 4 ~ 64 GB</text>
  <line x1="60" y1="60" x2="60" y2="200" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <polygon points="60,55 56,65 64,65" fill="currentColor" opacity="0.6"/>
  <polygon points="60,205 56,195 64,195" fill="currentColor" opacity="0.6"/>
  <text x="74" y="80" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">위로 갈수록</text>
  <text x="74" y="94" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">빠르고 · 작고 · 비쌈</text>
  <text x="74" y="172" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">아래로 갈수록</text>
  <text x="74" y="186" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">느리고 · 크고 · 저렴함</text>
  <text x="300" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">꼭대기에 가까울수록 빠르고 용량이 작고, 아래로 내려갈수록 느리고 용량이 큼</text>
</svg>
</div>

<br>

레지스터의 접근 시간을 1로 놓으면, L1은 약 3배, L2는 약 17배, L3는 약 50배, DRAM은 약 300배 느립니다. CPU 입장에서 레지스터는 손에 들고 있는 메모지, DRAM은 건물 밖 창고에 해당하는 거리감입니다. 이 격차 때문에, 데이터가 어느 계층에 위치하느냐가 연산 속도를 직접 결정합니다.

<br>

용량과 속도가 반비례하는 이유는 물리적 제약에 있습니다. 캐시에 사용되는 SRAM(Static RAM)은 1비트를 저장하는 데 트랜지스터 6개로 구성된 피드백 회로를 사용합니다. 트랜지스터끼리 서로의 상태를 유지해 주므로 전원이 켜져 있는 한 값이 사라지지 않고, 읽는 즉시 결과가 나옵니다. 대신 1비트당 트랜지스터 6개가 필요하므로 같은 칩 면적에 저장할 수 있는 양이 적고, 발열과 제조 비용도 높습니다.

DRAM은 트랜지스터 1개와 커패시터(전하를 저장하는 소자) 1개로 1비트를 저장합니다. 소자가 적으므로 같은 면적에 훨씬 많은 비트를 넣을 수 있어 대용량에 유리합니다. 하지만 커패시터의 전하는 시간이 지나면 빠져나가므로, 주기적으로 다시 채워야 하고(리프레시), 읽을 때 전하가 소멸되어 다시 써야 하는 과정도 필요합니다. 이 추가 과정 때문에 SRAM보다 접근 시간이 깁니다.

CPU 코어 바로 옆에 DRAM 크기의 SRAM을 배치하는 것은 물리적으로 불가능하므로, 빠르고 작은 메모리와 느리고 큰 메모리를 계층으로 조합하는 구조가 됩니다.

<br>

아래에서는 피라미드의 각 계층이 어떤 역할을 하는지 구체적으로 다룹니다.

---

## 레지스터

레지스터는 CPU 코어 내부에 있는 가장 빠른 저장 공간으로, [이전 글](/dev/unity/HardwareBasics-1/)에서 "연산에 필요한 데이터를 임시로 보관하는 초고속 저장 공간"으로 소개한 바 있습니다.

메모리 계층 피라미드에서 꼭대기에 위치하며, 속도와 용량 양쪽에서 가장 극단적인 특성을 갖습니다.

<br>

레지스터의 주된 용도는 ALU(산술 논리 연산 장치)가 연산할 때 피연산자를 읽어오고 결과를 기록하는 것입니다. 연산용 레지스터 외에, CPU 제어를 위한 레지스터도 있습니다. [이전 글](/dev/unity/HardwareBasics-1/)에서 다룬 프로그램 카운터(PC)는 다음에 실행할 명령어의 주소를 추적하고, 스택 포인터(SP)는 함수 호출 시 복귀 주소와 지역 변수가 쌓이는 스택 영역의 현재 위치를 가리킵니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">레지스터의 위치</text>
  <rect x="20" y="38" width="480" height="180" rx="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU 코어</text>
  <rect x="50" y="78" width="160" height="120" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="98" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">레지스터</text>
  <text x="70" y="124" font-family="monospace" font-size="11" fill="currentColor">r0: 42</text>
  <text x="70" y="142" font-family="monospace" font-size="11" fill="currentColor">r1: 17</text>
  <text x="70" y="160" font-family="monospace" font-size="11" fill="currentColor">r2: 0</text>
  <text x="70" y="178" font-family="monospace" font-size="11" fill="currentColor">…</text>
  <line x1="210" y1="125" x2="290" y2="125" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="290,125 282,121 282,129" fill="currentColor"/>
  <polygon points="210,125 218,121 218,129" fill="currentColor"/>
  <rect x="290" y="98" width="160" height="50" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="370" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">ALU</text>
  <text x="370" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">연산기</text>
  <text x="290" y="170" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">연산 예시:</text>
  <text x="290" y="188" font-family="monospace" font-size="11" fill="currentColor">ADD r2, r0, r1</text>
  <text x="298" y="204" font-family="monospace" font-size="10" fill="currentColor" opacity="0.85">→ r2 = 42 + 17 = 59</text>
</svg>
</div>

<br>

레지스터는 ALU와 같은 실리콘 위에 플립플롭(클럭 신호에 맞춰 1비트를 저장하는 소자) 회로로 구현되어 있어, 배선 지연 없이 ALU와 직접 값을 주고받습니다. 접근 시간이 약 0.3 나노초로, 한 클럭 사이클 안에 읽고 쓸 수 있습니다. 

대신 플립플롭 하나가 1비트만 저장하므로 용량이 극히 작습니다.

64비트 범용 레지스터가 16개라면 128바이트에 불과하고, 하나의 명령어로 여러 데이터를 동시에 처리하는 SIMD(Single Instruction Multiple Data) 전용 레지스터까지 포함해도 수 킬로바이트를 넘지 않습니다.

<br>

게임에서 실행되는 연산 — 캐릭터 좌표 계산, 물리 시뮬레이션, AI 판단 — 의 중간 결과는 레지스터에 잠시 머뭅니다.

하지만 128바이트에서 수 킬로바이트에 불과한 레지스터만으로는 게임에 필요한 데이터를 담을 수 없으므로, 나머지는 캐시와 DRAM에 저장됩니다.

---

## L1, L2, L3 캐시

캐시(Cache)는 CPU와 DRAM 사이의 속도 차이를 줄이기 위한 중간 저장소입니다.

CPU가 최근에 접근한 데이터의 복사본을 가까이에 유지하여, 같은 데이터나 그 근처 데이터를 다시 필요로 할 때 DRAM까지 가지 않고 빠르게 읽을 수 있게 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 560" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">캐시의 위치와 구조</text>
  <rect x="20" y="38" width="560" height="346" rx="6" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="58" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <rect x="50" y="74" width="220" height="200" rx="5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3,2"/>
  <text x="160" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">코어 0</text>
  <rect x="70" y="106" width="180" height="42" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="131" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">레지스터</text>
  <rect x="70" y="156" width="180" height="50" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="176" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L1 캐시</text>
  <text x="160" y="194" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">32 ~ 64 KB</text>
  <rect x="70" y="214" width="180" height="50" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="160" y="234" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L2 캐시</text>
  <text x="160" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">256 KB ~ 1 MB</text>
  <rect x="330" y="74" width="220" height="200" rx="5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="3,2"/>
  <text x="440" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">코어 1</text>
  <rect x="350" y="106" width="180" height="42" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="440" y="131" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">레지스터</text>
  <rect x="350" y="156" width="180" height="50" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="440" y="176" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L1 캐시</text>
  <text x="440" y="194" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">32 ~ 64 KB</text>
  <rect x="350" y="214" width="180" height="50" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="440" y="234" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L2 캐시</text>
  <text x="440" y="252" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">256 KB ~ 1 MB</text>
  <rect x="50" y="294" width="500" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="300" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L3 캐시 (공유)</text>
  <text x="300" y="334" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">4 MB ~ 64 MB</text>
  <text x="300" y="352" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">모든 코어가 함께 사용</text>
  <line x1="300" y1="384" x2="300" y2="438" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="416" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">메모리 버스</text>
  <rect x="180" y="438" width="240" height="86" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="462" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DRAM</text>
  <text x="300" y="480" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">메인 메모리</text>
  <text x="300" y="500" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">4 GB ~ 64 GB</text>
</svg>
</div>

### L1 캐시

L1 캐시는 CPU 코어 바로 옆에 위치하며, 코어마다 전용으로 할당되어 다른 코어와 공유하지 않습니다.

접근 시간은 약 1 나노초이고, 용량은 32~64 KB입니다. [이전 글](/dev/unity/HardwareBasics-1/)에서 다룬 수정된 하버드 아키텍처에 따라, L1 캐시는 **명령어 캐시(L1i)**와 **데이터 캐시(L1d)**로 분리되어 있습니다. 명령어 캐시는 실행할 명령어를, 데이터 캐시는 연산에 사용할 데이터를 저장하며, 이 분리 덕분에 명령어 인출과 데이터 접근이 동시에 이루어집니다.

<br>

32~64 KB는 용량 자체로는 작지만, CPU가 한 순간에 집중적으로 접근하는 데이터는 대부분 이 범위 안에 들어옵니다. 반복문 안에서 배열을 순차적으로 처리하는 경우, 현재 처리 중인 구간의 데이터가 L1에 올라와 있으면 레지스터 다음으로 빠르게 접근할 수 있습니다.

### L2 캐시

L2 캐시는 L1보다 크고 약간 느린 계층으로, 코어마다 전용으로 배치되는 경우가 일반적입니다. 용량은 256 KB에서 1 MB 사이이며, 접근 시간은 약 5 나노초입니다.

L1에 없는 데이터를 요청하면 DRAM으로 가기 전에 L2에서 먼저 탐색합니다. L2는 L1보다 용량이 크므로, L1에서 밀려난 데이터가 L2에는 남아 있을 가능성이 있습니다.

### L3 캐시

L3 캐시는 CPU 안의 모든 코어가 **공유**하는 캐시로, 용량은 4 MB에서 64 MB까지 다양하고 접근 시간은 약 15 나노초입니다.

L1과 L2가 코어 전용인 것과 달리, L3는 한 코어가 DRAM에서 가져온 데이터를 다른 코어도 L3에서 읽을 수 있습니다.

<br>

게임의 물리 시뮬레이션이나 잡 시스템에서는 여러 코어가 같은 데이터에 접근합니다. 코어 0이 먼저 데이터를 읽으면 그 데이터가 L3에 저장되고, 이후 코어 1이 같은 데이터를 필요로 할 때 DRAM 대신 L3에서 바로 가져옵니다.

### 캐시 조회 순서

CPU가 데이터를 필요로 하면, L1 → L2 → L3 → DRAM 순서로 조회합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 480" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데이터 조회 흐름</text>
  <rect x="160" y="36" width="300" height="40" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU가 주소 0x1000의 데이터 요청</text>
  <line x1="310" y1="76" x2="310" y2="104" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="310,108 306,100 314,100" fill="currentColor"/>
  <rect x="160" y="108" width="240" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="132" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L1 캐시에 있는가?</text>
  <line x1="400" y1="128" x2="430" y2="128" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="434,128 426,124 426,132" fill="currentColor"/>
  <text x="415" y="120" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">있음</text>
  <rect x="436" y="108" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="521" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">L1 히트</text>
  <text x="521" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">1 ns 만에 반환 · 끝</text>
  <line x1="280" y1="148" x2="280" y2="180" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="280,184 276,176 284,176" fill="currentColor"/>
  <text x="290" y="168" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">없음 (L1 미스)</text>
  <rect x="160" y="184" width="240" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="208" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L2 캐시에 있는가?</text>
  <line x1="400" y1="204" x2="430" y2="204" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="434,204 426,200 426,208" fill="currentColor"/>
  <text x="415" y="196" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">있음</text>
  <rect x="436" y="184" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="521" y="202" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">L2 히트</text>
  <text x="521" y="217" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">5 ns · L1에도 복사</text>
  <line x1="280" y1="224" x2="280" y2="256" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="280,260 276,252 284,252" fill="currentColor"/>
  <text x="290" y="244" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">없음 (L2 미스)</text>
  <rect x="160" y="260" width="240" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="284" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L3 캐시에 있는가?</text>
  <line x1="400" y1="280" x2="430" y2="280" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="434,280 426,276 426,284" fill="currentColor"/>
  <text x="415" y="272" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">있음</text>
  <rect x="436" y="260" width="170" height="40" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="521" y="278" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">L3 히트</text>
  <text x="521" y="293" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">15 ns · L2, L1에 복사</text>
  <line x1="280" y1="300" x2="280" y2="332" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="280,336 276,328 284,328" fill="currentColor"/>
  <text x="290" y="320" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">없음 (L3 미스)</text>
  <rect x="160" y="336" width="300" height="56" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="358" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DRAM에서 가져옴</text>
  <text x="310" y="376" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">100 ns · L3, L2, L1에 복사</text>
  <text x="310" y="430" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">상위 계층에 있을수록 빠르게 반환되며, 미스 시 하위 계층까지 내려가 가져옴</text>
</svg>
</div>

<br>

L1에서 데이터를 찾으면 1 나노초 만에 연산을 진행할 수 있고, L3까지 내려가도 15 나노초면 됩니다.

하지만 모든 캐시에서 미스가 발생하여 DRAM까지 가야 한다면 100 나노초가 소요됩니다. 3 GHz CPU의 1클럭은 약 0.33 나노초이므로, DRAM 접근 한 번에 약 300 클럭 동안 파이프라인이 데이터 도착을 기다리게 됩니다.

---

## 캐시의 동작 원리

CPU가 메모리에서 데이터를 가져올 때, 캐시는 요청한 바이트만 가져오지 않습니다.

해당 바이트가 속한 **64바이트 블록 전체**를 한 번에 가져옵니다.

이 64바이트 블록을 **캐시 라인(Cache Line)**이라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">캐시 라인</text>
  <text x="290" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">CPU가 주소 0x1004의 데이터를 요청하면</text>
  <text x="222" y="64" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">요청한 위치 (0x1004)</text>
  <line x1="222" y1="68" x2="222" y2="84" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="222,88 218,80 226,80" fill="currentColor"/>
  <rect x="60" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="78" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b0</text>
  <rect x="96" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="114" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b1</text>
  <rect x="132" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="150" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b2</text>
  <rect x="168" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="186" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b3</text>
  <rect x="204" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.30" stroke="currentColor" stroke-width="1.4"/>
  <text x="222" y="112" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="currentColor">b4</text>
  <rect x="240" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="258" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b5</text>
  <rect x="276" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="294" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b6</text>
  <rect x="312" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b7</text>
  <rect x="348" y="92" width="72" height="32" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="384" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">···</text>
  <rect x="420" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="438" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b61</text>
  <rect x="456" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="474" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b62</text>
  <rect x="492" y="92" width="36" height="32" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="510" y="112" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">b63</text>
  <text x="60" y="140" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">0x1000</text>
  <text x="528" y="140" text-anchor="end" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">0x103F</text>
  <text x="290" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.9" font-weight="bold">캐시 라인 (64바이트)</text>
  <line x1="60" y1="166" x2="60" y2="176" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <line x1="60" y1="171" x2="528" y2="171" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.6"/>
  <line x1="528" y1="166" x2="528" y2="176" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="290" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">요청한 1바이트(b4)뿐 아니라, 64바이트 블록 전체가 캐시에 올라옴</text>
</svg>
</div>

<br>

다이어그램에서 요청한 주소는 0x1004이지만, 캐시 라인은 0x1000에서 시작합니다. 요청한 위치를 중심으로 앞뒤 64바이트를 가져오는 것이 아닙니다.

DRAM의 주소 공간은 64바이트 단위로 미리 나뉘어 있고, 캐시 라인의 경계는 64의 배수 주소(0x0000, 0x0040, 0x0080, …)에 고정되어 있습니다.

CPU가 어떤 주소를 요청하면, 캐시는 그 주소가 속한 64바이트 정렬 블록 전체를 가져옵니다. 요청한 데이터가 블록의 처음에 있든 중간에 있든 끝에 있든, 가져오는 범위는 동일합니다.

<br>

요청하지 않은 나머지 바이트까지 함께 가져오지만, 추가 비용은 거의 없습니다.

DRAM 접근에서 시간이 오래 걸리는 부분은 행(Row)을 활성화하고 열(Column) 주소를 지정하는 초기 지연이며, 행이 열린 뒤에는 연속된 바이트를 버스트(burst) 모드로 빠르게 전송할 수 있기 때문입니다.

즉, 1바이트를 가져오든 64바이트를 가져오든 초기 지연은 동일하고, 나머지 바이트의 전송 시간은 초기 지연에 비해 짧습니다.

<br>

캐시가 1바이트가 아닌 블록 단위로 가져오는 이유는, 어떤 주소의 데이터를 사용했다면 그 근처의 데이터도 곧 사용할 가능성이 높기 때문입니다.

블록의 크기가 구체적으로 64바이트인 데에도 이유가 있습니다. 캐시 라인이 너무 작으면 근처 데이터를 충분히 활용하지 못해 DRAM 접근이 자주 발생하고, 너무 크면 사용하지 않을 데이터까지 가져와 캐시 공간과 대역폭을 낭비합니다. 64바이트는 이 양쪽 사이의 균형점이며, DDR 메모리가 한 번의 버스트로 전송하는 단위와도 일치합니다.

배열을 순차적으로 접근하는 코드가 대표적인 예입니다. 배열의 첫 번째 요소를 읽을 때 64바이트가 캐시에 올라오면, 이후 요소들은 이미 캐시에 있으므로 DRAM 접근 없이 읽을 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">배열 순차 접근과 캐시 라인</text>
  <text x="300" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">float 하나 = 4바이트 → 64바이트 캐시 라인 안에 float 16개가 들어감</text>
  <text x="50" y="74" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐시 라인 1 (64바이트)</text>
  <rect x="50" y="82" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="104" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[0]</text>
  <rect x="130" y="82" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="104" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[1]</text>
  <rect x="210" y="82" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="250" y="104" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[2]</text>
  <rect x="290" y="82" width="180" height="36" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="380" y="104" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">···</text>
  <rect x="470" y="82" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="510" y="104" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[15]</text>
  <text x="50" y="148" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐시 라인 2 (64바이트)</text>
  <rect x="50" y="156" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="178" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[16]</text>
  <rect x="130" y="156" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="178" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[17]</text>
  <rect x="210" y="156" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="250" y="178" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[18]</text>
  <rect x="290" y="156" width="180" height="36" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="380" y="178" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">···</text>
  <rect x="470" y="156" width="80" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="510" y="178" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">float[31]</text>
  <text x="300" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">float[0]을 읽는 순간 → 캐시 라인 1 전체가 캐시에 올라옴</text>
  <text x="300" y="240" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">float[1] ~ float[15] → 이미 캐시에 있음 → DRAM 접근 불필요</text>
  <text x="300" y="258" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">float[16]을 읽는 순간 → 캐시 라인 2가 캐시에 올라옴</text>
  <text x="300" y="282" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">이 패턴이 배열 끝까지 반복됨</text>
</svg>
</div>

<br>

16개의 float를 읽는 동안 DRAM 접근은 1번만 발생합니다. 순차 접근이 빠른 이유가 바로 이 캐시 라인 단위의 일괄 전송에 있습니다.

---

## 공간적 지역성과 시간적 지역성

앞 섹션에서 배열을 순차적으로 접근하면 캐시 라인 덕분에 DRAM 접근이 줄어드는 것을 확인했습니다. 이처럼 캐시가 효과적으로 작동하는 접근 패턴의 특성을 **지역성(Locality)**이라 하며, 크게 두 가지로 나뉩니다. 

**공간적 지역성(Spatial Locality)**과 **시간적 지역성(Temporal Locality)**입니다.

### 공간적 지역성

공간적 지역성은 "어떤 주소의 데이터를 사용했다면, 그 근처 주소의 데이터도 곧 사용할 가능성이 높다"는 경향입니다. 

배열 순차 접근 시 캐시 라인이 이웃 요소를 함께 가져오는 동작이 바로 이 경향을 활용한 것입니다.

<br>

적 캐릭터 100명의 위치를 매 프레임 갱신하는 게임 상황을 예로 들면, position 값이 배열에 연속으로 저장되어 있을 때 `positions[0]`부터 `positions[99]`까지 순차적으로 접근하는 코드는 공간적 지역성이 높습니다.

첫 번째 position을 읽을 때 64바이트 캐시 라인이 올라오면서 인접한 position 값들이 함께 적재되므로, 이후 요소들은 DRAM 접근 없이 캐시에서 바로 읽힙니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공간적 지역성이 높은 접근 패턴</text>
  <text x="50" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">메모리 배치</text>
  <rect x="50" y="56" width="76" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="88" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[0]</text>
  <rect x="126" y="56" width="76" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="164" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[1]</text>
  <rect x="202" y="56" width="76" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[2]</text>
  <rect x="278" y="56" width="76" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="316" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[3]</text>
  <rect x="354" y="56" width="76" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="392" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[4]</text>
  <rect x="430" y="56" width="76" height="36" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="468" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[5]</text>
  <text x="514" y="78" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">···</text>
  <line x1="88" y1="100" x2="88" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="88,122 84,114 92,114" fill="currentColor"/>
  <line x1="164" y1="100" x2="164" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="164,122 160,114 168,114" fill="currentColor"/>
  <line x1="240" y1="100" x2="240" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="240,122 236,114 244,114" fill="currentColor"/>
  <line x1="316" y1="100" x2="316" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="316,122 312,114 320,114" fill="currentColor"/>
  <line x1="392" y1="100" x2="392" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="392,122 388,114 396,114" fill="currentColor"/>
  <line x1="468" y1="100" x2="468" y2="118" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="468,122 464,114 472,114" fill="currentColor"/>
  <text x="88" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">접근 1</text>
  <text x="164" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">접근 2</text>
  <text x="240" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">접근 3</text>
  <text x="316" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">접근 4</text>
  <text x="392" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">접근 5</text>
  <text x="468" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">접근 6</text>
  <text x="290" y="178" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">메모리에서 연속된 위치를 순서대로 접근</text>
  <text x="290" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">캐시 라인 활용도 높음 → DRAM 접근 횟수 적음</text>
</svg>
</div>

### 시간적 지역성

시간적 지역성은 "한 번 사용한 데이터를 가까운 시간 내에 다시 사용할 가능성이 높다"는 경향입니다.

<br>

게임에서 플레이어 캐릭터의 위치 데이터는 매 프레임 읽고 갱신됩니다. 이동 로직, 충돌 판정, 카메라 추적, UI 업데이트 등 여러 시스템이 한 프레임 안에서 같은 데이터를 반복적으로 참조합니다.

캐시는 최근에 접근한 데이터를 유지하므로, 첫 번째 시스템이 읽을 때 DRAM에서 캐시로 올라온 데이터가 이후 시스템에서도 캐시에 남아 있어 바로 읽힙니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 350" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">시간적 지역성이 높은 접근 패턴</text>
  <text x="300" y="40" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">프레임 내에서 playerPosition 접근 순서</text>
  <rect x="60" y="58" width="180" height="42" rx="5" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="150" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이동 시스템</text>
  <text x="150" y="92" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">playerPosition 읽기/쓰기</text>
  <text x="270" y="83" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 캐시에 올라옴 (DRAM 접근)</text>
  <line x1="150" y1="100" x2="150" y2="124" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="150,128 146,120 154,120" fill="currentColor"/>
  <rect x="60" y="128" width="180" height="42" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="150" y="146" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">충돌 판정</text>
  <text x="150" y="162" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">playerPosition 읽기</text>
  <text x="270" y="153" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 캐시에서 즉시 읽힘</text>
  <line x1="150" y1="170" x2="150" y2="194" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="150,198 146,190 154,190" fill="currentColor"/>
  <rect x="60" y="198" width="180" height="42" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="150" y="216" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">카메라 추적</text>
  <text x="150" y="232" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">playerPosition 읽기</text>
  <text x="270" y="223" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 캐시에서 즉시 읽힘</text>
  <line x1="150" y1="240" x2="150" y2="264" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="150,268 146,260 154,260" fill="currentColor"/>
  <rect x="60" y="268" width="180" height="42" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="150" y="286" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">UI 갱신</text>
  <text x="150" y="302" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">playerPosition 읽기</text>
  <text x="270" y="293" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 캐시에서 즉시 읽힘</text>
  <text x="300" y="332" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-weight="bold">같은 데이터를 짧은 시간 내에 반복 사용 → 첫 접근만 DRAM, 이후는 캐시</text>
</svg>
</div>

<br>

공간적 지역성은 **가까운 주소**의 데이터를 연달아 사용하는 경향이고, 시간적 지역성은 **같은 데이터**를 짧은 시간 안에 반복 사용하는 경향입니다.

캐시 라인이 64바이트 블록을 한꺼번에 가져오는 구조는 공간적 지역성을, 최근 접근 데이터를 캐시에 유지하는 구조는 시간적 지역성을 뒷받침합니다.

프로그램의 접근 패턴이 이 두 지역성에 부합할수록 캐시 적중률(hit rate)이 높아지고, DRAM 접근이 줄어 성능이 향상됩니다.

---

## 캐시 미스의 종류와 비용

CPU가 필요한 데이터가 캐시에 없는 상황을 **캐시 미스(Cache Miss)**라고 합니다.

캐시 미스가 발생하면 CPU는 더 느린 하위 계층(L2, L3, 또는 DRAM)까지 내려가 데이터를 가져와야 하고, 그동안 해당 데이터에 의존하는 명령어는 진행되지 못합니다.

캐시 미스는 발생 원인에 따라 세 종류로 나뉩니다.

### Cold Miss (콜드 미스)

프로그램이 특정 데이터를 **처음** 접근할 때 발생합니다.

캐시에 아직 해당 데이터가 올라온 적이 없으므로, 반드시 DRAM에서 가져와야 합니다.

**강제 미스(Compulsory Miss)**라고도 부릅니다.

<br>

게임 시작 직후, 첫 프레임에서 텍스처, 메시, 게임 오브젝트 데이터를 처음 읽을 때 콜드 미스가 집중적으로 발생합니다. 이후 프레임에서는 해당 데이터가 캐시에 남아 있을 가능성이 높으므로, 각 데이터에 대한 콜드 미스는 최초 접근 시 한 번만 발생합니다.

### Capacity Miss (용량 미스)

캐시의 용량이 부족하여 이전에 올라왔던 데이터가 밀려난 후, 그 데이터를 다시 접근할 때 발생합니다.

캐시에 담아야 할 데이터의 총량이 캐시 크기를 초과하면, 캐시는 기존 데이터 중 일부를 교체 정책(대표적으로 LRU -- 가장 오래 사용되지 않은 항목 우선 제거)에 따라 내보냅니다(eviction).

내보내진 데이터를 다시 필요로 하면 하위 계층에서 다시 가져와야 합니다.

<br>

적 캐릭터 1,000명의 데이터를 매 프레임 처리하는 게임을 예로 들면, 적 하나당 128바이트일 때 총 128 KB를 다뤄야 합니다. L1 캐시가 32 KB이므로 전체의 1/4만 동시에 담을 수 있습니다. 처음 수백 명을 처리하며 캐시에 올린 데이터는 나머지를 처리하는 동안 밀려나고, 다시 처음 수백 명의 데이터를 참조하면 용량 미스가 발생합니다.

### Conflict Miss (충돌 미스)

용량 미스와 달리, 캐시에 빈 공간이 남아 있는데도 발생하는 미스입니다. 원인은 캐시의 저장 위치 제한에 있습니다.

캐시는 데이터를 아무 곳에나 저장하지 않고, 메모리 주소의 일부 비트를 사용하여 저장할 위치를 결정합니다. 이 위치를 **set**이라 부르며, 캐시의 모든 공간을 자유롭게 사용하는 것이 아니라 주소에 따라 저장할 수 있는 set이 고정됩니다.

각 set에 저장할 수 있는 캐시 라인 수는 고정되어 있으며, 이 수를 **way**라 부릅니다. 8-way set-associative 캐시라면 set 하나에 캐시 라인 8개까지 들어갑니다.

서로 다른 메모리 주소들이 주소 비트 특성상 같은 set에 매핑되면, way 수를 초과하는 순간 기존 데이터가 밀려납니다. 캐시 전체에는 빈 공간이 남아 있어도, 특정 set의 way가 모두 차 있으면 그 set에서 충돌 미스가 발생합니다.

| 미스 종류 | 발생 조건 | 핵심 특징 |
|---|---|---|
| Cold Miss (콜드 미스) | 데이터를 처음 접근 | 캐시에 올라온 적이 없음 |
| Capacity Miss (용량 미스) | 작업 데이터 총량 > 캐시 크기 | 밀려난 데이터를 다시 접근할 때 발생 |
| Conflict Miss (충돌 미스) | 같은 set에 매핑된 데이터가 way 수 초과 | 캐시 전체에 빈 공간이 있어도 발생 |

### 캐시 미스의 비용

캐시 미스가 발생하면, CPU는 하위 계층에서 데이터가 도착할 때까지 해당 명령어를 진행할 수 없습니다.

데이터를 기다리는 동안 파이프라인의 Memory 단계가 멈추고, 후속 단계도 연쇄적으로 대기합니다.

[이전 글](/dev/unity/HardwareBasics-1/)에서 다룬 **파이프라인 스톨(stall)**이 캐시 미스에서도 그대로 발생합니다.

3 GHz CPU 기준, 데이터가 어느 계층에서 발견되느냐에 따른 소요 클럭:

| 데이터 위치 | 소요 클럭 |
|---|---|
| L1 히트 | ~4 |
| L2 히트 (L1 미스) | ~19 |
| L3 히트 (L2 미스) | ~64 |
| DRAM 응답 (L3 미스) | ~300 |

L1 히트라면 3~4클럭이면 끝날 데이터 접근이, 모든 캐시를 미스하고 DRAM까지 내려가면 약 300클럭이 소요됩니다. CPU의 연산 능력이 아무리 높아도, 데이터가 제때 도착하지 않으면 파이프라인이 빈 채로 대기할 수밖에 없습니다.

<br>

현대 CPU는 [이전 글](/dev/unity/HardwareBasics-1/)에서 다룬 out-of-order 실행으로 이 대기 시간에 의한 성능 손실을 줄입니다. 데이터를 기다리는 동안 해당 데이터에 의존하지 않는 명령어를 먼저 실행하여, 파이프라인이 놀지 않게 하는 방식입니다.

다만 CPU가 동시에 추적할 수 있는 미완료 명령어 수는 리오더 버퍼(reorder buffer)의 크기로 제한됩니다.

모바일 big 코어에서 약 100~200개, 데스크톱 CPU에서 약 300~600개 수준입니다.

캐시 미스가 연속으로 발생하면 완료를 기다리는 명령어들이 이 버퍼를 빠르게 채우고, 새 명령어를 더 이상 투입할 수 없어 파이프라인이 결국 멈춥니다.

---

## 메모리 접근 패턴이 성능에 미치는 영향

같은 양의 데이터를 처리하더라도, **메모리 접근 순서**에 따라 캐시 적중률이 달라지고 성능 차이가 발생합니다.

가장 대표적인 비교가 **순차 접근과 랜덤 접근**입니다.

### 순차 접근 vs 랜덤 접근

순차 접근은 메모리의 연속된 주소를 차례대로 읽는 것입니다. 배열을 인덱스 0부터 끝까지 순서대로 접근하는 경우가 대표적입니다.

<br>

랜덤 접근은 메모리의 여기저기를 무작위로 읽는 것입니다. 연결 리스트(Linked List)의 노드를 포인터를 따라가며 접근하는 것이 대표적입니다.

연결 리스트에서 각 노드는 다음 노드의 주소를 담고 있으며, 노드들은 힙(heap, 동적 메모리 할당 영역)의 임의 위치에 흩어져 있습니다. 따라서 다음 노드의 주소가 현재 노드의 근처에 있을 보장이 없습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">순차 접근의 캐시 활용</text>
  <text x="290" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">배열 float 1024개 · 캐시 라인 64B = float 16개</text>
  <text x="40" y="74" font-family="monospace" font-size="11" fill="currentColor">data[0]</text>
  <text x="220" y="74" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 캐시 라인 로드 (미스)</text>
  <text x="40" y="98" font-family="monospace" font-size="11" fill="currentColor">data[1] ~ data[15]</text>
  <text x="220" y="98" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 같은 캐시 라인 (히트 15회)</text>
  <text x="40" y="122" font-family="monospace" font-size="11" fill="currentColor">data[16]</text>
  <text x="220" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 새 캐시 라인 로드 (미스)</text>
  <text x="40" y="146" font-family="monospace" font-size="11" fill="currentColor">data[17] ~ data[31]</text>
  <text x="220" y="146" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 같은 캐시 라인 (히트 15회)</text>
  <text x="40" y="172" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">이 패턴이 64회 반복</text>
  <line x1="40" y1="192" x2="540" y2="192" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="290" y="218" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">미스 64회 / 접근 1,024회 = 미스율 6.25%</text>
</svg>
</div>

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">랜덤 접근의 캐시 활용</text>
  <text x="290" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">연결 리스트 노드 1024개 · 각 노드가 힙의 임의 위치에 분산</text>
  <text x="40" y="74" font-family="monospace" font-size="11" fill="currentColor">node0</text>
  <text x="100" y="74" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">(주소 0x2000)</text>
  <text x="270" y="74" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 캐시 라인 로드 (미스)</text>
  <text x="40" y="98" font-family="monospace" font-size="11" fill="currentColor">node7</text>
  <text x="100" y="98" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">(주소 0xA400)</text>
  <text x="270" y="98" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 다른 캐시 라인 (미스)</text>
  <text x="40" y="122" font-family="monospace" font-size="11" fill="currentColor">node3</text>
  <text x="100" y="122" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">(주소 0x5C00)</text>
  <text x="270" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 다른 캐시 라인 (미스)</text>
  <text x="40" y="146" font-family="monospace" font-size="11" fill="currentColor">node9</text>
  <text x="100" y="146" font-family="monospace" font-size="10" fill="currentColor" opacity="0.7">(주소 0x1800)</text>
  <text x="270" y="146" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ 다른 캐시 라인 (미스)</text>
  <text x="40" y="172" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">매 접근마다 주소가 달라 캐시 라인 재사용 불가</text>
  <line x1="40" y1="192" x2="540" y2="192" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="290" y="218" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">미스율 최대 100%</text>
</svg>
</div>

<br>

앞 섹션에서 본 것처럼, 순차 접근은 16번 중 1번만 DRAM에 가고 나머지 15번은 캐시에서 처리됩니다. 반면 랜덤 접근은 매번 DRAM까지 내려갈 수 있습니다.

<br>

이 차이를 클럭 수로 환산하면 규모가 분명해집니다.

1,024개의 float를 처리할 때, 순차 접근은 캐시 미스 64회(1,024 / 16)에 히트 960회이므로 총 대기 클럭이 약 64 x 300 + 960 x 4 = 23,040클럭입니다.

랜덤 접근은 1,024회 모두 미스가 발생할 수 있으므로 최대 1,024 x 300 = 307,200클럭입니다. 같은 데이터를 처리하면서 약 13배의 대기 시간 차이가 발생합니다.

### Array of Structs vs Struct of Arrays

순차 접근과 랜덤 접근의 차이는 단순히 "배열 vs 연결 리스트"에만 해당하지 않습니다.

같은 배열이라도 데이터 배치 방식에 따라 실제 접근 패턴이 순차에 가까울 수도 있고 랜덤에 가까울 수도 있습니다.

게임에서 이 차이가 드러나는 대표적인 사례가 **AoS와 SoA** 두 가지 데이터 배치 방식입니다.

<br>

적 캐릭터의 데이터를 저장하는 상황에서, **Array of Structs (AoS)**는 각 적의 모든 데이터를 하나의 구조체에 모아서 구조체 배열을 만드는 방식입니다.

<br>

```csharp
struct Enemy {
    Vector3 position;  // 12바이트
    Vector3 velocity;  // 12바이트
    float   health;    //  4바이트
    int     state;     //  4바이트
}                      // 합계 32바이트

Enemy[] enemies = new Enemy[1000];
```

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Array of Structs (AoS) 메모리 배치</text>
  <rect x="30" y="46" width="240" height="56" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="150" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">enemies[0] (32B)</text>
  <line x1="90" y1="74" x2="90" y2="102" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
  <line x1="150" y1="74" x2="150" y2="102" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
  <line x1="210" y1="74" x2="210" y2="102" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
  <text x="60" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos</text>
  <text x="120" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">vel</text>
  <text x="180" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">health</text>
  <text x="240" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">state</text>
  <rect x="270" y="46" width="240" height="56" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="390" y="64" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">enemies[1] (32B)</text>
  <line x1="330" y1="74" x2="330" y2="102" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
  <line x1="390" y1="74" x2="390" y2="102" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
  <line x1="450" y1="74" x2="450" y2="102" stroke="currentColor" stroke-width="0.5" opacity="0.4"/>
  <text x="300" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos</text>
  <text x="360" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">vel</text>
  <text x="420" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">health</text>
  <text x="480" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">state</text>
  <text x="528" y="78" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="300" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">각 적의 모든 필드가 한 구조체에 모이고, 구조체들이 배열에 연속 배치됨</text>
</svg>
</div>

<br>

반면 **Struct of Arrays (SoA)**는 같은 종류의 데이터끼리 별도의 배열로 분리하여 저장합니다.

<br>

```csharp
Vector3[] positions  = new Vector3[1000];
Vector3[] velocities = new Vector3[1000];
float[]   healths    = new float[1000];
int[]     states     = new int[1000];
```

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Struct of Arrays (SoA) 메모리 배치</text>
  <text x="40" y="50" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">positions 배열</text>
  <rect x="40" y="58" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[0]</text>
  <rect x="120" y="58" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[1]</text>
  <rect x="200" y="58" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[2]</text>
  <rect x="280" y="58" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="320" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[3]</text>
  <rect x="360" y="58" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="400" y="78" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[4]</text>
  <text x="448" y="78" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="40" y="120" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">velocities 배열</text>
  <rect x="40" y="128" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="148" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel[0]</text>
  <rect x="120" y="128" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="148" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel[1]</text>
  <rect x="200" y="128" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="148" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel[2]</text>
  <rect x="280" y="128" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="320" y="148" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel[3]</text>
  <rect x="360" y="128" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="400" y="148" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel[4]</text>
  <text x="448" y="148" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="40" y="190" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">healths 배열</text>
  <rect x="40" y="198" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="218" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">hp[0]</text>
  <rect x="120" y="198" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="218" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">hp[1]</text>
  <rect x="200" y="198" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="218" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">hp[2]</text>
  <rect x="280" y="198" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="320" y="218" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">hp[3]</text>
  <rect x="360" y="198" width="80" height="32" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="400" y="218" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">hp[4]</text>
  <text x="448" y="218" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="300" y="258" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">같은 종류의 데이터가 별도의 배열로 분리되어 저장됨 (states 배열도 동일 구조)</text>
</svg>
</div>

<br>

"모든 적의 위치를 갱신하라"는 작업을 수행한다고 가정하면, 이 작업에 필요한 데이터는 position과 velocity뿐이고 health와 state는 사용하지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">AoS에서 위치 갱신 시 캐시 활용</text>
  <text x="40" y="44" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">필요한 데이터: position(12B) + velocity(12B) = 24바이트</text>
  <text x="40" y="60" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">실제 캐시 라인에 올라오는 데이터: 32바이트 (health, state 포함)</text>
  <text x="290" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">캐시 라인 64바이트 안에 Enemy 2개</text>
  <text x="170" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">enemies[0] (32B)</text>
  <rect x="50" y="108" width="80" height="36" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="130" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos</text>
  <rect x="130" y="108" width="80" height="36" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="170" y="130" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel</text>
  <rect x="210" y="108" width="40" height="36" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="230" y="130" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.6">health</text>
  <rect x="250" y="108" width="40" height="36" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="270" y="130" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.6">state</text>
  <text x="410" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">enemies[1] (32B)</text>
  <rect x="290" y="108" width="80" height="36" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="130" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos</text>
  <rect x="370" y="108" width="80" height="36" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="130" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">vel</text>
  <rect x="450" y="108" width="40" height="36" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="470" y="130" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.6">health</text>
  <rect x="490" y="108" width="40" height="36" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="510" y="130" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.6">state</text>
  <polygon points="250,148 246,156 254,156" fill="currentColor" opacity="0.6"/>
  <line x1="250" y1="156" x2="250" y2="166" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="250" y="180" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">사용하지 않는 8B</text>
  <polygon points="490,148 486,156 494,156" fill="currentColor" opacity="0.6"/>
  <line x1="490" y1="156" x2="490" y2="166" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <text x="490" y="180" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">사용하지 않는 8B</text>
  <text x="290" y="212" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐시 라인 64B 중 48B만 실제로 사용 (활용률 75%)</text>
  <text x="290" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">사용하지 않는 health, state가 캐시 공간을 차지함</text>
</svg>
</div>

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SoA에서 위치 갱신 시 캐시 활용</text>
  <text x="40" y="44" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">필요한 데이터: positions 배열, velocities 배열만 접근</text>
  <text x="290" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">positions 캐시 라인 (64B)</text>
  <rect x="80" y="78" width="80" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="120" y="96" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[0]</text>
  <text x="120" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">12B</text>
  <rect x="160" y="78" width="80" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="200" y="96" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[1]</text>
  <text x="200" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">12B</text>
  <rect x="240" y="78" width="80" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="96" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[2]</text>
  <text x="280" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">12B</text>
  <rect x="320" y="78" width="80" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="360" y="96" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[3]</text>
  <text x="360" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">12B</text>
  <rect x="400" y="78" width="80" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="440" y="96" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[4]</text>
  <text x="440" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">12B</text>
  <rect x="480" y="78" width="26" height="40" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="493" y="96" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos[5]</text>
  <text x="493" y="110" text-anchor="middle" font-family="monospace" font-size="8" fill="currentColor" opacity="0.7">4B…</text>
  <text x="290" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">모든 셀이 위치 데이터 (활용률 100%)</text>
  <line x1="40" y1="162" x2="540" y2="162" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="290" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐시 라인의 모든 데이터가 실제로 필요한 데이터</text>
  <text x="290" y="208" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">불필요한 데이터가 캐시를 차지하지 않음</text>
</svg>
</div>

<br>

AoS 방식에서는 필요하지 않은 health, state도 함께 올라와서 캐시 공간을 낭비합니다.

SoA 방식에서는 캐시 라인에 올라오는 데이터가 전부 실제로 필요한 데이터입니다.

<br>

구체적으로 비교하면, 적 1,000명의 위치를 갱신할 때 AoS는 캐시 라인당 Enemy 2개(32B x 2 = 64B)를 올리므로 500회의 캐시 라인 로드가 필요하고, 로드된 데이터 중 25%(health, state)는 사용되지 않습니다.

SoA는 position과 velocity에 필요한 총 24,000바이트(12B x 1,000 x 2)를 64바이트 단위로 가져오므로 약 375회면 충분합니다. AoS 대비 캐시 라인 로드가 약 25% 적고, 로드된 데이터가 전부 실제 연산에 사용됩니다.

데이터 총량이 L1 캐시(32 KB)를 넘어서면 이 차이가 캐시 미스 횟수의 차이로 직결됩니다.

<br>

Unity의 DOTS(Data-Oriented Technology Stack)와 ECS(Entity Component System)가 SoA 방식을 채택한 것도 같은 원리입니다.

DOTS/ECS는 컴포넌트 종류별로 데이터를 연속된 배열(Chunk)에 저장하고, 시스템이 특정 컴포넌트만 순차적으로 접근하도록 설계합니다.

위치 갱신 시스템이라면 positions과 velocities 배열만 순차 순회하므로, 캐시 라인에 불필요한 데이터가 섞이지 않고 공간적 지역성이 극대화됩니다.

---

## 대역폭과 지연의 차이

지금까지는 캐시 적중률 — 요청한 데이터가 캐시에 존재하는 비율 — 을 높여서 느린 DRAM 접근을 줄이는 데 초점을 맞추었습니다.

하지만 메모리 성능에는 두 가지 별개의 축이 있습니다.

"한 번 접근하는 데 걸리는 시간"인 **지연(Latency)**과, "단위 시간에 전송할 수 있는 데이터의 총량"인 **대역폭(Bandwidth)**입니다.

<br>

**지연(Latency)**은 데이터를 한 번 요청하고 그 데이터가 도착할 때까지 걸리는 시간으로, 앞에서 살펴본 L1 ~1 ns, DRAM ~100 ns 같은 수치가 지연에 해당합니다.

<br>

**대역폭(Bandwidth)**은 단위 시간당 전송할 수 있는 데이터의 총량입니다. DDR5 메모리의 대역폭이 50 GB/s라면, 1초에 최대 50 기가바이트의 데이터를 CPU로 전송할 수 있다는 뜻입니다.

<br>

고속도로에 비유하면, 지연은 한 대의 트럭이 출발지에서 목적지까지 왕복하는 데 걸리는 시간입니다. 짧을수록 한 건의 배달이 빨리 도착합니다.

대역폭은 차선 수에 해당하며, 많을수록 동시에 더 많은 트럭이 이동할 수 있습니다.

왕복 시간이 짧아도 차선이 좁으면 총 전송량이 제한되고, 차선이 넓어도 왕복 시간이 길면 개별 배달이 느립니다.

지연과 대역폭은 서로 독립적이지만, 메모리 성능에는 둘 다 영향을 줍니다.

<br>

게임에서 메모리 접근 패턴에 따라 지연과 대역폭 중 어느 쪽이 병목이 되는지가 달라집니다.

<br>

**지연이 병목이 되는 상황**: 연결 리스트를 따라가면서 각 노드를 하나씩 읽는 경우가 대표적입니다. 다음 노드의 주소를 알려면 현재 노드를 먼저 읽어야 하므로, 한 번에 하나의 메모리 요청만 보낼 수 있습니다. 요청이 직렬화되어 매번 DRAM 왕복 100 ns를 기다리고, 그 사이 메모리 버스는 유휴 상태가 됩니다. 결과적으로 실제 처리량은 64바이트/100 ns, 약 0.6 GB/s에 그쳐 대역폭의 극히 일부만 사용됩니다.

<br>

**대역폭이 병목이 되는 상황**: 대량의 데이터를 순차적으로 읽는 경우에 나타납니다. 텍스처 데이터나 정점 데이터를 GPU로 전송하거나, 큰 배열을 한 번에 처리하는 작업이 해당합니다. 순차 접근에서는 CPU가 다음에 필요할 데이터를 미리 캐시로 가져오는 프리페치(Prefetch)를 통해 개별 요청의 지연을 상쇄할 수 있지만, 초당 전송해야 하는 총 데이터량이 메모리 버스의 대역폭을 초과하면 병목으로 이어집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">지연 병목 vs 대역폭 병목</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">지연 병목 (Latency-bound)</text>
  <rect x="40" y="60" width="60" height="28" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="70" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">요청</text>
  <line x1="100" y1="74" x2="118" y2="74" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="122,74 114,70 114,78" fill="currentColor"/>
  <rect x="122" y="60" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <text x="172" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">100 ns 대기</text>
  <line x1="222" y1="74" x2="240" y2="74" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="244,74 236,70 236,78" fill="currentColor"/>
  <rect x="244" y="60" width="60" height="28" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="274" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">응답</text>
  <line x1="304" y1="74" x2="322" y2="74" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="326,74 318,70 318,78" fill="currentColor"/>
  <rect x="326" y="60" width="80" height="28" rx="3" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="366" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">다음 요청</text>
  <line x1="406" y1="74" x2="424" y2="74" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="428,74 420,70 420,78" fill="currentColor"/>
  <rect x="428" y="60" width="100" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <text x="478" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">100 ns 대기</text>
  <text x="540" y="78" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="60" y="116" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 한 번에 하나씩만 요청 가능 (직렬)</text>
  <text x="60" y="134" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 메모리 버스 대부분이 유휴 상태</text>
  <line x1="40" y1="156" x2="540" y2="156" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="184" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">대역폭 병목 (Bandwidth-bound)</text>
  <rect x="60" y="200" width="84" height="22" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="216" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[0]</text>
  <rect x="60" y="226" width="84" height="22" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="242" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[1]</text>
  <rect x="60" y="252" width="84" height="22" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="268" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[2]</text>
  <rect x="60" y="278" width="84" height="22" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="294" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[3]</text>
  <text x="102" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <line x1="144" y1="211" x2="240" y2="252" stroke="currentColor" stroke-width="1.2" opacity="0.85"/>
  <line x1="144" y1="237" x2="240" y2="258" stroke="currentColor" stroke-width="1.2" opacity="0.85"/>
  <line x1="144" y1="263" x2="240" y2="262" stroke="currentColor" stroke-width="1.2" opacity="0.85"/>
  <line x1="144" y1="289" x2="240" y2="268" stroke="currentColor" stroke-width="1.2" opacity="0.85"/>
  <rect x="240" y="244" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="300" y="260" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">메모리 버스</text>
  <text x="300" y="274" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">(50 GB/s)</text>
  <line x1="360" y1="256" x2="436" y2="240" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="440,239 432,238 434,246" fill="currentColor"/>
  <line x1="360" y1="268" x2="436" y2="284" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="440,285 432,284 434,292" fill="currentColor"/>
  <rect x="440" y="222" width="110" height="30" rx="5" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="495" y="242" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">CPU/GPU</text>
  <rect x="440" y="270" width="110" height="30" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="495" y="290" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">처리</text>
  <text x="60" y="338" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 요청을 동시에 보낼 수 있어 지연은 상쇄 가능</text>
  <text x="60" y="356" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 총 데이터량이 버스 용량을 초과하면 병목 발생</text>
</svg>
</div>

### 프리페치(Prefetch)

순차 접근에서 지연을 상쇄할 수 있는 이유는 하드웨어 프리페치에 있습니다.

CPU 내부의 하드웨어 프리페처(Hardware Prefetcher)는 메모리 접근 패턴을 실시간으로 감지하여, 아직 요청되지 않은 캐시 라인을 DRAM에서 미리 가져옵니다.

데이터가 실제로 필요한 시점에는 이미 캐시에 올라와 있으므로, DRAM 지연에 의한 대기가 발생하지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프리페치의 동작</text>
  <text x="40" y="46" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프리페치 없이</text>
  <text x="50" y="78" font-family="sans-serif" font-size="10" fill="currentColor">CPU</text>
  <rect x="100" y="62" width="100" height="26" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <text x="150" y="79" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">대기 100 ns</text>
  <rect x="200" y="62" width="80" height="26" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="240" y="79" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">처리</text>
  <rect x="280" y="62" width="100" height="26" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <text x="330" y="79" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">대기 100 ns</text>
  <rect x="380" y="62" width="80" height="26" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="420" y="79" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">처리</text>
  <text x="470" y="79" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="50" y="108" font-family="sans-serif" font-size="10" fill="currentColor">DRAM</text>
  <rect x="100" y="92" width="100" height="26" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="150" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">0~15 전송</text>
  <rect x="200" y="92" width="80" height="26" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="240" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">유휴</text>
  <rect x="280" y="92" width="100" height="26" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">16~31 전송</text>
  <rect x="380" y="92" width="80" height="26" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="420" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">유휴</text>
  <text x="470" y="109" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="300" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">처리와 전송이 번갈아 발생, CPU가 절반 가까이 대기</text>
  <line x1="40" y1="166" x2="560" y2="166" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="194" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프리페치 있을 때</text>
  <text x="50" y="226" font-family="sans-serif" font-size="10" fill="currentColor">CPU</text>
  <rect x="100" y="210" width="80" height="26" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <text x="140" y="227" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">대기</text>
  <rect x="180" y="210" width="100" height="26" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="230" y="227" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">0~15 처리</text>
  <rect x="280" y="210" width="100" height="26" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="227" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">16~31 처리</text>
  <rect x="380" y="210" width="100" height="26" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <text x="430" y="227" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">32~47 처리</text>
  <text x="490" y="227" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="50" y="256" font-family="sans-serif" font-size="10" fill="currentColor">DRAM</text>
  <rect x="100" y="240" width="80" height="26" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="140" y="257" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">0~15 전송</text>
  <rect x="180" y="240" width="100" height="26" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="230" y="257" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">16~31 전송</text>
  <rect x="280" y="240" width="100" height="26" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="257" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">32~47 전송</text>
  <rect x="380" y="240" width="100" height="26" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="430" y="257" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">48~63 전송</text>
  <text x="490" y="257" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">···</text>
  <text x="140" y="288" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">첫 미스</text>
  <line x1="180" y1="296" x2="180" y2="280" stroke="currentColor" stroke-width="1" opacity="0.6"/>
  <polygon points="180,276 176,284 184,284" fill="currentColor" opacity="0.6"/>
  <text x="280" y="298" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">여기서부터 프리페치 (패턴 감지 후 미리 요청)</text>
  <text x="300" y="338" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">첫 미스 이후, 처리와 전송이 겹쳐 진행되어 대기 없음</text>
</svg>
</div>

<br>

프리페치가 효과적으로 작동하려면 접근 패턴이 예측 가능해야 합니다.

배열의 순차 접근은 프리페처가 쉽게 예측할 수 있지만, 랜덤 접근은 다음에 어떤 주소를 접근할지 예측할 수 없으므로 프리페처가 도움을 주지 못합니다.

순차 접근이 빠른 이유에는 캐시 라인의 효율적 활용뿐 아니라, 하드웨어 프리페치의 효과도 포함됩니다.

### 모바일과 GPU에서의 대역폭 제약

프리페치로 지연을 상쇄할 수 있더라도, 전송해야 할 데이터 총량이 대역폭을 넘으면 병목이 발생합니다.

이 대역폭 병목은 GPU와 모바일 환경에서 더 두드러집니다.

GPU는 매 프레임 대량의 텍스처와 정점 데이터를 메모리에서 읽어야 하므로 대역폭 소비량이 큽니다.

데스크톱 GPU는 넓은 메모리 버스(256~384비트)와 고속 GDDR 메모리로 500~1,000 GB/s 수준의 대역폭을 확보하여 이를 감당합니다.

<br>

모바일 기기는 사정이 다릅니다.

배터리 전력의 제약으로 메모리 버스 폭이 좁고(64~128비트), 대역폭이 데스크톱 GPU와 비교하면 1/10 ~ 1/50 수준입니다. 같은 양의 텍스처·정점 데이터를 전송하더라도 대역폭 한도에 빠르게 도달합니다.

<br>

모바일 GPU가 텍스처를 많이 읽으면 대역폭이 부족해지고, 같은 메모리를 공유하는 CPU의 접근까지 느려질 수 있습니다.

모바일 GPU에 널리 쓰이는 TBDR(Tile-Based Deferred Rendering) 아키텍처는 화면을 작은 타일 단위로 나누어 타일 내 데이터를 GPU 내부의 온칩 메모리에서 처리함으로써, DRAM으로의 읽기·쓰기 횟수를 줄여 이 대역폭 제약에 대응합니다.

TBDR의 구체적인 구조는 [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 다룹니다.

---

## 마무리

- DRAM 접근은 CPU 연산보다 수백 배 느리며, 이 격차를 메우기 위해 레지스터, L1, L2, L3 캐시, DRAM으로 이루어진 메모리 계층 구조가 존재합니다.
- 캐시는 64바이트 단위(캐시 라인)로 데이터를 가져오며, 1바이트를 요청해도 주변 64바이트가 함께 올라옵니다.
- 공간적 지역성(가까운 주소 연속 접근)과 시간적 지역성(같은 데이터 반복 사용)이 높을수록 캐시 적중률이 올라갑니다.
- 캐시 미스(Cold, Capacity, Conflict)가 발생하면 파이프라인이 대기하며, DRAM 미스는 약 300 클럭의 손실을 초래합니다.
- 순차 접근은 캐시 라인과 프리페치를 활용하여 랜덤 접근보다 수 배에서 수십 배 빠를 수 있고, SoA 방식은 필요한 데이터만 캐시 라인에 올려 활용률을 높입니다.

메모리 계층 구조의 원리를 알면, "배열을 순차적으로 접근하라", "데이터를 연속 배치하라", "캐시 친화적으로 설계하라"는 최적화 조언이 물리적 근거를 갖게 됩니다. 대역폭과 지연이라는 두 축이 독립적으로 성능에 영향을 주며, 모바일 환경에서는 CPU와 GPU가 대역폭을 공유하므로 이 제약이 더 뚜렷합니다.

<br>

CPU가 데이터를 효율적으로 가져오더라도, 게임에서 화면에 보이는 것은 결국 GPU가 그린 결과입니다. CPU는 범용 연산에 적합하지만, 수백만 개의 픽셀을 동시에 처리하는 작업에는 다른 종류의 프로세서가 필요했습니다.

[하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)에서는 CPU가 처리하기 어려운 그래픽 연산을 전담하는 GPU가 어떤 과정을 거쳐 현재의 구조에 이르렀는지를 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)
- [메모리 관리 (1)](/dev/unity/MemoryManagement-1/)

**시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- **하드웨어 기초 (2) - 메모리 계층 구조** (현재 글)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- **하드웨어 기초 (2) - 메모리 계층 구조** (현재 글)
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
