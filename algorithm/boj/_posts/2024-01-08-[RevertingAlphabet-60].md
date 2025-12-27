---
layout: single
title: "[백준 30032] 알파벳 뒤집기 (C#, C++) - soo:bak"
date: "2024-01-08 08:52:00 +0900"
description: 구현, 문자열 등을 주제로 하는 백준 30032번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 30032
  - C#
  - C++
  - 알고리즘
keywords: "백준 30032, 백준 30032번, BOJ 30032, RevertingAlphabet, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [30032번 - 알파벳 뒤집기](https://www.acmicpc.net/problem/30032)

## 설명
알파벳 소문자 `d`, `b`, `q`, `p` 를 주어진 방향으로 뒤집는 문제입니다.<br>
<br>
각 알파벳은 `상하` 또는 `좌우` 로 뒤집을 때 다른 문자로 변환됩니다.<br>
<br>
주어진 `n` * `n` 크기의 격자에서, 각 문자를 주어진 방향으로 뒤집어 결과를 출력합니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    static char Flip(char ch, int d) {
      if (d == 1) {
        switch (ch) {
          case 'd' : return 'q';
          case 'q' : return 'd';
          case 'b' : return 'p';
          case 'p' : return 'b';
          default : return ch;
        }
      } else {
        switch (ch) {
          case 'd' : return 'b';
          case 'b' : return 'd';
          case 'q' : return 'p';
          case 'p' : return 'q';
          default : return ch;
        }
      }
    }

    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ').Select(int.Parse).ToArray();
      int n = input[0], d = input[1];

      List<string> grid  = new List<string>();
      for (int i = 0; i < n; i++)
        grid.Add(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        char[] row = grid[i].ToCharArray();
        for (int j = 0; j < n; j++)
          row[j] = Flip(row[j], d);

        grid[i] = new string(row);
      }

      foreach (string row in grid)
        Console.WriteLine(row);

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

char flip(char ch, int d) {
  if (d == 1) {
    if (ch == 'd') return 'q';
    if (ch == 'q') return 'd';
    if (ch == 'b') return 'p';
    if (ch == 'p') return 'b';
  } else {
    if (ch == 'd') return 'b';
    if (ch == 'b') return 'd';
    if (ch == 'q') return 'p';
    if (ch == 'p') return 'q';
  }

  return ch;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, d; cin >> n >> d;

  vector<string> grid(n);
  for (int i = 0; i < n; i++)
    cin >> grid[i];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++)
      grid[i][j] = flip(grid[i][j], d);
  }

  for (int i = 0; i < n; i++)
    cout << grid[i] << "\n";

  return 0;
}
  ```
