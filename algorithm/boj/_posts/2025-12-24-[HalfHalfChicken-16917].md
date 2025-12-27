---
layout: single
title: "[백준 16917] 양념 반 후라이드 반 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 16917번 C#, C++ 풀이 - 반반 치킨을 적절히 섞어 최소 비용을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 16917
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 16917, 백준 16917번, BOJ 16917, HalfHalfChicken, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16917번 - 양념 반 후라이드 반](https://www.acmicpc.net/problem/16917)

## 설명
양념과 후라이드를 최소 수량 이상 구매할 때 비용의 최솟값을 구하는 문제입니다.

<br>

## 접근법
반반 치킨 2마리로 양념 1마리와 후라이드 1마리를 대체할 수 있습니다.

반반 개수를 0부터 필요한 수량의 두 배까지 늘려가며 최소 비용을 갱신합니다.

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
    var c = int.Parse(parts[2]);
    var x = int.Parse(parts[3]);
    var y = int.Parse(parts[4]);

    var best = int.MaxValue;
    var limit = Math.Max(x, y) * 2;
    for (var i = 0; i <= limit; i += 2) {
      var needA = x - i / 2;
      var needB = y - i / 2;
      if (needA < 0) needA = 0;
      if (needB < 0) needB = 0;

      var cost = i * c + needA * a + needB * b;
      if (cost < best) best = cost;
    }

    Console.WriteLine(best);
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

  int a, b, c, x, y;
  cin >> a >> b >> c >> x >> y;

  int best = INT_MAX;
  int limit = max(x, y) * 2;
  for (int i = 0; i <= limit; i += 2) {
    int needA = x - i / 2;
    int needB = y - i / 2;
    if (needA < 0) needA = 0;
    if (needB < 0) needB = 0;

    int cost = i * c + needA * a + needB * b;
    if (cost < best) best = cost;
  }

  cout << best << "\n";

  return 0;
}
```
