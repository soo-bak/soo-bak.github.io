---
layout: single
title: "GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인 - soo:bak"
date: "2026-02-14 07:00:00 +0900"
description: CPU와 GPU의 아키텍처 차이, SIMD/SIMT 병렬 처리, 논리적 렌더링 파이프라인, IMR 방식을 설명합니다.
tags:
  - Unity
  - 최적화
  - GPU
  - 렌더링파이프라인
  - 모바일
---

## GPU가 필요해진 이유

[렌더링 기초](/dev/unity/RenderingFoundation-1/) 시리즈에서 메쉬, 텍스처, 머티리얼과 셰이더를 살펴보았습니다. 메쉬는 3D 오브젝트의 형태를 정의하고, 텍스처는 그 위에 입히는 이미지이며, 머티리얼은 텍스처와 셰이더를 묶어 오브젝트의 외형을 결정하는 단위였습니다.

이 중 셰이더는 **GPU에서 실행되는 프로그램**으로, 렌더링에서는 정점 변환이나 픽셀 색상 계산 등을 담당합니다. 머티리얼이 "이 오브젝트를 어떤 셰이더로 그려라"라고 지정하면, GPU가 해당 셰이더 코드를 수천 번 동시에 실행하여 화면에 픽셀을 채웁니다.

<br>

1990년대까지 3D 렌더링은 CPU가 전담했습니다. 정점 좌표를 변환하고, 삼각형을 래스터화하고, 픽셀 색상을 계산하는 작업을 CPU가 순차적으로 처리했습니다. 그러나 화면 해상도가 높아지고 3D 장면이 복잡해지면서, 수백만 개의 픽셀에 대해 같은 연산을 반복하는 작업이 CPU의 처리 능력을 초과하기 시작했습니다.

GPU는 이러한 대량 반복 연산을 처리하기 위해 설계된 프로세서입니다. CPU가 소수의 강력한 코어로 복잡한 작업을 빠르게 처리하는 데 집중한다면, GPU는 수천 개의 작은 코어로 같은 연산을 대량의 데이터에 동시에 적용하는 데 특화되어 있습니다.

<br>

셰이더의 성능은 GPU의 데이터 처리 방식에 직접 의존합니다. 셰이더에 분기문(if)을 넣었을 때 성능이 떨어지는 원인, 프래그먼트 셰이더가 버텍스 셰이더보다 병목이 되기 쉬운 구조적 이유 — 이런 현상은 모두 GPU 아키텍처에서 비롯됩니다.

이 글에서는 CPU와 GPU의 아키텍처 차이, GPU의 병렬 실행 모델(SIMD/SIMT), 논리적 렌더링 파이프라인, 그리고 데스크톱 GPU의 IMR(Immediate Mode Rendering) 방식을 다룹니다.

---

## CPU와 GPU: 설계 철학의 차이

CPU와 GPU는 모두 연산 장치이지만, 서로 다른 연산 패턴에 최적화되어 있습니다.

### CPU: 복잡한 작업을 빠르게

CPU는 소수의 강력한 코어로 구성됩니다. 데스크톱 CPU 기준으로 6~16개 정도이며, 각 코어는 독립적으로 복잡한 연산을 빠르게 처리할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- CPU 외곽 -->
  <rect x="1" y="1" width="518" height="338" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">CPU</text>

  <!-- 대용량 캐시 -->
  <rect x="20" y="36" width="480" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="55" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">대용량 캐시</text>
  <text x="260" y="72" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.6">L1 / L2 / L3 (수 MB ~ 수십 MB)</text>

  <!-- 코어 0 -->
  <rect x="20" y="96" width="180" height="210" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="116" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">코어 0</text>
  <!-- 제어 유닛 -->
  <rect x="38" y="126" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="147" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">제어 유닛</text>
  <!-- ALU -->
  <rect x="38" y="166" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="187" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">ALU</text>
  <!-- 분기 예측 -->
  <rect x="38" y="206" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="227" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">분기 예측</text>
  <!-- 비순서 실행 -->
  <rect x="38" y="246" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">비순서 실행</text>

  <!-- 코어 1 -->
  <rect x="220" y="96" width="180" height="210" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="116" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="12" font-weight="bold">코어 1</text>
  <!-- 제어 유닛 -->
  <rect x="238" y="126" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="147" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">제어 유닛</text>
  <!-- ALU -->
  <rect x="238" y="166" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="187" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">ALU</text>
  <!-- 분기 예측 -->
  <rect x="238" y="206" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="227" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">분기 예측</text>
  <!-- 비순서 실행 -->
  <rect x="238" y="246" width="144" height="32" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="310" y="267" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10">비순서 실행</text>

  <!-- ... 표시 -->
  <text x="430" y="200" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" opacity="0.5">...</text>

  <!-- (6 ~ 16개 코어) -->
  <text x="260" y="326" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">(6 ~ 16개 코어)</text>
</svg>
</div>

<br>

CPU 코어 하나의 내부에는 **연산 유닛(ALU, Arithmetic Logic Unit)** 외에도 제어 유닛, **분기 예측기(Branch Predictor)**, **비순서 실행(Out-of-Order Execution)** 장치, 그리고 다단계 캐시(L1/L2)가 들어 있습니다. L3 캐시는 여러 코어가 공유합니다. L1/L2/L3은 코어에 가까운 순서대로 번호를 매긴 캐시 메모리 계층(Level 1/2/3)입니다.

<br>

CPU는 하나의 명령어를 여러 단계(읽기, 해석, 실행, 저장)로 나누어 처리합니다. 이 구조를 **명령어 파이프라인**이라 합니다.

단계를 나누면, 한 명령어가 "실행" 단계에 있는 동안 다음 명령어를 "해석"하는 식으로 여러 명령어를 겹쳐서 진행할 수 있습니다. 
파이프라인이 끊기지 않고 흘러갈수록 단위 시간당 완료되는 명령어 수가 늘어납니다.

하지만 파이프라인이 항상 매끄럽게 흐르지는 않습니다. 분기(if문)를 만나면 조건 결과가 나올 때까지 다음 명령어를 넣을 수 없고, 앞 명령어의 결과를 기다려야 하는 명령어가 있으면 그 사이에 빈 틈이 생깁니다. 필요한 데이터가 캐시에 없는 경우에는 메인 메모리에서 가져오는 동안 수백 사이클을 대기하기도 합니다.
코어 내부의 장치들은 이런 멈춤을 줄이기 위해 존재합니다.

<br>

분기 예측기는 if문의 결과를 미리 추측하여, 조건 판정이 끝나기 전에 다음 명령어를 파이프라인에 넣어 둡니다. 추측이 맞으면 멈춤 없이 파이프라인이 계속 흐릅니다.

비순서 실행 장치는 앞 명령어의 결과를 기다리는 동안, 결과에 영향을 받지 않는 다른 명령어를 먼저 실행하여 빈 틈을 줄입니다.

다단계 캐시는 메인 메모리의 데이터를 코어 가까이에 복사해 두어, 메모리 접근 대기 시간을 줄입니다.

<br>

이 장치들은 모두 **레이턴시(latency, 하나의 작업을 완료하는 데 걸리는 시간)** 를 줄이기 위한 설계입니다.

### GPU: 같은 작업을 대량으로

CPU가 코어 하나의 레이턴시를 줄이는 데 트랜지스터를 투자했다면, GPU는 그 트랜지스터로 단순한 코어를 수천 개 배치합니다.
코어 하나의 성능 대신, 단위 시간당 처리하는 작업의 총량, 즉 **스루풋(throughput)** 을 높이는 설계입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- GPU 외곽 -->
  <rect x="1" y="1" width="538" height="298" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="22" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="13" font-weight="bold">GPU</text>

  <!-- SM 0 -->
  <rect x="20" y="36" width="105" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="72" y="54" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">SM 0</text>
  <!-- 코어 그리드 3x4 -->
  <rect x="32" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="44" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="60" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="72" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="88" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="100" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="32" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="44" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="60" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="72" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="88" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="100" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="32" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="44" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="60" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="72" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="88" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="100" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="32" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="44" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="60" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="72" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="88" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="100" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <text x="72" y="173" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(128+ 코어)</text>

  <!-- SM 1 -->
  <rect x="135" y="36" width="105" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="187" y="54" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">SM 1</text>
  <rect x="147" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="159" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="175" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="187" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="203" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="215" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="147" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="159" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="175" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="187" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="203" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="215" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="147" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="159" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="175" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="187" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="203" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="215" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="147" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="159" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="175" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="187" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="203" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="215" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <text x="187" y="173" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(128+ 코어)</text>

  <!-- SM 2 -->
  <rect x="250" y="36" width="105" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="302" y="54" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">SM 2</text>
  <rect x="262" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="274" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="290" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="302" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="318" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="330" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="262" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="274" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="290" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="302" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="318" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="330" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="262" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="274" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="290" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="302" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="318" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="330" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="262" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="274" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="290" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="302" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="318" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="330" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <text x="302" y="173" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(128+ 코어)</text>

  <!-- SM 3 -->
  <rect x="365" y="36" width="105" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="417" y="54" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">SM 3</text>
  <rect x="377" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="389" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="405" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="417" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="433" y="62" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="445" y="76" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="377" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="389" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="405" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="417" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="433" y="86" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="445" y="100" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="377" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="389" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="405" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="417" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="433" y="110" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="445" y="124" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="377" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="389" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="405" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="417" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <rect x="433" y="134" width="24" height="20" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="0.8"/>
  <text x="445" y="148" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="8">c</text>
  <text x="417" y="173" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="9" opacity="0.5">(128+ 코어)</text>

  <!-- ... 표시 -->
  <text x="497" y="130" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="18" opacity="0.5">...</text>

  <!-- 공유 메모리 / 캐시 -->
  <rect x="20" y="232" width="500" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="253" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="11" font-weight="bold">공유 메모리 / 캐시</text>
  <text x="270" y="270" text-anchor="middle" fill="currentColor" font-family="sans-serif" font-size="10" opacity="0.5">(CPU 대비 소용량)</text>
</svg>
</div>

<br>

GPU의 기본 단위는 **SM(Streaming Multiprocessor)** (NVIDIA 기준) 또는 **CU(Compute Unit)** (AMD 기준)입니다.
하나의 SM 안에 수십~128개의 작은 코어(**CUDA 코어**)가 있고, 이런 SM이 수십~백여 개 모여 전체적으로 수천 개의 코어를 구성합니다. SM의 개수는 GPU 모델마다 다르므로, 같은 작업이라도 SM이 많은 GPU에서 더 빠르게 처리될 수 있습니다.

개별 CUDA 코어는 CPU 코어와 비교하면 단순합니다.
앞에서 살펴본 분기 예측기도 없고, 비순서 실행 장치도 없으며, 캐시도 작습니다. GPU가 처리하는 작업에 이 장치들이 필요 없기 때문입니다.

