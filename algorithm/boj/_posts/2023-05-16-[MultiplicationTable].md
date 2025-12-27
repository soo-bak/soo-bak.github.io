---
layout: single
title: "[백준 2739] 구구단 (C#, C++) - soo:bak"
date: "2023-05-16 14:55:00 +0900"
description: 수학과 입력 출력을 주제로 하는 백준 2739번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2739
  - C#
  - C++
  - 알고리즘
keywords: "백준 2739, 백준 2739번, BOJ 2739, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2739번 - 구구단](https://www.acmicpc.net/problem/2739)

## 설명
입력으로 받은 숫자에 대해 간단한 구구단을 출력하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= 9; i++)
        Console.WriteLine($"{n} * {i} = {n * i}");

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

  for (int i = 1; i <= 9; i++)
    cout << n << " * " << i << " = " << n * i << "\n";

  return 0;
}
  ```
