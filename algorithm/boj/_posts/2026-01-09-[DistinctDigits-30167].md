---
layout: single
title: "[백준 30167] Distinct Digits (C#, C++) - soo:bak"
date: "2026-01-09 17:45:00 +0900"
description: "백준 30167번 C#, C++ 풀이 - 구간 [l, r]에서 모든 자릿수가 서로 다른 수를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 30167
  - C#
  - C++
  - 알고리즘
  - 구현
  - 브루트포스
keywords: "백준 30167, 백준 30167번, BOJ 30167, Distinct Digits, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[30167번 - Distinct Digits](https://www.acmicpc.net/problem/30167)

## 설명
정수 구간 [l, r]에서 자릿수가 모두 다른 정수 x를 아무거나 하나 찾는 문제입니다. 없으면 -1을 출력합니다.

<br>

## 접근법
먼저 l부터 r까지 순회하며 각 숫자를 확인합니다.

다음으로 각 숫자의 자릿수를 확인합니다. 이미 등장한 자릿수가 있으면 실패하고, 끝까지 겹치지 않으면 성공입니다.

이후 성공한 숫자를 찾으면 즉시 출력하고 종료합니다. 끝까지 찾지 못하면 -1을 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static bool DistinctDigits(int x) {
    var seen = new bool[10];
    if (x == 0)
      return true;
    while (x > 0) {
      var d = x % 10;
      if (seen[d])
        return false;
      seen[d] = true;
      x /= 10;
    }
    return true;
  }

  static void Main() {
    var parts = Console.ReadLine()!.Split();
    var l = int.Parse(parts[0]);
    var r = int.Parse(parts[1]);

    for (var x = l; x <= r; x++) {
      if (DistinctDigits(x)) {
        Console.WriteLine(x);
        return;
      }
    }
    Console.WriteLine(-1);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<bool> vb;

bool distinct(int x) {
  vb seen(10, false);
  if (x == 0)
    return true;
  while (x > 0) {
    int d = x % 10;
    if (seen[d])
      return false;
    seen[d] = true;
    x /= 10;
  }
  return true;
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int l, r;
  cin >> l >> r;
  for (int x = l; x <= r; x++) {
    if (distinct(x)) {
      cout << x << "\n";
      return 0;
    }
  }
  cout << -1 << "\n";

  return 0;
}
```
