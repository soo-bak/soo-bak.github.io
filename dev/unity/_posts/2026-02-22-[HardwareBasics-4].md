---
layout: single
title: "하드웨어 기초 (4) - 모바일 SoC - soo:bak"
date: "2026-02-22 01:11:00 +0900"
description: SoC 구조, 통합 메모리 아키텍처, LPDDR, ARM big.LITTLE, 전력 예산과 발열을 설명합니다.
tags:
  - Unity
  - 하드웨어
  - SoC
  - 모바일
  - ARM
---

## 데스크톱과 다른 모바일의 설계

[하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)에서는 그래픽 전용 하드웨어가 어떻게 발전했는지 다루었습니다. 데스크톱 환경에서는 CPU, GPU, 메모리, 냉각 장치가 비교적 여유 있는 공간과 전력 안에서 동작합니다.

모바일 기기에서는 같은 방식을 그대로 적용하기 어렵습니다. 배터리로 동작하고, 대부분 팬 없이 열을 처리하며, 손에 쥐는 크기 안에 디스플레이, 카메라, 통신 장치까지 함께 넣어야 하기 때문입니다. 그래서 모바일 하드웨어는 최고 성능만이 아니라, 제한된 전력과 열 안에서 여러 장치가 얼마나 오래 안정적으로 동작하는지를 기준으로 설계됩니다.

이 글에서는 모바일 기기의 중심에 있는 **SoC(System on Chip)**를 기준으로, 통합 메모리 구조, LPDDR 대역폭, 이종 CPU 코어 구성, 발열과 지속 성능이 Unity 게임 성능에 어떤 영향을 주는지 다룹니다.

---

## SoC란

SoC는 컴퓨터를 구성하는 여러 기능을 하나의 칩에 모은 형태입니다. 모바일 SoC에는 CPU와 GPU뿐 아니라 메모리 컨트롤러, 디스플레이 컨트롤러, 카메라 처리를 담당하는 ISP, 인공지능 연산을 위한 NPU, 통신 모뎀 등이 함께 들어갑니다.

데스크톱 PC에서는 이런 기능이 여러 부품으로 나뉘어 메인보드 위에 배치됩니다. 부품을 교체하거나 확장하기 쉽고, CPU와 GPU를 각각 냉각할 수 있다는 장점이 있습니다. 대신 부품 사이를 오가는 신호는 긴 배선과 접점을 지나야 하므로 전력과 지연 비용이 늘어납니다.

모바일에서는 내부 공간과 배터리 용량이 제한적입니다. 주요 기능을 한 칩에 모으면 부품 사이의 물리적 거리가 짧아지고, 데이터를 주고받는 데 드는 전력도 줄어듭니다. SoC가 모바일 기기에 적합한 이유는 이 통합이 공간과 전력 양쪽을 아끼기 때문입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 660 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; width: 100%; min-width: 430px;">
  <text x="160" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데스크톱 PC</text>
  <rect x="40" y="48" width="240" height="72" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="78" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">CPU · GPU · RAM · I/O</text>
  <text x="160" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">여러 부품이 보드 위에서 연결</text>
  <line x1="330" y1="32" x2="330" y2="166" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.25"/>
  <text x="500" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">모바일 SoC</text>
  <rect x="380" y="48" width="240" height="72" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="500" y="78" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">CPU · GPU · NPU · ISP · 모뎀</text>
  <text x="500" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">한 칩 안에서 짧게 연결</text>
  <text x="330" y="154" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">분리와 확장성 ↔ 공간과 전력 효율</text>
</svg>
</div>

<br>

통합 설계의 대가는 열과 전력을 함께 나눠 써야 한다는 점입니다. CPU와 GPU가 같은 칩 안에 있으므로 한쪽에서 발생한 열은 다른 쪽에도 영향을 줍니다. 게임처럼 CPU와 GPU가 동시에 바쁜 작업에서는 이 공유된 전력과 열 예산이 성능을 제한하는 주요 조건이 됩니다.

---

## 통합 메모리 아키텍처 (UMA)

