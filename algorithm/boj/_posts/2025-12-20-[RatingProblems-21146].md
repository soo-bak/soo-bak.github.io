---
layout: single
title: "[백준 21146] Rating Problems (C#, C++) - soo:bak"
date: "2025-12-20 15:33:00 +0900"
description: "백준 21146번 C#, C++ 풀이 - 남은 심사위원 점수가 최소/최대로 들어올 때 가능한 전체 평균의 범위를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 21146
  - C#
  - C++
  - 알고리즘
keywords: "백준 21146, 백준 21146번, BOJ 21146, RatingProblems, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[21146번 - Rating Problems](https://www.acmicpc.net/problem/21146)

## 설명
총 n명의 심사위원 중 k명이 이미 점수를 주었을 때, 나머지 심사위원이 줄 수 있는 점수에 따라 가능한 전체 평균의 최솟값과 최댓값을 구하는 문제입니다.

각 심사위원은 -3부터 3 사이의 정수 점수를 줄 수 있습니다.

<br>

## 접근법
평균의 최솟값을 구하려면 아직 점수를 주지 않은 심사위원들이 모두 최저점인 -3을 주는 경우를 생각하면 됩니다. 반대로 최댓값은 모두 최고점인 3을 주는 경우입니다.

이미 받은 점수의 합에 남은 심사위원 수만큼 -3을 더하면 가능한 최소 총점이 되고, 3을 더하면 최대 총점이 됩니다. 각각을 전체 심사위원 수로 나누면 평균의 최솟값과 최댓값을 얻을 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var k = int.Parse(first[1]);

    var sum = 0;
    for (var i = 0; i < k; i++)
      sum += int.Parse(Console.ReadLine()!);

    var remaining = n - k;
    var minAvg = (sum - 3 * remaining) / (double)n;
    var maxAvg = (sum + 3 * remaining) / (double)n;

    Console.WriteLine($"{minAvg:F10} {maxAvg:F10}");
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

  int n, k;
  cin >> n >> k;

  int sum = 0;
  for (int i = 0; i < k; i++) {
    int r; cin >> r;
    sum += r;
  }

  int rem = n - k;
  double minAvg = (sum - 3 * rem) / (double)n;
  double maxAvg = (sum + 3 * rem) / (double)n;

  cout << fixed << setprecision(10) << minAvg << " " << maxAvg << "\n";

  return 0;
}
```
