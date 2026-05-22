---
layout: single
title: "파티클과 애니메이션 (2) - 애니메이션 최적화 - soo:bak"
date: "2026-02-19 23:50:00 +0900"
description: Animator, 애니메이션 압축, Generic vs Humanoid, Culling 모드, GPU Skinning을 설명합니다.
tags:
  - Unity
  - 최적화
  - 애니메이션
  - Animator
---

## 파티클에서 애니메이션으로

[Part 1](/dev/unity/ParticleAndAnimation-1/)에서는 파티클 시스템의 비용 구조를 살펴보았습니다. 파티클의 비용은 CPU 시뮬레이션과 GPU 렌더링으로 나뉘며, 특히 반투명 입자가 겹치며 누적되는 오버드로우가 프래그먼트 셰이더 예산을 빠르게 소모합니다.

파티클이 시각 효과를 위한 서브시스템이라면, **애니메이션**은 캐릭터와 오브젝트의 움직임을 위한 서브시스템입니다. 캐릭터의 걷기·공격·피격 반응, 문 열림, UI 슬라이드, 환경 오브젝트의 흔들림이 모두 애니메이션에 해당합니다.

Unity는 매 프레임 활성 캐릭터의 애니메이션을 CPU에서 평가합니다. 재생 중인 클립에서 현재 시점의 값을 읽어 본의 Transform(위치·회전·크기)과 머티리얼 프로퍼티(색상·알파 등)를 갱신합니다. 한 캐릭터의 갱신은 가벼운 작업이지만, 활성 캐릭터가 늘고 캐릭터당 본 수가 많아질수록 같은 평가가 반복되며 메인 스레드 비용이 빠르게 늘어납니다.

이번 글에서는 애니메이션 비용이 어디에서 발생하는지부터 살펴봅니다. Animator의 매 프레임 평가 비용, 클립 데이터 압축, Generic·Humanoid 리그 타입의 차이, Animation Culling 모드를 차례로 다룹니다. 마지막으로 본의 계산 결과를 메쉬 정점에 적용하는 스키닝 단계가 CPU와 GPU 비용에 어떤 차이를 만드는지도 함께 살펴봅니다.

---

## 애니메이션 시스템

애니메이션을 처리하는 방식은 하나로 고정되지 않습니다. 복잡한 캐릭터처럼 상태 전환과 블렌딩이 필요한 대상도 있고, UI 패널 이동이나 문 열림처럼 시작 값과 끝 값만 있으면 충분한 대상도 있습니다.

Unity에서 이런 복잡한 흐름을 다루는 대표적인 시스템이 **Animator(Mecanim)**입니다. Animator는 상태 머신, 트랜지션, 블렌드 트리를 제공하지만, 그만큼 매 프레임 상태 평가와 블렌딩 계산이 필요합니다. 따라서 어떤 대상에 Animator를 사용할지, 더 단순한 트위닝이나 스크립트 제어로 충분한지는 비용 관점에서 구분해야 합니다.

### Animator (Mecanim)

Animator는 Unity에서 캐릭터 애니메이션을 구성할 때 가장 많이 사용하는 시스템입니다. 핵심은 **Animator Controller**이며, 이 컨트롤러는 상태 머신(State Machine)을 사용해 현재 재생할 애니메이션 상태와 상태 전환 조건을 관리합니다.

예를 들어 캐릭터가 대기, 달리기, 점프 상태를 오갈 때 Animator는 현재 상태를 평가하고, 파라미터 조건에 따라 다음 상태로 전환하며, 전환 중에는 두 클립을 블렌딩합니다. 이 구조는 복잡한 캐릭터 행동을 표현하기 좋지만, 매 프레임 상태 평가와 블렌딩 비용이 발생합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 460" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Animator (Mecanim) 구조</text>

  <text x="40" y="50" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Animator Controller (상태 머신)</text>

  <rect x="60" y="68" width="110" height="56" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="115" y="91" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Idle</text>
  <text x="115" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(대기)</text>

  <rect x="225" y="68" width="110" height="56" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="91" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Run</text>
  <text x="280" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(달리기)</text>

  <rect x="390" y="68" width="110" height="56" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="445" y="91" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Jump</text>
  <text x="445" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(점프)</text>

  <line x1="170" y1="90" x2="220" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="215,85 225,90 215,95" fill="currentColor"/>
  <text x="195" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">달리기</text>

  <line x1="335" y1="90" x2="385" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="380,85 390,90 380,95" fill="currentColor"/>
  <text x="360" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">점프</text>

  <path d="M 445 124 Q 445 165 280 165 Q 115 165 115 124" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="110,118 115,128 120,118" fill="currentColor"/>
  <text x="280" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">착지</text>

  <line x1="40" y1="195" x2="520" y2="195" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>

  <text x="40" y="218" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">매 프레임 처리</text>

  <rect x="40" y="232" width="480" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="252" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1) 상태 머신 평가</text>
  <text x="60" y="270" font-family="sans-serif" font-size="11" fill="currentColor">현재 상태의 트랜지션 조건 검사 → 조건 충족 시 다음 상태로 전환</text>

  <rect x="40" y="288" width="480" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="308" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">2) 블렌딩 계산</text>
  <text x="60" y="326" font-family="sans-serif" font-size="11" fill="currentColor">상태 전환 중이면 두 클립 블렌딩 + 블렌드 트리 가중치 계산</text>

  <rect x="40" y="344" width="480" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="364" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3) 클립 샘플링</text>
  <text x="60" y="382" font-family="sans-serif" font-size="11" fill="currentColor">현재 시간에 해당하는 키프레임 값 보간</text>

  <rect x="40" y="400" width="480" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="420" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">4) Transform 적용</text>
  <text x="60" y="438" font-family="sans-serif" font-size="11" fill="currentColor">계산된 값을 본(Bone)의 Transform에 기록</text>
</svg>
</div>

<br>

Animator는 상태 전환(Transition), 파라미터 조건, 블렌드 트리(Blend Tree)를 이용해 복잡한 애니메이션 흐름을 구성합니다. 예를 들어 캐릭터의 이동 속도에 따라 걷기와 달리기를 섞거나, 공격 중 피격 상태로 전환하는 흐름을 상태 머신 안에서 처리할 수 있습니다.

