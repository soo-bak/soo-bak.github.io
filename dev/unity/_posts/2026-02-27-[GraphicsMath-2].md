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

[그래픽스 수학 (1) - 벡터와 벡터 연산](/dev/unity/GraphicsMath-1/)에서는 벡터로 위치, 방향, 이동량을 표현하는 방법을 다루었습니다.

위치는 오브젝트가 어디에 있는지를 나타내고, 방향은 어느 쪽을 향하는지를 나타냅니다. 이동량은 한 프레임이나 일정 시간 동안 얼마나 움직일지를 나타냅니다.

게임에서는 이 값들이 계속 바뀝니다. 캐릭터는 앞으로 이동하고, 문은 회전하며 열리고, 아이템은 크기가 달라질 수 있습니다. 이렇게 위치, 방향, 크기를 바꾸는 계산을 **변환(Transformation)**이라고 합니다.

변환은 보통 세 가지로 나누어 다룹니다. 위치를 바꾸는 변환은 **이동(Translation)**, 방향을 바꾸는 변환은 **회전(Rotation)**, 크기를 바꾸는 변환은 **스케일(Scale)**입니다.

각 변환은 따로 계산할 수 있습니다. 이동은 위치에 이동량을 더하고, 스케일은 각 성분에 배율을 곱합니다. 회전은 축과 각도에 따라 좌표를 다시 계산합니다.

하지만 실제 렌더링에서는 한 정점에 이동, 회전, 스케일이 함께 적용되는 경우가 많습니다. 세 변환을 따로 처리하면 적용 순서를 매번 관리해야 하고, 정점마다 여러 종류의 계산을 차례대로 수행해야 합니다.

이 세 변환을 하나의 곱셈 형태로 묶기 위해 사용하는 도구가 **행렬(Matrix)**입니다. 행렬 하나에 이동, 회전, 스케일을 담아 두면, 정점마다 같은 형태의 행렬-벡터 곱셈으로 변환을 적용할 수 있습니다.

이 글에서는 행렬이 벡터를 어떻게 바꾸는지, 3D 그래픽스에서 왜 4×4 행렬을 사용하는지, 이동·회전·스케일이 행렬로 어떻게 표현되는지, 그리고 Unity의 `Transform` 값이 행렬과 어떻게 연결되는지 다룹니다.

---

## 행렬이란

행렬은 숫자를 행과 열에 맞춰 배치한 값입니다. 가로 줄을 **행(row)**, 세로 줄을 **열(column)**이라고 하며, 행이 m개이고 열이 n개이면 m x n 행렬이라고 부릅니다.

$$
\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}
$$

위 예시는 2개의 행과 3개의 열을 가진 2 × 3 행렬입니다. 첫 번째 행에는 $(1, \; 2, \; 3)$이 있고, 두 번째 행에는 $(4, \; 5, \; 6)$이 있습니다.

3D 그래픽스에서 행렬은 단순히 숫자를 모아 둔 표가 아니라, 벡터를 다른 벡터로 바꾸는 계산 규칙으로 쓰입니다. 회전 행렬을 곱하면 벡터의 방향이 바뀌고, 스케일 행렬을 곱하면 각 축의 크기가 바뀝니다.

$$
\underbrace{\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix}}_{\text{변환 행렬}} \underbrace{\begin{bmatrix} x \\ y \\ z \end{bmatrix}}_{\text{원래 벡터}} = \underbrace{\begin{bmatrix} x' \\ y' \\ z' \end{bmatrix}}_{\text{변환된 벡터}}
$$

행렬과 벡터를 곱하면 결과 벡터의 각 성분이 하나씩 계산됩니다. 첫 번째 행은 $x'$를 만들고, 두 번째 행은 $y'$를 만들며, 세 번째 행은 $z'$를 만듭니다.

$$
\begin{aligned}
x' &= ax + by + cz \quad \text{(1행} \cdot \text{벡터)} \\
y' &= dx + ey + fz \quad \text{(2행} \cdot \text{벡터)} \\
z' &= gx + hy + iz \quad \text{(3행} \cdot \text{벡터)}
\end{aligned}
$$

각 성분은 행렬의 한 행과 입력 벡터의 **내적(Dot Product)**으로 계산됩니다. 예를 들어 $x' = ax + by + cz$는 원래 x 성분에 a를 곱하고, y 성분에 b를 곱하고, z 성분에 c를 곱한 뒤 모두 더한 값입니다.

회전은 x, y, z 성분을 서로 섞어 방향을 바꾸고, 스케일은 각 성분에 배율을 곱해 크기를 바꿉니다. 이런 계산은 모두 기존 x, y, z 성분을 조합하는 방식이므로 3x3 행렬로 표현할 수 있습니다. 하지만 위치를 일정한 거리만큼 더하는 이동은 성분을 섞는 것만으로는 처리할 수 없습니다.

---

## 왜 4x4 행렬인가 --- 동차 좌표

3x3 행렬은 기존 x, y, z 성분을 서로 섞거나 배율을 바꾸는 데 사용할 수 있습니다. 그래서 회전과 스케일은 3x3 행렬로 표현할 수 있습니다.

하지만 이동은 성격이 다릅니다. 이동은 기존 성분을 섞는 것이 아니라, 좌표에 일정한 값을 더하는 변환입니다. 예를 들어 어떤 점을 x축으로 5만큼 옮기려면 결과 좌표에 `+5`가 들어가야 합니다.

3x3 행렬만으로는 이런 덧셈이 나오지 않습니다. 특히 원점 (0, 0, 0)에 어떤 3x3 행렬을 곱해도 결과는 항상 원점입니다.

$$
\begin{bmatrix} a & b & c \\ d & e & f \\ g & h & i \end{bmatrix} \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}
$$

