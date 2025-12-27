---
layout: single
title: "[백준 28960] Плащ левитации (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 28960번 C#, C++ 풀이 - 로프 방향에 따른 투영 길이를 이용해 바닥에 닿지 않는지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 28960
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 28960, 백준 28960번, BOJ 28960, LevitationCloak, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[28960번 - Плащ левитации](https://www.acmicpc.net/problem/28960)

## 설명
직사각형 모양의 망토를 로프에 걸었을 때 바닥에 닿지 않는지 판단하는 문제입니다.

<br>

## 접근법
망토를 가로 또는 세로로 걸 수 있으므로 두 경우를 각각 확인합니다.

각 경우에 로프 방향 길이가 로프 길이 이하이고, 수직 방향 길이가 바닥까지 높이의 두 배 이하이면 바닥에 닿지 않습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var h = int.Parse(parts[0]);
    var l = int.Parse(parts[1]);
    var a = int.Parse(parts[2]);
    var b = int.Parse(parts[3]);

    if ((a <= l && b <= 2 * h) || (b <= l && a <= 2 * h))
      Console.WriteLine("YES");
    else Console.WriteLine("NO");
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

  int h, l, a, b; cin >> h >> l >> a >> b;

  if ((a <= l && b <= 2 * h) || (b <= l && a <= 2 * h))
    cout << "YES\n";
  else cout << "NO\n";

  return 0;
}
```
