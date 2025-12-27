---
layout: single
title: "[백준 2110] 공유기 설치 (C#, C++) - soo:bak"
date: "2025-12-07 23:14:00 +0900"
description: 집에 공유기를 설치할 때 가장 인접한 두 공유기 사이의 거리를 최대화하는 백준 2110번 공유기 설치 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2110
  - C#
  - C++
  - 알고리즘
keywords: "백준 2110, 백준 2110번, BOJ 2110, RouterInstall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2110번 - 공유기 설치](https://www.acmicpc.net/problem/2110)

## 설명
N개의 집에 C개의 공유기를 설치할 때, 가장 인접한 두 공유기 사이의 거리를 최대화하는 문제입니다. 예를 들어 좌표 1, 2, 4, 8, 9에 3개를 설치한다면 1, 4, 8에 설치하여 최소 거리 3을 얻을 수 있습니다.

<br>

## 접근법
먼저 집의 좌표를 정렬합니다. 이분 탐색으로 가능한 최소 거리의 최댓값을 찾습니다. 탐색 범위는 1부터 양 끝 집 사이의 거리까지입니다.

특정 거리가 가능한지 판별할 때는 첫 번째 집에 공유기를 설치하고, 이후 직전에 설치한 집과의 거리가 해당 거리 이상인 집에만 설치합니다. 이렇게 설치한 공유기 개수가 C개 이상이면 해당 거리는 가능합니다.

가능하면 더 큰 거리를 탐색하고, 불가능하면 더 작은 거리를 탐색합니다. 탐색이 끝났을 때 가능했던 최대 거리가 답입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var c = int.Parse(parts[1]);
    var pos = new int[n];
    for (var i = 0; i < n; i++)
      pos[i] = int.Parse(Console.ReadLine()!);

    Array.Sort(pos);

    var lo = 1;
    var hi = pos[n - 1] - pos[0];
    var ans = 0;
    while (lo <= hi) {
      var mid = (lo + hi) / 2;
      var placed = 1;
      var prev = pos[0];
      for (var i = 1; i < n; i++) {
        if (pos[i] - prev >= mid) {
          placed++;
          prev = pos[i];
        }
      }

      if (placed >= c) {
        ans = mid;
        lo = mid + 1;
      } else hi = mid - 1;
    }

    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, c; cin >> n >> c;
  vi v(n);
  for (int i = 0; i < n; i++) cin >> v[i];
  sort(v.begin(), v.end());

  int lo = 1, hi = v.back() - v.front(), ans = 0;
  while (lo <= hi) {
    int mid = (lo + hi) / 2;
    int placed = 1, prev = v[0];
    for (int i = 1; i < n; i++) {
      if (v[i] - prev >= mid) {
        placed++;
        prev = v[i];
      }
    }

    if (placed >= c) {
      ans = mid;
      lo = mid + 1;
    } else hi = mid - 1;
  }

  cout << ans << "\n";

  return 0;
}
```