이 구조는 캐릭터 행동을 표현하기에 편리하지만, 매 프레임 평가해야 할 항목도 함께 늘어납니다. Animator는 현재 상태를 확인하고, 트랜지션 조건을 검사하고, 필요한 경우 블렌딩 가중치를 계산합니다. 상태, 트랜지션, 레이어, 블렌드 트리가 많아질수록 평가 비용도 커집니다.

### 선택 기준

Animator가 필요한지는 애니메이션의 길이나 시각적 중요도보다 **상태 전환과 블렌딩이 필요한지**로 판단하는 편이 적절합니다. 여러 상태를 오가고, 조건에 따라 전환하고, 클립을 섞어야 한다면 Animator가 맞습니다. 반대로 시작 값과 끝 값만 있거나 단순 반복만 필요하다면 트위닝 라이브러리나 스크립트 제어가 더 가볍습니다.

<br>

| 판단 기준 | Animator가 적합한 경우 | 트위닝·스크립트가 적합한 경우 |
|---|---|---|
| 상태 전환 | 대기, 이동, 공격, 피격처럼 여러 상태를 조건에 따라 전환 | 단일 동작을 시작하고 끝내면 충분 |
| 블렌딩 | 걷기와 달리기, 상체와 하체처럼 여러 클립을 섞어야 함 | 시작 값과 끝 값 사이를 보간하면 충분 |
| 대상 | 플레이어 캐릭터, 복잡한 NPC, 리타겟팅이 필요한 캐릭터 | UI 패널, 버튼 효과, 문 열림, 단순 환경 오브젝트 |
| 비용 특성 | 상태 머신 평가와 블렌딩 비용이 발생 | 상태 머신 없이 필요한 값만 갱신 |

<br>

정해진 값 사이를 한 번 이동하거나 단순히 반복하는 동작이라면, 상태 머신을 평가하거나 클립을 블렌딩할 필요가 없습니다. 버튼 확대, 패널 슬라이드, 문 열림처럼 시작 값과 끝 값이 분명한 동작이 여기에 해당합니다.

이런 경우에는 Animator보다 트위닝이나 스크립트 제어가 더 단순합니다. 트위닝 라이브러리(DOTween 등)는 시작 값, 끝 값, 지속 시간, easing을 기준으로 중간 값을 보간하므로, 상태 전환이 필요 없는 UI나 환경 오브젝트의 움직임을 Animator 평가 비용 없이 처리할 수 있습니다.

---

## 애니메이션 압축

애니메이션 비용은 어떤 시스템으로 재생하느냐뿐 아니라, 재생할 클립이 얼마나 많은 데이터를 가지고 있느냐에도 영향을 받습니다. 애니메이션 클립은 시간에 따른 위치, 회전, 크기 값을 키프레임으로 저장하고, Unity는 매 프레임 현재 시간에 필요한 값을 샘플링해 Transform에 적용합니다.

클립에 키프레임이 많을수록 메모리에 올려야 할 데이터가 늘고, 샘플링할 커브도 많아집니다. 애니메이션 압축은 결과 품질을 크게 해치지 않는 범위에서 불필요한 키프레임과 정밀도를 줄여, 클립 데이터 크기와 샘플링 부담을 낮추는 작업입니다.

### 키프레임 데이터의 구조

애니메이션 클립은 시간에 따른 값의 변화를 **키프레임(Keyframe)**으로 기록합니다. 키프레임은 “0초에는 이 값, 0.5초에는 이 값, 1초에는 이 값”처럼 특정 시점의 값을 저장한 데이터입니다. Unity는 재생 중인 시간에 맞춰 키프레임 사이를 보간하고, 그 결과를 본(Bone)의 위치나 회전 값에 적용합니다.

이 키프레임들은 값의 종류마다 별도의 커브를 이룹니다. 본 하나를 움직이려면 위치, 회전, 크기 값이 필요하고, 각 값은 다시 여러 성분으로 나뉩니다. 위치와 크기는 x, y, z 세 축으로 저장되고, 회전은 오일러 각이나 쿼터니언 값으로 저장됩니다. 따라서 본 하나만 보더라도 여러 개의 애니메이션 커브가 만들어집니다.

이 구조가 캐릭터 전체로 확장되면 데이터 양은 빠르게 커집니다. 예를 들어 본이 50개인 캐릭터에 5초 길이의 클립이 있고, 30fps 기준으로 키가 기록되어 있다면 150개의 시간 지점이 생깁니다. 본마다 약 10개의 커브가 있다고 단순화하면, 한 클립에 `50 × 10 × 150 = 75,000`개의 키프레임 값이 포함될 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">애니메이션 클립의 데이터 구조</text>

  <text x="40" y="50" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">본(Bone) 하나, 위치(x) 커브의 예</text>

  <rect x="40" y="65" width="500" height="60" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="84" font-family="sans-serif" font-size="11" fill="currentColor">프레임</text>
  <text x="60" y="104" font-family="sans-serif" font-size="11" fill="currentColor">값</text>
  <text x="160" y="84" font-family="sans-serif" font-size="11" fill="currentColor">0</text>
  <text x="160" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.0</text>
  <text x="210" y="84" font-family="sans-serif" font-size="11" fill="currentColor">1</text>
  <text x="210" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.1</text>
  <text x="260" y="84" font-family="sans-serif" font-size="11" fill="currentColor">2</text>
  <text x="260" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.2</text>
  <text x="310" y="84" font-family="sans-serif" font-size="11" fill="currentColor">3</text>
  <text x="310" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.3</text>
  <text x="360" y="84" font-family="sans-serif" font-size="11" fill="currentColor">4</text>
  <text x="360" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.3</text>
  <text x="410" y="84" font-family="sans-serif" font-size="11" fill="currentColor">5</text>
  <text x="410" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.3</text>
  <text x="460" y="84" font-family="sans-serif" font-size="11" fill="currentColor">6</text>
  <text x="460" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.3</text>
  <text x="510" y="84" font-family="sans-serif" font-size="11" fill="currentColor">7</text>
  <text x="510" y="104" font-family="sans-serif" font-size="11" fill="currentColor">0.5</text>

  <text x="290" y="148" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 8개의 키프레임이 하나의 커브를 구성</text>

  <line x1="40" y1="170" x2="540" y2="170" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>

  <text x="40" y="195" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">본 1개당 커브 수</text>
  <text x="40" y="215" font-family="sans-serif" font-size="11" fill="currentColor">위치(3) + 회전(3~4) + 크기(3) = 9~10개</text>

  <rect x="40" y="232" width="500" height="42" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="290" y="252" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">본 50개 × 커브 10개 × 프레임 150개</text>
  <text x="290" y="268" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">= 75,000개의 키프레임 값</text>

  <text x="40" y="298" font-family="sans-serif" font-size="11" fill="currentColor">각 값이 float(4바이트)이면:</text>
  <text x="60" y="318" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">75,000 × 4 = 300,000 바이트 ≒ 약 300 KB (비압축)</text>

  <text x="40" y="346" font-family="sans-serif" font-size="11" fill="currentColor">캐릭터 애니메이션 클립이 20개라면:</text>
  <text x="60" y="366" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">300 KB × 20 = 약 6 MB (비압축)</text>
