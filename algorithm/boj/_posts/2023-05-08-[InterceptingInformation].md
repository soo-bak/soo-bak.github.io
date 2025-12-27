---
layout: single
title: "[백준 26209] Intercepting Information (C#, C++) - soo:bak"
date: "2023-05-08 22:28:00 +0900"
description: 비트에 대한 이해와 시뮬레이션을 주제로 하는 백준 26209번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26209
  - C#
  - C++
  - 알고리즘
keywords: "백준 26209, 백준 26209번, BOJ 26209, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26209번 - Intercepting Information](https://www.acmicpc.net/problem/26209)

## 설명
입력으로 주어지는 비트 목록을 기반으로, 기계가 읽어들인 비트가 모두 성공적으로 읽혔는지 확인하는 문제입니다. <br>

`8` 개의 정수를 입력받은 후, 그 중 `9` 가 있다면 비트를 읽는 데에 실패한 것이고, 그렇지 않다면 성공한 것입니다. <br>

실패하였다면 `F` 를, 성공하였다면 `S` 를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      bool isFail = false;
      var input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < 8; i++) {
        var bit = int.Parse(input![i]);

        if (bit == 9) isFail = true;
      }

      if (isFail) Console.WriteLine("F");
      else Console.WriteLine("S");

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

  bool isFail = false;
  for (int i = 0; i < 8; i++) {
    int bit; cin >> bit;

    if (bit == 9) isFail = true;
  }

  if (isFail) cout << "F\n";
  else cout << "S\n";

  return 0;
}
  ```
