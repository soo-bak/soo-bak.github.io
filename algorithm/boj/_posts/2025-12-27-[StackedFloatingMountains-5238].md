---
layout: single
title: "[백준 5238] Stacked Floating Mountains (C#, C++) - soo:bak"
date: "2025-12-27 14:05:00 +0900"
description: "백준 5238번 C#, C++ 풀이 - 주어진 수열이 일반화된 피보나치 수열인지 판별하는 문제"
tags:
  - 백준
  - BOJ
  - 5238
  - C#
  - C++
  - 알고리즘
  - 수학
  - 구현
  - arithmetic
keywords: "백준 5238, 백준 5238번, BOJ 5238, StackedFloatingMountains, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[5238번 - Stacked Floating Mountains](https://www.acmicpc.net/problem/5238)

## 설명
수열이 주어질 때, 세 번째 항부터 이전 두 항의 합인지 확인하여 일반화된 피보나치 수열인지 판별하는 문제입니다.

<br>

## 접근법
세 번째 원소부터 순회하며 이전 두 원소의 합과 같은지 확인합니다.

모두 만족하면 YES, 하나라도 다르면 NO를 출력합니다.

<br>

- - -

## Code

### C#
```csharp
using System;
using System.Linq;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    while (n-- > 0) {
      var parts = Console.ReadLine()!.Split(' ', StringSplitOptions.RemoveEmptyEntries);
      var k = int.Parse(parts[0]);
      var x = parts.Skip(1).Select(int.Parse).ToArray();

      var ok = true;
      for (var i = 2; i < k; i++) {
        if (x[i] != x[i - 1] + x[i - 2]) ok = false;
      }

      Console.WriteLine(ok ? "YES" : "NO");
    }
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n; cin >> n;
  while (n--) {
    int k; cin >> k;
    vi x(k);
    for (int i = 0; i < k; i++)
      cin >> x[i];

    bool ok = true;
    for (int i = 2; i < k; i++) {
      if (x[i] != x[i - 1] + x[i - 2]) ok = false;
    }

    cout << (ok ? "YES" : "NO") << "\n";
  }

  return 0;
}
```

