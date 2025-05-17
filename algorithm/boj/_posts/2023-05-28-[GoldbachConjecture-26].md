---
layout: single
title: "[백준 9020] 골드바흐의 추측 (C#, C++) - soo:bak"
date: "2023-05-28 16:10:00 +0900"
description: 수학과 골드바흐의 추측, 에라토스테네스의 체 와 소수 찾기 등을 주제로 하는 백준 9020번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [9020번 - 골드바흐의 추측](https://www.acmicpc.net/problem/9020)

## 설명
`2` 보다 큰 모든 짝수는 `두 소수의 합` 으로 나타낼 수 있다는 `골드바흐의 추측` 을 적용하는 문제입니다. <br>

`에라토스테네스의 체` 알고리즘을 활용하여, 입력으로 주어지는 수 `n` 까지의 소수를 찾고, `n` 을 두 소수의 합으로 나타내는 방법을 찾습니다. <br>

이 때, 두 소수의 차이가 가장 작은 경우부터 찾아서 출력해야 합니다. <br>

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

      const int MAX = 10_000;

      var isPrime = Enumerable.Repeat(true, MAX + 1).ToArray();
      isPrime[0] = isPrime[1] = false;

      for (int i = 2; i * i <= MAX; i++) {
        if (isPrime[i]) {
          for (int j = i * i; j <= MAX; j += i)
            isPrime[j] = false;
        }
      }

      var cntCase = int.Parse(Console.ReadLine()!);
      for (int c = 0; c < cntCase; c++) {
        var n = int.Parse(Console.ReadLine()!);

        var a = n / 2;
        var b = n / 2;

        while (a > 0) {
          if (isPrime[a] && isPrime[b]) {
            Console.WriteLine($"{a} {b}");
            break ;
          }
          a--;
          b++;
        }
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

#define MAX 10'000

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<bool> isPrime(MAX + 1, true);
  isPrime[0] = isPrime[1] = false;

  for (int i = 2; i * i <= MAX; i++) {
    if (isPrime[i]) {
      for (int j = i * i; j <= MAX; j += i)
        isPrime[j] = false;
    }
  }

  int cntCase; cin >> cntCase;
  for (int c = 0; c < cntCase; c++) {
    int n; cin >> n;

    int a = n / 2, b = n / 2;

    while (a > 0) {
      if (isPrime[a] && isPrime[b]) {
        cout << a << " " << b << "\n";
        break ;
      }
      a--;
      b++;
    }
  }

  return 0;
}
  ```
