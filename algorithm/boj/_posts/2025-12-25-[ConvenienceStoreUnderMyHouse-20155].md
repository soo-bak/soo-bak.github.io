---
layout: single
title: "[백준 20155] 우리 집 밑에 편의점이 있는데 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 20155번 C#, C++ 풀이 - 브랜드별 편의점 수의 최댓값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 20155
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 20155, 백준 20155번, BOJ 20155, ConvenienceStoreUnderMyHouse, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[20155번 - 우리 집 밑에 편의점이 있는데](https://www.acmicpc.net/problem/20155)

## 설명
각 편의점의 브랜드가 주어질 때, 모든 브랜드를 놓치지 않기 위한 최소 인원을 구하는 문제입니다.

<br>

## 접근법
하루에 한 브랜드만 잠복하므로 필요한 인원은 해당 브랜드의 편의점 수입니다.  
따라서 브랜드별 개수의 최댓값을 출력하면 됩니다.

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

    var cnt = new int[m + 1];
    for (var i = 0; i < n; i++) {
      var x = int.Parse(parts[idx++]);
      cnt[x]++;
    }

    var best = 0;
    for (var i = 1; i <= m; i++)
      if (cnt[i] > best) best = cnt[i];

    Console.WriteLine(best);
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

  int n, m; cin >> n >> m;
  vector<int> cnt(m + 1, 0);
  for (int i = 0; i < n; i++) {
    int x; cin >> x;
    cnt[x]++;
  }

  int best = 0;
  for (int i = 1; i <= m; i++)
    if (cnt[i] > best) best = cnt[i];

  cout << best << "\n";

  return 0;
}
```
