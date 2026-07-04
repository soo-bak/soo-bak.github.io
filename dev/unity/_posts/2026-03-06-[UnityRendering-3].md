---
layout: single
title: "Unity 렌더링 (3) - Render Pipeline 개요 - soo:bak"
date: "2026-03-06 21:09:00 +0900"
description: URP를 중심으로 한 Unity Render Pipeline 선택 기준과 Built-in, HDRP, Custom SRP의 위치를 설명합니다.
tags:
  - Unity
  - 렌더링
  - URP
  - HDRP
  - SRP
  - 모바일
---

## 렌더 파이프라인이라는 상위 구조

[Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)에서는 카메라가 무엇을 어떤 순서로 그리는지를 다루었습니다. [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)에서는 그 결과가 어느 버퍼에 저장되고, 그 버퍼가 메모리와 대역폭에 어떤 비용을 만드는지 살펴보았습니다.

실제 엔진에서 이 과정은 따로 떨어져 실행되지 않습니다. 한 프레임 안에서 카메라 수집, 컬링, 조명과 그림자 준비, 불투명과 반투명 렌더링, Render Target 기록, 후처리가 정해진 순서로 이어집니다. 이 전체 흐름을 묶는 상위 규칙이 **렌더 파이프라인(Render Pipeline)**입니다.

렌더 파이프라인은 단순한 옵션 묶음이 아닙니다. 파이프라인이 달라지면 조명 계산 방식, 셰이더와 머티리얼 구조, 후처리 시스템, Render Target 구성, 커스텀 렌더 패스를 삽입하는 방식까지 함께 달라집니다. 결국 파이프라인 선택은 화면 품질뿐 아니라 CPU/GPU 비용, 지원 플랫폼, 이후 확장 방식까지 결정합니다.

이 선택은 프로젝트 중간에 바꾸기 어렵습니다. 파이프라인을 옮기면 머티리얼 변환, 셰이더 수정, 라이팅과 후처리 재설정, 커스텀 렌더링 코드 이전이 따라옵니다. 프로젝트가 커질수록 이 비용은 단순한 작업량을 넘어 구조적 리스크가 됩니다.

따라서 이 글은 렌더 파이프라인을 나열식으로 비교하지 않습니다. Built-in은 레거시와 이전 대상으로, HDRP는 고품질 요구가 분명할 때의 제한적 선택지로, Custom SRP는 특수한 직접 구현 선택지로 위치를 좁혀 봅니다. 중심은 URP입니다. 새 프로젝트에서 왜 URP가 기본 출발점이 되는지, 어떤 경우에만 다른 선택지를 검토해야 하는지를 기준으로 흐름을 잡습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 660 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; width: 100%;">
  <!-- Title -->
  <text x="330" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">새 프로젝트 기준의 렌더 파이프라인 선택</text>

  <!-- URP center -->
  <rect x="190" y="48" width="280" height="82" rx="5" fill="currentColor" fill-opacity="0.13" stroke="currentColor" stroke-width="2"/>
  <text x="330" y="74" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">URP</text>
  <text x="330" y="94" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Universal Render Pipeline</text>
  <text x="330" y="114" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">새 프로젝트의 기본 출발점 · 개발 집중</text>

  <!-- SRP base -->
  <rect x="140" y="154" width="380" height="54" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="176" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SRP 기반</text>
  <text x="330" y="196" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">렌더링 루프를 C#으로 구성하는 공통 프레임워크</text>

  <!-- Side boxes -->
  <rect x="20" y="230" width="190" height="52" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="115" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Built-in</text>
  <text x="115" y="270" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">Deprecated · 기존 프로젝트 유지/이전 대상</text>

  <rect x="235" y="230" width="190" height="52" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="330" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">HDRP</text>
  <text x="330" y="270" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">고품질 PC/콘솔 · 제한적 검토</text>

  <rect x="450" y="230" width="190" height="52" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="545" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Custom SRP</text>
  <text x="545" y="270" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.65">특수한 렌더러를 직접 구현할 때</text>
</svg>
</div>

<br>

그림에서 먼저 볼 것은 중심이 URP라는 점입니다. SRP는 URP가 동작하는 기반이고, Built-in은 그 기반이 왜 필요해졌는지를 보여 주는 이전 구조입니다. HDRP와 Custom SRP는 일반적인 출발점이 아니라, URP로 요구를 해결하기 어려운 특정 상황에서만 검토할 선택지입니다.

---

## Built-in Render Pipeline: 레거시 배경

Built-in Render Pipeline은 Unity가 오래 사용해 온 이전 세대의 렌더 파이프라인입니다. 기존 프로젝트, 오래된 튜토리얼, 에셋 스토어 자료에는 여전히 Built-in 기준 설명이 많이 남아 있습니다. 그래서 구조를 알아 둘 필요는 있지만, 새 프로젝트의 기본 선택지로 길게 검토할 대상은 아닙니다.

가장 큰 차이는 렌더링 루프가 엔진 내부에 고정되어 있다는 점입니다. 컬링, 정렬, 라이팅 패스, 드로우콜 생성 순서를 개발자가 직접 재구성하기 어렵습니다. `OnPreRender`, `OnPostRender`, `CommandBuffer` 같은 확장 지점은 있지만, 이미 정해진 흐름 사이에 명령을 덧붙이는 방식에 가깝습니다.

성능 특성도 명확합니다. Built-in Forward는 추가 픽셀 라이트가 늘어날수록 오브젝트를 여러 번 다시 그리는 멀티패스 구조입니다. 조명이 적은 장면에서는 단순하지만, 조명이 많아지면 드로우콜이 빠르게 늘어 CPU 비용이 커집니다. Built-in Deferred는 이 문제를 줄일 수 있지만, G-Buffer를 위해 여러 Render Target을 사용하므로 메모리와 대역폭 부담이 따라옵니다.

셰이더도 Built-in에 묶입니다. Surface Shader처럼 Built-in 전용 작성 방식으로 만든 셰이더와 머티리얼은 URP로 그대로 옮길 수 없습니다. 기존 프로젝트를 이전하려면 셰이더 교체, 머티리얼 변환, 라이팅 재설정 비용을 함께 계산해야 합니다.

따라서 여기서 Built-in은 추천 후보가 아니라 **SRP가 왜 필요해졌는지를 보여 주는 배경**으로 다룹니다. 고정된 렌더링 루프를 벗어나고, SRP Batcher와 Render Graph 같은 구조적 최적화를 활용하기 위해 Unity가 도입한 기반이 바로 SRP입니다.

