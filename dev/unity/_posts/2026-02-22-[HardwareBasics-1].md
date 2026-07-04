---
layout: single
title: "하드웨어 기초 (1) - CPU 아키텍처와 파이프라인 - soo:bak"
date: "2026-02-22 01:02:00 +0900"
description: CPU 명령어 파이프라인, 분기 예측, ILP, 슈퍼스칼라, in-order vs out-of-order 실행을 설명합니다.
tags:
  - Unity
  - 하드웨어
  - CPU
  - 파이프라인
  - 모바일
---

## CPU 구조와 성능 병목

Unity에서 작성한 스크립트는 게임 로직으로 보이지만, 실행 시점에는 CPU가 처리하는 명령어의 흐름이 됩니다. 평소에는 이 내부 과정을 몰라도 게임을 만들 수 있습니다. 하지만 프레임 시간의 대부분이 CPU 쪽에서 발생한다면, 코드가 CPU에서 어떤 방식으로 처리되는지 알아야 병목의 원인을 좁힐 수 있습니다.

프로파일러에서 CPU-bound 상황이 보인다고 해서 곧바로 어느 코드가 문제인지 알 수 있는 것은 아닙니다. 같은 로직이 데스크톱에서는 빠르게 실행되는데 모바일에서는 느릴 수 있고, 비슷한 반복문이라도 데이터 배치나 분기 패턴에 따라 실행 시간이 달라질 수 있습니다. 장시간 실행 후 프레임 시간이 늘어나는 현상도 발열과 클럭 변화처럼 하드웨어 조건의 영향을 받습니다.

이 글에서는 CPU가 명령어를 처리하는 기본 구조와 파이프라인, 분기 예측, 명령어 병렬성, in-order와 out-of-order 실행을 살펴봅니다. 이런 구조를 이해하면 Unity 스크립트 최적화, 캐시 친화적인 데이터 배치, 모바일 기기에서의 성능 편차를 해석할 때 기준을 세우기 쉽습니다.

---

## CPU가 명령어를 실행하는 방식

게임 로직은 C# 코드로 작성하지만, 실행 단계에서는 CPU가 이해할 수 있는 **명령어(instruction)**의 흐름으로 바뀝니다. 캐릭터 이동, 적 AI 판단, 물리 시뮬레이션, UI 갱신 같은 작업도 결국 CPU가 명령어를 실행하고 그 결과를 메모리나 레지스터에 기록하는 과정으로 처리됩니다. GPU는 이렇게 준비된 데이터와 렌더링 명령을 바탕으로 화면을 그립니다.

CPU가 직접 실행하는 코드는 **기계어**입니다. 기계어는 CPU가 해석할 수 있는 이진수 형태의 명령어이며, 각 명령어는 보통 아주 작은 작업을 나타냅니다. 예를 들어 "레지스터 A의 값과 레지스터 B의 값을 더해서 레지스터 C에 저장하라" 같은 연산도 하나의 명령어가 될 수 있습니다.

여기서 **레지스터(register)**는 CPU 코어 내부에 있는 매우 작은 고속 저장 공간입니다. CPU는 연산에 필요한 값을 레지스터에 올려 두고, 연산 결과도 다시 레지스터에 기록합니다. 레지스터의 용량은 작지만 접근 속도가 매우 빠르기 때문에, CPU가 명령어를 실행할 때 가장 가까이에서 사용하는 저장 공간이라고 볼 수 있습니다.

CPU는 명령어를 한 번에 끝내지 않고, 몇 개의 작은 단계로 나누어 처리합니다. 먼저 메모리에서 다음 명령어를 가져오고, 그 명령어가 어떤 작업인지 해석합니다. 그런 다음 연산을 수행하고, 필요하면 메모리에서 데이터를 읽거나 씁니다. 마지막으로 연산 결과를 레지스터나 메모리에 기록합니다. 이 단계들을 나누어 보면, 뒤에서 다룰 **파이프라인(pipeline)** 구조를 이해하기 쉬워집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 125" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">명령어 하나의 실행 과정 (개략)</text>
  <rect x="10" y="42" width="108" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="64" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">명령어</text>
  <text x="64" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">가져오기</text>
  <line x1="118" y1="63" x2="132" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="136,63 128,59 128,67" fill="currentColor"/>
  <rect x="136" y="42" width="96" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="184" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">명령어 해석</text>
  <line x1="232" y1="63" x2="246" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="250,63 242,59 242,67" fill="currentColor"/>
  <rect x="250" y="42" width="88" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="294" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">연산 수행</text>
  <line x1="338" y1="63" x2="352" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="356,63 348,59 348,67" fill="currentColor"/>
  <rect x="356" y="42" width="116" height="42" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="414" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">데이터</text>
  <text x="414" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">읽기 / 쓰기</text>
  <line x1="472" y1="63" x2="486" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="490,63 482,59 482,67" fill="currentColor"/>
  <rect x="490" y="42" width="120" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="550" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">결과</text>
  <text x="550" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">기록</text>
  <text x="310" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">데이터 읽기 / 쓰기는 명령어 종류에 따라 수행</text>
</svg>
</div>

<br>

CPU는 명령어 하나가 모든 단계를 끝낼 때까지 기다린 뒤 다음 명령어를 시작하지 않습니다. 첫 번째 명령어가 해석 단계로 넘어가면, CPU는 그다음 명령어를 가져오는 작업을 함께 진행할 수 있습니다. 이런 식으로 여러 명령어의 처리 단계를 겹쳐 실행하는 구조를 **명령어 파이프라인(Instruction Pipeline)**이라고 합니다.

---

## 명령어 파이프라인

파이프라인은 명령어 실행 과정을 여러 단계로 나누고, 각 단계가 서로 다른 명령어를 동시에 처리하게 만드는 구조입니다. 실제 CPU의 파이프라인은 더 복잡하지만, 기본 원리는 다음 5단계 모델로 이해할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 120" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">5단계 파이프라인</text>
  <rect x="10" y="38" width="110" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Fetch</text>
  <text x="65" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">명령어 인출</text>
  <text x="65" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(IF)</text>
  <line x1="120" y1="67" x2="132" y2="67" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="136,67 128,63 128,71" fill="currentColor"/>
  <rect x="136" y="38" width="110" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="191" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Decode</text>
  <text x="191" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">명령어 해독</text>
  <text x="191" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(ID)</text>
  <line x1="246" y1="67" x2="258" y2="67" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="262,67 254,63 254,71" fill="currentColor"/>
  <rect x="262" y="38" width="110" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="317" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Execute</text>
  <text x="317" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">실행</text>
  <text x="317" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(EX)</text>
  <line x1="372" y1="67" x2="384" y2="67" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="388,67 380,63 380,71" fill="currentColor"/>
  <rect x="388" y="38" width="110" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="443" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Memory</text>
  <text x="443" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">메모리 접근</text>
  <text x="443" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(MEM)</text>
  <line x1="498" y1="67" x2="510" y2="67" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="514,67 506,63 506,71" fill="currentColor"/>
  <rect x="514" y="38" width="96" height="58" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="562" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Writeback</text>
  <text x="562" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">결과 기록</text>
  <text x="562" y="88" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(WB)</text>
</svg>
</div>

<br>

**Fetch(명령어 인출)** 단계에서는 다음에 실행할 명령어를 메모리에서 가져옵니다. CPU는 다음 명령어가 메모리의 어느 위치에 있는지 알아야 하므로, 그 주소를 **프로그램 카운터(PC)**라는 레지스터에 저장해 둡니다. 명령어 하나를 가져오면 프로그램 카운터는 보통 그다음 명령어의 주소로 갱신됩니다.

**Decode(명령어 해독)** 단계에서는 가져온 명령어가 어떤 작업을 요구하는지 해석합니다. 덧셈인지, 비교인지, 메모리에서 값을 읽는 명령인지 판별하고, 연산에 필요한 입력값이 어떤 레지스터에 들어 있는지도 확인합니다. 예를 들어 두 값을 더하는 명령어라면, 어떤 두 레지스터의 값을 읽어야 하는지 이 단계에서 정해집니다.

**Execute(실행)** 단계에서는 앞 단계에서 해석한 작업을 실제로 수행합니다. 덧셈, 뺄셈, 비교, 논리 연산은 **ALU(Arithmetic Logic Unit, 산술 논리 연산 장치)**가 처리합니다. 조건문이나 반복문처럼 실행 흐름을 바꾸는 명령어라면, 조건을 만족하는지 판단하는 작업도 이 단계에서 이루어질 수 있습니다.

