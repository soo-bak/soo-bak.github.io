---
layout: single
title: "[백준 1531] 투명 (C#, C++) - soo:bak"
date: "2025-05-16 20:11:00 +0900"
description: 중첩된 종이의 수를 기준으로 그림이 보이지 않는 칸의 개수를 계산하는 백준 1531번 투명 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1531번 - 투명](https://www.acmicpc.net/problem/1531)

## 설명

**여러 장의 종이로** `100 × 100` **크기의 그림을 덮었을 때,**

**지정된 수보다 더 많이 덮여 가려진 칸의 개수를 계산하는 문제입니다.**

- 각 종이는 직사각형이며, 겹쳐서 그림 위에 올려질 수 있습니다.
- 특정 칸이 종이에 의해 가려진 횟수가 `K`를 초과하면 해당 칸의 그림은 보이지 않게 됩니다.
- 반대로 `K` 이하로만 가려졌다면 그 칸의 그림은 여전히 보입니다.

문제는 종이 `N`장과 기준값 `K`가 주어졌을 때,

**보이지 않는 칸의 개수**, 즉 `K`보다 많이 덮인 칸이 몇 개인지를 구하여 출력합니다.

<br>

## 접근법

`100 × 100` 의 격자를 만들어 각 칸에 종이가 몇 번씩 겹쳤는지를 카운팅합니다.

- 초기화된 격자에서 각 종이의 좌표 범위에 대해 순회하면서,<br>
  해당 범위 내 모든 칸의 값을 `1`씩 증가시킵니다.

모든 종이에 대해 이 과정을 반복한 후,

격자의 각 칸을 확인하여 값이 `K`를 초과하는 칸의 개수를 셉니다.

단순한 **2차원 누적 시뮬레이션**으로 시간 제한 내에 충분히 계산이 가능합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int[,] grid = new int[100, 100];

    var tokens = Console.ReadLine().Split();
    int n = int.Parse(tokens[0]);
    int k = int.Parse(tokens[1]);

    for (int t = 0; t < n; t++) {
      var input = Console.ReadLine().Split();
      int x1 = int.Parse(input[0]) - 1;
      int y1 = int.Parse(input[1]) - 1;
      int x2 = int.Parse(input[2]);
      int y2 = int.Parse(input[3]);

      for (int y = y1; y < y2; y++)
        for (int x = x1; x < x2; x++)
          grid[y, x]++;
    }

    int hidden = 0;
    for (int y = 0; y < 100; y++)
      for (int x = 0; x < 100; x++)
        if (grid[y, x] > k) hidden++;

    Console.WriteLine(hidden);
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

  int grid[100][100] = {};

  int n, k; cin >> n >> k;
  while (n--) {
    int x1, y1, x2, y2; cin >> x1 >> y1 >> x2 >> y2;
    for (int y = y1 - 1; y < y2; ++y) {
      for (int x = x1 - 1; x < x2; ++x)
        ++grid[y][x];
    }
  }

  int hidden = 0;
  for (int y = 0; y < 100; ++y) {
    for (int x = 0; x < 100; ++x)
      if (grid[y][x] > k) ++hidden;
  }

  cout << hidden << "\n";

  return 0;
}
```
