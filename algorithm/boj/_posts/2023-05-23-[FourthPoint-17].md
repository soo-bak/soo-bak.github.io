---
layout: single
title: "[백준 3009] 네 번째 점 (C#, C++) - soo:bak"
date: "2023-05-23 09:08:00 +0900"
description: 수학과 좌표 평면을 주제로 하는 백준 3009번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 3009
  - C#
  - C++
  - 알고리즘
  - 구현
  - 기하학
keywords: "백준 3009, 백준 3009번, BOJ 3009, FourthPoint, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [3009번 - 네 번째 점](https://www.acmicpc.net/problem/3009)

## 설명
입력으로 주어지는 세 점을 이용하여 축에 평행한 직사각형을 만들 때, 필요한 네 번째 점을 찾는 문제입니다. <br>

축에 평행한 직사각형을 만들기 위해서는 네 점의 `x` 좌표와 `y` 좌표 각각이 `2` 개 씩 동일해야 합니다. <br>

즉, 각각의 `x` 좌표와 `y` 좌표를 확인하여, 한 번만 등장하는 좌표가 네 번째 점의 좌표가 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var x = new int[3];
      var y = new int[3];
      for (int i = 0; i < 3; i++) {
        var input = Console.ReadLine()!.Split(' ');
        x[i] = int.Parse(input[0]);
        y[i] = int.Parse(input[1]);
      }

      int fourthPointX, fourthPointY;

      if (x[0] == x[1]) fourthPointX = x[2];
      else if (x[0] == x[2]) fourthPointX = x[1];
      else fourthPointX = x[0];

      if (y[0] == y[1]) fourthPointY = y[2];
      else if (y[0] == y[2]) fourthPointY = y[1];
      else fourthPointY = y[0];

      Console.WriteLine($"{fourthPointX} {fourthPointY}");

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

  vector<int> x(3), y(3);
  for (int i = 0; i < 3; i++)
    cin >> x[i] >> y[i];

  int fourthPointX, fourthPointY;

  if (x[0] == x[1]) fourthPointX = x[2];
  else if (x[0] == x[2]) fourthPointX = x[1];
  else fourthPointX = x[0];

  if (y[0] == y[1]) fourthPointY = y[2];
  else if (y[0] == y[2]) fourthPointY = y[1];
  else fourthPointY = y[0];

  cout << fourthPointX << " " << fourthPointY << "\n";

  return 0;
}
  ```
