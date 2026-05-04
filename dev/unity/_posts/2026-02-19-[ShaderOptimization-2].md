---
layout: single
title: "셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리 - soo:bak"
date: "2026-02-19 21:35:00 +0900"
description: 셰이더 배리언트 폭증, 키워드 관리, 스트리핑, Shader Graph 고려사항을 설명합니다.
tags:
  - Unity
  - 최적화
  - 셰이더
  - 배리언트
---

## 개별 셰이더에서 프로젝트 전체로

[셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)에서는 셰이더가 한 프래그먼트를 처리할 때 드는 비용을 살펴보았습니다. ALU 연산, 텍스처 샘플링, 정밀도 선택은 모두 셰이더 실행 시간에 직접 영향을 줍니다.

Unity는 하나의 셰이더 소스를 그대로 한 번만 컴파일하지 않습니다.
키워드, 라이트 설정, 렌더링 옵션의 조합에 따라 같은 셰이더를 여러 버전으로 컴파일하며, 이렇게 만들어지는 개별 버전을 **셰이더 배리언트(Shader Variant)**라고 부릅니다.

배리언트 수가 많아지면 런타임 셰이더 연산과는 다른 문제가 생깁니다. 빌드 시간이 길어지고, 포함해야 할 셰이더 바이너리가 늘어나며, 로딩 시간과 메모리 사용량도 증가합니다.
이번 글에서는 이 배리언트가 왜 늘어나는지, 그리고 프로젝트에서 어떻게 줄일 수 있는지를 살펴봅니다.

<br>

---

## 셰이더 배리언트란

셰이더 배리언트는 같은 셰이더 소스에서 조건이 다른 실행 버전을 미리 만들어 둔 것입니다.
예를 들어 포그를 켠 버전과 끈 버전, 노멀 맵을 사용하는 버전과 사용하지 않는 버전이 서로 다른 배리언트가 될 수 있습니다.

### 조건부 기능과 키워드

셰이더에는 포그(Fog), 노멀 맵, 그림자, 라이트맵처럼 상황에 따라 켜고 끄는 기능이 많습니다.
이런 기능을 셰이더 안에서 `if`문으로 처리하면 런타임 분기가 발생하고, GPU의 SIMD 실행 구조에서는 비효율적인 흐름이 생길 수 있습니다.

> GPU의 SIMD 실행 구조는 [GPU 아키텍처 (1) - GPU 병렬 처리와 렌더링 파이프라인](/dev/unity/GPUArchitecture-1/)에서, 런타임 분기가 일으키는 분기 발산과 그 비용은 [셰이더 최적화 (1)](/dev/unity/ShaderOptimization-1/)에서 자세히 다룹니다.

Unity는 이런 조건을 **컴파일 타임 분기**로 처리할 수 있게 합니다.
조건부 기능마다 키워드(keyword)를 정의하고, 키워드 조합별로 별도의 셰이더 프로그램을 미리 컴파일하는 방식입니다.

이렇게 미리 만들어진 셰이더 프로그램 중에서, 런타임에는 머티리얼과 렌더링 설정에 맞는 배리언트가 선택됩니다.
예를 들어 노멀 맵을 사용하는 머티리얼은 노멀 맵 코드가 포함된 배리언트를 사용하고, 노멀 맵을 사용하지 않는 머티리얼은 그 코드가 빠진 배리언트를 사용합니다.

그 결과 노멀 맵을 사용하지 않는 배리언트에서는 노멀 맵 샘플링 경로가 빠지고, 프래그먼트 셰이더가 해당 기능을 분기 처리하지 않아도 됩니다.
반대로 키워드 조합이 많아질수록 미리 만들어야 하는 배리언트 수도 함께 늘어납니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 550" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 타이틀 -->
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셰이더 소스 코드 (하나) → 배리언트 생성</text>

  <!-- 소스 코드 박스 -->
  <rect x="30" y="34" width="480" height="250" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="58" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">키워드 선언</text>
  <text x="50" y="78" font-family="monospace" font-size="10" fill="currentColor">#pragma multi_compile _ FOG_ON</text>
  <text x="380" y="78" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(2가지 상태)</text>
  <text x="50" y="96" font-family="monospace" font-size="10" fill="currentColor">#pragma multi_compile _ NORMAL_MAP_ON</text>
  <text x="380" y="96" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">(2가지 상태)</text>

  <text x="50" y="120" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">( _ 는 "키워드 없음", 즉 해당 기능 OFF )</text>

  <!-- 구분선 -->
  <line x1="50" y1="134" x2="490" y2="134" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <text x="50" y="156" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">셰이더 로직</text>
  <text x="50" y="176" font-family="monospace" font-size="10" fill="currentColor">#if defined(FOG_ON)</text>
  <text x="70" y="194" font-family="monospace" font-size="10" fill="currentColor" opacity="0.6">포그 계산</text>
  <text x="50" y="212" font-family="monospace" font-size="10" fill="currentColor">#endif</text>
  <text x="50" y="232" font-family="monospace" font-size="10" fill="currentColor">#if defined(NORMAL_MAP_ON)</text>
  <text x="70" y="250" font-family="monospace" font-size="10" fill="currentColor" opacity="0.6">노멀 맵 샘플링</text>
  <text x="50" y="268" font-family="monospace" font-size="10" fill="currentColor">#endif</text>

  <!-- 컴파일 화살표 -->
  <line x1="270" y1="284" x2="270" y2="330" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,326 270,336 276,326" fill="currentColor"/>
  <text x="290" y="312" font-family="sans-serif" font-size="11" fill="currentColor" font-weight="bold">컴파일: 2 × 2 = 배리언트 4개</text>

  <!-- 배리언트 4개를 2×2 그리드로 -->
  <rect x="30" y="342" width="235" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="147" y="367" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">배리언트 1: FOG_OFF + NORMAL_MAP_OFF</text>

  <rect x="275" y="342" width="235" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="392" y="367" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">배리언트 2: FOG_ON + NORMAL_MAP_OFF</text>

  <rect x="30" y="392" width="235" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="147" y="417" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">배리언트 3: FOG_OFF + NORMAL_MAP_ON</text>

  <rect x="275" y="392" width="235" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="392" y="417" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">배리언트 4: FOG_ON + NORMAL_MAP_ON</text>

  <!-- 하단 설명 -->
  <rect x="70" y="455" width="400" height="50" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1"/>
  <text x="270" y="476" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">각 배리언트는 별도로 컴파일된 셰이더 프로그램</text>
  <text x="270" y="493" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">해당 기능 조합에 맞는 버전이 런타임에 선택됨</text>
