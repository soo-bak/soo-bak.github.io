---
layout: single
title: "렌더링 기초 (1) - 메쉬의 구조 - soo:bak"
date: "2026-02-11 10:10:00 +0900"
description: 렌더링의 개념, 정점과 삼각형, 인덱스 버퍼, 정점 속성, 메쉬 메모리 구조, LOD를 설명합니다.
tags:
  - Unity
  - 최적화
  - 렌더링
  - 메쉬
  - 모바일
---

## 렌더링이란

[프레임의 구조](/dev/unity/GameLoop-1/)에서 CPU와 GPU가 한 프레임을 함께 완성한다는 점을, [CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)에서 프레임 예산의 대부분이 렌더링에 쓰인다는 점을 확인했습니다.

<br>

렌더링은 **데이터를 화면의 픽셀로 변환하는 과정**입니다. 2D 스프라이트든 3D 모델이든, 화면에 보이는 모든 것은 이 변환을 거친 결과입니다.

<br>

이 변환에서 실제 픽셀을 만들어내는 것은 GPU입니다.

GPU가 픽셀을 만들려면 원본 데이터가 필요합니다.
화면에 보이는 캐릭터, 지형, 건물은 모두 3D 공간에 수치로 정의된 형태 데이터로부터 만들어지고, 이 형태 데이터를 담는 구조가 **메쉬(Mesh)**입니다. 메쉬는 오브젝트의 형태를 점(정점)과 면(삼각형)의 집합으로 표현합니다.

<br>

이 글에서는 메쉬가 어떤 요소로 구성되어 있고, 각 요소가 렌더링에서 어떤 역할을 하며, 메모리를 얼마나 사용하는지 살펴봅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 170" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <!-- 왼쪽 박스: 3D 공간의 데이터 -->
  <rect x="1" y="1" width="200" height="168" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">3D 공간의 데이터</text>
  <text x="101" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">정점, 삼각형</text>
  <text x="101" y="80" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← 메쉬 (이 글)</text>
  <line x1="30" y1="98" x2="172" y2="98" stroke="currentColor" stroke-width="1" opacity="0.2"/>
  <text x="101" y="122" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">텍스처, 머티리얼</text>
  <text x="101" y="140" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">← 이후 글</text>
  <!-- 중앙 화살표: 렌더링 -->
  <line x1="215" y1="85" x2="355" y2="85" stroke="currentColor" stroke-width="2.5"/>
  <polygon points="355,79 367,85 355,91" fill="currentColor"/>
  <text x="290" y="72" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">렌더링</text>
  <!-- 오른쪽 박스: 2D 화면 이미지 -->
  <rect x="379" y="1" width="200" height="168" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="479" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">2D 화면 이미지</text>
  <text x="479" y="82" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">픽셀로 된</text>
  <text x="479" y="100" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">최종 이미지</text>
</svg>
</div>

<br>

왼쪽이 렌더링의 입력, 오른쪽이 출력입니다.

---

## 정점(Vertex)과 삼각형

메쉬는 **정점(Vertex)**으로 구성됩니다. 정점은 공간에서의 한 점으로, 좌표(x, y, z)를 가집니다. 정점을 찍는 것만으로는 점의 집합일 뿐이고, 채워진 표면을 만들려면 정점들을 이어서 면을 구성해야 합니다.
이때 GPU가 처리하는 면의 단위가 **삼각형(Triangle)**입니다. 정점 3개가 하나의 삼각형을 이룹니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 240 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 240px; width: 100%;">
  <!-- 삼각형 면 -->
  <polygon points="120,25 30,175 210,175" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 정점 원 -->
  <circle cx="120" cy="25" r="4" fill="currentColor"/>
  <circle cx="30" cy="175" r="4" fill="currentColor"/>
  <circle cx="210" cy="175" r="4" fill="currentColor"/>
  <!-- 정점 레이블 -->
  <text x="120" y="16" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v0</text>
  <text x="16" y="193" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v1</text>
  <text x="224" y="193" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v2</text>
</svg>
</div>

<br>

삼각형이 면의 기본 단위로 쓰이는 이유는 세 가지입니다.

첫째, 삼각형은 **항상 평면**입니다.
3D 공간에서 점 3개는 반드시 하나의 평면 위에 놓입니다. 점이 4개 이상이면 같은 평면에 있지 않을 수 있어서, 면이 뒤틀리고 렌더링 결과가 예측 불가능해집니다. 삼각형은 이런 문제가 원천적으로 발생하지 않습니다.

<br>

둘째, 삼각형은 **항상 볼록(Convex)**합니다.
다각형이 **오목(Concave)**하다는 것은 내각이 180°를 넘는 꼭짓점이 있어서 윤곽선이 안쪽으로 꺾이는 형태를 말합니다.
삼각형의 세 내각의 합은 180°이고, 각 내각은 0°보다 커야 하므로 어떤 내각도 180°에 도달할 수 없습니다. 따라서 삼각형은 오목해질 수 없습니다.

<br>

셋째, 이 두 성질 덕분에 **래스터화(Rasterization)**가 단순해집니다.
래스터화는 기하 도형이 화면에서 어떤 픽셀을 덮는지 결정하는 과정이며, GPU의 **래스터라이저(Rasterizer)**가 이 작업을 수행합니다.
삼각형은 평면이고 볼록하므로, 세 변 각각에 대해 "이 픽셀이 변의 안쪽에 있는가?"만 확인하면 됩니다.
판정 3번으로 내부 여부가 결정되고, GPU는 이 판정을 모든 픽셀에 대해 병렬로 수행합니다.
오목한 다각형은 이런 단순한 판정이 통하지 않아 더 복잡한 알고리즘이 필요하고, 다각형을 렌더링하려면 먼저 삼각형으로 분할하는 단계도 추가됩니다. GPU의 래스터라이저가 삼각형 단위로 설계된 이유입니다.

<br>

이 세 가지 성질 덕분에 GPU는 어떤 형태의 메쉬든 삼각형의 집합으로 처리할 수 있습니다.

---

### 사각형과 삼각형의 관계

화면에 사각형 하나를 그린다고 가정합니다. 사각형은 삼각형이 아니므로, 정점 4개와 삼각형 2개로 분할해야 합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 260 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 260px; width: 100%;">
  <!-- 삼각형 1: v0, v2, v1 -->
  <polygon points="30,30 30,180 230,30" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.5"/>
  <!-- 삼각형 2: v1, v2, v3 -->
  <polygon points="230,30 30,180 230,180" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5"/>
  <!-- 대각선 (공유 변) -->
  <line x1="30" y1="180" x2="230" y2="30" stroke="currentColor" stroke-width="1.5"/>
  <!-- 정점 원 -->
  <circle cx="30" cy="30" r="4" fill="currentColor"/>
  <circle cx="230" cy="30" r="4" fill="currentColor"/>
  <circle cx="30" cy="180" r="4" fill="currentColor"/>
  <circle cx="230" cy="180" r="4" fill="currentColor"/>
  <!-- 정점 레이블 -->
  <text x="18" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v0</text>
  <text x="244" y="20" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v1</text>
  <text x="18" y="200" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v2</text>
  <text x="244" y="200" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">v3</text>
  <!-- 삼각형 번호 보조 텍스트 -->
  <text x="82" y="90" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">삼각형 1</text>
  <text x="178" y="145" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">삼각형 2</text>
</svg>
</div>

<br>

정점 4개의 좌표는 다음과 같습니다.

```
v0 = (0, 1, 0)
v1 = (1, 1, 0)
v2 = (0, 0, 0)
v3 = (1, 0, 0)
```

<br>

이 4개의 정점으로 삼각형 2개를 구성합니다.

```
삼각형 1: v0, v2, v1
삼각형 2: v1, v2, v3
```

<br>

사각형처럼 단순한 형태도 삼각형 2개로 분해됩니다.
캐릭터나 건물 같은 복잡한 모델은 수천에서 수만 개의 삼각형으로 구성됩니다. 삼각형 수가 많을수록 표면이 매끄럽게 표현되지만, 그만큼 GPU가 처리해야 할 연산량도 증가합니다.

---

## 인덱스 버퍼

삼각형으로 면을 구성하는 방식은 간단하지만, 정점 데이터를 그대로 나열하면 메모리 낭비가 발생합니다.

