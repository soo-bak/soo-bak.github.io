---
layout: single
title: "[백준 13496] The Merchant of Venice (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 도착 가능 거리 내 선박의 화물 가치를 합산해 상환 가능한 두캇을 구하는 백준 13496번 The Merchant of Venice 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 13496
  - C#
  - C++
  - 알고리즘
keywords: "백준 13496, 백준 13496번, BOJ 13496, MerchantOfVenice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13496번 - The Merchant of Venice](https://www.acmicpc.net/problem/13496)

## 설명
도착 가능 거리 내 선박들의 화물 가치 합을 구하는 문제입니다.

<br>

## 접근법
선박 속도와 남은 일수를 곱하면 도착 가능 거리가 됩니다.

각 선박의 거리가 이 범위 이내이면 화물 가치를 누적합니다.

데이터셋별로 합계를 출력하며 데이터셋 사이에 빈 줄을 넣습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 1; tc <= t; tc++) {
      var line = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var n = line[0]; var s = line[1]; var d = line[2];
      var limit = s * d;
      var sum = 0;
      for (var i = 0; i < n; i++) {
        var ship = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
        var dist = ship[0]; var val = ship[1];
        if (dist <= limit) sum += val;
      }
      if (tc > 1) Console.WriteLine();
      Console.WriteLine($"Data Set {tc}:");
      Console.WriteLine(sum);
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

  int t;
  if (!(cin >> t)) return 0;
  for (int tc = 1; tc <= t; tc++) {
    int n, s, d;
    cin >> n >> s >> d;
    int limit = s * d;
    int sum = 0;
    for (int i = 0; i < n; i++) {
      int dist, val; cin >> dist >> val;
      if (dist <= limit) sum += val;
    }
    if (tc > 1) cout << "\n";
    cout << "Data Set " << tc << ":\n";
    cout << sum << "\n";
  }

  return 0;
}
```
