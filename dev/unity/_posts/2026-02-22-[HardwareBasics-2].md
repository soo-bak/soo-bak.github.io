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

[하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)에서는 CPU가 명령어를 어떻게 끊기지 않고 처리하려 하는지 살펴보았습니다. 하지만 명령어를 실행하려면 연산할 데이터도 필요합니다.

CPU 내부의 연산은 매우 빠르게 끝날 수 있지만, 필요한 데이터가 메인 메모리인 DRAM에 있다면 그 데이터를 가져오는 시간이 문제가 됩니다. 뒤의 연산이 그 데이터를 필요로 한다면 CPU는 값을 받을 때까지 기다려야 하고, 그동안 파이프라인에도 빈 시간이 생깁니다.

이 문제를 줄이기 위해 컴퓨터는 메모리를 하나의 큰 저장 공간으로만 두지 않습니다. CPU 가까이에는 빠르지만 작은 저장 공간을 두고, 멀리에는 느리지만 큰 저장 공간을 둡니다. 이렇게 속도와 용량이 다른 저장 공간을 여러 층으로 배치한 구조가 **메모리 계층 구조**입니다.

이 글에서는 메모리 계층 구조가 왜 필요한지, 캐시가 어떤 원리로 동작하는지, 그리고 게임 코드의 데이터 접근 순서가 성능에 어떤 영향을 주는지 살펴봅니다.

---

## 메모리 계층 피라미드

메모리 계층은 속도와 용량의 균형을 단계적으로 나눈 구조입니다. CPU에 가까운 저장 공간일수록 빠르지만 작고, 멀리 있는 저장 공간일수록 느리지만 더 많은 데이터를 담을 수 있습니다. 이 관계를 한눈에 보기 위해 보통 피라미드 형태로 나타냅니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">메모리 계층 피라미드</text>

  <polygon points="240,42 320,42 334,74 226,74" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="63" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">레지스터</text>

  <polygon points="226,74 334,74 354,108 206,108" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L1 캐시</text>

  <polygon points="206,108 354,108 382,146 178,146" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="132" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L2 캐시</text>

  <polygon points="178,146 382,146 420,188 140,188" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L3 캐시</text>

  <polygon points="140,188 420,188 466,234 94,234" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="216" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DRAM</text>

  <text x="78" y="78" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">CPU에 가까움</text>
  <text x="78" y="94" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">빠름 · 작음</text>
  <line x1="70" y1="106" x2="70" y2="178" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <polygon points="70,100 66,110 74,110" fill="currentColor" opacity="0.45"/>

  <text x="414" y="174" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">CPU에서 멀어짐</text>
  <text x="414" y="190" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">느림 · 큼</text>
  <line x1="404" y1="96" x2="404" y2="166" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <polygon points="404,172 400,162 408,162" fill="currentColor" opacity="0.45"/>

  <text x="280" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">빠른 저장 공간일수록 작고, 큰 저장 공간일수록 느립니다.</text>
</svg>
</div>

<br>

CPU 입장에서는 데이터가 어느 계층에 있는지가 매우 중요합니다. 레지스터나 L1 캐시에 있는 데이터는 거의 바로 사용할 수 있지만, DRAM에 있는 데이터는 훨씬 오래 기다려야 합니다. 같은 연산이라도 필요한 데이터가 가까운 계층에 있으면 빠르게 진행되고, 먼 계층에 있으면 파이프라인이 대기할 수 있습니다.

빠른 저장 공간을 크게 만들기 어려운 이유는 물리적인 비용 때문입니다. 캐시에 주로 쓰이는 SRAM(Static RAM)은 빠르게 읽고 쓸 수 있지만, 같은 면적에 담을 수 있는 데이터가 적습니다. 반대로 DRAM은 훨씬 큰 용량을 만들기 좋지만, 데이터를 읽고 유지하는 과정이 더 복잡해 접근 시간이 길어집니다.

따라서 모든 데이터를 CPU 바로 옆의 빠른 저장 공간에 둘 수는 없습니다. 자주 쓰는 데이터는 작고 빠른 계층에 올려 두고, 큰 데이터는 느리지만 용량이 큰 계층에 보관하는 방식이 필요합니다. 메모리 계층 구조는 이 절충을 시스템 전체에 적용한 형태입니다.

---

## 레지스터

레지스터는 CPU 코어 안에 있는 가장 가까운 저장 공간입니다. ALU(산술 논리 연산 장치)가 값을 더하거나 비교할 때, 입력값을 레지스터에서 읽고 결과도 다시 레지스터에 기록합니다.

메모리 계층에서 레지스터는 가장 빠른 대신 가장 작은 계층입니다. 일반적인 데이터 저장소라기보다, CPU가 지금 당장 계산에 사용할 값을 잠시 올려 두는 작업 공간에 가깝습니다.

레지스터가 항상 계산할 숫자만 담는 것은 아닙니다. CPU가 프로그램의 어느 위치를 실행 중인지 관리하는 값도 레지스터에 들어갑니다.
예를 들어 프로그램 카운터(PC)는 다음에 가져올 명령어의 주소를 저장합니다. 스택 포인터(SP)는 함수 호출과 지역 변수를 관리하는 스택 영역의 현재 위치를 가리킵니다. 이런 레지스터들은 연산 자체보다 CPU의 실행 흐름을 유지하는 데 사용됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 420px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">레지스터와 ALU</text>
  <rect x="28" y="40" width="464" height="160" rx="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="260" y="61" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU 코어 내부</text>

  <rect x="62" y="92" width="150" height="58" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="137" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">레지스터</text>
  <text x="137" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">입력값과 결과 보관</text>

  <rect x="308" y="92" width="150" height="58" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="383" y="114" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">ALU</text>
  <text x="383" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">연산 수행</text>

  <line x1="212" y1="112" x2="304" y2="112" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="308,112 300,108 300,116" fill="currentColor"/>
  <text x="260" y="102" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">값 읽기</text>

  <line x1="308" y1="138" x2="216" y2="138" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="212,138 220,134 220,142" fill="currentColor"/>
  <text x="260" y="157" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">결과 기록</text>

  <text x="260" y="188" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">CPU는 레지스터의 값을 읽어 계산하고, 결과를 다시 레지스터에 남깁니다.</text>
</svg>
</div>

<br>

