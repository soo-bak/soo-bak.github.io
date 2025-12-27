---
layout: single
title: "[백준 28636] Марафонец (C#, C++) - soo:bak"
date: "2023-09-05 11:46:00 +0900"
description: 수학, 사칙연산, 구현 등을 주제로 하는 백준 28636번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 28636
  - C#
  - C++
  - 알고리즘
keywords: "백준 28636, 백준 28636번, BOJ 28636, BalloonsColor, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [28636번 - Марафонец](https://www.acmicpc.net/problem/28636)

## 설명
`Бараш` 가 달린 총 시간을 구하는 문제입니다. <br>
<br>
`Бараш` 가 달리는 동안 총 `n` 곡의 노래를 들었고, 각 노래의 시간은 `mm:ss` 의 형식으로 주어집니다.<br>
<br>
각 노래의 시간을 모두 더해, 총 달린 시간을 `hh:mm:ss` 형태로 출력합니다. <br>
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

      int totalMinutes = 0, totalSeconds = 0;
      for (int i = 0; i < n; i++) {
          var time = Console.ReadLine()!;
          var minutes = int.Parse(time.Substring(0, 2));
          var seconds = int.Parse(time.Substring(3, 2));

          totalMinutes += minutes;
          totalSeconds += seconds;
      }

      totalMinutes += totalSeconds / 60;
      totalSeconds %= 60;

      int hours = totalMinutes / 60;
      totalMinutes %= 60;

      Console.WriteLine($"{hours:00}:{totalMinutes:00}:{totalSeconds:00}");

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

  int totalMinutes = 0, totalSeconds = 0;
  for (int i = 0; i < n; i++) {
    string time; cin >> time;
    int minutes = stoi(time.substr(0, 2));
    int seconds = stoi(time.substr(3, 2));

    totalMinutes += minutes;
    totalSeconds += seconds;
  }

  totalMinutes += totalSeconds / 60;
  totalSeconds %= 60;

  int hours = totalMinutes / 60;
  totalMinutes %= 60;

  cout << setw(2) << setfill('0') << hours << ":"
       << setw(2) << setfill('0') << totalMinutes << ":"
       << setw(2) << setfill('0') << totalSeconds << "\n";

  return 0;
}
  ```