앞의 사각형 예시에서 삼각형 2개의 정점을 그대로 나열하면 다음과 같습니다.

```
삼각형 1: v0, v2, v1
삼각형 2: v1, v2, v3
```

v1과 v2가 두 삼각형에 모두 등장합니다. 대각선을 공유하는 두 삼각형이 같은 정점을 사용하기 때문입니다.
각 삼각형마다 정점 데이터를 독립적으로 저장하면 총 6개가 필요하지만, 실제 고유한 정점은 4개뿐이므로 2개가 중복됩니다.

사각형 하나에서 2개 중복은 큰 문제가 아닙니다.
하지만 실제 모델에서는 하나의 정점이 평균 4~6개의 삼각형에 공유됩니다. 하나의 정점이 4개 삼각형에 공유된다면, 그 정점의 데이터가 4번 중복 저장됩니다.
정점 10,000개짜리 모델에서 이런 중복 저장을 하면 40,000~60,000개의 정점 데이터가 필요해집니다.

<br>

이 문제를 해결하는 구조가 **정점 버퍼(Vertex Buffer)**와 **인덱스 버퍼(Index Buffer)**의 분리입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 640 500" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%;">
  <!-- 상단 섹션: 인덱스 버퍼 없이 -->
  <rect x="1" y="1" width="638" height="168" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="26" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">인덱스 버퍼 없이 (정점 데이터를 그대로 나열)</text>
  <!-- 삼각형 1 행 -->
  <text x="30" y="60" font-family="sans-serif" font-size="11" fill="currentColor">삼각형 1 :</text>
  <rect x="110" y="44" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="155" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(0, 1, 0)</text>
  <rect x="215" y="44" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(0, 0, 0)</text>
  <rect x="320" y="44" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="62" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1, 1, 0)</text>
  <!-- 삼각형 2 행 -->
  <text x="30" y="100" font-family="sans-serif" font-size="11" fill="currentColor">삼각형 2 :</text>
  <rect x="110" y="84" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="155" y="102" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1, 1, 0)</text>
  <rect x="215" y="84" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="260" y="102" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(0, 0, 0)</text>
  <rect x="320" y="84" width="90" height="26" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="365" y="102" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">(1, 0, 0)</text>
  <!-- 중복 강조 점선: (1,1,0) 쌍 -->
  <rect x="320" y="44" width="90" height="26" rx="4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2" opacity="0.6"/>
  <rect x="110" y="84" width="90" height="26" rx="4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2" opacity="0.6"/>
  <!-- 중복 강조 점선: (0,0,0) 쌍 -->
  <rect x="215" y="44" width="90" height="26" rx="4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2" opacity="0.6"/>
  <rect x="215" y="84" width="90" height="26" rx="4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-dasharray="4,2" opacity="0.6"/>
  <text x="440" y="76" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">← 점선 = 중복</text>
  <!-- 상단 결론 -->
  <rect x="150" y="126" width="340" height="28" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="145" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 6개 저장 (2개 중복)</text>
  <!-- 비교 구분 -->
  <text x="320" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor" opacity="0.5">▼ 비교 ▼</text>
  <!-- 하단 섹션: 인덱스 버퍼 사용 -->
  <rect x="1" y="198" width="638" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="222" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">인덱스 버퍼 사용</text>
  <!-- 정점 버퍼 박스 -->
  <rect x="30" y="238" width="240" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="150" y="258" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 버퍼 (고유한 정점만 저장)</text>
  <text x="55" y="282" font-family="sans-serif" font-size="11" fill="currentColor">[0]  (0, 1, 0)</text>
  <text x="55" y="302" font-family="sans-serif" font-size="11" fill="currentColor">[1]  (1, 1, 0)</text>
  <text x="55" y="322" font-family="sans-serif" font-size="11" fill="currentColor">[2]  (0, 0, 0)</text>
  <text x="55" y="342" font-family="sans-serif" font-size="11" fill="currentColor">[3]  (1, 0, 0)</text>
  <!-- 참조 화살표 -->
  <line x1="370" y1="303" x2="280" y2="303" stroke="currentColor" stroke-width="1.5" stroke-dasharray="5,3"/>
  <polygon points="280,299 272,303 280,307" fill="currentColor"/>
  <text x="325" y="295" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">번호로</text>
  <text x="325" y="315" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor" opacity="0.55">참조</text>
  <!-- 인덱스 버퍼 박스 -->
  <rect x="370" y="238" width="240" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="490" y="258" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">인덱스 버퍼 (정점 번호만 저장)</text>
  <!-- 삼각형 1 인덱스 그룹 -->
  <rect x="385" y="272" width="96" height="48" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="433" y="296" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">0, 2, 1</text>
  <text x="433" y="314" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">삼각형 1</text>
  <!-- 삼각형 2 인덱스 그룹 -->
  <rect x="499" y="272" width="96" height="48" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="547" y="296" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">1, 2, 3</text>
  <text x="547" y="314" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">삼각형 2</text>
  <!-- 하단 결론 -->
  <rect x="150" y="390" width="340" height="28" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.5"/>
  <text x="320" y="409" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">정점 4개 + 인덱스 6개</text>
  <!-- 최하단 비교 결론 -->
  <line x1="160" y1="154" x2="160" y2="470" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.3"/>
  <line x1="480" y1="418" x2="480" y2="470" stroke="currentColor" stroke-width="1" stroke-dasharray="3,3" opacity="0.3"/>
  <line x1="160" y1="470" x2="480" y2="470" stroke="currentColor" stroke-width="1" opacity="0.3"/>
  <text x="320" y="490" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 중복 제거로 메모리 절약</text>
</svg>
</div>

<br>

정점 버퍼에는 고유한 정점 데이터만 저장하고, 인덱스 버퍼에는 삼각형을 구성하는 정점의 **번호(인덱스)**만 저장합니다.
GPU는 인덱스 버퍼의 번호를 읽어서 정점 버퍼의 해당 위치를 참조합니다.
삼각형 1의 인덱스 `0, 2, 1`은 "정점 버퍼의 0번, 2번, 1번 데이터를 사용하라"는 뜻입니다.

<br>

인덱스 버퍼를 사용하면 두 가지 효율이 높아집니다.

**메모리 절약.**
정점 하나의 데이터는 위치, 법선, UV 좌표 등을 포함하여 수십 바이트에 달하지만, 인덱스 하나는 16비트(2바이트) 또는 32비트(4바이트) 정수입니다.
앞서 나온 정점 10,000개짜리 모델을 예로 들면, 정점 하나가 40바이트일 때 중복 저장 시 60,000개 × 40바이트 = 약 2.3MB가 필요합니다. 인덱스 버퍼를 사용하면 정점 10,000개 × 40바이트 + 인덱스 60,000개 × 2바이트 = 약 0.5MB로 줄어듭니다.

<br>

**캐시 효율.**
GPU는 정점 셰이더를 실행한 뒤, 그 결과를 **포스트 트랜스폼 캐시(Post-Transform Cache)**에 보관합니다.
이후 다른 삼각형이 같은 인덱스를 참조하면, 정점 셰이더를 다시 실행하지 않고 캐시에서 결과를 가져옵니다.
인덱스 버퍼가 없으면 같은 좌표라도 버퍼의 다른 위치에 저장되므로, GPU는 같은 정점인지 알 수 없어 매번 정점 셰이더를 다시 실행합니다.

<br>

Unity에서도 이 구조를 그대로 사용합니다. `Mesh.vertices`(위치), `Mesh.normals`(법선), `Mesh.uv`(UV 좌표) 등의 속성 배열을 설정하면, Unity가 이를 GPU의 정점 버퍼로 업로드합니다. `Mesh.triangles`는 인덱스 버퍼가 됩니다.

### GPU 메모리에서의 배치

정점 버퍼와 인덱스 버퍼는 GPU가 직접 접근할 수 있는 메모리 영역에 배치됩니다.

