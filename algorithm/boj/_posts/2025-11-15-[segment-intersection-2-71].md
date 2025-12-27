---
layout: single
title: "[백준 17387] 선분 교차 2 (C#, C++) - soo:bak"
date: "2025-11-15 00:58:00 +0900"
description: 교차판별과 선분 겹침까지 포함하는 CCW 기반 로직을 구현한 백준 17387번 선분 교차 2 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17387
  - C#
  - C++
  - 알고리즘
keywords: "백준 17387, 백준 17387번, BOJ 17387, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17387번 - 선분 교차 2](https://www.acmicpc.net/problem/17387)

## 설명

두 선분이 주어졌을 때 교차하는지 판정하는 문제입니다.<br>

두 선분의 끝점끼리 만나거나 한 선분이 다른 선분 위에 일부 겹치는 경우도 교차로 판정합니다.<br>

CCW 알고리즘으로 선분 간의 위치 관계를 판별하며, 일직선상에 있는 경우는 선분 구간의 겹침을 추가로 확인합니다.<br>

<br>

## 접근법

CCW를 사용하여 선분의 교차를 판정합니다.

선분 `AB`와 선분 `CD`에 대해 네 개의 CCW 값을 구합니다.

점 `C`와 `D`가 선분 `AB`를 기준으로 어느 방향에 있는지, 점 `A`와 `B`가 선분 `CD`를 기준으로 어느 방향에 있는지를 각각 계산합니다.

<br>
CCW 값들 중 하나라도 `0`이 있다면 일직선이거나 끝점이 만나는 경우입니다.

이때는 각 선분의 시작점과 끝점을 정렬한 후, 두 선분의 좌표 구간이 겹치는지 확인하여 교차를 판정합니다.

<br>
CCW 값이 모두 `0`이 아닌 경우, 각 선분을 기준으로 상대 선분의 두 점이 반대편에 위치하는지 확인합니다.

선분 `AB`에 대한 두 CCW 값의 부호가 서로 다르고, 선분 `CD`에 대한 두 CCW 값의 부호도 서로 다르면 두 선분이 교차하는 경우입니다.

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
      public static bool operator <(Point a, Point b) {
        if (a.X != b.X) return a.X < b.X;
        return a.Y < b.Y;
      }
      public static bool operator >(Point a, Point b) {
        return b < a;
      }
      public static bool operator <=(Point a, Point b) {
        return a < b || (a.X == b.X && a.Y == b.Y);
      }
      public static bool operator >=(Point a, Point b) {
        return b <= a;
      }
    }

    static long CCW(Point a, Point b, Point c) {
      return (b.X - a.X) * (c.Y - a.Y) - (b.Y - a.Y) * (c.X - a.X);
    }

    static bool IsSameSign(long a, long b) {
      if (a >= 0 && b <= 0) return false;
      if (a <= 0 && b >= 0) return false;
      return true;
    }

    static void Main(string[] args) {
      var line1 = Console.ReadLine()!.Split();
      var p1 = new Point(long.Parse(line1[0]), long.Parse(line1[1]));
      var p2 = new Point(long.Parse(line1[2]), long.Parse(line1[3]));

      var line2 = Console.ReadLine()!.Split();
      var p3 = new Point(long.Parse(line2[0]), long.Parse(line2[1]));
      var p4 = new Point(long.Parse(line2[2]), long.Parse(line2[3]));

      var cp1 = CCW(p1, p2, p3);
      var cp2 = CCW(p1, p2, p4);
      var cp3 = CCW(p3, p4, p1);
      var cp4 = CCW(p3, p4, p2);

      if ((cp1 == 0 || cp2 == 0) && (cp3 == 0 || cp4 == 0)) {
        if (p2 < p1) (p1, p2) = (p2, p1);
        if (p4 < p3) (p3, p4) = (p4, p3);
        if (p1 <= p4 && p3 <= p2) Console.WriteLine(1);
        else Console.WriteLine(0);
      } else if (!IsSameSign(cp1, cp2) && !IsSameSign(cp3, cp4)) {
        Console.WriteLine(1);
      } else {
        Console.WriteLine(0);
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

struct Point {
  ll x, y;
  bool operator<(const Point& o) const {
    if (x != o.x) return x < o.x;
    return y < o.y;
  }
  bool operator<=(const Point& o) const {
    return *this < o || (x == o.x && y == o.y);
  }
};

ll ccw(const Point& a, const Point& b, const Point& c) {
  return (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
}

bool isSameSign(ll a, ll b) {
  if (a >= 0 && b <= 0) return false;
  if (a <= 0 && b >= 0) return false;
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  Point p1, p2, p3, p4;
  cin >> p1.x >> p1.y >> p2.x >> p2.y;
  cin >> p3.x >> p3.y >> p4.x >> p4.y;

  ll cp1 = ccw(p1, p2, p3);
  ll cp2 = ccw(p1, p2, p4);
  ll cp3 = ccw(p3, p4, p1);
  ll cp4 = ccw(p3, p4, p2);

  if ((cp1 == 0 || cp2 == 0) && (cp3 == 0 || cp4 == 0)) {
    if (p2 < p1) swap(p1, p2);
    if (p4 < p3) swap(p3, p4);
    if (p1 <= p4 && p3 <= p2) cout << 1 << "\n";
    else cout << 0 << "\n";
  } else if (!isSameSign(cp1, cp2) && !isSameSign(cp3, cp4)) {
    cout << 1 << "\n";
  } else {
    cout << 0 << "\n";
  }

  return 0;
}
```

