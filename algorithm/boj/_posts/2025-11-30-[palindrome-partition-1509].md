---
layout: single
title: "[백준 1509] 팰린드롬 분할 (C#, C++) - soo:bak"
date: "2025-11-30 01:48:00 +0900"
description: 팰린드롬 여부를 전처리한 뒤 최소 분할 횟수를 DP로 구하는 백준 1509번 팰린드롬 분할 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 1509
  - C#
  - C++
  - 알고리즘
  - 다이나믹 프로그래밍
keywords: "백준 1509, 백준 1509번, BOJ 1509, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1509번 - 팰린드롬 분할](https://www.acmicpc.net/problem/1509)

## 설명

문자열이 주어지는 상황에서, 문자열의 길이 (1 ≤ 길이 ≤ 2,500)가 주어질 때, 주어진 문자열을 팰린드롬들의 연속으로 분할할 때 필요한 최소 조각 수를 구하는 문제입니다.

팰린드롬(Palindrome)은 앞에서 읽으나 뒤에서 읽으나 같은 문자열을 의미합니다. 예를 들어, "aba"나 "aa"는 팰린드롬입니다. 문자열을 여러 개의 팰린드롬으로 분할할 때, 분할된 조각의 개수를 최소화해야 합니다.

<br>

## 접근법

`dp[i]`를 1번째부터 i번째 문자까지를 팰린드롬들로 분할할 때의 최소 조각 수로 정의합니다.

j번째부터 i번째까지가 팰린드롬이면 `dp[i] = min(dp[i], dp[j-1] + 1)`로 갱신할 수 있습니다. 하지만 모든 i와 j에 대해 매번 팰린드롬을 직접 확인하면 O(N³)이 되므로, 미리 전처리가 필요합니다.

<br>
`pal[i][j]`를 i번째부터 j번째까지가 팰린드롬인지 저장하는 테이블로 정의합니다. 팰린드롬 판정은 길이별로 진행합니다.

길이 1은 항상 팰린드롬입니다.

길이 2는 두 문자가 같으면 팰린드롬입니다.

길이 3 이상은 양 끝 문자가 같고(`s[i] == s[j]`) 안쪽이 팰린드롬(`pal[i+1][j-1]`)이면 팰린드롬입니다. 길이 순서대로 계산하면 안쪽 부분이 항상 먼저 계산되어 있으므로, O(N²) 시간에 모든 부분 문자열을 판정할 수 있습니다.

<br>
예를 들어 "ABACABA"에서:
- "ABA" (1~3)는 팰린드롬 → `dp[3] = 1`
- "C" (4)는 팰린드롬 → `dp[4] = dp[3] + 1 = 2`
- "ABA" (5~7)는 팰린드롬 → `dp[7] = dp[4] + 1 = 3`

따라서 "ABACABA"는 "ABA + C + ABA" 3조각으로 분할할 수 있습니다.

<br>
다른 예로 "ABBAB"에서:
- 위치 1: "A" → 1조각
- 위치 2: "B" → 2조각 (A + B)
- 위치 3: "ABB"는 팰린드롬 아님, "BB"는 팰린드롬 → 2조각 (A + BB)
- 위치 4: "ABBA"는 팰린드롬 → 1조각
- 위치 5: "ABBAB"는 팰린드롬 아님, "ABBA"는 팰린드롬이므로 `dp[4] + 1` → 2조각 (ABBA + B)

<br>
시간 복잡도는 팰린드롬 판정 O(N²)과 DP 계산 O(N²)로 총 O(N²)입니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    const int INF = 987654321;

    static void Main(string[] args) {
      var s = Console.ReadLine()!;
      var n = s.Length;
      s = " " + s; // 1-index

      var pal = new bool[n + 1, n + 1];
      for (var i = 1; i <= n; i++)
        pal[i, i] = true;
      for (var i = 1; i < n; i++)
        if (s[i] == s[i + 1])
          pal[i, i + 1] = true;

      for (var len = 3; len <= n; len++) {
        for (var i = 1; i + len - 1 <= n; i++) {
          var j = i + len - 1;
          if (s[i] == s[j] && pal[i + 1, j - 1])
            pal[i, j] = true;
        }
      }

      var dp = new int[n + 1];
      for (var i = 1; i <= n; i++)
        dp[i] = INF;

      for (var i = 1; i <= n; i++) {
        for (var j = 1; j <= i; j++) {
          if (pal[j, i])
            dp[i] = Math.Min(dp[i], dp[j - 1] + 1);
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

const int INF = 987654321;
bool pal[2501][2501];
int dp[2501];

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string str;
  cin >> str;
  int n = str.size();
  str = " " + str; // 1-index

  for (int i = 1; i <= n; i++)
    pal[i][i] = true;
  for (int i = 1; i < n; i++)
    if (str[i] == str[i + 1])
      pal[i][i + 1] = true;

  for (int len = 3; len <= n; len++) {
    for (int i = 1; i + len - 1 <= n; i++) {
      int j = i + len - 1;
      if (str[i] == str[j] && pal[i + 1][j - 1])
        pal[i][j] = true;
    }
  }

  for (int i = 1; i <= n; i++)
    dp[i] = INF;
  dp[0] = 0;

  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= i; j++) {
      if (pal[j][i])
        dp[i] = min(dp[i], dp[j - 1] + 1);
    }
  }

  cout << dp[n] << "\n";
  
  return 0;
}
```


