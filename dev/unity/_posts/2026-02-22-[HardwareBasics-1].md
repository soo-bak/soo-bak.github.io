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

## CPU를 알아야 성능이 보인다

Unity로 게임을 개발할 때, 코드 한 줄이 실행되는 과정은 겉으로 드러나지 않습니다. `Update()`에 작성한 이동 로직이 어떤 하드웨어 위에서 어떻게 처리되는지를 알지 못해도 게임은 동작합니다. 하지만 성능 문제가 발생하면 상황이 달라집니다.

프로파일러에서 CPU 바운드 경고가 나왔을 때, 원인을 파악하려면 CPU가 명령어를 어떤 구조로 처리하는지를 알아야 합니다. 같은 코드가 데스크톱에서는 빠르게 실행되는데 모바일에서 느린 이유, 정렬된 배열과 정렬되지 않은 배열을 순회할 때 성능이 달라지는 이유, 게임을 10분 이상 실행하면 프레임이 떨어지는 이유 -- 이 현상들의 답은 모두 CPU 아키텍처에 있습니다.

<br>

이 글에서는 CPU가 명령어를 처리하는 내부 구조를 살펴보고, 그 구조에서 성능 병목이 발생하는 원리와 이를 극복하기 위해 CPU가 사용하는 기법들을 다룹니다. Unity 스크립트 최적화, 캐시 친화적 데이터 배치, 모바일 기기에서의 성능 편차를 이해하기 위한 기초가 되는 내용입니다.

---

## CPU가 명령어를 실행하는 방식

게임이 실행되는 동안 화면에 보이는 모든 것은, CPU가 프로그램의 **명령어(instruction)**를 하나씩 읽어 실행하는 과정에서 출발합니다.

캐릭터의 이동, 적 AI의 판단, 물리 시뮬레이션, UI 갱신은 CPU가 명령어를 처리한 결과이고, 그 결과를 바탕으로 GPU가 화면을 그립니다.

CPU는 프로그램 코드를 **기계어**(CPU가 직접 해석할 수 있는 이진수 형태의 명령어) 나열로 받아들이고, 기본적으로 이 명령어들을 프로그램에 적힌 순서대로 처리합니다.

<br>

명령어 하나의 예를 들면, "레지스터 A의 값과 레지스터 B의 값을 더해서 레지스터 C에 저장하라"와 같은 단순한 연산입니다.

**레지스터(register)**는 CPU 코어 내부에 있는 소량의 초고속 저장 공간으로, 연산에 필요한 데이터를 임시로 보관합니다. 용량은 수백 바이트에서 수 킬로바이트에 불과하지만, CPU가 데이터에 접근하는 데 1 나노초도 걸리지 않을 만큼 빠릅니다.

CPU가 수행하는 모든 작업은 이런 단순한 명령어들의 조합으로 이루어져 있습니다.

<br>

CPU 내부에서 명령어 하나가 완료되기까지는 여러 단계를 거칩니다. 메모리에서 명령어를 가져오고, 그 명령어가 무엇을 의미하는지 해석하고, 실제 연산을 수행합니다. 이후에는 명령어의 종류에 따라 메모리에서 데이터를 읽거나 쓰고, 결과를 레지스터에 기록합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 125" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">명령어 하나의 실행 과정 (개략)</text>
  <rect x="10" y="42" width="110" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="65" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">메모리에서</text>
  <text x="65" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">명령어 인출</text>
  <line x1="120" y1="63" x2="134" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="138,63 130,59 130,67" fill="currentColor"/>
  <rect x="138" y="42" width="80" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="178" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">명령어 해석</text>
  <line x1="218" y1="63" x2="232" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="236,63 228,59 228,67" fill="currentColor"/>
  <rect x="236" y="42" width="76" height="42" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="274" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">연산 수행</text>
  <line x1="312" y1="63" x2="326" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="330,63 322,59 322,67" fill="currentColor"/>
  <rect x="330" y="42" width="142" height="42" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="401" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">메모리 데이터</text>
  <text x="401" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">읽기 / 쓰기</text>
  <line x1="472" y1="63" x2="486" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="490,63 482,59 482,67" fill="currentColor"/>
  <rect x="490" y="42" width="120" height="42" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="550" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">결과를</text>
  <text x="550" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">레지스터에 기록</text>
  <text x="310" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">점선 단계는 명령어 종류에 따라 선택적으로 수행</text>
</svg>
</div>

<br>

이 단계들을 체계적으로 분리하고, 각 단계를 전담하는 하드웨어가 동시에 작동하도록 만든 구조가 **명령어 파이프라인(Instruction Pipeline)**입니다.

첫 번째 명령어를 메모리에서 가져온 뒤 해석 단계로 넘기면, 가져오기를 담당하는 하드웨어는 할 일이 없어집니다. 이 하드웨어가 쉬지 않고 곧바로 두 번째 명령어를 가져오면, 두 하드웨어가 서로 다른 명령어를 동시에 처리하게 됩니다. 이런 식으로 5개 단계의 하드웨어가 모두 각기 다른 명령어를 처리하고 있으면, 매 클럭마다 명령어 하나가 완료됩니다.

---

## 명령어 파이프라인

앞 섹션에서 명령어 하나가 거치는 다섯 단계를 개략적으로 살펴보았습니다. 이 단계들을 각각 전담 하드웨어 유닛으로 분리한 것이 명령어 파이프라인이며, 가장 기본적인 형태는 다음 5단계로 구성됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 100" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">5단계 파이프라인</text>
  <rect x="14" y="40" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="64" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Fetch</text>
  <text x="64" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(IF)</text>
  <line x1="114" y1="63" x2="128" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="132,63 124,59 124,67" fill="currentColor"/>
  <rect x="132" y="40" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="182" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Decode</text>
  <text x="182" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(ID)</text>
  <line x1="232" y1="63" x2="246" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="250,63 242,59 242,67" fill="currentColor"/>
  <rect x="250" y="40" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Execute</text>
  <text x="300" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(EX)</text>
  <line x1="350" y1="63" x2="364" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="368,63 360,59 360,67" fill="currentColor"/>
  <rect x="368" y="40" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="418" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Memory</text>
  <text x="418" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(MEM)</text>
  <line x1="468" y1="63" x2="482" y2="63" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="486,63 478,59 478,67" fill="currentColor"/>
  <rect x="486" y="40" width="100" height="46" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="536" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Writeback</text>
  <text x="536" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(WB)</text>
</svg>
</div>

<br>

**Fetch(명령어 인출)**: **프로그램 카운터(PC)**가 가리키는 메모리 주소에서 다음 명령어를 가져옵니다. 프로그램 카운터는 "다음에 실행할 명령어의 주소"를 저장하는 레지스터로, 명령어를 가져온 뒤 자동으로 다음 주소를 가리키도록 증가합니다.

**Decode(명령어 해독)**: 가져온 명령어가 어떤 연산인지 해석합니다. 덧셈인지, 곱셈인지, 메모리 접근인지 판별하고, 연산에 사용할 소스 레지스터의 값을 읽어옵니다.

**Execute(실행)**: **ALU(Arithmetic Logic Unit, 산술 논리 연산 장치)**에서 실제 연산을 수행합니다. 덧셈, 뺄셈, 비교, 논리 연산 등이 이 단계에서 이루어집니다.

**Memory(메모리 접근)**: 메모리에서 데이터를 읽거나(load), 메모리에 데이터를 쓰는(store) 명령어일 경우 이 단계에서 메모리 접근이 수행됩니다. 연산만 하는 명령어는 이 단계를 통과합니다.

**Writeback(결과 기록)**: 연산 결과를 목적지 레지스터에 저장합니다. 레지스터에 기록할 결과가 없는 명령어는 이 단계를 통과합니다. 예를 들어 store 명령어는 메모리에 데이터를 쓰는 것이 목적이므로 기록할 결과가 없습니다.

### 파이프라인 없이 순차 실행하는 경우

각 단계가 실행에 얼마나 걸리는지를 따져 보려면, 시간 단위가 필요합니다. **클럭(clock)**은 CPU가 동작하는 기본 시간 단위입니다.

CPU 내부에는 일정한 간격으로 전기 신호를 보내는 클럭 발생기가 있고, 이 신호의 한 주기가 1클럭입니다. 3.0 GHz CPU라면 1초에 30억 번의 클럭 신호가 발생하므로, 1클럭은 약 0.33 나노초(10억분의 1초)입니다.

<br>

