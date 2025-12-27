---
layout: single
title: "[백준 31134] A Hero Named Magnus (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 31134번 C#, C++ 풀이 - 최악의 경우에도 우승을 확정하려면 필요한 최소 경기 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 31134
  - C#
  - C++
  - 알고리즘
keywords: "백준 31134, 백준 31134번, BOJ 31134, HeroNamedMagnus, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[31134번 - A Hero Named Magnus](https://www.acmicpc.net/problem/31134)

## 설명
x번째 경기부터 항상 승리할 때, 최악의 경우에도 우승을 보장하는 최소 경기 수를 구하는 문제입니다.

<br>

## 접근법
특정 경기부터 항상 승리하고, 그 전까지는 최악의 경우 모두 패배한다고 가정합니다.

이 조건에서 과반수 이상의 승리를 보장하려면, 총 경기 수가 시작 경기 번호의 두 배에서 1을 뺀 값 이상이어야 합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    var sb = new StringBuilder();
    for (var i = 0; i < t; i++) {
      var x = long.Parse(Console.ReadLine()!);
      sb.AppendLine((2 * x - 1).ToString());
    }
    Console.Write(sb.ToString());
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

  int t; cin >> t;
  while (t--) {
    ll x; cin >> x;
    cout << 2 * x - 1 << "\n";
  }

  return 0;
}
```
