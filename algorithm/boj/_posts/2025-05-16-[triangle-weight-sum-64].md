---
layout: single
title: "[백준 2721] 삼각수의 합 (C#, C++) - soo:bak"
date: "2025-05-16 21:15:00 +0900"
description: 삼각수에 가중치를 곱해 누적한 값을 계산하는 백준 2721번 삼각수의 합 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2721
  - C#
  - C++
  - 알고리즘
keywords: "백준 2721, 백준 2721번, BOJ 2721, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2721번 - 삼각수의 합](https://www.acmicpc.net/problem/2721)

## 설명

**삼각수에 일정한 가중치를 곱해 누적한 값을 구하는 수열 문제입니다.**

삼각수란 `1 + 2 + ... + n` 형태로 누적되는 수이며, 다음의 수식으로 계산할 수 있습니다:

$$
T(n) = \frac{n(n + 1)}{2}
$$

이 문제에서 요구하는 값 `W(n)`은 다음의 가중치 합으로 정의됩니다:

$$
W(n) = \sum_{k = 1}^{n} k \cdot T(k + 1)
$$

즉, `(k + 1)`번째 삼각수를 구한 뒤, 거기에 `k`를 곱하고,<br>
이 값을 `k = 1`부터 `n`까지 모두 더한 결과를 출력하는 문제입니다.

<br>

## 접근법

주어진 수식 구조를 그대로 구현하면 다음과 같은 형태가 됩니다:

- 각 `k`에 대해:
  - `T(k + 1) = (k + 1)(k + 2)/2` 를 먼저 구하고,
  - 여기에 `k`를 곱한 값을 누적합에 더해줍니다.

<br>
> 참고 : [1부터 n까지 자연수의 합과 삼각수 - soo:bak](https://soo-bak.github.io/algorithm/theory/TriNum/)

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());
    while (t-- > 0) {
      int n = int.Parse(Console.ReadLine());
      long sum = 0;
      for (int i = 1; i <= n; i++) {
        long tri = (long)(i + 1) * (i + 2) / 2;
        sum += tri * i;
      }
      Console.WriteLine(sum);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    int n; cin >> n;
    ll sum = 0;
    for (int i = 1; i <= n; ++i)
      sum += (ll)(i + 1) * (i + 2) / 2 * i;
    cout << sum << "\n";
  }

  return 0;
}
```
