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

[Unity 렌더링 (1) - Camera와 Rendering Layer](/dev/unity/UnityRendering-1/)에서는 카메라가 무엇을 어떤 순서로 그리는지를 살펴보았습니다. 이제 그 다음 단계는 GPU가 계산한 결과를 어디에 기록하는가입니다.

카메라가 드로우콜을 제출하면 GPU는 정점을 변환하고, 래스터화를 거쳐 프래그먼트를 만들고, 프래그먼트 셰이더에서 픽셀의 색을 계산합니다. 이 색이 최종적으로 기록되는 대상이 **Render Target**입니다. 화면에 바로 표시될 Back Buffer도 Render Target이고, 화면 대신 텍스처에 결과를 남기는 RenderTexture도 Render Target입니다.

Render Target은 단순한 출력 위치가 아니라 메모리와 대역폭 비용을 만드는 대상입니다. 해상도와 컬러 포맷에 따라 필요한 메모리가 달라지고, 한 프레임 안에서 Render Target을 자주 바꾸면 모바일 GPU에서는 추가 대역폭 비용이 생길 수 있습니다. 이 글에서는 Back Buffer, RenderTexture, Temporary RT의 역할을 먼저 정리한 뒤, Render Target 전환 비용과 메모리 계산 방법을 차례로 살펴보겠습니다.

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

**Back Buffer**는 GPU가 화면에 보낼 다음 프레임을 그려 넣는 기본 Render Target입니다. Unity에서 카메라의 **Target Texture**를 비워 두면, 카메라가 그린 결과는 별도의 RenderTexture가 아니라 Back Buffer에 기록됩니다.

Back Buffer는 그리는 동안에는 아직 화면에 보이지 않습니다. 한 프레임의 렌더링이 끝나면 이 버퍼가 표시 대상이 되고, 디스플레이는 그 내용을 읽어 실제 화면으로 내보냅니다. 즉 Back Buffer는 게임 화면의 최종 출력으로 넘어가기 직전의 렌더링 결과를 담는 버퍼입니다.

### Double Buffering

화면 표시와 렌더링이 같은 버퍼를 동시에 사용하면 문제가 생깁니다. 디스플레이는 화면에 표시할 이미지를 보통 위에서 아래 방향으로 순서대로 읽어 가는데, 이 도중 GPU가 같은 버퍼에 다음 프레임을 덮어쓰면 한 화면 안에 이전 프레임과 새 프레임이 섞일 수 있습니다. 이때 화면이 가로로 어긋나 찢어진 것처럼 보이는 현상을 **Tearing**이라고 합니다.

**Double Buffering**은 이 충돌을 피하기 위해 버퍼를 두 개로 나누는 방식입니다. 디스플레이가 현재 읽고 있는 버퍼를 **Front Buffer**, GPU가 다음 프레임을 그리고 있는 버퍼를 **Back Buffer**라고 부릅니다. 디스플레이는 Front Buffer만 읽고 GPU는 Back Buffer에만 쓰므로, 읽기와 쓰기가 같은 메모리에서 겹치지 않습니다.

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

한 프레임이 완성되면 Front Buffer와 Back Buffer는 역할을 바꿉니다. 이 교체를 **Swap**이라고 합니다. Swap은 보통 두 버퍼의 픽셀 데이터를 통째로 복사하는 작업이 아니라, 표시할 버퍼와 다음에 그릴 버퍼를 바꾸는 동작에 가깝습니다. 따라서 핵심 비용은 교체 자체보다 **언제 교체하느냐**에서 발생합니다.

[래스터화 파이프라인 (3)](/dev/unity/RasterPipeline-3/)에서 다룬 **VSync(수직 동기화)**는 Swap 시점을 디스플레이의 수직 귀선 기간(Vertical Blanking Interval, VBI)에 맞춥니다. VBI는 디스플레이가 한 화면을 다 읽고 다음 화면을 읽기 시작하기 전의 짧은 구간입니다. 이때 버퍼를 바꾸면 화면을 읽는 도중에 내용이 바뀌지 않으므로 Tearing을 막을 수 있습니다.

대신 VSync가 켜져 있으면 GPU가 프레임을 일찍 끝내도 곧바로 화면에 표시할 수 없습니다. 다음 VSync 시점까지 기다렸다가 Swap이 일어납니다. 반대로 GPU가 한 VSync 간격 안에 프레임을 끝내지 못하면, 그 프레임은 다음 표시 기회를 기다려야 합니다. 60Hz 디스플레이에서는 한 간격이 약 16.67ms이므로, 이 시점을 놓치면 표시가 한 간격 뒤로 밀리고 체감 프레임 레이트가 크게 떨어질 수 있습니다.

이 급격한 하락을 완화하기 위해 버퍼를 하나 더 두는 방식이 **Triple Buffering**입니다. 추가 버퍼가 있으면 GPU가 표시 대기 중인 버퍼와 별개로 다음 프레임을 계속 그릴 수 있어, 한 번의 VSync 간격을 놓쳤을 때 작업이 바로 멈추는 상황을 줄일 수 있습니다. 대신 화면에 표시되기 전까지 대기 중인 프레임이 늘어날 수 있으므로 입력 지연이 커질 수 있고, 버퍼 하나만큼의 GPU 메모리도 추가로 필요합니다.

모바일에서는 보통 화면 주사율에 맞춰 렌더링을 끝내는 것이 기본 전제입니다. 60Hz라면 한 프레임 예산은 약 16.67ms이고, 120Hz라면 약 8.33ms입니다. Render Target 비용을 따질 때도 이 시간 안에 렌더링, 후처리, 버퍼 전환까지 들어와야 한다는 점을 함께 봐야 합니다.

---

## RenderTexture

카메라가 그린 결과를 항상 Back Buffer로 보낼 필요는 없습니다. 어떤 경우에는 화면에 바로 표시하지 않고, 먼저 텍스처에 저장한 뒤 다른 렌더링 과정에서 다시 사용해야 합니다. 미니맵, 거울, 포탈, 후처리 효과가 이런 구조를 사용합니다.

이처럼 GPU가 런타임에 그린 결과를 담는 텍스처형 Render Target이 **RenderTexture**입니다. `Texture2D`가 디스크에서 읽어 온 이미지 데이터를 담는 텍스처라면, RenderTexture는 GPU가 직접 렌더링해서 채우는 텍스처입니다.

Camera 컴포넌트의 **Target Texture**에 RenderTexture를 지정하면, 그 카메라의 출력은 Back Buffer가 아니라 해당 RenderTexture에 기록됩니다. 이렇게 만든 결과는 UI에 표시하거나, 머티리얼에 연결하거나, 다음 셰이더 패스의 입력으로 사용할 수 있습니다.

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

