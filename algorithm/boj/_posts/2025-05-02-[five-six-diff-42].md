---
layout: single
title: "[백준 2864] 5와 6의 차이 (C#, C++) - soo:bak"
date: "2025-05-02 18:33:00 +0900"
description: 숫자에 포함된 5와 6의 인식 혼동으로 만들어질 수 있는 합의 최소값과 최대값을 구하는 백준 2864번 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 2864
  - C#
  - C++
  - 알고리즘
  - 수학
  - 그리디
  - 문자열
  - arithmetic
keywords: "백준 2864, 백준 2864번, BOJ 2864, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[2864번 - 5와 6의 차이](https://www.acmicpc.net/problem/2864)

## 설명
두 수가 주어졌을 때, 해당 수에 포함된 `5`와 `6`이 혼동될 수 있다고 가정합니다.

즉, `5`를 `6`으로, `6`을 `5`로 인식할 수 있다고 할 때 각각의 수가 가질 수 있는 **최솟값과 최댓값**을 계산한 뒤,

두 수의 가능한 합 중 **최솟값과 최댓값**을 출력하는 문제입니다.

예를 들어, `56`이라는 숫자는 다음 두 가지로 해석될 수 있습니다:
- `최솟값`: 55 (모든 `6`을 `5`로 인식)
- `최댓값`: 66 (모든 `5`를 `6`으로 인식)

<br>

## 접근법

- 입력으로 주어진 두 수를 문자열로 처리하여 `5 ↔ 6` 변환을 적용합니다.
- 최소값을 구할 땐 모든 `6`을 `5`로, <br>
  최대값을 구할 땐 모든 `5`를 `6`으로 바꾸어 각각 새로운 수를 만듭니다.
- 각 케이스에 대해 두 수를 더한 값을 계산하고, 최솟값과 최댓값을 차례로 출력합니다.

<br>

## Code

### C#

```csharp
using System;

class Program {
  static void Main() {
    var input = Console.ReadLine().Split();
    string num1 = input[0], num2 = input[1];

    string min1 = num1.Replace('6', '5');
    string min2 = num2.Replace('6', '5');
    string max1 = num1.Replace('5', '6');
    string max2 = num2.Replace('5', '6');

    int minSum = int.Parse(min1) + int.Parse(min2);
    int maxSum = int.Parse(max1) + int.Parse(max2);

    Console.WriteLine($"{minSum} {maxSum}");
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

  string num1, num2; cin >> num1 >> num2;

  string min1 = num1, min2 = num2, max1 = num1, max2 = num2;
  for (char &c : min1) if (c == '6') c = '5';
  for (char &c : min2) if (c == '6') c = '5';
  for (char &c : max1) if (c == '5') c = '6';
  for (char &c : max2) if (c == '5') c = '6';

  cout << stoi(min1) + stoi(min2) << " " << stoi(max1) + stoi(max2) << "\n";

  return 0;
}
```
