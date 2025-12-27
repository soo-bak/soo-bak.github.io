---
layout: single
title: "[백준 3679] 단순 다각형 (C#, C++) - soo:bak"
date: "2025-12-08 01:35:00 +0900"
description: 최좌하단 기준으로 극각 정렬 후 마지막 collinear 구간을 뒤집어 단순 다각형을 만드는 백준 3679번 단순 다각형 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 3679
  - C#
  - C++
  - 알고리즘
keywords: "백준 3679, 백준 3679번, BOJ 3679, SimplePolygon, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3679번 - 단순 다각형](https://www.acmicpc.net/problem/3679)

## 설명
주어진 점들을 모두 꼭짓점으로 사용하여 선분이 서로 교차하지 않는 단순 다각형을 만드는 문제입니다.

<br>

## 접근법
단순 다각형을 만드는 가장 직관적인 방법은 한 점을 기준으로 나머지 점들을 각도 순으로 정렬하는 것입니다. 기준점에서 시작해서 각도 순으로 점들을 이으면 선분이 교차하지 않습니다.

<br>

먼저 기준점을 정합니다. 가장 왼쪽에 있는 점 중에서 가장 아래에 있는 점을 기준으로 삼습니다. 이 점을 기준으로 나머지 점들을 반시계 방향 각도 순으로 정렬합니다. 각도가 같은 점들은 x 좌표가 작은 순으로 정렬합니다.

<br>

여기서 주의할 점이 있습니다. 정렬된 점들을 순서대로 이으면 마지막 점에서 다시 기준점으로 돌아와야 합니다. 그런데 마지막 구간에 기준점과 일직선상에 있는 점들이 여러 개 있으면 문제가 생깁니다.

예를 들어 기준점 A와 일직선상에 B, C가 있고 A에서 가까운 순으로 B, C라면, 정렬 결과는 ... B, C 순서가 됩니다. 그러면 C에서 A로 돌아갈 때 B를 지나게 되어 선분이 겹칩니다.

<br>

이 문제를 해결하려면 마지막 일직선 구간의 순서를 뒤집으면 됩니다. ... C, B 순서로 바꾸면 C에서 B로, B에서 A로 자연스럽게 이어집니다.

따라서 정렬 후 맨 끝에서부터 기준점과 일직선인 점들의 구간을 찾아서 그 구간만 역순으로 출력합니다.

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

  static long Ccw(long x1, long y1, long x2, long y2, long x3, long y3) =>
    (x1 * y2 + x2 * y3 + x3 * y1) - (y1 * x2 + y2 * x3 + y3 * x1);

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    while (t-- > 0) {
      var tokens = new Queue<string>(Console.ReadLine()!.Split());
      var n = int.Parse(tokens.Dequeue());
      var pts = new List<Point>(n);
      for (var i = 0; i < n; i++) {
        if (tokens.Count < 2) {
          foreach (var s in Console.ReadLine()!.Split())
            tokens.Enqueue(s);
        }
        var x = long.Parse(tokens.Dequeue());
        var y = long.Parse(tokens.Dequeue());
        pts.Add(new Point { idx = i, x = x, y = y });
      }

      pts.Sort((a, b) => {
        if (a.x != b.x) return a.x.CompareTo(b.x);
        return a.y.CompareTo(b.y);
      });

      var baseP = pts[0];
      pts.Sort(1, n - 1, Comparer<Point>.Create((a, b) => {
        var cross = Ccw(baseP.x, baseP.y, a.x, a.y, b.x, b.y);
        if (cross == 0) {
          if (a.x != b.x) return a.x.CompareTo(b.x);
          return a.y.CompareTo(b.y);
        }
        return cross > 0 ? -1 : 1;
      }));

      var idx = n - 2;
      while (idx >= 0 && Ccw(baseP.x, baseP.y, pts[idx].x, pts[idx].y, pts[idx + 1].x, pts[idx + 1].y) == 0) idx--;

      var output = new List<int>(n);
      for (var i = 0; i <= idx; i++) output.Add(pts[i].idx);
      for (var i = n - 1; i > idx; i--) output.Add(pts[i].idx);

      Console.WriteLine(string.Join(" ", output));
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
typedef pair<int, pll> pill;

vector<pill> v;

ll ccw(ll x1, ll y1, ll x2, ll y2, ll x3, ll y3) {
  return (x1 * y2 + x2 * y3 + x3 * y1) - (y1 * x2 + y2 * x3 + y3 * x1);
}

bool comp1(pill& a, pill& b) {
  if (a.second.first == b.second.first) return a.second.second < b.second.second;
  return a.second.first < b.second.first;
}

bool comp2(pill& a, pill& b) {
  ll crossP = ccw(v[0].second.first, v[0].second.second, a.second.first, a.second.second, b.second.first, b.second.second);
  if (!crossP) {
    if (a.second.first == b.second.first) return a.second.second < b.second.second;
    else return a.second.first < b.second.first;
  }
  return crossP > 0;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase; cin >> cntCase;
  while (cntCase--) {
    int n; cin >> n;
    v.clear(); v.assign(n, {0, {0, 0}});
    for (int i = 0; i < n; i++) {
      v[i].first = i;
      cin >> v[i].second.first >> v[i].second.second;
    }

    sort(v.begin(), v.end(), comp1);
    sort(v.begin() + 1, v.end(), comp2);

    int idx = n - 2;
    while (true) {
      if (idx < 0 || ccw(v[0].second.first, v[0].second.second, v[idx].second.first, v[idx].second.second, v[idx + 1].second.first, v[idx + 1].second.second))
        break;
      idx--;
    }

    for (int i = 0; i <= idx; i++) cout << v[i].first << " ";
    for (int i = n - 1; i > idx; i--) cout << v[i].first << " ";
    cout << "\n";
  }

  return 0;
}
```
