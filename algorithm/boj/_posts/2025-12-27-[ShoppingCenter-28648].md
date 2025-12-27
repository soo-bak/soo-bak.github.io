---
layout: single
title: "[백준 28648] Торговый центр (C#, C++) - soo:bak"
date: "2025-12-27 15:35:00 +0900"
description: "백준 28648번 C#, C++ 풀이 - 버스 도착 시간과 이동 시간을 이용해 가장 빨리 도착할 수 있는 시간을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 28648
  - C#
  - C++
  - 알고리즘
keywords: "백준 28648, 백준 28648번, BOJ 28648, ShoppingCenter, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[28648번 - Торговый центр](https://www.acmicpc.net/problem/28648)

## 설명
각 버스가 집 앞에 도착하는 시간과 쇼핑센터까지 걸리는 시간이 주어집니다.

가장 빨리 쇼핑센터에 도착할 수 있는 시간을 구하는 문제입니다.

<br>

## 접근법
각 버스의 도착 시간과 이동 시간의 합을 계산하고, 그 중 최솟값을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var earliest = int.MaxValue;

    for (var i = 0; i < n; i++) {
      var parts = Console.ReadLine()!.Split();
      var t = int.Parse(parts[0]);
      var l = int.Parse(parts[1]);
      earliest = Math.Min(earliest, t + l);
    }

    Console.WriteLine(earliest);
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

  int earliest = 1e9;
  for (int i = 0; i < n; i++) {
    int t, l; cin >> t >> l;
    earliest = min(earliest, t + l);
  }

  cout << earliest << "\n";

  return 0;
}
```