> 데스크톱 GPU는 자체 메모리(**VRAM**)를 갖고 있어 CPU 메모리와 물리적으로 분리되어 있고, 모바일 GPU는 CPU와 같은 물리 메모리(RAM)를 공유하되 드라이버가 GPU 접근에 최적화된 영역을 매핑하여 사용합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- CPU 박스 -->
  <rect x="1" y="1" width="200" height="158" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="101" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">CPU</text>
  <text x="101" y="62" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">메쉬 데이터</text>
  <text x="101" y="82" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">vertices, normals,</text>
  <text x="101" y="96" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">uvs, triangles</text>
  <!-- 업로드 화살표 -->
  <line x1="215" y1="80" x2="340" y2="80" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="340,76 348,80 340,84" fill="currentColor"/>
  <text x="278" y="68" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">업로드</text>
  <!-- GPU 박스 -->
  <rect x="358" y="1" width="200" height="158" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="458" y="22" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU</text>
  <!-- 정점 버퍼 내부 박스 -->
  <rect x="378" y="42" width="160" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="458" y="66" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">정점 버퍼</text>
  <!-- 인덱스 버퍼 내부 박스 -->
  <rect x="378" y="94" width="160" height="36" rx="4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text x="458" y="118" text-anchor="middle" font-family="sans-serif" font-size="12" fill="currentColor">인덱스 버퍼</text>
</svg>
</div>

<br>

Unity는 메쉬를 로드할 때 CPU 측에서 데이터를 구성한 뒤 GPU 메모리 영역으로 업로드합니다.

업로드가 완료된 후에도 Unity는 기본적으로 CPU 측에 같은 데이터의 복사본을 유지합니다. 런타임에서 메쉬 콜라이더의 충돌 판정을 하거나, 스크립트에서 정점 데이터를 읽거나, 메쉬를 변형하려면 CPU가 메쉬 데이터에 접근할 수 있어야 하기 때문입니다.

하지만 대부분의 메쉬는 로드 후 변형하지 않으므로, CPU 측 복사본이 불필요하게 메모리를 차지합니다.
모델 임포트 설정에서 **Read/Write Enabled**를 끄면 GPU 업로드 완료 후 CPU 측 복사본이 해제되어 메모리를 절약할 수 있습니다.
스크립트에서 동적으로 생성한 메쉬는 임포트 설정이 없으므로, `Mesh.UploadMeshData(true)`를 호출하여 같은 방식으로 CPU 측 복사본을 해제할 수 있습니다.

---

## 정점 속성(Vertex Attributes)

앞에서 정점은 위치(x, y, z) 좌표만 갖는 것처럼 설명했지만, 위치만으로는 렌더링할 수 없습니다.
빛이 표면에서 어떻게 반사되는지, 텍스처의 어느 부분을 입혀야 하는지 등의 정보가 추가로 필요하고, 이 정보들이 정점의 **속성(Attribute)**으로 위치와 함께 저장됩니다.

대표적인 정점 속성으로는 Position, Normal, UV, Tangent, Color가 있습니다.

---

### Position (위치)

앞에서 다룬 정점의 공간 좌표(x, y, z)입니다. **float**(32비트 부동소수점) 3개로 구성되며, 12바이트를 차지합니다.
다른 속성은 용도에 따라 생략할 수 있지만, 위치는 모든 정점에 반드시 포함됩니다.

---

### Normal (법선)

표면에 수직으로 바깥을 향하는 방향 벡터입니다. GPU는 이 벡터와 광원의 방향을 비교하여 표면이 얼마나 밝게 보이는지 계산합니다. x, y, z 세 개의 float 값으로 구성되며, 12바이트를 차지합니다.
길이가 1인 **단위 벡터(Unit Vector)**로 저장됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 320 160" xmlns="http://www.w3.org/2000/svg" style="max-width: 320px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="320" height="160" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 표면 선 -->
  <line x1="40" y1="120" x2="280" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <!-- 표면 라벨 -->
  <text x="284" y="124" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">표면</text>
  <!-- 법선 화살표 (수직 위쪽) -->
  <line x1="160" y1="120" x2="160" y2="35" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="160,25 155,35 165,35" fill="currentColor"/>
  <!-- 법선 라벨 -->
  <text x="160" y="16" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor" text-anchor="middle">법선 (Normal)</text>
</svg>
</div>

<br>

표면의 밝기는 빛의 방향과 법선 사이의 각도로 결정됩니다. 빛이 법선과 나란하게 들어오면 가장 밝고, 비스듬할수록 어두워지며, 표면과 평행하면 빛이 닿지 않습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 400 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 400px; width: 100%;">
  <!-- 배경 -->
  <rect x="0" y="0" width="400" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 표면 선 -->
  <line x1="40" y1="140" x2="360" y2="140" stroke="currentColor" stroke-width="1.5"/>
  <!-- 표면 라벨 -->
  <text x="364" y="144" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">표면</text>
  <!-- 법선 화살표 (수직 위쪽) -->
  <line x1="210" y1="140" x2="210" y2="30" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="210,20 205,30 215,30" fill="currentColor"/>
  <!-- 법선 라벨 -->
  <text x="210" y="13" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor" text-anchor="middle">법선</text>
  <!-- 빛 방향 화살표 (왼쪽 위에서 표면 교차점으로) -->
  <line x1="100" y1="30" x2="200" y2="130" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="205,135 195,127 203,125" fill="currentColor"/>
  <!-- 빛 방향 라벨 -->
  <text x="88" y="24" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor" text-anchor="middle">빛 방향</text>
  <!-- 각도 호 (θ) -->
  <path d="M 210,100 A 40,40 0 0,0 182,112" fill="none" stroke="currentColor" stroke-width="1.2"/>
  <!-- θ 라벨 -->
  <text x="188" y="97" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">θ</text>
</svg>
</div>

$$\text{밝기} = \cos(\theta)$$

$$\theta = 0^\circ \rightarrow \cos(0^\circ) = 1.0 \quad \text{(가장 밝음)}$$

$$\theta = 60^\circ \rightarrow \cos(60^\circ) = 0.5 \quad \text{(중간)}$$

$$\theta = 90^\circ \rightarrow \cos(90^\circ) = 0.0 \quad \text{(빛이 닿지 않음)}$$

<br>

법선이 없으면 빛의 각도에 따른 밝기 차이를 계산할 수 없어, 모든 표면이 동일한 밝기로 표시됩니다. 게임에서 캐릭터 얼굴의 음영이나 지형의 굴곡이 자연스럽게 표현되는 것은 법선을 이용한 조명 계산 덕분입니다.

<br>

삼각형은 평면이므로 표면이 향하는 방향이 어디서나 같습니다. 즉, 삼각형 전체의 법선이 하나뿐입니다.
이 법선 하나로 조명을 계산하면 삼각형 안의 모든 픽셀이 같은 밝기가 됩니다. 이것이 **플랫 셰이딩(Flat Shading)**입니다. 플랫 셰이딩에서는 인접한 삼각형의 법선 방향이 다르면 경계에서 밝기가 급격히 바뀌어, 면이 각져 보입니다.

<br>

정점마다 법선을 별도로 지정하면 이 문제를 해결할 수 있습니다.
GPU는 삼각형 내부의 각 픽셀을 렌더링할 때, 세 정점의 법선을 픽셀 위치에 따라 섞어서(**보간, Interpolation**) 그 픽셀만의 법선 방향을 만들어냅니다.

