---
layout: single
title: "[백준 28691] 정보보호학부 동아리 소개 (C#, C++) - soo:bak"
date: "2023-08-21 12:41:00 +0900"
description: 문자열, 구현 등을 주제로 하는 백준 28691번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 28691
  - C#
  - C++
  - 알고리즘
keywords: "백준 28691, 백준 28691번, BOJ 28691, IntroduceOfInfoCommu, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [28691번 - 정보보호학부 동아리 소개](https://www.acmicpc.net/problem/28691)

## 설명
입력으로 주어지는 문자열 중 첫 문자에 따라서 일치하는 동아리 명을 출력하는 단순한 문자열 처리 문제입니다. <br>
<br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      Dictionary<char, string> clubMap = new Dictionary<char, string> {
        {'M', "MatKor"},
        {'W', "WiCys"},
        {'C', "CyKor"},
        {'A', "AlKor"},
        {'$', "$clear"}
      };

      char firstLetter = Console.ReadLine()![0];

      Console.WriteLine(clubMap[firstLetter]);

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

  map<char, string> clubMap = {
    {'M', "MatKor"},
    {'W', "WiCys"},
    {'C', "CyKor"},
    {'A', "AlKor"},
    {'$', "$clear"}
  };

  char firstLetter; cin >> firstLetter;

  cout << clubMap[firstLetter] << "\n";

  return 0;
}
  ```
