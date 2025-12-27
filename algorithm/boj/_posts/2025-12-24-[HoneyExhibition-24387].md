---
layout: single
title: "[백준 24387] ИЗЛОЖЕНИЕ НА ПЧЕЛЕН МЕД (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 24387번 C#, C++ 풀이 - 세 종류 가격과 세 용량을 일대일로 매칭해 최대 수익을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 24387
  - C#
  - C++
  - 알고리즘
keywords: "백준 24387, 백준 24387번, BOJ 24387, HoneyExhibition, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[24387번 - ИЗЛОЖЕНИЕ НА ПЧЕЛЕН МЕД](https://www.acmicpc.net/problem/24387)

## 설명
세 종류의 가격과 세 용량을 서로 다르게 매칭해 얻을 수 있는 최대 수익을 구하는 문제입니다.

<br>

## 접근법
세 가지를 서로 다른 용기에 배치해야 하므로 모든 순열을 시도합니다.

각 매칭에서 수익을 계산하고 최대값을 선택합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var p = Console.ReadLine()!.Split();
    var a = new long[3];
    for (var i = 0; i < 3; i++)
      a[i] = long.Parse(p[i]);

    var q = Console.ReadLine()!.Split();
    var b = new long[3];
    for (var i = 0; i < 3; i++)
      b[i] = long.Parse(q[i]);

    long best = 0;
    for (var i = 0; i < 3; i++) {
      for (var j = 0; j < 3; j++) {
        if (j == i) continue;
        for (var k = 0; k < 3; k++) {
          if (k == i || k == j) continue;
          var sum = a[0] * b[i] + a[1] * b[j] + a[2] * b[k];
          if (sum > best) best = sum;
        }
      }
    }

    Console.WriteLine(best);
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

  ll a[3], b[3];
  for (int i = 0; i < 3; i++)
    cin >> a[i];
  for (int i = 0; i < 3; i++)
    cin >> b[i];

  ll best = 0;
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      if (j == i) continue;
      for (int k = 0; k < 3; k++) {
        if (k == i || k == j) continue;
        ll sum = a[0] * b[i] + a[1] * b[j] + a[2] * b[k];
        if (sum > best) best = sum;
      }
    }
  }

  cout << best << "\n";

  return 0;
}
```