정점 A에 가까운 픽셀은 A의 법선에 가깝고, 정점 B에 가까운 픽셀은 B의 법선에 가까운 값을 갖습니다. 이렇게 하면 삼각형 내부에서 법선이 부드럽게 변하고, 인접 삼각형 경계에서도 밝기가 자연스럽게 이어집니다.
이것이 **스무스 셰이딩(Smooth Shading)**입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 580 270" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%;">
  <defs>
    <linearGradient id="smoothGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="currentColor" stop-opacity="0.45"/>
      <stop offset="35%" stop-color="currentColor" stop-opacity="0.25"/>
      <stop offset="65%" stop-color="currentColor" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="currentColor" stop-opacity="0.03"/>
    </linearGradient>
  </defs>
  <!-- 제목 -->
  <text fill="currentColor" x="260" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">플랫 셰이딩 vs 스무스 셰이딩</text>
  <!-- 표면 선 -->
  <line x1="60" y1="100" x2="460" y2="100" stroke="currentColor" stroke-width="1.5"/>
  <!-- 정점 원 -->
  <circle cx="110" cy="100" r="4" fill="currentColor"/>
  <circle cx="210" cy="100" r="4" fill="currentColor"/>
  <circle cx="310" cy="100" r="4" fill="currentColor"/>
  <circle cx="410" cy="100" r="4" fill="currentColor"/>
  <!-- 정점 레이블 -->
  <text fill="currentColor" x="110" y="126" text-anchor="middle" font-size="11" font-family="sans-serif">정점A</text>
  <text fill="currentColor" x="210" y="126" text-anchor="middle" font-size="11" font-family="sans-serif">정점B</text>
  <text fill="currentColor" x="310" y="126" text-anchor="middle" font-size="11" font-family="sans-serif">정점C</text>
  <text fill="currentColor" x="410" y="126" text-anchor="middle" font-size="11" font-family="sans-serif">정점D</text>
  <!-- 법선 화살표: A (위쪽 ↑) -->
  <line x1="110" y1="94" x2="110" y2="50" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="110,46 106,54 114,54" fill="currentColor"/>
  <!-- 법선 화살표: B (위-오른쪽 ↗) -->
  <line x1="210" y1="94" x2="228" y2="56" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="231,52 223,53 226,61" fill="currentColor"/>
  <!-- 법선 화살표: C (위-오른쪽 ↗, 더 기울어짐) -->
  <line x1="310" y1="94" x2="338" y2="62" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="341,58 333,60 335,68" fill="currentColor"/>
  <!-- 법선 화살표: D (오른쪽 →) -->
  <line x1="414" y1="95" x2="454" y2="95" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="458,95 450,91 450,99" fill="currentColor"/>
  <!-- "정점 법선" 레이블 -->
  <text fill="currentColor" x="472" y="52" text-anchor="start" font-size="10" font-family="sans-serif" opacity="0.5">← 정점 법선</text>
  <!-- 삼각형 구분선 -->
  <line x1="110" y1="100" x2="110" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.3"/>
  <line x1="210" y1="100" x2="210" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.3"/>
  <line x1="310" y1="100" x2="310" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.3"/>
  <line x1="410" y1="100" x2="410" y2="140" stroke="currentColor" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.3"/>
  <!-- 삼각형 레이블 -->
  <text fill="currentColor" x="160" y="142" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">삼각형1</text>
  <text fill="currentColor" x="260" y="142" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">삼각형2</text>
  <text fill="currentColor" x="360" y="142" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">삼각형3</text>
  <!-- 플랫 셰이딩 -->
  <text fill="currentColor" x="55" y="178" text-anchor="end" font-size="11" font-weight="bold" font-family="sans-serif">플랫</text>
  <rect x="110" y="162" width="100" height="24" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="1"/>
  <rect x="210" y="162" width="100" height="24" fill="currentColor" fill-opacity="0.18" stroke="currentColor" stroke-width="1"/>
  <rect x="310" y="162" width="100" height="24" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="160" y="178" text-anchor="middle" font-size="10" font-family="sans-serif">밝음</text>
  <text fill="currentColor" x="260" y="178" text-anchor="middle" font-size="10" font-family="sans-serif">중간</text>
  <text fill="currentColor" x="360" y="178" text-anchor="middle" font-size="10" font-family="sans-serif">어두움</text>
  <text fill="currentColor" x="432" y="178" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">← 삼각형마다 균일, 경계에서 끊김</text>
  <!-- 스무스 셰이딩 -->
  <text fill="currentColor" x="55" y="232" text-anchor="end" font-size="11" font-weight="bold" font-family="sans-serif">스무스</text>
  <rect x="110" y="216" width="300" height="24" rx="5" fill="url(#smoothGrad)" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="120" y="232" text-anchor="start" font-size="10" font-family="sans-serif">밝음</text>
  <text fill="currentColor" x="210" y="232" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">점진</text>
  <text fill="currentColor" x="310" y="232" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">점진</text>
  <text fill="currentColor" x="400" y="232" text-anchor="end" font-size="10" font-family="sans-serif">어두움</text>
  <text fill="currentColor" x="432" y="232" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">← 내부에서 부드럽게 변화</text>
</svg>
</div>

---

### UV (텍스처 좌표)

메쉬의 표면에 2D 이미지(텍스처)를 입히려면, 각 정점이 텍스처의 어느 위치에 대응하는지 알아야 합니다. 이 대응 관계를 지정하는 것이 UV 좌표입니다. u, v 두 개의 float 값으로 구성되며, 8바이트를 차지합니다.

UV 좌표계에서 (0, 0)은 텍스처 이미지의 왼쪽 아래, (1, 1)은 오른쪽 위입니다. 각 정점에 UV 좌표를 지정하면, 그 정점이 텍스처의 어느 위치에 대응하는지 결정됩니다. 앞에서 다룬 사각형 메쉬에 텍스처를 입히는 경우를 예로 들면 다음과 같습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <!-- 왼쪽 영역: 텍스처 이미지 -->
  <text fill="currentColor" x="120" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">텍스처 이미지</text>
  <!-- UV 좌표 박스 -->
  <rect x="60" y="40" width="130" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="125" y="112" text-anchor="middle" font-size="12" font-family="sans-serif">텍스처</text>
  <!-- v축 (세로) -->
  <line x1="45" y1="170" x2="45" y2="30" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="45,26 41,34 49,34" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="38" y="28" text-anchor="end" font-size="11" font-family="sans-serif" opacity="0.6">v</text>
  <!-- v축 눈금 -->
  <text fill="currentColor" x="38" y="45" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">1</text>
  <text fill="currentColor" x="38" y="174" text-anchor="end" font-size="10" font-family="sans-serif" opacity="0.5">0</text>
  <!-- u축 (가로) -->
  <line x1="45" y1="183" x2="205" y2="183" stroke="currentColor" stroke-width="1.2" opacity="0.5"/>
  <polygon points="209,183 201,179 201,187" fill="currentColor" opacity="0.5"/>
  <text fill="currentColor" x="212" y="187" text-anchor="start" font-size="11" font-family="sans-serif" opacity="0.6">u</text>
  <!-- u축 눈금 -->
  <text fill="currentColor" x="60" y="196" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">0</text>
  <text fill="currentColor" x="190" y="196" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">1</text>
  <!-- 오른쪽 영역: 메쉬의 정점에 UV 지정 -->
  <text fill="currentColor" x="410" y="18" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">메쉬의 정점에 UV 지정</text>
  <!-- 메쉬 사각형 -->
  <rect x="345" y="40" width="130" height="130" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <!-- 정점 원 -->
  <circle cx="355" cy="50" r="4" fill="currentColor"/>
  <circle cx="465" cy="50" r="4" fill="currentColor"/>
  <circle cx="355" cy="160" r="4" fill="currentColor"/>
  <circle cx="465" cy="160" r="4" fill="currentColor"/>
  <!-- 정점 레이블 -->
  <text fill="currentColor" x="355" y="42" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">v0</text>
  <text fill="currentColor" x="465" y="42" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">v1</text>
  <text fill="currentColor" x="355" y="180" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">v2</text>
  <text fill="currentColor" x="465" y="180" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif">v3</text>
  <!-- UV 좌표 보조 텍스트 -->
  <text fill="currentColor" x="355" y="30" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(u=0, v=1)</text>
  <text fill="currentColor" x="465" y="30" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(u=1, v=1)</text>
  <text fill="currentColor" x="355" y="194" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(u=0, v=0)</text>
  <text fill="currentColor" x="465" y="194" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(u=1, v=0)</text>
  <!-- 정점 연결선 (상단) -->
  <line x1="361" y1="50" x2="459" y2="50" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <!-- 정점 연결선 (하단) -->
  <line x1="361" y1="160" x2="459" y2="160" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <!-- 정점 연결선 (좌측) -->
  <line x1="355" y1="56" x2="355" y2="154" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <!-- 정점 연결선 (우측) -->
  <line x1="465" y1="56" x2="465" y2="154" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
</svg>
</div>

<br>

v0에 (0, 1)을 지정하면 텍스처의 왼쪽 위, v3에 (1, 0)을 지정하면 텍스처의 오른쪽 아래가 대응됩니다.
GPU는 법선의 보간과 같은 방식으로 삼각형 내부의 각 픽셀에 대해 UV를 보간하고, 해당 좌표에서 텍스처 이미지의 색상을 가져옵니다.
이 과정을 **텍스처 매핑(Texture Mapping)**이라 합니다.

