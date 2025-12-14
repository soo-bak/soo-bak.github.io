---
layout: single
title: "[백준 25965] 미션 도네이션 (C#, C++) - soo:bak"
date: "2025-12-14 09:03:00 +0900"
description: 각 미션의 계산 결과가 음수면 0으로 처리해 합산하는 방식으로 게임별 총 도네이션을 구하는 백준 25965번 문제의 C#/C++ 풀이
---

## 문제 링크
[25965번 - 미션 도네이션](https://www.acmicpc.net/problem/25965)

## 설명
여러 게임이 주어지고, 각 게임마다 미션별 도네이션 금액을 합산하는 문제입니다.

각 미션의 금액은 K × k - D × d + A × a 로 계산되며, 음수이면 0으로 처리합니다.

<br>

## 접근법
각 게임마다 미션별 계수와 실제 k, d, a 값을 읽습니다.

이후 각 미션에 대해 공식을 적용하고, 결과가 양수인 경우에만 누적합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var g = 0; g < t; g++) {
      var m = int.Parse(Console.ReadLine()!);
      var missions = new long[m, 3];
      for (var i = 0; i < m; i++) {
        var p = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
        missions[i, 0] = p[0];
        missions[i, 1] = p[1];
        missions[i, 2] = p[2];
      }
      var kda = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
      var k = kda[0];
      var d = kda[1];
      var a = kda[2];

      var total = 0L;
      for (var i = 0; i < m; i++) {
        var val = missions[i, 0] * k - missions[i, 1] * d + missions[i, 2] * a;
        if (val > 0) total += val;
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

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int m; cin >> m;
    vector<array<ll, 3>> mission(m);
    for (int i = 0; i < m; i++)
      cin >> mission[i][0] >> mission[i][1] >> mission[i][2];
    ll k, d, a; cin >> k >> d >> a;
    ll total = 0;
    for (auto &e : mission) {
      ll val = e[0] * k - e[1] * d + e[2] * a;
      if (val > 0) total += val;
    }
    cout << total << "\n";
  }

  return 0;
}
```
