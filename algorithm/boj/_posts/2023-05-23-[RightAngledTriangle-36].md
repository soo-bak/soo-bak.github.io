---
layout: single
title: "[백준 4153] 직각삼각형 (C#, C++) - soo:bak"
date: "2023-05-23 09:28:00 +0900"
description: 수학과 피타고라스의 정리, 삼각형을 주제로 하는 백준 4153번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4153
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
  - pythagoras
keywords: "백준 4153, 백준 4153번, BOJ 4153, RightAngledTriangle, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [4153번 - 직각삼각형](https://www.acmicpc.net/problem/4153)

## 설명
입력으로 주어지는 세 변의 길이를 바탕으로 삼각형이 `직각 삼각형` 인지 아닌지를 판별하는 문제입니다. <br>

`피타고라스의 정리` 를 사용하여 직각삼각형을 판별할 수 있습니다. <br>

세 변의 길이를 `a` , `b` , `c` (`c` 가 가장 긴 변) 라고 가정했을 때, <br>

<b>c<sup>2</sup> = a<sup>2</sup> + b<sup>2</sup></b> 가 성립하면 직각삼각형입니다. <br>

따라서, 세 변의 길이를 입력으로 받아 정렬한 뒤, 가장 긴 변을 바탕으로 피타고라스의 정리가 성립하는지 확인하면 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var sides = Console.ReadLine()!.Split().Select(int.Parse).ToList();

        if (sides[0] == 0 && sides[1] == 0 && sides[2] == 0) break ;

        sides.Sort();

        if (sides[2] * sides[2] == sides[0] * sides[0] + sides[1] * sides[1])
          Console.WriteLine("right");
        else Console.WriteLine("wrong");
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

  vector<int> sides(3);

  while (true) {
    cin >> sides[0] >> sides[1] >> sides[2];

    if (sides[0] == 0 && sides[1] == 0 && sides[2] == 0)
      break;

    sort(sides.begin(), sides.end());

    if (sides[2] * sides[2] == sides[0] * sides[0] + sides[1] * sides[1])
      cout << "right\n";
    else cout << "wrong\n";
  }

  return 0;
}
  ```
