---
layout: single
title: "[백준 1001] A-B (C#, C++) - soo:bak"
date: "2023-05-10 11:23:00 +0900"
description: 수학과 사칙연산을 주제로 하는 백준 1001번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [1001번 - A-B](https://www.acmicpc.net/problem/1001)

## 설명
기본적인 사칙 연산 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {
      var input = Console.ReadLine()!.Split(' ');
      var a = int.Parse(input![0]);
      var b = int.Parse(input![1]);
      Console.WriteLine($"{a - b}");
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
  int a, b; cin >> a >> b;
  cout << a - b << "\n";
  return 0;
}
  ```
