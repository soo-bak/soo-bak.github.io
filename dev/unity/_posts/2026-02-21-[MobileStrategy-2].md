---
layout: single
title: "모바일 전략 (2) - 빌드와 품질 전략 - soo:bak"
date: "2026-02-21 01:50:00 +0900"
description: Quality Settings 티어, IL2CPP 스트리핑, 앱 사이즈, 디바이스 티어 전략, 전체 시리즈 통합 마무리를 다룹니다.
tags:
  - Unity
  - 최적화
  - 모바일
  - 빌드
  - 품질설정
---

## 기기별 성능 차이에 대응하기

[Part 1](/dev/unity/MobileStrategy-1/)에서 모바일 게임의 근본적 제약인 발열과 배터리를 다루었습니다. 서멀 쓰로틀링은 피크 성능과 지속 성능 사이에 큰 격차를 만듭니다. 60fps와 30fps 사이의 선택도 부드러움만의 문제가 아니라 전력 소비와 발열에 직결됩니다. 장시간 플레이에서 안정적인 경험을 유지하려면, 피크가 아닌 지속 성능을 기준으로 설계해야 합니다.

<br>

하지만 지속 성능이라는 기준 자체가 기기마다 다릅니다. 2GB RAM에 Mali-G52 GPU를 탑재한 저사양 기기와, 8GB RAM에 Apple A17 Pro를 탑재한 고사양 기기의 지속 성능은 수 배 차이가 납니다. 하나의 품질 설정으로 모든 기기를 만족시킬 수는 없습니다. 저사양에 맞추면 고사양 기기의 성능을 낭비하고, 고사양에 맞추면 저사양 기기에서 프레임이 유지되지 않기 때문입니다.

<br>

이 글에서는 다양한 성능의 기기에 대응하는 Quality Settings 전략과, 빌드 크기를 줄이는 IL2CPP 스트리핑 및 에셋 압축을 다룹니다. 전체 29편 시리즈의 마지막 글로서, 프레임 하나의 여정을 통합 정리하며 마무리합니다.

<br>

---

## Quality Settings 티어

Unity의 **Quality Settings**(Edit > Project Settings > Quality)는 여러 개의 품질 프리셋을 정의하고, 런타임에서 프리셋을 전환할 수 있는 시스템입니다. 각 프리셋에는 렌더 스케일, 그림자, 텍스처 해상도, LOD 등 렌더링 비용에 직접 영향을 미치는 설정이 포함됩니다.

<br>

**렌더 스케일(Render Scale).** URP의 Render Scale은 내부 렌더링 해상도를 화면 해상도보다 낮춥니다. 1080p 디스플레이에서 Render Scale 0.7이면 내부적으로 756p로 렌더링한 뒤 업스케일합니다. 가로와 세로가 모두 0.7배가 되므로 전체 픽셀 수는 약 49%(0.7 × 0.7)로 줄어들고, GPU 프래그먼트 부하가 절반 가까이 감소합니다. 단일 설정으로 가장 큰 GPU 비용 절감 효과를 얻을 수 있는 항목이지만, 해상도가 낮아지는 만큼 화면이 흐려지므로 UI는 별도 카메라로 원본 해상도를 유지하는 것이 일반적입니다.

**그림자.** 실시간 그림자는 셰도우맵을 별도로 렌더링하는 과정이므로 GPU 비용이 큽니다. 그림자를 끄면 셰도우맵 렌더링이 완전히 제거됩니다. 시각적으로 그림자가 필요한 경우에는 셰도우맵 해상도를 낮추거나(2048 → 512), 그림자 거리를 줄여 셰도우맵에 포함되는 오브젝트 수를 제한합니다. 캐스케이드 수도 중요한 조절 항목입니다. URP에서 Shadow Cascade Count가 4이면 셰도우맵을 4장 렌더링하고, 1이면 1장만 렌더링합니다. 저사양 프리셋에서는 캐스케이드를 1로 줄이면 그림자 패스의 GPU 비용이 크게 감소합니다.