**미니맵**은 메인 카메라와 다른 시점의 화면을 UI 안에 넣어야 하므로 RenderTexture와 잘 맞습니다. 위에서 내려다보는 전용 카메라가 씬을 RenderTexture에 그리고, UI는 그 텍스처를 RawImage로 표시합니다. 이때 [Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 다룬 Culling Mask를 미니맵 전용 레이어로 좁히면, 지도에 필요한 오브젝트만 렌더링하도록 제한할 수 있습니다.

**거울과 포탈**은 표면 안에 다른 시점의 장면을 보여 주는 경우입니다. 반사 방향이나 포탈 너머 위치에 별도 카메라를 두고, 그 결과를 RenderTexture에 기록한 뒤 거울 메쉬나 포탈 면의 머티리얼에 연결합니다. 화면에는 표면 자체가 다른 공간을 비추는 것처럼 보이지만, 실제로는 다른 카메라가 만든 이미지를 텍스처로 붙여 보여 주는 구조입니다.

**후처리**에서는 RenderTexture가 중간 결과를 넘기는 버퍼가 됩니다. 카메라가 그린 화면을 먼저 RenderTexture에 기록하고, Bloom이나 Color Grading 같은 셰이더 패스가 이를 입력으로 읽어 다른 RenderTexture에 결과를 씁니다. 여러 효과가 이어지면 한 패스의 출력이 다음 패스의 입력이 되므로, RenderTexture를 읽고 쓰는 단계가 체인처럼 연결됩니다.

### RenderTexture의 메모리 비용

RenderTexture는 GPU가 읽고 쓰는 실제 렌더링 버퍼이므로, 생성하는 순간 GPU 메모리를 차지합니다. 기본 메모리는 **가로 해상도 x 세로 해상도 x 픽셀당 바이트 수**로 계산합니다. 해상도가 커질수록 픽셀 수가 늘고, 컬러 포맷이 클수록 픽셀 하나가 차지하는 바이트도 늘어납니다.

예를 들어 1920x1080 RenderTexture를 RGBA32 포맷으로 만들면 픽셀당 4바이트를 사용하므로 컬러 버퍼만 약 7.9MB가 필요합니다. 같은 해상도에서 R16G16B16A16처럼 픽셀당 8바이트를 쓰는 HDR 포맷을 선택하면 약 15.8MB까지 늘어납니다. 다만 Unity의 Default HDR은 플랫폼과 설정에 따라 R11G11B10 같은 더 작은 포맷으로 선택될 수 있으므로, 실제 포맷은 대상 플랫폼에서 확인해야 합니다.

따라서 RenderTexture의 해상도는 실제 표시 크기와 용도에 맞춰 잡아야 합니다. 화면 한쪽에 256x256으로 표시되는 미니맵에 1920x1080 RenderTexture를 쓰면, 화면에 보이지도 않을 픽셀까지 렌더링하게 됩니다. 해상도가 커지면 메모리만 늘어나는 것이 아니라, 래스터화되는 프래그먼트 수와 프래그먼트 셰이더 실행량, 읽기/쓰기 대역폭까지 함께 늘어납니다.

수명 관리도 별도로 봐야 합니다. RenderTexture 객체는 C# 래퍼일 뿐이고, 실제 렌더링 버퍼는 GPU 리소스입니다. 더 이상 사용하지 않는 RenderTexture라면 `RenderTexture.Release()`를 호출해 GPU 리소스를 명시적으로 반환해야 합니다. C# 객체가 언젠가 GC 대상이 되는 것과 GPU 메모리가 필요한 시점에 해제되는 것은 같은 문제가 아닙니다.

`Release()`를 호출하지 않으면 RenderTexture가 더 이상 화면에 쓰이지 않아도 GPU 메모리에 남을 수 있습니다. 특히 매니저나 정적 필드가 RenderTexture 참조를 들고 있으면 씬이 바뀐 뒤에도 리소스가 유지될 수 있습니다. 미니맵이나 거울처럼 직접 생성해 오래 쓰는 RenderTexture는 소유한 컴포넌트의 `OnDestroy`나 씬 전환 정리 지점에서 해제하는 편이 안전합니다.

이처럼 직접 만들고 직접 해제하는 방식은 미니맵이나 거울처럼 수명이 긴 RenderTexture에 잘 맞습니다. 반면 후처리 체인처럼 매 프레임 잠깐 쓰는 중간 버퍼를 매번 생성하고 해제하면 할당 비용이 반복됩니다. 이런 경우에는 다음 절에서 볼 Temporary Render Texture처럼 풀에서 빌려 쓰고 반환하는 방식이 더 적합합니다.

---

## Temporary Render Texture

후처리나 중간 렌더 패스에서는 RenderTexture가 한 프레임 안에서 잠깐만 필요할 때가 많습니다. 이런 버퍼를 매번 새로 만들고 해제하면 GPU 리소스 할당과 반환이 프레임마다 반복됩니다.

Unity는 이 비용을 줄이기 위해 임시 RenderTexture 풀을 제공합니다. `RenderTexture.GetTemporary()`로 필요한 규격의 RT를 빌려 쓰고, 사용이 끝나면 `RenderTexture.ReleaseTemporary()`로 풀에 돌려놓습니다. 같은 규격의 RT가 다시 필요할 때는 새로 할당하지 않고 풀에 있던 리소스를 재사용할 수 있습니다.

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

후처리 효과는 보통 여러 개의 셰이더 패스로 나뉩니다. 한 패스는 이전 결과를 텍스처로 읽고, 처리 결과를 또 다른 텍스처에 씁니다. 이때 단계 사이를 지나가는 중간 결과는 오래 보관할 필요가 없으므로 Temporary RT로 다루기 좋습니다.

중요한 점은 패스가 끝난 뒤 더 이상 읽지 않을 RT를 바로 풀에 반환하는 것입니다. 이렇게 하면 한 프레임 안에서 동시에 살아 있어야 하는 RT 수를 줄일 수 있고, 다음 패스나 다음 프레임에서 같은 규격의 RT가 필요할 때 재사용할 수 있습니다.

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

위 그림은 Bloom을 단순화한 흐름입니다. 먼저 카메라 렌더링 결과에서 밝은 영역을 추출해 Temp RT A에 씁니다. 다음 패스가 A를 읽어 다운샘플과 블러를 수행하고 결과를 Temp RT B에 쓰면, 그 시점부터 A는 더 이상 필요하지 않습니다. 따라서 A는 곧바로 `ReleaseTemporary()`로 풀에 반환할 수 있습니다.

풀에 돌아간 RT는 뒤이은 패스가 같은 규격을 요청할 때 다시 사용될 수 있습니다. 여기서 같은 규격이란 해상도, 컬러 포맷, 깊이 버퍼 비트 수, MSAA 설정 같은 주요 조건이 일치한다는 뜻입니다. 이 조건이 하나라도 다르면 기존 RT를 그대로 재사용하기 어렵고, 풀은 다른 RT를 내주거나 새 리소스를 할당해야 합니다.

Temporary RT 풀은 계속 커지기만 하는 구조는 아닙니다. 반환된 RT는 이후 같은 규격 요청이 들어오면 재사용되고, 일정 시간 동안 다시 쓰이지 않으면 Unity가 내부적으로 정리할 수 있습니다. 예를 들어 특정 후처리 효과를 끄면 그 효과가 쓰던 Temporary RT 요청도 사라지고, 풀에 남아 있던 리소스는 더 이상 필요하지 않은 것으로 판단되어 정리 대상이 됩니다.

### CommandBuffer에서의 사용

렌더링 명령을 직접 묶어 실행하고 싶을 때 사용하는 API가 **CommandBuffer**입니다. 스크립트에서 Render Target 설정, Blit, 셰이더 파라미터 설정 같은 명령을 CommandBuffer에 기록해 두면, Unity가 정해진 시점에 그 명령 묶음을 GPU에 제출합니다.

CommandBuffer 안에서도 임시 RT를 요청할 수 있습니다. `cmd.GetTemporaryRT()`는 지정한 규격의 임시 RenderTexture를 만들고, 해당 RT를 셰이더에서 사용할 수 있도록 이름 ID에 연결합니다. 사용이 끝나면 같은 이름 ID로 `cmd.ReleaseTemporaryRT()`를 호출해 반환합니다.

명시적으로 반환하지 않은 임시 RT도 무한히 남지는 않습니다. Unity는 카메라 렌더링이 끝나거나 `Graphics.ExecuteCommandBuffer` 실행이 끝난 뒤 이런 임시 RT를 정리합니다. 그래도 한 CommandBuffer 안에서 더 이상 필요 없는 RT는 `ReleaseTemporaryRT()`로 바로 반환하는 편이 좋습니다. 그래야 같은 프레임의 뒤쪽 명령에서 풀 재사용이 가능하고, 동시에 살아 있는 RT 수를 줄일 수 있습니다.

Unity 6의 Render Graph 기반 URP에서는 이 수동 관리가 더 줄어듭니다. 개발자는 `RecordRenderGraph`에서 패스가 어떤 텍스처를 읽고, 어떤 텍스처를 Render Target으로 쓰는지를 선언합니다. 임시 텍스처는 `TextureHandle`로 표현되고, Render Graph는 패스 전체의 읽기/쓰기 관계를 보고 생성, 재사용, 해제 시점을 결정합니다. 프레임 결과에 쓰이지 않는 텍스처라면 아예 만들지 않는 식의 최적화도 가능합니다. 외부에서 직접 만든 지속 텍스처를 Render Graph 안에서 쓰려면 `RTHandle` 등을 `TextureHandle`로 import해 사용합니다.

Back Buffer, RenderTexture, Temporary RT는 쓰임새와 수명이 다르지만 모두 렌더링 결과를 기록하는 Render Target입니다. 한 프레임 안에서 GPU는 이 대상들 사이를 여러 번 오가며 그립니다. 다음 절에서는 이 Render Target 전환이 왜 비용이 되고, 특히 모바일 GPU에서 왜 더 민감하게 나타나는지 살펴보겠습니다.

---

## Render Target 전환 비용

한 프레임 안에서도 GPU가 결과를 기록하는 대상은 여러 번 바뀔 수 있습니다. 그림자 맵을 그릴 때는 깊이 전용 RT에 쓰고, 메인 카메라를 그릴 때는 컬러 RT에 쓰며, 후처리에서는 Temp RT A의 내용을 읽어 Temp RT B에 씁니다. 이렇게 현재 패스의 출력 대상을 다른 Render Target으로 바꾸는 동작을 **Render Target 전환(Switch)**이라고 합니다.

Render Target 전환은 단순히 변수 하나를 바꾸는 일은 아닙니다. 이전 대상에 쓰던 결과를 이후 패스에서 올바르게 읽을 수 있어야 하고, 새 대상의 기존 내용을 유지할지 버릴지도 정해야 합니다. 데스크톱 GPU에서는 전환이 대체로 비교적 감당 가능한 비용으로 처리되지만, 캐시 정리나 동기화, MSAA resolve 같은 부가 작업이 끼면 여전히 비용이 생길 수 있습니다.

모바일 GPU에서는 이 비용이 더 민감하게 나타납니다. 많은 모바일 GPU가 타일 기반 구조를 사용하기 때문에, Render Target을 바꾸는 순간 칩 안의 타일 메모리에 있던 결과를 외부 메모리에 저장하거나, 다음 대상의 내용을 다시 가져오는 작업이 필요할 수 있습니다.

### 모바일 GPU의 Resolve 비용

[GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)에서 다룬 것처럼, 많은 모바일 GPU는 **TBDR(Tile-Based Deferred Rendering)** 구조를 사용합니다. 화면을 작은 타일로 나누고, 각 타일의 컬러와 깊이 값을 GPU 칩 안의 빠른 **타일 메모리(On-Chip Tile Memory)**에서 처리하는 방식입니다.

타일 메모리는 빠르지만 용량이 작고 한 Render Target의 중간 결과를 오래 보관하는 저장소가 아닙니다. 따라서 현재 Render Target의 결과가 이후에도 필요하다면, 타일 메모리에 있던 내용을 칩 바깥의 시스템 메모리로 내보내야 합니다. 이 저장 과정을 보통 Store 또는 Resolve로 설명합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">TBDR에서 Render Target 전환 비용</text>

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

  <!-- Arrow 1: Store/Resolve -->
  <line x1="230" y1="148" x2="230" y2="200" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="223,194 230,206 237,194" fill="currentColor"/>
  <rect x="244" y="160" width="232" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="none"/>
  <text x="260" y="176" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Store/Resolve (타일 → 시스템 메모리)</text>

  <!-- Box 2: 시스템 메모리 (RT A) -->
  <rect x="130" y="214" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="236" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">시스템 메모리</text>
  <text x="230" y="254" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(Render Target A)</text>
  <!-- Annotation: slow bandwidth -->
  <text x="345" y="243" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">외부 대역폭 소비</text>

  <!-- Arrow 2: Load -->
  <line x1="230" y1="266" x2="230" y2="350" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="223,344 230,356 237,344" fill="currentColor"/>
  <rect x="244" y="298" width="225" height="22" rx="3" fill="currentColor" fill-opacity="0.08" stroke="none"/>
  <text x="260" y="314" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Load (시스템 → 타일 메모리)</text>

  <!-- Box 3: 타일 메모리 (RT B) -->
  <rect x="130" y="364" width="200" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="230" y="386" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">타일 메모리</text>
  <text x="230" y="404" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(Render Target B)</text>
  <!-- Annotation: bandwidth again -->
  <text x="345" y="393" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">외부 대역폭 소비</text>

  <!-- Phase label: RT B rendering start -->
  <text x="260" y="440" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Render Target B에 렌더링 시작</text>

  <!-- Footnote -->
  <text x="260" y="472" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">* Store는 RT A 결과가 이후 필요할 때 수행</text>
  <text x="260" y="488" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">* Load는 RT B의 기존 내용을 보존해야 할 때 수행</text>
</svg>
</div>

<br>

Render Target을 전환할 때 항상 Store와 Load가 모두 발생하는 것은 아닙니다. 이전 Render Target의 결과를 이후 패스에서 다시 읽어야 한다면 Store/Resolve가 필요하고, 다음 Render Target의 기존 내용을 이어서 사용해야 한다면 Load가 필요합니다. 반대로 이전 결과를 버려도 되거나 다음 RT를 화면 전체에 새로 그릴 수 있다면 이 작업을 생략할 수 있습니다.

문제는 Store와 Load가 발생할 때마다 칩 바깥의 시스템 메모리를 오간다는 점입니다. 모바일 기기에서는 CPU와 GPU가 제한된 시스템 메모리 대역폭을 공유하므로, 이런 전송이 쌓이면 프레임 시간이 늘어날 수 있습니다.

전력 비용도 함께 증가합니다. 칩 내부의 타일 메모리에 접근하는 것보다 외부 시스템 메모리에 접근하는 쪽이 훨씬 비싸기 때문에, 불필요한 Render Target 전환은 발열과 배터리 소모로도 이어질 수 있습니다. 그래서 모바일에서는 Render Target 전환 횟수뿐 아니라 각 전환에서 Store와 Load를 정말 해야 하는지도 함께 줄여야 합니다.

### 최소화 전략

가장 먼저 줄여야 하는 것은 전환 횟수입니다. 같은 Render Target에 이어서 그릴 수 있는 작업은 가능한 한 한 구간에 모으고, 중간에 다른 RT로 갔다가 다시 돌아오는 흐름을 피해야 합니다. 렌더 패스 순서를 정리해 출력 대상이 자주 바뀌지 않게 만들면 Store와 Load가 발생할 기회도 함께 줄어듭니다.

예를 들어 메인 컬러 RT에 불투명 오브젝트를 그린 뒤 후처리 RT로 넘어갔다가, 다시 메인 컬러 RT로 돌아와 반투명 오브젝트를 그리면 불필요한 왕복 전환이 생깁니다. 반대로 불투명과 반투명 오브젝트를 메인 컬러 RT에 이어서 그리고, 그다음 후처리 RT로 한 번만 넘어가면 전환 횟수를 줄일 수 있습니다.

### Store/Load Actions

전환 횟수를 줄이는 것이 첫 번째 최적화라면, 두 번째는 전환이 남았을 때 무엇을 보존할지 정확히 정하는 일입니다.
Render Target을 사용하기 전에는 이전 내용을 가져올지 결정하고, 사용이 끝난 뒤에는 결과를 시스템 메모리에 남길지 결정합니다. 이 두 선택이 각각 **Load Action**과 **Store Action**입니다.

TBDR에서는 이 선택이 곧 대역폭 비용으로 이어집니다. `Load`는 시스템 메모리에 있던 Render Target 내용을 타일 메모리로 읽어 오고, `Store`는 타일 메모리의 결과를 다시 시스템 메모리에 기록합니다.
반대로 이전 내용이 필요 없거나 결과를 다시 읽지 않는다면 이 전송을 생략할 수 있습니다.

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
  <text x="120" y="102" font-family="sans-serif" font-size="11" fill="currentColor">타일 결과를 시스템 메모리에 기록</text>
  <text x="120" y="122" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이후 패스나 최종 출력에서 필요할 때</text>

  <!-- DontCare -->
  <rect x="40" y="140" width="440" height="64" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="162" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DontCare</text>
  <text x="120" y="162" font-family="sans-serif" font-size="11" fill="currentColor">결과를 버리고 Store 생략</text>
  <text x="120" y="182" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이후에 다시 읽거나 표시하지 않을 때</text>
  <text x="120" y="196" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 대역폭 절약</text>

  <!-- === Load Action === -->
  <rect x="20" y="230" width="480" height="230" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="254" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Load Action (Render Target 사용 전)</text>

  <!-- Load -->
  <rect x="40" y="268" width="440" height="50" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="288" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Load</text>
  <text x="120" y="288" font-family="sans-serif" font-size="11" fill="currentColor">이전 내용을 타일 메모리로 불러옴</text>
  <text x="120" y="308" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">이전 패스의 결과 위에 추가로 그릴 때</text>

  <!-- Clear -->
  <rect x="40" y="326" width="440" height="64" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="348" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Clear</text>
  <text x="120" y="348" font-family="sans-serif" font-size="11" fill="currentColor">초기화하고 Load 생략</text>
  <text x="120" y="368" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">대상 전체를 새 값으로 다시 채울 때</text>
  <text x="120" y="382" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">→ 대역폭 절약</text>

  <!-- DontCare -->
  <rect x="40" y="398" width="440" height="50" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="56" y="418" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">DontCare</text>
  <text x="120" y="418" font-family="sans-serif" font-size="11" fill="currentColor">이전 내용을 정의하지 않고 Load 생략</text>
  <text x="120" y="438" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">필요한 픽셀을 패스가 모두 덮어쓸 때</text>
</svg>
</div>

Store Action은 Render Target 사용이 끝난 뒤의 처리입니다. 이후 패스에서 이 결과를 샘플링하거나 최종 화면으로 내보내야 한다면 `Store`가 필요합니다.
반대로 이번 패스 안에서만 쓰고 버릴 결과라면 `DontCare`로 둘 수 있습니다. 예를 들어 깊이 테스트에만 사용하고 이후에는 읽지 않는 depth buffer라면, 시스템 메모리에 결과를 저장할 이유가 없습니다.

Load Action은 Render Target 사용이 시작될 때의 처리입니다. 이전 패스의 결과 위에 이어서 그려야 한다면 `Load`가 필요합니다.
하지만 화면 전체를 새 값으로 채울 계획이라면 이전 내용을 읽어 올 필요가 없습니다. 이때는 `Clear`로 시작해 정해진 색이나 깊이 값으로 초기화합니다.
`DontCare`도 Load를 생략하지만, 시작 내용이 정의되지 않습니다. 따라서 패스가 필요한 픽셀을 확실히 모두 덮어쓰는 경우에만 사용해야 합니다.

가장 가벼운 조합은 Load Action을 `Clear` 또는 `DontCare`로, Store Action을 `DontCare`로 두는 경우입니다.
시작할 때 읽지 않고, 끝날 때 저장하지 않으므로 시스템 메모리와의 왕복이 사라집니다. 반대로 `Load`와 `Store`를 함께 사용하면 시작할 때 한 번 읽고 끝날 때 한 번 기록하므로 비용이 가장 큽니다.

MSAA가 켜진 Render Target은 Store 단계에서 한 가지를 더 고려해야 합니다. 픽셀마다 여러 샘플로 저장된 값을 단일 샘플 결과로 합치는 **MSAA Resolve**가 필요할 수 있기 때문입니다.
이후 패스나 최종 출력이 resolve된 색을 필요로 한다면 저장 또는 Resolve 동작이 필요해집니다. 반대로 결과가 더 이상 필요 없다면 `DontCare`로 버려 저장과 Resolve 비용을 함께 피할 수 있습니다.
따라서 MSAA가 적용된 중간 RT일수록 "정말 저장해야 하는가"를 더 엄격하게 봐야 합니다.

깊이/스텐실 버퍼처럼 한 프레임 안에서만 쓰고 나중에 읽지 않는 버퍼라면 **memoryless** 설정도 선택지가 됩니다.
`RenderTexture.memorylessMode`를 사용하면 지원 플랫폼에서 해당 버퍼가 타일 메모리에만 머물고 시스템 메모리 사본을 만들지 않습니다. 그만큼 메모리 사용량과 대역폭을 줄일 수 있지만, 나중에 내용을 읽거나 보존할 수는 없습니다.
따라서 샘플링, `ReadPixels`, 다음 패스 재사용이 필요한 Render Target에는 맞지 않습니다.

수동 렌더 패스가 많아지면 어느 RT를 저장하고 어느 RT를 버려도 되는지 사람이 직접 추적하기 어렵습니다.
Unity 6 이상의 URP에서 사용하는 **Render Graph**는 각 패스가 어떤 텍스처를 읽고 쓰는지 그래프로 선언하게 하고, 그 의존성을 바탕으로 임시 RT의 수명과 Store/Load Action을 정합니다.
다만 그래프가 올바른 결정을 하려면 각 패스의 읽기와 쓰기 관계를 정확히 선언해야 합니다.

정리하면 Store/Load Actions는 Render Target 전환 자체를 없애는 기능이 아니라, 전환이 남았을 때 불필요한 메모리 왕복을 줄이는 설정입니다.
이 Render Target을 나중에 읽을 것인가, 이전 내용을 이어서 쓸 것인가, 이번 패스가 필요한 영역을 모두 덮어쓸 것인가를 기준으로 선택하면 됩니다. 여기까지가 대역폭을 줄이는 쪽의 최적화라면, 다음 Dynamic Resolution은 처리할 픽셀 수 자체를 줄이는 접근입니다.

---

## Dynamic Resolution

앞 절까지는 같은 해상도에서 Render Target 전환과 대역폭을 줄이는 방법을 보았습니다. **Dynamic Resolution**은 한 단계 더 직접적으로, GPU가 처리해야 할 픽셀 수 자체를 줄이는 방법입니다.

핵심은 최종 디스플레이 해상도를 바꾸는 것이 아니라, 카메라가 그리는 내부 Render Target의 해상도를 상황에 따라 낮추는 데 있습니다. GPU 시간이 목표 프레임 예산을 넘으면 렌더링 스케일을 낮추고, 여유가 생기면 다시 올립니다. 마지막에는 낮은 해상도로 그린 결과를 화면 해상도에 맞게 업스케일합니다.

해상도를 낮추면 절감 효과는 면적으로 나타납니다. 가로와 세로를 모두 80%로 줄이면 처리해야 할 픽셀은 `0.8 x 0.8 = 0.64`, 즉 원래의 약 64%가 됩니다. 70%라면 약 49%까지 줄어듭니다. 픽셀 수가 줄어들면 래스터화 단계에서 만들어지는 프래그먼트 수, 프래그먼트 셰이더 실행 횟수, Render Target에 쓰는 데이터량도 함께 줄어듭니다.

따라서 Dynamic Resolution은 프래그먼트 셰이더 연산이나 메모리 대역폭이 병목인 **GPU Bound** 상황에서 효과가 큽니다. 특히 모바일 GPU는 CPU와 시스템 메모리를 공유하므로 대역폭 여유가 적어, 픽셀 수를 줄였을 때 얻는 이득이 분명하게 나타날 수 있습니다. 반대로 CPU가 드로우콜을 준비하거나 게임 로직을 처리하느라 늦는 상황에서는 해상도를 낮춰도 병목이 풀리지 않습니다.

<br>

### 설정 방법

URP에서 Dynamic Resolution을 쓰려면 먼저 대상 카메라가 동적 해상도 조절을 허용해야 합니다. Camera 컴포넌트의 **Allow Dynamic Resolution**을 켜면, 그 카메라가 사용하는 동적 스케일 대상 Render Target이 `ScalableBufferManager`의 제어를 받습니다.

URP Asset의 Quality 섹션에서는 이 결과를 어떻게 보정할지 정합니다. **Render Scale**은 고정 렌더링 스케일이고, **Upscaling Filter**는 낮은 해상도로 그린 결과를 화면 크기로 늘릴 때 사용할 필터입니다. Dynamic Resolution은 이 값을 매 프레임 직접 바꾸는 방식이 아니라, 동적으로 스케일 가능한 Render Target을 따로 표시해 두고 런타임에서 그 스케일만 조절하는 구조입니다.

실제 스케일 변경은 스크립트에서 `ScalableBufferManager.ResizeBuffers(widthScale, heightScale)`를 호출해 수행합니다. 두 인자는 가로와 세로 스케일이며, `1.0f`가 원본 해상도입니다. Unity 6 기준으로 실제 적용값은 지원 가능한 단계에 맞춰 보정될 수 있으므로, 필요하다면 `ScalableBufferManager.widthScaleFactor`와 `heightScaleFactor`로 현재 적용된 값을 확인합니다.

보통은 `FrameTimingManager` 같은 측정값을 바탕으로 이전 프레임의 CPU/GPU 시간을 확인한 뒤, GPU 시간이 목표 프레임 예산을 넘으면 스케일을 낮추고 여유가 생기면 다시 올립니다. `FrameTimingManager`를 사용하려면 Player Settings의 **Enable Frame Timing Stats**도 켜 두어야 합니다.
이때 스케일을 매 프레임 크게 흔들면 화면 선명도가 눈에 띄게 출렁일 수 있으므로, 최소/최대 스케일과 복원 조건을 정해 두고 단계적으로 조절하는 편이 안정적입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 500 470" xmlns="http://www.w3.org/2000/svg" style="max-width: 500px; width: 100%;">
  <!-- Title -->
  <text x="250" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Dynamic Resolution 적용 흐름</text>

  <!-- Label: 매 프레임 -->
  <text x="250" y="48" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">매 프레임</text>

  <!-- Step 1: GPU 시간 측정 -->
  <rect x="100" y="58" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="81" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1) 이전 프레임의 CPU/GPU 시간 확인</text>

  <!-- Arrow -->
  <line x1="250" y1="94" x2="250" y2="116" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="243,110 250,122 257,110" fill="currentColor"/>

  <!-- Step 2: 목표 비교 -->
  <rect x="100" y="124" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="147" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(2) GPU 시간을 목표 예산과 비교</text>

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
  <text x="130" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 내부 RT 스케일 낮춤</text>

  <!-- Right branch: GPU 시간 안정 -->
  <rect x="270" y="208" width="200" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="370" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU 시간 안정</text>
  <text x="370" y="248" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">ResizeBuffers(1.0f, 1.0f)</text>
  <text x="370" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">→ 단계적으로 복원</text>

  <!-- Merge arrows -->
  <line x1="130" y1="288" x2="130" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <line x1="370" y1="288" x2="370" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <line x1="130" y1="320" x2="370" y2="320" stroke="currentColor" stroke-width="1.5"/>
  <line x1="250" y1="320" x2="250" y2="340" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="243,334 250,346 257,334" fill="currentColor"/>

  <!-- Step 3: 렌더링 실행 -->
  <rect x="100" y="348" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="371" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(3) 조절된 내부 RT 크기로 렌더링</text>

  <!-- Arrow -->
  <line x1="250" y1="384" x2="250" y2="406" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="243,400 250,412 257,400" fill="currentColor"/>

  <!-- Step 4: 업스케일 -->
  <rect x="100" y="414" width="300" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="250" y="437" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(4) Upscaling Filter로 화면 크기 복원</text>
