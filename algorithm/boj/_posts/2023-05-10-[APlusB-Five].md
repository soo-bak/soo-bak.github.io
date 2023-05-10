---
layout: single
title: "[백준 10952] A+B - 5 (C#, C++) - soo:bak"
date: "2023-05-10 11:41:00 +0900"
---

## 문제 링크
  [10952번 - A+B - 5](https://www.acmicpc.net/problem/10952)

## 설명
기본적인 사칙 연산과 반복문을 사용하는 문제입니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      while (true) {
        var input = Console.ReadLine()!.Split(' ');
        var a = int.Parse(input[0]);
        var b = int.Parse(input[1]);

        if (a == 0 && b == 0) break ;

        Console.WriteLine($"{a + b}");
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

  while (true) {
    int a, b; cin >> a >> b;
    if (a == 0 && b == 0) break ;

    cout << a + b << "\n";
  }

  return 0;
}
  ```