</svg>
</div>

<br>

위 예시에서는 FOG_ON과 NORMAL_MAP_ON 두 키워드가 각각 켜짐/꺼짐 상태를 가지므로, 2 × 2 = 4개의 배리언트가 만들어집니다.
기능이 꺼진 배리언트에는 해당 계산 경로가 포함되지 않아 런타임 분기를 줄일 수 있지만, 키워드가 늘어날수록 조합 수도 빠르게 증가합니다.

---

## 배리언트 폭증(Variant Explosion)

배리언트 폭증은 키워드가 많아서 생기는 문제가 아니라, **키워드 조합**이 많아서 생기는 문제입니다.
각 기능은 보통 켜짐/꺼짐 또는 여러 품질 단계 중 하나를 선택하는 형태이고, Unity는 이 선택 조합마다 별도의 배리언트를 만들 수 있습니다.

### 배리언트 수 계산

배리언트는 기능별 선택을 모두 조합해서 만들어집니다.
포그를 켤지 끌지, 노멀 맵을 사용할지 말지, 그림자 품질을 어떤 단계로 둘지 같은 선택이 서로 곱해지는 구조입니다.

<br>

| 기능 | 선택 가능한 상태 | 선택지 수 |
|------|----------------|-----------|
| Fog | OFF / ON | 2 |
| Normal Map | OFF / ON | 2 |
| Shadow Quality | LOW / MEDIUM / HIGH | 3 |

<br>

이 경우 가능한 조합은 `2 × 2 × 3 = 12개`입니다.
Fog만 보면 2가지지만, 여기에 Normal Map의 2가지 상태가 곱해져 4가지가 되고, 다시 Shadow Quality의 3가지 상태가 곱해져 12가지가 됩니다.

배리언트 수가 빠르게 늘어나는 이유는, 새 기능이 기존 조합 뒤에 단순히 몇 개를 더하는 것이 아니라 기존 조합 전체를 다시 나누기 때문입니다.
예를 들어 위의 12개 조합에 ON/OFF 기능을 하나 더 추가하면 24개가 되고, 3단계 품질 옵션을 추가하면 36개가 됩니다.

<br>

| 추가되는 조건 | 배수 | 12개 조합 기준 결과 |
|--------------|------|------------------|
| ON/OFF 기능 1개 | ×2 | 24개 |
| 3단계 품질 옵션 1개 | ×3 | 36개 |
| ON/OFF 기능 2개 | ×4 | 48개 |
| ON/OFF 기능 5개 | ×32 | 384개 |

<br>

실제 프로젝트에서는 머티리얼에서 직접 켜는 키워드만 배리언트를 만드는 것이 아닙니다.
포그 사용 여부, 라이트맵 사용 여부, 그림자 설정, GPU Instancing, 렌더 파이프라인의 품질 옵션도 셰이더 컴파일 조건에 포함될 수 있습니다.

즉, 셰이더 코드가 짧더라도 프로젝트 설정과 머티리얼 옵션이 많이 열려 있으면 Unity가 준비해야 하는 배리언트 수가 크게 늘어날 수 있습니다.

### 배리언트 폭증의 영향

배리언트는 단순한 목록이 아니라 실제로 컴파일되고, 빌드에 포함되며, 런타임에 로드될 수 있는 셰이더 프로그램입니다.
따라서 배리언트 수가 많아지면 빌드 시간, 빌드 크기, 로딩 시간에 모두 영향을 줍니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 타이틀 -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">배리언트 폭증의 영향</text>

  <!-- (1) 빌드 시간 -->
  <rect x="30" y="38" width="460" height="82" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="58" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(1) 빌드 시간</text>
  <text x="50" y="78" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">컴파일해야 할 셰이더 조합 수 증가</text>
  <text x="50" y="94" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">셰이더, 플랫폼, 품질 설정별로 비용 누적</text>
  <text x="50" y="110" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">빌드 파이프라인의 셰이더 처리 시간이 길어짐</text>

  <!-- 화살표 1→2 -->
  <line x1="260" y1="120" x2="260" y2="136" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,132 260,142 266,132" fill="currentColor"/>

  <!-- (2) 빌드 크기와 메모리 -->
  <rect x="30" y="144" width="460" height="66" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="164" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(2) 빌드 크기와 메모리</text>
  <text x="50" y="184" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">빌드에 포함되는 셰이더 데이터 증가</text>
  <text x="50" y="200" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">설치 크기와 런타임 메모리 사용량 증가 가능</text>

  <!-- 화살표 2→3 -->
  <line x1="260" y1="210" x2="260" y2="226" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,222 260,232 266,222" fill="currentColor"/>

  <!-- (3) 로딩 시간 -->
  <rect x="30" y="234" width="460" height="66" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="254" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">(3) 로딩 시간</text>
  <text x="50" y="274" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">씬 전환이나 머티리얼 로딩 시 필요한 배리언트 준비</text>
  <text x="50" y="290" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">처음 사용하는 배리언트에서 로딩 지연이나 히치 가능</text>
