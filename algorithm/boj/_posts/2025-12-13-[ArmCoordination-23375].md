---
layout: single
title: "[백준 23375] Arm Coordination (C#, C++) - soo:bak"
date: "2025-12-13 00:03:00 +0900"
description: 원의 중심과 반지름이 주어질 때 이를 덮는 최소 축정렬 정사각형의 네 꼭짓점을 출력하는 백준 23375번 Arm Coordination 문제의 C# 및 C++ 풀이와 해설
tags:
  - 백준
  - BOJ
  - 23375
  - C#
  - C++
  - 알고리즘
  - 수학
  - 기하학
  - arithmetic
keywords: "백준 23375, 백준 23375번, BOJ 23375, ArmCoordination, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[23375번 - Arm Coordination](https://www.acmicpc.net/problem/23375)

## 설명
원의 중심과 반지름이 주어질 때, 원을 완전히 포함하는 최소 크기의 축 정렬 정사각형의 꼭짓점을 구하는 문제입니다.

<br>

## 접근법
원을 포함하는 가장 작은 정사각형의 한 변 길이는 지름과 같습니다.

중심에서 상하좌우로 반지름만큼 떨어진 네 점이 정사각형의 꼭짓점이 됩니다.

이 네 점을 시계 방향 또는 반시계 방향 순서로 출력하면 됩니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var line = Console.ReadLine()!.Split();
    var x = int.Parse(line[0]);
    var y = int.Parse(line[1]);
    var r = int.Parse(Console.ReadLine()!);

    Console.WriteLine($"{x - r} {y + r}");
    Console.WriteLine($"{x + r} {y + r}");
    Console.WriteLine($"{x + r} {y - r}");
    Console.WriteLine($"{x - r} {y - r}");
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

  int x, y, r; cin >> x >> y >> r;
  cout << x - r << " " << y + r << "\n";
  cout << x + r << " " << y + r << "\n";
  cout << x + r << " " << y - r << "\n";
  cout << x - r << " " << y - r << "\n";

  return 0;
}
```
