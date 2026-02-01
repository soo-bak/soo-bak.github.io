---
layout: single
title: "[백준 21301] Comfy Deviations (C#, C++) - soo:bak"
date: "2026-02-01 00:00:00 +0900"
description: "백준 21301번 C#, C++ 풀이 - 10개 온도의 표준편차가 1.0 이하인지 판단하는 문제"
tags:
  - 백준
  - BOJ
  - 21301
  - C#
  - C++
  - 알고리즘
  - 구현
  - 수학
keywords: "백준 21301, 백준 21301번, BOJ 21301, Comfy Deviations, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[21301번 - Comfy Deviations](https://www.acmicpc.net/problem/21301)

## 설명
온도 10개가 주어질 때 표준편차를 계산해 1.0 이하이면 COMFY, 크면 NOT COMFY를 출력하는 문제입니다.

<br>

## 접근법
10개의 온도 평균을 구하고, 각 값에서 평균을 뺀 제곱을 더한 뒤 (n-1)로 나누고 제곱근을 취해 표준편차를 얻습니다.

표준편차가 1.0 이하이면 COMFY, 초과하면 NOT COMFY를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    const int n = 10;
    var v = new double[n];
    double sum = 0;
    for (int i = 0; i < n; i++) {
      v[i] = double.Parse(parts[i]);
      sum += v[i];
    }
    double mean = sum / n;
    double sq = 0;
    for (int i = 0; i < n; i++) {
      double d = v[i] - mean;
      sq += d * d;
    }
    double st = Math.Sqrt(sq / (n - 1));
    Console.WriteLine(st <= 1.0 ? "COMFY" : "NOT COMFY");
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

  const int n = 10;
  double v[n], sum = 0;
  for (int i = 0; i < n; i++) {
    cin >> v[i];
    sum += v[i];
  }
  double mean = sum / n;
  double sq = 0;
  for (int i = 0; i < n; i++) {
    double d = v[i] - mean;
    sq += d * d;
  }
  double st = sqrt(sq / (n - 1));
  cout << (st <= 1.0 ? "COMFY" : "NOT COMFY") << "\n";
  return 0;
}
```
