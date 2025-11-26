---
layout: single
title: "[백준 10255] 교차점 (C#, C++) - soo:bak"
date: "2025-11-27 00:09:00 +0900"
description: 축에 평행한 사각형 경계와 임의의 선분의 교차 개수를 CCW와 중복 제거로 구하고, 겹치는 경우 4를 출력하는 백준 10255번 교차점 문제의 C# 및 C++ 풀이
---

## 문제 링크
[10255번 - 교차점](https://www.acmicpc.net/problem/10255)

## 설명

좌표 평면에서 축에 평행한 사각형과 임의의 선분이 주어질 때, 사각형의 경계선과 선분의 교차점 개수를 구하는 문제입니다.

여러 테스트 케이스가 주어지며, 각 테스트 케이스마다 사각형의 왼쪽 아래 꼭짓점과 오른쪽 위 꼭짓점, 그리고 선분의 양 끝점이 주어집니다.

교차점이 0개, 1개, 2개인 경우 그 개수를 출력하고, 선분이 사각형의 변과 일부 구간 겹쳐 교차점이 무한히 많은 경우 4를 출력합니다.

<br>

## 접근법

사각형을 네 개의 변(아래, 오른쪽, 위, 왼쪽)으로 나누고, 주어진 선분과 각 변의 교차 여부를 순서대로 확인합니다.

두 선분의 교차를 판단하기 위해 CCW(Counter-Clockwise) 알고리듬을 사용합니다.

먼저 두 선분이 일직선상에 있는지 확인하고, 일직선상에 있으면서 겹치는 구간이 한 점이 아닌 경우 교차점이 무한히 많으므로 즉시 4를 출력합니다.

<br>
두 선분이 일직선상에 있지 않고 교차하는 경우, 교점의 좌표를 계산하여 저장합니다.

사각형의 꼭짓점에서는 인접한 두 변이 모두 선분과 교차할 수 있으므로, 같은 교점이 중복으로 계산될 수 있습니다.

이를 방지하기 위해 각 교점을 저장할 때, 이미 저장된 교점들과 비교하여 좌표 차이가 매우 작으면(1e-9 이하) 같은 점으로 간주하고 중복을 제거합니다.

<br>
예를 들어, 사각형이 (0,0)-(2,0)-(2,2)-(0,2)이고 선분이 (1,-1)-(1,3)인 경우, 선분은 아래 변 (0,0)-(2,0)과 (1,0)에서 만나고 위 변 (0,2)-(2,2)과 (1,2)에서 만나므로 교차점이 2개입니다.

만약 선분이 (0,0)-(2,0)으로 아래 변과 완전히 겹친다면, 교차점이 무한히 많으므로 4를 출력합니다.

<br>
네 변을 모두 확인한 후, 무한 교차가 발견되지 않았다면 중복 제거된 교점의 개수를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;

namespace Solution {
  struct Point {
    public long X, Y;
    public Point(long x, long y) { X = x; Y = y; }
  }

  class Program {
    const double EPS = 1e-9;

    static long Ccw(Point a, Point b, Point c) {
      long v = a.X * b.Y + b.X * c.Y + c.X * a.Y;
      v -= a.Y * b.X + b.Y * c.X + c.Y * a.X;
      if (v > 0) return 1;
      if (v < 0) return -1;
      return 0;
    }

    static bool Overlap1D(long a1, long a2, long b1, long b2) {
      if (a1 > a2) (a1, a2) = (a2, a1);
      if (b1 > b2) (b1, b2) = (b2, b1);
      return Math.Max(a1, b1) <= Math.Min(a2, b2);
    }

    static int Relation(Point a, Point b, Point c, Point d, out (double x, double y) pt, out bool infinite) {
      pt = (0, 0); infinite = false;
      long ab_ccw_c = Ccw(a, b, c);
      long ab_ccw_d = Ccw(a, b, d);
      long cd_ccw_a = Ccw(c, d, a);
      long cd_ccw_b = Ccw(c, d, b);

      bool colA = ab_ccw_c == 0 && ab_ccw_d == 0;
      if (colA) {
        bool xOverlap = Overlap1D(a.X, b.X, c.X, d.X);
        bool yOverlap = Overlap1D(a.Y, b.Y, c.Y, d.Y);
        if (xOverlap && yOverlap) {
          // 겹침: 무한 또는 한 점
          long maxStartX = Math.Max(Math.Min(a.X, b.X), Math.Min(c.X, d.X));
          long minEndX = Math.Min(Math.Max(a.X, b.X), Math.Max(c.X, d.X));
          long maxStartY = Math.Max(Math.Min(a.Y, b.Y), Math.Min(c.Y, d.Y));
          long minEndY = Math.Min(Math.Max(a.Y, b.Y), Math.Max(c.Y, d.Y));
          if (maxStartX == minEndX && maxStartY == minEndY) {
            pt = (maxStartX, maxStartY); return 1;
          }
          infinite = true; return 2;
        }
        return 0;
      }

      if (ab_ccw_c * ab_ccw_d > 0 || cd_ccw_a * cd_ccw_b > 0) return 0;

      double x1 = a.X, y1 = a.Y, x2 = b.X, y2 = b.Y;
      double x3 = c.X, y3 = c.Y, x4 = d.X, y4 = d.Y;
      double den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
      double px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den;
      double py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den;
      pt = (px, py);
      return 1;
    }

    static bool SamePoint((double x, double y) a, (double x, double y) b) {
      return Math.Abs(a.x - b.x) < EPS && Math.Abs(a.y - b.y) < EPS;
    }

    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);

      while (t-- > 0) {
        var rect = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
        var seg = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);

        var r1 = new Point(rect[0], rect[1]);
        var r2 = new Point(rect[2], rect[1]);
        var r3 = new Point(rect[2], rect[3]);
        var r4 = new Point(rect[0], rect[3]);

        var s1 = new Point(seg[0], seg[1]);
        var s2 = new Point(seg[2], seg[3]);

        var edges = new List<(Point a, Point b)> { (r1, r2), (r2, r3), (r3, r4), (r4, r1) };
        var infinite = false;
        var points = new List<(double x, double y)>();

        foreach (var e in edges) {
          var rel = Relation(s1, s2, e.a, e.b, out var p, out var inf);

          if (inf) {
            infinite = true;
            break;
          }

          if (rel == 1) {
            var dup = false;

            foreach (var q in points)
              if (SamePoint(q, p)) {
                dup = true;
                break;
              }

            if (!dup) points.Add(p);
          }
        }

        if (infinite) Console.WriteLine(4);
        else Console.WriteLine(points.Count);
      }
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<double, double> pdd;

struct Point { ll x, y; };

const double EPS = 1e-9;

ll ccw(const Point& a, const Point& b, const Point& c) {
  ll v = a.x * b.y + b.x * c.y + c.x * a.y;
  v -= a.y * b.x + b.y * c.x + c.y * a.x;

  if (v > 0) return 1;
  if (v < 0) return -1;

  return 0;
}

bool overlap1D(ll a1, ll a2, ll b1, ll b2) {
  if (a1 > a2) swap(a1, a2);
  if (b1 > b2) swap(b1, b2);

  return max(a1, b1) <= min(a2, b2);
}

int relation(const Point& a, const Point& b, const Point& c, const Point& d, pdd& pt, bool& infinite) {
  pt = {0, 0};
  infinite = false;

  ll ab_c = ccw(a, b, c), ab_d = ccw(a, b, d);
  ll cd_a = ccw(c, d, a), cd_b = ccw(c, d, b);

  bool col = (ab_c == 0 && ab_d == 0);

  if (col) {
    bool xo = overlap1D(a.x, b.x, c.x, d.x);
    bool yo = overlap1D(a.y, b.y, c.y, d.y);

    if (xo && yo) {
      ll xs = max(min(a.x, b.x), min(c.x, d.x));
      ll xe = min(max(a.x, b.x), max(c.x, d.x));
      ll ys = max(min(a.y, b.y), min(c.y, d.y));
      ll ye = min(max(a.y, b.y), max(c.y, d.y));

      if (xs == xe && ys == ye) {
        pt = {(double)xs, (double)ys};
        return 1;
      }

      infinite = true;
      return 2;
    }

    return 0;
  }

  if (ab_c * ab_d > 0 || cd_a * cd_b > 0) return 0;

  double x1 = a.x, y1 = a.y, x2 = b.x, y2 = b.y;
  double x3 = c.x, y3 = c.y, x4 = d.x, y4 = d.y;
  double den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4);
  double px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den;
  double py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den;

  pt = {px, py};

  return 1;
}

bool samePoint(const pdd& a, const pdd& b) {
  return fabs(a.first - b.first) < EPS && fabs(a.second - b.second) < EPS;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    ll xmin, ymin, xmax, ymax; cin >> xmin >> ymin >> xmax >> ymax;

    Point r1{xmin, ymin}, r2{xmax, ymin}, r3{xmax, ymax}, r4{xmin, ymax};
    Point s1, s2; cin >> s1.x >> s1.y >> s2.x >> s2.y;

    vector<pair<Point, Point>> edges = {{r1, r2}, {r2, r3}, {r3, r4}, {r4, r1}};
    bool infinite = false;
    vector<pdd> pts;

    for (auto& e : edges) {
      pdd p;
      bool inf;
      int rel = relation(s1, s2, e.first, e.second, p, inf);

      if (inf) {
        infinite = true;
        break;
      }

      if (rel == 1) {
        bool dup = false;

        for (auto& q : pts)
          if (samePoint(p, q)) {
            dup = true;
            break;
          }

        if (!dup) pts.push_back(p);
      }
    }

    if (infinite) cout << 4 << "\n";
    else cout << pts.size() << "\n";
  }

  return 0;
}
```