파이프라인이 없으면, 하나의 명령어가 5단계를 모두 마쳐야 다음 명령어가 시작됩니다. 각 단계가 1클럭씩 걸린다고 가정하면, 명령어 하나에 5클럭, 명령어 5개를 실행하면 총 25클럭이 걸립니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%; min-width: 380px;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">순차 실행 (파이프라인 없음)</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="67" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="123" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="193" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">10</text>
  <text x="263" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">15</text>
  <text x="333" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">20</text>
  <text x="403" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">25</text>
  <text x="55" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="55" y="85" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>
  <text x="55" y="105" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 3</text>
  <text x="55" y="125" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 4</text>
  <text x="55" y="145" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 5</text>
  <rect x="60" y="50" width="350" height="100" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="60" y1="70" x2="410" y2="70" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="60" y1="90" x2="410" y2="90" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="60" y1="110" x2="410" y2="110" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="60" y1="130" x2="410" y2="130" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="130" y1="50" x2="130" y2="150" stroke="currentColor" stroke-width="0.5" opacity="0.25"/>
  <line x1="200" y1="50" x2="200" y2="150" stroke="currentColor" stroke-width="0.5" opacity="0.25"/>
  <line x1="270" y1="50" x2="270" y2="150" stroke="currentColor" stroke-width="0.5" opacity="0.25"/>
  <line x1="340" y1="50" x2="340" y2="150" stroke="currentColor" stroke-width="0.5" opacity="0.25"/>
  <rect x="60" y="50" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="67" y="64" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">IF</text>
  <rect x="74" y="50" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="81" y="64" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">ID</text>
  <rect x="88" y="50" width="14" height="20" fill="currentColor" fill-opacity="0.22"/><text x="95" y="64" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">EX</text>
  <rect x="102" y="50" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="109" y="64" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">MEM</text>
  <rect x="116" y="50" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="123" y="64" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">WB</text>
  <rect x="130" y="70" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="137" y="84" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">IF</text>
  <rect x="144" y="70" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="151" y="84" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">ID</text>
  <rect x="158" y="70" width="14" height="20" fill="currentColor" fill-opacity="0.22"/><text x="165" y="84" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">EX</text>
  <rect x="172" y="70" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="179" y="84" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">MEM</text>
  <rect x="186" y="70" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="193" y="84" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">WB</text>
  <rect x="200" y="90" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="207" y="104" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">IF</text>
  <rect x="214" y="90" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="221" y="104" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">ID</text>
  <rect x="228" y="90" width="14" height="20" fill="currentColor" fill-opacity="0.22"/><text x="235" y="104" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">EX</text>
  <rect x="242" y="90" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="249" y="104" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">MEM</text>
  <rect x="256" y="90" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="263" y="104" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">WB</text>
  <rect x="270" y="110" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="277" y="124" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">IF</text>
  <rect x="284" y="110" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="291" y="124" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">ID</text>
  <rect x="298" y="110" width="14" height="20" fill="currentColor" fill-opacity="0.22"/><text x="305" y="124" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">EX</text>
  <rect x="312" y="110" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="319" y="124" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">MEM</text>
  <rect x="326" y="110" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="333" y="124" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">WB</text>
  <rect x="340" y="130" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="347" y="144" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">IF</text>
  <rect x="354" y="130" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="361" y="144" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">ID</text>
  <rect x="368" y="130" width="14" height="20" fill="currentColor" fill-opacity="0.22"/><text x="375" y="144" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">EX</text>
  <rect x="382" y="130" width="14" height="20" fill="currentColor" fill-opacity="0.14"/><text x="389" y="144" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor">MEM</text>
  <rect x="396" y="130" width="14" height="20" fill="currentColor" fill-opacity="0.10"/><text x="403" y="144" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">WB</text>
  <text x="240" y="180" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">5개 명령어 × 5클럭 = 25클럭 소요</text>
</svg>
</div>

<br>

다이어그램을 보면, 명령어 하나가 5단계를 거치는 동안 각 유닛은 자기 차례인 1클럭만 작동하고 나머지 4클럭은 아무 일도 하지 않습니다.

Fetch 유닛은 클럭 1에서 명령어를 가져온 뒤 다음 명령어가 시작되는 클럭 6까지 유휴 상태이고, Execute 유닛도 클럭 3에서만 작동합니다. 5개 유닛 모두 활용률이 20%에 불과합니다.

### 파이프라인으로 겹쳐 실행하는 경우

앞 섹션에서 유닛 활용률이 20%에 불과한 이유를 확인했습니다.

활용률을 높이려면 각 유닛이 쉬는 시간에 다음 명령어를 처리하면 됩니다.

명령어 1이 Decode 단계로 넘어간 순간 Fetch 유닛은 비어 있으므로, 곧바로 명령어 2를 가져올 수 있습니다.

이렇게 각 단계가 끝난 즉시 다음 명령어를 받아 여러 명령어의 실행을 겹치는 방식이 파이프라인 실행입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">파이프라인 실행</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="205" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">5</text>
  <text x="233" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="261" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="289" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>
  <text x="317" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">9</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="75" y="85" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>
  <text x="75" y="105" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 3</text>
  <text x="75" y="125" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 4</text>
  <text x="75" y="145" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 5</text>
  <rect x="80" y="50" width="252" height="100" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="70" x2="332" y2="70" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="90" x2="332" y2="90" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="110" x2="332" y2="110" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="130" x2="332" y2="130" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="192" y="50" width="28" height="100" fill="currentColor" fill-opacity="0.05"/>
  <rect x="80" y="50" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="94" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="122" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="20" fill="currentColor" fill-opacity="0.22"/><text x="150" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="178" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="192" y="50" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="206" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="108" y="70" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="122" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="136" y="70" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="150" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="164" y="70" width="28" height="20" fill="currentColor" fill-opacity="0.22"/><text x="178" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="192" y="70" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="206" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="220" y="70" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="234" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="136" y="90" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="150" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="164" y="90" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="178" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="192" y="90" width="28" height="20" fill="currentColor" fill-opacity="0.22"/><text x="206" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="220" y="90" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="234" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="248" y="90" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="262" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="164" y="110" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="178" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="192" y="110" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="206" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="220" y="110" width="28" height="20" fill="currentColor" fill-opacity="0.22"/><text x="234" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="248" y="110" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="262" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="276" y="110" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="290" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="192" y="130" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="206" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="220" y="130" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="234" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="248" y="130" width="28" height="20" fill="currentColor" fill-opacity="0.22"/><text x="262" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="276" y="130" width="28" height="20" fill="currentColor" fill-opacity="0.14"/><text x="290" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="304" y="130" width="28" height="20" fill="currentColor" fill-opacity="0.10"/><text x="318" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="230" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">5개 명령어를 9클럭에 완료</text>
  <text x="230" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">클럭 5: 5개 유닛이 모두 사용 중 → 파이프라인이 가득 참</text>
  <text x="230" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">클럭 5 이후: 매 클럭마다 명령어 하나가 완료됨</text>
</svg>
</div>

<br>

같은 5개의 명령어가 순차 실행에서는 25클럭이 걸렸지만, 파이프라인에서는 9클럭에 완료됩니다.

다이어그램의 클럭 5를 보면 IF부터 WB까지 5개 유닛이 모두 서로 다른 명령어를 처리하고 있습니다. 이 상태가 **파이프라인이 가득 찬** 상태이며, 이후로는 매 클럭마다 WB 단계에서 명령어 하나가 완료됩니다.

<br>

명령어 수가 늘어나면 속도 비는 더 커집니다.

N개의 명령어를 실행할 때 순차 실행은 5N 클럭이 필요하고, 파이프라인은 처음 채우는 데 걸리는 4클럭을 더한 (N + 4) 클럭이면 충분합니다.

명령어 1,000개를 실행하면 순차 실행은 5,000클럭, 파이프라인은 1,004클럭이므로 속도 비는 약 4.98배입니다. N이 커질수록 이 비율은 파이프라인 단계 수인 5에 수렴합니다.

<br>

이 성능 향상을 두 가지 관점에서 정리할 수 있습니다.

<br>

**레이턴시(Latency)**는 명령어 하나가 IF에 진입한 시점부터 WB를 마칠 때까지 걸리는 시간입니다.

다이어그램에서 명령어 1은 클럭 1에 시작해 클럭 5에 완료되므로, 레이턴시는 순차 실행과 동일한 5클럭입니다. 파이프라인은 개별 명령어의 레이턴시를 줄이지 않습니다.

