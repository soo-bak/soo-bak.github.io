---
layout: single
title: "[백준 26711] A+B (C#, C++) - soo:bak"
date: "2023-05-03 19:20:00 +0900"
description: 수학과 큰 수 연산, 문자열로 덧셈을 구현하는 것을 주제로 하는 백준 26711번 알고리즘 문제를 C# 과 C++ 로 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 26711
  - C#
  - C++
  - 알고리즘
  - 수학
  - arithmetic
  - arbitrary_precision
keywords: "백준 26711, 백준 26711번, BOJ 26711, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
  [26711번 - A+B](https://www.acmicpc.net/problem/26711)

## 설명
얼핏 보면 단순히 두 개의 숫자를 더하는 프로그램을 작성하는 문제로 보입니다. <br>

하지만, 문제의 설명에 따르면 입력으로 <b>주어지는 숫자가 최대</b> `5000` <b>개의 자릿수를 가진다</b>는 조건이 있습니다.<br>
즉, `C++` 언어의 표준 라이브러리로는 숫자를 표현할 수 있는 방법에 한계가 있습니다. <br>
따라서, 외부 라이브러리를 사용하지 않고 `C++` 언어로 해당 문제를 풀이하기 위해서는, <b>문자열을 이용하여 덧셈을 직접 구현</b>해야 합니다. <br>

반면에, `C#` 언어에서는 `System.Numerics` 네임스페이스에 정의되어 있는 `BigInteger` 자료형을 통해 쉽게 해결할 수 있습니다. <br>
`C#` 언어에서 해당 `BigInteger` 자료형은 크기에 제한에 없기 때문에, 사용 가능한 메모리가 허용하는 한에서 어떠한 크기의 정수라도 저장할 수 있습니다. <br>

따라서, 아래의 코드 중 `C#` 언어를 이용한 풀이에서는 `BigInteger` 자료형을 활용하였고, <br>
`C++` 언어를 이용한 풀이에서는 문자열을 이용해 직접 덧셈을 구현하여 풀이하였습니다. <br>

- - -

## Code
<b>[ C# ] </b>
<br>

  ```c#
namespace Solution {

  using System.Numerics;

  class Program {
    static void Main(string[] args) {

    var a = BigInteger.Parse(Console.ReadLine()!);
    var b = BigInteger.Parse(Console.ReadLine()!);

    Console.WriteLine(a + b);

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

string addNums(const string& a, const string& b) {
  string ret = "";

  int carryOver = 0, lenA = a.length(), lenB = b.length();

  while (true) {
    if (lenA <= 0 && lenB <= 0) break ;

    int numA = 0, numB = 0;
    if (lenA > 0) numA = a[lenA - 1] - '0';
    if (lenB > 0) numB = b[lenB - 1] - '0';

    int sum = numA + numB + carryOver;
    carryOver = sum / 10;
    ret += (sum % 10) + '0';

    if (lenA > 0) lenA--;
    if (lenB > 0) lenB--;
  }

  if (carryOver > 0) ret += carryOver + '0';

  reverse(ret.begin(), ret.end());

  return ret;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  string a, b; cin >> a >> b;

  cout << addNums(a, b) << "\n";

  return 0;
}
  ```
