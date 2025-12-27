---
layout: single
title: "[백준 1198] 삼각형으로 자르기 (C#, C++) - soo:bak"
date: "2025-12-06 23:40:00 +0900"
description: 볼록 다각형에서 마지막으로 남을 수 있는 삼각형 넓이의 최댓값을 구하는 백준 1198번 삼각형으로 자르기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1198
  - C#
  - C++
  - 알고리즘
keywords: "백준 1198, 백준 1198번, BOJ 1198, CutByTriangles, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1198번 - 삼각형으로 자르기](https://www.acmicpc.net/problem/1198)

## 설명
볼록 다각형을 연속된 세 정점으로 삼각형을 잘라가며 마지막에 남는 삼각형 넓이의 최댓값을 구하는 문제입니다.

볼록 다각형의 정점이 시계방향으로 주어집니다.

<br>

## 접근법
볼록 다각형을 삼각형으로 자를 때 새로운 점이 생기지 않습니다. 어떻게 잘라도 원래 정점들만 사용하게 됩니다. 따라서 마지막에 남는 삼각형도 원래 정점 3개로 이루어집니다.

이 점을 이용하면 문제가 단순해집니다. 원래 정점들 중 3개를 골라 만들 수 있는 모든 삼각형의 넓이를 구하고, 그 중 최댓값을 찾으면 됩니다.

N이 최대 35이므로 3중 반복문으로 모든 조합을 확인해도 충분합니다. 세 점의 삼각형 넓이는 벡터 외적의 절댓값을 2로 나눈 값으로 구합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  struct Point { public int X, Y; }

  class Program {
    static int TwiceArea(Point a, Point b, Point c) {
      return Math.Abs((b.Y - a.Y) * (c.X - a.X) - (b.X - a.X) * (c.Y - a.Y));
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var p = new Point[n];
      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!.Split();
        p[i].X = int.Parse(s[0]);
        p[i].Y = int.Parse(s[1]);
      }

      var best2 = 0;
      for (var i = 0; i < n - 2; i++) {
        for (var j = i + 1; j < n - 1; j++) {
          for (var k = j + 1; k < n; k++) {
            var a2 = TwiceArea(p[i], p[j], p[k]);
            if (a2 > best2)
              best2 = a2;
          }
        }
      }

      Console.WriteLine((best2 / 2.0).ToString("0.000000000"));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

struct Point { int x, y; };

int twiceArea(const Point& a, const Point& b, const Point& c) {
  return abs((b.y - a.y) * (c.x - a.x) - (b.x - a.x) * (c.y - a.y));
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vector<Point> p(n);
  for (int i = 0; i < n; i++)
    cin >> p[i].x >> p[i].y;

  int best2 = 0;
  for (int i = 0; i < n - 2; i++) {
    for (int j = i + 1; j < n - 1; j++) {
      for (int k = j + 1; k < n; k++) {
        int a2 = twiceArea(p[i], p[j], p[k]);
        if (a2 > best2)
          best2 = a2;
      }
    }
  }

  cout << fixed << setprecision(9) << best2 / 2.0 << "\n";

  return 0;
}
```
