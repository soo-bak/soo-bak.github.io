---
layout: single
title: "[백준 10430] 나머지 (C#, C++) - soo:bak"
date: "2023-05-11 14:22:00 +0900"
---

## 문제 링크
  [10430번 - 나머지](https://www.acmicpc.net/problem/10430)

## 설명
간단한 사칙연산 문제입니다. <br>

세 정수 `a`, `b`, `c` 를 입력받은 후 문제의 조건에 맞추어 출력합니다. <br>

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
      var c = int.Parse(input[2]);

      Console.WriteLine($"{(a + b) % c}");
      Console.WriteLine($"{((a % c) + b % c) % c}");
      Console.WriteLine($"{(a * b) % c}");
      Console.WriteLine($"{((a % c) * (b % c) % c)}");

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

  int a, b, c; cin >> a >> b >> c;

  cout << (a + b) % c << "\n"
       << ((a % c) + b % c) % c << "\n"
       << (a * b) % c << "\n"
       << ((a % c) * (b % c) % c) << "\n";

  return 0;
}
  ```
