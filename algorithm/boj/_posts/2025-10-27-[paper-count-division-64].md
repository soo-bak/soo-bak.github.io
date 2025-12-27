---
layout: single
title: "[백준 1780] 종이의 개수 (C#, C++) - soo:bak"
date: "2025-10-27 22:10:00 +0900"
description: 3×3 분할 정복으로 -1, 0, 1로만 채워진 종이 조각의 개수를 세는 백준 1780번 종이의 개수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1780
  - C#
  - C++
  - 알고리즘
keywords: "백준 1780, 백준 1780번, BOJ 1780, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1780번 - 종이의 개수](https://www.acmicpc.net/problem/1780)

## 설명

`N × N` 크기의 종이에 `-1`, `0`, `1` 중 하나가 채워져 있습니다.<br>

한 장이 모두 같은 수라면 그대로 사용하고, 아니라면 3등분을 두 번 반복해 **총 9개의 정사각형**으로 나눕니다.<br>

이 과정을 반복해 나가면서 `-1`, `0`, `1`로만 이루어진 조각의 개수를 각각 세어야 합니다.<br>

<br>

## 접근법

각 영역이 한 숫자로 통일되었는지 검사하고, 아니라면 `3×3`으로 재귀 분할하는 **분할 정복(Divide & Conquer)** 문제입니다.

- 현재 영역이 모두 같은 값인지 확인합니다.
- 다른 값이 섞여 있다면, `size / 3` 크기의 9개 영역으로 나눠 재귀 호출합니다.
- 통일된 영역을 만날 때마다 해당 값에 대응하는 카운터를 증가시킵니다.

<br>
입력 크기가 최대 `3^7`(2187)이라 재귀 깊이와 검사 범위도 충분히 안정적으로 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static int[,] paper;
  static int[] counts = new int[3];

  static bool IsUniform(int row, int col, int size) {
    var value = paper[row, col];
    for (var r = row; r < row + size; r++) {
      for (var c = col; c < col + size; c++) {
        if (paper[r, c] != value) return false;
      }
    }
    return true;
  }

  static void Divide(int row, int col, int size) {
    if (IsUniform(row, col, size)) {
      counts[paper[row, col] + 1]++;
      return;
    }

    var next = size / 3;
    for (var dr = 0; dr < 3; dr++) {
      for (var dc = 0; dc < 3; dc++) {
        Divide(row + dr * next, col + dc * next, next);
      }
    }
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
    Console.WriteLine(counts[2]);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<vector<int>> vvi;

int counts[3];
vvi board;

bool isUniform(int row, int col, int sz) {
  int value = board[row][col];
  for (int r = row; r < row + sz; ++r) {
    for (int c = col; c < col + sz; ++c) {
      if (board[r][c] != value) return false;
    }
  }
  return true;
}

void divide(int row, int col, int sz) {
  if (isUniform(row, col, sz)) {
    counts[board[row][col] + 1]++;
    return;
  }

  int next = sz / 3;
  for (int dr = 0; dr < 3; ++dr) {
    for (int dc = 0; dc < 3; ++dc)
      divide(row + dr * next, col + dc * next, next);
  }
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  board.assign(n, vector<int>(n));
  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < n; ++c)
      cin >> board[r][c];
  }

  divide(0, 0, n);

  cout << counts[0] << "\n"
    << counts[1] << "\n"
    << counts[2] << "\n";

  return 0;
}
```

