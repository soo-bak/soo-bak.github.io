---
layout: single
title: "[백준 2004] 조합 0의 개수 (C#, C++) - soo:bak"
date: "2025-12-08 03:35:00 +0900"
description: 조합 nCk에서 소인수 2와 5의 지수 차를 계산해 끝자리 0의 개수를 구하는 백준 2004번 조합 0의 개수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2004
  - C#
  - C++
  - 알고리즘
  - 수학
  - 정수론
keywords: "백준 2004, 백준 2004번, BOJ 2004, CombinationZeros, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2004번 - 조합 0의 개수](https://www.acmicpc.net/problem/2004)

## 설명
조합 값의 끝에 붙는 0의 개수를 구하는 문제입니다. 끝자리 0은 10의 배수에서 나오고, 10은 2와 5의 곱이므로 소인수 2와 5의 개수 중 작은 값이 답이 됩니다.

<br>

## 접근법
먼저 n!에서 특정 소수가 몇 번 곱해지는지 구하는 방법을 생각합니다. n 이하의 수 중 그 소수의 배수 개수, 제곱의 배수 개수, 세제곱의 배수 개수, ... 를 모두 더하면 됩니다.

조합은 n!을 k!과 (n-k)!으로 나눈 것이므로, n!에서의 지수에서 k!의 지수와 (n-k)!의 지수를 빼면 조합에서의 지수가 됩니다. 이를 2와 5에 대해 각각 계산하고, 둘 중 작은 값을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static long CountFactor(long n, int p) {
    var res = 0L;
    for (var div = (long)p; div <= n; div *= p)
      res += n / div;
    return res;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = long.Parse(parts[0]);
    var k = long.Parse(parts[1]);
    var two = CountFactor(n, 2) - CountFactor(k, 2) - CountFactor(n - k, 2);
    var five = CountFactor(n, 5) - CountFactor(k, 5) - CountFactor(n - k, 5);
    Console.WriteLine(Math.Min(two, five));
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

ll countFactor(ll n, int p) {
  ll res = 0;
  for (ll div = p; div <= n; div *= p) res += n / div;
  return res;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n, k; cin >> n >> k;
  ll two = countFactor(n, 2) - countFactor(k, 2) - countFactor(n - k, 2);
  ll five = countFactor(n, 5) - countFactor(k, 5) - countFactor(n - k, 5);
  cout << min(two, five) << "\n";

  return 0;
}
```