레지스터가 빠른 이유는 ALU와 매우 가까운 위치에 있고, CPU가 한 명령어를 처리하는 동안 바로 읽고 쓸 수 있도록 설계되어 있기 때문입니다. 좌표 계산, 물리 연산, AI 판단처럼 게임 코드에서 발생하는 중간값도 실제 실행 순간에는 레지스터에 잠시 올라갑니다.

다만 레지스터는 CPU가 지금 처리 중인 값만 담을 수 있을 정도로 작습니다. 캐릭터 목록, 컴포넌트 데이터, 애니메이션 상태, 경로 탐색 데이터처럼 게임에 필요한 대부분의 데이터는 레지스터에 머물 수 없습니다. 이런 데이터는 캐시와 DRAM에 저장되고, CPU는 필요할 때마다 계층을 따라 값을 가져옵니다.

---

## L1, L2, L3 캐시

캐시(Cache)는 CPU와 DRAM 사이의 속도 차이를 줄이기 위한 작은 고속 저장 공간입니다.

CPU는 필요한 데이터를 매번 DRAM에서 직접 가져오지 않습니다. 곧 다시 사용할 가능성이 높은 데이터의 복사본을 캐시에 두고, 같은 데이터나 가까운 위치의 데이터를 다시 읽을 때 캐시에서 먼저 찾습니다. 캐시에 데이터가 있으면 DRAM까지 가지 않아도 되므로 대기 시간이 크게 줄어듭니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 430px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">캐시의 위치</text>

  <rect x="36" y="40" width="488" height="208" rx="6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="280" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>

  <rect x="70" y="82" width="180" height="116" rx="5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="160" y="104" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">코어 0</text>
  <rect x="94" y="120" width="132" height="28" rx="4" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">L1 캐시</text>
  <rect x="94" y="158" width="132" height="28" rx="4" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="176" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">L2 캐시</text>

  <rect x="310" y="82" width="180" height="116" rx="5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="400" y="104" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">코어 1</text>
  <rect x="334" y="120" width="132" height="28" rx="4" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="400" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">L1 캐시</text>
  <rect x="334" y="158" width="132" height="28" rx="4" fill="currentColor" fill-opacity="0.09" stroke="currentColor" stroke-width="1"/>
  <text x="400" y="176" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">L2 캐시</text>

  <rect x="70" y="214" width="420" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="232" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">L3 캐시 (여러 코어가 공유)</text>

  <line x1="280" y1="248" x2="280" y2="282" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="280,286 276,278 284,278" fill="currentColor"/>
  <rect x="170" y="286" width="220" height="38" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="310" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DRAM</text>

  <text x="280" y="334" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">가까운 캐시부터 확인하고, 없으면 더 먼 계층으로 내려갑니다.</text>
</svg>
</div>

### L1 캐시

L1 캐시는 CPU 코어에 가장 가까운 캐시입니다. 보통 코어마다 따로 붙어 있으며, 다른 코어와 공유하지 않습니다. 용량은 작지만 접근 속도가 가장 빠르기 때문에, 현재 실행 중인 코드가 바로 사용할 데이터가 L1에 있으면 파이프라인이 거의 기다리지 않고 진행할 수 있습니다.

L1 캐시는 보통 명령어 캐시와 데이터 캐시로 나뉩니다. 명령어 캐시는 CPU가 실행할 명령어를 보관하고, 데이터 캐시는 연산에 사용할 값을 보관합니다. 이렇게 나누어 두면 명령어를 가져오는 작업과 데이터를 읽고 쓰는 작업이 서로 덜 방해받습니다.

게임 코드에서는 반복문 안에서 순차적으로 처리하는 작은 데이터 구간이 L1 캐시에 올라오는 경우가 많습니다. 현재 처리 중인 배열 구간이나 구조체 일부가 L1에 들어와 있으면, CPU는 같은 데이터를 매우 빠르게 반복해서 사용할 수 있습니다.

### L2 캐시

L2 캐시는 L1보다 크지만 조금 더 느린 계층입니다. L1에 원하는 데이터가 없을 때, CPU는 바로 DRAM으로 가지 않고 먼저 L2를 확인합니다.

L2는 L1보다 더 넓은 작업 구간을 담을 수 있습니다. L1에서 밀려난 데이터라도 L2에는 남아 있을 수 있으므로, DRAM까지 내려가지 않고 다시 가져올 기회를 제공합니다. 반복문이 다루는 데이터가 L1에는 다 들어가지 않더라도 L2에 머물 수 있다면, 메인 메모리 접근을 크게 줄일 수 있습니다.

### L3 캐시

L3 캐시는 여러 코어가 함께 사용하는 더 큰 캐시입니다. L1과 L2가 코어 가까이에 붙어 있는 전용 공간이라면, L3는 코어들 사이에서 공유되는 완충 공간에 가깝습니다.

한 코어가 가져온 데이터가 L3에 남아 있으면, 다른 코어가 같은 데이터를 필요로 할 때 DRAM까지 내려가지 않고 L3에서 찾을 수 있습니다. 물리 시뮬레이션이나 잡 시스템처럼 여러 코어가 관련 데이터를 함께 다루는 경우, L3 캐시는 코어 사이의 데이터 재사용 비용을 줄이는 데 도움이 됩니다.

### 캐시 조회 순서

CPU가 데이터를 필요로 하면 가장 가까운 L1 캐시부터 확인합니다. L1에 없으면 L2, L3 순서로 내려가고, 어느 캐시에도 없을 때 DRAM에서 데이터를 가져옵니다.

캐시에 원하는 데이터가 있는 경우를 **캐시 히트(Cache Hit)**라고 하고, 없어서 더 아래 계층을 찾아야 하는 경우를 **캐시 미스(Cache Miss)**라고 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 430px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데이터 조회 흐름</text>

  <rect x="40" y="50" width="96" height="42" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="88" y="75" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU 요청</text>

  <line x1="136" y1="71" x2="168" y2="71" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="172,71 164,67 164,75" fill="currentColor"/>

  <rect x="172" y="50" width="78" height="42" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="211" y="75" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L1</text>
  <line x1="250" y1="71" x2="282" y2="71" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="286,71 278,67 278,75" fill="currentColor"/>
  <text x="268" y="62" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">미스</text>

  <rect x="286" y="50" width="78" height="42" rx="5" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.2"/>
  <text x="325" y="75" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L2</text>
  <line x1="364" y1="71" x2="396" y2="71" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="400,71 392,67 392,75" fill="currentColor"/>
  <text x="382" y="62" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">미스</text>

  <rect x="400" y="50" width="78" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="439" y="75" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">L3</text>
  <line x1="439" y1="92" x2="439" y2="126" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="439,130 435,122 443,122" fill="currentColor"/>
  <text x="454" y="116" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">미스</text>

  <rect x="376" y="130" width="126" height="42" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="439" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DRAM</text>

  <path d="M 376 151 H 211 V 96" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4,3" opacity="0.75"/>
  <polygon points="211,92 207,100 215,100" fill="currentColor" opacity="0.75"/>
  <text x="286" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">가져온 데이터를 캐시에 보관</text>

  <rect x="172" y="214" width="78" height="34" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="211" y="235" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">히트</text>
  <text x="268" y="235" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">데이터를 찾으면 바로 반환</text>

  <rect x="172" y="254" width="78" height="34" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.75"/>
  <text x="211" y="275" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">미스</text>
  <text x="268" y="275" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">없으면 다음 계층으로 이동</text>
