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

[하드웨어 기초 (1)](/dev/unity/HardwareBasics-1/)과 [(2)](/dev/unity/HardwareBasics-2/)에서는 CPU가 명령어를 실행하고 데이터를 가져오는 방식을 다루었습니다. CPU는 분기와 의존성이 많은 코드를 처리하는 데 강하지만, 같은 연산을 아주 많은 데이터에 동시에 적용하는 구조는 아닙니다.

화면을 그리는 작업에서는 이 차이가 크게 드러납니다. 장면을 그리려면 많은 정점과 픽셀에 좌표 변환, 조명 계산, 텍스처 샘플링 같은 연산을 반복해서 적용해야 합니다. 각 연산은 비교적 단순하더라도, 처리해야 할 대상의 수가 많고 서로 독립적인 경우가 많습니다.

초기에는 CPU가 이런 그래픽 계산까지 직접 처리했지만, 게임의 해상도와 장면 복잡도가 올라가면서 한계가 분명해졌습니다. 그래픽 처리는 복잡한 제어 흐름을 빠르게 처리하는 능력보다, 같은 종류의 연산을 대량으로 병렬 처리하는 능력을 더 많이 요구했기 때문입니다. GPU는 이 요구에 맞춰 그래픽 처리를 전담하기 위해 발전한 프로세서입니다.

이 글에서는 CPU가 그래픽을 직접 처리하던 소프트웨어 렌더링에서 시작해, 고정 기능 GPU, 프로그래머블 셰이더, 통합 셰이더 아키텍처, GPGPU로 이어지는 흐름을 따라갑니다. 각 단계에서 무엇이 부족했고, 그 부족함이 다음 구조로 어떻게 이어졌는지를 중심으로 다룹니다.

---

## CPU로 그래픽을 처리하던 시대

GPU가 보편화되기 전에는 3D 장면을 그리는 데 필요한 계산도 대부분 CPU가 처리했습니다. 이렇게 전용 그래픽 하드웨어에 맡기지 않고 CPU 코드로 화면을 그리는 방식을 **소프트웨어 렌더링(Software Rendering)**이라고 합니다.

이 방식에서는 CPU가 정점(vertex, 삼각형의 꼭짓점)을 화면 좌표로 변환하고, 삼각형이 차지하는 픽셀을 찾고, 각 픽셀의 색을 계산한 뒤, 결과를 **프레임버퍼**(화면에 출력할 이미지가 저장되는 메모리 영역)에 기록합니다. 지금은 GPU가 맡는 그래픽 파이프라인의 많은 단계가 당시에는 CPU 코드 안에 들어 있었습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 580 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%; min-width: 420px;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">소프트웨어 렌더링</text>
  <rect x="40" y="50" width="320" height="122" rx="6" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.4"/>
  <text x="200" y="74" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">CPU 코드</text>
  <rect x="68" y="100" width="78" height="38" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="107" y="123" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점</text>
  <line x1="146" y1="119" x2="174" y2="119" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="178,119 170,115 170,123" fill="currentColor"/>
  <rect x="178" y="100" width="78" height="38" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="217" y="123" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">픽셀</text>
  <line x1="256" y1="119" x2="284" y2="119" stroke="currentColor" stroke-width="1.3"/>
  <polygon points="288,119 280,115 280,123" fill="currentColor"/>
  <rect x="288" y="100" width="52" height="38" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="314" y="123" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">색</text>
  <line x1="360" y1="111" x2="418" y2="111" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="422,111 414,107 414,115" fill="currentColor"/>
  <rect x="422" y="76" width="118" height="70" rx="6" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="481" y="104" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프레임버퍼</text>
  <text x="481" y="124" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.8">최종 이미지</text>
  <text x="290" y="198" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.75">전용 그래픽 하드웨어 없이 CPU가 화면에 쓸 결과를 계산</text>
</svg>
</div>

<br>

