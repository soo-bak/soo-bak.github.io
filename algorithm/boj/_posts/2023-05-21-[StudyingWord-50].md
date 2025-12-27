---
layout: single
title: "[백준 1157] 단어 공부 (C#, C++) - soo:bak"
date: "2023-05-21 14:37:00 +0900"
description: 문자열 다루기와 탐색을 주제로 하는 백준 1157번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 1157
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 1157, 백준 1157번, BOJ 1157, StudyingWord, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [1157번 - 단어 공부](https://www.acmicpc.net/problem/1157)

## 설명
입력으로 주어지는 문자열에서 가장 많이 등장하는 알파벳을 찾는 문제입니다. <br>

문제의 조건에 따르면 알파벳의 대문자와 소문자를 구분하지 않고 찾아야 하기 때문에, <br>

문자열을 모두 대문자로 변환하거나 소문자로 변환한 후 탐색을 해야 합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var word = Console.ReadLine()!;

      var cntAlphabets = new int[26];

      foreach (var c in word.ToUpper())
        cntAlphabets[c - 'A']++;

      var cntMax = cntAlphabets.Max();
      var freqMax = cntAlphabets.Count(cnt => cnt == cntMax);

      if (freqMax > 1) Console.WriteLine("?");
      else Console.WriteLine((char)(Array.IndexOf(cntAlphabets, cntMax) + 'A'));

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

  string word; cin >> word;

  vector<int> cntAlphabets(26, 0);

  for (char c : word) {
    c = toupper(c);
    cntAlphabets[c - 'A']++;
  }

  int cntMax = *max_element(cntAlphabets.begin(), cntAlphabets.end());
  int freqMax = count(cntAlphabets.begin(), cntAlphabets.end(), cntMax);

  if (freqMax > 1) cout << "?\n";
  else cout << (char)(max_element(cntAlphabets.begin(), cntAlphabets.end()) -
                      cntAlphabets.begin() + 'A') << "\n";

  return 0;
}
  ```
