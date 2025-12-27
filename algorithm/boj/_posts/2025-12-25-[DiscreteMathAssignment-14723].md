---
layout: single
title: "[백준 14723] 이산수학 과제 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: "백준 14723번 C#, C++ 풀이 - 대각선 순서로 열거되는 유리수에서 N번째 항을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 14723
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
keywords: "백준 14723, 백준 14723번, BOJ 14723, DiscreteMathAssignment, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14723번 - 이산수학 과제](https://www.acmicpc.net/problem/14723)

## 설명
분자+분모가 같은 항들을 한 대각선으로 묶고, 각 대각선에서 분자가 큰 것부터 나열할 때 N번째 유리수를 찾는 문제입니다.

<br>

## 접근법
대각선 길이는 1, 2, 3, ... 순서로 늘어납니다.  
누적합이 N을 넘는 첫 대각선 길이를 k라고 하면, 그 대각선에서의 위치는 `idx = N - (k-1)k/2`입니다.  
분자는 `k - idx + 1`, 분모는 `idx`가 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var k = 1;
    var sum = 1;

    while (sum < n) {
      k++;
      sum += k;
    }

    var prev = sum - k;
    var idx = n - prev;
    var a = k - idx + 1;
    var b = idx;

    Console.WriteLine($"{a} {b}");
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

  int n; cin >> n;
  int k = 1, sum = 1;

  while (sum < n) {
    k++;
    sum += k;
  }

  int prev = sum - k;
  int idx = n - prev;
  int a = k - idx + 1;
  int b = idx;

  cout << a << " " << b << "\n";

  return 0;
}
```
