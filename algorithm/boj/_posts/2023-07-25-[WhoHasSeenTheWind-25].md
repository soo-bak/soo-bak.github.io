---
layout: single
title: "[백준 6779] Who Has Seen The Wind (C#, C++) - soo:bak"
date: "2023-07-25 23:15:00 +0900"
description: 구현, 수학, 문자열 등을 주제로 하는 백준 6779번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [6779번 - Who Has Seen The Wind](https://www.acmicpc.net/problem/6779)

## 설명
문제의 설명으로 주어진 공식을 활용하여 특정 시간 동안의 고도를 계산한 후,<br>

처음으로 땅에 닿는 시간을 계산하는 문제입니다. <br>

<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var h = int.Parse(Console.ReadLine()!);
      var m = int.Parse(Console.ReadLine()!);

      for (int t = 1; t <= m; t++) {
        double a = -6 * Math.Pow(t, 4) + h * Math.Pow(t, 3) + 2 * Math.Pow(t, 2) + t;

        if (a <= 0) {
          Console.WriteLine($"The balloon first touches ground at hour: {t}");
          return ;
        }
      }
      Console.WriteLine("The balloon does not touch ground in the given time.");

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

  int h, m; cin >> h >> m;

  for (int t = 1; t <= m; t++) {
    double a = -6 * pow(t, 4) + h * pow(t, 3) + 2 * pow(t, 2) + t;

    if (a <= 0) {
      cout << "The balloon first touches ground at hour: " << t << "\n";
      return 0;
    }
  }

  cout << "The balloon does not touch ground in the given time.\n";

  return 0;
}
  ```