SoC 안에 CPU와 GPU가 함께 들어가면 메모리 배치도 달라집니다. 데스크톱에서는 CPU가 쓰는 시스템 메모리와 GPU가 쓰는 전용 VRAM이 나뉘는 경우가 많습니다. CPU가 준비한 텍스처나 메시 데이터를 GPU가 사용하려면, 시스템 메모리에서 GPU 전용 메모리로 복사하는 과정이 필요합니다.

모바일 SoC는 보통 CPU와 GPU가 같은 물리 메모리를 공유합니다. 이 구조를 **통합 메모리 아키텍처(UMA, Unified Memory Architecture)**라고 합니다. 모바일에서 공유되는 메모리는 주로 **LPDDR(Low Power DDR)**이며, [하드웨어 기초 (2)](/dev/unity/HardwareBasics-2/)에서 다룬 DRAM 계층에 해당합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 660 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; width: 100%; min-width: 430px;">
  <text x="165" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데스크톱 — 분리 메모리</text>
  <rect x="35" y="52" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="85" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">CPU</text>
  <rect x="195" y="52" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="245" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">GPU</text>
  <rect x="35" y="120" width="100" height="34" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="85" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">시스템 RAM</text>
  <rect x="195" y="120" width="100" height="34" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="245" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">전용 VRAM</text>
  <line x1="85" y1="92" x2="85" y2="120" stroke="currentColor" stroke-width="1.2"/>
  <line x1="245" y1="92" x2="245" y2="120" stroke="currentColor" stroke-width="1.2"/>
  <line x1="125" y1="104" x2="205" y2="104" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="165" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">복사</text>
  <line x1="335" y1="32" x2="335" y2="166" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.25"/>
  <text x="500" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">모바일 SoC — 통합 메모리</text>
  <rect x="385" y="52" width="230" height="48" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="500" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">CPU · GPU · NPU · ISP</text>
  <line x1="500" y1="100" x2="500" y2="124" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="500,128 496,120 504,120" fill="currentColor"/>
  <rect x="430" y="128" width="140" height="34" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2"/>
  <text x="500" y="149" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">공유 LPDDR</text>
</svg>
</div>

UMA의 장점은 CPU와 GPU 사이의 큰 복사 단계를 줄일 수 있다는 점입니다. CPU가 준비한 데이터가 이미 GPU가 접근할 수 있는 메모리에 있으므로, 데스크톱처럼 별도의 GPU 전용 메모리로 옮기는 과정이 필요하지 않습니다.

다만 같은 메모리를 쓴다고 해서 비용이 모두 사라지는 것은 아닙니다. CPU와 GPU는 각각 캐시를 가지고 있으므로, 한쪽이 쓴 데이터를 다른 쪽이 읽기 전에 동기화가 필요할 수 있습니다. 또한 메모리 대역폭과 용량을 SoC 안의 여러 장치가 함께 나눠 써야 합니다.

게임이 큰 텍스처와 메시를 많이 사용하면 GPU만 영향을 받는 것이 아닙니다. OS와 다른 앱이 사용할 수 있는 메모리도 줄고, CPU가 게임 로직을 처리할 때 사용할 대역폭도 함께 줄어듭니다. 모바일에서 메모리 사용량과 대역폭을 함께 봐야 하는 이유입니다.

---

## LPDDR 메모리와 대역폭 제약

LPDDR은 모바일 기기에서 전력과 패키지 크기를 줄이기 위해 쓰는 DRAM입니다. 데스크톱 GPU가 사용하는 전용 그래픽 메모리처럼 높은 대역폭만을 목표로 하지 않고, 배터리 기기에서 오래 동작할 수 있도록 전력 효율을 우선합니다.

이 설계 방향 때문에 모바일 SoC의 메모리 대역폭은 신중하게 다뤄야 할 자원입니다. GPU가 텍스처와 렌더 타깃을 읽고 쓰는 동안, CPU, NPU, ISP 같은 다른 장치도 같은 LPDDR에 접근합니다. 전체 대역폭이 충분해 보여도, 여러 장치가 동시에 접근하면 한쪽의 메모리 사용량이 다른 쪽의 처리 시간을 흔들 수 있습니다.

<br>

