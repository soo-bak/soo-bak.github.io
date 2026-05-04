---
layout: single
title: "하드웨어 기초 (3) - GPU의 탄생과 발전 - soo:bak"
date: "2026-02-22 01:08:00 +0900"
description: CPU의 그래픽 처리 한계, 고정 기능 GPU, 프로그래머블 셰이더, 통합 셰이더, GPGPU를 설명합니다.
tags:
  - Unity
  - 하드웨어
  - GPU
  - 셰이더
  - 모바일
---

## 그래픽 처리를 전담하는 칩의 등장

[하드웨어 기초 (1)](/dev/unity/HardwareBasics-1/)과 [(2)](/dev/unity/HardwareBasics-2/)에서 다루었듯이, CPU는 복잡한 제어 흐름(분기, 의존성 처리)을 빠르게 처리하도록 설계된 프로세서이며, 파이프라인과 메모리 계층도 이 연산 특성에 맞춰 설계되어 있습니다. 소수의 코어가 높은 IPC를 유지하며 순차적으로 작업을 수행하는 구조입니다.

<br>

1990년대 중반 3D 그래픽이 게임에 본격적으로 도입되면서 이 구조의 한계가 드러났습니다. 3D 그래픽 처리는 수만~수십만 개의 정점과 픽셀 각각에 대해 동일한 종류의 연산(좌표 변환, 조명 계산, 텍스처 샘플링)을 독립적으로 수행하는 작업입니다. 각 연산 자체의 복잡도보다, 같은 연산을 대량의 데이터에 동시 적용해야 한다는 점이 핵심입니다. CPU의 강점인 "복잡한 작업의 빠른 순차 처리"와 그래픽의 요구인 "동일한 연산의 대량 병렬 처리"는 근본적으로 맞지 않았고, 이 불일치를 해결하기 위해 등장한 것이 GPU입니다.

<br>

이 글에서는 CPU가 그래픽을 직접 처리하던 소프트웨어 렌더링 시대부터, 고정 기능 GPU, 프로그래머블 셰이더, 통합 셰이더 아키텍처, GPGPU까지 GPU의 발전 과정을 시간 순서대로 다룹니다. 각 단계에서 존재했던 구체적인 한계와, 그 한계를 극복하기 위한 아키텍처 전환의 흐름을 함께 정리합니다.

<br>

---

## CPU로 그래픽을 처리하던 시대

GPU가 존재하기 이전, 3D 그래픽의 모든 계산은 CPU가 담당했습니다. 이 방식을 **소프트웨어 렌더링(Software Rendering)**이라고 합니다.

3D 장면의 정점(vertex, 삼각형의 꼭짓점) 좌표를 변환하고, 삼각형을 화면의 픽셀로 변환하는 **래스터화(rasterization)**를 수행하고, 각 픽셀의 색상을 계산한 뒤, 결과를 **프레임버퍼**(화면에 출력할 최종 이미지가 저장되는 메모리 영역)에 기록하는 작업 전체를 CPU 명령어로 처리했습니다.

<br>

1996년에 출시된 id Software의 **Quake**는 소프트웨어 렌더링의 대표적인 사례입니다. Quake는 완전한 3D 환경을 실시간으로 렌더링한 최초의 상용 게임 중 하나로, John Carmack이 C와 어셈블리로 작성한 소프트웨어 렌더러가 CPU만으로 3D 장면을 그렸습니다. 최소 사양은 Pentium 75MHz였고, 원활한 플레이에는 Pentium 133~166MHz가 필요했습니다. 소프트웨어 렌더링 모드의 기본 해상도는 320x200이었습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">소프트웨어 렌더링의 처리 흐름 (CPU)</text>
  <rect x="40" y="40" width="500" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="64" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1. 정점 변환</text>
  <text x="180" y="64" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">3D 좌표 → 2D 화면 좌표 (행렬 곱셈, 원근 나눗셈)</text>
  <line x1="290" y1="80" x2="290" y2="92" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="290,96 286,88 294,88" fill="currentColor"/>
  <rect x="40" y="96" width="500" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="120" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2. 래스터화</text>
  <text x="180" y="120" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">삼각형 → 픽셀 단위 분해 (스캔라인 알고리즘)</text>
  <line x1="290" y1="136" x2="290" y2="148" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="290,152 286,144 294,144" fill="currentColor"/>
  <rect x="40" y="152" width="500" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="176" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">3. 픽셀 색상 계산</text>
  <text x="200" y="176" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">텍스처 샘플링, 조명, 보간</text>
  <line x1="290" y1="192" x2="290" y2="204" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="290,208 286,200 294,200" fill="currentColor"/>
  <rect x="40" y="208" width="500" height="40" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="60" y="232" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">4. 프레임버퍼에 기록</text>
  <text x="290" y="276" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.85">모든 단계를 CPU가 범용 명령어로 처리</text>
</svg>
</div>

<br>

이 방식에는 근본적인 한계가 있었습니다.

화면 해상도가 높아지면 처리해야 할 픽셀 수가 급증합니다. 320x200 해상도에서는 64,000개의 픽셀이지만, 640x480에서는 307,200개로 약 5배 늘어납니다.

각 픽셀마다 텍스처 좌표를 보간하고, 텍스처 메모리에서 색상을 읽어오고, 조명을 계산해야 합니다. 당시 Pentium은 슈퍼스칼라 구조였지만 동시에 처리할 수 있는 명령어 수는 클럭당 최대 2개에 불과했으므로, 수만~수십만 개 픽셀 각각에 대한 연산을 CPU 혼자 감당해야 했습니다.

<br>

해상도뿐 아니라 장면의 복잡도도 CPU 부하를 높였습니다.

3D 장면을 구성하는 **폴리곤(polygon, 삼각형)**의 수가 늘어나면, 각 삼각형의 정점을 변환하는 데 드는 CPU 사이클도 비례하여 증가합니다.

Quake의 캐릭터 모델은 200~400개의 폴리곤으로 구성되었고, 장면 전체의 폴리곤 수가 수천 개를 넘으면 정점 변환에만 CPU 연산 시간의 상당 부분이 소비되었습니다.

픽셀 처리와 정점 처리가 모두 같은 CPU 자원을 놓고 경쟁하는 구조였으므로, 해상도를 높이면 폴리곤을 줄여야 하고, 폴리곤을 늘리면 해상도를 낮춰야 하는 트레이드오프가 존재했습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">소프트웨어 렌더링의 한계 — 동일한 CPU 자원을 공유</text>
  <text x="290" y="46" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">정점 변환(폴리곤 수 비례) + 픽셀 색상 계산(해상도 비례) + 게임 로직 · AI · 물리 연산</text>
  <line x1="40" y1="64" x2="540" y2="64" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="60" y="98" font-family="sans-serif" font-size="11" fill="currentColor">폴리곤 ↑</text>
  <text x="160" y="98" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 정점 처리 ↑</text>
  <text x="320" y="98" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 픽셀 처리 부족</text>
  <text x="60" y="128" font-family="sans-serif" font-size="11" fill="currentColor">해상도 ↑</text>
  <text x="160" y="128" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 픽셀 처리 ↑</text>
  <text x="320" y="128" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 정점 처리 부족</text>
  <text x="60" y="158" font-family="sans-serif" font-size="11" fill="currentColor">그래픽 ↑</text>
  <text x="160" y="158" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 게임 로직에 할당할 여유 부족</text>
