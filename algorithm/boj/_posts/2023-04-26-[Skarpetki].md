---
layout: single
title: "[백준 26742] Skarpetki (C#, C++) - soo:bak"
date: "2023-04-26 19:33:00 +0900"
---

## 문제 링크
  [26742번 - Skarpetki](https://www.acmicpc.net/problem/26742)

## 설명
주어진 문자열에서 가능한 양말의 짝 개수를 구하는 문제입니다. <br>

입력으로 주어지는 문자열에서 `C` 의 개수와 `B` 의 개수를 각각 구한 후, <br>

가능한 양말의 짝 개수를 구하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!;

      int whiteSocks = 0, blackSocks = 0;

      foreach (char c in input) {
        if (c == 'B') whiteSocks++;
        else blackSocks++;
      }

      int pairs = whiteSocks / 2 + blackSocks / 2;
      Console.WriteLine(pairs);

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

  string input; cin >> input;

  int whiteSocks = 0, blackSocks = 0;

  for (char c : input) {
    if (c == 'B') whiteSocks++;
    else blackSocks++;
  }

  int pairs = whiteSocks / 2 + blackSocks / 2;
  cout << pairs << "\n";

  return 0;
}
  ```
