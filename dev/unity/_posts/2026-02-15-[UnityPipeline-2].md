---
layout: single
title: "Unity 렌더 파이프라인 (2) - 드로우콜과 배칭 - soo:bak"
date: "2026-02-15 16:33:00 +0900"
description: 드로우콜의 정의, 상태 변경 비용, SetPass Call, Static/Dynamic Batching, SRP Batcher, GPU Instancing을 설명합니다.
tags:
  - Unity
  - 최적화
  - 드로우콜
  - 배칭
  - 모바일
---

## GPU에 명령을 보내는 비용

[Part 1](/dev/unity/UnityPipeline-1/)에서는 렌더 파이프라인이 씬을 렌더링하기 위해 GPU에 명령을 보내는 구조를 살펴보았습니다. 그런데 이 명령을 보내는 과정 자체에 비용이 발생합니다.

CPU는 오브젝트를 그릴 때마다 GPU에 렌더링 명령을 보내는데, 이를 **드로우콜(Draw Call)**이라 합니다. 씬의 오브젝트가 많아지면 드로우콜 수도 함께 늘어나고, 드로우콜을 준비하고 전달하는 CPU 측 비용이 병목이 되어 프레임을 제시간에 완성하지 못하게 됩니다.

이 비용을 줄이기 위해 여러 드로우콜을 묶거나 상태 변경을 줄이는 접근을 사용하는데, 이를 **배칭(Batching)**이라 합니다. Unity는 Static Batching, Dynamic Batching, SRP Batcher, GPU Instancing 네 가지 배칭 기법을 제공하며, 이 글에서는 드로우콜의 비용이 정확히 어디서 발생하는지 분석한 뒤 각 기법의 원리와 트레이드오프를 살펴봅니다.

---

## 드로우콜(Draw Call)의 정의

하나의 드로우콜에는 "이 메쉬의 삼각형들을, 이 머티리얼이 지정하는 셰이더와 프로퍼티로 렌더링하라"는 의미가 담겨 있습니다. 
하나의 드로우콜은 하나의 메쉬-머티리얼 조합만 처리할 수 있으므로, 기본적으로 오브젝트마다 별도의 드로우콜이 필요합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="520" height="300" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="260" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬의 오브젝트와 드로우콜</text>
  <!-- CPU 헤더 -->
  <text x="90" y="58" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <line x1="50" y1="63" x2="130" y2="63" stroke="currentColor" stroke-width="1"/>
  <!-- GPU 헤더 -->
  <text x="430" y="58" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU</text>
  <line x1="390" y1="63" x2="470" y2="63" stroke="currentColor" stroke-width="1"/>
  <!-- 나무 A -->
  <rect x="30" y="78" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 A</text>
  <line x1="150" y1="92" x2="370" y2="92" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,88 380,92 370,96" fill="currentColor"/>
  <text x="260" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">드로우콜 1</text>
  <rect x="380" y="78" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="96" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>
  <!-- 나무 B -->
  <rect x="30" y="116" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="134" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 B</text>
  <line x1="150" y1="130" x2="370" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,126 380,130 370,134" fill="currentColor"/>
  <text x="260" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">드로우콜 2</text>
  <rect x="380" y="116" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="134" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>
  <!-- 건물 A -->
  <rect x="30" y="154" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">건물 A</text>
  <line x1="150" y1="168" x2="370" y2="168" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,164 380,168 370,172" fill="currentColor"/>
  <text x="260" y="162" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">드로우콜 3</text>
  <rect x="380" y="154" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>
  <!-- 생략 표시 -->
  <text x="90" y="206" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">⋮</text>
  <text x="260" y="206" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">⋮</text>
  <text x="430" y="206" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">⋮</text>
  <!-- 캐릭터 C -->
  <rect x="30" y="218" width="120" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="236" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">캐릭터 C</text>
  <line x1="150" y1="232" x2="370" y2="232" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="370,228 380,232 370,236" fill="currentColor"/>
  <text x="260" y="226" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">드로우콜 18</text>
  <rect x="380" y="218" width="100" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="430" y="236" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>
  <!-- 하단 구분선 및 요약 -->
  <line x1="20" y1="260" x2="500" y2="260" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="282" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">오브젝트 18개 → 드로우콜 18회</text>
</svg>
</div>

<br>

오브젝트가 많아지면 드로우콜도 늘어납니다. 하지만 성능 병목은 드로우콜의 수 자체보다, 각 드로우콜 직전에 발생하는 **GPU 상태 변경을 CPU가 준비하는 과정**에 있는 경우가 많습니다.

---

## 상태 변경 비용

CPU가 GPU에 렌더링 명령을 보내는 구조는 **상태 머신(State Machine)** 모델을 따릅니다.
상태 머신은 현재 설정된 상태에 따라 동작이 결정되는 구조이므로, GPU가 삼각형을 그리기 전에는 어떤 셰이더를 사용할 것인지, 어떤 텍스처를 바인딩할 것인지, 블렌딩 모드는 무엇인지 같은 상태를 먼저 설정해야 합니다.
나무를 그린 뒤 건물을 그리려면, 나무에 사용하던 셰이더와 텍스처를 건물용으로 교체해야 합니다. 이처럼 드로우콜 사이에서 상태를 전환할 때마다 비용이 발생합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="560" height="420" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="280" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">하나의 오브젝트를 그리기 위한 CPU → GPU 명령 흐름</text>
  <!-- 헤더 -->
  <text x="140" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU가 보내는 명령</text>
  <text x="400" y="56" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU에서 일어나는 일</text>
  <line x1="30" y1="64" x2="530" y2="64" stroke="currentColor" stroke-width="1"/>
  <!-- 상태 변경 영역 배경 -->
  <rect x="20" y="72" width="520" height="264" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="530" y="204" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">상태 변경</text>
  <!-- (1) SetShader -->
  <rect x="40" y="82" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1) SetShader</text>
  <line x1="220" y1="96" x2="290" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,92 300,96 290,100" fill="currentColor"/>
  <rect x="300" y="82" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">셰이더 프로그램 전환</text>
  <!-- (2) SetBlendState -->
  <rect x="40" y="118" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="136" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(2) SetBlendState</text>
  <line x1="220" y1="132" x2="290" y2="132" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,128 300,132 290,136" fill="currentColor"/>
  <rect x="300" y="118" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="136" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">블렌딩 상태 전환</text>
  <!-- (3) SetDepthStencil -->
  <rect x="40" y="154" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(3) SetDepthStencil</text>
  <line x1="220" y1="168" x2="290" y2="168" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,164 300,168 290,172" fill="currentColor"/>
  <rect x="300" y="154" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">깊이·스텐실 상태 전환</text>
  <!-- (4) SetRasterizer -->
  <rect x="40" y="190" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="208" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(4) SetRasterizer</text>
  <line x1="220" y1="204" x2="290" y2="204" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,200 300,204 290,208" fill="currentColor"/>
  <rect x="300" y="190" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="208" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">래스터라이저 상태 전환</text>
  <!-- (5) BindTexture -->
  <rect x="40" y="226" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="244" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(5) BindTexture</text>
  <line x1="220" y1="240" x2="290" y2="240" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,236 300,240 290,244" fill="currentColor"/>
  <rect x="300" y="226" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="244" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처 슬롯 설정</text>
  <!-- (6) SetUniform -->
  <rect x="40" y="262" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="280" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(6) SetUniform</text>
  <line x1="220" y1="276" x2="290" y2="276" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,272 300,276 290,280" fill="currentColor"/>
  <rect x="300" y="262" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="280" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">상수 버퍼 갱신</text>
  <!-- (7) BindMesh -->
  <rect x="40" y="298" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(7) BindMesh</text>
  <line x1="220" y1="312" x2="290" y2="312" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,308 300,312 290,316" fill="currentColor"/>
  <rect x="300" y="298" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">정점·인덱스 버퍼 바인딩</text>
  <!-- 구분선 -->
  <line x1="30" y1="348" x2="530" y2="348" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,4"/>
  <!-- (8) DrawCall -->
  <rect x="40" y="360" width="180" height="28" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="2"/>
  <text x="130" y="378" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(8) DrawCall</text>
  <line x1="220" y1="374" x2="290" y2="374" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="290,370 300,374 290,378" fill="currentColor"/>
  <rect x="300" y="360" width="200" height="28" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="2"/>
  <text x="400" y="378" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">삼각형 렌더링 시작</text>
  <text x="530" y="378" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">← 실제 드로우콜</text>
