---
layout: single
title: "[백준 10870] 피보나치 수 5 (C#, C++) - soo:bak"
date: "2023-05-22 16:18:00 +0900"
description: 수학과 피보나치 수열, 다이나믹 프로그래밍을 주제로 하는 백준 10870번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10870
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 10870, 백준 10870번, BOJ 10870, FibonacciNumberFive, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [10870번 - 피보나치 수 5](https://www.acmicpc.net/problem/10870)

## 설명
피보나치 수열에서 `n` 번째 피보나치 수를 구하는 문제입니다. <br>

피보나치 수열을 구현하는 방법에는 여러 가지가 있지만,<br>

문제에서의 `n` 의 범위를 고려하여 다이나믹 프로그래밍을 활용하여 풀이하였습니다. <br>

<br>

> 참고 : [피보나치 수열 (Fibonacci Sequence) - soo:bak](https://soo-bak.github.io/algorithm/theory/fibonacciSeq/)

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      const int MAX = 21;

      var fibo = new int[MAX];
      fibo[0] = 0; fibo[1] = 1;

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 2; i <= n; i++)
        fibo[i] = fibo[i - 1] + fibo[i - 2];

      Console.WriteLine(fibo[n]);

    }
  }
}

  ```
<br><br>
<b>[ C++ ] </b>
<br>

  ```c++
#include <bits/stdc++.h>

#define MAX 21

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<int> fibo(MAX);
  fibo[0] = 0; fibo[1] = 1;

  int n; cin >> n;

  for (int i = 2; i <= n; i++)
    fibo[i] = fibo[i - 1] + fibo[i - 2];

  cout << fibo[n] << "\n";

  return 0;
}
  ```
