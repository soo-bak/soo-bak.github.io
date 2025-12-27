---
layout: single
title: "[백준 2231] 분해합 (C#, C++) - soo:bak"
date: "2023-05-22 16:58:00 +0900"
description: 자연수의 생성자와 수학을 주제로 하는 백준 2231번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2231
  - C#
  - C++
  - 알고리즘
  - 브루트포스
keywords: "백준 2231, 백준 2231번, BOJ 2231, DecompositionSum, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2231번 - 분해합](https://www.acmicpc.net/problem/2231)

## 설명
입력으로 주어지는 자연수 `n` 의 가장 작은 생성자를 찾는 문제입니다. <br>

어떤 자연 수 `n` 이 있을 때, 그 자연수 `n` 의 분해합은 `n` 과 `n` 을 이루는 각 자리수의 합을 의미합니다. <br>

이 때, 어떤 자연수 `m` 의 분해합이 `n` 인 경우, `m` 을 `n` 의 생성자라고 합니다. <br>

<br>
자연수 `n` 의 최소 생성자는 `1` 일 것입니다.<br>

따라서, `1` 부터 시작하여 `n - 1` 까지의 모든 자연수에 대하여 분해합을 계산하고, 이 값이 `n` 인지 확인합니다. <br>

만약 어떤 자연수의 분해합이 `n` 과 같다면, 해당 자연수는 `n` 의 생성자가 될 것입니다. <br>

생성자를 찾았으면 해당 생성자를 출력하고, 모든 경우에 대해서 생성자를 찾지 못하였다면 `0` 을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static int DecompositionSum(int num) {
      int sum = num;
      while (true) {
        if (num == 0) break ;

        sum += num % 10;
        num /= 10;
      }

      return sum;
    }

    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 1; i < n; i++) {
        if (DecompositionSum(i) == n) {
          Console.WriteLine(i);
          return ;
        }
      }

      Console.WriteLine(0);

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

int decompositionSum(int num) {
  int sum = num;
  while (true) {
    if (num == 0) break ;

    sum += num % 10;
    num /= 10;
  }

  return sum;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;

  for (int i = 1; i < n; i++) {
    if (decompositionSum(i) == n) {
      cout << i << "\n";
      return 0;
    }
  }

  cout << 0 << "\n";

  return 0;
}
  ```
