---
layout: single
title: "[백준 11057] 오르막 수 (C#, C++) - soo:bak"
date: "2025-12-09 13:00:00 +0900"
description: 자리수가 오름차순인 길이 N 수의 개수를 DP로 구해 10007로 나머지 출력하는 백준 11057번 오르막 수 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11057
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 11057, 백준 11057번, BOJ 11057, AscendingNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11057번 - 오르막 수](https://www.acmicpc.net/problem/11057)

## 설명
각 자릿수가 왼쪽에서 오른쪽으로 갈수록 크거나 같은 수를 오르막 수라고 합니다. 길이가 N인 오르막 수의 개수를 10007로 나눈 나머지를 구하는 문제입니다.

<br>

## 접근법
오르막 수는 뒤로 갈수록 숫자가 커지거나 같아야 합니다.

따라서 어떤 오르막 수 뒤에 숫자 하나를 붙이려면, 붙이는 숫자가 마지막 숫자보다 크거나 같아야 합니다.

예를 들어 12 뒤에는 2, 3, 4, ..., 9를 붙일 수 있고, 15 뒤에는 5, 6, 7, 8, 9만 붙일 수 있습니다.

이 관계를 이용해 길이가 짧은 것부터 차례로 개수를 세어나가면 됩니다.

길이 1짜리는 0부터 9까지 열 개이고, 이후 한 자리씩 늘려가며 마지막 숫자별 개수를 누적하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  const int MOD = 10007;

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var dp = new int[n + 1, 10];
    for (var d = 0; d < 10; d++)
      dp[1, d] = 1;

    for (var len = 2; len <= n; len++) {
      dp[len, 0] = 1;
      for (var d = 1; d < 10; d++)
        dp[len, d] = (dp[len, d - 1] + dp[len - 1, d]) % MOD;
    }

    var ans = 0;
    for (var d = 0; d < 10; d++)
      ans = (ans + dp[n, d]) % MOD;
    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

const int MOD = 10007;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvi dp(n + 1, vi(10, 0));
  for (int d = 0; d < 10; d++) dp[1][d] = 1;

  for (int len = 2; len <= n; len++) {
    dp[len][0] = 1;
    for (int d = 1; d < 10; d++)
      dp[len][d] = (dp[len][d - 1] + dp[len - 1][d]) % MOD;
  }

  int ans = 0;
  for (int d = 0; d < 10; d++)
    ans = (ans + dp[n][d]) % MOD;
  cout << ans << "\n";

  return 0;
}
```