**Memory(메모리 접근)** 단계에서는 명령어가 필요로 하는 메모리 읽기나 쓰기를 처리합니다. 메모리에서 값을 가져오는 명령어를 load, 메모리에 값을 저장하는 명령어를 store라고 부릅니다. 덧셈이나 비교처럼 메모리 접근이 필요 없는 명령어는 이 단계에서 별도의 메모리 작업을 하지 않습니다.

**Writeback(결과 기록)** 단계에서는 실행 결과를 이후 명령어가 사용할 수 있도록 레지스터에 기록합니다. 예를 들어 덧셈 결과가 다음 계산에 필요하다면, 그 결과를 정해진 레지스터에 저장해 둡니다. 반대로 메모리에 값을 쓰는 명령어처럼 이미 Memory 단계에서 목적을 끝낸 경우에는, 이 단계에서 새로 기록할 레지스터 결과가 없을 수 있습니다.

### 파이프라인 없이 순차 실행하는 경우

파이프라인이 왜 필요한지 보려면, 먼저 명령어를 겹쳐 처리하지 않는 경우를 기준으로 잡아야 합니다. 여기서는 설명을 단순하게 하기 위해, Fetch부터 Writeback까지 각 단계가 **1클럭(clock)**씩 걸린다고 가정하겠습니다. 클럭은 CPU 동작을 나누어 보는 기본 시간 단위입니다.

파이프라인이 없으면 하나의 명령어가 5단계를 모두 마친 뒤에야 다음 명령어를 시작합니다. 따라서 명령어 하나를 끝내는 데 5클럭이 걸리고, 명령어 5개를 순서대로 실행하면 총 25클럭이 필요합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 620 205" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%; min-width: 440px;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">순차 실행 (파이프라인 없음)</text>

  <text x="88" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="100" y1="40" x2="580" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="100" y1="36" x2="100" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="196" y1="36" x2="196" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="388" y1="36" x2="388" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="484" y1="36" x2="484" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="580" y1="36" x2="580" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="100" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">0</text>
  <text x="196" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">10</text>
  <text x="388" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">15</text>
  <text x="484" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">20</text>
  <text x="580" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">25</text>

  <text x="88" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="88" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>
  <text x="88" y="115" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 3</text>
  <text x="88" y="139" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 4</text>
  <text x="88" y="163" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 5</text>

  <rect x="100" y="52" width="96" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="196" y="76" width="96" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="292" y="100" width="96" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="388" y="124" width="96" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="484" y="148" width="96" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>

  <text x="148" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="244" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="340" y="113" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="436" y="137" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="532" y="161" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <text x="310" y="192" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">명령어가 서로 겹치지 않으므로 5개 명령어에 25클럭 필요</text>
</svg>
</div>

<br>

이 방식에서는 한 명령어가 끝날 때까지 다음 명령어가 시작되지 않습니다. 따라서 명령어 인출, 해독, 실행, 메모리 접근, 결과 기록을 담당하는 처리 단계들이 동시에 일하지 못하고 차례를 기다리게 됩니다.

예를 들어 첫 번째 명령어가 해독이나 실행 단계에 있는 동안에도, 다음 명령어의 인출은 아직 시작되지 않습니다. 파이프라인은 이 비어 있는 시간을 줄이기 위해 여러 명령어의 단계를 겹쳐 실행하는 구조입니다.

### 파이프라인으로 겹쳐 실행하는 경우

파이프라인 실행에서는 한 명령어가 모든 단계를 끝낼 때까지 기다리지 않습니다. 명령어 1이 Fetch를 마치고 Decode로 넘어가면, Fetch 단계는 곧바로 명령어 2를 가져올 수 있습니다.

다음 클럭에는 명령어 1이 Execute로 이동하고, 명령어 2는 Decode로 이동하며, Fetch 단계는 명령어 3을 가져옵니다. 이런 식으로 각 단계가 서로 다른 명령어를 맡으면, 여러 명령어가 동시에 진행되는 것처럼 처리됩니다.

각 명령어 자체는 여전히 5단계를 거치지만, 여러 명령어가 서로 다른 단계를 동시에 지나가므로 연속된 명령어 묶음을 더 짧은 시간 안에 끝낼 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 205" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 430px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">파이프라인 실행</text>

  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="460" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="36" x2="166" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="208" y1="36" x2="208" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="34" x2="250" y2="150" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="334" y1="36" x2="334" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="376" y1="36" x2="376" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="418" y1="36" x2="418" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="460" y1="36" x2="460" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="250" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="334" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="376" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>
  <text x="418" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">9</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>
  <text x="72" y="115" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 3</text>
  <text x="72" y="139" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 4</text>
  <text x="72" y="163" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 5</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="124" y="76" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="166" y="100" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="208" y="124" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <rect x="250" y="148" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>

  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="208" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="250" y="113" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="292" y="137" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <text x="334" y="161" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <text x="486" y="66" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">완료: 5</text>
  <text x="486" y="90" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">완료: 6</text>
  <text x="486" y="114" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">완료: 7</text>
  <text x="486" y="138" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">완료: 8</text>
  <text x="486" y="162" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">완료: 9</text>

  <text x="280" y="192" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">5개 명령어를 9클럭에 완료</text>
</svg>
</div>

<br>

같은 5개의 명령어를 실행해도 순차 실행에서는 25클럭이 필요하지만, 파이프라인 실행에서는 9클럭이면 됩니다. 각 명령어는 여전히 5단계를 거치지만, 두 번째 명령어부터는 앞 명령어가 끝나기 전에 실행을 시작하기 때문입니다.

처음 몇 클럭은 파이프라인을 채우는 구간입니다. 클럭 5가 되면 IF, ID, EX, MEM, WB 단계가 모두 서로 다른 명령어를 처리하고, 이후에는 매 클럭마다 WB 단계에서 명령어 하나가 완료됩니다.

명령어 수가 많아질수록 차이는 더 분명해집니다. 5단계 파이프라인 모델에서 N개의 명령어를 순차 실행하면 5N 클럭이 필요합니다. 반면 이상적인 파이프라인에서는 처음 파이프라인을 채우는 4클럭을 더해 N + 4클럭이면 됩니다. 예를 들어 명령어 1,000개를 실행하면 순차 실행은 5,000클럭, 파이프라인 실행은 1,004클럭이 필요합니다.

여기서 중요한 점은 명령어 하나가 거치는 시간이 줄어든 것은 아니라는 점입니다. 명령어 1은 여전히 IF부터 WB까지 5단계를 거쳐야 하므로, 시작부터 완료까지 걸리는 시간은 5클럭입니다. 이처럼 작업 하나가 시작해서 끝날 때까지 걸리는 시간을 **레이턴시(Latency)**라고 합니다.

파이프라인이 줄이는 것은 전체 명령어 묶음을 끝내는 시간입니다. 파이프라인이 가득 찬 뒤에는 매 클럭마다 명령어 하나가 완료되므로, 단위 시간당 완료되는 명령어 수가 늘어납니다. 이를 **스루풋(Throughput)**이라고 합니다. 즉, 파이프라인은 개별 명령어의 레이턴시보다 연속된 명령어의 스루풋을 높이는 구조입니다.

하지만 실제 코드에서는 모든 명령어가 독립적으로 이어지지 않습니다. 어떤 명령어는 앞 명령어가 계산한 값을 사용해야 하고, 어떤 명령어는 조건에 따라 다음에 실행할 위치를 바꿉니다. 이런 경우에는 다음 명령어를 예정대로 다음 단계로 넘길 수 없고, 파이프라인의 흐름이 끊길 수 있습니다.

---

## 파이프라인 해저드

**파이프라인 해저드(Pipeline Hazard)**는 명령어를 다음 파이프라인 단계로 바로 넘기기 어렵게 만드는 조건이나 상황을 말합니다. 해저드가 실제 실행 중에 드러나 파이프라인의 일부 단계가 멈추는 현상을 **스톨(stall)**이라고 합니다.

파이프라인이 멈추는 이유는 한 가지가 아닙니다. 앞 명령어의 결과를 기다려야 할 수도 있고, 다음 명령어의 위치를 아직 확정하지 못했을 수도 있으며, 같은 하드웨어 자원을 동시에 쓰려고 할 수도 있습니다. 이런 차이에 따라 해저드는 크게 세 가지로 나눌 수 있습니다.

