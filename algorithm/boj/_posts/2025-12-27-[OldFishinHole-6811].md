---
layout: single
title: "[백준 6811] Old Fishin’ Hole (C#, C++) - soo:bak"
date: "2025-12-27 10:45:00 +0900"
description: 주어진 점수 한도 내에서 갈색송어, 노던파이크, 옐로피컬을 잡는 모든 조합과 개수를 출력하는 문제
tags:
  - 백준
  - BOJ
  - 6811
  - C#
  - C++
  - 알고리즘
keywords: "백준 6811, 백준 6811번, BOJ 6811, OldFishinHole, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6811번 - Old Fishin’ Hole](https://www.acmicpc.net/problem/6811)

## 설명
세 종류의 물고기마다 점수가 주어지고 최대 허용 점수가 있습니다. 최소 한 마리 이상 잡으면서 허용 점수 이하인 모든 조합을 출력하는 문제입니다.

<br>

## 접근법
각 물고기 수를 0부터 가능한 최대치까지 삼중 반복으로 탐색합니다.

총점이 허용 범위 내이고 최소 한 마리 이상이면 출력하고 개수를 셉니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var p = int.Parse(Console.ReadLine()!);
    var w = int.Parse(Console.ReadLine()!);
    var lim = int.Parse(Console.ReadLine()!);

    var ways = 0;
    for (var a = 0; a * t <= lim; a++) {
      for (var b = 0; a * t + b * p <= lim; b++) {
        for (var c = 0; a * t + b * p + c * w <= lim; c++) {
          if (a == 0 && b == 0 && c == 0) continue;
          var total = a * t + b * p + c * w;
          if (total <= lim) {
            Console.WriteLine($"{a} Brown Trout, {b} Northern Pike, {c} Yellow Pickerel");
            ways++;
          } else break;
        }
      }
    }
    Console.WriteLine($"Number of ways to catch fish: {ways}");
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

  int t, p, w, lim;
  cin >> t >> p >> w >> lim;

  int ways = 0;
  for (int a = 0; a * t <= lim; a++) {
    for (int b = 0; a * t + b * p <= lim; b++) {
      for (int c = 0; a * t + b * p + c * w <= lim; c++) {
        if (a == 0 && b == 0 && c == 0) continue;
        cout << a << " Brown Trout, " << b << " Northern Pike, " << c << " Yellow Pickerel\n";
        ways++;
      }
    }
  }
  cout << "Number of ways to catch fish: " << ways << "\n";

  return 0;
}
```
