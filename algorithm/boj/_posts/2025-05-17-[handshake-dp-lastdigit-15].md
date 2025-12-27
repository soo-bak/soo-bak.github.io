---
layout: single
title: "[백준 8394] 악수 (C#, C++) - soo:bak"
date: "2025-05-17 05:36:00 +0900"
description: 좌우 인접한 사람 간의 악수 조합을 계산하며 마지막 자리만 출력하는 백준 8394번 악수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 8394
  - C#
  - C++
  - 알고리즘
  - 수학
  - 다이나믹 프로그래밍
keywords: "백준 8394, 백준 8394번, BOJ 8394, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[8394번 - 악수](https://www.acmicpc.net/problem/8394)

## 설명

**직선 형태의 테이블에 앉은 사람들끼리 서로 악수하는 모든 가능한 방법의 수를 구하는 문제입니다.**

각 사람은 **자기 양옆에 있는 사람과 악수할 수도 있고, 하지 않을 수도 있지만,**

자리를 벗어나거나 건너뛴 사람과는 악수를 하지 않습니다.

<br>
예를 들어 사람이 `4명`일 경우, 가능한 조합은 다음과 같습니다:

- `아무도 악수하지 않음`
- `(1-2)`
- `(2-3)`
- `(3-4)`
- `(1-2)`, `(3-4)`

총 `5가지`의 경우가 가능합니다.

<br>
문제에서는 가능한 모든 방법의 수에서 **마지막 자릿수만 출력**하도록 요구함에 주의합니다.

<br>

## 접근법

이 문제는 **피보나치 수열과 동일한 점화식**을 따르는 구조를 가집니다.

각 사람에 대해 생각해보면,
- 마지막 사람이 **아무와도 악수하지 않는 경우**: `n - 1`명의 경우의 수와 동일
- 마지막 사람이 `n - 1`**번째 사람과 악수하는 경우**: 그 둘을 제외한 `n - 2`명의 경우의 수와 동일

<br>
즉, 사람 수를 `n`이라 할 때 가능한 경우의 수는 다음과 같이 정의됩니다:

$$
dp[n] = dp[n - 1] + dp[n - 2]
$$

<br>
즉, 점화식은 정확히 피보나치 수열과 같으며 초기 조건은 다음과 같습니다:
- `dp[0] = 1`
- `dp[1] = 1`

<br>
또한, 문제에서는 최종 출력 시 **마지막 자리 숫자만 출력하라고 했기 때문에**,

계산 과정에서 계속해서 `% 10`을 유지하는 모듈러 연산으로 메모리와 계산량을 줄일 수 있습니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int n = int.Parse(Console.ReadLine());
    if (n == 0 || n == 1) {
      Console.WriteLine(1);
      return;
    }

    int prev = 1, curr = 1;
    for (int i = 2; i <= n; i++) {
      int next = (prev + curr) % 10;
      prev = curr;
      curr = next;
    }
    Console.WriteLine(curr);
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

  vi dp(n + 1);
  dp[0] = dp[1] = 1;
  if (n > 1) dp[2] = 2;

  for (int i = 3; i <= n; ++i)
    dp[i] = (dp[i - 1] + dp[i - 2]) % 10;
  cout << dp[n] << "\n";

  return 0;
}
```
