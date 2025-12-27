---
layout: single
title: "[백준 8965] Circular Sequence (C#, C++) - soo:bak"
date: "2025-12-27 05:35:00 +0900"
description: 원형 DNA 서열에서 사전순으로 가장 작은 선형 서열을 찾는 문제
---

## 문제 링크
[8965번 - Circular Sequence](https://www.acmicpc.net/problem/8965)

## 설명
원형 서열이 주어질 때 자르는 위치를 하나 정해 선형 서열을 만들 수 있습니다. 가능한 선형 서열 중 사전순으로 가장 작은 것을 구하는 문제입니다.

<br>

## 접근법
서열을 두 번 이어붙이면 모든 회전을 부분 문자열로 얻을 수 있습니다. 각 시작 위치에서 길이 n만큼 잘라 비교하며 가장 작은 것을 선택합니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var t = int.Parse(Console.ReadLine()!);
    for (var _ = 0; _ < t; _++) {
      var s = Console.ReadLine()!;
      var n = s.Length;
      var doubled = s + s;

      var best = doubled.Substring(0, n);
      for (var i = 1; i < n; i++) {
        var cand = doubled.Substring(i, n);
        if (string.Compare(cand, best, StringComparison.Ordinal) < 0)
          best = cand;
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

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int t; cin >> t;
  while (t--) {
    string s; cin >> s;
    int n = (int)s.size();
    string dbl = s + s;
    string best = dbl.substr(0, n);
    for (int i = 1; i < n; i++) {
      string cand = dbl.substr(i, n);
      if (cand < best) best = cand;
    }
    cout << best << "\n";
  }

  return 0;
}
```