소프트웨어 렌더링의 한계는 장면이 조금만 복잡해져도 빠르게 드러났습니다. 해상도가 올라가면 색을 계산해야 할 픽셀 수가 늘고, 모델이 복잡해지면 변환해야 할 정점 수가 늘어납니다. 두 작업은 모두 CPU 시간을 사용하므로, 그래픽 품질을 높일수록 게임 로직, AI, 물리 같은 다른 작업에 남는 시간이 줄어듭니다.

문제는 그래픽 작업의 성격이 CPU에 잘 맞지 않는다는 점입니다. 픽셀마다 비슷한 연산을 반복하고, 많은 정점에 같은 변환을 적용하는 일은 복잡한 분기를 빠르게 처리하는 능력보다 대량의 반복 연산을 병렬로 처리하는 능력을 요구합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 580 200" xmlns="http://www.w3.org/2000/svg" style="max-width: 580px; width: 100%; min-width: 420px;">
  <text x="290" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">CPU 자원의 경쟁</text>
  <rect x="45" y="50" width="210" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="150" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">게임 실행</text>
  <text x="150" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">로직 · AI · 물리</text>
  <rect x="325" y="50" width="210" height="78" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="430" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">그래픽 처리</text>
  <text x="430" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 · 픽셀 · 프레임버퍼</text>
  <line x1="255" y1="89" x2="325" y2="89" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="290" y="160" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">그래픽 부하가 커질수록 다른 작업에 남는 CPU 시간이 줄어듦</text>
</svg>
</div>

<br>

CPU가 그래픽 계산까지 계속 떠안는 구조에서는 해상도와 장면 복잡도를 높일수록 다른 작업에 쓸 시간이 줄어듭니다. 이 부담을 줄이기 위해 반복적인 그래픽 작업을 전담하는 별도의 하드웨어가 등장하기 시작했습니다.

---

## 고정 기능 GPU의 등장

초기 3D 가속기는 CPU가 하던 그래픽 작업을 한 번에 모두 가져간 장치가 아니었습니다. 게임 로직과 정점 변환은 여전히 CPU가 처리했고, 3D 가속기는 래스터화, 텍스처 매핑, 깊이 테스트, 프레임버퍼 기록처럼 픽셀마다 반복되는 작업을 덜어 주는 역할에 가까웠습니다.

이 변화만으로도 CPU의 부담은 크게 줄었습니다. 특히 텍스처 매핑은 삼각형 위의 각 픽셀에 텍스처 좌표를 보간하고, 텍스처에서 색을 읽어 필터링하는 작업입니다. 같은 형태의 연산이 많은 픽셀에 반복되므로, 범용 CPU보다 전용 회로에 잘 맞았습니다.

초기의 대표적인 3D 가속 카드로는 3dfx Voodoo 같은 제품이 자주 언급됩니다. 여기서 중요한 점은 특정 제품의 성능 수치가 아니라, 그래픽 파이프라인의 일부가 CPU 밖으로 분리되기 시작했다는 구조적 변화입니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 230" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">초기 3D 가속기의 작업 분담</text>
  <rect x="45" y="52" width="210" height="92" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="150" y="78" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">CPU</text>
  <text x="150" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">게임 로직 · AI · 물리</text>
  <text x="150" y="122" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 변환</text>
  <line x1="255" y1="98" x2="345" y2="98" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="349,98 341,94 341,102" fill="currentColor"/>
  <rect x="350" y="52" width="205" height="92" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.4"/>
  <text x="452" y="78" text-anchor="middle" font-family="sans-serif" font-size="12" font-weight="bold" fill="currentColor">3D 가속기</text>
  <text x="452" y="104" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">래스터화 · 텍스처 매핑</text>
  <text x="452" y="122" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">깊이 테스트 · 프레임버퍼</text>
  <text x="300" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">반복적인 픽셀 작업을 전용 하드웨어가 처리</text>
