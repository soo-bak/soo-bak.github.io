---
layout: single
title: "[백준 2475] 검증수 (C#, C++) - soo:bak"
date: "2023-05-25 12:17:00 +0900"
description: 수학과 제곱수를 주제로 하는 백준 2475번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2475
  - C#
  - C++
  - 알고리즘
keywords: "백준 2475, 백준 2475번, BOJ 2475, VerificationNumber, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2475번 - 검증수](https://www.acmicpc.net/problem/2475)

## 설명
입력으로 주어지는 `5` 개의 숫자를 각각 제곱하여, 그 합을 `10` 으로 나눈 나머지를 구하는 문제입니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int verificationNum = 0;

      var input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < 5; i++) {
        var num = int.Parse(input[i]);
        verificationNum += (int)Math.Pow(num, 2);
      }

      Console.WriteLine(verificationNum % 10);

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

  int verificationNum = 0;
  for (int i = 0; i < 5; i++) {
    int num; cin >> num;
    verificationNum += pow(num, 2);
  }

  cout << verificationNum % 10 << "\n";

  return 0;
}
  ```
