---
layout: single
title: "[백준 14013] Unit Conversion (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 14013번 C#, C++ 풀이 - 두 단위 사이의 비율이 주어질 때 여러 값을 상호 변환하는 문제"
tags:
  - 백준
  - BOJ
  - 14013
  - C#
  - C++
  - 알고리즘
keywords: "백준 14013, 백준 14013번, BOJ 14013, UnitConversion, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14013번 - Unit Conversion](https://www.acmicpc.net/problem/14013)

## 설명
두 단위 사이의 비율이 주어질 때, 여러 값을 반대 단위로 변환해 출력하는 문제입니다.

<br>

## 접근법
x A = y B라는 비율이 주어지면, 단위 A의 값 1은 단위 B로 y/x가 됩니다. 반대로 단위 B의 값 1은 단위 A로 x/y가 됩니다.

입력값이 A 단위면 y/x를 곱하고, B 단위면 x/y를 곱해서 출력합니다. 부동소수점 오차를 줄이기 위해 충분한 자릿수로 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Globalization;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var x = double.Parse(first[0]);
    var y = double.Parse(first[1]);
    var n = int.Parse(Console.ReadLine()!);

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var z = double.Parse(parts[0]);
      var q = parts[1][0];
      var res = q == 'A' ? z * y / x : z * x / y;
      Console.WriteLine(res.ToString("F12"));
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

  double x, y; cin >> x >> y;
  int n; cin >> n;

  cout << fixed << setprecision(12);

  for (int i = 0; i < n; i++) {
    double z; char q; cin >> z >> q;
    double res = (q == 'A') ? z * y / x : z * x / y;
    cout << res << "\n";
  }

  return 0;
}
```
