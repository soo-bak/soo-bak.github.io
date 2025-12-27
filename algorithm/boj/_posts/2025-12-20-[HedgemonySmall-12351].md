---
layout: single
title: "[백준 12351] Hedgemony (Small) (C#, C++) - soo:bak"
date: "2025-12-20 16:02:00 +0900"
description: "백준 12351번 C#, C++ 풀이 - 양끝 평균 이하가 될 때만 깎는 규칙을 따라가며 끝에서 두 번째 덤불 높이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 12351
  - C#
  - C++
  - 알고리즘
keywords: "백준 12351, 백준 12351번, BOJ 12351, HedgemonySmall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12351번 - Hedgemony (Small)](https://www.acmicpc.net/problem/12351)

## 설명
N개의 덤불 높이가 주어질 때, 양끝을 제외한 덤불들을 순서대로 확인하여 양옆 평균보다 높으면 그 평균으로 깎는 문제입니다. 과정을 마친 뒤 끝에서 두 번째 덤불의 높이를 출력합니다.

<br>

## 접근법
두 번째 덤불부터 끝에서 두 번째 덤불까지 순서대로 처리합니다. 각 덤불에 대해 왼쪽과 오른쪽 덤불 높이의 평균을 계산하고, 현재 덤불이 그 평균보다 높으면 평균으로 깎습니다.

한 번 순회하면서 갱신하면 되므로, 최종적으로 끝에서 두 번째 덤불의 높이를 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 1; tc <= t; tc++) {
      var n = int.Parse(Console.ReadLine()!);
      var h = Console.ReadLine()!.Split().Select(double.Parse).ToArray();

      for (var i = 1; i < n - 1; i++) {
        var avg = (h[i - 1] + h[i + 1]) / 2.0;
        if (h[i] > avg) h[i] = avg;
      }

      Console.WriteLine($"Case #{tc}: {h[n - 2]:F6}");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<double> vd;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  for (int tc = 1; tc <= t; tc++) {
    int n; cin >> n;
    vd h(n);
    for (int i = 0; i < n; i++)
      cin >> h[i];

    for (int i = 1; i + 1 < n; i++) {
      double avg = (h[i - 1] + h[i + 1]) / 2.0;
      if (h[i] > avg) h[i] = avg;
    }

    cout << fixed << setprecision(6);
    cout << "Case #" << tc << ": " << h[n - 2] << "\n";
  }

  return 0;
}
```
