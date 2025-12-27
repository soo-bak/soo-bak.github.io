---
layout: single
title: "[백준 28289] 과 조사하기 (C#, C++) - soo:bak"
date: "2023-07-11 22:35:00 +0900"
description: 수학, 구현, 조건 분기 등을 주제로 하는 백준 28289번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 28289
  - C#
  - C++
  - 알고리즘
keywords: "백준 28289, 백준 28289번, BOJ 28289, SearchingMajor, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [28289번 - 과 조사하기](https://www.acmicpc.net/problem/28289)

## 설명
문제의 목표는 동아리의 학생들이 어떤 과에 속해 있는지를 확인하고, <br>

각 과별 학생 수와 아무런 과에도 속하지 않은 학생 수를 세는 것입니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var p = int.Parse(Console.ReadLine()!);

      int software = 0, embedded = 0, ai = 0, noDept = 0;
      for (int i = 0; i < p; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var grade = int.Parse(input[0]);
        var classNum = int.Parse(input[1]);

        if (grade == 1) noDept++;
        else if (classNum <= 2) software++;
        else if (classNum == 3) embedded++;
        else if (classNum == 4) ai++;
      }

      Console.WriteLine($"{software}\n{embedded}\n{ai}\n{noDept}");

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

  int p; cin >> p;

  int software = 0, embedded = 0, ai = 0, noDept = 0;
  for(int i = 0; i < p; i++) {
    int grade, classNum, num;
    cin >> grade >> classNum >> num;

    if (grade == 1) noDept++;
    else if (classNum <= 2) software++;
    else if (classNum == 3) embedded++;
    else if (classNum == 4) ai++;
  }

  cout << software << "\n" << embedded << "\n" << ai << "\n" << noDept << "\n";

  return 0;
}
  ```
