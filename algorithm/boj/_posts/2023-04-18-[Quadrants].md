---
layout: single
title: "[백준 9772] Quadrants (C#, C++) - soo:bak"
date: "2023-04-18 17:20:00 +0900"
description: 수학과 좌표 판단을 주제로 하는 백준 9772번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [9772번 - Quadrants](https://www.acmicpc.net/problem/9772)

## 설명
주어진 좌표가 어느 사분면에 포함되어 있는지 판별하는 간단한 문제입니다. <br>

마지막으로 주어지는 좌표는 항상 (`0`, `0`) 이며, 이 좌표에 대해서도 결과를 출력해야 한다는 점을 주의해야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var input = Console.ReadLine()?.Split();
        var x = double.Parse(input![0]);
        var y = double.Parse(input![1]);

        if (x == 0 && y == 0) break ;

        if (x == 0 || y == 0) Console.WriteLine("AXIS");
        else if (x > 0 && y > 0) Console.WriteLine("Q1");
        else if (x < 0 && y > 0) Console.WriteLine("Q2");
        else if (x < 0 && y < 0) Console.WriteLine("Q3");
        else Console.WriteLine("Q4");
      }

      Console.WriteLine("AXIS");

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

  double x, y;
  while (true) {
    cin >> x >> y;
    if (x == 0 && y == 0) break ;

    if (x == 0 || y == 0) cout << "AXIS\n";
    else if (x > 0 && y > 0) cout << "Q1\n";
    else if (x < 0 && y > 0) cout << "Q2\n";
    else if (x < 0 && y < 0) cout << "Q3\n";
    else cout << "Q4\n";
  }
  cout << "AXIS\n";

  return 0;
}
  ```
