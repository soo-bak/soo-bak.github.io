---
layout: single
title: "[백준 10871] X보다 작은 수 (C#, C++) - soo:bak"
date: "2023-05-17 15:00:00 +0900"
description: 비교를 주제로 하는 백준 10871번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10871
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 10871, 백준 10871번, BOJ 10871, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [10871번 - X보다 작은 수](https://www.acmicpc.net/problem/10871)

## 설명
`n` 개의 정수들이 입력으로 주어졌을 때, `x` 보다 작은 수를 출력하는 문제입니다. <br>

반복문과 조건문의 활용에 대한 간단한 문제입니다. <br>

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
      var x = int.Parse(input[1]);

      input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < n; i++) {
        var ele = int.Parse(input[i]);
        if (ele < x) Console.Write($"{ele} ");
      }
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

  int n, x; cin >> n >> x;

  for (int i = 0; i < n; i++) {
    int ele; cin >> ele;
    if (ele < x) cout << ele << " ";
  }
  cout << "\n";

  return 0;
}
  ```
