---
layout: single
title: "[백준 2667] 단지번호붙이기 (C#, C++) - soo:bak"
date: "2025-11-15 00:10:00 +0900"
description: 2차원 지도에서 DFS/BFS로 단지를 찾고 각 단지의 크기를 정렬해 출력하는 백준 2667번 단지번호붙이기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2667
  - C#
  - C++
  - 알고리즘
  - 그래프
  - graph_traversal
  - BFS
  - DFS
  - grid_graph
keywords: "백준 2667, 백준 2667번, BOJ 2667, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2667번 - 단지번호붙이기](https://www.acmicpc.net/problem/2667)

## 설명

상하좌우로 연결된 집들의 모임을 하나의 단지로 정의할 때, 총 단지 수와 각 단지에 속하는 집의 수를 오름차순으로 출력하는 문제입니다.<br>

`N × N` 크기의 지도에서 집이 있는 곳은 `1`, 집이 없는 곳은 `0`으로 표시됩니다.<br>

`N`은 최대 `25`까지 주어집니다.<br>

<br>

## 접근법

너비 우선 탐색(BFS)을 사용하여 연결된 집들을 탐색합니다.

지도를 순회하면서 아직 방문하지 않은 집(`1`)을 발견하면 해당 위치에서 BFS를 시작합니다.

BFS를 통해 상하좌우로 연결된 모든 집을 방문하며 단지의 크기를 카운트합니다.

<br>
각 BFS 탐색이 끝날 때마다 해당 단지의 크기를 리스트에 저장합니다.

모든 탐색이 끝나면 단지 크기 리스트를 오름차순으로 정렬하여 출력합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static int n;
    static int[,] board;
    static bool[,] visited;
    static readonly int[] dr = { -1, 1, 0, 0 };
    static readonly int[] dc = { 0, 0, -1, 1 };

    static int BFS(int sr, int sc) {
      var queue = new Queue<(int r, int c)>();
      visited[sr, sc] = true;
      queue.Enqueue((sr, sc));
      var count = 1;

      while (queue.Count > 0) {
        var (r, c) = queue.Dequeue();
        for (var d = 0; d < 4; d++) {
          var nr = r + dr[d];
          var nc = c + dc[d];
          if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
          if (visited[nr, nc] || board[nr, nc] == 0) continue;
          visited[nr, nc] = true;
          queue.Enqueue((nr, nc));
          count++;
        }
      }

      return count;
    }

    static void Main(string[] args) {
      n = int.Parse(Console.ReadLine()!);
      board = new int[n, n];
      visited = new bool[n, n];

      for (var r = 0; r < n; r++) {
        var line = Console.ReadLine()!;
        for (var c = 0; c < n; c++)
          board[r, c] = line[c] - '0';
      }

      var sizes = new List<int>();
      for (var r = 0; r < n; r++) {
        for (var c = 0; c < n; c++) {
          if (board[r, c] == 1 && !visited[r, c])
            sizes.Add(BFS(r, c));
        }
      }

      sizes.Sort();
      Console.WriteLine(sizes.Count);
      Console.WriteLine(string.Join("\n", sizes));
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
typedef vector<bool> vb;
typedef vector<vb> vvb;
typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vs board(n);
  for (int i = 0; i < n; ++i)
    cin >> board[i];

  vvb visited(n, vb(n, false));
  vi sizes;
  int dr[4] = { -1, 1, 0, 0 };
  int dc[4] = { 0, 0, -1, 1 };

  for (int r = 0; r < n; ++r) {
    for (int c = 0; c < n; ++c) {
      if (board[r][c] == '1' && !visited[r][c]) {
        queue<pii> q;
        visited[r][c] = true;
        q.emplace(r, c);
        int count = 1;

        while (!q.empty()) {
          auto [cr, cc] = q.front();
          q.pop();
          for (int d = 0; d < 4; ++d) {
            int nr = cr + dr[d];
            int nc = cc + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
            if (visited[nr][nc] || board[nr][nc] != '1') continue;
            visited[nr][nc] = true;
            q.emplace(nr, nc);
            ++count;
          }
        }

        sizes.push_back(count);
      }
    }
  }

  sort(sizes.begin(), sizes.end());
  cout << sizes.size() << "\n";
  for (int size : sizes)
    cout << size << "\n";

  return 0;
}
```

