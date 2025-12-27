---
layout: single
title: "[백준 4327] Combination Lock (C#, C++) - soo:bak"
date: "2025-12-27 08:05:00 +0900"
description: "백준 4327번 C#, C++ 풀이 - 자물쇠 다이얼을 여는 데 필요한 총 회전 각도를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 4327
  - C#
  - C++
  - 알고리즘
keywords: "백준 4327, 백준 4327번, BOJ 4327, CombinationLock, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4327번 - Combination Lock](https://www.acmicpc.net/problem/4327)

## 설명
40칸 다이얼 자물쇠에서 초기 위치와 세 개의 번호가 주어질 때, 자물쇠를 열기 위해 다이얼을 돌린 총 각도를 구하는 문제입니다.

<br>

## 접근법
시계 방향으로 두 바퀴 돌린 후 첫 번째 번호까지 계속 시계 방향으로 돌립니다. 이후 반시계 방향으로 한 바퀴 돌린 후 두 번째 번호까지 계속 반시계로 돌립니다. 마지막으로 시계 방향으로 세 번째 번호까지 돌립니다.

각 단계에서 이동한 칸 수를 모두 더한 뒤 9를 곱하면 총 각도가 됩니다. 한 칸이 9도이기 때문입니다.

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
    string? line;
    while ((line = Console.ReadLine()) != null) {
      var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
      if (parts.Length == 0) continue;
      var p0 = int.Parse(parts[0]);
      var a = int.Parse(parts[1]);
      var b = int.Parse(parts[2]);
      var c = int.Parse(parts[3]);
      if (p0 == 0 && a == 0 && b == 0 && c == 0) break;

      var ticks = 80;
      ticks += (p0 - a + 40) % 40;
      ticks += 40;
      ticks += (b - a + 40) % 40;
      ticks += (b - c + 40) % 40;

      sb.AppendLine((ticks * 9).ToString());
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

  int p0, a, b, c;
  while (cin >> p0 >> a >> b >> c) {
    if (p0 == 0 && a == 0 && b == 0 && c == 0) break;

    int ticks = 80;
    ticks += (p0 - a + 40) % 40;
    ticks += 40;
    ticks += (b - a + 40) % 40;
    ticks += (b - c + 40) % 40;

    cout << ticks * 9 << "\n";
  }

  return 0;
}
```