---

## SRP (Scriptable Render Pipeline)

SRP는 Built-in처럼 완성된 렌더 파이프라인의 이름이 아니라, 렌더 파이프라인을 만들기 위한 프레임워크입니다. 엔진 내부에 고정되어 있던 컬링, 정렬, 드로우콜 생성, Render Target 설정 흐름을 C# 코드에서 구성할 수 있게 해 주는 기반입니다.

이 기반 위에 실제 프로젝트에서 사용하는 파이프라인이 올라갑니다. URP는 SRP 위에 만들어진 Unity의 주된 공식 구현체이고, Custom SRP는 같은 기반을 사용해 프로젝트가 직접 렌더링 루프를 작성하는 방식입니다. 따라서 SRP를 이해한다는 것은 특정 파이프라인 하나를 외우는 것이 아니라, Unity가 한 프레임의 렌더링 명령을 어떤 구조로 조립하는지 보는 일에 가깝습니다.

### SRP의 기본 구성 요소

SRP의 실행 흐름은 세 역할로 나뉩니다. 프로젝트가 어떤 파이프라인을 사용할지 지정하는 `RenderPipelineAsset`, 한 프레임의 렌더링 순서를 실제로 구현하는 `RenderPipeline`, 그리고 그 과정에서 만들어진 명령을 Unity 렌더링 시스템에 제출하는 `ScriptableRenderContext`입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Class 1: RenderPipelineAsset -->
  <rect x="60" y="12" width="400" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="36" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">RenderPipelineAsset</text>
  <text x="260" y="56" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">ScriptableObject를 상속</text>
  <text x="80" y="78" font-family="sans-serif" font-size="11" fill="currentColor">프로젝트 설정에서 파이프라인을 지정하는 에셋</text>
  <text x="80" y="100" font-family="monospace" font-size="11" fill="currentColor">CreatePipeline()</text>
  <text x="226" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">파이프라인 인스턴스 생성</text>
  <!-- Arrow 1 → 2 with label -->
  <line x1="260" y1="112" x2="260" y2="162" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,159 260,169 266,159" fill="currentColor"/>
  <text x="268" y="142" text-anchor="start" font-family="monospace" font-size="9" fill="currentColor" opacity="0.55">CreatePipeline()</text>
  <!-- Class 2: RenderPipeline -->
  <rect x="60" y="170" width="400" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="194" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">RenderPipeline</text>
  <text x="260" y="214" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">렌더링 루프의 실제 구현</text>
  <text x="80" y="238" font-family="monospace" font-size="11" fill="currentColor">Render(ScriptableRenderContext, List&lt;Camera&gt;)</text>
  <text x="80" y="258" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">매 프레임 호출되어 렌더링 명령을 구성</text>
  <!-- Arrow 2 → 3 with label -->
  <line x1="260" y1="270" x2="260" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,317 260,327 266,317" fill="currentColor"/>
  <text x="268" y="300" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Render() 내부에서 사용</text>
  <!-- Class 3: ScriptableRenderContext -->
  <rect x="60" y="328" width="400" height="105" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="352" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">ScriptableRenderContext</text>
  <text x="260" y="372" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">GPU에 명령을 제출하는 인터페이스</text>
  <text x="80" y="395" font-family="monospace" font-size="11" fill="currentColor">DrawRenderers()</text>
  <text x="230" y="395" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">오브젝트 렌더링</text>
  <text x="80" y="413" font-family="monospace" font-size="11" fill="currentColor">ExecuteCommandBuffer()</text>
  <text x="274" y="413" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">커스텀 명령 실행</text>
  <text x="80" y="431" font-family="monospace" font-size="11" fill="currentColor">Submit()</text>
  <text x="160" y="431" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">누적된 명령을 GPU에 제출</text>
</svg>
</div>

<br>

먼저 프로젝트 설정에는 `RenderPipelineAsset`이 등록됩니다. 이 에셋은 파이프라인의 설정값을 담고 있으며, Unity가 렌더링을 시작할 때 `CreatePipeline()`을 통해 실제 실행 객체인 `RenderPipeline`을 만듭니다.

프레임이 시작되면 Unity는 이 `RenderPipeline`의 `Render()` 메서드를 호출합니다. 파이프라인 구현은 이 안에서 카메라를 순회하고, 컬링과 정렬을 수행하고, 어떤 Render Target에 어떤 순서로 그릴지 결정합니다. 이렇게 구성한 명령은 `ScriptableRenderContext`에 쌓인 뒤 `Submit()`을 통해 Unity 렌더링 시스템으로 전달됩니다.

### SRP Batcher

SRP가 가져온 중요한 최적화 중 하나가 **SRP Batcher**입니다. 이름에는 Batcher가 붙어 있지만, Built-in의 Static Batching이나 Dynamic Batching처럼 여러 메쉬를 하나로 합쳐 드로우콜 수를 줄이는 방식은 아닙니다.

SRP Batcher의 초점은 드로우콜 사이의 **상태 전환 비용**입니다. CPU는 드로우콜을 보낼 때 셰이더 프로그램, 머티리얼 속성, 오브젝트별 상수 버퍼 같은 GPU 상태를 맞춰야 합니다. 같은 셰이더 배리언트를 쓰는 오브젝트가 이어져도 이 설정을 매번 반복하면, 화면에 그리는 일보다 상태를 준비하는 데 CPU 시간이 더 많이 쓰일 수 있습니다.

