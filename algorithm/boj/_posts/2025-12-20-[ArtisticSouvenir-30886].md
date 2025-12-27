---
layout: single
title: "[백준 30886] Artistic Souvenir (C#, C++) - soo:bak"
date: "2025-12-20 12:12:00 +0900"
description: 원형 무늬 면적이 주어질 때 1cm 여백을 두고 담을 최소 정사각형 타일의 면적을 구하는 문제
tags:
  - 백준
  - BOJ
  - 30886
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
  - arithmetic
keywords: "백준 30886, 백준 30886번, BOJ 30886, ArtisticSouvenir, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30886번 - Artistic Souvenir](https://www.acmicpc.net/problem/30886)

## 설명
원형 무늬의 면적이 주어질 때, 사방 1cm 여백을 두고 담을 수 있는 최소 정사각형 타일의 면적을 구하는 문제입니다.

<br>

## 접근법
먼저 원의 면적으로부터 반지름을 구합니다.

다음으로 지름에 양쪽 여백 2cm를 더해 정사각형 한 변의 길이를 계산합니다.

이후 한 변의 길이를 제곱하여 면적을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = double.Parse(Console.ReadLine()!);
    var r = Math.Sqrt(a / Math.PI);
    var side = 2.0 * (r + 1.0);
    var area = side * side;
    Console.WriteLine(area.ToString("F10"));
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
  double r = sqrt(a / acos(-1.0));
  double side = 2.0 * (r + 1.0);
  double area = side * side;
  cout << fixed << setprecision(10) << area << "\n";

  return 0;
}
```