**텍스처 해상도.** `QualitySettings.globalTextureMipmapLimit`(이전의 masterTextureLimit)으로 모든 텍스처의 밉맵 레벨을 강제로 올릴 수 있습니다. 밉맵(Mipmap)은 원본 텍스처를 절반, 1/4, 1/8 크기로 미리 축소해 둔 버전입니다. 값이 1이면 원본 대신 절반 해상도 밉맵을 사용하고, 2이면 1/4 해상도를 사용합니다. 텍스처 메모리와 대역폭이 함께 줄어듭니다.

**MSAA(Multi-Sample Anti-Aliasing).** MSAA는 폴리곤 경계의 계단 현상을 줄이는 안티앨리어싱 기법입니다. URP Asset에서 4x, 2x, Off를 선택할 수 있습니다. MSAA는 타일 기반 GPU에서 타일 메모리 안에서 처리되므로 데스크톱 GPU보다 비용이 낮지만, 4x MSAA는 여전히 프래그먼트 처리량과 타일 메모리 사용량을 늘립니다. 저사양 프리셋에서는 MSAA를 끄고, 고사양에서만 2x 또는 4x를 적용하는 것이 일반적입니다.

**후처리(Post-Processing).** URP Volume에 설정하는 Bloom, Color Grading, SSAO(Screen Space Ambient Occlusion) 등의 후처리 효과입니다. 이 중 SSAO는 화면의 모든 픽셀에 대해 주변 깊이를 샘플링하므로 모바일 GPU에서 비용이 높습니다. 저사양 프리셋에서 가장 먼저 끄는 항목이 SSAO이며, Bloom도 해상도가 높을수록 비용이 커지므로 다운샘플 횟수를 줄이거나 비활성화합니다. 후처리 효과의 활성 여부는 Volume Profile을 품질 등급별로 분리하여 관리합니다.

**LOD 바이어스.** LOD(Level of Detail) 전환 거리를 조절합니다. 기본값은 2.0이며, 값이 낮을수록 카메라에서 더 가까운 거리에서 저해상도 LOD로 전환됩니다. 저사양 프리셋에서 LOD 바이어스를 1.0이나 0.5로 낮추면, 화면에 보이는 메시의 정점 수가 줄어들어 버텍스 셰이더 부하가 감소합니다. 오브젝트가 많은 오픈월드 장르에서 효과가 큽니다.

<br>

URP에서는 각 Quality Level이 별도의 **URP Asset**(UniversalRenderPipelineAsset)을 참조합니다. 렌더 스케일, MSAA, 그림자 캐스케이드 등 렌더링 파이프라인 설정이 이 URP Asset에 정의되어 있으므로, 품질 프리셋마다 다른 URP Asset을 할당하면 Quality Level 전환 시 렌더링 설정이 함께 바뀝니다.

런타임에서는 `QualitySettings.SetQualityLevel(index)`로 프리셋을 전환합니다. 인덱스 0이 가장 낮은 품질, 숫자가 올라갈수록 높은 품질입니다.

<br>

---

## 디바이스 티어 전략

Quality Settings 프리셋을 정의한 다음에는, 어떤 기기에서 어떤 프리셋을 적용할지 결정해야 합니다. 이를 **디바이스 티어(Device Tier)** 전략이라 합니다.

<br>

### 티어 분류 기준

기기를 성능 등급으로 분류하는 데에는 여러 기준을 사용할 수 있습니다. Unity의 `SystemInfo` 클래스가 제공하는 정보가 대표적입니다.

<br>

```
디바이스 티어 분류에 사용하는 SystemInfo 항목

  SystemInfo.systemMemorySize     → RAM 크기 (MB) — 1차 분류 기준
  SystemInfo.graphicsDeviceName   → GPU 이름 문자열 — 정밀 분류 시 사용

기능 지원 여부 확인용
  SystemInfo.graphicsDeviceType     → 그래픽 API (Vulkan, Metal 등)
  SystemInfo.supportsComputeShaders → 컴퓨트 셰이더 지원 여부

티어 분류 예시
  Low   (저사양):  RAM ≤ 3GB,  GPU: Mali-G52, Adreno 506 등
  Mid   (중사양):  RAM 4~6GB,  GPU: Adreno 619, Mali-G77 등
  High  (고사양):  RAM ≥ 8GB,  GPU: Apple A15+, Adreno 730+ 등
```