<br>

**스루풋(Throughput)**은 단위 시간당 완료되는 명령어의 수입니다.

순차 실행에서는 5클럭마다 명령어 하나가 완료되지만, 파이프라인이 가득 찬 뒤에는 매 클럭마다 하나가 완료됩니다. 스루풋이 5배로 증가한 것입니다.

파이프라인은 레이턴시가 아니라 스루풋을 높이는 구조입니다.

<br>

다만, 파이프라인이 항상 이 이상적인 스루풋을 유지하지는 않습니다.

명령어들 사이의 의존성이나 분기 명령어 때문에 다음 단계가 진행되지 못하고 파이프라인이 멈추는 상황이 발생하며, 이를 **파이프라인 해저드(Pipeline Hazard)**라고 합니다.

---

## 파이프라인 해저드

파이프라인 해저드가 발생하면 파이프라인이 **스톨(stall)**됩니다. 스톨은 파이프라인의 특정 단계가 진행하지 못하고 멈추면서, 그 뒤의 단계들도 연쇄적으로 대기하는 현상입니다.

파이프라인 해저드는 원인에 따라 세 가지 유형으로 나뉩니다.

### 데이터 해저드 (Data Hazard)

이전 명령어가 아직 결과를 레지스터에 기록하지 않았는데, 다음 명령어가 그 레지스터의 값을 읽으려 할 때 발생합니다.

<br>

예를 들어 명령어 1이 `ADD R1, R2, R3` (R2 + R3 → R1)이고 뒤따르는 명령어 2가 `SUB R4, R1, R5` (R1 - R5 → R4)인 경우를 봅시다. 명령어 2는 ID 단계에서 R1 값을 읽지만, 명령어 1이 R1에 값을 기록하는 것은 WB 단계인 클럭 5이므로, 그 전까지 명령어 2의 ID는 진행할 수 없습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데이터 해저드의 스톨</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="205" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">5</text>
  <text x="233" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="261" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="289" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>
  <rect x="80" y="50" width="224" height="44" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="304" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="94" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="122" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="178" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="192" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="206" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="108" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="122" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="136" y="72" width="28" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.7"/><text x="150" y="87" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">stall</text>
  <rect x="164" y="72" width="28" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.7"/><text x="178" y="87" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">stall</text>
  <rect x="192" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="206" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="220" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="234" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="248" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="262" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="276" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="290" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="230" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3~4: 명령어 2 스톨 — R1 값이 아직 없으므로 ID 진행 불가</text>
  <text x="230" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 5: 명령어 1의 WB 완료 → R1 사용 가능 → 명령어 2의 ID 진행</text>
  <text x="230" y="160" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2클럭 스톨로 명령어 2의 완료가 2클럭 지연</text>
</svg>
</div>

<br>

데이터 해저드를 완화하는 대표적인 기법이 **데이터 포워딩(Data Forwarding)** 또는 **바이패스(Bypass)**입니다.

명령어 1의 Execute 단계에서 연산 결과가 나오는 즉시, 그 값을 Writeback까지 기다리지 않고 명령어 2의 Execute 단계 입력으로 직접 전달합니다. 이렇게 하면 스톨 없이 연속 실행이 가능합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <text x="210" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">데이터 포워딩</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">4</text>
  <text x="205" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="233" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 2</text>
  <rect x="80" y="50" width="168" height="44" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="248" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="94" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="122" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.28"/><text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="178" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="192" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="206" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="108" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="122" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="136" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="150" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="164" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.28"/><text x="178" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="192" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="206" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="220" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="234" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <path d="M 150 72 Q 150 102 178 102 Q 178 102 178 78" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="178,72 174,80 182,80" fill="currentColor"/>
  <text x="164" y="115" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85" font-style="italic">forward</text>
  <text x="210" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3: 명령어 1의 EX에서 R1 값 산출</text>
  <text x="210" y="166" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 4: 산출된 값을 명령어 2의 EX 입력으로 직접 전달 (WB 미경유)</text>
  <text x="210" y="190" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스톨 없이 연속 실행</text>
</svg>
</div>

<br>

데이터 포워딩으로 많은 데이터 해저드를 해결할 수 있지만, 포워딩으로도 해결할 수 없는 경우가 있습니다.

메모리 읽기(load) 명령어는 Execute 단계가 아니라 그다음인 Memory 단계에서 데이터를 가져옵니다. 바로 다음 명령어가 이 데이터를 Execute 단계 입력으로 필요로 하면, Memory 단계가 아직 완료되지 않은 시점이므로 포워딩할 값 자체가 존재하지 않습니다.

이 경우 최소 1클럭의 스톨이 불가피하며, 이를 **로드-유즈 해저드(load-use hazard)**라고 합니다.

### 제어 해저드 (Control Hazard)

분기 명령어(if, for, while 등에서 생성되는 조건 점프)는 조건에 따라 다음에 실행할 명령어의 주소가 달라집니다.

어디로 점프할지는 Execute 단계에서 결정되므로, 분기 명령어가 Execute에 도달하기 전까지 Fetch 유닛은 다음에 가져올 명령어를 알 수 없습니다.

<br>

예를 들어 `BEQ R1, R2, label`(R1 == R2이면 label로 점프) 같은 분기 명령은 점프 대상이 EX 단계인 클럭 3에서 확정됩니다. 정상 파이프라인이라면 다음 명령의 IF가 클럭 2에서 시작되겠지만, 분기의 경우 그 시점까지 어디로 갈지 알 수 없어 IF가 진행될 수 없습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">제어 해저드의 버블</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="205" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="233" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="261" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="289" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">분기 명령</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">다음 명령</text>
  <rect x="80" y="50" width="224" height="44" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="304" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="94" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="122" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.28"/><text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="178" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="192" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="206" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="108" y="72" width="28" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.7"/><text x="122" y="87" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">버블</text>
  <rect x="136" y="72" width="28" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.7"/><text x="150" y="87" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">버블</text>
  <rect x="164" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="178" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="192" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="206" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="220" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.28"/><text x="234" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="248" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="262" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="276" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="290" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="230" y="120" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 2~3: 버블 — 점프 대상 미확정으로 IF 진행 불가</text>
  <text x="230" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3 끝: EX 완료로 점프 대상 확정 → 클럭 4에서 다음 명령의 IF 시작</text>
  <text x="230" y="160" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정상이면 클럭 2에서 시작할 IF가 클럭 4로 밀림 (2클럭 스톨)</text>
</svg>
</div>

<br>

스톨되는 동안 파이프라인에 빈 슬롯이 생기며, 이를 **파이프라인 버블(Pipeline Bubble)**이라고 합니다.

제어 해저드는 분기 명령어가 실행될 때마다 발생할 수 있으므로, 분기 빈도가 높을수록 버블이 누적되어 파이프라인 효율이 떨어집니다.

이 손실을 줄이기 위해 CPU는 **분기 예측(Branch Prediction)** 장치를 사용합니다.

### 구조적 해저드 (Structural Hazard)

두 개 이상의 파이프라인 단계가 같은 하드웨어 자원에 동시에 접근하면 충돌이 발생합니다. 예를 들어 명령어 1의 Memory 단계(데이터 읽기)와 명령어 4의 Fetch 단계(명령어 인출)가 같은 클럭에 겹치면, 두 단계 모두 메모리에 접근해야 하므로 같은 메모리 포트에서 충돌합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 170" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">구조적 해저드: 메모리 포트 충돌</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">4</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 1</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 4</text>
  <rect x="80" y="50" width="112" height="44" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="192" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="94" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="122" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.32"/><text x="178" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="164" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.32"/><text x="178" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <text x="200" y="65" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">메모리 데이터 읽기</text>
  <text x="200" y="87" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.85">메모리 명령어 인출</text>
  <line x1="178" y1="74" x2="178" y2="86" stroke="currentColor" stroke-width="2"/>
  <polygon points="178,72 174,80 182,80" fill="currentColor"/>
  <polygon points="178,94 174,86 182,86" fill="currentColor"/>
  <text x="230" y="118" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">클럭 4: 같은 메모리 포트를 동시 사용 → 충돌</text>
  <text x="230" y="138" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">명령어 1의 MEM(데이터 읽기)와 명령어 4의 IF(명령어 인출)가 동시에 메모리 접근</text>
</svg>
</div>

<br>

이 문제는 하드웨어 설계 단계에서 자원을 분리하여 해결합니다.

