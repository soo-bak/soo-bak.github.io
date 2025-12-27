---
layout: single
title: "[백준 27331] 2 桁の整数 (Two-digit Integer) (C#, C++) - soo:bak"
date: "2023-05-10 00:52:00 +0900"
description: 수학과 수의 자릿수 다루기, 사칙 연산을 주제로 하는 백준 27331번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27331
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 27331, 백준 27331번, BOJ 27331, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27331번 - 2 桁の整数 (Two-digit Integer)](https://www.acmicpc.net/problem/27331)

## 설명
입력으로 주어지는 두 개의 정수 `a` 와 `b` 를 사용하여 두 자리 양의 정수를 출력하는 문제입니다. <br>

문제의 조건에 따르면, `a` 는 10의 자리 숫자로 사용해야 하며, `b` 는 1의 자리 숫자로 사용해야 합니다. <br>

간단한 수식을 활용하여 최종적으로 계산된 숫자를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var a = int.Parse(Console.ReadLine()!);
      var b = int.Parse(Console.ReadLine()!);

      var ret = (10 * a) + b;

      Console.WriteLine(ret);

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

  int a, b; cin >> a >> b;

  int ret = (10 * a) + b;

  cout << ret << "\n";

  return 0;
}
  ```
