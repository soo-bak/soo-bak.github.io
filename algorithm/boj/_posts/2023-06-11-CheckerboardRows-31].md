---
layout: single
title: "[백준 5246] Checkerboard Rows (C#, C++) - soo:bak"
date: "2023-06-11 20:11:00 +0900"
description: 최댓값 찾기를 주제로 하는 백준 5246번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [5246번 - Checkerboard Rows](https://www.acmicpc.net/problem/5246)

## 설명
`8 x 8` 사이즈의 체커보드에서 한 행에 가장 많이 놓인 체커 피스의 개수를 찾는 문제입니다. <br>

입력으로 피스의 행과 열이 주어질 때 마다 각 행에 대해서 체크를 한 후, 모든 행을 순회하며 가장 높은 값을 탐색하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntBoard = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < cntBoard; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var cntPieces = int.Parse(input[0]);

        var rows = new int[8];
        for (int j = 1; j <= cntPieces; j++) {
          var x = int.Parse(input[2 * j - 1]);
          var y = int.Parse(input[2 * j]);

          rows[y - 1]++;
        }

        var maxPieces = rows.Max();
        Console.WriteLine(maxPieces);
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

  int cntBoard; cin >> cntBoard;

  for (int i = 0; i < cntBoard; i++) {
    int cntPieces; cin >> cntPieces;
    vector<int> rows(8, 0);
    for (int j = 0; j < cntPieces; j++) {
      int x, y; cin >> x >> y;

      rows[y - 1]++;
    }

    int maxPieces = *max_element(rows.begin(), rows.end());
    cout << maxPieces << "\n";
  }

  return 0;
}
  ```
