---
layout: single
title: "[백준 1978] 소수 찾기 (C#, C++) - soo:bak"
date: "2023-05-23 09:09:00 +0900"
description: 수학과 소수 탐색의 기본을 주제로 하는 백준 1978번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1978
  - C#
  - C++
  - 알고리즘
keywords: "백준 1978, 백준 1978번, BOJ 1978, FindingPrimeNum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [1978번 - 소수 찾기](https://www.acmicpc.net/problem/1978)

## 설명
입력으로 주어지는 `n` 개의 숫자들 중 `소수` 의 개수를 찾는 문제입니다. <br>

소수를 판별하는 방법에는 여러가지가 있지만, 문제에서의 `n` 의 범위가 작다는 것을 고려했을 때 가장 기본적인 방법을 사용하여 풀이하였습니다. <br>

판별하고자 하는 수를 `2` 부터 해당 수의 제곱근까지 나누어보는 것입니다. <br>

만약, 해당 범위에서 나누어 떨어지는 수가 있다면, 그 수는 소수가 아니게 됩니다.<br>

숫자 `1` 도 소수가 아니라는 점에 주의합니다. <br>

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

    static bool IsPrime(int num) {
      if (num < 2) return false;

      for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) return false;
      }
      return true;
    }

    static void Main(string[] args) {

      int n = int.Parse(Console.ReadLine()!);

      var numbers = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

      var cntPrimeNums = numbers.Count(IsPrime);

      Console.WriteLine(cntPrimeNums);

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

bool isPrime(int num) {
  if (num < 2) return false;

  for (int i = 2; i <= sqrt(num); i++) {
    if (num % i == 0) return false;
  }
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  vector<int> numbers(n);
  for (int i = 0; i < n; i++)
    cin >> numbers[i];

  int cntPrimeNums = 0;
  for (int i = 0; i < n; i++) {
    if (isPrime(numbers[i]))
      cntPrimeNums++;
  }

  cout << cntPrimeNums << "\n";

  return 0;
}
  ```
