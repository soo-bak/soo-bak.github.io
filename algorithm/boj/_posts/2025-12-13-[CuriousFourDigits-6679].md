---
layout: single
title: "[백준 6679] 싱기한 네자리 숫자 (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 1000~9999 범위에서 10진수·12진수·16진수 자리수 합이 모두 같은 수를 찾는 백준 6679번 싱기한 네자리 숫자 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 6679
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 브루트포스
  - arithmetic
keywords: "백준 6679, 백준 6679번, BOJ 6679, CuriousFourDigits, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6679번 - 싱기한 네자리 숫자](https://www.acmicpc.net/problem/6679)

## 설명
네 자리 정수 중에서 10진수, 12진수, 16진수로 표현했을 때 자릿수 합이 모두 같은 수를 찾는 문제입니다.

<br>

## 접근법
1000부터 9999까지 모든 수를 검사합니다.

각 수에 대해 10진수, 12진수, 16진수로 변환하면서 자릿수 합을 구합니다.

세 값이 모두 같으면 해당 수를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int DigitSum(int n, int b) {
    var sum = 0;
    while (n > 0) {
      sum += n % b;
      n /= b;
    }
    return sum;
  }

  static void Main() {
    for (var x = 1000; x <= 9999; x++) {
      var s10 = DigitSum(x, 10);
      if (s10 == DigitSum(x, 12) && s10 == DigitSum(x, 16))
        Console.WriteLine(x);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int digitSum(int n, int b) {
  int s = 0;
  while (n) {
    s += n % b;
    n /= b;
  }
  return s;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  for (int x = 1000; x <= 9999; x++) {
    int s10 = digitSum(x, 10);
    if (s10 == digitSum(x, 12) && s10 == digitSum(x, 16))
      cout << x << "\n";
  }

  return 0;
}
```
