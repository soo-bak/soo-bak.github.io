---
layout: single
title: "[백준 15858] Simple Arithmetic (C#, C++) - soo:bak"
date: "2025-12-19 22:47:00 +0900"
description: a·b/c를 1e-6 오차 내로 출력하기 위해 정밀 부동소수로 계산하는 백준 15858번 Simple Arithmetic 문제의 C#/C++ 풀이
tags:
  - 백준
  - BOJ
  - 15858
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
  - arbitrary_precision
keywords: "백준 15858, 백준 15858번, BOJ 15858, SimpleArithmetic, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15858번 - Simple Arithmetic](https://www.acmicpc.net/problem/15858)

## 설명
세 정수 a, b, c가 주어질 때, a × b / c를 계산하여 출력하는 문제입니다.

절대 오차 10^-6 이내로 출력해야 합니다.

<br>

## 접근법
부동소수점 오차를 피하기 위해 정수 연산으로 계산합니다.

먼저 a × b를 구한 뒤 c로 나눈 몫이 정수 부분입니다.

이후 나머지에 10을 곱하고 c로 나누는 과정을 반복하여 소수점 아래 자릿수를 구합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var p = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
    var a = p[0];
    var b = p[1];
    var c = p[2];
    var mult = a * b;
    var div = mult / c;
    var sb = new StringBuilder();
    sb.Append(div);
    sb.Append('.');
    for (var i = 0; i < 6; i++) {
      mult = mult % c * 10;
      if (mult < c) sb.Append('0');
      else sb.Append(mult / c);
    }
    Console.WriteLine(sb.ToString());
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b, c; cin >> a >> b >> c;
  ll mult = a * b;
  ll div = mult / c;
  string ans = to_string(div) + ".";
  for (int i = 0; i < 6; i++) {
    mult = mult % c * 10;
    if (mult < c) ans += '0';
    else ans += ((mult / c) + '0');
  }
  cout << ans << "\n";

  return 0;
}
```
