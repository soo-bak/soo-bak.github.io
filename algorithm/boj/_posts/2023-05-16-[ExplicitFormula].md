---
layout: single
title: "[백준 3533] Explicit Formula (C#, C++) - soo:bak"
date: "2023-05-16 12:24:00 +0900"
description: 논리 연산과 비트 연산자 등을 주제로 하는 백준 3533번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3533
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 3533, 백준 3533번, BOJ 3533, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [3533번 - Explicit Formula](https://www.acmicpc.net/problem/3533)

## 설명
주어진 논리 공식을 계산하는 문제입니다. <br>

문제의 목표는 모든 `pair` 와 `triplet` 에 대해 적어도 하나의 변수가 `1` 인 경우를 세고, <br>

그 수가 홀수인지 짝수인지 판별하는 함수를 계산하는 것입니다. <br>

각 `pair` 와 `triplet` 에 대해 `논리 OR` 연산을 수행한 후, 그 결과들에 대해 모두 `논리 XOR` 연산을 수행하여 계산합니다.  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var b = new bool[10];

      var input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < 10; i++)
        b[i] = (int.Parse(input[i]) == 1);

      bool res = false;
      for (int i = 0; i < 10; i++) {
        for (int j = i + 1; j < 10; j++) {
          res ^= (b[i] || b[j]);
          for (int k = j + 1; k < 10; k++)
            res ^= (b[i] || b[j] || b[k]);
        }
      }

      Console.WriteLine(res ? "1" : "0");

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

  bool b[10];
  for (int i = 0; i < 10; i++)
    cin >> b[i];

  bool res = 0;
  for (int i = 0; i < 10; i++) {
    for (int j = i + 1; j < 10; j++) {
      res ^= (b[i] || b[j]);
      for (int k = j + 1; k < 10; k++)
        res ^= (b[i] || b[j] || b[k]);
    }
  }

  cout << res << "\n";

  return 0;
}
  ```
