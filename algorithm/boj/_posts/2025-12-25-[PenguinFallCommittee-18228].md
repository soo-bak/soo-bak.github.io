---
layout: single
title: "[백준 18228] 펭귄추락대책위원회 (C#, C++) - soo:bak"
date: "2025-12-25 14:56:00 +0900"
description: "백준 18228번 C#, C++ 풀이 - 펭귄이 있는 구간을 떨어뜨리기 위해 양쪽에서 최소 비용을 선택하는 문제"
tags:
  - 백준
  - BOJ
  - 18228
  - C#
  - C++
  - 알고리즘
  - 구현
keywords: "백준 18228, 백준 18228번, BOJ 18228, PenguinFallCommittee, C# 풀이, C++ 풀이, 알고리즘"
---

## 문제 링크
[18228번 - 펭귄추락대책위원회](https://www.acmicpc.net/problem/18228)

## 설명
펭귄이 위치한 얼음을 포함하는 구간이 얼음 1이나 N을 포함하지 않게 만들기 위해, 깨야 하는 최소 힘을 구하는 문제입니다.

<br>

## 접근법
펭귄이 있는 얼음을 포함한 구간이 아래로 떨어지려면 왼쪽과 오른쪽에서 각각 하나 이상 깨져 있어야 합니다.

따라서 펭귄 기준 왼쪽 구간에서 가장 작은 힘과 오른쪽 구간에서 가장 작은 힘을 더하면 최소 힘이 됩니다.

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var data = Console.In.ReadToEnd();
    var parts = data.Split(new[] { ' ', '\n', '\r', '\t' },
                           StringSplitOptions.RemoveEmptyEntries);
    var idx = 0;
    var n = int.Parse(parts[idx++]);

    var leftMin = int.MaxValue;
    var rightMin = int.MaxValue;
    var right = false;

    for (var i = 0; i < n; i++) {
      var v = int.Parse(parts[idx++]);
      if (v == -1) {
        right = true;
        continue;
      }
      if (!right) {
        if (v < leftMin) leftMin = v;
      } else {
        if (v < rightMin) rightMin = v;
      }
    }

    Console.WriteLine(leftMin + rightMin);
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

  int n; cin >> n;
  int leftMin = 1e9, rightMin = 1e9;
  bool right = false;

  for (int i = 0; i < n; i++) {
    int v; cin >> v;
    if (v == -1) {
      right = true;
      continue;
    }
    if (!right) leftMin = min(leftMin, v);
    else rightMin = min(rightMin, v);
  }

  cout << leftMin + rightMin << "\n";

  return 0;
}
```