</svg>
</div>

<br>

그래픽 연산만으로 CPU를 모두 소진하면, 게임 로직이나 AI 판단에 할당할 사이클이 부족해져 입력 반응이 느려지거나 AI가 멈추는 현상이 발생했습니다.

결국 소프트웨어 렌더링으로는 해상도, 장면 복잡도, 게임 로직 복잡도를 동시에 높이는 것이 불가능했습니다.

<br>

이 한계를 돌파하기 위해, 그래픽 처리만을 전담하는 별도의 하드웨어가 필요했습니다.

---

## 고정 기능 GPU의 등장

1996년, **3dfx**가 **Voodoo Graphics** 카드를 출시했습니다.

같은 시기에 S3 ViRGE 같은 2D/3D 통합 칩도 존재했지만, 3D 가속 성능이 미미하여 "3D 감속기(decelerator)"라는 별명이 붙을 정도였습니다.

Voodoo는 3D 가속 성능을 실제로 체감할 수 있는 수준으로 끌어올린 최초의 대중적 3D 게임 가속 카드였습니다.

Voodoo는 3D 전용 칩으로, 2D 출력 기능이 없어서 기존 2D VGA 카드에 패스스루(pass-through) 케이블로 연결해야 했습니다. 3D 게임이 실행될 때만 Voodoo가 출력을 넘겨받는 구조였습니다.

연산 측면에서는, CPU가 정점 변환을 수행한 뒤 래스터화와 텍스처 매핑(삼각형 표면에 텍스처 이미지를 입히는 작업)을 Voodoo 칩이 담당했습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">3dfx Voodoo 시대의 작업 분담</text>
  <rect x="40" y="46" width="220" height="160" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="68" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <text x="60" y="98" font-family="sans-serif" font-size="11" fill="currentColor">· 정점 변환 (좌표 계산)</text>
  <text x="60" y="120" font-family="sans-serif" font-size="11" fill="currentColor">· 게임 로직</text>
  <text x="60" y="142" font-family="sans-serif" font-size="11" fill="currentColor">· AI · 물리</text>
  <line x1="262" y1="120" x2="336" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="340,120 332,116 332,124" fill="currentColor"/>
  <rect x="340" y="46" width="220" height="160" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="68" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">Voodoo (3D 가속)</text>
  <text x="360" y="98" font-family="sans-serif" font-size="11" fill="currentColor">· 래스터화</text>
  <text x="360" y="120" font-family="sans-serif" font-size="11" fill="currentColor">· 텍스처 매핑</text>
  <text x="360" y="142" font-family="sans-serif" font-size="11" fill="currentColor">· 깊이 테스트</text>
  <text x="360" y="164" font-family="sans-serif" font-size="11" fill="currentColor">· 프레임버퍼 기록</text>
  <text x="300" y="246" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.85">CPU의 부담이 줄어듦 — 래스터화·텍스처 연산을 전용 하드웨어가 처리</text>
</svg>
</div>

<br>

Voodoo의 핵심은 **텍스처 매핑 유닛(TMU, Texture Mapping Unit)**과 래스터화 하드웨어였습니다.

TMU는 삼각형 표면에 텍스처를 입히는 연산(텍스처 좌표 보간, 텍스처 메모리에서 텍셀(texel, 텍스처의 픽셀) 읽기, 필터링)을 전용 회로로 수행했습니다. CPU가 소프트웨어로 처리하던 것과 동일한 연산이지만, 전용 회로가 병렬로 처리하므로 속도 차이가 컸습니다.

Quake를 소프트웨어 렌더링으로 실행하면 320x200 해상도에서 Pentium 166MHz 기준 약 30fps가 한계였지만, Voodoo를 장착하면 약 5배 넓은 640x480 해상도에서도 유사한 프레임 레이트를 유지할 수 있었습니다.

<br>

1998년에 출시된 **NVIDIA RIVA TNT(TwiN Texel)**는 두 개의 픽셀 파이프라인을 갖추어 클럭당 두 텍셀을 동시에 처리할 수 있었습니다.

단일 파이프라인이었던 Voodoo 대비 픽셀 필레이트가 두 배로 늘어난 구조입니다. TNT는 2D 가속과 3D 가속을 하나의 칩에 통합한 점에서도 차별화되었습니다. Voodoo는 3D 전용이어서 별도의 2D 카드와 함께 사용해야 했지만, TNT는 단독으로 사용할 수 있었습니다.

<br>

1999년에 출시된 **NVIDIA GeForce 256**은 GPU(Graphics Processing Unit)라는 용어를 대중화한 제품입니다.

NVIDIA는 GeForce 256을 "T&L, 삼각형 셋업, 렌더링 엔진을 통합한 단일 칩 프로세서"로 정의하며, 이를 최초의 GPU로 마케팅했습니다.

GeForce 256의 핵심 기능은 **하드웨어 T&L(Transform and Lighting)**이었습니다. T&L은 정점의 좌표 변환(Transform)과 조명 계산(Lighting)을 의미합니다.

이전까지 CPU가 담당하던 정점 변환과 조명 계산을 GPU 하드웨어가 처리하게 된 것입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 600 360" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">하드웨어 T&amp;L의 도입 (GeForce 256)</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이전 (Voodoo, TNT) — CPU가 정점 변환·조명을 처리</text>
  <rect x="40" y="60" width="220" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU</text>
  <text x="60" y="100" font-family="sans-serif" font-size="10" fill="currentColor">· 정점 변환 (T)</text>
  <text x="60" y="115" font-family="sans-serif" font-size="10" fill="currentColor">· 조명 계산 (L)</text>
  <text x="60" y="130" font-family="sans-serif" font-size="10" fill="currentColor">· 게임 로직</text>
  <line x1="262" y1="100" x2="336" y2="100" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="340,100 332,96 332,104" fill="currentColor"/>
  <rect x="340" y="60" width="220" height="80" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU</text>
  <text x="360" y="100" font-family="sans-serif" font-size="10" fill="currentColor">· 래스터화</text>
  <text x="360" y="115" font-family="sans-serif" font-size="10" fill="currentColor">· 텍스처 매핑</text>
  <text x="360" y="130" font-family="sans-serif" font-size="10" fill="currentColor">· 깊이 테스트</text>
  <line x1="40" y1="166" x2="560" y2="166" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="194" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이후 (GeForce 256) — 정점 변환·조명이 GPU로 이동</text>
  <rect x="40" y="206" width="220" height="80" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="226" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU</text>
  <text x="60" y="246" font-family="sans-serif" font-size="10" fill="currentColor">· 게임 로직</text>
  <text x="60" y="261" font-family="sans-serif" font-size="10" fill="currentColor">· AI · 물리</text>
  <line x1="262" y1="246" x2="336" y2="246" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="340,246 332,242 332,250" fill="currentColor"/>
  <rect x="340" y="206" width="220" height="80" rx="5" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.5"/>
  <text x="450" y="226" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU</text>
  <text x="360" y="244" font-family="sans-serif" font-size="10" fill="currentColor">· 정점 변환 (T) · 조명 계산 (L)</text>
  <text x="360" y="258" font-family="sans-serif" font-size="10" fill="currentColor">· 래스터화 · 텍스처 매핑</text>
  <text x="360" y="272" font-family="sans-serif" font-size="10" fill="currentColor">· 깊이 테스트</text>
  <text x="300" y="328" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.85">CPU가 그래픽 연산에서 거의 해방됨</text>
