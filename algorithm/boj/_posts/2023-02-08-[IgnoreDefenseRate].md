---
layout: single
title: "[백준 25756] 방어율 무시 계산하기 (C#, C++) - soo:bak"
date: "2023-02-08 06:55:00 +0900"
description: 사칙 연산과 수학을 주제로한 백준 25756번 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 25756
  - C#
  - C++
  - 알고리즘
keywords: "백준 25756, 백준 25756번, BOJ 25756, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [25756번 - 방어율 무시 계산하기](https://www.acmicpc.net/problem/25756)

## 설명
  간단한 사칙연산 문제입니다.<br>

  입력으로 주어지는 정수들을 파싱한 후, <br>
  문제에 주어진 '방어율 무시 수치의 계산 식` 을 이용하여 결과값을 출력합니다.

  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int.TryParse(Console.ReadLine(), out int n);

      string[]? input = Console.ReadLine()?.Split();

      double defenseIgRate = 0;
      for (int i = 0; i < n; i++) {
        int.TryParse(input?[i], out int effPotion);
        defenseIgRate = (effPotion + defenseIgRate) - ((defenseIgRate * effPotion) / 100);

        Console.WriteLine("{0:F6}", defenseIgRate);

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

  int n; cin >> n;

  double defenseIgRate = 0;
  for (int i = 0; i < n; i++) {
    int effPotion; cin >> effPotion;
    defenseIgRate = (effPotion + defenseIgRate) - ((defenseIgRate * effPotion) / 100);

    cout.setf(ios::fixed); cout.precision(6);
    cout << defenseIgRate << "\n";
  }

  return 0;
}
  ```
