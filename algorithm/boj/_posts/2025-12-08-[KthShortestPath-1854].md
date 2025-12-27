---
layout: single
title: "[백준 1854] K번째 최단경로 찾기 (C#, C++) - soo:bak"
date: "2025-12-08 03:05:00 +0900"
description: 각 정점별 상위 k개 경로 비용을 우선순위 큐로 관리해 k번째 최단경로를 구하는 백준 1854번 K번째 최단경로 찾기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1854
  - C#
  - C++
  - 알고리즘
  - 자료구조
  - 그래프
  - 최단경로
  - 다익스트라
  - 우선순위큐
keywords: "백준 1854, 백준 1854번, BOJ 1854, KthShortestPath, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1854번 - K번째 최단경로 찾기](https://www.acmicpc.net/problem/1854)

## 설명
1번 정점에서 각 정점으로 가는 k번째 최단 경로의 비용을 구하는 문제입니다. 최단 경로가 아니라 k번째로 짧은 경로를 찾아야 합니다.

<br>

## 접근법
일반적인 다익스트라에서는 각 정점에 최단 거리 하나만 저장합니다. 이 문제에서는 k번째까지 필요하므로 각 정점마다 지금까지 발견한 경로 비용 중 짧은 것 k개를 저장해야 합니다.

각 정점에 최대 힙을 두고 크기를 k개로 유지합니다. 최대 힙을 쓰는 이유는 가장 큰 값을 빠르게 확인하고 제거하기 위해서입니다. 새로운 경로가 발견되었을 때, 힙에 k개 미만이 들어있으면 그냥 넣습니다. 이미 k개가 있다면 힙의 최댓값과 비교해서, 새 경로가 더 짧을 때만 최댓값을 빼고 새 경로를 넣습니다. 새 경로가 더 길거나 같으면 k번째 안에 들 수 없으므로 무시합니다.

다익스트라처럼 비용이 작은 순서로 상태를 꺼내면서 인접 정점으로 확장합니다. 일반 다익스트라와 달리 방문 여부로 건너뛰지 않고, 힙에 경로를 추가할 수 있는지로 판단합니다. 같은 정점에 여러 번 도달할 수 있어야 k번째 경로를 찾을 수 있기 때문입니다.

탐색이 끝난 뒤 각 정점의 힙을 확인합니다. 힙에 k개가 들어있으면 그중 최댓값이 k번째 최단 경로이고, k개 미만이면 경로가 k개 존재하지 않으므로 -1을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Collections.Generic;

class Program {
  static List<(int to, int w)>[] adj = Array.Empty<List<(int, int)>>();
  static PriorityQueue<(int cost, int node), int> pq = new();

  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var m = int.Parse(first[1]);
    var k = int.Parse(first[2]);

    adj = new List<(int, int)>[n + 1];
    for (var i = 1; i <= n; i++) adj[i] = new List<(int, int)>();

    for (var i = 0; i < m; i++) {
      var parts = Console.ReadLine()!.Split();
      var a = int.Parse(parts[0]);
      var b = int.Parse(parts[1]);
      var c = int.Parse(parts[2]);
      adj[a].Add((b, c));
    }

    var heaps = new PriorityQueue<int, int>[n + 1];
    for (var i = 1; i <= n; i++)
      heaps[i] = new PriorityQueue<int, int>(Comparer<int>.Create((a, b) => b.CompareTo(a)));

    heaps[1].Enqueue(0, 0);
    pq.Enqueue((0, 1), 0);

    while (pq.Count > 0) {
      var cur = pq.Dequeue();
      var cost = cur.cost;
      var u = cur.node;
      foreach (var (v, w) in adj[u]) {
        var nc = cost + w;
        if (heaps[v].Count < k) {
          heaps[v].Enqueue(nc, nc);
          pq.Enqueue((nc, v), nc);
        } else if (heaps[v].Peek() > nc) {
          heaps[v].Dequeue();
          heaps[v].Enqueue(nc, nc);
          pq.Enqueue((nc, v), nc);
        }
      }
    }

    for (var i = 1; i <= n; i++) {
      if (heaps[i].Count < k) Console.WriteLine("-1");
      else Console.WriteLine(heaps[i].Peek());
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef pair<int, int> pii;
typedef pair<ll, int> pli;
typedef vector<pii> vp;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m, k; cin >> n >> m >> k;
  vector<vp> adj(n + 1);
  for (int i = 0; i < m; i++) {
    int a, b, c; cin >> a >> b >> c;
    adj[a].push_back({b, c});
  }

  vector<priority_queue<ll>> dist(n + 1);
  priority_queue<pli, vector<pli>, greater<pli>> pq;
  dist[1].push(0);
  pq.push({0, 1});

  while (!pq.empty()) {
    auto [cost, u] = pq.top(); pq.pop();
    for (auto [v, w] : adj[u]) {
      ll nc = cost + w;
      if ((int)dist[v].size() < k) {
        dist[v].push(nc);
        pq.push({nc, v});
      } else if (dist[v].top() > nc) {
        dist[v].pop();
        dist[v].push(nc);
        pq.push({nc, v});
      }
    }
  }

  for (int i = 1; i <= n; i++) {
    if ((int)dist[i].size() < k) cout << -1 << "\n";
    else cout << dist[i].top() << "\n";
  }

  return 0;
}
```