</svg>
</div>

<br>

해상도를 낮춰 렌더링하면 마지막에는 원본보다 적은 픽셀로 만든 이미지를 화면 크기까지 늘려야 합니다. 이 업스케일링 과정에서는 존재하지 않던 픽셀을 주변 값으로 보간해야 하므로, 필터 선택에 따라 선명도 차이가 납니다.
단순 바이리니어(Bilinear) 필터링은 인접한 4개 픽셀의 가중 평균으로 사이값을 채우기 때문에 빠르지만 흐려 보이기 쉽습니다. **AMD FSR(FidelityFX Super Resolution)** 같은 업스케일러는 에지 보정과 샤프닝을 더해 낮은 스케일에서도 선명도를 유지하려고 합니다.

마지막으로 플랫폼 지원도 확인해야 합니다. Dynamic Resolution은 모든 그래픽스 API에서 동일하게 동작하지 않습니다. 모바일이라면 iOS의 Metal, Android의 Vulkan처럼 Unity가 Dynamic Resolution을 지원하는 조합인지 먼저 확인해야 합니다.

### UI와 Dynamic Resolution

Dynamic Resolution을 적용할 때 가장 먼저 분리해야 할 대상은 UI입니다.
3D 장면은 해상도가 조금 내려가도 카메라 움직임, 조명, 후처리 때문에 흐려짐이 덜 눈에 띌 수 있습니다. 반면 텍스트, 아이콘, 얇은 선은 픽셀 경계가 분명해야 하므로 낮은 해상도로 렌더링한 뒤 업스케일하면 바로 흐릿해 보입니다.

