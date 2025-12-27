---
layout: single
title: "[백준 23320] 홍익 절대평가 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 23320번 C#, C++ 풀이 - 상대평가와 절대평가 기준의 A학점 인원을 계산하는 문제"
tags:
  - 백준
  - BOJ
  - 23320
  - C#
  - C++
  - 알고리즘
keywords: "백준 23320, 백준 23320번, BOJ 23320, AbsoluteGrading, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23320번 - 홍익 절대평가](https://www.acmicpc.net/problem/23320)

## 설명
학생 점수와 상대평가 비율, 절대평가 기준 점수가 주어질 때 각각 A학점 인원을 구하는 문제입니다.

<br>

## 접근법
상대평가 A 인원은 `N * X / 100`으로 바로 계산할 수 있습니다.  
절대평가 A 인원은 점수 중 `Y` 이상인 개수를 세면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);

    var scores = new int[n];
    for (var i = 0; i < n; i++)
      scores[i] = int.Parse(parts[idx++]);

    var x = int.Parse(parts[idx++]);
    var y = int.Parse(parts[idx++]);

    var relative = n * x / 100;
    var absolute = 0;
    for (var i = 0; i < n; i++)
      if (scores[i] >= y) absolute++;

    Console.WriteLine($"{relative} {absolute}");
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
  vi scores(n);
  for (int i = 0; i < n; i++)
    cin >> scores[i];

  int x, y; cin >> x >> y;
  int relative = n * x / 100;
  int absolute = 0;
  for (int i = 0; i < n; i++)
    if (scores[i] >= y) absolute++;

  cout << relative << " " << absolute << "\n";

  return 0;
}
```
