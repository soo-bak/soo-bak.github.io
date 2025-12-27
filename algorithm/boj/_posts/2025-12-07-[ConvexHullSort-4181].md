---
layout: single
title: "[백준 4181] Convex Hull (C#, C++) - soo:bak"
date: "2025-12-07 03:45:00 +0900"
description: 볼록 껍질에 속하는 점들을 반시계 방향 순서로 정렬하는 백준 4181번 Convex Hull 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 4181
  - C#
  - C++
  - 알고리즘
keywords: "백준 4181, 백준 4181번, BOJ 4181, ConvexHullSort, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4181번 - Convex Hull](https://www.acmicpc.net/problem/4181)

## 설명
볼록 껍질에 속하는 점들이 표시되어 주어질 때, 이 점들을 반시계 방향 순서로 정렬하여 출력하는 문제입니다. 시작점은 x 좌표가 가장 작은 점이며, x 좌표가 같다면 y 좌표가 가장 작은 점입니다.

<br>

## 접근법
먼저 볼록 껍질에 속하는 점들만 모읍니다. 그 중에서 x 좌표가 가장 작고, 같다면 y 좌표가 가장 작은 점을 기준점으로 선택합니다. 이 점이 출력의 시작점이 됩니다.

기준점을 제외한 나머지 점들을 기준점에서 바라본 각도 순으로 정렬합니다. 세 점의 방향을 판별하는 외적을 사용하여, 기준점에서 봤을 때 반시계 방향에 있는 점이 앞에 오도록 합니다. 같은 각도에 여러 점이 있다면 기준점과 가까운 점이 먼저 오도록 정렬합니다.

정렬된 점들을 순서대로 처리하며 볼록 껍질을 구성합니다. 새 점을 추가할 때 직전 두 점과 새 점이 시계 방향을 이루면 직전 점을 제거합니다. 이 문제에서는 일직선상의 점들도 모두 포함해야 하므로, 엄격한 시계 방향일 때만 제거합니다.

결과로 나온 점들이 반시계 방향 순서로 정렬된 볼록 껍질입니다.

<br>

- - -

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static List<(long x, long y)> v = new List<(long, long)>();
  static (long x, long y) pivot;

  static long Ccw(long x1, long y1, long x2, long y2, long x3, long y3) {
    return (x1 * y2 + x2 * y3 + x3 * y1) - (y1 * x2 + y2 * x3 + y3 * x1);
  }

  static int CompCCW((long x, long y) a, (long x, long y) b) {
    var crossP = Ccw(pivot.x, pivot.y, a.x, a.y, b.x, b.y);
    if (crossP == 0) {
      if (a.x == b.x) return b.y.CompareTo(a.y);
      else if (a.y == b.y) return a.x.CompareTo(b.x);
      else return b.y.CompareTo(a.y);
    }
    return crossP > 0 ? -1 : 1;
  }

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < n; i++) {
      var s = Console.ReadLine()!.Split();
      var x = long.Parse(s[0]);
      var y = long.Parse(s[1]);
      var c = s[2][0];
      if (c == 'Y') v.Add((x, y));
    }

    v.Sort((a, b) => a.x != b.x ? a.x.CompareTo(b.x) : a.y.CompareTo(b.y));
    pivot = v[0];
    v.Sort(1, v.Count - 1, Comparer<(long x, long y)>.Create(CompCCW));

    var convex = new List<(long x, long y)>();
    convex.Add(v[0]);
    convex.Add(v[1]);
    for (var i = 2; i < v.Count; i++) {
      while (true) {
        if (convex.Count < 2) break;
        var a = convex[convex.Count - 1];
        convex.RemoveAt(convex.Count - 1);
        var b = convex[convex.Count - 1];
        var crossP = Ccw(v[i].x, v[i].y, a.x, a.y, b.x, b.y);
        if (crossP <= 0) {
          convex.Add(a);
          break;
      }
      }
      convex.Add(v[i]);
    }

    Console.WriteLine(convex.Count);
    foreach (var p in convex)
      Console.WriteLine($"{p.x} {p.y}");
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<ll, ll> pll;
typedef vector<pll> vp;

vp v;

ll ccw(ll x1, ll y1, ll x2, ll y2, ll x3, ll y3) {
  return (x1 * y2 + x2 * y3 + x3 * y1) - (y1 * x2 + y2 * x3 + y3 * x1);
}

bool comp(const pll& a, const pll& b) {
  if (a.first == b.first) return a.second < b.second;
  return a.first < b.first;
}

bool compCCW(const pll& a, const pll& b) {
  ll crossP = ccw(v[0].first, v[0].second, a.first, a.second, b.first, b.second);
  if (!crossP) {
    if (a.first == b.first) return a.second > b.second;
    else if (a.second == b.second) return a.first < b.first;
    else return a.second > b.second;
  }
  return crossP > 0;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  for (int i = 0; i < n; i++) {
    int x, y; char c; cin >> x >> y >> c;
    if (c == 'Y') v.push_back({x, y});
  }

  sort(v.begin(), v.end(), comp);
  sort(v.begin() + 1, v.end(), compCCW);

  vp convex;
  convex.push_back(v[0]);
  convex.push_back(v[1]);
  for (size_t i = 2; i < v.size(); i++) {
    while (true) {
      if (convex.size() < 2) break;
      pll a = convex.back();
      convex.pop_back();
      pll b = convex.back();
      ll crossP = ccw(v[i].first, v[i].second, a.first, a.second, b.first, b.second);
      if (crossP <= 0) {
        convex.push_back(a);
        break;
    }
    }
    convex.push_back(v[i]);
  }

  cout << convex.size() << "\n";
  for (size_t i = 0; i < convex.size(); i++)
    cout << convex[i].first << " " << convex[i].second << "\n";

  return 0;
}
```