예를 들어, 1920×1080 해상도의 화면에서 각 픽셀에 조명 계산을 적용한다고 하면, 약 200만 개의 픽셀이 모두 같은 셰이더 프로그램을 실행합니다. 픽셀마다 좌표와 법선 벡터 같은 입력 데이터만 다를 뿐, 연산 자체는 동일합니다. if문으로 분기할 일이 거의 없고, 명령어 순서를 바꿀 필요도 없습니다.

CPU에서 파이프라인 멈춤을 방지하던 장치들이 GPU에는 필요 없고, 그 트랜지스터 예산으로 더 많은 연산 유닛을 넣을 수 있습니다.

개별 코어의 레이턴시는 CPU보다 크지만, 수천 개의 코어가 동시에 작업하므로 전체 스루풋은 CPU보다 훨씬 높습니다.

### CPU와 GPU의 비유

CPU는 **교수 4명이 각자 복잡한 연구 과제를 순서대로 풀어가는 것**에 해당합니다. 각 교수는 논리적으로 복잡한 문제도 빠르게 해결할 수 있지만, 동시에 처리할 수 있는 과제의 수는 4개뿐입니다.

GPU는 **학생 4,000명이 같은 유형의 계산 문제를 동시에 풀어가는 것**에 해당합니다. 개별 학생이 풀 수 있는 문제의 복잡도는 제한적이지만, 같은 종류의 문제가 4,000개 있다면 모두 한꺼번에 끝낼 수 있습니다.

<br>

렌더링이 GPU에서 실행되는 이유도 여기에 있습니다. 정점 10만 개 각각에 **같은** 좌표 변환을, 픽셀 200만 개 각각에 **같은** 색상 계산을 적용해야 하는 작업이므로, 데이터만 다를 뿐 연산은 동일합니다.

**CPU vs GPU 설계 비교**

| 작업 특성 | CPU | GPU |
|-----------|:---:|:---:|
| 복잡한 분기 로직 | ◎ | △ |
| 순차 의존성이 높은 연산 | ◎ | △ |
| 동일 연산의 대량 반복 | △ | ◎ |
| **설계 목표** | **레이턴시** | **스루풋** |

◎ 강점 &nbsp; △ 약점

<br>

---

## SIMD와 SIMT: GPU의 병렬 실행 모델

GPU의 코어들이 같은 연산을 동시에 수행한다고 했지만, 각 코어가 독립적으로 명령어를 읽는 것은 아닙니다. GPU는 코어 여러 개를 하나의 그룹으로 묶고, 그룹 전체가 하나의 명령어를 공유합니다.

### SIMD: 하나의 명령어, 여러 데이터

하나의 명령어로 여러 데이터를 동시에 처리하는 이 방식을 **SIMD(Single Instruction, Multiple Data)** 라 합니다.

정점 4개의 x좌표를 각각 2배로 만드는 예시로 살펴봅니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- 제목 -->
  <text x="145" y="22" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SISD</text>
  <text x="145" y="37" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">명령 1개 → 데이터 1개</text>
  <text x="435" y="22" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SIMD</text>
  <text x="435" y="37" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">명령 1개 → 데이터 4개</text>

  <!-- 구분선 -->
  <line x1="290" y1="10" x2="290" y2="295" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- SISD: 4개의 명령이 순서대로 -->
  <!-- 명령 1 -->
  <rect x="30" y="55" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="74" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">× 2</text>
  <text x="108" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <rect x="125" y="55" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="155" y="74" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x0</text>

  <!-- 명령 2 -->
  <rect x="30" y="95" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="114" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">× 2</text>
  <text x="108" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <rect x="125" y="95" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="155" y="114" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x1</text>

  <!-- 명령 3 -->
  <rect x="30" y="135" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="154" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">× 2</text>
  <text x="108" y="154" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <rect x="125" y="135" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="155" y="154" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x2</text>

  <!-- 명령 4 -->
  <rect x="30" y="175" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="60" y="194" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">× 2</text>
  <text x="108" y="194" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <rect x="125" y="175" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="155" y="194" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x3</text>

  <!-- SISD 시간 축 -->
  <line x1="15" y1="55" x2="15" y2="205" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="12,203 15,210 18,203" fill="currentColor" opacity="0.4"/>
  <text x="15" y="225" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">시간</text>

  <!-- SISD 결론 -->
  <text x="145" y="260" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">명령 4회 실행</text>

  <!-- SIMD: 1개의 명령이 4개 데이터를 동시에 -->
  <rect x="320" y="55" width="60" height="150" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="350" y="134" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">× 2</text>

  <text x="398" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="398" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="398" y="154" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="398" y="194" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>

  <rect x="415" y="55" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="445" y="74" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x0</text>
  <rect x="415" y="95" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="445" y="114" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x1</text>
  <rect x="415" y="135" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="445" y="154" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x2</text>
  <rect x="415" y="175" width="60" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="445" y="194" text-anchor="middle" font-family="monospace" font-size="10" fill="currentColor">x3</text>

  <!-- SIMD 결론 -->
  <text x="435" y="260" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">명령 1회 실행</text>

  <!-- 범례 -->
  <rect x="175" y="280" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="0.8"/>
  <text x="194" y="289" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">명령어</text>
  <rect x="260" y="280" width="14" height="10" rx="2" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="0.8"/>
  <text x="279" y="289" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터</text>
</svg>
</div>

<br>

SIMD는 하나의 넓은 레지스터에 여러 데이터를 나란히 넣고, 하나의 명령으로 모든 데이터에 같은 연산을 적용하는 방식입니다.
CPU도 SIMD 명령어(SSE, AVX 등)를 지원하지만 기능의 일부인 반면, GPU는 아키텍처 전체가 이 방식 위에 구축되어 있습니다.

### SIMT: 하나의 명령어, 여러 스레드

SIMD는 프로그래머가 여러 값을 하나의 벡터(여러 스칼라를 묶은 데이터)로 만들고, 벡터 전용 명령어를 직접 사용해야 합니다.

GPU의 **SIMT(Single Instruction, Multiple Threads)** 는 다릅니다.
셰이더를 작성할 때는 정점 하나, 픽셀 하나의 처리만 작성합니다. GPU가 이 프로그램을 수천 개의 스레드에 자동으로 배분하여, 각 스레드가 서로 다른 정점이나 프래그먼트를 동시에 처리합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SIMT — 프로그래머는 하나만 작성, GPU가 복제</text>

  <!-- 왼쪽: 셰이더 코드 (프로그래머가 작성) -->
  <rect x="20" y="50" width="140" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="72" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">셰이더 코드</text>
  <text x="90" y="92" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">pos × MVP 행렬</text>
  <text x="90" y="108" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">노멀 변환</text>
  <text x="90" y="124" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor">UV 전달</text>
  <text x="90" y="145" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">정점 1개 기준으로 작성</text>

  <!-- 화살표: 코드 → GPU 복제 -->
  <line x1="160" y1="100" x2="200" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="198,100 192,96 192,104" fill="currentColor"/>
  <text x="180" y="88" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">GPU가</text>
  <text x="180" y="118" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">복제</text>

  <!-- 오른쪽: 스레드들 -->
  <!-- 명령어 유닛 -->
  <rect x="210" y="42" width="290" height="30" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="355" y="62" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">현재 명령어: pos × MVP 행렬</text>

  <!-- 브로드캐스트 화살표 -->
  <line x1="280" y1="72" x2="280" y2="92" stroke="currentColor" stroke-width="1"/>
  <polygon points="277,90 280,96 283,90" fill="currentColor"/>
  <line x1="340" y1="72" x2="340" y2="92" stroke="currentColor" stroke-width="1"/>
  <polygon points="337,90 340,96 343,90" fill="currentColor"/>
  <line x1="400" y1="72" x2="400" y2="92" stroke="currentColor" stroke-width="1"/>
  <polygon points="397,90 400,96 403,90" fill="currentColor"/>
  <line x1="460" y1="72" x2="460" y2="92" stroke="currentColor" stroke-width="1"/>
  <polygon points="457,90 460,96 463,90" fill="currentColor"/>

  <!-- 스레드 0 -->
  <rect x="220" y="98" width="120" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="280" y="116" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드 0</text>
  <text x="280" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 0의 pos로</text>
  <text x="280" y="150" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MVP 곱셈 실행</text>

  <!-- 스레드 1 -->
  <rect x="350" y="98" width="120" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="410" y="116" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드 1</text>
  <text x="410" y="134" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 1의 pos로</text>
  <text x="410" y="150" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MVP 곱셈 실행</text>

  <!-- ... 표시 -->
  <text x="355" y="188" text-anchor="middle" font-family="sans-serif" font-size="14" fill="currentColor" opacity="0.4">...</text>

  <!-- 스레드 31 -->
  <rect x="285" y="200" width="140" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="355" y="218" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">스레드 31</text>
  <text x="355" y="236" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 31의 pos로</text>
  <text x="355" y="252" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">MVP 곱셈 실행</text>

  <!-- 하단 설명 -->
  <text x="355" y="286" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">같은 명령어, 서로 다른 데이터 → 동시 실행</text>
</svg>
</div>

<br>

스레드가 수천 개에 달하므로, GPU는 이를 **Warp**(NVIDIA 용어) 또는 **Wavefront**(AMD 용어)라는 단위로 묶어 관리합니다.

NVIDIA GPU에서 하나의 Warp는 32개의 스레드로 구성되며, 이 크기는 모든 NVIDIA GPU에서 동일합니다.
AMD GPU에서는 Wavefront라 부르며, 아키텍처에 따라 32개 또는 64개입니다. 동작 원리는 같으므로, 앞으로는 Warp(32스레드)를 기준으로 살펴봅니다.

