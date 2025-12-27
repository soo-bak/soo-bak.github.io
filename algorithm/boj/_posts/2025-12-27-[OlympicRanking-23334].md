---
layout: single
title: "[백준 23334] Olympic Ranking (C#, C++) - soo:bak"
date: "2025-12-27 06:05:00 +0900"
description: 금-은-동 순 사전식 비교로 최고 순위 국가를 찾는 문제
---

## 문제 링크
[23334번 - Olympic Ranking](https://www.acmicpc.net/problem/23334)

## 설명
국가별 금, 은, 동 메달 수가 주어질 때 금 → 은 → 동 순으로 사전식 비교해 최고의 국가를 출력하는 문제입니다. 최고 순위는 유일함이 보장됩니다.

<br>

## 접근법
입력을 순회하며 금, 은, 동 순서로 비교해 더 우수한 국가를 갱신합니다. 최고 순위가 유일하므로 동률 처리는 필요 없습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var n = int.Parse(Console.ReadLine()!);
    var bestName = "";
    int bg = -1, bs = -1, bb = -1;
    for (var i = 0; i < n; i++) {
      var line = Console.ReadLine()!;
      var parts = line.Split(' ', 4, StringSplitOptions.None);
      var g = int.Parse(parts[0]);
      var s = int.Parse(parts[1]);
      var b = int.Parse(parts[2]);
      var name = parts[3];

      if (g > bg || (g == bg && (s > bs || (s == bs && b > bb))))
        bg = g; bs = s; bb = b; bestName = name;
    }
    Console.WriteLine(bestName);
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
  string bestName;
  int bg = -1, bs = -1, bb = -1;
  string name;
  for (int i = 0; i < n; i++) {
    int g, s, b;
    cin >> g >> s >> b;
    getline(cin >> ws, name);

    if (g > bg || (g == bg && (s > bs || (s == bs && b > bb))))
      bg = g; bs = s; bb = b; bestName = name;
  }
  cout << bestName << "\n";

  return 0;
}
```
