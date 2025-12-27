---
layout: single
title: "[백준 27130] Long Multiplication (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 27130번 C#, C++ 풀이 - 두 정수의 긴 곱셈 과정을 자리별로 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 27130
  - C#
  - C++
  - 알고리즘
keywords: "백준 27130, 백준 27130번, BOJ 27130, LongMultiplication, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[27130번 - Long Multiplication](https://www.acmicpc.net/problem/27130)

## 설명
두 정수를 입력받아 긴 곱셈 과정의 중간 결과와 최종 결과를 출력하는 문제입니다.

<br>

## 접근법
첫 번째 수를 그대로 출력한 뒤, 두 번째 수의 각 자릿수에 대해 첫 번째 수와 곱한 결과를 뒤에서부터 순서대로 출력합니다.

마지막에 전체 곱을 출력합니다. 각 정수가 최대 20자리이므로 64비트 정수형으로 표현할 수 없어 문자열로 곱셈을 구현해 처리합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Numerics;

class Program {
  static void Main() {
    var a = BigInteger.Parse(Console.ReadLine()!);
    var b = Console.ReadLine()!;

    Console.WriteLine(a);
    Console.WriteLine(b);

    for (var i = b.Length - 1; i >= 0; i--) {
      var d = b[i] - '0';
      Console.WriteLine(a * d);
    }

    Console.WriteLine(a * BigInteger.Parse(b));
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

string mulDigit(const string& a, int d) {
  if (d == 0) return "0";
  string res;
  int carry = 0;
  for (int i = (int)a.size() - 1; i >= 0; i--) {
    int val = (a[i] - '0') * d + carry;
    res.push_back(char('0' + (val % 10)));
    carry = val / 10;
  }
  while (carry > 0) {
    res.push_back(char('0' + (carry % 10)));
    carry /= 10;
  }
  reverse(res.begin(), res.end());
  return res;
}

string mul(const string& a, const string& b) {
  vector<int> res(a.size() + b.size(), 0);
  for (int i = (int)a.size() - 1; i >= 0; i--) {
    for (int j = (int)b.size() - 1; j >= 0; j--) {
      int idx = i + j + 1;
      int val = (a[i] - '0') * (b[j] - '0') + res[idx];
      res[idx] = val % 10;
      res[idx - 1] += val / 10;
    }
  }
  string out;
  bool started = false;
  for (int v : res) {
    if (v != 0 || started) {
      out.push_back(char('0' + v));
      started = true;
    }
  }
  return started ? out : "0";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string a, b; cin >> a >> b;

  cout << a << "\n";
  cout << b << "\n";

  for (int i = (int)b.size() - 1; i >= 0; i--) {
    int d = b[i] - '0';
    cout << mulDigit(a, d) << "\n";
  }

  cout << mul(a, b) << "\n";

  return 0;
}
```
