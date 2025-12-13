---
layout: single
title: "[백준 27110] 특식 배부 (C#, C++) - soo:bak"
date: "2025-12-13 22:20:00 +0900"
description: 각 치킨 종류별 주문량 N과 선호 인원 A,B,C가 주어질 때, min(선호, N)을 합산해 원하는 치킨을 받는 최대 인원을 구하는 백준 27110번 특식 배부 문제의 C#/C++ 풀이
---

## 문제 링크
[27110번 - 특식 배부](https://www.acmicpc.net/problem/27110)

## 설명
세 종류의 치킨을 각각 n마리씩 주문했을 때, 원하는 치킨을 받을 수 있는 최대 인원을 구하는 문제입니다.

<br>

## 접근법
각 종류의 선호 인원이 n명보다 많으면 n명만 받을 수 있습니다.

따라서 각 종류별로 선호 인원과 n 중 작은 값을 더하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    var ans = Math.Min(parts[0], n) + Math.Min(parts[1], n) + Math.Min(parts[2], n);
    Console.WriteLine(ans);
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

  int n; cin >> n;
  int a, b, c; cin >> a >> b >> c;
  int ans = min(a, n) + min(b, n) + min(c, n);
  cout << ans << "\n";

  return 0;
}
```
