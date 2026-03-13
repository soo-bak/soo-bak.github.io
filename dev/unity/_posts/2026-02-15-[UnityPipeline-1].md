---
layout: single
title: "Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조 - soo:bak"
date: "2026-02-15 16:30:00 +0900"
description: 렌더 파이프라인의 역할, Built-in의 멀티패스 포워드, URP의 싱글패스 포워드와 SRP, Render Graph를 설명합니다.
tags:
  - Unity
  - 최적화
  - 렌더파이프라인
  - URP
  - 모바일
---

## 렌더 파이프라인의 역할

[GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 모바일 GPU가 TBDR(Tile-Based Deferred Rendering) 구조로 동작하는 과정을 살펴보았습니다.

GPU 하드웨어는 정점을 변환하고, 삼각형을 래스터화하고, 픽셀의 색상을 계산하는 물리적인 실행 장치입니다. 하지만 어떤 오브젝트를 어떤 순서로 그릴지, 조명을 어떻게 적용할지는 GPU가 스스로 결정하지 않습니다.

이러한 결정을 CPU가 내리고, GPU가 이를 실행하여 3D 씬 데이터를 최종 화면 이미지로 만드는 전체 처리 흐름을 **렌더 파이프라인(Render Pipeline)**이라 합니다.

<br>

렌더 파이프라인에서 CPU가 GPU의 그리기 명령(**드로우콜(Draw Call)**)을 준비하는 과정은 네 단계로 나뉩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 380 510" xmlns="http://www.w3.org/2000/svg" style="max-width: 380px; width: 100%;">
  <!-- Start label -->
  <rect x="90" y="10" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4 2"/>
  <text x="190" y="30" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">화면에 그려야 할 대상</text>
  <!-- Arrow 1 -->
  <line x1="190" y1="42" x2="190" y2="62" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,58 190,68 196,58" fill="currentColor"/>
  <!-- Stage 1: Culling -->
  <rect x="40" y="70" width="300" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="91" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) 컬링 (Culling)</text>
  <text x="190" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">카메라에 보이지 않는 오브젝트를 제외</text>
  <text x="190" y="123" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">그릴 필요가 없는 것은 처음부터 걸러내어 비용을 줄임</text>
  <!-- Arrow 2 -->
  <line x1="190" y1="138" x2="190" y2="158" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,154 190,164 196,154" fill="currentColor"/>
  <!-- Stage 2: Sorting -->
  <rect x="40" y="166" width="300" height="82" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="187" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) 정렬 (Sorting)</text>
  <text x="190" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">남은 오브젝트의 렌더링 순서를 결정</text>
  <text x="190" y="219" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">불투명 오브젝트: 앞에서 뒤로 (오버드로우 감소)</text>
  <text x="190" y="234" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">투명 오브젝트: 뒤에서 앞으로 (올바른 블렌딩)</text>
  <!-- Arrow 3 -->
  <line x1="190" y1="248" x2="190" y2="268" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,264 190,274 196,264" fill="currentColor"/>
  <!-- Stage 3: Lighting Pass -->
  <rect x="40" y="276" width="300" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="297" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) 라이팅 패스 (Lighting Pass)</text>
  <text x="190" y="314" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">조명을 어떻게 적용할지 결정</text>
  <text x="190" y="329" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">조명마다 별도 패스 또는 한 번에 모든 조명</text>
  <!-- Arrow 4 -->
  <line x1="190" y1="344" x2="190" y2="364" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,360 190,370 196,360" fill="currentColor"/>
  <!-- Stage 4: Draw Call -->
  <rect x="40" y="372" width="300" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="393" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(4) 드로우콜 생성 및 제출</text>
  <text x="190" y="410" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">GPU에 보낼 그리기 명령을 구성하여 제출</text>
  <text x="190" y="425" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">"이 메쉬를, 이 머티리얼로, 이 셰이더로 그려라"</text>
  <!-- Arrow 5 -->
  <line x1="190" y1="440" x2="190" y2="460" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,456 190,466 196,456" fill="currentColor"/>
  <!-- End label -->
  <rect x="90" y="468" width="200" height="32" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4 2"/>
  <text x="190" y="488" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">GPU가 화면을 렌더링</text>
</svg>
</div>

<br>

렌더 파이프라인이 이 네 단계를 처리하는 방식은 파이프라인의 종류에 따라 달라지며, 이 차이가 렌더링 성능과 표현 범위에 직접 영향을 줍니다.

<br>

Unity에는 여러 종류의 렌더 파이프라인이 존재합니다.

가장 먼저 제공된 것이 **Built-in 렌더 파이프라인**이고, 모바일을 포함한 넓은 범위의 플랫폼에서 성능을 우선시하는 것이 **URP(Universal Render Pipeline)**, PC와 콘솔에서 고품질 비주얼을 목표로 하는 것이 **HDRP(High Definition Render Pipeline)**입니다.

URP는 넓은 플랫폼 호환성과 런타임 성능에 초점을 맞추고, HDRP는 Volumetric Lighting, Subsurface Scattering, Ray Tracing 등 고급 렌더링 기능을 지원하는 대신 높은 하드웨어 사양을 요구합니다.

<br>

Built-in과 URP는 셰이더 시스템, 포스트 프로세싱, 카메라 구조 등 여러 면에서 다르지만, 렌더링 성능에 가장 직접적인 영향을 미치는 차이는 **조명 처리 방식**과 **배칭 구조**입니다. 이 글에서는 조명 처리 방식의 차이를 다루고, 배칭은 [Part 2](/dev/unity/UnityPipeline-2/)에서 이어집니다.

---

## 포워드 렌더링 (Forward Rendering)

Built-in과 URP 모두 **포워드 렌더링(Forward Rendering)**을 기본 렌더링 방식으로 사용합니다.

포워드 렌더링은 오브젝트를 하나씩 그리면서 지오메트리 처리와 조명 계산을 분리하지 않고 수행하여, 최종 픽셀 색상을 바로 출력하는 방식입니다.

### 멀티패스 포워드 렌더링

Built-in 파이프라인의 포워드 렌더링은 하나의 오브젝트를 조명 수만큼 반복해서 그리는 **멀티패스(Multi-pass)** 방식으로 동작합니다. 조명 하나당 별도의 렌더링 패스를 실행하므로, 조명이 3개이면 같은 오브젝트를 3번 그립니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- Title -->
  <text x="240" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">오브젝트 A에 조명 3개가 영향을 미치는 경우</text>

  <!-- Pass 1 box -->
  <rect x="30" y="42" width="330" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="60" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">패스 1 (ForwardBase)</text>
  <text x="45" y="76" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">메인 Directional Light + 환경광 + 그림자</text>
  <!-- Draw call 1 -->
  <line x1="360" y1="64" x2="388" y2="64" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="386,60 394,64 386,68" fill="currentColor" opacity="0.4"/>
  <text x="400" y="68" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">드로우콜 1</text>

  <!-- Arrow 1 -->
  <line x1="195" y1="86" x2="195" y2="118" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="190,115 195,125 200,115" fill="currentColor"/>
  <text x="215" y="108" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">가산 블렌딩</text>

  <!-- Pass 2 box -->
  <rect x="30" y="126" width="330" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="144" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">패스 2 (ForwardAdd)</text>
  <text x="45" y="160" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">추가 Point Light</text>
  <!-- Draw call 2 -->
  <line x1="360" y1="148" x2="388" y2="148" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="386,144 394,148 386,152" fill="currentColor" opacity="0.4"/>
  <text x="400" y="152" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">드로우콜 2</text>

  <!-- Arrow 2 -->
  <line x1="195" y1="170" x2="195" y2="202" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="190,199 195,209 200,199" fill="currentColor"/>
  <text x="215" y="192" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">가산 블렌딩</text>

  <!-- Pass 3 box -->
  <rect x="30" y="210" width="330" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="45" y="228" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">패스 3 (ForwardAdd)</text>
  <text x="45" y="244" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">추가 Spot Light</text>
  <!-- Draw call 3 -->
  <line x1="360" y1="232" x2="388" y2="232" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="386,228 394,232 386,236" fill="currentColor" opacity="0.4"/>
  <text x="400" y="236" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">드로우콜 3</text>

  <!-- Conclusion -->
  <text x="240" y="284" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">오브젝트 1개 x 조명 3개 = 드로우콜 3회</text>
