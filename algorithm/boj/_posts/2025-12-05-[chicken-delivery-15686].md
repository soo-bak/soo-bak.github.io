---
layout: single
title: "[백준 15686] 치킨 배달 (C#, C++) - soo:bak"
date: "2025-12-05 23:27:00 +0900"
description: 최대 13개의 치킨집 중 M개를 조합으로 골라 도시의 치킨 거리를 최소화하는 백준 15686번 치킨 배달 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[15686번 - 치킨 배달](https://www.acmicpc.net/problem/15686)

## 설명

N×N 도시에 집과 치킨집이 있습니다. 치킨집 중 최대 M개만 남기고 나머지는 폐업시킬 때, 각 집에서 가장 가까운 치킨집까지의 거리 합을 최소화하는 문제입니다.

<br>

## 접근법

치킨집이 최대 13개이고 M 또한 최대 13이므로, 모든 조합을 시도하는 완전 탐색으로 풀 수 있습니다.

다음으로 백트래킹으로 M개의 치킨집을 선택합니다. 첫 번째 치킨집부터 순서대로 선택하거나 선택하지 않는 경우를 나누어 재귀 호출하고, 선택한 개수가 M이 되면 거리 합을 계산합니다.

이후 각 집에서 선택된 치킨집들까지의 거리 중 최솟값을 구하고, 모든 집의 최솟값을 더해 도시의 치킨 거리를 얻습니다. 이 값이 현재까지의 최솟값보다 작으면 갱신합니다.

<br>

---

## Code

### C#

```csharp
using System;
using System.Collections.Generic;

namespace Solution {
  class Program {
    static int N, M, best = int.MaxValue;
    static List<(int r, int c)> houses = new List<(int, int)>();
    static List<(int r, int c)> shops = new List<(int, int)>();
    static bool[] pick = Array.Empty<bool>();

    static int Dist((int r, int c) a, (int r, int c) b)
      => Math.Abs(a.r - b.r) + Math.Abs(a.c - b.c);

    static void Dfs(int idx, int chosen) {
      if (chosen == M) {
        var sum = 0;
        foreach (var h in houses) {
          var d = int.MaxValue;
          for (var i = 0; i < shops.Count; i++) {
            if (!pick[i])
              continue;
            d = Math.Min(d, Dist(h, shops[i]));
          }
          sum += d;
          if (sum >= best)
            break;
        }
        if (sum < best)
          best = sum;
        return;
      }
      if (idx == shops.Count)
        return;

      pick[idx] = true;
      Dfs(idx + 1, chosen + 1);
      pick[idx] = false;
      Dfs(idx + 1, chosen);
    }

    static void Main(string[] args) {
      var first = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
      N = first[0];
      M = first[1];
      for (var r = 0; r < N; r++) {
        var row = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);
        for (var c = 0; c < N; c++) {
          if (row[c] == 1)
            houses.Add((r, c));
          else if (row[c] == 2)
            shops.Add((r, c));
        }
      }
      pick = new bool[shops.Count];
      Dfs(0, 0);
      Console.WriteLine(best);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef pair<int, int> pii;
typedef vector<pii> vp;
typedef vector<bool> vb;

int N, M, best = INT_MAX;
vp houses, shops;
vb pick;

int dist(const pii& a, const pii& b) {
  return abs(a.first - b.first) + abs(a.second - b.second);
}

void dfs(int idx, int chosen) {
  if (chosen == M) {
    int sum = 0;
    for (auto& h : houses) {
      int d = INT_MAX;
      for (int i = 0; i < (int)shops.size(); i++) {
        if (!pick[i])
          continue;
        d = min(d, dist(h, shops[i]));
      }
      sum += d;
      if (sum >= best)
        break;
    }
    best = min(best, sum);
    return;
  }
  if (idx == (int)shops.size())
    return;

  pick[idx] = true;
  dfs(idx + 1, chosen + 1);
  pick[idx] = false;
  dfs(idx + 1, chosen);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> N >> M;
  for (int r = 0; r < N; r++) {
    for (int c = 0; c < N; c++) {
      int v; cin >> v;
      if (v == 1)
        houses.push_back({r, c});
      else if (v == 2)
        shops.push_back({r, c});
    }
  }

  pick.assign(shops.size(), false);
  dfs(0, 0);
  cout << best << "\n";

  return 0;
}
```
