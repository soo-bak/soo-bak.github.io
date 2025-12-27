---
layout: single
title: "[백준 11653] 소인수분해 (C#, C++) - soo:bak"
date: "2023-05-28 15:38:00 +0900"
description: 수학과 소수 찾기, 소인수 분해를 주제로 하는 백준 11653번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 11653
  - C#
  - C++
  - 알고리즘
  - 수학
  - 정수론
  - primality_test
  - prime_factorization
keywords: "백준 11653, 백준 11653번, BOJ 11653, FactorizationOfFactors, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [11653번 - 소인수분해](https://www.acmicpc.net/problem/11653)

## 설명
입력으로 주어진 숫자 `n` 을 소인수분해하는 문제입니다. <br>

<br>
소인수분해 알고리즘을 구현하는 방법에는 여러가지가 있지만,<br>

가장 간단한 구현 방법은 주어진 숫자를 `2` 부터 시작하여 주어진 숫자의 제곱근까지 계속 나누어 보는 방법입니다. <br>

주어진 숫자를 어떤 수로 나누었을 때, 나누어 떨어진다면 그 수는 주어진 숫자의 소인수입니다. <br>

<br>
이 때, 나누어 떨어지지 않을 때까지 계속 나누어야 한다는 점에 주의해야합니다. <br>

그 이유는 소인수분해 결과에 같은 소인수가 여러 번 나올 수 있기 때문입니다. <br>

<br>
`2` 부터 어떤 수의 제곱근까지 반복하여 나눈 후에도 남은 숫자가 `1` 보다 크다면, 그 수는 마지막 소인수가 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 2; i * i <= n; i++) {
        while (n % i == 0) {
          Console.WriteLine(i);
          n /= i;
        }
      }

      if (n > 1) Console.WriteLine(n);

    }
  }
}
  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 2; i * i <= n; i++) {
    while (n % i == 0) {
      cout << i << "\n";
      n /= i;
    }
  }

  if (n > 1) cout << n << "\n";

  return 0;
}
  ```