### 데이터 해저드 (Data Hazard)

데이터 해저드는 뒤의 명령어가 앞의 명령어 결과를 필요로 할 때 발생합니다. 앞 명령어가 아직 결과를 레지스터에 기록하지 않았는데, 다음 명령어가 그 값을 읽으려고 하면 올바른 값이 준비될 때까지 기다려야 합니다.

다음 예시는 첫 번째 명령어의 결과를 바로 다음 명령어가 사용하는 경우입니다.

```text
ADD R1, R2, R3   // R1 = R2 + R3
SUB R4, R1, R5   // R4 = R1 - R5
```

두 번째 명령어는 `R1` 값을 읽은 뒤에야 뺄셈을 실행할 수 있습니다. 그런데 첫 번째 명령어의 결과가 `R1`에 기록되는 시점은 WB 단계입니다. 그 전에는 `R1`에 새 값이 아직 없으므로, 두 번째 명령어는 값을 읽는 단계에서 기다려야 합니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 185" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 420px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데이터 해저드와 스톨</text>
  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="418" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="36" x2="166" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="208" y1="36" x2="208" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="34" x2="250" y2="104" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="334" y1="36" x2="334" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="376" y1="36" x2="376" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="418" y1="36" x2="418" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="250" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="334" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="376" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <rect x="124" y="76" width="42" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="145" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="166" y="76" width="84" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,2" opacity="0.75"/>
  <text x="208" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">대기</text>
  <rect x="250" y="76" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="334" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID EX MEM WB</text>

  <text x="260" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3~4: R1 값이 아직 없어 명령어 2가 대기</text>
  <text x="260" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 5: 명령어 1의 WB 이후 R1 사용 가능</text>
  <text x="260" y="164" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">대기한 만큼 뒤 명령어의 완료 시점도 늦어짐</text>
</svg>
</div>

<br>

방금 예시에서 두 번째 명령어는 `R1` 값을 기다렸습니다. 그런데 첫 번째 명령어의 덧셈 결과는 WB 단계에서 레지스터에 기록되기 전에 이미 Execute 단계에서 만들어집니다. CPU는 이 중간 결과를 레지스터에 저장될 때까지 기다리지 않고, 바로 다음 명령어의 연산 입력으로 넘길 수 있습니다.

이 기법을 **데이터 포워딩(Data Forwarding)** 또는 **바이패스(Bypass)**라고 합니다. 레지스터 파일을 거치지 않고 필요한 값을 바로 전달하므로, 많은 데이터 해저드를 스톨 없이 처리할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 500 185" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%; min-width: 410px;">
  <text x="250" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데이터 포워딩</text>
  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="334" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="34" x2="166" y2="104" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="208" y1="34" x2="208" y2="104" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="250" y1="36" x2="250" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="334" y1="36" x2="334" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">4</text>
  <text x="250" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <rect x="124" y="76" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="208" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <path d="M 166 72 C 168 116, 208 116, 208 96" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="208,94 204,102 212,102" fill="currentColor"/>
  <text x="187" y="123" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">결과 전달</text>

  <text x="250" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">EX에서 만들어진 값을 다음 EX로 바로 전달</text>
  <text x="250" y="166" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">WB까지 기다리지 않아도 됨</text>
</svg>
</div>

<br>

데이터 포워딩은 앞 명령어의 결과가 이미 만들어져 있을 때 효과가 있습니다. 하지만 결과가 아직 나오지 않은 경우에는 전달할 값이 없습니다.

대표적인 예가 메모리에서 값을 읽는 load 명령어입니다. load 명령어는 먼저 Execute 단계에서 어느 메모리 주소를 읽을지 계산하고, 그다음 Memory 단계에서 실제 데이터를 가져옵니다. 즉, load의 결과는 Execute 단계가 아니라 Memory 단계가 지나야 준비됩니다.

문제는 바로 다음 명령어가 그 값을 곧바로 사용하려 할 때입니다. 다음 명령어가 연산을 시작하려는 시점에는 load의 Memory 단계가 아직 끝나지 않았을 수 있습니다. 이 경우에는 전달할 값이 준비되지 않았으므로, 파이프라인이 잠시 기다려야 합니다.

이처럼 load 결과가 준비되기 전에 다음 명령어가 그 값을 요구하면, 포워딩으로도 대기를 없앨 수 없습니다. 이런 형태의 데이터 해저드를 **로드-유즈 해저드(load-use hazard)**라고 합니다.

### 제어 해저드 (Control Hazard)

제어 해저드는 다음에 실행할 코드 위치가 조건에 따라 달라질 때 발생합니다. C#의 `if`, `for`, `while` 같은 흐름 제어문은 CPU 명령어로 바뀌면 조건에 따라 다른 위치로 이동하는 분기 명령어가 됩니다.

파이프라인이 끊기지 않으려면 Fetch 단계가 계속 다음 명령어를 가져와야 합니다. 그런데 분기 명령어를 만나면 다음에 가져올 위치가 두 가지로 갈릴 수 있습니다. 조건이 참이면 분기 대상 위치의 명령어를 가져와야 하고, 거짓이면 원래 순서대로 이어지는 명령어를 가져와야 합니다. 어느 명령어가 다음에 올지는 조건 계산이 끝나야 확정되며, 이 계산은 보통 분기 명령어가 Execute 단계에 도달한 뒤에 이루어집니다.

예를 들어 `BEQ R1, R2, label`은 `R1`과 `R2`가 같을 때 `label` 위치로 분기하는 명령어입니다. 두 값을 비교하기 전에는 분기를 수행할지, 원래 순서대로 계속 실행할지 확정할 수 없습니다. 따라서 CPU는 분기 결과가 나올 때까지 Fetch를 멈추거나, 한쪽 경로가 맞다고 가정하고 명령어를 가져온 뒤 가정이 틀리면 잘못 가져온 명령어를 폐기해야 합니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 420px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">제어 해저드</text>
  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="418" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="34" x2="166" y2="104" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="208" y1="36" x2="208" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="36" x2="250" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="334" y1="36" x2="334" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="376" y1="36" x2="376" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="418" y1="36" x2="418" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="250" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="334" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="376" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">분기 명령</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">다음 명령</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <rect x="124" y="76" width="84" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,2" opacity="0.75"/>
  <text x="166" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">대기</text>
  <rect x="208" y="76" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="292" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <text x="260" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3: 분기 조건이 확정됨</text>
  <text x="260" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">그전까지 다음 명령어 인출을 대기</text>
  <text x="260" y="164" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">대기한 만큼 다음 명령어 시작이 늦어짐</text>
</svg>
</div>

<br>

파이프라인이 대기하는 동안에는 어떤 단계에도 유효한 명령어가 들어가지 못하는 빈 구간이 생깁니다. 이런 빈 구간을 **파이프라인 버블(Pipeline Bubble)**이라고 합니다.

분기 명령어가 나올 때마다 결과를 기다리면 버블이 반복해서 생깁니다. 조건문이나 반복문이 많은 코드에서는 이런 대기가 누적되어 파이프라인의 처리량이 떨어질 수 있습니다.

CPU는 이 손실을 줄이기 위해 분기 결과를 기다리기보다, 어느 경로로 이어질지 미리 가정하고 다음 명령어를 가져옵니다. 이 동작을 **분기 예측(Branch Prediction)**이라고 합니다.

### 구조적 해저드 (Structural Hazard)

구조적 해저드는 파이프라인 단계들이 같은 하드웨어 자원을 동시에 필요로 할 때 발생합니다. 파이프라인은 여러 명령어를 겹쳐 실행하므로, 서로 다른 단계가 같은 클럭에 같은 장치를 사용하려는 상황이 생길 수 있습니다.

