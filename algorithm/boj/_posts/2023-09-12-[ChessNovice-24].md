---
layout: single
title: "[백준 29725] 체스 초보 브실이 (C#, C++) - soo:bak"
date: "2023-09-12 05:19:00 +0900"
description: 구현 을 주제로 하는 백준 29725번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 29725
  - C#
  - C++
  - 알고리즘
keywords: "백준 29725, 백준 29725번, BOJ 29725, ChessNovice, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [29725번 - 체스 초보 브실이](https://www.acmicpc.net/problem/29725)

## 설명
`8 × 8` 체스판 위에 놓인 기물의 상태가 주어졌을 때,

**백의 기물 점수 총합에서 흑의 기물 점수 총합을 뺀 값**을 계산하는 문제입니다.

기물별 점수는 다음과 같습니다:
- 킹: `0`점
- 폰: `1`점
- 나이트, 비숍: `3`점
- 룩: `5`점
- 퀸: `9`점

<br>
백은 대문자(`K`, `P`, `N`, `B`, `R`, `Q`), 흑은 소문자(`k`, `p`, `n`, `b`, `r`, `q`)로 주어지며,<br>
빈칸은 마침표(`.`)로 주어집니다.

<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {
      var pieces = new char[] {'K', 'P', 'N', 'B', 'R', 'Q',
                               'k', 'p', 'n', 'b', 'r', 'q'};
      var scores = new int[] {0, 1, 3, 3, 5, 9,
                              0, -1, -3, -3, -5, -9};

      var board = new string[8];
      for (int i = 0; i < 8; i++)
        board[i] = Console.ReadLine()!;

      int totalScore = 0;
      for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 8; j++) {
          for (int k = 0; k < 12; k++) {``
            if (board[i][j] == pieces[k]) {
              totalScore += scores[k];
              break;
            }
          }
        }
      }

      Console.WriteLine(totalScore);

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

  char pieces[] = {'K', 'P', 'N', 'B', 'R', 'Q',
                 'k', 'p', 'n', 'b', 'r', 'q'};
  int scores[] = {0, 1, 3, 3, 5, 9, 0, -1, -3, -3, -5, -9};

  char board[8][9];
  for (int i = 0; i < 8; i++)
    cin >> board[i];

  int totalScore = 0;
  for (int i = 0; i < 8; i++) {
    for (int j = 0; j < 8; j++) {
      for (int k = 0; k < 12; k++) {
        if (board[i][j] == pieces[k]) {
          totalScore += scores[k];
          break ;
        }
      }
    }
  }

  cout << totalScore << "\n";

  return 0;
}
  ```