</svg>
</div>

<br>

캐시에서 데이터를 찾으면 CPU는 비교적 짧은 대기 후 연산을 이어갈 수 있습니다. 반대로 모든 캐시에서 미스가 발생해 DRAM까지 내려가면 대기 시간이 크게 늘어납니다.

이 차이가 누적되면 같은 코드라도 실행 시간이 크게 달라집니다. 특히 반복문 안에서 매번 DRAM까지 내려가는 접근 패턴이 생기면, CPU는 연산보다 데이터를 기다리는 데 더 많은 시간을 쓰게 됩니다.

---

## 캐시의 동작 원리

CPU가 메모리에서 데이터를 가져올 때는 요청한 값 하나만 따로 가져오지 않습니다. 그 값이 들어 있는 주변 메모리까지 묶어서 캐시에 올립니다.

이때 캐시에 들어오는 고정 크기의 데이터 블록을 **캐시 라인(Cache Line)**이라고 합니다. 많은 CPU에서 캐시 라인은 64바이트 단위로 사용됩니다. 즉, 어떤 주소의 4바이트 정수 하나를 읽더라도, 캐시에는 그 주변 데이터까지 함께 들어올 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">캐시 라인</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">CPU가 특정 값을 요청하면, 그 값이 속한 블록 전체가 캐시에 올라옵니다.</text>

  <rect x="52" y="76" width="456" height="48" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="280" y="67" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">메모리의 한 캐시 라인</text>
  <line x1="52" y1="76" x2="52" y2="124" stroke="currentColor" stroke-width="1"/>
  <line x1="508" y1="76" x2="508" y2="124" stroke="currentColor" stroke-width="1"/>

  <rect x="80" y="88" width="86" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="123" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">주변 데이터</text>

  <rect x="180" y="88" width="86" height="24" rx="3" fill="currentColor" fill-opacity="0.26" stroke="currentColor" stroke-width="1.2"/>
  <text x="223" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">요청한 값</text>

  <rect x="280" y="88" width="86" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="323" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">주변 데이터</text>

  <rect x="380" y="88" width="86" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="423" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">주변 데이터</text>

  <line x1="223" y1="114" x2="223" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="223,152 219,144 227,144" fill="currentColor"/>
  <text x="232" y="138" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">요청</text>

  <rect x="92" y="154" width="376" height="38" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.4"/>
  <text x="280" y="177" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">캐시에 저장되는 단위: 캐시 라인</text>
  <text x="280" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">요청한 값만 따로 저장하지 않고, 같은 블록의 주변 데이터도 함께 저장합니다.</text>
</svg>
</div>

<br>

캐시는 메모리를 일정한 크기의 블록으로 나누어 다룹니다. CPU가 어떤 값을 요청하면, 캐시는 그 값만 따로 가져오는 것이 아니라 그 값이 들어 있는 블록 전체를 가져옵니다.

따라서 요청한 값이 블록의 앞쪽에 있든 중간에 있든, 캐시에 올라오는 범위는 같습니다. 캐시가 데이터를 관리하는 기본 단위가 개별 변수나 바이트가 아니라 캐시 라인이기 때문입니다.

캐시가 블록 단위로 데이터를 가져오는 이유는 메모리 접근이 대개 한 지점에서 끝나지 않기 때문입니다. 배열처럼 연속된 데이터를 처리할 때는 하나의 값을 읽은 뒤 바로 옆의 값을 이어서 읽는 경우가 많습니다. 이때 주변 데이터가 이미 캐시에 올라와 있으면 다음 접근은 DRAM까지 내려가지 않아도 됩니다.

캐시 라인이 너무 작으면 근처 데이터를 충분히 활용하지 못해 캐시 미스가 자주 발생합니다. 반대로 너무 크면 실제로 쓰지 않을 데이터까지 많이 가져와 캐시 공간을 차지합니다. 많은 CPU에서 사용하는 64바이트 캐시 라인은 이 두 부담 사이에서 정해진 크기에 가깝습니다.

이 장점이 잘 드러나는 예가 배열 순차 접근입니다. 배열의 첫 번째 요소를 읽을 때 해당 캐시 라인이 함께 올라오면, 같은 캐시 라인에 들어 있는 다음 요소들은 DRAM까지 내려가지 않고 캐시에서 읽을 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 430px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">배열 순차 접근과 캐시 라인</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">연속된 배열 요소는 같은 캐시 라인에 함께 들어올 수 있습니다.</text>

  <text x="52" y="74" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">메모리의 배열</text>
  <rect x="52" y="84" width="72" height="34" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1.2"/>
  <text x="88" y="105" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="currentColor">arr[0]</text>
  <rect x="124" y="84" width="72" height="34" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="160" y="105" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">arr[1]</text>
  <rect x="196" y="84" width="72" height="34" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="232" y="105" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">arr[2]</text>
  <rect x="268" y="84" width="112" height="34" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="324" y="105" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">...</text>
  <rect x="380" y="84" width="72" height="34" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="416" y="105" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">arr[n]</text>

  <line x1="88" y1="118" x2="88" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="88,152 84,144 92,144" fill="currentColor"/>
  <text x="102" y="138" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">읽기</text>

  <rect x="52" y="154" width="400" height="42" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="252" y="147" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">캐시에 올라온 캐시 라인</text>
  <text x="252" y="179" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">arr[0]과 인접한 요소들이 함께 캐시에 저장됨</text>

  <rect x="52" y="212" width="122" height="26" rx="4" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="113" y="229" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">첫 접근: 미스</text>
  <rect x="190" y="212" width="170" height="26" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="275" y="229" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">인접 요소 접근: 히트</text>
  <text x="384" y="229" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">이 흐름이 반복됨</text>
