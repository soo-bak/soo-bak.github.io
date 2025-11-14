---
layout: single
title: "[백준 2178] 미로 탐색 (C#, C++) - soo:bak"
date: "2025-11-08 23:29:00 +0900"
description: 1로 이동 가능한 칸만 따라 BFS로 (1,1)에서 (N,M)까지의 최단 경로 길이를 구하는 백준 2178번 미로 탐색 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[2178번 - 미로 탐색](https://www.acmicpc.net/problem/2178)

## 설명

`N × M` 크기의 미로에서 시작 위치 `(1, 1)`에서 도착 위치 `(N, M)`까지 이동하는 최소 칸 수를 구하는 문제입니다.<br>

미로에서 `1`은 이동 가능한 칸, `0`은 벽을 나타내며, 상하좌우로 인접한 칸으로만 이동할 수 있습니다.<br>

시작 칸과 도착 칸도 이동 횟수에 포함되며, 입력으로 주어지는 모든 미로는 항상 도착 가능함이 보장됩니다.<br>

<br>

## 접근법

최단 경로를 구하는 문제이므로 너비 우선 탐색(BFS)을 사용합니다.

모든 칸의 이동 비용이 `1`로 동일하기 때문에, BFS로 처음 도착 칸에 도달했을 때의 거리가 최단 거리입니다.

시작점 `(0, 0)`을 거리 `1`로 설정하여 큐에 넣고 BFS를 시작합니다. 상하좌우 4방향으로 인접한 칸을 탐색하며, 범위를 벗어나거나 벽이거나 이미 방문한 칸은 건너뜁니다.

방문 가능한 칸은 현재 거리에 `1`을 더한 값으로 거리를 갱신하고 큐에 추가합니다. 이 과정을 반복하여 도착 칸 `(N-1, M-1)`에 도달했을 때의 거리를 출력합니다.

<br>
시간 복잡도는 $$O(N \times M)$$으로, 최대 `100 × 100` 크기의 미로도 효율적으로 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var n = tokens[0];
      var m = tokens[1];

      var grid = new int[n, m];
      for (var r = 0; r < n; r++) {
        var line = Console.ReadLine()!;
        for (var c = 0; c < m; c++)
          grid[r, c] = line[c] - '0';
      }

      var visited = new bool[n, m];
      var dist = new int[n, m];

      var dr = new[] { -1, 1, 0, 0 };
      var dc = new[] { 0, 0, -1, 1 };

      var queue = new Queue<(int r, int c)>();
      visited[0, 0] = true;
      dist[0, 0] = 1;
      queue.Enqueue((0, 0));

      while (queue.Count > 0) {
        var (r, c) = queue.Dequeue();
        for (var d = 0; d < 4; d++) {
          var nr = r + dr[d];
          var nc = c + dc[d];
          if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
          if (visited[nr, nc] || grid[nr, nc] == 0) continue;
          visited[nr, nc] = true;
          dist[nr, nc] = dist[r, c] + 1;
          queue.Enqueue((nr, nc));
        }
      }

      Console.WriteLine(dist[n - 1, m - 1]);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<int, int> pii;
typedef vector<int> vi;
typedef vector<vi> vvi;
typedef vector<bool> vb;
typedef vector<vb> vvb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vvi grid(n, vi(m));
  for (int r = 0; r < n; ++r) {
    string line; cin >> line;
    for (int c = 0; c < m; ++c)
      grid[r][c] = line[c] - '0';
  }

  vvb visited(n, vb(m, false));
  visited[0][0] = true;

  vvi dist(n, vi(m, 0));
  dist[0][0] = 1;

  queue<pii> q;
  q.emplace(0, 0);

  int dr[4] = {-1, 1, 0, 0};
  int dc[4] = {0, 0, -1, 1};

  while (!q.empty()) {
    auto [r, c] = q.front();
    q.pop();
    for (int d = 0; d < 4; ++d) {
      int nr = r + dr[d], nc = c + dc[d];
      if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
      if (visited[nr][nc] || grid[nr][nc] == 0) continue;

      visited[nr][nc] = true;
      dist[nr][nc] = dist[r][c] + 1;
      q.emplace(nr, nc);
    }
  }

  cout << dist[n - 1][m - 1] << "\n";
  
  return 0;
}
```

