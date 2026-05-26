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

[Part 1](/dev/unity/MobileStrategy-1/)에서는 모바일 게임이 발열과 배터리라는 물리적 제약 안에서 동작한다는 점을 다루었습니다. 서멀 쓰로틀링이 시작되면 차가운 상태에서의 피크 성능을 계속 유지할 수 없고, 목표 프레임레이트도 전력과 발열까지 고려해 정해야 합니다. 결국 모바일 성능 설계의 기준은 순간적인 최고 성능이 아니라, 실제 플레이 시간 동안 유지되는 지속 성능입니다.

문제는 이 지속 성능이 기기마다 크게 다르다는 점입니다. SoC 성능, GPU 구조, RAM 용량, 화면 해상도, 방열 설계가 모두 다르기 때문에 같은 빌드라도 어떤 기기에서는 여유가 남고, 어떤 기기에서는 몇 분 만에 프레임 예산을 넘을 수 있습니다. 하나의 품질 설정으로 모든 기기를 만족시키기는 어렵습니다. 낮은 사양에 맞추면 고사양 기기의 여유 성능을 활용하지 못하고, 높은 사양에 맞추면 저사양 기기에서 프레임레이트와 발열을 안정적으로 유지하기 어렵습니다.

이 글에서는 기기 성능 차이에 대응하기 위한 Quality Settings 티어와 디바이스 분류 전략을 먼저 살펴봅니다. 이어서 모바일 배포에서 중요한 IL2CPP 스트리핑, 앱 크기, 에셋 압축을 정리합니다.

---

## Quality Settings 티어

Unity의 **Quality Settings**(Edit > Project Settings > Quality)는 여러 품질 프리셋을 만들어 두고, 기기 성능이나 실행 중 상태에 따라 전환할 수 있게 해 주는 시스템입니다. 여기서 중요한 것은 옵션을 많이 만드는 것이 아니라, 같은 목표 프레임레이트를 유지하기 위해 기기 등급별로 어떤 부하를 줄이고 어떤 품질을 남길지 정하는 것입니다. 저사양 티어에서는 프레임 시간과 발열에 직접 영향을 주는 항목을 먼저 낮추고, 고사양 티어에서는 지속 성능에 여유가 있는 범위 안에서 해상도, 그림자, 후처리 같은 시각 품질을 더 유지합니다.

품질 티어는 비용 축별로 나누어 설계하는 편이 좋습니다. 해상도는 픽셀 처리량을, 그림자는 추가 렌더링 패스를, 텍스처 설정은 메모리와 대역폭을, LOD는 정점 수와 원거리 오브젝트 비용을 조절합니다. 아래 항목들은 모바일에서 티어별 차이를 만들 때 자주 사용하는 설정입니다.

<br>

**품질 티어에서 주로 조정하는 항목**

| 항목 | 주로 줄이는 비용 | 낮췄을 때의 영향 |
|---|---|---|
| Render Scale | 픽셀 수, 프래그먼트 셰이더, 렌더 타깃 대역폭 | 화면이 흐려질 수 있음 |
| 그림자 | 셰도우맵 렌더링, 그림자 샘플링, 추가 드로우 | 입체감과 접지감이 약해짐 |
| 텍스처 밉맵 제한 | 텍스처 메모리, 텍스처 대역폭 | 표면 디테일이 낮아짐 |
| MSAA | 경계 샘플 수, 타일 메모리 사용량 | 폴리곤 경계가 거칠어질 수 있음 |
| 후처리 | 전체 화면 패스, 깊이·컬러 텍스처 샘플링 | 화면 연출이 단순해짐 |
| LOD 바이어스 | 정점 수, 원거리 오브젝트 비용 | 멀리 있는 오브젝트 품질이 낮아짐 |

<br>

가장 먼저 검토할 항목은 **Render Scale**입니다. URP의 Render Scale은 화면에 표시되는 해상도와 별개로 카메라가 장면을 렌더링하는 내부 해상도를 낮춥니다. 예를 들어 1080p 화면에서 Render Scale을 0.7로 설정하면 가로와 세로가 각각 70%로 줄어들고, 실제로 처리해야 하는 픽셀 수는 약 49%가 됩니다. 픽셀 셰이더, 후처리, 렌더 타깃 대역폭이 함께 줄어드는 효과가 크지만, 카메라가 그린 결과를 다시 확대해 보여주므로 화면이 흐려질 수 있습니다.

UI 선명도는 Render Scale 값만 보고 판단하기 어렵습니다. HUD나 텍스트가 장면 카메라의 저해상도 렌더 결과에 포함되어 있으면, 장면과 함께 확대되면서 흐려질 수 있습니다. Render Scale을 낮춘 뒤 UI가 흐려진다면, UI Canvas를 `Screen Space - Overlay`로 두거나 UI 전용 카메라 구성을 사용해 장면 렌더링과 분리하는 방법을 검토합니다. 핵심은 해상도를 낮춘 장면 렌더링과, 선명해야 하는 UI가 같은 저해상도 결과물에 묶이지 않도록 확인하는 것입니다.

**그림자**는 모바일에서 티어별 차이를 크게 만들 수 있는 항목입니다. 실시간 그림자는 먼저 그림자를 만드는 라이트 기준으로 셰도우맵을 렌더링하고, 이후 본 렌더링에서 그 셰도우맵을 샘플링해 밝기가 정해집니다. 즉 그림자를 켜면 셰도우맵을 만들기 위한 추가 렌더링 비용과, 화면을 그릴 때의 그림자 샘플링 비용이 함께 생깁니다. 저사양 티어에서 선택할 수 있는 방법은 그림자를 끄는 것, 그림자 거리와 셰도우맵 해상도를 낮추는 것, 캐스케이드 수를 줄이는 것입니다. 다만 그림자를 완전히 끄면 캐릭터와 바닥 사이의 접지감이 약해질 수 있으므로, Blob Shadow, 베이크된 그림자, 간단한 데칼이 대안이 됩니다.

