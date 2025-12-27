---
layout: single
title: "[백준 1711] 직각삼각형 (C#, C++) - soo:bak"
date: "2025-12-07 00:50:00 +0900"
description: 점들 중 세 점을 골라 만들 수 있는 직각삼각형의 개수를 구하는 백준 1711번 직각삼각형 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1711
  - C#
  - C++
  - 알고리즘
keywords: "백준 1711, 백준 1711번, BOJ 1711, RightTriangles, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1711번 - 직각삼각형](https://www.acmicpc.net/problem/1711)

## 설명
N개의 서로 다른 점이 주어질 때, 세 점을 골라 만들 수 있는 직각삼각형의 개수를 구하는 문제입니다.

<br>

## 접근법
먼저, 한 점을 직각의 꼭짓점으로 고정합니다. 이 점을 피벗이라 하고, 다른 점들까지의 방향 벡터를 구합니다. 두 벡터가 수직이면 내적이 0이므로, 수직인 벡터 쌍의 개수가 해당 피벗에서 만들 수 있는 직각삼각형의 개수가 됩니다.

다음으로, 같은 방향의 벡터를 하나로 묶기 위해 기약 분수 형태로 정규화합니다. 벡터의 각 성분을 최대공약수로 나누고, 부호를 일정하게 맞춥니다. 예를 들어, (2, 4)와 (1, 2)는 같은 방향이므로 동일한 키로 처리합니다.

이후, 각 벡터의 등장 횟수를 저장하고, 벡터 (dx, dy)에 대해 수직인 벡터 (-dy, dx)의 등장 횟수를 곱합니다. 양방향으로 중복 계산되므로 2로 나눕니다.

모든 피벗에 대해 이 과정을 반복하면 총 직각삼각형 개수를 구할 수 있습니다. 시간 복잡도는 O(N^2 log N)입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static int n;
    static (long x, long y)[] v;

    static long Gcd(long a, long b) {
      if (b == 0)
        return a;
      return Gcd(b, a % b);
    }

    static long Solve(int d) {
      var cache = ((long x, long y)[])v.Clone();
      (cache[0], cache[d]) = (cache[d], cache[0]);

      var m = new Dictionary<(long, long), int>();
      for (var i = 1; i < n; i++) {
        var x = cache[i].x - cache[0].x;
        var y = cache[i].y - cache[0].y;
        var g = Gcd(x, y);
        if (g < 0)
          g = -g;
        x /= g;
        y /= g;
        var key = (x, y);
        if (m.ContainsKey(key))
          m[key]++;
        else
          m[key] = 1;
      }

      var ret = 0L;
      foreach (var kv in m) {
        var x = kv.Key.Item1;
        var y = kv.Key.Item2;
        var perp = (-y, x);
        if (m.ContainsKey(perp))
          ret += (long)kv.Value * m[perp];
      }

      return ret;
    }

    static void Main(string[] args) {
      n = int.Parse(Console.ReadLine()!);
      v = new (long, long)[n];
      for (var i = 0; i < n; i++) {
        var s = Console.ReadLine()!.Split();
        v[i] = (long.Parse(s[0]), long.Parse(s[1]));
      }

      var ans = 0L;
      for (var i = 0; i < n; i++)
        ans += Solve(i);

      Console.WriteLine(ans);
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
typedef vector<pll> vp;

ll n;
vp v, cache;

ll gcd(ll a, ll b) {
  if (!b)
    return a;
  return gcd(b, a % b);
}

ll solve(ll d) {
  map<pll, int> m;
  cache = v;
  swap(cache[0], cache[d]);

  for (int i = 1; i < n; i++) {
    ll x = cache[i].first - cache[0].first;
    ll y = cache[i].second - cache[0].second;
    ll g = gcd(x, y);
    if (g < 0)
      g = -g;
    x /= g;
    y /= g;
    m[{x, y}]++;
  }

  ll ret = 0;
  for (auto& i : m) {
    ll x = i.first.first;
    ll y = i.first.second;
    if (m.find({-y, x}) != m.end())
      ret += i.second * m[{-y, x}];
  }

  return ret;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n;
  v.resize(n);
  for (int i = 0; i < n; i++) {
    ll x, y; cin >> x >> y;
    v[i] = {x, y};
  }

  ll ans = 0;
  for (int i = 0; i < n; i++)
    ans += solve(i);

  cout << ans << "\n";

  return 0;
}
```
