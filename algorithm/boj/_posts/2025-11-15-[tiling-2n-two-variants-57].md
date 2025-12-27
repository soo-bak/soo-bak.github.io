---
layout: single
title: "[백준 11727] 2×n 타일링 2 (C#, C++) - soo:bak"
date: "2025-11-15 00:02:00 +0900"
description: 1×2, 2×1, 2×2 타일로 2×n 직사각형을 채우는 경우의 수를 DP로 계산하는 백준 11727번 2×n 타일링 2 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 11727
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 11727, 백준 11727번, BOJ 11727, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[11727번 - 2×n 타일링 2](https://www.acmicpc.net/problem/11727)

## 설명

`2 × n` 크기의 직사각형을 `1 × 2`, `2 × 1`, `2 × 2` 세 종류의 타일로 채우는 방법의 수를 구하는 문제입니다.<br>

결과는 `10,007`로 나눈 나머지를 출력합니다.<br>

`n`은 최대 `1,000`까지 주어집니다.<br>

> 관련 문제: [[백준 11726] 2×n 타일링 (C#, C++) - soo:bak](https://soo-bak.github.io/algorithm/boj/tiling-2n-55) <br>

위 문제에 `2 × 2` 타일이 추가된 버전입니다.

타일 종류가 하나 더 있으므로 점화식이 `dp[n] = dp[n - 1] + 2 × dp[n - 2]`로 달라집니다.<br>

<br>

## 접근법

동적 프로그래밍을 사용하여 해결합니다.

`dp[i]`를 `2 × i` 직사각형을 채우는 방법의 수로 정의합니다.

<br>
`2 × n` 직사각형의 오른쪽 끝을 채우는 방법은 세 가지입니다.

첫 번째는 `2 × 1` 타일을 세로로 하나 놓는 경우입니다. 남은 부분은 `2 × (n - 1)` 크기가 되므로 `dp[n - 1]`가지입니다.

두 번째는 `1 × 2` 타일을 가로로 두 개 쌓는 경우입니다. 남은 부분은 `2 × (n - 2)` 크기가 되므로 `dp[n - 2]`가지입니다.

세 번째는 `2 × 2` 타일 하나를 놓는 경우입니다. 남은 부분은 `2 × (n - 2)` 크기가 되므로 `dp[n - 2]`가지입니다.

<br>
따라서 `dp[n] = dp[n - 1] + 2 × dp[n - 2]`의 점화식이 성립합니다.


기저 값은 `dp[1] = 1`, `dp[2] = 3`으로 설정합니다.

<br>
또한, 각 단계에서 `10,007`로 나눈 나머지만 저장하여 오버플로우를 방지합니다.

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
      var dp = new int[Math.Max(3, n + 1)];
      dp[1] = 1;
      if (n >= 2) dp[2] = 3;
      for (var i = 3; i <= n; i++)
        dp[i] = (dp[i - 1] + 2 * dp[i - 2]) % 10007;

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
  vi dp(max(3, n + 1));
  dp[1] = 1;
  if (n >= 2) dp[2] = 3;
  for (int i = 3; i <= n; ++i)
    dp[i] = (dp[i - 1] + 2 * dp[i - 2]) % 10007;

  cout << dp[n] << "\n";

  return 0;
}
```

