---
layout: single
title: "[백준 4727] Close Enough Computations (C#, C++) - soo:bak"
date: "2026-04-06 21:44:00 +0900"
description: "백준 4727번 C#, C++ 풀이 - 반올림되기 전 실제 영양 성분 범위로 가능한 칼로리 구간을 확인하는 문제"
tags:
  - 백준
  - BOJ
  - 4727
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 4727, 백준 4727번, BOJ 4727, Close Enough Computations, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4727번 - Close Enough Computations](https://www.acmicpc.net/problem/4727)

## 설명
표시된 지방, 탄수화물, 단백질 그램 수와 칼로리가 모두 반올림된 값이라고 할 때, 실제 값들이 그 표기를 만들 수 있는지 판단하는 문제입니다.

<br>

## 접근법
정수로 표시된 그램 수 `g`가 있다면, 실제 값은 반올림 전 기준으로 `g - 0.5` 이상 `g + 0.5` 미만 범위에 있어야 합니다. 다만 그램 수는 음수가 될 수 없으므로 `0`인 경우 하한은 `0`입니다.

지방은 1그램당 `9`칼로리, 탄수화물과 단백질은 1그램당 `4`칼로리이므로, 각 영양소의 가능한 최소값과 최대값으로 전체 칼로리의 가능한 구간도 바로 구할 수 있습니다.

이 칼로리 구간이 표시된 칼로리가 반올림될 수 있는 구간과 겹치면 `yes`, 겹치지 않으면 `no`입니다. 구현에서는 `0.5`를 없애기 위해 모든 값을 `2`배 해서 정수로 계산하면 편합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    while (true) {
      string[] input = Console.ReadLine()!.Split();
      int calories = int.Parse(input[0]);
      int fat = int.Parse(input[1]);
      int carb = int.Parse(input[2]);
      int protein = int.Parse(input[3]);

      if (calories == 0 && fat == 0 && carb == 0 && protein == 0)
        break;

      int fatLow = Math.Max(0, fat * 2 - 1);
      int fatHigh = fat * 2 + 1;
      int carbLow = Math.Max(0, carb * 2 - 1);
      int carbHigh = carb * 2 + 1;
      int proteinLow = Math.Max(0, protein * 2 - 1);
      int proteinHigh = protein * 2 + 1;

      int minCalories = 9 * fatLow + 4 * carbLow + 4 * proteinLow;
      int maxCalories = 9 * fatHigh + 4 * carbHigh + 4 * proteinHigh;

      int labelLow = Math.Max(0, calories * 2 - 1);
      int labelHigh = calories * 2 + 1;

      bool possible = Math.Max(minCalories, labelLow) < Math.Min(maxCalories, labelHigh);
      Console.WriteLine(possible ? "yes" : "no");
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

  while (true) {
    int calories, fat, carb, protein;
    cin >> calories >> fat >> carb >> protein;

    if (calories == 0 && fat == 0 && carb == 0 && protein == 0)
      break;

    int fatLow = max(0, fat * 2 - 1);
    int fatHigh = fat * 2 + 1;
    int carbLow = max(0, carb * 2 - 1);
    int carbHigh = carb * 2 + 1;
    int proteinLow = max(0, protein * 2 - 1);
    int proteinHigh = protein * 2 + 1;

    int minCalories = 9 * fatLow + 4 * carbLow + 4 * proteinLow;
    int maxCalories = 9 * fatHigh + 4 * carbHigh + 4 * proteinHigh;

    int labelLow = max(0, calories * 2 - 1);
    int labelHigh = calories * 2 + 1;

    bool possible = max(minCalories, labelLow) < min(maxCalories, labelHigh);
    cout << (possible ? "yes" : "no") << "\n";
  }

  return 0;
}
```