</svg>
</div>

<br>

이 데이터는 클립이 재생될 때 메모리에서 읽히고, 매 프레임 현재 시간에 맞는 값으로 샘플링됩니다. 클립 수가 많거나 키프레임이 과하게 많으면 메모리 사용량이 늘고, 애니메이션 평가 중에 읽어야 할 데이터도 많아집니다.

따라서 애니메이션 압축의 첫 번째 목표는 필요한 움직임은 유지하면서 불필요한 키프레임을 줄이는 것입니다. 데이터가 작아지면 메모리 사용량이 줄고, 매 프레임 샘플링해야 하는 커브 데이터도 가벼워집니다.

<br>

### 키프레임 리덕션 (Keyframe Reduction)

키프레임 리덕션은 보간으로 충분히 복원할 수 있는 키프레임을 제거해 데이터를 줄이는 기법입니다. 모든 프레임의 값을 그대로 저장하지 않고, 움직임의 형태를 유지하는 데 필요한 지점만 남깁니다.

예를 들어 어떤 커브에서 프레임 3~6의 값이 모두 `0.3`이라면, 네 프레임을 모두 저장할 필요가 없습니다. 구간의 시작과 끝만 남겨도 중간 값은 보간으로 같은 결과를 만들 수 있습니다. 값이 일정한 구간뿐 아니라 거의 직선에 가까운 변화도 같은 방식으로 줄일 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">키프레임 리덕션</text>

  <text x="40" y="48" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">원본 (8개 키프레임)</text>

  <g>
    <rect x="40" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="70" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">0:0.0</text>
    <rect x="100" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="130" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">1:0.1</text>
    <rect x="160" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="190" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">2:0.2</text>
    <rect x="220" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="250" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">3:0.3</text>
    <rect x="280" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
    <text x="310" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">4:0.3</text>
    <rect x="340" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
    <text x="370" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">5:0.3</text>
    <rect x="400" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
    <text x="430" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">6:0.3</text>
    <rect x="460" y="60" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="490" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">7:0.5</text>
  </g>

  <text x="40" y="125" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">리덕션 후 (5개 키프레임)</text>

  <g>
    <rect x="40" y="138" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="70" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">0:0.0</text>
    <rect x="100" y="138" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="130" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">1:0.1</text>
    <rect x="160" y="138" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="190" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">2:0.2</text>
    <rect x="220" y="138" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="250" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">3:0.3</text>
    <rect x="280" y="138" width="60" height="32" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
    <text x="310" y="158" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">7:0.5</text>
  </g>

  <text x="40" y="195" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">프레임 4, 5, 6은 보간으로 복원 가능 → 제거</text>

  <line x1="40" y1="215" x2="540" y2="215" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>

  <text x="40" y="240" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">직선 구간에서도 리덕션 가능</text>

  <text x="40" y="265" font-family="sans-serif" font-size="11" fill="currentColor">원본:</text>
  <text x="100" y="265" font-family="sans-serif" font-size="11" fill="currentColor">0:0.0   1:0.1   2:0.2   3:0.3</text>
  <text x="100" y="283" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 0에서 3까지 균일 증가</text>

  <text x="40" y="318" font-family="sans-serif" font-size="11" fill="currentColor">리덕션:</text>
  <text x="100" y="318" font-family="sans-serif" font-size="11" fill="currentColor">0:0.0   3:0.3</text>
  <text x="100" y="336" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">→ 선형 보간으로 중간값 복원 가능</text>
</svg>
</div>

<br>

키프레임 리덕션에서는 원본 커브와 리덕션 후 커브 사이의 허용 오차를 정합니다. 허용 오차를 크게 잡으면 더 많은 키프레임을 제거할 수 있어 데이터는 줄어들지만, 원본 움직임과의 차이가 커질 수 있습니다. 허용 오차를 작게 잡으면 원본에 더 가깝게 재생되지만, 제거되는 키프레임이 줄어 압축 효과도 작아집니다.

### Unity의 압축 모드

Unity에서는 모델의 Animation Import Settings에서 **Anim. Compression** 옵션을 설정할 수 있습니다. 이 옵션은 애니메이션 클립을 가져올 때 키프레임을 얼마나 줄이고, 어느 정도 오차를 허용할지를 결정합니다.

<br>

| 모드 | 동작 | 특징 |
|------|------|------|
| Off | 압축을 적용하지 않음 | 원본에 가장 가깝지만 데이터 크기가 큼 |
| Keyframe Reduction | 허용 오차 안에서 불필요한 키프레임 제거 | 데이터 크기와 움직임 품질의 균형을 직접 조정 |
| Optimal | Unity가 클립에 적합한 압축 방식을 선택 | 대체로 더 작은 데이터 크기를 목표로 하지만 결과 확인 필요 |

<br>

일반적으로는 **Optimal**을 먼저 적용해 보고, 재생 결과에 문제가 없는지 확인하는 방식이 적절합니다. 발이 미끄러지거나 손 위치가 어긋나는 것처럼 작은 오차가 눈에 띄는 클립은 Keyframe Reduction의 오차 값을 조정하거나, 필요한 경우 압축을 낮추는 방식으로 확인합니다.

### 정밀도와 오차 설정

Keyframe Reduction이나 Optimal 압축을 사용하면 Unity의 Import Settings에서 **Rotation Error**, **Position Error**, **Scale Error** 값을 조정할 수 있습니다. 이 값들은 압축 후 커브가 원본 커브에서 얼마나 벗어나도 되는지를 정하는 기준입니다.

