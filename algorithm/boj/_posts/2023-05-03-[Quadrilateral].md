---
layout: single
title: "[백준 10188] Quadrilateral (C#, C++) - soo:bak"
date: "2023-05-03 19:03:00 +0900"
description: 수학과 구현을 주제로 하는 백준 10188번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10188
  - C#
  - C++
  - 알고리즘
keywords: "백준 10188, 백준 10188번, BOJ 10188, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [10188번 - Quadrilateral](https://www.acmicpc.net/problem/10188)

## 설명
간단한 수학 문제입니다. <br>

문제의 목표는 입력으로 주어진 조건에 맞는 사각형을 출력하는 것입니다. <br>

사각형은 대문자 `X` 를 사용하여 출력해야 합니다. <br>

입력으로 주어지는 사각형의 `가로 변의 길이` 와 `세로 변의 길이` 에 따라서, 반복문을 이용해 사각형을 출력합니다. <br>

각 사각형은 하나의 빈 줄로 구분해야 된다는 점에 주의합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);;

      for (int i = 0; i < cntCase; i++) {
        var input = Console.ReadLine()!.Split();
        var len = int.Parse(input![0]);
        var width = int.Parse(input![1]);

        for (int j = 0; j < width; j++) {
          for (int k = 0; k < len; k++)
            Console.Write("X");
          Console.WriteLine();
        }

        if (i < cntCase - 1) Console.WriteLine();
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

  int cntCase; cin >> cntCase;

  for (int i = 0; i < cntCase; i++) {
    int len, width; cin >> len >> width;

    for (int j = 0; j < width; j++) {
      for (int k = 0; k < len; k++)
        cout << "X";
      cout << "\n";
    }

    if (i < cntCase - 1) cout << "\n";
  }

  return 0;
}
  ```
