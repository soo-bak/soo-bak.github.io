---
layout: single
title: "[백준 5235] Even Sum More Than Odd Sum (C#, C++) - soo:bak"
date: "2023-05-18 07:37:00 +0900"
description: 수학과 짝수 홀수 판별을 주제로 하는 백준 5235번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5235
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 5235, 백준 5235번, BOJ 5235, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [5235번 - Even Sum More Than Odd Sum](https://www.acmicpc.net/problem/5235)

## 설명
문제의 목표는 입력으로 주어지는 수열들에서 짝수의 합과 홀수의 합을 비교하는 것입니다. <br>

먼저, 테스트 케이스의 개수를 입력받은 후, 각 테스트 케이스에 대해 수열의 크기와 수열을 입력 받습니다. <br>

이후, 짝수들의 합과 홀수들의 합을 계산한 후, <br>

짝수의 합이 홀수의 합보다 큰 경우 `EVEN` 을, 홀수의 합이 짝수의 합보다 큰 경우 `ODD` 를, 두 합이 동일한 경우 `TIE`를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int c = 0; c < cntCase; c++) {
        var input = Console.ReadLine()!.Split(' ');
        var n = int.Parse(input[0]);

        int sumEven = 0, sumOdd = 0;

        for (int i = 0; i < n; i++) {
          var num = int.Parse(input[i + 1]);

          if (num % 2 == 0) sumEven += num;
          else sumOdd += num;
        }

        if (sumEven > sumOdd) Console.WriteLine("EVEN");
        else if (sumEven < sumOdd) Console.WriteLine("ODD");
        else Console.WriteLine("TIE");
      }

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

  int cntCase; cin >> cntCase;

  for (int t = 0; t < cntCase; t++) {
    int n; cin >> n;

    int sumEven = 0, sumOdd = 0;

    for (int i = 0; i < n; i++) {
      int num; cin >> num;

      if (num % 2 == 0) sumEven += num;
      else sumOdd += num;
    }

    if (sumEven > sumOdd) cout << "EVEN\n";
    else if (sumEven < sumOdd) cout << "ODD\n";
    else cout << "TIE\n";
  }

  return 0;
}
  ```
