---
layout: single
title: "[백준 6162] Superlatives (C#, C++) - soo:bak"
date: "2023-07-21 22:43:00 +0900"
description: 구현, 문자열, 수학 등을 주제로 하는 백준 6162번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6162
  - C#
  - C++
  - 알고리즘
keywords: "백준 6162, 백준 6162번, BOJ 6162, Superlatives, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6162번 - Superlatives](https://www.acmicpc.net/problem/6162)

## 설명
예측한 강수량과 실제 강수량을 비교하여 가뭄의 정도를 계산하는 문제입니다. <br>

예측한 강수량이 실제 강수량보다 `5` 배 많을 때, 즉, 실제 강수량이 예측한 강수량의 `1 / 5` 배 일 때마다, <br>

`drought` 앞에 `mega` 접두어를 붙여 출력합니다. <br >

만약, 실제 강수량이 예측한 강수량보다 같거나 더 많다면, 가뭄이 아니므로, `no drought` 를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var k = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= k; i++) {
        Console.WriteLine($"Data Set {i}:");
        var input = Console.ReadLine()!.Split(' ');
        var expected = int.Parse(input[0]);
        var acutal = int.Parse(input[1]);

        int megas = 0;
        while (expected > acutal) {
          acutal *= 5;
          megas++;
        }

        if (megas == 0) {
          Console.Write("no ");
        } else {
          for (int j = 0; j < megas - 1; j++)
            Console.Write("mega ");
        }
        Console.WriteLine("drought\n");
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

  int k; cin >> k;

  for (int i = 1; i <= k; i++) {
    cout << "Data Set " << i << ":\n";

    int expected, actual; cin >> expected >> actual;

    int megas = 0;
    while (expected > actual) {
      actual *= 5;
      megas++;
    }

    if (megas == 0) {
      cout << "no ";
    } else {
      for (int i = 0; i < megas - 1; i++)
        cout << "mega ";
    }
    cout << "drought\n\n";
  }

  return 0;
}
  ```
