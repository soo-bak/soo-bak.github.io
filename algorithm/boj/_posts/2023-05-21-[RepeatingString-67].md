---
layout: single
title: "[백준 2675] 문자열 반복 (C#, C++) - soo:bak"
date: "2023-05-21 12:55:00 +0900"
description: 문자열 다루기를 주제로 하는 백준 2675번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [2675번 - 문자열 반복](https://www.acmicpc.net/problem/2675)

## 설명
입력으로 주어지는 문자열의 각 문자를 주어진 횟수만큼 반복하여 늘려서 새로운 문자열을 만드는 문제입니다. <br>

대상이 되는 문자열을 탐색하며 문자열의 각 문자에 대해 반복 횟수 만큼 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int c = 0; c < cntCase; c++) {
        var input = Console.ReadLine()!.Split(' ');
        var cntRepeat = int.Parse(input[0]);
        var str = input[1];

        foreach (var ch in str) {
          for (int i = 0; i < cntRepeat; i++)
            Console.Write(ch);
        }
        Console.WriteLine();
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

  int cntCase; cin >> cntCase;

  for (int c = 0; c < cntCase; c++) {
    int cntRepeat; string str;
    cin >> cntRepeat >> str;

    for (char ch : str) {
      for (int i = 0; i < cntRepeat; i++)
        cout << ch;
    }
    cout << "\n";
  }

  return 0;
}
  ```
