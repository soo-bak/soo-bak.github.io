---
layout: single
title: "[백준 9498] 시험 성적 (C#, C++) - soo:bak"
date: "2023-05-12 09:03:00 +0900"
description: 수학과 조건문의 활용을 주제로 하는 백준 9498번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9498
  - C#
  - C++
  - 알고리즘
keywords: "백준 9498, 백준 9498번, BOJ 9498, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9498번 - 시험 성적](https://www.acmicpc.net/problem/9498)

## 설명
입력으로 주어지는 점수를 문제의 조건에 따라서 분기 후 성적을 출력하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var score = int.Parse(Console.ReadLine()!);

      if (score >= 90) Console.WriteLine("A");
      else if (score >= 80) Console.WriteLine("B");
      else if (score >= 70) Console.WriteLine("C");
      else if (score >= 60) Console.WriteLine("D");
      else Console.WriteLine("F");

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

  int score; cin >> score;

  if (score >= 90) cout << "A\n";
  else if (score >= 80) cout << "B\n";
  else if (score >= 70) cout << "C\n";
  else if (score >= 60) cout << "D\n";
  else cout << "F\n";

  return 0;
}
  ```
