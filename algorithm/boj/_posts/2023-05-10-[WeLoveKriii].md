---
layout: single
title: "[백준 10718] We love kriii (C#, C++) - soo:bak"
date: "2023-05-10 09:47:00 +0900"
description: 간단한 출력을 하는 백준 10718번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 10718
  - C#
  - C++
  - 알고리즘
keywords: "백준 10718, 백준 10718번, BOJ 10718, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [10718번 - We love kriii](https://www.acmicpc.net/problem/10718)

## 설명
간단한 출력 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      Console.WriteLine("강한친구 대한육군\n강한친구 대한육군");

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

  cout << "강한친구 대한육군\n강한친구 대한육군\n";

  return 0;
}
  ```
