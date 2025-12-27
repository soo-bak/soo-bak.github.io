---
layout: single
title: "[백준 6856] Roll the Dice (C#, C++) - soo:bak"
date: "2023-08-02 08:30:00 +0900"
description: 수학, 경우의 수, 완전 탐색(브루트 포스), 구현 등을 주제로 하는 백준 6856번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6856
  - C#
  - C++
  - 알고리즘
  - 브루트포스
keywords: "백준 6856, 백준 6856번, BOJ 6856, RollTheDice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6856번 - Roll the Dice](https://www.acmicpc.net/problem/6856)

## 설명
주어진 두 주사위를 굴려서 합이 `10` 이 되는 경우의 수를 찾는 문제입니다. <br>

이 때, 하나의 주사위는 `m` 개의 면을 가지고 있고, 다른 하나의 주사위는 `n` 개의 면을 가지고 있습니다. <br>

따라서, 각 주사위를 독립적으로 고려하여 가능한 모든 값에 대하여 그 값이 `10` 과 얼마나 차이가 나는지 확인하면 됩니다. <br>

예를 들어, 첫 번째 주사위가 `2` 를 나타내면 두번 째 주사위는 `8` 을 나타내야 합이 `10` 이 됩니다. <br>

그런 다음, 두 번째 주사위가 필요한 값을 나타낼 수 있는 면의 수를 가지고 있는지 확인하면 됩니다. <br>

위 과정을 두 주사위의 모든 가능한 값에 대하여 반복하면, 합이 `10` 이 되는 모든 방법을 찾을 수 있습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var m = int.Parse(Console.ReadLine()!);
      var n = int.Parse(Console.ReadLine()!);

      int ways = 0;
      for (int i = 1; i <= m; i++) {
        if (10 - i >= 1 && 10 - i <= n)
          ways++;
      }

      if (ways == 1)
        Console.WriteLine("There is 1 way to get the sum 10.");
      else
        Console.WriteLine($"There are {ways} ways to get the sum 10.");

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

  int m, n; cin >> m >> n;

  int ways = 0;
  for (int i = 1; i <= m; i++) {
    if (10 - i >= 1 && 10 - i <= n)
      ways++;
  }

  if (ways == 1) cout << "There is 1 way to get the sum 10." << "\n";
  else cout << "There are " << ways << " ways to get the sum 10." << "\n";

  return 0;
}
  ```
