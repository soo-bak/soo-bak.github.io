---
layout: single
title: "[백준 27194] Meeting Near the Fountain (C#, C++) - soo:bak"
date: "2023-03-23 15:36:00 +0900"
description: 시간 계산과 수학을 주제로 하는 백준 27194번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 27194
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
keywords: "백준 27194, 백준 27194번, BOJ 27194, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [27194번 - Meeting Near the Fountain](https://www.acmicpc.net/problem/27194)

## 설명
시간에 대한 간단한 사칙연산 문제입니다. <br>

문제에서 입력으로 주어지는 정보들을 입력 받은 후 <br>

`Kira` 가 공원 입구까지 도달하는 데 걸리는 시간, <br>
`Kira` 가 공원 안에서 만남 장소까지 도달하는 데 걸리는 시간을 계산합니다. <br>

이후, `Kira` 가 출발지부터 만남 장소까지 도달하는 데 걸리는 총 시간을 계산하여, <br>

`Kira` 가 제 시간에 도착할 수 있으면 `0` 을,<br>

그렇지 않다면 `Anna` 가 `Kira` 를 기다려야 하는 시간을 `분` 단위로 <b>반올림</b>하여 출력합니다.<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()?.Split(' ');
      var n = int.Parse(input![0]);
      var T = int.Parse(input![1]);
      var m = int.Parse(Console.ReadLine()!);
      input  = Console.ReadLine()?.Split(' ');
      var x = int.Parse(input![0]);
      var y = int.Parse(input![1]);

      var timeToPark = (double)m / x;
      var timeInPark = (double)(n - m) / y;
      var totalTime = timeToPark + timeInPark;

      var watingTime = (int)Math.Ceiling((totalTime - 60 * T) / 60);

      if (watingTime > 0) Console.WriteLine(watingTime);
      else Console.WriteLine(0);

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

  int n, T, m, x, y; cin >> n >> T >> m >> x >> y;

  double timeToPark = m / (double)x,
         timeInPark = (n - m) / (double)y,
         totalTime = timeToPark + timeInPark;

  int watingTime = ceil((totalTime - 60 * T) / 60);

  if (watingTime > 0) cout << watingTime << "\n";
  else cout << 0 << "\n";

  return 0;
}
  ```
