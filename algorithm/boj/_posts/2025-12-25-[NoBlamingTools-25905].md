---
layout: single
title: "[백준 25905] 장인은 도구를 탓하지 않는다 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 9개의 확률을 골라 최대 성공 확률을 계산하는 문제
---

## 문제 링크
[25905번 - 장인은 도구를 탓하지 않는다](https://www.acmicpc.net/problem/25905)

## 설명
10개의 강화망치 중 9개를 선택해 9강에 도달할 확률을 최대화하고, 그 값을 10^9배로 출력하는 문제입니다.

<br>

## 접근법
9강에 도달하려면 9번 모두 성공해야 하므로 확률은 각 단계의 성공 확률 곱입니다.  
성공 확률은 `p_i / x`이고 x는 1~9로 고정이므로 분모는 항상 9!로 같습니다. 따라서 p_i가 큰 9개를 선택해 곱을 최대로 하면 됩니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var p = new double[10];
    for (var i = 0; i < 10; i++)
      p[i] = double.Parse(Console.ReadLine()!);

    Array.Sort(p);
    Array.Reverse(p);

    double prod = 1.0;
    for (var i = 0; i < 9; i++)
      prod *= p[i];

    double fact = 1.0;
    for (var i = 1; i <= 9; i++)
      fact *= i;

    var ans = prod / fact * 1e9;
    Console.WriteLine(ans.ToString("0.000000"));
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

  vector<double> p(10);
  for (int i = 0; i < 10; i++)
    cin >> p[i];

  sort(p.begin(), p.end(), greater<double>());

  double prod = 1.0;
  for (int i = 0; i < 9; i++)
    prod *= p[i];

  double fact = 1.0;
  for (int i = 1; i <= 9; i++)
    fact *= i;

  double ans = prod / fact * 1e9;
  cout << fixed << setprecision(6) << ans << "\n";

  return 0;
}
```
