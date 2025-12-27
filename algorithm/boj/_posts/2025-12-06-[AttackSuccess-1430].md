---
layout: single
title: "[백준 1430] 공격 성공 (C#, C++) - soo:bak"
date: "2025-12-06 23:25:00 +0900"
description: 탑들의 에너지 전송과 손실을 고려해 적에게 가할 수 있는 최대 데미지를 구하는 백준 1430번 공격 성공 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1430
  - C#
  - C++
  - 알고리즘
keywords: "백준 1430, 백준 1430번, BOJ 1430, AttackSuccess, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1430번 - 공격 성공](https://www.acmicpc.net/problem/1430)

## 설명
N개의 탑이 있고, 각 탑은 초기 에너지 D를 가집니다. 두 탑 사이 거리가 R 이하이면 에너지를 전송할 수 있으며, 전송 시 받는 탑은 보낸 양의 절반만 얻습니다.

적과 거리가 R 이하인 탑만이 최종 공격을 가할 수 있습니다. 여러 탑의 에너지를 한 탑에 모아서 공격할 수 있을 때, 적에게 가할 수 있는 최대 데미지를 구하는 문제입니다.

<br>

## 접근법
이 문제의 핵심은 에너지 전송 시 손실이 발생한다는 점입니다. 간선을 한 번 지날 때마다 에너지가 절반으로 줄어듭니다. 따라서 각 탑의 에너지를 공격 가능한 탑까지 옮길 때, 거치는 간선 수가 적을수록 손실이 적습니다.

먼저, 문제를 그래프로 모델링합니다. 모든 탑 쌍에 대해 거리가 R 이하이면 무방향 간선을 만듭니다. 이렇게 하면 에너지 전송 가능 여부가 그래프의 연결 관계로 표현됩니다.

이후, 적과 거리가 R 이하인 탑들을 찾습니다. 이 탑들이 실제로 적을 공격할 수 있는 탑입니다. 이 탑들을 다중 시작점으로 하여 BFS를 수행하면, 모든 탑에서 공격 가능한 탑까지의 최소 홉수를 구할 수 있습니다.

그 다음, 각 탑의 기여 데미지를 계산합니다. 최소 홉수가 dist인 탑은 에너지가 dist번 절반으로 줄어들므로, 기여 데미지는 D를 2의 dist 제곱으로 나눈 값입니다. 공격 가능한 탑 자체는 홉수가 0이므로 손실 없이 D를 그대로 기여합니다.

마지막으로, 도달 가능한 모든 탑의 기여 데미지를 합산합니다. 공격 가능한 탑이 하나도 없으면 데미지는 0입니다.

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
      var first = Console.ReadLine()!.Split();
      var N = int.Parse(first[0]);
      var R = int.Parse(first[1]);
      var D = int.Parse(first[2]);
      var ex = int.Parse(first[3]);
      var ey = int.Parse(first[4]);

      var x = new int[N];
      var y = new int[N];
      for (var i = 0; i < N; i++) {
        var p = Console.ReadLine()!.Split();
        x[i] = int.Parse(p[0]);
        y[i] = int.Parse(p[1]);
      }

      var r2 = R * R;
      var adj = new List<int>[N];
      for (var i = 0; i < N; i++)
        adj[i] = new List<int>();
      for (var i = 0; i < N; i++) {
        for (var j = i + 1; j < N; j++) {
          var dx = x[i] - x[j];
          var dy = y[i] - y[j];
          if (dx * dx + dy * dy <= r2) {
            adj[i].Add(j);
            adj[j].Add(i);
          }
        }
      }

      var dist = new int[N];
      for (var i = 0; i < N; i++)
        dist[i] = -1;
      var q = new Queue<int>();
      for (var i = 0; i < N; i++) {
        var dx = x[i] - ex;
        var dy = y[i] - ey;
        if (dx * dx + dy * dy <= r2) {
          dist[i] = 0;
          q.Enqueue(i);
        }
      }

      while (q.Count > 0) {
        var cur = q.Dequeue();
        foreach (var nxt in adj[cur]) {
          if (dist[nxt] == -1) {
            dist[nxt] = dist[cur] + 1;
            q.Enqueue(nxt);
          }
        }
      }

      var damage = 0.0;
      for (var i = 0; i < N; i++) {
        if (dist[i] != -1)
          damage += D / Math.Pow(2.0, dist[i]);
      }

      Console.WriteLine(damage.ToString("0.00"));
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int N, R, D, ex, ey;
  cin >> N >> R >> D >> ex >> ey;

  vi x(N), y(N);
  for (int i = 0; i < N; i++)
    cin >> x[i] >> y[i];

  int r2 = R * R;
  vvi adj(N);
  for (int i = 0; i < N; i++) {
    for (int j = i + 1; j < N; j++) {
      int dx = x[i] - x[j];
      int dy = y[i] - y[j];
      if (dx * dx + dy * dy <= r2) {
        adj[i].push_back(j);
        adj[j].push_back(i);
      }
    }
  }

  vi dist(N, -1);
  queue<int> q;
  for (int i = 0; i < N; i++) {
    int dx = x[i] - ex;
    int dy = y[i] - ey;
    if (dx * dx + dy * dy <= r2) {
      dist[i] = 0;
      q.push(i);
    }
  }

  while (!q.empty()) {
    int cur = q.front(); q.pop();
    for (int nxt : adj[cur]) {
      if (dist[nxt] == -1) {
        dist[nxt] = dist[cur] + 1;
        q.push(nxt);
      }
    }
  }

  double damage = 0.0;
  for (int i = 0; i < N; i++) {
    if (dist[i] != -1)
      damage += D / pow(2.0, dist[i]);
  }

  cout << fixed << setprecision(2) << damage << "\n";

  return 0;
}
```
