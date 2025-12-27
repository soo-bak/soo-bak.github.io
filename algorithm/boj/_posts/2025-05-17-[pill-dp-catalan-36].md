---
layout: single
title: "[백준 4811] 알약 (C++, C#) - soo:bak"
date: "2025-05-17 05:41:00 +0900"
description: 원알과 반알을 꺼내는 규칙을 조합적으로 계산하는 백준 4811번 알약 문제의 C++ 및 C# 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4811
  - C#
  - C++
  - 알고리즘
keywords: "백준 4811, 백준 4811번, BOJ 4811, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4811번 - 알약](https://www.acmicpc.net/problem/4811)

## 설명

**약을 절반씩 나누어 복용하는 규칙에 따라 만들 수 있는 문자열의 총 개수를 계산하는 문제입니다.**

총 `N`개의 약이 병에 담겨 있으며,

문자열은 다음과 같은 방식으로 구성됩니다:

- 약 하나를 처음 꺼낼 때는 절반만 복용하고, 남은 절반은 병에 다시 넣습니다.
- 이후에는 매일 병에서 절반 조각을 꺼내 먹거나,<br>
  아직 복용하지 않은 온전한 약을 꺼내 다시 절반만 복용하고 나머지를 넣는 방식이 반복됩니다.
- 이 과정을 기록할 때:
  - 온전한 약을 꺼낸 날은 `W`
  - 절반 조각을 꺼낸 날은 `H`

로 표기하며, 총 `2N`일 동안 하나씩 꺼내는 동작이 반복됩니다.

이러한 방식으로 만들 수 있는 서로 다른 문자열의 개수를 구해야 합니다.
<br>

## 접근법

이 문제는 매일 약을 절반씩 복용하는 상황을 통해,

**W와 H로 이루어진 2N 길이의 문자열이 몇 가지 가능한지를 계산하는 조합 문제**로 바뀌게 됩니다.

<br>
초기에는 온전한 약이 `N`개 있으며,

첫째 날에는 반드시 약 하나를 꺼내 절반만 복용하고 나머지 절반은 병에 다시 넣습니다.

이후에는 다음 두 가지 동작이 가능해집니다:

- 아직 복용하지 않은 약이 남아 있다면, 하나를 꺼내 절반만 먹고 나머지는 다시 병에 넣습니다.
- 이미 병에 들어 있는 절반 조각이 있다면, 그것을 꺼내 복용합니다.

<br>
중요한 제약은 **남은 조각이 없는데도 그것을 꺼내려 할 수는 없다는 것**이며,

또한 복용 순서는 항상 정해진 규칙을 따라야 합니다.

<br>
이러한 상태 변화는 **매 순간마다 남아 있는 온전한 약과 조각의 개수에 따라 달라지며**,

동일한 상태가 여러 경로로 반복되기 때문에 **동적 계획법(DP)**으로 처리하는 것이 적합합니다.

`DP`의 상태는 다음과 같이 정의할 수 있습니다:

- 아직 복용하지 않은 약의 개수 `w`
- 현재 병에 들어 있는 조각의 개수 `h`

<br>
`dp[w][h]`는 `(w, h)` 상태에서 가능한 모든 문자열의 개수를 의미하며, 다음과 같은 점화식이 성립합니다:

- 아직 꺼내지 않은 약이 있다면:
  $$
  dp[w][h] += dp[w - 1][h + 1]
  $$
- 남은 조각이 있다면:
  $$
  dp[w][h] += dp[w][h - 1]
  $$

<br>
기저 조건은 더 이상 꺼낼 약이 없을 때이며,

그 경우 남은 조각을 순서대로 모두 꺼내는 한 가지 경우만 존재합니다.

<br>
모든 경우는 중복 계산을 방지하기 위해 메모이제이션으로 저장하며,

약의 개수는 최대 `30`개이므로 2차원 배열로도 충분히 계산 가능합니다.

<br>

> 참고 : [동적 계획법(Dynamic Programming)의 원리와 구현 - soo:bak](https://soo-bak.github.io/algorithm/theory/dynamic-programming/)

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static long[,] cache = new long[31, 31];

  static long Solve(int whole, int half) {
    if (whole == 0) return 1;
    if (cache[whole, half] != 0) return cache[whole, half];

    long res = Solve(whole - 1, half + 1);
    if (half > 0)
      res += Solve(whole, half - 1);

    return cache[whole, half] = res;
  }

  static void Main() {
    while (true) {
      int n = int.Parse(Console.ReadLine());
      if (n == 0) break;
      Console.WriteLine(Solve(n, 0));
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
#define MAX 30

using namespace std;
typedef long long ll;

ll cache[MAX + 1][MAX + 1];

ll solve(int cntWhole, int cntHalf) {
  if (cntWhole == 0) return 1;

  ll& ret = cache[cntWhole][cntHalf];
  if (ret) return ret;

  ret = solve(cntWhole - 1, cntHalf + 1);
  if (cntHalf) ret += solve(cntWhole, cntHalf - 1);

  return ret;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  while (true) {
    int n; cin >> n;
    if (!n) break;

    cout << solve(n, 0) << "\n";
  }

  return 0;
}
```
