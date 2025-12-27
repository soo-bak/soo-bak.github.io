---
layout: single
title: "[백준 27960] 사격 내기 (C#, C++) - soo:bak"
date: "2023-05-16 12:33:00 +0900"
description: 수학과 사칙연산, 비트 연산과 논리 연산자를 주제로 하는 백준 27960번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27960
  - C#
  - C++
  - 알고리즘
  - 수학
  - 비트마스킹
keywords: "백준 27960, 백준 27960번, BOJ 27960, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27960번 - 사격 내기](https://www.acmicpc.net/problem/27960)

## 설명
`A` 와 `B` 가 각각 얻은 점수가 주어졌을 때, `C` 가 얻은 점수를 계산하는 문제입니다.<br>

문제의 조건에 따르면, `C` 의 점수는 `A` 와 `B` 둘 중 한 명만 맞춘 과녁에 대해서 점수를 얻습니다. <br>

간단히 `논리 XOR` 연산을 사용하여 `C` 의 점수를 계산합니다.

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var scoreA = int.Parse(input[0]);
      var scoreB = int.Parse(input[1]);

      var scoreC = scoreA ^ scoreB;

      Console.WriteLine(scoreC);

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

  int scoreA, scoreB; cin >> scoreA >> scoreB;

  int scoreC = scoreA ^ scoreB;

  cout << scoreC << "\n";

  return 0;
}
  ```
