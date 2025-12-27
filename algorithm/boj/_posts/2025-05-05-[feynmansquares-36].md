---
layout: single
title: "[백준 5724] 파인만 (C#, C++) - soo:bak"
date: "2025-05-05 05:33:00 +0900"
description: N × N 정사각형 그리드에서 만들 수 있는 모든 크기의 정사각형 개수를 계산하는 백준 5724번 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5724
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 5724, 백준 5724번, BOJ 5724, feynmansquares, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5724 - 파인만](https://www.acmicpc.net/problem/5724)

## 설명

`N × N` 크기의 정사각형 격자에서, **서로 다른 크기의 정사각형이 총 몇 개인지를 계산하는 문제**입니다.

<br>
즉, `1 × 1`, `2 × 2`, `...`, `N × N` 크기의 정사각형이 격자 내에서 몇 개씩 등장하는지를 모두 합산해야 합니다.

예를 들어 `N = 2`일 경우:
- `1 × 1` 정사각형은 총 `4개` (2×2)
- `2 × 2` 정사각형은 총 `1개`

→ 총합은 `5개`입니다.

<br>

## 접근법

- 각 정사각형 크기 `k × k`는,<br>
  `N × N` 격자 안에서 `(N - k + 1)^2` 개 만들 수 있습니다.
  - 이는 `N × N` 정사각형 격자에서,
    한 변의 길이가 `k`인 정사각형은 `각 행`과 `각 열`에서 `N - k + 1`개씩 배치할 수 있기 때문입니다.
- 따라서, 모든 가능한 크기의 정사각형을 전부 고려하려면, 이 값을 k = 1부터 N까지 모두 더해야 하며,<br>
  그 총합이 곧 서로 다른 정사각형의 개수가 됩니다.
- 이는 수학적으로 다음과 같이 정리됩니다:

  $$
  \sum_{k=1}^{N} k^2 = \frac{N(N+1)(2N+1)}{6}
  $$

<br>
> 참고 : [자연수 제곱합 공식의 원리와 유도 과정 - soo:bak](https://soo-bak.github.io/algorithm/theory/sumOfSquaresNatNums/)

<br>

---

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      int n = int.Parse(Console.ReadLine());
      if (n == 0) break;
      int res = n * (n + 1) * (2 * n + 1) / 6;
      Console.WriteLine(res);
    }
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

  int n;
  while (cin >> n && n)
    cout << n * (n + 1) * (2 * n + 1) / 6 << "\n";

  return 0;
}
```
