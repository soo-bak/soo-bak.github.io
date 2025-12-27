---
layout: single
title: "[백준 2909] 캔디 구매 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 2909번 C#, C++ 풀이 - 가격을 10의 K제곱 단위로 반올림하는 문제"
tags:
  - 백준
  - BOJ
  - 2909
  - C#
  - C++
  - 알고리즘
keywords: "백준 2909, 백준 2909번, BOJ 2909, CandyPurchase, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2909번 - 캔디 구매](https://www.acmicpc.net/problem/2909)

## 설명
주어진 가격을 10의 K제곱 단위로 반올림해 출력하는 문제입니다.

<br>

## 접근법
반올림 단위는 10을 K번 곱한 값입니다.

이후 가격에 단위의 절반을 더한 뒤 단위로 나누고 다시 곱하면 가장 가까운 배수가 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var c = int.Parse(parts[0]);
    var k = int.Parse(parts[1]);

    var unit = 1;
    for (var i = 0; i < k; i++)
      unit *= 10;

    var ans = (c + unit / 2) / unit * unit;
    Console.WriteLine(ans);
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

  int c, k; cin >> c >> k;
  int unit = 1;
  for (int i = 0; i < k; i++)
    unit *= 10;

  int ans = (c + unit / 2) / unit * unit;
  cout << ans << "\n";

  return 0;
}
```