</svg>
</div>

<br>

다음으로 GPU 쪽으로 옮겨간 작업은 정점 변환과 조명 계산이었습니다. **T&L(Transform and Lighting)**은 모델의 정점을 화면에 그릴 위치로 변환하고, 조명에 따른 밝기를 계산하는 단계를 가리킵니다. 하드웨어 T&L이 도입된 뒤에는 이 계산도 CPU 코드가 아니라 GPU 내부의 고정된 회로에서 처리할 수 있게 되었습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">하드웨어 T&amp;L 이후</text>
  <rect x="45" y="50" width="210" height="66" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="150" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이전 CPU 부담</text>
  <text x="150" y="98" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 변환 · 조명 계산</text>
  <line x1="255" y1="83" x2="345" y2="83" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="349,83 341,79 341,87" fill="currentColor"/>
  <rect x="350" y="50" width="205" height="66" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
  <text x="452" y="76" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">GPU로 이동</text>
  <text x="452" y="98" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">그래픽 파이프라인 확대</text>
  <rect x="125" y="156" width="350" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="300" y="183" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">CPU는 게임 로직에 더 많은 시간을 쓸 수 있음</text>
</svg>
</div>

<br>

하드웨어 T&L은 더 많은 정점과 더 복잡한 장면을 실시간으로 다룰 수 있게 만든 중요한 전환점이었습니다. CPU가 그래픽 계산의 많은 부분에서 벗어나면서, 게임 로직과 시뮬레이션에 쓸 수 있는 시간이 늘어났습니다.

다만 이 시기의 GPU는 **고정 기능(Fixed Function)** 파이프라인이었습니다. 정점 변환, 조명 계산, 텍스처 블렌딩 같은 단계가 하드웨어에 정해진 방식으로 들어 있었고, 개발자는 행렬, 조명 값, 블렌딩 모드 같은 입력만 조정할 수 있었습니다. 원하는 알고리즘이 하드웨어에 없으면, 그 효과를 직접 구현하기 어려웠습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">고정 기능 파이프라인의 한계</text>
  <rect x="55" y="52" width="490" height="44" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="300" y="79" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">정해진 단계와 정해진 알고리즘</text>
  <rect x="55" y="132" width="210" height="44" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">개발자가 바꿀 수 있는 값</text>
  <rect x="335" y="132" width="210" height="44" rx="5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="440" y="158" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">직접 바꿀 수 없는 알고리즘</text>
  <line x1="300" y1="96" x2="300" y2="118" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="300,122 296,114 304,114" fill="currentColor"/>
</svg>
</div>

<br>

그래픽 품질을 더 다양하게 만들려면, GPU가 빠르게 처리하는 것만으로는 부족했습니다. 개발자가 정점과 픽셀의 계산 방식을 직접 정의할 수 있는 구조가 필요했습니다.

---

## 정점 처리와 픽셀 처리의 분리

고정 기능 GPU는 CPU의 그래픽 부담을 줄였지만, 내부 자원을 유연하게 나누어 쓰지는 못했습니다. 당시 GPU에는 정점을 처리하는 유닛과 픽셀을 처리하는 유닛이 따로 있었고, 각 유닛은 정해진 역할만 수행했습니다.

이렇게 나눈 이유는 두 작업의 성격이 다르기 때문입니다. 정점 처리는 메쉬의 꼭짓점을 화면에 그릴 위치로 변환하고 조명을 계산하는 작업입니다. 픽셀 처리는 래스터화 이후 만들어진 **프래그먼트(fragment)**를 대상으로 텍스처를 읽고 색을 계산하는 작업입니다. 프래그먼트는 아직 최종 픽셀로 확정되지 않은 후보 데이터이며, 깊이 테스트 같은 과정을 통과해야 화면에 남습니다.