가장 단순한 방법은 Canvas를 **Screen Space - Overlay**로 두는 것입니다. 이 모드의 UI는 화면 공간에 직접 그려지므로, 3D 카메라의 내부 Render Target 스케일이 내려가도 UI는 최종 화면 해상도 기준으로 유지됩니다.

UI를 카메라 흐름 안에서 그려야 한다면 별도 UI 카메라를 두고, 그 카메라의 **Allow Dynamic Resolution**을 꺼 둡니다. URP Camera Stacking을 사용한다면 3D 장면을 그리는 Base Camera에는 Dynamic Resolution을 적용하고, UI를 올리는 Overlay Camera는 원본 해상도로 남겨 두는 식입니다. 반대로 UI가 동적 스케일이 적용된 같은 카메라 출력에 함께 들어가면, UI도 3D 장면과 같이 낮은 해상도로 그려진 뒤 확대되어 선명도가 떨어질 수 있습니다.

정리하면 Dynamic Resolution은 처리할 픽셀 수를 줄이는 최적화입니다. 다음으로 볼 컬러 포맷은 픽셀 하나가 몇 바이트를 차지하는지를 정해, 같은 해상도에서도 Render Target의 메모리와 대역폭을 바꾸는 설정입니다.

---

## 컬러 포맷과 메모리

