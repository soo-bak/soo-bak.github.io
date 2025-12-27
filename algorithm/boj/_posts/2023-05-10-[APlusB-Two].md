---
layout: single
title: "[백준 2558] A+B - 2 (C#, C++) - soo:bak"
date: "2023-05-10 11:33:00 +0900"
description: 수학과 사칙연산을 주제로 하는 백준 2558번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2558
  - C#
  - C++
  - 알고리즘
  - 구현
  - arithmetic
  - 수학
keywords: "백준 2558, 백준 2558번, BOJ 2558, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2558번 - A+B - 2](https://www.acmicpc.net/problem/2558)

## 설명
기본적인 사칙 연산 문제입니다. <br>

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

      Console.WriteLine($"{a + b}");

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

  cout << a + b << "\n";

  return 0;
}
  ```
