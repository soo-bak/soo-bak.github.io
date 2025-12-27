---
layout: single
title: "[백준 2606] 바이러스 (C#, C++) - soo:bak"
date: "2025-10-27 22:20:00 +0900"
description: 그래프 탐색으로 1번 컴퓨터에서 감염이 전파되는 범위를 세는 백준 2606번 바이러스 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2606
  - C#
  - C++
  - 알고리즘
keywords: "백준 2606, 백준 2606번, BOJ 2606, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2606번 - 바이러스](https://www.acmicpc.net/problem/2606)

## 설명

네트워크를 무방향 그래프로 모델링하여, 1번 컴퓨터에서 시작한 바이러스가 연결된 경로를 통해 확산되는 범위를 구하는 문제입니다.<br>

1번 컴퓨터를 제외하고 감염되는 컴퓨터의 개수를 계산해야 합니다.<br>

<br>

## 접근법

1번 컴퓨터에서 도달 가능한 모든 컴퓨터를 찾기 위해 그래프 탐색을 사용합니다.

인접 리스트로 그래프를 구성한 후, 1번 노드에서 BFS 또는 DFS를 수행하여 방문한 노드의 개수를 셉니다. 최종 답은 방문한 노드 수에서 시작점인 1번을 제외한 값입니다.

<br>
컴퓨터 수가 최대 `100`대로 작기 때문에 시간 복잡도는 $$O(V + E)$$로 충분합니다.

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
    var n = int.Parse(Console.ReadLine()!);
    var m = int.Parse(Console.ReadLine()!);

    var adj = Enumerable.Range(0, n + 1)
      .Select(_ => new List<int>())
      .ToArray();

    foreach (var _ in Enumerable.Range(0, m)) {
      var edge = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var u = edge[0];
      var v = edge[1];
      adj[u].Add(v);
      adj[v].Add(u);
    }

    var visited = new bool[n + 1];
    var queue = new Queue<int>();
    visited[1] = true;
    queue.Enqueue(1);
    var count = 0;

    while (queue.Count > 0) {
      var cur = queue.Dequeue();
      foreach (var next in adj[cur]) {
        if (visited[next]) continue;
        visited[next] = true;
        queue.Enqueue(next);
        count++;
      }
    }

    Console.WriteLine(count);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;

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

  vector<bool> visited(n + 1, false);
  queue<int> q;
  visited[1] = true;
  q.push(1);
  int count = 0;
  while (!q.empty()) {
    int cur = q.front();
    q.pop();
    for (int next : adj[cur]) {
      if (visited[next]) continue;
      visited[next] = true;
      q.push(next);
      ++count;
    }
  }

  cout << count << "\n";
  
  return 0;
}
```

