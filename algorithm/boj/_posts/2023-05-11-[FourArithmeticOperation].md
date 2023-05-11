---
layout: single
title: "[백준 10869] 사칙연산 (C#, C++) - soo:bak"
date: "2023-05-11 13:27:00 +0900"
---

## 문제 링크
  [10869번 - 사칙연산](https://www.acmicpc.net/problem/10869)

## 설명
사칙연산에 대한 단순한 문제입니다. <br>

두 자연수를 입력받아, 두 수의 합, 차이, 곱, 몫, 그리고 나머지를 차례대로 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var input = Console.ReadLine()!.Split(' ');
      var a = int.Parse(input[0]);
      var b = int.Parse(input[1]);

      Console.WriteLine($"{a + b}");
      Console.WriteLine($"{a - b}");
      Console.WriteLine($"{a * b}");
      Console.WriteLine($"{a / b}");
      Console.WriteLine($"{a % b}");

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

  cout << a + b << "\n"
       << a - b << "\n"
       << a * b << "\n"
       << a / b << "\n"
       << a % b << "\n";

  return 0;
}
  ```
