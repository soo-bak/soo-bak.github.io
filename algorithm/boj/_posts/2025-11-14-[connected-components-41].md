---
layout: single
title: "[백준 11724] 연결 요소의 개수 (C#, C++) - soo:bak"
date: "2025-11-14 23:05:00 +0900"
description: 무방향 그래프에서 DFS/BFS로 연결 요소 개수를 세는 백준 11724번 연결 요소의 개수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11724
  - C#
  - C++
  - 알고리즘
  - 그래프
  - graph_traversal
  - BFS
  - DFS
keywords: "백준 11724, 백준 11724번, BOJ 11724, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11724번 - 연결 요소의 개수](https://www.acmicpc.net/problem/11724)

## 설명

`N`개의 정점과 `M`개의 간선으로 이루어진 무방향 그래프가 주어졌을 때, 연결 요소의 개수를 구하는 문제입니다.<br>

정점 번호는 `1`부터 시작하며, 중복 간선 없이 최대 `1,000`개의 정점이 주어집니다.<br>

<br>

## 접근법

연결 요소는 서로 연결된 정점들의 집합입니다.

방문하지 않은 정점을 시작점으로 DFS 또는 BFS를 수행하면 해당 연결 요소에 속한 모든 정점을 방문할 수 있습니다.

먼저 인접 리스트로 그래프를 표현하고, 방문 여부를 저장할 배열을 준비합니다.

정점 `1`부터 `N`까지 순회하면서 아직 방문하지 않은 정점을 발견하면 BFS를 시작하고 연결 요소 개수를 증가시킵니다.

<br>
BFS 과정에서는 현재 정점과 연결된 모든 인접 정점을 방문하며, 방문한 정점은 모두 같은 연결 요소에 속합니다.

모든 정점을 순회한 후, 총 BFS 시작 횟수가 연결 요소의 개수가 됩니다.

<br>
정점 수가 최대 `1,000`개로 작으므로, 인접 리스트와 BFS를 사용하면 충분히 빠르게 해결됩니다.

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

      var adj = new List<int>[n + 1];
      for (var i = 1; i <= n; i++)
        adj[i] = new List<int>();

      for (var i = 0; i < m; i++) {
        var edge = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
        var u = edge[0];
        var v = edge[1];
        adj[u].Add(v);
        adj[v].Add(u);
      }

      var visited = new bool[n + 1];
      var count = 0;
      for (var start = 1; start <= n; start++) {
        if (visited[start]) continue;
        count++;
        var queue = new Queue<int>();
        visited[start] = true;
        queue.Enqueue(start);

        while (queue.Count > 0) {
          var cur = queue.Dequeue();
          foreach (var next in adj[cur]) {
            if (visited[next]) continue;
            visited[next] = true;
            queue.Enqueue(next);
          }
        }
      }

      Console.WriteLine(count);
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vvi adj(n + 1);
  while (m--) {
    int u, v; cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }

  vb visited(n + 1, false);
  int count = 0;
  for (int start = 1; start <= n; ++start) {
    if (visited[start]) continue;
    count++;
    queue<int> q;
    visited[start] = true;
    q.push(start);

    while (!q.empty()) {
      int cur = q.front();
      q.pop();
      for (int next : adj[cur]) {
        if (visited[next]) continue;
        visited[next] = true;
        q.push(next);
      }
    }
  }

  cout << count << "\n";

  return 0;
}
```

