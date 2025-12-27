---
layout: single
title: "[백준 22279] Quality-Adjusted Life-Year (C#, C++) - soo:bak"
date: "2023-09-07 12:13:00 +0900"
description: 수학, 사칙 연산, 구현 등을 주제로 하는 백준 22279번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 22279
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 22279, 백준 22279번, BOJ 22279, QualityAdjusted, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [22279번 - Quality-Adjusted Life-Year](https://www.acmicpc.net/problem/22279)

## 설명
문제의 목표는 주어진 기간 동안의 각 질병 수준에 따른 `QALY` 를 계산하는 것입니다.<br>
<br>
`QALY` 는 주어진 기간 동안의 품질 `q` 와 `y` 의 곱으로 계산됩니다. <br>
<br>
모든 주어진 기간 동안에 대하여 `QALY` 를 계산하고, 그 값을 합하여 출력합니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      var totalQALY = 0.0;
      for (int i = 0; i < n; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var q = double.Parse(input[0]);
        var y = double.Parse(input[1]);
        totalQALY += q * y;
      }

      Console.WriteLine($"{totalQALY:F3}");

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

  double totalQALY = 0.0;
  for (int i = 0; i < n; i++) {
    double q, y; cin >> q >> y;
    totalQALY += q * y;
  }

  cout.setf(ios::fixed); cout.precision(3);
  cout << totalQALY << "\n";

  return 0;
}
  ```
