---
layout: single
title: "[백준 23812] 골뱅이 찍기 - 돌아간 ㅍ (C#, C++) - soo:bak"
date: "2025-12-13 17:01:00 +0900"
description: 가로줄과 세로줄을 N배로 그려 돌아간 ㅍ 모양을 출력하는 백준 23812번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23812
  - C#
  - C++
  - 알고리즘
keywords: "백준 23812, 백준 23812번, BOJ 23812, AtSignRotatedP, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23812번 - 골뱅이 찍기 - 돌아간 ㅍ](https://www.acmicpc.net/problem/23812)

## 설명
돌아간 ㅍ자 모양의 골뱅이 패턴을 출력하는 문제입니다.

<br>

## 접근법
전체 높이는 5n이 됩니다.

가로줄은 5n개의 골뱅이로, 세로줄 행은 양쪽 n개씩 골뱅이와 가운데 3n개의 공백으로 구성됩니다.

이후, 세로줄-가로줄-세로줄-가로줄-세로줄 순서로 각각 n줄씩 출력합니다.

<br>

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    var side = new string('@', n);
    var mid = new string(' ', 3 * n);
    var full = new string('@', 5 * n);

    void PrintSides() {
      for (var i = 0; i < n; i++)
        sb.AppendLine(side + mid + side);
    }
    void PrintFull() {
      for (var i = 0; i < n; i++)
        sb.AppendLine(full);
    }

    PrintSides();
    PrintFull();
    PrintSides();
    PrintFull();
    PrintSides();

    Console.Write(sb.ToString());
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

  int n;
  if (!(cin >> n)) return 0;
  string side(n, '@');
  string mid(3 * n, ' ');
  string full(5 * n, '@');

  auto printSides = [&]() {
    for (int i = 0; i < n; i++)
      cout << side << mid << side << "\n";
  };
  auto printFull = [&]() {
    for (int i = 0; i < n; i++)
      cout << full << "\n";
  };

  printSides();
  printFull();
  printSides();
  printFull();
  printSides();

  return 0;
}
```
