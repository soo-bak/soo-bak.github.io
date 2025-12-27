---
layout: single
title: "[백준 16625] Das Blinkenlights (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 16625번 C#, C++ 풀이 - 두 주기 p, q의 최소공배수가 s 이하인지 판단해 동시에 깜빡임 여부를 출력하는 문제"
tags:
  - 백준
  - BOJ
  - 16625
  - C#
  - C++
  - 알고리즘
keywords: "백준 16625, 백준 16625번, BOJ 16625, DasBlinkenlights, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[16625번 - Das Blinkenlights](https://www.acmicpc.net/problem/16625)

## 설명
두 불빛이 각각 다른 주기로 깜빡일 때, 주어진 시간 내에 동시에 깜빡이는 순간이 있는지 판정하는 문제입니다.

<br>

## 접근법
두 주기의 최소공배수가 주어진 시간 이하이면 동시에 깜빡이는 순간이 존재합니다. 최소공배수는 두 수의 곱을 최대공약수로 나눠서 구할 수 있습니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static int Gcd(int a, int b) {
    while (b != 0) { var t = a % b; a = b; b = t; }
    return a;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var p = int.Parse(parts[0]);
    var q = int.Parse(parts[1]);
    var s = int.Parse(parts[2]);

    var lcm = p / Gcd(p, q) * q;
    Console.WriteLine(lcm <= s ? "yes" : "no");
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

  int p, q, s; cin >> p >> q >> s;

  int lcm = p / __gcd(p, q) * q;
  cout << (lcm <= s ? "yes" : "no") << "\n";

  return 0;
}
```
