---
layout: single
title: "[백준 6889] Smile with Similes (C#, C++) - soo:bak"
date: "2023-08-03 09:42:00 +0900"
description: 문자열, 구현 등을 주제로 하는 백준 6889번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6889
  - C#
  - C++
  - 알고리즘
keywords: "백준 6889, 백준 6889번, BOJ 6889, SmileWithSmiles, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6889번 - Smile with Similes](https://www.acmicpc.net/problem/6889)

## 설명
형용사와 명사를 입력으로 받아, 각각의 조합을 만들어내는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);
      var m = int.Parse(Console.ReadLine()!);

      var prefix = new List<string>(n);
      for (int i = 0; i < n; i++)
        prefix.Add(Console.ReadLine()!);

      var nouns = new List<string>(m);
      for (int i = 0; i < m; i++)
        nouns.Add(Console.ReadLine()!);

      for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++)
          Console.WriteLine($"{prefix[i]} as {nouns[j]}");
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

  int n, m; cin >> n >> m;

  vector<string> prefix(n);
  for (int i = 0; i < n; i++)
    cin >> prefix[i];

  vector<string> nouns(m);
  for (int i = 0; i < m; i++)
    cin >> nouns[i];

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < m; j++)
      cout << prefix[i] << " as " << nouns[j] << "\n";
  }

  return 0;
}
  ```
