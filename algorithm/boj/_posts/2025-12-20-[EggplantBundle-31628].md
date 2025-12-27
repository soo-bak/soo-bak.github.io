---
layout: single
title: "[백준 31628] 가지 한 두름 주세요 (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 31628번 C#, C++ 풀이 - 10x10 격자에서 가로나 세로 한 줄이 모두 같은 색인지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 31628
  - C#
  - C++
  - 알고리즘
keywords: "백준 31628, 백준 31628번, BOJ 31628, EggplantBundle, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31628번 - 가지 한 두름 주세요](https://www.acmicpc.net/problem/31628)

## 설명
10×10 격자에서 가로나 세로 한 줄이 모두 같은 색인지 판별하는 문제입니다.

한 줄의 10칸이 모두 같은 색이면 가지 한 두름을 만들 수 있습니다.

<br>

## 접근법
각 행과 열을 순회하며 첫 원소와 나머지 원소가 모두 같은지 확인합니다. 한 줄이라도 모든 칸이 같으면 1을 출력하고, 그런 줄이 없으면 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var grid = new string[10, 10];
    for (var i = 0; i < 10; i++) {
      var parts = Console.ReadLine()!.Split();
      for (var j = 0; j < 10; j++) grid[i, j] = parts[j];
    }

    var ok = false;
    for (var i = 0; i < 10 && !ok; i++) {
      var same = true;
      for (var j = 1; j < 10; j++)
        if (grid[i, j] != grid[i, 0]) { same = false; break; }
      if (same) ok = true;
    }
    for (var j = 0; j < 10 && !ok; j++) {
      var same = true;
      for (var i = 1; i < 10; i++)
        if (grid[i, j] != grid[0, j]) { same = false; break; }
      if (same) ok = true;
    }

    Console.WriteLine(ok ? 1 : 0);
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

  string g[10][10];
  for (int i = 0; i < 10; i++)
    for (int j = 0; j < 10; j++)
      cin >> g[i][j];

  bool ok = false;
  for (int i = 0; i < 10 && !ok; i++) {
    bool same = true;
    for (int j = 1; j < 10; j++)
      if (g[i][j] != g[i][0]) { same = false; break; }
    if (same) ok = true;
  }
  for (int j = 0; j < 10 && !ok; j++) {
    bool same = true;
    for (int i = 1; i < 10; i++)
      if (g[i][j] != g[0][j]) { same = false; break; }
    if (same) ok = true;
  }

  cout << (ok ? 1 : 0) << "\n";

  return 0;
}
```
