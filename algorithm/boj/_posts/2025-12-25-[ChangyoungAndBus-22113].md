---
layout: single
title: "[백준 22113] 창영이와 버스 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: 지정된 버스 순서의 환승 요금 합을 계산하는 문제
---

## 문제 링크
[22113번 - 창영이와 버스](https://www.acmicpc.net/problem/22113)

## 설명
버스 환승 순서와 모든 환승 요금이 주어질 때, 순서대로 환승할 때 드는 총 비용을 구하는 문제입니다.

<br>

## 접근법
버스 순서를 배열로 저장하고, 연속한 두 버스의 요금을 더합니다.  
요금 표는 N×N이므로 입력 그대로 배열에 저장해 참조합니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var n = int.Parse(parts[idx++]);
    var m = int.Parse(parts[idx++]);

    var route = new int[m];
    for (var i = 0; i < m; i++)
      route[i] = int.Parse(parts[idx++]) - 1;

    var cost = new int[n, n];
    for (var i = 0; i < n; i++)
      for (var j = 0; j < n; j++)
        cost[i, j] = int.Parse(parts[idx++]);

    var sum = 0;
    for (var i = 0; i < m - 1; i++)
      sum += cost[route[i], route[i + 1]];

    Console.WriteLine(sum);
  }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;

typedef vector<int> vi;
typedef vector<vi> vvi;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m; cin >> n >> m;
  vi route(m);
  for (int i = 0; i < m; i++) {
    cin >> route[i];
    route[i]--;
  }

  vvi cost(n, vi(n));
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      cin >> cost[i][j];

  int sum = 0;
  for (int i = 0; i < m - 1; i++)
    sum += cost[route[i]][route[i + 1]];

  cout << sum << "\n";

  return 0;
}
```
