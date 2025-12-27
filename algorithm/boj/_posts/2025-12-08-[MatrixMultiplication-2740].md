---
layout: single
title: "[백준 2740] 행렬 곱셈 (C#, C++) - soo:bak"
date: "2025-12-08 03:30:00 +0900"
description: N×M, M×K 행렬을 곱해 N×K 결과를 출력하는 백준 2740번 행렬 곱셈 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2740
  - C#
  - C++
  - 알고리즘
keywords: "백준 2740, 백준 2740번, BOJ 2740, MatrixMultiplication, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2740번 - 행렬 곱셈](https://www.acmicpc.net/problem/2740)

## 설명
두 행렬이 주어질 때 곱한 결과를 출력하는 문제입니다. 첫 번째 행렬의 열 수와 두 번째 행렬의 행 수가 같으므로 곱셈이 가능합니다.

<br>

## 접근법
행렬 곱셈의 정의를 그대로 구현합니다. 결과 행렬의 각 원소는 첫 번째 행렬의 해당 행과 두 번째 행렬의 해당 열을 원소별로 곱한 뒤 모두 더한 값입니다.

삼중 반복문으로 모든 원소를 계산합니다. 행렬 크기가 최대 100이므로 시간 안에 충분히 처리됩니다.

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
    for (var i = 0; i < n; i++) {
      var row = Console.ReadLine()!.Split();
      for (var j = 0; j < m; j++) a[i, j] = int.Parse(row[j]);
    }

    var mk = Console.ReadLine()!.Split();
    var m2 = int.Parse(mk[0]);
    var k = int.Parse(mk[1]);
    var b = new int[m2, k];
    for (var i = 0; i < m2; i++) {
      var row = Console.ReadLine()!.Split();
      for (var j = 0; j < k; j++) b[i, j] = int.Parse(row[j]);
    }

    var c = new int[n, k];
    for (var i = 0; i < n; i++) {
      for (var j = 0; j < k; j++) {
        var sum = 0;
        for (var t = 0; t < m; t++) sum += a[i, t] * b[t, j];
        c[i, j] = sum;
      }
    }

    for (var i = 0; i < n; i++) {
      for (var j = 0; j < k; j++) {
        Console.Write(c[i, j]);
        Console.Write(j + 1 == k ? "\n" : " ");
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
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++) cin >> a[i][j];

  int m2, k; cin >> m2 >> k;
  vvi b(m2, vi(k));
  for (int i = 0; i < m2; i++)
    for (int j = 0; j < k; j++) cin >> b[i][j];

  vvi c(n, vi(k, 0));
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < k; j++) {
      int sum = 0;
      for (int t = 0; t < m; t++) sum += a[i][t] * b[t][j];
      c[i][j] = sum;
      cout << c[i][j] << (j + 1 == k ? '\n' : ' ');
    }
  }

  return 0;
}
```
