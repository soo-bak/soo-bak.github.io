---
layout: single
title: "[백준 27262] Лифт (C#, C++) - soo:bak"
date: "2023-04-23 07:33:00 +0900"
description: 수학과 시칙연산을 주제로 하는 백준 27262번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27262
  - C#
  - C++
  - 알고리즘
keywords: "백준 27262, 백준 27262번, BOJ 27262, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27262번 - Лифт](https://www.acmicpc.net/problem/27262)

## 설명
간단한 사칙연산 문제입니다. <br>

문제의 목표는 거주하는 층 `n` , 현재 위치한 엘레베이터의 층 `k`, 계단을 이동하는 데 걸리는 시간 `k`, <br>
엘리베이터가 각 층을 이동하는 데에 걸리는 시간 `b` 가 주어졌을 때, <b>엘레베이터를 이용하는 경우의 시간</b>과 <br>
<b>계단을 이용하는 경우의 시간</b>을 각각 계산하는 것입니다. <br>

주어진 조건에 따르면, 각각의 시간은 다음과 같이 계산됩니다. <br>

<b>엘레베이터를 이용하는 경우의 시간</b> <br>
  = 엘레베이터가 1층에 도달하는 시간 + 엘레베이터가 n층으로 이동하는 시간<br>
  = (abs(`1` - `k`) * `b`) + (`n` - `1`) * `b`<br>

<b>계단을 이용하는 경우의 시간</b><br>
  = (`n` - `1`) * `b`<br>

결과값을 계산한 후, 문제에서 주어진 출력 조건에 따라 적절히 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()?.Split();
      var n = int.Parse(input![0]);
      var k = int.Parse(input![1]);
      var a = int.Parse(input![2]);
      var b = int.Parse(input![3]);

      var elevTime = Math.Abs(1 - k) * b + (n - 1) * b;
      var stairTime = (n - 1) * a;

      Console.WriteLine($"{elevTime} {stairTime}");

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

  int n, k, a, b; cin >> n >> k >> a >> b;

  int elevTime = abs(1 - k) * b + (n - 1) * b;
  int stairTime = (n - 1) * a;

  cout << elevTime << " " << stairTime << "\n";

  return 0;
}
  ```