SRP Batcher는 이 비용을 줄이기 위해 셰이더 배리언트별 상태를 재사용하고, 머티리얼 데이터를 정해진 CBUFFER 구조로 GPU 메모리에 유지합니다. 드로우콜 수 자체는 그대로 남지만, 드로우콜마다 다시 설정해야 하는 항목이 줄어 CPU 오버헤드가 낮아집니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 720 500" xmlns="http://www.w3.org/2000/svg" style="max-width: 720px; width: 100%;">
  <text x="360" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SRP Batcher의 동작 원리</text>
  <rect x="15" y="40" width="335" height="370" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="182" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">기존 방식 (SRP Batcher 없음)</text>
  <text x="30" y="88" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 1</text>
  <rect x="30" y="95" width="145" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="111" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 A 설정</text>
  <rect x="182" y="95" width="152" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="258" y="111" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 속성 업로드</text>
  <rect x="55" y="125" width="110" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">메쉬 바인딩</text>
  <rect x="180" y="125" width="70" height="24" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Draw</text>
  <text x="30" y="172" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 2</text>
  <rect x="30" y="179" width="145" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 A 설정</text>
  <rect x="182" y="179" width="152" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="258" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 속성 업로드</text>
  <rect x="55" y="209" width="110" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="225" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">메쉬 바인딩</text>
  <rect x="180" y="209" width="70" height="24" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="225" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Draw</text>
  <text x="30" y="256" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 3</text>
  <rect x="30" y="263" width="145" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="102" y="279" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 B 설정</text>
  <rect x="182" y="263" width="152" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="258" y="279" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">머티리얼 속성 업로드</text>
  <rect x="55" y="293" width="110" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="110" y="309" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">메쉬 바인딩</text>
  <rect x="180" y="293" width="70" height="24" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="215" y="309" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Draw</text>
  <text x="182" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">같은 셰이더라도 매번 전체 상태를 재설정</text>
  <rect x="370" y="40" width="335" height="370" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="537" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SRP Batcher 활성화</text>
  <text x="385" y="88" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 1</text>
  <rect x="385" y="95" width="135" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="452" y="111" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 A 설정</text>
  <rect x="528" y="95" width="135" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="595" y="111" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CBUFFER 바인딩</text>
  <rect x="490" y="125" width="70" height="24" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Draw</text>
  <text x="385" y="172" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 2</text>
  <rect x="385" y="179" width="135" height="24" rx="4" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.3"/>
  <text x="452" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.3">셰이더 A 유지 (생략)</text>
  <rect x="528" y="179" width="135" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="595" y="195" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CBUFFER 바인딩</text>
  <rect x="490" y="209" width="70" height="24" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="225" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Draw</text>
  <text x="385" y="256" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">드로우콜 3</text>
  <rect x="385" y="263" width="135" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="452" y="279" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">셰이더 B 설정</text>
  <rect x="528" y="263" width="135" height="24" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="595" y="279" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">CBUFFER 바인딩</text>
  <rect x="490" y="293" width="70" height="24" rx="4" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="525" y="309" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Draw</text>
  <text x="537" y="340" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">같은 셰이더 배리언트 → 상태 전환 생략</text>
  <text x="537" y="356" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">머티리얼 속성은 Persistent CBUFFER에 미리 업로드</text>
  <rect x="15" y="420" width="690" height="40" rx="5" fill="currentColor" fill-opacity="0.04" stroke="none"/>
  <rect x="35" y="433" width="28" height="13" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.35"/>
  <text x="72" y="444" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">= 생략되는 단계</text>
  <rect x="200" y="433" width="28" height="13" rx="3" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="237" y="444" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">= 실행되는 단계</text>
  <rect x="380" y="433" width="28" height="13" rx="3" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.5"/>
  <text x="417" y="444" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">= GPU 드로우 호출</text>
</svg>
</div>

<br>

SRP Batcher가 동작하려면 셰이더가 정해진 메모리 배치 규칙을 따라야 합니다. 머티리얼 속성은 `UnityPerMaterial` CBUFFER에, 오브젝트별 데이터는 `UnityPerDraw` CBUFFER에 선언해야 합니다. CBUFFER는 GPU에 전달할 값을 묶어 두는 상수 버퍼(Constant Buffer)입니다.

이 규칙을 지키면 머티리얼 데이터가 GPU 메모리에 유지되고, 드로우콜마다 같은 값을 다시 업로드할 필요가 줄어듭니다. 같은 셰이더 배리언트가 이어질 때는 셰이더 상태도 재사용할 수 있으므로, CPU가 드로우콜을 준비하는 시간이 짧아집니다. URP의 기본 Lit, Unlit 셰이더는 이 호환 규칙을 갖춘 상태로 제공됩니다.

이제 이 SRP 기반이 실제 프로젝트에서 어떤 형태로 쓰이는지 URP를 통해 살펴보겠습니다. URP는 Built-in의 고정 루프와 멀티패스 비용을 피하면서, SRP Batcher와 같은 구조적 최적화를 기본 전제로 삼는 파이프라인입니다.

---

## URP (Universal Render Pipeline)

**URP(Universal Render Pipeline)**는 모바일부터 PC/콘솔까지 하나의 파이프라인으로 대응하기 위해 만들어진 공식 렌더 파이프라인입니다. 목표는 모든 플랫폼에서 가장 높은 품질을 내는 것이 아니라, 넓은 플랫폼 범위에서 예측 가능한 성능과 충분한 시각적 품질을 함께 확보하는 데 있습니다.

이 때문에 URP는 새 프로젝트의 기본 출발점으로 보기 좋습니다. SRP Batcher, Renderer Feature, Camera Stacking, Render Graph 같은 SRP 기반 기능을 바로 사용할 수 있고, 실시간 전역 조명(Real-time GI)이나 스크린 스페이스 반사(SSR)처럼 고급 기능도 점차 URP 쪽으로 들어오고 있습니다.

### 렌더링 방식

URP의 기본 렌더링 방식은 **싱글패스 포워드 렌더링(Single-pass Forward Rendering)**입니다. 오브젝트를 한 번 그릴 때, 그 표면에 영향을 주는 조명을 하나의 셰이더 패스 안에서 함께 계산합니다.

이 구조는 Built-in Forward의 멀티패스와 다릅니다. Built-in에서는 추가 픽셀 라이트가 붙을 때마다 오브젝트를 다시 그리는 패스가 늘어났지만, URP의 싱글패스 포워드는 조명을 한 패스 안에서 처리합니다. 그래서 기본 Forward에서는 조명 수가 곧바로 드로우콜 수로 늘어나지 않습니다.

> 멀티패스와 싱글패스가 드로우콜 수에 어떤 차이를 만드는지는 [Unity 렌더 파이프라인 (1)](/dev/unity/UnityPipeline-1/)에서 자세히 비교합니다.

조명이 많은 씬에서는 **Forward+**나 **Deferred Rendering**을 검토할 수 있습니다. Forward+는 화면을 작은 타일로 나누고, 각 타일에 실제로 영향을 주는 조명만 추려 계산합니다. 기본 Forward의 오브젝트당 추가 라이트 한계를 피하면서도 포워드 렌더링의 단순한 흐름을 유지할 수 있습니다.

Deferred는 G-Buffer에 표면 정보를 먼저 기록한 뒤, 조명을 화면 공간에서 한꺼번에 계산합니다. 조명이 매우 많은 장면에서는 Forward보다 유리할 수 있지만, G-Buffer 때문에 Render Target 수가 늘고 메모리와 대역폭 비용도 커집니다. 그래서 모바일처럼 대역폭이 빠듯한 환경에서는 기본 Forward나 Forward+를 먼저 검토하는 편이 일반적입니다.

