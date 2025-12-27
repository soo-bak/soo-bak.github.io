---
layout: single
title: "[백준 15028] Breaking Biscuits (C#, C++) - soo:bak"
date: "2025-12-07 00:10:00 +0900"
description: 볼록 다각형의 최소 폭을 구해 필요한 머그 지름을 계산하는 백준 15028번 Breaking Biscuits 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15028
  - C#
  - C++
  - 알고리즘
  - 기하학
  - convex_hull
  - rotating_calipers
keywords: "백준 15028, 백준 15028번, BOJ 15028, BreakingBiscuits, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15028번 - Breaking Biscuits](https://www.acmicpc.net/problem/15028)

## 설명
평면 상 볼록 다각형이 주어집니다. 다각형을 어떤 각도로 회전해도 완전히 담을 수 있는 원형 컵의 최소 지름을 구하는 문제입니다.

이는 다각형의 최소 폭과 같습니다. 최소 폭이란 다각형을 두 평행선 사이에 끼웠을 때, 그 간격이 가장 좁아지는 방향에서의 간격입니다.

<br>

## 접근법
다각형의 최소 폭은 항상 볼록 껍질의 어떤 변과 평행한 방향에서 나타납니다. 따라서 볼록 껍질을 구한 뒤, 각 변에 대해 그 변과 가장 먼 점까지의 수직 거리를 계산하면 됩니다.

먼저, 볼록 껍질을 구합니다. 점들을 x 좌표 기준으로 정렬하고, 정렬된 점들을 양 방향으로 순회하면서 아래 껍질과 위 껍질을 만듭니다. 새 점을 추가할 때 꺾이는 방향이 볼록하지 않으면 이전 점을 제거합니다.

다음으로, 각 변에 대해 가장 먼 점을 찾습니다. 변을 다음 변으로 이동하면 가장 먼 점도 같은 방향으로만 움직입니다. 따라서 껍질을 한 바퀴 도는 동안 가장 먼 점도 한 바퀴만 돌면 됩니다.

이후, 각 변마다 그 변에서 가장 먼 점까지의 수직 거리를 계산합니다. 이 거리는 외적의 절댓값을 변의 길이로 나눈 값입니다. 모든 변에 대해 이 값을 구하고 그 중 최솟값이 다각형의 최소 폭입니다.

최소 폭이 곧 필요한 컵의 지름이므로 이를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  struct Point {
    public long X, Y;
    public Point(long x, long y) { X = x; Y = y; }
  }

  class Program {
    static long Cross(Point a, Point b, Point c) {
      return (b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X);
    }

    static List<Point> ConvexHull(List<Point> pts) {
      pts.Sort((p1, p2) => {
        var cx = p1.X.CompareTo(p2.X);
        return cx != 0 ? cx : p1.Y.CompareTo(p2.Y);
      });
      pts = pts.Distinct().ToList();
      if (pts.Count <= 2)
        return pts;

      var lower = new List<Point>();
      foreach (var p in pts) {
        while (lower.Count >= 2 && Cross(lower[lower.Count - 2], lower[lower.Count - 1], p) <= 0)
          lower.RemoveAt(lower.Count - 1);
        lower.Add(p);
      }
      var upper = new List<Point>();
      for (var i = pts.Count - 1; i >= 0; i--) {
        var p = pts[i];
        while (upper.Count >= 2 && Cross(upper[upper.Count - 2], upper[upper.Count - 1], p) <= 0)
          upper.RemoveAt(upper.Count - 1);
        upper.Add(p);
      }
      lower.RemoveAt(lower.Count - 1);
      upper.RemoveAt(upper.Count - 1);
      lower.AddRange(upper);
      return lower;
    }

    static double MinWidth(List<Point> h) {
      var n = h.Count;
      if (n == 2)
        return 0.0;

      var j = 1;
      var best = double.MaxValue;
      for (var i = 0; i < n; i++) {
        var ni = (i + 1) % n;
        var dx = h[ni].X - h[i].X;
        var dy = h[ni].Y - h[i].Y;
        var edgeLen = Math.Sqrt((double)dx * dx + (double)dy * dy);

        while (true) {
          var nj = (j + 1) % n;
          var cur = Math.Abs(Cross(h[i], h[ni], h[j]));
          var nxt = Math.Abs(Cross(h[i], h[ni], h[nj]));
          if (nxt > cur)
            j = nj;
          else
            break;
        }
        var width = Math.Abs(Cross(h[i], h[ni], h[j])) / edgeLen;
        if (width < best)
          best = width;
      }
      return best;
    }

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var pts = new List<Point>(n);
      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!.Split();
        pts.Add(new Point(long.Parse(s[0]), long.Parse(s[1])));
      }

      var hull = ConvexHull(pts);
      var ans = MinWidth(hull);
      Console.WriteLine(ans.ToString("0.000000"));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<ll> vl;

struct Point {
  ll x, y;
  bool operator<(const Point& other) const {
    if (x != other.x)
      return x < other.x;
    return y < other.y;
  }
  bool operator==(const Point& other) const {
    return x == other.x && y == other.y;
  }
};

typedef vector<Point> vp;

ll cross(const Point& a, const Point& b, const Point& c) {
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

vp convexHull(vp p) {
  sort(p.begin(), p.end());
  p.erase(unique(p.begin(), p.end()), p.end());
  if (p.size() <= 2)
    return p;

  vp lower, upper;
  for (auto& pt : p) {
    while (lower.size() >= 2 && cross(lower[lower.size() - 2], lower[lower.size() - 1], pt) <= 0)
      lower.pop_back();
    lower.push_back(pt);
  }
  for (int i = (int)p.size() - 1; i >= 0; i--) {
    auto pt = p[i];
    while (upper.size() >= 2 && cross(upper[upper.size() - 2], upper[upper.size() - 1], pt) <= 0)
      upper.pop_back();
    upper.push_back(pt);
  }
  lower.pop_back();
  upper.pop_back();
  lower.insert(lower.end(), upper.begin(), upper.end());
  return lower;
}

double minWidth(const vp& h) {
  int n = (int)h.size();
  if (n == 2)
    return 0.0;

  int j = 1;
  double best = numeric_limits<double>::max();
  for (int i = 0; i < n; i++) {
    int ni = (i + 1) % n;
    ll dx = h[ni].x - h[i].x;
    ll dy = h[ni].y - h[i].y;
    double edgeLen = sqrt((double)dx * dx + (double)dy * dy);

    while (true) {
      int nj = (j + 1) % n;
      ll cur = llabs(cross(h[i], h[ni], h[j]));
      ll nxt = llabs(cross(h[i], h[ni], h[nj]));
      if (nxt > cur)
        j = nj;
      else
        break;
    }
    double width = llabs(cross(h[i], h[ni], h[j])) / edgeLen;
    if (width < best)
      best = width;
  }
  return best;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vp p(n);
  for (int i = 0; i < n; i++)
    cin >> p[i].x >> p[i].y;

  auto hull = convexHull(p);
  double ans = minWidth(hull);

  cout << fixed << setprecision(6) << ans << "\n";

  return 0;
}
```