Warp 안의 32개 스레드는 **항상 같은 명령어를 같은 순간에 실행합니다**. 스레드 0이 "좌표에 MVP 행렬을 곱하는" 명령을 실행할 때, 같은 Warp에 속한 스레드 1~31도 동시에 같은 명령을 실행합니다.
다만 각 스레드가 참조하는 정점 데이터가 다를 뿐입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Warp 구성 — 스레드를 32개씩 묶어 관리</text>
  <!-- Warp 0 -->
  <rect x="15" y="45" width="185" height="170" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="107" y="68" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Warp 0</text>
  <line x1="25" y1="76" x2="190" y2="76" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="50" y="97" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 0</text>
  <text x="117" y="97" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="135" y="97" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 0</text>
  <text x="50" y="117" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 1</text>
  <text x="117" y="117" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="135" y="117" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 1</text>
  <text x="107" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">...</text>
  <text x="50" y="168" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 31</text>
  <text x="117" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="135" y="168" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 31</text>
  <!-- Warp 0 caption -->
  <text x="107" y="195" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">32개가 항상 같은</text>
  <text x="107" y="208" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">명령어를 동시에 실행</text>
  <!-- Warp 1 -->
  <rect x="218" y="45" width="185" height="170" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="68" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Warp 1</text>
  <line x1="228" y1="76" x2="393" y2="76" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="248" y="97" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 32</text>
  <text x="320" y="97" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="335" y="97" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 32</text>
  <text x="248" y="117" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 33</text>
  <text x="320" y="117" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="335" y="117" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 33</text>
  <text x="310" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">...</text>
  <text x="248" y="168" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 63</text>
  <text x="320" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="335" y="168" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 63</text>
  <!-- Warp 1 caption -->
  <text x="310" y="195" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">32개가 항상 같은</text>
  <text x="310" y="208" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">명령어를 동시에 실행</text>
  <!-- Warp 2 -->
  <rect x="421" y="45" width="185" height="170" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="513" y="68" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Warp 2</text>
  <line x1="431" y1="76" x2="596" y2="76" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="451" y="97" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 64</text>
  <text x="523" y="97" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="538" y="97" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 64</text>
  <text x="451" y="117" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 65</text>
  <text x="523" y="117" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="538" y="117" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 65</text>
  <text x="513" y="143" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">...</text>
  <text x="451" y="168" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">스레드 95</text>
  <text x="523" y="168" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="538" y="168" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">정점 95</text>
  <!-- Warp 2 caption -->
  <text x="513" y="195" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">32개가 항상 같은</text>
  <text x="513" y="208" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">명령어를 동시에 실행</text>
</svg>
</div>

<br>

정리하면, 프로그래머는 정점이나 프래그먼트 하나의 처리만 작성하고, GPU가 스레드를 Warp로 묶어 SIMD 하드웨어로 동시에 처리하는 구조입니다.

### 분기(if문)가 GPU에서 비용이 큰 이유

셰이더에 if문이 있으면, 조건을 판정하는 것 자체는 하나의 명령어이므로 32개 스레드가 동시에 수행합니다.
하지만 판정 결과는 스레드마다 다를 수 있습니다. 어떤 스레드는 true여서 `if` 블록을, 어떤 스레드는 false여서 `else` 블록을 실행해야 하는데, 각 블록 안의 코드는 곱셈, 덧셈 등 여러 개의 기계어 명령어로 컴파일되고, Warp는 한 번에 하나의 기계어 명령어만 실행할 수 있으므로 양쪽을 동시에 처리할 수 없습니다.

```hlsl
// 프래그먼트 셰이더 예시
if (brightness > 0.5)
{
    // 밝은 영역: 조명 계산 + 반사광
    color = baseColor * lightIntensity;
    color += specular * roughness;
}
else
{
    // 어두운 영역: 그림자 색상만 적용
    color = baseColor * shadowFactor;
}
```

Warp 안의 32개 스레드는 각자 다른 프래그먼트(화면의 픽셀 후보)를 담당하므로, 프래그먼트마다 밝기 값이 달라 같은 Warp 안에서 분기 방향이 갈라질 수 있습니다. 이 상황을 **분기 발산(divergent branch)** 이라 합니다.

분기 발산이 발생하면 Warp는 양쪽 경로를 한쪽씩 차례로 실행합니다.
`if` 블록의 명령어들을 실행하는 동안 `else`에 해당하는 스레드는 대기하고, `else` 블록을 실행하는 동안 `if`에 해당하는 스레드가 대기합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">분기 발산 시 실행 흐름</text>
  <!-- Thread state header -->
  <text x="280" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Warp 내 32개 스레드 상태:</text>
  <text x="280" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">스레드 0~19: brightness &gt; 0.5 → true (if 블록)</text>
  <text x="280" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">스레드 20~31: brightness &gt; 0.5 → false (else 블록)</text>

  <!-- Step 1: if 조건 평가 -->
  <rect x="40" y="100" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="121" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. if 조건 평가</text>
  <text x="55" y="139" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">32개 스레드 모두 실행</text>
  <!-- Active indicators for step 1 -->
  <rect x="380" y="110" width="60" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="121" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">0~19 활성</text>
  <rect x="445" y="110" width="65" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="477" y="121" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">20~31 활성</text>

  <!-- Arrow 1→2 -->
  <line x1="280" y1="150" x2="280" y2="170" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,168 280,178 285,168" fill="currentColor"/>

  <!-- Step 2: if 블록 실행 -->
  <rect x="40" y="180" width="480" height="90" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="201" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. if 블록 실행</text>
  <text x="55" y="219" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">color = baseColor * lightIntensity</text>
  <text x="55" y="235" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">color += specular * roughness</text>
  <!-- Active threads -->
  <rect x="380" y="196" width="60" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="207" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">0~19 활성</text>
  <text x="410" y="223" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">실행 → 결과 저장</text>
  <!-- Inactive threads -->
  <rect x="445" y="196" width="65" height="14" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="477" y="207" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.4">20~31 대기</text>
  <text x="477" y="223" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">아무 일도 하지 않음</text>

  <!-- Arrow 2→3 -->
  <line x1="280" y1="270" x2="280" y2="290" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,288 280,298 285,288" fill="currentColor"/>

  <!-- Step 3: else 블록 실행 -->
  <rect x="40" y="300" width="480" height="75" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="321" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. else 블록 실행</text>
  <text x="55" y="339" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">color = baseColor * shadowFactor</text>
  <!-- Inactive threads -->
  <rect x="380" y="316" width="60" height="14" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="410" y="327" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.4">0~19 대기</text>
  <text x="410" y="343" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">아무 일도 하지 않음</text>
  <!-- Active threads -->
  <rect x="445" y="316" width="65" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="477" y="327" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">20~31 활성</text>
  <text x="477" y="343" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">실행 → 결과 저장</text>

  <!-- Arrow 3→4 -->
  <line x1="280" y1="375" x2="280" y2="395" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="275,393 280,403 285,393" fill="currentColor"/>

  <!-- Step 4: 합류 -->
  <rect x="40" y="405" width="480" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="426" text-anchor="start" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4. 합류</text>
  <text x="55" y="444" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor">32개 스레드가 다시 같은 명령어를 실행</text>
  <!-- Active indicators for step 4 -->
  <rect x="380" y="416" width="60" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="410" y="427" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">0~19 활성</text>
  <rect x="445" y="416" width="65" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="477" y="427" text-anchor="middle" font-family="sans-serif" font-size="8" fill="currentColor">20~31 활성</text>

  <!-- Conclusion -->
  <text x="280" y="490" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">→ if와 else를 모두 실행하므로, 총 실행 시간 = if + else</text>
</svg>
</div>

<br>

발산이 없었다면 한쪽 경로만 실행하면 되지만, 발산이 일어나면 양쪽을 모두 실행해야 하므로 최악의 경우 실행 시간이 2배가 됩니다.

다만, 32개 스레드가 **모두 같은 방향으로 분기하면** 이 비용은 발생하지 않습니다. 전부 true라면 true 경로만, 전부 false라면 false 경로만 실행하면 되기 때문입니다. 비용이 발생하는 것은 **같은 Warp 안에서** 분기 방향이 갈리는 경우뿐입니다.

셰이더 최적화에서 "if문을 줄여라"라는 조언은 여기서 비롯됩니다. if문 자체가 해로운 것이 아니라, Warp 안에서 스레드들이 서로 다른 방향으로 갈라지는 if문이 실행 시간을 늘립니다.

---

## 논리적 렌더링 파이프라인

3D 장면을 화면의 2D 이미지로 만들기까지, 데이터는 CPU와 GPU에 걸친 정해진 단계들을 차례로 통과합니다. 각 단계가 이전 단계의 출력을 입력으로 받아 처리하는 이 흐름을 **렌더링 파이프라인**이라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 820" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더링 파이프라인 전체 흐름</text>

  <!-- 1. 정점 데이터 입력 -->
  <rect x="120" y="48" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="73" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 데이터 입력</text>
  <text x="340" y="73" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">정점 좌표, UV, 노멀 등</text>

  <!-- 화살표 1→2 -->
  <line x1="220" y1="88" x2="220" y2="138" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,134 220,146 226,134" fill="currentColor"/>
  <text x="234" y="118" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터: 정점</text>

  <!-- 2. 버텍스 셰이더 (프로그래밍 가능) -->
  <rect x="120" y="148" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="173" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">버텍스 셰이더</text>
  <text x="340" y="165" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">좌표 변환 (로컬 → 클립)</text>
  <text x="340" y="181" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">◀ 프로그래밍 가능</text>

  <!-- 화살표 2→3 -->
  <line x1="220" y1="188" x2="220" y2="238" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,234 220,246 226,234" fill="currentColor"/>
  <text x="234" y="218" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터: 변환된 정점</text>

  <!-- 3. 프리머티브 어셈블리 + 클리핑 (고정 기능) -->
  <rect x="120" y="248" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="269" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프리머티브 어셈블리</text>
  <text x="220" y="287" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">+ 클리핑</text>
  <text x="340" y="265" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">정점 → 삼각형 조립</text>
  <text x="340" y="281" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">화면 밖 삼각형 제거</text>
  <text x="340" y="297" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">◁ 고정 기능</text>

  <!-- 화살표 3→4 -->
  <line x1="220" y1="300" x2="220" y2="350" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,346 220,358 226,346" fill="currentColor"/>
  <text x="234" y="330" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터: 삼각형</text>

  <!-- 4. 래스터화 (고정 기능) -->
  <rect x="120" y="360" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="385" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">래스터화</text>
  <text x="340" y="377" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">삼각형 → 프래그먼트 변환</text>
  <text x="340" y="393" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">◁ 고정 기능</text>

  <!-- 화살표 4→5 -->
  <line x1="220" y1="400" x2="220" y2="450" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,446 220,458 226,446" fill="currentColor"/>
  <text x="234" y="430" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터: 프래그먼트 (수가 급증)</text>

  <!-- 5. 프래그먼트 셰이더 (프로그래밍 가능) -->
  <rect x="120" y="460" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="485" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프래그먼트 셰이더</text>
  <text x="340" y="477" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">최종 색상 계산</text>
  <text x="340" y="493" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">◀ 프로그래밍 가능</text>

  <!-- 화살표 5→6 -->
  <line x1="220" y1="500" x2="220" y2="550" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,546 220,558 226,546" fill="currentColor"/>
  <text x="234" y="530" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터: 색상 + 깊이</text>

  <!-- 6. 스텐실/깊이 테스트 + 블렌딩 (고정 기능) -->
  <rect x="120" y="560" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="581" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">스텐실/깊이 테스트</text>
  <text x="220" y="599" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">+ 블렌딩</text>
  <text x="340" y="577" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">가려진 프래그먼트 제거</text>
  <text x="340" y="593" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">반투명 합성</text>
  <text x="340" y="609" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">◁ 고정 기능</text>

  <!-- 화살표 6→7 -->
  <line x1="220" y1="612" x2="220" y2="662" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,658 220,670 226,658" fill="currentColor"/>
  <text x="234" y="642" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">데이터: 최종 픽셀</text>

  <!-- 7. 프레임버퍼 출력 -->
  <rect x="120" y="672" width="200" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="697" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프레임버퍼 출력</text>
  <text x="340" y="697" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">최종 이미지 → 화면 표시</text>

  <!-- 범례 -->
  <rect x="120" y="740" width="16" height="12" rx="3" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1"/>
  <text x="142" y="750" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프로그래밍 가능 단계</text>
  <rect x="310" y="740" width="16" height="12" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="332" y="750" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">고정 기능 단계</text>