문제는 정점 유닛과 픽셀 유닛의 비율이 칩을 만들 때 정해진다는 점이었습니다. 실행 중인 장면이 픽셀 계산을 많이 요구해도 남는 정점 유닛을 픽셀 처리에 돌릴 수 없고, 반대의 경우도 마찬가지였습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 220" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">분리된 정점 유닛과 픽셀 유닛</text>
  <rect x="55" y="58" width="190" height="72" rx="5" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1.4"/>
  <text x="150" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 유닛</text>
  <text x="150" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">좌표 변환 · 조명</text>
  <rect x="355" y="58" width="190" height="72" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="450" y="86" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">픽셀 유닛</text>
  <text x="450" y="108" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">텍스처 · 색상 계산</text>
  <line x1="245" y1="94" x2="355" y2="94" stroke="currentColor" stroke-width="1.4" stroke-dasharray="4,3"/>
  <text x="300" y="170" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">각 유닛은 정해진 역할만 수행하며 서로의 일을 대신하지 못함</text>
</svg>
</div>

<br>

이 한계는 장면의 성격이 한쪽으로 치우칠 때 드러납니다. 화면을 크게 덮는 오브젝트가 많으면 픽셀 유닛 쪽 일이 늘어나고, 작은 오브젝트가 많이 등장하면 정점 유닛 쪽 일이 늘어납니다. 한쪽 유닛이 밀려 있어도 다른 쪽 유닛은 자기 역할이 아니면 도와줄 수 없었습니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">부하가 한쪽으로 치우치는 경우</text>
  <text x="60" y="58" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">픽셀 부하가 큰 장면</text>
  <rect x="60" y="76" width="130" height="24" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="125" y="93" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 유닛 여유</text>
  <rect x="230" y="76" width="300" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="380" y="93" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">픽셀 유닛 과부하</text>
  <text x="60" y="142" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 부하가 큰 장면</text>
  <rect x="60" y="160" width="300" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="210" y="177" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 유닛 과부하</text>
  <rect x="400" y="160" width="130" height="24" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.7"/>
  <text x="465" y="177" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">픽셀 유닛 여유</text>
  <text x="300" y="224" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">남는 유닛이 있어도 다른 종류의 작업을 대신 처리하지 못함</text>
</svg>
</div>

<br>

이처럼 전용 유닛을 나누어 두는 방식은 빠르지만, 장면마다 달라지는 작업량을 유연하게 받아들이기 어렵습니다. 여기에 더해 개발자가 정점과 픽셀의 계산 방식을 직접 바꾸기 어렵다는 한계도 남아 있었습니다.

---

## 프로그래머블 셰이더의 등장

이 한계를 줄이려면 GPU가 정해진 효과만 처리하는 데서 그치지 않고, 개발자가 작성한 계산식을 실행할 수 있어야 했습니다. **프로그래머블 셰이더(Programmable Shader)**는 정점 하나를 어떻게 변환할지, 프래그먼트 하나의 색을 어떻게 계산할지를 작은 프로그램으로 작성해 GPU에서 실행하는 구조입니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">고정 기능에서 프로그래머블 셰이더로</text>
  <rect x="55" y="52" width="210" height="70" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">고정 기능</text>
  <text x="160" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정해진 알고리즘에 값만 입력</text>
  <line x1="265" y1="87" x2="335" y2="87" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="339,87 331,83 331,91" fill="currentColor"/>
  <rect x="340" y="52" width="205" height="70" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
  <text x="442" y="80" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">프로그래머블 셰이더</text>
  <text x="442" y="102" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">계산 방식을 코드로 작성</text>
  <rect x="115" y="162" width="370" height="44" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="300" y="188" text-anchor="middle" font-family="sans-serif" font-size="11" fill="currentColor">버텍스 셰이더와 픽셀 셰이더가 렌더링 표현력을 확장</text>
</svg>
</div>

<br>

