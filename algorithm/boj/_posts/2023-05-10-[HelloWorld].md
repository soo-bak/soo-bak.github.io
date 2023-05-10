---
layout: single
title: "[백준 2557] Hello World (C#, C++) - soo:bak"
date: "2023-05-10 09:43:00 +0900"
---

## 문제 링크
  [2557번 - Hello World](https://www.acmicpc.net/problem/2557)

## 설명
새로운 프로그래밍 언어를 배울 때, 가장 먼저 해보는 관례인 <b>"Hello World!"</b> 를 출력하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      Console.WriteLine("Hello World!");

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

  cout << "Hello World!\n";

  return 0;
}
  ```