</svg>
</div>

### 1단계: 정점 데이터 입력 (Vertex Input)

오브젝트 하나를 화면에 그리기까지, CPU는 세 단계에 걸쳐 GPU에 데이터와 명령을 전달합니다.

| 단계 | 시점 | 하는 일 |
|------|------|---------|
| 에셋 로딩 | 씬 로드 등 (렌더링 이전) | 메쉬·텍스처 데이터를 GPU 메모리(VRAM)에 업로드 |
| 상태 변경 | 머티리얼이 바뀔 때 | 셰이더 바인딩, 텍스처 바인딩, 렌더 스테이트(깊이 쓰기, 블렌드 모드 등) 설정 |
| 드로우 콜 | 오브젝트마다 | "현재 설정된 상태로, 이 메쉬를 그려라" |

GPU는 드로우 콜을 받으면 VRAM에서 메쉬의 정점 버퍼와 인덱스 버퍼를 읽어옵니다. 메쉬 데이터는 에셋 로딩 시점에 이미 업로드되어 있으므로, 드로우 콜 시점에는 GPU가 자신의 메모리에서 바로 읽습니다.

[렌더링 기초 (1)](/dev/unity/RenderingFoundation-1/)에서 다룬 것처럼, 정점 하나에는 위치(position), 텍스처 좌표(UV), 노멀(normal) 등의 속성(attribute)이 포함되어 있습니다.

GPU 메모리에는 이 정점들이 **정점 버퍼(Vertex Buffer)** 라는 연속된 배열로 저장되어 있습니다.

```
정점 버퍼 예시 (바닥 평면의 네 꼭짓점)

정점 0: 위치(-1.0, 0.0, -1.0)  UV(0.0, 0.0)  노멀(0.0, 1.0, 0.0)
정점 1: 위치( 1.0, 0.0, -1.0)  UV(1.0, 0.0)  노멀(0.0, 1.0, 0.0)
정점 2: 위치( 1.0, 0.0,  1.0)  UV(1.0, 1.0)  노멀(0.0, 1.0, 0.0)
정점 3: 위치(-1.0, 0.0,  1.0)  UV(0.0, 1.0)  노멀(0.0, 1.0, 0.0)
```

하지만 정점 버퍼에는 정점의 속성만 나열되어 있을 뿐, 어떤 정점들을 묶어 삼각형을 만들지는 기록되어 있지 않습니다.

위 네 정점으로 사각형을 만들려면 삼각형 두 개가 필요한데, 각 삼각형을 구성할 정점의 번호를 지정하는 것이 **인덱스 버퍼(Index Buffer)** 입니다.

인덱스 버퍼는 정점 데이터를 복사하지 않고 정점 버퍼의 번호만 참조하므로, [0, 1, 2]와 [0, 2, 3]처럼 같은 번호가 여러 삼각형에 등장해도 정점 데이터는 중복되지 않습니다.

### 2단계: 버텍스 셰이더 (Vertex Shader)

버텍스 셰이더는 **정점 하나당 하나의 스레드**가 실행됩니다.

메쉬에 정점이 10,000개 있으면 GPU는 스레드 10,000개를 생성하고, 앞서 살펴본 SIMT 모델에 따라 32개씩 Warp로 묶어 병렬 처리합니다. 10,000개가 동시에 실행되는 것은 아니고, 313개의 Warp(10,000 ÷ 32)가 GPU의 SM들에 분배되어 스케줄링됩니다.

<br>

각 스레드가 수행하는 핵심 작업은 **좌표 변환**입니다.

1단계에서 읽어온 정점 좌표는 메쉬 자체의 로컬 좌표계로 되어 있어서, 이 정점이 화면의 어디에 찍혀야 하는지 알 수 없습니다. 예를 들어 캐릭터 모델의 코 끝이 (0, 1.7, 0.1)이라면, 이는 캐릭터 모델 내부에서의 위치일 뿐입니다.

버텍스 셰이더가 이 로컬 좌표에 오브젝트의 위치와 회전, 카메라의 시점, 원근감을 차례로 반영하여 화면에 투영할 수 있는 좌표로 변환합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 480" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 제목 -->
  <text x="270" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">좌표 변환 과정</text>

  <!-- 1. 로컬 공간 -->
  <rect x="80" y="48" width="140" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="73" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">로컬 공간</text>
  <text x="240" y="63" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(0, 1.7, 0.1)</text>
  <text x="240" y="80" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">메쉬 내부 좌표</text>

  <!-- 화살표 1→2 + 변환 행렬 -->
  <line x1="150" y1="88" x2="150" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="144,154 150,166 156,154" fill="currentColor"/>
  <text x="164" y="128" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">× 모델 행렬</text>
  <text x="164" y="143" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">위치 · 회전 · 크기 반영</text>

  <!-- 2. 월드 공간 -->
  <rect x="80" y="168" width="140" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="193" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">월드 공간</text>
  <text x="240" y="183" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(10, 1.7, 5.1)</text>
  <text x="240" y="200" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">게임 세계 좌표</text>

  <!-- 화살표 2→3 + 변환 행렬 -->
  <line x1="150" y1="208" x2="150" y2="278" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="144,274 150,286 156,274" fill="currentColor"/>
  <text x="164" y="248" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">× 뷰 행렬</text>
  <text x="164" y="263" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">카메라 기준으로 좌표계 변환</text>

  <!-- 3. 카메라 공간 -->
  <rect x="80" y="288" width="140" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="313" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">카메라 공간</text>
  <text x="240" y="313" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">카메라를 원점에 놓고 본 좌표</text>

  <!-- 화살표 3→4 + 변환 행렬 -->
  <line x1="150" y1="328" x2="150" y2="398" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="144,394 150,406 156,394" fill="currentColor"/>
  <text x="164" y="368" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">× 프로젝션 행렬</text>
  <text x="164" y="383" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">원근감 적용</text>

  <!-- 4. 클립 공간 -->
  <rect x="80" y="408" width="140" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="433" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">클립 공간</text>
  <text x="240" y="423" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">화면 표시 범위 판정 좌표</text>
  <text x="240" y="440" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">범위 밖 → 클리핑에서 제거</text>
</svg>
</div>

<br>

위치 이동, 회전, 원근 적용 같은 3D 좌표 변환은 모두 4×4 행렬 곱셈으로 표현할 수 있습니다. 다이어그램의 "× 모델 행렬", "× 뷰 행렬", "× 프로젝션 행렬"이 각각 이 곱셈에 해당합니다.
세 행렬은 하나로 합칠 수 있으므로, 실제 버텍스 셰이더는 세 행렬을 합친 **MVP(Model-View-Projection) 행렬** 하나만 정점 좌표에 곱해 로컬 공간에서 클립 공간까지 한 번에 변환합니다.

좌표 변환이 핵심 역할이지만, 버텍스 셰이더는 프로그래밍 가능한 단계이므로 바람에 흔들리는 풀처럼 정점 위치를 직접 움직이거나, 정점 단위로 조명을 근사하는 등 다른 작업도 수행할 수 있습니다.

### 3단계: 프리머티브 어셈블리와 클리핑

버텍스 셰이더를 거친 정점들이 인덱스 버퍼에 따라 삼각형으로 조립됩니다. 렌더링의 기본 도형 단위를 **프리머티브(Primitive)** 라 하며, 대부분의 경우 삼각형입니다.

이어서 카메라의 시야 영역인 **뷰 프러스텀(View Frustum)** 을 기준으로 **클리핑(Clipping)** 이 수행됩니다.
완전히 시야 밖에 있는 삼각형은 버리고, 일부만 걸쳐 있는 삼각형은 시야 안의 부분만 남도록 잘라냅니다. 보이지 않는 삼각형이 이 단계에서 제거되므로, 이후 래스터화와 프래그먼트 셰이딩의 연산량이 줄어듭니다.

프리머티브 어셈블리와 클리핑은 모두 GPU 고정 기능 하드웨어가 수행하며, 셰이더로 제어할 수 없습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">클리핑 (위에서 본 시야)</text>

  <!-- 뷰 프러스텀 -->
  <polygon points="240,48 75,252 405,252" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="240" cy="48" r="3" fill="currentColor"/>
  <text x="240" y="40" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">카메라</text>
  <text x="415" y="248" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">뷰 프러스텀</text>

  <!-- 삼각형 A: 완전히 안 -->
  <polygon points="220,110 198,165 242,165" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="220" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">A</text>
  <text x="265" y="142" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">완전히 안 → 유지</text>

  <!-- 삼각형 B: 경계에 걸침 -->
  <polygon points="310,215 288,270 332,270" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="207" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">B</text>
  <line x1="293" y1="252" x2="327" y2="252" stroke="currentColor" stroke-width="1.5" stroke-dasharray="3,2" opacity="0.6"/>
  <text x="348" y="248" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">걸침 → 안쪽만 남김</text>
  <text x="348" y="261" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.45">(교차점에 새 정점 생성)</text>

  <!-- 삼각형 C: 완전히 밖 -->
  <polygon points="170,275 148,325 192,325" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="170" y="267" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">C</text>
  <text x="210" y="303" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">완전히 밖 → 제거</text>
</svg>
</div>

<br>

클리핑과 함께 **뒷면 제거(Back-face Culling)** 도 수행됩니다.

[렌더링 기초 (3)](/dev/unity/RenderingFoundation-3/)에서 다룬 것처럼, 삼각형의 정점 나열 방향(**와인딩 오더**)이 시계 방향(CW)이면 앞면, 반시계 방향(CCW)이면 뒷면으로 판정됩니다. 같은 삼각형이라도 뒷면에서 보면 화면상 정점 순서가 반대로 뒤집히므로, GPU는 뒷면 삼각형을 자동으로 제거합니다.

구(sphere) 메쉬를 예로 들면, 카메라를 향한 절반의 삼각형은 시계 방향(앞면), 반대편 절반은 반시계 방향(뒷면)으로 나타납니다. 뒷면 제거만으로 처리할 삼각형 수를 절반으로 줄일 수 있습니다.

