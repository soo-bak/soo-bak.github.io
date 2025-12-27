---
layout: single
title: "[백준 2581] 소수 (C#, C++) - soo:bak"
date: "2023-05-28 07:20:00 +0900"
description: 수학과 소수 찾기, 에라토스테네스의 체를 주제로 하는 백준 2581번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2581
  - C#
  - C++
  - 알고리즘
keywords: "백준 2581, 백준 2581번, BOJ 2581, PrimeNumber, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2581번 - 소수](https://www.acmicpc.net/problem/2581)

## 설명
문제에서 주어진 범위 `m` 이상 `n` 이하의 자연수 중 소수를 모두 찾고, <br>

그 소수들의 `합` 과 `최솟값` 을 출력하는 문제입니다. <br>

`소수` 는 `1` 과 자기 자신 외에는 어떤 자연수로도 나누어 떨어지지 않는 `1` 보다 큰 자연수 입니다. <br>

어떤 수 `n` 에 대하여 소수 여부를 판별할 때, 해당 수를 직접 `2` 부터 모두 나누어보며 나머지가 있는지 없는지 확인하며 소수를 판별할 수도 있습니다. <br>

하지만, 더 효율적인 방법은 `에라토스테네스의 체` 알고리즘을 사용하는 것입니다. <br>

<br>

> 참고 : [에라토스테네스의 체 (Sieve of Eratosthenes) - soo:bak](https://soo-bak.github.io/algorithm/theory/SieveOfEratosthenes/)

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var m = int.Parse(Console.ReadLine()!);
      var n = int.Parse(Console.ReadLine()!);

      var isPrime = Enumerable.Repeat(true, n + 1).ToArray();
      isPrime[0] = isPrime[1] = false;

      for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
          for (int j = i * i; j <= n; j += i) {
            isPrime[j] = false;
          }
        }
      }

      int sum = 0, minPrime = -1;
      for (int i = m; i <= n; i++) {
        if (isPrime[i]) {
          sum += i;
          if (minPrime == -1) minPrime = i;
        }
      }

      if (minPrime == -1) Console.WriteLine(-1);
      else {
        Console.WriteLine(sum);
        Console.WriteLine(minPrime);
      }

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

  int m, n; cin >> m >> n;

  vector<bool> isPrime(n + 1, true);
  isPrime[0] = isPrime[1] = false;

  for (int i = 2; i * i <= n; i++) {
    if (isPrime[i]) {
      for (int j = i * i; j <= n; j+= i)
        isPrime[j] = false;
    }
  }

  int sum = 0, minPrime = -1;
  for (int i = m; i <= n; i++) {
    if (isPrime[i]) {
      sum += i;
      if (minPrime == -1) minPrime = i;
    }
  }

  if (minPrime == -1) cout << -1 << "\n";
  else cout << sum << "\n" << minPrime << "\n";

  return 0;
}
  ```
