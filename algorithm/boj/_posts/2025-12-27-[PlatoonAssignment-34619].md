---
layout: single
title: "[백준 34619] 소대 배정 (C#, C++) - soo:bak"
date: "2025-12-27 13:55:00 +0900"
description: "백준 34619번 C#, C++ 풀이 - k번째 입소자가 배정될 중대와 소대를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 34619
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - 브루트포스
  - arithmetic
keywords: "백준 34619, 백준 34619번, BOJ 34619, PlatoonAssignment, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[34619번 - 소대 배정](https://www.acmicpc.net/problem/34619)

## 설명
중대, 소대, 소대 정원이 정해져 있을 때 입소 순서대로 배정합니다. 특정 순번의 입소자가 배정될 중대와 소대를 구하는 문제입니다.

<br>

## 접근법
입소 순번에서 1을 빼고 소대 정원으로 나누면 전체 소대 중 몇 번째인지 알 수 있습니다.

이 값을 중대당 소대 수로 나누고 나머지를 구하면 중대와 소대 번호를 얻습니다.

<br>

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = long.Parse(parts[0]);
    var b = long.Parse(parts[1]);
    var n = long.Parse(parts[2]);
    var k = long.Parse(parts[3]);

    var platoonIdx = (k - 1) / n;
    var company = platoonIdx / b + 1;
    var platoon = platoonIdx % b + 1;

    Console.WriteLine($"{company} {platoon}");
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long ll;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  ll a, b, n, k; cin >> a >> b >> n >> k;

  ll platoonIdx = (k - 1) / n;
  ll company = platoonIdx / b + 1;
  ll platoon = platoonIdx % b + 1;

  cout << company << " " << platoon << "\n";

  return 0;
}
```
