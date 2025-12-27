---
layout: single
title: "[백준 3943] 헤일스톤 수열 (C#, C++) - soo:bak"
date: "2025-12-24 12:30:00 +0900"
description: "백준 3943번 C#, C++ 풀이 - 헤일스톤 수열을 진행하며 최댓값을 구하는 문제"
tags:
  - 백준
  - BOJ
  - 3943
  - C#
  - C++
  - 알고리즘
  - 구현
  - 시뮬레이션
keywords: "백준 3943, 백준 3943번, BOJ 3943, HailstoneSequence, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[3943번 - 헤일스톤 수열](https://www.acmicpc.net/problem/3943)

## 설명
주어진 n으로 헤일스톤 수열을 만들 때 등장하는 최댓값을 출력하는 문제입니다.

<br>

## 접근법
n이 1이 될 때까지 규칙을 반복하면서 최댓값을 갱신합니다.

이때 짝수면 2로 나누고, 홀수면 3을 곱한 뒤 1을 더합니다.

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
      var best = n;
      while (n != 1) {
        if (n % 2 == 0) n /= 2;
        else n = 3 * n + 1;
        if (n > best) best = n;
      }
      sb.AppendLine(best.ToString());
    }

    Console.Write(sb.ToString());
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
    int n; cin >> n;
    int best = n;
    while (n != 1) {
      if (n % 2 == 0) n /= 2;
      else n = 3 * n + 1;
      if (n > best) best = n;
    }
    cout << best << "\n";
  }

  return 0;
}
```