허용 오차를 높이면 더 많은 키프레임이 제거되어 데이터 크기가 줄어들 수 있습니다. 대신 회전이 어긋나거나, 발이 바닥에서 미끄러지거나, 손이 무기나 소품 위치와 맞지 않는 문제가 생길 수 있습니다. 반대로 허용 오차를 낮추면 원본에 더 가까운 움직임을 유지하지만 압축 효과는 작아집니다.

오차 값은 모든 클립에 같은 기준으로 적용하기보다, 애니메이션의 용도에 맞춰 조정하는 편이 적절합니다. 카메라 가까이에서 보이는 캐릭터, 손발 접지가 중요한 동작, 무기나 도구를 잡는 동작은 보수적으로 설정하고, 멀리 있는 NPC나 배경 오브젝트의 반복 동작은 더 큰 오차를 허용할 수 있습니다.

### 불필요한 커브 제거

애니메이션 파일에는 실제 움직임에 기여하지 않는 커브가 포함될 수 있습니다. 3D 모델링 툴에서 익스포트하는 과정에서 값이 변하지 않는 프로퍼티까지 키프레임으로 기록되는 경우가 있기 때문입니다.

대표적인 예가 Scale 커브입니다. 대부분의 캐릭터 애니메이션에서는 본의 크기가 변하지 않지만, 모든 본에 `(1, 1, 1)` Scale 값이 프레임마다 기록될 수 있습니다. 값이 일정하다면 재생 결과에는 영향을 주지 않지만, 데이터에는 그대로 남습니다. 본 50개짜리 캐릭터에서 Scale x, y, z 세 커브가 150프레임 동안 기록되어 있다면 `50 × 3 × 150 = 22,500`개의 키프레임 값이 추가됩니다.

Unity의 Animation Import Settings에는 이런 경우를 줄이기 위한 **Remove Constant Scale Curves** 옵션이 있습니다. 이 옵션은 초기 Scale 값과 동일하게 유지되는 Scale 커브를 임포트 과정에서 제거합니다. Scale 외에도 값이 변하지 않는 Position이나 Rotation 커브가 있다면, 필요한 경우 `AssetPostprocessor.OnPostprocessAnimation`과 `AnimationUtility`를 사용해 프로젝트 규칙에 맞게 커브를 정리할 수 있습니다.

---

## Generic vs Humanoid 리그

앞에서 다룬 압축과 커브 제거는 애니메이션 클립에 저장된 데이터 자체를 줄이는 방법이었습니다. 하지만 같은 클립을 재생하더라도, Unity가 캐릭터의 본 구조를 어떻게 해석하느냐에 따라 이후 처리 비용은 달라집니다.

이 차이를 만드는 설정이 **리그 타입(Rig Type)**입니다. 이 섹션에서는 먼저 Generic과 Humanoid가 본 구조를 처리하는 방식이 어떻게 다른지 살펴봅니다. 이어서 Humanoid에서 추가 비용이 발생하는 이유와, 리타겟팅·IK 같은 Humanoid 전용 기능이 필요한 경우를 정리합니다. 마지막으로 캐릭터 종류와 애니메이션 재사용 방식에 따라 어떤 리그 타입을 선택할지 기준을 잡습니다.

### 리그 타입의 차이

리그 타입은 캐릭터 모델의 본 구조를 Unity가 어떤 방식으로 해석할지를 정하는 설정입니다. **Generic**은 모델에 들어 있는 본 계층을 그대로 사용하는 방식이고, **Humanoid**는 본 계층을 Unity의 표준 인체 구조인 Avatar에 매핑하는 방식입니다.

두 방식은 같은 애니메이션 클립을 재생하더라도 처리 과정이 다릅니다. Generic은 원본 본 Transform을 비교적 직접적으로 적용하지만, Humanoid는 Avatar 매핑, Muscle 시스템, 리타겟팅 같은 추가 단계를 거칠 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 530" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Generic vs Humanoid 리그 — 처리 요소 비교</text>

  <text x="40" y="52" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Generic 리그</text>
  <text x="40" y="70" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">모델의 본 계층을 기준으로 애니메이션 적용</text>

  <rect x="40" y="82" width="520" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="106" font-family="sans-serif" font-size="11" fill="currentColor">클립에서 각 본의 로컬 Transform 샘플링</text>

  <rect x="40" y="128" width="520" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="152" font-family="sans-serif" font-size="11" fill="currentColor">모델 본 계층에 Transform 적용</text>

  <line x1="40" y1="190" x2="560" y2="190" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>

  <text x="40" y="215" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Humanoid 리그</text>
  <text x="40" y="233" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">본 구조를 Unity의 표준 인체 모델(Avatar)에 연결</text>
  <text x="40" y="251" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">모델 본 구조 ↔ Avatar 표준 인체 구조</text>

  <rect x="40" y="263" width="520" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="285" font-family="sans-serif" font-size="11" fill="currentColor">클립에서 애니메이션 값 샘플링</text>

  <rect x="40" y="303" width="520" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="325" font-family="sans-serif" font-size="11" fill="currentColor">Avatar 매핑을 통해 표준 인체 구조와 연결</text>

  <rect x="40" y="343" width="520" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="365" font-family="sans-serif" font-size="11" fill="currentColor">Muscle 시스템 기반 관절 보정 가능</text>

  <rect x="40" y="383" width="520" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="405" font-family="sans-serif" font-size="11" fill="currentColor">IK(Inverse Kinematics) 처리 가능 (활성화 시)</text>

  <rect x="40" y="423" width="520" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="445" font-family="sans-serif" font-size="11" fill="currentColor">리타겟팅 처리 가능 (클립 공유 시)</text>

  <rect x="40" y="463" width="520" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="485" font-family="sans-serif" font-size="11" fill="currentColor">최종 본 Transform 적용</text>

  <text x="300" y="518" text-anchor="middle" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">강조된 항목은 Humanoid에서 비용이 추가될 수 있는 처리 요소</text>
</svg>
</div>

<br>

### Humanoid의 추가 비용

Humanoid 리그의 추가 비용은 Avatar 기반 처리를 유지하기 위한 계산에서 발생합니다. Unity는 애니메이션 값을 Humanoid의 표준 인체 표현에 맞게 해석하고, 필요한 경우 관절 범위 보정, 리타겟팅, IK 결과를 반영합니다.