**텍스처 해상도**는 GPU가 사용하는 텍스처 해상도와 샘플링 대역폭을 조절하는 항목입니다. `QualitySettings.globalTextureMipmapLimit`은 2D 밉맵 텍스처에서 사용할 최고 해상도 mip을 제한합니다. 값이 1이면 원본 mip을 건너뛰고 절반 해상도부터, 2이면 1/4 해상도부터 사용하는 식입니다. 이렇게 하면 영향받는 텍스처의 고해상도 mip 업로드와 샘플링 대역폭을 줄일 수 있지만, 빌드에 포함된 텍스처 데이터 자체를 제거하는 설정은 아닙니다. UI, 폰트, 캐릭터 얼굴처럼 선명도가 중요한 텍스처는 별도의 Mipmap Limit Group에 넣거나 텍스처별 제한 값을 조정할 대상입니다. 일반 배경 텍스처와 같은 수준으로 낮아지면 품질 저하가 바로 보이기 때문입니다. 런타임에서 값을 바꿀 때는 텍스처 재업로드가 발생할 수 있으므로, 로딩 화면이나 씬 전환처럼 끊김을 감추기 쉬운 시점에 적용하는 편이 안전합니다.

**MSAA**는 폴리곤 경계의 계단 현상을 줄이기 위해 한 픽셀 안에서 여러 샘플을 저장하고 해석하는 방식입니다. 화면 전체를 고해상도로 다시 그리는 방식은 아니지만, 샘플 수가 늘어나는 만큼 컬러·깊이 버퍼 사용량과 resolve 비용이 증가할 수 있습니다. 특히 Render Scale이 높거나 HDR, 여러 렌더 타깃, 깊이 텍스처를 함께 쓰는 구성에서는 비용이 더 커질 수 있습니다. 저사양 티어에서는 Off나 2x부터 시작하고, 4x는 실제 기기에서 프레임 시간과 메모리 대역폭을 확인한 뒤 허용하는 편이 안전합니다.

**후처리**는 이미 렌더링된 화면을 다시 읽고 가공하는 단계입니다. 대부분 화면 크기에 비례해 비용이 늘어나므로, Render Scale과 화면 해상도의 영향을 함께 받습니다. Color Grading처럼 비교적 단순한 효과도 있지만, Bloom, SSAO, Depth of Field처럼 다운샘플·블러·깊이 텍스처 샘플링이 들어가는 효과는 모바일에서 부담이 커질 수 있습니다. 저사양 티어에서는 색 보정처럼 체감 대비 비용이 낮은 효과만 남기고, SSAO나 무거운 Bloom은 해상도와 샘플 수를 낮추거나 끄는 쪽이 안전합니다. 품질 티어별로 Volume Profile을 나누어 두면 효과의 활성 여부와 강도를 단계적으로 관리할 수 있습니다.

**LOD 바이어스**는 카메라 거리별로 어떤 LOD 메시를 사용할지 조정합니다. 바이어스를 낮추면 더 이른 시점에 낮은 LOD로 전환되므로, 멀리 있는 오브젝트의 정점 수와 셰이더 비용을 줄일 수 있습니다. 오브젝트 수가 많은 필드나 오픈월드에서는 효과가 크지만, 너무 공격적으로 낮추면 모델이 갑자기 단순해지는 팝핑이 눈에 띕니다. 따라서 티어별 LOD 바이어스만 바꾸기보다, 주요 오브젝트의 LOD Group 전환 거리와 크로스페이드 설정도 함께 확인하는 편이 좋습니다.

URP 프로젝트에서는 Quality Level의 **Render Pipeline** 항목에 서로 다른 **URP Asset**(UniversalRenderPipelineAsset)을 지정할 수 있습니다. 특정 Quality Level이 활성화되면 그 레벨에 지정된 URP Asset이 기본 렌더 파이프라인 설정을 덮어쓰는 구조입니다. Render Scale, MSAA, 그림자 캐스케이드처럼 URP Asset에 들어 있는 설정은 Low/Mid/High 티어별로 나누기 좋습니다. 반면 Volume Profile, 게임 내 오브젝트 밀도, 이펙트 개수, 동시 등장 수처럼 프로젝트 코드나 씬 데이터가 관리하는 항목은 Quality Settings만으로 자동 전환되지 않습니다. 이런 값은 별도의 품질 설정 데이터에 묶어 Quality Level과 함께 적용하는 편이 좋습니다.

런타임에서는 `QualitySettings.SetQualityLevel(index)`로 Quality Level을 전환할 수 있습니다. 다만 이 방식은 프리셋 전체를 바꾸는 작업이므로, 안티앨리어싱이나 렌더 파이프라인 설정처럼 리소스 재설정이 필요한 항목까지 함께 바뀔 수 있습니다. 그래서 기기 티어를 처음 적용할 때나 옵션 메뉴에서 사용자가 품질을 바꿀 때처럼, 전환 비용을 감수할 수 있는 시점에 사용하는 편이 적절합니다. 플레이 중 열 상태나 프레임 시간에 따라 품질을 조금씩 조정해야 한다면, 전체 Quality Level을 반복해서 바꾸기보다 Render Scale, 후처리 강도, 이펙트 수처럼 영향 범위가 분명한 항목만 따로 조절하는 구조가 더 안정적입니다.

---

## 디바이스 티어 전략

Quality Settings 티어는 Low, Mid, High 같은 품질 선택지를 만드는 단계입니다. 그다음에는 실행 중인 기기가 어느 선택지에 가까운지 판단해야 합니다. 이렇게 기기를 성능 등급으로 나누고, 각 등급에 맞는 시작 품질을 고르는 방식을 **디바이스 티어(Device Tier)** 전략이라고 합니다. 실제 성능보다 낮은 티어로 배정하면 고사양 기기에서 품질을 활용하지 못하고, 반대로 실제 성능보다 높은 티어로 배정하면 저사양 기기에서 프레임 시간과 발열을 감당하기 어려워집니다. 따라서 디바이스 티어는 기기의 대략적인 성능과 메모리 여유를 기준으로 시작 품질을 정하는 출발점이 됩니다.

