---
layout: single
title: "[백준 32089] 部員の変遷 (C#, C++) - soo:bak"
date: "2025-12-22 00:03:00 +0900"
description: "백준 32089번 C#, C++ 풀이 - 매년 신입이 들어오고 3년 뒤 졸업할 때 재학생 수의 최대값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 32089
  - C#
  - C++
  - 알고리즘
keywords: "백준 32089, 백준 32089번, BOJ 32089, ClubMemberTransitions, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[32089번 - 部員の変遷](https://www.acmicpc.net/problem/32089)

## 설명
연도별 신입 수가 주어질 때, 어느 해의 재학생 수가 최대인지 그 값을 출력하는 문제입니다.

<br>

## 접근법
각 해의 재학생 수는 해당 해와 직전 2년의 신입 수 합입니다.

이후 입력을 순회하며 최근 3년 합을 갱신해 최대값을 구합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var data = Console.In.ReadToEnd();
    var parts = data.Split(new[] { ' ', '\n', '\r', '\t' }, StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;

    while (idx < parts.Length) {
      var n = int.Parse(parts[idx++]);
      if (n == 0) break;

      long prev1 = 0, prev2 = 0;
      long best = 0;
      for (var i = 0; i < n; i++) {
        var cur = long.Parse(parts[idx++]);
        var total = cur + prev1 + prev2;
        if (total > best) best = total;
        prev2 = prev1;
        prev1 = cur;
      }

      Console.WriteLine(best);
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

  int n;
  while (cin >> n) {
    if (n == 0) break;

    ll prev1 = 0, prev2 = 0;
    ll best = 0;
    for (int i = 0; i < n; i++) {
      ll cur; cin >> cur;
      ll total = cur + prev1 + prev2;
      if (total > best) best = total;
      prev2 = prev1;
      prev1 = cur;
    }

    cout << best << "\n";
  }

  return 0;
}
```
