---
layout: single
title: "[백준 31995] 게임말 올려놓기 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 31995번 C#, C++ 풀이 - 대각선으로 인접한 두 칸을 선택하는 경우의 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 31995
  - C#
  - C++
  - 알고리즘
  - 수학
  - 조합론
keywords: "백준 31995, 백준 31995번, BOJ 31995, PlacingGamePieces, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31995번 - 게임말 올려놓기](https://www.acmicpc.net/problem/31995)

## 설명
N×M 격자에서 서로 대각선으로 이웃한 두 칸에 말을 놓는 경우의 수를 구하는 문제입니다.

<br>

## 접근법
2×2 블록마다 대각선 쌍이 2개 존재합니다.  
따라서 경우의 수는 `2 * (N-1) * (M-1)`입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var m = int.Parse(Console.ReadLine()!);
    var ans = 2 * (n - 1) * (m - 1);
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

  int n; cin >> n;
  int m; cin >> m;
  int ans = 2 * (n - 1) * (m - 1);
  cout << ans << "\n";

  return 0;
}
```