</svg>
</div>

<br>

하드웨어 T&L이 도입되면서, 정점 변환과 조명 계산에 소비되던 CPU 사이클이 GPU로 넘어갔습니다.

CPU는 그만큼 게임 로직에 집중할 수 있게 되었고, 장면에 사용할 수 있는 폴리곤 수도 크게 늘어났습니다.

NVIDIA의 사양에 따르면 GeForce 256은 초당 최소 1,000만 폴리곤, 최대 1,500만 폴리곤의 T&L 처리량을 제공했습니다. 이전 세대에서 CPU가 초당 수십만~수백만 개의 정점을 처리하던 것과 비교하면, 실시간 장면의 복잡도가 한 단계 올라간 수준입니다.

<br>

하지만 이 시기의 GPU에는 근본적인 제약이 있었습니다.

모든 연산이 **하드웨어에 고정(Fixed Function)**되어 있었다는 점입니다.

정점 변환은 행렬 곱셈으로만 수행되었고, 조명은 Gouraud 셰이딩(정점 단위 조명 보간)이나 Phong 조명 모델(앰비언트·디퓨즈·스페큘러 성분의 합산) 같은 미리 정해진 알고리즘만 사용할 수 있었습니다.

텍스처 매핑도 정해진 방식(텍스처 읽기 후 색상 곱하기 또는 더하기)만 가능했습니다.

<br>

카툰 셰이딩, 프레넬 반사 같은 효과를 구현하려 해도, GPU 하드웨어가 지원하지 않으면 방법이 없었습니다.

개발자가 파이프라인에 개입할 수 있는 범위는 행렬 값, 조명 위치, 텍스처 블렌딩 모드 같은 파라미터 설정뿐이었고, 알고리즘 자체를 변경하려면 GPU 하드웨어가 바뀌어야 했습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">고정 기능 GPU의 한계</text>
  <text x="40" y="46" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">고정 기능 파이프라인</text>
  <rect x="20" y="58" width="140" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">정점 변환</text>
  <text x="90" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">행렬 곱셈</text>
  <line x1="160" y1="76" x2="178" y2="76" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="182,76 174,72 174,80" fill="currentColor"/>
  <rect x="182" y="58" width="140" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="252" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">조명 계산</text>
  <text x="252" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">Gouraud</text>
  <line x1="322" y1="76" x2="340" y2="76" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="344,76 336,72 336,80" fill="currentColor"/>
  <rect x="344" y="58" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="394" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">래스터화</text>
  <line x1="444" y1="76" x2="462" y2="76" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="466,76 458,72 458,80" fill="currentColor"/>
  <rect x="466" y="58" width="140" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="536" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">텍스처 매핑</text>
  <text x="536" y="89" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">고정 블렌딩</text>
  <text x="40" y="124" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 각 단계의 알고리즘이 하드웨어에 내장되어 있음</text>
  <text x="40" y="142" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 개발자는 파라미터(행렬 값, 조명 위치 등)만 설정 가능</text>
  <text x="40" y="160" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 알고리즘 자체를 바꾸는 것은 불가능</text>
  <line x1="40" y1="184" x2="580" y2="184" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="208" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">지원하는 효과</text>
  <text x="40" y="226" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">텍스처 매핑, Gouraud 셰이딩, 안개 등</text>
  <text x="40" y="262" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">지원하지 않는 효과</text>
  <text x="40" y="280" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">카툰 셰이딩, 노멀 매핑, 프레넬 반사, 커스텀 조명 모델 등</text>
</svg>
</div>

<br>

이 한계를 넘어서려면, GPU의 파이프라인 일부를 개발자가 직접 프로그래밍할 수 있어야 했습니다.

---

## 정점 처리와 픽셀 처리의 분리

앞 섹션에서 다룬 고정 기능 GPU의 한계는 "알고리즘을 바꿀 수 없다"는 점이었습니다.

여기에 더해, 이 시기의 GPU에는 구조적인 비효율이 하나 더 있었습니다. 정점을 처리하는 유닛과 픽셀을 처리하는 유닛이 물리적으로 분리되어 있었다는 점입니다.

이 분리 구조는 이후 프로그래머블 셰이더가 도입된 뒤에도 그대로 유지되었고, 통합 셰이더 아키텍처가 등장해서야 해소되었습니다.

<br>

GPU 렌더링 파이프라인에서 정점 처리와 픽셀 처리는 다루는 데이터의 단위와 연산 내용이 다릅니다.

정점 처리는 메쉬의 각 정점에 대해 좌표 변환과 조명을 계산하는 작업으로, 데이터 단위가 정점입니다.

픽셀 처리는 래스터화된 각 **프래그먼트(fragment)**에 대해 텍스처를 읽고 최종 색상을 계산하는 작업으로, 데이터 단위가 프래그먼트입니다. 프래그먼트는 래스터화 단계에서 생성되는 "최종 픽셀이 될 후보 데이터"로, 화면의 한 픽셀 위치에 여러 삼각형이 겹치면 해당 위치에 여러 프래그먼트가 생성됩니다. 이 중 어떤 프래그먼트가 최종 픽셀 색상이 될지는 깊이 테스트 등의 과정을 거쳐 결정됩니다.

<br>

이 두 작업의 성격이 다르기 때문에, GPU는 정점 전용 유닛과 픽셀 전용 유닛을 물리적으로 나누어 설계했습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">정점 유닛과 픽셀 유닛의 물리적 분리</text>
  <text x="40" y="50" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 유닛 (3개, 고정)</text>
  <rect x="40" y="60" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="62" y="82" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">V0</text>
  <rect x="92" y="60" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="114" y="82" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">V1</text>
  <rect x="144" y="60" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="166" y="82" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">V2</text>
  <line x1="200" y1="120" x2="240" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="244,120 236,116 236,124" fill="currentColor"/>
  <rect x="244" y="106" width="120" height="28" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="304" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">래스터화</text>
  <line x1="364" y1="120" x2="404" y2="120" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="408,120 400,116 400,124" fill="currentColor"/>
  <text x="40" y="160" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">픽셀 유닛 (10개, 고정)</text>
  <rect x="40" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="62" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P0</text>
  <rect x="92" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="114" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P1</text>
  <rect x="144" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="166" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P2</text>
  <rect x="196" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="218" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P3</text>
  <rect x="248" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="270" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P4</text>
  <rect x="300" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="322" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P5</text>
  <rect x="352" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="374" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P6</text>
  <rect x="404" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="426" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P7</text>
  <rect x="456" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="478" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P8</text>
  <rect x="508" y="170" width="44" height="34" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/><text x="530" y="192" text-anchor="middle" font-family="monospace" font-size="11" fill="currentColor">P9</text>
  <text x="40" y="234" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 프래그먼트 수가 정점 수보다 훨씬 많으므로, 픽셀 유닛이 더 많음</text>
  <text x="40" y="252" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 두 유닛의 비율은 칩 설계 시 고정되어 실행 중에는 바꿀 수 없음</text>
