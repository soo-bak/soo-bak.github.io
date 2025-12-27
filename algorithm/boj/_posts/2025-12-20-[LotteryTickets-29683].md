---
layout: single
title: "[백준 29683] Рождественская лотерея (C#, C++) - soo:bak"
date: "2025-12-20 12:12:00 +0900"
description: "백준 29683번 C#, C++ 풀이 - 각 영수증 금액을 A로 나눈 몫을 합산해 필요한 복권 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 29683
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 29683, 백준 29683번, BOJ 29683, LotteryTickets, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29683번 - Рождественская лотерея](https://www.acmicpc.net/problem/29683)

## 설명
각 영수증 금액과 복권 1장을 받기 위한 금액이 주어질 때, 모든 영수증에서 받을 수 있는 복권 수의 합을 구하는 문제입니다.

<br>

## 접근법
각 영수증 금액을 기준 금액으로 나눈 몫을 모두 더합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var a = int.Parse(first[1]);
    var nums = Console.ReadLine()!.Split();

    var sum = 0;
    for (var i = 0; i < n; i++) {
      var x = int.Parse(nums[i]);
      sum += x / a;
    }

    Console.WriteLine(sum);
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

  int n, a; cin >> n >> a;
  long long sum = 0;
  for (int i = 0; i < n; i++) {
    int x; cin >> x;
    sum += x / a;
  }
  cout << sum << "\n";

  return 0;
}
```
