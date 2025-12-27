---
layout: single
title: "[백준 19751] Fractification (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: "백준 19751번 C#, C++ 풀이 - 네 수의 순서를 바꿔 a/b+c/d 값을 최소화하는 순열을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 19751
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 19751, 백준 19751번, BOJ 19751, Fractification, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[19751번 - Fractification](https://www.acmicpc.net/problem/19751)

## 설명
네 수의 순서를 바꿔 두 분수의 합을 최소로 만드는 문제입니다.

<br>

## 접근법
네 수를 두 분수의 분자와 분모로 배치하는 경우의 수는 24가지뿐입니다. 모든 순열을 시도해 각각의 합을 계산하고, 가장 작은 값을 주는 순열을 찾으면 됩니다. 분수 합을 실수로 계산하면 간단하게 비교할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var v = Array.ConvertAll(parts, int.Parse);

    var idx = new[] { 0, 1, 2, 3 };
    var best = double.MaxValue;
    var ans = new int[4];

    Permute(idx, 0, v, ref best, ans);

    Console.WriteLine(string.Join(" ", ans));
  }

  static void Permute(int[] a, int pos, int[] v, ref double best, int[] ans) {
    if (pos == 4) {
      var val = v[a[0]] / (double)v[a[1]] + v[a[2]] / (double)v[a[3]];
      if (val < best) {
        best = val;
        for (var i = 0; i < 4; i++)
          ans[i] = v[a[i]];
      }
      return;
    }
    for (var i = pos; i < 4; i++) {
      (a[pos], a[i]) = (a[i], a[pos]);
      Permute(a, pos + 1, v, ref best, ans);
      (a[pos], a[i]) = (a[i], a[pos]);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi v(4);
  for (int i = 0; i < 4; i++)
    cin >> v[i];

  vi perm = {0, 1, 2, 3};
  double best = 1e100;
  vi ans(4);

  sort(perm.begin(), perm.end());
  for (bool more = true; more; more = next_permutation(perm.begin(), perm.end())) {
    double val = (double)v[perm[0]] / v[perm[1]] + (double)v[perm[2]] / v[perm[3]];
    if (val < best) {
      best = val;
      for (int i = 0; i < 4; i++)
        ans[i] = v[perm[i]];
    }
  }

  cout << ans[0] << " " << ans[1] << " " << ans[2] << " " << ans[3] << "\n";

  return 0;
}
```
