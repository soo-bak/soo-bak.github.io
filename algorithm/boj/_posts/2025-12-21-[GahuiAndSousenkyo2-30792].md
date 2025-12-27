---
layout: single
title: "[백준 30792] gahui and sousenkyo 2 (C#, C++) - soo:bak"
date: "2025-12-21 21:51:00 +0900"
description: "백준 30792번 C#, C++ 풀이 - 지지 캐릭터의 득표 수보다 높은 득표 수를 센 뒤 등수를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 30792
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 30792, 백준 30792번, BOJ 30792, GahuiAndSousenkyo2, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30792번 - gahui and sousenkyo 2](https://www.acmicpc.net/problem/30792)

## 설명
지지하는 캐릭터의 득표 수가 주어질 때, 더 많은 득표 수를 가진 캐릭터 수를 이용해 등수를 구하는 문제입니다.

<br>

## 접근법
지지 캐릭터보다 득표 수가 큰 캐릭터의 수를 세고, 그 값에 1을 더하면 등수가 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var g = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();

    var higher = 0;
    for (var i = 0; i < n - 1; i++) {
      var v = int.Parse(parts[i]);
      if (v > g) higher++;
    }

    Console.WriteLine(higher + 1);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  int g; cin >> g;

  vi a(n - 1);
  for (int i = 0; i < n - 1; i++)
    cin >> a[i];

  int higher = 0;
  for (int i = 0; i < n - 1; i++) {
    if (a[i] > g) higher++;
  }

  cout << higher + 1 << "\n";

  return 0;
}
```
