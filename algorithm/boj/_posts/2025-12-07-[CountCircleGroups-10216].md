---
layout: single
title: "[백준 10216] Count Circle Groups (C#, C++) - soo:bak"
date: "2025-12-07 01:15:00 +0900"
description: 통신 범위가 겹치는 진영들의 그룹 수를 구하는 백준 10216번 Count Circle Groups 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10216
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 그래프
  - graph_traversal
  - 기하학
  - disjoint_set
keywords: "백준 10216, 백준 10216번, BOJ 10216, CountCircleGroups, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10216번 - Count Circle Groups](https://www.acmicpc.net/problem/10216)

## 설명
N개의 진영이 있고, 각 진영의 통신 범위가 원으로 주어질 때, 서로 통신 가능한 진영들을 하나의 그룹으로 묶어 총 그룹 수를 구하는 문제입니다. 두 원이 닿거나 겹치면 직접 통신이 가능합니다.

<br>

## 접근법
먼저, 두 원이 연결되는 조건을 확인합니다. 중심 사이의 거리가 두 반지름의 합 이하이면 두 원은 닿거나 겹칩니다. 제곱 비교를 사용하면 제곱근 연산을 피할 수 있습니다.

다음으로, 모든 쌍을 검사하면서 조건을 만족하면 유니온 파인드로 합칩니다. 처음에 그룹 수를 N으로 설정하고, 두 진영이 합쳐질 때마다 1씩 감소시킵니다.

이후, 모든 쌍 검사가 끝나면 남은 그룹 수가 답이 됩니다. 시간 복잡도는 O(N^2)이며, N이 최대 3000이므로 충분합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static int[] parent;

    static int Find(int x) {
      if (parent[x] == x)
        return x;
      return parent[x] = Find(parent[x]);
    }

    static void Union(int a, int b) {
      a = Find(a);
      b = Find(b);
      if (a != b)
        parent[a] = b;
    }

    static void Main(string[] args) {
      var t = int.Parse(Console.ReadLine()!);
      while (t-- > 0) {
        var n = int.Parse(Console.ReadLine()!);
        var x = new int[n];
        var y = new int[n];
        var r = new int[n];
        parent = new int[n];

        for (var i = 0; i < n; i++) {
          var s = Console.ReadLine()!.Split();
          x[i] = int.Parse(s[0]);
          y[i] = int.Parse(s[1]);
          r[i] = int.Parse(s[2]);
          parent[i] = i;
        }

        var groups = n;
        for (var i = 0; i < n; i++) {
          for (var j = i + 1; j < n; j++) {
            var dx = (long)(x[i] - x[j]);
            var dy = (long)(y[i] - y[j]);
            var dist2 = dx * dx + dy * dy;
            var rr = (long)(r[i] + r[j]);
            if (dist2 <= rr * rr) {
              if (Find(i) != Find(j)) {
                Union(i, j);
                groups--;
              }
            }
          }
        }

        Console.WriteLine(groups);
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
typedef vector<int> vi;

struct DSU {
  vi p;
  DSU(int n): p(n) { iota(p.begin(), p.end(), 0); }

  int find(int x) {
    if (p[x] == x)
      return x;
    return p[x] = find(p[x]);
  }

  bool unite(int a, int b) {
    a = find(a);
    b = find(b);
    if (a == b)
      return false;
    p[a] = b;
    return true;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int T; cin >> T;
  while (T--) {
    int n; cin >> n;
    vi x(n), y(n), r(n);
    for (int i = 0; i < n; i++)
      cin >> x[i] >> y[i] >> r[i];

    DSU dsu(n);
    int groups = n;

    for (int i = 0; i < n; i++) {
      for (int j = i + 1; j < n; j++) {
        ll dx = x[i] - x[j];
        ll dy = y[i] - y[j];
        ll dist2 = dx * dx + dy * dy;
        ll rr = r[i] + r[j];
        if (dist2 <= rr * rr) {
          if (dsu.unite(i, j))
            groups--;
        }
      }
    }

    cout << groups << "\n";
  }

  return 0;
}
```
