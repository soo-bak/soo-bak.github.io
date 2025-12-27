---
layout: single
title: "[백준 6439] 교차 (C#, C++) - soo:bak"
date: "2025-11-15 02:10:00 +0900"
description: 선분과 직사각형이 한 점이라도 공유하는지 CCW와 범위 비교로 판단하는 백준 6439번 교차 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 6439
  - C#
  - C++
  - 알고리즘
keywords: "백준 6439, 백준 6439번, BOJ 6439, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6439번 - 교차](https://www.acmicpc.net/problem/6439)

## 설명

선분과 직사각형이 주어질 때, 두 도형이 한 점이라도 공유하는지 판정하는 문제입니다.<br>

선분의 양 끝점 좌표와 직사각형의 대각 위치에 있는 두 꼭짓점 좌표가 주어집니다. 직사각형의 변은 x축 또는 y축에 평행합니다.<br>

두 도형이 교차한다는 것은 선분이 직사각형의 변과 만나거나, 선분이 완전히 직사각형 내부에 있는 경우를 모두 포함합니다.<br>

교차하면 `T`, 그렇지 않으면 `F`를 출력합니다.<br>

<br>

## 접근법

CCW 기반 선분 교차 판정과 내부 포함 검사를 결합하여 해결합니다.

<br>
입력으로 주어진 대각 두 점으로부터 직사각형의 네 꼭짓점을 구합니다.

좌표의 최솟값과 최댓값을 계산하여 직사각형의 정확한 범위를 정의합니다.

<br>
선분과 직사각형의 네 변 각각에 대해 교차 여부를 판정합니다. CCW 알고리즘을 사용하여 선분 간의 교차를 확인하고, 일직선상에 있는 경우는 구간 겹침을 검사합니다.

<br>
선분이 네 변 모두와 교차하지 않더라도 교차로 판정해야 하는 경우가 있습니다.

선분의 양 끝점이 모두 직사각형 내부에 있다면 선분 전체가 직사각형 안에 포함되므로 교차로 간주합니다.

<br>
네 변 중 하나라도 선분과 교차하거나 선분이 완전히 내부에 있으면 `T`를, 그렇지 않으면 `F`를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    struct Point {
      public long X, Y;
      public Point(long x, long y) { X = x; Y = y; }
    }

    static long CCW(Point a, Point b, Point c) {
      return (b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X);
    }

    static bool Overlap(Point a, Point b, Point c, Point d) {
      if (Compare(b, a) < 0) (a, b) = (b, a);
      if (Compare(d, c) < 0) (c, d) = (d, c);
      return Compare(c, b) <= 0 && Compare(a, d) <= 0;
    }

    static int Compare(Point p1, Point p2) {
      if (p1.X != p2.X) return p1.X.CompareTo(p2.X);
      return p1.Y.CompareTo(p2.Y);
    }

    static bool Intersect(Point a, Point b, Point c, Point d) {
      var abC = CCW(a, b, c);
      var abD = CCW(a, b, d);
      var cdA = CCW(c, d, a);
      var cdB = CCW(c, d, b);

      if (abC == 0 && abD == 0)
        return Overlap(a, b, c, d);

      return (abC * abD <= 0) && (cdA * cdB <= 0);
    }

    static bool Inside(Point p, long minX, long maxX, long minY, long maxY) {
      return p.X >= minX && p.X <= maxX && p.Y >= minY && p.Y <= maxY;
    }

    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      var outputs = new char[t];

      for (var i = 0; i < t; i++) {
        var tokens = Console.ReadLine()!.Split();
        var s = new Point(long.Parse(tokens[0]), long.Parse(tokens[1]));
        var e = new Point(long.Parse(tokens[2]), long.Parse(tokens[3]));
        var a = new Point(long.Parse(tokens[4]), long.Parse(tokens[5]));
        var c = new Point(long.Parse(tokens[6]), long.Parse(tokens[7]));
        var b = new Point(c.X, a.Y);
        var d = new Point(a.X, c.Y);

        var minX = Math.Min(a.X, c.X);
        var maxX = Math.Max(a.X, c.X);
        var minY = Math.Min(a.Y, c.Y);
        var maxY = Math.Max(a.Y, c.Y);

        var intersects = false;
        if (Intersect(s, e, a, b) || Intersect(s, e, b, c) ||
            Intersect(s, e, c, d) || Intersect(s, e, d, a))
          intersects = true;
        else if (Inside(s, minX, maxX, minY, maxY) && Inside(e, minX, maxX, minY, maxY))
          intersects = true;

        outputs[i] = intersects ? 'T' : 'F';
      }

      Console.WriteLine(string.Join("\n", outputs));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

struct Point {
  ll x, y;
};

ll ccw(const Point& a, const Point& b, const Point& c) {
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

int compare(const Point& p1, const Point& p2) {
  if (p1.x != p2.x) return p1.x < p2.x ? -1 : 1;
  if (p1.y != p2.y) return p1.y < p2.y ? -1 : 1;
  return 0;
}

bool overlap(Point a, Point b, Point c, Point d) {
  if (compare(b, a) < 0) swap(a, b);
  if (compare(d, c) < 0) swap(c, d);
  return compare(c, b) <= 0 && compare(a, d) <= 0;
}

bool intersect(Point a, Point b, Point c, Point d) {
  ll abC = ccw(a, b, c);
  ll abD = ccw(a, b, d);
  ll cdA = ccw(c, d, a);
  ll cdB = ccw(c, d, b);

  if (abC == 0 && abD == 0)
    return overlap(a, b, c, d);

  return (abC * abD <= 0) && (cdA * cdB <= 0);
}

bool inside(Point p, ll minX, ll maxX, ll minY, ll maxY) {
  return p.x >= minX && p.x <= maxX && p.y >= minY && p.y <= maxY;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    Point s, e;
    cin >> s.x >> s.y >> e.x >> e.y;
    Point a, c;
    cin >> a.x >> a.y >> c.x >> c.y;
    Point b{c.x, a.y};
    Point d{a.x, c.y};

    ll minX = min(a.x, c.x);
    ll maxX = max(a.x, c.x);
    ll minY = min(a.y, c.y);
    ll maxY = max(a.y, c.y);

    bool intersects = false;
    if (intersect(s, e, a, b) || intersect(s, e, b, c) ||
        intersect(s, e, c, d) || intersect(s, e, d, a))
      intersects = true;
    else if (inside(s, minX, maxX, minY, maxY) && inside(e, minX, maxX, minY, maxY))
      intersects = true;

    cout << (intersects ? "T\n" : "F\n");
  }

  return 0;
}
```

