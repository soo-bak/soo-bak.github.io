---
layout: single
title: "[백준 1012] 유기농 배추 (C#, C++) - soo:bak"
date: "2025-05-19 03:25:00 +0900"
description: 인접한 배추 그룹을 DFS로 탐색하여 필요한 지렁이 수를 구하는 백준 1012번 유기농 배추 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[1012번 - 유기농 배추](https://www.acmicpc.net/problem/1012)

## 설명

**배추가 심어진 위치들이 주어졌을 때 서로 맞닿아 있는 배추들을 하나의 묶음으로 보고,**

**그 묶음마다 지렁이 한 마리가 필요하다고 할 때 총 몇 마리의 지렁이가 필요한지를 구하는 문제입니다.**

<br>
배추는 밭 위에 띄엄띄엄 심겨 있으며, 각 배추는 다른 배추와 상하좌우 방향으로 인접해 있을 수 있습니다.

인접한 배추들은 함께 묶여 있어, 하나의 지렁이로 연결된 배추들 사이의 해충을 막을 수 있습니다.

<br>
입력으로는 밭의 크기와 배추의 좌표들이 주어지며, 각 테스트케이스마다 필요한 지렁이 수를 하나씩 출력해야 합니다.

<br>

## 접근법

이러한 문제는 **2차원 그래프에서의 연결 요소 개수 세기 문제**로 변환하여 풀이할 수 있습니다.

각 배추밭의 상태를 `가로 M`, `세로 N` 크기의 격자로 표현하며,

입력으로 주어지는 배추가 심어진 좌표를 바탕으로 전체 밭의 상태를 2차원 배열로 구성합니다.

이 때, 배추가 심어진 좌표는 `1`로 표시하고, 심어지지 않은 곳은 기본값 `0`으로 유지합니다.

<br>
이후 전체 격자 칸을 하나씩 확인하면서, **아직 방문하지 않은 배추**를 발견할 경우 새로운 탐색을 시작합니다.

<br>
탐색은 **상하좌우로 연결된 배추들을 모두 방문 처리**하는 방식으로 진행하며,

하나의 탐색이 끝날 때마다 연결된 배추 무리를 하나 처리한 것이므로 필요한 지렁이 수를 `1`만큼 늘려줍니다.

<br>
이 과정을 밭 전체에 대하여 반복하면, 최종적으로 총 몇 마리의 지렁이가 필요한지 구할 수 있습니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Linq;

class Program {
  static int[,] field;
  static bool[,] visited;
  static int m, n;

  static void DFS(int r, int c) {
    if (r < 0 || r >= n || c < 0 || c >= m) return;
    if (visited[r, c] || field[r, c] == 0) return;

    visited[r, c] = true;
    int[] dr = {-1, 1, 0, 0};
    int[] dc = {0, 0, -1, 1};

    for (int i = 0; i < 4; i++)
      DFS(r + dr[i], c + dc[i]);
  }

  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      var tokens = Console.ReadLine().Split().Select(int.Parse).ToArray();
      m = tokens[0]; n = tokens[1];
      int k = tokens[2];

      field = new int[n, m];
      visited = new bool[n, m];

      for (int i = 0; i < k; i++) {
        var pos = Console.ReadLine().Split().Select(int.Parse).ToArray();
        field[pos[1], pos[0]] = 1;
      }

      int cnt = 0;
      for (int r = 0; r < n; r++) {
        for (int c = 0; c < m; c++) {
          if (field[r, c] == 1 && !visited[r, c]) {
            cnt++;
            DFS(r, c);
          }
        }
      }
      Console.WriteLine(cnt);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>

using namespace std;
typedef vector<int> vi;
typedef vector<bool> vb;
typedef vector<vi> vvi;
typedef vector<vb> vvb;
typedef pair<int, int> pii;

vvi field;
vvb visited;
int col, row, cntCab;
int cntWorm = 0;

void solve(pii start) {
  int r = start.first, c = start.second;
  if (r < 0 || c < 0 || r >= row || c >= col) return;
  if (visited[r][c] || !field[r][c]) return;

  visited[r][c] = true;
  int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
  for (int i = 0; i < 4; i++)
    solve({r + dr[i], c + dc[i]});
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    cin >> col >> row >> cntCab;

    visited.clear();
    field.clear();
    visited.resize(row, vb(col, false));
    field.resize(row, vi(col, 0));
    for (int i = 0; i < cntCab; i++) {
      int c, r; cin >> c >> r;
      field[r][c] = 1;
    }
    cntWorm = 0;
    for (int r = 0; r < row; r++) {
      for (int c = 0; c < col; c++) {
        if (field[r][c] && !visited[r][c]) {
          cntWorm++;
          solve({r, c});
        }
      }
    }
    cout << cntWorm << "\n";
  }

  return 0;
}
```
