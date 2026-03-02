---
layout: single
title: "그래픽스 수학 (2) - 행렬과 변환 - soo:bak"
date: "2026-02-27 01:11:00 +0900"
description: 행렬의 개념, 4x4 행렬, 동차 좌표, 이동/회전/스케일 행렬, TRS 순서, Unity Transform을 설명합니다.
tags:
  - Unity
  - 그래픽스
  - 수학
  - 행렬
  - 모바일
---

## 벡터에서 변환으로

[그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)에서 벡터를 사용하여 3D 공간의 위치, 방향, 속도를 표현하는 방법을 다루었습니다.

벡터는 "어디에 있는가", "어느 쪽을 향하는가", "얼마나 빠르게 움직이는가"를 수치로 나타내는 도구, 즉 3D 세계의 **현재 상태**를 기술하는 수단이었습니다.

<br>

하지만 게임에서 오브젝트는 가만히 있지 않습니다. 캐릭터가 앞으로 이동하고, 문이 회전하며 열리고, 아이템이 커졌다 작아졌다 합니다.

벡터가 현재 상태를 표현한다면, 그 상태를 **바꾸는** 수단도 필요합니다. 이것이 **변환(Transformation)**이고, 세 가지로 나뉩니다.

위치를 바꾸는 **이동(Translation)**, 방향을 바꾸는 **회전(Rotation)**, 크기를 바꾸는 **스케일(Scale)**입니다.

이동은 벡터 덧셈, 스케일은 성분별 곱셈, 회전은 삼각함수를 이용한 좌표 변환으로 각각 처리할 수 있습니다.

그런데 세 가지를 별개의 연산으로 다루면, 이동+회전+스케일이 동시에 필요할 때마다 서로 다른 연산을 순서대로 수행해야 합니다.

변환의 종류가 늘어날수록 코드가 복잡해지고, GPU가 수만 개의 정점에 같은 변환을 반복 적용하는 상황에서도 연산이 통일되어 있지 않으면 병렬 처리 효율이 떨어집니다.

<br>

세 변환을 하나의 곱셈 연산으로 통일하는 도구가 **행렬(Matrix)**입니다.

행렬 하나에 이동, 회전, 스케일을 모두 담으면, 정점마다 행렬-벡터 곱셈 한 번으로 모든 변환이 적용됩니다.

이 글에서는 행렬의 개념, 4×4 행렬을 사용하는 이유, 각 변환의 행렬 표현, 그리고 Unity Transform 컴포넌트와 행렬의 연결을 다룹니다.

---

## 행렬이란

행렬은 **숫자를 직사각형 모양으로 배열한 것**입니다.

가로 줄을 **행(row)**, 세로 줄을 **열(column)**이라 합니다. 행이 m개이고 열이 n개인 행렬을 m x n 행렬이라 합니다.

<br>

$$
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
$$

위 행렬은 2개의 행과 3개의 열을 가진 2 × 3 행렬입니다. 첫 번째 행은 $(1, \; 2, \; 3)$, 두 번째 행은 $(4, \; 5, \; 6)$입니다.

3D 그래픽스에서 행렬은 **변환을 표현하는 도구**입니다.

벡터가 "위치"나 "방향"을 나타낸다면, 행렬은 "그 위치나 방향을 어떻게 바꿀 것인가"를 나타냅니다.

행렬과 벡터를 곱하면 벡터에 변환이 적용됩니다. 회전을 나타내는 행렬이라면, 곱셈의 결과는 원래 벡터를 회전시킨 새로운 벡터입니다.

$$
\underbrace{\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}}_{\text{변환 행렬}} \underbrace{\begin{bmatrix} x \\ y \\ z \end{bmatrix}}_{\text{원래 벡터}} = \underbrace{\begin{bmatrix} x' \\ y' \\ z' \end{bmatrix}}_{\text{변환된 벡터}}
$$

<br>

곱셈 규칙은 간단합니다. 행렬의 n번째 행과 입력 벡터를 **내적(Dot Product)**한 값이 결과 벡터의 n번째 성분이 됩니다.

$$
\begin{aligned}
x' &= ax + by + cz \quad \text{(1행} \cdot \text{벡터)} \\
y' &= dx + ey + fz \quad \text{(2행} \cdot \text{벡터)} \\
z' &= gx + hy + iz \quad \text{(3행} \cdot \text{벡터)}
\end{aligned}
$$

<br>

회전과 스케일은 3x3 행렬로 표현할 수 있지만, 이동은 다릅니다. 3x3 곱셈은 원점을 움직일 수 없어서, 이동까지 포함하려면 4x4 행렬이 필요합니다.

---

## 왜 4x4 행렬인가 --- 동차 좌표

3x3 행렬과 벡터의 곱셈은 **선형 변환(linear transformation)**에 해당하며, 선형 변환은 항상 원점을 원점에 그대로 둡니다.

회전과 스케일은 원점을 기준으로 작동하므로 3x3 행렬로 표현할 수 있지만, **이동(translation)**은 원점 자체를 옮기는 변환이라 3x3 행렬로는 불가능합니다.

<br>

원점 (0, 0, 0)을 곱해 보면 이를 확인할 수 있습니다.

$$
\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}
$$

행렬의 값이 무엇이든 결과는 항상 (0, 0, 0)이므로, 이동을 처리하려면 곱셈과 별도로 덧셈이 필요합니다.

$$
\mathbf{p'} = R \cdot \mathbf{p} + \mathbf{t}
$$

수식에서 보듯이 곱셈과 덧셈이 섞여 있어, 하나의 연산으로 통일할 수 없습니다.

<br>

차원을 하나 늘리면 이 문제를 해결할 수 있습니다. 3D 좌표 (x, y, z)에 네 번째 성분 w를 추가하면 행렬도 4x4로 확장되고, 늘어난 열에 이동량을 배치하여 곱셈만으로 이동을 처리할 수 있습니다.

이렇게 확장한 좌표 (x, y, z, w)를 **동차 좌표(Homogeneous Coordinates)**라 하며, w의 값에 따라 이동의 적용 여부가 달라집니다.

$$
\text{3D 좌표:} \quad (x, \; y, \; z) \qquad \Longrightarrow \qquad \text{동차 좌표:} \quad (x, \; y, \; z, \; w)
$$

$$
\begin{aligned}
\text{위치(점):} \quad & (x, \; y, \; z, \; 1) & & \leftarrow \; \text{이동의 영향을 받음} \\
\text{방향(벡터):} \quad & (x, \; y, \; z, \; 0) & & \leftarrow \; \text{이동의 영향을 받지 않음}
\end{aligned}
$$

<br>

방향은 위치가 아니므로 이동의 영향을 받으면 안 됩니다. 오브젝트를 (10, 0, 0)으로 이동시켜도 "위를 향한다"는 방향 (0, 1, 0)은 그대로여야 합니다. w = 0이 이를 보장합니다.

이동, 회전, 스케일을 하나의 4x4 행렬로 표현하면 다음과 같습니다.

$$
\begin{bmatrix} \cdot & \cdot & \cdot & t_x \\ \cdot & \cdot & \cdot & t_y \\ \cdot & \cdot & \cdot & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} x' \\ y' \\ z' \\ 1 \end{bmatrix}
$$

