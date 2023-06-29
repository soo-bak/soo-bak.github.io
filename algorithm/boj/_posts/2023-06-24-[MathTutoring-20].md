---
layout: single
title: "[백준 9299] Math Tutoring (C#, C++) - soo:bak"
date: "2023-06-24 10:10:00 +0900"
description: 수학, 미분, 도함수 등을 주제로 하는 백준 9299번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [9299번 - Math Tutoring](https://www.acmicpc.net/problem/9299)

## 설명
주어진 다항식의 도함수를 구하는 문제입니다. <br>

도함수란 함수 `y = f(x)` 를 미분하여 얻은 함수 `f(x)` 를 말합니다.<br>

도함수를 구하는 규칙에 대해서는 문제에서 간단히 설명되어 있습니다. <br>

규칙에 맞추어 주어진 다항식에 대한 도함수를 구한 후, 도함수 각 항의 계수를 출력합니다. <br>

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
        var input = Console.ReadLine()!.Split(' ');
        var n = int.Parse(input[0]);
        var coef = input.Select(int.Parse).Reverse().ToArray();

        Console.Write($"Case {i}: {n - 1}");

        for (int j = n; j > 0; j--)
          Console.Write($" {coef[j] * j}");
        Console.WriteLine();
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
    int n; cin >> n;
    vector<int> coef(n + 1);

    for (int j = n; j >= 0; j--)
      cin >> coef[j];

    cout << "Case " << i << ": " << n - 1;

    for (int j = n; j > 0; j--)
      cout << " " << coef[j] * j;
    cout << "\n";
  }

  return 0;
}
  ```