</svg>
</div>

<br>

첫 번째 패스인 **ForwardBase**는 메인 Directional Light, 환경광(**Ambient**), **라이트맵(Lightmap)**, 그림자 등 씬 전체에 공통으로 적용되는 기본 조명을 한 번에 처리합니다.

추가 조명(Point Light, Spot Light, 추가 Directional Light 등)이 있으면, 조명 하나마다 **ForwardAdd** 패스가 추가로 실행됩니다. ForwardAdd는 같은 오브젝트를 다시 그리면서 해당 조명만 계산하고, 그 결과를 ForwardBase의 픽셀 색상 위에 **가산 블렌딩(Additive Blending)**으로 누적합니다.

조명이 메인 Directional Light 하나뿐인 씬에서는 ForwardAdd가 실행되지 않으므로, ForwardBase 패스만으로 렌더링이 완료됩니다.

### 멀티패스의 비용 계산

멀티패스 구조에서는 조명 하나마다 같은 오브젝트를 다시 그리므로, 드로우콜 수가 오브젝트 수와 조명 수의 곱에 비례합니다.

<br>

오브젝트 10개, 조명 3개(Directional 1 + Point 2) — 오브젝트당 ForwardBase 1회 + ForwardAdd 2회 = 3회, 전체 10 × 3 = 드로우콜 30회

| | ForwardBase (메인+환경광) | ForwardAdd (Point) | ForwardAdd (Point) |
|---|---|---|---|
| 오브젝트 A | ① | ② | ③ |
| 오브젝트 B | ④ | ⑤ | ⑥ |
| 오브젝트 C | ⑦ | ⑧ | ⑨ |
| ... | | | |
| 오브젝트 J | ㉘ | ㉙ | ㉚ |

<br>

### 조명의 품질 등급

이 비용을 줄이기 위해 Unity의 Built-in 파이프라인은 모든 조명에 ForwardAdd 패스를 생성하는 대신, 조명을 품질 등급으로 나누어 처리합니다.
각 오브젝트를 렌더링할 때 조명의 밝기와 오브젝트까지의 거리 등을 기준으로 중요도를 판단하여, **픽셀 라이트(Pixel Light)**, **정점 라이트(Vertex Light)**, **SH 라이트(Spherical Harmonics Light)** 세 등급으로 분류합니다.
이 중 ForwardAdd 패스를 생성하는 것은 픽셀 라이트뿐입니다.

픽셀 라이트로 분류되는 조명의 수는 Quality Settings의 `Pixel Light Count`로 제한되며, 기본값은 4입니다. 이 제한을 초과하는 조명은 정점 라이트 또는 SH 라이트로 강등됩니다.

<br>

픽셀 라이트는 화면의 모든 픽셀에서 각 조명을 개별 계산하며, 세 등급 중 가장 정밀합니다.

정점 라이트는 각 조명을 메쉬의 정점에서만 계산하고, 정점 사이의 표면은 그 값을 부드럽게 이어서 채웁니다.
계산 지점이 정점에만 있으므로, 정점이 적은 로우폴리 메쉬에서는 조명이 뭉개져 보일 수 있습니다.

SH 라이트는 각 조명을 개별적으로 계산하지 않고, 조명 환경 전체를 소수의 수학적 계수(Unity에서는 색상 채널당 9개)로 요약하여 근사합니다. 이 계수는 빛이 대체로 어느 방향에서 오고 전체적으로 어떤 색조를 띠는지 같은 큰 경향만 담을 수 있으므로, 비용이 가장 낮지만 날카로운 그림자 경계나 하이라이트 같은 세밀한 조명 변화는 표현하지 못합니다.

정점 라이트와 SH 라이트는 ForwardBase 패스 안에서 함께 처리되므로 추가 드로우콜이 발생하지 않습니다.

<br>

### 멀티패스의 장점과 단점

멀티패스에서는 각 패스가 조명 하나만 처리하므로 셰이더 구현이 간결합니다. 조명이 늘어도 같은 셰이더로 패스만 추가하면 되므로, 셰이더 자체에 조명 수 제한이 없습니다.

대신 조명이 늘어날수록 비용도 함께 커집니다. 드로우콜이 늘어나 CPU가 GPU 상태를 설정하고 명령을 제출하는 작업이 누적되고, GPU도 같은 오브젝트의 같은 픽셀을 조명마다 반복 셰이딩해야 합니다.

### 디퍼드라는 대안

