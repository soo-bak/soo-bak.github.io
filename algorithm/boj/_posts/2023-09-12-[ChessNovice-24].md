---
layout: single
title: "[백준 29725] 체스 초보 브실이 (C#, C++) - soo:bak"
date: "2023-09-12 05:19:00 +0900"
description: 구현 을 주제로 하는 백준 29725번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [29725번 - 체스 초보 브실이](https://www.acmicpc.net/problem/29725)

## 설명
문제의 목표는 두 시간(오늘의 먹이 주는 시간, 내일의 먹이 주는 시간)이 주어졌을 때,<br>
<br>
두 시간 사이에 얼마나 시간이 지났는지 계산하는 것입니다. <br>
<br>
`"HH:MM"` 형식으로 주어지는 각 시간을 `60` * `HH` + `MM` 형식으로 변환한 후, <br>
<br>
두 시간을 분 단위로 뺄셈하여 시간 차이를 구합니다. <br>
<br>
오늘의 시간이 내일의 시간보다 큰 경우, 하루가 지난 것으로 간주해야 함에 주의합니다.<br>
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
