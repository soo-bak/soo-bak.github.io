---
layout: single
title: "Unity 렌더링 (2) - Render Target과 Frame Buffer - soo:bak"
date: "2026-03-06 21:06:00 +0900"
description: Back Buffer, RenderTexture, Temporary RT, Render Target 전환 비용, Dynamic Resolution, 컬러 포맷을 설명합니다.
tags:
  - Unity
  - 렌더링
  - RenderTexture
  - FrameBuffer
  - 모바일
---

## 렌더링 결과의 저장 위치, Render Target

[Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)에서 카메라가 무엇을 어떤 순서로 그리는지를 다루었습니다. 카메라가 씬의 오브젝트를 정렬하고 드로우콜을 제출하면, GPU는 버텍스 셰이더로 정점을 변환하고, 래스터화를 거쳐 프래그먼트를 생성한 뒤, 프래그먼트 셰이더로 각 픽셀의 최종 색상을 계산합니다.
이 계산 결과가 기록되는 메모리 영역이 **Render Target**입니다.

<br>

화면에 직접 표시되는 Back Buffer도, 화면 대신 텍스처에 렌더링하는 RenderTexture도 모두 Render Target에 해당합니다. 이 글에서는 Back Buffer, RenderTexture, Temporary RT의 구조와 비용, Render Target 전환이 모바일 GPU에 미치는 영향, 해상도와 컬러 포맷에 따른 메모리 사용량을 살펴봅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 310" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Render Target의 종류</text>

  <!-- (1) Back Buffer -->
  <rect x="30" y="42" width="460" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="64" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(1) Back Buffer</text>
  <text x="70" y="84" font-family="sans-serif" font-size="11" fill="currentColor">최종 디스플레이에 표시되는 버퍼</text>
  <text x="70" y="102" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 카메라의 기본 Render Target</text>

  <!-- (2) RenderTexture -->
  <rect x="30" y="122" width="460" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="144" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(2) RenderTexture</text>
  <text x="70" y="164" font-family="sans-serif" font-size="11" fill="currentColor">텍스처 형태의 Render Target</text>
  <text x="70" y="182" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 미니맵, 거울, 후처리 등에 사용</text>

  <!-- (3) Temporary Render Texture -->
  <rect x="30" y="202" width="460" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="224" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">(3) Temporary Render Texture</text>
  <text x="70" y="244" font-family="sans-serif" font-size="11" fill="currentColor">풀에서 임시로 꺼내 쓰는 RenderTexture</text>
  <text x="70" y="262" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 후처리 체인, CommandBuffer에서 사용</text>

  <!-- Bracket connecting all three -->
  <line x1="15" y1="52" x2="15" y2="262" stroke="currentColor" stroke-width="1.5" opacity="0.3"/>
  <line x1="15" y1="52" x2="25" y2="52" stroke="currentColor" stroke-width="1.5" opacity="0.3"/>
  <line x1="15" y1="262" x2="25" y2="262" stroke="currentColor" stroke-width="1.5" opacity="0.3"/>
  <text x="12" y="162" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5" transform="rotate(-90, 12, 162)">Render Target</text>
</svg>
</div>

---

## Back Buffer

**Back Buffer**는 GPU가 다음 프레임을 렌더링하는 메모리 영역입니다.
렌더링이 완료되면 이 버퍼가 Front Buffer로 전환되어 디스플레이 컨트롤러를 통해 화면에 표시됩니다. Unity에서 카메라의 Target Texture 필드가 비어있으면(None), 렌더링 결과는 자동으로 Back Buffer에 기록됩니다.

### Double Buffering

버퍼가 하나뿐이면(Single Buffering), 디스플레이가 현재 화면을 표시하는 동안 GPU가 같은 버퍼에 다음 프레임을 쓰게 됩니다.
디스플레이가 화면을 위에서 아래로 한 줄씩 읽어가는 도중에 버퍼 내용이 바뀌면, 화면 위쪽 절반은 이전 프레임이고 아래쪽 절반은 새 프레임인 상태가 되어 화면이 찢어지는 현상(**Tearing**)이 발생합니다.

**Double Buffering**은 이 문제를 방지하기 위해 버퍼를 두 개로 분리하는 구조입니다.
하나는 디스플레이가 현재 읽고 있는 **Front Buffer**, 다른 하나는 GPU가 다음 프레임을 렌더링하는 **Back Buffer**입니다.
GPU는 Back Buffer에만 쓰고, 디스플레이는 Front Buffer에서만 읽으므로 렌더링과 표시가 서로 간섭하지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Double Buffering</text>

  <!-- Front Buffer box -->
  <rect x="40" y="42" width="280" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Front Buffer</text>
  <text x="50" y="80" font-family="sans-serif" font-size="11" fill="currentColor">프레임 N의 완성된 이미지</text>

  <!-- Display read arrow -->
  <line x1="320" y1="72" x2="370" y2="72" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="365,66 377,72 365,78" fill="currentColor"/>
  <text x="385" y="68" font-family="sans-serif" font-size="11" fill="currentColor">디스플레이</text>
  <text x="385" y="82" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">읽기</text>

  <!-- Back Buffer box -->
  <rect x="40" y="122" width="280" height="60" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="142" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Back Buffer</text>
  <text x="50" y="160" font-family="sans-serif" font-size="11" fill="currentColor">프레임 N+1을 렌더링 중</text>

  <!-- GPU write arrow -->
  <line x1="370" y1="152" x2="320" y2="152" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="325,146 313,152 325,158" fill="currentColor"/>
  <text x="385" y="148" font-family="sans-serif" font-size="11" fill="currentColor">GPU</text>
  <text x="385" y="162" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">쓰기</text>

  <!-- Swap arrows on the left side -->
  <line x1="22" y1="98" x2="22" y2="126" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <polygon points="16,102 22,93 28,102" fill="currentColor"/>
  <polygon points="16,122 22,131 28,122" fill="currentColor"/>
  <text x="18" y="116" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5" transform="rotate(-90, 18, 116)">Swap</text>

  <!-- Swap explanation section -->
  <rect x="40" y="210" width="440" height="140" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="260" y="234" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">프레임 N+1 렌더링 완료 시: Swap</text>

  <!-- Swap visual -->
  <rect x="70" y="254" width="140" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="276" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Back Buffer</text>

  <rect x="310" y="254" width="140" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="380" y="276" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Front Buffer</text>

  <!-- Bidirectional swap arrows -->
  <line x1="210" y1="264" x2="305" y2="264" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="300,258 312,264 300,270" fill="currentColor"/>
  <line x1="310" y1="280" x2="215" y2="280" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="220,274 208,280 220,286" fill="currentColor"/>

  <!-- Explanation labels -->
  <text x="260" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 이전 Back Buffer가 새 Front Buffer가 됨</text>
  <text x="260" y="328" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 이전 Front Buffer가 새 Back Buffer가 됨</text>
  <text x="260" y="344" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">(포인터만 교체 — 메모리 복사 없음)</text>
</svg>
</div>

<br>

한 프레임의 렌더링이 완료되면 Front Buffer와 Back Buffer의 역할이 교체(Swap)됩니다. 이 교체는 메모리의 내용을 복사하는 것이 아니라 각 버퍼를 가리키는 포인터만 바꾸는 동작이므로, 교체 자체의 비용은 거의 없습니다.

교체 시점도 중요합니다. [래스터화 파이프라인 (3)](/dev/unity/RasterPipeline-3/)에서 다룬 **VSync(수직 동기화)**는 이 교체를 디스플레이의 수직 귀선 기간(Vertical Blanking Interval, VBI)에 맞추는 기법입니다.
VBI란 디스플레이가 화면의 마지막 줄을 그린 뒤 다시 첫 줄로 돌아가는 짧은 유휴 구간입니다. 이 구간에서 버퍼를 교체하면 화면 갱신 도중에 내용이 바뀌는 일이 없습니다. VSync가 켜져 있으면 GPU가 프레임을 완성해도 다음 VSync 신호가 올 때까지 교체를 지연하므로, Tearing은 방지됩니다.