Built-in 파이프라인은 **디퍼드 렌더링(Deferred Rendering)** 모드도 지원합니다. 포워드 렌더링에서는 오브젝트를 그릴 때 조명까지 함께 계산하지만, 디퍼드 렌더링에서는 이름 그대로 조명 계산을 뒤로 미루어(defer) 오브젝트를 그리는 단계와 조명을 계산하는 단계를 분리합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 330" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- === 포워드 렌더링 === -->
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">포워드 렌더링</text>
  <!-- 오브젝트 A -->
  <rect x="15" y="28" width="570" height="26" rx="4" fill="currentColor" fill-opacity="0.04"/>
  <text x="25" y="46" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">오브젝트 A 드로우콜</text>
  <text x="152" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="167" y="46" font-family="sans-serif" font-size="9.5" fill="currentColor">[정점 → 래스터 → 프래그먼트 : 표면 추출 + 조명 계산]</text>
  <text x="462" y="46" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="477" y="46" font-family="sans-serif" font-size="10" fill="currentColor">프레임버퍼</text>
  <!-- 오브젝트 B -->
  <rect x="15" y="58" width="570" height="26" rx="4" fill="currentColor" fill-opacity="0.04"/>
  <text x="25" y="76" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">오브젝트 B 드로우콜</text>
  <text x="152" y="76" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="167" y="76" font-family="sans-serif" font-size="9.5" fill="currentColor">[정점 → 래스터 → 프래그먼트 : 표면 추출 + 조명 계산]</text>
  <text x="462" y="76" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="477" y="76" font-family="sans-serif" font-size="10" fill="currentColor">프레임버퍼</text>
  <!-- === 구분선 === -->
  <line x1="15" y1="100" x2="585" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>
  <!-- === 디퍼드 렌더링 === -->
  <text x="300" y="122" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">디퍼드 렌더링</text>
  <!-- Geometry Pass 헤더 -->
  <text x="300" y="142" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.45">── Geometry Pass (드로우콜 묶음 1) ──</text>
  <!-- 오브젝트 A -->
  <rect x="15" y="150" width="570" height="26" rx="4" fill="currentColor" fill-opacity="0.04"/>
  <text x="25" y="168" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">오브젝트 A 드로우콜</text>
  <text x="152" y="168" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="167" y="168" font-family="sans-serif" font-size="9.5" fill="currentColor">[정점 → 래스터 → 프래그먼트 : 표면 추출만]</text>
  <text x="408" y="168" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="423" y="168" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">G-Buffer</text>
  <!-- 오브젝트 B -->
  <rect x="15" y="180" width="570" height="26" rx="4" fill="currentColor" fill-opacity="0.04"/>
  <text x="25" y="198" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">오브젝트 B 드로우콜</text>
  <text x="152" y="198" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="167" y="198" font-family="sans-serif" font-size="9.5" fill="currentColor">[정점 → 래스터 → 프래그먼트 : 표면 추출만]</text>
  <text x="408" y="198" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="423" y="198" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">G-Buffer</text>
  <!-- G-Buffer → Lighting Pass 연결 -->
  <line x1="300" y1="212" x2="300" y2="252" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="295,248 300,258 305,248" fill="currentColor"/>
  <!-- Lighting Pass 헤더 -->
  <text x="300" y="270" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.45">── Lighting Pass (드로우콜 묶음 2) ──</text>
  <!-- 라이트 도형 -->
  <rect x="15" y="278" width="570" height="26" rx="4" fill="currentColor" fill-opacity="0.04"/>
  <text x="25" y="296" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">라이트 도형 드로우콜</text>
  <text x="152" y="296" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="167" y="296" font-family="sans-serif" font-size="9.5" fill="currentColor">[정점 → 래스터 → 프래그먼트 : G-Buffer + 조명 계산]</text>
  <text x="462" y="296" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→</text>
  <text x="477" y="296" font-family="sans-serif" font-size="10" fill="currentColor">프레임버퍼</text>
  <text x="25" y="322" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">조명마다 반복</text>
</svg>
</div>

<br>

> 디퍼드 렌더링은 Built-in만의 기능이 아닙니다. URP도 Unity 2021.2(URP 12) 이상에서 Deferred를 선택할 수 있고, HDRP는 Deferred가 기본 렌더링 방식입니다. 다만 G-Buffer의 메모리·대역폭 부담 때문에 모바일에서는 어느 파이프라인이든 Forward가 현실적인 선택입니다. 각 파이프라인의 디퍼드 지원 범위와 차이는 [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)에서 다룹니다.

디퍼드 렌더링의 첫 번째 단계는 모든 오브젝트를 한 번씩 그리는 **Geometry Pass**입니다.
Geometry Pass에서는 각 오브젝트의 정점을 변환하고 래스터화하여 프래그먼트를 생성한 뒤, 프래그먼트 셰이더가 텍스처를 샘플링하고 법선을 계산합니다.
다만 이 단계의 프래그먼트 셰이더는 조명을 계산하지 않고, 표면 정보(색상, 법선, 반사, 깊이 등)를 여러 장의 화면 크기 텍스처에 나누어 기록합니다. 이 텍스처 전체를 **G-Buffer(Geometry Buffer)**라 합니다.

두 번째 단계는 **Lighting Pass**입니다.
G-Buffer가 완성되면 CPU가 조명마다 드로우콜을 하나씩 제출합니다.
각 드로우콜은 씬의 오브젝트 대신 조명의 영향 범위를 나타내는 단순한 도형(Directional Light는 화면 전체를 덮는 사각형, Point Light는 구, Spot Light는 원뿔)을 그리고, 이 도형의 프래그먼트 셰이더가 G-Buffer에서 해당 픽셀의 표면 정보를 읽어 조명 결과를 계산합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 380 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 380px; width: 100%;">
  <!-- Stage 1: Geometry Pass -->
  <rect x="40" y="10" width="300" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="31" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Geometry Pass</text>
  <text x="190" y="49" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">모든 오브젝트의 기하학적 정보를 기록 (조명 계산 없음)</text>
  <!-- Arrow 1 -->
  <line x1="190" y1="62" x2="190" y2="82" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,78 190,88 196,78" fill="currentColor"/>
  <!-- Stage 2: G-Buffer -->
  <rect x="40" y="90" width="300" height="68" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="111" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">G-Buffer</text>
  <text x="190" y="131" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Diffuse(색상)  ·  Normal(법선)</text>
  <text x="190" y="146" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">Specular(반사)  ·  Depth(깊이)</text>
  <!-- Arrow 2 -->
  <line x1="190" y1="158" x2="190" y2="178" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="184,174 190,184 196,174" fill="currentColor"/>
  <!-- Stage 3: Lighting Pass -->
  <rect x="40" y="186" width="300" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="190" y="207" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Lighting Pass</text>
  <text x="190" y="225" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">G-Buffer를 읽어 화면 픽셀 단위로 조명 계산</text>
</svg>
</div>

<br>

멀티패스에서 드로우콜이 오브젝트 수 × 조명 수에 비례한다면, 디퍼드에서는 오브젝트 수 + 조명 수에 비례합니다.
오브젝트는 Geometry Pass에서 한 번만 그리고, 조명이 추가되면 Lighting Pass 드로우콜이 하나만 추가되기 때문입니다.

디퍼드에서 드로우콜은 줄어들지만, G-Buffer에 Diffuse, Normal, Specular, Depth 등의 표면 정보를 각각 화면 크기 텍스처로 유지해야 합니다. 1920×1080 해상도 기준으로 텍스처 하나가 수 MB에 달하며, 이런 텍스처를 여러 장 동시에 유지하면 매 프레임 수십 MB의 메모리 읽기/쓰기가 발생합니다.

