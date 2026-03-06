---
layout: single
title: "[백준 10844] 쉬운 계단 수 (C#, C++) - soo:bak"
date: "2026-03-06 18:19:00 +0900"
description: "백준 10844번 C#, C++ 풀이 - 길이가 N인 계단 수의 개수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 10844
  - C#
  - C++
  - 알고리즘
  - DP
keywords: "백준 10844, 백준 10844번, BOJ 10844, 쉬운 계단 수, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[10844번 - 쉬운 계단 수](https://www.acmicpc.net/problem/10844)

## 설명
인접한 자리의 차이가 항상 1인 수를 계단 수라고 할 때, 길이가 N인 계단 수의 개수를 구하는 문제입니다. 단, 맨 앞자리가 0인 수는 제외하며 결과는 1,000,000,000으로 나눈 나머지를 출력합니다.

<br>

## 접근법
길이와 마지막 숫자를 기준으로 경우의 수를 누적하면 됩니다.  
마지막 숫자가 0이라면 그 앞자리는 1만 가능하고, 마지막 숫자가 9라면 그 앞자리는 8만 가능합니다. 1부터 8까지는 바로 앞자리로 하나 작은 숫자와 하나 큰 숫자 두 경우가 가능합니다.  
이 관계를 길이 1부터 N까지 차례대로 채운 뒤, 길이 N에서 마지막 숫자가 0~9인 값을 모두 더하면 정답입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    const long mod = 1_000_000_000L;
    int n = int.Parse(Console.ReadLine()!);

    long[,] dp = new long[n + 1, 10];
    for (int d = 1; d <= 9; d++)
      dp[1, d] = 1;

    for (int len = 2; len <= n; len++) {
      dp[len, 0] = dp[len - 1, 1] % mod;
      dp[len, 9] = dp[len - 1, 8] % mod;
      for (int d = 1; d <= 8; d++) {
        dp[len, d] = (dp[len - 1, d - 1] + dp[len - 1, d + 1]) % mod;
      }
    }

    long ans = 0;
    for (int d = 0; d <= 9; d++)
      ans = (ans + dp[n, d]) % mod;

    Console.WriteLine(ans);
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

  const long long mod = 1'000'000'000LL;
  int n; cin >> n;

  vector<vector<long long>> dp(n + 1, vector<long long>(10, 0));
  for (int d = 1; d <= 9; d++)
    dp[1][d] = 1;

  for (int len = 2; len <= n; len++) {
    dp[len][0] = dp[len - 1][1] % mod;
    dp[len][9] = dp[len - 1][8] % mod;
    for (int d = 1; d <= 8; d++) {
      dp[len][d] = (dp[len - 1][d - 1] + dp[len - 1][d + 1]) % mod;
    }
  }

  long long ans = 0;
  for (int d = 0; d <= 9; d++)
    ans = (ans + dp[n][d]) % mod;

  cout << ans << "\n";

  return 0;
}
```
