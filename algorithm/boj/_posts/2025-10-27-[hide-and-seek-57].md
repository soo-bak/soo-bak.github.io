---
layout: single
title: "[백준 1697] 숨바꼭질 (C#, C++) - soo:bak"
date: "2025-10-27 22:05:00 +0900"
description: 현재 위치에서 -1, +1, 2배 이동을 반복해 목표 지점까지 최단 시간을 찾는 백준 1697번 숨바꼭질 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1697
  - C#
  - C++
  - 알고리즘
  - 그래프
  - graph_traversal
  - BFS
keywords: "백준 1697, 백준 1697번, BOJ 1697, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1697번 - 숨바꼭질](https://www.acmicpc.net/problem/1697)

## 설명

시작 위치 `N`에서 목표 위치 `K`까지 이동할 때 사용할 수 있는 연산은 `-1`, `+1`, `×2`뿐입니다.<br>

각 연산은 1초가 걸리며, 좌표 범위는 `0`에서 `100,000` 사이로 제한됩니다.<br>

목표는 **최소 시간 안에 `K`에 도달하는 순서를 찾는 것**입니다.<br>

<br>

## 접근법

이 문제는 모든 이동의 비용이 같으므로 **너비 우선 탐색(BFS)**이 최단 시간을 보장합니다.

- 방문 여부와 시간을 기록할 배열을 두어 한 좌표를 다시 탐색하지 않습니다.
- 큐에 현재 위치와 걸린 시간을 넣고, `-1`, `+1`, `×2` 결과가 범위 안에 있다면 순서대로 추가합니다.
- 목표 위치를 만나는 순간의 시간이 곧 답입니다.

<br>
좌표 범위가 `100,000`이기 때문에 BFS 또한 충분히 빠르게 끝납니다.

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
    var start = tokens[0];
    var goal = tokens[1];

    if (start >= goal) {
      Console.WriteLine(start - goal);
      return;
    }

    var max = 100000;
    var visited = new bool[max + 1];
    var dist = new int[max + 1];
    var queue = new Queue<int>();

    visited[start] = true;
    queue.Enqueue(start);

    while (queue.Count > 0) {
      var cur = queue.Dequeue();
      if (cur == goal) break;

      foreach (var next in new[] { cur - 1, cur + 1, cur * 2 }) {
        if (next < 0 || next > max) continue;
        if (visited[next]) continue;
        visited[next] = true;
        dist[next] = dist[cur] + 1;
        queue.Enqueue(next);
      }
    }

    Console.WriteLine(dist[goal]);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef queue<int> qi;
typedef vector<bool> vb;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int start, goal; cin >> start >> goal;

  if (start >= goal) {
    cout << start - goal << "\n";
    return 0;
  }

  const int maxPos = 100'000;
  vb visited(maxPos + 1, false);
  vi dist(maxPos + 1, 0);
  qi q;

  visited[start] = true;
  q.push(start);

  while (!q.empty()) {
    int cur = q.front();
    q.pop();
    if (cur == goal) break;

    int moves[3] = {cur - 1, cur + 1, cur * 2};
    for (int next : moves) {
      if (next < 0 || next > maxPos) continue;
      if (visited[next]) continue;
      visited[next] = true;
      dist[next] = dist[cur] + 1;
      q.push(next);
    }
  }

  cout << dist[goal] << "\n";
  
  return 0;
}
```