### Forward의 라이트 제한

여기서 말하는 라이트 제한은 URP의 기본 **Forward** 경로에 해당합니다. Forward+와 Deferred는 라이트를 고르는 방식이 다르므로, 아래의 `Per Object Limit`가 그대로 적용되지 않습니다.

기본 Forward에서는 모든 라이트를 한 오브젝트의 셰이더 루프에 무제한으로 넣지 않습니다. 먼저 카메라 기준의 **Main Light** 1개를 따로 처리하고, 나머지는 각 오브젝트에 영향이 큰 **Additional Light**만 제한된 수만큼 고릅니다. 이 한도가 URP Asset의 **Additional Lights > Per Object Limit**입니다.

`Per Object Limit`의 기본값은 4이고, 일반적으로 8까지 올릴 수 있습니다. 한도를 넘는 추가 라이트는 그 오브젝트의 조명 계산에서 제외됩니다. 그래서 같은 씬 안에 라이트가 많이 놓여 있어도, 기본 Forward에서는 오브젝트 하나가 실제로 받는 추가 라이트 수가 이 값으로 잘립니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP Forward의 라이트 구조</text>
  <!-- Main Light box (emphasized) -->
  <rect x="30" y="42" width="500" height="105" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Main Light (Directional Light, 카메라당 1개)</text>
  <line x1="50" y1="74" x2="510" y2="74" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="50" y="94" font-family="sans-serif" font-size="11" fill="currentColor">씬 전체에 적용되는 주 조명</text>
  <text x="50" y="112" font-family="sans-serif" font-size="11" fill="currentColor">그림자 생성 가능</text>
  <text x="50" y="130" font-family="sans-serif" font-size="11" fill="currentColor">싱글패스 셰이더에서 가장 먼저 처리</text>
  <!-- Additional Lights box -->
  <rect x="30" y="160" width="500" height="120" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="184" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Additional Lights (Point, Spot 등, N개)</text>
  <line x1="50" y1="192" x2="510" y2="192" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="50" y="212" font-family="sans-serif" font-size="11" fill="currentColor">오브젝트별로 가장 가까운/밝은 N개만 적용</text>
  <text x="50" y="230" font-family="sans-serif" font-size="11" fill="currentColor">N = Per Object Limit (기본 4, 최대 8)</text>
  <text x="50" y="248" font-family="sans-serif" font-size="11" fill="currentColor">같은 셰이더 패스 안에서 루프로 처리</text>
  <text x="50" y="266" font-family="sans-serif" font-size="11" fill="currentColor">추가 라이트별 그림자는 선택적</text>
  <!-- Mobile recommendation -->
  <rect x="30" y="295" width="500" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="280" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">모바일 Forward 권장: Main Light 1 + Additional Light 2~4</text>
</svg>
</div>

<br>

메인 라이트는 씬의 기준이 되는 주 조명이고, 추가 라이트는 오브젝트마다 가까우면서 영향이 큰 것부터 선택됩니다. 선택된 추가 라이트만 같은 패스의 루프에서 처리되므로, `Per Object Limit`을 올릴수록 한 오브젝트의 조명 계산 비용도 함께 커집니다.

모바일에서는 이 값을 작게 잡는 편이 안전합니다. 보통 추가 라이트를 2~4개 정도로 제한하고, 추가 라이트 그림자는 꼭 필요한 라이트에만 켜는 식으로 비용을 관리합니다. 더 많은 라이트가 필요하다면 기본 Forward에서 한도를 무작정 올리기보다, Forward+나 라이트 베이킹을 먼저 검토하는 편이 좋습니다.

### Renderer Feature

URP가 기본 렌더링 경로만 제공한다면 프로젝트마다 필요한 특수 효과를 넣기 어렵습니다. 그래서 URP는 파이프라인 중간에 사용자가 만든 렌더링 단계를 끼워 넣을 수 있는 확장 지점을 제공합니다. 그 역할을 하는 API가 **ScriptableRendererFeature**입니다.

Renderer Feature는 하나 이상의 커스텀 렌더 패스를 등록하고, 그 패스를 어느 시점에 실행할지 정합니다. 예를 들어 불투명 오브젝트 렌더링 뒤, 투명 오브젝트 렌더링 전, 후처리 직전처럼 파이프라인의 특정 지점에 패스를 넣을 수 있습니다. 여기서 렌더 패스(Render Pass)는 특정 오브젝트를 다시 그리거나, Render Target을 읽고 쓰거나, 화면 전체에 효과를 적용하는 하나의 렌더링 단위입니다.

대표적인 예로는 아웃라인, 커스텀 블러, 특정 레이어만 따로 그려 만드는 마스크, 디버그 시각화가 있습니다. 기본 URP 렌더러를 통째로 바꾸지 않고도 필요한 단계만 추가할 수 있으므로, 대부분의 커스텀 렌더링 요구는 Custom SRP로 가기 전에 Renderer Feature에서 먼저 검토하는 편이 좋습니다.

Built-in에서 `CommandBuffer`를 특정 이벤트 시점에 붙이던 방식과 비교하면, Renderer Feature는 URP 렌더러가 관리하는 패스 목록 안에 들어간다는 점이 다릅니다. Render Graph 경로로 작성한 패스라면 어떤 리소스를 읽고 쓰는지도 함께 선언할 수 있어, 뒤에서 다룰 Render Graph가 Render Target 수명과 패스 의존성을 분석하는 데 활용할 수 있습니다.

### Camera Stacking

URP에서 여러 카메라를 한 화면에 합칠 때 사용하는 구조가 **Camera Stacking**입니다. 먼저 Base Camera가 장면의 기준 화면을 만들고, 그 위에 Overlay Camera가 등록된 순서대로 이어서 그립니다. Overlay Camera는 독립된 최종 출력 카메라처럼 동작하지 않고, Base Camera의 렌더링 흐름 안에 포함됩니다.