예를 들어 명령어를 가져오는 Fetch 단계와 데이터를 읽는 Memory 단계가 같은 메모리 포트에 접근해야 하는 구조라면, 두 단계가 같은 클럭에 동시에 진행되기 어렵습니다. 이 경우 둘 중 하나는 기다려야 합니다. 이런 자원 충돌이 구조적 해저드입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 170" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 420px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">구조적 해저드: 자원 충돌</text>
  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="250" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="36" x2="166" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="208" y1="34" x2="208" y2="96" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">4</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 A</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 B</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM</text>

  <rect x="208" y="76" width="42" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="229" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>

  <line x1="208" y1="70" x2="208" y2="76" stroke="currentColor" stroke-width="2"/>
  <polygon points="208,52 204,60 212,60" fill="currentColor"/>
  <polygon points="208,94 204,86 212,86" fill="currentColor"/>

  <rect x="305" y="50" width="150" height="48" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text x="380" y="70" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">공유 자원</text>
  <text x="380" y="87" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">예: 메모리 포트</text>

  <path d="M 250 61 C 275 61, 282 65, 305 65" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <path d="M 250 85 C 275 85, 282 83, 305 83" fill="none" stroke="currentColor" stroke-width="1.2"/>

  <text x="260" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">같은 클럭에 두 단계가 같은 자원을 요구</text>
  <text x="260" y="146" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">둘 중 하나는 대기해야 함</text>
</svg>
</div>

<br>

구조적 해저드는 주로 CPU 설계에서 줄입니다. 여러 파이프라인 단계가 같은 자원을 동시에 요구하지 않도록, CPU 내부의 접근 경로나 실행 장치를 분리해서 배치하는 방식입니다.

예를 들어 Fetch 단계는 명령어를 읽어야 하고, Memory 단계는 데이터를 읽거나 써야 합니다. 두 단계가 같은 저장 장치 포트에 의존하면 충돌이 생길 수 있습니다. 그래서 많은 CPU는 L1 캐시를 **명령어 캐시(I-Cache)**와 **데이터 캐시(D-Cache)**로 나눕니다. Fetch 단계는 I-Cache에서 명령어를 가져오고, Memory 단계는 D-Cache에서 데이터를 읽거나 쓰므로 두 접근이 같은 자원을 두고 경쟁할 가능성이 줄어듭니다.

메인 메모리까지 명령어와 데이터를 완전히 나누는 것은 아니지만, CPU 가까운 캐시 계층에서 두 경로를 분리하는 구조를 **수정된 하버드 아키텍처(Modified Harvard Architecture)**라고 부릅니다. 이 구조는 Fetch 단계와 Memory 단계가 동시에 진행될 때 생길 수 있는 자원 충돌을 줄이는 데 도움이 됩니다.

이처럼 구조적 해저드는 주로 CPU 내부 자원을 어떻게 배치하느냐와 관련된 문제입니다. 따라서 Unity나 C# 코드에서 직접 해결할 수 있는 영역은 제한적입니다.

반면 제어 해저드는 코드의 분기 패턴과 연결됩니다. 조건문이 어떤 순서로 배치되어 있는지, 참과 거짓이 얼마나 일정한 패턴으로 나타나는지에 따라 분기에서 생기는 대기 시간이 달라질 수 있습니다. 그래서 소프트웨어 관점에서는 제어 해저드와 이를 줄이기 위한 **분기 예측(Branch Prediction)**을 이해하는 것이 중요합니다.

> 실제 프로그램에서는 파이프라인 해저드뿐 아니라 캐시 미스도 큰 대기 시간을 만들 수 있습니다. 캐시의 동작 원리와 메모리 계층은 [하드웨어 기초 (2) - 캐시와 메모리 계층](/dev/unity/HardwareBasics-2/)에서 더 자세히 다룹니다.

---

## 분기 예측 (Branch Prediction)

`if`, `for`, `while`, `switch` 같은 제어 구조는 CPU 명령어 수준에서 분기 명령어로 바뀝니다. 일반적인 프로그램에는 이런 분기가 자주 등장하므로, 분기 결과가 나올 때마다 Fetch를 멈추면 파이프라인의 대기 시간이 계속 누적됩니다.

이때 어느 경로를 먼저 가져올지 판단하는 하드웨어가 **분기 예측기(Branch Predictor)**입니다. 분기 예측기는 이전 실행 기록이나 분기 패턴을 바탕으로 분기가 수행될지 예측하고, Fetch 단계는 그 예측에 따라 다음 명령어를 가져옵니다.

분기 결과가 아직 확정되지 않은 상태에서 예측한 경로의 명령어를 먼저 처리하는 방식을 **투기적 실행(Speculative Execution)**이라고 합니다. 예측이 맞으면 파이프라인은 멈추지 않고 계속 진행됩니다. 예측이 틀리면 잘못 가져온 명령어들을 폐기하고, 올바른 경로의 명령어를 다시 가져와야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">분기 예측의 동작</text>
  <rect x="120" y="36" width="240" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="54" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">분기 명령어</text>
  <text x="240" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">아직 결과가 확정되지 않음</text>
  <line x1="240" y1="74" x2="240" y2="92" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,96 236,88 244,88" fill="currentColor"/>
  <rect x="60" y="98" width="360" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="116" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">분기 예측기</text>
  <text x="240" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">이전 패턴을 보고 한쪽 경로를 선택</text>
  <line x1="240" y1="136" x2="240" y2="154" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,158 236,150 244,150" fill="currentColor"/>
  <rect x="100" y="160" width="280" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="180" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">예측한 경로의 명령어를 가져옴</text>
</svg>
</div>

### 예측 성공과 실패

분기 예측의 효과는 예측이 맞았을 때와 틀렸을 때가 크게 다릅니다. 예측이 맞으면 이미 가져온 명령어들을 그대로 사용할 수 있으므로, 파이프라인은 중간에 멈추지 않고 이어집니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 420px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">예측 성공</text>
  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="376" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="34" x2="166" y2="118" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="208" y1="36" x2="208" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="36" x2="250" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="334" y1="36" x2="334" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="376" y1="36" x2="376" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="250" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="334" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">분기 명령</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">예측 경로 1</text>
  <text x="72" y="115" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">예측 경로 2</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <rect x="124" y="76" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="208" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>
  <rect x="166" y="100" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="250" y="113" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <text x="400" y="65" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">분기 결과 확정</text>
  <text x="400" y="89" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">그대로 사용</text>
  <text x="400" y="113" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">그대로 사용</text>

  <text x="260" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">예측한 경로가 실제 결과와 일치</text>
  <text x="260" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이미 가져온 명령어를 버리지 않고 계속 진행</text>
</svg>
</div>

<br>

예측이 틀리면 이미 가져온 명령어들이 실제 실행 경로와 맞지 않게 됩니다. 이 명령어들은 계속 진행해도 의미가 없으므로 파이프라인에서 제거하고, 올바른 경로의 명령어를 다시 가져와야 합니다. 이 과정을 **파이프라인 플러시(Pipeline Flush)**라고 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 540 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%; min-width: 430px;">
  <text x="270" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">예측 실패</text>
  <text x="72" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <line x1="82" y1="40" x2="418" y2="40" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="82" y1="36" x2="82" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="124" y1="36" x2="124" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="166" y1="34" x2="166" y2="142" stroke="currentColor" stroke-width="1" opacity="0.18"/>
  <line x1="208" y1="36" x2="208" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="250" y1="36" x2="250" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="292" y1="36" x2="292" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="334" y1="36" x2="334" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="376" y1="36" x2="376" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <line x1="418" y1="36" x2="418" y2="44" stroke="currentColor" stroke-width="1" opacity="0.45"/>
  <text x="82" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="124" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="166" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">3</text>
  <text x="208" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="250" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="292" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="334" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="376" y="32" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>

  <text x="72" y="67" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">분기 명령</text>
  <text x="72" y="91" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">잘못된 경로 1</text>
  <text x="72" y="115" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">잘못된 경로 2</text>
  <text x="72" y="139" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">올바른 경로</text>

  <rect x="82" y="52" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <rect x="124" y="76" width="84" height="18" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <text x="166" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID</text>
  <line x1="124" y1="76" x2="208" y2="94" stroke="currentColor" stroke-width="1.3" opacity="0.8"/>
  <line x1="208" y1="76" x2="124" y2="94" stroke="currentColor" stroke-width="1.3" opacity="0.8"/>

  <rect x="166" y="100" width="42" height="18" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.7"/>
  <text x="187" y="113" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <line x1="166" y1="100" x2="208" y2="118" stroke="currentColor" stroke-width="1.3" opacity="0.8"/>
  <line x1="208" y1="100" x2="166" y2="118" stroke="currentColor" stroke-width="1.3" opacity="0.8"/>

  <rect x="208" y="124" width="168" height="18" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.7"/>
  <text x="292" y="137" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF ID EX MEM WB</text>

  <text x="440" y="65" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">분기 결과 확정</text>
  <text x="440" y="91" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">폐기</text>
  <text x="440" y="115" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">폐기</text>
  <text x="440" y="139" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">다시 인출</text>

  <text x="270" y="172" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">예측 경로가 실제 결과와 다르면 잘못 가져온 명령어를 폐기</text>
  <text x="270" y="194" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">올바른 경로를 다시 가져오며 그만큼 시간이 낭비됨</text>
