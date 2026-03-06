---
layout: single
title: "Unity 렌더링 (3) - Render Pipeline 개요 - soo:bak"
date: "2026-03-06 21:09:00 +0900"
description: Built-in Render Pipeline, SRP, URP, HDRP, Custom SRP의 설계 철학과 선택 기준을 설명합니다.
tags:
  - Unity
  - 렌더링
  - URP
  - HDRP
  - SRP
  - 모바일
---

## 렌더 파이프라인이라는 상위 구조

[Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)에서 카메라가 무엇을 어떤 순서로 그리는지를, [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)에서 그 결과가 어디에 저장되는지를 다루었습니다.
이 두 글에서 다룬 카메라 설정, 렌더링 순서, Render Target 관리를 하나의 흐름으로 엮는 상위 구조가 **렌더 파이프라인(Render Pipeline)**입니다.

렌더 파이프라인은 한 프레임을 완성하기 위해 어떤 단계를 어떤 순서로 실행할지를 정의합니다. 컬링(카메라에 보이지 않는 오브젝트를 렌더링 대상에서 제외하는 과정) 방식, 불투명과 반투명의 정렬 방식, 조명 패스 횟수, 후처리(렌더링된 이미지에 블룸, 색보정 등의 화면 효과를 적용하는 단계) 순서가 모두 렌더 파이프라인의 설계에 따라 결정됩니다.

<br>

Unity에서 렌더 파이프라인의 선택은 프로젝트의 시각적 품질, 성능 특성, 셰이더 작성 방식, 확장 가능성에 영향을 미칩니다.
한 번 선택한 파이프라인을 프로젝트 중간에 변경하면 셰이더, 머티리얼, 라이팅 설정 등을 전면 수정해야 하므로 비용이 큽니다.

이 글에서는 Unity가 제공하는 렌더 파이프라인의 종류와 각각의 설계 철학, 프로젝트에 맞는 선택 기준을 다룹니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 660 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 660px; width: 100%;">
  <!-- Built-in box -->
  <rect x="190" y="12" width="280" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Built-in Render Pipeline</text>
  <text x="330" y="52" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">최초, 레거시</text>
  <!-- Arrow Built-in → SRP with label -->
  <line x1="330" y1="62" x2="330" y2="112" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="324,109 330,119 336,109" fill="currentColor"/>
  <text x="338" y="92" text-anchor="start" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">수정 불가능한 고정 렌더링 루프</text>
  <!-- SRP box -->
  <rect x="120" y="119" width="420" height="56" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="142" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SRP (Scriptable Render Pipeline)</text>
  <text x="330" y="163" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Unity 2018 도입 · 렌더링 루프를 C#으로 제어 가능</text>
  <!-- Arrow → URP -->
  <line x1="120" y1="175" x2="120" y2="232" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="114,229 120,239 126,229" fill="currentColor"/>
  <!-- Arrow → HDRP -->
  <line x1="330" y1="175" x2="330" y2="232" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="324,229 330,239 336,229" fill="currentColor"/>
  <!-- Arrow → Custom SRP -->
  <line x1="540" y1="175" x2="540" y2="232" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="534,229 540,239 546,229" fill="currentColor"/>
  <!-- URP box -->
  <rect x="15" y="240" width="210" height="82" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="262" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP</text>
  <text x="120" y="280" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Universal Render Pipeline</text>
  <text x="120" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">모바일 ~ 중급 PC 대상</text>
  <!-- HDRP box -->
  <rect x="225" y="240" width="210" height="82" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="262" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">HDRP</text>
  <text x="330" y="280" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">High Definition Render Pipeline</text>
  <text x="330" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">고사양 PC / 콘솔 대상</text>
  <!-- Custom SRP box -->
  <rect x="435" y="240" width="210" height="82" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="540" y="262" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Custom SRP</text>
  <text x="540" y="288" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">직접 구현하는 파이프라인</text>
</svg>
</div>

<br>

Built-in에서 시작하여, SRP 프레임워크의 등장으로 URP, HDRP, Custom SRP라는 선택지가 생긴 흐름입니다. 각 파이프라인을 순서대로 살펴봅니다.

---

## Built-in Render Pipeline

Built-in Render Pipeline은 Unity가 초기부터 제공한 렌더 파이프라인입니다. SRP가 도입된 Unity 2018.1 이전에는 유일한 파이프라인이었으며, 현재도 레거시 프로젝트에서 사용됩니다.

### 구조적 특징

Built-in 파이프라인은 **Forward Rendering**과 **Deferred Rendering** 두 가지 렌더링 방식을 모두 지원합니다. 프로젝트 설정에서 둘 중 하나를 선택할 수 있으며, 카메라별로 다른 방식을 지정할 수도 있습니다.

Built-in의 Forward Rendering은 **멀티패스(Multi-pass)** 방식으로 동작합니다.
멀티패스란 하나의 오브젝트를 조명별로 나누어 여러 번 그리는 구조입니다. 메인 Directional Light는 ForwardBase 패스에서 처리되지만, 추가 픽셀 라이트 하나마다 ForwardAdd 패스가 별도로 실행됩니다. 따라서 드로우콜 수가 `오브젝트 수 x (1 + 추가 픽셀 라이트 수)`에 비례합니다.
조명이 적은 씬에서는 문제가 되지 않지만, 조명이 많아지면 드로우콜이 급증합니다. 드로우콜마다 CPU가 GPU 상태를 설정하고 명령을 제출해야 하므로, 이 증가는 곧 CPU 병목으로 이어집니다.
이 멀티패스 구조의 상세한 흐름은 [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)에서 다룹니다.

<br>

