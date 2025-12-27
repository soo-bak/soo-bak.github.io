---
layout: single
title: "[백준 16503] 괄호없는 사칙연산 (C#, C++) - soo:bak"
date: "2023-02-22 14:59:00 +0900"
description: 수학을 주제로한 백준 16503번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 16503
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 16503, 백준 16503번, BOJ 16503, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [16503번 - 괄호없는 사칙연산](https://www.acmicpc.net/problem/16503)

## 설명
  간단한 사칙연산에 대한 구현 문제입니다. <br>

  입력에 대하여 파싱을 진행한 후, <br>
  문제의 조건에 따른 첫 번째 연산 결과, 두 번째 연산 결과를 대/소 비교하여<br>
  숫자가 작은 결과를 첫 번째로, 숫자가 큰 결과를 두 번째로 출력합니다.
  <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {
  class Program {

    delegate int Calculator(int lhs, int rhs, string opt);

    static void Main(string[] args) {

      Calculator cal = (int lhs, int rhs, string opt) => {
        int ret = 0;
        if (opt == "*") ret = lhs * rhs;
        else if (opt == "/") ret = lhs / rhs;
        else if (opt == "+") ret = lhs + rhs;
        else if (opt == "-") ret = lhs - rhs;

        return ret;
      };

      string[]? input = Console.ReadLine()?.Split();
      int.TryParse(input![0], out int num1);
      int.TryParse(input![2], out int num2);
      int.TryParse(input![4], out int num3);

      int ans1 = cal(cal(num1, num2, input![1]), num3, input![3]),
          ans2 = cal(num1, cal(num2, num3, input![3]), input![1]);

      Console.WriteLine(Math.Min(ans1, ans2));
      Console.WriteLine(Math.Max(ans1, ans2));

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

int calculate(const int& lhs, const int& rhs, char& opt) {
  int ret = 0;
  if (opt == '*') ret = lhs * rhs;
  else if (opt == '/') ret = lhs / rhs;
  else if (opt == '+') ret = lhs + rhs;
  else if (opt == '-') ret = lhs - rhs;

  return ret;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int num1, num2, num3;
  char opt1, opt2;
  cin >> num1 >> opt1 >> num2 >> opt2 >> num3;

  int ans1 = calculate(calculate(num1, num2, opt1), num3, opt2),
      ans2 = calculate(num1, calculate(num2, num3, opt2), opt1);

  cout << min(ans1, ans2) << "\n" << max(ans1, ans2) << "\n";

  return 0;
}
  ```
