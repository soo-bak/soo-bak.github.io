---
layout: single
title: "[백준 12250] New Lottery Game (Small) (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 12250번 C#, C++ 풀이 - A, B, K < 1000 범위에서 (x&y) < K인 쌍을 완전탐색으로 세는 문제"
tags:
  - 백준
  - BOJ
  - 12250
  - C#
  - C++
  - 알고리즘
keywords: "백준 12250, 백준 12250번, BOJ 12250, NewLotteryGameSmall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12250번 - New Lottery Game (Small)](https://www.acmicpc.net/problem/12250)

## 설명
두 수의 비트 AND 연산 결과가 특정 값보다 작은 쌍의 개수를 구하는 문제입니다.

<br>

## 접근법
범위가 1000 이하로 작아서 모든 쌍을 확인하는 완전탐색이 가능합니다. 두 수 x와 y를 0부터 각각 A-1, B-1까지 순회하면서 비트 AND 결과가 K보다 작으면 개수를 증가시킵니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);

    for (var tc = 1; tc <= t; tc++) {
      var parts = Console.ReadLine()!.Split();
      var a = int.Parse(parts[0]);
      var b = int.Parse(parts[1]);
      var k = int.Parse(parts[2]);

      var cnt = 0L;
      for (var x = 0; x < a; x++) {
        for (var y = 0; y < b; y++) {
          if ((x & y) < k) cnt++;
        }
      }

      Console.WriteLine($"Case #{tc}: {cnt}");
    }
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

  for (int tc = 1; tc <= t; tc++) {
    int a, b, k; cin >> a >> b >> k;

    ll cnt = 0;
    for (int x = 0; x < a; x++) {
      for (int y = 0; y < b; y++) {
        if ((x & y) < k) cnt++;
      }
    }

    cout << "Case #" << tc << ": " << cnt << "\n";
  }

  return 0;
}
```