반면 Deferred Rendering은 렌더링을 두 단계로 나눕니다.
먼저 씬의 모든 오브젝트에 대해 표면 색상(Albedo), 법선(Normal), 깊이(Depth) 등의 기하 정보를 G-Buffer라는 여러 장의 텍스처에 기록합니다. 이후 G-Buffer 데이터를 입력으로 라이팅을 화면 공간에서 한 번에 처리합니다. 조명 수에 드로우콜이 비례하지 않는다는 장점이 있지만, G-Buffer가 여러 장의 Render Target을 사용하므로 메모리와 대역폭 소비가 큽니다. [Unity 렌더링 (2)](/dev/unity/UnityRendering-2/)에서 다룬 것처럼, Full HD 해상도에서 RGBA32 포맷의 G-Buffer 4장이 약 32MB의 추가 메모리를 차지합니다.

모바일에서는 이 메모리 비용에 대역폭 부담까지 겹칩니다. 모바일 GPU는 TBDR(Tile-Based Deferred Rendering — 화면을 타일 단위로 나누어 칩 내부의 고속 메모리에서 렌더링하는 구조) 방식을 사용하는데, G-Buffer 전체를 시스템 메모리에 Store한 뒤 조명 패스에서 다시 Load해야 하므로 대역폭 소비가 큽니다. 이 때문에 모바일에서 Built-in의 Deferred Rendering은 실용적이지 않습니다.

### 확장성의 한계

Built-in 파이프라인의 가장 큰 제약은 **렌더링 루프를 수정할 수 없다**는 점입니다. 컬링, 정렬, 라이팅 패스, 드로우콜 생성이 엔진 내부에 고정되어 있으며, 개발자가 이 과정을 변경하거나 재배치할 방법이 없습니다.

확장 수단으로는 **OnPreRender**, **OnPostRender**, **OnRenderObject** 같은 렌더링 콜백과, **CommandBuffer**를 특정 이벤트 시점에 삽입하는 방식이 있습니다. 하지만 파이프라인의 정해진 시점에 추가 명령을 끼워넣는 것일 뿐, 파이프라인 자체의 구조를 바꾸지는 못합니다.

### 셰이더

Built-in 파이프라인에서는 **Surface Shader**라는 Unity 고유의 셰이더 작성 방식을 사용할 수 있습니다.
개발자가 조명 모델과 표면의 속성(Albedo, Normal, Emission 등)만 지정하면, Unity가 멀티패스용 셰이더 코드를 자동 생성합니다. 조명 모델은 빛과 표면의 상호작용을 계산하는 수학적 공식이며, Lambert(확산광), Blinn-Phong(확산광 + 반사광) 등이 대표적입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Top section: Developer code -->
  <rect x="40" y="12" width="400" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="34" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">개발자가 작성하는 부분</text>
  <!-- Code block -->
  <text x="65" y="62" font-family="monospace" font-size="11" fill="currentColor">void surf(Input IN,</text>
  <text x="65" y="80" font-family="monospace" font-size="11" fill="currentColor">          inout SurfaceOutput o)</text>
  <text x="65" y="98" font-family="monospace" font-size="11" fill="currentColor">{</text>
  <text x="65" y="116" font-family="monospace" font-size="11" fill="currentColor">    o.Albedo = tex2D(_MainTex, IN.uv);</text>
  <text x="65" y="134" font-family="monospace" font-size="11" fill="currentColor">    o.Normal = UnpackNormal(normalMap);</text>
  <text x="65" y="148" font-family="monospace" font-size="11" fill="currentColor">}</text>
  <!-- Arrow down -->
  <line x1="240" y1="152" x2="240" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="234,207 240,217 246,207" fill="currentColor"/>
  <text x="248" y="188" text-anchor="start" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Unity가 자동 생성</text>
  <!-- Bottom section: Auto-generated passes -->
  <rect x="40" y="218" width="400" height="138" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="240" y="240" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">자동 생성되는 멀티패스 셰이더</text>
  <!-- Pass items -->
  <text x="65" y="268" font-family="sans-serif" font-size="11" fill="currentColor">ForwardBase 패스</text>
  <text x="260" y="268" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">메인 라이트 처리</text>
  <line x1="60" y1="278" x2="420" y2="278" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="65" y="298" font-family="sans-serif" font-size="11" fill="currentColor">ForwardAdd 패스</text>
  <text x="260" y="298" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">추가 라이트마다 1개씩 실행</text>
  <line x1="60" y1="308" x2="420" y2="308" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="65" y="328" font-family="sans-serif" font-size="11" fill="currentColor">ShadowCaster 패스</text>
  <text x="260" y="328" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">그림자 생성</text>
  <text x="240" y="350" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→ 멀티패스 셰이더 코드 자동 생성</text>
</svg>
</div>

<br>

Surface Shader의 자동 생성은 편리하지만, 생성된 코드를 세밀하게 제어하기 어렵습니다. 불필요한 패스가 생성되거나 의도하지 않은 셰이더 배리언트가 포함될 수 있습니다. **셰이더 배리언트**는 하나의 셰이더 소스에서 키워드 조합에 따라 생성되는 여러 버전의 컴파일된 셰이더입니다. 배리언트 수가 늘어나면 빌드 크기와 셰이더 로딩 시간이 함께 증가합니다.

### 현재 상태

Built-in Render Pipeline은 더 이상 신규 기능이 추가되지 않는 레거시 상태입니다.
Unity는 공식적으로 신규 프로젝트에 URP 또는 HDRP를 권장합니다. 기존 Built-in 프로젝트는 계속 동작하지만, SRP 기반에서만 제공되는 기능의 혜택을 받을 수 없습니다. 예를 들어, Render Graph는 렌더 패스 간 의존성을 분석하여 불필요한 패스를 자동 제거하고 메모리를 재사용하는 시스템인데, SRP 위에서만 동작합니다. 이후 다룰 SRP Batcher도 마찬가지입니다.

