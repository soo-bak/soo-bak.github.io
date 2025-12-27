---
layout: single
title: "[백준 17626] Four Squares (C#, C++) - soo:bak"
date: "2025-11-17 23:03:00 +0900"
description: 1부터 n까지의 최소 제곱수 합을 DP로 구해 네 개 이하의 제곱수로 표현하는 백준 17626번 Four Squares 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 17626
  - C#
  - C++
  - 알고리즘
keywords: "백준 17626, 백준 17626번, BOJ 17626, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[17626번 - Four Squares](https://www.acmicpc.net/problem/17626)

## 설명

자연수 `n`을 최소 개수의 완전제곱수의 합으로 나타내는 문제입니다.<br>

라그랑주의 네 제곱수 정리에 따르면 모든 자연수는 네 개 이하의 완전제곱수의 합으로 표현할 수 있습니다. 예를 들어 `25 = 5²`, `26 = 5² + 1²`, `27 = 3² + 3² + 3²`입니다.<br>

주어진 자연수 `n`을 완전제곱수의 합으로 표현할 때 필요한 제곱수의 최소 개수를 구해야 합니다.<br>

`n`은 `1` 이상 `50,000` 이하입니다.<br>

<br>

## 접근법

작은 수의 답을 이용하여 큰 수의 답을 구하는 동적 프로그래밍으로 해결합니다.

`dp[i]`를 `i`를 만드는 데 필요한 최소 제곱수 개수로 정의합니다.

`dp[1] = 1`, `dp[4] = 1 (2²)`, `dp[5] = 2 (4 + 1)`처럼 작은 수부터 차례로 계산합니다.

<br>
각 수 `i`에 대해 초기값을 `dp[i] = i`로 설정합니다. 이는 `1²`만 사용하는 최악의 경우입니다.

<br>
`i`보다 작거나 같은 모든 제곱수 `j²`를 시도하여 최솟값을 찾습니다.

이 때, `dp[i - j²]`는 이미 계산되어 있으므로 `dp[i - j²] + 1`로 갱신할 수 있습니다.

예를 들어 `dp[13]`을 계산할 때 `dp[4] = 1`을 이미 알고 있으므로 `dp[13] = dp[4] + 1 = 2 (9 + 4)`가 됩니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static void Main(string[] args) {
      var n = int.Parse(Console.ReadLine()!);
      var dp = new int[n + 1];

      for (var i = 1; i <= n; i++) {
        dp[i] = i;
        for (var j = 1; j * j <= i; j++) {
          var sq = j * j;
          dp[i] = Math.Min(dp[i], dp[i - sq] + 1);
        }
      }

      Console.WriteLine(dp[n]);
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

  int n; cin >> n;
  vi dp(n + 1, 0);

  for (int i = 1; i <= n; ++i) {
    dp[i] = i;
    for (int j = 1; j * j <= i; ++j)
      dp[i] = min(dp[i], dp[i - j * j] + 1);
  }

  cout << dp[n] << "\n";

  return 0;
}
```

