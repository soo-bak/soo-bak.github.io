---
layout: single
title: "[백준 9945] Centroid of Point Masses (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 9945번 C#, C++ 풀이 - 점 질량의 질량중심 좌표를 여러 테스트케이스에 대해 구하는 문제"
tags:
  - 백준
  - BOJ
  - 9945
  - C#
  - C++
  - 알고리즘
keywords: "백준 9945, 백준 9945번, BOJ 9945, CentroidPointMasses, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9945번 - Centroid of Point Masses](https://www.acmicpc.net/problem/9945)

## 설명
여러 점의 좌표와 질량이 주어질 때 질량중심 좌표를 구하는 문제입니다.

<br>

## 접근법
질량중심은 각 좌표에 질량을 가중치로 곱한 값의 합을 전체 질량으로 나누어 구합니다.

각 테스트케이스마다 질량의 합과 좌표별 가중합을 누적한 뒤, 전체 질량으로 나누어 질량중심 좌표를 계산합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var tc = 1;
    while (true) {
      var line = Console.ReadLine();
      if (line == null) break;
      line = line.Trim();
      if (line == "") continue;

      var n = int.Parse(line);
      if (n < 0) break;

      var sumM = 0L;
      var sumX = 0.0;
      var sumY = 0.0;
      for (var i = 0; i < n; i++) {
        var parts = Console.ReadLine()!.Split(new char[]{' ','\t'}, StringSplitOptions.RemoveEmptyEntries);
        var x = int.Parse(parts[0]);
        var y = int.Parse(parts[1]);
        var m = int.Parse(parts[2]);
        sumM += m;
        sumX += m * x;
        sumY += m * y;
      }

      var a = sumX / sumM;
      var b = sumY / sumM;
      Console.WriteLine($"Case {tc}: {a:F2} {b:F2}");
      tc++;
    }
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

  int n, tc = 1;
  while (cin >> n) {
    if (n < 0) break;

    double sumX = 0, sumY = 0;
    int sumM = 0;
    for (int i = 0; i < n; i++) {
      int x, y, m; cin >> x >> y >> m;
      sumM += m;
      sumX += (double)m * x;
      sumY += (double)m * y;
    }

    double a = sumX / sumM;
    double b = sumY / sumM;

    cout << fixed << setprecision(2);
    cout << "Case " << tc << ": " << (double)a << " " << (double)b << "\n";
    tc++;
  }

  return 0;
}
```
