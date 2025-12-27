---
layout: single
title: "[백준 28225] Flower Festival (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 28225번 C#, C++ 풀이 - 차량들의 위치와 속도로 가장 먼저 도착하는 차 번호를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 28225
  - C#
  - C++
  - 알고리즘
keywords: "백준 28225, 백준 28225번, BOJ 28225, FlowerFestival, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[28225번 - Flower Festival](https://www.acmicpc.net/problem/28225)

## 설명
각 차량의 현재 위치와 속도가 주어질 때, 가장 먼저 도착하는 차량 번호를 찾는 문제입니다.

<br>

## 접근법
각 차량의 도착 시간은 남은 거리를 속도로 나눈 값입니다. 

두 차량의 도착 순서를 비교한 후, 모든 차량을 순회하며 현재까지 가장 빠른 차량을 갱신합니다. 동시에 도착하는 경우는 없으므로, 최종적으로 가장 먼저 도착하는 차량의 번호를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var f = int.Parse(first[1]);

    int bestIdx = 1;
    int bestDist, bestV;
    {
      var p = Console.ReadLine()!.Split();
      var x = int.Parse(p[0]);
      var v = int.Parse(p[1]);
      bestDist = f - x;
      bestV = v;
    }

    for (var i = 2; i <= n; i++) {
      var p = Console.ReadLine()!.Split();
      var x = int.Parse(p[0]);
      var v = int.Parse(p[1]);

      var dist = f - x;
      if (dist * bestV < bestDist * v) {
        bestDist = dist;
        bestV = v;
        bestIdx = i;
      }
    }

    Console.WriteLine(bestIdx);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, f; cin >> n >> f;

  int x, v; cin >> x >> v;
  int bestIdx = 1;
  int bestDist = f - x, bestV = v;

  for (int i = 2; i <= n; i++) {
    cin >> x >> v;
    int dist = f - x;
    if (dist * bestV < bestDist * v) {
      bestDist = dist;
      bestV = v;
      bestIdx = i;
    }
  }

  cout << bestIdx << "\n";

  return 0;
}
```
