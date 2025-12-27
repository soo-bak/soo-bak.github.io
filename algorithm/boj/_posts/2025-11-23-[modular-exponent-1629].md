---
layout: single
title: "[백준 1629] 곱셈 (C#, C++) - soo:bak"
date: "2025-11-23 02:45:00 +0900"
description: 거듭제곱을 분할 정복으로 계산한 뒤 모듈러 연산을 곱셈 과정마다 적용해 오버플로와 시간 초과를 모두 피하는 백준 1629번 곱셈 문제의 C# 및 C++ 풀이
tags:
  - 백준
  - BOJ
  - 1629
  - C#
  - C++
  - 알고리즘
keywords: "백준 1629, 백준 1629번, BOJ 1629, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1629번 - 곱셈](https://www.acmicpc.net/problem/1629)

## 설명

자연수 `A`, `B`, `C`가 주어질 때 `A^B mod C`를 계산하는 문제입니다.

`B`는 최대 약 21억까지 가능하므로 `A`를 `B`번 반복해서 곱하는 방식으로는 시간 초과가 발생합니다.

또한 곱셈 중간 결과가 64비트 범위를 넘을 수 있어 매 단계마다 모듈러 연산을 적용하여 값을 작게 유지해야 합니다.

<br>

## 접근법

분할 정복 거듭제곱(Exponentiation by Squaring)을 사용하여 `O(log B)` 시간에 계산합니다.

지수 `B`가 짝수일 때는 `A^B = (A^{B/2})²`로, 홀수일 때는 `A^B = A × A^{B-1}`로 나누어 계산하면 지수를 절반씩 줄일 수 있습니다.

또한, 이를 반복문 방식으로 구현하면 재귀 깊이 제한을 피할 수 있습니다.

`B`의 각 비트를 검사하여 해당 비트가 1이면 현재 밑수를 결과에 곱하고, 밑수는 매번 제곱합니다.

`B`를 오른쪽으로 1비트씩 이동시키며 0이 될 때까지 반복합니다.

매 곱셈마다 `mod C`를 적용하여 중간 결과가 64비트를 초과하지 않도록 합니다.

초기값은 `result = 1`, `base = A mod C`로 설정합니다.

<br>

---

## Code

### C#

```csharp
using System;

namespace Solution {
  class Program {
    static long ModPow(long a, long b, long mod) {
      var result = 1L % mod;
      var baseValue = a % mod;

      while (b > 0) {
        if ((b & 1) == 1)
          result = (result * baseValue) % mod;

        baseValue = (baseValue * baseValue) % mod;
        b >>= 1;
      }

      return result;
    }

    static void Main(string[] args) {
      var tokens = Console.ReadLine()!.Split();
      var a = long.Parse(tokens[0]);
      var b = long.Parse(tokens[1]);
      var c = long.Parse(tokens[2]);

      Console.WriteLine(ModPow(a, b, c));
    }
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

ll modPow(ll a, ll b, ll mod) {
  ll result = 1 % mod;
  ll base = a % mod;

  while (b > 0) {
    if (b & 1) result = (result * base) % mod;
    base = (base * base) % mod;
    b >>= 1;
  }

  return result;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b, c; cin >> a >> b >> c;

  cout << modPow(a, b, c) << "\n";

  return 0;
}
```