<br>

RAM 크기가 가장 간단하고 효과적인 분류 기준입니다. 제조사가 고사양 SoC(System on Chip)를 탑재하는 기기에는 RAM도 많이 넣고, 저사양 SoC에는 RAM도 적게 넣는 경향이 있으므로, RAM 하나로도 대략적인 성능 등급을 추정할 수 있습니다.

GPU 이름으로 더 정밀하게 분류할 수도 있지만, GPU 모델이 수백 가지에 달하므로 관리 비용이 커집니다.

`SystemInfo.graphicsMemorySize`(GPU 메모리)와 `SystemInfo.processorFrequency`(CPU 클럭)도 존재하지만, 모바일 기기에서는 0이나 부정확한 값을 반환하는 경우가 많아 분류 기준으로 신뢰하기 어렵습니다.

<br>

### 티어별 설정

각 티어에 적용할 URP Asset 설정과 게임 자체 설정의 예시입니다. URP Asset 항목은 `SetQualityLevel`로 함께 전환되고, 게임 설정 항목은 별도 코드로 관리해야 합니다.

<br>

```
디바이스 티어별 설정 예시

Low 티어 (2~3GB RAM, Mali-G52 급)
  [URP Asset]
  렌더 스케일:     0.65~0.7 (1080p 기기에서 약 700~756p)
  그림자:          끔
  그림자 캐스케이드: —
  MSAA:           끔
  후처리:          끔
  텍스처 해상도:    Half (밉맵 레벨 +1)
  LOD 바이어스:     0.5
  [게임 설정]
  파티클 최대:      30~50개
  프레임레이트:     30fps

  목표: 30fps 안정 유지, 쓰로틀링 최소화

Mid 티어 (4~6GB RAM, Adreno 619 급)
  [URP Asset]
  렌더 스케일:     0.85 (1080p 기기에서 약 918p)
  그림자:          켬 (해상도 512, 거리 30m)
  그림자 캐스케이드: 1
  MSAA:           끔
  후처리:          Bloom
  텍스처 해상도:    Full
  LOD 바이어스:     1.0
  [게임 설정]
  파티클 최대:      100개
  프레임레이트:     30fps

  목표: 30fps 안정 유지, 시각적 품질 확보

High 티어 (8GB+ RAM, Apple A15 / Snapdragon 8 급)
  [URP Asset]
  렌더 스케일:     1.0 (풀 해상도)
  그림자:          켬 (해상도 1024, 거리 50m)
  그림자 캐스케이드: 2
  MSAA:           2x
  후처리:          Bloom + Color Grading + Vignette + SSAO
  텍스처 해상도:    Full
  LOD 바이어스:     1.5
  [게임 설정]
  파티클 최대:      200개
  프레임레이트:     60fps 옵션 제공

  목표: 높은 시각 품질 + 60fps 옵션
```

<br>

### 티어 결정 시점

Low/Mid/High 프리셋은 앱 최초 실행 시 자동으로 결정됩니다.

앱이 처음 실행되면 Unity의 `SystemInfo`에서 RAM, GPU 이름, 그래픽스 API 지원 여부 등을 읽어 티어를 판별하고, 해당 티어에 맞는 Quality Level을 적용하는 코드를 작성합니다. `QualitySettings.SetQualityLevel()`은 앱 재시작 시 유지되지 않으므로, 판별 결과를 `PlayerPrefs`에 저장해 두고 이후 실행에서는 저장된 값을 읽어 바로 적용합니다. `PlayerPrefs`는 Unity가 제공하는 간단한 키-값 저장소로, 앱을 종료해도 값이 유지됩니다.

<br>

```
디바이스 티어 결정 흐름

앱 최초 실행
    │
    ▼
SystemInfo 조회
(RAM, GPU 이름, API 지원 여부)
    │
    ▼
티어 판별 로직
    RAM ≤ 3GB                → Low
    3GB < RAM ≤ 6GB          → Mid
    RAM > 6GB                → High
    │
    ▼
QualitySettings.SetQualityLevel(tier)
    │
    ▼
PlayerPrefs에 티어 저장
    │
    ▼
설정 화면에서 플레이어가 수동 변경 가능
```

