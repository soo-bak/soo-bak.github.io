---
layout: single
title: "[백준 1389] 케빈 베이컨의 6단계 법칙 (C#, C++) - soo:bak"
date: "2025-10-24 23:54:00 +0900"
description: 모든 사용자 쌍의 최단 연락 단계를 합산해 케빈 베이컨 수가 가장 작은 사용자를 찾는 백준 1389번 케빈 베이컨의 6단계 법칙 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1389
  - C#
  - C++
  - 알고리즘
keywords: "백준 1389, 백준 1389번, BOJ 1389, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1389번 - 케빈 베이컨의 6단계 법칙](https://www.acmicpc.net/problem/1389)

## 설명

각 유저는 서로 친구 관계로 연결된 무방향 그래프의 정점으로 볼 수 있습니다.<br>

이 때, **임의의 두 사람이 몇 단계 만에 이어질 수 있는지**는 그래프 상의 최단 거리로 해석할 수 있습니다.<br>

따라서, 한 사용자의 `케빈 베이컨 수`는 **모든 다른 사용자까지의 최단 거리 합**이 됩니다.<br>

<br>
목표는 **케빈 베이컨 수의 합이 가장 작은 사용자**를 찾는 것이며,<br>

동점일 경우 **번호가 가장 작은 사용자**를 출력해야 합니다.<br>

<br>

## 접근법

`N`이 최대 `100`이므로, **각 정점을 시작점으로 하는 BFS**(너비 우선 탐색)를 반복해도 충분히 빠르게 해결됩니다.

- 그래프는 인접 리스트로 저장하고, 매 탐색마다 방문 배열과 거리 배열을 초기화합니다.
- 각 시작점에서 BFS를 수행하여 **최단 거리 합을 계산**합니다.
- 최소 합을 갱신할 때, 동률이라면 문제의 조건에 따라 **더 작은 번호를 유지**합니다.

<br>
모든 정점이 연결되어 있다는 조건 덕분에 BFS가 항상 모든 정점을 방문하므로, 시작점마다의 거리 합이 정확히 계산됩니다.

<br>

> 참고 : [그래프 탐색 - DFS와 BFS - soo:bak](https://soo-bak.github.io/algorithm/theory/graph-traversal-dfs-bfs/)

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
    var n = tokens[0];
    var m = tokens[1];

    var adj = Enumerable.Range(0, n + 1)
      .Select(_ => new List<int>())
      .ToArray();

    foreach (var _ in Enumerable.Range(0, m)) {
      var edge = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
      var a = edge[0];
      var b = edge[1];
      adj[a].Add(b);
      adj[b].Add(a);
    }

    foreach (var list in adj)
      list.Sort();

    var ans = 1;
    var best = int.MaxValue;
    var dist = new int[n + 1];

    for (var start = 1; start <= n; start++) {
      Array.Fill(dist, -1);
      var queue = new Queue<int>();
      dist[start] = 0;
      queue.Enqueue(start);

      while (queue.Count > 0) {
        var cur = queue.Dequeue();
        foreach (var next in adj[cur]) {
          if (dist[next] != -1) continue;
          dist[next] = dist[cur] + 1;
          queue.Enqueue(next);
        }
      }

      var sum = dist.Sum();
      if (sum < best) {
        best = sum;
        ans = start;
      }
    }

    Console.WriteLine(ans);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;
typedef queue<int> qi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vvi adj(n + 1);
  while (m--) {
    int a, b; cin >> a >> b;
    adj[a].push_back(b);
    adj[b].push_back(a);
  }

  for (int i = 1; i <= n; ++i)
    sort(adj[i].begin(), adj[i].end());

  int ans = 1, best = INT_MAX;
  vi dist(n + 1);

  for (int start = 1; start <= n; ++start) {
    fill(dist.begin(), dist.end(), -1);
    dist[start] = 0;
    qi q; q.push(start);

    while (!q.empty()) {
      int cur = q.front();
      q.pop();
      for (int next : adj[cur]) {
        if (dist[next] != -1) continue;
        dist[next] = dist[cur] + 1;
        q.push(next);
      }
    }

    int sum = 0;
    for (int v = 1; v <= n; ++v)
      sum += dist[v];

    if (sum < best) {
      best = sum;
      ans = start;
    }
  }

  cout << ans << "\n";

  return 0;
}
```
