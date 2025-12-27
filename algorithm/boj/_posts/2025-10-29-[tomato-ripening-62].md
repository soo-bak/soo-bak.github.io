---
layout: single
title: "[백준 7576] 토마토 (C#, C++) - soo:bak"
date: "2025-10-29 00:25:00 +0900"
description: 여러 익은 토마토에서 동시에 확산되는 BFS로 모든 토마토가 익는 최소 일수를 구하는 백준 7576번 토마토 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 7576
  - C#
  - C++
  - 알고리즘
  - BFS
  - 그래프
  - graph_traversal
  - grid_graph
  - 최단경로
keywords: "백준 7576, 백준 7576번, BOJ 7576, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[7576번 - 토마토](https://www.acmicpc.net/problem/7576)

## 설명

`M × N` 크기의 격자에서 익은 토마토(`1`)가 하루마다 상하좌우로 인접한 익지 않은 토마토(`0`)를 익게 만드는 문제입니다.<br>

비어 있는 칸(`-1`)은 토마토가 없으며, 모든 토마토가 익는 데 걸리는 최소 일수를 구해야 합니다.<br>

처음부터 모든 토마토가 익어 있다면 `0`을, 끝까지 익지 못하는 토마토가 남아 있다면 `-1`을 출력합니다.<br>

<br>

## 접근법

여러 출발점에서 동시에 확산되는 멀티 소스 BFS(Multi-source BFS)를 사용합니다.

처음에 익어 있는 모든 토마토의 위치를 큐에 넣고 BFS를 시작합니다.

각 토마토는 상하좌우 4방향으로 인접한 익지 않은 토마토를 익게 만들며, 이 과정을 큐가 빌 때까지 반복합니다.

BFS 탐색이 끝난 후, 격자를 순회하여 익지 않은 토마토가 남아 있는지 확인합니다.

남아 있다면 `-1`을, 모두 익었다면 마지막 날짜를 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static void Main() {
    var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    var m = tokens[0];
    var n = tokens[1];

    var box = new int[n, m];
    var queue = new Queue<(int r, int c)>();

    for (var r = 0; r < n; r++) {
      var row = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      for (var c = 0; c < m; c++) {
        box[r, c] = row[c];
        if (box[r, c] == 1)
          queue.Enqueue((r, c));
      }
    }

    var dr = new[] { -1, 1, 0, 0 };
    var dc = new[] { 0, 0, -1, 1 };

    while (queue.Count > 0) {
      var (r, c) = queue.Dequeue();
      for (var d = 0; d < 4; d++) {
        var nr = r + dr[d];
        var nc = c + dc[d];
        if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
        if (box[nr, nc] != 0) continue;
        box[nr, nc] = box[r, c] + 1;
        queue.Enqueue((nr, nc));
      }
    }

    var days = 0;
    for (var r = 0; r < n; r++) {
      for (var c = 0; c < m; c++) {
        if (box[r, c] == 0) {
          Console.WriteLine(-1);
          return;
        }
        if (box[r, c] > days) days = box[r, c];
      }
    }

    Console.WriteLine(days <= 1 ? 0 : days - 1);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<int, int> pii;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int m, n;
  cin >> m >> n;

  vector<vector<int>> box(n, vector<int>(m));
  queue<pii> q;

  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < m; ++c) {
      cin >> box[r][c];
      if (box[r][c] == 1)
        q.emplace(r, c);
    }
  }

  int dr[4] = {-1, 1, 0, 0};
  int dc[4] = {0, 0, -1, 1};

  while (!q.empty()) {
    auto [r, c] = q.front();
    q.pop();
    for (int d = 0; d < 4; ++d) {
      int nr = r + dr[d];
      int nc = c + dc[d];
      if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
      if (box[nr][nc] != 0) continue;
      box[nr][nc] = box[r][c] + 1;
      q.emplace(nr, nc);
    }
  }

  int days = 0;
  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < m; ++c) {
      if (box[r][c] == 0) {
        cout << -1 << "\n";
        return 0;
      }
      days = max(days, box[r][c]);
    }
  }

  cout << (days <= 1 ? 0 : days - 1) << "\n";
  return 0;
}
```

