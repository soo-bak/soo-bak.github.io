---
layout: single
title: "[백준 26336] Are We Stopping Again? (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 26336번 C#, C++ 풀이 - 주행 거리에서 주유/식사 정차 횟수를 합집합으로 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 26336
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
keywords: "백준 26336, 백준 26336번, BOJ 26336, AreWeStoppingAgain, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[26336번 - Are We Stopping Again?](https://www.acmicpc.net/problem/26336)

## 설명
주행 거리 D와 주유/식사 주기가 주어질 때 정차 횟수를 계산하는 문제입니다.

<br>

## 접근법
목적지에서는 정차하지 않으므로 시작점부터 목적지 직전까지의 거리에서 정차 위치를 셉니다.

이후 주유 주기와 식사 주기의 배수 개수를 포함배제 원리로 계산하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Gcd(int a, int b) {
    while (b != 0) {
      var t = a % b;
      a = b;
      b = t;
    }
    return a;
  }

  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var i = 0; i < t; i++) {
      var parts = Console.ReadLine()!.Split();
      var d = int.Parse(parts[0]);
      var g = int.Parse(parts[1]);
      var f = int.Parse(parts[2]);

      var limit = d - 1;
      var lcm = g / Gcd(g, f) * f;
      var stops = limit / g + limit / f - limit / lcm;

      Console.WriteLine($"{d} {g} {f}");
      Console.WriteLine(stops);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int gcdInt(int a, int b) {
  while (b != 0) {
    int t = a % b;
    a = b;
    b = t;
  }
  return a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int d, g, f; cin >> d >> g >> f;
    int limit = d - 1;
    int lcm = g / gcdInt(g, f) * f;
    int stops = limit / g + limit / f - limit / lcm;

    cout << d << " " << g << " " << f << "\n";
    cout << stops << "\n";
  }

  return 0;
}
```
