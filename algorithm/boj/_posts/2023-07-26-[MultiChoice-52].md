---
layout: single
title: "[백준 6784] Multiple Choice (C#, C++) - soo:bak"
date: "2023-07-26 23:15:00 +0900"
description: 구현, 수학, 문자열 등을 주제로 하는 백준 6784번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6784
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 6784, 백준 6784번, BOJ 6784, MultiChoice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6784번 - Multiple Choice](https://www.acmicpc.net/problem/6784)

## 설명
객관식 시험의 답안과 학생이 제출한 답안을 비교하여, 얼마나 많은 문제를 맞추었는지 계산하는 문제입니다. <br>

<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);
      List<char> studentAns = new List<char>();
      for (int i = 0; i < n; i++)
        studentAns.Add(Console.ReadLine()![0]);

      List<char> correctAns = new List<char>();
      for (int i = 0; i < n; i++)
        correctAns.Add(Console.ReadLine()![0]);

      int cntCorrect = 0;
      for (int i = 0; i < n; i++) {
        if (studentAns[i] == correctAns[i])
          cntCorrect++;
      }

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
  vector<char> studentAns(n);
  for (int i = 0; i < n; i++)
    cin >> studentAns[i];

  vector<char> correctAns(n);
  for (int i = 0; i < n; i++)
    cin >> correctAns[i];

  int cntCorrect = 0;
  for (int i = 0; i < n; i++) {
    if (studentAns[i] == correctAns[i])
      cntCorrect++;
  }

  cout << cntCorrect << "\n";

  return 0;
}
  ```
