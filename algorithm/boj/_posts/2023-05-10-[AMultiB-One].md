---
layout: single
title: "[백준 10998] A×B (C#, C++) - soo:bak"
date: "2023-05-10 19:45:00 +0900"
---

## 문제 링크
  [10998번 - A×B](https://www.acmicpc.net/problem/10998)

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

      Console.WriteLine($"{a * b}");

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

  cout << a * b << "\n";

  return 0;
}
  ```
