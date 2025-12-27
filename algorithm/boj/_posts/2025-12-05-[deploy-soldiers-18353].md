---
layout: single
title: "[백준 18353] 병사 배치하기 (C#, C++) - soo:bak"
date: "2025-12-05 23:27:00 +0900"
description: 내림차순으로 남길 최대 병사 수를 구하기 위해 감소 부분 수열 길이를 계산하고 제거 인원을 출력하는 백준 18353번 병사 배치하기 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 18353
  - C#
  - C++
  - 알고리즘
keywords: "백준 18353, 백준 18353번, BOJ 18353, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18353번 - 병사 배치하기](https://www.acmicpc.net/problem/18353)

## 설명

병사들의 전투력 배열에서 내림차순으로 남길 수 있는 최대 병사 수를 구한 뒤, 제거해야 할 최소 인원을 출력하는 문제입니다.

내림차순으로 남길 수 있는 최대 길이는 가장 긴 감소하는 부분 수열(LDS)의 길이와 같습니다. N이 최대 2,000이므로 O(N²) DP로 충분히 해결할 수 있습니다.

<br>

## 접근법

DP를 활용하여 각 위치에서 끝나는 가장 긴 감소 부분 수열의 길이를 계산합니다.

<br>
먼저 dp[i]를 i번째 병사를 마지막으로 하는 감소 부분 수열의 최대 길이로 정의합니다. 모든 dp 값은 최소 1로 초기화합니다.

다음으로 각 위치 i에 대해 앞에 있는 모든 원소 j를 확인합니다. power[j] > power[i]인 경우, 즉 감소하는 관계라면 dp[i]를 dp[j] + 1과 비교하여 더 큰 값으로 갱신합니다.

이후 모든 dp 값 중 최댓값이 LDS 길이가 됩니다. 최소 제거 인원은 N - LDS 길이입니다.

<br>
시간 복잡도는 O(N²)입니다.

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
      var arr = Array.ConvertAll(Console.ReadLine()!.Split(), int.Parse);

      var dp = new int[n];
      var best = 0;
      for (var i = 0; i < n; i++) {
        dp[i] = 1;
        for (var j = 0; j < i; j++) {
          if (arr[j] > arr[i] && dp[i] < dp[j] + 1)
            dp[i] = dp[j] + 1;
        }
        if (dp[i] > best)
          best = dp[i];
      }

      Console.WriteLine(n - best);
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
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  vi dp(n, 1);
  int best = 0;
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < i; j++) {
      if (a[j] > a[i] && dp[i] < dp[j] + 1)
        dp[i] = dp[j] + 1;
    }
    best = max(best, dp[i]);
  }

  cout << n - best << "\n";

  return 0;
}
```