### 4단계: 래스터화 (Rasterization)

3단계까지 삼각형은 세 정점의 좌표만으로 정의되어 있습니다. 화면에 표시하려면 이 삼각형이 어떤 픽셀들을 덮는지 알아내야 합니다.

**래스터화(Rasterization)** 는 삼각형이 화면에서 덮는 영역을 픽셀 단위로 변환하는 과정입니다.

삼각형이 덮는 각 픽셀 위치마다 **프래그먼트(Fragment)** 가 하나씩 생성됩니다. 프래그먼트는 아직 최종 색상이 결정되지 않은 픽셀 후보로, 이후 프래그먼트 셰이더와 깊이 테스트를 거쳐야 실제 픽셀이 됩니다.

하나의 픽셀 위치에 여러 삼각형이 겹치면 프래그먼트도 여러 개 생성되며, 깊이 테스트에서 가장 가까운 것만 남습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 제목 -->
  <text x="260" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">래스터화 — 삼각형 → 프래그먼트</text>

  <!-- 좌측: 삼각형 -->
  <polygon points="120,42 50,170 190,170" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">삼각형</text>

  <!-- 화살표 -->
  <line x1="210" y1="110" x2="270" y2="110" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="268,105 278,110 268,115" fill="currentColor"/>

  <!-- 우측: 픽셀 격자 (7×5) -->
  <!-- 격자 시작: x=295, y=50, 셀 크기=24 -->
  <!-- 행 0: 3번째만 프래그먼트 -->
  <rect x="295" y="50" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <rect x="319" y="50" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <rect x="343" y="50" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="367" y="50" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <rect x="391" y="50" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- 행 1: 2~4번 프래그먼트 -->
  <rect x="295" y="74" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <rect x="319" y="74" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="343" y="74" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="367" y="74" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="391" y="74" width="24" height="24" rx="2" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- 행 2: 1~5번 프래그먼트 -->
  <rect x="295" y="98" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="319" y="98" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="343" y="98" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="367" y="98" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="391" y="98" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <!-- 행 3: 전부 프래그먼트 -->
  <rect x="271" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="295" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="319" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="343" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="367" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="391" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <rect x="415" y="122" width="24" height="24" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>

  <!-- 삼각형 외곽선을 격자 위에 오버레이 -->
  <polygon points="355,45 277,150 439,150" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3" stroke-dasharray="4,3"/>

  <!-- 범례 -->
  <rect x="295" y="162" width="12" height="12" rx="1" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1"/>
  <text x="312" y="173" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">프래그먼트</text>
  <rect x="375" y="162" width="12" height="12" rx="1" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="392" y="173" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">삼각형 밖</text>
</svg>
</div>

<br>

프래그먼트가 생성될 때, 세 정점의 속성(UV, 노멀 등)이 프래그먼트 위치에 맞게 **보간(Interpolation)** 됩니다. 프래그먼트가 세 정점 중 어느 쪽에 가까운지에 비례하여 해당 위치의 속성값이 결정됩니다.

정점은 삼각형의 꼭짓점일 뿐이고, 프래그먼트는 그 삼각형이 덮는 픽셀마다 생성됩니다. 예를 들어 Full HD(1920×1080) 화면의 절반을 채우는 오브젝트는 정점이 수백 개에 불과해도 약 100만 개의 프래그먼트를 만들어냅니다.
프래그먼트 셰이더는 이 각각에 대해 실행되므로, 버텍스 셰이더보다 비용이 높아지기 쉽습니다.

### 5단계: 프래그먼트 셰이더 (Fragment Shader)

프래그먼트 셰이더의 역할은 각 프래그먼트의 **최종 색상**을 결정하는 것입니다.

**프래그먼트 하나당 하나의 스레드**가 실행되며, 버텍스 셰이더와 마찬가지로 Warp 단위로 병렬 처리됩니다.

같은 픽셀 위치에 배경 벽과 캐릭터가 겹치면, 그 위치에서 프래그먼트가 두 개 생성되고 프래그먼트 셰이더도 두 번 실행됩니다. 장면이 복잡할수록 겹치는 오브젝트가 많아지므로, 총 프래그먼트 수도 늘어납니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프래그먼트 셰이더의 주요 작업</text>

  <!-- 1. 텍스처 샘플링 -->
  <rect x="30" y="42" width="420" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="62" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 텍스처 샘플링</text>
  <text x="50" y="82" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">보간된 UV 좌표로 텍스처에서 텍셀(텍스처의 픽셀)을 읽어옴</text>
  <text x="420" y="62" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">메모리 접근</text>

  <!-- 2. 조명 계산 -->
  <rect x="30" y="106" width="420" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="126" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. 조명 계산</text>
  <text x="50" y="146" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">법선 벡터·광원 방향·카메라 방향으로 표면의 밝기와 색상을 계산</text>
  <text x="420" y="126" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">수학 연산</text>

  <!-- 3. 추가 효과 -->
  <rect x="30" y="170" width="420" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="190" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 추가 효과</text>
  <text x="50" y="210" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">그림자, 반사, 노멀 맵핑, 이미시브(자체 발광) 등</text>
  <text x="420" y="190" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">메모리 + 수학</text>

  <!-- 하단: 결과 -->
  <line x1="240" y1="228" x2="240" y2="242" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="235,240 240,250 245,240" fill="currentColor"/>
  <text x="240" y="260" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">최종 색상 출력</text>
</svg>
</div>

<br>

텍스처를 3장 샘플링하면 1장일 때보다 메모리 접근이 3배 늘어나고, 조명 모델이 복잡해지면 수학 연산도 비례하여 늘어납니다. 이 비용이 프래그먼트 수만큼 곱해지므로, 프래그먼트 셰이더 한 줄의 변경이 전체 프레임 시간에 큰 차이를 만들 수 있습니다.

### 6단계: 스텐실 테스트, 깊이 테스트, 블렌딩

프래그먼트 셰이더가 색상을 계산한 뒤에도, 그 결과가 바로 화면에 쓰이지는 않습니다. 다른 오브젝트에 가려지는지, 반투명이라면 뒤쪽 색상과 어떻게 혼합할지를 먼저 판단해야 합니다.

이 판단은 **스텐실 테스트 → 깊이 테스트 → 블렌딩** 순서로 수행되며, 앞 과정에서 실패한 프래그먼트는 뒤 과정으로 넘어가지 않습니다. 세 처리 모두 **프레임버퍼(Framebuffer)** — 최종 이미지를 담는 GPU 메모리 영역 — 안의 버퍼를 사용합니다.

<br>

**스텐실 테스트(Stencil Test)** 는 프레임버퍼의 **스텐실 버퍼(Stencil Buffer)** 를 사용합니다. 스텐실 버퍼에는 각 픽셀마다 정수값이 저장되어 있어, 특정 영역에만 렌더링을 허용하거나 차단하는 마스크 역할을 합니다.

예를 들어 거울 효과를 구현할 때, 먼저 거울 오브젝트를 렌더링하면서 거울이 차지하는 픽셀에 스텐실 값 1을 기록합니다. 이후 반사된 장면을 그릴 때 스텐실 값이 1인 픽셀에만 렌더링을 허용하면, 반사 장면이 거울 영역 밖으로 새어 나가지 않습니다. 포털 효과도 같은 원리입니다.

<br>

스텐실 테스트를 통과한 프래그먼트는 **깊이 테스트(Depth Test)** 를 거칩니다. 깊이 테스트는 프레임버퍼의 **깊이 버퍼(Z-buffer)** 를 사용하여, 같은 픽셀에 겹치는 오브젝트 중 카메라에 가장 가까운 것만 화면에 남깁니다.

깊이 버퍼에는 각 픽셀 위치마다 현재까지 기록된 가장 가까운 프래그먼트의 깊이값이 저장되어 있습니다. 새 프래그먼트가 도착하면 GPU가 이 값과 비교하여, 기존값보다 가까우면 색상을 기록하고, 그렇지 않으면 버립니다.

깊이 테스트는 내부적으로 **깊이 읽기**(비교)와 **깊이 쓰기**(갱신) 두 동작으로 나뉘며, 각각 독립적으로 켜고 끌 수 있습니다.

불투명 오브젝트는 읽기와 쓰기를 모두 활성화하여, 렌더링 순서와 무관하게 가까운 것이 먼 것을 자연스럽게 가립니다. 반투명 오브젝트는 쓰기를 끄고 읽기만 수행합니다.

<br>

불투명 오브젝트는 깊이 테스트를 통과하면 프레임버퍼의 기존 색상을 그대로 덮어씁니다. 유리나 파티클 이펙트처럼 뒤가 비치는 오브젝트는 덮어쓰는 대신 **블렌딩(Blending)** 으로 기존 색상과 혼합합니다.
예를 들어, 알파값이 0.5인 반투명 유리의 프래그먼트가 도착하면, 유리의 색상 50%와 프레임버퍼에 이미 기록된 뒤쪽 오브젝트의 색상 50%를 혼합합니다.

블렌딩에는 뒤쪽 색상이 프레임버퍼에 먼저 기록되어 있어야 하므로, 반투명 오브젝트에 깊이 쓰기를 켜 두면 문제가 됩니다.
반투명 유리 A(깊이 0.3)가 먼저 렌더링되면서 깊이 버퍼에 0.3을 기록하면, A를 통해 비쳐 보여야 할 반투명 유리 B(깊이 0.7)가 깊이 테스트에서 탈락하여 GPU가 폐기합니다.

그래서 반투명 오브젝트는 **깊이 쓰기를 비활성화**하고 읽기만 수행합니다.