</svg>
</div>

<br>

순차 접근에서는 처음 요소를 읽을 때 캐시 미스가 나더라도, 같은 캐시 라인에 들어 있는 다음 요소들은 캐시에서 바로 읽을 수 있습니다. 배열을 앞에서부터 차례대로 처리하는 코드가 캐시에 유리한 이유입니다.

---

## 공간적 지역성과 시간적 지역성

캐시가 성능에 도움이 되려면, 한 번 가져온 데이터가 곧 다시 쓰이거나 그 주변 데이터가 이어서 쓰여야 합니다. 이런 접근 경향을 **지역성(Locality)**이라고 합니다.

지역성은 보통 두 가지로 나누어 설명합니다. 가까운 주소의 데이터를 이어서 사용하는 **공간적 지역성(Spatial Locality)**과, 같은 데이터를 짧은 시간 안에 다시 사용하는 **시간적 지역성(Temporal Locality)**입니다.

### 공간적 지역성

공간적 지역성은 가까운 주소에 있는 데이터를 이어서 사용하는 경향입니다. 배열을 앞에서부터 차례대로 읽는 코드가 대표적입니다.

예를 들어 적 캐릭터의 위치가 `positions` 배열에 연속으로 저장되어 있고, 매 프레임 앞에서부터 순서대로 갱신된다고 하겠습니다. 첫 번째 위치 값을 읽을 때 그 주변 위치 값들도 같은 캐시 라인에 함께 올라올 수 있습니다.

이후 다음 위치 값을 읽을 때는 이미 캐시에 들어 있는 데이터를 사용할 가능성이 높습니다. 그래서 연속된 배열을 순차적으로 처리하는 코드는 DRAM 접근을 줄이기 쉽습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">공간적 지역성</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">가까운 주소의 데이터를 이어서 사용하는 접근 패턴</text>

  <text x="52" y="72" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">연속된 메모리 배치</text>
  <rect x="52" y="82" width="76" height="34" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="103" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[0]</text>
  <rect x="128" y="82" width="76" height="34" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="166" y="103" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[1]</text>
  <rect x="204" y="82" width="76" height="34" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="242" y="103" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[2]</text>
  <rect x="280" y="82" width="76" height="34" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="318" y="103" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[3]</text>
  <rect x="356" y="82" width="76" height="34" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="394" y="103" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[4]</text>
  <rect x="432" y="82" width="76" height="34" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="470" y="103" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">pos[5]</text>

  <path d="M 88 138 H 470" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="474,138 466,134 466,142" fill="currentColor"/>
  <text x="280" y="132" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">순서대로 접근</text>

  <rect x="92" y="162" width="376" height="34" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">한 번 올라온 캐시 라인의 인접 데이터를 계속 활용</text>
</svg>
</div>

### 시간적 지역성

시간적 지역성은 같은 데이터를 짧은 시간 안에 다시 사용하는 경향입니다.

예를 들어 플레이어 위치 값은 한 프레임 안에서도 여러 번 필요할 수 있습니다. 이동 처리에서 값을 갱신한 뒤, 충돌 판정이나 카메라 추적에서도 같은 위치 값을 다시 읽을 수 있습니다.

처음 접근할 때 캐시에 올라온 데이터가 잠시 뒤에도 남아 있다면, 다음 접근은 DRAM까지 내려가지 않고 캐시에서 처리됩니다. 같은 값을 반복해서 읽는 코드가 캐시에 유리한 이유입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">시간적 지역성</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">같은 데이터를 짧은 시간 안에 반복해서 사용하는 접근 패턴</text>

  <rect x="52" y="74" width="160" height="46" rx="5" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="132" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">첫 접근</text>
  <text x="132" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.85">playerPosition</text>

  <line x1="212" y1="97" x2="254" y2="97" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="258,97 250,93 250,101" fill="currentColor"/>
  <text x="235" y="88" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">캐시에 저장</text>

  <rect x="258" y="74" width="120" height="46" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="318" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐시</text>
  <text x="318" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">최근 데이터 유지</text>

  <line x1="378" y1="97" x2="420" y2="97" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="424,97 416,93 416,101" fill="currentColor"/>
  <text x="400" y="88" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">재사용</text>

  <rect x="424" y="74" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="474" y="94" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">다음 접근</text>
  <text x="474" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">캐시 히트</text>

  <rect x="94" y="154" width="372" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="177" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">같은 값이 캐시에 남아 있으면 DRAM 접근을 줄일 수 있습니다.</text>
</svg>
</div>

<br>

캐시는 이런 지역성이 있는 코드에서 가장 효과적으로 동작합니다. 연속된 데이터를 차례대로 읽거나, 방금 읽은 데이터를 곧 다시 사용하면 캐시 히트가 늘어나고 DRAM 접근은 줄어듭니다.

반대로 접근 위치가 계속 흩어지거나 한 번 읽은 데이터를 다시 사용하지 않는다면, 캐시에 올린 데이터가 충분히 활용되지 못합니다. 이런 상황에서는 캐시에서 원하는 데이터를 찾지 못하는 **캐시 미스(Cache Miss)**가 자주 발생합니다.

---

## 캐시 미스의 종류와 비용

CPU가 필요한 데이터를 캐시에서 찾지 못하는 상황을 **캐시 미스(Cache Miss)**라고 합니다.

캐시 미스가 발생하면 CPU는 더 아래의 메모리 계층에서 데이터를 가져와야 합니다. L1에 없으면 L2를 확인하고, L2에도 없으면 L3나 DRAM까지 내려갑니다. 그동안 해당 값을 필요로 하는 명령어는 계속 진행할 수 없습니다.

캐시 미스는 왜 원하는 데이터가 캐시에 없었는지에 따라 몇 가지 유형으로 나누어 볼 수 있습니다.

### Cold Miss (콜드 미스)

콜드 미스는 프로그램이 어떤 데이터를 처음 접근할 때 발생합니다. 아직 그 데이터가 캐시에 올라온 적이 없으므로, 캐시가 아무리 잘 동작해도 첫 접근에서는 미스가 날 수밖에 없습니다.

그래서 콜드 미스는 **강제 미스(Compulsory Miss)**라고도 부릅니다. 처음 읽는 데이터는 하위 계층에서 가져와야 하고, 그 과정에서 해당 캐시 라인이 캐시에 채워집니다.

