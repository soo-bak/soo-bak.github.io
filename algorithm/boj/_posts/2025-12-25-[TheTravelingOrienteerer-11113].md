---
layout: single
title: "[백준 11113] The Traveling Orienteerer (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 11113번 C#, C++ 풀이 - 경로의 연속한 점 거리 합을 반올림해 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 11113
  - C#
  - C++
  - 알고리즘
keywords: "백준 11113, 백준 11113번, BOJ 11113, TheTravelingOrienteerer, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11113번 - The Traveling Orienteerer](https://www.acmicpc.net/problem/11113)

## 설명
각 경로의 제어점을 순서대로 이어가며 이동한 총 거리를 구하고, 이를 반올림해 출력하는 문제입니다.

<br>

## 접근법
모든 점의 좌표를 저장한 뒤, 각 경로의 인덱스를 읽으며 이전 점과의 유클리드 거리를 누적합니다.  
경로의 총합에 0.5를 더해 정수로 변환하면 반올림 값이 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);

    var xs = new double[n];
    var ys = new double[n];
    for (var i = 0; i < n; i++) {
      xs[i] = double.Parse(parts[idx++]);
      ys[i] = double.Parse(parts[idx++]);
    }

    var m = int.Parse(parts[idx++]);
    var sb = new StringBuilder();
    for (var route = 0; route < m; route++) {
      var p = int.Parse(parts[idx++]);
      var prev = int.Parse(parts[idx++]);
      var sum = 0.0;
      for (var i = 1; i < p; i++) {
        var cur = int.Parse(parts[idx++]);
        var dx = xs[prev] - xs[cur];
        var dy = ys[prev] - ys[cur];
        sum += Math.Sqrt(dx * dx + dy * dy);
        prev = cur;
      }
      var ans = (int)(sum + 0.5);
      sb.AppendLine(ans.ToString());
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

  int n; cin >> n;
  vector<double> xs(n), ys(n);
  for (int i = 0; i < n; i++)
    cin >> xs[i] >> ys[i];

  int m; cin >> m;
  for (int route = 0; route < m; route++) {
    int p; cin >> p;
    int prev; cin >> prev;
    double sum = 0;
    for (int i = 1; i < p; i++) {
      int cur; cin >> cur;
      double dx = xs[prev] - xs[cur];
      double dy = ys[prev] - ys[cur];
      sum += sqrt(dx * dx + dy * dy);
      prev = cur;
    }
    int ans = (int)(sum + 0.5);
    cout << ans << "\n";
  }

  return 0;
}
```
