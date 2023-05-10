---
layout: single
title: "[백준 1000] A+B (C#, C++) - soo:bak"
date: "2023-05-10 10:07:00 +0900"
---

## 문제 링크
  [1000번 - A+B](https://www.acmicpc.net/problem/1000)

## 설명
두 수의 합을 출력하는 간단한 문제입니다. <br>

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

      Console.WriteLine($"{a + b}");

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
  cout << a + b << "\n";

  return 0;
}
  ```