초기 프로그래머블 셰이더는 사용할 수 있는 명령어 수가 적고, 조건문이나 반복문에도 제약이 많았습니다. 복잡한 재질 표현을 자유롭게 만들 수 있는 단계는 아니었지만, 정점과 픽셀의 계산 방식을 개발자가 직접 작성할 수 있다는 점만으로도 고정 기능 파이프라인과는 큰 차이가 있었습니다.

이후 셰이더 모델이 발전하면서 명령어 수, 정밀도, 분기, 텍스처 접근, 새로운 셰이더 단계가 점차 확장되었습니다. 그 결과 픽셀 단위 조명, 노멀 매핑, 카툰 셰이딩, 환경 반사, 서브서피스 스캐터링처럼 고정 기능만으로는 다루기 어려웠던 표현을 구현할 수 있게 되었습니다.

셰이더를 작성하는 방식도 함께 바뀌었습니다. 초기에는 GPU 명령어에 가까운 저수준 코드로 작성해야 했지만, 이후에는 C와 비슷한 문법의 셰이더 언어가 일반화되었습니다. Unity에서는 주로 HLSL 문법으로 셰이더를 작성하고, 빌드 과정에서 대상 그래픽스 API에 맞게 변환됩니다.

다만 셰이더를 코드로 작성할 수 있게 된 것과, GPU 내부 자원을 유연하게 나누어 쓰는 것은 별개의 문제였습니다.

---

## 통합 셰이더 아키텍처

정점 셰이더와 픽셀 셰이더를 코드로 작성할 수 있어도, 실행 유닛이 서로 분리되어 있으면 남는 자원을 다른 단계에 돌리기 어렵습니다. **통합 셰이더 아키텍처(Unified Shader Architecture)**는 이 전용 유닛 구분을 줄이고, 여러 셰이더 단계를 같은 실행 자원에서 처리하도록 만든 구조입니다.

이 구조에서는 정점 전용 유닛과 픽셀 전용 유닛 대신, 여러 종류의 셰이더를 실행할 수 있는 범용 셰이더 코어를 둡니다. 같은 코어가 버텍스 셰이더와 픽셀 셰이더를 실행하고, 이후에 추가된 지오메트리, 테셀레이션, 컴퓨트 셰이더도 필요에 따라 처리합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 170" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">분리형에서 통합형으로</text>
  <rect x="55" y="52" width="210" height="78" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="160" y="78" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">분리형</text>
  <text x="160" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">정점 유닛 / 픽셀 유닛</text>
  <text x="160" y="116" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">역할 고정</text>
  <line x1="265" y1="91" x2="335" y2="91" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="339,91 331,87 331,95" fill="currentColor"/>
  <rect x="340" y="52" width="205" height="78" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
  <text x="442" y="78" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">통합형</text>
  <text x="442" y="100" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">범용 셰이더 코어</text>
  <text x="442" y="116" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">부하에 따라 역할 배정</text>
</svg>
</div>

<br>

통합형 구조에서는 장면의 부하에 따라 코어 배정이 더 유연해집니다. 정점 처리가 많은 장면에서는 더 많은 코어가 버텍스 셰이더를 실행하고, 픽셀 처리가 무거운 장면에서는 더 많은 코어가 픽셀 셰이더를 실행합니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">동적 부하 분배</text>
  <text x="60" y="60" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">픽셀 부하가 큰 장면</text>
  <rect x="60" y="78" width="130" height="24" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="125" y="95" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 작업</text>
  <rect x="205" y="78" width="325" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="368" y="95" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">픽셀 작업</text>
  <text x="60" y="138" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">정점 부하가 큰 장면</text>
  <rect x="60" y="156" width="325" height="24" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
  <text x="223" y="173" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">정점 작업</text>
  <rect x="400" y="156" width="130" height="24" fill="currentColor" fill-opacity="0.10" stroke="currentColor" stroke-width="1"/>
  <text x="465" y="173" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">픽셀 작업</text>
</svg>
</div>

<br>

