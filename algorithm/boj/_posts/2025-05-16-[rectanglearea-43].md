---
layout: single
title: "[백준 2669] 직사각형 네개의 합집합의 면적 구하기 (C#, C++) - soo:bak"
date: "2025-05-16 02:18:00 +0900"
description: 4개의 좌표 사각형이 차지하는 전체 면적을 격자 기반으로 계산하는 백준 2669번 직사각형 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2669
  - C#
  - C++
  - 알고리즘
keywords: "백준 2669, 백준 2669번, BOJ 2669, rectanglearea, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2669번 - 직사각형 네개의 합집합의 면적 구하기](https://www.acmicpc.net/problem/2669)

## 설명

**네 개의 직사각형이 주어졌을 때, 이들이 차지하는 전체 면적을 계산하는 문제입니다.**

입력으로 주어지는 각 직사각형은 왼쪽 아래 꼭짓점과 오른쪽 위 꼭짓점의 좌표로 표현되며,

좌표는 모두 정수이고 `x`, `y` 값 모두 `1` 이상 `100` 이하입니다.

<br>
각 사각형은 겹쳐질 수도 있고, 떨어져 있을 수도 있으며,

겹친 부분은 중복해서 세지 않고 전체 넓이를 한 번만 계산해야 합니다.

<br>

## 접근법
직사각형의 좌표는 모두 `1` 이상 `100` 이하의 정수로 주어지므로, 전체 평면을 `100 x 100 `격자로 생각할 수 있습니다.

각 직사각형은 이 격자 위의 일부 영역을 차지하게 되며, 여러 개가 겹쳐질 수도 있습니다.

<br>
이 문제에서는 전체 넓이에서 겹치는 부분을 한 번만 계산해야 하므로, 다음과 같은 방식으로 처리할 수 있습니다:
- `100 x 100` 크기의 2차원 배열을 사용하여, 해당 칸이 한 번이라도 직사각형에 의해 덮였는지 여부를 기록합니다.
- 각 직사각형에 대해, 주어진 좌표 범위만큼 격자 칸을 순회하며 해당 칸을 표시합니다.
- 마지막에는 배열 전체를 순회하며, 표시된 칸의 개수를 세면 전체 넓이가 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    bool[,] board = new bool[100, 100];

    for (int i = 0; i < 4; i++) {
      var input = Console.ReadLine().Split();
      int x1 = int.Parse(input[0]);
      int y1 = int.Parse(input[1]);
      int x2 = int.Parse(input[2]);
      int y2 = int.Parse(input[3]);

      for (int y = y1; y < y2; y++) {
        for (int x = x1; x < x2; x++)
          board[y, x] = true;
      }
    }

    int area = 0;
    foreach (var cell in board)
      if (cell) area++;

    Console.WriteLine(area);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  bool cord[100][100] = { };
  for (int i = 0; i < 4; i++) {
    int sX, sY, eX, eY; cin >> sX >> sY >> eX >> eY;
    for (int y = sY; y < eY; y++) {
      for (int x = sX; x < eX; x++)
        cord[y][x] = true;
    }
  }

  int s = 0;
  for (int y = 0; y < 100; y++) {
    for (int x = 0; x < 100; x++)
      s += cord[y][x];
  }

  cout << s << "\n";

  return 0;
}
```