이 과정에서 사용되는 대표적인 개념이 **Muscle 시스템**입니다. Humanoid는 관절 회전을 단순한 본 회전값으로만 다루지 않고, 인체 관절의 움직임 범위에 맞춘 Muscle 값으로 해석합니다. 이 표현을 사용하면 서로 다른 체형의 캐릭터 사이에서 애니메이션을 공유하거나, 관절이 지나치게 꺾이는 움직임을 보정하기 쉽습니다.

대신 매 프레임 추가 계산이 필요합니다. 애니메이션에서 얻은 값을 Avatar와 Muscle 표현에 맞게 해석하고, 필요한 경우 관절 범위 안으로 보정하며, 리타겟팅이나 IK를 사용한다면 그 결과까지 반영해야 합니다.

따라서 Humanoid의 비용은 단순히 본 수만의 문제가 아닙니다. 리타겟팅, Muscle 기반 보정, IK 같은 기능을 활용할수록 Generic보다 더 많은 CPU 작업이 발생할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Humanoid 리그의 추가 처리 요소</text>

  <rect x="40" y="42" width="520" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="64" font-family="sans-serif" font-size="11" fill="currentColor">Avatar: 모델의 본 구조를 표준 인체 구조와 연결</text>
  <text x="60" y="86" font-family="sans-serif" font-size="11" fill="currentColor">Muscle: 관절 움직임을 인체 기준의 값으로 표현</text>

  <text x="40" y="128" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Generic보다 비용이 추가될 수 있는 요소</text>

  <rect x="40" y="142" width="250" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="166" font-family="sans-serif" font-size="11" fill="currentColor">Avatar 표준 인체 구조와 매핑</text>

  <rect x="310" y="142" width="250" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="330" y="166" font-family="sans-serif" font-size="11" fill="currentColor">Muscle 값 기반 관절 표현</text>

  <rect x="40" y="186" width="250" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="210" font-family="sans-serif" font-size="11" fill="currentColor">관절 범위 보정 가능</text>

  <rect x="310" y="186" width="250" height="40" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="330" y="210" font-family="sans-serif" font-size="11" fill="currentColor">리타겟팅·IK 처리 가능</text>

  <line x1="40" y1="248" x2="560" y2="248" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>

  <text x="300" y="274" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">Humanoid는 Avatar, Muscle, 리타겟팅, IK를 지원하기 위해 추가 처리가 발생할 수 있음</text>
</svg>
</div>

<br>

### Humanoid가 필요한 경우

Humanoid 리그를 선택하는 가장 큰 이유는 인간형 캐릭터 사이에서 애니메이션을 재사용하기 위해서입니다. Generic 리그는 모델의 본 계층을 기준으로 동작하므로, 본 이름이나 계층 구조가 다른 캐릭터에 같은 클립을 그대로 적용하기 어렵습니다. 반면 Humanoid 리그는 각 캐릭터를 Avatar에 매핑해 공통의 인간형 구조로 다루므로, 서로 다른 체형의 캐릭터가 같은 Humanoid 클립을 공유할 수 있습니다.

**리타겟팅(Retargeting)**은 한 인간형 캐릭터용 애니메이션을 다른 인간형 캐릭터에 적용하는 기능입니다. 키, 팔 길이, 어깨 너비가 다른 캐릭터라도 Avatar 매핑이 올바르게 되어 있으면 같은 걷기, 달리기, 공격 클립을 재사용할 수 있습니다. 플레이어가 여러 캐릭터 모델을 선택할 수 있는 게임이나, 하나의 애니메이션 세트로 여러 NPC를 처리해야 하는 경우에 유용합니다.

**IK(Inverse Kinematics)**도 Humanoid를 선택하는 이유가 될 수 있습니다. 일반적인 애니메이션은 부모 본에서 자식 본으로 움직임이 전달되지만, IK는 손이나 발의 목표 위치를 먼저 정하고 그 위치에 맞도록 팔꿈치, 무릎, 어깨 같은 관절을 조정합니다. 경사면에서 발을 바닥에 맞추는 Foot IK나, 손을 문 손잡이에 맞추는 Hand IK가 대표적인 예입니다. Unity의 내장 Animator IK(`OnAnimatorIK`)는 Humanoid Avatar의 표준 관절 정보를 사용하므로 Humanoid 리그에서 동작합니다.

이런 기능이 필요하다면 Humanoid의 추가 비용은 기능을 얻기 위한 비용으로 볼 수 있습니다. 반대로 리타겟팅이나 내장 IK를 사용하지 않고, 캐릭터마다 전용 클립을 재생하기만 한다면 Generic 리그가 더 단순한 선택이 될 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">리그 타입 선택 기준</text>

  <rect x="185" y="44" width="230" height="44" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">여러 인간형 캐릭터가</text>
  <text x="300" y="78" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">같은 클립을 공유해야 하는가?</text>

  <line x1="250" y1="88" x2="140" y2="124" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="138,118 134,128 145,127" fill="currentColor"/>
  <text x="176" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예</text>

  <line x1="350" y1="88" x2="460" y2="124" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="455,127 466,128 462,118" fill="currentColor"/>
  <text x="424" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">아니오</text>

  <rect x="60" y="126" width="160" height="48" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="146" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Humanoid</text>
  <text x="140" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">리타겟팅 활용</text>

  <rect x="365" y="126" width="190" height="48" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="146" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Unity 내장 Animator IK를</text>
  <text x="460" y="162" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">사용해야 하는가?</text>

  <line x1="420" y1="174" x2="300" y2="212" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="298,206 295,216 305,214" fill="currentColor"/>
  <text x="345" y="196" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예</text>

  <line x1="500" y1="174" x2="500" y2="212" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="495,208 500,218 505,208" fill="currentColor"/>
  <text x="520" y="196" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">아니오</text>

  <rect x="220" y="218" width="160" height="48" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="238" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Humanoid</text>
  <text x="300" y="254" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">내장 IK 활용</text>

  <rect x="420" y="218" width="160" height="48" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="500" y="238" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Generic</text>
  <text x="500" y="254" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">전용 클립 재생</text>

  <text x="300" y="314" text-anchor="middle" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">리타겟팅이나 Unity 내장 Animator IK가 필요 없다면 Generic부터 검토</text>
</svg>
</div>

<br>

**리그 선택 예시**

