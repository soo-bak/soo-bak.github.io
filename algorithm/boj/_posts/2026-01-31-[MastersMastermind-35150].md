---
layout: single
title: "[백준 35150] 동우의 생일은? (C#, C++) - soo:bak"
date: "2026-01-31 23:11:00 +0900"
description: "백준 35150번 C#, C++ 풀이 - 직사각형 선물 N개를 배치해 외접 최소 직사각형의 최대 면적을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 35150
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 35150, 백준 35150번, BOJ 35150, 동우의 생일은?, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[35150번 - 동우의 생일은?](https://www.acmicpc.net/problem/35150)

## 설명
가로 A, 세로 B인 직사각형 선물 N개를 회전 가능하게 겹치지 않고 연결해 놓을 때, 이들을 포함하는 외접 최소 직사각형의 넓이를 최대로 만드는 값을 구하는 문제입니다.

<br>

## 접근법
선물을 한 개씩 계단 모양으로 이어 붙이면, 각 선물을 (A,B) 또는 (B,A)로 두어 폭과 높이에 각각 (A,B) 또는 (B,A)가 더해집니다. (N개 모두 연결됨)

따라서 k개를 (A,B)로 두면 폭 W = k·A + (N−k)·B, 높이 H = k·B + (N−k)·A가 되며 넓이는 f(k)=W·H 입니다.

f(k)는 k에 대한 이차식으로 최대값이 가운데에서 발생하므로 k = ⌊N/2⌋, ⌈N/2⌉ 두 경우만 계산해 큰 값을 택하면 됩니다. 64비트 정수 범위 안에 들어갑니다.

시간 복잡도 O(1) (테스트 케이스당).

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static long Area(long a, long b, long n, long k) {
    long w = k * a + (n - k) * b;
    long h = k * b + (n - k) * a;
    return w * h;
  }

  static void Main() {
    int t = int.Parse(Console.ReadLine()!);
    for (int _ = 0; _ < t; _++) {
      var p = Console.ReadLine()!.Split();
      long a = long.Parse(p[0]);
      long b = long.Parse(p[1]);
      long n = long.Parse(p[2]);

      long k0 = n / 2;
      long k1 = n - k0;

      long ans = Math.Max(Area(a, b, n, k0), Area(a, b, n, k1));
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

ll area(ll a, ll b, ll n, ll k) {
  ll w = k * a + (n - k) * b;
  ll h = k * b + (n - k) * a;
  return w * h;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    ll a, b, n;
    cin >> a >> b >> n;

    ll k0 = n / 2;
    ll k1 = n - k0;

    ll ans = max(area(a, b, n, k0), area(a, b, n, k1));
    cout << ans << "\n";
  }

  return 0;
}
```