통합형 구조에서는 셰이더 단계가 늘어나도 각 단계마다 전용 하드웨어를 따로 둘 필요가 줄어듭니다. 새 단계도 같은 범용 셰이더 코어에서 실행할 수 있기 때문입니다.

예를 들어 **지오메트리 셰이더(Geometry Shader)**는 버텍스 셰이더와 래스터화 사이에 들어가는 단계입니다. 버텍스 셰이더가 넘긴 삼각형이나 선 같은 **프리미티브(primitive)**를 받아, 필요하면 새로운 프리미티브를 만들거나 기존 형태를 바꿉니다.

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 190" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">셰이더 단계의 확장</text>
  <rect x="40" y="58" width="120" height="38" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="100" y="81" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">버텍스 셰이더</text>
  <line x1="160" y1="77" x2="190" y2="77" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="194,77 186,73 186,81" fill="currentColor"/>
  <rect x="194" y="58" width="130" height="38" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="259" y="81" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">지오메트리 셰이더</text>
  <line x1="324" y1="77" x2="354" y2="77" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="358,77 350,73 350,81" fill="currentColor"/>
  <rect x="358" y="58" width="90" height="38" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="403" y="81" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">래스터화</text>
  <line x1="448" y1="77" x2="478" y2="77" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="482,77 474,73 474,81" fill="currentColor"/>
  <rect x="482" y="58" width="90" height="38" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="527" y="81" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">픽셀 셰이더</text>
  <text x="300" y="140" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">새로운 단계도 같은 범용 셰이더 코어에서 실행</text>
</svg>
</div>

<br>

GPU의 실행 코어가 여러 셰이더 단계를 처리하게 되면서, 같은 병렬 실행 구조를 렌더링 외의 계산에도 활용할 수 있는 가능성이 생겼습니다.

---

## GPGPU와 범용 연산

통합 셰이더 코어는 그래픽을 위해 만들어졌지만, 구조적으로는 같은 연산을 많은 데이터에 반복 적용하는 데 적합합니다. 이 특성은 꼭 렌더링에만 쓰일 필요가 없습니다. 입자 위치를 갱신하거나, 이미지의 모든 픽셀에 필터를 적용하거나, 큰 행렬을 계산하는 작업도 많은 데이터에 비슷한 연산을 반복한다는 점에서 같은 구조를 가지기 때문입니다.

GPU를 그래픽이 아닌 범용 계산에 활용하는 접근을 **GPGPU(General-Purpose computing on Graphics Processing Units)**라고 합니다. 초기에는 그래픽 API를 우회적으로 사용해야 했지만, 이후 CUDA, OpenCL, DirectCompute, Metal 같은 계산용 API가 등장하면서 GPU를 병렬 연산 장치로 다루는 방식이 일반화되었습니다.

GPGPU가 효과적인 작업에는 공통점이 있습니다. 데이터가 많고, 각 데이터에 적용하는 연산이 비슷하며, 항목끼리 서로 강하게 의존하지 않습니다. 반대로 분기가 복잡하거나 앞선 결과를 기다려야 하는 작업은 CPU 쪽이 더 적합할 수 있습니다.

게임에서도 이 성격은 그대로 적용됩니다. 파티클 시뮬레이션, GPU 스키닝, 절차적 메쉬 생성, 이미지 후처리처럼 많은 요소에 같은 계산을 적용하는 작업은 GPU 계산과 잘 맞습니다. 특히 계산 결과를 다시 GPU 렌더링에 바로 연결할 수 있을 때 효과가 큽니다. 반대로 결과를 CPU로 가져와 판단에 사용해야 한다면, GPU 작업이 끝날 때까지 기다리는 시간이 생길 수 있습니다.

### Unity의 Compute Shader

Unity에서 GPGPU를 활용하는 대표적인 수단이 **Compute Shader**입니다. 일반적인 렌더링 셰이더는 메시를 그리는 과정에서 호출됩니다. 버텍스 셰이더는 정점을 처리하고, 픽셀 셰이더는 화면에 남을 색을 계산합니다.

