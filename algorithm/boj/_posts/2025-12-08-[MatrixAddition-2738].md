---
layout: single
title: "[백준 2738] 행렬 덧셈 (C#, C++) - soo:bak"
date: "2025-12-08 03:50:00 +0900"
description: 두 N×M 행렬을 더해 결과를 출력하는 백준 2738번 행렬 덧셈 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2738
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 2738, 백준 2738번, BOJ 2738, MatrixAddition, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2738번 - 행렬 덧셈](https://www.acmicpc.net/problem/2738)

## 설명
같은 크기의 두 행렬이 주어질 때, 두 행렬을 더한 결과를 출력하는 문제입니다.

<br>

## 접근법
행렬 덧셈은 같은 위치의 원소끼리 더하면 됩니다. 두 행렬을 입력받은 뒤 각 위치의 합을 계산하여 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var nm = Console.ReadLine()!.Split();
    var n = int.Parse(nm[0]);
    var m = int.Parse(nm[1]);
    var a = new int[n, m];
    var b = new int[n, m];
    for (var i = 0; i < n; i++) {
      var row = Console.ReadLine()!.Split();
      for (var j = 0; j < m; j++) a[i, j] = int.Parse(row[j]);
    }
    for (var i = 0; i < n; i++) {
      var row = Console.ReadLine()!.Split();
      for (var j = 0; j < m; j++) b[i, j] = int.Parse(row[j]);
    }
    for (var i = 0; i < n; i++) {
      for (var j = 0; j < m; j++) {
        Console.Write(a[i, j] + b[i, j]);
        Console.Write(j + 1 == m ? "\n" : " ");
      }
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vvi a(n, vi(m));
  vvi b(n, vi(m));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++) cin >> a[i][j];
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++) cin >> b[i][j];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++) {
      cout << a[i][j] + b[i][j];
      cout << (j + 1 == m ? '\n' : ' ');
    }
  }

  return 0;
}
```
