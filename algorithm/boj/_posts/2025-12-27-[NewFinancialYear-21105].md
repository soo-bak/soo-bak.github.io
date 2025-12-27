---
layout: single
title: "[백준 21105] New Financial Year (C#, C++) - soo:bak"
date: "2025-12-27 14:45:00 +0900"
description: "백준 21105번 C#, C++ 풀이 - 새 가격과 변화율로부터 원래 가격을 역산하는 문제"
tags:
  - 백준
  - BOJ
  - 21105
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 21105, 백준 21105번, BOJ 21105, NewFinancialYear, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[21105번 - New Financial Year](https://www.acmicpc.net/problem/21105)

## 설명
새 가격과 백분율 변화율이 주어질 때, 원래 가격을 구하는 문제입니다.

<br>

## 접근법
변화율 공식을 원래 가격에 대해 정리하면, 원래 가격은 새 가격에 100을 곱하고 100과 변화율의 합으로 나눈 값이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Globalization;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var p = double.Parse(parts[0], CultureInfo.InvariantCulture);
      var c = double.Parse(parts[1], CultureInfo.InvariantCulture);

      var o = (100 * p) / (100 + c);
      Console.WriteLine(o.ToString("F5", CultureInfo.InvariantCulture));
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

  int n; cin >> n;
  for (int i = 0; i < n; i++) {
    double p, c; cin >> p >> c;

    double o = (100 * p) / (100 + c);
    cout << fixed << setprecision(5) << o << "\n";
  }

  return 0;
}
```