</svg>
</div>

<br>

정점 유닛의 수와 픽셀 유닛의 수는 GPU 칩 설계 시점에 고정됩니다.

일반적인 3D 장면에서는 정점 수보다 프래그먼트 수가 훨씬 많습니다. 정점 1,000개의 메쉬가 화면에 크게 그려지면 수십만 개의 프래그먼트가 생성되므로, GPU는 픽셀 유닛을 정점 유닛보다 많이 배치했습니다. 실제로 GeForce 7800 GTX는 정점 유닛 8개, 픽셀 유닛 24개로, 3:1 비율이었습니다.

<br>

이 고정된 비율이 **부하 불균형(Load Imbalance)** 문제를 일으켰습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">부하 불균형 문제</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">장면 A: 정점이 적고, 화면을 가득 채우는 큰 삼각형</text>
  <text x="40" y="74" font-family="sans-serif" font-size="10" fill="currentColor">정점 유닛</text>
  <rect x="120" y="64" width="40" height="20" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.8"/>
  <rect x="160" y="64" width="320" height="20" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="320" y="78" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">유휴</text>
  <text x="40" y="100" font-family="sans-serif" font-size="10" fill="currentColor">픽셀 유닛</text>
  <rect x="120" y="90" width="360" height="20" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="0.8"/>
  <text x="300" y="104" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">과부하</text>
  <text x="60" y="132" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">→ 픽셀 유닛이 병목. 정점 유닛은 남아도는데 도울 수 없음.</text>
  <line x1="40" y1="158" x2="580" y2="158" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="186" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">장면 B: 정점이 매우 많고, 화면에 작게 그려지는 오브젝트 다수</text>
  <text x="40" y="212" font-family="sans-serif" font-size="10" fill="currentColor">정점 유닛</text>
  <rect x="120" y="202" width="360" height="20" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="0.8"/>
  <text x="300" y="216" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">과부하</text>
  <text x="40" y="238" font-family="sans-serif" font-size="10" fill="currentColor">픽셀 유닛</text>
  <rect x="120" y="228" width="100" height="20" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.8"/>
  <rect x="220" y="228" width="260" height="20" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.5"/>
  <text x="350" y="242" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.6">유휴</text>
  <text x="60" y="270" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">→ 정점 유닛이 병목. 픽셀 유닛은 남아도는데 도울 수 없음.</text>
  <line x1="40" y1="294" x2="580" y2="294" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="310" y="324" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">어떤 장면이든 유휴 유닛의 연산 능력이 낭비됨</text>
  <text x="310" y="346" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">하드웨어 자원의 일부가 항상 사용되지 않는 비효율적 구조</text>
</svg>
</div>

<br>

장면의 특성에 따라 병목이 정점 쪽에 걸릴 수도, 픽셀 쪽에 걸릴 수도 있지만, 유닛 비율은 칩에 고정되어 있으므로 항상 한쪽은 유휴 상태가 됩니다.

정점 유닛이 유휴 상태일 때 그 연산 능력을 픽셀 처리에 빌려줄 수 없고, 반대의 경우에도 마찬가지입니다.

이 비효율은 프로그래머블 셰이더가 도입된 뒤에도 유닛 분리 구조 자체는 바뀌지 않았기 때문에 그대로 남아 있었고, 통합 셰이더 아키텍처가 등장해서야 해소되었습니다.

---

## 프로그래머블 셰이더의 등장

2001년, NVIDIA가 **GeForce 3**를 출시하면서 GPU의 연산 방식이 바뀌기 시작했습니다.

GeForce 3는 **Shader Model 1.0**(DirectX 8.0, 셰이더 프로파일 vs_1_1/ps_1_1)을 지원하는 최초의 GPU로, 정점 처리와 픽셀 처리의 알고리즘을 개발자가 직접 프로그래밍할 수 있게 되었습니다.

<br>

고정 기능 GPU에서는 정점 변환과 조명 계산이 하드웨어에 내장된 알고리즘으로만 수행되었고, 개발자는 행렬 값이나 조명 파라미터 같은 입력만 바꿀 수 있었습니다.

프로그래머블 셰이더는 이 구조를 바꾸어, **개발자가 작성한 셰이더 프로그램**이 GPU에서 실행되도록 했습니다.

정점 하나를 어떻게 변환할지, 프래그먼트 하나의 색상을 어떻게 계산할지를 코드로 정의할 수 있게 된 것입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">고정 기능 vs 프로그래머블 셰이더</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">고정 기능 (GeForce 256 시대)</text>
  <rect x="40" y="60" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 입력</text>
  <line x1="140" y1="78" x2="158" y2="78" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="162,78 154,74 154,82" fill="currentColor"/>
  <rect x="162" y="60" width="120" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="222" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">하드웨어 T&amp;L</text>
  <line x1="282" y1="78" x2="300" y2="78" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="304,78 296,74 296,82" fill="currentColor"/>
  <rect x="304" y="60" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="354" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">래스터화</text>
  <line x1="404" y1="78" x2="422" y2="78" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="426,78 418,74 418,82" fill="currentColor"/>
  <rect x="426" y="60" width="160" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="506" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">하드웨어 텍스처 매핑</text>
  <text x="40" y="118" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">개발자 제어 범위: 파라미터(행렬 값, 조명 위치 등). 알고리즘 변경 불가.</text>
  <line x1="40" y1="138" x2="580" y2="138" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="166" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프로그래머블 (GeForce 3 이후)</text>
  <rect x="40" y="178" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="90" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 입력</text>
  <line x1="140" y1="196" x2="158" y2="196" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="162,196 154,192 154,200" fill="currentColor"/>
  <rect x="162" y="178" width="120" height="36" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="222" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">버텍스 셰이더</text>
  <line x1="282" y1="196" x2="300" y2="196" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="304,196 296,192 296,200" fill="currentColor"/>
  <rect x="304" y="178" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="354" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">래스터화</text>
  <line x1="404" y1="196" x2="422" y2="196" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="426,196 418,192 418,200" fill="currentColor"/>
  <rect x="426" y="178" width="160" height="36" rx="4" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="1.2"/>
  <text x="506" y="200" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">픽셀 셰이더</text>
  <text x="40" y="236" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">개발자 제어 범위: 연산 알고리즘 자체를 코드로 작성.</text>
  <text x="310" y="284" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.85">정점 변환과 색상 계산 방식을 개발자가 직접 정의 가능</text>
</svg>
</div>

<br>

초기의 프로그래머블 셰이더는 제한적이었습니다.

Shader Model 1.0의 버텍스 셰이더는 128개의 명령어 슬롯까지만 사용할 수 있었고, 픽셀 셰이더는 텍스처 명령어 4개와 산술 명령어 8개만 지원했습니다.