<div align="center">
<svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- 제목 -->
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">깊이 쓰기 비활성화의 효과</text>

  <!-- 구분선 -->
  <line x1="310" y1="38" x2="310" y2="300" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.15"/>

  <!-- ===== 왼쪽: 깊이 쓰기 OFF ===== -->
  <text x="150" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="#4CAF50">깊이 쓰기 OFF</text>

  <!-- ① 불투명 벽 -->
  <rect x="10" y="62" width="280" height="56" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.3"/>
  <text x="24" y="82" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="currentColor">① 불투명 벽 렌더링</text>
  <text x="24" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">깊이 버퍼 ← 0.9</text>

  <line x1="150" y1="118" x2="150" y2="131" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="147,129 150,135 153,129" fill="currentColor" opacity="0.3"/>

  <!-- ② 유리 A -->
  <rect x="10" y="138" width="280" height="56" rx="5" fill="#4CAF50" fill-opacity="0.06" stroke="#4CAF50" stroke-width="1" stroke-opacity="0.4"/>
  <text x="24" y="158" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="currentColor">② 유리 A (깊이 0.3)</text>
  <text x="24" y="176" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">0.3 &lt; 0.9 → ✓ 통과 · 혼합</text>
  <text x="276" y="188" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">깊이 버퍼: 0.9 (변경 없음)</text>

  <line x1="150" y1="194" x2="150" y2="207" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="147,205 150,211 153,205" fill="currentColor" opacity="0.3"/>

  <!-- ③ 유리 B -->
  <rect x="10" y="214" width="280" height="56" rx="5" fill="#4CAF50" fill-opacity="0.06" stroke="#4CAF50" stroke-width="1" stroke-opacity="0.4"/>
  <text x="24" y="234" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="currentColor">③ 유리 B (깊이 0.7)</text>
  <text x="24" y="252" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">0.7 &lt; 0.9 → ✓ 통과 · 혼합</text>
  <text x="276" y="264" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">깊이 버퍼: 0.9 (변경 없음)</text>

  <!-- 결과 -->
  <text x="150" y="300" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="#4CAF50">벽 · 유리 A · 유리 B 모두 표시</text>

  <!-- ===== 오른쪽: 깊이 쓰기 ON ===== -->
  <text x="470" y="50" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="#EF5350">깊이 쓰기 ON</text>

  <!-- ① 불투명 벽 -->
  <rect x="330" y="62" width="280" height="56" rx="5" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.3"/>
  <text x="344" y="82" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="currentColor">① 불투명 벽 렌더링</text>
  <text x="344" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">깊이 버퍼 ← 0.9</text>

  <line x1="470" y1="118" x2="470" y2="131" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="467,129 470,135 473,129" fill="currentColor" opacity="0.3"/>

  <!-- ② 유리 A — 통과하지만 깊이 버퍼 갱신 -->
  <rect x="330" y="138" width="280" height="56" rx="5" fill="#FFA726" fill-opacity="0.06" stroke="#FFA726" stroke-width="1" stroke-opacity="0.4"/>
  <text x="344" y="158" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="currentColor">② 유리 A (깊이 0.3)</text>
  <text x="344" y="176" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">0.3 &lt; 0.9 → ✓ 통과 · 혼합</text>
  <text x="596" y="188" text-anchor="end" font-family="sans-serif" font-size="9" fill="#FFA726" font-weight="bold">깊이 버퍼: 0.3 ← 갱신</text>

  <line x1="470" y1="194" x2="470" y2="207" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="467,205 470,211 473,205" fill="currentColor" opacity="0.3"/>

  <!-- ③ 유리 B — 폐기 -->
  <rect x="330" y="214" width="280" height="56" rx="5" fill="#EF5350" fill-opacity="0.06" stroke="#EF5350" stroke-width="1" stroke-opacity="0.4"/>
  <text x="344" y="234" font-family="sans-serif" font-size="10.5" font-weight="bold" fill="currentColor">③ 유리 B (깊이 0.7)</text>
  <text x="344" y="252" font-family="sans-serif" font-size="10" fill="#EF5350" opacity="0.8">0.7 &gt; 0.3 → ✗ 폐기</text>
  <text x="596" y="264" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.35">깊이 버퍼: 0.3</text>

  <!-- 결과 -->
  <text x="470" y="300" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="#EF5350">유리 B 누락</text>
</svg>
</div>

반투명 오브젝트끼리는 깊이 버퍼를 갱신하지 않아 서로를 가리지 않지만, 깊이 테스트는 수행하므로 불투명 오브젝트 뒤에 있으면 폐기됩니다.

<br>

다만 블렌딩은 대칭적인 혼합이 아니라, 새 프래그먼트의 색상으로 프레임버퍼의 기존 색상을 부분적으로 덮어쓰는 연산이므로 렌더링 순서에 따라 결과가 달라집니다.

예를 들어 알파 0.5인 유리 두 장이 앞뒤로 겹쳐 있을 때, 뒤쪽 유리를 먼저 렌더링하면 프레임버퍼에는 뒤쪽 유리 50%와 배경 50%가 기록됩니다. 이어서 앞쪽 유리를 렌더링하면, 앞쪽 유리가 최종 색상의 50%를 차지하고 기존 결과 전체가 나머지 50%로 밀려납니다. 뒤쪽 유리는 기존 결과에서 50%였으므로 최종적으로 25%만 남습니다.

현실에서는 눈에 가까운 반투명 오브젝트가 더 잘 보이고, 블렌딩에서는 마지막에 렌더링된 오브젝트의 비중이 가장 높으므로, 가까운 오브젝트가 마지막에 오도록 CPU가 **먼 것부터 가까운 순서(back-to-front)**로 정렬하여 드로우 콜을 제출합니다. 이 순서가 어긋나면 앞뒤가 뒤집혀 보입니다.

<br>

반투명 오브젝트끼리의 순서는 back-to-front으로 정해지지만, 불투명 오브젝트와의 순서도 정해져야 합니다. 반투명 유리가 불투명 벽 앞에 있다면, 유리는 벽의 색상과 블렌딩해야 합니다. 벽이 아직 렌더링되지 않았다면 블렌딩할 색상이 버퍼에 없으므로, 불투명 오브젝트가 항상 먼저 렌더링되어 깊이값과 색상을 버퍼에 기록해야 합니다.

Unity는 이 순서를 **렌더 큐(Render Queue)** 로 보장합니다. Unity의 셰이더 파일에는 GPU 프로그램 코드 외에 렌더링 설정도 함께 기술되어 있으며, 렌더 큐는 그중 렌더링 순서를 결정하는 번호입니다. 불투명 셰이더는 2000(Geometry), 반투명 셰이더는 3000(Transparent)이 기본값입니다.

Unity에서 CPU는 렌더 큐 번호가 낮은 순서대로 드로우 콜을 제출합니다. 렌더 큐 2500 이하인 오브젝트는 불투명 경로로 front-to-back 정렬되어 먼저 렌더링되고 깊이 버퍼에 깊이값을 기록합니다. 렌더 큐 2500 초과인 오브젝트는 반투명 경로로 back-to-front 정렬되어 그 뒤에 렌더링되며, 이 깊이값을 기준으로 깊이 테스트를 거칩니다.

앞서 설명한 깊이 쓰기 비활성화와 블렌딩 방식은 셰이더 파일에서 `ZWrite Off`, `Blend SrcAlpha OneMinusSrcAlpha` 같은 **렌더링 상태 선언**으로 지정하고, CPU가 이를 GPU 고정 기능 하드웨어에 적용합니다.

### 7단계: 프레임버퍼 출력

모든 테스트를 통과한 프래그먼트의 데이터가 프레임버퍼에 기록됩니다. 프레임버퍼는 색상 버퍼, 깊이 버퍼, 스텐실 버퍼로 구성되며, 각각 프래그먼트의 색상, 깊이값, 스텐실 값을 저장합니다.

색상 버퍼에는 블렌딩 설정에 따라 기존 색상을 덮어쓰거나 기존 색상과 혼합한 결과가 기록됩니다. 깊이 버퍼는 읽기·쓰기 설정에 따라 비교와 갱신이 이루어지고, 스텐실 버퍼는 스텐실 연산 설정에 따라 갱신됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 타이틀 -->
  <text x="240" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레임버퍼 구성</text>
  <!-- 외곽 프레임버퍼 박스 -->
  <rect x="30" y="35" width="420" height="215" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="55" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프레임버퍼</text>
  <!-- 색상 버퍼 -->
  <rect x="55" y="68" width="140" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="125" y="88" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">색상 버퍼</text>
  <text x="125" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(Color)</text>
  <text x="215" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">각 픽셀의 최종 색상</text>
  <text x="215" y="104" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(RGBA: 빨강, 초록, 파랑, 알파)</text>
  <!-- 깊이 버퍼 -->
  <rect x="55" y="128" width="140" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="125" y="148" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">깊이 버퍼</text>
  <text x="125" y="164" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(Depth)</text>
  <text x="215" y="148" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">각 픽셀의 깊이 값</text>
  <text x="215" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(깊이 테스트에 사용)</text>
  <!-- 스텐실 버퍼 -->
  <rect x="55" y="188" width="140" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="125" y="208" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">스텐실 버퍼</text>
  <text x="125" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(Stencil)</text>
  <text x="215" y="208" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">각 픽셀의 스텐실 값</text>
  <text x="215" y="224" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(마스킹에 사용)</text>
</svg>
</div>

<br>

이 프레임버퍼의 내용을 실제로 모니터에 전송하는 것은 GPU 칩 안에서 렌더링과 별도로 동작하는 **디스플레이 컨트롤러**입니다.
모니터의 주사율에 맞춰 픽셀 데이터를 지속적으로 읽고, HDMI나 DisplayPort 같은 인터페이스를 통해 전송합니다.

만약 프레임버퍼가 한 벌뿐이라면, 디스플레이 컨트롤러가 읽고 있는 프레임버퍼에 GPU가 동시에 렌더링하게 됩니다.
이 경우 화면을 스캔하는 도중에 내용이 바뀌어 상반부는 이전 프레임, 하반부는 현재 프레임이 표시되는 **티어링(Tearing)** 이 발생합니다.

이를 방지하기 위해 일반적으로 프레임버퍼를 두 벌 이상 사용하며, 가장 기본적인 형태가 **더블 버퍼링**입니다.
GPU가 화면에 보이지 않는 **백 버퍼(Back Buffer)**에 렌더링하고, 한 프레임이 완성되면 화면에 표시 중인 **프론트 버퍼(Front Buffer)**와 교체(Swap)하는 방식입니다. 교체 후 백 버퍼가 프론트 버퍼가 되어 화면에 표시되고, 기존 프론트 버퍼는 다음 프레임의 렌더링 대상이 됩니다.

<br>

렌더링 파이프라인은 정점 데이터에서 시작하여 프레임버퍼의 픽셀까지 데이터가 흘러가는 과정입니다.

개발자가 직접 프로그래밍하는 단계는 좌표를 변환하는 버텍스 셰이더와 색상을 계산하는 프래그먼트 셰이더 두 곳이고, 래스터화·깊이 테스트·블렌딩 같은 나머지 단계는 GPU의 고정 기능 하드웨어가 처리합니다.

Unity의 셰이더 파일은 이 두 프로그래머블 단계의 GPU 프로그램 코드와 함께, 렌더 큐·깊이 쓰기·블렌드 모드 같은 고정 기능 하드웨어의 렌더링 상태를 정의합니다.

CPU는 렌더 큐 순서에 따라 드로우 콜을 제출하고, 이 렌더링 상태를 GPU에 적용합니다.

---

## 데스크톱 GPU의 IMR 방식

앞서 다룬 렌더링 파이프라인의 7단계는 모든 GPU에서 동일한 논리적 흐름입니다. 그러나 이 흐름을 **물리적으로 어떻게 실행하는가**는 GPU 아키텍처마다 다릅니다.