다만 VSync가 켜진 Double Buffering에서는 버퍼 교체가 VBI에서만 가능하므로, GPU가 한 VSync 간격(VBI와 다음 VBI 사이) 안에 프레임을 완성하지 못하면 다음 VBI까지 기다려야 합니다.
60Hz 디스플레이에서 VSync 간격은 16.67ms이므로, 하나를 놓치면 한 프레임이 두 VSync 간격(33.33ms)을 차지하게 되어 프레임 레이트가 60fps에서 30fps로 절반이 됩니다.

<br>

이 문제를 완화하기 위해 버퍼를 세 개로 늘리는 **Triple Buffering**도 존재합니다. Triple Buffering에서는 GPU가 VSync를 기다리는 동안에도 세 번째 버퍼에 다음 프레임을 미리 렌더링할 수 있어, 프레임 레이트가 절반으로 떨어지는 현상을 방지합니다. 대신 한 프레임분의 입력 지연(Input Latency)이 추가되며, 버퍼 하나만큼의 GPU 메모리가 더 필요합니다.

모바일 환경에서는 대부분 VSync가 기본 활성화되어 있습니다. 따라서 화면 주사율(60Hz 또는 120Hz)에 맞춰 프레임을 완성해야 하며, 60Hz 디스플레이 기준 프레임 예산은 약 16.67ms(1000ms / 60 ≈ 16.67ms)입니다.

---

## RenderTexture

**RenderTexture**는 렌더링 결과를 텍스처 형태로 저장하는 Render Target입니다.
일반 텍스처(Texture2D)가 디스크에서 읽어온 이미지라면, RenderTexture는 GPU가 실시간으로 렌더링한 결과를 담습니다.
Camera 컴포넌트의 **Target Texture** 필드에 RenderTexture를 할당하면, 해당 카메라의 렌더링 결과가 Back Buffer 대신 이 텍스처에 기록됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">RenderTexture 사용 구조</text>

  <!-- === Row 1: 일반 카메라 === -->
  <text x="30" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">일반 카메라:</text>

  <rect x="30" y="65" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">카메라</text>

  <line x1="110" y1="81" x2="145" y2="81" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="140,75 152,81 140,87" fill="currentColor"/>

  <rect x="155" y="65" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="195" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>

  <line x1="235" y1="81" x2="270" y2="81" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="265,75 277,81 265,87" fill="currentColor"/>

  <rect x="280" y="65" width="100" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="330" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Back Buffer</text>

  <line x1="380" y1="81" x2="410" y2="81" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="405,75 417,81 405,87" fill="currentColor"/>

  <rect x="420" y="65" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="460" y="85" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">디스플레이</text>

  <!-- === Row 2: RenderTexture 카메라 === -->
  <text x="30" y="135" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">RenderTexture 카메라:</text>

  <rect x="30" y="145" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="70" y="165" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">카메라</text>

  <line x1="110" y1="161" x2="145" y2="161" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="140,155 152,161 140,167" fill="currentColor"/>

  <rect x="155" y="145" width="80" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="195" y="165" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">렌더링</text>

  <line x1="235" y1="161" x2="270" y2="161" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="265,155 277,161 265,167" fill="currentColor"/>

  <rect x="280" y="145" width="120" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="340" y="165" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">RenderTexture</text>

  <!-- Arrow down from RenderTexture to branch label -->
  <line x1="340" y1="177" x2="340" y2="210" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="334,205 340,217 346,205" fill="currentColor"/>

  <!-- Branch label -->
  <text x="340" y="235" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">텍스처로 활용</text>

  <!-- Horizontal branch line -->
  <line x1="80" y1="252" x2="440" y2="252" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="340" y1="242" x2="340" y2="252" stroke="currentColor" stroke-width="1" opacity="0.4"/>

  <!-- Branch 1: 미니맵 UI -->
  <line x1="110" y1="252" x2="110" y2="268" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="104,263 110,275 116,263" fill="currentColor"/>
  <rect x="50" y="278" width="120" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="110" y="296" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">미니맵 UI</text>
  <text x="110" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">에 표시</text>

  <!-- Branch 2: 거울 메쉬 -->
  <line x1="260" y1="252" x2="260" y2="268" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,263 260,275 266,263" fill="currentColor"/>
  <rect x="200" y="278" width="120" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="296" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">거울 메쉬</text>
  <text x="260" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">에 매핑</text>

  <!-- Branch 3: 후처리 입력 -->
  <line x1="410" y1="252" x2="410" y2="268" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="404,263 410,275 416,263" fill="currentColor"/>
  <rect x="350" y="278" width="120" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="410" y="296" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">후처리 입력</text>
  <text x="410" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">으로 사용</text>
</svg>
</div>

### 사용 예시