| 메모리 | 주 용도 | 설계 우선순위 |
|:---|:---|:---|
| LPDDR | 모바일 SoC 공유 메모리 | 낮은 전력, 작은 패키지 |
| GDDR | 외장 GPU 전용 메모리 | 높은 대역폭 |
| HBM | 고성능 GPU·가속기 | 매우 넓은 인터페이스 |

<br>

LPDDR의 저전력 특성은 단순히 성능을 낮춘 결과가 아니라, 배터리 기기에 맞춘 선택입니다. 외부 메모리 접근은 칩 내부 캐시 접근보다 훨씬 많은 에너지를 쓰므로, 모바일에서는 메모리에 덜 접근하고, 접근하더라도 필요한 만큼만 읽고 쓰는 것이 중요합니다.

이 제약은 모바일 렌더링 방식에도 영향을 줍니다. 모바일 GPU는 외부 메모리 트래픽을 줄이기 위해 타일 단위로 화면을 처리하는 구조를 많이 사용합니다. 이 내용은 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 더 자세히 다룹니다.

Unity 프로젝트에서는 텍스처 크기, 압축 포맷, 밉맵, 렌더 타깃 개수, 오버드로우가 모두 LPDDR 대역폭 사용량에 연결됩니다. 모바일에서 “픽셀을 많이 그린다”는 말은 단순히 GPU 연산이 늘어난다는 뜻만이 아니라, 공유 메모리에 오가는 데이터도 함께 늘어난다는 뜻입니다.

---

## 이종 CPU 코어 구성

모바일 SoC는 CPU 코어도 하나의 성격으로만 구성하지 않습니다. 높은 순간 성능을 내는 코어와 낮은 전력으로 오래 동작하는 코어를 함께 두고, 운영체제가 작업의 성격에 따라 어느 코어에서 실행할지 결정합니다.

ARM 계열 SoC에서 자주 언급되는 **big.LITTLE**과 **DynamIQ**는 이런 이종 코어 구성을 설명하는 대표적인 용어입니다. 이 글에서는 특정 코어 이름이나 세대별 스펙보다, 모바일 CPU가 성능과 전력 효율이 다른 코어를 함께 사용한다는 점에 초점을 둡니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 620 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%; min-width: 420px;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">모바일 CPU 코어 구성</text>
  <rect x="65" y="55" width="210" height="64" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="170" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">고성능 코어</text>
  <text x="170" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">높은 처리량 · 높은 전력</text>
  <rect x="345" y="55" width="210" height="64" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.4"/>
  <text x="450" y="82" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">고효율 코어</text>
  <text x="450" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">낮은 전력 · 긴 지속 시간</text>
  <text x="310" y="156" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">운영체제 스케줄러가 부하와 온도에 따라 스레드를 배치</text>
</svg>
</div>

고성능 코어는 복잡한 실행 구조와 큰 캐시를 사용해 같은 시간에 더 많은 명령어를 처리합니다. Unity의 메인 스레드, 렌더 준비, 물리 계산처럼 프레임 시간에 직접 영향을 주는 작업은 이런 코어에서 실행될 때 유리합니다. 대신 전력 소모와 발열이 크기 때문에 오래 높은 부하를 유지하기 어렵습니다.

고효율 코어는 처리량은 낮지만 적은 전력으로 동작합니다. 오디오, 네트워크, OS 백그라운드 작업처럼 부하가 낮거나 간헐적으로 실행되는 작업에 적합합니다. 고성능 코어도 온도와 배터리 상태에 따라 클럭이 낮아지거나 스케줄링이 바뀔 수 있으므로, 처음 몇 분의 성능이 장시간 플레이 성능을 그대로 대표하지는 않습니다.

Unity 게임에서는 이 배치가 프레임 시간에 영향을 줍니다. 메인 스레드가 고효율 코어에서 실행되면 같은 작업도 더 오래 걸릴 수 있고, 스레드가 코어 사이를 이동하면 이전 코어의 캐시를 그대로 쓰기 어렵습니다. 잡 시스템처럼 여러 코어에 일을 나누는 경우에도, 가장 늦게 끝나는 작업이 전체 완료 시점을 결정하므로 코어 성능 차이를 고려해야 합니다.

---

## 전력 예산과 발열

