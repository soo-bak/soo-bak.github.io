---
layout: single
title: "[백준 31922] 이 대회는 이제 제 겁니다 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: Division 1 우승 상금 A와 shake! 우승 상금 C의 합 또는 Division 2 상금 P 중 최댓값을 구하는 백준 31922번 문제에 대한 C# 및 C++ 설명
---

## 문제 링크
[31922번 - 이 대회는 이제 제 겁니다](https://www.acmicpc.net/problem/31922)

## 설명
Division 1 또는 Division 2 중 하나만 참가할 수 있을 때, 얻을 수 있는 최대 상금을 계산하는 문제입니다.

<br>

## 접근법
Division 1 우승 시 본 대회 상금과 shake! 상금을 함께 받습니다. Division 2 우승 시 해당 상금만 받습니다. 두 경우 중 최댓값을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var p = int.Parse(parts[1]);
    var c = int.Parse(parts[2]);

    Console.WriteLine(Math.Max(p, a + c));
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

  int a, p, c; cin >> a >> p >> c;

  cout << max(p, a + c) << "\n";

  return 0;
}
```
