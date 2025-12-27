---
layout: single
title: "[백준 31669] 특별한 학교 탈출 (C#, C++) - soo:bak"
date: "2024-04-24 00:02:00 +0900"
description: 구현, 문자열, 파싱 등을 주제로 하는 백준 31669번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 31669
  - C#
  - C++
  - 알고리즘
keywords: "백준 31669, 백준 31669번, BOJ 31669, EscapeSpecialSchool, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [31669번 - 특별한 학교 탈출](https://www.acmicpc.net/problem/31669)

## 설명
학교에서 탈출하려는 학생들이 선생님에게 들키지 않고 탈출할 수 있는 가장 빠른 시각을 찾는 문제입니다.<br>
<br>
각 선생님의 순찰 스케줄이 주어지고, 학생들은 모든 선생님이 순찰하지 않는 시각에 탈출해야 합니다.<br>
<br>

입력으로 주어지는 문자열에서 `'O'` 는 해당 시간에 선생님이 순찰을 한다는 것을, `'X'` 는 해당 시간에 선생님이 순찰을 하지 않는다는 것을 의미합니다.<br>
<br>

<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var reader = new System.IO.StreamReader(Console.OpenStandardInput());
      Console.SetIn(reader);

      var inputs = Console.ReadLine()!.Split();
      var n = int.Parse(inputs[0]);
      var m = int.Parse(inputs[1]);

      var schedules = Enumerable.Range(0, n)
        .Select(_ => Console.ReadLine())
        .ToList();

      var escapeColumn = Enumerable.Range(0, m)
        .FirstOrDefault(i => schedules
          .All(sch => sch![i] != 'O'), -1);

      if (escapeColumn == -1)
        Console.WriteLine("ESCAPE FAILED");
      else Console.WriteLine(escapeColumn + 1);

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

typedef vector<string> vs;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;

  vs schedules(n);
  for (int i = 0; i < n; i++)
    cin >> schedules[i];

  for (int j = 0; j < m; j++) {
    bool enableEscape = true;
    for (int i = 0; i < n; i++) {
      if (schedules[i][j] == 'O') {
        enableEscape = false;
        break ;
      }
    }

    if (enableEscape) {
      cout << j + 1 << "\n";
      return 0;
    }
  }

  cout << "ESCAPE FAILED\n";

  return 0;
}
  ```