</svg>
</div>

<br>

따라서 배리언트 관리는 셰이더 코드의 실행 비용과는 별개의 최적화 축입니다. 프레임 안에서 실행되는 연산을 줄이는 것만큼, 빌드에 포함되는 셰이더 조합을 관리하는 일도 중요합니다.

---

## multi_compile과 shader_feature

같은 키워드 조합이라도 어떤 `#pragma`로 선언했는지에 따라 빌드에 포함되는 범위가 달라집니다.
이 차이를 이해하려면 `multi_compile`과 `shader_feature`를 구분해야 합니다.

### multi_compile

`multi_compile`은 선언된 선택지의 모든 조합을 빌드에 포함합니다.
현재 씬이나 머티리얼에서 일부 조합만 사용하고 있어도, 런타임 전환 가능성을 위해 나머지 조합까지 빌드에 포함됩니다.

<br>

```
#pragma multi_compile _ FEATURE_A_ON
#pragma multi_compile _ FEATURE_B_ON
#pragma multi_compile _ FEATURE_C_ON

선택지:
  Feature A = OFF / ON
  Feature B = OFF / ON
  Feature C = OFF / ON

가능한 조합 = 2 × 2 × 2 = 8개
```

<br>

`_`는 해당 키워드가 꺼진 상태입니다. 위 예시에서는 기능 A, B, C가 각각 OFF/ON 두 상태를 가지므로 총 8개의 조합이 만들어집니다.
`multi_compile`은 이 8개 조합을 현재 머티리얼 사용 여부와 관계없이 빌드에 포함합니다. 빌드 크기는 늘 수 있지만, 런타임에 코드나 품질 설정으로 키워드를 바꿔도 필요한 배리언트를 찾을 수 있습니다. 따라서 옵션 메뉴에서 포그를 켜고 끄는 기능처럼 실행 중 키워드 상태가 바뀌는 경우에는 `shader_feature`보다 `multi_compile`이 적합합니다.

<br>

### shader_feature

`shader_feature`는 빌드에 포함할 배리언트를 실제로 사용되는 조합 위주로 좁히는 방식입니다. 사용되지 않는 `shader_feature` 배리언트는 최종 빌드에서 제외될 수 있습니다.

<br>

```
#pragma shader_feature _ NORMAL_MAP_ON
#pragma shader_feature _ EMISSION_ON

선언상 가능한 조합:
  Normal Map = OFF / ON
  Emission   = OFF / ON

전체 조합 = 2 × 2 = 4개

실제로 사용 중인 머티리얼 조합:
  머티리얼 A = NORMAL_MAP_ON  + EMISSION_OFF
  머티리얼 B = NORMAL_MAP_OFF + EMISSION_ON

빌드에 남는 조합 = 사용된 2개 조합
사용되지 않은 조합 = 제외 가능
```

<br>

이처럼 `shader_feature`는 머티리얼에서 실제로 쓰는 조합만 남길 수 있어, 불필요한 배리언트와 빌드 크기를 줄이는 데 유리합니다.

대신 실행 중 키워드 상태를 바꾸는 기능에는 맞지 않을 수 있습니다. 예를 들어 빌드 시점에 `NORMAL_MAP_ON + EMISSION_ON` 조합이 사용되지 않았다면, 해당 배리언트는 빌드에서 빠질 수 있습니다. 이후 코드로 `EMISSION_ON`을 켜도 그 조합의 배리언트가 없으면 의도한 셰이더 경로를 사용할 수 없습니다.

<br>

### 선택 기준

실행 중에 키워드 상태가 바뀔 수 있으면 `multi_compile`을 사용합니다. 반대로 빌드 전에 사용할 조합이 정해져 있고 실행 중 바꾸지 않는 기능이라면 `shader_feature`를 우선 검토합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 타이틀 -->
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">multi_compile vs shader_feature 선택</text>

  <!-- 왼쪽: multi_compile -->
  <rect x="20" y="40" width="240" height="220" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="64" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">multi_compile</text>

  <!-- 구분선 -->
  <line x1="40" y1="74" x2="240" y2="74" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <text x="40" y="96" font-family="sans-serif" font-size="10" fill="currentColor">실행 중 키워드 상태가</text>
  <text x="40" y="112" font-family="sans-serif" font-size="10" fill="currentColor">바뀔 수 있는 경우</text>

  <text x="40" y="138" font-family="sans-serif" font-size="10" fill="currentColor">코드나 품질 설정에서</text>
  <text x="40" y="154" font-family="sans-serif" font-size="10" fill="currentColor">키워드를 전환하는 경우</text>

  <!-- 결과 강조 -->
  <rect x="35" y="172" width="210" height="36" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="140" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">모든 조합이 빌드에 포함</text>
  <text x="140" y="204" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">전환에는 안전, 크기는 증가</text>

  <!-- 화살표 (vs 표시) -->
  <text x="270" y="155" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.4">vs</text>

  <!-- 오른쪽: shader_feature -->
  <rect x="280" y="40" width="240" height="220" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="400" y="64" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">shader_feature</text>

  <!-- 구분선 -->
  <line x1="300" y1="74" x2="500" y2="74" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <text x="300" y="96" font-family="sans-serif" font-size="10" fill="currentColor">빌드 전에 사용할 조합이</text>
  <text x="300" y="112" font-family="sans-serif" font-size="10" fill="currentColor">정해지는 경우</text>

  <text x="300" y="138" font-family="sans-serif" font-size="10" fill="currentColor">실행 중 키워드 상태를</text>
  <text x="300" y="154" font-family="sans-serif" font-size="10" fill="currentColor">바꾸지 않는 경우</text>

  <!-- 결과 강조 -->
  <rect x="295" y="172" width="210" height="36" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="400" y="190" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">미사용 조합 제외 가능</text>
  <text x="400" y="204" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">배리언트 수와 크기 감소</text>
