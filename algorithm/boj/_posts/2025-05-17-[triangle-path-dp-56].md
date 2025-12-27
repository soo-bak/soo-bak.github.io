---
layout: single
title: "[백준 1932] 정수 삼각형 (C#, C++) - soo:bak"
date: "2025-05-17 05:34:00 +0900"
description: 정수 삼각형에서 대각선으로만 내려가며 최댓값을 누적하는 동적 계획법 백준 1932번 정수 삼각형 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1932
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 1932, 백준 1932번, BOJ 1932, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1932번 - 정수 삼각형](https://www.acmicpc.net/problem/1932)

## 설명

**정수로 이루어진 삼각형에서 맨 위에서부터 시작해 아래로 내려가며 만들 수 있는 경로 중, 합이 가장 큰 값을 구하는 문제입니다.**

각 위치에서는 **바로 아래층의 대각선 왼쪽 또는 오른쪽**에 있는 수만 선택할 수 있으며,

이동은 한 칸 아래로만 가능하다는 제약이 있습니다.

<br>
삼각형의 구조는 다음과 같이 점점 넓어지는 형태입니다:

```
      7
     3 8
    8 1 0
   2 7 4 4
  4 5 2 6 5
```

<br>
이 중에서 위에서부터 아래로 내려가며 만들어지는 경로들 중,

합이 가장 큰 값을 출력하는 것이 목표입니다.

<br>

## 접근법

이 문제는 **최대 누적합합을 계산해 나가는 동적 계획법(DP)** 방식으로 해결할 수 있습니다.

<br>
각 칸에서는 그 위의 두 칸(왼쪽 대각선, 오른쪽 대각선)에서만 올 수 있기 때문에,

각 위치에서 만들 수 있는 최대 합은 다음과 같이 정의할 수 있습니다:

- 맨 왼쪽 칸은 항상 왼쪽 위 한 칸에서만 올 수 있고,
- 맨 오른쪽 칸은 오른쪽 위 한 칸에서만 올 수 있으며,
- 그 외의 칸은 두 경로 중 더 큰 값을 선택해서 누적합니다.

이처럼 **한 줄씩 아래로 내려가며** 각 위치의 최대 누적 합을 갱신하면,

가장 마지막 줄에서의 최대값이 전체 경로 중 최대 합이 됩니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    int[][] tri = new int[n][];
    for (int i = 0; i < n; i++) {
      var row = Console.ReadLine().Split();
      tri[i] = Array.ConvertAll(row, int.Parse);
    }

    int[][] dp = new int[n][];
    for (int i = 0; i < n; i++)
      dp[i] = new int[n];

    dp[0][0] = tri[0][0];
    int max = dp[0][0];

    for (int i = 1; i < n; i++) {
      for (int j = 0; j <= i; j++) {
        if (j == 0) dp[i][j] = dp[i - 1][j] + tri[i][j];
        else if (j == i) dp[i][j] = dp[i - 1][j - 1] + tri[i][j];
        else dp[i][j] = Math.Max(dp[i - 1][j - 1], dp[i - 1][j]) + tri[i][j];

        max = Math.Max(max, dp[i][j]);
      }
    }

    Console.WriteLine(max);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  vvi tri(n, vi(n));
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j <= i; ++j)
      cin >> tri[i][j];
  }

  vvi dp(n, vi(n));
  dp[0][0] = tri[0][0];
  int maxSum = dp[0][0];
  for (int i = 1; i < n; ++i) {
    for (int j = 0; j <= i; ++j) {
      dp[i][j] = tri[i][j];
      if (j == 0) dp[i][j] += dp[i - 1][j];
      else if (j == i) dp[i][j] += dp[i - 1][j - 1];
      else dp[i][j] += max(dp[i - 1][j - 1], dp[i - 1][j]);

      maxSum = max(maxSum, dp[i][j]);
    }
  }

  cout << maxSum << "\n";

  return 0;
}
```