행렬 안의 값이 무엇이든 0에 어떤 수를 곱해 더하면 다시 0입니다. 그래서 3x3 행렬만 사용하면 원점을 다른 위치로 옮길 수 없습니다.

$$
\mathbf{p'} = R \cdot \mathbf{p} + \mathbf{t}
$$

이동을 처리하려면 위 수식처럼 행렬 곱셈 뒤에 이동량 $\mathbf{t}$를 따로 더해야 합니다. 이 상태에서는 회전과 스케일은 곱셈으로 처리하고, 이동은 덧셈으로 처리하게 됩니다.

이 계산을 하나의 곱셈으로 묶기 위해 좌표에 성분을 하나 더 붙입니다. 3D 좌표 (x, y, z)를 (x, y, z, w)로 확장하고, 행렬도 4x4로 늘립니다. 그러면 새로 생긴 네 번째 열에 이동량을 넣을 수 있습니다.

이렇게 확장한 좌표를 **동차 좌표(Homogeneous Coordinates)**라고 합니다. 여기서 w는 이 좌표가 위치인지 방향인지를 구분하는 데 쓰입니다.

$$
\text{3D 좌표:} \quad (x, \; y, \; z) \qquad \Longrightarrow \qquad \text{동차 좌표:} \quad (x, \; y, \; z, \; w)
$$

$$
\begin{aligned}
\text{위치(점):} \quad & (x, \; y, \; z, \; 1) & & \leftarrow \; \text{이동의 영향을 받음} \\
\text{방향(벡터):} \quad & (x, \; y, \; z, \; 0) & & \leftarrow \; \text{이동의 영향을 받지 않음}
\end{aligned}
$$

위치는 w = 1을 사용합니다. 그러면 네 번째 열에 들어 있는 이동량이 결과에 더해집니다. 방향은 w = 0을 사용합니다. 방향은 공간의 한 점이 아니므로, 오브젝트를 (10, 0, 0)으로 옮겨도 "위를 향한다"는 방향 (0, 1, 0)은 그대로 남아야 하기 때문입니다.

이동, 회전, 스케일을 하나의 4x4 행렬로 표현하면 다음과 같습니다.

$$
\begin{bmatrix} \cdot & \cdot & \cdot & t_x \\ \cdot & \cdot & \cdot & t_y \\ \cdot & \cdot & \cdot & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} x' \\ y' \\ z' \\ 1 \end{bmatrix}
$$

왼쪽 위 3x3 영역에는 회전과 스케일이 들어가고, 네 번째 열에는 이동량 $(t_x, t_y, t_z)$가 들어갑니다. 위치 벡터는 w = 1이므로 이동량이 더해지고, 방향 벡터는 w = 0이므로 이동량이 사라집니다.

GPU가 많은 정점을 처리할 때도 같은 원리를 사용합니다. 각 정점을 동차 좌표 (x, y, z, 1)로 표현하고 같은 4x4 행렬과 곱하면, 오브젝트를 이루는 모든 정점에 같은 이동, 회전, 스케일이 적용됩니다.

---

## 이동 행렬 (Translation)

이동 행렬은 위치에 이동량을 더하는 행렬입니다. x축 이동량은 $t_x$, y축 이동량은 $t_y$, z축 이동량은 $t_z$로 쓰며, 이 세 값은 4x4 행렬의 네 번째 열에 들어갑니다.

$$
T = \begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

위치 벡터는 w = 1을 사용하므로, 이 행렬을 곱하면 네 번째 열에 있는 이동량이 결과 좌표에 더해집니다.

$$
\begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} x + t_x \\ y + t_y \\ z + t_z \\ 1 \end{bmatrix}
$$

첫 번째 성분만 보면 계산이 더 분명합니다. 위치 벡터에서는 w가 1이므로 $1 \cdot x + t_x \cdot 1 = x + t_x$가 됩니다. y와 z도 같은 방식으로 각각 $t_y$, $t_z$가 더해집니다.

반대로 방향 벡터는 w = 0을 사용합니다.

$$
\begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 0 \end{bmatrix} = \begin{bmatrix} x \\ y \\ z \\ 0 \end{bmatrix}
$$

$t_x$, $t_y$, $t_z$에 모두 0이 곱해지므로 이동량은 결과에 더해지지 않습니다. 그래서 같은 이동 행렬을 곱해도 위치는 옮겨지고, 방향은 그대로 유지됩니다.

---

## 회전 행렬 (Rotation)

회전 행렬은 점이나 방향을 특정 축을 중심으로 돌리는 변환입니다. 예를 들어 Y축을 기준으로 회전하면 높이인 Y 값은 그대로 두고, 수평 방향을 나타내는 X와 Z 값만 바뀝니다.