</svg>
</div>

(1)~(7)이 상태 변경이고, (8)이 실제 드로우콜입니다.

> 이 외에도 렌더 타겟 전환(SetRenderTarget), 뷰포트·시저 설정(SetViewport/SetScissor), 텍스처 샘플러 설정(SetSampler), 정점 입력 형식 설정(SetInputLayout) 등의 상태 변경이 있습니다. 렌더 타겟과 뷰포트는 오브젝트 단위가 아니라 렌더 패스나 카메라 단위로 변경되고, 샘플러와 입력 형식은 셰이더 전환 시 함께 변경되므로 위 다이어그램에서는 오브젝트를 그릴 때마다 개별적으로 변경될 수 있는 항목만 표기했습니다.

<br>

오브젝트 단위로 발생하는 상태 변경 중 일반적으로 가장 비용이 큰 것은 셰이더 교체입니다. GPU 파이프라인이 처리량을 높이기 위해 여러 단계를 동시에 진행하는 구조이기 때문입니다.

CPU가 드로우콜을 실행하면, GPU는 해당 메쉬의 삼각형들을 파이프라인에 순서대로 투입합니다. 삼각형 A가 정점 처리를 마치고 프래그먼트 처리로 넘어가면, 비어진 정점 처리 자리에 삼각형 B가 곧바로 들어옵니다.
이때 다음 드로우콜이 다른 셰이더를 사용한다면, 이전 셰이더와 새 셰이더의 처리 로직이 다르므로 파이프라인에서 두 셰이더의 작업을 섞어 진행할 수 없습니다.
파이프라인에 남아 있는 이전 작업이 모두 정리될 때까지 지연(pipeline stall)이 발생하고, 셰이더 교체가 잦을수록 이 지연이 누적되어 성능에 영향을 줍니다.

**같은 머티리얼**을 사용하는 오브젝트를 연속으로 그리면 셰이더·텍스처·블렌딩·깊이/스텐실·래스터라이저 상태가 모두 동일하므로, 비용이 큰 상태 전환을 건너뛸 수 있습니다. 오브젝트마다 달라지는 것은 트랜스폼 등의 상수 버퍼(SetUniform)와 메쉬 데이터(BindMesh) 정도입니다.

---

## SetPass Call

앞에서 살펴본 것처럼 드로우콜 사이에는 여러 종류의 상태 변경이 발생합니다.
이 중 상수 버퍼(SetUniform)나 메쉬(BindMesh)처럼 오브젝트마다 바뀌는 가벼운 변경도 있지만, 셰이더의 **패스(Pass)**가 바뀌는 경우에는 비용이 큽니다.
패스란 셰이더가 정점 처리부터 프래그먼트 처리까지를 한 번 수행하는 단위로, 셰이더 프로그램·블렌딩·깊이/스텐실·래스터라이저·텍스처 설정을 하나의 묶음으로 포함합니다. 패스가 바뀌면 이 설정이 한꺼번에 전환됩니다.

Unity는 이 패스 전환 횟수만을 따로 **SetPass Call**이라는 지표로 추적하며, 렌더링 성능을 판단하는 핵심 지표로 사용합니다.

같은 머티리얼을 사용하는 오브젝트를 연속으로 그리면 패스가 유지되므로 SetPass Call이 줄어듭니다. [Part 1](/dev/unity/UnityPipeline-1/)에서 다룬 렌더 파이프라인의 오브젝트 정렬에서 머티리얼이 정렬 기준 중 하나인 것도 이러한 이유입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="640" height="520" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="320" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">패스 전환과 드로우콜의 관계</text>

  <!-- ===== 비효율적 섹션 ===== -->
  <rect x="20" y="46" width="600" height="210" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="320" y="66" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">[비효율적] 머티리얼이 계속 바뀜</text>

  <!-- Row 1: 패스 전환 A -->
  <rect x="40" y="78" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="94" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → A</text>
  <line x1="170" y1="90" x2="230" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,86 240,90 230,94" fill="currentColor"/>
  <rect x="240" y="78" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="94" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 1: 나무</text>

  <!-- Row 2: 패스 전환 B -->
  <rect x="40" y="110" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → B</text>
  <line x1="170" y1="122" x2="230" y2="122" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,118 240,122 230,126" fill="currentColor"/>
  <rect x="240" y="110" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 2: 건물</text>

  <!-- Row 3: 패스 전환 A again -->
  <rect x="40" y="142" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → A</text>
  <line x1="170" y1="154" x2="230" y2="154" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,150 240,154 230,158" fill="currentColor"/>
  <rect x="240" y="142" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 3: 나무</text>
  <text x="420" y="158" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">← A로 되돌아감</text>

  <!-- Row 4: 패스 전환 C -->
  <rect x="40" y="174" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → C</text>
  <line x1="170" y1="186" x2="230" y2="186" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,182 240,186 230,190" fill="currentColor"/>
  <rect x="240" y="174" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 4: 캐릭터</text>

  <!-- 비효율 결과 -->
  <text x="320" y="224" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 패스 전환 4회, 드로우콜 4회</text>

  <!-- ===== 효율적 섹션 ===== -->
  <rect x="20" y="270" width="600" height="232" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="320" y="290" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">[효율적] 같은 머티리얼끼리 정렬</text>

  <!-- Row 1: 패스 전환 A -->
  <rect x="40" y="302" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="318" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → A</text>
  <line x1="170" y1="314" x2="230" y2="314" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,310 240,314 230,318" fill="currentColor"/>
  <rect x="240" y="302" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="318" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 1: 나무</text>

  <!-- Row 2: 상태 유지 (패스 전환 없음) -->
  <rect x="40" y="334" width="130" height="24" rx="5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="105" y="350" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">패스 유지</text>
  <line x1="170" y1="346" x2="230" y2="346" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <polygon points="230,342 240,346 230,350" fill="currentColor" opacity="0.4"/>
  <rect x="240" y="334" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 2: 나무</text>
  <text x="420" y="350" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">← 패스 전환 불필요</text>

  <!-- Row 3: 패스 전환 B -->
  <rect x="40" y="366" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="382" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → B</text>
  <line x1="170" y1="378" x2="230" y2="378" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,374 240,378 230,382" fill="currentColor"/>
  <rect x="240" y="366" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="382" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 3: 건물</text>

  <!-- Row 4: 패스 전환 C -->
  <rect x="40" y="398" width="130" height="24" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="105" y="414" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">패스 전환 → C</text>
  <line x1="170" y1="410" x2="230" y2="410" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="230,406 240,410 230,414" fill="currentColor"/>
  <rect x="240" y="398" width="160" height="24" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="414" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 4: 캐릭터</text>

  <!-- 효율 결과 -->
  <text x="320" y="450" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 패스 전환 3회, 드로우콜 4회</text>

  <!-- 범례 -->
  <rect x="180" y="468" width="14" height="14" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>
  <text x="200" y="480" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">패스 전환 발생</text>
  <rect x="310" y="468" width="14" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="330" y="480" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">패스 유지 (비용 없음)</text>
