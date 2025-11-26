---
layout: single
title: "[백준 11444] 피보나치 수 6 (C#, C++) - soo:bak"
date: "2025-11-27 00:40:00 +0900"
description: 행렬 거듭제곱과 빠른 거듭제곱으로 피보나치 수를 O(log n) 시간에 구하는 백준 11444번 피보나치 수 6 문제의 C# 및 C++ 풀이
---

## 문제 링크
[11444번 - 피보나치 수 6](https://www.acmicpc.net/problem/11444)

## 설명

피보나치 수열이 `F₀ = 0`, `F₁ = 1`, `Fₙ = Fₙ₋₁ + Fₙ₋₂ (n ≥ 2)`로 정의되는 상황에서 `n (1 ≤ n ≤ 10¹⁸)`이 주어질 때, `Fₙ mod 1,000,000,007`을 구하는 문제입니다.

`n`이 최대 10¹⁸으로 매우 크므로 단순 반복으로는 시간 내에 계산할 수 없습니다.

<br>

## 접근법

단순 반복으로는 시간 내에 계산할 수 없으므로 행렬 거듭제곱을 사용합니다.

피보나치 점화식을 행렬로 표현하면 `[[Fₙ₊₁, Fₙ], [Fₙ, Fₙ₋₁]] = [[1, 1], [1, 0]]ⁿ`이 성립하며, 2×2 행렬 `[[1, 1], [1, 0]]`을 n번 거듭제곱한 결과의 `[0][1]` 위치 값이 `Fₙ`이 됩니다.

행렬 거듭제곱은 빠른 거듭제곱(분할 정복)을 사용하여 O(log n) 시간에 계산할 수 있습니다.

<br>
빠른 거듭제곱은 지수를 이진수로 표현하는 원리를 이용합니다.

예를 들어, A⁵ = A⁽¹⁰¹⁾₂ = A⁴ × A¹이므로, 지수가 홀수일 때만 결과에 현재 기저를 곱하고, 기저를 제곱하면서 지수를 절반으로 줄여나가면 O(log n)번의 곱셈으로 계산할 수 있습니다.

모든 행렬 곱셈 과정에서 각 원소를 1,000,000,007로 나눈 나머지를 취하여 오버플로를 방지합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    const long MOD = 1_000_000_007;

    static long[,] Multiply(long[,] a, long[,] b) {
      var res = new long[2, 2];

      for (var i = 0; i < 2; i++)
        for (var j = 0; j < 2; j++)
          for (var k = 0; k < 2; k++)
            res[i, j] = (res[i, j] + a[i, k] * b[k, j]) % MOD;

      return res;
    }

    static long[,] Pow(long[,] baseM, long n) {
      var result = new long[,] { {1, 0}, {0, 1} };

      while (n > 0) {
        if ((n & 1) == 1) result = Multiply(result, baseM);

        baseM = Multiply(baseM, baseM);
        n >>= 1;
      }

      return result;
    }

    static void Main(string[] args) {
      var n = long.Parse(Console.ReadLine()!);
      var a = new long[,] { {1, 1}, {1, 0} };

      var mat = Pow(a, n);

      Console.WriteLine(mat[0, 1]);
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

const ll MOD = 1'000'000'007;

struct Mat {
  ll m[2][2];
};

Mat mul(const Mat& a, const Mat& b) {
  Mat r{};

  for (int i = 0; i < 2; i++)
    for (int j = 0; j < 2; j++)
      for (int k = 0; k < 2; k++)
        r.m[i][j] = (r.m[i][j] + a.m[i][k] * b.m[k][j]) % MOD;

  return r;
}

Mat mpow(Mat base, ll n) {
  Mat res = {{{1, 0}, {0, 1}}};

  while (n > 0) {
    if (n & 1) res = mul(res, base);

    base = mul(base, base);
    n >>= 1;
  }

  return res;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll n; cin >> n;

  Mat a = {{{1, 1}, {1, 0}}};
  Mat r = mpow(a, n);

  cout << r.m[0][1] << "\n";

  return 0;
}
```