데스크톱·콘솔 GPU는 이 대역폭을 감당할 수 있어 디퍼드 렌더링이 널리 사용됩니다. 하지만 [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 살펴본 것처럼 모바일 GPU는 메모리 대역폭이 제한적이고, TBDR 구조의 온칩 타일 메모리도 한정되어 있습니다. 이 환경에서 매 프레임 G-Buffer 여러 장을 읽고 쓰는 부담은 크므로, 모바일에서 Built-in Deferred는 현실적인 선택이 되지 못합니다.

결국 Built-in 파이프라인에서 모바일 게임이 선택할 수 있는 현실적인 방식은 포워드 렌더링이며, 멀티패스로 인한 드로우콜 증가가 주요 병목으로 남습니다.

---

## SRP와 URP의 등장

Built-in 파이프라인에는 성능 문제 외에 구조적 한계도 있었습니다.
렌더링 과정(컬링, 정렬, 라이팅 패스, 드로우콜 제출)이 Unity 엔진 내부의 C++ 코드에 고정되어 있어, 불필요한 패스를 제거하거나 프로젝트에 맞는 커스텀 패스를 추가하려면 엔진 소스 코드를 직접 수정해야 했습니다.

Unity는 이 한계를 해결하기 위해 2018년(Unity 2018.1)에 **SRP(Scriptable Render Pipeline)** 아키텍처를 도입했습니다.

### SRP란

SRP는 렌더링 과정을 C# 스크립트로 제어할 수 있게 하는 프레임워크입니다.
Built-in에서 엔진이 강제하던 렌더링 흐름을, 개발자가 렌더 패스를 추가하거나 제거하거나 수정하는 방식으로 직접 정의할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 450 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 450px; width: 100%;">
  <!-- Built-in Section -->
  <text x="225" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Built-in 파이프라인</text>
  <rect x="30" y="30" width="390" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Unity 엔진 (C++) — 렌더링 과정 고정</text>
  <text x="225" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">컬링 → 정렬 → ForwardBase → ForwardAdd</text>
  <text x="225" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(수정 불가)</text>
  <!-- SRP Section -->
  <text x="225" y="162" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">SRP 아키텍처</text>
  <rect x="30" y="174" width="390" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="196" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Unity 엔진 (C++) — SRP Core</text>
  <text x="225" y="216" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">컬링, 커맨드 버퍼, 렌더 타겟 관리</text>
  <line x1="225" y1="234" x2="225" y2="274" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="220,270 225,280 230,270" fill="currentColor"/>
  <text x="245" y="260" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">C# API</text>
  <rect x="30" y="282" width="390" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="304" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">렌더 파이프라인 (C# 스크립트)</text>
  <text x="225" y="324" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">렌더 패스 구성, 실행 순서, 리소스 관리</text>
  <text x="225" y="346" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">(개발자가 수정 가능)</text>
</svg>
</div>

<br>

SRP Core는 컬링 실행, **커맨드 버퍼(Command Buffer)** 구성, **렌더 타겟(Render Target)** 관리 등 렌더링에 필요한 기본 기능을 C# API로 제공합니다. URP와 HDRP는 이 API를 사용하여 각자의 렌더링 방식을 구현한 파이프라인입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <rect x="120" y="10" width="220" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="28" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SRP Core</text>
  <text x="230" y="44" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">저수준 렌더링 C# API</text>
  <line x1="175" y1="54" x2="120" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="115,83 120,93 125,83" fill="currentColor"/>
  <line x1="285" y1="54" x2="340" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="335,83 340,93 345,83" fill="currentColor"/>
  <rect x="20" y="94" width="200" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="120" y="118" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">URP</text>
  <text x="120" y="140" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">모바일/범용</text>
  <text x="120" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">성능 우선</text>
  <text x="120" y="176" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">싱글패스 포워드</text>
  <rect x="240" y="94" width="200" height="110" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="118" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">HDRP</text>
  <text x="340" y="140" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">고사양 PC/콘솔 전용</text>
  <text x="340" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">시각 품질 우선</text>
  <text x="340" y="176" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">디퍼드 + 포워드</text>
</svg>
</div>

---

## URP의 포워드 렌더링

URP가 싱글패스로 드로우콜을 줄이는 구조와, 렌더 패스가 어떻게 구성되는지 살펴봅니다.

### 싱글패스 포워드 렌더링

URP는 멀티패스 대신 **싱글패스 포워드 렌더링(Single-pass Forward Rendering)**을 사용합니다.
멀티패스에서는 조명마다 별도의 드로우콜로 셰이더를 다시 실행했다면, 싱글패스에서는 오브젝트를 그리는 드로우콜 하나에서 프래그먼트 셰이더가 모든 조명을 순회하며 최종 색상을 계산합니다.
Built-in의 ForwardBase와 ForwardAdd가 하나로 합쳐진 셈이며, URP에서는 이 통합 패스를 **ForwardLit**이라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <!-- Title -->
  <text x="300" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">오브젝트 2개, 조명 3개인 씬</text>

  <!-- Left column: Built-in 멀티패스 -->
  <rect x="10" y="35" width="280" height="270" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4 2"/>
  <text x="150" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Built-in 멀티패스</text>

  <!-- Object A -->
  <text x="30" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">오브젝트 A</text>
  <rect x="30" y="88" width="110" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="85" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">메인 라이트</text>
  <line x1="140" y1="99" x2="192" y2="99" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,95 197,99 189,103" fill="currentColor"/>
  <rect x="198" y="88" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="236" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ①</text>

  <rect x="30" y="114" width="110" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="85" y="129" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">추가 라이트 1</text>
  <line x1="140" y1="125" x2="192" y2="125" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,121 197,125 189,129" fill="currentColor"/>
  <rect x="198" y="114" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="236" y="129" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ②</text>

  <rect x="30" y="140" width="110" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="85" y="155" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">추가 라이트 2</text>
  <line x1="140" y1="151" x2="192" y2="151" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,147 197,151 189,155" fill="currentColor"/>
  <rect x="198" y="140" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="236" y="155" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ③</text>

  <!-- Object B -->
  <text x="30" y="182" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">오브젝트 B</text>
  <rect x="30" y="190" width="110" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="85" y="205" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">메인 라이트</text>
  <line x1="140" y1="201" x2="192" y2="201" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,197 197,201 189,205" fill="currentColor"/>
  <rect x="198" y="190" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="236" y="205" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ④</text>

  <rect x="30" y="216" width="110" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="85" y="231" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">추가 라이트 1</text>
  <line x1="140" y1="227" x2="192" y2="227" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,223 197,227 189,231" fill="currentColor"/>
  <rect x="198" y="216" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="236" y="231" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ⑤</text>

  <rect x="30" y="242" width="110" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="85" y="257" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">추가 라이트 2</text>
  <line x1="140" y1="253" x2="192" y2="253" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="189,249 197,253 189,257" fill="currentColor"/>
  <rect x="198" y="242" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="236" y="257" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ⑥</text>

  <!-- Left total -->
  <rect x="30" y="275" width="244" height="22" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="152" y="290" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합계: 6회</text>

  <!-- Right column: URP 싱글패스 -->
  <rect x="310" y="35" width="280" height="270" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4 2"/>
  <text x="450" y="55" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">URP 싱글패스</text>

  <!-- Object A -->
  <text x="330" y="80" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">오브젝트 A</text>
  <rect x="330" y="88" width="120" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">모든 조명 (3개)</text>
  <line x1="450" y1="99" x2="492" y2="99" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="489,95 497,99 489,103" fill="currentColor"/>
  <rect x="498" y="88" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="536" y="103" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ①</text>

  <!-- Object B -->
  <text x="330" y="138" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">오브젝트 B</text>
  <rect x="330" y="146" width="120" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="161" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">모든 조명 (3개)</text>
  <line x1="450" y1="157" x2="492" y2="157" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="489,153 497,157 489,161" fill="currentColor"/>
  <rect x="498" y="146" width="76" height="22" rx="3" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="536" y="161" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">드로우콜 ②</text>

  <!-- Right total -->
  <rect x="330" y="275" width="244" height="22" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="452" y="290" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">합계: 2회</text>
</svg>
</div>

<br>

위 다이어그램처럼 URP 싱글패스에서는 조명 수와 관계없이 오브젝트당 드로우콜이 1회이므로, 전체 드로우콜은 오브젝트 수에만 비례합니다.

### 드로우콜 감소 효과

같은 씬 구성(오브젝트 10개, 조명 3개)으로 비교하면, ForwardLit 패스가 오브젝트당 1회 실행되므로 오브젝트 10개 × 1 = 드로우콜 10회입니다.

<br>

| 씬 구성 | Built-in 멀티패스 | URP 싱글패스 |
|---|---|---|
| 오브젝트 10, 조명 3 | 30회 | 10회 |
| 오브젝트 50, 조명 4 | 200회 | 50회 |
| 오브젝트 100, 조명 4 | 400회 | 100회 |


공식으로 표현하면 Built-in은 `오브젝트 수 × 조명 수`, URP는 `오브젝트 수`입니다. 조명이 늘어날수록 차이가 커집니다.

<br>

다만 URP에서도 오브젝트당 추가 조명 수에는 제한이 있습니다. 메인 Directional Light를 제외한 추가 조명은 오브젝트당 최대 8개까지 처리됩니다.

이 제한을 적용하기 위해 URP는 렌더링 전에 각 오브젝트에 영향을 미치는 조명을 선별합니다.
Point Light와 Spot Light는 범위(Range)를 가지므로 오브젝트의 바운딩 볼륨이 이 범위와 겹치는 조명만 후보가 되고, 추가 Directional Light는 범위 제한이 없으므로 항상 후보에 포함됩니다.
URP는 이 후보를 밝기와 오브젝트까지의 거리를 기준으로 중요도 순으로 정렬한 뒤, 상위 8개만 선별하여 오브젝트별 조명 인덱스 리스트로 구성하고 GPU 메모리의 상수 버퍼에 기록합니다.

상위 8개 밖의 조명은 해당 오브젝트에 아예 반영되지 않습니다. 예를 들어 씬에 추가 조명이 20개 있더라도, 각 오브젝트는 자기 주변에서 가장 중요한 8개만 처리하고 나머지 12개는 무시합니다. Built-in에서는 초과 조명이 정점 라이트나 SH 라이트로 강등되어 낮은 품질로라도 반영되었지만, URP에서는 강등 없이 제외됩니다.

> 이 제한은 **URP Asset → Lighting → Additional Lights → Per Object Limit**에서 0~8 범위로 조정할 수 있습니다. 모바일에서 하나의 오브젝트에 다수의 실시간 추가 조명이 동시에 영향을 미치는 경우는 드물어, 대부분 기본값으로 충분합니다.

### 싱글패스가 가능한 이유

싱글패스가 가능하려면, 프래그먼트 셰이더가 여러 조명을 하나의 루프로 순회할 수 있어야 합니다. 조명 수는 오브젝트마다 다르고 프레임마다 바뀌므로, 이 루프는 반복 횟수가 실행 중에 결정되는 **동적 루프**여야 합니다.

Built-in 파이프라인이 설계된 시기(2005)에 주류였던 셰이더 모델 SM 2.0에서는 루프 반복 횟수가 컴파일 시점에 확정되어야 했고, 상수 레지스터 수도 적어 여러 조명 데이터를 한 패스에 담을 수 없었습니다.
그래서 Built-in은 조명 하나당 별도의 패스를 실행하는 멀티패스 방식을 택할 수밖에 없었습니다.

이 제약은 데스크톱에서는 SM 3.0(2004)부터, 모바일에서는 그래픽스 API 표준인 OpenGL ES 3.0(2012)부터 해소되었습니다. 
2015년 이후 대부분의 모바일 기기가 OpenGL ES 3.0에 대응하면서, 모든 플랫폼에서 싱글패스가 가능한 환경이 갖춰졌습니다.

URP는 OpenGL ES 3.0을 최소 요구 사양으로 설정하여 싱글패스를 구현합니다.
CPU는 프레임마다 모든 추가 조명의 데이터를 GPU 메모리에 기록합니다. 이후 드로우콜마다 선별된 조명의 인덱스와 개수를 상수 버퍼에 설정하면, 프래그먼트 셰이더가 이 인덱스로 조명 데이터를 읽어 동적 루프로 순회하고 한 번의 패스에서 처리합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 400 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px; width: 100%;">
  <!-- CPU block -->
  <rect x="30" y="10" width="340" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="32" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU (C# 렌더링 코드)</text>
  <text x="55" y="56" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">1. 씬의 활성 조명 수집</text>
  <text x="55" y="78" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">2. 오브젝트별 조명 선별 (컬링 → 중요도 정렬 → 상위 8개)</text>
  <text x="55" y="100" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">3. 조명 데이터를 배열로 정리</text>
  <text x="55" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">4. 그래픽스 API를 통해 상수 버퍼에 기록</text>
  <!-- Arrow CPU to GPU -->
  <line x1="200" y1="150" x2="200" y2="192" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="195,188 200,198 205,188" fill="currentColor"/>
  <!-- GPU block -->
  <rect x="30" y="200" width="340" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="200" y="222" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">GPU (셰이더)</text>
  <text x="55" y="248" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">1. 메인 라이트 계산</text>
  <text x="55" y="270" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">2. 추가 조명을 동적 루프로 순회 (i = 0 ~ additionalLightCount)</text>
  <text x="55" y="292" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">3. 각 조명의 기여를 누적</text>
  <text x="55" y="314" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">4. 최종 색상 출력</text>
</svg>
</div>

---

## URP의 렌더링 구조

프레임을 완성하려면 조명 외에도 여러 단계가 필요합니다. 깊이값을 기록하는 단계, 불투명 오브젝트를 그리는 단계, 투명 오브젝트를 그리는 단계, 후처리를 적용하는 단계 등이 각각 별도로 실행됩니다.
URP는 이 단계 하나하나를 **렌더 패스(Render Pass)**라는 단위로 나누어 순서대로 실행합니다.

### Renderer와 Render Pass

어떤 렌더 패스를 어떤 순서로 실행할지는 **Renderer**가 정의합니다. URP의 기본 Renderer인 **Universal Renderer**는 다음과 같은 순서로 렌더 패스를 실행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 540" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- Title -->
  <text x="210" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor" opacity="0.6">URP의 기본 렌더 패스 실행 순서</text>
  <!-- Stage 1: Depth Prepass -->
  <rect x="50" y="32" width="320" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="53" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) Depth Prepass</text>
  <text x="210" y="71" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">깊이값만 먼저 기록 (선택적)</text>
  <!-- Arrow 1 -->
  <line x1="210" y1="84" x2="210" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,96 210,106 216,96" fill="currentColor"/>
  <!-- Stage 2: Opaque Rendering -->
  <rect x="50" y="108" width="320" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="129" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) Opaque Rendering</text>
  <text x="210" y="147" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">불투명 오브젝트를 앞→뒤 정렬하여 싱글패스로 렌더링</text>
  <!-- Arrow 2 -->
  <line x1="210" y1="160" x2="210" y2="176" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,172 210,182 216,172" fill="currentColor"/>
  <!-- Stage 3: Skybox -->
  <rect x="50" y="184" width="320" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="205" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) Skybox</text>
  <text x="210" y="223" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">빈 영역을 하늘 배경으로 채움</text>
  <!-- Arrow 3 -->
  <line x1="210" y1="236" x2="210" y2="252" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,248 210,258 216,248" fill="currentColor"/>
  <!-- Stage 4: Transparent Rendering -->
  <rect x="50" y="260" width="320" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="281" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(4) Transparent Rendering</text>
  <text x="210" y="299" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">투명 오브젝트를 뒤→앞 정렬하여 알파 블렌딩</text>
  <!-- Arrow 4 -->
  <line x1="210" y1="312" x2="210" y2="328" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,324 210,334 216,324" fill="currentColor"/>
  <!-- Stage 5: Post-Processing -->
  <rect x="50" y="336" width="320" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="357" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(5) Post-Processing</text>
  <text x="210" y="375" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">블룸, 색보정, 안티앨리어싱 등 화면 전체 효과</text>
  <!-- Arrow 5 -->
  <line x1="210" y1="388" x2="210" y2="404" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,400 210,410 216,400" fill="currentColor"/>
  <!-- Stage 6: Final Blit -->
  <rect x="50" y="412" width="320" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="433" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(6) Final Blit</text>
  <text x="210" y="451" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">렌더링 결과를 화면(백버퍼)에 복사</text>
