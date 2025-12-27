---
layout: single
title: "[백준 21339] Contest Struggles (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 전체 평균과 풀었던 문제 평균으로 남은 문제들의 평균 난이도를 구하거나 불가능하면 impossible을 출력하는 백준 21339번 문제에 대한 C# 및 C++ 설명
tags:
  - 백준
  - BOJ
  - 21339
  - C#
  - C++
  - 알고리즘
keywords: "백준 21339, 백준 21339번, BOJ 21339, ContestStruggles, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[21339번 - Contest Struggles](https://www.acmicpc.net/problem/21339)

## 설명
문제 세트의 전체 평균 난이도와 이미 푼 문제들의 평균 난이도가 주어질 때, 남은 문제들의 평균 난이도를 계산하거나 범위를 벗어나면 impossible을 출력하는 문제입니다.

<br>

## 접근법
전체 문제 수와 전체 평균, 푼 문제 수와 푼 문제의 평균이 주어집니다. 전체 난이도 합에서 푼 문제의 난이도 합을 빼면 남은 문제의 난이도 합이 됩니다. 이를 남은 문제 수로 나누면 남은 문제의 평균을 구할 수 있습니다.

계산된 평균이 0 이상 100 이하이면 출력하고, 범위를 벗어나면 impossible을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var k = int.Parse(first[1]);

    var second = Console.ReadLine()!.Split();
    var d = int.Parse(second[0]);
    var s = int.Parse(second[1]);

    var x = (n * d - k * s) / (double)(n - k);
    if (x < -1e-9 || x > 100 + 1e-9) Console.WriteLine("impossible");
    else Console.WriteLine(x.ToString("0.##########"));
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

  int n, k; cin >> n >> k;
  int d, s; cin >> d >> s;

  double x = (n * d - k * s) / double(n - k);
  if (x < -1e-9 || x > 100.0 + 1e-9) cout << "impossible\n";
  else cout << fixed << setprecision(10) << x << "\n";

  return 0;
}
```
