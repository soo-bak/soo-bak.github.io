---
layout: single
title: "[백준 10951] A+B - 4 (C#, C++) - soo:bak"
date: "2023-05-10 12:11:00 +0900"
description: 수학과 사칙연산과 반복문을 주제로 하는 백준 10951번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10951
  - C#
  - C++
  - 알고리즘
  - 구현
  - arithmetic
  - 수학
keywords: "백준 10951, 백준 10951번, BOJ 10951, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [10951번 - A+B - 4](https://www.acmicpc.net/problem/10951)

## 설명
기본적인 사칙 연산과 반복문을 사용하는 문제입니다. <br>

다만, 입력의 끝인 `EOF` 에 관한 처리를 해주어야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      string? input;
      while (true) {
        input = Console.ReadLine();
        if (input == null) break ;

        var tokens = input.Split(' ');
        var a = int.Parse(tokens[0]);
        var b = int.Parse(tokens[1]);

        Console.WriteLine($"{a + b}");
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

  while (true) {
    int a, b; cin >> a >> b;
    if(cin.eof()) break;

    cout << a + b << "\n";
  }

  return 0;
}
  ```
