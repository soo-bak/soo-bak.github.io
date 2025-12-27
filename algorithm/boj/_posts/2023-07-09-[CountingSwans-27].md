---
layout: single
title: "[백준 5292] Counting Swann’s Coins (C#, C++) - soo:bak"
date: "2023-07-09 17:10:00 +0900"
description: 수학, 배수, 구현 등을 주제로 하는 백준 5292번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5292
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 5292, 백준 5292번, BOJ 5292, CountingSwans, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [5292번 - Counting Swann’s Coins](https://www.acmicpc.net/problem/5292)

## 설명
숫자 `n` 이 입력으로 주어질 때,<br>

`1` 부터 `n` 까지의 숫자들에 하여 특정 조건에 따라서 각각 다른 출력을 하는 문제입니다. <br>

조건은 다음과 같습니다. <br>

- `3` 의 배수는 `Dead` 출력<br>
- `5` 의 배수는 `Man` 출력<br>
- `15` 의 배수는 `DeadMan` 출력<br>
- 이외의 숫자는 그대로 출력<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= n; i++) {
        if (i % 15 == 0) Console.WriteLine("DeadMan");
        else if (i % 3 == 0) Console.WriteLine("Dead");
        else if (i % 5 == 0) Console.WriteLine("Man");
        else Console.Write($"{i} ");
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

  int n; cin >> n;

  for (int i = 1; i <= n; ++i) {
    if (i % 15 == 0) cout << "DeadMan\n";
    else if (i % 3 == 0) cout << "Dead\n";
    else if (i % 5 == 0) cout << "Man\n";
    else cout << i << " ";
  }

  return 0;
}
  ```
