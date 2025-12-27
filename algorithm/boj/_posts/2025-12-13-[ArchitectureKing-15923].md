---
layout: single
title: "[백준 15923] 욱제는 건축왕이야!! (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 직교 단순 다각형의 꼭짓점을 따라 맨해튼 거리를 누적해 둘레를 구하는 백준 15923번 욱제는 건축왕이야!! 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15923
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 기하학
keywords: "백준 15923, 백준 15923번, BOJ 15923, ArchitectureKing, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15923번 - 욱제는 건축왕이야!!](https://www.acmicpc.net/problem/15923)

## 설명
직교 다각형의 꼭짓점 좌표가 순서대로 주어질 때, 다각형의 둘레를 구하는 문제입니다.

<br>

## 접근법
인접한 두 꼭짓점 사이의 거리는 x 좌표 차이의 절댓값과 y 좌표 차이의 절댓값을 더한 값입니다.

입력 순서대로 좌표를 읽으면서 이전 점과의 거리를 누적합니다.

마지막 점과 첫 점 사이의 거리까지 더하면 전체 둘레가 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var first = Console.ReadLine()!.Split();
    var sx = int.Parse(first[0]);
    var sy = int.Parse(first[1]);

    var prevX = sx;
    var prevY = sy;
    var peri = 0;

    for (var i = 1; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var x = int.Parse(parts[0]);
      var y = int.Parse(parts[1]);
      peri += Math.Abs(x - prevX) + Math.Abs(y - prevY);
      prevX = x; prevY = y;
    }

    peri += Math.Abs(prevX - sx) + Math.Abs(prevY - sy);
    Console.WriteLine(peri);
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

  int n; cin >> n;
  int sx, sy; cin >> sx >> sy;
  int px = sx, py = sy;
  int peri = 0;

  for (int i = 1; i < n; i++) {
    int x, y; cin >> x >> y;
    peri += abs(x - px) + abs(y - py);
    px = x; py = y;
  }

  peri += abs(px - sx) + abs(py - sy);
  cout << peri << "\n";

  return 0;
}
```