UV 좌표가 없으면 텍스처를 표면에 어떻게 대응시킬지 알 수 없으므로, 텍스처를 사용하는 모든 메쉬에 UV가 필요합니다.

<br>

하나의 메쉬에 여러 종류의 텍스처를 입혀야 할 때가 있습니다.
예를 들어, 기본 외형을 위한 텍스처와 미리 계산된 조명 정보를 담은 **라이트맵(Lightmap)** 텍스처는 서로 다른 UV 좌표가 필요합니다.
이를 위해 UV 채널을 여러 개 사용할 수 있습니다. Unity에서는 관례적으로 UV0을 기본 텍스처, UV1을 라이트맵에 사용합니다.
UV 채널이 추가될 때마다 정점당 8바이트가 더 사용됩니다.

---

### Tangent (접선)

법선에 수직이면서 표면 위에 놓인 방향 벡터입니다. x, y, z, w 네 개의 float 값으로 구성되며, 16바이트를 차지합니다.
접선은 **노멀맵(Normal Map)**을 사용할 때 필요합니다.

앞서 살펴본 스무스 셰이딩은 삼각형 경계를 매끄럽게 이어주지만, 벽돌 벽의 홈이나 피부의 주름, 금속 표면의 스크래치 같은 미세한 요철까지 표현하지는 못합니다. 이런 디테일을 삼각형으로 직접 모델링하면 삼각형 수가 크게 늘어납니다.
노멀맵은 삼각형을 늘리지 않고 이 문제를 해결합니다.

노멀맵은 일반 텍스처와 같은 2D 이미지이지만, 각 픽셀에 색상 대신 법선 방향을 저장합니다 — R, G, B 값이 각각 법선의 x, y, z 방향에 대응합니다.

<br>

법선의 각 성분은 -1 ~ 1 범위이지만, RGB는 0 ~ 255 범위입니다. 그래서 노멀맵에 저장할 때 다음과 같이 변환합니다.

$$\text{RGB} = \frac{\text{법선} + 1}{2} \times 255$$

요철이 없는 평평한 표면의 법선은 (0, 0, 1)로 표면에서 수직으로 바깥을 가리킵니다. 이 값을 위 공식에 넣으면 다음과 같습니다.

| 성분 | 법선 값 | 변환 결과 |
|:---:|:---:|:---:|
| R (x) | 0 | 128 |
| G (y) | 0 | 128 |
| B (z) | 1 | 255 |

결과는 RGB (128, 128, 255)입니다.
대부분의 표면이 이 기본 법선에 가깝기 때문에 노멀맵은 전체적으로 푸른 보라색을 띠고, 요철이 있는 부분만 이 색에서 벗어나 다른 방향의 법선을 나타냅니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 420 290" xmlns="http://www.w3.org/2000/svg" style="max-width: 420px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="210" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">노멀맵의 구조</text>
  <text fill="currentColor" x="210" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">각 픽셀의 RGB = 법선 방향</text>

  <!-- 배경 박스 -->
  <rect x="20" y="50" width="380" height="230" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>

  <!-- R 채널 -->
  <rect x="40" y="68" width="100" height="44" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="90" y="86" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">R (빨강)</text>
  <text fill="currentColor" x="90" y="103" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">x 방향 기울기</text>

  <!-- 화살표 R → 설명 -->
  <line x1="140" y1="90" x2="168" y2="90" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="168,86 176,90 168,94" fill="currentColor"/>
  <text fill="currentColor" x="182" y="87" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.55">128 = 수정 없음</text>
  <text fill="currentColor" x="182" y="100" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.55">&lt;128 / &gt;128 → 좌 / 우 기울기</text>

  <!-- G 채널 -->
  <rect x="40" y="126" width="100" height="44" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="90" y="144" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">G (초록)</text>
  <text fill="currentColor" x="90" y="161" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">y 방향 기울기</text>

  <!-- 화살표 G → 설명 -->
  <line x1="140" y1="148" x2="168" y2="148" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="168,144 176,148 168,152" fill="currentColor"/>
  <text fill="currentColor" x="182" y="145" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.55">128 = 수정 없음</text>
  <text fill="currentColor" x="182" y="158" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.55">&lt;128 / &gt;128 → 하 / 상 기울기</text>

  <!-- B 채널 -->
  <rect x="40" y="184" width="100" height="44" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1"/>
  <text fill="currentColor" x="90" y="202" text-anchor="middle" font-size="12" font-weight="bold" font-family="sans-serif">B (파랑)</text>
  <text fill="currentColor" x="90" y="219" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">z 방향 (표면 수직)</text>

  <!-- 화살표 B → 설명 -->
  <line x1="140" y1="206" x2="168" y2="206" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="168,202 176,206 168,210" fill="currentColor"/>
  <text fill="currentColor" x="182" y="203" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.55">255 = 표면 수직 (기본)</text>
  <text fill="currentColor" x="182" y="216" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.55">값이 작을수록 기울어짐</text>

  <!-- 하단 기본값 설명 -->
  <line x1="60" y1="245" x2="360" y2="245" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
  <text fill="currentColor" x="210" y="263" text-anchor="middle" font-size="10" font-family="sans-serif">기본값 (128, 128, 255) = 푸른 보라색 → 수정 없음 (평평)</text>
  <text fill="currentColor" x="210" y="276" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">값이 128에서 벗어날수록 해당 방향으로 법선이 기울어짐</text>
</svg>
</div>

<br>

렌더링 시 GPU는 픽셀마다 노멀맵에서 법선 방향을 읽어, 스무스 셰이딩으로 보간된 법선을 수정합니다.
수정된 법선으로 조명을 계산하면, 실제 표면은 평평하지만 빛이 요철에 반응하는 것처럼 보입니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="270" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">노멀맵 적용 전후</text>

  <!-- ===== 왼쪽: 적용 전 ===== -->
  <rect x="15" y="38" width="245" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="138" y="58" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">적용 전 (평평한 면)</text>

  <!-- 표면 선 -->
  <line x1="38" y1="130" x2="252" y2="130" stroke="currentColor" stroke-width="2"/>

  <!-- 법선 화살표들 — 모두 위쪽 -->
  <line x1="58" y1="128" x2="58" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="54,90 58,78 62,90" fill="currentColor"/>
  <line x1="90" y1="128" x2="90" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="86,90 90,78 94,90" fill="currentColor"/>
  <line x1="122" y1="128" x2="122" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="118,90 122,78 126,90" fill="currentColor"/>
  <line x1="154" y1="128" x2="154" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="150,90 154,78 158,90" fill="currentColor"/>
  <line x1="186" y1="128" x2="186" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="182,90 186,78 190,90" fill="currentColor"/>
  <line x1="218" y1="128" x2="218" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="214,90 218,78 222,90" fill="currentColor"/>
  <line x1="245" y1="128" x2="245" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="241,90 245,78 249,90" fill="currentColor"/>

  <text fill="currentColor" x="138" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">법선이 모두 같은 방향</text>
  <text fill="currentColor" x="138" y="170" text-anchor="middle" font-size="10" font-family="sans-serif">→ 균일한 밝기</text>

  <!-- 표면 균일 밝기 표시 바 -->
  <rect x="48" y="180" width="180" height="8" rx="3" fill="currentColor" fill-opacity="0.12"/>
  <text fill="currentColor" x="138" y="203" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">밝기 균일</text>

  <!-- ===== 오른쪽: 적용 후 ===== -->
  <rect x="280" y="38" width="245" height="180" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text fill="currentColor" x="403" y="58" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">적용 후 (같은 면 + 노멀맵)</text>

  <!-- 표면 선 -->
  <line x1="303" y1="130" x2="517" y2="130" stroke="currentColor" stroke-width="2"/>

  <!-- 법선 화살표들 — 방향이 제각각 -->
  <!-- ↑ -->
  <line x1="323" y1="128" x2="323" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="319,90 323,78 327,90" fill="currentColor"/>
  <!-- ↗ -->
  <line x1="355" y1="128" x2="375" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="369,88 379,78 377,92" fill="currentColor"/>
  <!-- ↑ -->
  <line x1="387" y1="128" x2="387" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="383,90 387,78 391,90" fill="currentColor"/>
  <!-- ↖ -->
  <line x1="419" y1="128" x2="399" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="397,92 395,78 405,88" fill="currentColor"/>
  <!-- ↑ -->
  <line x1="451" y1="128" x2="451" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="447,90 451,78 455,90" fill="currentColor"/>
  <!-- ↗ -->
  <line x1="483" y1="128" x2="503" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="497,88 507,78 505,92" fill="currentColor"/>
  <!-- ↑ -->
  <line x1="510" y1="128" x2="510" y2="88" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="506,90 510,78 514,90" fill="currentColor"/>

  <text fill="currentColor" x="403" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">픽셀마다 법선이 다른 방향</text>
  <text fill="currentColor" x="403" y="170" text-anchor="middle" font-size="10" font-family="sans-serif">→ 밝고 어두운 부분이 생김</text>

  <!-- 표면 밝기 변화 표시 바 -->
  <rect x="313" y="180" width="40" height="8" rx="3" fill="currentColor" fill-opacity="0.08"/>
  <rect x="353" y="180" width="40" height="8" rx="3" fill="currentColor" fill-opacity="0.22"/>
  <rect x="393" y="180" width="40" height="8" rx="3" fill="currentColor" fill-opacity="0.06"/>
  <rect x="433" y="180" width="40" height="8" rx="3" fill="currentColor" fill-opacity="0.20"/>
  <rect x="473" y="180" width="40" height="8" rx="3" fill="currentColor" fill-opacity="0.10"/>
  <text fill="currentColor" x="403" y="203" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">요철이 있는 것처럼 보임</text>
