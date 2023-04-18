---
layout: single
title: "[백준 26731] Zagubiona litera (C#, C++) - soo:bak"
date: "2023-04-18 14:21:00 +0900"
---

## 문제 링크
  [26731번 - Zagubiona litera](https://www.acmicpc.net/problem/26731)

## 설명
간단한 구현 문제입니다. <br>

문자열을 입력 받은 후, 주어진 문자열에서 포함되지 않은 알파벳을 찾아 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var str = Console.ReadLine();

      for (char c = 'A'; c <= 'Z'; c++) {
        if (str!.IndexOf(c) == -1) {
          Console.WriteLine($"{c}");
          break ;
        }
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

  string str; cin >> str;

  for (char c = 'A'; c <= 'Z'; c++) {
    if (str.find(c) == string::npos) {
      cout << c << "\n";
      break ;
    }
  }

  return 0;
}
  ```
