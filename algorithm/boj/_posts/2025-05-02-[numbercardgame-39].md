---
layout: single
title: "[백준 4564] 숫자 카드놀이 (C#, C++) - soo:bak"
date: "2025-05-02 19:57:00 +0900"
description: 자릿수의 곱을 반복하며 한 자리 수가 나올 때까지 수열을 생성하는 백준 4564번 숫자 카드놀이 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 4564
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 4564, 백준 4564번, BOJ 4564, numbercardgame, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4564번 - 숫자 카드놀이](https://www.acmicpc.net/problem/4564)

## 설명
각 입력마다 주어지는 자연수에 대하여,

해당 수가 한 자리 수가 될 때까지 **각 자릿수의 수를 곱해 다음 수를 만들어 나가는 과정**을 반복하며,

모든 중간 값을 순서대로 출력하는 문제입니다.

<br>

## 접근법

- 입력으로 주어지는 수 마다, **모든 자릿수를 곱한 값**을 구합니다.
- 곱셈 결과가 **한 자리 수가 되기 전까지** 위 과정을 반복하며 수열을 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      string s = Console.ReadLine();
      if (s == "0") break;

      while (s.Length > 1) {
        Console.Write(s + " ");
        int prod = 1;
        foreach (char ch in s) {
          if (ch == '0') {
            prod = 0;
            break;
          }
          prod *= ch - '0';
        }
        s = prod.ToString();
      }
      Console.WriteLine(s);
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

  string num;
  while (cin >> num && num != "0") {
    while (num.size() > 1) {
      cout << num << " ";
      int prod = 1;
      for (char ch : num) {
        if (ch == '0') {
          prod = 0;
          break;
        }
        prod *= ch - '0';
      }
      num = to_string(prod);
    }
    cout << num << "\n";
  }

  return 0;
}
```
