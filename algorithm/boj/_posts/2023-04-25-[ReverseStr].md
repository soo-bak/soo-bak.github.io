---
layout: single
title: "[백준 26546] Reverse (C#, C++) - soo:bak"
date: "2023-04-25 17:35:00 +0900"
description: 문자열과 구현을 주제로 하는 백준 26546번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26546
  - C#
  - C++
  - 알고리즘
keywords: "백준 26546, 백준 26546번, BOJ 26546, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26546번 - Reverse](https://www.acmicpc.net/problem/26546)

## 설명
문자열을 다루는 구현 문제입니다. <br>

문제의 목표는 기존의 `substring` 함수와 반대의 작업을 구현하는 것입니다.<br>

입력으로 주어지는 문자열에서, 인덱스 `i` 부터 시작하여 `j - 1` 까지의 문자열을 부분적으로 제거한 후 결과를 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var n = int.Parse(Console.ReadLine()!);

      for (int t = 0; t < n; t++) {
        var input = Console.ReadLine()?.Split();
        var i = int.Parse(input![1]);
        var j = int.Parse(input![2]);

        var ret = input[0]!.Substring(0, i) + input[0]!.Substring(j);
        Console.WriteLine(ret);
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

  int n; cin >> n;

  for (int t = 0; t < n; t++) {
    string input;
    int i, j;
    cin >> input >> i >> j;

    string ret = input.substr(0, i) + input.substr(j);
    cout << ret << "\n";
  }

  return 0;
}
  ```