게임에서는 새 씬을 로드한 직후나 첫 프레임에서 이런 미스가 몰릴 수 있습니다. 텍스처, 메시, 컴포넌트 데이터처럼 아직 접근하지 않았던 데이터가 처음 사용되기 때문입니다. 다만 같은 데이터에 대한 콜드 미스는 최초 접근에서만 발생합니다.

### Capacity Miss (용량 미스)

용량 미스는 작업 중에 사용하는 데이터가 캐시에 담을 수 있는 양보다 많을 때 발생합니다.

캐시는 공간이 부족해지면 기존에 들어 있던 캐시 라인 일부를 내보내고 새 데이터를 채웁니다. 이 과정을 **축출(eviction)**이라고 합니다.

문제는 내보낸 데이터를 다시 필요로 할 때입니다. 한 번 캐시에 올라왔던 데이터라도 이미 밀려난 뒤라면, CPU는 그 데이터를 하위 계층에서 다시 가져와야 합니다.

작업 대상이 많고 각 대상의 데이터가 크면 이런 상황이 쉽게 생깁니다. 예를 들어 많은 적 캐릭터의 상태를 순회하는 동안, 앞쪽 캐릭터의 데이터가 캐시에 올라왔다가 뒤쪽 캐릭터를 처리하는 사이 밀려날 수 있습니다. 이후 앞쪽 데이터를 다시 참조하면 캐시에 남아 있지 않아 용량 미스가 발생합니다.

### Conflict Miss (충돌 미스)

충돌 미스는 캐시에 빈 공간이 남아 있는데도 특정 데이터가 밀려나는 경우입니다. 캐시 라인이 캐시 안의 아무 위치에나 들어갈 수 있는 것은 아니기 때문입니다.

캐시는 메모리 주소를 기준으로 각 캐시 라인이 들어갈 구역을 정합니다. 이 구역을 **set**이라고 합니다. 같은 set으로 배정된 캐시 라인들은 서로 같은 공간을 나누어 써야 합니다.

set 하나가 동시에 담을 수 있는 캐시 라인 수는 제한되어 있습니다. 이 개수를 **way**라고 부릅니다. 예를 들어 8-way 캐시에서는 같은 set 안에 캐시 라인 8개까지 보관할 수 있습니다.

문제는 서로 다른 데이터가 계속 같은 set으로 배정될 때 생깁니다. 캐시 전체에는 여유가 있어도 해당 set이 이미 가득 차 있다면, 새 캐시 라인을 넣기 위해 기존 캐시 라인을 밀어내야 합니다. 이후 밀려난 데이터를 다시 읽으면 충돌 미스가 발생합니다.

### 캐시 미스의 비용

캐시 미스가 발생하면 CPU는 더 느린 계층에서 데이터가 도착할 때까지 기다려야 합니다. 해당 데이터가 필요한 명령어는 값을 받기 전까지 실행을 마칠 수 없습니다.

이 대기는 [이전 글](/dev/unity/HardwareBasics-1/)에서 다룬 **파이프라인 스톨(stall)**로 이어질 수 있습니다. 데이터 접근이 빠르게 끝나면 파이프라인은 곧바로 이어지지만, DRAM까지 내려가야 하면 그만큼 빈 시간이 길어집니다.

CPU의 연산 장치가 충분히 빠르더라도, 필요한 데이터가 제때 도착하지 않으면 다음 계산을 진행할 수 없습니다. 캐시 미스가 성능에 큰 영향을 주는 이유는 연산 자체보다 데이터를 기다리는 시간이 길어질 수 있기 때문입니다.

out-of-order 실행을 지원하는 CPU는 이 손실을 어느 정도 줄일 수 있습니다. 어떤 데이터가 도착하기를 기다리는 동안, 그 데이터에 의존하지 않는 다른 명령어를 먼저 실행할 수 있기 때문입니다.

하지만 캐시 미스가 계속 이어지면 이 방식에도 한계가 있습니다. 기다리는 명령어가 쌓이고, 독립적으로 먼저 처리할 수 있는 명령어가 부족해지면 CPU는 결국 데이터가 도착할 때까지 멈춰 서게 됩니다.

---

## 메모리 접근 패턴이 성능에 미치는 영향

캐시 미스를 줄이려면 어떤 데이터를 읽는지뿐 아니라, 어떤 순서로 읽는지도 중요합니다. 처리하는 데이터의 양이 같아도 접근 순서가 달라지면 캐시 히트율이 크게 달라질 수 있습니다.

차이가 가장 잘 드러나는 예가 **순차 접근**과 **랜덤 접근**입니다.

### 순차 접근 vs 랜덤 접근

순차 접근은 메모리에 연속으로 배치된 데이터를 차례대로 읽는 방식입니다. 배열을 앞에서부터 끝까지 순서대로 순회하는 경우가 대표적입니다.

랜덤 접근은 다음에 읽을 데이터가 현재 위치 근처에 있다고 기대하기 어려운 접근 방식입니다. 연결 리스트(Linked List)를 포인터를 따라 순회하는 경우가 대표적입니다.

연결 리스트의 각 노드는 다음 노드의 주소를 따로 가지고 있습니다. 노드들이 메모리상에서 서로 떨어진 위치에 할당되어 있으면, 현재 노드를 읽어도 다음 노드가 같은 캐시 라인이나 가까운 주소에 있을 가능성이 낮습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">순차 접근의 캐시 활용</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">연속된 배열을 차례대로 읽으면 같은 캐시 라인을 재사용합니다.</text>

  <rect x="54" y="76" width="80" height="34" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.2"/>
  <text x="94" y="97" text-anchor="middle" font-family="monospace" font-size="10" font-weight="bold" fill="currentColor">data[0]</text>
  <rect x="134" y="76" width="80" height="34" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="174" y="97" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[1]</text>
  <rect x="214" y="76" width="80" height="34" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="254" y="97" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[2]</text>
  <rect x="294" y="76" width="80" height="34" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="334" y="97" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">data[3]</text>
  <rect x="374" y="76" width="92" height="34" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="420" y="97" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">...</text>

  <line x1="94" y1="112" x2="94" y2="144" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="94,148 90,140 98,140" fill="currentColor"/>
  <text x="112" y="134" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">첫 접근</text>

  <rect x="70" y="150" width="134" height="32" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.1"/>
  <text x="137" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">캐시 라인 로드</text>
  <rect x="226" y="150" width="184" height="32" rx="5" fill="currentColor" fill-opacity="0.07" stroke="currentColor" stroke-width="1.1"/>
  <text x="318" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">인접 요소는 캐시 히트</text>

  <text x="280" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">다음 캐시 라인에서도 같은 패턴이 반복됩니다.</text>
