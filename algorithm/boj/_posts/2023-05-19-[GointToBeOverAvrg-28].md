---
layout: single
title: "[백준 4344] 평균은 넘겠지 (C#, C++) - soo:bak"
date: "2023-05-19 14:13:00 +0900"
description: 평균 계산, 수학, 사칙연산을 주제로 하는 백준 4344번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4344
  - C#
  - C++
  - 알고리즘
keywords: "백준 4344, 백준 4344번, BOJ 4344, GointToBeOverAvrg, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [4344번 - 평균은 넘겠지](https://www.acmicpc.net/problem/4344)

## 설명
입력으로 학생들의 수와 학생들의 점수가 주어졌을 때, 평균이 넘는 학생의 비율을 계산하는 문제입니다. <br>

따라서, 학생들의 <b>평균 점수</b>와 <b>평균을 넘는 학생들의 수</b>를 센 후 그 비율을 계산합니다. <br>

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

        var cntStudent = int.Parse(input[0]);

        var scores = new int[cntStudent];

        double totalScore = 0.0;
        for (int i = 0; i < cntStudent; i++) {
          scores[i] = int.Parse(input[i + 1]);
          totalScore += scores[i];
        }

        var avrg = totalScore / cntStudent;

        int cntOverAvrg = 0;
        foreach(var score in scores)
          if (score > avrg) cntOverAvrg++;

        var ratio = 100.0 * cntOverAvrg / cntStudent;

        Console.WriteLine($"{ratio:F3}%");
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

  for (int c = 0; c < cntCase; c++) {
    int cntStudent; cin >> cntStudent;

    vector<int> scores(cntStudent);

    double totalScore = 0.0;
    for (int i = 0; i < cntStudent; i++) {
      cin >> scores[i];
      totalScore += scores[i];
    }

    double avrg = totalScore / cntStudent;

    int cntOverAvrg = 0;
    for (int score : scores)
      if (score > avrg) cntOverAvrg++;

    double ratio = 100.0 * cntOverAvrg / cntStudent;

    cout.setf(ios::fixed); cout.precision(3);
    cout << ratio << "%\n";

  }

  return 0;
}
  ```
