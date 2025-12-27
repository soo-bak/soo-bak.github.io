---
layout: single
title: "[백준 15128] Congruent Numbers (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 직각삼각형 두 변이 유리수 p1/q1, p2/q2일 때 넓이 (p1·p2)/(2·q1·q2)가 정수인지 나머지 연산으로 판정하는 백준 15128번 Congruent Numbers 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15128
  - C#
  - C++
  - 알고리즘
keywords: "백준 15128, 백준 15128번, BOJ 15128, CongruentNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15128번 - Congruent Numbers](https://www.acmicpc.net/problem/15128)

## 설명
직각삼각형의 넓이가 정수인지 판단하는 문제입니다.

<br>

## 접근법
두 직각변이 유리수일 때 넓이는 분자끼리 곱하고 분모끼리 곱한 뒤 2로 나눈 형태입니다.

분자가 분모로 나누어떨어지면 넓이가 정수이므로 1을, 그렇지 않으면 0을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var p = Array.ConvertAll(Console.ReadLine()!.Split(), long.Parse);
    var p1 = p[0]; var q1 = p[1]; var p2 = p[2]; var q2 = p[3];

    var num = p1 * p2;
    var den = 2 * q1 * q2;
    Console.WriteLine(num % den == 0 ? 1 : 0);
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

  ll p1, q1, p2, q2; cin >> p1 >> q1 >> p2 >> q2;
  ll num = p1 * p2;
  ll den = 2 * q1 * q2;
  cout << (num % den == 0 ? 1 : 0) << "\n";

  return 0;
}
```
