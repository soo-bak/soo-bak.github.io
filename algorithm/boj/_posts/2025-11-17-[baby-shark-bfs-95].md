---
layout: single
title: "[백준 16236] 아기 상어 (C#, C++) - soo:bak"
date: "2025-11-17 23:05:00 +0900"
description: BFS로 가장 가까운 먹잇감을 찾고, 먹을 때마다 크기와 시간을 갱신하는 백준 16236번 아기 상어 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 16236
  - C#
  - C++
  - 알고리즘
  - 구현
  - 그래프
  - graph_traversal
  - 시뮬레이션
  - BFS
keywords: "백준 16236, 백준 16236번, BOJ 16236, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16236번 - 아기 상어](https://www.acmicpc.net/problem/16236)

## 설명

`N × N` 크기의 공간에 아기 상어와 물고기들이 있습니다. 아기 상어는 초기 크기가 `2`이며, 상하좌우로 한 칸씩 이동할 수 있습니다.<br>

아기 상어는 자신보다 큰 물고기가 있는 칸은 지나갈 수 없고, 자신보다 작은 물고기만 먹을 수 있습니다. 크기가 같은 물고기는 먹을 수 없지만 지나갈 수는 있습니다.<br>

먹을 수 있는 물고기가 여러 마리라면 다음 우선순위로 선택합니다.

- 첫 번째, 가장 가까운 물고기.
- 두 번째, 가장 위쪽에 있는 물고기.
- 세 번째, 가장 왼쪽에 있는 물고기입니다.<br>

아기 상어가 자신의 크기와 같은 수의 물고기를 먹으면 크기가 `1` 증가합니다.

예를 들어 크기가 `2`일 때 물고기를 `2`마리 먹으면 크기가 `3`이 됩니다.<br>

더 이상 먹을 수 있는 물고기가 없을 때까지 걸린 시간을 구해야 합니다. `N`은 `2` 이상 `20` 이하입니다.<br>

<br>

## 접근법

BFS를 반복하여 먹을 수 있는 가장 가까운 물고기를 찾고, 먹은 후 상태를 갱신하는 방식으로 해결합니다.

현재 아기 상어의 위치에서 BFS를 시작합니다.

`자신보다 큰 물고기가 있는 칸은 지나갈 수 없으므로, 크기 이하의 칸만 이동합니다.

<br>
BFS 탐색 중 자신보다 작은 물고기를 만나면 후보로 저장합니다.

모든 탐색이 끝나면 우선순위(거리 → 행 → 열)에 따라 가장 적합한 물고기를 선택합니다.

<br>
선택한 물고기를 먹으면 해당 위치로 이동하고, 걸린 시간을 누적합니다.

먹은 물고기 수를 증가시키고, 크기와 같아지면 크기를 `1` 증가시킨 뒤 먹은 수를 `0`으로 초기화합니다.

<br>
더 이상 먹을 수 있는 물고기가 없을 때까지 이 과정을 반복합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    struct Shark {
      public int R, C, Size, Eaten, Time;
    }

    struct Node : IComparable<Node> {
      public int R, C, Dist;
      public int CompareTo(Node other) {
        if (Dist != other.Dist) return Dist - other.Dist;
        if (R != other.R) return R - other.R;
        return C - other.C;
      }
    }

    static readonly int[] dr = { -1, 0, 0, 1 };
    static readonly int[] dc = { 0, -1, 1, 0 };

    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var board = new int[n, n];
      var shark = new Shark { Size = 2 };

      for (var r = 0; r < n; r++) {
        var row = Console.ReadLine()!.Split();
        for (var c = 0; c < n; c++) {
          board[r, c] = int.Parse(row[c]);
          if (board[r, c] == 9) {
            board[r, c] = 0;
            shark.R = r;
            shark.C = c;
          }
        }
      }

      while (true) {
        var visited = new bool[n, n];
        var q = new Queue<Node>();
        var pq = new SortedSet<Node>();
        q.Enqueue(new Node { R = shark.R, C = shark.C, Dist = 0 });
        visited[shark.R, shark.C] = true;

        while (q.Count > 0) {
          var cur = q.Dequeue();
          for (var dir = 0; dir < 4; dir++) {
            var nr = cur.R + dr[dir];
            var nc = cur.C + dc[dir];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
            if (visited[nr, nc]) continue;
            if (board[nr, nc] > shark.Size) continue;

            visited[nr, nc] = true;
            var next = new Node { R = nr, C = nc, Dist = cur.Dist + 1 };
            q.Enqueue(next);
            if (board[nr, nc] != 0 && board[nr, nc] < shark.Size)
              pq.Add(next);
          }
        }

        if (pq.Count == 0) break;

        var target = pq.Min;
        board[target.R, target.C] = 0;
        shark.R = target.R;
        shark.C = target.C;
        shark.Time += target.Dist;
        shark.Eaten++;
        if (shark.Eaten == shark.Size) {
          shark.Size++;
          shark.Eaten = 0;
        }
      }

      Console.WriteLine(shark.Time);
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
typedef vector<bool> vb;
typedef vector<vb> vvb;

struct Node {
  int r, c, dist;
};

struct Target {
  int r, c, dist;
  bool operator<(const Target& other) const {
    if (dist != other.dist) return dist > other.dist;
    if (r != other.r) return r > other.r;
    return c > other.c;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvi board(n, vi(n));
  int sr = 0, sc = 0, size = 2, eaten = 0, totalTime = 0;

  for (int r = 0; r < n; ++r)
    for (int c = 0; c < n; ++c) {
      cin >> board[r][c];
      if (board[r][c] == 9) {
        sr = r; sc = c;
        board[r][c] = 0;
      }
    }

  int dr[4] = {-1, 0, 0, 1};
  int dc[4] = {0, -1, 1, 0};

  while (true) {
    vvb visited(n, vb(n, false));
    queue<Node> q;
    priority_queue<Target> pq;
    q.push({sr, sc, 0});
    visited[sr][sc] = true;

    while (!q.empty()) {
      auto [r, c, dist] = q.front(); q.pop();
      for (int dir = 0; dir < 4; ++dir) {
        int nr = r + dr[dir], nc = c + dc[dir];
        if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
        if (visited[nr][nc]) continue;
        if (board[nr][nc] > size) continue;

        visited[nr][nc] = true;
        q.push({nr, nc, dist + 1});
        if (board[nr][nc] > 0 && board[nr][nc] < size)
          pq.push({nr, nc, dist + 1});
      }
    }

    if (pq.empty()) break;

    auto target = pq.top(); pq.pop();
    sr = target.r;
    sc = target.c;
    totalTime += target.dist;
    board[sr][sc] = 0;
    if (++eaten == size) {
      eaten = 0;
      ++size;
    }
  }

  cout << totalTime << "\n";

  return 0;
}
```

