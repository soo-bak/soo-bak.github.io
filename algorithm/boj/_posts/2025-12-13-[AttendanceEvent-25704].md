---
layout: single
title: "[백준 25704] 출석 이벤트 (C#, C++) - soo:bak"
date: "2025-12-13 13:02:00 +0900"
description: 출석 도장 수에 따른 할인 쿠폰 중 하나를 적용해 지불해야 할 최소 금액을 구하는 백준 25704번 출석 이벤트 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 25704
  - C#
  - C++
  - 알고리즘
keywords: "백준 25704, 백준 25704번, BOJ 25704, AttendanceEvent, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[25704번 - 출석 이벤트](https://www.acmicpc.net/problem/25704)

## 설명
출석 도장 수에 따른 할인 쿠폰을 적용해 지불해야 할 최소 금액을 구하는 문제입니다.

<br>

## 접근법
출석 도장 5개부터 500원 할인, 10개부터 10% 할인, 15개부터 2000원 할인, 20개부터 25% 할인 쿠폰을 사용할 수 있습니다.

적용 가능한 모든 할인을 계산하고 그중 최소값을 선택합니다.

할인 결과가 0보다 작으면 0으로 보정합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var p = int.Parse(Console.ReadLine()!);

    var best = p;
    if (n >= 5) best = Math.Min(best, p - 500);
    if (n >= 10) best = Math.Min(best, p * 90 / 100);
    if (n >= 15) best = Math.Min(best, p - 2000);
    if (n >= 20) best = Math.Min(best, p * 75 / 100);

    if (best < 0) best = 0;
    Console.WriteLine(best);
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

  int n, p; cin >> n >> p;
  int best = p;
  if (n >= 5) best = min(best, p - 500);
  if (n >= 10) best = min(best, p * 90 / 100);
  if (n >= 15) best = min(best, p - 2000);
  if (n >= 20) best = min(best, p * 75 / 100);
  if (best < 0) best = 0;
  cout << best << "\n";

  return 0;
}
```
