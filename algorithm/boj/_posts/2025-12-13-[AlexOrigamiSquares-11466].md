---
layout: single
title: "[백준 11466] Alex Origami Squares (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 한 장의 h×w 직사각형에서 축을 맞춘 정사각형 세 개를 자를 때 만들 수 있는 최대 한 변 길이를 경우 나눠 구하는 백준 11466번 Alex Origami Squares 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11466
  - C#
  - C++
  - 알고리즘
keywords: "백준 11466, 백준 11466번, BOJ 11466, AlexOrigamiSquares, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11466번 - Alex Origami Squares](https://www.acmicpc.net/problem/11466)

## 설명
직사각형 종이에서 같은 크기의 정사각형 세 장을 자를 때, 정사각형 한 변의 최댓값을 구하는 문제입니다.

<br>

## 접근법
먼저 너비가 높이보다 크도록 정렬합니다.

너비가 높이의 세 배 이상이면 정사각형 세 개를 가로로 나란히 배치할 수 있으므로, 한 변은 높이와 같습니다.

너비가 높이의 1.5배보다 크고 세 배보다 작으면 가로 배치 시 너비에 제한을 받으므로, 한 변은 너비를 3으로 나눈 값입니다.

그보다 좁으면 두 개를 세로로 쌓고 옆에 하나를 두는 배치가 최선이므로, 한 변은 높이를 2로 나눈 값입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var h = double.Parse(line[0]);
    var w = double.Parse(line[1]);
    if (w < h) (h, w) = (w, h);

    double ans;
    if (w >= 3 * h) ans = h;
    else if (w > 1.5 * h) ans = w / 3.0;
    else ans = h / 2.0;

    Console.WriteLine($"{ans:F10}");
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

  double h, w; cin >> h >> w;
  if (w < h) swap(w, h);

  double ans;
  if (w >= 3 * h) ans = h;
  else if (w > 1.5 * h) ans = w / 3.0;
  else ans = h / 2.0;

  cout.setf(ios::fixed);
  cout.precision(10);
  cout << ans << "\n";

  return 0;
}
```
