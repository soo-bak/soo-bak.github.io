---
layout: single
title: "[백준 10026] 적록색약 (C#, C++) - soo:bak"
date: "2025-11-15 00:20:00 +0900"
description: 일반 시야와 적록색약 시야에서 각각의 영역 개수를 BFS/DFS로 계산하는 백준 10026번 적록색약 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 10026
  - C#
  - C++
  - 알고리즘
keywords: "백준 10026, 백준 10026번, BOJ 10026, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10026번 - 적록색약](https://www.acmicpc.net/problem/10026)

## 설명

`N × N` 크기의 그림에서 `R`(빨강), `G`(초록), `B`(파랑) 세 가지 색상으로 칠해진 영역의 개수를 구하는 문제입니다.<br>

상하좌우로 인접한 같은 색상의 칸들은 하나의 영역으로 간주합니다.<br>

보통 사람은 `R`, `G`, `B`를 모두 구분할 수 있지만, 적록색약인 사람은 `R`과 `G`를 같은 색으로 인식합니다.<br>

보통 사람이 보는 영역 개수와 적록색약인 사람이 보는 영역 개수를 각각 출력합니다.<br>

`N`은 최대 `100`까지 주어집니다.<br>

<br>

## 접근법

너비 우선 탐색(BFS)을 사용하여 연결된 영역을 탐색합니다.

보통 사람과 적록색약인 사람 각각에 대해 영역 개수를 세기 위해 BFS를 두 번 수행합니다.

<br>
첫 번째 탐색에서는 보통 사람의 시야로 영역을 셉니다. 같은 색상(`R`, `G`, `B`)의 칸끼리만 연결된 것으로 간주합니다.

<br>
두 번째 탐색에서는 적록색약인 사람의 시야로 영역을 셉니다. `R`과 `G`를 동일한 색으로 취급하여 연결 여부를 판단합니다. `B`는 여전히 독립적인 색상으로 구분합니다.

<br>
각 탐색마다 방문 배열을 새로 초기화하여 독립적으로 영역 개수를 카운트합니다.

색상 비교 로직은 별도의 함수로 분리하여 적록색약인 사람인지에 따라 다르게 동작하도록 구현합니다.

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
    static char[,] board;
    static bool[,] visited;
    static readonly int[] dr = { -1, 1, 0, 0 };
    static readonly int[] dc = { 0, 0, -1, 1 };

    static void BFS(int sr, int sc, bool colorBlind) {
      var queue = new Queue<(int r, int c)>();
      visited[sr, sc] = true;
      queue.Enqueue((sr, sc));
      char baseColor = board[sr, sc];

      while (queue.Count > 0) {
        var (r, c) = queue.Dequeue();
        for (var d = 0; d < 4; d++) {
          var nr = r + dr[d];
          var nc = c + dc[d];
          if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
          if (visited[nr, nc]) continue;
          if (!IsSameColor(baseColor, board[nr, nc], colorBlind)) continue;
          visited[nr, nc] = true;
          queue.Enqueue((nr, nc));
        }
      }
    }

    static bool IsSameColor(char a, char b, bool colorBlind) {
      if (!colorBlind) return a == b;
      if (a == 'B' || b == 'B') return a == b;
      return true;
    }

    static int CountRegions(bool colorBlind) {
      visited = new bool[n, n];
      var count = 0;
      for (var r = 0; r < n; r++) {
        for (var c = 0; c < n; c++) {
          if (!visited[r, c]) {
            BFS(r, c, colorBlind);
            count++;
          }
        }
      }
      return count;
    }

    static void Main(string[] args) {
      n = int.Parse(Console.ReadLine()!);
      board = new char[n, n];
      for (var i = 0; i < n; i++) {
        var line = Console.ReadLine()!;
        for (var j = 0; j < n; j++)
          board[i, j] = line[j];
      }

      var normal = CountRegions(false);
      var colorBlind = CountRegions(true);
      Console.WriteLine($"{normal} {colorBlind}");
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef pair<int, int> pii;
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

  auto bfs = [&](bool colorBlind) {
    vvb visited(n, vb(n, false));
    int count = 0;
    int dr[4] = { -1, 1, 0, 0 };
    int dc[4] = { 0, 0, -1, 1 };

    auto sameColor = [&](char a, char b) {
      if (!colorBlind) return a == b;
      if (a == 'B' || b == 'B') return a == b;
      return true;
    };

    for (int r = 0; r < n; ++r) {
      for (int c = 0; c < n; ++c) {
        if (visited[r][c]) continue;
        queue<pii> q;
        visited[r][c] = true;
        q.emplace(r, c);
        while (!q.empty()) {
          auto [cr, cc] = q.front();
          q.pop();
          for (int d = 0; d < 4; ++d) {
            int nr = cr + dr[d];
            int nc = cc + dc[d];
            if (nr < 0 || nr >= n || nc < 0 || nc >= n) continue;
            if (visited[nr][nc]) continue;
            if (!sameColor(board[cr][cc], board[nr][nc])) continue;
            visited[nr][nc] = true;
            q.emplace(nr, nc);
          }
        }
        ++count;
      }
    }

    return count;
  };

  int normal = bfs(false);
  int colorBlind = bfs(true);
  cout << normal << " " << colorBlind << "\n";

  return 0;
}
```

