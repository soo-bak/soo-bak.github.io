---
layout: single
title: "[백준 2052] 지수연산 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 2052번 C#, C++ 풀이 - 1/2^N을 정확한 소수 형태로 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 2052
  - C#
  - C++
  - 알고리즘
keywords: "백준 2052, 백준 2052번, BOJ 2052, Exponentiation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2052번 - 지수연산](https://www.acmicpc.net/problem/2052)

## 설명
1/2^N을 소수 형태로 정확히 출력하는 문제입니다.

<br>

## 접근법
분모가 2의 거듭제곱이면 분자와 분모에 같은 5의 거듭제곱을 곱해 분모를 10의 거듭제곱으로 만들 수 있습니다.

5의 N제곱을 계산한 뒤, 자릿수가 N이 되도록 앞에 0을 채우고 소수점을 붙여 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Numerics;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    BigInteger pow = 1;
    for (var i = 0; i < n; i++) pow *= 5;

    var s = pow.ToString().PadLeft(n, '0');
    Console.WriteLine("0." + s);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

string mul(const string& a, int b) {
  string r;
  int c = 0;
  for (int i = a.size() - 1; i >= 0 || c; i--) {
    int x = (i >= 0 ? a[i] - '0' : 0) * b + c;
    r.push_back('0' + x % 10);
    c = x / 10;
  }
  reverse(r.begin(), r.end());
  return r;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  string pow = "1";
  for (int i = 0; i < n; i++)
    pow = mul(pow, 5);

  if ((int)pow.size() < n)
    pow = string(n - pow.size(), '0') + pow;

  cout << "0." << pow << "\n";

  return 0;
}
```