3D 공간의 회전은 기준이 되는 축에 따라 X축 회전, Y축 회전, Z축 회전으로 나누어 볼 수 있습니다. 회전각은 보통 $\theta$(세타)로 표기합니다. 기준 축에 해당하는 성분은 그대로 남고, 나머지 두 성분이 바뀌는 식입니다.

### X축 회전

X축을 기준으로 회전하면 X 성분은 변하지 않습니다. 대신 Y와 Z 성분이 서로 섞이면서, 점이 YZ 평면 위에서 도는 것처럼 바뀝니다.

$$
R_x(\theta) = \begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta & 0 \\ 0 & \sin\theta & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

### Y축 회전

Y축을 기준으로 회전하면 Y 성분은 변하지 않습니다. X와 Z 성분이 바뀌므로, Unity에서 캐릭터가 좌우로 방향을 돌 때 가장 자주 떠올리는 회전에 가깝습니다.

$$
R_y(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta & 0 \\ 0 & 1 & 0 & 0 \\ -\sin\theta & 0 & \cos\theta & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

예를 들어 $\theta = 90°$이면 $\cos 90° = 0$, $\sin 90° = 1$입니다. 정점 (5, 2, 3)에 Y축 90도 회전을 적용하면 다음과 같습니다.

$$
\begin{bmatrix} 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ -1 & 0 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} 5 \\ 2 \\ 3 \\ 1 \end{bmatrix} = \begin{bmatrix} 3 \\ 2 \\ -5 \\ 1 \end{bmatrix}
$$

Y 성분은 2로 그대로 남고, X와 Z 성분만 바뀝니다. 수평면에서 점의 위치가 회전한 것입니다.

### Z축 회전

Z축을 기준으로 회전하면 Z 성분은 변하지 않습니다. X와 Y 성분이 바뀌므로, XY 평면 위에서 도는 회전입니다.