<br>

자동 판별 결과가 항상 정확하지는 않습니다. 예를 들어 RAM이 4GB인 구형 기기가 RAM 3GB인 신형 기기보다 GPU 성능이 낮을 수 있습니다. RAM 수치만으로는 실제 렌더링 성능을 정확히 반영하기 어렵기 때문입니다. 이런 한계를 보완하기 위해, 설정 화면에서 플레이어가 품질을 수동으로 변경할 수 있는 옵션을 함께 제공하는 것이 안전합니다.

<br>

---

## IL2CPP 스트리핑과 코드 최적화

앞서 디바이스 티어로 런타임 품질을 조절했다면, 빌드 크기는 IL2CPP 스트리핑으로 줄일 수 있습니다.

<br>

### IL2CPP와 코드 변환

Unity에서 C# 코드를 작성하면, C# 컴파일러가 **IL(Intermediate Language)** 바이트코드로 변환합니다. 모바일 빌드에서는 **IL2CPP** 백엔드가 이 IL 코드를 **C++ 코드**로 변환하고, 네이티브 컴파일러가 최종 실행 파일을 만듭니다.

<br>

```
IL2CPP 빌드 과정

C# 소스 코드
    │
    ▼  (C# 컴파일러)
IL 바이트코드 (.dll)
    │
    ▼  (IL2CPP)
C++ 소스 코드
    │
    ▼  (네이티브 컴파일러: Clang/GCC)
네이티브 바이너리 (.so / 실행 파일)

IL2CPP의 이점:
  - Mono(C#을 직접 실행하는 런타임)보다 실행 성능이 높음
    (네이티브 코드로 미리 컴파일되므로)
  - iOS에서 필수 (iOS는 보안 정책상 JIT(실행 시점 컴파일)를 허용하지 않음)
  - 코드 역공학이 어려움 (C++ 바이너리)
  
```

<br>

### Managed Stripping Level

IL2CPP 빌드 과정에서는 **코드 스트리핑(Code Stripping)**이 함께 수행됩니다. 스트리핑은 사용하지 않는 코드를 빌드에서 제거하여 실행 파일 크기를 줄이는 최적화입니다.

<br>

제거 범위는 Unity의 Player Settings에 있는 **Managed Stripping Level** 설정으로 조절합니다. 레벨이 높을수록 더 많은 코드를 제거하지만, 필요한 코드까지 잘못 제거할 위험도 함께 커집니다.

<br>

| 레벨 | 제거 범위 | 크기 감소 | 안전성 |
|------|----------|----------|--------|
| **Minimal** | UnityEngine·.NET 라이브러리에서 참조되지 않는 코드만 제거. 사용자 코드는 건드리지 않음 | 작음 | 높음 |
| **Low** | Minimal + 사용자 어셈블리에서도 정적으로 도달할 수 없는 코드 제거 | 중간 | 높음 |
| **Medium** | Low + 참조되지 않는 타입과 메서드까지 제거 | 큼 | 중간 |
| **High** | Medium + 메서드 본문 최적화, 가장 적극적으로 제거 | 가장 큼 | 낮음 |

Minimal과 Low의 차이는 사용자 코드 포함 여부입니다. Minimal은 Unity 엔진과 .NET 라이브러리만 정리하므로 사용자 코드에는 영향이 없고, Low부터 사용자 어셈블리의 미사용 코드도 제거 대상에 포함됩니다. Medium부터는 리플렉션으로 접근하는 타입이 "참조되지 않음"으로 판정되어 제거될 수 있습니다.

<br>

스트리핑 레벨이 높을수록 빌드 크기가 작아지지만, 리플렉션(Reflection)으로 접근하는 코드가 제거될 위험이 커집니다. 리플렉션은 문자열로 타입이나 메서드를 참조하는 방식이므로, 정적 분석으로는 "이 코드가 사용되는지" 판별할 수 없습니다. JSON 직렬화 라이브러리, 의존성 주입 프레임워크, 일부 애널리틱스 SDK가 리플렉션을 사용합니다.

