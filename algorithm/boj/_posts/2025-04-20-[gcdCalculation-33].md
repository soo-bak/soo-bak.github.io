---
layout: single
title: "[백준 9884] Euclid (C#, C++) - soo:bak"
date: "2025-04-20 18:11:00 +0900"
description: 두 정수의 최대공약수를 유클리드 호제법으로 계산하는 백준 9884번 Euclid 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9884
  - C#
  - C++
  - 알고리즘
keywords: "백준 9884, 백준 9884번, BOJ 9884, gcdCalculation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9884번 - Euclid](https://www.acmicpc.net/problem/9884)

## 설명
**두 개의 자연수가 주어졌을 때, 이들의 최대공약수(GCD)를 구하는 문제입니다.**
<br>

- 입력으로 두 개의 양의 정수가 주어집니다.
- 이 두 수의 **최대공약수(Greatest Common Divisor)**를 출력해야 합니다.
- 유클리드 호제법을 이용하면 효율적으로 최대공약수를 구할 수 있습니다.

> 참고 : [GCD(최대공약수)와 유클리드 호제법의 원리 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)


## 접근법

- 먼저 두 개의 정수를 입력받습니다.
- 이후 유클리드 호제법을 사용하여 최대공약수를 계산하여 출력합니다.

## Code

### C#
```csharp
using System;
using System.Numerics;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    long a = long.Parse(input[0]);
    long b = long.Parse(input[1]);

    Console.WriteLine(BigInteger.GreatestCommonDivisor(a, b));
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>

using namespace std;
typedef long long ll;

ll gcd(ll a, ll b) {
  return b ? gcd(b, a % b) : a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b; cin >> a >> b;
  cout << gcd(a, b) << "\n";

  return 0;
}
```
