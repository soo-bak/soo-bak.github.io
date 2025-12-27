---
layout: single
title: "[백준 1516] 게임 개발 (C#, C++) - soo:bak"
date: "2025-12-07 02:30:00 +0900"
description: DFS와 메모이제이션으로 각 건물의 최소 완성 시간을 구하는 백준 1516번 게임 개발 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1516
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
  - 그래프
  - dag
  - topological_sorting
keywords: "백준 1516, 백준 1516번, BOJ 1516, GameDevelopment, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1516번 - 게임 개발](https://www.acmicpc.net/problem/1516)

## 설명
각 건물마다 건설 시간과 선행 건물 목록이 주어질 때, 각 건물을 완성하는 데 걸리는 최소 시간을 구하는 문제입니다. 여러 건물을 동시에 건설할 수 있습니다.

<br>

## 접근법
어떤 건물을 짓기 위해서는 선행 건물들이 모두 완성되어야 합니다. 여러 건물을 동시에 지을 수 있으므로, 선행 건물들 중 가장 늦게 완성되는 시간에 해당 건물의 건설 시간을 더하면 됩니다.

DFS로 각 건물의 완성 시간을 재귀적으로 구합니다. 선행 건물이 없으면 자신의 건설 시간만 걸립니다. 선행 건물이 있으면 각 선행 건물의 완성 시간 중 최댓값을 구한 뒤 자신의 건설 시간을 더합니다.

한 번 계산한 건물의 완성 시간은 저장해두어 중복 계산을 피합니다. 모든 건물에 대해 완성 시간을 구해 출력합니다.

<br>

- - -

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

class Program {
  static int n;
  static int[] cost = Array.Empty<int>();
  static int[] dp = Array.Empty<int>();
  static List<int>[] pre = Array.Empty<List<int>>();

  static int Dfs(int u) {
    if (dp[u] != -1) return dp[u];
    var maxPrev = 0;
    foreach (var v in pre[u]) {
      var t = Dfs(v);
      if (t > maxPrev) maxPrev = t;
    }
    dp[u] = cost[u] + maxPrev;
    return dp[u];
  }

  static void Main() {
    n = int.Parse(Console.ReadLine()!);
    cost = new int[n + 1];
    dp = new int[n + 1];
    pre = new List<int>[n + 1];
    for (var i = 1; i <= n; i++) {
      dp[i] = -1;
      pre[i] = new List<int>();
      var parts = Console.ReadLine()!.Split();
      cost[i] = int.Parse(parts[0]);
      for (var j = 1; j < parts.Length; j++) {
        var v = int.Parse(parts[j]);
        if (v == -1) break;
        pre[i].Add(v);
      }
    }

    for (var i = 1; i <= n; i++)
      Console.WriteLine(Dfs(i));
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

int n;
vi cost, dp;
vvi pre;

int dfs(int u) {
  if (dp[u] != -1) return dp[u];
  int maxPrev = 0;
  for (int v : pre[u]) {
    int t = dfs(v);
    if (t > maxPrev) maxPrev = t;
  }
  dp[u] = cost[u] + maxPrev;
  return dp[u];
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n;
  cost.assign(n + 1, 0);
  dp.assign(n + 1, -1);
  pre.assign(n + 1, {});

  for (int i = 1; i <= n; i++) {
    int t; cin >> cost[i];
    while (cin >> t) {
      if (t == -1) break;
      pre[i].push_back(t);
    }
  }

  for (int i = 1; i <= n; i++)
    cout << dfs(i) << "\n";

  return 0;
}
```