<br>

### link.xml로 코드 보존

스트리핑이 필요한 코드까지 제거하는 것을 방지하려면 **link.xml** 파일을 프로젝트에 추가합니다. 이 파일에 보존할 타입이나 어셈블리를 명시하면, 스트리핑이 해당 코드를 제거하지 않습니다.

<br>

```xml
<linker>
  <!-- 특정 어셈블리 전체 보존 -->
  <assembly fullname="MyGameAssembly" preserve="all"/>

  <!-- 특정 타입만 보존 -->
  <assembly fullname="UnityEngine">
    <type fullname="UnityEngine.Networking.UnityWebRequest"
          preserve="all"/>
  </assembly>

  <!-- 네임스페이스 단위 보존 -->
  <assembly fullname="Newtonsoft.Json">
    <type fullname="Newtonsoft.Json.JsonConvert"
          preserve="all"/>
  </assembly>
</linker>
```

<br>

리플렉션을 거의 사용하지 않는 프로젝트라면 Medium이 안전한 출발점입니다. 빌드 크기 감소 효과가 충분하면서도 link.xml 관리 부담이 적습니다. 빌드 크기를 최대한 줄여야 하는 경우에는 High로 설정한 뒤 link.xml에 보존할 코드를 명시하는 조합을 사용합니다. 단, link.xml에서 누락한 타입이 있으면 런타임에서야 오류가 발생하므로, High 레벨을 적용한 빌드는 리플렉션을 사용하는 경로(JSON 파싱, 의존성 주입 등)를 중심으로 실기기 테스트를 거칩니다.

<br>

---

## 에셋 압축과 앱 사이즈

코드 스트리핑이 실행 파일 크기를 줄인다면, 에셋 압축은 전체 앱 크기에서 대부분을 차지하는 리소스 크기를 줄입니다. 모바일 앱의 빌드 크기에서 에셋은 전체 빌드의 90% 이상을 차지하고, 코드는 5% 내외에 불과합니다.

<br>

### 플랫폼 크기 제한

앱 스토어마다 초기 다운로드 크기에 대한 제한이 있습니다.

<br>

| 플랫폼 | 제한 | 성격 | 초과 시 대응 |
|--------|------|------|-------------|
| **Google Play** | AAB 기본 설치 200MB | 하드 제한 (초과 시 업로드 불가) | Play Asset Delivery로 에셋 분리 |
| **App Store** | 200MB | 셀룰러 다운로드 경고 임계값 | On-Demand Resources, App Thinning |

<br>

두 플랫폼 모두 200MB가 기준선이지만 성격이 다릅니다. Android는 이 크기를 초과하면 Play Asset Delivery 없이는 스토어에 업로드할 수 없고, iOS는 셀룰러 네트워크에서 다운로드 경고가 표시되어 설치를 포기하는 사용자가 늘어납니다. 앱 크기를 가능한 한 줄이는 것이 사용자 획득에 직접적인 영향을 미칩니다.

<br>

### 텍스처 압축