$$
R_z(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 & 0 \\ \sin\theta & \cos\theta & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

세 회전 행렬은 같은 패턴을 가집니다. 회전축 방향의 성분은 축 위에 그대로 남고, 실제 회전은 그 축에 수직인 평면에서 일어납니다. 그래서 X축 회전에서는 Y와 Z가, Y축 회전에서는 X와 Z가, Z축 회전에서는 X와 Y가 바뀝니다.

$\cos\theta$와 $\sin\theta$는 이 2D 평면 안에서 점을 $\theta$만큼 돌릴 때 필요한 값입니다. 3D 회전 행렬은 결국 "한 성분은 그대로 두고, 나머지 두 성분에 2D 회전 공식을 적용한 것"으로 볼 수 있습니다.

### 오일러 각과 짐벌 락

X축, Y축, Z축 회전을 정해진 순서로 적용하면 3D 방향을 세 개의 각도로 표현할 수 있습니다. 이 표현을 **오일러 각(Euler Angles)**이라고 합니다. Unity Transform 인스펙터의 Rotation 항목에 보이는 (x, y, z) 값도 오일러 각입니다.

오일러 각은 읽고 입력하기 쉽지만, 세 축 회전을 순서대로 적용한다는 한계가 있습니다. 특정 각도에서는 두 회전축이 같은 방향으로 겹치고, 서로 다른 두 회전 입력이 같은 회전처럼 작동합니다. 이렇게 독립적으로 조절할 수 있는 회전축이 하나 줄어드는 현상을 **짐벌 락(Gimbal Lock)**이라고 합니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 560 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 560px; width: 100%;">
  <defs>
    <marker id="rotArrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>
  <text x="140" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">일반 상태</text>
  <line x1="140" y1="90" x2="210" y2="90" stroke="currentColor" stroke-width="1.8" marker-end="url(#rotArrow)"/>
  <line x1="140" y1="90" x2="140" y2="35" stroke="currentColor" stroke-width="1.8" marker-end="url(#rotArrow)"/>
  <line x1="140" y1="90" x2="85" y2="130" stroke="currentColor" stroke-width="1.8" marker-end="url(#rotArrow)"/>
  <text x="218" y="94" font-family="sans-serif" font-size="11" fill="currentColor">X</text>
  <text x="146" y="38" font-family="sans-serif" font-size="11" fill="currentColor">Y</text>
  <text x="72" y="138" font-family="sans-serif" font-size="11" fill="currentColor">Z</text>
  <text x="140" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">세 축이 서로 구분됨</text>

  <line x1="265" y1="90" x2="305" y2="90" stroke="currentColor" stroke-width="1.4" marker-end="url(#rotArrow)" opacity="0.55"/>

  <text x="420" y="24" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">짐벌 락</text>
  <line x1="420" y1="90" x2="490" y2="90" stroke="currentColor" stroke-width="1.8" marker-end="url(#rotArrow)"/>
  <line x1="420" y1="90" x2="420" y2="35" stroke="currentColor" stroke-width="1.8" marker-end="url(#rotArrow)"/>
  <line x1="420" y1="94" x2="490" y2="94" stroke="currentColor" stroke-width="1.8" stroke-dasharray="5,4" marker-end="url(#rotArrow)"/>
  <text x="498" y="94" font-family="sans-serif" font-size="11" fill="currentColor">X/Z</text>
  <text x="426" y="38" font-family="sans-serif" font-size="11" fill="currentColor">Y</text>
  <text x="420" y="160" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">두 축이 겹쳐 자유도 감소</text>
</svg>
</div>

오일러 각은 회전을 한 번에 처리하지 않고, 정해진 순서대로 축 회전을 차례로 적용합니다. 이 과정에서 앞 단계의 회전은 뒤에서 사용할 회전축의 방향도 함께 바꿉니다. 어떤 축이 90도 가까이 돌아가면 원래 서로 달랐던 두 회전축이 나란해질 수 있고, 그 순간 두 입력이 같은 축을 돌리는 것처럼 작동합니다.

Unity는 이런 한계를 피하기 위해 회전을 내부적으로 **쿼터니언(Quaternion)**으로 저장합니다. 쿼터니언은 4개의 성분 (x, y, z, w)으로 3D 회전을 표현하며, 오일러 각처럼 특정 축 순서에 묶이지 않습니다. 인스펙터에는 사람이 읽기 쉬운 오일러 각을 보여 주지만, `transform.rotation`의 실제 타입은 쿼터니언입니다.

## 스케일 행렬 (Scale)

스케일은 좌표 성분에 배율을 곱해 오브젝트의 크기를 바꾸는 변환입니다. x축으로 2배 늘리고 싶다면 x 성분에 2를 곱하고, y축 크기를 그대로 두고 싶다면 y 성분에 1을 곱합니다.

스케일 행렬에서는 각 축의 배율 $(s_x, \; s_y, \; s_z)$이 대각선에 들어갑니다.

$$
S = \begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

이 행렬을 위치 벡터 (x, y, z, 1)에 곱하면 x에는 $s_x$, y에는 $s_y$, z에는 $s_z$가 각각 곱해집니다.

$$
\begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \\ 1 \end{bmatrix} = \begin{bmatrix} s_x \cdot x \\ s_y \cdot y \\ s_z \cdot z \\ 1 \end{bmatrix}
$$

$s_x = s_y = s_z = 2$이면 모든 축에 같은 배율이 적용되므로 오브젝트 전체가 2배 커집니다. 이렇게 모든 축에 같은 배율을 적용하는 경우를 **균일 스케일(Uniform Scale)**이라고 합니다.

### 비균일 스케일과 부작용

**비균일 스케일(Non-uniform Scale)**은 축마다 다른 배율을 적용하는 스케일입니다. (2, 1, 1)을 적용하면 X축 방향으로만 2배 늘어나고, Y와 Z 방향의 크기는 그대로 유지됩니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg" style="max-width: 520px; width: 100%;">
  <text fill="currentColor" x="130" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">균일 스케일 (2, 2, 2)</text>
  <text fill="currentColor" x="130" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">모든 방향으로 동일하게 확대</text>
  <rect x="55" y="65" width="40" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <line x1="110" y1="85" x2="140" y2="85" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="142,85 136,81 136,89" fill="currentColor" opacity="0.4"/>
  <rect x="155" y="45" width="80" height="80" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <text fill="currentColor" x="400" y="20" text-anchor="middle" font-size="13" font-weight="bold" font-family="sans-serif">비균일 스케일 (2, 1, 1)</text>
  <text fill="currentColor" x="400" y="36" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.6">X축만 늘어남</text>
  <rect x="315" y="65" width="40" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <line x1="370" y1="85" x2="400" y2="85" stroke="currentColor" stroke-width="1.2" opacity="0.4"/>
  <polygon points="402,85 396,81 396,89" fill="currentColor" opacity="0.4"/>
  <rect x="415" y="65" width="80" height="40" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.5" rx="2"/>
  <text fill="currentColor" x="130" y="155" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">비율이 유지됨</text>
  <text fill="currentColor" x="400" y="155" text-anchor="middle" font-size="10" font-family="sans-serif" opacity="0.5">비율이 왜곡됨</text>
</svg>
</div>

비균일 스케일은 간단히 형태를 바꿀 수 있어 편리하지만, 렌더링과 물리 계산에서는 주의가 필요합니다. 축마다 다른 배율을 적용하면 표면이 바라보는 방향이 달라지고, 콜라이더가 보이는 모양과 다르게 동작할 수 있으며, 부모 아래에 있는 자식 오브젝트의 회전도 예상과 다르게 보일 수 있습니다.

가장 먼저 문제가 되는 것은 법선 벡터입니다. 정점은 공간상의 위치이므로 스케일을 적용하면 좌표가 늘어나거나 줄어드는 것이 맞습니다. 하지만 법선은 위치가 아니라 표면에 수직인 방향입니다. 변환 뒤에도 법선은 바뀐 표면에 계속 수직이어야 합니다.

균일 스케일처럼 모든 축이 같은 비율로 늘어나면 표면과 법선의 관계가 크게 달라지지 않습니다. 반면 비균일 스케일은 축마다 다른 비율을 적용하므로, 정점에 사용한 행렬을 법선에 그대로 곱하면 법선이 새 표면에 수직이 아닌 방향을 가리킬 수 있습니다.

법선을 올바르게 바꾸려면 한 가지 조건을 지켜야 합니다. 변환 전의 법선이 표면 위의 방향과 수직이었다면, 변환 후의 법선도 변환된 표면 위의 방향과 수직이어야 합니다. 정점에 쓰는 행렬을 그대로 법선에 곱하면 이 조건이 깨질 수 있습니다.

그래서 법선에는 정점 변환 행렬을 그대로 쓰지 않고, 그 행렬을 법선용으로 바꾼 행렬을 사용합니다. 일반적으로 변환 행렬의 역행렬을 구한 뒤 행과 열을 바꾼 **역전치 행렬(Inverse Transpose)**을 법선에 곱합니다. 역행렬은 정점 변환으로 기울어진 축의 영향을 되돌리고, 전치는 그 결과를 법선 방향 계산에 맞는 형태로 바꿉니다. 이 과정을 거치면 법선이 다시 표면에 수직인 방향을 가리키므로 조명 계산이 올바르게 동작합니다.

이 보정은 렌더링 결과를 정확하게 만들지만, 셰이더에서 처리해야 할 계산도 늘립니다.

물리 콜라이더도 시각적 모양과 다르게 동작할 수 있습니다. 예를 들어 구(Sphere) 콜라이더에 비균일 스케일을 적용하면 화면에서는 타원처럼 보일 수 있지만, Unity의 `SphereCollider`는 타원 콜라이더를 직접 지원하지 않습니다. 이 경우 보이는 메쉬와 실제 충돌 판정에 쓰이는 형상이 어긋날 수 있습니다.

계층 구조에서도 문제가 생길 수 있습니다. 부모 오브젝트가 X축으로만 길게 늘어난 상태라면, 자식 오브젝트의 좌표축도 부모의 변환을 기준으로 해석됩니다. 이 상태에서 자식을 회전시키면, 회전된 축에 부모의 비균일 스케일이 다시 섞이면서 모양이 한쪽으로 밀린 것처럼 보일 수 있습니다.

이런 변형을 **전단(Shearing)**이라고 합니다. 전단은 직사각형이 평행사변형처럼 기울어지는 변형입니다. 오브젝트를 단순히 늘리거나 돌린 것과 달리, 축 사이의 직각이 유지되지 않는다는 점이 문제입니다.

따라서 자주 움직이거나 많이 그려지는 오브젝트에는 균일 스케일을 우선 사용하는 편이 안전합니다. 형태 자체를 바꿔야 한다면 Transform의 비균일 스케일에 의존하기보다, 모델링 단계나 메쉬 데이터에서 원하는 비율을 반영하는 쪽이 관리하기 쉽습니다.

## 변환의 합성 --- 행렬 곱셈

이동, 회전, 스케일은 각각 따로 설명했지만, 화면에 오브젝트를 그릴 때는 세 변환이 함께 적용됩니다. 캐릭터를 예로 들면, 먼저 크기가 정해지고, 어느 방향을 바라볼지 정해진 뒤, 월드의 어느 위치에 놓일지가 함께 결정되어야 합니다.

각 변환을 매번 따로 적용할 수도 있지만, 그래픽스에서는 보통 세 행렬을 먼저 곱해 하나의 행렬로 묶습니다. 이렇게 만들어진 최종 행렬을 보통 $M$으로 표기합니다.

$$
M = \underbrace{\begin{bmatrix} 1 & 0 & 0 & t_x \\ 0 & 1 & 0 & t_y \\ 0 & 0 & 1 & t_z \\ 0 & 0 & 0 & 1 \end{bmatrix}}_{T} \times \underbrace{\begin{bmatrix} \cdot & \cdot & \cdot & 0 \\ \cdot & \cdot & \cdot & 0 \\ \cdot & \cdot & \cdot & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}}_{R} \times \underbrace{\begin{bmatrix} s_x & 0 & 0 & 0 \\ 0 & s_y & 0 & 0 \\ 0 & 0 & s_z & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}}_{S}
$$

