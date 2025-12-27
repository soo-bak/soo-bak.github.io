---
layout: single
title: "[백준 11434] Ampelmännchen (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: "백준 11434번 C#, C++ 풀이 - 각 품목마다 서독/동독 버전 중 행복 총합이 큰 쪽을 선택해 최대 행복을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 11434
  - C#
  - C++
  - 알고리즘
keywords: "백준 11434, 백준 11434번, BOJ 11434, Ampelmaennchen, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11434번 - Ampelmännchen](https://www.acmicpc.net/problem/11434)

## 설명
각 품목마다 서독 버전과 동독 버전 중 하나를 선택해 전체 행복을 최대화하는 문제입니다.

<br>

## 접근법
각 품목에 대해 서독 주민과 동독 주민의 선호도가 주어집니다. 서독 버전을 선택하면 서독 인구에 서독 버전 선호도를, 동독 인구에 서독 버전 선호도를 곱해 더합니다. 동독 버전도 마찬가지로 계산합니다.

품목 간에 영향이 없으므로, 각 품목에서 두 선택지 중 더 큰 행복을 주는 쪽을 선택하면 됩니다. 모든 품목에서 선택한 값을 누적하면 최대 행복이 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var k = int.Parse(Console.ReadLine()!);
    for (var tc = 1; tc <= k; tc++) {
      var first = Console.ReadLine()!.Split();
      var n = int.Parse(first[0]);
      var w = int.Parse(first[1]);
      var e = int.Parse(first[2]);

      var total = 0;
      for (var i = 0; i < n; i++) {
        var p = Console.ReadLine()!.Split();
        var lww = int.Parse(p[0]);
        var lwe = int.Parse(p[1]);
        var lew = int.Parse(p[2]);
        var lee = int.Parse(p[3]);

        var west = w * lww + e * lew;
        var east = w * lwe + e * lee;
        total += west > east ? west : east;
      }

      Console.WriteLine($"Data Set {tc}:");
      Console.WriteLine(total);
      Console.WriteLine();
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

  int k; cin >> k;
  for (int tc = 1; tc <= k; tc++) {
    int n, w, e;
    cin >> n >> w >> e;

    int total = 0;
    for (int i = 0; i < n; i++) {
      int lww, lwe, lew, lee;
      cin >> lww >> lwe >> lew >> lee;

      int west = w * lww + e * lew;
      int east = w * lwe + e * lee;
      total += max(west, east);
    }

    cout << "Data Set " << tc << ":\n" << total << "\n\n";
  }

  return 0;
}
```
