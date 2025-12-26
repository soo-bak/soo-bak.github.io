---
layout: single
title: "[백준 9558] Between the Mountains (C#, C++) - soo:bak"
date: "2025-12-26 04:50:00 +0900"
description: 두 배열에서 차이가 최소인 값을 찾는 문제
---

## 문제 링크
[9558번 - Between the Mountains](https://www.acmicpc.net/problem/9558)

## 설명
두 산의 후보 고도 중에서 차이가 최소가 되는 한 쌍의 차이를 구하는 문제입니다.

<br>

## 접근법
먼저 두 고도 목록을 정렬합니다.

다음으로 두 포인터로 차이를 줄여가며 최소 차이를 갱신합니다.

마지막으로 구한 최소 차이를 출력합니다.

<br>

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
      for (var i = 0; i < n; i++) {
        a[i] = int.Parse(parts[idx++]);
      }

      var m = int.Parse(parts[idx++]);
      var b = new int[m];
      for (var i = 0; i < m; i++) {
        b[i] = int.Parse(parts[idx++]);
      }

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