여기서 $T$는 이동, $R$은 회전, $S$는 스케일 행렬입니다. 세 행렬을 곱해 둔 뒤에는 정점마다 $T$, $R$, $S$를 따로 곱할 필요가 없습니다. 각 정점에 최종 행렬 $M$만 곱하면 같은 변환이 한 번에 적용됩니다.

이 방식의 장점은 계산 형태가 일정하다는 데 있습니다. 오브젝트마다 위치, 회전, 크기는 달라도 렌더링 단계에서는 모두 "정점에 4x4 행렬을 곱한다"는 같은 형태로 처리할 수 있습니다. 다만 행렬 곱셈은 숫자 곱셈과 달리 순서를 바꾸면 결과가 달라지므로, 어떤 순서로 합성하는지가 중요합니다.

### 행렬 곱셈의 비교환성

숫자 곱셈에서는 $3 \times 5 = 5 \times 3$이지만, 행렬 곱셈에서는 $A \times B \neq B \times A$입니다.

**곱하는 순서가 바뀌면 결과도 달라집니다.**

오브젝트가 원점 (0, 0, 0)에 있을 때, 앞서 본 Y축 회전 행렬($\theta = +90°$)과 (5, 0, 0) 이동을 어떤 순서로 적용하느냐에 따라 결과가 완전히 달라집니다. $R_y(+90°)$는 +X 방향을 -Z 방향으로 회전시키는 행렬입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 340" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">행렬 곱셈의 비교환성 — 이동 후 회전 vs 회전 후 이동</text>
  <text x="310" y="38" text-anchor="middle" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">오브젝트 초기 위치: 원점 · 회전: Ry(+90°) — +X를 -Z로 회전</text>
  <line x1="40" y1="56" x2="580" y2="56" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="84" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">이동 후 회전</text>
  <text x="60" y="106" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">1) 오브젝트를 (5, 0, 0)으로 이동</text>
  <text x="60" y="124" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">2) 원점 기준 Ry(+90°) 적용 → +X 방향이 -Z 방향으로 회전</text>
  <text x="60" y="148" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 오브젝트는 (0, 0, -5) 위치에 놓임</text>
  <line x1="40" y1="172" x2="580" y2="172" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="200" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">회전 후 이동</text>
  <text x="60" y="222" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">1) 원점 기준 Ry(+90°) 적용 (원점이므로 위치 변화 없음)</text>
  <text x="60" y="240" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.85">2) (5, 0, 0)으로 이동</text>
  <text x="60" y="264" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">→ 오브젝트는 (5, 0, 0) 위치에 놓임</text>
  <line x1="40" y1="288" x2="580" y2="288" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="310" y="316" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">같은 변환이라도 적용 순서에 따라 결과가 전혀 다름</text>
