---
layout: single
title: "[백준 7569] 토마토 (C#, C++) - soo:bak"
date: "2025-11-17 23:10:00 +0900"
description: 3차원 상자에서 익은 토마토를 동시에 확산시키는 BFS로 최소 일수를 구하는 백준 7569번 토마토 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 7569
  - C#
  - C++
  - 알고리즘
  - BFS
  - 그래프
  - graph_traversal
  - grid_graph
  - 최단경로
keywords: "백준 7569, 백준 7569번, BOJ 7569, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7569번 - 토마토](https://www.acmicpc.net/problem/7569)

## 설명

`M × N × H` 크기의 3차원 상자에 토마토가 보관되어 있습니다. 각 칸은 익은 토마토(`1`), 익지 않은 토마토(`0`), 또는 빈 칸(`-1`) 중 하나입니다.<br>

익은 토마토가 있으면 하루마다 상하좌우, 위아래 인접한 6방향의 익지 않은 토마토를 익게 합니다.

이때 모든 익은 토마토는 동시에 주변 토마토를 익히므로 여러 위치에서 동시에 확산이 일어납니다.<br>

처음부터 모든 토마토가 익어있거나, 토마토가 모두 익을 수 있다면 최소 며칠이 걸리는지 구합니다.

토마토가 모두 익지 못하는 상황이면 `-1`을 출력합니다.<br>

`M`, `N`, `H`는 각각 최대 `100`입니다.<br>

<br>

## 접근법

BFS를 사용하여 토마토가 동시에 익어가는 과정을 시뮬레이션합니다.

모든 익은 토마토를 큐에 먼저 넣고 시작합니다.

하루 단위로 BFS를 진행하며, 큐에 있는 현재 단계의 모든 토마토를 꺼내어 각각 6방향(상하좌우위아래)으로 인접한 칸을 확인합니다.

익지 않은 토마토(`0`)를 만나면 익은 상태로 바꾸고 큐에 추가합니다.<br>

BFS가 끝나면 상자 전체를 확인합니다. 익지 않은 토마토가 남아있으면 `-1`을 출력하고, 모두 익었다면 걸린 일수를 출력합니다.<br>

처음부터 모든 토마토가 익어있는 경우는 `0`을 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    struct Point {
      public int Z, Y, X;
    }

    static readonly int[] dz = { 1, -1, 0, 0, 0, 0 };
    static readonly int[] dy = { 0, 0, 1, -1, 0, 0 };
    static readonly int[] dx = { 0, 0, 0, 0, 1, -1 };

    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var m = int.Parse(tokens[0]);
      var n = int.Parse(tokens[1]);
      var h = int.Parse(tokens[2]);

      var board = new int[h, n, m];
      var queue = new Queue<Point>();
      for (var z = 0; z < h; z++) {
        for (var y = 0; y < n; y++) {
          var row = Console.ReadLine()!.Split();
          for (var x = 0; x < m; x++) {
            board[z, y, x] = int.Parse(row[x]);
            if (board[z, y, x] == 1)
              queue.Enqueue(new Point { Z = z, Y = y, X = x });
          }
        }
      }

      var days = Bfs(queue, board, h, n, m);
      Console.WriteLine(days);
    }

    static int Bfs(Queue<Point> queue, int[,,] board, int h, int n, int m) {
      var days = -1;
      while (queue.Count > 0) {
        var size = queue.Count;
        days++;

        for (var i = 0; i < size; i++) {
          var cur = queue.Dequeue();
          for (var dir = 0; dir < 6; dir++) {
            var nz = cur.Z + dz[dir];
            var ny = cur.Y + dy[dir];
            var nx = cur.X + dx[dir];
            if (nz < 0 || nz >= h || ny < 0 || ny >= n || nx < 0 || nx >= m) continue;
            if (board[nz, ny, nx] != 0) continue;

            board[nz, ny, nx] = 1;
            queue.Enqueue(new Point { Z = nz, Y = ny, X = nx });
          }
        }
      }

      for (var z = 0; z < h; z++)
        for (var y = 0; y < n; y++)
          for (var x = 0; x < m; x++)
            if (board[z, y, x] == 0)
              return -1;

      return Math.Max(days, 0);
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
typedef vector<vvi> vvvi;

struct Point { int z, y, x; };

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int m, n, h; cin >> m >> n >> h;
  vvvi board(h, vvi(n, vi(m)));
  queue<Point> q;

  for (int z = 0; z < h; ++z)
    for (int y = 0; y < n; ++y)
      for (int x = 0; x < m; ++x) {
        cin >> board[z][y][x];
        if (board[z][y][x] == 1)
          q.push({z, y, x});
      }

  int dz[6] = { 1, -1, 0, 0, 0, 0 };
  int dy[6] = { 0, 0, 1, -1, 0, 0 };
  int dx[6] = { 0, 0, 0, 0, 1, -1 };

  int days = -1;
  while (!q.empty()) {
    int size = q.size();
    ++days;

    for (int i = 0; i < size; ++i) {
      auto cur = q.front(); q.pop();
      for (int dir = 0; dir < 6; ++dir) {
        int nz = cur.z + dz[dir], ny = cur.y + dy[dir], nx = cur.x + dx[dir];
        if (nz < 0 || nz >= h || ny < 0 || ny >= n || nx < 0 || nx >= m) continue;
        if (board[nz][ny][nx] != 0) continue;

        board[nz][ny][nx] = 1;
        q.push({nz, ny, nx});
      }
    }
  }

  for (int z = 0; z < h; ++z)
    for (int y = 0; y < n; ++y)
      for (int x = 0; x < m; ++x)
        if (board[z][y][x] == 0) {
          cout << -1 << "\n";
          return 0;
        }

  cout << max(days, 0) << "\n";

  return 0;
}
```

