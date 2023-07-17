---
layout: single
title: "[백준 28248] Deliv-e-droid (C#, C++) - soo:bak"
date: "2023-07-18 06:07:00 +0900"
description: 수학, 조건문, 사칙연산 등을 주제로 하는 백준 28248번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [28248번 - Deliv-e-droid](https://www.acmicpc.net/problem/28248)

## 설명
입력으로 주어지는 짐의 개수와 충돌 횟수를 바탕으로, 최종 점수를 계산하여 출력하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var p = int.Parse(Console.ReadLine()!);
      var c = int.Parse(Console.ReadLine()!);

      var score = 50 * p - 10 * c;
      if (p > c) score += 500;

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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int p, c; cin >> p >> c;

  int score = 50 * p - 10 * c;
  if (p > c) score += 500;

  cout << score << "\n";

  return 0;
}
  ```
