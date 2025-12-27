---
layout: single
title: "[백준 25591] 푸앙이와 종윤이 (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 두 두자리 수에 대해 베다수학 방식으로 a,b,c,d,q,r을 계산하고 결과 앞/뒤 자릿수를 출력하는 백준 25591번 푸앙이와 종윤이 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 25591
  - C#
  - C++
  - 알고리즘
keywords: "백준 25591, 백준 25591번, BOJ 25591, PooangiJongyoon, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25591번 - 푸앙이와 종윤이](https://www.acmicpc.net/problem/25591)

## 설명
베다수학 방식으로 두 두자리 수의 곱셈 중간 과정과 결과를 구하는 문제입니다.

<br>

## 접근법
먼저 두 수 x, y를 각각 100에서 뺀 값 a, b를 구합니다.

다음으로 c는 100에서 a + b를 뺀 값이고, d는 a와 b의 곱입니다.

이후 d를 100으로 나눈 몫 q와 나머지 r을 구하고, 최종 앞자리는 c + q, 뒷자리는 r이 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var p = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
    var x = p[0]; var y = p[1];

    var a = 100 - x;
    var b = 100 - y;
    var c = 100 - (a + b);
    var d = a * b;

    var q = d / 100;
    var r = d % 100;

    var prev = c + q;
    var aft = r;

    Console.WriteLine($"{a} {b} {c} {d} {q} {r}");
    Console.WriteLine($"{prev} {aft}");
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

  int x, y; cin >> x >> y;
  int a = 100 - x;
  int b = 100 - y;
  int c = 100 - (a + b);
  int d = a * b;
  int q = d / 100;
  int r = d % 100;
  int prev = c + q;
  int aft = r;

  cout << a << ' ' << b << ' ' << c << ' ' << d << ' ' << q << ' ' << r << "\n";
  cout << prev << ' ' << aft << "\n";

  return 0;
}
```
