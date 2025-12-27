---
layout: single
title: "[백준 5928] Contest Timing (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: 2011-11-11 11:11을 기준으로 종료 시각까지의 경과 분을 계산하고, 이전이면 -1을 출력하는 백준 5928번 Contest Timing 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 5928
  - C#
  - C++
  - 알고리즘
keywords: "백준 5928, 백준 5928번, BOJ 5928, ContestTiming, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5928번 - Contest Timing](https://www.acmicpc.net/problem/5928)

## 설명
대회 시작 시각인 2011년 11월 11일 11:11부터 종료 시각까지의 경과 시간을 분 단위로 구하는 문제입니다.

<br>

## 접근법
먼저 시작 시각과 종료 시각을 모두 분으로 환산합니다.

시작 시각은 11일 × 24 × 60 + 11 × 60 + 11분이고, 종료 시각도 같은 방식으로 계산합니다.

두 값의 차이가 음수면 -1, 아니면 그 차이를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var d = int.Parse(line[0]);
    var h = int.Parse(line[1]);
    var m = int.Parse(line[2]);

    int start = 11 * 24 * 60 + 11 * 60 + 11;
    int end = d * 24 * 60 + h * 60 + m;
    int diff = end - start;
    Console.WriteLine(diff < 0 ? -1 : diff);
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

  int d, h, m; cin >> d >> h >> m;
  int start = 11 * 24 * 60 + 11 * 60 + 11;
  int end = d * 24 * 60 + h * 60 + m;
  int diff = end - start;
  cout << (diff < 0 ? -1 : diff) << "\n";

  return 0;
}
```