반복문이나 조건 분기도 없었으므로, 모든 연산을 직선 코드(straight-line code)로 나열해야 했고 복잡한 효과를 구현하기 어려웠습니다.

<br>

이후 Shader Model은 세대마다 명령어 수, 흐름 제어, 셰이더 종류를 확장하며 발전했습니다.

<br>

**Shader Model의 발전 과정**

| 버전 | 출시 | 주요 변화 |
|:---:|:---:|:---|
| SM 1.0 | 2001 | 최초의 프로그래머블 셰이더 · 명령어 슬롯 제한(VS: 128, PS: 텍스처 4 + 산술 8) · 반복문, 분기 없음 |
| SM 2.0 | 2002 | 명령어 슬롯 확대(VS: 256, PS: 텍스처 32 + 산술 64 = 96) · 정적 분기(Static Branch) 지원 · 부동소수점(float) 연산 정밀도 향상 |
| SM 3.0 | 2004 | 동적 분기(Dynamic Branch) 지원 · 명령어 슬롯 최소 512, 최대 32,768 · 버텍스 셰이더에서 텍스처 읽기 가능 (Vertex Texture Fetch) |
| SM 4.0 | 2006 | 통합 셰이더 아키텍처 · 지오메트리 셰이더 추가 · 정수 연산 지원 |
| SM 5.0 | 2009 | 테셀레이션 셰이더 추가 · 컴퓨트 셰이더 추가 · 배정밀도(double) 연산 |

<br>

SM 2.0에서는 픽셀 셰이더의 명령어 슬롯이 96개로 늘어나고 부동소수점 정밀도가 향상되면서, 범프 매핑(노멀 맵으로 표면의 요철을 표현하는 기법)이나 픽셀 단위 조명(per-pixel lighting) 같은 효과를 구현할 수 있게 되었습니다.

SM 3.0에서는 동적 분기(실행 중 조건에 따라 다른 경로를 실행하는 if문)가 지원되면서, 하나의 셰이더가 재질이나 조명 조건에 따라 다른 연산을 수행할 수 있게 되었습니다.

<br>

프로그래머블 셰이더의 등장과 함께 **셰이더 언어(Shading Language)**도 발전했습니다.

초기에는 어셈블리 수준의 저수준 명령어로 셰이더를 작성해야 했습니다. 레지스터와 명령어 코드를 직접 다루어야 했으므로, 셰이더가 길어지면 작성과 유지보수가 어려웠습니다.

이후 C와 유사한 문법의 고수준 셰이더 언어가 등장하면서, 변수·함수·제어 구조를 사용해 셰이더를 작성할 수 있게 되었습니다.

<br>

**주요 셰이더 언어**

| 언어 | 제작사 | 특징 |
|:---|:---|:---|
| HLSL | Microsoft | DirectX 전용, Windows/Xbox 플랫폼 · Unity의 셰이더도 HLSL 기반 |
| GLSL | Khronos | OpenGL 용 (Vulkan은 SPIR-V 경유) · 크로스 플랫폼, 모바일 OpenGL ES에서도 사용 |
| Cg | NVIDIA | "C for Graphics" · HLSL과 문법이 거의 동일, DirectX/OpenGL 양쪽 지원 · 2012년 개발 중단, HLSL이 대체 |
| MSL | Apple | Metal Shading Language · Apple 플랫폼 전용, C++14 기반 문법 |

<br>

Unity의 셰이더는 **HLSL(High-Level Shading Language)**로 작성합니다.

빌드 시점에 대상 플랫폼에 맞게 크로스 컴파일되므로, 개발자는 HLSL로만 작성하면 OpenGL(GLSL), Apple(MSL), Vulkan(SPIR-V) 등 모든 플랫폼을 지원할 수 있습니다.

<br>

프로그래머블 셰이더의 등장으로 GPU는 "고정된 기능을 수행하는 하드웨어"에서 "개발자가 프로그래밍할 수 있는 프로세서"로 전환되었습니다. 카툰 셰이딩, 환경 매핑, 서브서피스 스캐터링, 패럴랙스 매핑 등 고정 기능으로는 불가능했던 렌더링 기법이 이 전환을 통해 구현 가능해졌습니다.

---

## 통합 셰이더 아키텍처

2006년, NVIDIA가 **GeForce 8800 GTX**를 출시하면서 GPU 아키텍처가 다시 바뀌었습니다. 이 GPU는 **통합 셰이더 아키텍처(Unified Shader Architecture)**를 채택한 최초의 데스크톱 GPU였습니다. (Xbox 360의 Xenos GPU가 2005년에 먼저 통합 셰이더를 채택했지만, PC용 GPU에서는 GeForce 8800이 최초입니다.)

<br>

앞서 살펴본 것처럼, 이전 세대의 GPU에는 정점 전용 유닛과 픽셀 전용 유닛이 물리적으로 분리되어 있었습니다. 정점 유닛은 버텍스 셰이더만, 픽셀 유닛은 픽셀 셰이더만 실행할 수 있었고, 한쪽이 유휴 상태여도 다른 쪽의 부하를 분담할 수 없는 구조였습니다.

<br>

통합 셰이더 아키텍처는 이 구분을 없앴습니다.

정점 전용 유닛과 픽셀 전용 유닛 대신, **범용 셰이더 코어(Unified Shader Core)**가 도입되었습니다.

하나의 셰이더 코어가 버텍스 셰이더와 픽셀 셰이더를 모두 실행할 수 있으며, 이후 추가된 셰이더 종류(지오메트리, 테셀레이션, 컴퓨트)도 같은 코어에서 실행됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">분리형 vs 통합형 아키텍처</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">분리형 (GeForce 7 시대)</text>
  <text x="40" y="72" font-family="sans-serif" font-size="10" fill="currentColor">정점 전용 유닛 ×8</text>
  <text x="200" y="72" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">— 버텍스 셰이더만 실행 가능</text>
  <text x="40" y="92" font-family="sans-serif" font-size="10" fill="currentColor">픽셀 전용 유닛 ×24</text>
  <text x="200" y="92" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">— 픽셀 셰이더만 실행 가능</text>
  <text x="40" y="118" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">비율 고정 (8:24). 유휴 유닛이 다른 쪽을 도울 수 없음.</text>
  <line x1="40" y1="142" x2="580" y2="142" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="170" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">통합형 (GeForce 8800 이후)</text>
  <text x="40" y="194" font-family="sans-serif" font-size="10" fill="currentColor">범용 셰이더 코어 ×128</text>
  <text x="200" y="194" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">— 버텍스, 픽셀, 지오메트리 셰이더 모두 실행 가능</text>
  <text x="40" y="218" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">부하에 따라 동적으로 역할 할당.</text>
  <line x1="40" y1="244" x2="580" y2="244" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="310" y="278" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">전용 유닛의 구분이 사라지고, 모든 코어를 필요한 셰이더에 할당 가능</text>
</svg>
</div>

<br>

통합 셰이더 아키텍처의 핵심 이점은 **동적 부하 분배(Dynamic Load Balancing)**입니다.