현대 CPU는 코어 바로 옆에 소용량 고속 메모리인 **캐시(cache)**를 둡니다. 캐시는 자주 사용하는 데이터의 복사본을 CPU 가까이에 유지하여, DRAM까지 가지 않고도 빠르게 접근할 수 있게 하는 메모리입니다. 캐시의 동작 원리와 계층 구조는 [다음 글](/dev/unity/HardwareBasics-2/)에서 자세히 다루며, 여기서는 구조적 해저드 해결과 관련된 부분만 다룹니다.

<br>

캐시의 첫 번째 계층인 L1 캐시는 **명령어 캐시(I-Cache)**와 **데이터 캐시(D-Cache)**로 분리되어 있습니다. Fetch 단계는 I-Cache에서 명령어를 가져오고, Memory 단계는 D-Cache에서 데이터를 읽거나 쓰므로, 두 접근이 물리적으로 별개의 메모리에서 이루어져 충돌하지 않습니다.

<br>

이 방식을 **수정된 하버드 아키텍처(Modified Harvard Architecture)**라고 합니다.

원래 하버드 아키텍처는 명령어 메모리와 데이터 메모리를 완전히 분리한 구조입니다. 현대 CPU는 메인 메모리(DRAM)는 하나로 통합하되, L1 캐시 수준에서만 명령어와 데이터를 분리하므로 "수정된" 하버드 아키텍처로 불립니다. 이름은 이 개념이 처음 적용된 것으로 알려진 하버드 마크 I 컴퓨터에서 유래합니다.

<br>

ALU를 여러 개 배치하여 Execute 단계에서의 충돌을 줄이는 것도 구조적 해저드의 해결 방법입니다.

구조적 해저드는 대부분 칩 설계 단계에서 해결되므로, 소프트웨어 개발자가 직접 대응해야 하는 경우는 드뭅니다.

<br>

세 가지 해저드 중 소프트웨어 개발자가 코드 수준에서 가장 직접적으로 영향을 줄 수 있는 것은 **제어 해저드**입니다.

제어 해저드는 프로그램의 분기 패턴에 따라 런타임에 반복적으로 발생하며, 코드의 분기 구조를 바꾸면 예측 성공률에 직접 영향을 줄 수 있기 때문입니다.

데이터 해저드는 포워딩과 컴파일러의 명령어 스케줄링으로 대부분 해소되고, 구조적 해저드는 하드웨어 설계로 해결됩니다.

<br>

다만 실전에서는 해저드 외에도 **캐시 미스로 인한 메모리 지연**이 파이프라인 스톨의 주요 원인입니다. 캐시에 없는 데이터는 메인 메모리(DRAM)에서 가져와야 하고, 이 접근에는 수백 클럭이 소요되므로 파이프라인이 긴 스톨에 빠집니다.

---

## 분기 예측 (Branch Prediction)

프로그램에서 분기 명령어가 차지하는 비율은 전체 명령어의 약 15~25%입니다. `if`, `for`, `while`, `switch` 같은 제어 구조가 모두 분기 명령어로 변환되기 때문입니다. 4~7개의 명령어마다 분기가 하나씩 나타나는 빈도이므로, 분기마다 파이프라인이 스톨되면 성능 손실이 누적됩니다.

<br>

분기 예측은 이 문제를 해결하기 위한 하드웨어 장치입니다.

분기 명령어의 결과가 확정되기 전에, **분기 예측기(Branch Predictor)**가 결과를 미리 추측하고, 그 추측에 따라 Fetch 유닛이 다음 명령어를 가져옵니다.

이렇게 확정되지 않은 결과에 기반하여 미리 실행하는 것을 **투기적 실행(Speculative Execution)**이라 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">분기 예측의 동작</text>
  <rect x="120" y="36" width="240" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="54" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">분기 명령어</text>
  <text x="240" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(아직 결과 모름)</text>
  <line x1="240" y1="74" x2="240" y2="92" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,96 236,88 244,88" fill="currentColor"/>
  <rect x="60" y="98" width="360" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="116" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">분기 예측기</text>
  <text x="240" y="130" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">"이 분기는 taken 될 가능성이 높다"</text>
  <line x1="240" y1="136" x2="240" y2="154" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="240,158 236,150 244,150" fill="currentColor"/>
  <rect x="100" y="160" width="280" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="180" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">예측에 따라 다음 명령어를 미리 Fetch</text>
</svg>
</div>

### 예측 성공과 실패

예측이 맞으면 파이프라인은 스톨 없이 계속 진행됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">예측 성공</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="205" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="233" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="261" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="289" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">분기 명령</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">다음 명령</text>
  <text x="75" y="109" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">그 다음</text>
  <rect x="80" y="50" width="224" height="66" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="304" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="94" x2="304" y2="94" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="94" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="122" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.28"/><text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="178" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="192" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="206" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="108" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="122" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="136" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="150" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="164" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="178" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="192" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="206" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="220" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="234" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="136" y="94" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="150" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="164" y="94" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="178" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="192" y="94" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="206" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="220" y="94" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="234" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="248" y="94" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="262" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="240" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 1: 예측기가 "taken"으로 예측 → 예측 경로 명령어를 클럭 2에서 Fetch</text>
  <text x="240" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3: EX에서 분기 결과 확정 — 예측이 맞았으므로 파이프라인 그대로 진행</text>
  <text x="240" y="184" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스톨 없음, 파이프라인이 끊기지 않음</text>
</svg>
</div>

<br>

예측이 틀리면, 잘못된 경로에서 이미 파이프라인에 진입한 명령어들의 처리 결과를 모두 무효화하고 올바른 경로에서 Fetch를 다시 시작해야 합니다. 이 과정을 **파이프라인 플러시(Pipeline Flush)**라고 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <text x="250" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">예측 실패 (Misprediction)</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="93" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="121" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="149" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">3</text>
  <text x="177" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="205" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5</text>
  <text x="233" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">6</text>
  <text x="261" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">7</text>
  <text x="289" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">8</text>
  <text x="317" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">9</text>
  <text x="345" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">10</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">분기 명령</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">잘못된 A</text>
  <text x="75" y="109" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">잘못된 B</text>
  <text x="75" y="131" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">올바른 X</text>
  <text x="75" y="153" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">올바른 Y</text>
  <rect x="80" y="50" width="280" height="110" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="360" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="94" x2="360" y2="94" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="116" x2="360" y2="116" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="138" x2="360" y2="138" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <rect x="80" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="94" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="108" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="122" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="136" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.28"/><text x="150" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="164" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="178" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="192" y="50" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="206" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="108" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="122" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="136" y="72" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="150" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <line x1="108" y1="72" x2="164" y2="94" stroke="currentColor" stroke-width="1.4" opacity="0.85"/>
  <line x1="164" y1="72" x2="108" y2="94" stroke="currentColor" stroke-width="1.4" opacity="0.85"/>
  <text x="240" y="87" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">폐기 (flush)</text>
  <rect x="136" y="94" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="150" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <line x1="136" y1="94" x2="164" y2="116" stroke="currentColor" stroke-width="1.4" opacity="0.85"/>
  <line x1="164" y1="94" x2="136" y2="116" stroke="currentColor" stroke-width="1.4" opacity="0.85"/>
  <text x="240" y="109" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">폐기 (flush)</text>
  <rect x="164" y="116" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="178" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="192" y="116" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="206" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="220" y="116" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="234" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="248" y="116" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="262" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="276" y="116" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="290" y="131" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="192" y="138" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="206" y="153" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="220" y="138" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="234" y="153" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="248" y="138" width="28" height="22" fill="currentColor" fill-opacity="0.22"/><text x="262" y="153" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="276" y="138" width="28" height="22" fill="currentColor" fill-opacity="0.14"/><text x="290" y="153" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="304" y="138" width="28" height="22" fill="currentColor" fill-opacity="0.10"/><text x="318" y="153" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="250" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 1: 잘못된 경로로 예측 → 잘못된 A, B를 클럭 2~3에서 Fetch</text>
  <text x="250" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 3: EX에서 예측 오류 확인 → 잘못된 A, B 폐기 (파이프라인 플러시)</text>
  <text x="250" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">클럭 4: 올바른 경로에서 Fetch 재시작</text>
  <text x="250" y="246" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정상이면 클럭 2에서 시작할 IF가 클럭 4로 밀림 (2클럭 낭비)</text>
</svg>
</div>

<br>

현대 CPU의 파이프라인은 5단계보다 깁니다.