</svg>
</div>

<br>

다만 노멀맵은 조명 계산에 쓰이는 법선만 수정할 뿐, 실제 메쉬의 정점을 움직이지는 않습니다. 음영으로 요철이 있는 것처럼 보일 뿐 표면 자체는 평평하기 때문에, 오브젝트를 옆에서 보면 윤곽선(실루엣)은 여전히 평평합니다.

<br>

노멀맵이 무엇인지 알았으니, 이제 접선이 왜 필요한지 살펴봅니다.

노멀맵은 법선 방향을 저장한 텍스처인데, 방향을 기록하려면 기준이 되는 좌표계가 있어야 합니다.
장면 전체의 절대 좌표인 월드 공간을 기준으로 저장하면, 벽돌 벽을 90° 회전시켰을 때 요철의 방향도 함께 회전해야 하지만 저장된 법선은 회전 전 방향을 그대로 가리키므로 요철이 깨집니다.

그래서 노멀맵은 월드 공간 대신 **접선 공간(Tangent Space)**을 기준으로 법선을 저장합니다.
접선 공간은 각 정점의 법선(Normal), 접선(Tangent), **바이탄젠트(Bitangent)** 세 벡터로 구성되는 좌표계로, 표면에 붙어 있어서 오브젝트가 회전하면 함께 회전합니다. 덕분에 오브젝트가 어떤 자세를 취하든 노멀맵의 요철 방향이 표면에 대해 올바르게 유지됩니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 380 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 380px; width: 100%;">
  <!-- 제목 -->
  <text fill="currentColor" x="190" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">접선 공간 (Tangent Space)</text>
  <text fill="currentColor" x="190" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">세 축이 서로 직교하는 표면 기준 좌표계</text>

  <!-- 원점 -->
  <circle cx="170" cy="190" r="3" fill="currentColor"/>

  <!-- 법선 (Normal) — 위쪽 (표면에 수직) -->
  <line x1="170" y1="187" x2="170" y2="70" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="165,74 170,58 175,74" fill="currentColor"/>
  <text fill="currentColor" x="185" y="66" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">법선 (N)</text>
  <text fill="currentColor" x="185" y="80" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">표면 수직 방향</text>

  <!-- 접선 (Tangent) — 오른쪽 (표면 위, U 방향) -->
  <line x1="173" y1="190" x2="320" y2="190" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="316,185 330,190 316,195" fill="currentColor"/>
  <text fill="currentColor" x="300" y="210" text-anchor="middle" font-size="11" font-weight="bold" font-family="sans-serif">접선 (T)</text>
  <text fill="currentColor" x="300" y="224" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">U 방향</text>

  <!-- 바이탄젠트 (Bitangent) — 오른쪽 아래 (표면 위, V 방향, 아이소메트릭 안쪽) -->
  <line x1="173" y1="193" x2="253" y2="237" stroke="currentColor" stroke-width="1.8"/>
  <polygon points="248,231 263,247 257,231" fill="currentColor"/>
  <text fill="currentColor" x="270" y="252" text-anchor="start" font-size="11" font-weight="bold" font-family="sans-serif">바이탄젠트 (B)</text>
  <text fill="currentColor" x="270" y="266" text-anchor="start" font-size="9" font-family="sans-serif" opacity="0.5">V 방향</text>

  <!-- 직교 표시: N⊥T -->
  <path d="M 180,190 L 180,180 L 170,180" fill="none" stroke="currentColor" stroke-width="1" opacity="0.4"/>
</svg>
</div>

<br>

노멀맵에 저장된 법선은 위에서 설명한 접선 공간 기준으로 기록되어 있습니다.
조명 계산은 월드 공간에서 이루어지므로, 노멀맵의 법선을 접선 공간에서 월드 공간으로 변환해야 합니다.

이 변환에 정점의 법선(N), 접선(T), 바이탄젠트(B) 세 벡터가 필요하며, 세 벡터를 열로 묶은 행렬을 **TBN 행렬**이라 합니다.
TBN 행렬은 미리 저장되는 것이 아니라, 셰이더에서 실시간으로 구성됩니다.

정점 속성에는 법선과 접선만 저장하고, 바이탄젠트는 이 두 벡터의 외적으로 계산합니다. 접선이 x, y, z 세 성분이 아닌 네 성분(x, y, z, w)인 이유가 이것으로, w는 이 외적의 방향(+1 또는 -1)을 결정하는 부호입니다.

GPU는 이렇게 구성한 TBN 행렬로 노멀맵의 법선을 월드 공간으로 변환하고, 그 결과로 조명을 계산합니다.

접선은 노멀맵을 위해 존재하는 속성이므로, 노멀맵을 사용하지 않는 메쉬에서는 정점에서 접선 데이터를 제거하여 정점당 16바이트를 절약할 수 있습니다.

---

### Color (정점 색상)

정점에 직접 색상을 지정하는 속성입니다. r, g, b, a 네 개의 값으로 구성됩니다. 일반적으로 각 채널을 8비트로 저장하여 정점당 4바이트를 차지합니다. HDR 등 더 넓은 범위가 필요한 경우 32비트 float으로 저장하며, 이 경우 16바이트가 됩니다. 법선이나 UV와 마찬가지로 삼각형 내부에서 보간되므로, 인접한 정점의 색상이 다르면 그 사이에서 색이 자연스럽게 섞입니다.

정점 색상은 텍스처 없이 단독으로 쓰일 수도 있고, 텍스처와 함께 쓰일 수도 있습니다. 로우폴리(Low-Poly) 아트 스타일에서는 텍스처 없이 정점 색상만으로 색을 표현합니다.