왼쪽 위 3x3 영역(·)에 회전과 스케일이, 네 번째 열에 이동량 $(t_x, t_y, t_z)$가 배치됩니다. 하나의 곱셈으로 세 변환이 모두 적용됩니다.

<br>

GPU가 수만 개의 정점을 처리할 때도 같은 구조입니다.

각 정점을 동차 좌표 (x, y, z, 1)로 표현하고 동일한 4x4 행렬과 곱하면, 모든 정점에 같은 변환이 적용됩니다.

연산이 곱셈 하나로 통일되어 있어, GPU의 SIMD(Single Instruction, Multiple Data) 유닛이 하나의 명령으로 여러 정점을 동시에 처리할 수 있습니다.

---

## 이동 행렬 (Translation)

각 변환 행렬의 구조를 이동부터 살펴봅니다.

<br>

이동 행렬은 오브젝트의 위치를 바꾸는 변환입니다. 이동량 $(t_x, \; t_y, \; t_z)$가 앞서 본 네 번째 열에 들어갑니다.

$$
T = \begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

$$t_x$$ = x축 이동량, $$t_y$$ = y축 이동량, $$t_z$$ = z축 이동량

<br>

위치 벡터 (x, y, z, 1)에 이 행렬을 곱하면, 각 성분에 이동량이 더해집니다.

$$
\begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} x + t_x \\ y + t_y \\ z + t_z \\ 1 \end{bmatrix}
$$

<br>

첫 번째 성분을 직접 계산하면 $1 \cdot x + 0 \cdot y + 0 \cdot z + t_x \cdot w = x + t_x$입니다. 마지막 항 $t_x \cdot w$가 핵심으로, w = 1이면 이동량이 더해지고 w = 0이면 사라집니다.

방향 벡터(w = 0)로 확인하면 다음과 같습니다.

$$
\begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 0 \end{bmatrix} = \begin{bmatrix} x \\ y \\ z \\ 0 \end{bmatrix}
$$

$t_x \cdot 0 = 0$이므로 이동 성분이 사라지고, 방향 벡터는 변하지 않습니다. 위치와 방향의 차이가 w 값 하나로 구분됩니다.

---

## 회전 행렬 (Rotation)

이동 행렬이 위치를 바꾸었다면, 회전 행렬은 방향을 바꿉니다. 3D 공간에서 회전은 특정 축을 중심으로 일어나며, X축, Y축, Z축 각각의 회전 행렬이 있습니다. 회전각은 $\theta$(세타)로 표기합니다.

### X축 회전

X축을 중심으로 $\theta$만큼 회전하는 행렬입니다. X 성분은 변하지 않고, Y와 Z 성분이 $\cos\theta$와 $\sin\theta$의 조합으로 바뀝니다.

$$
R_x(\theta) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta & 0 \\ 0 & \sin\theta & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

### Y축 회전

Y축을 중심으로 $\theta$만큼 회전하는 행렬입니다. Y 성분은 변하지 않고, X와 Z 성분이 바뀝니다.

$$
R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -\sin\theta & 0 & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

<br>

$\theta = 90°$($\cos 90° = 0$, $\sin 90° = 1$)를 대입하여 (5, 2, 3) 위치의 정점을 변환하면 다음과 같습니다.

$$
\begin{bmatrix} 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} 5 \\ 2 \\ 3 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 2 \\ -5 \\ 1 \end{bmatrix}
$$

$$
\begin{aligned}
x' &= 0 \times 5 + 0 \times 2 + 1 \times 3 = 3 \quad \text{(원래 Z 성분)} \\
y' &= 2 \quad \text{(변하지 않음)} \\
z' &= -1 \times 5 + 0 \times 2 + 0 \times 3 = -5 \quad \text{(원래 X 성분의 부호 반전)}
\end{aligned}
$$

Y 성분(높이)은 그대로 유지되고, X와 Z 성분(수평 위치)이 바뀝니다. 게임에서 캐릭터를 Y축 기준으로 회전시키면 좌우로 도는 동작이 됩니다.

### Z축 회전

Z축을 중심으로 $\theta$만큼 회전하는 행렬입니다. Z 성분은 변하지 않고, X와 Y 성분이 바뀝니다.