데스크톱 CPU의 파이프라인은 14~20단계에 이르고, 일부 아키텍처는 그 이상입니다.

파이프라인이 길면 Fetch에서 분기 결과가 확정되는 단계까지의 거리가 멀어지므로, 그 사이에 투기적으로 진입한 명령어가 많아지고 예측 실패 시 폐기해야 할 작업도 늘어납니다.

5단계 파이프라인에서 예측 실패 시 2클럭이 낭비되지만, 14~20단계 파이프라인에서는 10~20클럭 이상이 낭비됩니다.

### 분기 예측의 방식

분기 명령어의 결과는 두 가지뿐입니다.

조건이 참이어서 점프하는 **taken**과, 조건이 거짓이어서 점프하지 않고 다음 명령어로 진행하는 **not-taken**입니다.

분기 예측기는 이 둘 중 어느 쪽이 될지를 추측합니다.

<br>

가장 단순한 방식은 **정적 예측(Static Prediction)**입니다.

"뒤로 향하는 분기(이미 실행한 주소로 점프하는 분기)는 항상 taken, 앞으로 향하는 분기는 항상 not-taken"이라고 가정합니다.

루프의 끝에서 루프 시작으로 돌아가는 분기가 "뒤로 향하는 분기"의 대표적인 예입니다. 루프는 대부분 반복을 계속하므로(= taken), 이 규칙이 잘 맞습니다. 일반적인 벤치마크에서 이 규칙만으로도 약 90%의 예측 정확도에 이릅니다.

<br>

현대 CPU에서 사용하는 **동적 예측(Dynamic Prediction)**은 과거의 분기 기록을 기반으로 예측합니다.

분기 명령어마다 최근 몇 번의 실행에서 taken이었는지 not-taken이었는지를 기록하고, 패턴을 학습합니다. 단순한 2비트 포화 카운터부터, 수천 개의 분기 기록을 상관 분석하는 복잡한 예측기까지 다양한 방식이 존재합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2비트 포화 카운터 (Branch History)</text>
  <rect x="20" y="80" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Strongly</text>
  <text x="80" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Not-Taken</text>
  <text x="80" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">(00)</text>
  <rect x="160" y="80" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Weakly</text>
  <text x="220" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Not-Taken</text>
  <text x="220" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">(01)</text>
  <rect x="300" y="80" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Weakly</text>
  <text x="360" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Taken</text>
  <text x="360" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">(10)</text>
  <rect x="440" y="80" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.5"/>
  <text x="500" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Strongly</text>
  <text x="500" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Taken</text>
  <text x="500" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">(11)</text>
  <line x1="140" y1="98" x2="156" y2="98" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,98 152,94 152,102" fill="currentColor"/>
  <text x="150" y="74" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">taken</text>
  <line x1="280" y1="98" x2="296" y2="98" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="300,98 292,94 292,102" fill="currentColor"/>
  <text x="290" y="74" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">taken</text>
  <line x1="420" y1="98" x2="436" y2="98" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="440,98 432,94 432,102" fill="currentColor"/>
  <text x="430" y="74" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">taken</text>
  <line x1="300" y1="116" x2="284" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="280,116 288,112 288,120" fill="currentColor"/>
  <text x="290" y="148" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">not-taken</text>
  <line x1="160" y1="116" x2="144" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,116 148,112 148,120" fill="currentColor"/>
  <text x="150" y="148" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">not-taken</text>
  <line x1="440" y1="116" x2="424" y2="116" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="420,116 428,112 428,120" fill="currentColor"/>
  <text x="430" y="148" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.75">not-taken</text>
  <path d="M 40 80 Q 40 56 60 56 Q 80 56 80 80" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3,2" opacity="0.7"/>
  <polygon points="80,80 76,72 84,72" fill="currentColor" opacity="0.7"/>
  <text x="60" y="50" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.6">not-taken</text>
  <path d="M 520 80 Q 520 56 540 56 Q 560 56 560 80" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="3,2" opacity="0.7"/>
  <polygon points="560,80 556,72 564,72" fill="currentColor" opacity="0.7"/>
  <text x="540" y="50" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.6">taken</text>
  <text x="290" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">결과가 taken이면 오른쪽으로, not-taken이면 왼쪽으로 이동합니다.</text>
  <text x="290" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">양 끝에서는 더 이동하지 않으므로 "포화(saturating)" 카운터로 부릅니다.</text>
  <text x="290" y="226" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예측 기준</text>
  <text x="290" y="244" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">상태 00, 01 → Not-Taken으로 예측</text>
  <text x="290" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">상태 10, 11 → Taken으로 예측</text>
</svg>
</div>

<br>

현대 CPU의 동적 분기 예측 정확도는 **95% 이상**이며, 고성능 데스크톱 CPU에서는 97~99%에 달합니다.

수천 개 분기의 이력을 상관 분석하는 글로벌 히스토리 예측기, 여러 히스토리 길이를 동시에 참조하는 TAGE 예측기 등 2비트 카운터보다 발전한 방식들이 이 정확도를 가능하게 합니다. 루프처럼 규칙적인 분기는 거의 100%에 가까운 정확도로 예측됩니다.

### 게임에서의 의미

게임 코드에서 분기 예측의 영향이 드러나는 대표적인 상황은 **예측 불가능한 분기 패턴**입니다.

정렬되지 않은 배열을 순회하면서 조건 검사를 수행할 때, 조건의 참/거짓이 무작위에 가깝게 번갈아 나타나면 분기 예측기가 패턴을 학습할 수 없습니다. 이 경우 예측 실패율이 높아집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <text x="240" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">예측하기 쉬운 패턴 vs 어려운 패턴</text>
  <text x="20" y="50" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">패턴 A — 예측 쉬움 (루프: 대부분 taken)</text>
  <rect x="120" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="132" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="148" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="160" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="176" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="188" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="204" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="216" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="232" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="244" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="260" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="272" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="288" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="300" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="316" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="328" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="344" y="60" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="356" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="372" y="60" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/><text x="384" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">F</text>
  <text x="240" y="106" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">예측기가 "taken"으로 학습 → 정확도 90%</text>
  <text x="20" y="142" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">패턴 B — 예측 어려움 (무작위에 가까운 패턴)</text>
  <rect x="120" y="152" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="132" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="148" y="152" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/><text x="160" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">F</text>
  <rect x="176" y="152" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="188" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="204" y="152" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="216" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="232" y="152" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/><text x="244" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">F</text>
  <rect x="260" y="152" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="272" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="288" y="152" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/><text x="300" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">F</text>
  <rect x="316" y="152" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/><text x="328" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">F</text>
  <rect x="344" y="152" width="24" height="22" fill="currentColor" fill-opacity="0.30"/><text x="356" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">T</text>
  <rect x="372" y="152" width="24" height="22" fill="none" stroke="currentColor" stroke-width="1" opacity="0.6"/><text x="384" y="168" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.7">F</text>
  <text x="240" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">예측기가 패턴을 찾기 어려움 → 정확도 낮음</text>
  <text x="240" y="222" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">진한 칸 = taken (T), 빈 칸 = not-taken (F)</text>
</svg>
</div>

<br>

Unity에서 `Update()` 루프 안에 많은 조건 분기가 있는 경우, 오브젝트 상태에 따라 분기 방향이 불규칙하게 바뀌면 CPU 파이프라인 효율이 떨어집니다.

분기 하나의 예측 실패는 10~20클럭 수준의 낭비이지만, 수천 개의 오브젝트를 매 프레임 처리하면 이 낭비가 누적되어 체감 가능한 성능 차이를 만들 수 있습니다.

<br>

데이터를 미리 정렬하거나, 조건 분기 대신 수학 연산으로 대체하는 기법(**브랜치리스 프로그래밍**)이 이 문제를 완화합니다.

모든 분기를 제거할 수는 없지만, 핫 루프(자주 실행되는 반복문)에서 분기 패턴이 불규칙하지 않은지 점검하고, 불규칙한 패턴을 정렬이나 브랜치리스 연산으로 줄이는 것이 실용적인 접근입니다.

---

## ILP와 슈퍼스칼라 실행

파이프라인은 명령어 실행의 각 단계를 겹쳐서 스루풋을 높이지만, 파이프라인 하나로는 클럭당 완료되는 명령어가 최대 1개입니다.

**슈퍼스칼라(Superscalar)** 실행은 Fetch·Decode·Execute 등 각 단계의 하드웨어를 여러 벌 배치하여, 클럭당 2개 이상의 명령어를 동시에 처리하는 구조입니다.

