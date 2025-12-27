---
layout: single
title: "[백준 2775] 부녀회장이 될테야 (C#, C++) - soo:bak"
date: "2023-05-23 08:08:00 +0900"
description: 수학과 일반항 찾기, 계산을 주제로 하는 백준 2775번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2775
  - C#
  - C++
  - 알고리즘
keywords: "백준 2775, 백준 2775번, BOJ 2775, GoingToBeHead, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2775번 - 부녀회장이 될테야](https://www.acmicpc.net/problem/2775)

## 설명
반상회를 주최하기 위해 각 층별, 호별로 사람의 수를 계산하는 문제입니다. <br>

문제의 조건에 따르면, 각 호의 사람 수는 아래층의 같은 호의 사람수와 그 이전 호까지의 사람 수의 합과 같습니다. <br>

따라서, `0` 층의 각 호에는 호수와 같은 수의 사람이 살고 있습니다. <br>

이후 `1` 층부터 시작하여, 각 층의 각 호에 사는 사람의 수를 계산합니다. <br>

이 때, 각 호에 사는 사람의 수는 바로 아래층의 같은 호 사람 수와 그 이전 호까지 사는 모든 사람 수의 합입니다. <br>

반복문을 활용하여 위와 같은 계산을 진행하면, 주어진 층과 호에 살고 있는 사람의 수를 계산할 수 있습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      const int MAX = 15;

      var apt = new int[MAX, MAX];

      for (int i = 0; i < MAX; i++) {
        apt[i, 1] = 1;
        apt[0, i] = i;
      }

      for (int i = 1; i < MAX; i++) {
        for (int j = 2; j < MAX; j++)
          apt[i, j] = apt[i - 1, j] + apt[i, j - 1];
      }

      var cntCase = int.Parse(Console.ReadLine()!);
      for (int c = 0; c < cntCase; c++) {
        var floor = int.Parse(Console.ReadLine()!);
        var numRoom = int.Parse(Console.ReadLine()!);

        Console.WriteLine($"{apt[floor, numRoom]}");
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

#define MAX 15

using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  vector<vi> apt(MAX, vi(MAX, 0));

  for (int i = 0; i < MAX; i++) {
    apt[i][1] = 1;
    apt[0][i] = i;
  }

  for (int i = 1; i < MAX; i++) {
    for (int j = 2; j < MAX; j++)
      apt[i][j] = apt[i - 1][j] + apt[i][j - 1];
  }

  int cntCase; cin >> cntCase;
  for (int c = 0; c < cntCase; c++) {
    int floor, numRoom; cin >> floor >> numRoom;
    cout << apt[floor][numRoom] << "\n";
  }

  return 0;
}
  ```
