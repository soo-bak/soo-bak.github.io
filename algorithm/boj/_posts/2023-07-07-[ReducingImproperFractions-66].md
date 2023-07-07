---
layout: single
title: "[백준 9297] Reducing Improper Fractions (C#, C++) - soo:bak"
date: "2023-07-07 09:57:00 +0900"
description: 분수, 수학, 정수부, 소수부, 구현 등을 주제로 하는 백준 9297번 문제를 C++ C# 으로 풀이 및 해설
---

## 문제 링크
  [9297번 - Reducing Improper Fractions](https://www.acmicpc.net/problem/9297)

## 설명
두 개의 정수를 입력받아, 앞의 정수를 뒤의 정수로 나눈 몫과 나머지 부분을 출력하는 문제입니다. <br>

나머지 부분에 대해서는 분수 형태로 출력해야 합니다. <br>
- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {
    static void Main(string[] args) {

      int t = int.Parse(Console.ReadLine()!);

      for (int i = 1; i <= t; i++) {
        var input = Console.ReadLine()!.Split();
        var num = int.Parse(input[0]);
        var den = int.Parse(input[1]) ;

        var quotient = num / den;
        num %= den;

        Console.Write($"Case {i}: ");

        if (quotient == 0) {
          if (num == 0) Console.WriteLine("0");
          else Console.WriteLine($"{num}/{den}");
        } else {
          if (num == 0) Console.WriteLine(quotient);
          else Console.WriteLine($"{quotient} {num}/{den}");
        }
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

  int t; cin >> t;

  for (int i = 1; i <= t; i++) {
    int num, den; cin >> num >> den;

    int quotient = num / den;
    num %= den;

    cout << "Case " << i << ": ";

    if (quotient == 0) {
      if (num == 0) cout << "0\n";
      else cout << num << "/" << den << "\n";
    } else {
      if (num == 0) cout << quotient << "\n";
      else cout << quotient << " " << num << "/" << den << "\n";
    }
  }

  return 0;
}
  ```
