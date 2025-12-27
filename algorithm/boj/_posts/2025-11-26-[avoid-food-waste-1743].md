---
layout: single
title: "[백준 1743] 음식물 피하기 (C#, C++) - soo:bak"
date: "2025-11-26 22:48:00 +0900"
description: 통로 격자에 놓인 음식물을 상하좌우로 묶어 가장 큰 덩어리의 크기를 DFS/BFS로 찾는 백준 1743번 음식물 피하기 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 1743
  - C#
  - C++
  - 알고리즘
  - 그래프
  - graph_traversal
  - BFS
  - DFS
  - grid_graph
keywords: "백준 1743, 백준 1743번, BOJ 1743, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1743번 - 음식물 피하기](https://www.acmicpc.net/problem/1743)

## 설명

통로 격자에 음식물 쓰레기가 여러 개 놓여 있고, 상하좌우로 인접한 음식물끼리는 하나의 덩어리로 간주될 때, 가장 큰 음식물 덩어리의 크기를 구하는 문제입니다.

통로의 세로와 가로 크기, 음식물의 개수와 각 음식물의 좌표가 주어집니다.

좌표는 1부터 시작하며, 모든 음식물은 서로 다른 위치에 있습니다.

<br>

## 접근법

통로의 모든 칸을 순회하면서 아직 방문하지 않은 음식물을 발견하면, 그곳을 시작점으로 탐색을 시작합니다.

탐색 과정에서 현재 위치에서 상하좌우 4방향으로 인접한 모든 음식물을 찾아 방문 표시를 하고, 덩어리의 크기를 세어갑니다.

하나의 탐색이 끝나면 해당 덩어리의 크기를 기록하고, 지금까지 발견한 덩어리 중 가장 큰 크기를 갱신합니다.

<br>
예를 들어, 3×4 격자에서 음식물이 (1,1), (1,2), (2,2), (3,3), (3,4) 위치에 있다고 가정하면, (1,1)-(1,2)-(2,2)가 하나의 덩어리로 연결되어 크기 3, (3,3)-(3,4)가 다른 덩어리로 연결되어 크기 2를 이루므로, 가장 큰 덩어리의 크기는 3입니다.

<br>
입력 좌표는 1부터 시작하므로, 배열에 저장할 때는 1을 빼서 0부터 시작하도록 변환합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static readonly int[] dy = {-1, 1, 0, 0};
    static readonly int[] dx = {0, 0, -1, 1};

    static void Main(string[] args) {
      var first = Console.ReadLine()!.Split();
      var n = int.Parse(first[0]);
      var m = int.Parse(first[1]);
      var k = int.Parse(first[2]);

      var board = new bool[n][];
      var visited = new bool[n][];

      for (var i = 0; i < n; i++) {
        board[i] = new bool[m];
        visited[i] = new bool[m];
      }

      for (var i = 0; i < k; i++) {
        var line = Console.ReadLine()!.Split();
        var r = int.Parse(line[0]) - 1;
        var c = int.Parse(line[1]) - 1;

        board[r][c] = true;
      }

      var answer = 0;
      var q = new Queue<(int y, int x)>();

      for (var y = 0; y < n; y++) {
        for (var x = 0; x < m; x++) {
          if (!board[y][x] || visited[y][x]) continue;

          var size = 0;
          visited[y][x] = true;
          q.Enqueue((y, x));

          while (q.Count > 0) {
            var cur = q.Dequeue();
            size++;

            for (var dir = 0; dir < 4; dir++) {
              var ny = cur.y + dy[dir];
              var nx = cur.x + dx[dir];

              if (ny < 0 || ny >= n || nx < 0 || nx >= m) continue;
              if (visited[ny][nx] || !board[ny][nx]) continue;

              visited[ny][nx] = true;
              q.Enqueue((ny, nx));
            }
          }

          if (size > answer) answer = size;
        }
      }

      Console.WriteLine(answer);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<bool> vb;
typedef vector<vb> vvb;
typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m, k; cin >> n >> m >> k;

  vvb board(n, vb(m, false));
  vvb visited(n, vb(m, false));

  for (int i = 0; i < k; i++) {
    int r, c; cin >> r >> c;

    board[r - 1][c - 1] = true;
  }

  const int dy[4] = {-1, 1, 0, 0};
  const int dx[4] = {0, 0, -1, 1};
  int answer = 0;

  queue<pii> q;

  for (int y = 0; y < n; y++) {
    for (int x = 0; x < m; x++) {
      if (!board[y][x] || visited[y][x]) continue;

      visited[y][x] = true;
      q.push({y, x});
      int size = 0;

      while (!q.empty()) {
        auto [cy, cx] = q.front();
        q.pop();

        ++size;

        for (int dir = 0; dir < 4; dir++) {
          int ny = cy + dy[dir];
          int nx = cx + dx[dir];

          if (ny < 0 || ny >= n || nx < 0 || nx >= m) continue;
          if (visited[ny][nx] || !board[ny][nx]) continue;

          visited[ny][nx] = true;
          q.push({ny, nx});
        }
      }

      if (size > answer) answer = size;
    }
  }

  cout << answer << "\n";

  return 0;
}
```

