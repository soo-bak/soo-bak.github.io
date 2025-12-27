---
layout: single
title: "[백준 4892] 숫자 맞추기 게임 (C#, C++) - soo:bak"
date: "2025-12-27 17:05:00 +0900"
description: "백준 4892번 C#, C++ 풀이 - 주어진 규칙에 따라 연산을 수행하여 숫자를 맞추는 시뮬레이션 문제"
tags:
  - 백준
  - BOJ
  - 4892
  - C#
  - C++
  - 알고리즘
keywords: "백준 4892, 백준 4892번, BOJ 4892, NumberGuessingGame, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4892번 - 숫자 맞추기 게임](https://www.acmicpc.net/problem/4892)

## 설명
주어진 숫자에 대해 정해진 규칙에 따라 연산을 수행하고, 중간 결과의 홀짝 여부와 최종 값을 출력하는 문제입니다.

<br>

## 접근법
문제에서 제시한 규칙을 그대로 구현합니다. n0에 3을 곱한 n1의 홀짝 여부에 따라 n2를 다르게 계산합니다.

이후 n2에 3을 곱한 n3를 9로 나눈 몫이 n4가 됩니다. 각 테스트 케이스마다 n1의 홀짝 여부와 n4를 출력합니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var cntCase = 1;
    while (true) {
      var num0 = int.Parse(Console.ReadLine()!);
      if (num0 == 0) break;

      var num1 = 3 * num0;
      int num2;
      string parity;
      if (num1 % 2 == 0) {
        parity = "even";
        num2 = num1 / 2;
      } else {
        parity = "odd";
        num2 = (num1 + 1) / 2;
      }

      var num3 = 3 * num2;
      var num4 = num3 / 9;

      Console.WriteLine($"{cntCase}. {parity} {num4}");
      cntCase++;
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int cntCase = 1;
  int num0;
  while (cin >> num0 && num0) {
    cout << cntCase << ". ";

    int num1 = 3 * num0;
    int num2;
    if (num1 % 2 == 0) {
      cout << "even ";
      num2 = num1 / 2;
    } else {
      cout << "odd ";
      num2 = (num1 + 1) / 2;
    }

    int num3 = 3 * num2;
    int num4 = num3 / 9;

    cout << num4 << "\n";
    cntCase++;
  }

  return 0;
}
```

