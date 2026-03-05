---
layout: single
title: "[백준 13241] 최소공배수 (C#, C++) - soo:bak"
date: "2026-03-05 20:04:00 +0900"
description: "백준 13241번 C#, C++ 풀이 - 두 정수의 최소공배수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 13241
  - C#
  - C++
  - 알고리즘
  - 수학
  - 유클리드 호제법
keywords: "백준 13241, 백준 13241번, BOJ 13241, 최소공배수, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[13241번 - 최소공배수](https://www.acmicpc.net/problem/13241)

## 설명
두 정수 A, B가 주어질 때 두 수의 최소공배수를 구하는 문제입니다.

<br>

## 접근법
최소공배수는 두 수의 곱을 최대공약수로 나누어 구할 수 있습니다. 최대공약수는 유클리드 호제법으로 O(log min(A, B))에 계산할 수 있습니다.

곱셈 과정에서 범위를 넘지 않도록 64비트 정수로 계산합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static long Gcd(long a, long b) {
    while (b != 0) {
      long t = a % b;
      a = b;
      b = t;
    }
    return a;
  }

  static void Main() {
    var p = Console.ReadLine()!.Split();
    long a = long.Parse(p[0]);
    long b = long.Parse(p[1]);

    long g = Gcd(a, b);
    long lcm = (a / g) * b;
    Console.WriteLine(lcm);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

ll gcd(ll a, ll b) {
  while (b != 0) {
    ll t = a % b;
    a = b;
    b = t;
  }
  return a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b;
  cin >> a >> b;

  ll g = gcd(a, b);
  ll lcm = (a / g) * b;
  cout << lcm << "\n";

  return 0;
}
```
