---
layout: single
title: "[백준 21983] Basalt Breakdown (C#, C++) - soo:bak"
date: "2024-01-02 08:07:00 +0900"
description: 수학, 기하학, 사칙연산 을 주제로 하는 백준 21983번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 21983
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
  - arithmetic
keywords: "백준 21983, 백준 21983번, BOJ 21983, BasaltBreakdown, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [21983번 - Basalt Breakdown](https://www.acmicpc.net/problem/21983)

## 설명
문제의 목표는 규칙적인 육각형의 면적이 주어졌을 때, 그 둘레를 계산하는 것입니다. <br>
<br>
- 정육각형의 면적은 변의 길이를 `s` 라고 할 때, $$\frac{(3 \sqrt{3})}{2} \times s^2$$<br>
<br>

위 식을 활용하여 주어진 면적 `a` 에 대하여 변의 길이 `s` 를 계산하고, 둘레 `6s` 를 계산하여 출력합니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      double area = double.Parse(Console.ReadLine()!);

      double sideLength = Math.Sqrt((2 * area) / (3 * Math.Sqrt(3)));
      double perimeter = 6 * sideLength;

      Console.WriteLine($"{perimeter:F6}");

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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll area; cin >> area;

  double sideLength = sqrt((2 * area) / (3 * sqrt(3)));
  double perimeter = 6 * sideLength;

  cout.flags(ios::fixed); cout.precision(6);
  cout << perimeter << "\n";

  return 0;
}
  ```
