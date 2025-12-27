---
layout: single
title: "[백준 8387] Dyslexia (C#, C++) - soo:bak"
date: "2023-06-21 05:57:00 +0900"
description: 문자열, 비교, 탐색 등을 주제로 하는 백준 8387번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 8387
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 8387, 백준 8387번, BOJ 8387, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [8387번 - Dyslexia](https://www.acmicpc.net/problem/8387)

## 설명
원본 문자열과 학생이 다시 쓴 문자열이 주어졌을 때, <br>

학생이 다시 쓴 문자열에서 올바르게 받아 쓴 문자의 개수를 출력하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);
      var txtOriginal = Console.ReadLine()!;
      var txtRewritten = Console.ReadLine()!;

      int cntCorrect = 0;
      for (int i = 0; i < n; i++)
        if (txtOriginal[i] == txtRewritten[i])
          cntCorrect++;

      Console.WriteLine(cntCorrect);

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

  string txtOriginal, txtRewritten;
  cin >> txtOriginal >> txtRewritten;

  int cntCorrect = 0;
  for (int i = 0; i < n; i++)
    if (txtOriginal[i] == txtRewritten[i])
      cntCorrect++;

  cout << cntCorrect << "\n";

  return 0;
}
  ```