장면에 정점이 많아서 버텍스 셰이더의 부하가 높으면, GPU는 더 많은 셰이더 코어를 버텍스 셰이더 실행에 할당합니다.

반대로 화면을 가득 채우는 큰 삼각형이 많아서 픽셀 셰이더의 부하가 높으면, 더 많은 코어를 픽셀 셰이더에 할당합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">동적 부하 분배 (128개 범용 코어)</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">장면 A: 정점이 적고, 화면을 채우는 큰 삼각형</text>
  <text x="40" y="74" font-family="sans-serif" font-size="10" fill="currentColor">VS (20개)</text>
  <rect x="130" y="64" width="62" height="20" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.8"/>
  <text x="40" y="100" font-family="sans-serif" font-size="10" fill="currentColor">PS (108개)</text>
  <rect x="130" y="90" width="338" height="20" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="0.8"/>
  <text x="60" y="132" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">→ 픽셀 처리에 자원 집중. 유휴 코어 없음.</text>
  <line x1="40" y1="158" x2="580" y2="158" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="186" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">장면 B: 정점이 매우 많고, 화면에 작게 그려지는 오브젝트 다수</text>
  <text x="40" y="212" font-family="sans-serif" font-size="10" fill="currentColor">VS (80개)</text>
  <rect x="130" y="202" width="250" height="20" fill="currentColor" fill-opacity="0.32" stroke="currentColor" stroke-width="0.8"/>
  <text x="40" y="238" font-family="sans-serif" font-size="10" fill="currentColor">PS (48개)</text>
  <rect x="130" y="228" width="150" height="20" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="0.8"/>
  <text x="60" y="270" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85" font-style="italic">→ 정점 처리에 자원 집중. 유휴 코어 없음.</text>
  <line x1="40" y1="296" x2="580" y2="296" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="310" y="330" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">분리형과 달리, 장면 특성에 따라 코어 할당 비율이 동적으로 변함</text>
</svg>
</div>

<br>

분리형에서는 어떤 장면이든 한쪽 유닛이 유휴 상태였지만, 통합형에서는 모든 코어가 부하에 따라 재할당되므로 같은 트랜지스터 수로 더 높은 성능을 낼 수 있습니다.

<br>

GeForce 8800과 함께 **Shader Model 4.0**이 도입되었습니다.

SM 4.0에서 추가된 주요 기능은 **지오메트리 셰이더(Geometry Shader)**입니다. 

버텍스 셰이더가 정점 하나를 처리하고, 픽셀 셰이더가 프래그먼트 하나를 처리하는 것과 달리, 지오메트리 셰이더는 **프리미티브(삼각형, 선, 점) 단위**로 동작합니다. 입력으로 하나의 프리미티브를 받아서, 새로운 프리미티브를 생성하거나 기존 프리미티브를 변형할 수 있습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">지오메트리 셰이더의 위치 (SM 4.0에서 추가)</text>
  <rect x="20" y="46" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="65" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 입력</text>
  <line x1="110" y1="64" x2="124" y2="64" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="128,64 120,60 120,68" fill="currentColor"/>
  <rect x="128" y="46" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="178" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">버텍스 셰이더</text>
  <line x1="228" y1="64" x2="242" y2="64" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="246,64 238,60 238,68" fill="currentColor"/>
  <rect x="246" y="46" width="118" height="36" rx="4" fill="currentColor" fill-opacity="0.20" stroke="currentColor" stroke-width="1.4"/>
  <text x="305" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">지오메트리 셰이더</text>
  <line x1="364" y1="64" x2="378" y2="64" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="382,64 374,60 374,68" fill="currentColor"/>
  <rect x="382" y="46" width="90" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="427" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">래스터화</text>
  <line x1="472" y1="64" x2="486" y2="64" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="490,64 482,60 482,68" fill="currentColor"/>
  <rect x="490" y="46" width="100" height="36" rx="4" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="540" y="68" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">픽셀 셰이더</text>
  <text x="60" y="120" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">단위</text>
  <text x="160" y="120" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">프리미티브 (삼각형, 선, 점)</text>
  <text x="60" y="142" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">입력</text>
  <text x="160" y="142" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">프리미티브 1개</text>
  <text x="60" y="164" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">출력</text>
  <text x="160" y="164" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">0개 이상의 프리미티브</text>
  <text x="60" y="200" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">활용 예</text>
  <text x="160" y="200" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">풀 렌더링, 와이어프레임, 파티클 빌보드</text>
</svg>
</div>

<br>

지오메트리 셰이더는 통합 셰이더 아키텍처의 범용 코어에서 실행됩니다.

별도의 전용 하드웨어가 필요하지 않고, 같은 셰이더 코어가 버텍스, 지오메트리, 픽셀 셰이더를 모두 처리합니다. 통합 아키텍처가 아니었다면, 지오메트리 셰이더를 위한 전용 유닛을 추가로 설계해야 했을 것입니다.

<br>

이후 SM 5.0에서는 **테셀레이션 셰이더(Tessellation Shader)**와 **컴퓨트 셰이더(Compute Shader)**가 추가되었습니다.

테셀레이션 셰이더는 저폴리곤 메쉬를 GPU에서 실시간으로 세분화하여 고폴리곤으로 만드는 기능이고, 컴퓨트 셰이더는 렌더링 파이프라인과 무관한 범용 연산을 GPU에서 실행하는 기능입니다.

지오메트리 셰이더와 마찬가지로, 두 기능 모두 전용 하드웨어 없이 범용 셰이더 코어에서 실행됩니다.

<br>

---

## GPGPU와 범용 연산

통합 셰이더 아키텍처의 범용 셰이더 코어는 정점과 픽셀을 구분하지 않고 같은 명령어 집합을 실행합니다.

원래 그래픽 처리를 위해 설계된 코어이지만, 구조적으로는 "같은 연산을 대량의 데이터에 병렬 적용"하는 모든 작업을 수행할 수 있습니다.

GPU의 대량 병렬 코어를 그래픽 렌더링이 아닌 **범용 연산(General-Purpose computation)**에 사용하려는 시도가 여기서 시작되었고, 이 접근을 **GPGPU(General-Purpose computing on Graphics Processing Units)**라고 합니다.

### CUDA와 OpenCL

GPGPU 초기에는 범용 연산을 위한 전용 인터페이스가 없었습니다. 그래픽 API(OpenGL, DirectX)를 우회적으로 사용해야 했고, 연산 데이터를 텍스처로 인코딩한 뒤 셰이더 프로그램으로 연산을 수행하고, 결과를 렌더 타겟(GPU가 셰이더 출력을 기록하는 메모리 영역)에서 읽어오는 방식이었습니다.

범용 연산을 하려면 그래픽 렌더링 경로를 반드시 거쳐야 하므로, 프로그래밍이 번거롭고 GPU 자원의 활용 효율도 낮았습니다.

<br>

2007년, NVIDIA는 **CUDA(Compute Unified Device Architecture)**를 발표했습니다.

CUDA는 C/C++를 확장한 언어와 컴파일러, GPU 메모리 관리 API, 스레드 계층 구조(그리드 → 블록 → 스레드)로 구성된 GPU 범용 연산 프레임워크로, NVIDIA GPU에서만 동작합니다.

