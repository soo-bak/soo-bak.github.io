---
layout: single
title: "[백준 28352] 10! (C#, C++) - soo:bak"
date: "2023-07-20 19:07:00 +0900"
description: 수학, 팩토리얼, 구현 등을 주제로 하는 백준 28352번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 28352
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 28352, 백준 28352번, BOJ 28352, FactorialTen, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [28352번 - 10!](https://www.acmicpc.net/problem/28352)

## 설명
팩토리얼의 계산과 단위 변환을 주제로하는 문제입니다. <br>

입력으로 주어지는 `n` 에 대하여 팩토리얼을 계산하고, 이를 문제에서 주어진 단위로 변환하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static long Factorial(int n) {
      long res = 1;
      for (int i = 1; i <= n; i++)
        res *= i;
      return res;
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      long secPerWeek = 7 * 24 * 60 * 60;
      long factorialN = Factorial(n);

      Console.WriteLine(factorialN / secPerWeek);

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

typedef long long ll;

ll factorial(int n) {
  ll res = 1;
  for(int i = 1; i <= n; i++)
    res *= i;
  return res;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  ll secPerWeek = 7 * 24 * 60 * 60;
  ll factorialN = factorial(n);

  cout << factorialN / secPerWeek << "\n";

  return 0;
}
  ```