에셋 중에서도 가장 큰 비중을 차지하는 것은 텍스처입니다. 텍스처 압축 포맷 자체는 [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 다루었고, 빌드 크기 관점에서 핵심은 **ASTC(Adaptive Scalable Texture Compression)**입니다.

<br>

동일한 1024×1024 RGBA 텍스처 기준으로 포맷별 크기 차이는 다음과 같습니다.

| 포맷 | 크기 | 압축비 |
|------|------|--------|
| 비압축 (RGBA 32bit) | 4MB | — |
| ETC2 | 1MB | 4:1 |
| ASTC 6×6 | 0.45MB | 약 9:1 |
| ASTC 8×8 | 0.25MB | 약 16:1 |

ASTC는 블록 크기를 선택할 수 있습니다. 블록이 클수록 압축률이 높아지지만 품질이 떨어지므로, 용도에 따라 블록 크기를 달리 설정합니다.

| 용도 | 권장 블록 | 이유 |
|------|----------|------|
| 노멀맵 | 4×4 ~ 5×5 | 법선 벡터의 디테일 보존 |
| UI 스프라이트 | 4×4 | 선명한 경계선 유지 |
| 일반 텍스처 | 6×6 | 품질과 크기의 균형 |
| 배경 / 디퓨즈 | 6×6 ~ 8×8 | 디테일 손실이 눈에 덜 띔 |

<br>

### 오디오 압축

텍스처 다음으로 빌드 크기에 영향을 주는 에셋이 오디오입니다. 빌드 크기의 10~20%를 차지하는 경우도 있으므로, 클립 길이와 용도에 따라 Import Settings의 압축 방식과 로드 방식을 구분해서 설정합니다.

<br>

| 클립 길이 | Load Type | Compression | 효과 |
|-----------|-----------|-------------|------|
| 1초 미만 (효과음) | Decompress On Load | ADPCM 또는 PCM | 재생 지연 없음, 메모리에 상주 |
| 1~10초 | Compressed In Memory | Vorbis (Quality 40~60%) | 메모리 절약 + 빠른 재생 |
| 10초 이상 (배경음) | Streaming | Vorbis (Quality 30~50%) | 메모리 최소 사용 (버퍼만 유지) |

공통적으로, 모바일에서 스테레오가 불필요한 효과음은 **Force To Mono**를 활성화하면 크기가 50% 줄어듭니다. 음악 외 효과음은 Sample Rate를 22050Hz로 낮춰도 품질 차이가 거의 느껴지지 않습니다.

<br>

### 메쉬 압축

메쉬도 정점 수가 많은 모델이 쌓이면 빌드 크기에 영향을 줍니다. Unity의 Import Settings에서 Mesh Compression을 Low/Medium/High로 설정하면, 양자화(Quantization) 방식으로 정점 위치, 노멀, UV 좌표의 값을 더 적은 비트로 근사하여 메쉬 데이터 크기를 줄입니다. High 설정에서는 메쉬 데이터가 40~80% 줄어드는 경우가 일반적입니다. 다만 높은 압축률에서는 정점 위치에 미세한 오차가 생길 수 있으므로, 시각적으로 확인한 뒤 적용합니다.

압축과 별도로, 처음부터 불필요한 정점 데이터를 Import에서 제외하는 방법도 있습니다. 탄젠트는 정점당 16바이트, 노멀은 12바이트, 두 번째 UV는 8바이트를 차지합니다. 10,000개 정점의 메쉬에서 탄젠트와 두 번째 UV를 제외하면 약 240KB가 절약됩니다. 노멀맵을 사용하지 않는 오브젝트에서 탄젠트를 제외하고, 라이트맵을 사용하지 않는 오브젝트에서 두 번째 UV를 제외하는 것이 기본 원칙입니다.

<br>

---

## Play Asset Delivery와 On-Demand Resources

텍스처, 오디오, 메쉬를 압축해도 앱 크기가 플랫폼 제한(Google Play AAB 200MB, iOS 셀룰러 다운로드 200MB)을 초과할 수 있습니다. 이 경우 에셋 일부를 초기 설치에서 분리하여 나중에 다운로드하는 방식을 사용합니다. [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 Addressables를 통한 온디맨드 다운로드를 다루었는데, 이와 별도로 플랫폼 자체가 제공하는 공식 에셋 전달 메커니즘도 있습니다.

<br>

```
Play Asset Delivery (Android) — 전달 모드

install-time
  APK/AAB와 함께 설치, 사용자가 기다리는 시간에 포함
  필수 에셋에 사용, 스토어 표시 크기에 포함됨
  install-time 팩 전체 합산 200MB 이내

fast-follow
  설치 완료 직후 백그라운드에서 자동 다운로드
  앱을 처음 열었을 때 이미 받아져 있을 가능성이 높음
  메인 콘텐츠에 적합

on-demand
  앱이 요청할 때만 다운로드
  확장 콘텐츠, 이벤트 등에 적합
  다운로드 진행률 UI 필요


iOS On-Demand Resources
  태그 기반 → 에셋에 태그를 부여하고, 앱이 태그를 요청하면 App Store에서 다운로드
  사용 완료 후 시스템이 자동 정리 가능
```

<br>

Addressables만 단독으로 사용하면, 에셋 번들을 호스팅할 CDN 서버를 직접 준비하고 운영해야 합니다. Play Asset Delivery나 On-Demand Resources는 Google Play / App Store가 에셋 호스팅과 다운로드를 대신 처리하므로 별도 서버가 필요 없습니다.

두 방식을 결합할 수도 있습니다. Addressables만 쓰면 에셋 번들 파일을 CDN 서버에 올려두고, 앱이 그 서버에서 다운로드합니다. Play Asset Delivery와 결합하면, 같은 에셋 번들 파일을 CDN 대신 Google Play 스토어가 배포합니다. 게임 코드에서는 `Addressables.LoadAssetAsync("무기_텍스처")` 같은 호출을 동일하게 사용하고, 그 파일이 CDN에서 오는지 Google Play에서 오는지는 빌드 설정에 따라 달라집니다.

<br>

---

## Build Report로 빌드 크기 점검하기

빌드 크기는 한 번 줄여 놓고 끝나는 것이 아니라, 에셋이 추가될 때마다 다시 확인해야 합니다. Unity 에디터의 **Build Report**(빌드 완료 후 Console 로그에 표시)에서 에셋 유형별 크기 비중을 확인할 수 있습니다.

<br>

```
빌드 리포트 예시 (개략적)

카테고리          크기       비중
──────────────────────────────────────────
텍스처            45MB       55%
오디오            15MB       18%
메쉬              8MB        10%
셰이더            5MB        6%
코드 (IL2CPP)     4MB        5%
애니메이션        3MB        4%
기타              2MB        2%
──────────────────────────────────────────
합계              82MB       100%

→ 텍스처가 절반 이상을 차지
→ ASTC 압축 포맷과 밉맵 레벨 확인이 우선
→ 불필요한 텍스처가 빌드에 포함되어 있지 않은지 확인
```

<br>

빌드에 포함되지 말아야 할 에셋(개발용 텍스처, 테스트 프리팹, 사용하지 않는 폰트 등)이 포함되어 있는 경우가 빌드 크기 증가의 흔한 원인입니다. Resources 폴더에 넣은 에셋은 사용 여부와 관계없이 모두 빌드에 포함되므로, Resources 폴더 대신 Addressables를 사용하는 것이 크기 관리에도 유리합니다.

<br>

---

## 전체 시리즈 통합 — 프레임 하나의 여정

지금까지 29편에 걸쳐 Unity 모바일 최적화의 각 영역을 개별적으로 다루었습니다. 아래 다이어그램은 프레임 하나가 시작되어 화면에 표시되기까지의 여정을 따라가면서, 각 단계에 대응하는 시리즈 글을 함께 표기한 것입니다.

<br>

```
프레임 하나의 여정과 시리즈 매핑

프레임 시작
    │
    ├── 입력 처리
    │     터치/가속도계 입력 수신
    │
    ├── FixedUpdate (물리)
    │     충돌 감지, 강체 시뮬레이션
    │     ← PhysicsOptimization (1)(2)
    │       콜라이더 단순화, 레이어 매트릭스, 물리 오브젝트 수 관리
    │
    ├── Update (스크립트 로직)
    │     게임플레이 코드, AI, 상태 머신
    │     ← ScriptOptimization (1)(2)
    │       GC 할당 최소화, 캐싱, 오브젝트 풀링
    │     ← MemoryManagement (1)(2)(3)
    │       가비지 컬렉션, Addressables
    │
    ├── LateUpdate (애니메이션, 카메라)
    │     Animator 평가, 본 변환, 카메라 추적
    │     ← ParticleAndAnimation (2)
    │       Animator 최적화, Culling Mode
    │
    ├── UI 업데이트
    │     Canvas 리빌드, 레이아웃 계산
    │     ← UIOptimization (1)(2)
    │       Canvas 분리, ScrollRect 풀링, TextMeshPro, Raycast Target
    │
    ├── 렌더링 준비 (CPU)
    │     컬링: 카메라 밖 오브젝트 제거
    │     정렬: 불투명(앞→뒤), 반투명(뒤→앞)
    │     배칭: SRP Batcher, 정적/동적 배칭
    │     커맨드 버퍼 구성
    │     ← UnityPipeline (1)(2)(3)
    │       URP 구조, 드로우콜 배칭, 컬링 전략
    │
    ├── GPU 제출 및 렌더링
    │
    │     정점 셰이더 실행
    │       메쉬 정점 변환, 스키닝
    │       ← RenderingFoundation (1)
    │
    │     래스터라이징
    │       삼각형 → 프래그먼트
    │
    │     프래그먼트 셰이더 실행
    │       텍스처 샘플링, 라이팅 계산
    │       ← RenderingFoundation (2)(3)
    │       ← ShaderOptimization (1)(2)
    │       ← LightingAndShadows (1)(2)
    │
    │     TBDR 타일 처리 (모바일)
    │       ← GPUArchitecture (1)(2)
    │
    │     파티클 렌더링
    │       ← ParticleAndAnimation (1)
    │
    ├── 후처리 (Post-Processing)
    │     Bloom, Color Grading, Anti-Aliasing
    │     ← LightingAndShadows (2)
    │     ← ShaderOptimization (2)
    │
    ├── Present (화면 표시)
    │     VSync 대기, 프레임 버퍼 교체
    │     ← GameLoop (1)(2)
    │       프레임 구조, VSync, 프레임 페이싱
    │
    ▼
프레임 완료


전체를 관통하는 제약:

  서멀 쓰로틀링, 전력 예산, 디바이스 티어
  ← MobileStrategy (1)(2)

  프로파일링으로 병목 위치 파악
  ← Profiling (1)(2)
```

<br>

다이어그램의 각 단계는 서로 독립적이지 않고, 한 단계의 비용이 다른 단계에 영향을 미칩니다. 스크립트에서 너무 많은 오브젝트를 생성하면 가비지 컬렉션 스파이크가 발생하여 렌더링 준비 단계의 시작이 지연됩니다. 그림자를 고해상도로 렌더링하면 GPU가 다른 렌더링 작업에 착수하는 시점이 늦어지고, UI Canvas가 매 프레임 리빌드되면 CPU 예산의 상당 부분이 UI에 소비되어 스크립트 로직의 여유가 줄어듭니다.

최적화는 이 파이프라인에서 **가장 느린 단계**를 찾아 개선하는 과정입니다. [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)에서 다룬 프로파일러가 이 "가장 느린 단계"를 알려 줍니다. [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)에서 다룬 병목 판별이 CPU와 GPU 중 어느 쪽을 먼저 최적화할지 결정해 줍니다.

한쪽 병목을 해소하면 다른 쪽이 새로운 병목이 됩니다. CPU를 최적화하면 GPU가 병목이 되고, GPU를 최적화하면 다시 CPU가 병목이 됩니다. 이 과정을 반복하면서 프레임 시간을 목표 예산 이내로 줄이고, [모바일 전략 (1)](/dev/unity/MobileStrategy-1/)에서 다룬 지속 성능 기준으로 안정성을 검증합니다.

<br>

---

## 마무리

[게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)에서 프레임 하나의 구조를 이해하는 것으로 시작하여, 렌더링 데이터의 구조, GPU의 동작 원리, Unity 렌더 파이프라인, 스크립트와 메모리 관리, UI, 조명, 셰이더, 물리, 파티클, 애니메이션, 프로파일링, 그리고 모바일 특유의 발열/배터리/빌드 전략까지, 29편에 걸쳐 하나의 프레임이 만들어지는 전 과정을 다루었습니다.

<br>

최적화는 프레임에서 가장 느린 단계를 찾고, 그 단계의 원리를 이해하고, 원리에 맞는 방법을 적용하는 과정입니다. 프레임 하나가 어떻게 만들어지는지 이해하면 병목이 보이고, 병목이 보이면 최적화가 보입니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)

**시리즈**
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- **모바일 전략 (2) - 빌드와 품질 전략** (현재 글)

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
- [셰이더 최적화 (2) - 셰이더 배리언트와 모바일 기법](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- **모바일 전략 (2) - 빌드와 품질 전략** (현재 글)