데스크톱 GPU(NVIDIA GeForce, AMD Radeon 등)는 대부분 **IMR(Immediate Mode Rendering)** 방식을 사용합니다.

### IMR의 동작 원리

IMR은 이름 그대로 **즉시 실행**하는 렌더링 방식입니다. CPU가 드로우 콜을 제출하면, GPU는 해당 삼각형을 파이프라인의 처음부터 프레임버퍼 기록까지 곧바로 처리합니다.

개별 삼각형은 파이프라인을 순차적으로 통과하지만, GPU 전체로 보면 여러 삼각형이 서로 다른 단계에 동시에 있습니다. 삼각형 A가 프래그먼트 셰이딩 단계에 있을 때, 삼각형 B는 래스터화, 삼각형 C는 버텍스 셰이더 단계에 있을 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <!-- 타이틀 -->
  <text x="340" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">IMR 처리 흐름</text>
  <!-- 시간 축 화살표 -->
  <line x1="60" y1="40" x2="640" y2="40" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="640,40 633,36 633,44" fill="currentColor"/>
  <text x="650" y="44" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">시간</text>
  <!-- 단계 박스 크기: w=80 h=28, 간격=8 -->
  <!-- 삼각형 1: 시작 x=68 -->
  <text x="20" y="68" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">삼각형 1</text>
  <rect x="68" y="52" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="104" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">VS</text>
  <line x1="140" y1="66" x2="148" y2="66" stroke="currentColor" stroke-width="1"/>
  <polygon points="148,66 144,63 144,69" fill="currentColor"/>
  <rect x="148" y="52" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="184" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">클리핑</text>
  <line x1="220" y1="66" x2="228" y2="66" stroke="currentColor" stroke-width="1"/>
  <polygon points="228,66 224,63 224,69" fill="currentColor"/>
  <rect x="228" y="52" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="264" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">래스터화</text>
  <line x1="300" y1="66" x2="308" y2="66" stroke="currentColor" stroke-width="1"/>
  <polygon points="308,66 304,63 304,69" fill="currentColor"/>
  <rect x="308" y="52" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="344" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">FS</text>
  <line x1="380" y1="66" x2="388" y2="66" stroke="currentColor" stroke-width="1"/>
  <polygon points="388,66 384,63 384,69" fill="currentColor"/>
  <rect x="388" y="52" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="424" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">테스트</text>
  <line x1="460" y1="66" x2="468" y2="66" stroke="currentColor" stroke-width="1"/>
  <polygon points="468,66 464,63 464,69" fill="currentColor"/>
  <rect x="468" y="52" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="504" y="70" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">FB 쓰기</text>
  <!-- 삼각형 2: 시작 x=148 (1단계 오프셋) -->
  <text x="20" y="108" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">삼각형 2</text>
  <rect x="148" y="92" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="184" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">VS</text>
  <line x1="220" y1="106" x2="228" y2="106" stroke="currentColor" stroke-width="1"/>
  <polygon points="228,106 224,103 224,109" fill="currentColor"/>
  <rect x="228" y="92" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="264" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">클리핑</text>
  <line x1="300" y1="106" x2="308" y2="106" stroke="currentColor" stroke-width="1"/>
  <polygon points="308,106 304,103 304,109" fill="currentColor"/>
  <rect x="308" y="92" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="344" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">래스터화</text>
  <line x1="380" y1="106" x2="388" y2="106" stroke="currentColor" stroke-width="1"/>
  <polygon points="388,106 384,103 384,109" fill="currentColor"/>
  <rect x="388" y="92" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="424" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">FS</text>
  <line x1="460" y1="106" x2="468" y2="106" stroke="currentColor" stroke-width="1"/>
  <polygon points="468,106 464,103 464,109" fill="currentColor"/>
  <rect x="468" y="92" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="504" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">테스트</text>
  <line x1="540" y1="106" x2="548" y2="106" stroke="currentColor" stroke-width="1"/>
  <polygon points="548,106 544,103 544,109" fill="currentColor"/>
  <rect x="548" y="92" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="584" y="110" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">FB 쓰기</text>
  <!-- 삼각형 3: 시작 x=228 (2단계 오프셋) -->
  <text x="20" y="148" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">삼각형 3</text>
  <rect x="228" y="132" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="264" y="150" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">VS</text>
  <line x1="300" y1="146" x2="308" y2="146" stroke="currentColor" stroke-width="1"/>
  <polygon points="308,146 304,143 304,149" fill="currentColor"/>
  <rect x="308" y="132" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="344" y="150" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">클리핑</text>
  <line x1="380" y1="146" x2="388" y2="146" stroke="currentColor" stroke-width="1"/>
  <polygon points="388,146 384,143 384,149" fill="currentColor"/>
  <rect x="388" y="132" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="424" y="150" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">래스터화</text>
  <line x1="460" y1="146" x2="468" y2="146" stroke="currentColor" stroke-width="1"/>
  <polygon points="468,146 464,143 464,149" fill="currentColor"/>
  <rect x="468" y="132" width="72" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="504" y="150" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">FS</text>
  <line x1="540" y1="146" x2="548" y2="146" stroke="currentColor" stroke-width="1"/>
  <polygon points="548,146 544,143 544,149" fill="currentColor"/>
  <text x="560" y="150" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">...</text>
  <!-- 범례 -->
  <text x="140" y="195" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">VS = 버텍스 셰이더</text>
  <text x="300" y="195" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">FS = 프래그먼트 셰이더</text>
  <text x="470" y="195" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">FB = 프레임버퍼</text>
</svg>
</div>

<br>

이처럼 삼각형이 파이프라인을 곧바로 통과하면서, 생성된 프래그먼트마다 **외부 메모리(VRAM)** 접근이 여러 번 발생합니다. 텍스처 샘플링, 스텐실/깊이 버퍼 읽기/쓰기, 색상 버퍼 읽기/쓰기가 모두 VRAM 접근입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- 타이틀 -->
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">IMR의 메모리 접근 패턴</text>
  <!-- GPU 코어 박스 (좌측) -->
  <rect x="30" y="45" width="160" height="220" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 코어 (온칩)</text>
  <rect x="55" y="130" width="110" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="148" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프래그먼트</text>
  <text x="110" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">처리</text>
  <!-- VRAM 박스 (우측) -->
  <rect x="410" y="45" width="160" height="220" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="490" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">VRAM (외부 메모리)</text>
  <!-- 텍스처 읽기 (← 방향) -->
  <line x1="190" y1="95" x2="405" y2="95" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,95 202,91 202,99" fill="currentColor"/>
  <text x="300" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">텍스처 읽기</text>
  <text x="490" y="99" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">텍스처 데이터</text>
  <!-- 스텐실 읽기 (← 방향) -->
  <line x1="190" y1="128" x2="405" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,128 202,124 202,132" fill="currentColor"/>
  <text x="300" y="123" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">스텐실 읽기</text>
  <!-- 스텐실 쓰기 (→ 방향) -->
  <line x1="190" y1="148" x2="405" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="405,148 398,144 398,152" fill="currentColor"/>
  <text x="300" y="143" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">스텐실 쓰기</text>
  <text x="490" y="140" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">스텐실 버퍼</text>
  <!-- 깊이 읽기 (← 방향) -->
  <line x1="190" y1="175" x2="405" y2="175" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,175 202,171 202,179" fill="currentColor"/>
  <text x="300" y="170" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">깊이 읽기</text>
  <!-- 깊이 쓰기 (→ 방향) -->
  <line x1="190" y1="195" x2="405" y2="195" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="405,195 398,191 398,199" fill="currentColor"/>
  <text x="300" y="190" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">깊이 쓰기</text>
  <text x="490" y="187" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">깊이 버퍼</text>
  <!-- 색상 읽기 (← 방향) -->
  <line x1="190" y1="222" x2="405" y2="222" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,222 202,218 202,226" fill="currentColor"/>
  <text x="300" y="217" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">색상 읽기</text>
  <!-- 색상 쓰기 (→ 방향) -->
  <line x1="190" y1="242" x2="405" y2="242" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="405,242 398,238 398,246" fill="currentColor"/>
  <text x="300" y="237" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">색상 쓰기</text>
  <text x="490" y="234" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">색상 버퍼</text>
  <!-- 메모리 버스 (하단) -->
  <line x1="100" y1="290" x2="500" y2="290" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,3"/>
  <polygon points="105,290 112,286 112,294" fill="currentColor"/>
  <polygon points="495,290 488,286 488,294" fill="currentColor"/>
  <text x="300" y="308" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">메모리 버스 (128 ~ 512 bit)</text>
  <text x="300" y="325" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">대역폭: 수백 GB/s</text>
</svg>
</div>

### 대역폭과 IMR

GPU 코어와 VRAM 사이의 데이터 전송에는 **메모리 대역폭(Memory Bandwidth)** 이라는 물리적 한계가 있습니다. 대역폭은 단위 시간당 전송할 수 있는 데이터의 양이며, 외부 메모리 접근이 빈번할수록 이 한계에 가까워집니다.

Full HD 해상도(1920×1080 = 약 200만 픽셀)에서 같은 위치에 여러 오브젝트가 겹치면 프래그먼트 수는 수백만에 달하고, 프래그먼트마다 VRAM 접근이 반복되므로 대역폭 소모가 큽니다.

<br>

이 대역폭을 결정하는 핵심 요소가 **메모리 버스(Memory Bus)** 의 폭입니다. 메모리 버스는 GPU 코어와 VRAM을 연결하는 물리적 데이터 통로로, 버스 폭이 256bit이면 한 번에 256bit를 보낼 수 있고, 512bit이면 그 두 배입니다. 버스가 넓을수록 대역폭이 높아집니다.

넓은 버스는 전력 소모도 크지만, 데스크톱 환경에서는 전원 콘센트에서 수백 와트를 공급받을 수 있어 이를 감당합니다. 데스크톱 GPU는 초당 500GB 이상의 대역폭을 제공하며, IMR 방식의 빈번한 VRAM 접근도 병목 없이 처리할 수 있습니다.

### IMR의 오버드로우 문제

같은 픽셀 위치에 여러 삼각형이 겹쳐 그려져 나중 결과가 앞선 결과를 덮어쓰는 현상을 **오버드로우(Overdraw)** 라고 합니다. 
오버드로우 자체는 모든 GPU에서 발생할 수 있지만, IMR에서는 겹치는 모든 프래그먼트가 셰이딩을 거치므로, 덮어쓰인 프래그먼트의 셰이딩 비용이 그대로 낭비됩니다.

