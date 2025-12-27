---
layout: single
title: "[백준 9161] Sir Bedavere’s Bogus Division Solutions (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: "백준 9161번 C#, C++ 풀이 - 분자 끝자리와 분모 앞자리를 지워도 값이 같은 세 자리 수 분수 쌍을 나열하는 문제"
tags:
  - 백준
  - BOJ
  - 9161
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 브루트포스
  - arithmetic
keywords: "백준 9161, 백준 9161번, BOJ 9161, BogusDivision, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9161번 - Sir Bedavere’s Bogus Division Solutions](https://www.acmicpc.net/problem/9161)

## 설명
세 자리 분수에서 특정 자릿수를 지워도 값이 같은 분수 쌍을 모두 찾는 문제입니다.

<br>

## 접근법
분자의 일의 자리 숫자와 분모의 백의 자리 숫자가 같을 때, 그 숫자를 각각 지웁니다. 지운 후의 분수가 원래 분수와 값이 같은지 확인합니다.

등식 비교는 부동소수점 오차를 피하기 위해 교차 곱셈으로 처리합니다. 분자에 축약된 분모를 곱한 값과 축약된 분자에 분모를 곱한 값이 같으면 조건을 만족합니다.

같은 숫자가 세 번 반복되는 자명한 경우는 제외합니다. 100부터 999까지 모든 세 자리 수 쌍을 탐색하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    for (var n = 100; n <= 999; n++) {
      var last = n % 10;
      for (var m = 100; m <= 999; m++) {
        if (m / 100 != last) continue;

        var n2 = n / 10;
        var m2 = m % 100;
        if (n * m2 != n2 * m) continue;

        if (n % 111 == 0 && m % 111 == 0 && n / 111 == m / 111)
          continue;

        Console.WriteLine($"{n} / {m} = {n2} / {m2}");
      }
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

  for (int n = 100; n <= 999; n++) {
    int last = n % 10;
    for (int m = 100; m <= 999; m++) {
      if (m / 100 != last) continue;

      int n2 = n / 10;
      int m2 = m % 100;
      if (n * m2 != n2 * m) continue;

      if (n % 111 == 0 && m % 111 == 0 && n / 111 == m / 111)
        continue;

      cout << n << " / " << m << " = " << n2 << " / " << m2 << "\n";
    }
  }

  return 0;
}
```
