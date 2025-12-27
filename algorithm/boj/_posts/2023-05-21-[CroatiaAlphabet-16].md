---
layout: single
title: "[백준 2941] 크로아티아 알파벳 (C#, C++) - soo:bak"
date: "2023-05-21 16:00:00 +0900"
description: 문자열 다루기와 시뮬레이션을 주제로 하는 백준 2941번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2941
  - C#
  - C++
  - 알고리즘
  - 구현
  - 문자열
keywords: "백준 2941, 백준 2941번, BOJ 2941, CroatiaAlphabet, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [2941번 - 크로아티아 알파벳](https://www.acmicpc.net/problem/2941)

## 설명
입력으로 주어진 단어에서, 문제의 표를 바탕으로 변경된 형태로 주어진 <b>크로아티아 알파벳</b>을 찾아서 그 개수를 세는 문제입니다. <br>

단어에서 크로아티아 알파벳을 찾아 임의의 일반 알파벳으로 대체하면, 남은 문자의 개수가 크로아티아 알파벳의 개수와 같게 됩니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      string[] croatiaAlphabets = {"c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="};

      var word = Console.ReadLine()!;

        foreach (string alphabet in croatiaAlphabets) {
          while (word.Contains(alphabet))
            word = word.Replace(alphabet, "a");
        }

        Console.WriteLine(word.Length);

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

  string croatiaAlphabets[8] = {"c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z="};

  string word; cin >> word;

  for (string alphabet : croatiaAlphabets) {
    while (word.find(alphabet) != string::npos)
      word.replace(word.find(alphabet), alphabet.length(), "a");
  }

  cout << word.length() << "\n";

  return 0;
}
  ```