<br>

렌더링 루프를 수정할 수 없는 Built-in의 구조적 한계를 해소하기 위해 Unity가 도입한 프레임워크가 SRP입니다.

---

## SRP (Scriptable Render Pipeline)

**SRP(Scriptable Render Pipeline)**는 Unity 2018에서 도입된 프레임워크로, 렌더링 루프를 **C# 스크립트로 직접 제어**할 수 있게 해주는 기반 구조입니다. SRP 자체는 특정 렌더 파이프라인이 아니며, URP와 HDRP가 SRP 위에 구축된 구체적인 파이프라인 구현체에 해당합니다.

### 핵심 클래스

SRP의 구조는 세 개의 핵심 클래스를 중심으로 동작합니다.

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
  <text x="80" y="238" font-family="monospace" font-size="11" fill="currentColor">Render(ScriptableRenderContext, Camera[])</text>
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

`RenderPipelineAsset`은 ScriptableObject를 상속한 에셋입니다. 이 에셋을 Graphics Settings에서 프로젝트의 렌더 파이프라인으로 지정하면, `CreatePipeline()`을 통해 `RenderPipeline` 인스턴스가 생성됩니다. Unity는 매 프레임 이 인스턴스의 `Render()` 메서드를 호출합니다.

`Render()` 메서드 안에서 개발자는 컬링, 정렬, 드로우콜 생성, Render Target 설정 등을 C# 코드로 직접 구성하고, `ScriptableRenderContext`를 통해 이 명령들을 GPU에 제출합니다.

### SRP Batcher

SRP와 함께 도입된 **SRP Batcher**는 드로우콜의 CPU 오버헤드를 줄이는 배칭 시스템입니다.

Built-in 파이프라인의 Static/Dynamic Batching은 여러 메쉬를 하나로 합쳐 드로우콜 수 자체를 줄이는 방식입니다.

반면 SRP Batcher는 드로우콜 수는 유지하되, **셰이더 배리언트별 GPU 상태를 캐싱**하여 드로우콜 사이의 상태 전환 비용을 줄입니다.

여기서 상태 전환이란, 다음 드로우콜을 실행하기 전에 CPU가 셰이더 프로그램, 머티리얼 속성, 텍스처 바인딩 등을 GPU에 다시 설정하는 과정입니다. 같은 셰이더를 사용하는 드로우콜이 연속되더라도 매번 이 설정을 반복하면 CPU 시간이 소모됩니다.

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

SRP Batcher가 동작하려면 셰이더가 SRP Batcher **호환(Compatible)**이어야 합니다.

호환 셰이더는 머티리얼 속성을 `UnityPerMaterial` CBUFFER에, 오브젝트 트랜스폼을 `UnityPerDraw` CBUFFER에 올바르게 선언해야 합니다. CBUFFER는 GPU에 데이터를 전달하기 위한 상수 버퍼(Constant Buffer)입니다.

이 규칙을 따르면 머티리얼 속성이 GPU 메모리의 Persistent CBUFFER에 상주하므로, 매 드로우콜마다 CPU가 머티리얼 데이터를 다시 업로드할 필요가 없어집니다.
같은 셰이더 배리언트를 사용하는 드로우콜이 연속되면 셰이더 프로그램 바인딩도 생략되어 CPU 오버헤드가 크게 줄어듭니다. URP의 기본 셰이더(Lit, Unlit 등)는 모두 SRP Batcher 호환입니다.

<br>

SRP가 제공하는 프레임워크 위에서, Unity는 대상 플랫폼과 시각적 품질 수준에 따라 두 가지 공식 파이프라인을 구현했습니다. 먼저 모바일~중급 PC를 겨냥한 URP를 살펴봅니다.

---

## URP (Universal Render Pipeline)

**URP(Universal Render Pipeline)**는 **모바일에서 중급 PC까지**를 대상으로 설계된 SRP 기반 렌더 파이프라인입니다. 성능 효율을 우선시하며, Unity가 가장 적극적으로 개발하는 주력 파이프라인입니다.

### 렌더링 방식

URP의 기본 렌더링 방식은 **싱글패스 포워드 렌더링(Single-pass Forward Rendering)**입니다.

하나의 오브젝트를 그릴 때 모든 조명을 하나의 셰이더 패스 안에서 루프로 처리합니다. Built-in의 멀티패스가 조명 하나당 별도의 패스를 실행하여 드로우콜이 조명 수에 비례했던 것과 달리, URP의 싱글패스에서는 조명 수가 드로우콜 수에 영향을 미치지 않습니다.
이 구조적 차이의 상세한 비교는 [Unity 렌더 파이프라인 (1)](/dev/unity/UnityPipeline-1/)에서 다룹니다.

<br>

Unity 2021.2 이상(URP 12+)에서는 **Deferred Rendering**도 선택할 수 있습니다. URP의 Deferred는 G-Buffer에 기하 정보를 기록한 뒤 화면 공간에서 라이팅을 처리하는 방식으로, 조명 수가 많은 씬에서 Forward보다 효율적일 수 있습니다. 다만, G-Buffer의 추가 메모리와 대역폭이 필요하므로 모바일에서는 Forward가 여전히 기본 선택입니다.

<br>

