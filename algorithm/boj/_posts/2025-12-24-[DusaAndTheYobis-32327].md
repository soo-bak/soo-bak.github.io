---
layout: single
title: "[백준 32327] Dusa And The Yobis (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32327번 C#, C++ 풀이 - 순서대로 먹을 수 있는 Yobi만 흡수하며 크기를 갱신하는 문제"
tags:
  - 백준
  - BOJ
  - 32327
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
  - 시뮬레이션
keywords: "백준 32327, 백준 32327번, BOJ 32327, DusaAndTheYobis, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32327번 - Dusa And The Yobis](https://www.acmicpc.net/problem/32327)

## 설명
Dusa가 Yobi를 만날 때마다 크기를 갱신하다가 도망치는 순간의 크기를 출력하는 문제입니다.

<br>

## 접근법
입력을 순서대로 읽으며 현재 크기보다 작은 Yobi는 흡수해 크기에 더합니다.

크기가 같거나 큰 Yobi를 만나면 도망치므로 그때의 크기를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var data = Console.In.ReadToEnd();
    var parts = data.Split();
    var idx = 0;
    var d = int.Parse(parts[idx++]);

    while (idx < parts.Length) {
      var y = int.Parse(parts[idx++]);
      if (y < d) d += y;
      else break;
    }

    Console.WriteLine(d);
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

  int d;
  if (!(cin >> d)) return 0;
  int y;
  while (cin >> y) {
    if (y < d) d += y;
    else break;
  }

  cout << d << "\n";

  return 0;
}
```