</svg>
</div>

<br>

여기서는 이해를 돕기 위해 5단계 파이프라인으로 설명했지만, 실제 CPU의 파이프라인은 이보다 더 복잡합니다.

파이프라인이 깊을수록 분기 결과가 확정되기 전까지 더 많은 명령어가 예측 경로로 들어갈 수 있습니다. 예측이 맞으면 그만큼 작업을 미리 진행한 효과가 있지만, 예측이 틀리면 이미 들어간 명령어를 더 많이 버려야 합니다.

그래서 분기 예측 실패의 비용은 파이프라인 구조에 따라 달라집니다. 단순한 5단계 예시에서는 몇 클럭의 손실로 보이지만, 더 깊은 파이프라인에서는 잘못 예측한 경로를 비우고 올바른 경로로 다시 채우는 비용이 더 커질 수 있습니다.

### 분기 예측의 방식

분기 예측기가 맞히려는 것은 다음에 가져올 명령어의 위치입니다. 분기 명령어에는 보통 두 가지 가능성이 있습니다. 하나는 점프 대상 주소로 이동하는 경우이고, 이를 **taken**이라고 부릅니다. 다른 하나는 점프하지 않고 코드에 적힌 다음 명령어로 이어지는 경우이며, 이를 **not-taken**이라고 부릅니다.

가장 단순한 방식은 **정적 예측(Static Prediction)**입니다. 정적 예측은 이전에 같은 분기가 어떻게 실행되었는지 기록하지 않습니다. 대신 CPU가 미리 정해 둔 규칙에 따라 항상 한쪽을 선택합니다.

예를 들어 루프의 끝에서는 보통 다시 루프의 처음으로 돌아갑니다. 이런 분기는 점프 대상 주소로 이동하는 경우가 많으므로 taken으로 예측할 수 있습니다. 반대로 루프가 끝나는 마지막 순간에는 더 이상 처음으로 돌아가지 않으므로 not-taken이 됩니다. 정적 예측은 이런 실제 반복 횟수를 알지 못하고, 정해진 규칙만 적용합니다.

그래서 정적 예측은 단순하지만 한계가 있습니다. 같은 분기라도 입력 데이터나 실행 상황에 따라 taken과 not-taken이 달라질 수 있기 때문입니다.

그래서 현대 CPU는 **동적 예측(Dynamic Prediction)**을 함께 사용합니다. 동적 예측은 같은 분기가 이전 실행에서 taken이었는지 not-taken이었는지를 기록하고, 그 기록을 바탕으로 다음 결과를 예측합니다. 단순한 방식은 최근 결과를 몇 비트로 저장하는 정도에서 시작하고, 더 복잡한 방식은 여러 분기의 흐름을 함께 보며 패턴을 찾습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 430px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2비트 카운터의 상태 변화</text>

  <rect x="22" y="76" width="112" height="52" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.3"/>
  <text x="78" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">00</text>
  <text x="78" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">not-taken</text>
  <text x="78" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">강한 예측</text>

  <rect x="156" y="76" width="112" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.3"/>
  <text x="212" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">01</text>
  <text x="212" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">not-taken</text>
  <text x="212" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">약한 예측</text>

  <rect x="292" y="76" width="112" height="52" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.3"/>
  <text x="348" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">10</text>
  <text x="348" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">taken</text>
  <text x="348" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">약한 예측</text>

  <rect x="426" y="76" width="112" height="52" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.3"/>
  <text x="482" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">11</text>
  <text x="482" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">taken</text>
  <text x="482" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">강한 예측</text>

  <line x1="134" y1="93" x2="152" y2="93" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="156,93 148,89 148,97" fill="currentColor"/>
  <line x1="268" y1="93" x2="288" y2="93" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="292,93 284,89 284,97" fill="currentColor"/>
  <line x1="404" y1="93" x2="422" y2="93" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="426,93 418,89 418,97" fill="currentColor"/>
  <text x="280" y="62" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">실제 결과가 taken이면 오른쪽으로 이동</text>

  <line x1="426" y1="111" x2="408" y2="111" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="404,111 412,107 412,115" fill="currentColor"/>
  <line x1="292" y1="111" x2="272" y2="111" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="268,111 276,107 276,115" fill="currentColor"/>
  <line x1="156" y1="111" x2="138" y2="111" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="134,111 142,107 142,115" fill="currentColor"/>
  <text x="280" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">실제 결과가 not-taken이면 왼쪽으로 이동</text>

  <line x1="20" y1="168" x2="268" y2="168" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <line x1="292" y1="168" x2="540" y2="168" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <text x="145" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">00, 01은 not-taken으로 예측</text>
  <text x="415" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">10, 11은 taken으로 예측</text>
  <text x="280" y="216" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">한 번 반대 결과가 나와도 예측 방향이 바로 뒤집히지 않습니다.</text>
</svg>
</div>

<br>

실제 CPU의 분기 예측기는 이보다 훨씬 복잡합니다. 하나의 분기만 따로 보지 않고, 여러 분기의 과거 흐름과 반복 패턴을 함께 참고합니다.

그래서 루프처럼 규칙적인 분기는 높은 확률로 맞힐 수 있습니다. 반대로 입력 데이터에 따라 참과 거짓이 불규칙하게 바뀌는 분기는 과거 기록만으로 다음 결과를 예측하기 어렵습니다.

### 게임에서의 의미

게임 코드에서 분기 예측의 영향은 같은 조건문이 여러 번 반복해서 실행될 때 드러납니다.

예를 들어 많은 적 캐릭터를 순회하는 코드는 `isAlive`, `isVisible`, `isInRange` 같은 조건을 반복해서 검사합니다. 살아 있는 적과 죽은 적이 섞여 있거나, 화면 안팎의 오브젝트가 불규칙하게 섞여 있으면 조건의 참과 거짓도 불규칙하게 나타납니다.

이런 패턴은 분기 예측기가 다음 결과를 맞히기 어렵습니다. 반대로 같은 상태의 오브젝트가 어느 정도 모여 있거나, 대부분 같은 결과가 반복되는 조건문은 예측하기 쉽습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 420px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">반복되는 조건 결과와 섞인 조건 결과</text>

  <text x="40" y="54" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예측하기 쉬운 경우</text>
  <text x="40" y="76" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">같은 결과가 오래 반복됨</text>
  <rect x="190" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="216" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="242" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="268" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="294" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="320" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="346" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="372" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="398" y="42" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="424" y="42" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <text x="318" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">대부분 같은 방향이라 다음 결과를 맞히기 쉬움</text>

  <line x1="40" y1="110" x2="480" y2="110" stroke="currentColor" stroke-width="1" opacity="0.18"/>

  <text x="40" y="138" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예측하기 어려운 경우</text>
  <text x="40" y="160" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">참과 거짓이 불규칙하게 섞임</text>
  <rect x="190" y="126" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="216" y="126" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <rect x="242" y="126" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="268" y="126" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="294" y="126" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <rect x="320" y="126" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="346" y="126" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <rect x="372" y="126" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <rect x="398" y="126" width="22" height="22" fill="currentColor" fill-opacity="0.28"/>
  <rect x="424" y="126" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <text x="318" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">반복 패턴이 약해 다음 결과를 맞히기 어려움</text>

  <text x="260" y="204" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">진한 칸 = 조건이 참, 빈 칸 = 조건이 거짓</text>
</svg>
</div>

<br>

Unity에서 `Update()` 루프 안에 많은 조건 분기가 있더라도, 대부분의 코드에서 분기 예측을 직접 의식할 필요는 없습니다. 문제가 되는 것은 같은 조건문이 아주 많이 반복되고, 그 결과가 매번 불규칙하게 바뀌는 경우입니다.

예를 들어 수천 개의 오브젝트를 매 프레임 순회하면서 상태 검사를 수행하면, 예측 실패 비용이 반복해서 누적될 수 있습니다. 이때는 조건문 자체를 없애기보다, 먼저 데이터 배치와 처리 순서를 조정하는 편이 현실적입니다. 살아 있는 오브젝트와 비활성 오브젝트를 분리하거나, 같은 상태의 오브젝트를 묶어서 처리하면 조건 결과가 더 규칙적으로 나타납니다.