$$
R_z(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 & 0 \\ \sin\theta & \cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

<br>

세 행렬에 공통 패턴이 있습니다. 회전 축의 성분은 변하지 않으므로 해당 행과 열은 단위 행렬(대각선이 1, 나머지가 0)과 동일하고, 실제로 변하는 나머지 2×2 부분에만 $\cos\theta$와 $\sin\theta$가 배치됩니다.

### 오일러 각과 짐벌 락

3D 공간에서 원하는 방향을 만들기 위해, X축, Y축, Z축 회전을 순서대로 적용하는 방식을 **오일러 각(Euler Angles)**이라 합니다. Unity의 Transform 인스펙터에서 Rotation 항목에 표시되는 (x, y, z) 값이 오일러 각입니다.

<br>

오일러 각은 직관적이지만 구조적 한계가 있습니다. 세 축의 회전을 순서대로 적용하는 과정에서, 특정 조건에서 축 하나가 다른 축과 겹치면서 **자유도가 하나 줄어드는 현상**이 발생합니다. 이 현상이 **짐벌 락(Gimbal Lock)**입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 760 380" xmlns="http://www.w3.org/2000/svg" style="max-width: 760px; width: 100%;">
  <defs>
    <marker id="gblAx" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#ED7D31"/>
    </marker>
    <marker id="gblAy" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#70AD47"/>
    </marker>
    <marker id="gblAz" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#5B9BD5"/>
    </marker>
    <marker id="gblAt" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- ===== MAIN: Left — Normal (3 orthogonal axes) ===== -->
  <g transform="translate(175, 135)">
    <text x="0" y="-100" text-anchor="middle" fill="currentColor" font-size="14" font-weight="bold" font-family="sans-serif">일반 상태</text>
    <text x="0" y="-83" text-anchor="middle" fill="currentColor" font-size="11" font-family="sans-serif" opacity="0.6">(3 자유도)</text>

    <circle cx="0" cy="0" r="3" fill="currentColor" opacity="0.3"/>

    <!-- X → lower-right (isometric) -->
    <line x1="0" y1="0" x2="69" y2="40" stroke="#ED7D31" stroke-width="2.5" marker-end="url(#gblAx)"/>
    <text x="80" y="46" fill="#ED7D31" font-size="12" font-weight="bold" font-family="sans-serif">X</text>

    <!-- Y → up -->
    <line x1="0" y1="0" x2="0" y2="-80" stroke="#70AD47" stroke-width="2.5" marker-end="url(#gblAy)"/>
    <text x="10" y="-75" fill="#70AD47" font-size="12" font-weight="bold" font-family="sans-serif">Y</text>

    <!-- Z → lower-left (isometric) -->
    <line x1="0" y1="0" x2="-69" y2="40" stroke="#5B9BD5" stroke-width="2.5" marker-end="url(#gblAz)"/>
    <text x="-82" y="46" fill="#5B9BD5" font-size="12" font-weight="bold" font-family="sans-serif">Z</text>

    <text x="0" y="78" text-anchor="middle" fill="currentColor" font-size="10.5" font-family="sans-serif">세 회전축이 직교</text>
    <text x="0" y="93" text-anchor="middle" fill="currentColor" font-size="10.5" font-family="sans-serif" opacity="0.7">→ 3 자유도</text>
  </g>

  <!-- ===== Transition Arrow ===== -->
  <g transform="translate(380, 130)">
    <line x1="-30" y1="0" x2="30" y2="0" stroke="currentColor" stroke-width="1.5" marker-end="url(#gblAt)"/>
    <text x="0" y="-18" text-anchor="middle" fill="currentColor" font-size="10" font-family="sans-serif" font-style="italic">중간 축 회전이</text>
    <text x="0" y="-6" text-anchor="middle" fill="currentColor" font-size="10" font-family="sans-serif" font-style="italic">±90°에 도달하면</text>
  </g>

  <!-- ===== MAIN: Right — Gimbal Lock (2 DOF) ===== -->
  <g transform="translate(585, 135)">
    <text x="0" y="-100" text-anchor="middle" fill="currentColor" font-size="14" font-weight="bold" font-family="sans-serif">짐벌 락</text>
    <text x="0" y="-83" text-anchor="middle" fill="currentColor" font-size="11" font-family="sans-serif" opacity="0.6">(2 자유도)</text>

    <circle cx="0" cy="0" r="3" fill="currentColor" opacity="0.3"/>

    <!-- Y → still up (independent) -->
    <line x1="0" y1="0" x2="0" y2="-80" stroke="#70AD47" stroke-width="2.5" marker-end="url(#gblAy)"/>
    <text x="10" y="-75" fill="#70AD47" font-size="12" font-weight="bold" font-family="sans-serif">Y</text>

    <!-- Z → lower-left (solid, offset +3,+4 perpendicular) -->
    <line x1="2" y1="3" x2="-67" y2="43" stroke="#5B9BD5" stroke-width="2.5" marker-end="url(#gblAz)"/>
    <text x="-55" y="56" fill="#5B9BD5" font-size="12" font-weight="bold" font-family="sans-serif">Z</text>

    <!-- X → NOW aligned with Z (dashed, offset -3,-4 perpendicular) -->
    <line x1="-2" y1="-3" x2="-71" y2="37" stroke="#ED7D31" stroke-width="2.5" stroke-dasharray="6,4" marker-end="url(#gblAx)"/>
    <text x="-83" y="33" fill="#ED7D31" font-size="12" font-weight="bold" font-family="sans-serif">X</text>

    <text x="0" y="78" text-anchor="middle" fill="currentColor" font-size="10.5" font-family="sans-serif">X축과 Z축의 회전축이 정렬</text>
    <text x="0" y="93" text-anchor="middle" fill="currentColor" font-size="10.5" font-family="sans-serif" opacity="0.7">→ 독립 자유도 1개 상실</text>
  </g>

  <!-- ===== INSET: Gimbal Rings (supplementary analogy) ===== -->
  <rect x="230" y="248" width="300" height="118" rx="6" fill="none" stroke="currentColor" stroke-width="0.8" stroke-dasharray="4,3" opacity="0.25"/>
  <text x="380" y="265" text-anchor="middle" fill="currentColor" font-size="10" font-family="sans-serif" opacity="0.5" font-style="italic">짐벌 장치에서의 비유</text>

  <!-- Inset Left: Normal gimbal rings (35% scale) -->
  <g transform="translate(310, 318)">
    <ellipse cx="0" cy="0" rx="44" ry="15" fill="none" stroke="#5B9BD5" stroke-width="1.5"/>
    <ellipse cx="0" cy="0" rx="11" ry="33" fill="none" stroke="#70AD47" stroke-width="1.5"/>
    <g transform="rotate(-30)">
      <ellipse cx="0" cy="0" rx="26" ry="9" fill="none" stroke="#ED7D31" stroke-width="1.5"/>
    </g>
    <circle cx="0" cy="0" r="2" fill="currentColor" opacity="0.3"/>
  </g>

  <!-- Inset transition -->
  <line x1="368" y1="318" x2="392" y2="318" stroke="currentColor" stroke-width="1" marker-end="url(#gblAt)" opacity="0.4"/>

  <!-- Inset Right: Locked gimbal rings (35% scale) -->
  <g transform="translate(450, 318)">
    <ellipse cx="0" cy="0" rx="11" ry="33" fill="none" stroke="#70AD47" stroke-width="1.5"/>
    <ellipse cx="0" cy="0" rx="44" ry="15" fill="none" stroke="#5B9BD5" stroke-width="1.5"/>
    <ellipse cx="0" cy="0" rx="33" ry="11" fill="none" stroke="#ED7D31" stroke-width="1.5" stroke-dasharray="5,3"/>
    <circle cx="0" cy="0" r="2" fill="currentColor" opacity="0.3"/>
  </g>
</svg>
</div>

<br>

예를 들어, 중간 축(Y)의 회전이 90°에 가까워지면 X축 회전과 Z축 회전의 회전축이 정렬되어 같은 효과를 내게 됩니다. 카메라가 정면을 바라보다가 완전히 위를 향하면, 좌우 회전과 기울이기가 구분되지 않는 상황이 짐벌 락입니다. 이 상태에서는 원하는 방향으로의 부드러운 회전이 불가능합니다.

이 문제를 해결하기 위해 **쿼터니언(Quaternion)**이라는 수학적 표현이 사용됩니다. 쿼터니언은 4개의 성분 (x, y, z, w)으로 3D 회전을 표현하며, 짐벌 락이 발생하지 않고 두 회전 사이의 부드러운 보간(Slerp)도 가능합니다.

<br>

Unity의 `transform.rotation`은 내부적으로 쿼터니언을 사용합니다. 인스펙터에 표시되는 오일러 각 값은 사람이 읽기 쉽도록 변환하여 보여주는 것이고, 실제 데이터는 쿼터니언으로 저장됩니다.

---

## 스케일 행렬 (Scale)

이동과 회전에 이어, 세 번째 변환인 스케일은 오브젝트의 크기를 바꾸는 변환입니다. 각 축의 스케일 값 $(s_x, \; s_y, \; s_z)$를 4×4 행렬의 **대각 성분**에 배치합니다.

<br>

$$
S = \begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

$$s_x$$ = x축 스케일, $$s_y$$ = y축 스케일, $$s_z$$ = z축 스케일

<br>

이 행렬을 벡터 (x, y, z, 1)에 곱하면, 각 성분이 해당 축의 스케일 값으로 곱해집니다.

$$
\begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} s_x \cdot x \\ s_y \cdot y \\ s_z \cdot z \\ 1 \end{bmatrix}
$$

