---
layout: single
title: "[백준 29738] Goodbye, Code Jam (C#, C++) - soo:bak"
date: "2025-12-20 12:12:00 +0900"
description: "백준 29738번 C#, C++ 풀이 - 마지막 등수 N에 따라 참가자가 머문 라운드를 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 29738
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 29738, 백준 29738번, BOJ 29738, GoodbyeCodeJam, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[29738번 - Goodbye, Code Jam](https://www.acmicpc.net/problem/29738)

## 설명
참가자의 마지막 라운드에서의 등수 n이 주어질 때, 마지막으로 참여한 라운드를 출력하는 문제입니다.

<br>
각 라운드의 진출 조건은 Round 1에서 상위 4500명, Round 2에서 상위 1000명, Round 3에서 상위 25명이 다음 라운드로 진출합니다.

<br>

## 접근법
등수에 따라 분기합니다. 25 이하면 World Finals, 1000 이하면 Round 3, 4500 이하면 Round 2, 그 외는 Round 1입니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var tc = 1; tc <= t; tc++) {
      var n = int.Parse(Console.ReadLine()!);
      var res = "";
      if (n <= 25) res = "World Finals";
      else if (n <= 1000) res = "Round 3";
      else if (n <= 4500) res = "Round 2";
      else res = "Round 1";

      Console.WriteLine($"Case #{tc}: {res}");
    }
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

  int t; cin >> t;
  for (int tc = 1; tc <= t; tc++) {
    int n; cin >> n;
    string res;
    if (n <= 25) res = "World Finals";
    else if (n <= 1000) res = "Round 3";
    else if (n <= 4500) res = "Round 2";
    else res = "Round 1";

    cout << "Case #" << tc << ": " << res << "\n";
  }

  return 0;
}
```
