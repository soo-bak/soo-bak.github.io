---
layout: single
title: "[백준 10953] A+B - 6 (C#, C++) - soo:bak"
date: "2023-05-10 11:43:00 +0900"
description: 수학과 문자열, 사칙연산과 반복문을 주제로 하는 백준 10953번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
---

## 문제 링크
  [10953번 - A+B - 6](https://www.acmicpc.net/problem/10953)

## 설명
문자열에서 구분자를 다루는 것과 반복문의 사용하는 기본적인 사칙연산 문제입니다. <br>

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
        var input = Console.ReadLine()!.Split(',');
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
    int a, b; char delim;
    cin >> a >> delim >> b;
    cout << a + b << "\n";
  }

  return 0;
}

  ```
