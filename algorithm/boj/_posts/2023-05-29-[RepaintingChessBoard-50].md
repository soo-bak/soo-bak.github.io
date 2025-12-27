---
layout: single
title: "[백준 1018] 체스판 다시 칠하기 (C#, C++) - soo:bak"
date: "2023-05-29 08:43:00 +0900"
description: 수학과 그리디 알고리즘, 시뮬레이션 등을 주제로 하는 백준 1018번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1018
  - C#
  - C++
  - 알고리즘
keywords: "백준 1018, 백준 1018번, BOJ 1018, RepaintingChessBoard, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [1018번 - 체스판 다시 칠하기](https://www.acmicpc.net/problem/1018)

## 설명
`8 x 8` 크기의 체스판으로 자를 수 있는 판이 주어졌을 때,<br>

체스판 각 칸의 색깔이 번갈아가면서 나오도록 만들기 위해 다시 칠해야하는 칸의 최소 개수를 구하는 문제입니다. <br>

문제 해결을 위해서 체스판의 왼쪽 위 칸을 기준으로 두 가지 경우를 고려합니다. <br>

- 체스판의 왼쪽 위칸이 흰색인 경우 (`WBWBWBWB...`)<br>
- 체스판의 왼쪽 위칸이 검은색인 경우 (`BWBWBWBW...`)<br>

이 두 가지 경우에 대해 가능한 모든 `8 x 8` 크기의 체스판을 고려하여, 각 경우마다 다시 칠해야 하는 칸의 개수를 세고, <br>

이 중 최솟값을 출력합니다. <br>

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

      var board = new string[n];
      for (int i = 0; i < n; i++)
        board[i] = Console.ReadLine()!;

      int res = 64;
      for (int i = 0; i <= n - 8; i++) {
        for (int j = 0; j <= m - 8; j++) {
          int case1 = 0, case2 = 0;
          for (int k = i; k < i + 8; k++) {
            for (int l = j; l < j + 8; l++) {
              if ((k + l) % 2 == 0) {
                if (board[k][l] != 'W') case1++;
                if (board[k][l] != 'B') case2++;
              } else {
                if (board[k][l] != 'B') case1++;
                if (board[k][l] != 'W') case2++;
              }
            }
          }
          res = Math.Min(res, Math.Min(case1, case2));
        }
      }

      Console.WriteLine(res);

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

  vector<string> board(n);
  for (int i = 0; i < n; i++)
    cin >> board[i];

  int res = 64;
  for (int i = 0; i <= n - 8; i++) {
    for (int j = 0; j <= m - 8; j++) {
      int case1 = 0, case2 = 0;
      for (int k = i; k < i + 8; k++) {
        for (int l = j; l < j + 8; l++) {
          if ((k + l) % 2 == 0) {
            if (board[k][l] != 'W') case1++;
            if (board[k][l] != 'B') case2++;
          } else {
            if (board[k][l] != 'B') case1++;
            if (board[k][l] != 'W') case2++;
          }
        }
      }
      res = min(res, min(case1, case2));
    }
  }

  cout << res << "\n";

  return 0;
}
  ```
