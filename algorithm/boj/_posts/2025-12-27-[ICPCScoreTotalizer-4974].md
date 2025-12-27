---
layout: single
title: "[백준 4974] ICPC Score Totalizer Software (C#, C++) - soo:bak"
date: "2025-12-27 10:25:00 +0900"
description: "백준 4974번 C#, C++ 풀이 - 최고점 1개와 최저점 1개를 제외한 점수 평균의 내림 값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 4974
  - C#
  - C++
  - 알고리즘
keywords: "백준 4974, 백준 4974번, BOJ 4974, ICPCScoreTotalizer, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4974번 - ICPC Score Totalizer Software](https://www.acmicpc.net/problem/4974)

## 설명
여러 심사 점수 중 최고점 하나와 최저점 하나를 제외한 평균을 구하는 문제입니다. 소수점 이하는 버립니다.

<br>

## 접근법
모든 점수의 합에서 최고점과 최저점을 뺀 뒤, 남은 개수로 나눕니다. 같은 값이 여러 개여도 하나씩만 제외합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    string? line;
    while ((line = Console.ReadLine()) != null) {
      if (line.Trim() == "0") break;
      var n = int.Parse(line);
      int min = int.MaxValue, max = int.MinValue;
      long sum = 0;
      for (var i = 0; i < n; i++) {
        var s = int.Parse(Console.ReadLine()!);
        sum += s;
        if (s < min) min = s;
        if (s > max) max = s;
      }
      var avg = (sum - min - max) / (n - 2);
      Console.WriteLine(avg);
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  while (cin >> n) {
    if (n == 0) break;
    int mn = INT_MAX, mx = INT_MIN;
    ll sum = 0;
    for (int i = 0; i < n; i++) {
      int s; cin >> s;
      sum += s;
      mn = min(mn, s);
      mx = max(mx, s);
    }
    cout << (sum - mn - mx) / (n - 2) << "\n";
  }

  return 0;
}
```
