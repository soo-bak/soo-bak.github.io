---
layout: single
title: "[백준 16928] 뱀과 사다리 게임 (C#, C++) - soo:bak"
date: "2025-11-17 23:07:00 +0900"
description: 사다리·뱀 이동을 간선으로 보고 BFS로 최소 주사위 굴림 횟수를 찾는 백준 16928번 뱀과 사다리 게임 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 16928
  - C#
  - C++
  - 알고리즘
  - 그래프
  - graph_traversal
  - BFS
keywords: "백준 16928, 백준 16928번, BOJ 16928, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16928번 - 뱀과 사다리 게임](https://www.acmicpc.net/problem/16928)

## 설명

`1`번 칸에서 시작하여 주사위를 굴려 `100`번 칸에 도착하는 최소 주사위 굴림 횟수를 구하는 문제입니다.<br>

주사위는 `1`부터 `6`까지의 눈이 나오며, 원하는 눈을 선택할 수 있습니다.<br>

보드에는 사다리와 뱀이 있어서 특정 칸에 도착하면 연결된 다른 칸으로 즉시 이동합니다.<br>

`100`번을 넘어가면 이동할 수 없으며, 정확히 `100`번에 도착해야 합니다.<br>

<br>

## 접근법

BFS를 사용하여 최소 주사위 굴림 횟수를 구합니다.

모든 주사위 굴림의 비용이 `1`로 동일하기 때문에, BFS로 처음 `100`번 칸에 도달했을 때의 거리가 최소 굴림 횟수입니다.

<br>
`1`번 칸에서 시작하여 주사위 눈 `1`부터 `6`까지 각각 시도합니다.

이동한 칸에 사다리나 뱀이 있으면 연결된 칸으로 즉시 이동합니다.

<br>
이미 방문한 칸은 건너뛰며, 각 칸까지의 최소 굴림 횟수를 기록합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var ladders = int.Parse(tokens[0]);
      var snakes = int.Parse(tokens[1]);

      var jump = new Dictionary<int, int>();
      for (var i = 0; i < ladders + snakes; i++) {
        var line = Console.ReadLine()!.Split();
        var from = int.Parse(line[0]);
        var to = int.Parse(line[1]);
        jump[from] = to;
      }

      var visited = new bool[101];
      var dist = new int[101];
      var queue = new Queue<int>();
      queue.Enqueue(1);
      visited[1] = true;

      while (queue.Count > 0) {
        var cur = queue.Dequeue();
        if (cur == 100) break;

        for (var dice = 1; dice <= 6; dice++) {
          var next = cur + dice;
          if (next > 100) continue;
          if (jump.TryGetValue(next, out var moved))
            next = moved;
          if (visited[next]) continue;

          visited[next] = true;
          dist[next] = dist[cur] + 1;
          queue.Enqueue(next);
        }
      }

      Console.WriteLine(dist[100]);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int ladders, snakes; cin >> ladders >> snakes;
  vi jump(101, 0);

  for (int i = 0; i < ladders + snakes; ++i) {
    int from, to; cin >> from >> to;
    jump[from] = to;
  }

  vi dist(101, -1);
  queue<int> q;
  q.push(1);
  dist[1] = 0;

  while (!q.empty()) {
    int cur = q.front(); q.pop();
    if (cur == 100) break;

    for (int dice = 1; dice <= 6; ++dice) {
      int next = cur + dice;
      if (next > 100) continue;
      if (jump[next] != 0) next = jump[next];
      if (dist[next] != -1) continue;

      dist[next] = dist[cur] + 1;
      q.push(next);
    }
  }

  cout << dist[100] << "\n";

  return 0;
}
```

