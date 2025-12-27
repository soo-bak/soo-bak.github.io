---
layout: single
title: "[백준 26040] 특정 대문자를 소문자로 바꾸기 (C#, C++) - soo:bak"
date: "2023-06-17 11:35:00 +0900"
description: 문자열, 구현 등을 주제로 하는 백준 26040번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26040
  - C#
  - C++
  - 알고리즘
keywords: "백준 26040, 백준 26040번, BOJ 26040, ConvertingUppercase, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26040번 - 특정 대문자를 소문자로 바꾸기](https://www.acmicpc.net/problem/26040)

## 설명
대문자와 소문자로 이루어진 문자열 `a` 와 대문자 목록 `b` 가 주어졌을 때, <br>

`b` 에 있는 모든 대문자를 `a` 에서 찾은 후 해당 대문자를 소문자로 바꾸는 문제입니다. <br>

풀이 과정은 다음과 같습니다. <br>

- 문자열 `a` 와 대문자 목록 `b` 를 입력 받습니다. <br>
- 대문자 목록 `b` 에 있는 모든 대문자들을 문자열 `a` 에서 탐색한 후 소문자로 변환합니다. <br>
- 변환된 문자열을 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var a = Console.ReadLine()!;
      var b = Console.ReadLine()!;

      HashSet<char> caps = new HashSet<char>(b.Where(c => c != ' '));

      foreach (var c in a) {
        if (caps.Contains(c))
          a = a.Replace(c, char.ToLower(c));
      }

      Console.WriteLine(a);

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

  string a, b;
  getline(cin, a);
  getline(cin, b);

  unordered_set<char> caps;
  for (const char& c : b)
    if (c != ' ')
      caps.insert(c);

  for (char& c : a)
    if (caps.find(c) != caps.end())
      c = tolower(c);

  cout << a << "\n";

  return 0;
}
  ```