<br>

$s_x = s_y = s_z = 2$이면 오브젝트가 X, Y, Z 모든 축에서 2배로 커집니다. 이처럼 모든 축의 스케일 값이 동일한 경우를 **균일 스케일(Uniform Scale)**이라 합니다.

### 비균일 스케일과 부작용

**비균일 스케일(Non-uniform Scale)**은 축마다 스케일 값이 다른 변환입니다. (2, 1, 1)이면 X축으로만 2배 늘어납니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Title: Uniform -->
  <text fill="currentColor" x="130" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">균일 스케일 (2, 2, 2)</text>
  <text fill="currentColor" x="130" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">모든 방향으로 동일하게 확대</text>
  <!-- Original square -->
  <rect x="55" y="65" width="40" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <!-- Arrow -->
  <line x1="110" y1="85" x2="140" y2="85" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="142,85 136,81 136,89" fill="currentColor" opacity="0.4"/>
  <!-- Scaled square -->
  <rect x="155" y="45" width="80" height="80" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <!-- Title: Non-uniform -->
  <text fill="currentColor" x="400" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">비균일 스케일 (2, 1, 1)</text>
  <text fill="currentColor" x="400" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">X축만 늘어남</text>
  <!-- Original square -->
  <rect x="315" y="65" width="40" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <!-- Arrow -->
  <line x1="370" y1="85" x2="400" y2="85" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="402,85 396,81 396,89" fill="currentColor" opacity="0.4"/>
  <!-- Scaled rectangle (X only) -->
  <rect x="415" y="65" width="80" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <!-- Dimension labels -->
  <text fill="currentColor" x="130" y="155" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">비율이 유지됨</text>
  <text fill="currentColor" x="400" y="155" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">비율이 왜곡됨</text>
</svg>
</div>

<br>

비균일 스케일은 편리하지만, 렌더링과 물리 양쪽에서 부작용을 일으킵니다.

첫째, **법선 벡터가 왜곡**됩니다.

메쉬가 축마다 다른 비율로 늘어나면 표면의 기울기가 바뀌는데, 법선에 같은 스케일 행렬을 그대로 적용하면 바뀐 기울기를 반영하지 못해 법선이 표면에 수직이 아닌 방향을 가리킵니다.

올바른 법선을 구하려면, 스케일 행렬의 역행렬(변환을 되돌리는 행렬)을 구한 뒤 행과 열을 뒤바꾼 **역전치 행렬(Inverse Transpose)**을 법선에 곱해야 합니다. 이 추가 연산이 성능 비용으로 이어집니다.

<br>

둘째, **물리 엔진의 충돌 판정이 부정확**해질 수 있습니다.

구(Sphere) 콜라이더에 비균일 스케일을 적용하면 형상이 타원이 되어야 하지만, Unity의 SphereCollider는 타원을 지원하지 않아 실제 메쉬와 콜라이더가 어긋납니다.

<br>

셋째, 부모 오브젝트에 비균일 스케일이 적용된 상태에서 자식을 회전시키면 **전단(Shearing)**이 나타날 수 있습니다.

직사각형이 평행사변형처럼 비틀리는 변형으로, 비균일 스케일 행렬과 회전 행렬을 곱하면 축이 직교하지 않게 되면서 발생합니다.

<br>

모바일에서는 역전치 행렬 계산 등 추가 연산의 성능 부담이 크므로, 가능하면 균일 스케일을 사용하고 형상을 바꿔야 할 때는 메쉬 자체를 수정하는 편이 낫습니다.

---

## 변환의 합성 --- 행렬 곱셈

지금까지 이동, 회전, 스케일 행렬을 각각 살펴보았는데, 실제 게임에서는 세 변환이 동시에 필요합니다. 캐릭터 하나만 봐도 어딘가에 서 있고, 어딘가를 바라보며, 일정한 크기를 갖습니다.

행렬 곱셈은 이 세 개별 행렬을 하나의 4×4 행렬 $M$으로 합성할 수 있게 해 줍니다.

<br>

$$
M = \underbrace{\begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}}_{T} \times \underbrace{\begin{bmatrix} \cdot & \cdot & \cdot & 0 \\ \cdot & \cdot & \cdot & 0 \\ \cdot & \cdot & \cdot & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}}_{R} \times \underbrace{\begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}}_{S}
$$

이처럼 개별 변환을 먼저 정의한 뒤 곱셈으로 합성하는 구조 덕분에, 변환의 종류나 개수가 달라져도 최종 결과는 언제나 하나의 $M$으로 귀결됩니다.

### 행렬 곱셈의 비교환성

숫자 곱셈에서는 $3 \times 5 = 5 \times 3$이지만, 행렬 곱셈에서는 $A \times B \neq B \times A$입니다.

**곱하는 순서가 바뀌면 결과도 달라집니다.**

오브젝트가 원점 (0, 0, 0)에 있을 때, 앞서 본 Y축 회전 행렬($\theta = +90°$)과 (5, 0, 0) 이동을 어떤 순서로 적용하느냐에 따라 결과가 완전히 달라집니다. $R_y(+90°)$는 +X 방향을 -Z 방향으로 회전시키는 행렬입니다.

