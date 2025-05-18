---
layout: single
title: "[백준 4998] 저금 (C++, C#) - soo:bak"
date: "2025-05-18 18:21:00 +0900"
description: 원금과 이자율로 목표 금액을 달성하는 데 걸리는 시간을 계산하는 백준 4998번 저금 문제의 C# 및 C++ 풀이 및 해설
---

## 문제 링크
[4998번 - 저금](https://www.acmicpc.net/problem/4998)

## 설명

**현재 예치된 금액에서 시작해 매년 일정 비율의 이자가 붙을 때, 목표 금액을 초과하기까지 걸리는 최소 연도를 계산하는 문제입니다.**

입력으로는 세 가지 값이 주어집니다:

- 현재 예치된 금액 `N` (소수점 둘째 자리까지)
- 연 이자율 `B%` (소수점 둘째 자리까지)
- 목표 금액 `M`

이자는 복리로 계산되며, 해마다 **예치된 금액 전체에 대해 이자가 붙습니다.**

따라서 **연속적으로 이자가 누적되는 방식**으로 예치 금액이 증가하게 됩니다.

<br>

## 접근법

1. 입력으로 주어진 `N`, `B`, `M`을 실수형으로 받아 처리합니다.
2. 해마다 이자를 계산하여 원금에 더해주며, 매년 반복합니다.
3. 현재 금액이 목표 금액 `M`을 초과하면 종료하고, 그때까지 걸린 연수를 출력합니다.

<br>

---

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string input;
    while ((input = Console.ReadLine()) != null) {
      var parts = input.Split();
      double n = double.Parse(parts[0]);
      double b = double.Parse(parts[1]);
      double m = double.Parse(parts[2]);

      int year = 0;
      while (n <= m) {
        n += n * b / 100.0;
        year++;
      }
      Console.WriteLine(year);
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

  double depo, rate, tar;
  while (cin >> depo >> rate >> tar) {
    int year = 0;
    while (depo <= tar) {
      depo += depo * rate / 100;
      ++year;
    }
    cout << year << "\n";
  }

  return 0;
}
```
