---
layout: single
title: "[백준 25869] Window on the Wall (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 25869번 C#, C++ 풀이 - 벽과 창문 사이 최소 여백이 주어질 때 설치 가능한 최대 창문 넓이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 25869
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 25869, 백준 25869번, BOJ 25869, WindowOnTheWall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25869번 - Window on the Wall](https://www.acmicpc.net/problem/25869)

## 설명
직사각형 벽의 가로·세로와 창문 테두리와 벽 테두리 사이 필요한 최소 여백 d가 주어질 때, 설치 가능한 최대 직사각형 창문의 넓이를 구하는 문제입니다. 여백을 두면 창문의 가로는 w-2d, 세로는 h-2d가 됩니다.

<br>

## 접근법
창문은 벽의 상하좌우 테두리에서 각각 d만큼 떨어져야 합니다. 따라서 창문의 가로는 벽의 가로에서 2d를 뺀 값이고, 세로도 마찬가지입니다.

계산된 가로나 세로가 0 이하라면 창문을 설치할 수 없으므로 0을 출력하고, 둘 다 양수라면 두 값을 곱한 넓이를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var w = long.Parse(parts[0]);
    var h = long.Parse(parts[1]);
    var d = long.Parse(parts[2]);

    var ww = w - 2 * d;
    var hh = h - 2 * d;

    if (ww <= 0 || hh <= 0) Console.WriteLine(0);
    else Console.WriteLine(ww * hh);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll w, h, d; cin >> w >> h >> d;

  ll ww = w - 2 * d;
  ll hh = h - 2 * d;

  if (ww <= 0 || hh <= 0) cout << 0 << "\n";
  else cout << ww * hh << "\n";

  return 0;
}
```
