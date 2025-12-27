---
layout: single
title: "[백준 6750] Rotating Letters (C#, C++) - soo:bak"
date: "2023-07-19 11:21:00 +0900"
description: 문자열, 문자, 구현 등을 주제로 하는 백준 6750번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 6750
  - C#
  - C++
  - 알고리즘
keywords: "백준 6750, 백준 6750번, BOJ 6750, RotatingLetter, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [6750번 - Rotating Letters](https://www.acmicpc.net/problem/6750)

## 설명
입력으로 주어지는 단어가 `180` 도 회전을 했을 때에도도 그대로인 문자<br>

`I`, `O`, `S`, `H`, `Z`, `X`, `N` 들로 이루어졌는지 판단하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      HashSet<char> validChar = new HashSet<char>{'I', 'O', 'S', 'H', 'Z', 'X', 'N'};

      var word = Console.ReadLine()!;

      foreach (var c in word)  {
        if (!validChar.Contains(c))  {
          Console.WriteLine("NO");
          return ;
        }
      }

      Console.WriteLine("YES");

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

  set<char> validChar {'I', 'O', 'S', 'H', 'Z', 'X', 'N'};

  string word; cin >> word;

  for (char c : word) {
    if (validChar.find(c) == validChar.end()) {
      cout << "NO\n";
      return 0;
    }
  }

  cout << "YES\n";

  return 0;
}
  ```
