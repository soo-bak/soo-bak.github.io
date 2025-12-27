---
layout: single
title: "[백준 30204] 병영외 급식 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: "백준 30204번 C#, C++ 풀이 - 전체 인원 합이 X로 나누어떨어지는지 확인하는 문제"
tags:
  - 백준
  - BOJ
  - 30204
  - C#
  - C++
  - 알고리즘
  - 수학
  - 애드혹
  - arithmetic
keywords: "백준 30204, 백준 30204번, BOJ 30204, BarracksCatering, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30204번 - 병영외 급식](https://www.acmicpc.net/problem/30204)

## 설명
생활관들을 하나 이상 묶어 각 그룹 인원이 X의 배수가 되게 할 수 있는지 판단하는 문제입니다.

<br>

## 접근법
모든 생활관을 하나의 그룹으로 묶는 것이 항상 가능하므로, 전체 인원 합이 X로 나누어떨어지는지만 확인하면 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var first = Console.ReadLine()!.Split();
    var n = int.Parse(first[0]);
    var x = int.Parse(first[1]);

    var parts = Console.ReadLine()!.Split();
    var sum = 0;
    for (var i = 0; i < n; i++)
      sum += int.Parse(parts[i]);

    Console.WriteLine(sum % x == 0 ? 1 : 0);
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

  int n, x; cin >> n >> x;
  int sum = 0;
  for (int i = 0; i < n; i++) {
    int v; cin >> v;
    sum += v;
  }

  cout << (sum % x == 0 ? 1 : 0) << "\n";

  return 0;
}
```