</svg>
</div>

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

행렬 곱셈은 순서가 바뀌면 결과도 바뀝니다. 그래서 오브젝트 변환을 합성할 때는 어떤 변환을 먼저 적용할지 정해야 합니다.

일반적인 오브젝트 변환에서는 **Scale → Rotate → Translate** 순서로 적용합니다. 먼저 오브젝트의 로컬 공간에서 크기를 정하고, 그 결과를 회전시켜 방향을 맞춘 뒤, 마지막에 월드 공간의 위치로 옮깁니다.

이 순서가 자연스러운 이유는 스케일과 회전이 오브젝트 자신의 원점을 기준으로 적용되어야 하기 때문입니다. 이동을 먼저 적용하면 오브젝트가 원점에서 떨어진 상태가 되고, 그 뒤의 회전은 제자리 회전이 아니라 원점을 중심으로 도는 회전처럼 보일 수 있습니다.

이 적용 순서를 행렬로 합성하면 $M = T \times R \times S$로 씁니다. 이름은 왼쪽부터 보이는 행렬의 순서 때문에 **TRS**라고 부르지만, 실제로 벡터에 적용되는 순서는 오른쪽부터입니다. 벡터 $\mathbf{v}$에 가장 가까운 $S$가 먼저 적용되고, 그 결과에 $R$, 마지막으로 $T$가 적용됩니다.

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

Unity에서도 같은 방식으로 오브젝트 변환을 다룹니다. Transform에 저장된 `position`, `rotation`, `localScale` 값은 렌더링에 사용되기 전에 하나의 4x4 행렬로 묶이며, 그 결과가 `localToWorldMatrix`입니다.

---

## Unity의 Transform과 행렬

Unity에서 Transform 컴포넌트의 `position`, `rotation`, `localScale`은 오브젝트를 배치하기 위한 입력값입니다. 렌더링이나 좌표 변환이 실제로 수행될 때는 이 값들이 4x4 행렬로 바뀌어 사용됩니다.

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

메쉬 정점은 오브젝트 안에서의 위치로 저장됩니다. 캐릭터 모델의 코 끝이 `(0, 1.7, 0.1)`에 있다는 말은 월드의 절대 위치가 아니라, 캐릭터 자신의 원점을 기준으로 그만큼 떨어져 있다는 뜻입니다.

이 로컬 좌표를 월드 공간의 좌표로 바꾸려면 오브젝트의 Transform이 반영되어야 합니다. Unity에서 이 변환을 담고 있는 4x4 행렬이 `localToWorldMatrix`입니다.

부모가 없는 오브젝트라면 `localToWorldMatrix`는 `position`, `rotation`, `localScale`을 TRS 순서로 합성한 행렬입니다.

$$
\text{localToWorldMatrix} = T \times R \times S
$$

$T$ = 이동 행렬 (position 기반), $R$ = 회전 행렬 (rotation 기반), $S$ = 스케일 행렬 (localScale 기반)