Compute Shader는 이 렌더링 흐름과 조금 다릅니다. 화면에 오브젝트를 그리기 위해 자동으로 호출되는 셰이더가 아니라, 개발자가 준비한 데이터에 병렬 계산을 적용하기 위해 직접 실행하는 셰이더입니다. 예를 들어 파티클 위치 배열, 타일별 조명 목록, 이미지 처리용 텍스처 같은 데이터를 GPU 버퍼나 텍스처에 넣고, `Dispatch()`로 실행 범위를 지정합니다.

실행이 시작되면 GPU는 많은 스레드를 만들어 각 스레드가 데이터의 일부를 처리하게 합니다. 결과는 다시 버퍼나 텍스처에 기록할 수 있고, 이후 렌더링에서 그 결과를 사용할 수도 있습니다.

<br>

**렌더링 셰이더 vs Compute Shader**

| 구분 | 렌더링 셰이더 | Compute Shader |
|:---|:---|:---|
| 호출 방식 | 드로우 콜 과정에서 실행 | `Dispatch()`로 직접 실행 |
| 처리 대상 | 정점, 프래그먼트 | 버퍼, 텍스처, 배열 형태의 데이터 |
| 결과 | 화면에 그릴 정점과 픽셀 색 | 버퍼나 텍스처에 기록된 계산 결과 |
| 대표 용도 | 오브젝트 렌더링 | 파티클, 후처리, 데이터 병렬 계산 |

<br>

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg" style="max-width: 600px; width: 100%; min-width: 430px;">
  <text x="300" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">Compute Shader 실행 흐름</text>
  <rect x="45" y="56" width="150" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="120" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">입력 버퍼</text>
  <line x1="195" y1="80" x2="245" y2="80" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="249,80 241,76 241,84" fill="currentColor"/>
  <rect x="250" y="56" width="150" height="48" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
  <text x="325" y="76" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">Compute Shader</text>
  <text x="325" y="92" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">스레드 그룹 병렬 실행</text>
  <line x1="400" y1="80" x2="450" y2="80" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="454,80 446,76 446,84" fill="currentColor"/>
  <rect x="455" y="56" width="100" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <text x="505" y="84" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">출력 버퍼</text>
  <rect x="115" y="154" width="370" height="44" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.4"/>
  <text x="300" y="180" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">렌더링 파이프라인 밖에서 데이터를 병렬 처리</text>
</svg>
</div>

<br>

Compute Shader도 렌더링 셰이더와 같은 범용 셰이더 코어에서 실행됩니다. 따라서 Compute Shader로 옮긴 계산은 CPU 부담을 줄일 수 있지만, GPU 입장에서는 렌더링 작업 옆에 또 다른 일이 추가되는 셈입니다. 이미 렌더링 부하가 큰 상황이라면 Compute Shader가 오히려 프레임 시간을 늘릴 수 있습니다.

특히 모바일 GPU에서는 전력, 발열, 메모리 대역폭의 여유가 작기 때문에 Compute Shader의 비용을 더 신중하게 봐야 합니다. 결과를 렌더링에서 다시 사용한다면 동기화 비용도 생길 수 있습니다. 모바일 GPU의 구조와 제약은 [하드웨어 기초 (4)](/dev/unity/HardwareBasics-4/)에서 이어서 다룹니다.

---

## GPU 발전 과정 요약

GPU의 발전은 단순히 더 빠른 칩이 나온 과정이라기보다, 이전 구조의 한계를 다음 구조가 줄여 온 과정에 가깝습니다.