다만, 아무 명령어나 동시에 실행할 수 있는 것은 아닙니다. 서로 의존성이 없는 명령어만 동시에 실행해도 결과가 동일하게 유지되므로, 프로그램 안에 그런 독립적인 명령어가 얼마나 존재하는지가 동시 실행의 전제 조건이 됩니다.

### ILP (Instruction Level Parallelism)

**ILP(Instruction-Level Parallelism, 명령어 수준 병렬성)**는 프로그램의 명령어 흐름에 내재된 동시 실행 가능량을 뜻합니다.

서로 의존성이 없는 명령어가 많을수록 ILP가 높고, 직전 결과에 의존하는 명령어 체인이 길수록 ILP가 낮습니다.

ILP는 프로그램 코드 자체의 특성이지, CPU 하드웨어의 특성이 아닙니다. 하드웨어는 코드에 내재된 ILP를 활용하는 역할을 할 뿐, ILP 자체를 만들어내지는 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">ILP 예시</text>
  <rect x="30" y="50" width="220" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="72" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="currentColor">A: R1 = R2 + R3</text>
  <text x="140" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">R2와 R3을 더해 R1에 저장</text>
  <rect x="30" y="120" width="220" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="142" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="currentColor">B: R4 = R5 * R6</text>
  <text x="140" y="159" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">R5와 R6을 곱해 R4에 저장</text>
  <rect x="350" y="85" width="200" height="50" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="107" text-anchor="middle" font-family="monospace" font-size="12" font-weight="bold" fill="currentColor">C: R7 = R1 + R4</text>
  <text x="450" y="124" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">R1과 R4를 더해 R7에 저장</text>
  <path d="M 250 75 L 310 75 L 310 110" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <path d="M 250 145 L 310 145 L 310 110" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="310" y1="110" x2="346" y2="110" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="350,110 342,106 342,114" fill="currentColor"/>
  <text x="140" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">서로 다른 레지스터 사용 → 의존성 없음</text>
  <text x="140" y="211" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">동시 실행 가능 (ILP 존재)</text>
  <text x="450" y="155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">A, B 결과를 모두 필요로 함</text>
  <text x="450" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">→ A, B가 끝나야 실행 가능</text>
</svg>
</div>

<br>

위 예시에서 A와 B는 서로 다른 레지스터를 사용하므로 의존성이 없고, 하드웨어가 이 두 명령어를 동시에 실행하면 클럭당 완료하는 명령어 수(IPC)가 올라갑니다.

반면 C는 A와 B의 결과를 모두 필요로 하므로, 두 명령어가 완료될 때까지 대기해야 합니다.

게임 코드에서 벡터 좌표 X·Y·Z를 각각 독립적으로 계산하는 구간은 ILP가 높고, 한 값의 결과를 다음 계산의 입력으로 사용하는 연쇄 연산 구간은 ILP가 낮습니다.

### 슈퍼스칼라 CPU

슈퍼스칼라 CPU는 프로그램에 내재된 ILP를 실제로 활용하는 하드웨어 구조입니다.

파이프라인의 각 단계에 여러 유닛을 배치하여, 한 클럭 사이클에 여러 명령어를 동시에 페치·디코드·실행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
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
  <text x="290" y="87" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">A와 동시 실행</text>
  <text x="290" y="131" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">C와 동시 실행</text>
  <text x="230" y="170" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">매 클럭마다 2개의 명령어를 Fetch · Decode · Execute</text>
  <text x="230" y="194" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이상적으로 클럭당 2개의 명령어 완료</text>
</svg>
</div>

<br>

2-way 슈퍼스칼라는 Fetch 유닛 2개, Decode 유닛 2개, 실행 유닛(ALU, FPU 등) 2개 이상을 배치하여 클럭당 최대 2개의 명령어를 처리합니다.

4-way라면 각 단계 유닛이 4벌이므로 클럭당 최대 4개입니다.

현대 데스크톱 CPU(Intel Alder Lake 이후, Apple M 시리즈 등)는 6-way 이상의 슈퍼스칼라 구조를 사용합니다.

<br>

다만, 이 최대치를 매 클럭 달성할 수 있는 것은 아닙니다.

명령어 간 의존성(데이터 해저드)이 있으면 동시에 실행할 수 없고, 같은 유형의 실행 유닛이 부족해도 대기가 발생합니다(구조적 해저드).

슈퍼스칼라의 실질적 성능 상한은, 프로그램에 내재된 ILP의 양과 하드웨어가 갖춘 실행 유닛의 수가 함께 결정합니다.

### 클럭 속도와 IPC의 관계

CPU 성능은 **클럭 속도(Clock Speed)**와 **IPC(Instructions Per Clock)**의 곱으로 근사됩니다.

<br>

$$\text{성능} \;\propto\; \text{클럭 속도} \;\times\; \text{IPC}$$

클럭 속도는 초당 사이클 수(GHz 단위 — 3.0 GHz는 초당 30억 사이클)이고, IPC는 클럭 사이클당 완료되는 명령어 수입니다. 파이프라인·슈퍼스칼라·분기 예측 같은 구조가 IPC를 결정합니다.

| CPU | 클럭 속도 | IPC | 초당 명령어 수 |
|:---:|:---:|:---:|:---:|
| A | 3.0 GHz | 2.0 | 60억 |
| B | 2.5 GHz | 3.0 | 75억 |

<br>

클럭 속도만 보면 CPU A가 빨라 보이지만, IPC까지 고려하면 CPU B가 초당 더 많은 명령어를 처리합니다.

과거에는 클럭 속도를 높이는 것이 성능 향상의 주된 방법이었습니다.

하지만 클럭이 올라갈수록 전력 소모는 주파수의 세제곱에 비례하여 증가하고, 발열 역시 급격히 심해집니다.

이 물리적 한계를 **전력 벽(Power Wall)**이라 부르며, 2000년대 중반 이후 클럭 경쟁은 둔화되었습니다.

이후 CPU 아키텍처의 발전 방향은 IPC를 높이는 쪽으로 전환되었고, 파이프라인 효율 개선, 더 넓은 슈퍼스칼라, 더 정교한 분기 예측이 그 수단입니다.

<br>

모바일 CPU는 발열과 배터리 제약으로 클럭 속도를 데스크톱만큼 높이기 어렵습니다.

클럭을 올리기 어려운 만큼, 같은 클럭에서 완료하는 명령어 수 -- 즉 IPC -- 가 모바일 CPU의 성능을 더 크게 좌우합니다.

최근 모바일 AP(Arm Cortex-X 시리즈, Apple A/M 시리즈)가 세대마다 IPC 향상을 핵심 지표로 내세우는 이유가 여기에 있습니다.

---

## in-order vs out-of-order 실행

파이프라인과 슈퍼스칼라는 CPU가 명령어를 빠르게 처리하는 기반 구조입니다.

여기에 더해, 명령어의 **실행 순서**를 어떻게 관리하느냐에 따라 CPU 아키텍처가 크게 두 갈래로 나뉩니다.

### in-order 실행

in-order 실행은 프로그램에 적힌 순서 그대로 명령어를 실행하는 방식입니다.

명령어 A 다음에 명령어 B가 있으면, A가 완료되어야 B를 실행합니다. A에 데이터 해저드가 있어 스톨이 발생하면, B가 A와 의존성이 없더라도 대기해야 합니다.

<br>

예시로 명령어 A `LOAD R1, [mem]`(메모리에서 값을 읽어 R1에 저장 — 캐시 미스 시 수십 클럭 소요), 명령어 B `ADD R3, R4, R5`(R4+R5 → R3, A와 의존성 없음), 명령어 C `MUL R6, R1, R7`(R1 사용 — A의 결과 필요)을 가정해 봅시다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">in-order 실행</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="96" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="128" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="160" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="216" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4 ··· 29</text>
  <text x="272" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">30</text>
  <text x="304" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">31</text>
  <text x="336" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">32</text>
  <text x="368" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">33</text>
  <text x="400" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">34</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 A</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 B</text>
  <text x="75" y="109" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 C</text>
  <rect x="80" y="50" width="336" height="66" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="416" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="94" x2="416" y2="94" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="256" y1="50" x2="256" y2="116" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>
  <rect x="80" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="96" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="112" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="128" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="144" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="160" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="176" y="50" width="80" height="22" fill="currentColor" fill-opacity="0.18"/><text x="216" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM ··· MEM</text>
  <rect x="256" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="272" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="112" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="128" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="144" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="160" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="176" y="72" width="80" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.6"/><text x="216" y="87" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">스톨 ··· 스톨</text>
  <rect x="256" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="272" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="288" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="304" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="320" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="336" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="144" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="160" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="176" y="94" width="80" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.6"/><text x="216" y="109" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">스톨 ··· 스톨</text>
  <rect x="256" y="94" width="32" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.5"/><text x="272" y="109" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.6">스톨</text>
  <rect x="288" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="304" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="320" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="336" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="352" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="368" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="230" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">A: 캐시 미스로 MEM이 수십 클럭 동안 지속</text>
  <text x="230" y="166" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">B: A와 무관하지만 in-order이므로 대기 (낭비)</text>
  <text x="230" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">C: A의 결과 필요 → 대기는 정당</text>
  <text x="230" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">B는 A와 무관한데도 A의 MEM이 끝날 때까지 대기 → 낭비</text>
