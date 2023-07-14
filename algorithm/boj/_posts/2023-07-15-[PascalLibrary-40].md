---
layout: single
title: "[백준 5753] Pascal Library (C#, C++) - soo:bak"
date: "2023-07-15 06:32:00 +0900"
description: 문자열, 구현 등을 주제로 하는 백준 5753번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [5753번 - Pascal Library](https://www.acmicpc.net/problem/5753)

## 설명
모든 만찬에 모두 참석한 참가자가 있는지 확인하는 문제입니다.<br>

각 만찬에 대한 모든 참석자들의 만찬 참가 여부를 표기하여,<br>

모든 만찬에 참가한 참석자가 있는지 판별하여 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      int len = 1;
      var input = Console.ReadLine()!.Split(' ');
      for (int i = 0; i < n; i++) {
        var word = input[i];
        char decodedC;
        if (word.Length < len) decodedC = ' ';
        else decodedC = word[len - 1];

        len = word.Length;

        Console.Write(decodedC);
      }
      Console.WriteLine();

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

  int n; cin >> n;
  size_t len = 1;
  for (int i = 0; i < n; i++) {
    string word; cin>> word;
    char decodedC;
    if (word.size() < len) decodedC = ' ';
    else decodedC = word[len - 1];
    len = word.size();

    cout << decodedC;
  }
  cout << "\n";

  return 0;
}
  ```
