---
layout: single
title: "[백준 12571] Rope Intranet (Small) (C#, C++) - soo:bak"
date: "2025-12-21 09:00:00 +0900"
description: "백준 12571번 C#, C++ 풀이 - 두 건물 사이 N개 선분의 교차 개수를 완전탐색으로 세는 문제"
tags:
  - 백준
  - BOJ
  - 12571
  - C#
  - C++
  - 알고리즘
keywords: "백준 12571, 백준 12571번, BOJ 12571, RopeIntranetSmall, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[12571번 - Rope Intranet (Small)](https://www.acmicpc.net/problem/12571)

## 설명
두 건물 사이를 잇는 선분들이 주어질 때 서로 교차하는 선분 쌍의 개수를 구하는 문제입니다.

<br>

## 접근법
두 선분이 교차하려면 한쪽 건물에서의 높이 순서와 반대쪽 건물에서의 높이 순서가 반대여야 합니다. 예를 들어 왼쪽에서는 첫 번째 선분이 더 높은데 오른쪽에서는 두 번째 선분이 더 높다면 두 선분은 교차합니다.

모든 선분 쌍을 확인하면서 이 조건을 만족하는 쌍의 개수를 셉니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);

    for (var tc = 1; tc <= t; tc++) {
      var n = int.Parse(Console.ReadLine()!);
      var a = new int[n];
      var b = new int[n];
      for (var i = 0; i < n; i++) {
        var parts = Console.ReadLine()!.Split();
        a[i] = int.Parse(parts[0]);
        b[i] = int.Parse(parts[1]);
      }

      var cnt = 0L;
      for (var i = 0; i < n; i++) {
        for (var j = i + 1; j < n; j++) {
          if ((long)(a[i] - a[j]) * (b[i] - b[j]) < 0) cnt++;
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
typedef vector<int> vi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;

  for (int tc = 1; tc <= t; tc++) {
    int n; cin >> n;
    vi a(n), b(n);
    for (int i = 0; i < n; i++)
      cin >> a[i] >> b[i];

    ll cnt = 0;
    for (int i = 0; i < n; i++) {
      for (int j = i + 1; j < n; j++) {
        if ((ll)(a[i] - a[j]) * (b[i] - b[j]) < 0) cnt++;
      }
    }

    cout << "Case #" << tc << ": " << cnt << "\n";
  }

  return 0;
}
```
