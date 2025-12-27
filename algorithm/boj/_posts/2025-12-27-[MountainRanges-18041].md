---
layout: single
title: "[백준 18041] Mountain Ranges (C#, C++) - soo:bak"
date: "2025-12-27 07:35:00 +0900"
description: "백준 18041번 C#, C++ 풀이 - 인접 고도 차이가 X 이내인 최장 연속 구간의 길이를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 18041
  - C#
  - C++
  - 알고리즘
keywords: "백준 18041, 백준 18041번, BOJ 18041, MountainRanges, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18041번 - Mountain Ranges](https://www.acmicpc.net/problem/18041)

## 설명
고도가 비내림차순으로 주어진 N개의 전망대가 있을 때, 인접한 전망대로 이동할 때마다 상승량이 X를 넘지 않아야 계속 이동합니다. 시작 지점을 자유롭게 선택할 때 방문할 수 있는 최대 전망대 수를 구하는 문제입니다.

<br>

## 접근법
연속한 두 고도의 차이가 X 이하이면 구간을 이어가고, 초과하면 구간을 끊습니다.

한 번의 순회로 현재 구간 길이를 유지하며 최댓값을 갱신하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split().Select(int.Parse).ToArray();
    int n = first[0], x = first[1];
    var arr = Console.ReadLine()!.Split().Select(int.Parse).ToArray();

    int best = 1, cur = 1;
    for (int i = 1; i < n; i++) {
      if (arr[i] - arr[i - 1] <= x) cur++;
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

  int n, x; cin >> n >> x;
  vi a(n);
  for (int i = 0; i < n; i++)
    cin >> a[i];

  int best = 1, cur = 1;
  for (int i = 1; i < n; i++) {
    if (a[i] - a[i - 1] <= x) cur++;
    else cur = 1;

    if (cur > best) best = cur;
  }

  cout << best << "\n";
  return 0;
}
```
