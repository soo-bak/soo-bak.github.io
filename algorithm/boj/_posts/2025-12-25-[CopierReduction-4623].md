---
layout: single
title: "[백준 4623] Copier Reduction (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 4623번 C#, C++ 풀이 - 이미지가 종이에 맞도록 최대 축소 비율을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 4623
  - C#
  - C++
  - 알고리즘
keywords: "백준 4623, 백준 4623번, BOJ 4623, CopierReduction, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[4623번 - Copier Reduction](https://www.acmicpc.net/problem/4623)

## 설명
이미지를 회전할 수 있을 때, 종이에 맞게 축소한 최대 정수 비율을 구하는 문제입니다.

<br>

## 접근법
회전하지 않은 경우와 90도 회전한 경우를 각각 계산합니다.  
각 경우의 최대 비율은 `min(C*100/A, D*100/B)`이며, 두 경우 중 큰 값을 택하되 100을 넘을 수는 없습니다.

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
    var sb = new StringBuilder();

    while (idx + 3 < parts.Length) {
      var a = int.Parse(parts[idx++]);
      var b = int.Parse(parts[idx++]);
      var c = int.Parse(parts[idx++]);
      var d = int.Parse(parts[idx++]);

      if (a == 0 && b == 0 && c == 0 && d == 0) break;

      var p1 = Math.Min(c * 100 / a, d * 100 / b);
      var p2 = Math.Min(c * 100 / b, d * 100 / a);
      var ans = Math.Min(100, Math.Max(p1, p2));
      sb.Append(ans).AppendLine("%");
    }

    Console.Write(sb);
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

  int a, b, c, d;
  while (cin >> a >> b >> c >> d) {
    if (a == 0 && b == 0 && c == 0 && d == 0) break;

    int p1 = min(c * 100 / a, d * 100 / b);
    int p2 = min(c * 100 / b, d * 100 / a);
    int ans = min(100, max(p1, p2));
    cout << ans << "%\n";
  }

  return 0;
}
```