| 상황 | 우선 검토할 리그 | 판단 기준 |
|------|------|------|
| 여러 인간형 캐릭터가 같은 클립을 공유해야 함 | Humanoid | Avatar 매핑을 통한 리타겟팅이 필요 |
| Foot IK, Hand IK 등 Unity 내장 Animator IK를 사용함 | Humanoid | Humanoid Avatar의 표준 관절 정보가 필요 |
| 전용 클립만 재생하는 인간형 캐릭터 | Generic | 리타겟팅이나 내장 IK가 없다면 Humanoid의 이점이 작음 |
| 모델별 고유 동작을 가진 NPC나 몬스터 | Generic | 각 모델에 맞춘 전용 클립을 사용 |
| 동물, 기계, 비인간형 보스 | Generic | Humanoid Avatar로 매핑할 대상이 아님 |
| 인간형 몬스터 종류가 많고 클립을 공유해야 함 | 상황에 따라 판단 | 클립 재사용 이점과 Humanoid 평가 비용을 비교 |

<br>

정리하면 Humanoid는 인간형 캐릭터 사이의 클립 재사용이나 Unity 내장 Animator IK가 필요할 때 선택할 이유가 분명합니다. 반대로 캐릭터마다 전용 클립을 사용하고 Humanoid 전용 기능을 쓰지 않는다면, Generic 리그부터 검토하는 편이 적절합니다. 캐릭터 수가 많을수록 이 차이는 프레임 예산에 더 크게 누적됩니다.

---

## Animation Culling 모드

리그 타입을 조정해도, 애니메이션을 평가해야 하는 캐릭터 수가 많으면 비용은 계속 누적됩니다. 특히 화면에 보이지 않는 캐릭터까지 같은 방식으로 평가하면, 플레이어가 볼 수 없는 움직임에 CPU 시간을 쓰게 됩니다.

캐릭터가 카메라 밖에 있어 렌더링되지 않더라도, Animator는 설정에 따라 상태 머신을 평가하고 본 Transform을 갱신할 수 있습니다. 이런 비용을 줄이기 위해 Unity는 Animator의 **Culling Mode**를 제공합니다. Culling Mode는 화면 밖 캐릭터의 애니메이션 평가를 계속할지, 일부만 처리할지, 완전히 멈출지를 정하는 설정입니다.

### 화면 밖 애니메이션의 비용

Animator의 Culling Mode는 캐릭터가 카메라 밖에 있을 때 애니메이션 평가를 어느 단계까지 유지할지 정합니다. 화면 안에서는 세 모드가 모두 정상적으로 애니메이션을 처리하지만, 화면 밖에서는 생략하는 작업의 범위가 달라집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 470" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">Animator Culling Mode</text>

  <rect x="40" y="42" width="540" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">화면 안: 세 모드 모두 동일</text>
  <text x="60" y="80" font-family="sans-serif" font-size="11" fill="currentColor">애니메이션 평가 + Transform 적용 + 렌더링</text>

  <text x="40" y="115" font-family="sans-serif" font-size="12" font-weight="bold" font-style="italic" fill="currentColor">차이는 화면 밖 동작에서 발생</text>

  <rect x="40" y="128" width="540" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="150" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Always Animate</text>
  <text x="60" y="170" font-family="sans-serif" font-size="11" fill="currentColor">화면 밖에서도 전체 애니메이션 평가 유지</text>
  <text x="60" y="190" font-family="sans-serif" font-size="11" fill="currentColor">절약: 없음</text>
  <text x="60" y="210" font-family="sans-serif" font-size="11" fill="currentColor">복귀: 시간 흐름이 유지된 상태로 이어짐</text>

  <rect x="40" y="240" width="540" height="118" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="262" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Cull Update Transforms</text>
  <text x="60" y="282" font-family="sans-serif" font-size="11" fill="currentColor">상태 머신과 Root Motion은 계속 평가</text>
  <text x="60" y="300" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">(루트 모션: 애니메이션이 캐릭터 위치를 직접 이동시키는 기능)</text>
  <text x="60" y="320" font-family="sans-serif" font-size="11" fill="currentColor">생략: 리타겟팅, IK, Transform 쓰기</text>
  <text x="60" y="340" font-family="sans-serif" font-size="11" fill="currentColor">복귀: Transform 갱신이 재개되며 포즈가 튈 수 있음</text>

  <rect x="40" y="370" width="540" height="92" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="392" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Cull Completely</text>
  <text x="60" y="412" font-family="sans-serif" font-size="11" fill="currentColor">화면 밖에서는 애니메이션 평가 중지</text>
  <text x="60" y="432" font-family="sans-serif" font-size="11" fill="currentColor">절약: Animator 평가 비용 제거</text>
  <text x="60" y="452" font-family="sans-serif" font-size="11" fill="currentColor">복귀: 다시 보일 때 애니메이션 평가 재개</text>
</svg>
</div>

<br>

### 모드 선택 기준

모드 선택은 화면 밖에서도 유지해야 하는 정보가 무엇인지에 따라 달라집니다. 일반 NPC, 군중 캐릭터, 배경 몬스터처럼 보이지 않는 동안의 포즈나 애니메이션 진행이 게임 로직에 영향을 주지 않는 대상은 `Cull Completely`부터 검토하는 편이 적절합니다. 반대로 상태 진행, Root Motion, Animation Event, IK 결과가 화면 밖에서도 필요하다면 더 보수적인 모드를 선택해야 합니다.

`Cull Update Transforms`는 중간 선택지입니다. 화면 밖에서도 상태 머신과 Root Motion은 계속 평가하지만, 리타겟팅, IK, Transform 쓰기는 생략합니다. 따라서 상태 진행은 유지해야 하지만 보이지 않는 동안 본 포즈를 갱신할 필요는 없는 캐릭터에 사용할 수 있습니다.

`Always Animate`는 화면 밖에서도 애니메이션 결과가 계속 필요할 때만 검토합니다. 예를 들어 Animation Event가 게임 로직을 호출하거나, 화면 밖 캐릭터의 포즈와 IK 결과가 다른 시스템에 영향을 준다면 애니메이션 평가를 멈출 수 없습니다. 이런 경우가 아니라면 화면 밖 캐릭터에 Always Animate를 유지할 이유는 크지 않습니다.

<br>

| 모드 | 선택 기준 |
|------|-------------|
| Cull Completely | 화면 밖에서는 애니메이션 상태를 유지할 필요가 없는 캐릭터 |
| Cull Update Transforms | 상태 머신과 Root Motion은 유지해야 하지만, 보이지 않는 동안 본 포즈 갱신은 생략해도 되는 캐릭터 |
| Always Animate | 화면 밖에서도 Animation Event, IK, 본 Transform 갱신이 계속 필요한 캐릭터 |