</svg>
</div>

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">랜덤 접근의 캐시 활용</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">다음 데이터가 멀리 떨어져 있으면 캐시 라인을 재사용하기 어렵습니다.</text>

  <rect x="54" y="78" width="92" height="34" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="100" y="99" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">node A</text>

  <rect x="238" y="64" width="92" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="284" y="85" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">node B</text>

  <rect x="394" y="98" width="92" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="440" y="119" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">node C</text>

  <path d="M 146 95 C 180 60 206 54 238 76" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="238,76 230,72 232,82" fill="currentColor"/>
  <path d="M 330 82 C 360 88 374 100 394 112" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="394,112 386,106 386,116" fill="currentColor"/>

  <rect x="70" y="158" width="126" height="30" rx="5" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="1.1"/>
  <text x="133" y="177" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">각 노드에서 미스 가능</text>
  <rect x="220" y="158" width="252" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.1"/>
  <text x="346" y="177" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">가져온 캐시 라인의 주변 데이터 재사용이 어려움</text>

  <text x="280" y="214" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">포인터를 따라 이동할 때마다 다른 캐시 라인이 필요할 수 있습니다.</text>
</svg>
</div>

<br>

순차 접근은 한 번 가져온 캐시 라인 안의 데이터를 이어서 활용하기 쉽습니다. 그래서 첫 접근에서 미스가 발생하더라도, 같은 캐시 라인에 있는 다음 데이터는 캐시에서 읽을 가능성이 높습니다.

반대로 랜덤 접근은 매번 다른 위치로 이동하기 쉽습니다. 이전 접근에서 가져온 캐시 라인의 주변 데이터가 다음 접근에 도움이 되지 않으면, 캐시 라인을 새로 가져오는 일이 반복됩니다.

결국 같은 양의 데이터를 처리하더라도 순차 접근은 캐시 히트가 늘어나고, 랜덤 접근은 캐시 미스가 늘어날 수 있습니다. 이 차이가 반복문 안에서 누적되면 CPU 시간 차이로 나타납니다.

### Array of Structs vs Struct of Arrays

캐시 효율은 자료구조의 종류만으로 결정되지 않습니다. 배열을 사용하더라도, 실제로 필요한 데이터가 메모리에 어떻게 섞여 있는지에 따라 캐시 라인의 활용도가 달라집니다.

게임 코드에서 이 차이가 자주 드러나는 지점이 **AoS(Array of Structs)**와 **SoA(Struct of Arrays)** 데이터 배치입니다.

먼저 AoS는 한 개체가 가진 여러 값을 하나의 구조체에 모으고, 그 구조체를 배열로 저장하는 방식입니다. 적 캐릭터의 위치, 속도, 체력, 상태를 함께 저장하면 다음과 같은 형태가 됩니다.

<br>

```csharp
struct Enemy {
    Vector3 position;
    Vector3 velocity;
    float   health;
    int     state;
}

Enemy[] enemies = new Enemy[1000];
```

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Array of Structs (AoS)</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">개체 하나의 필드가 한 덩어리로 묶여 반복됩니다.</text>

  <rect x="48" y="68" width="206" height="52" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="151" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">enemy[0]</text>
  <text x="82" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos</text>
  <text x="128" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">vel</text>
  <text x="179" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">health</text>
  <text x="226" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">state</text>

  <rect x="280" y="68" width="206" height="52" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="383" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">enemy[1]</text>
  <text x="314" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos</text>
  <text x="360" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">vel</text>
  <text x="411" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">health</text>
  <text x="458" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">state</text>

  <rect x="110" y="142" width="340" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="159" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">position만 필요해도 velocity, health, state가 함께 캐시 라인에 들어올 수 있음</text>
</svg>
</div>

<br>

SoA는 개체별로 데이터를 묶지 않고, 같은 종류의 값끼리 별도의 배열로 분리해 저장하는 방식입니다. 위치만 갱신하는 코드라면 `positions` 배열만 순차적으로 읽을 수 있습니다.

<br>

```csharp
Vector3[] positions  = new Vector3[1000];
Vector3[] velocities = new Vector3[1000];
float[]   healths    = new float[1000];
int[]     states     = new int[1000];
```

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Struct of Arrays (SoA)</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">같은 종류의 값이 별도 배열에 연속으로 저장됩니다.</text>

  <text x="56" y="76" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">positions</text>
  <rect x="136" y="60" width="300" height="28" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="286" y="79" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos[0]  pos[1]  pos[2]  pos[3]  ...</text>

  <text x="56" y="116" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">velocities</text>
  <rect x="136" y="100" width="300" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="286" y="119" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">vel[0]  vel[1]  vel[2]  vel[3]  ...</text>

  <text x="56" y="156" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">healths</text>
  <rect x="136" y="140" width="300" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="286" y="159" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">hp[0]   hp[1]   hp[2]   hp[3]   ...</text>

  <rect x="118" y="184" width="324" height="20" rx="4" fill="currentColor" fill-opacity="0.06"/>
  <text x="280" y="198" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">위치 갱신처럼 필요한 배열만 순차적으로 접근할 수 있음</text>
</svg>
</div>

<br>

적의 위치를 갱신하는 루프에서는 보통 `position`과 `velocity`만 필요합니다. `health`나 `state`는 같은 적 데이터에 들어 있어도, 이 작업에서는 사용하지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">AoS에서 위치 갱신</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">필요한 필드와 필요하지 않은 필드가 같은 구조체 안에 섞여 있습니다.</text>

  <rect x="52" y="72" width="206" height="48" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="155" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">enemy[0]</text>
  <text x="86" y="110" text-anchor="middle" font-family="monospace" font-size="9" font-weight="bold" fill="currentColor">pos</text>
  <text x="132" y="110" text-anchor="middle" font-family="monospace" font-size="9" font-weight="bold" fill="currentColor">vel</text>
  <text x="184" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.55">health</text>
  <text x="230" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.55">state</text>

  <rect x="302" y="72" width="206" height="48" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="405" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">enemy[1]</text>
  <text x="336" y="110" text-anchor="middle" font-family="monospace" font-size="9" font-weight="bold" fill="currentColor">pos</text>
  <text x="382" y="110" text-anchor="middle" font-family="monospace" font-size="9" font-weight="bold" fill="currentColor">vel</text>
  <text x="434" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.55">health</text>
  <text x="480" y="110" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.55">state</text>

  <rect x="104" y="152" width="352" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="174" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">위치 갱신에는 pos와 vel만 필요하지만, health와 state도 함께 들어올 수 있음</text>
