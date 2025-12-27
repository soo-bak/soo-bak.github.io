---
layout: single
title: "[백준 20215] Cutting Corners (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 직사각형 모서리 w×h를 자를 때 직선 두 번 길이에서 대각선 길이를 뺀 값을 구하는 백준 20215번 Cutting Corners 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 20215
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
  - pythagoras
keywords: "백준 20215, 백준 20215번, BOJ 20215, CuttingCorners, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20215번 - Cutting Corners](https://www.acmicpc.net/problem/20215)

## 설명
직사각형 모서리를 자를 때, 직각으로 두 번 자르는 것과 대각선으로 한 번 자르는 것의 길이 차이를 구하는 문제입니다.

<br>

## 접근법
직각으로 자르면 두 변을 따라 w + h만큼 이동합니다.

대각선으로 자르면 피타고라스 정리에 의해 w와 h를 각각 제곱한 값의 합의 제곱근만큼 이동합니다.

두 값의 차이를 소수점 아래 여섯 자리까지 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var w = double.Parse(line[0]);
    var h = double.Parse(line[1]);
    var ans = w + h - Math.Sqrt(w * w + h * h);
    Console.WriteLine($"{ans:F6}");
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

  double w, h; cin >> w >> h;
  double ans = w + h - sqrt(w * w + h * h);
  cout.setf(ios::fixed);
  cout.precision(6);
  cout << ans << "\n";

  return 0;
}
```
