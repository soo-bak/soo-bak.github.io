---
layout: single
title: "[백준 32500] Dishonest Lottery (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 32500번 C#, C++ 풀이 - 등장 횟수가 20%를 초과하는 번호를 찾는 문제"
tags:
  - 백준
  - BOJ
  - 32500
  - C#
  - C++
  - 알고리즘
keywords: "백준 32500, 백준 32500번, BOJ 32500, DishonestLottery, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32500번 - Dishonest Lottery](https://www.acmicpc.net/problem/32500)

## 설명
주어진 추첨 결과에서 20%를 초과해 등장한 번호를 출력하는 문제입니다.

<br>

## 접근법
총 추첨 횟수의 20%를 초과해 등장한 번호가 의심 대상입니다.

따라서 1부터 50까지 각 번호의 등장 횟수를 세고, 조건을 만족하는 번호를 출력합니다.

- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var data = Console.In.ReadToEnd();
    var parts = data.Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var cnt = new int[51];

    for (var i = 0; i < 10 * n; i++) {
      for (var j = 0; j < 5; j++) {
        var x = int.Parse(parts[idx++]);
        cnt[x]++;
      }
    }

    var sb = new StringBuilder();
    var first = true;
    for (var i = 1; i <= 50; i++) {
      if (cnt[i] > 2 * n) {
        if (!first) sb.Append(' ');
        sb.Append(i);
        first = false;
      }
    }

    Console.WriteLine(first ? "-1" : sb.ToString());
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

  int n; cin >> n;
  int cnt[51] = {};
  for (int i = 0; i < 10 * n; i++) {
    for (int j = 0; j < 5; j++) {
      int x; cin >> x;
      cnt[x]++;
    }
  }

  bool first = true;
  for (int i = 1; i <= 50; i++) {
    if (cnt[i] > 2 * n) {
      if (!first) cout << " ";
      cout << i;
      first = false;
    }
  }

  if (first) cout << -1;
  cout << "\n";

  return 0;
}
```