Dynamic Resolution이 픽셀 수를 줄이는 설정이라면, 컬러 포맷은 픽셀 하나가 얼마나 많은 데이터를 갖는지를 정하는 설정입니다.
Render Target의 메모리는 `가로 해상도 x 세로 해상도 x 픽셀당 바이트 수`로 계산되므로, 같은 해상도라도 포맷이 커지면 메모리 사용량이 그대로 늘어납니다.

포맷은 색을 몇 개의 채널로 나누어 저장할지, 각 채널에 몇 비트를 줄지, 값을 정수로 해석할지 부동소수점으로 해석할지를 정합니다. 이 선택은 색 표현 범위와 정밀도를 바꾸는 동시에, GPU가 Render Target을 읽고 쓸 때 소비하는 대역폭도 바꿉니다.

### LDR 포맷

LDR(Low Dynamic Range)은 채널 값을 보통 0.0~1.0 범위 안에서 저장하는 포맷입니다. 후처리까지 끝난 최종 색이나, HDR 밝기 정보가 필요 없는 중간 버퍼에 주로 사용합니다.

대표적인 포맷은 **R8G8B8A8_UNorm**입니다. R, G, B, A 네 채널에 각각 8비트를 배정하므로 픽셀 하나가 **4바이트**를 사용합니다.
`UNorm`은 Unsigned Normalized의 줄임말입니다. 저장 자체는 0~255의 부호 없는 정수로 하지만, 셰이더에서 읽을 때는 0.0~1.0 범위의 값으로 정규화해 해석합니다.

