---
layout: single
title: "[백준 15995] 잉여역수 구하기 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: "백준 15995번 C#, C++ 풀이 - 확장 유클리드 알고리즘으로 최소 양의 잉여역수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 15995
  - C#
  - C++
  - 알고리즘
keywords: "백준 15995, 백준 15995번, BOJ 15995, ModularInverse, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[15995번 - 잉여역수 구하기](https://www.acmicpc.net/problem/15995)

## 설명
서로소인 두 수 a, m이 주어질 때 a의 법 m에서의 잉여역수를 구하는 문제입니다.

<br>

## 접근법
확장 유클리드 알고리즘으로 `a x + m y = 1`을 만족하는 x를 구합니다.  
이때 x가 a의 잉여역수이므로, `x mod m`을 양수 범위로 맞춰 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Egcd(int a, int b, out int x, out int y) {
    if (b == 0) {
      x = 1;
      y = 0;
      return a;
    }

    int x1, y1;
    int g = Egcd(b, a % b, out x1, out y1);
    x = y1;
    y = x1 - (a / b) * y1;
    return g;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var m = int.Parse(parts[1]);

    int x, y;
    Egcd(a, m, out x, out y);

    var ans = x % m;
    if (ans < 0) ans += m;
    Console.WriteLine(ans);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int egcd(int a, int b, int& x, int& y) {
  if (b == 0) {
    x = 1;
    y = 0;
    return a;
  }

  int x1, y1;
  int g = egcd(b, a % b, x1, y1);
  x = y1;
  y = x1 - (a / b) * y1;
  return g;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int a, m; cin >> a >> m;
  int x, y;
  egcd(a, m, x, y);

  int ans = x % m;
  if (ans < 0) ans += m;
  cout << ans << "\n";

  return 0;
}
```
