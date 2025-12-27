---
layout: single
title: "[백준 11055] 가장 큰 증가하는 부분 수열 (C#, C++) - soo:bak"
date: "2025-12-09 13:20:00 +0900"
description: 증가하는 부분 수열들의 합 중 최댓값을 O(N^2) DP로 구하는 백준 11055번 가장 큰 증가하는 부분 수열 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11055
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 11055, 백준 11055번, BOJ 11055, MaxIncreasingSubsequenceSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11055번 - 가장 큰 증가하는 부분 수열](https://www.acmicpc.net/problem/11055)

## 설명
수열에서 증가하는 부분 수열을 골랐을 때, 원소들의 합이 최대가 되는 값을 구하는 문제입니다.

<br>

## 접근법
각 원소로 끝나는 증가 부분 수열의 최대 합을 구합니다.

예를 들어 1, 100, 2, 50, 60이 있다면, 60으로 끝나는 증가 수열 중 합이 가장 큰 것은 1, 2, 50, 60으로 합이 113입니다.

어떤 원소로 끝나는 최대 합을 구하려면, 그 앞에 있는 더 작은 원소들 중에서 최대 합이 가장 큰 것을 찾아 이어붙이면 됩니다.

각 원소마다 자기 자신만 선택한 경우를 시작으로, 앞의 모든 원소를 확인하며 갱신합니다.

전체 중 가장 큰 값이 답입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var a = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

    var dp = new int[n];
    var best = 0;
    for (var i = 0; i < n; i++) {
      dp[i] = a[i];
      for (var j = 0; j < i; j++) {
        if (a[j] < a[i] && dp[i] < dp[j] + a[i])
          dp[i] = dp[j] + a[i];
      }
      if (best < dp[i]) best = dp[i];
    }

    Console.WriteLine(best);
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

  int n; cin >> n;
  vi a(n), dp(n, 0);
  for (int i = 0; i < n; i++) cin >> a[i];

  int best = 0;
  for (int i = 0; i < n; i++) {
    dp[i] = a[i];
    for (int j = 0; j < i; j++) {
      if (a[j] < a[i] && dp[i] < dp[j] + a[i])
        dp[i] = dp[j] + a[i];
    }
    if (best < dp[i]) best = dp[i];
  }

  cout << best << "\n";

  return 0;
}
```
