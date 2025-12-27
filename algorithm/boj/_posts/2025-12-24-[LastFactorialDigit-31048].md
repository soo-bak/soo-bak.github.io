---
layout: single
title: "[백준 31048] Last Factorial Digit (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 31048번 C#, C++ 풀이 - N!의 마지막 자릿수를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 31048
  - C#
  - C++
  - 알고리즘
keywords: "백준 31048, 백준 31048번, BOJ 31048, LastFactorialDigit, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31048번 - Last Factorial Digit](https://www.acmicpc.net/problem/31048)

## 설명
각 테스트케이스마다 N!의 마지막 자릿수를 출력하는 문제입니다.

<br>

## 접근법
N이 10 이하이므로 팩토리얼 값을 직접 계산해도 충분합니다.

따라서 1부터 N까지 곱하면서 매번 10으로 나눈 나머지만 유지하면 마지막 자릿수를 구할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      var n = int.Parse(Console.ReadLine()!);
      var res = 1;
      for (var k = 2; k <= n; k++)
        res = (res * k) % 10;
      Console.WriteLine(res);
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

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    int res = 1;
    for (int k = 2; k <= n; k++)
      res = (res * k) % 10;
    cout << res << "\n";
  }

  return 0;
}
```