텍스처와 정점 색상을 함께 사용하는 경우도 있습니다. 넓은 지형에서 풀, 흙, 바위 텍스처를 섞어야 할 때, 정점 색상의 각 채널을 가중치로 활용합니다.
이것을 **버텍스 컬러 블렌딩(Vertex Color Blending)**이라 합니다. 지형의 삼각형 하나를 예로 들면 다음과 같습니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <!-- 왼쪽 제목 -->
  <text x="130" y="20" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 색상 (RGB 값)</text>

  <!-- 왼쪽 삼각형 -->
  <polygon points="130,50 40,190 220,190" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="130" y="145" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">보간</text>

  <!-- 정점 A (왼쪽 위) -->
  <circle cx="130" cy="50" r="4" fill="currentColor"/>
  <text x="130" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 A</text>
  <text x="130" y="30" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">R=1.0, G=0.0</text>

  <!-- 정점 B (왼쪽 아래 왼) -->
  <circle cx="40" cy="190" r="4" fill="currentColor"/>
  <text x="40" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 B</text>
  <text x="40" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">R=0.0, G=1.0</text>

  <!-- 정점 C (왼쪽 아래 우) -->
  <circle cx="220" cy="190" r="4" fill="currentColor"/>
  <text x="220" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 C</text>
  <text x="220" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">R=0.0, G=1.0</text>

  <!-- 가운데 화살표 -->
  <line x1="245" y1="120" x2="285" y2="120" stroke="currentColor" stroke-width="1.5"/>
  <polygon points="285,116 293,120 285,124" fill="currentColor"/>

  <!-- 오른쪽 제목 -->
  <text x="410" y="20" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">텍스처 블렌딩 결과</text>

  <!-- 오른쪽 삼각형 -->
  <polygon points="410,50 320,190 500,190" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="410" y="110" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">풀</text>
  <text x="410" y="125" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">↓</text>
  <text x="410" y="140" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.5">서서히 전환</text>
  <text x="410" y="155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.4">↓</text>
  <text x="410" y="170" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.6">흙</text>

  <!-- 정점 A (오른쪽 위) -->
  <circle cx="410" cy="50" r="4" fill="currentColor"/>
  <text x="410" y="42" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 A</text>
  <text x="410" y="30" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">풀 100%</text>

  <!-- 정점 B (오른쪽 아래 왼) -->
  <circle cx="320" cy="190" r="4" fill="currentColor"/>
  <text x="320" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 B</text>
  <text x="320" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">흙 100%</text>

  <!-- 정점 C (오른쪽 아래 우) -->
  <circle cx="500" cy="190" r="4" fill="currentColor"/>
  <text x="500" y="210" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 C</text>
  <text x="500" y="224" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">흙 100%</text>
</svg>
</div>

<br>

정점 A에 R=1.0, 정점 B·C에 G=1.0을 지정합니다. 셰이더가 R을 풀 텍스처의 가중치로, G를 흙 텍스처의 가중치로 사용하므로, 정점 A 근처에는 풀만, 정점 B·C 근처에는 흙만 나타납니다. 삼각형 내부에서는 R과 G가 보간되면서 풀에서 흙으로 자연스럽게 전환됩니다.

---

### 속성별 크기 정리

지금까지 살펴본 정점 속성의 크기를 정리하면 다음과 같습니다.

| 속성 | 크기 | 용도 |
|------|------|------|
| Position | 12 바이트 | 3D 공간 좌표 |
| Normal | 12 바이트 | 표면 방향 (빛 계산) |
| UV0 | 8 바이트 | 텍스처 매핑 좌표 |
| UV1 | 8 바이트 | 라이트맵 좌표 |
| Tangent | 16 바이트 | 노멀맵 변환 (TBN 행렬) |
| Color | 4 바이트 | 정점 색상/블렌딩 가중치 |
| **전체 합계** | **60 바이트** | **(모든 속성을 사용할 경우)** |

<br>

모든 속성을 사용하면 정점 하나가 60바이트를 차지합니다.
속성이 많을수록 정점당 메모리가 증가하고, GPU가 처리해야 할 데이터량도 늘어납니다. 렌더링에 실제로 필요한 속성만 포함하는 것이 중요합니다.

---

## 메쉬의 메모리 구조

메쉬 메모리의 대부분은 정점 버퍼와 인덱스 버퍼가 차지합니다. 두 버퍼의 크기를 합하면 메쉬의 메모리 크기를 추정할 수 있습니다.

<br>

$$\text{메쉬 메모리} = (\text{정점 수} \times \text{정점당 바이트}) + (\text{인덱스 수} \times \text{인덱스 크기})$$

> 골격 애니메이션을 사용하는 메쉬는 본 가중치(Bone Weight), 블렌드 셰이프(Blend Shape) 등의 데이터가 추가로 메모리를 차지합니다. 위 공식은 이러한 추가 데이터를 포함하지 않은 기본 추정입니다.

<br>

정점 수는 메쉬마다 정해져 있지만, 나머지 항목은 메쉬의 구성에 따라 달라집니다.

**정점당 바이트**는 사용하는 속성의 조합으로 결정되며, 앞의 속성별 크기 표 기준으로 Position + Normal + UV0만 사용하면 32바이트, 모든 속성을 사용하면 60바이트입니다.

**인덱스 수**는 삼각형 하나가 인덱스 3개를 사용하므로 삼각형 수의 3배가 됩니다.

**인덱스 크기**는 정점 수에 따라 16비트(2바이트) 또는 32비트(4바이트)가 결정되는데, 16비트 정수의 최대값이 65,535(2^16 - 1)이므로 정점이 이 범위를 넘으면 32비트 인덱스가 필요합니다. 가능하면 16비트 인덱스 범위 안에 들도록 메쉬를 관리하는 것이 메모리와 성능 양쪽에 유리합니다.

---

### 메모리 계산 예시

정점 10,000개, 삼각형 18,000개이고 노멀맵을 사용하는 캐릭터 메쉬로 실제 크기를 계산해 봅니다.

<br>

**정점 버퍼**

| 사용 속성 | 크기 |
|-----------|------|
| Position | 12 바이트 |
| Normal | 12 바이트 |
| UV0 | 8 바이트 |
| Tangent | 16 바이트 |
| **합계** | **48 바이트/정점** |

$$\text{정점 버퍼 크기} = 10{,}000 \times 48 = 480{,}000 \text{ 바이트} \approx 469 \text{ KB}$$

<br>

**인덱스 버퍼**

| 항목 | 값 |
|------|------|
| 인덱스 수 | 18,000 × 3 = 54,000 |
| 인덱스 크기 | 2 바이트 (정점 10,000개 < 65,535이므로 16비트) |

$$\text{인덱스 버퍼 크기} = 54{,}000 \times 2 = 108{,}000 \text{ 바이트} \approx 105 \text{ KB}$$

<br>

**합계**

$$\text{메쉬 메모리} = 469 + 105 \approx 574 \text{ KB}$$

<br>

하나의 캐릭터 메쉬가 약 574KB의 GPU 메모리를 차지합니다.

---

### 정점 속성과 메모리 절약

렌더링에 사용하지 않는 정점 속성을 제거하면 메쉬 메모리를 줄일 수 있습니다.

앞의 574KB 캐릭터 메쉬(정점 10,000개)를 기준으로, 노멀맵을 사용하지 않는 오브젝트에서 Tangent를 제거하면 약 156KB(10,000 × 16바이트), 라이트맵이 필요 없는 동적 오브젝트에서 UV1을 제거하면 약 78KB(10,000 × 8바이트)를 절약할 수 있습니다. 두 속성을 함께 제거하면 234KB가 줄어들어, 원래 크기의 약 40%를 절감하는 셈입니다.

---

## LOD (Level of Detail)

정점 속성을 줄이는 것 외에, 메쉬의 삼각형 수 자체를 상황에 따라 줄이는 방법도 있습니다.

카메라에서 멀리 있는 오브젝트는 화면에서 차지하는 픽셀 수가 적습니다. 5,000개의 삼각형으로 이루어진 오브젝트가 화면에서 50×50 픽셀 정도로 보인다면, 대부분의 삼각형은 1픽셀보다 작아 디테일이 보이지 않습니다.

이런 오브젝트에 원본과 같은 삼각형 수를 유지하는 것은 GPU 연산의 낭비입니다. **LOD(Level of Detail)**는 카메라와의 거리에 따라 메쉬의 복잡도를 단계적으로 바꿔 이 낭비를 줄이는 기법입니다. 카메라가 가까울 때는 원본 메쉬(LOD 0)를 사용하고, 거리가 멀어질수록 삼각형 수가 적은 메쉬로 전환합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 480 210" xmlns="http://www.w3.org/2000/svg" style="max-width: 480px; width: 100%;">
  <!-- 거리 축 -->
  <text x="60" y="18" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">카메라에서 가까움</text>
  <text x="420" y="18" text-anchor="end" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">카메라에서 멀어짐</text>
  <line x1="30" y1="28" x2="450" y2="28" stroke="currentColor" stroke-width="1" opacity="0.35"/>
  <polygon points="30,24 22,28 30,32" fill="currentColor" opacity="0.35"/>
  <polygon points="450,24 458,28 450,32" fill="currentColor" opacity="0.35"/>

  <!-- LOD 0 (140×100, 면적 14,000 = 100%) -->
  <rect x="30" y="50" width="140" height="100" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="100" y="168" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LOD 0</text>
  <text x="100" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">5,000 삼각형</text>
  <text x="100" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">원본 (가장 정밀)</text>

  <!-- LOD 1 (89×63, 면적 5,607 ≈ 40%) -->
  <rect x="200" y="87" width="89" height="63" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="245" y="168" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LOD 1</text>
  <text x="245" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">2,000 삼각형</text>
  <text x="245" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">중간 정밀</text>

  <!-- LOD 2 (44×32, 면적 1,408 ≈ 10%) -->
  <rect x="348" y="118" width="44" height="32" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.5"/>
  <text x="370" y="168" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">LOD 2</text>
  <text x="370" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">500 삼각형</text>
  <text x="370" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.55">가장 단순</text>
