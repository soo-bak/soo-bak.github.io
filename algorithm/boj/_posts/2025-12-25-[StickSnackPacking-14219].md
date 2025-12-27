---
layout: single
title: "[백준 14219] 막대과자 포장 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 14219번 C#, C++ 풀이 - 넓이 3짜리 과자로 N×M 상자를 채울 수 있는지 판정하는 문제"
tags:
  - 백준
  - BOJ
  - 14219
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 14219, 백준 14219번, BOJ 14219, StickSnackPacking, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14219번 - 막대과자 포장](https://www.acmicpc.net/problem/14219)

## 설명
3칸짜리 두 종류의 과자를 사용해 N×M 상자를 빈틈없이 채울 수 있는지 판단하는 문제입니다.

<br>

## 접근법
모든 과자의 넓이는 3이므로 전체 칸 수 `n*m`이 3의 배수가 아니면 불가능합니다.  
`n*m`이 3의 배수라면 n 또는 m이 3의 배수이므로, 3×1 과자만으로 줄 단위로 채울 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var n = int.Parse(parts[0]);
    var m = int.Parse(parts[1]);

    var ok = (n * m) % 3 == 0;
    Console.WriteLine(ok ? "YES" : "NO");
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

  int n, m; cin >> n >> m;
  cout << ((n * m) % 3 == 0 ? "YES" : "NO") << "\n";

  return 0;
}
```
