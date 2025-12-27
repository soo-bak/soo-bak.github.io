---
layout: single
title: "[백준 10902] Penalty calculation (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 10902번 C#, C++ 풀이 - 최고 점수를 가장 먼저 받은 제출을 찾아 페널티를 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 10902
  - C#
  - C++
  - 알고리즘
keywords: "백준 10902, 백준 10902번, BOJ 10902, PenaltyCalculation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10902번 - Penalty calculation](https://www.acmicpc.net/problem/10902)

## 설명
n개의 제출에 대해 시각과 점수가 주어질 때, 최고 점수를 가장 먼저 받은 제출의 페널티를 계산하는 문제입니다. 점수가 0이면 페널티는 0이고, 그렇지 않으면 제출 시각에 이전 제출 횟수 × 20을 더한 값이 페널티입니다.

<br>

## 접근법
제출을 순서대로 확인하며 최고 점수와 그 점수를 처음 받은 제출의 시각, 순번을 기록합니다. 최고 점수가 0이면 페널티는 0이고, 그렇지 않으면 해당 제출 시각에 이전 제출 횟수 × 20을 더해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var bestScore = -1;
    var bestIdx = -1;
    var bestTime = 0;

    for (var i = 1; i <= n; i++) {
      var parts = Console.ReadLine()!.Split();
      var t = int.Parse(parts[0]);
      var s = int.Parse(parts[1]);
      if (s > bestScore) {
        bestScore = s;
        bestIdx = i;
        bestTime = t;
      }
    }

    if (bestScore == 0) Console.WriteLine(0);
    else Console.WriteLine(bestTime + (bestIdx - 1) * 20);
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

  int n; cin >> n;
  int bestS = -1, bestIdx = -1, bestT = 0;

  for (int i = 1; i <= n; i++) {
    int t, s; cin >> t >> s;
    if (s > bestS) {
      bestS = s;
      bestIdx = i;
      bestT = t;
    }
  }

  if (bestS == 0) cout << 0 << "\n";
  else cout << bestT + (bestIdx - 1) * 20 << "\n";

  return 0;
}
```
