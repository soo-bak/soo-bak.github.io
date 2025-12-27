---
layout: single
title: "[백준 9723] Right Triangle (C#, C++) - soo:bak"
date: "2023-06-28 13:53:00 +0900"
description: 수학, 피타고라스의 정리, 직각 삼각형 판별 등을 주제로 하는 백준 9723번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 9723
  - C#
  - C++
  - 알고리즘
keywords: "백준 9723, 백준 9723번, BOJ 9723, RightTriangle, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [9723번 - Right Triangle](https://www.acmicpc.net/problem/9723)

## 설명
입력으로 주어지는 삼각형의 세 변의 길이를 바탕으로, 해당 삼각형이 직각삼각형인지 아닌지를 판별하는 문제입니다. <br>

직각삼각형의 세 변은 피타고라스의 정리(`a`<sup>2</sup> + `b`<sup>2</sup> = `c`<sup>2</sup>, `c` 는 빗변)를 만족해야 합니다. <br>

따라서, 주어진 세 변의 길이 중 가장 긴 변을 찾아, 이를 빗변으로 설정하고 나머지 두 변에 대해서 피타고라스의 정리를 만족하는지 확인하면 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var t = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= t; i++) {
        var sides = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();

        Array.Sort(sides);

        Console.Write($"Case #{i}: ");

        if (Math.Pow(sides[0], 2) + Math.Pow(sides[1], 2) == Math.Pow(sides[2], 2))
          Console.WriteLine("YES");
        else Console.WriteLine("NO");
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

  int t; cin >> t;

  for (int i = 1; i <= t; i++) {
    int sides[3];
    cin >> sides[0] >> sides[1] >> sides[2];

    sort(sides, sides + 3);

    cout << "Case #" << i << ": ";

    if (pow(sides[0], 2) + pow(sides[1], 2) == pow(sides[2], 2))
      cout << "YES\n";
    else cout << "NO\n";
  }

  return 0;
}
  ```
