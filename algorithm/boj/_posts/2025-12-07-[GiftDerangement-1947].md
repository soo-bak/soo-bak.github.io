---
layout: single
title: "[백준 1947] 선물 전달 (C#, C++) - soo:bak"
date: "2025-12-07 02:45:00 +0900"
description: N명이 자기 선물을 받지 않도록 교환하는 경우의 수를 구하는 백준 1947번 선물 전달 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1947번 - 선물 전달](https://www.acmicpc.net/problem/1947)

## 설명
N명이 각자 준비한 선물을 서로 교환할 때, 아무도 자기 선물을 받지 않는 경우의 수를 구하는 문제입니다. 답은 1000000000으로 나눈 나머지를 출력합니다.

<br>

## 접근법
이 문제는 완전순열 문제입니다. N명 중 한 명이 특정 사람의 선물을 받으면, 나머지는 두 가지 경우로 나뉩니다. 그 사람이 자신의 선물을 받는 경우와 받지 않는 경우입니다.

이를 정리하면 N번째 경우의 수는 N - 1번째와 N - 2번째 경우의 수의 합에 N - 1을 곱한 값이 됩니다. 1명일 때는 0, 2명일 때는 1을 기본값으로 사용합니다.

N이 최대 100만이므로 동적 계획법으로 순서대로 값을 채워나갑니다. 곱셈에서 오버플로가 발생할 수 있으므로 중간 계산마다 나머지 연산을 적용합니다.

<br>

- - -

## Code

### C#

```csharp
using System;

class Program {
  const long MOD = 1000000000L;

  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var dp = new long[n + 2];
    dp[1] = 0;
    if (n >= 2) dp[2] = 1;
    for (var i = 3; i <= n; i++)
      dp[i] = ((dp[i - 1] + dp[i - 2]) % MOD) * (i - 1) % MOD;
    Console.WriteLine(dp[n] % MOD);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<ll> vl;

const ll MOD = 1000000000LL;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vl dp(n + 2, 0);
  dp[1] = 0;
  if (n >= 2) dp[2] = 1;
  for (int i = 3; i <= n; i++)
    dp[i] = ((dp[i - 1] + dp[i - 2]) % MOD) * (i - 1) % MOD;
  cout << dp[n] % MOD << "\n";

  return 0;
}
```
