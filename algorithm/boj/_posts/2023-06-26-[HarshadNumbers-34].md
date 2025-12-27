---
layout: single
title: "[백준 16861] Harshad Numbers (C#, C++) - soo:bak"
date: "2023-06-26 17:15:00 +0900"
description: 수학, 완전 탐색, 브루트 포스 등을 주제로 하는 백준 16861번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 16861
  - C#
  - C++
  - 알고리즘
keywords: "백준 16861, 백준 16861번, BOJ 16861, HarshadNumbers, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [16861번 - Harshad Numbers](https://www.acmicpc.net/problem/16861)

## 설명
문제의 목표는 주어진 숫자 이상의 최소 <b>하샤드 숫자</b>를 찾는 것입니다.<br>

하샤드 숫자는 각 자리수의 합으로 그 숫자 자체를 나눌 수 있는 숫자를 말합니다. <br>

예를 들어, 숫자 `24` 는 각 자리수의 합이 `2` + `4` = `6` 이며, `24` 를 `6` 으로 나눌 수 있으므로, 하샤드 숫자입니다. <br>

입력으로 주어진 숫자 이상의 최소 하샤드 숫자를 완전 탐색을 활용하여 탐색 후 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      while (true) {
        var strNum = n.ToString();

        int sumDigits = 0;
        foreach (var c in strNum)
          sumDigits += c - '0';

        if (n % sumDigits == 0) {
          Console.WriteLine(n);
          break ;
        }

        n++;
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

  while (true) {
    string strNum = to_string(n);

    int sumDigits = 0;
    for (char c : strNum)
      sumDigits += c - '0';

    if (n % sumDigits == 0) {
      cout << n << "\n";
      break ;
    }

    n++;
  }

  return 0;
}
  ```