<br>

2008년 말에는 **OpenCL(Open Computing Language)**이 Khronos Group에 의해 표준화되었습니다. OpenCL은 CUDA와 유사한 기능을 제공하지만, NVIDIA뿐 아니라 AMD, Intel, ARM, Apple 등 다양한 하드웨어에서 동작하는 크로스 플랫폼 프레임워크입니다.

<br>

**GPGPU 프레임워크 비교**

| 구분 | CUDA (2007) | OpenCL (2008) |
|:---|:---|:---|
| 제작사 | NVIDIA | Khronos Group |
| 지원 GPU | NVIDIA 전용 | 크로스 플랫폼 |
| 생태계 | cuDNN, cuBLAS 등 | CUDA 대비 적음 |
| 주 용도 | 머신러닝, 과학 시뮬레이션 | 이기종 컴퓨팅 |

### GPGPU의 활용 분야

GPU의 병렬 코어는 "같은 연산을 방대한 데이터에 반복 적용"하는 작업에 적합합니다. 이 특성 덕분에 그래픽 외 여러 분야에서 GPU가 활용되고 있습니다.

<br>

가장 대표적인 분야는 딥러닝입니다.

신경망의 학습과 추론은 대규모 행렬 곱셈의 반복으로 이루어지는데, 행렬 곱셈은 각 원소에 대해 독립적인 곱셈과 덧셈을 수행하므로 수천 개 코어의 동시 처리에 적합합니다.

NVIDIA의 CUDA와 cuDNN 라이브러리가 딥러닝 프레임워크(TensorFlow, PyTorch 등)의 핵심 연산을 가속하며, 2026년 현재 GPU 수요를 끌어올리는 가장 큰 요인 중 하나입니다.

<br>

과학 시뮬레이션에서도 같은 원리가 적용됩니다.

유체 역학, 분자 동역학, 기상 시뮬레이션 등은 공간을 격자로 나누고 각 격자점에서 독립적인 물리 방정식을 풀어야 합니다. 격자점이 수백만~수억 개에 달하므로, GPU의 병렬 처리가 시뮬레이션 속도를 수십~수백 배 향상시킵니다.

<br>

영상 처리도 GPU 가속의 대상입니다.

이미지의 각 픽셀에 필터를 적용하는 작업(블러, 엣지 검출, 색 보정 등)은 픽셀마다 독립적인 연산이므로 GPU에서 병렬 처리할 수 있습니다. 영상 인코딩/디코딩에서도 프레임 내 블록 단위 처리를 GPU가 가속합니다.

### Unity의 Compute Shader

Unity에서 GPGPU를 활용하는 수단이 **Compute Shader**입니다.

Compute Shader는 렌더링 파이프라인과 독립적으로 GPU에서 실행되는 프로그램이며, SM 5.0(DirectX 11)에서 도입되었습니다.

<br>

**렌더링 셰이더 vs Compute Shader**

| 구분 | 렌더링 셰이더 | Compute Shader |
|:---|:---|:---|
| 입력 | 정점/프래그먼트 (파이프라인 제공) | 개발자 정의 버퍼 |
| 출력 | 변환된 정점 또는 픽셀 색상 | 개발자 정의 버퍼 |
| 실행 시점 | 드로우 콜 시 자동 호출 | `Dispatch()` 명시적 호출 |
| 용도 | 오브젝트 렌더링 | 범용 병렬 연산 |

**Compute Shader 활용 예**: 파티클 시뮬레이션, GPU 스키닝, 절차적 메쉬 생성, 이미지 후처리, 군중 경로 계산

<br>

Compute Shader는 정점→래스터화→프래그먼트의 렌더링 파이프라인을 거치지 않습니다.

개발자가 처리할 데이터를 버퍼(ComputeBuffer, StructuredBuffer 등)에 담고, **스레드 그룹(Thread Group)** 단위로 실행을 구성합니다.

그룹당 스레드 수와 디스패치할 그룹 수를 지정한 뒤 `Dispatch()`를 호출하면, GPU의 범용 셰이더 코어가 해당 스레드들을 병렬로 실행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Compute Shader의 스레드 구조</text>
  <text x="310" y="40" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">예: 27개의 파티클 위치를 병렬 업데이트</text>
  <text x="40" y="68" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">그룹당 스레드 수</tspan> — 9</text>
  <text x="40" y="86" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">디스패치할 그룹 수</tspan> — 3</text>
  <rect x="30" y="106" width="180" height="100" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="120" y="124" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">그룹 0</text>
  <text x="120" y="144" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">스레드 0 ~ 8</text>
  <text x="120" y="184" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">[t0][t1][t2][t3][t4][t5][t6][t7][t8]</text>
  <rect x="220" y="106" width="180" height="100" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="310" y="124" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">그룹 1</text>
  <text x="310" y="144" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">스레드 9 ~ 17</text>
  <text x="310" y="184" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">[t9][t10][t11][t12][t13][t14][t15][t16][t17]</text>
  <rect x="410" y="106" width="180" height="100" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="500" y="124" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">그룹 2</text>
  <text x="500" y="144" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">스레드 18 ~ 26</text>
  <text x="500" y="184" text-anchor="middle" font-family="monospace" font-size="9" fill="currentColor" opacity="0.7">[t18][t19][t20][t21][t22][t23][t24][t25][t26]</text>
  <text x="40" y="240" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 총 스레드 = 9 × 3 = 27</text>
  <text x="40" y="258" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· 스레드 k는 파티클[k]를 처리</text>
  <text x="40" y="276" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">· SV_DispatchThreadID가 각 스레드에 고유 인덱스(k)를 부여</text>
</svg>
</div>

<br>

Compute Shader는 통합 셰이더 아키텍처 위에서 동작합니다.

Compute 작업을 실행하는 코어와 렌더링 셰이더를 실행하는 코어는 물리적으로 같은 범용 셰이더 코어이며, GPU는 두 종류의 작업을 동적으로 분배합니다.

통합 셰이더 아키텍처가 없었다면, 즉 정점 전용·픽셀 전용으로 유닛이 분리되어 있었다면, 범용 연산을 위한 코어를 따로 할당할 수 없으므로 Compute Shader라는 개념 자체가 성립하기 어려웠을 것입니다.

<br>

다만 모바일 GPU에서는 Compute Shader 사용 시 트레이드오프가 존재합니다.

모바일 GPU의 셰이더 코어 수는 데스크톱 GPU 대비 적으므로, Compute Shader에 코어가 할당되면 그만큼 렌더링에 사용 가능한 코어가 줄어듭니다.

또한 Compute Shader의 결과를 렌더링에서 사용하려면 GPU 내부에서 동기화가 필요하고, 모바일 GPU 특유의 TBDR(Tile-Based Deferred Rendering) 아키텍처에서는 타일 메모리와의 상호작용도 고려해야 합니다.

TBDR과 모바일 GPU의 구조적 특성은 [하드웨어 기초 (4)](/dev/unity/HardwareBasics-4/)에서 다룹니다.

<br>

---