<br>

실제 절감량은 캐릭터 수, Animator Controller의 복잡도, 리그 타입, 활성화된 레이어와 블렌드 트리에 따라 달라집니다. 따라서 Culling Mode를 바꾼 뒤에는 Profiler에서 화면 밖 캐릭터가 많은 장면을 기준으로 Animator 평가 시간이 줄어드는지 확인해야 합니다.

---

## GPU Skinning vs CPU Skinning

지금까지는 Animator가 어떤 클립을 평가하고, 어떤 리그 타입으로 본(Bone)의 포즈를 계산하며, 화면 밖 캐릭터를 어디까지 갱신할지 살펴봤습니다. 하지만 본의 포즈가 계산되어도 플레이어가 보는 캐릭터 메쉬가 자동으로 변형되는 것은 아닙니다.

계산된 본 Transform을 실제 메쉬 정점에 반영하는 단계가 따로 필요합니다. 이 단계를 **스키닝(Skinning)**이라고 하며, Unity에서는 이 작업을 CPU에서 처리할지 GPU에서 처리할지 선택할 수 있습니다.

### 스키닝이란

본은 캐릭터의 움직임을 정의하는 뼈대이고, 메쉬는 플레이어가 실제로 보는 표면입니다. 스키닝은 이 둘을 연결하는 과정입니다. 각 정점은 하나 이상의 본에 연결되어 있고, 본마다 얼마나 영향을 받을지 가중치를 가지고 있습니다.

예를 들어 팔꿈치 근처의 정점은 상완본과 전완본의 영향을 함께 받을 수 있습니다. 팔이 구부러지면 두 본의 현재 Transform을 가중치에 따라 섞어 그 정점의 최종 위치를 계산합니다. 이 계산이 메쉬의 모든 정점에 대해 반복되므로, 정점 수가 많고 정점 하나에 연결된 본이 많을수록 스키닝 비용도 커집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 390" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">스키닝 계산 흐름</text>

  <rect x="34" y="52" width="160" height="82" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="114" y="74" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">현재 본 포즈</text>
  <text x="54" y="98" font-family="sans-serif" font-size="11" fill="currentColor">상완본 Transform</text>
  <text x="54" y="116" font-family="sans-serif" font-size="11" fill="currentColor">전완본 Transform</text>

  <rect x="230" y="52" width="160" height="82" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="310" y="74" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 P의 가중치</text>
  <text x="250" y="98" font-family="sans-serif" font-size="11" fill="currentColor">상완본 0.6</text>
  <text x="250" y="116" font-family="sans-serif" font-size="11" fill="currentColor">전완본 0.4</text>

  <rect x="426" y="52" width="160" height="82" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="506" y="74" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">원본 정점 위치</text>
  <text x="446" y="100" font-family="sans-serif" font-size="11" fill="currentColor">바인드 포즈 기준</text>
  <text x="446" y="118" font-family="sans-serif" font-size="11" fill="currentColor">메쉬 안의 정점 P</text>

  <line x1="114" y1="134" x2="250" y2="176" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="246,170 256,178 244,180" fill="currentColor"/>
  <line x1="310" y1="134" x2="310" y2="174" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="305,170 310,180 315,170" fill="currentColor"/>
  <line x1="506" y1="134" x2="370" y2="176" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="376,180 364,178 374,170" fill="currentColor"/>

  <rect x="170" y="180" width="280" height="72" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.4"/>
  <text x="310" y="204" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">스키닝</text>
  <text x="190" y="226" font-family="sans-serif" font-size="11" fill="currentColor">본별 변형 결과를 가중치만큼 섞음</text>
  <text x="190" y="242" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">상완본 결과 60% + 전완본 결과 40%</text>

  <line x1="310" y1="252" x2="310" y2="292" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="305,288 310,298 315,288" fill="currentColor"/>

  <rect x="210" y="298" width="200" height="52" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="310" y="320" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">변형된 정점 P'</text>
  <text x="310" y="338" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">현재 포즈에 맞는 메쉬 위치</text>

  <text x="310" y="374" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">이 계산이 메쉬의 모든 정점에 반복되므로, 비용은 정점 수와 정점당 본 영향 수에 비례</text>
</svg>
</div>

<br>

### CPU Skinning vs GPU Skinning

CPU Skinning과 GPU Skinning의 차이는 정점 변형 계산을 어느 쪽에서 처리하느냐입니다. CPU Skinning은 CPU가 본 Transform과 정점 가중치를 이용해 변형된 정점 위치를 계산합니다. 이 방식은 GPU에 스키닝 계산을 맡기지 않지만, 캐릭터 수와 정점 수가 늘어날수록 CPU 시간이 증가합니다.

GPU Skinning은 같은 계산을 GPU에서 처리합니다. CPU는 본 행렬이나 스키닝에 필요한 데이터를 준비하고, 실제 정점 변형은 GPU의 정점 처리 단계나 GPU 스키닝 경로에서 수행됩니다. 각 정점의 스키닝 계산은 다른 정점과 독립적으로 처리할 수 있으므로, 여러 정점을 동시에 계산하는 GPU의 구조와 잘 맞습니다.

다만 GPU Skinning이 항상 더 빠른 것은 아닙니다. CPU 병목이 있는 장면에서는 CPU 시간을 줄이는 데 도움이 되지만, 이미 GPU가 바쁜 장면에서는 정점 변형 작업까지 GPU에 추가되어 오히려 프레임 시간이 나빠질 수 있습니다. 따라서 스키닝을 어디에서 처리할지는 현재 병목이 CPU 쪽인지 GPU 쪽인지에 따라 결정해야 합니다.

두 방식의 차이를 단순화하면 다음과 같습니다.

<br>

| 항목 | CPU Skinning | GPU Skinning |
|------|--------------|--------------|
| 정점 변형 계산 | CPU에서 수행 | GPU에서 수행 |
| CPU 영향 | 정점 수와 캐릭터 수가 늘수록 CPU 시간이 증가 | CPU의 스키닝 부담을 줄일 수 있음 |
| GPU 영향 | GPU에는 스키닝 계산이 추가되지 않음 | GPU에 정점 변형 작업이 추가됨 |
| 적합한 상황 | GPU 여유가 적거나 캐릭터 수가 적은 장면 | CPU 병목이 있고 GPU 여유가 있는 장면 |
| 주의할 점 | 많은 캐릭터가 동시에 등장하면 CPU 비용이 누적됨 | GPU 병목 상황에서는 프레임 시간이 늘 수 있음 |
| 확인 항목 | CPU의 Animator·Skinning 시간 | GPU 시간과 플랫폼 지원 여부 |