</svg>
</div>

<br>

실행 중 바뀌지 않는 조합을 `multi_compile`로 선언하면 사용하지 않는 배리언트까지 빌드에 남을 수 있습니다. 반대로 실행 중 바뀌는 조합을 `shader_feature`로 선언하면 필요한 배리언트가 빌드에서 제외되어, 런타임에 의도한 셰이더 경로를 사용할 수 없을 수 있습니다.

---

## 키워드 관리와 스트리핑

배리언트 수를 줄이는 작업은 두 지점에서 이루어집니다. 하나는 키워드 조합 자체를 줄이는 것이고, 다른 하나는 빌드 과정에서 필요 없는 후보를 제거하는 것입니다.

### 사용하지 않는 키워드 제거

배리언트 수를 줄일 때는 먼저 키워드 자체를 줄이는 편이 효과적입니다. 사용하지 않는 키워드가 셰이더에 남아 있으면 그 키워드까지 포함해 배리언트 후보가 만들어지고, 이후 스트리핑 단계에서 걸러야 할 조합도 늘어납니다. ON/OFF 키워드 하나만 추가되어도 기존 조합마다 켜진 버전과 꺼진 버전이 나뉘기 때문입니다.

<br>

```
ON/OFF 키워드 기준

키워드 10개:
  가능한 조합 = 2^10 = 1,024

키워드 8개:
  가능한 조합 = 2^8 = 256

키워드 2개를 줄이면
  후보 배리언트 공간 = 1,024개 → 256개
```

<br>

이처럼 키워드를 줄이면 스트리핑 이전 단계에서 만들어지는 배리언트 후보 수가 먼저 줄어듭니다.
항상 켜져 있거나 항상 꺼져 있는 기능, 프로젝트에서 사용하지 않는 품질 단계, 특정 셰이더에 필요 없는 렌더링 옵션은 키워드로 분리하지 않는 편이 좋습니다.
가능한 조합이 줄어들수록 빌드가 검사하고 컴파일해야 할 셰이더 프로그램도 함께 줄어듭니다.

### Unity의 셰이더 스트리핑(Shader Stripping)

앞 절의 키워드 정리는 셰이더 코드에서 불필요한 키워드 선언을 없애는 작업입니다. 이렇게 하면 해당 키워드가 만들던 조합 자체가 사라집니다. 반면 스트리핑은 셰이더에 남아 있는 `multi_compile`, `shader_feature`, 렌더 파이프라인 내부 키워드가 만든 후보 중 일부를 빌드에서 제외하는 작업입니다.

따라서 남아 있는 모든 조합이 그대로 최종 빌드에 들어가는 것은 아닙니다. Unity는 프로젝트 설정과 사용 중인 머티리얼을 기준으로, 빌드에 필요하지 않다고 판단되는 배리언트를 제외합니다.

이처럼 빌드에 포함할 배리언트를 줄이는 과정을 **셰이더 스트리핑**이라고 합니다. 프로젝트에서 포그를 사용하지 않으면 포그 관련 배리언트를 제외할 수 있고, `shader_feature`로 선언된 기능이 어떤 머티리얼에서도 쓰이지 않으면 그 조합도 빌드에서 빠질 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 520" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 타이틀 -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셰이더 스트리핑 과정</text>

  <!-- 남은 키워드 박스 -->
  <rect x="120" y="34" width="280" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="49" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">셰이더에 남아 있는 키워드</text>
  <text x="260" y="64" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">multi_compile · shader_feature · 파이프라인 키워드</text>

  <!-- 화살표 1 -->
  <line x1="260" y1="70" x2="260" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,84 260,94 266,84" fill="currentColor"/>

  <!-- 배리언트 후보 목록 박스 -->
  <rect x="130" y="96" width="260" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="111" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">배리언트 후보 목록</text>
  <text x="260" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">아직 빌드에 모두 들어간 상태는 아님</text>

  <!-- 화살표 2 -->
  <line x1="260" y1="132" x2="260" y2="150" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,146 260,156 266,146" fill="currentColor"/>

  <!-- 스트리핑 단계 그룹 박스 -->
  <rect x="30" y="158" width="460" height="285" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="178" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">스트리핑 단계</text>

  <!-- (1) 설정 기반 스트리핑 박스 -->
  <rect x="50" y="190" width="420" height="62" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="211" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(1) 설정 기반 스트리핑</text>
  <text x="260" y="230" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Graphics Settings, 렌더 파이프라인 설정 반영</text>
  <text x="260" y="245" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">꺼진 기능의 포그·라이트맵·그림자 조합 제외</text>

  <!-- (2) shader_feature 박스 -->
  <rect x="50" y="268" width="420" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="289" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(2) shader_feature 스트리핑</text>
  <text x="260" y="308" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">머티리얼에서 사용하지 않는 shader_feature 조합 제외</text>

  <!-- (3) 커스텀 스트리핑 박스 -->
  <rect x="50" y="339" width="420" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="360" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(3) 커스텀 스트리핑</text>
  <text x="260" y="379" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">IPreprocessShaders로 프로젝트 규칙 적용</text>

  <!-- 화살표 3 (그룹 박스 밖으로) -->
  <line x1="260" y1="443" x2="260" y2="466" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,462 260,472 266,462" fill="currentColor"/>

  <!-- 남은 배리언트만 빌드에 포함 박스 -->
  <rect x="115" y="476" width="290" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="491" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">남은 배리언트만 컴파일</text>
  <text x="260" y="506" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">최종 빌드에 포함</text>
</svg>
</div>

<br>