### 티어 분류 기준

모든 기기를 직접 측정한 뒤 품질을 정할 수는 없으므로, 처음에는 기기 정보로 기본 품질을 추정해야 합니다. Unity의 `SystemInfo`에서 확인할 수 있는 RAM, GPU 이름, 그래픽 API는 그때 사용할 수 있는 대표적인 정보입니다.

<br>

**초기 품질 선택에 참고할 SystemInfo 항목**

| 항목 | 용도 |
|---|---|
| `SystemInfo.systemMemorySize` | 전체 RAM 크기. 메모리 예산과 저사양 기기 구분에 가장 먼저 참고 |
| `SystemInfo.graphicsDeviceName` | GPU 이름. 알려진 GPU 목록과 대조해 그래픽 성능 등급을 보정 |
| `SystemInfo.graphicsDeviceType` | 사용 중인 그래픽 API. Vulkan, Metal, OpenGL ES 등 렌더링 경로와 기능 차이 확인 |
| `SystemInfo.supportsComputeShaders` | 컴퓨트 셰이더 지원 여부. compute 기반 효과나 대체 경로 선택에 사용 |

<br>

이 중에서 가장 먼저 보기 쉬운 값은 RAM입니다. RAM은 메모리 예산을 직접 가늠할 수 있게 해 주고, 매우 낮은 RAM을 가진 기기를 Low 티어로 분류하는 데 유용합니다. 다만 RAM이 곧 그래픽 성능을 의미하지는 않습니다. 같은 RAM 용량이라도 SoC와 GPU 세대, 화면 해상도에 따라 실제 프레임 시간은 크게 달라질 수 있습니다.

그래서 RAM은 대략적인 출발점으로 보고, GPU 정보로 한 번 더 확인하는 편이 좋습니다. 예를 들어 RAM 용량만 보면 Mid 티어에 가까운 기기라도 GPU 세대가 오래되었거나 화면 해상도가 높다면 렌더 스케일, 그림자, 후처리 설정을 더 낮게 잡아야 할 수 있습니다. 반대로 RAM 용량이 아주 크지 않아도 비교적 최신 GPU를 탑재한 기기는 같은 메모리 조건의 다른 기기보다 렌더링 품질을 더 안정적으로 유지할 수 있습니다. 즉 RAM은 메모리 여유를 보는 기준이고, GPU는 렌더링 부하를 얼마나 감당할 수 있는지 가늠하는 기준입니다.

Unity에서 GPU 이름은 `SystemInfo.graphicsDeviceName`으로 읽을 수 있습니다. 이 값을 이용하면 Adreno, Mali, Apple GPU처럼 알려진 GPU 계열이나 세대를 기준으로 티어를 보정할 수 있습니다. 다만 실제로 반환되는 문자열은 드라이버, OS, 제조사 펌웨어에 따라 조금씩 달라질 수 있으므로, 문자열을 완전히 똑같이 비교하는 방식에만 의존하면 예외가 늘어납니다. 실무에서는 GPU 이름을 대략적인 제조사와 모델명으로 정리한 뒤 알려진 목록과 대조하고, 알 수 없는 GPU는 한 단계 보수적인 티어로 배정하는 편이 안전합니다.

`SystemInfo.graphicsMemorySize`와 `SystemInfo.processorFrequency`도 참고할 수는 있지만, RAM이나 GPU 이름보다 우선순위는 낮습니다. 모바일에서는 CPU와 GPU가 시스템 메모리를 함께 쓰는 경우가 많아, `graphicsMemorySize` 값만으로 텍스처나 렌더 타깃에 실제로 남는 여유를 알기 어렵기 때문입니다. `processorFrequency`도 비슷합니다. 모바일 CPU는 발열, 배터리 상태, 전력 정책에 따라 클럭이 계속 바뀌므로, 표시된 주파수가 플레이 중 오래 유지된다고 보기 어렵습니다. 그래서 이 값들은 Low/Mid/High를 나누는 주된 조건으로 삼기보다, RAM과 GPU 이름으로 추정한 티어를 보완하는 정도로 사용하는 편이 좋습니다.

### 티어 결정 시점

디바이스 티어는 보통 앱을 처음 실행할 때 한 번 정해 두는 편이 적절합니다. 실행할 때마다 기기 정보를 다시 읽어 자동 판별을 수행하면, 사용자가 설정 화면에서 선택한 티어가 자동 판별 결과로 바뀔 수 있기 때문입니다. OS나 드라이버 업데이트로 `SystemInfo` 값이 조금 달라졌을 때도, 같은 기기에서 품질이 갑자기 바뀌는 상황을 줄일 수 있습니다.

