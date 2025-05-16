---
layout: single
title: "[백준 9455] 박스 (C#, C++) - soo:bak"
date: "2025-05-16 20:51:00 +0900"
description: 박스가 중력 방향으로 떨어지며 바닥에 쌓일 때 이동한 총 거리를 계산하는 백준 9455번 박스 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[9455번 - 박스](https://www.acmicpc.net/problem/9455)

## 설명

**위에서 아래로 박스가 떨어지며 바닥이나 다른 박스 위에 쌓일 때, 박스들이 이동한 총 거리를 계산하는 시뮬레이션 문제입니다.**

<br>
그리드는 `r × c` 크기의 2차원 배열로 구성되며

각 칸에는 박스(`1`) 또는 빈 공간(`0`)이 들어있습니다.

<br>
박스는 **중력 방향인 아래쪽**으로 계속 이동할 수 있으며,

바닥 또는 다른 박스 위에 도달하면 더 이상 움직이지 않습니다.

<br>
모든 박스가 아래로 떨어져 정지했을 때, **이동한 거리의 총합**을 출력합니다.

<br>

## 접근법

이 문제는 **박스가 아래로 떨어질 수 있을 만큼 떨어졌을 때, 총 이동 거리**를 계산하는 것이 핵심입니다.

전체 과정은 다음과 같습니다:

1. 각 테스트케이스마다 `2차원 배열`로 그리드를 입력받습니다.
2. **위에서부터 아래로 탐색**하며,<br>
  박스가 발견되면 해당 열에서 빈 공간의 개수를 세어 최대로 떨어질 수 있는 거리 `k`를 계산합니다.
3. 현재 칸의 값을 `0`으로 바꾸고, 아래에 `1`을 새로 설정하여 박스를 "떨어뜨린" 효과를 시뮬레이션합니다.
4. 박스가 이동한 거리 `k`를 누적합에 더합니다.
5. 모든 박스에 대해 위 과정을 반복하여 최종 합계를 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split();
      int r = int.Parse(tokens[0]), c = int.Parse(tokens[1]);

      int[,] grid = new int[r, c];
      for (int i = 0; i < r; i++) {
        var row = Console.ReadLine().Split().Select(int.Parse).ToArray();
        for (int j = 0; j < c; j++)
          grid[i, j] = row[j];
      }

      int total = 0;
      for (int j = 0; j < c; j++) {
        int dropTo = r - 1;
        for (int i = r - 1; i >= 0; i--) {
          if (grid[i, j] == 1) {
            total += dropTo - i;
            dropTo--;
          }
        }
      }
      Console.WriteLine(total);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int r, c; cin >> r >> c;

    vvi grid(r, vi(c));
    for (auto& row : grid) {
      for (auto& x : row)
        cin >> x;
    }

    int moves = 0;
    for (int i = r - 2; i >= 0; --i) {
      for (int j = 0; j < c; ++j) {
        if (grid[i][j]) {
          int k = 1;
          while (i + k < r && !grid[i + k][j])
            ++k;
          --k;
          grid[i][j] = 0;
          grid[i + k][j] = 1;
          moves += k;
        }
      }
    }

    cout << moves << "\n";
  }

  return 0;
}
```