모바일 SoC의 성능은 연산 유닛의 수만으로 결정되지 않습니다. 칩이 낼 수 있는 성능이 높아도, 배터리가 공급할 수 있는 전력과 기기가 배출할 수 있는 열에는 한계가 있습니다.

데스크톱은 큰 방열판과 팬을 사용할 수 있어, 칩에서 발생한 열을 비교적 빠르게 밖으로 내보낼 수 있습니다. 반면 모바일 기기는 대부분 수동 방열에 의존하기 때문에, 짧은 순간에는 높은 성능을 낼 수 있어도 열이 쌓이면 그 상태를 오래 유지하기 어렵습니다.

<br>

| 항목 | 데스크톱 | 모바일 SoC |
|:---|:---|:---|
| 전력 공급 | 콘센트 | 배터리 |
| 냉각 방식 | 팬 + 방열판 | 수동 방열 |
| CPU/GPU 배치 | 별도 칩인 경우가 많음 | 하나의 SoC에 통합 |
| 성능 특성 | 높은 전력 유지에 유리 | 피크와 지속 성능 차이가 큼 |

<br>

모바일 SoC의 전력 예산은 CPU, GPU, NPU, 모뎀, 메모리 컨트롤러가 함께 나눠 씁니다. 게임 실행 중 GPU가 많은 전력을 쓰면 CPU가 쓸 수 있는 여유가 줄고, 반대로 CPU 작업이 많으면 GPU가 높은 클럭을 오래 유지하기 어려울 수 있습니다.

짧은 벤치마크나 로딩 구간에서는 SoC가 높은 클럭으로 동작해 피크 성능을 보여 줄 수 있습니다. 하지만 열이 쌓이면 운영체제는 칩을 보호하기 위해 CPU와 GPU 클럭을 낮춥니다. 이 과정을 **서멀 스로틀링(Thermal Throttling)**이라고 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 480 225" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%; min-width: 360px;">
  <line x1="60" y1="180" x2="60" y2="32" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="60,28 56,36 64,36" fill="currentColor"/>
  <text x="60" y="20" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">전력</text>
  <line x1="60" y1="180" x2="436" y2="180" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="440,180 432,176 432,184" fill="currentColor"/>
  <text x="446" y="184" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">시간</text>
  <polyline points="75,58 185,58 285,122 420,122" fill="none" stroke="currentColor" stroke-width="2.4"/>
  <line x1="60" y1="58" x2="75" y2="58" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.4"/>
  <line x1="60" y1="122" x2="285" y2="122" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.3"/>
  <text x="130" y="50" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">피크 구간</text>
  <text x="360" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">지속 구간</text>
  <text x="95" y="196" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="currentColor" opacity="0.55">시작</text>
  <text x="235" y="196" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="currentColor" opacity="0.55">스로틀링</text>
  <text x="375" y="196" text-anchor="middle" font-family="sans-serif" font-size="9.5" fill="currentColor" opacity="0.55">안정화</text>
  <text x="240" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">시간이 지나면 유지 가능한 전력 수준으로 내려감</text>
</svg>
</div>

서멀 스로틀링은 기기와 OS에 따라 다르게 나타납니다. 어떤 기기는 먼저 GPU 클럭을 낮추고, 어떤 기기는 CPU의 고성능 코어를 제한하거나 스레드를 고효율 코어로 옮길 수 있습니다. 개발자가 확인해야 할 것은 내부 정책의 정확한 단계보다, 일정 시간 플레이했을 때 프레임 시간이 어떻게 변하는지입니다.

배터리 사용 시간도 같은 문제와 연결됩니다. 렌더링 부하가 높아 GPU가 높은 클럭을 오래 유지하면 SoC뿐 아니라 디스플레이, 메모리, 통신 장치까지 포함한 기기 전체 소비 전력이 커집니다. 소비 전력이 커질수록 발열은 빨라지고, 배터리 사용 시간은 짧아집니다.