조건 분기 대신 수학 연산이나 비트 연산으로 처리하는 **브랜치리스 프로그래밍(Branchless Programming)**도 이런 문제를 줄이는 방법 중 하나입니다. 다만 코드를 읽기 어렵게 만들 수 있으므로, 모든 분기를 없애려는 방식으로 접근하기보다 프로파일러에서 반복 비용이 확인된 핫 루프에 제한적으로 적용하는 편이 좋습니다.

---

## ILP와 슈퍼스칼라 실행

파이프라인을 사용하면 여러 명령어가 동시에 진행되지만, 단순한 파이프라인에서는 한 시점에 각 단계가 명령어 하나씩만 처리합니다. 파이프라인이 가득 찬 뒤에도 한 클럭에 완료되는 명령어는 하나입니다.

**슈퍼스칼라(Superscalar)** 실행은 이 한계를 줄이기 위한 구조입니다. CPU가 한 클럭에 명령어를 하나만 보내는 것이 아니라, 여러 명령어를 동시에 발행하고 여러 실행 유닛에 나누어 보냅니다.

예를 들어 한 명령어는 덧셈 유닛에서 처리하고, 다른 명령어는 메모리 접근 유닛에서 처리할 수 있습니다. 두 명령어가 서로의 결과를 기다리지 않는다면, CPU는 두 작업을 같은 시점에 진행할 수 있습니다.

반대로 뒤의 명령어가 앞의 명령어 결과를 사용해야 한다면 함께 실행할 수 없습니다. 앞의 결과가 나와야 다음 명령어를 계산할 수 있기 때문입니다. 그래서 슈퍼스칼라 실행은 프로그램 안에 서로 독립적인 명령어가 많을수록 효과가 커집니다.

### ILP (Instruction Level Parallelism)

**ILP(Instruction-Level Parallelism, 명령어 수준 병렬성)**는 프로그램 안에 서로 독립적으로 실행할 수 있는 명령어가 얼마나 있는지를 나타내는 개념입니다.

앞 명령어의 결과를 기다리지 않아도 되는 명령어가 많으면 ILP가 높습니다. 반대로 각 명령어가 바로 앞 명령어의 결과에 계속 의존하면, CPU는 여러 실행 유닛을 가지고 있어도 기다리는 시간이 많아집니다.

따라서 ILP는 CPU가 임의로 만들어내는 성능이 아닙니다. CPU는 코드 안에 이미 존재하는 독립적인 명령어들을 찾아 동시에 실행할 뿐입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 430px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">독립적인 명령어와 의존적인 명령어</text>

  <rect x="36" y="56" width="180" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="126" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">명령어 A</text>
  <text x="126" y="92" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">위치 X 계산</text>

  <rect x="36" y="126" width="180" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="126" y="146" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">명령어 B</text>
  <text x="126" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">위치 Y 계산</text>

  <rect x="344" y="91" width="180" height="48" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
  <text x="434" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">명령어 C</text>
  <text x="434" y="127" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">A와 B 결과 사용</text>

  <path d="M 216 80 L 284 80 L 284 115" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M 216 150 L 284 150 L 284 115" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="284" y1="115" x2="340" y2="115" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="344,115 336,111 336,119" fill="currentColor"/>

  <text x="126" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">A와 B는 서로 기다리지 않음</text>
  <text x="434" y="174" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">C는 A와 B가 끝난 뒤 실행</text>
  <text x="280" y="222" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">독립적인 명령어가 많을수록 동시에 실행할 여지가 커짐</text>
</svg>
</div>

<br>

위 예시에서 A와 B는 서로의 결과를 사용하지 않습니다. CPU는 이런 명령어를 같은 시점에 실행할 수 있고, 그만큼 한 클럭 동안 더 많은 일을 처리할 수 있습니다.

반면 C는 A와 B의 결과가 모두 필요합니다. A나 B가 끝나기 전에는 C를 계산할 수 없으므로, C는 앞의 계산을 기다려야 합니다.

게임 코드에서도 같은 차이가 나타납니다. 위치의 X, Y, Z 값을 각각 독립적으로 계산하는 구간은 동시에 처리할 여지가 큽니다. 반대로 이전 계산 결과를 다음 계산의 입력으로 계속 넘기는 연쇄적인 코드는 CPU가 병렬로 처리하기 어렵습니다.

### 슈퍼스칼라 CPU

ILP가 충분한 코드에서는 CPU가 여러 명령어를 같은 시점에 진행할 수 있습니다. 슈퍼스칼라 CPU는 이때 한 번에 하나의 명령어만 파이프라인에 넣지 않고, 여러 명령어를 나란히 흘려보냅니다.

아래 그림은 한 클럭에 두 개의 명령어를 처리할 수 있는 단순화한 예시입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 500 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%; min-width: 430px;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2-way 슈퍼스칼라 파이프라인</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="96" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="128" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="160" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="192" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="224" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="256" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 A</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 B</text>
  <text x="75" y="109" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 C</text>
  <text x="75" y="131" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 D</text>
  <rect x="80" y="50" width="192" height="88" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="272" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="94" x2="272" y2="94" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="116" x2="272" y2="116" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="96" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="112" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="128" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="144" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="160" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="176" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="192" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="208" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="224" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="80" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="96" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="112" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="128" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="144" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="160" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="176" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="192" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="208" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="224" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="112" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="128" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="144" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="160" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="176" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="192" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="208" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="224" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="240" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="256" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="112" y="116" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="128" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="144" y="116" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="160" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="176" y="116" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="192" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="208" y="116" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="224" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="240" y="116" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="256" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="292" y="87" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">A와 B가 같은 클럭에 시작</text>
  <text x="292" y="131" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">C와 D가 같은 클럭에 시작</text>
  <text x="250" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">독립적인 명령어가 충분하면 두 줄로 파이프라인을 채울 수 있음</text>
  <text x="250" y="194" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이상적인 경우 한 클럭에 명령어 2개까지 완료</text>
</svg>
</div>

<br>

여기서 **2-way**는 한 클럭에 최대 두 개의 명령어를 동시에 진행할 수 있도록 설계된 폭을 뜻합니다. **4-way**라면 그 폭이 네 개까지 늘어납니다.

다만 이 숫자가 매 클럭의 실제 처리량을 의미하지는 않습니다. 2-way 구조라도 매번 두 개의 명령어가 함께 완료되는 것은 아닙니다.

명령어 사이에 의존성이 있으면 뒤의 명령어는 앞의 결과를 기다려야 합니다. 의존성이 없는 명령어라도 필요한 실행 유닛이 이미 사용 중이거나, 메모리 접근이 늦어지면 바로 진행되지 못합니다.

따라서 슈퍼스칼라 CPU의 실제 처리량은 코드와 하드웨어가 함께 결정합니다. 코드 안에 독립적으로 실행할 수 있는 명령어가 충분히 있어야 하고, CPU에도 그 명령어들을 동시에 처리할 실행 유닛과 대역폭이 있어야 합니다.

### 클럭 속도와 IPC의 관계

CPU 성능을 볼 때 클럭 속도만 비교하면 판단이 흔들릴 수 있습니다. 클럭 속도는 CPU가 1초에 몇 번의 사이클을 진행하는지를 나타내고, **IPC(Instructions Per Clock)**는 한 사이클 동안 평균적으로 몇 개의 명령어를 끝내는지를 나타냅니다.

단순화하면 같은 종류의 작업에서는 다음 관계로 생각할 수 있습니다.

$$\text{처리량} \;\approx\; \text{클럭 속도} \;\times\; \text{IPC}$$

예를 들어 클럭이 더 높은 CPU라도 한 사이클에 끝내는 일이 적으면 실제 처리량이 낮을 수 있습니다. 반대로 클럭이 조금 낮아도 IPC가 높으면 같은 시간 동안 더 많은 명령어를 처리할 수 있습니다.

IPC는 앞에서 다룬 구조들과 연결됩니다. 파이프라인이 자주 멈추지 않고, 분기 예측이 잘 맞고, 슈퍼스칼라 실행으로 독립적인 명령어를 함께 처리할 수 있을수록 IPC가 높아집니다. 반대로 데이터 의존성, 예측 실패, 캐시 미스가 많으면 클럭이 높아도 IPC가 떨어집니다.

