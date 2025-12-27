---
layout: single
title: "[백준 15080] Every Second Counts (C#, C++) - soo:bak"
date: "2025-12-13 05:01:00 +0900"
description: 시작·종료 시각 hh:mm:ss를 초로 환산해 경과 시간을 계산하고 자정 넘김을 처리하는 백준 15080번 Every Second Counts 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 15080
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 15080, 백준 15080번, BOJ 15080, EverySecondCounts, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15080번 - Every Second Counts](https://www.acmicpc.net/problem/15080)

## 설명
시작 시각과 종료 시각이 주어질 때 경과 시간을 초 단위로 구하는 문제입니다.

<br>

## 접근법
각 시각을 초로 환산하여 차이를 구합니다.

종료 시각이 시작 시각보다 작으면 자정을 넘긴 것이므로 24시간을 더해 보정합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int ToSeconds(string time) {
    var parts = time.Split(' ');
    var h = int.Parse(parts[0]);
    var m = int.Parse(parts[2]);
    var s = int.Parse(parts[4]);
    return h * 3600 + m * 60 + s;
  }

  static void Main() {
    var start = ToSeconds(Console.ReadLine()!);
    var end = ToSeconds(Console.ReadLine()!);
    var diff = end - start;
    if (diff < 0) diff += 24 * 3600;
    Console.WriteLine(diff);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int toSeconds() {
  int h, m, s; char colon;
  cin >> h >> colon >> m >> colon >> s;
  return h * 3600 + m * 60 + s;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int start = toSeconds();
  int end = toSeconds();
  int diff = end - start;
  if (diff < 0) diff += 24 * 3600;
  cout << diff << "\n";

  return 0;
}
```
