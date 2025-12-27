---
layout: single
title: "[백준 6609] 모기곱셈 (C#, C++) - soo:bak"
date: "2025-12-25 16:05:00 +0900"
description: "백준 6609번 C#, C++ 풀이 - 모기 성장 규칙을 N주 반복해 성충 수를 구하는 문제"
tags:
  - 백준
  - BOJ
  - 6609
  - C#
  - C++
  - 알고리즘
keywords: "백준 6609, 백준 6609번, BOJ 6609, MosquitoMultiplication, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[6609번 - 모기곱셈](https://www.acmicpc.net/problem/6609)

## 설명
초기 모기 상태와 규칙이 주어질 때, N번째 일요일 후의 성충 모기 수를 구하는 문제입니다.

<br>

## 접근법
일요일마다 성충, 번데기, 유충의 수가 `M = P / S`, `P = L / R`, `L = M * E`로 갱신됩니다.  
이 갱신을 N번 반복한 뒤 성충 수를 출력합니다.

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

    while (idx + 6 < parts.Length) {
      var m = int.Parse(parts[idx++]);
      var p = int.Parse(parts[idx++]);
      var l = int.Parse(parts[idx++]);
      var e = int.Parse(parts[idx++]);
      var r = int.Parse(parts[idx++]);
      var s = int.Parse(parts[idx++]);
      var n = int.Parse(parts[idx++]);

      for (var i = 0; i < n; i++) {
        var nm = p / s;
        var np = l / r;
        var nl = m * e;
        m = nm;
        p = np;
        l = nl;
      }

      sb.AppendLine(m.ToString());
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

  int m, p, l, e, r, s, n;
  while (cin >> m >> p >> l >> e >> r >> s >> n) {
    for (int i = 0; i < n; i++) {
      int nm = p / s;
      int np = l / r;
      int nl = m * e;
      m = nm;
      p = np;
      l = nl;
    }
    cout << m << "\n";
  }

  return 0;
}
```