스트리핑은 셰이더 코드만으로 결정되지 않습니다. 프로젝트 설정에서 어떤 기능을 사용할 수 있다고 열어 두었는지도 중요합니다.
예를 들어 포그, 인스턴싱, 특정 라이트/그림자 기능을 실제로 쓰지 않는다면, 셰이더 코드뿐 아니라 Graphics Settings와 렌더 파이프라인 설정에서도 해당 기능을 사용하지 않는 상태로 맞춰 두는 편이 좋습니다. 이렇게 해야 Unity의 스트리핑 단계에서 관련 배리언트가 제거될 수 있습니다.

### IPreprocessShaders로 커스텀 스트리핑

`IPreprocessShaders`는 빌드 과정에서 Unity가 셰이더 배리언트를 컴파일하기 전에 호출되는 콜백 인터페이스입니다. 핵심은 `OnProcessShader(shader, snippet, data)`의 세 번째 인자인 `data`입니다. `data`는 컴파일 후보 배리언트가 들어 있는 수정 가능한 목록입니다.

개발자는 특정 셰이더 이름, 패스 타입, 키워드 조합을 확인한 뒤, 프로젝트에 필요 없는 항목을 `data`에서 제거할 수 있습니다. 콜백이 끝나면 Unity는 `data`에 남아 있는 배리언트만 컴파일합니다. 즉, Unity의 기본 스트리핑으로 부족한 부분을 개발자가 프로젝트 기준에 맞게 직접 지정할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">IPreprocessShaders 커스텀 스트리핑</text>
  <!-- Step 1: 컴파일 후보 목록(data) -->
  <rect x="160" y="38" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="54" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">컴파일 후보 목록(data)</text>
  <text x="260" y="68" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">ShaderCompilerData 리스트</text>
  <!-- Arrow down -->
  <line x1="260" y1="74" x2="260" y2="94" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,90 260,100 266,90" fill="currentColor"/>
  <!-- Step 2: OnProcessShader 호출 -->
  <rect x="75" y="100" width="370" height="36" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="123" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">OnProcessShader(shader, snippet, data) 호출</text>
  <!-- Arrow down -->
  <line x1="260" y1="136" x2="260" y2="160" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,156 260,166 266,156" fill="currentColor"/>
  <!-- Filter group background -->
  <rect x="55" y="166" width="410" height="196" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="260" y="184" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">개발자 코드에서 제거할 항목 판단</text>
  <!-- Filter 1: 셰이더 이름 -->
  <rect x="85" y="194" width="350" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="211" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">셰이더 이름 확인</text>
  <text x="260" y="227" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">예: 배포 빌드에서 Debug 셰이더 후보 제거</text>
  <!-- Arrow down -->
  <line x1="260" y1="234" x2="260" y2="248" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,244 260,254 266,244" fill="currentColor"/>
  <!-- Filter 2: 패스 타입 -->
  <rect x="85" y="254" width="350" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="271" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">패스/스니펫 확인</text>
  <text x="260" y="287" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">예: 사용하지 않는 Pass의 후보 제거</text>
  <!-- Arrow down -->
  <line x1="260" y1="294" x2="260" y2="308" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,304 260,314 266,304" fill="currentColor"/>
  <!-- Filter 3: 키워드 -->
  <rect x="85" y="314" width="350" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="331" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">키워드 조합 확인</text>
  <text x="260" y="347" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">예: 쓰지 않는 라이트 키워드 조합 제거</text>
  <!-- Arrow down to result -->
  <line x1="260" y1="356" x2="260" y2="378" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,374 260,384 266,374" fill="currentColor"/>
  <!-- Result -->
  <rect x="115" y="384" width="290" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="399" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">data에 남은 항목만 컴파일</text>
  <text x="260" y="413" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">제거한 항목은 빌드에서 제외</text>
</svg>
</div>

<br>

커스텀 스트리핑은 자동 스트리핑보다 더 구체적인 기준을 적용할 수 있지만, 잘못 제거했을 때의 영향도 큽니다. 런타임에 필요한 조합을 제거하면 해당 키워드 조합의 배리언트가 없어지고, Unity가 대체 배리언트를 선택해 결과가 달라지거나 의도한 셰이더 경로를 사용할 수 없게 됩니다.

따라서 커스텀 스트리핑은 프로젝트에서 사용하지 않는다고 확인된 조건에만 적용해야 합니다. 적용 후에는 빌드된 플레이어에서 주요 씬과 머티리얼을 확인하고, 필요한 배리언트가 빠지지 않았는지도 빌드 로그로 함께 점검해야 합니다.

<br>

### 빌드 로그에서 배리언트 수 확인

키워드를 정리하고 스트리핑 규칙을 추가했다면, 실제로 배리언트 수가 줄었는지 확인해야 합니다. Unity 에디터에서 빌드를 수행하면 `Editor.log`에 셰이더와 패스별 배리언트 수가 단계별로 기록됩니다.

<br>

```
Editor.log의 셰이더 배리언트 정보 예시

Compiling shader "Universal Render Pipeline/Lit" pass "ForwardLit"
    Full variant space:          24,576
    After settings filtering:     4,096
    After built-in stripping:     1,024
    After scriptable stripping:     256
    Compiled:                       256

→ 가능한 후보 24,576개 중 최종 컴파일 대상은 256개
```

<br>

항목명과 출력 형식은 Unity 버전과 렌더 파이프라인에 따라 조금 달라질 수 있지만, 후보 수가 단계별로 줄어드는 흐름은 같습니다.

| 항목 | 의미 |
|------|------|
| `Full variant space` | 스트리핑 전, 키워드 조합으로 만들 수 있는 전체 후보 수 |
| `After settings filtering` | 프로젝트, 플랫폼, Graphics Settings를 반영한 뒤의 후보 수 |
| `After built-in stripping` | Unity와 렌더 파이프라인의 자동 스트리핑이 적용된 뒤의 후보 수 |
| `After scriptable stripping` | `IPreprocessShaders` 같은 스크립트 기반 스트리핑이 적용된 뒤의 후보 수 |
| `Compiled` | 최종적으로 컴파일된 배리언트 수 |