따라서 저장된 티어가 없다면 `SystemInfo`에서 RAM, GPU 이름, 그래픽스 API 지원 여부 등을 읽고 Low/Mid/High 중 하나를 초기 티어로 정합니다. 선택한 티어는 `QualitySettings.SetQualityLevel()`로 적용합니다. 다만 Unity가 이 선택을 다음 실행까지 자동으로 기억해 주지는 않으므로, 같은 티어를 유지하려면 결과를 따로 저장해야 합니다. 간단한 구현에서는 `PlayerPrefs`에 티어 값을 저장해 두고, 이후 실행에서는 그 값을 먼저 읽어 적용합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 585" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">디바이스 티어 적용 흐름</text>

  <rect x="230" y="42" width="160" height="36" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="64" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">앱 실행</text>

  <line x1="310" y1="78" x2="310" y2="90" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="305,86 310,96 315,86" fill="currentColor"/>

  <polygon points="310,96 430,136 310,176 190,136" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="132" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">저장된 티어가</text>
  <text x="310" y="149" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">있는가?</text>

  <text x="166" y="128" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">없음</text>
  <polyline points="190,136 170,136 170,200" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="165,195 170,205 175,195" fill="currentColor"/>

  <rect x="50" y="205" width="240" height="56" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="227" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">SystemInfo 조회</text>
  <text x="170" y="248" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">RAM, GPU 이름, API 지원 여부</text>

  <line x1="170" y1="261" x2="170" y2="282" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="165,277 170,287 175,277" fill="currentColor"/>

  <rect x="50" y="287" width="240" height="70" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="309" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">초기 티어 결정</text>
  <text x="170" y="330" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">RAM 기준 + GPU 보정</text>
  <text x="170" y="348" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">Low / Mid / High</text>

  <line x1="170" y1="357" x2="170" y2="377" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="165,372 170,382 175,372" fill="currentColor"/>

  <rect x="50" y="382" width="240" height="42" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="170" y="407" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">PlayerPrefs에 티어 저장</text>

  <text x="454" y="128" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">있음</text>
  <polyline points="430,136 465,136 465,242" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="460,237 465,247 470,237" fill="currentColor"/>

  <rect x="360" y="247" width="210" height="42" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="465" y="272" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">PlayerPrefs에서 티어 읽기</text>

  <polyline points="170,424 170,450 310,450" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <polyline points="465,289 465,450 310,450" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <line x1="310" y1="450" x2="310" y2="460" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="305,455 310,465 315,455" fill="currentColor"/>

  <rect x="160" y="465" width="300" height="40" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="310" y="489" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">QualitySettings.SetQualityLevel(tier)</text>

  <line x1="310" y1="505" x2="310" y2="520" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="305,515 310,525 315,515" fill="currentColor"/>

  <rect x="130" y="525" width="360" height="42" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3"/>
  <text x="310" y="548" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">설정 화면에서 플레이어가 수동 변경 가능</text>
  <text x="310" y="563" text-anchor="middle" font-family="sans-serif" font-size="11" font-style="italic" fill="currentColor">변경 시 PlayerPrefs 갱신</text>
</svg>
</div>

<br>

이 흐름에서 자동 판별은 최종 결정이라기보다 첫 실행을 위한 기본값에 가깝습니다. 실제 체감 성능은 배터리 절약 모드, 주변 온도, 백그라운드 앱, 플레이어가 원하는 프레임레이트에 따라 달라질 수 있습니다. 따라서 설정 화면에는 자동 설정을 기본으로 두고, 필요하면 사용자가 품질 프리셋을 바꿀 수 있는 선택지를 함께 제공하는 것이 적절합니다. 이때 내부 티어 이름을 그대로 노출하기보다 성능 우선, 균형, 품질 우선처럼 사용자가 결과를 예상하기 쉬운 이름으로 보여주는 편이 좋습니다.

---

## IL2CPP 스트리핑과 코드 최적화

디바이스 티어가 실행 중 품질을 맞추기 위한 전략이라면, 빌드 단계에서는 앱에 포함되는 코드와 리소스의 양을 관리해야 합니다. 앱 크기의 대부분은 에셋이 차지하지만, 코드 쪽에서도 IL2CPP와 스트리핑 설정을 통해 불필요한 부분을 줄일 수 있습니다.

다만 스트리핑 레벨을 높일수록 무조건 좋은 것은 아닙니다. 사용하지 않는 코드를 제거해 실행 파일 크기를 줄일 수 있지만, 리플렉션이나 일부 SDK처럼 정적 분석만으로 사용 여부를 알기 어려운 코드가 함께 제거될 수도 있기 때문입니다. 먼저 IL2CPP 빌드 과정에서 코드가 어떻게 변환되는지 살펴보고, 이어서 Managed Stripping Level별 차이와 적용 시 주의할 점을 다룹니다.

### IL2CPP와 코드 변환

Unity 프로젝트의 스크립트는 C#으로 작성되지만, 빌드에서 C# 소스가 그대로 실행되는 것은 아닙니다. 먼저 C# 컴파일러가 스크립트를 **IL(Intermediate Language)** 바이트코드로 변환하고, IL2CPP가 이 IL을 다시 C++ 코드로 변환합니다. 그다음 플랫폼별 네이티브 컴파일러가 C++ 코드를 컴파일해 최종 실행 파일과 라이브러리에 포함합니다.

결과적으로 C#으로 작성한 게임 로직은 모바일 기기에서 네이티브 코드 형태로 실행됩니다. 실행 중에 IL을 기계어로 변환하는 단계가 없기 때문에, 런타임에 JIT(Just-In-Time) 컴파일을 수행하는 방식과는 동작 특성이 달라집니다.

