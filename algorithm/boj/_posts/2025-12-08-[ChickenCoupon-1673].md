---
layout: single
title: "[백준 1673] 치킨 쿠폰 (C#, C++) - soo:bak"
date: "2025-12-08 04:50:00 +0900"
description: 쿠폰과 도장을 교환하며 최대 치킨 수를 구하는 백준 1673번 치킨 쿠폰 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1673
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 1673, 백준 1673번, BOJ 1673, ChickenCoupon, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1673번 - 치킨 쿠폰](https://www.acmicpc.net/problem/1673)

## 설명
쿠폰으로 치킨을 시키면 도장을 받고, 도장을 모아 다시 쿠폰으로 교환할 수 있습니다. 이 과정을 반복하여 먹을 수 있는 치킨의 총 개수를 구하는 문제입니다.

<br>

## 접근법
현재 가진 쿠폰으로 치킨을 주문하고 같은 수의 도장을 받습니다. 도장이 k개 이상이면 k개당 쿠폰 1장으로 교환하고 나머지 도장은 유지합니다. 쿠폰이 0이 될 때까지 이 과정을 반복하며 주문한 치킨 수를 누적합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string? line;
    while ((line = Console.ReadLine()) != null) {
      var parts = line.Split(' ', StringSplitOptions.RemoveEmptyEntries);
      if (parts.Length != 2) continue;
      var n = int.Parse(parts[0]);
      var k = int.Parse(parts[1]);
      var coupon = n;
      var stamp = 0;
      var ans = 0;
      while (coupon > 0) {
        ans += coupon;
        stamp += coupon;
        coupon = stamp / k;
        stamp %= k;
      }
      Console.WriteLine(ans);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, k;
  while (cin >> n >> k) {
    int coupon = n;
    int stamp = 0;
    int ans = 0;
    while (coupon > 0) {
      ans += coupon;
      stamp += coupon;
      coupon = stamp / k;
      stamp %= k;
    }
    cout << ans << "\n";
  }

  return 0;
}
```
