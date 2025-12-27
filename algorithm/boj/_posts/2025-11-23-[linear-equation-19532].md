---
layout: single
title: "[백준 19532] 수학은 비대면강의입니다 (C#, C++) - soo:bak"
date: "2025-11-23 04:05:00 +0900"
description: 2×2 연립방정식을 Cramer의 공식으로 풀어 정수 해를 찾는 백준 19532번 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 19532
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 19532, 백준 19532번, BOJ 19532, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[19532번 - 수학은 비대면강의입니다](https://www.acmicpc.net/problem/19532)

## 설명

두 개의 일차방정식으로 이루어진 연립방정식의 계수가 주어질 때, 정수 해를 구하는 문제입니다.

해가 유일하게 존재하며, 두 해 모두 -999 이상 999 이하의 정수로 보장됩니다.

<br>

## 접근법

2×2 연립방정식은 Cramer의 공식을 이용하여 해를 구합니다.

먼저 첫 번째 방정식의 첫 번째 계수와 두 번째 방정식의 두 번째 계수를 곱한 값에서 첫 번째 방정식의 두 번째 계수와 두 번째 방정식의 첫 번째 계수를 곱한 값을 뺀 행렬식을 계산합니다.

<br>
행렬식이 0이 아니므로 해가 유일하게 존재하며,

각 해는 상수항과 계수들의 곱셈과 뺄셈을 이용하여 구한 값을 행렬식으로 나누어 계산됩니다.

입력 범위가 작고 나눗셈 결과가 항상 정수로 떨어지므로 정수 연산으로 처리합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var a = int.Parse(tokens[0]);
      var b = int.Parse(tokens[1]);
      var c = int.Parse(tokens[2]);
      var d = int.Parse(tokens[3]);
      var e = int.Parse(tokens[4]);
      var f = int.Parse(tokens[5]);

      var det = a * e - b * d;
      var x = (c * e - b * f) / det;
      var y = (a * f - c * d) / det;

      Console.WriteLine($"{x} {y}");
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

  int a, b, c, d, e, f; cin >> a >> b >> c >> d >> e >> f;

  int det = a * e - b * d;
  int x = (c * e - b * f) / det;
  int y = (a * f - c * d) / det;

  cout << x << ' ' << y << '\n';

  return 0;
}
```

