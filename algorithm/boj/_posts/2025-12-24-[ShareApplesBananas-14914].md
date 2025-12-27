---
layout: single
title: "[백준 14914] 사과와 바나나 나눠주기 (C#, C++) - soo:bak"
date: "2025-12-24 22:35:00 +0900"
description: "백준 14914번 C#, C++ 풀이 - 공평하게 나눌 수 있는 친구 수와 분배량을 모두 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 14914
  - C#
  - C++
  - 알고리즘
  - 수학
  - 브루트포스
  - arithmetic
keywords: "백준 14914, 백준 14914번, BOJ 14914, ShareApplesBananas, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[14914번 - 사과와 바나나 나눠주기](https://www.acmicpc.net/problem/14914)

## 설명
사과와 바나나를 공평하게 나눌 수 있는 모든 경우를 출력하는 문제입니다.

<br>

## 접근법
친구 수는 a와 b의 공약수여야 합니다.

따라서 gcd를 구한 뒤, 1부터 gcd까지의 모든 약수를 확인해 가능한 분배를 출력합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Gcd(int x, int y) {
    while (y != 0) {
      var t = x % y;
      x = y;
      y = t;
    }
    return x;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var a = int.Parse(parts[0]);
    var b = int.Parse(parts[1]);

    var g = Gcd(a, b);
    for (var k = 1; k <= g; k++) {
      if (g % k != 0) continue;
      Console.WriteLine($"{k} {a / k} {b / k}");
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

  int a, b; cin >> a >> b;
  int g = gcd(a, b);
  for (int k = 1; k <= g; k++) {
    if (g % k != 0) continue;
    cout << k << " " << a / k << " " << b / k << "\n";
  }

  return 0;
}
```
