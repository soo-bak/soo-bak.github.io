---
layout: single
title: "[백준 32326] Conveyor Belt Sushi (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32326번 C#, C++ 풀이 - 접시 색깔별 가격을 곱해 합산하는 문제"
tags:
  - 백준
  - BOJ
  - 32326
  - C#
  - C++
  - 알고리즘
keywords: "백준 32326, 백준 32326번, BOJ 32326, ConveyorBeltSushi, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32326번 - Conveyor Belt Sushi](https://www.acmicpc.net/problem/32326)

## 설명
빨강, 초록, 파랑 접시 수가 주어질 때 총 비용을 계산하는 문제입니다.

<br>

## 접근법
빨강, 초록, 파랑 접시는 각각 3, 4, 5달러입니다.

따라서 각 색의 개수에 해당 가격을 곱해 합산하면 총 비용이 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var r = int.Parse(Console.ReadLine()!);
    var g = int.Parse(Console.ReadLine()!);
    var b = int.Parse(Console.ReadLine()!);
    Console.WriteLine(r * 3 + g * 4 + b * 5);
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

  int r, g, b; cin >> r >> g >> b;
  cout << r * 3 + g * 4 + b * 5 << "\n";

  return 0;
}
```