새 키워드를 추가하거나 렌더 파이프라인 설정을 바꾼 뒤에는 이 로그를 이전 빌드와 비교하는 편이 좋습니다.
먼저 `Full variant space`를 보면 키워드 조합 자체가 얼마나 커졌는지 확인할 수 있습니다.

그다음 `After settings filtering`과 `After built-in stripping`에서 후보 수가 줄어드는지 확인합니다. 이 단계에서 거의 줄지 않는다면 프로젝트 설정이나 렌더 파이프라인 설정에 사용하지 않는 기능이 남아 있을 수 있습니다. `After scriptable stripping`에서 변화가 없다면 커스텀 스트리핑 규칙이 실제 후보와 맞는지 확인해야 합니다.

---

## Shader Graph 고려사항

Shader Graph를 사용해도 앞에서 다룬 셰이더 비용과 배리언트 문제는 사라지지 않습니다. 노드 그래프로 작성할 뿐, 최종적으로는 Unity가 셰이더 코드와 배리언트를 생성합니다.

### Shader Graph의 편의성

Unity의 **Shader Graph**는 노드를 연결해 셰이더를 작성하는 시각적 도구입니다. HLSL 코드를 직접 작성하지 않아도 텍스처 샘플링, 색상 연산, 노멀 맵, 마스크 조합 같은 로직을 그래프 형태로 구성할 수 있습니다.

이 덕분에 셰이더 코드를 직접 다루지 않아도 결과를 빠르게 만들고 수정할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 타이틀 -->
  <text x="270" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Shader Graph의 변환 흐름</text>

  <!-- Shader Graph 에디터 영역 -->
  <rect x="20" y="40" width="500" height="160" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Shader Graph 에디터</text>

  <!-- Texture Sample 흐름 -->
  <rect x="40" y="82" width="100" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">텍스처</text>

  <rect x="170" y="82" width="110" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Sample Texture</text>

  <line x1="140" y1="97" x2="166" y2="97" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="164,93 172,97 164,101" fill="currentColor"/>

  <rect x="40" y="130" width="100" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="150" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">색상</text>

  <rect x="320" y="106" width="80" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="126" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">Multiply</text>

  <line x1="280" y1="97" x2="316" y2="114" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="311,109 320,116 313,120" fill="currentColor"/>

  <line x1="140" y1="145" x2="316" y2="128" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="311,123 320,126 313,132" fill="currentColor"/>

  <rect x="430" y="106" width="70" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="465" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Base Color</text>

  <line x1="400" y1="121" x2="426" y2="121" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="424,117 432,121 424,125" fill="currentColor"/>

  <!-- Normal 흐름 -->
  <rect x="40" y="165" width="100" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="182" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">노멀 맵</text>

  <rect x="170" y="165" width="110" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="182" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Unpack Normal</text>

  <line x1="140" y1="178" x2="166" y2="178" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="164,174 172,178 164,182" fill="currentColor"/>

  <rect x="320" y="165" width="80" height="26" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="360" y="182" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Normal</text>

  <line x1="280" y1="178" x2="316" y2="178" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="314,174 322,178 314,182" fill="currentColor"/>

  <!-- 변환 화살표 영역 -->
  <text x="270" y="222" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">Unity가 그래프를 셰이더 소스와 키워드 정보로 변환</text>
  <line x1="270" y1="230" x2="270" y2="255" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="264,251 270,261 276,251" fill="currentColor"/>

  <!-- 생성된 HLSL 코드 영역 -->
  <rect x="20" y="270" width="245" height="120" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="142" y="292" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">생성된 HLSL</text>

  <rect x="40" y="306" width="205" height="70" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="52" y="326" font-family="monospace" font-size="9" fill="currentColor">sample = SAMPLE_TEXTURE2D(...)</text>
  <text x="52" y="346" font-family="monospace" font-size="9" fill="currentColor">baseColor = sample * color</text>
  <text x="52" y="366" font-family="monospace" font-size="9" fill="currentColor">normal = UnpackNormal(...)</text>

  <!-- 키워드/배리언트 영역 -->
  <rect x="275" y="270" width="245" height="120" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="398" y="292" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">키워드와 배리언트</text>

  <rect x="295" y="306" width="205" height="70" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="398" y="326" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Keyword 노드와 Graph 설정</text>
  <text x="398" y="346" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">기능 조합별 배리언트 생성</text>
  <text x="398" y="366" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">일반 셰이더처럼 스트리핑 대상</text>

  <!-- 하단 note -->
  <text x="270" y="415" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">그래프는 편의 도구이며, 결과물은 일반 셰이더처럼 비용과 배리언트를 관리해야 함</text>
</svg>
</div>

<br>

### 생성 코드의 비효율성

직접 작성한 HLSL에서는 셰이더가 실제로 필요한 계산 경로만 남기기 쉽습니다. 반면 Shader Graph는 노드와 연결 구조를 바탕으로 HLSL을 생성합니다. 따라서 그래프에 남아 있는 노드가 많거나 연결이 복잡하면 생성 코드도 복잡해질 수 있습니다.
테스트 목적으로 추가했다가 정리하지 않은 노드, 더 이상 결과에 필요하지 않은 중간 계산, 불필요하게 복잡한 마스크 조합이 남아 있으면 생성 코드가 무거워질 수 있습니다.