<div style="text-align: center; margin: 1.5em 0; overflow-x: auto;">
<svg viewBox="0 0 640 260" xmlns="http://www.w3.org/2000/svg" style="max-width: 640px; width: 100%; min-width: 460px;">
  <text x="320" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">GPU 발전의 흐름</text>
  <rect x="30" y="58" width="110" height="48" rx="5" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1.2"/>
  <text x="85" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">CPU 렌더링</text>
  <text x="85" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">모든 단계가 CPU</text>
  <line x1="140" y1="82" x2="170" y2="82" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="174,82 166,78 166,86" fill="currentColor"/>
  <rect x="174" y="58" width="110" height="48" rx="5" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.2"/>
  <text x="229" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">고정 기능</text>
  <text x="229" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">전용 회로</text>
  <line x1="284" y1="82" x2="314" y2="82" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="318,82 310,78 310,86" fill="currentColor"/>
  <rect x="318" y="58" width="120" height="48" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="378" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">프로그래머블</text>
  <text x="378" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">셰이더 코드</text>
  <line x1="438" y1="82" x2="468" y2="82" stroke="currentColor" stroke-width="1.2"/>
  <polygon points="472,82 464,78 464,86" fill="currentColor"/>
  <rect x="472" y="58" width="138" height="48" rx="5" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <text x="541" y="78" text-anchor="middle" font-family="sans-serif" font-size="10" font-weight="bold" fill="currentColor">통합 셰이더</text>
  <text x="541" y="94" text-anchor="middle" font-family="sans-serif" font-size="9" fill="currentColor">범용 코어 풀</text>
  <rect x="180" y="158" width="280" height="46" rx="5" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="320" y="185" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor">GPGPU: 그래픽 외 병렬 계산으로 확장</text>
</svg>
</div>

<br>

CPU만으로는 그래픽 부하를 감당하기 어려워 전용 하드웨어가 등장했고, 고정된 알고리즘의 한계는 프로그래머블 셰이더로 이어졌습니다. 전용 유닛을 나누어 둔 구조의 비효율은 통합 셰이더 아키텍처로 줄어들었고, 그 범용 코어는 렌더링 밖의 병렬 계산에도 활용되기 시작했습니다.

---

## 마무리

이번 글에서는 GPU가 왜 CPU와 다른 구조로 발전했는지, 그리고 그래픽 전용 하드웨어가 어떻게 프로그래밍 가능한 병렬 프로세서로 바뀌었는지 다루었습니다.

- 소프트웨어 렌더링은 CPU가 그래픽 파이프라인 전체를 처리하므로, 그래픽 부하가 커질수록 게임 로직에 남는 시간이 줄어듭니다.
- 고정 기능 GPU는 래스터화, 텍스처 매핑, 정점 변환 같은 반복 작업을 전용 하드웨어로 옮겼지만, 개발자가 알고리즘 자체를 바꾸기는 어려웠습니다.
- 프로그래머블 셰이더는 정점과 픽셀의 계산 방식을 코드로 작성할 수 있게 하면서 렌더링 표현력을 크게 넓혔습니다.
- 통합 셰이더 아키텍처는 정점 전용 유닛과 픽셀 전용 유닛의 구분을 줄이고, 여러 셰이더 작업을 같은 범용 코어 풀에서 처리하도록 만들었습니다.
- GPGPU와 Compute Shader는 GPU의 병렬 처리 능력을 렌더링 밖의 계산에도 활용하는 흐름입니다.

<br>

다만 이 구조가 모든 기기에서 같은 방식으로 동작하는 것은 아닙니다. 모바일 환경에서는 CPU와 GPU가 하나의 칩 안에서 전력, 발열, 메모리 대역폭을 함께 나누어 씁니다.

[하드웨어 기초 (4)](/dev/unity/HardwareBasics-4/)에서는 모바일 SoC의 통합 구조, 전력 제약, 메모리 공유, 쓰로틀링이 게임 성능에 미치는 영향을 다룹니다.

<br>

---

**관련 글**
- [GPU 아키텍처 (1)](/dev/unity/GPUArchitecture-1/)

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