Unity 2022.2 이상(URP 14.0+)에서는 **Forward+ 렌더링**도 선택할 수 있습니다. Forward+는 화면을 작은 타일 단위로 나눈 뒤, 각 타일에 실제로 영향을 미치는 조명만 골라내어 계산하는 방식입니다. 기본 싱글패스 포워드에서는 오브젝트당 추가 라이트 수가 제한되지만, Forward+에서는 이 제한이 사라집니다. 대신 카메라 단위의 최대 가시 라이트 수 제한이 적용되며, 데스크톱에서는 Main Light 포함 최대 256개, 모바일에서는 Main Light 포함 최대 32개까지 지원됩니다.

### 라이트 제한

URP의 기본 설정에서 씬에 영향을 미치는 라이트는 **메인 Directional Light 1개 + 추가 라이트 N개**입니다.
오브젝트 하나에 동시에 영향을 미치는 추가 라이트의 수는 URP Asset의 Per Object Limit 슬라이더로 지정하며, 기본값 4개에서 최대 8개까지 설정할 수 있습니다. 이 제한을 초과하는 추가 라이트는 자동으로 무시됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- Title -->
  <text x="280" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP의 라이트 구조</text>
  <!-- Main Light box (emphasized) -->
  <rect x="30" y="42" width="500" height="105" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Main Light (Directional Light, 1개)</text>
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
  <text x="280" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.7">모바일 권장: Main Light 1 + Additional Light 2~4</text>
</svg>
</div>

<br>

모바일에서는 추가 라이트 수를 2~4개로 제한하고, 추가 라이트의 그림자는 꼭 필요한 경우에만 활성화하는 것이 일반적입니다.

### Renderer Feature

싱글패스 포워드 렌더링과 라이트 제한으로 기본 렌더링 흐름이 정해지지만, 프로젝트마다 기본 흐름에 없는 추가 효과가 필요한 경우가 있습니다.
URP에서는 이러한 추가 효과를 **ScriptableRendererFeature**로 구현합니다. Renderer Feature는 URP의 렌더링 파이프라인 실행 도중 특정 시점(예: 불투명 렌더링 직후, 후처리 직전)에 개발자가 작성한 커스텀 렌더 패스를 삽입하는 구조입니다.
여기서 렌더 패스(Render Pass)란 특정 종류의 오브젝트를 그리거나 화면 효과를 적용하는 하나의 렌더링 단위를 가리킵니다.

<br>

아웃라인 효과를 위해 Opaque 렌더링 이후에 별도 패스를 추가하거나, 특정 레이어의 오브젝트만 별도로 렌더링하여 후처리용 마스크를 생성하거나, 커스텀 블러 패스를 삽입하는 것 등이 가능합니다.
Built-in의 CommandBuffer 삽입과 달리, 파이프라인 구조 안에서 정식으로 패스를 추가하는 방식이므로 Render Graph의 자동 최적화 대상에도 포함됩니다.

### Camera Stacking

