---
layout: single
title: "[백준 25985] Fastestest Function (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 25985번 C#, C++ 풀이 - 최적화 전후 전체 비중 x, y로부터 함수가 얼마나 빨라졌는지 비율을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 25985
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 25985, 백준 25985번, BOJ 25985, FastestestFunction, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25985번 - Fastestest Function](https://www.acmicpc.net/problem/25985)

## 설명
최적화 전후에 전체 실행 시간 중 foo가 차지하는 비율이 주어질 때, foo가 얼마나 빨라졌는지 배율을 구하는 문제입니다.

<br>

## 접근법
최적화 전후 비율에서 나머지 시간은 동일하다는 점을 이용합니다. 두 비율 관계식을 정리하면 최적화 전후 시간의 배율을 구할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var x = double.Parse(parts[0]);
    var y = double.Parse(parts[1]);

    var p = x / 100.0;
    var q = y / 100.0;
    var factor = p * (1 - q) / (q * (1 - p));

    Console.WriteLine(factor.ToString("0.###############"));
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
  double p = x / 100.0;
  double q = y / 100.0;
  double factor = p * (1 - q) / (q * (1 - p));

  cout << fixed << setprecision(10) << factor << "\n";

  return 0;
}
```