</svg>
</div>

<br>

in-order 실행의 장점은 구조가 단순하다는 점입니다.

명령어 순서를 추적하거나 재배치하는 복잡한 하드웨어가 필요 없으므로, 트랜지스터 수가 적고 제어 회로도 간결합니다.

그만큼 전력 소모가 적고 발열이 낮습니다. **다이(die)** -- 반도체 회로가 새겨진 실리콘 조각 -- 의 면적도 작아 제조 비용이 낮습니다.

### out-of-order 실행

out-of-order(OoO) 실행은 명령어 간의 **의존성을 분석**하여, 순서를 바꿔도 결과가 같은 명령어를 먼저 실행하는 방식입니다.

프로그램의 의미(결과)는 보존하면서 실행 순서만 최적화합니다.

<br>

같은 세 명령어가 out-of-order 실행에서는 다음과 같이 처리됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <text x="230" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">out-of-order 실행</text>
  <text x="6" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">시간(클럭)</text>
  <text x="96" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">1</text>
  <text x="128" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">2</text>
  <text x="160" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3</text>
  <text x="192" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">4</text>
  <text x="248" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">5 ··· 29</text>
  <text x="304" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-weight="bold">30</text>
  <text x="336" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">31</text>
  <text x="368" y="46" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">32</text>
  <text x="75" y="65" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 A</text>
  <text x="75" y="87" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 B</text>
  <text x="75" y="109" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">명령어 C</text>
  <rect x="80" y="50" width="304" height="66" fill="none" stroke="currentColor" stroke-width="1" opacity="0.55"/>
  <line x1="80" y1="72" x2="384" y2="72" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="80" y1="94" x2="384" y2="94" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <line x1="288" y1="50" x2="288" y2="116" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>
  <rect x="80" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="96" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="112" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="128" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="144" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="160" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="176" y="50" width="112" height="22" fill="currentColor" fill-opacity="0.18"/><text x="232" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM ··· MEM</text>
  <rect x="288" y="50" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="304" y="65" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="112" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="128" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="144" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="160" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="176" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="192" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="208" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="224" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="240" y="72" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="256" y="87" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <rect x="144" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="160" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">IF</text>
  <rect x="176" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="192" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">ID</text>
  <rect x="208" y="94" width="80" height="22" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.6"/><text x="248" y="109" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.7">대기 ···</text>
  <rect x="288" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.22"/><text x="304" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">EX</text>
  <rect x="320" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.14"/><text x="336" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MEM</text>
  <rect x="352" y="94" width="32" height="22" fill="currentColor" fill-opacity="0.10"/><text x="368" y="109" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">WB</text>
  <text x="230" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">A: 캐시 미스로 MEM이 수십 클럭 동안 지속</text>
  <text x="230" y="166" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">B: A를 기다리지 않고 즉시 실행 (의존성 없음)</text>
  <text x="230" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">C: A의 결과가 나온 뒤에 실행</text>
  <text x="230" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">B가 A의 MEM 완료를 기다리지 않음 → 파이프라인 유휴 시간 감소</text>
</svg>
</div>

<br>

out-of-order 실행을 구현하려면 CPU 내부에 복잡한 하드웨어가 필요합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">out-of-order 실행에 필요한 하드웨어</text>
  <rect x="220" y="40" width="160" height="48" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="60" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">디스패처</text>
  <text x="300" y="76" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">명령어 해석 · 의존성 분석</text>
  <path d="M 300 88 V 100 H 160 V 124" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,128 156,120 164,120" fill="currentColor"/>
  <text x="170" y="113" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">ROB에 등록 (프로그램 순서 기록)</text>
  <path d="M 300 88 V 100 H 440 V 124" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="440,128 436,120 444,120" fill="currentColor"/>
  <text x="350" y="113" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">RS에 배정 (피연산자 대기)</text>
  <rect x="80" y="128" width="160" height="60" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="160" y="148" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">리오더 버퍼 (ROB)</text>
  <text x="160" y="164" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">프로그램 순서 기록</text>
  <text x="160" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">완료된 결과를 순서대로 커밋</text>
  <rect x="360" y="128" width="160" height="60" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="440" y="148" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예약 스테이션 (RS)</text>
  <text x="440" y="164" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">피연산자가 준비될 때까지 보관</text>
  <text x="440" y="178" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">준비되면 실행 유닛으로 발급</text>
  <line x1="440" y1="188" x2="440" y2="220" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="440,224 436,216 444,216" fill="currentColor"/>
  <text x="448" y="210" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">준비 완료 시</text>
  <rect x="360" y="224" width="160" height="44" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="440" y="248" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">실행 유닛</text>
  <path d="M 360 246 H 280 V 162 H 244" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="240,162 248,158 248,166" fill="currentColor"/>
  <text x="295" y="220" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">결과를 ROB에 기록</text>
  <line x1="160" y1="188" x2="160" y2="284" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="160,288 156,280 164,280" fill="currentColor"/>
  <text x="168" y="240" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7" font-style="italic">프로그램 순서대로</text>
  <rect x="80" y="288" width="160" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2"/>
  <text x="160" y="306" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">커밋 (commit)</text>
  <text x="160" y="322" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.8">결과 확정 — 외부에서 보이는 순서</text>
  <text x="300" y="354" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">실행 순서는 자유롭지만 커밋은 프로그램 순서대로</text>
</svg>
</div>

<br>

**리오더 버퍼(Reorder Buffer, ROB)**는 실행 결과를 바로 확정하지 않고 임시로 보관합니다. 앞의 예시에서 B가 A보다 먼저 실행되었는데, A 실행 중 오류가 발생하면 B의 결과는 되돌려야 합니다. 이미 확정된 결과는 되돌릴 수 없으므로, ROB는 프로그램 순서상 앞선 명령어가 정상 완료된 것을 확인한 뒤에야 차례대로 결과를 확정(**커밋(commit)**)합니다. 실행은 순서 없이 하면서도, 외부에서 보기에는 프로그램 순서대로 완료된 것과 같은 결과를 보장합니다.

**예약 스테이션(Reservation Station, RS)**은 각 명령어가 필요로 하는 피연산자(입력 레지스터 값)를 감시합니다. 앞의 예시에서 C는 A의 결과인 R1이 필요하므로, RS는 R1 값이 실행 유닛에서 생산될 때까지 C를 보관합니다. R1 값이 도착하면 C의 모든 피연산자가 준비된 것이므로, RS는 C를 즉시 실행 유닛으로 보냅니다.

<br>

이 하드웨어들은 트랜지스터를 많이 사용하고, 의존성 분석과 순서 추적에 에너지를 소모합니다.

같은 클럭 속도의 in-order 코어와 비교하면, out-of-order 코어는 **2~3배 이상의 전력**을 소모하고 **칩 면적도 2배 이상 큽니다**.

대신, IPC가 크게 향상되어 같은 클럭에서 **1.5~2배 이상의 성능**을 냅니다.

### 모바일 CPU: big.LITTLE과 DynamIQ

in-order와 out-of-order의 전력-성능 트레이드오프를 실제로 활용하는 대표적인 사례가 모바일 SoC(System on Chip)입니다.

모바일 SoC에서 사용되는 ARM CPU는 in-order 코어와 out-of-order 코어를 함께 탑재합니다. ARM의 **big.LITTLE** 아키텍처(이후 **DynamIQ**로 발전)가 이 방식을 사용합니다.

<br>

**모바일 SoC의 ARM big.LITTLE / DynamIQ 구성 예시**