Unity나 GPU 컴파일러가 사용되지 않는 계산을 제거하는 경우도 있지만, 항상 제거된다고 기대해서는 안 됩니다. 따라서 Shader Graph를 사용할 때도 최종 출력에 필요한 노드만 남기고, 실험용 노드나 사용하지 않는 분기는 정리하는 편이 좋습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 타이틀 -->
  <text x="280" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Shader Graph 정리 여부와 생성 코드</text>

  <!-- === 정리된 그래프 (상단) === -->
  <rect x="15" y="38" width="530" height="105" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5"/>
  <text x="34" y="58" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정리된 그래프</text>

  <!-- 텍스처 A -->
  <rect x="35" y="72" width="76" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="73" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">텍스처 A</text>

  <!-- 샘플링 A -->
  <rect x="135" y="72" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="169" y="90" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">샘플링</text>

  <!-- 텍스처 A → 샘플링 A -->
  <line x1="111" y1="86" x2="131" y2="86" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="129,82 137,86 129,90" fill="currentColor"/>

  <!-- 텍스처 B -->
  <rect x="35" y="108" width="76" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="73" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">텍스처 B</text>

  <!-- 샘플링 B -->
  <rect x="135" y="108" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="169" y="126" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">샘플링</text>

  <!-- 텍스처 B → 샘플링 B -->
  <line x1="111" y1="122" x2="131" y2="122" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="129,118 137,122 129,126" fill="currentColor"/>

  <!-- Lerp -->
  <rect x="235" y="90" width="60" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="265" y="108" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Lerp</text>

  <!-- 샘플링 A → Lerp (직각 ㄱ자) -->
  <polyline points="203,86 219,86 219,99 231,99" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="229,95 237,99 229,103" fill="currentColor"/>

  <!-- 샘플링 B → Lerp (직각 ㄴ자) -->
  <polyline points="203,122 219,122 219,109 231,109" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="229,105 237,109 229,113" fill="currentColor"/>

  <!-- Multiply -->
  <rect x="330" y="90" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="364" y="108" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Multiply</text>

  <!-- Lerp → Multiply -->
  <line x1="295" y1="104" x2="326" y2="104" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="324,100 332,104 324,108" fill="currentColor"/>

  <!-- 출력 -->
  <rect x="435" y="90" width="60" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="465" y="108" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">출력</text>

  <!-- Multiply → 출력 -->
  <line x1="398" y1="104" x2="431" y2="104" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="429,100 437,104 429,108" fill="currentColor"/>

  <text x="280" y="136" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">필요한 경로만 남아 생성 코드도 단순함</text>

  <!-- === 정리되지 않은 그래프 (하단) === -->
  <rect x="15" y="160" width="530" height="125" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="34" y="180" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정리되지 않은 그래프</text>

  <rect x="35" y="202" width="76" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="73" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">텍스처 C</text>

  <rect x="135" y="202" width="68" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="169" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">샘플링</text>

  <line x1="111" y1="216" x2="131" y2="216" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="129,212 137,216 129,220" fill="currentColor"/>

  <rect x="235" y="202" width="70" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="270" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Contrast</text>

  <line x1="203" y1="216" x2="231" y2="216" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="229,212 237,216 229,220" fill="currentColor"/>

  <rect x="335" y="202" width="76" height="28" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="373" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Preview</text>

  <line x1="305" y1="216" x2="331" y2="216" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="329,212 337,216 329,220" fill="currentColor"/>

  <text x="280" y="260" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">테스트용 샘플링·보정·Preview 노드가 남아 있으면 그래프와 생성 코드 검토가 복잡해짐</text>

  <!-- 하단 설명 텍스트 -->
  <text x="280" y="306" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">컴파일러가 일부 계산을 제거할 수는 있지만, 필요한 노드만 남기는 것이 안전함</text>
</svg>
</div>

<br>

Shader Graph에서 주의해야 할 부분은 노드 구성이 그대로 셰이더 비용으로 이어질 수 있다는 점입니다. 노드 하나는 텍스처 샘플링, 벡터 변환, 정규화, 보간 같은 HLSL 연산으로 변환됩니다. 따라서 그래프가 복잡해질수록 프래그먼트 셰이더의 ALU 연산이나 텍스처 샘플링도 함께 늘어날 수 있습니다.

HLSL을 직접 작성할 때는 셰이더의 사용 조건에 맞춰 필요한 연산만 남길 수 있습니다. 반면 Shader Graph는 노드와 그래프 설정을 기준으로 코드를 생성하므로, 의도하지 않은 텍스처 샘플링, 반복되는 정규화, 불필요한 변환이 포함되지 않았는지 생성 코드를 확인해야 합니다.

Shader Graph의 Keyword도 일반 셰이더 키워드처럼 배리언트를 만듭니다. 예를 들어 ON/OFF Keyword 하나를 추가하면 기능이 꺼진 배리언트와 켜진 배리언트가 나뉘고, 다른 Keyword와 조합되면서 전체 배리언트 수가 늘어납니다.
따라서 그래프를 점검할 때는 노드 수뿐 아니라 Keyword 설정도 함께 확인해야 합니다. 해당 Keyword가 `shader_feature`인지 `multi_compile`인지, 로컬 키워드인지 글로벌 키워드인지에 따라 빌드에 남는 배리언트 범위가 달라집니다.

<br>

### 생성 코드 확인과 최적화

Shader Graph의 실제 비용은 최종적으로 생성된 셰이더 코드에서 드러납니다. Unity 버전에 따라 메뉴 이름은 조금 다를 수 있지만, Shader Graph 에셋의 Inspector에서 생성 코드나 컴파일된 셰이더를 확인할 수 있습니다.

**Shader Graph 생성 코드 점검 항목**

