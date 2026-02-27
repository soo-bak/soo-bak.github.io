---
layout: single
title: "[백준 4697] Fifty Coats of Gray (C#, C++) - soo:bak"
date: "2026-02-27 09:21:00 +0900"
description: "백준 4697번 C#, C++ 풀이 - 아파트 여러 세대의 벽과 천장을 칠하는 데 필요한 페인트 통 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 4697
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 4697, 백준 4697번, BOJ 4697, Fifty Coats of Gray, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4697번 - Fifty Coats of Gray](https://www.acmicpc.net/problem/4697)

## 설명
같은 구조의 아파트 여러 세대에 대해 네 벽과 천장을 칠하려고 할 때, 창문과 문 넓이를 제외한 전체 면적을 구해 필요한 페인트 통 수를 계산하는 문제입니다.

<br>

## 접근법
한 세대에서 칠해야 할 면적은 네 벽의 넓이와 천장 넓이를 더한 뒤, 창문과 문이 차지하는 넓이를 빼서 구할 수 있습니다. 여기에 세대 수를 곱하면 전체 면적이 됩니다.

페인트는 한 통당 일정 면적을 칠할 수 있으므로, 전체 면적을 한 통이 덮는 면적으로 나눈 뒤 올림하여 필요한 통 수를 구하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      var p = Console.ReadLine()!.Split();
      var n = int.Parse(p[0]);
      var width = int.Parse(p[1]);
      var length = int.Parse(p[2]);
      var height = int.Parse(p[3]);
      var area = int.Parse(p[4]);
      var m = int.Parse(p[5]);

      if (n == 0 && width == 0 && length == 0 && height == 0 && area == 0 && m == 0)
        break;

      var openings = 0;
      for (var i = 0; i < m; i++) {
        var q = Console.ReadLine()!.Split();
        var w = int.Parse(q[0]);
        var h = int.Parse(q[1]);
        openings += w * h;
      }

      var walls = 2 * height * (width + length);
      var ceiling = width * length;
      var oneRoom = walls + ceiling - openings;
      var total = oneRoom * n;
      var answer = (total + area - 1) / area;

      Console.WriteLine(answer);
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

  while (true) {
    int n, width, length, height, area, m;
    cin >> n >> width >> length >> height >> area >> m;

    if (n == 0 && width == 0 && length == 0 && height == 0 && area == 0 && m == 0)
      break;

    int openings = 0;
    for (int i = 0; i < m; i++) {
      int w, h;
      cin >> w >> h;
      openings += w * h;
    }

    int walls = 2 * height * (width + length);
    int ceiling = width * length;
    int one_room = walls + ceiling - openings;
    int total = one_room * n;
    int answer = (total + area - 1) / area;

    cout << answer << "\n";
  }

  return 0;
}
```
