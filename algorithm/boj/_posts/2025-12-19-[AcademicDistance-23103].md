---
layout: single
title: "[백준 23103] Academic Distance (C#, C++) - soo:bak"
date: "2025-12-19 22:47:00 +0900"
description: 주어진 교실 좌표를 순서대로 이동할 때의 맨해튼 거리 합을 구하는 문제
---

## 문제 링크
[23103번 - Academic Distance](https://www.acmicpc.net/problem/23103)

## 설명
교실 좌표가 순서대로 주어질 때, 전체 이동 거리의 합을 구하는 문제입니다.

이웃한 두 좌표 사이의 거리는 맨해튼 거리로 계산합니다.

<br>

## 접근법
연속한 두 좌표마다 맨해튼 거리를 계산해 누적합니다.

좌표 범위가 작으므로 단순 합산으로 충분합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);

    var prevX = 0;
    var prevY = 0;
    var total = 0;
    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split(' ');
      var x = int.Parse(parts[0]);
      var y = int.Parse(parts[1]);

      if (i > 0)
        total += Math.Abs(prevX - x) + Math.Abs(prevY - y);

      prevX = x;
      prevY = y;
    }

    Console.WriteLine(total);
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

  int n; cin >> n;

  int prevX = 0, prevY = 0;
  int total = 0;
  for (int i = 0; i < n; i++) {
    int x, y; cin >> x >> y;

    if (i > 0)
      total += abs(prevX - x) + abs(prevY - y);

    prevX = x;
    prevY = y;
  }

  cout << total << "\n";

  return 0;
}
```
