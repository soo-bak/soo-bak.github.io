---
layout: single
title: "[백준 1504] 특정한 최단 경로 (C#, C++) - soo:bak"
date: "2025-12-01 19:03:00 +0900"
description: 두 정점을 반드시 지나면서 1에서 N까지의 최단 거리를 구하기 위해 다익스트라를 세 번 돌려 조합하는 백준 1504번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1504
  - C#
  - C++
  - 알고리즘
keywords: "백준 1504, 백준 1504번, BOJ 1504, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1504번 - 특정한 최단 경로](https://www.acmicpc.net/problem/1504)

## 설명

무방향 가중치 그래프가 주어지는 상황에서, N개의 정점 (2 ≤ N ≤ 800), E개의 간선 (0 ≤ E ≤ 200,000), 그리고 반드시 거쳐야 하는 두 정점 v1, v2가 주어질 때, 1번 정점에서 N번 정점까지 v1과 v2를 모두 거쳐서 가는 최단 경로의 길이를 구하는 문제입니다.

가능한 경로는 1 → v1 → v2 → N 또는 1 → v2 → v1 → N 두 가지입니다. 경로가 존재하지 않으면 -1을 출력합니다.

<br>

## 접근법

다익스트라를 세 번 실행하여 필요한 모든 구간의 최단 거리를 구합니다.

<br>
먼저 1번, v1, v2에서 각각 다익스트라를 실행합니다. 1번에서 시작한 다익스트라로 1 → v1과 1 → v2 거리를 얻고, v1에서 시작한 다익스트라로 v1 → v2와 v1 → N 거리를, v2에서 시작한 다익스트라로 v2 → N 거리를 얻습니다.

두 가지 경로의 비용을 계산합니다. 첫 번째 경로는 1 → v1 + v1 → v2 + v2 → N이고, 두 번째 경로는 1 → v2 + v2 → v1 + v1 → N입니다.

이렇게 계산한 두 경로 중 더 짧은 것을 선택합니다. 어느 구간이라도 도달 불가능하면 -1을 출력합니다.

<br>
시간 복잡도는 O(E log N)입니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    const int INF = int.MaxValue / 4;
    static List<(int to, int w)>[] adj = Array.Empty<List<(int, int)>>();

    static int[] Dijkstra(int start, int n) {
      var dist = new int[n + 1];
      Array.Fill(dist, INF);
      dist[start] = 0;

      var pq = new PriorityQueue<int, int>();
      pq.Enqueue(start, 0);

      while (pq.Count > 0) {
        pq.TryDequeue(out var cur, out var d);
        if (d > dist[cur])
          continue;
        foreach (var edge in adj[cur]) {
          var nxt = edge.to;
          var w = edge.w;
          var nd = dist[cur] + w;
          if (nd < dist[nxt]) {
            dist[nxt] = nd;
            pq.Enqueue(nxt, nd);
          }
        }
      }
      return dist;
    }

    static void Main(string[] args) {
      var first = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var n = first[0];
      var e = first[1];

      adj = new List<(int, int)>[n + 1];
      for (var i = 1; i <= n; i++)
        adj[i] = new List<(int, int)>();

      for (var i = 0; i < e; i++) {
        var parts = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
        var a = parts[0];
        var b = parts[1];
        var c = parts[2];
        adj[a].Add((b, c));
        adj[b].Add((a, c));
      }

      var last = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      var v1 = last[0];
      var v2 = last[1];

      var distFrom1 = Dijkstra(1, n);
      var distFromV1 = Dijkstra(v1, n);
      var distFromV2 = Dijkstra(v2, n);

      var path1 = (long)distFrom1[v1] + distFromV1[v2] + distFromV2[n];
      var path2 = (long)distFrom1[v2] + distFromV2[v1] + distFromV1[n];

      var ans = Math.Min(path1, path2);
      if (distFromV1[v2] >= INF || ans >= INF)
        Console.WriteLine(-1);
      else
        Console.WriteLine(ans);
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
typedef vector<int> vi;
typedef vector<pii> vp;
typedef vector<vp> vvp;

const int INF = 1e9;

vvp adj;

vi dijkstra(int start, int n) {
  vi dist(n + 1, INF);
  priority_queue<pii, vp, greater<pii>> pq;
  dist[start] = 0;
  pq.push({0, start});

  while (!pq.empty()) {
    auto [d, u] = pq.top();
    pq.pop();
    if (d > dist[u])
      continue;
    for (auto [v, w] : adj[u]) {
      if (dist[v] > dist[u] + w) {
        dist[v] = dist[u] + w;
        pq.push({dist[v], v});
      }
    }
  }
  return dist;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, e; cin >> n >> e;
  adj.assign(n + 1, {});
  for (int i = 0; i < e; i++) {
    int a, b, c; cin >> a >> b >> c;
    adj[a].push_back({b, c});
    adj[b].push_back({a, c});
  }
  int v1, v2; cin >> v1 >> v2;

  auto d1 = dijkstra(1, n);
  auto dv1 = dijkstra(v1, n);
  auto dv2 = dijkstra(v2, n);

  ll path1 = (ll)d1[v1] + dv1[v2] + dv2[n];
  ll path2 = (ll)d1[v2] + dv2[v1] + dv1[n];
  ll ans = min(path1, path2);

  if (dv1[v2] >= INF || ans >= INF)
    cout << -1 << "\n";
  else
    cout << ans << "\n";

  return 0;
}
```
