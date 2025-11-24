---
layout: single
title: "[백준 20149] 선분 교차 3 (C#, C++) - soo:bak"
date: "2025-11-24 23:15:00 +0900"
description: CCW로 교차 여부를 판정하고, 한 점에서 만날 때만 직선 교점 공식을 사용해 좌표를 출력하는 백준 20149번 선분 교차 3 문제의 C# 및 C++ 풀이
---

## 문제 링크
[20149번 - 선분 교차 3](https://www.acmicpc.net/problem/20149)

## 설명

2차원 평면 위에 두 개의 선분이 주어집니다.

각 선분은 시작점과 끝점의 좌표로 표현되며, 두 선분이 교차하는지 판정하고, 교차한다면 교점의 좌표를 출력하는 문제입니다.

두 선분이 겹쳐서 교점이 무한히 많은 경우에는 좌표를 출력하지 않습니다.

<br>

## 접근법

두 선분의 교차 여부를 판정하기 위해 CCW(Counter Clock Wise) 알고리즘을 사용합니다.

CCW는 세 점의 방향성을 판단하는 기법으로, 세 점 p1, p2, p3가 주어졌을 때 외적을 이용해 p1에서 p2로 가는 벡터와 p2에서 p3로 가는 벡터의 회전 방향을 계산합니다.

결과가 양수면 반시계 방향, 음수면 시계 방향, 0이면 일직선상에 있음을 의미합니다.

<br>
두 선분 AB와 CD가 교차하는지 판정하려면, A-B를 기준으로 C와 D가 서로 다른 방향에 있는지, C-D를 기준으로 A와 B가 서로 다른 방향에 있는지를 확인합니다.

구체적으로, CCW(A, B, C)와 CCW(A, B, D)의 곱이 0 이하이고, CCW(C, D, A)와 CCW(C, D, B)의 곱도 0 이하이면 두 선분은 교차합니다.

예를 들어, 선분 AB가 (0,0)-(2,2)이고 선분 CD가 (0,2)-(2,0)일 때, A-B 기준으로 C는 반시계, D는 시계 방향에 있고, C-D 기준으로 A는 반시계, B는 시계 방향에 있으므로 두 선분은 교차합니다.

<br>
두 CCW 곱이 모두 0인 경우는 네 점이 모두 일직선상에 있는 경우입니다.

이때는 각 선분을 정렬한 후(작은 점이 앞에 오도록), 첫 번째 선분의 시작점이 두 번째 선분의 끝점보다 작거나 같고, 두 번째 선분의 시작점이 첫 번째 선분의 끝점보다 작거나 같으면 겹칩니다.

<br>
교점 좌표를 구할 때는 교차가 확인되면 항상 교점 계산 함수를 호출합니다.

교점 계산 함수 내에서 분모 값을 먼저 계산하는데, 이 값이 0이 아니면 일반적인 교차이므로 직선의 교점 공식을 사용합니다.

분모가 0이면 두 선분이 평행하거나 일직선상에 있는 경우로, 이때는 두 선분의 끝점이 정확히 한 점에서 만나는 경우만 그 점을 출력합니다.

<br>
직선의 교점 공식은 다음과 같습니다.

선분의 두 점을 (x1, y1), (x2, y2), 다른 선분의 두 점을 (x3, y3), (x4, y4)라 할 때, 분모는 (x1 - x2)(y3 - y4) - (y1 - y2)(x3 - x4)입니다.

교점의 x 좌표는 ((x1y2 - y1x2)(x3 - x4) - (x1 - x2)(x3y4 - y3x4))를 분모로 나눈 값이고, y 좌표는 ((x1y2 - y1x2)(y3 - y4) - (y1 - y2)(x3y4 - y3x4))를 분모로 나눈 값입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Globalization;

namespace Solution {
  struct Point {
    public long X, Y;
    public Point(long x, long y) { X = x; Y = y; }
    public static bool operator <=(Point a, Point b) => (a.X != b.X) ? a.X <= b.X : a.Y <= b.Y;
    public static bool operator >=(Point a, Point b) => (a.X != b.X) ? a.X >= b.X : a.Y >= b.Y;
    public static bool operator ==(Point a, Point b) => a.X == b.X && a.Y == b.Y;
    public static bool operator !=(Point a, Point b) => !(a == b);
    public override bool Equals(object? obj) => obj is Point p && this == p;
    public override int GetHashCode() => HashCode.Combine(X, Y);
  }

  class Program {
    static long Ccw(Point p1, Point p2, Point p3) {
      var v = p1.X * p2.Y + p2.X * p3.Y + p3.X * p1.Y;
      v -= p2.X * p1.Y + p3.X * p2.Y + p1.X * p3.Y;

      if (v > 0) return 1;
      if (v == 0) return 0;

      return -1;
    }

    static void PrintCrossPoint(Point p1, Point p2, Point p3, Point p4) {
      var numerX = (p1.X * p2.Y - p1.Y * p2.X) * (p3.X - p4.X) - (p1.X - p2.X) * (p3.X * p4.Y - p3.Y * p4.X);
      var numerY = (p1.X * p2.Y - p1.Y * p2.X) * (p3.Y - p4.Y) - (p1.Y - p2.Y) * (p3.X * p4.Y - p3.Y * p4.X);
      var denomi = (p1.X - p2.X) * (p3.Y - p4.Y) - (p1.Y - p2.Y) * (p3.X - p4.X);

      if (denomi == 0) {
        if (p2 == p3 && p1 <= p3)
          Console.WriteLine($"{p2.X} {p2.Y}");
        else if (p1 == p4 && p3 <= p1)
          Console.WriteLine($"{p1.X} {p1.Y}");
      } else {
        var x = (double)numerX / denomi;
        var y = (double)numerY / denomi;

        Console.WriteLine(x.ToString("F9", CultureInfo.InvariantCulture) + " " + y.ToString("F9", CultureInfo.InvariantCulture));
      }
    }

    static void Main(string[] args) {
      var l1 = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
      var l2 = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);

      var l1b = new Point(l1[0], l1[1]);
      var l1e = new Point(l1[2], l1[3]);
      var l2b = new Point(l2[0], l2[1]);
      var l2e = new Point(l2[2], l2[3]);

      var cp1 = Ccw(l1b, l1e, l2b) * Ccw(l1b, l1e, l2e);
      var cp2 = Ccw(l2b, l2e, l1b) * Ccw(l2b, l2e, l1e);

      if (cp1 == 0 && cp2 == 0) {
        if (l1e <= l1b) (l1b, l1e) = (l1e, l1b);
        if (l2e <= l2b) (l2b, l2e) = (l2e, l2b);

        if (l1b <= l2e && l2b <= l1e) {
          Console.WriteLine(1);
          PrintCrossPoint(l1b, l1e, l2b, l2e);
        } else Console.WriteLine(0);
      } else {
        if (cp1 <= 0 && cp2 <= 0) {
          Console.WriteLine(1);
          PrintCrossPoint(l1b, l1e, l2b, l2e);
        } else Console.WriteLine(0);
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
typedef pair<ll, ll> pll;

ll ccw(pll p1, pll p2, pll p3) {
  ll tmp = (p1.first * p2.second) + (p2.first * p3.second) + (p3.first * p1.second);
  tmp -= (p2.first * p1.second) + (p3.first * p2.second) + (p1.first * p3.second);

  if (tmp > 0) return 1;
  else if (tmp == 0) return 0;
  else return -1;
}

void printCrossPoint(pll p1, pll p2, pll p3, pll p4) {
  double numerX, numerY, denomi;

  numerX = (p1.first * p2.second - p1.second * p2.first) * (p3.first - p4.first) -
           (p1.first - p2.first) * (p3.first * p4.second - p3.second * p4.first);
  numerY = (p1.first * p2.second - p1.second * p2.first) * (p3.second - p4.second) -
           (p1.second - p2.second) * (p3.first * p4.second - p3.second * p4.first);
  denomi = (p1.first - p2.first) * (p3.second - p4.second) - (p1.second - p2.second) * (p3.first - p4.first);

  if (!denomi) {
    if (p2 == p3 && p1 <= p3)
      cout << p2.first << " " << p2.second << "\n";
    else if (p1 == p4 && p3 <= p1)
      cout << p1.first << " " << p1.second << "\n";
  } else {
    double x = numerX / denomi, y = numerY / denomi;

    cout << fixed;
    cout.precision(9);
    cout << x << " " << y << "\n";
  }
}

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  pll l1b, l1e, l2b, l2e;

  cin >> l1b.first >> l1b.second >> l1e.first >> l1e.second;
  cin >> l2b.first >> l2b.second >> l2e.first >> l2e.second;

  ll cp1 = ccw(l1b, l1e, l2b) * ccw(l1b, l1e, l2e);
  ll cp2 = ccw(l2b, l2e, l1b) * ccw(l2b, l2e, l1e);

  if (!cp1 && !cp2) {
    if (l1b > l1e) swap(l1b, l1e);
    if (l2b > l2e) swap(l2b, l2e);

    if (l1b <= l2e && l2b <= l1e) {
      cout << 1 << "\n";
      printCrossPoint(l1b, l1e, l2b, l2e);
    } else cout << 0 << "\n";
  } else {
    if (cp1 <= 0 && cp2 <= 0) {
      cout << 1 << "\n";
      printCrossPoint(l1b, l1e, l2b, l2e);
    } else  cout << 0 << "\n";
  }

  return 0;
}
```

