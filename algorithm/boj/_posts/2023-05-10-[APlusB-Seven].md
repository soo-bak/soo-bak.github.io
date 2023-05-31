---
layout: single
title: "[백준 11021] A+B - 7 (C#, C++) - soo:bak"
date: "2023-05-10 19:38:00 +0900"
description: 수학과 기본적인 사칙연산을 주제로 하는 백준 11021번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [11021번 - A+B - 7](https://www.acmicpc.net/problem/11021)

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

      for (int i = 1; i <= cntCase; i++) {
        var input = Console.ReadLine()!.Split(' ');
        var a = int.Parse(input![0]);
        var b = int.Parse(input![1]);

        Console.WriteLine($"Case #{i}: {a + b}");
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

  for (int i = 1; i <= cntCase; i++) {
    int a, b; cin >> a >> b;

    cout << "Case #" << i << ": " << a + b << "\n";
  }

  return 0;
}
  ```