그래서 최신 CPU의 성능 향상은 단순히 클럭을 올리는 문제만은 아닙니다. 클럭을 높이면 전력 소모와 발열도 함께 커지므로, 특히 모바일 기기에서는 높은 클럭을 오래 유지하기 어렵습니다. 같은 클럭에서 더 많은 일을 끝내는 구조, 즉 IPC를 높이는 설계가 중요한 이유입니다.

---

## in-order vs out-of-order 실행

파이프라인과 슈퍼스칼라 구조가 있어도, 명령어를 어떤 순서로 실행할지는 별도의 문제입니다.

CPU가 명령어를 프로그램에 적힌 순서대로 실행하는 방식을 **in-order 실행**이라고 합니다. 반대로 결과가 바뀌지 않는 범위에서 실행 순서를 조정하는 방식을 **out-of-order 실행**이라고 합니다.

차이는 앞쪽 명령어가 오래 걸릴 때 드러납니다. 첫 번째 명령어가 메모리에서 데이터를 읽느라 대기하는 동안, 그 뒤의 덧셈 명령어가 별개의 값만 사용하는 상황을 예로 들 수 있습니다. in-order 실행은 프로그램 순서를 지키기 때문에 덧셈 명령어도 앞 명령어를 기다립니다. out-of-order 실행은 덧셈처럼 먼저 처리해도 결과가 바뀌지 않는 명령어를 찾아, 기다리는 동안 실행할 수 있습니다.

### in-order 실행

in-order 실행은 명령어를 프로그램에 적힌 순서대로 처리합니다. 앞 명령어가 다음 단계로 넘어가지 못하면, 뒤 명령어도 순서상 함께 기다립니다.

아래 예시는 세 명령어가 차례로 들어온 흐름입니다.

```text
A: LOAD R1, [mem]    // 메모리에서 값을 읽어 R1에 저장
B: ADD  R3, R4, R5   // R4와 R5를 더해 R3에 저장
C: MUL  R6, R1, R7   // A가 읽어 온 R1 값을 사용
```

A는 메모리 접근 때문에 오래 걸릴 수 있습니다. B는 A의 결과를 사용하지 않지만, in-order 실행에서는 A보다 앞서 실행될 수 없습니다. C는 R1 값을 사용하므로 A가 끝난 뒤에야 실행할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 430px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">in-order 실행</text>
  <text x="78" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간</text>
  <line x1="90" y1="40" x2="445" y2="40" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <polygon points="452,40 442,35 442,45" fill="currentColor" opacity="0.65"/>

  <text x="78" y="70" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 A</text>
  <text x="78" y="104" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 B</text>
  <text x="78" y="138" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 C</text>

  <rect x="94" y="55" width="74" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="131" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">읽기 요청</text>
  <rect x="168" y="55" width="160" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="248" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">메모리 대기</text>
  <rect x="328" y="55" width="58" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="357" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">완료</text>

  <rect x="120" y="89" width="208" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="224" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">순서 때문에 대기</text>
  <rect x="328" y="89" width="58" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="357" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">실행</text>

  <rect x="146" y="123" width="182" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="237" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">A 결과 대기</text>
  <rect x="386" y="123" width="58" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="415" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">실행</text>

  <text x="260" y="178" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">B는 A의 결과를 쓰지 않지만, 순서를 지키느라 기다림</text>
  <text x="260" y="198" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">in-order 실행에서는 앞 명령어의 지연이 뒤 명령어로 전파될 수 있음</text>
</svg>
</div>

<br>

in-order 실행은 성능 면에서는 불리할 수 있지만, 제어 구조가 단순합니다. CPU가 명령어 순서를 크게 바꾸지 않으므로, 어떤 명령어를 먼저 실행할지 판단하고 추적하는 하드웨어가 상대적으로 적게 필요합니다.

이 단순함은 전력과 면적 측면에서 장점이 됩니다. 그래서 높은 성능보다 전력 효율과 작은 코어 면적이 중요한 CPU 코어에서는 in-order 구조가 여전히 사용됩니다.

### out-of-order 실행

out-of-order(OoO) 실행은 명령어 사이의 의존성을 확인한 뒤, 먼저 실행해도 결과가 바뀌지 않는 명령어를 앞당겨 처리합니다. 앞의 예시에서는 B가 A의 결과를 사용하지 않으므로, A가 메모리를 기다리는 동안 B를 먼저 실행할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%; min-width: 430px;">
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">out-of-order 실행</text>
  <text x="78" y="44" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간</text>
  <line x1="90" y1="40" x2="445" y2="40" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <polygon points="452,40 442,35 442,45" fill="currentColor" opacity="0.65"/>

  <text x="78" y="70" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 A</text>
  <text x="78" y="104" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 B</text>
  <text x="78" y="138" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 C</text>

  <rect x="94" y="55" width="74" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="131" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">읽기 요청</text>
  <rect x="168" y="55" width="160" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="248" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">메모리 대기</text>
  <rect x="328" y="55" width="58" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="357" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">완료</text>

  <rect x="132" y="89" width="72" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="168" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">먼저 실행</text>

  <rect x="146" y="123" width="182" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="237" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">A 결과 대기</text>
  <rect x="386" y="123" width="58" height="22" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="415" y="138" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">실행</text>

  <path d="M 208 100 C 250 102 286 92 326 72" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.7" stroke-dasharray="4,3"/>
  <text x="300" y="101" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">A를 기다리지 않음</text>

  <text x="260" y="178" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">B는 A의 결과를 쓰지 않으므로 먼저 실행 가능</text>
  <text x="260" y="198" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">out-of-order 실행은 대기 시간 동안 처리할 수 있는 일을 찾음</text>
</svg>
</div>

<br>

out-of-order 실행은 단순히 순서를 바꿔 실행하는 기능이 아닙니다. CPU는 어떤 명령어를 먼저 실행해도 되는지 판단하고, 먼저 끝난 결과를 임시로 보관한 뒤, 외부에서 보이는 결과는 원래 순서대로 확정해야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 560 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%; min-width: 440px;">
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">out-of-order 실행의 기본 흐름</text>

  <rect x="40" y="62" width="130" height="58" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="105" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">명령어 대기열</text>
  <text x="105" y="102" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.78">준비된 명령어 선택</text>

  <line x1="170" y1="91" x2="214" y2="91" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="218,91 210,87 210,95" fill="currentColor"/>

  <rect x="218" y="62" width="130" height="58" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
  <text x="283" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">실행 유닛</text>
  <text x="283" y="102" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.78">가능한 명령어 실행</text>

  <line x1="348" y1="91" x2="392" y2="91" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="396,91 388,87 388,95" fill="currentColor"/>

  <rect x="396" y="62" width="130" height="58" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="461" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">결과 보관</text>
  <text x="461" y="102" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.78">순서대로 확정</text>

  <rect x="78" y="156" width="110" height="34" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text x="133" y="177" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">예약 스테이션</text>
  <line x1="133" y1="156" x2="133" y2="124" stroke="currentColor" stroke-width="1" opacity="0.55" stroke-dasharray="4,3"/>

  <rect x="372" y="156" width="110" height="34" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text x="427" y="177" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">리오더 버퍼</text>
  <line x1="427" y1="156" x2="427" y2="124" stroke="currentColor" stroke-width="1" opacity="0.55" stroke-dasharray="4,3"/>

  <text x="280" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">실행 순서는 바뀔 수 있지만, 결과는 프로그램 순서대로 확정됩니다.</text>
</svg>
</div>

<br>

**리오더 버퍼(Reorder Buffer, ROB)**는 먼저 끝난 명령어의 결과를 바로 확정하지 않고 잠시 보관합니다. out-of-order 실행에서는 B가 A보다 먼저 끝날 수 있지만, 외부에서 보기에는 A, B, C가 프로그램 순서대로 완료된 것처럼 보여야 합니다. ROB는 앞선 명령어들이 문제없이 끝난 것을 확인한 뒤, 결과를 원래 순서대로 확정합니다. 이 과정을 **커밋(commit)**이라고 합니다.

**예약 스테이션(Reservation Station, RS)**은 아직 실행할 준비가 되지 않은 명령어를 보관합니다. 어떤 명령어가 필요한 입력값을 모두 갖추면, RS는 그 명령어를 실행 유닛으로 보냅니다. 앞의 예시에서 C는 A가 읽어 온 R1 값이 필요하므로, R1이 준비될 때까지 기다립니다.