| 점검 항목 | 확인 이유 |
|----------|----------|
| 사용되지 않는 텍스처 샘플링 | 불필요한 텍스처 접근은 프래그먼트 셰이더 비용을 늘립니다. |
| 반복되는 정규화(normalize)나 변환 | 같은 보정 연산이 여러 번 들어가면 ALU 비용이 증가합니다. |
| `float` 정밀도 사용 | `half`로 충분한 값까지 `float`으로 남아 있으면 레지스터와 연산 비용이 커질 수 있습니다. |
| 의도하지 않은 Keyword | 불필요한 배리언트가 늘어나 빌드 크기와 로딩 비용에 영향을 줄 수 있습니다. |

<br>
단순한 머티리얼이나 사용 빈도가 낮은 효과라면 Shader Graph를 그대로 사용해도 충분한 경우가 많습니다. 반대로 화면에서 넓게 쓰이거나 프레임마다 많이 그려지는 셰이더라면, Shader Graph로 프로토타입을 만든 뒤 생성 코드를 참고해 HLSL로 직접 작성하는 방법도 고려할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- 타이틀 -->
  <text x="260" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Shader Graph 활용 워크플로</text>

  <!-- (1) 프로토타입 박스 -->
  <rect x="120" y="36" width="280" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="53" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(1) Shader Graph에서 프로토타입</text>
  <text x="260" y="68" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">시각적으로 결과 확인</text>

  <!-- 화살표 1→2 -->
  <line x1="260" y1="76" x2="260" y2="96" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,92 260,102 266,92" fill="currentColor"/>

  <!-- (2) 생성 코드 확인 박스 -->
  <rect x="120" y="104" width="280" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="121" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(2) 생성 코드 확인</text>
  <text x="260" y="136" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">불필요한 연산, 키워드 수 파악</text>

  <!-- 화살표 2→3 -->
  <line x1="260" y1="144" x2="260" y2="164" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="254,160 260,170 266,160" fill="currentColor"/>

  <!-- (3) 판단 박스 -->
  <rect x="160" y="172" width="200" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="260" y="195" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">(3) 판단</text>

  <!-- 분기 stem (판단 → 분기점) -->
  <line x1="260" y1="208" x2="260" y2="224" stroke="currentColor" stroke-width="1.5"/>

  <!-- 분기 좌 (ㄴ자) -->
  <polyline points="260,224 140,224 140,240" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="134,236 140,246 146,236" fill="currentColor"/>

  <!-- 분기 우 (ㄱ자) -->
  <polyline points="260,224 380,224 380,240" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="374,236 380,246 386,236" fill="currentColor"/>

  <!-- 좌: Shader Graph 유지 -->
  <rect x="30" y="248" width="220" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="140" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Shader Graph 그대로 사용</text>
  <text x="140" y="286" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">성능에 민감하지 않은 셰이더</text>

  <!-- 우: 직접 작성한 HLSL 전환 -->
  <rect x="270" y="248" width="220" height="50" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="380" y="268" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">직접 작성한 HLSL로 전환</text>
  <text x="380" y="286" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">성능에 민감한 셰이더 → 최적화</text>
</svg>
</div>

<br>

Shader Graph를 사용할지 HLSL로 직접 작성할지는 셰이더의 사용 빈도와 GPU 비용을 기준으로 판단하는 편이 좋습니다.
사용 빈도가 낮거나 화면에서 차지하는 면적이 작은 효과는 Shader Graph로 유지해도 문제가 없는 경우가 많습니다.

반대로 화면에 넓게 그려지거나 많은 오브젝트에서 반복해서 사용되는 셰이더는 프레임 비용에 영향을 주기 쉽습니다.
이런 셰이더는 프로파일러로 GPU 비용을 확인한 뒤, 필요하다면 생성 코드를 정리하거나 HLSL로 직접 작성하는 방식으로 최적화합니다.

## 마무리

- 셰이더 배리언트는 키워드 조합마다 별도의 GPU 프로그램이 만들어지는 구조입니다.
- ON/OFF 키워드가 n개라면 가능한 조합은 2ⁿ으로 늘어나며, 품질 단계처럼 선택지가 3개 이상인 키워드가 섞이면 더 빠르게 증가합니다.
- `multi_compile`은 선언된 조합을 빌드에 남기는 쪽에 가깝고, `shader_feature`는 실제 사용 여부에 따라 일부 조합이 제외될 수 있습니다.
- 사용하지 않는 키워드 제거, Unity 자동 스트리핑, `IPreprocessShaders` 콜백으로 빌드에 포함되는 배리언트를 줄일 수 있습니다.
- Shader Graph를 사용할 때도 노드 구성, Keyword 설정, 생성 코드를 확인해야 합니다.

배리언트 관리는 감으로 판단하기보다 빌드 로그를 함께 보는 편이 좋습니다. 키워드를 추가하거나 셰이더 설정을 바꾼 뒤에는 `Full variant space`, 스트리핑 이후의 후보 수, 최종 `Compiled` 수를 비교해야 실제로 빌드에 남는 조합을 확인할 수 있습니다.

여기까지는 셰이더와 배리언트처럼 GPU 렌더링 비용에 영향을 주는 요소를 다루었습니다. 하지만 프레임 시간은 렌더링만으로 결정되지 않습니다. 충돌 감지, 리지드바디 시뮬레이션, 레이캐스트 같은 물리 연산도 매 프레임 CPU 시간을 사용합니다.

[PhysicsOptimization 시리즈](/dev/unity/PhysicsOptimization-1/)에서는 물리 엔진의 구조와 최적화를 다룹니다.

<br>

---

**관련 글**
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)
- [Unity 렌더 파이프라인 (2) - 드로우콜과 배칭](/dev/unity/UnityPipeline-2/)

**시리즈**
- [셰이더 최적화 (1) - 셰이더 성능의 원리](/dev/unity/ShaderOptimization-1/)
- **셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리 (현재 글)**

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
- **셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리** (현재 글)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