> Camera Stacking의 카메라 구성과 렌더링 순서는 [Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 자세히 다룹니다.

이 구조의 장점은 출력 대상과 순서가 명확하다는 점입니다. Overlay Camera는 Base Camera가 사용하는 Render Target 위에 결과를 덧그리므로, 카메라별 결과를 따로 만든 뒤 다시 합성하는 구성을 줄일 수 있습니다.

다만 Overlay Camera가 추가된다고 렌더링 비용이 사라지는 것은 아닙니다. Overlay Camera도 자신이 담당하는 레이어를 컬링하고, 필요한 오브젝트를 다시 그립니다. 따라서 UI, 1인칭 무기 뷰, 특정 효과처럼 별도 카메라가 필요한 경우에만 Stack에 올리고, Culling Mask를 좁혀 그 카메라가 처리할 대상을 제한하는 편이 좋습니다.

### 2D Renderer

URP는 3D 렌더러만 제공하지 않습니다. 스프라이트 중심의 2D 게임을 위해 **2D Renderer**도 별도로 제공합니다. 이 렌더러를 선택하면 2D 전용 라이트, 2D 그림자, 스프라이트용 노멀 맵 같은 기능을 같은 URP 프로젝트 안에서 사용할 수 있습니다.

Built-in에서는 2D 스프라이트에 동적인 조명을 넣으려면 커스텀 셰이더나 별도 구현에 의존하는 경우가 많았습니다. URP의 2D Renderer는 이 흐름을 파이프라인 기능으로 제공합니다. 스프라이트를 단순히 밝기만 입힌 이미지로 두지 않고, 2D 라이트의 영향을 받는 렌더링 대상으로 다룰 수 있게 해 줍니다.

핵심 컴포넌트는 **Light 2D**입니다. 자유로운 윤곽을 그리는 Freeform, 텍스처를 광원처럼 쓰는 Sprite, 한 점에서 퍼지는 Point, 화면 전체를 비추는 Global 같은 유형을 제공합니다. 여기에 스프라이트용 Normal Map을 함께 쓰면, 빛이 들어오는 방향에 따라 평면 이미지에도 입체감과 재질감이 생깁니다.

### 모바일 최적화 특성

URP가 모바일에서 유리한 이유는 개별 옵션 하나가 아니라 전체 구조에 있습니다. 기본 Forward 경로는 Built-in의 멀티패스처럼 조명 수에 따라 드로우콜을 반복해서 늘리지 않고, SRP Batcher는 드로우콜을 준비할 때 발생하는 CPU 상태 전환 비용을 줄입니다.

GPU 쪽에서는 Render Target 전환과 대역폭이 중요합니다. 모바일 GPU는 타일 메모리에서 렌더링한 결과를 시스템 메모리로 저장하거나 다시 불러오는 과정에서 비용이 커질 수 있습니다. URP는 렌더 패스를 명확한 단위로 구성하고, 필요한 경우 Render Graph를 통해 Render Target의 수명과 재사용을 관리해 불필요한 전환과 임시 버퍼 사용을 줄일 수 있습니다.

> 모바일 GPU에서 Render Target 전환이 왜 대역폭을 먹는지는 [Unity 렌더링 (2)](/dev/unity/UnityRendering-2/)에서 자세히 다룹니다.

안티에일리어싱도 모바일 구조와 맞물립니다. URP는 MSAA(Multi-Sample Anti-Aliasing)를 지원하며, 타일 기반 모바일 GPU에서는 MSAA 샘플이 타일 메모리 안에서 처리되는 동안에는 시스템 메모리 대역폭 부담이 상대적으로 작습니다. 그래서 모바일에서는 무거운 후처리 기반 안티에일리어싱보다 MSAA가 더 적합한 경우가 많습니다.

결국 URP의 강점은 "가볍다"는 한마디로 끝나지 않습니다. 모바일에서 시작해 PC와 콘솔까지 같은 파이프라인 안에서 확장할 수 있고, SRP Batcher, Renderer Feature, Camera Stacking, Render Graph 같은 핵심 기능을 함께 사용할 수 있습니다. 그래서 새 프로젝트에서는 URP를 먼저 검토하고, URP로 해결되지 않는 요구가 분명할 때만 다른 파이프라인을 검토하는 흐름이 자연스럽습니다.

---

## HDRP: 고품질 요구가 분명할 때의 선택지

HDRP(High Definition Render Pipeline)는 고사양 PC와 콘솔을 목표로 만들어진 고품질 SRP 파이프라인입니다. 물리 기반 조명, 고급 머티리얼, Volumetric Fog, Sub-Surface Scattering, 고급 반사처럼 사실적인 화면을 만드는 기능을 폭넓게 갖추고 있습니다.

다만 이 글의 흐름에서 HDRP는 새 프로젝트의 기본 출발점이 아닙니다. Unity의 렌더링 개발 중심은 URP로 옮겨 갔고, HDRP는 새 기능 확장보다 안정성, 회귀 수정, 중요 문제 대응, 플랫폼 도달 범위 유지에 무게가 실린 상태입니다. 즉 HDRP가 사라진다는 뜻은 아니지만, 앞으로의 일반적인 확장 방향을 기대하고 선택할 파이프라인은 아닙니다.

기술 비용도 분명합니다. HDRP는 고품질 표현을 위해 여러 Render Target, 복잡한 셰이더, 추가 렌더 패스를 적극적으로 사용합니다. 그만큼 GPU 메모리와 대역폭, 셰이더 비용이 커지고, Compute Shader를 포함한 현대적인 GPU 기능을 전제로 합니다. 모바일처럼 전력과 대역폭이 제한된 환경과는 맞지 않습니다.

따라서 HDRP는 두 경우에만 검토하는 편이 좋습니다. 이미 HDRP로 제작 중인 프로젝트를 유지해야 하거나, 목표 플랫폼이 고사양 PC/콘솔이고 URP로는 충족하기 어려운 고품질 조명과 머티리얼 요구가 명확할 때입니다. 그 외의 새 프로젝트라면 먼저 URP에서 필요한 화면을 만들 수 있는지 확인하는 쪽이 안전합니다.

URP에서 부족한 부분이 보이더라도 곧바로 HDRP로 옮겨 가기보다, 먼저 URP의 Renderer Feature, Render Graph, 커스텀 셰이더로 해결할 수 있는지 확인합니다. 그래도 파이프라인의 실행 순서 자체가 요구와 맞지 않는다면 Custom SRP를 검토하게 됩니다.

---

## Custom SRP

Custom SRP는 SRP 프레임워크 위에서 **렌더 파이프라인을 직접 구현하는** 방식입니다. `RenderPipeline` 클래스를 상속해 카메라 처리, 컬링, 정렬, Render Target 설정, 드로우콜 제출 순서를 직접 작성합니다. URP 위에 패스를 추가하는 수준이 아니라, 한 프레임의 렌더링 루프 자체를 프로젝트가 책임지는 선택입니다.

### 직접 구현이 필요한 경우

Custom SRP가 필요한 경우는 단순히 화면 효과 하나를 추가하고 싶을 때가 아닙니다. 그런 요구는 대개 URP의 Renderer Feature나 커스텀 셰이더로 처리할 수 있습니다. Custom SRP는 렌더링 순서, 컬링 방식, 패스 구성, Render Target 사용 방식 자체가 기존 파이프라인과 맞지 않을 때 검토합니다.

예를 들어 게임 전체가 특정 스타일의 셀 셰이딩(Cel Shading)만 사용하고, 그에 맞춰 조명과 그림자 계산을 단순화하려는 경우가 있습니다. 복셀(Voxel) 렌더링처럼 일반적인 메쉬 렌더링 흐름과 다른 구조를 쓰거나, 특정 장르에 맞춰 불필요한 기능을 걷어 낸 매우 가벼운 전용 파이프라인을 만들 때도 Custom SRP가 후보가 됩니다.

학습용으로 직접 구현해 보는 것도 의미가 있습니다. 컬링, 정렬, 드로우콜 생성, Render Target 설정을 직접 작성하면 URP가 내부에서 처리하는 기본 흐름을 더 구체적으로 이해할 수 있습니다. 다만 실무에서 선택하려면, 구현보다 유지보수 비용까지 감당할 수 있는지 먼저 따져야 합니다.

<br>

**Custom SRP의 최소 구현 구조**

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

class CustomRenderPipeline : RenderPipeline
{
    static readonly ShaderTagId ShaderTagId =
        new ShaderTagId("SRPDefaultUnlit");

    protected override void Render(
        ScriptableRenderContext context,
        List<Camera> cameras)
    {
        foreach (Camera camera in cameras)
            RenderCamera(context, camera);
    }

    static void RenderCamera(
        ScriptableRenderContext context,
        Camera camera)
    {
        // (1) 컬링
        if (!camera.TryGetCullingParameters(out var cullingParams))
            return;

        var cullingResults = context.Cull(ref cullingParams);

        // (2) 카메라 행렬과 기본 상태 설정
        context.SetupCameraProperties(camera);

        // (3) 컬러/깊이 버퍼 초기화
        var cmd = CommandBufferPool.Get("Custom SRP");
        cmd.ClearRenderTarget(true, true, Color.clear);
        context.ExecuteCommandBuffer(cmd);
        cmd.Clear();
        CommandBufferPool.Release(cmd);

        // (4) 불투명 오브젝트 렌더링
        var sortingSettings = new SortingSettings(camera)
        {
            criteria = SortingCriteria.CommonOpaque
        };
        var drawingSettings =
            new DrawingSettings(ShaderTagId, sortingSettings);
        var filteringSettings =
            new FilteringSettings(RenderQueueRange.opaque);

        context.DrawRenderers(
            cullingResults, ref drawingSettings,
            ref filteringSettings);

        // (5) 반투명 오브젝트 렌더링
        sortingSettings.criteria = SortingCriteria.CommonTransparent;
        drawingSettings.sortingSettings = sortingSettings;
        filteringSettings.renderQueueRange =
            RenderQueueRange.transparent;

        context.DrawRenderers(
            cullingResults, ref drawingSettings,
            ref filteringSettings);

        // (6) 누적된 명령 제출
        context.Submit();
    }
}
```

<br>

위 코드는 실제 프로덕션용 렌더러가 아니라, Custom SRP의 최소 흐름을 보여 주는 예시입니다. 카메라별로 컬링 결과를 만들고, 카메라 상태를 설정한 뒤, 버퍼를 지우고, 불투명 오브젝트와 반투명 오브젝트를 나누어 그린 다음 `Submit()`으로 명령을 제출합니다.

`ShaderTagId`는 어떤 셰이더 패스를 그릴지 고르는 기준입니다. 셰이더의 `Tags { "LightMode" = "..." }` 값과 일치하는 패스만 `DrawRenderers()`의 대상이 됩니다. 예시에서는 `SRPDefaultUnlit` 패스만 그리므로, 조명과 그림자, 스카이박스, 후처리, Render Graph 같은 기능은 포함되어 있지 않습니다.

그래도 기본 흐름은 같습니다. 렌더 파이프라인은 결국 컬링 → 정렬 → 드로우콜 생성 → GPU 제출이라는 순서를 바탕으로 동작합니다. URP도 이 흐름 위에 라이트, 그림자, 후처리, Renderer Feature, Render Graph 같은 단계를 더한 구조라고 보면 됩니다.

### 유지보수 부담

Custom SRP의 비용은 처음 구현할 때보다 이후에 더 크게 드러납니다. URP에서는 렌더 패스 구성, Render Target 수명, 플랫폼별 처리, API 변화 대응을 Unity가 파이프라인 안에서 관리합니다. Custom SRP를 선택하면 이 책임을 프로젝트가 직접 떠안게 됩니다.

Unity 버전을 올릴 때는 SRP API와 렌더링 백엔드 동작을 다시 검증해야 합니다. 새 플랫폼을 추가한다면 GPU 특성, MSAA 처리, Store/Load Action, 셰이더 호환성도 직접 맞춰야 합니다. 그림자, 후처리, XR, 디버그 도구처럼 URP가 기본으로 제공하는 기능도 필요하다면 별도로 설계해야 합니다.

따라서 Custom SRP의 판단 기준은 "직접 만들 수 있는가"가 아니라 **계속 관리할 수 있는가**입니다. 요구 사항이 URP의 Renderer Feature, Render Graph, 커스텀 셰이더 안에서 해결된다면 그 안에서 확장하는 편이 낫습니다. 파이프라인 루프 자체를 바꿔야 할 때만 Custom SRP를 선택합니다.

이제 선택 기준은 단순해집니다. 새 프로젝트는 URP에서 출발하고, Built-in은 기존 프로젝트와 이전 비용, HDRP는 명확한 고품질 PC/콘솔 요구, Custom SRP는 직접 파이프라인을 유지할 수 있는 특수 요구가 있을 때만 따로 검토합니다. 다음 절에서는 이 기준을 프로젝트 상황별로 정리합니다.

---

## 파이프라인 선택 기준

앞에서 본 내용을 실제 프로젝트 판단으로 옮기면, 파이프라인 선택은 여러 후보를 같은 무게로 비교하는 일이 아닙니다. 기본 출발점은 URP입니다. 먼저 URP로 목표 플랫폼과 화면 품질, 필요한 렌더링 기능을 충족할 수 있는지 확인하고, 부족한 부분이 Renderer Feature, Render Graph, 커스텀 셰이더로 해결되는지 봅니다.

그래도 요구가 맞지 않을 때만 다른 선택지를 엽니다. 기존 Built-in 프로젝트라면 유지할지 URP로 이전할지를 따지고, 고품질 PC/콘솔 요구가 URP로 해결되지 않는다면 HDRP를 검토합니다. 렌더링 루프 자체를 바꿔야 한다면 Custom SRP가 마지막 선택지가 됩니다.

이 판단은 프로젝트 초기에 끝내는 편이 좋습니다. 렌더 파이프라인은 셰이더와 머티리얼, 라이팅, 후처리, 커스텀 렌더링 코드의 전제를 함께 정합니다. 중간에 바꾸면 화면 품질을 다시 맞추는 일뿐 아니라 에셋 변환, 셰이더 수정, 렌더링 코드 재작성, 시각적 검수까지 이어집니다.

### 상황별 판단

아래 표는 파이프라인을 나란히 놓고 고르는 목록이 아니라, URP에서 출발한 뒤 어떤 경우에 예외를 검토할지 정리한 기준입니다. 새 프로젝트와 기존 프로젝트는 판단 방식이 다릅니다. 새 프로젝트는 앞으로의 확장성과 유지보수 비용을 먼저 보고, 기존 프로젝트는 출시 일정과 이전 비용, 품질 회귀 위험을 함께 봐야 합니다.

<br>

| 상황 | 판단 | 확인할 점 |
|---|---|---|
| 새 모바일 프로젝트 | URP | Forward/Forward+, SRP Batcher, Render Graph를 기준으로 CPU와 대역폭 비용을 관리할 수 있음 |
| 새 PC/콘솔 프로젝트 | URP에서 시작 | 대부분의 실시간 렌더링 요구를 URP 안에서 처리할 수 있고, 플랫폼 확장 부담이 작음 |
| 기존 Built-in 프로젝트 | 유지 또는 URP 이전 계획 | 셰이더와 머티리얼 변환, 라이팅 재설정, 출시 일정까지 함께 계산해야 함 |
| 기존 HDRP 프로젝트 | 유지 중심 | 이미 구축한 고품질 렌더링을 보존하되, 신규 확장과 장기 유지 비용을 신중히 봐야 함 |
| URP로 부족한 고품질 PC/콘솔 요구 | HDRP 제한 검토 | 필요한 기능이 HDRP에 이미 있고, 높은 메모리와 GPU 비용을 감수할 수 있어야 함 |
| 파이프라인 구조 자체가 다른 특수 렌더링 | Custom SRP | URP의 Renderer Feature나 Render Graph로 해결할 수 없고, 장기 유지까지 감당할 수 있어야 함 |

<br>

핵심은 새 프로젝트와 기존 프로젝트를 구분하는 것입니다. 새 프로젝트라면 URP를 기본값으로 두고, 명확한 예외 조건이 있을 때만 다른 파이프라인을 엽니다. 반대로 이미 Built-in이나 HDRP로 제작 중인 프로젝트라면 무조건 이전하기보다, 일정과 품질 회귀, 마이그레이션 비용을 먼저 따져야 합니다.

### 대상 플랫폼

플랫폼은 파이프라인 선택에서 가장 먼저 걸러야 할 조건입니다. 특히 모바일은 선택 폭이 좁습니다. CPU 드로우콜 비용과 GPU 대역폭, 발열, 배터리까지 함께 관리해야 하므로, 처음부터 URP의 Forward/Forward+ 구조와 SRP Batcher를 기준으로 잡는 편이 맞습니다. HDRP는 모바일 대상 파이프라인이 아니고, Built-in은 조명이 늘어날수록 멀티패스 비용이 커지며 SRP Batcher도 사용할 수 없습니다.

PC나 콘솔에서도 기본 판단은 크게 달라지지 않습니다. URP는 Forward뿐 아니라 Forward+와 Deferred를 제공하므로, 조명이 많은 씬이나 비교적 높은 품질의 화면도 같은 파이프라인 안에서 단계적으로 확장할 수 있습니다. 여러 플랫폼을 동시에 노리는 프로젝트라면 이 점이 특히 중요합니다. 파이프라인을 하나로 유지할수록 셰이더, 머티리얼, 후처리 설정을 플랫폼마다 갈라 관리할 일이 줄어듭니다.

HDRP는 범용 선택지가 아니라 고사양 PC/콘솔을 전제로 한 제한적 선택지입니다. Volumetric Fog, Sub-Surface Scattering, 고급 반사처럼 HDRP에 이미 갖춰진 기능이 반드시 필요하고, G-Buffer와 추가 렌더 패스가 만드는 메모리와 대역폭 비용을 감당할 수 있을 때만 검토합니다. 단순히 "더 좋은 그래픽"이 필요하다는 이유만으로 HDRP를 고르기보다, URP에서 같은 요구를 충족할 수 있는지 먼저 확인하는 편이 안전합니다.

### 셰이더 호환성

파이프라인을 바꿀 때 가장 먼저 드러나는 문제는 셰이더입니다. 셰이더는 단순히 표면 색을 계산하는 코드가 아니라, 어떤 조명 데이터를 받을지, 어떤 렌더 패스에서 실행될지, 어떤 태그와 상수 버퍼 구조를 따를지까지 파이프라인의 규약에 맞춰 작성됩니다. 그래서 파이프라인이 다르면 같은 머티리얼처럼 보여도 내부 전제가 달라집니다.

Built-in의 Surface Shader는 URP에서 그대로 동작하지 않습니다. URP의 Lit Shader와 HDRP의 Lit Shader도 이름은 비슷하지만, 서로 다른 라이팅 모델과 렌더링 구조를 전제로 합니다. 셰이더가 기대하는 `LightMode` 태그, 패스 구성, 머티리얼 프로퍼티 배치가 맞지 않으면 오브젝트가 제대로 그려지지 않거나 오류 셰이더로 표시될 수 있습니다.

Built-in에서 URP로 이전할 때는 **Render Pipeline Converter**(Window > Rendering > Render Pipeline Converter)를 사용할 수 있습니다. 다만 이 도구는 주로 Unity가 제공하는 기본 셰이더와 일반적인 머티리얼 참조를 URP용으로 바꾸는 데 초점이 있습니다. 커스텀 HLSL, 직접 만든 조명 계산, 특정 렌더 패스에 의존하는 셰이더는 자동 변환 대상이 아니므로 새 파이프라인 규약에 맞춰 다시 작성해야 합니다.

따라서 파이프라인 선택은 셰이더 작성 방식의 선택이기도 합니다. 새 프로젝트라면 처음부터 URP용 Shader Graph나 URP HLSL 구조를 기준으로 잡는 편이 이후 비용을 줄입니다. 기존 프로젝트를 옮긴다면 변환 도구를 먼저 돌리는 것보다, 커스텀 셰이더와 핵심 머티리얼이 얼마나 많은지부터 확인해야 합니다.

### 파이프라인 변경 비용

렌더 파이프라인을 바꾸는 일은 렌더링 설정 하나를 교체하는 작업이 아닙니다. 파이프라인은 셰이더, 머티리얼, 라이팅, 후처리, 커스텀 렌더링 코드가 기대하는 전제를 함께 정합니다. 그래서 전환이 시작되면 화면을 만드는 여러 층을 다시 맞춰야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- 제목 -->
  <text x="250" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">파이프라인 전환 시 다시 맞춰야 하는 영역</text>

  <!-- (1) 셰이더/머티리얼 -->
  <rect x="24" y="42" width="452" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="52" cy="62" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="52" y="66" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1</text>
  <text x="76" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">셰이더와 머티리얼</text>
  <text x="52" y="88" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">파이프라인별 셰이더 교체</text>
  <text x="52" y="104" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">커스텀 HLSL과 핵심 머티리얼 재검토</text>

  <!-- (2) 라이팅/후처리 -->
  <rect x="24" y="132" width="452" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="52" cy="152" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="52" y="156" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2</text>
  <text x="76" y="156" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">라이팅과 후처리</text>
  <text x="52" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">라이트, 그림자, 라이트맵 설정 재조정</text>
  <text x="52" y="194" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">후처리 볼륨과 카메라 옵션 재구성</text>

  <!-- (3) 커스텀 렌더링 -->
  <rect x="24" y="222" width="452" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="52" cy="242" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="52" y="246" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3</text>
  <text x="76" y="246" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">커스텀 렌더링 코드</text>
  <text x="52" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">CommandBuffer, Renderer Feature, Render Pass 이전</text>
  <text x="52" y="284" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">Render Target 수명과 패스 순서 재검토</text>

  <!-- (4) 검증 -->
  <rect x="24" y="312" width="452" height="76" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="52" cy="332" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="52" y="336" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4</text>
  <text x="76" y="336" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">시각적 검수와 성능 재측정</text>
  <text x="52" y="358" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">씬별 밝기, 색, 그림자, 후처리 결과 확인</text>
  <text x="52" y="374" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.65">드로우콜, RT 메모리, GPU 시간 다시 측정</text>
</svg>
</div>

<br>

작은 샘플 프로젝트라면 변환 도구와 몇 가지 수동 수정으로 끝날 수 있습니다. 하지만 씬이 많고, 커스텀 셰이더와 베이크된 라이트맵, 후처리 프로파일, 커스텀 렌더 패스가 쌓인 프로젝트에서는 전환 자체가 별도의 마이그레이션 작업이 됩니다. 기능이 다시 동작하는지 확인하는 것과, 이전과 같은 화면이 나오는지 검수하는 것은 다른 문제입니다.

그래서 렌더 파이프라인은 프로젝트 초기에 정하고, 중간에 바꾸지 않는 것을 전제로 설계하는 편이 좋습니다. 새 프로젝트는 URP에서 시작하고, 예외적인 요구가 분명할 때만 다른 파이프라인을 검토합니다.

---

## 마무리

이번 글의 결론은 단순합니다. 새 프로젝트는 URP에서 시작하고, 다른 파이프라인은 예외 조건이 있을 때만 검토합니다. 각 파이프라인이 지금 어디에 서 있는지 정리하면 다음과 같습니다.

- **렌더 파이프라인**은 한 프레임을 그리는 동안 컬링과 정렬, 라이팅, Render Target, 후처리를 어떤 순서와 규칙으로 실행할지 정하는 상위 구조입니다.
- **Built-in Render Pipeline**은 Unity의 이전 세대 렌더 파이프라인으로, 지금은 레거시로 남아 있습니다. 기존 프로젝트나 오래된 자료를 읽을 때는 구조를 알아 둘 필요가 있지만, 새 프로젝트의 기본 선택지로 삼기는 어렵습니다.
- **SRP(Scriptable Render Pipeline)**는 렌더링 루프를 C# 코드로 제어하게 해 주는 기반으로, URP와 HDRP가 모두 이 위에 세워져 있습니다.
- **URP**는 모바일부터 PC와 콘솔까지 폭넓게 대응하며, SRP Batcher와 Renderer Feature, Camera Stacking, Render Graph를 두루 갖춘 Unity의 단일 주력 파이프라인입니다.
- **HDRP**는 고사양 PC와 콘솔을 겨냥한 고품질 파이프라인이지만, 지금은 신규 기능 개발에서 물러나 유지보수 모드에 있습니다. 기존 HDRP 프로젝트나 URP만으로는 충족하기 어려운 고품질 요구가 있을 때 제한적으로 검토합니다.
- **Custom SRP**는 URP의 확장 지점으로도 풀리지 않는 특수한 렌더링 구조가 필요할 때 택하는 마지막 수단입니다.
- **파이프라인 전환 비용**은 큽니다. 셰이더와 머티리얼, 라이팅, 후처리, 커스텀 렌더링 코드를 모두 새 파이프라인에 맞춰야 하므로, 방향은 프로젝트 초기에 정해 두는 편이 좋습니다.

<br>

어떤 파이프라인을 선택할지는 목표 플랫폼과 화면 품질, 전환 비용이 함께 정합니다. 대부분의 프로젝트에서 그 답은 URP이고, HDRP나 Custom SRP는 URP만으로는 충족하기 어려운 요구가 분명할 때 택하는 예외입니다.

<br>

이로써 Unity 렌더링 세 편에서는 카메라([Unity 렌더링 (1)](/dev/unity/UnityRendering-1/))가 무엇을 어떤 순서로 그리는지, Render Target([Unity 렌더링 (2)](/dev/unity/UnityRendering-2/))이 그 결과를 어디에 저장하는지, 그리고 렌더 파이프라인(이 글)이 이 과정을 어떻게 하나로 묶는지를 살펴보았습니다. 이 내용을 바탕으로 [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)에서 렌더링 구조를 더 깊게 다루고, [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)에서 라이팅 비용을, [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서 셰이더 성능을 이어서 살펴볼 수 있습니다.

<br>

---

**관련 글**
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)

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
- **Unity 렌더링 (3) - Render Pipeline 개요** (현재 글)
