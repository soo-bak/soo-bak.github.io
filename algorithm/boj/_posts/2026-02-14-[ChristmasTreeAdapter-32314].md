---
layout: single
title: "[백준 32314] Christmas Tree Adapter (C#, C++) - soo:bak"
date: "2026-02-14 21:24:00 +0900"
description: "백준 32314번 C#, C++ 풀이 - 전류 요구치와 후보 어댑터의 전류를 비교해 적합 여부를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 32314
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 32314, 백준 32314번, BOJ 32314, Christmas Tree Adapter, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32314번 - Christmas Tree Adapter](https://www.acmicpc.net/problem/32314)

## 설명
트리가 요구하는 전류 a와, 후보 어댑터의 전력 w, 전압 v가 주어졌을 때 어댑터의 전류 w/v가 a 이상이면 1, 아니면 0을 출력하는 문제입니다.

<br>

## 접근법
어댑터 전류 amp = w / v를 계산해 a와 비교하면 되는 단순한 문제입니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    int a = int.Parse(Console.ReadLine()!);
    var p = Console.ReadLine()!.Split();
    int w = int.Parse(p[0]);
    int v = int.Parse(p[1]);
    int amp = w / v;
    Console.WriteLine(amp >= a ? 1 : 0);
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

  int a, w, v; cin >> a >> w >> v;
  int amp = w / v;
  cout << (amp >= a ? 1 : 0) << "\n";
  return 0;
}
```