</svg>
</div>

<br>

**Depth Prepass**는 GPU가 모든 불투명 오브젝트의 깊이값만 깊이 버퍼에 먼저 기록하는 단계입니다.

Depth Prepass가 가장 먼저 실행되는 이유는 Early-Z 테스트의 효과를 극대화하기 위해서입니다. 깊이 버퍼에 최종 깊이값이 미리 채워져 있으면, 이후 Opaque Rendering 단계에서 가려진 모든 픽셀의 셰이딩을 건너뛸 수 있습니다.

다만 Depth Prepass를 활성화하면 모든 불투명 오브젝트의 정점 변환과 래스터화가 Depth Prepass와 Opaque Rendering에서 두 번 수행됩니다.
정점 변환과 래스터화는 프래그먼트 셰이딩에 비해 비용이 낮으므로, 오브젝트끼리 많이 겹치는 씬에서는 Early-Z로 절감되는 셰이딩 비용이 이 중복을 충분히 상쇄합니다. 반면 겹침이 적은 씬에서는 절감 효과가 작아 오히려 손해가 될 수 있습니다.

<br>

**Opaque Rendering**은 불투명 오브젝트를 카메라로부터 가까운 순서대로(**Front-to-Back**) 정렬하여 그리는 단계입니다.
가까운 것부터 그리면 뒤에 가려진 픽셀이 깊이 테스트에서 걸러지므로 불필요한 셰이딩이 줄어듭니다.