<br>

### 성능 예산이 제한된 환경에서의 선택

스키닝 처리 위치는 현재 병목을 기준으로 정해야 합니다. CPU 프레임 시간이 길고 애니메이션이나 스키닝 비용이 눈에 띄는 장면이라면, GPU Skinning으로 CPU 부담을 줄일 여지가 있습니다. 반대로 GPU 시간이 이미 프레임 예산에 가깝다면, 스키닝 작업을 GPU로 옮기는 것이 오히려 부담이 될 수 있습니다.

따라서 캐릭터 수만으로 CPU Skinning과 GPU Skinning을 결정하기는 어렵습니다. 캐릭터의 정점 수, Skin Weights, 화면에 동시에 보이는 캐릭터 수, 렌더링 부하가 함께 영향을 줍니다. Unity Profiler와 실제 기기 측정으로 CPU 시간과 GPU 시간을 비교한 뒤, 병목이 줄어드는 쪽을 선택하는 편이 적절합니다.

### 정점 수와 본 가중치

스키닝 비용은 메쉬 정점 수와 정점마다 사용하는 본 영향 수에 따라 커집니다. 정점 하나가 본 하나에만 영향을 받으면 한 본의 Transform만 반영하면 되지만, 네 개의 본에 영향을 받는다면 네 본의 결과를 계산한 뒤 가중치에 따라 합산해야 합니다.

Unity의 **Skin Weights** 설정은 스키닝 계산에 사용할 본 영향 수의 상한을 정합니다. 메쉬 파일에 더 많은 본 가중치가 들어 있더라도, 이 설정이 낮으면 Unity는 런타임 스키닝에서 그중 일부만 사용합니다.

<br>

**본 가중치 수에 따른 비용** (Quality Settings &gt; Skin Weights)

| 설정 | 계산에 사용하는 본 영향 수 | 특징 |
|------|----------------------------|------|
| 1 Bone | 정점당 최대 1개 | 가장 가볍지만 관절 변형이 거칠어질 수 있음 |
| 2 Bones | 정점당 최대 2개 | 원거리 캐릭터나 단순한 모델에서 검토 가능 |
| 4 Bones | 정점당 최대 4개 | 일반적인 캐릭터 변형에서 품질과 비용의 균형을 잡기 쉬움 |
| Unlimited | 메쉬가 가진 본 가중치를 더 많이 사용 | 복잡한 변형에는 유리하지만 비용 확인 필요 |

Skin Weights를 낮추면 정점 하나를 계산할 때 참조하는 본 수가 줄어들어 스키닝 비용도 줄어듭니다. 대신 여러 본의 영향을 부드럽게 섞어야 하는 부위에서는 메쉬가 딱딱하게 접히거나, 관절 주변이 어색하게 찌그러질 수 있습니다. 특히 팔꿈치, 무릎, 어깨, 손가락처럼 움직임이 큰 관절에서 차이가 눈에 띄기 쉽습니다.

따라서 모든 캐릭터에 같은 값을 적용하기보다 화면 크기와 중요도에 따라 판단하는 편이 적절합니다. 플레이어 캐릭터나 클로즈업되는 캐릭터는 4 Bones 이상이 필요할 수 있고, 원거리 NPC나 단순한 몬스터는 2 Bones로도 충분할 수 있습니다. 낮은 Skin Weights가 적절한지는 실제 게임 카메라에서 관절 주변의 접힘이나 찌그러짐이 얼마나 눈에 띄는지에 따라 달라집니다.

---

## 마무리

- 애니메이션 비용은 본 Transform을 계산하는 **애니메이션 평가** 단계와, 계산된 Transform을 메쉬 정점에 반영하는 **스키닝** 단계로 나뉩니다.
- 상태 전환과 블렌딩이 필요 없는 UI나 환경 오브젝트는 Animator보다 트위닝 라이브러리나 스크립트 제어가 단순할 수 있습니다.
- 애니메이션 압축과 상수 커브 제거는 클립 데이터 크기를 줄여 메모리 사용량과 샘플링 부담을 낮춥니다.
- Humanoid 리그는 리타겟팅과 Unity 내장 Animator IK가 필요할 때 의미가 큽니다. 이런 기능이 없다면 Generic 리그부터 검토하는 편이 적절합니다.
- Animation Culling Mode는 화면 밖 캐릭터의 애니메이션 평가 범위를 줄이는 설정입니다. 화면 밖에서도 상태, 이벤트, IK 결과가 필요한지에 따라 모드를 선택합니다.
- 스키닝 비용은 메쉬 정점 수와 Skin Weights의 영향을 받습니다. Skin Weights를 낮추면 비용은 줄 수 있지만 관절 변형 품질도 함께 확인해야 합니다.
- GPU Skinning은 스키닝 계산을 GPU로 옮겨 CPU 부담을 줄일 수 있지만, GPU 병목 상황에서는 오히려 부담이 될 수 있습니다.

<br>

파티클과 애니메이션 최적화의 공통점은 비용이 한 지점에만 모이지 않는다는 점입니다. 파티클은 생성 수, 모듈, Culling, 오버드로우가 함께 작용하고, 애니메이션은 상태 평가, 클립 데이터, 리그 타입, Culling, 스키닝이 함께 비용을 만듭니다.

따라서 최적화 항목을 많이 아는 것보다, 실제 프로젝트에서 어떤 항목이 프레임 시간을 쓰고 있는지 확인하는 과정이 중요합니다. 이어지는 [프로파일링](/dev/unity/Profiling-1/) 시리즈에서는 Unity Profiler를 비롯한 도구로 CPU와 GPU 시간을 읽고, 병목 위치에 맞춰 최적화 우선순위를 정하는 방법을 다룹니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)

**시리즈**
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- **파티클과 애니메이션 (2) - 애니메이션 최적화** (현재 글)

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
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- **파티클과 애니메이션 (2) - 애니메이션 최적화** (현재 글)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