URP의 멀티 카메라 구조는 [Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 다룬 **Camera Stacking**입니다.
Base Camera 위에 Overlay Camera를 쌓는 구조이며, Overlay Camera는 Base Camera의 렌더링 루프 안에서 실행됩니다.

Overlay Camera가 독립적인 Render Target을 생성하지 않고 Base Camera의 Render Target에 직접 그리므로, 별도의 RT 할당과 전환 비용이 줄어듭니다. UI, 무기 뷰, 미니맵 등 별도 레이어가 필요한 경우에 Camera Stacking으로 분리하면 렌더링 순서를 명확하게 관리할 수 있습니다.

### 2D Renderer

URP는 3D 렌더링뿐 아니라 **2D Renderer**도 제공합니다. 2D Renderer는 Sprite를 대상으로 한 2D 라이팅, 2D 그림자, Shape Light 등을 지원합니다.

Built-in 파이프라인에서는 2D 전용 라이팅 시스템이 없어 스프라이트에 동적 조명을 적용하려면 커스텀 셰이더를 직접 작성해야 했습니다. URP의 2D Renderer는 이 기능을 기본으로 제공하므로, 2D 게임에서도 커스텀 작업 없이 동적 조명과 그림자를 사용할 수 있습니다.

<br>

**Shape Light**(Light 2D)는 URP의 2D 전용 광원 컴포넌트로, Freeform(자유 형태), Sprite(텍스처 기반), Point(점 광원), Global(전역 조명) 유형을 제공합니다. 3D 렌더링에서 라이트가 메쉬 표면의 Normal을 기준으로 밝기를 계산하듯, 2D Renderer에서도 스프라이트에 Normal Map을 적용하면 광원 방향에 따라 입체감 있는 조명을 표현할 수 있습니다.

### 모바일 최적화 특성

URP가 모바일에 적합한 이유는 구조적입니다. 앞서 살펴본 싱글패스 포워드 렌더링으로 조명 수에 비례하는 드로우콜 증가를 방지하고, SRP Batcher로 드로우콜의 CPU 오버헤드를 줄입니다.

<br>

렌더 패스 설계 측면에서도 Render Target 전환을 최소화하도록 구성되어 있습니다.
[Unity 렌더링 (2)](/dev/unity/UnityRendering-2/)에서 다룬 것처럼, 모바일 GPU에서 Render Target 전환은 Resolve/Load 비용을 유발하므로 전환 횟수를 줄이는 것이 대역폭 절약에 직결됩니다.
MSAA(Multi-Sample Anti-Aliasing)도 기본 지원하며, 모바일 GPU의 타일 메모리 구조에서는 MSAA 샘플이 타일 메모리 안에서만 유지되고 외부 메모리로 나가지 않으므로 대역폭 비용이 거의 발생하지 않습니다. Unity 6 이상에서는 Render Graph가 기본 적용되어, 불필요한 렌더 패스의 자동 제거와 RT 메모리 재사용으로 대역폭과 메모리 효율이 한층 개선됩니다.

<br>

URP가 성능 효율에 초점을 맞춘 파이프라인이라면, 시각적 품질의 상한을 끌어올리기 위한 파이프라인이 HDRP입니다.

---

## HDRP (High Definition Render Pipeline)

**HDRP(High Definition Render Pipeline)**는 **고사양 PC와 콘솔**을 대상으로 설계된 SRP 기반 렌더 파이프라인입니다. 시각적 품질을 최우선으로 두며, Area Light, Volumetric Fog, Sub-Surface Scattering 등 물리 기반 라이팅의 고급 기능을 제공합니다.

### 렌더링 방식

HDRP의 기본 렌더링 방식은 **Deferred Rendering**입니다. G-Buffer에 기하 정보를 먼저 기록하고 라이팅을 화면 공간에서 처리합니다.
Forward Rendering도 선택할 수 있습니다. 다만 G-Buffer는 픽셀당 하나의 표면 정보만 저장하므로, 여러 표면의 색상을 겹쳐 혼합해야 하는 반투명 오브젝트는 처리할 수 없습니다.

Hair(머리카락)나 Fabric(직물)처럼 복잡한 BRDF를 사용하는 셰이더도, G-Buffer의 한정된 채널로는 필요한 모든 표면 데이터를 저장할 수 없으므로 Forward로만 렌더링됩니다. 이런 머티리얼만 Forward로 처리하고 나머지는 Deferred로 처리하는 혼합 방식이 실무에서 자주 사용됩니다.

<br>

Deferred Rendering은 조명 수에 드로우콜이 비례하지 않는다는 장점이 있지만, G-Buffer가 여러 장의 Render Target을 사용하므로 메모리와 대역폭 요구량이 큽니다.
HDRP의 G-Buffer는 기본 4장의 RT로 구성되며, Light Layers나 Shadow Mask 기능을 활성화하면 각각 RT가 추가되어 최대 6장까지 확장됩니다. Full HD 해상도 기준, 4장일 때 약 32MB, 6장일 때 약 48MB의 추가 메모리를 소비합니다.

### 고급 라이팅 기능

HDRP는 URP에서 지원하지 않는 고급 라이팅 기능을 제공합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">HDRP 고급 라이팅 기능</text>
  <!-- Card 1: Area Light (top-left) -->
  <rect x="15" y="42" width="275" height="148" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="152" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Area Light</text>
  <line x1="35" y1="74" x2="270" y2="74" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="35" y="96" font-family="sans-serif" font-size="11" fill="currentColor">면적을 가진 광원</text>
  <text x="35" y="114" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(사각형, 디스크 등)</text>
  <text x="35" y="138" font-family="sans-serif" font-size="11" fill="currentColor">점 광원보다 사실적인 부드러운 그림자</text>
  <text x="35" y="160" font-family="sans-serif" font-size="11" fill="currentColor">계산 비용이 높음</text>
  <text x="35" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">(레이 트레이싱 또는 근사)</text>
  <!-- Card 2: Volumetric Fog (top-right) -->
  <rect x="310" y="42" width="275" height="148" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="447" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Volumetric Fog</text>
  <line x1="330" y1="74" x2="565" y2="74" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="330" y="96" font-family="sans-serif" font-size="11" fill="currentColor">3D 공간에서 빛이 안개/입자에</text>
  <text x="330" y="114" font-family="sans-serif" font-size="11" fill="currentColor">산란하는 효과</text>
  <text x="330" y="138" font-family="sans-serif" font-size="11" fill="currentColor">광선이 안개를 통과하며 밝아지는</text>
  <text x="330" y="156" font-family="sans-serif" font-size="11" fill="currentColor">God Ray 표현 가능</text>
  <text x="330" y="178" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">볼류메트릭 렌더링 패스 추가</text>
  <!-- Card 3: Sub-Surface Scattering (bottom-left) -->
  <rect x="15" y="205" width="275" height="148" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="152" y="229" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Sub-Surface Scattering (SSS)</text>
  <line x1="35" y1="237" x2="270" y2="237" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="35" y="259" font-family="sans-serif" font-size="11" fill="currentColor">빛이 표면 아래로 투과하여</text>
  <text x="35" y="277" font-family="sans-serif" font-size="11" fill="currentColor">산란하는 효과</text>
  <text x="35" y="301" font-family="sans-serif" font-size="11" fill="currentColor">피부, 왁스, 나뭇잎 등</text>
  <text x="35" y="319" font-family="sans-serif" font-size="11" fill="currentColor">반투과 재질의 사실적 표현</text>
  <text x="35" y="341" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">별도의 SSS 프로파일과 렌더링 패스 필요</text>
  <!-- Card 4: Screen Space Reflection (bottom-right) -->
  <rect x="310" y="205" width="275" height="148" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="447" y="229" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Screen Space Reflection (SSR)</text>
  <line x1="330" y1="237" x2="565" y2="237" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <text x="330" y="259" font-family="sans-serif" font-size="11" fill="currentColor">화면 공간에서 반사를 계산</text>
  <text x="330" y="283" font-family="sans-serif" font-size="11" fill="currentColor">Reflection Probe보다</text>
  <text x="330" y="301" font-family="sans-serif" font-size="11" fill="currentColor">동적이고 정밀한 반사</text>
  <text x="330" y="325" font-family="sans-serif" font-size="11" fill="currentColor">G-Buffer의 깊이와 노멀을 활용</text>
</svg>
</div>

<br>

이 기능들은 모두 추가적인 렌더링 패스나 GPU 연산을 수반하므로, 각각을 활성화할 때마다 프래그먼트 셰이더 비용과 메모리 사용량이 증가합니다.

### Lit Shader

위와 같은 고급 라이팅 기능을 활용하려면 셰이더도 이에 대응해야 합니다.
HDRP의 기본 셰이더인 **Lit Shader**는 Standard(일반 표면), Sub-Surface Scattering(피부 등), Anisotropy(머리카락, 브러시드 메탈 등), Iridescence(비눗방울, 기름막 등), Specular Color(비금속 스페큘러 직접 지정) 등의 표면 유형을 지원합니다. Anisotropy는 반사 특성이 방향에 따라 달라지는 재질, Iridescence는 보는 각도에 따라 색상이 변하는 재질을 표현합니다.

<br>

각 표면 유형에 따라 셰이더 내부의 BRDF 계산이 달라집니다. BRDF(Bidirectional Reflectance Distribution Function)는 빛이 표면에 닿았을 때 어떤 방향으로 얼마나 반사되는지를 수학적으로 정의하는 함수로, 표면 유형이 복잡할수록 BRDF 계산에 포함되는 항이 늘어나 프래그먼트 셰이더 비용이 증가합니다.

### Frame Settings

HDRP는 고급 라이팅 기능이 많은 만큼, 모든 카메라에서 모든 기능을 활성화하면 GPU 비용이 과도해질 수 있습니다.

**Frame Settings**는 이 문제를 해결하기 위해 카메라별로 렌더링 기능을 개별적으로 켜거나 끌 수 있게 해주는 설정입니다. 예를 들어, 메인 카메라에서는 Volumetric Fog와 SSR을 활성화하되, 미니맵 카메라에서는 이 기능들을 모두 비활성화하여 비용을 줄일 수 있습니다. 반사 프로브(Reflection Probe) 렌더링이나 실시간 그림자 캐스케이드 수도 카메라별로 다르게 지정할 수 있습니다. 이 설정은 카메라 컴포넌트의 Frame Settings 오버라이드에서 관리합니다.

### 제약사항

HDRP는 **모바일을 지원하지 않습니다.** G-Buffer 메모리, 고급 라이팅의 GPU 요구사항, 높은 대역폭 소비가 모바일 환경과 맞지 않기 때문입니다. 모바일 GPU의 타일 기반 렌더링 구조에서는 G-Buffer가 요구하는 다중 Render Target의 대역폭 비용이 특히 큽니다.

HDRP의 최소 요구 사양은 DirectX 11 / Metal / Vulkan을 지원하면서 **Compute Shader와 Shader Model 5.0**을 지원하는 GPU입니다.
OpenGL과 OpenGL ES는 지원하지 않으므로, 이 API만 사용하는 기기에서는 HDRP를 실행할 수 없습니다.
콘솔에서는 PlayStation 4, Xbox One 이상입니다. 대상 플랫폼이 PC(중급 이상) 또는 콘솔이고 시각적 품질이 최우선인 프로젝트에서 선택하는 파이프라인입니다.

<br>

URP와 HDRP가 대부분의 프로젝트를 커버하지만, 두 파이프라인 모두 맞지 않는 특수한 요구사항이 있을 수 있습니다.

---

## Custom SRP

URP와 HDRP 외에, SRP 프레임워크를 사용하여 **렌더 파이프라인을 직접 구현**하는 것도 가능합니다. `RenderPipeline` 클래스를 상속받아 렌더링 루프를 처음부터 작성하는 방식입니다.

### 활용 사례

프로젝트가 특수한 시각적 스타일을 요구하여 기존 파이프라인으로 구현이 어려운 경우에 Custom SRP를 고려합니다.
셀 셰이딩(Cel Shading, 만화처럼 명암을 단계적으로 나누어 표현하는 기법) 전용 파이프라인, 복셀(Voxel, 3D 공간을 작은 정육면체 단위로 구성하는 방식) 렌더링 전용 파이프라인, 특정 장르에 최적화된 경량 파이프라인 등이 예입니다.

학습 목적으로도 Custom SRP 구현이 유용합니다. 컬링, 정렬, 드로우콜 생성, Render Target 관리를 직접 구현해보면, URP나 HDRP가 내부에서 수행하는 작업을 구체적으로 파악할 수 있습니다.

<br>

**Custom SRP의 최소 구현 구조**

```csharp
class CustomRenderPipeline : RenderPipeline
{
    protected override void Render(
        ScriptableRenderContext context, Camera[] cameras)
    {
        foreach (Camera camera in cameras)
        {
            // (1) 컬링
            if (!camera.TryGetCullingParameters(out var cullingParams))
                continue;
            var cullingResults = context.Cull(ref cullingParams);

            // (2) 카메라 설정 (VP 행렬 등)
            context.SetupCameraProperties(camera);

            // (3) Clear
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
            var drawingSettings = new DrawingSettings(
                shaderTagId, sortingSettings);
            var filteringSettings = new FilteringSettings(
                RenderQueueRange.opaque);
            context.DrawRenderers(
                cullingResults, ref drawingSettings,
                ref filteringSettings);

            // (5) 반투명 오브젝트 렌더링
            sortingSettings.criteria =
                SortingCriteria.CommonTransparent;
            drawingSettings.sortingSettings = sortingSettings;
            filteringSettings.renderQueueRange =
                RenderQueueRange.transparent;
            context.DrawRenderers(
                cullingResults, ref drawingSettings,
                ref filteringSettings);

            // (6) GPU에 제출
            context.Submit();
        }
    }
}
```

<br>

위 코드에서 `shaderTagId`는 렌더링에 사용할 셰이더 패스를 식별하는 태그입니다. 셰이더의 `Tags { "LightMode" = "..." }` 값과 일치하는 패스만 실행됩니다.

<br>

렌더 파이프라인의 핵심 흐름은 컬링 → 정렬 → 드로우콜 생성 → GPU 제출이며, 위의 Custom SRP 코드가 그 흐름을 그대로 보여줍니다. URP와 HDRP도 동일한 흐름을 기반으로, 라이팅·그림자·후처리 등의 단계를 추가한 형태입니다.

### 유지보수 부담

Custom SRP의 가장 큰 단점은 **유지보수 부담**입니다.

URP와 HDRP는 Unity 팀이 지속적으로 업데이트하며, 새로운 GPU 기능 지원, 버그 수정, 성능 최적화를 반영합니다.
Custom SRP는 이 모든 것을 직접 관리해야 합니다. Unity 버전 업그레이드 시 SRP API가 변경되면 Custom SRP도 함께 수정해야 하며, 새 플랫폼을 지원하려면 해당 GPU 특성에 맞는 최적화를 직접 구현해야 합니다.

프로젝트의 특수한 요구사항이 URP의 Renderer Feature나 Render Graph로 해결 가능하다면, Custom SRP보다 URP 위에서 확장하는 것이 유지보수 비용 면에서 유리합니다.

<br>

지금까지 Built-in, URP, HDRP, Custom SRP 네 가지 선택지를 다루었습니다. 이제 각 파이프라인의 특성을 바탕으로 실제 프로젝트에서의 선택 기준을 정리합니다.

---

## 파이프라인 선택 기준

파이프라인 변경 비용이 크므로, 렌더 파이프라인은 프로젝트 초기에 결정해야 합니다. 주요 선택 기준은 대상 플랫폼과 시각적 목표이며, 셰이더 호환성과 변경 비용도 함께 고려해야 합니다.

### 비교 표

앞에서 다룬 세 파이프라인의 주요 특성을 항목별로 비교하면 다음과 같습니다.

<br>

| 항목 | Built-in | URP | HDRP |
|---|---|---|---|
| 대상 플랫폼 | 모든 플랫폼<br>(레거시) | 모바일 ~ PC<br>(주력) | PC / 콘솔<br>(고사양) |
| Forward 렌더링 | O (멀티패스) | O (싱글패스) | O (선택) |
| Deferred 렌더링 | O | O (선택) | O (기본) |
| 라이트 제한 | 제한 없음<br>(비용 비례) | Forward:<br>Per Object 4~8<br>Forward+/Def:<br>제한 없음 | 제한 없음<br>(G-Buffer 기반) |
| 셰이더 | Surface Shader | Shader Graph /<br>HLSL | Shader Graph /<br>HLSL |
| 커스텀 패스 | CommandBuffer<br>(제한적) | Renderer Feature | Custom Pass<br>(Volume 기반) |
| SRP Batcher | X | O | O |
| Render Graph | X | O (Unity 6+) | O |
| 모바일 지원 | O (비효율) | O (최적화) | X |
| 고급 라이팅 | 제한적 | 기본 수준 | Area Light,<br>SSS, Vol. Fog |
| 업데이트 상태 | 레거시<br>(동결) | 활발 | 활발 |

<br>

표에서 드러나듯, Built-in은 레거시로 동결된 상태이고, URP와 HDRP는 각각 대상 플랫폼과 시각적 품질 수준에 따라 명확히 구분됩니다. 이 구분을 바탕으로 실제 선택 기준을 항목별로 살펴봅니다.

### 대상 플랫폼

대상 플랫폼이 **모바일**이라면 URP가 유일한 현실적 선택입니다. HDRP는 모바일을 지원하지 않고, Built-in은 멀티패스 드로우콜 비용과 SRP Batcher 미지원으로 모바일에서 성능 병목이 발생합니다.

대상 플랫폼이 **PC/콘솔**이고 시각적 품질이 최우선이라면 HDRP를 선택합니다. Area Light, Volumetric Fog, Sub-Surface Scattering 등이 필요한 프로젝트에서 URP는 이 기능들을 제공하지 않습니다.

대상이 **PC/콘솔이지만 모바일도 고려**하거나, 시각적 요구가 극단적이지 않다면 URP가 적합합니다. URP는 PC에서도 충분한 시각적 품질을 제공하며, Forward+ 렌더링으로 조명 제한도 완화할 수 있습니다.

### 셰이더 호환성

**각 파이프라인이 제공하는 기본 셰이더는 서로 호환되지 않습니다.**
Built-in의 Surface Shader는 URP에서 동작하지 않고, URP의 Lit Shader는 HDRP에서 동작하지 않습니다. Core SRP 라이브러리만 사용하는 커스텀 셰이더는 파이프라인 간 동작할 수 있지만, 파이프라인별 기능(라이팅 모델, 셰이더 변수 등)에 의존하는 셰이더는 교체가 필요합니다. 실무에서는 대부분의 머티리얼이 파이프라인별 Lit 셰이더를 사용하므로, 파이프라인 변경 시 사실상 모든 머티리얼을 교체해야 합니다.

Unity는 Built-in에서 URP로의 변환을 돕는 **Render Pipeline Converter**(Window > Rendering > Render Pipeline Converter)와, Built-in에서 HDRP로의 머티리얼 변환 기능(Edit > Rendering > Materials)을 제공합니다.
두 도구 모두 Unity 기본 셰이더의 자동 변환을 지원하지만, 커스텀 셰이더는 새 파이프라인에 맞게 수동으로 다시 작성해야 합니다. 커스텀 셰이더가 많을수록 파이프라인 변경 비용이 증가합니다.

### 파이프라인 변경 비용

셰이더 호환성 문제에서 알 수 있듯, 파이프라인 변경은 셰이더뿐 아니라 프로젝트 전반에 걸친 작업을 수반합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 500" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 제목 -->
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">파이프라인 변경 시 수반되는 작업</text>

  <!-- (1) 셰이더 변환/재작성 -->
  <rect x="20" y="42" width="440" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="48" cy="62" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="48" y="66" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1</text>
  <text x="68" y="66" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">셰이더 변환/재작성</text>
  <text x="48" y="86" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">모든 머티리얼의 셰이더를 새 파이프라인용으로 교체</text>
  <text x="48" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">커스텀 셰이더는 수동 재작성 필요</text>

  <!-- (2) 라이팅 재설정 -->
  <rect x="20" y="132" width="440" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="48" cy="152" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="48" y="156" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2</text>
  <text x="68" y="156" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">라이팅 재설정</text>
  <text x="48" y="176" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">라이트 설정, 그림자 설정, 라이트맵 재베이크</text>
  <text x="48" y="192" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">파이프라인마다 라이팅 파라미터가 다름</text>

  <!-- (3) 후처리 재구성 -->
  <rect x="20" y="222" width="440" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="48" cy="242" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="48" y="246" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3</text>
  <text x="68" y="246" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">후처리 재구성</text>
  <text x="48" y="266" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Built-in의 Post Processing Stack v2 →</text>
  <text x="48" y="282" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">URP/HDRP의 Volume 기반 후처리로 변환</text>

  <!-- (4) Renderer Feature / Custom Pass 이전 -->
  <rect x="20" y="312" width="440" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="48" cy="332" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="48" y="336" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4</text>
  <text x="68" y="336" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Renderer Feature / Custom Pass 이전</text>
  <text x="48" y="356" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">커스텀 렌더링 기능의 API 변경</text>

  <!-- (5) 시각적 결과 검증 -->
  <rect x="20" y="392" width="440" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="48" cy="412" r="12" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="48" y="416" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">5</text>
  <text x="68" y="416" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">시각적 결과 검증</text>
  <text x="48" y="436" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">변환 후 모든 씬에서 시각적 결과가</text>
  <text x="48" y="452" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">의도한 대로 나오는지 확인</text>
</svg>
</div>

<br>

이 비용은 프로젝트 규모에 비례합니다. 씬이 수십 개이고, 커스텀 셰이더가 수십 종이며, 라이트맵이 베이크되어 있는 프로젝트에서 파이프라인을 변경하면 수 주에서 수 개월의 작업이 필요할 수 있습니다. **프로젝트 초기에 파이프라인을 결정하고, 이후 변경하지 않는 것**이 원칙입니다.

---

## 마무리

- **Built-in Render Pipeline**은 Forward와 Deferred를 모두 지원하지만, 렌더링 루프를 수정할 수 없고 멀티패스 구조로 인해 조명이 많을수록 드로우콜이 급증합니다. 레거시 상태이며, 신규 프로젝트에는 권장되지 않습니다.
- **SRP(Scriptable Render Pipeline)**는 렌더링 루프를 C#으로 제어할 수 있는 프레임워크이며, URP와 HDRP의 기반입니다. SRP Batcher는 머티리얼 속성을 GPU 메모리에 상주시키고 같은 셰이더 배리언트의 드로우콜 사이에서 셰이더 바인딩을 생략하여 CPU 오버헤드를 줄입니다.
- **URP**는 모바일~중급 PC를 대상으로 싱글패스 포워드 렌더링, SRP Batcher, Renderer Feature, Camera Stacking, Render Graph를 제공하며 모바일에서 가장 효율적인 선택입니다.
- **HDRP**는 고사양 PC/콘솔을 대상으로 Deferred 기반의 고급 라이팅(Area Light, Volumetric Fog, SSS 등)을 제공하지만, 모바일은 지원하지 않습니다.
- **Custom SRP**는 렌더링 루프를 완전히 제어할 수 있는 반면 유지보수 부담이 큽니다. URP의 Renderer Feature나 Render Graph로 해결 가능한 요구사항이라면 URP 위에서 구현하는 편이 유리합니다.
- **파이프라인별 셰이더는 호환되지 않고** 변경 비용이 크므로, 프로젝트 초기에 대상 플랫폼과 시각적 목표를 기준으로 결정해야 합니다.

<br>

렌더 파이프라인은 한 프레임을 완성하기 위한 렌더링 단계의 전체 구성과 순서를 정의하는 상위 구조입니다. 컬링, 정렬, 라이팅, 후처리의 방식과 순서가 파이프라인에 의해 결정되므로, 어떤 파이프라인을 선택하느냐에 따라 프로젝트의 성능 특성과 시각적 표현 범위가 함께 결정됩니다.

<br>

이 시리즈에서 카메라([Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)), Render Target([Unity 렌더링 (2)](/dev/unity/UnityRendering-2/)), 렌더 파이프라인(이 글)의 기초를 다루었습니다. 이 기초 위에서 [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)의 렌더링 구조, [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)의 라이팅 비용, [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)의 셰이더 성능을 구체적으로 이해할 수 있습니다.

<br>

---

**관련 글**
- [Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조](/dev/unity/UnityPipeline-1/)
- [조명과 그림자 (1) - 실시간 조명과 베이크](/dev/unity/LightingAndShadows-1/)
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)

**시리즈**
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- [Unity 렌더링 (2) - Render Target과 Frame Buffer](/dev/unity/UnityRendering-2/)
- **Unity 렌더링 (3) - Render Pipeline 개요 (현재 글)**

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
- **Unity 렌더링 (3) - Render Pipeline 개요** (현재 글)