| 구분 | big 코어 (고성능) | LITTLE 코어 (고효율) |
|:---|:---|:---|
| 예시 | Cortex-A78 / X3 | Cortex-A55 / A510 |
| 실행 방식 | out-of-order | in-order (A510은 제한적 out-of-order) |
| IPC | 높음 | 낮음 |
| 전력 소모 | 높음 | 낮음 |
| 클럭 | 2.5 ~ 3 GHz | 1.8 ~ 2 GHz |
| 코어 수 | 1 ~ 4개 | 4개 |
| 활성화 시점 | 게임, 카메라, 복잡한 연산 | 대기 화면, 알림, 경량 작업 |

<br>

**big 코어**(예: Cortex-A78, Cortex-X3)는 out-of-order 실행, 넓은 슈퍼스칼라(3~6way), 대용량 캐시를 갖춘 고성능 코어입니다. 게임 실행, 영상 편집 같은 무거운 작업에 사용됩니다. 전력 소모가 크므로 장시간 최대 클럭으로 동작하면 발열이 급격히 높아집니다.

<br>

**LITTLE 코어**(예: Cortex-A55, Cortex-A510)는 in-order 실행(또는 제한적인 out-of-order), 좁은 슈퍼스칼라(2~3way), 작은 캐시를 갖춘 저전력 코어입니다. 알림 확인, 음악 재생, 센서 모니터링 같은 가벼운 작업에 사용되며, 전력 소모는 big 코어의 1/10 수준에 불과합니다.

<br>

Cortex-A55는 ARM에서 가장 널리 쓰이는 LITTLE 코어 중 하나로, **in-order 2-way 슈퍼스칼라** 구조입니다. 명령어를 프로그램 순서대로 처리하며, 클럭당 최대 2개의 명령어를 동시에 디코드합니다.

후속 세대인 Cortex-A510은 디코드 폭을 3-way로 넓히면서도 기본적으로 in-order 파이프라인을 유지합니다. 다만, 캐시 미스가 발생했을 때 후속 명령어를 제한적으로 추적할 수 있는 비차단(non-blocking) 메커니즘을 도입하여, 순수 in-order 설계인 A55보다 메모리 지연을 더 잘 흡수합니다. 전력 효율을 크게 희생하지 않으면서 처리량을 높인 설계입니다.

반면 Cortex-A78은 **out-of-order 4-way 슈퍼스칼라**로, 의존성이 없는 명령어를 재배치하여 클럭당 최대 4개의 명령어를 처리합니다.

<br>

데스크톱 CPU(Intel Core, AMD Ryzen)는 전통적으로 모든 코어가 동일한 out-of-order 대칭 구조였습니다.

전원 콘센트에서 수백 와트를 공급받을 수 있으므로, 전력 효율보다 절대 성능을 우선하는 설계입니다.

다만 Intel은 12세대(Alder Lake) 이후부터 고성능 P-core와 고효율 E-core를 혼합하는 비대칭 구조를 도입했습니다. E-core(Gracemont)도 out-of-order 실행을 지원하지만, 실행 폭과 캐시 크기가 P-core보다 작아 전력 효율에 초점을 맞추고 있습니다.

모바일 SoC는 이보다 훨씬 오래전부터 비대칭 구조를 핵심 설계 원칙으로 사용해 왔으며, 배터리 수명과 발열 관리가 성능 못지않게 중요하기 때문에 성격이 다른 코어를 혼합하는 이종(heterogeneous) 구조가 채택됩니다.

### 모바일에서 in-order 코어가 게임 성능에 미치는 영향

게임 실행 중에는 대부분의 연산이 big 코어에서 수행됩니다.

하지만 게임을 장시간 실행하면 SoC의 온도가 상승하고, 운영체제의 전력 관리 모듈이 big 코어의 클럭을 강제로 낮추는 **서멀 쓰로틀링(Thermal Throttling)**이 발생합니다.

서멀 쓰로틀링이 진행되면 big 코어의 클럭이 단계적으로 하락하고, 일부 작업이 LITTLE 코어로 옮겨지는 경우도 있습니다.

<br>

서멀 쓰로틀링이 발생하면 big 코어의 클럭이 낮아져 IPC x 클럭이 감소하고, 프레임 레이트가 하락합니다.

일부 시나리오에서는 운영체제가 게임의 워크로드 일부를 LITTLE 코어로 이동시킵니다.

in-order 코어인 LITTLE 코어의 IPC는 big 코어보다 훨씬 낮으므로, 해당 작업의 처리 시간이 길어지고 전체 프레임 시간에 영향을 줍니다.

<br>

이 때문에 모바일 게임 최적화에서는 **지속 가능한 성능(Sustained Performance)**이라는 개념이 중요합니다.

순간 최대 성능이 아니라, 장시간 안정적으로 유지할 수 있는 성능 수준을 기준으로 게임을 설계해야 합니다.

CPU 연산량을 줄여 big 코어의 부하를 낮추면 발열이 덜 발생하고, 서멀 쓰로틀링을 지연시켜 안정적인 프레임 레이트를 유지할 수 있습니다.

<br>

**모바일 CPU 아키텍처 비교 정리**

| 구분 | in-order 코어 (예: A55) | out-of-order 코어 (예: A78) |
|:---|:---|:---|
| 명령어 실행 순서 | 프로그램 순서 그대로 | 의존성 분석 후 재배치 |
| 슈퍼스칼라 | 2-way | 4-way 이상 |
| IPC | 낮음 | 높음 |
| 전력 소모 | 낮음 (0.05W 대) | 높음 (1W 대) |
| 칩 면적 | 작음 | 큼 |
| 분기 예측 실패 대응 | 단순 (페널티 작음) | 정교 (페널티 큼) |
| 파이프라인 깊이 | 짧음 (8 ~ 10단계) | 김 (11 ~ 15단계) |
| 주 용도 | 대기, 경량 작업 | 게임, 카메라, 연산 |

<br>

in-order 코어와 out-of-order 코어의 차이는 "느린 코어"와 "빠른 코어"로 단순화할 수 없습니다.

전력과 성능 사이의 트레이드오프에서 서로 다른 지점을 선택한 결과이며, 모바일 환경에서는 두 유형이 함께 존재하는 것이 합리적입니다.

게임 개발자의 입장에서는, 게임이 in-order 코어에서 실행될 가능성을 인지하고 CPU 연산 비용을 최소화하여, 어떤 코어에서든 **프레임 예산**(한 프레임을 완성하는 데 허용된 시간, 60fps 기준 약 16.67ms)을 지킬 수 있도록 설계하는 것이 바람직합니다.

---

## 마무리

- 파이프라인은 명령어 실행의 각 단계를 겹쳐 처리하여 스루풋을 높이며, 해저드(데이터/제어/구조적)가 연속 실행을 방해합니다.
- 분기 예측기는 분기 결과를 미리 추측하여 파이프라인 스톨을 줄입니다. 현대 CPU의 예측 정확도는 95% 이상이지만, 예측 실패 시 파이프라인 플러시로 10~20클럭이 낭비됩니다.
- 슈퍼스칼라 CPU는 한 클럭에 여러 명령어를 동시에 처리하여 IPC를 높이며, CPU 성능은 클럭 속도 × IPC로 결정됩니다.
- in-order 실행은 저전력, out-of-order 실행은 고IPC이며, 모바일 SoC는 두 유형을 함께 탑재하여 성능과 전력 효율을 양립합니다.
- 서멀 쓰로틀링으로 big 코어의 성능이 하락하거나 LITTLE 코어로 워크로드가 이동할 수 있으므로, 모바일 게임에서는 지속 가능한 성능을 기준으로 설계해야 합니다.

파이프라인 위에서 해저드를 줄이고, IPC를 높이고, 실행 순서를 재배치하는 기법들은 모두 같은 목표를 향합니다. CPU 내부의 하드웨어 유닛이 한 클럭이라도 유휴 상태로 남지 않도록 하는 것입니다.

<br>

CPU가 명령어를 효율적으로 처리하더라도, 명령어가 다루는 데이터는 메모리에 저장되어 있습니다. CPU가 아무리 빠르게 명령어를 실행해도, 데이터를 메모리에서 가져오는 데 시간이 오래 걸리면 파이프라인은 대기할 수밖에 없습니다.

[하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)에서는 CPU와 메모리 사이의 속도 차이, 캐시의 원리, 그리고 메모리 접근 패턴이 게임 성능에 미치는 영향을 다룹니다.

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
