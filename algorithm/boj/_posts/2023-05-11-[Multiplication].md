---
layout: single
title: "[백준 2588] 곱셈 (C#, C++) - soo:bak"
date: "2023-05-11 14:43:00 +0900"
---

## 문제 링크
  [2588번 - 곱셈](https://www.acmicpc.net/problem/2588)

## 설명
곱셈의 과정에 대한 수학 문제입니다. <br>

문제에서 요구하는 위치의 수를 순서대로 출력합니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      var a = int.Parse(Console.ReadLine()!);
      var b = int.Parse(Console.ReadLine()!);

      var remdDigitOne = b % 10;
      var remdDigitTen = (b % 100) - remdDigitOne;
      var quotientHund = b / 100;

      Console.WriteLine($"{a * remdDigitOne}");
      Console.WriteLine($"{a * remdDigitTen / 10}");
      Console.WriteLine($"{a * quotientHund}");
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

  int remdDigitOne = b % 10,
      remdDigitTen = (b % 100) - remdDigitOne,
      quotientHund = b / 100;

  cout << a * remdDigitOne << "\n"
       << a * remdDigitTen / 10 << "\n"
       << a * quotientHund << "\n"
       << a * b << "\n";

  return 0;
}
  ```
