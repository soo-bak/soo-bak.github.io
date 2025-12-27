---
layout: single
title: "[백준 6190] Another Cow Number Game (C#, C++) - soo:bak"
date: "2023-06-19 08:33:00 +0900"
description: 구현과 수학, 사칙연산을 주제로 하는 백준 6190번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6190
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 6190, 백준 6190번, BOJ 6190, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6190번 - Another Cow Number Game](https://www.acmicpc.net/problem/6190)

## 설명
문제의 목표는 주어진 규칙에 따라서, 입력으로 주어진 숫자에 대한 총 점수를 구하는 것입니다. <br>

점수를 계산하는 규칙은 다음과 같습니다. <br>

- 홀수의 경우 `3` 을 곱한 후 `1` 을 더한 것이 다음 숫자 <br>
- 짝수의 경우 `2` 로 나눈 것이 다음 숫자 <br>
- 숫자가 `1` 이 될 때 까지 반복하며, 각 반복마다 점수는 `1`씩 증가

입력으로 주어지는 숫자에 대하여, 위 규칙에 따라서 점수를 계산한 후 출력합니다. <br>

점수 계산 과정 중 숫자가 `int` 의 범위를 초과할 수 있음에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = long.Parse(Console.ReadLine()!);

      int score = 0;
      while (n != 1) {
        if (n % 2 == 0) n /= 2;
        else n = 3 * n + 1;
        score++;
      }

      Console.WriteLine(score);

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

  ll n; cin >> n;

  int score = 0;
  while (n != 1) {
    if (n % 2 == 0) n /= 2;
    else n = 3 * n + 1;
    score++;
  }

  cout << score << "\n";

  return 0;
}
  ```