예를 들어, 뒤에 있는 배경 벽이 먼저 셰이딩되어 프레임버퍼에 기록된 뒤, 앞에 있는 캐릭터가 같은 위치를 덮어쓰면 배경 벽의 셰이딩 비용은 낭비된 셈입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 타이틀 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">오버드로우 — 같은 픽셀 위치 (x, y)</text>
  <text x="280" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">렌더링 순서: 뒤에 있는 오브젝트부터 · 깊이 버퍼 초기값: 1.0 (가장 먼 거리)</text>

  <!-- ① 배경 벽 -->
  <text x="30" y="72" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">① 배경 벽</text>
  <text x="30" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.9</text>

  <rect x="130" y="58" width="110" height="36" rx="5" fill="#EF5350" fill-opacity="0.08" stroke="#EF5350" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="185" y="81" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이딩 실행</text>

  <line x1="240" y1="76" x2="260" y2="76" stroke="currentColor" stroke-width="1"/>
  <polygon points="258,72 266,76 258,80" fill="currentColor"/>

  <rect x="266" y="58" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="331" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">깊이 테스트</text>
  <text x="331" y="88" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">0.9 &lt; 1.0 → 통과</text>

  <line x1="396" y1="76" x2="416" y2="76" stroke="currentColor" stroke-width="1"/>
  <polygon points="414,72 422,76 414,80" fill="currentColor"/>

  <rect x="422" y="58" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="477" y="74" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">색상/깊이 기록</text>
  <text x="477" y="88" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">깊이 버퍼: 1.0 → 0.9</text>

  <!-- 화살표 ①→② -->
  <line x1="280" y1="94" x2="280" y2="120" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="276,118 280,126 284,118" fill="currentColor" opacity="0.3"/>

  <!-- ② 캐릭터 -->
  <text x="30" y="148" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">② 캐릭터</text>
  <text x="30" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.3</text>

  <rect x="130" y="134" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="185" y="157" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이딩 실행</text>

  <line x1="240" y1="152" x2="260" y2="152" stroke="currentColor" stroke-width="1"/>
  <polygon points="258,148 266,152 258,156" fill="currentColor"/>

  <rect x="266" y="134" width="130" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="331" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">깊이 테스트</text>
  <text x="331" y="164" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">0.3 &lt; 0.9 → 통과</text>

  <line x1="396" y1="152" x2="416" y2="152" stroke="currentColor" stroke-width="1"/>
  <polygon points="414,148 422,152 414,156" fill="currentColor"/>

  <rect x="422" y="134" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="477" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">색상/깊이 덮어쓰기</text>
  <text x="477" y="164" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">깊이 버퍼: 0.9 → 0.3</text>

  <!-- 프레임버퍼 결과 -->
  <line x1="280" y1="182" x2="280" y2="208" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="276,206 280,214 284,206" fill="currentColor" opacity="0.3"/>

  <rect x="170" y="218" width="220" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="243" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임버퍼: 캐릭터만 표시</text>

  <!-- 결론 -->
  <rect x="130" y="278" width="300" height="22" rx="3" fill="#EF5350" fill-opacity="0.04" stroke="none"/>
  <text x="280" y="293" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="#EF5350">① 배경 벽의 셰이딩 비용은 낭비됨</text>
</svg>
</div>

<br>

이 낭비의 근본 원인은 파이프라인의 단계 순서입니다.
앞서 살펴보았듯이 깊이 테스트는 프래그먼트 셰이더 **이후**에 수행되므로, 프래그먼트가 가려져 폐기되더라도 셰이딩 비용은 이미 발생한 뒤입니다.

<br>

이 문제를 완화하는 방식이 **Early-Z 테스트(Early Depth Test)** 입니다.
Early-Z는 깊이 테스트를 프래그먼트 셰이더 **이전에** 수행하는 방식입니다. 더 가까운 프래그먼트가 이미 기록된 위치라면 셰이딩 자체를 건너뜁니다.

Early-Z가 효과적이려면 가까운 오브젝트의 깊이값이 깊이 버퍼에 먼저 기록되어 있어야 합니다. 앞서 CPU가 불투명 오브젝트를 front-to-back으로 정렬한다고 했는데, 이 정렬로 가까운 깊이값이 먼저 기록되면 먼 오브젝트의 깊이 테스트 탈락률이 높아져 프레임버퍼 쓰기가 줄고, Early-Z에서는 셰이딩까지 건너뛸 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 타이틀 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Early-Z 최적화 — 같은 픽셀 위치 (x, y)</text>
  <text x="280" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">렌더링 순서: 앞에 있는 오브젝트부터 (front-to-back)</text>
  <text x="280" y="54" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 버퍼 초기값: 1.0 (가장 먼 거리)</text>

  <!-- ① 캐릭터 -->
  <text x="30" y="88" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">① 캐릭터</text>
  <text x="30" y="104" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.3</text>

  <rect x="130" y="74" width="120" height="36" rx="5" fill="#4CAF50" fill-opacity="0.08" stroke="#4CAF50" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="190" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Early-Z</text>
  <text x="190" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#4CAF50" font-weight="bold">0.3 &lt; 1.0 → 통과</text>

  <line x1="250" y1="92" x2="270" y2="92" stroke="currentColor" stroke-width="1"/>
  <polygon points="268,88 276,92 268,96" fill="currentColor"/>

  <rect x="276" y="74" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="331" y="97" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이딩 실행</text>

  <line x1="386" y1="92" x2="406" y2="92" stroke="currentColor" stroke-width="1"/>
  <polygon points="404,88 412,92 404,96" fill="currentColor"/>

  <rect x="412" y="74" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="472" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">색상/깊이 기록</text>
  <text x="472" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">깊이 버퍼: 1.0 → 0.3</text>

  <!-- 화살표 ①→② -->
  <line x1="280" y1="110" x2="280" y2="136" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="276,134 280,142 284,134" fill="currentColor" opacity="0.3"/>

  <!-- ② 배경 벽 -->
  <text x="30" y="164" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">② 배경 벽</text>
  <text x="30" y="180" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">깊이 0.9</text>

  <rect x="130" y="150" width="120" height="36" rx="5" fill="#EF5350" fill-opacity="0.08" stroke="#EF5350" stroke-width="1.5" stroke-opacity="0.5"/>
  <text x="190" y="166" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Early-Z</text>
  <text x="190" y="180" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#EF5350" font-weight="bold">0.9 &gt; 0.3 → 탈락</text>

  <!-- 셰이딩 건너뜀 표시 -->
  <line x1="260" y1="168" x2="532" y2="168" stroke="currentColor" stroke-width="1" stroke-dasharray="4,4" opacity="0.2"/>
  <rect x="316" y="154" width="140" height="28" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.3"/>
  <text x="386" y="173" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.35">셰이딩 건너뜀</text>

  <!-- 프레임버퍼 결과 -->
  <line x1="280" y1="192" x2="280" y2="216" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="276,214 280,222 284,214" fill="currentColor" opacity="0.3"/>

  <rect x="170" y="226" width="220" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="280" y="251" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">프레임버퍼: 캐릭터만 표시</text>

  <!-- 결론 -->
  <rect x="105" y="283" width="350" height="22" rx="3" fill="#4CAF50" fill-opacity="0.04" stroke="none"/>
  <text x="280" y="298" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="#4CAF50">배경 벽의 셰이딩 비용이 발생하지 않음</text>
</svg>
</div>

<br>

앞에서 Unity의 불투명 오브젝트가 렌더 큐 2000(Geometry)에 속하고, CPU가 카메라와의 거리 기준으로 가까운 것부터(front-to-back) 정렬하여 드로우 콜을 제출한다고 했습니다.

URP와 Built-in 렌더링 파이프라인은 이 Geometry 큐를 포함하여 렌더 큐 2500 이하의 오브젝트를 Opaque 패스에서 렌더링합니다.

> Unity의 기본 설정(`OpaqueSortMode.Default`)은 GPU 종류에 따라 동작이 달라집니다. 대부분의 GPU에서는 front-to-back 정렬을 적용하지만, PowerVR/Apple GPU에서는 이 정렬을 적용하지 않습니다. PowerVR/Apple GPU는 타일 내에서 가시성을 완전히 판정하는 자체 메커니즘(HSR)이 있어 front-to-back 정렬이 불필요하기 때문입니다. 이 메커니즘의 구체적인 동작은 [다음 글](/dev/unity/GPUArchitecture-2/)에서 다룹니다.

---

## 마무리

- CPU는 레이턴시 중심, GPU는 스루풋 중심으로 설계되었습니다. GPU는 SIMT 모델에 따라 같은 셰이더를 Warp(32스레드) 단위로 묶어 병렬 실행하며, Warp 내에서 분기 방향이 갈리면 양쪽 경로를 모두 실행해야 합니다.
- 렌더링 파이프라인은 정점 입력 → 버텍스 셰이더 → 클리핑 → 래스터화 → 프래그먼트 셰이더 → 테스트와 블렌딩 → 프레임버퍼 출력 순서로 진행됩니다. 래스터화 이후 프래그먼트 수가 급증하므로, 프래그먼트 셰이더의 복잡도가 전체 성능에 미치는 영향이 큽니다.
- IMR 방식은 삼각형을 파이프라인의 처음부터 프레임버퍼 기록까지 곧바로 처리하며, 이 과정에서 텍스처 샘플링·깊이 버퍼·색상 버퍼 접근이 모두 VRAM에서 이루어집니다. 데스크톱 GPU는 넓은 메모리 버스와 수백 GB/s의 대역폭으로 이를 감당합니다. 같은 픽셀에 여러 프래그먼트가 겹치는 오버드로우가 발생하면 셰이딩 비용이 낭비되며, front-to-back 정렬과 Early-Z로 이 낭비를 줄일 수 있습니다.

셰이더에서 if문을 줄이라는 조언은 SIMT의 분기 비용에서, 프래그먼트 셰이더의 복잡도를 경계하라는 조언은 래스터화 이후 프래그먼트 수 급증에서, 엔진이 불투명 오브젝트를 front-to-back으로 정렬하는 동작은 Early-Z 최적화에서 비롯됩니다.

<br>

모바일 환경에서는 조건이 다릅니다.

스마트폰의 배터리는 수 와트 수준의 전력만 공급할 수 있고, 메모리 버스 폭도 64~128bit로 좁으며, 대역폭은 데스크톱의 1/10 이하입니다.

이 조건에서 IMR 방식의 빈번한 VRAM 접근은 한정된 대역폭을 압박하고, 전력 소모를 크게 늘립니다.

[다음 글](/dev/unity/GPUArchitecture-2/)에서는 모바일 GPU가 이 한계를 극복하기 위해 채택한 **TBDR(Tile-Based Deferred Rendering)** 아키텍처의 동작 원리와, 이 아키텍처가 Unity 모바일 최적화에 미치는 구체적인 영향을 다룹니다.

<br>

---

**관련 글**
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- **GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인** (현재 글)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- **GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인** (현재 글)
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
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
