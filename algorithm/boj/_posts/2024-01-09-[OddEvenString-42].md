---
layout: single
title: "[백준 25801] Odd/Even Strings (C#, C++) - soo:bak"
date: "2024-01-09 08:33:00 +0900"
description: 구현, 문자열 등을 주제로 하는 백준 25801번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 25801
  - C#
  - C++
  - 알고리즘
keywords: "백준 25801, 백준 25801번, BOJ 25801, OddEvenString, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [25801번 - Odd/Even Strings](https://www.acmicpc.net/problem/25801)

## 설명
입력으로 주어지는 문자열이 `Even` 문자열인지, `Odd` 문자열인지, 또는 둘 다 아닌지를 판별하는 문제입니다.<br>
<br>
문자열이 `Even` 문자열이 되려면 모든 문자가 짝수 번 등장해야 하며,<br>
<br>
`Odd` 문자열이 되려면 모든 문자가 홀수 번 등장해야 합니다.<br>
<br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var str = Console.ReadLine()!;

      Dictionary<char, int> freq = new Dictionary<char, int>();
      foreach (char ch in str) {
        if (!freq.ContainsKey(ch)) freq[ch] = 0;
        freq[ch]++;
      }

      int eventCount = 0, oddCount = 0;
      foreach (var p in freq) {
        if (p.Value % 2 == 0) eventCount++;
        else oddCount++;
      }

      if (oddCount == 0) Console.WriteLine("0");
      else if (eventCount == 0) Console.WriteLine("1");
      else Console.WriteLine("0/1");

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

  string str; cin >> str;

  unordered_map<char, int> freq;
  for (char ch : str)
    freq[ch]++;

  int eventCount = 0, oddCount = 0;
  for (auto& p : freq) {
    if (p.second % 2 == 0) eventCount++;
    else oddCount++;
  }

  if (oddCount == 0) cout << "0\n";
  else if (eventCount == 0) cout << "1\n";
  else cout << "0/1\n";

  return 0;
}
  ```
