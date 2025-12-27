---
layout: single
title: "[백준 9558] Between the Mountains (C#, C++) - soo:bak"
date: "2025-12-26 04:50:00 +0900"
description: "백준 9558번 C#, C++ 풀이 - 두 배열에서 차이가 최소인 값을 찾는 문제"
tags:
  - 백준
  - BOJ
  - 9558
  - C#
  - C++
  - 알고리즘
keywords: "백준 9558, 백준 9558번, BOJ 9558, BetweenTheMountains, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[9558번 - Between the Mountains](https://www.acmicpc.net/problem/9558)

## 설명
두 산의 후보 고도 중에서 차이가 최소가 되는 한 쌍의 차이를 구하는 문제입니다.

<br>

## 접근법
두 배열을 정렬하면 투 포인터로 효율적으로 최소 차이를 찾을 수 있습니다.

두 포인터가 가리키는 값의 차이를 계산하고, 더 작은 쪽의 포인터를 앞으로 이동시킵니다. 작은 값을 키워야 차이가 줄어들 가능성이 있기 때문입니다.

이 과정에서 만난 모든 차이 중 최솟값이 답입니다.



- - -

## Code

### C#
```csharp
using System;
using System.Text;

class Program {
  static void Main() {
    var parts = Console.In.ReadToEnd().Split();
    var idx = 0;
    var t = int.Parse(parts[idx++]);
    var sb = new StringBuilder();

    for (var tc = 0; tc < t; tc++) {
      var n = int.Parse(parts[idx++]);
      var a = new int[n];
      for (var i = 0; i < n; i++)
        a[i] = int.Parse(parts[idx++]);

      var m = int.Parse(parts[idx++]);
      var b = new int[m];
      for (var i = 0; i < m; i++)
        b[i] = int.Parse(parts[idx++]);

      Array.Sort(a);
      Array.Sort(b);

      var i1 = 0;
      var i2 = 0;
      var best = int.MaxValue;
      while (i1 < n && i2 < m) {
        var diff = Math.Abs(a[i1] - b[i2]);
        if (diff < best) best = diff;

        if (a[i1] < b[i2]) i1++;
        else i2++;
      }

      sb.AppendLine(best.ToString());
    }

    Console.Write(sb);
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

  int t; cin >> t;

  for (int tc = 0; tc < t; tc++) {
    int n; cin >> n;
    vi a(n);
    for (int i = 0; i < n; i++)
      cin >> a[i];

    int m; cin >> m;
    vi b(m);
    for (int i = 0; i < m; i++)
      cin >> b[i];

    sort(a.begin(), a.end());
    sort(b.begin(), b.end());

    int i1 = 0;
    int i2 = 0;
    int best = INT_MAX;
    while (i1 < n && i2 < m) {
      int diff = abs(a[i1] - b[i2]);
      if (diff < best) best = diff;
      
      if (a[i1] < b[i2]) i1++;
      else i2++;
    }

    cout << best << "\n";
  }

  return 0;
}
```