부모가 있는 경우에는 부모의 변환까지 함께 반영됩니다. 이 내용은 뒤의 [부모-자식 관계와 행렬 계층](#부모-자식-관계와-행렬-계층)에서 다룹니다.

정점에 이 행렬을 곱할 때는 동차 좌표를 사용합니다. 정점은 위치이므로 w = 1을 붙여 `(x, y, z, 1)`로 만들고, 여기에 `localToWorldMatrix`를 곱합니다. 그러면 스케일, 회전, 이동이 순서대로 반영된 월드 좌표를 얻을 수 있습니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">로컬 좌표 → 월드 좌표 변환</text>
  <text x="40" y="48" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">캐릭터의 Transform</text>
  <text x="60" y="68" font-family="monospace" font-size="11" fill="currentColor">position   = (10, 0, 5)</text>
  <text x="60" y="86" font-family="monospace" font-size="11" fill="currentColor">rotation   = Y축 90도</text>
  <text x="60" y="104" font-family="monospace" font-size="11" fill="currentColor">localScale = (1, 1, 1)</text>
  <text x="40" y="138" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">로컬 좌표</tspan>: (0, 1.7, 0.1)</text>
  <text x="40" y="166" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">월드 좌표</tspan> = localToWorldMatrix × (0, 1.7, 0.1, 1)</text>
  <line x1="40" y1="186" x2="580" y2="186" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="212" font-family="sans-serif" font-size="11" fill="currentColor">→ 스케일 적용</text>
  <text x="200" y="212" font-family="monospace" font-size="11" fill="currentColor">(0, 1.7, 0.1)</text>
  <text x="340" y="212" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">스케일 1이므로 변화 없음</text>
  <text x="40" y="236" font-family="sans-serif" font-size="11" fill="currentColor">→ Y축 90도 회전</text>
  <text x="200" y="236" font-family="monospace" font-size="11" fill="currentColor">(0.1, 1.7, 0)</text>
  <text x="340" y="236" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">x'=z, z'=-x 이므로 x'=0.1, z'=0</text>
  <text x="40" y="260" font-family="sans-serif" font-size="11" fill="currentColor">→ 이동 적용</text>
  <text x="200" y="260" font-family="monospace" font-size="11" font-weight="bold" fill="currentColor">(10.1, 1.7, 5.0)</text>
  <text x="340" y="260" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">position 더함</text>
</svg>
</div>

`localToWorldMatrix`는 렌더링 파이프라인에서 **Model 행렬**에 해당합니다. Model 행렬은 메쉬의 로컬 좌표를 월드 좌표로 옮기는 첫 번째 변환입니다.

정점이 화면에 그려지려면 여기서 끝나지 않습니다. 월드 좌표는 다시 카메라 기준 좌표로 바뀌고, 마지막에는 화면에 보이는 범위를 판정하기 위한 좌표로 변환됩니다. 이 흐름은 보통 Model, View, Projection 행렬로 설명합니다.

이 글에서는 그중 Model 행렬, 즉 `localToWorldMatrix`까지만 다룹니다. View 행렬과 Projection 행렬을 포함한 전체 좌표 공간 전환 과정은 [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)에서 이어집니다.

### worldToLocalMatrix

`localToWorldMatrix`가 오브젝트 기준 좌표를 월드 좌표로 바꾸는 행렬이라면, `worldToLocalMatrix`는 반대 방향의 변환을 담당합니다. 월드 공간에 있는 점을 특정 오브젝트의 로컬 공간에서 다시 해석할 때 사용합니다.

월드 좌표를 다시 로컬 좌표로 바꾸려면, 로컬 좌표를 월드 좌표로 만들 때 적용했던 변환을 반대로 적용하면 됩니다. 따라서 `worldToLocalMatrix`는 `localToWorldMatrix`의 역행렬입니다.

$$
\text{worldToLocalMatrix} = \text{localToWorldMatrix}^{-1}
$$

앞의 캐릭터 예시를 그대로 사용하면, 월드 좌표 $(15, \; 3, \; 8)$에 있는 점을 캐릭터 기준의 로컬 좌표로 바꿀 수 있습니다.

$$
\text{로컬 좌표} = \text{worldToLocalMatrix} \times \begin{bmatrix} 15 \\ 3 \\ 8 \\ 1 \end{bmatrix}
$$

이 변환은 월드 공간의 위치를 특정 오브젝트 기준으로 다시 보고 싶을 때 유용합니다. 예를 들어 적이 플레이어 앞에 있는지 뒤에 있는지 판단하려면, 적의 위치를 월드 축이 아니라 플레이어의 축 기준으로 읽어야 합니다. 플레이어가 회전하면 플레이어의 정면 방향도 함께 바뀌지만, 월드 좌표축의 +z 방향은 그대로이기 때문입니다.

적의 월드 좌표에 플레이어의 `worldToLocalMatrix`를 곱하면, 그 좌표는 플레이어 기준의 로컬 좌표가 됩니다. 플레이어 로컬 공간에서는 +z가 정면이고 +x가 오른쪽이므로, 변환된 좌표의 z 부호로 앞뒤를, x 부호로 좌우를 판단할 수 있습니다.

### 부모-자식 관계와 행렬 계층

부모가 있는 오브젝트의 `localPosition`, `localRotation`, `localScale`은 월드 기준 값이 아닙니다. 부모 오브젝트를 기준으로 얼마나 떨어져 있고, 얼마나 회전해 있고, 어떤 크기를 가지는지를 나타냅니다.

그래서 자식의 월드 위치를 구하려면 두 단계를 거쳐야 합니다. 먼저 자식 자신의 로컬 TRS 행렬을 적용하고, 그 결과에 부모의 월드 변환을 다시 적용합니다. 부모가 움직이거나 회전하면 자식도 함께 따라 움직이는 이유가 여기에 있습니다.

행렬로 쓰면 자식의 `localToWorldMatrix`는 부모의 `localToWorldMatrix`에 자식의 로컬 TRS 행렬을 곱한 결과입니다.

<div style="text-align: center; margin: 1.5em 0;">
<svg viewBox="0 0 620 320" xmlns="http://www.w3.org/2000/svg" style="max-width: 620px; width: 100%;">
  <text x="310" y="18" text-anchor="middle" font-family="sans-serif" font-size="13" font-weight="bold" fill="currentColor">부모-자식 행렬 계층</text>
  <text x="310" y="46" text-anchor="middle" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">자식의 월드 행렬 = 부모의 월드 행렬 × 자식의 로컬 행렬</text>
  <line x1="40" y1="64" x2="580" y2="64" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="92" font-family="sans-serif" font-size="11" font-weight="bold" fill="currentColor">예: 탱크의 포탑</text>
  <text x="60" y="114" font-family="sans-serif" font-size="10" fill="currentColor"><tspan font-weight="bold">탱크 (부모)</tspan>: position (100, 0, 50), rotation Y축 30도</text>
  <text x="60" y="132" font-family="sans-serif" font-size="10" fill="currentColor"><tspan font-weight="bold">포탑 (자식)</tspan>: localPosition (0, 2, 0), localRotation Y축 15도</text>
  <text x="40" y="170" font-family="sans-serif" font-size="11" fill="currentColor"><tspan font-weight="bold">포탑의 월드 행렬</tspan></text>
  <text x="60" y="190" font-family="sans-serif" font-size="11" fill="currentColor">= 탱크의 localToWorldMatrix × 포탑의 로컬 TRS 행렬</text>
  <line x1="40" y1="212" x2="580" y2="212" stroke="currentColor" stroke-width="0.6" opacity="0.3"/>
  <text x="40" y="240" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">→ 포탑은 탱크의 위에 위치하면서</text>
  <text x="60" y="260" font-family="sans-serif" font-size="11" fill="currentColor" opacity="0.85">탱크의 방향(30도) + 자신의 추가 회전(15도) = <tspan font-weight="bold">45도</tspan>를 바라봄</text>
  <text x="60" y="280" font-family="sans-serif" font-size="10" fill="currentColor" opacity="0.7">(같은 축 회전이라 각도가 단순 덧셈됨)</text>
</svg>
</div>

부모의 월드 행렬이 자식의 월드 행렬에 포함되기 때문에, 부모를 움직이면 자식도 같은 변화를 함께 받습니다. 캐릭터의 손에 무기를 붙이거나, 차량의 바퀴를 차체 아래에 두는 방식이 이 원리를 사용합니다.

반대로 말하면, 부모의 Transform이 바뀌면 그 아래 자식들의 월드 행렬도 영향을 받습니다. 계층이 깊거나 자식이 많을수록 갱신해야 할 변환 정보가 늘어날 수 있습니다.

그래서 자주 움직이는 오브젝트는 계층을 지나치게 깊게 만들지 않는 편이 좋습니다. 특히 매 프레임 움직이는 부모 아래에 많은 자식을 두면 Transform 변경이 넓게 전파될 수 있으므로, 불필요한 중간 노드를 줄이고 실제로 함께 움직여야 하는 오브젝트만 같은 계층에 두는 편이 관리하기 쉽습니다.

Transform 변경 전파의 구체적인 비용과 최적화 방법은 [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)에서 다룹니다.

---

## 마무리

이 글에서는 벡터로 표현한 위치와 방향을 실제로 움직이고 돌리고 키우기 위해 행렬을 사용했습니다. 이동, 회전, 스케일은 따로 계산할 수도 있지만, 4x4 행렬로 묶으면 정점마다 같은 형태의 행렬-벡터 곱셈으로 처리할 수 있습니다.

- 3x3 행렬은 기존 x, y, z 성분을 섞거나 배율을 바꿀 수 있지만, 좌표에 일정한 값을 더하는 이동은 표현하지 못합니다.
- 동차 좌표를 사용하면 위치는 w = 1, 방향은 w = 0으로 구분할 수 있고, 이동·회전·스케일을 하나의 4x4 행렬 안에 담을 수 있습니다.
- 이동은 네 번째 열, 회전은 왼쪽 위 3x3 영역, 스케일은 대각 성분에 배치됩니다.
- 행렬 곱셈은 순서가 바뀌면 결과도 바뀝니다. 일반적인 오브젝트 변환은 Scale → Rotate → Translate 순서로 적용하고, 행렬로는 $M = T \times R \times S$로 씁니다.
- 오일러 각은 읽기 쉽지만 짐벌 락이 생길 수 있으므로, Unity는 회전을 내부적으로 쿼터니언으로 저장합니다.
- 비균일 스케일은 법선 보정, 콜라이더 해석, 자식 오브젝트 회전에서 예상과 다른 결과를 만들 수 있습니다.
- `localToWorldMatrix`는 Transform의 `position`, `rotation`, `localScale`을 반영한 Model 행렬이며, 로컬 좌표를 월드 좌표로 바꿉니다.
- 부모-자식 관계에서는 부모의 월드 행렬이 자식의 월드 행렬에 포함됩니다. 이 덕분에 자식은 부모를 따라 움직이지만, 깊고 자주 변하는 계층은 갱신 비용을 늘릴 수 있습니다.

여기까지는 오브젝트 안에 정의된 정점을 월드 공간에 배치하는 과정입니다. 화면에 그려지려면 정점은 이후에도 카메라 기준 공간과 투영을 위한 공간을 더 거칩니다. [그래픽스 수학 (3) - 좌표 공간의 전환](/dev/unity/GraphicsMath-3/)에서는 Model, View, Projection 행렬이 정점을 어떤 순서로 다음 좌표 공간으로 옮기는지 이어서 다룹니다.

---

**관련 글**
- [Unity 엔진 핵심 (2) - Transform 계층과 씬 그래프](/dev/unity/UnityCore-2/)

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