따라서 모바일 게임은 피크 성능보다 **지속 성능**을 기준으로 품질을 잡는 편이 안정적입니다. 기기가 차가운 상태에서 잠깐 측정한 값만 기준으로 삼으면, 실제 플레이 중 온도가 오른 뒤 프레임 시간이 달라질 수 있습니다. 프로파일링도 일정 시간 실행한 뒤의 프레임 시간, 온도, 클럭 변화를 함께 보는 편이 실제 플레이 환경에 가깝습니다.

---

## SoC별 차이와 테스트 범위

지금까지 다룬 통합 설계, 공유 메모리, LPDDR 대역폭, 이종 CPU 코어, 전력 제약은 모바일 SoC 전반에 공통으로 나타나는 조건입니다. 하지만 실제 게임 성능은 SoC와 GPU 계열에 따라 달라질 수 있습니다.

테스트에서는 이런 차이가 어디에서 드러나는지 확인해야 합니다. 어떤 기기에서는 렌더 타깃 전환이 부담이 되고, 다른 기기에서는 셰이더 컴파일이나 드라이버 처리 비용이 더 크게 드러날 수 있습니다. 따라서 테스트 기기는 같은 계열의 최신 기기만 고르기보다, GPU 계열과 성능 등급이 나뉘도록 구성하는 편이 좋습니다.

<br>

| 테스트 축 | 확인할 내용 |
|:---|:---|
| GPU 계열 | 셰이더 컴파일, 오버드로우, 렌더 타깃 비용 |
| 성능 등급 | Low/Mid/High 프리셋의 실제 프레임 시간 |
| 메모리 구성 | 텍스처, 메시, 렌더 타깃 사용량 |
| 지속 성능 | 장시간 플레이 중 클럭, 발열, 프레임 시간 변화 |
| 드라이버/API | Vulkan, Metal, OpenGL ES 사용 시 차이 |

<br>

Android에서는 같은 OS라도 GPU와 드라이버 조합이 넓게 갈라집니다. 특정 기기에서 안정적이던 셰이더가 다른 GPU 계열에서는 컴파일 시간이 길거나 실행 비용이 커질 수 있습니다. iOS는 기기 조합이 상대적으로 좁지만, 해상도와 세대 차이에 따른 GPU 성능과 메모리 대역폭 차이는 여전히 확인해야 합니다.

출시 전 테스트 목록에는 고성능 기기와 보급형 기기, 서로 다른 GPU 계열, 발열이 빠르게 쌓이는 기기를 함께 포함하는 편이 좋습니다. 그래야 평균적인 성능뿐 아니라, 특정 계열이나 장시간 플레이에서 드러나는 문제도 확인할 수 있습니다.

---

## 마무리

모바일 SoC를 볼 때는 개별 부품의 성능보다, 여러 장치가 같은 전력, 열, 메모리 예산을 나눠 쓴다는 점이 중요합니다.

- SoC는 CPU, GPU, NPU, ISP, 모뎀, 메모리 컨트롤러를 한 칩에 모아 공간과 통신 전력을 줄입니다.
- UMA는 CPU와 GPU 사이의 큰 복사 단계를 줄이지만, 메모리 대역폭과 용량을 여러 장치가 함께 쓰게 만듭니다.
- LPDDR은 모바일에 맞춘 저전력 메모리이므로, 텍스처, 렌더 타깃, 오버드로우가 곧 대역폭 사용량으로 이어집니다.
- 이종 CPU 코어 구성은 전력 효율에 유리하지만, 스케줄링과 코어 이동이 프레임 시간에 영향을 줄 수 있습니다.
- 서멀 스로틀링 때문에 모바일 게임은 피크 성능보다 장시간 유지되는 프레임 시간을 기준으로 봐야 합니다.

모바일 게임 최적화는 공유 자원을 덜 쓰고, 지속 가능한 품질 기준을 잡는 데서 출발합니다. GPU 계열과 드라이버 차이도 있으므로, 테스트 기기는 성능 등급뿐 아니라 GPU 계열과 발열 특성이 다르게 구성하는 편이 좋습니다.

LPDDR의 대역폭 제약이 모바일 GPU 구조에 어떤 영향을 주는지는 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 이어서 다룹니다. 발열과 전력 예산에 맞춰 품질을 조정하는 방법은 [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)에서 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- **하드웨어 기초 (4) - 모바일 SoC** (이 글)
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