## GPU 발전 과정 요약

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 680 760" xmlns="http://www.w3.org/2000/svg" style="max-width: 680px; width: 100%;">
  <text x="340" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU 발전의 흐름</text>
  <rect x="80" y="40" width="120" height="50" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="140" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">~1995</text>
  <text x="140" y="80" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">소프트웨어 렌더링</text>
  <text x="220" y="58" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">CPU가 모든 그래픽 연산을 수행</text>
  <text x="220" y="76" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">→ 해상도/폴리곤 증가에 한계</text>
  <line x1="140" y1="90" x2="140" y2="112" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,116 136,108 144,108" fill="currentColor"/>
  <rect x="80" y="116" width="120" height="64" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="140" y="138" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1996</text>
  <text x="140" y="156" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">고정 기능 GPU</text>
  <text x="140" y="170" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">3dfx Voodoo 등</text>
  <text x="220" y="138" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">래스터화, 텍스처 매핑을 하드웨어가 처리</text>
  <text x="220" y="156" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">정점 변환은 여전히 CPU 담당</text>
  <line x1="140" y1="180" x2="140" y2="202" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,206 136,198 144,198" fill="currentColor"/>
  <rect x="80" y="206" width="120" height="64" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="140" y="228" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">1999</text>
  <text x="140" y="246" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">하드웨어 T&amp;L</text>
  <text x="140" y="260" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">GeForce 256</text>
  <text x="220" y="222" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">정점 변환과 조명 계산도 GPU가 처리</text>
  <text x="220" y="240" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">NVIDIA가 "GPU"라는 용어를 사용</text>
  <text x="220" y="258" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">한계: 고정된 알고리즘만 사용 가능</text>
  <line x1="140" y1="270" x2="140" y2="292" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,296 136,288 144,288" fill="currentColor"/>
  <rect x="80" y="296" width="120" height="78" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.2"/>
  <text x="140" y="318" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2001</text>
  <text x="140" y="336" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">프로그래머블 셰이더</text>
  <text x="140" y="350" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">GeForce 3, SM 1.0</text>
  <text x="220" y="312" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">개발자가 정점/픽셀 처리 코드를 직접 작성</text>
  <text x="220" y="330" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">SM 1.0 → 2.0 → 3.0으로 표현력 확대</text>
  <text x="220" y="348" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">한계: 정점 유닛과 픽셀 유닛이 물리적으로 분리</text>
  <text x="240" y="364" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">→ 부하 불균형으로 유휴 유닛 발생</text>
  <line x1="140" y1="374" x2="140" y2="396" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,400 136,392 144,392" fill="currentColor"/>
  <rect x="80" y="400" width="120" height="78" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="140" y="422" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2006</text>
  <text x="140" y="440" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">통합 셰이더</text>
  <text x="140" y="454" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">아키텍처</text>
  <text x="140" y="468" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">GeForce 8800, SM 4.0</text>
  <text x="220" y="416" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">범용 셰이더 코어가 모든 셰이더를 실행</text>
  <text x="220" y="434" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">부하에 따라 동적 할당 → 유휴 유닛 감소</text>
  <text x="220" y="452" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">지오메트리 셰이더 추가</text>
  <line x1="140" y1="478" x2="140" y2="500" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,504 136,496 144,496" fill="currentColor"/>
  <rect x="80" y="504" width="120" height="78" rx="5" fill="currentColor" fill-opacity="0.14" stroke="currentColor" stroke-width="1.2"/>
  <text x="140" y="526" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">2007+</text>
  <text x="140" y="544" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">GPGPU</text>
  <text x="140" y="558" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.7">CUDA, OpenCL</text>
  <text x="220" y="520" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">GPU의 병렬 코어를 그래픽 외 연산에 활용</text>
  <text x="220" y="538" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">머신러닝, 과학 시뮬레이션, 영상 처리</text>
  <text x="220" y="556" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">Unity의 Compute Shader (SM 5.0)</text>
  <line x1="140" y1="582" x2="140" y2="604" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="140,608 136,600 144,600" fill="currentColor"/>
  <rect x="80" y="608" width="120" height="64" rx="5" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1.4"/>
  <text x="140" y="632" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">현재</text>
  <text x="140" y="652" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">통합 셰이더</text>
  <text x="140" y="666" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">+ GPGPU 기반</text>
  <text x="220" y="630" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">통합 셰이더 + GPGPU 아키텍처를 기반으로</text>
  <text x="220" y="648" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">레이 트레이싱 코어, AI 가속 유닛 등</text>
  <text x="220" y="666" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">전용 하드웨어 추가</text>
  <text x="340" y="730" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7" font-style="italic">각 단계의 한계가 다음 아키텍처 전환의 동기가 됨</text>
</svg>
</div>

<br>

각 전환의 동기는 이전 단계의 구체적인 한계였습니다.

CPU만으로는 해상도와 폴리곤을 동시에 높일 수 없어 전용 하드웨어가 등장했고, 고정된 알고리즘으로는 다양한 시각 효과를 표현할 수 없어 프로그래머블 셰이더가 도입되었으며, 분리된 유닛의 부하 불균형이 통합 아키텍처를 이끌었고, 통합된 범용 코어의 병렬 처리 능력이 GPGPU로 확장되었습니다.

현재의 GPU도 이 통합 셰이더 + GPGPU 아키텍처를 기반으로, 레이 트레이싱 전용 코어나 AI 가속 유닛 같은 특수 목적 하드웨어를 추가하는 방향으로 진화하고 있습니다.

<br>

---

## 마무리

- CPU가 모든 그래픽을 처리하던 소프트웨어 렌더링은 해상도와 폴리곤 수를 동시에 높일 수 없었습니다.
- 고정 기능 GPU(Voodoo, GeForce 256)는 래스터화와 T&L을 하드웨어로 처리했지만, 알고리즘을 변경할 수 없었습니다.
- 프로그래머블 셰이더(SM 1.0~3.0)는 정점/픽셀 처리를 개발자가 직접 코드로 작성할 수 있게 했습니다.
- 통합 셰이더 아키텍처는 범용 코어로 부하 불균형을 해소하고, 지오메트리/컴퓨트 셰이더의 기반을 마련했습니다.
- GPGPU(CUDA, OpenCL, Compute Shader)는 GPU의 병렬 코어를 그래픽 외 범용 연산에 활용합니다.

<br>

다만 데스크톱 GPU와 모바일 GPU는 설계 제약이 다릅니다.

모바일 환경에서는 CPU와 GPU가 하나의 칩(SoC)에 통합되어 있고, 전력과 발열이라는 물리적 제약이 아키텍처 전반을 좌우합니다.

[하드웨어 기초 (4)](/dev/unity/HardwareBasics-4/)에서는 모바일 SoC의 통합 구조, 전력 제약, 메모리 공유, 쓰로틀링이 게임 성능에 미치는 영향을 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)

**시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- **하드웨어 기초 (3) - GPU의 탄생과 발전** (현재 글)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- **하드웨어 기초 (3) - GPU의 탄생과 발전** (현재 글)
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
- [Unity 렌더링 (3) - Render Pipeline 개요](/dev/unity/UnityRendering-3/)
