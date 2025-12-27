---
layout: single
title: "[백준 32306] Basketball Score (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32306번 C#, C++ 풀이 - 1, 2, 3점 슛 개수로 두 팀의 총점을 비교하는 문제"
tags:
  - 백준
  - BOJ
  - 32306
  - C#
  - C++
  - 알고리즘
keywords: "백준 32306, 백준 32306번, BOJ 32306, BasketballScore, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32306번 - Basketball Score](https://www.acmicpc.net/problem/32306)

## 설명
두 팀의 1, 2, 3점 슛 개수로 총점을 계산해 승패를 출력하는 문제입니다.

<br>

## 접근법
각 팀의 총점은 1점 슛 개수에 1을, 2점 슛 개수에 2를, 3점 슛 개수에 3을 곱해 모두 더하면 됩니다.

이후 총점이 더 큰 팀 번호를 출력하고, 같으면 0을 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var a = Console.ReadLine()!.Split();
    var b = Console.ReadLine()!.Split();

    var s1 = int.Parse(a[0]) + 2 * int.Parse(a[1]) + 3 * int.Parse(a[2]);
    var s2 = int.Parse(b[0]) + 2 * int.Parse(b[1]) + 3 * int.Parse(b[2]);

    if (s1 > s2) Console.WriteLine(1);
    else if (s2 > s1) Console.WriteLine(2);
    else Console.WriteLine(0);
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

  int a1, a2, a3; cin >> a1 >> a2 >> a3;
  int b1, b2, b3; cin >> b1 >> b2 >> b3;

  int s1 = a1 + 2 * a2 + 3 * a3;
  int s2 = b1 + 2 * b2 + 3 * b3;

  if (s1 > s2) cout << 1 << "\n";
  else if (s2 > s1) cout << 2 << "\n";
  else cout << 0 << "\n";

  return 0;
}
```