화면에 바로 내보내는 컬러 버퍼나 UI처럼 HDR이 필요 없는 대상이라면 이 계열의 포맷이 기본 선택지가 됩니다. 표현 범위는 제한적이지만, 메모리와 대역폭 사용량이 낮고 대부분의 플랫폼에서 다루기 쉽습니다.

### HDR 포맷

HDR(High Dynamic Range)은 1.0을 넘어서는 밝기 값을 보존해야 할 때 사용합니다.
LDR 포맷에 태양광, 폭발, 강한 발광 머티리얼처럼 1.0보다 큰 값을 저장하면 값이 1.0으로 잘려 밝은 영역의 차이가 사라집니다. Bloom이나 톤 매핑은 이 초과 밝기 정보를 바탕으로 동작하므로, 후처리 전에 사용하는 컬러 버퍼는 HDR 포맷이어야 합니다.

가장 단순한 HDR 선택지는 **R16G16B16A16_SFloat**입니다. 네 채널에 각각 16비트 부동소수점을 저장하므로 픽셀 하나가 **8바이트**를 사용합니다.
알파까지 포함해 넉넉한 정밀도를 제공하지만, R8G8B8A8 계열보다 메모리와 대역폭을 두 배로 씁니다.

모바일에서는 이 비용이 부담스러울 수 있어 **R11G11B10_UFloat** 계열을 자주 검토합니다. 이 포맷은 R과 G에 11비트, B에 10비트를 사용하고 알파 채널은 저장하지 않습니다.
픽셀당 **4바이트**만 사용하면서도 부동소수점 기반 HDR 값을 담을 수 있으므로, 알파가 필요 없는 메인 컬러 버퍼에서는 메모리 효율이 좋습니다.

대신 정밀도는 R16G16B16A16_SFloat보다 낮고, 알파 채널도 없습니다. 어두운 영역의 미세한 밝기 차이나 부드러운 그라데이션에서 밴딩(Banding)이 보일 수 있습니다.
그래도 HDR 컬러 버퍼가 필요하고 알파를 쓰지 않는다면, R11G11B10 계열은 메모리와 대역폭을 줄이는 현실적인 선택입니다. 밴딩이 눈에 띄는 경우에는 디더링(Dithering)이나 톤 매핑 설정으로 완화할 수 있습니다.

<br>

**컬러 포맷 비교**

| 포맷 | 픽셀당 바이트 | 특징 | 주 용도 |
|------|------|------|------|
| R8G8B8A8_UNorm | 4 | LDR, 알파 포함 | 최종 색, UI, 일반 컬러 버퍼 |
| R16G16B16A16_SFloat | 8 | HDR, 알파 포함, 높은 정밀도 | 고품질 HDR 컬러 버퍼 |
| R11G11B10_UFloat | 4 | HDR, 알파 없음 | 모바일 HDR 컬러 버퍼 |
| B10G11R11_UFloat | 4 | HDR, 알파 없음 | 플랫폼별 대체 표기 |

<br>

R11G11B10_UFloat와 B10G11R11_UFloat는 같은 32비트 HDR 계열로 보면 됩니다. API나 플랫폼에 따라 채널 순서가 반대로 표기될 수 있으므로, 실제 프로젝트에서는 `SystemInfo.GetGraphicsFormat(DefaultFormat.HDR)`나 URP가 선택한 기본 HDR 포맷을 함께 확인하는 편이 좋습니다.

### Depth 포맷

컬러 버퍼가 픽셀의 색을 남긴다면, 깊이 버퍼는 픽셀마다 카메라에서 가장 가까운 표면의 깊이를 남깁니다.
GPU는 새 프래그먼트를 그리기 전에 이 값과 자신의 깊이를 비교합니다. 이미 더 가까운 표면이 기록되어 있다면 뒤쪽 프래그먼트는 버려지고, 더 가까운 프래그먼트만 통과합니다. 이 과정이 **Depth Test**입니다.

깊이 포맷을 고를 때 보는 기준은 두 가지입니다. 하나는 깊이 정밀도이고, 다른 하나는 스텐실이 필요한지입니다.
깊이 비트가 많을수록 가까운 두 표면을 더 안정적으로 구분할 수 있지만, 픽셀당 바이트 수가 커져 메모리와 대역폭도 늘어납니다. 스텐실을 쓰는 효과가 있다면 깊이 값만 있는 포맷이 아니라 깊이와 스텐실을 함께 담는 Depth/Stencil 포맷을 선택해야 합니다.

<br>

**Depth 포맷 비교**

| 포맷 | 픽셀당 바이트 | 구성 | 선택 기준 |
|------|------|------|------|
| D16 | 2 | 16비트 깊이 | 정밀도보다 메모리가 중요할 때 |
| D24S8 | 4 | 24비트 깊이 + 8비트 스텐실 | 깊이와 스텐실이 모두 필요한 일반적인 경우 |
| D32_SFloat | 4 | 32비트 부동소수점 깊이 | 스텐실 없이 깊이 정밀도를 높일 때 |
| D32_SFloat_S8 | 8 | 32비트 깊이 + 8비트 스텐실 | 높은 깊이 정밀도와 스텐실이 모두 필요할 때 |

<br>

D16은 가장 가볍습니다. 픽셀당 2바이트라 depth buffer 비용을 크게 줄일 수 있지만, 깊이를 16비트로만 나누기 때문에 정밀도가 낮습니다.
가까운 두 표면의 깊이를 충분히 구분하지 못하면 어느 쪽이 앞인지가 프레임마다 흔들리고, 화면에는 **Z-fighting**처럼 깜빡이는 현상으로 나타납니다. [Unity 렌더링 (1)](/dev/unity/UnityRendering-1/)에서 다루었듯 Near/Far 비율이 커질수록 깊이 정밀도는 더 빠르게 부족해지므로, 넓은 3D 공간이나 먼 거리까지 보는 카메라에서는 D16을 조심해서 써야 합니다.

D24S8은 깊이 24비트와 스텐실 8비트를 4바이트 안에 함께 담습니다.
스텐실은 아웃라인, 포탈, 마스킹처럼 픽셀 단위로 영역을 표시하거나 제외할 때 사용합니다. 깊이 테스트도 필요하고 스텐실도 필요한 일반적인 렌더링에서는 D24S8이 기능과 메모리의 균형이 좋습니다.

D32_SFloat는 32비트 부동소수점 깊이만 저장합니다. 스텐실이 필요 없고 깊이 정밀도를 더 확보해야 할 때 선택합니다.
깊이 정밀도와 스텐실이 모두 필요하면 D32_SFloat_S8을 사용할 수 있지만, 이 포맷은 32비트 깊이와 8비트 스텐실 외에 사용되지 않는 비트까지 포함해 64비트 계열로 다뤄질 수 있습니다. 그래서 픽셀당 8바이트, D24S8의 두 배 비용이 듭니다.