```
행렬 곱셈의 비교환성 — 이동 후 회전 vs 회전 후 이동
(오브젝트 초기 위치: 원점, 회전: Ry(+90°) — +X를 -Z로 회전)

이동 후 회전:
  1) 오브젝트를 (5, 0, 0)으로 이동
  2) 원점 기준 Ry(+90°) 적용 → +X 방향이 -Z 방향으로 회전
  → 오브젝트는 (0, 0, -5) 위치에 놓임

회전 후 이동:
  1) 원점 기준 Ry(+90°) 적용 (원점이므로 위치 변화 없음)
  2) (5, 0, 0)으로 이동
  → 오브젝트는 (5, 0, 0) 위치에 놓임

→ 같은 변환이라도 적용 순서에 따라 결과가 전혀 다름
```

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 540 298" xmlns="http://www.w3.org/2000/svg" style="max-width: 540px; width: 100%;">
  <defs>
    <marker id="ncArw" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- XZ 평면 시점 (Y축 회전이 이 평면에서 발생) -->
  <text fill="currentColor" x="270" y="18" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">위에서 내려다본 XZ 평면 (Y축은 화면 수직 방향, ⊙ 표시)</text>

  <!-- ===== Left: 이동 → 회전 ===== -->
  <text fill="currentColor" x="130" y="36" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">이동 → 회전</text>

  <g transform="translate(115, 128)">
    <!-- Axes -->
    <line x1="-10" y1="0" x2="108" y2="0" stroke="currentColor" stroke-width="1" opacity="0.25"/>
    <text fill="currentColor" x="113" y="4" font-size="10" font-family="sans-serif" opacity="0.35">X</text>
    <line x1="0" y1="10" x2="0" y2="-82" stroke="currentColor" stroke-width="1" opacity="0.25"/>
    <text fill="currentColor" x="-12" y="-78" font-size="10" font-family="sans-serif" opacity="0.35">Z</text>

    <!-- Y axis indicator (perpendicular to screen) -->
    <circle cx="0" cy="0" r="6" fill="none" stroke="currentColor" stroke-width="0.8" opacity="0.2"/>
    <circle cx="0" cy="0" r="1.2" fill="currentColor" opacity="0.2"/>

    <!-- Origin -->
    <circle cx="0" cy="0" r="3.5" fill="currentColor" opacity="0.5"/>
    <text fill="currentColor" x="-12" y="20" font-size="9" font-family="sans-serif" opacity="0.5">원점</text>

    <!-- Step ①: 이동 along X -->
    <line x1="7" y1="0" x2="85" y2="0" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#ncArw)"/>
    <text fill="currentColor" x="50" y="-10" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">① 이동 (+5,0,0)</text>
    <circle cx="93" cy="0" r="3.5" fill="currentColor" opacity="0.7"/>
    <text fill="currentColor" x="99" y="-6" font-size="9" font-family="sans-serif" opacity="0.55">(5,0,0)</text>

    <!-- Step ②: Y축 90° 회전 — arc from X-axis to −Z direction -->
    <path d="M 89,6 A 88,88 0 0,1 6,88" stroke="currentColor" stroke-width="1.8" fill="none" stroke-dasharray="5,3" marker-end="url(#ncArw)"/>
    <text fill="currentColor" x="78" y="66" font-size="9" font-family="sans-serif" opacity="0.6">② Ry(+90°)</text>

    <!-- Final point at (0,0,−5) — −Z direction (below origin) -->
    <circle cx="0" cy="93" r="5" fill="currentColor"/>
    <text fill="currentColor" x="10" y="108" font-size="10" font-weight="bold" font-family="sans-serif">(0, 0, −5)</text>
  </g>

  <!-- ===== Right: 회전 → 이동 ===== -->
  <text fill="currentColor" x="400" y="36" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">회전 → 이동</text>

  <g transform="translate(385, 128)">
    <!-- Axes -->
    <line x1="-10" y1="0" x2="108" y2="0" stroke="currentColor" stroke-width="1" opacity="0.25"/>
    <text fill="currentColor" x="113" y="4" font-size="10" font-family="sans-serif" opacity="0.35">X</text>
    <line x1="0" y1="10" x2="0" y2="-82" stroke="currentColor" stroke-width="1" opacity="0.25"/>
    <text fill="currentColor" x="-12" y="-78" font-size="10" font-family="sans-serif" opacity="0.35">Z</text>

    <!-- Y axis indicator (perpendicular to screen) -->
    <circle cx="0" cy="0" r="6" fill="none" stroke="currentColor" stroke-width="0.8" opacity="0.2"/>
    <circle cx="0" cy="0" r="1.2" fill="currentColor" opacity="0.2"/>

    <!-- Origin -->
    <circle cx="0" cy="0" r="3.5" fill="currentColor" opacity="0.5"/>
    <text fill="currentColor" x="-12" y="20" font-size="9" font-family="sans-serif" opacity="0.5">원점</text>

    <!-- Step ①: Y축 90° 회전 at origin (rotation arc, no position change) -->
    <path d="M 14,0 A 14,14 0 1,1 0,-14" stroke="currentColor" stroke-width="1.5" fill="none" stroke-dasharray="4,3" marker-end="url(#ncArw)"/>
    <text fill="currentColor" x="22" y="32" font-size="9" font-family="sans-serif" opacity="0.6">① Ry(+90°)</text>
    <text fill="currentColor" x="22" y="44" font-size="8" font-family="sans-serif" opacity="0.4">(위치 변화 없음)</text>

    <!-- Step ②: 이동 along X -->
    <line x1="7" y1="0" x2="85" y2="0" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5,3" marker-end="url(#ncArw)"/>
    <text fill="currentColor" x="50" y="-10" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.6">② 이동 (+5,0,0)</text>

    <!-- Final point at (5,0,0) -->
    <circle cx="93" cy="0" r="5" fill="currentColor"/>
    <text fill="currentColor" x="99" y="-6" font-size="10" font-weight="bold" font-family="sans-serif">(5, 0, 0)</text>
  </g>

  <!-- Bottom caption -->
  <text fill="currentColor" x="270" y="286" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">같은 변환이라도 적용 순서에 따라 결과가 전혀 다름</text>
</svg>
</div>

### TRS 순서

행렬 곱셈의 순서가 결과를 바꾸기 때문에, 3D 그래픽스에서는 변환을 적용하는 표준 순서가 정해져 있습니다.

**Scale → Rotate → Translate** 순서입니다.

오브젝트가 아직 원점에 있을 때 크기를 조절하고, 원점 기준으로 회전하여 방향을 잡은 뒤, 최종 위치로 옮깁니다.

스케일과 회전은 원점을 기준으로 작동하는 변환이므로, 이동 전에 적용해야 위치를 건드리지 않고 형태와 방향만 바꿀 수 있습니다.

이 적용 순서를 행렬 곱셈으로 표기하면 $M = T \times R \times S$입니다.

**TRS 순서**라는 이름은 이 행렬 표기에서 T, R, S가 왼쪽부터 나열되는 순서에서 유래합니다.

<br>

다만, 표기 순서와 적용 순서는 반대입니다. $T \times R \times S$에서 왼쪽에 있는 T가 먼저 적용되는 것이 아니라, 행렬 곱셈에서는 **오른쪽 행렬이 먼저 적용**됩니다. 벡터 $\mathbf{v}$에 가장 가까운 $S$가 첫 번째로 곱해지고, 그 결과에 $R$, 마지막으로 $T$가 곱해집니다.

$$
\begin{aligned}
\mathbf{v'} &= M \times \mathbf{v} \\
&= T \times R \times S \times \mathbf{v} \\
&= T \times (R \times (S \times \mathbf{v}))
\end{aligned}
$$

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 440 90" xmlns="http://www.w3.org/2000/svg" style="max-width: 440px; width: 100%;">
  <!-- Boxes -->
  <rect x="40" y="20" width="80" height="36" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="80" y="42" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">T (이동)</text>
  <rect x="180" y="20" width="80" height="36" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="220" y="42" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">R (회전)</text>
  <rect x="320" y="20" width="80" height="36" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text fill="currentColor" x="360" y="42" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">S (스케일)</text>
  <!-- Multiplication signs -->
  <text fill="currentColor" x="140" y="43" text-anchor="middle" font-size="16" font-family="sans-serif" opacity="0.5">×</text>
  <text fill="currentColor" x="280" y="43" text-anchor="middle" font-size="16" font-family="sans-serif" opacity="0.5">×</text>
  <!-- Application order arrow (right to left) -->
  <line x1="380" y1="72" x2="60" y2="72" stroke="currentColor" stroke-width="1" opacity="0.4"/>
  <polygon points="58,72 66,68 66,76" fill="currentColor" opacity="0.4"/>
  <text fill="currentColor" x="220" y="86" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">← 적용 순서 (오른쪽이 먼저)</text>
</svg>
</div>

<br>

앞의 비교환성 예시에서 확인한 것처럼, TRS 순서를 지키지 않으면 결과가 달라집니다.

이동을 먼저 적용하면 오브젝트가 원점에서 이미 멀어진 상태이므로, 이후의 회전이 제자리에서 도는 자전이 아니라 원점을 중심으로 도는 공전이 됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 700 148" xmlns="http://www.w3.org/2000/svg" style="max-width: 700px; width: 100%;">
  <defs>
    <marker id="trsArw" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>

  <!-- ===== State 0: 초기 (작은 ▲) ===== -->
  <g transform="translate(60, 58)">
    <!-- Crosshair (origin) -->
    <line x1="-7" y1="0" x2="7" y2="0" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
    <line x1="0" y1="-7" x2="0" y2="7" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
    <!-- Small ▲ -->
    <polygon points="0,-10 -7,8 7,8" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  </g>
  <text fill="currentColor" x="60" y="95" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(원점, 기본 크기)</text>

  <!-- Arrow ① Scale -->
  <line x1="90" y1="58" x2="148" y2="58" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4" marker-end="url(#trsArw)"/>
  <text fill="currentColor" x="119" y="48" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.7">① Scale</text>

  <!-- ===== State 1: Scale 후 (큰 ▲) ===== -->
  <g transform="translate(200, 58)">
    <!-- Crosshair -->
    <line x1="-7" y1="0" x2="7" y2="0" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
    <line x1="0" y1="-7" x2="0" y2="7" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
    <!-- Big ▲ -->
    <polygon points="0,-20 -14,16 14,16" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  </g>
  <text fill="currentColor" x="200" y="100" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(원점, 크기 변화)</text>

  <!-- Arrow ② Rotate -->
  <line x1="240" y1="58" x2="308" y2="58" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4" marker-end="url(#trsArw)"/>
  <text fill="currentColor" x="274" y="48" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.7">② Rotate</text>

  <!-- ===== State 2: Rotate 후 (큰 ▶) ===== -->
  <g transform="translate(360, 58)">
    <!-- Crosshair -->
    <line x1="-7" y1="0" x2="7" y2="0" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
    <line x1="0" y1="-7" x2="0" y2="7" stroke="currentColor" stroke-width="0.8" opacity="0.3"/>
    <!-- Big ▶ (rotated 90° from ▲) -->
    <polygon points="-16,-14 -16,14 16,0" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  </g>
  <text fill="currentColor" x="360" y="100" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(원점, 방향 변화)</text>

  <!-- Arrow ③ Translate -->
  <line x1="400" y1="58" x2="478" y2="58" stroke="currentColor" stroke-width="1" stroke-dasharray="4,3" opacity="0.4" marker-end="url(#trsArw)"/>
  <text fill="currentColor" x="439" y="48" text-anchor="middle" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.7">③ Translate</text>

  <!-- ===== State 3: Translate 후 (큰 ▶ 이동) ===== -->
  <g transform="translate(530, 58)">
    <!-- Faded crosshair at original origin -->
    <line x1="-7" y1="0" x2="7" y2="0" stroke="currentColor" stroke-width="0.8" opacity="0.15"/>
    <line x1="0" y1="-7" x2="0" y2="7" stroke="currentColor" stroke-width="0.8" opacity="0.15"/>
    <!-- Displacement arrow from origin to final position -->
    <line x1="5" y1="0" x2="38" y2="0" stroke="currentColor" stroke-width="1" stroke-dasharray="3,2" opacity="0.25"/>
    <!-- Big ▶ at final position -->
    <g transform="translate(55, 0)">
      <polygon points="-16,-14 -16,14 16,0" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
    </g>
  </g>
  <text fill="currentColor" x="570" y="100" text-anchor="middle" font-size="9" font-family="sans-serif" opacity="0.5">(최종 위치에 배치)</text>

  <!-- Bottom caption -->
  <text fill="currentColor" x="350" y="138" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">원점에서 형태(S)와 방향(R)을 먼저 잡은 뒤, 마지막에 위치(T)를 지정</text>
</svg>
</div>

<br>

Unity의 Transform 컴포넌트는 position, rotation, localScale을 내부적으로 이 TRS 순서로 합성하여 `localToWorldMatrix`를 만듭니다.

---

## Unity의 Transform과 행렬

Unity에서 모든 게임 오브젝트는 Transform 컴포넌트를 가집니다.

Transform은 오브젝트의 위치(position), 회전(rotation), 크기(localScale)를 저장하고, 이 세 값을 내부적으로 4x4 행렬로 합성하여 좌표 변환에 사용합니다.

<br>

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <!-- Card background -->
  <rect x="8" y="8" width="504" height="324" rx="6" fill="currentColor" fill-opacity="0.03" stroke="currentColor" stroke-width="1" stroke-opacity="0.15"/>

  <!-- Title -->
  <text fill="currentColor" x="260" y="34" text-anchor="middle" font-size="15" font-weight="bold" font-family="sans-serif">Transform</text>

  <!-- ===== 위치 ===== -->
  <rect x="18" y="48" width="484" height="18" rx="3" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="28" y="61" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.5">위치</text>

  <text fill="currentColor" x="28" y="80" font-size="11" font-weight="bold" font-family="sans-serif">position</text>
  <text fill="currentColor" x="230" y="80" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Vector3</text>
  <text fill="currentColor" x="340" y="80" font-size="10" font-family="sans-serif" opacity="0.55">월드 공간 위치</text>

  <text fill="currentColor" x="28" y="100" font-size="11" font-weight="bold" font-family="sans-serif">localPosition</text>
  <text fill="currentColor" x="230" y="100" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Vector3</text>
  <text fill="currentColor" x="340" y="100" font-size="10" font-family="sans-serif" opacity="0.55">부모 기준 로컬 위치</text>

  <!-- ===== 회전 ===== -->
  <rect x="18" y="112" width="484" height="18" rx="3" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="28" y="125" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.5">회전</text>

  <text fill="currentColor" x="28" y="144" font-size="11" font-weight="bold" font-family="sans-serif">rotation</text>
  <text fill="currentColor" x="230" y="144" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Quaternion</text>
  <text fill="currentColor" x="340" y="144" font-size="10" font-family="sans-serif" opacity="0.55">월드 공간 회전</text>

  <text fill="currentColor" x="28" y="164" font-size="11" font-weight="bold" font-family="sans-serif">localRotation</text>
  <text fill="currentColor" x="230" y="164" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Quaternion</text>
  <text fill="currentColor" x="340" y="164" font-size="10" font-family="sans-serif" opacity="0.55">부모 기준 로컬 회전</text>

  <text fill="currentColor" x="28" y="184" font-size="11" font-weight="bold" font-family="sans-serif">eulerAngles</text>
  <text fill="currentColor" x="230" y="184" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Vector3</text>
  <text fill="currentColor" x="340" y="184" font-size="10" font-family="sans-serif" opacity="0.55">오일러 각 (읽기/쓰기용)</text>

  <!-- ===== 스케일 ===== -->
  <rect x="18" y="196" width="484" height="18" rx="3" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="28" y="209" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.5">스케일</text>

  <text fill="currentColor" x="28" y="228" font-size="11" font-weight="bold" font-family="sans-serif">localScale</text>
  <text fill="currentColor" x="230" y="228" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Vector3</text>
  <text fill="currentColor" x="340" y="228" font-size="10" font-family="sans-serif" opacity="0.55">부모 기준 스케일</text>

  <text fill="currentColor" x="28" y="248" font-size="11" font-weight="bold" font-family="sans-serif">lossyScale</text>
  <text fill="currentColor" x="230" y="248" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Vector3</text>
  <text fill="currentColor" x="340" y="248" font-size="10" font-family="sans-serif" opacity="0.55">월드 공간 스케일 (읽기 전용)</text>

  <!-- ===== 변환 행렬 ===== -->
  <rect x="18" y="260" width="484" height="18" rx="3" fill="currentColor" fill-opacity="0.06"/>
  <text fill="currentColor" x="28" y="273" font-size="10" font-weight="bold" font-family="sans-serif" opacity="0.5">변환 행렬</text>

  <text fill="currentColor" x="28" y="292" font-size="11" font-weight="bold" font-family="sans-serif">localToWorldMatrix</text>
  <text fill="currentColor" x="230" y="292" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Matrix4x4</text>
  <text fill="currentColor" x="340" y="292" font-size="10" font-family="sans-serif" opacity="0.55">로컬 → 월드 변환 행렬</text>

  <text fill="currentColor" x="28" y="312" font-size="11" font-weight="bold" font-family="sans-serif">worldToLocalMatrix</text>
  <text fill="currentColor" x="230" y="312" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.45">Matrix4x4</text>
  <text fill="currentColor" x="340" y="312" font-size="10" font-family="sans-serif" opacity="0.55">월드 → 로컬 변환 행렬</text>
</svg>
</div>

### localToWorldMatrix

`localToWorldMatrix`는 오브젝트의 **로컬 공간 좌표를 월드 공간 좌표로 변환**하는 4x4 행렬입니다.

부모가 없는 루트 오브젝트의 경우, position, rotation, localScale을 TRS 순서로 합성한 결과와 같습니다. (부모가 있는 경우는 [부모-자식 관계와 행렬 계층](#부모-자식-관계와-행렬-계층)에서 다룹니다.)

$$
\text{localToWorldMatrix} = T \times R \times S
$$

$T$ = 이동 행렬 (position 기반), $R$ = 회전 행렬 (rotation 기반), $S$ = 스케일 행렬 (localScale 기반)

<br>

메쉬의 정점은 로컬 공간에 정의되어 있으므로, localToWorldMatrix를 곱해야 월드 공간 좌표가 됩니다.

예를 들어 캐릭터 모델의 코 끝이 로컬 좌표 (0, 1.7, 0.1)일 때, 이 정점을 동차 좌표 (0, 1.7, 0.1, 1)로 표현한 뒤 localToWorldMatrix를 곱하면 월드 좌표를 얻습니다. (w = 1은 위치를 뜻하며, 이동 변환이 적용되도록 합니다.)

```
로컬 좌표 → 월드 좌표 변환

캐릭터의 Transform:
  position   = (10, 0, 5)
  rotation   = Y축 90도
  localScale = (1, 1, 1)

로컬 좌표:  (0, 1.7, 0.1)

월드 좌표 = localToWorldMatrix × (0, 1.7, 0.1, 1)

→ 스케일 적용:   (0, 1.7, 0.1)     (스케일 1이므로 변화 없음)
→ Y축 90도 회전: (0.1, 1.7, 0)     (x'=z, z'=-x 이므로 x'=0.1, z'=0)
→ 이동 적용:     (10.1, 1.7, 5.0)  (position 더함)
```

<br>

지금까지 다룬 로컬 → 월드 변환은, GPU가 정점을 화면에 그리기까지 거치는 여러 좌표 변환 중 첫 번째입니다.

GPU는 화면에 그리기 전에 **클리핑(Clipping)**이라는 단계를 거칩니다. GPU는 메쉬를 삼각형 단위로 처리하는데, 프러스텀 컬링이 오브젝트 전체를 대상으로 "화면에 보이는가"를 판정하는 CPU 단계라면, 클리핑은 이 삼각형 하나하나가 화면 안에 있는지를 검사하는 GPU 단계입니다.

화면 경계에 걸쳐 있는 삼각형은 경계선에서 잘라 보이는 부분만 남기고, 완전히 밖에 있는 삼각형은 폐기합니다. **클립 공간(Clip Space)**은 이 클리핑 판정이 이루어지는 좌표 공간입니다.

버텍스 셰이더가 로컬 공간에서 클립 공간까지의 변환을 한 번에 수행하며, Unity 셰이더에서는 `UnityObjectToClipPos(v.vertex)` 함수가 이를 담당합니다.

<br>

내부적으로는 세 단계의 행렬이 순서대로 정점에 적용됩니다.

먼저 Model 행렬이 로컬 공간을 월드 공간으로, 다음으로 View 행렬이 월드 공간을 카메라 기준 좌표로, 마지막으로 Projection 행렬이 카메라 좌표를 클립 공간으로 변환합니다.

이 중 Model 행렬이 바로 localToWorldMatrix이며, 나머지 View 행렬과 Projection 행렬을 포함한 전체 좌표 공간 전환 과정은 [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)에서 이어집니다.

### worldToLocalMatrix

`worldToLocalMatrix`는 localToWorldMatrix의 **역행렬(Inverse Matrix)**으로, 월드 공간의 좌표를 오브젝트의 로컬 공간 좌표로 변환합니다.

역행렬은 원래 변환을 되돌리는 행렬입니다. 이동 (10, 0, 5)의 역행렬은 이동 (-10, 0, -5)이고, 90도 회전의 역행렬은 -90도 회전이며, 스케일 2의 역행렬은 스케일 0.5입니다.

행렬 $A$에 역행렬 $A^{-1}$을 곱하면 단위 행렬(Identity Matrix), 즉 아무 변환도 하지 않는 행렬이 됩니다.

$$
\text{worldToLocalMatrix} = \text{localToWorldMatrix}^{-1}
$$

<br>

앞의 예시에서 사용한 캐릭터(position = (10, 0, 5), rotation = Y축 90도, localScale = (1, 1, 1))를 그대로 사용하면, 

월드 좌표 $(15, \; 3, \; 8)$에 있는 점을 이 캐릭터의 로컬 공간 좌표로 변환할 수 있습니다.

$$
\text{로컬 좌표} = \text{worldToLocalMatrix} \times \begin{bmatrix} 15 \\ 3 \\ 8 \\ 1 \end{bmatrix}
$$

worldToLocalMatrix는 월드 공간의 데이터를 오브젝트 기준으로 해석할 때 사용됩니다.

예를 들어 적이 플레이어의 앞에 있는지 뒤에 있는지 알고 싶을 때, 월드 좌표는 월드 축 기준이라 적의 좌표만 봐서는 플레이어 기준의 앞/뒤가 바로 드러나지 않습니다.

이때 적의 월드 좌표를 플레이어의 worldToLocalMatrix로 변환하면, 플레이어의 로컬 공간에서 +z는 항상 정면, +x는 항상 오른쪽이므로 변환된 좌표의 z 부호만으로 앞/뒤, x 부호만으로 좌/우를 바로 판단할 수 있습니다.

### 부모-자식 관계와 행렬 계층

Unity에서 오브젝트가 부모-자식 관계(hierarchy)를 가지면, 자식의 로컬 TRS 행렬은 부모를 기준으로 한 상대적 변환이므로, 자식의 월드 좌표를 구하려면 부모의 localToWorldMatrix까지 곱해야 합니다.

즉, 자식의 localToWorldMatrix는 부모의 localToWorldMatrix에 자신의 로컬 TRS 행렬을 곱한 결과입니다.

```
부모-자식 행렬 계층

자식의 월드 행렬 = 부모의 월드 행렬 × 자식의 로컬 행렬

예: 탱크의 포탑
  탱크 (부모): position (100, 0, 50), rotation Y축 30도
  포탑 (자식): localPosition (0, 2, 0), localRotation Y축 15도

  포탑의 월드 행렬
    = 탱크의 localToWorldMatrix × 포탑의 로컬 TRS 행렬

  → 포탑은 탱크의 위에 위치하면서
     탱크의 방향(30도) + 자신의 추가 회전(15도) = 45도를 바라봄
    (같은 축 회전이라 각도가 단순 덧셈됨)
```

<br>

자식의 월드 행렬은 부모의 월드 행렬에 자신의 로컬 TRS 행렬을 곱한 결과이므로, 부모를 움직이면 자식도 함께 움직입니다. 

캐릭터의 손에 무기를 붙이거나 차량의 바퀴를 차체에 연결할 수 있는 것도 이 행렬 계층 덕분입니다.

<br>

계층이 깊어지면 최종 월드 행렬을 구하기 위해 곱해야 하는 행렬의 수가 늘어납니다.

Unity에서 Transform의 position이나 rotation을 변경하면, 해당 오브젝트의 변환 행렬이 즉시 재계산되고, 모든 자식의 월드 행렬도 재귀적으로 다시 계산됩니다.

정적인 오브젝트는 변경이 발생하지 않으므로 재계산 비용이 없지만, 부모의 Transform을 매 프레임 변경하면 그 아래 모든 자식의 월드 행렬이 매 프레임 다시 계산됩니다.

계층이 깊고 자식이 많은 구조에서 부모가 매 프레임 변하면 CPU 부하가 커지므로, 자주 움직이는 오브젝트는 계층을 얕게 유지하거나 불필요한 중간 노드를 줄이는 것이 좋습니다.

Transform 변경 전파의 구체적인 비용 구조와 최적화 방법은 [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)에서 확인할 수 있습니다.

---

## 마무리

벡터가 위치와 방향을 표현한다면, 행렬은 이동·회전·스케일을 하나의 곱셈 연산으로 통일하는 변환 도구입니다.

<br>

- 3x3 행렬은 원점을 움직일 수 없으므로 이동을 표현하지 못합니다. 동차 좌표 (x, y, z, w)를 도입하여 4x4 행렬로 확장하면, 이동·회전·스케일을 하나의 행렬-벡터 곱셈으로 처리할 수 있습니다.
- w = 1은 위치(이동 적용), w = 0은 방향(이동 무시)으로 구분됩니다.
- 이동은 4x4 행렬의 네 번째 열에, 회전은 왼쪽 위 3x3 영역에 cos/sin 값으로, 스케일은 대각 성분에 배치됩니다.
- 행렬 곱셈은 비교환적이므로 적용 순서가 결과를 바꿉니다. 3D 그래픽스에서는 Scale → Rotate → Translate 순서(TRS)로 적용하여, 원점에서 형태와 방향을 잡은 뒤 최종 위치로 옮깁니다.
- 오일러 각은 짐벌 락이 발생할 수 있으므로, Unity는 내부적으로 쿼터니언을 사용합니다.
- 비균일 스케일은 법선 왜곡, 물리 충돌 부정확, 전단 현상을 일으킵니다. 모바일에서는 역전치 행렬 계산의 성능 부담이 크므로, 균일 스케일을 우선 사용합니다.
- Unity Transform의 localToWorldMatrix는 position, rotation, localScale을 TRS 순서로 합성한 4x4 행렬이며, 버텍스 셰이더의 Model 행렬로 사용됩니다.
- 부모-자식 관계에서 자식의 월드 행렬은 부모의 월드 행렬에 자식의 로컬 TRS 행렬을 곱한 결과입니다. 부모를 움직이면 자식도 함께 움직이며, 계층이 깊고 자주 변하면 CPU 부하가 커집니다.

여기서 다룬 TRS 합성은 오브젝트의 로컬 공간을 월드 공간으로 옮기는 첫 번째 단계입니다.

정점은 월드 공간 이후에도 카메라 공간, 클립 공간 등 여러 좌표 공간을 거치며, 각 단계마다 서로 다른 변환 행렬이 적용됩니다. [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)에서 이 좌표 공간 전환의 전체 과정을 이어갑니다.

---

**관련 글**
- [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)

**시리즈**
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- **그래픽스 수학 (2) - 행렬과 변환 (현재 글)**
- [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)
- [그래픽스 수학 (4) - 투영](/dev/unity/GraphicsMath-4/)

**전체 시리즈**
- [하드웨어 기초 (1) - CPU 아키텍처와 파이프라인](/dev/unity/HardwareBasics-1/)
- [하드웨어 기초 (2) - 메모리 계층 구조](/dev/unity/HardwareBasics-2/)
- [하드웨어 기초 (3) - GPU의 탄생과 발전](/dev/unity/HardwareBasics-3/)
- [하드웨어 기초 (4) - 모바일 SoC](/dev/unity/HardwareBasics-4/)
- [그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)
- **그래픽스 수학 (2) - 행렬과 변환** (현재 글)
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