> IL, JIT/AOT, Mono와 IL2CPP의 차이는 [C# 런타임 기초 (2) - .NET 런타임과 IL2CPP](/dev/unity/CSharpRuntime-2/)에서 더 자세히 다룹니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="22" text-anchor="middle" font-family="sans-serif" font-size="14" font-weight="bold" fill="currentColor">IL2CPP 빌드 과정</text>

  <rect x="180" y="42" width="220" height="38" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="65" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">C# 소스 코드</text>

  <line x1="290" y1="80" x2="290" y2="105" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,100 290,110 295,100" fill="currentColor"/>
  <text x="305" y="97" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">C# 컴파일러</text>

  <rect x="180" y="110" width="220" height="38" rx="6" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="133" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">IL 바이트코드 (.dll)</text>

  <line x1="290" y1="148" x2="290" y2="173" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,168 290,178 295,168" fill="currentColor"/>
  <text x="305" y="165" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">IL2CPP</text>

  <rect x="180" y="178" width="220" height="38" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="201" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">C++ 소스 코드</text>

  <line x1="290" y1="216" x2="290" y2="241" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,236 290,246 295,236" fill="currentColor"/>
  <text x="305" y="233" font-family="sans-serif" font-size="10" font-style="italic" fill="currentColor">플랫폼별 네이티브 컴파일러</text>

  <rect x="160" y="246" width="260" height="38" rx="6" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="290" y="269" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">실행 파일과 네이티브 라이브러리</text>
</svg>
</div>

<br>

모바일 빌드에서 IL2CPP를 사용하는 가장 큰 이유는 플랫폼 제약과 실행 성능입니다. iOS처럼 JIT 컴파일을 허용하지 않는 플랫폼에서는 실행 전에 기계어가 준비되는 방식이 필요하므로, IL2CPP가 사실상 필수 선택지가 됩니다.

또한 IL2CPP는 생성된 C++ 코드를 플랫폼의 네이티브 컴파일러로 다시 빌드합니다. 이 과정에서 인라이닝, 데드 코드 제거 같은 C++ 컴파일러 최적화가 적용될 수 있으므로, 런타임에서 IL을 바로 실행하는 방식보다 실행 성능을 확보하기 쉽습니다. C# 어셈블리를 그대로 배포하는 방식보다 코드 구조가 직접 노출되기 어렵다는 점도 모바일 배포에서 장점이 됩니다.

### Managed Stripping Level

IL2CPP 빌드에서는 C# 코드와 .NET 라이브러리 코드가 모두 최종 바이너리로 이어질 수 있습니다. 프로젝트에서 실제로 쓰지 않는 타입과 메서드까지 모두 포함하면 실행 파일 크기가 불필요하게 커지므로, Unity는 빌드 과정에서 **관리 코드 스트리핑(Managed Code Stripping)**을 수행합니다.

이 작업은 UnityLinker가 담당합니다. UnityLinker는 씬, 스크립트, 어셈블리 참조를 따라가며 실행 중 도달할 수 있는 코드를 남기고, 도달할 수 없다고 판단한 관리 코드를 제거합니다. **Managed Stripping Level**은 이 분석을 얼마나 보수적으로 할지 정하는 설정입니다. 레벨이 높아질수록 더 넓은 범위를 분석해 빌드 크기를 줄일 수 있지만, 동적으로 접근하는 코드가 제거될 가능성도 함께 커집니다.

<br>

| 레벨 | 성격 | 사용 기준 |
|------|------|----------|
| **Minimal** | 가장 보수적인 설정. 사용자 코드 제거를 최소화하고, 예상치 못한 동작 변화가 가장 적음 | 안정성이 우선이거나 리플렉션·외부 SDK 사용이 많은 프로젝트 |
| **Low** | Minimal보다 조금 더 넓게 분석하지만, 여전히 보수적인 설정 | 기존 프로젝트에서 낮은 위험으로 크기를 조금 줄이고 싶을 때 |
| **Medium** | 모든 어셈블리를 더 넓게 분석해 빌드 크기 감소 효과가 커짐 | 모바일 빌드 크기를 줄이고 싶을 때의 현실적인 출발점 |
| **High** | 크기 감소를 우선해 가장 적극적으로 제거 | 빌드 크기가 특히 중요하고, 스트리핑 이후 전체 기능 테스트가 가능한 경우 |

<br>

레벨을 고를 때는 빌드 크기만 보지 않는 것이 좋습니다. Minimal은 가장 안전하지만 크기 감소 효과가 제한적이고, High는 크기를 더 줄일 수 있지만 런타임에서만 접근하는 코드가 제거될 가능성이 커집니다. 일반적인 모바일 프로젝트라면 Minimal이나 Medium에서 시작하고, 빌드 크기와 기능 테스트 결과를 보며 조정하는 편이 적절합니다.

특히 리플렉션(Reflection)을 사용하는 코드는 주의해야 합니다. 예를 들어 문자열로 타입을 찾거나, JSON 직렬화 라이브러리와 의존성 주입 프레임워크가 런타임에 멤버를 찾는 경우에는 코드 안에 직접 참조가 드러나지 않을 수 있습니다. UnityLinker가 이런 코드를 사용하지 않는다고 판단하면 빌드에서 제거할 수 있으므로, 스트리핑 레벨을 올릴수록 보존해야 할 타입과 메서드를 별도로 표시하는 작업이 중요해집니다.

### link.xml로 코드 보존

정적 분석으로는 사용 여부가 드러나지 않지만 런타임에는 필요한 코드가 있다면 **link.xml**로 보존 대상을 지정할 수 있습니다. `link.xml`은 UnityLinker에게 "이 타입이나 어셈블리는 제거하지 말라"고 알려주는 파일이며, 보통 프로젝트의 `Assets` 폴더 아래에 둡니다.

중요한 것은 보존 범위를 필요한 만큼만 좁게 잡는 것입니다. 전체 어셈블리를 보존하면 안전해 보일 수 있지만, 그만큼 스트리핑으로 줄일 수 있는 크기도 줄어듭니다. JSON 저장 데이터, 리플렉션으로 생성하는 타입, 외부 SDK가 문서에서 보존을 요구하는 타입처럼 실제로 런타임 접근이 필요한 대상부터 명시하는 편이 좋습니다.

<br>

```xml
<linker>
  <!-- asmdef를 쓰지 않는 일반 스크립트의 타입 보존 -->
  <assembly fullname="Assembly-CSharp">
    <type fullname="MyGame.Save.PlayerSaveData" preserve="all"/>
  </assembly>

  <!-- asmdef를 사용하는 경우에는 해당 어셈블리 이름을 지정 -->
  <assembly fullname="MyGame.Runtime">
    <type fullname="MyGame.Analytics.AnalyticsEvent" preserve="all"/>
  </assembly>

  <!-- SDK 문서에서 요구하는 경우에만 어셈블리 전체 보존 -->
  <assembly fullname="ThirdParty.SDK" preserve="all"/>
</linker>
```

<br>

위 예시는 형식을 보여주기 위한 것이며, 실제 `fullname` 값은 프로젝트의 어셈블리 이름과 네임스페이스를 포함한 타입 이름에 맞춰야 합니다. `preserve="all"`은 해당 타입의 생성자, 필드, 메서드까지 보존하므로 JSON 역직렬화 대상처럼 런타임에 멤버 접근이 필요한 타입에 사용할 수 있습니다. 반대로 어셈블리 전체 보존은 범위가 넓으므로, 필요한 타입을 특정하기 어렵거나 SDK 문서에서 요구하는 경우에만 사용하는 편이 적절합니다.

따라서 `link.xml`은 스트리핑 레벨을 무작정 높이기 위한 안전장치라기보다, UnityLinker가 정적 분석만으로 알기 어려운 사용 경로를 보완하는 설정으로 보는 것이 좋습니다. 스트리핑 레벨을 올린 빌드는 저장 데이터 로드, JSON 파싱, 의존성 주입, 애널리틱스 초기화처럼 리플렉션이나 외부 SDK가 관여하는 경로를 중심으로 확인해야 합니다.

---

## 에셋 압축과 앱 사이즈

코드 스트리핑은 관리 코드와 실행 파일 쪽의 불필요한 부분을 줄이는 작업입니다. 하지만 모바일 빌드 크기를 크게 좌우하는 것은 대개 텍스처, 오디오, 모델, 영상 같은 에셋입니다.

따라서 앱 사이즈를 줄일 때는 코드 스트리핑만으로 끝내기보다, 어떤 에셋이 빌드에 포함되는지와 각 에셋이 어떤 압축 포맷으로 저장되는지를 함께 봐야 합니다. 특히 텍스처는 용량과 메모리 사용량 모두에 영향을 주므로, 모바일 빌드에서는 압축 포맷과 해상도 설정을 먼저 점검하는 편이 적절합니다.

### 플랫폼 크기 제한

스토어마다 앱 크기를 판단하는 기준은 다르고, 같은 플랫폼 안에서도 배포 방식에 따라 적용되는 조건이 달라질 수 있습니다. 그래서 빌드 크기를 관리할 때는 어떤 파일이 처음 설치 패키지에 들어가고 어떤 파일을 나중에 받을 수 있는지 나누어 보는 편이 좋습니다. 초기 설치에 꼭 필요한 리소스와 이후에 받을 수 있는 콘텐츠를 구분해 두면, 플랫폼 정책이 바뀌어도 빌드 구성을 조정하기 쉽기 때문입니다.

이런 분리 배포를 위해 각 플랫폼은 자체 기능을 제공합니다. Android에서는 App Bundle과 Play Asset Delivery가 대표적이고, iOS에서는 App Thinning, On-Demand Resources, Background Assets 같은 기능을 사용할 수 있습니다. 어떤 기능을 선택할지는 에셋의 크기, 다운로드 시점, 스토어 정책에 따라 달라지므로, 출시 전에는 Google Play Console과 App Store Connect의 최신 기준을 확인하는 것이 좋습니다.

실무 기준으로는 초기 설치에 꼭 필요한 코드, 첫 실행 리소스, 공통 UI, 기본 튜토리얼 정도만 기본 빌드에 남기고, 이후 콘텐츠나 선택적으로 쓰는 고해상도 에셋은 분리 배포 대상으로 검토하는 편이 좋습니다. 이렇게 나누어 두면 스토어 제한에 대응하기 쉬울 뿐 아니라, 사용자가 처음 게임을 설치하고 실행하기까지의 대기 시간도 줄일 수 있습니다.

### 텍스처 압축

빌드 크기를 줄일 때 가장 먼저 확인할 에셋은 텍스처입니다. 텍스처는 프로젝트 안에서 개수가 많고, 개별 파일의 해상도도 커지기 쉬워 전체 용량에서 큰 비중을 차지하기 때문입니다. 따라서 모바일 빌드에서는 텍스처의 최대 해상도와 압축 포맷을 먼저 점검하는 것이 적절합니다. 이 설정은 설치 크기뿐 아니라 런타임 메모리 사용량에도 영향을 줍니다.

모바일에서는 플랫폼 지원 범위를 확인한 뒤 **ASTC(Adaptive Scalable Texture Compression)**를 우선 검토하는 편이 좋습니다. ASTC는 블록 크기를 선택할 수 있어, 같은 포맷 안에서도 품질과 용량의 균형을 조정할 수 있기 때문입니다.

> 텍스처 블록 압축의 원리와 ETC2, ASTC 포맷의 차이는 [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 더 자세히 다룹니다.

ASTC를 사용할 때는 블록 크기를 텍스처 용도별로 나누는 것이 중요합니다. 4×4처럼 작은 블록은 품질을 더 잘 유지하지만 용량이 커지고, 6×6이나 8×8처럼 큰 블록은 용량을 줄이는 대신 세부 디테일이 손상될 수 있습니다. 그래서 UI, 폰트, 캐릭터 얼굴, 노멀맵처럼 품질 저하가 바로 보이는 텍스처는 보수적인 블록 크기에서 시작하는 편이 좋습니다. 반대로 원거리 배경, 반복 패턴이 많은 표면, 디테일 손실이 눈에 덜 띄는 디퓨즈 텍스처는 더 큰 블록을 검토할 수 있습니다.

텍스처 압축 설정은 실제 기기에서 확인한 뒤 확정하는 편이 좋습니다. 에디터에서는 크게 눈에 띄지 않던 색 번짐, 블록 노이즈, 작은 글자의 흐림, 노멀맵 하이라이트 깨짐이 모바일 화면에서는 더 잘 보일 수 있기 때문입니다. 따라서 빌드 크기를 줄이기 위해 블록 크기를 키우더라도, UI와 주요 캐릭터처럼 시선이 오래 머무는 텍스처는 품질을 확인하면서 보수적으로 조정하는 것이 안전합니다.

### 오디오 압축

오디오도 빌드 크기에 크게 영향을 줄 수 있습니다. 특히 BGM, 보이스, 긴 환경음처럼 길이가 긴 클립이 많으면 텍스처 압축만으로는 앱 크기를 충분히 줄이기 어렵습니다. 오디오는 클립 길이보다 용도를 기준으로 압축 방식과 로드 방식을 나누는 편이 좋습니다.

짧고 자주 재생되는 효과음은 재생 지연이 체감되기 쉬우므로, 메모리 사용량을 감수하고 빠르게 재생되는 설정을 선택할 수 있습니다. 반대로 BGM이나 긴 보이스처럼 재생 시간이 긴 클립은 처음부터 모두 메모리에 올리기보다 압축 상태로 두거나 스트리밍하는 편이 적절합니다. 핵심은 모든 오디오를 같은 설정으로 처리하지 않고, 재생 빈도와 길이, 지연 허용 범위에 따라 Import Settings를 나누는 것입니다.

모바일에서는 스테레오가 꼭 필요하지 않은 효과음을 모노로 바꾸는 것도 먼저 확인할 만한 항목입니다. 채널 수를 줄이면 파일 크기와 메모리 사용량을 줄일 수 있기 때문입니다. 샘플레이트도 마찬가지입니다. UI 효과음이나 짧은 피드백 사운드는 낮은 샘플레이트에서도 충분한 경우가 있지만, 보이스와 음악은 품질 저하가 더 잘 드러날 수 있으므로 실제 기기에서 들어 보며 조정하는 것이 좋습니다.

### 메쉬 압축

메쉬는 텍스처나 오디오보다 눈에 덜 띄는 경우가 많지만, 정점 수가 많은 캐릭터와 배경 모델이 쌓이면 빌드 크기에 영향을 줍니다. 특히 모바일에서는 같은 모델이 여러 LOD와 스킨드 메시로 함께 들어가는 경우가 있으므로, 메쉬 데이터도 import 단계에서 확인하는 편이 좋습니다.

먼저 볼 것은 압축률보다 불필요한 정점 데이터입니다. 노멀맵을 쓰지 않는 오브젝트라면 탄젠트가 필요하지 않을 수 있고, 라이트맵이나 별도 UV 기반 효과를 쓰지 않는다면 두 번째 UV도 제거할 수 있습니다. 이런 데이터는 메쉬마다 작아 보여도 모델 수가 늘어나면 누적되므로, Import Settings에서 실제로 필요한 vertex attribute만 남기는 것이 기본입니다.

그다음 Mesh Compression을 검토합니다. Mesh Compression은 정점 위치, 노멀, UV 같은 값을 더 적은 정밀도로 저장해 메쉬 데이터 크기를 줄이는 방식입니다. 압축 강도를 높이면 크기는 줄어들 수 있지만, 정점 위치가 미세하게 흔들리거나 노멀과 UV 정밀도가 떨어져 실루엣, 라이팅, 텍스처 경계가 어색해질 수 있습니다. 따라서 배경 소품이나 원거리 LOD처럼 오차가 눈에 덜 띄는 메쉬부터 적용하고, 캐릭터 얼굴, 손, 무기처럼 화면에서 자주 보이는 모델은 실제 기기에서 확인하면서 보수적으로 적용하는 편이 안전합니다.

---

## Play Asset Delivery와 On-Demand Resources

텍스처, 오디오, 메쉬를 압축한 뒤에도 모든 콘텐츠를 초기 설치 패키지에 넣으면 설치 크기와 첫 실행 대기 시간이 커질 수 있습니다. 시즌 콘텐츠, 고해상도 리소스, 특정 챕터에서만 쓰는 에셋처럼 처음 실행에 필요하지 않은 데이터는 나중에 받도록 분리하는 편이 좋습니다.

Unity 프로젝트에서는 Addressables로 에셋 참조와 로딩 단위를 나눌 수 있고, 배포 단계에서는 플랫폼이 제공하는 에셋 전달 기능을 함께 사용할 수 있습니다. Android의 Play Asset Delivery와 iOS의 On-Demand Resources는 초기 설치에 넣지 않은 에셋을 필요한 시점에 내려받도록 구성할 때 사용하는 대표적인 방식입니다.

> Addressables를 통한 에셋 그룹 구성과 온디맨드 로딩 전략은 [메모리 관리 (3) - Addressables와 에셋 전략](/dev/unity/MemoryManagement-3/)에서 더 자세히 다룹니다.

<br>

**Play Asset Delivery (Android)**

Play Asset Delivery는 Android App Bundle 안의 에셋을 여러 에셋 팩으로 나누고, 각 팩의 전달 시점을 지정하는 방식입니다. 처음 실행에 반드시 필요한 데이터는 설치 시점에 포함하고, 특정 모드나 챕터에서만 쓰는 데이터는 설치 후 또는 앱 실행 중 필요한 시점에 받도록 구성할 수 있습니다.

| 모드 | 전달 시점 | 적합한 에셋 | 주의할 점 |
|---|---|---|---|
| `install-time` | 앱 설치 시 함께 전달 | 첫 실행에 필요한 공통 리소스 | 초기 설치 크기와 설치 대기 시간이 늘어남 |
| `fast-follow` | 설치 직후 백그라운드에서 전달 | 초반 플레이에 곧 필요한 콘텐츠 | 다운로드 완료 전 접근하는 경우를 처리해야 함 |
| `on-demand` | 앱이 요청할 때 전달 | 선택 콘텐츠, 후반 챕터, 이벤트 리소스 | 진행률 표시, 실패 처리, 재시도 흐름이 필요함 |

<br>

**iOS On-Demand Resources**

iOS의 On-Demand Resources는 리소스에 태그를 붙여 묶고, 앱이 해당 태그를 요청할 때 App Store에서 내려받는 방식입니다. 특정 스테이지, 언어 리소스, 고해상도 에셋처럼 처음 설치에는 필요 없지만 특정 시점에 필요한 콘텐츠를 분리할 때 사용할 수 있습니다.

iOS는 On-Demand Resources로 받은 리소스를 계속 보관한다고 보장하지 않습니다. 앱에서 더 이상 사용하지 않는 리소스는 저장 공간 상황에 따라 정리될 수 있습니다. 따라서 필요한 시점보다 조금 앞서 요청하고, 다운로드 진행 중인 상태와 실패한 상태를 처리하는 흐름을 함께 만들어야 합니다.

<br>

Play Asset Delivery와 On-Demand Resources는 Addressables를 대체하는 기능이라기보다, 에셋을 전달하는 위치와 시점을 플랫폼 쪽에서 관리하게 해 주는 기능입니다. Addressables는 코드에서 에셋을 참조하고 로드하는 구조를 담당하고, 플랫폼 전달 기능은 그 에셋이 설치 패키지에 들어갈지, 스토어를 통해 나중에 내려받을지를 담당합니다.

원격 Addressables만 사용하는 경우에는 에셋 번들을 올려둘 서버나 CDN이 필요할 수 있습니다. 반대로 플랫폼 전달 기능을 함께 사용하면, 스토어가 제공하는 배포 경로를 통해 해당 에셋을 전달할 수 있습니다. 어느 방식을 쓰든 먼저 정해야 할 것은 같습니다. 첫 실행에 필요한 에셋과 나중에 받아도 되는 에셋을 구분하고, 나중에 받는 에셋에는 다운로드 대기와 실패 처리 흐름을 마련해야 합니다.

---

## Build Report로 빌드 크기 점검하기

빌드 크기는 한 번 줄여 두고 끝나는 값이 아닙니다. 새 에셋이 추가되거나 압축 설정, Addressables 그룹, 플랫폼별 import 설정이 바뀌면 최종 빌드에 포함되는 파일도 달라집니다.

그래서 모바일 빌드에서는 빌드가 끝난 뒤 **Build Report**를 확인하는 과정이 필요합니다. Build Report를 보면 텍스처, 오디오, 메쉬, 셰이더, 코드처럼 어떤 항목이 빌드 크기를 크게 차지하는지 대략적인 비중을 확인할 수 있습니다.

예를 들어 텍스처 비중이 크다면 압축 포맷, 최대 해상도, 밉맵 설정을 먼저 확인합니다. 오디오 비중이 크다면 긴 클립의 압축 방식과 로드 방식을 보고, 메쉬 비중이 크다면 불필요한 vertex attribute나 과도한 LOD 포함 여부를 확인합니다. Build Report는 어떤 최적화를 먼저 볼지 정하는 출발점으로 쓰는 것이 좋습니다.

빌드에 포함되지 말아야 할 에셋(개발용 텍스처, 테스트 프리팹, 사용하지 않는 폰트 등)이 포함되어 있는 경우가 빌드 크기 증가의 흔한 원인입니다. Resources 폴더에 넣은 에셋은 사용 여부와 관계없이 모두 빌드에 포함되므로, Resources 폴더 대신 Addressables를 사용하는 것이 크기 관리에도 유리합니다.

---

## 마무리

이 글의 핵심은 모바일 품질 전략을 런타임 설정과 빌드 구성으로 나누어 봐야 한다는 점입니다. 실행 중에는 기기 성능과 발열에 맞게 품질을 조정하고, 빌드 단계에서는 불필요한 코드와 에셋이 앱에 포함되지 않도록 관리해야 합니다.

- Quality Settings는 Low/Mid/High 같은 계층으로 나누되, 렌더 스케일, 그림자, 후처리, 셰이더 품질처럼 실제 비용이 큰 항목을 중심으로 차이를 둡니다.
- 디바이스 티어는 RAM만으로 확정하기보다 GPU 이름과 그래픽스 API 지원 여부를 함께 보고, 사용자가 설정 화면에서 품질을 조정할 수 있게 둡니다.
- `QualitySettings.SetQualityLevel()`은 현재 실행 중인 품질 레벨을 바꾸는 호출이므로, 선택한 티어를 다음 실행에서도 유지하려면 별도로 저장해야 합니다.
- IL2CPP 스트리핑은 빌드 크기를 줄이는 데 도움이 되지만, 리플렉션이나 외부 SDK가 사용하는 코드가 제거되지 않도록 Managed Stripping Level과 `link.xml`을 함께 관리해야 합니다.
- 텍스처, 오디오, 메쉬는 빌드 크기의 큰 비중을 차지하므로, 압축 포맷과 import 설정을 에셋 용도에 맞게 나누어야 합니다.
- 처음 실행에 필요하지 않은 콘텐츠는 Addressables와 플랫폼별 에셋 전달 기능을 이용해 나중에 받도록 분리할 수 있습니다.
- Build Report는 빌드 크기를 줄일 때 어떤 항목을 먼저 확인할지 정하는 출발점으로 사용합니다.

모바일 최적화는 한 가지 설정으로 끝나지 않습니다. 프레임 시간, 발열, 메모리, 빌드 크기, 다운로드 흐름이 서로 연결되어 있으므로, 품질 기준과 빌드 구성을 함께 조정해야 실제 기기에서 안정적인 결과를 얻을 수 있습니다.

[게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)에서 시작한 이 시리즈는 하나의 프레임이 만들어지는 과정을 여러 관점에서 나누어 살펴보았습니다. 렌더링과 GPU, 스크립트와 메모리, UI와 조명, 셰이더와 물리, 파티클과 애니메이션, 프로파일링과 모바일 전략은 모두 같은 프레임 안에서 서로 영향을 주는 요소입니다.

최적화는 이 요소들 중 어디에서 비용이 커지는지 찾고, 그 원리를 이해한 뒤, 상황에 맞는 방법을 적용하는 과정입니다. 프레임의 구조를 이해하면 병목을 더 정확히 볼 수 있고, 병목을 정확히 보면 어떤 최적화가 필요한지도 분명해집니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)

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
- [셰이더 최적화 (2) - 셰이더 배리언트와 키워드 관리](/dev/unity/ShaderOptimization-2/)
- [물리 최적화 (1) - 물리 엔진의 실행 구조](/dev/unity/PhysicsOptimization-1/)
- [물리 최적화 (2) - 물리 최적화 전략](/dev/unity/PhysicsOptimization-2/)
- [파티클과 애니메이션 (1) - 파티클 시스템 최적화](/dev/unity/ParticleAndAnimation-1/)
- [파티클과 애니메이션 (2) - 애니메이션 최적화](/dev/unity/ParticleAndAnimation-2/)
- [프로파일링 (1) - Unity Profiler와 Frame Debugger](/dev/unity/Profiling-1/)
- [프로파일링 (2) - 모바일 프로파일링](/dev/unity/Profiling-2/)
- [모바일 전략 (1) - 발열과 배터리](/dev/unity/MobileStrategy-1/)
- **모바일 전략 (2) - 빌드와 품질 전략** (현재 글)