1080p 기준으로 D32_SFloat_S8 깊이/스텐실 버퍼 하나만 약 15.8MB를 차지합니다. 모바일에서는 이 차이가 메모리와 대역폭 모두에 부담이 되므로, 특별히 높은 깊이 정밀도가 필요한 장면이 아니라면 D24S8을 먼저 기준으로 잡는 편이 현실적입니다.

### 해상도별 메모리 계산 예시

Render Target 메모리는 결국 픽셀 수와 픽셀당 바이트 수의 곱입니다. 같은 포맷이라도 해상도가 올라가면 픽셀 수만큼 커지고, 같은 해상도라도 포맷이 무거우면 그만큼 더 많은 메모리를 차지합니다.

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

모바일에서는 먼저 "필요한 표현을 만족하는 가장 가벼운 포맷"을 기준으로 잡는 편이 좋습니다. 해상도는 Dynamic Resolution으로 낮출 수 있지만, 포맷이 무거우면 픽셀 하나를 읽고 쓰는 비용이 계속 커지기 때문입니다.

컬러 버퍼는 HDR이 필요 없는 대상이라면 R8G8B8A8_UNorm 계열로 충분합니다. HDR이 필요하더라도 알파를 저장하지 않는 메인 컬러 버퍼라면 R11G11B10_UFloat 계열을 먼저 검토합니다. R16G16B16A16_SFloat는 정밀도와 알파가 필요할 때 선택할 수 있지만, 4바이트 포맷보다 메모리와 대역폭을 두 배로 씁니다.

깊이 버퍼는 스텐실 사용 여부를 먼저 봅니다. 스텐실이 필요하다면 D24S8이 모바일에서 가장 무난한 기준점입니다. 스텐실이 필요 없고 깊이 정밀도를 더 확보해야 한다면 D32_SFloat를 검토할 수 있습니다. D32_SFloat_S8은 정밀도와 스텐실을 모두 제공하지만 비용이 크므로, 모바일에서는 특별한 이유가 있을 때만 선택하는 편이 좋습니다.

다만 포맷 선택은 표만 보고 끝내면 안 됩니다. 실제 기기에서 지원하지 않는 포맷은 Unity가 다른 포맷으로 대체할 수 있고, 렌더 파이프라인 설정에 따라 최종 포맷이 달라질 수 있습니다. 따라서 Frame Debugger나 프로파일러로 실제 생성된 Render Target의 포맷과 메모리를 확인해야 합니다.

<br>

---

## Render Target 메모리 총합 관리

포맷 하나를 가볍게 고르는 것만으로는 충분하지 않습니다. 실제 프레임에서는 메인 컬러 RT와 깊이 RT만 쓰이는 것이 아니라, 그림자 맵, 후처리 중간 RT, 임시 RT, 경우에 따라 G-Buffer까지 함께 등장합니다.
개별 RT는 몇 MB 수준이어도, 한 프레임 안에서 동시에 살아 있거나 순차적으로 필요한 RT가 많아지면 전체 GPU 메모리와 대역폭 부담은 빠르게 커집니다.

따라서 Render Target 메모리는 "RT 하나의 크기"가 아니라 "프레임 전체에서 필요한 RT 묶음"으로 봐야 합니다. Render Graph나 Temporary RT 풀이 수명이 겹치지 않는 버퍼를 재사용할 수는 있지만, 어떤 RT들이 필요한지 먼저 계산해 두어야 예산을 잡을 수 있습니다.

<br>

**한 프레임의 Render Target 메모리 예시**  
(URP Forward 계열, Full HD, HDR, 단순 계산)

| Render Target | 포맷 | 메모리 |
|------|------|------|
| 메인 컬러 RT | R11G11B10 | 7.9 MB |
| 메인 깊이 RT | D24S8 | 7.9 MB |
| Shadow Map (2048x2048) | D16 | 8.0 MB |
| Bloom 다운샘플 체인 | R11G11B10 | ~3.0 MB (합산) |
| 후처리 Temp RT | R11G11B10 | 7.9 MB |
| **합계** | | **≈ 34.7 MB** |

<br>

이 합계는 실제 점유량의 절대값이라기보다 규모를 가늠하기 위한 계산입니다. 후처리 체인의 임시 RT처럼 수명이 짧은 버퍼는 풀이나 Render Graph가 재사용할 수 있고, 반대로 설정에 따라 추가 RT가 더 붙을 수도 있습니다. 중요한 점은 Full HD 기준 4바이트 포맷 RT 한 장만으로도 약 7.9MB가 든다는 사실입니다.

Deferred 렌더링을 사용하면 여기서 RT 수가 더 늘어납니다. **G-Buffer(Geometry Buffer)**는 Deferred 렌더링이 사용하는 다중 RT 묶음으로, 픽셀마다 색상, 법선, 재질 같은 표면 정보를 여러 RT에 먼저 저장해 두고 조명 계산을 뒤에서 한꺼번에 처리합니다.

예를 들어 4바이트 포맷의 Full HD G-Buffer 4장을 사용한다고 보면 다음 정도의 메모리가 추가됩니다. 실제 구성과 포맷은 URP/HDRP 버전, 렌더링 경로, Rendering Layers, ShadowMask, Native Render Pass 같은 설정에 따라 달라질 수 있습니다.

| G-Buffer | 포맷 | 메모리 |
|------|------|------|
| G-Buffer 0 (BaseColor 등) | RGBA32 계열 | 7.9 MB |
| G-Buffer 1 (Normal 등) | RGBA32 계열 | 7.9 MB |
| G-Buffer 2 (Material 등) | RGBA32 계열 | 7.9 MB |
| G-Buffer 3 (Lighting 등) | RGBA32 계열 | 7.9 MB |

<br>

이 경우 G-Buffer만 약 32MB가 추가됩니다. 여기에 메인 컬러, 깊이, 그림자, 후처리 RT가 더해지면 프레임 전체의 Render Target 메모리는 단일 RT를 볼 때보다 훨씬 커집니다.

모바일에서 Deferred를 조심해야 하는 이유도 여기에 있습니다. 문제는 메모리만이 아닙니다. [GPU 아키텍처 (2)](/dev/unity/GPUArchitecture-2/)에서 다룬 것처럼 모바일 GPU(TBDR)는 타일 안에서 그린 결과를 필요할 때 시스템 메모리로 Store하고, 다음 패스에서 다시 Load합니다.
G-Buffer 여러 장을 모두 저장한 뒤 조명 패스에서 다시 읽으면, 각 RT의 메모리 사용량뿐 아니라 Store/Load 대역폭도 함께 증가합니다. 그래서 모바일에서는 RT 개수, 포맷, 해상도, 렌더링 경로를 한 묶음으로 보고 결정해야 합니다.

### Shadow Map의 메모리

앞서 RT 메모리 예시에서 나온 그림자 맵(Shadow Map)도 Render Target입니다.
카메라가 씬을 그리기 전에, Unity는 빛의 시점에서 그림자를 만드는 오브젝트를 한 번 더 렌더링합니다. 이때 필요한 것은 색이 아니라 빛에서 표면까지의 깊이이므로, 결과는 depth texture 형태의 shadow map에 저장됩니다.

이후 메인 카메라 렌더링에서는 현재 픽셀이 빛에서 보이는 깊이보다 뒤에 있는지를 비교해 그림자 여부를 판단합니다. 구조상 shadow map은 화면에 직접 보이지 않지만, 매 프레임 생성되는 Render Target이므로 메모리와 렌더링 비용에 포함해야 합니다.

메모리는 다른 RT와 같은 방식으로 계산합니다. 2048x2048 shadow map을 D16 포맷으로 만들면 `2048 x 2048 x 2바이트`, 즉 약 8MB가 필요합니다.
해상도를 4096으로 올리면 가로와 세로가 각각 두 배가 되므로 픽셀 수는 네 배가 되고, 메모리도 약 32MB까지 늘어납니다. [조명과 그림자 (2)](/dev/unity/LightingAndShadows-2/)에서 설명했듯 그림자 품질을 올리려고 해상도를 높이면 그만큼 RT 메모리도 함께 커집니다.

