---
layout: single
title: "[백준 5340] Secret Location (C#, C++) - soo:bak"
date: "2023-07-10 09:17:00 +0900"
description: 문자열, 파싱, 구현 등을 주제로 하는 백준 5340번 문제를 C++ C# 으로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 5340
  - C#
  - C++
  - 알고리즘
keywords: "백준 5340, 백준 5340번, BOJ 5340, ScretLocation, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [5340번 - Secret Location](https://www.acmicpc.net/problem/5340)

## 설명
입력으로 주어지는 `6` 줄의 문장을 바탕으로, 위도와 경도를 복호화하는 문제입니다.<br>

단순히, 문장의 길이들이 위도와 경도의 정보를 나타냅니다.<br>

<br>
문장의 마지막에 `' '` 공백이 주어지는 경우에 대해서 주의합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var coord = new List<int>(6);
      for (int i = 0; i < 6; i++) {
        var line = Console.ReadLine()!;
        if (line.EndsWith(' '))
          line = line.Remove(line.Length - 1);
        coord.Add(line.Length);
      }

      Console.WriteLine($"Latitude {coord[0]}:{coord[1]}:{coord[2]}");
      Console.WriteLine($"Longitude {coord[3]}:{coord[4]}:{coord[5]}");

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

  vector<int> coord(6);
  for (int i = 0; i < 6; i++) {
    string line; getline(cin, line);
    if (*(line.end() - 1) == ' ')
      line.pop_back();
    coord[i] = line.length();
  }

  cout << "Latitude " << coord[0] << ":" << coord[1] << ":" << coord[2] << "\n";
  cout << "Longitude " << coord[3] << ":" << coord[4] << ":" << coord[5] << "\n";

  return 0;
}
  ```
