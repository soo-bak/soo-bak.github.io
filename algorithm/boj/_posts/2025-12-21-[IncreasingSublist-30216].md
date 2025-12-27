---
layout: single
title: "[백준 30216] Increasing Sublist (C#, C++) - soo:bak"
date: "2025-12-21 20:42:00 +0900"
description: "백준 30216번 C#, C++ 풀이 - 연속 구간 중 Strictly Increasing한 최대 길이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 30216
  - C#
  - C++
  - 알고리즘
keywords: "백준 30216, 백준 30216번, BOJ 30216, IncreasingSublist, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30216번 - Increasing Sublist](https://www.acmicpc.net/problem/30216)

## 설명
리스트에서 연속한 구간 중 엄격히 증가하는 구간의 최대 길이를 구하는 문제입니다.

<br>

## 접근법
배열을 처음부터 끝까지 순회하면서 현재 증가 구간의 길이를 추적합니다. 이전 원소보다 크면 길이를 늘리고, 그렇지 않으면 1로 초기화합니다. 순회하면서 최대 길이를 갱신해 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var parts = Console.ReadLine()!.Split();
    var a = new int[n];
    for (var i = 0; i < n; i++)
      a[i] = int.Parse(parts[i]);

    var best = 1;
    var cur = 1;
    for (var i = 1; i < n; i++) {
      if (a[i] > a[i - 1]) cur++;
      else cur = 1;
      if (cur > best) best = cur;
    }

    Console.WriteLine(best);
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
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int best = 1, cur = 1;
  for (int i = 1; i < n; i++) {
    if (a[i] > a[i - 1]) cur++;
    else cur = 1;
    best = max(best, cur);
  }

  cout << best << "\n";

  return 0;
}
```