<br>

이 구조를 구현하려면 CPU가 더 많은 정보를 관리해야 합니다. 어떤 명령어가 어떤 결과를 기다리는지, 어떤 명령어가 먼저 실행되어도 되는지, 먼저 끝난 결과를 언제 확정해도 되는지를 계속 추적해야 합니다. 그만큼 제어 회로가 복잡해지고 전력 소모도 늘어납니다.

그 비용을 감수하는 이유는 대기 시간을 줄일 수 있기 때문입니다. 메모리 접근처럼 오래 걸리는 명령어가 있어도, 그 결과와 관계없는 다른 명령어를 먼저 실행하면 파이프라인이 비어 있는 시간을 줄일 수 있습니다. 이 효과가 누적되면 같은 클럭에서도 더 높은 IPC를 얻을 수 있습니다.

### 모바일 CPU: big.LITTLE과 DynamIQ

모바일 기기는 배터리로 동작하고, 작은 본체 안에서 열을 처리해야 합니다. 모든 CPU 코어를 최고 성능 위주로 만들면 짧은 순간에는 빠를 수 있지만, 전력 소모와 발열 때문에 그 상태를 오래 유지하기 어렵습니다. 그래서 모바일 SoC(System on Chip)는 무거운 작업을 빠르게 처리하는 코어와 가벼운 작업을 낮은 전력으로 처리하는 코어를 함께 둡니다.

이런 구조에서는 높은 처리량이 필요한 작업에는 고성능 코어를 사용하고, 오래 지속되지만 가벼운 작업에는 고효율 코어를 사용해 전력 소모와 발열을 줄입니다. ARM 계열 모바일 SoC에서는 이와 관련된 구조를 설명할 때 **big.LITTLE**이나 **DynamIQ** 같은 용어가 함께 등장합니다.

<br>

**모바일 SoC의 코어 구성 예시**

| 구분 | 고성능 코어 | 고효율 코어 |
|:---|:---|:---|
| 설계 목표 | 짧은 시간에 많은 작업 처리 | 낮은 전력으로 꾸준히 작업 처리 |
| 일반적인 특징 | 높은 IPC, 큰 캐시, 적극적인 실행 구조 | 낮은 전력, 작은 면적, 단순한 실행 구조 |
| 적합한 작업 | 게임 로직, 카메라, 압축, 복잡한 연산 | 백그라운드 작업, 알림, 오디오, 가벼운 시스템 작업 |
| 한계 | 전력 소모와 발열이 큼 | 무거운 작업에서는 처리 시간이 길어짐 |

<br>

고성능 코어는 같은 시간에 더 많은 명령어를 처리하도록 설계됩니다. 큰 캐시와 적극적인 실행 구조를 사용하므로, 메인 스레드, 렌더링 준비, 물리 계산처럼 프레임 시간에 직접 영향을 주는 작업에 유리합니다. 대신 전력 소모와 발열이 크기 때문에 높은 부하를 오래 유지하기 어렵습니다.

고효율 코어는 처리량보다 전력 효율을 우선합니다. 백그라운드 작업, 오디오 재생, 센서 처리처럼 부하가 낮고 오래 지속되는 작업에 적합합니다. 같은 작업을 처리하는 데 더 오래 걸릴 수 있지만, 전력 소모와 발열을 줄이는 데 유리합니다.

고성능 코어와 고효율 코어의 차이는 특정 코어 이름이나 세부 스펙을 외우기 위한 구분이 아닙니다. 중요한 것은 각 코어가 서로 다른 목표로 설계된다는 점입니다. 어떤 코어는 짧은 시간에 많은 일을 처리하는 데 초점을 두고, 어떤 코어는 낮은 전력으로 오래 동작하는 데 초점을 둡니다.

어떤 스레드가 어느 코어에서 실행될지는 운영체제 스케줄러가 결정합니다. 스케줄러는 현재 부하, 배터리 상태, 온도, 스레드 우선순위 등을 보고 코어를 배정합니다. 따라서 게임이 실행 중이더라도 모든 작업이 항상 고성능 코어에서만 실행된다고 볼 수는 없습니다.

### 모바일에서 지속 성능이 중요한 이유

모바일 게임은 짧은 순간의 최대 성능보다 오래 유지되는 성능이 더 중요합니다. 게임을 오래 실행하면 SoC 온도가 올라가고, 기기는 발열을 줄이기 위해 CPU와 GPU 클럭을 낮출 수 있습니다.

클럭이 낮아지면 같은 코드도 더 오래 걸립니다. 여기에 스케줄러가 일부 작업을 고효율 코어로 옮기면, 작업이 끝나는 시점도 달라질 수 있습니다. 메인 스레드, 렌더링 준비, 물리 계산처럼 프레임 완료를 막는 작업에서 이런 변화가 생기면 프레임 시간이 흔들립니다.

따라서 모바일 최적화에서는 장시간 플레이 중 프레임 시간이 어떻게 변하는지 확인해야 합니다. 짧은 벤치마크에서는 안정적으로 보이던 게임도, 온도가 오른 뒤에는 CPU 클럭과 코어 배치가 달라져 다른 결과를 보일 수 있습니다.

<br>

**모바일 게임 관점의 코어 차이**

| 구분 | 고효율 코어 | 고성능 코어 |
|:---|:---|:---|
| 강점 | 낮은 전력으로 오래 실행 | 짧은 시간에 많은 작업 처리 |
| 주로 맡기 좋은 작업 | 백그라운드, 오디오, 가벼운 보조 작업 | 메인 스레드, 렌더링 준비, 물리 계산 |
| 성능상 주의점 | 무거운 작업이 올라가면 프레임을 늦출 수 있음 | 부하가 오래 이어지면 발열로 클럭이 낮아질 수 있음 |

<br>

모바일 CPU의 코어 구성은 단순히 빠른 코어와 느린 코어를 나누는 문제가 아닙니다. 제한된 전력과 열 예산 안에서 순간 성능과 지속 성능을 함께 맞추기 위한 설계입니다. Unity에서 모바일 성능을 점검할 때도 특정 코어 이름보다, 장시간 플레이 중 CPU 시간과 프레임 시간이 안정적으로 유지되는지를 확인하는 것이 더 중요합니다.

---

## 마무리

이번 글에서는 CPU가 명령어를 더 끊기지 않고 처리하기 위해 사용하는 구조들을 살펴보았습니다.

- 파이프라인은 여러 명령어의 실행 단계를 겹쳐 CPU가 쉬는 시간을 줄입니다.
- 데이터 의존성, 분기, 자원 충돌은 파이프라인을 멈추게 만들 수 있으며, 분기 예측과 포워딩 같은 기법은 이 대기 시간을 줄이기 위해 사용됩니다.
- 슈퍼스칼라 실행은 서로 독립적인 명령어를 여러 실행 유닛에 나누어 처리해 IPC를 높입니다.
- in-order 실행은 단순하고 전력 효율에 유리하며, out-of-order 실행은 더 복잡한 하드웨어로 독립적인 명령어를 앞당겨 실행합니다.
- 모바일 SoC는 성격이 다른 코어를 함께 사용하므로, 모바일 게임에서는 순간 최대 성능보다 장시간 유지되는 프레임 시간이 더 중요합니다.

이번 글에서 다룬 구조들은 모두 같은 방향을 향합니다. CPU가 다음 명령어를 기다리거나, 필요한 값을 기다리거나, 실행 유닛을 비워 두는 시간을 줄이는 것입니다. 성능 최적화에서 CPU 바운드를 해석할 때도 결국 이 대기 시간이 어디에서 생기는지를 보는 것이 출발점입니다.

다만 CPU가 명령어를 빠르게 처리할 준비가 되어 있어도, 명령어가 사용할 데이터가 늦게 도착하면 다시 대기가 발생합니다. 이 지점부터는 CPU 내부의 실행 구조만으로 설명하기 어렵고, 메모리 계층과 캐시를 함께 봐야 합니다.

[하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)에서는 CPU와 메모리의 속도 차이, 캐시가 필요한 이유, 그리고 데이터 접근 패턴이 게임 성능에 미치는 영향을 다룹니다.

<br>

---

**시리즈**
- **하드웨어 기초 (1) - CPU 아키텍처와 파이프라인** (현재 글)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)

**전체 시리즈**
- **하드웨어 기초 (1) - CPU 아키텍처와 파이프라인** (현재 글)
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