</svg>
</div>

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SoA에서 위치 갱신</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">필요한 필드가 별도 배열에 모여 있어 순차 접근하기 쉽습니다.</text>

  <text x="72" y="82" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">positions</text>
  <rect x="160" y="64" width="300" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="84" text-anchor="middle" font-family="monospace" font-size="9" font-weight="bold" fill="currentColor">pos[0]  pos[1]  pos[2]  pos[3]  ...</text>

  <text x="72" y="124" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">velocities</text>
  <rect x="160" y="106" width="300" height="30" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="126" text-anchor="middle" font-family="monospace" font-size="9" font-weight="bold" fill="currentColor">vel[0]  vel[1]  vel[2]  vel[3]  ...</text>

  <rect x="104" y="166" width="352" height="34" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="188" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">위치 갱신에 필요한 배열만 캐시 라인에 올라옴</text>
</svg>
</div>

<br>

AoS 방식에서는 위치 갱신에 필요하지 않은 `health`, `state`도 같은 구조체에 들어 있으므로 캐시 라인에 함께 올라올 수 있습니다. 반면 SoA 방식에서는 `positions`와 `velocities`처럼 필요한 배열만 순차적으로 접근할 수 있습니다.

따라서 특정 필드만 대량으로 처리하는 루프에서는 SoA가 캐시 라인을 더 효율적으로 사용할 수 있습니다. 단, 항상 SoA가 더 좋은 것은 아닙니다. 한 개체의 여러 필드를 한꺼번에 자주 읽는 코드라면 AoS가 더 단순하고 접근 패턴도 나쁘지 않을 수 있습니다.

<br>

Unity의 DOTS(Data-Oriented Technology Stack)와 ECS(Entity Component System)도 이 관점에서 이해할 수 있습니다.

ECS는 데이터를 오브젝트 단위로 흩어 두기보다, 같은 조합의 컴포넌트를 가진 엔티티들을 청크(Chunk) 단위로 모아 저장합니다. 시스템은 자신에게 필요한 컴포넌트 집합만 순회하므로, 접근 패턴이 연속적인 데이터 처리에 가까워집니다.

예를 들어 위치 갱신 시스템은 위치와 속도에 해당하는 컴포넌트를 중심으로 순회합니다. 이 구조에서는 작업에 필요하지 않은 데이터가 캐시 라인에 섞이는 일을 줄이고, 같은 종류의 데이터를 연속적으로 처리하기 쉬워집니다.

---

## 대역폭과 지연의 차이

캐시 히트가 늘어나면 느린 메모리 접근을 줄일 수 있습니다. 하지만 메모리 성능은 캐시 히트율만으로 설명되지 않습니다.

캐시에 없는 데이터를 읽거나 큰 데이터를 연속으로 옮길 때는 메모리 자체의 성능이 중요해집니다. 이 성능은 데이터를 요청한 뒤 도착하기까지의 시간인 **지연(Latency)**과, 일정 시간 동안 옮길 수 있는 데이터의 양인 **대역폭(Bandwidth)**으로 나누어 볼 수 있습니다.

지연은 메모리 요청 하나가 완료되기까지 걸리는 시간입니다. 포인터를 따라 다음 노드로 이동하는 코드처럼, 현재 데이터를 읽어야 다음 주소를 알 수 있는 경우에는 요청을 겹치기 어렵습니다. 이런 코드는 데이터가 도착할 때까지 다음 단계로 진행하기 어렵기 때문에 지연의 영향을 크게 받습니다.

대역폭은 일정 시간 동안 옮길 수 있는 데이터의 양입니다. 큰 배열을 순차적으로 처리하거나 정점, 텍스처처럼 큰 데이터를 전송하는 작업에서는 개별 요청의 대기 시간보다 전체 데이터 전송량이 더 중요해질 수 있습니다.

따라서 지연 병목은 다음 데이터가 도착하기를 기다리는 문제에 가깝고, 대역폭 병목은 옮겨야 할 데이터량이 전송 능력을 넘어서는 문제에 가깝습니다. 게임 코드에서는 접근 패턴에 따라 어느 쪽이 더 크게 드러나는지가 달라집니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">지연 병목과 대역폭 병목</text>

  <text x="52" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">지연 병목</text>
  <rect x="52" y="66" width="82" height="32" rx="4" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="93" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">요청</text>
  <line x1="134" y1="82" x2="190" y2="82" stroke="currentColor" stroke-width="1.3" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="162" y="74" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">대기</text>
  <polygon points="194,82 186,78 186,86" fill="currentColor"/>
  <rect x="194" y="66" width="82" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="235" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">응답</text>
  <line x1="276" y1="82" x2="332" y2="82" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="336,82 328,78 328,86" fill="currentColor"/>
  <rect x="336" y="66" width="104" height="32" rx="4" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="388" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">다음 요청</text>
  <text x="280" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">이전 응답이 와야 다음 요청을 보낼 수 있는 흐름</text>

  <line x1="52" y1="148" x2="508" y2="148" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>

  <text x="52" y="180" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">대역폭 병목</text>
  <rect x="52" y="198" width="74" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <rect x="136" y="198" width="74" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <rect x="220" y="198" width="74" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <rect x="304" y="198" width="74" height="28" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="89" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">데이터</text>
  <text x="173" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">데이터</text>
  <text x="257" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">데이터</text>
  <text x="341" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">데이터</text>
  <line x1="378" y1="212" x2="452" y2="212" stroke="currentColor" stroke-width="3" opacity="0.55"/>
  <polygon points="458,212 446,206 446,218" fill="currentColor" opacity="0.75"/>
  <rect x="458" y="196" width="70" height="32" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="493" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">처리</text>
  <text x="280" y="258" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">요청은 이어지지만, 옮겨야 할 데이터량이 전송 능력을 채우는 흐름</text>
</svg>
</div>

### 프리페치(Prefetch)

순차 접근이 지연의 영향을 덜 받는 이유 중 하나는 **프리페치(Prefetch)**입니다.

