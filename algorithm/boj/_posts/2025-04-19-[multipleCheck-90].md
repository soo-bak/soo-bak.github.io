---
layout: single
title: "[백준 4504] 배수 찾기 (C#, C++) - soo:bak"
date: "2025-04-19 22:49:00 +0900"
description: "입력된 수들이 특정 수의 배수인지 여부를 판단하는 간단한 조건 검사 문제인 백준 4504번 배수 찾기 문제의 C# 및 C++ 풀이 및 해설"
tags:
  - 백준
  - BOJ
  - 4504
  - C#
  - C++
  - 알고리즘
keywords: "백준 4504, 백준 4504번, BOJ 4504, multipleCheck, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4504번 - 배수 찾기](https://www.acmicpc.net/problem/4504)

## 설명
**기준이 되는 수를 입력받고, 이후 들어오는 여러 수들이 그 수의 배수인지 여부를 판별하는 문제**입니다.<br>

- 첫 번째 줄에 기준이 되는 정수 `n`이 주어집니다.<br>
- 이후 한 줄에 하나씩 수가 주어지며, 이 수가 `0`일 경우 입력이 종료됩니다.<br>
- 각 수가 `n`의 배수이면 `is a multiple of` 형식으로 출력하고, 아니라면 `is NOT a multiple of` 형식으로 출력합니다.<br>

입력이 종료될 때까지 계속해서 조건을 검사하고, 문제에서 요구하는 형식대로 출력합니다.<br>

## 접근법

1. 먼저 기준이 되는 정수 `n`을 입력받습니다.<br>
2. 이후 반복문을 이용하여 수를 계속 입력받고, 입력된 수가 `0`이면 반복을 종료합니다.<br>
3. 각 수에 대해 나머지가 존재하는지 검사하여 배수 여부를 판단합니다.<br>
4. 결과를 출력 형식에 맞게 출력합니다.<br>

## Code

[ C# ]

```csharp
using System;

class Program {
  static void Main() {
    int div = int.Parse(Console.ReadLine());
    while (true) {
      int num = int.Parse(Console.ReadLine());
      if (num == 0) break;

      if (num % div == 0)
        Console.WriteLine($"{num} is a multiple of {div}.");
      else
        Console.WriteLine($"{num} is NOT a multiple of {div}.");
    }
  }
}
```

[ C++ ]

```cpp
#include <bits/stdc++.h>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int div; cin >> div;
  while (true) {
    int num; cin >> num;
    if (num == 0) break ;

    if (num % div == 0)
      cout << num << " is a multiple of " << div << ".\n";
    else
      cout << num << " is NOT a multiple of " << div << ".\n";
  }

  return 0;
}
```
