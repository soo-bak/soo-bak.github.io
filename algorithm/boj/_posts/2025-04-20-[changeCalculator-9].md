---
layout: single
title: "[백준 2720] 세탁소 사장 동혁 (C#, C++) - soo:bak"
date: "2025-04-20 01:09:00 +0900"
description: 거스름돈을 쿼터, 다임, 니켈, 페니 단위로 최소 개수로 나누는 백준 2720번 세탁소 사장 동혁 문제의 C# 및 C++ 풀이 및 해설
tags:
  - 백준
  - BOJ
  - 2720
  - C#
  - C++
  - 알고리즘
keywords: "백준 2720, 백준 2720번, BOJ 2720, changeCalculator, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2720번 - 세탁소 사장 동혁](https://www.acmicpc.net/problem/2720)

## 설명
**입력으로 주어진 거스름돈을 미국 동전 단위인 쿼터($0.25), 다임($0.10), 니켈($0.05), 페니($0.01)로 최소 개수로 나누어 출력하는 구현 문제**입니다.
<br>

- 테스트케이스의 개수가 주어진 후, 각 테스트케이스마다 하나의 거스름돈 액수가 주어집니다.
- 이 금액을 `25`, `10`, `5`, `1` 센트 단위로 나누되, **각 동전의 개수는 최소가 되도록** 분배해야 합니다.
- 각 테스트케이스마다 4개의 정수를 한 줄에 출력합니다.
  - 순서: 쿼터($0.25), 다임($0.10), 니켈($0.05), 페니($0.01)
  - 동전 개수는 공백으로 구분하여 출력합니다.

## 접근법

1. 테스트케이스 개수를 입력받습니다.
2. 각 테스트케이스마다:
   - 먼저 `25`로 나눈 몫을 구하고 출력
   - 나머지를 다시 `10`으로 나눈 몫을 구하고 출력
   - 이후 `5`, `1`로 반복
3. 나눈 후 나머지는 다음 동전 단위 계산에 사용됩니다.
4. 각 테스트케이스 결과는 한 줄로 출력합니다.

- **그리디 알고리즘의 기초적인 형태**로, 큰 단위부터 순차적으로 나누는 것이 항상 최적입니다.
- 동전 단위가 서로 배수 관계이기 때문에 그리디 방식이 항상 정답을 보장합니다.

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int t = int.Parse(Console.ReadLine());

    while (t-- > 0) {
      int sum = int.Parse(Console.ReadLine());

      Console.Write($"{sum / 25} ");
      sum %= 25;
      Console.Write($"{sum / 10} ");
      sum %= 10;
      Console.Write($"{sum / 5} ");
      sum %= 5;
      Console.WriteLine($"{sum / 1}");
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

  int t; cin >> t;
  while (t--) {
    int sum; cin >> sum;
    cout << sum / 25 << " ";
    sum %= 25;
    cout << sum / 10 << " ";
    sum %= 10;
    cout << sum / 5 << " ";
    sum %= 5;
    cout << sum / 1 << "\n";
  }
  return 0;
}
```