CPU의 하드웨어 프리페처(Hardware Prefetcher)는 메모리 접근이 일정한 방향으로 이어지는지 감지합니다. 예를 들어 배열을 앞에서부터 차례대로 읽고 있다면, CPU는 다음에도 그 뒤쪽 주소를 읽을 가능성이 높다고 판단할 수 있습니다.

이때 프리페처는 현재 캐시 라인을 처리하는 동안 다음 캐시 라인을 미리 가져오려고 합니다. 예측이 맞으면 다음 캐시 라인이 필요해지는 시점에는 이미 캐시에 들어와 있으므로, CPU가 메모리 응답을 기다리는 시간이 줄어듭니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 420px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프리페치의 동작</text>
  <text x="280" y="42" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">현재 데이터를 처리하는 동안 다음 캐시 라인을 미리 가져옵니다.</text>

  <text x="58" y="78" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">현재</text>
  <rect x="112" y="60" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="172" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">캐시 라인 처리</text>

  <line x1="232" y1="78" x2="304" y2="78" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="308,78 300,74 300,82" fill="currentColor"/>
  <text x="270" y="68" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">패턴 감지</text>

  <rect x="308" y="60" width="158" height="36" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="387" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">다음 캐시 라인 요청</text>

  <line x1="387" y1="96" x2="387" y2="136" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4,3"/>
  <polygon points="387,140 383,132 391,132" fill="currentColor"/>

  <text x="58" y="158" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">다음</text>
  <rect x="112" y="142" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="172" y="164" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">다음 라인 필요</text>

  <rect x="308" y="142" width="158" height="36" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="387" y="164" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">이미 캐시에 있음</text>

  <rect x="96" y="210" width="368" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="280" y="229" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">예측이 맞으면 다음 접근의 대기 시간이 줄어듭니다.</text>
</svg>
</div>

<br>

프리페치가 효과를 내려면 접근 패턴이 어느 정도 예측 가능해야 합니다. 배열을 순서대로 읽는 코드는 다음 주소를 예상하기 쉽기 때문에 프리페치가 잘 맞는 편입니다.

반대로 포인터를 따라 이동하거나 접근 위치가 계속 바뀌는 코드는 다음 주소를 미리 알기 어렵습니다. 이런 경우에는 프리페치가 충분히 앞서 움직이기 어렵고, 캐시 미스의 지연이 그대로 드러나기 쉽습니다.

따라서 순차 접근이 빠른 이유에는 캐시 라인 재사용뿐 아니라, 다음 데이터를 미리 가져올 수 있는 프리페치의 효과도 포함됩니다.

### 모바일과 GPU에서의 대역폭 제약

프리페치가 잘 맞아도, 옮겨야 할 데이터의 양 자체가 많으면 대역폭이 병목이 됩니다. 이 문제는 GPU 작업과 모바일 환경에서 특히 중요합니다.

GPU는 매 프레임 텍스처, 정점, 렌더 타깃 데이터를 계속 읽고 씁니다. 화면 해상도가 높고 후처리 단계가 많을수록 메모리에서 오가는 데이터도 늘어납니다.

모바일에서는 이 대역폭을 더 조심해서 써야 합니다. 모바일 SoC는 CPU와 GPU가 같은 시스템 메모리를 공유하는 경우가 많고, 배터리와 발열 제약 때문에 메모리 대역폭을 무작정 넓히기 어렵습니다. GPU가 많은 텍스처 샘플링이나 렌더 타깃 쓰기를 요구하면, 같은 메모리를 쓰는 CPU 작업에도 영향이 갈 수 있습니다.

그래서 모바일 그래픽스에서는 대역폭을 줄이는 전략이 중요합니다. 텍스처 압축, 적절한 렌더 타깃 포맷, 불필요한 후처리 감소, 오버드로우 감소는 모두 메모리에서 오가는 데이터량을 줄이는 데 연결됩니다.

모바일 GPU에 널리 쓰이는 TBDR(Tile-Based Deferred Rendering) 구조도 같은 맥락에서 이해할 수 있습니다. 화면을 작은 타일로 나누고, 타일 안의 중간 데이터를 온칩 메모리에서 처리하면 DRAM을 오가는 횟수를 줄일 수 있습니다.

TBDR의 구체적인 구조는 [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)에서 더 자세히 다룹니다.

---

## 마무리

이번 글에서는 CPU가 데이터를 가져오는 과정이 왜 성능에 영향을 주는지, 그리고 캐시가 어떤 접근 패턴에서 효과적으로 동작하는지 살펴보았습니다.

- CPU와 DRAM 사이의 속도 차이를 줄이기 위해 레지스터와 여러 단계의 캐시가 계층적으로 배치됩니다.
- 캐시는 값을 하나씩 가져오기보다 캐시 라인 단위로 주변 데이터를 함께 가져오며, 이 구조는 공간적 지역성을 활용합니다.
- 같은 데이터를 짧은 시간 안에 다시 쓰는 시간적 지역성도 캐시 히트율을 높이는 중요한 조건입니다.
- 캐시 미스는 처음 접근, 용량 부족, set 충돌처럼 서로 다른 이유로 발생하며, 데이터가 도착할 때까지 파이프라인을 기다리게 만들 수 있습니다.
- 순차 접근과 필요한 데이터만 모아 처리하는 배치는 캐시 라인과 프리페치를 더 잘 활용하게 해 줍니다.
- 지연은 데이터 하나를 기다리는 비용에 가깝고, 대역폭은 많은 데이터를 옮길 때의 전송 한계에 가깝습니다. 모바일에서는 CPU와 GPU가 메모리 대역폭을 공유하므로 이 제약이 더 중요해집니다.

결국 메모리 최적화는 데이터를 덜 읽는 것만이 아니라, CPU가 기다리지 않도록 읽는 순서와 배치를 정리하는 작업입니다. 배열을 순차적으로 접근하고, 함께 처리할 데이터를 가까이 두고, 사용하지 않는 데이터를 캐시 라인에 덜 섞는 이유가 여기에 있습니다.

<br>

CPU가 데이터를 효율적으로 가져와 게임 상태를 계산하더라도, 화면을 구성하는 픽셀은 GPU가 처리합니다. 다음 글에서는 이 그래픽 연산을 전담하기 위해 GPU가 어떤 구조로 발전했는지로 이어집니다.

[하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)에서는 CPU와 다른 방식으로 대량의 그래픽 연산을 처리하는 GPU의 배경과 구조를 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)
- [메모리 관리 (1)](/dev/unity/MemoryManagement-1/)

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