<br>

**Skybox**는 하늘 배경을 그리는 단계입니다. 불투명 렌더링 이후에 실행되므로, 오브젝트가 이미 그려진 픽셀은 깊이 테스트에서 걸러지고 하늘이 보이는 픽셀만 셰이딩됩니다.

<br>

**Transparent Rendering**은 투명 오브젝트를 뒤에서 앞으로(**Back-to-Front**) 정렬하여 그리는 단계입니다.
알파 블렌딩으로 혼합할 배경색이 화면에 먼저 존재해야 하므로, 먼 오브젝트부터 그립니다.

<br>

**Post-Processing**은 렌더링이 완료된 이미지에 **블룸(Bloom)**, **색보정(Color Grading)**, **안티앨리어싱(Anti-Aliasing)** 등의 화면 전체 효과를 적용하는 단계입니다. 효과마다 화면의 모든 픽셀을 처리하는 풀스크린 패스가 추가되므로, 모바일에서는 효과 수를 최소화하는 것이 일반적입니다.

<br>

**Final Blit**는 렌더링 결과를 화면의 **백버퍼(Back Buffer)**에 복사하는 마지막 단계입니다.

후처리가 비활성화되어 있으면 URP는 백버퍼에 직접 렌더링하므로, 별도의 복사 없이 프레임이 완성됩니다.

후처리가 활성화되어 있으면 백버퍼에 직접 렌더링할 수 없습니다.
GPU는 같은 렌더 타겟을 동시에 읽고 쓸 수 없는데, 후처리 효과는 렌더링된 이미지 전체를 입력으로 읽어야 하기 때문입니다. 그래서 URP는 별도의 **오프스크린 렌더 타겟(Off-screen Render Target)**에 먼저 그린 뒤, 후처리를 적용하고, 최종 결과를 백버퍼에 복사합니다.

---

## Render Graph (Unity 6+)

렌더 패스가 사용하는 GPU 리소스를 효율적으로 관리하기 위해, Unity 6부터 URP에 **Render Graph** 시스템이 도입되었습니다.

### 기존 방식의 한계

앞서 살펴본 Depth Prepass, Opaque Rendering, Post-Processing 등 각 렌더 패스는 실행 과정에서 렌더 타겟이나 임시 텍스처 등의 GPU 리소스를 사용합니다.

기존 URP(Unity 6 이전)에서는 이러한 리소스를 각 패스가 스스로 할당하고 해제했습니다. 리소스를 총괄하는 주체가 없으므로 패스 간에 어떤 리소스가 어디서 쓰이는지 파악할 수 없습니다.

앞선 패스가 이미 할당한 리소스를 재사용할 수 있는 상황에서도 패스마다 별도로 할당하므로 메모리가 낭비됩니다. 어떤 패스의 출력이 최종 프레임에 기여하지 않는다면 그 패스는 실행할 필요가 없지만, 이런 의존 관계를 파악할 수 없으므로 불필요한 패스도 항상 실행됩니다.

### Render Graph의 도입

Render Graph는 각 렌더 패스가 선언한 텍스처 입출력 정보를 바탕으로 패스 간 의존 관계를 **방향 비순환 그래프(DAG, Directed Acyclic Graph)**로 구성하고, 이를 통해 리소스 재사용과 불필요한 패스 제거를 자동으로 수행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 300" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- ===== Section 1: 기존 방식 (리스트) ===== -->
  <text x="280" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">기존 방식 (리스트)</text>

  <!-- Depth box -->
  <rect x="30" y="32" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Depth</text>
  <!-- Arrow -->
  <line x1="120" y1="48" x2="155" y2="48" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="152,43 162,48 152,53" fill="currentColor"/>
  <!-- Shadow box -->
  <rect x="163" y="32" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="208" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Shadow</text>
  <!-- Arrow -->
  <line x1="253" y1="48" x2="288" y2="48" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,43 295,48 285,53" fill="currentColor"/>
  <!-- Opaque box -->
  <rect x="296" y="32" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="341" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Opaque</text>
  <!-- Arrow -->
  <line x1="386" y1="48" x2="421" y2="48" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="418,43 428,48 418,53" fill="currentColor"/>
  <!-- Post box -->
  <rect x="429" y="32" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="474" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Post</text>

  <!-- Subtitle -->
  <text x="280" y="84" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(패스 간 텍스처 관계가 기록되지 않음)</text>

  <!-- ===== Divider ===== -->
  <line x1="30" y1="100" x2="530" y2="100" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <!-- ===== Section 2: Render Graph 방식 (그래프) ===== -->
  <text x="280" y="122" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Render Graph 방식 (그래프)</text>

  <!-- Depth box -->
  <rect x="30" y="140" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="160" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Depth</text>
  <!-- Depth → Opaque arrow (diagonal down) with DepthTexture label -->
  <line x1="120" y1="156" x2="248" y2="222" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="244,217 254,225 247,227" fill="currentColor"/>
  <text x="170" y="183" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55" transform="rotate(-24, 170, 183)">DepthTexture</text>

  <!-- Shadow box -->
  <rect x="30" y="210" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="75" y="230" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Shadow</text>
  <!-- Shadow → Opaque arrow (horizontal) with ShadowMap label -->
  <line x1="120" y1="226" x2="248" y2="226" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="245,221 255,226 245,231" fill="currentColor"/>
  <text x="184" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">ShadowMap</text>

  <!-- Opaque box -->
  <rect x="256" y="210" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="301" y="230" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Opaque</text>
  <!-- Opaque → Post arrow with ColorTexture label -->
  <line x1="346" y1="226" x2="418" y2="226" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="415,221 425,226 415,231" fill="currentColor"/>
  <text x="382" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">ColorTexture</text>

  <!-- Post box -->
  <rect x="426" y="210" width="90" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="471" y="230" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Post</text>

  <!-- Graph structure note -->
  <text x="280" y="270" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(텍스처 의존 관계가 그래프로 기록됨)</text>
