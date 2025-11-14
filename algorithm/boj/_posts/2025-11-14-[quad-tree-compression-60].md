---
layout: single
title: "[백준 1992] 쿼드트리 (C#, C++) - soo:bak"
date: "2025-11-14 23:40:00 +0900"
description: 흑백 영상을 4분할하며 재귀적으로 압축해 문자열을 만드는 백준 1992번 쿼드트리 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1992번 - 쿼드트리](https://www.acmicpc.net/problem/1992)

## 설명

`N × N` 크기의 흑백 영상을 쿼드트리 방식으로 압축하여 문자열로 표현하는 문제입니다.<br>

영역의 모든 픽셀이 같은 값이면 그 값(`0` 또는 `1`)을 출력하고, 그렇지 않으면 영역을 4등분하여 재귀적으로 압축한 결과를 괄호로 묶어 출력합니다.<br>

`N`은 `2`의 거듭제곱이며 최대 `64`까지 주어집니다.<br>

<br>

## 접근법

분할 정복을 사용하여 해결합니다.

현재 영역의 모든 픽셀이 같은 값인지 확인합니다. 모두 같다면 해당 값을 출력하고 종료합니다.

만약 섞여 있다면 영역을 4등분하여 각 영역에 대해 재귀적으로 같은 과정을 반복합니다.

분할 순서는 왼쪽 위, 오른쪽 위, 왼쪽 아래, 오른쪽 아래 순입니다.

4개 영역의 결과를 괄호로 묶어 `(왼쪽위)(오른쪽위)(왼쪽아래)(오른쪽아래)` 형태로 출력합니다.


C#에서는 `StringBuilder`로 문자열을 누적하고, C++에서는 재귀 과정에서 바로 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Text;

namespace Solution {
  class Program {
    static int n;
    static int[,] board;
    static StringBuilder sb = new StringBuilder();

    static bool IsUniform(int r, int c, int size) {
      var value = board[r, c];
      for (var i = r; i < r + size; i++)
        for (var j = c; j < c + size; j++)
          if (board[i, j] != value) return false;
      return true;
    }

    static void Solve(int r, int c, int size) {
      if (IsUniform(r, c, size)) {
        sb.Append(board[r, c]);
        return;
      }
      sb.Append("(");
      var half = size / 2;
      Solve(r, c, half);
      Solve(r, c + half, half);
      Solve(r + half, c, half);
      Solve(r + half, c + half, half);
      sb.Append(")");
    }

    static void Main(string[] args) {
      n = int.Parse(Console.ReadLine()!);
      board = new int[n, n];
      for (var i = 0; i < n; i++) {
        var line = Console.ReadLine()!;
        for (var j = 0; j < n; j++)
          board[i, j] = line[j] - '0';
      }

      Solve(0, 0, n);
      Console.WriteLine(sb.ToString());
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<string> vs;

vs board;

bool isUniform(int r, int c, int size) {
  char value = board[r][c];
  for (int i = r; i < r + size; ++i)
    for (int j = c; j < c + size; ++j)
      if (board[i][j] != value) return false;
  return true;
}

void solve(int r, int c, int size) {
  if (isUniform(r, c, size)) {
    cout << board[r][c];
    return;
  }
  cout << "(";
  int half = size / 2;
  solve(r, c, half);
  solve(r, c + half, half);
  solve(r + half, c, half);
  solve(r + half, c + half, half);
  cout << ")";
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  board.resize(n);
  for (int i = 0; i < n; ++i)
    cin >> board[i];

  solve(0, 0, n);
  cout << "\n";

  return 0;
}
```

