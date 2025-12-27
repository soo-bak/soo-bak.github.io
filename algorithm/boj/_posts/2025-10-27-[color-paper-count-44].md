---
layout: single
title: "[백준 2630] 색종이 만들기 (C#, C++) - soo:bak"
date: "2025-10-27 22:30:00 +0900"
description: 흰색과 파란색으로 칠해진 종이를 4분할 분할 정복으로 나누며 색종이 개수를 세는 백준 2630번 색종이 만들기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2630
  - C#
  - C++
  - 알고리즘
keywords: "백준 2630, 백준 2630번, BOJ 2630, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2630번 - 색종이 만들기](https://www.acmicpc.net/problem/2630)

## 설명

`0`(하얀색)과 `1`(파란색)으로 채워진 `N × N` 종이를 재귀적으로 4등분하여, 각 조각이 단일 색이 될 때까지 자르는 문제입니다.<br>

최종적으로 얻은 흰색 색종이와 파란색 색종이의 개수를 각각 구해야 합니다.<br>

<br>

## 접근법

분할 정복 알고리듬듬을 적용합니다.

현재 영역의 모든 칸이 같은 색인지 확인하고, 단일 색이면 해당 색의 카운터를 증가시킵니다.

다른 색이 섞여 있다면 영역을 4등분하여 각각에 대해 같은 과정을 재귀적으로 반복합니다.

<br>
`N`은 최대 `128`이므로, 재귀 깊이는 최대 $$\log_2 128 = 7$$이며 시간 복잡도는 $$O(N^2 \log N)$$입니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static int[,] paper;
  static int[] counts = new int[2];

  static bool IsUniform(int row, int col, int size) {
    var color = paper[row, col];
    for (var r = row; r < row + size; r++) {
      for (var c = col; c < col + size; c++) {
        if (paper[r, c] != color) return false;
      }
    }
    return true;
  }

  static void Divide(int row, int col, int size) {
    if (IsUniform(row, col, size)) {
      counts[paper[row, col]]++;
      return;
    }

    var next = size / 2;
    Divide(row, col, next);
    Divide(row, col + next, next);
    Divide(row + next, col, next);
    Divide(row + next, col + next, next);
  }

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    paper = new int[n, n];
    for (var r = 0; r < n; r++) {
      var tokens = Console.ReadLine()!.Split();
      for (var c = 0; c < n; c++)
        paper[r, c] = int.Parse(tokens[c]);
    }

    Divide(0, 0, n);
    Console.WriteLine(counts[0]);
    Console.WriteLine(counts[1]);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;

int countsArr[2];
vvi board;

bool isUniform(int row, int col, int sz) {
  int color = board[row][col];
  for (int r = row; r < row + sz; ++r)
    for (int c = col; c < col + sz; ++c)
      if (board[r][c] != color) return false;
  return true;
}

void divide(int row, int col, int sz) {
  if (isUniform(row, col, sz)) {
    countsArr[board[row][col]]++;
    return ;
  }

  int next = sz / 2;
  divide(row, col, next);
  divide(row, col + next, next);
  divide(row + next, col, next);
  divide(row + next, col + next, next);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  board.assign(n, vi(n));
  for (int r = 0; r < n; ++r)
    for (int c = 0; c < n; ++c)
      cin >> board[r][c];

  divide(0, 0, n);

  cout << countsArr[0] << "\n" << countsArr[1] << "\n";

  return 0;
}
```

