---
layout: single
title: "[백준 15610] Abbey Courtyard (C#, C++) - soo:bak"
date: "2025-12-08 01:55:00 +0900"
description: 면적이 a인 정사각형의 둘레를 구해 전선 길이를 계산하는 백준 15610번 Abbey Courtyard 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15610
  - C#
  - C++
  - 알고리즘
keywords: "백준 15610, 백준 15610번, BOJ 15610, AbbeyCourtyard, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15610번 - Abbey Courtyard](https://www.acmicpc.net/problem/15610)

## 설명
정사각형 마당의 넓이가 주어질 때, 마당을 둘러싸는 전선의 총 길이를 구하는 문제입니다.

<br>

## 접근법
정사각형의 넓이가 a이면 한 변의 길이는 a의 제곱근입니다. 둘레는 한 변의 4배이므로, 제곱근에 4를 곱하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = double.Parse(Console.ReadLine()!);
    var perim = 4 * Math.Sqrt(a);
    Console.WriteLine(perim.ToString("F6"));
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

  double a; cin >> a;
  cout.setf(ios::fixed);
  cout << setprecision(6) << 4 * sqrt(a) << "\n";

  return 0;
}
```
