---
layout: single
title: "[백준 4117] Combination Lock (C#, C++) - soo:bak"
date: "2026-01-12 21:00:00 +0900"
description: "백준 4117번 C#, C++ 풀이 - 시작 위치를 임의로 잡아 세 번의 회전으로 자물쇠를 여는 데 필요한 최대 틱 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 4117
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 4117, 백준 4117번, BOJ 4117, Combination Lock, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4117번 - Combination Lock](https://www.acmicpc.net/problem/4117)

## 설명
원형 다이얼 자물쇠가 있습니다. 다이얼에는 0부터 N-1까지 번호가 매겨진 N개의 틱이 있으며, 시계 방향으로 번호가 증가합니다.

자물쇠를 여는 방법은 세 단계입니다. 먼저 시계 방향으로 정확히 두 바퀴를 돌고 계속 시계 방향으로 틱 T1까지 이동합니다. 다음으로 반시계 방향으로 정확히 한 바퀴를 돌고 계속 반시계 방향으로 틱 T2까지 이동합니다. 마지막으로 시계 방향으로 틱 T3까지 이동하면 자물쇠가 열립니다.

시작 위치는 자유롭게 선택할 수 있으며, 세 번의 회전으로 자물쇠를 여는 데 필요한 최대 틱 수를 구하는 문제입니다. 

<br>

## 접근법
먼저 각 단계에서 회전하는 틱 수를 계산합니다.

첫 번째 단계는 두 바퀴에 시작 위치에서 T1까지의 거리를 더한 값이고,

두 번째 단계는 한 바퀴에 T1에서 T2까지의 거리를 더한 값이며,

세 번째 단계는 T2에서 T3까지의 거리입니다.

시작 위치는 자유롭게 선택할 수 있으므로, 첫 번째 단계에서 시작 위치에서 T1까지의 거리가 최대가 되도록 선택합니다. 이 거리의 최댓값은 N - 1입니다.

이후 세 단계의 회전 틱 수를 모두 합하면 최대 틱 수를 구할 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var sb = new StringBuilder();
    while (true) {
      var line = Console.ReadLine();
      if (line == null)
        break;
      var p = line.Split();
      var n = int.Parse(p[0]);
      var t1 = int.Parse(p[1]);
      var t2 = int.Parse(p[2]);
      var t3 = int.Parse(p[3]);
      if (n == 0 && t1 == 0 && t2 == 0 && t3 == 0)
        break;

      int Cw(int a, int b) {
        return (a - b + n) % n;
      }

      int Ccw(int a, int b) {
        return (b - a + n) % n;
      }

      var res = 3 * n + (n - 1) + Ccw(t1, t2) + Cw(t2, t3);
      sb.Append(res).Append('\n');
    }
    Console.Write(sb);
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

  while (true) {
    int n, t1, t2, t3;
    if (!(cin >> n >> t1 >> t2 >> t3))
      break;
    if (n == 0 && t1 == 0 && t2 == 0 && t3 == 0)
      break;

    auto cw = [n](int a, int b) {
      return (a - b + n) % n;
    };
    auto ccw = [n](int a, int b) {
      return (b - a + n) % n;
    };

    int ans = 3 * n + (n - 1) + ccw(t1, t2) + cw(t2, t3);
    cout << ans << "\n";
  }

  return 0;
}
```