**미니맵**에서는 씬을 위에서 내려다보는 카메라를 별도로 배치하고, 그 결과를 RenderTexture에 담아 UI의 RawImage로 표시합니다. [Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 다룬 Culling Mask를 미니맵 전용 레이어로 제한하면, 전체 씬의 오브젝트를 처리하지 않아 비용을 줄일 수 있습니다.

**거울과 포탈**에서는 거울 표면에 반사된 시점의 카메라를 배치하고, RenderTexture에 렌더링한 결과를 거울 메쉬의 텍스처로 매핑합니다. 포탈도 같은 원리로, 포탈 너머의 시점에 카메라를 두고 RenderTexture에 렌더링합니다.

**후처리**에서는 카메라의 렌더링 결과를 RenderTexture에 기록한 뒤, 그 텍스처를 입력으로 Bloom, Color Grading 등의 셰이더를 실행합니다. 후처리의 각 단계가 RenderTexture를 입력으로 받고 또 다른 RenderTexture에 결과를 출력하는 체인 구조를 이룹니다.

### RenderTexture의 메모리 비용

RenderTexture는 GPU 메모리를 점유합니다. 그 크기는 **해상도 × 픽셀당 바이트 수**로 결정됩니다.
1920×1080 해상도 기준으로, RGBA32(4바이트/픽셀)는 약 7.9MB, R16G16B16A16 HDR(8바이트/픽셀)는 약 15.8MB를 점유합니다.
Unity의 DefaultHDR 포맷은 플랫폼에 따라 R11G11B10(4바이트/픽셀)이 선택되기도 하므로, 같은 HDR이라도 실제 메모리는 절반으로 줄어들 수 있습니다.

예를 들어, 미니맵에 1920x1080 해상도의 RenderTexture를 사용하면 미니맵 UI 크기에 비해 불필요하게 높은 해상도를 소비합니다. 미니맵 UI가 256x256 픽셀 크기라면, RenderTexture도 256x256이면 충분합니다. 불필요하게 큰 RenderTexture는 GPU 메모리를 낭비할 뿐 아니라, 래스터화와 프래그먼트 셰이더가 처리해야 할 픽셀 수와 읽기/쓰기 대역폭도 함께 증가시킵니다.

<br>

이처럼 RenderTexture는 해상도와 포맷에 따라 수 MB 이상의 GPU 메모리를 점유하므로, **사용이 끝나면 반드시 해제해야 합니다.**
`RenderTexture.Release()`를 호출하면 GPU 하드웨어 리소스가 해제됩니다. RenderTexture의 C# 래퍼 객체가 가비지 컬렉터(GC)에 의해 수거될 때 finalizer를 통해 GPU 리소스가 해제되는 경로도 존재하지만, GC의 수거 타이밍은 불확정적입니다.
Release를 명시적으로 호출하지 않으면 GPU 메모리가 필요 이상 오래 점유될 수 있습니다.
씬 전환 시에도 참조가 남아있으면 해제되지 않으므로, 씬 전환 이벤트에서 명시적으로 Release를 호출해야 합니다.

<br>

RenderTexture를 직접 생성하고 해제하는 방식은 미니맵이나 거울처럼 수명이 긴 용도에 적합합니다. 반면, 후처리 체인처럼 매 프레임 잠깐 쓰고 버리는 용도에는 할당/해제가 반복되어 비효율적입니다.

---

## Temporary Render Texture

앞서 살펴본 것처럼, 후처리 체인에서 매 프레임 `new`/`Release`를 반복하면 GPU 메모리 할당/해제 비용이 누적됩니다.
**RenderTexture.GetTemporary**와 **RenderTexture.ReleaseTemporary**는 이 문제를 해결하는 Unity의 임시 RenderTexture 풀(Pool) 시스템입니다. 한 번 할당한 RT를 풀에 보관했다가 재사용하는 방식으로 반복 할당 비용을 제거합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 440" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">일반 RenderTexture vs Temporary RT</text>

  <!-- === Left column: 일반 RenderTexture === -->
  <text x="130" y="52" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">일반 RenderTexture</text>

  <!-- Frame 1 -->
  <text x="130" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프레임 1</text>
  <rect x="40" y="88" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="107" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">new → 할당</text>
  <rect x="40" y="122" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="130" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">사용</text>
  <rect x="40" y="156" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="175" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Release → 해제</text>

  <!-- Frame 2 -->
  <text x="130" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프레임 2</text>
  <rect x="40" y="214" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="233" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">new → 할당 (다시)</text>
  <rect x="40" y="248" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="130" y="267" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">사용</text>
  <rect x="40" y="282" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="130" y="301" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Release → 해제 (다시)</text>

  <!-- Left result -->
  <rect x="40" y="330" width="180" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="351" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">매 프레임 할당/해제 반복</text>

  <!-- Divider -->
  <line x1="260" y1="65" x2="260" y2="370" stroke="currentColor" stroke-width="1" opacity="0.2"/>

  <!-- === Right column: Temporary RT === -->
  <text x="390" y="52" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Temporary RT</text>

  <!-- Frame 1 -->
  <text x="390" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프레임 1</text>
  <rect x="300" y="88" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="107" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">GetTemporary → 할당</text>
  <rect x="300" y="122" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="390" y="141" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">사용</text>
  <rect x="300" y="156" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="175" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">ReleaseTemporary → 풀에 반환</text>

  <!-- Frame 2 -->
  <text x="390" y="204" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">프레임 2</text>
  <rect x="300" y="214" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="390" y="233" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">GetTemporary → 풀에서 재사용</text>
  <rect x="300" y="248" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="390" y="267" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">사용</text>
  <rect x="300" y="282" width="180" height="28" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text x="390" y="301" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">ReleaseTemporary → 풀에 반환</text>

  <!-- Right result -->
  <rect x="300" y="330" width="180" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="390" y="351" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">할당 1회, 이후 재사용</text>

  <!-- Bottom comparison note -->
  <text x="260" y="400" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">* 왼쪽: 프레임마다 GPU 메모리 할당/해제 비용 발생</text>
  <text x="260" y="418" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">* 오른쪽: 첫 프레임만 할당, 이후 풀에서 꺼내 재사용</text>
</svg>
</div>

### 후처리 체인에서의 활용

후처리 효과는 여러 단계의 셰이더 패스를 연속으로 실행합니다. 각 패스는 입력 텍스처를 읽어 셰이더를 실행하고, 결과를 다른 텍스처에 씁니다. 이 중간 텍스처들이 모두 Temporary RT로 관리됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 540" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Bloom 후처리의 Temporary RT 사용</text>

  <!-- Source RT -->
  <rect x="185" y="42" width="150" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="63" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Source RT</text>
  <text x="260" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">카메라 렌더링 결과</text>

  <!-- Arrow to Pass 1 -->
  <line x1="260" y1="96" x2="260" y2="114" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,109 260,120 266,109" fill="currentColor"/>

  <!-- Pass 1: 밝기 추출 -->
  <rect x="130" y="122" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="145" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(1) 밝기 추출 패스</text>

  <!-- Arrow to Temp RT A -->
  <line x1="260" y1="158" x2="260" y2="176" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,171 260,182 266,171" fill="currentColor"/>

  <!-- Temp RT A -->
  <rect x="185" y="184" width="150" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="205" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Temp RT A</text>

  <!-- Arrow to Pass 2a -->
  <line x1="260" y1="216" x2="260" y2="234" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,229 260,240 266,229" fill="currentColor"/>

  <!-- Pass 2a: 다운샘플 + 블러 -->
  <rect x="130" y="242" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="265" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(2a) 다운샘플 + 블러</text>

  <!-- Release A annotation -->
  <text x="420" y="265" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Release(A) → 풀 반환</text>

  <!-- Arrow to Temp RT B -->
  <line x1="260" y1="278" x2="260" y2="296" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,291 260,302 266,291" fill="currentColor"/>

  <!-- Temp RT B (절반 해상도) -->
  <rect x="195" y="304" width="130" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="325" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Temp RT B</text>
  <text x="260" y="350" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">절반 해상도</text>

  <!-- Arrow to Pass 2b -->
  <line x1="260" y1="354" x2="260" y2="368" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,363 260,374 266,363" fill="currentColor"/>

  <!-- Pass 2b: 다운샘플 + 블러 -->
  <rect x="130" y="376" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="399" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(2b) 다운샘플 + 블러</text>

  <!-- Release B annotation -->
  <text x="420" y="399" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">Release(B) → 풀 반환</text>

  <!-- Arrow to Temp RT C -->
  <line x1="260" y1="412" x2="260" y2="430" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,425 260,436 266,425" fill="currentColor"/>

  <!-- Temp RT C (또 절반 해상도) -->
  <rect x="205" y="438" width="110" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="459" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Temp RT C</text>

  <!-- Temp RT boxes shrink to show resolution reduction -->
  <text x="260" y="486" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">또 절반 해상도</text>

  <!-- Arrow to Pass 3 -->
  <line x1="260" y1="490" x2="260" y2="504" stroke="currentColor" stroke-width="1.5"/>

  <!-- Note: boxes get narrower to visually represent resolution reduction -->
  <text x="260" y="524" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">→ (3) 업샘플 + 합성 → 최종 결과 (Release C)</text>
</svg>
</div>

<br>

각 단계에서 더 이상 필요 없는 Temporary RT는 즉시 ReleaseTemporary로 풀에 반환합니다.
풀에 반환된 RT는 이후 다른 패스가 같은 규격의 RT를 요청할 때 재사용됩니다. "같은 규격"이란 해상도(가로 x 세로 픽셀 수), 컬러 포맷(예: R11G11B10_UFloat), 깊이 버퍼 비트 수, 안티앨리어싱 레벨이 모두 일치하는 경우를 뜻합니다. 이 조건 중 하나라도 다르면 풀에서 꺼낼 수 없으므로 새로운 할당이 발생합니다.

<br>

앞의 Bloom 예시에서 Temp RT A는 (2a) 패스가 끝나면 즉시 풀에 반환됩니다. 따라서 (2b) 패스가 실행될 때 A는 이미 풀에 돌아간 상태이므로, 한 시점에 GPU 메모리를 실제로 점유하는 RT 수가 최소한으로 유지됩니다.

풀에 반환된 RT는 다음 프레임에서 같은 규격의 요청이 오면 즉시 재사용됩니다. 반대로 수 프레임 동안 재사용 요청이 없으면, Unity가 자동으로 해당 RT의 GPU 메모리를 해제합니다.
예를 들어, 특정 후처리 효과를 비활성화하면 해당 효과의 Temporary RT 요청이 멈추고, 풀에 남아있던 RT는 시간이 지나면 자동으로 회수됩니다.

### CommandBuffer에서의 사용

**CommandBuffer**는 렌더링 명령을 수동으로 구성하는 API입니다. 스크립트에서 드로우콜, Render Target 전환, 셰이더 파라미터 설정 등의 명령을 CommandBuffer에 기록해 두면, Unity가 이를 GPU에 한 번에 제출하여 실행합니다.

CommandBuffer에서도 `cmd.GetTemporaryRT()`로 임시 RT를 할당하고, `cmd.ReleaseTemporaryRT()`로 풀에 반환하여 재사용할 수 있습니다. 명시적으로 반환하지 않은 임시 RT가 있더라도, 해당 CommandBuffer의 실행이 끝나면 Unity가 자동으로 해제하므로 메모리 누수는 발생하지 않습니다.

Unity 6 이상의 Render Graph 기반 URP에서는 이 수동 관리가 불필요해집니다. 개발자가 각 렌더 패스에서 어떤 RT를 읽고 쓰는지만 선언하면, Render Graph가 전체 프레임의 패스 구조를 보고 RT의 할당, 재사용, 해제를 자동으로 결정합니다.
이때 `cmd.GetTemporaryRT()` 대신 **RTHandle**이라는 RT 래퍼를 사용합니다.

<br>

Back Buffer, RenderTexture, Temporary RT는 용도와 수명이 다르지만, GPU 메모리에 렌더링 결과를 기록한다는 점은 동일합니다. 이 Render Target들 사이를 전환할 때 발생하는 비용은 플랫폼에 따라 크게 다르며, 모바일에서는 성능에 직접적인 영향을 미칩니다.

---

## Render Target 전환 비용

한 프레임 안에서 GPU는 여러 Render Target에 번갈아 렌더링합니다.
후처리 체인에서 Temp RT A에 쓰다가 Temp RT B로 넘어가거나, 그림자 맵을 렌더링한 뒤 메인 컬러 RT로 돌아오는 과정이 전형적입니다. 이처럼 GPU가 현재 쓰고 있는 Render Target을 다른 것으로 변경하는 동작을 **Render Target 전환(Switch)**이라 합니다.

<br>

데스크톱 GPU에서 Render Target 전환은 상대적으로 가벼운 연산입니다. 전용 비디오 메모리(VRAM)에 프레임버퍼 전체가 상주하므로, 전환 시에는 GPU 내부 렌더 캐시를 플러시(Flush, 캐시에 쌓인 쓰기 결과를 VRAM에 반영)하고 쓰기 대상 주소를 변경하면 됩니다. 이 과정에서 일부 지연이 발생하지만, 프레임버퍼 전체를 복사하는 동작은 아니므로 비용이 제한적입니다.

모바일 GPU에서는 아키텍처가 근본적으로 다르기 때문에 전환 비용이 훨씬 큽니다.

### 모바일 GPU의 Resolve 비용

[GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 다룬 것처럼, 모바일 GPU는 **TBDR(Tile-Based Deferred Rendering)** 구조로 동작합니다. 화면을 작은 타일(일반적으로 16x16 또는 32x32 픽셀)로 나누고, 각 타일의 렌더링을 GPU 칩 내부의 고속 **타일 메모리(On-Chip Tile Memory)**에서 수행하는 방식입니다. 타일 하나의 렌더링이 완료되면, 그 결과를 외부 시스템 메모리로 복사하는데, 이 복사 과정을 **Resolve**라 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">TBDR에서 Render Target 전환 시 Resolve</text>

  <!-- Phase label: RT A rendering -->
  <text x="260" y="50" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Render Target A에 렌더링 중</text>

  <!-- Box 1: GPU 타일 메모리 (On-Chip) -->
  <rect x="130" y="64" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="84" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 타일 메모리</text>
  <text x="230" y="102" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">타일의 컬러 + 깊이</text>
  <!-- Annotation: fast on-chip -->
  <text x="345" y="93" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">빠른 On-Chip 접근</text>

  <!-- Event label: RT switch -->
  <line x1="230" y1="116" x2="230" y2="148" stroke="currentColor" stroke-width="1.5"/>
  <text x="244" y="138" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Render Target 전환 (A → B)</text>

  <!-- Arrow 1: Resolve -->
  <line x1="230" y1="148" x2="230" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="223,194 230,206 237,194" fill="currentColor"/>
  <rect x="244" y="160" width="232" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="none"/>
  <text x="260" y="176" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Resolve (타일 메모리 → 시스템 메모리)</text>

  <!-- Box 2: 시스템 메모리 (RT A) -->
  <rect x="130" y="214" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="236" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">시스템 메모리</text>
  <text x="230" y="254" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(Render Target A)</text>
  <!-- Annotation: slow bandwidth -->
  <text x="345" y="243" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">느린 대역폭 소비</text>

  <!-- Arrow 2: Load -->
  <line x1="230" y1="266" x2="230" y2="350" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="223,344 230,356 237,344" fill="currentColor"/>
  <rect x="244" y="298" width="225" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="none"/>
  <text x="260" y="314" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Load (시스템 메모리 → 타일 메모리)</text>

  <!-- Box 3: 타일 메모리 (RT B) -->
  <rect x="130" y="364" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="386" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">타일 메모리</text>
  <text x="230" y="404" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(Render Target B)</text>
  <!-- Annotation: bandwidth again -->
  <text x="345" y="393" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">다시 대역폭 소비</text>

  <!-- Phase label: RT B rendering start -->
  <text x="260" y="440" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Render Target B에 렌더링 시작</text>

  <!-- Footnote -->
  <text x="260" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">* Load는 RT B에 이전 내용이 있을 때 발생</text>
  <text x="260" y="488" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">Clear/DontCare이면 생략 가능 (아래 Store/Load Actions 참고)</text>
</svg>
</div>

<br>

Render Target 전환마다 발생하는 Resolve(Store)와 Load, 두 번의 메모리 전송이 **대역폭을 소비**합니다.
모바일 기기에서 CPU와 GPU는 칩 외부의 시스템 메모리를 공유하며, 이 시스템 메모리의 대역폭은 한정되어 있습니다. Resolve와 Load가 누적되어 대역폭이 포화되면 프레임 시간이 늘어납니다.
또한 시스템 메모리 접근의 전력 소모는 칩 내부의 타일 메모리 접근에 비해 약 10배 이상 크기 때문에, 전환이 늘어날수록 발열과 배터리 소모도 직접 증가합니다.

### 최소화 전략

Render Target 전환 횟수를 줄이는 핵심 원칙은, 같은 Render Target에 가능한 한 많은 드로우콜을 묶어서 실행하는 것입니다.
예를 들어, 불투명 오브젝트 10개를 그린 뒤 후처리 RT로 전환하고, 다시 원래 RT로 돌아와 반투명 오브젝트를 그리면, RT 전환이 두 번 발생하면서 Resolve/Load도 두 번 반복됩니다. 불투명과 반투명을 모두 같은 RT에 연속으로 그린 뒤 한 번만 전환하면, 불필요한 Resolve/Load 한 쌍을 제거하여 대역폭을 절약할 수 있습니다.

### Store/Load Actions

전환 횟수를 줄이는 것 외에, 불필요한 Store와 Load 자체를 생략하는 방법도 있습니다.
예를 들어, 이후 패스에서 다시 읽지 않을 RT는 시스템 메모리에 저장(Store)할 필요가 없고, 전체를 새로 그릴 RT는 이전 내용을 불러올(Load) 필요가 없습니다. URP에서는 각 RT에 대해 Store와 Load를 수행할지 생략할지를 **Store/Load Action**으로 지정할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 480" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Store/Load Actions</text>

  <!-- === Store Action === -->
  <rect x="20" y="44" width="480" height="170" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="68" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Store Action (Render Target 사용 후)</text>

  <!-- Store -->
  <rect x="40" y="82" width="440" height="50" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="102" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Store</text>
  <text x="120" y="102" font-family="sans-serif" font-size="11" fill="currentColor">타일 메모리 → 시스템 메모리에 저장</text>
  <text x="120" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이 RT를 이후 패스에서 읽어야 할 때</text>

  <!-- DontCare -->
  <rect x="40" y="140" width="440" height="64" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="162" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DontCare</text>
  <text x="120" y="162" font-family="sans-serif" font-size="11" fill="currentColor">타일 메모리 내용을 버림 (Resolve 생략)</text>
  <text x="120" y="182" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이 RT의 내용이 이후에 필요 없을 때</text>
  <text x="120" y="196" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 대역폭 절약</text>

  <!-- === Load Action === -->
  <rect x="20" y="230" width="480" height="230" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="254" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Load Action (Render Target 사용 전)</text>

  <!-- Load -->
  <rect x="40" y="268" width="440" height="50" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="288" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Load</text>
  <text x="120" y="288" font-family="sans-serif" font-size="11" fill="currentColor">시스템 메모리 → 타일 메모리로 이전 내용 복사</text>
  <text x="120" y="308" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이전 패스의 결과 위에 추가로 그릴 때</text>

  <!-- Clear -->
  <rect x="40" y="326" width="440" height="64" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="348" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Clear</text>
  <text x="120" y="348" font-family="sans-serif" font-size="11" fill="currentColor">타일 메모리를 초기화 (Load 생략)</text>
  <text x="120" y="368" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">새로 그리기 시작할 때</text>
  <text x="120" y="382" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 대역폭 절약</text>

  <!-- DontCare -->
  <rect x="40" y="398" width="440" height="50" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="418" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DontCare</text>
  <text x="120" y="418" font-family="sans-serif" font-size="11" fill="currentColor">이전 내용 무시 (Load 생략)</text>
  <text x="120" y="438" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이전 내용이 필요 없고, 초기화도 불필요할 때</text>
</svg>
</div>

<br>

가장 비용이 낮은 조합은 Load Action = Clear(또는 DontCare), Store Action = DontCare입니다. 이 조합에서는 시스템 메모리와의 데이터 전송이 발생하지 않습니다.
반대로 Load Action = Load, Store Action = Store는 양방향 전송이 모두 발생하므로 비용이 가장 높습니다.

<br>

MSAA를 사용하면 Store에 추가 비용이 붙습니다. MSAA는 픽셀당 여러 샘플을 온칩 타일 메모리에 유지하다가, Store 시점에 샘플들을 하나의 최종 색상으로 합치는 **MSAA Resolve** 연산을 수행합니다.
Resolve 자체는 온칩에서 처리되어 추가 대역폭은 발생하지 않지만, GPU 연산 비용은 발생합니다. Store Action을 DontCare로 설정하면 Store뿐 아니라 Resolve도 함께 생략되므로, MSAA가 적용된 RT에서는 불필요한 Store를 DontCare로 설정하는 효과가 더 큽니다.

<br>

깊이/스텐실 버퍼처럼 현재 프레임에서만 필요하고 이후에 읽을 일이 없는 RT는 아예 시스템 메모리에 할당하지 않는 방법도 있습니다.
Unity에서 RenderTexture의 `memorylessMode`를 설정하면 해당 RT가 온칩 타일 메모리에만 존재하게 되어, Store 자체가 불가능해지는 대신 시스템 메모리 할당과 대역폭을 모두 절약할 수 있습니다.

<br>

실제 프로젝트에서는 여러 렌더 패스가 RT를 주고받으므로, 각 패스마다 Store/Load Action을 수동으로 최적화하는 작업이 복잡해지기 쉽습니다.
Unity 6 이상의 **Render Graph**는 이 문제를 자동화합니다. 한 프레임의 모든 렌더 패스를 그래프 구조로 선언하면, 각 패스가 RT를 읽고 쓰는 패턴을 분석하여 Store/Load Action을 자동으로 최적화합니다.

<br>

Render Target 전환 비용을 줄이는 것이 대역폭 측면의 최적화라면, 렌더링 해상도 자체를 동적으로 조절하는 것은 프래그먼트 셰이더 측면의 최적화에 해당합니다.

---

## Dynamic Resolution

**Dynamic Resolution**은 GPU 프레임 시간을 모니터링하다가 목표 프레임 레이트를 유지하기 어려워지면 렌더링 해상도를 동적으로 낮추는 기법입니다.
해상도가 낮아지면 Render Target의 픽셀 수가 줄어들고, 래스터화 단계에서 생성되는 프래그먼트 수도 비례하여 감소하므로 프래그먼트 셰이더 호출 횟수가 줄어듭니다. 해상도 축소는 가로·세로 모두에 적용되므로 프래그먼트 수는 비율의 제곱으로 줄어듭니다. 예를 들어 해상도를 80 %로 낮추면 프래그먼트 수는 약 64 %가 되고, 70 %로 낮추면 약 49 %가 됩니다.
프래그먼트가 줄어들면 Render Target에 쓰는 데이터량도 함께 줄어드므로 메모리 대역폭 사용량도 감소합니다. 따라서 프래그먼트 셰이더 연산이 병목이거나, Render Target 읽기/쓰기 대역폭이 병목인 **GPU Bound** 상황에서 직접적인 효과가 있습니다.

모바일 GPU는 시스템 메모리를 공유하여 대역폭 제약이 데스크톱 대비 크므로, 해상도를 낮추는 것만으로도 프레임 시간이 눈에 띄게 줄어드는 경우가 많습니다. 반면, CPU에서 드로우콜 제출이 병목인 CPU Bound 상황에서는 해상도를 낮추어도 개선되지 않습니다. Dynamic Resolution이 줄이는 것은 GPU가 처리하는 프래그먼트 수와 대역폭이며, CPU 측 드로우콜 준비·제출 작업량은 변하지 않기 때문입니다.

<br>

### 설정 방법

URP에서는 URP Asset의 Quality 섹션과 Camera 컴포넌트의 `Allow Dynamic Resolution`, 두 곳 모두 활성화해야 동작합니다.

다만, 이 설정만으로 해상도가 자동으로 조절되지는 않습니다. 실제 해상도 비율은 스크립트에서 `ScalableBufferManager.ResizeBuffers(widthScale, heightScale)`를 호출하여 직접 제어합니다. widthScale과 heightScale은 0.0~1.0 범위이며, 1.0이 원본 해상도에 해당합니다. 매 프레임 GPU 시간을 측정하여 목표를 초과하면 비율을 낮추고, 여유가 생기면 비율을 올리는 방식으로 구현합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 470" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Title -->
  <text x="250" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Dynamic Resolution 적용 흐름</text>

  <!-- Label: 매 프레임 -->
  <text x="250" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">매 프레임</text>

  <!-- Step 1: GPU 시간 측정 -->
  <rect x="100" y="58" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="81" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1) 이전 프레임의 GPU 시간 측정</text>

  <!-- Arrow -->
  <line x1="250" y1="94" x2="250" y2="116" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="243,110 250,122 257,110" fill="currentColor"/>

  <!-- Step 2: 목표 비교 -->
  <rect x="100" y="124" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(2) 목표 프레임 시간과 비교 (예: 16.67ms)</text>

  <!-- Arrow splitting into two branches -->
  <line x1="250" y1="160" x2="250" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <line x1="250" y1="180" x2="130" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <line x1="250" y1="180" x2="370" y2="180" stroke="currentColor" stroke-width="1.5"/>
  <line x1="130" y1="180" x2="130" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="123,194 130,206 137,194" fill="currentColor"/>
  <line x1="370" y1="180" x2="370" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="363,194 370,206 377,194" fill="currentColor"/>

  <!-- Left branch: GPU 시간 > 목표 -->
  <rect x="30" y="208" width="200" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 시간 > 목표</text>
  <text x="130" y="248" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">ResizeBuffers(0.8f, 0.8f)</text>
  <text x="130" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 해상도 80%로 낮춤</text>

  <!-- Right branch: GPU 시간 < 목표 * 0.8 -->
  <rect x="270" y="208" width="200" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="370" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 시간 &lt; 목표 * 0.8</text>
  <text x="370" y="248" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">ResizeBuffers(1.0f, 1.0f)</text>
  <text x="370" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 해상도 100%로 복원</text>

  <!-- Merge arrows -->
  <line x1="130" y1="288" x2="130" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <line x1="370" y1="288" x2="370" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <line x1="130" y1="320" x2="370" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <line x1="250" y1="320" x2="250" y2="340" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="243,334 250,346 257,334" fill="currentColor"/>

  <!-- Step 3: 렌더링 실행 -->
  <rect x="100" y="348" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="371" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(3) 렌더링 실행 (조절된 해상도로)</text>

  <!-- Arrow -->
  <line x1="250" y1="384" x2="250" y2="406" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="243,400 250,412 257,400" fill="currentColor"/>

  <!-- Step 4: 업스케일 -->
  <rect x="100" y="414" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="437" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(4) 결과를 화면 해상도로 업스케일</text>
</svg>
</div>

<br>

해상도를 낮추면 원본보다 적은 픽셀로 렌더링하므로, 최종 디스플레이 해상도로 늘리는 업스케일링 과정에서 이미지가 흐려질 수 있습니다. 원본에 존재하지 않는 픽셀을 주변 값으로부터 추정해야 하기 때문입니다.
단순 바이리니어(Bilinear) 필터링은 인접 4개 픽셀의 가중 평균으로 보간하므로 결과가 흐릿해지기 쉽습니다. **바이큐빅(Bicubic)** 필터링은 참조 범위를 4×4 픽셀로 넓혀 보다 부드러운 보간을 제공하고, **AMD FSR(FidelityFX Super Resolution)**은 여기에 에지 보존 알고리즘까지 적용하여 선명도를 높입니다.

### UI와 Dynamic Resolution

**UI는 Dynamic Resolution 대상에서 제외해야 합니다.**
텍스트와 아이콘은 해상도가 낮아지면 즉시 눈에 띄게 흐려집니다. URP에서 UI 카메라를 Overlay Camera로 구성하고, 해당 카메라에서 Allow Dynamic Resolution을 비활성화하면 UI는 항상 원본 해상도로 렌더링됩니다.
creen Space - Overlay 모드의 Canvas는 렌더 파이프라인 바깥에서 그려지므로, Dynamic Resolution의 영향을 받지 않습니다.

<br>

Dynamic Resolution이 해상도를 조절하여 프래그먼트 수를 줄이는 기법이라면, 컬러 포맷은 각 픽셀이 차지하는 바이트 수를 결정하여 메모리와 대역폭에 직접 영향을 미치는 요소입니다.

---

## 컬러 포맷과 메모리

Render Target의 메모리 크기는 해상도뿐 아니라 컬러 포맷에 의해서도 결정됩니다.
컬러 포맷은 각 픽셀에 저장되는 색상 데이터의 크기(바이트 수)와 정밀도(비트 수)를 규정하며, 픽셀당 바이트 수가 클수록 한 픽셀을 읽고 쓸 때 이동하는 데이터량이 증가합니다.

### LDR 포맷

**R8G8B8A8_UNorm**은 가장 기본적인 LDR(Low Dynamic Range) 포맷입니다. R, G, B, A 각 채널이 8비트(0~255)이며, 픽셀당 **4바이트**를 사용합니다. 각 채널의 값은 0.0~1.0 범위의 정규화된 부호 없는 정수(Unsigned Normalized)로 해석되며, 포맷 이름의 "UNorm"이 이를 나타냅니다.
일반적인 게임에서 후처리 없이 화면에 직접 출력하는 컬러 버퍼의 기본 포맷이며, 메모리와 대역폭 측면에서 가장 효율적인 컬러 포맷입니다.

### HDR 포맷

LDR 포맷은 각 채널 값이 0.0~1.0 범위로 제한됩니다. 태양광이나 폭발 이펙트처럼 1.0보다 밝은 값은 모두 1.0으로 잘려(Clamp) 버리므로, 밝기 차이가 사라집니다.
후처리에서 Bloom이나 톤 매핑을 사용하려면, 1.0을 초과하는 밝기 값을 저장할 수 있는 HDR(High Dynamic Range) 포맷이 필요합니다. HDR 포맷은 부동소수점을 사용하여 이 범위를 넘어서는 값을 저장합니다.

<br>

**R16G16B16A16_SFloat**는 채널당 16비트 부동소수점, 픽셀당 **8바이트**입니다. 정밀도가 높지만 메모리 사용량이 LDR의 두 배입니다.

<br>

**R11G11B10_UFloat**는 R과 G가 11비트, B가 10비트 부동소수점이며, 알파 채널이 없습니다. 픽셀당 **4바이트**로 LDR과 같은 메모리를 사용하면서 HDR을 지원합니다.
다만 R16G16B16A16_SFloat(가수부 10비트)에 비해 가수부가 R/G 6비트, B 5비트로 정밀도가 낮고, 부호 비트가 없어 음수 값을 저장할 수 없습니다. 정밀도가 낮으면 어두운 영역의 미세한 밝기 차이를 구분하지 못하여 색상이 계단처럼 끊기는 밴딩(Banding)이 나타날 수 있습니다.
그럼에도 알파가 필요 없는 컬러 버퍼에 HDR이 필요할 때 메모리 효율 면에서 최적의 선택입니다. 모바일에서 HDR 렌더링이 필요한 경우, R16G16B16A16_SFloat 대신 R11G11B10_UFloat를 사용하면 메모리와 대역폭을 절반으로 줄일 수 있으며, 밴딩이 문제가 되면 디더링(Dithering)으로 완화할 수 있습니다.

<br>

**컬러 포맷 비교**

| 포맷 | 픽셀당 바이트 | HDR 지원 | 알파 채널 |
|------|------|------|------|
| R8G8B8A8_UNorm | 4 | X | O (8bit) |
| R16G16B16A16_SFloat | 8 | O | O (16bit) |
| R11G11B10_UFloat | 4 | O | X |
| B10G11R11_UFloat | 4 | O | X |

R11G11B10_UFloat와 B10G11R11_UFloat는 같은 32비트 HDR 포맷이며, 채널 배치 순서만 다릅니다. 플랫폼에 따라 지원하는 이름이 다를 수 있습니다.

### Depth 포맷

컬러 버퍼와 마찬가지로, 깊이 버퍼도 포맷에 따라 픽셀당 바이트 수가 다릅니다. 깊이 버퍼는 각 픽셀의 카메라로부터의 거리를 기록하며, 이 값으로 앞뒤 가림(Depth Test)을 판별합니다. 포맷의 비트 수가 높을수록 정밀도가 올라가지만 메모리 사용량도 증가합니다.

<br>

**Depth 포맷 비교**

| 포맷 | 픽셀당 바이트 | 설명 |
|------|------|------|
| D16 | 2 | 16비트 깊이, 정밀도 낮음 |
| D24S8 | 4 | 24비트 깊이 + 8비트 스텐실 |
| D32_SFloat | 4 | 32비트 부동소수점 깊이 |
| D32_SFloat_S8 | 8 | 32비트 깊이 + 8비트 스텐실 |

<br>

D16은 메모리가 적지만 정밀도가 낮아 **Z-fighting**이 발생하기 쉽습니다.
Z-fighting은 깊이 값이 거의 같은 두 표면이 정밀도 부족으로 앞뒤 판별이 프레임마다 뒤바뀌며 깜빡이는 현상입니다. [Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 다룬 것처럼, Near/Far 비율이 클수록 깊이 정밀도가 부족해지므로 D16에서는 문제가 더 두드러집니다.

D24S8은 깊이 24비트에 스텐실 8비트를 포함합니다. 스텐실 버퍼는 픽셀 단위의 마스킹에 사용되며, 아웃라인 효과나 포탈 마스킹처럼 특정 영역만 렌더링하거나 제외하는 처리에 필요합니다.

D32_SFloat는 가장 높은 깊이 정밀도를 제공하지만 스텐실을 포함하지 않습니다.

높은 깊이 정밀도와 스텐실이 모두 필요한 경우 D32_SFloat_S8을 선택합니다. HDRP Deferred 렌더링에서는 스텐실 버퍼로 머티리얼 유형을 분류하므로, 이 포맷이 기본 깊이 포맷입니다. 다만 픽셀당 8바이트로 D24S8의 두 배이며, 1080p 기준 깊이 버퍼만 약 15.8MB를 차지합니다.

<br>

모바일에서는 깊이와 스텐실을 함께 사용하면서도 메모리를 절약해야 하므로 D24S8이 일반적인 선택입니다.

### 해상도별 메모리 계산 예시

포맷별 픽셀당 바이트 수를 알았으니, 실제 해상도와 조합하여 메모리 사용량을 구체적으로 계산해 봅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Title -->
  <text x="250" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">해상도별 Render Target 메모리</text>

  <!-- ===== Full HD ===== -->
  <text x="12" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1920 × 1080 (Full HD)</text>

  <text x="155" y="68" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">R8G8B8A8 (4B/px)</text>
  <rect x="160" y="57" width="68" height="14" rx="2" fill="currentColor" fill-opacity="0.12"/>
  <text x="233" y="68" font-family="sans-serif" font-size="10" fill="currentColor">7.9 MB</text>

  <text x="155" y="88" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">R16G16B16A16 (8B/px)</text>
  <rect x="160" y="77" width="135" height="14" rx="2" fill="currentColor" fill-opacity="0.12"/>
  <text x="300" y="88" font-family="sans-serif" font-size="10" fill="currentColor">15.8 MB</text>

  <text x="155" y="108" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">R11G11B10 (4B/px)</text>
  <rect x="160" y="97" width="68" height="14" rx="2" fill="currentColor" fill-opacity="0.12"/>
  <text x="233" y="108" font-family="sans-serif" font-size="10" fill="currentColor">7.9 MB</text>

  <text x="155" y="128" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">D24S8 (4B/px)</text>
  <rect x="160" y="117" width="68" height="14" rx="2" fill="currentColor" fill-opacity="0.12"/>
  <text x="233" y="128" font-family="sans-serif" font-size="10" fill="currentColor">7.9 MB</text>

  <!-- Separator -->
  <line x1="160" y1="140" x2="420" y2="140" stroke="currentColor" stroke-width="0.5" opacity="0.2" stroke-dasharray="3,3"/>

  <text x="155" y="158" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">LDR + Depth</text>
  <rect x="160" y="147" width="135" height="14" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <text x="300" y="158" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">15.8 MB</text>

  <text x="155" y="178" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">HDR 16F + Depth</text>
  <rect x="160" y="167" width="202" height="14" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <text x="367" y="178" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">23.7 MB</text>

  <!-- ===== QHD ===== -->
  <text x="12" y="210" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2560 × 1440 (QHD)</text>

  <text x="155" y="230" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">R8G8B8A8 (4B/px)</text>
  <rect x="160" y="219" width="120" height="14" rx="2" fill="currentColor" fill-opacity="0.12"/>
  <text x="285" y="230" font-family="sans-serif" font-size="10" fill="currentColor">14.1 MB</text>

  <text x="155" y="250" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">LDR + Depth</text>
  <rect x="160" y="239" width="240" height="14" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <text x="405" y="250" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">28.1 MB</text>

  <!-- ===== Mobile ===== -->
  <text x="12" y="282" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">720 × 1280 (모바일 세로)</text>

  <text x="155" y="302" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor">R8G8B8A8 (4B/px)</text>
  <rect x="160" y="291" width="30" height="14" rx="2" fill="currentColor" fill-opacity="0.12"/>
  <text x="195" y="302" font-family="sans-serif" font-size="10" fill="currentColor">3.5 MB</text>

  <text x="155" y="322" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">LDR + Depth</text>
  <rect x="160" y="311" width="60" height="14" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <text x="225" y="322" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold">7.0 MB</text>
</svg>
</div>

### 모바일에서의 포맷 선택 가이드

모바일 환경에서는 메모리와 대역폭이 제한되므로, 필요한 최소한의 포맷을 선택해야 합니다. HDR이 불필요하면 R8G8B8A8_UNorm을, HDR이 필요하지만 알파가 불필요하면 R11G11B10_UFloat를 사용하는 것이 적합합니다. 깊이 버퍼는 D24S8이 균형 잡힌 선택이며, 스텐실이 불필요하고 정밀도를 더 원하면 D32_SFloat를 고려합니다.

<br>

---

## Render Target 메모리 총합 관리

개별 RT의 메모리를 아무리 절약해도, 한 프레임에 동시에 활성화되는 RT가 많으면 총합이 GPU 메모리 예산을 초과할 수 있습니다. 메인 컬러 RT와 깊이 RT 외에도 그림자 맵, 후처리 중간 텍스처, G-Buffer 등이 더해지므로, 실제 프레임의 RT 메모리는 개별 RT를 따로 볼 때보다 훨씬 큽니다.

이 중 **G-Buffer(Geometry Buffer)**는 Deferred 렌더링에서 사용하는 다중 RT 구조로, 각 픽셀의 표면 정보(색상, 법선, 재질 등)를 별도의 RT에 먼저 기록해 두고 이후 조명 계산을 일괄 수행합니다.

<br>

**한 프레임의 Render Target 메모리 예시 (URP, Full HD, HDR)**

| Render Target | 포맷 | 메모리 |
|------|------|------|
| 메인 컬러 RT | R11G11B10 | 7.9 MB |
| 메인 깊이 RT | D24S8 | 7.9 MB |
| Shadow Map (2048x2048) | D16 | 8.0 MB |
| Bloom 다운샘플 체인 | R11G11B10 | ~3.0 MB (합산) |
| 후처리 Temp RT | R11G11B10 | 7.9 MB |
| **합계** | | **≈ 34.7 MB** |

Deferred 렌더링 추가 시 (HDRP, 구성은 버전에 따라 다름):

| G-Buffer | 포맷 | 메모리 |
|------|------|------|
| G-Buffer 0 (BaseColor 등) | RGBA32 계열 | 7.9 MB |
| G-Buffer 1 (Normal 등) | RGBA32 계열 | 7.9 MB |
| G-Buffer 2 (Material 등) | RGBA32 계열 | 7.9 MB |
| G-Buffer 3 (Lighting 등) | RGBA32 계열 | 7.9 MB |

G-Buffer만 약 32 MB 추가 (4장 기준, Light Layers 등 활성화 시 더 증가)

<br>

Deferred 렌더링을 사용하는 HDRP는 G-Buffer가 여러 장의 RT를 추가로 사용하므로, Forward 렌더링의 URP에 비해 Render Target 메모리가 크게 증가합니다.
모바일에서 Deferred가 비현실적인 이유는 메모리뿐이 아닙니다. [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 것처럼, 모바일 GPU(TBDR)는 타일 단위로 렌더링한 결과를 시스템 메모리에 Store/Load하는 구조이므로, G-Buffer 4장을 모두 Store하고 조명 패스에서 다시 Load하는 과정에서 발생하는 대역폭 비용이 메모리 사용량 이상으로 큰 부담이 됩니다.

### Shadow Map의 메모리

그림자 맵(Shadow Map)도 Render Target에 해당합니다.
조명의 시점에서 씬을 렌더링하여 깊이 정보만 기록한 텍스처이며, 이 깊이 값을 카메라 시점의 깊이와 비교하여 그림자 영역을 판별하는 데 사용됩니다.

앞의 메모리 예시에서 2048x2048 해상도의 Shadow Map이 8MB를 차지하고 있습니다. [조명과 그림자 (2)](/dev/unity/LightingAndShadows-2/)에서 다루듯, 그림자 해상도가 높을수록 메모리 사용량도 함께 증가합니다.

<br>

**캐스케이드 그림자(Cascaded Shadow Map)**는 카메라에서 가까운 영역과 먼 영역의 그림자 정밀도를 분리하기 위해 여러 장의 그림자 맵을 사용하는 기법입니다. 카메라에 가까운 영역은 높은 정밀도가 필요하고 먼 영역은 낮은 정밀도로도 충분하므로, 거리 구간별로 별도의 그림자 맵을 생성하여 정밀도를 차등 배분합니다.

<br>

URP에서 그림자 해상도를 2048로 설정하고 4개의 캐스케이드를 사용하면, 각 캐스케이드가 2048x2048 크기의 그림자 맵을 생성합니다.
Unity는 이 4장을 하나의 아틀라스 텍스처(여러 작은 이미지를 한 장에 모아 놓은 구조)에 2x2 격자로 배치하므로, 최종 텍스처 크기는 4096x4096이 됩니다. D16 포맷 기준으로 4096 x 4096 x 2바이트 = 약 32MB에 달합니다. 단일 Shadow Map의 8MB와 비교하면 4배 증가한 수치입니다.
모바일에서는 캐스케이드 수를 줄이거나 그림자 해상도를 낮추어 이 메모리를 관리해야 합니다.

### Frame Debugger로 RT 확인

Unity의 **Frame Debugger**(Window > Analysis > Frame Debugger)를 사용하면, 현재 프레임에서 사용되는 모든 Render Target을 단계별로 확인할 수 있습니다.
각 드로우콜이 어떤 RT에 쓰고 있는지, RT의 해상도와 포맷이 무엇인지, Render Target 전환이 몇 번 발생하는지가 시각적으로 드러납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- Title -->
  <text x="270" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Frame Debugger 활용</text>

  <!-- Left box: 확인 가능 정보 -->
  <rect x="10" y="32" width="252" height="150" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="136" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">확인 가능 정보</text>
  <line x1="24" y1="58" x2="248" y2="58" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <text x="24" y="76" font-family="sans-serif" font-size="10" fill="currentColor">(1) 렌더 패스별 Render Target</text>
  <text x="24" y="94" font-family="sans-serif" font-size="10" fill="currentColor">(2) RT 해상도, 포맷, 메모리 크기</text>
  <text x="24" y="112" font-family="sans-serif" font-size="10" fill="currentColor">(3) Render Target 전환 횟수</text>
  <text x="24" y="130" font-family="sans-serif" font-size="10" fill="currentColor">(4) Store/Load Action (URP)</text>
  <text x="24" y="148" font-family="sans-serif" font-size="10" fill="currentColor">(5) 드로우콜의 셰이더·머티리얼·메쉬</text>

  <!-- Arrow -->
  <line x1="266" y1="107" x2="274" y2="107" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="273,103 280,107 273,111" fill="currentColor" opacity="0.4"/>

  <!-- Right box: 최적화 점검 항목 -->
  <rect x="284" y="32" width="246" height="150" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="407" y="52" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">최적화 점검 항목</text>
  <line x1="298" y1="58" x2="516" y2="58" stroke="currentColor" stroke-width="0.5" opacity="0.15"/>
  <text x="298" y="76" font-family="sans-serif" font-size="10" fill="currentColor">- 불필요하게 큰 해상도의 RT</text>
  <text x="298" y="94" font-family="sans-serif" font-size="10" fill="currentColor">- 불필요한 Render Target 전환</text>
  <text x="298" y="112" font-family="sans-serif" font-size="10" fill="currentColor">- DontCare 가능한 Store Action</text>
  <text x="298" y="130" font-family="sans-serif" font-size="10" fill="currentColor">- 미사용 RT의 할당 여부</text>
</svg>
</div>

<br>

Render Target은 런타임에 GPU가 생성하는 버퍼이므로, 텍스처나 메쉬처럼 에셋 목록에서 바로 확인되지 않습니다. Frame Debugger로 각 RT의 포맷과 해상도를 파악하고, 프로파일러의 Memory 모듈로 실제 점유량을 병행 확인해야 합니다. 모바일에서는 전체 GPU 메모리 예산이 제한적이므로, 텍스처 메모리와 RT 메모리를 합산하여 예산 안에서 관리하는 것이 필수적입니다.

---

## 마무리

- **Back Buffer**는 최종 디스플레이에 표시되는 기본 Render Target이며, Double Buffering으로 Tearing을 방지합니다.
- **RenderTexture**는 렌더링 결과를 텍스처 형태로 저장하는 Render Target으로, 미사용 시 Release가 필수입니다.
- **Temporary Render Texture**는 풀에서 RT를 재사용하여 매 프레임 할당/해제 비용을 줄입니다.
- 모바일 GPU(TBDR)에서 **Render Target 전환**은 Resolve/Load를 유발하며, Store/Load Action 설정이 대역폭 절약의 핵심입니다.
- **Dynamic Resolution**은 GPU Bound 상황에서 해상도를 낮추어 프래그먼트 셰이더 부하를 줄입니다. UI는 대상에서 제외해야 합니다.
- **컬러 포맷**은 HDR이 불필요하면 R8G8B8A8_UNorm, HDR이 필요하면 R11G11B10_UFloat가 모바일에 적합합니다.
- 한 프레임에 활성화되는 모든 RT의 **메모리 합**을 Frame Debugger로 확인하고 예산 안에서 관리해야 합니다.

<br>

Render Target은 GPU가 렌더링 결과를 기록하는 메모리 영역입니다.
그 종류(Back Buffer, RenderTexture, Temporary RT)에 따라 수명과 용도가 다르지만, 해상도와 컬러 포맷에 따라 수~수십 MB의 GPU 메모리를 점유한다는 점은 동일합니다.
모바일에서는 Render Target 전환마다 대역폭을 소비하므로, 전환 횟수를 줄이고 Store/Load Action을 적절히 설정하는 것이 성능에 직접적으로 영향을 미칩니다.

<br>

[Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 카메라가 무엇을 어떤 순서로 그리는지를, 이 글에서 그 결과가 어디에 저장되는지를 다루었습니다. [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)에서는 카메라, 렌더링 순서, Render Target 관리를 하나의 흐름으로 엮는 렌더 파이프라인의 종류와 선택 기준을 다룹니다.

<br>

---

**관련 글**
- [래스터화 파이프라인 (2) - 버퍼 시스템](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3)](/dev/unity/RasterPipeline-3/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [조명과 그림자 (2)](/dev/unity/LightingAndShadows-2/)

**시리즈**
- [Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)
- **Unity 렌더링 (2) - Render Target과 Frame Buffer (현재 글)**
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)

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
- **Unity 렌더링 (2) - Render Target과 Frame Buffer** (현재 글)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
