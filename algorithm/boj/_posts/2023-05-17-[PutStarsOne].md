---
layout: single
title: "[백준 2438] 별 찍기 - 1 (C#, C++) - soo:bak"
date: "2023-05-17 12:46:00 +0900"
description: 반복문과 구현을 주제로 하는 백준 2438번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [2438번 - 별 찍기 - 1](https://www.acmicpc.net/problem/2438)

## 설명
`1` 번째 줄부터 `n` 번째 줄까지, 각 줄에 문자 `*` 을 출력하는 문제입니다. <br>

각 줄에 출력해야하는 `*` 의 개수는 줄의 행 번호와 일치합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        for (int j = 0; j < i + 1; j++)
          Console.Write("*");
        Console.WriteLine();
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

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < i + 1; j++)
      cout << "*";
    cout << "\n";
  }

  return 0;
}
  ```