</svg>
</div>

<br>

위 그래프에서 Depth와 Shadow 사이에는 화살표가 없습니다. 서로의 출력을 필요로 하지 않으므로 Render Graph는 두 패스가 독립적임을 알 수 있고, 실행 순서를 자유롭게 결정하거나 리소스를 효율적으로 재사용할 수 있습니다.

### Render Graph의 최적화

Render Graph는 프레임을 실행하기 전에 이 그래프를 분석하여 두 가지 최적화를 자동으로 수행합니다.

<br>

첫 번째 최적화는 **불필요한 패스의 자동 제거(Culling)**입니다. 어떤 패스의 출력을 이후의 어떤 패스도 읽지 않는다면, 그 패스는 실행할 필요가 없습니다.

Render Graph는 최종 출력(화면에 표시되는 결과)에서 출발하여 그래프를 역방향으로 탐색하고, 최종 출력에 기여하지 않는 패스를 자동으로 제거합니다. 예를 들어 그림자가 비활성화되어 ShadowMap을 아무 패스도 읽지 않으면, Shadow 패스가 자동으로 생략됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 460 100" xmlns="http://www.w3.org/2000/svg" style="max-width: 460px; width: 100%;">
  <!-- 역방향 탐색 방향 표시 -->
  <line x1="195" y1="9" x2="170" y2="9" stroke="currentColor" stroke-width="0.6" opacity="0.25"/>
  <polygon points="173,7 167,9 173,11" fill="currentColor" opacity="0.25"/>
  <text x="210" y="12" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.35">역방향 탐색</text>

  <!-- Depth (도달) -->
  <rect x="8" y="22" width="60" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="38" y="38" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Depth</text>

  <!-- Opaque ←DepthTex— -->
  <line x1="148" y1="34" x2="74" y2="34" stroke="currentColor" stroke-width="1"/>
  <polygon points="74,30 68,34 74,38" fill="currentColor"/>
  <text x="108" y="28" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.4">DepthTex</text>

  <!-- Opaque (도달) -->
  <rect x="148" y="22" width="66" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="181" y="38" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Opaque</text>

  <!-- Post ←ColorTex— -->
  <line x1="290" y1="34" x2="220" y2="34" stroke="currentColor" stroke-width="1"/>
  <polygon points="220,30 214,34 220,38" fill="currentColor"/>
  <text x="252" y="28" text-anchor="middle" font-family="sans-serif" font-size="7" fill="currentColor" opacity="0.4">ColorTex</text>

  <!-- Post (도달) -->
  <rect x="290" y="22" width="56" height="24" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="318" y="38" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Post</text>

  <!-- 최종 출력 ←— -->
  <line x1="380" y1="34" x2="352" y2="34" stroke="currentColor" stroke-width="1"/>
  <polygon points="352,30 346,34 352,38" fill="currentColor"/>

  <!-- 최종 출력 (역추적 시작점) -->
  <rect x="380" y="22" width="72" height="24" rx="4" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="416" y="38" text-anchor="middle" font-family="sans-serif" font-size="9" font-weight="bold" fill="currentColor">최종 출력</text>

  <!-- Shadow (미도달) -->
  <line x1="181" y1="46" x2="181" y2="58" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2 2" opacity="0.3"/>
  <rect x="148" y="62" width="66" height="24" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3 2" opacity="0.4"/>
  <text x="181" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">Shadow</text>
  <line x1="154" y1="66" x2="208" y2="82" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <line x1="208" y1="66" x2="154" y2="82" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>

  <text x="222" y="78" font-family="sans-serif" font-size="8" fill="currentColor" opacity="0.5">미도달 → 자동 제거</text>
</svg>
</div>

<br>

두 번째 최적화는 **리소스 수명 관리와 메모리 재사용(Aliasing)**입니다. 각 텍스처의 수명(처음 쓰여지는 시점부터 마지막으로 읽히는 시점까지)을 그래프에서 파악할 수 있으므로, 수명이 끝난 텍스처의 메모리를 이후 텍스처가 그대로 재사용합니다.

수명이 겹치지 않는 텍스처끼리 같은 물리 메모리를 공유하므로, 전체 메모리 사용량이 줄어듭니다. 메모리가 제한된 모바일 환경에서 이 최적화의 효과가 특히 큽니다.

---

## Built-in vs URP 비교 요약

지금까지 살펴본 URP와 Built-in 파이프라인의 차이를 정리해보면 다음과 같습니다.

<br>

| 항목 | Built-in 파이프라인 | URP |
|---|---|---|
| 조명 처리 | 멀티패스 포워드 (조명마다 별도 패스) | 싱글패스 포워드 (모든 조명을 한 패스에서) |
| 드로우콜 | 오브젝트 × 조명 수에 비례 | 오브젝트 수에 비례 (조명 수와 무관) |
| 셰이더 작성 | Surface Shader (.shader / Cg) | Shader Graph 또는 HLSL 직접 작성 |
| 배칭 | Static/Dynamic Batching (제한적) | SRP Batcher (주) + Static/Dynamic Batching |
| 확장성 | 제한적 (엔진 내부 고정) | ScriptableRendererFeature로 커스텀 패스 추가 |
| 리소스 관리 (Unity 6+) | 패스별 개별 할당 | Render Graph (자동 최적화) |
| 모바일 적합성 | 낮음 (멀티패스 비용) | 높음 (싱글패스, SRP Batcher, 경량 설계) |
| 유지 보수 | 레거시 (신규 기능 추가 없음) | 활발히 업데이트 중 (Unity의 주력 파이프라인) |

### 셰이더

Built-in 파이프라인에서는 **Surface Shader**라는 Unity 고유의 셰이더 작성 방식을 사용합니다.
개발자가 표면의 속성(색상, 반사율, 노멀 등)만 정의하면, 엔진이 이를 바탕으로 멀티패스 조명 처리에 필요한 버텍스/프래그먼트 셰이더 코드를 자동 생성합니다. 조명 모델을 직접 구현하지 않아도 되지만, 엔진이 생성한 최종 셰이더의 동작을 세밀하게 제어하기 어렵습니다.

