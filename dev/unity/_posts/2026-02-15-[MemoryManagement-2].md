---
layout: single
title: "메모리 관리 (2) - 네이티브 메모리와 에셋 - soo:bak"
date: "2026-02-15 23:33:00 +0900"
description: 네이티브 메모리 구조, 에셋 생명주기, Resources.Load, 모바일 메모리 예산, 메모리 단편화를 설명합니다.
tags:
  - Unity
  - 최적화
  - 메모리
  - 에셋
  - 모바일
---

## 관리 힙 너머의 메모리

Unity 게임의 메모리 대부분은 텍스처, 메쉬, 오디오 클립, 셰이더, 애니메이션 클립 같은 **에셋 데이터**가 차지합니다.
이 에셋은 C# 관리 힙이 아닌 **네이티브 메모리(Native Memory)**에 로드되며, Unity 엔진의 C++ 코어가 관리합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 110" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- 네이티브 메모리 바 -->
  <rect x="20" y="15" width="430" height="30" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="35" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">네이티브 메모리</text>
  <text x="170" y="35" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">텍스처, 메쉬, 오디오, 셰이더 등</text>
  <text x="445" y="35" text-anchor="end" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">70~90%</text>

  <!-- 관리 힙 바 -->
  <rect x="20" y="55" width="120" height="30" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="30" y="75" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">관리 힙</text>
  <text x="148" y="75" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">10~30% — C# 객체, 배열, 문자열 등</text>

  <!-- 결론 -->
  <text x="260" y="105" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">→ 메모리 대부분은 네이티브 영역의 에셋</text>

</svg>
</div>

모바일에서 메모리 부족으로 앱이 강제 종료될 때, 대부분은 관리 힙이 아니라 네이티브 메모리에 로드된 에셋 때문입니다.

---

## 네이티브 메모리의 구조

네이티브 메모리 사용량은 에셋 유형별로 크게 다릅니다.

| 에셋 유형 | 비중 |
|-----------|------|
| 텍스처 | 50~70% |
| 오디오, 셰이더, 기타 | 15~30% |
| 메쉬 버퍼 | 5~15% |

<br>

### 텍스처 — 가장 큰 비중

텍스처는 모바일 게임에서 메모리를 가장 많이 소비하는 에셋이며, 그 크기는 **해상도 x 포맷(bpp, bit per pixel) x 밉맵 계수**로 결정됩니다.

$$\text{텍스처 메모리} = \text{가로} \times \text{세로} \times \frac{\text{bpp}}{8} \times \text{밉맵 계수}$$

<br>

[텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 다룬 **밉맵(Mipmap)**을 활성화하면 축소 버전들이 추가되어 메모리가 약 $1.33$배가 됩니다.

$2048 \times 2048$, **ASTC(Adaptive Scalable Texture Compression)** 6x6 ($3.56\;\text{bpp}$), 밉맵 ON인 텍스처의 경우:

$$2048 \times 2048 \times \frac{3.56}{8} \times 1.33 \approx 2.37\;\text{MB}$$

<br>

텍스처 데이터는 GPU가 렌더링 중에 직접 읽어야 하므로 GPU 전용 메모리인 **VRAM(Video RAM)**에 로드됩니다.

PC에서는 시스템 RAM과 VRAM이 분리되어 있어 텍스처가 시스템 메모리에 영향을 주지 않습니다.
반면 모바일 기기는 CPU와 GPU가 같은 물리 메모리를 공유하는 **통합 메모리 아키텍처(Unified Memory Architecture, UMA)**를 사용하므로, 텍스처가 차지하는 만큼 다른 용도에 사용할 수 있는 메모리가 줄어듭니다.

캐릭터, 배경, 이펙트에 사용되는 텍스처를 합치면 수백 MB에 달하는 경우가 흔합니다. PBR 렌더링 기준으로 캐릭터 한 명에만 색상(Diffuse), 표면 굴곡(Normal), 재질(Mask) 등 최소 3장이 필요하기 때문입니다. 해상도를 낮추거나 bpp가 낮은 압축 포맷을 사용하는 것이 가장 효과적인 절감 방법입니다.

<br>

### 메쉬 — 정점 버퍼와 인덱스 버퍼

메쉬는 [메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 다룬 정점 버퍼(Vertex Buffer)와 인덱스 버퍼(Index Buffer)로 GPU 메모리에 올라가며, 그 크기는 정점 수, 정점 속성 구성, 삼각형 수에 따라 달라집니다.

$$\text{메쉬 메모리} = (\text{정점 수} \times \text{정점당 바이트}) + (\text{삼각형 수} \times 3 \times \text{인덱스 크기})$$

정점 10,000개, 삼각형 18,000개, 속성 48바이트/정점, 16비트 인덱스인 메쉬의 경우:

$$\begin{aligned}
&(10{,}000 \times 48) + (18{,}000 \times 3 \times 2) \\
&= 480{,}000 + 108{,}000 \\
&= 588{,}000\;\text{바이트} \approx 574\;\text{KB}
\end{aligned}$$

<br>

**Read/Write Enabled** 옵션도 메쉬 메모리에 큰 영향을 줍니다.
이 옵션이 켜져 있으면 GPU용 메쉬 데이터 외에 CPU가 접근할 수 있는 복사본이 추가로 할당되어 메모리가 2배가 됩니다.
런타임에 정점을 수정하는 경우(Procedural Mesh, Cloth 시뮬레이션 등)에만 필요하므로, 수정하지 않는 메쉬에서는 끄는 것이 좋습니다.

<br>

**위 메쉬(574 KB)에 Read/Write Enabled를 적용한 경우**

| 설정 | 할당 | 합계 |
|------|------|------|
| 꺼짐 (기본, 권장) | GPU 버퍼 574 KB | 574 KB |
| 켜짐 | GPU 버퍼 574 KB + CPU 복사본 574 KB | 1,148 KB (2배) |

<br>

### 오디오 — 로딩 방식에 따른 메모리 차이

오디오 클립은 디스크에 압축 형태(Vorbis, AAC 등)로 저장되지만, 메모리에 로드하는 방식에 따라 사용량이 크게 달라집니다.
압축 상태를 유지한 채 로드할 수도 있고, **PCM(원본 파형 데이터)**으로 풀어서 올릴 수도 있기 때문입니다.

| 로딩 모드 | 동작 방식 | 메모리 | CPU |
|-----------|-----------|--------|-----|
| Decompress On Load | 로드 시 전체 클립을 비압축 PCM으로 메모리에 올림 | 최대 | 최소 |
| Compressed In Memory | 압축 상태로 메모리에 올리고, 재생 시 실시간 디코딩 | 중간 | 약간 증가 |
| Streaming | 작은 버퍼만 유지하고 디스크에서 조금씩 읽으며 재생 | 최소 | I/O 발생 |

<br>

1분짜리 스테레오 오디오(44.1kHz, 16bit)의 비압축 PCM 크기:

$$44{,}100 \times 2\;\text{채널} \times 2\;\text{바이트} \times 60\;\text{초} = 10{,}584{,}000\;\text{바이트} \approx 10.1\;\text{MB}$$

Vorbis 압축 (Quality 70%)을 적용하면 약 $1.0 \sim 1.5\;\text{MB}$ 입니다.

<br>

**위 클립(1분, 스테레오)을 각 모드로 로드한 경우**

| 로딩 모드 | 메모리 사용량 | 비고 |
|-----------|-------------|------|
| Decompress On Load | 약 10.1 MB | 비압축 전체 |
| Compressed In Memory | 약 1.2 MB | 압축 상태 |
| Streaming | 약 0.2 MB | 버퍼만 |

<br>

클립의 길이와 재생 방식에 따라 적합한 모드가 달라집니다.

| 클립 유형 | 권장 모드 | 이유 |
|-----------|-----------|------|
| 짧은 효과음 (총소리, 발걸음) | Decompress On Load | 비압축 크기가 작고 재생 빈도가 높아 CPU 부담 감소 |
| BGM (길고 단일 재생) | Streaming | 메모리 최소, 단일 스트림이라 I/O 부담도 적음 |
| 음성 (대사, 내레이션) | Compressed In Memory | 비압축하기엔 길고, 스트리밍하기엔 동시 재생 시 I/O 과다 |

<br>

### 셰이더 — variant 수에 비례하는 메모리

셰이더 소스 코드 자체는 작지만, 빌드 시 키워드 조합에 따라 **variant(변형)**가 생성됩니다.
안개 ON/OFF, 그림자 ON/OFF처럼 각 키워드 조합마다 별개의 바이너리가 만들어지고, 각각이 메모리를 차지합니다.

ON/OFF 키워드가 3개이면 $2^3 = 8$개, 10개이면 $2^{10} = 1{,}024$개의 variant가 생성됩니다.
실제로 유효한 조합은 일부이지만, 관리하지 않으면 variant가 수천~수만 개로 늘어날 수 있습니다.

variant 하나의 크기는 플랫폼과 셰이더 복잡도에 따라 다릅니다. 예를 들어 간단한 Unlit 셰이더는 약 2~4 KB이지만 PBR 셰이더는 20~50 KB에 달합니다. variant가 1,000개인 PBR 셰이더라면 셰이더 하나만으로 20~50 MB를 차지합니다.

이 중 불필요한 variant는 빌드 과정의 **셰이더 variant stripping**으로 제거할 수 있습니다.

Unity가 프로젝트의 Graphics Settings와 머티리얼을 분석하여 어떤 머티리얼도 사용하지 않는 키워드 조합의 variant를 자동으로 제거하므로, 메모리와 빌드 크기가 동시에 줄어듭니다.

### 애니메이션 클립 — 키프레임 데이터

애니메이션 클립은 시간에 따른 프로퍼티 변화를 키프레임(Keyframe)으로 저장하며, 뼈대(Bone) 수와 키프레임 밀도에 비례하여 크기가 커집니다.

$$\text{클립 크기} = \text{뼈대 수} \times \text{키프레임 수} \times \text{프로퍼티당 바이트}$$

60개 뼈대, 초당 30 키프레임, 3초 클립(총 90 키프레임)의 경우:

$$\begin{aligned}
&60 \times 90 \times (\underbrace{12}_{\text{위치}} + \underbrace{16}_{\text{회전}}) \\
&= 60 \times 90 \times 28 \\
&= 151{,}200\;\text{바이트} \approx 148\;\text{KB}\;\text{(비압축 시)}
\end{aligned}$$

<br>

캐릭터가 많고 애니메이션이 다양한 게임에서는 비압축 클립의 총 메모리가 수십 MB에 이르므로, 애니메이션 압축이 중요합니다.

압축 방식 중 **Keyframe Reduction**은 보간으로 복원 가능한 중간 키프레임을 제거합니다. 원본이 초당 30 키프레임이라도 방향이 바뀌는 지점만 남기면 충분한 경우가 많습니다.
또 다른 방식인 **Optimal** 모드는 여기에 커브 근사와 정밀도 축소까지 조합하여, 시각적 품질 손실을 최소화하면서 클립 크기를 50~80% 줄입니다.

---

## 에셋 생명주기 — 로딩, 참조, 해제

에셋이 언제 메모리에 올라가고 어떤 조건에서 해제되는지에 따라 실제 메모리 사용량이 달라집니다.

| 단계 | 설명 |
|------|------|
| 로딩 (Load) | 디스크/번들에서 메모리로 읽어옴 |
| 참조 (Use) | 게임에서 사용 중, 메모리에 유지 |
| 해제 (Unload) | 참조가 없어지면 메모리에서 제거 가능 |

<br>

에셋이 메모리에 올라가는 시점과 해제되는 조건은 로드 방식에 따라 달라집니다.
로드 방식은 씬에서 직접 참조하는 방식과 코드에서 명시적으로 로드하는 방식으로 나뉩니다.

### 씬 직접 참조

MonoBehaviour의 public 필드나 `[SerializeField]`에 에셋을 드래그 앤 드롭으로 연결하면, 해당 에셋은 씬이 로드될 때 함께 메모리에 올라갑니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 370" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 직접 참조의 생명주기</text>

  <!-- === 씬 로드 시 === -->
  <text x="20" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 로드 시</text>

  <!-- Scene A box -->
  <rect x="30" y="68" width="100" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="80" y="92" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Scene A</text>

  <!-- Arrow to 캐릭터 프리팹 -->
  <line x1="130" y1="78" x2="185" y2="78" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="185,74 193,78 185,82" fill="currentColor"/>

  <!-- 캐릭터 프리팹 box -->
  <rect x="195" y="63" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">캐릭터 프리팹</text>

  <!-- Sub-assets: 텍스처 A -->
  <line x1="315" y1="72" x2="350" y2="62" stroke="currentColor" stroke-width="1"/>
  <polygon points="347,58 355,60 349,65" fill="currentColor"/>
  <rect x="357" y="48" width="68" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="391" y="63" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">텍스처 A</text>

  <!-- Sub-assets: 메쉬 A -->
  <line x1="315" y1="78" x2="350" y2="78" stroke="currentColor" stroke-width="1"/>
  <polygon points="350,75 357,78 350,81" fill="currentColor"/>
  <rect x="357" y="73" width="68" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="391" y="88" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">메쉬 A</text>

  <!-- Sub-assets: 머티리얼 A -->
  <line x1="315" y1="84" x2="350" y2="94" stroke="currentColor" stroke-width="1"/>
  <polygon points="347,97 355,96 349,91" fill="currentColor"/>
  <rect x="357" y="98" width="78" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="396" y="113" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">머티리얼 A</text>

  <!-- Arrow to 배경 오브젝트 -->
  <line x1="130" y1="98" x2="185" y2="133" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="182,129 190,135 184,137" fill="currentColor"/>

  <!-- 배경 오브젝트 box -->
  <rect x="195" y="125" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="255" y="144" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">배경 오브젝트</text>

  <!-- Sub-asset: 텍스처 B -->
  <line x1="315" y1="140" x2="350" y2="140" stroke="currentColor" stroke-width="1"/>
  <polygon points="350,137 357,140 350,143" fill="currentColor"/>
  <rect x="357" y="129" width="68" height="22" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="391" y="144" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">텍스처 B</text>

  <!-- Result label -->
  <text x="260" y="178" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 참조된 에셋이 모두 메모리에 로드됨</text>

  <!-- Divider -->
  <line x1="20" y1="192" x2="500" y2="192" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- === 씬 언로드 시 === -->
  <text x="20" y="215" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">씬 언로드 시</text>

  <!-- Scene A (unloading, dashed) -->
  <rect x="30" y="228" width="100" height="40" rx="5" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="80" y="252" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">Scene A</text>

  <!-- Arrow down -->
  <line x1="80" y1="268" x2="80" y2="288" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="76,288 80,296 84,288" fill="currentColor"/>

  <!-- Ref count box -->
  <rect x="20" y="298" width="160" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="317" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">참조 카운트 감소</text>

  <!-- Arrow -->
  <line x1="180" y1="313" x2="215" y2="313" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="215,309 223,313 215,317" fill="currentColor"/>

  <!-- Decision -->
  <rect x="225" y="298" width="120" height="30" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="285" y="317" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">카운트 = 0 ?</text>

  <!-- Arrow -->
  <line x1="345" y1="313" x2="380" y2="313" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="380,309 388,313 380,317" fill="currentColor"/>

  <!-- UnloadUnusedAssets box -->
  <rect x="390" y="293" width="115" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="447" y="311" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">UnloadUnused</text>
  <text x="447" y="324" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">Assets 시 해제</text>

  <!-- Bottom note -->
  <text x="260" y="358" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 참조가 끊긴 뒤, 다음 씬 전환 시 자동 해제 (UnloadUnusedAssets)</text>
</svg>
</div>

씬이 언로드되면 해당 씬에서 참조하던 에셋의 **참조 카운트(Reference Count)**가 감소합니다.
참조 카운트란 해당 에셋을 현재 사용하고 있는 곳이 몇 개인지를 추적하는 값입니다. 다른 씬이나 코드에서 같은 에셋을 참조하고 있지 않다면, 참조 카운트가 0이 되어 그 에셋은 "미사용 상태"가 됩니다.
Unity는 씬 전환 시 내부적으로 `Resources.UnloadUnusedAssets()`를 호출하여 미사용 에셋을 메모리에서 해제합니다.

이처럼 씬 직접 참조에서는 별도의 로딩 코드 없이 에셋이 씬과 함께 로드되고, 씬이 해제되면 자동으로 정리됩니다. 다만 씬이 로드될 때 참조된 모든 에셋이 한꺼번에 올라오므로, 참조가 많으면 로딩 시 메모리 피크가 높아집니다.

### Resources.Load

씬 참조와 달리 `Resources.Load()`는 `Resources` 폴더에 넣어둔 에셋을 코드에서 필요한 시점에 디스크에서 읽어 메모리에 올립니다. 이미 로드된 에셋을 다시 요청하면 중복 로드 없이 캐시된 인스턴스를 반환합니다.

```csharp
Texture2D tex = Resources.Load<Texture2D>("Textures/CharacterSkin");

tex = null;

Resources.UnloadUnusedAssets();
```

`Resources.Load()`로 로드한 에셋은 C# 참조가 남아 있는 한 메모리에 유지됩니다. 변수를 `null`로 설정하거나, 컬렉션에서 제거하거나, 에셋을 참조하는 GameObject를 Destroy하는 등 모든 참조를 끊은 뒤 `Resources.UnloadUnusedAssets()`를 호출하면 해당 에셋이 메모리에서 해제됩니다.

특정 에셋 하나를 즉시 해제하고 싶다면 `Resources.UnloadAsset(asset)`을 사용할 수 있지만, 다른 곳에서 해당 에셋을 아직 참조하고 있으면 텍스처가 분홍색으로 표시되는 등 렌더링 오류가 발생할 수 있습니다.

<br>

`Resources.Load()`는 런타임에 문자열 경로로 에셋을 찾기 때문에, 빌드 시점에는 어떤 에셋이 실제로 로드될지 엔진이 판단할 수 없습니다. 그래서 `Resources` 폴더 안의 **모든 에셋**이 빌드에 포함되며, 불필요한 에셋이 폴더에 남아 있으면 빌드 크기가 커집니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 400" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <!-- Title -->
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Resources 폴더의 빌드 포함 문제</text>

  <!-- Project structure label -->
  <text x="30" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프로젝트 구조</text>

  <!-- Assets/ -->
  <text x="40" y="76" font-family="sans-serif" font-size="11" fill="currentColor">Assets/</text>

  <!-- Resources/ -->
  <line x1="50" y1="82" x2="50" y2="96" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="50" y1="96" x2="62" y2="96" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="66" y="100" font-family="sans-serif" font-size="11" fill="currentColor">Resources/</text>

  <!-- Textures/ -->
  <line x1="76" y1="106" x2="76" y2="120" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="76" y1="120" x2="88" y2="120" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="92" y="124" font-family="sans-serif" font-size="11" fill="currentColor">Textures/</text>

  <!-- CharacterSkin.png (used) -->
  <line x1="102" y1="130" x2="102" y2="144" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="102" y1="144" x2="114" y2="144" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <rect x="114" y="133" width="150" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="122" y="147" font-family="sans-serif" font-size="9.5" fill="currentColor">CharacterSkin.png</text>
  <text x="290" y="147" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">게임에서 사용</text>

  <!-- OldCharacterSkin.png (unused) -->
  <line x1="102" y1="144" x2="102" y2="168" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="102" y1="168" x2="114" y2="168" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <rect x="114" y="157" width="150" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="122" y="171" font-family="sans-serif" font-size="9.5" fill="currentColor" opacity="0.5">OldCharacterSkin.png</text>
  <text x="290" y="171" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">사용하지 않음</text>

  <!-- TestTexture.png (unused) -->
  <line x1="102" y1="168" x2="102" y2="192" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="102" y1="192" x2="114" y2="192" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <rect x="114" y="181" width="150" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="122" y="195" font-family="sans-serif" font-size="9.5" fill="currentColor" opacity="0.5">TestTexture.png</text>
  <text x="290" y="195" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">사용하지 않음</text>

  <!-- Audio/ -->
  <line x1="76" y1="120" x2="76" y2="220" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="76" y1="220" x2="88" y2="220" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <text x="92" y="224" font-family="sans-serif" font-size="11" fill="currentColor">Audio/</text>

  <!-- BGM_01.ogg (used) -->
  <line x1="102" y1="230" x2="102" y2="244" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="102" y1="244" x2="114" y2="244" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <rect x="114" y="233" width="150" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="122" y="247" font-family="sans-serif" font-size="9.5" fill="currentColor">BGM_01.ogg</text>
  <text x="290" y="247" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">게임에서 사용</text>

  <!-- BGM_Unused.ogg (unused) -->
  <line x1="102" y1="244" x2="102" y2="268" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <line x1="102" y1="268" x2="114" y2="268" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <rect x="114" y="257" width="150" height="20" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="122" y="271" font-family="sans-serif" font-size="9.5" fill="currentColor" opacity="0.5">BGM_Unused.ogg</text>
  <text x="290" y="271" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">사용하지 않음</text>

  <!-- Divider -->
  <line x1="30" y1="295" x2="590" y2="295" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.3"/>

  <!-- Build result label -->
  <text x="30" y="322" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">빌드 결과</text>

  <!-- Result box -->
  <rect x="30" y="332" width="560" height="55" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="50" y="352" font-family="sans-serif" font-size="10" fill="currentColor">위 5개 에셋 모두 빌드에 포함됨</text>
  <text x="50" y="368" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">→ 빌드 크기 증가 / Resources 폴더의 색인(lookup table) 크기 증가 / 앱 시작 시 색인 로딩 시간 증가</text>
</svg>
</div>

에셋이 많아질수록 빌드 크기뿐 아니라 앱 시작 시간과 메모리 사용량도 함께 증가합니다. 이러한 구조적 한계 때문에 Unity 공식 문서에서도 Resources 시스템은 프로토타이핑 등 제한된 용도 외에는 사용하지 않도록 권장하고 있습니다.

### 직접 참조 vs Resources.Load

| 항목 | 씬 직접 참조 | Resources.Load |
|------|-------------|----------------|
| 로드 시점 | 씬 로드 시 자동 | 코드에서 명시적 호출 |
| 해제 시점 | 씬 언로드 시 자동(UnloadUnused) | 수동(UnloadUnusedAssets 호출 필요) |
| 빌드 포함 기준 | 실제 참조된 에셋만 포함 | Resources 폴더의 모든 에셋 포함 |
| 빌드 크기 | 최소화 | 불필요한 에셋까지 포함되어 증가 가능 |
| 메모리 관리 | 씬 단위 자동 관리(비교적 단순) | 개발자가 수동 관리(복잡) |
| 적합한 경우 | 씬에 종속된 에셋 | 동적 로딩이 필요한 에셋(제한적 사용) |

<br>

씬 직접 참조에서는 Unity 엔진이 빌드 시 에셋의 참조 관계를 분석할 수 있으므로, 실제로 참조된 에셋만 빌드에 포함합니다.

빌드 포함 범위를 더 세밀하게 통제할 수 있는 AssetBundle과 Addressables는 [메모리 관리 (3)](/dev/unity/MemoryManagement-3/)에서 다룹니다.

---

## 모바일 메모리 예산

개별 에셋을 최적화하더라도 전체 메모리 사용량은 기기의 허용 한계를 넘을 수 있습니다.

PC에서는 메모리 여유가 상대적으로 넉넉하지만, 모바일에서는 OS가 앱의 메모리 사용량을 감시하고, 한계를 초과한 앱을 강제 종료합니다.

메모리 압박으로 인한 이러한 강제 종료를 통칭하여 **OOM(Out of Memory) Kill**이라 하며, iOS와 Android 모두에서 발생합니다.

### iOS

iOS에서는 별도의 경고나 예외 없이 즉시 종료되므로, 사용자에게는 앱이 갑자기 꺼진 것으로 보입니다.

앱에 허용되는 정확한 한계는 공개되어 있지 않으며 OS 버전과 시스템 상태에 따라 달라지지만, 일반적으로 물리 RAM의 50~65%를 앱이 사용할 수 있습니다. 타깃 기기의 최소 RAM에 이 비율을 적용하여 메모리 예산을 산출합니다.

### Android — 기기 파편화

Android에서도 한계를 초과하면 강제 종료되는데, 기기 간 RAM 격차가 커서 고사양 기기에서 문제없이 동작하는 게임도 저사양 기기에서는 OOM Kill이 발생할 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">

  <!-- 범례 -->
  <rect x="110" y="10" width="12" height="12" rx="2" fill="currentColor" fill-opacity="0.2"/>
  <text x="126" y="20" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">OS + 시스템</text>
  <rect x="230" y="10" width="12" height="12" rx="2" fill="currentColor" fill-opacity="0.08"/>
  <text x="246" y="20" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">앱 가용 영역</text>

  <!-- 고사양 -->
  <text x="65" y="52" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">고사양</text>
  <rect x="75" y="38" width="100" height="24" rx="3" fill="currentColor" fill-opacity="0.2"/>
  <rect x="175" y="38" width="300" height="24" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <text x="325" y="54" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">앱 가용 영역 넓음</text>

  <!-- 중사양 -->
  <text x="65" y="102" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">중사양</text>
  <rect x="75" y="88" width="160" height="24" rx="3" fill="currentColor" fill-opacity="0.2"/>
  <rect x="235" y="88" width="165" height="24" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>

  <!-- 저사양 -->
  <text x="65" y="152" text-anchor="end" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">저사양</text>
  <rect x="75" y="138" width="220" height="24" rx="3" fill="currentColor" fill-opacity="0.2"/>
  <rect x="295" y="138" width="80" height="24" rx="3" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.2"/>
  <text x="420" y="154" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor" opacity="0.7">OOM 위험</text>

  <!-- 결론 -->
  <line x1="40" y1="185" x2="480" y2="185" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="260" y="205" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.5">→ 저사양일수록 OS가 차지하는 비중이 커져 앱 가용 메모리가 줄어듦</text>

</svg>
</div>

Android의 메모리 예산 산출 방식도 iOS와 동일하게 물리 RAM의 50~65%를 적용하지만, 지원 범위가 넓은 만큼 최저 사양 기기의 RAM을 기준으로 잡아야 합니다.

---

## 메모리 단편화

Boehm GC의 비압축(Non-compacting) 특성은 관리 힙에 **메모리 단편화(Memory Fragmentation)**를 일으킵니다.
빈 공간의 합계는 충분해도 연속된 공간이 부족하면 힙이 확장되고, 한 번 확장된 힙은 줄어들지 않습니다.

단편화는 관리 힙만의 문제가 아닙니다.
텍스처, 메쉬 등 에셋 데이터가 저장되는 네이티브 메모리는 Boehm GC가 아닌 Unity 엔진 내부의 C++ 할당기가 관리하는데, 이 할당기 역시 할당된 블록을 이동시켜 빈틈을 메우지 않으므로 네이티브 메모리에서도 단편화가 발생합니다.

### 네이티브 메모리의 단편화

네이티브 메모리에는 텍스처, 메쉬, 오디오 클립 등 크기가 각기 다른 에셋이 저장됩니다.
이 에셋들이 로드되고 해제되면서 다양한 크기의 빈 공간이 생기는데, 해제된 자리보다 큰 에셋은 그 자리에 들어갈 수 없어 빈 공간이 그대로 남습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 430" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">네이티브 메모리 단편화 시나리오</text>

  <!-- === Stage 1 === -->
  <text x="20" y="52" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 씬 A 로드: 텍스처 a, b, c 로드</text>

  <!-- a: 4MB (width ~60) -->
  <rect x="30" y="62" width="60" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">a</text>
  <text x="60" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">4MB</text>

  <!-- b: 8MB (width ~120) -->
  <rect x="90" y="62" width="120" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">b</text>
  <text x="150" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">8MB</text>

  <!-- c: 2MB (width ~30) -->
  <rect x="210" y="62" width="30" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">c</text>
  <text x="225" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">2MB</text>

  <!-- Free space -->
  <rect x="240" y="62" width="250" height="40" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="365" y="86" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">빈 공간</text>

  <!-- Arrow down -->
  <line x1="260" y1="110" x2="260" y2="130" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="256,130 260,138 264,130" fill="currentColor"/>

  <!-- === Stage 2 === -->
  <text x="20" y="158" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. 씬 B 전환: b 해제, 텍스처 d(10MB) 로드</text>

  <!-- a: 4MB -->
  <rect x="30" y="168" width="60" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">a</text>
  <text x="60" y="200" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">4MB</text>

  <!-- b freed: 8MB empty -->
  <rect x="90" y="168" width="120" height="40" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="150" y="186" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">빈칸</text>
  <text x="150" y="200" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">8MB</text>

  <!-- c: 2MB -->
  <rect x="210" y="168" width="30" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">c</text>
  <text x="225" y="200" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">2MB</text>

  <!-- d: 10MB (width ~150) -->
  <rect x="240" y="168" width="150" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="315" y="186" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">d</text>
  <text x="315" y="200" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">10MB</text>

  <!-- Remaining free -->
  <rect x="390" y="168" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="440" y="192" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">빈 공간</text>

  <!-- Annotation: d can't fit in 8MB gap -->
  <text x="150" y="224" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">d(10MB)는 8MB 빈칸에 못 들어감 → 뒤쪽에 배치</text>

  <!-- Arrow down -->
  <line x1="260" y1="234" x2="260" y2="254" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="256,254 260,262 264,254" fill="currentColor"/>

  <!-- === Stage 3 === -->
  <text x="20" y="282" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 텍스처 e(12MB) 로드 시도</text>

  <!-- a: 4MB -->
  <rect x="30" y="292" width="60" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="310" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">a</text>
  <text x="60" y="324" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">4MB</text>

  <!-- 8MB empty -->
  <rect x="90" y="292" width="120" height="40" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="150" y="310" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">빈칸</text>
  <text x="150" y="324" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">8MB</text>

  <!-- c: 2MB -->
  <rect x="210" y="292" width="30" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="225" y="310" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">c</text>
  <text x="225" y="324" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">2MB</text>

  <!-- d: 10MB -->
  <rect x="240" y="292" width="150" height="40" rx="4" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>
  <text x="315" y="310" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">d</text>
  <text x="315" y="324" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">10MB</text>

  <!-- Small remaining free -->
  <rect x="390" y="292" width="100" height="40" rx="4" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,3"/>
  <text x="440" y="316" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">빈 공간</text>

  <!-- e? annotation -->
  <text x="260" y="355" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">e(12MB): 빈칸 8MB + 뒤쪽 빈 공간의 합계는 충분하지만,</text>
  <text x="260" y="370" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.6">연속 12MB 공간이 없으면 단편화로 인한 할당 실패 가능</text>

  <!-- X marks on gaps to show they're not contiguous -->
  <line x1="88" y1="350" x2="212" y2="350" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.3"/>
  <line x1="388" y1="350" x2="492" y2="350" stroke="currentColor" stroke-width="1" stroke-dasharray="2,2" opacity="0.3"/>
  <text x="150" y="346" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">8MB</text>
  <text x="440" y="346" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.4">나머지</text>

  <!-- Not contiguous indicator -->
  <text x="300" y="412" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" font-weight="bold" opacity="0.5">← 연속되지 않음 →</text>
</svg>
</div>

네이티브 메모리 할당기는 나란히 비어 있는 블록을 하나로 합쳐 큰 공간을 만들 수 있어서, Boehm GC보다 단편화 완화에 유리합니다. 하지만 에셋 크기 차이가 크고 로드/언로드가 빈번하면 단편화를 완전히 피하기는 어렵습니다.

### 단편화 완화 전략

단편화를 완전히 제거하기는 어렵지만, 네이티브 메모리 할당기의 동작 원리를 활용하면 로딩 방식(씬 직접 참조, Resources, AssetBundle, Addressables)과 무관하게 단편화를 완화할 수 있습니다.

**에셋 로딩 순서 관리.**
여러 씬에 걸쳐 사용되는 공통 에셋(배경 텍스처, 캐릭터 메쉬 등)을 먼저, 수명이 짧은 에셋(이펙트 텍스처 등)을 나중에 로드합니다.
할당기는 요청 순서대로 메모리를 배치하는 경향이 있으므로, 공통 에셋이 연속된 영역에 자리 잡으면 짧은 에셋이 해제될 때 빈 공간이 한쪽에 모여 병합되기 쉽습니다.
다만 먼저 로드한 에셋이 중간에 해제되면 효과가 사라지므로, 오래 유지되는 에셋에 적합한 전략입니다.

**씬 전환 전 참조 정리.**
씬 전환 시 Unity는 내부적으로 `Resources.UnloadUnusedAssets()`를 호출하여, 어디서도 참조되지 않는 에셋을 메모리에서 해제합니다(이름과 달리 Resources로 로드한 에셋에 한정되지 않고 모든 에셋이 대상입니다).
씬에 속한 오브젝트는 전환 시 파괴되므로 그 오브젝트가 가진 에셋 참조도 함께 사라지지만, static 변수, DontDestroyOnLoad 오브젝트, 캐시용 컬렉션처럼 씬 전환 후에도 유지되는 곳에 참조가 남아 있으면 해당 에셋은 해제되지 않습니다.
씬 전환 전에 불필요한 참조를 `null`로 정리해야 에셋이 제대로 해제되며, 정리하지 않으면 해제되어야 할 에셋이 메모리에 남아 단편화가 누적됩니다.

**로딩 화면 활용.** `LoadSceneMode.Single`로 씬을 전환하면 Unity는 새 씬을 먼저 로드한 뒤 이전 씬을 해제합니다.
공유 에셋은 중복 로드되지 않지만, 각 씬의 고유 에셋은 전환 중에 동시에 메모리에 존재하므로 피크가 높아집니다.
로딩 화면을 경유하여 "이전 씬 해제 → 빈 상태 → 새 씬 로드" 순서로 진행하면 한 시점에 한 씬의 에셋만 존재하여 피크를 줄일 수 있고, 이전 씬 해제 시점에 메모리가 비워지면서 할당기가 연속 공간을 확보하기 쉬워져 단편화도 완화됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- Title -->
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">씬 전환 시 메모리 피크 관리</text>
  <!-- Direct transition -->
  <text x="30" y="55" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">직접 전환</text>
  <!-- Timeline arrow -->
  <line x1="30" y1="70" x2="550" y2="70" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="550,66 558,70 550,74" fill="currentColor" opacity="0.3"/>
  <!-- Scene B load box -->
  <rect x="30" y="80" width="120" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="90" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">씬 B 로드</text>
  <!-- Arrow -->
  <line x1="155" y1="98" x2="175" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="175,94 183,98 175,102" fill="currentColor"/>
  <!-- Peak zone (highlighted) -->
  <rect x="185" y="75" width="230" height="46" rx="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="2" stroke-dasharray="4,2"/>
  <text x="300" y="95" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">씬 A 에셋 + 씬 B 에셋 동시 존재</text>
  <text x="300" y="112" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">메모리 피크 높음</text>
  <!-- Arrow -->
  <line x1="420" y1="98" x2="440" y2="98" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="440,94 448,98 440,102" fill="currentColor"/>
  <!-- Result -->
  <rect x="450" y="80" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="500" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">피크 높음</text>

  <!-- Divider -->
  <line x1="30" y1="140" x2="555" y2="140" stroke="currentColor" stroke-width="0.5" opacity="0.2"/>

  <!-- Loading screen transition -->
  <text x="30" y="165" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">로딩 화면 경유</text>
  <!-- Timeline arrow -->
  <line x1="30" y1="180" x2="550" y2="180" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <polygon points="550,176 558,180 550,184" fill="currentColor" opacity="0.3"/>
  <!-- Scene A unload -->
  <rect x="30" y="190" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="85" y="212" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">씬 A 해제</text>
  <!-- Arrow -->
  <line x1="145" y1="208" x2="165" y2="208" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="165,204 173,208 165,212" fill="currentColor"/>
  <!-- Empty state -->
  <rect x="175" y="190" width="100" height="36" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="225" y="212" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">빈 상태</text>
  <!-- Arrow -->
  <line x1="280" y1="208" x2="300" y2="208" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="300,204 308,208 300,212" fill="currentColor"/>
  <!-- Scene B load -->
  <rect x="310" y="190" width="110" height="36" rx="5" fill="currentColor" fill-opacity="0.1" stroke="currentColor" stroke-width="1.5"/>
  <text x="365" y="206" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">씬 B 로드</text>
  <text x="365" y="220" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">한 씬 에셋만 존재</text>
  <!-- Arrow -->
  <line x1="425" y1="208" x2="445" y2="208" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="445,204 453,208 445,212" fill="currentColor"/>
  <!-- Result -->
  <rect x="455" y="190" width="95" height="36" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="502" y="212" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">피크 낮음</text>
</svg>
</div>

위 다이어그램은 메모리 피크가 발생하는 구간과 그렇지 않은 구간의 차이를 보여줍니다.
직접 전환 방식에서 피크가 문제가 되는 이유는, 피크 구간에서 메모리 한계에 도달하면 OOM Kill이 발생하기 때문입니다.
로딩 화면 경유 방식은 피크를 낮출 뿐 아니라, 이전 씬의 에셋이 모두 해제된 시점에서 할당기가 메모리를 정리할 기회를 얻으므로 단편화 완화 효과도 있습니다.

이 전략들이 실제로 효과가 있는지 확인하려면, 현재 메모리를 어디에서 얼마나 사용하는지를 먼저 측정해야 합니다.

---

## Unity Profiler로 메모리 확인하기

Unity Profiler의 Memory 모듈은 메모리 사용량을 에셋 유형별로 분류하여 표시합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 420" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title -->
  <text x="260" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Unity Profiler — Memory 모듈에서 확인할 수 있는 항목</text>
  <!-- Total Used Memory (outer box) -->
  <rect x="20" y="40" width="480" height="370" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <text x="40" y="62" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Total Used Memory</text>

  <!-- Unity (Native) -->
  <rect x="40" y="78" width="440" height="185" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="98" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Unity (네이티브)</text>
  <!-- Asset items -->
  <rect x="60" y="108" width="200" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="70" y="124" font-family="sans-serif" font-size="10" fill="currentColor">Textures: XXX MB (개수: N)</text>
  <rect x="60" y="136" width="160" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="70" y="152" font-family="sans-serif" font-size="10" fill="currentColor">Meshes: XX MB (개수: N)</text>
  <rect x="60" y="164" width="160" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="70" y="180" font-family="sans-serif" font-size="10" fill="currentColor">Audio: XX MB (개수: N)</text>
  <rect x="270" y="108" width="190" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="280" y="124" font-family="sans-serif" font-size="10" fill="currentColor">Shaders: XX MB (개수: N)</text>
  <rect x="270" y="136" width="190" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="280" y="152" font-family="sans-serif" font-size="10" fill="currentColor">AnimationClips: X MB (개수: N)</text>
  <rect x="270" y="164" width="190" height="24" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="280" y="180" font-family="sans-serif" font-size="10" fill="currentColor">Materials: X MB (개수: N)</text>

  <!-- Connector lines from Unity box to sub-items -->
  <line x1="50" y1="100" x2="50" y2="250" stroke="currentColor" stroke-width="1" opacity="0.3"/>

  <!-- Mono / Managed -->
  <rect x="40" y="275" width="440" height="52" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="295" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">Mono / Managed (관리 힙)</text>
  <rect x="60" y="303" width="150" height="18" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="70" y="316" font-family="sans-serif" font-size="10" fill="currentColor">Used: XX MB</text>
  <rect x="230" y="303" width="170" height="18" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <text x="240" y="316" font-family="sans-serif" font-size="10" fill="currentColor">Reserved: XX MB</text>

  <!-- GfxDriver -->
  <rect x="40" y="339" width="220" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="55" y="358" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">GfxDriver (그래픽스 드라이버)</text>

  <!-- Other -->
  <rect x="275" y="339" width="205" height="30" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="358" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Other</text>

  <!-- Sub-labels -->
  <text x="55" y="253" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.5">렌더 타깃, 프레임 버퍼 등은 GfxDriver에 포함</text>
</svg>
</div>

Profiler에서 관리 힙은 Unity 버전에 따라 "Mono" 또는 "Managed"로 표시됩니다.
이전 버전에서는 Mono 런타임의 이름을 따 "Mono"로 표시했지만, IL2CPP 빌드에서도 관리 힙은 동일하게 존재하므로 최신 버전에서는 런타임과 무관한 "Managed"로 표기가 통일되는 추세입니다.

<br>

Profiler의 Memory 모듈에서 "Detailed" 모드를 선택하면 에셋 유형별 메모리 사용량을 확인할 수 있습니다. "Take Sample" 버튼을 눌러 특정 시점의 스냅샷을 찍으면 개별 에셋의 이름, 크기, 참조 횟수까지 확인할 수 있습니다.

메모리 문제를 진단할 때는 총 사용량에서 유형별, 개별 에셋으로 범위를 좁혀 갑니다.
앞 절의 모바일 메모리 예산과 총 사용량을 비교하여 초과 여부를 확인한 뒤, 유형별 비중에서 비정상적으로 큰 항목이 있는지 살핍니다.
예를 들어 텍스처가 예산의 70%를 넘는다면 해상도나 압축 설정을 점검합니다.

개별 에셋 목록까지 내려가면 예상보다 큰 에셋이나 중복 로드된 에셋을 찾을 수 있습니다.
같은 텍스처가 이름만 다르게 두 번 로드되어 있거나, 사용하지 않는 에셋이 여전히 메모리에 남아 있는 경우도 확인합니다.

씬 전환 전후의 메모리 변화를 비교하는 것도 유용합니다.
씬을 언로드한 후에도 메모리가 줄어들지 않으면 해제되지 못한 에셋이 남아 있다는 뜻이며, 이는 메모리 누수입니다.

---

## 에셋 메모리 최적화 체크리스트

Profiler로 메모리 사용 현황을 파악했다면, 에셋 유형별로 구체적인 최적화를 적용할 차례입니다.

### 텍스처

화면에서 작게 보이는 오브젝트에 2048x2048 텍스처가 할당되어 있다면, 실제 표시 크기에 맞게 해상도를 낮추는 것만으로 메모리를 크게 줄일 수 있습니다.
모바일에서는 ASTC 압축이 화질 대비 메모리 효율이 높으며, 시각적 중요도에 따라 블록 크기(4x4~8x8)를 조절하여 품질과 메모리 사이 균형을 잡을 수 있습니다.

3D 오브젝트처럼 카메라와의 거리가 변하는 텍스처에는 밉맵을 켜고, UI처럼 항상 원본 해상도로 표시되는 텍스처에는 밉맵을 끕니다. 앞서 설명한 것처럼 밉맵은 원본 대비 약 33%의 추가 메모리를 사용하므로, 사용되지 않는 곳에서는 메모리만 차지합니다.

알파 채널도 확인합니다. 알파가 필요 없는 텍스처를 RGB 전용 포맷으로 전환하면 메모리를 절약할 수 있습니다.

### 메쉬

Read/Write Enabled가 불필요하게 켜진 메쉬가 있는지 확인합니다.
앞에서 살펴본 것처럼 이 옵션이 켜져 있으면 GPU 버퍼와 CPU 복사본이 동시에 존재하여 메모리가 2배로 소모되므로, 런타임에 메쉬를 수정하지 않는다면 끄는 것이 좋습니다.

사용하지 않는 정점 속성(Tangent, UV1 등)도 제거하면 메모리를 추가로 절약할 수 있습니다. (정점 속성별 크기와 용도는 [렌더링 기초 (1) - 메쉬의 구조](/dev/unity/RenderingFoundation-1/)에서 확인할 수 있습니다.)

### 오디오

짧은 효과음처럼 자주 재생되는 클립은 Decompress On Load로 미리 풀어 두면 재생 시 CPU 부담이 줄어듭니다.
긴 BGM처럼 용량이 큰 클립은 Streaming으로 필요한 부분만 읽으면 메모리를 절약할 수 있습니다.
음성 대사처럼 중간 길이인 경우에는 Compressed In Memory가 메모리와 CPU 사이 균형에 유리합니다.

샘플레이트는 초당 기록하는 오디오 샘플의 수이며, 샘플 수에 비례하여 메모리를 차지합니다.
AudioClip Import Settings의 플랫폼별 탭에서 Sample Rate Setting을 조정할 수 있습니다.

Preserve Sample Rate는 원본을 유지하고, Optimize Sample Rate는 Unity가 자동으로 선택하며, Override Sample Rate는 원하는 값을 직접 지정합니다.
예를 들어 48kHz에서 22.05kHz로 낮추면 데이터 총량이 약 절반으로 줄어듭니다. 재현 가능한 최대 주파수도 낮아지지만(나이퀴스트 정리: 최대 주파수 = 샘플레이트 / 2), 모바일 기기의 스피커 특성상 11kHz 이상의 고음역은 재현이 제한되는 경우가 있어 효과음에 22.05kHz를 적용하는 것도 검토할 수 있습니다.

채널 수도 메모리에 영향을 줍니다.
공간감이 필요 없는 효과음에 스테레오(stereo)가 적용되어 있다면, 모노(mono)로 전환하면 메모리가 절반으로 줄어듭니다.

### 셰이더

셰이더는 기능 조합(안개, 그림자 등의 ON/OFF)마다 별도의 variant로 컴파일되어 빌드에 포함됩니다.
조합 수가 늘어나면 variant도 기하급수적으로 늘어나 빌드 크기와 메모리를 차지하므로, variant stripping으로 사용하지 않는 variant를 빌드에서 제외하는 것이 중요합니다.
`multi_compile`과 `shader_feature`의 차이, variant stripping의 구체적인 설정 방법은 [셰이더 최적화 (2)](/dev/unity/ShaderOptimization-2/)에서 다룹니다.

### 애니메이션

애니메이션 클립은 위치, 회전, 스케일 등의 변화를 프레임별로 기록하므로, 데이터가 많을수록 메모리를 차지합니다.
압축 설정을 Optimal로 하면 Unity가 데이터를 분석하여 시각적 차이 없이 가장 작은 크기를 선택합니다.
캐릭터 애니메이션처럼 본의 크기가 변하지 않는 경우에는 스케일(Scale) 데이터를 제거하면 메모리를 추가로 절약할 수 있습니다.
애니메이션 압축의 구체적인 동작 방식은 [파티클과 애니메이션 (2)](/dev/unity/ParticleAndAnimation-2/)에서 다룹니다.

---

## 에셋을 세밀하게 제어하려면

위 체크리스트로 개별 에셋의 크기를 줄일 수 있지만, 메모리를 안정적으로 유지하려면 에셋을 언제 로드하고 언제 해제할지도 관리해야 합니다. 앞서 살펴본 것처럼 Resources 폴더는 빌드 포함 범위를 통제할 수 없어 이런 관리에 한계가 있습니다.

**AssetBundle**과 **Addressables**는 에셋을 번들 단위로 묶어 필요한 시점에 로드하고, 사용이 끝나면 해제하는 구조를 제공합니다. 구체적인 구조와 활용 전략은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 이어집니다.

---

## 마무리

Unity 게임의 메모리 사용량 중 대부분은 C# 관리 힙이 아니라, C++ 엔진이 관리하는 네이티브 메모리에 로드된 에셋입니다. 
텍스처, 메쉬, 오디오, 셰이더, 애니메이션의 메모리 특성을 이해하고, 에셋의 생명주기를 관리하는 것이 모바일 메모리 최적화의 핵심입니다.

- 텍스처는 게임 메모리의 가장 큰 비중(50% 이상)을 차지하며, 해상도와 압축 포맷(ASTC) 설정이 메모리 절약에 큰 영향을 줍니다
- 메쉬의 Read/Write Enabled 옵션이 켜져 있으면 GPU 버퍼와 CPU 복사본이 동시에 존재하여 메모리가 2배로 소모됩니다
- 오디오는 로딩 모드(Decompress On Load, Compressed In Memory, Streaming)에 따라 메모리 사용량이 10배 이상 차이납니다
- 셰이더 variant는 키워드 조합에 따라 수천 개까지 생성될 수 있으며, variant stripping으로 사용하지 않는 variant를 빌드에서 제외할 수 있습니다
- Resources 폴더는 사용 여부와 무관하게 모든 에셋이 빌드에 포함되므로, Unity 공식 문서에서도 사용을 권장하지 않습니다
- 모바일에서는 OS가 메모리 한계를 초과한 앱을 강제 종료(OOM Kill)하므로, 저사양 기기 기준으로 메모리 예산을 설정하는 것이 안전합니다
- 에셋 로드/언로드 반복으로 네이티브 메모리에도 단편화가 발생하며, 로딩 순서 관리와 로딩 화면 활용으로 완화할 수 있습니다

에셋 하나하나의 크기를 줄이는 것도 중요하지만, 메모리를 안정적으로 유지하려면 에셋을 언제 로드하고 언제 해제할지도 체계적으로 관리해야 합니다.
이어지는 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 이를 가능하게 하는 AssetBundle과 Addressables를 다룹니다.

<br>

---

**관련 글**
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [스크립트 최적화 (1) - C# 실행과 메모리 할당](/dev/unity/ScriptOptimization-1/)

**시리즈**
- [메모리 관리 (1) - 가비지 컬렉션의 원리](/dev/unity/MemoryManagement-1/)
- **메모리 관리 (2) - 네이티브 메모리와 에셋** (현재 글)
- [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)

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
- **메모리 관리 (2) - 네이티브 메모리와 에셋** (현재 글)
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
