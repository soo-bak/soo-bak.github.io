---
layout: single
title: "[백준 26145] 출제비 재분배 (C#, C++) - soo:bak"
date: "2023-05-16 12:18:00 +0900"
description: 수학과 사칙 연산을 주제로 하는 백준 26145번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26145
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 26145, 백준 26145번, BOJ 26145, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26145번 - 출제비 재분배](https://www.acmicpc.net/problem/26145)

## 설명
대회의 운영진들이 얼마나 돈을 분배 받게 될지를 계산하는 문제입니다. <br>

각 출제자가 받는 출제비에서 다른 운영자들에게 나눠주는 금액을 반영하여 계산합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var n = int.Parse(input[0]);
      var m = int.Parse(input[1]);

      var money = new int[n + m + 1];

      input = Console.ReadLine()!.Split(' ');
      for (int i = 1; i <= n; i++)
        money[i] = int.Parse(input[i - 1]);

      for (int i = 1; i <= n; i++) {
        input = Console.ReadLine()!.Split(' ');
        for (int j = 1; j <= n + m; j++) {
          var tmp = int.Parse(input[j - 1]);
          money[i] -= tmp;
          money[j] += tmp;
        }
      }

      for (int i = 1; i <= n + m; i++)
        Console.Write(money[i] + " ");
      Console.WriteLine();

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

  int n, m; cin >> n >> m;

  vector<int> money(n + m + 1, 0);

  for (int i = 1; i <= n; i++)
    cin >> money[i];

  for (int i = 1; i <= n; i++) {
    for (int j = 1; j <= n + m; j++) {
      int tmp; cin >> tmp;
      money[i] -= tmp;
      money[j] += tmp;
    }
  }

  for (int i = 1; i <= n + m; i++)
    cout << money[i] << " ";
  cout << "\n";

  return 0;
}
  ```