URP에서는 **Shader Graph**(노드 기반 비주얼 셰이더 에디터)를 사용하거나, HLSL을 직접 작성합니다. Surface Shader는 URP에서 지원되지 않으므로, Built-in에서 URP로 전환할 때 셰이더를 다시 작성해야 합니다.

### 배칭

Built-in 파이프라인의 **Static Batching**과 **Dynamic Batching**은 같은 머티리얼을 공유하는 오브젝트의 메쉬를 합쳐 드로우콜을 줄이는 기법입니다. 하지만 Static Batching은 오브젝트가 움직이지 않아야 하고 메모리 사용량이 늘어나며, Dynamic Batching은 버텍스 수가 적은 메쉬에만 적용됩니다. 또한 멀티패스 구조에서는 배칭으로 패스당 드로우콜을 줄이더라도, 조명마다 패스 자체가 반복되므로 드로우콜 총량의 근본적인 해결은 되지 않습니다.

URP에서도 Static Batching과 Dynamic Batching을 사용할 수 있지만, 주된 배칭 방식으로 **SRP Batcher**가 도입되었습니다. SRP Batcher는 드로우콜 자체를 줄이는 대신, 같은 **셰이더 배리언트(Shader Variant)**를 사용하는 드로우콜 사이에서 셰이더 패스 전환(**SetPass Call**)을 줄이는 방식으로 동작합니다. 각 배칭 기법의 상세한 동작 원리는 [Part 2](/dev/unity/UnityPipeline-2/)에서 다룹니다.

### 확장성

Built-in 파이프라인은 렌더링 과정이 엔진 내부에 고정되어 있어 커스텀 렌더 패스를 추가하기 어렵습니다.
**CommandBuffer**를 통해 특정 시점에 추가 명령을 삽입하는 것은 가능하지만, 전체 렌더링 흐름 자체를 제어할 수는 없습니다.

URP에서는 **ScriptableRendererFeature**를 통해 커스텀 렌더 패스를 파이프라인의 원하는 시점에 삽입할 수 있습니다.
예를 들어, 아웃라인 효과를 위한 별도의 렌더 패스를 Opaque Rendering 이후에 추가하거나, 특정 레이어의 오브젝트만 별도로 렌더링하는 패스를 삽입하는 것이 가능합니다.

---

## 렌더 파이프라인 선택

지금까지 살펴본 URP의 구조적 이점을 정리하면 다음과 같습니다.

<br>

| URP 기능 | 이점 | 절감 자원 |
|---|---|---|
| 싱글패스 포워드 | 드로우콜 감소 | CPU |
| SRP Batcher | SetPass Call 감소 | CPU |
| Render Graph | 불필요한 패스 제거, 메모리 재사용 | GPU 메모리, 대역폭 |

<br>

Built-in 파이프라인은 더 이상 신규 기능이 추가되지 않으며, Unity 공식 문서에서도 신규 프로젝트에는 URP 또는 HDRP를 권장합니다. 기존 Built-in 프로젝트를 URP로 전환하면 셰이더 변환과 에셋 수정 등의 작업이 수반되지만, 싱글패스 렌더링, SRP Batcher, Render Graph 등 성능 최적화에 구조적으로 유리한 기반을 확보할 수 있습니다.

---

## GPU 아키텍처에서 렌더 파이프라인까지

GPU 아키텍처와 렌더 파이프라인이 이어지는 전체 흐름은 다음과 같습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- Title -->
  <text x="210" y="18" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor" opacity="0.6">전체 렌더링 흐름</text>
  <!-- Layer 1: Scene -->
  <rect x="60" y="30" width="300" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="55" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 (오브젝트, 머티리얼, 조명, 카메라)</text>
  <!-- Arrow 1 -->
  <line x1="210" y1="70" x2="210" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,86 210,96 216,86" fill="currentColor"/>
  <!-- Layer 2: Render Pipeline (CPU) -->
  <rect x="20" y="98" width="380" height="140" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="118" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더 파이프라인 (CPU)</text>
  <!-- Pipeline steps inside -->
  <text x="210" y="140" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">컬링 → 정렬 → 라이팅 패스 결정 → 드로우콜 생성</text>
  <!-- Built-in vs URP comparison -->
  <rect x="40" y="154" width="160" height="38" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="120" y="171" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Built-in</text>
  <text x="120" y="185" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">멀티패스 → 드로우콜 多</text>
  <rect x="220" y="154" width="160" height="38" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="300" y="171" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">URP</text>
  <text x="300" y="185" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">싱글패스 → 드로우콜 少</text>
  <!-- 드로우콜 제출 label -->
  <text x="210" y="228" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">드로우콜 제출</text>
  <!-- Arrow 2 -->
  <line x1="210" y1="238" x2="210" y2="262" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="204,258 210,268 216,258" fill="currentColor"/>
  <!-- Layer 3: GPU Hardware -->
  <rect x="20" y="270" width="380" height="136" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="210" y="290" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU 하드웨어</text>
  <!-- Desktop path -->
  <rect x="40" y="304" width="340" height="32" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="58" y="324" text-anchor="start" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">데스크톱</text>
  <text x="370" y="324" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">정점 처리 → 래스터화 → 프래그먼트 처리 → 프레임 버퍼</text>
  <!-- Mobile path -->
  <rect x="40" y="346" width="340" height="46" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="58" y="366" text-anchor="start" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">모바일</text>
  <text x="370" y="366" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">정점 처리 + 타일링 → 타일 메모리</text>
  <text x="370" y="382" text-anchor="end" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">→ 타일별 프래그먼트 → 프레임 버퍼</text>
</svg>
</div>

<br>

렌더 파이프라인이 CPU에서 드로우콜을 구성하고, GPU가 이를 실행하여 최종 화면을 만듭니다.

---

## 마무리

- 렌더 파이프라인은 씬의 오브젝트를 GPU가 실행할 드로우콜로 변환하는 CPU 측 제어 계층입니다.
- Built-in의 멀티패스 포워드에서는 조명 하나당 별도 패스를 실행하며, 드로우콜이 `오브젝트 수 × 조명 수`에 비례합니다.
- SRP는 렌더링 과정을 C#으로 제어하는 프레임워크이며, URP와 HDRP가 그 위에 구축되어 있습니다.
- URP의 싱글패스 포워드에서는 모든 조명을 한 패스에서 처리하여, 드로우콜이 오브젝트 수에만 비례합니다.
- Render Graph(Unity 6+)는 렌더 패스 간 리소스 의존성을 그래프로 관리하여 불필요한 패스 제거와 메모리 재사용을 자동으로 수행합니다.

싱글패스 설계는 URP의 핵심이며, SRP Batcher와 Render Graph가 이를 보완합니다.

[Part 2](/dev/unity/UnityPipeline-2/)에서는 드로우콜의 내부 동작과 배칭 기법의 원리를 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)

**시리즈**
- **Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조** (현재 글)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)
- [Unity 렌더 파이프라인 (3) - 컬링과 오클루전](/dev/unity/UnityPipeline-3/)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- **Unity 렌더 파이프라인 (1) - Built-in과 URP의 구조** (현재 글)
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
