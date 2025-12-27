---
layout: single
title: "[백준 1145] 적어도 대부분의 배수 (C#, C++) - soo:bak"
date: "2025-05-16 21:49:00 +0900"
description: 다섯 수 중 세 수의 최소공배수를 구해 가장 작은 배수를 찾는 백준 1145번 적어도 대부분의 배수 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1145
  - C#
  - C++
  - 알고리즘
  - 브루트포스
keywords: "백준 1145, 백준 1145번, BOJ 1145, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[1145번 - 적어도 대부분의 배수](https://www.acmicpc.net/problem/1145)

## 설명

**주어진 다섯 개의 자연수 중 적어도 세 수의 공배수 중 가장 작은 수를 찾는 문제입니다.**

문제에서 정의하는 ‘적어도 대부분의 배수’란 다음 조건을 만족하는 **가장 작은 자연수**를 말합니다:

- 다섯 수 중 **세 개 이상으로 나누어지는 수** 중 가장 작은 수

<br>
예를 들어 `1 2 3 4 5`가 입력으로 주어졌다면, `4`는 `1`, `2`, `4`로 나누어 떨어지므로 정답이 됩니다.

<br>

## 접근법

총 다섯 개의 수 중 **세 수를 선택**해서 최소공배수(LCM)를 구합니다.

- 모든 조합은 $$ \binom{5}{3} = 10 $$ 가지이므로, 모든 경우를 전부 시도해도 성능에 문제가 없습니다.
- 각 조합에 대해 다음 순서로 처리합니다:
  - 두 수의 LCM을 구한 뒤, 세 번째 수와 다시 LCM을 계산합니다.
  - 구한 LCM 값 중 가장 작은 값을 기록합니다.
- LCM을 계산할 때는 **유클리드 호제법 기반의 GCD**를 이용해 다음 공식을 활용합니다:

$$
\text{LCM}(a, b) = \frac{a \times b}{\text{GCD}(a, b)}
$$

이 과정을 모든 세 수 조합에 대해 반복하며 최솟값을 찾습니다.

<br>

> 참고 : [GCD(최대공약수)와 유클리드 호제법의 원리 - soo:bak](https://soo-bak.github.io/algorithm/theory/gcd-euclidean-explained/)

<br>

## Code

### C#
```csharp
using System;

class Program {
  static int GCD(int a, int b) => b == 0 ? a : GCD(b, a % b);
  static int LCM(int a, int b) => a / GCD(a, b) * b;

  static void Main() {
    var tokens = Console.ReadLine().Split();
    var nums = Array.ConvertAll(tokens, int.Parse);

    int minLCM = int.MaxValue;
    for (int i = 0; i < 3; i++) {
      for (int j = i + 1; j < 4; j++) {
        for (int k = j + 1; k < 5; k++) {
          int lcm = LCM(nums[i], nums[j]);
          lcm = LCM(lcm, nums[k]);
          minLCM = Math.Min(minLCM, lcm);
        }
      }
    }

    Console.WriteLine(minLCM);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> vi;

int gcd(int a, int b) {
  return b ? gcd(b, a % b) : a;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vi a(5);
  for (int& x : a) cin >> x;

  int lcmMin = INT_MAX;
  for (int i = 0; i < 3; ++i) {
    for (int j = i + 1; j < 4; ++j) {
      for (int k = j + 1; k < 5; ++k) {
        int g = gcd(a[i], a[j]);
        int lcm = a[i] / g * a[j];
        g = gcd(lcm, a[k]);
        lcm = lcm / g * a[k];
        lcmMin = min(lcmMin, lcm);
      }
    }
  }

  cout << lcmMin << "\n";

  return 0;
}
```
