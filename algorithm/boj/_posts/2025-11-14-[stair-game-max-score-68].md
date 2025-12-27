---
layout: single
title: "[백준 2579] 계단 오르기 (C#, C++) - soo:bak"
date: "2025-11-14 23:52:00 +0900"
description: 연속 세 계단을 밟을 수 없는 제약하에 DP로 최대 점수를 계산하는 백준 2579번 계단 오르기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2579
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 2579, 백준 2579번, BOJ 2579, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2579번 - 계단 오르기](https://www.acmicpc.net/problem/2579)

## 설명

각 계단에 점수가 주어지고, 다음 규칙을 지키며 올라갈 때 얻을 수 있는 최대 점수를 구하는 문제입니다.<br>

한 번에 한 계단 또는 두 계단씩 오를 수 있으며, 연속된 세 개의 계단을 모두 밟을 수 없습니다. 마지막 계단은 반드시 밟아야 합니다.<br>

계단 수는 최대 `300`개입니다.<br>

<br>

## 접근법

동적 프로그래밍을 사용하여 해결합니다.

`dp[i]`를 `i`번째 계단을 밟았을 때의 최대 점수로 정의합니다.

<br>
`i`번째 계단에 도달하는 방법은 두 가지입니다.

첫 번째는 `i - 2`번째 계단에서 두 계단을 올라오는 경우입니다.

이 경우 `dp[i] = dp[i - 2] + score[i]`가 됩니다.

<br>
두 번째는 `i - 1`번째 계단을 밟고 오는 경우입니다.

이때 `i - 1`번째 계단은 `i - 2`번째 계단에서 올 수 없습니다(연속 세 계단 금지).

따라서 `i - 3`번째 계단에서 `i - 1`번째로 와야 하므로 `dp[i] = dp[i - 3] + score[i - 1] + score[i]`가 됩니다.

<br>
두 경우 중 큰 값을 선택합니다.

기저 값은 `dp[1] = score[1]`, `dp[2] = score[1] + score[2]`, `dp[3] = max(score[1] + score[3], score[2] + score[3])`로 설정합니다.

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
      var score = new int[Math.Max(4, n + 1)];
      for (var i = 1; i <= n; i++)
        score[i] = int.Parse(Console.ReadLine()!);

      var dp = new int[Math.Max(4, n + 1)];
      dp[1] = score[1];
      if (n >= 2) dp[2] = score[1] + score[2];
      if (n >= 3) dp[3] = Math.Max(score[1] + score[3], score[2] + score[3]);

      for (var i = 4; i <= n; i++) {
        var option1 = dp[i - 2] + score[i];
        var option2 = dp[i - 3] + score[i - 1] + score[i];
        dp[i] = Math.Max(option1, option2);
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
  vi score(max(4, n + 1));
  for (int i = 1; i <= n; ++i)
    cin >> score[i];

  vi dp(max(4, n + 1));
  dp[1] = score[1];
  if (n >= 2) dp[2] = score[1] + score[2];
  if (n >= 3) dp[3] = max(score[1] + score[3], score[2] + score[3]);

  for (int i = 4; i <= n; ++i) {
    int option1 = dp[i - 2] + score[i];
    int option2 = dp[i - 3] + score[i - 1] + score[i];
    dp[i] = max(option1, option2);
  }

  cout << dp[n] << "\n";

  return 0;
}
```

