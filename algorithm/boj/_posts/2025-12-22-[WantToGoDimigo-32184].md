---
layout: single
title: "[백준 32184] 디미고에 가고 싶어! (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 32184번 C#, C++ 풀이 - 연속 페이지에서 한 장 또는 펼친 면으로 찍을 때 필요한 최소 촬영 횟수 계산"
tags:
  - 백준
  - BOJ
  - 32184
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 32184, 백준 32184번, BOJ 32184, WantToGoDimigo, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32184번 - 디미고에 가고 싶어!](https://www.acmicpc.net/problem/32184)

## 설명
책자의 A페이지부터 B페이지까지를 빠짐없이 저장하기 위한 최소 촬영 횟수를 구하는 문제입니다.

<br>

## 접근법
펼친 면은 홀수와 짝수 한 쌍이므로, 범위 안에 완전히 포함되는 펼친 면은 모두 한 번에 찍는 것이 이득입니다.

전체 페이지 수에서 범위에 완전히 포함된 펼친 면의 개수만큼 줄이면 최소 횟수가 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);

    var total = b - a + 1;
    var spreads = b / 2 - a / 2;
    Console.WriteLine(total - spreads);
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

  int a, b; cin >> a >> b;
  int total = b - a + 1;
  int spreads = b / 2 - a / 2;
  cout << total - spreads << "\n";

  return 0;
}
```
