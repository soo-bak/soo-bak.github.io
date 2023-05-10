---
layout: single
title: "[백준 10950] A+B - 3 (C#, C++) - soo:bak"
date: "2023-05-10 11:23:00 +0900"
---

## 문제 링크
  [10950번 - A+B - 3](https://www.acmicpc.net/problem/10950)

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

      var cntCase = int.Parse(Console.ReadLine()!);

      for (int i = 0; i < cntCase; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var a = int.Parse(input![0]);
        var b = int.Parse(input![1]);

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

  int cntCase; cin >> cntCase;

  for (int i = 0; i < cntCase; i++) {
    int a, b; cin >> a >> b;
    cout << a + b << "\n";
  }

  return 0;
}
  ```