</svg>
</div>

---

### LOD의 효과

삼각형 수가 줄면 GPU가 처리해야 할 정점과 래스터화 대상이 함께 줄어듭니다. GPU는 **정점 셰이더(Vertex Shader)**에서 각 정점의 위치를 변환하고 속성을 처리하는데, 이 연산은 정점 수에 비례합니다. LOD 0(5,000 삼각형)에서 LOD 2(500 삼각형)로 전환하면 처리량이 약 1/10이 됩니다.

<br>

화면에 나무 100그루가 보이는 장면을 가정합니다. 가까운 나무 10그루만 LOD 0(5,000 삼각형)을 사용하고, 중간 거리 30그루는 LOD 1(2,000 삼각형), 먼 거리 60그루는 LOD 2(500 삼각형)를 사용하면:

<br>

$$\text{LOD 없이: } 100 \times 5{,}000 = 500{,}000 \text{ 삼각형}$$

<br>

| 거리 | 오브젝트 수 | LOD 단계 | 삼각형 수 |
|------|------------|---------|----------|
| 가까움 | 10 | LOD 0 (5,000) | 50,000 |
| 중간 | 30 | LOD 1 (2,000) | 60,000 |
| 멀리 | 60 | LOD 2 (500) | 30,000 |
| **합계** | **100** | | **140,000** |

<br>

총 삼각형 수가 500,000에서 140,000으로, 72% 감소합니다.

---

### LOD 전환 시 주의점

LOD 단계가 전환될 때, 삼각형 수가 갑자기 바뀌면서 모델의 실루엣이 순간적으로 변하는 현상을 **팝핑(Popping)**이라 합니다. 특히 카메라가 앞뒤로 움직여 LOD 경계를 반복적으로 넘나들면, 오브젝트가 계속 변형되어 눈에 띕니다.

**LOD 크로스페이드(Crossfade)**는 이 팝핑을 완화하는 기법입니다. 전환 시점에서 이전 LOD와 다음 LOD를 짧은 시간 동안 동시에 렌더링하면서 투명도를 교차시켜 부드럽게 전환합니다.

다만 크로스페이드 구간에서는 이전 LOD 메쉬와 다음 LOD 메쉬를 동시에 그리므로 드로우 콜이 2배가 되고, 여러 오브젝트가 동시에 전환되면 그만큼 부담이 커집니다.

---

### LOD 단계 설계

LOD 단계를 몇 개로 구성하고, 각 단계에서 삼각형을 얼마나 줄일지는 오브젝트의 특성에 따라 달라집니다. 일반적인 가이드라인은 다음과 같습니다.

<br>

| LOD | 원본 대비 삼각형 비율 |
|-----|----------------------|
| LOD 0 | 100% |
| LOD 1 | 50% |
| LOD 2 | 25% |
| Culled | 0% (비표시) |

<br>

> Unity의 LOD Group은 단순 거리가 아니라, 오브젝트가 화면에서 차지하는 비율(Screen Height Ratio)로 전환 시점을 결정합니다. 같은 거리에 있어도 큰 오브젝트는 화면을 많이 차지하므로 LOD 0을 유지하고, 작은 오브젝트는 더 일찍 LOD 1로 전환됩니다.

<br>

마지막 단계인 **Culled**는 오브젝트를 아예 렌더링하지 않는 것입니다. 화면 차지 비율이 설정한 임계값 이하로 떨어지면 적용되어, GPU 비용이 0이 됩니다.

LOD 단계별 메쉬는 3D 모델링 도구에서 미리 만들거나, 엔진의 도구로 원본 메쉬에서 자동 생성할 수 있습니다.

---

### LOD와 메쉬 메모리의 관계

LOD를 사용하면 프레임당 처리하는 삼각형 수는 줄어들지만, 모든 LOD 단계의 메쉬가 GPU 메모리에 동시에 올라가 있어야 하므로 메모리 사용량은 늘어납니다.
삼각형 비율이 100%, 50%, 25%일 때, 원본이 100KB라면 LOD 1이 약 50KB, LOD 2가 약 25KB로 총 175KB가 됩니다. 원본 대비 75%의 메모리가 추가되는 셈입니다.

다만 이 수치는 근사값입니다. 인덱스 버퍼는 삼각형 수에 정비례하지만, 정점 버퍼는 고유 정점 수에 비례합니다. 정점은 여러 삼각형에 공유될 수 있으므로, 삼각형을 제거해도 그 정점을 참조하는 다른 삼각형이 남아 있으면 정점 자체는 제거되지 않습니다.
따라서 삼각형을 50% 줄여도 전체 메모리가 정확히 50% 감소하지 않는 경우가 대부분입니다.

<br>

LOD는 메모리 사용량이 늘어나는 대신 프레임당 삼각형 처리량을 줄이는 트레이드오프입니다. 모든 오브젝트에 LOD를 적용하면 메모리 부담이 커지므로, 화면에 자주 등장하고 거리 변화가 큰 오브젝트에 우선적으로 적용하는 것이 효율적입니다.

---

## 마무리

정점과 삼각형의 기본 구조에서 출발하여, 인덱스 버퍼를 통한 중복 제거, 법선·UV·접선·색상 등 정점 속성의 역할, 메쉬 메모리 계산, LOD를 통한 처리량 절감까지 살펴보았습니다.

- 메쉬는 정점과 삼각형으로 구성됩니다. 삼각형은 항상 평면이고 항상 볼록하여 래스터화가 단순하므로, GPU의 기본 처리 단위로 쓰입니다.
- 인덱스 버퍼는 고유 정점만 저장하고 번호로 참조하여 메모리를 절약하고, GPU가 같은 정점을 식별할 수 있게 하여 포스트 트랜스폼 캐시 재사용을 가능하게 합니다.
- 정점에는 위치 외에 법선, UV, 접선, 색상 등의 속성이 포함되며, 모든 속성을 사용하면 정점 하나가 60바이트를 차지합니다. 사용하지 않는 속성을 제거하면 메모리를 절약할 수 있습니다.
- 메쉬 메모리의 대부분은 정점 버퍼와 인덱스 버퍼가 차지하며, 두 버퍼의 크기를 합하면 메쉬의 메모리 크기를 추정할 수 있습니다.
- LOD는 카메라와의 거리에 따라 메쉬 복잡도를 줄여 처리 비용을 절약하지만, 모든 LOD 단계의 메쉬가 GPU 메모리에 동시에 올라가는 트레이드오프가 있습니다.

메쉬가 오브젝트의 형태를 정의한다면, 텍스처는 그 형태에 색과 질감을 입힙니다. 텍스처는 메쉬보다 더 많은 메모리를 차지하는 경우가 대부분이며, [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)에서 텍스처의 메모리 구조와 압축 포맷을 다룹니다.

<br>

---

**관련 글**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)

**시리즈**
- **렌더링 기초 (1) - 메쉬의 구조 (현재 글)**
- [렌더링 기초 (2) - 텍스처와 압축](/dev/unity/RenderingFoundation-2/)
- [렌더링 기초 (3) - 머티리얼과 셰이더 기초](/dev/unity/RenderingFoundation-3/)

**전체 시리즈**
- [게임 루프의 원리 (1) - 프레임의 구조](/dev/unity/GameLoop-1/)
- [게임 루프의 원리 (2) - CPU-bound와 GPU-bound](/dev/unity/GameLoop-2/)
- **렌더링 기초 (1) - 메쉬의 구조** (현재 글)
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
- [모바일 전략 (2) - 빌드와 품질 전략](/dev/unity/MobileStrategy-2/)