여기서 주의할 대상이 **캐스케이드 그림자(Cascaded Shadow Map)**입니다. 캐스케이드는 카메라가 보는 거리를 여러 구간으로 나누고, 각 구간에 별도의 directional light shadow map을 배정하는 방식입니다.
가까운 구간은 화면에서 크게 보이므로 더 촘촘한 그림자가 필요하고, 먼 구간은 상대적으로 낮은 정밀도로도 티가 덜 납니다. 캐스케이드는 같은 shadow atlas 안에서 이 정밀도를 거리별로 나누어 쓰게 해 줍니다.

다만 캐스케이드 수가 곧바로 "해상도 x 캐스케이드 수"만큼 메모리를 늘린다는 뜻은 아닙니다. URP는 directional light shadow map들을 하나의 shadow atlas에 배치하고, atlas 크기는 URP Asset의 Main Light Shadow Resolution이 정합니다.
캐스케이드 수를 늘리면 atlas 안에 들어가야 하는 shadow map 수가 늘어나므로 각 캐스케이드가 차지하는 영역, shadow 품질, 그림자 렌더링 드로우 비용에 영향을 줍니다. 같은 품질을 유지하려고 atlas 해상도를 함께 올리면 그때 메모리가 크게 증가합니다.

따라서 모바일에서는 두 값을 함께 봐야 합니다. 캐스케이드 수를 줄이면 그림자 렌더링 횟수와 atlas 압박을 줄일 수 있고, shadow atlas 해상도를 낮추면 메모리와 대역폭을 직접 줄일 수 있습니다. 그림자 품질이 부족하다면 무작정 해상도를 올리기보다 Shadow Distance, Cascade Count, Cascade Split을 함께 조정하는 편이 더 효율적입니다.

### Frame Debugger로 RT 확인

앞에서 계산한 RT 메모리는 예산을 잡기 위한 추정값입니다. 실제 프레임에서 어떤 RT가 만들어지고, 어느 패스가 그 RT를 읽고 쓰는지는 도구로 확인해야 합니다.
Unity의 **Frame Debugger**(Window > Analysis > Frame Debugger)를 켜면 한 프레임이 어떤 렌더링 이벤트로 구성되는지 단계별로 볼 수 있습니다.

Frame Debugger에서 특히 봐야 할 것은 렌더 패스별 Render Target입니다. 어느 드로우콜이 어떤 RT에 쓰는지, RT의 해상도와 포맷이 무엇인지, 한 프레임 안에서 Render Target 전환이 몇 번 일어나는지를 따라가면 앞에서 계산한 메모리와 대역폭 비용이 어디서 생기는지 확인할 수 있습니다.

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
  <text x="24" y="94" font-family="sans-serif" font-size="10" fill="currentColor">(2) RT 해상도와 포맷</text>
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
  <text x="298" y="112" font-family="sans-serif" font-size="10" fill="currentColor">- Store/Load Action 낭비</text>
  <text x="298" y="130" font-family="sans-serif" font-size="10" fill="currentColor">- 불필요한 임시 RT 생성</text>
</svg>
</div>

<br>

다만 Frame Debugger는 렌더링 흐름을 따라가는 도구이지, 프로젝트의 전체 GPU 메모리 사용량을 완전히 집계해 주는 도구는 아닙니다.
RT의 해상도와 포맷은 Frame Debugger에서 확인하고, 실제 메모리 점유량은 프로파일러의 Memory 모듈과 함께 봐야 합니다. Render Target은 런타임에 만들어지는 버퍼라 프로젝트 에셋 목록만 봐서는 드러나지 않습니다.

모바일에서는 텍스처 메모리와 RT 메모리를 따로 관리하면 실제 예산을 놓치기 쉽습니다. 둘 다 같은 GPU 메모리와 시스템 메모리 대역폭을 압박하므로, 최종적으로는 한 프레임의 RT 묶음과 로드된 에셋 메모리를 합쳐 전체 예산 안에 들어오는지 확인해야 합니다.

---

## 마무리

이번 글에서는 GPU가 렌더링 결과를 어디에 기록하는지, 그리고 그 Render Target들이 메모리와 대역폭 비용을 어떻게 만드는지 살펴보았습니다. 핵심은 다음과 같습니다.

- **Back Buffer**는 화면에 표시될 다음 프레임을 그려 넣는 기본 Render Target입니다. Double Buffering이 읽는 버퍼와 그리는 버퍼를 분리해 Tearing을 막고, Swap 시점은 VSync가 맞춥니다.
- **RenderTexture**는 GPU가 그린 결과를 텍스처 형태로 담는 Render Target으로, 미니맵이나 거울, 후처리 입력에 사용합니다. 직접 생성한 RenderTexture는 더 사용하지 않을 때 `Release()`로 GPU 메모리를 해제해야 합니다.
- **Temporary RT**는 풀에서 빌려 쓰는 임시 RenderTexture입니다. 한 프레임 안에서 잠깐 쓰는 중간 버퍼를 매번 할당하지 않고 재사용하며, 더 읽지 않는 RT는 바로 풀에 반환합니다.
- **Render Target 전환**은 모바일 GPU(TBDR)에서 타일 메모리의 내용이 시스템 메모리를 오가는 Store/Load로 이어질 수 있습니다. 전환 횟수를 먼저 줄이고, 남은 전환에는 Store/Load Action으로 보존할 내용만 지정해야 대역폭을 아낄 수 있습니다.
- **Dynamic Resolution**은 GPU Bound일 때 내부 Render Target의 해상도를 낮춰, 처리할 픽셀 수를 줄입니다. 픽셀 경계가 또렷해야 하는 UI는 적용 대상에서 제외합니다.
- **컬러 포맷**은 HDR이 필요 없으면 R8G8B8A8_UNorm, HDR이 필요하고 알파를 쓰지 않으면 R11G11B10_UFloat가 모바일 기준이 됩니다. 깊이 버퍼는 스텐실이 필요한 일반적인 경우 D24S8을 기준으로 잡습니다.
- **RT 메모리**는 메인 컬러와 깊이만이 아니라 Shadow Map, 후처리 Temp RT, 경우에 따라 G-Buffer까지 한 프레임 단위로 합산해서 봐야 합니다. 실제 포맷과 점유량은 Frame Debugger와 프로파일러로 확인합니다.

<br>

정리하면, Render Target 비용은 두 축으로 정해집니다. 메모리는 해상도와 포맷, 한 프레임에 필요한 RT 수가 정하고, 대역폭은 전환 횟수와 Store/Load Action이 정합니다. Full HD 기준 4바이트 포맷 RT 한 장이 약 7.9MB이므로, 모바일에서는 두 축을 함께 관리해야 GPU 메모리와 대역폭 예산을 지킬 수 있습니다.

<br>

렌더링 결과가 담길 버퍼가 정해져도, 그 버퍼에 무엇을 어떤 순서로 그릴지는 렌더 파이프라인이 결정합니다. 이어지는 [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)에서는 렌더 파이프라인이 어떤 종류로 나뉘고 무엇을 기준으로 선택하는지 살펴봅니다.

<br>

---

**관련 글**
- [래스터화 파이프라인 (2) - 출력 병합](/dev/unity/RasterPipeline-2/)
- [래스터화 파이프라인 (3)](/dev/unity/RasterPipeline-3/)
- [GPU 아키텍처 (2) - 모바일 GPU와 TBDR](/dev/unity/GPUArchitecture-2/)
- [조명과 그림자 (2)](/dev/unity/LightingAndShadows-2/)

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
- **Unity 렌더링 (2) - Render Target과 Frame Buffer** (현재 글)
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
