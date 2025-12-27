---
layout: single
title: "[백준 1926] 그림 (C#, C++) - soo:bak"
date: "2025-10-29 00:35:00 +0900"
description: 4방향 연결된 그림의 개수와 최대 넓이를 DFS/BFS로 구하는 백준 1926번 그림 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1926
  - C#
  - C++
  - 알고리즘
  - 그래프
  - graph_traversal
  - BFS
  - DFS
  - grid_graph
keywords: "백준 1926, 백준 1926번, BOJ 1926, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1926번 - 그림](https://www.acmicpc.net/problem/1926)

## 설명

`n × m` 크기의 도화지에서 가로 또는 세로로 연결된 `1`의 묶음을 하나의 그림으로 정의할 때,

도화지에 있는 그림의 개수와 가장 넓은 그림의 넓이를 구하는 문제입니다.<br>

그림의 넓이는 해당 그림에 포함된 `1`의 개수이며, 그림이 하나도 없으면 최대 넓이는 `0`입니다.<br>

<br>

## 접근법

연결된 영역을 찾는 전형적인 그래프 탐색 문제입니다.

도화지의 모든 칸을 순회하면서 방문하지 않은 `1`을 발견하면 BFS 또는 DFS를 시작합니다.

탐색을 통해 상하좌우로 연결된 모든 `1`을 방문하면서 넓이를 계산하고, 각 탐색마다 그림 개수를 증가시킵니다.

모든 탐색이 끝난 후, 찾은 그림의 개수와 그 중 최대 넓이를 출력합니다.

<br>
시간 복잡도는 $$O(n \times m)$$으로, 최대 `500 × 500` 크기의 도화지도 효율적으로 처리할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

class Program {
  static int[,] board;
  static bool[,] visited;
  static int n, m;
  static readonly int[] dr = { -1, 1, 0, 0 };
  static readonly int[] dc = { 0, 0, -1, 1 };

  static int BFS(int sr, int sc) {
    var queue = new Queue<(int r, int c)>();
    visited[sr, sc] = true;
    queue.Enqueue((sr, sc));
    var area = 0;

    while (queue.Count > 0) {
      var (r, c) = queue.Dequeue();
      area++;
      for (var d = 0; d < 4; d++) {
        var nr = r + dr[d];
        var nc = c + dc[d];
        if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
        if (visited[nr, nc] || board[nr, nc] == 0) continue;
        visited[nr, nc] = true;
        queue.Enqueue((nr, nc));
      }
    }
    return area;
  }

  static void Main() {
    var tokens = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    n = tokens[0];
    m = tokens[1];

    board = new int[n, m];
    visited = new bool[n, m];
    for (var r = 0; r < n; r++) {
      var row = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      for (var c = 0; c < m; c++)
        board[r, c] = row[c];
    }

    var count = 0;
    var maxArea = 0;
    for (var r = 0; r < n; r++) {
      for (var c = 0; c < m; c++) {
        if (board[r, c] == 1 && !visited[r, c]) {
          count++;
          var area = BFS(r, c);
          if (area > maxArea) maxArea = area;
        }
      }
    }

    Console.WriteLine(count);
    Console.WriteLine(maxArea);
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

  int n, m;
  cin >> n >> m;

  vvi board(n, vi(m));
  vvb visited(n, vb(m, false));
  for (int r = 0; r < n; ++r)
    for (int c = 0; c < m; ++c)
      cin >> board[r][c];

  int dr[4] = {-1, 1, 0, 0};
  int dc[4] = {0, 0, -1, 1};

  int count = 0, maxArea = 0;

  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < m; ++c) {
      if (board[r][c] == 0 || visited[r][c]) continue;
      ++count;

      queue<pii> q;
      visited[r][c] = true;
      q.emplace(r, c);
      int area = 0;

      while (!q.empty()) {
        auto [r, c] = q.front();
        q.pop();
        ++area;
        for (int d = 0; d < 4; ++d) {
          int nr = r + dr[d];
          int nc = c + dc[d];
          if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
          if (visited[nr][nc] || board[nr][nc] == 0) continue;
          visited[nr][nc] = true;
          q.emplace(nr, nc);
        }
      }

      maxArea = max(maxArea, area);
    }
  }

  cout << count << "\n" << maxArea << "\n";
  return 0;
}
```

