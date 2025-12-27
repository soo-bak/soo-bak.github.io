---
layout: single
title: "[백준 1085] 직사각형에서 탈출 (C#, C++) - soo:bak"
date: "2023-05-23 09:21:00 +0900"
description: 수학과 사각형의 개념을 주제로 하는 백준 1085번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1085
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
keywords: "백준 1085, 백준 1085번, BOJ 1085, EscapingFromRect, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [1085번 - 직사각형에서 탈출](https://www.acmicpc.net/problem/1085)

## 설명
입력으로 주어지는 위치에서 직사각형의 경계선까지의 최소 거리를 구하는 문제입니다. <br>

직사각형의 경계선까지의 거리는 4가지의 경우가 있습니다. <br>

- 왼쪽으로 이동하는 거리 : `x` <br>
- 오른쪽으로 이동하는 거리 : `w` - `x` <br>
- 아래로 이동하는 거리 : `y` <br>
- 위로 이동하는 거리 : `h` - `y` <br>

<br>
위의 경우 중에서 최솟값으로 계산된 값을 선택하면 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');

      var x = int.Parse(input[0]);
      var y = int.Parse(input[1]);
      var w = int.Parse(input[2]);
      var h = int.Parse(input[3]);

      var minDist = Math.Min(Math.Min(x, y), Math.Min(w - x, h - y));

      Console.WriteLine(minDist);

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

  int x, y, w, h; cin >> x >> y >> w >> h;

  int minDist = min({x, y, w - x, h - y});

  cout << minDist << "\n";

  return 0;
}
  ```
