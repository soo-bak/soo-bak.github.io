---
layout: single
title: "[백준 30009] 포지션 제로 (C#, C++) - soo:bak"
date: "2025-05-14 01:46:00 +0900"
description: 수직선 위의 직선이 원의 내부 또는 경계에 접하는지 판단하는 백준 30009번 포지션 제로 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[30009번 - 포지션 제로](https://www.acmicpc.net/problem/30009)

## 설명
**주어진 수직선들이 원의 내부 또는 경계에 닿는지를 판단하는 문제입니다.**<br>

2차원 좌표평면 위에 중심이 $$(X, Y)$$이고 반지름이 $$R$$인 원이 존재하며,

이때 $$x = T_i$$ 형태로 표현된 여러 개의 수직선 중 해당 원의 내부에 닿는 수직선과,

경계에만 접하는 수직선의 개수를 구하는 것이 목표입니다.

<br>

모든 수직선은 세로 방향으로 고정되어 있으며,

원의 형태로 정의된 "포지션 제로"에 접하거나 포함되는지를 판단해야 합니다.

<br>

## 접근법

입력으로 주어지는 모든 수직선은 $$x = T_i$$ 형태이므로,

해당 수직선이 원의 내부에 들어가는지, 경계에 위치하는지를 x좌표 기준으로만 판단할 수 있습니다.

<br>

- 먼저 원의 좌우 범위는 중심 $$X$$를 기준으로,
  - 좌측 끝 $$X - R$$
  - 우측 끝 $$X + R$$
- 수직선의 `x`좌표 $$T_i$$가 이 범위와 어떤 관계를 가지는지를 기준으로 나누어 판단합니다.

<br>

- 만약 $$T_i = X - R$$ 또는 $$T_i = X + R$$인 경우, 원의 **경계에 정확히 접하는 직선**입니다.
- $$X - R < T_i < X + R$$인 경우는 원의 **내부에 닿는 직선**입니다.
- 나머지의 경우는 원과 **아무 접점이 없는 직선**입니다.

<br>

이렇게 모든 직선에 대해 조건을 확인하면서, 내부 접촉과 경계 접촉의 개수를 각각 카운트하여 출력합니다.

입력 크기가 작기 때문에, 각 수직선에 대해 단순 조건 분기로 충분히 해결할 수 있습니다.

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    var tokens = Console.ReadLine().Split();
    int x = int.Parse(tokens[0]);
    int y = int.Parse(tokens[1]);
    int r = int.Parse(tokens[2]);

    int[] points = new int[n];
    for (int i = 0; i < n; i++)
      points[i] = int.Parse(Console.ReadLine());

    int left = x - r, right = x + r;
    int inner = 0, boundary = 0;

    foreach (int p in points) {
      if (p == left || p == right) boundary++;
      else if (left < p && p < right) inner++;
    }

    Console.WriteLine($"{inner} {boundary}");
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  int x, y, r; cin >> x >> y >> r;

  vi points(n);
  for (int i = 0; i < n; i++)
    cin >> points[i];

  int left = x - r, right = x + r;
  int inner = 0, boundary = 0;
  for (int p : points) {
    if (p == left || p == right) boundary++;
    else if (left < p && p < right) inner++;
  }

  cout << inner << " " << boundary << "\n";

  return 0;
}
```
