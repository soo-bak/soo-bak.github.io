---
layout: single
title: "[백준 14500] 테트로미노 (C#, C++) - soo:bak"
date: "2025-11-17 23:03:00 +0900"
description: 19개 테트로미노 모양을 모든 위치에 대입해 최댓값을 찾는 백준 14500번 테트로미노 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[14500번 - 테트로미노](https://www.acmicpc.net/problem/14500)

## 설명

`N × M` 크기의 종이 위에 테트로미노 하나를 놓아 테트로미노가 놓인 칸에 적힌 수들의 합을 최대로 하는 문제입니다.<br>

테트로미노는 네 개의 정사각형이 변을 공유하며 연결된 도형입니다. 회전과 대칭을 고려하면 총 19가지 모양이 있습니다.<br>

테트로미노를 자유롭게 회전시키거나 뒤집을 수 있으며, 종이를 벗어나지 않게 놓아야 합니다.<br>

`N`과 `M`은 각각 `4` 이상 `500` 이하이고, 각 칸에 쓰여 있는 수는 `1,000` 이하의 자연수입니다.<br>

<br>

## 접근법

모든 위치에 19가지 테트로미노 모양을 시도하는 완전 탐색으로 해결합니다.

19가지 테트로미노 모양을 상대 좌표로 미리 정의합니다. 예를 들어 `I` 모양의 가로 배치는 `{(0,0), (0,1), (0,2), (0,3)}`으로 표현됩니다.

<br>
보드의 각 칸을 시작점으로 하여 19가지 모양을 차례로 시도합니다. 모양이 보드를 벗어나지 않으면 네 칸의 합을 계산합니다.

<br>
계산된 모든 합 중에서 최댓값을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var n = int.Parse(tokens[0]);
      var m = int.Parse(tokens[1]);
      var board = new int[n][];
      for (var i = 0; i < n; i++) {
        var row = Console.ReadLine()!.Split();
        board[i] = new int[m];
        for (var j = 0; j < m; j++)
          board[i][j] = int.Parse(row[j]);
      }

      var tetrominoes = new (int r, int c)[][] {
        new[] {(0,0),(0,1),(0,2),(0,3)},
        new[] {(0,0),(1,0),(2,0),(3,0)},
        new[] {(0,0),(0,1),(1,0),(1,1)},
        new[] {(0,0),(1,0),(2,0),(2,1)},
        new[] {(0,0),(0,1),(0,2),(1,0)},
        new[] {(0,0),(0,1),(1,1),(2,1)},
        new[] {(1,0),(1,1),(1,2),(0,2)},
        new[] {(2,0),(2,1),(1,1),(0,1)},
        new[] {(0,0),(1,0),(1,1),(1,2)},
        new[] {(0,0),(0,1),(1,0),(2,0)},
        new[] {(0,0),(0,1),(0,2),(1,2)},
        new[] {(0,0),(1,0),(1,1),(2,1)},
        new[] {(1,0),(0,1),(1,1),(0,2)},
        new[] {(1,0),(2,0),(1,1),(0,1)},
        new[] {(0,0),(0,1),(1,1),(1,2)},
        new[] {(0,0),(0,1),(0,2),(1,1)},
        new[] {(1,0),(0,1),(1,1),(2,1)},
        new[] {(1,0),(0,1),(1,1),(1,2)},
        new[] {(0,0),(1,0),(2,0),(1,1)}
      };

      var best = 0;
      for (var r = 0; r < n; r++) {
        for (var c = 0; c < m; c++) {
          foreach (var shape in tetrominoes) {
            var sum = 0;
            var valid = true;
            foreach (var (dr, dc) in shape) {
              var nr = r + dr;
              var nc = c + dc;
              if (nr < 0 || nr >= n || nc < 0 || nc >= m) {
                valid = false;
                break;
              }
              sum += board[nr][nc];
            }
            if (valid && sum > best) best = sum;
          }
        }
      }

      Console.WriteLine(best);
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
typedef pair<int,int> pii;
typedef vector<pii> vpii;
typedef vector<vpii> vvpii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vvi board(n, vi(m));
  for (int i = 0; i < n; ++i)
    for (int j = 0; j < m; ++j)
      cin >> board[i][j];

  vvpii shapes = {
    {{0,0},{0,1},{0,2},{0,3}},
    {{0,0},{1,0},{2,0},{3,0}},
    {{0,0},{0,1},{1,0},{1,1}},
    {{0,0},{1,0},{2,0},{2,1}},
    {{0,0},{0,1},{0,2},{1,0}},
    {{0,0},{0,1},{1,1},{2,1}},
    {{1,0},{1,1},{1,2},{0,2}},
    {{2,0},{2,1},{1,1},{0,1}},
    {{0,0},{1,0},{1,1},{1,2}},
    {{0,0},{0,1},{1,0},{2,0}},
    {{0,0},{0,1},{0,2},{1,2}},
    {{0,0},{1,0},{1,1},{2,1}},
    {{1,0},{0,1},{1,1},{0,2}},
    {{1,0},{2,0},{1,1},{0,1}},
    {{0,0},{0,1},{1,1},{1,2}},
    {{0,0},{0,1},{0,2},{1,1}},
    {{1,0},{0,1},{1,1},{2,1}},
    {{1,0},{0,1},{1,1},{1,2}},
    {{0,0},{1,0},{2,0},{1,1}}
  };

  int best = 0;
  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < m; ++c) {
      for (const auto& shape : shapes) {
        int sum = 0;
        bool ok = true;

        for (auto [dr, dc] : shape) {
          int nr = r + dr, nc = c + dc;
          if (nr < 0 || nr >= n || nc < 0 || nc >= m) {
            ok = false;
            break;
          }
          sum += board[nr][nc];
        }

        if (ok) best = max(best, sum);
      }
    }
  }

  cout << best << "\n";

  return 0;
}
```

