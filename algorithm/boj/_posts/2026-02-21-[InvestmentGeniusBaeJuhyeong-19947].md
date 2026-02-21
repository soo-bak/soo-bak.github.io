---
layout: single
title: "[백준 19947] 투자의 귀재 배주형 (C#, C++) - soo:bak"
date: "2026-02-21 19:50:00 +0900"
description: "백준 19947번 C#, C++ 풀이 - Y년 뒤 자산을 최대화하는 복리 투자 패턴을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 19947
  - C#
  - C++
  - 알고리즘
  - DP
  - 구현
keywords: "백준 19947, 백준 19947번, BOJ 19947, 투자의 귀재 배주형, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[19947번 - 투자의 귀재 배주형](https://www.acmicpc.net/problem/19947)

## 설명
초기 자산 H와 투자 기간 Y가 주어질 때, 1년(5%), 3년(20%), 5년(35%) 투자 방법을 조합해 Y년 뒤 자산을 최대로 만드는 값을 구하는 문제입니다.

<br>

## 접근법
각 연도마다 "그 시점에 만들 수 있는 최대 자산"만 저장하며 진행합니다.

예를 들어 i년 시점의 최대 자산을 구할 때는, 1년 전 최대 자산에 5%를 적용한 경우, 3년 전 최대 자산에 20%를 적용한 경우, 5년 전 최대 자산에 35%를 적용한 경우를 비교하면 됩니다.  

문제 조건상 이자는 항상 소수점을 버려야 하므로 매번 정수 계산으로 처리하고, 세 경우 중 가장 큰 값을 선택합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var p = Console.ReadLine()!.Split();
    var h = int.Parse(p[0]);
    var y = int.Parse(p[1]);

    var dp = new int[y + 1];
    dp[0] = h;

    for (var i = 1; i <= y; i++) {
      var best = dp[i - 1] * 105 / 100;
      if (i >= 3)
        best = Math.Max(best, dp[i - 3] * 120 / 100);
      if (i >= 5)
        best = Math.Max(best, dp[i - 5] * 135 / 100);
      dp[i] = best;
    }

    Console.WriteLine(dp[y]);
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

  int h, y;
  cin >> h >> y;

  vector<int> dp(y + 1, 0);
  dp[0] = h;

  for (int i = 1; i <= y; i++) {
    int best = dp[i - 1] * 105 / 100;
    if (i >= 3)
      best = max(best, dp[i - 3] * 120 / 100);
    if (i >= 5)
      best = max(best, dp[i - 5] * 135 / 100);
    dp[i] = best;
  }

  cout << dp[y] << "\n";

  return 0;
}
```
