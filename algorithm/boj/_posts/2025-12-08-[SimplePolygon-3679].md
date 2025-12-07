---
layout: single
title: "[백준 3679] 단순 다각형 (C#, C++) - soo:bak"
date: "2025-12-08 01:35:00 +0900"
description: 최좌하단 기준으로 극각 정렬 후 마지막 collinear 구간을 뒤집어 단순 다각형을 만드는 백준 3679번 단순 다각형 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[3679번 - 단순 다각형](https://www.acmicpc.net/problem/3679)

## 설명
**주어진 점들을 모두 꼭짓점으로 갖는 단순 다각형을 만드는 한 가지 순서를 찾는 문제입니다.**

최좌하단 점을 기준점으로 잡아 다른 점들을 극각 기준으로 정렬하면 볼록껍질 순서가 됩니다. 기준점과 일직선상에 있는 점들이 맨 끝에 몰리는데, 이 collinear 구간을 뒤집어주면 선분 교차 없이 모든 점을 잇는 단순 다각형 순서를 얻을 수 있습니다.

<br>

## 접근법
- 입력 순서 index를 함께 저장합니다.
- `y`가 가장 작고 `x`가 가장 작은 점을 기준으로 삼아, 나머지를 CCW(극각) 기준으로 정렬합니다. (동일 각도 시 거리 순)
- 정렬 뒤, 끝에서부터 기준점과 일직선인 구간을 찾아 그 구간을 역순으로 출력합니다.
- 정렬된 순서를 index로 출력하면 조건을 만족하는 다각형이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  struct Point {
    public int idx;
    public long x, y;
  }

  static long Ccw(Point a, Point b, Point c) =>
    a.x * b.y + b.x * c.y + c.x * a.y - (a.y * b.x + b.y * c.x + c.y * a.x);

  static void Main() {
    int T = int.Parse(Console.ReadLine()!);
    while (T-- > 0) {
      var tokens = new Queue<string>(Console.ReadLine()!.Split());
      int n = int.Parse(tokens.Dequeue());
      var pts = new List<Point>(n);
      for (int i = 0; i < n; i++) {
        if (tokens.Count < 2) {
          foreach (var s in Console.ReadLine()!.Split())
            tokens.Enqueue(s);
        }
        long x = long.Parse(tokens.Dequeue());
        long y = long.Parse(tokens.Dequeue());
        pts.Add(new Point { idx = i, x = x, y = y });
      }

      pts.Sort((a, b) => {
        if (a.y != b.y) return a.y.CompareTo(b.y);
        return a.x.CompareTo(b.x);
      });

      Point baseP = pts[0];
      pts.Sort(1, n - 1, Comparer<Point>.Create((a, b) => {
        long cross = Ccw(baseP, a, b);
        if (cross == 0) {
          if (a.x == b.x) return a.y.CompareTo(b.y);
          return a.x.CompareTo(b.x);
        }
        return cross > 0 ? -1 : 1; // CCW 먼저
      }));

      int idx = n - 2;
      while (idx >= 0 && Ccw(baseP, pts[idx], pts[idx + 1]) == 0) idx--;

      var output = new List<int>(n);
      for (int i = 0; i <= idx; i++) output.Add(pts[i].idx);
      for (int i = n - 1; i > idx; i--) output.Add(pts[i].idx);

      Console.WriteLine(string.Join(" ", output));
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Point {
  int idx;
  ll x, y;
};

ll ccw(const Point& a, const Point& b, const Point& c) {
  return a.x * b.y + b.x * c.y + c.x * a.y - (a.y * b.x + b.y * c.x + c.y * a.x);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int T; cin >> T;
  while (T--) {
    int n; cin >> n;
    vector<Point> p(n);
    for (int i = 0; i < n; i++) {
      cin >> p[i].x >> p[i].y;
      p[i].idx = i;
    }

    sort(p.begin(), p.end(), [](const Point& a, const Point& b) {
      if (a.y != b.y) return a.y < b.y;
      return a.x < b.x;
    });
    Point base = p[0];

    sort(p.begin() + 1, p.end(), [&](const Point& a, const Point& b) {
      ll cross = ccw(base, a, b);
      if (cross == 0) {
        if (a.x != b.x) return a.x < b.x;
        return a.y < b.y;
      }
      return cross > 0;
    });

    int idx = n - 2;
    while (idx >= 0 && ccw(base, p[idx], p[idx + 1]) == 0) idx--;

    for (int i = 0; i <= idx; i++) cout << p[i].idx << " ";
    for (int i = n - 1; i > idx; i--) {
      cout << p[i].idx;
      if (i > 0) cout << " ";
    }
    cout << "\n";
  }
  return 0;
}
```
