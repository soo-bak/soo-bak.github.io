---
layout: single
title: "[백준 31867] 홀짝홀짝 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: 각 자릿수의 짝수/홀수 개수를 비교해 더 많으면 0 또는 1, 같으면 -1을 출력하는 문제
tags:
  - 백준
  - BOJ
  - 31867
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 문자열
keywords: "백준 31867, 백준 31867번, BOJ 31867, OddEvenOddEven, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31867번 - 홀짝홀짝](https://www.acmicpc.net/problem/31867)

## 설명
주어진 수의 각 자릿수가 짝수인지 홀수인지 세어 비교한 뒤, 짝수가 더 많으면 0, 홀수가 더 많으면 1, 같으면 -1을 출력하는 문제입니다.

<br>

## 접근법
자연수 K를 문자열로 받아 각 문자를 숫자로 변환해 홀짝을 판별합니다. 짝수와 홀수 개수를 각각 세고 비교해 조건에 맞는 값을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var k = Console.ReadLine()!;

    var even = 0;
    var odd = 0;
    for (var i = 0; i < n; i++) {
      var digit = k[i] - '0';
      if (digit % 2 == 0) even++;
      else odd++;
    }

    if (even > odd) Console.WriteLine(0);
    else if (odd > even) Console.WriteLine(1);
    else Console.WriteLine(-1);
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
  string k; cin >> k;

  int even = 0, odd = 0;
  for (int i = 0; i < n; i++) {
    int digit = k[i] - '0';
    if (digit % 2 == 0) even++;
    else odd++;
  }

  if (even > odd) cout << 0 << "\n";
  else if (odd > even) cout << 1 << "\n";
  else cout << -1 << "\n";

  return 0;
}
```
