---
layout: single
title: "[백준 2502] 떡 먹는 호랑이 (C#, C++) - soo:bak"
date: "2025-05-16 20:40:00 +0900"
description: 피보나치 계수로 구성된 수열의 특정 항 합을 맞추는 조합을 찾는 백준 2502번 떡 먹는 호랑이 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2502
  - C#
  - C++
  - 알고리즘
  - 수학
  - 다이나믹 프로그래밍
  - 브루트포스
keywords: "백준 2502, 백준 2502번, BOJ 2502, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2502번 - 떡 먹는 호랑이](https://www.acmicpc.net/problem/2502)

## 설명

**피보나치 수열처럼 구성된 떡의 양에 대해, 첫째 날과 둘째 날의 떡 개수를 찾아내는 문제입니다.**

호랑이는 다음 조건으로 떡을 요구합니다:

- 셋째 날부터는 전날과 그 전날에 준 떡의 개수를 합쳐서 요구합니다.
- 예를 들어, `A = 2, B = 7`이라면 수열은 `2, 7, 9, 16, 25, 41`로 이어집니다.

<br>
이때, `D`일째 날에 받은 떡의 개수 `K`가 주어지면 가능한 `A`, `B` 조합 중 하나를 출력해야 합니다.

단, 항상 `1 ≤ A ≤ B` 조건이 보장되며, 해는 항상 존재합니다.

<br>

## 접근법

우선 피보나치 수열처럼 **수식 기반 계수를 먼저 계산**합니다.

- `a[i]`: `i`번째 날에 `A`가 몇 번 더해지는지를 나타내는 계수
- `b[i]`: `i`번째 날에 `B`가 몇 번 더해지는지를 나타내는 계수

`a[0] = 1`, `b[1] = 1`로 초기화하고, 이후에는 일반적인 피보나치 수열처럼:

- `a[i] = a[i - 1] + a[i - 2]`
- `b[i] = b[i - 1] + b[i - 2]`

이렇게 만들어두면, `D`일째 날에 준 떡의 개수는 다음과 같은 식이 됩니다:

$$
K = A \cdot a[D-1] + B \cdot b[D-1]
$$

이를 만족하는 `(A, B)`를 찾아야 하므로, 가능한 `A` 값을 기준으로 완전탐색을 수행합니다.

- A를 `1`부터 증가시키며 위 식에 대해 `B`가 정수로 존재하는지 확인
- B는 `(K - A × a[D-1]) / b[D-1]` 로 계산할 수 있으며, 나머지가 `0`이어야 함

이 과정을 통해 조건을 만족하는 `A` 와 `B`를 찾으면 바로 출력합니다.

<br>
> 참고 : [피보나치 수열 (Fibonacci Sequence) - soo:bak](https://soo-bak.github.io/algorithm/theory/fibonacciSeq/)

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    int d = int.Parse(input[0]);
    int k = int.Parse(input[1]);

    var a = new int[d];
    var b = new int[d];
    a[0] = 1; b[1] = 1;
    for (int i = 2; i < d; i++) {
      a[i] = a[i - 1] + a[i - 2];
      b[i] = b[i - 1] + b[i - 2];
    }

    for (int A = 1; A <= k; A++) {
      int rem = k - A * a[d - 1];
      if (rem % b[d - 1] == 0) {
        int B = rem / b[d - 1];
        Console.WriteLine(A);
        Console.WriteLine(B);
        break;
      }
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

  int n, k; cin >> n >> k;
  vi a(n), b(n);
  a[0] = 1; b[1] = 1;
  for (int i = 2; i < n; ++i) {
    a[i] = a[i-1] + a[i-2];
    b[i] = b[i-1] + b[i-2];
  }

  for (int x = 1; x <= k; ++x) {
    int rem = k - a[n-1] * x;
    if (rem % b[n-1] == 0) {
      cout << x << "\n" << rem / b[n-1] << "\n";
      return 0;
    }
  }

  return 0;
}
```