</svg>
</div>

이어서 살펴볼 배칭 기법들은 드로우콜 수 또는 SetPass Call 수를 줄이는 것을 목표로 합니다.

---

## Static Batching

**Static Batching**은 움직이지 않는(Static으로 표시된) 오브젝트들의 메쉬를 빌드 시점에 하나의 큰 메쉬로 합치는 기법입니다.

같은 머티리얼을 사용하는 나무가 씬에 50그루 있다면, 배칭 없이는 50번의 드로우콜이 필요합니다. Static Batching을 적용하면 빌드 시점에 50그루의 메쉬가 하나로 합쳐져, 런타임에는 1번의 드로우콜로 모두 그릴 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 전체 배경 -->
  <rect x="0" y="0" width="540" height="420" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- === 적용 전 === -->
  <text x="270" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Static Batching 적용 전</text>
  <!-- 나무 1 -->
  <rect x="30" y="44" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="61" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 1</text>
  <line x1="120" y1="57" x2="200" y2="57" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,53 210,57 200,61" fill="currentColor"/>
  <rect x="210" y="44" width="110" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="61" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 1</text>
  <!-- 나무 2 -->
  <rect x="30" y="78" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 2</text>
  <line x1="120" y1="91" x2="200" y2="91" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,87 210,91 200,95" fill="currentColor"/>
  <rect x="210" y="78" width="110" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="95" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 2</text>
  <!-- 나무 3 -->
  <rect x="30" y="112" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 3</text>
  <line x1="120" y1="125" x2="200" y2="125" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,121 210,125 200,129" fill="currentColor"/>
  <rect x="210" y="112" width="110" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="129" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 3</text>
  <!-- 생략 -->
  <text x="75" y="157" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">⋮</text>
  <text x="265" y="157" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">⋮</text>
  <!-- 나무 50 -->
  <rect x="30" y="168" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 50</text>
  <line x1="120" y1="181" x2="200" y2="181" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="200,177 210,181 200,185" fill="currentColor"/>
  <rect x="210" y="168" width="110" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="185" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 50</text>
  <!-- 우측 브래킷 설명 -->
  <line x1="330" y1="50" x2="340" y2="50" stroke="currentColor" stroke-width="1.5"/>
  <line x1="340" y1="50" x2="340" y2="188" stroke="currentColor" stroke-width="1.5"/>
  <line x1="330" y1="188" x2="340" y2="188" stroke="currentColor" stroke-width="1.5"/>
  <text x="355" y="112" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">50번의 드로우콜</text>
  <text x="355" y="127" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(같은 머티리얼이지만</text>
  <text x="355" y="141" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">개별 메쉬이므로 개별 제출)</text>
  <!-- === 구분선 === -->
  <line x1="20" y1="210" x2="520" y2="210" stroke="currentColor" stroke-width="1.5" stroke-dasharray="6,4"/>
  <!-- === 적용 후 === -->
  <text x="270" y="238" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Static Batching 적용 후 (빌드 시점)</text>
  <!-- 나무들 -->
  <rect x="30" y="254" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="271" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 1</text>
  <rect x="30" y="286" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="303" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 2</text>
  <rect x="30" y="318" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="335" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 3</text>
  <text x="75" y="362" text-anchor="middle" font-family="sans-serif" font-size="13" fill="currentColor" opacity="0.5">⋮</text>
  <rect x="30" y="372" width="90" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="389" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">나무 50</text>
  <!-- 수렴 화살표들 -->
  <line x1="120" y1="267" x2="210" y2="330" stroke="currentColor" stroke-width="1.2"/>
  <line x1="120" y1="299" x2="210" y2="330" stroke="currentColor" stroke-width="1.2"/>
  <line x1="120" y1="331" x2="210" y2="330" stroke="currentColor" stroke-width="1.2"/>
  <line x1="120" y1="385" x2="210" y2="330" stroke="currentColor" stroke-width="1.2"/>
  <!-- 합친 메쉬 -->
  <rect x="210" y="316" width="110" height="30" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="2"/>
  <text x="265" y="335" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합친 메쉬</text>
  <!-- 드로우콜 1 -->
  <line x1="320" y1="331" x2="380" y2="331" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="380,327 390,331 380,335" fill="currentColor"/>
  <rect x="390" y="316" width="110" height="30" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="2"/>
  <text x="445" y="335" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 1</text>
  <!-- 설명 -->
  <text x="265" y="360" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">하나의 큰 메쉬로 합침</text>
  <text x="445" y="360" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">1번의 드로우콜로</text>
  <text x="445" y="373" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">50그루 모두 렌더링</text>
</svg>
</div>

<br>

### 작동 조건

첫째, 오브젝트의 Inspector에서 Static 체크박스 아래 **Batching Static** 플래그가 켜져 있어야 합니다. 이 플래그는 "이 오브젝트는 런타임에 이동하지 않는다"는 약속이므로, 엔진이 빌드 시점에 위치를 확정하고 메쉬를 합칠 수 있습니다.

둘째, **같은 머티리얼**을 사용해야 합니다. 머티리얼이 다르면 GPU 상태가 달라지므로, 하나의 드로우콜로 합칠 수 없습니다.

<br>

### 장점과 단점

장점은 **드로우콜 감소**입니다. CPU가 GPU에 보내는 드로우콜 수가 줄어들어 CPU 측 렌더링 준비 비용이 감소합니다. 메쉬를 합치는 작업이 빌드 시점에 끝나므로, 런타임에 추가 CPU 비용이 발생하지 않습니다.
또한 메쉬를 합친 뒤에도 개별 오브젝트 단위의 **Frustum Culling**을 지원하므로, 보이지 않는 오브젝트는 GPU에 제출되지 않습니다.

> 컬링 기법에 대해서는 [Part 3](/dev/unity/UnityPipeline-3/)에서 자세히 다룹니다.

<br>

단점은 **메모리 증가**입니다. 나무 50그루가 모두 같은 프리팹에서 만들어졌다면, 배칭 없이는 메쉬 데이터 하나만 메모리에 올리고 50번 재사용합니다. 각 인스턴스에는 위치, 회전, 스케일 정보(변환 행렬)만 저장하면 됩니다.
하지만 Static Batching을 적용하면 각 나무의 정점이 월드 좌표로 변환되어 하나의 큰 메쉬에 복사됩니다. 합쳐진 메쉬가 원본과 별도로 메모리에 상주하므로, 정점 데이터가 약 51배로 늘어납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 전체 배경 -->
  <rect x="0" y="0" width="520" height="340" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="260" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">메모리 사용 비교 (나무 1,000 정점 × 50그루)</text>
  <!-- === Static Batching 없이 === -->
  <rect x="20" y="46" width="480" height="120" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="68" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Static Batching 없이</text>
  <!-- 항목들 -->
  <text x="60" y="94" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">원본 메쉬:</text>
  <text x="200" y="94" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">1,000 정점</text>
  <text x="320" y="94" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(1개를 50번 재사용)</text>
  <text x="60" y="114" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">인스턴스:</text>
  <text x="200" y="114" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">변환 행렬 50개</text>
  <!-- 구분선 -->
  <line x1="50" y1="126" x2="470" y2="126" stroke="currentColor" stroke-width="1"/>
  <!-- 합계 -->
  <text x="60" y="148" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 합계:</text>
  <text x="200" y="148" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">1,000</text>
  <!-- 작은 바 차트 표현 -->
  <rect x="310" y="137" width="20" height="14" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <!-- === Static Batching 적용 === -->
  <rect x="20" y="180" width="480" height="146" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="202" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Static Batching 적용</text>
  <!-- 항목들 -->
  <text x="60" y="228" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">합친 메쉬:</text>
  <text x="200" y="228" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">50 × 1,000 = 50,000 정점</text>
  <text x="60" y="248" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">원본 메쉬:</text>
  <text x="200" y="248" text-anchor="start" font-family="sans-serif" font-size="11" fill="currentColor">1,000 정점</text>
  <text x="320" y="248" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(MeshFilter 참조로 메모리에 남음)</text>
  <!-- 구분선 -->
  <line x1="50" y1="260" x2="470" y2="260" stroke="currentColor" stroke-width="1"/>
  <!-- 합계 -->
  <text x="60" y="282" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 합계:</text>
  <text x="200" y="282" text-anchor="start" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">51,000</text>
  <!-- 큰 바 차트 표현 (51배) -->
  <rect x="310" y="271" width="160" height="14" rx="2" fill="currentColor" fill-opacity="0.25" stroke="currentColor" stroke-width="1"/>
  <!-- 비교 화살표 -->
  <text x="260" y="325" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">정점 데이터가 약 51배로 증가</text>
</svg>
</div>

메모리를 과도하게 사용하면, 오히려 메모리 부족으로 OS가 앱을 강제 종료하거나 다른 리소스의 로딩이 지연될 수 있습니다.

---

## Dynamic Batching

**Dynamic Batching**은 움직이는 오브젝트에도 배칭을 적용하기 위해, **런타임에 매 프레임** CPU가 작은 메쉬들을 합치는 방식입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="560" height="340" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="280" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Dynamic Batching — 매 프레임 CPU가 수행하는 작업</text>

  <!-- 단계 흐름 -->
  <!-- (1) -->
  <rect x="30" y="50" width="500" height="32" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="50" y="70" font-family="sans-serif" font-size="11" fill="currentColor">(1) 같은 머티리얼을 사용하는 작은 메쉬들을 찾음</text>
  <!-- 화살표 -->
  <line x1="280" y1="82" x2="280" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="276,92 280,100 284,92" fill="currentColor"/>

  <!-- (2) -->
  <rect x="30" y="100" width="500" height="32" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="120" font-family="sans-serif" font-size="11" fill="currentColor">(2) 각 메쉬의 정점을 로컬 좌표 → 월드 좌표로 변환 (행렬 곱셈)</text>
  <!-- 화살표 -->
  <line x1="280" y1="132" x2="280" y2="146" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="276,142 280,150 284,142" fill="currentColor"/>

  <!-- (3) -->
  <rect x="30" y="150" width="500" height="32" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="170" font-family="sans-serif" font-size="11" fill="currentColor">(3) 변환된 정점들을 하나의 버퍼에 합침</text>
  <!-- 화살표 -->
  <line x1="280" y1="182" x2="280" y2="196" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="276,192 280,200 284,192" fill="currentColor"/>

  <!-- (4) -->
  <rect x="30" y="200" width="500" height="32" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="2"/>
  <text x="50" y="220" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(4) 합친 메쉬를 하나의 드로우콜로 GPU에 제출</text>

  <!-- 구분선 -->
  <line x1="30" y1="256" x2="530" y2="256" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- 비교 -->
  <text x="280" y="280" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Static Batching → 빌드 시점에 1회</text>
  <text x="280" y="302" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Dynamic Batching → 매 프레임 반복</text>
  <text x="280" y="326" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(2)~(3)의 CPU 비용이 매 프레임 누적됨</text>
</svg>
</div>

<br>

매 프레임 모든 정점에 대해 로컬→월드 좌표 변환(행렬 곱셈)을 수행해야 하므로, 이 CPU 비용이 드로우콜 절약으로 얻는 이점보다 커지는 경우가 많습니다. 이 때문에 Dynamic Batching에는 엄격한 제한이 걸려 있습니다.

### 제한 사항

CPU가 매 프레임 처리해야 하는 데이터량은 정점 수와 정점당 속성(위치, 법선, UV 좌표 등) 수에 비례하므로, Unity는 두 가지 제한을 동시에 적용합니다.

정점 수는 **300개 이하**, 정점 속성 총합(정점 수 × 정점당 속성 수)은 **900개 이하**이며, 둘 중 먼저 도달하는 쪽이 실제 제한이 됩니다.

**Dynamic Batching 정점 제한 (정점 속성 총합 900 이하)**

| 속성 수 | 사용 속성 예시 | 최대 정점 |
| --- | --- | --- |
| 3개 | 위치 + 법선 + UV | 300 |
| 4개 | 위치 + 법선 + UV + 탄젠트 | 225 |
| 5개 | 위치 + 법선 + UV0 + UV1 + 탄젠트 | 180 |

<br>

정점 수 외에 추가 조건도 있습니다. 같은 머티리얼을 사용해야 하고, 스케일 유형도 일치해야 합니다.
균일 스케일(Uniform Scale, x·y·z 비율이 동일)과 비균일 스케일(Non-uniform Scale, 축마다 비율이 다름)은 법선 벡터 계산 방식이 달라, 같은 유형끼리만 배칭됩니다. 음수 스케일(미러링)은 배칭에서 제외됩니다.
라이트맵을 사용하는 경우에는 같은 라이트맵 인덱스와 같은 오프셋/스케일을 가져야 하고, 멀티패스 셰이더를 사용하는 오브젝트도 배칭 대상이 되지 않습니다.

### URP에서의 비활성화

제한이 엄격한 만큼 Dynamic Batching이 실제로 적용되는 상황은 한정적입니다. 300 정점 이하의 메쉬는 UI 요소나 단순한 파티클 정도에 국한되고, 적용되더라도 매 프레임 정점을 변환하는 CPU 비용이 드로우콜 절약 효과보다 큰 경우가 빈번합니다.

이런 이유로 **URP에서는 Dynamic Batching이 기본적으로 비활성화**되어 있으며, 대신 SRP Batcher를 기본 배칭 방식으로 사용합니다. URP Asset의 Inspector에서 Dynamic Batching을 강제로 활성화할 수는 있지만, SRP Batcher가 대부분의 상황에서 더 효율적입니다.

---

## SRP Batcher

**SRP Batcher**는 메쉬를 합쳐 드로우콜 수를 줄이는 대신, **드로우콜 사이의 GPU 상태 변경을 최소화**하여 CPU 측 비용을 줄이는 방식입니다. 드로우콜 수는 그대로지만 각 드로우콜의 준비 비용이 낮아집니다. URP와 HDRP의 기본 배칭 방식에 해당합니다.

### 기존 방식의 문제

기존 렌더링 방식에서는 머티리얼이 바뀔 때마다 해당 머티리얼의 속성 값(색상, 텍스처 오프셋, 반사 강도 등)을 CPU가 GPU 메모리에 새로 업로드합니다. 다양한 머티리얼이 교차하는 실제 씬에서는 이 전송이 빈번하게 발생하여 CPU 비용이 증가합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="720" height="520" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="360" y="30" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기존 방식: 드로우콜의 GPU 상태 설정 흐름</text>
  <!-- 컬럼 헤더 -->
  <text x="180" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU가 보내는 데이터</text>
  <text x="540" y="58" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU에서 일어나는 일</text>
  <line x1="40" y1="68" x2="320" y2="68" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <line x1="400" y1="68" x2="680" y2="68" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- 드로우콜 1 -->
  <rect x="30" y="80" width="290" height="120" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="175" y="100" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 1 (셰이더 A)</text>
  <!-- 셰이더 설정 -->
  <rect x="50" y="110" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 설정</text>
  <line x1="320" y1="122" x2="395" y2="122" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,118 405,122 395,126" fill="currentColor"/>
  <rect x="410" y="110" width="140" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 A 로드</text>
  <!-- 머티리얼 속성 -->
  <rect x="50" y="140" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="156" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 속성</text>
  <line x1="320" y1="152" x2="395" y2="152" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,148 405,152 395,156" fill="currentColor"/>
  <rect x="410" y="140" width="140" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="156" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">상수 버퍼 갱신</text>
  <!-- 변환 행렬 -->
  <rect x="50" y="170" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">오브젝트 변환 행렬</text>
  <line x1="320" y1="182" x2="395" y2="182" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,178 405,182 395,186" fill="currentColor"/>
  <rect x="410" y="170" width="200" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="510" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">변환 행렬 갱신 → 렌더링</text>

  <!-- 드로우콜 2 -->
  <rect x="30" y="215" width="290" height="120" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="175" y="235" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 2 (셰이더 A, 다른 머티리얼)</text>
  <!-- 셰이더 설정 -->
  <rect x="50" y="245" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="261" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 설정</text>
  <line x1="320" y1="257" x2="395" y2="257" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,253 405,257 395,261" fill="currentColor"/>
  <rect x="410" y="245" width="140" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="261" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 A 유지</text>
  <!-- 머티리얼 속성 -->
  <rect x="50" y="275" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="291" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 속성</text>
  <line x1="320" y1="287" x2="395" y2="287" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,283 405,287 395,291" fill="currentColor"/>
  <rect x="410" y="275" width="140" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="291" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">상수 버퍼 갱신</text>
  <!-- 변환 행렬 -->
  <rect x="50" y="305" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="321" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">오브젝트 변환 행렬</text>
  <line x1="320" y1="317" x2="395" y2="317" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,313 405,317 395,321" fill="currentColor"/>
  <rect x="410" y="305" width="200" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="510" y="321" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">변환 행렬 갱신 → 렌더링</text>
  <!-- 주석: DC2 전체에 대한 설명 -->
  <text x="175" y="345" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">머티리얼이 바뀌었으므로 속성 값을 CPU → GPU로 다시 전송</text>

  <!-- 드로우콜 3 -->
  <rect x="30" y="350" width="290" height="120" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="175" y="370" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 3 (셰이더 B)</text>
  <!-- 셰이더 설정 -->
  <rect x="50" y="380" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="396" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 설정</text>
  <line x1="320" y1="392" x2="395" y2="392" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,388 405,392 395,396" fill="currentColor"/>
  <rect x="410" y="380" width="140" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="396" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 B 로드</text>
  <!-- 머티리얼 속성 -->
  <rect x="50" y="410" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="426" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 속성</text>
  <line x1="320" y1="422" x2="395" y2="422" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,418 405,422 395,426" fill="currentColor"/>
  <rect x="410" y="410" width="140" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="480" y="426" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">상수 버퍼 갱신</text>
  <!-- 변환 행렬 -->
  <rect x="50" y="440" width="130" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="456" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">오브젝트 변환 행렬</text>
  <line x1="320" y1="452" x2="395" y2="452" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="395,448 405,452 395,456" fill="currentColor"/>
  <rect x="410" y="440" width="200" height="24" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="510" y="456" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">변환 행렬 갱신 → 렌더링</text>

  <!-- 하단 요약 -->
  <text x="360" y="498" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">머티리얼·셰이더 전환 시 해당 데이터를 CPU → GPU로 다시 전송</text>
</svg>
</div>

### SRP Batcher의 동작

기존 방식에서 이런 일이 발생하는 이유는, 머티리얼 속성을 저장하는 GPU의 **상수 버퍼(Constant Buffer, CBUFFER)**가 하나뿐이고, 머티리얼이 바뀔 때마다 덮어써지기 때문입니다.
상수 버퍼는 셰이더 실행 중 변하지 않는 데이터를 저장하는 GPU 메모리 영역으로, 머티리얼 A의 값을 올린 뒤 머티리얼 B를 그리면 같은 버퍼가 B의 값으로 교체됩니다. 머티리얼 A를 다시 그려야 할 때 A의 값은 이미 사라졌으므로, CPU가 처음부터 다시 업로드해야 합니다.

SRP Batcher는 머티리얼마다 별도의 CBUFFER를 GPU 메모리에 할당하여, 속성 값을 유지합니다. 머티리얼 A와 B가 각자의 CBUFFER에 동시에 상주하므로 서로 덮어쓰이지 않고, CPU는 머티리얼이 바뀔 때마다 데이터를 복사하는 대신 사용할 CBUFFER만 지정하면 됩니다.

머티리얼 수만큼 CBUFFER가 상주하므로 GPU 메모리 사용량은 늘어나지만, 머티리얼이 바뀔 때마다 CPU가 데이터를 재업로드하는 비용이 사라지는 것이 핵심 이점입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="600" height="280" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="300" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SRP Batcher — 머티리얼별 CBUFFER가 GPU 메모리에 상주</text>

  <!-- 머티리얼 A CBUFFER -->
  <rect x="30" y="55" width="160" height="55" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CBUFFER A</text>
  <text x="110" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">색상, UV 등</text>

  <!-- 머티리얼 B CBUFFER -->
  <rect x="220" y="55" width="160" height="55" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="300" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CBUFFER B</text>
  <text x="300" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">색상, UV 등</text>

  <!-- 머티리얼 C CBUFFER -->
  <rect x="410" y="55" width="160" height="55" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="490" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CBUFFER C</text>
  <text x="490" y="96" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">색상, UV 등</text>

  <!-- 상주 표시 -->
  <text x="300" y="132" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">각 머티리얼의 속성 값이 별도의 CBUFFER에 상주 — 서로 덮어쓰이지 않음</text>

  <!-- 구분선 -->
  <line x1="30" y1="148" x2="570" y2="148" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- 드로우콜 흐름 -->
  <text x="300" y="172" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 시 CPU가 하는 일</text>

  <!-- 기존 -->
  <text x="160" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">기존: 머티리얼 전환 시 속성 값을 복사하여 전송</text>
  <line x1="30" y1="210" x2="290" y2="210" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="160" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">CPU → GPU 데이터 전송 반복</text>

  <!-- SRP Batcher -->
  <text x="440" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">SRP Batcher: 사용할 CBUFFER만 지정</text>
  <line x1="310" y1="210" x2="570" y2="210" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="440" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">데이터 전송 없이 참조만 전달</text>

  <!-- 하단 요약 -->
  <text x="300" y="262" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU 메모리 사용량은 증가하지만, CPU 측 머티리얼 전환 비용이 크게 감소</text>
</svg>
</div>

<br>

기존 방식에서는 머티리얼이 바뀔 때마다 속성 값을 CPU에서 GPU로 복사해야 했지만, SRP Batcher에서는 GPU에 이미 상주하는 CBUFFER를 지정하기만 하면 되므로 머티리얼 전환에 따른 CPU 비용이 크게 줄어듭니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 480" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="720" height="480" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 제목 -->
  <text x="360" y="28" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">기존 방식 vs SRP Batcher (머티리얼 A, B를 사용하는 드로우콜 3회)</text>

  <!-- === 기존 방식 섹션 === -->
  <rect x="20" y="48" width="680" height="185" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="72" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">기존 방식</text>
  <!-- 헤더 라인 -->
  <text x="250" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">동작</text>
  <text x="570" y="72" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">CPU 동작</text>
  <line x1="35" y1="80" x2="685" y2="80" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- 드로우콜 1 -->
  <rect x="35" y="88" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 1</text>
  <text x="250" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 A 속성 → 상수 버퍼에 복사</text>
  <rect x="490" y="88" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="105" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">데이터 복사</text>
  <!-- 드로우콜 2 -->
  <rect x="35" y="122" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="139" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 2</text>
  <text x="250" y="139" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 B 속성 → 상수 버퍼에 복사</text>
  <rect x="490" y="122" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="139" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">데이터 복사</text>
  <!-- 드로우콜 3 -->
  <rect x="35" y="156" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="173" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 3</text>
  <text x="250" y="173" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 A 속성 → 상수 버퍼에 복사</text>
  <rect x="490" y="156" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="173" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">데이터 복사 (A를 다시)</text>
  <!-- 합계 -->
  <line x1="460" y1="192" x2="640" y2="192" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="550" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합계: 복사 3회</text>

  <!-- === SRP Batcher 섹션 === -->
  <rect x="20" y="248" width="680" height="215" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="272" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SRP Batcher</text>
  <!-- 헤더 라인 -->
  <text x="250" y="272" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">동작</text>
  <text x="570" y="272" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.6">CPU 동작</text>
  <line x1="35" y1="280" x2="685" y2="280" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <!-- 초기화 -->
  <rect x="35" y="288" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="80" y="305" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">초기화</text>
  <text x="250" y="305" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">A → CBUFFER A, B → CBUFFER B에 저장</text>
  <rect x="490" y="288" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="305" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">데이터 복사</text>
  <!-- 드로우콜 1 -->
  <rect x="35" y="322" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="339" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 1</text>
  <text x="250" y="339" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CBUFFER A 사용 지정</text>
  <rect x="490" y="322" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="339" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">CBUFFER 지정</text>
  <!-- 드로우콜 2 -->
  <rect x="35" y="356" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="373" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 2</text>
  <text x="250" y="373" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CBUFFER B 사용 지정</text>
  <rect x="490" y="356" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="373" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">CBUFFER 지정</text>
  <!-- 드로우콜 3 -->
  <rect x="35" y="390" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1"/>
  <text x="80" y="407" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">드로우콜 3</text>
  <text x="250" y="407" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CBUFFER A 사용 지정</text>
  <rect x="490" y="390" width="120" height="26" rx="4" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1"/>
  <text x="550" y="407" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">CBUFFER 지정</text>
  <!-- 합계 -->
  <line x1="460" y1="426" x2="640" y2="426" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="550" y="444" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합계: 복사 0회 (초기화 이후)</text>
</svg>
</div>

<br>

### SRP Batcher의 배칭 단위

하나의 셰이더는 기능 옵션의 조합에 따라 서로 다른 컴파일 버전인 **셰이더 variant(Shader Variant)**로 나뉩니다. 예를 들어 URP Lit 셰이더는 안개(Fog), 그림자 수신(Receive Shadows) 같은 기능을 켜거나 끌 수 있는데, 안개를 켠 Lit과 끈 Lit은 서로 다른 variant입니다.
같은 셰이더라도 variant가 다르면 GPU 입장에서는 별개의 프로그램이므로 패스 전환이 발생합니다.

SRP Batcher는 이 셰이더 variant를 배칭의 기준으로 사용합니다. 앞에서 살펴본 것처럼 머티리얼마다 별도의 CBUFFER가 GPU에 상주하므로, 머티리얼이 달라도 데이터를 재업로드할 필요 없이 CBUFFER만 전환하면 됩니다.
따라서 **같은 셰이더 variant**를 사용하는 드로우콜은 머티리얼이 달라도 하나의 배치로 묶입니다.
같은 variant끼리 묶이면 셰이더 패스 전환은 원래 발생하지 않고, 머티리얼 속성도 각자의 CBUFFER에 이미 상주하므로 재업로드가 필요 없습니다. 드로우콜 자체가 합쳐지는 것은 아니지만, 배치 안에서 머티리얼 전환 비용이 사라지는 것이 핵심입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SRP Batcher의 배칭 단위: 셰이더 variant</text>

  <!-- Batch 1 group -->
  <rect x="20" y="44" width="580" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SRP 배치 1 — 셰이더 variant A</text>
  <!-- Column headers -->
  <text x="60" y="90" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">드로우콜</text>
  <text x="220" y="90" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">머티리얼</text>
  <text x="440" y="90" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU 상태</text>
  <line x1="40" y1="96" x2="580" y2="96" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Row 1 -->
  <rect x="40" y="102" width="540" height="24" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="118" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 1</text>
  <text x="220" y="118" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼 A (빨간색 나무)</text>
  <text x="440" y="118" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">SetPass (셰이더 A)</text>
  <!-- Row 2 -->
  <text x="60" y="144" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 2</text>
  <text x="220" y="144" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼 B (파란색 나무)</text>
  <text x="440" y="144" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">CBUFFER만 변경</text>
  <!-- Row 3 -->
  <rect x="40" y="152" width="540" height="24" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="168" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 3</text>
  <text x="220" y="168" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼 C (초록색 나무)</text>
  <text x="440" y="168" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">CBUFFER만 변경</text>

  <!-- Batch 2 group -->
  <rect x="20" y="200" width="580" height="114" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="222" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SRP 배치 2 — 셰이더 variant B</text>
  <!-- Column headers -->
  <text x="60" y="246" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">드로우콜</text>
  <text x="220" y="246" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">머티리얼</text>
  <text x="440" y="246" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU 상태</text>
  <line x1="40" y1="252" x2="580" y2="252" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Row 4 -->
  <rect x="40" y="258" width="540" height="24" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="274" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 4</text>
  <text x="220" y="274" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼 D (투명 유리)</text>
  <text x="440" y="274" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">SetPass (셰이더 B)</text>
  <!-- Row 5 -->
  <text x="60" y="300" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 5</text>
  <text x="220" y="300" font-family="sans-serif" font-size="11" fill="currentColor">머티리얼 E (투명 물)</text>
  <text x="440" y="300" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">CBUFFER만 변경</text>

  <!-- Summary -->
  <rect x="170" y="332" width="280" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="353" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">드로우콜 5회, SetPass Call 2회</text>
</svg>
</div>

<br>

Static Batching과 Dynamic Batching은 같은 머티리얼이어야 배칭할 수 있었습니다. SRP Batcher는 셰이더 variant만 일치하면 되므로, 머티리얼 종류가 다양한 씬에서도 효과적으로 배칭됩니다.

### 장점과 단점

앞에서 살펴본 것처럼 CBUFFER 상주를 통해 **머티리얼 전환 비용이 크게 감소**합니다.
메쉬를 합치지 않기 때문에 Static Batching과 달리 **메쉬 복제로 인한 메모리 증가가 없고**, **움직이는 오브젝트에도 동작**합니다.
Dynamic Batching처럼 매 프레임 정점을 변환하는 작업도 필요 없어 **런타임 CPU 비용이 추가되지 않습니다**.

반면, 머티리얼 수만큼 CBUFFER가 GPU 메모리에 상주하므로 **머티리얼 종류가 많을수록 GPU 메모리 사용량이 증가**합니다.

### 작동 조건

첫째, **SRP 호환 셰이더**를 사용해야 합니다. URP/HDRP에 포함된 Lit, Unlit 등의 기본 셰이더는 이미 호환됩니다. 커스텀 셰이더의 경우, 앞에서 설명한 머티리얼별 CBUFFER에 해당하는 `UnityPerMaterial`과 오브젝트별 데이터(변환 행렬 등)를 담는 `UnityPerDraw`를 셰이더 코드에 올바르게 선언해야 합니다. Inspector에서 셰이더를 선택하면 "SRP Batcher: compatible" 표시로 호환 여부를 확인할 수 있습니다.

둘째, URP Asset의 Inspector에서 **SRP Batcher가 활성화**되어 있어야 합니다. URP에서는 기본적으로 활성화 상태입니다.

---

## GPU Instancing

**GPU Instancing**은 같은 메쉬와 머티리얼을 사용하는 오브젝트가 여러 개일 때, 하나의 드로우콜로 한꺼번에 그리는 기법입니다. 이때 같은 메쉬를 공유하는 개별 오브젝트를 각각 **인스턴스(Instance)**라 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 480" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU Instancing (나무 메쉬 A · 같은 머티리얼 × 100개)</text>

  <!-- Without Instancing -->
  <rect x="20" y="44" width="580" height="195" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Instancing 없이</text>
  <line x1="40" y1="76" x2="580" y2="76" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
  <!-- Rows -->
  <rect x="40" y="82" width="540" height="22" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="97" font-family="sans-serif" font-size="11" fill="currentColor">나무 A</text>
  <text x="200" y="97" font-family="sans-serif" font-size="11" fill="currentColor">위치(0,0,0)</text>
  <text x="460" y="97" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 1</text>

  <text x="60" y="119" font-family="sans-serif" font-size="11" fill="currentColor">나무 A</text>
  <text x="200" y="119" font-family="sans-serif" font-size="11" fill="currentColor">위치(5,0,0)</text>
  <text x="460" y="119" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 2</text>

  <rect x="40" y="126" width="540" height="22" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="141" font-family="sans-serif" font-size="11" fill="currentColor">나무 A</text>
  <text x="200" y="141" font-family="sans-serif" font-size="11" fill="currentColor">위치(10,0,0)</text>
  <text x="460" y="141" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 3</text>

  <!-- Dots -->
  <text x="260" y="163" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">⋮</text>
  <text x="490" y="163" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">⋮</text>

  <rect x="40" y="170" width="540" height="22" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="185" font-family="sans-serif" font-size="11" fill="currentColor">나무 A</text>
  <text x="200" y="185" font-family="sans-serif" font-size="11" fill="currentColor">위치(500,0,0)</text>
  <text x="460" y="185" font-family="sans-serif" font-size="11" fill="currentColor">드로우콜 100</text>

  <!-- Without total -->
  <text x="460" y="222" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">합계: 100회</text>

  <!-- With Instancing -->
  <rect x="20" y="254" width="580" height="190" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="278" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU Instancing</text>
  <line x1="40" y1="286" x2="580" y2="286" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>

  <!-- Mesh data row -->
  <rect x="40" y="294" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="60" y="312" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">메쉬 데이터</text>
  <text x="200" y="312" font-family="sans-serif" font-size="11" fill="currentColor">나무 A (100개가 공유)</text>

  <!-- Instance buffer -->
  <text x="60" y="340" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">인스턴스 버퍼</text>
  <rect x="200" y="328" width="360" height="22" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="210" y="343" font-family="sans-serif" font-size="10" fill="currentColor">#1  변환 행렬, 색상</text>
  <text x="210" y="363" font-family="sans-serif" font-size="10" fill="currentColor">#2  변환 행렬, 색상</text>
  <rect x="200" y="368" width="360" height="18" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="210" y="381" font-family="sans-serif" font-size="10" fill="currentColor">#3  변환 행렬, 색상</text>
  <text x="310" y="400" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">⋮</text>
  <rect x="200" y="404" width="360" height="18" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="210" y="417" font-family="sans-serif" font-size="10" fill="currentColor">#100  변환 행렬, 색상</text>

  <!-- With total -->
  <text x="460" y="450" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">합계: 1회</text>
</svg>
</div>

<br>

GPU Instancing의 핵심은 GPU가 메쉬 데이터를 한 번만 읽고, 각 인스턴스를 다른 위치·회전·스케일로 반복 렌더링하는 것입니다. 셰이더에서 인스턴스 프로퍼티를 선언하면 색상이나 밝기 같은 속성도 인스턴스별로 다르게 지정할 수 있습니다.

### 동작 방식

일반 렌더링에서는 오브젝트마다 드로우콜이 하나씩 필요합니다. GPU Instancing에서는 모든 인스턴스의 변환 행렬·속성을 하나의 **인스턴스 버퍼**로 묶어, 단일 드로우콜로 N개를 한꺼번에 렌더링합니다. GPU는 같은 메쉬를 반복 사용하면서 인스턴스 버퍼에서 1번, 2번, …, N번 데이터를 각각 적용합니다.
메쉬 자체가 복제되지 않으므로, Static Batching이 나무 50그루를 합쳐 정점 50,000개로 늘리는 것과 달리 원본 메쉬(1,000 정점)만 GPU에 유지됩니다.

### 적합한 상황

GPU Instancing은 같은 메쉬가 많이 반복될수록 효과가 큽니다.
숲의 나무, 풀, 돌처럼 같은 에셋이 수백~수천 개 배치되는 환경이 대표적이며, 전략 게임의 유닛이나 총알 같은 반복 오브젝트에도 적합합니다.
반면 같은 메쉬가 2~3개뿐이라면, 인스턴스 버퍼를 준비하는 비용에 비해 드로우콜 절약이 적어 효과가 미미합니다.

### SRP Batcher와의 관계

GPU Instancing과 SRP Batcher는 같은 머티리얼에 **동시에 적용할 수 없습니다**. 두 기법이 CBUFFER를 사용하는 방식이 서로 달라, 하나의 머티리얼이 두 구조를 동시에 만족할 수 없기 때문입니다.

기본적으로 SRP Batcher가 우선 적용됩니다. 동일 메쉬가 대량 반복되는 머티리얼만 Inspector에서 "Enable GPU Instancing"을 켜면, 해당 머티리얼이 SRP Batcher 대신 GPU Instancing으로 동작합니다.

---

## 배칭 기법 비교

| 항목 | Static Batching | Dynamic Batching | SRP Batcher | GPU Instancing |
| --- | --- | --- | --- | --- |
| 배칭 방식 | 빌드 시 메쉬 합침 | 매 프레임 합침 | 합치지 않음 | 합치지 않음 |
| 머티리얼 조건 | 같은 머티리얼 | 같은 머티리얼 | 같은 셰이더 variant | 같은 머티리얼 |
| 메쉬 제한 | 없음 | 최대 300 정점 | 없음 | 같은 메쉬 |
| 움직이는 오브젝트 | 불가 | 가능 | 가능 | 가능 |
| 메모리 증가 | 있음 (메쉬 복제) | 없음 | 있음 (CBUFFER 상주) | 없음 |
| 런타임 CPU 비용 | 없음 (빌드 시점) | 있음 (매 프레임) | 없음 | 없음 |
| URP 기본 상태 | 활성화 | 비활성화 | 활성화 | 비활성화 (SRP Batcher 우선) |

<br>

URP 환경에서는 SRP Batcher를 기본 전략으로 유지합니다. 머티리얼이나 메쉬의 종류에 관계없이 셰이더 variant만 일치하면 배칭되므로, 대부분의 씬에서 별도 설정 없이 머티리얼 전환 비용이 줄어듭니다.

여기에 보완적으로, 움직이지 않는 배경 오브젝트 중 같은 머티리얼을 공유하며 메모리 증가를 감수할 수 있는 경우에는 Static Batching을, 동일 메쉬가 수백 개 이상 반복되는 상황에서는 GPU Instancing을 적용합니다.
Dynamic Batching은 SRP Batcher가 이미 머티리얼 전환 비용을 크게 낮추므로, 매 프레임 정점을 변환하는 추가 비용 대비 실익이 적어 URP에서는 기본 비활성화 상태입니다.

## 드로우콜 흐름 요약

지금까지 다룬 개념들이 실제 렌더링에서 어떤 순서로 동작하는지 정리해보면 다음과 같습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 560" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">프레임의 렌더링 과정</text>

  <!-- CPU section -->
  <rect x="20" y="44" width="580" height="280" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="68" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">CPU</text>
  <line x1="70" y1="60" x2="580" y2="60" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- CPU Step 1 -->
  <rect x="40" y="80" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="97" font-family="sans-serif" font-size="11" fill="currentColor">1. 씬의 오브젝트 수집</text>

  <!-- CPU Step 2 -->
  <rect x="40" y="112" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="129" font-family="sans-serif" font-size="11" fill="currentColor">2. 가시성 판단 (카메라에 보이는 오브젝트 선별)</text>

  <!-- CPU Step 3 -->
  <rect x="40" y="144" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="161" font-family="sans-serif" font-size="11" fill="currentColor">3. 정렬 (머티리얼/셰이더 기준)</text>

  <!-- CPU Step 4 - Batching with sub-items -->
  <rect x="40" y="176" width="540" height="100" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="195" font-family="sans-serif" font-size="11" fill="currentColor">4. 배칭 적용</text>
  <!-- Sub-items -->
  <rect x="80" y="204" width="480" height="22" rx="3" fill="currentColor" fill-opacity="0.05"/>
  <text x="96" y="219" font-family="sans-serif" font-size="10" fill="currentColor">SRP Batcher</text>
  <text x="260" y="219" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">같은 셰이더 variant → 머티리얼 전환 비용 최소화</text>
  <rect x="80" y="230" width="480" height="22" rx="3" fill="currentColor" fill-opacity="0.05"/>
  <text x="96" y="245" font-family="sans-serif" font-size="10" fill="currentColor">Static Batching</text>
  <text x="260" y="245" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">정적 오브젝트 메쉬 합침</text>
  <rect x="80" y="256" width="480" height="22" rx="3" fill="currentColor" fill-opacity="0.05"/>
  <text x="96" y="271" font-family="sans-serif" font-size="10" fill="currentColor">GPU Instancing</text>
  <text x="260" y="271" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">같은 메쉬 인스턴스 묶음</text>

  <!-- CPU Step 5 -->
  <rect x="40" y="282" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="299" font-family="sans-serif" font-size="11" fill="currentColor">5. 드로우콜 생성 및 GPU에 제출</text>

  <!-- Arrow from CPU to GPU -->
  <line x1="310" y1="324" x2="310" y2="354" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="304,348 310,360 316,348" fill="currentColor"/>

  <!-- GPU section -->
  <rect x="20" y="364" width="580" height="186" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="388" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU</text>
  <line x1="70" y1="380" x2="580" y2="380" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- GPU Step 1 -->
  <rect x="40" y="398" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="415" font-family="sans-serif" font-size="11" fill="currentColor">1. 상태 변경 (SetPass)</text>

  <!-- GPU Step 2 -->
  <rect x="40" y="430" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="447" font-family="sans-serif" font-size="11" fill="currentColor">2. 정점 처리</text>

  <!-- GPU Step 3 -->
  <rect x="40" y="462" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="479" font-family="sans-serif" font-size="11" fill="currentColor">3. 래스터화</text>

  <!-- GPU Step 4 -->
  <rect x="40" y="494" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="511" font-family="sans-serif" font-size="11" fill="currentColor">4. 프래그먼트 처리</text>

  <!-- GPU Step 5 -->
  <rect x="40" y="526" width="540" height="26" rx="3" fill="currentColor" fill-opacity="0.04"/>
  <text x="56" y="543" font-family="sans-serif" font-size="11" fill="currentColor">5. 프레임 버퍼에 기록</text>
</svg>
</div>

<br>

다이어그램에서 "배칭 적용" 단계가 CPU 쪽에 위치하는 이유는, 배칭이 CPU에서 드로우콜을 묶거나 상태 변경 비용을 줄이는 작업이기 때문입니다.

---

## 마무리

- 드로우콜은 CPU가 GPU에 보내는 렌더링 명령이며, 실제 비용은 드로우콜 직전의 GPU 상태 변경을 CPU가 준비하고 전달하는 과정에서 발생합니다.
- SRP Batcher는 머티리얼 속성을 GPU의 CBUFFER에 유지하여 머티리얼 전환 비용을 줄이며, URP의 기본 배칭 전략입니다.
- Static Batching은 빌드 시점에 메쉬를 합쳐 드로우콜을 줄이지만, 정점 데이터 복제로 메모리가 증가합니다.
- GPU Instancing은 동일 메쉬가 수백 개 이상 반복되는 상황에서 효과적이지만, 같은 머티리얼에 SRP Batcher와 동시에 적용할 수 없습니다.

이 글에서는 GPU에 렌더링 명령을 보내는 비용, 즉 "어떻게" 보내는지를 다뤘습니다. 그러나 비용을 줄이는 것만큼, 화면에 보이지 않는 오브젝트를 GPU에 아예 제출하지 않는 것도 중요합니다. [Part 3](/dev/unity/UnityPipeline-3/)에서는 "무엇을" 보낼지를 줄이는 방법, 즉 GPU에 제출할 오브젝트 수 자체를 줄이는 컬링(Culling)과 거리에 따라 메쉬 복잡도를 낮추는 LOD 시스템을 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**시리즈**
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- **Unity 렌더 파이프라인 (2) - 드로우콜과 배칭** (현재 글)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- **Unity 렌더 파이프라인 (2) - 드로우콜과 배칭** (현재 글)
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
