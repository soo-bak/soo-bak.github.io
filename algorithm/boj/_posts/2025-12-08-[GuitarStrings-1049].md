---
layout: single
title: "[백준 1049] 기타줄 (C#, C++) - soo:bak"
date: "2025-12-08 03:45:00 +0900"
description: 패키지 최소가와 낱개 최소가만 비교해 구입 조합을 결정하는 백준 1049번 기타줄 문제의 C# 및 C++ 풀이와 해설
---

## 문제 링크
[1049번 - 기타줄](https://www.acmicpc.net/problem/1049)

## 설명
끊어진 기타줄 n개를 사는 데 필요한 최소 비용을 구하는 문제입니다. 패키지는 6개 묶음이고, 낱개로도 살 수 있습니다.

<br>

## 접근법
여러 브랜드 중에서 가장 싼 패키지 가격과 가장 싼 낱개 가격만 알면 됩니다. 같은 브랜드일 필요가 없으므로 각각의 최솟값을 따로 구합니다.

6개를 살 때 패키지가 더 싸면 패키지를 사고, 낱개 6개가 더 싸면 낱개로 삽니다. 필요한 줄 수를 6으로 나눈 몫만큼 이 방식으로 구입합니다.

나머지 줄은 패키지 하나를 사는 것과 낱개로 채우는 것 중 더 싼 쪽을 선택합니다. 패키지가 낱개보다 싸면 필요한 것보다 많이 사더라도 패키지가 이득일 수 있습니다.

<br>

- - -

## Code

### C#
```csharp
using System;

class Program {
  static void Main() {
    var nm = Console.ReadLine()!.Split();
    var n = int.Parse(nm[0]);
    var m = int.Parse(nm[1]);
    var minPack = int.MaxValue;
    var minEach = int.MaxValue;
    for (var i = 0; i < m; i++) {
      var parts = Console.ReadLine()!.Split();
      var p = int.Parse(parts[0]);
      var e = int.Parse(parts[1]);
      if (p < minPack) minPack = p;
      if (e < minEach) minEach = e;
    }

    var cost = 0;
    var full = n / 6;
    if (minPack < minEach * 6) cost += minPack * full;
    else cost += minEach * 6 * full;

    var rem = n % 6;
    cost += Math.Min(minPack, rem * minEach);

    Console.WriteLine(cost);
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
  int minPack = 1001, minEach = 1001;
  for (int i = 0; i < m; i++) {
    int p, e; cin >> p >> e;
    minPack = min(minPack, p);
    minEach = min(minEach, e);
  }

  int cost = 0;
  int full = n / 6;
  if (minPack < minEach * 6) cost += minPack * full;
  else cost += minEach * 6 * full;

  int rem = n % 6;
  cost += min(minPack, rem * minEach);

  cout << cost << "\n";

  return 0;
}
```
