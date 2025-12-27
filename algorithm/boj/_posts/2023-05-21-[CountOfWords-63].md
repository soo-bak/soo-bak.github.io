---
layout: single
title: "[백준 1152] 단어의 개수 (C#, C++) - soo:bak"
date: "2023-05-21 15:49:00 +0900"
description: 문자열 다루기를 주제로 하는 백준 1152번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1152
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 1152, 백준 1152번, BOJ 1152, CountOfWords, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [1152번 - 단어의 개수](https://www.acmicpc.net/problem/1152)

## 설명
주어진 문자열에서 단어의 개수를 세는 문제입니다. <br>

문자열을 공백으로 구분하여 단어의 개수를 센 후 출력합니다.

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntWord = Console.ReadLine()!.Split(' ', StringSplitOptions.RemoveEmptyEntries).Length;

      Console.WriteLine(cntWord);

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

  int cntWord = 0;
  while (true) {
    string word; cin >> word;
    if (cin.eof()) break ;
    cntWord++;
  }

  cout << cntWord << "\n";

  return 0;
}
  ```
